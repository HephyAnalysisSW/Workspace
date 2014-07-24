import ROOT
import pickle
from commons import label
from Workspace.HEPHYPythonTools.helpers import getVarValue
from math import pi, cos, sin, sqrt, atan2
ROOT.gROOT.ProcessLine(".L ../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()
from commons import *

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--sample", dest="sample", default="dy53X", type="string", action="store", help="samples:Which samples.")
parser.add_option("--prefix", dest="prefix", default="", type="string", action="store", help="prefix:Which prefix.")
parser.add_option("--maps", dest="maps", default='all', type="string", action="store", help="samples:Which maps.")
parser.add_option("--small", dest="small", action="store_true", help="Just do a small subset.")
parser.add_option("--useMapWeight", dest="useMapWeight", action="store_true", help="use the stored map weight")

(options, args) = parser.parse_args()
prefixes=[]
if options.prefix!='':
  prefixes.append(options.prefix)
if options.small:
  prefixes.append('small')
if options.useMapWeight:
  prefixes.append('useMapWeight')

prefix = '_'.join(prefixes)
if prefix!='':
  prefix+='_'
print "options: sample",options.sample, 'maps', options.maps, 'small',options.small,'useMapWeight',options.useMapWeight,'prefix',options.prefix
if options.maps=='all':
  maps = allMaps
else:
  exec("maps = [" +options.maps+ "]")


c = ROOT.TChain('Events')

if options.sample == 'dy53X':
#sample = 'MinimumBias-Run2012A-22Jan2013'
  if options.small:
#    c.Add('/data/schoef/convertedMETTuples_v2/inc/'+options.sample+'/histo_'+options.sample+'*_from0To1.root')
    c.Add('/data/schoef/convertedMETTuples_v2/inc/dy53X_dy53X_rwTo_flat/histo_dy53X_from10To11.root')
  else:
#    c.Add('/data/schoef/convertedMETTuples_v2/inc/'+options.sample+'/histo_'+options.sample+'*.root')
    c.Add('/data/schoef/convertedMETTuples_v2/inc/dy53X_dy53X_rwTo_flat/histo_dy53X_from*')
if options.sample.lower().count('doublemu') or options.sample.lower().count('minimumbias') or options.sample.lower()=='ttjets':
  if options.small:
    c.Add('/data/schoef/convertedMETTuples_v2/inc/'+options.sample+'/histo_'+options.sample+'*_0.root')
    c.Add('/data/schoef/convertedMETTuples_v2/inc/'+options.sample+'/histo_'+options.sample+'*_1.root')
    c.Add('/data/schoef/convertedMETTuples_v2/inc/'+options.sample+'/histo_'+options.sample+'*_2.root')
    c.Add('/data/schoef/convertedMETTuples_v2/inc/'+options.sample+'/histo_'+options.sample+'*_3.root')
    c.Add('/data/schoef/convertedMETTuples_v2/inc/'+options.sample+'/histo_'+options.sample+'*_4.root')
    c.Add('/data/schoef/convertedMETTuples_v2/inc/'+options.sample+'/histo_'+options.sample+'*_5.root')
  else:
    c.Add('/data/schoef/convertedMETTuples_v2/inc/'+options.sample+'/histo_'+options.sample+'*.root')

h['fitRange'] = [0,1200]
h0Barrel['fitRange'] = [0,30]
h0EndcapPlus['fitRange'] = [0,30]
h0EndcapMinus['fitRange'] = [0,30]
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
h0Barrel['zoomRange'] = [-20,20]
h0EndcapPlus['zoomRange'] = [-20,20]
h0EndcapMinus['zoomRange'] = [-20,20]
gammaBarrel['zoomRange'] = [-20,20]
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

makeN2Fit =  [m['name'] for m in [ h_HF, h_HF_Minus, h_HF_Plus, h_HF_InnerMostRingsMinus, h_HF_InnerMostRingsPlus]]
makeN2Fit += [m['name'] for m in [ egamma_HF, egamma_HF_Minus, egamma_HF_Plus, egamma_HF_InnerMostRingsMinus, egamma_HF_InnerMostRingsPlus]]

#for map in [h_HF, egamma_HF]:
for map in maps:
#for map in [ h_HF, egamma_HF, h_HF_Minus, h_HF_Plus, h_HF_InnerMostRingsMinus, h_HF_InnerMostRingsPlus]:
  candSelCut = 'candId=='+str(label[map['type']])+'&&candEta>'+str(map['binning'][1])+'&&candEta<='+str(map['binning'][2])
  print 'sample',options.sample,"candSelCut", candSelCut
  if options.useMapWeight:
    weightString = '*candW'
  else:
    weightString = ''
  px=ROOT.TProfile("p_MEx_"+map['name'],"p_MEx"+map['name'],*(map['candBinning']+[-200,200,'i']))
  py=ROOT.TProfile("p_MEy_"+map['name'],"p_MEy"+map['name'],*(map['candBinning']+[-200,200,'i']))

  if map['name'] in makeN2Fit:
    fx = ROOT.TF1('fx', '[0]*x**2+[1]*x',*(map['fitRange']))
  else:
    fx = ROOT.TF1('fx', '[0]*x',*(map['fitRange']))
  c.Draw('Sum$(-('+candSelCut+')*candPt*cos(candPhi)'+weightString+'):Sum$('+candSelCut+')>>p_MEx_'+map['name'],'','goff')
  px.Fit(fx, 'R')
  param_x = '('+str(fx.GetParameter(0))+')*Sum$('+candSelCut+')'
  if map['name'] in makeN2Fit:
    param_x +="**2" 
    param_x += '+('+str(fx.GetParameter(1))+')*Sum$('+candSelCut+')'

  if map['name'] in makeN2Fit:
    fy = ROOT.TF1('fy', '[0]*x**2+[1]*x',*(map['fitRange']))
  else:
    fy = ROOT.TF1('fy', '[0]*x',*(map['fitRange']))
  c.Draw('Sum$(-('+candSelCut+')*candPt*sin(candPhi)'+weightString+'):Sum$('+candSelCut+')>>p_MEy_'+map['name'],'','goff')
  py.Fit(fy,'R')
  param_y = '('+str(fy.GetParameter(0))+')*Sum$('+candSelCut+')'
  if map['name'] in makeN2Fit:
    param_y +="**2" 
    param_y += '+('+str(fy.GetParameter(1))+')*Sum$('+candSelCut+')'

  result = {'fx':fx.Clone(),'fy':fy.Clone(), 'candCount':'Sum$('+candSelCut+')', 'MEx':'Sum$(-('+candSelCut+')*candPt*cos(candPhi))', 'MEy':'Sum$(-('+candSelCut+')*candPt*sin(candPhi))', 'param_x':param_x, 'param_y':param_y}
  
  if not options.small and not options.useMapWeight:
    pickle.dump(result, file('/data/schoef/tools/metPhiShifts/shift_'+prefix+options.sample+'_'+map['name']+'.pkl', 'w'))

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
  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngPF/'+prefix+options.sample+'_candidateBased_MExy_'+map['name']+'.png')
  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngPF/'+prefix+options.sample+'_candidateBased_MExy_'+map['name']+'.root')
  del px, py, l, c1



