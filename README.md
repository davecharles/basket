# basket
Simple shoppping basket application developed for an off-line python coding test.

## Usage
Check out the repo and navigate to `basket/`.  There are two json data files used by
the application which are self explanatory:
 - goods.json
 - offers.json

Execute as follows to show help usage:
```
python -m basket -h
usage: basket [-h] [-v] [--goods GOODS] [--offers OFFERS] [--verbose]
              item [item ...]

positional arguments:
  item             One or more items for the basket. Only items listed in
                   goods.json are accepted.

optional arguments:
  -h, --help       show this help message and exit
  -v, --version    show program's version number and exit
  --goods GOODS    Path of the goods json file
  --offers OFFERS  Path of the offers json file
  --verbose        Verbose output```
```
  
## Examples
```
$ python -m basket apples milk
Subtotal: £2.30
Apples 10% off: -10p
Total: £2.20
```
```
$ python -m basket milk soup eggs --verbose
2016-12-17 14:03:02 INFO: Item 'eggs' not in stock
Subtotal: £1.95
(No offers available)
Total: £1.95
```
```
$ python -m basket milk soup soup bread apples
Subtotal: £4.40
2 tins soup get you a half price loaf: -40p
Apples 10% off: -10p
Total: £3.90
```

