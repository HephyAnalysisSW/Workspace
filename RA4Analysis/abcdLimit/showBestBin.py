import ROOT
import pickle
import os,sys

binDefs = (
 ((5, 5), (250, 350), (500, -1)),
 ((5, 5), (350, 450), (500, -1)),
 ((5, 5), (450, -1), (500, -1)),
 ((6, 7), (250, 350), (500, 750)),
 ((6, 7), (250, 350), (750, -1)),
 ((6, 7), (350, 450), (500, 750)),
 ((6, 7), (350, 450), (750, -1)),
 ((6, 7), (450, -1), (500, 1000)),
 ((6, 7), (450, -1), (1000, -1)),
 ((8, -1), (250, 350), (500, 750)),
 ((8, -1), (250, 350), (750, -1)),
 ((8, -1), (350, 450), (500, -1)),
 ((8, -1), (450, -1), (500, -1))
)

def rangeToText(name,rng):
    if rng[0]==rng[1]:
        result = name+"="+str(rng[0])
    elif rng[1]==-1:
        result = name+" \geq "+str(rng[0])
    else:
        result = str(rng[0])+" \leq "+name+" \leq "+str(rng[1])
    return result

def binToName(bdef):
#    jets = bdef[0]
#    result = rangeToText("n_{jet}",bdef[0])
#    result += ", "
    result = rangeToText("L_{T}",bdef[1])
    result += ", "
    result += rangeToText("H_{T}",bdef[2])
    return result

fnstyle = os.path.expandvars("$WORK/susy/CMSSW_7_4_14/src/Workspace/HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.gROOT.ProcessLine(".L "+fnstyle)
ROOT.setTDRStyle()
ROOT.gStyle.SetPadRightMargin(0.10)

fncolor = os.path.expandvars("$WORK/susy/CMSSW_7_4_14/src/Workspace/HEPHYPythonTools/scripts/root/useNiceColorPalette.C")
ROOT.gROOT.ProcessLine(".L "+fncolor)
ROOT.useNiceColorPalette()

#
# define full set of mass points
#
mglus = set()
mlsps = set()
expLimits = { }

for ibin in range(13):

    results = pickle.load(file(sys.argv[1]+"_bin"+str(ibin)+".pkl"))
    
    for mg in results:
        mglus.add(mg)
        if not mg in expLimits:
            expLimits[mg] = { }
        for ml in results[mg]:
            mlsps.add(ml)
            if not ml in expLimits[mg]:
                expLimits[mg][ml] = [ ]
            if '0.500' in results[mg][ml]:
                expLimits[mg][ml].append(results[mg][ml]['0.500'])
            else:
                print "Expectation missing from ",ibin,mg,ml
                expLimits[mg][ml].append(None)
#
# define frame histograms
#
mgluMin = min(mglus)
mgluMax = max(mglus)
dmglu = mgluMax - mgluMin

mlspMin = min(mlsps)
mlspMax = max(mlsps)
dmlsp = mlspMax - mlspMin

cnv = ROOT.TCanvas("cnv","cnv",900,800)
frame = cnv.DrawFrame(mgluMin-0.05*dmglu,0.,mgluMax+0.05*dmglu,mlspMax+0.05*dmlsp)
frame.GetXaxis().SetTitle("m_{#tilde{g}} [GeV]")
frame.GetYaxis().SetTitle("m_{#tilde{#chi_{1}^{0}}} [GeV]")
cnv.Update()

text = ROOT.TLatex()
text.SetTextAlign(22)
text.SetTextSize(0.018)
markers = [ ]
for ibin in range(13):
    markers.append(ROOT.TMarker())
    markers[-1].SetMarkerSize(1.75)

leg = ROOT.TLegend(0.165,0.61,0.55,0.93)
leg.SetBorderSize(0)
leg.SetFillStyle(0)
leg.SetMargin(0.1)
leg.SetEntrySeparation(-0.4)

nj = binDefs[0][0]
leg.AddEntry(0,rangeToText("n_{jet}",nj),"")
ics = [ ROOT.kGreen, ROOT.kGreen+1, ROOT.kGreen+2, ROOT.kGreen-7, ROOT.kGreen-9, ROOT.kGreen+4 ]
for ibin in range(3):
    assert nj==binDefs[ibin][0]
    markers[ibin].SetMarkerStyle(21)
    markers[ibin].SetMarkerColor(ics.pop())
#    leg.AddEntry(markers[ibin],"Bin"+str(ibin),"P")
    leg.AddEntry(markers[ibin],binToName(binDefs[ibin]),"P")

nj = binDefs[3][0]
leg.AddEntry(0,rangeToText("n_{jet}",nj),"")
ics = [ ROOT.kBlue, ROOT.kBlue+1, ROOT.kBlue+2, ROOT.kBlue-7, ROOT.kBlue-9, ROOT.kBlue+4 ]
for ibin in range(3,9):
    assert nj==binDefs[ibin][0]
    markers[ibin].SetMarkerStyle(21)
    markers[ibin].SetMarkerColor(ics.pop())
    leg.AddEntry(markers[ibin],binToName(binDefs[ibin]),"P")

nj = binDefs[9][0]
leg.AddEntry(0,rangeToText("n_{jet}",nj),"")
ics = [ ROOT.kRed, ROOT.kRed+1, ROOT.kRed+2, ROOT.kRed-7, ROOT.kRed-9, ROOT.kRed+4 ]
for ibin in range(9,13):
    assert nj==binDefs[ibin][0]
    markers[ibin].SetMarkerStyle(21)
    markers[ibin].SetMarkerColor(ics.pop())
    leg.AddEntry(markers[ibin],binToName(binDefs[ibin]),"P")
    # leg.AddEntry(markers[ibin],"Bin"+str(ibin),"P")

for mg in expLimits:
    for ml in expLimits[mg]:
        ibmin = None
        lmin = None
        # assert len(expLimits[mg][ml])==13
        for i,l in enumerate(expLimits[mg][ml]):
            if l!=None and ( ibmin==None or lmin==None or l<lmin ):
                ibmin = i
                lmin = l
        if lmin!=None:
            xp = ROOT.Double(mg)
            yp = ROOT.Double(ml)
            markers[ibmin].DrawMarker(xp,yp)
            text.DrawLatex(xp,yp,str(ibmin))
leg.Draw()
cnv.Update()
cnv.SaveAs("ZeroBBestBin.pdf")
cnv.SaveAs("ZeroBBestBin.png")
