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

def target_function(t):
    '''
        The Target function of which to find the
        inverse Weierstrass transform
    '''
    f = np.tanh(t*0.45)
    return f


def extend_odd(y, parity):
    '''Creates an odd extention of an array'''
    if parity == 'even':
        y = y[1:]
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
        y_ext = extend_odd(points, PARAMS['parity'])
    elif PARAMS['parity'] == 'even':
        y_ext = extend_even(points)
    else:
        y_ext = points
    if PARAMS['parity'] == 'odd' or PARAMS['parity'] == 'even':
        x_ext = extend_odd(x, PARAMS['parity'])
    else:
        x_ext = x

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


def plot_data(pos, axis):
    '''
        Converts a list of spline points (pos) to its
        spline representation and plots the resulting curve.
    '''
    y = pos
    if PARAMS['parity'] == 'odd':
        y_ext = extend_odd(y, PARAMS['parity'])
    elif PARAMS['parity'] == 'even':
        y_ext = extend_even(y)

    x_ext = extend_odd(x, PARAMS['parity'])
    spline_data = splrep(x_ext, y_ext)

    axis.plot(x, y, 'o', X_FINE, splev(X_FINE, spline_data),
              '-', color='black')

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
    return


def convert_config_types(config, name):
    '''
        Converts the config entries to the appropriate type.
    '''
    params = dict(config[name])
    types = dict(config[name+'_TYPES'])
    for key in params:
        if types[key] == 'int':
            params[key] = int(params[key])
        elif types[key] == 'float':
            params[key] = float(params[key])
    return params

CONFIG = configparser.ConfigParser()
CONFIG.read('params.cfg')
PARAMS = convert_config_types(CONFIG, 'WEIERSTRASS')

if PARAMS['parity'] == 'odd' or PARAMS['parity'] == 'even':

    X_RANGE = PARAMS['a_range'] + PARAMS['cutoff']
    if PARAMS['parity'] == 'odd':
        NUM = PARAMS['num_x'] + 1
    else:
        NUM = PARAMS['num_x']
    if PARAMS['distribution'] == 'square':
        x = np.linspace(0, 1, num=NUM)**2 * X_RANGE
    else:
        x = np.linspace(0, 1, num=NUM) * X_RANGE

    if PARAMS['parity'] == 'odd':
        x = x[1:]

    A = np.linspace(-PARAMS['a_range'], PARAMS['a_range'],
                    num=PARAMS['num_a'])

    X_FINE = np.linspace(-X_RANGE, X_RANGE, num=301)

TARGET = target_function(A)

SWARM_PARAMS = convert_config_types(CONFIG, 'SWARM')

random.seed(SWARM_PARAMS['seed'])

BOUNDS = [[SWARM_PARAMS['bound_low'] for i in range(PARAMS['num_x'])],
          [SWARM_PARAMS['bound_high'] for i in range(PARAMS['num_x'])]]

SWARMS = [pso.Swarm(SWARM_PARAMS['n_particles'], PARAMS['num_x'],
                    fitness, BOUNDS) for i in range(20)]

if __name__ == '__main__':
    MULTISWARM = pso.MultiSwarm(SWARMS)
    MULTISWARM.run_multiswarm(100, 4)

    fig, ax = plt.subplots()
    for swarm in MULTISWARM.swarms:
        ax.plot(swarm.history)
    ax.semilogy()
    plt.show()

# #1) Run without any visualisation (fastest)
# SWARM.run(SWARM_PARAMS['n_steps'], verbose=True)
# fig, axis = plt.subplots()
# plot_data(SWARM.best[0], axis)
# plt.show()

# #2) Run with fitness history visualisation (slower)
# SWARM.run_anim(SWARM_PARAMS['n_steps'])
# fig, axis = plt.subplots()
# plot_data(SWARM.best[0], axis)
# plt.show()

# #3) Run with fitness history visualisation and running best (slowest)
# SWARM.run_anim(SWARM_PARAMS['n_steps'], plot_best=plot_data)
# FIG, AXIS = plt.subplots()
# plot_data(SWARM.best[0], AXIS)
# plt.show()
