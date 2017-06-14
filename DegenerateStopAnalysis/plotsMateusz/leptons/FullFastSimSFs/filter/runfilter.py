import os, sys, time, glob
import subprocess

startM = time.clock()
startC = time.time()

indir = '/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/8025_mAODv2_v7/80X_postProcessing_v1/analysisHephy_13TeV_2016_v2_3/step1/'
#indir = '/afs/hephy.at/data/imikulec01/run16full_v7'
outdir = '/afs/hephy.at/data/mzarucki01/filterTest/'
#outdir = '/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/8025_mAODv2_v7/80X_postProcessing_v1/analysisHephy_13TeV_2016_v2_3/step1/'
mc_path     = "RunIISummer16MiniAODv2_v7" 
data_path   = "Data2016_v7"
insubdir = 'skimPreselect/incLep'
outsubdir = 'skimPreselect/filterLepSF'
#insubdir = 'oneLepGood'
#outsubdir = 'oneLepGood/filter'
#insubdir = 'LT120'
#outsubdir = 'LT120/filter'

samples = sys.argv[1].split(",")

datasamples = ["MET","SingleElectron","SingleMuon","JetHT"]
#filterscript = "filterPP.py"
filterscript = "filterFullFastSimSF.py"
#filterscript = "filterAddJigsaw.py"
inputskims = ["ST", "LT", "STfilter", "FR"]

inputskim = "ST"
outputskim = 'srcr'

if len(sys.argv) > 2: inputskim = sys.argv[2]
if inputskim not in inputskims:
    print "inputskim",inputskim,"not known, exiting"
    sys.exit()
    
if inputskim == "ST":
    insubdir = 'skimPreselect/incLep'
    #outsubdir = 'skimPreselect/filter'
elif inputskim == "LT":
    insubdir = 'LT120'
    #outsubdir = 'LT120/filter'
elif inputskim == "STfilter":
    insubdir = 'skimPreselect/filter'
    #outsubdir = 'skimPreselect/filterJigsaw'
elif inputskim == "FR":
    insubdir = 'oneLepGood_HT800'
    #outsubdir = 'oneLepGood_HT800/filter'


inputskims = {
               'ST': 'skimPreselect/incLep',
               'LT': "LT120",
              'STfilter':'skimPreselect/filter',
             'FR':'oneLepGood_HT800',
             }

outputskims = {
            'pre1Lep' : 'skimPreselect/filter'      ,
            'srcr'    : 'skimPreselect/filterMETHT250' ,
              }


insubdir = inputskims[inputskim]
outsubdir = outputskims[outputskim]


print "Input SubDir"   , insubdir
print "Output SubDir"  , outsubdir


for sample in samples:

    #thispath = data_path if sample in datasamples else mc_path
    thispath = data_path if any( [x in sample for x in  datasamples]) else mc_path
    
    print thispath
    
    ds = glob.glob("/".join([indir,thispath,insubdir,sample])+"*")
    print "found %s directories!"%len(ds)
    
    print "/".join([indir,thispath,insubdir,sample])+"*"
    print ds
    
#    if sample[:8] == "TTJets_H":
#        ds += (glob.glob("/".join([indir,thispath,"lheHThigh",insubdir,sample])+"*"))
#    if sample[:8] == "TTJets_T":
#        ds = (glob.glob("/".join([indir,thispath,"lheHTlow",insubdir,sample])+"*"))
    
    for d in ds:
        ix = d.rindex("/") + 1
        thisindir = d
        thisoutdir = "/".join([outdir,thispath,outsubdir,d[ix:]])
        if not os.path.isdir(thisoutdir):
            command = 'mkdir -p '+thisoutdir
            print command
#            os.system(command)          
            output = subprocess.check_output(command,shell=True)
            print output

        files = os.listdir(thisindir)
        for f in files:
            infile = "/".join([thisindir,f])
            outfile = "/".join([thisoutdir,f])
            command = "python {0} {1} {2}".format(filterscript,infile,outfile)
            print command
#            os.system(command)
            output = subprocess.check_output(command,shell=True)
            print output
        
endM = time.clock()
endC = time.time()

print "-"*20,"total","-"*20
print "machine:", (endM-startM), "wall clock:", (endC-startC)
