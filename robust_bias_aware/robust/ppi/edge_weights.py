import networkx as nx


class UnitEdgeWeight:
    """
    Simple unit edge weights. Every edge has the same weight. A Steiner tree, thus,
    minimizes just the number of vertices.
    """
    def __getitem__(self, e):
        return 1.0

            
class BiasAwareEdgeWeight:
    """
    TODO
    """
    def __init__(self, network: nx.Graph, gamma):
        self._graph = network
        self._gamma = float(gamma)
        self._average_max_bias = self._calculate_average_max_bias()
        
    def _calculate_average_max_bias(self):
        biases = nx.get_node_attributes(self._graph, 'study_bias_score')
        sum_ = 0
        for u, v in self._graph.edges:
            sum_ = sum_ + max(biases[u], biases[v])
        return sum_ / self._graph.number_of_edges()
    
    def __getitem__(self, e):
        max_edge_bias = max(self._graph.nodes[e[0]]['study_bias_score'], self._graph.nodes[e[1]]['study_bias_score'])
        return (1 - self._gamma) * self._average_max_bias + self._gamma * max_edge_bias




















