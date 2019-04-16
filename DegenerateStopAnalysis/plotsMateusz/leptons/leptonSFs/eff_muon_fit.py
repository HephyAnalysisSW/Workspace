from ROOT import *
from math import *
import os, sys
import array

datatag = "2016_80X_v5"

binning = [3.5, 5., 10., 20., 30., 45., 60.]
x1 = array.array("d",binning)
nb = len(x1)-1
x2 = -999

mode = "Data"
if len(sys.argv)>1: mode = sys.argv[1]
if mode != "Data" and mode != "MC":
    print "wrong mode"
    sys.exit()

stage = "IpIso"
if len(sys.argv)>2: stage = sys.argv[2]
if stage != "IpIso" and stage != "Id" and stage != "IpIsoSpec":
    print "wrong stage"
    sys.exit()

etabin = 'all'
if len(sys.argv)>3: etabin = sys.argv[3]
if etabin not in ['all', 'barrel', 'endcap']:
    print "wrong etabin"
    sys.exit()

def makeDir(path):
    if "." in path[-5:]:
        path = path.replace(os.path.basename(path),"")
        print path
    if os.path.isdir(path):
        return
    else:
        os.makedirs(path)

pout = ["lowedge","pthigh","mean","sigma","sigma2","gaus1f","a","signal","bkg"]

makeDir("results/%s/fits"%datatag)

fpout = open("results/%s/fits/mu_%s_%s.params"%(datatag,mode,stage),"w")
sout = "\t".join(pout)
fpout.write(sout+"\n")

fin = TFile("results/%s/hists/mu_hists_%s_%s.root"%(datatag,mode,stage))
print fin

def getsigZ(hz,lowedge,pl=False):
#    x = RooRealVar("x","Mass (GeV/c^{2})", 75.,130.)
#    hz = TH1F("hz","",55,75,130)
    x = RooRealVar("x","Mass (GeV/c^{2})", 60.,130.)
    rdh = RooDataHist("rdh","",RooArgList(x),hz)
    x.setRange("R1",86,96)    
#    x.setRange("R1",60,120)    

    meang = RooRealVar("meang", "meang", 91., 88, 92)
    sigma1 = RooRealVar("sigma1", "sigma1", 2., 1.5, 2.5)
    sigma2 = RooRealVar("sigma2", "sigma2", 4., 3., 7.)
    n = RooRealVar("n", "", 1.,0.,50.)
    alpha = RooRealVar("alpha", "", 1.,0.,5.)
#    gaus1 = RooCBShape("gaus1","gaus1",x,meang,sigma1,alpha,n)
    gaus1 = RooGaussian("gaus1","gaus1",x,meang,sigma1)
    gaus2 = RooGaussian("gaus2","gaus2",x,meang,sigma2)
    gaus1f = RooRealVar("gaus1f","gaus1f",0.8,0.4,1.)
#    gaus1f = RooRealVar("gaus1f","gaus1f",1.)
    dgaus = RooAddPdf("dgaus","dgaus",gaus1,gaus2,gaus1f)
    
    amin = -0.08 if lowedge<50. else -0.035
    a = RooRealVar("a", "a",max(-0.06,amin), amin,-0.03)
#    a = RooRealVar("a", "", -10.,10.)

    expo = RooExponential("expo","exponential",x,a)
    
#    a0 = RooRealVar("a0", "", 1., -10.,10.)
#    a1 = RooRealVar("a1", "", 0., -1.,1.)
#    a2 = RooRealVar("a2", "", 0., -.1,.1)
#    a3 = RooRealVar("a3", "", 0., -.01,.01)
#    expo = RooChebychev("expo","exponential",x,RooArgList(a0,a1,a2,a3))
 
#    a0 = RooRealVar("a0", "", 115,90.,120.)
#    a1 = RooRealVar("a1", "", -20,-100.,100.)
#    expo = RooArgusBG("expo","exponential",x,a0,a1)
    
    
    signal = RooRealVar("signal", "signal", 1000, 0., 1.e9)
    bkg = RooRealVar("bkg", "", 100,0., 1.e9)

    dgex = RooAddPdf("dgex","dgex",RooArgList(dgaus,expo),RooArgList(signal,bkg))
    
    lowedgefit = 60
    if lowedge == 30: lowedgefit = 80
    if lowedge == 25: lowedgefit = 78
    if lowedge == 20: lowedgefit = 75
    if lowedge >= 35: lowedgefit = 82
    if lowedge >= 45: lowedgefit = 85
    fitres = dgex.fitTo(rdh,RooFit.Save(),RooFit.Range(lowedgefit,130),RooFit.Extended())

    if pl:
        xframe = x.frame()
        rdh.plotOn(xframe)
        dgex.plotOn(xframe)
        dgex.plotOn(xframe,RooFit.Components("dgaus"),RooFit.LineStyle(kDotted))
        dgex.plotOn(xframe,RooFit.Components("expo"),RooFit.LineStyle(kDashed))
        xframe.Draw()
    
    soutlist = [lowedge,pthigh,meang.getVal(),sigma1.getVal(),sigma2.getVal(),gaus1f.getVal(),a.getVal(),signal.getVal(),bkg.getVal()]
    sout = "\t".join(str(x) for x in soutlist)
    fpout.write(sout+"\n")
#    soutlist = [a0.getVal(),a1.getVal(),a2.getVal(),a3.getVal()]
#    sout = "---->"+"\t".join(str(x) for x in soutlist)
#    fpout.write(sout+"\n")

    return fitres.floatParsFinal().find("signal"),rdh.sumEntries("1","R1")

fout = TFile("results/%s/fits/muon_result_%s_%s.root"%(datatag,mode,stage),"recreate")

hpassfit = TH1F("hpassfit","",nb,x1)
hpassfit.Sumw2()
hfailfit = TH1F("hfailfit","",nb,x1)
hfailfit.Sumw2()
hpasscnt = TH1F("hpasscnt","",nb,x1)
hfailcnt = TH1F("hfailcnt","",nb,x1)

for ipt in range(len(binning)-1):
#for ipt in [1]:
    aux_ptlow = binning[ipt]
    pthigh = binning[ipt+1]
    print aux_ptlow,pthigh
    
    namestring = "{0:.1f}_{1:.1f}".format(aux_ptlow,pthigh)
    namestring = namestring.replace(".","p")
    namestring += '_' + etabin

    histname = "h_"+namestring+"_pass"
    print 'histname', histname
    
    savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/TnP/%s/fits/%s/%s"%(datatag,mode,stage)
    makeDir(savedir)

    fitp,cntp = getsigZ(fin.Get(histname),aux_ptlow,True)
    gPad.SaveAs("%s/muon_passing_%s_%s_%s.png"%(savedir,namestring,mode,stage))
    histname = "h_"+namestring+"_fail"
    fitf,cntf = getsigZ(fin.Get(histname),aux_ptlow,True)
    gPad.SaveAs("%s/muon_failing_%s_%s_%s.png"%(savedir,namestring,mode,stage))
    
    hpassfit.SetBinContent(ipt+1,fitp.getVal())
    hpassfit.SetBinError(ipt+1,fitp.getError())
    hfailfit.SetBinContent(ipt+1,fitf.getVal())
    hfailfit.SetBinError(ipt+1,fitf.getError())
    print ">>>",fitp.getVal(),fitp.getError(),fitf.getVal(),fitf.getError()

    hpasscnt.SetBinContent(ipt+1,cntp)
    hfailcnt.SetBinContent(ipt+1,cntf)
    

hhh = TH1F("hhh","",nb,x1)
hhh.SetMinimum(0.7)
hhh.SetMaximum(1.1)
hhh.Draw()
 
hallcnt = hpasscnt.Clone("hallcnt")
hallcnt.Add(hfailcnt)
effcnt = TEfficiency(hpasscnt,hallcnt)
effcnt.Draw("same")

hallfit = hpassfit.Clone("hallfit")
hallfit.Add(hfailfit)
efffit = TEfficiency(hpassfit,hallfit)
efffit.SetLineColor(2)
efffit.Draw("same")

effcnt.Write("effcnt")
efffit.Write("efffit")

fout.Write()
fout.Close()

fpout.close()
gPad.Update()

