#TODO MOAR GENERATORS

from poly import Poly
import copy

class CZPoly(Poly):

    coef : list #list(list(Poly))

    #gets a list of lists as input, converts those to list of polys
    def __init__(self,coef : list) -> None:
        if coef and type(coef[0]) == Poly:
            self.coef = coef
            return
        self.coef = []
        for i in coef:
            self.coef.append(Poly(i))
            
    def __add__(self,a):
        return CZPoly(
            [v^self.coef[i] for i,v in enumerate(a.coef)]+ [(self.coef[len(a.coef):])] 
            if len(self.coef) >= len(a.coef) 
            else  
            [v^a.coef[i] for i,v in enumerate(self.coef)] + [(a.coef[len(self.coef)])])
          
    def __mul__(self,a):
        out = CZPoly([[] for i in range(len(self.coef) + len(a.coef)-1)])
        for i1,v1 in enumerate(self.coef):
            for i2,v2 in enumerate(a.coef):
                inserter = v2*v1    
                out.coef[i1+i2] ^= inserter
        return out

    def sqm(self,exp : int): #no reduce needed because the multiply reduces for every step anyhow, not quite the most performant way, but works none the less
        p = copy.deepcopy(self)
        binlist = Poly(exp).binlist()[-2::-1]#automatically cuts the first one, bc that inherently represented in the algorithm
        for i in binlist:
            p *=p
            if i == 1:
                p*=self
        return p
    
    def binlist(self) -> list:
        return [i.binlist() for i in self.coef]
    def binlist_8bit(self) -> list:        
        return [i.binlist_8bit() for i in self.coef]


    #def gcd(self,p):
    #    pass
    
    #def __mod__(self,red):
    #    return self._reduce(red)

    def __divmod__(self, d):
        a = copy.deepcopy(self)
        out = list()
        i = 1
        while len(out)< len(d.coef):
            index = a.coef[len(a.coef)-i].p[-1]-d.coef[-1].p[-1]
            val = a.coef[len(a.coef)-i]/(d.coef[-1])
            out.insert(0,val)
            for j,v in enumerate(d.coef[len(d.coef)-1::-1]):
                print(Poly(v._lshift(index)))
                a.coef[len(a.coef)-len(d.coef)-j]^=(Poly(v._lshift(index)))
            i += 1
        return out

    def __pow__(self, exp):
        return self.sqm(exp)
    
    """def pow(self, exp, mod : Poly):
        cpoly = copy.deepcopy(self)
        #basically sqm but with the functions supporting mod instead
        binlist = Poly(exp).binlist()[-2::-1]
        b = bytes(Poly(exp).poly2block())
        out = list()
        for i,p in enumerate(cpoly.coef):
            for b in binlist:
                p = p.mulred(p,mod.coef[i])
                print()
                if b == 1:
                    p = p.mulred(cpoly.coef[i],mod.coef[i])
                    print()

            out.append(p)
        return out
        """
    
    
    
    def _monic(self):
        pass

    def __repr__(self):
        return "".join([str(i)+"," for i in self.coef])