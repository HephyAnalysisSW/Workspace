import ROOT
#from Workspace.RA4Analysis.cmgTuples_Spring15 import *
from Workspace.RA4Analysis.cmgTuplesPostProcessed_Spring15 import *
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.HEPHYPythonTools.helpers import getObjFromFile
ecalVeto= getObjFromFile('ecalveto.root','ecalveto')

presel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80&&Flag_EcalDeadCellTriggerPrimitiveFilter&&st>250&&htJet30j>500&&nJet30>1&&deltaPhi_Wl>1"
presel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80&&st>250&&htJet30j>500&&nJet30>1"
lepSel='hard'
#c = getChain(DY[lepSel],histname='')
c = getChain(WJetsHTToLNu[lepSel],histname='')



#c=ROOT.TChain('Events')
c1 = ROOT.TCanvas()
#c.Add('/data/easilar/cmgTuples/postProcessed_Spring15_bugfixed/hard/WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/*.root')
#c.Draw('Jet_phi:Jet_eta', 'abs(Jet_rawPt-Jet_mcPt)>50&&sqrt((met_genPt*cos(met_genPhi)-met_pt*cos(met_phi))**2+(met_genPt*sin(met_genPhi)-met_pt*sin(met_phi))**2)>150&&htJet30j>500&&htJet30j<750&&nBJetMediumCSV30==0&&st>250&&st<350&&met_genPt<50')
#c.Draw('Jet_phi:Jet_eta', 'abs(Jet_rawPt-Jet_mcPt)>50&&sqrt((met_genPt*cos(met_genPhi)-met_pt*cos(met_phi))**2+(met_genPt*sin(met_genPhi)-met_pt*sin(met_phi))**2)>150&&htJet30j>500&&htJet30j<750&&st>250&&st<350&&met_genPt<100','colz')
c.Draw('Jet_phi:Jet_eta', presel+'&&abs(Jet_rawPt-Jet_mcPt)*(abs(Jet_rawPt-Jet_mcPt)>100)','colz')
ecalVeto.Draw('same')
#c.Draw('Jet_phi:Jet_eta', 'abs(Jet_rawPt-Jet_mcPt)>50','colz')
#c.Draw('Jet_phi:Jet_eta', 'abs(Jet_rawPt-Jet_mcPt)>150','colz')
#c.Draw('met_genPt:sqrt((met_genPt*cos(met_genPhi)-met_pt*cos(met_phi))**2+(met_genPt*sin(met_genPhi)-met_pt*sin(met_phi))**2)', 'htJet30j>500&&htJet30j<750&&nBJetMediumCSV30==0&&st>250&&st<350&&Max$(abs(Jet_pt-Jet_mcPt))<50','colz')
#c.Draw('met_genPt:sqrt((met_genPt*cos(met_genPhi)-met_pt*cos(met_phi))**2+(met_genPt*sin(met_genPhi)-met_pt*sin(met_phi))**2)', 'htJet30j>500&&htJet30j<750&&nBJetMediumCSV30==0&&st>250&&st<350&&Max$(abs(Jet_pt-Jet_mcPt))>50','colz')
#c.Draw('met_genPt:sqrt((met_genPt*cos(met_genPhi)-met_pt*cos(met_phi))**2+(met_genPt*sin(met_genPhi)-met_pt*sin(met_phi))**2)', 'htJet30j>500&&htJet30j<750&&nBJetMediumCSV30==0&&st>250&&st<350','colz')
