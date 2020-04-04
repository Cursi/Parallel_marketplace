"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2020
"""

from threading import Thread
from time import sleep


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time

        self.consumer_id = marketplace.new_cart()

        Thread.__init__(self, group=None, **kwargs)

    def write_parsed_order(self, bought_products):
        """
        Function that parses the final list with the bought products and prints it to STDOUT
        """
        for product in bought_products:
            print(Thread.getName(self), "bought", product[0])

    def run(self):
        for current_cart in self.carts:
            for current_operation in current_cart:
                for _ in range(0, int(current_operation["quantity"])):
                    if current_operation["type"] == "add":
                        while not self.marketplace.add_to_cart(
                                self.consumer_id, current_operation["product"]):
                            sleep(self.retry_wait_time)
                    elif current_operation["type"] == "remove":
                        self.marketplace.remove_from_cart(
                            self.consumer_id, current_operation["product"])

        self.write_parsed_order(self.marketplace.place_order(self.consumer_id))
