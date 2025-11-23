import random


def calculate_flight_price(distance_km, airline=None, seed=None):
    price_per_km = 0.12
    base_price = distance_km * price_per_km
    min_price = 50

    if seed is not None:
        random.seed(seed)

    variation_factor = random.uniform(0.6, 1.4)
    price_with_variation = base_price * variation_factor
    final_price = max(price_with_variation, min_price)

    return int(round(final_price))


def calculate_route_price(distance_km, origin_code, destination_code, airline=None):
    route_str = f"{origin_code}-{destination_code}"
    if airline:
        route_str += f"-{airline}"

    seed = hash(route_str) % (2**31)

    return calculate_flight_price(distance_km, airline, seed)
