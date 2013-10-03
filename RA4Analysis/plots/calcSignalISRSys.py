import ROOT, pickle, os
from math import sqrt
ROOT.gROOT.ProcessLine(".L ../../Scripts/aclic/tdrstyle.C")
ROOT.setTDRStyle()

ROOT.gROOT.ProcessLine(".L ../../Scripts/aclic/useNiceColorPalette.C")
ROOT.useNiceColorPalette(255)
ROOT.tdrStyle.SetPadRightMargin(0.16)

prefix = ""

small = False

#sms = "T5tttt"
#sms = "T1t1t"
sms = "T1tttt-madgraph"

print "SMS", sms
c = ROOT.TChain("Events")

from smsInfo import nfsDirectories, th2Binning, th2VarString, xAxisTitle, yAxisTitle
#for d in nfsDirectories[sms]:
#  if small:
#    c.Add(d+"/histo_10_*.root")
#  else:
#    c.Add(d+"/histo_*.root")

for varX in range(th2Binning[sms][1],th2Binning[sms][2],25):
  for varY in range(th2Binning[sms][4],th2Binning[sms][5],25):
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


htBins = [(400, 750), (750, 2500), (1000, 2500)]
metBins = [\
#    (150, 2500),
    (450, 2500),
    (350, 450),
    (250, 350),
    (150, 250),
    (250, 2500)]
#htBins = [(750, 2500)]
#metBins = [(250, 2500)]

btbCut={'2':"nbtags==2", '1':'nbtags==1', '0':'nbtags==0', 2:"nbtags==2",'2p':'nbtags>=2', 1:'nbtags==1', 0:'nbtags==0', 'ex2':"nbtags==2", '3p':"nbtags>=3", 3:"nbtags>=3", 'none':"(1)"}

lcut = 'njets>=6&&((singleMuonic && nvetoMuons==1 && nvetoElectrons==0) || (singleElectronic && nvetoElectrons == 1 && nvetoMuons == 0))'

for htb in htBins:
  for metb in metBins:
    for btb in ['3p', '2']:
      iname = "h_btb"+btb+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_met_"+str(metb[0])+"_"+str(metb[1])
      print "Calculating", htb, metb, btb
  
      hISRUp = ROOT.TH2D(iname+"_ISRUp", iname+"_ISRUp",       *(th2Binning[sms]))
      hISRDown = ROOT.TH2D(iname+"_ISRDown", iname+"_ISRDown", *(th2Binning[sms]))
      hRef   = ROOT.TH2D(iname+"_Ref", iname+"_Ref",           *(th2Binning[sms]))
      gluinoSystemPt = "sqrt( (gluino0Pt*cos(gluino0Phi) + gluino1Pt*cos(gluino1Phi))**2 + (gluino0Pt*sin(gluino0Phi) + gluino1Pt*sin(gluino1Phi))**2)"
      ISRRefWeight  = "(1.*("+gluinoSystemPt+"<120) + "+".95*( "+gluinoSystemPt+">120&&"+gluinoSystemPt+"<150) + "+".90*( "+gluinoSystemPt+">150&&"+gluinoSystemPt+"<250) + "+".80*( "+gluinoSystemPt+">250))" 
      ISRDownWeight = "(1.*("+gluinoSystemPt+"<120) + "+".90*( "+gluinoSystemPt+">120&&"+gluinoSystemPt+"<150) + "+".80*( "+gluinoSystemPt+">150&&"+gluinoSystemPt+"<250) + "+".60*( "+gluinoSystemPt+">250))" 
      ISRUpWeight = "(1)"
      cut = lcut+'&&ht>'+str(htb[0])+'&&ht<'+str(htb[1])+'&&type1phiMet>'+str(metb[0])+'&&type1phiMet<'+str(metb[1])
      print "Up!"
      c.Draw(th2VarString[sms]+' >> '+iname+'_ISRUp', '('+ISRUpWeight+')*('+cut+'&&'+btbCut[btb]+')', 'goff')    
      print "Down!"
      c.Draw(th2VarString[sms]+' >> '+iname+'_ISRDown', '('+ISRDownWeight+')*('+cut+'&&'+btbCut[btb]+')', 'goff')
      print "Ref!"
      c.Draw(th2VarString[sms]+' >> '+iname+'_Ref', '('+ISRRefWeight+')*('+cut+'&&'+btbCut[btb]+')', 'goff')

      c1 = ROOT.TCanvas()
      sys = hISRDown.Clone('hist2DSFunc')
      sys.Scale(-1)
      sys.Add(hISRUp)
      sys.Divide(hRef)
      sys.Scale(0.5)
      sys.GetXaxis().SetTitle(xAxisTitle[sms])
      sys.GetYaxis().SetTitle(yAxisTitle[sms])
      sys.GetZaxis().SetRangeUser(0,0.3)

      sys.Draw("COLZ")
     
      c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngSys/sigISRSys_"+sms+"_bt"+btb+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_met_"+str(metb[0])+"_"+str(metb[1])+prefix+".png")
      c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngSys/sigISRSys_"+sms+"_bt"+btb+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_met_"+str(metb[0])+"_"+str(metb[1])+prefix+".pdf")
      c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngSys/sigISRSys_"+sms+"_bt"+btb+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_met_"+str(metb[0])+"_"+str(metb[1])+prefix+".root")
      f = ROOT.TFile("/data/schoef/results2012/"+sms+"/ISR/sigISRSys_"+sms+"_bt"+btb+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_met_"+str(metb[0])+"_"+str(metb[1])+".root", "recreate")
      f.cd()
      sys.Write()
      f.Close()
      del c1
