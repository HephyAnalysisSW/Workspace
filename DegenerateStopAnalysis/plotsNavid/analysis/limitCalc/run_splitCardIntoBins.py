import sys,os
import subprocess
from optparse import OptionParser
import glob

from limitTools import *

call_script = "splitCardIntoBins.py"


#
# any options needed for this script?
#
parser = OptionParser()
(options,args) = parser.parse_args()
#
# parse input files
#

# the systs will be read from these cards
input_cards = glob.glob(args[0])


if not input_cards:
    raise Exception("no cards found: %s"%cards_with_sys)


#
# outdir
#
output_dir = args[1]






for card in input_cards:
    command = ["python",call_script, card ,output_dir]
    subprocess.call(command)
    
    
