import ROOT

variable = "met"	 #variable to plot
cut =	"(singleMuonic&&nvetoMuons==1&&nvetoElectrons==0||singleElectronic&&nvetoElectrons==1&&nvetoMuons==0)&&ht>400&&met>150&&njets>=3"		 #cut to use
#cut =	"(singleMuonic OR singleElectronic)&&ht>400&&met>150&&nbtags>=2"		 #cut to use
binning = [40,0,1000]		 #binning

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
data	   	 = {"name":"Data",          "chain":data,                  "histo":ROOT.TH1F("data",     "data", *binning),   "weight":1,         "color":ROOT.kBlack}
qcd_mc   	 = {"name":"QCD",           "chain":QCD_MC,                "histo":ROOT.TH1F("metMC",    "metMC", *binning),   "weight":"weight", "color":ROOT.kBlue}
singletop_mc     = {"name":"singleTop",     "chain":SINGLETOP_MC,          "histo":ROOT.TH1F("metMC",    "metMC", *binning),   "weight":"weight", "color":ROOT.kGreen}
wjetscombined_mc = {"name":"WJetsCombined", "chain":WJETSCOMBINED_MC,      "histo":ROOT.TH1F("metMC",    "metMC", *binning),   "weight":"weight", "color":ROOT.kRed}
ttjetspowheg_mc  = {"name":"TTJets-PowHeg", "chain":TTJETSPOWHEG_MC,       "histo":ROOT.TH1F("metMC",    "metMC", *binning),   "weight":"weight", "color":ROOT.kYellow}

allMCSamples = [qcd_mc,singletop_mc,wjetscombined_mc,ttjetspowheg_mc]
allSignals = []

for sample in allMCSamples + [data] + allSignals: #Loop over samples
  sample["chain"].Draw(">>eList", cut) #Get the event list 'eList' which has all the events satisfying the cut
  elist = ROOT.gDirectory.Get("eList")
  number_events = elist.GetN()
  print "Sample ",sample["name"],": Will loop over", number_events,"events" #Number of events satisfying the cut
  for i in range(number_events): #Loop over those events
#    if i>0 and (i%10000)==0:
#      print "Filled",i
    sample["chain"].GetEntry(elist.GetEntry(i))  #Set the chain to the current event (it's the i-th event of the eList). This is the central line in this file!
    varValue = getVarValue(sample["chain"], variable)   #Get the value of the variable
    weight = 1
    if sample.has_key('weight'):
	if type(sample['weight'])==type(''):
	  weight = getVarValue(sample['chain'], sample['weight'])
        else:
	  weight = sample['weight']
    sample["histo"].Fill(varValue, weight) #Fill the histo
  del elist

#Define and stack the histograms ...
c1 = ROOT.TCanvas()
c1.SetLogy()
l = ROOT.TLegend(0.7,0.8,1.0,1.0)
l.SetFillColor(0)
l.SetShadowColor(ROOT.kWhite)
l.SetBorderSize(0)

stack = ROOT.THStack("stack","Stacked Backgrounds")

for i, sample in enumerate(allMCSamples):
  sample["histo"].SetLineColor(ROOT.kBlack)
  sample["histo"].SetFillColor(sample["color"])
  sample["histo"].SetMarkerStyle(0)
  sample["histo"].GetXaxis().SetTitle(variable)
  sample["histo"].GetYaxis().SetTitle("Events / "+str( (binning[2] - binning[1])/binning[0])+" GeV")
  sample["histo"].GetXaxis().SetLabelSize(0.04)
  sample["histo"].GetYaxis().SetLabelSize(0.04)
  stack.Add(sample["histo"])
#  if i==0:
#    sample["histo"].Draw()
#  else:
#    sample["histo"].Draw("same")
  l.AddEntry(sample["histo"], sample["name"])

stack.Draw()
stack.GetXaxis().SetTitle("#xout{E}_{T}")
stack.GetYaxis().SetTitle("Number of Events / "+str( (binning[2] - binning[1])/binning[0])+" GeV")

#for i, sample in enumerate(allSignals)
  #sample['histo']...

data['histo'].SetMarkerStyle(21)
data['histo'].Draw('same E')
l.AddEntry(data['histo'], data['name'])

l.Draw()

