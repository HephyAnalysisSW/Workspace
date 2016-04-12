import ROOT
import pickle
from Workspace.HEPHYPythonTools.user import username
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain, getChunks, getCutYieldFromChain, getYieldFromChain
from Workspace.RA4Analysis.cmgTuples_Spring15_MiniAODv2_25ns import *
from Workspace.HEPHYPythonTools.xsecSMS import *

#samples = [T5qqqqVV_mGluino_1000To1075_mLSP_1To950] #, T5qqqqVV_mGluino_1200To1275_mLSP_1to1150]
#samples = [T5qqqqVV_mGluino_800To975_mLSP_1To850, T5qqqqVV_mGluino_1300To1375_mLSP_1to1250, T5qqqqVV_mGluino_1600To1750_mLSP_1To950]
#samples = [T5qqqqVV_mGluino_1400To1550_mLSP_1To1275, T5qqqqVV_mGluino_1100To1175_mLSP_1to1050]
#T5qqqqVV_mGluino_1200To1275_mLSP_1to1150, 
samples = [T5qqqqVV_mGluino_600To675_mLSP_1to550, T5qqqqVV_mGluino_700To775_mLSP_1To650, T5qqqqVV_mGluino_800To975_mLSP_1To850, T5qqqqVV_mGluino_1000To1075_mLSP_1To950,\
           T5qqqqVV_mGluino_1100To1175_mLSP_1to1050, T5qqqqVV_mGluino_1200To1275_mLSP_1to1150, T5qqqqVV_mGluino_1300To1375_mLSP_1to1250, T5qqqqVV_mGluino_1400To1550_mLSP_1To1275,\
            T5qqqqVV_mGluino_1600To1750_mLSP_1To950  ]

pickleDir = '/data/'+username+'/Spring15/25ns/'

sample_label = "WZ"    ###can be WW , WZ , ZZ

for sample in samples: 
  print sample["name"]
  mass_dict = {}  
  chunks = getChunks(sample, maxN=-1)
  chain = getChain(chunks[0], minAgeDPM=0, histname='histo', xrootPrefix='root://hephyse.oeaw.ac.at/', maxN=-1, treeName='tree')

  hgluino = ROOT.TH1D("hgluino","hgluino",2000,0,2000)
  hlsp = ROOT.TH1D("hlsp","hlsp",2000,0,2000)
  #cpTree = chain.CopyTree("Sum$(abs(GenPart_pdgId)==1000022&&abs(GenPart_motherId)==1000024&&abs(GenPart_grandmotherId)==1000021)==2&&(Sum$(abs(GenPart_pdgId)==24)==2)")
  ###T5qqqqWW
  if sample_label == "WW" :
    print "I am at WW"
    cut_common = "Sum$(abs(GenPart_pdgId)==1000022&&abs(GenPart_motherId)==1000024&&abs(GenPart_grandmotherId)==1000021)==2&&(Sum$(abs(GenPart_pdgId)==24)==2)"
  ###T5qqqqWZ
  if sample_label == "WZ" :
    print "I am at WZ"
    cut_common = "Sum$(abs(GenPart_pdgId)==1000022&&abs(GenPart_motherId)==1000024&&abs(GenPart_grandmotherId)==1000021)==1&&Sum$(abs(GenPart_pdgId)==1000022&&abs(GenPart_motherId)==1000023&&abs(GenPart_grandmotherId)==1000021)==1&&Sum$(abs(GenPart_pdgId)==23)==1&&Sum$(abs(GenPart_pdgId)==24)==1&&(Sum$(abs(GenPart_pdgId)==23)+Sum$(abs(GenPart_pdgId)==24))==2"
  ###T5qqqqZZ
  if sample_label == "ZZ" :
    print "I am at ZZ"
    cut_common = "Sum$(abs(GenPart_pdgId)==1000022&&abs(GenPart_motherId)==1000023&&abs(GenPart_grandmotherId)==1000021)==2&&(Sum$(abs(GenPart_pdgId)==23)==2)"
  cpTree = chain
  print "tree is copied"
  cpTree.Draw("GenSusyMGluino>>hgluino")
  bin_cont_temp = 0
  for cbin in range(0,hgluino.GetNbinsX()):
    if hgluino.GetBinContent(cbin) != 0: 
       bin_cont = hgluino.GetBin(cbin)
       if bin_cont != bin_cont_temp :
         mglu = hgluino.GetBin(cbin)-1
         print "gliuno mass:" , mglu
         mass_dict[mglu] = {}
         cpTree.Draw("GenSusyMNeutralino>>hlsp",cut_common+"&&GenSusyMGluino=="+str(mglu)) 
         lspbin_content_temp = 0
         for cnbin in range(0,hlsp.GetNbinsX()):
          if hlsp.GetBinContent(cnbin) != 0:
            bin_cont_lsp = hlsp.GetBin(cnbin) 
            if bin_cont_lsp != lspbin_content_temp :
              mlsp = hlsp.GetBin(cnbin)-1
              print "=====lsp mass:" , mlsp
              mass_dict[mglu][mlsp] = {}
              nEntry = cpTree.GetEntries(cut_common+"&&GenSusyMGluino=="+str(mglu)+"&&GenSusyMNeutralino=="+str(mlsp))
              m_xsec = gluino13TeV_NLONLL[mglu]
              mass_dict[mglu][mlsp] = {"nEntry": nEntry , "xsec":m_xsec }
            lspbin_content_temp = bin_cont_lsp
       bin_cont_temp = bin_cont
  print mass_dict

  pickle.dump(mass_dict, file(pickleDir+sample["name"]+'_mass_nEvents_xsec_'+sample_label+'_pkl','w'))
  print "written:" , pickleDir+sample["name"]+'_mass_nEvents_xsec_'+sample_label+'_pkl'
