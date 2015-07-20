import ROOT
import pickle, os
from Workspace.HEPHYPythonTools.helpers import getChain, getObjFromFile

from math import pi, cos, sin, sqrt, atan2
ROOT.gROOT.ProcessLine(".L ../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()
from commons import *

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--prefix", dest="prefix", default="WJets_100-600", type="string", action="store", help="prefix:Which prefix.")
parser.add_option("--maps", dest="maps", default='all', type="string", action="store", help="Which maps.")
parser.add_option("--mode", dest="mode", default='all', type="string", action="store", help="Which mode [ngoodVertices/sumPt/multiplicity]")
parser.add_option("--small", dest="small", action="store_true", help="Just do a small subset.")
parser.add_option("--input", dest="input", default='/data/schoef/mult_191214/WJets_100-600.root', type="string", action="store", help="Which input.")
parser.add_option("--plotDir", dest="plotDir", default='/afs/hephy.at/user/s/schoefbeck/www/pngPF/', type="string", action="store", help="Which plotDir.")

(options, args) = parser.parse_args()
prefixes=[]
if options.prefix!='':
  prefixes.append(options.prefix)
if options.small:
  prefixes.append('small')
prefix = '_'.join(prefixes)
if prefix!='':
  prefix+='_'
print 'maps', options.maps,'prefix',options.prefix, 'input', options.input, 'mode', options.mode
if options.maps=='all':
  maps = allMaps
else:
  exec("maps = [" +options.maps+ "]")
if options.mode=='all':
  modes=["ngoodVertices", "sumPt", "multiplicity"]
else:
  modes=[options.mode ]
if os.path.isdir(options.input):
  c = getChain(options.input, maxN=1) if options.small else getChain(options.input)
else:
  c=None
def getLinSquStr(f):
  return  "10^{-6}#upoint ("+str(round(10**6*f.GetParameter(0),1))+'#pm '+str(round(10**6*abs(f.GetParError(0)),1))+") #upoint n^{2}+10^{-3}#upoint("+str(round(10**3*f.GetParameter(1),1))+'#pm '+str(round(10**3*abs(f.GetParError(1)),1))+") #upoint n"
def getLinSquStrNoFac(f):
  return  "("+str(round(f.GetParameter(0),1))+'#pm '+str(round(abs(f.GetParError(0)),1))+") #upoint n^{2}+("+str(round(f.GetParameter(1),1))+'#pm '+str(round(abs(f.GetParError(1)),1))+") #upoint n"
def getSquStr(f):
  return  "10^{-6}#upoint ("+str(round(10**6*f.GetParameter(0),1))+'#pm '+str(round(10**6*abs(f.GetParError(0)),1))+") #upoint n^{2}"
def getPropStr(f):
  return "10^{-3} #upoint ("+str(round(10**3*f.GetParameter(0),1))+'#pm '+str(round(10**3*abs(f.GetParError(0)),1))+") #upoint n"
def getLinStr(f):
  return '10^{-2} #upoint ('+str(round(10**2*f.GetParameter(0),1))+'#pm '+str(round(10**2*abs(f.GetParError(0)),1))+") + 10^{-3}#upoint("+str(round(10**3*f.GetParameter(1),1))+'#pm '+str(round(10**3*abs(f.GetParError(1)),1))+") #upoint n"

for mode in modes:
  if mode=="ngoodVertices":
    h['fitRange'] = [0,50]
    h0Barrel['fitRange'] = [0,50]
    h0EndcapPlus['fitRange'] = [0,50]
    h0EndcapMinus['fitRange'] = [0,50]
    gammaBarrel['fitRange'] = [0,300]
    gammaEndcapPlus['fitRange']   = [0,50]
    gammaEndcapMinus['fitRange']  = [0,50]
    gammaForwardPlus['fitRange'] = [0,50]
    gammaForwardMinus['fitRange'] = [0,50]
    e['fitRange'] = [0,50]
    mu['fitRange'] = [0,50]
    h_HF_Minus['fitRange'] = [0,50]
    h_HF_Plus['fitRange'] = [0,50]
    egamma_HF_Minus['fitRange'] = [0,50]
    egamma_HF_Plus['fitRange'] = [0,50]
  ##pt
  if mode=="sumPt":
    h['fitRange'] = [0,2000]
    h0Barrel['fitRange'] = [0,150]
    h0EndcapPlus['fitRange'] = [0,250]
    h0EndcapMinus['fitRange'] = [0,250]
    gammaBarrel['fitRange'] = [0,500]
    gammaEndcapPlus['fitRange']   = [0,250]
    gammaEndcapMinus['fitRange']  = [0,250]
    gammaForwardPlus['fitRange'] = [0,20]
    gammaForwardMinus['fitRange'] = [0,20]
    e['fitRange'] = [0,150]
    mu['fitRange'] = [0,150]
    h_HF_Minus['fitRange'] = [0,300]
    h_HF_Plus['fitRange'] = [0,300]
    egamma_HF_Minus['fitRange'] = [0,100]
    egamma_HF_Plus['fitRange'] = [0,100]

  #multiplicity
  if mode=="multiplicity":
    h['fitRange'] = [0,2000]
    h0Barrel['fitRange'] = [0,120]
    h0EndcapPlus['fitRange'] = [0,80]
    h0EndcapMinus['fitRange'] = [0,80]
    gammaBarrel['fitRange'] = [0,500]
    gammaEndcapPlus['fitRange']   = [0,250]
    gammaEndcapMinus['fitRange']  = [0,250]
    gammaForwardPlus['fitRange'] = [0,10]
    gammaForwardMinus['fitRange'] = [0,10]
    e['fitRange'] = [0,10]
    mu['fitRange'] = [0,10]
    h_HF_Minus['fitRange'] = [0,300]
    h_HF_Plus['fitRange'] = [0,300]
    egamma_HF_Minus['fitRange'] = [0,300]
    egamma_HF_Plus['fitRange'] = [0,300]

  h['zoomRange'] = [-40,40]
  h0Barrel['zoomRange'] = [-2,2]
  h0EndcapPlus['zoomRange'] = [-5,5]
  h0EndcapMinus['zoomRange'] = [-5,5]
  gammaBarrel['zoomRange'] = [-2,2]
  gammaEndcapPlus['zoomRange'] = [-20,20]
  gammaEndcapMinus['zoomRange'] = [-20,20]
  gammaForwardPlus['zoomRange'] = [-2,2]
  gammaForwardMinus['zoomRange'] = [-2,2]
  e['zoomRange'] = [-20,20]
  mu['zoomRange'] = [-20,20]
  h_HF_Minus['zoomRange'] = [-5,5]
  h_HF_Plus['zoomRange'] = [-5,5]
  egamma_HF_Minus['zoomRange'] = [-5,5]
  egamma_HF_Plus['zoomRange'] = [-5,5]


  for map in maps:
    map['func'] = '[0]*x**2+[1]*x'
    map['strFunc'] = None
#  gammaBarrel['func'] = '[0] + [1]*x'
#  gammaBarrel['strFunc'] = getLinStr
#  gammaForwardPlus['func'] = '[0] + [1]*x'
#  gammaForwardPlus['strFunc'] = getLinStr
#  gammaForwardMinus['func'] = '[0] + [1]*x'
#  gammaForwardMinus['strFunc'] = getLinStr
  gammaBarrel['func'] = '[0]*x'
  gammaBarrel['strFunc'] = getPropStr
  gammaForwardPlus['func'] = '[0]*x'
  gammaForwardPlus['strFunc'] = getPropStr
  gammaForwardMinus['func'] = '[0]*x'
  gammaForwardMinus['strFunc'] = getPropStr
  

  for map in maps:
    fx = ROOT.TF1('fx', map['func'], *(map['fitRange']))
    fy = ROOT.TF1('fy', map['func'], *(map['fitRange']))
    
    if c:
      candSelCut = 'candId=='+str(label[map['type']])+'&&candEta>'+str(map['binning'][1])+'&&candEta<='+str(map['binning'][2])
      print "candSelCut", candSelCut
  #    binning=map['candBinning']
      binning=[50]+map['fitRange']
      px=ROOT.TProfile("p_MEx_"+map['name'],"p_MEx"+map['name'],*(binning+[-200,200,'i']))
      py=ROOT.TProfile("p_MEy_"+map['name'],"p_MEy"+map['name'],*(binning+[-200,200,'i']))
  #    c.Draw('Sum$(-('+candSelCut+')*candPt*cos(candPhi)):Sum$(('+map['candFunc']+')*('+candSelCut+'))>>p_MEx_'+map['name'],'','goff')
  #    c.Draw('Sum$(-('+candSelCut+')*candPt*sin(candPhi)):Sum$(('+map['candFunc']+')*('+candSelCut+'))>>p_MEy_'+map['name'],'','goff')
      c.Draw('Sum$(-('+candSelCut+')*candPt*cos(candPhi)):ngoodVertices>>p_MEx_'+map['name'],'','goff')
      c.Draw('Sum$(-('+candSelCut+')*candPt*sin(candPhi)):ngoodVertices>>p_MEy_'+map['name'],'','goff')
    else:
      px = getObjFromFile(options.input, 'pfMEtMultCorrInfoWriter/pfMEtMultCorrInfoWriter_'+mode+'_'+map['name'].replace('h_HF','hHF').replace('egamma_HF','egammaHF')+'_Px')
      py = getObjFromFile(options.input, 'pfMEtMultCorrInfoWriter/pfMEtMultCorrInfoWriter_'+mode+'_'+map['name'].replace('h_HF','hHF').replace('egamma_HF','egammaHF')+'_Py')
    if px and py:
      px.Fit(fx, 'R')
      py.Fit(fy,'R')
    else:
      print "Problem with input",options.input
      continue

    result = {'fx':fx.Clone(),'fy':fy.Clone()}

    c1 = ROOT.TCanvas()  
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptFit(0)
    px.Draw('h')
    if mode=="multiplicity":
      px.GetXaxis().SetTitle("multiplicity in "+map['name'])
    if mode=="sumPt":
      px.GetXaxis().SetTitle("#Sigma p_{T} of "+map['name'])
    if mode=="ngoodVertices":
      px.GetXaxis().SetTitle("ngoodVertices")
    px.GetYaxis().SetTitle("<#slash{E}_{x,y}> (GeV)")
  #    px.GetXaxis().SetLabelSize(0.04)
    px.GetXaxis().SetTitleSize(0.05)
    px.GetXaxis().SetTitleOffset(1.1)
    px.GetYaxis().SetRangeUser(*(map['zoomRange']))
    if map.has_key('plotRange'):
      px.GetXaxis().SetRangeUser(*(map['plotRange']))
    else:
      px.GetXaxis().SetRangeUser(*(map['fitRange']))
    px.SetLineColor(ROOT.kBlue)
    px.SetLineStyle(0)
    px.SetLineWidth(2)
    px.SetMarkerStyle(0)
    px.SetMarkerSize(0)
  #    py.GetYaxis().SetRangeUser(-20,20)
    py.SetLineColor(ROOT.kRed)
    py.SetLineStyle(0)
    py.SetLineWidth(2)
    py.SetMarkerStyle(0)
    py.SetMarkerSize(0)
    py.Draw('hsame')
    if mode=='ngoodVertices':
      if map.has_key('strFunc') and map['strFunc']:
        lines = [ [0.18, 0.78,  "<#slash{E}_{x}> = "+map['strFunc'](fx)],
                  [0.18, 0.73,  "<#slash{E}_{y}> = "+map['strFunc'](fy)]]
      else:
        lines = [ [0.18, 0.78,  "<#slash{E}_{x}> = 10^{-4}#upoint ("+str(round(10**4*fx.GetParameter(0),1))+'#pm '+str(round(10**4*abs(fx.GetParError(0)),1))+") #upoint n^{2}+10^{-3}#upoint("+str(round(10**3*fx.GetParameter(1),1))+'#pm '+str(round(10**3*abs(fx.GetParError(1)),1))+") #upoint n"],
                  [0.18, 0.73,  "<#slash{E}_{y}> = 10^{-4}#upoint ("+str(round(10**4*fy.GetParameter(0),1))+'#pm '+str(round(10**4*abs(fy.GetParError(0)),1))+") #upoint n^{2}+10^{-3}#upoint("+str(round(10**3*fy.GetParameter(1),1))+'#pm '+str(round(10**3*abs(fy.GetParError(1)),1))+") #upoint n"]]
  #    lines = [ [0.4, 0.78,  "<#slash{E}_{x}> = 10^{-3} #upoint ("+str(round(10**3*fx.GetParameter(0),1))+'#pm '+str(round(10**3*abs(fx.GetParError(0)),1))+") #upoint n"],
  #              [0.4, 0.73,  "<#slash{E}_{y}> = 10^{-3} #upoint ("+str(round(10**3*fy.GetParameter(0),1))+'#pm '+str(round(10**3*abs(fy.GetParError(0)),1))+") #upoint n"]]
  #  if mode=='multiplicity' or mode=='sumPt':
    else:
      if map.has_key('strFunc') and map['strFunc']:
        lines = [ [0.18, 0.78,  "<#slash{E}_{x}> = "+map['strFunc'](fx)],
                  [0.18, 0.73,  "<#slash{E}_{y}> = "+map['strFunc'](fy)]]
      else:
        lines = [ [0.18, 0.78,  "<#slash{E}_{x}> = 10^{-6}#upoint ("+str(round(10**6*fx.GetParameter(0),1))+'#pm '+str(round(10**6*abs(fx.GetParError(0)),1))+") #upoint n^{2}+10^{-3}#upoint("+str(round(10**3*fx.GetParameter(1),1))+'#pm '+str(round(10**3*abs(fx.GetParError(1)),1))+") #upoint n"],
                  [0.18, 0.73,  "<#slash{E}_{y}> = 10^{-6}#upoint ("+str(round(10**6*fy.GetParameter(0),1))+'#pm '+str(round(10**6*abs(fy.GetParError(0)),1))+") #upoint n^{2}+10^{-3}#upoint("+str(round(10**3*fy.GetParameter(1),1))+'#pm '+str(round(10**3*abs(fy.GetParError(1)),1))+") #upoint n"]]
  #  else:
  #    lines = [ [0.4, 0.78,  "<#slash{E}_{x}> = 10^{-3} #upoint ("+str(round(10**3*fx.GetParameter(0),1))+'#pm '+str(round(10**3*abs(fx.GetParError(0)),1))+") #upoint n"],
  #              [0.4, 0.73,  "<#slash{E}_{y}> = 10^{-3} #upoint ("+str(round(10**3*fy.GetParameter(0),1))+'#pm '+str(round(10**3*abs(fy.GetParError(0)),1))+") #upoint n"]]

    latex = ROOT.TLatex();
    latex.SetNDC();
    latex.SetTextSize(0.04);
    latex.SetTextAlign(11); # align right
    for line in lines:
        latex.SetTextSize(0.04)
        latex.DrawLatex(line[0],line[1],line[2])
    l = ROOT.TLegend(0.55,0.83,.95,.95)
    l.AddEntry(px, "< #slash{E}_{x} >")#+etab[0].split('_')[0]+", "+shortName[etab[0].split('_')[1]])
    l.AddEntry(py, "< #slash{E}_{y} >")
    l.SetFillColor(0)
    l.SetShadowColor(ROOT.kWhite)
    l.SetBorderSize(1)
    l.Draw()
    c1.Print(options.plotDir+'/'+prefix+mode+'_singleFit_MExy_'+map['name']+'.png')
    c1.Print(options.plotDir+'/'+prefix+mode+'_singleFit_MExy_'+map['name']+'.root')
    del px, py, l, c1



