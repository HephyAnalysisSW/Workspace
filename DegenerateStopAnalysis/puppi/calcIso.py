from DataFormats.FWLite import Events, Handle
from PhysicsTools.PythonAnalysis import *
from math import * 
import ROOT

filelist=[]
filelist.append('histo.root')

events = Events(filelist)
events.toBegin()
c = ROOT.TChain('Events')
for f in filelist:
  c.Add(f)

pfLabel = ("packedPFCandidates")
pfHandle = Handle("vector<pat::PackedCandidate>")
gpLabel = ("packedGenParticles")
gpHandle = Handle("vector<pat::PackedGenParticle>")
puppiLabel = ("puppi","Puppi")
puppiHandle = Handle("vector<reco::PFCandidate>")
pfMetLabel = ("pfMet")
pfMetHandle = Handle("vector<reco::PFMET>")
pfMetPuppiLabel = ("pfMetPuppi")
pfMetPuppiHandle = Handle("vector<reco::PFMET>")





#isoCands = [{'c':cand,'iso':0.} for cand in filter(lambda c:c.pt()>10 and c.fromPV()==c.PVTight and abs(c.pdgId()) in [11, 13, 211], pfc)]

#EventLoop over events>>>
nEvents = 10#events.size()

#metLepDist=ROOT.TH1F('metLepDist','metLepDist',100,0,100)
metDist=ROOT.TH1F('metDist','metDist',100,0,100)
metPuppiDist=ROOT.TH1F('metPuppiDist','metPuppiDist',100,0,100)
pfMetDist=ROOT.TH1F('pfMetDist','pfMetDist',100,0,100)
pfMetDist=ROOT.TH1F('pfMetDist','pfMetDist',100,0,100)

sumPy = sumPx = 0
for i in range(nEvents):
  c.GetEntry(i)
  events.to(i)

  ## Filter Hadronic events
  events.getByLabel(gpLabel,gpHandle)
  gps =gpHandle.product()
  lgps = list(gps)
  isHad=True
  for igp,gp in enumerate(gps):
    pdgId = abs(gp.pdgId())
    if pdgId==12 or pdgId==14 or pdgId==16:
      if gp.numberOfMothers()>0 and abs(gp.mother(0).pdgId())==24:
        isHad=False
        break
  if not isHad:continue

  events.getByLabel(puppiLabel,puppiHandle)
  puppicH = puppiHandle.product()
  puppic = list(puppicH) #->Puppi 
  sumPy = sumPx = 0
  for p in puppic:
    sumPx += p.px()
    sumPy += p.py()
  met = sqrt(sumPx**2 + sumPy**2)
  metPuppiDist.Fill(met)

  events.getByLabel(pfMetPuppiLabel,pfMetPuppiHandle)
  pfMetPuppicH = pfMetPuppiHandle.product()
  pfMetPuppic = list(pfMetPuppicH)

  print 'PUPPI\n', met, 'vs. ', pfMetPuppicH[0].pt() , 'with difference: ', met - pfMetPuppicH[0].pt()

  events.getByLabel(pfLabel,pfHandle)
  pfcH = pfHandle.product()
  pfc = list(pfcH) #->packedCandidates (PFCandidates)
  sumPy = sumPx = 0
  for p in pfc:
    sumPx += p.px()
    sumPy += p.py()
  met = sqrt(sumPx**2 + sumPy**2)
  metDist.Fill(met)

  events.getByLabel(pfMetLabel,pfMetHandle)
  pfMetcH = pfMetHandle.product()
  pfMetc = list(pfMetcH) #->pfmet 
#  sumPy = sumPx = 0
#  for p in pfMetc:
#    sumPx += p.px()
#    sumPy += p.py()
#  met = sqrt(sumPx**2 + sumPy**2)
#  pfMetDist.Fill(met)


#  print met, 'vs. ', c.GetLeaf('float_BasicTupelizer_slimmedMETs_Tupelizer.obj').GetValue()
  print met, 'vs. ', pfMetcH[0].pt() , 'with difference: ', met - pfMetcH[0].pt()


def calcMet(label,handle):
  events.getByLabel(label,handle)
  cH=handle.product()
  clist = list(cH)
  sumPy = sumPx =0
  for p in clist:
    sumPx += p.px()
    sumPy += p.py()
  met = sqrt(sumPx**2 + sumPy**2)
  

#  print met, c.GetLeaf(c.GetAlias('pfMet')).GetValue()

##remove leptonic jets
##c.ngNuEFromW=0
# print met[i] 

#metAve= sum(met)/len(met)
#print metAve

##### plot MET dist #####

c1 = ROOT.TCanvas("c1","c1")
c1.cd()
metDist.Draw()
#c2 = ROOT.TCanvas("c2","c2")
#ROOT.c2.cd()
metPuppiDist.SetLineColor(3)
metPuppiDist.Draw("same")
#pfmetDist.SetLineColor(5)
#pfmetDist.Draw("same")

# for j, pc in enumerate(pfc):
# print i,j, pc.pt()

