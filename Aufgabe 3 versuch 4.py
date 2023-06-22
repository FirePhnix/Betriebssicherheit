import os
import graphviz
os.environ["PATH"] += os.pathsep + 'C:/Users/fabio/anaconda3/Library/bin/graphviz'

class ANDNODE:
    def __init__(self,name):
        self.name = name
        self.nodes = []
    def add(self,node):
        self.nodes.append(node)
        return
    #............
    def print(self, Graph):
        # aktueller Knoten einfügen
        Graph.node(self.name, label = self.name + ' (&)', shape ='rectangle')
        # alle unterknoten einfügen
        for node in self.nodes:
            # Kante vom aktuellen- zum unterknoten einfügen
            Graph.edge(self.name, node.name)
            if node != EVENT:
                # wenn der unterknoten kein event ist führe print für den unterknoten aus
                node.print(Graph)
        return
    def topdown(self,mat):
        #...............
        return mat

# Oder-Verknüpfungselement
class ORNODE:
    def __init__(self,name):
        self.name = name
        self.nodes = []
    def add(self,node):
        self.nodes.append(node)
        return
    #..............
    def print(self, Graph):
        # aktueller Knoten einfügen
        Graph.node(self.name, label = self.name + ' (>=1)', shape = 'rectangle')
        # alle unterknoten einfügen
        for node in self.nodes:
            # Kante vom aktuellen- zum unterknoten einfügen 
            Graph.edge(self.name, node.name)
            if node != EVENT:
                # wenn der unterknoten kein event ist führe print für den unterknoten aus
                node.print(Graph)
        return
    def topdown(self,mat):
        #..............
        return mat

# Standardeingang
class EVENT:
    name = ''
    def __init__(self,name):
        self.name = name
    #...............
    def print(self, Graph):
        # Den Event knoten einfügen
        Graph.node(self.name)
        return
    def topdown(self,mat):
        return mat

class CONNECT:
    def __init__(self, name):
        self.name = name
        self.con = None

    def getname(self):
        return self.name

class NODE:
    def __init__(self, name):
        self.name = name
        self.zero = CONNECT("ZERO")
        self.one = CONNECT("ONE")

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
        else:
            assert(0>1)

        return ntop

    def createand(self, node, ft):
        if isinstance(ft.nodes[0], EVENT):
            node.zero.con = BDDEVENT(ft.nodes[0].name)
        else:
            new_node = NODE(ft.nodes[0].name)
            node.zero.con = new_node
            self.create(new_node, ft.nodes[0])

        if isinstance(ft.nodes[1], EVENT):
            node.one.con = BDDEVENT(ft.nodes[1].name)
        else:
            new_node = NODE(ft.nodes[1].name)
            node.one.con = new_node
            self.create(new_node, ft.nodes[1])

    def createor(self, node, ft):
        event_names = []
        for node in ft.nodes:
            if isinstance(node, EVENT):
                event_names.append(node.name)
            else:
                new_node = NODE(node.name)
                node.zero.con = new_node
                self.create(new_node, node)

        event_names.sort()
        event_name = '+'.join(event_names)
        bdd_event = BDDEVENT(event_name)
        node.zero.con = bdd_event
        node.one.con = bdd_event

def convert_to_bdd(ft):
    bdd = FT2BDD()
    bdd.create(None, ft)
    return bdd

# Fehlerbaum Beispiel aus Aufgabe 2
TOP = ANDNODE('TOP')
A = ORNODE('A')
E1 = EVENT('1')
E2 = EVENT('2')
E3 = EVENT('3')

TOP.add(A)
TOP.add(E1)
A.add(E2)
A.add(E3)

# Fehlerbaum in BDD umwandeln
bdd = convert_to_bdd(TOP)

# BDD graphisch darstellen
bdd.dot.view()
