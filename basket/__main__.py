"""Basket.

Simple application that prices a basket of goods taking into account
any special offers.  The program accepts a list of items in the basket
and outputs the subtotal, the special offer discounts and the final price.

Information about goods available for purchase (product names, units and
price) are loaded (by default) from the json file ``goods.json``.  Special
offers are are loaded (by default) from the json file ``offers.json``.
"""


import argparse
import json
import sys
import time

from basket import product
from basket import offer
from basket import basket


LOGGING = False

# Log levels
INFO = 'INFO'
ERROR = 'ERROR'


def log(message, level=INFO):
    """Simple logger.

    :param str message: Log message
    :param str level: Log level
    """
    if LOGGING:
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        print('{} {}: {}'.format(now, level, message))


def parse_args(argv=None):
    """Parse command line arguments.

    :param list argv: Args to parse.
    """
    parser = argparse.ArgumentParser(prog='basket')
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='%(prog)s 0.1',
    )
    parser.add_argument(
        '--goods',
        help='Path of the goods json file',
        default='goods.json',
        dest='goods',
    )
    parser.add_argument(
        '--offers',
        help='Path of the offers json file',
        default='offers.json',
        dest='offers',
    )
    parser.add_argument(
        'items',
        metavar='item',
        type=str,
        nargs='+',
        help='One or more items for the basket.  Only items listed in '
             'goods.json are accepted.')
    parser.add_argument(
        '--verbose',
        help='Verbose output',
        default=False,
        action='store_true',
        dest='verbose',
    )
    return parser.parse_args(argv)


def load_json(json_file_path):
    """Load json data.

    :param str json_file_path: Path to json file to load.
    """
    data = None
    try:
        with open(json_file_path) as f:
            data = json.load(f)
    except EnvironmentError:
        log('No such file or directory: {}'.format(json_file_path), ERROR)
    except ValueError as e:  # JSONDecodeError only supported from 3.5
        log('Failed to parse data file {}: {}'.format(
            json_file_path, e), ERROR)
    return data


def load_goods(goods_file_path):
    """Load goods definitions.

    Load goods definition data describing the goods this program will
    accept including product names, units and price.

    :param str goods_file_path: Path to goods file.
    :return dict: Dictionary of product.Product instances.
    """
    goods = {}
    data = load_json(goods_file_path)
    if data is None:
        log('No stock found in goods data', INFO)
    else:
        # Build products list
        for prod in data:
            try:
                p = product.Product(prod['name'], prod['price'], prod['unit'])
                goods[p.name] = p
            except ValueError as e:
                log('Failed to load a product with data: {} ({})'.format(
                    prod, e), ERROR)
    return goods


def load_offers(offers_file_path):
    """Load offers.

    Load offers data that specifies discounts that can be applied
    to goods purchased.

    :param str offers_file_path: Path to offers file.
    :return list: List of offer.Offer instances.
    """
    offers = []
    data = load_json(offers_file_path)
    if data:
        for prod_offer in data:
            try:
                offers.append(offer.Offer(prod_offer))
            except (ValueError, KeyError) as e:
                log('Failed to load offer with data: {} ({})'.format(
                    prod_offer, e), ERROR)
    return offers


def main(argv=None):
    """Program entry point.

    Parses any arguments, invokes ``load_goods`` and ``load_offers`` (to
    load the available goods and offers) and constructs a ``basket``
    instance, giving it the available products in stock (``goods``) and any
    prevailing offers (``offers``).  For each product item specified on the
    command line, we add it to the basket.  When all items have been added
    we query ``basket`` for a sub-total, discounts that could be applied
    and total price, which is output.

    :param list argv: Command line arguments.
    """
    # Parse arguments
    args = parse_args(argv)
    global LOGGING
    LOGGING = args.verbose

    # Load available goods and offers
    goods = load_goods(args.goods)
    offers = load_offers(args.offers)

    # Make a basket and fill
    shopping_basket = basket.Basket(goods, offers)
    for item in args.items:
        if not shopping_basket.add(item):
            log('Item not in stock', INFO)

    # Print the results
    print('Subtotal: £{:.2f}'.format(shopping_basket.subtotal/100))
    shopping_basket.calculate_discounts()
    if shopping_basket.discounted_items:
        for item in shopping_basket.discounted_items:
            print(item.discount_message)
    else:
        print('(No offers available)')
    print('Total: £{:.2f}'.format(shopping_basket.total/100))


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main())
