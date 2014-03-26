#
# Draw ratios of MET<muPt / MET>muPt from muPtMetIndex*.root files
#   produced with LP_plots.py . Needs synchronisation with the
#   muPt / MET / HT bin definitions in LP_plots!
# Arguments: list of muPtMetIndex* files
#
import ROOT
import sys
from math import sqrt

def getObjectsFromDirectory(dir,type,name=None):
  result = [ ]
  ROOT.gROOT.cd()
  for key in dir.GetListOfKeys():
    obj = key.ReadObj()
    if obj.InheritsFrom(type):
      if name==None or obj.GetName()==name:
        result.append(obj)
  return result

def getObjectsFromCanvas(canvas,type,name=None):
  result = [ ]
  ROOT.gROOT.cd()
  for obj in canvas.GetListOfPrimitives():
    if obj.InheritsFrom(type):
      if name==None or obj.GetName()==name:
        result.append(obj)
  return result


nbht = 3
nbmet = 3
binsToAdd = [ 2, 3, 6 ]

def addBins(histo):
  result = [ [ ],  [ ] ]
  for i in range(2):
    bins = [ ]
    bins.extend(binsToAdd)
    if i==1:
      bins = [ nbmet**2+1-k for k in bins ]
    for j in range(nbht):
      sumc = 0
      sume2 = 0
      for b in bins:
        sumc += histo.GetBinContent(b+nbmet**2*j)
        sume2 += histo.GetBinError(b+nbmet**2*j)**2
      result[i].append( ( sumc, sqrt(sume2) ) )
  return result

ROOT.gStyle.SetOptStat(0)

filesByName = { }
for ff in sys.argv[1:]:
  fields = ff.split("/")
  nf = fields[-1].split(".")[0]
  if not nf in filesByName:
    filesByName[nf] = [ ]
  filesByName[nf].append(ff)

allcnvs = [ ]
allhratios = [ ]
for nf in filesByName:

  col = 1
  hnames = [ ]
  hratios = [ ]
  for ff in filesByName[nf]:

    df = ff.split("/")[0]
    hratioMC = ROOT.TH1F("ratioMC",nf,nbht,-0.5,nbht-0.5)
    hratioMC.SetDirectory(ROOT.gROOT)
    hratioMC.SetLineColor(col)
    hratioMC.SetLineStyle(2)
    hratioMC.SetLineWidth(3)
    hratioMC.SetFillColor(col)
    hratioMC.SetFillStyle(3844)

    hratioData = ROOT.TH1F("ratioData",nf,nbht,-0.5,nbht-0.5)
    hratioData.SetDirectory(ROOT.gROOT)
    hratioData.SetLineColor(col)
    hratioData.SetLineWidth(2)
    hratioData.SetMarkerStyle(20)
    hratioData.SetMarkerColor(col)

    hnames.append(df)
    hratios.append( ( hratioMC, hratioData ) )
    col += 1
    if col==3:
      col += 1

    tf = ROOT.TFile(ff)

    cnvs = getObjectsFromDirectory(tf,ROOT.TCanvas.Class())
    assert len(cnvs)==1

    pads = getObjectsFromCanvas(cnvs[0],ROOT.TVirtualPad.Class(),"p1")
    assert len(pads)==1


    stacks = getObjectsFromCanvas(pads[0],ROOT.THStack.Class())
    assert len(stacks)==1

    data = None
    th1s = getObjectsFromCanvas(pads[0],ROOT.TH1.Class())
    for th1 in th1s:
      if th1.GetMarkerStyle()==20:
        data = th1
        break
    assert data!=None

    resMC = addBins(stacks[0].GetStack().Last())
    resData = addBins(data)


    for ir in range(nbht):
      v = resMC[0][ir][0]/resMC[1][ir][0]
      e = sqrt(resMC[0][ir][1]**2+(resMC[1][ir][1]*v)**2)/resMC[1][ir][0]
      hratioMC.SetBinContent(ir+1,v)
      hratioMC.SetBinError(ir+1,e)
      v = resData[0][ir][0]/resData[1][ir][0]
      e = sqrt(resData[0][ir][1]**2+(resData[1][ir][1]*v)**2)/resData[1][ir][0]
      hratioData.SetBinContent(ir+1,v)
      hratioData.SetBinError(ir+1,e)



  hmin, hmax = None, None
  for hs in hratios:
    for h in hs:
      for i in range(h.GetNbinsX()):
        v = h.GetBinContent(i+1)
        e = h.GetBinError(i+1)
        if hmin==None or (v-e)<hmin:
          hmin = v - e
        if hmax==None or (v+e)>hmax:
          hmax = v + e
  print hmin,hmax
  dh = hmax - hmin
  hmax += 0.05*dh
  hmin -= 0.05*dh

  cnv = ROOT.TCanvas(nf,nf)
  leg = ROOT.TLegend(0.60,0.70,0.90,0.90,"","brNDC")
  leg.SetFillStyle(0)
  leg.SetBorderSize(0)
  opt = "E2"
  for i in range(len(hratios)):
    hn = hnames[i]
    hmc,hd = hratios[i]
    hmc.SetMinimum(hmin)
    hmc.SetMaximum(hmax)
    hmc.Draw(opt)
    hmc2 = hmc.Clone()
    hmc2.SetFillStyle(0)
    hmc2.DrawCopy("hist same")
    if opt.find("same")==-1:
      opt += " same"
    leg.AddEntry(hmc,hn,"l")
  opt = "E1 same"
  for hmc,hd in hratios:
    hd.SetMinimum(hmin)
    hd.SetMaximum(hmax)
    hd.Draw(opt)
  leg.Draw()
  allcnvs.append(leg)

  cnv.Update()
  allcnvs.append(cnv)
  allhratios.extend(hratios)

raw_input("Enter")


