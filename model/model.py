import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._bestPath = []
        self._genereGrafo = None

    def getAllGenre(self):
        return DAO.getAllGenre()

    def getArtistGenre(self, genere):
        return DAO.getArtistGenre(genere)

    def buildGraphP(self, genere):
        self._grafo.clear()
        nodi = DAO.getAllNodes(genere)
        self._grafo.add_nodes_from(nodi)

        idMap = {}
        for n in nodi:
            idMap[n.ArtistId] = n

        edges = DAO.getAllEdges(genere)

        for e in edges:
            id1 = e["idArtista1"]
            id2= e["idArtista2"]

            pop1 = e["popolarita1"]
            pop2 = e["popolarita2"]

            peso = e["peso"]

            artista1 = idMap[id1]
            artista2 = idMap[id2]

            if pop1 > pop2:
                self._grafo.add_edge(artista1, artista2, weight= peso)

            elif pop2 > pop1:
                self._grafo.add_edge(artista2, artista1, weight= peso)

            else:
                self._grafo.add_edge(artista1, artista2, weight=peso)
                self._grafo.add_edge(artista2, artista1, weight=peso)

        self._genereGrafo = genere

        #print(f"Nodi inseriti: {len(self._grafo.nodes)}")
        #for n in self._grafo.nodes:
        #    print(n)

    def getGenereGrafo(self):
        return self._genereGrafo

    def getArtistaMaxInfluenza(self):
        bestArtista = None
        bestInfluenza = None

        for artista in self._grafo.nodes:
            peso_uscenti = 0
            peso_entranti = 0

            for _,_, dati in self._grafo.out_edges(artista, data=True):
                peso_uscenti += dati["weight"]

            for _,_, dati in self._grafo.in_edges(artista, data=True):
                peso_entranti += dati["weight"]

            influenza = peso_uscenti - peso_entranti

            if bestInfluenza is None or influenza > bestInfluenza:
                bestInfluenza = influenza
                bestArtista = artista

        return bestArtista, bestInfluenza

    def getTop5Edges(self):
        archi = list(self._grafo.edges(data=True))

        archi.sort(key=lambda x: x[2]["weight"], reverse=True)

        return archi[:5]


    def getNumNodes(self):
        return len(self._grafo.nodes)

    def getNumEdges(self):
        return len(self._grafo.edges)


    def getArtistByName(self, nomeArtista):
        for artista in self._grafo.nodes():
            if artista.Name == nomeArtista:
                return artista
        return None

    def getPesoArco(self, u, v):
        return self._grafo[u][v]["weight"]


    def getPercorsoPiuLungo(self, nomeArtista):
        artistaPartenza = self.getArtistByName(nomeArtista)

        if artistaPartenza is None:
            return []

        bestPath = []

        def ricorsione(nodoCorrente, pathCorrente, pesoPrecedente):
            nonlocal bestPath

            if len(pathCorrente) > len(bestPath):
                bestPath = copy.deepcopy(pathCorrente)

            for vicino in self._grafo.successors(nodoCorrente):
                pesoArco = self._grafo[nodoCorrente][vicino]["weight"]

                if vicino not in pathCorrente and pesoArco > pesoPrecedente:
                    pathCorrente.append(vicino)
                    ricorsione(vicino, pathCorrente, pesoArco)
                    pathCorrente.pop()

        ricorsione(artistaPartenza, [artistaPartenza], -1)

        return bestPath







