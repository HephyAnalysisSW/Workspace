import ROOT

#sample = "TTJets-PowHeg"
sample = "WJetsHT250"

htbins = [\
    [350,400,   "HLTHT300"],
    [400,450,   "HLTHT300"],
    [450,500,   "HLTHT350"],
    [500,550,   "HLTHT400"],
    [550,600,   "HLTHT450"],
    [600,650,   "HLTHT500"],
    [650,700,   "HLTHT550"],
    [700,750,   "HLTHT550"],
    [750,800,   "HLTHT650"],
    [800,1000,  "HLTHT650"],
    [1000,1200, "HLTHT750"],
    [1200,1500, "HLTHT750"],
    [1500,2500, "HLTHT750"]
  ]


c = ROOT.TChain("Events")
c.Add("/data/schoef/convertedTuples_v16/copyMET/Mu/"+sample+"/h*.root")
c.Add("/data/schoef/convertedTuples_v16/copyMET/Ele/"+sample+"/h*.root")

leptonCut = "((singleMuonic&&nvetoMuons==1&&nvetoElectrons==0)||(singleElectronic&&nvetoMuons==0&&nvetoElectrons==1))"
prefix = "htBase0"

def njetCut(n1,n2):
  if n1==n2 : 
    if n1<0: return "(1)"
    else: return "njets=="+str(n1)

  if n1<0:
    return "njets<="+str(n2)

  if n2<0:
    return "njets>="+str(n1)

  return "njets>="+str(n1)+"&&njets<="+str(n2)


stuff=[]

color = {(4,-1):ROOT.kBlack, (4,4):ROOT.kBlack, (5,5):ROOT.kRed, (3,3):ROOT.kBlue, (2,2):ROOT.kRed, (6,-1): ROOT.kGreen}

def getErfc(c, ht, htBase, njbin):
  if type(ht)==type([]):
    htcut = "ht>"+str(ht[0])+"&&ht<"+str(ht[1])
  else:
    htcut = "ht>"+str(ht)
  c.Draw("genmet>>hmetBase(17,125,975)", "weight*("+leptonCut+"&&ht>"+str(htBase)+"&&"+njetCut(*njbin)+")")
  cut =                                  "weight*("+leptonCut+"&&"+htcut+"&&"+njetCut(*njbin)+")"
  print "Using", cut
  c.Draw("genmet>>hmetCut(17,125,975)",  cut)
  hmetBase = ROOT.gDirectory.Get("hmetBase")
  hmetCut  = ROOT.gDirectory.Get("hmetCut")
  res = hmetCut.Clone()
  res.SetLineColor(color[tuple(njbin)])
  res.Divide(hmetBase.Clone())
  stuff.append(res)
  del hmetBase
  del hmetCut
  return res


#htvals = [400, 450, 500, 550, 600, 650, 750, 850, 1000]
#
#erfs = {}
#for ht in htvals:
#  erfs[ht]= {}
#  for ib in [[4,-1], [3,3], [2,2], [6,-1]]:
#    erfs[ht][tuple(ib)] = getErfc(c, ht, 0, ib)
#    erfs[ht][tuple(ib)].SetLineColor(color[tuple(ib)])
#
#for ht in htvals:
#  drawOpt = ""
#  c1 = ROOT.TCanvas()
#  for ib in [[4,-1], [3,3], [2,2], [6,-1]]:
#    erfs[ht][tuple(ib)].Draw(drawOpt)
#    drawOpt = "same"
#  c1.Print("/afs/hephy.at/user/s/schoefbeck/www/erf/"+prefix+"_"+sample+"_ht_"+str(ht)+".png")

def getHTShape(c, metc, njbin):
  cut =                              "weight*("+leptonCut+"&&met>"+str(metc)+"&&"+njetCut(*njbin)+")"
  print "Using", cut
  c.Draw("ht>>hht(50,0,1000)",  cut)
  hht  = ROOT.gDirectory.Get("hht")
  res = hht.Clone()
  res.SetLineColor(color[tuple(njbin)])
  stuff.append(res)
  del hht
  return res

#hts = {}
#for ib in [[4,-1], [3,3], [2,2], [6,-1]]:
#  hts[tuple(ib)] = getHTShape(c, 300, ib)
#
#drawOpt = ""
#c1 = ROOT.TCanvas()
#max=0.
#for ib in [[4,-1], [3,3], [2,2], [6,-1]]:
#  tmax= hts[tuple(ib)].GetMaximum()
#  if tmax>max: max = tmax
#
#for ib in [[4,-1], [3,3], [2,2], [6,-1]]:
#  hts[tuple(ib)].Draw(drawOpt)
#  hts[tuple(ib)].GetYaxis().SetRangeUser(0.1, 7*max)
#  drawOpt = "same"
#del c1
#
#c1 = ROOT.TCanvas()
#c1.SetLogy()
#c1.Print("/afs/hephy.at/user/s/schoefbeck/www/erf/"+prefix+"_"+sample+"_ht.png")
#
#for htval in htbins:
#  erf_4j = getErfc(c, htval, 0, [4,4])
#  erf_3j = getErfc(c, htval, 0, [5,5])
#  erf_2j = getErfc(c, htval, 0, [6,-1])
#  erf_3j.GetYaxis().SetRangeUser(10**(-3), 1.)
#  erf_3j.Draw()
#  erf_4j.Draw("same")
#  erf_2j.Draw("same")
#  c1.Print("/afs/hephy.at/user/s/schoefbeck/www/erf/"+prefix+"_"+sample+"_ht_highNJets_"+str(htval[0])+"_"+str(htval[1])+".png")

def getGenErfc(c, ht, htBase, njbin, lepPtCut = 20):
#  genCut = "(antinuMu+nuMu+antinuE+nuE==1)&&(antinuTau+nuTau==0)&&"+leptonCut
  genCut = "(1)"
  lepCut = "((abs(l0Pdg)==11&&l0Eta<2.5&&l0Pt>"+str(lepPtCut)+")||(abs(l0Pdg)==13&&l0Eta<2.1&&l0Pt>"+str(lepPtCut)+"))"
#  lepCut = "("+lCut+"||"+lCut.replace("l0","l1")+")" 
  if type(ht)==type([]):
    htcut = "ht>"+str(ht[0])+"&&ht<"+str(ht[1])
  else:
    htcut = "ht>"+str(ht)
  c.Draw("genmet>>hmetBase(17,125,975)", "weight*("+genCut+"&&"+lepCut+"&&ht>"+str(htBase)+"&&"+njetCut(*njbin)+")")
  cut =                                 "weight*("+genCut+"&&"+lepCut+"&&"+htcut+"&&"+njetCut(*njbin)+")"
  print "Using", cut
  c.Draw("met>>hmetCut(17,125,975)",  cut)
  hmetBase = ROOT.gDirectory.Get("hmetBase")
  hmetCut  = ROOT.gDirectory.Get("hmetCut")
  res = hmetCut.Clone()
  res.SetLineColor(color[tuple(njbin)])
  res.Divide(hmetBase.Clone())
  stuff.append(res)
  del hmetBase
  del hmetCut
  return res
