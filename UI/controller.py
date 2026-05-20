import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._generi = None

    def fillDDGenre(self, dd: ft.Dropdown()):
        genres = self._model.getAllGenre()

        if dd.label == "Genere":
            for g in genres:
                dd.options.append(ft.dropdown.Option(text=g,
                                                     data=g,
                                                     on_click=self.read_DD_Genres))

        #genresDD = []
        #for g in genres:
        #    genresDD.append(ft.dropdown.Option(g))

        #for g in genres:
        #    self._view._ddGenre.options.append(
        #        ft.dropdown.Option(data=g,
        #                           key=g.name,
        #                           on_click=self._choiceGenre))

    def read_DD_Genres(self, e):
        print("read_DD_Genres called ")
        if e.control.data is None:
            self._generi = None
        else:
            self._generi = e.control.data

    #def _choiceGenre(self, e):
    #    self._choiceGenre = e.control.data
    #    print(f"Hai selezionato il genere {self._choiceGenre}")

    def handleCreaGrafo(self, e):
        pass

    def handleCreaGrafo(self,e):
        pass

    def handleCammino(self,e):
        pass