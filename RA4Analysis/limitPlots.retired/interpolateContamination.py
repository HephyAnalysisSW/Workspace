import ROOT
import sys
import os

#
# find range and spacing of a 1D grid of masses
#   returns tuple of ( delta, min, max )
#
def findRange (ms):
  dm0 = None
  m0 = None
  m0min = None
  m0max = None
  for im in ms:
    if m0 == None:
      m0min = im
      m0max = im
    else:
      dm = abs(im-m0)
      if dm > 0 and ( dm0 == None or dm < dm0 ):  dm0 = dm
      if im < m0min:  m0min = im
      if im > m0max:  m0max = im
    m0 = im;
  return ( dm0,m0min,m0max)

#
# read contamination from ROOT files (in WKs format) and interpolate
#   write result to a new dictionary
#
def interpolateContamination(htbin,metbin, inDir, th2Binning):
  try:
    type(ROOT.triangular)
  except:
    ROOT.gROOT.ProcessLine(".L TriangularInterpolation.C+")

#  th2Binning["T1tttt-madgraph"] = [48, 400, 1600, 52, 0, 1300]
#  nbglu = 47
#  mglurange = [ 25., 350., 1500. ]
#  nbneut = 43
#  mneutrange = [ 25., 0., 1050. ]
#
#  hInter = ROOT.TH2F("hCont","hCont", \
#                   nbglu,mglurange[1]-mglurange[0]/2.,mglurange[2]+mglurange[0]/2., \
#                   nbneut,mneutrange[1]-mneutrange[0]/2.,mneutrange[2]+mneutrange[0]/2.)
  hInter = ROOT.TH2F("hCont","hCont", *th2Binning)


  currDir = ROOT.gDirectory
  filename = inDir+"/c_sigcont_"
  filename += str(htbin[0])+"_ht_"+str(htbin[1])+"_"
  filename += str(metbin[0])+"_met_"+str(metbin[1])+".root"
  if not os.path.exists(filename):
    print "Missing file with contamination information",filename
#    sys.exit(1)
    return None
  print filename
  file = ROOT.TFile(filename)
  hInter.Reset()
  for iglu in range(th2Binning[0]): #nbglu = th2Binning[0]
    mglu = int(hInter.GetXaxis().GetBinCenter(iglu+1)+0.5)
    for ineut in range(th2Binning[3]):
      mneut = int(hInter.GetYaxis().GetBinCenter(ineut+1)+0.5)
#      if (mglu-mneut)>=350:  hInter.SetBinContent(iglu+1,ineut+1,1.)
      hInter.SetBinContent(iglu+1,ineut+1,1.)
  hInter = ROOT.triangular(hInter,file)
  #hInter.Smooth()
  file.Close()
  currDir.cd()
  return hInter
