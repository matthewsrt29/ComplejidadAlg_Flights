import json
import folium
from collections import Counter
import random


def cargar_datos():
    with open('../data/processed/aeropuertos.json', 'r', encoding='utf-8') as f:
        aeropuertos = json.load(f)

    with open('../data/processed/rutas.json', 'r', encoding='utf-8') as f:
        rutas = json.load(f)

    return aeropuertos, rutas


def mapa_global(aeropuertos, rutas):
    # Mapa centrado en el mundo
    mapa = folium.Map(
        location=[20, 0],
        zoom_start=2,
        tiles='OpenStreetMap'
    )

    # Número total de vuelos que llegan y salen de un aeropuerto
    grados = Counter()
    for ruta in rutas:
        grados[ruta['origen']] += 1
        grados[ruta['destino']] += 1

    # Agregar aeropuertos
    aeropuertos_muestra = random.sample(
        list(aeropuertos.items()),
        min(800, len(aeropuertos))
    )

    for iata, datos in aeropuertos_muestra:
        # Tamaño según conexiones
        conexiones = grados.get(iata, 0)

        if conexiones > 100:
            radius = 6
            color = 'red'
            fillColor = 'red'
        elif conexiones > 50:
            radius = 4
            color = 'orange'
            fillColor = 'orange'
        else:
            radius = 2
            color = 'blue'
            fillColor = 'lightblue'

        folium.CircleMarker(
            location=[datos['latitud'], datos['longitud']],
            radius=radius,
            popup=f"<b>{iata}</b><br>{datos['ciudad']}<br>{datos['pais']}<br>{conexiones} conexiones",
            color=color,
            fill=True,
            fillColor=fillColor,
            fillOpacity=0.7
        ).add_to(mapa)

    # Agregar rutas
    rutas_muestra = random.sample(rutas, min(300, len(rutas)))

    for ruta in rutas_muestra:
        origen_datos = aeropuertos.get(ruta['origen'])
        destino_datos = aeropuertos.get(ruta['destino'])

        if origen_datos and destino_datos:
            folium.PolyLine(
                locations=[
                    [origen_datos['latitud'], origen_datos['longitud']],
                    [destino_datos['latitud'], destino_datos['longitud']]
                ],
                color='red',
                weight=1,
                opacity=0.2
            ).add_to(mapa)

    # Guardar
    mapa.save('mapa_global.html')


def mapa_sudamerica(aeropuertos, rutas):

    paises_sudamerica = ['Brazil', 'Argentina', 'Chile', 'Peru', 'Colombia',
                         'Venezuela', 'Ecuador', 'Bolivia', 'Paraguay', 'Uruguay']

    # Filtrar Sudamérica
    aeropuertos_sa = {
        iata: datos for iata, datos in aeropuertos.items()
        if datos['pais'] in paises_sudamerica
    }

    # Mapa  Sudamérica
    mapa = folium.Map(
        location=[-15, -60],
        zoom_start=3,
        tiles='OpenStreetMap'
    )

    # Calcular conexiones
    grados = Counter()
    for ruta in rutas:
        if ruta['origen'] in aeropuertos_sa and ruta['destino'] in aeropuertos_sa:
            grados[ruta['origen']] += 1
            grados[ruta['destino']] += 1

    # Agregar aeropuertos
    for iata, datos in aeropuertos_sa.items():
        conexiones = grados.get(iata, 0)

        if conexiones > 20:
            radius = 8
            color = 'red'
        elif conexiones > 10:
            radius = 5
            color = 'orange'
        else:
            radius = 3
            color = 'blue'

        folium.CircleMarker(
            location=[datos['latitud'], datos['longitud']],
            radius=radius,
            popup=f"<b>{iata}</b><br>{datos['ciudad']}<br>{conexiones} conexiones",
            color=color,
            fill=True,
            fillColor=color,
            fillOpacity=0.8
        ).add_to(mapa)

    # Agregar rutas internas de Sudamérica
    for ruta in rutas:
        if ruta['origen'] in aeropuertos_sa and ruta['destino'] in aeropuertos_sa:
            origen_datos = aeropuertos_sa[ruta['origen']]
            destino_datos = aeropuertos_sa[ruta['destino']]

            folium.PolyLine(
                locations=[
                    [origen_datos['latitud'], origen_datos['longitud']],
                    [destino_datos['latitud'], destino_datos['longitud']]
                ],
                color='blue',
                weight=1.5,
                opacity=0.4
            ).add_to(mapa)

    mapa.save('mapa_sudamerica.html')


def main():
    aeropuertos, rutas = cargar_datos()
    mapa_global(aeropuertos, rutas)
    mapa_sudamerica(aeropuertos, rutas)


if __name__ == "__main__":
    main()