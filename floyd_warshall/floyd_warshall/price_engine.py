from math import inf
from common.loggable import Loggable


class PriceEngine(Loggable):
    """" Main Rates Price Engine class, could be reduced in size using MVC
         Connect To Price Update Maessage Handlers and User Client RateRequests
         exchange -> line_reader -> message_parser  -> PRICE_ENGINE
                                    client_handler <-> PRICE_ENGINE
    """
    def __init__(self, logging=True):
        super(Loggable, self).__init__()
        if logging:
            self.init_logging("PriceEngine")
        self._exchange_message_handlers = {}
        self._exch_curr_to_vertex_id = []
        self._id_to_name_helper = []
        self._currency_list = {}
        self._vertex_count = 0
        self._vertex_list = {}
        self._edges = {}
        self._rates = None
        self._nxt = None
        self._graph_updated_needed = False

    def connect_to_msg_parser(self, exch_name, msg_parser):
        """ connect to our exchange msg parser """
        self._exchange_message_handlers[exch_name] = msg_parser
        self._exchange_message_handlers[exch_name].register_price_update_client(self)

    def process_update_message(self, price_update_msg):
        """ handles all price update messages """
        u = self._get_vertex_id_or_create_new_id(price_update_msg.exch, price_update_msg.curr_1)
        v = self._get_vertex_id_or_create_new_id(price_update_msg.exch, price_update_msg.curr_2)
        try:
            # TODO - Add extra Price reasonability checks
            rate_sum = float(price_update_msg.fwd) * float(price_update_msg.bkwd)
            if rate_sum > 1:
                self.log_error("Warning fwd * bkwd price sum > 1")

            self._edges[u][v] = price_update_msg.fwd
            self._edges[v][u] = price_update_msg.bkwd
            if self._graph_updated_needed is False:
                self._graph_updated_needed = True
        except KeyError:
            self.log_error("Error price update " + price_update_msg.exch)

    def _get_vertex_id_or_create_new_id(self, exch, curr):
        """" returns local vertex id """
        try:
            return self._get_vertex_id(exch, curr)
        except KeyError:
            # New exch or currency,  create a new vertex
            return self._add_new_vertex(exch, curr)

    def _get_vertex_id(self, exch, curr):
        return self._vertex_list[(exch, curr)]

    def _add_new_vertex(self, exch, curr):
        """ a new Vertex, needs to be added to a few helper lookups """
        vertex_id = self._vertex_count
        self._vertex_count += 1

        self._vertex_list[(exch, curr)] = vertex_id
        self._edges[vertex_id] = {}
        self._add_static_edges(curr, vertex_id)
        self._id_to_name_helper.append(exch + ", " + curr)

        return vertex_id

    def _add_static_edges(self, curr, vert_id):
        """ Create all the currency 1 to 1 edges where the currencies are the same """
        if curr not in self._currency_list:
            self._currency_list[curr] = []
        self._currency_list[curr].append(vert_id)
        for u in self._currency_list[curr]:
            for v in self._currency_list[curr]:
                try:
                    self._edges[u][v] = 1
                except KeyError:
                    self.log_error("KeyError ", u, v)

    def handle_rate_request(self, request):
        # Make sure valid Vertex
        try:
            u = self._get_vertex_id(request.exch_1, request.curr_1)
            v = self._get_vertex_id(request.exch_2, request.curr_2)
        except KeyError:
            # at least one vertex doesn't exist return
            request.error_msg = "Invalid Currency"
            self.log_info("Invalid Currency {0}{1}{2}{3}".format(request.exch_1, request.curr_1, request.exch_2, request.curr_2))
            return

        # Check for cache hit
        if self._graph_updated_needed:
            self._calculate_optimal_rates_graph()
            self._graph_updated_needed = False

        request.rate = self._rates[u][v]

        if request.rate != float(0):
            # we have a rate so find the path
            path = self.get_path(u, v)
            for hop in path:
                request.path.append(self._id_to_name_helper[hop])

    def _calculate_optimal_rates_graph(self):
        """
            use a modified Floyd-Warshall implementation
        """
        n = self._vertex_count
        rn = range(n)
        self._rates = [[float(0)] * n for i in rn]
        self._nxt = [[inf] * n for i in rn]

        for u in self._edges:
            for v in self._edges[u]:
                self._rates[u][v] = float(self._edges[u][v])
                self._nxt[u][v] = v
        for k in rn:
            for i in rn:
                for j in rn:
                    if self._rates[i][j] < (self._rates[i][k] * self._rates[k][j]):
                        self._rates[i][j] = (self._rates[i][k] * self._rates[k][j])
                        self._nxt[i][j] = self._nxt[i][k]
        print(self._rates)
        print(self._nxt)

    def get_path(self, u, v):
        """"
            TODO put a linit
        """
        if self._nxt[u][v] == 0:
            return []
        path = [u]
        while u != v:
            u = self._nxt[u][v]
            path.append(u)
            # if we're more than the vertex count, we're caught in a loop
            # likely due to an extreme price
            if len(path) > self._vertex_count:
                return path
        return path
