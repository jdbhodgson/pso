# A patricle swarm optimisation approach to finding approximate inverse Weierstrass Transforms

Givea a function f(a), find G(x) such that W[G(x)] = f(a) (where W is the Weierstrass Transform)

## weierstrass.py
The python3 program weierstrass.py will find approximate solutions for the inverse Weierstrass Transform.
The function target_function should be edited to represent f(a), all other parameters should be edited in
the config file params.cfh

## params.cfg
This is the main parameter file that should be adjusted before running weierstrass.py.
### Description of the parameters\n
[HYPERPARAMS]  
Contains the hyperparameters for the particle swarm optimiser. The default values should suffice for most cases,
however experimenting with different values is encouraged to find the best values for a specific problem.\n
omega = 0.9\n
phi_p = 0.7\n
phi_g = 0.7\n

[SWARM]\n
Contains parameters for the swarm itself.\n
SEED = 12 # Random seed for reproducability\n
N_PARTICLES = 20 # Number of particles in the swarm\n
N_STEPS = 200  # Number of steps the swarm takes\n
BOUND_LOW = 0 # lower bound for the particles\n
BOUND_HIGH = 2 # upper bound for the particles\n

[WEIERSTRASS]
Conatains parameters specific to the Weierstrass problem.
A_RANGE = 20.0 # range of A values over which we approximate
CUTOFF = 4 # range over which the gaussian is evaluated
NUM_X = 8 # number of points in the spline
NUM_A = 20 # number of points over which we evaluate integrals
PARITY = odd # parity of target function (odd or even)
DISTRIBUTION = square # how the spline points are distributed

The 'types' parameters encode how python should read in the above values and should not need to be changed 
[WEIERSTRASS_TYPES]
A_RANGE = float
CUTOFF = float
NUM_X = int
NUM_A = int
PARITY = str
DISTRIBUTION = str

[SWARM_TYPES]
SEED = int
N_PARTICLES = int
N_STEPS = int
BOUND_LOW = float
BOUND_HIGH = float
