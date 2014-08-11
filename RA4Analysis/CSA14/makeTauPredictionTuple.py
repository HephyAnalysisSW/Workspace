import ROOT
import pickle
from array import array
from helpers import gTauAbsEtaBins, gTauPtBins, metParRatioBins, jetRatioBins
from Workspace.HEPHYPythonTools.helpers import getVarValue
from objectSelection import getLooseMuStage2, tightPOGMuID, vetoMuID
from stage2Tuples import ttJetsCSA14
from math import sqrt, cos, sin, atan2

c = ROOT.TChain('Events')
for b in ttJetsCSA14['bins']:
  c.Add(ttJetsCSA14['dirname']+'/'+b+'/h*.root')

small = False
maxN=1001

doubleLeptonPreselection = "ngoodMuons>=1&&nvetoMuons==2"

templates = pickle.load(file('/data/schoef/results2014/tauTemplates/CSA14_TTJets_genTau.pkl'))
ofile =                      '/data/schoef/results2014/tauTuples/CSA14_TTJets_genTau.root'

for ptk in templates.keys():
  for etak in templates[ptk].keys():
    templates[ptk][etak].Scale(1./templates[ptk][etak].Integral())
    res=[]
    for b in range(1, 1+templates[ptk][etak].GetNbinsX()):
      res.append({'frac':templates[ptk][etak].GetBinCenter(b), 'weight':templates[ptk][etak].GetBinContent(b)})
    templates[ptk][etak]=res

def getTwoMuons(c):
  nmuCount = int(getVarValue(c, 'nmuCount' ))
  res=[]
  nt=0
  nl=0
  for i in range(nmuCount):
    l=getLooseMuStage2(c, i)
    isTight=tightPOGMuID(l)
    isLoose=vetoMuID(l)
    l['isTight'] = isTight 
    l['isLoose'] = isLoose
    if isTight:nt+=1
    if isLoose:nl+=1
    if isTight or isLoose: res.append(l)
  if len(res)!=2: print "Warning: found",len(l),'muons -> inconsistent with preselection!!'
  if not (nt>=1 and nl==2):print "Warning! Not >=1 tight and ==2 loose -> Inconsistent w/ preselection"
  return res

def getTypeStr(s):
  if s=='l': return 'ULong64_t'
  if s=='F': return 'Float_t'
  if s=='I': return 'Int_t'

copyVars  = ['event/l', 'njets/I', 'ht/F', 'met/F', 'metphi/F']
newVars   = ['njetsPred/I', 'htPred/F', 'metPred/F', 'metphiPred/F','weightPred/F', 'mTPred/F', 'weight/F']
vars      = copyVars+newVars  

structString = "struct MyStruct{"
structString+= "".join([getTypeStr(v.split('/')[1])+" "+v.split('/')[0]+";" for v in vars])
structString+="}"   
ROOT.gROOT.ProcessLine(structString)
exec("from ROOT import MyStruct")
exec("s = MyStruct()")
dir=ROOT.gDirectory.func()

f=ROOT.TFile(ofile, 'recreate')
f.cd()
t = ROOT.TTree( "Events", "Events", 1 )
for v in vars:
 t.Branch(v.split('/')[0],   ROOT.AddressOf(s,v.split('/')[0]), v) 
dir.cd()

c.Draw(">>eList", doubleLeptonPreselection)
eList = ROOT.gDirectory.Get("eList")
number_events = eList.GetN()
if small:
  if number_events>maxN:
    number_events=maxN
number_events=min(number_events, eList.GetN())
for i in range(number_events):
  if (i%10000 == 0) and i>0 :
    print i,"/",number_events
  c.GetEntry(eList.GetEntry(i))
  s.event = long(c.GetLeaf('event').GetValue())
  for v in copyVars[1:]:
    n=v.split('/')[0]
    exec('s.'+n+'='+str(c.GetLeaf(n).GetValue()))
  muons = getTwoMuons(c)
  assert len(muons)==2
 
  for iperm, m12 in enumerate([muons, reversed(muons)]):
    m,m2=m12
    if m2['isTight']:
#      print iperm, m['isTight'],m2['isTight']
#      print "pt",m['pt'],m['phi'],m['eta']
      abseta=abs(m['eta'])
      if abseta>=2.3:continue
      template=None
      for ptb in gTauPtBins:
        if m['pt']>=ptb[0] and (m['pt']<ptb[1] or ptb[1]<0):
          for etab in gTauAbsEtaBins:
            if abseta>=etab[0] and abseta<etab[1]:
              template=templates[ptb][etab]
              break
          if template:break
      assert template, "No template found for muon: %r" % repr(m)
#      print template 
      s.weight=c.GetLeaf('weight').GetValue()/len(template)
      for p in template:
        metpar    = p['frac']*m['pt']
        s.weightPred = p['weight']*s.weight
        MEx = s.met*cos(s.metphi)+cos(m['phi'])*metpar
        MEy = s.met*sin(s.metphi)+sin(m['phi'])*metpar

        s.metPred = sqrt(MEx**2+MEy**2)
        s.metphiPred = atan2(MEy,MEx)
        jetpt =  (1.-p['frac'])*m['pt']
        if jetpt>30.:
          s.njetsPred = s.njets+1
          s.htPred   = s.ht+jetpt
        else:
          s.njetsPred = s.njets
          s.htPred   = s.ht
        s.mTPred = sqrt(2.*s.metPred*m2['pt']*(1-cos(m2['phi']-s.metphiPred)))
        t.Fill()

f.cd()
t.Write()
f.Close()
dir.cd()

