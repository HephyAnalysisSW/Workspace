import ROOT
from Workspace.RA4Analysis.simplePlotsCommon import *

def getLepVar(var):
  cvar =  "((top1WDaughter0Pdg>=10)*("+var.replace("topL", "top1").replace("topH", "top0")+")+(top0WDaughter0Pdg>=10)*("+var.replace("topL", "top0").replace("topH","top1")+"))"
#  print cvar
  return cvar

singleLepCut = "( ((abs(top1WDaughter0Pdg)>=10)||(abs(top0WDaughter0Pdg)>=10))&&(!((abs(top1WDaughter0Pdg)>=10)&&(abs(top0WDaughter0Pdg)>=10))))"
c = ROOT.TChain("Events")
c.Add("/data/schoef/pat_120925/mc8TeV/8TeV-TTJets/*.root")
#c.Add("/data/schoef/pat_120925/mc8TeV/8TeV-TTJets/histo_10*.root")

commoncf="met<200"
allStacks =\
  [
#    [getLepVar("(topLbPx*topLPx + topLbPy*topLPy)/(sqrt(topLbPx**2 + topLbPy**2)*sqrt(topLPx**2 + topLPy**2))"), "htLbLt", "(20,-1,1)", singleLepCut+"&&jet2pt>40&&met>100&&met<150", ROOT.kBlack, 1, "100<MET<150 bL/tL"],
#    [getLepVar("(topHbPx*topLPx + topHbPy*topLPy)/(sqrt(topHbPx**2 + topHbPy**2)*sqrt(topLPx**2 + topLPy**2))"), "htHbLt", "(20,-1,1)", singleLepCut+"&&jet2pt>40&&met>100&&met<150", ROOT.kRed, 1, "100<MET<150 bH/tL"],
#    [getLepVar("(topLbPx*topLPx + topLbPy*topLPy)/(sqrt(topLbPx**2 + topLbPy**2)*sqrt(topLPx**2 + topLPy**2))"), "htLbLt", "(20,-1,1)", singleLepCut+"&&jet2pt>40&&met>200", ROOT.kBlack, 2, "MET>200 bL/tL"],
#    [getLepVar("(topHbPx*topLPx + topHbPy*topLPy)/(sqrt(topHbPx**2 + topHbPy**2)*sqrt(topLPx**2 + topLPy**2))"), "htHbLt", "(20,-1,1)", singleLepCut+"&&jet2pt>40&&met>200", ROOT.kRed, 2, "MET>200 bH/tL"],

   [[[getLepVar("sqrt(topLbPx**2 + topLbPy**2)"), "htLbLt", "(20,0,200)", singleLepCut+"&&jet2pt>40&&met>100&&met<150", ROOT.kBlack, 1, "100<MET<150 bL"],
     [getLepVar("sqrt(topHbPx**2 + topHbPy**2)"), "htHbLt", "(20,0,200)", singleLepCut+"&&jet2pt>40&&met>100&&met<150", ROOT.kRed, 1,   "100<MET<150 bH"]],"pT_b_100_150.png"],
#   [[[getLepVar("sqrt(topLbPx**2 + topLbPy**2)"), "htLbLt", "(20,0,200)", singleLepCut+"&&jet2pt>40&&met>150&&met<200", ROOT.kBlack, 1, "150<MET<200 bL"],
#     [getLepVar("sqrt(topHbPx**2 + topHbPy**2)"), "htHbLt", "(20,0,200)", singleLepCut+"&&jet2pt>40&&met>150&&met<200", ROOT.kRed, 1,   "150<MET<200 bH"]],"pT_b_150_200.png"],
#   [[[getLepVar("sqrt(topLbPx**2 + topLbPy**2)"), "htLbLt", "(20,0,200)", singleLepCut+"&&jet2pt>40&&met>200&&met<250", ROOT.kBlack, 1, "200<MET<250 bL"],
#     [getLepVar("sqrt(topHbPx**2 + topHbPy**2)"), "htHbLt", "(20,0,200)", singleLepCut+"&&jet2pt>40&&met>200&&met<250", ROOT.kRed, 1,   "200<MET<250 bH"]],"pT_b_200_250.png"],
#   [[[getLepVar("sqrt(topLbPx**2 + topLbPy**2)"), "htLbLt", "(20,0,200)", singleLepCut+"&&jet2pt>40&&met>250&&met<300", ROOT.kBlack, 1, "250<MET<300 bL"],
#     [getLepVar("sqrt(topHbPx**2 + topHbPy**2)"), "htHbLt", "(20,0,200)", singleLepCut+"&&jet2pt>40&&met>250&&met<300", ROOT.kRed, 1,   "250<MET<300 bH"]],"pT_b_250_300.png"],
#   [[[getLepVar("sqrt(topLbPx**2 + topLbPy**2)"), "htLbLt", "(20,0,200)", singleLepCut+"&&jet2pt>40&&met>300&&met<350", ROOT.kBlack, 1, "300<MET<350 bL"],
#     [getLepVar("sqrt(topHbPx**2 + topHbPy**2)"), "htHbLt", "(20,0,200)", singleLepCut+"&&jet2pt>40&&met>300&&met<350", ROOT.kRed, 1,   "300<MET<350 bH"]],"pT_b_300_350.png"],
#   [[[getLepVar("sqrt(topLbPx**2 + topLbPy**2)"), "htLbLt", "(20,0,200)", singleLepCut+"&&jet2pt>40&&met>350&&met<400", ROOT.kBlack, 1, "350<MET<400 bL"],
#     [getLepVar("sqrt(topHbPx**2 + topHbPy**2)"), "htHbLt", "(20,0,200)", singleLepCut+"&&jet2pt>40&&met>350&&met<400", ROOT.kRed, 1,   "350<MET<400 bH"]],"pT_b_350_400.png"],
#   [[[getLepVar("sqrt(topLWDaughter0Px**2+topLWDaughter0Py**2)*(topLWDaughter0Pdg%2==1) + sqrt(topLWDaughter1Px**2+topLWDaughter1Py**2)*(topLWDaughter0Pdg%2==0)"), "htLbLt", "(20,0,400)", singleLepCut+"&&jet2pt>40&&met>100&&met<150", ROOT.kBlack, 1, "100<MET<150 lepton Pt"],
#     [getLepVar("sqrt(topLWDaughter0Px**2+topLWDaughter0Py**2)*(topLWDaughter0Pdg%2==0) + sqrt(topLWDaughter1Px**2+topLWDaughter1Py**2)*(topLWDaughter0Pdg%2==1)"), "htHbLt", "(20,0,400)", singleLepCut+"&&jet2pt>40&&met>100&&met<150", ROOT.kRed, 1,   "100<MET<150 neutrino Pt"]],"pT_topLWDaughter0Pt_100_150.png"],
#   [[[getLepVar("sqrt(topLWDaughter0Px**2+topLWDaughter0Py**2)*(topLWDaughter0Pdg%2==1) + sqrt(topLWDaughter1Px**2+topLWDaughter1Py**2)*(topLWDaughter0Pdg%2==0)"), "htLbLt", "(20,0,400)", singleLepCut+"&&jet2pt>40&&met>150&&met<200", ROOT.kBlack, 1, "150<MET<200 lepton Pt"],
#     [getLepVar("sqrt(topLWDaughter0Px**2+topLWDaughter0Py**2)*(topLWDaughter0Pdg%2==0) + sqrt(topLWDaughter1Px**2+topLWDaughter1Py**2)*(topLWDaughter0Pdg%2==1)"), "htHbLt", "(20,0,400)", singleLepCut+"&&jet2pt>40&&met>150&&met<200", ROOT.kRed, 1,   "150<MET<200 neutrino Pt"]],"pT_topLWDaughter0Pt_150_200.png"],
#   [[[getLepVar("sqrt(topLWDaughter0Px**2+topLWDaughter0Py**2)*(topLWDaughter0Pdg%2==1) + sqrt(topLWDaughter1Px**2+topLWDaughter1Py**2)*(topLWDaughter0Pdg%2==0)"), "htLbLt", "(20,0,400)", singleLepCut+"&&jet2pt>40&&met>200&&met<250", ROOT.kBlack, 1, "200<MET<250 lepton Pt"],
#     [getLepVar("sqrt(topLWDaughter0Px**2+topLWDaughter0Py**2)*(topLWDaughter0Pdg%2==0) + sqrt(topLWDaughter1Px**2+topLWDaughter1Py**2)*(topLWDaughter0Pdg%2==1)"), "htHbLt", "(20,0,400)", singleLepCut+"&&jet2pt>40&&met>200&&met<250", ROOT.kRed, 1,   "200<MET<250 neutrino Pt"]],"pT_topLWDaughter0Pt_200_250.png"],
#   [[[getLepVar("sqrt(topLWDaughter0Px**2+topLWDaughter0Py**2)*(topLWDaughter0Pdg%2==1) + sqrt(topLWDaughter1Px**2+topLWDaughter1Py**2)*(topLWDaughter0Pdg%2==0)"), "htLbLt", "(20,0,400)", singleLepCut+"&&jet2pt>40&&met>250&&met<300", ROOT.kBlack, 1, "250<MET<300 lepton Pt"],
#     [getLepVar("sqrt(topLWDaughter0Px**2+topLWDaughter0Py**2)*(topLWDaughter0Pdg%2==0) + sqrt(topLWDaughter1Px**2+topLWDaughter1Py**2)*(topLWDaughter0Pdg%2==1)"), "htHbLt", "(20,0,400)", singleLepCut+"&&jet2pt>40&&met>250&&met<300", ROOT.kRed, 1,   "250<MET<300 neutrino Pt"]],"pT_topLWDaughter0Pt_250_300.png"],
#   [[[getLepVar("sqrt(topLWDaughter0Px**2+topLWDaughter0Py**2)*(topLWDaughter0Pdg%2==1) + sqrt(topLWDaughter1Px**2+topLWDaughter1Py**2)*(topLWDaughter0Pdg%2==0)"), "htLbLt", "(20,0,400)", singleLepCut+"&&jet2pt>40&&met>300&&met<350", ROOT.kBlack, 1, "300<MET<350 lepton Pt"],
#     [getLepVar("sqrt(topLWDaughter0Px**2+topLWDaughter0Py**2)*(topLWDaughter0Pdg%2==0) + sqrt(topLWDaughter1Px**2+topLWDaughter1Py**2)*(topLWDaughter0Pdg%2==1)"), "htHbLt", "(20,0,400)", singleLepCut+"&&jet2pt>40&&met>300&&met<350", ROOT.kRed, 1,   "300<MET<350 neutrino Pt"]],"pT_topLWDaughter0Pt_300_350.png"],
#   [[[getLepVar("sqrt(topLWDaughter0Px**2+topLWDaughter0Py**2)*(topLWDaughter0Pdg%2==1) + sqrt(topLWDaughter1Px**2+topLWDaughter1Py**2)*(topLWDaughter0Pdg%2==0)"), "htLbLt", "(20,0,400)", singleLepCut+"&&jet2pt>40&&met>350&&met<400", ROOT.kBlack, 1, "350<MET<400 lepton Pt"],
#     [getLepVar("sqrt(topLWDaughter0Px**2+topLWDaughter0Py**2)*(topLWDaughter0Pdg%2==0) + sqrt(topLWDaughter1Px**2+topLWDaughter1Py**2)*(topLWDaughter0Pdg%2==1)"), "htHbLt", "(20,0,400)", singleLepCut+"&&jet2pt>40&&met>350&&met<400", ROOT.kRed, 1,   "350<MET<400 neutrino Pt"]],"pT_topLWDaughter0Pt_350_400.png"],
  ]
stuff = []

for stack in allStacks:
  c1 = ROOT.TCanvas()
  #c.Draw(getLepVar("sqrt(top1Px**2 + top1Py**2)"), singleLepCut)
  l = ROOT.TLegend(0.6, 0.75, 0.99, 0.99)
  l.SetFillColor(0)
  l.SetShadowColor(ROOT.kWhite)
  l.SetBorderSize(1)
  for i, plot in enumerate(stack[0]):
    print plot[0]+">>"+plot[1]+plot[2], plot[3]
    c.Draw(plot[0]+">>"+plot[1]+plot[2], plot[3], "goff")
    p = ROOT.gDirectory.Get(plot[1]).Clone()
    p.SetLineColor(plot[4])
    p.SetLineStyle(plot[5])
    p.SetMarkerStyle(0)
    p.SetMarkerColor(plot[4])

    p.Scale(1./p.Integral())
    l.AddEntry(p, plot[6])
    print p.Integral()
    if i==0:
      p.GetYaxis().SetRangeUser(0,0.35) 
      p.Draw()
      print "h1"
    else:
      p.Draw("same")
      print "h2"
    stuff.append(p)
  l.Draw()
  #c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngMetShapeBias/deltaPhi_b_top.png")
  c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngMetShapeBias/"+stack[1])

  #del htLbLt, htHbLt

#c = ROOT.TChain("Events")
#c.Add("/data/schoef/convertedTuples_v6/copy/Mu/TTJets-Fall11/histo_TTJets-Fall11_pf-3j40.root")
#for nj in [4,5,6]:
#  for htbin in [[x, x+100] for x in range(400,1200,100) ]:
#    l = ROOT.TLegend(0.6, 0.75, 0.99, 0.99)
#    l.SetFillColor(0)
#    l.SetShadowColor(ROOT.kWhite)
#    l.SetBorderSize(1)
#    c1 = ROOT.TCanvas()
#    c1.SetLogy()
#    c.Draw("met>>hM4j(50,100,1100)", "nbtags==2&&met>100&&njets< "+str(nj)+"&&ht>"+str(htbin[0])+"&&ht<"+str(htbin[1])) 
#    c.Draw("met>>hM5j(50,100,1100)", "nbtags==2&&met>100&&njets>="+str(nj)+"&&ht>"+str(htbin[0])+"&&ht<"+str(htbin[1])) 
#    hM4j = ROOT.gDirectory.Get("hM4j")
#    hM4j.Scale(1./hM4j.Integral())
#    hM5j = ROOT.gDirectory.Get("hM5j")
#    hM5j.Scale(1./hM5j.Integral())
#    hM5j.SetLineColor(ROOT.kRed)
#    l.AddEntry(hM4j, "njet<"+str(nj))
#    l.AddEntry(hM5j, "njet>="+str(nj))
#    hM4j.Draw()
#    hM5j.Draw("same")
#    l.Draw()
#    c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngMetShapeBias/met_2b_ht_"+str(htbin[0])+"_"+str(htbin[1])+"_nj_geq"+str(nj)+"_comparison.png")
