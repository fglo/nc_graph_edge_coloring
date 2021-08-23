import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as cls
import numpy as np
import math as math
from UsedColors import *

white = '#FFFFFF'

def start_experiment():
    used_colors = UsedColors()
    number_of_steps = 0
    same_color = False

    print("Coloring the graph...")

    number_of_nodes = random.randint(8,16)
    # G = nx.gnm_random_graph(8, 16)
    probability_of_edge = 0.4
    G = nx.gnp_random_graph(number_of_nodes, probability_of_edge)
    edges = list(G.edges)
    nodes_by_degrees_descending = sorted(dict(G.degree).items(), key=lambda d: d[1], reverse=True) 

    for u, v in edges:
        G[u][v]['color'] = white

    edge_labels = {}

    for i, d in nodes_by_degrees_descending:
        neighbor_colors = []
        
        for neighbor in G.neighbors(i):
            number_of_steps += 1
            if G[i][neighbor]['color'] != white:
                neighbor_colors.append(G[i][neighbor]['color'])
        
        for neighbor in G.neighbors(i):
            number_of_steps += 1
            neighbor_colors2 = neighbor_colors
            if G[i][neighbor]['color'] == white:
                for neighbor2 in G.neighbors(neighbor):
                    number_of_steps += 1
                    if G[neighbor][neighbor2]['color'] != white:
                        neighbor_colors2.append(G[neighbor][neighbor2]['color'])

                new_color = used_colors.getColorNotIn(neighbor_colors2)
                same_color = same_color or (new_color in neighbor_colors2)
                G[i][neighbor]['color'] = new_color
                edge_labels[(i,neighbor)] = new_color
                neighbor_colors.append(new_color)
                used_colors.pickColor(new_color)

    print("Are there neighbours with the same color: %r" % same_color)

    degree = max(dict(G.degree).values())
    number_of_edges = len(edges)
    number_of_used_colors = len(used_colors.colors)

    print("Number of steps: %d" % number_of_steps)
    print("Pesymistic complexity: %d" % (number_of_edges * (degree + degree * math.log(degree, 3))))
    mean = np.mean(np.random.poisson(number_of_nodes * probability_of_edge, 10000))
    print("Mean complexity: %d" % (number_of_edges * (mean + mean * math.log(mean, 3))))
    print("\n")

    print("Pesymistic number of used colors: %d" % number_of_edges)
    print("Number of used colors: %d" % number_of_used_colors)
    print("\n")

    print("Number of used colors: %d" % number_of_used_colors)
    print("Max node degree: %d" % degree)
    print("\n")

    print("Drawing the graph...")
    colors = [G[u][v]['color'] for u,v in edges]
    plt.figure()
    pos = nx.circular_layout(G)
    nx.draw(G,pos, node_color='#A0CBE2', edges=edges, edge_color=colors, width=5, node_size=1024, with_labels=True)
    nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels,font_color='red')
    plt.show()

for i in range(5):
    start_experiment()