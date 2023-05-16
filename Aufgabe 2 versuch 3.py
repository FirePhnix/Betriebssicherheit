import os
from graphviz import Digraph
os.environ["PATH"] += os.pathsep + 'C:/Users/fabio/anaconda3/Library/bin/graphviz'

class BLOCK:
    def __init__(self, name, reliability):
        self.name = name
        self.reliability = reliability

    def printname(self):
        print(self.name)

    def getname(self):
        return self.name

    def rel(self):
        # ...
        reliability = self.reliability
        return reliability
    
    def print(self, graph):
        graph.node(self.name)

class SEQBLOCK:
    def __init__(self, name):
        self.blocks = []
        self.name = name

    def append(self, node):
        self.blocks.append(node)
        return

    def printname(self):
        print(self.name)

    def getname(self):
        return self.name

    def rel(self):
        reliability = 1.0
        # ...
        reliability = 1.0
        for block in self.blocks:
            reliability *= block.rel()
        return reliability
    
    def print(self, graph):
        with graph.subgraph() as s:
            s.attr(rank='same')
            for block in self.blocks:
                block.print(graph)
                s.node(block.name)

            s.attr(rank='min')
            s.node(self.name, shape='none')

            for block in self.blocks:
                graph.edge(block.name, self.name)

class PARBLOCK:
    def __init__(self, name):
        self.blocks = []
        self.name = name

    def append(self, node):
        self.blocks.append(node)
        return

    def printname(self):
        print(self.name)

    def getname(self):
        return self.name

    def rel(self):
        availability = 1.0
        # ...
        for block in self.blocks:
            availability *= (1 - block.rel())
        return 1.0 - availability
    
    def print(self, graph):
        graph.node(self.name, shape='doublecircle')
        with graph.subgraph() as s:
            s.attr(rank='same')
            for block in self.blocks:
                block.print(graph)
                s.node(block.name)

        for block in self.blocks:
            graph.edge(block.name, self.name)
        


E = BLOCK('Eingang', 0.99)
R1 = BLOCK('Rechner1', 0.99)
R2 = BLOCK('Rechner2', 0.99)
A = BLOCK('Ausgang', 0.99)

seq = SEQBLOCK("Alle")
par = PARBLOCK("Alle_Rechner")

par.append(R1)
par.append(R2)

seq.append(E)
seq.append(par)
seq.append(A)

def print_reliability_diagram(system):
    graph = Digraph('G', format='jpg')
    system.print(graph)
    graph.render('reliability_diagram', format='jpg', view=True)

system_reliability = seq.rel()
print("Systemzuverlässigkeit:", system_reliability)

print_reliability_diagram(seq)