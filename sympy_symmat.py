from sympy import *

x = MatrixSymbol('x', 2, 1)
y = MatrixSymbol('y', 2, 1)
M = MatrixSymbol('M', 2, 2)
h = Symbol('h')
L = MatrixSymbol('L', 2, 2)
J = MatrixSymbol('J', 2, 2)
d = MatrixSymbol('d', 2, 1)
b = MatrixSymbol('b', 2, 1)

e  = 0.5 * (x - y).T * M * (x - y) + h*h*(0.5 * x.T * L * x - x.T*J*d)
e2 = 0.5 * (x - y).T * M * (x - y) + h*h*0.5 * x.T * L * x - h*h*x.T*J*d

print(e-e2)