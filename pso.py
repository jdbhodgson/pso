'''
   A python3 implementation of Particle Swarm Optimisation
'''
import sys
import time
import random
from multiprocessing import Process, Queue
import configparser
from math import cos
import matplotlib.pyplot as plt
import anim


class Swarm(object):
    '''
        The main Swarm class consists of a collection of particles,
        and contains routines for advancing the swarm.
    '''
    # pylint: disable=too-many-instance-attributes
    # Ten is reasonable in this case.

    def __init__(self, swarm_size, p_dim, function, bounds):
        config = configparser.ConfigParser()
        config.read('params.cfg')
        hyperparams = [float(config['HYPERPARAMS'][key])
                       for key in config['HYPERPARAMS']]

        self.swarm_size = swarm_size   # int - swarm size
        self.p_dim = p_dim   # int - particle dimension
        self.function = function   # int - minimizing function
        self.b_lo = bounds[0]   # list[n] - lower bound
        self.b_up = bounds[1]   # list[n] - upper bound
        self.range = [abs(self.b_up[i]-self.b_lo[i])
                      for i in range(p_dim)]
        self.best = (None, None)  # tuple - best value (X, f(X))

        self.particles = [Particle(self, j, hyperparams)
                          for j in range(swarm_size)]
        self.history = [self.best[1]]
        # Ring topology
        self.groups = [[self.particles[(i+j) % swarm_size]
                        for i in range(-1, 2)]
                       for j in range(swarm_size)]
        self.update_swarm_g()

    def __repr__(self):
        out = ('<Swarm: particles=%d, minimizer=%s, best=%8.2e>'
               % (self.swarm_size, self.function.__name__, self.best[1]))
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
            bests = [particle.p_best[1] for particle in group]
            min_best = min(bests)
            i = bests.index(min_best)
            self.particles[j].g_best = group[i].p_best

    def run(self, n_steps, verbose=False):
        ''' Advances the swarm by N PSO steps. '''
        for i in range(n_steps):
            self.update()
            if verbose:
                if round(n_steps/500) < 2:
                    out = '%6.2f%% Complete' % round(100*i/n_steps, 2)
                    sys.stdout.write('\r' + out)
                    sys.stdout.flush()
                elif i % round(n_steps/500):
                    out = '%6.2f%% Complete' % round(100*i/n_steps, 2)
                    sys.stdout.write('\r' + out)
                    sys.stdout.flush()

        if verbose:
            out = '%6.2f%% Complete' % 100
            sys.stdout.write('\r' + out+'\n')
            sys.stdout.flush()

    def run_anim(self, n_steps, plot_best=None):
        '''
            Advances the swarm by N PSO steps, while
            showing the swarm best history.
            if plot_best is given, it should be a function which
            takes as arguments a plot axis and a list of points
            (position of a particle). Then run_anim will plot the
            best particle along with the history.
        '''
        animator = anim.Animator(plot_best=plot_best, swarm=self)
        animator.xrange_0 = (0, 10)
        animator.yrange_0 = (self.best[1]/10, self.best[1])
        animator.yscale = 'log'
        animator.axis.set_xlabel('step')
        animator.axis.set_ylabel('fitness')

        def data_gen(t=0):
            '''Completes one PSO step, and outputs history'''
            i = 0

            yield t, self.best[1]
            while i < n_steps:
                self.update()
                i += 1
                t += 1
                yield t, self.best[1]

        animator.animate(data_gen)

    def plot(self, dims=(0, 1)):
        ''' Shows a scatter plot for all particles in the swarm for
            a given 2D slice. '''
        x = [p.x[dims[0]] for p in self.particles]
        y = [p.x[dims[1]] for p in self.particles]

        fig, axis = plt.subplots()
        axis.scatter(x, y)

        plt.show(fig)


class Particle(object):
    '''
        A python class for a particle within the swarm. Updates
        its velocity and position via a pso implementation.
    '''

    # pylint: disable=too-many-instance-attributes
    # Ten is reasonable in this case.

    def __init__(self, swarm, j, hyperparams):
        self.j = j
        self.swarm = swarm
        p_dim = swarm.p_dim
        self.x = [random.random()*swarm.range[i] +
                  swarm.b_lo[i] for i in range(p_dim)]
        self.v = [2*random.random()*swarm.range[i] -
                  swarm.range[i] for i in range(p_dim)]

        self.vmax = [0.2*swarm.range[i] for i in range(p_dim)]
        self.p_best = (list(self.x), swarm.function(self.x))
        if (not swarm.best[1]) or self.p_best[1] < swarm.best[1]:
            swarm.best = self.p_best
        self.g_best = self.p_best
        self.omega = hyperparams[0]
        self.phi_p = hyperparams[1]
        self.phi_g = hyperparams[2]

    def __repr__(self):
        out = ('<Particle #%d: omega=%4.2f, phi_p=%4.2f,'
               ' phi_g=%4.2f, best=%8.2e>'
               % (self.j, self.omega, self.phi_p,
                  self.phi_g, self.p_best[1]))
        return out

    def update_v(self):
        ''' Updates the particle velocity. '''
        for i in range(self.swarm.p_dim):
            r_p = random.random()
            r_g = random.random()
            self.v[i] = (self.omega*self.v[i] +
                         r_p*self.phi_p*(self.p_best[0][i]-self.x[i]) +
                         r_g*self.phi_g*(self.g_best[0][i]-self.x[i]))
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
        func_x = self.swarm.function(self.x)
        if func_x < self.p_best[1]:
            self.p_best = (list(self.x), func_x)
            if func_x < self.swarm.best[1]:
                self.swarm.best = (list(self.x), func_x)

    def update(self):
        ''' Updates the particle one PSO step '''
        self.update_v()
        self.update_x()
        self.update_p()


def benchmark(n_steps):
    ''' Carries out a benchmark run of the PSO algorithm for N steps.
        Uses the test_swarm to minimize the test_function.
        Prints the Swarm minimum, Accuracy, and time to complete.
        Returns the Swarm itself for inspection.
    '''
    random.seed(12)
    swarm = test_swarm()
    start_time = time.time()
    swarm.run(n_steps)

    print('Swarm min = %e' % swarm.best[1])
    end_time = round(time.time()-start_time, 4)
    print('Completed in %f seconds.' % end_time)
    return swarm


def test_swarm():
    ''' Creates a swarm object for benchmarking and unit tests.
        Returns a swarm of 20 particles in 4 dimensions, with
        minimizer=test_function, and bounds of -10<x[i]<10 for
        all dimensions.
    '''
    swarm = Swarm(20, 4, test_function,
                  [[-10 for i in range(4)],
                   [10 for i in range(4)]])
    return swarm


def test_function(variables):
    ''' Test function for benchmarking and unit tests.
        Takes a 4 element list as its only argument.
        f([x,y,z,t]) = 4-cos(x)-cos(y)-cos(z)-cos(t)
                       +(x^2+y^2+z^2+t^2)/100
        f has a minimum at f([0,0,0,0]) = 0.
    '''
    x, y, z, t = variables
    return (4 - cos(x) - cos(y) -
            cos(z) - cos(t) +
            (x**2 + y**2 + z**2 + t**2)/100.)


class MultiSwarm(object):
    '''
    '''
    def __init__(self, swarms):
        self.swarms = swarms
        self.n_swarms = len(swarms)

    def do_it(self, n_processes):

        start_time = time.time()
        print('Initialising...')
        queue = Queue()
        processes = [Process(target=self.run_swarm, args=(queue,))
                     for i in range(n_processes)]
        print(__name__)
        for process in processes:
            process.start()

        end_time = round(time.time()-start_time, 4)
        print('Initialised in %f seconds.' % end_time)
        start_time = time.time()

        for i in range(self.n_swarms):
            queue.put(i)

        for process in processes:
            queue.put(-1)

        for process in processes:
            process.join()

        end_time = round(time.time()-start_time, 4)
        print('Completed in %f seconds.' % end_time)

    def run_swarm(self, queue):
        i = ''
        while True:
            i = queue.get()
            if i < 0:
                break
            self.swarms[i].run(100)
