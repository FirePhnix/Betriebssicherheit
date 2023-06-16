#Import und Path initialisieren
import os
import graphviz
os.environ["PATH"] += os.pathsep + 'C:/Users/fabio/anaconda3/Library/bin/graphviz'

#Klassen

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
    
    def create_bdd(self, bdd):
        bdd_node = BDDEVENT(self.name)
        bdd.zero = self.nodes[0].create_bdd(bdd.zero)
        bdd.one = self.nodes[1].create_bdd(bdd.one)
        return bdd_node



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
            # weil es OR ist wird nur ein Unterknoten pro weg benötigt also muss die liste erst geleert werden
            del mat[0]
            anzahl_and = 0
            for i in range(len(self.nodes)):
                if type(self.nodes[i]) == ANDNODE:
                    anzahl_and += 1
            #Wenn nicht alle Unterknoten ANDNODEs sind
            if anzahl_and < len(self.nodes):    
                for i in range(len(self.nodes)):
                    # alle ausser & Unterknoten an mat anhängen
                    if type(self.nodes[i]) != ANDNODE:
                        mat.append([self.nodes[i]])
            else:
                for i in range(len(self.nodes)):
                    # alle Unterknoten an mat anhängen
                    mat.append([self.nodes[i]])
            i=0
            while i < len(mat):
                mat_node = False
                for i in range(len(mat)):
                    for j in range(len(mat[i])):
                        # Wenn der Unterknoten kein event ist
                        if type(mat[i][j]) != EVENT:
                            # rufe die topdown funktion des Unterknotens auf und speichere den rückgabewer
                            mat = mat[i][j].topdown(mat)
                            mat_node = True
                            break
                    # Wenn alle Knoten Events waren stoppe die while schleife
                    if i == len(mat)-1:
                        i += 1
                    if mat_node:
                        break    
        else:
            mat_node=False
            for i in range(len(mat)):
                for j in range(len(mat[i])):
                    if mat[i][j].name == self.name:
                        # Kopiere die liste von mat an der Stelle i
                        mat_kopie = mat[i]
                        # Wegen OR muss die Zeile für jeden unterknoten erstellt werden deshalb wird die alte Zeile entfernt
                        del mat[i]

                        anzahl_and = 0
                        for k in range(len(self.nodes)):
                            if type(self.nodes[k]) == ANDNODE:
                                anzahl_and += 1
                        #Wenn nicht alle Unterknoten ANDNODEs sind
                        if anzahl_and < len(self.nodes):    
                            for node in self.nodes:
                                # alle ausser & Unterknoten an mat anhängen
                                if type(node) != ANDNODE:
                                    # an der Stelle j war die ORNODE, diese ersetzen wir jetzt mit dem Unterknoten
                                    mat_kopie[j] = node
                                    mat.append(list(mat_kopie))
                            mat_node = True
                            break
                        #Wenn alle Unterknoten ANDNODEs sind
                        else:
                            for node in self.nodes:
                                # an der Stelle j war die ORNODE, diese ersetzen wir jetzt mit dem Unterknoten
                                mat_kopie[j] = node
                                mat.append(list(mat_kopie))

                            mat_node = True
                            break
                if mat_node:
                    break
        return mat
    
    def create_bdd(self, bdd):
        bdd_node = BDDEVENT(self.name)
        bdd.zero = self.nodes[0].create_bdd(bdd.zero)
        bdd.one = self.nodes[1].create_bdd(bdd.one)
        return bdd_node

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
    
    def create_bdd(self, bdd):
        bdd_node = BDDEVENT(self.name)
        bdd.zero = self.zero.create_bdd(bdd.zero)
        bdd.one = self.one.create_bdd(bdd.one)
        return bdd_node


class CONNECT:
    def __init__(self,name):
        self.name = name
        self.con = None
    #...
    def getname(self):
        return self.name

class NODE:
    def __init__(self,name):
        self.name = name

        self.zero = CONNECT("ZERO")
        self.one = CONNECT("ONE")

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
            self.create_and(ntop, ft)
        elif isinstance(ft, ORNODE):
            self.create_or(ntop, ft)
        else:
            None

        return ntop

    def create_and(self, ntop, ft):
        bdd_node = BDDEVENT(ft.name)
        ntop.zero = CONNECT(ft.name + "_ZERO")
        ntop.one = CONNECT(ft.name + "_ONE")
        self.dot.node(ntop.zero.getname(), label="0", shape="rectangle")
        self.dot.node(ntop.one.getname(), label="1", shape="rectangle")
        self.dot.edge(ntop.getname(), ntop.zero.getname(), label="0")
        self.dot.edge(ntop.getname(), ntop.one.getname(), label="1")
        self.create(ntop.zero, ft.nodes[0])
        self.create(ntop.one, ft.nodes[1])

    def create_or(self, ntop, ft):
        bdd_node = BDDEVENT(ft.name)
        ntop.zero = CONNECT(ft.name + "_ZERO")
        ntop.one = CONNECT(ft.name + "_ONE")
        self.dot.node(ntop.zero.getname(), label="0", shape="rectangle")
        self.dot.node(ntop.one.getname(), label="1", shape="rectangle")
        self.dot.edge(ntop.getname(), ntop.zero.getname(), label="0")
        self.dot.edge(ntop.getname(), ntop.one.getname(), label="1")
        self.create(ntop.zero, ft.nodes[0])
        self.create(ntop.one, ft.nodes[1])



TOP = ANDNODE('TOP')
A = ORNODE('A')

E1 = EVENT('E1')
E2 = EVENT('E2')
E3 = EVENT('E3')

A.add(E1)
A.add(E3)

TOP.add(E1)
TOP.add(A)

ft2bdd = FT2BDD()
root = ft2bdd.create(None, TOP)
dot = ft2bdd.show()
dot.render("bdd_graph", format="jpeg", view=True)

# #Fehlerbaum Bild 1

# TTOP = ANDNODE('TOP')
# A = ORNODE('A')
# E1 = EVENT('1')
# E2 = EVENT('2')
# E3 = EVENT('3')

# TOP.add(A)
# TOP.add(E1)
# A.add(E2)
# A.add(E3)
 
# # Digraph funktion als "Graph" importieren
# Graph = graphviz.Digraph()

# # print funktion des TOP Knoten ausführen
# TOP.print(Graph)

# # den Fehlerbaum rendern 
# Graph.render('fehlerbaum', format='jpg', view=True)

# mat = [[TOP]]
# mat = TOP.topdown(mat)

# #mat durchlaufen und alle instanzen durch ihre namen ersetzen
# for i in range(len(mat)):
#     for j in range(len(mat[i])):
#         mat[i][j] = mat[i][j].name
# print(mat)    