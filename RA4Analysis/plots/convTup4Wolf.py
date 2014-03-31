import copy, pickle
import ROOT as R
from Workspace.RA4Analysis.simplePlotsCommon import *
from math import *
import os

# ============================================================================
Path = '/data/jkancsar/topDiLepton/convertedTuples/'
inputDir  = Path+'Powheg_130111/TTJets-PowHeg/'
outputDir = Path+'Powheg_130111/Tuple_kwolf/'
outputFile = outputDir+'tuple.root'

CutB1 = 'Reco==1 && Flag_t1ptMin==1 && chi2Min<3'# && ht2Min>400'
CutB2 = 'Reco==1 && Flag_t2ptMin==1 && chi2Min<3'# && ht1Min>400'

variables = ["weight", "run","lumi"]
extraVariables = ['met', 'ht', 'Zweig','leptonPdg', 'weightCorrHT400']

# ============================================================================
def getVarValue(c, var, n=0):
  varNameHisto = var
  leaf = c.GetAlias(varNameHisto)
  if leaf!='':
    return c.GetLeaf(leaf).GetValue(n)
  else:
    return c.GetLeaf(var).GetValue(n)
    #return float('nan')

def f(x):
#  a = 1.10716860861   # abs() nicht implementiert
#  b = -0.000545146100932
  a = 1.09550347886
  b = -0.000481049974545
  return a+b*x

# ============================================================================

Cut = [CutB1, CutB2]

structString = "struct MyStruct{ULong_t event;"

for var in variables:
  structString +="Float_t "+var+";"
for var in extraVariables:
  structString +="Float_t "+var+";"

structString   +="};"

ROOT.gROOT.ProcessLine(structString)

from ROOT import MyStruct

s = MyStruct()

if not os.path.isdir(outputDir):
  os.system("mkdir "+outputDir)

t = R.TTree( "Events", "Events", 1 )
t.Branch("event", ROOT.AddressOf(s, "event"), "event/l")
for var in variables:
  t.Branch(var,   ROOT.AddressOf(s,var), var+'/F')
for var in extraVariables:
  t.Branch(var,   ROOT.AddressOf(s,var), var+'/F')

# ============================================================================
for cut in Cut:
  c = R.TChain('Events')
  c.Add(inputDir+'*.root')
  #c.Add(inputDir+'histo_TTJets-PowHeg_0_100.root')
  print 'applying Cut', cut
  c.Draw('>>eList', cut)
  elist = ROOT.gDirectory.Get("eList")
  number_events = elist.GetN()
  print '# Events:', number_events

  for i in range(0, number_events):
    if (i%10000 == 0) and i>0:
      print i, '('+str(number_events)+')'
    c.GetEntry(elist.GetEntry(i))

    for var in variables:
      getVar = var
      exec("s."+var+"="+str(getVarValue(c, getVar)).replace("nan","float('nan')"))
    
    for var in extraVariables:
      exec("s."+var+"=float('nan')")

    s.event = long(getVarValue(c, 'event'))
    #s.weight = getVarValue(c, 'weight')

    if cut == CutB1:
      s.met = getVarValue(c, 'nu1ptMin')
      s.leptonPdg = getVarValue(c, 'l1Pdg')
      s.ht = getVarValue(c, 'ht2Min')
      s.Zweig = 1
    elif cut == CutB2:
      s.met = getVarValue(c, 'nu2ptMin')
      s.leptonPdg = getVarValue(c, 'l2Pdg')
      s.ht = getVarValue(c, 'ht1Min')
      s.Zweig = 2

    s.weightCorrHT400 = s.weight * 1./f(s.met)

    t.Fill()

# ============================================================================
f = R.TFile(outputFile, 'recreate')
t.Write()
f.Close()

# EOF
