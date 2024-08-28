import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listShape = []

    def fillDD(self):
        self._listYear = self._model.getYears()
        for anno in self._listYear:
            self._view.ddyear.options.append(ft.dropdown.Option(anno))
        self._view.update_page()

    def fillDDShape(self, anno):
        self._listShape = self._model.getShape(anno)
        for shape in self._listShape:
            self._view.ddshape.options.append(ft.dropdown.Option(shape))
        self._view.update_page()

    def read_anno(self, e):
        if e.control.value is None:
            self._anno = None
        else:
            self._anno = e.control.value
            self._view.ddshape.options.clear()
            self.fillDDShape(self._anno)

    def read_shape(self, e):
        if e.control.value is None:
            self._shape = None
        else:
            self._shape = e.control.value

    def handle_graph(self, e):
        anno = self._view.ddyear.value
        shape = self._view.ddshape.value
        if anno is None:
            self._view.create_alert("Anno non inserito")
            return
        if shape is None:
            self._view.create_alert("Shape non inserita")
            return

        self._model.buildGraph(anno, shape)
        self._view.txt_result1.controls.append(ft.Text(f"Numero di vertici: {self._model.getNumNodi()}"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di archi: {self._model.getNumArchi()}"))
        # STAMPA LA LISTA DEGLI ARCHI CHE HANNO PESI MAGGIORI
        self._view.txt_result1.controls.append(
            ft.Text(f"I 5 archi di peso maggiore sono:"))
        listaBest = self._model.getArchiPesoMaggiore()
        for arco in listaBest:
            self._view.txt_result1.controls.append(
                ft.Text(f"{arco[0]} -> {arco[1]} | weight = {arco[2]}"))
        self._view.update_page()


    def handle_path(self, e):
        pass
