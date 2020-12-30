#!/usr/bin/env python3
import os
from pathlib import Path
import sys

__projectdir__ = Path(os.path.dirname(os.path.realpath(__file__)) + '/')

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
    sys.path.append(str(__projectdir__ / Path('submodules/linux-popupinfo/')))
    from displaypopup_func import genpopup_basic
    genpopup_basic('COMPLETED: ' + str(minutes) + '.', title = 'Finished Work')


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
