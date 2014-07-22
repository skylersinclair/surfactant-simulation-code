surfactant-simulation-code
==========================

This repository contains simulation initial condition and output processing code for the 
clawpack-4.6.3 implicit_solvers 2d surfactant code. It is comparable to the Surfactant folder
in the claridge/implicit_solvers directory, but it has been customized to fit the needs of the
Harvey Mudd reseach group.

The main differences are as follows:

qinit.90 now contains code to model the inward/outward spreading surfactant case. Set the desired
concentrations (as fractions of gamma_c) as the INSIDE and OUTSIDE variables at the top of the code.
The ring is considered to be at radius r = 1. Only when you re-dimensionalize will the actual radius
of the ring be taken into account.

surface_tension_utils.f90 now contains an experimentally derived equation of state, along with the 
multilayer and linear equations. 

setrun.py is now substantially more commented for easier reading.

_plots now contains format_forts.py and format_times.py to convert output into MATLAB files.

For more details on how to use the simulations, contact the Levy Lab at Harvey Mudd.
