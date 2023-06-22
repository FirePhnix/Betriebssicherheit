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
        # Knoten innerhalb des And-Node platzieren
        for node in self.nodes:
            node.print(graph)
    
        # Verbindungen erstellen
        for i, node in enumerate(self.nodes):
            # Verbindung vom aktuellen Knoten zum nächsten Knoten oder zu 1
            next_node = self.nodes[i + 1] if i + 1 < len(self.nodes) else '1'
            graph.edge(node.name, next_node, label='1')
    
        # Verbindung vom And-Node zum 0-Endblock
        for node in self.nodes:
            graph.edge(self.name, node.name, label='0')
    
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
        # Knoten innerhalb des Or-Node platzieren
        for node in self.nodes:
            node.print(graph)
        # Verbindungen erstellen
        for node in self.nodes:
            # Verbindung vom Or-Node zum aktuellen Knoten
            graph.edge(self.name, node.name, label='0')
        # Verbindung vom Or-Node zum 1-Endblock
        graph.edge(self.name, '1')
    
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
        # Knoten als Kreis darstellen
        graph.node(self.name, shape='circle')
        if self.zero:
            # Kante vom aktuellen Knoten zum Ausgang "0"
            graph.edge(self.zero, self.name, label='0')
            if not isinstance(self.zero, EVENT):
                self.zero.print(graph)
        if self.one:
            # Kante vom aktuellen Knoten zum Ausgang "1"
            graph.edge(self.one, self.name, label='1')
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
E1 = EVENT('1')
E2 = EVENT('2')
E3 = EVENT('3')

A = ANDNODE('A')
A.add(E2)
A.add(E3)

OR = ORNODE('OR')
OR.add(A)
OR.add(E1)


# Digraph für den BDD erstellen
bdd_graph = graphviz.Digraph()

# BDD graphisch darstellen
OR.print(bdd_graph)

# Endblöcke hinzufügen
bdd_graph.node('0', shape='square')
bdd_graph.node('1', shape='square')

# Die Ausgabe der Graphviz-Datei anzeigen
print(bdd_graph.source)
bdd_graph.render('bdd_graph', format='png', view=True)


# BDD erstellen
bdd_root = convert_to_bdd(OR)
bdd_root.print(bdd_graph)
print(bdd_graph.source)
bdd_graph.render('bdd_graph', format='png', view=True)
