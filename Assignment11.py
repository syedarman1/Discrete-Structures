
from random import random
import numpy as np
from matplotlib import pyplot as plt
import Assignment8 as as8
import networkx as nx


# [1] Define a function read_graph(file_name) that reads in a graph from a file in the form of an adjacency matrix.
def read_graph(file_name):
    with open(file_name) as f:
        lines = f.readlines()
        return [[1 if c == "1" else 0 for c in line.strip().split(" ")] for line in lines]


# [2] Define a function print_adj_matrix(matrix) that nicely prints a graph stored as an adjacency matrix.
def print_adj_matrix(matrix):
    print(np.array(matrix))


# [3] Define a function adjacency_table(matrix) that converts an adjacency matrix into an adjacency table.
def adj_table(matrix):
    table = []
    n = len(matrix)
    for i in range(n):
        row = []
        for j in range(n):
            if matrix[i][j] == 1:
                row.append(j)
        table.append(row)
    return table


# def a function incidence_matrix that provide the incidence_matrix graph
def incidence_matrix(matrix, dir):
    edges = list(edge_set(matrix, dir))
    n_edges = len(edges)
    n_vertices = len(matrix)
    inc_matrix = [[0] * n_edges for j in range(n_vertices)]
    for k in range(n_edges):
        i, j = edges[k]
        inc_matrix[i][k] = 1
        inc_matrix[j][k] = 1
    return inc_matrix


# [4] Define a function print_adj_table(table) that nicely prints a graph stored as an adjacency table.
def print_adj_table(table):
    for i in range(len(table)):
        print(i, ":", table[i])


# [5] Define a function edge_set(matrix) that converts an adjacency matrix into a list of edges.
def edge_set(matrix, dir):
    edges = set()
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] == 1 and (dir or i > j):
                edges.add((i, j))
    return edges


# [6] Define a function random_graph(n, s, p) with n vertices, s if symmetric, and probability of edge p.
def random_graph(n, dir, p):
    matrix = [[0] * n for i in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if random() < p:
                matrix[i][j] = 1
                if not dir:
                    matrix[i][j] = 1
            if dir and random() < p:
                matrix[j][i] = 1
    return matrix


# [7] Define functions that determine the properties of the relation E. (See Overview above.)
# Reflexive - if aRa is true for every a in S.
# Irreflexive - if aRa may sometimes be true but not always true for every a in S
# Anti-reflexive - if aRa is false for every a in S
# Symmetric - if aRb is true implies bRa is true for every a and b in S
# Asymmetric - if aRb is true implies bRa is false for every a and b in S
# Antisymmetric - if aRb is true implies bRa is false for every a and b in S unless a and b are equal
# Transitive - if aRb is true and bRc is true, then aRc must also be true for every a, b, c in S
# Intransitive - if aRb is true and bRc is true, then aRc is not necessarily true for every a, b, c in S
# Antitransitive - if aRb is true and bRc is true, then aRc is false for every a, b, c in S
def reflexive(matrix):
    for i in range(len(matrix)):
        if matrix[i][i] == 0:
            return False
    return True


def anti_reflexive(matrix):
    for i in range(len(matrix)):
        if matrix[i][i] == 1:
            return False
    return True


def irreflexive(matrix):
    return not reflexive(matrix) and not anti_reflexive(matrix)


def symmetric(matrix):
    for i in range(len(matrix)):
        for j in range(i+1, len(matrix)):
            if matrix[i][j] != matrix[j][i]:
                return False
    return True


def anti_symmetric(matrix):
    for i in range(len(matrix)):
        for j in range(i+1, len(matrix)):
            if matrix[i][j] != matrix[j][i] and i != j:
                return False
    return True


def asymmetric(matrix):
    for i in range(len(matrix)):
        for j in range(i+1, len(matrix)):
            if matrix[i][j] == matrix[j][i]:
                return False
    return True


def transitive(matrix):
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if matrix[i][j] == 1 and matrix[j][k] == 1 and matrix[i][k] == 0:
                    return False
    return True


def anti_transitive(matrix):
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if matrix[i][j] == 1 and matrix[j][k] == 1 and matrix[i][k] == 1:
                    return False
    return True


def intransitive(matrix):
    return not transitive(matrix) and not anti_transitive(matrix)


# [8] Define a function print_properties(graph) that prints the properties determined in the previous task.
def print_properties(description, matrix, properties):
    data = [[prop.__name__, str(prop(matrix))] for prop in properties]
    headers = ["Property name", "Value"]
    alignments = ["l"] * 2
    as8.print_table(description, headers, data, alignments)


# [9] Define a function print_verticies(graph) that lists each vertex and its in-degree, out-degree, and neighbors.
def print_vertex_properties(description, matrix):
    data = [[i, outdegree(matrix, i), indegree(matrix, i), neighbors(matrix, i)] for i in range(len(matrix))]
    headers = ["Vertex", "Out Degree", "In Degree", "Neighbors"]
    alignments = ["r", "r", "r", "l"]
    as8.print_table(description, headers, data, alignments)


def neighbors(matrix, v):
    return [j for j in range(len(matrix)) if matrix[v][j] == 1]


def outdegree(matrix, v):
    return sum([matrix[v][i] for i in range(len(matrix))])


def indegree(matrix, v):
    return sum([matrix[i][v] for i in range(len(matrix))])


# [10] Define a function draw_graph(graph) that draws a graph and saves it as an image file. See
# https://stackoverflow.com/questions/20133479/how-to-draw-directed-graphs-using-networkx-in-python
# https://stackoverflow.com/questions/74312314/draw-a-directed-graph-in-python
def draw_graph(edges, directed, file_name):
    G = nx.DiGraph()
    G.add_edges_from(edges)
    val_map = {'A': 1.0, 'D': 0.5714285714285714, 'H': 0.0}
    values = [val_map.get(node, 0.25) for node in G.nodes()]
    pos = nx.spring_layout(G)
    cmap = plt.get_cmap('jet')
    nx.draw_networkx_nodes(G, pos, cmap=cmap, node_color=values, node_size=500)
    nx.draw_networkx_labels(G, pos, font_size=12, font_color='white')
    if directed:
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color='r', arrows=directed, arrowsize=10)
    else:
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color='r', arrows=False)
    plt.savefig(file_name)
    plt.show()


def do_graph(assn, description, matrix, dir):
    print(description)
    print("\nAdjacency Matrix:")
    print_adj_matrix(matrix)

    print("\nAdjacency Table:")
    table = adj_table(matrix)
    print_adj_table(table)

    print("\nEdge Set:")
    edges = edge_set(matrix, dir)
    print(edges)

    print("\nIncidence Matrix:")
    inc_matrix = incidence_matrix(matrix, dir)
    print_adj_matrix(inc_matrix)

    properties = [reflexive, anti_reflexive, irreflexive, symmetric, anti_symmetric, asymmetric,
                  transitive, intransitive, anti_transitive]
    print_properties("\nRelation Properties for the Graph", matrix, properties)
    print_vertex_properties("\nVertex Properties for the Graph", matrix)
    print()
    image_file = assn + "_" + description.replace(" ", "-") + ".png"
    draw_graph(edges, dir, image_file)


def main():
    assn = "Assignment11"
    matrix = read_graph("Graph1.txt")
    do_graph(assn, "Graph Read from Graph1.txt", matrix, True)
    matrix2 = random_graph(8, False, 0.5)
    do_graph(assn, "Random Graph of Size 8", matrix2, False)
    matrix3 = random_graph(10, True, .9)
    do_graph(assn, "Random Graph of Size 10 with P = .9", matrix3, True)


if __name__ == "__main__":
    main()
