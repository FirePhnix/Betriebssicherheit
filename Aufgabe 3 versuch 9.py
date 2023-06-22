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

class BDDEVENT:
    def __init__(self, name):
        self.name = name
        self.zero = None
        self.one = None
    
    def set_zero(self, event):
        self.zero = event
    
    def set_one(self, event):
        self.one = event
    
    def print(self, Graph):
        # Knoten als Kreis darstellen
        Graph.node(self.name, shape='circle')
        if self.zero:
            # Kante vom aktuellen Knoten zum Ausgang "0"
            Graph.edge(self.name, self.zero.name, label='0')
            self.zero.print(Graph)
        if self.one:
            # Kante vom aktuellen Knoten zum Ausgang "1"
            Graph.edge(self.name, self.one.name, label='1')
            self.one.print(Graph)
    
    def topdown(self):
        return self


# Funktion zum Umwandeln des Fehlerbaums in ein BDD
def convert_to_bdd(node):
    if isinstance(node, EVENT):
        # BDDEVENT für das Event erstellen und zurückgeben
        return BDDEVENT(node.name)
    elif isinstance(node, ANDNODE):
        # BDDEVENT für das AND-Gatter erstellen
        bdd_event = BDDEVENT(node.name)
        
        # Rekursiv die Unterlemente in BDDEVENTs umwandeln
        zero_event = convert_to_bdd(node.nodes[0])
        one_event = convert_to_bdd(node.nodes[1])
        
        # Verbindungen herstellen
        bdd_event.set_zero(zero_event)
        bdd_event.set_one(one_event)
        
        return bdd_event
    elif isinstance(node, ORNODE):
        # BDDEVENT für das OR-Gatter erstellen
        bdd_event = BDDEVENT(node.name)
        
        # Rekursiv die Unterlemente in BDDEVENTs umwandeln
        zero_event = convert_to_bdd(node.nodes[0])
        one_event = convert_to_bdd(node.nodes[1])
        
        # Verbindungen herstellen
        bdd_event.set_zero(zero_event)
        bdd_event.set_one(one_event)
        
        return bdd_event


# Fehlerbaum erstellen (Beispiel)
TOP = ANDNODE('TOP')
A = ORNODE('A')
E1 = EVENT('1')
E2 = EVENT('2')
E3 = EVENT('3')

TOP.add(A)
TOP.add(E1)
A.add(E2)
A.add(E3)

# Fehlerbaum in ein BDD umwandeln
bdd_root = convert_to_bdd(TOP)

# Digraph für den BDD erstellen
bdd_graph = graphviz.Digraph()

# BDD graphisch darstellen
bdd_root.print(bdd_graph)

# Die Ausgabe der Graphviz-Datei anzeigen
print(bdd_graph.source)
bdd_graph.render('bdd_graph', format='png', view=True)
