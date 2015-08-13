import ROOT
ROOT.gROOT.LoadMacro("../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()
from math import *
import os, copy, sys
from array import array
from random import randint

from Workspace.HEPHYPythonTools.helpers import *
from Workspace.HEPHYPythonTools.xsec import *
from Workspace.RA4Analysis.cmgTuples_v1_PHYS14V3 import *
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v8_Phys14V3_HT400ST200 import *
from Workspace.RA4Analysis.helpers import *
from draw_helpers import *
from eleID_helper import *
from localInfo import username

#lepSel = 'hard'
#dPhiStr = "acos((leptonPt+met*cos(leptonPhi-metPhi))/sqrt(leptonPt**2+met**2+2*met*leptonPt*cos(leptonPhi-metPhi)))"
#small = True
small = False

target_lumi = 3000 #pb-1
def getWeight(sample,nEvents,target_lumi):
  weight = xsec[sample['dbsName']] * target_lumi/nEvents
  return weight

#Bkg chains 
allBkg=[
       {'name':'ttJets_PU20bx25', 'sample':ttJets_PU20bx25, 'legendName':'t#bar{t}+Jets', 'color':ROOT.kBlue-2, 'merge':'ttbar'},
       {'name':'DYJetsToLL_M50_HT100to200_PU20bx25', 'sample':DYJetsToLL_M50_HT100to200_PU20bx25, 'legendName':'DY HT100-200', 'color':ROOT.kRed-6, 'merge':'DY'},
       {'name':'DYJetsToLL_M50_HT200to400_PU20bx25', 'sample':DYJetsToLL_M50_HT200to400_PU20bx25, 'legendName':'DY HT200-400', 'color':ROOT.kRed-6, 'merge':'DY'},
       {'name':'DYJetsToLL_M50_HT400to600_PU20bx25', 'sample':DYJetsToLL_M50_HT400to600_PU20bx25, 'legendName':'DY HT400-600', 'color':ROOT.kRed-6, 'merge':'DY'},
       {'name':'DYJetsToLL_M50_HT600toInf_PU20bx25', 'sample':DYJetsToLL_M50_HT600toInf_PU20bx25, 'legendName':'DY HT600-Inf', 'color':ROOT.kRed-6, 'merge':'DY'},
]

maxN=1 if small else -1

for sample in allBkg:
  sample['chunks'], sample['nEvents'] = getChunks(sample['sample'],treeName='treeProducerSusySingleLepton', maxN=maxN)
  sample['chain'] = ROOT.TChain('tree')
  for chunk in sample['chunks']:
    sample['chain'].Add(chunk['file'])

  sample['weight'] = getWeight(sample['sample'], sample['nEvents'], target_lumi)

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

#for s in allSignals:
  #s['chain'] = getChain(s['sample'],histname='')
  #s['chain'].SetAlias('dPhi',dPhiStr)

#defining ht, st and njets for SR
streg = [(250,-1)]#,(350,450),(450,-1)]                         
htreg = [(500,-1)]#,(750,1000),(1000,1250),(1250,-1)]
njreg = [(5,-1)]
btb = [(0,0)]
diMuonic = '(Sum$(abs(LepGood_pdgId)==13&&LepGood_pt[0]>=25&&LepGood_pt[1]>=20&&abs(LepGood_eta)<2.4&&LepGood_miniRelIso<0.2&&LepGood_tightId==1&&LepGood_sip3d<4.0&&((LepGood_charge[0]+LepGood_charge[1])==0))==2)'
diElectronic = "(Sum$(abs(LepGood_pdgId)==11&&LepGood_pt[0]>=25&&LepGood_pt[1]>=20&&LepGood_miniRelIso<0.1&&"+ele_MVAID_cutstr_tight+"&&LepGood_lostHits<=1&&LepGood_convVeto&&LepGood_sip3d<4.0&&LepGood_tightId>=3&&((LepGood_charge[0]+LepGood_charge[1])==0))==2)"
presel = '('+diMuonic+'||'+diElectronic+')'
#presel = diElectronic
preprefix = 'diLeptonic_ht500_lt250_nj5'
wwwDir = '/afs/hephy.at/user/d/dhandl/www/pngCMG2/hard/Phys14V3/'+preprefix+'/'

if not os.path.exists(wwwDir):
  os.makedirs(wwwDir)

def getHt(c):
  jets = cmgGetJets(c,ptMin=30,etaMax=2.4)
  ht=0
  for j in jets:
    ht += j['pt']
  return ht 

def getNJets(c):
  jets = cmgGetJets(c,ptMin=30,etaMax=2.4)
  return len(jets)

def getLeadLep(c):
  leadLep = c.GetLeaf('LepGood_pt').GetValue(0)
  return leadLep

def getZPt(c):
  leadLepPt = c.GetLeaf('LepGood_pt').GetValue(0)
  leadLepPhi = c.GetLeaf('LepGood_phi').GetValue(0)
  subLepPt = c.GetLeaf('LepGood_pt').GetValue(1)
  subLepPhi = c.GetLeaf('LepGood_phi').GetValue(1)
  Zpt = sqrt(leadLepPt**2+subLepPt**2+2*leadLepPt*subLepPt*cos(leadLepPhi-subLepPhi))
  return Zpt

def getLt(c):
  leadLepPt = c.GetLeaf('LepGood_pt').GetValue(0)
  met = c.GetLeaf('met_pt').GetValue()
  Lt = met + leadLepPt
  return Lt

def getInvMass(c):
  leadLepPt = c.GetLeaf('LepGood_pt').GetValue(0)
  leadLepPhi = c.GetLeaf('LepGood_phi').GetValue(0)
  leadLepEta = c.GetLeaf('LepGood_eta').GetValue(0)
  subLepPt = c.GetLeaf('LepGood_pt').GetValue(1)
  subLepPhi = c.GetLeaf('LepGood_phi').GetValue(1)
  subLepEta = c.GetLeaf('LepGood_eta').GetValue(1)
  invMass = sqrt(2*leadLepPt*subLepPt*(cosh(leadLepEta-subLepEta)-cos(leadLepPhi-subLepPhi)))
  return invMass

def getdPhi(c):
  a=randint(0,1)
  if a:
    #subleading lepton becomes neutrino
    lepPt = c.GetLeaf('LepGood_pt').GetValue(0)
    lepPhi = c.GetLeaf('LepGood_phi').GetValue(0)
    nuPt = c.GetLeaf('LepGood_pt').GetValue(1)
    nuPhi = c.GetLeaf('LepGood_phi').GetValue(1)
  else:
    #leading lepton becomes neutrino
    lepPt = c.GetLeaf('LepGood_pt').GetValue(1)
    lepPhi = c.GetLeaf('LepGood_phi').GetValue(1)
    nuPt = c.GetLeaf('LepGood_pt').GetValue(0)
    nuPhi = c.GetLeaf('LepGood_phi').GetValue(0)
  metPt = c.GetLeaf('met_pt').GetValue()
  metPhi = c.GetLeaf('met_phi').GetValue()
  metCorrX = metPt*cos(metPhi) + nuPt*cos(nuPhi)
  metCorrY = metPt*sin(metPhi) + nuPt*sin(nuPhi)
  metCorrPt = sqrt(metCorrX**2 + metCorrY**2)
  metCorrPhi = atan2(metCorrY,metCorrX) 
  dPhi = acos((lepPt+metCorrPt*cos(lepPhi-metCorrPhi))/(lepPt**2+metCorrPt**2+2*lepPt*metCorrPt*cos(lepPhi-metCorrPhi)))
  return dPhi

def getleadingJet(c):
  jets = cmgGetJets(c,ptMin=30,etaMax=2.4)
  Jet0 = jets[0]['pt']
  return Jet0

def getsecondJet(c):
  jets = cmgGetJets(c,ptMin=30,etaMax=2.4)
  Jet1 = jets[1]['pt']
  return Jet1

def getdPhiMetJet(c):
  jets = cmgGetJets(c,ptMin=30,etaMax=2.4)
  met = c.GetLeaf('met_pt').GetValue()
  metPhi = c.GetLeaf('met_phi').GetValue()
  JetPt = jets[0]['pt']
  JetPhi = jets[0]['phi']
#  dPhi = acos((met*JetPt*cos(metPhi-JetPhi))/(met*JetPt))
  dPhi = deltaPhi(metPhi,JetPhi)
  return dPhi

allVariables = []

met = {'name':'mymet', 'varString':"met_pt", 'legendName':'#slash{E}_{T}', 'Ytitle':'# of Events / 25GeV', 'binning':[32,0,800]}
ht = {'name':'myht', 'varFunc':getHt, 'legendName':'H_{T}', 'Ytitle':'# of Events / 25GeV', 'binning':[64,0,1600]}
Lt = {'name':'mylt', 'varFunc':getLt, 'legendName':'L_{T}', 'Ytitle':'# of Events / 25GeV', 'binning':[64,0,1600]}
#isoTrack = {'name':'myisoTrack', 'legendName':'isoTrack', 'binning':[10,0,10]}
#relIso = {'name':'myrelIso', 'legendName':'relIso', 'binning':[100,0,1.0]}
nJets = {'name':'mynJets', 'varFunc':getNJets, 'legendName':'Jets', 'Ytitle':'# of Events', 'binning':[17,-0.5,16.5]}
#nBJets = {'name':'mynBJets', 'varString':'nBJetMediumCMVA30', 'legendName':'B Jets', 'Ytitle':'# of Events', 'binning':[17,-0.5,16.5]}
dPhi = {'name':'mydeltaPhi', 'varFunc':getdPhi, 'legendName':'#Delta#Phi(W,l)','binning':[30,0,pi], 'Ytitle':'# of Events'}#, 'binningIsExplicit':True} 
lMomentum = {'name':'myleptonPt', 'varFunc':getLeadLep, 'legendName':'p_{T}(lead. l)', 'Ytitle':'# of Events / 25GeV', 'binning':[40,0,1000]}
Zmomentum = {'name':'myZPt', 'varFunc':getZPt, 'legendName':'p_{T}(Z)', 'Ytitle':'# of Events / 25GeV', 'binning':[40,0,1000]}
invMassVar = {'name':'myInvMass', 'varFunc':getInvMass, 'legendName':'m_{ll}', 'Ytitle':'# of Events / 1GeV', 'binning':[30,76,106]}
#htratio = {'name':'myhtratio', 'varFunc':gethtRatio, 'legendName':'#frac{H_{T,j>2}}{j_{1}+j_{2}}', 'Ytitle':'# of Events', 'binning':[25,0,2.5]}
#htratio3 = {'name':'myhtratio3', 'varFunc':gethtRatio3, 'legendName':'#frac{H_{T,j>3}}{j_{1}+j_{2}+j_{3}}', 'Ytitle':'# of Events', 'binning':[25,0,2.5]}
#ht3 = {'name':'myHTwithout3j', 'varFunc':getHTwithoutLeadSub, 'legendName':'H_{T,j>3}', 'Ytitle':'# of Events', 'binning':[60,0,1500]}
#jetsum3 = {'name':'myjetsum3', 'varFunc':getJetSum3, 'legendName':'j_{1}+j_{2}+j_{3}', 'Ytitle':'# of Events', 'binning':[64,0,1600]}
#jetratio = {'name':'myjetratio', 'varFunc':getJetRatio, 'legendName':'2^{nd}Jet/1^{st}Jet', 'Ytitle':'# of Events', 'binning':[15,0,1.5]}
#mt = {'name':'mymt', 'varFunc':cmgMT, 'legendName':'M_{T}', 'Ytitle':'# of Events / 10GeV', 'binning':[35,0,350]}
#MT2W = {'name':'mymt2w', 'varString':'mt2w', 'legendName':'M^{W}_{T2}', 'Ytitle':'# of Events / 10GeV', 'binning':[45,0,450]}
#dphimetjet = {'name':'mydPhimetjet', 'varFunc':getdPhiMetJet, 'legendName':'#Delta#Phi(#slash{E}_{T},J_{1})', 'Ytitle':'# of Events', 'binning':[20,0,pi]}#, 'binningIsExplicit':True}
leadingJet = {'name':'myleadingJet', 'varFunc':getleadingJet, 'legendName':'p_{T}(leading Jet)', 'Ytitle':'# of Events / 50GeV', 'binning':[32,0,1600]}
secondJet = {'name':'mysecondJet', 'varFunc':getsecondJet, 'legendName':'p_{T}(J_{2})', 'Ytitle':'# of Events / 50GeV', 'binning':[32,0,1600]}
#htOppRatio = {'name':'myhtOppRatio', 'varFunc':cmgHTRatio, 'legendName':'H^{opp. to #slash{E}_{T}}_{T}/H_{T}', 'Ytitle':'# of Events', 'binning':[20,0,1]}
#minDPhiMetJettwo = {'name':'myminDPhiMetJet12', 'varFunc':cmgMinDPhiJet, 'legendName':'min #Delta#Phi(#slash{E}_{T},J_{1,2})', 'Ytitle':'# of Events', 'binning':[20,0,pi]}#, 'binningIsExplicit':True}
#minDPhiMetJetthree = {'name':'myminDPhiMetJet123', 'varFunc':cmgMinDPhiJet, 'legendName':'min #Delta#Phi(#slash{E}_{T},J_{1,2,3})', 'Ytitle':'# of Events', 'binning':[20,0,pi]}#, 'binningIsExplicit':True}
#MTclosestJetMet = {'name':'myMTClosestJetMET', 'varFunc':cmgMTClosestJetMET, 'legendName':'M_{T} (closest Jet,#slash{E}_{T})', 'Ytitle':'# of Events / 10GeV', 'binning':[35,0,350]}
#dphijetjet = {'name':'mydPhijetjet', 'varFunc':getdPhiJetJet, 'legendName':'#Delta#Phi(J_{1},J_{0})', 'Ytitle':'# of Events', 'binning':[20,0,pi]}#, 'binningIsExplicit':True}
#jetMag = {'name':'myjetmag', 'varFunc':getJetMagnitude, 'legendName':'#frac{H_{T}}{nJets}', 'Ytitle':'# of Events', 'binning':[50,0,500]}
#mht = {'name':'mymht', 'varFunc':missingHT, 'legendName':'#slash{H}_{T}', 'Ytitle':'# of Events / 25GeV', 'binning':[40,0,1000]}
#dphimhtmet = {'name':'mydphimhtmet', 'varFunc':dPhiMHTMET, 'legendName':'#Delta#Phi(#slash{H}_{T},#slash{E}_{T})', 'Ytitle':'# of Events', 'binning':[20,0,pi]}
#stSig = {'name':'mystsig', 'varFunc':getStSig, 'legendName':'#frac{S_{T}}{#sqrt{H_{T}}}', 'Ytitle':'# of Events', 'binning':[40,0,40]}

allVariables.append(met)
allVariables.append(ht)
allVariables.append(Lt)
allVariables.append(nJets)
allVariables.append(dPhi)
allVariables.append(lMomentum)
allVariables.append(Zmomentum)
allVariables.append(invMassVar)
allVariables.append(leadingJet)
allVariables.append(secondJet)

histos = {}
h_ratio = {}

for i_htb, htb in enumerate(htreg):
  for stb in streg:
    for srNJet in njreg:
      for b in btb:
        print 'Var region => ht: ',htb,'NJet: ',srNJet,'B-tag:',b
  #    for sig in allSignals:            
  #      h_ratio[sig['name']] = {}     
        for sample in allBkg: #Loop over samples
          histos[sample['name']] = {}
  
          for var in allVariables:
            if var.has_key('binningIsExplicit') and var['binningIsExplicit']:
              histos[sample['name']][var['name']] = ROOT.TH1F(sample['name']+'_'+var['name'], sample['name']+'_'+var['name'], len(var['binning'])-1, array('d', var['binning']))
            else:
              histos[sample['name']][var['name']] = ROOT.TH1F(sample['name']+'_'+var['name'], sample['name']+'_'+var['name'], *var['binning'])
            histos[sample['name']][var['name']].Reset()
            #sample['chain'].Draw("Sum$(isoTrack_pt<15&&abs(isoTrack_pdgId)==211&&abs(isoTrack_dz)<0.05)"+">>"+sample["name"]+"_"+var["name"])
            #sample['chain'].Draw(var['varString']+">>"+sample['name']+'_'+var['name'], sample["weight"]+"*("+cut+")")
            
          namestr = nameAndCut(stb, htb, srNJet, btb=None, presel=presel, btagVar = 'nBJetMediumCMVA30')[0]
          cut = presel+'&&'+htCut(htb, minPt=30, maxEta=2.4, njCorr=0.)+'&&'+nJetCut(srNJet, minPt=30, maxEta=2.4)+'&&'+nJetCut(2, minPt=30, maxEta=2.4)#+'&&'+nBTagCut(b, minPt=30, maxEta=2.4, minCSVTag=0.814)
          #print cut
          
          sample["chain"].Draw(">>eList",cut) #Get the event list 'eList' which has all the events satisfying the cut
          elist = ROOT.gDirectory.Get("eList")
          number_events = elist.GetN()
          print "Sample ",sample["name"],": Will loop over", number_events,"events" #Number of events satisfying the cut
          
          #Event loop
          for i in range(number_events): #Loop over those events
            sample["chain"].GetEntry(elist.GetEntry(i))  #Set the chain to the current event (it's the i-th event of the eList). This is the central line in this file!
            for var in allVariables:
              invMass = getInvMass(sample['chain'])
              #Lt = getLt(sample['chain'])
              if abs(invMass-91.)>15: continue
              #if Lt<stb[0]: continue
              assert (var.has_key('varString') or var.has_key('varFunc')), "Error: Did not specify 'varString' or 'varFunc' for var %s" % repr(var)
              assert not (var.has_key('varString') and var.has_key('varFunc')), "Error: Specified both 'varString' and 'varFunc' for var %s" % repr(var)
              #if var['name'] == 'myminDPhiMetJet12':
              #  varValue = getVarValue(sample["chain_soft"], var['varString']) if var.has_key('varString') else var['varFunc'](sample["chain_soft"],nJets=2)
              #else:
              varValue = getVarValue(sample["chain"], var['varString']) if var.has_key('varString') else var['varFunc'](sample["chain"])
  #            weight = 1
  #            if sample.has_key('weight'):
  #              if type(sample['weight'])==type(''):
  #                weight = getVarValue(sample['chain'], sample['weight'])
  #              else:
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
         
  #        for sig in allSignals:
  #          histos[sig['name']][var['name']].SetLineColor(sig['color'])
  #          histos[sig['name']][var['name']].SetLineWidth(2)
  #          histos[sig['name']][var['name']].SetFillColor(0)
  #          histos[sig['name']][var['name']].SetMarkerStyle(0)
  #          histos[sig['name']][var['name']].Draw('same')
  #          l.AddEntry(histos[sig['name']][var['name']], sig['name'])
         
          l.Draw()
  
  #        for line in lines:
  #          text.SetTextSize(0.04)
  #          try:
  #            text.SetTextSize(line['options']['size'])
  #          except:pass
  #          text.DrawLatex(line['pos'][0],line['pos'][1],line['text'])
          text.DrawLatex(0.15,.96,"CMS Simulation")
          text.DrawLatex(0.65,0.96,"L="+str(target_lumi/1000)+" fb^{-1} (13 TeV)")
          
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
          del canvas, stack
          for sample in allBkg:
            del histos[sample['name']][var['name']]
