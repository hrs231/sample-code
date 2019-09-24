import unittest
from floyd_warshall.price_engine import PriceEngine
from messages.price_update import PriceUpdate
from messages.rate_request import RateRequest


class PriceEngineTestCase(unittest.TestCase):
    """ TODO - implement further units test
        algo checks
        price small change single instrument small graph
        price large change update effect on small graph
        price small change large graph
        price large change large graph many routes
        edge case invalid rates fwd * bkwd > 1
    """
    def test_price_initial(self):
        """" Basic Price Upd """
        pc = PriceEngine(logging=False)
        pc.process_update_message(PriceUpdate("TEST_EX","BTC", "USD", 1001.0, 0.0009))
        rate_request = RateRequest("TEST_EX", "BTC", "TEST_EX", "USD")
        pc.handle_rate_request(rate_request)
        self.assertEqual(rate_request.rate, 1001)
        rate_request = RateRequest("TEST_EX", "USD", "TEST_EX", "BTC")
        pc.handle_rate_request(rate_request)
        self.assertEqual(rate_request.rate, 0.0009)

    def test_price_update(self):
        """" Basic Price change """
        pc = PriceEngine(logging=False)
        pc.process_update_message(PriceUpdate("TEST_EX", "BTC", "USD", 1001.0, 0.0009))
        pc.process_update_message(PriceUpdate("TEST_EX","BTC", "USD", 1009.0, 0.0008))
        rate_request = RateRequest("TEST_EX", "BTC", "TEST_EX", "USD")
        pc.handle_rate_request(rate_request)
        self.assertEqual(rate_request.rate, 1009)
        rate_request = RateRequest("TEST_EX", "USD", "TEST_EX", "BTC")
        pc.handle_rate_request(rate_request)
        self.assertEqual(rate_request.rate, 0.0008)

    def test_price_no_path(self):
        """" Isolated Edge so ro rate available """
        pc = PriceEngine(logging=False)
        pc.process_update_message(PriceUpdate("TEST_EX", "BTC", "USD", 1001.0, 0.0009))
        pc.process_update_message(PriceUpdate("TEST_EX","ETH", "EUR", 800.0, 0.0008))
        rate_request = RateRequest("TEST_EX", "BTC", "TEST_EX", "EUR")
        pc.handle_rate_request(rate_request)
        self.assertEqual(rate_request.rate, 0)
        rate_request = RateRequest("TEST_EX", "ETH", "TEST_EX", "USD")
        pc.handle_rate_request(rate_request)
        self.assertEqual(rate_request.rate, 0)

    def test_price_cross_exchange(self):
        """" Test better price on another exchange """
        pc = PriceEngine(logging=False)
        # Create an price on the TEST_EX
        pc.process_update_message(PriceUpdate("TEST_EX", "BTC", "USD", 1001.0, 0.0009))
        rate_request = RateRequest("TEST_EX", "BTC", "TEST_EX", "USD")
        pc.handle_rate_request(rate_request)
        self.assertEqual(rate_request.rate, 1001)
        # Create a better price on another TEST_EX_2
        # Check we pick up the improved rate
        pc.process_update_message(PriceUpdate("TEST_EX_2", "BTC", "USD", 1100.0, 0.0008))
        rate_request = RateRequest("TEST_EX", "BTC", "TEST_EX", "USD")
        pc.handle_rate_request(rate_request)
        self.assertEqual(rate_request.rate, 1100)

    """ TODO - implement further units test"""

if __name__ == '__main__':
    unittest.main()
