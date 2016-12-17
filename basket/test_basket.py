import pytest

import basket.basket as basket
import basket.product as product
import basket.offer as offer


@pytest.fixture
def goods():
    return {
      'soup': product.Product('soup', 65, 'tin'),
      'bread': product.Product('bread', 80, 'loaf'),
      'milk': product.Product('milk', 130, 'bottle'),
      'apples': product.Product('apples', 100, 'bag'), }


@pytest.fixture
def goods_empty():
    return {}


@pytest.fixture
def offer_def():
    return {'id': 1, 'title': 'Apples 10% off',
            'qualifying_product': 'apples',
            'qualifying_qty': 1,
            'discounted_product': 'apples',
            'discount_percent': 10}

@pytest.fixture
def offers(offer_def):
    return [offer.Offer(offer_def)]


@pytest.fixture
def offers_empty():
    return []


def test_basket(goods, offers):
    b = basket.Basket(goods, offers)
    assert b.goods is goods
    assert b.offers is offers
    assert b.items == []
    assert b.discounts == []


def test_add_item(goods, offers):
    b = basket.Basket(goods, offers)
    assert b.add('apples')
    assert len(b.items) == 1
    assert b.subtotal == 100
    assert b.total == 100


def test_add_item_no_goods(goods_empty, offers):
    b = basket.Basket(goods_empty, offers)
    assert b.goods is goods_empty
    assert b.offers is offers
    assert b.add('apples') is False


def test_add_item_no_offers(goods, offers_empty):
    b = basket.Basket(goods, offers_empty)
    assert b.goods is goods
    assert b.offers is offers_empty
    assert b.add('apples')
    b.calculate_discounts()
    assert b.subtotal == 100
    assert b.total == 100
    assert not len(b.discounted_items)


def test_discount(goods, offers):
    b = basket.Basket(goods, offers)
    assert b.add('apples')
    assert len(b.items) == 1
    assert b.subtotal == 100
    b.calculate_discounts()
    assert b.total == 90
    assert len(b.discounted_items) == 1
    assert b.discounted_items[0] is b.items[0]


def test_add_items_discount(goods, offers):
    b = basket.Basket(goods, offers)
    assert b.add('apples')
    assert b.add('apples')
    assert len(b.items) == 2
    assert b.subtotal == 200
    b.calculate_discounts()
    assert b.total == 180
    assert len(b.discounted_items) == 2
    assert b.discounted_items[0] is b.items[0]
    assert b.discounted_items[1] is b.items[1]
