import ROOT as r
from ROOT import RooFit as rf
#r.gROOT.ProcessLine(".x load.cc")

h1=r.TF1('f','TMath::Gaus(x,0,0.5)',-1,1.5)
h2=r.TF1('f','TMath::Gaus(x,1,0.5)',-1,1.5)

h12 = r.TH1F("h12","  ",100,-1,1.5)  # Create 'data' (h12)
h1t = r.TH1F("h1t","  ",100,-1,1.5)  # Create scaled MCs (h1t, h2t)
h2t = r.TH1F("h2t","  ",100,-1,1.5)

for i in range(3000):      # Fill 'data' (h12) with one MC template
 life=h1.GetRandom()
 h12.Fill(life)    

for i in range(2000):      # Fill 'data' (h12) with second MC template
 life=h2.GetRandom()
 h12.Fill(life)

for i in range(5000):      # Fill scaled MCs (h1t, h2t)
  life1=h1.GetRandom()
  h1t.Fill(life1)
  life2=h2.GetRandom()
  h2t.Fill(life2)

# Make RooFit histograms from input

x = r.RooRealVar("x","x",-3., 3.)     

data = r.RooDataHist("data","data",r.RooArgList(x),h12)
mc1 =   r.RooDataHist("mc1","scaled mc1",r.RooArgList(x),h1t)
mc2 =   r.RooDataHist("mc2","scaled mc2",r.RooArgList(x),h2t)

mc1_yield = r.RooRealVar("mc1_yield","yield mc1",0.1,0,1)    # These are variables for output
mc2_yield = r.RooRealVar("mc2_yield","yield of mc2",0.1,0,1)   # These are variables for output

# Make PDF from MC histograms
modelmc1=  r.RooHistPdf("modelmc1","modelmc1",r.RooArgSet(x), mc1)
modelmc2=  r.RooHistPdf("modelmc2","modelmc2",r.RooArgSet(x), mc2)

model = r.RooAddPdf ("model","model",r.RooArgList(modelmc1,modelmc2),r.RooArgList(mc1_yield,mc2_yield)) 
                  # Combines my MCs into one PDF model
  

# Plot the imported histogram(s)
dframe = x.frame(rf.Title("Data"))
data.plotOn(dframe)

mc1frame = x.frame(rf.Title("MC Scaled (1)"))
mc1.plotOn(mc1frame)

mc2frame = x.frame(rf.Title("MC Scaled (2)"))
mc2.plotOn(mc2frame)

c = r.TCanvas("roofit_example","RooFit FractionFit Example",800,1200)
c.Divide(1,3)
r.gROOT.SetStyle("Plain") # Removes gray background from plots 
c.cd(1)
r.gPad.SetLeftMargin(0.15)
dframe.GetYaxis().SetTitleOffset(1.4)
dframe.Draw()
c.cd(2)
r.gPad.SetLeftMargin(0.15)
mc1frame.GetYaxis().SetTitleOffset(1.4)
mc1frame.Draw()
c.cd(3)
r.gPad.SetLeftMargin(0.15)
mc2frame.GetYaxis().SetTitleOffset(1.4)
mc2frame.Draw()
  

r.gROOT.SetStyle("Plain")

nll = model.createNLL(data,rf.NumCPU(1))  # From other example, looks like
pll_phi = nll.createProfile(r.RooArgSet(mc1_yield))  # another way of doing the fitTo
  
r.RooMinuit(nll).migrad()
r.RooMinuit(nll).hesse()
r.RooMinuit(nll).minos()  #optional

#model.fitTo(data)    # It is this fitTo command that gives the statistical output

fitFrame=x.frame(rf.Bins(50), rf.Title("Fit Model"))
  
model.paramOn(fitFrame)
data.plotOn(fitFrame, rf.LineColor(r.kRed))
model.plotOn(fitFrame, rf.LineStyle(r.kDashed))
model.plotOn(fitFrame, rf.Components("modelmc1"), rf.LineColor(r.kGreen))
model.plotOn(fitFrame, rf.Components("modelmc2"), rf.LineColor(r.kBlue))

c6 = r.TCanvas("c6","Fit Model",800,1200)
r.gROOT.SetStyle("Plain") # Removes gray background from plots 
r.gPad.SetLeftMargin(0.15)
fitFrame.GetYaxis().SetTitleOffset(1.4)
fitFrame.Draw()
params = model.getParameters(r.RooArgSet(x))


