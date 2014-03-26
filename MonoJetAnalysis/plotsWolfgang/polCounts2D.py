#
# Print ratios in two complementary MET<muPt / MET>muPt regions
#   from muPt_vs_met_(Minus|Plus).root files produced with LP_plots.py . 
# Arguments: list of input files
#
import ROOT
import sys
from math import sqrt


def getObjectsFromDirectory(dir,type,name=None):
  result = [ ]
  for key in dir.GetListOfKeys():
    obj = key.ReadObj()
    if obj.InheritsFrom(type):
      if name==None or obj.GetName()==name:
        result.append(obj)
  return result

def getObjectsFromCanvas(canvas,type,name=None):
  result = [ ]
  for obj in canvas.GetListOfPrimitives():
    if obj.InheritsFrom(type):
      if name==None or obj.GetName()==name:
        result.append(obj)
  return result

for nf in sys.argv[1:]:
  tf = ROOT.TFile(nf)

  cnvs = getObjectsFromDirectory(tf,ROOT.TCanvas.Class())
  assert len(cnvs)==1
  cnvs[0].Draw()

  pads = getObjectsFromCanvas(cnvs[0],ROOT.TVirtualPad.Class(),"cnv_1")
  assert len(pads)==1

  th2ds = getObjectsFromCanvas(pads[0],ROOT.TH2.Class())
  assert len(th2ds)==1

  ranges = ( ( 150., 300. ), ( 300., 600.) )

  sums = [ 0., 0. ]
  xaxis = th2ds[0].GetXaxis()
  yaxis = th2ds[0].GetYaxis()
  for ix in range(1,th2ds[0].GetNbinsX()+1):
    x = xaxis.GetBinCenter(ix)
    if x>ranges[0][0] and x<ranges[0][1]:
      isum = 0
    elif x>ranges[1][0] and x<ranges[1][1]:
      isum = 1
    else:
      continue
    for iy in range(1,th2ds[0].GetNbinsY()+1):
      y = yaxis.GetBinCenter(iy)
      if ( isum==1 and y>ranges[0][0] and y<ranges[0][1] ) or \
            ( isum==0 and y>ranges[1][0] and y<ranges[1][1] ):
        sums[isum] += th2ds[0].GetBinContent(ix,iy)

  print nf,sums,sums[1]/sums[0]


