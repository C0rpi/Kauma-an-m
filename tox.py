from Aufgabe3.CZPoly import CZPoly
from Aufgabe3.poly import Poly 
czpoly =CZPoly([[0, 5, 7, 8, 10, 13, 15, 16, 19, 21, 23, 28, 29, 36, 37, 40, 41, 46, 47, 48, 50, 51, 54, 56, 57, 58, 60, 64, 67, 69, 73, 74, 75, 77, 80, 82, 83, 85, 87, 88, 91, 92, 93, 94, 95, 96, 97, 98, 99, 102, 103, 107, 108, 109, 116, 117, 118, 119, 120, 123, 124, 125, 126],[1],[1]])

for i,v in enumerate(czpoly.coef[:-1]):
    print(i)


l = list()
for index, i in enumerate(czpoly.coef):
    l.append("("+"".join([f" x^{v} + " for v in i.p]).removesuffix('+ ')+f")*X^{index} + ".removesuffix('+ '))
print("+".join(l))
