from model.model import Model


def main():
    model = Model()

    genere = "Jazz"

    model.buildGraphP(genere)

    print("Genere:", genere)
    print("Numero nodi:", model.getNumNodes())
    print("Numero archi:", model.getNumEdges())

    print("-" * 80)

    artista, influenza = model.getArtistaMaxInfluenza()

    print("Artista con maggiore influenza:")
    print(artista)
    print("Influenza:", influenza)

    print("-" * 80)

    print("Top 5 archi per peso:")

    top5 = model.getTop5Edges()

    for u, v, dati in top5:
        print(u, "->", v, "peso:", dati["weight"])


if __name__ == "__main__":
    main()