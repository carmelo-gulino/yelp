import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.cities = DAO.get_all_cities()
        self.locali = None
        self.graph = None
        self.reviews_map = None

    def get_locali(self, city):
        return DAO.get_locali(city)

    def build_graph(self, business):
        self.graph = nx.DiGraph()
        reviews = DAO.get_reviews(business.business_id)
        self.reviews_map = {r.review_id: r for r in reviews}
        self.graph.add_nodes_from(reviews)
        for r in self.graph.nodes:
            for r2 in self.graph.nodes:
                if r != r2 and r.review_date > r2.review_date:
                    peso = abs(r.review_date - r2.review_date)
                    if peso != 0:
                        self.graph.add_edge(r, r2, weight=peso)

    def get_max_uscenti(self):
        nodo_uscenti = []
        for node in self.graph.nodes:
            successor = [s for s in self.graph.successors(node)]
            nodo_uscenti.append((node, len(successor)))
        nodo_uscenti.sort(key=lambda x: x[1], reverse=True)
        return nodo_uscenti[0][0], nodo_uscenti[0][1]

    def get_graph_details(self):
        return len(self.graph.nodes), len(self.graph.edges)

    def get_percorso(self):
        self.best_sol = []
        for n in self.graph.nodes:
            for s in self.graph.successors(n):
                parziale = [(n, s)]
                self.ricorsione(parziale)
                parziale.pop()
        return self.best_sol

    def ricorsione(self, parziale):
        ultimo = parziale[-1][1]
        if len(parziale) > len(self.best_sol):
            self.best_sol = copy.deepcopy(parziale)
            print(parziale)
        for s in self.graph.successors(ultimo):
            if (s, ultimo) not in parziale and s.stars >= ultimo.stars:
                parziale.append((ultimo, s))
                self.ricorsione(parziale)
                parziale.pop()
