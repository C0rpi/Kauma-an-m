from .poly import Poly
from .CZPoly import CZPoly
import random
import copy
from math import ceil
class Cantor:
    
    nonce : Poly
    ct : list
    ad : list
    at : list
    def __init__(self,nonce,ct,ad,at) -> None:
        
        ctl = list()
        for i,v in enumerate(ct):
            print(len(v))
            ctl.append([Poly(v[index:index+16]) for index in range(0,len(v),16) ])
            
        self.nonce = Poly(nonce)
        self.ct = ctl
        self.ad = [Poly(i) for i in ad]
        self.at = [Poly(i) for i in at]

    def rand_poly(self,ind):
        out = list()
        for i in range(ind):
            out.append(Poly(random.getrandbits(128)))
        return CZPoly(out)


    def _round(self):
        l = len(self.ct)#is always every ct the same length
        for i in self.ct:
            pass
        p = list()
        for i,v in enumerate(self.ct[0]):
            p.append(v+self.ct[1][i])
        
        f = CZPoly(p)
        p = copy.deepcopy(f)
        q = 2**128
        while True:
            h = self.rand_poly(len(f.coef)-1)
            g = h.pow((q-1)//3-1,f)
            poly_q = g.gcd(p)
            if not q == Poly(1) and not q == p:
                return q, p/q
    def run(self):
        k1,k2 = self._round()
        print(k1,k2)