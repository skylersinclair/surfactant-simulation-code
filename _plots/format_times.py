"""
Program to take the results from running the simulator and format them
so that they nicely work with matlab.

Will generally be called as "python format_times.py _output/fort.t*"
As such, if called with no arguments, it will search for files matching
'fort.t*' or '_output/fort.t*'.

Author: Eric A. Autry (adapted from format_forts.py)
Date: 06/22/2011
"""

import sys

def readDataFile(datafile, frame_num):
    """
    frame_num: the 4-digit number for which frame this is.  It is a string.
    """
    
    "Load data from file."
    params = {}
    gotparams = False
    while not gotparams:
        line = datafile.readline()
        if not line:
            error("No data in file '%s'." % (datafile.name))
        line = line.strip()
        if not line:
            gotparams = True
        else:
            val, param = line.split()
            # Values tend to be either floats or ints.
            try:
                if "e+" in val.lower() or "e-" in val.lower():
                    val = float(val)
                else:
                    val = int(val)
            except:
                warning("Couldn't determine type for value '%s'." % (val))
            params[param] = val
    time = params["time"]
    
    # Now put the data into matlab friendly format and put it into output
    output = "time" + frame_num + " = " + str(time) + ";"
    return output

def main(argv):
    "Actually run the program."
    if len(argv) < 2:
        print "Usage:"
        print "python format_forts.py <data file>"
        return 1
    for fname in argv[1:]:
        f = file(fname, "r")
        try:
            output = readDataFile(f, fname[-4:])
        finally:
            f.close()
        new_name = "t" + fname[-4:] + ".m"
        f_write = file(new_name, "w")
        f_write.write(output)
        f_write.close()
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
