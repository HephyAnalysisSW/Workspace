import ROOT
import pickle
from array import array
##from helpers import gTauAbsEtaBins, gTauPtBins, metParRatioBins, jetRatioBins
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


##ofile =                      '/data/schoef/results2014/tauTuples/CSA14_TTJets_genTau.root'
ofile =  '/data/easilar/convertedTuples_v23/resuls/CSA14_DiLep_noPred_hT.root'


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

 
  for perm in [muons, reversed(muons)]:
    m,m2 = perm
    if m2['isTight']:
#      print iperm, m['isTight'],m2['isTight']
#      print "pt",m['pt'],m['phi'],m['eta']
    	#abseta=abs(m['eta'])
    	#if abseta>=2.3:continue
    	#metpar    = p['frac']*m['pt']
      metpar    = m['pt']   ###confusion in writing MEx and MEy
    	#s.weightPred = p['weight']*s.weight
      s.weight=c.GetLeaf('weight').GetValue()
      s.weightPred = s.weight
      MEx = s.met*cos(s.metphi)+cos(m['phi'])*metpar
      MEy = s.met*sin(s.metphi)+sin(m['phi'])*metpar
      s.metPred = sqrt(MEx**2+MEy**2)
      s.metphiPred = atan2(MEy,MEx)
      #if s.ht>400 and s.met>150 and s.njets>=4:
      s.mTPred = sqrt(2.*s.metPred*m2['pt']*(1-cos(m2['phi']-s.metphiPred)))
      t.Fill()

f.cd()
t.Write()
f.Close()
dir.cd()


