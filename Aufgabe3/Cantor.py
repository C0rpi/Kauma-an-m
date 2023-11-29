from .poly import Poly
from .CZPoly import CZPoly
import random
import copy
from math import ceil
from functools import reduce
class Cantor:
    
    nonce : Poly
    ct : list
    ad : list
    at : list
    f : CZPoly
    def __init__(self,nonce,ct,ad,at) -> None:
        
        ctl = list()
        for i,v in enumerate(ct):
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


    def _round(self, p = None):
        l = len(self.ct)#is always every ct the same length
        for i in self.ct:
            pass
        if not p:
            p = list()
            for i,v in enumerate(self.ct[0]):
                p.append(v^self.ct[1][i])
            p.insert(0,self.at[0]^self.at[1])
            p = CZPoly(p)
            self.f = copy.deepcopy(p)
        q = 2**128
        counter = 0
        while True:
            h = self.rand_poly(len(p.coef)-1)
            g = h.pow((q-1)//3,self.f) + CZPoly([[0]])
            poly_q = p.gcd(g)#idk why, always poly_q == p 🤷 
            if not poly_q.is_empty() and not poly_q == p._to_monic() and not poly_q == CZPoly([[0]]):
                print(f"g: {g}\n\n")
                print(f"P: {p}\n\npolyq: {poly_q}\n\n p/q:{(p/poly_q)._to_monic()}")
                return poly_q, (p/poly_q)._to_monic()
            counter+=1
            if counter >10:
                return None, None
            
    def get_candidates(self):
        out = list()
        k2 = None
        while not k2:
            k1,k2 = self._round()
        out.append(k1)
        out.append(k2)
        condition = True
        res = list()
        while condition:
            if out == [] and res == []:
                k2 = None
                while not k2:
                    k1,k2 = self._round()
            else:
                for i,v in enumerate(out):
                    if len(v.coef) == 2 and v.coef[1] == Poly([0]):
                        continue
                    if not k2:
                        out = list()
                        res = list()
                        break
                    k1,k2 = self._round(v)
                    out.append(k1)
                    out.append(k2)
            for i in out:
                if not i[1] == Poly([0]):
                    done = True
                else:
                    done = False
                    break
                    
                
            if not out == [] and done:
                res = out
                break
                
        print(f"\nout: {out}\n")
        print(f"res: {res}\n")

        return res
    
    #untested, too many errors found in previously completed code, runtime far too slow to enable proper debugging, sad sad
    def check_candidates(self, candidates):
        for i,candidate in enumerate(candidates):
            l = Poly(sum([i.orig_length for i in self.ad[0]]).to_bytes(8,'big') + sum([i.orig_length for i in self.ct[0]]).to_bytes(8,'big'))
            res = self.at[0]^(candidate[0]^l)

            #idk couldnt test
            for ct in self.ct[0]:
                res ^= (ct^candidate[0])
            ek = res

            l = Poly(sum([i.orig_length for i in self.ad[0]]).to_bytes(8,'big') + sum([i.orig_length for i in self.ct[0]]).to_bytes(8,'big'))
            res = self.at[1]^(candidate[0]^l)
            for ct in self.ct[1]:
                res ^= (ct^candidate[0])
            res ^=ek
            if not res == self.at[1]:
                continue
            #.......

        return res, ek

    
    def authenticate(self,h,ek):
        pass
        from .aes import AES128GCM
        at = self._ghash(self.ad[3],self.ct,h,ek)

    def _ghash(self,ad,cts,h,ek):
        acc = Poly([])    
        l = Poly(sum([i.orig_length for i in ad]).to_bytes(8,'big') + sum([i.orig_length for i in cts]).to_bytes(8,'big'))
        for i in reversed(ad):
            cts.insert(0,i)
        for ct in cts:
            acc ^= ct
            acc *= h
        return acc ^ ek

    def run(self):
        #c : list
        c = self.get_candidates()
        print('\n\n\n\n\n\n')
        print(c)
        print('\n\n\n\n\n\n')
        h, ek = self.check_candidates(c)
        at = self.authenticate(h,ek)
        return at


    
