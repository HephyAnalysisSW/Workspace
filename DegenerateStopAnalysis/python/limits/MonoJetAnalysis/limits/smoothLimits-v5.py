#
# Limit smoothing for T2DegStop limits
#
# Extracts values in a dm vs. mstop grid from mneut vs. mstop histograms,
# transforms to a dm vs. mstop histogram, interpolates one step in dm,
# smooths, calculates the contour and transforms back.
#
import ROOT
import sys
import ctypes,array
from optparse import OptionParser

#
# input parameters: input file name and names of the histograms
# with the different variations (exp. with +-1 and,optionally,  +-2 sigma bands; 
# observed)
#
hNames = { "expected" : "exp",
           "expPlus1" : "expP1",	
           "expPlus2" : "expP2",	
           "expMinus1" : "expM1",	
           "expMinus2" : "expM2",	
           "observed" : "obs" }
xsrefName = "stop13TeV_NLONLL"
xsupName = "stop13TeV_NLONLL_Up"
xsdownName = "stop13TeV_NLONLL_Down"

parser = OptionParser()
#parser.add_option("--type", "-t", dest="type",  help="type of limit", \
#                    action="store_true", default="EXP")
#parser.add_option("--xsecs", "-x",  dest="xsecs",  \
#                    choices = [ None, "stop8TeV_NLONLL", "stop8TeV_NLONLL_Up", "stop8TeV_NLONLL_Down" ], \
#                    default=None )
parser.add_option("--output",  dest="outputfile", help="output root filename", \
                    default="DegStop2016_singleLepton.root")
parser.add_option("--input",  dest="inputfile", help="input root filename", \
                    default="test.root")


parser.add_option("--processAbs",  dest="processAbs", help="smooth in absolute cross section", \
                    action="store_true", default=False)
parser.add_option("--interpolateOnly",  dest="interpolateOnly", help="skip smoothing", \
                    action="store_true", default=False)
parser.add_option("--drawOnly",  dest="drawOnly", help="skip interpolation & smoothing", \
                    action="store_true", default=False)
parser.add_option("--debug", "-d", dest="debug", help="debug", action="store_true", default=False)
parser.add_option("--saveDebug", dest="saveDebug",  help="save debug canvases", \
                    choices = [ None, "png", "pdf" ], default=None)
(options, args) = parser.parse_args()


fileName   = options.inputfile
outputfile = options.outputfile

if options.drawOnly:
  options.interpolateOnly = True

ROOT.gROOT.ProcessLine(".L useNiceColorPalette.C")
ROOT.useNiceColorPalette()
#cols = array.array("i",[ROOT.kRed-10,ROOT.kGreen-9])
#ROOT.gStyle.SetPalette(2,cols)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

ROOT.gROOT.ProcessLine(".L interpolate.h+")
ROOT.gROOT.ProcessLine(".L LimitSmoothing.C+")

execfile("xsecSMS.py")
exec("xsrefs = "+xsrefName)
exec("xsups = "+xsupName)
exec("xsdowns = "+xsdownName)

#mstopRange = ( 250, 800 )
mstopRange = ( 250, 800 )
dmRange = ( 10, 80 )
dmstopIn = 25
dmstopTmp = 25
ddmIn = 10
ddmTmp = 5

results = { }

def binning(xmin,xmax,dx):
  nb = int((xmax-xmin+(xmax-xmin)*0.001)/dx) + 1
  return (nb,xmin-dx/2.,xmax+dx/2.)


mstopBinsIn = binning(mstopRange[0],mstopRange[1],dmstopIn)
mstopBinsTmp = binning(mstopRange[0],mstopRange[1],dmstopTmp)
mstopBinsOut = binning(mstopRange[0],mstopRange[1],dmstopTmp)
dmBinsIn = binning(dmRange[0],dmRange[1],ddmIn)
dmBinsTmp = binning(dmRange[0],dmRange[1],ddmTmp)
mneutBinsOut = binning(mstopRange[0]-dmRange[1],mstopRange[1]-dmRange[0],ddmTmp)

def getLimit(fin,hname,hsuffix,xsref,xsec=None):

  global options
  global results

  hin = fin.Get(hname)
  if not hin:
    return None
  hin.UseCurrentStyle()
  xIn = hin.GetXaxis()
  yIn = hin.GetYaxis()


  ROOT.gROOT.cd()

  hnDmTmp = hname + hsuffix + "DmTmp"
  hDmTmp = ROOT.TH2F(hnDmTmp,hnDmTmp,mstopBinsTmp[0],mstopBinsTmp[1],mstopBinsTmp[2],
                        dmBinsTmp[0],dmBinsTmp[1],dmBinsTmp[2])
  xDmTmp = hDmTmp.GetXaxis()
  yDmTmp = hDmTmp.GetYaxis()

  #
  # transfer values from input histogram (mneut vs. mstop) to
  #   temporary histogram (dm vs. mstop)
  #
  for mstop in range(mstopRange[0],mstopRange[1]+dmstopIn,dmstopIn):
    ixIn = xIn.FindBin(mstop)
    ixDmTmp = xDmTmp.FindBin(mstop)
    for dm in range(dmRange[0],dmRange[1]+ddmIn,ddmIn):
      mneut = mstop - dm
      iyIn = yIn.FindBin(mneut)
      v = hin.GetBinContent(ixIn,iyIn)
#      if ( mstop==375 and dm==60 ) or ( mstop==100 and ( dm==10 or dm==20 ) ):
#        v = 0.
      iyDmTmp = yDmTmp.FindBin(dm)
      hDmTmp.SetBinContent(ixDmTmp,iyDmTmp,v)

  if options.debug:
    print "hDmTmp",hnDmTmp
    cDmRel = ROOT.TCanvas("cDmRel"+hname,"cDmRel"+hname)
    hDmTmp.SetMinimum(0.)
    hDmTmp.SetMaximum(2.)
    hDmTmp.DrawCopy("zcol")
    cDmRel.Update()
    if options.saveDebug!=None:
      cDmRel.SaveAs(cDmRel.GetName()+"."+options.saveDebug)

  if options.processAbs:
    #
    # rescale to absolute cross section (using reference)
    #
    for mstop in range(mstopRange[0],mstopRange[1]+dmstopTmp,dmstopTmp):
      ixDmTmp = xDmTmp.FindBin(mstop)
      for dm in range(dmRange[0],dmRange[1]+ddmTmp,ddmTmp):
        iyDmTmp = yDmTmp.FindBin(dm)
        v = hDmTmp.GetBinContent(ixDmTmp,iyDmTmp)
        v *= xsref[mstop]
        hDmTmp.SetBinContent(ixDmTmp,iyDmTmp,v)
    if options.debug:
      print "Abs",hnDmTmp
      cDmAbs = ROOT.TCanvas("cDmAbs"+hname,"cDmAbs"+hname)
      hDmTmp.SetMinimum(0.)
      hDmTmp.DrawCopy("zcol")
      cDmAbs.Update()
      if options.saveDebug!=None:
        cDmAbs.SaveAs(cDmAbs.GetName()+"."+options.saveDebug)

  if options.drawOnly:
    hinter = hDmTmp.Clone()
  else:
    hinter = ROOT.interpolate(hDmTmp,"EW")
  hninter = hname + hsuffix + "Inter"
  hinter.SetNameTitle(hninter,hninter)
  if options.debug:
    cinter = ROOT.TCanvas("cinter"+hname,"cinter"+hname)
    hinter.SetMinimum(0.)
    if not options.processAbs:
      hinter.SetMaximum(2.)
    print "hinter",hninter
    hinter.Draw("zcol")
    cinter.Update()
    if options.saveDebug!=None:
      cinter.SaveAs(cinter.GetName()+"."+options.saveDebug)

  if options.interpolateOnly:
    hsmooth = hinter.Clone()
  else:
    hsmooth = ROOT.doSmooth(hinter,1)
    hnsmooth = hname + hsuffix + "Smooth"
    hsmooth.SetNameTitle(hnsmooth,hnsmooth)

  if options.debug:
    csmooth = ROOT.TCanvas("csmooth"+hname,"csmooth"+hname)
    if xsec==None:
      hsmooth.SetMaximum(10.)
    hsmooth.SetMaximum(2.)
    hsmooth.DrawCopy("zcol")
    csmooth.Update()
    if options.saveDebug!=None:
      csmooth.SaveAs(csmooth.GetName()+"."+options.saveDebug)

  if not options.processAbs:
    #
    # rescale to absolute cross section (using reference)
    #   if not done before
    #
    for mstop in range(mstopRange[0],mstopRange[1]+dmstopTmp,dmstopTmp):
      ixDmTmp = xDmTmp.FindBin(mstop)
      for dm in range(dmRange[0],dmRange[1]+ddmTmp,ddmTmp):
        iyDmTmp = yDmTmp.FindBin(dm)
        v = hsmooth.GetBinContent(ixDmTmp,iyDmTmp)
        v *= xsref[mstop]
        hsmooth.SetBinContent(ixDmTmp,iyDmTmp,v)
    if options.debug:
      cDmAbs = ROOT.TCanvas("cDmAbs"+hname,"cDmAbs"+hname)
      hsmooth.SetMinimum(0.)
      hsmooth.SetMaximum(2.)
      hsmooth.DrawCopy("zcol")
      cDmAbs.Update()
      if options.saveDebug!=None:
        cDmAbs.SaveAs(cDmAbs.GetName()+"."+options.saveDebug)

  #
  # create output histogram (smoothed, absolute cross section limits)
  #
  hnout = hname + hsuffix + "Out"
  hout = ROOT.TH2F(hnout,hnout,mstopBinsOut[0],mstopBinsOut[1],mstopBinsOut[2],
                   mneutBinsOut[0],mneutBinsOut[1],mneutBinsOut[2])
  xOut = hout.GetXaxis()
  yOut = hout.GetYaxis()
  for mstop in range(mstopRange[0],mstopRange[1]+dmstopTmp,dmstopTmp):
    ixDmTmp = xDmTmp.FindBin(mstop)
    ixOut = xOut.FindBin(mstop)
    for dm in range(dmRange[0],dmRange[1]+ddmTmp,ddmTmp):
      mneut = mstop - dm
      iyDmTmp = yDmTmp.FindBin(dm)
      v = hsmooth.GetBinContent(ixDmTmp,iyDmTmp)
      iyOut = yOut.FindBin(mneut)
      hout.SetBinContent(ixOut,iyOut,v)
  if options.debug:
    cout = ROOT.TCanvas("cout"+hname,"cout"+hname)
    hout.Draw("zcol")
    cout.Update()
    if options.saveDebug!=None:
      cout.SaveAs(cout.GetName()+"."+options.saveDebug)


  #
  # now go back to relative and possibly apply cross section variation
  #
  csmoothMin = None
  csmoothMax = None
  for mstop in range(mstopRange[0],mstopRange[1]+dmstopTmp,dmstopTmp):
    ixDmTmp = xDmTmp.FindBin(mstop)
    for dm in range(dmRange[0],dmRange[1]+ddmTmp,ddmTmp):
      iyDmTmp = yDmTmp.FindBin(dm)
      v = hsmooth.GetBinContent(ixDmTmp,iyDmTmp)
      if xsec:
          v /= xsec[mstop]
      else:
          v /= xsref[mstop]
      hsmooth.SetBinContent(ixDmTmp,iyDmTmp,v)
      if csmoothMin==None or v<csmoothMin:
        csmoothMin = v
      if csmoothMax==None or v>csmoothMax:
        csmoothMax = v

  #
  # extract contour lines
  #
  ccont = ROOT.TCanvas("ccont","ccont")
  # contlist = [0.5,1.0,1.5]
  #
  # order of contours is wrong if one is empty (i.e., no result for that level)
  # try to avoid the problem by creating a list within min/max of the histogram
  #   (did not yet check if running into trouble if the list contains only 1 element)
  #
  contlist = [ ]
  for v in [0.5,1.0,1.5]:
    if v>=csmoothMin and v<=csmoothMax:
      contlist.append(v)
  if len(contlist)==0:
    contlist = [ 1.0 ]
  c_contlist = ((ctypes.c_double)*(len(contlist)))(*contlist)
  print len(contlist),c_contlist
  # retrieve contours (need to plot histogram in a temporary canvas)
  hsmooth.SetContour(len(contlist),c_contlist)
  hsmooth.Draw("contzlist")
  ccont.Update()
  #
  # retrieve contour(s) corresponding to contents=1 and delete temporary canvas
  #
  idx = contlist.index(1.0)
  contours_obs = ROOT.gROOT.GetListOfSpecials().FindObject("contours")
  graph_list = contours_obs.At(idx)
  del ccont

  if options.debug:
    print "Sample points on graphs"
    for g in graph_list:
      x = ROOT.Double(0.)
      y = ROOT.Double(0.)
      g.GetPoint(g.GetN()/2,x,y)
      print g.GetN()/2,x,y
    csmooth.cd()
    for g in graph_list:
      g.SetLineWidth(3)
      g.Draw("csame")
    csmooth.Update()
    if options.saveDebug!=None:
      csmooth.SaveAs(csmooth.GetName()+"."+options.saveDebug)
  #
  # transform graph from dm vs. mstop to mneut vs. mstop
  #   and superimpose on limit plot
  #
  graphs = [ ]
  for g in graph_list:
    graph = ROOT.TGraph()
    xp = ROOT.Double(0.)
    yp = ROOT.Double(0.)
    for ip in range(g.GetN()):
      g.GetPoint(ip,xp,yp)
      graph.SetPoint(ip,xp,xp-yp)
    graphs.append(graph.Clone())

  if options.debug:
    cout.cd()
    for g in graphs:
      g.SetLineWidth(3)
      g.Draw("csame")
    cout.Update()
    if options.saveDebug!=None:
      cout.SaveAs(cout.GetName()+"."+options.saveDebug)

  del contours_obs
  for g in graph_list:
    del g

  if options.debug:
    raw_input("Enter")

  return ( hout.Clone(), graphs )

fin = ROOT.TFile(fileName)
for t in hNames:
#  if t=="observed" or ( not hNames[t].startswith("expM") ):
#    continue
  if t=="observed":
    results[t] = getLimit(fin,hNames[t],"",xsrefs)
    results[t+"Up"] = getLimit(fin,hNames[t],"Up",xsrefs,xsups)
    results[t+"Down"] = getLimit(fin,hNames[t],"Down",xsrefs,xsdowns)
  else:
    results[t] = getLimit(fin,hNames[t],"",xsrefs)

cres = ROOT.TCanvas("smoothed_limits","smoothed_limits",800,700)
cres.SetLeftMargin(0.15)
cres.SetRightMargin(0.20)
hobs = results["observed"][0]
hobs.GetXaxis().SetTitle("m(#tilde{t}) [GeV]")
hobs.GetYaxis().SetTitle("m(#tilde{#chi}^{0}) [GeV]")
hobs.GetZaxis().SetTitle("95% CL upper limit on cross section [pb]")
hobs.GetXaxis().SetTitleOffset(0.80)
hobs.GetYaxis().SetTitleOffset(1.30)
hobs.GetZaxis().SetTitleOffset(1.40)
hobs.GetXaxis().SetTitleSize(0.05)
hobs.GetYaxis().SetTitleSize(0.05)
hobs.GetZaxis().SetTitleSize(0.05)
hobs.GetXaxis().SetTitleFont(42)
hobs.GetYaxis().SetTitleFont(42)
hobs.GetZaxis().SetTitleFont(42)
hobs.SetMinimum(0.1)
hobs.SetMaximum(100.)
hobs.Draw("zcol")
ROOT.gPad.SetLogz(1)

for t,r in results.iteritems():
  if r==None:
    continue
  for g in r[1]:
    if t.startswith("observed"):
      g.SetLineColor(2)
    else:
      g.SetLineColor(1)
    if t=="observed":
      g.SetLineWidth(3)
    elif t=="expected":
      g.SetLineWidth(3)
      g.SetLineStyle(2)
    else:
      g.SetLineWidth(2)
      g.SetLineStyle(3)
    g.Draw("csame")

header = ROOT.TLatex()
header.SetTextFont(42)
header.SetTextAlign(11)
header.SetTextSize(0.04)
header.SetNDC(1)
header.DrawLatex(0.16,0.925,'CMS preliminary  L=35.9fb^{-1}  #sqrt{s} = 13TeV')

desc = ROOT.TLatex()
desc.SetTextFont(42)
desc.SetTextAlign(11)
desc.SetTextSize(0.03)
desc.SetNDC(1)
#desc.DrawLatex(0.18,0.850,'Single muon channel')


ROOT.gPad.Update()

cres.SaveAs("smoothed_limits.png")
cres.SaveAs("smoothed_limits.pdf")
cres.SaveAs("smoothed_limits.root")

print results.keys()
outNameDict = {
  "observed" : "OBSOut",
  "observedDown" : "OBSDownOut",
  "observedUp" : "OBSUpOut",
  "expected" : "EXPOut",
  "expMinus1" : "M1SOut",
  "expMinus2" : "M2SOut",
  "expPlus1" : "P1SOut",
  "expPlus2" : "P2SOut"
}
#flim = ROOT.TFile("DegStop2016_singleLepton.root","recreate")
flim = ROOT.TFile("%s"%outputfile,"recreate")
print results
for k,n in outNameDict.iteritems():
  # write central observed and expected histograms
  if k=="expected" or k=="observed":
    h = results[k][0].Clone(n)
    h.Write()
  graphs = results[k][1]
  # check that there is only 1 graph
  #assert len(graphs)==1, graphs 
  # write graph
  g = graphs[0].Clone("g"+n+"0")
  g.Write()
flim.Close()

#raw_input("Enter")
