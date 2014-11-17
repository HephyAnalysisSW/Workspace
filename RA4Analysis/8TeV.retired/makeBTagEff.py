from btagEff import *
import pickle

from defaultMu2012Samples import ttbarPowHeg

mcEffPowHeg4j = getBTagMCTruthEfficiencies(False, ttbarPowHeg, "ht>400&&type1phiMet>150&&njets>=4")
pickle.dump(mcEffPowHeg4j, file("/data/schoef/results2012/BTagEffPowHegHT400Met150njets4.pkl", "w"))
#mcEffPowHeg6j = getBTagMCTruthEfficiencies(False, ttbarPowHeg, "ht>400&&type1phiMet>150&&njets>=6")
#pickle.dump(mcEffPowHeg6j, file("/data/schoef/results2012/BTagEffPowHegHT600Met150njets6.pkl", "w"))

#mcEff = pickle.load(file("btagEff/mceff_mod2.pkl"))
#mcEff = pickle.load(file("/data/schoef/results2012/btagEff/mceff.pkl"))

