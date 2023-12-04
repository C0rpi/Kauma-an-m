from .poly import Poly
from .CZPoly import CZPoly
import random
import copy
import base64
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
        if not p:
            l1 = self.gen_l(0)
            l2 = self.gen_l(1)
            p = list()

            b1 = list()
            b2 = list()

            for i,v in enumerate(self.ad[0]):
                    b1.insert(0,v)
            for i,v in enumerate(self.ct[0]):
                b1.insert(0,v)
            b1.insert(0,self.gen_l(0))
            b1.insert(0,self.at[0])
            for i,v in enumerate(self.ad[1]):
                    b2.insert(0,v)
            for i,v in enumerate(self.ct[1]):
                b2.insert(0,v)
            b2.insert(0,self.gen_l(1))
            b2.insert(0,self.at[1])

            p = CZPoly(b1)^CZPoly(b2)
            
            self.f = copy.deepcopy(p)._to_monic()
            
            
        q = 2**128
        counter = 1
        while True:
            h = self.rand_poly(len(p.coef)-1)
            #h =
            g = h.pow((q-1)//3,self.f) + CZPoly([[0]])
            poly_q = p.gcd(g)
            
            if not poly_q == p and not poly_q == CZPoly([[0]]) :
                pdq = (p/poly_q)
                return poly_q, pdq._to_monic()
            counter+=1
            if counter >15:
                return None, None
            
    def get_candidates(self):
        out = list()
        for i in range(5):
            k1,k2 = self._round()
            if k1 == None:#dont waste more time
                return None
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
            for i in out:
                if i and i.coef[1]== Poly([0]) and len(i.coef)==2:
                    res.append(i)
            return res
    
    def _get_ek(self, candidates):
        for i in candidates:
            candidate = i.coef[0]
            l = self.gen_l(0)
            ek = Poly([])
            current_ct = copy.deepcopy(self.ct[0][::-1])
            for i in self.ad[0][::-1]:
                current_ct.append(i)
            for i,v in enumerate(current_ct):
                ek^= v*(candidate.pow(i+2))
            ek^=l*candidate
            ek^= self.at[0]
            at = self.try_authenticate(candidate,ek,2)
            if at == self.at[2]:
                return candidate, ek
        return None

    
    def try_authenticate(self,h,ek,index):
        at = self._ghash(self.ad[index],self.ct[index],h,ek,index)
        return at

    def _ghash(self,ad,ctlist,h,ek,index):
        cts = copy.deepcopy(ctlist)
        acc = Poly([])    
        l = self.gen_l(index)
        cts.append(l)
        for i in reversed(ad):
            cts.insert(0,i)
        for ct in cts:
            acc ^= ct
            acc *= h
        #print(base64.b64encode((acc^ek).poly2block()))
        #print(base64.b64encode(acc.poly2block()))    
        return acc ^ ek
    def gen_l(self,index):
        return Poly(sum([i.orig_length for i in self.ad[index]]).to_bytes(8,'big') + sum([i.orig_length for i in self.ct[index]]).to_bytes(8,'big'))

    def check_candidates(self,candidates):
        h, ek = self._get_ek(candidates)   
        at4 = self.try_authenticate(h,ek,3)
        return at4
            


    def run(self):
        #c : list
        c = self.get_candidates()
        if c:
            res = c[0]
            for i in c[1:]:
                res*=i
            at = self.check_candidates(c)
        return at
