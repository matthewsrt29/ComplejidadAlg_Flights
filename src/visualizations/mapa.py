import folium


def get_price_color(price):
    if price < 200:
        return '#00FF00', 'Barato'
    elif price < 500:
        return '#0066FF', 'Medio'
    elif price < 800:
        return '#FF9900', 'Caro'
    else:
        return '#FF0000', 'Muy Caro'


def create_route_map(airports, routes, origin, destination, path=None):
    if origin not in airports or destination not in airports:
        return None

    origin_airport = airports[origin]
    dest_airport = airports[destination]

    center_lat = (origin_airport['latitud'] + dest_airport['latitud']) / 2
    center_lon = (origin_airport['longitud'] + dest_airport['longitud']) / 2

    map_obj = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=4,
        tiles='OpenStreetMap'
    )

    origin_connections = len([r for r in routes if r['origen'] == origin or r['destino'] == origin])
    dest_connections = len([r for r in routes if r['origen'] == destination or r['destino'] == destination])

    folium.CircleMarker(
        location=[origin_airport['latitud'], origin_airport['longitud']],
        radius=12,
        popup=f"<b>ORIGEN: {origin}</b><br>"
              f"{origin_airport['ciudad']}, {origin_airport['pais']}<br>"
              f"Altitud: {origin_airport['altitud']}m<br>"
              f"Conexiones: {origin_connections}",
        tooltip=f"{origin} - {origin_airport['ciudad']}",
        color='green',
        fill=True,
        fillColor='green',
        fillOpacity=0.8
    ).add_to(map_obj)

    folium.CircleMarker(
        location=[dest_airport['latitud'], dest_airport['longitud']],
        radius=12,
        popup=f"<b>DESTINO: {destination}</b><br>"
              f"{dest_airport['ciudad']}, {dest_airport['pais']}<br>"
              f"Altitud: {dest_airport['altitud']}m<br>"
              f"Conexiones: {dest_connections}",
        tooltip=f"{destination} - {dest_airport['ciudad']}",
        color='red',
        fill=True,
        fillColor='red',
        fillOpacity=0.8
    ).add_to(map_obj)

    direct_routes = [
        r for r in routes
        if r['origen'] == origin and r['destino'] == destination
    ]

    if direct_routes:
        avg_price = sum(r['price_usd'] for r in direct_routes) / len(direct_routes)
        min_price = min(r['price_usd'] for r in direct_routes)
        max_price = max(r['price_usd'] for r in direct_routes)
        avg_duration = sum(r['duration_min'] for r in direct_routes) / len(direct_routes)

        color, category = get_price_color(avg_price)

        folium.PolyLine(
            locations=[
                [origin_airport['latitud'], origin_airport['longitud']],
                [dest_airport['latitud'], dest_airport['longitud']]
            ],
            color=color,
            weight=4,
            opacity=0.7,
            popup=f"<b>{origin} → {destination}</b><br>"
                  f"Rutas disponibles: {len(direct_routes)}<br>"
                  f"Precio promedio: ${avg_price:.0f} USD<br>"
                  f"Rango: ${min_price} - ${max_price}<br>"
                  f"Duracion promedio: {avg_duration:.0f} min<br>"
                  f"Categoria: {category}",
            tooltip=f"{len(direct_routes)} ruta(s) - ${avg_price:.0f} ({category})"
        ).add_to(map_obj)

    legend_html = '''
    <div style="position: fixed;
                bottom: 50px; right: 50px; width: 180px; height: 160px;
                background-color: white; border:2px solid grey; z-index:9999;
                font-size:14px; padding: 10px">
    <p style="margin:0; font-weight:bold;">Categoria de Precios:</p>
    <p style="margin:5px 0;"><span style="color:#00FF00;">⬤</span> Barato (&lt; $200)</p>
    <p style="margin:5px 0;"><span style="color:#0066FF;">⬤</span> Medio ($200-$500)</p>
    <p style="margin:5px 0;"><span style="color:#FF9900;">⬤</span> Caro ($500-$800)</p>
    <p style="margin:5px 0;"><span style="color:#FF0000;">⬤</span> Muy Caro (&gt; $800)</p>
    </div>
    '''
    map_obj.get_root().html.add_child(folium.Element(legend_html))

    if path and len(path) > 2:
        for i in range(len(path) - 1):
            curr_code = path[i]
            next_code = path[i + 1]

            if curr_code in airports and next_code in airports:
                curr_airport = airports[curr_code]
                next_airport = airports[next_code]

                folium.PolyLine(
                    locations=[
                        [curr_airport['latitud'], curr_airport['longitud']],
                        [next_airport['latitud'], next_airport['longitud']]
                    ],
                    color='#FFD700',
                    weight=5,
                    opacity=0.9,
                    popup=f"<b>Tramo {i+1}</b><br>{curr_code} → {next_code}",
                    tooltip=f"Tramo {i+1}: {curr_code} → {next_code}"
                ).add_to(map_obj)

                if i > 0 and i < len(path) - 1:
                    connections = len([r for r in routes if r['origen'] == curr_code or r['destino'] == curr_code])
                    folium.CircleMarker(
                        location=[curr_airport['latitud'], curr_airport['longitud']],
                        radius=9,
                        popup=f"<b>ESCALA {i}: {curr_code}</b><br>"
                              f"{curr_airport['ciudad']}, {curr_airport['pais']}<br>"
                              f"Altitud: {curr_airport['altitud']}m<br>"
                              f"Conexiones: {connections}",
                        tooltip=f"Escala: {curr_code} - {curr_airport['ciudad']}",
                        color='#FFD700',
                        fill=True,
                        fillColor='#FFA500',
                        fillOpacity=0.9
                    ).add_to(map_obj)

    return map_obj


def create_global_map(airports, routes, sample_size=500):
    map_obj = folium.Map(
        location=[20, 0],
        zoom_start=2,
        tiles='OpenStreetMap'
    )

    import random
    sampled_routes = random.sample(routes, min(sample_size, len(routes)))

    for route in sampled_routes:
        origin_code = route['origen']
        dest_code = route['destino']

        if origin_code in airports and dest_code in airports:
            origin_airport = airports[origin_code]
            dest_airport = airports[dest_code]

            folium.PolyLine(
                locations=[
                    [origin_airport['latitud'], origin_airport['longitud']],
                    [dest_airport['latitud'], dest_airport['longitud']]
                ],
                color='blue',
                weight=1,
                opacity=0.3
            ).add_to(map_obj)

    return map_obj
