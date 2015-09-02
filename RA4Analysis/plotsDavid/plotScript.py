import ROOT
ROOT.gROOT.LoadMacro("../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()
from math import *
import os, copy, sys
from array import array
from random import randint

from Workspace.HEPHYPythonTools.helpers import *
from Workspace.HEPHYPythonTools.xsec import *
from Workspace.HEPHYPythonTools.user import *
from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_postProcessed import *
from Workspace.RA4Analysis.helpers import *
from draw_helpers import *
from eleID_helper import *

dPhiStr = "acos((leptonPt+met*cos(leptonPhi-metPhi))/sqrt(leptonPt**2+met**2+2*met*leptonPt*cos(leptonPhi-metPhi)))"

#Bkg chains 
allBkg=[
        {'name':'QCD',       'sample':      },
        {'name':'DY',        'sample':DY_25ns           },
        {'name':'TTV',       'sample':     },
        {'name':'single top', 'sample':singleTop_25ns   },
        {'name':'W+Jets',     'sample':WJetsHTToLNu_25ns},
        {'name':'tt+Jets',   'sample':TTJets_25ns       },
      ]

for bkg in allBkg:
  bkg['chain'] = getChain(bkg['sample'],histname='',treeName='tree')
  bkg['color'] = color(bkg['name'])
#  bkg['chain'].SetAlias('dPhi',dPhiStr)

#Data
#data=[
#     {'name':'DoubleMuon_Run2015B_17Jul2015', 'sample':DoubleMuon_Run2015B_17Jul2015, 'legendName':'Data', 'merge':'Data'},
#     {'name':'DoubleMuon_Run2015B_PromptReco', 'sample':DoubleMuon_Run2015B_PromptReco, 'legendName':'Data', 'merge':'Data'},
#     {'name':'DoubleEG_Run2015B_17Jul2015', 'sample':DoubleEG_Run2015B_17Jul2015, 'legendName':'Data', 'merge':'Data'},
#     {'name':'DoubleEG_Run2015B_PromptReco', 'sample':DoubleEG_Run2015B_PromptReco, 'legendName':'Data', 'merge':'Data'},
#]

#Signal chains
#allSignals=[
            #"SMS_T1tttt_2J_mGl1200_mLSP800",
            #"SMS_T1tttt_2J_mGl1500_mLSP100",
            #"SMS_T2tt_2J_mStop425_mLSP325",
            #"SMS_T2tt_2J_mStop500_mLSP325",
            #"SMS_T2tt_2J_mStop650_mLSP325",
            #"SMS_T2tt_2J_mStop850_mLSP100",
            #{'name':'T5q^{4} 1.2/1.0/0.8', 'sample':T5qqqqWW_mGo1200_mCh1000_mChi800[lepSel], 'weight':'weight', 'color':ROOT.kBlack},
            #{'name':'T5q^{4} 1.5/0.8/0.1',  'sample':T5qqqqWW_mGo1500_mCh800_mChi100[lepSel],  'weight':'weight', 'color':ROOT.kMagenta},
            #{'name':'T5q^{4} 1.0/0.8/0.7', 'sample':T5qqqqWW_mGo1000_mCh800_mChi700[lepSel], 'weight':'weight', 'color':ROOT.kBlue},
            #"T1ttbbWW_mGo1000_mCh725_mChi715",
            #"T1ttbbWW_mGo1000_mCh725_mChi720",
            #"T1ttbbWW_mGo1300_mCh300_mChi290",
            #"T1ttbbWW_mGo1300_mCh300_mChi295",
            #"T5ttttDeg_mGo1000_mStop300_mCh285_mChi280",
            #"T5ttttDeg_mGo1000_mStop300_mChi280",
            #"T5ttttDeg_mGo1300_mStop300_mCh285_mChi280",
            #"T5ttttDeg_mGo1300_mStop300_mChi280",
#]

for s in allSignals:
  s['chain'] = getChain(s['sample'],histname='')
  s['chain'].SetAlias('dPhi',dPhiStr)

#defining ht, st and njets for SR
streg = [(250,350),(350,450),(450,-1)]                         
htreg = [(500,750)]#,(750,1000),(1000,1250),(1250,-1)]
njreg = [(5,5),(6,-1),(6,7),(8,-1)]
btb = (0,0)
presel='singleMuonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80'
preprefix = 'singleMuonic_0b_ht750-1000_st350_nj6-7'
wwwDir = '/afs/hephy.at/user/d/dhandl/www/pngCMG2/'+lepSel+'/Phys14V3/'+preprefix+'/'

if not os.path.exists(wwwDir):
  os.makedirs(wwwDir)

#use small to check some changes faster
#small = True
small = 1 
if small == 1:
  streg = [(350,-1)]
  htreg = [(750,1000)]
  njreg = [(6,7)]
  btb   = (0,0)

allVariables = []

def getdPhiMetJet(c):
  jets = cmgGetJets(c,ptMin=30,etaMax=2.4)
  met = c.GetLeaf('met_pt').GetValue()
  metPhi = c.GetLeaf('met_phi').GetValue()
  JetPt = jets[0]['pt']
  JetPhi = jets[0]['phi']
#  dPhi = acos((met*JetPt*cos(metPhi-JetPhi))/(met*JetPt))
  dPhi = deltaPhi(metPhi,JetPhi)
  return dPhi

def gethtRatio(c):
  jets = cmgGetJets(c,ptMin=30,etaMax=2.4)
  ht = c.GetLeaf('htJet30j').GetValue()
  Jet0 = jets[0]['pt']
  Jet1 = jets[1]['pt']
  ratio = (ht-Jet0-Jet1)/(Jet0+Jet1)
  return ratio

def gethtRatio3(c):
  jets = cmgGetJets(c,ptMin=30,etaMax=2.4)
  ht = c.GetLeaf('htJet30j').GetValue()
  Jet0 = jets[0]['pt']
  Jet1 = jets[1]['pt']
  Jet2 = jets[2]['pt']
  ratio = (ht-Jet0-Jet1-Jet2)/(Jet0+Jet1+Jet2)
  return ratio

def getHTwithoutLeadSub(c):
  jets = cmgGetJets(c,ptMin=30,etaMax=2.4)
  ht = c.GetLeaf('htJet30j').GetValue()
  Jet0 = jets[0]['pt']
  Jet1 = jets[1]['pt']
  Jet2 = jets[2]['pt']
  ratio = (ht-Jet0-Jet1-Jet2)
  return ratio

def getJetSum3(c):
  jets = cmgGetJets(c,ptMin=30,etaMax=2.4)
  ht = c.GetLeaf('htJet30j').GetValue()
  Jet0 = jets[0]['pt']
  Jet1 = jets[1]['pt']
  Jet2 = jets[2]['pt']
  ratio = Jet0+Jet1+Jet2
  return ratio

def getJetRatio(c):
  jets = cmgGetJets(c,ptMin=30,etaMax=2.4)
  Jet0 = jets[0]['pt']
  Jet1 = jets[1]['pt']
  ratio = (Jet1)/(Jet0)
  return ratio

def getleadingJet(c):
  jets = cmgGetJets(c,ptMin=30,etaMax=2.4)
  Jet0 = jets[0]['pt']
  return Jet0

def getsecondJet(c):
  jets = cmgGetJets(c,ptMin=30,etaMax=2.4)
  Jet1 = jets[1]['pt']
  return Jet1

def getdPhiJetJet(c):
  jets = cmgGetJets(c,ptMin=30,etaMax=2.4)
  leadJetPt = jets[0]['pt']
  leadJetPhi = jets[0]['phi']
  subJetPt = jets[1]['pt']
  subJetPhi = jets[1]['phi']
#  dPhi = acos((met*JetPt*cos(metPhi-JetPhi))/(met*JetPt))
  dPhi = deltaPhi(subJetPhi,leadJetPhi)
  return dPhi

def getJetMagnitude(c):
  jets = cmgGetJets(c,ptMin=30,etaMax=2.4)
  leadJetPt = jets[0]['pt']
  subJetPt = jets[1]['pt']
  ht = c.GetLeaf('htJet30j').GetValue()
  nJ = c.GetLeaf('nJet30').GetValue()
  res = (ht)/(nJ)
  return res

def getStSig(c):
  met = c.GetLeaf('met_pt').GetValue()
  lepton = c.GetLeaf('leptonPt').GetValue()
  ht = c.GetLeaf('htJet30j').GetValue()
  nJ = c.GetLeaf('nJet30').GetValue()
  res = (met+lepton)/sqrt(ht)
  return res

def getFWMT2(c):
  jets = cmgGetJets(c,ptMin=30,etaMax=2.4)
  rd = foxWolframMoments(jets)
  return rd['FWMT2']

def getFWMT4(c):
  jets = cmgGetJets(c,ptMin=30,etaMax=2.4)
  rd = foxWolframMoments(jets)
  return rd['FWMT4']

def getCirc2D(c):
  jets = cmgGetJets(c,ptMin=30,etaMax=2.4)
  rd = circularity2D(jets)
  return rd['c2D']

def getlinCirc2D(c):
  jets = cmgGetJets(c,ptMin=30,etaMax=2.4)
  rd = circularity2D(jets)
  return rd['linC2D']

met = {'name':'mymet', 'varString':"met_pt", 'legendName':'#slash{E}_{T}', 'Ytitle':'# of Events / 25GeV', 'binning':[64,0,1600]}
ht = {'name':'myht', 'varString':"htJet30j", 'legendName':'H_{T}', 'Ytitle':'# of Events / 25GeV', 'binning':[64,0,1600]}
St = {'name':'myst', 'varString':"st", 'legendName':'S_{T}', 'Ytitle':'# of Events / 25GeV', 'binning':[64,0,1600]}
#isoTrack = {'name':'myisoTrack', 'legendName':'isoTrack', 'binning':[10,0,10]}
#relIso = {'name':'myrelIso', 'legendName':'relIso', 'binning':[100,0,1.0]}
nJets = {'name':'mynJets', 'varString':'nJet30', 'legendName':'Jets', 'Ytitle':'# of Events', 'binning':[17,-0.5,16.5]}
#nBJets = {'name':'mynBJets', 'varString':'nBJetMediumCMVA30', 'legendName':'B Jets', 'Ytitle':'# of Events', 'binning':[17,-0.5,16.5]}
dPhi = {'name':'mydeltaPhi', 'varFunc':cmgDPhi, 'legendName':'#Delta#Phi(W,l)','binning':[20,0,pi], 'Ytitle':'# of Events'}#, 'binningIsExplicit':True} 
lMomentum = {'name':'myleptonPt', 'varString':'leptonPt', 'legendName':'p_{T}(l)', 'Ytitle':'# of Events / 25GeV', 'binning':[40,0,1000]}
htratio = {'name':'myhtratio', 'varFunc':gethtRatio, 'legendName':'#frac{H_{T,j>2}}{j_{1}+j_{2}}', 'Ytitle':'# of Events', 'binning':[25,0,2.5]}
htratio3 = {'name':'myhtratio3', 'varFunc':gethtRatio3, 'legendName':'#frac{H_{T,j>3}}{j_{1}+j_{2}+j_{3}}', 'Ytitle':'# of Events', 'binning':[25,0,2.5]}
ht3 = {'name':'myHTwithout3j', 'varFunc':getHTwithoutLeadSub, 'legendName':'H_{T,j>3}', 'Ytitle':'# of Events', 'binning':[60,0,1500]}
jetsum3 = {'name':'myjetsum3', 'varFunc':getJetSum3, 'legendName':'j_{1}+j_{2}+j_{3}', 'Ytitle':'# of Events', 'binning':[64,0,1600]}
jetratio = {'name':'myjetratio', 'varFunc':getJetRatio, 'legendName':'2^{nd}Jet/1^{st}Jet', 'Ytitle':'# of Events', 'binning':[15,0,1.5]}
mt = {'name':'mymt', 'varFunc':cmgMT, 'legendName':'M_{T}', 'Ytitle':'# of Events / 10GeV', 'binning':[35,0,350]}
MT2W = {'name':'mymt2w', 'varString':'mt2w', 'legendName':'M^{W}_{T2}', 'Ytitle':'# of Events / 10GeV', 'binning':[45,0,450]}
dphimetjet = {'name':'mydPhimetjet', 'varFunc':getdPhiMetJet, 'legendName':'#Delta#Phi(#slash{E}_{T},J_{1})', 'Ytitle':'# of Events', 'binning':[20,0,pi]}#, 'binningIsExplicit':True}
leadingJet = {'name':'myleadingJet', 'varFunc':getleadingJet, 'legendName':'p_{T}(leading Jet)', 'Ytitle':'# of Events / 50GeV', 'binning':[32,0,1600]}
secondJet = {'name':'mysecondJet', 'varFunc':getsecondJet, 'legendName':'p_{T}(J_{2})', 'Ytitle':'# of Events / 50GeV', 'binning':[32,0,1600]}
htOppRatio = {'name':'myhtOppRatio', 'varFunc':cmgHTRatio, 'legendName':'H^{opp. to #slash{E}_{T}}_{T}/H_{T}', 'Ytitle':'# of Events', 'binning':[20,0,1]}
#minDPhiMetJettwo = {'name':'myminDPhiMetJet12', 'varFunc':cmgMinDPhiJet, 'legendName':'min #Delta#Phi(#slash{E}_{T},J_{1,2})', 'Ytitle':'# of Events', 'binning':[20,0,pi]}#, 'binningIsExplicit':True}
minDPhiMetJetthree = {'name':'myminDPhiMetJet123', 'varFunc':cmgMinDPhiJet, 'legendName':'min #Delta#Phi(#slash{E}_{T},J_{1,2,3})', 'Ytitle':'# of Events', 'binning':[20,0,pi]}#, 'binningIsExplicit':True}
MTclosestJetMet = {'name':'myMTClosestJetMET', 'varFunc':cmgMTClosestJetMET, 'legendName':'M_{T} (closest Jet,#slash{E}_{T})', 'Ytitle':'# of Events / 10GeV', 'binning':[35,0,350]}
dphijetjet = {'name':'mydPhijetjet', 'varFunc':getdPhiJetJet, 'legendName':'#Delta#Phi(J_{1},J_{0})', 'Ytitle':'# of Events', 'binning':[20,0,pi]}#, 'binningIsExplicit':True}
jetMag = {'name':'myjetmag', 'varFunc':getJetMagnitude, 'legendName':'#frac{H_{T}}{nJets}', 'Ytitle':'# of Events', 'binning':[50,0,500]}
mht = {'name':'mymht', 'varFunc':missingHT, 'legendName':'#slash{H}_{T}', 'Ytitle':'# of Events / 25GeV', 'binning':[40,0,1000]}
dphimhtmet = {'name':'mydphimhtmet', 'varFunc':dPhiMHTMET, 'legendName':'#Delta#Phi(#slash{H}_{T},#slash{E}_{T})', 'Ytitle':'# of Events', 'binning':[20,0,pi]}
stSig = {'name':'mystsig', 'varFunc':getStSig, 'legendName':'#frac{S_{T}}{#sqrt{H_{T}}}', 'Ytitle':'# of Events', 'binning':[40,0,40]}
thrust = {'name':'mythrust', 'varFunc':calcThrust, 'legendName':'T', 'Ytitle':'# of Events ', 'binning':[20,0.5,1]}
circ = {'name':'mycirc', 'varFunc':getCirc2D, 'legendName':'C', 'Ytitle':'# of Events ', 'binning':[40,0,1]}
lincirc = {'name':'mylincirc', 'varFunc':getlinCirc2D, 'legendName':'lin. C', 'Ytitle':'# of Events ', 'binning':[40,0,1]}
fwmt2 = {'name':'myfwmt2', 'varFunc':getFWMT2, 'legendName':'FWMT2', 'Ytitle':'# of Events ', 'binning':[40,0,1]}
fwmt4 = {'name':'myfwmt4', 'varFunc':getFWMT4, 'legendName':'FWMT4', 'Ytitle':'# of Events ', 'binning':[40,0,1]}

allVariables.append(met)
allVariables.append(ht)
allVariables.append(St)
#allVariables.append(isoTrack)
#allVariables.append(relIso)
#allVariables.append(nBJets)
allVariables.append(dPhi)
allVariables.append(nJets)
allVariables.append(lMomentum)
allVariables.append(htratio)
allVariables.append(htratio3)
allVariables.append(ht3)
allVariables.append(jetsum3)
allVariables.append(jetratio)
allVariables.append(mt)
#allVariables.append(MT2W)
allVariables.append(dphimetjet)
allVariables.append(leadingJet)
allVariables.append(secondJet)
allVariables.append(htOppRatio)
#allVariables.append(minDPhiMetJettwo)
allVariables.append(minDPhiMetJetthree)
allVariables.append(MTclosestJetMet)
allVariables.append(dphijetjet)
allVariables.append(jetMag)
#allVariables.append(mht)
#allVariables.append(dphimhtmet)
#allVariables.append(stSig)
allVariables.append(thrust)
allVariables.append(circ)
allVariables.append(lincirc)
allVariables.append(fwmt2)
allVariables.append(fwmt4)

histos = {}
h_ratio = {}

for i_htb, htb in enumerate(htreg):
  for stb in streg:
    for srNJet in njreg:
      print 'Var region => ht: ',htb,'st: ',stb #'NJet: ',srNJet
      for sig in allSignals:            
        h_ratio[sig['name']] = {}     
      for sample in allBkg + allSignals: #Loop over samples
        histos[sample['name']] = {}



        for var in allVariables:
          if var.has_key('binningIsExplicit') and var['binningIsExplicit']:
            histos[sample['name']][var['name']] = ROOT.TH1F(sample['name']+'_'+var['name'], sample['name']+'_'+var['name'], len(var['binning'])-1, array('d', var['binning']))
          else:
            histos[sample['name']][var['name']] = ROOT.TH1F(sample['name']+'_'+var['name'], sample['name']+'_'+var['name'], *var['binning'])
          histos[sample['name']][var['name']].Reset()
          #sample['chain'].Draw("Sum$(isoTrack_pt<15&&abs(isoTrack_pdgId)==211&&abs(isoTrack_dz)<0.05)"+">>"+sample["name"]+"_"+var["name"])
          #sample['chain'].Draw(var['varString']+">>"+sample['name']+'_'+var['name'], sample["weight"]+"*("+cut+")")
          
        namestr, cut = nameAndCut(stb, htb, srNJet, btb=btb, presel=presel, btagVar = 'nBJetMediumCMVA30')
        print cut
        
        if sample.has_key('addcut'):
          if type(sample['addcut'])==type(''):
            cut = cut + sample["addcut"]
  
        sample["chain"].Draw(">>eList",cut) #Get the event list 'eList' which has all the events satisfying the cut
        elist = ROOT.gDirectory.Get("eList")
        number_events = elist.GetN()
        print "Sample ",sample["name"],": Will loop over", number_events,"events" #Number of events satisfying the cut
        
        #Event loop
        for i in range(number_events): #Loop over those events
          sample["chain"].GetEntry(elist.GetEntry(i))  #Set the chain to the current event (it's the i-th event of the eList). This is the central line in this file!
          for var in allVariables:
            assert (var.has_key('varString') or var.has_key('varFunc')), "Error: Did not specify 'varString' or 'varFunc' for var %s" % repr(var)
            assert not (var.has_key('varString') and var.has_key('varFunc')), "Error: Specified both 'varString' and 'varFunc' for var %s" % repr(var)
            #if var['name'] == 'myminDPhiMetJet12':
            #  varValue = getVarValue(sample["chain_soft"], var['varString']) if var.has_key('varString') else var['varFunc'](sample["chain_soft"],nJets=2)
            #else:
            varValue = getVarValue(sample["chain"], var['varString']) if var.has_key('varString') else var['varFunc'](sample["chain"])
#            if var == dPhi:
#              #WPhi = getWPhi(sample['chain'])
#              #lPhi = getVarValue(sample['chain'],'leptonPhi')
#              #varValue = deltaPhi(WPhi,lPhi)
#              varValue = getdPhi(sample['chain_soft'])
#             # print 'WPhi: ',WPhi,' lPhi: ',lPhi,'deltaPhi: ',varValue
#            if var == htratio:
#              varValue = gethtRatio(sample['chain_soft'])
#            else:
#              varValue = getVarValue(sample["chain_soft"], var['varString'])   #Get the value of the variable
            weight = 1
            if sample.has_key('weight'):
              if type(sample['weight'])==type(''):
                weight = getVarValue(sample['chain'], sample['weight'])
              else:
                weight = sample['weight']
            histos[sample['name']][var['name']].Fill(varValue, weight)
        del elist
        
        #for sample in signals:
        #  for var in allVariables:
        #    if histos[sample['name']][var['name']].Integral()>0:
        #      histos[sample['name']][var['name']].Scale(histos['TTJets'][var['name']].Integral()/histos[sample['name']][var['name']].Integral())
        
        #Define and stack the histograms...
      for var in allVariables:
        canvas = ROOT.TCanvas(var['name']+' Window',var['name']+' Window')
        pad1 = ROOT.TPad(var['name']+' Pad',var['name']+' Pad',0.,0.0,1.,1.)
        #pad1.SetBottomMargin(0)
        pad1.SetLogy()
        pad1.Draw()
        pad1.cd()
        l = ROOT.TLegend(0.65,0.75,0.95,0.95)
        l.SetFillColor(0)
        l.SetBorderSize(1)
        l.SetShadowColor(ROOT.kWhite)
        stack = ROOT.THStack('stack','Stacked Histograms')
       
#        lines = [{'pos':(0.15, 0.95),'text':'CMS Simulation',        'options':{'size':0.045}},\
#                 {'pos':(0.7, 0.95), 'text':'L=4fb{}^{-1} (13 TeV)', 'options':{'size':0.045}}]
        text = ROOT.TLatex()
        text.SetNDC()
        text.SetTextSize(0.045)
        text.SetTextAlign(11) 

        for sample in allBkg:
          histos[sample['name']][var['name']].SetLineColor(ROOT.kBlack)
          histos[sample['name']][var['name']].SetFillColor(sample['color'])
          histos[sample['name']][var['name']].SetMarkerStyle(0)
          histos[sample['name']][var['name']].GetXaxis().SetTitle(var['legendName'])
          histos[sample['name']][var['name']].GetYaxis().SetTitle(var['Ytitle'])# / '+ str( (var['binning'][2] - var['binning'][1])/var['binning'][0])+'GeV')
          histos[sample['name']][var['name']].GetXaxis().SetLabelSize(0.04)
          histos[sample['name']][var['name']].GetYaxis().SetLabelSize(0.04)
          stack.Add(histos[sample['name']][var['name']])
          l.AddEntry(histos[sample['name']][var['name']], sample['name'],'f')
       
        stack.Draw()
        stack.GetXaxis().SetTitle(var['legendName'])
        stack.GetYaxis().SetTitle(var['Ytitle'])# / '+ str( (var['binning'][2] - var['binning'][1])/var['binning'][0])+'GeV')
        stack.SetMinimum(10**(-2))
        stack.SetMaximum(100*stack.GetMaximum())
 
        #for extra in extraSamples:
        #  histos[extra['name']][var['name']].SetMarkerStyle(21)
        #  histos[extra['name']][var['name']].Draw('same E')
        #  l.AddEntry(histos[extra['name']][var['name']],extra['name'])
       
        for sig in allSignals:
          histos[sig['name']][var['name']].SetLineColor(sig['color'])
          histos[sig['name']][var['name']].SetLineWidth(2)
          histos[sig['name']][var['name']].SetFillColor(0)
          histos[sig['name']][var['name']].SetMarkerStyle(0)
          histos[sig['name']][var['name']].Draw('same')
          l.AddEntry(histos[sig['name']][var['name']], sig['name'])
       
        l.Draw()

#        for line in lines:
#          text.SetTextSize(0.04)
#          try:
#            text.SetTextSize(line['options']['size'])
#          except:pass
#          text.DrawLatex(line['pos'][0],line['pos'][1],line['text'])
        text.DrawLatex(0.15,.96,"CMS Simulation")
        text.DrawLatex(0.65,0.96,"L=4 fb^{-1} (13 TeV)")
        
#        canvas.cd()
#        pad2 = ROOT.TPad(var['name']+" Ratio",var['name']+" Ratio",0.,0.,1.,0.3)
#        pad2.SetTopMargin(0)
#        pad2.SetBottomMargin(0.3)
#        pad2.Draw()
#        pad2.cd()
#        
#        if var.has_key('binningIsExplicit') and var['binningIsExplicit']:
#          histo_merge = ROOT.TH1F(var['name']+" Ratio",var['name']+" Ratio", len(var['binning'])-1, array('d', var['binning']))
#        else:
#          histo_merge = ROOT.TH1F(var['name']+" Ratio",var['name']+" Ratio", *var['binning'])
#        histo_merge.Merge(stack.GetHists())
#
#        for sig in allSignals:
#          h_ratio[sig['name']][var['name']] = histos[sig['name']][var['name']].Clone()
#          h_ratio[sig['name']][var['name']].SetLineColor(sig['color'])
#          h_ratio[sig['name']][var['name']].SetLineWidth(2)
#        # h_ratio[sig['name']][var['name']].SetMinimum(0.0)
#       #  h_ratio[sig['name']][var['name']].SetMaximum(0.02)
#          h_ratio[sig['name']][var['name']].Sumw2()
#          h_ratio[sig['name']][var['name']].SetStats(0)
#          h_ratio[sig['name']][var['name']].Divide(histo_merge)
#          h_ratio[sig['name']][var['name']].SetMarkerStyle(21)
#          h_ratio[sig['name']][var['name']].Draw("ep")
#          h_ratio[sig['name']][var['name']].GetXaxis().SetTitle(var['legendName'])
#          h_ratio[sig['name']][var['name']].GetYaxis().SetTitle("Signal/Bkg")
#          h_ratio[sig['name']][var['name']].GetYaxis().SetNdivisions(505)
#          h_ratio[sig['name']][var['name']].GetYaxis().SetTitleSize(23)
#          h_ratio[sig['name']][var['name']].GetYaxis().SetTitleFont(43)
#          h_ratio[sig['name']][var['name']].GetYaxis().SetTitleOffset(1.8)
#          h_ratio[sig['name']][var['name']].GetYaxis().SetLabelFont(43)
#          h_ratio[sig['name']][var['name']].GetYaxis().SetLabelSize(20)
#          h_ratio[sig['name']][var['name']].GetYaxis().SetLabelOffset(0.015)
#        #  h_ratio[sig['name']][var['name']].GetXaxis().SetNdivisions(510)
#          h_ratio[sig['name']][var['name']].GetXaxis().SetTitleSize(23)
#          h_ratio[sig['name']][var['name']].GetXaxis().SetTitleFont(43)
#          h_ratio[sig['name']][var['name']].GetXaxis().SetTitleOffset(3.4)
#          h_ratio[sig['name']][var['name']].GetXaxis().SetLabelFont(43)
#          h_ratio[sig['name']][var['name']].GetXaxis().SetLabelSize(20)
#          h_ratio[sig['name']][var['name']].GetXaxis().SetLabelOffset(0.04)
          
          #h_ratio2 = histos['T5Full_1500_800_100'][var['name']].Clone('h_ratio2')
          #h_ratio2.SetLineColor(signal1500['color'])
          #h_ratio2.SetLineWidth(2)
          #h_ratio2.Sumw2()
          #h_ratio2.SetStats(0)
          #h_ratio2.Divide(histo_merge)
          #h_ratio2.SetMarkerStyle(21)
          #h_ratio2.SetMarkerColor(ROOT.kBlue+2)
          #h_ratio2.Draw("same")
         
        canvas.cd()
        canvas.Print(wwwDir+namestr+'_'+var['name']+'.png')
        canvas.Print(wwwDir+namestr+'_'+var['name']+'.root')
        canvas.Print(wwwDir+namestr+'_'+var['name']+'.pdf')

