import json
import graphviz as gv

# Cargar datos
with open('../data/processed/aeropuertos.json', 'r', encoding='utf-8') as f:
    aeropuertos = json.load(f)
with open('../data/processed/rutas.json', 'r', encoding='utf-8') as f:
    rutas = json.load(f)


peru = {iata: datos for iata, datos in aeropuertos.items() if datos['pais'] == 'Peru'}


grafo = gv.Digraph('Aeropuertos_Peru')
grafo.attr(rankdir='LR', size='10,8')
grafo.attr('node', shape='ellipse', style='filled', fontsize='11')

###Asigna nodos
for iata, datos in peru.items():
    grafo.node(iata, datos['ciudad'], fillcolor='lightcoral', fontcolor='black')

###Asigna aristas
count_rutas = 0
for ruta in rutas:
    if ruta['origen'] in peru and ruta['destino'] in peru:
        grafo.edge(ruta['origen'], ruta['destino'])
        count_rutas += 1

print(f"Rutas internas en Perú: {count_rutas}")

grafo.save('aeropuertos_peru.dot')

with open('aeropuertos_peru_source.txt', 'w', encoding='utf-8') as f:
    f.write(grafo.source)



