import os, sys, time, glob
import subprocess

startM = time.clock()
startC = time.time()

indir = "/afs/hephy.at/data/mzarucki01/cmgTuples/postProcessed_mAODv2/8025_mAODv2_v7/80X_postProcessing_v0/analysisHephy_13TeV_2016_v2_4/step1"
outdir = "/afs/hephy.at/data/mzarucki01/cmgTuples/postProcessed_mAODv2/8025_mAODv2_v7/80X_postProcessing_v0/analysisHephy_13TeV_2016_v2_4/step1"
mc_path = "RunIISummer16MiniAODv2_v7"
data_path = "Data2016_v7"

#outdir = '/data/run2/run16_v10'
#indir = '/home/run2/run16_v3'
#outdir = '/home/run2/run16_v3'
mc_path     = "RunIISummer16MiniAODv2_v7" 
data_path   = "Data2016_v7"
#insubdir = 'oneLep/filter'
#outsubdir = 'oneLep/filterW'

samples = ['WJetsToLNu_HT'] #sys.argv[1].split(",")
datasamples = ["MET","SingleElectron","SingleMuon"]

#mcsamples = ["DYJetsToLL","QCD_HT","QCD_Pt_","QCD_Pt-","TTJets_HT","TTJets_Tune","ZJetsToNuNu_HT","DYJetsToNuNu","SMS_T2_4bd","WJetsToLNu"]
mcsamples = ["WJetsToLNu_HT"]
#mcsamples = ["DYJetsToLL","QCD_HT","TTJets_HT","TTJets_Tune","ZJetsToNuNu_HT","SMS_T2tt","WJetsToLNu_HT","ST_","WW_","WZ_","ZZ_"]
filterscript = "filterWpol.py"

skim = 'HT300_ISR100'

if skim == "HT300_ISR100":
   insubdir = 'HT300_ISR100'
   outsubdir = 'HT300_ISR100/filter'

batchScript = open('batchScript_filter.sh', 'w')

for sample in samples:

    thispath = data_path if sample in datasamples else mc_path

    ds = glob.glob("/".join([indir,thispath,insubdir,sample])+"*")

    if sample[:8] == "TTJets_H":
        ds += (glob.glob("/".join([indir,thispath,"lheHThigh",insubdir,sample])+"*"))
    if sample[:8] == "TTJets_T":
        ds = (glob.glob("/".join([indir,thispath,"lheHTlow",insubdir,sample])+"*"))
   
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
            #output = subprocess.check_output(command,shell=True)
            #print output
 
            batchScript.write(command + '\n')

batchScript.close()
endM = time.clock()
endC = time.time()

print "-"*20,"total","-"*20
print "machine:", (endM-startM), "wall clock:", (endC-startC)
