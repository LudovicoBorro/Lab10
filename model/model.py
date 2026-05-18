import networkx as nx

from database.DAO import DAO

class Model:

    def __init__(self):
        self._graph = nx.Graph()
        self._idMapCountry = {}
        allCountries = DAO.getAllCountry()
        for country in allCountries:
            self._idMapCountry[country.CCode] = country
        self._comp_connesse = set()

    def build_graph(self, year: int):
        self._graph.clear()
        allNodes = DAO.getAllNodes(year, self._idMapCountry)
        self._graph.add_nodes_from(allNodes)
        self.addEdges(year)

    def addEdges(self, year):
        allEdges = DAO.getAllEdges(year, self._idMapCountry)
        for edge in allEdges:
            self._graph.add_edge(edge.Country1, edge.Country2)

    def calcolaComponentiConnesse(self):
        return len(list(nx.connected_components(self._graph)))

    def getNumNodi(self):
        return len(self._graph.nodes)

    def getNumEdges(self):
        return len(self._graph.edges)

    def getNodesWithDegree(self):
        allNodes = self._graph.nodes
        allNodesSorted = sorted(allNodes, key=lambda x: x.StateNme)
        nodesWithGrade = {}
        for node in allNodesSorted:
            nodesWithGrade[node] = self._graph.degree(node)
        return nodesWithGrade

    def getRaggiungibili(self, source):
        nodiWNx = self._visitWithNx(source)
        nodiWIt = self._visitWithIteration(source)
        print(nodiWNx)
        print(nodiWIt)
        if len(nodiWNx) == len(nodiWIt):
            print("Le due liste hanno la stessa lunghezza.")
        else:
            print("Le liste hanno lunghezze diverse!!")
            print(f"Lunghezza lista ottenuta con networkX: {len(nodiWNx)}")
            print(f"Lunghezza lista ottenuta con approccio iterativo: {len(nodiWIt)}")
        return nodiWNx

    def _visitWithNx(self, source):
        tree = nx.bfs_tree(self._graph, source)
        nodes = []
        for node in tree.nodes:
            if node != source:
                nodes.append(node)
        return nodes

    def _visitWithIteration(self, source):
        visitati = []
        daVisitare = [source]
        while len(daVisitare) > 0:
            node = daVisitare.pop()
            for vicino in self._graph.neighbors(node):
                if vicino not in visitati:
                    daVisitare.append(vicino)
            if node != source and node not in visitati:
                visitati.append(node)
        return visitati

    @staticmethod
    def getAllCountries():
        return DAO.getAllCountry()