import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceDDStato = None
        self._grafo_creato = False

    def handleCalcola(self, e):
        self._view._txt_result.controls.clear()
        self._grafo_creato = False

        year = str(self._view._txtAnno.value)

        if year is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text("Inserisci un valore per l'anno.", color="red")
            )
            self._view.update_page()
            return

        try:
            yearInt = int(year)
        except ValueError:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text("Inserisci un valore numerico per l'anno.", color="red")
            )
            self._view.update_page()
            return

        if yearInt < 1816 or yearInt > 2016:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text("Inserisci un anno compreso tra 1816 e 2016.", color="red")
            )
            self._view.update_page()
            return

        self._model.build_graph(yearInt)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(
            ft.Text("Grafo correttamente creato.", color="green")
        )
        self._view._txt_result.controls.append(
            ft.Text(f"Il grafo ha {self._model.calcolaComponentiConnesse()} componenti connesse.")
        )
        self._view._txt_result.controls.append(
            ft.Text("Di seguito i dettagli sui nodi:")
        )
        for nodo, grade in self._model.getNodesWithDegree().items():
            self._view._txt_result.controls.append(
                ft.Text(f"{nodo} -- {grade}")
            )
        self._grafo_creato = True
        self._view.update_page()

    def handleStatiRaggiungibili(self, e):
        if self._choiceDDStato is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text("Attenzione, seleziona uno stato!", color="red")
            )
            self._view.update_page()
            return

        if not self._grafo_creato:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text("Attenzione, crea il grafo prima di calcolare gli Stati Raggiungibili!", color="red")
            )
            self._view.update_page()
            return

        raggiungibili = self._model.getRaggiungibili(self._choiceDDStato)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(
            ft.Text(f"Di seguito sono elencati tutti gli Stati raggiungibili da {self._choiceDDStato}.", color="green")
        )
        for r in raggiungibili:
            self._view._txt_result.controls.append(
                ft.Text(r)
            )
        self._view.update_page()

    def fillDDStato(self):
        countries = sorted(self._model.getAllCountries(), key=lambda x: x.StateNme)

        for c in countries:
            self._view._ddStato.options.append(
                ft.dropdown.Option(data=c, text=c.StateNme, on_click=self._readDDStato)
            )

        self._view.update_page()

    def _readDDStato(self, e):
        if e.control.data is None:
            self._choiceDDStato = None
        else:
            self._choiceDDStato = e.control.data
        print(f"Selezionato {self._choiceDDStato}")