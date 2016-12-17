"""Product module."""


class Product:
    """Class that encapsulates a product item to be purchased."""

    def __init__(self, name, price, unit):
        """
        Given a name, price and unit constructs a product that can be
        used in purchases.

        :param name: Name of the product.
        :param price: Price of the product in pence.
        :param unit: The product's unit of quantity, e.g. bag or loaf.
        """
        self.name = name.lower()
        self.price = int(price)  # Assumed price is in pence
        self.unit = unit.lower()
        self._offer = None

    def apply_offer(self, offer):
        """Apply an offer to this product.

        :param: offer.Offer instance.
        """
        self._offer = offer

    def clear_offer(self):
        """Remove any offer applied to this product."""
        self._offer = None

    @property
    def has_offer(self):
        """Check if product has an offer applied.

        :return: True if the product has an offer applied and
          False otherwise.
        """
        return self._offer is not None

    @property
    def discounted_price(self):
        """The product price with discount applied.

        :return: Price in pence.
        """
        if self._offer:
            return int(self.price - self.discount_amount)
        return self.price

    @property
    def discount_amount(self):
        """The amount of discount earned.

        :return: Discount amount in pence.
        """
        if self._offer:
            return int(self.price * self._offer.discount_percent / 100.0)
        return 0

    @property
    def discount_message(self):
        """Returns a message that represents the applied offer.

        :return: String message.
        """
        discount_amount_str = '-£{:.2f}'.format(self.discount_amount/100)
        if self.discount_amount < 100:
            discount_amount_str = '-{}p'.format(self.discount_amount)
        if self._offer:
            return '{}: {}'.format(
                self._offer.title, discount_amount_str)
        return None
