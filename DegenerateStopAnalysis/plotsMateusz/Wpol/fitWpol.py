from ROOT import *
from math import *
import os, sys, time, glob
from hist import *

sample = "WJetsToLNu_HT"
ptbins = [50.,100.,300.,500.,10000.]
etabins = [0.,1.,2.,5.]
qbins = ["neg","pos"]

f = TFile("Wpol.root")

formula = [
"3./8.*[0]*(1.+x)^2 + 3./8.*[1]*(1.-x)^2 + 3./4.*[2]*(1-x^2)",
"3./8.*[0]*(1.-x)^2 + 3./8.*[1]*(1.+x)^2 + 3./4.*[2]*(1-x^2)"
]

indoffset = -1

fout = TFile("fitWpol.root","recreate")
HLplus = h2f("h_W_plus_fl",4,0.,4.,3,0.,3.)
HRplus = h2f("h_W_plus_fr",4,0.,4.,3,0.,3.)
H0plus = h2f("h_W_plus_f0",4,0.,4.,3,0.,3.)
HLminus = h2f("h_W_minus_fl",4,0.,4.,3,0.,3.)
HRminus = h2f("h_W_minus_fr",4,0.,4.,3,0.,3.)
H0minus = h2f("h_W_minus_f0",4,0.,4.,3,0.,3.)

canvases = []
for iq in xrange(len(qbins)):
    c = TCanvas("c"+str(iq),"",900,700)
    canvases.append(c)
    c.Divide(4,3)
    ipad = 1
    fx = TF1("fx",formula[iq],-1.,1.)
    for ieta in xrange(1,len(etabins)):
        for ipt in xrange(1,len(ptbins)):
            extratag = "pt{0:.0f}to{1:.0f}eta{2:.0f}to{3:.0f}W{4}".format(ptbins[ipt-1],ptbins[ipt],etabins[ieta-1],etabins[ieta],qbins[iq])
            hname = "H"+sample+extratag
            H = f.Get(hname)
            
            title = "{0:.0f} < pt < {1:.0f}  {2:.0f} < |eta| < {3:.0f}  W{4}".format(ptbins[ipt-1],ptbins[ipt],etabins[ieta-1],etabins[ieta],qbins[iq])
            H.SetTitle(title)
            c.cd(ipad)
#            H.Draw()
            fx.SetParameter(0,100.)
            fx.SetParameter(1,10.)
            fx.SetParameter(2,10.)
            fx.SetParLimits(0,0.,1.e10)
            fx.SetParLimits(1,0.,1.e10)
            fx.SetParLimits(2,0.,1.e10)
            H.Fit(fx,"LEB","",-1.,1.)
            ipad += 1
            gPad.Update()
            

            fl = fx.GetParameter(0)
            fr = fx.GetParameter(1)
            f0 = fx.GetParameter(2)
            fn = fl+fr+f0
            if iq == 0:
                HLminus.SetBinContent(ipt+indoffset,ieta+indoffset,fl/fn)
                HRminus.SetBinContent(ipt+indoffset,ieta+indoffset,fr/fn)
                H0minus.SetBinContent(ipt+indoffset,ieta+indoffset,f0/fn)
            else:
                HLplus.SetBinContent(ipt+indoffset,ieta+indoffset,fl/fn)
                HRplus.SetBinContent(ipt+indoffset,ieta+indoffset,fr/fn)
                H0plus.SetBinContent(ipt+indoffset,ieta+indoffset,f0/fn)
                
    c.SaveAs("W"+qbins[iq]+"Pol.png")
    c.SaveAs("W"+qbins[iq]+"Pol.root")


fout.Write()
fout.Close()
