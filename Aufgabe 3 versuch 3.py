import os
import graphviz
os.environ["PATH"] += os.pathsep + 'C:/Users/fabio/anaconda3/Library/bin/graphviz'

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
            exit
        
        return ntop
    
    def create_and(self, node, ft):
        if node.zero.con is None:
            node.zero.con = self.create(node.zero.con, ft.nodes[0])
        if node.one.con is None:
            node.one.con = self.create(node.one.con, ft.nodes[1])
        
        self.dot.node(node.getname(), label=node.getname(), shape='circle')
        self.dot.node(node.zero.con.getname(), label=node.zero.con.getname(), shape='circle')
        self.dot.node(node.one.con.getname(), label=node.one.con.getname(), shape='circle')
        
        self.dot.edge(node.getname(), node.zero.con.getname(), label='0')
        self.dot.edge(node.getname(), node.one.con.getname(), label='1')

    def create_or(self, node, ft):
        if node.zero.con is None:
            node.zero.con = self.create(node.zero.con, ft.nodes[0])
        if node.one.con is None:
            node.one.con = self.create(node.one.con, ft.nodes[1])
        
        self.dot.node(node.getname(), label=node.getname(), shape='circle')
        self.dot.node(node.zero.con.getname(), label=node.zero.con.getname(), shape='circle')
        self.dot.node(node.one.con.getname(), label=node.one.con.getname(), shape='circle')
        
        self.dot.edge(node.getname(), node.zero.con.getname(), label='0')
        self.dot.edge(node.getname(), node.one.con.getname(), label='1')

# Fehlerbaum-Instanzen erstellen (vorheriger Code)
class ANDNODE:
    def __init__(self, name):
        self.name = name
        self.nodes = []
    
    def add(self, node):
        self.nodes.append(node)

    def getname(self):
        return self.name

class ORNODE:
    def __init__(self, name):
        self.name = name
        self.nodes = []
    
    def add(self, node):
        self.nodes.append(node)

    def getname(self):
        return self.name

class EVENT:
    def __init__(self, name, prob, value):
        self.name = name
        self.prob = prob
        self.value = value
    
    def getname(self):
        return self.name

TOP = ANDNODE('TOP')
A = ORNODE('A')

E1 = EVENT('E1', 1/1000, 1/4)
E2 = EVENT('E2', 1/1000, 1/4)
E3 = EVENT('E3', 1/1000, 1/4)

A.add(E1)
A.add(E3)

TOP.add(E1)
TOP.add(A)

# BDD erstellen
ft2bdd = FT2BDD()
bdd_root = ft2bdd.create(None, TOP)

# BDD graphisch darstellen
dot = ft2bdd.show()
#dot.format = 'png'
dot.render('bdd_graph', format='png', view=True)
