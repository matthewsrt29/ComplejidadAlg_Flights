import csv
import json
import os


def crear_carpetas():

    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('data/config', exist_ok=True)



def csv_a_json_aeropuertos(csv_path='data/raw/airports.dat',
                           json_path='data/processed/aeropuertos.json',
                           limite=None):

    aeropuertos = {}
    count = 0
    skipped = 0


    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)

            for fila in reader:
                # Límite alcanzado
                if limite and count >= limite:
                    break

                try:
                    # Formato OpenFlights airports.dat:
                    # [0]=Airport ID, [1]=Name, [2]=City, [3]=Country,
                    # [4]=IATA, [5]=ICAO, [6]=Latitude, [7]=Longitude,
                    # [8]=Altitude, [9]=Timezone, [10]=DST, [11]=Tz

                    airport_id = fila[0]
                    nombre = fila[1]
                    ciudad = fila[2]
                    pais = fila[3]
                    iata = fila[4]
                    icao = fila[5]
                    latitud = fila[6]
                    longitud = fila[7]
                    altitud = fila[8]
                    timezone = fila[9]

                    # Filtrar aeropuertos sin código IATA
                    if iata == "\\N" or iata == "" or len(iata) != 3:
                        skipped += 1
                        continue

                    # Validar coordenadas
                    try:
                        lat = float(latitud)
                        lon = float(longitud)
                    except ValueError:
                        skipped += 1
                        continue

                    aeropuertos[iata] = {
                        'id': airport_id,
                        'nombre': nombre,
                        'ciudad': ciudad,
                        'pais': pais,
                        'iata': iata,
                        'icao': icao if icao != "\\N" else None,
                        'latitud': lat,
                        'longitud': lon,
                        'altitud': int(altitud) if altitud != "\\N" else 0,
                        'timezone': timezone if timezone != "\\N" else None
                    }

                    count += 1

                except (IndexError, ValueError) as e:
                    skipped += 1
                    continue

        # Guardar como JSON
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(aeropuertos, f, indent=2, ensure_ascii=False)


        return aeropuertos

    except FileNotFoundError:
        print(f" ERROR {csv_path}")
        print("  descargado los datasets en data/raw/")
        return {}


def csv_a_json_rutas(csv_path='data/raw/routes.dat',
                     json_path='data/processed/rutas.json',
                     aeropuertos_validos=None):
    if aeropuertos_validos is None:
        print(" ERROR")
        return []

    rutas = []
    count = 0
    skipped = 0

    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)

            for fila in reader:
                try:
                    # Formato OpenFlights routes.dat:
                    # [0]=Airline, [1]=Airline ID, [2]=Source airport,
                    # [3]=Source airport ID, [4]=Destination airport,
                    # [5]=Destination airport ID, [6]=Codeshare,
                    # [7]=Stops, [8]=Equipment

                    aerolinea = fila[0]
                    aerolinea_id = fila[1]
                    origen = fila[2]
                    destino = fila[4]
                    codeshare = fila[6]
                    escalas = fila[7]
                    equipo = fila[8]

                    # Solo incluir rutas entre aeropuertos que tenemos
                    if origen not in aeropuertos_validos or destino not in aeropuertos_validos:
                        skipped += 1
                        continue

                    # Solo vuelos directos (0 escalas)
                    if escalas != "0":
                        skipped += 1
                        continue

                    rutas.append({
                        'aerolinea': aerolinea,
                        'aerolinea_id': aerolinea_id,
                        'origen': origen,
                        'destino': destino,
                        'codeshare': codeshare,
                        'escalas': int(escalas) if escalas else 0,
                        'equipo': equipo.split() if equipo else []
                    })

                    count += 1

                except (IndexError, ValueError):
                    skipped += 1
                    continue

        # Guardar como JSON
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(rutas, f, indent=2, ensure_ascii=False)



        return rutas

    except FileNotFoundError:
        print(f" ERROR: No se encontró el archivo {csv_path}")
        return []


def csv_a_json_aerolineas(csv_path='data/raw/airlines.dat',
                          json_path='data/processed/aerolineas.json'):

    aerolineas = {}
    count = 0
    skipped = 0

    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)

            for fila in reader:
                try:
                    # Formato OpenFlights airlines.dat:
                    # [0]=Airline ID, [1]=Name, [2]=Alias, [3]=IATA,
                    # [4]=ICAO, [5]=Callsign, [6]=Country, [7]=Active

                    airline_id = fila[0]
                    nombre = fila[1]
                    alias = fila[2]
                    iata = fila[3]
                    icao = fila[4]
                    callsign = fila[5]
                    pais = fila[6]
                    activa = fila[7]

                    # Filtrar aerolíneas sin código IATA
                    if iata == "\\N" or iata == "" or len(iata) != 2:
                        skipped += 1
                        continue

                    # Solo aerolíneas activas
                    if activa != "Y":
                        skipped += 1
                        continue

                    aerolineas[iata] = {
                        'id': airline_id,
                        'nombre': nombre,
                        'alias': alias if alias != "\\N" else None,
                        'iata': iata,
                        'icao': icao if icao != "\\N" else None,
                        'callsign': callsign if callsign != "\\N" else None,
                        'pais': pais,
                        'activa': True
                    }

                    count += 1

                except (IndexError, ValueError):
                    skipped += 1
                    continue

        # Guardar como JSON
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(aerolineas, f, indent=2, ensure_ascii=False)


        return aerolineas

    except FileNotFoundError:
        print(f" ERROR: No se encontró el archivo {csv_path}")
        return {}


def generar_estadisticas(aeropuertos, rutas, aerolineas):

    print(f"\nAeropuertos: {len(aeropuertos)}")

    paises = {}
    for aeropuerto in aeropuertos.values():
        pais = aeropuerto['pais']
        paises[pais] = paises.get(pais, 0) + 1

    top_paises = sorted(paises.items(), key=lambda x: x[1], reverse=True)[:5]
    print("\n  Top 5 paises con mas aeropuertos:")
    for pais, cantidad in top_paises:
        print(f"    - {pais}: {cantidad}")

    print(f"\nRutas: {len(rutas)}")


    aerolineas_rutas = {}
    for ruta in rutas:
        codigo = ruta['aerolinea']
        aerolineas_rutas[codigo] = aerolineas_rutas.get(codigo, 0) + 1

    top_aerolineas = sorted(aerolineas_rutas.items(), key=lambda x: x[1], reverse=True)[:5]
    print("\n  Top 5 aerolineas con mas rutas:")
    for codigo, cantidad in top_aerolineas:
        nombre = aerolineas.get(codigo, {}).get('nombre', codigo)
        print(f"    - {nombre} ({codigo}): {cantidad} rutas")

    print(f"\nAerolineas: {len(aerolineas)}")

    print("\n" + "=" * 60)


def main():

    crear_carpetas()

    # Procesar aeropuertos
    aeropuertos = csv_a_json_aeropuertos(limite=None)

    if not aeropuertos:
        print("\nERROR")
        return

    # Procesar rutas (solo entre aeropuertos válidos)
    rutas = csv_a_json_rutas(aeropuertos_validos=set(aeropuertos.keys()))

    aerolineas = csv_a_json_aerolineas()

    generar_estadisticas(aeropuertos, rutas, aerolineas)

    print("  - data/processed/aeropuertos.json")
    print("  - data/processed/rutas.json")
    print("  - data/processed/aerolineas.json")



if __name__ == "__main__":
    main()