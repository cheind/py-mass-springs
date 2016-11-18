import numpy as np
import scipy.sparse
import scipy.sparse.linalg


particles = np.zeros(3, dtype=[
    ('x', float, 2),
    ('xprev', float, 2),
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

        self.nparticles = self.particles.shape[0]
        self.nsprings = self.springs.shape[0]
        self.ndim = self.particles['x'].shape[1]

        self.M, self.Mi = self.compute_M()
        self.L = self.compute_L()
        self.J = self.compute_J()

        self.d = np.empty((self.ndim * self.nsprings, 1))
        self.b = np.zeros((self.nparticles * self.ndim, 1))

        # Prefactor M + L * timestep**2
        self.solveAxb = scipy.sparse.linalg.factorized(self.M + self.L * self.timestep**2)

    def compute_A(self, i):
        """Returns the incidence vector for the i-th spring of size m x 1"""
        i1 = self.springs[i]['first']
        i2 = self.springs[i]['second']
        return scipy.sparse.csc_matrix(([1., -1.], ([i1, i2], [0, 0])), shape=(self.nparticles, 1))

    def compute_S(self, i):
        """Returns the i-th spring indicator of size s x 1"""
        return scipy.sparse.csc_matrix(([1], ([i], [0])), shape=(self.nsprings, 1))         

    def compute_L(self):
        """Computes the stiffness-weighted Laplacian of the mass-spring graph. L is m*ndims x m*ndims """
        l = scipy.sparse.csc_matrix((self.nparticles, self.nparticles))

        for i in range(self.springs.shape[0]):
            s = self.springs[i]
            A = self.compute_A(i)
            l += s['k'] * A * A.transpose()

        return scipy.sparse.kron(l, np.eye(self.ndim, self.ndim), format='csc')

    def compute_M(self):
        """Computes the diagonal mass matrix and its inverse. M and M inverse are m*ndims x m*ndims """
        return (scipy.sparse.kron(scipy.sparse.diags(self.particles['m']), np.eye(self.ndim, self.ndim), format='csc'),
                scipy.sparse.kron(scipy.sparse.diags(1.0 / particles['m']), np.eye(self.ndim, self.ndim), format='csc'))


    def compute_J(self):
        """Computes J. J is m*ndims x s*ndims """
        j = scipy.sparse.csc_matrix((self.nparticles, self.nsprings))

        for i in range(self.nsprings):
            s = self.springs[i]
            A = self.compute_A(i)
            j += s['k'] * A * self.compute_S(i).transpose()

        return scipy.sparse.kron(j, np.eye(self.ndim, self.ndim), format='csc')
       
    def update_d(self):
        """Updates the spring lengths to optimal rest length values while keeping their directions."""

        def normalized(a):
            """Normalizes each row of a."""
            n = np.apply_along_axis(np.linalg.norm, 1, a)
            n[n==0.] = 1 # Leave as is for zero vectors
            return a / n.reshape(-1, 1)

        # Compute the directions of springs using the current position of the particles
        self.d[:] = (self.springs['r'] * normalized(self.particles['x'][self.springs['second']] - self.particles['x'][self.springs['first']])).reshape(-1, 1) 

    def update_x(self):
        """Computes new particles positions by solving Ax=b."""

        # Update the right hand side.
        self.b.fill(0.)

        self.b += self.timestep**2 * self.J * self.d
        self.b += self.M * (2 * self.particles['x'] - self.particles['xprev']).reshape(-1, 1) 
        
        self.particles['xprev'][:] = self.particles['x']
        self.particles['x'][:] = self.solveAxb(self.b).reshape(self.nparticles, -1)       

    def solve(self, iterations):      
        for _ in range(iterations):
            self.update_d()
            self.update_x()

particles['m'] = 1.
particles[1]['m'] = 100000
particles[0]['x'] = [0, 0]
particles[1]['x'] = [1.5, 0]
particles[2]['x'] = [100, 0]
particles['xprev'][:] = particles['x']
springs[0]['first'] = 0
springs[0]['second'] = 1
springs[1]['first'] = 1
springs[1]['second'] = 2
springs['k'] = 10
springs['r'] = 1

solver = BlockCoordinateSolver(particles, springs, 1.0 / 30.0)


solver.solve(10)
print(particles['x'])
solver.solve(10)
print(particles['x'])
solver.solve(10)
print(particles['x'])
solver.solve(10)
print(particles['x'])

