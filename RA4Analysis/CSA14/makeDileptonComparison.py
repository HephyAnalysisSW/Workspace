import ROOT
#from stage2Tuples import ttJetsCSA14
from localInfo import username

htCut     = 400
metCut    = 150
minNJets  =   4


cPred = ROOT.TChain('Events')
hMTPred = ROOT.TH1F('hMTPred', 'hMTPred',40,0,800)
cPred.Add('/data/easilar/results2014/CSA14_DiLep.root')
#cPred.Add('/data/'+username+'/results2014/CSA14_DiLep.root')
print username
#option goff: no graphics
cPred.Draw('mTPred>>hMTPred','weightPred*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')')

c1=ROOT.TCanvas()
hMTPred.SetLineColor(ROOT.kRed)
#hMTPred.Scale(hMT.Integral()/hMTPred.Integral())
hMTPred.Draw()
c1.SetLogy()
c1.Print('/afs/hephy.at/user/e/easilar/www/hMTtest.png')
