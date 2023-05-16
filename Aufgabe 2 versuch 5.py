import os
from graphviz import Digraph

os.environ["PATH"] += os.pathsep + 'C:/Users/fabio/anaconda3/Library/bin/graphviz'

class BLOCK:
    def __init__(self, name, reliability):
        self.name = name
        self.reliability = reliability

    def rel(self):
        return self.reliability

class SEQBLOCK:
    def __init__(self, name):
        self.blocks = []
        self.name = name

    def append(self, node):
        self.blocks.append(node)

    def rel(self):
        reliability = 1.0
        for block in self.blocks:
            reliability *= block.rel()
        return reliability

class PARBLOCK:
    def __init__(self, name):
        self.blocks = []
        self.name = name

    def append(self, node):
        self.blocks.append(node)

    def rel(self):
        availability = 1.0
        for block in self.blocks:
            availability *= (1 - block.rel())
        return 1.0 - availability


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

def create_reliability_diagram(system):
    graph = Digraph('G', format='png', strict=True)
    graph.attr('node', shape='circle', fontsize='14', fontname='Arial')
    graph.attr('edge', fontsize='12', fontname='Arial')

    # Add blocks
    graph.node('E', 'Eingang', shape='doublecircle')
    graph.node('A', 'Ausgang', shape='doublecircle')
    graph.node('Alle', 'Alle', shape='rect')

    # Add block connections
    graph.edge('E', 'Alle')
    graph.edge('Alle', 'A')

    # Add parallel block
    graph.node('Alle_Rechner', 'Alle Rechner', shape='rect')
    graph.edge('Alle', 'Alle_Rechner')

    # Add subgraph for parallel blocks
    with graph.subgraph(name='cluster_parblocks') as parblocks:
        parblocks.attr(label='Alle Rechner', labeljust='l')
        parblocks.attr('node', shape='circle', fontsize='14', fontname='Arial')
        parblocks.attr('edge', fontsize='12', fontname='Arial')
        parblocks.attr('graph', style='dotted')

        parblocks.node('Rechner1', 'Rechner1')
        parblocks.node('Rechner2', 'Rechner2')

    # Add connections within the parallel block
    graph.edge('Rechner1', 'Rechner2')

    # Set system reliability label
    system_reliability = seq.rel()
    graph.attr(label=f'Systemzuverlässigkeit: {system_reliability:.4f}', labeljust='r')

    # Render and save the diagram
    graph.render('reliability_diagram', format='png', view=True)

create_reliability_diagram(seq)
