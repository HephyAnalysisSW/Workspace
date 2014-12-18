import ROOT, copy, numbers
import types
from array import array
ROOT.gROOT.LoadMacro("../../HEPHYPythonTools/scripts/root/tdrstyle.C")
#ROOT.gROOT.LoadMacro("../../HEPHYPythonTools/scripts/root/CMS_lumi.C")
ROOT.setTDRStyle()
ROOT.TH1F.SetDefaultSumw2()
#def setupLumiPlotInfo():
#  ROOT.gROOT.ProcessLine('writeExtraText = true;      ') # if extra text
#  ROOT.gROOT.ProcessLine('extraText  = "Preliminary"; ') # default extra text is "Preliminary"
#  ROOT.gROOT.ProcessLine('lumi_8TeV  = "19.1 fb^{-1}";') # default is "19.7 fb^{-1}"
#  ROOT.gROOT.ProcessLine('lumi_7TeV  = "4.9 fb^{-1}"; ') # default is "5.1 fb^{-1}"
#  ROOT.gROOT.ProcessLine('int iPeriod = 3;')
topMargin = 0.07
from Workspace.HEPHYPythonTools.helpers import getFileList, getVarValue

#ROOT_colors = [ROOT.kBlack, ROOT.kRed-7, ROOT.kBlue-2, ROOT.kGreen+3, ROOT.kOrange+1,ROOT.kRed-3, ROOT.kAzure+6, ROOT.kCyan+3, ROOT.kOrange , ROOT.kRed-10]
#upperrightlines=[[0.62,0.7,"#font[22]{CMS preliminary 2012}"],[0.62,0.65,"#sqrt{s} = 8TeV"]]
#upperrightlines2=[[0.62,0.75,"#font[22]{CMS preliminary 2012}"],[0.62,0.7,"#sqrt{s} = 8TeV"]]
#upperleftlines=[[0.2,0.88,"#font[22]{CMS preliminary 2012}"],[0.2,0.83,"#sqrt{s} = 8TeV"]]
#middlerightlines=[[0.62,0.6,"#font[22]{CMS preliminary 2012}"],[0.62,0.55,"#sqrt{s} = 8TeV"]]

class plot:
  def __init__(self, var, binning, cut, sample, style, weight = {'string':'weight'}, options=None):

    self.leaf = var['leaf'] if var.has_key('leaf') else None
    self.func = var['func'] if var.has_key('func') else None
    self.TTreeFormula = var['TTreeFormula'] if var.has_key('TTreeFormula') else None
    self.usedBranches = var['branches'] if var.has_key('branches') else []
    assert sum(bool(x) for x in [self.leaf, self.func, self.TTreeFormula])==1, "Error: Should specify exactly one of 'leaf', 'func' or 'TTreeFormula' in var %s" % repr(var)
    if self.leaf:
      assert type(self.leaf) == types.StringType, "Error: 'leaf' should be StringType in var %s" % repr(var)
      self.title=self.leaf 
    if self.func:
      assert type(self.func) == types.FunctionType, "Error: 'func' should be FunctionType in var %s" % repr(var)
      self.title="Functor_"+self.func.func_name
    if self.TTreeFormula:
      assert type(self.TTreeFormula) == types.StringType, "Error: 'TTreeFormula' should be StringType in var %s" % repr(var)
      self.title="TTreeFormula"
    self.name = "_".join([var['name'], self.title, sample['name']])

    self.ind = var['ind'] if var.has_key('ind') else 0
    assert not (self.ind and not self.leaf) , "Error: Use 'ind' with other than 'leaf' in var: %s" % repr(var)
   
    self.overFlow = var['overFlow'] if var.has_key('overFlow') else None

#    self.additionalCutFunc=additionalCutFunc #Not yet implemented
    self.binning=binning
    self.cut = cut
    self.style=style
    self.sample=sample
    self.weight=weight
    try:
      if type(self.histo)==type(ROOT.TH1F()):
        self.Reset()
        del self.histo
    except:
      pass

    rClass = ROOT.TProfile if options and options.has_key('isProfile') and options['isProfile'] else ROOT.TH1F
    binninArgs = binning['binning'] if not (self.binning.has_key('isExplicit') and self.binning['isExplicit']) else [len(binning['binning']) - 1, array('d',binning['binning'])]
    self.histo = rClass(self.name, self.name, *binninArgs)
    self.histo.Sumw2()
    self.histo.Reset()

  @staticmethod
  def fromHisto(histo,style,options=None):
    p = plot(var=None,binning=None,cut=None,sample=None,style=style,weight=None,options=options)
    p.histo = histo
    return p

class stack:
  def __init__(self, stackLists, options):
    self.stackLists = stackLists
    self.options = options
    self.usedBranches = []
  def __getitem__(self, p):return self.stackLists[p]

def switchOnBranches(c, usedBranches):
      c.SetBranchStatus("*", 0)
#      print usedBranches
      for br in usedBranches:
        if "*" in br:
          c.SetBranchStatus(br, 1)
        else:
          if c.GetBranch(br):
#            print "Turning on branch", b
            c.SetBranchStatus(br, 1)
          else:
            br2 = c.GetAlias(br)
#            print "Not a branch",b,"alias",alias
            if br2:
#              br = c.GetBranch(alias)
              c.SetBranchStatus(br2, 1)
#              print "Turning on branch", br,"(aliased from",b, ")"

def loopAndFill(stacks):
  allSamples=[]
  allSampleNames=[]
  allPlots = []
  usedBranches = []
  for s in stacks:
    usedBranches = list(set(usedBranches+s.usedBranches))
    for l in s.stackLists:
      for p in l:
        allPlots.append(p)
        if p.leaf:
          if not p.leaf in usedBranches:
            usedBranches.append(p.leaf)
          if p.weight  and p.weight.has_key('string') and p.weight['string'] and not p.weight['string'] in usedBranches:
            usedBranches.append(p.weight['string'])
        else:
          usedBranches = list(set(usedBranches+p.usedBranches))
        if not p.sample in allSamples:
          allSamples.append(p.sample)
  
  print "Found",len(allSamples),'different samples:',", ".join(s['name'] for s in allSamples)
  for s in allSamples:
    cutStringForSample=[]
    plotsPerCutForSample={}
    for p in allPlots:
      if p.sample==s:
        if not p.cut['string'] in cutStringForSample:
          cutStringForSample.append(p.cut['string'])
          plotsPerCutForSample[p.cut['string']]=[]
        if not p in plotsPerCutForSample[p.cut['string']]:
          plotsPerCutForSample[p.cut['string']].append(p)
    s['plotsPerCutForSample'] = plotsPerCutForSample
  for s in allSamples:
    sampleScaleFac = 1 if not s.has_key('scale') else s['scale']
    if sampleScaleFac!=1:
      print "Using sampleScaleFac", sampleScaleFac ,"for sample",s["name"]
    for b in s['bins']:
      c = ROOT.TChain('Events')
      counter=0
      dir = s['dirname'] if s.has_key('dirname') else s['dir']
      for f in getFileList(dir+'/'+b, maxN = -1 if not (s.has_key('small') and s['small']) else 1):#, minAgeDPM, histname, xrootPrefix, maxN):
        counter+=1
        c.Add(f)
      ntot = c.GetEntries()
      print "Added ",counter,'files from sample',s['name'],'dir',dir,'bin',b,'ntot',ntot
      switchOnBranches(c, usedBranches)
         
      if ntot==0:
        print "Warning! Found zero events in",s['name'],'bin',b," -> do nothing"
        continue
      for cutString in s['plotsPerCutForSample'].keys():
        plotsToFill = s['plotsPerCutForSample'][cutString]
        c.Draw(">>eList",cutString)
        elist = ROOT.gDirectory.Get("eList")
        number_events = elist.GetN() if not (s.has_key('small')  and s['small']) else min(elist.GetN(), 100)
        print "Reading: ", s["name"], b, "with",number_events,"events passing cutString", cutString, 'and will fill', len([p.name for p in plotsToFill]),'vars.'
        for p in plotsToFill:
          if not (p.cut.has_key('func') and p.cut['func']):
            p.cut['func']=None
          if p.TTreeFormula:
            fString='ROOT.TTreeFormula('+p['name']+','+p.var+',c)'
            exec('p.ttreeFormula='+fString)
            print "Created TTreeFormula:",fString
        for i in range(0, number_events):
          if (i%10000 == 0) and i>0 :
            print i
          c.GetEntry(elist.GetEntry(i))
          for p in plotsToFill:
            if (not p.cut['func']) or p.cut['func'](c):
              weight = c.GetLeaf(p.weight['string']).GetValue()#getVarValue(c, p.weight['string'])
               
              if p.leaf:
                val =  getVarValue(c, p.leaf, p.ind)
#                print "Fill leaf",p.leaf, p.ind, val, weight,sampleScaleFac
              if p.TTreeFormula:
                p.ttreeFormula.UpdateFormulaLeaves()
                val = p.ttreeFormula.EvalInstance()
              if p.func:
                val = p.func(c)
              p.histo.Fill(val, weight*sampleScaleFac)
        del elist
      del c
  for s in stacks:
    sumStackHistos(s)   
#                reweightFac = 1.
#                if type(var.reweightVar) == types.FunctionType:
#                    reweightFac = var.reweightVar(c)
#  #                  print "Using function", var.reweightVar, "->",reweightFac
#                else:
#                  if var.reweightVar!="":
#                    reweightFac = var.reweightHisto.GetBinContent(var.reweightHisto.FindBin(getValue(c, var.reweightVar)))
#  #                  print "reweightVar = ",var.reweightVar, c.GetLeaf(var.reweightVar).GetValue(), "->", reweightFac
#                nvtxWeight=reweightFac*nvtxWeight
#                scaleFac = 1
#                if sample.has_key('scaleFac'):
#                  scaleFac = sample['scaleFac']
#                weight = 1
#                if sample.has_key("hasWeight"):
#                  if sample["hasWeight"]:
#                    weight = getValue(c, sample["weight"])
#                  else:
#                    weight = sample["weight"][bin]
#                else:
#                  weight = sample["weight"][bin]

def sumStackHistos(stack):
  for l in stack.stackLists:
    n = len(l)
    for i in range(n):
      for j in range(i+1,n):
        l[i].histo.Add(l[j].histo)

def drawStack(stk, maskedArea=None):
  print "maskedArea",maskedArea
  stuff=[]
  try:
    l = ROOT.TLegend(*(stk.options['legend']['coordinates']))
    l.SetFillColor(0)
    l.SetShadowColor(ROOT.kWhite)
    l.SetBorderSize(0)
    try:
      l.SetBorderSize(1)
    except:pass
    stuff.append(l)
  except:pass
  first=True
  print stk.options
  try:
    autoAdjustY = stk.options['yRange'][1].lower()=='auto' and isinstance(stk.options['yRange'][0], numbers.Number)
  except:
    autoAdjustY = False
  if autoAdjustY and  stk.options.has_key('logY') and stk.options['logY']:
    ymin = stk.options['yRange'][0]
    logYMaxGlobal = log(ymin,10)
    for s in stk.stackLists:
      for p in s:
        for iBin in range(1, 1 + p.histo.GetNbinsX()):
          xLowAbs, xHighAbs = p.histo.GetbinLowEdge(iBin), p.histo.GetbinLowEdge(iBin)+p.histo.GetbinWidth(iBin)
          xLow = (xLowAbs -  p.histo.GetXaxis().GetXmin())/(p.histo.GetXaxis().GetXmax() - p.histo.GetXaxis().GetXmin())
          xHigh = (xHighAbs -  p.histo.GetXaxis().GetXmin())/(p.histo.GetXaxis().GetXmax() - p.histo.GetXaxis().GetXmin())
          yFracMax =  maskedArea['yLow'] if xHigh>maskedArea['xLow'] and xLow<maskedArea['xHigh'] else 1
          deltaLogY = log(1.5, 10) if yFracMax==1 else log(1.2,10)
          y =  p.histo.GetbinContent(iBin)
          logyMax = (log(y/ymin, 10) + deltaLogY)/yFracMax
          logYMaxGlobal = logyMax if logyMax>logYMaxGlobal else logYMaxGlobal
          print iBin, y, logyMax, logYMaxGlobal
  else:
    logYMaxGlobal=None 
  for s in stk.stackLists:
    for p in s:
      hcopy = p.histo.Clone()
      if p.style.has_key('errorBars') and not p.style['errorBars']:
        for nbin in range(0, hcopy.GetNbinsX()+1):
          hcopy.SetBinError(nbin, 0.)
#      if stk.options.has_key('labels'):
      try:
        hcopy.GetXaxis().SetTitle(stk.options['labels']['x'])
        hcopy.GetYaxis().SetTitle(stk.options['labels']['y'])
      except:pass
      try: hcopy.GetYaxis().SetTitleOffset(stk.options['yTitleOffset'])
      except:pass
      hcopy.SetTitle("")
      if p.style['style'] == "e":
        hcopy.SetMarkerColor(p.style['color'])
        hcopy.SetLineColor(p.style['color'])
#        if p.style.has_key('markerStyle') and p.style['markerStyle']:
        try:
          hcopy.SetMarkerStyle(p.style['markerStyle'])
        except:
          hcopy.SetMarkerStyle(20)
#        if p.style.has_key('markerSize') and p.style['markerSize']:
        try:
          hcopy.SetMarkerSize(p.style['markerSize'])
        except:
          hcopy.SetMarkerSize(1)
      if p.style['style'] == "f":
        hcopy.SetLineColor(ROOT.kBlack)
        hcopy.SetLineStyle(0)
        hcopy.SetLineWidth(0)
        hcopy.SetFillColor(p.style['color'])
        hcopy.SetMarkerColor(ROOT.kBlack)
        hcopy.SetMarkerStyle(0)
      if p.style['style'] == "l" or p.style['style'] == "d":
        hcopy.SetLineColor(p.style['color'])
        hcopy.SetLineWidth(0)
        hcopy.SetMarkerColor(p.style['color'])
        hcopy.SetMarkerStyle(0)
        hcopy.SetMarkerSize(0)
      if p.style['style'] == "l":
        hcopy.SetLineStyle(0)
      if p.style['style'] == "d":
        hcopy.SetLineStyle(2)
#      if p.style.has_key('thickNess') and  p.style['thickNess']:
      try:
        hcopy.SetLineWidth(p.style['lineThickness'])
      except:pass
      stuff.append(hcopy)
      if stk.options.has_key('logY') and stk.options['logY']:
        yHeadRoomFac = 1.5 if not  stk.options.has_key('yHeadRoomFac') else stk.options['yHeadRoomFac']
        defaultYRange = [0.7, yHeadRoomFac*hcopy.GetMaximum()]
      else:
        yHeadRoomFac = 1.2 if not  stk.options.has_key('yHeadRoomFac') else stk.options['yHeadRoomFac']
        defaultYRange = [0, yHeadRoomFac*hcopy.GetMaximum()]
      if stk.options and stk.options.has_key('yRange') and type(stk.options['yRange'])==type([]) and len(stk.options['yRange'])==2:
        stk.options['yRange'][0]=defaultYRange[0] if not isinstance(stk.options['yRange'][0], numbers.Number) else stk.options['yRange'][0]#If yRange is 'None' use default
        stk.options['yRange'][1]=defaultYRange[1] if not isinstance(stk.options['yRange'][1], numbers.Number) else stk.options['yRange'][1]#If yRange is 'None' use default
      hcopy.GetYaxis().SetRangeUser(*defaultYRange)
      if logYMaxGlobal:
        stk.options['yRange'][1]=10**logYMaxGlobal
      try:
        hcopy.GetYaxis().SetRangeUser(*(stk.options['yRange']) )
      except:pass

      
      if first:
        if p.style['style'] == "e":
          hcopy.Draw("e1")
        if p.style['style'] == "f" or p.style['style'] == "l" or p.style['style'] == "d":
          hcopy.Draw("eh1")
        first=False
      else:
        if p.style['style'] == "e":
          hcopy.Draw("e1same")
        if p.style['style'] == "f" or p.style['style'] == "l" or p.style['style'] == "d":
          hcopy.Draw("eh1same")
#      if p.style.has_key('legendText') and stk.options.has_key('legend') and stk.options['legend']:
      try:
        l.AddEntry(hcopy, p.style['legendText'])
      except:pass
  ROOT.gPad.RedrawAxis()
#  if  stk.options.has_key('legend') and stk.options['legend']:
  try:
    l.Draw()
  except:pass
  if stk.options['legend'] and (not (stk.options['legend'].has_key('boxed')) and stk.options['legend']['boxed']):
    ROOT.gPad.RedrawAxis()
  latex = ROOT.TLatex()
  latex.SetNDC()
  latex.SetTextSize(0.04)
  latex.SetTextAlign(11) # align right
#  if stk.options.has_key('texLines') and stk.options['texLines']:
  try:
    for line in stk.options['texLines']:
      latex.SetTextSize(0.04)
      try:#if line.has_key('options'):
#        if line['options'].has_key('textSize'):
          latex.SetTextSize(line['options']['size'])
      except:pass
      stuff.append(latex.DrawLatex(line['pos'][0],line['pos'][1],line['text']))
  except:pass
  return stuff

from localInfo import afsuser
defaultWWWPath = '/afs/hephy.at/user/'+afsuser[0]+'/'+afsuser+'/www/'

def bound01(x):
  return max(0,min(1,x))

def calcTLegendMaskedArea(legendC, margins):
  return {
    'yLow': bound01(1.-(1.-legendC[1] - margins['top'])/(1.-margins['top']-margins['bottom'])),
    'xLow': bound01((legendC[0] - margins['right'])/(1.-margins['right']-margins['left'])),
    'xHigh':bound01((legendC[2] - margins['right'])/(1.-margins['right']-margins['left']))
    }


def drawNMStacks(intn, intm, stacks, filename, path = defaultWWWPath):
  stuff=[]
  yswidth = 500
  ylwidth = 700
  ywidth = yswidth
#  if len(stacks[0][0].dataMCRatio)==2:
#    ywidth = ylwidth
  scaleFacBottomPad = yswidth/float((ylwidth-yswidth))
  yBorder = (ylwidth-yswidth)/float(ylwidth)
  c1 = ROOT.TCanvas("ROOT.c1","drawHistos",200,10,500*intn,ywidth*intm)
  c1.SetFillColor(0)
  if intn!=1 or intm!=1:
    c1.Divide(intn,intm)
  for istack in range(intn*intm):
    stk=None
    if istack<len(stacks):
      stk = stacks[istack]
    else:
      print "Only",len(stacks),"stacks supplied, expected", intn*intm
      continue
    if not stk:
      continue
    if intn*intm!=1:
      thisPad = c1.cd(istack+1)
    else:
      thisPad = c1
#    setupLumiPlotInfo()
#    ROOT.CMS_lumi(thisPad, 3, 22 )

    if stk.options.has_key('ratio') and stk.options['ratio']:
      rops = stk.options['ratio']
      thisPad.Divide(1,2,0,0)
      toppad = thisPad.cd(1)
      if stk.options.has_key('logY'):
        toppad.SetLogy(stk.options['logY'])
      if stk.options.has_key('logX'):
        toppad.SetLogx(stk.options['logX'])
      toppad.SetBottomMargin(0)
      toppad.SetLeftMargin(0.15)
      toppad.SetTopMargin(topMargin)
      toppad.SetRightMargin(0.02)
      toppad.SetPad(toppad.GetX1(), yBorder, toppad.GetX2(), toppad.GetY2())
      stk.options['yTitleOffset'] = 1.

      maskedArea = calcTLegendMaskedArea(stk.options['legend']['coordinates'], margins={'top':topMargin, 'bottom':0.13,'right':0.02,'left':0.15}) if stk.options.has_key('legend') else None
      stuff += drawStack(stk, maskedArea=maskedArea)
      bottompad = thisPad.cd(2)
      bottompad.SetTopMargin(0)
      bottompad.SetRightMargin(0.02)
      bottompad.SetLeftMargin(0.15)
      bottompad.SetBottomMargin(scaleFacBottomPad*0.13)
      bottompad.SetPad(bottompad.GetX1(), bottompad.GetY1(), bottompad.GetX2(), yBorder)
      rp = copy.deepcopy(stk[stk.options['ratio']['numIndex']][0])
#      rp.style['style']=
      rp.histo.Sumw2()
      rp.histo.Divide(stk[stk.options['ratio']['denIndex']][0].histo)
      rp.style['color'] = rops['color']
      rp.histo.GetXaxis().SetTitleSize(scaleFacBottomPad*rp.histo.GetXaxis().GetTitleSize())
      rp.histo.GetXaxis().SetLabelSize(scaleFacBottomPad*rp.histo.GetXaxis().GetLabelSize())
      rp.histo.GetXaxis().SetTickLength(scaleFacBottomPad*rp.histo.GetXaxis().GetTickLength())
      rp.histo.GetYaxis().SetTitleSize(scaleFacBottomPad*rp.histo.GetYaxis().GetTitleSize())
      rp.histo.GetYaxis().SetLabelSize(scaleFacBottomPad*rp.histo.GetYaxis().GetLabelSize())
      rp.histo.GetYaxis().SetNdivisions(505)
#      rp.histo.GetYaxis().SetTitleOffset(1. / scaleFacBottomPad)
#      rp.histo.GetYaxis().SetTitle(stack[0].ratioVarName)
      rs = stack([[rp]], options = {'labels':{'x':stk.options['labels']['x'],'y':rops['yLabel']}, \
                                    'logX':stk.options['logX'], 'logY':rops['logY'], 'legend':None, 
                                    'texLines':None, 'yRange':rops['yRange'] if rops.has_key('yRange') else [0.3,1.7], 'yTitleOffset':1./scaleFacBottomPad}) 
      line = ROOT.TPolyLine(2)
      line.SetPoint(0, rp.histo.GetXaxis().GetXmin(), 1.)
      line.SetPoint(1, rp.histo.GetXaxis().GetXmax(), 1.)
      line.SetLineWidth(1)
      stuff += drawStack(rs)
      line.Draw()
      stuff.append(line)
    else:
      if stk.options.has_key('logY'):
        thisPad.SetLogy(stk.options['logY'])
      if stk.options.has_key('logX'):
        thisPad.SetLogx(stk.options['logX'])
      maskedArea = calcTLegendMaskedArea(stk.options['legend']['coordinates'], margins={'top':topMargin, 'bottom':0.13,'right':0.02,'left':0.15}) if stk.options.has_key('legend') else None
      stuff += drawStack(stk, maskedArea=maskedArea)
  if filename[-4:] not in [".png", ".pdf", "root"]:
    c1.Print(path+filename+".png")
    c1.Print(path+filename+".root")
    c1.Print(path+filename+".pdf")
  else:
    c1.Print(path+filename)
  del c1
  return stuff
#class plot2D:
#  cutstring=""
#  lines=upperrightlines
#  sample=""
#  binning=[]
#  lines = []
#  def __init__(self, var1, var2, profile = False):
#    self.var1 = copy.deepcopy(var1)
#    self.var2 = copy.deepcopy(var2)
#    if var1.sample!=var2.sample:
#      print "Warning! Overriding var2.sample!!"
#    self.sample = var1.sample
#    try:
#      if type(self.histo)==type(ROOT.TH1F()):
#        del self.histo
#    except:
#      pass
#    self.binning=[]
#    self.binning.extend(self.var1.binning)
#    self.binning.extend(self.var2.binning)
#    self.name = self.var1.name+"_vs_"+self.var2.name
#    self.titleaxisstring = self.var1.titleaxisstring.split(";")[1]+";"+self.var2.titleaxisstring.split(";")[1]
#    if profile:
#      self.histo = ROOT.TProfile2D(self.name,self.name+";"+self.titleaxisstring,*self.binning)
#    else:
#      self.histo = ROOT.TH2F(self.name,self.name+";"+self.titleaxisstring,*self.binning)
#      self.histo.Sumw2()
#    self.histo.Reset()
#    if var1.commoncf!=var2.commoncf:
#      print "Warning! var2.commoncf ignored:", var2.name, "taken:",var1.commoncf,"skipped:",var2.commoncf
#    self.commoncf=var1.commoncf
#    self.logy=False


#def draw2D(var,filename, logz = True, exclusionsRegions = "None"):
#  c1 = ROOT.TCanvas("ROOT.c1","drawHistos",200,10,600,600)
#  c1.SetFillColor(0)
#  if logz:
#    c1.SetLogz()
#  else:
#    c1.SetLogz(0)
#  hcopy = var.histo.Clone()
#  stuff.append(hcopy)
#  hcopy.Draw("COLZ")
#  if type(exclusionsRegions) == type([]):
#    drawExclusionRegions(hcopy, exclusionsRegions[0], exclusionsRegions[1])
#  latex = ROOT.TLatex()
#  for line in var.lines:
#    if len(line)>3:
#      latex.SetTextSize(line[3])
#    else:
#      latex.SetTextSize(0.04)
#    if len(line)>4:
#      latex.SetTextAlign(line[4])
#    else:
#      latex.SetTextSize(11) #align right
#    if len(line)>5:
#      latex.SetNDC(line[5])
#    else:
#      latex.SetNDC(True)
#    stuff.append(latex.DrawLatex(line[0],line[1],line[2]))
#  if filename.count(".")==0:
#    c1.Print(defaultWWWPath+filename+".png")
#    c1.Print(defaultWWWPath+filename+".eps")
#    c1.Print(defaultWWWPath+filename+".root")
#    c1.Print(defaultWWWPath+filename+".pdf")
#    c1.Print(defaultWWWPath+filename+".C")
#  else:
#    c1.Print(defaultWWWPath+filename)
#  del c1

#def setBoolean(stack):
#  histo = stack[0].histo
#  xaxis = histo.GetXaxis()
#  #falsebin = histo.FindBin(0)
#  #truebin  = histo.FindBin(1)
#  #falsebincont = histo.GetBinContent(falsebin)
#  #truebincont  = histo.GetBinContent(truebin)
#  #print "Bin with 0: ",falsebin," contains: ", falsebincont, " Bin with 1: ", truebin, " contains: ", truebincont
#  xaxis.Set(2,-0.5,1.5)
#  xaxis.SetNdivisions(002)
#  xaxis.SetBinLabel(1,"false")
#  xaxis.SetBinLabel(2,"true")
#  #histo.SetBinContent(1,falsebincont)
#  #histo.SetBinContent(2,truebincont )
#  #print "Bin with 0: ",histo.FindBin(0)," contains: ", histo.GetBinContent(1), " Bin with 1: ", histo.FindBin(1), " contains: ", histo.GetBinContent(2)
 
