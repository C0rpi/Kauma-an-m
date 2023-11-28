#TODO MOAR GENERATORS

from .poly import Poly
import copy

class CZPoly(Poly):

    coef : list #list(list(Poly))

    #gets a list of lists as input, converts those to list of polys
    def __init__(self,coef : list) -> None:
        index = len(coef)+1
        for i,v in enumerate(coef):
            if not type(v) == Poly:
                coef[i] = Poly(v)
        for i,v in enumerate(coef[::-1]):
            if v == Poly([]):
                index = i
            else:
                break
        
        self.coef = coef[:index]
    
    def binlist(self) -> list:
        return [i.binlist() for i in self.coef]
    
    def binlist_8bit(self) -> list:        
        return [i.binlist_8bit() for i in self.coef]
    
    def poly2block(self) -> bytes:
        out = list()
        for i in self.coef:
            out.append(i.poly2block())
        return out
    
    def __add__(self,a):
        if len(self.coef) > len(a.coef):
            out = [v^self.coef[i] for i,v in enumerate(a.coef)]+ self.coef[len(a.coef):]
        elif len(self.coef) < len(a.coef):
            out = [v^a.coef[i] for i,v in enumerate(self.coef)] + a.coef[len(self.coef):]
        else:
            out = [v^a.coef[i] for i,v in enumerate(self.coef)]
        return CZPoly(out)
          
    def __mul__(self,a):
        out = [[] for i in range(len(self.coef) + len(a.coef)-1)]
        for i1,v1 in enumerate(self.coef):
            for i2,v2 in enumerate(a.coef):
                inserter = v2*v1
                if not out[i1+i2] == []:
                    out[i1+i2] ^= inserter
                else:
                    out[i1+i2] = inserter
        return CZPoly(out)

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
                    p=(p*self)%red
        return p

    #eea basically pseudocode
    def gcd(self,p):
        if len(self.coef) > len(p.coef):
            r0 = copy.deepcopy(self)
            r1 = copy.deepcopy(p)
        else:
            r1 = copy.deepcopy(self)
            r0 = copy.deepcopy(p)
            rnext = r0%r1
            if rnext == r1:
                return CZPoly([[0]])
            r1,r0 = r0,rnext
        if r0.is_empty():
            return CZPoly([[0]])
        return r0._to_monic()
    
    def __divmod__(self, d):
        a = copy.deepcopy(self)
        out = list()
        i = 1
        res_degree = 1
        
        if len(self.coef)<=len(d.coef): return None, self
        
        while len(out)<len(d.coef):
            res_degree = len(a.coef)-(i-1) - len(d.coef)
            if res_degree <0:
                break

            res_div = a.coef[len(a.coef)-i]/(d.coef[-1])
            a.coef[len(a.coef)-i]^=res_div*d.coef[-1]
            out.insert(0,res_div)
            for j,v in enumerate(d.coef[len(d.coef)-2::-1]):
                index = res_degree + (len(d.coef)-2)-j
                rem_poly = v*res_div
                if index >= 0:
                    a.coef[index]^=rem_poly
                else:
                    breakpoint()
            i += 1
        rem = list()
        for i,v in enumerate(a.coef[::-1]):
            if not v.p == []:
                rem.append(v)
        return CZPoly(out), CZPoly(rem[::-1])
    
    def __truediv__(self, exp):
        res, mod = divmod(self,exp)
        return res

    def __mod__(self,mod):
        a,b = divmod(self,mod)
        return b
    
    def __pow__(self, exp):
        return self.sqm(exp)
    
    def powmod(self, exp : int, mod):
        return self.sqm(exp, mod)
        
    def is_empty(self):
        for i in self.coef:
            if not i == Poly([]):
                return False
        return True
        
    def _to_monic(self):
        red = self.coef[-1]
        out = list()
        for i in self.coef:
            out.append(i / red)
        return CZPoly(out) 
    
    def __eq__(self,a):
        if type(self) == CZPoly and type(a) == CZPoly:

            return self.coef == a.coef 
        return False

    def __repr__(self):
        return str([str(i)+"," for i in self.coef])