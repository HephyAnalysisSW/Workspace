import ROOT as R
import ctypes
import os, sys
path = os.path.abspath('../plots')
if not path in sys.path:
    sys.path.insert(1, path)

from xsecSMS import gluino8TeV_NLONLL, gluino8TeV_NLONLL_Up, gluino8TeV_NLONLL_Down
from smsInfo import xAxisTitle, yAxisTitle
R.gROOT.ProcessLine(".L ../../HEPHYPythonTools/scripts/root/useNiceColorPalette.C")
R.useNiceColorPalette(255)
R.gROOT.ProcessLine(".L TriangularInterpolation.C+")
R.gROOT.ProcessLine(".L LimitSmoothing.C+")
R.gROOT.ProcessLine(".L interpolate.h+")

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--interpolate", dest="interpolate", action="store_true", help="interpolate empty bins")
parser.add_option("--smooth", dest="smooth", action="store_true", help="smooth")
parser.add_option("--mode", dest="mode", default="full", type="string", action="store", help="mode: full or asymptotic")
(options, args) = parser.parse_args()


def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]

def readResFile(fpath):
    f = R.TFile.Open(fpath)
    t = f.Get("limit")
    l = t.GetLeaf("limit")
    qE = t.GetLeaf("quantileExpected")
    limit = {}
    preFac = 1.
    for i in range(t.GetEntries()):
        t.GetEntry(i)
#        limit["{0:.3f}".format(round(qE.GetValue(),3))] = preFac*l.GetValue()
        limit["{0:.3f}".format(round(qE.GetValue(),3))] = preFac*l.GetValue()
    f.Close()
    return limit

def cutGraph(graph, sms="T1tttt-madgraph"):
    newgraph = R.TGraph()
    newgraph.SetName(graph.GetName()+"_cut")
    x = R.Double(0)
    y = R.Double(0)
    skip = 0
    for i in range(graph.GetN()):
        graph.GetPoint(i,x,y)
        if sms=="T1tttt" and ((y+350)<(x+25)) and (y+350)>(x-25):
            skip+=1
            continue
        if sms=="T1tttt-madgraph" and x-y<200:
            print "Skipping",i,x,y
            skip+=1
            continue
        if sms=="T5tttt" and x-y<175:
          print i, x-y
          skip+=1
          continue
        newgraph.SetPoint(i-skip,x,y)
    return newgraph

home = os.environ["HOME"]
subDir = os.path.join(home,"www/pngLimit/")
assert os.path.isdir(subDir)
#sms = sys.argv[1]
#mode = "full"
#if len(sys.argv)>2 and sys.argv[2].lower()=="asymptotic":
#    mode = "asymptotic"
sms = args[0]
mode = options.mode
inputpath = None

R.gStyle.SetOptStat(0)
plotObserved = True
doInterpolate = options.interpolate
doSmooth = options.smooth
if options.smooth:
    doInterpolate = True
#inputpath = "/afs/hephy.at/scratch/s/schoefbeck/CMS/CMSSW_6_1_1/src/Workspace/RA4Analysis/limits/resultsAsymptotic/"
#inputpath = "/data/schoef/tmpWS/Workspace/RA4Analysis/limits/resultsAsymptotic_1_overlappingHT/"
#inputpath = "/data/schoef/tmpWS/Workspace/RA4Analysis/limits/resultsAsymptotic_Combined/"
#inputpath = "/data/schoef/tmpWS/Workspace/RA4Analysis/limits/resultsAsymptotic_unifiedLowHT/"
#mode = "asymptotic"

#inputpath = "/afs/hephy.at/scratch/s/schoefbeck/CMS/CMSSW_5_3_3_patch2/src/Workspace/RA4Analysis/limits/resultsAsymptotic_unifiedLowHT_ISRPDF/"

if sms=="T1t1t":
##T1t1t asymptotic
#sms = "T1t1t"
#mode="asymptotic"
  if mode=="asymptotic":
    inputpath = "/afs/hephy.at/scratch/s/schoefbeck/CMS/CMSSW_5_3_3_patch2/src/Workspace/RA4Analysis/limits/resultsAsymptotic_unifiedLowHT_noCombWeights_T1t1t/"
    prefix = "asymptotic_T1t1t_noCombWeights_smoothed"

####T1t1t full
#sms = "T1t1t"
#mode="full"
  else:
##inputpath = "/data/schoef/lim_130618_T1t1t_part0/outputToy/"
    inputpath = ["/data/adamwo/lim2_130726_T1t1t_part0/outputToy/"]
    prefix = "full_T1t1t_WAsmoothed_new"


elif sms=="T5tttt":
##T5tttt asymptotic
#sms = "T5tttt"
#mode="asymptotic"
  if mode=="asymptotic":
    inputpath = "/afs/hephy.at/scratch/s/schoefbeck/CMS/CMSSW_5_3_3_patch2/src/Workspace/RA4Analysis/limits/resultsAsymptotic_unifiedLowHT_noCombWeights_T5tttt/"
    prefix = "asymptotic_T5tttt_noCombWeights_smoothed"
##T5tttt full limit
#sms = "T5tttt"
#mode="full"
  else:
    inputpath = ["/data/adamwo/lim2_130726_T5tttt_part0/outputToy/", "/data/adamwo/lim2_130726_T5tttt_part1/outputToy/"]
    prefix = "full_T5tttt_new"

elif sms=="T1tttt":
##T1tttt pythia full limit
#sms = "T1tttt"
#mode="full"
  if mode=="full":
    inputpath = "/data/schoef/lim_130509/outputToy/"
    prefix = "test_full_ISRFSR_smoothed"

elif sms=="T1tttt-madgraph":
##T1tttt madgraph asymptotic limit
#sms = "T1tttt-madgraph"
#mode="asymptotic"
  if mode=="asymptotic":
##inputpath = "/afs/hephy.at/scratch/s/schoefbeck/CMS/CMSSW_5_3_3_patch2/src/Workspace/RA4Analysis/limits/resultsAsymptotic_test_useHT1000Inconsistent_T1tttt-madgraph/"
##inputpath = "/afs/hephy.at/scratch/s/schoefbeck/CMS/CMSSW_5_3_3_patch2/src/Workspace/RA4Analysis/limits/resultsAsymptotic_test_estimationModifier_0.9_T1tttt-madgraph/"
    inputpath = "/afs/hephy.at/scratch/s/schoefbeck/CMS/CMSSW_5_3_3_patch2/src/Workspace/RA4Analysis/limits/resultsAsymptotic_test_T1tttt-madgraph/"
    prefix = "asymptotic_T1tttt-madgraph"

##T1tttt madgraph full limit
#sms = "T1tttt-madgraph"
#mode="full"
  else:
##inputpath = ["/data/adamwo/lim2_130624_T1tttt-madgraph_part0/outputToy/", "/data/adamwo/lim2_130624_T1tttt-madgraph_part1/outputToy/", "/data/adamwo/lim2_130624_T1tttt-madgraph_part0/outputToy/", "/data/adamwo/lim2_130624_T1tttt-madgraph_part1/outputToy/"]
    inputpath = ["/data/adamwo/lim2_130726_T1tttt-madgraph_part0/outputToy/", "/data/adamwo/lim2_130726_T1tttt-madgraph_part1/outputToy/"]
    prefix = "full_T1tttt-madgraph_WASmoothing_new"

assert inputpath!=None

if type(inputpath)==type([]):
  allfiles=[]
  for d in inputpath:
    allfiles+=listdir_fullpath(d)
else:
  allfiles = listdir_fullpath(inputpath)

resfiles = []
for file in allfiles:
  if mode=="asymptotic":
    if file.count("higgsCombine_Asymptotic"):
        resfiles.append(file)
  else:
    if file.count("higgsCombineTest.HybridNew.mH120"):
        resfiles.append(file)

limits = {}
for tfile in resfiles:
  if mode=="asymptotic":
    mass_str = tfile.replace("higgsCombine_Asymptotic_","").replace(".root","").split("/")[-1].partition("_")
    try:
        varX = int(mass_str[0])
        varY = int(mass_str[2])
        limits[(varX,varY)] = readResFile(tfile)
        print "Succesfully read file",tfile
    except:
        print "Error reading file",tfile
        continue
  else:
    mass_str = tfile.split(".")[3]
    print mass_str
    try:
        varX = int(mass_str[:-4])
        varY = int(mass_str[-4:])
        limits[(varX,varY)] = readResFile(tfile)
        print "Succesfully read file",tfile, limits[(varX,varY)]
    except:
        print "Error reading file",tfile
        continue

#print limits
if mode=="asymptotic":
  title = "asymptotic limit"
else:
  title = "limit"

if sms=="T1tttt" or sms=="T1tttt-madgraph":
  varX_min = 400.
  varX_max = 1400.
  varX_bs = 25.
  varY_min = 0.
  varY_max = 750.
  varY_bs = 25.

if sms=="T1t1t":
  varX_min = 100.
  varX_max = 800.
  varX_bs = 25.
  varY_min = 100
  varY_max = 800.
  varY_bs = 25.
if sms=="T5tttt":
  varX_min = 800.
  varX_max = 1425.
  varX_bs = 25.
  varY_min = 225
  varY_max = 1200.
  varY_bs = 25.

args = [int((varX_max-varX_min)/varX_bs)+1,varX_min-varX_bs/2.,varX_max+varX_bs/2.,int((varY_max-varY_min)/varY_bs)+1,varY_min-varY_bs/2.,varY_max+varY_bs/2.]
h_limit         = R.TH2F("h_limit",   title, *args)
h_cont_obs      = R.TH2F("h_cont_obs",title, *args)
h_cont_exp      = R.TH2F("h_cont_exp",title, *args)
h_cont_exp_down = R.TH2F("h_cont_exp_down",title, *args)
h_cont_exp_up   = R.TH2F("h_cont_exp_up",title, *args)
h_cont_th_down  = R.TH2F("h_cont_th_down",title, *args)
h_cont_th_up    = R.TH2F("h_cont_th_up",title, *args)

for key in limits.keys():
  bin = h_limit.FindBin(key[0],key[1])
  if sms=="T1tttt" or sms=="T5tttt" or sms=="T1tttt-madgraph":
    mgl = key[0]
  if sms=="T1t1t":
    mgl = 1000

  xsec = gluino8TeV_NLONLL[mgl]
  xsec_Down = gluino8TeV_NLONLL_Down[mgl]
  xsec_Up = gluino8TeV_NLONLL_Up[mgl]
  xsec = gluino8TeV_NLONLL[mgl]
  try:
    h_limit.SetBinContent(bin,xsec*limits[key]["-1.000"])
    h_cont_obs.SetBinContent(bin,limits[key]["-1.000"])

    h_cont_exp.SetBinContent(bin,limits[key]["0.500"])
    h_cont_exp_down.SetBinContent(bin,limits[key]["0.160"])
    h_cont_exp_up.SetBinContent(bin,limits[key]["0.840"])
    h_cont_th_down.SetBinContent(bin,xsec_Down/xsec*limits[key]["-1.000"])
    h_cont_th_up.SetBinContent  (bin,xsec_Up/xsec*limits[key]["-1.000"])
  except:
    print "-> [observed limit] problem at ",key
    print "-> [obs] problem at ",key


#if sms=="T1t1t":
#  h_limit_interpolated = h_limit.Clone("h_limit_interpolated")
#  for h in [h_limit_interpolated, h_cont_obs, h_cont_exp, h_cont_exp_down, h_cont_exp_up, h_cont_th_down, h_cont_th_up]:
#    for msq in range(200, 825, 25): 
#      for mn in range(100,msq-75,25):
#        b = h.FindBin(msq, mn)
#        if h.GetBinContent(b)<10**-6:
#          cbins = [[msq-25, mn - 25], [msq-25, mn], [msq-25, mn + 25], [msq, mn - 25], [msq, mn + 25], [msq+25, mn - 25], [msq+25, mn ], [msq+25, mn + 25]]
#          av=0
#          count=0
#          for cb in cbins:
#            if cb[0]>=200 and cb[0]<=825 and cb[1]>=100 and cb[1]<=msq-75:
#              ib = h.FindBin(*cb)
#              cont = h.GetBinContent(ib)
#              if cont>10**-6:
#                av+=cont
#                count+=1
#          if count>0:
#            res=av/count
#          else:
#            res=0
#          h.SetBinContent(b, res)
        

if doInterpolate or doSmooth:
#  h_limit = R.doSmooth(R.doSmooth(h_limit,"ka3",2,0,0,1), "ka3",2,0,0,1)
  if sms=="T5tttt" or sms=="T1tttt-madgraph": #SW for T5tttt and T1tttt, "EW" for T1t1t, https://indico.cern.ch/conferenceDisplay.py?confId=256523
#    h_limit = R.rebin(R.rebin(R.rebin(R.rebin(R.rebin(R.interpolate(h_limit,"SW"), "SW"),"SW"),"SW"),"SW"),"SW")
#    h_cont_obs = R.rebin(R.rebin(R.rebin(R.rebin(R.rebin(R.interpolate(h_cont_obs,"SW"), "SW"),"SW"),"SW"),"SW"),"SW")
#    h_cont_exp = R.rebin(R.rebin(R.rebin(R.rebin(R.rebin(R.interpolate(h_cont_exp,"SW"), "SW"),"SW"),"SW"),"SW"),"SW")
#    h_cont_exp_down = R.rebin(R.rebin(R.rebin(R.rebin(R.rebin(R.interpolate(h_cont_exp_down,"SW"), "SW"),"SW"),"SW"),"SW"),"SW")
#    h_cont_exp_up = R.rebin(R.rebin(R.rebin(R.rebin(R.rebin(R.interpolate(h_cont_exp_up,"SW"), "SW"),"SW"),"SW"),"SW"),"SW")
#    h_cont_th_down = R.rebin(R.rebin(R.rebin(R.rebin(R.rebin(R.interpolate(h_cont_th_down,"SW"), "SW"),"SW"),"SW"),"SW"),"SW")
#    h_cont_th_up = R.rebin(R.rebin(R.rebin(R.rebin(R.rebin(R.interpolate(h_cont_th_up,"SW"), "SW"),"SW"),"SW"),"SW"),"SW")

    h_limit_ip = R.interpolate(h_limit, "SW")
    h_cont_obs_ip = R.interpolate(h_cont_obs, "SW")
    h_cont_exp_ip = R.interpolate(h_cont_exp, "SW")
    h_cont_exp_down_ip = R.interpolate(h_cont_exp_down, "SW")
    h_cont_exp_up_ip = R.interpolate(h_cont_exp_up, "SW")
    h_cont_th_down_ip = R.interpolate(h_cont_th_down, "SW")
    h_cont_th_up_ip = R.interpolate(h_cont_th_up, "SW")
        
  if sms=="T1t1t":
    print "Smoothing T1t1t!"
    h_limit_ip = R.interpolate(h_limit, "EW")
    h_cont_obs_ip = R.interpolate(h_cont_obs, "EW")
    h_cont_exp_ip = R.interpolate(h_cont_exp, "EW")
    h_cont_exp_down_ip = R.interpolate(h_cont_exp_down, "EW")
    h_cont_exp_up_ip = R.interpolate(h_cont_exp_up, "EW")
    h_cont_th_down_ip = R.interpolate(h_cont_th_down, "EW")
    h_cont_th_up_ip = R.interpolate(h_cont_th_up, "EW")

  if doSmooth:
      h_limit = R.doSmooth(h_limit_ip,1)
      h_cont_obs = R.doSmooth(h_cont_obs_ip,1)
      h_cont_exp = R.doSmooth(h_cont_exp_ip,1)
      h_cont_exp_down = R.doSmooth(h_cont_exp_down_ip,1)
      h_cont_exp_up = R.doSmooth(h_cont_exp_up_ip,1)
      h_cont_th_down = R.doSmooth(h_cont_th_down_ip,1)
      h_cont_th_up = R.doSmooth(h_cont_th_up_ip,1)
  else:
      h_limit = h_limit_ip.Clone()
      h_cont_obs = h_cont_obs_ip.Clone()
      h_cont_exp = h_cont_exp_ip.Clone()
      h_cont_exp_down = h_cont_exp_down_ip.Clone()
      h_cont_exp_up = h_cont_exp_up_ip.Clone()
      h_cont_th_down = h_cont_th_down_ip.Clone()
      h_cont_th_up = h_cont_th_up_ip.Clone()

  for h in [h_cont_obs, h_cont_exp, h_cont_exp_down, h_cont_exp_up, h_cont_th_down, h_cont_th_up]:
    for bx in range(1,h.GetNbinsX()+1):
      for by in range(1,h.GetNbinsY()+1):
        if h.GetBinContent(bx,by)==0.:
          h.SetBinContent(bx,by,1000.)
  
c_limit = R.TCanvas("c_limit", "")
c_limit.SetRightMargin(0.15)
if sms=="T1t1t":
  c_limit.SetRightMargin(0.1)

h_limit.SetTitle("")
h_limit.Draw("colz")
h_limit.GetZaxis().SetRangeUser(0.001,10)
h_limit.GetXaxis().SetTitle(xAxisTitle[sms])
h_limit.GetYaxis().SetTitle(yAxisTitle[sms])
h_limit.GetYaxis().SetTitleOffset(1.1)
#h_limit.GetZaxis().SetTitle("95% CL upper limit on #sigma [pb]")
h_limit.GetZaxis().SetTitle(" ")
h_limit.GetZaxis().SetTitleOffset(1.2)

R.gPad.SetLogz()

header = R.TLatex()
header.SetTextFont(22)
header.SetTextSize(0.04)
header.SetNDC(1)
header.DrawLatex(0.12,0.91,"CMS preliminary, L=19.4fb^{-1}, #sqrt{s}=8TeV")


contlist = [0.5,1.0,1.5]
idx = contlist.index(1.0)

c_contlist = ((ctypes.c_double)*(len(contlist)))(*contlist)

if plotObserved:
  c_cont_obs = R.TCanvas("c_cont_obs", title)
  h_cont_obs.SetContour(len(contlist),c_contlist)
  h_cont_obs.Draw("contzlist")
  c_cont_obs.Update()
else:
  c_cont_obs = R.TCanvas("c_cont_obs", title)
  h_cont_obs.SetContour(len(contlist),c_contlist)
  h_cont_exp.Draw("contzlist")
  c_cont_obs.Update()

contours_obs = R.gROOT.GetListOfSpecials().FindObject("contours")
graph_list_obs = contours_obs.At(idx)
graphs_obs = []
np = 0
idx_graph_obs = 0
for i in range(graph_list_obs.GetEntries()):
    graphs_obs.append( graph_list_obs.At(i).Clone("cont_obs_"+str(i)) )
    if graphs_obs[i].GetN()>np:
        np=graphs_obs[i].GetN()
        idx_graph_obs = i


c_cont_exp = R.TCanvas("c_cont_exp","expected "+title)
h_cont_exp.SetContour(len(contlist),c_contlist)
h_cont_exp.Draw("contzlist")
c_cont_exp.Update()
contours_exp = R.gROOT.GetListOfSpecials().FindObject("contours")
graph_list_exp = contours_exp.At(idx)
graphs_exp = []
np = 0
idx_graph_exp = 0
for i in range(graph_list_exp.GetEntries()):
    graphs_exp.append( graph_list_exp.At(i).Clone("cont_exp_"+str(i)) )
    if graphs_exp[i].GetN()>np:
        np=graphs_exp[i].GetN()
        idx_graph_exp = i

c_cont_exp_down = R.TCanvas("c_cont_exp_down","expected "+title)
h_cont_exp_down.SetContour(len(contlist),c_contlist)
h_cont_exp_down.Draw("contzlist")
c_cont_exp_down.Update()
contours_exp_down = R.gROOT.GetListOfSpecials().FindObject("contours")
graph_list_exp_down = contours_exp_down.At(idx)
graphs_exp_down = []
np = 0
idx_graph_exp_down = 0
for i in range(graph_list_exp_down.GetEntries()):
    graphs_exp_down.append( graph_list_exp_down.At(i).Clone("cont_exp_down_"+str(i)) )
    if graphs_exp_down[i].GetN()>np:
        np=graphs_exp_down[i].GetN()
        idx_graph_exp_down = i

c_cont_exp_up = R.TCanvas("c_cont_exp_up","expected "+title)
h_cont_exp_up.SetContour(len(contlist),c_contlist)
h_cont_exp_up.Draw("contzlist")
c_cont_exp_up.Update()
contours_exp_up = R.gROOT.GetListOfSpecials().FindObject("contours")
graph_list_exp_up = contours_exp_up.At(idx)
graphs_exp_up = []
np = 0
idx_graph_exp_up = 0
for i in range(graph_list_exp_up.GetEntries()):
    graphs_exp_up.append( graph_list_exp_up.At(i).Clone("cont_exp_up_"+str(i)) )
    if graphs_exp_up[i].GetN()>np:
        np=graphs_exp_up[i].GetN()
        idx_graph_exp_up = i

c_cont_th_down = R.TCanvas("c_cont_th_down","expected "+title)
h_cont_th_down.SetContour(len(contlist),c_contlist)
h_cont_th_down.Draw("contzlist")
c_cont_th_down.Update()
contours_th_down = R.gROOT.GetListOfSpecials().FindObject("contours")
graph_list_th_down = contours_th_down.At(idx)
graphs_th_down = []
np = 0
idx_graph_th_down = 0
for i in range(graph_list_th_down.GetEntries()):
    graphs_th_down.append( graph_list_th_down.At(i).Clone("cont_th_down_"+str(i)) )
    if graphs_th_down[i].GetN()>np:
        np=graphs_th_down[i].GetN()
        idx_graph_th_down = i

c_cont_th_up = R.TCanvas("c_cont_th_up","expected "+title)
h_cont_th_up.SetContour(len(contlist),c_contlist)
h_cont_th_up.Draw("contzlist")
c_cont_th_up.Update()
contours_th_up = R.gROOT.GetListOfSpecials().FindObject("contours")
graph_list_th_up = contours_th_up.At(idx)
graphs_th_up = []
np = 0
idx_graph_th_up = 0
for i in range(graph_list_th_up.GetEntries()):
    graphs_th_up.append( graph_list_th_up.At(i).Clone("cont_th_up_"+str(i)) )
    if graphs_th_up[i].GetN()>np:
        np=graphs_th_up[i].GetN()
        idx_graph_th_up = i

c_limit.cd()

graph_exp_cut = cutGraph(graphs_exp[idx_graph_exp], sms)
graph_exp_cut.SetLineWidth(2)
graph_exp_cut.SetLineColor(R.kRed)
graph_exp_cut.Draw("csame")

graph_exp_down_cut = cutGraph(graphs_exp_down[idx_graph_exp_down],sms)
graph_exp_down_cut.SetLineWidth(2)
graph_exp_down_cut.SetLineColor(R.kRed)
graph_exp_down_cut.SetLineStyle(R.kDashed)
graph_exp_down_cut.Draw("csame")

graph_exp_up_cut = cutGraph(graphs_exp_up[idx_graph_exp_up],sms)
graph_exp_up_cut.SetLineWidth(2)
graph_exp_up_cut.SetLineColor(R.kRed)
graph_exp_up_cut.SetLineStyle(R.kDashed)
graph_exp_up_cut.Draw("csame")

graph_th_down_cut = cutGraph(graphs_th_down[idx_graph_th_down],sms)
graph_th_down_cut.SetLineWidth(2)
graph_th_down_cut.SetLineColor(R.kBlue)
#graph_th_down_cut.SetLineStyle(R.kDashed)
graph_th_down_cut.Draw("csame")

graph_th_up_cut = cutGraph(graphs_th_up[idx_graph_th_up],sms)
graph_th_up_cut.SetLineWidth(2)
graph_th_up_cut.SetLineColor(R.kBlue)
#graph_th_up_cut.SetLineStyle(R.kDashed)
graph_th_up_cut.Draw("csame")


graph_obs_cut = cutGraph(graphs_obs[idx_graph_obs],sms)
graph_obs_cut.SetLineWidth(2)
graph_obs_cut.Draw("csame")

c_limit.Update()
if plotObserved:
  R.gPad.SetRightMargin(1.5)
  legend = R.TLegend(0.12,0.65,0.42,0.89)
  legend.SetBorderSize(0)
  legend.SetFillStyle(0)
  legend.SetTextSize(0.04)
  legend.SetTextFont(22)
  legend.SetHeader(sms+" model, NLO-NLL exclusions")
  legend.AddEntry(graph_obs_cut,"Observed","L")
  legend.AddEntry(graph_th_up_cut,"#pm 1#sigma(theor.)","L")
  legend.AddEntry(graph_exp_cut,"Expected","L")
  legend.AddEntry(graph_exp_up_cut,"#pm 1#sigma(exp.)","L")
  legend.Draw()

  latex = R.TLatex()
  latex.SetTextFont(22)
  latex.SetTextSize(0.04)
  latex.SetNDC(1)
  if sms=="T1tttt-madgraph": 
    latex.DrawLatex(0.5,0.78,"Single lepton channel")
    latex.DrawLatex(0.485,0.73,"  E_{T}^{miss} template method")
  if sms=="T5tttt":
    latex.DrawLatex(0.35, 0.805,"Single lepton channel")
    latex.DrawLatex(0.335,0.755,"  E_{T}^{miss} template method")
    
  if not (sms=="T1tttt-madgraph" or sms=="T5tttt"):
    latex.DrawLatex(0.13,0.58,"Single lepton channel")
    latex.DrawLatex(0.13,0.53,"  E_{T}^{miss} template method")

  savename = subDir+"limit_"+prefix+"_obs"
  if doSmooth:
      savename += "_smooth"
  elif doInterpolate:
      savename += "_interpol"
  c_limit.SaveAs(savename+".png")
  c_limit.SaveAs(savename+".pdf")
  c_limit.SaveAs(savename+".root")
  foutname = subDir+"limit_"+prefix+"_out"
  if doSmooth:
      foutname += "_smooth"
  elif doInterpolate:
      foutname += "_interpol"
  fout = R.TFile(foutname+".root","recreate")
  h_limit.Write()
  graph_obs_cut.SetName("graph_obs")
  graph_obs_cut.Write()
  graph_th_down_cut.SetName("graph_th_down")
  graph_th_down_cut.Write()
  graph_th_up_cut.SetName("graph_th_up")
  graph_th_up_cut.Write()
  graph_exp_cut.SetName("graph_exp")
  graph_exp_cut.Write()
  graph_exp_down_cut.SetName("graph_exp_down")
  graph_exp_down_cut.Write()
  graph_exp_up_cut.SetName("graph_exp_up")
  graph_exp_up_cut.Write()
  fout.Close()
  
else:
  c_limit.SaveAs(subDir+"limit_"+prefix+".png")
  c_limit.SaveAs(subDir+"limit_"+prefix+".pdf")

