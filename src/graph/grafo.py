from collections import defaultdict


class Graph:
    def __init__(self):
        self.adjacency_list = defaultdict(list)
        self.airports = {}

    def add_airport(self, code, airport_data):
        self.airports[code] = airport_data

    def add_route(self, origin, destination, weight, route_data):
        self.adjacency_list[origin].append({
            'destination': destination,
            'weight': weight,
            'route_data': route_data
        })

    def get_neighbors(self, airport_code):
        return self.adjacency_list.get(airport_code, [])

    def airport_exists(self, code):
        return code in self.airports

    def build_from_data(self, airports, routes, optimization='precio'):
        for code, airport_data in airports.items():
            self.add_airport(code, airport_data)

        weight_key = 'price_usd' if optimization == 'precio' else 'duration_min'

        for route in routes:
            origin = route['origen']
            destination = route['destino']
            weight = route[weight_key]

            self.add_route(origin, destination, weight, route)

            reverse_route = route.copy()
            reverse_route['origen'] = destination
            reverse_route['destino'] = origin
            self.add_route(destination, origin, weight, reverse_route)
