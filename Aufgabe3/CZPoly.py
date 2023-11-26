#TODO fix sqm, manual verification for values if possible LOL


from poly import Poly
import copy

class CZPoly(Poly):

    coefficients : list #list(list(Poly))

    #gets a list of lists as input, converts those to list of polys
    def __init__(self,coefficients : list) -> None:
        self.coefficients = []
        for i in coefficients:
            self.coefficients.append(Poly(i))
            
    def __add__(self,a):
        for i,v in enumerate(self.coefficients):
            self.coefficients[i] == self.coefficients[i] ^ a.coefficients[i]
        return 
    
    def __mul__(self,a):
        out = CZPoly([[] for i in range(len(self.coefficients) + len(a.coefficients)-1)])
        for i1,v1 in enumerate(self.coefficients):
            for i2,v2 in enumerate(a.coefficients):
                inserter = v2*v1    
                out.coefficients[i1+i2] ^= inserter
        return out

    def sqm(self,exp : int): #no reduce needed because the multiply reduces for every step anyhow, not quite the most performant way, but works none the less
        p = copy.deepcopy(self)
        exp = Poly(exp).p
        binlist = [1 if i in exp else 0 for i in range(exp[-1]+1)]
        for i in binlist:
            p *=p
            if i == 1:
                p*=self
        return p
            

    def gcd(self,p):
        pass
    
    def __mod__(self,red):
        return self._reduce(red)

    def __pow__(self, exp):
        return self.sqm(exp)
    
    def powmod(self,mod):
        p = copy.deepcopy(self)
        binlist = [1 if i in p else 0 for i in range(p[-1])]
        for i in binlist:
            for i,v in enumerate(p.coefficients):
                p.coefficients[i] == v.mulred(v,mod)
                if i == 1:
                    p.coefficients = v.mulred(self.coefficients,mod)
        return p
    
    def __repr__(self):
        return "".join([str(i) for i in self.coefficients])