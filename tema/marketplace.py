"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2020
"""


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """

    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer

        self.products_from_producers = {}
        self.last_producer_id = 0

        self.carts_for_consumers = {}
        self.last_consumer_id = 0

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        self.last_producer_id += 1
        self.products_from_producers[self.last_producer_id] = []

        return self.last_producer_id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        if len(self.products_from_producers[producer_id]) < self.queue_size_per_producer:
            self.products_from_producers[producer_id].append(product)
            return True

        return False

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        self.last_consumer_id += 1
        self.carts_for_consumers[self.last_consumer_id] = []

        return self.last_consumer_id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        for (producer_id, producer_queue) in self.products_from_producers.items():
            if product in producer_queue:
                self.carts_for_consumers[cart_id].append(((product, producer_id)))
                producer_queue.remove(product)
                return True

        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        cart_item = None

        for cart_item in enumerate(self.carts_for_consumers[cart_id]):
            if cart_item[1][0] == product:
                producer_id = cart_item[1][1]
                break

        self.products_from_producers[producer_id].append(product)
        del self.carts_for_consumers[cart_id][cart_item[0]]

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        return self.carts_for_consumers[cart_id]
