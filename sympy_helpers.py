
import sympy

def symidx(idx, prefix='m_', offset=1):
    if len(idx) == 1:
        return sympy.symbols('{}{}'.format(prefix, idx[0] + offset))
    else:
        return sympy.symbols('{}{}{}'.format(prefix, idx[0] + offset, idx[1] + offset))

def symmat(rows, cols, prefix='m', type='dense'):
    if type == 'dense':
        syms = []
        for i in range(rows):
            for j in range(cols):
                syms.append(symidx((i,j), prefix))
        return sympy.Matrix(rows, cols, syms)
    elif type == 'symmetric':
        m = sympy.Matrix.zeros(rows, rows)
        for i in range(rows):
            for j in range(i, rows):
                sym = symidx((i,j), prefix)
                m[i, j] = m[j, i] = sym
        return m
