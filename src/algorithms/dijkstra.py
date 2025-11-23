import heapq


def find_shortest_path(graph, origin, destination, max_stops=999):
    if not graph.airport_exists(origin) or not graph.airport_exists(destination):
        return None

    distances = {airport: float('inf') for airport in graph.airports}
    distances[origin] = 0

    previous = {airport: None for airport in graph.airports}
    route_info = {airport: None for airport in graph.airports}
    stops_count = {airport: 0 for airport in graph.airports}

    priority_queue = [(0, origin)]
    visited = set()

    while priority_queue:
        current_distance, current_airport = heapq.heappop(priority_queue)

        if current_airport in visited:
            continue

        visited.add(current_airport)

        if current_airport == destination:
            break

        if stops_count[current_airport] >= max_stops:
            continue

        for neighbor in graph.get_neighbors(current_airport):
            next_airport = neighbor['destination']
            weight = neighbor['weight']
            route_data = neighbor['route_data']

            if next_airport in visited:
                continue

            new_distance = current_distance + weight
            new_stops = stops_count[current_airport] + 1

            if new_stops > max_stops:
                continue

            if new_distance < distances[next_airport]:
                distances[next_airport] = new_distance
                previous[next_airport] = current_airport
                route_info[next_airport] = route_data
                stops_count[next_airport] = new_stops
                heapq.heappush(priority_queue, (new_distance, next_airport))

    if distances[destination] == float('inf'):
        return None

    path = []
    routes = []
    current = destination

    while current is not None:
        path.append(current)
        if route_info[current] is not None:
            routes.append(route_info[current])
        current = previous[current]

    path.reverse()
    routes.reverse()

    total_cost = distances[destination]
    total_stops = len(path) - 1

    return {
        'path': path,
        'routes': routes,
        'total_cost': total_cost,
        'total_stops': total_stops
    }
