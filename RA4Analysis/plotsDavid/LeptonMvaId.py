import ROOT
import copy, os, sys
ROOT.gROOT.LoadMacro("../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()

from Workspace.HEPHYPythonTools.helpers import *
from Workspace.HEPHYPythonTools.xsec import *
from Workspace.RA4Analysis.helpers import *
from Workspace.RA4Analysis.cmgTuples_v1_PHYS14V3 import *
from math import *

preprefix = 'QCDestimation'
wwwDir = '/afs/hephy.at/user/d/dhandl/www/pngCMG2/hard/Phys14V3/'+preprefix+'/'

if not os.path.exists(wwwDir):
  os.makedirs(wwwDir)

#cut = '((nLepGood==1&&nLepOther==0)||(nLepGood==0&&nLepOther==1))&&(Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id)>=3)&&(Sum$((Jet_pt)*(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id))>500)&&(Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id&&Jet_btagCSV>0.814)==0)'
#cut = '((nLepGood==1&&nLepOther==0)||(nLepGood==0&&nLepOther==1))&&(Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id&&Jet_btagCSV>0.814)==0)'
cut = 'Sum$(abs(LepGood_pdgId)==11)+Sum$(abs(LepOther_pdgId)==11)>=1'
#small = True
small = False
eleVarList = ['pt', 'eta', 'phi', 'pdgId', 'miniRelIso', 'convVeto', 'sip3d', 'mvaIdPhys14', 'charge']
eleFromW = ['pt', 'eta', 'phi', 'pdgId', 'motherId', 'grandmotherId', 'charge', 'sourceId']

def getMatch(genLep,recoLep):
  return ( (genLep['charge']==recoLep['charge']) and deltaR(genLep,recoLep)<0.1 and (abs(genLep['pt']-recoLep['pt'])/genLep['pt'])<0.5)

target_lumi = 2000 #pb-1
def getWeight(sample,nEvents,target_lumi):
  weight = xsec[sample['dbsName']] * target_lumi/nEvents
  return weight

def antiSel(e):
  if abs(e['eta'])<0.8:
    return (e['pt']>25 and abs(e['pdgId'])==11 and e['miniRelIso']<0.4 and e['mvaIdPhys14']>=0.35 and e['mvaIdPhys14']<0.73)
  if (abs(e['eta'])>=0.8 and abs(e['eta'])<1.4):
    return (e['pt']>25 and abs(e['pdgId'])==11 and e['miniRelIso']<0.4 and e['mvaIdPhys14']>=0.20 and e['mvaIdPhys14']<0.57)
  if (abs(e['eta'])>=1.4 and abs(e['eta'])<2.4):
    return (e['pt']>25 and abs(e['pdgId'])==11 and e['miniRelIso']<0.4 and e['mvaIdPhys14']>=(-0.52) and e['mvaIdPhys14']<0.05)

def Sel(e):
  if abs(e['eta'])<0.8:
    return (e['pt']>25 and abs(e['pdgId'])==11 and e['miniRelIso']<0.1 and e['convVeto']==1 and e['sip3d']<4.0 and e['mvaIdPhys14']>0.73)
  if (abs(e['eta'])>=0.8 and abs(e['eta'])<1.4):
    return (e['pt']>25 and abs(e['pdgId'])==11 and e['miniRelIso']<0.1 and e['convVeto']==1 and e['sip3d']<4.0 and e['mvaIdPhys14']>0.57)
  if (abs(e['eta'])>=1.4 and abs(e['eta'])<2.4):
    return (e['pt']>25 and abs(e['pdgId'])==11 and e['miniRelIso']<0.1 and e['convVeto']==1 and e['sip3d']<4.0 and e['mvaIdPhys14']>0.05)

def getLp(c,e):
  met = c.GetLeaf('met_pt').GetValue()
  metPhi = c.GetLeaf('met_phi').GetValue()
  Lp = e['pt']/sqrt( (e['pt']*cos(e['phi']) + met*cos(metPhi))**2 + (e['pt']*sin(e['phi']) + met*sin(metPhi))**2 )\
       * cos(acos((e['pt']+met*cos(e['phi']-metPhi))/sqrt(e['pt']**2+met**2+2*met*e['pt']*cos(e['phi']-metPhi))))
  return Lp

Bkg = [{'name':'QCD_HT_100To250_PU20bx25', 'sample':QCD_HT_100To250_PU20bx25},
       {'name':'QCD_HT_250To500_PU20bx25', 'sample':QCD_HT_250To500_PU20bx25},
       {'name':'QCD_HT_500To1000_PU20bx25', 'sample':QCD_HT_500To1000_PU20bx25},
       {'name':'QCD_HT_1000ToInf_PU20bx25', 'sample':QCD_HT_1000ToInf_PU20bx25}]
Sig = [{'name':'ttJets_PU20bx25', 'sample':ttJets_PU20bx25, 'prompt':True}]

histos = {}

maxN=5 if small else -1

for sample in Bkg + Sig:
  sample['chunks'], sample['nEvents'] = getChunks(sample['sample'],treeName='treeProducerSusySingleLepton', maxN=maxN)
  sample['chain'] = ROOT.TChain('tree')
  for chunk in sample['chunks']:
    sample['chain'].Add(chunk['file'])

  sample['weight'] = getWeight(sample['sample'], sample['nEvents'], target_lumi)

  histos[sample['name']] = {}
  histos[sample['name']]['mvaIdSEhisto'] = ROOT.TH1F(sample['name']+'_mvaIdSEhisto', sample['name']+'_mvaIdSEhisto',24,-1.2,1.2)
  histos[sample['name']]['mvaIdMEhisto'] = ROOT.TH1F(sample['name']+'_mvaIdMEhisto', sample['name']+'_mvaIdMEhisto',24,-1.2,1.2)
  histos[sample['name']]['mvaIdLEhisto'] = ROOT.TH1F(sample['name']+'_mvaIdLEhisto', sample['name']+'_mvaIdLEhisto',24,-1.2,1.2)
  #histos[sample['name']]['antiSelection'] = ROOT.TH1F(sample['name']+'_antiSelection', sample['name']+'_antiSelection',20,-1.5,2.5)
  #histos[sample['name']]['Selection'] = ROOT.TH1F(sample['name']+'_Selection', sample['name']+'_Selection',20,-1.5,2.5)
  histos[sample['name']]['mvaIdSEhistofake'] = ROOT.TH1F(sample['name']+'_mvaIdSEhistofake', sample['name']+'_mvaIdSEhistofake',24,-1.2,1.2)
  histos[sample['name']]['mvaIdMEhistofake'] = ROOT.TH1F(sample['name']+'_mvaIdMEhistofake', sample['name']+'_mvaIdMEhistofake',24,-1.2,1.2)
  histos[sample['name']]['mvaIdLEhistofake'] = ROOT.TH1F(sample['name']+'_mvaIdLEhistofake', sample['name']+'_mvaIdLEhistofake',24,-1.2,1.2)

  sample["chain"].Draw(">>eList",cut) #Get the event list 'eList' which has all the events satisfying the cut
  elist = ROOT.gDirectory.Get("eList")
  number_events = elist.GetN() #if not small else 1000
  print "Sample ",sample['name'],": Will loop over", number_events,"events"

#leptons = []
#  promptEl = []
#  fakeEl = []
  
  #Event Loop
  for i in range(number_events):
    if i%10000==0:
      print "At %i of %i for sample %s"%(i,number_events,sample['name'])
    sample['chain'].GetEntry(elist.GetEntry(i))
    #print i, getVarValue(cQCD,'nLepGood'), getVarValue(cQCD,'nLepOther')

    eles = [getObjDict(sample['chain'], 'LepGood_', eleVarList, j) for j in range(int(sample['chain'].GetLeaf('nLepGood').GetValue()))]\
         + [getObjDict(sample['chain'], 'LepOther_', eleVarList, j) for j in range(int(sample['chain'].GetLeaf('nLepOther').GetValue()))]

    genEle = [getObjDict(sample['chain'], 'genLep_', eleFromW, j) for j in range(int(sample['chain'].GetLeaf('ngenLep').GetValue()))]

    if i%10000==0:    
      print len(eles), len(genEle)

    eles = filter(lambda e:abs(e['pdgId'])==11, eles) 
    eles = filter(lambda e:e['pt']>25, eles) 
    eles = filter(lambda e:e['miniRelIso']<0.4, eles) #require relIso
    eles = filter(lambda e:abs(e['eta'])<2.4, eles) 

    genEle = filter(lambda e:abs(e['pdgId'])==11, genEle) 
    genEle = filter(lambda e:e['pt']>10, genEle) 

    if sample.has_key('prompt'):
      if sample['prompt']:
        for reco in eles:
          hasMatch=False
          for gen in genEle:
            if getMatch(gen,reco):
#               print "Found match",gen,reco
#              prompt = ele
    #          print 'prompt:',prompt
#              for e in prompt:
               if (abs(reco['eta'])>=1.4 and abs(reco['eta'])<2.4):
                 histos[sample['name']]['mvaIdLEhisto'].Fill(reco['mvaIdPhys14'],sample['weight'])
               elif (abs(reco['eta'])>=0.8 and abs(reco['eta'])<1.4):
                 histos[sample['name']]['mvaIdMEhisto'].Fill(reco['mvaIdPhys14'],sample['weight'])
               elif abs(reco['eta'])<0.8:
                 histos[sample['name']]['mvaIdSEhisto'].Fill(reco['mvaIdPhys14'],sample['weight'])
            hasMatch=True
          if not hasMatch:
            if (abs(reco['eta'])>=1.4 and abs(reco['eta'])<2.4):
              histos[sample['name']]['mvaIdLEhistofake'].Fill(reco['mvaIdPhys14'],sample['weight'])
            elif (abs(reco['eta'])>=0.8 and abs(reco['eta'])<1.4):
              histos[sample['name']]['mvaIdMEhistofake'].Fill(reco['mvaIdPhys14'],sample['weight'])
            elif abs(reco['eta'])<0.8:
              histos[sample['name']]['mvaIdSEhistofake'].Fill(reco['mvaIdPhys14'],sample['weight'])

    else:
      for reco in eles:
        if (abs(reco['eta'])>=1.4 and abs(reco['eta'])<2.4):
          histos[sample['name']]['mvaIdLEhisto'].Fill(reco['mvaIdPhys14'],sample['weight'])
        elif (abs(reco['eta'])>=0.8 and abs(reco['eta'])<1.4):
          histos[sample['name']]['mvaIdMEhisto'].Fill(reco['mvaIdPhys14'],sample['weight'])
        elif abs(reco['eta'])<0.8:
          histos[sample['name']]['mvaIdSEhisto'].Fill(reco['mvaIdPhys14'],sample['weight'])
  
#    antiSelected_e = filter(antiSel, ele)
#    Selected_e = filter(Sel, ele)
#  if len(antiSelected_e)>1: print ele, antiSelected_e
#  if len(Selected_e)>1: print ele, Selected_e
#  if len(antiSelected_e)>1: print len(ele), len(antiSelected_e)
#  print len(ele), len(antiSelected_e), len(Selected_e)
#    if not len(antiSelected_e)==1:continue
#    if not len(Selected_e)==1:continue
  
#    for e in antiSelected_e:
#      antiVal = getLp(sample['chain'],e) 
#      histos[sample['name']]['antiSelection'].Fill(antiVal)
#    for e in Selected_e:
#      selVal = getLp(sample['chain'],e)
#      histos[sample['name']]['Selection'].Fill(selVal)
  
  del elist 

#  print 'Number of anti selected events:',len(antiSelected_e)
#  print 'Number of selected events:',len(Selected_e)

canv = ROOT.TCanvas('canv','canv',600,600)
canv.SetLogy()
l = ROOT.TLegend(0.65,0.75,0.95,0.95)
l.SetFillColor(0)
l.SetBorderSize(1)
l.SetShadowColor(ROOT.kWhite)

text = ROOT.TLatex()
text.SetNDC()
text.SetTextSize(0.045)
text.SetTextAlign(11)
text.DrawLatex(0.15,.96,"CMS Simulation")
text.DrawLatex(0.65,0.96,"L=2 fb^{-1} (13 TeV)")

stackSE = ROOT.THStack('Stacked QCD small eta','Stacked QCD small eta')
stackME = ROOT.THStack('Stacked QCD medium eta','Stacked QCD small eta')
stackLE = ROOT.THStack('Stacked QCD large eta','Stacked QCD large eta')

for b in Bkg:
#  for hist in histos[b['name']]:
#    hist.SetLineWidth(2)
#    hist.GetXaxis().SetTitle('mvaIdPhys14') 
#    hist.GetYaxis().SetTitle('# of Events') 
#    hist.SetMaximum(10*hist.GetMaximum())

  histos[b['name']]['mvaIdSEhisto'].SetLineColor(ROOT.kBlue)
  histos[b['name']]['mvaIdSEhisto'].SetLineWidth(2)
  histos[b['name']]['mvaIdSEhisto'].GetYaxis().SetTitle('# of Events')
  histos[b['name']]['mvaIdMEhisto'].SetLineColor(ROOT.kBlue)
  histos[b['name']]['mvaIdMEhisto'].SetLineWidth(2)
  histos[b['name']]['mvaIdMEhisto'].GetYaxis().SetTitle('# of Events')
  histos[b['name']]['mvaIdLEhisto'].SetLineColor(ROOT.kBlue)
  histos[b['name']]['mvaIdLEhisto'].SetLineWidth(2)
  histos[b['name']]['mvaIdLEhisto'].GetYaxis().SetTitle('# of Events')
  
  if histos[b['name']]['mvaIdSEhisto'].Integral()>1:
    histos[b['name']]['mvaIdSEhisto'].Scale(1./histos[b['name']]['mvaIdSEhisto'].Integral())
  if histos[b['name']]['mvaIdMEhisto'].Integral()>1:
    histos[b['name']]['mvaIdMEhisto'].Scale(1./histos[b['name']]['mvaIdMEhisto'].Integral())
  if histos[b['name']]['mvaIdLEhisto'].Integral()>1:
    histos[b['name']]['mvaIdLEhisto'].Scale(1./histos[b['name']]['mvaIdLEhisto'].Integral())
  
  stackSE.Add(histos[b['name']]['mvaIdSEhisto'])
  l.AddEntry(histos[b['name']]['mvaIdSEhisto'], b['name'], 'l')
  stackME.Add(histos[b['name']]['mvaIdMEhisto'])
#  l.AddEntry(histos[b['name']]['mvaIdMEhisto'], b['name'], 'l')
  stackLE.Add(histos[b['name']]['mvaIdLEhisto'])
#  l.AddEntry(histos[b['name']]['mvaIdLEhisto'], b['name'], 'l')
  
stackSE.Draw()
stackSE.GetXaxis().SetTitle('mvaIdPhys14')
stackSE.GetYaxis().SetTitle('# of Events')# / '+ str( (var['binning'][2] - var['binning'][1])/var['binning'][0])+'GeV')
stackSE.SetMaximum(100*stackSE.GetMaximum())
stackSE.SetMinimum(10**(-2))
#stackME.Draw()
#stackME.GetXaxis().SetTitle('mvaIdPhys14')
#stackME.GetYaxis().SetTitle('# of Events')# / '+ str( (var['binning'][2] - var['binning'][1])/var['binning'][0])+'GeV')
#stackME.SetMaximum(100*stackME.GetMaximum())
#stackME.SetMinimum(10**(-2))
#stackLE.Draw()
#stackLE.GetXaxis().SetTitle('mvaIdPhys14')
#stackLE.GetYaxis().SetTitle('# of Events')# / '+ str( (var['binning'][2] - var['binning'][1])/var['binning'][0])+'GeV')
#stackLE.SetMaximum(100*stackLE.GetMaximum())
#stackLE.SetMinimum(10**(-2))
 
#  histos[b['name']]['mvaIdSEhisto'].Draw()
#  histos[b['name']]['mvaIdMEhisto'].Draw('same')
#  histos[b['name']]['mvaIdLEhisto'].Draw('same')
#  histos[b['name']]['mvaIdSEhisto'].SetMaximum(100*histos[b['name']]['mvaIdSEhisto'].GetMaximum())
#  histos[b['name']]['mvaIdSEhisto'].SetMinimum(10**(-3))
#  histos[b['name']]['mvaIdMEhisto'].SetMaximum(100*histos[b['name']]['mvaIdMEhisto'].GetMaximum())
#  histos[b['name']]['mvaIdLEhisto'].SetMaximum(100*histos[b['name']]['mvaIdLEhisto'].GetMaximum())

#  histos[b['name']]['antiSelection'].SetLineColor(ROOT.kRed)
#  histos[b['name']]['antiSelection'].SetLineWidth(2)
#  histos[b['name']]['antiSelection'].GetYaxis().SetTitle('# of Events')
#  histos[b['name']]['antiSelection'].GetXaxis().SetTitle('L_{p}')
#  histos[b['name']]['Selection'].SetLineColor(ROOT.kBlack)
#  histos[b['name']]['Selection'].SetLineWidth(2)
#  histos[b['name']]['Selection'].GetYaxis().SetTitle('# of Events')
#  histos[b['name']]['Selection'].GetXaxis().SetTitle('L_{P}')
#  l.AddEntry(histos[b['name']]['Selection'], 'selected')
#  l.AddEntry(histos[b['name']]['antiSelection'], 'anti-selected')

#  histos[b['name']]['antiSelection'].Draw()
#  histos[b['name']]['Selection'].Draw('same')
#  histos[b['name']]['antiSelection'].SetMaximum(10*histos[b['name']]['antiSelection'].GetMaximum())
#  histos[b['name']]['Selection'].SetMaximum(10*histos[b['name']]['Selection'].GetMaximum())

for b in Sig:
  histos[b['name']]['mvaIdSEhisto'].SetLineColor(ROOT.kRed)
  histos[b['name']]['mvaIdSEhisto'].SetLineWidth(2)
  histos[b['name']]['mvaIdSEhisto'].GetYaxis().SetTitle('# of Events')
  histos[b['name']]['mvaIdMEhisto'].SetLineColor(ROOT.kRed)
  histos[b['name']]['mvaIdMEhisto'].SetLineWidth(2)
  histos[b['name']]['mvaIdMEhisto'].GetYaxis().SetTitle('# of Events')
  histos[b['name']]['mvaIdLEhisto'].SetLineColor(ROOT.kRed)
  histos[b['name']]['mvaIdLEhisto'].SetLineWidth(2)
  histos[b['name']]['mvaIdLEhisto'].GetYaxis().SetTitle('# of Events')

  if histos[b['name']]['mvaIdSEhisto'].Integral()>1:
    histos[b['name']]['mvaIdSEhisto'].Scale(1./histos[b['name']]['mvaIdSEhisto'].Integral())
  if histos[b['name']]['mvaIdMEhisto'].Integral()>1:
    histos[b['name']]['mvaIdMEhisto'].Scale(1./histos[b['name']]['mvaIdMEhisto'].Integral())
  if histos[b['name']]['mvaIdLEhisto'].Integral()>1:
    histos[b['name']]['mvaIdLEhisto'].Scale(1./histos[b['name']]['mvaIdLEhisto'].Integral())

  histos[b['name']]['mvaIdSEhisto'].Draw('same')
  histos[b['name']]['mvaIdSEhisto'].SetMaximum(100*histos[b['name']]['mvaIdSEhisto'].GetMaximum())
  l.AddEntry(histos[b['name']]['mvaIdSEhisto'], b['name']+' prompt')
  #histos[b['name']]['mvaIdMEhisto'].Draw('same')
  #histos[b['name']]['mvaIdMEhisto'].SetMaximum(100*histos[b['name']]['mvaIdMEhisto'].GetMaximum())
  #l.AddEntry(histos[b['name']]['mvaIdMEhisto'], b['name']+' prompt')
  #histos[b['name']]['mvaIdLEhisto'].Draw('same')
  #histos[b['name']]['mvaIdLEhisto'].SetMaximum(100*histos[b['name']]['mvaIdLEhisto'].GetMaximum())  
  #l.AddEntry(histos[b['name']]['mvaIdLEhisto'], b['name']+' prompt') 

  #plot fakes
  histos[b['name']]['mvaIdSEhistofake'].SetLineColor(ROOT.kRed)
  histos[b['name']]['mvaIdSEhistofake'].SetLineStyle(ROOT.kDashed)
  histos[b['name']]['mvaIdSEhistofake'].SetLineWidth(2)
  histos[b['name']]['mvaIdSEhistofake'].GetYaxis().SetTitle('# of Events')
  histos[b['name']]['mvaIdMEhistofake'].SetLineColor(ROOT.kRed)
  histos[b['name']]['mvaIdMEhistofake'].SetLineStyle(ROOT.kDashed)
  histos[b['name']]['mvaIdMEhistofake'].SetLineWidth(2)
  histos[b['name']]['mvaIdMEhistofake'].GetYaxis().SetTitle('# of Events')
  histos[b['name']]['mvaIdLEhistofake'].SetLineColor(ROOT.kRed)
  histos[b['name']]['mvaIdLEhistofake'].SetLineStyle(ROOT.kDashed)
  histos[b['name']]['mvaIdLEhistofake'].SetLineWidth(2)
  histos[b['name']]['mvaIdLEhistofake'].GetYaxis().SetTitle('# of Events')

  if histos[b['name']]['mvaIdSEhistofake'].Integral()>1:
    histos[b['name']]['mvaIdSEhistofake'].Scale(1./histos[b['name']]['mvaIdSEhistofake'].Integral())
  if histos[b['name']]['mvaIdMEhistofake'].Integral()>1:
    histos[b['name']]['mvaIdMEhistofake'].Scale(1./histos[b['name']]['mvaIdMEhistofake'].Integral())
  if histos[b['name']]['mvaIdLEhistofake'].Integral()>1:
    histos[b['name']]['mvaIdLEhistofake'].Scale(1./histos[b['name']]['mvaIdLEhistofake'].Integral())

  histos[b['name']]['mvaIdSEhistofake'].Draw('same')
  histos[b['name']]['mvaIdSEhistofake'].SetMaximum(100*histos[b['name']]['mvaIdSEhistofake'].GetMaximum())
  l.AddEntry(histos[b['name']]['mvaIdSEhistofake'], b['name']+' fake')
  #histos[b['name']]['mvaIdMEhisto'].Draw('same')
  #histos[b['name']]['mvaIdMEhisto'].SetMaximum(100*histos[b['name']]['mvaIdMEhisto'].GetMaximum())
  #l.AddEntry(histos[b['name']]['mvaIdMEhisto'], b['name']+' fake')
  #histos[b['name']]['mvaIdLEhisto'].Draw('same')
  #histos[b['name']]['mvaIdLEhisto'].SetMaximum(100*histos[b['name']]['mvaIdLEhisto'].GetMaximum())  
  #l.AddEntry(histos[b['name']]['mvaIdLEhisto'], b['name']+' fake') 

l.Draw() 

#canv.cd()
#canv.Print(wwwDir+'mvaId_largeEta.png')
#canv.Print(wwwDir+'mvaId_largeEta.root')
#canv.Print(wwwDir+'mvaId_largeEta.pdf')
