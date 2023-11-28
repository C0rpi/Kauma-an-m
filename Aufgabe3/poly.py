from functools import reduce
from math import ceil
import copy
from collections import Counter

#Polyclass
#stores 1s (and only ones) of polynoms in big endian notation by saving their corresponding exponent
class Poly:

    p : list
    orig_length : int #size of original input if e.g. the input has 0-bytes at the end

    def __init__(self, inp) -> None:
        #if type(inp) == Poly:
        #    self = copy.deepcopy(inp)
        #input can be either list or bytes or int
        if type(inp) == bytes or type(inp) == bytearray:
            val = int.from_bytes(inp,'big')
            self.p = [i for i in range(len(inp)*8) if (val >> (len(inp)*8-1-i) & 1) == 1]
            self.orig_length = len(inp)*8
            
        elif type(inp) == list:
            self.p = inp 
            if not self.p == []:
                self.orig_length = self.blocksize()
            else:
                self.orig_length = 8
                
        elif type(inp) == int:    
            bitlength = ceil(len((bin(inp).removeprefix('0b')))/8)*8
            self.p = [(bitlength-1)-i for i in range(bitlength) if (inp >> (bitlength-1-i) & 1) == 1][::-1]
            self.orig_length = bitlength
        else:
            raise ValueError()
        
    def increment(self,lowbit) -> None:
        if not lowbit in self.p:
            self.p.append(lowbit)
            return
        for i in reversed(range(lowbit+1)):
            if i in self.p:
                self.p.remove(i)
            else:
                self.p.append(i)
                return
    
    def poly2block(self) -> bytes:
        if self.p == []:
            return b'\0'*16
        outlist = [1 if i in self.p else 0 for i in range(128) ]
        res = list()
        for j in range(8,129,8):
            b = 0
            for i,v in enumerate(outlist[j-8:j]):
                if v ==1:
                    b = b + (1 << ((7-i) % 8))
            res.append(b)
        res = bytes(res)
        return res
    
    def poly2block_long(self) -> bytes:
        if self.p == []:
            return b'\0'
        outlist = [1 if i in self.p else 0 for i in range(self.blocksize()+7)]
        res = list()
        for j in range(8,self.blocksize()+7,8):
            b = 0
            for i,v in enumerate(outlist[j-8:j]):
                if v ==1:
                    b = b + (1 << ((7-i) % 8))
            res.append(b)
        res = bytes(res)
        return res
    
    def binlist(self) -> list:
        return [1 if i in self.p else 0 for i in range(self.p[-1]+1)]
    def binlist_8bit(self) -> list:
        return [1 if i in self.p else 0 for i in range(self.blocksize())]
    def binlist_128bit(self) -> list:
        return [1 if i in self.p else 0 for i in range(128)]
    
    def blocksize(self):
        if not self.p == []:
            return ceil(((self.p[-1]+1)/8))*8
        return 0
    
    def _aes_reduce(self) -> None:
        a = self
        red = Poly([0,1,2,7,128]) #fix            
        while not a.p == [] and red.p[-1] <= a.p[-1]:
            red_poly = Poly(red._lshift(a.p[-1]-red.p[-1]))
            a ^= red_poly
        return a
    
    def _reduce(self,red) -> None:       
        a = self  
        while not a.p == [] and red.orig_length <= a.p[-1]:
            red_poly = Poly(red._lshift(a.p[-1]-red.p[-1]))
            a ^= red_poly
        return a

    def _to_int(self):
        return sum([1<< i for i in self.p])
    
    def _lshift(self, index):
        return [i+index for i in self.p]

    def __mul__(self,a):
        if a.p == [] or self.p == []:
            return Poly([])
        l = list()
        mul = Poly([])
        for i in a.p:
            mul^=Poly(self._lshift(i))
        #mul = reduce(lambda a,b: b^a, l)
        res = mul._aes_reduce()
        return res

    def mulred(self,a,red):        
        if a.p == [] or self.p == []:
            return Poly([])
        l = list()
        for i in a.p:
            l.append(Poly(self._lshift(i)))
        mul = reduce(lambda a,b: b^a, l)
        res = mul._reduce(red)
        return res
    
    def __add__(self,a):
        if len(a.p) ==0 or len(self.p) == 0:
            return Poly(self.p + a.p)
        if self.p[-1] > a.p[0]:
            return Poly(self.p + a._lshift(ceil((self.p[-1]/8))*8))
        else:
            return Poly(self.p + a.p)

    def pow(self,a,mod = None):
        return self.sqm(a,mod)

    def sqm(self,exp,red = None): #no reduce needed because the multiply reduces for every step anyhow, not quite the most performant way, but works none the less
        if not red:
            red = Poly([0,1,2,7,128]) #fix
        p = self
        binlist = Poly(exp).binlist()[-2::-1]#automatically cuts the first one, bc that inherently represented in the algorithm
        for i in binlist:
            p *=p%red
            if i == 1:
                p*=self%red
        return p
    def __truediv__(self,exp):
        if self == exp:
            return Poly([0])
        mul =  exp.pow(2**128-2) #this is soooooo slow
        return self * mul

    def __mod__(self,red):
        a = self
        out = Poly([])
        while not a.p ==[] and red.p[-1] <= a.p[-1]:
            index = a.p[-1]-red.p[-1]
            red_poly = Poly(red._lshift(index))
            a ^= red_poly
            out.p.append(index)
        return a
    
    def __xor__(self,a) -> list:
        #b3 = (self.poly2block_long())
        #b4 = (a.poly2block_long())
        #b1 = reverse_bitorder(self.poly2block_long())
        #b2 = reverse_bitorder(a.poly2block_long())
        #i1 = int.from_bytes(b1,'little')
        #i2 = int.from_bytes(b2,'little')
        #res = Poly(bxor(b1,b2))
        #out = Poly(reverse_bitorder(int.to_bytes(i1^i2,(max(len(b1),len(b2))),'little')))
        res = Poly(sorted(list(set(a.p + self.p)-set(a.p).intersection(self.p))))
        
        return res
    
    def __eq__(self,a):
        if type(self) == Poly and type(a) == Poly:
            return self.p == a.p
        else:
            return False
    
    def __repr__(self) -> str:
        return str(self.p)


#not used currently
  
def bxor(ba : bytes, bb : bytes):
    if len(ba)>len(bb):
        bb = bb + b'\0'*(len(ba)-len(bb))
    elif len(bb)>len(ba):
        ba = ba + b'\0'*(len(bb)-len(ba))
    return bytes(x ^ y for (x, y) in zip(ba, bb)) 

def reverse_bitorder(b_in):
    out = bytearray()
    for b in bytearray(b_in):
        i = 0
        for bitindex in range(b.bit_length()):
            if (b >> bitindex) & 1 == 1:
                i |= 1 << (7-bitindex)
        out.append(i)
    return out
                
