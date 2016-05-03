import ROOT
import pickle
from Workspace.HEPHYPythonTools.user import username
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain, getChunks, getCutYieldFromChain, getYieldFromChain
from Workspace.RA4Analysis.cmgTuples_Spring15_MiniAODv2_25ns import *
from Workspace.HEPHYPythonTools.xsecSMS import *
from math import *

def tryGluLSP(mass_dict, mglu, mlsp, def_val = 0):
    try:
        mass_dict[mglu]
    except KeyError:
        mass_dict[mglu]={}
    try:
        mass_dict[mglu][mlsp]
    except KeyError:
        mass_dict[mglu][mlsp]=def_val


VV_label = "WZ"    ###can be WW , WZ , ZZ

samples = [T5qqqqVV_mGluino_600To675_mLSP_1to550, T5qqqqVV_mGluino_700To775_mLSP_1To650, T5qqqqVV_mGluino_800To975_mLSP_1To850, T5qqqqVV_mGluino_1000To1075_mLSP_1To950,\
           T5qqqqVV_mGluino_1100To1175_mLSP_1to1050, T5qqqqVV_mGluino_1200To1275_mLSP_1to1150, T5qqqqVV_mGluino_1300To1375_mLSP_1to1250, T5qqqqVV_mGluino_1400To1550_mLSP_1To1275,\
            T5qqqqVV_mGluino_1600To1750_mLSP_1To950  ]
#samples = [T5qqqqVV_mGluino_600To675_mLSP_1to550,T5qqqqVV_mGluino_700To775_mLSP_1To650]
pickleDir = '/data/'+username+'/Spring15/25ns/'

def getGluLSPInfo(sample):
  VV_label = "WZ"    ###can be WW , WZ , ZZ

  ###T5qqqqWW
  if VV_label == "WW" :
    print "I am at WW"
    cut_common = "Sum$(abs(GenPart_pdgId)==1000022&&abs(GenPart_motherId)==1000024&&abs(GenPart_grandmotherId)==1000021)==2&&(Sum$(abs(GenPart_pdgId)==24)==2)"
  ###T5qqqqWZ
  if VV_label == "WZ" :
    print "I am at WZ"
    cut_common = "Sum$(abs(GenPart_pdgId)==1000022&&abs(GenPart_motherId)==1000024&&abs(GenPart_grandmotherId)==1000021)==1&&Sum$(abs(GenPart_pdgId)==1000022&&abs(GenPart_motherId)==1000023&&abs(GenPart_grandmotherId)==1000021)==1&&Sum$(abs(GenPart_pdgId)==23)==1&&Sum$(abs(GenPart_pdgId)==24)==1&&(Sum$(abs(GenPart_pdgId)==23)+Sum$(abs(GenPart_pdgId)==24))==2"
  ###T5qqqqZZ
  if VV_label == "ZZ" :
    print "I am at ZZ"
    cut_common = "Sum$(abs(GenPart_pdgId)==1000022&&abs(GenPart_motherId)==1000023&&abs(GenPart_grandmotherId)==1000021)==2&&(Sum$(abs(GenPart_pdgId)==23)==2)"
  if VV_label == "VV" :
    print "I am at VV"
    cut_common = "(1)"

  print sample , cut_common
  sample_name = sample["name"]
  print sample["name"]
  chunks = getChunks(sample, maxN=-1)
  chain = getChain(chunks[0], maxN=-1, treeName='tree')
  mass_dict = {}  

  hist_name = "glu_lsp_%s"%sample_name
  hist = ROOT.TH2D(hist_name, hist_name, 2000,0,2000, 2000 , 0, 2000)

  chain.Draw("GenSusyMNeutralino:GenSusyMGluino>>%s"%hist_name,cut_common)

  for xbin in xrange(hist.GetNbinsX()):
    for ybin in xrange(hist.GetNbinsY()):
      mglu, mlsp = xbin-1 , ybin-1 
      bin_cont = hist.GetBinContent(xbin,ybin)
      if bin_cont > 1e-07 :
        print "gliuno mass:" , mglu , "    lsp mass :" , mlsp
        print "bin content: " , bin_cont
        #nEntry = chain.GetEntries(cut_common+"&&GenSusyMGluino=="+str(mglu)+"&&GenSusyMNeutralino=="+str(mlsp))
        #print "nEntry:" , nEntry
        #nEntry = bin_cont
        m_xsec = gluino13TeV_NLONLL[mglu]
        tryGluLSP(mass_dict, mglu, mlsp, def_val= {"nEntry":0, "xSec": m_xsec  } )
        mass_dict[mglu][mlsp]["nEntry"] = bin_cont
        mass_dict[mglu][mlsp]["xSec"] = m_xsec
  return mass_dict

if __name__ == "__main__":

  import multiprocessing
  pool = multiprocessing.Pool(10)
  print samples
  results = pool.map(getGluLSPInfo , samples)
  #print results
  pool.close()
  pool.join()

  final_dict = {}
  for res in results:
    final_dict.update(res) 
  pickle.dump(final_dict, file(pickleDir+'T5qqqq'+VV_label+'_mass_nEvents_xsec_pkl','w'))
  print "written:" , pickleDir+'T5qqqq'+VV_label+'_mass_nEvents_xsec_pkl'
