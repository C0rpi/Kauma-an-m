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
c = CZPoly([[7, 10, 14, 15],[8, 11, 15, 16, 17],[8, 9, 10, 11, 13, 16, 18, 19],[9, 13, 15, 19, 20, 21],[10, 11, 12, 14, 15, 17, 18]])
base = CZPoly([base64.b64decode(i) for i in base])
mod = CZPoly([base64.b64decode(i) for i in modulo])
c = base*mod
assert base == c/mod

exponent = 1000000
print(base.powmod(exponent,mod))

c = mod*base
out = c.__divmod__(base)
print(c.gcd(base))
print()