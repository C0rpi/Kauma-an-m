from poly import Poly
from CZPoly import CZPoly
import random
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

    def rand_poly(self):
        return Poly(random.getrandbits(128))


    def run(self):
        h = self.rand_poly()
        
        pass