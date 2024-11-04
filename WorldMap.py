import networkx as nx
from matplotlib import pyplot as plt

class WorldMap():
    nodes: list
    node_labels: dict
    node_colors: list
    edges: list

    def __init__(self, board, board_ref, color_ref) -> None:
        self.build_graph(board, board_ref, color_ref)

    def build_graph(self, board, board_ref, color_ref):
        import functions as fns
        colors = []
        territories = []
        territory_color = []
        territory_labels = {}
        troops = 0
        for territory in board:
            player_index = fns.get_player_here(board, territory)
            troops = fns.get_troops_here(board, territory)
            if player_index == -1:
                color = 'skyblue'
            else:
                color = color_ref[player_index]
            territories.append(territory)
            territory_color.append(color)
            territory_labels[territory] = f"{territory}: {troops}"
        connections = []
        for territory in board_ref:
            for col, neighbor in board_ref[territory]:
                if not ((territory, neighbor) in connections) and not ((neighbor, territory) in connections):
                    connections.append((territory, neighbor))
        self.nodes = territories
        self.edges = connections
        self.node_colors = territory_color
        self.node_labels = territory_labels
        