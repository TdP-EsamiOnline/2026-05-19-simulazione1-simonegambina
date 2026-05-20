from model.artist import Artista
from model.generi import Genere
from model.model import Model

model = Model()

print(f"Numero nodi: {len(model._grafo.nodes)}")
#print("Numero nodi: ", model.get_numnodi())
#print("Numero archi: ", model.get_numarchi())

model.buildGraphP("Jazz")

#source = Artista(68, "Miles Davis")
source = Genere(2, "Jazz")

