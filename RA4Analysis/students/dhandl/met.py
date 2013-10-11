import ROOT
ROOT.gROOT.ProcessLine('.L ../../scripts/tdrstyle.C')
ROOT.setTDRStyle()

cut =  "(singleMuonic&&nvetoMuons==1&&nvetoElectrons==0||singleElectronic&&nvetoElectrons==1&&nvetoMuons==0)&&ht>400&&met>150&&njets>=3"     #cut to use
prefix = 'FirstTry'
allVariables = []

met = {'name':'mymet', 'varString':"met", 'legendName':'#slash{E}_{T}', 'binning':[40,0,1000]}
ht = {'name':'myht', 'varString':"ht", 'legendName':'H_{T}', 'binning':[100,0,2500]}
mT = {'name':'mymT', 'varString':"mT", 'legendName':'m_{T}', 'binning':[40,0,1000]}
mt2w = {'name':'mymt2w', 'varString':"mt2w", 'legendName':'m_{T2}^{W}', 'binning':[40,0,1000]}

allVariables.append(met)
allVariables.append(ht)
allVariables.append(mT)
allVariables.append(mt2w)

   #variables to plot
#variable2 = "ht"
#variable3 = "mT"
#variable4 = "mt2w"

def getVarValue(c, var, n=0):         #A general method to get the value of a variable from a chain after chain.GetEntry(i) has been called
  varNameHisto = var
  leaf = var
  #leaf = c.GetAlias(varNameHisto)
  if leaf!='':
    return c.GetLeaf(leaf).GetValue(n)
  else:
    return float('nan')

#Creat Chain with Signals
data = ROOT.TChain("Events")
data.Add("/data/schoef/convertedTuples_v20/copyMET/Mu/data/histo_data.root")
data.Add("/data/schoef/convertedTuples_v20/copyMET/Ele/data/histo_data.root")

#Create Chain with MC
QCD_MC = ROOT.TChain("Events")
QCD_MC.Add("/data/schoef/convertedTuples_v20/copyMET/Mu/QCD/histo_QCD.root")
QCD_MC.Add("/data/schoef/convertedTuples_v20/copyMET/Ele/QCD/histo_QCD.root")

SINGLETOP_MC = ROOT.TChain("Events")
SINGLETOP_MC.Add("/data/schoef/convertedTuples_v20/copyMET/Mu/singleTop/histo_singleTop.root")
SINGLETOP_MC.Add("/data/schoef/convertedTuples_v20/copyMET/Ele/singleTop/histo_singleTop.root")

WJETSCOMBINED_MC = ROOT.TChain("Events")
WJETSCOMBINED_MC.Add("/data/schoef/convertedTuples_v20/copyMET/Mu/WJetsCombined/histo_WJetsCombined.root")
WJETSCOMBINED_MC.Add("/data/schoef/convertedTuples_v20/copyMET/Ele/WJetsCombined/histo_WJetsCombined.root")

TTJETSPOWHEG_MC = ROOT.TChain("Events")
TTJETSPOWHEG_MC.Add("/data/schoef/convertedTuples_v20/copyMET/Mu/TTJets-PowHeg/histo_TTJets-PowHeg.root")
TTJETSPOWHEG_MC.Add("/data/schoef/convertedTuples_v20/copyMET/Ele/TTJets-PowHeg/histo_TTJets-PowHeg.root")

#Define two samples; I used dicts. Adapt as you need.
data        = {"name":"Data",          "chain":data,                    "weight":1,        "color":ROOT.kBlack}
qcd_mc      = {"name":"QCD",           "chain":QCD_MC,                  "weight":"weight", "color":ROOT.kBlue}
singletop_mc     = {"name":"singleTop",     "chain":SINGLETOP_MC,            "weight":"weight", "color":ROOT.kGreen}
wjetscombined_mc = {"name":"WJetsCombined", "chain":WJETSCOMBINED_MC,        "weight":"weight", "color":ROOT.kRed}
ttjetspowheg_mc  = {"name":"TTJets-PowHeg", "chain":TTJETSPOWHEG_MC,         "weight":"weight", "color":ROOT.kYellow}

allMCSamples = [qcd_mc,singletop_mc,wjetscombined_mc,ttjetspowheg_mc]
extraSamples = [data]

histos = {}
 
for sample in allMCSamples + extraSamples: #Loop over samples
  histos[sample['name']] = {}
  
  for var in allVariables:
    histos[sample['name']][var['name']] = ROOT.TH1F(sample['name']+'_'+var['name'], sample['name']+'_'+var['name'], *var['binning'])
  
  sample["chain"].Draw(">>eList", cut) #Get the event list 'eList' which has all the events satisfying the cut
  elist = ROOT.gDirectory.Get("eList")
  number_events = elist.GetN()
  print "Sample ",sample["name"],": Will loop over", number_events,"events" #Number of events satisfying the cut
  
  for i in range(number_events): #Loop over those events
    sample["chain"].GetEntry(elist.GetEntry(i))  #Set the chain to the current event (it's the i-th event of the eList). This is the central line in this file!
    for var in allVariables:
      varValue = getVarValue(sample["chain"], var['varString'])   #Get the value of the variable
      weight = 1
      if sample.has_key('weight'):
        if type(sample['weight'])==type(''):
          weight = getVarValue(sample['chain'], sample['weight'])
        else:
          weight = sample['weight']
      histos[sample['name']][var['name']].Fill(varValue, weight)
  del elist

#Define and stack the histograms...
for var in allVariables:
  canvas = ROOT.TCanvas(var['name']+' Window',var['name']+' Window')
  canvas.SetLogy()
  l = ROOT.TLegend(0.65,0.75,0.95,0.95)
  l.SetFillColor(0)
  l.SetBorderSize(1)
  l.SetShadowColor(ROOT.kWhite)
  stack = ROOT.THStack('stack','Stacked Histograms')

  for sample in allMCSamples: 
    histos[sample['name']][var['name']].SetLineColor(ROOT.kBlack)
    histos[sample['name']][var['name']].SetFillColor(sample['color'])
    histos[sample['name']][var['name']].SetMarkerStyle(0)
    histos[sample['name']][var['name']].GetXaxis().SetTitle(var['legendName'])
    histos[sample['name']][var['name']].GetYaxis().SetTitle('Number of Events / '+ str( (var['binning'][2] - var['binning'][1])/var['binning'][0])+' GeV')
    histos[sample['name']][var['name']].GetXaxis().SetLabelSize(0.04)
    histos[sample['name']][var['name']].GetYaxis().SetLabelSize(0.04)
    stack.Add(histos[sample['name']][var['name']])
    l.AddEntry(histos[sample['name']][var['name']], sample['name'])

  stack.Draw()
  stack.GetXaxis().SetTitle(var['legendName'])
  stack.GetYaxis().SetTitle('Number of Events / '+ str( (var['binning'][2] - var['binning'][1])/var['binning'][0])+' GeV')

  for extra in extraSamples:
    histos[extra['name']][var['name']].SetMarkerStyle(21)
    histos[extra['name']][var['name']].Draw('same E')
    l.AddEntry(histos[extra['name']][var['name']],extra['name'])
  
  l.Draw()
  canvas.Print('/afs/hephy.at/user/d/dhandl/www/png/'+prefix+'_'+var['name']+'.png')
  canvas.Print('/afs/hephy.at/user/d/dhandl/www/png/'+prefix+'_'+var['name']+'.root')
  canvas.Print('/afs/hephy.at/user/d/dhandl/www/png/'+prefix+'_'+var['name']+'.pdf')
 
#l = ROOT.TLegend(0.7,0.8,1.0,1.0)
#l.SetFillColor(0)
#l.SetShadowColor(ROOT.kWhite)
#l.SetBorderSize(0)

#stack = ROOT.THStack("stack","Stacked Backgrounds")

#for i, sample in enumerate(allMCSamples):
#  sample["histo"].SetLineColor(ROOT.kBlack)
#  sample["histo"].SetFillColor(sample["color"])
#  sample["histo"].SetMarkerStyle(0)
#  sample["histo"].GetXaxis().SetTitle(variable)
#  sample["histo"].GetYaxis().SetTitle("Events / "+str( (binning[2] - binning[1])/binning[0])+" GeV")
#  sample["histo"].GetXaxis().SetLabelSize(0.04)
#  sample["histo"].GetYaxis().SetLabelSize(0.04)
#  stack.Add(sample["histo"])
#  l.AddEntry(sample["histo"], sample["name"])
#
#stack.Draw()
#stack.GetXaxis().SetTitle("#slash{E}_{T} [GeV]")
#stack.GetYaxis().SetTitle("Number of Events / "+str( (binning[2] - binning[1])/binning[0])+" GeV")
#
#for i, signal in enumerate(extraSamples):
#  signal['histo'].SetMarkerStyle(21)
#  signal['histo'].Draw('same E')
#  l.AddEntry(signal['histo'], signal['name'])

#l.Draw()

