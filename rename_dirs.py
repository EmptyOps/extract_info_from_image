import argparse

import sys, os
import json
from numpy import array
import numpy as np
from glob import glob


# Instantiate the parser
parser = argparse.ArgumentParser(description='a rename util ')

# verbose
parser.add_argument('--verbose', action='store_true',
                    help='A boolean True False')

# 
parser.add_argument('--input_dir', type=str, 
                    help='An input_dir, must be provided')
                    
args = parser.parse_args()
print(args)
    
dirs = glob( args.input_dir + "/*/" )
print(dirs)

#rename spaces     
for dir in dirs:
    actual_dir = os.path.basename(os.path.dirname(dir))

    os.rename( dir, os.path.join( args.input_dir, actual_dir.replace(" ", "___") ) )
    
