import ROOT
from array import array
from math import *
from Workspace.RA4Analysis.simplePlotsCommon import *

cMad = ROOT.TChain("Events")
cMad.Add("/data/schoef/convertedTuples_v10/copyMET/Mu/TTJets-53X/histo_TTJets-53X.root")
cMad.Add("/data/schoef/convertedTuples_v10/copyMET/Ele/TTJets-53X/histo_TTJets-53X.root")
cPow = ROOT.TChain("Events")
cPow.Add("/data/schoef/convertedTuples_v11/copyMET/Mu/TTJets-PowHeg/histo_TTJets-PowHeg.root")
cPow.Add("/data/schoef/convertedTuples_v11/copyMET/Ele/TTJets-PowHeg/histo_TTJets-PowHeg.root")

cData = ROOT.TChain("Events")
cData.Add("/data/schoef/convertedTuples_v11/copyMET/Mu/data/histo_data.root")
cData.Add("/data/schoef/convertedTuples_v11/copyMET/Ele/data/histo_data.root")

htvals = [\
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


htbins = [h[0] for h in htvals] + [htvals[-1][1]]
njetbins = range(3,8)+[-1]

cut = "njets==6&&ht>1000&&met>150&&met<250&&((singleMuonic&&nvetoElectrons==0&&nvetoMuons==1)||(singleElectronic&&nvetoElectrons==1&&nvetoMuons==0))"
cPow.Draw("(weightBTag2_SF)>>htmpWH(150,0,.1)",cut, "goff")
weightHist = ROOT.gDirectory.Get("htmpWH")
n = int(weightHist.Integral())
y = weightHist.GetMean()*n

import numpy as np
weightHist.Scale(1./weightHist.Integral())
wh = []
maxWeight = weightHist.GetBinLowEdge(weightHist.GetNbinsX()+1)
for i in range(1, weightHist.GetNbinsX()+1):
  wh.append(weightHist[i])


#def rebin(ar):
#  if len(ar)%2==0:
#    print "Not an odd number!"
#  res = []
#  for i in range(len(ar)/2):
#    res.append(ar[i]+ar[i+1])
#  res.append(ar[-1])
#  return res

#wh = [0.5,0,0.5]
#n=2
wh = array('f',wh)
yh = wh
#for i in range(n-1):
##  print i, n-1, "len",len(yh)
#  yh = rebin(np.convolve(yh, wh))

max2NPow = len(bin(n))-3 #2**max2NPow > n / 2
atPow = 2
yh_pow = {}
yh_pow[0] = yh
for i in range(1, max2NPow+1):
  yh_pow[i]=np.convolve(yh_pow[i-1], yh_pow[i-1])
  print "Created basis histo for 2**"+str(i),"with len", len(yh_pow[i])

bits = list(bin(n)[2:])
bits.reverse()
res = array('d', [1]) 
testcounter=0
for i, b in enumerate(bits):
  if b=='1':
    print "Folding", i ,"with len", len(yh_pow[i]), "to res with len", len(res)
    res = np.convolve(res,yh_pow[i]) 
    testcounter+=2**i

print testcounter, i

nbins = int((len(res)-1)/n + 1)
ymax = maxWeight*n

yDist = ROOT.TH1F("y", "y", 10*nbins, 0, ymax/2.)

for i in range(len(res)):
  pos = i*ymax/(len(res)-1)
  yDist.Fill( pos, res[i] )

yDist.Draw()
print yDist.GetMean(),"+/-",yDist.GetRMS() , "(true",y,")"

#weightHist_FFTMag   = ROOT.TH1F("Mag", "Mag",     200,0,30)
#weightHist_FFTPhase = ROOT.TH1F("Phase", "Phase", 200,0,30) 
#
#
#weightHist.FFT(weightHist_FFTMag, "MAG R2C M")
#weightHist.FFT(weightHist_FFTPhase, "PH R2C M")
##weightHist.FFT(weightHist_FFTPhase, "PH M")
#
#for i in range(0, weightHist_FFTMag.GetNbinsX()):
#  print "Mag", i, weightHist_FFTMag.GetBinContent(i), weightHist_FFTPhase.GetBinContent(i)
#  if not weightHist_FFTMag.GetBinContent(i)<float('inf'):
#    weightHist_FFTMag.SetBinContent(i,0.)
#  if not weightHist_FFTPhase.GetBinContent(i)<float('inf'):
#    weightHist_FFTPhase.SetBinContent(i,0.)
#
#weightHist_FFTPhase.SetLineColor(ROOT.kBlue)
#weightHist_FFTPhase.Draw()
#weightHist_FFTMag.SetLineColor(ROOT.kRed)
#weightHist_FFTMag.Draw("same")

#rData3o2 = {}
#rData4o2 = {}
#SpFData_3o2 = {} 
#SpFData_4o2 = {} 
#for nj in njetbins:
#  rData3o2[nj] = {}
#  rData4o2[nj] = {}
#  SpFData_3o2[nj] = ROOT.TH1F("SpF_3o2_Data_"+str(nj),"SpF", len(htbins) - 1, array('d',htbins))
#  SpFData_4o2[nj] = ROOT.TH1F("SpF_4o2_Data_"+str(nj),"SpF", len(htbins) - 1, array('d',htbins))
#
#for htb in htvals:
#  print "\nHT bin", htb
#  for nj in njetbins:
#    cut="met>100&&met<250&&ht>"+str(htb[0])+"&&ht<"+str(htb[1])+"&&((singleMuonic&&nvetoElectrons==0&&nvetoMuons==1)||(singleElectronic&&nvetoElectrons==1&&nvetoMuons==0))"
#    if nj>0:
#      cut = "njets=="+str(nj)+"&&"+cut
#    n_bt2 = cData.GetEntries(cut+"&&nbtags==2")
#    n_bt3 = cData.GetEntries(cut+"&&nbtags==3")
#    n_bt4 = cData.GetEntries(cut+"&&nbtags==4")
##    print "n-jet ", nj, "n-bt 2,3,4", n_bt2, n_bt3, n_bt4
#    if n_bt2>0:
#      rData3o2[nj][htb[0]] = n_bt3/float(n_bt2) 
#      rData4o2[nj][htb[0]] = n_bt4/float(n_bt2)
#      print "n-jet ", nj,"n-bt 2,3,4", n_bt2, n_bt3, n_bt4, "n-bt 3/2, 4/2", n_bt3/float(n_bt2), n_bt4/float(n_bt2)
##    else:
##      rData3o2[nj][htb[0]] = n_bt3/float('nan') 
##      rData4o2[nj][htb[0]] = n_bt4/float('nan')
##      print "n-jet ", nj, "n-bt 2,3,4", n_bt2, n_bt3, n_bt4,"n-bt 3/2, 4/2", n_bt3/float('nan'), n_bt4/float('nan')
#    b = SpFData_3o2[njetbins[0]].FindBin(htb[0])
#    if rData3o2[nj].has_key(htb[0]):
#      SpFData_3o2[nj].SetBinContent(b, rData3o2[nj][htb[0]] )
#    if n_bt3>0:
#      SpFData_3o2[nj].SetBinError(b, rData3o2[nj][htb[0]]*sqrt(1./n_bt3 + 1./n_bt2))
#    if rData4o2[nj].has_key(htb[0]):
#      SpFData_4o2[nj].SetBinContent(b, rData4o2[nj][htb[0]] )
#    if n_bt4>0:
#      SpFData_4o2[nj].SetBinError(b, rData4o2[nj][htb[0]]*sqrt(1./n_bt4 + 1./n_bt2))
#
#
#def getSpillFactor(c, cut="met>100&&ht>400&&singleMuonic", w1="2_SF", w2="3_SF"):
#  n = c.GetEntries(cut)
#  c.Draw("met>>htmp1","(weightBTag"+w1+")*("+cut+")")
#  c.Draw("met>>htmp2","(weightBTag"+w2+")*("+cut+")")
#  c.Draw("met>>htmp1W2","(weightBTag"+w1+")**2*("+cut+")")
#  c.Draw("met>>htmp2W2","(weightBTag"+w2+")**2*("+cut+")")
#  den = ROOT.gDirectory.Get("htmp1").Integral()
#  if den>0.:
#    r = ROOT.gDirectory.Get("htmp2").Integral()/den
#    var_den = ROOT.gDirectory.Get("htmp1W2").Integral()
#    var_num = ROOT.gDirectory.Get("htmp2W2").Integral()
#    return r, r/sqrt(n)
#  else:
#    return 0., 0.
#
#SpFMad_3o2 = {} 
#SpFPow_3o2 = {} 
#SpFMad_4o2 = {} 
#SpFPow_4o2 = {} 
#
#for nj in njetbins:
#  SpFMad_3o2[nj] = ROOT.TH1F("SpFMad_3o2","SpF", len(htbins) - 1, array('d',htbins))
#  SpFPow_3o2[nj] = ROOT.TH1F("SpFPow_3o2","SpF", len(htbins) - 1, array('d',htbins))
#  SpFMad_4o2[nj] = ROOT.TH1F("SpFMad_4o2","SpF", len(htbins) - 1, array('d',htbins))
#  SpFPow_4o2[nj] = ROOT.TH1F("SpFPow_4o2","SpF", len(htbins) - 1, array('d',htbins))
#for nj in njetbins:
#  for htb in htvals:
#    b = SpFMad_3o2[njetbins[0]].FindBin(htb[0])
#    cut="met>100&&met<250&&ht>"+str(htb[0])+"&&ht<"+str(htb[1])+"&&((singleMuonic&&nvetoElectrons==0&&nvetoMuons==1)||(singleElectronic&&nvetoElectrons==1&&nvetoMuons==0))"
#    if nj>0:
#      cut = "njets=="+str(nj)+"&&"+cut
#    spf, sigma_spf = getSpillFactor(cPow, cut, w1="2_SF", w2="3_SF")
#    SpFPow_3o2[nj].SetBinContent(b, spf)
#    SpFPow_3o2[nj].SetBinError(b, sigma_spf)
#    print spf, sigma_spf, cut
#    spf, sigma_spf = getSpillFactor(cMad, cut, w1="2_SF", w2="3_SF")
#    SpFMad_3o2[nj].SetBinContent(b, spf)
#    SpFMad_3o2[nj].SetBinError(b, sigma_spf)
#    print spf, sigma_spf, cut
#    spf, sigma_spf = getSpillFactor(cPow, cut, w1="2_SF", w2="4_SF")
#    SpFPow_4o2[nj].SetBinContent(b, spf)
#    SpFPow_4o2[nj].SetBinError(b, sigma_spf)
#    print spf, sigma_spf, cut
#    spf, sigma_spf = getSpillFactor(cMad, cut, w1="2_SF", w2="4_SF")
#    SpFMad_4o2[nj].SetBinContent(b, spf)
#    SpFMad_4o2[nj].SetBinError(b, sigma_spf)
#    print spf, sigma_spf, cut
#
#c1 = ROOT.TCanvas()
#for nj in njetbins:
#  l = ROOT.TLegend(0.7, 0.7, 0.99,0.99)
#  l.SetFillColor(0)
#  l.SetShadowColor(ROOT.kWhite)
#  l.SetBorderSize(1)
#  SpFMad_3o2[nj].GetYaxis().SetRangeUser(0., 1.5*max(SpFMad_3o2[nj].GetMaximum(), SpFPow_3o2[nj].GetMaximum(), SpFData_3o2[nj]))
#  SpFMad_3o2[nj].SetLineColor(ROOT.kRed)
#  SpFMad_3o2[nj].SetLineStyle(0)
#  SpFMad_3o2[nj].SetLineWidth(0)
#  SpFMad_3o2[nj].SetMarkerColor(ROOT.kRed)
#  SpFMad_3o2[nj].SetMarkerStyle(0)
#  SpFMad_3o2[nj].GetXaxis().SetTitle("H_{T} (GeV)")
#  l.AddEntry(SpFMad_3o2[nj], "3/2 Madgraph")
#  SpFMad_3o2[nj].Draw("h")
#  SpFPow_3o2[nj].SetLineColor(ROOT.kBlue)
#  SpFPow_3o2[nj].SetLineStyle(0)
#  SpFPow_3o2[nj].SetLineWidth(0)
#  SpFPow_3o2[nj].SetMarkerColor(ROOT.kBlue)
#  SpFPow_3o2[nj].SetMarkerStyle(0)
#  l.AddEntry(SpFPow_3o2[nj], "3/2 PowHeg")
#  SpFPow_3o2[nj].Draw("hsame")
#  l.AddEntry(SpFData_3o2[nj], "Data")
#  SpFData_3o2[nj].Draw("same")
#  l.Draw()
#  c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngBTag/SpF_3o2_njet_"+str(nj)+".png") 
#
#  l = ROOT.TLegend(0.7, 0.7, 0.99,0.99)
#  l.SetFillColor(0)
#  l.SetShadowColor(ROOT.kWhite)
#  l.SetBorderSize(1)
#  SpFMad_4o2[nj].GetYaxis().SetRangeUser(0., 1.5*max(SpFMad_4o2[nj].GetMaximum(), SpFPow_4o2[nj].GetMaximum(), SpFData_4o2[nj]))
#  SpFMad_4o2[nj].SetLineColor(ROOT.kRed)
#  SpFMad_4o2[nj].SetLineStyle(0)
#  SpFMad_4o2[nj].SetLineWidth(0)
#  SpFMad_4o2[nj].SetMarkerColor(ROOT.kRed)
#  SpFMad_4o2[nj].SetMarkerStyle(0)
#  SpFMad_4o2[nj].GetXaxis().SetTitle("H_{T} (GeV)")
#  l.AddEntry(SpFMad_4o2[nj], "3/2 Madgraph")
#  SpFMad_4o2[nj].Draw("h")
#  SpFPow_4o2[nj].SetLineColor(ROOT.kBlue)
#  SpFPow_4o2[nj].SetLineStyle(0)
#  SpFPow_4o2[nj].SetLineWidth(0)
#  SpFPow_4o2[nj].SetMarkerColor(ROOT.kBlue)
#  SpFPow_4o2[nj].SetMarkerStyle(0)
#  l.AddEntry(SpFPow_4o2[nj], "3/2 PowHeg")
#  SpFPow_4o2[nj].Draw("hsame")
#  l.AddEntry(SpFData_4o2[nj], "Data")
#  SpFData_4o2[nj].Draw("same")
#  l.Draw()
#  c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngBTag/SpF_4o2_njet_"+str(nj)+".png") 
#
