import ROOT
from simplePlotsCommon import *
from simpleStatTools import niceNum
from math import *

ROOT.tdrStyle.SetPadRightMargin(0.16)
ROOT.gROOT.ProcessLine(".L ../../HEPHYCommonTools/scripts/root/useNiceColorPalette.C")
ROOT.useNiceColorPalette(255)

small = False
mode = "Mu"

print "Constructing MET templates and MET projection templates"

doubleMu = ROOT.TChain("Events")
if small:
  doubleMu.Add("/data/schoef/pat_120125/DoubleMu/Run2011B-Prompt-v1/histo_1*.root")
else:
  doubleMu.Add("/data/schoef/pat_120125/DoubleMu/Run2011A-Aug5ReReco-v1/*.root")
  doubleMu.Add("/data/schoef/pat_120125/DoubleMu/Run2011A-May10ReReco/*.root")
  doubleMu.Add("/data/schoef/pat_120125/DoubleMu/Run2011A-Prompt-v4/*.root")
  doubleMu.Add("/data/schoef/pat_120125/DoubleMu/Run2011A-Prompt-v6/*.root")
  doubleMu.Add("/data/schoef/pat_120125/DoubleMu/Run2011B-Prompt-v1/*.root")
doubleMu_commoncf  = "ngoodMuons>1" 

#oneLepFromDataMETHT =  ROOT.TH2F("oneLepFromDataMETHT",  "oneLepFromDataMETHT",  20,0,1000, 20,0,2000) 
#oneLepFromDataMETHT.GetXaxis().SetTitle("#slash{E}_{T} (GeV)")
#oneLepFromDataMETHT.GetYaxis().SetTitle("H_{T} (GeV)")

nvtxBinning = [[-1,-1], [0,5], [5,10], [5,15], [15,20], [20,25], [25, -1]]
ptZBinning = [[-1,-1]]
zMax = 100
zBins = 10
for ptZ in range(0, zMax, zBins):
  ptZBinning.append([ptZ, ptZ+zMax/zBins])
  
met_nvtx={}
metPerp_nvtx={}
metPar_nvtx={}
resolutionPerp = {}
resolutionPar = {}
for bin in nvtxBinning:
  resolutionPerp[tuple(bin)] = ROOT.TH1F("resPerp_nvtx"+str(bin[0])+"_"+str(bin[1]), "resPerp_nvtx"+str(bin[0])+"_"+str(bin[1]), zMax/zBins, 0, zMax)
  resolutionPar [tuple(bin)] = ROOT.TH1F("resPar_nvtx"+str(bin[0])+"_"+str(bin[1]), "resPar_nvtx"+str(bin[0])+"_"+str(bin[1]), zMax/zBins, 0, zMax)
  met_nvtx[tuple(bin)] = {}
  metPerp_nvtx[tuple(bin)] = {}
  metPar_nvtx[tuple(bin)] = {}
  for ptZ in ptZBinning: 
#    met_nvtx[tuple(bin)][tuple(ptZ)] = ROOT.TH1F("met_nvtx"+str(bin[0])+"_"+str(bin[1])+"_ptZ_"+str(ptZ[0]), "met_nvtx"+str(bin[0])+"_"+str(bin[1])+"_ptZ_"+str(ptZ[0]), 100,-500,500)
    metPerp_nvtx[tuple(bin)][tuple(ptZ)] = ROOT.TH1F("metPerp_nvtx"+str(bin[0])+"_"+str(bin[1])+"_ptZ_"+str(ptZ[0]), "metPerp_nvtx"+str(bin[0])+"_"+str(bin[1])+"_ptZ_"+str(ptZ[0]), 100,-200,200)
    metPar_nvtx[tuple(bin)][tuple(ptZ)] = ROOT.TH1F("metPar_nvtx"+str(bin[0])+"_"+str(bin[1])+"_ptZ_"+str(ptZ[0]), "metPar_nvtx"+str(bin[0])+"_"+str(bin[1])+"_ptZ_"+str(ptZ[0]), 100,-200,200)
  

ntot = doubleMu.GetEntries()
doubleMu.Draw(">>eList", doubleMu_commoncf)
elist = ROOT.gDirectory.Get("eList")
number_events = elist.GetN()
print "nevents:", number_events
if small:
  if number_events>200:
    number_events=200
for i in range(0, number_events):
  if (i%10000 == 0) and i>0 :
    print i
#      # Update all the Tuples
  if elist.GetN()>0 and ntot>0:
    doubleMu.GetEntry(elist.GetEntry(i))
    leptonPt = getValue(doubleMu,"leptonPt")
    leptonPhi = getValue(doubleMu,"leptonPhi")
    leptonEta = getValue(doubleMu,"leptonEta")
    lepton2Pt = getValue(doubleMu,"lepton2Pt")
    lepton2Phi = getValue(doubleMu,"lepton2Phi")
    lepton2Eta = getValue(doubleMu,"lepton2Eta")
    px = leptonPt*cos(leptonPhi)
    py = leptonPt*sin(leptonPhi)
    pz = leptonPt*sinh(leptonEta)
    E = sqrt(px**2+py**2+pz**2)
    p2x = lepton2Pt*cos(lepton2Phi)
    p2y = lepton2Pt*sin(lepton2Phi)
    p2z = lepton2Pt*sinh(lepton2Eta)
    E2 = sqrt(p2x**2+p2y**2+p2z**2)
    mZ = sqrt((E+E2)**2 - (px+p2x)**2 - (py+p2y)**2 - (pz+p2z)**2)
    
    zx = px + p2x
    zy = py + p2y
    zt = sqrt(zx*zx+zy*zy)
    metx = getValue(doubleMu,"metpxUncorr") 
    mety = getValue(doubleMu,"metpyUncorr")
    metPar = (zx*metx + zy*mety)/zt
    metPerp = (-zy*metx + zx*mety)/zt
    ngoodVertices = getValue(doubleMu,"ngoodVertices") 
     
    if abs((mZ-91.2)) < 15.:
      for bin in nvtxBinning:
        if bin[0]<0 or ngoodVertices>=bin[0]:
          if bin[1]<0 or ngoodVertices<bin[1]:
            for ptZbin in ptZBinning:
              if ptZbin[0]<0 or zt>=ptZbin[0]:
                if ptZbin[1]<0 or zt<ptZbin[1]:
                  metPerp_nvtx[tuple(bin)][tuple(ptZbin)].Fill(metPerp)
                  metPar_nvtx[tuple(bin)][tuple(ptZbin)].Fill(metPar)
del elist
metPerp_nvtx[tuple(nvtxBinning[0])][tuple(ptZBinning[0])].Draw()
metPar_nvtx[tuple(nvtxBinning[0])][tuple(ptZBinning[0])].Draw("same")

for nvtx in metPerp_nvtx.keys():
   for nptz in metPerp_nvtx[nvtx].keys():
      if metPerp_nvtx[nvtx][nptz].Integral()>10:
        fitres = metPerp_nvtx[nvtx][nptz].Fit("gaus", "S")
  #      if fitres.isValid():
        h = resolutionPerp[nvtx]
        h.SetBinContent(h.FindBin(nptz[0]), fitres.Parameter(2))
        h.SetBinError(h.FindBin(nptz[0]), fitres.ParError(2))
        h.SetLineColor(ROOT.kBlue)
        h.SetMarkerColor(ROOT.kBlue)
      if metPar_nvtx[nvtx][nptz].Integral()>10:
        fitres = metPar_nvtx[nvtx][nptz].Fit("gaus", "S")
  #      if fitres.isValid():
        h = resolutionPar[nvtx]
        h.SetBinContent(h.FindBin(nptz[0]), fitres.Parameter(2))
        h.SetBinError(h.FindBin(nptz[0]), fitres.ParError(2))

resolutionPar[tuple([-1,-1])].Draw()
resolutionPerp[tuple([-1,-1])].Draw("same")

