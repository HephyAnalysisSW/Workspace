from math import *
import os, sys, time, getopt
import array
from ROOT import *

infile = "/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/8020_mAODv2_v5/80X_postProcessing_v0/analysisHephy_13TeV_2016_v2_1/step1/RunIISpring16MiniAODv2_v5/skimPreselect/incLep/WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1_Chunks_0_99_0.root"
outfile = "filterPP.root"
branchfile_data = "branches-keep_ppv7_data.list"
branchfile_mc = "branches-keep_ppv7_mc.list"

if len(sys.argv)>1: infile = sys.argv[1]
if len(sys.argv)>2: outfile = sys.argv[2]

branchfile = branchfile_mc
if infile.find("Data2016") > -1: branchfile = branchfile_data

def getlistofbranches(filename):
    f = open(filename,'r')
    outlist = []
    for line in f:
        ll = line.split(':')
        print ll
        if len(ll) == 3: outlist.append(ll[1].strip())
    f.close()
    return outlist
    
def dofilter(infile,outfile,keepbranches):
    infilename = infile
    outfilename = outfile
    f = TFile(infilename)
    t = f.Get("Events")
    t.SetBranchStatus("*", 0)
    for br in keepbranches:
        print br
        t.SetBranchStatus(br, 1)

    g = TFile(outfilename,"recreate")
#    a = t.CloneTree(0)
    a = t.CloneTree(-1)
    print t.GetEntries()
#    for i in xrange(t.GetEntries()):
##        if i>10: break
#        if not i%1000000: print i,time.strftime('%X %x %Z')
#        t.GetEntry(i)

#        a.Fill()

    g.cd()

    a.Write()
    g.Close()
    f.Close()

print 'start time:',time.strftime('%X %x %Z')  
keeplist = getlistofbranches(branchfile) 
print keeplist
dofilter(infile,outfile,keeplist) 
print 'end time:',time.strftime('%X %x %Z')  

