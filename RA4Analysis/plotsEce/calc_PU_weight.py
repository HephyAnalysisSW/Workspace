import ROOT

from Workspace.RA4Analysis.cmgTuples_Spring16_MiniAODv2 import *
from Workspace.HEPHYPythonTools.helpers import getChunks , getPUHistos


path = "~/www/data/Run2016B/4fb/PU_histos/"

#bkg_list = [\
#TTJets_SingleLeptonFromT_full, TTJets_SingleLeptonFromTbar_full, TTJets_DiLepton_full,\
#TTJets_LO_HT600to800_25ns, TTJets_LO_HT800to1200_25ns, TTJets_LO_HT1200to2500_25ns, TTJets_LO_HT2500toInf_25ns,\
##DYJetsToLL_M_50_HT_100to200_25ns,DYJetsToLL_M_50_HT_200to400_25ns,DYJetsToLL_M_50_HT_400to600_25ns,DYJetsToLL_M_50_HT_600toInf_25ns,\
#WJetsToLNu_HT200to400,WJetsToLNu_HT400to600,WJetsToLNu_HT600to800,WJetsToLNu_HT800to1200,WJetsToLNu_HT1200to2500,WJetsToLNu_HT2500toInf,\
#QCD_HT300to500_25ns,QCD_HT500to700_25ns,QCD_HT700to1000_25ns,QCD_HT1000to1500_25ns,QCD_HT1500to2000_25ns,QCD_HT2000toInf_25ns,\
#TTWJetsToLNu,TTWJetsToQQ,TTZToLLNuNu,\
#ST_schannel_4f_leptonDecays,ST_tchannel_antitop_4f_leptonDecays,ST_tchannel_antitop_4f_leptonDecays,ST_tW_antitop_5f_inclusiveDecays,ST_tW_top_5f_inclusiveDecays,\
##DiBoson_WW,DiBoson_WZ,DiBoson_ZZ\
#]
#
#tot_bkg_PU_histo = ROOT.TH1F()
#
#for bkg in bkg_list:
#  print bkg["name"]
#  chunks = getChunks(bkg,getPU=True)
#  pu_histo = getPUHistos(chunks, histname='pileup')
#  tot_bkg_PU_histo.Add(pu_histo)
#  del pu_histo , chunks 
##tot_bkg_PU_histo.Draw()
#tot_bkg_PU_histo.SaveAs(path+"MC.root")
#mc_histo = tot_bkg_PU_histo

file = ROOT.TFile(path+"/MC.root")
mc_histo = file.Get("pileup") 

PU_var = [70 , 66, 74]

for var in PU_var:
  data_f = ROOT.TFile(path+"/pileup_data_"+str(var)+".root")
  h_data = data_f.Get("pileup")
  mc_histo.Scale(h_data.Integral()/mc_histo.Integral())
  h_ratio = h_data.Clone('h_ratio')
  h_ratio.Divide(mc_histo)
  h_ratio.SaveAs(path+"h_ratio_"+str(var)+".root")
  cb = ROOT.TCanvas("cb","cb",564,232,600,600)
  cb.cd()
  h_ratio.Draw()
  h_ratio.SetMaximum(4)
  cb.SaveAs(path+"h_ratio_"+str(var)+".png")


 
