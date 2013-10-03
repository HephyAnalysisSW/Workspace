import ROOT
c = ROOT.TChain("pfRA4Analyzer/Events")
small = False
if small:
  c.Add("/scratch/schoef/pat_110924/Mu/WJetsToLNu/histo_1_*.root")
else:
  c.Add("/scratch/schoef/pat_110924/Mu/WJetsToLNu/histo_*.root")

commoncf = "singleMuonic&&lepton_pdg>0"
prefix = "Minus"

c.Draw("genmet>>hInc(100,0,1000)", commoncf)
htmp = ROOT.gDirectory.Get("hInc")
hInc = htmp.Clone()
del htmp

htvals = [0,100,200,300, 400, 500, 600, 700, 800, 900, 1000]
#htvals = [300, 400]
htbins = []
for nht in range(len(htvals)-1):
  htbins.append([htvals[nht], htvals[nht+1]])

lowerCutHistos = {}
upperCutHistos = {}
bothCutHistos = {}
for ht in htvals:
  print "At ht", ht
  c.Draw("genmet>>htmp(100,0,1000)", commoncf+"&&ht>"+str(ht))
  htmp =  ROOT.gDirectory.Get("htmp")
  lowerCutHistos[ht] = htmp.Clone()
  lowerCutHistos[ht].SetLineColor(ROOT.kBlack)
  lowerCutHistos[ht].SetName("lowerCut_"+str(ht))
  del htmp
  c.Draw("genmet>>htmp(100,0,1000)", commoncf+"&&ht<"+str(ht))
  htmp =  ROOT.gDirectory.Get("htmp")
  upperCutHistos[ht] = htmp.Clone()
  upperCutHistos[ht].SetLineColor(ROOT.kRed)
  upperCutHistos[ht].SetName("upperCut_"+str(ht))
  del htmp


bothCutHistos = {}

for htb in htbins:
  print "At htb", htb
  c.Draw("genmet>>htmp(100,0,1000)", commoncf+"&&ht>"+str(htb[0])+"&&ht<"+str(htb[1]))
  htmp =  ROOT.gDirectory.Get("htmp")
  bothCutHistos[htb[0]] = htmp.Clone()
  bothCutHistos[htb[0]].SetLineColor(ROOT.kBlue)
  bothCutHistos[htb[0]].SetName("bothCuts_"+str(ht))
  del htmp
  
for ht in htvals:
  lowerCutHistos[ht].Divide(hInc)
  upperCutHistos[ht].Divide(hInc)

productCutHistos={}
for htb in htbins:
  bothCutHistos[htb[0]].Divide(hInc)
  productCutHistos[htb[0]]=lowerCutHistos[htb[0]].Clone()
  productCutHistos[htb[0]].Multiply(upperCutHistos[htb[1]])
  productCutHistos[htb[0]].SetLineColor(ROOT.kGreen)

for htb in htbins:
  l = ROOT.TLegend(0.7, 0.8,1.0,1.0)
  l.AddEntry(upperCutHistos[htb[1]],   "upper Cut") 
  l.AddEntry(lowerCutHistos[htb[0]],   "lower Cut") 
  l.AddEntry(bothCutHistos[htb[0]],    "both Cuts") 
#  l.AddEntry(productCutHistos[htb[0]], "product"  )
  c1 = ROOT.TCanvas()
  ROOT.gPad.SetLogy()
  upperCutHistos[htb[1]].Draw()
  lowerCutHistos[htb[0]].Draw("same")
  bothCutHistos[htb[0]].Draw("same")
#  productCutHistos[htb[0]].Draw("same")
  l.Draw() 
  c1.SaveAs("/afs/hephy.at/user/s/schoefbeck/www/pngTMP/"+prefix+"_ratio-ht-"+str(htb[0])+"-"+str(htb[1])+".png")
ofile = ROOT.TFile("/afs/hephy.at/user/s/schoefbeck/www/pngTMP/"+prefix+"_ratios.root","recreate")
hInc.Write()
for ht in htvals:
  lowerCutHistos[ht].Write()
  upperCutHistos[ht].Write()
for htb in htbins:
  bothCutHistos[htb[0]].Write()
ofile.Close()

