""" 
Module to set up run time parameters for Clawpack.

The values set in the function setrun are then written out to data files
that will be read in by the Fortran code.
    
""" 

import os
from pyclaw import data 
from math import pi

#------------------------------
def setrun(claw_pkg='classic'):
#------------------------------
    
    """ 
    Define the parameters used for running Clawpack.

    INPUT:
        claw_pkg expected to be "classic" for this setrun.

    OUTPUT:
        rundata - object of class ClawRunData 
    
    """ 
   
    # Needs classic clawpack in order to run  
    assert claw_pkg.lower() == 'classic',  "Expected claw_pkg = 'classic'"
   
    # Number of spacial dimensions
    ndim = 2
    rundata = data.ClawRunData(claw_pkg, ndim)

    probdata = rundata.new_UserData(name='probdata',fname='setprob.data')

    # Using the Crank-Nicolson method of iteration
    probdata.add_param('implicit_integration_scheme', 'Crank-Nicolson')

    ''' 
    Note: Uses Crank Nicolson to formulate each iteration (timestep),
    but within each of those iterations, converges nonlinear 
    equations using Newton's method (uses linear solver if timestep
    gives linear equations).
    '''

    # Maximum of newton_max_iter iterations per timestep
    probdata.add_param('newton_max_iter', 30)
    # Tolerance indicates maximum diff between 2 iterations before
    # computer determines that timestep has converged
    probdata.add_param('newton_tolerance', 1e-4)
    # Amount of information outputted (for debugging purposes)
    probdata.add_param('newton_verbosity', 2)

    # Same but for linear solver
    probdata.add_param('linear_solver_tolerance', 1e-4)
    probdata.add_param('linear_solver_verbosity', 1)

    # Number of threads used if possible (if on a multicore machine)
    probdata.add_param('num_threads', 4)

    '''
    Possible variables:
    'p' = periodic boundary conditions, which means that when the flow
    exits through one boundary, it reenters through the other one. This
    must be coordinated between upper and lower ends of the domain.
    
    'n' = none, which sets the boundary cells first and third 
    derivatives to zero.

    '0' or '1' = one derivative is specified (kept constant) at each
     boundary interface, with the string specifying the order of the
     derivative.

    '01' '03' '23' etc. = two derivatives are specified at each boundary
    interface, again with the string specifying which two.

    The 4 arguments in film/surfactant_bc_options are the 4 walls, in
    some (?) order with east/west first, north/south last. FIND?
    '''

    probdata.add_param('film_bc_options', ['13', '13', '13', '13'])
    probdata.add_param('surfactant_bc_options', ['1', '1', '1', '1'])
    
    probdata.add_param('beta', 0.42, 'gravitational constant')  # Estimated value: beta=.271
    probdata.add_param('kappa', 0.019, 'capillarity')  # Estimated value: kappa=.013
    probdata.add_param('delta', 3*10**(-5), 'surfactant diffusivity')
    probdata.add_param('mu', 1.25,  'surface tension parameter: sigma = (1+mu*Gamma)**(-3)')
    
    # IS THIS BEING USED? ALSO, TYPO?
    probdata.add_param('right_fllm_height', 0.05)
    
    
    clawdata = rundata.clawdata  # initialized when rundata instantiated

    clawdata.ndim = ndim
    clawdata.meqn = 2 #number of equations
    clawdata.maux = 4 #number of auxiliary things (?)
    clawdata.mcapa = 0

    # Initiating the domain
    clawdata.xlower = -pi 
    clawdata.xupper = pi    
    clawdata.ylower = -pi
    clawdata.yupper = pi
    clawdata.mx = 400 # number of gridpoints (or cells, not sure)
    clawdata.my = 400
    
    # Setting timestep information
    clawdata.t0 = 0.0
    clawdata.dt_initial = .001 # WHY SO SMALL?
    clawdata.dt_variable = 0 # 0 or 1 if can vary or not
    clawdata.tfinal = 1.0
    clawdata.nout = 50 # Either number of timesteps output 
    # or every nout, output timestep (check later)

    clawdata.verbosity = 1
    clawdata.restart = 1 # WHAT IS THIS?
    #clawdata.N_restart = 50
    
    # Maximum number of timesteps to allow between output times:
    clawdata.max_steps = 10000 # CHECK

    clawdata.src_split = 1 
    clawdata.mbc = 2 # Something about boundary conditions (?)
    
    return rundata


if __name__ == '__main__':
    # Set up run-time parameters and write all data files.
    import sys
    if len(sys.argv) == 2:
	rundata = setrun(sys.argv[1])
    else:
	rundata = setrun()

    rundata.write()
    
