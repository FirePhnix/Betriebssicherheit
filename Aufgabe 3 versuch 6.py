import os
import graphviz

os.environ["PATH"] += os.pathsep + 'C:/Users/fabio/anaconda3/Library/bin/graphviz'

# Classes

# Und-Verknüpfungselement
class ANDNODE:
    def __init__(self, name):
        self.name = name
        self.nodes = []

    def add(self, node):
        self.nodes.append(node)

    def print(self, Graph):
        Graph.node(self.name, label=self.name + ' (&)', shape='rectangle')
        for node in self.nodes:
            Graph.edge(self.name, node.name)
            if not isinstance(node, EVENT):
                node.print(Graph)

    def topdown(self, mat):
        if self == TOP:
            mat[0] = self.nodes
            i = 0
            while i < len(mat):
                mat_node = False
                for i in range(len(mat)):
                    for j in range(len(mat[i])):
                        if not isinstance(mat[i][j], EVENT):
                            mat = mat[i][j].topdown(mat)
                            mat_node = True
                            break
                    if i == len(mat) - 1:
                        i = len(mat)
                    if mat_node:
                        break
        else:
            mat_node = False
            for i in range(len(mat)):
                for j in range(len(mat[i])):
                    if mat[i][j].name == self.name:
                        del mat[i][j]
                        for node in self.nodes:
                            mat[i].append(node)
                        mat_node = True
                        break
                if mat_node:
                    break
        return mat


# Oder-Verknüpfungselement
class ORNODE:
    def __init__(self, name):
        self.name = name
        self.nodes = []

    def add(self, node):
        self.nodes.append(node)

    def print(self, Graph):
        Graph.node(self.name, label=self.name + ' (>=1)', shape='rectangle')
        for node in self.nodes:
            Graph.edge(self.name, node.name)
            if not isinstance(node, EVENT):
                node.print(Graph)

    def topdown(self, mat):
        if self == TOP:
            del mat[0]
            anzahl_and = sum(isinstance(node, ANDNODE) for node in self.nodes)
            if anzahl_and < len(self.nodes):
                for i in range(len(self.nodes)):
                    if not isinstance(self.nodes[i], ANDNODE):
                        mat.append([self.nodes[i]])
            else:
                for i in range(len(self.nodes)):
                    mat.append([self.nodes[i]])
            i = 0
            while i < len(mat):
                mat_node = False
                for i in range(len(mat)):
                    for j in range(len(mat[i])):
                        if not isinstance(mat[i][j], EVENT):
                            mat = mat[i][j].topdown(mat)
                            mat_node = True
                            break
                    if i == len(mat) - 1:
                        i += 1
                    if mat_node:
                        break
        else:
            mat_node = False
            for i in range(len(mat)):
                for j in range(len(mat[i])):
                    if mat[i][j].name == self.name:
                        mat_kopie = mat[i]
                        del mat[i]
                        anzahl_and = sum(isinstance(node, ANDNODE) for node in self.nodes)
                        if anzahl_and < len(self.nodes):
                            for node in self.nodes:
                                if not isinstance(node, ANDNODE):
                                    mat_kopie[j] = node
                                    mat.append(list(mat_kopie))
                            mat_node = True
                            break
                        else:
                            for node in self.nodes:
                                mat_kopie[j] = node
                                mat.append(list(mat_kopie))
                            mat_node = True
                            break
                if mat_node:
                    break
        return mat


# Ausfallwahrscheinlichkeitselement
class EVENT:
    def __init__(self, name, probability):
        self.name = name
        self.probability = probability

    def print(self, Graph):
        Graph.node(self.name, label=self.name + ' (' + str(self.probability) + ')', shape='ellipse')


# Verbindungskante
class CONNECT:
    def __init__(self, name, node):
        self.name = name
        self.node = node

    def print(self, Graph):
        Graph.node(self.name, label=self.name, shape='point')
        Graph.edge(self.name, self.node.name)
        if not isinstance(self.node, EVENT):
            self.node.print(Graph)


# BDD-Node
class NODE:
    def __init__(self, name):
        self.name = name
        self.left = None
        self.right = None

    def print(self, Graph):
        Graph.node(self.name, label=self.name, shape='ellipse')
        self.left.print(Graph)
        self.right.print(Graph)


# BDD-Ausfallwahrscheinlichkeitselement
class BDDEVENT:
    def __init__(self, name, probability):
        self.name = name
        self.probability = probability

    def print(self, Graph):
        Graph.node(self.name, label=self.name + ' (' + str(self.probability) + ')', shape='ellipse')


# FT in BDD umwandeln
class FT2BDD:
    def __init__(self, root):
        self.root = root

    def create(self):
        bdd = NODE(self.root.name)
        bdd = self.build(bdd, self.root)
        return bdd

    def build(self, bdd_node, ft_node):
        if isinstance(ft_node, EVENT):
            return BDDEVENT(ft_node.name, ft_node.probability)
        elif isinstance(ft_node, ANDNODE):
            if bdd_node.left is None:
                bdd_node.left = self.build(bdd_node.left, ft_node.nodes[0])
                bdd_node.right = self.build(bdd_node.right, ft_node.nodes[1])
            else:
                bdd_node.right = self.build(bdd_node.right, ft_node)
            return bdd_node
        elif isinstance(ft_node, ORNODE):
            if bdd_node.left is None:
                bdd_node.left = self.build(bdd_node.left, ft_node.nodes[0])
                bdd_node.right = self.build(bdd_node.right, ft_node.nodes[1])
            else:
                left = NODE(bdd_node.name + 'L')
                right = NODE(bdd_node.name + 'R')
                left = self.build(left, ft_node.nodes[0])
                right = self.build(right, ft_node.nodes[1])
                bdd_node.left = left
                bdd_node.right = right
            return bdd_node

    def show(self, bdd):
        Graph = graphviz.Digraph('BDD', filename='BDD.gv', format='png')
        bdd.print(Graph)
        Graph.view()

# Print FT using Graphviz
def print_ft(ft):
    Graph = graphviz.Digraph('FT', filename='FT.gv', format='png')
    ft.print(Graph)
    Graph.view()

# Print BDD using Graphviz
def print_bdd(bdd):
    Graph = graphviz.Digraph('BDD', filename='BDD.gv', format='png')
    bdd.print(Graph)
    Graph.view()

# Sample usage
if __name__ == '__main__':
    # Create FT
    E1 = EVENT('E1', 0.1)
    E2 = EVENT('E2', 0.2)
    E3 = EVENT('E3', 0.15)
    E4 = EVENT('E4', 0.25)

    AND1 = ANDNODE('AND1')
    AND1.add(E1)
    AND1.add(E2)

    AND2 = ANDNODE('AND2')
    AND2.add(E3)
    AND2.add(E4)

    OR1 = ORNODE('OR1')
    OR1.add(AND1)
    OR1.add(AND2)

    FT = OR1

    # Print FT
    print_ft(FT)

    # Convert FT to BDD
    converter = FT2BDD(FT)
    BDD = converter.create()

    # Print BDD
    print_bdd(BDD)
