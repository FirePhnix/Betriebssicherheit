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
        for block in self.blocks:
            reliability *= block.rel()
        return reliability


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
        for block in self.blocks:
            availability *= (1 - block.rel())
        return 1.0 - availability


# Erstellen der Blöcke
block1 = BLOCK("R1", 0.9)
block2 = BLOCK("R2", 0.8)
block3 = BLOCK("A", 0.95)
block4 = BLOCK("E", 0.85)

# Erstellen der SEQBLOCKs und Hinzufügen der Blöcke
seq1 = SEQBLOCK("seq1")
seq1.append(block1)
seq1.append(block2)

seq2 = SEQBLOCK("seq2")
seq2.append(block3)
seq2.append(block4)

# Erstellen des PARBLOCKs und Hinzufügen der SEQBLOCKs
par = PARBLOCK("par")
par.append(seq1)
par.append(seq2)

# Berechnung der Zuverlässigkeit des PARBLOCKs
reliability = par.rel()
print("Zuverlässigkeit:", reliability)

