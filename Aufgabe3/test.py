from poly import Poly
import base64
from CZPoly import CZPoly

base= [
"BAAAAAAAAAAAAAAAAAAAAA==",
"AgAAAAAAAAAAAAAAAAAAAA==",
"AcAAAAAAAAAAAAAAAAAAAA=="
]
exponent = 0xf4240
modulo = [
"JGAAAAAAAAAAAAAAAAAAAA==",
"AAgAAAAAAAAAAAAAAAAAAA==",
"EUAAAAAAAAAAAAAAAAAAAA=="
]
base = CZPoly([base64.b64decode(i) for i in base])
mod = CZPoly([base64.b64decode(i) for i in modulo])
c = base*mod
res = c/mod
assert base == res

res = CZPoly([[2, 3, 6, 8, 9, 15, 16, 19, 20, 21, 22, 24, 31, 32, 33, 36, 38, 41, 42, 43, 48, 49, 51, 53, 58, 59, 60, 66, 68, 71, 73, 74, 75, 79, 83, 86, 91, 93, 95, 96, 98, 100, 101, 105, 107, 108, 110, 111, 113, 118, 119, 120, 121, 123, 126, 127],[2, 4, 12, 14, 16, 18, 20, 26, 27, 33, 36, 38, 39, 41, 43, 44, 45, 48, 49, 50, 51, 52, 55, 57, 59, 61, 62, 63, 64, 65, 66, 68, 69, 70, 71, 77, 78, 79, 82, 83, 85, 86, 89, 94, 97, 101, 102, 106, 108, 110, 115, 122, 123, 125, 127]])
for i in res.coef:
    print(base64.b64encode(i.poly2block()))
exponent = 1000000
out = base.powmod(exponent,mod)

assert out == res





#c = mod*base
#out = c.__divmod__(base)
#print(c.gcd(base))
#print()