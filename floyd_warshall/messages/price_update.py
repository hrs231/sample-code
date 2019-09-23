
class PriceUpdate(object):
    """" Used by exchange message parsers to update prices on the Price Engine """
    def __init__(self, exch, curr_1, curr_2, fwd, bkwd):
        self.exch = exch
        self.curr_1 = curr_1
        self.curr_2 = curr_2
        self.fwd = fwd
        self.bkwd = bkwd
