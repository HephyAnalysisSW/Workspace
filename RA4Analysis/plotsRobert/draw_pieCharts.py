import ROOT
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain
from Workspace.RA4Analysis.cmgTuplesPostProcessed_v5_Phys14V2 import * 
small = False
maxN = -1 if not small else 1 
from array import array

ROOT.gROOT.LoadMacro("../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()

from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName,nBTagBinName,varBinName, color, getBinBorders
from math import pi, sqrt
from localInfo import afsuser as username
uDir = username[0]+'/'+username
subDir = 'pngPie'

prefix=None
leptonMinPt=25

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--stb", dest="stb", default="250,-1", type="string", action="store", help="Which ST region")
parser.add_option("--btb", dest="btb", default="", type="string", action="store", help="Which ST region")
parser.add_option("--htb", dest="htb", default="", type="string", action="store", help="Which HT region")
parser.add_option("--lepton", dest="lepton", default="muon", type="string", action="store", help="muon/electron")

(options, args) = parser.parse_args()
stb = eval("("+options.stb+")")
btb = eval("("+options.btb+")") if options.btb!="" else None
htb = eval("("+options.htb+")") if options.htb!="" else None

from draw_helpers import *

from Workspace.RA4Analysis.cmgTuples_v5_Phys14 import *
samples=[WJetsHTToLNu['hard'], ttJets['hard'], QCD['hard'], singleTop['hard'], DY['hard'],  TTVH['hard']]
for s in samples:
  s['chain']=getChain(s,maxN=maxN,histname="")

lepton = options.lepton
print "lepton", lepton, "ST:",stb, 'htb',htb, "btb", btb

htreg = [(400,500),(500,750),(750, 1000),(1000,-1)]
njreg = [(2,2),(3,3),(4,4),(5,5),(6,-1)]
nbtreg = [(0,0),(1,1),(2,2),(3,-1)]

plots={}
stuff=[]
c1=ROOT.TCanvas('c1','c1',700,572)
c1.SetLeftMargin(0.2)
ROOT.gStyle.SetPadLeftMargin(0.2)

if lepton=="muon":
   minID=1; minRelIso=0.12
if lepton=="electron":
   minID=3; minRelIso=0.14

if btb and stb:
  name = nameAndCut(stb, htb=None, njetb=None, btb=btb)[0]
  cut= "&&".join([
      exactlyOneTightLepton(lepton=lepton, minPt=leptonMinPt, maxEta=2.4, minID=minID, minRelIso=minRelIso),\
      looseLeptonVeto(lepton=lepton, minPt=10), \
  #            nJetCut(njb=njb, minPt=30, maxEta=2.4), \
  #            htCut  (htb=htb, minPt=30, maxEta=2.4), \
      nBTagCut(btb, minPt=30, maxEta=2.4, minCMVATag=0.732),
      stCut(lepton=lepton, stb=stb, minPt=leptonMinPt, maxEta=2.4, minID=minID, minRelIso=minRelIso), \
      ])
  for s in samples:
    hName="yield_"+s['name']+'_'+name
    h =  ROOT.TH2F(hName, "",len(njreg),array('d',getBinBorders(njreg)), len(htreg),array('d', getBinBorders(htreg)) )
    stuff.append(h)
    h.Reset()
    for  i_njb, njb in enumerate(njreg):
      h.GetXaxis().SetBinLabel(i_njb+1, nJetBinName(njb))
    for i_htb, htb in enumerate(htreg):
      h.GetYaxis().SetBinLabel(i_htb+1, varBinName(htb,"H_{T}"))
    print "At",hName,'cut',cut
    s['chain'].Draw(htStr(minPt=30, maxEta=2.4)+":"+nJetStr(minPt=30, maxEta=2.4)+">>"+hName,"weight*("+cut+")",'goff')
    plots[hName]=h.Clone()
  #  print h.Integral()
    del h
  fname="_".join(([prefix] if prefix else [])+[lepton,name])
  hPie = ROOT.TH2F(hName.replace('yield','pie'), "",len(njreg),0,len(njreg), len(htreg),0,len(htreg)) 
  stuff.append(hPie)
  hPie.Reset()
  for  i_njb, njb in enumerate(njreg):
    hPie.GetXaxis().SetBinLabel(i_njb+1, nJetBinName(njb))
  for i_htb, htb in enumerate(htreg):
    hPie.GetYaxis().SetBinLabel(i_htb+1, varBinName(htb,"H_{T}"))
  hPie.Reset()
  hPie.Draw()
  for  i_njb, njb in enumerate(njreg):
    for i_htb, htb in enumerate(htreg):
      vals=[ plots["yield_"+s['name']+'_'+name].GetBinContent(i_njb+1, i_htb+1) for s in samples]
      if sum(vals)==0.: continue
      vals=array('f', vals)
      cols=array('i', [color(s['name']) for s in samples])
  #    print "Vals",vals,"cols",cols
      height=1-ROOT.gStyle.GetPadBottomMargin()-ROOT.gStyle.GetPadTopMargin()
      width =1-ROOT.gStyle.GetPadLeftMargin()-ROOT.gStyle.GetPadRightMargin()
      x0 = ROOT.gStyle.GetPadLeftMargin() + (0.01+i_njb)*width/float(len(njreg))
      x1 = ROOT.gStyle.GetPadLeftMargin() + (0.99+i_njb)*width/float(len(njreg))
      y0 = ROOT.gStyle.GetPadBottomMargin() + (0.01+i_htb)*height/float(len(htreg))
      y1 = ROOT.gStyle.GetPadBottomMargin() + (0.99+i_htb)*height/float(len(htreg))
  #          print x0,x1,y0,y1, vals
      pad=ROOT.TPad('pad_'+s['name']+'_'+name+'_'+str(i_htb)+"_"+str( i_njb),'pad', x0,y0, x1,y1 )
      stuff.append(pad)
      pad.Draw()
      pad.cd()
      pie = ROOT.TPie('p_'+s['name']+'_'+name+'_'+str(i_htb)+"_"+str( i_njb),'', len(vals), vals, cols)
      pie.SetLabelFormat("")
      stuff.append(pie)
      pie.Draw('nol ')
  #          pad.Update()
      stuff.append(pad)
      c1.cd()
  c1.RedrawAxis()
  #      l.Draw()
  #      c1.Update()
  c1.Print('/afs/hephy.at/user/'+uDir+'/www/'+subDir+'/pieChart_njet_vs_ht_'+fname+".png")
  c1.Print('/afs/hephy.at/user/'+uDir+'/www/'+subDir+'/pieChart_njet_vs_ht_'+fname+".pdf")
  c1.Print('/afs/hephy.at/user/'+uDir+'/www/'+subDir+'/pieChart_njet_vs_ht_'+fname+".root")
if htb and stb:
  name = nameAndCut(stb, htb=htb, njetb=None, btb=None)[0]
  cut= "&&".join([
      exactlyOneTightLepton(lepton=lepton, minPt=leptonMinPt, maxEta=2.4, minID=minID, minRelIso=minRelIso),\
      looseLeptonVeto(lepton=lepton, minPt=10), \
  #            nJetCut(njb=njb, minPt=30, maxEta=2.4), \
      htCut  (htb=htb, minPt=30, maxEta=2.4), \
  #    nBTagCut(btb, minPt=30, maxEta=2.4, minCMVATag=0.732),
      stCut(lepton=lepton, stb=stb, minPt=leptonMinPt, maxEta=2.4, minID=minID, minRelIso=minRelIso), \
      ])
  for s in samples:
    hName="yield_"+s['name']+'_'+name
    h =  ROOT.TH2F(hName, "",len(njreg),array('d',getBinBorders(njreg)), len(nbtreg),array('d', getBinBorders(nbtreg)) )
    stuff.append(h)
    h.Reset()
    for  i_njb, njb in enumerate(njreg):
      h.GetXaxis().SetBinLabel(i_njb+1, nJetBinName(njb))
    for i_btb, btb in enumerate(nbtreg):
      h.GetYaxis().SetBinLabel(i_btb+1, nBTagBinName(btb))
    print "At",hName,'cut',cut
    s['chain'].Draw(nBTagStr(minPt=30, maxEta=2.4, minCMVATag=0.732)+":"+nJetStr(minPt=30, maxEta=2.4)+">>"+hName,"weight*("+cut+")",'goff')
    plots[hName]=h.Clone()
  #  print h.Integral()
    del h
  fname="_".join(([prefix] if prefix else [])+[lepton,name])
  hPie = ROOT.TH2F(hName.replace('yield','pie'), "",len(njreg),0,len(njreg), len(nbtreg),0,len(nbtreg)) 
  stuff.append(hPie)
  hPie.Reset()
  for  i_njb, njb in enumerate(njreg):
    hPie.GetXaxis().SetBinLabel(i_njb+1, nJetBinName(njb))
  for i_btb, btb in enumerate(nbtreg):
    hPie.GetYaxis().SetBinLabel(i_btb+1, nBTagBinName(btb))
  hPie.Reset()
  hPie.Draw()
  for  i_njb, njb in enumerate(njreg):
    for i_btb, btb in enumerate(nbtreg):
      vals=[ plots["yield_"+s['name']+'_'+name].GetBinContent(i_njb+1, i_btb+1) for s in samples]
      if sum(vals)==0.: continue
      vals=array('f', vals)
      cols=array('i', [color(s['name']) for s in samples])
  #    print "Vals",vals,"cols",cols
      height=1-ROOT.gStyle.GetPadBottomMargin()-ROOT.gStyle.GetPadTopMargin()
      width =1-ROOT.gStyle.GetPadLeftMargin()-ROOT.gStyle.GetPadRightMargin()
      x0 = ROOT.gStyle.GetPadLeftMargin() + (0.01+i_njb)*width/float(len(njreg))
      x1 = ROOT.gStyle.GetPadLeftMargin() + (0.99+i_njb)*width/float(len(njreg))
      y0 = ROOT.gStyle.GetPadBottomMargin() + (0.01+i_btb)*height/float(len(nbtreg))
      y1 = ROOT.gStyle.GetPadBottomMargin() + (0.99+i_btb)*height/float(len(nbtreg))
  #          print x0,x1,y0,y1, vals
      pad=ROOT.TPad('pad_'+s['name']+'_'+name+'_'+str(i_btb)+"_"+str( i_njb),'pad', x0, y0, x1, y1 )
      stuff.append(pad)
      pad.Draw()
      pad.cd()
      pie = ROOT.TPie('p_'+s['name']+'_'+name+'_'+str(i_btb)+"_"+str( i_njb),'', len(vals), vals, cols)
      pie.SetLabelFormat("")
      stuff.append(pie)
      pie.Draw('nol ')
  #          pad.Update()
      stuff.append(pad)
      c1.cd()
  c1.RedrawAxis()
  c1.Print('/afs/hephy.at/user/'+uDir+'/www/'+subDir+'/pieChart_njet_vs_nbjet_'+fname+".png")
  c1.Print('/afs/hephy.at/user/'+uDir+'/www/'+subDir+'/pieChart_njet_vs_nbjet_'+fname+".pdf")
  c1.Print('/afs/hephy.at/user/'+uDir+'/www/'+subDir+'/pieChart_njet_vs_nbjet_'+fname+".root")
#      del hPie
