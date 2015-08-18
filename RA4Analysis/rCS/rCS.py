import ROOT
import os,sys
from Workspace.HEPHYPythonTools.helpers import *
from Workspace.RA4Analysis.helpers import *# nameAndCut, nJetBinName, nBTagBinName, varBinName, varBin

#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v6_Phys14V2_HT400_withDF import *
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v6_Phys14V2_HT400ST150_withDF import *
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v8_Phys14V3_HT400ST200 import *
from Workspace.RA4Analysis.cmgTuplesPostProcessed_Spring15_hard import *
from rCShelpers import *
import math
from Workspace.RA4Analysis.signalRegions import *

#ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
#ROOT.setTDRStyle()

small = False
maxN = -1 if not small else 1 

lepSel = 'hard'

cWJets  = getChain(WJetsHTToLNu[lepSel],histname='',maxN=maxN)
#cTTJets = getChain(ttJets[lepSel],histname='',maxN=maxN)
#cBkg    = getChain([WJetsHTToLNu[lepSel], ttJets[lepSel], QCD[lepSel], DY[lepSel], singleTop[lepSel], TTVH[lepSel]],histname='')

from Workspace.HEPHYPythonTools.user import username
uDir = username[0]+'/'+username
subDir = 'Spring15/rCS/enhancedStatWithWeight2'
#subDir = 'pngCMG2/rCS/PHYS14V3/useRecoMet'

path = '/afs/hephy.at/user/'+uDir+'/www/'+subDir+'/'
if not os.path.exists(path):
  os.makedirs(path)

ROOT_colors = [ROOT.kBlack, ROOT.kRed-7, ROOT.kAzure-1, ROOT.kGreen+3, ROOT.kOrange+1,ROOT.kRed-3, ROOT.kAzure+6, ROOT.kCyan+3, ROOT.kOrange , ROOT.kRed-10]
#dPhiStr = 'acos((leptonPt+met*cos(leptonPhi-metPhi))/sqrt(leptonPt**2+met**2+2*met*leptonPt*cos(leptonPhi-metPhi)))'
dPhiStr = 'deltaPhi_Wl'
#no stat box
ROOT.gStyle.SetOptStat(0)

ROOT.TH1F().SetDefaultSumw2()

#channels = [['ele',11],['mu',13],['both',0]]
channels = [['both',0]]


channel = 'ele'
if channel == 'ele':
  pdgId = 11
elif channel =='mu':
  pdgId = 13

streg = [[(250,350),1.],[(350,450),1.],[(450,-1),1.]]#,[(350,450), 1.],[(450,-1),1.]]#, [(350, 450), 1.],  [(450, -1), 1.] ]
htreg = [(500,750),(750,1000),(1000,-1)]#,(1000,1250),(1250,-1)]#,(1250,-1)]
btreg = (0,0)
njreg = [(3,3),(4,4),(5,5),(6,7),(8,-1)]#,(7,7),(8,8),(9,9)]
nbjreg = [(0,0),(1,1),(2,2)]

#Usage of GenMet for deltaPhi / rCS
GenMetSwitch = False
useOnlyGenMetPt = False
useOnlyGenMetPhi = False

ngNuEFromW = "Sum$(abs(genPartAll_pdgId)==12&&abs(genPartAll_motherId)==24)"
ngNuMuFromW = "Sum$(abs(genPartAll_pdgId)==14&&abs(genPartAll_motherId)==24)"
ngNuTauFromW = "Sum$(abs(genPartAll_pdgId)==16&&abs(genPartAll_motherId)==24)"
l_H     = ngNuEFromW+"+"+ngNuMuFromW+"==1&&"+ngNuTauFromW+"==0"

#presel="singleMuonic&&nVetoMuons==1&&nVetoElectrons==0&&nBJetMedium40==1"
#presel="singleMuonic&&nVetoMuons==1&&nVetoElectrons==0&&nBJetMedium25==0"
#presel='singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80&&'+l_H
#presel='singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80&&Max$(abs(Jet_pt-Jet_mcPt))<50'
#presel='singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80&&(sqrt((-met_genPt*cos(met_genPhi)+met_pt*cos(met_phi))**2+(-met_genPt*sin(met_genPhi)+met_pt*sin(met_phi))**2)/met_genPt)<1'
#presel='singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80&&acos(cos(Jet_phi[0]-met_phi))>0.45&&acos(cos(Jet_phi[1]-met_phi))>0.45'
presel='singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80'
#presel='singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80&&Flag_EcalDeadCellTriggerPrimitiveFilter&&acos(cos(Jet_phi[0]-met_phi))>0.45&&acos(cos(Jet_phi[1]-met_phi))>0.45'
prefix = presel.split('&&')[0]+'_'

##2D plots of yields
#c1 = ROOT.TCanvas()
#ROOT.gStyle.SetOptStat(0)
#c1.SetGridx()
#c1.SetGridy()
#yield_2d = {}
#for name, c in [ ["W",cWJets], ["TT", cTTJets] ]:
#  yield_2d[name] = {}
#  for stb, dPhiCut in streg:
#    yield_2d[name][stb] = {}
#    yield_2d[name][stb] = ROOT.TH2F("rcs_nj_ht", "",len(njreg),0,len(njreg), len(htreg),0,len(htreg) )
#
#    for  i_njb, njb in enumerate(njreg):
#      yield_2d[name][stb].GetXaxis().SetBinLabel(i_njb+1, nJetBinName(njb)) 
#    for i_htb, htb in enumerate(htreg):
#      yield_2d[name][stb].GetYaxis().SetBinLabel(i_htb+1, varBinName(htb,"H_{T}")) 
#
#    for i_htb, htb in enumerate(htreg):
#      for i_njb, njb in enumerate(njreg):
##        h = getPlotFromChain(c, "acos((leptonPt+met*cos(leptonPhi-metPhi))/sqrt(leptonPt**2+met**2+2*met*leptonPt*cos(leptonPhi-metPhi)))", [0,dPhiCut,pi], cutString=cut, binningIsExplicit=True)
#        cname, cut = nameAndCut(stb,htb,njb, btb=(0,0), presel=presel) 
#        h = getPlotFromChain(c, "(1)",  [1,0,2], weight="weight", cutString=cut, binningIsExplicit=False)
#        res, resErr = h.GetBinContent(1) , h.GetBinError(1)
#        print 'yield', res,resErr, name, cname
#        yield_2d[name][stb].SetBinContent(i_njb+1, i_htb+1, res) 
#        yield_2d[name][stb].SetBinError(i_njb+1, i_htb+1, resErr)
#        del h 
#
#for stb, dPhiCut in streg:
#  for name, c in [ ["W",cWJets], ["TT", cTTJets]]:
#    c1 = ROOT.TCanvas()
#    ROOT.gStyle.SetPadLeftMargin(0.12)
#    ROOT.gStyle.SetPadRightMargin(0.1)
#    c1.SetGridx()
#    c1.SetGridy()
#    first = True 
#    l = ROOT.TLegend(0.1,0.75,0.4,0.9)
#    l.SetFillColor(ROOT.kWhite)
#    l.SetShadowColor(ROOT.kWhite)
#    l.SetBorderSize(1)
#    yield_2d[name][stb].Draw('COLZTEXT')
#    c1.Print('/afs/hephy.at/user/'+uDir+'/www/'+subDir+'/'+prefix+'_yield_njet_vs_ht_'+name+'_'+nameAndCut(stb,htb=None,njetb=None,btb=None, presel=presel)[0]+".png")
#  hRatio  = yield_2d['W'][stb].Clone()
#  hAll    = yield_2d['TT'][stb].Clone()
#  hAll.Add(hRatio)
#  hRatio.Divide(hAll)
#  hRatio.Draw('COLZTEXT')
#  c1.Print('/afs/hephy.at/user/'+uDir+'/www/'+subDir+'/'+prefix+'_wRatio_njet_vs_ht_'+name+'_'+nameAndCut(stb,htb=None,njetb=None, btb=None,presel=presel)[0]+".png")
#  del hRatio, hAll
  


#1D and 2D plots of RCS

h_nj_pos = {}
h_nj_neg = {}
h_nj = {}
h_ht = {}
h_nbj = {}
h_2d = {}
rcsDict = {}

for lep, pdgId in channels:
  h_nj_pos[lep] = {}
  h_nj_neg[lep] = {}
  h_nj[lep] = {}
  h_ht[lep] = {}
  h_nbj[lep] = {}
  h_2d[lep] = {}
  rcsDict[lep] = {}
  for name, c in [["W",cWJets] ]:# [["tt", cTTJets] , ["W",cWJets] ]:
    h_nj_pos[lep][name] = {}
    h_nj_neg[lep][name] = {}
    h_nj[lep][name] = {}
    h_ht[lep][name] = {}
    h_nbj[lep][name] = {}
    h_2d[lep][name] = {}
    rcsDict[lep][name] ={}
    for stb, dPhiCut in streg:
      h_nj_pos[lep][name][stb] = {}
      h_nj_neg[lep][name][stb] = {}
      h_nj[lep][name][stb] = {}
      h_ht[lep][name][stb] = {}
      h_nbj[lep][name][stb] = {}
      h_2d[lep][name][stb] = {}
      h_2d[lep][name][stb] = ROOT.TH2F("rcs_nj_ht", "",len(njreg),0,len(njreg), len(htreg),0,len(htreg) )
      rcsDict[lep][name][stb] = {}
      for  i_njb, njb in enumerate(njreg):
        h_ht[lep][name][stb][njb] = ROOT.TH1F("rcs_ht", "",len(htreg),0,len(htreg))
        h_2d[lep][name][stb].GetXaxis().SetBinLabel(i_njb+1, nJetBinName(njb)) 
        for i in range(h_ht[lep][name][stb][njb].GetNbinsX()):
          h_ht[lep][name][stb][njb].GetXaxis().SetBinLabel(i+1, varBinName(htreg[i],"H_{T}"))
      print 
      for i_htb, htb in enumerate(htreg): 
        h_nbj[lep][name][stb][htb] = {}
        h_2d[lep][name][stb].GetYaxis().SetBinLabel(i_htb+1, varBinName(htb,"H_{T}")) 
        h_nj_pos[lep][name][stb][htb] = ROOT.TH1F("rcs_nj_pos", "",len(njreg),0,len(njreg))
        h_nj_neg[lep][name][stb][htb] = ROOT.TH1F("rcs_nj_neg", "",len(njreg),0,len(njreg))
        h_nj[lep][name][stb][htb] = ROOT.TH1F("rcs_nj", "",len(njreg),0,len(njreg))
        rcsDict[lep][name][stb][htb] = {}
        for i in range(h_nj[lep][name][stb][htb].GetNbinsX()):
          h_nj[lep][name][stb][htb].GetXaxis().SetBinLabel(i+1, nJetBinName(njreg[i]))
          h_nj_pos[lep][name][stb][htb].GetXaxis().SetBinLabel(i+1, nJetBinName(njreg[i]))
          h_nj_neg[lep][name][stb][htb].GetXaxis().SetBinLabel(i+1, nJetBinName(njreg[i]))
          h_nj[lep][name][stb][htb].SetMinimum(0.)
          h_nj_pos[lep][name][stb][htb].SetMinimum(0.)
          h_nj_neg[lep][name][stb][htb].SetMinimum(0.)
        for i_njb, njb in enumerate(njreg):
          cname, cut = nameAndCut(stb,htb,njb, btb=btreg ,presel=presel)#, stVar='(leptonPt+met_genPt)')
          if lep in ['ele','mu']:
            cut = cut+'&&abs(leptonPdg)=='+str(pdgId)
          poscut = 'leptonPdg>0&&'+cut
          negcut = 'leptonPdg<0&&'+cut
          dPhiCut = dynDeltaPhi(1.0,stb, htb, njb)
          #if njb[1]<5 and njb[1]>0:
          #  dPhiJetMetCut = 0.6
          #else:
          #  dPhiJetMetCut = 0.45
          dPhiJetMetCut = 0.45
          #rcs = getRCSel(c, cut, dPhiCut, dPhiMetJet=dPhiJetMetCut)
          #rcsPos = getRCSel(c, poscut, dPhiCut, dPhiMetJet=dPhiJetMetCut)
          #rcsNeg = getRCSel(c, negcut, dPhiCut, dPhiMetJet=dPhiJetMetCut)
          rcs = getRCS(c, cut, dPhiCut, useGenMet=GenMetSwitch, useOnlyGenMetPt=useOnlyGenMetPt, useOnlyGenMetPhi=useOnlyGenMetPhi, useWeight=True)
          rcsPos = getRCS(c, poscut, dPhiCut, useGenMet=GenMetSwitch, useOnlyGenMetPt=useOnlyGenMetPt, useOnlyGenMetPhi=useOnlyGenMetPhi, useWeight=True)
          rcsNeg = getRCS(c, negcut, dPhiCut, useGenMet=GenMetSwitch, useOnlyGenMetPt=useOnlyGenMetPt, useOnlyGenMetPhi=useOnlyGenMetPhi, useWeight=True)
          print rcs, dPhiCut
          res = rcs['rCS']
          resErr = rcs['rCSE_sim']
          rcsDict[lep][name][stb][htb][njb] = {'PosPdg':rcsPos['rCS'], 'PosPdgE':rcsPos['rCSE_sim'], 'NegPdg':rcsNeg['rCS'], 'NegPdgE':rcsNeg['rCSE_sim'], 'AllPdg':res, 'AllPdgE':resErr}
          #res, resErr = getRCS(c, cut,  dPhiCut)
          #print res,resErr, name, cname
          if not math.isnan(rcsPos['rCS']):
            if rcsPos['rCS']>0.:
              h_nj_pos[lep][name][stb][htb].SetBinContent(i_njb+1, rcsPos['rCS'])
              h_nj_pos[lep][name][stb][htb].SetBinError(i_njb+1, rcsPos['rCSE_sim'])
          if not math.isnan(rcsNeg['rCS']):
            if rcsNeg['rCS']>0.:
              h_nj_neg[lep][name][stb][htb].SetBinContent(i_njb+1, rcsNeg['rCS'])
              h_nj_neg[lep][name][stb][htb].SetBinError(i_njb+1, rcsNeg['rCSE_sim'])
          if not math.isnan(res):
            if res>0.:
              h_nj[lep][name][stb][htb].SetBinContent(i_njb+1, res)
              h_nj[lep][name][stb][htb].SetBinError(i_njb+1, resErr)
            #h_ht[name][stb][njb].SetBinContent(i_htb+1, res)
            #h_ht[name][stb][njb].SetBinError(i_htb+1, resErr)
            #h_2d[name][stb].SetBinContent(i_njb+1, i_htb+1, res) 
            #h_2d[name][stb].SetBinError(i_njb+1, i_htb+1, resErr) 
        #for i_nbjb, bjb in enumerate(nbjreg):
        #  h_nbj[name][stb][htb][bjb] = ROOT.TH1F("rcs_nbj","",len(njreg),0,len(njreg))
        #  for i_njb, njb in enumerate(njreg):
        #    cname, cut = nameAndCut(stb,htb,njb, btb=bjb ,presel=presel)
        #    dPhiCut = dynDeltaPhi(1.0,stb, htb, njb)
        #    rcs = getRCS(c, cut, dPhiCut)
        #    print rcs, dPhiCut
        #    res = rcs['rCS']
        #    resErrPred = rcs['rCSE_pred']
        #    resErr = rcs['rCSE_sim']
        #    #res, resErr = getRCS(c, cut,  dPhiCut)
        #    h_nbj[name][stb][htb][bjb].GetXaxis().SetBinLabel(i_njb+1, nJetBinName(njb))
        #    if not math.isnan(res):
        #      h_nbj[name][stb][htb][bjb].SetBinContent(i_njb+1, res)
        #      h_nbj[name][stb][htb][bjb].SetBinError(i_njb+1, resErr) #maybe should be changed to predicted error (estimated error for poisson distributed values)


#Draw plots binned in njets for all ST and HT bins
for lep, pdgId in channels:
  for name, c in [["W",cWJets] ]:#[["tt", cTTJets] , ["W",cWJets] ]:
    for istb, [stb, dPhiCut] in enumerate(streg):
      c1 = ROOT.TCanvas('c1','c1',600,600)
      pad1 = ROOT.TPad('Pad','Pad',0.,0.0,1.,1.)
      pad1.SetLeftMargin(0.15)
      pad1.Draw()
      pad1.cd()
  #    c1.SetGridx()
  #    c1.SetGridy()
      first = True 
  #    l = ROOT.TLegend(0.15,0.65,0.4,0.78)#left aligned legend
      l = ROOT.TLegend(0.6,0.65,0.9,0.78)#right aligned legend
      l.SetFillColor(ROOT.kWhite)
      l.SetShadowColor(ROOT.kWhite)
      l.SetBorderSize(0)
      for ihtb, htb in enumerate(htreg):
        print ihtb, htb
        h_nj[lep][name][stb][htb].GetXaxis().SetLabelSize(0.06)
        h_nj[lep][name][stb][htb].GetYaxis().SetLabelSize(0.04)
        h_nj[lep][name][stb][htb].GetYaxis().SetTitleSize(0.04)
        h_nj[lep][name][stb][htb].GetYaxis().SetTitleOffset(1.5)
        h_nj[lep][name][stb][htb].GetYaxis().SetTitle('R_{CS}')
        h_nj[lep][name][stb][htb].GetYaxis().SetRangeUser(0, 3*h_nj[lep][name][stb][htb].GetBinContent(h_nj[lep][name][stb][htb].GetMaximumBin()))
        upperbound = 0
        for i_njb, njb in enumerate(njreg):
          if h_nj[lep][name][stb][htb].GetBinContent(i_njb+1)>0.:
            upperbound = i_njb+1
          else:
            break
        h_nj[lep][name][stb][htb].Fit('pol1','','same',0,upperbound)
        FitFunc     = h_nj[lep][name][stb][htb].GetFunction('pol1')
        FitParD     = FitFunc.GetParameter(0)
        FitParDError = FitFunc.GetParError(0)
        FitParK = FitFunc.GetParameter(1)
        FitParKError = FitFunc.GetParError(1)
        FitFunc.SetLineColor(ROOT_colors[ihtb])
        FitFunc.SetLineStyle(2)
        FitFunc.SetLineWidth(2)
        rcsDict[lep][name][stb][htb].update({'D':FitParD, 'DErr':FitParDError, 'K':FitParK, 'Kerr':FitParKError})
        if name == 'tt':
          h_nj[lep][name][stb][htb].SetMaximum(0.25)
        else:
          h_nj[lep][name][stb][htb].SetMaximum(0.08)
  #      h_nj[name][stb][htb].GetYaxis().SetRangeUser(0, 0.1)
        h_nj[lep][name][stb][htb].SetLineColor(ROOT_colors[ihtb])
        h_nj[lep][name][stb][htb].SetLineWidth(2)
        l.AddEntry(h_nj[lep][name][stb][htb], varBinName(htb, 'H_{T}'))
        text=ROOT.TLatex()
        text.SetNDC()
        text.SetTextSize(0.04)
        text.SetTextAlign(11)
        text.DrawLatex(0.6,0.85,name+'+jets')
        text.DrawLatex(0.6,0.8,varBinName(stb, 'S_{T}'))
        if first:
          first = False
          h_nj[lep][name][stb][htb].Draw()
        else:
          h_nj[lep][name][stb][htb].Draw('same')
        text.DrawLatex(0.4,0.75-0.05*ihtb,str(round(FitParK*1000,2))+'#pm'+str(round(FitParKError*1000,2)))
        FitFunc.Draw("same")
      l.Draw()
      c1.Print(path+prefix+'_rCS_njet_'+lep+'_'+name+'_'+nameAndCut(stb,htb=None,njetb=None, btb=btreg, presel=presel)[0]+".pdf")
      c1.Print(path+prefix+'_rCS_njet_'+lep+'_'+name+'_'+nameAndCut(stb,htb=None,njetb=None, btb=btreg, presel=presel)[0]+".png")
      c1.Print(path+prefix+'_rCS_njet_'+lep+'_'+name+'_'+nameAndCut(stb,htb=None,njetb=None, btb=btreg, presel=presel)[0]+".root")
      h_2d[lep][name][stb].Draw('COLZ TEXTE')
      c1.Print(path+prefix+'_rCS_njet_vs_ht_'+lep+'_'+name+'_'+nameAndCut(stb,htb=None,njetb=None, btb=btreg, presel=presel)[0]+".png")
    for htb in htreg:
      c1 = ROOT.TCanvas('c1','c1',600,600)
      pad1 = ROOT.TPad('Pad','Pad',0.,0.0,1.,1.)
      pad1.SetLeftMargin(0.15)
      pad1.Draw()
      pad1.cd()
      first = True 
      l = ROOT.TLegend(0.6,0.65,0.9,0.78)#right aligned legend
      l.SetFillColor(ROOT.kWhite)
      l.SetShadowColor(ROOT.kWhite)
      l.SetBorderSize(0)
      for istb, [stb, dPhiCut] in enumerate(streg):
        h_nj[lep][name][stb][htb].GetXaxis().SetLabelSize(0.06)
        h_nj[lep][name][stb][htb].GetYaxis().SetLabelSize(0.04)
        h_nj[lep][name][stb][htb].GetYaxis().SetTitleSize(0.04)
        h_nj[lep][name][stb][htb].GetYaxis().SetTitleOffset(1.5)
        h_nj[lep][name][stb][htb].GetYaxis().SetTitle('R_{CS}')
        h_nj[lep][name][stb][htb].GetYaxis().SetRangeUser(0, 3*h_nj[lep][name][stb][htb].GetBinContent(h_nj[lep][name][stb][htb].GetMaximumBin()))
        FitFunc     = h_nj[lep][name][stb][htb].GetFunction('pol1')
        FitParD     = FitFunc.GetParameter(0)
        FitParDError = FitFunc.GetParError(0)
        FitParK = FitFunc.GetParameter(1)
        FitParKError = FitFunc.GetParError(1)
        FitFunc.SetLineColor(ROOT_colors[istb])
        FitFunc.SetLineStyle(2)
        FitFunc.SetLineWidth(2)
        if name == 'tt':
          h_nj[lep][name][stb][htb].SetMaximum(0.25)
        else:
          h_nj[lep][name][stb][htb].SetMaximum(0.08)
  #      h_nj[name][stb][htb].GetYaxis().SetRangeUser(0, 0.1)
        h_nj[lep][name][stb][htb].SetLineColor(ROOT_colors[istb])
        h_nj[lep][name][stb][htb].SetLineWidth(2)
        l.AddEntry(h_nj[lep][name][stb][htb], varBinName(stb, 'S_{T}'))
        text=ROOT.TLatex()
        text.SetNDC()
        text.SetTextSize(0.04)
        text.SetTextAlign(11)
        text.DrawLatex(0.6,0.85,name+'+jets')
        text.DrawLatex(0.6,0.8,varBinName(htb, 'H_{T}'))
        if first:
          first = False
          h_nj[lep][name][stb][htb].Draw()
        else:
          h_nj[lep][name][stb][htb].Draw('same')
        text.DrawLatex(0.4,0.75-0.05*istb,str(round(FitParK*1000,2))+'#pm'+str(round(FitParKError*1000,2)))
      l.Draw()
      c1.Print(path+prefix+'_rCS_njet_'+lep+'_'+name+'_'+nameAndCut(stb,htb=htb,njetb=None, btb=btreg, presel=presel)[0]+".pdf")
      c1.Print(path+prefix+'_rCS_njet_'+lep+'_'+name+'_'+nameAndCut(stb,htb=htb,njetb=None, btb=btreg, presel=presel)[0]+".png")
      c1.Print(path+prefix+'_rCS_njet_'+lep+'_'+name+'_'+nameAndCut(stb,htb=htb,njetb=None, btb=btreg, presel=presel)[0]+".root")
#  for name, c in [["tt", cTTJets] , ["W",cWJets] ]:
#    for htb in htreg:
#      c1 = ROOT.TCanvas('c1','c1',600,600)
#      pad1 = ROOT.TPad('Pad','Pad',0.,0.0,1.,1.)
#      pad1.SetLeftMargin(0.15)
#      pad1.Draw()
#      pad1.cd()
#      first = True
#      l = ROOT.TLegend(0.6,0.65,0.9,0.78)#right aligned legend
#      l.SetFillColor(ROOT.kWhite)
#      l.SetShadowColor(ROOT.kWhite)
#      l.SetBorderSize(0)
#      for istb, [stb, dPhiCut] in enumerate(streg):
#        h_nj_pos[lep][name][stb][htb].GetXaxis().SetLabelSize(0.06)
#        h_nj_pos[lep][name][stb][htb].GetYaxis().SetLabelSize(0.04)
#        h_nj_pos[lep][name][stb][htb].GetYaxis().SetTitleSize(0.04)
#        h_nj_pos[lep][name][stb][htb].GetYaxis().SetTitleOffset(1.5)
#        h_nj_pos[lep][name][stb][htb].GetYaxis().SetTitle('R_{CS}')
#        h_nj_pos[lep][name][stb][htb].GetYaxis().SetRangeUser(0, 3*h_nj[lep][name][stb][htb].GetBinContent(h_nj[lep][name][stb][htb].GetMaximumBin()))
#        upperbound = 0
#        for i_njb, njb in enumerate(njreg):
#          if h_nj_pos[lep][name][stb][htb].GetBinContent(i_njb+1)>0.:
#            upperbound = i_njb+1
#          else:
#            break
#        h_nj_pos[lep][name][stb][htb].Fit('pol1','','same',0,upperbound)
#        FitFunc     = h_nj_pos[lep][name][stb][htb].GetFunction('pol1')
#        FitParD     = FitFunc.GetParameter(0)
#        FitParDError = FitFunc.GetParError(0)
#        FitParK = FitFunc.GetParameter(1)
#        FitParKError = FitFunc.GetParError(1)
#        FitFunc.SetLineColor(ROOT_colors[istb])
#        FitFunc.SetLineStyle(2)
#        FitFunc.SetLineWidth(2)
#        #rcsDict[lep][name][stb][htb].update({'D':FitParD, 'DErr':FitParDError, 'K':FitParK, 'Kerr':FitParKError})
#        if name == 'tt':
#          h_nj_pos[lep][name][stb][htb].SetMaximum(0.25)
#        else:
#          h_nj_pos[lep][name][stb][htb].SetMaximum(0.08)
#        h_nj_pos[lep][name][stb][htb].SetLineColor(ROOT_colors[istb])
#        h_nj_pos[lep][name][stb][htb].SetLineWidth(2)
#        l.AddEntry(h_nj_pos[lep][name][stb][htb], varBinName(stb, 'S_{T}'))
#        text=ROOT.TLatex()
#        text.SetNDC()
#        text.SetTextSize(0.04)
#        text.SetTextAlign(11)
#        text.DrawLatex(0.6,0.85,name+'+jets, - Charge')
#        text.DrawLatex(0.6,0.8,varBinName(htb, 'H_{T}'))
#        if first:
#          first = False
#          h_nj_pos[lep][name][stb][htb].Draw()
#        else:
#          h_nj_pos[lep][name][stb][htb].Draw('same')
#        text.DrawLatex(0.4,0.75-0.05*istb,str(round(FitParK*1000,2))+'#pm'+str(round(FitParKError*1000,2)))
#        FitFunc.Draw('same')
#      l.Draw()
#      c1.Print(path+prefix+'_rCS_njet_PosPDG_'+lep+'_'+name+'_'+nameAndCut(stb,htb=htb,njetb=None, btb=btreg, presel=presel)[0]+".pdf")
#      c1.Print(path+prefix+'_rCS_njet_PosPDG_'+lep+'_'+name+'_'+nameAndCut(stb,htb=htb,njetb=None, btb=btreg, presel=presel)[0]+".png")
#      c1.Print(path+prefix+'_rCS_njet_PosPDG_'+lep+'_'+name+'_'+nameAndCut(stb,htb=htb,njetb=None, btb=btreg, presel=presel)[0]+".root")
#  for name, c in [["tt", cTTJets] , ["W",cWJets] ]:
#    for htb in htreg:
#      c1 = ROOT.TCanvas('c1','c1',600,600)
#      pad1 = ROOT.TPad('Pad','Pad',0.,0.0,1.,1.)
#      pad1.SetLeftMargin(0.15)
#      pad1.Draw()
#      pad1.cd()
#      first = True
#      l = ROOT.TLegend(0.6,0.65,0.9,0.78)#right aligned legend
#      l.SetFillColor(ROOT.kWhite)
#      l.SetShadowColor(ROOT.kWhite)
#      l.SetBorderSize(0)
#      for istb, [stb, dPhiCut] in enumerate(streg):
#        h_nj_neg[lep][name][stb][htb].GetXaxis().SetLabelSize(0.06)
#        h_nj_neg[lep][name][stb][htb].GetYaxis().SetLabelSize(0.04)
#        h_nj_neg[lep][name][stb][htb].GetYaxis().SetTitleSize(0.04)
#        h_nj_neg[lep][name][stb][htb].GetYaxis().SetTitleOffset(1.5)
#        h_nj_neg[lep][name][stb][htb].GetYaxis().SetTitle('R_{CS}')
#        h_nj_neg[lep][name][stb][htb].Fit('pol1','','same',0,upperbound)
#        upperbound = 0
#        for i_njb, njb in enumerate(njreg):
#          if h_nj_neg[lep][name][stb][htb].GetBinContent(i_njb+1)>0.:
#            upperbound = i_njb+1
#          else:
#            break
#        FitFunc     = h_nj_neg[lep][name][stb][htb].GetFunction('pol1')
#        FitParD     = FitFunc.GetParameter(0)
#        FitParDError = FitFunc.GetParError(0)
#        FitParK = FitFunc.GetParameter(1)
#        FitParKError = FitFunc.GetParError(1)
#        FitFunc.SetLineColor(ROOT_colors[istb])
#        FitFunc.SetLineStyle(2)
#        FitFunc.SetLineWidth(2)
#        rcsDict[lep][name][stb][htb].update({'D':FitParD, 'DErr':FitParDError, 'K':FitParK, 'Kerr':FitParKError})
#        if name == 'tt':
#          h_nj_neg[lep][name][stb][htb].SetMaximum(0.25)
#        else:
#          h_nj_neg[lep][name][stb][htb].SetMaximum(0.08)
#        FitFunc.Draw('same')
#        h_nj_neg[lep][name][stb][htb].SetLineColor(ROOT_colors[istb])
#        h_nj_neg[lep][name][stb][htb].SetLineWidth(2)
#        l.AddEntry(h_nj_neg[lep][name][stb][htb], varBinName(stb, 'S_{T}'))
#        text=ROOT.TLatex()
#        text.SetNDC()
#        text.SetTextSize(0.04)
#        text.SetTextAlign(11)
#        text.DrawLatex(0.6,0.85,name+'+jets, + Charge')
#        text.DrawLatex(0.6,0.8,varBinName(htb, 'H_{T}'))
#        if first:
#          first = False
#          h_nj_neg[lep][name][stb][htb].Draw()
#        else:
#          h_nj_neg[lep][name][stb][htb].Draw('same')
#        
#        text.DrawLatex(0.4,0.75-0.05*istb,str(round(FitParK*1000,2))+'#pm'+str(round(FitParKError*1000,2)))
#      l.Draw()
#      c1.Print(path+prefix+'_rCS_njet_NegPDG_'+lep+'_'+name+'_'+nameAndCut(stb,htb=htb,njetb=None, btb=btreg, presel=presel)[0]+".pdf")
#      c1.Print(path+prefix+'_rCS_njet_NegPDG_'+lep+'_'+name+'_'+nameAndCut(stb,htb=htb,njetb=None, btb=btreg, presel=presel)[0]+".png")
#      c1.Print(path+prefix+'_rCS_njet_NegPDG_'+lep+'_'+name+'_'+nameAndCut(stb,htb=htb,njetb=None, btb=btreg, presel=presel)[0]+".root")

##Draw plots binned in HT for all ST and njet bins
#for name, c in [ ["W",cWJets], ["tt", cTTJets]]:
#  for stb, dPhiCut in streg:
#    c1 = ROOT.TCanvas()
#    first = True 
#    l = ROOT.TLegend(0.6,0.7,0.9,0.9)
#    l.SetFillColor(ROOT.kWhite)
#    l.SetShadowColor(ROOT.kWhite)
#    l.SetBorderSize(1)
#    for injb, njb in enumerate(njreg):
#      h_ht[name][stb][njb].GetXaxis().SetLabelSize(0.05)
##      h_ht[name][stb][njb].GetYaxis().SetRangeUser(0, 3*h_ht[name][stb][njb].GetBinContent(h_ht[name][stb][njb].GetMaximumBin()))
##      h_ht[name][stb][njb].GetYaxis().SetRangeUser(0, 0.1)
#      h_ht[name][stb][njb].SetLineColor(ROOT_colors[injb])
#      h_nj[name][stb][htb].SetLineWidth(2)
#      l.AddEntry(h_ht[name][stb][njb], nJetBinName(njb))
#      if first:
#        first = False
#        h_ht[name][stb][njb].Draw()
#      else:
#        h_ht[name][stb][njb].Draw('same')
#    l.Draw()
#    c1.Print(path+prefix+'_rCS_ht_'+name+'_'+nameAndCut(stb,htb=None,njetb=None, btb=btreg,presel=presel)[0]+".png")
#  for njb in njreg:
#    c1 = ROOT.TCanvas()
#    first = True 
#    l = ROOT.TLegend(0.6,0.7,0.9,0.9)
#    l.SetFillColor(ROOT.kWhite)
#    l.SetShadowColor(ROOT.kWhite)
#    l.SetBorderSize(1)
#    for istb, [stb, dPhiCut] in enumerate(streg):
#      h_ht[name][stb][njb].GetXaxis().SetLabelSize(0.05)
##      h_ht[name][stb][njb].GetYaxis().SetRangeUser(0, 1.2*h_ht[name][stb][njb].GetBinContent(h_ht[name][stb][njb].GetMaximumBin()))
##      h_ht[name][stb][njb].GetYaxis().SetRangeUser(0, 0.1)
#      h_ht[name][stb][njb].SetLineColor(ROOT_colors[istb])
#      h_nj[name][stb][htb].SetLineWidth(2)
#      l.AddEntry(h_ht[name][stb][njb], varBinName(stb, 'S_{T}'))
#      if first:
#        first = False
#        h_ht[name][stb][njb].Draw()
#      else:
#        h_ht[name][stb][njb].Draw('same')
#    l.Draw()
#    c1.Print(path+prefix+'_rCS_ht_'+name+'_'+nameAndCut(stb=None,htb=None,njetb=njb,btb=btreg, presel=presel)[0]+".png")



#for name, c in [["tt", cTTJets] , ["W",cWJets] ]:
#  for stb, dPhiCut in streg:
#    for htb in htreg:
#      c1 = ROOT.TCanvas('c1','c1',600,600)
#      pad1 = ROOT.TPad('Pad','Pad',0.,0.0,1.,1.)
#      pad1.SetLeftMargin(0.15)
#      pad1.Draw()
#      pad1.cd()
#      first = True
#      l = ROOT.TLegend(0.6,0.65,0.9,0.78)#right aligned legend
#      l.SetFillColor(ROOT.kWhite)
#      l.SetShadowColor(ROOT.kWhite)
#      l.SetBorderSize(0)
#      FitParList = {}
#      FitParErrorList = {}
#      for inbb, nbb in enumerate(reversed(nbjreg)):
#        h_nbj[name][stb][htb][nbb].GetXaxis().SetLabelSize(0.06)
#        h_nbj[name][stb][htb][nbb].GetYaxis().SetLabelSize(0.04)
#        h_nbj[name][stb][htb][nbb].GetYaxis().SetTitleSize(0.04)
#        h_nbj[name][stb][htb][nbb].GetYaxis().SetTitleOffset(1.5)
#        h_nbj[name][stb][htb][nbb].GetYaxis().SetTitle('R_{CS}')
#        h_nbj[name][stb][htb][nbb].SetMaximum(0.25)
#        #h_nbj[name][stb][htb][nbb].GetYaxis().SetRangeUser(0, 3*h_nbj[name][stb][htb][nbb].GetBinContent(h_nbj[name][stb][htb][nbb].GetMaximumBin()))
#        h_nbj[name][stb][htb][nbb].SetLineColor(ROOT_colors[inbb])
#        h_nbj[name][stb][htb][nbb].SetLineWidth(2)
#        l.AddEntry(h_nbj[name][stb][htb][nbb], nBTagBinName(nbb))
#        text=ROOT.TLatex()
#        text.SetNDC()
#        text.SetTextSize(0.04)
#        text.SetTextAlign(11)
#        text.DrawLatex(0.3,0.85,name+'+jets')
#        text.DrawLatex(0.6,0.85,varBinName(htb, 'H_{T}'))
#        text.DrawLatex(0.6,0.8,varBinName(stb, 'S_{T}'))
#        h_nbj[name][stb][htb][nbb].Fit('pol0','','same',2,6)
#        FitFunc     = h_nbj[name][stb][htb][nbb].GetFunction('pol0')
#        FitPar      = FitFunc.GetParameter(0)
#        FitParError = FitFunc.GetParError(0)
#        FitFunc.SetLineColor(ROOT_colors[inbb])
#        FitFunc.SetLineStyle(2)
#        FitFunc.SetLineWidth(2)
#        FitParList.update({nbb:FitPar})
#        FitParErrorList.update({nbb:FitParError})
#        if first:
#          first = False
#          h_nbj[name][stb][htb][nbb].Draw()
#        else:
#          h_nbj[name][stb][htb][nbb].Draw('same')
#        FitFunc.Draw("same")
#      FitRatio = FitParList[(0,0)]/FitParList[(1,1)]
#      FitRatioError = FitRatio*sqrt((FitParErrorList[(0,0)]/FitParList[(0,0)])**2+(FitParErrorList[(1,1)]/FitParList[(1,1)])**2)
#      Etext=ROOT.TLatex()
#      Etext.SetNDC()
#      Etext.SetTextSize(0.04)
#      Etext.SetTextAlign(11)
#      Etext.DrawLatex(0.18,0.75,'Fit(0b/1b)='+str(round(FitRatio,3))+'#pm'+str(round(FitRatioError,4)))
#      l.Draw()
#      c1.Print(path+prefix+'_rCS_nbjet_'+name+'_'+nameAndCut(stb,htb=htb,njetb=None, btb=btreg, presel=presel)[0]+".pdf")
#      c1.Print(path+prefix+'_rCS_nbjet_'+name+'_'+nameAndCut(stb,htb=htb,njetb=None, btb=btreg, presel=presel)[0]+".png")


#1D and 2D plots of RCS vs nBTag for TTJets
#prefix = 'Phys14_hardSingleMuonic' 
#presel = 'singleMuonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0'
#btreg = [(0,0), (1,1), (2,-1)]
#njreg = [(2,3),(4,4),(5,5),(6,-1)]
#h_btb={}
#for name, c in [  ["TT", cTTJets] ]:
#  h_btb[name]={}
#  for stb, dPhiCut in streg:
#    h_btb[name][stb]={}
#    for i_htb, htb in enumerate(htreg):
#      h_btb[name][stb][htb]={}
#      for i_njb, njb in enumerate(njreg):
#        h_btb[name][stb][htb][njb] = ROOT.TH1F("rcs_btag", "",len(btreg),0,len(btreg))
#        for i in range(h_btb[name][stb][htb][njb].GetNbinsX()):
#          h_btb[name][stb][htb][njb].GetXaxis().SetBinLabel(i+1, nBTagBinName(btreg[i]))
#        for i_btb, btb in enumerate(btreg):
#          cname, cut = nameAndCut(stb,htb,njb,btb=btb, presel=presel) 
#          res, resErr = getRCS(c, cut,  dPhiCut)
#          print res,resErr, name, cname
#          if res:
#            h_btb[name][stb][htb][njb].SetBinContent(i_btb+1, res)
#            h_btb[name][stb][htb][njb].SetBinError(i_btb+1, resErr)
#
#c1 = ROOT.TCanvas()
#ROOT.gStyle.SetOptStat(0)
##c1.SetGridx()
##c1.SetGridy()
#for name, c in [["TT", cTTJets] ]:
#  for stb, dPhiCut in streg:
#    c1 = ROOT.TCanvas('c1','c1',600,600)
##    c1.SetGridx()
##    c1.SetGridy()
#    pad1 = ROOT.TPad('Pad','Pad',0.,0.0,1.,1.)
#    pad1.SetLeftMargin(0.15)
#    pad1.Draw()
#    pad1.cd()
#    for ihtb, htb in enumerate(htreg):
#      first = True
#      l = ROOT.TLegend(0.65,0.75,0.9,0.89)
#      l.SetFillColor(ROOT.kWhite)
#      l.SetShadowColor(ROOT.kWhite)
#      l.SetBorderSize(0)
#      for i_njb, njb in enumerate(njreg):
#        h_btb[name][stb][htb][njb].GetXaxis().SetLabelSize(0.06)
#        h_btb[name][stb][htb][njb].GetYaxis().SetLabelSize(0.04)
#        h_btb[name][stb][htb][njb].GetYaxis().SetTitleSize(0.04)
#        h_btb[name][stb][htb][njb].GetYaxis().SetTitleOffset(1.5)
#        h_btb[name][stb][htb][njb].GetYaxis().SetTitle('R_{CS}')
#  #      h_btb[name][stb][htb].GetYaxis().SetRangeUser(0, 1.2*h_btb[name][stb][htb].GetBinContent(h_btb[name][stb][htb].GetMaximumBin()))
#        h_btb[name][stb][htb][njb].GetYaxis().SetRangeUser(0, 0.1)
#        h_btb[name][stb][htb][njb].SetLineColor(ROOT_colors[i_njb])
#        h_btb[name][stb][htb][njb].SetLineWidth(2)
#        l.AddEntry(h_btb[name][stb][htb][njb],  nJetBinName(njb))
#        text=ROOT.TLatex()
#        text.SetNDC()
#        text.SetTextSize(0.04)
#        text.SetTextAlign(11)
#        text.DrawLatex(0.2,0.85,name+'+jets')
#        text.DrawLatex(0.2,0.8,varBinName(stb, 'S_{T}'))
#        text.DrawLatex(0.2,0.75,varBinName(htb, 'H_{T}'))
#        if first:
#          first = False
#          h_btb[name][stb][htb][njb].Draw()
#        else:
#          h_btb[name][stb][htb][njb].Draw('same')
#      l.Draw()
#      c1.Print('/afs/hephy.at/user/'+uDir+'/www/'+subDir+'/'+prefix+'_rCS_nbtag_'+name+'_'+nameAndCut(stb,htb=htb,njetb=None, btb=None, presel=presel)[0]+".pdf")
#      c1.Print('/afs/hephy.at/user/'+uDir+'/www/'+subDir+'/'+prefix+'_rCS_nbtag_'+name+'_'+nameAndCut(stb,htb=htb,njetb=None, btb=None, presel=presel)[0]+".png")
#      c1.Print('/afs/hephy.at/user/'+uDir+'/www/'+subDir+'/'+prefix+'_rCS_nbtag_'+name+'_'+nameAndCut(stb,htb=htb,njetb=None, btb=None, presel=presel)[0]+".root")


## W Prediction RCS table stability check
#
#p = 'W'
#print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|rrr|rrr|rrr|rrr|rrr|rrr|rrr|c|c|}\\hline'
#print ' \ST & \HT & \\njet & \multicolumn{9}{c|}{- charge} & \multicolumn{9}{c|}{+ charge} & \multicolumn{9}{c|}{all} & \multicolumn{2}{c|}{Fit}\\\%\hline'
#print '  $[$GeV$]$ & $[$GeV$]$ & & \multicolumn{3}{c}{e} & \multicolumn{3}{c}{$\mu$} & \multicolumn{3}{c|}{both} & \multicolumn{3}{c}{e} & \multicolumn{3}{c}{$\mu$} & \multicolumn{3}{c|}{both}'\
#        + '& \multicolumn{3}{c}{e} & \multicolumn{3}{c}{$\mu$} & \multicolumn{3}{c|}{both} & \multicolumn{1}{c}{K} & \multicolumn{1}{c|}{D} \\\\\hline '
#secondLine = False
#for stb, dPhiCut in streg:
#  print '\\hline'
#  if secondLine: print '\\hline'
#  secondLine = True
#  print '\multirow{21}{*}{\\begin{sideways}$'+varBin(stb)+'$\end{sideways}}'
#  for ihtb, htb in enumerate(htreg):
#    print '&\multirow{7}{*}{\\begin{sideways}$'+varBin(htb)+'$\end{sideways}}'
#    first = True
#    for injb, njb in enumerate(njreg):
#      if not first: print '&'
#      print '&$'+varBin(njb)+'$&'
#      print  ' & '.join([getNumString(rcsDict['ele'][p][stb][htb][njb]['PosPdg'], rcsDict['ele'][p][stb][htb][njb]['PosPdgE'],4), \
#                         getNumString(rcsDict['mu'][p][stb][htb][njb]['PosPdg'], rcsDict['mu'][p][stb][htb][njb]['PosPdgE'],4), \
#                         getNumString(rcsDict['both'][p][stb][htb][njb]['PosPdg'], rcsDict['both'][p][stb][htb][njb]['PosPdgE'],4),\
#                         getNumString(rcsDict['ele'][p][stb][htb][njb]['NegPdg'], rcsDict['ele'][p][stb][htb][njb]['NegPdgE'],4), \
#                         getNumString(rcsDict['mu'][p][stb][htb][njb]['NegPdg'], rcsDict['mu'][p][stb][htb][njb]['NegPdgE'],4), \
#                         getNumString(rcsDict['both'][p][stb][htb][njb]['NegPdg'], rcsDict['both'][p][stb][htb][njb]['NegPdgE'],4),\
#                         getNumString(rcsDict['ele'][p][stb][htb][njb]['AllPdg'], rcsDict['ele'][p][stb][htb][njb]['AllPdgE'],4), \
#                         getNumString(rcsDict['mu'][p][stb][htb][njb]['AllPdg'], rcsDict['mu'][p][stb][htb][njb]['AllPdgE'],4), \
#                         getNumString(rcsDict['both'][p][stb][htb][njb]['AllPdg'], rcsDict['both'][p][stb][htb][njb]['AllPdgE'],4)])
#      if first:
#        print '&\multirow{7}{*}{$' + str(round(rcsDict['both'][p][stb][htb]['K']*1000,2)) + '\pm' + str(round(rcsDict['both'][p][stb][htb]['Kerr']*1000,2)) +'$}'
#        print '&\multirow{7}{*}{$' + str(round(rcsDict['both'][p][stb][htb]['D'],4)) + '\pm' + str(round(rcsDict['both'][p][stb][htb]['DErr'],4)) +'$} \\\\'
#      else:
#        print '&&\\\\'
#      first = False
#      if njb[1] == -1 : print '\\cline{2-32}'
#print '\\hline\end{tabular}}\end{center}\caption{RCS stability for tt jets}\end{table}'
      
