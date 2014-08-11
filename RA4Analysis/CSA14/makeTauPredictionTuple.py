import ROOT

import ROOT
import pickle
from array import array
from helpers import gTauAbsEtaBins, gTauPtBins, metParRatioBins, jetRatioBins

from stage2Tuples import ttJetsCSA14
c = ROOT.TChain('Events')
for b in ttJetsCSA14['bins']:
  c.Add(ttJetsCSA14['dirname']+'/'+b+'/h*.root')

small = True

doubleLeptonPreselection = "ngoodMuons==1&&nvetoMuons==2" 

c.Draw(">>eList", doubleLeptonPreselection)
eList = ROOT.gDirectory.Get("eList")
number_events = elist.GetN()
if small:
  if number_events>1001:
    number_events=1001
for i in range(min(number_events, eList.GetN())):
  if (i%10000 == 0) and i>0 :
    print i
#      # Update all the Tuples
  if elist.GetN()>0 and ntot>0:
    c.GetEntry(elist.GetEntry(i))
    print i
    
