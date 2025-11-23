import json
import os


def load_airports(filepath='data/processed/aeropuertos.json'):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_routes(filepath='data/processed/rutas.json'):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_airlines(filepath='data/processed/aerolineas.json'):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)
