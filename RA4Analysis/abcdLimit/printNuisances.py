#!/usr/bin/env python
import re
from sys import argv, stdout, stderr, exit
from optparse import OptionParser
from HiggsAnalysis.CombinedLimit.DatacardParser import *

# import ROOT with a fix to get batch mode (http://root.cern.ch/phpBB3/viewtopic.php?t=3198)
hasHelp = False
#for X in ("-h", "-?", "--help"):
#    if X in argv:
#        hasHelp = True
#        argv.remove(X)
#argv.append( '-b-' )
import ROOT
#ROOT.gROOT.SetBatch(True)
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
#argv.remove( '-b-' )
if hasHelp: argv.append("-h")

parser = OptionParser(usage="usage: %prog [options] in.root  \nrun with --help to get list of options")
parser.add_option("-A", "--absolute", dest="abs",    default=False,  action="store_true", help="Report also absolute values of nuisance values and errors, not only the ones normalized to the input sigma")

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
for n in sorted(rateParms.keys()):
    v,vmin,vmax = rateParms[n]
    print "Prefit  {0:20s}   {1:8.3f}  {2:8.3f}  {3:8.3f}".format(n,v,vmin,vmax)


file = ROOT.TFile(args[1])
if file == None: raise RuntimeError, "Cannot open file %s" % args[0]
fit_b  = file.Get("fit_b")
fpf_b = fit_b.floatParsFinal()
prefit = file.Get("nuisances_prefit")
if fit_b == None or fit_b.ClassName()   != "RooFitResult": raise RuntimeError, "File %s does not contain the output of the background fit 'fit_b'" % args[0]
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
#    nuis_b = fpf_b.find(name)
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
        mean_p, sigma_p = (nuis_p.getVal(), nuis_p.getError())
        print "Prefit  {0:20s}   {1:8.3f} +- {2:8.3f}".format(name,nuis_p.getVal(), nuis_p.getError())
        results[cat][name]["mean_p"] = mean_p
        results[cat][name]["sigma_p"] = sigma_p
    for fit_name, nuis_x in [('b', nuis_b)]:
        if nuis_x == None:
            pass
        else:
            results[cat][name]["nuis_val"] = nuis_x.getVal()
            results[cat][name]["nuis_err"] = nuis_x.getError()
            print "Postfit {0:20s}   {1:8.3f}  {2:8.3f}".format(name,nuis_x.getVal(),nuis_x.getError())

