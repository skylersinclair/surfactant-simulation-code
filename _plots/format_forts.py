"""
Program to take the results from running the simulator and format them
so that they nicely work with matlab.

Will generally be called as "python format_forts.py _output/fort.q*"
As such, if called with no arguments, it will search for files matching
'fort.q*' or '_output/fort.q*'.

Author: Eric A. Autry assisted by Greg Kronmiller
Date: 06/15/2011
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
    dx = params["dx"]
    dy = params["dy"]
    mx = params["mx"]
    my = params["my"]
    xlow = params["xlow"]
    ylow = params["ylow"]
    xhigh = xlow + mx*dx
    yhigh = ylow + my*dy
    
    # Now put the data into matlab friendly format
    height_vals = "["
    surf_con_vals = "["
    for line in datafile:
        if line.strip():
            vals = line.split()
            height_vals += vals[0] + " "
            surf_con_vals += vals[1] + " "
        else:
            height_vals += ";\n"
            surf_con_vals += ";\n"
    height_vals += "]"
    surf_con_vals += "]"
    
    # Create x_vec and y_vec
    x_vec = "["
    y_vec = "["
    for i in range(mx):
        new_x = xlow + (.5 * dx) + (i * dx)
        x_vec += str(new_x) + " \n"
    for j in range(my):
        new_y = ylow + (.5 * dy) + (j * dy)
        y_vec += str(new_y) + " \n"
    
    # Now put it all together nicely
    output = "height_mat" + frame_num + " = " + height_vals + \
             ";\nsurf_mat" + frame_num + " = " + surf_con_vals + \
             ";\nx_vec = " + x_vec + "];\ny_vec = " + y_vec + \
             "];\nxmin = " + str(xlow) + ";\nxmax = " + str(xhigh) + \
             ";\nymin = " + str(ylow) + ";\nymax = " + str(yhigh) + ";"
    return output

def main(argv):
    "Actually run the program."
    if len(argv) < 2:
        print "Usage:"
        print "python format_forts.py <data file>"
        return 1
    tot_num_frames = 0
    for fname in argv[1:]:
        f = file(fname, "r")
        try:
            output = readDataFile(f, fname[-4:])
        finally:
            f.close()
        new_name = "frame" + fname[-4:] + ".m"
        f_write = file(new_name, "w")
        f_write.write(output + "\nframe_num = " + fname[-4:] + ";")
        f_write.close()
        tot_num_frames += 1
    tnf = file("tnf.m", "w")
    tnf.write("tot_num_frames = " + str(tot_num_frames) + ";")
    tnf.close()
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
