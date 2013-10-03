import ROOT, copy, pickle
from array import array
#ROOT.gROOT.SetStyle("Plain")
#ROOT.gROOT.ForceStyle()
ROOT.gROOT.ProcessLine(".L ../scripts/tdrstyle.C")
ROOT.setTDRStyle()
from simplePlotsLocals import *
dataColor =   ROOT.kBlack
caloColor =  ROOT.kYellow
typeIColor =  ROOT.kYellow
typeIIColor =  ROOT.kYellow
tcColor   =  896  #red
pfColor   =  38   #blue
myBlue   =  38   #blue

bold  = "\033[1m"
reset = "\033[0;0m"
def b(s):
  if type(s)!=type(""):
    s = str(s)
  return bold+s+reset

def pload(varstr, sfile):
  print globals().has_key(varstr)
  if not globals().has_key(varstr):
    globals()[varstr] = pickle.load(open(sfile))

ROOT_colors = [ROOT.kBlack, ROOT.kRed+1, ROOT.kBlue+1, ROOT.kMagenta+1, ROOT.kOrange+1,ROOT.kRed-3, ROOT.kAzure+6, ROOT.kViolet-5, ROOT.kOrange , ROOT.kRed-10]

def getVarValue(c, var, n=0):
  varNameHisto = var
  leaf = c.GetAlias(varNameHisto)
  if leaf!='':
    return c.GetLeaf(leaf).GetValue(n)
  else:
    return float('nan')

def getValue(chain, varname):
  alias = chain.GetAlias(varname)
  if alias!="":
    return chain.GetLeaf( alias ).GetValue()
  else:
    return chain.GetLeaf( varname ).GetValue()


def frange(start, end=None, inc=None):
    "A range function, that does accept float increments..."
    if end == None:
        end = start + 0.0
        start = 0.0
    else: start += 0.0 # force it to be a float
    if inc == None:
        inc = 1.0
    count = int((end - start) / inc)
    if start + count * inc != end:
        # need to adjust the count.
        # AFAIKT, it always comes up one short.
        count += 1
    L = [None,] * count
    for i in xrange(count):
        L[i] = start + i * inc
    return L

def getABCDDataFileName(var1, var2, var1_cut1_, var1_cut2_, var1_cut3_, var2_cut1_, var2_cut2_, var2_cut3_):
 return var1+"_"+str(var1_cut1_)+"_"+str(var1_cut2_)+"_"+str(var1_cut3_)+"_"+var2+"_"+str(var2_cut1_)+"_"+str(var2_cut2_)+"_"+str(var2_cut3_)+".py"

def getMSUGRAString(var_m0,var_m12,var_tanb,var_A0,var_signmu):
  return "m0_"+str(int(var_m0))+"_m12_"+str(int(var_m12))+"_tanb_"+str(int(var_tanb))+"_A0_"+str(int(var_A0))+"_Mu_"+str(int(var_signmu))

def getMSUGRAShortString(var_m0,var_m12,var_tanb,var_A0,var_signmu):
  return "msugra_"+str(int(var_m0))+"_"+str(int(var_m12))+"_"+str(int(var_tanb))+"_"+str(int(var_A0))+"_"+str(int(var_signmu))

def getOSTShortString(var_model, var_mgl, var_mn, var_mc):
  return var_model+"_"+str(int(var_mgl))+"_"+str(int(var_mn))+"_"+str(int(var_mc))

def getHTBinCutString(htval):
  cs1="(1)"
  if htval[0]>0:
    cs1 = "ht>"+str(htval[0])
  cs2="(1)"
  if htval[1]>0:
    cs2 = "ht<"+str(htval[1])
  if cs1=="(1)":
    return cs2 
  if cs2=="(1)":
    return cs1
  return "("+cs1+"&&"+cs2+")"

def addCutString(s1,s2):
  if s1=="":
    return s2
  return s1+"&&"+s2

def cmsPrel(xpos = 0.02, ypos = 0.95, intLumi=-1): 
 latex = ROOT.TLatex();
 latex.SetNDC();
 latex.SetTextSize(0.035);

 latex.SetTextAlign(11); # align right
 latex.DrawLatex(0.98,0.95,"#sqrt{s} = 7 TeV");
# if intLumi > 0. :
#   latex.SetTextAlign(31); # align right
#   latex.DrawLatex(0.98,0.88,Form("#int #font[12]{L}dt = %.1f
#nb^{-1}",intLumi));
 latex.SetTextAlign(11); # align left
 return latex.DrawLatex(xpos, ypos, "#font[22]{CMS preliminary 2012}");

def getLinesForStack(stack, lumi = -1, xpos = -1, ypos = -1):
  if type(lumi) == type(""):
    stack[0].lines = [[0.17,0.963,'#sqrt{s} = 8TeV'], [0.36,0.963,"#font[22]{CMS preliminary}"], [0.75, 0.963, "L = "+lumi]]
  else:
#    stack[0].lines = [[0.17,0.963,'#sqrt{s} =87TeV'], [0.36,0.963,"#font[22]{CMS preliminary}"], [0.75, 0.963, "L_{int} = "+str(int(round(lumi)))+" pb^{-1}"]]
    stack[0].lines = [[0.17,0.963,'#sqrt{s} = 8TeV'], [0.36,0.963,"#font[22]{CMS preliminary}"], [0.75, 0.963, "L_{int} = "+str(int(round(lumi)))+" pb^{-1}"]]
  if lumi<-1:
    stack[0].lines = stack[0].lines[:2]

#class ncolor:
#  allColors = [ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kGreen, ROOT.kMagenta, ROOT.kOrange]
#  ncolor=0
#  colcycles=0
#  def reset(__self__):
#    self.ncolor=0
#    self.colcycles=0
#  def nextColor(__self__):
#    self.ncolor+=1
#    if self.ncolor==len(allColors):
#      self.ncolor=1
#      self.colcycles+=1
#    return allColors[self.ncolor-1] + self.colcycles
    

upperrightlines=[[0.62,0.7,"#font[22]{CMS preliminary 2012}"],[0.62,0.65,"#sqrt{s} = 8TeV"]]
upperrightlines2=[[0.62,0.75,"#font[22]{CMS preliminary 2012}"],[0.62,0.7,"#sqrt{s} = 8TeV"]]
upperleftlines=[[0.2,0.88,"#font[22]{CMS preliminary 2012}"],[0.2,0.83,"#sqrt{s} = 8TeV"]]
middlerightlines=[[0.62,0.6,"#font[22]{CMS preliminary 2012}"],[0.62,0.55,"#sqrt{s} = 8TeV"]]


class variable:
  name = ""
  hname = ""
  binning = [0,0,0]
  texname=""
  cutstring=""
  title=""
  legendText=""
  legendCoordinates=[0.62,0.75,.98,.95]
  floating = False
  reweightVar = ""
  reweightHisto = ""
  scale = 1.
#  cprlCoordinates=[]

  lines=upperrightlines
  sample=""
  style="e"
  color=ROOT.kBlue
  markerStyle=-1
  normalizeTo=""
  normalizeWhat=""
  add=[]
  legendBoxed=True
  minimum = ""
  maximum = ""
  addOverFlowBin = ""
  varfunc=""
  dataMCRatio = []
  ratioMin = 0.
  ratioMax = 1.9
  logRatio = False
  ratioVarName = "Data / MC"
  def __init__(self, name, binning, cutfunc="", profile=False, varfunc = ""):
    self.initname = name
    sname=""
    self.title=""
    self.varfunc = varfunc
    if name.count(":")>0:
      sname = name.split(":")
      self.title = sname[0]
      self.name = sname[1]
    else:
      self.name=name
    if len(sname)==3:
      self.cutstring = sname[2]
    self.titleaxisstring=""
    splitsemic = self.name.split(";")
    if len(splitsemic)==3:
      self.name = splitsemic[0]
      self.titleaxisstring=";"+splitsemic[1]+";"+splitsemic[2]
    self.binning=binning

#    if self.prefix!="":
#      self.hname=self.prefix+"_"+self.name
#    else:
    if self.title!="":
      self.hname=self.title
    try:
      if type(self.data_histo)==type(ROOT.TH1F()):
        del self.data_histo
    except:
      pass
    self.title = self.hname+self.titleaxisstring
    self.data_histo = ROOT.TH1F(self.name+"_Data",self.hname+self.titleaxisstring,*binning)
    self.data_histo.Sumw2()
    if profile:
      self.data_histo = ROOT.TProfile(self.name+"_Data",self.hname+self.titleaxisstring,*binning)

    self.data_histo.Reset()
    self.cutfunc=cutfunc
    self.logy=False
    self.logx=False
    self.color=ROOT.kBlue

  binningIsExplicit = False
  def setExplicitBinning(self, binning):
    self.binningIsExplicit = True
    csqbins = array('d',binning)
    if len(binning)<2:
      print "Warning! setExplicitBinning with len(binning)<2 for var", self,"skipped!"
    else:
      self.data_histo.SetBins(len(binning) - 1, csqbins)
      self.binning = csqbins 

allVars=[]
allStacks=[]
allSamples=[]
stuff=[]
def drawStack(stack,normalized=False):
  counter=0;
#  ROOT.setTDRStyle()
#  ROOT.gStyle.SetOptStat(0)
#  ROOT.gStyle.SetTitleBorderSize(0)
#  ROOT.gStyle.SetTitleX(0.1)
#  ROOT.gStyle.SetTitleY(0.982)
#  ROOT.gStyle.SetTitleSize(0.010)
  l = ROOT.TLegend(*(stack[0].legendCoordinates))
  stuff.append(l)
  l.SetFillColor(0)
  l.SetShadowColor(ROOT.kWhite)
  l.SetBorderSize(1)
  if not stack[0].legendBoxed:
    l.SetBorderSize(0)
  first=True
  rescale=1
  returnDataForDataOverMC = ""
  returnMCForDataOverMC = ""
  for var in stack:
    hcopy = var.data_histo.Clone()
    hcopy.SetTitle("")
    counter=counter+1
#    hcopy.GetXaxis().SetTitleSize(0.055)
#    hcopy.GetXaxis().SetTitleOffset(0.78)
    if var.style[0] == "e":
      hcopy.SetMarkerColor(var.color)
      hcopy.SetLineColor(var.color)
      if var.markerStyle>0:
        hcopy.SetMarkerStyle(var.markerStyle)
      else:
        hcopy.SetMarkerStyle(20)
      hcopy.SetMarkerSize(1)
    if var.style[0] == "f":
      hcopy.SetLineColor(ROOT.kBlack)
      hcopy.SetLineStyle(0)
      hcopy.SetLineWidth(0)
      hcopy.SetFillColor(var.color)
      hcopy.SetMarkerColor(ROOT.kBlack);
      hcopy.SetMarkerStyle(0);
    if var.style[0] == "l":
      hcopy.SetLineColor(var.color)
      hcopy.SetLineStyle(0)
      hcopy.SetLineWidth(0)
      if len(var.style)>=3:
        hcopy.SetLineWidth(int(var.style[2]))
      hcopy.SetMarkerColor(var.color)
      hcopy.SetMarkerStyle(0);
    stuff.append(hcopy)
    hcopy.GetYaxis().SetRangeUser(1,1.5*hcopy.GetMaximum())
#    hcopy.GetYaxis().SetTitleOffset(1.3)
    scaleFac = 1.
    if  var.normalizeTo!="":
      if normalized:
        print "Warning: normalizeTo!=0 and plotting normalized (overrides)!"
      if var.normalizeWhat=="":
        if hcopy.Integral()>0:
          if type(var.normalizeTo) == type(float()) or type(var.normalizeTo) == type(int()):
            scaleFac = 1. # Don't do anything if normalized to Data; The weight should take care of normalization 
          else:
            scaleFac = var.normalizeTo.data_histo.Integral()/hcopy.Integral()
      else:
        refValue = var.normalizeWhat.data_histo.Integral()
        if refValue>0:
          scaleFac = var.normalizeTo.data_histo.Integral()/refValue
        else:
          print "Warning! (Not scaled!)",var.name,"normalizeTo",var.normalizeTo.name,var.normalizeTo.cutfunc,"normalizeWhat",var.normalizeWhat.name,var.normalizeWhat.cutfunc,"has Integral",refValue
    if type(var.sample) == type({}):
      print var.name,var.sample["name"],hcopy.Integral(),"scaleFac",scaleFac
    hcopy.Scale(scaleFac)
    if first:
      if var.style[0] == "e":
        if var.minimum!="":
           hcopy.SetMinimum(var.minimum)
        if var.maximum!="":
           hcopy.SetMaximum(var.maximum)
        hcopy.Draw("e1")
      if var.style[0] == "f" or var.style[0] == "l":
        if var.minimum!="":
           hcopy.SetMinimum(var.minimum)
        if var.maximum!="":
           hcopy.SetMaximum(var.maximum)
        hcopy.Draw("h")
      first=False
      if normalized:
        rescale = hcopy.Integral()
        print var.name, rescale
    else:
      if normalized:
        integr = hcopy.Integral()
        print var.name, rescale, integr
        if integr>0:
          hcopy.Scale(rescale/integr)
      if var.style[0] == "e":
        if var.minimum!="":
           hcopy.SetMinimum(var.minimum)
        if var.maximum!="":
           hcopy.SetMaximum(var.maximum)
        hcopy.Draw("e1same")
      if var.style[0] == "f" or var.style[0] == "l":
        if var.minimum!="":
           hcopy.SetMinimum(var.minimum)
        if var.maximum!="":
           hcopy.SetMaximum(var.maximum)
        hcopy.Draw("hsame")
    if var.legendText!="":
      l.AddEntry(hcopy, var.legendText)
    if len(stack[0].dataMCRatio) == 2:
      if stack[0].dataMCRatio[0] == var:
        returnDataForDataOverMC = hcopy.Clone()
      if stack[0].dataMCRatio[1] == var:
        returnMCForDataOverMC = hcopy.Clone()
    if len(var.style)>=2:
      if var.style[1] =="0":
        for nbin in range(0, hcopy.GetNbinsX()+1):
          hcopy.SetBinError(nbin, 0.)
  ROOT.gPad.RedrawAxis()
  l.Draw()
  if not stack[0].legendBoxed:
    ROOT.gPad.RedrawAxis()
  latex = ROOT.TLatex();
  latex.SetNDC();
  latex.SetTextSize(0.04);
  latex.SetTextAlign(11); # align right
  for line in stack[0].lines:
    stuff.append(latex.DrawLatex(line[0],line[1],line[2]))
  if len(stack[0].dataMCRatio) == 2:
    return [returnDataForDataOverMC, returnMCForDataOverMC]

#def replaceNameForRatio(namestring):
#  sstring = namestring.split(";")
#  return sstring[0]+";"+sstring[1]+";Data / MC"

def drawNMStacks(intn, intm, thesestacks, filename, normalized=False, path = defaultWWWPath):
  yswidth = 500
  ylwidth = 700
  ywidth = yswidth
  if len(thesestacks[0][0].dataMCRatio)==2:
    ywidth = ylwidth
  scaleFacBottomPad = yswidth/float((ylwidth-yswidth))
  yBorder = (ylwidth-yswidth)/float(ylwidth)
  c1 = ROOT.TCanvas("ROOT.c1","drawHistos",200,10,500*intn,ywidth*intm)
  c1.SetFillColor(0)
  if intn!=1 or intm!=1:
    c1.Divide(intn,intm)
  for istack in range(intn*intm):
    stack=0
    if istack<len(thesestacks):
      stack = thesestacks[istack]
    else:
      print "Only",len(thesestacks),"stacks supplied, expected", intn*intm
      continue
    if stack=="":
      continue
    if intn*intm!=1:
      thisPad = c1.cd(istack+1)
    else:
      thisPad = c1
    if stack[0].logy:
      thisPad.SetLogy()
    else:
      thisPad.SetLogy(0)
    if stack[0].logx:
      thisPad.SetLogx()
    else:
      thisPad.SetLogx(0)
    if len(stack[0].dataMCRatio)==2:
      thisPad.Divide(1,2,0,0)
      toppad = thisPad.cd(1)
      if stack[0].logy:
        toppad.SetLogy()
      else:
        toppad.SetLogy(0)
      if stack[0].logx:
        toppad.SetLogx()
      else:
        toppad.SetLogx(0)
      toppad.SetBottomMargin(0)
      toppad.SetTopMargin(0.05)
      toppad.SetRightMargin(0.02)
      toppad.SetPad(toppad.GetX1(), yBorder, toppad.GetX2(), toppad.GetY2())
      datamcstacks = drawStack(thesestacks[istack], normalized)
      bottompad = thisPad.cd(2)
      bottompad.SetTopMargin(0)
      bottompad.SetRightMargin(0.02)
      bottompad.SetBottomMargin(scaleFacBottomPad*0.13)
      bottompad.SetPad(bottompad.GetX1(), bottompad.GetY1(), bottompad.GetX2(), yBorder)
      rvar = variable(stack[0].initname, stack[0].binning, stack[0].cutfunc)
      rvar.data_histo.Sumw2()
      rvar.logy = False
      rvar.minimum=0.2
      rvar.maximum=1.7
      rvar.data_histo = datamcstacks[0] 
      rvar.data_histo.Divide(datamcstacks[1])
      rvar.lines = []
      rvar.style = "e"
      rvar.color = stack[0].dataMCRatio[0].color
      rvar.legendCoordinates = [0,0,0,0]
      rvar.dataMCratio=""
      rvar.data_histo.GetXaxis().SetTitleSize(scaleFacBottomPad*rvar.data_histo.GetXaxis().GetTitleSize())
      rvar.data_histo.GetXaxis().SetLabelSize(scaleFacBottomPad*rvar.data_histo.GetXaxis().GetLabelSize())
      rvar.data_histo.GetXaxis().SetTickLength(scaleFacBottomPad*rvar.data_histo.GetXaxis().GetTickLength())
      rvar.data_histo.GetYaxis().SetTitleSize(scaleFacBottomPad*rvar.data_histo.GetYaxis().GetTitleSize())
      rvar.data_histo.GetYaxis().SetLabelSize(.8*scaleFacBottomPad*rvar.data_histo.GetYaxis().GetLabelSize())
      rvar.data_histo.GetYaxis().SetTitle(stack[0].ratioVarName)
      rvar.minimum = stack[0].ratioMin
      rvar.maximum = stack[0].ratioMax
      rvar.data_histo.GetYaxis().SetNdivisions(505)
      rvar.data_histo.GetYaxis().SetTitleOffset(1.25 / scaleFacBottomPad)
      line = ROOT.TPolyLine(2)
      line.SetPoint(0, rvar.data_histo.GetXaxis().GetXmin(), 1.)
      line.SetPoint(1, rvar.data_histo.GetXaxis().GetXmax(), 1.)
      line.SetLineWidth(1)
#      if stack[0].logRatio:
#        rvar.logy=True
#      else:
#        rvar.logy=False
      drawStack([rvar], False)
      stack[0].rvar = rvar
      if stack[0].logRatio:
        bottompad.SetLogy()
      else:
        bottompad.SetLogy(0)
      line.Draw()
      stuff.append(line)
    else:
      drawStack(thesestacks[istack], normalized)
  if filename[-3:]!="png":
    c1.Print(path+filename+".png")
    c1.Print(path+filename+".root")
    c1.Print(path+filename+".pdf")
  else:
    c1.Print(path+filename)
  del c1

class variable2D:
  cutstring=""
  lines=upperrightlines
  sample=""
  binning=[]
  lines = []
  def __init__(self, var1, var2, profile = False):
    self.var1 = copy.deepcopy(var1)
    self.var2 = copy.deepcopy(var2)
    if var1.sample!=var2.sample:
      print "Warning! Overriding var2.sample!!"
    self.sample = var1.sample
    try:
      if type(self.data_histo)==type(ROOT.TH1F()):
        del self.data_histo
    except:
      pass
    self.binning=[]
    self.binning.extend(self.var1.binning)
    self.binning.extend(self.var2.binning)
    self.name = self.var1.name+"_vs_"+self.var2.name
    self.titleaxisstring = self.var1.titleaxisstring.split(";")[1]+";"+self.var2.titleaxisstring.split(";")[1]
    if profile:
      self.data_histo = ROOT.TProfile2D(self.name,self.name+";"+self.titleaxisstring,*self.binning)
    else:
      self.data_histo = ROOT.TH2F(self.name,self.name+";"+self.titleaxisstring,*self.binning)
      self.data_histo.Sumw2()
    self.data_histo.Reset()
    if var1.cutfunc!=var2.cutfunc:
      print "Warning! var2.cutfunc ignored:", var2.name, "taken:",var1.cutfunc,"skipped:",var2.cutfunc
    self.cutfunc=var1.cutfunc
    self.logy=False

def drawExclusionRegions(histo, var1cuts, var2cuts):
  xmin = histo.GetXaxis().GetXmin()
  xmax = histo.GetXaxis().GetXmax()
  ymin = histo.GetYaxis().GetXmin()
  ymax = histo.GetYaxis().GetXmax()
  toDraw = []
  linex1 = ROOT.TPolyLine(2)
  linex1.SetPoint(0, var1cuts[0], ymin)
  linex1.SetPoint(1, var1cuts[0], ymax)
  linex1.SetLineWidth(2)
  toDraw.append([linex1, "l"]) 
  liney1 = ROOT.TPolyLine(2)
  liney1.SetPoint(0, xmin, var2cuts[0] )
  liney1.SetPoint(1, xmax, var2cuts[0] )
  liney1.SetLineWidth(2)
  toDraw.append([liney1, "l"])
  if var1cuts[1]==var1cuts[2] and var2cuts[1]==var2cuts[2]:
    linex2 = ROOT.TPolyLine(2)
    linex2.SetPoint(0, var1cuts[1], ymin)
    linex2.SetPoint(1, var1cuts[1], ymax)
    linex2.SetLineWidth(2)
    toDraw.append([linex2, "l"])
    liney2 = ROOT.TPolyLine(2)
    liney2.SetPoint(0, xmin, var2cuts[1] ) 
    liney2.SetPoint(1, xmax, var2cuts[1] ) 
    liney2.SetLineWidth(2)
    toDraw.append([liney2,"l"])
  if var1cuts[1]==var1cuts[2] and var2cuts[1]!=var2cuts[2]:
    linex2 = ROOT.TPolyLine(2)
    linex2.SetPoint(0, var1cuts[1], ymin)
    linex2.SetPoint(1, var1cuts[1], ymax)
    linex2.SetLineWidth(2)
    toDraw.append([linex2, "l"])
    liney2 = ROOT.TPolyLine(5)
    liney2.SetPoint(0, xmin, var2cuts[1] ) 
    liney2.SetPoint(1, xmax, var2cuts[1] ) 
    liney2.SetPoint(2, xmax, var2cuts[2] ) 
    liney2.SetPoint(3, xmin, var2cuts[2] ) 
    liney2.SetPoint(3, xmin, var2cuts[1] ) 
    liney2.SetLineWidth(1)
    liney2.SetFillStyle(3004)
    liney2.SetFillColor(ROOT.kBlack)
    toDraw.append([liney2, "l"])
    toDraw.append([liney2.Clone(), "f"])
  if var1cuts[1]!=var1cuts[2] and var2cuts[1]==var2cuts[2]:
    linex2 = ROOT.TPolyLine(5)
    linex2.SetPoint(0, var1cuts[1], ymin)
    linex2.SetPoint(1, var1cuts[1], ymax)
    linex2.SetPoint(2, var1cuts[2], ymax)
    linex2.SetPoint(3, var1cuts[2], ymin)
    linex2.SetPoint(4, var1cuts[1], ymin)
    linex2.SetLineWidth(1)
    linex2.SetFillStyle(3004)
    linex2.SetFillColor(ROOT.kBlack)
    toDraw.append([linex2, "l"])
    toDraw.append([linex2.Clone(), "f"])
    liney2 = ROOT.TPolyLine(2)
    liney2.SetPoint(0, xmin, var2cuts[1] ) 
    liney2.SetPoint(1, xmax, var2cuts[1] ) 
    liney2.SetLineWidth(2)
    toDraw.append([liney2, "l"])
  if var1cuts[1]!=var1cuts[2] and var2cuts[1]!=var2cuts[2]:
    line2 = ROOT.TPolyLine(12)
    line2.SetPoint(0, var1cuts[1], ymin)
    line2.SetPoint(1, var1cuts[2], ymin)
    line2.SetPoint(2, var1cuts[2], var2cuts[1])
    line2.SetPoint(3, xmax, var2cuts[1])
    line2.SetPoint(4, xmax, var2cuts[2])
    line2.SetPoint(5, var1cuts[2], var2cuts[2])
    line2.SetPoint(6, var1cuts[2], ymax)
    line2.SetPoint(7, var1cuts[1], ymax)
    line2.SetPoint(8, var1cuts[1], var2cuts[2])
    line2.SetPoint(9, xmin, var2cuts[2])
    line2.SetPoint(10, xmin, var2cuts[1])
    line2.SetPoint(11, var1cuts[1], var2cuts[1])
    line2.SetPoint(12, var1cuts[1], ymin)
    line2.SetLineWidth(1)
    line2.SetFillStyle(3004)
    line2.SetFillColor(ROOT.kBlack)
    toDraw.append([line2, "l"])
    toDraw.append([line2.Clone(), "f"])
  for obj in toDraw:
    obj[0].Draw(obj[1])
    stuff.append(obj[0])

def draw2D(var,filename, logz = True, exclusionsRegions = "None"):
  c1 = ROOT.TCanvas("ROOT.c1","drawHistos",200,10,600,600)
  c1.SetFillColor(0)
  if logz:
    c1.SetLogz()
  else:
    c1.SetLogz(0)
  hcopy = var.data_histo.Clone()
  stuff.append(hcopy)
  hcopy.Draw("COLZ")
  if type(exclusionsRegions) == type([]):
    drawExclusionRegions(hcopy, exclusionsRegions[0], exclusionsRegions[1])
  latex = ROOT.TLatex();
  for line in var.lines:
    if len(line)>3:
      latex.SetTextSize(line[3])
    else:
      latex.SetTextSize(0.04)
    if len(line)>4:
      latex.SetTextAlign(line[4])
    else:
      latex.SetTextSize(11) #align right
    if len(line)>5:
      latex.SetNDC(line[5])
    else:
      latex.SetNDC(True)
    stuff.append(latex.DrawLatex(line[0],line[1],line[2]))
  if filename.count(".")==0:
    c1.Print(defaultWWWPath+filename+".png")
    c1.Print(defaultWWWPath+filename+".eps")
    c1.Print(defaultWWWPath+filename+".root")
    c1.Print(defaultWWWPath+filename+".pdf")
    c1.Print(defaultWWWPath+filename+".C")
  else:
    c1.Print(defaultWWWPath+filename)
  del c1

def setBoolean(stack):
  histo = stack[0].data_histo
  xaxis = histo.GetXaxis()
  #falsebin = histo.FindBin(0)
  #truebin  = histo.FindBin(1)
  #falsebincont = histo.GetBinContent(falsebin)
  #truebincont  = histo.GetBinContent(truebin)
  #print "Bin with 0: ",falsebin," contains: ", falsebincont, " Bin with 1: ", truebin, " contains: ", truebincont
  xaxis.Set(2,-0.5,1.5)
  xaxis.SetNdivisions(002)
  xaxis.SetBinLabel(1,"false")
  xaxis.SetBinLabel(2,"true")
  #histo.SetBinContent(1,falsebincont)
  #histo.SetBinContent(2,truebincont )
  #print "Bin with 0: ",histo.FindBin(0)," contains: ", histo.GetBinContent(1), " Bin with 1: ", histo.FindBin(1), " contains: ", histo.GetBinContent(2)
 
