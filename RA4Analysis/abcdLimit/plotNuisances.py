#!/usr/bin/env python
import re
from sys import argv, stdout, stderr, exit
from optparse import OptionParser
from HiggsAnalysis.CombinedLimit.DatacardParser import *


import ROOT
#ROOT.gROOT.SetBatch(True)
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")

parser = OptionParser(usage="usage: %prog [options] in.root  \nrun with --help to get list of options")
(options, args) = parser.parse_args()
if len(args) == 0:
    parser.print_usage()
    exit(1)

dcparser = OptionParser()
addDatacardParserOptions(dcparser)
(dcoptions, dcargs) = dcparser.parse_args([])
dc = parseCard(file(args[0]),dcoptions)
rateParms = { }
for r in dc.rateParams:
    assert len(dc.rateParams[r])==1
    assert len(dc.rateParams[r][0])==2
    if len(dc.rateParams[r][0][0])==3:
        n = dc.rateParams[r][0][0][0]
        v = float(dc.rateParams[r][0][0][1])
        vmin,vmax = eval(dc.rateParams[r][0][1])
        assert not n in rateParms
        rateParms[n] = [ v, vmin, vmax ]

file = ROOT.TFile(args[1])
if file == None: raise RuntimeError, "Cannot open file %s" % args[0]
fit_b  = file.Get("fit_b")
fit_s  = file.Get("fit_s")
fpf_b = fit_b.floatParsFinal()
fpf_s = fit_s.floatParsFinal()
prefit = file.Get("nuisances_prefit")
if fit_b == None or fit_b.ClassName()   != "RooFitResult": raise RuntimeError, "File %s does not contain the output of the background fit 'fit_b'" % args[0]
if fit_s == None or fit_s.ClassName()   != "RooFitResult": raise RuntimeError, "File %s does not contain the output of the background fit 'fit_b'" % args[0]
if prefit == None or prefit.ClassName() != "RooArgSet":    raise RuntimeError, "File %s does not contain the prefit nuisances 'nuisances_prefit'"  % args[0]

results = {
#    "DiLep" : { },
    "QCD" : { },
    "corrTTDF" : { },
    "corrTTEF" : { },
    "corrWBF" : { },
    "corrWEF" : { },
    "j3" : { },
    "j4" : { },
    "j5" : { },
    "j6" : { },
    "j8" : { },
    "kJ" : { },
#    "jec" : { },
    "kappaTT" : { },
    "kappaW" : { },
    "kappab" : { },
#    "rcs" : { },
    "rcsWemu" : { },
    "statSeff" : { },
    "yWtt" : { },
#    "isr" : { },
    "stat" : { },
    "other" : { }
}


for i in range(fpf_b.getSize()):
    nuis_b = fpf_b.at(i)
    name   = nuis_b.GetName();
    nuis_s = fpf_s.find(name)
    nuis_p = prefit.find(name)

    cat = "other"
    for k in sorted(results.keys(),reverse=True):
        if k!="other" and name.startswith(k):
            cat = k
            break
    assert not name in results[cat]
    results[cat][name] = { }

    mean_p, sigma_p = 0,0
    if nuis_p == None:
        #print "Skipping ",cat,name
        #del results[cat][name]
        assert name in rateParms
#        if not options.abs: continue
#        print "No prefit for ",name
#        continue
    else:
        print name,nuis_p.getMin(),nuis_p.getMax()
        mean_p, sigma_p = (nuis_p.getVal(), nuis_p.getError())
        results[cat][name]["mean_p"] = mean_p
        results[cat][name]["sigma_p"] = sigma_p
    for fit_name, nuis_x in [('b', nuis_b)]:
        if nuis_x == None:
            pass
        else:
            results[cat][name]["nuis_b_val"] = nuis_x.getVal()
            results[cat][name]["nuis_b_err"] = nuis_x.getError()
    for fit_name, nuis_x in [('s', nuis_s)]:
        if nuis_x == None:
            pass
        else:
            results[cat][name]["nuis_s_val"] = nuis_x.getVal()
            results[cat][name]["nuis_s_err"] = nuis_x.getError()

ROOT.gStyle.SetOptTitle(0)
ROOT.gROOT.cd()
canvases = [ ]
legends = [ ]
gobjects = { }
for c in results:
    names = sorted(results[c].keys())
    nnames = len(names)
    if nnames==0:
        continue
    gobjects[c] = [ ]
    gobjects[c].append(ROOT.TH1F("h"+c,"h"+c,nnames,-0.5,nnames-0.5))
    gobjects[c][-1].SetStats(0)
    xaxis = gobjects[c][-1].GetXaxis()
    for i,n in enumerate(names):
        xaxis.SetBinLabel(i+1,n)
    for postfix in [ "pre", "postb", "posts" ]:
        g = ROOT.TGraphAsymmErrors()
        g.SetName("g"+cat+postfix)
        gobjects[c].append(g)
        g.SetLineWidth(2)
    gobjects[c][1].SetLineColor(ROOT.kGray)
    gobjects[c][1].SetFillColor(ROOT.kGray)
    gobjects[c][2].SetLineColor(ROOT.kBlue)
    gobjects[c][3].SetLineColor(ROOT.kRed)
    ymin = None
    ymax = None
    for i,n in enumerate(names):
        if not "mean_p" in results[c][n]:
            assert n in rateParms
            y = rateParms[n][0]
            eyl = y - rateParms[n][1]
            eyh = rateParms[n][2] - y
        else:
            y = results[c][n]["mean_p"]
            ey = results[c][n]["sigma_p"]
            eyl = ey
            eyh = ey
        if ymin==None or (y-eyl)<ymin:
            ymin = y - eyl
        if ymax==None or (y+eyh)>ymax:
            ymax = y + eyh
        gobjects[c][1].SetPoint(i,float(i),y)
        gobjects[c][1].SetPointError(i,0.40,0.40,eyl,eyh)

        y = results[c][n]["nuis_b_val"]
        ey = results[c][n]["nuis_b_err"]
        if ymin==None or (y-ey)<ymin:
            ymin = y - ey
        if ymax==None or (y+ey)>ymax:
            ymax = y + ey
        gobjects[c][2].SetPoint(i,float(i)-0.20,y)
        gobjects[c][2].SetPointError(i,0.20,0.20,ey,ey)

        y = results[c][n]["nuis_s_val"]
        ey = results[c][n]["nuis_s_err"]
        if ymin==None or (y-ey)<ymin:
            ymin = y - ey
        if ymax==None or (y+ey)>ymax:
            ymax = y + ey
        gobjects[c][3].SetPoint(i,float(i)+0.20,y)
        gobjects[c][3].SetPointError(i,0.20,0.20,ey,ey)

    canvases.append(ROOT.TCanvas("c"+c,"c"+c,800,600))
    if c.startswith("j"):
        gobjects[c][0].SetMinimum(ymax/5000.)
        gobjects[c][0].SetMaximum(5*ymax)
        canvases[-1].SetLogy(1)
    else:
        dy = ymax - ymin
        gobjects[c][0].SetMinimum(ymin-0.05*dy)
        gobjects[c][0].SetMaximum(ymax+0.05*dy)
    gobjects[c][0].Draw()
    gobjects[c][1].Draw("e2 z same")
    if c.startswith("j"):
        gobjects[c][1].Draw("p same")
    gobjects[c][2].Draw("e0 z same")
    gobjects[c][3].Draw("e0 z same")
    leg = ROOT.TLegend(0.68,0.78,0.88,0.88)
    legends.append(leg)
    leg.SetFillColor(ROOT.kWhite)
    leg.SetBorderSize(0)
    leg.AddEntry(gobjects[c][1],"Prefit","f")
    leg.AddEntry(gobjects[c][2],"Post bkg fit","l")
    leg.AddEntry(gobjects[c][3],"Post sig+bkg fit","l")
    leg.Draw()
    canvases[-1].Update()
    canvases[-1].SaveAs("nuisances-"+c+".pdf")

raw_input("Enter")

