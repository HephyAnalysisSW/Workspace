import ROOT

def getObjFromFile(fname, hname):
  f = ROOT.TFile(fname)
  assert not f.IsZombie()
  f.cd()
  htmp = f.Get(hname)
  if not htmp:  return htmp
  ROOT.gDirectory.cd('PyROOT:/')
  res = htmp.Clone()
  f.Close()
  return res

def passPUJetID(flag, level="Tight"): #Medium, #Loose,  kTight  = 0,   kMedium = 1,   kLoose  = 2
  if type(level)==type(0):
    return ( flag & (1 << level) ) != 0
  if level=="Tight":
    l=0
  if level=="Medium":
    l=1
  if level=="Loose":
    l=2
  return ( flag & (1 << l) ) != 0

