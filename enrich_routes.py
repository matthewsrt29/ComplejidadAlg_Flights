import json
import sys
sys.path.append('src')

from calculators.distancia import calculate_airport_distance
from calculators.duracion import calculate_flight_duration
from calculators.precio import calculate_route_price


def enrich_routes():
    print("Loading data...")

    with open('data/processed/aeropuertos.json', 'r', encoding='utf-8') as f:
        airports = json.load(f)

    with open('data/processed/rutas.json', 'r', encoding='utf-8') as f:
        routes = json.load(f)

    print(f"Processing {len(routes)} routes...")

    enriched_routes = []
    processed = 0
    skipped = 0

    for route in routes:
        origin_code = route['origen']
        dest_code = route['destino']

        if origin_code not in airports or dest_code not in airports:
            skipped += 1
            continue

        origin_airport = airports[origin_code]
        dest_airport = airports[dest_code]

        distance = calculate_airport_distance(origin_airport, dest_airport)
        duration = calculate_flight_duration(distance)
        price = calculate_route_price(distance, origin_code, dest_code, route['aerolinea'])

        enriched_route = {
            **route,
            'distance_km': distance,
            'duration_min': duration,
            'price_usd': price
        }

        enriched_routes.append(enriched_route)
        processed += 1

        if processed % 10000 == 0:
            print(f"  Processed {processed} routes...")

    print(f"\nSaving enriched routes...")
    with open('data/processed/rutas.json', 'w', encoding='utf-8') as f:
        json.dump(enriched_routes, f, indent=2, ensure_ascii=False)

    print(f"\nDone!")
    print(f"  Total routes processed: {processed}")
    print(f"  Skipped (missing airports): {skipped}")
    print(f"  Output: data/processed/rutas.json")

    if len(enriched_routes) > 0:
        sample = enriched_routes[0]
        print(f"\nSample route:")
        print(f"  {sample['origen']} -> {sample['destino']}")
        print(f"  Distance: {sample['distance_km']} km")
        print(f"  Duration: {sample['duration_min']} min")
        print(f"  Price: ${sample['price_usd']} USD")


if __name__ == "__main__":
    enrich_routes()
