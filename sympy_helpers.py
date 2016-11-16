
import sympy

def symidx(row, col, prefix='m_', offset=1, shape=None):
    is_matrix = shape is None or (len(shape) == 2 and shape[0] > 1 and shape[1] > 1)
    if is_matrix:
        return sympy.symbols('{}{}{}'.format(prefix, row + offset, col + offset))
    else:
        which = row if len(shape) == 1 or shape[0] > 1 else col
        return sympy.symbols('{}{}'.format(prefix, which + offset))

def symmat(rows, cols, prefix='m', type='dense'):
    if type == 'dense':
        syms = []
        for i in range(rows):
            for j in range(cols):
                syms.append(symidx(i, j, prefix, shape=(rows, cols)))
        return sympy.Matrix(rows, cols, syms)
    elif type == 'symmetric':
        m = sympy.Matrix.zeros(rows, rows)
        for i in range(rows):
            for j in range(i, rows):
                sym = symidx(i, j, prefix)
                m[i, j] = m[j, i] = sym
        return m
