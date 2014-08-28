import os
templateFile = 'crab_template.py'
samples=[\
#/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM  
#/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Spring14miniaod-PU20bx25_POSTLS170_V5-v2/MINIAODSIM #Identical? Same event count  #miniAODTuple_e/
#  "/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Spring14miniaod-PU_S14_POSTLS170_V6-v1/MINIAODSIM", #MiniAODTupleTT1e/
  "/WJetsToLNu_HT-200to400_Tune4C_13TeV-madgraph-tauola/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM", #/data/easilar/crab3WorkAreas/...
#  "/WJetsToLNu_HT-400to600_Tune4C_13TeV-madgraph-tauola/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM",  #/data/easilar/crab3WorkAreas/...
#  "/WJetsToLNu_HT-600toInf_Tune4C_13TeV-madgraph-tauola/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM",
#  "/WJetsToLNu_13TeV-madgraph-pythia8-tauola/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM",
#  "/DYJetsToLL_M-50_HT-200to400_Tune4C_13TeV-madgraph-tauola/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM",
#  "/DYJetsToLL_M-50_HT-400to600_Tune4C_13TeV-madgraph-tauola/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM",
#  "/DYJetsToLL_M-50_HT-600toInf_Tune4C_13TeV-madgraph-tauola/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM",
#  "/DYJetsToLL_M-50_13TeV-madgraph-pythia8/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM", #/data/easilar/crab3WorkAreas/...
#  "/DYJetsToLL_M-50_13TeV-pythia6/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM",
#  "/DYToEE_M-50_Tune4C_13TeV-pythia8/Spring14miniaod-castor-v2/MINIAODSIM",
#  "/DYToEE_Tune4C_13TeV-pythia8/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM",
#  "/DYToMuMu_M-15To50_Tune4C_13TeV-pythia8/Spring14miniaod-castor_PU20bx25_POSTLS170_V5-v1/MINIAODSIM",
#  "/DYToMuMu_M-50_Tune4C_13TeV-pythia8/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM",
#  "/DYToMuMu_M-50_Tune4C_13TeV-pythia8/Spring14miniaod-castor_PU20bx25_POSTLS170_V5-v1/MINIAODSIM",
#  "/DYToMuMu_M-6To15_Tune4C_13TeV-pythia8/Spring14miniaod-castor_PU20bx25_POSTLS170_V5-v1/MINIAODSIM",
#  "/DYToMuMu_Tune4C_13TeV-pythia8/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM",
#  "/TToBLNu_s-channel-EMu_Tune4C_13TeV-madgraph-tauola/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM",
#  "/TToBLNu_t-channel-EMu_Tune4C_13TeV-madgraph-tauola/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM",
#  "/TToBLNu_tW-channel-DR-EMu_Tune4C_13TeV-madgraph-tauola/Spring14miniaod-PU20bx25_POSTLS170_V5-v2/MINIAODSIM",
#  "/TToLeptons_s-channel-CSA14_Tune4C_13TeV-aMCatNLO-tauola/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM",
#  "/T_tW-channel-DR_Tune4C_13TeV-CSA14-powheg-tauola/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM",
#  "/Tbar_tW-channel-DR_Tune4C_13TeV-CSA14-powheg-tauola/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM",
#  "/TBarToLeptons_s-channel-CSA14_Tune4C_13TeV-aMCatNLO-tauola/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM",
#  "/TBarToLeptons_t-channel_Tune4C_CSA14_13TeV-aMCatNLO-tauola/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM",
#"/WJetsToLNu_HT-100to200_Tune4C_13TeV-madgraph-tauola/Spring14miniaod-PU20bx25_POSTLS170_V5-v2/MINIAODSIM",
#"/WJetsToLNu_HT-100to200_Tune4C_13TeV-madgraph-tauola/kreis-Spring14dr-PU_S14_POSTLS170_V6AN1-miniAOD706p1-814812ec83fce2f620905d2bb30e9100/USER",
#"/WJetsToLNu_HT-200to400_Tune4C_13TeV-madgraph-tauola/kreis-Spring14dr-PU_S14_POSTLS170_V6AN1-miniAOD706p1-814812ec83fce2f620905d2bb30e9100/USER",
#"/WJetsToLNu_HT-400to600_Tune4C_13TeV-madgraph-tauola/StoreResults-Spring14dr_PU_S14_POSTLS170_V6AN1_miniAOD706p1_814812ec83fce2f620905d2bb30e9100-v1/USER",
#"/WJetsToLNu_HT-600toInf_Tune4C_13TeV-madgraph-tauola/kreis-Spring14dr-PU_S14_POSTLS170_V6AN1-miniAOD706p1-814812ec83fce2f620905d2bb30e9100/USER",
]

for s in samples:
  pySampleName = s[1:].replace('/','_')
  #pySampleName = s[1:].replace('/','').replace('_','').replace('-','')
  cfgFileName = 'crab_'+pySampleName+'.py'
  print "Sample",s
  print "Using template",templateFile
  if os.path.isfile(cfgFileName) :
    print "Skipping! File ",cfgFileName,"already there!!"
    continue
  ofile = file(cfgFileName,'w')

  if not os.path.isfile(templateFile) :
    print "Stop. TemplateFile not found:", templateFile
    break
  ifile = open(templateFile,'r')

  replacements = [["DPMDIRECTORY", pySampleName], ["WORKINGDIRECTORY", '/data/easilar/crab3WorkAreas/'+pySampleName], ["SAMPLENAME", s]]

  for line in ifile.readlines():
#    print line
    for r in replacements:
      line=line.replace(r[0],r[1])
    ofile.write(line)
  ifile.close()
  ofile.close()
  print "Written",ofile.name
