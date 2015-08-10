import ROOT
from array import array
from math import *
import os, copy, sys
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain, getChunks
import Workspace.HEPHYPythonTools.xsec as xsec
from Workspace.RA4Analysis.helpers import *

from Workspace.RA4Analysis.cmgTuples_Spring15 import *

lumi=100.
samples={ 
  {"name":"DY", "bins":[DYJetsToLL_M_50], "title":"Drell-Yan"]}
}

for s in samples:
  totalYield=0
  for b in s["bins"]:
    chunks, sumWeight = getChunks(b)
    print "Chunks:" , chunks
    lumiScale = xsec[b['dbsName']]*lumi/float(sumWeight)

    b["lumiScale"] = lumiScale
    b["chain"]     = getChain(b)
    print b["name"],"xsec",xsec.xsec[b['dbsName']],"sumWeight",sumWeight


#          genWeight = t.GetLeaf('genWeight').GetValue()
#          s.weight = prelumiWeight*genWeight


#commoncf = "njets>=4&&ht>400&&nTightMuons+nTightElectrons==1&&nbtags==0&&(ht>750&&met>350)&&htThrustLepSideRatio>0.4"
#c.Draw('>>eList', commoncf)
#eList = ROOT.gDirectory.Get('eList')
#
#n=100
#for e in range(min([n, eList.GetN()])):
#  stuff=[]
