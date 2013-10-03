from simplePlotsCommon import *
import pickle
from array import array

htvals = [\
    [400, 750],
    [400,2500  ],
    [500,2500  ],
    [750,2500  ],
    [1000,2500 ],
  ]       
metvals = [\
    [150,2500  ],
    [250,2500  ],
    [150,250  ],
    [250,350  ],
    [350,450 ],
    [450,2500 ],
    [250, 275],
    [275, 300],
    [300, 350],
    [150,175],
    [175,200],
    [200,225],
    [225,250]
  ]       
          
          
htbins = [h[0] for h in htvals] + [htvals[-1][1]]


cMC = ROOT.TChain("Events")
cMC.Add("/data/schoef/convertedTuples_v17/copyMET/Ele/TTJets-PowHeg/h*.root")
cMC.Add("/data/schoef/convertedTuples_v17/copyMET/Mu/TTJets-PowHeg/h*.root")
cData = ROOT.TChain("Events")
cData.Add("/data/schoef/convertedTuples_v17/copyMET/Ele/data/h*.root")
cData.Add("/data/schoef/convertedTuples_v17/copyMET/Mu/data/h*.root")

var = "probOneMoreBTagSF"
ofile = ROOT.TFile("/afs/hephy.at/user/s/schoefbeck/www/pngBTag/"+var+".root", "recreate")

sysDict = {}
for htl, hth in htvals:
  sysDict[tuple([htl, hth])] = {}

for metl, meth in metvals:
#  for njl, njh in [[3,3],[4,4],[5,5],[6,99], [3,5]]: 
  for njl, njh in [ [3,5] ]: 
    c1 = ROOT.TCanvas()
    cut = "weight*(nbtags>=2&&ht>400&&njets>="+str(njl)+"&&njets<="+str(njh)+"&&type1phiMet>150&&type1phiMet>"+str(metl)+"&&type1phiMet<"+str(meth)+"&&(singleMuonic&&nvetoMuons==1&&nvetoElectrons==0||singleElectronic&&nvetoMuons==0&&nvetoElectrons==1))"
    print cut
    hMC = ROOT.TProfile("MC_"+var, "MC_"+var, len(htbins) - 1, array('d',htbins))
    hData = ROOT.TProfile("Data_"+var, "Data_"+var, len(htbins) - 1, array('d',htbins))
    l = ROOT.TLegend(0.7, 0.7, 0.99,0.99)
    l.SetFillColor(0)
    l.SetShadowColor(ROOT.kWhite)
    l.SetBorderSize(1)
    hMC.GetYaxis().SetRangeUser(0,1)
    hMC.SetLineColor(ROOT.kRed)
    cMC.Draw(var+":ht>>MC_"+var, cut)
    cData.Draw(var+":ht>>Data_"+var, cut)
    hMC = ROOT.gDirectory.Get("MC_"+var).Clone()
    hMC.SetMarkerStyle(1)
    hMC.GetXaxis().SetTitle("H_{T} (GeV)")
    hMC.GetYaxis().SetTitle("fake probability")
    hData = ROOT.gDirectory.Get("Data_"+var).Clone()
    hMC.Draw("histe")
    hData.SetMarkerStyle(1)
    hData.SetLineColor(ROOT.kBlue)
    hData.Draw("histesame")
    l.AddEntry(hMC, "Simulation")
    l.AddEntry(hData, "Data")
    l.Draw()
    c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngBTag/"+var+"_njets_"+str(njl)+"_"+str(njh)+"_met_"+str(metl)+"_"+str(meth)+".png")
    c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngBTag/"+var+"_njets_"+str(njl)+"_"+str(njh)+"_met_"+str(metl)+"_"+str(meth)+".pdf")
    c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngBTag/"+var+"_njets_"+str(njl)+"_"+str(njh)+"_met_"+str(metl)+"_"+str(meth)+".root")
    del l
    del c1
    hname = var+"_njets_"+str(njl)+"_"+str(njh)+"_met_"+str(metl)+"_"+str(meth)
    hMC.Clone("MC_"+hname).Write()
    hData.Clone("Data_"+hname).Write()
    hRatio = hData.Clone("Ratio_"+hname)
    hRatio.Divide(hMC)
    hRatio.Write()
    maxDeviation = 0.
    for htl, hth in htvals:
      ibin = hRatio.FindBin(htl)
      if hMC.GetBinContent(ibin)==0.0: continue
      dev = abs(1. - hRatio.GetBinContent(ibin))
      print htl, hth, hMC.GetBinContent(ibin), hData.GetBinContent(ibin), dev
      if dev>maxDeviation:
         maxDeviation = dev
    print maxDeviation
    for htl, hth in htvals:
      ibin = hRatio.FindBin(htl)
      if hMC.GetBinContent(ibin)==0.0: sys = maxDeviation
      else: sys = abs(1. - hRatio.GetBinContent(ibin))
      if metl==450 and meth==2500: sys = maxDeviation
      print "Sys: met",metl,meth,"ht",htl,hth, sys
      sysDict[tuple([htl, hth])][tuple([metl, meth])] = sys
    del hMC, hData
       
ofile.Close()

pickle.dump(sysDict, file('/data/schoef/results2012/SpillFactorDataMCSys.pkl', 'w')) 
