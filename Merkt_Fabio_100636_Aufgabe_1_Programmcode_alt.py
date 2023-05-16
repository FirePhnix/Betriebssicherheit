#Aufgabe a) mit Aufgabe c) für den output des Fehlerbaums für die Kontrollfrage

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

#Fehlerbaum Kontrollfrage

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

#Kontrollfrage:

#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡖⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⢒⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇     TOP (&)  ⢸⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀             ⠘⡀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠓⠒⠒⠒⡖⠒⠒⠲⡒⠒⠒⠚⠁⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠌⠀⠀⠀⠀⠐⡀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣎⠀⠀⠀⠀⠀⠀⠐⣄⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⡖⠒⠒⠒⠒⠒⠒⠒⠒⢒⠀⠀⠀ ⢀⠹⠆⠀⠠⠤⢀⠀⠀
#⠀⠀⠀⠀⠀⠀⡇⠀          ⠸⠀⠀⠀⠔⠀⠀⠀ ⠀⠀⠀⠑⡀
#⠀⠀⠀⠀⠀⠀⡇ A (>=1)   ⢘⠀⠀⠀⢆⠀⠀⠀ 1 ⠀⠀⢀⠃
#⠀⠀⠀⠀⠀⠀⠧⠤⠤⢤⠤⠤⠤⡤⠤⠬⠀⠀⠀⠀⠁⠂⠠⠤⠤⠀⠂⠁⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⢀⠂⠀⠀⠀⠐⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⣀⠂⠀⠀⠀⠀⠀⠘⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⣀⠀⠀⠰⡟⠁⠀⠀⠀⠀⠀⠀⢹⡇⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⢀⠔⠁⠀⠀ ⠀⠀⠁⢢⠀⠀⠀⡀⠈⠀⠀   ⠀⠈⠀⡀⠀⠀⠀⠀⠀⠀⠀
#⠸⡀⠀⠀  2⠀⠀⠀⢠⠀⠀⠀⠅⠀⠀⠀ 3 ⠀⠀⠀⠇⠀⠀⠀⠀⠀⠀⠀
#⠀⠈⠂⠄⠀⠀⠀⠤⠐⠁⠀⠀⠀⠈⠐⠠⠀⠀⠀⠠⠐⠈⠀⠀⠀⠀⠀⠀⠀⠀

#Aufgabenblatt1 Aufgaben a-c

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

#Fehlerbaum Bild 1

TOP = ANDNODE('TOP')
D = ANDNODE('D')
A = ORNODE('A')
B = ORNODE('B')
E1 = EVENT('1')
E2 = EVENT('2')
E3 = EVENT('3')
E4 = EVENT('4')
E5 = EVENT('5')

TOP.add(A)
TOP.add(B)
A.add(E1)
A.add(E2)
B.add(D)
B.add(E5)
D.add(E3)
D.add(E4)
 
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