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
        return CZPoly(out) #NOTE
    
    def __xor__(self, a) -> list:
        return self + a
          
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

        if p == CZPoly([[]]):
            return self

        if len(self.coef) > len(p.coef):
            r0 = copy.deepcopy(self)
            r1 = copy.deepcopy(p)
        else:
            r1 = copy.deepcopy(self)
            r0 = copy.deepcopy(p)

        if r0 == r1:
            return r0
        while not r0.is_empty():
            rnext = r0%r1
            r1,r0 = rnext,r1

        return r1._to_monic()
    
    #basically written division
    #res_degree is the degree of the quotient
    #the remainder results from writing on the dividend
    def __divmod__(self, d):

        a = copy.deepcopy(self)
        out = CZPoly([[]])
        res_degree = 1
        if d.is_empty():
            return CZPoly([[]]),self
        
        if len(self.coef)<len(d.coef): 
            return CZPoly([[]]), self
        final_degree = len(self.coef)- len(d.coef)

        #if len(d.coef) == 1:
        #    res_degree = len(a.coef)- len(d.coef)
        #    #if res_degree <0:
        #    #    break
        #    res_div = a.coef[-1]/(d.coef[-1])
        #    out.coef.insert(0,res_div)
        #    a.coef.pop(-1)
#
        #    prepend_x = CZPoly([[]])
        #    for i in range(res_degree):
        #        prepend_x.coef.append(Poly([]))
        #    prepend_x.coef.append(out.coef[0])
        #    xor = (prepend_x)*CZPoly(d.coef[:-1])
#
        #    a += (prepend_x)*CZPoly(d.coef[:-1])
#
        #    for i in range(len(self.coef)- len(d.coef)-len(out.coef)):
        #        out.coef.insert(0,Poly([]))
#
        #    return out,a

        while res_degree > 0:
            if a.is_empty():
                for i in range(len(self.coef)- len(d.coef)-len(out.coef)+1):
                    out.coef.insert(0,Poly([]))
                    return out,a
            res_degree = len(a.coef)- len(d.coef)
            #if res_degree <0:
            #    break
            res_div = a.coef[-1]/(d.coef[-1])
            out.coef.insert(0,res_div)
            a.coef.pop(-1)

            prepend_x = CZPoly([[]])
            for i in range(res_degree):
                prepend_x.coef.append(Poly([]))
            prepend_x.coef.append(out.coef[0])

            a += (prepend_x)*CZPoly(d.coef[:-1])

        #pad if output doesnt match size that it should be
        if a.is_empty():
            for i in range(len(self.coef)- len(d.coef)-len(out.coef)+1):
                out.coef.insert(0,Poly([]))
        return out, a
    
    def __truediv__(self, exp):
        res, mod = divmod(self,exp)
        return res

    def __mod__(self,mod):
        a,b = divmod(self,mod)
        return b
    
    def __pow__(self, exp):
        if exp == 0:
            return CZPoly([[0]])
        return self.sqm(exp)
    
    def powmod(self, exp : int, mod):
        if exp == 0:
            return CZPoly([[0]])
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
    
def sageme(inp):
    l = list()
    czpoly = inp
    for index, i in enumerate(czpoly.coef):
        if i.p == []:
            continue
        l.append("("+"".join([f" x^{v} + " for v in i.p]).removesuffix('+ ')+f")*X^{index} + ".removesuffix('+ '))
    return("+".join(l))
