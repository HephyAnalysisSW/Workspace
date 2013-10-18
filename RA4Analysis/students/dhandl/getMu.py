import ROOT
import funcs,sys,os
sys.path.insert(0,'/afs/hephy.at/scratch/d/dhandl/CMSSW_5_3_3_patch2/src/Workspace/RA4Analysis/plots')
from defaultMu2012Samples import *

ROOT.gROOT.ProcessLine('.L ../../scripts/tdrstyle.C')
ROOT.setTDRStyle()

#cut = "ht>400&&met>150"
cut =  "(singleMuonic&&nvetoMuons==1&&nvetoElectrons==0||singleElectronic&&nvetoElectrons==1&&nvetoMuons==0)&&ht>400&&met>150&&njets>=3"     #cut to use
prefix = 'FirstTry'

allVariables = []

spher = {'name':'mysphericity', 'legendName':'Sphericity', 'binning':[40,0,1]}
circ = {'name':'mycircularity', 'legendName':'Circularity', 'binning':[40,0,1]}
circ2D = {'name':'mycircularity2D', 'legendName':'2D Circularity', 'binning':[40,0,1]}
ht0 = {'name':'myHT0', 'legendName':'H_{0}^{T}', 'binning':[40,0,1]}
ht1 = {'name':'myHT1', 'legendName':'H_{1}^{T}', 'binning':[40,0,1]}
ht2 = {'name':'myHT2', 'legendName':'H_{2}^{T}', 'binning':[40,0,1]}
ht3 = {'name':'myHT3', 'legendName':'H_{3}^{T}', 'binning':[40,0,1]}
ht4 = {'name':'myHT4', 'legendName':'H_{4}^{T}', 'binning':[40,0,1]}

allVariables.append(spher)
allVariables.append(circ)
allVariables.append(circ2D)
allVariables.append(ht0)
allVariables.append(ht1)
allVariables.append(ht2)
allVariables.append(ht3)
allVariables.append(ht4)

#Creat Chain with Samples
DATA = ROOT.TChain("Events")
DATA.Add("/data/mhickel/pat_130412/MuHad-Run2012A-13Jul2012/histo_*.root")
#DATA.Add("/data/mhickel/pat_130412/MuHad-Run2012B-13Jul2012/histo_*.root")
#DATA.Add("/data/mhickel/pat_130412/MuHad-Run2012C-Aug24ReReco/histo_*.root")
#DATA.Add("/data/mhickel/pat_130412/MuHad-Run2012C-PromptReco-v2/histo_*.root")
#DATA.Add("/data/mhickel/pat_130412/MuHad-Run2012D-PromptReco/histo_*.root")

#QCD = ROOT.TChain('Events')                         #create chain for every bin
#QCD.Add('/data/schoef/pat_130517/8TeV-QCD-Pt1000-MuEnrichedPt5/histo_*.root')     #Add root-files to chain

#QCD1 = ROOT.TChain('Events')                         #create chain for every bin
#QCD1.Add('/data/schoef/pat_130517/8TeV-QCD-Pt120to170-MuEnrichedPt5/histo_*.root')     #Add root-files to chain

#QCD2 = ROOT.TChain('Events')                         #create chain for every bin
#QCD2.Add('/data/schoef/pat_130517/8TeV-QCD-Pt170to300-MuEnrichedPt5/histo_*.root')     #Add root-files to chain

#QCD3 = ROOT.TChain('Events')                         #create chain for every bin
#QCD3.Add('/data/schoef/pat_130517/8TeV-QCD-Pt20to30-MuEnrichedPt5/histo_*.root')     #Add root-files to chain

#Define two samples; I used dicts. Adapt as you need.
data        = {"name":"Data",          "chain":DATA,                "weight":1,        "color":ROOT.kBlack}
#qcd  = {'name':'8TeV-QCD-Pt1000-MuEnrichedPt5', 'chain':QCD,  'weight':0.000219628708966,  'color':ROOT.kBlue}
#qcd1  ={'name':'8TeV-QCD-Pt120to170-MuEnrichedPt5', 'chain':QCD1,  'weight': 8.828953617457433,  'color':ROOT.kBlue+1}
#qcd2  ={'name':'8TeV-QCD-Pt170to300-MuEnrichedPt5', 'chain':QCD2,  'weight': 3.0172762943641565, 'color':ROOT.kBlue+2}
#qcd3  ={'name':'8TeV-QCD-Pt20to30-MuEnrichedPt5', 'chain':QCD3,  'weight':2202.2442941154804,  'color':ROOT.kBlue+3}
#QCD-Pt300to470-MuEnrichedPt5_mc  ={'name':'8TeV-QCD-Pt300to470-MuEnrichedPt5', 'chain':8TeV-QCD-Pt300to470-MuEnrichedPt5,  'weight':0.19521566984441494,  'color':ROOT.kBlue+4}
#QCD-Pt30to50-MuEnrichedPt5_mc  ={'name':'8TeV-QCD-Pt30to50-MuEnrichedPt5', 'chain':8TeV-QCD-Pt30to50-MuEnrichedPt5,  'weight':844.79842083177698,  'color':ROOT.kBlue-1}
#QCD-Pt470to600-MuEnrichedPt5_mc  ={'name':'8TeV-QCD-Pt470to600-MuEnrichedPt5', 'chain':8TeV-QCD-Pt470to600-MuEnrichedPt5,  'weight':0.031718905995021876,  'color':ROOT.kBlue-2}
#QCD-Pt50to80-MuEnrichedPt5_mc  ={'name':'8TeV-QCD-Pt50to80-MuEnrichedPt5', 'chain':8TeV-QCD-Pt50to80-MuEnrichedPt5,  'weight':170.373930373853,  'color':ROOT.kBlue-3}
#QCD-Pt600to800-MuEnrichedPt5_mc  ={'name':'8TeV-QCD-Pt600to800-MuEnrichedPt5', 'chain':8TeV-QCD-Pt600to800-MuEnrichedPt5,  'weight':0.0066737682957082609,  'color':ROOT.kBlue-4}
#QCD-Pt800to1000-MuEnrichedPt5_mc  ={'name':'8TeV-QCD-Pt800to1000-MuEnrichedPt5', 'chain':8TeV-QCD-Pt800to1000-MuEnrichedPt5,  'weight':0.00089949810395640998,  'color':ROOT.kBlue-5}
#QCD-Pt80to120-MuEnrichedPt5_mc  ={'name':'8TeV-QCD-Pt80to120-MuEnrichedPt5', 'chain':8TeV-QCD-Pt80to120-MuEnrichedPt5,  'weight':44.048325089881537,  'color':ROOT.kBlue-6}

# '8TeV-T-s': 0.14579109943414589,
# '8TeV-T-t': 5.6470022828307105,
# '8TeV-T-tW': 0.2230447415695116,
# '8TeV-TTJets-powheg-v1+2': 0.08011071077752073,
# '8TeV-Tbar-s': 0.12573763698972668,
# '8TeV-Tbar-t': 0.15865042747763392,
# '8TeV-Tbar-tW': 0.2249422445588295,
# '8TeV-WJets-HT250to300': 0.29371423397541391,
# '8TeV-WJets-HT300to400': 0.22536225658816841,
# '8TeV-WJets-HT400': 0.1544579365473078,
# '8TeV-WJetsToLNu': 8.077162147717976}

allSamples = []
#allSamples.append(qcd)
#allSamples.append(qcd1)
#allSamples.append(qcd2)
#allSamples.append(qcd3)
#allSamples.append(8TeV-QCD-Pt300to470-MuEnrichedPt5_mc)
#allSamples.append(8TeV-QCD-Pt30to50-MuEnrichedPt5_mc)
#allSamples.append(8TeV-QCD-Pt470to600-MuEnrichedPt5_mc)
#allSamples.append(8TeV-QCD-Pt50to80-MuEnrichedPt5_mc)
#allSamples.append(8TeV-QCD-Pt600to800-MuEnrichedPt5_mc)
#allSamples.append(8TeV-QCD-Pt800to1000-MuEnrichedPt5_mc)
#allSamples.append(8TeV-QCD-Pt80to120-MuEnrichedPt5_mc)

extraSamples = [data]

histos = {}

for sample in extraSamples + allSamples: #Loop over samples
  histos[sample['name']] = {} 

  for var in allVariables:
    histos[sample['name']][var['name']] = ROOT.TH1F(sample['name']+'_'+var['name'], sample['name']+'_'+var['name'], *var['binning'])
  
  sample["chain"].Draw(">>eList", cut) #Get the event list 'eList' which has all the events satisfying the cut
  elist = ROOT.gDirectory.Get("eList")
  number_events = elist.GetN()
  print "Sample ",sample["name"],": Will loop over", number_events,"events" #Number of events satisfying the cut
  
  for i in range(number_events): #Loop over those events
    sample["chain"].GetEntry(elist.GetEntry(i))  #Set the chain to the current event (it's the i-th event of the eList). This is the central line in this file!
    nmuons = getVarValue(sample['chain'], "nmuons")
    neles = getVarValue(sample['chain'], "neles")
    #print i+1,". Event: ",nmuons," Muons; ",neles," Electrons"
    #mulist = getGoodMuons(sample['chain'], nmuons)
    #elelist = getGoodElectrons(sample['chain'],neles)
    leplist = getGoodLeptons(sample['chain'], nmuons, neles)
    jetlist = getGoodJets(sample['chain'], leplist['leptons'])

#    weight = 1
#    if sample.has_key('weight'):
#      if type(sample['weight'])==type(''):
#        weight = getVarValue(sample['chain'], sample['weight'])
#      else:
#        weight = sample['weight']

    s = sphericity(jetlist[0])
    c = circularity(s)
    c2D = circularity2D(jetlist[0])
    foxwolfram = HT(jetlist[0])

#    print i+1,'.Event:',foxwolfram
    histos[sample['name']]['mysphericity'].Fill(s[0],sample['weight'])  
    histos[sample['name']]['mycircularity'].Fill(c,sample['weight'])  
    histos[sample['name']]['mycircularity2D'].Fill(c2D,sample['weight'])
    histos[sample['name']]['myHT0'].Fill(foxwolfram[0],sample['weight'])
    histos[sample['name']]['myHT1'].Fill(foxwolfram[1],sample['weight'])
    histos[sample['name']]['myHT2'].Fill(foxwolfram[2],sample['weight'])
    histos[sample['name']]['myHT3'].Fill(foxwolfram[3],sample['weight'])
    histos[sample['name']]['myHT4'].Fill(foxwolfram[4],sample['weight'])
    
  del elist

#Define and stack the histograms...
for var in allVariables:
  canvas = ROOT.TCanvas(var['name']+' Window',var['name']+' Window')
  l = ROOT.TLegend(0.65,0.75,0.95,0.95)
  l.SetFillColor(0)
  l.SetBorderSize(1)
  l.SetShadowColor(ROOT.kWhite)
#  stack = ROOT.THStack('stack','Stacked Histograms')

  for sample in allSamples:
    histos[sample['name']][var['name']].SetLineColor(ROOT.kBlack)
    histos[sample['name']][var['name']].SetFillColor(sample['color'])
    histos[sample['name']][var['name']].SetMarkerStyle(0)
    histos[sample['name']][var['name']].GetXaxis().SetTitle(var['legendName'])
    histos[sample['name']][var['name']].GetYaxis().SetTitle('Number of Events / '+ str( (var['binning'][2] - var['binning'][1])/var['binning'][0]))
    histos[sample['name']][var['name']].GetXaxis().SetLabelSize(0.04)
    histos[sample['name']][var['name']].GetYaxis().SetLabelSize(0.04)
    stack.Add(histos[sample['name']][var['name']])
    l.AddEntry(histos[sample['name']][var['name']], sample['name'],'f')

#  stack.Draw()
#  stack.GetXaxis().SetTitle(var['legendName'])
#  stack.GetYaxis().SetTitle('Number of Events / '+ str( (var['binning'][2] - var['binning'][1])/var['binning'][0]))

  for extra in extraSamples:
    histos[extra['name']][var['name']].SetMarkerStyle(21)
    histos[extra['name']][var['name']].Draw('same E')
    
    l.AddEntry(histos[extra['name']][var['name']],extra['name'])

  l.Draw()
#  canvas.Print('/afs/hephy.at/user/d/dhandl/www/esv/'+prefix+'_'+var['name']+'.png')
#  canvas.Print('/afs/hephy.at/user/d/dhandl/www/esv/'+prefix+'_'+var['name']+'.root')
#  canvas.Print('/afs/hephy.at/user/d/dhandl/www/esv/'+prefix+'_'+var['name']+'.pdf')
                                 
