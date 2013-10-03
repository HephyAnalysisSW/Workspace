import ROOT
import pickle

ROOT.TH1F().SetDefaultSumw2()

data = ROOT.TChain("Events")
data.Add( "/data/mhickel/pat_121207/MuHad-Run2012A-13Jul2012/h*.root")
data.Add( "/data/mhickel/pat_121207/MuHad-Run2012B-13Jul2012/h*.root")
data.Add( "/data/mhickel/pat_121207/MuHad-Run2012C-Aug24ReReco/h*.root")
data.Add( "/data/mhickel/pat_121207/MuHad-Run2012C-PromptReco-v2/h*.root")
data.Add( "/data/mhickel/pat_121207/MuHad-Run2012D-PromptReco/h*.root")
data.Add( "/data/mhickel/pat_121207/ElectronHad-Run2012A-13Jul2012/h*.root")
data.Add( "/data/mhickel/pat_121207/ElectronHad-Run2012B-13Jul2012/h*.root")
data.Add( "/data/mhickel/pat_121207/ElectronHad-Run2012C-Aug24ReReco/h*.root")
data.Add( "/data/mhickel/pat_121207/ElectronHad-Run2012C-PromptReco-v2/h*.root")
data.Add( "/data/mhickel/pat_121207/ElectronHad-Run2012D-PromptReco/h*.root")

c = ROOT.TChain("Events")
c.Add("/data/mhickel/pat_121211/8TeV-TTJets-powheg-v1+2/histo_*.root")
preselCut = "ht>400&&type1phiMet>150&&nbtags>=2&&njets>=4"
#c.Draw("jetsBtag>>hDiscC(20,0,1)", preselCut+"&&abs(jetsParton)==4&&jetsPt>40&&abs(jetsEta)<2.4&&jetsID&&jetsMuCleaned&&jetsEleCleaned")
#c.Draw("jetsBtag>>hDiscB(20,0,1)", preselCut+"&&abs(jetsParton)==5&&jetsPt>40&&abs(jetsEta)<2.4&&jetsID&&jetsMuCleaned&&jetsEleCleaned")
#c.Draw("jetsBtag>>hDisc0(20,0,1)", preselCut+"&&(abs(jetsParton)>5||abs(jetsParton)<4)&&jetsPt>40&&abs(jetsEta)<2.4&&jetsID&&jetsMuCleaned&&jetsEleCleaned")
#
#hDiscC = ROOT.gDirectory.Get("hDiscC")
#hDiscC.Scale(1./hDiscC.Integral())
#hDiscB = ROOT.gDirectory.Get("hDiscB")
#hDiscB.Scale(1./hDiscB.Integral())
#hDisc0 = ROOT.gDirectory.Get("hDisc0")
#hDisc0.Scale(1./hDisc0.Integral())
#
c1 = ROOT.TCanvas()
#hDisc0.SetLineColor(ROOT.kBlack)
#hDisc0.Draw()
#hDiscC.SetLineColor(ROOT.kGreen)
#hDiscC.Draw("same")
#hDiscB.SetLineColor(ROOT.kRed)
#hDiscB.Draw("same")
#c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngBTag/disc.png")
#c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngBTag/disc.pdf")
##del hDiscC, hDiscB, hDisc0
leptonCut = "((singleMuonic&&nvetoMuons==1&&nvetoElectrons==0)||(singleElectronic&&nvetoMuons==0&&nvetoElectrons==1))"

c.Draw("jetsBtag>>hDiscCMC(20,0,1)", leptonCut+"&&"+preselCut+"&&abs(jetsParton)==4&&jetsPt>40&&abs(jetsEta)<2.4&&jetsID&&jetsMuCleaned&&jetsEleCleaned")
c.Draw("jetsBtag>>hDiscBMC(20,0,1)", leptonCut+"&&"+preselCut+"&&abs(jetsParton)==5&&jetsPt>40&&abs(jetsEta)<2.4&&jetsID&&jetsMuCleaned&&jetsEleCleaned")
c.Draw("jetsBtag>>hDisc0MC(20,0,1)", leptonCut+"&&"+preselCut+"&&(abs(jetsParton)>5||abs(jetsParton)<4)&&jetsPt>40&&abs(jetsEta)<2.4&&jetsID&&jetsMuCleaned&&jetsEleCleaned")
print "MC","c", ROOT.hDiscCMC.Integral(),"b", ROOT.hDiscBMC.Integral(),"0", ROOT.hDisc0MC.Integral() 
#
#pickle.dump([hDisc0, hDiscC, hDiscB], file("hDisc.pkl","w"))
hDisc0, hDiscC, hDiscB = pickle.load( file("hDisc.pkl"))

##c.Draw("jetsBtag>>hMCTarget(20,0,1)", leptonCut+"&&"+preselCut+"&&jetsPt>40&&abs(jetsEta)<2.4&&jetsID&&jetsMuCleaned&&jetsEleCleaned")
##hMCTarget = ROOT.gDirectory.Get("hMCTarget")
#c.Draw("jetsBtag>>hMCDiscC(20,0,1)", leptonCut+"&&"+preselCut+"&&abs(jetsParton)==4&&jetsPt>40&&abs(jetsEta)<2.4&&jetsID&&jetsMuCleaned&&jetsEleCleaned")
#c.Draw("jetsBtag>>hMCDiscB(20,0,1)", leptonCut+"&&"+preselCut+"&&abs(jetsParton)==5&&jetsPt>40&&abs(jetsEta)<2.4&&jetsID&&jetsMuCleaned&&jetsEleCleaned")
#c.Draw("jetsBtag>>hMCDisc0(20,0,1)", leptonCut+"&&"+preselCut+"&&(abs(jetsParton)>5||abs(jetsParton)<4)&&jetsPt>40&&abs(jetsEta)<2.4&&jetsID&&jetsMuCleaned&&jetsEleCleaned")
#
#hMCDiscC = ROOT.gDirectory.Get("hMCDiscC")
#hMCDiscB = ROOT.gDirectory.Get("hMCDiscB")
#hMCDisc0 = ROOT.gDirectory.Get("hMCDisc0")
#

#data.Draw("jetsBtag>>hDataTarget(20,0,1)", leptonCut+"&&"+preselCut+"&&jetsPt>40&&abs(jetsEta)<2.4&&jetsID&&jetsMuCleaned&&jetsEleCleaned")
#hDataTarget = ROOT.gDirectory.Get("hDataTarget")
#target = hDataTarget
#
#mc = ROOT.TObjArray(3)
#mc.Add(hDisc0)
#mc.Add(hDiscC)
#mc.Add(hDiscB)
#fit = ROOT.TFractionFitter(target, mc)
#fit.Constrain(0,0.0,1.0)
#fit.Constrain(1,0.0,1.0)
#fit.Constrain(2,0.0,1.0)
##fit.SetRangeX(1,15);                    // use only the first 15 bins in the fit
#status = fit.Fit()
#print status
#if status == 0:
# result = fit.GetPlot()
# target.Draw("Ep")
# result.Draw("same")
# tyield = result.Integral()
# v = ROOT.Double()
# ve = ROOT.Double()
# fit.GetResult(0,v,ve)
# hDisc0.Scale(tyield*v)
# fit.GetResult(1,v,ve)
# hDiscC.Scale(tyield*v)
# fit.GetResult(2,v,ve)
# hDiscB.Scale(tyield*v)
# hDisc0.Draw("same")
# hDiscC.Draw("same")
# hDiscB.Draw("same")
# c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngBTag/fitres.png")
# c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngBTag/fitres.pdf")
