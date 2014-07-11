# .bashrc

# User specific aliases and functions

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

#Change shell prompt to FLASHING PURPLE DINNER!
#export PS1='\e[5;35m[Dinner \W]\$ \e[m '

#Boring old way of doing things (but still has purple yay)
export PS1='\e[1;35m[\u@\h \W]\$ \e[m '

#Shortcut directories for convenience
export SURF='clawpack-4.6.3/implicit_solvers/applications/2d/Surfactant'

#Setting up for simulations
export PATH=/shared/local/sw/gcc/gcc-4.8.2/bin:/shared/local/sw/python/python-2.7/bin:$PATH
export LD_LIBRARY_PATH=/shared/local/sw/gcc/gcc-4.8.2/lib64:$LD_LIBRARY_PATH
source ~/clawpack-4.6.3/setenv.bash
source ~/clawpack-4.6.3/implicit_solvers/setenv.bash
#Code used to process data and turn it into usable MATLAB files
#Use in _plots folder after simulation runs
export FORT='python format_forts.py ../_output/fort.q*'
export TIME='python format_times.py ../_output/fort.t*'

#source setenv.bash
