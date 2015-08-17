import ROOT
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain, getChunks, getObjDict, getVarValue
from Workspace.HEPHYPythonTools.xsec import xsec
ROOT.gROOT.LoadMacro("$CMSSW_BASE/src/Workspace/HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()
ROOT.gROOT.ProcessLine(".L $CMSSW_BASE/src/Workspace/HEPHYPythonTools/scripts/root/useNiceColorPalette.C+")
ROOT.useNiceColorPalette()

from Workspace.RA4Analysis.cmgTuples_Spring15_150809 import *

lumi=100.
small = False

samples=[ 
  {"name":"DY", "bins":[DYJetsToLL_M50_25ns_CERNRerun], "legendText":"Drell-Yan"}
]

maxN = 10 if small else -1
for s in samples:
  totalYield=0
  for b in s["bins"]:
    chunks, sumWeight = getChunks(b, maxN=maxN)
#    print "Chunks:" , chunks
    lumiScale = xsec[b['dbsName']]*lumi/float(sumWeight)
    b["lumiScale"] = lumiScale
    b["chain"]     = getChain(chunks,  histname="", treeName = b["treeName"])
    print b["name"],"xsec",xsec[b['dbsName']],"sumWeight",sumWeight

DYJetsToLL_M50_25ns_CERNRerun['chain'].Draw('Jet_pt/Jet_rawPt:Jet_eta','','COLZ')
