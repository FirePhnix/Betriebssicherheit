import os
import graphviz
os.environ["PATH"] += os.pathsep + 'C:/Users/fabio/anaconda3/Library/bin/graphviz'

class CONNECT:
    def __init__(self, name):
        self.name = name
        self.con = None
        self.zero = None
        self.one = None
    
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
        self.generate_dot(self.nroot, dot)
        return dot
    
    def generate_dot(self, node, dot):
        if node is None:
            return

        dot.node(node.getname())

        if node.zero and node.zero.con:
            if node.zero.con.getname() == "Stub0":
                dot.node("Stub0", shape="square")
                dot.edge(node.getname(), "Stub0", label="0")
            else:
                dot.edge(node.getname(), node.zero.con.getname(), label="0")
                self.generate_dot(node.zero.con, dot)

        if node.one and node.one.con:
            if node.one.con.getname() == "Stub1":
                dot.node("Stub1", shape="square")
                dot.edge(node.getname(), "Stub1", label="1")
            else:
                dot.edge(node.getname(), node.one.con.getname(), label="1")
                self.generate_dot(node.one.con, dot)
        
    
    def create(self, ntop, ft):
        if ntop is None:
            ntop = NODE("root")
        
        if self.nroot is None:
            self.nroot = ntop
        
        if isinstance(ft, ANDNODE):
            self.createand(ntop, ft)
        elif isinstance(ft, ORNODE):
            self.createor(ntop, ft)
        
        return ntop
    
    def createand(self, node, ft):
        zero_con = CONNECT("ZERO")
        one_con = CONNECT("ONE")
        
        self.create(node.zero.con, ft.inputs[0])
        self.create(node.one.con, ft.inputs[1])
        
        node.zero.con = zero_con
        node.one.con = one_con
    
    def createor(self, node, ft):
        zero_con = NODE("Stub0")
        one_con = NODE("Stub1")
        
        self.create(node.zero.con, ft.inputs[0])
        self.create(node.one.con, ft.inputs[1])
        
        node.zero.con = zero_con
        node.one.con = one_con

# Beispiel-Fehlerbaum
class ANDNODE:
    def __init__(self, name):
        self.name = name
        self.inputs = []
    
    def add(self, event):
        self.inputs.append(event)

class ORNODE:
    def __init__(self, name):
        self.name = name
        self.inputs = []
    
    def add(self, event):
        self.inputs.append(event)

class EVENT:
    def __init__(self, name):
        self.name = name

TOP = ORNODE("1")

A = ANDNODE("2")
E1 = EVENT("3")
E2 = EVENT("4")
E3 = EVENT("5")

TOP.add(A)
TOP.add(E1)
A.add(E2)
A.add(E3)

# BDD erstellen
converter = FT2BDD()
root_node = converter.create(None, TOP)

# Graph erstellen und anzeigen
dot = converter.show()
dot.format = 'png'
dot.render('bdd_graph', view=True)
