
import sympy

def symidx(row, col, prefix='m_', offset=1):
    return sympy.symbols('{}{}{}'.format(prefix, row + offset, col + offset))

def symmat(rows, cols, prefix='m', type='dense'):
    if type == 'dense':
        syms = []
        for i in range(rows):
            for j in range(cols):
                syms.append(symidx(i, j, prefix))
        return sympy.Matrix(rows, cols, syms)
    elif type == 'symmetric':
        m = sympy.Matrix.zeros(rows, rows)
        for i in range(rows):
            for j in range(i, rows):
                sym = symidx(i, j, prefix)
                m[i, j] = m[j, i] = sym
        return m
