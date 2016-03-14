"""
Usage: 
python adjustCardSysts.py path/to/card/withsys.txt path/to/card/withrates.txt output/dir
ex:
python adjustCardSysts.py cards/base/T2DegStop_300_270_cards_8TeV.txt cards/base/Reload_Inc.txt ./test_output/
"""
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
# parse input files
#

# the systs will be read from this card
dc  = parseCard(file(args[0]),dcoptions)

# rates will be read from this card
new = parseCard(file(args[1]),dcoptions)

#
# output dir
#
output_dir = args[2]


if not os.path.isdir(output_dir):
    os.mkdir(output_dir)



output_postfix = "SysAdjusted"

assert sorted(dc.bins)==sorted(new.bins)
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
    cfw.specifyObservation(b,int(new.obs[b]))
    for p in new.processes:       
        process_exp = new.exp[b][p]
        if p in dc.processes:
            cfw.specifyExpectation( b, p, process_exp )
        else:
            try:                    ## if bin "other" bin exist for process, add exp val to it
                process_exp +=  cfw.expectation[ (b,p) ]
            except KeyError:
                pass
            cfw.specifyExpectation( b, "other", process_exp)
        
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
inputfile = os.path.basename(args[1])
basename, ext = os.path.splitext(inputfile)

if output_postfix:
    if not output_postfix.startswith("_"):
        output_postfix = "_"+output_postfix
output_file = output_dir +"/"+ basename + output_postfix + ext


print "-----------------------------------------"
print "Output file created:     %s"%output_file
print "based on systematics of: %s"%args[0]
print "and rates of           : %s"%args[1]
print "-----------------------------------------"

cfw.writeToFile(output_file)

        
