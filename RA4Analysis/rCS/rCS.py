import ROOT
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain
from Workspace.RA4Analysis.cmgTuplesPostProcessed import * 
cWJets  = getChain(WJetsHTToLNu)
cTTJets = getChain(ttJetsCSA1450ns)
cSignal1200 = getChain(T5Full_1200_1000_800)
cSignal1500 = getChain(T5Full_1500_800_100)
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName,nBTagBinName,varBinName
from math import pi, sqrt
from localInfo import username
uDir = username[0]+'/'+username
subDir = 'pngCMG'

ROOT_colors = [ROOT.kBlack, ROOT.kRed-7, ROOT.kBlue-2, ROOT.kGreen+3, ROOT.kOrange+1,ROOT.kRed-3, ROOT.kAzure+6, ROOT.kCyan+3, ROOT.kOrange , ROOT.kRed-10]

ROOT.TH1F().SetDefaultSumw2()
def getRCS(c, cut, dPhiCut):
  h = getPlotFromChain(c, "acos((leptonPt+met*cos(leptonPhi-metPhi))/sqrt(leptonPt**2+met**2+2*met*leptonPt*cos(leptonPhi-metPhi)))", [0,dPhiCut,pi], cutString=cut, binningIsExplicit=True)
  if h.GetBinContent(1)>0 and h.GetBinContent(2)>0:
    rcs = h.GetBinContent(2)/h.GetBinContent(1)
    rcsE = rcs*sqrt(h.GetBinError(2)**2/h.GetBinContent(2)**2 + h.GetBinError(1)**2/h.GetBinContent(1)**2)
    del h
    return rcs, rcsE
  del h
  return None, None

#streg = [[(250, 350), 1.], [(350, 450), 1.], [(450, -1), 0.5]]
#htreg = [(400,500),(500,750),(750, 1000),(1000,-1)]
#njreg = [(1,1), (2,2),(3,3),(4,4),(5,5),(6,-1)]

streg = [[(250, 350), 1.], [(350, -1), 1.]]
htreg = [(400,500),(500,750),(750, -1)]
njreg = [(2,2),(3,3),(4,4),(5,-1),(6,-1)]


prefix = 'reduced'
#presel="singleMuonic&&nVetoMuons==1&&nVetoElectrons==0&&nBJetMedium40==1"
presel="singleMuonic&&nVetoMuons==1&&nVetoElectrons==0&&nBJetMedium25==0"

##2D plots of yields
#c1 = ROOT.TCanvas()
#ROOT.gStyle.SetOptStat(0)
#c1.SetGridx()
#c1.SetGridy()
#yield_2d = {}
#for name, c in [ ["W",cWJets], ["TT", cTTJets] , ["Sig1200", cSignal1200], ["Sig1500", cSignal1500] ]:
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
#        cname, cut = nameAndCut(stb,htb,njb, btb=None, presel=presel) 
#        h = getPlotFromChain(c, "(1)",  [1,0,2], weight="weight", cutString=cut, binningIsExplicit=False)
#        res, resErr = h.GetBinContent(1) , h.GetBinError(1)
#        print 'yield', res,resErr, name, cname
#        yield_2d[name][stb].SetBinContent(i_njb+1, i_htb+1, res) 
#        yield_2d[name][stb].SetBinError(i_njb+1, i_htb+1, resErr)
#        del h 
#
#for stb, dPhiCut in streg:
#  for name, c in [ ["W",cWJets], ["TT", cTTJets], ["Sig1200", cSignal1200], ["Sig1500", cSignal1500]]:
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
h_2d = {}
for name, c in [ ["W",cWJets], ["TT", cTTJets] ]:
  h_nj[name] = {}
  h_ht[name] = {}
  h_2d[name] = {}
  for stb, dPhiCut in streg:
    h_nj[name][stb] = {}
    h_ht[name][stb] = {}
    h_2d[name][stb] = {}
    h_2d[name][stb] = ROOT.TH2F("rcs_nj_ht", "",len(njreg),0,len(njreg), len(htreg),0,len(htreg) )
    for  i_njb, njb in enumerate(njreg):
      h_ht[name][stb][njb] = ROOT.TH1F("rcs_ht", "",len(htreg),0,len(htreg))
      h_2d[name][stb].GetXaxis().SetBinLabel(i_njb+1, nJetBinName(njb)) 
      for i in range(h_ht[name][stb][njb].GetNbinsX()):
        h_ht[name][stb][njb].GetXaxis().SetBinLabel(i+1, varBinName(htreg[i],"H_{T}"))
    print 
    for i_htb, htb in enumerate(htreg):
      print 
      h_2d[name][stb].GetYaxis().SetBinLabel(i_htb+1, varBinName(htb,"H_{T}")) 
      h_nj[name][stb][htb] = ROOT.TH1F("rcs_nj", "",len(njreg),0,len(njreg))
      for i in range(h_nj[name][stb][htb].GetNbinsX()):
        h_nj[name][stb][htb].GetXaxis().SetBinLabel(i+1, nJetBinName(njreg[i]))
      for i_njb, njb in enumerate(njreg):
        cname, cut = nameAndCut(stb,htb,njb, btb=None,presel=presel) 
        res, resErr = getRCS(c, cut,  dPhiCut)
        print res,resErr, name, cname
        if res:
          h_nj[name][stb][htb].SetBinContent(i_njb+1, res)
          h_nj[name][stb][htb].SetBinError(i_njb+1, resErr)
          h_ht[name][stb][njb].SetBinContent(i_htb+1, res)
          h_ht[name][stb][njb].SetBinError(i_htb+1, resErr)
          h_2d[name][stb].SetBinContent(i_njb+1, i_htb+1, res) 
          h_2d[name][stb].SetBinError(i_njb+1, i_htb+1, resErr) 

for name, c in [ ["W",cWJets], ["TT", cTTJets]]:
  for stb, dPhiCut in streg:
    c1 = ROOT.TCanvas()
    c1.SetGridx()
    c1.SetGridy()
    first = True 
    l = ROOT.TLegend(0.1,0.75,0.4,0.9)
    l.SetFillColor(ROOT.kWhite)
    l.SetShadowColor(ROOT.kWhite)
    l.SetBorderSize(1)
    for ihtb, htb in enumerate(htreg):
      h_nj[name][stb][htb].GetXaxis().SetLabelSize(0.07)
#      h_nj[name][stb][htb].GetYaxis().SetRangeUser(0, 1.2*h_nj[name][stb][htb].GetBinContent(h_nj[name][stb][htb].GetMaximumBin()))
      h_nj[name][stb][htb].GetYaxis().SetRangeUser(0, 0.1)
      h_nj[name][stb][htb].SetLineColor(ROOT_colors[ihtb])
      l.AddEntry(h_nj[name][stb][htb], varBinName(htb, 'H_{T}'))
      if first:
        first = False
        h_nj[name][stb][htb].Draw()
      else:
        h_nj[name][stb][htb].Draw('same')
    l.Draw()
    c1.Print('/afs/hephy.at/user/'+uDir+'/www/'+subDir+'/'+prefix+'_rCS_njet_'+name+'_'+nameAndCut(stb,htb=None,njetb=None, btb=None, presel=presel)[0]+".png")
    h_2d[name][stb].Draw('COLZ')
    c1.Print('/afs/hephy.at/user/'+uDir+'/www/'+subDir+'/'+prefix+'_rCS_njet_vs_ht_'+name+'_'+nameAndCut(stb,htb=None,njetb=None, btb=None, presel=presel)[0]+".png")
  for htb in htreg:
    c1 = ROOT.TCanvas()
    first = True 
    l = ROOT.TLegend(0.1,0.75,0.4,0.9)
    l.SetFillColor(ROOT.kWhite)
    l.SetShadowColor(ROOT.kWhite)
    l.SetBorderSize(1)
    for istb, [stb, dPhiCut] in enumerate(streg):
      h_nj[name][stb][htb].GetXaxis().SetLabelSize(0.07)
#      h_nj[name][stb][htb].GetYaxis().SetRangeUser(0, 1.2*h_nj[name][stb][htb].GetBinContent(h_nj[name][stb][htb].GetMaximumBin()))
      h_nj[name][stb][htb].GetYaxis().SetRangeUser(0, 0.1)
      h_nj[name][stb][htb].SetLineColor(ROOT_colors[istb])
      l.AddEntry(h_nj[name][stb][htb], varBinName(stb, 'S_{T}'))
      if first:
        first = False
        h_nj[name][stb][htb].Draw()
      else:
        h_nj[name][stb][htb].Draw('same')
    l.Draw()
    c1.Print('/afs/hephy.at/user/'+uDir+'/www/'+subDir+'/'+prefix+'_rCS_njet_'+name+'_'+nameAndCut(stb=None,htb=htb,njetb=None, btb=None presel=presel)[0]+".png")
for name, c in [ ["W",cWJets], ["TT", cTTJets]]:
  for stb, dPhiCut in streg:
    c1 = ROOT.TCanvas()
    first = True 
    l = ROOT.TLegend(0.1,0.9-0.05*len(njreg),0.4,0.9)
    l.SetFillColor(ROOT.kWhite)
    l.SetShadowColor(ROOT.kWhite)
    l.SetBorderSize(1)
    for injb, njb in enumerate(njreg):
      h_ht[name][stb][njb].GetXaxis().SetLabelSize(0.05)
#      h_ht[name][stb][njb].GetYaxis().SetRangeUser(0, 1.2*h_ht[name][stb][njb].GetBinContent(h_ht[name][stb][njb].GetMaximumBin()))
      h_ht[name][stb][njb].GetYaxis().SetRangeUser(0, 0.1)
      h_ht[name][stb][njb].SetLineColor(ROOT_colors[injb])
      l.AddEntry(h_ht[name][stb][njb], nJetBinName(njb))
      if first:
        first = False
        h_ht[name][stb][njb].Draw()
      else:
        h_ht[name][stb][njb].Draw('same')
    l.Draw()
    c1.Print('/afs/hephy.at/user/'+uDir+'/www/'+subDir+'/'+prefix+'_rCS_ht_'+name+'_'+nameAndCut(stb,htb=None,njetb=None, btb=None,presel=presel)[0]+".png")
  for njb in njreg:
    c1 = ROOT.TCanvas()
    first = True 
    l = ROOT.TLegend(0.1,0.9-0.05*len(streg),0.4,0.9)
    l.SetFillColor(ROOT.kWhite)
    l.SetShadowColor(ROOT.kWhite)
    l.SetBorderSize(1)
    for istb, [stb, dPhiCut] in enumerate(streg):
      h_ht[name][stb][njb].GetXaxis().SetLabelSize(0.05)
#      h_ht[name][stb][njb].GetYaxis().SetRangeUser(0, 1.2*h_ht[name][stb][njb].GetBinContent(h_ht[name][stb][njb].GetMaximumBin()))
      h_ht[name][stb][njb].GetYaxis().SetRangeUser(0, 0.1)
      h_ht[name][stb][njb].SetLineColor(ROOT_colors[istb])
      l.AddEntry(h_ht[name][stb][njb], varBinName(stb, 'S_{T}'))
      if first:
        first = False
        h_ht[name][stb][njb].Draw()
      else:
        h_ht[name][stb][njb].Draw('same')
    l.Draw()
    c1.Print('/afs/hephy.at/user/'+uDir+'/www/'+subDir+'/'+prefix+'_rCS_ht_'+name+'_'+nameAndCut(stb=None,htb=None,njetb=njb,btb=None, presel=presel)[0]+".png")



##1D and 2D plots of RCS vs nBTag for TTJets
#prefix = 'reduced'
#presel="singleMuonic&&nVetoMuons==1&&nVetoElectrons==0"
#btreg = [(0,0), (1,1), (2,-1)]
#njreg = [(2,3),(4,4),(5,5),(6,-1)]
#h_btb={}
#for name, c in [ ["TT", cTTJets] ]:
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
#c1.SetGridx()
#c1.SetGridy()
#for name, c in [ ["TT", cTTJets]]:
#  for stb, dPhiCut in streg:
#    c1 = ROOT.TCanvas()
#    c1.SetGridx()
#    c1.SetGridy()
#    for ihtb, htb in enumerate(htreg):
#      first = True 
#      l = ROOT.TLegend(0.1,0.75,0.4,0.9)
#      l.SetFillColor(ROOT.kWhite)
#      l.SetShadowColor(ROOT.kWhite)
#      l.SetBorderSize(1)
#      for i_njb, njb in enumerate(njreg):
#        h_btb[name][stb][htb][njb].GetXaxis().SetLabelSize(0.07)
#  #      h_btb[name][stb][htb].GetYaxis().SetRangeUser(0, 1.2*h_btb[name][stb][htb].GetBinContent(h_btb[name][stb][htb].GetMaximumBin()))
#        h_btb[name][stb][htb][njb].GetYaxis().SetRangeUser(0, 0.08)
#        h_btb[name][stb][htb][njb].SetLineColor(ROOT_colors[i_njb])
#        l.AddEntry(h_btb[name][stb][htb][njb],  nJetBinName(njb))
#        if first:
#          first = False
#          h_btb[name][stb][htb][njb].Draw()
#        else:
#          h_btb[name][stb][htb][njb].Draw('same')
#      l.Draw()
#      c1.Print('/afs/hephy.at/user/'+uDir+'/www/'+subDir+'/'+prefix+'_rCS_nbtag_'+name+'_'+nameAndCut(stb,htb=htb,njetb=None, btb=None, presel=presel)[0]+".png")
