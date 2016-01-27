#!/usr/bin/python
"""
Runs iraf commands from the command line, opening ds9 if needed. Example:
exiraf.py imstat galaxy.fits[25:50,25:50]

For commands in subpackages, supply the full package tree in period-separated format:
exiraf.py noao.obsutil.psfmeasure @images.list size=MFWHM

Will attempt to execute ds9 for commands that need it, add additional commands to ds9tasks variable
"""

import sys
import subprocess

if len(sys.argv) < 2:
    print(__doc__)
    exit(1)

# if(not os.path.exists("./login.cl") or not os.path.exists("./pyraf/") or 
# 	not os.path.exists("./uparm/")):
# 	subprocess.call("mkiraf", shell=True)

## TODO: Handle spawning ds9 display more properly than a simple list? How to
# tell if we need it?
# ds9tasks = ["noao.obsutil.psfmeasure", "imexamine"]

# for task in ds9tasks:
#     if (task.find(sys.argv[1]) == 0):
subprocess.call("ds9 &", shell=True)

## The import call actually sets up the iraf environment, so gotta do it after
## calling mkiraf and starting ds9 (stupid, stupid iraf)
from pyraf import iraf

## TODO: Make sure this splitting is robust
if ("." in sys.argv[1]):
    pkgs = sys.argv[1].split(".")
    for pkg in pkgs[:len(pkgs) - 1]:
        # Suppress printing package contents
        irafcmd = "iraf." + pkg + "(_doprint=0)"
        exec (irafcmd)

## Quote arguments supplied on cmd line
cmdargs = sys.argv[2:] if len(sys.argv) > 2 else [""]
for i, arg in enumerate(cmdargs):
    if ("=" in arg):
        cmdargs[i] = "=\"".join(arg.split("=")) + "\""
    else:
        cmdargs[i] = "\"" + arg + "\""

irafcmd = "iraf." + sys.argv[1] + "(" + ", ".join(cmdargs) + ")"
exec(irafcmd)