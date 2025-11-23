import streamlit as st
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.data_loader import load_airports, load_routes, load_airlines
from src.visualizations.mapa import create_route_map
from src.graph.grafo import Graph
from src.algorithms.dijkstra import find_shortest_path
from ui.components.search import render_search_form
from ui.components.filters import render_filters
from ui.components.results import render_results


st.set_page_config(
    page_title="Optimizador de Rutas de Vuelo",
    layout="wide",
    initial_sidebar_state="expanded"
)



@st.cache_data
def load_data():
    airports = load_airports()
    routes = load_routes()
    airlines = load_airlines()
    return airports, routes, airlines


def main():
    st.title("Optimizador de Rutas de Vuelo")
    st.markdown("Encuentra las mejores rutas de vuelo con conexiones optimas")
    st.markdown("---")

    airports, routes, airlines = load_data()

    with st.sidebar:
        st.header("Buscar Vuelos")
        origin, destination = render_search_form(airports)

        st.header("Filtros")
        filters = render_filters()

    if origin and destination:
        if origin == destination:
            st.warning("El origen y destino deben ser diferentes")
        else:
            st.header(f"Ruta: {origin} → {destination}")

            graph = Graph()
            graph.build_from_data(airports, routes, filters['optimization'])

            result = find_shortest_path(graph, origin, destination, filters['max_stops'])

            if result:
                path = result['path']
                route_list = result['routes']
                total_cost = result['total_cost']
                total_stops = result['total_stops']

                map_obj = create_route_map(airports, routes, origin, destination, path)
                if map_obj:
                    from streamlit_folium import st_folium
                    st_folium(map_obj, width=1400, height=600)

                render_results(route_list, origin, destination, filters, airports, result)
            else:
                st.error("No se encontraron rutas entre los aeropuertos seleccionados")
    else:
        st.info("Selecciona aeropuertos de origen y destino para comenzar la busqueda")

        st.markdown("### Estadisticas del Dataset")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Aeropuertos", len(airports))
        with col2:
            st.metric("Total Rutas", len(routes))
        with col3:
            st.metric("Total Aerolineas", len(airlines))


if __name__ == "__main__":
    main()
