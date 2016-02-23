import ROOT
import pickle, os

ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()

path = '/afs/hephy.at/user/d/dspitzbart/www/Spring15/25ns/templateFit_SFtemplates_fullSR_lep_data_2p25/'
name = 'st250-350_ht500-750_njet6-7_nBTagFitRes'

f = ROOT.TFile(path+name+'.root')

c = f.Get('c1')

c.Draw()

can1 = ROOT.TCanvas('can1','can1',650,500)
can2 = ROOT.TCanvas('can2','can2',650,650)

can1.cd()

p1 = c.GetPrimitive('c1_2')
#p2 = c.GetPrimitive('c1_2')

p1.SetPad(0,0,1,1)
#can1.cd()
p1.Draw()
#p1.cd()

frame1 = p1.GetPrimitive('frame_5a85cd0')
curve1 = p1.GetPrimitive('model_NegPdg_Norm[nBJetMediumCSV30]')
curve2 = p1.GetPrimitive('model_NegPdg_Norm[nBJetMediumCSV30]_Comp[model_WJets_NegPdg]')
curve3 = p1.GetPrimitive('model_NegPdg_Norm[nBJetMediumCSV30]_Comp[model_TTJets]')
curve4 = p1.GetPrimitive('model_NegPdg_Norm[nBJetMediumCSV30]_Comp[model_Rest_NegPdg]')
curve5 = p1.GetPrimitive('model_NegPdg_Norm[nBJetMediumCSV30]_Comp[model_QCD]')
h_d = p1.GetPrimitive('h_data')

can2.cd()

#frame1.Draw()
h_t = ROOT.TH1F('h_t','h_t',3,0,3)
h_t.SetMaximum(300)
h_t.GetXaxis().SetTitle('n_{b-jet}')
h_t.GetXaxis().SetTitleSize(0.065)
h_t.GetXaxis().SetBinLabel(1,'0')
h_t.GetXaxis().SetBinLabel(2,'1')
h_t.GetXaxis().SetBinLabel(3,'#geq2')
h_t.GetXaxis().SetLabelSize(0.08)

h_t.GetYaxis().SetTitle('Events')
h_t.GetYaxis().SetNdivisions(508)

h_t.Draw()
curve1.Draw('same')
curve2.Draw('same')
curve3.Draw('same')
curve4.Draw('same')
if curve5: curve5.Draw('same')
h_d.Draw('E1P same')

latex1 = ROOT.TLatex()
latex1.SetNDC()
latex1.SetTextSize(0.04)
latex1.SetTextAlign(11)

latex1.DrawLatex(0.16,0.96,'CMS #bf{#it{Preliminary}}')
latex1.DrawLatex(0.75,0.96,"2.2fb^{-1} (13TeV)")

if curve5: lowerBound = 0.70
else: lowerBound = 0.75
leg = ROOT.TLegend(0.72,lowerBound,0.98,0.95)
leg.SetFillColor(ROOT.kWhite)
leg.SetShadowColor(ROOT.kWhite)
leg.SetBorderSize(1)
leg.SetTextSize(0.035)
leg.AddEntry(h_d, 'data', 'lp')
leg.AddEntry(curve1, 'total', 'l')
leg.AddEntry(curve2, 'W+jets', 'l')
leg.AddEntry(curve3, 't#bar{t}+jets', 'l')
leg.AddEntry(curve4, 'rest EWK', 'l')
if curve5: leg.AddEntry(curve5, 'QCD', 'l')
leg.Draw()


printPath = '/afs/hephy.at/user/d/dspitzbart/www/Results2016/btagFitResults/'

if not os.path.exists(printPath):
  os.makedirs(printPath)

can2.Print(printPath+name+'.png')
can2.Print(printPath+name+'.pdf')
can2.Print(printPath+name+'.root')




