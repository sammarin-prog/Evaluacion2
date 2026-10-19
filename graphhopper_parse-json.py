# -*- coding: utf-8 -*-
"""
Evaluación 2 - CUY6142
Software de geolocalización con la API GraphHopper Directions.
Mejoras: textos en español, valores con máximo 2 decimales,
salida con "s" o "salir" y narrativa del viaje en español.
"""
import os
import urllib.parse
import requests

route_url = "https://graphhopper.com/api/1/route?"
geocode_url = "https://graphhopper.com/api/1/geocode?"

# El token se lee desde una variable de entorno para no publicarlo en GitHub.
key = os.environ.get("GRAPHHOPPER_KEY", "")
if key == "":
    key = input("Ingrese su token de GraphHopper: ").strip()

OPCIONES_SALIDA = ("s", "salir")
PERFILES = {"auto": "car", "bicicleta": "bike", "a pie": "foot",
            "car": "car", "bike": "bike", "foot": "foot"}
KM_POR_MILLA = 1.609344


def quiere_salir(texto):
    return texto.strip().lower() in OPCIONES_SALIDA


def formatear_duracion(milisegundos):
    total_seg = int(milisegundos / 1000)
    horas = total_seg // 3600
    minutos = (total_seg % 3600) // 60
    segundos = total_seg % 60
    return f"{horas:02d}:{minutos:02d}:{segundos:02d}"


def geocodificar(lugar):
    url = geocode_url + urllib.parse.urlencode(
        {"q": lugar, "limit": "1", "locale": "es", "key": key})
    respuesta = requests.get(url)
    datos = respuesta.json()
    print(f"URL de la API de geocodificación para {lugar}:\n{url}")
    if respuesta.status_code == 200 and len(datos.get("hits", [])) != 0:
        hit = datos["hits"][0]
        lat = hit["point"]["lat"]
        lng = hit["point"]["lng"]
        nombre = hit["name"]
        pais = hit.get("country", "")
        estado = hit.get("state", "")
        ubicacion = ", ".join(x for x in (nombre, estado, pais) if x)
        print(f"Ubicación encontrada: {ubicacion}")
        return respuesta.status_code, lat, lng, ubicacion
    print(f"Mensaje de error: {datos.get('message', 'Ubicación no encontrada')}")
    return respuesta.status_code, "null", "null", lugar


while True:
    print("\n" + "=" * 60)
    print("Perfiles de vehículo disponibles: auto, bicicleta, a pie")
    print("=" * 60)
    perfil_ingresado = input(
        "Ingrese un perfil de vehículo (escriba 's' o 'salir' para terminar): ")
    if quiere_salir(perfil_ingresado):
        break
    perfil = PERFILES.get(perfil_ingresado.strip().lower(), "car")

    origen = input("Ubicación de origen: ")
    if quiere_salir(origen):
        break
    destino = input("Destino: ")
    if quiere_salir(destino):
        break

    est_o, o_lat, o_lng, o_nombre = geocodificar(origen)
    est_d, d_lat, d_lng, d_nombre = geocodificar(destino)
    print("=" * 60)

    if est_o == 200 and est_d == 200 and o_lat != "null" and d_lat != "null":
        puntos = [("point", f"{o_lat},{o_lng}"), ("point", f"{d_lat},{d_lng}")]
        parametros = puntos + [("profile", perfil), ("locale", "es"),
                               ("key", key)]
        url = route_url + urllib.parse.urlencode(parametros)
        respuesta = requests.get(url)
        datos = respuesta.json()
        print(f"Estado de la API de rutas: {respuesta.status_code}")
        print(f"URL de la API de rutas:\n{url}")
        print("=" * 60)
        print(f"Indicaciones desde {o_nombre} hasta {d_nombre} en {perfil_ingresado}")
        print("=" * 60)
        if respuesta.status_code == 200:
            ruta = datos["paths"][0]
            km = ruta["distance"] / 1000
            millas = km / KM_POR_MILLA
            print(f"Distancia recorrida: {km:.2f} km / {millas:.2f} millas")
            print(f"Duración del viaje: {formatear_duracion(ruta['time'])}")
            print("=" * 60)
            print("Narrativa del viaje:")
            for i, paso in enumerate(ruta["instructions"], start=1):
                p_km = paso["distance"] / 1000
                p_mi = p_km / KM_POR_MILLA
                print(f"{i}. {paso['text']} ({p_km:.2f} km / {p_mi:.2f} millas)")
            print("=" * 60)
        else:
            print(f"Mensaje de error: {datos.get('message', 'Error desconocido')}")
            print("*" * 60)
    else:
        print("No se pudo calcular la ruta: revise las ubicaciones ingresadas.")

print("Programa finalizado. ¡Hasta pronto!")