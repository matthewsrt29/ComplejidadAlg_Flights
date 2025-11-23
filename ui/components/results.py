import streamlit as st
from src.calculators.duracion import minutes_to_hours_format


def render_results(routes, origin, destination, filters, airports, dijkstra_result=None):
    if dijkstra_result:
        path = dijkstra_result['path']
        route_list = dijkstra_result['routes']
        total_cost = dijkstra_result['total_cost']
        total_stops = dijkstra_result['total_stops']

        total_price = sum(r['price_usd'] for r in route_list)
        total_duration = sum(r['duration_min'] for r in route_list)
        total_distance = sum(r['distance_km'] for r in route_list)

        st.markdown(f"### Mejor Ruta Encontrada ({total_stops} escala(s))")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Precio Total", f"${total_price} USD")
        with col2:
            st.metric("Duracion Total", minutes_to_hours_format(total_duration))
        with col3:
            st.metric("Distancia Total", f"{total_distance} km")
        with col4:
            st.metric("Escalas", total_stops)

        st.markdown("---")
        st.markdown("### Detalles del Itinerario")

        for idx, route in enumerate(route_list, 1):
            origin_code = route['origen']
            dest_code = route['destino']

            with st.expander(
                f"Tramo {idx}: {origin_code} → {dest_code} - ${route['price_usd']} USD | {minutes_to_hours_format(route['duration_min'])}",
                expanded=(idx == 1)
            ):
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown("**Precio**")
                    st.markdown(f"${route['price_usd']} USD")

                with col2:
                    st.markdown("**Duracion**")
                    st.markdown(minutes_to_hours_format(route['duration_min']))

                with col3:
                    st.markdown("**Distancia**")
                    st.markdown(f"{route['distance_km']} km")

                st.markdown(f"**Aerolinea:** {route['aerolinea']}")
                st.markdown(f"**Desde:** {airports[origin_code]['ciudad']}, {airports[origin_code]['pais']} ({origin_code})")
                st.markdown(f"**Hasta:** {airports[dest_code]['ciudad']}, {airports[dest_code]['pais']} ({dest_code})")

        st.markdown("---")
        st.markdown("**Ruta Completa:**")
        route_text = " → ".join([f"{code} ({airports[code]['ciudad']})" for code in path])
        st.markdown(route_text)
    else:
        direct_routes = [
            r for r in routes
            if r['origen'] == origin and r['destino'] == destination
        ]

        filtered_routes = [
            r for r in direct_routes
            if r['price_usd'] <= filters['max_price'] and
               r['duration_min'] <= filters['max_duration']
        ]

        if not filtered_routes:
            if filters.get('filters_enabled', False):
                st.warning("No se encontraron rutas directas con los filtros actuales")
            else:
                st.warning("No se encontraron rutas directas entre estos aeropuertos")
            return

        if filters['optimization'] == 'precio':
            filtered_routes.sort(key=lambda x: x['price_usd'])
        elif filters['optimization'] == 'duracion':
            filtered_routes.sort(key=lambda x: x['duration_min'])

        filters_text = " (con filtros aplicados)" if filters.get('filters_enabled', False) else ""
        st.markdown(f"### Se encontraron {len(filtered_routes)} ruta(s) directa(s){filters_text}")

        for idx, route in enumerate(filtered_routes[:10], 1):
            with st.expander(f"Ruta {idx} - ${route['price_usd']} USD | {minutes_to_hours_format(route['duration_min'])}", expanded=(idx == 1)):
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown("**Precio**")
                    st.markdown(f"${route['price_usd']} USD")

                with col2:
                    st.markdown("**Duracion**")
                    st.markdown(minutes_to_hours_format(route['duration_min']))

                with col3:
                    st.markdown("**Distancia**")
                    st.markdown(f"{route['distance_km']} km")

                st.markdown(f"**Aerolinea:** {route['aerolinea']}")
                st.markdown(f"**Desde:** {airports[origin]['ciudad']}, {airports[origin]['pais']}")
                st.markdown(f"**Hasta:** {airports[destination]['ciudad']}, {airports[destination]['pais']}")
