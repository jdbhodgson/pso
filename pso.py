'''
   A python3 implementation of Particle Swarm Optimisation
'''
import sys
import time
import random
from math import cos
import matplotlib.pyplot as plt
import anim

class Swarm(object):
    '''
        The main Swarm class consists of a collection of particles,
        and contains routines for advancing the swarm.
    '''

    def __init__(self, m, n, f, b_lo, b_up, w=0.9, phi_p=0.7, phi_g=0.7):
        self.swarm_size = swarm_size   # int - swarm size
        self.p_dim = p_dim   # int - particle dimension
        self.f = f   # int - minimizing function
        self.b_lo = b_lo   # list[n] - lower bound
        self.b_up = b_up   # list[n] - upper bound
        self.range = [abs(b_up[i]-b_lo[i]) for i in range(n)]
        self.best = None   # tuple - best value (X, f(X))

        self.particles = [Particle(self, j, w, phi_p, phi_g)
                          for j in range(swarm_size)]
        self.history=[self.best[1]]
        # Ring topology
        self.groups = [[self.particles[(i+j)%swarm_size]
                        for i in range(-1, 2)]
                       for j in range(swarm_size)]
        self.update_swarm_g()

    def __repr__(self):
        out = ('<Swarm: particles=%d, minimizer=%s, best=%8.2e>'
                % (self.swarm_size, self.f.__name__, self.best[1]))
        return out

    def update(self):
        ''' Updates the swarm by one PSO step. '''
        self.update_swarm_x()
        self.update_swarm_g()
        self.history.append(self.best[1])

    def update_swarm_x(self):
        ''' Updates the swarm positions by one PSO step. '''
        for particle in self.particles:
            particle.update()

    def update_swarm_g(self):
        ''' Updates the swarm group bests.
            (Should be called after update_swarm_x) '''
        for j, group in enumerate(self.groups):
            bests = [particle.p[1] for particle in group]
            minBest = min(bests)
            i = bests.index(minBest)
            self.particles[j].g = group[i].p

    def run(self, N, v=False):
        ''' Advances the swarm by N PSO steps. '''
        for i in range(N):
            self.update()
            if v:
                if round(N/500) < 2:
                    out = '%6.2f%% Complete' % round(100*i/N, 2)             
                    sys.stdout.write('\r' + out)
                    sys.stdout.flush()
                elif i%round(N/500):
                    out = '%6.2f%% Complete' % round(100*i/N, 2)
                    sys.stdout.write('\r' + out)
                    sys.stdout.flush()

        if v:
            out = '%6.2f%% Complete' % 100
            sys.stdout.write('\r' + out+'\n')
            sys.stdout.flush()

    def run_anim(self, N, v=False):
        a = anim.Animator()
        a.xrange_0 = (0,10)
        a.yrange_0 = (self.best[1]/10,self.best[1])
        a.yscale= 'log'
        def data_gen(swarm, t=0):
            i = 0

            yield t, self.best[1]
            while i < N:
                swarm.update()
                i += 1
                t += 1
                yield t, swarm.best[1]

        a.data_gen = data_gen(self)

        a.animate()

    def plot(self, dims=(0, 1)):
        ''' Shows a scatter plot for all particles in the swarm for
            a given 2D slice. '''
        x = [p.x[dims[0]] for p in self.particles]
        y = [p.x[dims[1]] for p in self.particles]

        fig,ax =plt.subplots()
        ax.scatter(x, y)

        plt.show()

class Particle(object):

    def __init__(self, swarm, j, w, phi_p, phi_g):
        self.j = j
        self.swarm = swarm
        p_dim = swarm.p_dim
        self.x = [random.random()*swarm.range[i]
                  + swarm.b_lo[i] for i in range(p_dim)]
        self.v = [2*random.random()*swarm.range[i]
                    - swarm.range[i] for i in range(p_dim)]

        self.vmax = [0.2*swarm.range[i] for i in range(p_dim)]
        self.p = (list(self.x), swarm.f(self.x))
        if (not swarm.best) or  self.p[1] < swarm.best[1]:
            swarm.best = self.p
        self.g = self.p
        self.w = w
        self.phi_p = phi_p
        self.phi_g = phi_g

    def __repr__(self):
        out = ('<Particle #%d: w=%4.2f, phi_p=%4.2f, phi_g=%4.2f, best=%8.2e>'
                % (self.j, self.w, self.phi_p, self.phi_g, self.p[1]))
        return out

    def update_v(self):
        ''' Updates the particle velocity. '''
        for i in range(self.swarm.p_dim):
            r_p = random.random()
            r_g = random.random()

            self.v[i] = (self.w*self.v[i]
                        + r_p*self.phi_p*(self.p[0][i]-self.x[i])
                        + r_g*self.phi_g*(self.g[0][i]-self.x[i]))
            if self.v[i] > self.vmax[i]:
                self.v[i] = self.vmax[i]
            elif self.v[i] < -self.vmax[i]:
                self.v[i] = -self.vmax[i]

    def update_x(self):
        ''' Updates the particle position. '''
        for i in range(self.swarm.p_dim):
            self.x[i] += self.v[i]
            if self.x[i] > self.swarm.b_up[i]:
                self.x[i] = self.swarm.b_up[i]
                self.v[i] = 0

            elif self.x[i] < self.swarm.b_lo[i]:
                self.x[i] = self.swarm.b_lo[i]
                self.v[i] = 0

    def update_p(self):
        ''' Updates the particle best known position and value.
            (Also updates the swarm best if necessary)'''
        fx = self.swarm.f(self.x)
        if fx < self.p[1]:
            self.p = (list(self.x), fx)
            if fx < self.swarm.best[1]:
                self.swarm.best = (list(self.x),fx)

    def update(self):
        ''' Updates the particle one PSO step '''
        self.update_v()
        self.update_x()
        self.update_p()


def benchmark(N):
    ''' Carries out a benchmark run of the PSO algorithm for N steps.
        Uses the test_swarm to minimize the test_function.
        Prints the Swarm minimum, Accuracy, and time to complete.
        Returns the Swarm itself for inspection.
    '''
    random.seed(12)
    s = test_swarm()
    startTime = time.time()
    s.run(N)

    print('Swarm min = %e',s.best[1])
    endTime = round(time.time()-startTime, 4)
    print('Completed in %f seconds.' % endTime)
    return s

def test_swarm():
    ''' Creates a swarm object for benchmarking and unit tests.
        Returns a swarm of 20 particles in 4 dimensions, with
        minimizer=test_function, and bounds of -10<x[i]<10 for
        all dimensions.
    '''
    s = Swarm(20, 4, test_function,
              [-10 for i in range(4)],
              [ 10 for i in range(4)])
    return s

def test_function(L):
    ''' Test function for benchmarking and unit tests.
        Takes a 4 element list as its only argument.
        f([x,y,z,t]) = 4-cos(x)-cos(y)-cos(z)-cos(t)
                       +(x^2+y^2+z^2+t^2)/100
        f has a minimum at f([0,0,0,0]) = 0.
    '''
    x,y,z,t = L
    return (4-cos(x)-cos(y)
             -cos(z)-cos(t)
             +(x**2+y**2+z**2+t**2)/100.)
 