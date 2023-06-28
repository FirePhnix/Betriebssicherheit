import os
import graphviz
os.environ["PATH"] += os.pathsep + 'C:/Users/fabio/anaconda3/Library/bin/graphviz'

# And-Verknüpfungselement
class ANDNODE:
    def __init__(self, name):
        self.name = name
        self.nodes = []
    
    def add(self, node):
        self.nodes.append(node)
    
    def print(self, graph):
        # Hintergrund für And-Node erstellen
        graph.node(self.name, shape='rect', style='filled', fillcolor='lightgray')
        # Knoten innerhalb der And-Node platzieren
        for node in self.nodes:
            node.print(graph)
            # Verbindung vom 0-Ausgang zum aktuellen Knoten
            graph.edge('0', node.name, label='0')
            # Verbindung vom 1-Ausgang zum 1-Endblock
            graph.edge(node.name, '1')
    
    def topdown(self):
        # ...
        pass


# Oder-Verknüpfungselement
class ORNODE:
    def __init__(self, name):
        self.name = name
        self.nodes = []
    
    def add(self, node):
        self.nodes.append(node)
    
    def print(self, graph):
        # Hintergrund für Or-Node erstellen
        graph.node(self.name, shape='rect', style='filled', fillcolor='lightgray')
        # Knoten innerhalb der Or-Node platzieren
        for node in self.nodes:
            node.print(graph)
            # Verbindung vom 0-Ausgang zum nächsten Knoten
            graph.edge('0', node.name, label='0')
            # Verbindung vom 1-Ausgang zum 1-Endblock
            graph.edge(node.name, '1')
    
    def topdown(self):
        # ...
        pass


# Eingangsknoten
class EVENT:
    def __init__(self, name):
        self.name = name
    
    def print(self, graph):
        # Den Event-Knoten als Kreis darstellen
        graph.node(self.name)
    
    def topdown(self):
        # ...
        pass


class BDDEVENT:
    def __init__(self, name):
        self.name = name
        self.zero = None
        self.one = None
    
    def set_zero(self, node):
        self.zero = node
    
    def set_one(self, node):
        self.one = node
    
    def print(self, graph):
        # Knoten als rechteckige Box darstellen
        graph.node(self.name, shape='box', label='E{}'.format(self.name))
        if self.zero:
            # Kante vom aktuellen Knoten zum Ausgang "0"
            graph.edge(self.name, self.zero.name, label='0', tailport='s', headport='n')
            if not isinstance(self.zero, EVENT):
                self.zero.print(graph)
        if self.one:
            # Kante vom aktuellen Knoten zum Ausgang "1"
            graph.edge(self.name, self.one.name, label='1', tailport='s', headport='n')
            if not isinstance(self.one, EVENT):
                self.one.print(graph)
    
    def topdown(self):
        # ...
        pass


# Funktion zum Umwandeln des Fehlerbaums in ein BDD
def convert_to_bdd(node):
    if isinstance(node, EVENT):
        # BDDEVENT für das Event erstellen und zurückgeben
        return BDDEVENT(node.name)
    elif isinstance(node, ANDNODE):
        # Rekursiv die Unterlemente in BDDEVENTs umwandeln
        zero_node = convert_to_bdd(node.nodes[0])
        one_node = convert_to_bdd(node.nodes[1])
        
        # BDDEVENT für das AND-Gatter erstellen
        bdd_node = BDDEVENT(node.name)
        
        # Verbindungen herstellen
        bdd_node.set_zero(zero_node)
        bdd_node.set_one(one_node)
        
        return bdd_node
    elif isinstance(node, ORNODE):
        # Rekursiv die Unterlemente in BDDEVENTs umwandeln
        zero_node = convert_to_bdd(node.nodes[0])
        one_node = convert_to_bdd(node.nodes[1])
        
        # BDDEVENT für das OR-Gatter erstellen
        bdd_node = BDDEVENT(node.name)
        
        # Verbindungen herstellen
        bdd_node.set_zero(zero_node)
        bdd_node.set_one(one_node)
        
        return bdd_node


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


# Digraph für den BDD erstellen
bdd_graph = graphviz.Digraph()

# BDD graphisch darstellen
TOP.print(bdd_graph)

# Quadratische Endblöcke hinzufügen
# Quadratische Endblöcke hinzufügen
bdd_graph.node('0', shape='square', pos='0,-1!')
bdd_graph.node('1', shape='box', label='E1', pos='1,-2!')
bdd_graph.edge('1', '0', label='0', tailport='s', headport='n', weight='10')


# Die Ausgabe der Graphviz-Datei anzeigen
print(bdd_graph.source)
bdd_graph.render('bdd_graph', format='png', view=True)


# BDD erstellen
bdd_top = convert_to_bdd(TOP)
bdd_top.print(bdd_graph)
print(bdd_graph.source)
bdd_graph.render('bdd_graph', format='png', view=True)
