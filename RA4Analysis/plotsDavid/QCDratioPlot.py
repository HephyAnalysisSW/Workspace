import ROOT
import pickle 
import copy, os, sys
ROOT.gROOT.LoadMacro("../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()
ROOT.gStyle.SetPalette(1)

from Workspace.HEPHYPythonTools.helpers import *
from Workspace.HEPHYPythonTools.xsec import *
from Workspace.RA4Analysis.helpers import *
from Workspace.RA4Analysis.cmgTuples_v1_PHYS14V3 import *
from draw_helpers import *
from math import *
from localInfo import username
from LpTemplateFit import LpTemplateFit

preprefix = 'QCDestimation/ratioPlots'
wwwDir = '/afs/hephy.at/user/d/dhandl/www/pngCMG2/hard/Phys14V3/'+preprefix+'/'
presel = 'QCDratio_singleElectronic_'

if not os.path.exists(wwwDir):
  os.makedirs(wwwDir)

htreg = [(500,-1), (500,750), (750,-1), (750,1250),(1250,-1)]
streg = [(250,350), (350,450), (450,-1)]
njreg = [(3,4), (5,5), (6,7), (8,-1)]
btreg = [(0,0)]

#small = True
small = False
#doFit = True
doFit = False

eleVarList = ['pt', 'eta', 'phi', 'pdgId', 'miniRelIso', 'convVeto', 'sip3d', 'mvaIdPhys14', 'charge', 'lostHits']
eleFromW = ['pt', 'eta', 'phi', 'pdgId', 'motherId', 'grandmotherId', 'charge', 'sourceId']

def getMatch(genLep,recoLep):
  return ( (genLep['charge']==recoLep['charge']) and deltaR(genLep,recoLep)<0.1 and (abs(genLep['pt']-recoLep['pt'])/genLep['pt'])<0.5)

target_lumi = 3000 #pb-1
def getWeight(sample,nEvents,target_lumi):
  weight = xsec[sample['dbsName']] * target_lumi/nEvents
  return weight

def antiSel(e):
  if abs(e['eta'])<0.8:
    return (e['pt']>=25 and abs(e['pdgId'])==11 and e['miniRelIso']<0.4 and e['mvaIdPhys14']>=0.35 and e['mvaIdPhys14']<0.73)
  if (abs(e['eta'])>=0.8 and abs(e['eta'])<1.4):
    return (e['pt']>=25 and abs(e['pdgId'])==11 and e['miniRelIso']<0.4 and e['mvaIdPhys14']>=0.20 and e['mvaIdPhys14']<0.57)
  if (abs(e['eta'])>=1.4 and abs(e['eta'])<2.4):
    return (e['pt']>=25 and abs(e['pdgId'])==11 and e['miniRelIso']<0.4 and e['mvaIdPhys14']>=(-0.52) and e['mvaIdPhys14']<0.05)
  return False

def sel(e):
  if abs(e['eta'])<0.8:
    return (e['pt']>=25 and abs(e['pdgId'])==11 and e['miniRelIso']<0.1 and e['convVeto']==1 and e['sip3d']<4.0 and e['lostHits']==0 and e['mvaIdPhys14']>=0.73)
  if (abs(e['eta'])>=0.8 and abs(e['eta'])<1.4):
    return (e['pt']>=25 and abs(e['pdgId'])==11 and e['miniRelIso']<0.1 and e['convVeto']==1 and e['sip3d']<4.0 and e['lostHits']==0 and e['mvaIdPhys14']>=0.57)
  if (abs(e['eta'])>=1.4 and abs(e['eta'])<2.4):
    return (e['pt']>=25 and abs(e['pdgId'])==11 and e['miniRelIso']<0.1 and e['convVeto']==1 and e['sip3d']<4.0 and e['lostHits']==0 and e['mvaIdPhys14']>=0.05)
  return False

def getLp(met,metPhi,e):
#  met = c.GetLeaf('met_pt').GetValue()
#  metPhi = c.GetLeaf('met_phi').GetValue()
  
  Lp = e['pt']/sqrt( (e['pt']*cos(e['phi']) + met*cos(metPhi))**2 + (e['pt']*sin(e['phi']) + met*sin(metPhi))**2 )\
       * (e['pt']+met*cos(e['phi']-metPhi))/sqrt(e['pt']**2+met**2+2*met*e['pt']*cos(e['phi']-metPhi))
  return Lp

Bkg = [#{'name':'QCD_HT_100To250_PU20bx25', 'sample':QCD_HT_100To250_PU20bx25, 'legendName':'QCD HT100-250', 'color':ROOT.kCyan+3},
       {'name':'QCD_HT_250To500_PU20bx25', 'sample':QCD_HT_250To500_PU20bx25, 'legendName':'QCD HT250-500', 'color':ROOT.kCyan, 'merge':'QCD'},
       {'name':'QCD_HT_500To1000_PU20bx25', 'sample':QCD_HT_500To1000_PU20bx25, 'legendName':'QCD HT500-1000', 'color':ROOT.kCyan-3, 'merge':'QCD'},
       {'name':'QCD_HT_1000ToInf_PU20bx25', 'sample':QCD_HT_1000ToInf_PU20bx25, 'legendName':'QCD HT1000-Inf', 'color':ROOT.kCyan-7, 'merge':'QCD'},
       {'name':'TBarToLeptons_sChannel_PU20bx25', 'sample':TBarToLeptons_sChannel_PU20bx25, 'legendName':'TBarToLep sCh', 'color':ROOT.kViolet, 'merge':'EWK'},
       {'name':'TBarToLeptons_tChannel_PU20bx25', 'sample':TBarToLeptons_tChannel_PU20bx25, 'legendName':'TBarToLep tCh', 'color':ROOT.kViolet-3, 'merge':'EWK'},
       {'name':'TToLeptons_sChannel_PU20bx25', 'sample':TToLeptons_sChannel_PU20bx25, 'legendName':'TToLep sCh', 'color':ROOT.kViolet-5, 'merge':'EWK'},
       {'name':'TToLeptons_tChannel_PU20bx25', 'sample':TToLeptons_tChannel_PU20bx25, 'legendName':'TToLep tCh', 'color':ROOT.kViolet-7, 'merge':'EWK'},
       {'name':'T_tWChannel_PU20bx25', 'sample':T_tWChannel_PU20bx25, 'legendName':'TtW', 'color':ROOT.kViolet+1, 'merge':'EWK'},
       {'name':'TBar_tWChannel_PU20bx25', 'sample':TBar_tWChannel_PU20bx25, 'legendName':'TBartW', 'color':ROOT.kViolet+6, 'merge':'EWK'},
       {'name':'ttWJets_PU20bx25', 'sample':ttWJets_PU20bx25, 'legendName':'tt+W', 'color':ROOT.kOrange, 'merge':'EWK'},
       {'name':'ttZJets_PU20bx25', 'sample':ttZJets_PU20bx25, 'legendName':'tt+Z', 'color':ROOT.kOrange+7, 'merge':'EWK'},
       {'name':'ttH_PU20bx25', 'sample':ttH_PU20bx25, 'legendName':'tt+H', 'color':ROOT.kOrange+4, 'merge':'EWK'},
       {'name':'DYJetsToLL_M50_HT100to200_PU20bx25', 'sample':DYJetsToLL_M50_HT100to200_PU20bx25, 'legendName':'DY HT100-200', 'color':ROOT.kRed, 'merge':'EWK'},
       {'name':'DYJetsToLL_M50_HT200to400_PU20bx25', 'sample':DYJetsToLL_M50_HT200to400_PU20bx25, 'legendName':'DY HT200-400', 'color':ROOT.kRed+2, 'merge':'EWK'},
       {'name':'DYJetsToLL_M50_HT400to600_PU20bx25', 'sample':DYJetsToLL_M50_HT400to600_PU20bx25, 'legendName':'DY HT400-600', 'color':ROOT.kRed-7, 'merge':'EWK'},
       {'name':'DYJetsToLL_M50_HT600toInf_PU20bx25', 'sample':DYJetsToLL_M50_HT600toInf_PU20bx25, 'legendName':'DY HT600-Inf', 'color':ROOT.kRed-8, 'merge':'EWK'},
       {'name':'WJetsToLNu_HT100to200_PU20bx25', 'sample':WJetsToLNu_HT100to200_PU20bx25, 'legendName':'W HT100-200', 'color':ROOT.kGreen+3, 'merge':'EWK'},
       {'name':'WJetsToLNu_HT200to400_PU20bx25', 'sample':WJetsToLNu_HT200to400_PU20bx25, 'legendName':'W HT200-400', 'color':ROOT.kGreen, 'merge':'EWK'},
       {'name':'WJetsToLNu_HT400to600_PU20bx25', 'sample':WJetsToLNu_HT400to600_PU20bx25, 'legendName':'W HT400-600', 'color':ROOT.kGreen-3, 'merge':'EWK'},
       {'name':'WJetsToLNu_HT600toInf_PU20bx25', 'sample':WJetsToLNu_HT600toInf_PU20bx25, 'legendName':'W HT600-Inf', 'color':ROOT.kGreen-7, 'merge':'EWK'},
       {'name':'ttJets_PU20bx25', 'sample':ttJets_PU20bx25, 'legendName':'ttJets', 'color':ROOT.kRed, 'merge':'EWK'},# 'prompt':False},
]

maxN=1 if small else -1

for sample in Bkg:
  sample['chunks'], sample['nEvents'] = getChunks(sample['sample'],treeName='treeProducerSusySingleLepton', maxN=maxN)
  sample['chain'] = ROOT.TChain('tree')
  for chunk in sample['chunks']:
    sample['chain'].Add(chunk['file'])

  sample['weight'] = getWeight(sample['sample'], sample['nEvents'], target_lumi)

histos = {}
bins = {}
for htb in htreg:
  bins[htb] = {}
  for stb in streg:
    bins[htb][stb] = {}
    for srNJet in njreg:
      bins[htb][stb][srNJet] = {}
      for btb in btreg:
        bins[htb][stb][srNJet][btb]={}

        print 'Binning => ht: ',htb,'st: ',stb,'NJet: ',srNJet
        SRname = nameAndCut(stb, htb, srNJet, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]#use this function only for the name string!!!
        #cut only includes very loose lepton selection, HT cut, NJet cut, Btagging and subleading JetPt>=80!!! St cut applied in the Event Loop!!!
#        cut = '(Sum$(abs(LepGood_pdgId)==11&&abs(LepGood_dxy)<=0.05&&abs(LepGood_dz)<=0.1)+Sum$(abs(LepOther_pdgId)==11&&abs(LepOther_dxy)<=0.05&&abs(LepOther_dz)<=0.1)>=1)&&'+htCut(htb, minPt=30, maxEta=2.4, njCorr=0.)+'&&'+ nBTagCut(btb, minPt=30, maxEta=2.4, minCSVTag=0.814)+'&&'+nJetCut(srNJet, minPt=30, maxEta=2.4)+'&&'+nJetCut(2, minPt=80, maxEta=2.4)
        cut = '(Sum$(abs(LepGood_pdgId)==11&&LepGood_pt>10)>=1)&&'+htCut(htb, minPt=30, maxEta=2.4, njCorr=0.)+'&&'+ nBTagCut(btb, minPt=30, maxEta=2.4, minCSVTag=0.814)+'&&'+nJetCut(srNJet, minPt=30, maxEta=2.4)+'&&'+nJetCut(2, minPt=80, maxEta=2.4)

#        histos['merged_QCD']={}
#        histos['merged_EWK']={}
#        histos['merged_QCD']['antiSelection']=ROOT.TH1F('merged_QCD_antiSelection','merged_QCD_antiSelection',12,-0.7,1.7)
#        histos['merged_QCD']['Selection']=ROOT.TH1F('merged_QCD_Selection','merged_QCD_Selection',12,-0.7,1.7)
#        histos['merged_EWK']['antiSelection']=ROOT.TH1F('merged_EWK_antiSelection','merged_EWK_antiSelection',12,-0.7,1.7)
#        histos['merged_EWK']['Selection']=ROOT.TH1F('merged_EWK_Selection','merged_EWK_Selection',12,-0.7,1.7)

        nSelected = 0
        nSelectedVar = 0
        nQCDSelected = 0
        nQCDSelectedVar = 0
        nAntiSelected = 0     
        nAntiSelectedVar = 0     
        
        for sample in Bkg:
          nSampleSelected = 0
          nSampleSelectedVar = 0
          nSampleAntiSelected =0
          nSampleAntiSelectedVar = 0
#          histos[sample['name']] = {}
#          histos[sample['name']]['antiSelection'] = ROOT.TH1F(sample['name']+'_antiSelection', sample['name']+'_antiSelection',1,0,2)
#          histos[sample['name']]['Selection'] = ROOT.TH1F(sample['name']+'_Selection', sample['name']+'_Selection',1,0,2)
        
          #Get the event list 'eList' which has all the events satisfying the cut
          sample["chain"].Draw(">>eList",cut)
          elist = ROOT.gDirectory.Get("eList")
          number_events = elist.GetN()
          print "Sample ",sample['name'],": Will loop over", number_events,"events"
        
          #Event Loop
          for i in range(number_events):
            if i%10000==0:
              print "At %i of %i for sample %s"%(i,number_events,sample['name'])
            sample['chain'].GetEntry(elist.GetEntry(i))
        
            eles = [getObjDict(sample['chain'], 'LepGood_', eleVarList, j) for j in range(int(sample['chain'].GetLeaf('nLepGood').GetValue()))]
#                 + [getObjDict(sample['chain'], 'LepOther_', eleVarList, j) for j in range(int(sample['chain'].GetLeaf('nLepOther').GetValue()))]
        
            genEle = [getObjDict(sample['chain'], 'genLep_', eleFromW, j) for j in range(int(sample['chain'].GetLeaf('ngenLep').GetValue()))] 
        
            met=sample['chain'].GetLeaf('met_pt').GetValue()
            metPhi=sample['chain'].GetLeaf('met_phi').GetValue()
        
            eles = filter(lambda e:abs(e['pdgId'])==11, eles) 
            eles = filter(lambda e:e['pt']>=25, eles) 
            eles = filter(lambda e:e['miniRelIso']<0.4, eles) #require relIso
            eles = filter(lambda e:abs(e['eta'])<2.4, eles) 
        
            eles = filter(lambda e:(e['pt']+met)>=stb[0], eles) 

            if stb[1]>0:
              eles = filter(lambda e:(e['pt']+met)<stb[1], eles)

            for e in eles:
              e["antiSel"] =  antiSel(e) 
              e["sel"] =  sel(e) 

            elesSelected = filter(lambda e:e['sel'],eles)
            elesAntiSelected = filter(lambda e:e['antiSel'],eles)
            nElesSelected = len(elesSelected)
            nElesAntiSelected = len(elesAntiSelected)

            if not nElesSelected+nElesAntiSelected==1:continue
            #print "nElesSelected %i nElesAntiSelected %i"%(nElesSelected,nElesAntiSelected)
            if nElesSelected==1:
              recoEle = elesSelected[0]
              isSelected = True 
            else:
              recoEle = elesAntiSelected[0]
              isSelected = False 

            #gen Electrons        
            genEle = filter(lambda e:abs(e['pdgId'])==11, genEle)
            genEle = filter(lambda e:e['pt']>=10, genEle)

#            if len(eles)>1:
#        #      print len(eles), len(genEle)
#              continue

            if len(eles)==0:print "Should never happen"
 
#            if sample.has_key('prompt'):
#              if sample['prompt']:
#                for reco in eles:
#                  hasMatch=False
#                  for gen in genEle:
#                    if getMatch(gen,reco):
#                      if reco["antiSel"]:
#                        antiVal = getLp(met,metPhi,reco) 
#                        histos[sample['name']]['antiSelection'].Fill(antiVal,sample['weight'])
#                      if sel(reco):
#                        selVal = getLp(met,metPhi,reco)
#                        histos[sample['name']]['Selection'].Fill(selVal,sample['weight'])
#                    hasMatch=True
#        #          if not hasMatch:
#        #            if antiSel(reco):
#        #              antiVal = getLp(sample['chain'],reco)
#        #              histos[sample['name']]['antiSelection'].Fill(antiVal,sample['weight'])
#        #            elif Sel(reco):
#        #              selVal = getLp(sample['chain'],reco)
#        #              histos[sample['name']]['Selection'].Fill(selVal,sample['weight'])  
#        
#            else:
        #      print len(eles)
#            for reco in eles:
#            lp = getLp(met,metPhi,recoEle)
            if isSelected:
              nSampleSelected += sample['weight']
              nSampleSelectedVar += sample['weight']*sample['weight']
#              histos[sample['name']]['Selection'].Fill(1,sample['weight'])
            else: 
              nSampleAntiSelected += sample['weight']
              nSampleAntiSelectedVar += sample['weight']*sample['weight']
#              histos[sample['name']]['antiSelection'].Fill(1,sample['weight'])
        
          del elist
          sample['nSelected'] = nSampleSelected
          sample['nSelectedVar'] = nSampleSelectedVar
          sample['nAntiSelected'] = nSampleAntiSelected
          sample['nAntiSelectedVar'] = nSampleAntiSelectedVar
          bins[htb][stb][srNJet][btb].update({sample['name']+'_nSelected':sample['nSelected'], sample['name']+'_nSelectedVar':sample['nSelectedVar'],\
                                              sample['name']+'_nAntiSelected':sample['nAntiSelected'], sample['name']+'_nAntiSelectedVar':sample['nAntiSelectedVar']})
          nSelected += sample['nSelected'] 
          nSelectedVar += sample['nSelectedVar'] 
          nAntiSelected += sample['nAntiSelected']
          nAntiSelectedVar += sample['nAntiSelectedVar']
          if sample['merge']=='QCD':
            nQCDSelected += sample['nSelected']
            nQCDSelectedVar += sample['nSelectedVar']
          bins[htb][stb][srNJet][btb].update({'nSelected':nSelected, 'nSelectedVar':nSelectedVar,\
                                              'nAntiSelected':nAntiSelected, 'nAntiSelectedVar':nAntiSelectedVar,\
                                              'nQCDSelected':nQCDSelected, 'nQCDSelectedVar':nQCDSelectedVar})

ROOT_colors = [ROOT.kBlack, ROOT.kRed-7, ROOT.kBlue-2, ROOT.kGreen+3, ROOT.kOrange+1,ROOT.kRed-3, ROOT.kAzure+6, ROOT.kCyan+3, ROOT.kOrange , ROOT.kRed-10]
#plot F_sel-to-antisel binned in HT for all Njets
ratio_ht={}
for stb in streg:
  ratio_ht[stb]={}
  first = True
  canv = ROOT.TCanvas('canv','canv',600,600)
  #canv.SetLogy()
  l = ROOT.TLegend(0.65,0.85,0.95,0.95)
  l.SetFillColor(0)
  l.SetBorderSize(1)
  
  l.SetShadowColor(ROOT.kWhite)
  text = ROOT.TLatex()
  text.SetNDC()
  text.SetTextSize(0.04)
  text.SetTextAlign(11)
  t=ROOT.TLatex()
  t.SetNDC()
  t.SetTextSize(0.04)
  t.SetTextAlign(11)
  for i_njb, njb in enumerate(njreg):
    ratio_ht[stb][njb]={}
    for btb in btreg:
      ratio_ht[stb][njb][btb]=ROOT.TH1F('ratio_htHist','ratio_htHist',len(htreg),0,len(htreg))
      ratio_ht[stb][njb][btb].SetLineColor(ROOT_colors[i_njb])
      ratio_ht[stb][njb][btb].SetLineWidth(2)
      for i_htb, htb in enumerate(htreg):
        nQCDsel = bins[htb][stb][njb][btb]['nQCDSelected'] 
        nQCDselVar = bins[htb][stb][njb][btb]['nQCDSelectedVar'] 
        nQCDantisel = bins[htb][stb][njb][btb]['nAntiSelected'] 
        nQCDantiselVar = bins[htb][stb][njb][btb]['nAntiSelectedVar'] 
#          print nQCDsel, nQCDantisel
        if nQCDantisel>0:
          F=nQCDsel/nQCDantisel
          print 'F_sel-to-anti-sel('+str(stb)+','+str(njb)+','+str(htb)+'):',F
          if F>0:
            F_err= F*sqrt(nQCDselVar/nQCDsel**2+nQCDantiselVar/nQCDantisel**2)
            ratio_ht[stb][njb][btb].SetBinContent(i_htb+1,F)
            ratio_ht[stb][njb][btb].SetBinError(i_htb+1,F_err)
        ratio_ht[stb][njb][btb].GetXaxis().SetBinLabel(i_htb+1, varBinName(htb,'H_{T}'))
        ratio_ht[stb][njb][btb].GetYaxis().SetTitle('F_{sel-to-antisel}')
#        ratio_ht[stb][njb].GetXaxis().SetTitle('F_{sel-to-antisel}')
      l.AddEntry(ratio_ht[stb][njb][btb], nJetBinName(njb))
      if first:
        ratio_ht[stb][njb][btb].Draw()
        first = False
      else:
        ratio_ht[stb][njb][btb].Draw('same') 
      l.Draw()
      t.DrawLatex(0.175,0.85,varBinName(stb,'S_{T}'))
      text.DrawLatex(0.15,.96,"CMS Simulation")
      text.DrawLatex(0.65,0.96,"L="+str(target_lumi/1000)+" fb^{-1} (13 TeV)")
      canv.Print(wwwDir+presel+'Fsa_ht_'+nameAndCut(stb, None, None, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.png')
      canv.Print(wwwDir+presel+'Fsa_ht_'+nameAndCut(stb, None, None, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.pdf')
      canv.Print(wwwDir+presel+'Fsa_ht_'+nameAndCut(stb, None, None, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.root')

#plot F_sel-to-antisel binned in ST for all Njets
ratio_st={}
for htb in htreg:
  ratio_st[htb]={}
  first = True
  canv2= ROOT.TCanvas('canv2','canv2',600,600)
  #canv.SetLogy()
  l2 = ROOT.TLegend(0.65,0.85,0.95,0.95)
  l2.SetFillColor(0)
  l2.SetBorderSize(1)
  l2.SetShadowColor(ROOT.kWhite)
  
  t=ROOT.TLatex()
  t.SetNDC()
  t.SetTextSize(0.04)
  t.SetTextAlign(11)
  for i_njb, njb in enumerate(njreg):
    ratio_st[htb][njb]={}
    for btb in btreg:
      ratio_st[htb][njb][btb]=ROOT.TH1F('ratio_stHist','ratio_stHist',len(streg),0,len(streg))
      ratio_st[htb][njb][btb].SetLineColor(ROOT_colors[i_njb])
      ratio_st[htb][njb][btb].SetLineWidth(2)
      for i_stb, stb in enumerate(streg):
        nQCDsel = bins[htb][stb][njb][btb]['nQCDSelected'] 
        nQCDselVar = bins[htb][stb][njb][btb]['nQCDSelectedVar'] 
        nQCDantisel = bins[htb][stb][njb][btb]['nAntiSelected'] 
        nQCDantiselVar = bins[htb][stb][njb][btb]['nAntiSelectedVar'] 
#          print nQCDsel, nQCDantisel
        if nQCDantisel>0:
          F=nQCDsel/nQCDantisel
          print 'F_sel-to-anti-sel('+str(stb)+','+str(njb)+','+str(htb)+'):',F
          if F>0:
            F_err= F*sqrt(nQCDselVar/nQCDsel**2+nQCDantiselVar/nQCDantisel**2)
            ratio_st[htb][njb][btb].SetBinContent(i_stb+1,F)
            ratio_st[htb][njb][btb].SetBinError(i_stb+1,F_err)
        ratio_st[htb][njb][btb].GetXaxis().SetBinLabel(i_stb+1, varBinName(stb,'S_{T}'))
        ratio_st[htb][njb][btb].GetYaxis().SetTitle('F_{sel-to-antisel}')
#        ratio_st[htb][njb].GetXaxis().SetTitle('F_{sel-to-antisel}')
      l2.AddEntry(ratio_st[htb][njb][btb], nJetBinName(njb))
      if first:
        ratio_st[htb][njb][btb].Draw()
        first = False
      else:
        ratio_st[htb][njb][btb].Draw('same') 
      l2.Draw()
      t.DrawLatex(0.175,0.85,varBinName(htb,'H_{T}'))
      text.DrawLatex(0.15,.96,"CMS Simulation")
      text.DrawLatex(0.65,0.96,"L="+str(target_lumi/1000)+" fb^{-1} (13 TeV)")
      canv2.Print(wwwDir+presel+'Fsa_st_'+nameAndCut(None, htb, njetb=None, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.png')
      canv2.Print(wwwDir+presel+'Fsa_st_'+nameAndCut(None, htb, njetb=None, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.pdf')
      canv2.Print(wwwDir+presel+'Fsa_st_'+nameAndCut(None, htb, njetb=None, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.root')

#plot F_sel-to-antisel binned in ST vs HT
ratio_2d={}
for njb in njreg:
  ratio_2d[njb]={}
  canv3= ROOT.TCanvas('canv3','canv3',600,600)
  #canv.SetLogy()
#  l3 = ROOT.TLegend(0.65,0.75,0.95,0.95)
#  l3.SetFillColor(0)
#  l3.SetBorderSize(1)
#  l3.SetShadowColor(ROOT.kWhite)
  
  t=ROOT.TLatex()
  t.SetNDC()
  t.SetTextSize(0.04)
  t.SetTextAlign(11)
  for btb in btreg:
    ratio_2d[njb][btb]={}
    ratio_2d[njb][btb]=ROOT.TH2F('ratio_2dHist','ratio_2dHist',len(htreg),0,len(htreg),len(streg),0,len(streg))
    for i_htb, htb in enumerate(htreg):
      ratio_2d[njb][btb].GetXaxis().SetBinLabel(i_htb+1,varBinName(htb,'H_{T}'))
    for i_stb, stb in enumerate(streg):
      ratio_2d[njb][btb].GetYaxis().SetBinLabel(i_stb+1,varBinName(stb,'S_{T}'))

    for i_htb, htb in enumerate(htreg):
      for i_stb, stb in enumerate(streg):
        nQCDsel = bins[htb][stb][njb][btb]['nQCDSelected'] 
        nQCDselVar = bins[htb][stb][njb][btb]['nQCDSelectedVar'] 
        nQCDantisel = bins[htb][stb][njb][btb]['nAntiSelected'] 
        nQCDantiselVar = bins[htb][stb][njb][btb]['nAntiSelectedVar'] 
#          print nQCDsel, nQCDantisel
        if nQCDantisel>0:
          F=nQCDsel/nQCDantisel
          print 'F_sel-to-anti-sel('+str(stb)+','+str(njb)+','+str(htb)+'):',F
          if F>0:
            F_err= F*sqrt(nQCDselVar/nQCDsel**2+nQCDantiselVar/nQCDantisel**2)
            ratio_2d[njb][btb].SetBinContent(i_htb+1,i_stb+1,F)
            ratio_2d[njb][btb].SetBinError(i_htb+1,i_stb+1,F_err)
#      l.AddEntry(ratio_2d[htb][njb][btb], nJetBinName(njb))
        ratio_2d[njb][btb].Draw('COLZ TEXTE')
      t.DrawLatex(0.175,0.85,nJetBinName(njb))
      text.DrawLatex(0.15,.96,"CMS Simulation")
      text.DrawLatex(0.65,0.96,"L="+str(target_lumi/1000)+" fb^{-1} (13 TeV)") 
      canv3.Print(wwwDir+presel+'st_vs_ht_'+nameAndCut(None, None, njetb=njb, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.png')
      canv3.Print(wwwDir+presel+'st_vs_ht_'+nameAndCut(None, None, njetb=njb, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.pdf')
      canv3.Print(wwwDir+presel+'st_vs_ht_'+nameAndCut(None, None, njetb=njb, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.root')
#        
#        first = True
#        antiMax=0
#        selMax=0
#        for sample in Bkg:
#          histos[sample['name']]['antiSelection'].SetLineColor(sample['color'])
#          histos[sample['name']]['antiSelection'].SetLineStyle(ROOT.kDashed)
#          histos[sample['name']]['antiSelection'].SetLineWidth(2)
#          histos[sample['name']]['antiSelection'].GetYaxis().SetTitle('# of Events')
#          histos[sample['name']]['antiSelection'].GetXaxis().SetTitle('L_{p}')
#          histos[sample['name']]['Selection'].SetLineColor(sample['color'])
#          histos[sample['name']]['Selection'].SetLineWidth(2)
#          histos[sample['name']]['Selection'].GetYaxis().SetTitle('# of Events')
#          histos[sample['name']]['Selection'].GetXaxis().SetTitle('L_{P}')
#          l.AddEntry(histos[sample['name']]['antiSelection'], sample['legendName']+' anti-selected')
#          l.AddEntry(histos[sample['name']]['Selection'], sample['legendName']+' selected')
#        
#          if sample['merge']=='QCD':
#            histos['merged_QCD']['antiSelection'].Add(histos[sample['name']]['antiSelection'])
#            histos['merged_QCD']['Selection'].Add(histos[sample['name']]['Selection'])
#        
#          elif sample['merge']=='EWK':
#            histos['merged_EWK']['antiSelection'].Add(histos[sample['name']]['antiSelection'])
#            histos['merged_EWK']['Selection'].Add(histos[sample['name']]['Selection'])
#        
#          if first:
#            histos[sample['name']]['antiSelection'].Draw()
#            histos[sample['name']]['Selection'].Draw('same')
#          else:
#            histos[sample['name']]['antiSelection'].Draw('same')
#            histos[sample['name']]['Selection'].Draw('same')
#          first = False
#        
#          if histos[sample['name']]['antiSelection'].GetMaximum() > antiMax:
#            antiMax = histos[sample['name']]['antiSelection'].GetMaximum()
#          if histos[sample['name']]['Selection'].GetMaximum() > selMax:
#            selMax = histos[sample['name']]['Selection'].GetMaximum()
#        
#        for sample in Bkg:
#          histos[sample['name']]['antiSelection'].SetMaximum(1.5*antiMax)
#          histos[sample['name']]['antiSelection'].SetMinimum(0)
#          histos[sample['name']]['Selection'].SetMaximum(1.5*selMax)
#          histos[sample['name']]['Selection'].SetMinimum(0)
#        
#        l.Draw() 
#        text.DrawLatex(0.15,.96,"CMS Simulation")
#        text.DrawLatex(0.65,0.96,"L="+str(target_lumi/1000)+" fb^{-1} (13 TeV)")
#        
##        canv.cd()
##        canv.Print(wwwDir+presel+SRname+'_subBkg.png')
##        canv.Print(wwwDir+presel+SRname+'_subBkg.root')
##        canv.Print(wwwDir+presel+SRname+'_subBkg.pdf')
#        
#        mergeCanv = ROOT.TCanvas('merged Canv','merged Canv',600,600)
#        #mergeCanv.SetLogy()
#        leg = ROOT.TLegend(0.65,0.75,0.95,0.95)
#        leg.SetFillColor(0)
#        leg.SetBorderSize(1)
#        leg.SetShadowColor(ROOT.kWhite)
#        
#        for hist in [histos['merged_QCD']['antiSelection'],histos['merged_QCD']['Selection'],histos['merged_EWK']['antiSelection'],histos['merged_EWK']['Selection']]:
#          hist.SetStats(0)
#          hist.GetYaxis().SetTitle('# of Events')
#          hist.GetXaxis().SetTitle('L_{p}')
#          hist.SetLineWidth(2)
#       
#        NdataSel =  histos['merged_QCD']['Selection'].Integral() +  histos['merged_EWK']['Selection'].Integral() 
#        NdataAntiSel =  histos['merged_QCD']['antiSelection'].Integral() +  histos['merged_EWK']['antiSelection'].Integral() 
#        bins[htb][stb][srNJet][btb] = {'NdataSel':NdataSel, 'NdataAntiSel':NdataAntiSel}
#        print bins[htb][stb][srNJet][btb]
#
#        #do the template fit:
#        if doFit:
#          LpTemplates = {'EWKantiSel':histos['merged_EWK']['antiSelection'], 'EWKsel':histos['merged_EWK']['Selection'], 'QCDantiSel':histos['merged_QCD']['antiSelection'], 'QCDsel':histos['merged_QCD']['Selection']}
#          fit_QCD = LpTemplateFit(LpTemplates, prefix=presel+SRname, printDir='/afs/hephy.at/user/'+username[0]+'/'+username+'/www/pngCMG2/templateFit_Phys14V3/QCDestimation')
#          bins[htb][stb][srNJet][btb].update(fit_QCD)
#     
#        mergeCanv.cd() 
##        if histos['merged_QCD']['antiSelection'].Integral()>0:
##          histos['merged_QCD']['antiSelection'].Scale(1./histos['merged_QCD']['antiSelection'].Integral())
#        histos['merged_QCD']['antiSelection'].SetLineColor(ROOT.kRed)
#        histos['merged_QCD']['antiSelection'].SetLineStyle(ROOT.kDashed)
##        histos['merged_QCD']['antiSelection'].SetMaximum(1)
#        leg.AddEntry(histos['merged_QCD']['antiSelection'],'QCD anti-selected','l')
# 
##        if histos['merged_QCD']['Selection'].Integral()>0:
##          histos['merged_QCD']['Selection'].Scale(1./histos['merged_QCD']['Selection'].Integral())      
#        histos['merged_QCD']['Selection'].SetLineColor(ROOT.kRed)
##        histos['merged_QCD']['Selection'].SetMaximum(1)
#        leg.AddEntry(histos['merged_QCD']['Selection'],'QCD selected','l')
# 
##        if histos['merged_EWK']['antiSelection'].Integral()>0:
##          histos['merged_EWK']['antiSelection'].Scale(1./histos['merged_EWK']['antiSelection'].Integral())       
#        histos['merged_EWK']['antiSelection'].SetLineColor(ROOT.kBlack)
#        histos['merged_EWK']['antiSelection'].SetLineStyle(ROOT.kDashed)
##        histos['merged_EWK']['antiSelection'].SetMaximum(1)
#        leg.AddEntry(histos['merged_EWK']['antiSelection'],'EWK anti-selected','l')
# 
##        if histos['merged_EWK']['Selection'].Integral()>0:
##          histos['merged_EWK']['Selection'].Scale(1./histos['merged_EWK']['Selection'].Integral())             
#        histos['merged_EWK']['Selection'].SetLineColor(ROOT.kBlack)
##        histos['merged_EWK']['Selection'].SetMaximum(1)
#        leg.AddEntry(histos['merged_EWK']['Selection'],'EWK selected','l')
#        
#        histos['merged_QCD']['antiSelection'].Draw()
#        histos['merged_QCD']['Selection'].Draw('same')
#        histos['merged_EWK']['antiSelection'].Draw('same')
#        histos['merged_EWK']['Selection'].Draw('same')
#          
#        leg.Draw()
#        text.DrawLatex(0.15,.96,"CMS Simulation")
#        text.DrawLatex(0.65,0.96,"L="+str(target_lumi/1000)+" fb^{-1} (13 TeV)")
        
#        mergeCanv.cd()
#        mergeCanv.Print(wwwDir+presel+SRname+'.png')
#        mergeCanv.Print(wwwDir+presel+SRname+'.root')
#        mergeCanv.Print(wwwDir+presel+SRname+'.pdf')


#path = '/data/'+username+'/results2015/rCS_0b/'
#if not os.path.exists(path):
#  os.makedirs(path)
#pickle.dump(bins, file(path+'QCDyieldFromTemplateFit_inclusive__pkl','w'))
