from poly import Poly
from CZPoly import CZPoly
import random
import copy
from math import ceil
class Cantor:
    
    nonce : Poly
    ct : list
    ad : list
    at : list
    def __init__(self,nonce,ct,ad,at) -> None:
        self.nonce = nonce
        self.ct = ct
        self.ad = ad
        self.at = at

    def rand_poly(self,ind):
        out = list()
        for i in ind:
            out.append(Poly(random.getrandbits(128)))
        return CZPoly(out)


    def run(self):
        ctl = [[] for i in j for j in self.ct]
        for i in self.ct[:3]:
            for j in i:
                ctl
        len = ceil(len(self.ct[0]/16))#is always every ct the same length
        f = Poly(self.at[0]+self.at[1])
        p = copy.deepcopy(len-1)
        q = 2**128
        condition = True
        while condition:
            h = self.rand_poly(len(f.coef)-1)
            g = h.mod((q-1)/3+Poly(1),f)
            poly_q = g.gcd(p)