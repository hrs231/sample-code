from floyd_warshall.price_engine import PriceEngine
from messages.rate_request import RateRequest
from common.loggable import Loggable


class RateRequestClientHandler(Loggable):
    """ Simulate a rate requesting client
        clients <-> CLIENT_HANDLER <-> price_engine """
    def __init__(self, price_engine):
        super(Loggable, self).__init__()
        self._price_engine = price_engine
        self.init_logging("ClientHandler")

    def set_price_engine(self, price_engine):
        self._price_engine = price_engine

    def process_rate_request(self, msg_string):
        """ TODO Implement a command pattern """
        self.log_info(msg_string)

        [header, exch_1, curr_1, exch_2, curr_2] = msg_string.split()
        request = RateRequest(exch_1, curr_1, exch_2, curr_2)

        self._price_engine.handle_rate_request(request)

        return self._create_rate_request_response(request)

    def _create_rate_request_response(self, request):
        """ output response in format expected by users """
        if request.error_msg is None:
            msg = "BEST_RATES_BEGIN {0} {1} {2} {3} {4}\n".format(request.exch_1, request.curr_1, request.exch_2, request.curr_2, request.rate)
            for item in request.path:
                msg += "{0}\n".format(item)
            msg += "BEST_RATES_END"
        else:
            msg = "BEST_RATES_ERROR {0} {1} {2} {3} {4}\n".format(request.exch_1, request.curr_1, request.exch_2,
                                                                  request.curr_2, request.rate)
            msg += request.error_msg + "\nBEST_RATES_ERROR_END"

        self.log_info(msg)

        return msg
