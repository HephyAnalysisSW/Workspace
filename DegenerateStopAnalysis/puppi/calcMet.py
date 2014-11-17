from DataFormats.FWLite import Events, Handle
from PhysicsTools.PythonAnalysis import *
from math import *
import ROOT
'''
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
'''

labellist = ('packedGenParticles','packedPFCandidates',('puppi','Puppi'),'pfMet','pfMetPuppi')
handlelist = ("vector<pat::PackedGenParticle>", "vector<pat::PackedCandidate>","vector<reco::PFCandidate>","vector<reco::PFMET>","vector<reco::PFMET>")
#labellist = ('packedGenParticles','packedPFCandidates','pfMet')
#handlelist = ("vector<pat::PackedGenParticle>", "vector<pat::PackedCandidate>","vector<reco::PFMET>")
#cuts are made based on the first element of the label and handlelist

provide = [\
       {'type':"vector<pat::PackedGenParticle>", 'label':'packedGenParticles', 'localName':'pfCandidates'}, 
#       {'handle':"vector<pat::PackedGenParticle>", 'label':'packedGenParticles', 'localName':'pfCanditates'}, 
          ]
mothers =[]
metD = []
def calcMet(labels,handles,filelist=['/data/schoef/puppi/histo.root']):
  events = Events(filelist)
  events.toBegin()
  c = ROOT.TChain('Events')
  for f in filelist:
    c.Add(f)

  nEvents=10 #events.size()
  sumPy = sumPx = 0

  for s in range (0,len(labels)):
    metD.append(0)
    metD[s] = ROOT.TH1F(str(s),str(s),100,0,100)

  for p in provide:
    p['handle'] = Handle(p['type'])

  for iEvent in range(nEvents):
    c.GetEntry(iEvent)
    events.to(iEvent)
    
#    for p in provide:
#      events.getByLabel(p['label'], p['handle'])
#      exec(p['localName'] +"= p['handle'].product()")
#    print pfCandidates
    ## Filter Hadronic events
    gps = Handle(handles[0])
    lgp = labels[0]
    events.getByLabel(lgp,gps)
    gps = gps.product()
    lgp = list(gps)
    isHad=True
    for igp,gp in enumerate(gps):
      pdgId = abs(gp.pdgId())
#      if abs(gp.mother(0).pdgId())==24: print 'from W'
#      if gp.pt() > 100 : print 'p ', pdgId  , 'pt= ', gp.pt(), 'mother is: ', gp.mother(0).pdgId()
      if pdgId==12 or pdgId==14 or pdgId==16:
#        if gp.mother(0).pdgId() not in mothers: mothers.append(gp.mother(0).pdgId())
 #       print 'here', gp.numberOfMothers(), gp.mother(0).pdgId()
        if abs(gp.mother(0).pdgId())==24:
         # print 'from W', pdgId, gp.pt()
          isHad=False
          break 
#    print "isHad", isHad
    if not isHad:continue
#    print c.GetLeaf(c.GetAlias('genMet')).GetValue()
    for s in range (1,len(labels)):
      hndl = Handle(handles[s]) 
      lbl = labels[s]
      htitle = lbl
      events.getByLabel(lbl,hndl)
      cH=hndl.product()
      clist = list(cH)
      sumPy = sumPx =0
      for p in clist:
        sumPx += p.px()
        sumPy += p.py()
      met = sqrt(sumPx**2 + sumPy**2)
      metD[s].Fill(met)

 # del ROOT.gDirectory.FindObject("c1");
  leg = ROOT.TLegend(0.1,0.7,0.48,0.9)
  
  c1= ROOT.TCanvas("c1","c1")
  c1.cd()
  drawOpt=''
  for s  in range (1,len(labels)):
    if s > 1 : drawOpt = 'same'
    metD[s].SetLineWidth(1/s)
    metD[s].SetLineColor(s)
    leg.AddEntry(metD[s],str(labels[s]),"f")
    metD[s].Draw(drawOpt)   

  leg.Draw()

calcMet(labellist,handlelist)
