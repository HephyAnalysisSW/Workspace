import ROOT
import os,sys
#ROOT.gROOT.LoadMacro('/afs/hephy.at/scratch/d/dhandl/CMSSW_7_2_3/src/Workspace/HEPHYPythonTools/scripts/root/tdrstyle.C')
#ROOT.setTDRStyle()
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain

#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v6_Phys14V2_HT400_withDF import *
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v6_Phys14V2_HT400ST150_withDF import *
from Workspace.RA4Analysis.cmgTuplesPostProcessed_v8_Phys14V3_HT400ST200 import *
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName,nBTagBinName,varBinName
from rCShelpers import *
#from slidingDeltaPhi import *
import math
#from math import pi, sqrt

#ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
#ROOT.setTDRStyle()


small = False
maxN = -1 if not small else 1 

lepSel = 'hard'

cWJets  = getChain(WJetsHTToLNu[lepSel],histname='',maxN=maxN)
cTTJets = getChain(ttJets[lepSel],histname='',maxN=maxN)
#cBkg    = getChain([WJetsHTToLNu[lepSel], ttJets[lepSel], QCD[lepSel], DY[lepSel], singleTop[lepSel], TTVH[lepSel]],histname='')


from localInfo import username
uDir = username[0]+'/'+username
subDir = 'PHYS14v3/withCSV/rCS/'

path = '/afs/hephy.at/user/'+uDir+'/www/'+subDir+'/'
if not os.path.exists(path):
  os.makedirs(path)

ROOT_colors = [ROOT.kBlack, ROOT.kRed-7, ROOT.kBlue-2, ROOT.kGreen+3, ROOT.kOrange+1,ROOT.kRed-3, ROOT.kAzure+6, ROOT.kCyan+3, ROOT.kOrange , ROOT.kRed-10]
#dPhiStr = 'acos((leptonPt+met*cos(leptonPhi-metPhi))/sqrt(leptonPt**2+met**2+2*met*leptonPt*cos(leptonPhi-metPhi)))'
dPhiStr = 'deltaPhi_Wl'
#no stat box
ROOT.gStyle.SetOptStat(0)

ROOT.TH1F().SetDefaultSumw2()
#def getRCS(c, cut, dPhiCut):
#  h = getPlotFromChain(c, dPhiStr, [0,dPhiCut,pi], cutString=cut, binningIsExplicit=True)
#  if h.GetBinContent(1)>0 and h.GetBinContent(2)>0:
#    rcs = h.GetBinContent(2)/h.GetBinContent(1)
#    rcsE = rcs*sqrt(h.GetBinError(2)**2/h.GetBinContent(2)**2 + h.GetBinError(1)**2/h.GetBinContent(1)**2)
#    del h
#    return rcs, rcsE
#  else :
#    rcs =  0
#    rcsE = 0
#    return rcs, rcsE 
#    del h

streg = [[(250, 350), 1.], [(350, 450), 1.],  [(450, -1), 1.] ]
htreg = [(500,750),(750, 1000),(1000,1250),(1250,-1)]
btreg = (0,0)
njreg = [(2,2),(3,3),(4,5),(6,7),(8,-1)]#,(7,7),(8,8),(9,9)]
nbjreg = [(0,0),(1,1),(2,2)]

prefix = 'singleLeptonic_'
#presel="singleMuonic&&nVetoMuons==1&&nVetoElectrons==0&&nBJetMedium40==1"
#presel="singleMuonic&&nVetoMuons==1&&nVetoElectrons==0&&nBJetMedium25==0"
presel='singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80'

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
h_nj = {}
h_ht = {}
h_nbj = {}
h_2d = {}
for name, c in [["TT", cTTJets] , ["W",cWJets] ]:
  h_nj[name] = {}
  h_ht[name] = {}
  h_nbj[name] = {}
  h_2d[name] = {}
  for stb, dPhiCut in streg:
    h_nj[name][stb] = {}
    h_ht[name][stb] = {}
    h_nbj[name][stb] = {}
    h_2d[name][stb] = {}
    h_2d[name][stb] = ROOT.TH2F("rcs_nj_ht", "",len(njreg),0,len(njreg), len(htreg),0,len(htreg) )
    for  i_njb, njb in enumerate(njreg):
      h_ht[name][stb][njb] = ROOT.TH1F("rcs_ht", "",len(htreg),0,len(htreg))
      h_2d[name][stb].GetXaxis().SetBinLabel(i_njb+1, nJetBinName(njb)) 
      for i in range(h_ht[name][stb][njb].GetNbinsX()):
        h_ht[name][stb][njb].GetXaxis().SetBinLabel(i+1, varBinName(htreg[i],"H_{T}"))
    print 
    for i_htb, htb in enumerate(htreg): 
      h_nbj[name][stb][htb] = {}
      h_2d[name][stb].GetYaxis().SetBinLabel(i_htb+1, varBinName(htb,"H_{T}")) 
      h_nj[name][stb][htb] = ROOT.TH1F("rcs_nj", "",len(njreg),0,len(njreg))
      for i in range(h_nj[name][stb][htb].GetNbinsX()):
        h_nj[name][stb][htb].GetXaxis().SetBinLabel(i+1, nJetBinName(njreg[i]))
      for i_njb, njb in enumerate(njreg):
        cname, cut = nameAndCut(stb,htb,njb, btb=btreg ,presel=presel)
        dPhiCut = dynDeltaPhi(1.0,stb)
        rcs = getRCS(c, cut, dPhiCut)
        print rcs, dPhiCut
        res = rcs['rCS']
        resErr = rcs['rCSE_sim']
        #res, resErr = getRCS(c, cut,  dPhiCut)
        #print res,resErr, name, cname
        if not math.isnan(res):
          h_nj[name][stb][htb].SetBinContent(i_njb+1, res)
          h_nj[name][stb][htb].SetBinError(i_njb+1, resErr)
          h_ht[name][stb][njb].SetBinContent(i_htb+1, res)
          h_ht[name][stb][njb].SetBinError(i_htb+1, resErr)
          h_2d[name][stb].SetBinContent(i_njb+1, i_htb+1, res) 
          h_2d[name][stb].SetBinError(i_njb+1, i_htb+1, resErr) 
      for i_nbjb, bjb in enumerate(nbjreg):
        h_nbj[name][stb][htb][bjb] = ROOT.TH1F("rcs_nbj","",len(njreg),0,len(njreg))
        for i_njb, njb in enumerate(njreg):
          cname, cut = nameAndCut(stb,htb,njb, btb=bjb ,presel=presel)
          dPhiCut = dynDeltaPhi(1.0,stb)
          rcs = getRCS(c, cut, dPhiCut)
          print rcs, dPhiCut
          res = rcs['rCS']
          resErrPred = rcs['rCSE_pred']
          resErr = rcs['rCSE_sim']
          #res, resErr = getRCS(c, cut,  dPhiCut)
          h_nbj[name][stb][htb][bjb].GetXaxis().SetBinLabel(i_njb+1, nJetBinName(njb))
          if not math.isnan(res):
            h_nbj[name][stb][htb][bjb].SetBinContent(i_njb+1, res)
            h_nbj[name][stb][htb][bjb].SetBinError(i_njb+1, resErr) #maybe should be changed to predicted error (estimated error for poisson distributed values)


#Draw plots binned in njets for all ST and HT bins
for name, c in [["TT", cTTJets] , ["W",cWJets] ]:
  for stb, dPhiCut in streg:
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
      h_nj[name][stb][htb].GetXaxis().SetLabelSize(0.06)
      h_nj[name][stb][htb].GetYaxis().SetLabelSize(0.04)
      h_nj[name][stb][htb].GetYaxis().SetTitleSize(0.04)
      h_nj[name][stb][htb].GetYaxis().SetTitleOffset(1.5)
      h_nj[name][stb][htb].GetYaxis().SetTitle('R_{CS}')
      h_nj[name][stb][htb].GetYaxis().SetRangeUser(0, 3*h_nj[name][stb][htb].GetBinContent(h_nj[name][stb][htb].GetMaximumBin()))
#      h_nj[name][stb][htb].GetYaxis().SetRangeUser(0, 0.1)
      h_nj[name][stb][htb].SetLineColor(ROOT_colors[ihtb])
      h_nj[name][stb][htb].SetLineWidth(2)
      l.AddEntry(h_nj[name][stb][htb], varBinName(htb, 'H_{T}'))
      text=ROOT.TLatex()
      text.SetNDC()
      text.SetTextSize(0.04)
      text.SetTextAlign(11)
      text.DrawLatex(0.6,0.85,name+'+jets')
      text.DrawLatex(0.6,0.8,varBinName(stb, 'S_{T}'))
      if first:
        first = False
        h_nj[name][stb][htb].Draw()
      else:
        h_nj[name][stb][htb].Draw('same')
    l.Draw()
    c1.Print(path+prefix+'_rCS_njet_'+name+'_'+nameAndCut(stb,htb=None,njetb=None, btb=btreg, presel=presel)[0]+".png")
    h_2d[name][stb].Draw('COLZ TEXTE')
    c1.Print(path+prefix+'_rCS_njet_vs_ht_'+name+'_'+nameAndCut(stb,htb=None,njetb=None, btb=btreg, presel=presel)[0]+".png")
  for htb in htreg:
    c1 = ROOT.TCanvas('c1','c1',600,600)
    pad1 = ROOT.TPad('Pad','Pad',0.,0.0,1.,1.)
    pad1.SetLeftMargin(0.15)
    pad1.Draw()
    pad1.cd()
    first = True 
#    l = ROOT.TLegend(0.15,0.65,0.4,0.78)#left aligned legend
    l = ROOT.TLegend(0.6,0.65,0.9,0.78)#right aligned legend
    l.SetFillColor(ROOT.kWhite)
    l.SetShadowColor(ROOT.kWhite)
    l.SetBorderSize(0)
    for istb, [stb, dPhiCut] in enumerate(streg):
      h_nj[name][stb][htb].GetXaxis().SetLabelSize(0.06)
      h_nj[name][stb][htb].GetYaxis().SetLabelSize(0.04)
      h_nj[name][stb][htb].GetYaxis().SetTitleSize(0.04)
      h_nj[name][stb][htb].GetYaxis().SetTitleOffset(1.5)
      h_nj[name][stb][htb].GetYaxis().SetTitle('R_{CS}')
      h_nj[name][stb][htb].GetYaxis().SetRangeUser(0, 3*h_nj[name][stb][htb].GetBinContent(h_nj[name][stb][htb].GetMaximumBin()))
#      h_nj[name][stb][htb].GetYaxis().SetRangeUser(0, 0.1)
      h_nj[name][stb][htb].SetLineColor(ROOT_colors[istb])
      h_nj[name][stb][htb].SetLineWidth(2)
      l.AddEntry(h_nj[name][stb][htb], varBinName(stb, 'S_{T}'))
      text=ROOT.TLatex()
      text.SetNDC()
      text.SetTextSize(0.04)
      text.SetTextAlign(11)
      text.DrawLatex(0.6,0.85,name+'+jets')
      text.DrawLatex(0.6,0.8,varBinName(htb, 'H_{T}'))
      if first:
        first = False
        h_nj[name][stb][htb].Draw()
      else:
        h_nj[name][stb][htb].Draw('same')
    l.Draw()
#    c1.Print(path+prefix+'_rCS_njet_'+name+'_'+nameAndCut(stb,htb=htb,njetb=None, btb=None, presel=presel)[0]+".pdf")
    c1.Print(path+prefix+'_rCS_njet_'+name+'_'+nameAndCut(stb,htb=htb,njetb=None, btb=btreg, presel=presel)[0]+".png")
#    c1.Print(path+prefix+'_rCS_njet_'+name+'_'+nameAndCut(stb,htb=htb,njetb=None, btb=None, presel=presel)[0]+".root")


#Draw plots binned in HT for all ST and njet bins
for name, c in [ ["W",cWJets], ["TT", cTTJets]]:
  for stb, dPhiCut in streg:
    c1 = ROOT.TCanvas()
    first = True 
    l = ROOT.TLegend(0.6,0.7,0.9,0.9)
    l.SetFillColor(ROOT.kWhite)
    l.SetShadowColor(ROOT.kWhite)
    l.SetBorderSize(1)
    for injb, njb in enumerate(njreg):
      h_ht[name][stb][njb].GetXaxis().SetLabelSize(0.05)
#      h_ht[name][stb][njb].GetYaxis().SetRangeUser(0, 3*h_ht[name][stb][njb].GetBinContent(h_ht[name][stb][njb].GetMaximumBin()))
#      h_ht[name][stb][njb].GetYaxis().SetRangeUser(0, 0.1)
      h_ht[name][stb][njb].SetLineColor(ROOT_colors[injb])
      h_nj[name][stb][htb].SetLineWidth(2)
      l.AddEntry(h_ht[name][stb][njb], nJetBinName(njb))
      if first:
        first = False
        h_ht[name][stb][njb].Draw()
      else:
        h_ht[name][stb][njb].Draw('same')
    l.Draw()
    c1.Print(path+prefix+'_rCS_ht_'+name+'_'+nameAndCut(stb,htb=None,njetb=None, btb=btreg,presel=presel)[0]+".png")
  for njb in njreg:
    c1 = ROOT.TCanvas()
    first = True 
    l = ROOT.TLegend(0.6,0.7,0.9,0.9)
    l.SetFillColor(ROOT.kWhite)
    l.SetShadowColor(ROOT.kWhite)
    l.SetBorderSize(1)
    for istb, [stb, dPhiCut] in enumerate(streg):
      h_ht[name][stb][njb].GetXaxis().SetLabelSize(0.05)
#      h_ht[name][stb][njb].GetYaxis().SetRangeUser(0, 1.2*h_ht[name][stb][njb].GetBinContent(h_ht[name][stb][njb].GetMaximumBin()))
#      h_ht[name][stb][njb].GetYaxis().SetRangeUser(0, 0.1)
      h_ht[name][stb][njb].SetLineColor(ROOT_colors[istb])
      h_nj[name][stb][htb].SetLineWidth(2)
      l.AddEntry(h_ht[name][stb][njb], varBinName(stb, 'S_{T}'))
      if first:
        first = False
        h_ht[name][stb][njb].Draw()
      else:
        h_ht[name][stb][njb].Draw('same')
    l.Draw()
    c1.Print(path+prefix+'_rCS_ht_'+name+'_'+nameAndCut(stb=None,htb=None,njetb=njb,btb=btreg, presel=presel)[0]+".png")



for name, c in [["TT", cTTJets] , ["W",cWJets] ]:
  for stb, dPhiCut in streg:
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
      for inbb, nbb in enumerate(nbjreg):
        h_nbj[name][stb][htb][nbb].GetXaxis().SetLabelSize(0.06)
        h_nbj[name][stb][htb][nbb].GetYaxis().SetLabelSize(0.04)
        h_nbj[name][stb][htb][nbb].GetYaxis().SetTitleSize(0.04)
        h_nbj[name][stb][htb][nbb].GetYaxis().SetTitleOffset(1.5)
        h_nbj[name][stb][htb][nbb].GetYaxis().SetTitle('R_{CS}')
        h_nbj[name][stb][htb][nbb].GetYaxis().SetRangeUser(0, 3*h_nbj[name][stb][htb][nbb].GetBinContent(h_nbj[name][stb][htb][nbb].GetMaximumBin()))
#       h_nbj[name][stb][htb][nbb].GetYaxis().SetRangeUser(0, 0.1)
        h_nbj[name][stb][htb][nbb].SetLineColor(ROOT_colors[inbb])
        h_nbj[name][stb][htb][nbb].SetLineWidth(2)
        l.AddEntry(h_nbj[name][stb][htb][nbb], nBTagBinName(nbb))
        text=ROOT.TLatex()
        text.SetNDC()
        text.SetTextSize(0.04)
        text.SetTextAlign(11)
        text.DrawLatex(0.3,0.85,name+'+jets')
        text.DrawLatex(0.6,0.85,varBinName(htb, 'H_{T}'))
        text.DrawLatex(0.6,0.8,varBinName(stb, 'S_{T}'))
        h_nbj[name][stb][htb][nbb].Fit('pol0','','same')
        FitFunc     = h_nbj[name][stb][htb][nbb].GetFunction('pol0')
        FitPar      = FitFunc.GetParameter(0)
        FitParError = FitFunc.GetParError(0)
        FitFunc.SetLineColor(ROOT_colors[inbb])
        FitFunc.SetLineStyle(2)
        FitFunc.SetLineWidth(2)
        #rd['FitFunction']  = FitFunc
        #rd['FitParameter'] = FitPar
        #rd['FitParError']  = FitParError
        #res[htb][stb][btb] = rd        
        if first:
          first = False
          h_nbj[name][stb][htb][nbb].Draw()
        else:
          h_nbj[name][stb][htb][nbb].Draw('same')
      l.Draw()
#      c1.Print(path+prefix+'_rCS_njet_'+name+'_'+nameAndCut(stb,htb=htb,njetb=None, btb=None, presel=presel)[0]+".pdf")
      c1.Print(path+prefix+'_rCS_nbjet_'+name+'_'+nameAndCut(stb,htb=htb,njetb=None, btb=btreg, presel=presel)[0]+".png")
#      c1.Print(path+prefix+'_rCS_njet_'+name+'_'+nameAndCut(stb,htb=htb,njetb=None, btb=None, presel=presel)[0]+".root")


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
       
