#!/usr/bin/env python
"""
usage:
./calcLimit.py "path/to/card/pattern" path/to/output/pickle.pkl
usage: ./calc_cards_limit.py "../cutbased/cards/reload_scan_2200pbm1/Reload_Inc_T2_4bd*" ../cutbased/pkl/RunII_Reload_Scan_Limits_2260.pkl
"""


import glob
import os 


import pickle
import json

from optparse import OptionParser

import Workspace.DegenerateStopAnalysis.tools.limitTools as limitTools
import Workspace.DegenerateStopAnalysis.tools.degTools as degTools


getFileName  = lambda f : os.path.splitext( os.path.basename(f) )[0] 

def calcLimitAndStoreResults( card, output_dir = "./", output_name = None, exts =["pkl", "json"] ):
    res = limitTools.calcLimit( card )
    card_file_name = getFileName(card)
    if not output_name:
        output_name = "Limit_" + card_file_name  
    output_file = output_dir +"/" + output_name 
    for ext in exts:
        if ext=="pkl":
            pickle.dump( res, file( output_file +"."+ext, "w" ) )
            print "limit results for card %s, stored in %s"%(card_file_name , output_file+"."+ext)
        elif ext=="json":
            json.dump( res, file( output_file +".json", "w" ) , indent = 4)
            print "limit results for card %s, stored in %s"%(card_file_name , output_file+"."+ext)
        else:
            raise Exception("Output extention not recognized")
    return card_file_name, output_file+".pkl",  res
    



if __name__ == '__main__':



    parser = OptionParser()
    (options,args) = parser.parse_args()
    
    
    
    card_pattern = args[0]
    if len(args) > 1:
        output_dir   = args[-1]
        if not output_dir.endswith("/"):
            raise Exception("Last argument should be the output directory ending with '/' but it  is %s"%output_dir)
        degTools.makeDir(output_dir)
    else:
         output_dir = "./"
    
    
    print card_pattern
    cards  = glob.glob(card_pattern)
    
    if not cards:
        raise Exception("No Cards Found with the pattern: %s"%card_pattern)
    
    


    single_card = len(cards)==1


    print "Found %s Cards"%len(cards)
    
 
    make_script = not single_card 
    if make_script:
        fname = "calc_limits_all.sh"
        f = open( fname, "w")
        f.write("##\n")
    for card in cards:
        if make_script:
            command = "./calcLimit.py {card}  {output_dir}".format(card=card, output_dir = output_dir) 
            f.write(command)
            f.write("\n")
        else:
            print ""
            card_file_name, output_file, res = calcLimitAndStoreResults( card, output_dir = output_dir, output_name = None)
    if make_script:
        print "\n \n Script to be run: %s "%fname
        batchcommand = "submitBatch.py %s   --title=Limits"%fname
        print batchcommand
        f.close()


    if False: 
        limits = {}
        for card, limit in results:
            print card
            mstop, mlsp = getMasses(card)
            try: 
                limits[mstop]
            except KeyError:
                limits[mstop]={}
            limits[mstop][mlsp] = limit 
            
            
        
        
        
        
        if pkl_out.endswith(".pkl"):
            pass
        else:
            pkl_out +=".pkl"
        json_out = pkl_out.replace(".pkl",".json")
        
        print limits
        
        
        pickle.dump(limits,open(pkl_out,"w"))
        json.dump(limits, open(json_out,"w") , indent = 4)
        print "json and pickle written in  \n %s  \n %s"%(pkl_out, json_out)

