import os, sys, ROOT
ROOT.gROOT.ProcessLine(".L ../scripts/tdrstyle.C")
ROOT.setTDRStyle()
ROOT.tdrStyle.SetPadRightMargin(0.20)

ROOT.gROOT.ProcessLine(".L ../scripts/useNiceColorPalette.C")
ROOT.useNiceColorPalette(255)
ROOT.gROOT.ProcessLine(".L TriangularInterpolation.C+")
ROOT.gROOT.ProcessLine(".L SmoothingUtils.C+")
path = os.path.abspath('../plots')
if not path in sys.path:
    sys.path.insert(1, path)
del path
from analysisHelpers import getObjFromFile

requ = "T5tttt"

subDirName = "/afs/hephy.at/user/s/schoefbeck/www/pngSys/"
filelist=os.listdir(subDirName)
for filename in filelist:
  if not filename[-5:]==".root":continue
  if filename.count("smoothed"):continue
  if not filename.count(requ):continue
  print subDirName+filename
  os.system("python smootheOneFile.py "+subDirName+"/"+filename) 
