import ROOT

from Workspace.HEPHYPythonTools.helpers import getObjFromFile

ifile = '/afs/hephy.at/user/s/schoefbeck/www/pngT5LNu/T5Lnu_v5_refSelNoNJet_copy__met150_ht400_njets2-99_wPlusGenMass.root'
f = ROOT.TFile(ifile)
k = f.GetListOfKeys()[0].GetName()
f.Close()
canv = getObjFromFile(ifile, k)
h = canv.GetPrimitive('XXX_Data').Clone('hist') 
print h.Integral()
#f = ROOT.TF1('bw', '[0]*x/((x**2-[1]**2)**2+[1]**2*[2]**2)', 50.,400.)
#f.SetParameter(0,10**7)
#f.SetParameter(1,80.4)
#f.SetParameter(2,1.)
#
#c1 = ROOT.TCanvas()
#h.Fit('bw')
#h.Draw()
#c1.SetLogy()
#f.Draw('same')
