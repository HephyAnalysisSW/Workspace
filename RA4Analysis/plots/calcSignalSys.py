import ROOT
from analysisHelpers import *

ROOT.gROOT.ProcessLine(".L ../../HEPHYCommonTools/scripts/root/useNiceColorPalette.C")
ROOT.useNiceColorPalette(255)

cMC = getRefChain()
cMC.Draw("ngoodVertices>>hMCRef(60,0,60)", "weight*(ht>400&&type1phiMet>150&&(singleMuonic&&nvetoMuons==1&&nvetoElectrons==0||singleElectronic&&nvetoMuons==0&&nvetoElectrons==1))")
cMC.Draw("ngoodVertices>>hMCPUSysPlus(60,0,60)", "weightPUSysPlus*(ht>400&&type1phiMet>150&&(singleMuonic&&nvetoMuons==1&&nvetoElectrons==0||singleElectronic&&nvetoMuons==0&&nvetoElectrons==1))")
cMC.Draw("ngoodVertices>>hMCPUSysMinus(60,0,60)", "weightPUSysMinus*(ht>400&&type1phiMet>150&&(singleMuonic&&nvetoMuons==1&&nvetoElectrons==0||singleElectronic&&nvetoMuons==0&&nvetoElectrons==1))")

hMCRef = ROOT.gDirectory.Get("hMCRef")
hMCPUSysPlus = ROOT.gDirectory.Get("hMCPUSysPlus")
hMCPUSysMinus = ROOT.gDirectory.Get("hMCPUSysMinus")
hMCRef.Scale(1./hMCRef.Integral())
hMCPUSysPlus.Scale(1./hMCPUSysPlus.Integral())
hMCPUSysMinus.Scale(1./hMCPUSysMinus.Integral())

#htBins = [[400,750], [400,2500], [500,2500], [750, 2500], [1000,2500]]
#metBins = [\
#    [150, 2500],
#    [250, 2500],
#    [150, 250],
#    [250, 350],
#    [350, 450],
#    [450, 2500]]

htBins = [[400,750],  [750, 2500]]
metBins = [\
    [250, 2500],
    [150, 250],
    [250, 350],
    [350, 450],
    [450, 2500]]

from smsInfo import nfsDirectories, th2Binning, th2VarString, xAxisTitle, yAxisTitle

#sms = "T1tttt-madgraph"
#prefix = ""

#prefix = "_coarse"
#sms = "T1t1t"
#prefix = "_coarse"
#sms = "T1t1t"

sms = "T5tttt"
prefix = ""

eleEffSysEB = ROOT.TF1("eleEffSysEB", "0.916/(1+exp((6.3-x))/12)")
eleEffSysEE= ROOT.TF1("eleEffSysEE", "0.862/(1+exp((10.4-x))/14)")
muEffSys1= ROOT.TF1("muEffSys1", "0.949/(1+exp((-16.1-x))/11)")
muEffSys2= ROOT.TF1("muEffSys2", "1.01/(1+exp((-3.83-x))/14)")

if not globals().has_key("yieldRef"):
  yieldRef          = {} 
  yieldPURef          = {} 
  yieldPUSysPlus    = {} 
  yieldPUSysMinus   = {}
  yieldMuEff1Sys = {}
  yieldMuEff2Sys = {}
  yieldEleEffSys = {}
  for htb in htBins:
    yieldRef        [tuple(htb)]  = {} 
    yieldPURef        [tuple(htb)]  = {} 
    yieldPUSysPlus  [tuple(htb)]  = {} 
    yieldPUSysMinus [tuple(htb)]  = {}
    yieldMuEff1Sys [tuple(htb)]= {}
    yieldMuEff2Sys [tuple(htb)]= {}
    yieldEleEffSys [tuple(htb)]= {}
    for metb in metBins: 
      iname = "ht_"+str(htb[0])+"_"+str(htb[1])+"_met_"+str(metb[0])+"_"+str(metb[1])+"_"
      yieldRef       [tuple(htb)][tuple(metb)]   = ROOT.TH2D(iname+"yieldRef",       iname+"yieldRef",        *(th2Binning[sms+prefix]))
      yieldPURef       [tuple(htb)][tuple(metb)] = ROOT.TH2D(iname+"yieldPURef",     iname+"yieldPURef",      *(th2Binning[sms+prefix]))
      yieldPUSysPlus [tuple(htb)][tuple(metb)]   = ROOT.TH2D(iname+"yieldPUSysPlus", iname+"yieldPUSysPlus",  *(th2Binning[sms+prefix]))
      yieldPUSysMinus[tuple(htb)][tuple(metb)]   = ROOT.TH2D(iname+"yieldPUSysMinus",iname+"yieldPUSysMinus", *(th2Binning[sms+prefix]))
      yieldMuEff1Sys [tuple(htb)][tuple(metb)]   = ROOT.TH2D(iname+"yieldMuEff1Sys", iname+"yieldMuEff1Sys",  *(th2Binning[sms+prefix]))
      yieldMuEff2Sys [tuple(htb)][tuple(metb)]   = ROOT.TH2D(iname+"yieldMuEff2Sys", iname+"yieldMuEff2Sys",  *(th2Binning[sms+prefix]))
      yieldEleEffSys [tuple(htb)][tuple(metb)]   = ROOT.TH2D(iname+"yieldEleEffSys", iname+"yieldEleEffSys",  *(th2Binning[sms+prefix]))

  for varX in range(th2Binning[sms][1],th2Binning[sms][2],25):
    for varY in range(th2Binning[sms][4],th2Binning[sms][5],25):
      varYName, varXName = th2VarString[sms].split(":")
      print "varX/varY", varXName,varX,varYName,varY
      c = ROOT.TChain("Events")
      if sms == "T1t1t":
        fstringMu  = "/data/schoef/convertedTuples_v19/copyMET/Mu/"+sms+"_"+str(varY)+"_"+str(varX)+"/histo_"+sms+"_"+str(varY)+"_"+str(varX)+".root"
        fstringEle = "/data/schoef/convertedTuples_v19/copyMET/Ele/"+sms+"_"+str(varY)+"_"+str(varX)+"/histo_"+sms+"_"+str(varY)+"_"+str(varX)+".root"
      if sms == "T1tttt-madgraph":
        fstringMu  = "/data/schoef/convertedTuples_v19/copyMET/Mu/"+sms+"_"+str(varX)+"_"+str(varY)+"/histo_"+sms+"_"+str(varX)+"_"+str(varY)+".root"
        fstringEle = "/data/schoef/convertedTuples_v19/copyMET/Ele/"+sms+"_"+str(varX)+"_"+str(varY)+"/histo_"+sms+"_"+str(varX)+"_"+str(varY)+".root"
      if sms == "T5tttt":
        fstringMu  = "/data/schoef/convertedTuples_v19/copyMET/Mu/"+sms+"_"+str(varX)+"_"+str(varY)+"/histo_"+sms+"_"+str(varX)+"_"+str(varY)+".root"
        fstringEle = "/data/schoef/convertedTuples_v19/copyMET/Ele/"+sms+"_"+str(varX)+"_"+str(varY)+"/histo_"+sms+"_"+str(varX)+"_"+str(varY)+".root"
      if not (os.path.isfile(fstringMu) and os.path.isfile(fstringEle)): 
        print "Omitting",sms,varXName,varX,varYName,varY
        continue
      print "Found",sms,varXName,varX,varYName,varY
      c.Add(fstringMu)
      c.Add(fstringEle)
      if c.GetEntries()==0:
        print "Empty!->continue"
        continue
      c.Draw("ngoodVertices>>signalNvtx(60,0,60)", "weight*(ht>400&&type1phiMet>150&&(singleMuonic&&nvetoMuons==1&&nvetoElectrons==0||singleElectronic&&nvetoMuons==0&&nvetoElectrons==1))")
      signalNvtx = ROOT.gDirectory.Get("signalNvtx")
      signalNvtx.Scale(1./signalNvtx.Integral())

      rwRef = hMCRef.Clone("chMCRef")
      rwPUSysPlus = hMCPUSysPlus.Clone("chMCPUSysPlus")
      rwPUSysMinus = hMCPUSysMinus.Clone("chMCPUSysMinus")
      rwRef.Divide(signalNvtx)
      rwPUSysPlus.Divide(signalNvtx)
      rwPUSysMinus.Divide(signalNvtx)

      del signalNvtx

      commoncf = "njets>=6&&ht>400&&type1phiMet>150&&nbtags>=2&&(singleMuonic&&nvetoMuons==1&&nvetoElectrons==0||singleElectronic&&nvetoMuons==0&&nvetoElectrons==1)"
      c.Draw(">>eList", commoncf)
      elist = ROOT.gDirectory.Get("eList")
      number_events = elist.GetN()
      for i in range(0, number_events):
        if (i%10000 == 0) and i>0 :
          print i
  #      # Update all the Tuples
        if elist.GetN()>0 and number_events>0:
          c.GetEntry(elist.GetEntry(i))
        met = c.GetLeaf("type1phiMet").GetValue()
        ht = c.GetLeaf("ht").GetValue()
        w = c.GetLeaf("weight").GetValue()
        nv = c.GetLeaf("ngoodVertices").GetValue()
        b = rwRef.FindBin(nv)
        pt = c.GetLeaf("leptonPt").GetValue()
        eta = c.GetLeaf("leptonEta").GetValue()
        singleMuonic = c.GetLeaf("singleMuonic").GetValue() 
        singleElectronic = c.GetLeaf("singleElectronic").GetValue()

        for htb in htBins:
          if not (ht>=htb[0] and ht<htb[1]): continue
          for metb in metBins:
            if not (met>=metb[0] and  met<metb[1]): continue

            yieldRef[tuple(htb)][tuple(metb)].Fill(varX, varY,        w)

            yieldPURef[tuple(htb)][tuple(metb)].Fill(varX, varY,      w*rwRef.GetBinContent(b))
            yieldPUSysPlus[tuple(htb)][tuple(metb)].Fill(varX, varY,  w*rwPUSysPlus.GetBinContent(b))
            yieldPUSysMinus[tuple(htb)][tuple(metb)].Fill(varX, varY, w*rwPUSysMinus.GetBinContent(b))

            if singleMuonic:        
              yieldMuEff1Sys[tuple(htb)][tuple(metb)].Fill(varX, varY, w*muEffSys1(pt))
              yieldMuEff2Sys[tuple(htb)][tuple(metb)].Fill(varX, varY, w*muEffSys2(pt))
            else:
              yieldMuEff1Sys[tuple(htb)][tuple(metb)].Fill(varX, varY, w)
              yieldMuEff2Sys[tuple(htb)][tuple(metb)].Fill(varX, varY, w)
            wn=w
            if singleElectronic:        
              if (abs(eta)<1.4442):
                wn = eleEffSysEB(pt)*w
              else:
                wn = eleEffSysEE(pt)*w
            yieldEleEffSys[tuple(htb)][tuple(metb)].Fill(varX, varY, wn)

sys = {}
ROOT.tdrStyle.SetPadRightMargin(0.18)
c1 = ROOT.TCanvas()
for htb in htBins:
  sys[tuple(htb)]={}
  for metb in metBins:
    sys[tuple(htb)][tuple(metb)] = yieldPUSysMinus[tuple(htb)][tuple(metb)].Clone('hist2DSFunc')
    sys[tuple(htb)][tuple(metb)].Scale(-1)
    sys[tuple(htb)][tuple(metb)].Add(yieldPUSysPlus[tuple(htb)][tuple(metb)])
    sys[tuple(htb)][tuple(metb)].Divide(yieldPURef[tuple(htb)][tuple(metb)])
    sys[tuple(htb)][tuple(metb)].Scale(0.5)
    sys[tuple(htb)][tuple(metb)].GetXaxis().SetTitle(xAxisTitle[sms])
    sys[tuple(htb)][tuple(metb)].GetYaxis().SetTitle(yAxisTitle[sms])
    sys[tuple(htb)][tuple(metb)].Draw("COLZ")
    c1.Update()
    palette = sys[tuple(htb)][tuple(metb)].GetListOfFunctions().FindObject("palette");
    palette.SetX1NDC(0.83);
    palette.SetX2NDC(0.87);
    c1.Modified();
    c1.Update();
    c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngSys/sigPUSys_"+sms+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_met_"+str(metb[0])+"_"+str(metb[1])+prefix+".png")
    c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngSys/sigPUSys_"+sms+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_met_"+str(metb[0])+"_"+str(metb[1])+prefix+".pdf")
    c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngSys/sigPUSys_"+sms+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_met_"+str(metb[0])+"_"+str(metb[1])+prefix+".root")
    f = ROOT.TFile("/data/schoef/results2012/"+sms+"/PU/sigPUSys_"+sms+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_met_"+str(metb[0])+"_"+str(metb[1])+".root", "recreate")
    f.cd()
    sys[tuple(htb)][tuple(metb)].Write()
    f.Close()
    sys[tuple(htb)][tuple(metb)] = yieldRef[tuple(htb)][tuple(metb)].Clone('hist2DSFunc')
    sys[tuple(htb)][tuple(metb)].Scale(-1)
    sys[tuple(htb)][tuple(metb)].Add(yieldMuEff1Sys[tuple(htb)][tuple(metb)])
    sys[tuple(htb)][tuple(metb)].Divide(yieldRef[tuple(htb)][tuple(metb)])
    sys[tuple(htb)][tuple(metb)].GetXaxis().SetTitle(xAxisTitle[sms])
    sys[tuple(htb)][tuple(metb)].GetYaxis().SetTitle(yAxisTitle[sms])
    sys[tuple(htb)][tuple(metb)].Draw("COLZ")
    c1.Update()
    palette = sys[tuple(htb)][tuple(metb)].GetListOfFunctions().FindObject("palette");
    palette.SetX1NDC(0.83);
    palette.SetX2NDC(0.87);
    c1.Modified();
    c1.Update();
    c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngSys/sigMuEff1Sys_"+sms+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_met_"+str(metb[0])+"_"+str(metb[1])+prefix+".png")
    c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngSys/sigMuEff1Sys_"+sms+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_met_"+str(metb[0])+"_"+str(metb[1])+prefix+".pdf")
    c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngSys/sigMuEff1Sys_"+sms+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_met_"+str(metb[0])+"_"+str(metb[1])+prefix+".root")
    f = ROOT.TFile("/data/schoef/results2012/"+sms+"/MuEff1/sigMuEff1Sys_"+sms+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_met_"+str(metb[0])+"_"+str(metb[1])+".root", "recreate")
    f.cd()
    sys[tuple(htb)][tuple(metb)].Write()
    f.Close()
    sys[tuple(htb)][tuple(metb)] = yieldRef[tuple(htb)][tuple(metb)].Clone('hist2DSFunc')
    sys[tuple(htb)][tuple(metb)].Scale(-1)
    sys[tuple(htb)][tuple(metb)].Add(yieldMuEff2Sys[tuple(htb)][tuple(metb)])
    sys[tuple(htb)][tuple(metb)].Divide(yieldRef[tuple(htb)][tuple(metb)])
    sys[tuple(htb)][tuple(metb)].GetXaxis().SetTitle(xAxisTitle[sms])
    sys[tuple(htb)][tuple(metb)].GetYaxis().SetTitle(yAxisTitle[sms])
    sys[tuple(htb)][tuple(metb)].Draw("COLZ")
    c1.Update()
    palette = sys[tuple(htb)][tuple(metb)].GetListOfFunctions().FindObject("palette");
    palette.SetX1NDC(0.83);
    palette.SetX2NDC(0.87);
    c1.Modified();
    c1.Update();
    c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngSys/sigMuEff2Sys_"+sms+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_met_"+str(metb[0])+"_"+str(metb[1])+prefix+".png")
    c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngSys/sigMuEff2Sys_"+sms+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_met_"+str(metb[0])+"_"+str(metb[1])+prefix+".pdf")
    c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngSys/sigMuEff2Sys_"+sms+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_met_"+str(metb[0])+"_"+str(metb[1])+prefix+".root")
    f = ROOT.TFile("/data/schoef/results2012/"+sms+"/MuEff2/sigMuEff2Sys_"+sms+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_met_"+str(metb[0])+"_"+str(metb[1])+".root", "recreate")
    f.cd()
    sys[tuple(htb)][tuple(metb)].Write()
    f.Close()
    sys[tuple(htb)][tuple(metb)] = yieldRef[tuple(htb)][tuple(metb)].Clone('hist2DSFunc')
    sys[tuple(htb)][tuple(metb)].Scale(-1)
    sys[tuple(htb)][tuple(metb)].Add(yieldEleEffSys[tuple(htb)][tuple(metb)])
    sys[tuple(htb)][tuple(metb)].Divide(yieldRef[tuple(htb)][tuple(metb)])
    sys[tuple(htb)][tuple(metb)].GetXaxis().SetTitle(xAxisTitle[sms])
    sys[tuple(htb)][tuple(metb)].GetYaxis().SetTitle(yAxisTitle[sms])
    sys[tuple(htb)][tuple(metb)].Draw("COLZ")
    c1.Update()
    palette = sys[tuple(htb)][tuple(metb)].GetListOfFunctions().FindObject("palette");
    palette.SetX1NDC(0.83);
    palette.SetX2NDC(0.87);
    c1.Modified();
    c1.Update();
    c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngSys/sigEleEffSys_"+sms+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_met_"+str(metb[0])+"_"+str(metb[1])+prefix+".png")
    c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngSys/sigEleEffSys_"+sms+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_met_"+str(metb[0])+"_"+str(metb[1])+prefix+".pdf")
    c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngSys/sigEleEffSys_"+sms+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_met_"+str(metb[0])+"_"+str(metb[1])+prefix+".root")
    f = ROOT.TFile("/data/schoef/results2012/"+sms+"/EleEff/sigEleEffSys_"+sms+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_met_"+str(metb[0])+"_"+str(metb[1])+".root", "recreate")
    f.cd()
    sys[tuple(htb)][tuple(metb)].Write()
    f.Close()
