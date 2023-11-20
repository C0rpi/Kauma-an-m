from functools import reduce

class Poly:

    p : list

    def __init__(self, inp) -> None:
        #input can be either list or bytes
        if type(inp) == bytes:
            val = int.from_bytes(inp)
            self.p = [i for i in range(len(inp)*8) if (val >> (len(inp)*8-1-i) & 1) == 1]
        elif type(inp) == list:
            self.p = inp 
        else:
            raise ValueError()
        
    
    
    def poly2block(self) -> bytes:
        outlist = [1 if i in self.p else 0 for i in range(129) ]
        res = bytearray()
        for j in range(8,129,8):
            b = 0
            for i,v in enumerate(outlist[j-8:j]):
                if v ==1:
                    b = b + (1 << ((7-i) % 8))
            res.append(b)
        return res
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
        l = list()
        for i in a.p:
            l.append(Poly(self._lshift(i)))
        mul = reduce(lambda a,b: a^b, l) #Performance?
        res = mul._reduce()
        return res

    def __xor__(self,a) -> list:
        out = list()
        for i in self.p:
            if not i in a.p:
                out.append(i)
            else:
                a.p.remove(i)
        for i in a.p:
            if not i in self.p:
                out.append(i)
        return Poly(sorted(out))
    def __repr__(self) -> str:
        return str(self.p)