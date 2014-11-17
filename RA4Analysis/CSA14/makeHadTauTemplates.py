import ROOT
import pickle
from Workspace.RA4Analysis.stage2Tuples import ttJetsCSA1450ns
from array import array
c = ROOT.TChain('Events')
for b in ttJetsCSA1450ns['bins']:
  c.Add(ttJetsCSA1450ns['dirname']+'/'+b+'/h*.root')

stuff=[]
hadTauReq = 'gTauNENu+gTauNMuNu==0&&gTauNTauNu==1'

from Workspace.RA4Analysis.objectSelection import gTauAbsEtaBins, gTauPtBins, metParRatioBins, jetRatioBins

colors = [ROOT.kGray, ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kGreen, ROOT.kMagenta, ROOT.kCyan]

def getCut(var, bin):
  s=var+'_'+str(bin[0])
  cut = var+">="+str(bin[0])
  if bin[1]!=-1:
      cut+="&&"+var+"<"+str(bin[1])
      s+='_'+str(bin[1])
  return cut, s

##Taus: Pt
#c1 = ROOT.TCanvas()
#c.Draw('gTauEta>>hgenTauEta(100,-5,5)',hadTauReq)
#hgenTauEta=ROOT.gDirectory.Get('hgenTauEta')
#c1.SetLogy()
#c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/hgenTauEta.png')
#del hgenTauEta
#c.Draw('gTauPt>>hgenTauPt(100,0,500)',hadTauReq)
#hgenTauPt=ROOT.gDirectory.Get('hgenTauPt')
#c1.SetLogy()
#c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/hgenTauPt.png')
#del hgenTauPt
#
##Taus: Pt VS Eta
#c1 = ROOT.TCanvas()
#c.Draw('gTauEta:gTauPt>>hgenTau2D(20,0,500,20,-5,5)',hadTauReq,'COLZ')
#hgenTau2D=ROOT.gDirectory.Get('hgenTau2D')
#c1.SetLogz()
#c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/genTauPt_vs_genTauEta.png')
#del hgenTau2D
#
##Compare jet-DR cuts for genTau Match
#c1 = ROOT.TCanvas()
#c.Draw('gTauJetDR>>hgenTauDR(100,0,2)','gTauPt>40&&'+hadTauReq,'goff')
#hgenTauDR=ROOT.gDirectory.Get('hgenTauDR')
#c.Draw('gTauJetDR>>hgenTauDRHigh(100,0,2)','gTauPt>100&&'+hadTauReq,'goff')
#hgenTauDRHigh=ROOT.gDirectory.Get('hgenTauDRHigh')
#hgenTauDRHigh.SetLineColor(ROOT.kRed)
#c.Draw('gTauJetDR>>hgenTauDRLow(100,0,2)','gTauPt>40&&gTauPt<100&&'+hadTauReq,'goff')
#hgenTauDRLow=ROOT.gDirectory.Get('hgenTauDRLow')
#hgenTauDRLow.SetLineColor(ROOT.kBlue)
#hgenTauDR.GetYaxis().SetRangeUser(0.7, 1.2*hgenTauDR.GetBinContent(hgenTauDR.GetMaximumBin()))
#hgenTauDR.Draw()
#hgenTauDRHigh.Draw('same')
#hgenTauDRLow.Draw('same')
#c1.SetLogy()
#c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/genTauDR.png')
#del hgenTauDR
#
##Compare genTau/recoTau-DR cuts for genTau Match
#c1 = ROOT.TCanvas()
#c.Draw('gTauTauDR>>hgenTauDR(100,0,2)','gTauPt>40&&'+hadTauReq,'goff')
#hgenTauDR=ROOT.gDirectory.Get('hgenTauDR')
#c.Draw('gTauTauDR>>hgenTauDRHigh(100,0,2)','gTauPt>100&&'+hadTauReq,'goff')
#hgenTauDRHigh=ROOT.gDirectory.Get('hgenTauDRHigh')
#hgenTauDRHigh.SetLineColor(ROOT.kRed)
#c.Draw('gTauTauDR>>hgenTauDRLow(100,0,2)','gTauPt>40&&gTauPt<100&&'+hadTauReq,'goff')
#hgenTauDRLow=ROOT.gDirectory.Get('hgenTauDRLow')
#hgenTauDRLow.SetLineColor(ROOT.kBlue)
#hgenTauDR.GetYaxis().SetRangeUser(0.7, 1.2*hgenTauDR.GetBinContent(hgenTauDR.GetMaximumBin()))
#hgenTauDR.Draw()
#hgenTauDRHigh.Draw('same')
#hgenTauDRLow.Draw('same')
#c1.SetLogy()
#c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/recoTauGenTauDR.png')
#del hgenTauDR
#
##Perp and Par ratio in bins of gTauPt
#c1 = ROOT.TCanvas()
#c.Draw('gTauMetPerp/gTauPt>>hgTauMetPerp(100,-.1,.1)','gTauPt>10.&&'+hadTauReq)
#hgTauMetPerp=ROOT.gDirectory.Get('hgenTau2D')
#c1.SetLogz()
#c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/hgTauMetPerpRatio.png')
#del hgTauMetPerp
#c.Draw('gTauMetPar/gTauPt>>hgTauMetPar(120,-.1,1.1)','gTauPt>10.&&'+hadTauReq)
#hgTauMetPar=ROOT.gDirectory.Get('hgTauMetPar')
#hgTauMetParPt={}
#for i, b in enumerate(gTauPtBins):
#  cut,s = getCut('gTauPt',b)
#  hgTauMetParPt[b] = ROOT.TH1F('hgTauMetPar_'+s, 'hgTauMetPar_'+s,120,-.1,1.1)
#  hgTauMetParPt[b].SetLineColor(colors[i])
#  c.Draw('gTauMetPar/gTauPt>>hgTauMetPar_'+s,cut+"&&"+hadTauReq,'goff')
#hgTauMetPar.Draw()
#for b in gTauPtBins:
#  hgTauMetParPt[b].Scale(hgTauMetParPt[gTauPtBins[0]].Integral()/hgTauMetParPt[b].Integral())
#  hgTauMetParPt[b].Draw('same')
#c1.SetLogz()
#c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/hgTauMetParRatio.png')
#
##MetPar/gTauPT ratio in bins of gTauPt and gTauEta
#c1 = ROOT.TCanvas()
#for etab in gTauAbsEtaBins:
#  etaCut, seta = getCut('abs(gTauEta)', etab)
#  seta=seta.replace('abs(gTauEta)','eta') 
#  c.Draw('gTauMetPar/gTauPt>>hgTauMetPar(10,0,1)','gTauPt>10.&&'+etaCut+"&&"+hadTauReq)
#  hgTauMetPar=ROOT.gDirectory.Get('hgTauMetPar')
#  hgTauMetParPt={}
#  for i, b in enumerate(gTauPtBins):
#    cut,s = getCut('gTauPt',b)
#    cut+='&&'+etaCut
#    hgTauMetParPt[b] = ROOT.TH1F('hgTauMetPar_'+s, 'hgTauMetPar_'+s,10,0,1)
#    hgTauMetParPt[b].SetLineColor(colors[i])
#    c.Draw('gTauMetPar/gTauPt>>hgTauMetPar_'+s,cut+"&&"+hadTauReq,'goff')
#  hgTauMetPar.Draw()
#  hgTauMetPar.GetYaxis().SetRangeUser(0, 1.2*hgTauMetPar.GetBinContent(hgTauMetPar.GetMaximumBin()))
#  for b in gTauPtBins:
#    hgTauMetParPt[b].Scale(hgTauMetParPt[gTauPtBins[0]].Integral()/hgTauMetParPt[b].Integral())
#    hgTauMetParPt[b].Draw('same')
#  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/hgTauMetParRatio_'+seta+'.png')
#
##JetPt/gTauPt ratio in bins of gTauPt and gTauEta
#c1 = ROOT.TCanvas()
#for etab in gTauAbsEtaBins+[(0,-1)]:
#  etaCut, seta = getCut('abs(gTauEta)', etab)
#  seta=seta.replace('abs(gTauEta)','eta') 
#  c.Draw('0>>hgTauJetPar(50,-0.2,3)',                             'gTauJetInd==0&&gTauPt>10.&&'+etaCut+"&&"+hadTauReq)
#  c.Draw('jetPt[gTauJetInd]*(gTauJetDR<0.3)/gTauPt>>+hgTauJetPar','gTauJetInd>0&&gTauPt>10.&&'+etaCut+"&&"+hadTauReq)
#  hgTauJetPar=ROOT.gDirectory.Get('hgTauJetPar')
#  hgTauJetParPt={}
#  for i, b in enumerate(gTauPtBins):
#    cut,s = getCut('gTauPt',b)
#    cut+='&&'+etaCut
#    hgTauJetParPt[b] = ROOT.TH1F('hgTauJetPar_'+s, 'hgTauJetPar_'+s,50,-0.2,3)
#    hgTauJetParPt[b].SetLineColor(colors[i])
#    c.Draw('0>>hgTauJetPar_'+s,                                                       'gTauJetInd==0&&gTauPt>10.&&'+cut+"&&"+hadTauReq,'goff')
#    c.Draw('jetPt[gTauJetInd]*(gTauJetDR<0.3)/gTauPt>>+hgTauJetPar_'+s,               'gTauJetInd>0&&gTauPt>10.&&'+cut+"&&"+hadTauReq,'goff')
#  hgTauJetPar.Draw()
#  hgTauJetPar.GetYaxis().SetRangeUser(0.7, 1.2*hgTauJetPar.GetBinContent(hgTauJetPar.GetMaximumBin()))
#  for b in gTauPtBins:
#    if hgTauJetParPt[b].Integral()>0:
#      hgTauJetParPt[b].Scale(hgTauJetParPt[gTauPtBins[0]].Integral()/hgTauJetParPt[b].Integral())
#    hgTauJetParPt[b].Draw('same')
#  c1.SetLogy()
#  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/hgTauJetParRatio_'+seta+'.png')
#
##gTauTauPt/gTauPt ratio in bins of gTauPt and gTauEta
#c1 = ROOT.TCanvas()
#for etab in gTauAbsEtaBins+[(0,-1)]:
#  etaCut, seta = getCut('abs(gTauEta)', etab)
#  seta=seta.replace('abs(gTauEta)','eta') 
#  c.Draw('0>>hgTauTauPar(50,-0.2,3)',                             'gTauTauInd==0&&gTauPt>10.&&'+etaCut+"&&"+hadTauReq)
#  c.Draw('tauPt[gTauTauInd]*(gTauTauDR<0.4)/gTauPt>>+hgTauTauPar','gTauTauInd>0&&gTauPt>10.&&'+etaCut+"&&"+hadTauReq)
#  hgTauTauPar=ROOT.gDirectory.Get('hgTauTauPar')
#  hgTauTauParPt={}
#  for i, b in enumerate(gTauPtBins):
#    cut,s = getCut('gTauPt',b)
#    cut+='&&'+etaCut
#    hgTauTauParPt[b] = ROOT.TH1F('hgTauTauPar_'+s, 'hgTauTauPar_'+s,50,-0.2,3)
#    hgTauTauParPt[b].SetLineColor(colors[i])
#    c.Draw('0>>hgTauTauPar_'+s,                                                       'gTauTauInd==0&&gTauPt>10&&'+cut+"&&"+hadTauReq,'goff')
#    c.Draw('tauPt[gTauTauInd]*(gTauTauDR<0.4)/gTauPt>>+hgTauTauPar_'+s,               'gTauTauInd>0&&gTauPt>10&&'+cut+"&&"+hadTauReq,'goff')
#  hgTauTauPar.Draw()
#  hgTauTauPar.GetYaxis().SetRangeUser(0.7, 1.2*hgTauTauPar.GetBinContent(hgTauTauPar.GetMaximumBin()))
#  for b in gTauPtBins:
#    if hgTauTauParPt[b].Integral()>0:
#      hgTauTauParPt[b].Scale(hgTauTauParPt[gTauPtBins[0]].Integral()/hgTauTauParPt[b].Integral())
#    hgTauTauParPt[b].Draw('same')
#  c1.SetLogy()
#  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/hgTauTauParRatio_'+seta+'.png')
#
###gTauMetPar/gTauPt VS. jpt templates in bins of gTauPt and gTauEta
#c1 = ROOT.TCanvas()
#templates={}
#for etab in gTauAbsEtaBins+[(0,-1)]:
#  etaCut, seta = getCut('abs(gTauEta)', etab)
#  seta=seta.replace('abs(gTauEta)','eta') 
#  jetGenTauTemplatePt={}
#  for i, b in enumerate(gTauPtBins+[(10,-1)]):
#    if not templates.has_key(b):
#      templates[b]={}
#    cut,s = getCut('gTauPt',b)
#    cut+='&&'+etaCut
#    s+="_"+seta
#    jetGenTauTemplatePt[b] = ROOT.TH2F('jetGenTauTemplate_'+s, 'jetGenTauTemplate_'+s,len(metParRatioBins)-1, array('d',metParRatioBins),len(jetRatioBins)-1,array('d',jetRatioBins))
#    c.Draw('0:gTauMetPar/gTauPt>>jetGenTauTemplate_'+s,                                                       'gTauJetInd==0&&'+cut+"&&"+hadTauReq,'goff')
#    c.Draw('jetPt[gTauJetInd]/gTauPt*(gTauJetDR<0.3):gTauMetPar/gTauPt>>+jetGenTauTemplate_'+s,               'gTauJetInd>0&&'+cut+"&&"+hadTauReq,'goff')
#    jetGenTauTemplatePt[b].Scale(1./jetGenTauTemplatePt[b].Integral())
#    jetGenTauTemplatePt[b].Draw('COLZ')
#    templates[b][etab]=jetGenTauTemplatePt[b]
#    c1.SetLogz()
#    c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/jetGenTauTemplate_'+s+'.png')
#pickle.dump(templates, file('/data/schoef/results2014/tauTemplates/CSA14_TTJets_jetGenTau.pkl','w'))
#
##gTauMetPar/gTauPt VS. recoTau/genTau templates in bins of gTauPt and gTauEta
#c1 = ROOT.TCanvas()
#templates={}
#for etab in gTauAbsEtaBins+[(0,-1)]:
#  etaCut, seta = getCut('abs(gTauEta)', etab)
#  seta=seta.replace('abs(gTauEta)','eta') 
#  recoTauGenTauTemplatePt={}
#  for i, b in enumerate(gTauPtBins+[(10,-1)]):
#    if not templates.has_key(b):
#      templates[b]={}
#    cut,s = getCut('gTauPt',b)
#    cut+='&&'+etaCut
#    s+="_"+seta
#    recoTauGenTauTemplatePt[b] = ROOT.TH2F('recoTauGenTauTemplate_'+s, 'recoTauGenTauTemplate_'+s,len(metParRatioBins)-1, array('d',metParRatioBins),len(jetRatioBins)-1,array('d',jetRatioBins))
#    c.Draw('0:gTauMetPar/gTauPt>>recoTauGenTauTemplate_'+s,                                                   'gTauTauInd==0&&'+cut+"&&"+hadTauReq,'goff')
#    c.Draw('tauPt[gTauTauInd]/gTauPt*(gTauTauDR<0.4):gTauMetPar/gTauPt>>+recoTauGenTauTemplate_'+s,           'gTauTauInd>0&&'+cut+"&&"+hadTauReq,'goff')
#    recoTauGenTauTemplatePt[b].Scale(1./recoTauGenTauTemplatePt[b].Integral())
#    recoTauGenTauTemplatePt[b].Draw('COLZ')
#    templates[b][etab]=recoTauGenTauTemplatePt[b]
#    c1.SetLogz()
#    c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/recoTauGenTauTemplate_'+s+'.png')
#pickle.dump(templates, file('/data/schoef/results2014/tauTemplates/CSA14_TTJets_recoTauGenTau.pkl','w'))

##gTauMetPar/gTauPt VS. restJet/genTau templates in bins of gTauPt and gTauEta
#c1 = ROOT.TCanvas()
#templates={}
#for etab in gTauAbsEtaBins+[(0,-1)]:
#  etaCut, seta = getCut('abs(gTauEta)', etab)
#  seta=seta.replace('abs(gTauEta)','eta') 
#  genTauTemplatePt={}
#  for i, b in enumerate(gTauPtBins+[(10,-1)]):
#    if not templates.has_key(b):
#      templates[b]={}
#    cut,s = getCut('gTauPt',b)
#    cut+='&&'+etaCut
#    s+="_"+seta
#    genTauTemplatePt[b] = ROOT.TH1F('genTauTemplate_'+s, 'genTauTemplate_'+s,len(metParRatioBins)-1, array('d',metParRatioBins))
#    c.Draw('gTauMetPar/gTauPt>>genTauTemplate_'+s,  cut+"&&"+hadTauReq,'goff')
#    genTauTemplatePt[b].Scale(1./genTauTemplatePt[b].Integral())
#    genTauTemplatePt[b].Draw()
#    templates[b][etab]=genTauTemplatePt[b]
#    c1.SetLogz()
#    c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/genTauTemplate_'+s+'.png')
#ofile = '/data/schoef/results2014/tauTemplates/CSA14_TTJets_genTau.pkl'
#pickle.dump(templates, file(ofile,'w'))
#print "Written", ofile 


###BELOW IS JUST FOR QUICK PLOT!!
#gTauMetPar/gTauPt VS. restJet/genTau templates in bins of gTauPt and gTauEta
c1 = ROOT.TCanvas()
templates={}
for etab in [(0,0.5)]:
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
    c.Draw('gTauMetPar/gTauPt>>genTauTemplate_'+s,  cut+"&&"+hadTauReq,'goff')
    genTauTemplatePt[b].Scale(1./genTauTemplatePt[b].Integral())
    genTauTemplatePt[b].Draw()
    templates[b][etab]=genTauTemplatePt[b]
    c1.SetLogz()
    c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/genTauTemplate_'+s+'.png')

c1 = ROOT.TCanvas()
l=ROOT.TLegend(0.7,0.5,1.0,1.0)
l.SetFillColor(ROOT.kWhite)
l.SetShadowColor(ROOT.kWhite)
l.SetBorderSize(1)

ROOT.gStyle.SetOptStat(0)
etab = gTauAbsEtaBins[0]
etaCut, seta = getCut('abs(gTauEta)', etab)
seta=seta.replace('abs(gTauEta)','eta') 
first = True
templates[(10,-1)][etab].GetYaxis().SetRangeUser(0, 0.3)
templates[(10,-1)][etab].SetTitle("")
templates[(10,-1)][etab].SetLineWidth(3)
templates[(10,-1)][etab].Draw('goff')
c1.SetLogz()
for i, b in enumerate(gTauPtBins):
  l.AddEntry(templates[b][etab], getCut('pT(tau)', b)[0])
  templates[b][etab].SetLineColor(colors[i])
  templates[b][etab].Draw('same')

l.Draw()
c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/genTauTemplate_'+seta+'.png')
