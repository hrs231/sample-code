from floyd_warshall.price_engine import PriceEngine
from floyd_warshall.exchange_simulator import ExchangeSimulator
from floyd_warshall.exchange_line_reader import ExchangeLineReader
from floyd_warshall.exchange_msg_handler import ExchangeMsgHandler
from floyd_warshall.rate_request_client_handler import RateRequestClientHandler


class SimulateProductionEnvironment(object):
    """  Simulates the whole production environment
         exchange -> line_reader -> message_parser -> price_engine
    """

    def __init__(self, ):
        # Create a simulated environment components
        self._exchanges_simulated = {}
        self._exchange_line_readers = {}
        self._exchange_message_parsers = {}
        self._price_engine = PriceEngine()
        self._rate_requesting_client = RateRequestClientHandler(self._price_engine)

    def process_input_data(self, msg_string):
        # No response needed for a price update
        response = None
        if msg_string.startswith("EXCHANGE_RATE_REQUEST"):
            # client Rate Request
            # Format EXCHANGE_RATE_REQUEST KRAKEN BTC GDAX USD
            response = self._rate_requesting_client.process_rate_request(msg_string)
        else:
            # Price Update Msg, Extract the exchange name so we can simulate the corrected exchange
            # Format 2017-11-01T09:42:23+00:00 KRAKEN BTC USD 1000.0 0.0009
            exchange_name = msg_string.split()[1]
            simulated_exchange = self._get_exchange(exchange_name)
            simulated_exchange.push_message(msg_string)
        return response

    def _get_exchange(self, exch_name):
        try:
            return self._exchanges_simulated[exch_name]
        except KeyError:
            return self._create_simulated_exchange_environment(exch_name)

    def _create_simulated_exchange_environment(self, exch_name):
        # Create a new simulated exchange, line reader and message parser
        # each connected to the next, as we would in production
        # exch -> line_reader -> msg_parser -> price_engine

        exch = ExchangeSimulator(exch_name)
        line_reader = ExchangeLineReader()
        msg_parser = ExchangeMsgHandler()

        line_reader.connect_to_exchange(exch)
        msg_parser.connect_to_line_reader(line_reader)
        self._price_engine.connect_to_msg_parser(exch_name, msg_parser)

        self._exchanges_simulated[exch_name] = exch
        self._exchange_line_readers[exch_name] = line_reader
        self._exchange_message_parsers[exch_name] = msg_parser
        return exch
