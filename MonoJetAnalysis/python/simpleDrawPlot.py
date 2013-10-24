import ROOT

cBkg = ROOT.TChain("Events")
cBkg.Add("/data/imikulec/copy/MC/WJetsHT250/histo_WJetsHT250.root")
#cBkg.Add("/data/imikulec/copy/MC/WJetsToLNu/histo_WJetsToLNu.root")
cSig = ROOT.TChain("Events")
cSig.Add("/data/imikulec/copy/MC/S300N270/histo_S300N270.root")

jetID = "jetChef>0.2&&jetNeef<0.7&&jetNhef<0.7&&jetCeef<0.5"

isrJetSel = "jetPt>110&&"+jetID

muSel  = "muPt>5&&muPt<20&&muIso<5."


def sum(s):
  return "Sum$("+s+")"

def specify(var, requ):
  return var+"*("+requ+")"

def require(what, requStr):
  return "(("+what+")"+requStr+")"

ht30 = sum(specify("jetPt", jetID+"&&jetPt>30"))
njet30 = sum(jetID+"&&jetPt>30")

#mT = "sqrt(2.*met*"+sum(specify("muPt",muSel))+"*(1.-cos(metphi-"+sum(specify("muPhi",muSel))+")))"
mT = sum(specify("sqrt(2.*muPt*met*(1-cos(muPhi-metphi)))",muSel))

sLepSel = "&&".join([require(ht30,">=300"),require(sum(isrJetSel),'==1'),require(sum(muSel),'==1'),"met>=0"])

cBkg.Draw(mT, "weight*("+sLepSel+")")
cSig.Draw(mT, "weight*("+sLepSel+")", "same")
#cBkg.Draw(njet30, "weight*("+sLepSel+")")
#cSig.Draw(njet30, "weight*("+sLepSel+")", "same")
