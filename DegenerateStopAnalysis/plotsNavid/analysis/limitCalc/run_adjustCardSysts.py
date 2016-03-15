import sys,os
import subprocess
from optparse import OptionParser
import glob

from limitTools import *

call_script = "adjustCardSysts.py"


#
# any options needed for this script?
#
parser = OptionParser()
(options,args) = parser.parse_args()
#
# parse input files
#

# the systs will be read from these cards
cards_with_sys = glob.glob(args[0])

# rates will be read from this card
cards_with_rates = glob.glob(args[1])

if not cards_with_sys:
    raise Exception("no cards found: %s"%cards_with_sys)
if not cards_with_rates:
    raise Exception("no cards found: %s"%cards_with_rates)


#
# outdir
#
output_dir = args[2]






no_match=0
no_match_list = []
no_match_list_rates= cards_with_rates
for scard in cards_with_sys:
    scard_name = get_filename(scard)       

    scard_masses = getMasses(scard) 
    matches = [ rcard for rcard in cards_with_rates if getMasses(rcard)==scard_masses ]

    assert len(matches) <= 1, "Multiple matches for %s , ie %s"%(scard, matches)

    if len(matches)==0:
        print "No matches found for %s"%scard
        no_match_list.append(scard)
        no_match +=1
        continue
    match = matches[0]
    no_match_list_rates.pop(no_match_list_rates.index(match))


    command = ["python",call_script,scard,match,output_dir]

    subprocess.call(command)

    #print scard, match
    
    
