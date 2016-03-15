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
#base_lumi = 10000
#base_lumi = 19700
#new_lumi = float(args[1])
#adjust_lumi = new_lumi / base_lumi

#
# Output dir
#

output_dir = args[1]

if not os.path.isdir(output_dir):
    os.mkdir(output_dir)


#
# prepare output
#



#
# define bins (signal is added automatically), observations and expectations
#

srBins = [ 
          'SRL1a',
          'SRH1a',
          'SRV1a',
          'SRL1b',
          'SRH1b',
          'SRV1b',
          'SRL1c',
          'SRH1c',
          'SRV1c',
          'SRL2' ,
          'SRH2' ,
          'SRV2' ,
        ]

srBinsToUse = {
          'SRL1a':['SRL1a'],
          'SRH1a':['SRH1a'],
          'SRV1a':['SRV1a'],
          'SRL1b':['SRL1b'],
          'SRH1b':['SRH1b'],
          'SRV1b':['SRV1b'],
          'SRL1c':['SRL1c'],
          'SRH1c':['SRH1c'],
          'SRV1c':['SRV1c'],
          'SRL2' :['SRL2' ],
          'SRH2' :['SRH2' ],
          'SRV2' :['SRV2' ],

          "SRSL1a": ['SRL1a', 'SRH1a', 'SRV1a'] ,
          "SRSL1b": ['SRL1b', 'SRH1b', 'SRV1b'] ,
          "SRSL1c": ['SRL1c', 'SRH1c', 'SRV1c'],
          "SRSL2" : ['SRL2', 'SRH2', 'SRV2'],
          "SRSL1" : ['SRL1a', 'SRH1a', 'SRV1a', 'SRL1b', 'SRH1b', 'SRV1b' , 'SRL1c', 'SRH1c', 'SRV1c' , 'SRL2', 'SRH2', 'SRV2' ]
    
        }


for srBin in srBinsToUse:

    bins = [x for x in dc.bins if x in srBinsToUse[srBin] or "CR" in x] 
    ignorebins = [x for x in srBins if not x in srBinsToUse[srBin] ]


    print "----------------------------------------------------"
    print srBin, srBinsToUse[srBin]
    print bins
    print ignorebins
    print len(bins)
    assert len(bins) + len(ignorebins) == len(dc.bins)
    print "----------------------------------------------------"


    cfw = cardFileWriter()
    cfw.reset()
    cfw.defWidth=10
    cfw.precision=4
    cfw.maxUncNameWidth = 15
    cfw.maxUncStrWidth = 10

    for b in bins:
        print "----- Adding", b 
        cfw.addBin(b,[ x for x in dc.processes if x!="signal" ])
        print "   ", "Specify Obs"
        if b in ignorebins:
            cfw.specifyObservation(b, 0 )
            for p in dc.processes:       
                cfw.specifyExpectation(b,p, 0  )
        else:
            cfw.specifyObservation(b,int(dc.obs[b]  ))
            for p in dc.processes:       
                cfw.specifyExpectation(b,p,dc.exp[b][p] )
        #
        # define and fill systematics
        #
    print "      ", "Systs:"
    for s in dc.systs:
        sname = s[0]
        stype = s[2]
        #if any( x[0:4] in sname for x in ignorebins  ):
        #    continue
        if stype=="gmN":
            print "       ", "add gmn", sname, stype, s[3][0]
            cfw.addUncertainty(sname,stype,s[3][0])
        else:
            print "       ", "add ", sname, stype 
            cfw.addUncertainty(sname,stype)
        # each systematics contains entries for bins ...
        for b in s[4]:
            if b in ignorebins:
                continue
            # ... and processes
            for p in s[4][b]:
                # extract value and add it, if non-zero
                v = s[4][b][p]
                if v>1.e-6:
                    cfw.specifyUncertainty(sname,b,p,v)
    #
    # write output file
    #
    output_name = os.path.basename(args[0])
    #output_file = args[0].replace( os.path.basename(args[0]), output_name+".txt" )
    sr_dir = output_dir+"/"+srBin
    if not os.path.isdir(sr_dir):
        os.mkdir(sr_dir)
    output_file = sr_dir +"/"+output_name
    print output_file
    cfw.writeToFile(output_file)
        
