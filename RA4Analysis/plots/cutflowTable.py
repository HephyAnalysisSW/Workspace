import ROOT
from analysisHelpers import getBkgChain, getSignalChain, getCutSignalYield
for path in [os.path.abspath(p) for p in ['../../HEPHYPythonTools/python/']]:
  if not path in sys.path:
      sys.path.insert(1, path)

from xsecSMS import gluino8TeV_NLONLL, gluino14TeV_NLO
#signals = [(1500, 0), (1850,0), (2000, 0), (1250, 0)]
signals = [(1000,600), (1250, 0)]
backgrounds = ["TTJets-PowHeg", "WJetsCombined", ("singleTop", "DY", "QCD")]

scaleTo14TeV = False

tableTexName = {}
tableTexName["TTJets-PowHeg"] = "\\ttjets"
tableTexName["WJetsCombined"] = "\\wjets"
tableTexName["singleTop"] = "t+jets"
tableTexName[("DY", "QCD")] = "other"
tableTexName[("singleTop", "DY", "QCD")] = "other"

scaling8To14={}
scaling8To14["TTJets-PowHeg"] = 882.29/745.16
scaling8To14["WJetsCombined"] = 0.5*(12005./6876 + 9017./4871) 
scaling8To14["singleTop"] = 0.5*(155.8/55.5 + 93.9/30.0) 
scaling8To14[("DY", "QCD")] = 2155./1174.
scaling8To14[("singleTop", "DY", "QCD")] = scaling8To14["singleTop"]

for s in signals:
  tableTexName[s] = "_".join([str(s[0])])
  if scaleTo14TeV:
    scaling8To14[s] = gluino14TeV_NLO[s[0]] / gluino8TeV_NLONLL[s[0]] 
  else:
    scaling8To14[s]=1.
  print "Signal scaling for",s,":", scaling8To14[s]

cuts=[\
  ("$\\ETmiss>100\\GeV$",                     "type1phiMet>100&&((singleElectronic&&nvetoMuons==0&&nvetoElectrons==1)||(singleMuonic&&nvetoMuons==1&&nvetoElectrons==0))"),
  ("$\\geq 1$ \\cPqb-tag",                    "nbtags>=1&&type1phiMet>100&&((singleElectronic&&nvetoMuons==0&&nvetoElectrons==1)||(singleMuonic&&nvetoMuons==1&&nvetoElectrons==0))"),
  ("$\\geq$4 jets",                           "njets>=4&&nbtags>=1&&type1phiMet>100&&((singleElectronic&&nvetoMuons==0&&nvetoElectrons==1)||(singleMuonic&&nvetoMuons==1&&nvetoElectrons==0))"),
  ("$\\HT\\geq 500$ \\GeV",                   "njets>=4&&nbtags>=1&&type1phiMet>100&&ht>500&&((singleElectronic&&nvetoMuons==0&&nvetoElectrons==1)||(singleMuonic&&nvetoMuons==1&&nvetoElectrons==0))"),
  ("$\\geq 2$ \\cPqb-tags",                   "njets>=4&&nbtags>=2&&type1phiMet>100&&ht>500&&((singleElectronic&&nvetoMuons==0&&nvetoElectrons==1)||(singleMuonic&&nvetoMuons==1&&nvetoElectrons==0))"),
  ("$\\geq$6 jets",                           "njets>=6&&nbtags>=2&&type1phiMet>100&&ht>500&&((singleElectronic&&nvetoMuons==0&&nvetoElectrons==1)||(singleMuonic&&nvetoMuons==1&&nvetoElectrons==0))"),
  ("$\\ETmiss\\geq 250$ \GeV",                "njets>=6&&nbtags>=2&&type1phiMet>250&&ht>500&&((singleElectronic&&nvetoMuons==0&&nvetoElectrons==1)||(singleMuonic&&nvetoMuons==1&&nvetoElectrons==0))"),
  ("$\\mT>120$ \\GeV",                        "mT>120&&njets>=6&&nbtags>=2&&type1phiMet>250&&ht>500&&((singleElectronic&&nvetoMuons==0&&nvetoElectrons==1)||(singleMuonic&&nvetoMuons==1&&nvetoElectrons==0))"),
  ("$\\test$ \\GeV",                          "njets>=4&&nbtags==2&&type1phiMet>150&&ht>400&&((singleElectronic&&nvetoMuons==0&&nvetoElectrons==1)||(singleMuonic&&nvetoMuons==1&&nvetoElectrons==0))"),
  ]
if not globals().has_key('chain'):
  chain={}
  for bkg in backgrounds:
    chain[(bkg)] = getBkgChain(dir = "/data/schoef/convertedTuples_v19/copyMET/", samples=(bkg))
  for sig in signals:
#    chain[sig] = getSignalChain(sig[0], sig[1], "T1tttt", dir = "/data/adamwo/convertedTuples_v16/copyMET/")
    chain[sig] = getSignalChain(sig[0], sig[1], "T1tttt-madgraph", dir = "/data/schoef/convertedTuples_v19/copyMET/")

print " & " + " & ".join([tableTexName[s] for s in backgrounds+signals])+"\\\\\\hline"
for c in cuts:
  sstring  = c[0]+" & " + " & ".join([str(round(getCutSignalYield(chain[s], c[1], "("+str(scaling8To14[s])+"*weight)", correctForFastSim = False, mtcut = None)['res'],1)) for s in backgrounds+signals])
  if not c==cuts[-1]:
    sstring+="\\\\"
  print sstring
