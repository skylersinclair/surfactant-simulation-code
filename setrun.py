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
    # 0 is no output, 1 is some output, 2 is maximum output.
    probdata.add_param('newton_verbosity', 2)

    # Same but for linear solver
    probdata.add_param('linear_solver_tolerance', 1e-4) # Error in solution for linear system
    probdata.add_param('linear_solver_verbosity', 1)

    # Number of threads used if possible (if on a multicore machine)
    probdata.add_param('num_threads', 4)

    '''
    Possible variables:
    'p' = periodic boundary conditions, which means that when the flow
    exits through one boundary, it reenters through the other one. This
    must be coordinated between upper and lower ends of the domain.
    
    If you enter in 'p' for the x_lower and y_lower, it will ignore
    x_upper and y_upper and make the boundary periodic. However, you
    should still set both upper and lower to 'p' for the sake of clarity.
    
    Don't use n
    'n' = none, which sets the boundary cells first and third 
    derivatives to zero.

    '0' or '1' = one derivative is specified (kept constant) at each
     boundary interface, with the string specifying the order of the
     derivative.

    '01' '03' '23' etc. = two derivatives are specified at each boundary
    interface, again with the string specifying which two.
    
    The four argument orders are(specifying the four boundary condition walls):
    [x_lower, x_upper, y_lower, y_upper]
    
    0 means the function value (0th derivative)
    
    builtin_bc_routines.f90 in implicit_solvers/implicit_claw_2d is where
    the boundary conditions actually get set
    
    You can set the value of the derivatives you're keeping constant in
    set_implicit_boundary_conditions.f90 (in the Surfactant folder)
    '''

    probdata.add_param('film_bc_options', ['13', '13', '13', '13'])
    probdata.add_param('surfactant_bc_options', ['1', '1', '1', '1'])
    
    probdata.add_param('beta', 1.2, 'gravitational constant')  # Estimated value: beta=.271
    probdata.add_param('kappa', 0.0066, 'capillarity')  # Estimated value: kappa=.013
    probdata.add_param('delta', 0.00032, 'surfactant diffusivity')
    probdata.add_param('mu', 1.33,  'surface tension parameter: sigma = (1+mu*Gamma)**(-3)') # material parameter eta = sigma s/(sigma 0 - sigma s)
    
    # IS THIS BEING USED? ALSO, TYPO? -> Fixed from right_fllm_height to right_film_height
    # If changing conditions in qinit, could pass right_film_height to qinit
    # probdata.add_param('right_film_height', 0.05)
    
    
    clawdata = rundata.clawdata  # initialized when rundata instantiated

    clawdata.ndim = ndim
    clawdata.meqn = 2 #number of equations
    clawdata.maux = 4 #number of auxiliary variables in the problem (beta,kappa,delta,mu)
    clawdata.mcapa = 0 # not used (index of the aux array something complicated look at documentation)

    # Initiating the domain
    clawdata.xlower = -pi 
    clawdata.xupper = pi    
    clawdata.ylower = -pi
    clawdata.yupper = pi
    clawdata.mx = 400 # number of cells, NOT gridpoints
    clawdata.my = 400
    
    # Setting timestep information
    clawdata.t0 = 0.0
    clawdata.dt_initial = .0002 # WHY SO SMALL?
    clawdata.dt_variable = 0 # 0 or 1 if can vary or not. Timestepping done in implicit_claw/2d/src2 
    # Look at max_time_step_splits in src2 change to 5ish (rather than 0). Can maybe put to aux array
    # in setrun.py, if want to fight with fortran.
    clawdata.tfinal = 40.0
    clawdata.nout = 320 # Either number of timesteps output 
    # or every nout, output timestep (check later)

    clawdata.verbosity = 1
    clawdata.restart = 1 # Lets you restart from old data
    #clawdata.N_restart = 50 # Restart frame. Might work now, I'll check. Look at documentation.
    
    # Maximum number of timesteps to allow between output times:
    clawdata.max_steps = 10000 # CHECK

    # Source split is the method it uses to do operator splitting
    # 1 inditcates 1st order splitting (Godunov)
    # 2 indicates 2nd order splitting (Strang)(more work but sometimes more accurate)
    clawdata.src_split = 1 
    clawdata.mbc = 2 # Number of ghost cells on boundary needed (need 2 for 4th order terms)
    
    return rundata


if __name__ == '__main__':
    # Set up run-time parameters and write all data files.
    import sys
    if len(sys.argv) == 2:
	rundata = setrun(sys.argv[1])
    else:
	rundata = setrun()

    rundata.write()
    
