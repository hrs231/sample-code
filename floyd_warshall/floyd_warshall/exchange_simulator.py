from floyd_warshall.exchange_line_reader import ExchangeLineReader


class ExchangeSimulator(object):
    """"
        Creates a mock exchange which simluates the send of data to clients
        EXCHANGE -> line_reader -> message_handler -> price_engine
    """
    def __init__(self, name):
        self._exchange_line_readers = []
        self.name = name

    def register_client_line_reader(self, client):
        """ For the sake of this simulator client line reader must
            implement a Line Reader Interface which has a receive_message method """
        self._exchange_line_readers.append(client)

    def push_message(self, msg):
        for exch_client in self._exchange_line_readers:
            exch_client.receive_message(msg)
