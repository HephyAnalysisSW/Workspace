import ROOT
from math import *
import os

def getSignalYield(btb, htb, metb, metvar, minNJet, varX, varY, sms,  dir = '/data/adamwo/convertedTuples_v19/copyMET/', weight = "weight", correctForFastSim = False):

  if sms == "T1tttt" or sms=="T1tttt-madgraph":
    fstringMu  = dir+"/Mu/"+sms+"_"+str(varX)+"_"+str(varY)+"/histo_"+sms+"_"+str(varX)+"_"+str(varY)+".root"
    fstringEle = dir+"/Ele/"+sms+"_"+str(varX)+"_"+str(varY)+"/histo_"+sms+"_"+str(varX)+"_"+str(varY)+".root"
  if sms == "T1t1t":
    fstringMu  = dir+"/Mu/"+sms+"_"+str(varY)+"_"+str(varX)+"/histo_"+sms+"_"+str(varY)+"_"+str(varX)+".root"
    fstringEle = dir+"/Ele/"+sms+"_"+str(varY)+"_"+str(varX)+"/histo_"+sms+"_"+str(varY)+"_"+str(varX)+".root"
  if sms == "T5tttt":
    fstringMu  = dir+"/Mu/"+sms+"_"+str(varX)+"_"+str(varY)+"/histo_"+sms+"_"+str(varX)+"_"+str(varY)+".root"
    fstringEle = dir+"/Ele/"+sms+"_"+str(varX)+"_"+str(varY)+"/histo_"+sms+"_"+str(varX)+"_"+str(varY)+".root"
  if not (os.path.isfile(fstringMu) and os.path.isfile(fstringEle)):
    print "[getSignalYield] File missing!", fstringMu,fstringEle
    return 
  c = ROOT.TChain("Events")
  c.Add(fstringMu)
  c.Add(fstringEle)
  if c.GetEntries()==0:
    print "[getSignalYield] Files empty!"
    return 

  leptonCut = metvar+">=150&&njets>="+str(minNJet)+"&&ht>=400&&((singleMuonic&&nvetoMuons==1&&nvetoElectrons==0)||(singleElectronic&&nvetoMuons==0&&nvetoElectrons==1))"
  cut =  leptonCut+"&&ht>="+str(htb[0])+"&&ht<"+str(htb[1])+"&&"+metvar+">="+str(metb[0])+"&&"+metvar+"<"+str(metb[1])
  if btb>=0:
    cut+="&&"+btbCut[btb]

  gluinoSystemPt = "sqrt( (gluino0Pt*cos(gluino0Phi) + gluino1Pt*cos(gluino1Phi))**2 + (gluino0Pt*sin(gluino0Phi) + gluino1Pt*sin(gluino1Phi))**2)"
  ISRRefWeight  = "(1.*("+gluinoSystemPt+"<120) + "+".95*( "+gluinoSystemPt+">120&&"+gluinoSystemPt+"<150) + "+".90*( "+gluinoSystemPt+">150&&"+gluinoSystemPt+"<250) + "+".80*( "+gluinoSystemPt+">250))"

  leptonAndHadWeight = "(0.98*(0.95*singleMuonic + singleElectronic*(0.86*(abs(leptonEta)>1.552) + 0.98*(abs(leptonEta)<=1.552) )))"
  leptonTriggerEff = "(0.96*singleElectronic + singleMuonic*( (abs(leptonEta)<0.9)*0.98 + (abs(leptonEta)>0.9)*0.84) )"

  cut = weight+"*("+cut+")"
  print cut
  if correctForFastSim:
    cut = ISRRefWeight+"*"+leptonAndHadWeight+"*"+leptonTriggerEff+"*"+cut
#    cut = leptonAndHadWeight+"*"+cut
    print "[getSignalYield] Correcting ISR and lepton weight"
  c.Draw(metvar+">>htmp(1,0,2500)", cut, "goff")
  htmp =  ROOT.gDirectory.Get("htmp")
  res = htmp.Integral()
  del c
  del htmp
  return res

def getBkgChain(dir = "/data/schoef/convertedTuples_v19/copyMET/", samples=None):
  if (not samples) or not ( type(samples)==type("") or type(samples)==type([]) or type(samples)==type(()))  :return
  if type(samples)==type(""):
    samples=[samples]
  cMC   = ROOT.TChain("Events")
  for s in samples:
    for l in ["Mu","Ele"]:
      fname = dir+"/"+l+"/"+s+"/histo_"+s+".root"
      if os.path.isfile(fname):
        print "Adding",fname
        cMC.Add(fname)
      else:
        print fname,"not found!"
  return cMC


def getSignalChain(varX, varY, sms,  dir = '/data/schoef/convertedTuples_v19/copyMET/'):
  if sms == "T1tttt" or sms=="T1tttt-madgraph":
    fstringMu  = dir+"/Mu/"+sms+"_"+str(varX)+"_"+str(varY)+"/histo_"+sms+"_"+str(varX)+"_"+str(varY)+".root"
    fstringEle = dir+"/Ele/"+sms+"_"+str(varX)+"_"+str(varY)+"/histo_"+sms+"_"+str(varX)+"_"+str(varY)+".root"
  if sms == "T1t1t":
    fstringMu  = dir+"/Mu/"+sms+"_"+str(varY)+"_"+str(varX)+"/histo_"+sms+"_"+str(varY)+"_"+str(varX)+".root"
    fstringEle = dir+"/Ele/"+sms+"_"+str(varY)+"_"+str(varX)+"/histo_"+sms+"_"+str(varY)+"_"+str(varX)+".root"
  if sms == "T5tttt":
    fstringMu  = dir+"/Mu/"+sms+"_"+str(varX)+"_"+str(varY)+"/histo_"+sms+"_"+str(varX)+"_"+str(varY)+".root"
    fstringEle = dir+"/Ele/"+sms+"_"+str(varX)+"_"+str(varY)+"/histo_"+sms+"_"+str(varX)+"_"+str(varY)+".root"
  if not (os.path.isfile(fstringMu) and os.path.isfile(fstringEle)):
    print "[getSignalYield] File missing!", fstringMu,fstringEle
    return 
  c = ROOT.TChain("Events")
  print "Adding",fstringMu
  c.Add(fstringMu)
  print "Adding",fstringEle
  c.Add(fstringEle)
  
  if c.GetEntries()==0:
    print "[getSignalYield] Files empty!"
    return 
  return c

def getCutSignalYield(c, cut,  weight = "weight", correctForFastSim = True, mtcut = None) :

  if correctForFastSim:
    gluinoSystemPt = "sqrt( (gluino0Pt*cos(gluino0Phi) + gluino1Pt*cos(gluino1Phi))**2 + (gluino0Pt*sin(gluino0Phi) + gluino1Pt*sin(gluino1Phi))**2)"
    ISRRefWeight  = "(1.*("+gluinoSystemPt+"<120) + "+".95*( "+gluinoSystemPt+">120&&"+gluinoSystemPt+"<150) + "+".90*( "+gluinoSystemPt+">150&&"+gluinoSystemPt+"<250) + "+".80*( "+gluinoSystemPt+">250))"

    leptonAndHadWeight = "(0.98*(0.95*singleMuonic + singleElectronic*(0.86*(abs(leptonEta)>1.552) + 0.98*(abs(leptonEta)<=1.552) )))"
    leptonTriggerEff = "(0.96*singleElectronic + singleMuonic*( (abs(leptonEta)<0.9)*0.98 + (abs(leptonEta)>0.9)*0.84) )"
    weight = ISRRefWeight+"*"+leptonAndHadWeight+"*"+leptonTriggerEff+"*("+weight+")"
#    cut = leptonAndHadWeight+"*"+cut
    print "[getSignalYield] Correcting ISR and lepton weight"

  weight = weight+"*("+cut+")"
  if mtcut:
    from funcs import type1phiMT
    mTVar = "sqrt(2.*(leptonPt*(type1phiMet - type1phiMetpx*cos(leptonPhi) - type1phiMetpy*sin(leptonPhi) )))"
    weight = weight+"*("+cut+")*("+mTVar+">="+str(mtcut[0])+"&&"+mTVar+"<"+str(mtcut[1])+")"
#  print weight
  htmp = ROOT.TH1F("htmp","htmp",1,0,2500)
  htmp.Sumw2()
  c.Draw("1>>htmp", weight, "goff")
#  htmp =  ROOT.gDirectory.Get("htmp")
  res = htmp.GetBinContent(1)
  err = htmp.GetBinError(1)
  del c
  del htmp
  return {'res':res, 'err':err}


