from Workspace.DegenerateStopAnalysis.navidTools.NavidTools import CutClass, joinCutStrings, splitCutInPt, btw, less, more

## --------------------------------------------------------------
##                           Variables
## --------------------------------------------------------------



## --------------------------------------------------------------
##                            CUT LISTS
## --------------------------------------------------------------

## Common presel for Mu and El

dPhiJetMet = "Min$(acos(cos(met_phi - Jet_phi[IndexJet_vetoJet*(IndexJet_vetoJet>-1)])))"



presel_noAntiQCD = CutClass ("PreselNoAntiQCD", [
                              ["MET200","met>200"],
                              ["ISR110","nIsrJet>=1" ],
                              ["HT300","ht_basJet>300"],
                              #["No3rdJet60","nVetoJet<3"],
                              #["TauElVeto","(Sum$(TauGood_idMVA)==0) && (Sum$(abs(LepGood_pdgId)==11 && LepGood_SPRING15_25ns_v1==1)==0)"],
                              #["1Mu-2ndMu20Veto", "(nLepGood_mu==1 || (nLepGood_mu ==2 && LepGood_pt[IndexLepGood_mu[1]] < 20) )"],
                             ],
                baseCut=None,
                )



presel_antiQCD = CutClass ("presel_antiQCD", [
                              ["AntiQCD", " (vetoJet_dPhi_j1j2 < 2.5)" ], # old
                              ["No3rdJet60","nVetoJet<=2"],
                             ],
                baseCut=None,
                )

presel_common = CutClass('presel_common', [], baseCut=None)
presel_common.add( presel_noAntiQCD )
presel_common.add( presel_antiQCD   )






 
