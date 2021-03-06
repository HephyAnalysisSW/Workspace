#!/bin/env python


########################################################################
## file: update_header.py                                             ##
##                                                                    ##
## description: Update the header of LHE files to include all needed  ##
##              SLHA information to do subsequent decays.             ##
##              This includes updating the MASS and DECAY blocks.     ##
##                                                                    ##
## Input is a configuration file that specifies all the actions that  ##
## will be taken. Please refer to create_update_header_config.py for  ##
## more information on how to construct a proper config file.         ##
##                                                                    ##
## There is a flag --stableLSP which should be used when you want a   ##
## stable LSP, and the original LHE file does not have this in the    ##
## header yet.                                                        ##
##                                                                    ##
## Author: Nadja Strobbe                                              ##
## Created: 2014-12-02                                                ##
## Updated: ...                                                       ##
##                                                                    ##
########################################################################

import sys, os, glob, re
import gzip
import argparse
import ConfigParser
import math
import shutil 
## ---------------------------------------------------------------------
##  Process the lhe file with name 'infilename', and save it to a file
##  with name 'outfilename'. The masses to be replaced are specified in
##  'masses_to_replace'. This should be a dictionary of the form
##  {particle pdgId : mass}
##  The decay info should be the full decay block that needs to be 
##  inserted.
##  the stop_mixing_matrix should be of the form:
##  matrix =  {'1': {'1': F11,
##                   '2': F12 },
##             '2': {'1': F21,
##                   '2': F22 }}
##
##  Please note that overriding branching fractions that are present in 
##  the original lhe, does not work yet.
## ---------------------------------------------------------------------

def update_header(infilename, outfilename, masses, decay_info, nevents, modeltag, stop_mixing_matrix):
    if infilename.endswith(".lhe.gz"):
        infile = gzip.open(infilename)
    elif any([infilename.endswith(suffix) for suffix in ['.lhe','.dat','.txt']]):
        infile = open(infilename)
    else: 
        sys.exit("LHE files should have extension .lhe or .lhe.gz")
    outfile = open(outfilename,'w')

    lastblock = ""
    in_ev = False
    nev = 0
    for line in infile: 
        if "BLOCK" in line:
            lastblock = line
        newline = line
        if "MASS" in lastblock:
            for particle,mass in masses.iteritems():
                if particle in line:
                    newline = "      %s     %s       # \n" % (particle, mass)
        if "DECAY" in line and decay_info != "":
            # check the particles in decay_info
            # if they are there, do not keep the old info
            decay_part1 = line.split()[0] 
            decay_part2 = line.split()[1]
            if re.search("%s\s+%s"%(decay_part1, decay_part2),decay_info):
                continue
        if "STOPMIX" in lastblock and stop_mixing_matrix:
            s = line.split()
            if not (line == lastblock or  len(s)<=3):
                #print line
                i,j,v         = line.split()[:3]
                newval  = stop_mixing_matrix[i][j]
                #print "replacing StopMix[%s][%s] from %s to %s"%(i,j,v,newval)
                newline="  %(i)s  %(j)s     %(newval)s   # F_\{%(i)s%(j)s} \n"%{"i":i, "j":j, "newval":newval}
        if "</slha>" in line and decay_info != "":
            # add the DECAY before closing the tag
            # check whether decay_info ends in \n
            if decay_info.strip(" ")[-1:] == "\n":
                newline = decay_info
            else: 
                newline = decay_info+"\n"
            newline += line
        if in_ev and line.startswith("<"):
            newline = "%s\n%s" % (modeltag,line)
            in_ev = False
        outfile.write(newline)
        if "<event>" in line: 
            in_ev = True
        if "</event>" in line:
            nev += 1
        if nev == nevents:
            # We've reached the number of events we wanted
            # write out the end statement and stop
            outfile.write("</LesHouchesEvents>\n")
            break
    outfile.close()
    infile.close()


def update_proc_card(infilename, outfilename ): 
    if not "proc_card" in infilename:
        raise Exception("The input should be a proc_card but it is %s"%infilename)
    if infilename.endswith(".lhe.gz"):
        infile = gzip.open(infilename)
    elif any([infilename.endswith(suffix) for suffix in ['.lhe','.dat','.txt']]):
        infile = open(infilename)
    else: 
        sys.exit("LHE files should have extension .lhe or .lhe.gz")
    outfile = open(outfilename,'w')
    output  = os.path.splitext( os.path.basename( outfilename ) )[0].replace("_proc_card","")

    for line in infile: 
        if line.startswith("output"):
            newline = "output %s -nojpeg\n"%output
        else:
            newline = line
        outfile.write(newline)
    outfile.close()
    infile.close()


def make_stop_mixing_matrix( theta_eff ):
    atantan = math.atan( -1/4.* math.tan( theta_eff) )
    sin     = round( math.sin( atantan ) , 15)
    cos     = round( math.cos( atantan ) , 15)
    matrix =  {
               '1': {'1': cos, '2': -sin },
               '2': {'1': -sin,'2': -cos }
               }
    return matrix



stop_cards_0j = {
                'run': 'default_cards/T2tt_0j_run_card.dat',
                'param': 'default_cards/T2tt_0j_param_card.dat',
                'proc': 'default_cards/T2tt_0j_proc_card.dat',
             }

stop_cards_1j = {
                'run': 'default_cards/T2tt_run_card.dat',
                'param': 'default_cards/T2tt_param_card.dat',
                'proc': 'default_cards/T2tt_proc_card.dat',
             }

stop_cards = stop_cards_0j

#def make_new_stop_cards( name , incards, mstop, mlsp, stop_mixing_matrix ):
def make_new_stop_cards( name , incards, mstop, mlsp, theta_eff, outdir="./"):
    stop_mixing_matrix = make_stop_mixing_matrix(theta_eff) 
    #print "%s : Using STOPMIX: %s"%(name, stop_mixing_matrix)
    if not os.path.isdir( outdir ) : os.makedirs( outdir ) 
    outcards  = { k:outdir+"/"+os.path.basename(v).replace(k,"%s_%s"%(name,k)) for k,v in incards.items() }
    masses = {'1000006':mstop, '1000022':mlsp}    
    update_header( incards['param'], outcards['param'], masses, "", "", "", stop_mixing_matrix)
    update_proc_card( incards['proc'], outcards['proc'] ) 

    for rp in ['run']:
        shutil.copyfile( incards[rp], outcards[rp])

if __name__ == '__main__':
    theta_eff_dict = {}
    
    outdir = "./t2tt_0j_polar_cards/"

    coeff_onshell     = [ 0.,0.25,0.5,1]
    import numpy as np
    poi_points = lambda poi : [ float("%s"%x) for x in np.linspace(poi-0.5,poi+0.5,21).round(2) ]

    dm_POIs = { 
                90:  -0.4 , 
                80:  -0.35, 
                70:  -0.3 , 
                60:  -0.25, 
                50:  -0.20, 
                40:  -0.15, 
                30:  -0.10, 
                20:  -0.05, 
                10:  0    , 
              }
      
    

    dm_coeff_dicts ={
                      230:  coeff_onshell + [-1,-0.5,-0.25],   
                      200:  coeff_onshell, 
                      175:  coeff_onshell, 
                      170:  coeff_onshell,   
                      90:   coeff_onshell + [-1,-0.5,-0.25] ,
                      80:   poi_points( dm_POIs[80] ),
                      70:   poi_points( dm_POIs[70] ),
                      60:   poi_points( dm_POIs[60] ),
                      50:   poi_points( dm_POIs[50] ),
                      40:   poi_points( dm_POIs[40] ),
                      30:   poi_points( dm_POIs[30] ),
                      20:   poi_points( dm_POIs[20] ),
                      10:   poi_points( dm_POIs[10] ),
                    }


    mstop = 500
    commands = []
    for dm, coeffs in dm_coeff_dicts.items(): 
        theta_eff_dict = { 
                        ('%sPi'%(round(coeff,3))).replace(".","p").replace("-","m"): math.pi * coeff 
                        for coeff in coeffs
                     }
        mlsp = mstop - dm 
        for thetatag, theta_eff in theta_eff_dict.items():
            card_tag  = "mStop_%s_mLSP_%s_%s"%( mstop,mlsp, thetatag)
            make_new_stop_cards( card_tag, stop_cards, mstop, mlsp , theta_eff, outdir)
            card_name = os.path.basename( stop_cards['run'].replace("run_card.dat","") ) + card_tag
            command = "./submit_gridpack_generation.sh 12000 12000 1nw %s %s 8nh"%(card_name, outdir)
            #command = "submit_condor_gridpack_generation.sh %s %s"%(card_name, outdir)
            commands.append(command)

    for c in commands:
        print c
