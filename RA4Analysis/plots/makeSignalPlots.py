from analysisHelpers import *
signals = [[1000,600], [1250,0]]

minNJet = 6
metvar = "type1phiMet"
weight="weight"

signalPlotFile = ROOT.TFile("/afs/hephy.at/user/s/schoefbeck/www/etc/signalHistos.root","recreate")

for i,s in enumerate(signals):
  c = ROOT.TChain("Events")
  fstringMu  = "/data/schoef/convertedTuples_v19/copyMET/Mu/T1tttt-madgraph_"+str(s[0])+"_"+str(s[1])+"/histo_T1tttt-madgraph_"+str(s[0])+"_"+str(s[1])+".root"
  fstringEle = "/data/schoef/convertedTuples_v19/copyMET/Ele/T1tttt-madgraph_"+str(s[0])+"_"+str(s[1])+"/histo_T1tttt-madgraph_"+str(s[0])+"_"+str(s[1])+".root"
  if not (os.path.isfile(fstringMu) and os.path.isfile(fstringEle)):
    print "Error: files not found",fstringMu,fstringEle
    continue
  c.Add(fstringMu)
  c.Add(fstringEle)
  for htb in [(400,2500),(500,2500),(750,2500),(1000,2500)]:
    for btb in ['2', '3']:
      leptonCut = metvar+">=150&&njets>="+str(minNJet)+"&&ht>=400&&((singleMuonic&&nvetoMuons==1&&nvetoElectrons==0)||(singleElectronic&&nvetoMuons==0&&nvetoElectrons==1))"
      cut =  leptonCut+"&&ht>="+str(htb[0])+"&&ht<"+str(htb[1])
      cut+="&&"+btbCut[btb]

      gluinoSystemPt = "sqrt( (gluino0Pt*cos(gluino0Phi) + gluino1Pt*cos(gluino1Phi))**2 + (gluino0Pt*sin(gluino0Phi) + gluino1Pt*sin(gluino1Phi))**2)"
      ISRRefWeight  = "(1.*("+gluinoSystemPt+"<120) + "+".95*( "+gluinoSystemPt+">120&&"+gluinoSystemPt+"<150) + "+".90*( "+gluinoSystemPt+">150&&"+gluinoSystemPt+"<250) + "+".80*( "+gluinoSystemPt+">250))"

      leptonAndHadWeight = "(0.98*(0.95*singleMuonic + singleElectronic*(0.86*(abs(leptonEta)>1.552) + 0.98*(abs(leptonEta)<=1.552) )))"

      cut = weight+"*("+cut+")"

      c.Draw("type1phiMet>>hTMP(19,150,1000)",cut,"goff")
      hTMP = ROOT.gDirectory.Get("hTMP")
      res = hTMP.Clone("T1tttt-madgraph_"+str(s[0])+"_"+str(s[1])+"_bt"+btb+"_ht_"+str(htb[0])+"_"+str(htb[1]))
      if i==0:  res.SetLineColor(ROOT.kGreen)
      if i==1:  res.SetLineColor(ROOT.kMagenta)
      res.Write() 
      del hTMP
      del res
 
signalPlotFile.Close() 
