from .poly import Poly
from cryptography.hazmat.primitives.ciphers.algorithms import AES128
from cryptography.hazmat.primitives.ciphers import Cipher, modes
import math
import copy
import base64
class AES128GCM:
    
    key : Poly
    nonce : Poly
    ad : Poly
    pt : list
    h : Poly
    atxor : Poly
    ctr : Poly
    y : Poly
    def __init__(self, key : Poly, nonce : Poly,ad : Poly, pt : list) -> None:
        self.key = key
        self.nonce = nonce
        self.ad = ad
        self.pt = pt

    def encrypt(self):
        cts,y0 = self._gen_ct()
        at = self._ghash(copy.deepcopy(cts))
        return cts,at,y0,self.h
    
    def _gen_ct(self):
        cts = list()
        self.ctr = Poly([])
        cipher = Cipher(AES128(self.key.poly2block()),modes.ECB()).encryptor()
        self._update_y()
        self._update_h(cipher)
        self._update_y()
        y0 = self.y    
        self._gen_atxor(cipher)
        #if no plaintexts are present, return no ciphertexts!
        if self.pt == [] or self.pt[0].p == []:
            return [],y0
        for p in self.pt:
            self._update_y()
            bce = Poly(cipher.update(self.y.poly2block()))
            cts.append(self._block_xor(p,bce))
            cts[-1].orig_length = p.orig_length #help
        cipher.finalize()
        return cts,y0
    
    def _ghash(self, cts : list):
        acc = Poly([])        
        l = Poly(sum([i.orig_length for i in self.ad]).to_bytes(8,'big') + sum([i.orig_length for i in cts]).to_bytes(8,'big'))
        cts.append(l)

        for i in reversed(self.ad):
            cts.insert(0,i)

        for ct in cts:
            acc ^= ct
            acc *= self.h
        return acc ^ self.atxor
    
    def _update_y(self) -> None:
        self.y = self.nonce + self.ctr
        self.ctr.increment(127)

    def _update_h(self,cipher):
        self.h = Poly(cipher.update(b'\0'*16))

    def _gen_atxor(self,cipher):
        self.atxor = Poly(cipher.update(self.y.poly2block()))

    def _block_xor(self,ptb,bce):
        res = ptb ^ bce
        return res