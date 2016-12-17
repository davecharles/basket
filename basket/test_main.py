import time

import pytest

import basket.__main__ as main


@pytest.fixture
def goods_json():
    return """[
    {
      "name": "Soup", "price": 65, "unit": "Tin"
    },
    {
      "name": "Bread", "price": 80, "unit": "Loaf"
    },
    {
      "name": "Milk", "price": 130, "unit": "Bottle"
    },
    {
      "name": "Apples", "price": 100, "unit": "Bag"
    }]"""


@pytest.fixture
def faulty_goods_json():
    return """[
    {
      "name": "Apples", "price": "100.0", "unit": "Bag"
    }]"""


@pytest.fixture
def faulty_offers_json():
    return """[
    {
      "id": 1,
      "title": "Apples 10% off",
      "qualifying_product": "Apples",
      "qualifying_qty": 0,
      "discounted_product": "Apples",
      "discount_percent": 10
    }]"""


@pytest.fixture
def ok_json():
    return """[
    {
      "hello": "json", "int": 10, "float": 1.2, "list": [1, 2, 3]
    }]"""


@pytest.fixture
def bad_json():
    return 'foo'


@pytest.fixture
def offers_json():
    return """[
    {
      "id": 1,
      "title": "Apples 10% off",
      "qualifying_product": "Apples",
      "qualifying_qty": 1,
      "discounted_product": "Apples",
      "discount_percent": 10
    },
    {
      "id": 2,
      "title": "2 tins soup get you a half price loaf",
      "qualifying_product": "Soup",
      "qualifying_qty": 2,
      "discounted_product": "Bread",
      "discount_percent": 50
    }]"""


@pytest.fixture
def empty_json():
    return '[]'


@pytest.fixture
def ok_json_file(tmpdir, ok_json):
    tmpfile = tmpdir.join('ok.json')
    with tmpfile.open('w') as f:
        f.write(ok_json)
    return str(tmpfile)


@pytest.fixture
def bad_json_file(tmpdir, bad_json):
    tmpfile = tmpdir.join('bad.json')
    with tmpfile.open('w') as f:
        f.write(bad_json)
    return str(tmpfile)


@pytest.fixture
def goods_json_file(tmpdir, goods_json):
    tmpfile = tmpdir.join('goods.json')
    with tmpfile.open('w') as f:
        f.write(goods_json)
    return str(tmpfile)


@pytest.fixture
def faulty_goods_json_file(tmpdir, faulty_goods_json):
    tmpfile = tmpdir.join('faulty.json')
    with tmpfile.open('w') as f:
        f.write(faulty_goods_json)
    return str(tmpfile)


@pytest.fixture
def offers_json_file(tmpdir, offers_json):
    tmpfile = tmpdir.join('offers.json')
    with tmpfile.open('w') as f:
        f.write(offers_json)
    return str(tmpfile)


@pytest.fixture
def faulty_offers_json_file(tmpdir, faulty_offers_json):
    tmpfile = tmpdir.join('faulty_offers.json')
    with tmpfile.open('w') as f:
        f.write(faulty_offers_json)
    return str(tmpfile)


@pytest.fixture
def empty_json_file(tmpdir, empty_json):
    tmpfile = tmpdir.join('empty.json')
    with tmpfile.open('w') as f:
        f.write(empty_json)
    return str(tmpfile)


def test_log(capsys):
    main.LOGGING = True
    main.log('foo')
    stdout, _ = capsys.readouterr()
    assert isinstance(time.strptime(stdout[:19], '%Y-%m-%d %H:%M:%S'),
                      time.struct_time)
    assert 'INFO: foo' in stdout


def test_log_error(capsys):
    main.LOGGING = True
    main.log('foo', level=main.ERROR)
    stdout, _ = capsys.readouterr()
    assert 'ERROR: foo' in stdout


def test_log_quiet(capsys):
    main.LOGGING = False
    main.log('foo')
    stdout, _ = capsys.readouterr()
    assert not len(stdout)


class TestParseArgs:

    def test_version(self, capsys):
        with pytest.raises(SystemExit):
            main.parse_args(['--version'])
        stdout, _ = capsys.readouterr()
        assert 'basket' in stdout

    def test_goods_default(self):
        args = main.parse_args(['apple'])
        assert args.goods == 'goods.json'

    def test_offers_default(self):
        args = main.parse_args(['apple'])
        assert args.offers == 'offers.json'

    def test_goods_override(self):
        args = main.parse_args(['--goods=foo.json', 'apple'])
        assert args.goods == 'foo.json'

    def test_offers_override(self):
        args = main.parse_args(['--offers=foo.json', 'apple'])
        assert args.offers == 'foo.json'

    def test_verbose(self):
        args = main.parse_args(['--verbose', 'apple'])
        assert args.verbose is True


def test_load_json(ok_json_file):
    assert main.load_json(ok_json_file) is not None


def test_load_json_no_file(capsys):
    main.LOGGING = True
    assert main.load_json('foo.json') is None
    stdout, _ = capsys.readouterr()
    assert 'ERROR: No such file or directory: foo.json' in stdout


def test_load_json_bad_file(bad_json_file, capsys):
    main.LOGGING = True
    assert main.load_json(bad_json_file) is None
    stdout, _ = capsys.readouterr()
    assert 'ERROR: Failed to parse data file' in stdout
    assert 'bad.json' in stdout


def test_load_goods(goods_json_file):
    products = main.load_goods(goods_json_file)
    assert products
    assert len(products) == 4
    assert all(k in products for k in ('soup', 'bread', 'milk', 'apples'))
    assert products['soup'].price == 65
    assert products['soup'].unit == 'tin'
    assert products['bread'].price == 80
    assert products['bread'].unit == 'loaf'
    assert products['milk'].price == 130
    assert products['milk'].unit == 'bottle'
    assert products['apples'].price == 100
    assert products['apples'].unit == 'bag'


def test_load_goods_no_stock(empty_json_file):
    products = main.load_goods(empty_json_file)
    assert products == {}
    assert len(products) is 0


def test_load_goods_bad_item(faulty_goods_json_file, capsys):
    main.LOGGING = True
    products = main.load_goods(faulty_goods_json_file)
    stdout, _ = capsys.readouterr()
    assert 'Failed to load a product with data' in stdout
    assert '(invalid literal for int() with base 10: \'100.0\'' in stdout
    assert len(products) is 0


def test_load_offers(offers_json_file):
    offers = main.load_offers(offers_json_file)
    assert offers
    assert len(offers) == 2
    assert offers[0].offer_id == 1
    assert offers[1].offer_id == 2
    assert offers[0].title == 'Apples 10% off'
    assert offers[1].title == '2 tins soup get you a half price loaf'


def test_load_offers_bad_item(faulty_offers_json_file, capsys):
    main.LOGGING = True
    offers = main.load_offers(faulty_offers_json_file)
    stdout, _ = capsys.readouterr()
    assert 'Failed to load offer with data' in stdout
    assert '(Unacceptable value for qualifying_qty)' in stdout
    assert len(offers) is 0


def test_main(capsys):
    main.main(['apples'])
    stdout, _ = capsys.readouterr()
    expectd_op = 'Subtotal: £1.00\nApples 10% off: -10p\nTotal: £0.90'
    assert expectd_op in stdout


def test_main_unknown_prod(capsys):
    main.main(['pie', '--verbose'])
    stdout, _ = capsys.readouterr()
    expectd_op = ('INFO: Item \'pie\' not in stock\nSubtotal: £0.00\n'
                  '(No offers available)\nTotal: £0.00')
    assert expectd_op in stdout
