#def electronSelectionStr(minPt=25, maxEta=2.4, minID=3, minRelIso=0.14):
#  return "abs(LepGood_pdgId)==11&&LepGood_pt>"+str(minPt)+"&&abs(LepGood_eta)<"+str(maxEta)+"&&LepGood_tightId>="+str(minID)+"&&LepGood_relIso03<"+str(minRelIso)
#def muonSelectionStr(minPt=25, maxEta=2.4, minID=1, minRelIso=0.12):
#  return "abs(LepGood_pdgId)==13&&LepGood_pt>"+str(minPt)+"&&abs(LepGood_eta)<"+str(maxEta)+"&&LepGood_tightId>="+str(minID)+"&&LepGood_relIso03<"+str(minRelIso)
#def anyLeptonSelectionStr(minPt=(25,25), maxEta=(2.4,2.4), minID=(3,1), minRelIso=(0.14,0.12)):
#  assert len(minPt)==2 and len(maxEta)==2 and len(minID)==2 and len(minRelIso)==2, "leptonSelectionStr: Not all args of length 2!"
#  return "abs(LepGood_pdgId)==11&&LepGood_pt>"+str(minPt[0])+"&&abs(LepGood_eta)<"+str(maxEta[0])+"&&LepGood_tightId>="+str(minID[0])+"&&LepGood_relIso03<"+str(minRelIso[0])+\
#       "||abs(LepGood_pdgId)==13&&LepGood_pt>"+str(minPt[1])+"&&abs(LepGood_eta)<"+str(maxEta[1])+"&&LepGood_tightId>="+str(minID[1])+"&&LepGood_relIso03<"+str(minRelIso[1])
#
#def exactlyOneTightMuon(minPt=25, maxEta=2.4, minID=1, minRelIso=0.12):
#  return "(Sum$("+muonSelectionStr(minPt=minPt, maxEta=maxEta, minID=minID, minRelIso=minRelIso)+")==1)"
#def exactlyOneTightElectron(minPt=25, maxEta=2.4, minID=1, minRelIso=0.14):
#  return "(Sum$("+electronSelectionStr(minPt=minPt, maxEta=maxEta, minID=minID, minRelIso=minRelIso)+")==1)"
 
def exactlyOneTightLepton(lepton="muon"):
  if lepton.lower()=="muon":
    #return exactlyOneTightMuon(minPt=minPt, maxEta=maxEta, minID=minID, minRelIso=minRelIso)
    return "singleMuonic"
  if lepton.lower()=="electron":
    #return exactlyOneTightElectron(minPt=minPt, maxEta=maxEta, minID=minID, minRelIso=minRelIso)
    return "singleElectronic"
  if lepton.lower()=="both":
    #assert len(minPt)==2 and len(maxEta)==2 and len(minID)==2 and len(minRelIso)==2, "exactlyOneTightLepton: Not all args of length 2!"
    #return "(Sum$("+anyLeptonSelectionStr(minPt=minPt, maxEta=maxEta, minID=minID, minRelIso=minRelIso)+")==1)" 
    return "singleLeptonic"

def looseLeptonVeto(lepton, minPt=10):
  if lepton=="muon":
    #return "(Sum$(abs(LepGood_pdgId)==13&&LepGood_pt>"+str(minPt)+")==1&&Sum$(abs(LepGood_pdgId)==11&&LepGood_pt>"+str(minPt)+")==0)"
    return "nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0"
  if lepton=="electron":
    #return "(Sum$(abs(LepGood_pdgId)==13&&LepGood_pt>"+str(minPt)+")==0&&Sum$(abs(LepGood_pdgId)==11&&LepGood_pt>"+str(minPt)+")==1)"
    return "nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0"
  if lepton=="both":
    #return "(Sum$(abs(LepGood_pdgId)==13&&LepGood_pt>"+str(minPt)+") + Sum$(abs(LepGood_pdgId)==11&&LepGood_pt>"+str(minPt)+")==1)"
    return "nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0"

def nBTagStr():
  #return "Sum$(Jet_pt>"+str(minPt)+"&&abs(Jet_eta)<"+str(maxEta)+"&&Jet_id&&Jet_btagCMVA>"+str(minCMVATag)+")"
   return "nBJetMediumCSV30"
def nBTagCut(btb):
  if type(btb)==type([]) or type(btb)==type(()):
    if len(btb)>1 and btb[1]>=0:
      if btb[0]==btb[1]:
        return "("+nBTagStr()+"=="+str(btb[0])+")"
      else:
        return "("+nBTagStr()+">="+str(btb[0])+"&&"+nBTagStr()+"<="+str(btb[1])+")"
    else:
      return nBTagCut(btb[0])
  else:
    return "("+nBTagStr()+">="+str(btb)+")"
    
def nJetStr():
   return "nJet30"

def nJetCut(njb):
  if type(njb)==type([]) or type(njb)==type(()):
    if len(njb)>1 and njb[1]>=0:
      if njb[0]==njb[1]:
        return "("+nJetStr()+"=="+str(njb[0])+")"
      else:
        return "("+nJetStr()+">="+str(njb[0])+"&&"+nJetStr()+"<="+str(njb[1])+")"
    else: 
      return nJetCut(njb[0], minPt=minPt, maxEta=maxEta)
  else:
    return "("+nJetStr()+">="+str(njb)+")"

def htStr():
     return "htJet30j"

def jet2Ptcut():
    return "(Jet_pt[1]>80)"
    
def htCut(htb):
  if type(htb)==type([]) or type(htb)==type(()):
    if len(htb)>1 and htb[1]>=0:
      return "("+htStr()+">"+str(htb[0])+"&&"+htStr()+"<="+str(htb[1])+")"
    else:
      return  htCut(htb[0])
  else:
    return "("+htStr()+">"+str(htb)+")"

def stCut(stb):
  if type(stb)==type([]) or type(stb)==type(()):
    if len(stb)>1 and stb[1]>=0:
      return   "(st>"+str(stb[0])+"&&"\
              +"st<="+str(stb[1])+" )"
    else:
      return  stCut(stb=stb[0])
  else:
    return   "(st>"+str(stb)+")"

def dPhiCut(minDPhi):
  return  "(deltaPhi_Wl>"+str(minDPhi)+")"

def dPhiCut_r(minDPhi):
  return  "(deltaPhi_Wl<="+str(minDPhi)+")"
