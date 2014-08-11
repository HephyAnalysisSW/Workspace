import ROOT

import ROOT
import pickle
from array import array
from helpers import gTauAbsEtaBins, gTauPtBins, metParRatioBins, jetRatioBins

from stage2Tuples import ttJetsCSA14
c = ROOT.TChain('Events')
for b in ttJetsCSA14['bins']:
  c.Add(ttJetsCSA14['dirname']+'/'+b+'/h*.root')

doubleLeptonPreselection = 

c.Draw(">>eList", commoncf)
elist = ROOT.gDirectory.Get("eList")
number_events = elist.GetN()
if options.small:
  if number_events>1001:
    number_events=1001
start = int(options.fromPercentage/100.*number_events)
stop  = int(options.toPercentage/100.*number_events)
print "Reading: ", sample["name"], bin, "with",number_events,"Events using cut", commoncf
print "Reading percentage ",options.fromPercentage, "to",options.toPercentage, "which is range",start,"to",stop,"of",number_events
for i in range(start, stop):
  if (i%10000 == 0) and i>0 :
    print i
#      # Update all the Tuples
  if elist.GetN()>0 and ntot>0:
    c.GetEntry(elist.GetEntry(i))
    events.to(elist.GetEntry(i))

