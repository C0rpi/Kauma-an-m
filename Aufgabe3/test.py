from poly import Poly
import base64
from CZPoly import CZPoly

i = 3
i = Poly(i)
print(i)
print(i)



l = [
"BAAAAAAAAAAAAAAAAAAAAA==",
"AgAAAAAAAAAAAAAAAAAAAA==",
"AcAAAAAAAAAAAAAAAAAAAA=="
]
b = [
"JGAAAAAAAAAAAAAAAAAAAA==",
"AAgAAAAAAAAAAAAAAAAAAA==",
"EUAAAAAAAAAAAAAAAAAAAA=="
]
result = [
"IGAAAAAAAAAAAAAAAAAAAA==",
"AggAAAAAAAAAAAAAAAAAAA==",
"EIAAAAAAAAAAAAAAAAAAAA=="
]
p1 = []
for i in l:
    p1.append(Poly(base64.b64decode(i)))
for p in p1:
    print(p)
print("\n")
p1 = []
for i in b:
    p1.append(Poly(base64.b64decode(i)))
for p in p1:
    print(p)
print("\n")
p1 = []
    
for i in result:
    p1.append(Poly(base64.b64decode(i)))
for p in p1:
    print(p)
print("\n")


l = [
"BAAAAAAAAAAAAAAAAAAAAA==",
"AgAAAAAAAAAAAAAAAAAAAA==",
"AcAAAAAAAAAAAAAAAAAAAA=="
],
exponent= 1000000,
b = [
"JGAAAAAAAAAAAAAAAAAAAA==",
"AAgAAAAAAAAAAAAAAAAAAA==",
"EUAAAAAAAAAAAAAAAAAAAA=="
]
base = [
"BAAAAAAAAAAAAAAAAAAAAA==",
"AgAAAAAAAAAAAAAAAAAAAA==",
"AcAAAAAAAAAAAAAAAAAAAA=="
]
exponent = 3


p1 = []
for i in base:
    p1.append((base64.b64decode(i)))
for p in p1:
    print(p)
p1 = CZPoly(p1)
print(p1**exponent)
print()