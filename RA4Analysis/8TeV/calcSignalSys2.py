import ROOT, sys
from analysisHelpers import *

ROOT.gROOT.ProcessLine(".L ../../HEPHYPythonTools/scripts/root/useNiceColorPalette.C")
ROOT.useNiceColorPalette(255)
small = False
#prefix = "_coarse"
prefix=""
sms = "T1tttt-madgraph"
#prefix=""
#sms = "T5tttt"

c       = ROOT.TChain("Events")
cJESPlus= ROOT.TChain("Events")
cJESMinus= ROOT.TChain("Events")

from smsInfo import nfsDirectories, th2Binning, th2VarString, xAxisTitle, yAxisTitle

for varX in range(th2Binning[sms][1],th2Binning[sms][2],25):
  for varY in range(th2Binning[sms][4],th2Binning[sms][5],25):
#for mgl in range(400,1800,25):
#  for mn in range(0,mgl-350,25):
#    if small and (mgl!=1000 ): continue
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
      continue
    c.Add(fstringMu)
    c.Add(fstringEle)
    cJESPlus.Add(fstringMu.replace("copyMET", "copyMET_JES+"))
    cJESPlus.Add(fstringEle.replace("copyMET", "copyMET_JES+"))
    cJESMinus.Add(fstringMu.replace("copyMET", "copyMET_JES-"))
    cJESMinus.Add(fstringEle.replace("copyMET", "copyMET_JES-"))

#htBins = [[400,750], [400,2500], [500,2500], [750, 2500], [1000,2500]]
htBins = [[400,750], [750, 2500], [1000,2500]]
metBins = [\
#    [150, 2500],
    [250, 2500],
    [150, 250],
    [250, 350],
    [350, 450],
    [450, 2500]]

if small:
  htBins = [[750,2500]]
  metBins = [\
      [450, 2500]]

if len(sys.argv)>=5:
  htBins = [[sys.argv[1], sys.argv[2]]]
  metBins = [[sys.argv[3], sys.argv[4]]]

nbinsx = 48/4
nbinsy = 52/4

lcut = 'njets>=6&&((singleMuonic && nvetoMuons==1 && nvetoElectrons==0) || (singleElectronic && nvetoElectrons == 1 && nvetoMuons == 0))'
btbCut={'2':"nbtags==2", '1':'nbtags==1', '0':'nbtags==0', 2:"nbtags==2",'2p':'nbtags>=2', 1:'nbtags==1', 0:'nbtags==0', 'ex2':"nbtags==2", '3p':"nbtags>=3", 3:"nbtags>=3", 'none':"(1)"}
yieldJESRef          = {} 
yieldJESSysPlus    = {} 
yieldJESSysMinus   = {}
yieldSFRef          = {} 
yieldSFbSysPlus = {}
yieldSFbSysMinus = {}
yieldSFlSysPlus = {}
yieldSFlSysMinus = {}
for htb in htBins:
  yieldJESRef        [tuple(htb)]  = {} 
  yieldJESSysPlus  [tuple(htb)]  = {} 
  yieldJESSysMinus [tuple(htb)]  = {}
  yieldSFRef        [tuple(htb)]  = {} 
  yieldSFbSysPlus  [tuple(htb)]  = {} 
  yieldSFbSysMinus [tuple(htb)]  = {}
  yieldSFlSysPlus  [tuple(htb)]  = {} 
  yieldSFlSysMinus [tuple(htb)]  = {}
  for metb in metBins: 
    yieldJESRef       [tuple(htb)][tuple(metb)]   = {}
    yieldJESSysPlus [tuple(htb)][tuple(metb)]   = {}
    yieldJESSysMinus[tuple(htb)][tuple(metb)]   = {}
    yieldSFRef      [tuple(htb)][tuple(metb)]   = {}
    yieldSFbSysPlus [tuple(htb)][tuple(metb)]   = {}
    yieldSFbSysMinus[tuple(htb)][tuple(metb)]   = {}
    yieldSFlSysPlus [tuple(htb)][tuple(metb)]   = {}
    yieldSFlSysMinus[tuple(htb)][tuple(metb)]   = {}
    for btb in ['2', '3p']:
      print "ht",htb,"met",metb,"btb",btb
      iname = "btb"+btb+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_met_"+str(metb[0])+"_"+str(metb[1])
      yieldJESRef       [tuple(htb)][tuple(metb)][btb]    = ROOT.TH2D(iname+"_yieldJESRef", iname+"_yieldJESRef",           *(th2Binning[sms]))
      yieldJESSysPlus [tuple(htb)][tuple(metb)][btb]      = ROOT.TH2D(iname+"_yieldJESSysPlus", iname+"_yieldJESSysPlus",   *(th2Binning[sms]))
      yieldJESSysMinus[tuple(htb)][tuple(metb)][btb]      = ROOT.TH2D(iname+"_yieldJESSysMinus", iname+"_yieldJESSysMinus", *(th2Binning[sms]))
      yieldSFRef       [tuple(htb)][tuple(metb)][btb]     = ROOT.TH2D(iname+"_yieldSFRef", iname+"_yieldSFRef",             *(th2Binning[sms]))
      yieldSFbSysPlus [tuple(htb)][tuple(metb)][btb]      = ROOT.TH2D(iname+"_yieldSFbSysPlus", iname+"_yieldSFbSysPlus",   *(th2Binning[sms]))
      yieldSFbSysMinus[tuple(htb)][tuple(metb)][btb]      = ROOT.TH2D(iname+"_yieldSFbSysMinus", iname+"_yieldSFbSysMinus", *(th2Binning[sms]))
      yieldSFlSysPlus [tuple(htb)][tuple(metb)][btb]      = ROOT.TH2D(iname+"_yieldSFlSysPlus", iname+"_yieldSFlSysPlus",   *(th2Binning[sms]))
      yieldSFlSysMinus[tuple(htb)][tuple(metb)][btb]      = ROOT.TH2D(iname+"_yieldSFlSysMinus", iname+"_yieldSFlSysMinus", *(th2Binning[sms]))

      cut = lcut+'&&ht>'+str(htb[0])+'&&ht<'+str(htb[1])+'&&type1phiMet>'+str(metb[0])+'&&type1phiMet<'+str(metb[1])
      c.Draw(         th2VarString[sms]+' >> '+iname+'_yieldJESRef', 'weight*('+cut+'&&'+btbCut[btb]+')', 'goff')
      cJESPlus.Draw(  th2VarString[sms]+' >> '+iname+'_yieldJESSysPlus', 'weight*('+cut+'&&'+btbCut[btb]+')', 'goff')
      cJESMinus.Draw( th2VarString[sms]+' >> '+iname+'_yieldJESSysMinus', 'weight*('+cut+'&&'+btbCut[btb]+')', 'goff')

      btweight = "weightBTag"+btb+"_SF"
      btweight_SF_b_Up = btweight+"_b_Up"
      btweight_SF_b_Down = btweight+"_b_Down"
      btweight_SF_light_Up = btweight+"_light_Up"
      btweight_SF_light_Down = btweight+"_light_Down"
      c.Draw(th2VarString[sms]+' >> '+iname+'_yieldSFRef', btweight+'*('+cut+')', 'goff')
      c.Draw(th2VarString[sms]+' >> '+iname+'_yieldSFbSysPlus', btweight_SF_b_Up+'*('+cut+')', 'goff')
      c.Draw(th2VarString[sms]+' >> '+iname+'_yieldSFbSysMinus', btweight_SF_b_Down+'*('+cut+')', 'goff')
      c.Draw(th2VarString[sms]+' >> '+iname+'_yieldSFlSysPlus', btweight_SF_light_Up+'*('+cut+')', 'goff')
      c.Draw(th2VarString[sms]+' >> '+iname+'_yieldSFlSysMinus', btweight_SF_light_Down+'*('+cut+')', 'goff')

ROOT.tdrStyle.SetPadRightMargin(0.18)
c1 = ROOT.TCanvas()
for htb in htBins:
  for metb in metBins:
    for btb in ['2', '3p']:
      sys = yieldJESSysMinus[tuple(htb)][tuple(metb)][btb].Clone('hist2DSFunc')
      sys.Scale(-1)
      sys.Add(yieldJESSysPlus[tuple(htb)][tuple(metb)][btb])
      sys.Divide(yieldJESRef[tuple(htb)][tuple(metb)][btb])
      sys.Scale(0.5)
      if htb==[750, 2500] and metb==[450, 2500] and btb=='2':
        sys.SetBinContent(sys.FindBin(475,100), 0.)
      if htb==[750, 2500] and metb==[450, 2500] and btb=='3p':
        sys.SetBinContent(sys.FindBin(400,100), 0.)
      sys.GetXaxis().SetTitle(xAxisTitle[sms])
      sys.GetYaxis().SetTitle(yAxisTitle[sms])
      sys.Draw("COLZ")
      c1.Update()
      palette = sys.GetListOfFunctions().FindObject("palette");
      palette.SetX1NDC(0.83);
      palette.SetX2NDC(0.87);
      c1.Modified();
      c1.Update();
      c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngSys/sigJESSys_"+sms+"_bt"+btb+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_met_"+str(metb[0])+"_"+str(metb[1])+prefix+".png")
      c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngSys/sigJESSys_"+sms+"_bt"+btb+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_met_"+str(metb[0])+"_"+str(metb[1])+prefix+".pdf")
      c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngSys/sigJESSys_"+sms+"_bt"+btb+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_met_"+str(metb[0])+"_"+str(metb[1])+prefix+".root")
      f = ROOT.TFile("/data/schoef/results2012/sigJESSys_"+sms+"_bt"+btb+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_met_"+str(metb[0])+"_"+str(metb[1])+".root", "recreate")
      f.cd()
      sys.Write()
      f.Close()
      sys = yieldSFbSysMinus[tuple(htb)][tuple(metb)][btb].Clone('hist2DSFunc')
      sys.Scale(-1)
      sys.Add(yieldSFbSysPlus[tuple(htb)][tuple(metb)][btb])
      sys.Divide(yieldSFRef[tuple(htb)][tuple(metb)][btb])
      sys.Scale(0.5)
      sys.GetXaxis().SetTitle(xAxisTitle[sms])
      sys.GetYaxis().SetTitle(yAxisTitle[sms])
      sys.Draw("COLZ")
      c1.Update()
      palette = sys.GetListOfFunctions().FindObject("palette");
      palette.SetX1NDC(0.83);
      palette.SetX2NDC(0.87);
      c1.Modified();
      c1.Update();
      c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngSys/sigSFbSys_"+sms+"_bt"+btb+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_met_"+str(metb[0])+"_"+str(metb[1])+prefix+".png")
      c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngSys/sigSFbSys_"+sms+"_bt"+btb+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_met_"+str(metb[0])+"_"+str(metb[1])+prefix+".pdf")
      c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngSys/sigSFbSys_"+sms+"_bt"+btb+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_met_"+str(metb[0])+"_"+str(metb[1])+prefix+".root")
      f = ROOT.TFile("/data/schoef/results2012/sigSFbSys_"+sms+"_bt"+btb+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_met_"+str(metb[0])+"_"+str(metb[1])+".root", "recreate")
      f.cd()
      sys.Write()
      f.Close()
      sys = yieldSFlSysMinus[tuple(htb)][tuple(metb)][btb].Clone('hist2DSFunc')
      sys.Scale(-1)
      sys.Add(yieldSFlSysPlus[tuple(htb)][tuple(metb)][btb])
      sys.Divide(yieldSFRef[tuple(htb)][tuple(metb)][btb])
      sys.Scale(0.5)
      sys.GetXaxis().SetTitle(xAxisTitle[sms])
      sys.GetYaxis().SetTitle(yAxisTitle[sms])
      sys.Draw("COLZ")
      c1.Update()
      palette = sys.GetListOfFunctions().FindObject("palette");
      palette.SetX1NDC(0.83);
      palette.SetX2NDC(0.87);
      c1.Modified();
      c1.Update();
      c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngSys/sigSFlSys_"+sms+"_bt"+btb+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_met_"+str(metb[0])+"_"+str(metb[1])+prefix+".png")
      c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngSys/sigSFlSys_"+sms+"_bt"+btb+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_met_"+str(metb[0])+"_"+str(metb[1])+prefix+".pdf")
      c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngSys/sigSFlSys_"+sms+"_bt"+btb+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_met_"+str(metb[0])+"_"+str(metb[1])+prefix+".root")
      f = ROOT.TFile("/data/schoef/results2012/sigSFlSys_"+sms+"_bt"+btb+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_met_"+str(metb[0])+"_"+str(metb[1])+".root", "recreate")
      f.cd()
      sys.Write()
      f.Close()
