import ROOT
from math import sqrt, cos, sin, atan2

###Control Parameters###
Mt = 'sqrt(2*leptonPt*met*(1-cos(metPhi-leptonPhi)))'
Wx = 'met*cos(metPhi)+leptonPt*cos(leptonPhi)'
Wy = 'met*sin(metPhi)+leptonPt*sin(leptonPhi)'
WPhi = 'atan2('+Wy+','+Wx+')'
WPT = 'sqrt(('+Wx+')**2+('+Wy+')**2)'
StLep = 'sqrt(('+WPT+')**2+('+Mt+')**2)'
#deltaPhi = 'abs(leptonPhi-'+WPhi+')'
njets = 'njets'
ht = 'ht'
met = 'met'
muCharge = 'muPdg/abs(muPdg)'

htCut = 500
Stmin = 250
Stmax = 350

presel = 'ht>'+str(htCut)+'&&'+str(StLep)+'>='+str(Stmin)+'&&'+str(StLep)+'<'+str(Stmax)+'&&njets>=6&&singleMuonic==1&&nbtags==0'
#presel = 'ht>'+str(htCut)+'&&'+str(StLep)+'>='+str(Stmax)+'&&njets>=3&&singleMuonic==1&&nbtags==0'
name = presel[0:].replace('&&','_')+'BkgStack_weighted_csvm0.679'

samples = [
{'chain':'WJets','path': '/data/schoef/convertedTuples_v25/copyMET/WJetsHTToLNu/histo_WJetsHTToLNu_from*'},\
{'chain':'ttJets','path': '/data/schoef/convertedTuples_v25/copyMET/ttJetsCSA1450ns/histo_ttJetsCSA1450ns_from*'},\
{'chain':'T51200','path': '/data/schoef/convertedTuples_v25/copyMET/T5Full_1200_1000_800/histo_T5Full_1200_1000_800_from*'},\
{'chain':'T51500','path': '/data/schoef/convertedTuples_v25/copyMET/T5Full_1500_800_100/histo_T5Full_1500_800_100_from*'}, 
]

plots = [ 
  {'varname':'Mt',         'var':Mt,          'lowlimit':0,  'limit':1400},\
  {'varname':'WPT',        'var':WPT,         'lowlimit':0,  'limit':1400},\
  {'varname':'StLep',      'var':StLep,       'lowlimit':0,  'limit':1400},\
  {'varname':'njets',      'var':njets,       'lowlimit':0,  'limit':16},\
  {'varname':'met',        'var':met,         'lowlimit':0,  'limit':1400},\
  {'varname':'ht',         'var':ht,          'lowlimit':0,  'limit':2000},\
  {'varname':'muCharge',   'var':muCharge,    'lowlimit':-2, 'limit':2},\
  ]

for p in plots:
  print p['varname']
  File = ROOT.TFile('/afs/hephy.at/user/e/easilar/CMSSW_7_0_6_patch1/src/Workspace/RA4Analysis/rootfiles/moreTrySignal_Bkg0'+p['varname']+'.root','RECREATE')
  File.cd()
  for s in samples:
    chain = 'c'+s['chain']
    chain = ROOT.TChain('Events')
    chain.Add(s['path'])
    histo = 'h_'+s['chain']
    print histo
    histoname = histo
    histo = ROOT.TH1F(str(histo) ,str(histo),20,p['lowlimit'],p['limit'])
    print histo 
    chain.Draw(p['var']+'>>'+str(histoname),'weight*('+presel+')','goff')
    histo.Write()
  File.Write()
  File.Close()

