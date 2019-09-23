from floyd_warshall.exchange_msg_handler import ExchangeMsgHandler
from common.loggable import Loggable


class ExchangeLineReader(Loggable):
    """"
        Creates a exchange line reader which receives messages from the exchange and passes them
        to a message handler, option to log the message, so we can replay the data in a simulated
        environment
        exchange -> LINE_READER -> message_handler -> price_engine
        Note: One to One relationship with Msg Parsers
    """
    def __init__(self):
        super(Loggable, self).__init__()
        self.simulated_exchange = None
        self._message_handler = None

    def connect_to_exchange(self, exchange):
        """ register as an observer for exchange messages """
        self.simulated_exchange = exchange
        self.simulated_exchange.register_client_line_reader(self)
        self.init_logging("LR-" + self.simulated_exchange.name)

    def register_message_handler(self, handler):
        """ Allow only a single message handler to connect,
            must implement Interface method process_message """
        self._message_handler = handler

    def receive_message(self, msg):
        """ called from the exchange to simulate arrive of an exchange message """
        if self._message_handler is not None:
            self._message_handler.process_message(msg)
        self.log_info(msg)
