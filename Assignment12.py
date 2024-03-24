
from random import randint, shuffle
import Assignment11 as as11
import Assignment8 as as8


class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

    def __str__(self):
        return "" if self is None else f"{self.key} -> [{self.left} , {self.right}]"


# [1] Declare a variable size and assign it a number, e.g. 100. Build a list of numbers between 1 and size,
# and then shuffle the numbers into a random permutation. We will refer to this list as the "keys".
def random_list(n):
    l = ordered_list(n)
    shuffle(l)
    return l


def ordered_list(n):
    l = [i for i in range(n)]
    return l


# [2] Define a function build_tree(keys) that builds a binary search tree by starting with a root node with key key[
# 0] and gradually inserts the remaining keys following the BST property (smaller on the left, larger on the right).
# We will use a simple list as a node, in which node[0] is the key, node[1] is the left subtree (LST), and node[2] is
# the right subtree (RST).
def build_tree(keys):
    tree = Node(keys[0])
    for key in keys[1:]:
        insert(tree, key)
    return tree


def insert(root, key):
    if root is None:
        return Node(key)
    elif root.key == key:
        return root
    elif root.key > key:
        root.left = insert(root.left, key)
    else:
        root.right = insert(root.right, key)
    return root


# [3] Implement the following functions
# height(tree) - determine the height of the tree
def height(tree):
    if tree is None:
        return -1
    elif tree.right is None and tree.left is None:
        return 0
    else:
        return 1 + max(height(tree.left), height(tree.right))


def print_tree_properties(description, tree, properties):
    data = [[prop.__name__, prop(tree)] for prop in properties]
    headers = ["Property name", "Value"]
    alignments = ["l"] * 2
    as8.print_table(description, headers, data, alignments)


# num_nodes(tree) - number of nodes in the tree (should match what we started with)
# num_edges(tree) - number of edges in the tree (should be one less than number of nodes)
# sum_keys(tree) - sum of the keys in all nodes
# avg_keys(tree) - average of all keys in the tree
# med_key(tree) - median of all keys on the tree
# depth(tree, node) - determines the distance of a node relative to the root
# preorder(tree) - pre-order traversal of the tree
def preorder(tree):
    if tree is None:
        return ""
    else:
        return clean(f"{tree.key} {preorder(tree.left)} {preorder(tree.right)}")


# inorder(tree) - in-order traversal of the tree
def inorder(tree):
    if tree is None:
        return ""
    else:
        return clean(f"{inorder(tree.left)} {tree.key} {inorder(tree.right)}")


# postorder(tree) - post-order traversal of the tree
def postorder(tree):
    if tree is None:
        return ""
    else:
        return clean(f"{postorder(tree.left)} {postorder(tree.right)} {tree.key}")


# reverseorder(tree) - reverse-order traversal of the tree
def reverseorder(tree):
    if tree is None:
        return ""
    else:
        return clean(f"{reverseorder(tree.right)} {tree.key} {reverseorder(tree.left)}")


def clean(s):
    while s.find("  ") >= 0:
        s = s.replace("  ", " ")
    return s


# min_key(tree) - minimum key in the tree
def min_key(tree):
    if tree is None:
        return 9999
    elif tree.left is None:
        return tree.key
    else:
        return min_key(tree.left)


# max_key(tree) - the maximum key in the tree
def max_key(tree):
    if tree is None:
        return -1
    elif tree.left is None:
        return tree.key
    else:
        return max_key(tree.right)


# [4] Define a function print_tree_properties that prints the name and value of each function listed in [3].


# [5] Define functions
# tree_to_matrix(tree) that maps a tree into an adjacency matrix
def tree_to_matrix(edges, n):
    matrix = [[0] * n for _ in range(n)]
    for edge in edges:
        i, j = edge
        matrix[i][j] = 1
    return matrix


# tree_to_tablex(tree) that maps a tree into an adjacency table
# tree_to_edges(tree) that maps a tree into an edge set
def tree_to_edges(tree, edges=None):
    if edges is None:
        edges = set()
    if tree is None:
        return edges
    if tree.right:
        edges.add((tree.key, tree.right.key))
        tree_to_edges(tree.right, edges)
    if tree.left:
        edges.add((tree.key, tree.left.key))
        tree_to_edges(tree.left, edges)
    return edges


# [6] Use the function from an earlier assignment to analyze the vertex properties of the obtained graph


# [7] Use the functions from an earlier assignment to analyze the relation properties of the obtained graph


# [8] Define a function draw_tree(tree) that draws the tree using the edge-list and draw_graph() from earlier assignment


# [9] Wrap all the functionality from the previous tasks into a function do_tree(tree)


# [10] Build a Balanced Binary Search Tree using the approach at
# https://www.geeksforgeeks.org/sorted-array-to-balanced-bst/ and then call do_tree(on the bbst)


def do_tree(assn, desc, keys):
    tree = build_tree(keys)
    edges = set()
    edges = tree_to_edges(tree, edges)
    matrix = tree_to_matrix(edges, len(keys))
    as11.do_graph(assn, desc, matrix, dir=True)
    properties = [height, min_key, max_key, inorder, reverseorder, preorder, postorder]
    print_tree_properties("tree properties", tree, properties)
    print("vertices", len(keys), "edges", len(edges))
    print("=" * 80)
    return tree


def main():
    assn = "Assignment12"
    keys = random_list(10)
    do_tree(assn, "random_tree", keys)

    keys = ordered_list(10)
    do_tree(assn, "ordered_tree", keys)

    keys = ordered_list(10)[::-1]
    do_tree(assn, "backward_tree", keys)


if __name__ == '__main__':
    main()

