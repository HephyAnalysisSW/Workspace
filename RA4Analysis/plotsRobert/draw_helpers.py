def muonSelectionStr(minPt=25, maxEta=2.4, minID=1, minRelIso=0.12):
  return "abs(LepGood_pdgId)==13&&LepGood_pt>"+str(minPt)+"&&abs(LepGood_eta)<"+str(maxEta)+"&&LepGood_tightId>="+str(minID)+"&&LepGood_relIso03<"+str(minRelIso)
def electronSelectionStr(minPt=25, maxEta=2.4, minID=3, minRelIso=0.12):
  return "abs(LepGood_pdgId)==11&&LepGood_pt>"+str(minPt)+"&&abs(LepGood_eta)<"+str(maxEta)+"&&LepGood_tightId>="+str(minID)+"&&LepGood_relIso03<"+str(minRelIso)

def exactlyOneTightMuon(minPt=25, maxEta=2.4, minID=1, minRelIso=0.12):
  return "(Sum$("+muonSelectionStr(minPt=minPt, maxEta=maxEta, minID=minID, minRelIso=minRelIso)+")==1)"
def exactlyOneTightElectron(minPt=25, maxEta=2.4, minID=1, minRelIso=0.12):
  return "(Sum$("+electronSelectionStr(minPt=minPt, maxEta=maxEta, minID=minID, minRelIso=minRelIso)+")==1)"
 
def exactlyOneTightLepton(lepton="muon", minPt=25, maxEta=2.4, minID=1, minRelIso=0.12):
  if lepton.lower()=="muon":
    return exactlyOneTightMuon(minPt=minPt, maxEta=maxEta, minID=minID, minRelIso=minRelIso)
  if lepton.lower()=="electron":
    return exactlyOneTightElectron(minPt=minPt, maxEta=maxEta, minID=minID, minRelIso=minRelIso)

def looseLeptonVeto(minPt=10, muMultiplicity=1, eleMultiplicity=0):
  return "(Sum$(abs(LepGood_pdgId)==13&&LepGood_pt>"+str(minPt)+")=="+str(muMultiplicity)+"&&Sum$(abs(LepGood_pdgId)==11&&LepGood_pt>"+str(minPt)+")=="+str(eleMultiplicity)+")"

def nBTagStr(minPt=30, maxEta=2.4, minCMVATag=0.732):
  return "Sum$(Jet_pt>"+str(minPt)+"&&abs(Jet_eta)<"+str(maxEta)+"&&Jet_id&&Jet_btagCMVA>"+str(minCMVATag)+")"

def nBTagCut(btb, minPt=30, maxEta=2.4, minCMVATag=0.732):
  if type(btb)==type([]) or type(btb)==type(()):
    if len(btb)>1 and btb[1]>=00:
      return "("+nBTagStr(minPt=minPt,maxEta=maxEta,minCMVATag=minCMVATag)+">="+str(btb[0])+"&&"+nBTagStr(minPt=minPt,maxEta=maxEta,minCMVATag=minCMVATag)+"<="+str(btb[1])+")"
    else:
      return nBTagCut(btb[0], minPt=minPt,maxEta=maxEta, minCMVATag=minCMVATag)
  else:
    return "("+nBTagStr(minPt=minPt,maxEta=maxEta,minCMVATag=minCMVATag)+">="+str(btb)+")"
    
def nJetStr(minPt=30, maxEta=2.4):
  return "Sum$(Jet_pt>"+str(minPt)+"&&abs(Jet_eta)<"+str(maxEta)+"&&Jet_id)"

def nJetCut(njb, minPt=30, maxEta=2.4):
  if type(njb)==type([]) or type(njb)==type(()):
    if len(njb)>1 and njb[1]>=0:
      return "("+nJetStr(minPt=minPt,maxEta=maxEta)+"="+str(njb[0])+"&&"+nJetStr(minPt=minPt,maxEta=maxEta)+"<="+str(njb[1])+")"
    else: 
      return nJetCut(njb[0], minPt=minPt, maxEta=maxEta)
  else:
    return "("+nJetStr(minPt=minPt,maxEta=maxEta)+">="+str(njb)+")"

def htStr(minPt=30, maxEta=2.4):
  return "Sum$(Jet_pt*(Jet_pt>"+str(minPt)+"&&abs(Jet_eta)<"+str(maxEta)+"&&Jet_id))"
    
def htCut(htb, minPt=30, maxEta=2.4):
  if type(htb)==type([]) or type(htb)==type(()):
    if len(htb)>1 and htb[1]>=0:
      return "("+htStr(minPt=minPt,maxEta=maxEta)+">"+str(htb[0])+"&&"+htStr(minPt=minPt,maxEta=maxEta)+"<="+str(htb[1])+")"
    else:
      return  htCut(htb[0], minPt=minPt, maxEta=maxEta)
  else:
    return "("+htStr(minPt=minPt,maxEta=maxEta)+">"+str(htb)+")"

def stCut(stb, lepton="muon", minPt=25, maxEta=2.4, minID=1, minRelIso=0.12):
  if lepton.lower()=="muon":
    lStr = muonSelectionStr(minPt=minPt, maxEta=maxEta, minID=minID, minRelIso=minRelIso)
  if lepton.lower()=="electron":
    lStr = electronSelectionStr(minPt=minPt, maxEta=maxEta, minID=minID, minRelIso=minRelIso)
  if type(stb)==type([]) or type(stb)==type(()):
    if len(stb)>1 and stb[1]>=0:
      return   "(Sum$((LepGood_pt+met_pt)*("+lStr+")>"+str(stb[0])+")==1&&"\
              +"Sum$((LepGood_pt+met_pt)*("+lStr+")<="+str(stb[1])+")==1 )"
    else:
      return  stCut(stb=stb[0],lepton=lepton, minPt=minPt, maxEta=maxEta, minID=minID, minRelIso=minRelIso)
  else:
    return   "(Sum$((LepGood_pt+met_pt)*("+lStr+")>"+str(stb)+")==1)"

def dPhiCut(minDPhi,lepton="muon", minPt=25, maxEta=2.4, minID=1, minRelIso=0.12):
  if lepton.lower()=="muon":
    lStr = muonSelectionStr(minPt=minPt, maxEta=maxEta, minID=minID, minRelIso=minRelIso)
  if lepton.lower()=="electron":
    lStr = electronSelectionStr(minPt=minPt, maxEta=maxEta, minID=minID, minRelIso=minRelIso)
  return  "(Sum$(acos((LepGood_pt + met_pt*cos(LepGood_phi - met_phi))/sqrt(LepGood_pt**2 + met_pt**2+2*met_pt*LepGood_pt*cos(LepGood_phi-met_phi)))"\
         +"*("+lStr+")>"+str(minDPhi)+")==1)"
