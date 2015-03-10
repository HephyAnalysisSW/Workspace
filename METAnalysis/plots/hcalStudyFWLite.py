import ROOT
from DataFormats.FWLite import Events, Handle
from PhysicsTools.PythonAnalysis import *
from math import *
import sys, os, copy, random, subprocess, datetime
import pickle

ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.AutoLibraryLoader.enable()

ROOT.gROOT.ProcessLine(".L ../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.gROOT.ProcessLine(".L ../../HEPHYPythonTools/scripts/root/useNiceColorPalette.C")

ROOT.gStyle.SetOptStat(0)
ROOT.setTDRStyle()
ROOT.tdrStyle.SetPadRightMargin(0.18)
if type(ROOT.tdrStyle)!=type(ROOT.gStyle):
  del ROOT.tdrStyle
  ROOT.setTDRStyle()

ROOT.useNiceColorPalette(255)
printDir = "/afs/hephy.at/user/s/schoefbeck/www/png73XCalo/"
maxEvts=-1

#53X PromptReco JetHT RECO 203835
#files = [
#  'root://eoscms.cern.ch//eos/cms/store/data/Run2012D/JetHT/RECO/PromptReco-v1/000/203/835/2418E19C-7E0B-E211-BA6E-0019B9F70468.root',
#  'root://eoscms.cern.ch//eos/cms/store/data/Run2012D/JetHT/RECO/PromptReco-v1/000/203/835/32130242-8C0B-E211-A5E8-003048D2C0F2.root',
#  'root://eoscms.cern.ch//eos/cms/store/data/Run2012D/JetHT/RECO/PromptReco-v1/000/203/835/34151EB5-800B-E211-82F8-001D09F29524.root',
#  'root://eoscms.cern.ch//eos/cms/store/data/Run2012D/JetHT/RECO/PromptReco-v1/000/203/835/404A4DE0-760B-E211-831F-003048D2C020.root',
#  'root://eoscms.cern.ch//eos/cms/store/data/Run2012D/JetHT/RECO/PromptReco-v1/000/203/835/9E999D7B-880B-E211-9F7F-001D09F2A49C.root',
#  'root://eoscms.cern.ch//eos/cms/store/data/Run2012D/JetHT/RECO/PromptReco-v1/000/203/835/C2405F36-8C0B-E211-AEC5-003048D2BD66.root'
#]
#73X RECO of JetHT_RECO_GR_R_73_V0_HcalExtValid_RelVal_jet2012D_v2
#from files import JetHT_RECO_GR_R_73_V0_HcalExtValid_RelVal_jet2012D_v2
#files = JetHT_RECO_GR_R_73_V0_HcalExtValid_RelVal_jet2012D_v2

#53X Jan22 rereco JetHT AOD of run 208352
files_53X=[
'root://eoscms.cern.ch//eos/cms/store/cmst3/group/susy/schoef/Run2012D_JetHT_AOD_22Jan2013-v1_10001_CE3F0E9D-E496-E211-AF4F-001EC9D7F1F3.root',
'root://eoscms.cern.ch//eos/cms/store/cmst3/group/susy/schoef/Run2012D_JetHT_AOD_22Jan2013-v1_10001_E44B778C-2897-E211-8D62-00259073E482.root',
'root://eoscms.cern.ch//eos/cms/store/cmst3/group/susy/schoef/Run2012D_JetHT_AOD_22Jan2013-v1_10001_F241442B-1D97-E211-ABC8-00259073E446.root',
'root://eoscms.cern.ch//eos/cms/store/cmst3/group/susy/schoef/Run2012D_JetHT_AOD_22Jan2013-v1_10002_ECCBD06E-4B97-E211-A0FB-0025907277BE.root',
]
##73X JetHT_RECO_GR_R_73_V0_HcalExtValid_RelVal_jet2012D_v2 RECO run 208352
files_73X=['root://eoscms.cern.ch//store/relval/CMSSW_7_3_2_patch1/JetHT/RECO/GR_R_73_V0_HcalExtValid_RelVal_jet2012D-v2/00000/0C38D6DD-2FB5-E411-9EE7-0025905964CC.root',
 'root://eoscms.cern.ch//store/relval/CMSSW_7_3_2_patch1/JetHT/RECO/GR_R_73_V0_HcalExtValid_RelVal_jet2012D-v2/00000/28287B06-29B5-E411-9D08-0025905A612A.root',
 'root://eoscms.cern.ch//store/relval/CMSSW_7_3_2_patch1/JetHT/RECO/GR_R_73_V0_HcalExtValid_RelVal_jet2012D-v2/00000/3813BA50-31B5-E411-8FED-003048FFD71E.root',
 'root://eoscms.cern.ch//store/relval/CMSSW_7_3_2_patch1/JetHT/RECO/GR_R_73_V0_HcalExtValid_RelVal_jet2012D-v2/00000/40E2486B-1AB5-E411-89D8-0025905A608C.root',
 'root://eoscms.cern.ch//store/relval/CMSSW_7_3_2_patch1/JetHT/RECO/GR_R_73_V0_HcalExtValid_RelVal_jet2012D-v2/00000/64DFB678-28B5-E411-AF21-0025905A60EE.root',
 'root://eoscms.cern.ch//store/relval/CMSSW_7_3_2_patch1/JetHT/RECO/GR_R_73_V0_HcalExtValid_RelVal_jet2012D-v2/00000/A2FEE11F-30B5-E411-8515-0025905A612A.root',
 'root://eoscms.cern.ch//store/relval/CMSSW_7_3_2_patch1/JetHT/RECO/GR_R_73_V0_HcalExtValid_RelVal_jet2012D-v2/00000/C6F1138A-31B5-E411-99DA-0025905A48FC.root',
 'root://eoscms.cern.ch//store/relval/CMSSW_7_3_2_patch1/JetHT/RECO/GR_R_73_V0_HcalExtValid_RelVal_jet2012D-v2/00000/CE5D6E95-25B5-E411-96C5-0025905A608C.root',
 'root://eoscms.cern.ch//store/relval/CMSSW_7_3_2_patch1/JetHT/RECO/GR_R_73_V0_HcalExtValid_RelVal_jet2012D-v2/00000/FA472010-33B5-E411-B8E3-0025905A610C.root',
 'root://eoscms.cern.ch//store/relval/CMSSW_7_3_2_patch1/JetHT/RECO/GR_R_73_V0_HcalExtValid_RelVal_jet2012D-v2/00000/FC998BD1-34B5-E411-AD7B-0025905938A8.root']

from vetoed import vetoed as vetoedEvents73X
from passed53XFilters import  passed53XFilters as  passed53XFilters

edmCollections = [ \
  ("vector<reco::PFMET>", "pfMet", ""), #, "RECO")
  ("vector<reco::CaloMET>", "caloMet", ""), #, "RECO")
#  ("vector<reco::CaloMET>", "caloMet"                   ""                "reRECO"
  ("vector<reco::PFCandidate>", "particleFlow", "")
] 

label = {"X":0,"h":1, "e":2, "mu":3,"gamma":4, 'h0':5, 'h_HF':6, 'egamma_HF':7, 0:"X",1:"h", 2:"e", 3:"mu",4:"gamma", 5:'h0', 6:'h_HF', 7:'egamma_HF'}
pfTypes = ["h", "h0", "gamma","e", "h_HF", "egamma_HF", "mu"]

handles={v[1]:Handle(v[0]) for v in edmCollections}
res={}
for files, ver in [[files_53X, "53X"],[files_73X,"73X"]]:
  print "Reading",ver,"files",files
  res[ver]={}
  events = Events(files)
  events.toBegin()
  fileNames=events._filenames
  usedFiles=[]
  runs=[]
  products={}
  size=events.size()
  for nev in range(size):
    if nev%10000==0:print nev,'/',size
    events.to(nev)
    eaux=events.eventAuxiliary()
    run=eaux.run()            
    if run==208352:
      event=eaux.event()
      lumi=eaux.luminosityBlock()
      k = ":".join(str(x) for x in [run,lumi,event])
      if k in vetoedEvents73X:
        print "Event vetoed (73X)"
        continue
      if not k in passed53XFilters:
        print "Event vetoed (53X)"
        continue
      for v in edmCollections:
        events.getByLabel(v[1:],handles[v[1]])
        products[v[1]] =handles[v[1]].product()
      sumPt={"sumPt_"+t:0. for t in pfTypes}
      MEx={"MEx_"+t:0. for t in pfTypes}
      MEy={"MEy_"+t:0. for t in pfTypes}
      subdet = {"MEx_ecal":0., "MEx_hcal":0,"MEx_ho":0., "MEy_ecal":0.,"MEy_hcal":0.,"MEy_ho":0.,"sumEt_ecal":0.,"sumEt_hcal":0.,"sumEt_ho":0. }
      mult={"mult_"+t:0 for t in pfTypes}
      for p in range(products['particleFlow'].size()):
        cand = products['particleFlow'][p]
        sumPt["sumPt_"+label[cand.particleId()]]+=cand.pt() 
        mult["mult_"+label[cand.particleId()]]+=1 
        MEx["MEx_"+label[cand.particleId()]]+=-cand.px() 
        MEy["MEy_"+label[cand.particleId()]]+=-cand.py()
        phi = cand.phi()
        cphi,sphi = cos(phi), sin(phi)
        subdet["MEx_ecal"]+=-cphi*cand.rawEcalEnergy()
        subdet["MEx_hcal"]+=-cphi*cand.rawHcalEnergy()
        subdet["MEx_ho"]+=  -cphi*cand.rawHoEnergy()
        subdet["MEy_ecal"]+=-sphi*cand.rawEcalEnergy()
        subdet["MEy_hcal"]+=-sphi*cand.rawHcalEnergy()
        subdet["MEy_ho"]+=  -sphi*cand.rawHoEnergy()
        subdet["sumEt_ecal"]+=cand.rawEcalEnergy()
        subdet["sumEt_hcal"]+=cand.rawHcalEnergy()
        subdet["sumEt_ho"]+=cand.rawHoEnergy()
      d={'met':products["pfMet"][0].pt(),  'sumEt':products["pfMet"][0].sumEt(), 'metPhi':products["pfMet"][0].phi()}
      d.update({'caloMet':products["caloMet"][0].pt(),  'caloSumEt':products["caloMet"][0].sumEt(), 'caloMetPhi':products["caloMet"][0].phi()})
      d.update(sumPt)
      d.update(subdet)
      d.update(MEx)
      d.update(MEy)
      d.update(mult)
      res[ver][k] = d
for m in ['53X','73X']:
  for k in res[m].keys():
    for p in pfTypes:
      res[m][k]["MET_"+p] = sqrt( res[m][k]["MEx_"+p]**2+ res[m][k]["MEy_"+p]**2)
pickle.dump(res, file('res.pkl', 'w'))

res = pickle.load(file('res.pkl'))

commonKeys =  [val for val in res['53X'].keys() if val in res['73X'].keys()]
print "Have",len(commonKeys),"events in common"
outliers={'met':[], 'sumEt':[],'caloMet':[],'caloSumEt':[]}
outliers.update({"sumPt_"+p:[] for p in pfTypes})
outliers.update({"MET_"+p:[] for p in pfTypes})
for k in commonKeys:
  outliers['met'].append(   [res['73X'][k]['met'] - res['53X'][k]['met'],k,res['73X'][k]['met'],  res['53X'][k]['met']] )
  outliers['sumEt'].append( [res['73X'][k]['sumEt'] - res['53X'][k]['sumEt'],k, res['73X'][k]['sumEt'], res['53X'][k]['sumEt']] )
  outliers['caloMet'].append(   [res['73X'][k]['caloMet'] - res['53X'][k]['caloMet'],k,res['73X'][k]['caloMet'],  res['53X'][k]['caloMet']] )
  outliers['caloSumEt'].append( [res['73X'][k]['caloSumEt'] - res['53X'][k]['caloSumEt'],k, res['73X'][k]['caloSumEt'], res['53X'][k]['caloSumEt']] )
  for p in pfTypes:
    outliers["sumPt_"+p].append([res['73X'][k]["sumPt_"+p] -  res['53X'][k]["sumPt_"+p], k, res['73X'][k]["sumPt_"+p], res['73X'][k]['mult_'+p], res['53X'][k]["sumPt_"+p], res['53X'][k]['mult_'+p]])
    outliers["MET_"+p].append([sqrt(res['73X'][k]["MEx_"+p]**2 +res['73X'][k]["MEy_"+p]**2) - sqrt(res['53X'][k]["MEx_"+p]**2 +res['53X'][k]["MEy_"+p]**2),k,sqrt(res['73X'][k]["MEx_"+p]**2 +res['73X'][k]["MEy_"+p]**2), res['73X'][k]['mult_'+p], sqrt(res['53X'][k]["MEx_"+p]**2 +res['53X'][k]["MEy_"+p]**2), res['53X'][k]['mult_'+p]])

outliers['sumEt'].sort(reverse=True)
outliers['met'].sort(reverse=True)
for p in pfTypes:
  outliers['sumPt_'+p].sort(reverse=True)
  outliers['MET_'+p].sort(reverse=True)

print "*************************"
print "** Outliers: total met **"
print "*************************"
for i, o in enumerate(filter(lambda x:abs(x[0])>100, outliers['met'][:10]+outliers['met'][-10:])):
  print "%2i met(73X-53X) %8.1f id %20s MET %8.1f (73X) %8.1f (53X)"%tuple([i]+o)+ " Details:"+" ".join([("sumPt_"+p2+"%8.1f (53X) %8.1f (73X)  MET_"+p2+"%8.1f (53X) %8.1f (73X)") %(res['53X'][o[1]]['sumPt_'+p2],res['73X'][o[1]]['sumPt_'+p2],res['53X'][o[1]]['MET_'+p2],res['73X'][o[1]]['MET_'+p2]) for p2 in pfTypes ]) 
print "****************************"
print "** Outliers: total sumET **"
print "****************************"
for o in outliers['sumEt'][:10]+outliers['sumEt'][-10:]:
  if abs(o[0])>100:
    print "sumEt(73X-53X) %8.1f id %20s sumEt %8.1f (73X) %8.1f (53X)"%tuple(o) + " Details:"+" ".join([("sumPt_"+p2+"%8.1f (53X) %8.1f (73X)  MET_"+p2+"%8.1f (53X) %8.1f (73X)") %(res['53X'][o[1]]['sumPt_'+p2],res['73X'][o[1]]['sumPt_'+p2],res['53X'][o[1]]['MET_'+p2],res['73X'][o[1]]['MET_'+p2]) for p2 in pfTypes ])
print "*****************************"
print "** Outliers: total caloMet **"
print "*****************************"
for i, o in enumerate(filter(lambda x:abs(x[0])>100, outliers['caloMet'][:10]+outliers['caloMet'][-10:])):
  print "%2i met(73X-53X) %8.1f id %20s caloMET %8.1f (73X) %8.1f (53X)"%tuple([i]+o)+ " Details:"+" ".join([("sumPt_"+p2+"%8.1f (53X) %8.1f (73X)  MET_"+p2+"%8.1f (53X) %8.1f (73X)") %(res['53X'][o[1]]['sumPt_'+p2],res['73X'][o[1]]['sumPt_'+p2],res['53X'][o[1]]['MET_'+p2],res['73X'][o[1]]['MET_'+p2]) for p2 in pfTypes ]) 
print "*******************************"
print "** Outliers: total caloSumET **"
print "*******************************"
for o in outliers['caloSumEt'][:10]+outliers['caloSumEt'][-10:]:
  if abs(o[0])>100:
    print "sumEt(73X-53X) %8.1f id %20s sumEt %8.1f (73X) %8.1f (53X)"%tuple(o) + " Details:"+" ".join([("sumPt_"+p2+"%8.1f (53X) %8.1f (73X)  MET_"+p2+"%8.1f (53X) %8.1f (73X)") %(res['53X'][o[1]]['sumPt_'+p2],res['73X'][o[1]]['sumPt_'+p2],res['53X'][o[1]]['MET_'+p2],res['73X'][o[1]]['MET_'+p2]) for p2 in pfTypes ])
print "***************************************"
print "** Outliers sub-sums (MET and sumET) **"
print "***************************************"
for p in pfTypes:
  print "Outliers: Met "+p
  for o in outliers['MET_'+p][:10]+outliers['MET_'+p][-10:]:
    if abs(o[0])>100:
      print "MET "+p+" (73X-53X) %8.1f id %20s 73X: %8.1f (n=%4i) 53X: %8.1f (n=%4i)"%tuple(o)+ " Details:"+" ".join([("sumPt_"+p2+"%8.1f (53X) %8.1f (73X)  MET_"+p2+"%8.1f (53X) %8.1f (73X)") %(res['53X'][o[1]]['sumPt_'+p2],res['73X'][o[1]]['sumPt_'+p2],res['53X'][o[1]]['MET_'+p2],res['73X'][o[1]]['MET_'+p2]) for p2 in pfTypes ]) 
  print "Outliers: sumPt "+p
  for o in outliers['sumPt_'+p][:10]+outliers['sumPt_'+p][-10:]:
    if abs(o[0])>100:
      print "sumPt "+p+" (73X-53X) %8.1f id %20s 73X: %8.1f (n=%4i) 53X: %8.1f (n=%4i)"%tuple(o) + " Details:"+" ".join([("sumPt_"+p2+"%8.1f (53X) %8.1f (73X)  MET_"+p2+"%8.1f (53X) %8.1f (73X)") %(res['53X'][o[1]]['sumPt_'+p2],res['73X'][o[1]]['sumPt_'+p2],res['53X'][o[1]]['MET_'+p2],res['73X'][o[1]]['MET_'+p2]) for p2 in pfTypes ])

import ROOT
sumEt = ROOT.TH2F('sumEt','sumEt',100,0,5000,100,0,5000)
met = ROOT.TH2F('met','met',100,0,500,100,0,500)
caloSumEt = ROOT.TH2F('caloSumEt','caloSumEt',100,0,5000,100,0,5000)
caloMet = ROOT.TH2F('caloMet','caloMet',100,0,500,100,0,500)
metPhi = ROOT.TH2F('met','met',100,-pi,pi,100,-pi,pi)
metPhi50 = ROOT.TH2F('met','met',100,-pi,pi,100,-pi,pi)
sumEts={}
METs={}
for p in pfTypes:
  sumEts[p] = ROOT.TH2F('sumEt','sumEt',500,0,5000,500,0,5000)
  METs[p] = ROOT.TH2F('MET','MET',500,0,5000,500,0,5000)
 
for k in commonKeys:
  met.Fill(res['53X'][k]['met'], res['73X'][k]['met'])
  sumEt.Fill(res['53X'][k]['sumEt'], res['73X'][k]['sumEt'])
  caloMet.Fill(res['53X'][k]['caloMet'], res['73X'][k]['caloMet'])
  caloSumEt.Fill(res['53X'][k]['caloSumEt'], res['73X'][k]['caloSumEt'])
  metPhi.Fill(res['53X'][k]['metPhi'], res['73X'][k]['metPhi'])
  if res['53X'][k]['met']>50:
    metPhi50.Fill(res['53X'][k]['metPhi'], res['73X'][k]['metPhi'])
  for p in pfTypes:
    sumEts[p].Fill(res['53X'][k]["sumPt_"+p], res['73X'][k]["sumPt_"+p])
    METs[p].Fill(sqrt(res['53X'][k]["MEx_"+p]**2 +res['53X'][k]["MEy_"+p]**2) , sqrt(res['73X'][k]["MEx_"+p]**2 +res['73X'][k]["MEy_"+p]**2))

metPhi.GetXaxis().SetTitle("53X #phi(MET)")
metPhi.GetXaxis().SetLabelSize(0.04)
metPhi.GetYaxis().SetTitle("73X #phi(MET)")
metPhi.GetYaxis().SetLabelSize(0.04)
metPhi50.GetXaxis().SetTitle("53X #phi(MET)")
metPhi50.GetXaxis().SetLabelSize(0.04)
metPhi50.GetYaxis().SetTitle("73X #phi(MET)")
metPhi50.GetYaxis().SetLabelSize(0.04)
met.GetXaxis().SetTitle("53X MET")
met.GetXaxis().SetLabelSize(0.04)
met.GetYaxis().SetLabelSize(0.04)
met.GetYaxis().SetTitle("73X MET")
sumEt.GetXaxis().SetTitle("53X sumEt")
sumEt.GetYaxis().SetTitle("73X sumEt")
sumEt.GetYaxis().SetLabelSize(0.04)
sumEt.GetXaxis().SetLabelSize(0.04)
sumEt.GetXaxis().SetRangeUser(0,3000)
sumEt.GetYaxis().SetRangeUser(0,3000)
caloMet.GetXaxis().SetTitle("53X caloMET")
caloMet.GetXaxis().SetLabelSize(0.04)
caloMet.GetYaxis().SetLabelSize(0.04)
caloMet.GetYaxis().SetTitle("73X caloMET")
caloSumEt.GetXaxis().SetTitle("53X caloSumEt")
caloSumEt.GetYaxis().SetTitle("73X caloSumEt")
caloSumEt.GetYaxis().SetLabelSize(0.04)
caloSumEt.GetXaxis().SetLabelSize(0.04)
caloSumEt.GetXaxis().SetRangeUser(0,3000)
caloSumEt.GetYaxis().SetRangeUser(0,3000)

for p in sumEts.keys():
  sumEts[p].GetXaxis().SetTitle("53X sumEt "+p)
  sumEts[p].GetYaxis().SetTitle("73X sumEt "+p)
  sumEts[p].GetYaxis().SetLabelSize(0.04)
  sumEts[p].GetXaxis().SetLabelSize(0.04)
  sumEts[p].GetXaxis().SetRangeUser(0,1000)
  sumEts[p].GetYaxis().SetRangeUser(0,1000)
sumEts['h'].GetXaxis().SetRangeUser(0,2000)
sumEts['h'].GetYaxis().SetRangeUser(0,2000)
for p in METs.keys():
  METs[p].GetXaxis().SetTitle("53X MET from "+p)
  METs[p].GetYaxis().SetTitle("73X MET from "+p)
  METs[p].GetYaxis().SetLabelSize(0.04)
  METs[p].GetXaxis().SetLabelSize(0.04)
  METs[p].GetXaxis().SetRangeUser(0,800)
  METs[p].GetYaxis().SetRangeUser(0,800)

c1 = ROOT.TCanvas()
met.Draw('colz')
c1.Print(printDir+'/'+'met.png')
c1.Print(printDir+'/'+'met.pdf')
metPhi.Draw('colz')
c1.Print(printDir+'/'+'metPhi.png')
c1.Print(printDir+'/'+'metPhi.pdf')
metPhi50.Draw('colz')
c1.Print(printDir+'/'+'metPhi50.png')
c1.Print(printDir+'/'+'metPhi50.pdf')
sumEt.Draw('colz')
c1.Print(printDir+'/'+'sumEt.png')
c1.Print(printDir+'/'+'sumEt.pdf')
caloMet.Draw('colz')
c1.Print(printDir+'/'+'caloMet.png')
c1.Print(printDir+'/'+'caloMet.pdf')
caloSumEt.Draw('colz')
c1.Print(printDir+'/'+'caloSumEt.png')
c1.Print(printDir+'/'+'caloSumEt.pdf')
for p in sumEts:
  sumEts[p].Draw('COLZ')
  c1.Print(printDir+'/'+p+'_sumEt.png')
  c1.Print(printDir+'/'+p+'_sumEt.pdf')
for p in METs:
  METs[p].Draw('COLZ')
  c1.Print(printDir+'/'+p+'_MET.png')
  c1.Print(printDir+'/'+p+'_MET.pdf')

##
###  if run not in runs:
###    runs.append(run)
###    print "Added run",run
###  if run==208352:
###    nf = fileNames[events.fileIndex()]
###    if nf not in usedFiles:
###      print "Found file",run,nf
###      usedFiles.append(nf)
##
###  print ":".join([str(x) for x in [event, run, lumi]] ),products['pfMet'][0].pt(),  products['pfMet'][0].sumEt()
