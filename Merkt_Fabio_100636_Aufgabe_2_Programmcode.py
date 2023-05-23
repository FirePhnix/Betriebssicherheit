import os
import graphviz

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
        return self.reliability

    def render(self, dot):
        dot.node(self.name, label=self.name)
        
class SEQBLOCK:
    def __init__(self, name):
        self.blocks = []
        self.name = name

    def append(self, node):
        self.blocks.append(node)

    def printname(self):
        print(self.name)

    def getname(self):
        return self.name

    def rel(self):
        reliability = 1.0
        for block in self.blocks:
            reliability *= block.rel()
        return reliability

    def render(self, dot):
        dot.attr(rankdir='LR')
        with dot.subgraph(name='cluster_seq') as sg:
            sg.attr(label=self.name)
            
            for block in self.blocks:
                block.render(sg)
                seq_list.append(block.getname())

class PARBLOCK:
    def __init__(self, name):
        self.blocks = []
        self.name = name

    def append(self, node):
        self.blocks.append(node)

    def printname(self):
        print(self.name)

    def getname(self):
        return self.name

    def rel(self):
        availability = 1.0
        for block in self.blocks:
            availability *= (1.0 - block.rel())
        return 1.0 - availability

    def render(self, dot):
        with dot.subgraph(name='cluster_par') as sg:
            sg.attr(label=self.name)
            
            for block in self.blocks:
                block.render(sg)
                par_list.append(block.getname())

class ZuverlaessigkeitsDiagramm:
    def __init__(self, root):
        self.root = root

    def print(self):
        dot = graphviz.Digraph(comment='Reliability Diagram')
        self.root.render(dot)

        input_name = "Eingang"
        output_name = "Ausgang"

        for block in par_list:
            dot.edge(input_name, block)
            dot.edge(block, output_name)

        dot.format = 'png'
        dot.render('reliability_diagram', view=True)

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

par_list = []
seq_list = []

system_reliability = seq.rel()
print("Zuverlässigkeit des Systems:", system_reliability)

zuverlaessigkeitsdiagramm = ZuverlaessigkeitsDiagramm(seq)
zuverlaessigkeitsdiagramm.print()
