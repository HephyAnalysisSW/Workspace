import os, sys, uuid

#/data/schoef/lhe/decayed_stop200lsp170g100.lhe
#/data/schoef/lhe/decayed_stop300lsp240g150.lhe
#/data/schoef/lhe/decayed_stop300lsp270g175.lhe
#/data/schoef/lhe/decayed_stop300lsp270g200.lhe

ifile = sys.argv[1]
skipEvents = int(sys.argv[2])
stop = int(sys.argv[3])

maxJobLength=10

uniqueDirname = str(uuid.uuid4())

while True:

  if stop - skipEvents<=0: break

  maxEvents = min(maxJobLength, stop - skipEvents)
  
  
  sstring = "mkdir "+uniqueDirname+";cd "+uniqueDirname+";"

  sstring+="cmsRun /afs/hephy.at/scratch/s/schoefbeck/CMS/CMSSW_5_3_11_patch6/src/Workspace/MonoJetAnalysis/crab/run_Hadronizer_SMS_Scans_2jets_Qcut44_TuneZ2star_8TeV_madgraph_tauola_cff_py_GEN_FASTSIM_HLT_PU.py"
  sstring+=" infile=file:"+ifile+" maxEvents="+str(maxEvents)+" skipEvents="+str(skipEvents)+";"
  sstring+="cd ..; rm -rf "+uniqueDirname
  print sstring
  os.system(sstring)
  skipEvents+=maxEvents

