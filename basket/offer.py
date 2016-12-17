"""Offer module."""


class Offer:
    """Class that encapsulates a product offer."""

    def __init__(self, offer_def):
        """
        Given a definition, constructs a product offer that can be applied to
        purchases.

        :param offer_def: Dictionary like object defining the offer and
          should include values for they keys ``id``, ``title``,
          ``qualifying_product``, ``qualifying_qty``, ``discounted_product``
          and ``discount_percent``.
        :raises: ValueError if the qualifying qty is invalid.
        """
        self.offer_id = offer_def['id']
        self.title = offer_def['title']
        self.qualifying_product = offer_def['qualifying_product'].lower()
        self.qualifying_qty = int(offer_def['qualifying_qty'])
        if not self.qualifying_qty:
            raise ValueError('Unacceptable value for qualifying_qty')
        self.discounted_product = offer_def['discounted_product'].lower()
        self.discount_percent = float(offer_def['discount_percent'])
