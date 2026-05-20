import flet as ft

from model import model


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._generi = None
        self._artisti = None

    def fillDDGenre(self):
        genres = self._model.getAllGenre()
        self._view._ddGenre.options.clear()
        for g in genres:
            self._view._ddGenre.options.append(
                    ft.dropdown.Option(g["name"]))

        self._view.update_page()

        #if dd.label == "Genere":
        #    for g in genres:
        #        dd.options.append(ft.dropdown.Option(text=g,
        #                                             data=g,
        #                                             on_click=self.read_DD_Genres))

        #genresDD = []
        #for g in genres:
        #    genresDD.append(ft.dropdown.Option(g))

        #for g in genres:
        #    self._view._ddGenre.options.append(
        #        ft.dropdown.Option(data=g,
        #                           key=g.name,
        #                           on_click=self._choiceGenre))

    #def read_DD_Genres(self, e):
    #    print("read_DD_Genres called ")
    #    if e.control.data is None:
    #        self._generi = None
    #    else:
    #        self._generi = e.control.data

    def handleChangeGeneri(self, e):
        genere = self._view._ddGenre.value

        if genere is None:
            return

        self._view._ddArtist.options.clear()
        self._view._ddArtist.value = None

        artisti = self._model.getArtistGenre(genere)

        for a in artisti:
            self._view._ddArtist.options.append(
                ft.dropdown.Option(a["Name"]))

        self._view._ddArtist.disabled = False
        self._view.update_page()

    def fillDDArtist(self, dd: ft.Dropdown()):
        artists = self._model.getArtistGenre()

        if dd.label == "Artist":
            for a in artists:
                dd.options.append(ft.dropdown.Option(text=a,
                                                     data=a,
                                                     on_click=self.read_DD_Artist))

    def read_DD_Artist(self, e):
        print("read_DD_Artist called")
        if e.control.data is None:
            self._artisti = None
        else:
            self._artisti = e.control.data

    #def _choiceGenre(self, e):
    #    self._choiceGenre = e.control.data
    #    print(f"Hai selezionato il genere {self._choiceGenre}")

    def handleCreaGrafo(self, e):
        genere = self._view._ddGenre.value

        if genere is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione, selezionare un genere.",
                        color="red"))
            self._view.update_page()
            return

        self._model.buildGraphP(genere)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo per il genere {genere} correttamente creato.",
                                                      color="green"))
        self._view.txt_result.controls.append(
            ft.Text(f"Il grafo è composto da {self._model.getNumNodes()} nodi "
                    f"e da {self._model.getNumEdges()} archi."))

        artista, influenza = self._model.getArtistaMaxInfluenza()

        self._view.txt_result.controls.append(
            ft.Text(f"Artista con maggiore influenza: {artista} - influenza: {influenza}"))

        self._view.txt_result.controls.append(
            ft.Text("Top 5 archi con peso maggiore:"))

        top5 = self._model.getTop5Edges()

        for u, v, dati in top5:
            self._view.txt_result.controls.append(
                ft.Text(f"{u.Name} -> {v.Name} | peso: {dati["weight"]}"))

        self._view.update_page()


    def handleCammino(self,e):
        print("Click su Trova percorso")
        self._view.txt_result.controls.clear()

        genere = self._view._ddGenre.value
        artista = self._view._ddArtist.value

        if genere is None or genere == "":
            self._view.txt_result.controls.append(
                ft.Text("Errore: selezionare un genere.",
                        color="red"))
            self._view.update_page()
            return

        if artista is None or artista == "" :
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione, selezionare un artista.",
                        color="red"))
            self._view.update_page()
            return

        if self._model.getNumNodes() == 0:
            self._view.txt_result.controls.append(
                ft.Text("Errore: prima devi creare il grafo.",
                        color="red"))
            self._view.update_page()
            return

        if self._model.getGenereGrafo() != genere:
            self._view.txt_result.controls.append(
                ft.Text("Errore: hai cambiato genere. Devi ricreare il grafo.",
                        color="red"))
            self._view.update_page()
            return

        self._view.txt_result.controls.append(
            ft.Text(f"Hai selezionato l'artista {artista}",
                    color="blue"))


        path = self._model.getPercorsoPiuLungo(artista)

        if len(path) == 0:
            self._view.txt_result.controls.append(
                ft.Text("Nessun percorso trovato."))
            self._view.update_page()
            return

        self._view.txt_result.controls.append(
            ft.Text(f"Percorso più lungo a partire da {artista}:"))
        self._view.txt_result.controls.append(
            ft.Text(f"Lunghezza: {len(path) - 1} archi"))
        self._view.txt_result.controls.append(ft.Text("-" * 50))

        for i in range(len(path) -1):
            u = path[i]
            v = path[i+1]
            peso = self._model.getPesoArco(u, v)

            self._view.txt_result.controls.append(
                ft.Text(f"{u.Name} -> {v.Name} | peso: {peso}"))

        self._view.update_page()
