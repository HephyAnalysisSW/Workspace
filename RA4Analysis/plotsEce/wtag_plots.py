import ROOT
from Workspace.RA4Analysis.makeCompPlotDilep import DrawClosure
from math import sqrt, cos, sin, atan2, acos, pi
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName,nBTagBinName,varBinName, cmgMTClosestJetMET, cmgMTClosestBJetMET,  cmgMinDPhiJet, cmgMinDPhiBJet , cmgMTTopClosestJetMET , cmgHTOrthMET
from Workspace.RA4Analysis.cmgObjectSelection import get_cmg_genPartsAll,get_cmg_genParts, get_cmg_fatJets, get_cmg_jets, get_cmg_index_and_DR, get_cmg_genLeps, get_cmg_recoMuons
from Workspace.RA4Analysis.objectSelection import getGoodJetsStage2,gTauAbsEtaBins, gTauPtBins, metParRatioBins, jetRatioBins
from Workspace.HEPHYPythonTools.helpers import findClosestObject, deltaR,getVarValue, getObjFromFile
from Workspace.RA4Analysis.objectSelection import getGenLepsWithMatchInfo,getGenLeps, getMuons, getLooseMuStage2, getGenLep
from Workspace.RA4Analysis.cmgTuplesPostProcessed_v2_Phys14V3_HT400ST200 import *
from Workspace.RA4Analysis.helpers import deltaPhi
ROOT.gROOT.Reset()
ROOT.gROOT.LoadMacro("/afs/hephy.at/scratch/e/easilar/newWorkDir/CMSSW_7_2_3/src/Workspace/HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()

#ROOT.TH1F.SetDefaultSumw2()
lepSel = 'hard'
#sample = getChain(WJetsHTToLNu[lepSel],histname='')
#sample = getChain(T5qqqqWW_mGo1500_mCh800_mChi100[lepSel],histname='')
#sample = getChain(ttJets[lepSel],histname='')
#sample_name = "T5qqqqWW_mGo1500_mCh800_mLSP100"
#sample_name = "TTJets"
#sample_name = "WJets"
#c = sample
samples = [
{'flag':'bkg','cname':'QCD'      ,                        'label':'QCD'           ,                      'color':ROOT.kCyan-6  ,'chain':getChain(QCD[lepSel],histname='')         },\
{'flag':'bkg','cname':'TTVH'     ,                        'label':'t#bar{t}+W/Z/H',                      'color':ROOT.kOrange-3  ,'chain':getChain(TTVH[lepSel],histname='')        },\
{'flag':'bkg','cname':'DY'       ,                        'label':'DY+Jets'       ,                      'color':ROOT.kRed-6 ,'chain':getChain(DY[lepSel],histname='')          },\
{'flag':'bkg','cname':'singleTop',                        'label':'single top'    ,                      'color':ROOT.kViolet+5,'chain':getChain(singleTop[lepSel],histname='')   },\
{'flag':'bkg','cname':'WJets'    ,                        'label':'W+Jets'        ,                      'color':ROOT.kGreen-2 ,'chain':getChain(WJetsHTToLNu[lepSel],histname='')},\
{'flag':'bkg','cname':'TTJets'   ,                        'label':'t#bar{t}+Jets' ,                      'color':ROOT.kBlue-2 ,'chain':getChain(ttJets[lepSel],histname='')      },\
{'flag':'sig','cname':'T5qqqqWW_mGo1000_mCh800_mLSP700',  'label':'T5qqqqWW_mGo1000_mCh800_mLSP700'  ,   'color':ROOT.kBlack  ,'chain':getChain(T5qqqqWW_mGo1000_mCh800_mChi700[lepSel],histname='')},\
{'flag':'sig','cname':'T5qqqqWW_mGo1200_mCh1000_mLSP800', 'label':'T5qqqqWW_mGo1200_mCh1000_mLSP800' ,   'color':ROOT.kRed    ,'chain':getChain(T5qqqqWW_mGo1200_mCh1000_mChi800[lepSel],histname='')},\
{'flag':'sig','cname':'T5qqqqWW_mGo1500_mCh800_mLSP100',  'label':'T5qqqqWW_mGo1500_mCh800_mLSP100'  ,   'color':ROOT.kYellow    ,'chain':getChain(T5qqqqWW_mGo1500_mCh800_mChi100[lepSel],histname='')},\
{'flag':'sig','cname':'SMS_T1tttt_2J_mGl1500_mLSP100','color':ROOT.kMagenta    ,'chain':getChain(SMS_T1tttt_2J_mGl1500_mLSP100[lepSel],histname='')},\
{'flag':'sig','cname':'SMS_T1tttt_2J_mGl1200_mLSP800','color':ROOT.kCyan       ,'chain':getChain(SMS_T1tttt_2J_mGl1200_mLSP800[lepSel],histname='')},\
]

#plot = {'name':'hadMatchedprunedmass'}
#plot = {'name':'hadMatchedtau2_tau1'}
plot = {'name':'hadMatchednwtagged'}
#plot = {'name':'ptGenWhadGenPartAll'}
#plot = {'name':'deltaRvsPt'}


small = False
maxN = 10000


def findDaughters(genParts,index):
  w = genParts[index]
  #print "PdgID:" , w['pdgId']  
  dau = []
  for g in genParts:
    if g['motherId'] == w['pdgId'] and g['pdgId']!=w['pdgId']:
      if abs(g['pdgId'])>=1 and abs(g['pdgId'])<=6  :
       dau.append(g)
  return dau

import itertools
from itertools import *

def findRealDaus(daus , w):
  p = []
  trash = []
  for p1,p2 in list(combinations(daus, 2)):
    px = (p1['pt']*cos(p1['phi'])+p2['pt']*cos(p2['phi']))
    py = (p1['pt']*sin(p1['phi'])+p2['pt']*sin(p2['phi']))
    pt = sqrt(px**2+py**2) 
    if abs(pt-w['pt'])/w['pt'] < 0.000001:  
    #if pt == w['pt']:  
      p.append(p1)
      p.append(p2)
    else :
      trash.append(p1) 
      trash.append(p2) 
  return p


htCut = [500,10000000000]
#stCut = [250,350]
stCut = [200,10000000000]
njetCut = [6,20]
nbtagCut = 0
mt2Cut = 0
jetPtCut = 80
dfCut =1


prepresel = 'singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&'

#presel = prepresel+'deltaPhi_Wl>'+str(dfCut)+'&&Jet_pt[1]>='+str(jetPtCut)+'&&htJet30j>='+str(htCut[0])+'&&htJet30j<'+str(htCut[1])+'&&st>='+str(stCut[0])+'&&st<'+str(stCut[1])+'&&nJet30>='+str(njetCut[0])+'&&nJet30<'+str(njetCut[1])+'&&nBJetMediumCMVA30=='+str(nbtagCut)
presel = ""
path = '/afs/hephy.at/user/e/easilar/www/PHYS14v3/fatJet/Wtagging/tests/'
if not os.path.exists(path):
  os.makedirs(path)


#mass = ROOT.TH1F('mass', 'pruned mass',50,0,500)
can = ROOT.TCanvas('mass','mass',600,600)
can.cd()
latex = ROOT.TLatex()
latex.SetNDC()
latex.SetTextSize(0.035)
latex.SetTextAlign(11)
leg = ROOT.TLegend(0.5,0.75,0.95,0.95)
h_Stack = ROOT.THStack('h_Stack','mass')
h_Stack_S = ROOT.THStack('h_Stack_S','h_Stack_S')

for b in samples:
  color = b['color']
  print color
  print b['cname']  , b['chain']
  histo = 'h_'+b['cname']
  chain = b['chain']
  histoname = histo
  print histoname
  #histo = ROOT.TH1F(str(histo) ,str(histo),p['bin'],p['lowlimit'],p['limit'])
  #print presel
  #histo = ROOT.TH1F('histo', 'pruned mass',50,0,500)
  #histo = ROOT.TH1F('histo', 'gen W Pt',50,0,2000)
  #histo = ROOT.TH1F('histo', 'DeltaR',50,0,5)
  #histo = ROOT.TH1F('histo', 'tau2/tau1',50,0,1)
  histo = ROOT.TH1F('histo', 'nWtagged',6,0,6)
  c = chain
  c.Draw(">>eList",presel)
  eList = ROOT.gDirectory.Get("eList")
  number_events = eList.GetN()
  #number_events = c.GetEntries()
  if small:
    if number_events>maxN:
      number_events=maxN

  number_events=min(number_events, eList.GetN())
  counter = 0   ## count number of w tagged
  nwtagged = counter 
  for i in range(number_events):
    if (i%10000 == 0) and i>0 :
      print i,"/",number_events
    c.GetEntry(eList.GetEntry(i))
    weight = c.GetLeaf('weight').GetValue()
    run =  c.GetLeaf('run').GetValue()
    lumi =  c.GetLeaf('lumi').GetValue()
    evt =  c.GetLeaf('evt').GetValue()
    xsec =  c.GetLeaf('xsec').GetValue()
    print "NEW EVENT:" , "Run" , run ,"Lumi" ,lumi ,"xsec" ,xsec ,"evt" , evt 
    fatJets = get_cmg_fatJets(c)
    if b['flag'] == 'bkg' : genParts = get_cmg_genParts(c)
    if b['flag'] == 'sig' : genParts = get_cmg_genPartsAll(c)
    #genParts = get_cmg_genParts(c)
    for g in range(len(genParts)):   ##loop over gen parts
      genPart = genParts[g]
      if abs(genPart['pdgId'])==24:  ## take gen W
        print "GenPart (The W):" , genPart
        #histo.Fill(genPart['pt'],weight)
        idaus = findDaughters(genParts,g)
        print "initial daus", idaus
        if idaus:
          daus = findRealDaus(idaus,genPart) 
          if daus:
            print "real daus:" , daus
            assert len(daus) == 2
            gInd , gDR = get_cmg_index_and_DR(fatJets,genPart['phi'],genPart['eta'])
            if gInd>=0 and  gDR<0.4 :    ##find a matched fat jet to this W
              fatJet = fatJets[gInd] ##matched fat Jet 
              if fatJet['prunedMass']>60 and fatJet['prunedMass']<100 and (fatJet['tau2']/fatJet['tau1'])<0.5 : 
                nwtagged = counter + 1 ##matched and w tagged jets found  
              else : nwtagged = counter
              #histo.Fill(fatJet['prunedMass'],weight)
              #if fatJet['tau1']!=0 : histo.Fill(fatJet['tau2']/fatJet['tau1'],weight)
              #continue
    #print "nWtagged" , nwtagged 
    histo.Fill(nwtagged , weight)  ##fill n W tagged in this event
  histo.SetMinimum(.001)
  #histo.GetXaxis().SetTitle('W matched Jet prunedmass')
  histo.GetXaxis().SetTitle('n W tagged')
  histo.GetYaxis().SetTitle('Events')
  if b['flag'] == 'bkg' :
    histo.SetFillColor(color)
    #histo.SetLineColor(color)
    histo.SetLineWidth(2)
    h_Stack.Add(histo)
  if b['flag'] == 'sig' : 
    histo.SetLineColor(color)
    histo.SetLineWidth(4)
    h_Stack_S.Add(histo)
  leg.AddEntry(histo, b['label'],"f")

h_Stack.SetMaximum((h_Stack.GetMaximum())*5)
h_Stack.SetMinimum(0.001)
h_Stack.Draw()
h_Stack_S.Draw('noStacksame')
leg.SetFillColor(0)
leg.Draw()
latex.DrawLatex(0.16,0.96,"CMS Simulation")
latex.DrawLatex(0.71,0.96,"L=4 fb^{-1} (13 TeV)")
#latex.DrawLatex(0.5,0.05,'W matched Jet prunedmass')
can.SetLogy()
#can.Update()
can.SaveAs(path+plot['name']+'.png')
can.SaveAs(path+plot['name']+'.pdf')
can.SaveAs(path+plot['name']+'.root')
del can
#can = ROOT.TCanvas("c","Eff",800,800)
#can.cd()
#latex = ROOT.TLatex()
#latex.SetNDC()
#latex.SetTextSize(0.035)
#latex.SetTextAlign(11)
##mass.SetAxisRange(0, 1.0,"Y")
#mass.SetMinimum(0.001)
#mass.SetLineColor(ROOT.kBlack)
#mass.GetYaxis().SetTitle("Events")
#mass.GetXaxis().SetTitle("tagged Jet pruned mass")
#mass.Draw()
#
#latex.DrawLatex(0.16,0.96,"CMS Simulation")
#latex.DrawLatex(0.71,0.96,"L=4 fb^{-1} (13 TeV)")
#latex.DrawLatex(0.5,0.8,sample_name)
#
#can.SetLogy()
#can.SaveAs(path+"/wtag_with04_prunedmass"+"_"+sample_name+".png")
#can.SaveAs(path+"/wtag_with04_prunedmass"+"_"+sample_name+".root")
#can.SaveAs(path+"/wtag_with04_prunedmass"+"_"+sample_name+".pdf")
#
#print "Written",  path
