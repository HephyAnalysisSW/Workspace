import sys,os
from optparse import OptionParser
from HiggsAnalysis.CombinedLimit.DatacardParser import *
from Workspace.DegenerateStopAnalysis.cardFileWriter import cardFileWriter
#
# options needed for the DatacardParser
#
dcparser = OptionParser()
addDatacardParserOptions(dcparser)
(dcoptions, dcargs) = dcparser.parse_args([])
#
# any options needed for this script?
#
parser = OptionParser()
(options,args) = parser.parse_args()
#
# parse input file
#
dc = parseCard(file(args[0]),dcoptions)
#
# lumi info
#
base_lumi = 10000
#base_lumi = 19700
new_lumi = float(args[1])
adjust_lumi = new_lumi / base_lumi
#
# Output dir
#
output_dir = args[2]
#
# prepare output
#
cfw = cardFileWriter()
cfw.defWidth=10
cfw.precision=4
cfw.maxUncNameWidth = 15
cfw.maxUncStrWidth = 10

#
# define bins (signal is added automatically), observations and expectations
#
for b in dc.bins:
    cfw.addBin(b,[ x for x in dc.processes if x!="signal" ])
    cfw.specifyObservation(b,int(dc.obs[b] * adjust_lumi ))
    for p in dc.processes:       
        cfw.specifyExpectation(b,p,dc.exp[b][p] * adjust_lumi)
#
# define and fill systematics
#
for s in dc.systs:
    sname = s[0]
    stype = s[2]
    if stype=="gmN":
        cfw.addUncertainty(sname,stype,s[3][0])
    else:
        cfw.addUncertainty(sname,stype)
    # each systematics contains entries for bins ...
    for b in s[4]:
        # ... and processes
        for p in s[4][b]:
            # extract value and add it, if non-zero
            v = s[4][b][p]
            if v>1.e-6:
                cfw.specifyUncertainty(sname,b,p,v)
#
# write output file
#
output_name = os.path.splitext(os.path.basename(args[0]))[0] + "_%spbm1"%int(new_lumi)
#output_file = args[0].replace( os.path.basename(args[0]), output_name+".txt" )
output_file = output_dir+"/"+output_name
print "Expecation values changes based on lumi %s, by factor %s. output: %s"%(new_lumi, adjust_lumi, output_file)
cfw.writeToFile(output_file)

        
