import ROOT
from math import *
from simplePlotsCommon import *

ROOT.tdrStyle.SetPadRightMargin(0.16)
ROOT.gROOT.ProcessLine(".L ../scripts/useNiceColorPalette.C")
ROOT.useNiceColorPalette(255)

run = "205236"
#run = "204601"
dir = "/data/schoef/qpll/"+run+"/"
pT = 60

qdef = ROOT.TChain("Events")
qmod = ROOT.TChain("Events")
qdef.Add(dir+"/def/h*.root")
qmod.Add(dir+"/mod/h*.root")

#qdef.Draw("jetsPtUncorr*cosh(jetsEta):jetsPhi:jetsEta>>hdef(80, -5, 5, 80, -4, 4);#phi;#eta", "(jetsPtUncorr>20&&jetsID&&jetsMuCleaned&&jetsEleCleaned)", "prof")
#qmod.Draw("jetsPtUncorr*cosh(jetsEta):jetsPhi:jetsEta>>hmod(80, -5, 5, 80, -4, 4);#phi;#eta", "(jetsPtUncorr>20&&jetsID&&jetsMuCleaned&&jetsEleCleaned)", "prof")
qdef.Draw("jetsPtUncorr:jetsPhi:jetsEta>>hdef(30, -5, 5, 30, -pi, pi)", "(jetsPtUncorr>"+str(pT)+"&&jetsID&&jetsMuCleaned&&jetsEleCleaned)", "prof")
qmod.Draw("jetsPtUncorr:jetsPhi:jetsEta>>hmod(30, -5, 5, 30, -pi, pi)", "(jetsPtUncorr>"+str(pT)+"&&jetsID&&jetsMuCleaned&&jetsEleCleaned)", "prof")

c1 = ROOT.TCanvas()
c1.SetLogz()
hmod = ROOT.gDirectory.Get("hmod")
hmod.Draw("COLZ")
c1.Print("/afs/hephy.at/user/s/schoefbeck/www/Qpll/jetsPtUncorr_"+str(pT)+"_"+run+"_mod.png")

hdef = ROOT.gDirectory.Get("hdef")
hdef.Draw("COLZ")
c1.Print("/afs/hephy.at/user/s/schoefbeck/www/Qpll/jetsPtUncorr_"+str(pT)+"_"+run+"_def.png")

c1.SetLogz(0)
qdiff = hmod.Clone()
qdiff.Scale(-1)
qdiff.Add(hdef)
qdiff.Scale(-1)
c1 = ROOT.TCanvas()
c1.SetLogx(0)
c1.SetLogy(0)
c1.SetLogz(0)
qdiff.GetZaxis().SetRangeUser(-10,10)
qdiff.Draw("COLZ")
c1.Print("/afs/hephy.at/user/s/schoefbeck/www/Qpll/jetsPtUncorr_"+str(pT)+"_"+run+"_diff.png")

del hmod, hdef
