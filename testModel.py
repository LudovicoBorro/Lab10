from model.model import Model

model = Model()
model.build_graph(1980)
print("Grafo correttamente creato")
print(f"Il grafo contiene {model.getNumNodi()} nodi e {model.getNumEdges()} archi.")