"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2020
"""

from threading import Thread
from time import sleep


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time

        self.producer_id = marketplace.register_producer()
        self.current_product_index = 0

        Thread.__init__(self, group=None, **kwargs)

    def get_next_product_index(self, current_index):
        """
        Function that returns the index for the next product to be produced
        """
        if current_index + 1 == len(self.products):
            return 0

        return current_index + 1

    def run(self):
        while True:
            for _ in range(0, int(self.products[self.current_product_index][1])):
                sleep(float(self.products[self.current_product_index][2]))

                while not self.marketplace.publish(
                        self.producer_id,
                        self.products[self.current_product_index][0]):
                    sleep(self.republish_wait_time)

            self.current_product_index = self.get_next_product_index(
                self.current_product_index)
