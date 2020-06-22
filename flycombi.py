#!/usr/bin/env python3

import sys
import csv
from grafo import Grafo
from biblioteca import orden_topo, obtener_ciclo_n_dfs, bfs, centralidad_aux, ordenar_vertices, camino_aleatorio, camino_minimo

COMANDOS = ["camino_mas", "camino_escalas", "centralidad", "centralidad_aprox", "recorrer_mundo_aprox", "vacaciones", "itinerario"]

def recorrer_mundo_aprox(vuelos, aeropuertos, origen): 
    a_visitar = set()
    orden = [aeropuertos[origen]][0]
    costo = 0
    for v in vuelos.ver_vertices(): a_visitar.add(v)
    a_visitar.remove(orden[0])
    while (len(a_visitar)):
        v = a_visitar.pop()
        padres = (camino_minimo(vuelos, orden[-1],v,0))[1]
        recorrido = [v]
        while recorrido[0] != orden[-1]:
            recorrido.insert(0, (padres)[recorrido[0]])
        for i in range(len(recorrido)):
            if recorrido[i] == orden[-1]: continue
            orden.append(recorrido[i])
            if recorrido[i] in a_visitar: a_visitar.remove(recorrido[i])
            if i != len(recorrido)-1 : costo+= vuelos.peso(recorrido[i], recorrido[i+1])[1]
    print (" -> ".join(orden))
    print("Costo: {}".format(costo))

def itinerario(aeropuertos, vuelos, nombre_ruta):
    grafo = Grafo(True)
    with open (nombre_ruta, "r") as archivo:
        archivo_csv = csv.reader(archivo) 
        ciudades = next(archivo_csv)
        for ciudad in ciudades: grafo.agregar_vertice(ciudad)
        for linea in archivo_csv: grafo.agregar_arista(linea[0],linea[1],0)
    orden = orden_topo(grafo)
    print(", ".join(orden))
    for i in range(len(orden) - 1):
        camino_escalas(aeropuertos, vuelos, orden[i], orden[i+1])

def vacaciones(aeropuertos, vuelos, origen, n):
    for a_origen in aeropuertos[origen]:
        recorrido = obtener_ciclo_n_dfs(vuelos, a_origen, n, aeropuertos[origen])
        if recorrido: break
    if not recorrido: print("No se encontro recorrido") 
    else: print(" -> ".join(recorrido))

def centralidad(vuelos, n):
    cent = centralidad_aux(vuelos)
    centrales_ordenados = ordenar_vertices(cent)
    print(", ".join(centrales_ordenados[:n]))

def centralidad_aprox(grafo,n):
    cent = camino_aleatorio(grafo)
    centrales_ordenados = ordenar_vertices(cent)
    print(", ".join(centrales_ordenados[:n]))

def camino_aux(minimo):
    recorrido = [minimo[3]]
    while recorrido[0] != minimo[2]:
        recorrido.insert(0, (minimo[1])[recorrido[0]])
    print(" -> ".join(recorrido))

def camino_mas(aeropuertos, vuelos, filtro, origen, destino):
    peso = 0
    if filtro == "barato":
        peso = 1
    minimo = ()
    for a_origen in aeropuertos[origen]:
        for a_destino in aeropuertos[destino]:
            dist, padre = camino_minimo(vuelos, a_origen, a_destino, peso)
            if not len(minimo) or (dist[a_destino] < (minimo[0])[minimo[3]]):
                minimo = (dist, padre, a_origen, a_destino)
    camino_aux(minimo)  

def camino_escalas(aeropuertos, vuelos, origen, destino):
    minimo = ()
    for a_origen in aeropuertos[origen]:
        for a_destino in aeropuertos[destino]:
            orden, padre = bfs(vuelos, a_origen, a_destino)
            if not len(minimo) or (orden[a_destino] < (minimo[0])[minimo[3]]):
                minimo = (orden, padre, a_origen, a_destino)
    camino_aux(minimo)
    
def procesar_archivos():
    aeropuertos = {}    
    vuelos = Grafo(False)
    with open(sys.argv[1]) as a:
        a_csv = csv.reader(a)
        for linea in a_csv:
            aeropuertos[linea[0]] = aeropuertos.get(linea[0], []) + [linea[1]]
    with open(sys.argv[2]) as v:
        v_csv = csv.reader(v)
        for origen, destino, tiempo, precio, cant_vuelos in v_csv:
            vuelos.agregar_arista(origen, destino, (int(tiempo), int(precio), 1/int(cant_vuelos)))
    return aeropuertos, vuelos

def listar_operaciones():
    for c in COMANDOS:
        print(c)

def ejecutar_comandos(comando_arr, aeropuertos, vuelos):
    if comando_arr[0] == "listar_operaciones":
        return listar_operaciones()
    datos = (" ".join(comando_arr[1:])).split(",")
    if comando_arr[0] == "camino_mas":
        return camino_mas(aeropuertos, vuelos, datos[0], datos[1], datos[2])
    if comando_arr[0] == "camino_escalas":
        return camino_escalas(aeropuertos, vuelos, datos[0], datos[1])
    if comando_arr[0] == "centralidad":
        return centralidad(vuelos, int(datos[0]))
    if comando_arr[0] == "centralidad_aprox":
        return centralidad_aprox(vuelos, int(datos[0]))
    if comando_arr[0] == "vacaciones":
        return vacaciones(aeropuertos, vuelos, datos[0], int(datos[1]))
    if comando_arr[0] == "itinerario":
        return itinerario(aeropuertos, vuelos, datos[0])
    if comando_arr[0] == "recorrer_mundo_aprox":
        return recorrer_mundo_aprox(vuelos, aeropuertos, datos[0])
    

def procesar_entradas(aeropuertos, vuelos):
    for linea in sys.stdin:
        comando_arr = (linea.rstrip('\n')).split(" ")
        ejecutar_comandos(comando_arr, aeropuertos, vuelos)

def main():
    aeropuertos, vuelos = procesar_archivos()
    procesar_entradas(aeropuertos, vuelos)

main()