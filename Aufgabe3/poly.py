from functools import reduce
from math import ceil


#Polyclass
#stores 1s (and only ones) of polynoms in big endian notation by saving their corresponding exponent
class Poly:

    p : list
    orig_length : int #size of original input if e.g. the input has 0-bytes at the end

    def __init__(self, inp) -> None:
        #input can be either list or bytes
        if type(inp) == bytes:
            val = int.from_bytes(inp)
            self.p = [i for i in range(len(inp)*8) if (val >> (len(inp)*8-1-i) & 1) == 1]
            self.orig_length = len(inp)*8
        elif type(inp) == list:

            self.p = inp 
            if not self.p == []:
                self.orig_length = self.blocksize()
            else:
                self.orig_length = 8
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


        self.p = self.p[:-1] + [(self.p[-1]+1)]
    
    def poly2block(self) -> bytes:
        if self.p == []:
            return b'\0'*16
        outlist = [1 if i in self.p else 0 for i in range(128) ]
        res = bytearray()
        for j in range(8,self.blocksize()+1,8):
            b = 0
            for i,v in enumerate(outlist[j-8:j]):
                if v ==1:
                    b = b + (1 << ((7-i) % 8))
            res.append(b)
        l = bytes(res)
        return res
    

    def blocksize(self):
        if not self.p == []:
            if not self.p[-1] % 8 == 0:
                return ceil((self.p[-1]/8))*8
            else:
                return self.p[-1] + 1
        return 0
    def _reduce(self) -> None:
        a = self
        red = Poly([0,1,2,7,128]) #fix
        while red.p[-1] <= a.p[-1]:
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
        for i in a.p:
            l.append(Poly(self._lshift(i)))
        mul = reduce(lambda a,b: b^a, l)
        res = mul._reduce()
        return res
    def __add__(self,a):
        if len(a.p) ==0 or len(self.p) == 0:
            return Poly(self.p + a.p)
        if self.p[-1] > a.p[0]:
            return Poly(self.p + a._lshift(ceil((self.p[-1]/8))*8))
        else:
            return Poly(self.p + a.p)

    def __xor__(self,a) -> list:
        #if one list is empty return other list
        if self.p == [] or a.p == []:
            return Poly(self.p+a.p)
        
        out = list()
        for i in self.p:
            if not i in a.p:
                out.append(i)
            else:
                a.p.remove(i)
        for i in a.p:
            if not i in self.p:
                if i > self.p[-1]:
                    break
                out.append(i)
        return Poly(sorted(out))
    def __repr__(self) -> str:
        return str(self.p)
    