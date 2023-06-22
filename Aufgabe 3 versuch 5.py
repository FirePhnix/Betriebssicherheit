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

    def show(self):
        dot = graphviz.Digraph()
        self._show(dot, self.nroot)
        return dot

    def _show(self, dot, node):
        if isinstance(node, BDDEVENT):
            dot.node(node.getname())
        elif isinstance(node, NODE):
            dot.node(node.getname(), label=node.getname() + ' (>=1)', shape='rectangle')
            dot.edge(node.getname(), node.zero.con.getname(), label='0')
            dot.edge(node.getname(), node.one.con.getname(), label='1')
            self._show(dot, node.zero.con)
            self._show(dot, node.one.con)

    def create(self, ft):
        top = NODE("root")
        self.nroot = top
        self._create(top, ft)
        return top

    def _create(self, node, ft):
        if isinstance(ft, ANDNODE):
            self._createand(node, ft)
        elif isinstance(ft, ORNODE):
            self._createor(node, ft)

    def _createand(self, node, ft):
        left = ft.nodes[0]
        right = ft.nodes[1]

        left_node = NODE(left.name)
        right_node = NODE(right.name)
        node.zero.con = left_node
        node.one.con = right_node

        if isinstance(left, ANDNODE):
            self._createand(left_node, left)
        elif isinstance(left, ORNODE):
            left_event = BDDEVENT(left.nodes[0].name)
            left_event.zero = left.zero
            left_event.one = left.one
            left_node.zero.con = left_event
            self._create(left_node, left)
        elif isinstance(left, EVENT):
            event = BDDEVENT(left.name)
            left_node.zero.con = event

        if isinstance(right, ANDNODE):
            self._createand(right_node, right)
        elif isinstance(right, ORNODE):
            right_event = BDDEVENT(right.nodes[0].name)
            right_event.zero = right.zero
            right_event.one = right.one
            right_node.zero.con = right_event
            self._create(right_node, right)
        elif isinstance(right, EVENT):
            event = BDDEVENT(right.name)
            right_node.zero.con = event

    def _createor(self, node, ft):
        left = ft.nodes[0]
        right = ft.nodes[1]

        left_node = NODE(left.name)
        right_node = NODE(right.name)
        left_event = BDDEVENT(left.nodes[0].name)
        right_event = BDDEVENT(right.nodes[0].name)

        node.zero.con = left_node
        node.one.con = right_node
        left_node.zero.con = left_event
        right_node.zero.con = right_event

        self._create(left_node, left)
        self._create(right_node, right)

        if isinstance(left, ANDNODE):
            left_node = NODE(left.name)
            left_event = BDDEVENT(left.nodes[0].name)
            left_event.zero = left.zero
            left_event.one = left.one
            node.zero.con = left_node
            left_node.zero.con = left_event
            self._create(left_node, left)
        elif isinstance(left, ORNODE):
            left_node = NODE(left.name)
            left_event = BDDEVENT(left.nodes[0].name)
            left_event.zero = left.zero
            left_event.one = left.one
            node.zero.con = left_node
            left_node.zero.con = left_event
            self._create(left_node, left)
        elif isinstance(left, EVENT):
            event = BDDEVENT(left.name)
            node.zero.con = event

        if isinstance(right, ANDNODE):
            right_node = NODE(right.name)
            right_event = BDDEVENT(right.nodes[0].name)
            right_event.zero = right.zero
            right_event.one = right.one
            node.one.con = right_node
            right_node.zero.con = right_event
            self._create(right_node, right)
        elif isinstance(right, ORNODE):
            right_node = NODE(right.name)
            right_event = BDDEVENT(right.nodes[0].name)
            right_event.zero = right.zero
            right_event.one = right.one
            node.one.con = right_node
            right_node.zero.con = right_event
            self._create(right_node, right)
        elif isinstance(right, EVENT):
            event = BDDEVENT(right.name)
            node.one.con = event





#Fehlerbaum Bild 1

TOP = ANDNODE('TOP')
A = ORNODE('A')
E1 = EVENT('1')
E2 = EVENT('2')
E3 = EVENT('3')

TOP.add(A)
TOP.add(E1)
A.add(E2)
A.add(E3)
 
# Digraph funktion als "Graph" importieren
Graph = graphviz.Digraph()

# print funktion des TOP Knoten ausführen
TOP.print(Graph)

# den Fehlerbaum rendern 
Graph.render('fehlerbaum', format='jpg', view=True)

mat = [[TOP]]
mat = TOP.topdown(mat)

#mat durchlaufen und alle instanzen durch ihre namen ersetzen
for i in range(len(mat)):
    for j in range(len(mat[i])):
        mat[i][j] = mat[i][j].name
print(mat)  

# Erstellen Sie den Fehlerbaum (beispielsweise den aus Aufgabe 2)
# ft = ...

# Erstellen Sie ein FT2BDD-Objekt und rufen Sie die Methode create auf, um den BDD zu erstellen
converter = FT2BDD()
root_node = converter.create(mat)

# Rufen Sie die Methode show auf, um den BDD graphisch darzustellen
dot = converter.show()
dot.render('bdd_graph', format='png', view=True)
