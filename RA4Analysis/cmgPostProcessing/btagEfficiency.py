import ROOT, pickle, itertools, os

from Workspace.HEPHYPythonTools.helpers import *
from Workspace.RA4Analysis.helpers import *

#import PhysicsTools.Heppy.physicsutils.BTagSF

#from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_HT400ST200_postProcessed import *
#WJETS = {'name':'WJets', 'chain':getChain(WJetsHTToLNu_25ns,histname=''), 'color':color('WJets'),'weight':'weight', 'niceName':'W Jets'}
#TTJetsLO = {'name':'TTJets', 'chain':getChain(TTJets_LO_25ns,histname=''), 'color':color('TTJets')-2,'weight':'weight', 'niceName':'t#bar{t} Jets LO'}
#newpresel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0&&st>250&&nJet30>=2&&htJet30j>500"


#bTagEffFile = '/afs/hephy.at/data/dspitzbart02/RA4/btagEfficiency/Moriond_v3.pkl'

#ptBorders = [30, 40, 50, 60, 70, 80, 100, 120, 160, 210, 260, 320, 400, 500, 670]
ptBorders = [30, 50, 70, 100, 140, 200, 300, 600, 1000]
ptBins = []
etaBins = [[0,0.8], [0.8,1.6], [ 1.6, 2.4]]

scaleFactorFile   = '$CMSSW_BASE/src/Workspace/RA4Analysis/cmgPostProcessing/data/CSVv2_Moriond17_B_H.csv'
scaleFactorFileFS = '$CMSSW_BASE/src/Workspace/RA4Analysis/cmgPostProcessing/data/fastsim_csvv2_ttbar_26_1_2017.csv'


#SFb_errors = [\
# 0.0209663,
# 0.0207019,
# 0.0230073,
# 0.0208719,
# 0.0200453,
# 0.0264232,
# 0.0240102,
# 0.0229375,
# 0.0184615,
# 0.0216242,
# 0.0248119,
# 0.0465748,
# 0.0474666,
# 0.0718173
#]

#SFb_err={}
for i in range(len(ptBorders)-1):
  ptBins.append([ptBorders[i], ptBorders[i+1]])
#  SFb_err[tuple(ptBins[i])] = SFb_errors[i]
  if i == len(ptBorders)-2:
    ptBins.append([ptBorders[i+1], -1])

#ROOT.gROOT.ProcessLine(".L btagEff/FSimCorr_UCSB.C+")

def partonName (parton):
  if parton==5:  return 'b'
  if parton==4:  return 'c'
  return 'other'

def getSignalChain(signal):
  l = []
  for x in signal:
    print
    print 'mgl', x
    for y in signal[x]:
      print 'mX', y
      l.append(signal[x][y])
  c = getChain(l, histname='')
  return c

def toFlavourKey(pdgId):
    if abs(pdgId)==5: return ROOT.BTagEntry.FLAV_B
    if abs(pdgId)==4: return ROOT.BTagEntry.FLAV_C
    return ROOT.BTagEntry.FLAV_UDSG


# get MC truth efficiencies for a specific sample
def getBTagMCTruthEfficiencies(c, cut="(1)", overwrite=False, btagVar='Jet_btagCSV', btagWP='0.8484'):
  print c, cut
  mceff = {}
  commoncf=cut+"&&"
  for ptBin in ptBins:
    mceff[tuple(ptBin)] = {}
    for etaBin in etaBins:
      mceff[tuple(ptBin)][tuple(etaBin)] = {}
      #c.Draw("Sum$(jetsBtag>0.679&&jetsParton==5&&jetsPt>40&&jetsPt<50&&abs(jetsEta)>0&&abs(jetsEta)<1)/Sum$(jetsParton==5&&jetsPt>40&&jetsPt<50&&abs(jetsEta)>0&&abs(jetsEta)<1)")
      etaCut = "abs(Jet_eta)>"+str(etaBin[0])+"&&abs(Jet_eta)<"+str(etaBin[1])
      ptCut = "Jet_pt>"+str(ptBin[0])
      if ptBin[1]>0:
        ptCut += "&&Jet_pt<"+str(ptBin[1])
      c.Draw(commoncf+"("+btagVar+">"+str(btagWP)+")>>hbQuark(100,-1,2)",commoncf+"abs(Jet_hadronFlavour)==5&&                     "+etaCut+"&&"+ptCut)
      c.Draw(commoncf+"("+btagVar+">"+str(btagWP)+")>>hcQuark(100,-1,2)",commoncf+"abs(Jet_hadronFlavour)==4&&                     "+etaCut+"&&"+ptCut)
      c.Draw(commoncf+"("+btagVar+">"+str(btagWP)+")>>hOther(100,-1,2)" ,commoncf+"(abs(Jet_hadronFlavour) < 4  || abs(Jet_hadronFlavour) > 5)&&  "+etaCut+"&&"+ptCut)
      hbQuark = ROOT.gDirectory.Get("hbQuark")
      hcQuark = ROOT.gDirectory.Get("hcQuark")
      hOther = ROOT.gDirectory.Get("hOther")
      mceff[tuple(ptBin)][tuple(etaBin)]["b"]     = hbQuark.GetMean()
      mceff[tuple(ptBin)][tuple(etaBin)]["c"]     = hcQuark.GetMean()
      mceff[tuple(ptBin)][tuple(etaBin)]["other"] = hOther.GetMean()
      print "Eta",etaBin,etaCut,"Pt",ptBin,ptCut,"Found b/c/other", mceff[tuple(ptBin)][tuple(etaBin)]["b"], mceff[tuple(ptBin)][tuple(etaBin)]["c"], mceff[tuple(ptBin)][tuple(etaBin)]["other"]
      del hbQuark, hcQuark, hOther
  if overwrite: pickle.dump(mceff, file(bTagEffFile, 'w'))
  return mceff

def getDummyEfficiencies():
  mceff={}
  for ptBin in ptBins:
    mceff[tuple(ptBin)] = {}
    for etaBin in etaBins:
      mceff[tuple(ptBin)][tuple(etaBin)] = {}
      mceff[tuple(ptBin)][tuple(etaBin)]["b"]     = 0.5
      mceff[tuple(ptBin)][tuple(etaBin)]["c"]     = 0.5
      mceff[tuple(ptBin)][tuple(etaBin)]["other"] = 0.5
  return mceff

def getHistMCTruthEfficiencies(MCEff, histname, etaBin = (0,0.8), hadron='b'):
  nBins = len(MCEff)
  hist = ROOT.TH1F(histname,'MC truth b-tag efficiency',nBins,0,nBins)
  effs = []
  for a in sorted(MCEff):
    effs.append(MCEff[a][etaBin][hadron])
  for b in range(1,nBins+1):
    hist.SetBinContent(b,effs[b-1])
    hist.GetXaxis().SetBinLabel(b,varBinName(sorted(MCEff.keys())[b-1],"p_{T}"))
  return hist

# get SF
def getSF(parton, pt, eta, year = 2012):
  btag = ROOT.heppy.BTagSF.BTagSF()
  if year == 2012: y = True
  else: y = False
  if abs(parton)==5: #SF for b
    sf = btag.getSFb(pt,0,y)
    sf_d = btag.getSFb(pt,1,y)
    sf_u = btag.getSFb(pt,2,y)
  elif abs(parton)==4: #SF for c
    sf = btag.getSFc(pt,0,y)
    sf_d = btag.getSFc(pt,1,y)
    sf_u = btag.getSFc(pt,2,y)
  else: #SF for light flavours
    sf = btag.getSFl(pt,eta,0,y)
    sf_d = btag.getSFl(pt,eta,1,y)
    sf_u = btag.getSFl(pt,eta,2,y)
  return {"SF":sf, "SF_down":sf_d,"SF_up":sf_u}

## get SFs
WP = ROOT.BTagEntry.OP_MEDIUM
ROOT.gSystem.Load('libCondFormatsBTauObjects')
ROOT.gSystem.Load('libCondToolsBTau')

print 'Loading SF files:'
print os.path.expandvars(scaleFactorFile)
print os.path.expandvars(scaleFactorFileFS)

calib   = ROOT.BTagCalibration("csvv2", os.path.expandvars(scaleFactorFile))
calibFS = ROOT.BTagCalibration("csv", os.path.expandvars(scaleFactorFileFS))

v_sys = getattr(ROOT, 'vector<string>')()
v_sys.push_back('up')
v_sys.push_back('down')
reader = ROOT.BTagCalibrationReader(WP, "central", v_sys)
reader.load(calib, 0, "comb")
reader.load(calib, 1, "comb")
reader.load(calib, 2, "incl")

calibFS = ROOT.BTagCalibration("csv", os.path.expandvars( scaleFactorFileFS ) )
readerFS = ROOT.BTagCalibrationReader(WP, "central", v_sys)
readerFS.load(calibFS, 0, "fastsim")
readerFS.load(calibFS, 1, "fastsim")
readerFS.load(calibFS, 2, "fastsim")


def getSF2015(parton, pt, eta):

  if pt<20: raise ValueError( "BTag SF Not implemented below 20 GeV. Got %f"%pt )
  flavKey = toFlavourKey(parton)

  #FullSim SFs (times FSSF)
  if abs(parton)==5 or abs(parton)==4: #SF for b/c
      sf    = reader.eval_auto_bounds('central',  flavKey, eta, pt)
      sf_d  = reader.eval_auto_bounds('down',     flavKey, eta, pt)
      sf_u  = reader.eval_auto_bounds('up',       flavKey, eta, pt)
  else: #SF for light flavours
      sf    = reader.eval_auto_bounds('central',  flavKey, eta, pt)
      sf_d  = reader.eval_auto_bounds('down',     flavKey, eta, pt)
      sf_u  = reader.eval_auto_bounds('up',       flavKey, eta, pt)

  return {"SF":sf, "SF_down":sf_d,"SF_up":sf_u}

# get MC efficiencies and scale factors for a specific jet (with parton flavor, pt and eta)
#try:
#  mcEff = pickle.load(file(bTagEffFile))
#except IOError:
#  print 'Unable to load MC efficiency file!'
#  mcEff = False
def getMCEff(parton, pt, eta, mcEff, year = 2015):
  for ptBin in ptBins:
    if pt>=ptBin[0] and (pt<ptBin[1] or ptBin[1]<0):
      for etaBin in etaBins:
        if abs(eta)>=etaBin[0] and abs(eta)<etaBin[1]:
          if year == 2015: res=getSF2015(parton, pt, eta)
          else: res=getSF(parton, pt, eta, year)
#          print ptBin, etaBin      , mcEff[tuple(ptBin)][tuple(etaBin)]
          if abs(parton)==5:                  res["mcEff"] = mcEff[tuple(ptBin)][tuple(etaBin)]["b"]
          if abs(parton)==4:                  res["mcEff"] = mcEff[tuple(ptBin)][tuple(etaBin)]["c"]
          if abs(parton)>5 or abs(parton)<4:  res["mcEff"] = mcEff[tuple(ptBin)][tuple(etaBin)]["other"]
          return res


SFlist = ["mceffs", "mceffs_SF", "mceffs_SF_b_Up", "mceffs_SF_b_Down", "mceffs_SF_light_Up", "mceffs_SF_light_Down"]

# get MC efficiencies and scale factors for all jets of one event c, uses getMCEff
def getMCEfficiencyForBTagSF(c, mcEff, onlyLightJetSystem = False, sms=""):
  nsoftjets = int(getVarValue(c, "nJet30"))
  njets = int(getVarValue(c, "nJet"))
  jets = []
  for i in range(njets):
    jPt     = getVarValue(c, "Jet_pt", i)
    jEta    = getVarValue(c, "Jet_eta", i)
    jParton = getVarValue(c, "Jet_hadronFlavour", i)
#                eff = 0.9-min(5,i)*0.1#getEfficiencyAndMistagRate(jPt, jEta, jParton )
    #if jPt<=40. or abs(jEta)>=2.4 or (not getVarValue(c, "jetsEleCleaned", i)) or (not getVarValue(c, "jetsMuCleaned", i)) or (not getVarValue(c, "jetsID", i)):
    if jPt<=30. or abs(jEta)>=2.4 or (not getVarValue(c, "Jet_id", i)):
      continue
    if onlyLightJetSystem and getVarValue(c, "Jet_btagCSV", i)>0.890:
      continue
    if onlyLightJetSystem:
      jParton=1
    jets.append([jParton, jPt, jEta])
  if onlyLightJetSystem and len(jets)>0:
    nc = randint(0, len(jets)-1)
    jets[nc][0] = 4
  for jet in jets:
    jParton, jPt, jEta = jet
    r = getMCEff(parton=jParton, pt=jPt, eta=jEta, mcEff=mcEff, year=2015)#getEfficiencyAndMistagRate(jPt, jEta, jParton )
    jet.append(r)
#    print [j[0] for j in jets]
  if len(jets) != nsoftjets: print '!!!!! Different number of jets in collection than there should be !!!!!'
  mceffs = tuple()
  mceffs_SF = tuple()
  mceffs_SF_b_Up = tuple()
  mceffs_SF_b_Down = tuple()
  mceffs_SF_light_Up = tuple()
  mceffs_SF_light_Down = tuple()
  for jParton, jPt, jEta, r in jets:
    if sms!="":
      flavKey = toFlavourKey(jParton)
      #FastSim SFs
      fsim_SF       = readerFS.eval_auto_bounds('central', flavKey, jEta, jPt)
      fsim_SF_down  = readerFS.eval_auto_bounds('down',    flavKey, jEta, jPt)
      fsim_SF_up    = readerFS.eval_auto_bounds('up',      flavKey, jEta, jPt)
      if fsim_SF == 0:  # should not happen, however, if pt=1000 (exactly) the reader will return a sf of 0.
          fsim_SF       = 1
          fsim_SF_up    = 1
          fsim_SF_down  = 1
    else:
      fsim_SF = 1.
      fsim_SF_up = 1.
      fsim_SF_down = 1.
    mceffs += (r["mcEff"],)
    mceffs_SF += (r["mcEff"]*r["SF"]*fsim_SF,)
    if abs(jParton)==5 or abs(jParton)==4:
      mceffs_SF_b_Up   += (r["mcEff"]*r["SF_up"]*fsim_SF_up,)
      mceffs_SF_b_Down += (r["mcEff"]*r["SF_down"]*fsim_SF_down,)
      mceffs_SF_light_Up   += (r["mcEff"]*r["SF"],)
      mceffs_SF_light_Down += (r["mcEff"]*r["SF"],)
    else:
      mceffs_SF_b_Up   += (r["mcEff"]*r["SF"],)
      mceffs_SF_b_Down += (r["mcEff"]*r["SF"],)
      mceffs_SF_light_Up   += (r["mcEff"]*r["SF_up"]*fsim_SF_up,)
      mceffs_SF_light_Down += (r["mcEff"]*r["SF_down"]*fsim_SF_down,)
  for ix, x in enumerate([mceffs,mceffs_SF,mceffs_SF_b_Up,mceffs_SF_b_Down,mceffs_SF_light_Up,mceffs_SF_light_Down]):
    if 1 in x:
      print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
      print jets
      print SFlist[ix]
      print mcEff
  return {"mceffs":mceffs, "mceffs_SF":mceffs_SF, "mceffs_SF_b_Up":mceffs_SF_b_Up, "mceffs_SF_b_Down":mceffs_SF_b_Down, "mceffs_SF_light_Up":mceffs_SF_light_Up, "mceffs_SF_light_Down":mceffs_SF_light_Down}


# get the tag weights for the efficiencies calculated with getMCEfficiencyForBTagSF
def getTagWeightDict(effs, maxConsideredBTagWeight):
  zeroTagWeight = 1.
  for e in effs:
    zeroTagWeight*=(1-e)
  tagWeight={}
  for i in range(min(len(effs), maxConsideredBTagWeight)+1):
    tagWeight[i]=zeroTagWeight
    twfSum = 0.
    for tagged in itertools.combinations(effs, i):
      twf=1.
      for x in tagged:
        if x ==1:
          print 'Possible problem spotted!'
          print effs, tagged
      for fac in [x/(1-x) for x in tagged]:
        twf*=fac
      twfSum+=twf
#      print "tagged",tagged,"twf",twf,"twfSum now",twfSum
    tagWeight[i]*=twfSum
#  print "tagWeight",tagWeight,"\n"
  for i in range(maxConsideredBTagWeight+1):
    if not tagWeight.has_key(i):
      tagWeight[i] = 0.
  return tagWeight

# Function for different method, described in https://twiki.cern.ch/twiki/bin/view/CMS/BTagSFMethods#1a_Event_reweighting_using_scale
# FastSim corrections not implemented yet

def getBTagWeight(c, sms=""):
  nsoftjets = int(getVarValue(c, "nJet30"))
  njets = int(getVarValue(c, "nJet"))
  jets = []
  for i in range(njets):
    isBtagged = False
    jPt     = getVarValue(c, "Jet_pt", i)
    jEta    = getVarValue(c, "Jet_eta", i)
    jParton = getVarValue(c, "Jet_hadronFlavour", i)
    jBTagCSV = getVarValue(c, "Jet_btagCSV", i)
    if jBTagCSV > 0.890: isBtagged = True
    if jPt<=30. or abs(jEta)>=2.4 or (not getVarValue(c, "Jet_id", i)):
      continue
    jets.append([jParton, jPt, jEta, isBtagged])
  if len(jets) != nsoftjets: print 'Different number of jets in collection than there should be!!'
  mceffs = tuple()
  mceffs_SF = tuple()
  mceffs_SF_b_Up = tuple()
  mceffs_SF_b_Down = tuple()
  mceffs_SF_light_Up = tuple()
  mceffs_SF_light_Down = tuple()
  PMC = 1.
  PData = 1.
  PData_b_up = 1.
  PData_b_down = 1.
  PData_l_up = 1.
  PData_l_down = 1.
  for jParton, jPt, jEta, isBtagged in jets:
    r = getMCEff(parton=jParton, pt=jPt, eta=jEta, year=2015)#getEfficiencyAndMistagRate(jPt, jEta, jParton )
    if sms!="":
      fsim_SF = ROOT.getFastSimCorr(partonName(abs(jParton)),jPt,"mean",jEta)
      fsim_SF_up = ROOT.getFastSimCorr(partonName(abs(jParton)),jPt,"up",jEta)
      fsim_SF_down = ROOT.getFastSimCorr(partonName(abs(jParton)),jPt,"down",jEta)
    else:
      fsim_SF = 1.
      fsim_SF_up = 1.
      fsim_SF_down = 1.
    if isBtagged:
      PMC *= r['mcEff']
      PData *= r['mcEff']*r['SF']
      if abs(jParton)==5 or abs(jParton)==4:
        PData_b_up *= r['mcEff']*r['SF_up']
        PData_b_down *= r['mcEff']*r['SF_down']
        PData_l_up *= r['mcEff']*r['SF']
        PData_l_down *= r['mcEff']*r['SF']
      else:
        PData_b_up *= r['mcEff']*r['SF']
        PData_b_down *= r['mcEff']*r['SF']
        PData_l_up *= r['mcEff']*r['SF_up']
        PData_l_down *= r['mcEff']*r['SF_down']
    else:
      PMC *= (1. - r['mcEff'])
      PData *= (1. - r['mcEff']*r['SF'])
      if abs(jParton)==5 or abs(jParton)==4:
        PData_b_up *=   (1 - r['mcEff']*r['SF_up'])
        PData_b_down *= (1 - r['mcEff']*r['SF_down'])
        PData_l_up *=   (1 - r['mcEff']*r['SF'])
        PData_l_down *= (1 - r['mcEff']*r['SF'])
      else:
        PData_b_up *=   (1 - r['mcEff']*r['SF'])
        PData_b_down *= (1 - r['mcEff']*r['SF'])
        PData_l_up *=   (1 - r['mcEff']*r['SF_up'])
        PData_l_down *= (1 - r['mcEff']*r['SF_down'])
      #PData_up *= (1 - r['mcEff']*r['SF_up'])
      #PData_down *= (1 - r['mcEff']*r['SF_down'])
    res = {'w':PData/PMC, 'w_b_up':PData_b_up/PMC, 'w_b_down':PData_b_down/PMC, 'w_l_up':PData_l_up/PMC, 'w_l_down':PData_l_down/PMC}
    return res



