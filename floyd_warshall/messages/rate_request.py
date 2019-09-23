

class RateRequest(object):
    """" Used by Price Engine Clients to query the Price Engine """
    def __init__(self, exch_1, curr_1, exch_2, curr_2):
        self.exch_1 = exch_1
        self.curr_1 = curr_1
        self.exch_2 = exch_2
        self.curr_2 = curr_2
        self.rate = 0
        self.path = []
        self.error_msg = None