from messages.price_update import PriceUpdate
from common.loggable import Loggable


class ExchangeMsgHandler(Loggable):
    """"
        Creates a exchange msg reader
        1. Make sure message in correct format
        2. Make sure and not an old message
        Before passing onto clients
        exchange -> line_reader -> MESSAGE_HANDLER -> price_engine

    """
    def __init__(self):
        super(Loggable, self).__init__()
        self._exchange_line_reader = None
        self._price_update_clients = []
        self._last_message_times = {}

    def connect_to_line_reader(self, exchange_line_reader):
        self._exchange_line_reader = exchange_line_reader
        self._exchange_line_reader.register_message_handler(self)
        self.init_logging("MP-" + exchange_line_reader.simulated_exchange.name)

    def register_price_update_client(self, price_engine):
        """ Allow multiple PriceEngines to connect,
            use an Interface so process_update_message method implemented"""
        self._price_update_clients.append(price_engine)

    def process_message(self, msg):
        """ Splits the message into components and validates them """
        [time, exch, curr_1, curr_2, fwd, bkwd] = msg.split()

        # can use string cmp as we have a timestamp format
        try:
            if time < self._last_message_times[curr_1, curr_2]:
                self.log_info("Ignored Message - " + msg)
                return
        except KeyError:
            self.log_info("New Currency Pair" + curr_1 + curr_2)
            self._last_message_times[curr_1, curr_2] = ""

        self._last_message_times[curr_1, curr_2] = time

        price_update_msg = PriceUpdate(exch, curr_1, curr_2, fwd, bkwd)
        for price_update_client in self._price_update_clients:
            price_update_client.process_update_message(price_update_msg)
