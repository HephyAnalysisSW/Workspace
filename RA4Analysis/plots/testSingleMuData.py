import ROOT

#[["Run2012A", 192000, 8*10**7],["Run2012B", 195000, 8*10**7],["Run2012C-v1", 198550, 8*10**7],["Run2012C-v2", 203002, 3*10**7]]

for prefix, cut in [["ABCD","(1)"], ["ABC","run<=203002"], ["D","run>203002"]]:
#for prefix, cut in [["ABCD_ht_400_450","(ht>400&&ht<450)"], ["ABC_ht_400_450","run<=203002&&ht>400&&ht<450"], ["D_ht_400_450","run>203002&&ht>400&&ht<450"]]:
#for prefix, cut in [["ABCD_ht_400_750","(ht>400&&ht<750)"], ["ABC","run<=203002&&ht>400&&ht<750"], ["D","run>203002&&ht>400&&ht<750"]]:
  for mode in ["Ele", "Mu"]:
    cS = ROOT.TChain("Events")
    #cM = ROOT.TChain("Events")
    if mode=="Mu":
      cS.Add("/data/schoef/convertedTuples_v16/copyMET/Mu/singleMuData/h*.root")
      leptonCut = "(singleMuonic&&nvetoMuons==1&&nvetoElectrons==0)"
      baseTrigger = "HLTIsoMu24eta2p1"
      triggerCut = "(HLTPFHT350Mu15PFMET45||HLTPFHT350Mu15PFMET50||HLTPFHT400Mu5PFMET45||HLTPFHT400Mu5PFMET50||HLTPFNoPUHT350Mu15PFMET45||HLTPFNoPUHT350Mu15PFMET50||HLTPFNoPUHT400Mu5PFMET45||HLTPFNoPUHT400Mu5PFMET50)"
    #  cM.Add("/data/schoef/convertedTuples_v16/copyMET/Mu/data/*.root")
    if mode=="Ele":
      cS.Add("/data/schoef/convertedTuples_v16/copyMET/Ele/singleEleData/h*.root")
      leptonCut = "(singleElectronic&&nvetoMuons==0&&nvetoElectrons==1)"
      baseTrigger = "HLTEle27WP80"
      triggerCut = "(HLTCleanPFHT300Ele15CaloIdTCaloIsoVLTrkIdTTrkIsoVLPFMET45||HLTCleanPFHT300Ele15CaloIdTCaloIsoVLTrkIdTTrkIsoVLPFMET50||HLTCleanPFHT350Ele5CaloIdTCaloIsoVLTrkIdTTrkIsoVLPFMET45||HLTCleanPFHT350Ele5CaloIdTCaloIsoVLTrkIdTTrkIsoVLPFMET50||HLTCleanPFNoPUHT300Ele15CaloIdTCaloIsoVLTrkIdTTrkIsoVLPFMET45||HLTCleanPFNoPUHT300Ele15CaloIdTCaloIsoVLTrkIdTTrkIsoVLPFMET50||HLTCleanPFNoPUHT350Ele5CaloIdTCaloIsoVLTrkIdTTrkIsoVLPFMET45||HLTCleanPFNoPUHT350Ele5CaloIdTCaloIsoVLTrkIdTTrkIsoVLPFMET50)"
    c1 = ROOT.TCanvas()
    c1.SetLogy()
    commoncf = cut+"&&jet3pt>40&&leptonPt>25&&abs(leptonEta)<2.1&&"+leptonCut
    #commoncf = "ht>400&&jet3pt>40&&leptonPt>25&&abs(leptonEta)<2.1&&"+leptonCut
    cS.Draw("met>>hDenominator_met(101,0,1010)","ht>400&&"+commoncf+"&&"+baseTrigger) 
    cS.Draw("met>>hNominator_met(101,0,1010)","ht>400&&"+commoncf+"&&"+baseTrigger+"&&"+triggerCut,"same") 
    cS.Draw("ht>>hDenominator_ht(101,0,1010)","met>150&&"+commoncf+"&&"+baseTrigger) 
    cS.Draw("ht>>hNominator_ht(101,0,1010)","met>150&&"+commoncf+"&&"+baseTrigger+"&&"+triggerCut,"same") 
    #cS.Draw("met>>hDenominator(101,0,1010)",commoncf+"&&"+baseTrigger) 
    #cS.Draw("met>>hNominator(101,0,1010)",commoncf+"&&"+baseTrigger+"&&"+triggerCut,"same") 
    hDenominator_met = ROOT.gDirectory.Get("hDenominator_met")
    hNominator_met = ROOT.gDirectory.Get("hNominator_met")
    hDenominator_ht = ROOT.gDirectory.Get("hDenominator_ht")
    hNominator_ht = ROOT.gDirectory.Get("hNominator_ht")

    #hDenominator.Scale(hNominator.Integral()/hDenominator.Integral())
    hNominator_met.SetLineColor(ROOT.kRed)
    hDenominator_met.Draw()
    hNominator_met.Draw("same")
    c1.Print("/afs/hephy.at/user/s/schoefbeck/www/singleMu/"+prefix+"_"+mode+"_met_comparison.png")
    c1.Print("/afs/hephy.at/user/s/schoefbeck/www/singleMu/"+prefix+"_"+mode+"_met_comparison.root")

    hNominator_ht.SetLineColor(ROOT.kRed)
    hDenominator_ht.Draw()
    hNominator_ht.Draw("same")
    c1.Print("/afs/hephy.at/user/s/schoefbeck/www/singleMu/"+prefix+"_"+mode+"_ht_comparison.png")
    c1.Print("/afs/hephy.at/user/s/schoefbeck/www/singleMu/"+prefix+"_"+mode+"_ht_comparison.root")
