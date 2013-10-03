import ROOT
from math import sqrt, pi
from simplePlotsCommon import *

def getVarValue(c, var, n=0):
  leaf = c.GetAlias(var)
  if leaf!='':
    return c.GetLeaf(leaf).GetValue(n)
  if c.GetLeaf(var):
    return c.GetLeaf(var).GetValue(n)
  else:
    return float('nan')


def goodMuID(c, imu):
  pt                              = getVarValue(c, "muonsPt", imu)
  if pt >= 20.:
    isPF                            = getVarValue(c, "muonsisPF", imu)
    isGlobal                        = getVarValue(c, "muonsisGlobal", imu)
    eta                             = getVarValue(c, "muonsEta", imu)
    eta = abs(eta)
    chi2                            = getVarValue(c, "muonsNormChi2", imu)
    nValMuHits                      = getVarValue(c, "muonsNValMuonHits", imu)
    numMatchedStadions              = getVarValue(c, "muonsNumMatchedStadions", imu)
    numMatchedStations              = getVarValue(c, "muonsNumMatchedStations", imu)
    if not numMatchedStations<float('inf'):
      numMatchedStations = numMatchedStadions
    pixelHits                       = getVarValue(c, "muonsPixelHits", imu)
    numTrackerLayersWithMeasurement  = getVarValue(c, "muonsNumtrackerLayerWithMeasurement", imu)
    dz                              = getVarValue(c, "muonsDz", imu)
    pfDeltaPt                       = getVarValue(c, "muonsPFDeltaPT", imu)
    pfDeltaPt = abs(pfDeltaPt)
#    relIso                          = getVarValue(c, "muonsPFRelIso", imu)    # < 0.12
#    dxy                             = getVarValue(c, "muonsDxy", imu)         # < 0.02, control region: > 0.01 

    return ((eta <= 2.4) and \
      (isPF) and  (isGlobal) and \
      (pfDeltaPt < 5) and \
      (chi2 <= 10) and \
      (nValMuHits > 0) and \
      (numMatchedStations > 1) and \
      (pixelHits > 0) and \
      (numTrackerLayersWithMeasurement > 5) and \
      (dz < 0.5))

  else: return False

def goodEleID(c, iele, eta = "none"):
  if eta=="none": eta   = getVarValue(c, "elesEta", iele)
  eta = abs(eta)
  pt                    = getVarValue(c, "elesPt", iele)
  if pt >= 20.:
    sigmaIEtaIEta         = getVarValue(c, "elesSigmaIEtaIEta", iele)
    DPhi                  = getVarValue(c, "elesDPhi", iele)
    DPhi = abs(DPhi)
    DEta                  = getVarValue(c, "elesDEta", iele)
    DEta = abs(DEta)
    HoE                   = getVarValue(c, "elesHoE", iele)
    oneOverEMinusOneOverP = getVarValue(c, "elesOneOverEMinusOneOverP", iele)
    passConvRejection     = getVarValue(c, "elesPassConversionRejection", iele)
    missingHits           = getVarValue(c, "elesMissingHits", iele)
    dz                    = getVarValue(c, "elesDz", iele)
    pfDeltaPt             = getVarValue(c, "elesPFDeltaPT", iele)
    isBarrel              = eta < 1.4442
    isEndcap              = (eta > 1.566) and (eta < 2.5)
#    print iele, eta, pt, sigmaIEtaIEta, DPhi, DEta, HoE, oneOverEMinusOneOverP, passConvRejection, missingHits, dz, pfDeltaPt, isBarrel, isEndcap

    return ( (eta <= 2.5) and (isBarrel or isEndcap) and \
      (oneOverEMinusOneOverP < 0.05) and \
      (  (isBarrel and (sigmaIEtaIEta < 0.01)) or (isEndcap and (sigmaIEtaIEta < 0.03)) ) and \
      (  (isBarrel and (HoE < 0.12)) or (isEndcap and (HoE < 0.10)) ) and \
      (  (isBarrel and (DPhi < 0.06)) or (isEndcap and (DPhi < 0.03)) ) and \
      (  (isBarrel and (DEta < 0.004)) or (isEndcap and (DEta < 0.007)) ) and \
      ( pfDeltaPt < 10. ) and \
      ( missingHits <= 1 ) and \
      ( dz < 0.1 ) and \
      ( passConvRejection > 0))
  else: return False


def getGoodMuons(c, nmuons):
  res=[]
  for i in range(0, int(nmuons)):
    if goodMuID(c, i):
      relIso      = getVarValue(c, 'muonsPFRelIso', i)
      dxy         = getVarValue(c, 'muonsDxy', i)
      pt          = getVarValue(c, 'muonsPt', i)
      eta         = getVarValue(c, 'muonsEta', i)
      phi         = getVarValue(c, 'muonsPhi', i)
      pdg         = getVarValue(c, 'muonsPdg', i)
      res.append({'relIso'  : relIso,
                  'dxy'     : dxy,
                  'pt'      : pt,
                  'eta'     : eta,
                  'phi'     : phi,
                  'pdg'     : pdg          })
  res = sorted(res, key=lambda k: -k['pt'])
  return res

def getGoodElectrons(c, neles):
  res=[]
  for i in range(0, int(neles)):
    if goodEleID(c, i):
      relIso   = getVarValue(c, 'elesPfRelIso', i)
      dxy      = getVarValue(c, 'elesDxy', i)
      pt       = getVarValue(c, 'elesPt',  i)
      eta      = getVarValue(c, 'elesEta', i)
      phi      = getVarValue(c, 'elesPhi', i)
      pdg      = getVarValue(c, 'elesPdg', i)
      res.append({'relIso'  : relIso,
                  'pt'      : pt,
                  'eta'     : eta,
                  'phi'     : phi,
                  'pdg'     : pdg,
                  'dxy'     : dxy        })
  res= sorted(res, key=lambda k: -k['pt'])
  return res

def getGoodLeptons(c, nmuons, neles ):
  res={}
  res["muons"] = getGoodMuons(c,nmuons)
  res["electrons"] = getGoodElectrons(c, neles)
  leptons = res["muons"] + res["electrons"]
  res["leptons"] = leptons
  return res

def getGoodJets(c, crosscleanobjects):
  njets = getVarValue(c, "nsoftjets")   # jet.pt() > 10.
  res=[]
  bres=[]
  ht = 0.
  nbtags = 0
  for i in range(int(njets)):
    eta = getVarValue(c, "jetsEta", i)
    pt  = getVarValue(c, "jetsPt", i)
    if abs(eta)<=2.4 and getVarValue(c, "jetsID", i) and pt>=40.: # FIXME abs(eta)<3.0 (?)
      phi = getVarValue(c, "jetsPhi", i)
      parton = int(abs(getVarValue(c, "jetsParton", i)))
      jet = {"pt":pt, "eta":eta,"phi":phi, 'pdg':parton}
      isolated = True
      for obj in crosscleanobjects:
        if deltaR(jet, obj)<0.3:  # FIXME <0.4 (?)
          isolated = False
#          print "Not this one!", jet, obj, deltaR(jet, obj)
          break
      if isolated:
        ht+=jet["pt"]
        btag = getVarValue(c, "jetsBtag", i)
        jet["btag"] = btag
        res.append(jet)
        if btag >= 0.679:   # bjets
          bres.append(jet)
          nbtags = nbtags+1

  res= sorted(res, key=lambda k: -k['pt'])
  bres= sorted(bres, key=lambda k: -k['pt'])
  return res, bres, ht, nbtags

def deltaR(l1, l2):
  return sqrt(deltaPhi(l1["phi"], l2["phi"])**2 + (l1["eta"] - l2["eta"])**2)

def deltaPhi( phi1, phi2):
  dphi = phi2-phi1
  if  dphi > pi:
    dphi -= 2.0*pi
  if dphi <= -pi:
    dphi += 2.0*pi
  return abs(dphi)

def myMinDeltaR(c):
  nmuons = getVarValue(c, "nmuons") 
  neles = getVarValue(c, "neles")
  leptons = getGoodLeptons(c, nmuons, neles)
  jets, bjets, ht, nbtags = getGoodJets(c, leptons["leptons"])
#  jets, bjets, ht, nbtags = getGoodJets(c, [])
  deltaRs=[]
  for j in jets:
    for l in leptons["leptons"]:
      deltaRs.append(deltaR(j,l))
  deltaRs.sort()
#  return deltaRs[0]
  if len(deltaRs)>0:
    return deltaRs[0]
  else:
    return -1
#  print "jets", len(jets), "uncl_jets", len(uncl_jets), "leptons", len( leptons["leptons"])

cMC = ROOT.TChain("Events")
cMC.Add("/data/schoef/pat_130517/8TeV-TTJets-powheg-v1+2/histo_100*.root")
small = False
from defaultHad2012Samples import *
cData = ROOT.TChain("Events")
for b in HTdata["bins"]:
  if small:
    print HTdata["dirname"]+"/"+b+"/h*_10*.root"
    cData.Add(HTdata["dirname"]+"/"+b+"/h*_10*.root")
  else:
    print HTdata["dirname"]+"/"+b+"/h*.root"
    cData.Add(HTdata["dirname"]+"/"+b+"/h*.root")

cMC = ROOT.TChain("Events")
if small:
  cMC.Add("/data/schoef/pat_130517/8TeV-TTJets-powheg-v1+2/histo_10*.root")
else:
  cMC.Add("/data/schoef/pat_130517/8TeV-TTJets-powheg-v1+2/histo_*.root")

ROOT.TH1F().SetDefaultSumw2()

commoncf = "nbtags>=2&&type1phiMet>250&&ht>750&&njets>=3&&njets<=5&&(singleMuonic&&nvetoMuons==1&&nvetoElectrons==0||singleElectronic&&nvetoMuons==0&&nvetoElectrons==1)"
h={}
for sample, c in [["TTJets", cMC], ["Data", cData]]:
  h[sample] = ROOT.TH1F(sample, sample, 20,0,2)
  ntot = c.GetEntries()
  c.Draw(">>eList", commoncf)
  elist = ROOT.gDirectory.Get("eList")
  number_events = elist.GetN()
  print sample, "Looping over",number_events,"from", ntot
  for i in range(0, number_events):
    if (i%10000 == 0) and i>0 :
      print i
  #      # Update all the Tuples
    if elist.GetN()>0 and ntot>0:
      c.GetEntry(elist.GetEntry(i))
      h[sample].Fill(myMinDeltaR(c))

del elist

c1 = ROOT.TCanvas()
h['TTJets'].Scale(0.16)
h['TTJets'].SetLineColor(ROOT.kRed)
h['TTJets'].SetMarkerColor(ROOT.kRed)
h['TTJets'].SetMarkerSize(0)
h['TTJets'].Scale(h['Data'].Integral()/h['TTJets'].Integral())
h['Data'].GetXaxis().SetTitle("min #Delta R(l, jets)")
h['Data'].GetYaxis().SetTitle("Number of Events")
h['Data'].Draw()
c1.SetLogy()
h['TTJets'].Draw("histsame")

l = ROOT.TLegend(0.65,0.75,.95,.95)
l.SetFillColor(0)
l.SetBorderSize(1)
l.AddEntry(h['TTJets'], "Simulation")
l.AddEntry(h['Data'],"Data")
l.Draw()
c1.Print("/afs/hephy.at/user/s/schoefbeck/www/etc/leptonDeltaRShapes_HT750_MET250_3-5j_bt2.png")
c1.Print("/afs/hephy.at/user/s/schoefbeck/www/etc/leptonDeltaRShapes_HT750_MET250_3-5j_bt2.pdf")
c1.Print("/afs/hephy.at/user/s/schoefbeck/www/etc/leptonDeltaRShapes_HT750_MET250_3-5j_bt2.root")

#tf = ROOT.TFile("/afs/hephy.at/user/s/schoefbeck/www/etc/leptonDeltaRShapes.root", "recreate")
##tf.cd()
#for k in h.keys():
#  h[k].Write()
#tf.Close()

