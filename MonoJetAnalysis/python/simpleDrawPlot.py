import ROOT

cBkg = ROOT.TChain("Events")
cBkg.Add("/data/imikulec/copy/MC/WJetsHT250/histo_WJetsHT250.root")
#cBkg.Add("/data/imikulec/copy/MC/WJetsToLNu/histo_WJetsToLNu.root")
cSig = ROOT.TChain("Events")
cSig.Add("/data/imikulec/copy/MC/S300N270/histo_S300N270.root")

jetID = "jetChef>0.2&&jetNeef<0.7&&jetNhef<0.7&&jetCeef<0.5"

isrJetSel = "jetPt>110&&"+jetID
softJetSel = "jetPt>30&&"+jetID

muSel       = "muPt>5&&muPt<20&&muIso*muPt<5."
muSelTight  = "muPt>5&&muPt>20&&muIso*muPt<5."


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

ht30 = sum(select("jetPt", jetID+"&&jetPt>30"))
njet30 = sum(jetID+"&&jetPt>30")

#mT = "sqrt(2.*met*"+sum(select("muPt",muSel))+"*(1.-cos(metphi-"+sum(select("muPhi",muSel))+")))"
mT = sum(select("sqrt(2.*muPt*met*(1-cos(muPhi-metphi)))",muSel))

sLepSel = "&&".join([require(sum(isrJetSel),'==1'),require(sum(muSel),'==1'), require(sum(muSelTight),"==0"),"met>=250"])

cBkg.Draw(mT, "weight*("+sLepSel+")")
cSig.Draw(mT, "weight*("+sLepSel+")", "same")
#cBkg.Draw(njet30, "weight*("+sLepSel+")")
#cSig.Draw(njet30, "weight*("+sLepSel+")", "same")

#cBkg.Draw( sum(isrJetSel), "weight*("+sLepSel+")")
#cSig.Draw( sum(isrJetSel), "weight*("+sLepSel+")", "same")

#cBkg.Draw(select("jetPt", softJetSel, 1), "weight*("+sLepSel+")")
#cSig.Draw(select("jetPt", softJetSel, 1), "weight*("+sLepSel+")", "same")
