import numpy as np
import scipy.sparse
import scipy.sparse.linalg


particles = np.zeros(3, dtype=[
    ('q', float, 2),
    ('qprev', float, 2),
    ('m', float),
])

springs = np.zeros(2, dtype=[
    ('first', int),
    ('second', int),
    ('k', float),
    ('r', float)
])

class BlockCoordinateSolver:

    def __init__(self, particles, springs, timestep):
        self.particles = particles
        self.springs = springs
        self.timestep = timestep
        self.m = self.particles.shape[0]
        self.s = self.springs.shape[0]
        self.dims = self.particles['q'].shape[1]

        self.M = scipy.sparse.kron(scipy.sparse.diags(particles['m']), np.eye(self.dims, self.dims), format='csc')
        self.Mi = scipy.sparse.kron(scipy.sparse.diags(1.0 / particles['m']), np.eye(self.dims, self.dims), format='csc')
        self.L = self.compute_L()
        self.J = self.compute_J()

        # Prefactor M + L * timestep**2
        self.global_solver = scipy.sparse.linalg.factorized(self.M + self.L * self.timestep**2)

    def compute_A(self, i):
        """Returns the incidence vector for the i-th spring of size m x 1"""
        i1 = self.springs[i]['first']
        i2 = self.springs[i]['second']
        return scipy.sparse.csc_matrix(([1., -1.], ([i1, i2], [0, 0])), shape=(self.m, 1))

    def compute_S(self, i):
        """Returns the i-th spring indicator of size s x 1"""
        return scipy.sparse.csc_matrix(([1], ([i], [0])), shape=(self.s, 1))         

    def compute_L(self):
        """Computes the stiffness-weighted Laplacian of the mass-spring graph. L is m*ndims x m*ndims """
        l = scipy.sparse.csc_matrix((self.m, self.m))

        for i in range(self.springs.shape[0]):
            s = self.springs[i]
            A = self.compute_A(i)
            l += s['k'] * A * A.transpose()

        return scipy.sparse.kron(l, np.eye(self.dims, self.dims), format='csc')


    def compute_J(self):
        """Computes J. J is m*ndims x s*ndims """
        j = scipy.sparse.csc_matrix((self.m, self.s))

        for i in range(self.springs.shape[0]):
            s = self.springs[i]
            A = self.compute_A(i)
            j += s['k'] * A * self.compute_S(i).transpose()

        return scipy.sparse.kron(j, np.eye(self.dims, self.dims), format='csc')
       
    def solve(self, iterations):        
        pass

particles['m'] = 1.
springs[0]['first'] = 0
springs[0]['second'] = 1
springs[1]['first'] = 1
springs[1]['second'] = 2
springs['k'] = 1.

solver = BlockCoordinateSolver(particles, springs, 1.0 / 30.0)




