import ROOT
from Workspace.HEPHYPythonTools.helpers import getObjFromFile

ntot=0.

from commons import label, categories, pfTypes
occ={}
en={}
for i in range(100):
  ifile = '/data/schoef/convertedMETTuples_v1/Mu-DYJetsToLL-M50/histo_from'+str(i)+'To'+str(i+1)+'.root'
  c = ROOT.TChain('Events')
  c.Add(ifile)
  n = c.GetEntries()
  ntot+=n

  for t in pfTypes:
    o = getObjFromFile(ifile, 'occ_'+t )
    e = getObjFromFile( ifile, 'en_'+t)
    o.Scale(n)
    e.Scale(n)
    if occ.has_key(t):
      occ[t].Add(o)
      en[t].Add(e)
    else:
      occ[t] = o.Clone()
      en[t] = o.Clone()
    del o
    del e
      
     
for t in pfTypes:
  occ[t].Scale(1./ntot)
  en[t].Scale(1./ntot)
  c1 = ROOT.TCanvas()
  occ[t].Draw('colz')
  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhi/occ_'+t+'.png')
  en[t].Draw('colz')
  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhi/en_'+t+'.png')
