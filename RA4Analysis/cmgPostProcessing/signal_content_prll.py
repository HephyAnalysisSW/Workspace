import ROOT
import pickle
from Workspace.HEPHYPythonTools.user import username
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain, getChunks, getCutYieldFromChain, getYieldFromChain
from Workspace.RA4Analysis.cmgTuples_Spring16_MiniAODv2 import *
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


samples = [SMS_T5qqqqVV_TuneCUETP8M1] # , SMS_T5qqqqVV_TuneCUETP8M1_v2 ]
#samples = [T5qqqqVV_mGluino_600To675_mLSP_1to550,T5qqqqVV_mGluino_700To775_mLSP_1To650]
pickleDir = '/afs/hephy.at/data/easilar01/Ra40b/pickleDir/'

VV_label = "WW"    ###can be WW , WZ , ZZ

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

def getGluLSPInfo(sample):
  cut_common = "Sum$(abs(GenPart_pdgId)==1000022&&abs(GenPart_motherId)==1000024&&abs(GenPart_grandmotherId)==1000021)==2&&(Sum$(abs(GenPart_pdgId)==24)==2)"
  #print sample , cut_common
  #sample_name = sample["name"]
  #print sample["name"]
  #chunks = getChunks(sample, maxN=-1)
  #chain = getChain(chunks[0], maxN=-1, treeName='tree')
  chain = sample
  mass_dict = {}  

  #hist_name = "glu_lsp_%s"%sample_name
  hist = ROOT.TH2D("hist", "hist", 3000,0,3000, 3000 , 0, 3000)

  #chain.Draw("GenSusyMNeutralino:GenSusyMGluino>>%s"%hist_name,cut_common)
  chain.Draw("GenSusyMNeutralino:GenSusyMGluino>>hist",cut_common)
  
  #file = ROOT.TFile("/afs/hephy.at/user/e/easilar/www/data/Run2016B/7p7fb/plots/signal_crosscheck_plots/T5qqqqWW_mass_plain.root")
  #can = file.Get("cb")
  #hist = can.GetPrimitive("glu_lsp")

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

#if __name__ == "__main__":

#import multiprocessing
#pool = multiprocessing.Pool(10)
print samples
chunks0 = getChunks(samples[0], maxN=-1)
#chunks1 = getChunks(samples[1], maxN=-1)
chain = getChain(chunks0[0], maxN=-1, treeName='tree')
results = getGluLSPInfo(chain)
#results = pool.map(getGluLSPInfo , chain)
print results
#pool.close()
#pool.join()
 
pickle.dump(results, file(pickleDir+'T5qqqq'+VV_label+'_mass_nEvents_xsec_fullChunks_pkl','w'))
print "written:" , pickleDir+'T5qqqq'+VV_label+'_mass_nEvents_xsec_fullChunks_pkl'
