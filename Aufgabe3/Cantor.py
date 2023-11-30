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
        adl = list()
        for i,v in enumerate(ad):
            adl.append([Poly(v[index:index+16]) for index in range(0,len(v),16) ])
            
        self.nonce = Poly(nonce)
        self.ct = ctl
        self.ad = adl
        self.at = [Poly(i) for i in at]

    def rand_poly(self,ind):
        out = list()
        for i in range(ind):
            out.append(Poly(random.getrandbits(128)))
        return CZPoly(out)


    def _round(self, p = None):
        for i in self.ct:
            pass
        if not p:
            #l = Poly(sum([i.orig_length for i in self.ad[0]]).to_bytes(8,'big') + sum([i.orig_length for i in self.ct[0]]).to_bytes(8,'big'))
            p = list()
            for i,v in enumerate(self.ct[0]):
                p.insert(0,v^self.ct[1][i])#NOTE order reversed?
            p.insert(0,Poly([]))
            p.insert(0,self.at[0]^self.at[1])
            p = CZPoly(p)
            self.f = copy.deepcopy(p)
        q = 2**128
        counter = 1
        while True:
            h = self.rand_poly(len(p.coef)-1)
            g = h.pow((q-1)//3,self.f) + CZPoly([[0]])
            poly_q = p.gcd(g)
            if not poly_q.is_empty() and not poly_q == p._to_monic() and not poly_q == CZPoly([[0]]):
                #print(f"g: {g}\n\n")
                #print(f"P: {p}\n\npolyq: {poly_q}\n\n p/q:{(p/poly_q)._to_monic()}")
                print( (p/poly_q)._to_monic())
                return poly_q, (p/poly_q)._to_monic()
            counter+=1
            print(counter)
            if counter >10:
                return None, None
            
    def get_candidates(self):
        out = list()
        k2 = None
        while not k2:
            k1,k2 = self._round()
        out.append(k1)
        out.append(k2)
        #out = [None, None, CZPoly([[1, 2, 3, 8, 12, 13, 16, 18, 22, 23, 26, 28, 30, 31, 32, 38, 40, 41, 42, 45, 47, 48, 49, 50, 51, 52, 53, 54, 56, 57, 61, 67, 70, 71, 72, 75, 76, 78, 79, 80, 81, 85, 88, 91, 93, 94, 96, 98, 99, 101, 104, 105, 106, 108, 110, 111, 112, 114, 115, 117, 118, 119, 121, 122, 123, 125, 126, 127], [0]]), CZPoly([[0, 3, 4, 8, 9, 12, 13, 14, 17, 18, 19, 20, 22, 23, 25, 26, 29, 31, 33, 35, 36, 47, 50, 51, 53, 54, 57, 58, 59, 60, 62, 64, 65, 66, 70, 71, 72, 73, 76, 77, 80, 81, 84, 86, 87, 88, 90, 91, 94, 98, 100, 101, 102, 103, 104, 105, 106, 108, 110, 114, 115, 117, 119, 120, 124], [0]]), CZPoly([[0, 1, 3, 4, 5, 6, 9, 11, 18, 19, 22, 23, 26, 27, 32, 35, 36, 37, 38, 40, 43, 44, 45, 47, 48, 49, 50, 51, 54, 55, 56, 57, 58, 59, 60, 61, 64, 66, 67, 68, 69, 70, 73, 74, 78, 79, 82, 83, 85, 86, 89, 93, 94, 100, 101, 104, 106, 107, 112, 121, 122, 123, 124, 126, 127], [0]]), CZPoly([[1, 2, 3, 4, 5, 6, 9, 11, 12, 14, 15, 17, 20, 24, 25, 26, 28, 29, 34, 35, 38, 39, 40, 41, 42, 46, 47, 49, 51, 52, 53, 55, 59, 60, 61, 68, 69, 71, 72, 73, 75, 76, 78, 81, 82, 84, 85, 88, 92, 93, 94, 100, 102, 103, 104, 107, 109, 113, 116, 117, 121, 123, 124, 125, 127], [0]])]        
        res = list()
        
        for i,v in enumerate(out):
            if len(v.coef) == 2 and v.coef[1] == Poly([0]):
                continue
            if not k2:
                out = list()
                res = list()
                break
            k1,k2 = self._round(v)
            out[i] = None
            out.append(k1)
            out.append(k2)   
        print(out)
        for i in out:
            if i and i.coef[1]== Poly([0]) and len(i.coef)==2:
                res.append(i)
        print(f"\n\nres: {res}\n\n")
        return res
    
    def _get_ek(self, candidate):
        l = self.gen_l()        
        p = Poly([])
        for i,v in enumerate(self.ct[2]):
            p^= v*(candidate.pow(i+2))
        p^=l*candidate
        p^= self.at[2]
        ek = self.at[2]^(candidate^l)
        return ek

    
    def try_authenticate(self,h,ek):
        at = self._ghash(self.ad[3],self.ct[3],h,ek)
        return at

    def _ghash(self,ad,cts,h,ek):
        acc = Poly([])    
        l = self.gen_l()
        for i in reversed(ad):
            cts.insert(0,i)
        for ct in cts:
            acc ^= ct
            acc *= h
        return acc ^ ek
    def gen_l(self):
        return Poly(sum([i.orig_length for i in self.ad[0]]).to_bytes(8,'big') + sum([i.orig_length for i in self.ct[0]]).to_bytes(8,'big'))

    def check_candidates(self,candidates):        
        for i,candidate in enumerate(candidates):
            ek = self._get_ek(candidate.coef[0])
            at_try = self.try_authenticate(candidate.coef[0],ek)
            if at_try == self.at[2]:
                at4 = self.try_authenticate(candidate.coef[0],ek)
                return at4
            


    def run(self):
        #c : list
        c = self.get_candidates()
        #c = [CZPoly([[0, 1, 4, 7, 10, 11, 12, 13, 19, 23, 25, 29, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 46, 47, 48, 50, 52, 53, 54, 58, 60, 61, 72, 73, 75, 76, 78, 79, 85, 88, 89, 92, 95, 99, 100, 105, 106, 110, 111, 112, 113, 115, 117, 118, 120, 125, 126], [0]]), CZPoly([[0, 1, 4, 6, 7, 9, 13, 15, 18, 25, 27, 29, 31, 33, 35, 36, 37, 38, 39, 41, 42, 43, 44, 45, 50, 52, 53, 55, 56, 57, 63, 66, 67, 68, 69, 70, 71, 73, 76, 78, 81, 83, 92, 95, 96, 98, 101, 102, 105, 106, 108, 110, 112, 114, 120, 123, 124, 127], [0]]),CZPoly([[0, 1, 2, 3, 6, 10, 12, 14, 15, 16, 17, 21, 26, 27, 29, 30, 32, 33, 34, 37, 39, 40, 41, 44, 45, 47, 49, 55, 59, 60, 61, 63, 68, 74, 80, 83, 85, 86, 87, 89, 91, 92, 94, 95, 96, 97, 101, 103, 105, 106, 107, 108, 110, 111, 113, 115, 117, 120, 121, 123, 124, 126, 127], [0]]),CZPoly([[0, 3, 5, 10, 11, 12, 17, 21, 22, 24, 28, 30, 32, 33, 34, 36, 37, 38, 39, 40, 41, 42, 46, 51, 55, 56, 59, 63, 66, 67, 69, 71, 72, 76, 77, 78, 79, 80, 84, 85, 86, 87, 91, 92, 94, 95, 96, 98, 99, 100, 101, 102, 104, 107, 108, 109, 110, 111, 114, 118, 121, 123, 127], [0]])]
        res = c[0]
        for i in c[1:]:
            res*=i
        print(res)
        
        print('\n\n\n\n\n\n')
        print(c)
        print('\n\n\n\n\n\n')
        h, ek = self.check_candidates(c)
        at = self.authenticate(h,ek)
        return at


    
