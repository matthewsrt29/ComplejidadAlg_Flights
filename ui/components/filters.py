import streamlit as st


def render_filters():
    apply_filters = st.checkbox("Aplicar Filtros", value=False)

    if apply_filters:
        max_price = st.slider(
            "Precio Maximo (USD)",
            min_value=0,
            max_value=5000,
            value=2000,
            step=50
        )

        max_duration = st.slider(
            "Duracion Maxima (horas)",
            min_value=0,
            max_value=24,
            value=12,
            step=1
        )

        max_stops = st.slider(
            "Escalas Maximas",
            min_value=0,
            max_value=3,
            value=2,
            step=1
        )
    else:
        max_price = 999999
        max_duration = 999999
        max_stops = 999

    optimization = st.radio(
        "Optimizar por",
        options=["Precio", "Duracion", "Escalas"],
        index=0
    )

    return {
        'max_price': max_price,
        'max_duration': max_duration * 60 if apply_filters else max_duration,
        'max_stops': max_stops,
        'optimization': optimization.lower(),
        'filters_enabled': apply_filters
    }
