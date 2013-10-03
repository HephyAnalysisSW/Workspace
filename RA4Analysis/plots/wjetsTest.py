import ROOT
mode = "Ele"
mode = "Mu"
guy="RS"
guy="WK"
postfix = "nj4"
if not globals().has_key("loadedNCP"):
  ROOT.gROOT.ProcessLine(".L ../scripts/useNiceColorPalette.C")
  ROOT.useNiceColorPalette(255)
  globals()["loadedNCP"] = True


cHT250 = ROOT.TChain("Events")
cHT250.Add("/data/schoef/convertedTuples_v16/copyMET/"+mode+"/WJetsHT250/h*.root")
cInc = ROOT.TChain("Events")
cInc.Add("/data/schoef/convertedTuples_v16/copyMET/"+mode+"/WJetsToLNu/h*.root")


if guy=="WK":
  scaleFac=1.
  htCutVal = 275
if guy=="RS":
  htCutVal = 325
  if mode=="Mu":
    scaleFac    = 0.8851333125242441 
  if mode=="Ele":
    scaleFac    = 0.87565035713284523 
if mode=="Mu":
  leptonCut = "singleMuonic&&nvetoMuons==1&&nvetoElectrons==0"
if mode=="Ele":
  leptonCut = "singleElectronic&&nvetoMuons==0&&nvetoElectrons==1"

for var in ["ht", "genmet"]:
 
  h_ht        = ROOT.TH1F("h_"+var+""       , "h_"+var+""       ,40, 0, 500)
  h_ht_HT250  = ROOT.TH1F("h_"+var+"_HT250" , "h_"+var+"_HT250" ,40, 0, 500)
  h_ht_Inc    = ROOT.TH1F("h_"+var+"_Inc"   , "h_"+var+"_Inc"   ,40, 0, 500)

  cHT250.Draw(var+">>h_"+var+"_HT250", "weight*(ht>"+str(htCutVal)                +"&&"+leptonCut+"&&njets>=4)") 
  cInc  .Draw(var+">>h_"+var+"_Inc", str(scaleFac)+"*"+"weight*(ht<"+str(htCutVal)+"&&"+leptonCut+"&&njets>=4)")
  h_ht = h_ht_HT250.Clone()
  h_ht.Add(h_ht_Inc)

  c1 = ROOT.TCanvas()
  c1.SetLogy()
  h_ht.SetLineColor(ROOT.kRed)
  h_ht.Draw()
  h_ht_HT250.Draw("same")
  h_ht_Inc.Draw("same")

  c1.Print("/afs/hephy.at/user/s/schoefbeck/www/etc/"+mode+"_"+guy+"_"+var+"_"+postfix+".png")

h_ht_vs_met_HT250  = ROOT.TH2F("h_ht_genmet_HT250", "h_ht_genmet_HT250" ,40, 0, 500, 40, 0, 500)
cHT250.Draw("genmet:ht>>h_ht_genmet_HT250", "weight*(ht>"+str(htCutVal)+"&&"+leptonCut+"&&njets>=4)") 
h_ht_vs_met_Inc  = ROOT.TH2F("h_ht_genmet_Inc", "h_ht_genmet_Inc" ,40, 0, 500, 40, 0, 500)
cInc.Draw("genmet:ht>>h_ht_genmet_Inc", "weight*(ht<"+str(htCutVal)+"&&"+leptonCut+"&&njets>=4)")

c1 = ROOT.TCanvas()
c1.SetLogz()
#h_ht_vs_met_HT250.Draw("COLZ")
#c1.Print("/afs/hephy.at/user/s/schoefbeck/www/etc/"+mode+"_"+guy+"_genmet_vs_ht_HT250_"+postfix+".png" )
#h_ht_vs_met_Inc.Draw("COLZ")
#c1.Print("/afs/hephy.at/user/s/schoefbeck/www/etc/"+mode+"_"+guy+"_genmet_vs_ht_Inc_"+postfix+".png" )
h_ht_vs_met_Inc.Add(h_ht_vs_met_HT250)
h_ht_vs_met_Inc.Draw("COLZ")
c1.Print("/afs/hephy.at/user/s/schoefbeck/www/etc/"+mode+"_"+guy+"_genmet_vs_ht_Sum_"+postfix+".png" )

del h_ht_vs_met_HT250, h_ht_vs_met_Inc
