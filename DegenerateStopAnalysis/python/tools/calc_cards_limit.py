#!/usr/bin/env python
"""
usage:
./calc_cards_limit.py "path/to/card/pattern" path/to/output/pickle.pkl
usage: ./calc_cards_limit.py "../cutbased/cards/reload_scan_2200pbm1/Reload_Inc_T2_4bd*" ../cutbased/pkl/RunII_Reload_Scan_Limits_2260.pkl
"""


import glob
import os 

#from Workspace.DegenerateStopAnalysis.tools.limitTools import  getLimit, plotLimits, calcLimitFromCard

import pickle
import json

from optparse import OptionParser

from Workspace.DegenerateStopAnalysis.tools.limitTools import *
#from HiggsAnalysis.CombinedLimit.DatacardParser import *
import multiprocessing

parser = OptionParser()
(options,args) = parser.parse_args()



card_pattern = args[0]
pkl_out = args[-1]
if not pkl_out.endswith(".pkl"):
    raise Exception("Last argument should be the pickle output ending with .pkl but instead it is %s"%pkl_out)

nProc = args[-2] if type(args[-2]) == int else 15


print card_pattern
cards  = glob.glob(card_pattern)

if not cards:
    raise Exception("No Cards Found with the pattern: %s"%card_pattern)


print "Found %s Cards"%len(cards)

#get_mass = lambda card: os.path.splitext( os.path.basename(card) )[0]
#masses = getMasses(card)





if __name__ == '__main__':






    def calcLimitFromCard(card):
        return (card, calcLimit(card))

    ######################################## MULTIPROCESS ##################################
    pool    =   multiprocessing.Pool( processes = nProc )
    results = pool.map( calcLimitFromCard, cards )
    pool.close()
    pool.join()
    ######################################## MULTIPROCESS ##################################


    limits = {}
    for card, limit in results:
        mstop, mlsp = getMasses(card)
        try: 
            limits[mstop]
        except KeyError:
            limits[mstop]={}
        #limits[mstop][mlsp] = [card, limit,]
        limits[mstop][mlsp] = limit 
        
        
    
    
        #limits[mstop][mlsp] = calcLimitFromCard( card , name="",mass="")
        #limits[mstop][mlsp] = calcLimitFromCard( card , name="",mass="%s%s"(mstop,mlsp))
    
        #print type(mstop),type(mlsp), limits[mstop][mlsp]
        #1medianLimits[lumi]=limits[lumi]["50.0"]
    
    
    if pkl_out.endswith(".pkl"):
        pass
    else:
        pkl_out +=".pkl"
    json_out = pkl_out.replace(".pkl",".json")
    
    print limits
    
    
    pickle.dump(limits,open(pkl_out,"w"))
    json.dump(limits, open(json_out,"w") , indent = 4)
    print "json and pickle written in  \n %s  \n %s"%(pkl_out, json_out)

