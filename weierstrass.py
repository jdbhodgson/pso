'''
   A python program which uses particle swarm optimisation
   to find the inverse Weierstrass transform of a given function
'''
import random
import configparser
import numpy as np
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

    if PARAMS['parity'] == 'odd':
        y_ext = extend_odd(points)
    elif PARAMS['parity'] == 'even':
        y_ext = extend_even(points)
    x_ext = extend_odd(x)

    spline_data = splrep(x_ext, y_ext)

    G = np.empty(PARAMS['num_a']) * 0

    for i in range(PARAMS['num_a']):
        x_a = np.linspace(A[i]-PARAMS['cutoff'],
                          A[i]+PARAMS['cutoff'],
                          num=PARAMS['num_a'])

        kernel = np.exp(-(x_a-A[i])**2/2.)/(np.sqrt(2.*np.pi))
        G[i] = np.trapz(kernel*splev(x_a, spline_data), x_a)

    integral = np.trapz((G-TARGET)**2, A)

    return integral


def plot_data(pos):
    '''
        Converts a list of spline points (pos) to its
        spline representation and plots the resulting curve.
    '''

    fig = plt.figure()
    y = pos
    if PARAMS['parity'] == 'odd':
        y_ext = extend_odd(y)
    elif PARAMS['parity'] == 'even':
        y_ext = extend_even(y)

    x_ext = extend_odd(x)
    spline_data = splrep(x_ext, y_ext)

    plt.plot(x, y, 'o', X_FINE, splev(X_FINE, spline_data), '-', color='black')

    # if plotSave == 'save':
    #
    #    fig.savefig( num_ame + '.png', dpi=fig.dpi)
    #
    #    plt.close(fig)
    #
    # else:
    #
    #    plt.show()
    #
    return fig

random.seed(12)

CONFIG = configparser.ConfigParser()
CONFIG.read('params.cfg')
PARAMS = dict(CONFIG['WEIERSTRASS'])
PARAMS_TYPES = dict(CONFIG['WEIERSTRASS_TYPES'])
for key in PARAMS:
    if PARAMS_TYPES[key] == 'int':
        PARAMS[key] = int(PARAMS[key])
    elif PARAMS_TYPES[key] == 'float':
        PARAMS[key] = float(PARAMS[key])

X_RANGE = PARAMS['a_range'] + PARAMS['cutoff']
x = np.linspace(0, 1, num=PARAMS['num_x']+1)**2 * X_RANGE
x = x[1:]

A = np.linspace(-PARAMS['a_range'], PARAMS['a_range'],
                num=PARAMS['num_a'])
TARGET = np.tanh(A*0.45)

X_FINE = np.linspace(-X_RANGE, X_RANGE, num=301)

BOUNDS = [[PARAMS['bound_low'] for i in range(PARAMS['num_x'])],
          [PARAMS['bound_high'] for i in range(PARAMS['num_x'])]]
SWARM = pso.Swarm(20, PARAMS['num_x'], fitness, BOUNDS)
SWARM.run_anim(1000)
PLT = plot_data(SWARM.best[0])
PLT.show()
