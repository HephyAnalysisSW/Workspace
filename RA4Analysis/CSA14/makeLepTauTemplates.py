import ROOT
import pickle
from Workspace.RA4Analysis.stage2Tuples import ttJetsCSA14
from array import array
c = ROOT.TChain('Events')
for b in ttJetsCSA14['bins']:
  c.Add(ttJetsCSA14['dirname']+'/'+b+'/h*.root')

stuff=[]
lepTauReq = 'gTauNENu+gTauNMuNu==1&&gTauNTauNu==1'

from Workspace.RA4Analysis.objectSelection import gTauAbsEtaBins, gTauPtBins, metParRatioBins, jetRatioBins

colors = [ROOT.kGray, ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kGreen, ROOT.kMagenta, ROOT.kCyan]

def getCut(var, bin):
  s=var+'_'+str(bin[0])
  cut = var+">="+str(bin[0])
  if bin[1]!=-1:
      cut+="&&"+var+"<"+str(bin[1])
      s+='_'+str(bin[1])
  return cut, s



##Perp and Par ratio in bins of gTauPt
#c1 = ROOT.TCanvas()
#c.Draw('gTauMetPerp/gTauPt>>lgTauMetPerp(100,-.1,.1)','gTauPt>10.&&'+lepTauReq)
#lgTauMetPerp=ROOT.gDirectory.Get('lgenTau2D')
#c1.SetLogz()
#c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/lgTauMetPerpRatio.png')
#del lgTauMetPerp
#c.Draw('gTauMetPar/gTauPt>>lgTauMetPar(120,-.1,1.1)','gTauPt>10.&&'+lepTauReq)
#lgTauMetPar=ROOT.gDirectory.Get('lgTauMetPar')
#lgTauMetParPt={}
#for i, b in enumerate(gTauPtBins):
#  cut,s = getCut('gTauPt',b)
#  lgTauMetParPt[b] = ROOT.TH1F('lgTauMetPar_'+s, 'lgTauMetPar_'+s,120,-.1,1.1)
#  lgTauMetParPt[b].SetLineColor(colors[i])
#  c.Draw('gTauMetPar/gTauPt>>lgTauMetPar_'+s,cut+"&&"+lepTauReq,'goff')
#lgTauMetPar.Draw()
#for b in gTauPtBins:
#  lgTauMetParPt[b].Scale(lgTauMetParPt[gTauPtBins[0]].Integral()/lgTauMetParPt[b].Integral())
#  lgTauMetParPt[b].Draw('same')
#c1.SetLogz()
#c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/lgTauMetParRatio.png')

#MetPar/gTauPT ratio in bins of gTauPt and gTauEta
c1 = ROOT.TCanvas()
for etab in gTauAbsEtaBins:
  etaCut, seta = getCut('abs(gTauEta)', etab)
  seta=seta.replace('abs(gTauEta)','eta') 
  c.Draw('gTauMetPar/gTauPt>>lgTauMetPar(10,0,1)','gTauPt>10.&&'+etaCut+"&&"+lepTauReq)
  lgTauMetPar=ROOT.gDirectory.Get('lgTauMetPar')
  lgTauMetParPt={}
  for i, b in enumerate(gTauPtBins):
    cut,s = getCut('gTauPt',b)
    cut+='&&'+etaCut
    lgTauMetParPt[b] = ROOT.TH1F('lgTauMetPar_'+s, 'lgTauMetPar_'+s,10,0,1)
    lgTauMetParPt[b].SetLineColor(colors[i])
    c.Draw('gTauMetPar/gTauPt>>lgTauMetPar_'+s,cut+"&&"+lepTauReq,'goff')
  lgTauMetPar.Draw()
  lgTauMetPar.GetYaxis().SetRangeUser(0, 1.2*lgTauMetPar.GetBinContent(lgTauMetPar.GetMaximumBin()))
  for b in gTauPtBins:
    lgTauMetParPt[b].Scale(lgTauMetParPt[gTauPtBins[0]].Integral()/lgTauMetParPt[b].Integral())
    lgTauMetParPt[b].Draw('same')
  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/lgTauMetParRatio_'+seta+'.png')


#gTauMetPar/gTauPt VS. restJet/genTau templates in bins of gTauPt and gTauEta
c1 = ROOT.TCanvas()
templates={}
for etab in gTauAbsEtaBins+[(0,-1)]:
  etaCut, seta = getCut('abs(gTauEta)', etab)
  seta=seta.replace('abs(gTauEta)','eta') 
  genTauTemplatePt={}
  for i, b in enumerate(gTauPtBins+[(10,-1)]):
    if not templates.has_key(b):
      templates[b]={}
    cut,s = getCut('gTauPt',b)
    cut+='&&'+etaCut
    s+="_"+seta
    genTauTemplatePt[b] = ROOT.TH1F('genTauTemplate_'+s, 'genTauTemplate_'+s,len(metParRatioBins)-1, array('d',metParRatioBins))
    c.Draw('gTauMetPar/gTauPt>>genTauTemplate_'+s,  cut+"&&"+lepTauReq,'goff')
    genTauTemplatePt[b].Scale(1./genTauTemplatePt[b].Integral())
    genTauTemplatePt[b].Draw()
    templates[b][etab]=genTauTemplatePt[b]
    c1.SetLogz()
    c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/lepGenTauTemplate_'+s+'.png')

ofile = '/data/schoef/results2014/tauTemplates/CSA14_TTJets_lepGenTau.pkl'
pickle.dump(templates, file(ofile,'w'))
print "Written", ofile

