import base64
from poly import Poly

b = base64.b64decode("OkfFRfHYf/t/PILSC706Qg==")
p = Poly(b)
assert p.p == [2, 3, 4, 6, 9, 13, 14, 15, 16, 17, 21, 23, 25, 29, 31, 32, 33, 34, 35, 39, 40, 41, 43, 44, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 62, 63, 65, 66, 67, 68, 69, 70, 71, 74, 75, 76, 77, 80, 86, 88, 89, 91, 94, 100, 102, 103, 104, 106, 107, 108, 109, 111, 114, 115, 116, 118, 121, 126] 

l = [ 4, 8, 15, 16, 23, 42 ]
p = Poly(l)
res = str(base64.b64encode(p.poly2block()),'ascii')
assert res == 'CIGBAAAgAAAAAAAAAAAAAA=='
a = base64.b64decode("jjYoD6kfN+/Y/g4Hl991Cw==")
b = base64.b64decode("tQsToM4bzOQtot/1w4x8PA==")
p1 = Poly(a)
p2 = Poly(b)
p3 = p1*p2
res = base64.b64encode(bytearray(p3.poly2block()))
assert res == b"khnvYitpTW8Sv3ZUmFqasw=="