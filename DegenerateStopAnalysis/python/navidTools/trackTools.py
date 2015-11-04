import math
from getSamples_PP_withTracks import *
from Workspace.HEPHYPythonTools.helpers import getYieldFromChain, deltaR
from Workspace.DegenerateStopAnalysis import cuts

leadingIsrPt   = 110
sysUnc  = 0.2
#genCut = "nGenJet>0 && GenJet_pt[0]>{leadingIsrPt} && met_genPt > 200 && Sum$(abs(genPartPkd_pdgId)==13 && abs(genPartPkd_eta)<2.5 && genPartPkd_pt > 5 && genPartPkd_pt<30)==1".format(leadingIsrPt=leadingIsrPt)
SGenCut = "nGenJet>0 && GenJet_pt[0]>{leadingIsrPt} && met_genPt > 200 && Sum$( genPartPkd_pdgId==13 && abs(genPartPkd_eta)<2.5 && genPartPkd_pt > 5 && genPartPkd_pt<30 && abs(genPartPkd_motherId)==1000006 )==1".format(leadingIsrPt=leadingIsrPt)
WGenCut = "nGenJet>0 && GenJet_pt[0]>{leadingIsrPt} && met_genPt > 200 && Sum$( genPartPkd_pdgId==13 && abs(genPartPkd_eta)<2.5 && genPartPkd_pt > 5 && genPartPkd_pt<30 && ( abs(genPartPkd_motherId)==24 || abs(genPartPkd_motherId)==15) )==1".format(leadingIsrPt=leadingIsrPt)

recoCut = "nJet110>=1 && met>200 && htJet30j>200 && nlep==1 && lepPt<30"


def getHistsFromFile(f,histType="TH2F"):
  keyList = f.GetListOfKeys()
  #th2fList = [x.GetName() for x in keyList if x.GetClassName().lower()==histType.lower()] 
  #th2fs = [getattr(f,x.GetName()) for x in keyList if x.GetClassName().lower()==histType.lower()]
  return { x.GetName():getattr(f,x.GetName()) for x in keyList if x.GetClassName().lower()==histType.lower() }

def AMSSYS (s,b):
  #print s, b
  if s==0:
    return 0
  if b==0:
    return -1
  #return (lambda s,b : math.sqrt(2*( (s+b)*math.log(((s+b)*(b+sysUnc*b))/(b*b+(s+b)*sysUnc*b))  - b*b/(sysUnc*b)*math.log(1+sysUnc*b*s/(b*(b+sysUnc*b))) )) if b!=0 else -1)(s,b)
  return (lambda s,b : math.sqrt(2*( (s+b)*math.log(((s+b)*(b+ (sysUnc*sysUnc*b*b) ))/(b*b+(s+b)* (sysUnc*sysUnc*b*b) ))  - b*b/( (sysUnc*sysUnc*b*b) )*math.log(1+ (sysUnc*sysUnc*b*b) *s/(b*(b+ (sysUnc*sysUnc*b*b) )))))) (s,b)
  
fomFuncs={
            "SOB"       : {'func':lambda s,b : s/math.sqrt(b) if b!=0 else -1 },
            "SOBSYS"   : {'func':lambda s,b : s/math.sqrt(b+(sysUnc*sysUnc*b*b) ) if b!=0 else -1 },
            "AMS"   : {'func':lambda s,b : math.sqrt(2*((s+b)*math.log(1+1.*s/b)-s) ) if b!=0 else -1 },
            #"FOM_AMSSYS": {'func':lambda s,b : math.sqrt(2*( (s+b)*math.log(((s+b)*(b+sigb*sigb))/(b*b+(s+b)*sigb*sigb))  - b*b/(sigb*sigb)*math.log(1+sigb*sigb*s/(b*(b+sigb*sigb)))   ) if b!=0 else -1 },
            #"FOM_AMSSYS": {'func':lambda s,b : math.sqrt(2*( (s+b)*math.log(((s+b)*(b+sysUnc*b))/(b*b+(s+b)*sysUnc*b))  - b*b/(sysUnc*b)*math.log(1+sysUnc*b*s/(b*(b+sysUnc*b))) )) if b!=0 elif s==0 -1 },
            "AMSSYS": {'func':AMSSYS },
            } 

def getFOMs(s,b):
  ret = {}
  for f in fomFuncs:
    ret[f]=fomFuncs[f]['func'](s,b)
  return ret

#foms=\
#           {
#            "FOM"       : {'func':lambda s,b : s/math.sqrt(b) if b!=0 else -1 },
#            "FOM_sys"   : {'func':lambda s,b : s/math.sqrt(b+ (sysUnc*b*b) ) if b!=0 else -1 },
#            "FOM_AMS"   : {'func':lambda s,b : math.sqrt(2*((s+b)*math.log(1+1.*s/b)-s) ) if b!=0 else -1 },
#            #"FOM_AMSSYS": {'func':lambda s,b : math.sqrt(2*( (s+b)*math.log(((s+b)*(b+sigb*sigb))/(b*b+(s+b)*sigb*sigb))  - b*b/(sigb*sigb)*math.log(1+sigb*sigb*s/(b*(b+sigb*sigb)))   ) if b!=0 else -1 },
#            "FOM_AMSSYS": {'func':lambda s,b : math.sqrt(2*( (s+b)*math.log(((s+b)*(b+ (sysUnc*b*b) ))/(b*b+(s+b)* (sysUnc*b*b) ))  - b*b/( (sysUnc*b*b) )*math.log(1+ (sysUnc*b*b) *s/(b*(b+ (sysUnc*b*b) )))
#            }
#

def makeTGraphFromList(l):
  graph=ROOT.TGraph()
  for i,j in enumerate(l):
    graph.SetPoint(i,i,j)
  return graph

def getFOMfromCut(cut="(1)", fom="AMSSYS"):
  s=sampleDict['s']['tree']
  b=sampleDict['W']['tree']
  sYield = getYieldFromChain(s,cut)
  bYield = getYieldFromChain(b,cut)
  #FOM = fomFuncs[fom]['func'](sYield,bYield)
  FOMS = getFOMs(sYield,bYield)[fom]
  return (sYield,bYield,FOMS)

def getFOMFromTH2F(sHist,bHist): 
  assert sHist.GetNbinsX() == bHist.GetNbinsX(), "xBins dont match" 
  assert sHist.GetNbinsY() == bHist.GetNbinsY(), "yBins don't match" 
  nBinX= sHist.GetNbinsX() 
  nBinY= sHist.GetNbinsY() 
  for fomHist in fomFuncs: 
    #fomFuncs[fomHist]['hist']=sHist.Copy(fomHist) 
    fomFuncs[fomHist]['hist']=sHist.Clone() 
    fomFuncs[fomHist]['hist'].Reset() 
    fomFuncs[fomHist]['hist'].SetMarkerSize(0.8) 
    fomFuncs[fomHist]['hist'].SetName("FOM_"+fomFuncs[fomHist]['hist'].GetName() ) 
  for x in range(1,nBinX+1): 
    for y in range(1,nBinY+1): 
      s=sHist.GetBinContent(x,y) 
      b=bHist.GetBinContent(x,y) 
      for fomHist in fomFuncs.itervalues(): 
        fom= fomHist['func'](s,b) 
        #print s, b 
        fomHist['hist'].SetBinContent(x,y,fom) 
  return fomFuncs   


def isNotJetTrack(gp, isrList,drMax):
  trfl = True
  for isr in isrList:
    dR = deltaR(gp,isr)
    #print dR
    if dR < drMax:
      #trfl = isr['pt']
      trfl = False
      #print trfl, dR
      break
  return trfl




def drawTracks(tree,iEvt):
  tree.SetLineColor(ROOT.kBlue); 
  tree.Draw("genPartPkd_phi>>(20,-3,3)","( cos(genPartPkd_phi - GenJet_phi[0]) < 0 ) && abs(genPartPkd_charge)>0 && genPartPkd_pt>1 && abs(genPartPkd_eta)<2.5  && evt==%s"%iEvt); 
  tree.SetLineColor(ROOT.kViolet); 
  sampleDict['s']['tree'].SetLineColor(ROOT.kViolet); 
  tree.Draw("GenJet_phi",'(evt==%s)*10*GenJet_pt/(Sum$(GenJet_pt))'%iEvt,'same')
  tree.SetLineColor(ROOT.kRed); 
  tree.Draw("GenJet_phi[0]",'(evt==%s)'%iEvt,'same'); 


#def countTracks(gp,jets,isrPtList,drList)
#ntrks={}
#def testForNonIsrTracks(part,isrJets,isrPtList,drList,trkPtList,debug=False):
#  #ntrks=makeDict(isrPtList,drList,trkPtList)
#  for isrPt in isrPtList:
#    if debug: print "isrPt:  ", isrPt, "--------------"
#    for drMax in drList:
#      if isNotJetTrack(part, isrJets[isrPt]['list'],drMax):
#        for trkPt in trkPtList:
#          if part['pt'] > trkPt:
#            ntrks[isrPt][drMax][trkPt]+=1
#  return ntrks


def countNonIsrTracks(parts,isrJets,isrPtList,drList,trkPtList,debug=False,trackCheck=None):
  if trackCheck==None:
    trackCheck = lambda part: part['pt'] > min(trkPtList) and abs(part['eta']) < 2.5 and abs(part['charge']) > 0
  ntrks=makeDict(isrPtList,drList,trkPtList)
  for part in parts:
    if trackCheck(part):
    #if part['pt'] > min(trkPtList) and abs(part['eta']) < 2.5 and abs(part['charge']) > 0 :
      for isrPt in isrPtList:
        if debug: print "isrPt:  ", isrPt, "--------------"
        for drMax in drList:
          if isNotJetTrack(part, isrJets[isrPt]['list'],drMax):
            for trkPt in trkPtList:
              if part['pt'] > trkPt:
                ntrks[isrPt][drMax][trkPt]+=1
  return ntrks

def countNonIsrTracksInHemis(parts,isrJets,isrPtList,hemiList,nIsrList,trkPtList,drMax=0.4,debug=False,cosines={},trackCheck=None):
  if trackCheck==None:
    trackCheck = lambda part: part['pt'] > min(trkPtList) and abs(part['eta']) < 2.5 and abs(part['charge']) > 0
  ntrks = { isrPt:makeDict(hemiList,nIsrList,trkPtList) for isrPt in isrPtList}
  for part in parts:
    if trackCheck(part):
    #if part['pt'] > min(trkPtList) and abs(part['eta']) < 2.5 and abs(part['charge']) > 0 :
      for isrPt in isrPtList:
        for nIsr in nIsrList:
          totIsrPhi = isrJets[isrPt]['tot'][nIsr].Phi()
          for hemi in hemiList:
            if math.cos( part['phi']-totIsrPhi) < cosines[hemi]:
              if isNotJetTrack(part, isrJets[isrPt]['list'][:nIsr],drMax):
                for trkPt in trkPtList:
                  if part['pt'] > trkPt:
                    ntrks[isrPt][hemi][nIsr][trkPt]+=1
  return ntrks





#trackQual = lambda part: part['pt'] > min(trkPtList) and abs(part['eta']) < 2.5 and abs(part['charge']) > 0


def countNonIsrRecoTracksInHemis(parts,isrJets,isrPtList,hemiList,nIsrList,trkPtList,drMax=0.4,debug=False,cosines={}):
  ntrks = { isrPt:makeDict(hemiList,nIsrList,trkPtList) for isrPt in isrPtList}
  for part in parts:    
    if part['pt'] > 0 and abs(part['eta']) < 2.5 and abs(part['charge']) > 0:
    #if part['pt'] > min(trkPtList) and abs(part['eta']) < 2.5 and abs(part['charge']) > 0 :
      for isrPt in isrPtList:
        for nIsr in nIsrList:
          totIsrPhi = isrJets[isrPt]['tot'][nIsr].Phi()
          for hemi in hemiList:
            if math.cos( part['phi']-totIsrPhi) < cosines[hemi]:
              if isNotJetTrack(part, isrJets[isrPt]['list'][:nIsr],drMax):
                for trkPt in trkPtList:
                  if part['pt'] > trkPt:
                    ntrks[isrPt][hemi][nIsr][trkPt]+=1
  return ntrks



def makeDict(l1, l2, l3, defVal=0):
  ret={}
  for il1 in l1:
    ret[il1]={}
    for il2 in l2:
      ret[il1][il2]={}
      for il3 in l3:
        ret[il1][il2][il3]=0
  return ret


