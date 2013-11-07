import ROOT
for path in [os.path.abspath(p) for p in ['../../HEPHYCommonTools/python/']]:
  if not path in sys.path:
      sys.path.insert(1, path)

from xsecSMS import *

for x in ["gluino8TeV_NLONLL", "stop8TeV_NLONLL", "gluino8TeV_NLONLL_Up", "gluino8TeV_NLONLL_Down", "gluino14TeV_NLO"]:
  fname = "mOutput/"+x.replace("_","")+".m"
  xsec = eval(x)
  f = file(fname, 'w')
  for m in xsec: 
    line = x.replace("_","")+"["+str(m)+"]="+str(xsec[m])+";\n"
    f.write(line)
  f.close()

#xsec = ROOT.TH1F("xsec", "xsec", (2000-200)/5, 200, 2000)
#for mgl in gluino_NLONLL:
#  xsec.SetBinContent(xsec.FindBin(mgl), gluino_NLONLL[mgl])

#c1 = ROOT.TCanvas()
#c1.SetLogy()
#xsec.Draw()
#
#pareto = ROOT.TF1("pareto",  "[0]*(1 + ((-200 + x)*[2])/[1])**(-1 - 1./[2])/[1]", 200, 2000)
#pareto.SetParameter(0, 10**5)       #mu
#pareto.SetParameter(1, 30)        #sigma
#pareto.SetParameter(2, 0.1)       #xi
#xsec.Fit(pareto)
#pareto.Draw("same")
 
