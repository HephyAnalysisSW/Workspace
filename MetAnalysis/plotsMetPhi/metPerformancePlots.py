import ROOT
from array import array
from math import *
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getObjDict, getVarValue
ROOT.TH1F.SetDefaultSumw2()
try:
  ROOT.setTDRStyle()
except:
  ROOT.gROOT.ProcessLine(".L ../../HEPHYPythonTools/scripts/root/tdrstyle.C")
  ROOT.gROOT.ProcessLine(".L ../../HEPHYPythonTools/scripts/root/useNiceColorPalette.C")

  ROOT.gStyle.SetOptStat(0)
  ROOT.setTDRStyle()
  ROOT.tdrStyle.SetPadRightMargin(0.18)

ROOT.setTDRStyle()
ROOT.useNiceColorPalette(255)

prefix='highHT_'
cut='(1)'
c = ROOT.TChain("Events")
c.Add('/data/schoef/convertedMetTuples2_v1/looseDoubleMuHTGr200/DYJetsToLL_HT/*.root')
#c.Add('/data/schoef/convertedMetTuples2_v1/looseDoubleMuHTSm200/DYJets/*.root')
#c.Add('/data/schoef/convertedMetTuples2_v1/looseDoubleMu/DYJetsToLL_HT/*.root')

# Simple 1D plots
ngoodVertices  = {'color':ROOT.kBlue, 'var':'ngoodVertices', 'niceName':'', 'histo': ROOT.TH1F('h_ngoodVertices',    'h_ngoodVertices',   50,0,50), 'xTitle':'nvtx'}
ht             = {'color':ROOT.kBlue, 'var':'ht',            'niceName':'', 'histo': ROOT.TH1F('h_ht',               'h_ht',   50,0,1500),'xTitle':'H_{T} (GeV)'}
ptZ            = {'color':ROOT.kBlue, 'var':'ptZ',           'niceName':'', 'histo': ROOT.TH1F('h_ptZ',              'h_ptZ',   50,0,500),'xTitle':'p_{T}(Z) (GeV)'}
mll            = {'color':ROOT.kBlue, 'var':'mll',           'niceName':'', 'histo': ROOT.TH1F('h_mll',              'h_mll',   50,70,120),'xTitle':'m(ll) (GeV)'}
rawMetPt       = {'color':ROOT.kBlue, 'var':'rawMetPt',      'niceName':'raw #slash{E}_{T}', 'histo': ROOT.TH1F('h_rawMetPt',         'h_rawMetPt',   50,0,500),'xTitle':'#slash{E}_{T} (GeV)'}
t1MetPt        = {'color':ROOT.kGreen, 'var':'t1MetPt',      'niceName':'T1 #slash{E}_{T}', 'histo': ROOT.TH1F('h_t1MetPt',          'h_t1MetPt',   50,0,500),'xTitle':'#slash{E}_{T} (GeV)'}
t1TxyMetPt     = {'color':ROOT.kRed, 'var':'t1TxyMetPt',     'niceName':'T1Txy #slash{E}_{T}', 'histo': ROOT.TH1F('h_t1TxyMetPt',       'h_t1TxyMetPt',   50,0,500),'xTitle':'#slash{E}_{T} (GeV)'}
txyMetPt       = {'color':ROOT.kMagenta, 'var':'txyMetPt',   'niceName':'Txy #slash{E}_{T}', 'histo': ROOT.TH1F('h_txyMetPt',         'h_txyMetPt',   50,0,500),'xTitle':'#slash{E}_{T} (GeV)'}
rawMetPhi      = {'color':ROOT.kBlue, 'var':'rawMetPhi',     'niceName':'raw #phi(#slash{E}_{T})', 'histo': ROOT.TH1F('h_rawMetPhi',         'h_rawMetPhi',   50,-pi,pi),'xTitle':'#phi(#slash{E}_{T})'}
t1MetPhi       = {'color':ROOT.kGreen, 'var':'t1MetPhi',     'niceName':'T1 #phi(#slash{E}_{T})', 'histo': ROOT.TH1F('h_t1MetPhi',          'h_t1MetPhi',   50,-pi,pi),'xTitle':'#phi(#slash{E}_{T})'}
t1TxyMetPhi    = {'color':ROOT.kRed, 'var':'t1TxyMetPhi',    'niceName':'T1Txy #phi(#slash{E}_{T})', 'histo': ROOT.TH1F('h_t1TxyMetPhi',       'h_t1TxyMetPhi',   50,-pi,pi),'xTitle':'#phi(#slash{E}_{T})'}
txyMetPhi      = {'color':ROOT.kMagenta, 'var':'txyMetPhi',  'niceName':'Txy #phi(#slash{E}_{T})', 'histo': ROOT.TH1F('h_txyMetPhi',         'h_txyMetPhi',   50,-pi,pi),'xTitle':'#phi(#slash{E}_{T})'}
plots = [\
  ['ngv',[ngoodVertices]], 
  ['ht', [ht]], 
  ['ptZ', [ptZ]], 
  ['mll', [mll]],
  ['met',[rawMetPt, t1MetPt, t1TxyMetPt, txyMetPt]],
  ['metPhi',[rawMetPhi, t1MetPhi, t1TxyMetPhi, txyMetPhi]]
  ]
stuff=[]
for name, pl in plots:
  first=True
  maximum=0
  for p in pl:
    c.Draw(p['var']+'>>'+p['histo'].GetName(),'weight*('+cut+')','goff')
    if maximum<p['histo'].GetMaximum():maximum=p['histo'].GetMaximum()
    p['histo'].SetLineColor(p['color'])
    p['histo'].SetMarkerColor(p['color'])
    p['histo'].SetMarkerStyle(0)
    p['histo'].GetXaxis().SetLabelSize(0.03)
    p['histo'].GetXaxis().SetTitle(p['xTitle'])
    p['histo'].GetYaxis().SetLabelSize(0.03)

  c1 = ROOT.TCanvas()
  for p in pl:
    if first:
      p['histo'].Draw('eh')
      first=False
    else:
      p['histo'].Draw('hsame')
    if 'phi' in name.lower():
      p['histo'].GetYaxis().SetRangeUser(0,1.4*maximum)
    else:
      p['histo'].GetYaxis().SetRangeUser(0.7,2*maximum)
  if 'phi' in name.lower():c1.SetLogy(0)
  else:c1.SetLogy()
  if len(pl)>1: 
    l= ROOT.TLegend(0.55,0.95-0.06*len(pl),.95,.95)
    for p in pl:
      l.AddEntry(p['histo'], p['niceName'])#+etab[0].split('_')[0]+", "+shortName[etab[0].split('_')[1]])
    l.SetFillColor(0)
    l.SetShadowColor(ROOT.kWhite)
    l.SetBorderSize(1)
    l.Draw()
    stuff.append(l)
  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhiValidation/'+prefix+name+'.png')
  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhiValidation/'+prefix+name+'.pdf')
  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhiValidation/'+prefix+name+'.root')
  del c1

# MET phi modulation vs HT
htVals=[150,250,350,450,550,650,750,850]
ht_rawMetPhi      = {'color':ROOT.kBlue, 'var':'rawMetPhi',     'niceName':'raw #phi(#slash{E}_{T})', 'histo': ROOT.TH1F('ht_rawMetPhi',         'ht_rawMetPhi',  len(htVals)-1, array('d',htVals) ), 'xTitle':'H_{T} (GeV)'}
ht_t1MetPhi       = {'color':ROOT.kGreen, 'var':'t1MetPhi',     'niceName':'T1 #phi(#slash{E}_{T})', 'histo': ROOT.TH1F('ht_t1MetPhi',          'ht_t1MetPhi', len(htVals)-1, array('d',htVals)   ),'xTitle':'H_{T} (GeV)'}
ht_t1TxyMetPhi    = {'color':ROOT.kRed, 'var':'t1TxyMetPhi',    'niceName':'T1Txy #phi(#slash{E}_{T})', 'histo': ROOT.TH1F('ht_t1TxyMetPhi',       'ht_t1TxyMetPhi',len(htVals)-1, array('d',htVals)  ),'xTitle':'H_{T} (GeV)'}
ht_txyMetPhi      = {'color':ROOT.kMagenta, 'var':'txyMetPhi',  'niceName':'Txy #phi(#slash{E}_{T})', 'histo': ROOT.TH1F('ht_txyMetPhi',         'ht_txyMetPhi', len(htVals)-1, array('d',htVals)  ),'xTitle':'H_{T} (GeV)'}
phis = [\
  ht_rawMetPhi, ht_t1MetPhi, ht_t1TxyMetPhi, ht_txyMetPhi
  ]
stuff=[]
first=True

for p in phis:
  for i_htv in range(len(htVals)-1):
    htb = htVals[i_htv:i_htv+2]
#    print htb,p['var']+'>>'+p['histo'].GetName(), 'weight*(ht>'+str(htb[0])+'&&ht<'+str(htb[1])+')'
    c.Draw(p['var']+'>>phitmp(50,-pi,pi)','weight*(ht>'+str(htb[0])+'&&ht<'+str(htb[1])+')','goff')
    phitmp = ROOT.gDirectory.Get('phitmp')
    cs=0
    cc=0
    c0=phitmp.Integral()/(2.*pi)
    for i in range(1, phitmp.GetNbinsX()+1):
      cs+=phitmp.GetBinContent(i)*sin(phitmp.GetBinCenter(i))
      cc+=phitmp.GetBinContent(i)*cos(phitmp.GetBinCenter(i))
    cs=cs/pi
    cc=cc/pi
#    print p['var'],c0,cs,cc,sqrt(cs**2+cc**2)/c0
    p['histo'].Fill(0.5*sum(htb), sqrt(cs**2+cc**2)/c0)
    del phitmp

for p in phis:
  p['histo'].SetLineColor(p['color'])
  p['histo'].SetMarkerColor(p['color'])
  p['histo'].SetMarkerStyle(0)
  p['histo'].GetXaxis().SetLabelSize(0.03)
  p['histo'].GetXaxis().SetTitle(p['xTitle'])
  p['histo'].GetYaxis().SetTitle("#sqrt{a_{1}^{2}+b_{1}^{2}}/c_{0}")
  p['histo'].GetYaxis().SetRangeUser(0,0.4)
  p['histo'].GetYaxis().SetLabelSize(0.03)
  for i in range(1, p['histo'].GetNbinsX()+1):
    p['histo'].SetBinError(i,0)

c1 = ROOT.TCanvas()
first=True
for p in phis:
  if first:
    p['histo'].Draw('h')
    first=False
  else:
    p['histo'].Draw('hsame')

l= ROOT.TLegend(0.55,0.95-0.06*len(phis),.95,.95)
for p in phis:
  l.AddEntry(p['histo'], p['niceName'])#+etab[0].split('_')[0]+", "+shortName[etab[0].split('_')[1]])

l.SetFillColor(0)
l.SetShadowColor(ROOT.kWhite)
l.SetBorderSize(1)
l.Draw()
c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhiValidation/'+prefix+'fc_ht.png')
c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhiValidation/'+prefix+'fc_ht.pdf')
c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhiValidation/'+prefix+'fc_ht.root')
del c1

#met scale
#zPt+ETmiss+u=0
qtVals=range(150,1000,25)
scale_rawMet      = {'color':ROOT.kBlue, 'var':'rawMet',     'niceName':'raw #slash{E}_{T}', 'histo': ROOT.TProfile('qt_rawMet',         'qt_rawMet',  len(qtVals)-1, array('d',qtVals), 0,2), 'xTitle':'Z q_{T} (GeV)'}
scale_t1Met       = {'color':ROOT.kGreen, 'var':'t1Met',     'niceName':'T1 #slash{E}_{T}', 'histo': ROOT.TProfile('qt_t1Met',          'qt_t1Met', len(qtVals)-1, array('d',qtVals)   ,0,2),'xTitle':'Z q_{T} (GeV)'}
scale_t1TxyMet    = {'color':ROOT.kRed, 'var':'t1TxyMet',    'niceName':'T1Txy #slash{E}_{T}', 'histo': ROOT.TProfile('qt_t1TxyMet',       'qt_t1TxyMet',len(qtVals)-1, array('d',qtVals) ,0,2  ),'xTitle':'Z q_{T} (GeV)'}
scale_txyMet      = {'color':ROOT.kMagenta, 'var':'txyMet',  'niceName':'Txy #slash{E}_{T}', 'histo': ROOT.TProfile('qt_txyMet',         'qt_txyMet', len(qtVals)-1, array('d',qtVals) ,0,2 ),'xTitle':'Z q_{T} (GeV)'}
mets = [\
  scale_rawMet, scale_t1Met, scale_t1TxyMet, scale_txyMet
  ]
stuff=[]
first=True

def getUparaStr(m):
  return '(-cos('+m+'Phi-phiZ)*'+m+'Pt-ptZ)'

def getScaleStr(m):
  return '(-'+getUparaStr(m)+')/ptZ'

for p in mets:
#  for i_qtv in range(len(qtVals)-1):
#    qtb = qtVals[i_qtv:i_qtv+2]
  print getScaleStr(p['var'])+':ptZ>>'+p['histo'].GetName(),'weight','goff'
  c.Draw(getScaleStr(p['var'])+':ptZ>>'+p['histo'].GetName(),'weight','goff')

for p in mets:
  p['histo'].SetLineColor(p['color'])
  p['histo'].SetMarkerColor(p['color'])
  p['histo'].SetMarkerStyle(0)
  p['histo'].GetXaxis().SetLabelSize(0.03)
  p['histo'].GetXaxis().SetTitle(p['xTitle'])
  p['histo'].GetYaxis().SetTitle("-<u_{||}/q_{T}>")
  p['histo'].GetYaxis().SetRangeUser(0.4,1.6)
  p['histo'].GetYaxis().SetLabelSize(0.03)

c1 = ROOT.TCanvas()
first=True
for p in mets:
  if first:
    p['histo'].Draw('h')
    first=False
  else:
    p['histo'].Draw('hsame')

l= ROOT.TLegend(0.55,0.95-0.06*len(mets),.95,.95)
for p in mets:
  l.AddEntry(p['histo'], p['niceName'])#+etab[0].split('_')[0]+", "+shortName[etab[0].split('_')[1]])

l.SetFillColor(0)
l.SetShadowColor(ROOT.kWhite)
l.SetBorderSize(1)
l.Draw()
c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhiValidation/'+prefix+'scale_qt.png')
c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhiValidation/'+prefix+'scale_qt.pdf')
c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhiValidation/'+prefix+'scale_qt.root')
del c1


#met resolution
rmsUPara_rawMet      = {'scale':scale_rawMet,'color':ROOT.kBlue, 'var':'rawMet',     'niceName':'raw #slash{E}_{T}', 'histo': ROOT.TH1F('qt_upara_rawMet',         'qt_upara_rawMet',  len(qtVals)-1, array('d',qtVals)), 'xTitle':'Z q_{T} (GeV)'}
rmsUPara_t1Met       = {'scale':scale_t1Met,'color':ROOT.kGreen, 'var':'t1Met',     'niceName':'T1 #slash{E}_{T}', 'histo': ROOT.TH1F('qt_upara_t1Met',          'qt_upara_t1Met', len(qtVals)-1, array('d',qtVals)),'xTitle':'Z q_{T} (GeV)'}
rmsUPara_t1TxyMet    = {'scale':scale_t1TxyMet,'color':ROOT.kRed, 'var':'t1TxyMet',    'niceName':'T1Txy #slash{E}_{T}', 'histo': ROOT.TH1F('qt_upara_t1TxyMet',       'qt_upara_t1TxyMet',len(qtVals)-1, array('d',qtVals)),'xTitle':'Z q_{T} (GeV)'}
rmsUPara_txyMet      = {'scale':scale_txyMet,'color':ROOT.kMagenta, 'var':'txyMet',  'niceName':'Txy #slash{E}_{T}', 'histo': ROOT.TH1F('qt_upara_txyMet',         'qt_upara_txyMet', len(qtVals)-1, array('d',qtVals)),'xTitle':'Z q_{T} (GeV)'}
rmsUPerp_rawMet      = {'color':ROOT.kBlue, 'var':'rawMet',     'niceName':'raw #slash{E}_{T}', 'histo': ROOT.TH1F('qt_upara_rawMet',         'qt_upara_rawMet',  len(qtVals)-1, array('d',qtVals)), 'xTitle':'Z q_{T} (GeV)'}
rmsUPerp_t1Met       = {'color':ROOT.kGreen, 'var':'t1Met',     'niceName':'T1 #slash{E}_{T}', 'histo': ROOT.TH1F('qt_upara_t1Met',          'qt_upara_t1Met', len(qtVals)-1, array('d',qtVals)),'xTitle':'Z q_{T} (GeV)'}
rmsUPerp_t1TxyMet    = {'color':ROOT.kRed, 'var':'t1TxyMet',    'niceName':'T1Txy #slash{E}_{T}', 'histo': ROOT.TH1F('qt_upara_t1TxyMet',       'qt_upara_t1TxyMet',len(qtVals)-1, array('d',qtVals)),'xTitle':'Z q_{T} (GeV)'}
rmsUPerp_txyMet      = {'color':ROOT.kMagenta, 'var':'txyMet',  'niceName':'Txy #slash{E}_{T}', 'histo': ROOT.TH1F('qt_upara_txyMet',         'qt_upara_txyMet', len(qtVals)-1, array('d',qtVals)),'xTitle':'Z q_{T} (GeV)'}
rmsUPara = [\
  rmsUPara_rawMet, rmsUPara_t1Met, rmsUPara_t1TxyMet, rmsUPara_txyMet,
  ]
rmsUPerp = [\
  rmsUPerp_rawMet, rmsUPerp_t1Met, rmsUPerp_t1TxyMet, rmsUPerp_txyMet
]
stuff=[]
first=True

def getUParaStr(m):
  return '(-cos('+m+'Phi-phiZ)*'+m+'Pt)'
def getUPerpStr(m):
  return '(-cos('+m+'Phi-phiZ+pi/2.)*'+m+'Pt)'

def getScaleStr(m):
  return '(-'+getUparaStr(m)+')/ptZ'

for p in rmsUPara:
  for i_qtv in range(len(qtVals)-1):
#    htmp = ROOT.TH1F('htmp','htmp',30,-pi,pi)
    qtb = qtVals[i_qtv:i_qtv+2]

#    print getUParaStr(p['var'])+'>>htmp2','weight*(ptZ>'+str(qtb[0])+'&&ptZ<'+str(qtb[1])+')','goff'
    c.Draw(getUParaStr(p['var'])+'>>htmp2', 'weight*(ptZ>'+str(qtb[0])+'&&ptZ<'+str(qtb[1])+')','goff')
    htmp = ROOT.gDirectory.Get('htmp2')
#    print 'bin',0.5*sum(qtb), 'rms',htmp.GetRMS(), 'scale', p['scale']['histo'].GetBinContent(p['scale']['histo'].FindBin(0.5*sum(qtb)))
    rmsOverScale=htmp.GetRMS()/p['scale']['histo'].GetBinContent(p['scale']['histo'].FindBin(0.5*sum(qtb)))
    rmsEOverScale=htmp.GetRMSError()/p['scale']['histo'].GetBinContent(p['scale']['histo'].FindBin(0.5*sum(qtb)))
    ib = p['histo'].FindBin(0.5*sum(qtb))
    p['histo'].SetBinContent(ib, rmsOverScale)
    p['histo'].SetBinError(ib, rmsEOverScale)
for p in rmsUPerp:
  for i_qtv in range(len(qtVals)-1):
#    htmp = ROOT.TH1F('htmp','htmp',30,-pi,pi)
    qtb = qtVals[i_qtv:i_qtv+2]
    print getUPerpStr(p['var'])+'>>htmp2','weight*(ptZ>'+str(qtb[0])+'&&ptZ<'+str(qtb[1])+')','goff'
    c.Draw(getUPerpStr(p['var'])+'>>htmp2', 'weight*(ptZ>'+str(qtb[0])+'&&ptZ<'+str(qtb[1])+')','goff')
    htmp = ROOT.gDirectory.Get('htmp2')
    print 'bin',0.5*sum(qtb), 'rms',htmp.GetRMS()
    rms=htmp.GetRMS()
    rmsE=htmp.GetRMSError()
    ib = p['histo'].FindBin(0.5*sum(qtb))
    p['histo'].SetBinContent(ib, rms)
    p['histo'].SetBinError(ib, rmsE)

for p in rmsUPara+rmsUPerp:
  p['histo'].SetLineColor(p['color'])
  p['histo'].SetMarkerColor(p['color'])
  p['histo'].SetMarkerStyle(0)
  p['histo'].GetXaxis().SetLabelSize(0.03)
  p['histo'].GetXaxis().SetTitle(p['xTitle'])
  p['histo'].GetYaxis().SetLabelSize(0.03)

for p in rmsUPara:
  p['histo'].GetYaxis().SetTitle("#sigma(u_{||}+q_{T})/scale")
  p['histo'].GetYaxis().SetRangeUser(20,100)

for p in rmsUPerp:
  p['histo'].GetYaxis().SetTitle("#sigma(u_{#perp} )")
  p['histo'].GetYaxis().SetRangeUser(10, 40)

c1 = ROOT.TCanvas()
first=True
for p in rmsUPara:
  if first:
    p['histo'].Draw('h')
    first=False
  else:
    p['histo'].Draw('hsame')

l= ROOT.TLegend(0.55,0.95-0.06*len(rmsUPara),.95,.95)
for p in rmsUPara:
  l.AddEntry(p['histo'], p['niceName'])#+etab[0].split('_')[0]+", "+shortName[etab[0].split('_')[1]])

l.SetFillColor(0)
l.SetShadowColor(ROOT.kWhite)
l.SetBorderSize(1)
l.Draw()
c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhiValidation/'+prefix+'rmsOverScale_UPara_qt.png')
c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhiValidation/'+prefix+'rmsOverScale_UPara_qt.pdf')
c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhiValidation/'+prefix+'rmsOverScale_UPara_qt.root')
first=True
for p in rmsUPerp:
  if first:
    p['histo'].Draw('h')
    first=False
  else:
    p['histo'].Draw('hsame')

l= ROOT.TLegend(0.55,0.95-0.06*len(rmsUPerp),.95,.95)
for p in rmsUPerp:
  l.AddEntry(p['histo'], p['niceName'])#+etab[0].split('_')[0]+", "+shortName[etab[0].split('_')[1]])

l.SetFillColor(0)
l.SetShadowColor(ROOT.kWhite)
l.SetBorderSize(1)
l.Draw()
c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhiValidation/'+prefix+'rmsOverScale_UPerp_qt.png')
c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhiValidation/'+prefix+'rmsOverScale_UPerp_qt.pdf')
c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhiValidation/'+prefix+'rmsOverScale_UPerp_qt.root')
del c1


##met phi resolution
#qtVals=range(150,550,50)
#metPhiRes_rawMet      = {'color':ROOT.kBlue, 'var':'rawMet',     'niceName':'raw #slash{E}_{T}', 'histo': ROOT.TProfile('qt_rawMet',         'qt_rawMet',  len(qtVals)-1, array('d',qtVals), 0,2), 'xTitle':'Z q_{T} (GeV)'}
#metPhiRes_t1Met       = {'color':ROOT.kGreen, 'var':'t1Met',     'niceName':'T1 #slash{E}_{T}', 'histo': ROOT.TProfile('qt_t1Met',          'qt_t1Met', len(qtVals)-1, array('d',qtVals)   ,0,2),'xTitle':'Z q_{T} (GeV)'}
#metPhiRes_t1TxyMet    = {'color':ROOT.kRed, 'var':'t1TxyMet',    'niceName':'T1Txy #slash{E}_{T}', 'histo': ROOT.TProfile('qt_t1TxyMet',       'qt_t1TxyMet',len(qtVals)-1, array('d',qtVals) ,0,2  ),'xTitle':'Z q_{T} (GeV)'}
#metPhiRes_txyMet      = {'color':ROOT.kMagenta, 'var':'txyMet',  'niceName':'Txy #slash{E}_{T}', 'histo': ROOT.TProfile('qt_txyMet',         'qt_txyMet', len(qtVals)-1, array('d',qtVals) ,0,2 ),'xTitle':'Z q_{T} (GeV)'}
#mets = [\
#  metPhiRes_rawMet, metPhiRes_t1Met, metPhiRes_t1TxyMet, metPhiRes_txyMet
#  ]
#stuff=[]
#first=True
#
###zPt+ETmiss+u=0
##-etmiss-zpt 
##'atan2(-'+m+'Pt*cos('+m+'Phi)-ptZ*cos(phiZ), -'+m+'Pt*sin('+m+'Phi)-ptZ*sin(phiZ))'
##def getUparaStr(m):
##  return '(-cos('+m+'Phi-phiZ)*'+m+'Pt-ptZ)'
#def getDPhiStr(m):
##  return 'acos(cos('+m+'Phi-phiZ))'
#  return 'acos(cos(pi+atan2(-'+m+'Pt*cos('+m+'Phi)-ptZ*cos(phiZ), -'+m+'Pt*sin('+m+'Phi)-ptZ*sin(phiZ))-phiZ))'
#
#for p in mets:
#  for i_qtv in range(len(qtVals)-1):
#    htmp = ROOT.TH1F('htmp','htmp',30,-pi,pi)
#    qtb = qtVals[i_qtv:i_qtv+2]
#    print getDPhiStr(p['var'])+'>>htmp','weight*(ptZ>'+str(qtb[0])+'&&ptZ<'+str(qtb[1])+')','goff'
#    c.Draw(getDPhiStr(p['var'])+'>>htmp', 'weight*(ptZ>'+str(qtb[0])+'&&ptZ<'+str(qtb[1])+')','goff')
#    rms= htmp.GetRMS()
#    print rms
#    p['histo'].Fill(0.5*sum(qtb),rms)
#    c1=ROOT.TCanvas()
#    htmp.Draw()
#    c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhiValidation/mphi.png') 
#    del c1
#    del htmp
#
#for p in mets:
#  p['histo'].SetLineColor(p['color'])
#  p['histo'].SetMarkerColor(p['color'])
#  p['histo'].SetMarkerStyle(0)
#  p['histo'].GetXaxis().SetLabelSize(0.03)
#  p['histo'].GetXaxis().SetTitle(p['xTitle'])
#  p['histo'].GetYaxis().SetTitle("rms(#Delta#Phi(q_{T},u))")
#  p['histo'].GetYaxis().SetRangeUser(0.4,1.6)
#  p['histo'].GetYaxis().SetLabelSize(0.03)
#
#c1 = ROOT.TCanvas()
#first=True
#for p in mets:
#  if first:
#    p['histo'].Draw('h')
#    first=False
#  else:
#    p['histo'].Draw('hsame')
#
#l= ROOT.TLegend(0.55,0.95-0.06*len(mets),.95,.95)
#for p in mets:
#  l.AddEntry(p['histo'], p['niceName'])#+etab[0].split('_')[0]+", "+shortName[etab[0].split('_')[1]])
#
#l.SetFillColor(0)
#l.SetShadowColor(ROOT.kWhite)
#l.SetBorderSize(1)
#l.Draw()
#c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhiValidation/rmsPhi_qt.png')
#c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhiValidation/rmsPhi_qt.pdf')
#c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhiValidation/rmsPhi_qt.root')
#del c1

