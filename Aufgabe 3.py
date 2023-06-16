TOP = ANDNODE('TOP')
A = ORNODE('A')

E1 = EVENT('E1', 1/1000, 1/4)
E2 = EVENT('E2', 1/1000, 1/4)
E3 = EVENT('E3', 1/1000, 1/4)

A.add(E1)
A.add(E3)

TOP.add(E1)
TOP.add(A)




class CONNECT:
    def __init__(self,name):
        self.name = name
        self.con = None
    #...
    def getname(self):
        return self.name
    

class NODE:
    def __init__(self,name):
        self.name = name

        self.zero = CONNECT("ZERO")
        self.one = CONNECT("ONE")

    #...

    def getname(self):
        return self.name
    

class BDDEVENT:
    def __init__(self,name):
        self.name = name
        self.zero = None
        self.one = None

    #...

    def getname(self):
        return self.name


class FT2BDD:
    def __init__(self):
        self.nroot = None
        #...

    def show(self):
        #...
        return self.dot
    
    def create(self, ntop, ft):

        if ntop == None:
            ntop = NODE("root")

        if self.nroot == None:
            self.nroot = ntop

        if isinstance(ft, ANDNODE):
            self.createand(ntop, ft)
        elif isinstance(ft, ORNODE):
            self.createor(ntop, ft)
        else:
            assert(0>1)

        return ntop