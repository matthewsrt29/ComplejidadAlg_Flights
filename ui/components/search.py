import streamlit as st


def render_search_form(airports):
    airport_codes = sorted(airports.keys())
    airport_options = {
        code: f"{airports[code]['ciudad']}, {airports[code]['pais']} ({code})"
        for code in airport_codes
    }

    if 'swap_airports' not in st.session_state:
        st.session_state.swap_airports = False

    origin_default = 0
    if st.session_state.swap_airports and 'last_destination' in st.session_state:
        try:
            origin_default = airport_codes.index(st.session_state.last_destination)
        except ValueError:
            origin_default = 0

    origin = st.selectbox(
        "Aeropuerto de Origen",
        options=airport_codes,
        format_func=lambda x: airport_options[x],
        index=origin_default,
        key="origin_select"
    )

    dest_default = 1 if len(airport_codes) > 1 else 0
    if st.session_state.swap_airports and 'last_origin' in st.session_state:
        try:
            dest_default = airport_codes.index(st.session_state.last_origin)
        except ValueError:
            dest_default = 1

    destination = st.selectbox(
        "Aeropuerto de Destino",
        options=airport_codes,
        format_func=lambda x: airport_options[x],
        index=dest_default,
        key="destination_select"
    )

    if st.button("⇄ Invertir Ruta", help="Intercambiar origen y destino", use_container_width=True):
        st.session_state.swap_airports = True
        st.session_state.last_origin = origin
        st.session_state.last_destination = destination
        st.rerun()

    if st.session_state.swap_airports:
        st.session_state.swap_airports = False

    st.session_state.last_origin = origin
    st.session_state.last_destination = destination

    return origin, destination
