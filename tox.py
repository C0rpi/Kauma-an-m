from Aufgabe3.CZPoly import CZPoly
from Aufgabe3.poly import Poly 

self = [[0, 5, 7, 8, 9, 17, 20, 23, 24, 26, 27, 36, 39, 44, 46, 52, 56, 59, 62, 63, 67, 68, 70, 73, 75, 76, 77, 78, 80, 82, 83, 84, 86, 87, 88, 89, 91, 93, 94, 95, 97, 98, 100, 101, 103, 104, 105, 106, 107, 110, 111, 114, 117, 119, 120, 121, 124], [], [0, 5, 7, 8, 10, 13, 15, 16, 19, 21, 23, 28, 29, 36, 37, 40, 41, 46, 47, 48, 50, 51, 54, 56, 57, 58, 60, 64, 67, 69, 73, 74, 75, 77, 80, 82, 83, 85, 87, 88, 91, 92, 93, 94, 95, 96, 97, 98, 99, 102, 103, 107, 108, 109, 116, 117, 118, 119, 120, 123, 124, 125, 126], [0, 1, 6, 8, 9, 10, 14, 15, 16, 17, 18, 20, 21, 23, 27, 29, 30, 31, 33, 35, 39, 41, 42, 43, 48, 50, 51, 54, 55, 56, 59, 60, 61, 62, 65, 66, 68, 71, 76, 78, 79, 81, 82, 83, 85, 86, 87, 89, 90, 91, 92, 94, 96, 97, 100, 101, 103, 105, 106, 107, 109, 110, 112, 113, 116, 117, 119, 122, 123, 125, 127], [0, 1, 4, 10, 18, 22, 23, 29, 30, 31, 32, 33, 35, 36, 38, 40, 42, 45, 46, 50, 53, 56, 57, 61, 62, 63, 64, 69, 70, 71, 73, 74, 75, 76, 78, 79, 82, 84, 86, 87, 88, 89, 90, 93, 94, 95, 96, 100, 101, 103, 104, 105, 107, 109, 110, 111, 115, 117, 119, 120, 122, 124, 127]]
p = [[1, 2, 4, 6, 7, 10, 13, 17, 19, 21, 23, 26, 27, 29, 30, 32, 39, 41, 42, 43, 44, 45, 47, 48, 49, 50, 52, 53, 54, 55, 56, 57, 65, 66, 67, 69, 72, 73, 79, 83, 85, 87, 88, 90, 91, 92, 93, 94, 97, 98, 99, 103, 106, 107, 108, 109, 112, 113, 114, 116, 117, 119, 120, 121, 124, 125, 126], [3, 6, 7, 10, 11, 12, 13, 14, 15, 25, 28, 31, 32, 33, 37, 39, 41, 42, 43, 44, 45, 47, 49, 53, 57, 59, 60, 63, 67, 69, 71, 72, 73, 75, 77, 79, 84, 89, 90, 91, 93, 95, 98, 99, 101, 102, 104, 105, 106, 109, 110, 113, 116, 117, 119, 120, 122, 123, 125, 126, 127], [0, 1, 2, 4, 5, 6, 7, 8, 11, 12, 13, 14, 17, 19, 21, 22, 23, 24, 25, 28, 29, 34, 35, 36, 37, 40, 46, 47, 52, 54, 55, 56, 59, 66, 69, 72, 73, 74, 76, 77, 78, 79, 80, 82, 85, 89, 93, 95, 96, 98, 100, 101, 103, 104, 105, 106, 109, 110, 112, 116, 119, 124, 126], [0, 1, 3, 4, 5, 6, 7, 8, 11, 14, 15, 17, 19, 20, 22, 23, 24, 25, 26, 27, 29, 35, 36, 38, 41, 42, 44, 46, 47, 48, 49, 50, 51, 54, 55, 57, 58, 59, 60, 64, 68, 73, 74, 77, 82, 83, 84, 85, 86, 90, 91, 93, 95, 98, 100, 101, 102, 105, 108, 110, 111, 112, 114, 117, 120, 122, 123, 124, 126, 127]]
pdq = [[0, 1, 4, 10, 18, 22, 23, 29, 30, 31, 32, 33, 35, 36, 38, 40, 42, 45, 46, 50, 53, 56, 57, 61, 62, 63, 64, 69, 70, 71, 73, 74, 75, 76, 78, 79, 82, 84, 86, 87, 88, 89, 90, 93, 94, 95, 96, 100, 101, 103, 104, 105, 107, 109, 110, 111, 115, 117, 119, 120, 122, 124, 127]]
g = [[1, 2, 4, 6, 7, 10, 13, 17, 19, 21, 23, 26, 27, 29, 30, 32, 39, 41, 42, 43, 44, 45, 47, 48, 49, 50, 52, 53, 54, 55, 56, 57, 65, 66, 67, 69, 72, 73, 79, 83, 85, 87, 88, 90, 91, 92, 93, 94, 97, 98, 99, 103, 106, 107, 108, 109, 112, 113, 114, 116, 117, 119, 120, 121, 124, 125, 126], [3, 6, 7, 10, 11, 12, 13, 14, 15, 25, 28, 31, 32, 33, 37, 39, 41, 42, 43, 44, 45, 47, 49, 53, 57, 59, 60, 63, 67, 69, 71, 72, 73, 75, 77, 79, 84, 89, 90, 91, 93, 95, 98, 99, 101, 102, 104, 105, 106, 109, 110, 113, 116, 117, 119, 120, 122, 123, 125, 126, 127], [0, 1, 2, 4, 5, 6, 7, 8, 11, 12, 13, 14, 17, 19, 21, 22, 23, 24, 25, 28, 29, 34, 35, 36, 37, 40, 46, 47, 52, 54, 55, 56, 59, 66, 69, 72, 73, 74, 76, 77, 78, 79, 80, 82, 85, 89, 93, 95, 96, 98, 100, 101, 103, 104, 105, 106, 109, 110, 112, 116, 119, 124, 126], [0, 1, 3, 4, 5, 6, 7, 8, 11, 14, 15, 17, 19, 20, 22, 23, 24, 25, 26, 27, 29, 35, 36, 38, 41, 42, 44, 46, 47, 48, 49, 50, 51, 54, 55, 57, 58, 59, 60, 64, 68, 73, 74, 77, 82, 83, 84, 85, 86, 90, 91, 93, 95, 98, 100, 101, 102, 105, 108, 110, 111, 112, 114, 117, 120, 122, 123, 124, 126, 127]]
h = [[3, 4, 10, 12, 13, 14, 15, 17, 18, 19, 20, 21, 22, 25, 28, 29, 30, 32, 33, 34, 37, 45, 46, 47, 48, 49, 50, 52, 53, 54, 55, 56, 59, 60, 62, 63, 64, 66, 70, 72, 73, 74, 77, 78, 79, 81, 84, 85, 88, 89, 90, 92, 96, 97, 101, 102, 105, 108, 109, 110, 111, 112, 113, 115, 116, 118, 120, 123, 124, 125, 127], [6, 7, 12, 13, 14, 16, 17, 24, 27, 29, 31, 32, 34, 35, 36, 43, 44, 45, 46, 48, 50, 51, 52, 53, 54, 56, 57, 58, 59, 60, 63, 68, 69, 71, 72, 74, 75, 76, 77, 79, 81, 82, 85, 87, 89, 90, 94, 100, 102, 103, 104, 105, 108, 109, 110, 112, 113, 114, 118, 119, 120, 122, 123, 125], [3, 4, 6, 7, 9, 11, 14, 17, 18, 20, 22, 24, 25, 27, 29, 31, 33, 34, 39, 40, 46, 47, 48, 49, 54, 55, 57, 58, 59, 60, 61, 62, 64, 65, 72, 75, 77, 78, 79, 80, 81, 83, 84, 85, 88, 89, 90, 91, 92, 93, 94, 96, 97, 98, 100, 101, 104, 105, 106, 107, 108, 109, 112, 113, 114, 115, 117, 119, 121, 125], [0, 2, 4, 5, 7, 8, 9, 10, 11, 18, 19, 20, 22, 26, 31, 32, 33, 34, 35, 36, 41, 42, 44, 45, 49, 50, 54, 55, 56, 58, 59, 61, 62, 64, 65, 67, 68, 70, 71, 73, 74, 75, 76, 78, 80, 81, 82, 83, 86, 89, 95, 96, 97, 98, 100, 102, 103, 108, 110, 113, 116, 117, 119, 120, 121, 122, 123, 124]]
j  =[[0, 5, 7, 8, 9, 17, 20, 23, 24, 26, 27, 36, 39, 44, 46, 52, 56, 59, 62, 63, 67, 68, 70, 73, 75, 76, 77, 78, 80, 82, 83, 84, 86, 87, 88, 89, 91, 93, 94, 95, 97, 98, 100, 101, 103, 104, 105, 106, 107, 110, 111, 114, 117, 119, 120, 121, 124], [], [0, 5, 7, 8, 10, 13, 15, 16, 19, 21, 23, 28, 29, 36, 37, 40, 41, 46, 47, 48, 50, 51, 54, 56, 57, 58, 60, 64, 67, 69, 73, 74, 75, 77, 80, 82, 83, 85, 87, 88, 91, 92, 93, 94, 95, 96, 97, 98, 99, 102, 103, 107, 108, 109, 116, 117, 118, 119, 120, 123, 124, 125, 126], [0, 1, 6, 8, 9, 10, 14, 15, 16, 17, 18, 20, 21, 23, 27, 29, 30, 31, 33, 35, 39, 41, 42, 43, 48, 50, 51, 54, 55, 56, 59, 60, 61, 62, 65, 66, 68, 71, 76, 78, 79, 81, 82, 83, 85, 86, 87, 89, 90, 91, 92, 94, 96, 97, 100, 101, 103, 105, 106, 107, 109, 110, 112, 113, 116, 117, 119, 122, 123, 125, 127], [0, 1, 4, 10, 18, 22, 23, 29, 30, 31, 32, 33, 35, 36, 38, 40, 42, 45, 46, 50, 53, 56, 57, 61, 62, 63, 64, 69, 70, 71, 73, 74, 75, 76, 78, 79, 82, 84, 86, 87, 88, 89, 90, 93, 94, 95, 96, 100, 101, 103, 104, 105, 107, 109, 110, 111, 115, 117, 119, 120, 122, 124, 127]]
a = [self,p,pdq,g,h]

p = [[3, 4, 6, 7, 19, 20, 22, 23, 24, 26, 27, 30, 31, 34, 37, 38, 40, 41, 42, 43, 44, 45, 48, 50, 51, 52, 54, 56, 60, 62, 65, 67, 68, 69, 70, 71, 73, 75, 76, 77, 84, 85, 86, 87, 88, 89, 90, 91, 92, 94, 98, 100, 103, 104, 105, 106, 109, 110, 111, 113, 114, 116, 117, 118, 119, 122, 123, 124, 127], [], [0, 1, 2, 4, 5, 13, 14, 21, 23, 25, 27, 34, 35, 36, 38, 41, 42, 45, 46, 48, 50, 53, 54, 56, 57, 58, 59, 60, 64, 65, 70, 74, 79, 81, 85, 86, 87, 88, 95, 96, 97, 99, 103, 104, 106, 109, 110, 111, 113, 114, 115, 117, 119, 122, 123, 125, 127], [1, 2, 5, 9, 10, 12, 14, 16, 18, 19, 22, 23, 24, 26, 28, 29, 31, 34, 36, 38, 40, 42, 48, 49, 51, 54, 55, 57, 58, 63, 70, 74, 75, 76, 77, 78, 81, 84, 85, 88, 96, 97, 101, 103, 104, 105, 106, 108, 109, 111, 120, 123, 125, 127], [0]]
g = [[0, 1, 5, 6, 7, 8, 10, 15, 18, 19, 21, 22, 23, 26, 27, 30, 31, 36, 37, 39, 40, 45, 47, 51, 53, 61, 62, 64, 69, 70, 74, 75, 78, 82, 83, 85, 87, 91, 94, 96, 100, 106, 107, 114, 117, 120, 121, 122, 123, 127], [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 15, 16, 20, 21, 22, 26, 27, 28, 29, 34, 36, 37, 41, 42, 45, 46, 49, 50, 51, 52, 53, 54, 56, 57, 59, 60, 61, 66, 68, 69, 73, 74, 75, 76, 79, 80, 82, 84, 85, 86, 88, 90, 93, 94, 95, 96, 97, 100, 101, 103, 104, 105, 106, 107, 108, 110, 112, 113, 115, 116, 117, 120, 121, 122, 124, 125, 127], [0, 2, 4, 5, 7, 10, 12, 13, 14, 16, 18, 22, 25, 27, 28, 31, 32, 34, 35, 37, 38, 39, 40, 41, 42, 43, 45, 46, 47, 48, 49, 50, 51, 55, 56, 58, 59, 60, 62, 64, 65, 68, 69, 70, 71, 73, 75, 78, 79, 80, 82, 85, 86, 87, 90, 91, 92, 93, 94, 96, 97, 100, 101, 102, 105, 107, 109, 111, 112, 117, 118, 119, 120, 122], [0, 1, 2, 5, 8, 9, 12, 14, 16, 20, 21, 23, 25, 32, 34, 36, 37, 38, 39, 44, 47, 48, 49, 50, 51, 54, 55, 57, 58, 60, 61, 62, 64, 65, 66, 70, 72, 73, 77, 81, 82, 83, 84, 86, 87, 90, 91, 98, 101, 102, 104, 109, 110, 114, 118, 120, 123, 126, 127]]

poly_q = [[0, 3, 5, 7, 8, 9, 10, 11, 13, 17, 19, 26, 30, 31, 33, 35, 36, 38, 39, 41, 42, 43, 44, 45, 47, 50, 51, 54, 55, 59, 60, 61, 62, 63, 64, 66, 68, 69, 76, 77, 79, 85, 86, 87, 88, 90, 91, 93, 96, 100, 101, 102, 105, 107, 109, 111, 113, 114, 116, 119, 122, 123, 126, 127], [1, 2, 7, 9, 10, 11, 12, 13, 16, 17, 22, 24, 25, 26, 27, 28, 32, 33, 34, 35, 36, 37, 39, 47, 49, 51, 54, 56, 59, 63, 64, 65, 67, 71, 82, 84, 86, 97, 98, 99, 101, 102, 104, 105, 108, 113, 115, 117, 120, 123, 124, 125], [0]]

self = [[0, 2, 3, 4, 7, 9, 10, 11, 12, 14, 19, 20, 23, 25, 26, 29, 40, 41, 42, 44, 45, 47, 50, 51, 52, 56, 57, 63, 65, 68, 69, 76, 81, 82, 83, 84, 85, 86, 88, 89, 90, 91, 92, 94, 95, 98, 99, 100, 102, 103, 106, 107, 108, 114, 115, 116, 120, 121, 122, 124, 126, 127], [0, 1, 3, 6, 9, 10, 11, 13, 16, 17, 19, 21, 23, 24, 26, 27, 28, 29, 31, 32, 39, 40, 41, 42, 43, 46, 47, 48, 50, 52, 53, 55, 56, 57, 58, 62, 63, 67, 70, 72, 74, 76, 78, 79, 83, 84, 86, 93, 95, 98, 99, 100, 101, 102, 104, 107, 109, 110, 112, 114, 115, 117, 118, 119, 122, 124, 125, 126], [0, 1, 3, 4, 5, 7, 9, 12, 17, 18, 22, 24, 27, 28, 29, 30, 33, 34, 35, 37, 39, 40, 41, 44, 45, 47, 49, 50, 51, 54, 56, 58, 59, 62, 63, 65, 66, 68, 70, 71, 74, 77, 80, 81, 83, 87, 88, 89, 90, 91, 94, 95, 96, 97, 98, 99, 100, 101, 102, 108, 110, 111, 113, 116, 117, 123, 124, 126]]

d = [[3, 4, 6, 7, 19, 20, 22, 23, 24, 26, 27, 30, 31, 34, 37, 38, 40, 41, 42, 43, 44, 45, 48, 50, 51, 52, 54, 56, 60, 62, 65, 67, 68, 69, 70, 71, 73, 75, 76, 77, 84, 85, 86, 87, 88, 89, 90, 91, 92, 94, 98, 100, 103, 104, 105, 106, 109, 110, 111, 113, 114, 116, 117, 118, 119, 122, 123, 124, 127], [], [0, 1, 2, 4, 5, 13, 14, 21, 23, 25, 27, 34, 35, 36, 38, 41, 42, 45, 46, 48, 50, 53, 54, 56, 57, 58, 59, 60, 64, 65, 70, 74, 79, 81, 85, 86, 87, 88, 95, 96, 97, 99, 103, 104, 106, 109, 110, 111, 113, 114, 115, 117, 119, 122, 123, 125, 127], [1, 2, 5, 9, 10, 12, 14, 16, 18, 19, 22, 23, 24, 26, 28, 29, 31, 34, 36, 38, 40, 42, 48, 49, 51, 54, 55, 57, 58, 63, 70, 74, 75, 76, 77, 78, 81, 84, 85, 88, 96, 97, 101, 103, 104, 105, 106, 108, 109, 111, 120, 123, 125, 127], [0]]



def sageme(inp):
    l = list()
    czpoly = inp
    for index, i in enumerate(czpoly):
        l.append("("+"".join([f" x^{v} + " for v in i]).removesuffix('+ ')+f")*X^{index} + ".removesuffix('+ '))
    return("+".join(l))

print()
print()
print(sageme(self))
print()
print()
print(sageme(d))