import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self.chosen_business = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fill_dd_city(self):
        for c in self.model.cities:
            self.view.dd_city.options.append(ft.dropdown.Option(c, on_click=self.fill_dd_locali))

    def fill_dd_locali(self, e):
        self.view.dd_locale.options.clear()
        city = self.view.dd_city.value
        locali = self.model.get_locali(city)
        for loc in locali:
            self.view.dd_locale.options.append(ft.dropdown.Option(data=loc,
                                                                  text=loc,
                                                                  on_click=self.choose_business))
        self.view.update_page()

    def choose_business(self, e):
        if e.control.data is None:
            self.chosen_business = None
        self.chosen_business = e.control.data

    def handle_crea_grafo(self, e):
        if self.chosen_business is None:
            self.view.create_alert("Selezionare un locale")
            return
        self.model.build_graph(self.chosen_business)
        self.view.txt_result.controls.clear()
        n_nodi, n_archi = self.model.get_graph_details()
        self.view.txt_result.controls.append(ft.Text(f"Il grafo creato ha {n_nodi} nodi e {n_archi} archi"))
        review_max, n_uscenti = self.model.get_max_uscenti()
        self.view.txt_result.controls.append(ft.Text(f"La recensione con più archi uscenti è {review_max}, "
                                                     f"con {n_uscenti} archi"))
        self.view.update_page()

    def handle_miglioramento(self, e):
        path = self.model.get_percorso()
        self.view.txt_result.controls.clear()
        self.view.txt_result.controls.append(ft.Text(f"Il cammino trovato è il seguente: "))
        for i in range(len(path)-1):
            self.view.txt_result.controls.append(ft.Text(f"{path[i]} --> {path[i+1]}"))
        self.view.txt_result.controls.append(ft.Text(f"La differenza tra ultimo e primo è di "
                                                     f"{abs(path[-1][1].review_date-path[0][0].review_date)} giorni"))
        self.view.update_page()

    @property
    def view(self):
        return self._view

    @property
    def model(self):
        return self._model
