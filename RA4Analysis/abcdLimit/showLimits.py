import ROOT
import pickle
import os,sys
from array import array

def drawContours(cnv,h,lstyle,lwidth):
    hc = h.Clone()
    for ix in range(h.GetXaxis().GetNbins()):
        for iy in range(h.GetYaxis().GetNbins()):
            c = hc.GetBinContent(ix+1,iy+1)
            if c<0.000001:
                hc.SetBinContent(ix+1,iy+1,999999.)
    levels = array('d',[1.])
    hc.SetContour(1,levels)
    cc = ROOT.TCanvas()
    hc.Draw("cont list")
    cc.Update()
    
    cnv.cd()
    result = [ ]
    conts = ROOT.gROOT.GetListOfSpecials().FindObject("contours")
    for c in conts:
        for g in c:
            if g.GetN()>5:
                result.append(g.Clone())
                result[-1].SetLineStyle(lstyle)
                result[-1].SetLineWidth(lwidth)
#                result[-1].Draw("C")
                print "Drawing graph with ",g.GetN()," points"
    return result

results = pickle.load(file(sys.argv[1]))

fnstyle = os.path.expandvars("$WORK/susy/CMSSW_7_4_14/src/Workspace/HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.gROOT.ProcessLine(".L "+fnstyle)
ROOT.setTDRStyle()

fncolor = os.path.expandvars("$WORK/susy/CMSSW_7_4_14/src/Workspace/HEPHYPythonTools/scripts/root/useNiceColorPalette.C")
ROOT.gROOT.ProcessLine(".L "+fncolor)
ROOT.useNiceColorPalette()

mglus = set()
mlsps = set()
for mg in results:
    if not mg in mglus:
        mglus.add(mg)
    for ml in results[mg]:
        if not ml in mlsps:
            mlsps.add(ml)

mglus = sorted(mglus)
dmgs = [ ]
for i in range(len(mglus)-1):
    dm = mglus[i+1] - mglus[i]
    if not dm in dmgs:
        dmgs.append(dm)
dmgs.sort()
print mglus
print dmgs
print " "

mlsps = sorted(mlsps)
dmls = [ ]
for i in range(len(mlsps)-1):
    dm = mlsps[i+1] - mlsps[i]
    if not dm in dmls:
        dmls.append(dm)
dmls.sort()
print mlsps
print dmls

dmglu = 25.
#dmglu = 50.
mgluMin = mglus[0]
mgluMax = mglus[-1]
nmglu = int((mgluMax-mgluMin)/dmglu+1.5)

dmlsp = 25.
#dmlsp = 50.
mlspMin = 0.
mlspMax = mlsps[-1]
nmlsp = int((mlspMax-mlspMin)/dmlsp+1.5)

hNames = { "obs" : "-1.000", "expM1" : "0.160", "exp" : "0.500", "expP1" : "0.840" }
histos = { }

for hn in hNames:
    h = ROOT.TH2F(hn,hn, \
                      nmglu,mgluMin-dmglu/2.,mgluMax+dmglu/2., \
                      nmlsp,mlspMin-dmlsp/2.,mlspMax+dmlsp/2.)
    h.SetMinimum(0.001)
    h.SetMaximum(100.)
    h.GetXaxis().SetTitleSize(0.05)
    h.GetXaxis().SetTitleOffset(1.1)
    h.GetXaxis().SetTitle("m(#tilde{g}) [GeV]")
    h.GetYaxis().SetTitleSize(0.05)
    h.GetYaxis().SetTitleOffset(1.5)
    h.GetYaxis().SetTitle("m(#tilde{#chi}_{1}^{0}) [GeV]")
    h.GetZaxis().SetTitleSize(0.05)
    h.GetZaxis().SetTitleOffset(1.5)
    h.GetZaxis().SetTitle("95% CL limit on signal strength")
    histos[hn] = h

for mg in results:
    ix = histos["obs"].GetXaxis().FindBin(float(mg))
    for ml in results[mg]:
        iy = histos["obs"].GetYaxis().FindBin(float(ml))
        lims = results[mg][ml]
        for hn in hNames:
            h = histos[hn]
            lim = lims[hNames[hn]]
            h.SetBinContent(ix,iy,lim)

cObs = ROOT.TCanvas("obs","observed",700,600)
cObs.SetRightMargin(0.20)
histos["obs"].Draw("zcol")
cObs.SetLogz(1)
rObs = drawContours(cObs,histos["obs"],1,3)
#cObs.Update()

#marker = ROOT.TMarker()
#for mg in results:
#    ix = histos["obs"].GetXaxis().FindBin(float(mg))
#    for ml in results[mg]:
#        iy = histos["obs"].GetYaxis().FindBin(float(ml))
#        marker.DrawMarker(float(mg),float(ml))

cExp = ROOT.TCanvas("exp","expected",700,600)
cExp.SetRightMargin(0.20)
histos["exp"].Draw("zcol")
rExp = drawContours(cExp,histos["exp"],2,3)
rExpM1 = drawContours(cExp,histos["expM1"],2,1)
rExpP1 = drawContours(cExp,histos["expP1"],2,1)
cExp.SetLogz(1)
#cExp.Update()

cObs.cd()
for g in rObs+rExp+rExpM1+rExpP1:
    g.Draw("C")
cObs.Update()
cExp.cd()
for g in rObs+rExp+rExpM1+rExpP1:
    g.Draw("C")
cExp.Update()
