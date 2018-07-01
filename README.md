# A patricle swarm optimisation approach to finding approximate inverse Weierstrass Transforms

Given a function G(A), find f(x) such that W[f(x)] = G(A) (where W is the Weierstrass Transform)

## weierstrass.py
The python3 program weierstrass.py will find approximate solutions for the inverse Weierstrass Transform.
The function target_function should be edited to represent G(A), all other parameters should be edited in
the config file params.cfg.

By default weierstrass.py will attempt to find approximations for f(x) when G(A) = tanh(0.45\*A). There are
three running options at the bottom of the file:

### 1) Run verbose, no visualisations (fastest)
Will run the particle swarm optimiser with no visualisations, outputting only the percent completion.
This can be further sped up by choosing verbose=False.

### 2) Run with running history (slow)
Runs the optimiser outputting a running history of the best fitness of the swarm. The overhead of plotting
a graph every iteration makes this significantly slower than option 1. However it is useful for visualising
the progress of the optimiser and running tests.

### 3) Run with running history and best particle (slowest)
Same as option 2 but also outputs a plot with the best f(x) found so far. 

## params.cfg
This is the main parameter file that should be adjusted before running weierstrass.py.

### Description of the parameters

#### HYPERPARAMS

Contains the hyperparameters for the particle swarm optimiser. The default values should suffice for most cases,
however experimenting with different values is encouraged to find the best values for a specific problem.

omega = 0.9

phi_p = 0.7

phi_g = 0.7

#### SWARM

Contains parameters for the swarm itself.

SEED = 12 # Random seed for reproducability

N_PARTICLES = 20 # Number of particles in the swarm

N_STEPS = 200  # Number of steps the swarm takes

BOUND_LOW = 0 # lower bound for the particles

BOUND_HIGH = 2 # upper bound for the particles

#### WEIERSTRASS

Conatains parameters specific to the Weierstrass problem.

A_RANGE = 20.0 # range of A values over which we approximate

CUTOFF = 4 # range over which the gaussian is evaluated

NUM_X = 8 # number of points in the spline

NUM_A = 20 # number of points over which we evaluate integrals

PARITY = odd # parity of target function (odd or even)

DISTRIBUTION = square # how the spline points are distributed

#### TYPES
The 'types' parameters encode how python should read in the above values and should not need to be changed 

