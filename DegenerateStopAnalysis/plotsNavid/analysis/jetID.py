from Workspace.DegenerateStopAnalysis.navidPlotTools import *

import ROOT
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain, getChunks

#from Workspace.HEPHYPythonTools.helpers import getChunksFromNFS, getChunksFromDPM, getChunks
#from Workspace.DegenerateStopAnalysis.cmgTuples_v1_Phys14 import *

import os
import math
tableDir="/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/analysis/postProcessed_v4/tables/"

t = ROOT.TChain("tree")

t.Add("/afs/cern.ch/work/n/nrad/delme/CMSSW_7_2_3/src/CMGTools/TTHAnalysis/cfg/genJets/T2ttDeg_mStop350_mChi330_4bodydec_dil/treeProducerSusySingleLepton/tree.root")
weight= 4000*0.0004174/t.GetEntries()


weight = 1
sampleDict= {
          'T2Deg': {'tree':t    , "weight":weight, 'color':31          ,'lineColor':1   , 'isSignal':1 , 'isData':0       }
            }





binFrac=(100,0,1)
binJetPt=(20,0,500)
binEffJetPt=(15,0,1000)


plotDict = {}
      

 
energyFractions= [('chHEF'   , 'Jet_chHEF'            ,1),
                  ('neHEF'   , 'Jet_neHEF'            ,1),
                  ('phEF'    , 'Jet_phEF'             ,1),
                  ('eEF'     , 'Jet_eEF'              ,1),
                  ('muEF'    , 'Jet_muEF'             ,1),
                  ('HFHEF'   , 'Jet_HFHEF'            ,1),
                  ('HFEMEF'  , 'Jet_HFEMEF'           ,1),
                  ('chEF'    , '(Jet_eEF+Jet_muEF)'   ,1),
                  ]

#for ef,efVar,color in energyFractions:
#  efName="Jet_%s"%ef
#  plotDict[efName]={'var':efVar,    "presel":"(1)" ,"cut":"(1)", "fillColor":1 ,"color":1 ,"lineWidth":1 , "bin":binFrac,  "title":efName    ,"xLabel":efName,     "yLabel":"",     "xLog":1, "yLog":0    }

jetVars         = [
                  ('GenJet_pt'   , 'GenJet_pt[0]'            ,ROOT.kRed),
                  ('Jet_pt'      , 'Jet_pt[0]'               ,1),
                  ]


for name,var,color in jetVars:
  plotDict[name]={'var':var,    "presel":"(1)" ,"cut":"(1)", "fillColor":1 ,"color":color ,"lineWidth":1 , "bin":binJetPt,  "title":name    ,"xLabel":name,     "yLabel":"",     "xLog":1, "yLog":0    }


#j['chef'] > 0.2 and j['neef']<0.7 and j['nhef']<0.7 and j['ceef'] < 0.5 and abs(j['eta']) < 2.4

jetIdCutList=[
      #["stCut"," (nLepGood[0]+met_pt > 200)"],
      ["noCut","(1)"],
      ["chef","Jet_chHEF[0] >0.2"],
      ["nhef","Jet_neHEF[0] < 0.7"],
      ["neef","Jet_phEF[0] < 0.7 "],
      ["ceef","(Jet_eEF[0]+Jet_muEF[0]) < 0.5"],
      ["jetEta","Jet_eta[0]<2.4"],
	]

jetIdCutFlow=makeCutFlowList(jetIdCutList)




effPlot2 = ROOT.TH1D("eff","eff",20,0,500)
effG = ROOT.TGraph()

#for ptRange in [""]:
#  tree=SampleDict['T2Deg']['tree']
#  cut = jetIdCutFlow[5][1]
#  tree.Draw("Jet_pt[0]",,"same")
from deltaR import *


deltaRString = lambda e1,p1,e2,p2: "sqrt( (%s - %s)^2 + (%s-%s)^2 )"%(e1,e2,p1,p2)
deltaRCutString = lambda e1,p1,e2,p2,deltaR: "("+deltaRString(e1,p1,e2,p2) + "<%s)"%deltaR 
jetDRCut=deltaRCutString("Jet_eta[0]","Jet_phi[0]","GenJet_eta[0]","GenJet_phi[0]","0.4")
jetDR=deltaRString("Jet_eta[0]","Jet_phi[0]","GenJet_eta[0]","GenJet_phi[0]")
def matchJets(recoJet,genJet,maxDeltaR):
  
  recoEta = tree.GetLeaf("Jet_eta").GetValue(0)  
  recoPhi = tree.GetLeaf("Jet_phi").GetValue(0)
  genEta = tree.GetLeaf("GenJet_eta").GetValue(0)
  genPhi = tree.GetLeaf("GenJet_phi").GetValue(0)

  if deltaR(recoEta,recoPhi,genEta,genPhi) < maxDeltaR:
    ret=True
  else: ret=False

  return ret  
  

maxDeltaR=0.4


nEvents=sampleDict['T2Deg']['tree'].GetEntries()
nEvents=25
num=             ROOT.TH1D("a","a",20,0,500) 
div=             ROOT.TH1D("b","b",20,0,500) 
allRecoJets=     ROOT.TH1D("c","c",20,0,500) 
matchedRecoJets= ROOT.TH1D("d","d",20,0,500) 
allGenJets=      ROOT.TH1D("e","e",20,0,500) 




ROOT.TH1F().Sumw2()




plots={}

for p in ["matchedRecoJets","allRecoJets","matchedGenJets","allGenJets","matchedRecoJetsISR","matchEff","ISREff"]:
  plots[p]=    ROOT.TH1D(p,p,*binJetPt)


test=0

cut="Jet_pt>0"
tree=sampleDict['T2Deg']['tree']
tree.Draw(">>eList", cut, 'goff')
eList = ROOT.gDirectory.Get('eList')
nEvents=eList.GetN()
if test==1:
  nEvents=100
matchJetList=[]
mjList=[]
for iEvt in range(nEvents):
  tree.GetEntry(eList.GetEntry(iEvt))
  nRecoJets= int(tree.GetLeaf("nJet").GetValue())
  nGenJets=  int(tree.GetLeaf("nGenJet").GetValue())

  matchJetList.append([])
  mjList.append([])
  genJets = [(tree.GetLeaf("GenJet_pt").GetValue(iGj),tree.GetLeaf("GenJet_eta").GetValue(iGj),tree.GetLeaf("GenJet_phi").GetValue(iGj)) for iGj in range(nGenJets) ]
  recoJets= [(tree.GetLeaf("Jet_pt").GetValue(iRj), tree.GetLeaf("Jet_eta").GetValue(iRj), tree.GetLeaf("Jet_phi").GetValue(iRj)      ) for iRj in range(nRecoJets) ]

  for iGj,gj in enumerate(genJets):
    plots['allGenJets'].Fill( gj[0] )
    mjList[iEvt].append([])
    for iRj,rj in enumerate(recoJets):
      dR=deltaR(rj[1],rj[2],gj[1],gj[2])
      ptPercDiff=abs((rj[0]-gj[0])/gj[0])
      if dR < maxDeltaR and ptPercDiff < 0.4:
        mjList[iEvt][iGj].append( (eList.GetEntry(iEvt),iGj,iRj) )  
        plots['matchedRecoJets'].Fill(rj[0])
        plots['matchedGenJets'].Fill(gj[0])

        chef=tree.GetLeaf("Jet_chHEF").GetValue(iRj)
        nhef=tree.GetLeaf("Jet_neHEF").GetValue(iRj)
        neef=tree.GetLeaf("Jet_phEF").GetValue(iRj)
        ceef=tree.GetLeaf("Jet_eEF").GetValue(iRj) +tree.GetLeaf("Jet_muEF").GetValue(iRj)

        if chef > 0.2 and nhef < 0.7 and neef < 0.7 and ceef <0.5 and rj[1] < 2.4:
          plots['matchedRecoJetsISR'].Fill(rj[0])

  if len(mjList[iEvt])>1:
    if len(mjList[iEvt][iGj]) >1:
      print iEvt,iGj




  #for iGj in range(nGenJets):
  #  genEta = tree.GetLeaf("GenJet_eta").GetValue(iGj)
  #  genPhi = tree.GetLeaf("GenJet_phi").GetValue(iGj)
  #  genJetPt=tree.GetLeaf("GenJet_pt").GetValue(iGj)

  #  matchJetList[iEvt].append([])
 
  #  for iRj in range(nRecoJets):
  #   recoEta = tree.GetLeaf("Jet_eta").GetValue(iRj) 
  #   recoPhi = tree.GetLeaf("Jet_phi").GetValue(iRj) 
  #   recoJetPt=tree.GetLeaf("Jet_pt").GetValue(iRj)  
  #    dR=deltaR(recoEta,recoPhi,genEta,genPhi)
  #    ptPercDiff=abs((genJetPt-recoJetPt)/genJetPt)

  #    matchJetList[iEvt][iGj].append( (eList.GetEntry(iEvt),iGj,iRj, dR, ptPercDiff, dR < maxDeltaR and ptPercDiff < 0.4 ))
  #    #if dR < maxDeltaR and ptPercDiff < 0.4:


  #allRecoJets.Fill(recoJetPt)
  #allGenJets.Fill(genJetPt)
  #print recoJetPt, genJetPt
  #print (recoEta,recoPhi,genEta,genPhi) , "DR:", deltaR(recoEta,recoPhi,genEta,genPhi)
    #print "MATCHED"
    #chef=tree.GetLeaf("Jet_chHEF").GetValue(0)
    #nhef=tree.GetLeaf("Jet_neHEF").GetValue(0)
    #neef=tree.GetLeaf("Jet_phEF").GetValue(0)
    #ceef=tree.GetLeaf("Jet_eEF").GetValue(0) +tree.GetLeaf("Jet_muEF").GetValue(0)

    ##print iEvt, chef, nhef, neef, ceef, genJetPt, recoJetPt, deltaR(recoEta,recoPhi,genEta,genPhi) <0.4

    #matchedRecoJets.Fill(recoJetPt)
    #div.Fill(genJetPt)
    #if chef > 0.2 and nhef < 0.7 and neef < 0.7 and ceef <0.5 and recoEta < 2.4:
    #  #print "GOOOOOOOOOOOOOOD"
    #  num.Fill(recoJetPt)

  #else:
    #print "not matched"


ROOT.gStyle.SetOptStat(0)
plots["matchEff"] = plots["matchedRecoJets"].Clone()
plots["matchEff"].Divide(plots["allGenJets"])
plots["matchEff"].SetLineColor(ROOT.kBlue)

plots["ISREff"] = plots["matchedRecoJetsISR"].Clone()
plots["ISREff"].Divide(plots["matchedGenJets"])
plots["ISREff"].SetLineColor(ROOT.kViolet)

plots["matchISREff"] = plots["matchedRecoJetsISR"].Clone()
plots["matchISREff"].Divide(plots["allGenJets"])
plots["matchISREff"].SetLineColor(ROOT.kRed)




g = ROOT.TGraph()
g.SetPoint(0,0,1)
g.SetPoint(1,1000,1)
g.SetLineWidth(2)

effPlot3.Draw()
g.Draw("lsame")







getPlots(sampleDict,plotDict,varList="GenJet_pt",cut=jetDRCut)
getPlots(sampleDict,plotDict,varList="Jet_pt",cut=jetDRCut+"&&"+jetIdCutFlow[5][1])
#getPlots(sampleDict,plotDict,varList="Jet_pt",cut=jetDRCut+"&&"+"((Jet_chHEF[0] >0.2) && (Jet_neHEF[0] < 0.7) && (Jet_phEF[0] < 0.7 ) && ((Jet_eEF[0]+Jet_muEF[0]) < 0.5)) ")
hist1=sampleDict['T2Deg']['plots']['Jet_pt']
hist2=sampleDict['T2Deg']['plots']['GenJet_pt']

effPlot = hist1.Clone()
effPlot.Divide(hist2)
effPlot.Draw("same")






