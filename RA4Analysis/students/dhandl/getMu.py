import ROOT
import funcs, sys, os
sys.path.insert(0,'/afs/hephy.at/scratch/d/dhandl/CMSSW_5_3_3_patch2/src/Workspace/RA4Analysis/plots')
from defaultMu2012Samples import *
from localConfig import defaultWWWPath

path = os.path.abspath('../../plots')
if not path in sys.path:
    sys.path.insert(1, path)
del path
import eventShape

ROOT.gROOT.ProcessLine('.L ../../../HEPHYCommonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()

cut =  "(singleMuonic&&nvetoMuons==1&&nvetoElectrons==0||singleElectronic&&nvetoElectrons==1&&nvetoMuons==0)&&ht>400&&met>150&&njets>=3"     #cut to use
prefix = 'FirstTry'
metVar = "type1phiMet"

allVariables = []

spher = {'name':'S3D', 'legendName':'Sphericity (3D)', 'binning':[40,0,1]}
circ = {'name':'C3D', 'legendName':'Circularity (3D)', 'binning':[40,0,1]}
circ2D = {'name':'C2D', 'legendName':'Circularity (2D)', 'binning':[40,0,1]}
#fwmt0 = {'name':'FWMT0', 'legendName':'FWM_{0}^{T}', 'binning':[40,0,1]}
fwmt1 = {'name':'FWMT1', 'legendName':'FWM_{1}^{T}', 'binning':[40,0,1]}
fwmt2 = {'name':'FWMT2', 'legendName':'FWM_{2}^{T}', 'binning':[40,0,1]}
fwmt3 = {'name':'FWMT3', 'legendName':'FWM_{3}^{T}', 'binning':[40,0,1]}
fwmt4 = {'name':'FWMT4', 'legendName':'FWM_{4}^{T}', 'binning':[40,0,1]}
circ2DLepMET = {'name':'C2DLepMET', 'legendName':'Circularity (2D)', 'binning':[40,0,1]}
#fwmt0LepMET    = {'name':'FWMT0LepMET', 'legendName':'FWM_{0}^{T}', 'binning':[40,0,1]}
fwmt1LepMET    = {'name':'FWMT1LepMET', 'legendName':'FWM_{1}^{T}', 'binning':[40,0,1]}
fwmt2LepMET    = {'name':'FWMT2LepMET', 'legendName':'FWM_{2}^{T}', 'binning':[40,0,1]}
fwmt3LepMET    = {'name':'FWMT3LepMET', 'legendName':'FWM_{3}^{T}', 'binning':[40,0,1]}
fwmt4LepMET    = {'name':'FWMT4LepMET', 'legendName':'FWM_{4}^{T}', 'binning':[40,0,1]}

allVariables.append(spher)
allVariables.append(circ)
allVariables.append(circ2D)
#allVariables.append(fwmt0)
allVariables.append(fwmt1)
allVariables.append(fwmt2)
allVariables.append(fwmt3)
allVariables.append(fwmt4)
allVariables.append(circ2DLepMET)
#allVariables.append(fwmt0LepMET)
allVariables.append(fwmt1LepMET)
allVariables.append(fwmt2LepMET)
allVariables.append(fwmt3LepMET)
allVariables.append(fwmt4LepMET)

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
    nmuons = funcs.getVarValue(sample['chain'], "nmuons")
    neles = funcs.getVarValue(sample['chain'], "neles")
    #print i+1,". Event: ",nmuons," Muons; ",neles," Electrons"
    #mulist = getGoodMuons(sample['chain'], nmuons)
    #elelist = getGoodElectrons(sample['chain'],neles)
    leplist = funcs.getGoodLeptons(sample['chain'], nmuons, neles)
    allJets, bjets = funcs.getGoodJets(sample['chain'], leplist['leptons'])

    s3D = eventShape.sphericity(allJets)
    c3D = eventShape.circularity(s3D["ev"])
    c2D = eventshape.circularity2D(allJets)
    foxwolfram = eventShape.foxWolframMoments(allJets)
#    print i+1,'.Event:',foxwolfram
    histos[sample['name']]['S3D'].Fill(s3D['sphericity'],sample['weight'])  
    histos[sample['name']]['C3D'].Fill(c3D,sample['weight'])  
    histos[sample['name']]['C2D'].Fill(c2D,sample['weight'])
#    histos[sample['name']]['FWMT0'].Fill(foxwolfram["FWMT0"],sample['weight'])
    histos[sample['name']]['FWMT1'].Fill(foxwolfram["FWMT1"],sample['weight'])
    histos[sample['name']]['FWMT2'].Fill(foxwolfram["FWMT2"],sample['weight'])
    histos[sample['name']]['FWMT3'].Fill(foxwolfram["FWMT3"],sample['weight'])
    histos[sample['name']]['FWMT4'].Fill(foxwolfram["FWMT4"],sample['weight'])

    if len(leplist['leptons'])==1:
      metObj = {"pt":funcs.getVarValue(sample['chain'], metVar), "phi":funcs.getVarValue(sample['chain'], metVar+"phi")}
#      print metObj
      c2DLepMET = funcs.circularity2D(allJets+leplist['leptons']+[metObj])
      foxwolfram = funcs.foxWolframMoments(allJets+leplist['leptons']+[metObj])
  #    print i+1,'.Event:',foxwolfram
      histos[sample['name']]['C2DLepMET'].Fill(c2DLepMET,sample['weight'])
#      histos[sample['name']]['FWMT0LepMET'].Fill(foxwolfram["FWMT0"],sample['weight'])
      histos[sample['name']]['FWMT1LepMET'].Fill(foxwolfram["FWMT1"],sample['weight'])
      histos[sample['name']]['FWMT2LepMET'].Fill(foxwolfram["FWMT2"],sample['weight'])
      histos[sample['name']]['FWMT3LepMET'].Fill(foxwolfram["FWMT3"],sample['weight'])
      histos[sample['name']]['FWMT4LepMET'].Fill(foxwolfram["FWMT4"],sample['weight'])
    
  del elist

#Define and stack the histograms...
for var in allVariables:
  canvas = ROOT.TCanvas(var['name']+' Window',var['name']+' Window')
  l = ROOT.TLegend(0.65,0.75,0.95,0.95)
  l.SetFillColor(0)
  l.SetBorderSize(1)
  l.SetShadowColor(ROOT.kWhite)
#  stack = ROOT.THStack('stack','Stacked Histograms')
#
#  for sample in allSamples:
#    histos[sample['name']][var['name']].SetLineColor(ROOT.kBlack)
#    histos[sample['name']][var['name']].SetFillColor(sample['color'])
#    histos[sample['name']][var['name']].SetMarkerStyle(0)
#    histos[sample['name']][var['name']].GetXaxis().SetTitle(var['legendName'])
#    histos[sample['name']][var['name']].GetYaxis().SetTitle('Number of Events / '+ str( (var['binning'][2] - var['binning'][1])/var['binning'][0]))
#    histos[sample['name']][var['name']].GetXaxis().SetLabelSize(0.04)
#    histos[sample['name']][var['name']].GetYaxis().SetLabelSize(0.04)
#    stack.Add(histos[sample['name']][var['name']])
#    l.AddEntry(histos[sample['name']][var['name']], sample['name'],'f')
#
#  stack.Draw()
#  stack.GetXaxis().SetTitle(var['legendName'])
#  stack.GetYaxis().SetTitle('Number of Events / '+ str( (var['binning'][2] - var['binning'][1])/var['binning'][0]))

  for extra in extraSamples:
    histos[extra['name']][var['name']].SetMarkerStyle(21)
    histos[extra['name']][var['name']].Draw('E')
#    histos[extra['name']][var['name']].Draw('same E') #FIXME
    
    l.AddEntry(histos[extra['name']][var['name']],extra['name'])

  l.Draw()
  canvas.Print(defaultWWWPath+'/pngESV/'+prefix+'_'+var['name']+'.png')
  canvas.Print(defaultWWWPath+'/pngESV/'+prefix+'_'+var['name']+'.root')
  canvas.Print(defaultWWWPath+'/pngESV/'+prefix+'_'+var['name']+'.pdf')
                                 
