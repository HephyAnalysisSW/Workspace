import ROOT
from Workspace.HEPHYPythonTools.helpers import scatterOnTH2
ROOT.gROOT.ProcessLine(".L ../../HEPHYPythonTools/scripts/root/useNiceColorPalette.C+")
ROOT.useNiceColorPalette(255)

rand = ROOT.TRandom()
data = [(rand.Gaus(), rand.Gaus(), rand.Gaus()) for i in range(1000)]
data = [(0,0,0.1), (0.5,0.5,0.5), (1,1,1), (1.5,1.5,10) ]

ROOT.gStyle.SetOptStat(0)
h2=ROOT.TH2F('','',100,-2,2,100,-2,2)
scatterOnTH2(data, h2, "/afs/hephy.at/user/s/schoefbeck/www/etc/test.png", markerType=24)
#for d in data:
#  h.Fill(d[0], d[1], 0) 
#c1 = ROOT.TCanvas()
#xmin = h.GetXaxis().GetXmin()
#xmax = h.GetXaxis().GetXmax()
#ymin = h.GetYaxis().GetXmin()
#ymax = h.GetYaxis().GetXmax()
#data.sort(key=lambda x:x[2])
#zvals = [d[2] for d in data] 
#zmin, zmax = min(zvals), max(zvals)
##  h.Reset()
#h.GetZaxis().SetRangeUser(zmin,zmax)
#c1.SetLogz()
#h.Draw("COLZ")
#c1.Update()
#zPaletteAxis=h.GetListOfFunctions().FindObject("palette")
#stuff=[]
##  h.GetListOfFunctions().ls()
#for d in data:
#  if d[0]>xmin and d[0]<xmax and d[1]>ymin and d[1]<ymax:
#    e = ROOT.TMarker(d[0], d[1], 20)
#    e.SetMarkerColor(zPaletteAxis.GetValueColor(d[2])) 
#    stuff.append(e)
#for s in stuff:
#  s.Draw()

