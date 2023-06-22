import os
import graphviz

os.environ["PATH"] += os.pathsep + 'C:/Users/fabio/anaconda3/Library/bin/graphviz'



class CONNECT:
    def __init__(self, name):
        self.name = name
        self.con = None

    def getname(self):
        return self.name


class NODE:
    def __init__(self, name):
        self.name = name

        self.zero = None
        self.one = None

    def getname(self):
        return self.name


class BDDEVENT:
    def __init__(self, name):
        self.name = name
        self.zero = None
        self.one = None

    def getname(self):
        return self.name


class FT2BDD:
    def __init__(self):
        self.nroot = None
        self.dot = graphviz.Digraph()

    def show(self):
        return self.dot

    def create(self, ntop, ft):
        if ntop is None:
            ntop = NODE("root")

        if self.nroot is None:
            self.nroot = ntop

        if isinstance(ft, ANDNODE):
            self.createand(ntop, ft)
        elif isinstance(ft, ORNODE):
            self.createor(ntop, ft)

        return ntop

    def createand(self, node, ft):
        n1 = NODE("AND")
        n1.zero = node.zero
        node.zero = n1
        n1.one = node.one
        node.one = n1

        self.create(node.zero, ft.nodes[0])
        self.create(node.one, ft.nodes[1])

    def createor(self, node, ft):
        n1 = NODE("OR")
        n1.zero = node.zero
        node.zero = n1
        n1.one = node.one
        node.one = n1

        self.create(node.zero, ft.nodes[0])
        self.create(node.one, ft.nodes[1])

    def convert_ft_to_bdd(self, ft):
        bdd = self.create(None, ft)
        return bdd


# Sample FT classes for testing
class ANDNODE:
    def __init__(self, name):
        self.name = name
        self.nodes = []

    def add(self, node):
        self.nodes.append(node)


class ORNODE:
    def __init__(self, name):
        self.name = name
        self.nodes = []

    def add(self, node):
        self.nodes.append(node)


# Sample FT
TOP = ANDNODE('TOP')
A = ORNODE('A')
E1 = BDDEVENT('1')
E2 = BDDEVENT('2')
E3 = BDDEVENT('3')

TOP.add(A)
TOP.add(E1)
A.add(E2)
A.add(E3)

# Convert FT to BDD
converter = FT2BDD()
bdd = converter.convert_ft_to_bdd(TOP)

# Visualization
def visualize_bdd(bdd):
    dot = bdd.show()

    def traverse_bdd(node):
        if isinstance(node, NODE):
            dot.node(node.getname(), shape='circle')
            if node.zero:
                dot.edge(node.getname(), node.zero.getname(), label='0')
                traverse_bdd(node.zero)
            if node.one:
                dot.edge(node.getname(), node.one.getname(), label='1')
                traverse_bdd(node.one)
        elif isinstance(node, BDDEVENT):
            dot.node(node.getname(), shape='circle')
            dot.edge(node.getname(), 'T', label='0')
            dot.edge(node.getname(), 'F', label='1')

    traverse_bdd(bdd.nroot)
    dot.render('bdd', format='jpg', view=True)


visualize_bdd(bdd)
