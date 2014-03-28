import ROOT
from Workspace.RA4Analysis.simplePlotsCommon import *

#c = ROOT.TChain("Events")
#c.Add("/data/schoef/convertedTuples_v11/copyMET/Mu/TTJets-PowHeg/histo_TTJets-PowHeg.root")
#d = ROOT.TChain("Events")
#d.Add("/data/schoef/convertedTuples_v11/copyMET/Mu/T1tttt/histo_T1tttt_1000_100.root")
#
#c1 = ROOT.TCanvas()
#c.Draw("njets>>hTTJets(14,0,14)", "weight*(singleMuonic&&ht>750&&met>250&&nbtags>=3&&njets>=4)")
#d.Draw("njets>>hT1tttt(14,0,14)", "weight*(singleMuonic&&ht>750&&met>250&&nbtags>=3&&njets>=4)", "same")
#hT1tttt = ROOT.gDirectory.Get("hT1tttt")
#hTTJets = ROOT.gDirectory.Get("hTTJets")
#hTTJets.GetXaxis().SetTitle("number of jets")
#hT1tttt.SetLineColor(ROOT.kRed)
#hT1tttt.Draw("same")
#c1.Print(defaultWWWPath+"/pngMetShapeBias/njets_TT_sig.png")
#del hT1tttt
#del hTTJets

#c.Draw("genmet>>hInc(50,0,1000)", "weight*(singleMuonic&&genmet>100)")
#c.Draw("genmet>>hJ1(50,0,1000)",  "weight*(ht>750&&singleMuonic&&genmet>100&&njets>=1)","same")
#c.Draw("genmet>>hJ2(50,0,1000)",  "weight*(ht>750&&singleMuonic&&genmet>100&&njets>=2)","same")
#c.Draw("genmet>>hJ3(50,0,1000)",  "weight*(ht>750&&singleMuonic&&genmet>100&&njets>=3)","same")
#c.Draw("genmet>>hJ4(50,0,1000)",  "weight*(ht>750&&singleMuonic&&genmet>100&&njets>=4)","same")
#c.Draw("genmet>>hJ5(50,0,1000)",  "weight*(ht>750&&singleMuonic&&genmet>100&&njets>=5)","same")
#c.Draw("genmet>>hJ6(50,0,1000)",  "weight*(ht>750&&singleMuonic&&genmet>100&&njets>=6)","same")
#
#hInc=ROOT.gDirectory.Get("hInc") 
#histos={}
#for j in range(1,7):
#  h = ROOT.gDirectory.Get("hJ"+str(j))
#  stuff.append(h)
#  h.Divide(hInc)
#  h.SetLineColor(ROOT_colors[j])
#  if j==1:
#    h.Draw()
#  else:
#    h.Draw("same")
#  histos[j] = h
#c1.Print(defaultWWWPath+"/pngMetShapeBias/met_njetRatio_TT_HT750.png")
#del hInc

#c1 = ROOT.TCanvas()
#c = ROOT.TChain("Events")
#c.Add("/data/schoef/pat_120925/mc8TeV/8TeV-TTJets-powheg-v1+2/h*.root")
#c.Draw("genmet>>hmet(100,0,1000)", "singleMuonic")
#hmet = ROOT.gDirectory.Get("hmet")
#
##  "(x<x0)*(-((exp(1. + (x0*(1. + xi))/(s - mu*xi + x0*xi) + x*(-(1./x0) - (1. + xi)/(s - mu*xi + x0*xi)))*x*(s + x0 - mu*xi + 2*x0*xi))/(x0**2*(s - mu*xi + x0*xi)**2*(1 + ((-mu + x0)*xi)/s)**(1/xi)*(-(1/x0) - (1 + xi)/(s - mu*xi + x0*xi)))) +(x>=x0)* (1 + ((-mu + x)*xi)/s)**(-1 - 1/xi)/s"
#func = ROOT.TF1("func",  "[4]*((x<[0])*(-(exp(1. + ([0]*(1. + [3]))/([2] - [1]*[3] + [0]*[3]) + x*(-(1./[0]) - (1. + [3])/([2] - [1]*[3] + [0]*[3])))*x*([2] + [0] - [1]*[3] + 2*[0]*[3]))/([0]**2*([2] - [1]*[3] + [0]*[3])**2*(1 + ((-[1] + [0])*[3])/[2])**(1/[3])*(-(1/[0]) - (1 + [3])/([2] - [1]*[3] + [0]*[3])))) +(x>=[0])* (1 + ((-[1] + x)*[3])/[2])**(-1 - 1./[3])/[2])", 0, 1000)
#
#func.SetParameter(0, 150)       #x0
#func.SetParLimits(0,150,150)
#
#func.SetParameter(1, 100)       #mu
#func.SetParameter(2, 25)        #sigma
#func.SetParameter(3, 0.2)       #xi
#func.SetParameter(4, .5*10**7)  #norm
#
#hmet.Fit(func, "", "", 150, 1000)
#hmet.Draw()
#func.Draw("same")
#c1.Print("/afs/hephy.at/user/s/schoefbeck/www/etc/ttbar_globalFit.png")

#c1 = ROOT.TCanvas()
#c1.SetLogy()
#c = ROOT.TChain("Events")
#c.Add("/data/mhickel/pat_120917/mc8TeV/8TeV-WJetsToLNu/h*.root")
#c.Draw("genmet>>hmet(100,0,1000)", "singleMuonic&&njets>=4&&ht>400")
#hmet = ROOT.gDirectory.Get("hmet")
##func = ROOT.TF1("func2",  "[4]*((x<[0])*(x/(exp(((x - [0])*([2] + [0] - [1]*[3] + 2*[0]*[3]))/([0]*([2] - [1]*[3] + [0]*[3])))*[2]*[0]*(([2] - [1]*[3] + [0]*[3])/[2])**((1 + [3])/[3]))) +(x>=[0])* (1 + ((-[1] + x)*[3])/[2])**(-1 - 1./[3])/[2])", 0, 1000)
#func = ROOT.TF1("func2",  "[4]*((x<[0])*((exp(sqrt(x)*[5] - sqrt([0])*[5])*x)/([2]*[0]*(([2] + [0]*[3] - [3]*[1])/[2])**((1 + [3])/[3]))) +(x>=[0])* (1 + ((-[1] + x)*[3])/[2])**(-1 - 1./[3])/[2])", 0, 1000)
#
#func.SetParameter(0, 150)       #x0
#func.SetParLimits(0,150,150)
#
#func.SetParameter(1, 0.)       #mu
#
#func.SetParameter(2, 25)        #sigma
#func.SetParameter(3, 0.2)       #xi
#func.SetParameter(4, 10**5)  #norm
#func.SetParameter(5, .00000001)  #alpha
#func.Draw()
#hmet.Draw("same")
#
##hmet.Draw()
##hmet.Fit(func, "", "", 0, 1000)
##func.Draw("same")
##c1.Print("/afs/hephy.at/user/s/schoefbeck/www/etc/wjets_globalFit.png")

c1 = ROOT.TCanvas()
pareto = ROOT.TF1("pareto",  "(1 + ((-[1] + x)*[3])/[2])**(-1 - 1./[3])/[2]", 0, 1000)

pareto.SetParameter(0, 150)       #x0
pareto.SetParLimits(0,150,150)

pareto.SetParameter(1, 0.)       #mu

pareto.SetParameter(2, 25)        #sigma
pareto.SetParameter(3, 0.2)       #xi
pareto.SetParameter(4, 10**5)  #norm
pareto.SetParameter(5, .00000001)  #alpha
hp = ROOT.TH1F("hp", "hp",100,0,1000)
for i in range(hp.GetNbinsX()+1):
  hp.SetBinContent(i, pareto.Eval(hp.GetBinCenter(i)))

hp.Draw()
pareto.Draw("same")

func = ROOT.TF1("func2",  "[3]*exp(-[1]*x**[2])", 0, 1000)

func.SetParameter(0, 1.5)       #alpha
func.SetParameter(1, 0.5)       #beta
func.SetParameter(2, 1)       #n

func.Draw("same")
