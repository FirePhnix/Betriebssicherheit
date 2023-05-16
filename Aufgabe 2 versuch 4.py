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
        graph.node(self.name, shape='box', label=self.name, style='rounded,filled', color='#dddddd', fontcolor='black', fontsize='10')

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
            s.node("seq", shape='none')
            for block in self.blocks:
                with s.subgraph() as b:
                    b.attr(rank='same')
                    block.print(b)
                    b.node(block.name, shape='square', width='1.5', height='1.5', fixedsize='true', style='rounded,filled', color='#dddddd', fontcolor='black', fontsize='10')
            s.node("par", shape='none')



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
        with graph.subgraph() as s:
            s.attr(rank='same')
            s.node("par", shape='none')
            for block in self.blocks:
                with s.subgraph() as b:
                    b.attr(rank='same')
                    block.print(b)
                    b.node(block.name, shape='square', width='1.5', height='1.5')
            s.node("seq", shape='none')

        graph.edge("par", self.blocks[0].name, style='invis')
        graph.edge(self.blocks[-1].name, "seq", style='invis')

        


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
    graph = Digraph('G', format='png')
    graph.attr(rankdir='LR', margin='0.2', pad='0.2')
    
    # Set node styles
    graph.attr('node', shape='box', width='1.5', height='0.8', fixedsize='true', style='rounded,filled', color='#f4f4f4', fontcolor='black', fontsize='10')
    graph.node("start", shape='none', width='0', height='0')
    graph.node("end", shape='none', width='0', height='0')

    # Set edge styles
    graph.attr('edge', arrowhead='none', style='setlinewidth(1.5)', penwidth='1.5', color='#808080')

    # Set graph attributes
    graph.attr('graph', bgcolor='#ffffff')

    system.print(graph)

    graph.edge("start", "seq", style='invis')
    graph.edge("par", "end", style='invis')

    graph.render('reliability_diagram', format='png', view=True)


system_reliability = seq.rel()
print("Systemzuverlässigkeit: -|{}|-".format(system_reliability))

print_reliability_diagram(seq)