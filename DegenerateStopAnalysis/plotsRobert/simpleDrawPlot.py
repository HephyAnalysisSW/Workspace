import ROOT

cBkg = ROOT.TChain("Events")
#cBkg.Add("/data/imikulec/copy/MC/WJetsHT250/histo_WJetsHT250.root")
#cBkg.Add("/data/imikulec/copy/MC/WJetsToLNu/histo_WJetsToLNu.root")
cBkg.Add('/data/schoef/monoJetTuples_v1/copy/W1JetsToLNu/histo_W1JetsToLNu.root')
cBkg.Add('/data/schoef/monoJetTuples_v1/copy/W2JetsToLNu/histo_W2JetsToLNu.root')
cBkg.Add('/data/schoef/monoJetTuples_v1/copy/W3JetsToLNu/histo_W3JetsToLNu.root')
cBkg.Add('/data/schoef/monoJetTuples_v1/copy/W4JetsToLNu/histo_W4JetsToLNu.root')

#cBkg.Scan('event:isrJetCutBasedPUJetIDFlag:isrJetMET53XPUJetIDFlag:isrJetFull53XPUJetIDFlag:isrJetPt:softIsolatedMuDz','softIsolatedMuPt>0&&isrJetPt>110&&(isrJetCutBasedPUJetIDFlag!=7||isrJetMET53XPUJetIDFlag!=7||isrJetFull53XPUJetIDFlag!=7)&&isrJetPt>110&&isrJetBTBVetoPassed&&softIsolatedMuPt>5&&nHardElectrons+nHardMuons==0&&njet60<=2')

#c.Draw("((Sum$(jetPt>110&&jetChef>0.2&&jetNeef<0.7&&jetNhef<0.7&&jetCeef<0.5))==1)", )

cSig = ROOT.TChain("Events")
cSig.Add("/data/schoef/monoJetTuples_v1/copy/stop300lsp270FastSim/histo_stop300lsp270FastSim.root")

commoncf="isrJetPt>110&&isrJetBTBVetoPassed&&softIsolatedMuPt>5&&nHardElectrons+nHardMuons==0&&njet60<=2"

jetID = "jetChef>0.2&&jetNeef<0.7&&jetNhef<0.7&&jetCeef<0.5"

isrJetSel = "jetPt>110&&"+jetID
softJetSel = "jetPt>30&&"+jetID
#
#muSel       = "muPt>5&&muPt<20&&muIso*muPt<5."
#muSelTight  = "muPt>5&&muPt>20&&muIso*muPt<5."



def sum(s):
  return "Sum$("+s+")"

def select(var, requ, instance=-1):
  if not type(instance)==type(0):
    print "Warning! Selecting instance by other type than int:",instance
  if instance==-1:
    return var+"*("+requ+")"
  else:
    return var+"*("+requ+"&&Iteration$=="+str(instance)+")"
    

def require(what, requStr):
  return "(("+what+")"+requStr+")"

def nth(what, int):
  return require(what, "Iteration$=="+str(num))

#ht30 = sum(select("jetPt", jetID+"&&jetPt>30"))
#njet30 = sum(jetID+"&&jetPt>30")

#cBkg.Draw("jetPt>>h(100,0,500)", "weight*(jetPt>20&&abs(jetEta)<2.5&&"+commoncf+")") 
#cSig.Draw("jetPt",               "weight*(jetPt>20&&abs(jetEta)<2.5&&"+commoncf+")", "same") 


#mT = "sqrt(2.*met*"+sum(select("muPt",muSel))+"*(1.-cos(metphi-"+sum(select("muPhi",muSel))+")))"
#mT = sum(select("sqrt(2.*muPt*met*(1-cos(muPhi-metphi)))",muSel))
#
#sLepSel = "&&".join([require(sum(isrJetSel),'==1'),require(sum(muSel),'==1'), require(sum(muSelTight),"==0"),"met>=250"])
#
#cBkg.Draw(mT, "weight*("+sLepSel+")")
#cSig.Draw(mT, "weight*("+sLepSel+")", "same")
#cBkg.Draw(njet30, "weight*("+sLepSel+")")
#cSig.Draw(njet30, "weight*("+sLepSel+")", "same")

#cBkg.Draw( sum(isrJetSel), "weight*("+sLepSel+")")
#cSig.Draw( sum(isrJetSel), "weight*("+sLepSel+")", "same")


#kTight  = 0,   kMedium = 1,   kLoose  = 2
#cBkg.Draw(select("jetPt", softJetSel, 1), "weight*("+commoncf+"&&(( flag & (1 << level) ) != 0)")
#cSig.Draw(select("jetPt", softJetSel, 1), "weight*("+commoncf+")", "same")
