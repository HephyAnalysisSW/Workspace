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
# prepare output
#
cfw = cardFileWriter()
cfw.defWidth=10
cfw.precision=4
cfw.maxUncNameWidth = 15
cfw.maxUncStrWidth = 10
#
# XSec 8TeV -> 13TeV
#
new_xsec = "xsec_scaled_to_13TeV"
xsec_factor={
        "WJets": 61526.7  / 36257.2   ,
        "TTJets":  831.76 / 225.197   ,
        "signal":   8.51615  /1.99608 ,
        "other" : 2.                  ,
        }



#
# define bins (signal is added automatically), observations and expectations
#
for b in dc.bins:
    cfw.addBin(b,[ x for x in dc.processes if x!="signal" ])
    for p in dc.processes:       
        cfw.specifyExpectation( b,p,dc.exp[b][p] * xsec_factor[p] )
    #cfw.specifyObservation(b,int(dc.obs[b] ))
    cfw.specifyObservation(b,int(sum([ dc.exp[b][p]*xsec_factor[p] for p in ["TTJets","WJets","other"] ])) )

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
output_name = os.path.splitext(os.path.basename(args[0]))[0] + "_%s"%new_xsec
output_file = args[0].replace( os.path.basename(args[0]), output_name+".txt" )
print "Expecation values scaled to 13 TeV. output: %s"%(output_file)
cfw.writeToFile(output_file)

        
