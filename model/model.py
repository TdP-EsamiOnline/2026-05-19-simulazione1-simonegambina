import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()

    def getAllGenre(self):
        return DAO.getAllGenre()

    def buildGraphP(self, genere):
        self._grafo.clear()
        nodi = DAO.getAllNodes(genere)
        self._grafo.add_edges_from(nodi)
        #self.addEdgesPesati()

        print(f"Nodi inseriti: {len(self._grafo.nodes)}")
        for n in self._grafo.nodes:
            print(n)