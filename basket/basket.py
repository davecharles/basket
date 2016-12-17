"""Basket module."""

import copy


class Basket:
    """Class that encapsulates a basket of goods to be purchased."""
    def __init__(self, goods, offers):
        """
        :param dict goods: The goods available.
        :param list offers: The offers available.
        :return: None
        """
        self.goods = goods
        self.offers = offers
        self.items = []
        self.discounts = []

    def calculate_discounts(self):
        """Calculate discounts.

        Determine what the discounts are based on the current list if items.
        First we reset any previously calculated discounts on products in
        ``self.items``.  The for each offer we ascertain the number of
        qualifying items and how that translates into discounts to apply.
        Finally we assemble a list of products to apply the discounts to
        and apply as many discounts as we have qualified for in this
        particular offer.
        """
        # Clear any previously applied offers
        for p in self.items:
            p.clear_offer()

        for offer in self.offers:
            # Do we have enough qualifying products for this offer?
            qualifying = [p for p in self.items
                          if p.name == offer.qualifying_product]
            qty_qualifying = len(qualifying)

            # And how many times can we apply the discount?
            num_discounts = qty_qualifying // offer.qualifying_qty

            if not num_discounts:
                continue

            # Apply discounts to each product discounted in the offer,
            # up to the number of discounts earned (note the discounted
            # product might not be the qualifying product).
            prods_nominated_discount = [p for p in self.items
                                        if p.name == offer.discounted_product]

            for prod in prods_nominated_discount:
                prod.apply_offer(offer)
                num_discounts -= 1
                if not num_discounts:
                    break

    def add(self, item):
        """Add an item to the basket.

        Adds a product to the list if it is in stock.  We take a
        shallow copy of the corresponding item in the supplied goods list.

        :param str item: The name of an item to be added to the basket.
        :return: True if the item is added and False otherwise.
        """
        try:
            self.items.append(copy.copy(self.goods[item.lower()]))
        except KeyError:
            return False
        return True

    @property
    def discounted_items(self):
        """Returns a list of discounted items.

        :return: List of items in the basket with discounts applied
          (if any).
        """
        return [p for p in self.items if p.has_offer]

    @property
    def total(self):
        """The total price of the basket with discounts applied.

        :return: Price in pence.
        """
        return sum(product.discounted_price for product in self.items)

    @property
    def subtotal(self):
        """The total price of the basket without discounts applied.

        :return: Price in pence.
        """
        return sum(product.price for product in self.items)
