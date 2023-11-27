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

    def sqm(self,exp : int, red  = None): #no reduce needed because the multiply reduces for every step anyhow, not quite the most performant way, but works none the less
        p = copy.deepcopy(self)
        binlist = Poly(exp).binlist()[-2::-1]#automatically cuts the first one, bc that inherently represented in the algorithm
        if not red:
            for i in binlist:
                p *=p
                if i == 1:
                    p*=self
        else:
            for i in binlist:
                p =(p*p)%red
                if i == 1:
                    p*=self
                    p %= red
        return p
    
    def binlist(self) -> list:
        return [i.binlist() for i in self.coef]
    def binlist_8bit(self) -> list:        
        return [i.binlist_8bit() for i in self.coef]


    def gcd(self,p):
        c, rem = divmod(self,p)
        for i in rem.coef:
            if not i.p == []:
                return rem._to_monic()
        return c._to_monic()
    
    def __divmod__(self, d):
        a = copy.deepcopy(self)
        out = list()
        i = 1
        res_degree = 1
        
        if len(self.coef)<=len(d.coef): return None, self
        
        while len(out)<=len(d.coef):
            res_degree = len(a.coef)-(i-1) - len(d.coef)
            res_div = a.coef[len(a.coef)-i]/(d.coef[-1])
            a.coef[len(a.coef)-i]^=res_div*d.coef[-1]
            out.insert(0,res_div)
            for j,v in enumerate(d.coef[len(d.coef)-2::-1]):
                index = res_degree + (len(d.coef)-2)-j
                if index >= 0:
                    a.coef[index]^=v*res_div
            i += 1
        rem = list()
        for i,v in enumerate(a.coef[::-1]):
            if not v.p == []:
                rem.append(v)
        return CZPoly(out), CZPoly(rem[::-1])

    def __mod__(self,mod):
        a,b = divmod(self,mod)
        return b
    
    def __pow__(self, exp):
        return self.sqm(exp)
    
    def powmod(self, exp : int, mod):
        return self.sqm(exp, mod)
        
        
        
        pass
        
    
    
    
    def _to_monic(self):
        red = self.coef[-1]
        out = list()
        for i in self.coef:
            out.append(i / red)
        return CZPoly(out) 

    def __repr__(self):
        return "".join([str(i)+"," for i in self.coef])