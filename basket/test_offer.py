import pytest

import basket.offer as offer


@pytest.mark.parametrize('qualifying_product', ['apples', 'Apples', 'appLeS'])
@pytest.mark.parametrize('qualifying_qty', [1, 1.0, '1'])
@pytest.mark.parametrize('discounted_product', ['appLes', 'Apples'])
@pytest.mark.parametrize('discount_percent', [10, '10', 10.0])
def test_offer(qualifying_product, qualifying_qty, discounted_product,
              discount_percent):
    offer_def = {'id': 1,
                 'title': 'Apples 10% off',
                 'qualifying_product': qualifying_product,
                 'qualifying_qty': qualifying_qty,
                 'discounted_product': discounted_product,
                 'discount_percent': discount_percent}
    o = offer.Offer(offer_def)
    assert o.offer_id == 1
    assert o.title == 'Apples 10% off'
    assert o.qualifying_product == 'apples'
    assert o.qualifying_qty == 1
    assert o.discounted_product == 'apples'
    assert o.discount_percent == 10


def test_bad_offer():
    offer_def = {'id': 1,
                 'title': 'Apples 10% off',
                 'qualifying_product': 'Apples',
                 'qualifying_qty': 0,
                 'discounted_product': 'Apples',
                 'discount_percent': 10}
    with pytest.raises(ValueError) as e:
        offer.Offer(offer_def)
    assert 'Unacceptable value for qualifying_qty' in str(e)
