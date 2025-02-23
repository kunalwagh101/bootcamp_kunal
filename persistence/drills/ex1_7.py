import pickle

class Graph:
    def __init__(self):
        self.adj_list = {}

    def add_edge(self, node1, node2):
        if node1 not in self.adj_list:
            self.adj_list[node1] = []
        if node2 not in self.adj_list:
            self.adj_list[node2] = []
        self.adj_list[node1].append(node2)
        self.adj_list[node2].append(node1)

    def serialize(self):  
        return pickle.dumps(self)

    @classmethod
    def deserialize(cls, data):
        return pickle.loads(data)

if __name__ == "__main__":
    g = Graph()
    g.add_edge("A", "B")
    g.add_edge("A", "C")

    serialized_graph = g.serialize()
    new_g = Graph.deserialize(serialized_graph)

    print(new_g.adj_list)
