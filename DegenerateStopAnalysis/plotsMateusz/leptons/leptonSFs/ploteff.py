from ROOT import *
from math import *
import os, sys
import array

datatag = "2016_80X_v5"

binning = [3.5, 5., 10., 20., 30., 45., 60.]
x1 = array.array("d",binning)
nb = len(x1)-1

mineff = 0.3
maxeff = 1.05
minsf = 0.7
maxsf = 1.05

flavor = "muon"
if len(sys.argv)>1: flavor = sys.argv[1]
if flavor != "muon" and flavor != "ele":
    print "wrong flavor"
    sys.exit()

stage = "Id"
if len(sys.argv)>2: stage = sys.argv[2]
if stage != "IpIso" and stage != "Id" and stage != "IdSpec" and stage != "IpIsoSpec":
    print "wrong stage"
    sys.exit()

etabin = "all"
if len(sys.argv)>3: etabin = sys.argv[3]
if etabin != "barrel" and etabin != "endcap" and etabin != "all":
    print "wrong etabin"
    sys.exit()

plotcount = 1
if len(sys.argv)>4: plotcount = int(sys.argv[4])

def makeDir(path):
    if "." in path[-5:]:
        path = path.replace(os.path.basename(path),"")
        print path
    if os.path.isdir(path):
        return
    else:
        os.makedirs(path)

def divideEff(e1,e2):
    n = e1.GetTotalHistogram().GetNbinsX()
    res = TGraphAsymmErrors(n)
    for i in range(n):
        a = e1.GetTotalHistogram().GetBinLowEdge(i+1)
        w = e1.GetTotalHistogram().GetBinWidth(i+1)
        v1 = e1.GetEfficiency(i+1)
        u1 = e1.GetEfficiencyErrorUp(i+1)
        d1 = e1.GetEfficiencyErrorLow(i+1)
        v2 = e2.GetEfficiency(i+1)
        u2 = e2.GetEfficiencyErrorUp(i+1)
        d2 = e2.GetEfficiencyErrorLow(i+1)
        if v1*v2 == 0:
            v = 0.
            u = 0.
            d = 0.
        else:
            v = v1/v2 if v2>0. else 0.
            u = v*sqrt(pow(u1/v1,2)+pow(u2/v2,2))
            d = v*sqrt(pow(d1/v1,2)+pow(d2/v2,2))
        print i,v,u,d
        x = a+0.5*w
        res.SetPoint(i,x,v)
        res.SetPointError(i,0.,0.,d,u)
    return res

def gethistbin(h,x):
    if x > binning[-1]:
        ib = nb+1
        return ib
    if x < binning[0]:
        ib = 0
        return ib
    for i in xrange(nb):
        if x > binning[i] and x < binning[i+1]:
            ib = i+1
            return ib
    return -999
    
def converttohist(g,n):
    h = TH1F(n,"",nb,x1)
    h.Sumw2()
    for i in xrange(g.GetN()):
        x = Double(0.)
        y = Double(0.)
        g.GetPoint(i,x,y)
        eyh = g.GetErrorYhigh(i)
        eyl = g.GetErrorYlow(i)
        ey = max(eyh,eyl)
        ibin = gethistbin(h,x)
        h.SetBinContent(ibin,y)
        h.SetBinError(ibin,ey)
    h1c = h.Clone()
    h1c.Print("all")
    return h1c

gStyle.SetOptStat(kFALSE)
c1 = TCanvas("c1","",700,700)
leg = TLegend(0.4,0.2,0.85,0.45)

Hdummy = TH1F("Hdummy","",10,0,60)
Hdummy.SetMinimum(mineff)
Hdummy.SetMaximum(maxeff)
Hdummy.SetXTitle("p_{T} (GeV)")
Hdummy.SetYTitle("efficiency")
Hdummy.GetYaxis().SetTitleOffset(1.4)
Hdummy.Draw()

if flavor == "ele":
    suffix = "_"+etabin
else:
    suffix = ""

f = TFile("results/%s/fits/%s_result_MC_%s%s.root"%(datatag,flavor,stage,suffix))
effcntZMC = TEfficiency(f.Get("effcnt"))
efffitZMC = TEfficiency(f.Get("efffit"))
f.Close()
f = TFile("results/%s/fits/%s_result_Data_%s%s.root"%(datatag,flavor,stage,suffix))
effcntZData = TEfficiency(f.Get("effcnt"))
efffitZData = TEfficiency(f.Get("efffit"))
f.Close()

if plotcount:
    effcntZMC.SetMarkerStyle(20)
    effcntZMC.SetMarkerColor(2)
    effcntZMC.SetLineColor(2)
    effcntZMC.Draw("same")
    leg.AddEntry(effcntZMC,"Z MC counting T&P","lpe")

    effcntZData.SetMarkerStyle(20)
    effcntZData.SetMarkerColor(kOrange)
    effcntZData.SetLineColor(kOrange)
    effcntZData.Draw("same")
    leg.AddEntry(effcntZData,"Z Data counting T&P","lpe")


efffitZMC.SetMarkerStyle(20)
efffitZMC.SetMarkerColor(4)
efffitZMC.SetLineColor(4)
efffitZMC.Draw("same")
leg.AddEntry(efffitZMC,"Z MC fit T&P","lpe")

efffitZData.SetMarkerStyle(20)
efffitZData.SetMarkerColor(7)
efffitZData.SetLineColor(7)
efffitZData.Draw("same")
leg.AddEntry(efffitZData,"Z Data fit T&P","lpe")


leg.Draw()
gPad.Update()

savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/TnP/%s/finalplots/%s"%(datatag,stage)
makeDir(savedir)
makeDir("results/%s/finalplots"%datatag)

c1.SaveAs("results/%s/finalplots/%s_eff_%s_%s.png"%(datatag,flavor,stage,etabin))
c1.SaveAs("%s/%s_eff_%s_%s.png"%(savedir,flavor,stage,etabin))
fout = TFile("results/%s/finalplots/%s_eff_%s_%s.root"%(datatag,flavor,stage,etabin),"RECREATE")
c1c = c1.Clone()
c1c.Write()
fout.Close()


c2 = TCanvas("c2","",700,700)
leg2 = TLegend(0.4,0.25,0.85,0.4)

Hdummy.SetYTitle("Data/MC scale factor")
Hdummy.SetMinimum(minsf)
Hdummy.SetMaximum(maxsf)
Hdummy.Draw()

print plotcount
if plotcount:
    print plotcount
    SFcntZ = divideEff(effcntZData,effcntZMC)
    SFcntZ.SetMarkerStyle(20)
    SFcntZ.SetMarkerColor(2)
    SFcntZ.SetLineColor(2)
    SFcntZ.Draw("same p")
    leg2.AddEntry(SFcntZ,"Z counting T&P","lpe")

SFfitZ = divideEff(efffitZData,efffitZMC)
SFfitZ.SetMarkerStyle(20)
SFfitZ.SetMarkerColor(4)
SFfitZ.SetLineColor(4)
SFfitZ.Draw("same p")
leg2.AddEntry(SFfitZ,"Z fit T&P","lpe")


leg2.Draw()
gPad.Update()

c2.SaveAs("results/%s/finalplots/%s_SF_%s_%s.png"%(datatag,flavor,stage,etabin))
c2.SaveAs("%s/%s_SF_%s_%s.png"%(savedir,flavor,stage,etabin))
fout = TFile("results/%s/finalplots/%s_SF_%s_%s.root"%(datatag,flavor,stage,etabin),"RECREATE")
c2c = c2.Clone()
c2c.Write()
fout.Close()

fsfout = TFile("results/%s/finalplots/hephy_scale_factors.root"%datatag,"update")
H_SFfitZ_name = "{0}_SF_{1}_{2}".format(flavor,stage,etabin)
fsfout.Delete(H_SFfitZ_name+";*")

H_SFfitZ = converttohist(SFfitZ,H_SFfitZ_name)

fsfout.Write()
fsfout.Close()
