import os
import graphviz
os.environ["PATH"] += os.pathsep + 'C:/Users/fabio/anaconda3/Library/bin/graphviz'

# Klassen

# Und-Verknüpfungselement
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
        if self == TOP:
            # speicher die unterknoten in mat (da wegen & beide gebraucht werden)
            mat[0] = self.nodes
            i=0
            while i < len(mat):
                #Sobald eine node gefunden wird werden die for-schleifen abgebrochen
                mat_node = False
                for i in range(len(mat)):
                    for j in range(len(mat[i])):
                        # Wenn der Unterknoten kein event ist
                        if type(mat[i][j]) != EVENT:
                            # rufe die topdown funktion des Unterknotens auf und speichere den rückgabewert
                            mat = mat[i][j].topdown(mat)
                            mat_node = True
                            break
                    # Wenn alle Knoten Events waren stoppe die while schleife
                    if i == len(mat)-1:
                        i = len(mat)
                    if mat_node == True:
                        break                
        else:
            mat_node = False
            for i in range(len(mat)):
                for j in range(len(mat[i])):
                    if mat[i][j].name == self.name:
                        # lösche die ANDNODE aus der Liste
                        del mat[i][j]
                        for node in self.nodes:
                            # hänge da wo die ANDNODE drin stand beide ihrer Unterknoten an
                            mat[i].append(node)
                        mat_node = True
                        break
                if mat_node:
                    break
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
        if self == TOP:
            # weil es OR ist wird nur ein Unterknoten pro weg benötigt also muss die while schleife nur einmal ausgeführt werden
            i = 0
            # Sucht die erste ANDNODE im mat Array
            while type(mat[i][0]) != ANDNODE:
                i += 1
            # speicher die ANDNODE in einer Variablen
            andnode = mat[i][0]
            # Ersetze die ANDNODE in mat mit ihren beiden Unterknoten
            del mat[i][0]
            for node in andnode.nodes:
                mat[i].append(node)
            # Rufe die topdown Funktion rekursiv auf um eventuell weitere ORNODES zu ersetzen
            mat = self.topdown(mat)
        else:
            # wenn es eine ORNODE ist suche die ANDNODE und ersetze sie mit den unterknoten
            # i zählt die zustände im mat array
            i = 0
            # wenn ein ANDNODE gefunden wurde breake die for schleife
            while i < len(mat):
                for j in range(len(mat[i])):
                    if mat[i][j].name == self.name:
                        # lösche die ORNODE aus der Liste
                        del mat[i][j]
                        for node in self.nodes:
                            # hänge da wo die ORNODE drin stand alle ihrer Unterknoten an
                            mat[i].append(node)
                        # ein Knoten wurde ersetzt
                        break
                    # wenn keine ANDNODE gefunden wurde inkrementiere i
                    if j == len(mat[i])-1:
                        i += 1
                # wenn ein Knoten ersetzt wurde breake die while schleife
                if i < len(mat):
                    break
        return mat

# Event (Blatt)
class EVENT:
    def __init__(self,name):
        self.name = name
    def print(self, Graph):
        #fügt Knoten zum Graphen hinzu
        Graph.node(self.name, shape = 'circle')
        return
    def topdown(self,mat):
        # sobald die Funktion für ein EVENT ausgeführt wird breche die while schleife ab
        i = len(mat)
        return mat


# Funktionen

# Erzeugt ein Beispielbaum
def Beispielbaum():
    global TOP, A, E1, E2, E3
    TOP = ANDNODE('TOP')
    A = ORNODE('A')
    E1 = EVENT('1')
    E2 = EVENT('2')
    E3 = EVENT('3')

    TOP.add(A)
    TOP.add(E1)
    A.add(E2)
    A.add(E3)
    return

class CONNECT:
    def __init__(self,name):
        self.name = name
        self.con = None
    #...
    def getname(self):
        return self.name
    

class BDDEVENT:
    def __init__(self,name):
        self.name = name
        self.zero = None
        self.one = None

    #...

    def getname(self):
        return self.name
    
class BDDNODE:
    def __init__(self,name):
        self.name = name

        self.zero = CONNECT("ZERO")
        self.one = CONNECT("ONE")

    #...

    def getname(self):
        return self.name
    def set_zero(self, node):
        self.zero = node

    def set_one(self, node):
        self.one = node


# Wandelt den Fehlerbaum in einen BDD um
def convert_to_bdd(node):
    if isinstance(node, EVENT):
        return BDDEVENT(node.name)
    elif isinstance(node, ANDNODE) or isinstance(node, ORNODE):
        bdd_node = BDDNODE(node.name)
        bdd_node.set_zero(convert_to_bdd(node.nodes[0]))
        bdd_node.set_one(convert_to_bdd(node.nodes[1]))
        return bdd_node

# Baut den BDD-Graphen auf
def build_bdd_graph(bdd_node, graph):
    if isinstance(bdd_node, BDDEVENT):
        graph.node(bdd_node.name, shape="box")
    else:
        graph.node(bdd_node.name, shape="circle")
        build_bdd_graph(bdd_node.zero, graph)
        build_bdd_graph(bdd_node.one, graph)
        graph.edge(bdd_node.name, bdd_node.zero.name, label="0")
        graph.edge(bdd_node.name, bdd_node.one.name, label="1")

# Beispielbaum erzeugen
Beispielbaum()

# Fehlerbaum darstellen
graph1 = graphviz.Digraph()
TOP.print(graph1)
graph1.render('fehlerbaum', format='png', view=True)

# Fehlerbaum in BDD umwandeln
bdd = convert_to_bdd(TOP)

# BDD darstellen
graph2 = graphviz.Digraph()
build_bdd_graph(bdd, graph2)
graph2.render('bdd', format='png', view=True)
