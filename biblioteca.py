from heapq import heappush, heappop, heapify
from cola import *
import random

def bfs(grafo, origen, destino):
    visitados = set()
    padres = {}
    orden = {}
    q = Cola()
    visitados.add(origen)
    padres[origen] = None
    orden[origen] = 0
    q.encolar(origen)
    while not q.esta_vacia():
        v = q.desencolar()
        if v == destino:
            break
        for w in grafo.adyacentes(v):
            if w not in visitados:
                visitados.add(w)
                padres[w] = v
                orden[w] = orden[v] + 1
                q.encolar(w)
    
    return orden, padres

def reconstruir_ciclo(padres, origen, penultimo, ultimo):
    recorrido = [penultimo]
    while recorrido[0] != origen:
        recorrido.insert(0, padres[recorrido[0]])
    recorrido.append(ultimo)
    return recorrido

def _obtener_ciclo_n_dfs(grafo, v, padres, orden, ord_probados, origen, n, aeropuertos):
    if orden[v] == n-1:
        for a in aeropuertos:
            if grafo.estan_unidos(a,v): return reconstruir_ciclo(padres, origen, v, a)
    for w in grafo.adyacentes(v):
        if w not in padres and orden[v] < n-1:
            if (w not in ord_probados or (orden[v] + 1) not in ord_probados[w]):
                padres[w] = v
                orden[w] = orden[v] + 1
                if w not in ord_probados: ord_probados[w] = set()
                ord_probados[w].add(orden[w])
                ciclo_n = _obtener_ciclo_n_dfs(grafo, w, padres, orden, ord_probados, origen, n, aeropuertos)
                if ciclo_n: 
                    return ciclo_n

    padres.pop(v)
    orden.pop(v)
    return None

def obtener_ciclo_n_dfs(grafo, origen, n, aeropuertos):
    padres = {}
    orden = {}
    ord_probados = {}
    for a in aeropuertos:
        padres[a] = None
        orden[a] = 0
        ord_probados[a] = 0
    ciclo_n = _obtener_ciclo_n_dfs(grafo, origen, padres, orden, ord_probados, origen, n, aeropuertos)
     
    return ciclo_n

def orden_topo(grafo):
    grados = {}
    for v in grafo.ver_vertices():
            grados[v] = 0
    for v in grafo.ver_vertices():
        for w in grafo.adyacentes(v):
            grados[w] += 1
    q = Cola() 
    for v in grafo.ver_vertices():
        if grados[v] == 0:
            q.encolar(v)
    resul = []
    while not q.esta_vacia():
        v = q.desencolar()
        resul.append(v)
        for w in grafo.adyacentes(v):
            grados[w] -= 1
            if grados[w] == 0: 
                q.encolar(w) 

    return resul

def camino_minimo(grafo, origen, destino, valor):
    dist = {}
    padre = {}
    for v in grafo.ver_vertices(): dist[v] = -1
    dist[origen] = 0
    padre[origen] = None
    heap = []
    heapify(heap)
    heappush(heap, (dist[origen], origen))
    while len(heap) > 0:
        v = heappop(heap)[1]
        if destino and v == destino: break
        for w in grafo.adyacentes(v):
            if (dist[w] == -1) or (dist[v] + (grafo.peso(v, w))[valor] < dist[w]):
                dist[w] = dist[v] + (grafo.peso(v, w))[valor]
                padre[w] = v
                heappush(heap, (dist[w], w))
    
    return dist, padre

def segundo_elem(elem):
    return elem[1]

def ordenar_vertices(distancias):
    ordenados = []
    dists = list(distancias.items())
    dists.sort(key = segundo_elem, reverse = True)
    ordenados = [i[0] for i in dists]
    return ordenados

def centralidad_aux(grafo):
    cent = {}
    for v in grafo.ver_vertices(): cent[v] = 0
    for v in grafo.ver_vertices():
        distancias, padre = camino_minimo(grafo, v, None, 2)
        cent_aux = {}
        for w in grafo.ver_vertices(): cent_aux[w] = 0
        vertices_ordenados = ordenar_vertices(distancias)
        for w in vertices_ordenados:
            if not padre[w]: continue
            cent_aux[padre[w]] += 1 + cent_aux[w]
        for w in grafo.ver_vertices():
            if w == v: continue
            cent[w] += cent_aux[w]
    return cent

def camino_aleatorio(grafo):
    visitados = set()
    cent = {}
    for v in grafo.ver_vertices():
        if v in visitados or not len(grafo.adyacentes(v)): continue
        for _ in range(10000):
            w = ady_aleatorio(grafo.adyacentes(v))
            cent[w] = cent.get(w,0) + 1
            if len(grafo.adyacentes(w)): 
                v = w
                visitados.add(v)
    return cent

def ady_aleatorio(pesos):
    total = sum([1/i[2] for i in list(pesos.values())])
    rand = random.uniform(0, total)
    acum = 0
    for vertice, peso_arista in pesos.items():
        if acum + 1/peso_arista[2] >= rand:
            return vertice
        acum += 1/peso_arista[2]