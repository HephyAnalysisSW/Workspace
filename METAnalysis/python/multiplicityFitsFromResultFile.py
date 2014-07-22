import ROOT
import pickle
from commons import label
from Workspace.HEPHYPythonTools.helpers import getVarValue, getObjFromFile
from math import pi, cos, sin, sqrt, atan2
ROOT.gROOT.ProcessLine(".L ../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()
from commons import *

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--prefix", dest="prefix", default="13TeV-WJetsToLNu_HT-100to200-Spring14dr-PU20bx25_POSTLS170_V5", type="string", action="store", help="prefix:Which prefix.")
parser.add_option("--maps", dest="maps", default='all', type="string", action="store", help="Which maps.")
parser.add_option("--infile", dest="infile", default='/data/schoef/metCorr_140605/13TeV-WJetsToLNu_HT-100to200-Spring14dr-PU20bx25_POSTLS170_V5.root', type="string", action="store", help="Which infile.")

(options, args) = parser.parse_args()
prefixes=[]
if options.prefix!='':
  prefixes.append(options.prefix)

prefix = '_'.join(prefixes)
if prefix!='':
  prefix+='_'
print 'maps', options.maps,'prefix',options.prefix, 'infile', options.infile
if options.maps=='all':
  maps = allMaps
else:
  exec("maps = [" +options.maps+ "]")


h['fitRange'] = [0,1500]
h0Barrel['fitRange'] = [0,50]
h0EndcapPlus['fitRange'] = [0,50]
h0EndcapMinus['fitRange'] = [0,50]
gammaBarrel['fitRange'] = [0,500]
gammaEndcapPlus['fitRange'] = [0,150]
gammaEndcapMinus['fitRange'] = [0,150]
gammaForwardPlus['fitRange'] = [0,10]
gammaForwardMinus['fitRange'] = [0,10]
e['fitRange'] = [0,10]
mu['fitRange'] = [0,10]
h_HF_Minus['fitRange'] = [10,250]
h_HF_Plus['fitRange'] = [10,250]
h_HF_InnerMostRingsMinus['fitRange'] = [0,50]
h_HF_InnerMostRingsPlus['fitRange'] = [0,50]
egamma_HF_Minus['fitRange'] = [0,250]
egamma_HF_Plus['fitRange'] = [0,250]
egamma_HF_InnerMostRingsMinus['fitRange'] = [0,50]
egamma_HF_InnerMostRingsPlus['fitRange'] = [0,50]
h_HF['fitRange'] = [0,500]
egamma_HF['fitRange'] = [0,500]

h['zoomRange'] = [-20,20]
h0Barrel['zoomRange'] = [-2,2]
h0EndcapPlus['zoomRange'] = [-5,5]
h0EndcapMinus['zoomRange'] = [-5,5]
gammaBarrel['zoomRange'] = [-2,2]
gammaEndcapPlus['zoomRange'] = [-20,20]
gammaEndcapMinus['zoomRange'] = [-20,20]
gammaForwardPlus['zoomRange'] = [-20,20]
gammaForwardMinus['zoomRange'] = [-20,20]
e['zoomRange'] = [-20,20]
mu['zoomRange'] = [-20,20]
h_HF_Minus['zoomRange'] = [-5,5]
h_HF_Plus['zoomRange'] = [-5,5]
h_HF_InnerMostRingsMinus['zoomRange'] = [-5,5]
h_HF_InnerMostRingsPlus['zoomRange'] = [-5,5]
egamma_HF_Minus['zoomRange'] = [-5,5]
egamma_HF_Plus['zoomRange'] = [-5,5]
egamma_HF_InnerMostRingsMinus['zoomRange'] = [-5,5]
egamma_HF_InnerMostRingsPlus['zoomRange'] = [-5,5]
h_HF['zoomRange'] = [-5,5]
egamma_HF['zoomRange'] = [-5,5]

makeN2Fit =  [m['name'] for m in maps] #[ h, h0EndcapPlus, h0EndcapMinus,  h_HF, h_HF_Minus, h_HF_Plus, h_HF_InnerMostRingsMinus, h_HF_InnerMostRingsPlus]]
#makeN2Fit += [m['name'] for m in [ egamma_HF, egamma_HF_Minus, egamma_HF_Plus, egamma_HF_InnerMostRingsMinus, egamma_HF_InnerMostRingsPlus]]

for map in maps:
  if map['name'] in makeN2Fit:
    fx = ROOT.TF1('fx', '[0]*x**2+[1]*x',*(map['fitRange']))
  else:
    fx = ROOT.TF1('fx', '[0]*x',*(map['fitRange']))
  px = getObjFromFile(options.infile, 'pfMEtMultCorrInfoWriter/pfMEtMultCorrInfoWriter_'+map['name'].replace('h_HF','hHF').replace('egamma_HF','egammaHF')+'_Px') 
  px.Fit(fx, 'R')

  if map['name'] in makeN2Fit:
    fy = ROOT.TF1('fy', '[0]*x**2+[1]*x',*(map['fitRange']))
  else:
    fy = ROOT.TF1('fy', '[0]*x',*(map['fitRange']))
  py = getObjFromFile(options.infile, 'pfMEtMultCorrInfoWriter/pfMEtMultCorrInfoWriter_'+map['name'].replace('h_HF','hHF').replace('egamma_HF','egammaHF')+'_Py') 
  py.Fit(fy,'R')

  result = {'fx':fx.Clone(),'fy':fy.Clone()}
  

  c1 = ROOT.TCanvas()  
  ROOT.gStyle.SetOptStat(0)
  ROOT.gStyle.SetOptFit(0)
  px.Draw('h')
  px.GetXaxis().SetTitle("multiplicity in "+map['name'])
  px.GetYaxis().SetTitle("<#slash{E}_{x,y}> (GeV)")
#    px.GetXaxis().SetLabelSize(0.04)
  px.GetXaxis().SetTitleSize(0.05)
  px.GetXaxis().SetTitleOffset(1.1)
  px.GetYaxis().SetRangeUser(*(map['zoomRange']))
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
  if map['name'] in makeN2Fit:
    lines = [ [0.18, 0.78,  "<#slash{E}_{x}> = 10^{-6}#upoint ("+str(round(10**6*fx.GetParameter(0),1))+'#pm '+str(round(10**6*abs(fx.GetParError(0)),1))+") #upoint n^{2}+10^{-3}#upoint("+str(round(10**3*fx.GetParameter(1),1))+'#pm '+str(round(10**3*abs(fx.GetParError(1)),1))+") #upoint n"],
              [0.18, 0.73,  "<#slash{E}_{y}> = 10^{-6}#upoint ("+str(round(10**6*fy.GetParameter(0),1))+'#pm '+str(round(10**6*abs(fy.GetParError(0)),1))+") #upoint n^{2}+10^{-3}#upoint("+str(round(10**3*fy.GetParameter(1),1))+'#pm '+str(round(10**3*abs(fy.GetParError(1)),1))+") #upoint n"]]
  else:
    lines = [ [0.4, 0.78,  "<#slash{E}_{x}> = 10^{-3} #upoint ("+str(round(10**3*fx.GetParameter(0),1))+'#pm '+str(round(10**3*abs(fx.GetParError(0)),1))+") #upoint n"],
              [0.4, 0.73,  "<#slash{E}_{y}> = 10^{-3} #upoint ("+str(round(10**3*fy.GetParameter(0),1))+'#pm '+str(round(10**3*abs(fy.GetParError(0)),1))+") #upoint n"]]

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
  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngPF/'+prefix+'candidateBasedFromFiled_MExy_'+map['name']+'.png')
  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngPF/'+prefix+'candidateBasedFromFiled_MExy_'+map['name']+'.root')
  del px, py, l, c1



