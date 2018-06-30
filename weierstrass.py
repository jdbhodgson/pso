'''
   A python program which uses particle swarm optimisation
   to find the inverse Weierstrass transform of a given function
'''
import random
import numpy as np
import configparser
from scipy.interpolate import interp1d
from scipy.interpolate import CubicSpline
from scipy.interpolate import splev, splrep
import matplotlib.pyplot as plt
import pso

def extend_odd(y):
    '''Creates an odd extention of an array'''
    y_odd = -np.flipud(y)
    y_odd = np.append(y_odd, 0)
    y = np.append(y_odd, y)
    return y

def extend_even(y):
    '''Creates an even extention of an array'''
    y_zero = y[0]
    y = np.delete(y, 0)
    y_even = np.flipud(y)
    y_even = np.append(y_even, y_zero)
    y = np.append(y_even, y)

    return y

def fitness(points):
    '''
       Evaluates how well a list approximates a solution
       to the inverse Weierstrass Transform.
       fitness is alsways positive and a lower fitness
       implies better approximation
    '''

    if parity == 'odd':
        y_ext = extend_odd(points)
    elif parity == 'even':
        y_ext = extend_even(points)
    x_ext = extend_odd(x)

    tck = splrep(x_ext, y_ext)

    G_func = np.empty(num_a) * 0

    for i in range(num_a):
        x_a = np.linspace(A[i]-cutoff, A[i]+cutoff, num=num_a)
        Kernel = np.exp(-(x_a-A[i])**2/2.)/(np.sqrt(2.*np.pi))
        G_func[i] = np.trapz(Kernel*splev(x_a, tck), x_a)

    integral = np.trapz((G_func-Target)**2, A)

    return integral

random.seed(12)

A0 = 20.

cutoff = 4
num_x = 4
num_a = 20

config = configparser.ConfigParser()
config.read('params.cfg')
params = [float(config['WEIERSTRASS'][key])
          for key in config['WEIERSTRASS']]
x = np.linspace(0, 1, num=num_x+1)**2 *(A0 + cutoff)
x = x[1:]
parity = 'odd'

A = np.linspace(-A0, A0, num=num_a)
Target = np.tanh(A*0.45)

x2 = np.linspace(-A0-cutoff, A0+cutoff, num=301)

lower_bound, upper_bound = 0, 2
bounds = [[lower_bound for i in range(num_x)],
          [upper_bound for i in range(num_x)]]
swarm = pso.Swarm(20, num_x, fitness, bounds)

def plotData(pos):

    fig = plt.figure()
    y = pos
    if parity == 'odd':
        yExt = extend_odd(y)
    elif parity == 'even':
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
