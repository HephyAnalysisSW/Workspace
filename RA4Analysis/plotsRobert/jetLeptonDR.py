import ROOT
import pickle
from array import array
from Workspace.RA4Analysis.objectSelection import gTauAbsEtaBins, gTauPtBins, metParRatioBins, jetRatioBins
from Workspace.HEPHYPythonTools.helpers import getVarValue, getObjFromFile, findClosestObjectDR, deltaR
from Workspace.RA4Analysis.objectSelection import getLooseMuStage2, tightPOGMuID, vetoMuID, getGoodJetsStage2
from Workspace.RA4Analysis.stage2Tuples import *
from math import sqrt, cos, sin, atan2, sinh, cosh

presel = 'ht>400&&met>150&&nmuCount>0'
small = True

#sample = ttJetsCSA1450ns
#prefix='standardCC'
#sample = vetoCC_ttJetsCSA1450ns
#prefix='vetoCC'
sample = DR4CC_ttJetsCSA1450ns
prefix='DR4CC'

c = ROOT.TChain('Events')
for b in sample['bins']:
  files=os.listdir(sample['dirname']+'/'+b)
  for f in files:
    if not 'small' in f:
      c.Add(sample['dirname']+'/'+b+'/'+f)

c.Draw(">>eList", presel)
eList = ROOT.gDirectory.Get("eList")
number_events = eList.GetN()
maxN=100000
if small:
  if number_events>maxN:
    number_events=maxN
number_events=min(number_events, eList.GetN())
countLeptons=0

varBinning={}
varBinning['ptRel'] = [100,0,50]

plot={}
for var in ['muef', 'dR', 'ptRatio', 'ptRel']:
  plot[var] = {}
  for id in ['Loose', 'Tight']:
    plot[var][id]={}
    for dr in ['Near', 'Far', 'All']:
      plot[var][id][dr]={}
      for isB in ['b', 'noB', 'All']:
        t = '_'.join([var, id, dr, isB])
        binning=[100,0,2]
        if varBinning.has_key(var):
          binning = varBinning[var]
        plot[var][id][dr][isB] = ROOT.TH1F(t,t,*binning)
        plot[var][id][dr][isB].GetXaxis().SetTitle(var)
#        if id=='Loose':
#          plot[var][id][dr][isB].SetLineColor(ROOT.kRed)
#        if isB=='noB':
#          plot[var][id][dr][isB].SetLineStyle(2)

ptRatioVSdRLoose = ROOT.TH2F('ptRatio_vs_dR','ptRatio_vs_dR',100,0,1,100,0,2)
ptRatioVSdRLoose.GetYaxis().SetTitle('ptRatio')
ptRatioVSdRLoose.GetXaxis().SetTitle('dR')
ptRatioVSdRLoose_b = ROOT.TH2F('ptRatio_vs_dR','ptRatio_vs_dR',100,0,1,100,0,2)
ptRatioVSdRLoose_b.GetYaxis().SetTitle('ptRatio')
ptRatioVSdRLoose_b.GetXaxis().SetTitle('dR')
ptRatioVSdRLoose_nob = ROOT.TH2F('ptRatio_vs_dR','ptRatio_vs_dR',100,0,1,100,0,2)
ptRatioVSdRLoose_nob.GetYaxis().SetTitle('ptRatio')
ptRatioVSdRLoose_nob.GetXaxis().SetTitle('dR')
ptRatioVSdRTight = ROOT.TH2F('ptRatio_vs_dR','ptRatio_vs_dR',100,0,1,100,0,2)
ptRatioVSdRTight.GetYaxis().SetTitle('ptRatio')
ptRatioVSdRTight.GetXaxis().SetTitle('dR')

ptRatioVSptRelLoose = ROOT.TH2F('ptRatio_vs_ptRel','ptRatio_vs_ptRel',100,0,50,100,0,2)
ptRatioVSptRelLoose.GetYaxis().SetTitle('ptRatio')
ptRatioVSptRelLoose.GetXaxis().SetTitle('ptRel')
ptRatioVSptRelLoose_b = ROOT.TH2F('ptRatio_vs_ptRel','ptRatio_vs_ptRel',100,0,50,100,0,2)
ptRatioVSptRelLoose_b.GetYaxis().SetTitle('ptRatio')
ptRatioVSptRelLoose_b.GetXaxis().SetTitle('ptRel')
ptRatioVSptRelLoose_nob = ROOT.TH2F('ptRatio_vs_ptRel','ptRatio_vs_ptRel',100,0,50,100,0,2)
ptRatioVSptRelLoose_nob.GetYaxis().SetTitle('ptRatio')
ptRatioVSptRelLoose_nob.GetXaxis().SetTitle('ptRel')
ptRatioVSptRelTight = ROOT.TH2F('ptRatio_vs_ptRel','ptRatio_vs_ptRel',100,0,50,100,0,2)
ptRatioVSptRelTight.GetYaxis().SetTitle('ptRatio')
ptRatioVSptRelTight.GetXaxis().SetTitle('ptRel')

nLightJet = 0
nBJet = 0
nLightJetLost = 0
nBJetLost = 0

for i in range(number_events):
  if (i%10000 == 0) and i>0 :
    print i,"/",number_events
  c.GetEntry(eList.GetEntry(i))
  jets = getGoodJetsStage2(c)
  nmuCount = int(getVarValue(c, 'nmuCount' ))
  vetoMuons=[]
  for i in range(nmuCount):
    l=getLooseMuStage2(c, i)
    if vetoMuID(l) and l['pt']>15:
      vetoMuons.append(l)
      closestJet = findClosestObjectDR(jets, l)
      jet = closestJet['obj']

      cosPhi3D = (cos(l['phi'] - jet['phi']) + sinh(l['eta'])*sinh(jet['eta']))/(cosh(jet['eta'])*cosh(l['eta']))
      ptRel = jet['pt']*sqrt(1-cosPhi3D**2) 

      isB = abs(jet['pdg'])==5
      isTight = tightPOGMuID(l)
      isNear = closestJet['deltaR']<0.4

      nKeys=['All']
      if isNear:
        nKeys += ['Near']
      else:
        nKeys += ['Far']

      idKeys = ['Loose']      
      if isTight:
        idKeys += ['Tight']

      bKeys = ['All'] 
      if isB:
        bKeys+=['b']
      else:
        bKeys+=['noB']
      
      for idK in idKeys:
        for nK in nKeys:
          for bK in bKeys:
            plot['muef'][idK][nK][bK].Fill(jet['muef'])
            plot['dR'][idK][nK][bK].Fill(closestJet['deltaR'])
            plot['ptRatio'][idK][nK][bK].Fill(l['pt']/jet['pt'])
            plot['ptRel'][idK][nK][bK].Fill(ptRel)

      ptRatioVSdRLoose.Fill(closestJet['deltaR'], l['pt']/jet['pt'])
      if isTight:
        ptRatioVSdRTight.Fill(closestJet['deltaR'], l['pt']/jet['pt'])
      if isB:
        ptRatioVSdRLoose_b.Fill(closestJet['deltaR'], l['pt']/jet['pt'])
      else:
        ptRatioVSdRLoose_nob.Fill(closestJet['deltaR'], l['pt']/jet['pt'])
      ptRatioVSptRelLoose.Fill(ptRel, l['pt']/jet['pt'])
      if isTight:
        ptRatioVSptRelTight.Fill(ptRel, l['pt']/jet['pt'])
      if isB:
        ptRatioVSptRelLoose_b.Fill(ptRel, l['pt']/jet['pt'])
      else:
        ptRatioVSptRelLoose_nob.Fill(ptRel, l['pt']/jet['pt'])
  
  for j in jets:
    if j['btag']>0.679:
      nBJet +=1
    else:
      nLightJet +=1
    for m in vetoMuons:
      if deltaR(j, m)<0.4:
        if j['btag']>0.679:
          nBJetLost +=1
        else:
          nLightJetLost +=1
        break

print "Lost light jets:",nLightJetLost/float(nLightJet),"from",nLightJet
print "Lost b jets:",nBJetLost/float(nBJet),"from",nBJet
          
ROOT.gStyle.SetOptStat(0)
c1=ROOT.TCanvas()

for iDk in ['Loose','Tight']:
  for var in ['dR', 'muef', 'ptRatio', 'ptRel']:
    c1.SetLogy()
    plot[var][iDk]['All']['All'].SetTitle("")
    plot[var][iDk]['All']['All'].GetYaxis().SetRangeUser(0.7, 1.5*plot[var][iDk]['All']['All'].GetBinContent(plot[var][iDk]['All']['All'].GetMaximumBin()))
    plot[var][iDk]['All']['All'].Draw()
#    plot[var][iDk]['Near']['All'].Draw('same')
    plot[var][iDk]['Near']['b'].SetLineColor(ROOT.kGreen)
    plot[var][iDk]['Near']['b'].Draw('same')
    plot[var][iDk]['Near']['noB'].SetLineColor(ROOT.kGreen)
    plot[var][iDk]['Near']['noB'].SetLineStyle(2)
    plot[var][iDk]['Near']['noB'].Draw('same')
#    plot[var][iDk]['Far']['All'].Draw('same')
    plot[var][iDk]['Far']['b'].SetLineColor(ROOT.kMagenta)
    plot[var][iDk]['Far']['b'].Draw('same')
    plot[var][iDk]['Far']['noB'].SetLineColor(ROOT.kMagenta)
    plot[var][iDk]['Far']['noB'].SetLineStyle(2)
    plot[var][iDk]['Far']['noB'].Draw('same')
#    plot[var][iDk]['All']['b'].SetLineColor(ROOT.kRed)
#    plot[var][iDk]['All']['b'].Draw('same')
    plot[var][iDk]['All']['noB'].SetLineColor(ROOT.kRed)
    plot[var][iDk]['All']['noB'].SetLineStyle(2)
    plot[var][iDk]['All']['noB'].Draw('same')
    plot[var][iDk]['All']['b'].SetLineColor(ROOT.kRed)
    plot[var][iDk]['All']['b'].Draw('same')
    plot[var][iDk]['All']['All'].Draw('same')
    l=ROOT.TLegend(0.7,0.7,1.0,1.0)
    l.SetFillColor(ROOT.kWhite) 
    l.SetShadowColor(ROOT.kWhite)
    l.SetBorderSize(1)
    l.AddEntry(plot[var][iDk]['All']['All'], 'All')
    l.AddEntry(plot[var][iDk]['All']['b'], 'from b')
    l.AddEntry(plot[var][iDk]['All']['noB'], 'not from b')
#    l.AddEntry(plot[var][iDk]['Near']['All'], 'All (near)')
    l.AddEntry(plot[var][iDk]['Near']['b'], 'from b (near)')
    l.AddEntry(plot[var][iDk]['Near']['noB'], 'not from b (near)')
#    l.AddEntry(plot[var][iDk]['Far']['All'], 'All (far)')
    l.AddEntry(plot[var][iDk]['Far']['b'], 'from b (far)')
    l.AddEntry(plot[var][iDk]['Far']['noB'], 'not from b (far)')
    l.Draw()
    c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/'+var+'_'+iDk+'_b_'+prefix+'.png')

for iDk in ['Loose','Tight']:
  for var in ['dR', 'muef', 'ptRatio', 'ptRel']:
    c1.SetLogy()
    plot[var][iDk]['Near']['All'].SetTitle("")
    plot[var][iDk]['Near']['All'].GetYaxis().SetRangeUser(0.7, 1.5*plot[var][iDk]['All']['All'].GetBinContent(plot[var][iDk]['All']['All'].GetMaximumBin()))
    plot[var][iDk]['Near']['All'].Draw()
#    plot[var][iDk]['Near']['All'].Draw('same')
    plot[var][iDk]['Near']['b'].SetLineColor(ROOT.kGreen)
    plot[var][iDk]['Near']['b'].Draw('same')
    plot[var][iDk]['Near']['noB'].SetLineColor(ROOT.kGreen)
    plot[var][iDk]['Near']['noB'].SetLineStyle(2)
    plot[var][iDk]['Near']['noB'].Draw('same')
    plot[var][iDk]['Near']['All'].Draw('same')
    l=ROOT.TLegend(0.7,0.7,1.0,1.0)
    l.SetFillColor(ROOT.kWhite) 
    l.SetShadowColor(ROOT.kWhite)
    l.SetBorderSize(1)
    l.AddEntry(plot[var][iDk]['Near']['All'], 'All (near)')
    l.AddEntry(plot[var][iDk]['Near']['b'], 'from b (near)')
    l.AddEntry(plot[var][iDk]['Near']['noB'], 'not from b (near)')
    l.Draw()
    c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/'+var+'_'+iDk+'_b_onlyNear_'+prefix+'.png')

for iDk in ['Loose','Tight']:
  for var in ['dR', 'muef', 'ptRatio', 'ptRel']:
    c1.SetLogy()
    plot[var][iDk]['Far']['All'].SetTitle("")
    plot[var][iDk]['Far']['All'].GetYaxis().SetRangeUser(0.7, 1.5*plot[var][iDk]['All']['All'].GetBinContent(plot[var][iDk]['All']['All'].GetMaximumBin()))
    plot[var][iDk]['Far']['All'].Draw()
    plot[var][iDk]['Far']['b'].SetLineColor(ROOT.kMagenta)
    plot[var][iDk]['Far']['b'].Draw('same')
    plot[var][iDk]['Far']['noB'].SetLineColor(ROOT.kMagenta)
    plot[var][iDk]['Far']['noB'].SetLineStyle(2)
    plot[var][iDk]['Far']['noB'].Draw('same')
    plot[var][iDk]['Far']['All'].Draw('same')
    l=ROOT.TLegend(0.7,0.7,1.0,1.0)
    l.SetFillColor(ROOT.kWhite) 
    l.SetShadowColor(ROOT.kWhite)
    l.SetBorderSize(1)
    l.AddEntry(plot[var][iDk]['Far']['All'], 'All')
    l.AddEntry(plot[var][iDk]['Far']['b'], 'from b (far)')
    l.AddEntry(plot[var][iDk]['Far']['noB'], 'not from b (far)')
    l.Draw()
    c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/'+var+'_'+iDk+'_b_onlyFar_'+prefix+'.png')
#
#c1.SetLogy()
#c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/dR_nob_'+prefix+'.png')
#
#c1.SetLogy()
#dRLoose_b.SetLineColor(ROOT.kRed)
#dRLoose_b.Draw()
#dRTight_b.Draw('same')
#dRLoose_nob.SetLineStyle(2)
#dRTight_nob.SetLineStyle(2)
#dRLoose_nob.SetLineColor(ROOT.kRed)
#dRLoose_nob.Draw('same')
#dRTight_nob.Draw('same')
#c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/dR_bNob_'+prefix+'.png')
#
#c1.SetLogy()
#ptRatioLoose.SetLineColor(ROOT.kRed)
#ptRatioLoose.Draw()
#ptRatioTight.Draw('same')
#c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/ptRatio_'+prefix+'.png')
#
#c1.SetLogy()
#ptRatioLoose_b.SetLineColor(ROOT.kRed)
#ptRatioLoose_b.Draw()
#ptRatioTight_b.Draw('same')
#ptRatioLoose_nob.SetLineStyle(2)
#ptRatioTight_nob.SetLineStyle(2)
#ptRatioLoose_nob.SetLineColor(ROOT.kRed)
#ptRatioLoose_nob.Draw('same')
#ptRatioTight_nob.Draw('same')
#c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/ptRatio_bNob_'+prefix+'.png')
#
#c1.SetLogy()
#muefNearLoose.SetLineColor(ROOT.kRed)
#muefNearLoose.Draw()
#muefNearTight.Draw('same')
#c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/muefNear_'+prefix+'.png')
#c1.SetLogy()
#muefFarLoose.SetLineColor(ROOT.kRed)
#muefFarLoose.Draw()
#muefFarTight.Draw('same')
#c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/muefFar_'+prefix+'.png')
#
#c1.SetLogy()
#muefNearLoose_b.SetLineColor(ROOT.kRed)
#muefNearLoose_b.Draw()
#muefNearTight_b.Draw('same')
#muefNearLoose_nob.SetLineStyle(2)
#muefNearTight_nob.SetLineStyle(2)
#muefNearLoose_nob.SetLineColor(ROOT.kRed)
#muefNearLoose_nob.Draw('same')
#muefNearTight_nob.Draw('same')
#c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/muefNear_bNob_'+prefix+'.png')
##c1.SetLogy()
##muefFarLoose_nob.SetLineColor(ROOT.kRed)
##muefFarLoose_nob.Draw()
##muefFarTight_nob.Draw('same')
##c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/muefFar_nob_'+prefix+'.png')
#c1.SetLogy()
#c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/muefNear_b_'+prefix+'.png')
##c1.SetLogy()
##muefFarLoose_b.SetLineColor(ROOT.kRed)
##muefFarLoose_b.Draw()
##muefFarTight_b.Draw('same')
##c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/muefFar_b_'+prefix+'.png')
#
#ptRatioTight_nob = ROOT.TH1F('ptRatio','lep/jet',100,0,2)
#ptRatioLoose_nob = ROOT.TH1F('ptRatio','lep/jet',100,0,2)
#muefNearTight_nob = ROOT.TH1F('muef','muef',100,0,2)
#muefNearLoose_nob = ROOT.TH1F('muef','muef',100,0,2)
#
#
c1.SetLogy(0)
c1.SetLogz(1)
ptRatioVSdRLoose.Draw('COLZ')
c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/ptRatio_vs_DR_Loose_'+prefix+'.png')
ptRatioVSdRTight.Draw('COLZ')
c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/ptRatio_vs_DR_Tight_'+prefix+'.png')
ptRatioVSdRLoose_b.Draw('COLZ')
c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/ptRatio_vs_DR_Loose_b_'+prefix+'.png')
ptRatioVSdRLoose_nob.Draw('COLZ')
c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/ptRatio_vs_DR_Loose_nob_'+prefix+'.png')


c1.SetLogy(0)
c1.SetLogz(1)
ptRatioVSptRelLoose.Draw('COLZ')
c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/ptRatio_vs_ptRel_Loose_'+prefix+'.png')
ptRatioVSptRelTight.Draw('COLZ')
c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/ptRatio_vs_ptRel_Tight_'+prefix+'.png')
ptRatioVSptRelLoose_b.Draw('COLZ')
c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/ptRatio_vs_ptRel_Loose_b_'+prefix+'.png')
ptRatioVSptRelLoose_nob.Draw('COLZ')
c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/ptRatio_vs_ptRel_Loose_nob_'+prefix+'.png')
