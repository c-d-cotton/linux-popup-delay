#!/usr/bin/env python3
# PYTHON_PREAMBLE_START_STANDARD:{{{

# Christopher David Cotton (c)
# http://www.cdcotton.com

# modules needed for preamble
import importlib
import os
from pathlib import Path
import sys

# Get full real filename
__fullrealfile__ = os.path.abspath(__file__)

# Function to get git directory containing this file
def getprojectdir(filename):
    curlevel = filename
    while curlevel is not '/':
        curlevel = os.path.dirname(curlevel)
        if os.path.exists(curlevel + '/.git/'):
            return(curlevel + '/')
    return(None)

# Directory of project
__projectdir__ = Path(getprojectdir(__fullrealfile__))

# Function to call functions from files by their absolute path.
# Imports modules if they've not already been imported
# First argument is filename, second is function name, third is dictionary containing loaded modules.
modulesdict = {}
def importattr(modulefilename, func, modulesdict = modulesdict):
    # get modulefilename as string to prevent problems in <= python3.5 with pathlib -> os
    modulefilename = str(modulefilename)
    # if function in this file
    if modulefilename == __fullrealfile__:
        return(eval(func))
    else:
        # add file to moduledict if not there already
        if modulefilename not in modulesdict:
            # check filename exists
            if not os.path.isfile(modulefilename):
                raise Exception('Module not exists: ' + modulefilename + '. Function: ' + func + '. Filename called from: ' + __fullrealfile__ + '.')
            # add directory to path
            sys.path.append(os.path.dirname(modulefilename))
            # actually add module to moduledict
            modulesdict[modulefilename] = importlib.import_module(''.join(os.path.basename(modulefilename).split('.')[: -1]))

        # get the actual function from the file and return it
        return(getattr(modulesdict[modulefilename], func))

# PYTHON_PREAMBLE_END:}}}

import subprocess
import time

def main(minutes, mutesound = False, blanklines = None):
    """
    minutes is number of minutes before show popup
    mutesound means mute sound when show popup
    blanklines is number of blanklnes to leave below each minute update (so that I avoid seeing how many minutes remaining)
    """
    if blanklines is None:
        blanklines = 0

    while minutes > 0:
        print('Minutes remaining: ' + str(minutes) + '.' + ' Time: ' + time.strftime('%H:%M') + '.')
        print('\n'.join(['Blank line. Code still running.'] * blanklines))
        time.sleep(60)
        minutes = minutes - 1

    if mutesound is True:
        subprocess.call(['amixer', 'set', 'Master', 'mute'])
    importattr(__projectdir__ / Path('submodules/linux-popupinfo/displaypopup_func.py'), 'genpopup_basic')('COMPLETED: ' + str(minutes) + '.', title = 'Finished Work')


def main_ap():
    #Argparse:{{{
    import argparse
    
    parser=argparse.ArgumentParser()
    parser.add_argument("minutes", type = int)
    parser.add_argument("-m", "--mutesound", action = 'store_true')
    parser.add_argument("-b", "--blanklines", type = int)
    
    args=parser.parse_args()
    #End argparse:}}}

    main(args.minutes, mutesound = args.mutesound, blanklines = args.blanklines)
