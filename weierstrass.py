'''
   A python program which uses particle swarm optimisation
   to find the inverse Weierstrass transform of a given function
'''
import random
import numpy as np
from scipy.interpolate import interp1d
from scipy.interpolate import CubicSpline
from scipy.interpolate import splev, splrep
import matplotlib.pyplot as plt
import pso

def extend_odd(x):
    '''Creates an odd extention of an array'''
    x_odd = -np.flipud(x)
    x_odd = np.append(x_odd, 0)
    x = np.append(x_odd, x)
    return x

def extend_even(x):
    '''Creates an even extention of an array'''
    x_zero = x[0]
    x = np.delete(x, 0)
    x_even = np.flipud(x)
    x_even = np.append(x_even, x_zero)
    x = np.append(x_even, x)

    return x

def fitness(points):
    '''
       Evaluates how well a list approximates a solution
       to the inverse Weierstrass Transform.
       fitness is alsways positive and a lower fitness
       implies better approximation
    '''

    if type == 'odd':
        y_ext = extend_odd(points)
    elif type == 'even':
        y_ext = extend_even(points)
    x_ext = extend_odd(x)

    tck = splrep(x_ext, y_ext)

    G = np.empty(num_a) * 0
    
    for i in range(num_a):
        xi = np.linspace(A[i]-cutoff, A[i]+cutoff, num=num_a)
        Ker = np.exp(-(xi-A[i])**2/2.)/(np.sqrt(2.*np.pi))
        G[i] = np.trapz(Ker*splev(xi, tck), xi)

    Integral = np.trapz((G-Target)**2, A)

    return Integral

random.seed(12)

A0 = 20.

cutoff = 4
num_x = 4
num_a = 20
x = np.linspace(0, 1, num=num_x+1)**2 *(A0 + cutoff)
x = x[1:]
type = 'odd'

A = np.linspace(-A0, A0, num=num_a)
Target = np.tanh(A*0.45)

x2 = np.linspace(-A0-cutoff, A0+cutoff, num=301)

lower_bound, upper_bound = 0,2
bounds = [[lower_bound for i in range(num_x)],
          [upper_bound for i in range(num_x)]]
swarm = pso.Swarm(20, num_x, fitness, bounds)

def plotData(pos):

    fig = plt.figure()
    y = pos
    if type == 'odd':
        yExt = extend_odd(y)
    elif type == 'even':
        yExt = extend_even(y)

    xExt = extend_odd(x)
    tck = splrep(xExt, yExt)

    plt.plot(x, y, 'o', x2, splev(x2, tck), '-', color='black')

    #if plotSave == 'save':
    #
    #   fig.savefig( num_ame + '.png', dpi=fig.dpi)
    #
    #   plt.close(fig)
    #
    #else:
    #
    #   plt.show()
    #
    return fig