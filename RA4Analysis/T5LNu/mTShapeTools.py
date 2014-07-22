import ROOT
from math import sqrt
from Workspace.HEPHYPythonTools.helpers import getCutPlotFromChain, getCutYieldFromChain, getObjFromFile
from array import array
from helpers import nameAndCut, nameAndCutLShape, wRecoPt

ROOT.TH1F().SetDefaultSumw2()
ROOT.gROOT.ProcessLine(".L ../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()

pdfLength       =  {"cteq":44, "mstw":40, "nnpdf":100}
redFac  =  {"cteq":1.654, "mstw":1., "nnpdf":1.}

targetLumi=19700
defaultLines = [[0.2, 0.9, "#font[22]{CMS Collaboration}"], [0.2,0.85,str(int(round(targetLumi/10.))/100.)+" fb^{-1},  #sqrt{s} = 8 TeV"]]
outDir = "/afs/hephy.at/user/s/schoefbeck/www/pngT5Full/"
binningCoarse = [0,140,200,400,800]
binningFine = range(0,1000,20)
doPDF= False
logy = True


from defaultConvertedTuples import T5Full_1100_200_100, T5Full_1100_800_600 
T5Full_1100_200_100['color'] = ROOT.kBlue + 3
T5Full_1100_800_600['color'] = ROOT.kRed + 3
signals=[T5Full_1100_200_100, T5Full_1100_800_600]

stuff=[]

def getPDFRelUncertaintyPlot(chain, var, binning, cut, weight='weight'):
  res = ROOT.TH1D(var, var, len(binning) - 1, array('d',binning))
  res.Reset()
#  res.SetBins(len(binning) - 1, array('d',binning))
  h2D = {}
  for pdft in ["cteq", "mstw", "nnpdf"]:
    iname = "h_"+pdft+'_var'
#    binning2D = binning+[l[pdft]+1, 0, l[pdft]+1]
#    hPDF = ROOT.TH2D(iname+"_2D", iname+"_2D", *binning2D)
    hPDF = ROOT.TH2D(iname+"_2D", iname+"_2D", len(binning) - 1, array('d',binning),pdfLength[pdft]+1,array('d', range(pdfLength[pdft]+2)))
#    hPDF.SetBins(len(binning) - 1, array('d',binning),l[pdft]+1,array('d', range(l[pdft]+2)))
    chain.Draw('Iteration$:'+var+' >> '+iname+'_2D', pdft+'Weights*weight*('+cut+')', 'goff')
    h = ROOT.gDirectory.Get(iname+"_2D")
    h2D[pdft] = h.Clone() 
    x0 = h.GetBinContent(1,1)
    for by in range(2, h.GetNbinsY() + 1):
      for bx in range(1, h.GetNbinsX() + 1):
        if x0>0:
          h.SetBinContent(bx, by, x0/h.GetBinContent(1, by)*h.GetBinContent(bx, by))
          h.SetBinError(bx, by, x0/h.GetBinContent(1, by)*h.GetBinError(bx, by))
    for bx in range(1, h.GetNbinsX() + 1):
      x0 = h.GetBinContent(h.FindBin(h.GetXaxis().GetBinCenter(bx), 0))
      Delta2XMaxPlus  = 0
      Delta2XMaxMinus = 0
      for iUnc in range(pdfLength[pdft]/2):
        nPlus =  1 + 2*iUnc
        nMinus = 2 + 2*iUnc
        xip = h.GetBinContent(h.FindBin(h.GetXaxis().GetBinCenter(bx), nPlus))
        xim = h.GetBinContent(h.FindBin(h.GetXaxis().GetBinCenter(bx), nMinus))
        Delta2XMaxPlus  += max(xip - x0, xim - x0, 0)**2
        Delta2XMaxMinus += max(x0 - xip, x0 - xim, 0)**2
#        rint "Setting pdft",pdft, bx, x0,nPlus,nMinus,xip,xim,x0, max(xip - x0, xim - x0, 0), max(x0 - xip, x0 - xim, 0), Delta2XMaxPlus, Delta2XMaxMinus
      if x0>0:
        unc = 0.5/redFac[pdft]*(sqrt(Delta2XMaxPlus) + sqrt(Delta2XMaxMinus))/x0
#        print "Setting pdft",pdft, bx, x0,  0.5/redFac[pdft]*(sqrt(Delta2XMaxPlus) + sqrt(Delta2XMaxMinus)), unc 
        if res.GetBinContent(bx)<unc:
#          print "Increasing error to",pdft,unc
          res.SetBinContent(bx, unc)
  return res

def  getJESRelUncertaintyPlot(chains, hRef, var, binning, cut, weight):
  hPlus = getCutPlotFromChain(chains[0], 'mT', binning, cut, weight, binningIsExplicit=True, addOverFlowBin='upper')
  hMinus = getCutPlotFromChain(chains[1], 'mT', binning, cut, weight, binningIsExplicit=True, addOverFlowBin='upper')
  res = hPlus.Clone()
  res.Reset()
  hPlus.Scale(hRef.GetBinContent(1)/hPlus.GetBinContent(1))
  hMinus.Scale(hRef.GetBinContent(1)/hMinus.GetBinContent(1))
  for b in range(1,1+res.GetNbinsX()):
    ref=hRef  .GetBinContent(b)
    p  =hPlus .GetBinContent(b)
    m  =hMinus.GetBinContent(b)
    if ref>0:
      relErr = 1./ref * max(abs(p-ref),abs(m-ref))
    else:
      relErr=0.
#    print b, relErr
    res.SetBinContent(b, relErr)
  del hPlus, hMinus
  return res 

def  getJERRelUncertaintyPlot(chains, var, binning, cut, weight):
  hRef = getCutPlotFromChain(chains[0], 'mT', binning, cut, weight, binningIsExplicit=True, addOverFlowBin='upper')
  hPlus = getCutPlotFromChain(chains[1], 'mT', binning, cut, weight, binningIsExplicit=True, addOverFlowBin='upper')
  hMinus = getCutPlotFromChain(chains[2], 'mT', binning, cut, weight, binningIsExplicit=True, addOverFlowBin='upper')
  res = hPlus.Clone()
  res.Reset()
  hPlus.Scale(hRef.GetBinContent(1)/hPlus.GetBinContent(1))
  hMinus.Scale(hRef.GetBinContent(1)/hMinus.GetBinContent(1))
  for b in range(1,1+res.GetNbinsX()):
    ref=hRef  .GetBinContent(b)
    p  =hPlus .GetBinContent(b)
    m  =hMinus.GetBinContent(b)
    if ref>0:
      relErr = 1./ref * max(abs(p-ref),abs(m-ref))
    else:
      relErr=0.
#    print b, relErr
    res.SetBinContent(b, relErr)
  del hPlus, hMinus, hRef
  return res 

def makeMTPlotWithUncertainties(c,  binning, cut, weight, doPDF = doPDF):
  hMT = getCutPlotFromChain(c, 'mT', binning, cut, weight, binningIsExplicit=True, addOverFlowBin='upper')
  hPDF = None
  if doPDF:
    cPDF = ROOT.TChain('Events')
    cPDF.Add('/data/schoef/convertedTuples_v22/copy/WJetsHT150PDF/histo_WJetsHT150PDF*.root')
    hPDF = getPDFRelUncertaintyPlot(cPDF, 'mT', binning, cut, weight)
    del cPDF
#    hErrPDF = hMT.Clone()
#    for b in range(1,1+hMT.GetNbinsX()):
##      hErrPDF.SetBinContent(b,0)
#      hErrPDF.SetBinContent(b, hPDF.GetBinContent(b)*hMT.GetBinContent(b))

  cJESPlus = ROOT.TChain('Events')
  cJESPlus.Add('/data/schoef/convertedTuples_v22/copy_JESup/WJetsHT150v2/histo_WJetsHT150v2*.root')
  cJESMinus = ROOT.TChain('Events')
  cJESMinus.Add('/data/schoef/convertedTuples_v22/copy_JESdown/WJetsHT150v2/histo_WJetsHT150v2*.root')
  hErrJES = getJESRelUncertaintyPlot([cJESPlus, cJESMinus], hMT, 'mT', binning, cut, weight)
  del cJESPlus, cJESMinus

  cJERCentral = ROOT.TChain('Events')
  cJERCentral.Add('/data/schoef/convertedTuples_v22/copy_JERcentral/WJetsHT150v2/histo_WJetsHT150v2*.root')
  cJERPlus = ROOT.TChain('Events')
  cJERPlus.Add('/data/schoef/convertedTuples_v22/copy_JERup/WJetsHT150v2/histo_WJetsHT150v2*.root')
  cJERMinus = ROOT.TChain('Events')
  cJERMinus.Add('/data/schoef/convertedTuples_v22/copy_JERdown/WJetsHT150v2/histo_WJetsHT150v2*.root')
  hErrJER = getJERRelUncertaintyPlot([cJERCentral, cJERPlus, cJERMinus], 'mT', binning, cut, weight)
  del cJERPlus, cJERMinus, cJERCentral

  return {'hist':hMT, 'unc':{'pdf':hPDF, 'jes':hErrJES, 'jer':hErrJER}}

plots = [\
#  nameAndCut([150,350], [400,750], [2,4], 'pos') +[ True ],
#  nameAndCut([150,350], [400,750], [2,2], 'pos') +[ True ],
#  nameAndCut([150,350], [400,750], [3,3], 'pos') +[ True ],
#  nameAndCut([150,350], [400,750], [4,4], 'pos') +[ True ],
#  nameAndCut([150,350], [400,750], [2,4], 'neg') +[ True ],
#  nameAndCut([150,350], [400,750], [2,2], 'neg') +[ True ],
#  nameAndCut([150,350], [400,750], [3,3], 'neg') +[ True ],
#  nameAndCut([150,350], [400,750], [4,4], 'neg') +[ True ],
#  nameAndCut([150,350], [400,750], [2,4], '')    +[ True ],
#  nameAndCut([150,350], [400,750], [2,2], '')    +[ True ],
#  nameAndCut([150,350], [400,750], [3,3], '')    +[ True ],
#  nameAndCut([150,350], [400,750], [4,4], '')    +[ True ],
#
#  nameAndCut([350,-1], [400,750], [2,4], 'pos') +[ True ],
#  nameAndCut([350,-1], [400,750], [2,2], 'pos') +[ True ],
#  nameAndCut([350,-1], [400,750], [3,3], 'pos') +[ True ],
#  nameAndCut([350,-1], [400,750], [4,4], 'pos') +[ True ],
#  nameAndCut([350,-1], [400,750], [2,4], 'neg') +[ True ],
#  nameAndCut([350,-1], [400,750], [2,2], 'neg') +[ True ],
#  nameAndCut([350,-1], [400,750], [3,3], 'neg') +[ True ],
#  nameAndCut([350,-1], [400,750], [4,4], 'neg') +[ True ],
#  nameAndCut([350,-1], [400,750], [2,4], '')    +[ True ],
#  nameAndCut([350,-1], [400,750], [2,2], '')    +[ True ],
#  nameAndCut([350,-1], [400,750], [3,3], '')    +[ True ],
#  nameAndCut([350,-1], [400,750], [4,4], '')    +[ True ],
#
#  nameAndCut([150,350], [750, -1], [2,4], 'pos') +[ True ],
#  nameAndCut([150,350], [750, -1], [2,2], 'pos') +[ True ],
#  nameAndCut([150,350], [750, -1], [3,3], 'pos') +[ True ],
#  nameAndCut([150,350], [750, -1], [4,4], 'pos') +[ True ],
#  nameAndCut([150,350], [750, -1], [2,4], 'neg') +[ True ],
#  nameAndCut([150,350], [750, -1], [2,2], 'neg') +[ True ],
#  nameAndCut([150,350], [750, -1], [3,3], 'neg') +[ True ],
#  nameAndCut([150,350], [750, -1], [4,4], 'neg') +[ True ],
#  nameAndCut([150,350], [750, -1], [2,4], '')    +[ True ],
#  nameAndCut([150,350], [750, -1], [2,2], '')    +[ True ],
#  nameAndCut([150,350], [750, -1], [3,3], '')    +[ True ],
#  nameAndCut([150,350], [750, -1], [4,4], '')    +[ True ],
#
#  nameAndCut([350, -1], [750, -1], [2,4], 'pos') +[ True ],
#  nameAndCut([350, -1], [750, -1], [2,2], 'pos') +[ True ],
#  nameAndCut([350, -1], [750, -1], [3,3], 'pos') +[ True ],
#  nameAndCut([350, -1], [750, -1], [4,4], 'pos') +[ True ],
#  nameAndCut([350, -1], [750, -1], [2,4], 'neg') +[ True ],
#  nameAndCut([350, -1], [750, -1], [2,2], 'neg') +[ True ],
#  nameAndCut([350, -1], [750, -1], [3,3], 'neg') +[ True ],
#  nameAndCut([350, -1], [750, -1], [4,4], 'neg') +[ True ],
#  nameAndCut([350, -1], [750, -1], [2,4], '')    +[ True ],
#  nameAndCut([350, -1], [750, -1], [2,2], '')    +[ True ],
#  nameAndCut([350, -1], [750, -1], [3,3], '')    +[ True ],
#  nameAndCut([350, -1], [750, -1], [4,4], '')    +[ True ],
#
#  nameAndCut([150,350], [1000, -1], [2,4], 'pos') +[ True ],
#  nameAndCut([150,350], [1000, -1], [2,2], 'pos') +[ True ],
#  nameAndCut([150,350], [1000, -1], [3,3], 'pos') +[ True ],
#  nameAndCut([150,350], [1000, -1], [4,4], 'pos') +[ True ],
#  nameAndCut([150,350], [1000, -1], [2,4], 'neg') +[ True ],
#  nameAndCut([150,350], [1000, -1], [2,2], 'neg') +[ True ],
#  nameAndCut([150,350], [1000, -1], [3,3], 'neg') +[ True ],
#  nameAndCut([150,350], [1000, -1], [4,4], 'neg') +[ True ],
#  nameAndCut([150,350], [1000, -1], [2,4], '')    +[ True ],
#  nameAndCut([150,350], [1000, -1], [2,2], '')    +[ True ],
#  nameAndCut([150,350], [1000, -1], [3,3], '')    +[ True ],
#  nameAndCut([150,350], [1000, -1], [4,4], '')    +[ True ],
#
#  nameAndCut([350, -1], [1000, -1], [2,4], 'pos') +[ True ],
#  nameAndCut([350, -1], [1000, -1], [2,2], 'pos') +[ True ],
#  nameAndCut([350, -1], [1000, -1], [3,3], 'pos') +[ True ],
#  nameAndCut([350, -1], [1000, -1], [4,4], 'pos') +[ True ],
#  nameAndCut([350, -1], [1000, -1], [2,4], 'neg') +[ True ],
#  nameAndCut([350, -1], [1000, -1], [2,2], 'neg') +[ True ],
#  nameAndCut([350, -1], [1000, -1], [3,3], 'neg') +[ True ],
#  nameAndCut([350, -1], [1000, -1], [4,4], 'neg') +[ True ],
#  nameAndCut([350, -1], [1000, -1], [2,4], '')    +[ True ],
#  nameAndCut([350, -1], [1000, -1], [2,2], '')    +[ True ],
#  nameAndCut([350, -1], [1000, -1], [3,3], '')    +[ True ],
#  nameAndCut([350, -1], [1000, -1], [4,4], '')    +[ True ],
#
#  nameAndCut([150,350], [400,750], [5,5], 'pos') +[ True ],
#  nameAndCut([150,350], [400,750], [5],   'pos') +[ True ],
#  nameAndCut([150,350], [400,750], [6],   'pos') +[ True ],
#  nameAndCut([150,350], [400,750], [5,5], 'neg') +[ True ],
#  nameAndCut([150,350], [400,750], [5],   'neg') +[ True ],
#  nameAndCut([150,350], [400,750], [6],   'neg') +[ True ],
#  nameAndCut([150,350], [400,750], [5,5], '')    +[ True ],
#  nameAndCut([150,350], [400,750], [5],   '')    +[ True ],
#  nameAndCut([150,350], [400,750], [6],   '')    +[ True ],
#
#  nameAndCut([350,-1], [400,750], [5,5], 'pos') +[ True ],
#  nameAndCut([350,-1], [400,750], [5],   'pos') +[ True ],
#  nameAndCut([350,-1], [400,750], [6],   'pos') +[ True ],
#  nameAndCut([350,-1], [400,750], [5,5], 'neg') +[ True ],
#  nameAndCut([350,-1], [400,750], [5],   'neg') +[ True ],
#  nameAndCut([350,-1], [400,750], [6],   'neg') +[ True ],
#  nameAndCut([350,-1], [400,750], [5,5], '')    +[ True ],
#  nameAndCut([350,-1], [400,750], [5],   '')    +[ True ],
#  nameAndCut([350,-1], [400,750], [6],   '')    +[ True ],
#
#  nameAndCut([150,350], [750, -1], [5,5], 'pos') +[ True ],
#  nameAndCut([150,350], [750, -1], [5],   'pos') +[ True ],
#  nameAndCut([150,350], [750, -1], [6],   'pos') +[ True ],
#  nameAndCut([150,350], [750, -1], [5,5], 'neg') +[ True ],
#  nameAndCut([150,350], [750, -1], [5],   'neg') +[ True ],
#  nameAndCut([150,350], [750, -1], [6],   'neg') +[ True ],
#  nameAndCut([150,350], [750, -1], [5,5], '')    +[ True ],
#  nameAndCut([150,350], [750, -1], [5],   '')    +[ True ],
#  nameAndCut([150,350], [750, -1], [6],   '')    +[ True ],
#
#  nameAndCut([350, -1], [750, -1], [5,5], 'pos')+[ False ],
#  nameAndCut([350, -1], [750, -1], [5],   'pos')+[ False ],
#  nameAndCut([350, -1], [750, -1], [6],   'pos')+[ False ],
#  nameAndCut([350, -1], [750, -1], [5,5], 'neg')+[ False ],
#  nameAndCut([350, -1], [750, -1], [5],   'neg')+[ False ],
#  nameAndCut([350, -1], [750, -1], [6],   'neg')+[ False ],
#  nameAndCut([350, -1], [750, -1], [5,5], '')   +[ False ],
#  nameAndCut([350, -1], [750, -1], [5],   '')   +[ False ],
#  nameAndCut([350, -1], [750, -1], [6],   '')   +[ False ],
#
#  nameAndCut([150,350], [1000, -1], [5,5], 'pos') +[ True ],
#  nameAndCut([150,350], [1000, -1], [5],   'pos') +[ True ],
#  nameAndCut([150,350], [1000, -1], [6],   'pos') +[ True ],
#  nameAndCut([150,350], [1000, -1], [5,5], 'neg') +[ True ],
#  nameAndCut([150,350], [1000, -1], [5],   'neg') +[ True ],
#  nameAndCut([150,350], [1000, -1], [6],   'neg') +[ True ],
#  nameAndCut([150,350], [1000, -1], [5,5], '')    +[ True ],
#  nameAndCut([150,350], [1000, -1], [5],   '')    +[ True ],
#  nameAndCut([150,350], [1000, -1], [6],   '')    +[ True ],
#
#  nameAndCut([350, -1], [1000, -1], [5,5], 'pos')+[ False ],
#  nameAndCut([350, -1], [1000, -1], [5],   'pos')+[ False ],
#  nameAndCut([350, -1], [1000, -1], [6],   'pos')+[ False ],
#  nameAndCut([350, -1], [1000, -1], [5,5], 'neg')+[ False ],
#  nameAndCut([350, -1], [1000, -1], [5],   'neg')+[ False ],
#  nameAndCut([350, -1], [1000, -1], [6],   'neg')+[ False ],
#  nameAndCut([350, -1], [1000, -1], [5,5], '')   +[ False ],
#  nameAndCut([350, -1], [1000, -1], [5],   '')   +[ False ],
#  nameAndCut([350, -1], [1000, -1], [6],   '')   +[ False ],

  nameAndCutLShape("L0", [2,2], '') + [ True ],
  nameAndCutLShape("L0", [3,3], '') + [ True ],
  nameAndCutLShape("L0", [4,4], '') + [ True ],
  nameAndCutLShape("L0", [2,4], '') + [ True ],
  nameAndCutLShape("L0", [5,5], '') + [ True ],
  nameAndCutLShape("L0", [5], '') + [ True ],
  nameAndCutLShape("L0", [6], '') + [ True ],
  nameAndCutLShape("L1", [2,2], '') + [ True ],
  nameAndCutLShape("L1", [3,3], '') + [ True ],
  nameAndCutLShape("L1", [4,4], '') + [ True ],
  nameAndCutLShape("L1", [2,4], '') + [ True ],
  nameAndCutLShape("L1", [5,5], '') + [ True ],
  nameAndCutLShape("L1", [5], '') + [ True ],
  nameAndCutLShape("L1", [6], '') + [ True ],
  nameAndCutLShape("L2", [2,2], '') + [ True ],
  nameAndCutLShape("L2", [3,3], '') + [ True ],
  nameAndCutLShape("L2", [4,4], '') + [ True ],
  nameAndCutLShape("L2", [2,4], '') + [ True ],
  nameAndCutLShape("L2", [5,5], '') + [ True ],
  nameAndCutLShape("L2", [5], '') + [ True ],
  nameAndCutLShape("L2", [6], '') + [ True ],
  nameAndCutLShape("L3", [2,2], '') + [ True ],
  nameAndCutLShape("L3", [3,3], '') + [ True ],
  nameAndCutLShape("L3", [4,4], '') + [ True ],
  nameAndCutLShape("L3", [2,4], '') + [ True ],
  nameAndCutLShape("L3", [5,5], '') + [ True ],
  nameAndCutLShape("L3", [5], '') + [ True ],
  nameAndCutLShape("L3", [6], '') + [ True ],
  nameAndCutLShape("L4", [2,2], '') + [ True ],
  nameAndCutLShape("L4", [3,3], '') + [ True ],
  nameAndCutLShape("L4", [4,4], '') + [ True ],
  nameAndCutLShape("L4", [2,4], '') + [ True ],
  nameAndCutLShape("L4", [5,5], '') + [ True ],
  nameAndCutLShape("L4", [5], '') + [ True ],
  nameAndCutLShape("L4", [6], '') + [ True ],
 
  nameAndCutLShape("L0", [2,2], 'pos') + [ True ],
  nameAndCutLShape("L0", [3,3], 'pos') + [ True ],
  nameAndCutLShape("L0", [4,4], 'pos') + [ True ],
  nameAndCutLShape("L0", [2,4], 'pos') + [ True ],
  nameAndCutLShape("L0", [5,5], 'pos') + [ True ],
  nameAndCutLShape("L0", [5], 'pos') + [ True ],
  nameAndCutLShape("L0", [6], 'pos') + [ True ],
  nameAndCutLShape("L1", [2,2], 'pos') + [ True ],
  nameAndCutLShape("L1", [3,3], 'pos') + [ True ],
  nameAndCutLShape("L1", [4,4], 'pos') + [ True ],
  nameAndCutLShape("L1", [2,4], 'pos') + [ True ],
  nameAndCutLShape("L1", [5,5], 'pos') + [ True ],
  nameAndCutLShape("L1", [5], 'pos') + [ True ],
  nameAndCutLShape("L1", [6], 'pos') + [ True ],
  nameAndCutLShape("L2", [2,2], 'pos') + [ True ],
  nameAndCutLShape("L2", [3,3], 'pos') + [ True ],
  nameAndCutLShape("L2", [4,4], 'pos') + [ True ],
  nameAndCutLShape("L2", [2,4], 'pos') + [ True ],
  nameAndCutLShape("L2", [5,5], 'pos') + [ True ],
  nameAndCutLShape("L2", [5], 'pos') + [ True ],
  nameAndCutLShape("L2", [6], 'pos') + [ True ],
  nameAndCutLShape("L3", [2,2], 'pos') + [ True ],
  nameAndCutLShape("L3", [3,3], 'pos') + [ True ],
  nameAndCutLShape("L3", [4,4], 'pos') + [ True ],
  nameAndCutLShape("L3", [2,4], 'pos') + [ True ],
  nameAndCutLShape("L3", [5,5], 'pos') + [ True ],
  nameAndCutLShape("L3", [5], 'pos') + [ True ],
  nameAndCutLShape("L3", [6], 'pos') + [ True ],
  nameAndCutLShape("L4", [2,2], 'pos') + [ True ],
  nameAndCutLShape("L4", [3,3], 'pos') + [ True ],
  nameAndCutLShape("L4", [4,4], 'pos') + [ True ],
  nameAndCutLShape("L4", [2,4], 'pos') + [ True ],
  nameAndCutLShape("L4", [5,5], 'pos') + [ True ],
  nameAndCutLShape("L4", [5], 'pos') + [ True ],
  nameAndCutLShape("L4", [6], 'pos') + [ True ],
  nameAndCutLShape("L0", [2,2], 'neg') + [ True ],
  nameAndCutLShape("L0", [3,3], 'neg') + [ True ],
  nameAndCutLShape("L0", [4,4], 'neg') + [ True ],
  nameAndCutLShape("L0", [2,4], 'neg') + [ True ],
  nameAndCutLShape("L0", [5,5], 'neg') + [ True ],
  nameAndCutLShape("L0", [5], 'neg') + [ True ],
  nameAndCutLShape("L0", [6], 'neg') + [ True ],
  nameAndCutLShape("L1", [2,2], 'neg') + [ True ],
  nameAndCutLShape("L1", [3,3], 'neg') + [ True ],
  nameAndCutLShape("L1", [4,4], 'neg') + [ True ],
  nameAndCutLShape("L1", [2,4], 'neg') + [ True ],
  nameAndCutLShape("L1", [5,5], 'neg') + [ True ],
  nameAndCutLShape("L1", [5], 'neg') + [ True ],
  nameAndCutLShape("L1", [6], 'neg') + [ True ],
  nameAndCutLShape("L2", [2,2], 'neg') + [ True ],
  nameAndCutLShape("L2", [3,3], 'neg') + [ True ],
  nameAndCutLShape("L2", [4,4], 'neg') + [ True ],
  nameAndCutLShape("L2", [2,4], 'neg') + [ True ],
  nameAndCutLShape("L2", [5,5], 'neg') + [ True ],
  nameAndCutLShape("L2", [5], 'neg') + [ True ],
  nameAndCutLShape("L2", [6], 'neg') + [ True ],
  nameAndCutLShape("L3", [2,2], 'neg') + [ True ],
  nameAndCutLShape("L3", [3,3], 'neg') + [ True ],
  nameAndCutLShape("L3", [4,4], 'neg') + [ True ],
  nameAndCutLShape("L3", [2,4], 'neg') + [ True ],
  nameAndCutLShape("L3", [5,5], 'neg') + [ True ],
  nameAndCutLShape("L3", [5], 'neg') + [ True ],
  nameAndCutLShape("L3", [6], 'neg') + [ True ],
  nameAndCutLShape("L4", [2,2], 'neg') + [ True ],
  nameAndCutLShape("L4", [3,3], 'neg') + [ True ],
  nameAndCutLShape("L4", [4,4], 'neg') + [ True ],
  nameAndCutLShape("L4", [2,4], 'neg') + [ True ],
  nameAndCutLShape("L4", [5,5], 'neg') + [ True ],
  nameAndCutLShape("L4", [5], 'neg') + [ True ],
  nameAndCutLShape("L4", [6], 'neg') + [ True ],
  ]

cAllMC = ROOT.TChain('Events')
cWJets = ROOT.TChain('Events')
cWJets.Add('/data/schoef/convertedTuples_v22/copy/WJetsHT150v2/histo_WJetsHT150v2*.root')
cAllMC.Add('/data/schoef/convertedTuples_v22/copy/WJetsHT150v2/histo_WJetsHT150v2*.root')

cRest = ROOT.TChain('Events')
for s in['WW','ZZ','WZ','TTJetsPowHeg','singleTop','DY','QCD20to600','QCD600to1000','QCD1000']:
  cRest.Add('/data/schoef/convertedTuples_v22/copy/'+s+'/histo_'+s+'*.root')
  cAllMC.Add('/data/schoef/convertedTuples_v22/copy/'+s+'/histo_'+s+'*.root')

cData = ROOT.TChain('Events')
cData.Add('/data/schoef/convertedTuples_v22/copy/data/histo_data*.root')

for postFix, binning in [['_binningCoarse', binningCoarse], ['_binningFine', binningFine] ]:
  for plotName, cut, addData in plots:
    print "At", plotName, cut,'addData', addData
    mTRes = makeMTPlotWithUncertainties(cWJets, binning, cut, 'weight', doPDF = doPDF)
    hRest = getCutPlotFromChain(cRest, 'mT', binning, cut, 'weight', binningIsExplicit=True, addOverFlowBin='upper')
    mTRes['hist'].Add(hRest)
    if addData:
      hData = getCutPlotFromChain(cData, 'mT', binning, cut, 'weight', binningIsExplicit=True, addOverFlowBin='upper')
      scaleF = hData.GetBinContent(1)/mTRes['hist'].GetBinContent(1)
      mTRes['hist'].Scale(scaleF)
      hRest.Scale(scaleF)
      for k in mTRes['unc'].keys():
        if mTRes['unc'][k]:
          mTRes['unc'][k].Scale(scaleF)
    topPadDrawObjs=[]
    bottomPadDrawObjs=[]
    for b in range(1, 1+mTRes['hist'].GetNbinsX()):
      binWidth = mTRes['hist'].GetBinWidth(b)
      xLow = mTRes['hist'].GetBinLowEdge(b)
      xHigh = xLow + binWidth 
      central = mTRes['hist'].GetBinContent(b)
      errRelSys=0
      for k in mTRes['unc'].keys():
        if mTRes['unc'][k]:
          errRelSys += mTRes['unc'][k].GetBinContent(b)**2
          print b,'mT in', mTRes['unc'][k].GetBinLowEdge(b),mTRes['unc'][k].GetBinLowEdge(b)+mTRes['unc'][k].GetBinWidth(b),k,mTRes['unc'][k].GetBinContent(b)
      errSys = sqrt(errRelSys)*central
    #  statErr = 0.
      totErr = sqrt(mTRes['hist'].GetBinError(b)**2 + errSys**2)
      boxS = ROOT.TBox(xLow,central-errSys,xHigh,central+errSys)
      boxS.SetFillStyle(3004)
      boxS.SetFillColor(ROOT.kRed)
      boxTot = ROOT.TBox(xLow,central-totErr,xHigh,central+totErr)
      boxTot.SetFillStyle(3004)
      boxTot.SetFillColor(ROOT.kBlue)
      topPadDrawObjs.append(boxTot)
      topPadDrawObjs.append(boxS)
      if central>0:
        boxS = ROOT.TBox(xLow,1.-errSys/central,xHigh,1+errSys/central)
        boxS.SetFillStyle(3004)
        boxS.SetFillColor(ROOT.kRed)
        boxTot = ROOT.TBox(xLow,1-totErr/central,xHigh,1+totErr/central)
        boxTot.SetFillStyle(3004)
        boxTot.SetFillColor(ROOT.kBlue)
        bottomPadDrawObjs.append(boxTot)
        bottomPadDrawObjs.append(boxS)

    hf1 = ROOT.TH1F()
    hf1.SetFillStyle(3004)
    hf1.SetFillColor(ROOT.kBlue)
    hf1.SetLineStyle(4000)
    hf1.SetLineWidth(0)
    hf1.SetMarkerStyle(0)
    hf1.SetLineColor(ROOT.kBlack)
    hf1.SetMarkerColor(ROOT.kBlack)
    hf2 = ROOT.TH1F()
    hf2.SetFillStyle(3004)
    hf2.SetFillColor(ROOT.kRed)
    hf2.SetLineStyle(4000)
    hf2.SetLineWidth(0)
    hf2.SetMarkerStyle(0)
    mTRes['hist'].SetMarkerSize(0)
    mTRes['hist'].SetMarkerColor(ROOT.kBlack)
    mTRes['hist'].SetMarkerStyle(0)
    mTRes['hist'].SetLineColor(ROOT.kBlack)
    mTRes['hist'].SetLineStyle(0)
    mTRes['hist'].SetLineWidth(2)
    hRest.SetMarkerSize(0)
    hRest.SetMarkerColor(ROOT.kBlack)
    hRest.SetMarkerStyle(0)
    hRest.SetLineColor(ROOT.kBlack)
    hRest.SetLineStyle(2)
    if addData:
      hData.GetYaxis().SetTitle("Number of Events / GeV")
      hData.GetXaxis().SetTitle("m_{T} (GeV)")
      minMax = [10**-1.2, 10**1*hData.GetBinContent(hData.GetMaximumBin())]
    else:
      mTRes['hist'].GetYaxis().SetTitle("Number of Events / GeV")
      mTRes['hist'].GetXaxis().SetTitle("m_{T} (GeV)")
      minMax = [10**-1.2, 10**1*mTRes['hist'].GetBinContent(mTRes['hist'].GetMaximumBin())]
    
    l = ROOT.TLegend(0.55,0.5,.95,.95)
    l.SetFillColor(0)
    l.SetShadowColor(ROOT.kWhite)
    l.SetBorderSize(1)
    if addData:
      l.AddEntry(hData, "Data")
    l.AddEntry(mTRes['hist'], "Prediction")
    l.AddEntry(hf1, "total uncertainty")
    l.AddEntry(hf2, "sys. uncertainty")
    l.AddEntry(hRest, 'Non-W MC')

    yswidth = 500
    ylwidth = 700
    ywidth = yswidth
    if addData:
      ywidth = ylwidth
    scaleFacBottomPad = yswidth/float((ylwidth-yswidth))
    yBorder = (ylwidth-yswidth)/float(ylwidth)

    c1 = ROOT.TCanvas("ROOT.c1","drawHistos",200,10,500,ylwidth)
    if addData:
      c1.Divide(1,2,0,0)
      topPad    = c1.cd(1)
      bottomPad = c1.cd(2)
    else:
      topPad = c1

    topPad.SetTopMargin(0.05)
    topPad.SetRightMargin(0.04)
    topPad.SetPad(topPad.GetX1(), yBorder, topPad.GetX2(), topPad.GetY2())
    if addData:
      topPad.SetBottomMargin(0)
      bottomPad.SetTopMargin(0)
      bottomPad.SetRightMargin(0.04)
      bottomPad.SetBottomMargin(scaleFacBottomPad*0.13)
      bottomPad.SetPad(bottomPad.GetX1(), bottomPad.GetY1(), bottomPad.GetX2(), yBorder)

    topPad.cd()
    topPad.SetLogy()
    if addData:
      hData.Draw("e1")
      hData.GetYaxis().SetRangeUser(*minMax)
      hData.Draw("e1")
    else:
      mTRes['hist'].Draw("hist")
      mTRes['hist'].GetYaxis().SetRangeUser(*minMax)
      mTRes['hist'].Draw("hist")

    for o in topPadDrawObjs:
      if o.GetY1()<minMax[0]:
        o.SetY1(minMax[0])
      if o.GetY2()>minMax[0]:
        o.Draw()
    mTRes['hist'].Draw("histsame")
    hRest.Draw("histsame")

    l.Draw()
    latex = ROOT.TLatex();
    latex.SetNDC();
    latex.SetTextSize(0.04);
    latex.SetTextAlign(11); # align right
    for line in defaultLines:
      latex.DrawLatex(line[0],line[1],line[2])
    if addData:
      hData.Draw("e1same")

    for s in signals:
      cS = ROOT.TChain('Events')
      cS.Add(s['dirname']+'/'+s['name']+'/h*.root')
      hcS = getCutPlotFromChain(cS, 'mT', binning, cut, 'weight', binningIsExplicit=True, addOverFlowBin='upper')
#      print 'signalInt',hcS.Integral()
      hcS.SetLineColor(s['color'])
      hcS.SetMarkerSize(0)
      hcS.SetMarkerColor(s['color'])
      hcS.SetMarkerStyle(0)
#      hcS.SetLineStyle(2)
      l.AddEntry(hcS, s['name'])
      hcS.Draw('histSame')
      stuff.append(hcS)
      del cS

    if addData:
      bottomPad.cd()
      bottomPad.SetLogy(0)
      ratioHist = hData.Clone() 
      ratioHist.Sumw2()
      minMaxBottom = (0.2, 1.7)
      ratioHist.GetYaxis().SetRangeUser(*minMaxBottom)
      ratioHist.Divide(mTRes['hist'])
      ratioHist.SetMarkerSize(hData.GetMarkerSize())
      ratioHist.SetMarkerStyle(hData.GetMarkerStyle())
      ratioHist.SetLineColor(hData.GetLineColor())
      ratioHist.GetXaxis().SetTitleSize(scaleFacBottomPad*hData.GetXaxis().GetTitleSize())
      ratioHist.GetXaxis().SetLabelSize(scaleFacBottomPad*hData.GetXaxis().GetLabelSize())
      ratioHist.GetXaxis().SetTickLength(scaleFacBottomPad*hData.GetXaxis().GetTickLength())
      ratioHist.GetYaxis().SetTitleSize(scaleFacBottomPad*hData.GetYaxis().GetTitleSize())
      ratioHist.GetYaxis().SetLabelSize(.8*scaleFacBottomPad*hData.GetYaxis().GetLabelSize())
      ratioHist.GetYaxis().SetTitle('Data / MC')
      ratioHist.GetYaxis().SetNdivisions(505)
      ratioHist.GetYaxis().SetTitleOffset(1.25 / scaleFacBottomPad)
      line = ROOT.TPolyLine(2)
      line.SetPoint(0, ratioHist.GetXaxis().GetXmin(), 1.)
      line.SetPoint(1, ratioHist.GetXaxis().GetXmax(), 1.)
      line.SetLineWidth(2)

      ratioHist.Draw('e1')
      line.Draw()
      for o in bottomPadDrawObjs:
        if o.GetY1()<minMaxBottom[0]:
          o.SetY1(minMaxBottom[0])
        if o.GetY2()>minMaxBottom[1]:
          o.SetY2(minMaxBottom[1])
        if o.GetY2()>minMaxBottom[0] and o.GetY1()<minMaxBottom[1]:
          o.Draw()
    prefix=""
    if not doPDF:
      prefix = "noPDF_"
    c1.Print(outDir+"/"+prefix+plotName+postFix+".png")
    c1.Print(outDir+"/"+prefix+plotName+postFix+".pdf")
    c1.Print(outDir+"/"+prefix+plotName+postFix+".root")

#mTBins = [ (binningCoarse[i], binningCoarse[i+1]) for i in range(len(binningCoarse)-2)]+[(binningCoarse[-2],-1)]
#
#def getPrediction(metb, htb, njetCR, njetSR, leptonPdg, btagRequirement='def', useData = False):
#  if useData:
#    cDataAnalysis = cData
#  else:
#    cDataAnalysis = cAllMC
#
#  nameCR, cutCR = nameAndCut(metb, htb, njetCR, leptonPdg, btagRequirement=btagRequirement)
#  nameSR, cutSR = nameAndCut(metb, htb, njetSR, leptonPdg, btagRequirement=btagRequirement)
#  namePostFix='_to_njet'+str(njetSR[0])
#  if len(njetSR)>1 and njetSR[1]>0:
#    namePostFix+='-'+str(njetSR[1])
##  genPtRWHisto = getObjFromFile('/data/schoef/results2014/T5Lnu_v5_refSelNoNJet_copy_reweightingHistos.root', 'recoPt_'+nameCR+namePostFix)
#
#  crYieldWMC = {}
#  crYieldRestMC = {}
#  crYieldData = {}
#  srYieldWMC = {}
#  srYieldRestMC = {}
#  srYieldData = {}
#  for mtb in mTBins:
#    print "At", mtb, 'SR:', cutSR, 'CR:',cutCR
#    mTCut = 'mT>'+str(mtb[0])
#    if mtb[1]>0:
#      mTCut+='&&mT<='+str(mtb[1])
#    mTCutCR = mTCut+'&&'+cutCR
#    mTCutSR = mTCut+'&&'+cutSR
#    crYWMC, crYWMCVar = getCutYieldFromChain(cWJets, mTCutCR, cutFunc=None, weight='weight', returnVar=True)
#    crYieldWMC[mtb] =  {#'recoPtRW':getCutYieldFromChain(cWJets, mTCutCR, cutFunc=None, weight='weight',weightFunc=lambda c:genPtRWHisto.GetBinContent(genPtRWHisto.FindBin(wRecoPt(c)))),
#                        'nominal': crYWMC, 'nominalVar':crYWMCVar}
#    crYRestMC, crYRestMCVar = getCutYieldFromChain(cRest, mTCutCR, cutFunc=None, weight='weight', returnVar=True)
#    crYieldRestMC[mtb] =  {#'recoPtRW':getCutYieldFromChain(cRest, mTCutCR, cutFunc=None, weight='weight',weightFunc=lambda c:genPtRWHisto.GetBinContent(genPtRWHisto.FindBin(wRecoPt(c)))),
#                           'nominal': crYRestMC, 'nominalVar':crYRestMCVar}
#    crYData, crYDataVar = getCutYieldFromChain(cDataAnalysis, mTCutCR, cutFunc=None, weight='weight', returnVar=True) 
#    crYieldData[mtb] =  {#'recoPtRW':getCutYieldFromChain(cDataAnalysis, mTCutCR, cutFunc=None, weight='weight',weightFunc=lambda c:genPtRWHisto.GetBinContent(genPtRWHisto.FindBin(wRecoPt(c)))),
#                         'nominal': crYData, 'nominalVar': crYDataVar}
#    srYWMC, srYWMCVar = getCutYieldFromChain(cWJets, mTCutSR, cutFunc=None, weight='weight', returnVar=True)
#    srYieldWMC[mtb] =  {#'recoPtRW':getCutYieldFromChain(cWJets, mTCutSR, cutFunc=None, weight='weight',weightFunc=lambda c:genPtRWHisto.GetBinContent(genPtRWHisto.FindBin(wRecoPt(c)))),
#                        'nominal': srYWMC, 'nominalVar':srYWMCVar}
#    srYRestMC, srYRestMCVar = getCutYieldFromChain(cRest, mTCutSR, cutFunc=None, weight='weight', returnVar=True)
#    srYieldRestMC[mtb] =  {#'recoPtRW':getCutYieldFromChain(cRest, mTCutSR, cutFunc=None, weight='weight',weightFunc=lambda c:genPtRWHisto.GetBinContent(genPtRWHisto.FindBin(wRecoPt(c)))),
#                           'nominal': srYRestMC, 'nominalVar':srYRestMCVar}
#    srYData, srYDataVar = getCutYieldFromChain(cDataAnalysis, mTCutSR, cutFunc=None, weight='weight', returnVar=True)
#    srYieldData[mtb] =  {#'recoPtRW':getCutYieldFromChain(cDataAnalysis, mTCutCR, cutFunc=None, weight='weight',weightFunc=lambda c:genPtRWHisto.GetBinContent(genPtRWHisto.FindBin(wRecoPt(c)))),
#                         'nominal': srYData, 'nominalVar':srYDataVar}
#
#  cutNorm = 'mT>'+str(mTBins[0][0])+'&&mT<='+str(mTBins[0][1])+'&&'+cutSR
#
#  normYWMC, normYWMCVar = getCutYieldFromChain(cWJets, cutNorm, cutFunc=None, weight='weight', returnVar=True)
#  normYieldWMC = {#'recoPtRW':getCutYieldFromChain(cWJets, cutNorm, cutFunc=None, weight='weight',weightFunc=lambda c:genPtRWHisto.GetBinContent(genPtRWHisto.FindBin(wRecoPt(c)))),
#                  'nominal': normYWMC, 'nominalVar':normYWMCVar}
#  normYRestMC, normYRestMCVar = getCutYieldFromChain(cRest, cutNorm, cutFunc=None, weight='weight', returnVar=True)
#  normYieldRestMC = {#'recoPtRW':getCutYieldFromChain(cRest, cutNorm, cutFunc=None, weight='weight',weightFunc=lambda c:genPtRWHisto.GetBinContent(genPtRWHisto.FindBin(wRecoPt(c)))),
#                     'nominal': normYRestMC, 'nominalVar':normYRestMCVar}
#  normYData, normYDataVar = getCutYieldFromChain(cDataAnalysis, cutNorm, cutFunc=None, weight='weight', returnVar=True) 
#  normYieldData = {#'recoPtRW':getCutYieldFromChain(cDataAnalysis, cutNorm, cutFunc=None, weight='weight',weightFunc=lambda c:genPtRWHisto.GetBinContent(genPtRWHisto.FindBin(wRecoPt(c)))),
#                   'nominal': normYData, 'nominalVar':normYDataVar}
#
#  hPred = ROOT.TH1D('pred', 'pred', len(binningCoarse) - 1, array('d',binningCoarse))
#  hPred.Reset()
#  for mtb in mTBins[1:]:
#    wMCSR = srYieldWMC[mtb]['nominal']*(normYieldData['nominal'] - normYieldRestMC['nominal']) / normYieldWMC['nominal']
#    wMCSRVar = wMCSR**2*(srYieldWMC[mtb]['nominalVar']/srYieldWMC[mtb]['nominal']**2 \
#                      + (normYieldData['nominalVar'] + normYieldRestMC['nominalVar'])/(normYieldData['nominalVar'] - normYieldRestMC['nominalVar'])**2 + 
#                      +normYieldWMC['nominalVar']/normYieldWMC['nominal']**2)
##    print 'wMCSR',wMCSR, '+/-',sqrt(wMCSRVar)
#    wMCCR = crYieldWMC[mtb]['nominal']*(crYieldData[mTBins[0]]['nominal'] - crYieldRestMC[mTBins[0]]['nominal']) / crYieldWMC[mTBins[0]]['nominal']
#    wMCCRVar = wMCCR**2*(crYieldWMC[mtb]['nominalVar']/crYieldWMC[mtb]['nominal']**2 \
#                      + (crYieldData[mTBins[0]]['nominalVar'] + crYieldRestMC[mTBins[0]]['nominalVar'])/(crYieldData[mTBins[0]]['nominal'] - crYieldRestMC[mTBins[0]]['nominal'])**2 + 
#                      +crYieldWMC[mTBins[0]]['nominalVar']/crYieldWMC[mTBins[0]]['nominal']**2)
##    print 'wMCCR',wMCCR, '+/-',sqrt(wMCCRVar)
#    predictedW = (crYieldData[mtb]['nominal'] - crYieldRestMC[mtb]['nominal']) * wMCSR/wMCCR
##    print mtb, crYieldData[mtb]['nominal'],'+/-', sqrt(crYieldData[mtb]['nominalVar']), crYieldRestMC[mtb]['nominal'],sqrt(crYieldRestMC[mtb]['nominalVar'])
##    print mtb, crYieldData[mtb]['nominal']-crYieldRestMC[mtb]['nominal'],'+/-', sqrt(crYieldData[mtb]['nominalVar']+crYieldRestMC[mtb]['nominalVar'])
#    predictedWVar = predictedW**2*((crYieldData[mtb]['nominalVar'] + crYieldRestMC[mtb]['nominalVar'])/(crYieldData[mtb]['nominal'] - crYieldRestMC[mtb]['nominal'])**2 \
#                      + wMCSRVar/wMCSR**2 + wMCCRVar/wMCCR**2)
#    predictedWRelErr = sqrt((crYieldData[mtb]['nominalVar'] + crYieldRestMC[mtb]['nominalVar'])/(crYieldData[mtb]['nominal'] - crYieldRestMC[mtb]['nominal'])**2 \
#                      + wMCSRVar/wMCSR**2 + wMCCRVar/wMCCR**2)
#    hPred.SetBinContent(hPred.FindBin(mtb[0]), predictedW)
#    hPred.SetBinError  (hPred.FindBin(mtb[0]), sqrt(predictedWVar))
#    print predictedW,'+/-',sqrt(predictedWVar), srYieldRestMC[mtb]['nominal'],"+/-",sqrt(srYieldRestMC[mtb]['nominalVar']), srYieldData[mtb]['nominal']
#    print "Tot.:", predictedW + srYieldRestMC[mtb]['nominal'] ,'+/-',sqrt(predictedWVar+srYieldRestMC[mtb]['nominalVar']),  srYieldData[mtb]['nominal']
#
#  return hPred
#
#btagRequirement = 'noloose'
##btagRequirement = 'def'
##metb = [150, 350]
#metb = [350, -1]
#htb  = [400, 750]
##htb  = [750, -1]
##njetCR = [2,3]
##njetSR = [4, 4]
#useData = True
#for njetCR in [[2,3]]:
##  for njetSR in [[4,4], [4,-1], [5,-1]]:
#  for njetSR in [[4,4]]:
##    for lpdg in ['pos','neg','']:
#    for lpdg in ['pos','neg']:
#      print "\nMET/HT",metb,htb,"Estimating from njet ",njetCR,'to',njetSR,'for pdg',lpdg
#      getPrediction(metb, htb, njetCR, njetSR, lpdg, useData = useData, btagRequirement=btagRequirement)
