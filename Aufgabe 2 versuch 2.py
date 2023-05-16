import graphviz
import os
os.environ["PATH"] += os.pathsep + 'C:/Users/fabio/anaconda3/Library/bin/graphviz'

class BLOCK:
	def __init__(self,name, reliability):

		self.name = name
		self.reliability = reliability

	def printname(self):
		print(self.name)
	def getname(self):
		return self.name
	def rel(self):
		
		#...
		return reliability
	
	def draw(self, graph):
		graph.node(self.name, label=self.name)

	def print(self):
		

		for block in self.blocks:
			block.draw(graph)


	
class SEQBLOCK:
	def __init__(self,name):
		self.blocks = []

		self.name = name

	def append(self,node):
		self.blocks.append(node)
		return

	def printname(self):
		print(self.name)
	def getname(self):
		return self.name
	def rel(self):
		reliability = 1.0
		for block in self.blocks:
			reliability *= block.rel()
		return reliability

	def draw(self, graph):
		with graph.subgraph(name='cluster_' + self.name) as c:
			c.attr(style='dashed')
			c.node(self.name, shape='box', label=self.name)
			for block in self.blocks:
				block.draw(c)

	def print(self):
		

		for block in self.blocks:
			block.draw(graph)

	
class PARBLOCK:
	def __init__(self,name):
		self.blocks = []

		self.name = name

	def append(self,node):
		self.blocks.append(node)
		return

	def printname(self):
		print(self.name)
	def getname(self):
		return self.name
	def rel(self):
		availability = 1.0
		for block in self.blocks:
			availability *= (1 - block.rel())
		return 1.0-availability
	
	def draw(self, graph):
		with graph.subgraph(name='cluster_' + self.name) as c:
			c.node(self.name, shape='box', label=self.name)
			for block in self.blocks:
				block.draw(c)

	def print(self):
		

		for block in self.blocks:
			block.draw(graph)

		





# Erstellen der Block-Instanzen
block_A = BLOCK("A", 0.95)
block_R1 = BLOCK("R1", 0.90)
block_R2 = BLOCK("R2", 0.85)
block_E = BLOCK("E", 0.98)

# Erstellen der Container-Instanzen
seq_block = SEQBLOCK("seq")
par_block = PARBLOCK("par")

# Verknüpfen der Blöcke zu SEQBLOCK
par_block.append(block_R1)
par_block.append(block_R2)

# Verknüpfen von SEQBLOCK und PARBLOCK zu PARBLOCK
seq_block.append(par_block)
seq_block.append(block_A)
seq_block.append(block_E)

graph = graphviz.Digraph(format='jpg')
# Aufrufen der print() Methode, um das Zuverlässigkeitsdiagramm zu erzeugen
par_block.print()

graph.render(filename='reliability_diagram', directory='.', cleanup=True, format='jpg', view=True)

##Option1:

## Ausgabe des Zuverlässigkeitsdiagramms
#par_block.printname()  # Gibt "par" aus
#for block in par_block.blocks:
#    if isinstance(block, SEQBLOCK):
#        block.printname()  # Gibt "seq" aus
#        for seq_block_block in block.blocks:
#            seq_block_block.printname()  # Gibt "R1", "E" und "R2" aus
#    else:
#        block.printname()  # Gibt "A" aus
#
## Option2:
#
## Berechnung der Systemzuverlässigkeit
#system_reliability = par_block.rel()
#
## Ausgabe der Systemzuverlässigkeit
#print("Systemzuverlässigkeit:", system_reliability)