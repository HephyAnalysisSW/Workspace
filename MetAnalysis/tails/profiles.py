import ROOT
from math import *
from Workspace.HEPHYPythonTools.helpers import getObjFromFile
ecalveto = getObjFromFile("ecalveto.root", "ecalveto")

c = ROOT.TChain("Events")
c.Add('/data/schoef/monoJetTuples_v8/copyMu/data/histo_data_from*.root')

#for ratio in ['Phef', 'Chef', 'Nhef','Ceef', 'Neef', 'Muef', 'Elef', 'Unc']:
#  profile = ROOT.TProfile2D(ratio.lower(),ratio.lower(),120,-3,3,120,-pi,pi)
#  c.Draw('jet'+ratio+':jetPhi:jetEta>>'+ratio.lower(),'')
#  c1 = ROOT.TCanvas()
#  profile.Draw('COLZ')
#  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngTails/'+ratio.lower()+'_forProj.root')
#  ecalveto.Draw('boxsame')
#  #phef.Draw('colzsame')
#  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngTails/'+ratio.lower()+'.png')
#  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngTails/'+ratio.lower()+'.pdf')
#  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngTails/'+ratio.lower()+'.root')
for ratio in ['Phef', 'Chef', 'Nhef','Ceef', 'Neef', 'Muef', 'Elef', 'Unc']:
  profile = ROOT.TProfile2D(ratio.lower(),ratio.lower(),120,-3,3,120,-pi,pi)
  c.Draw('jet'+ratio+'*jetPt:jetPhi:jetEta>>'+ratio.lower(),'')
  c1 = ROOT.TCanvas()
  profile.Draw('COLZ')
  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngTails/'+ratio.lower()+'timesPt_forProj.root')
  ecalveto.Draw('boxsame')
  #phef.Draw('colzsame')
  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngTails/'+ratio.lower()+'timesPt.png')
  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngTails/'+ratio.lower()+'timesPt.pdf')
  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngTails/'+ratio.lower()+'timesPt.root')
