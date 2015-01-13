import ROOT
ROOT.gROOT.ProcessLine('.L /afs/hephy.at/scratch/d/dhandl/CMSSW_7_0_6_patch1/src/Workspace/HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()
from math import *
import os, copy, sys
from array import array
from Workspace.HEPHYPythonTools.helpers import getVarValue, getChain, deltaPhi
from Workspace.RA4Analysis.cmgTuplesPostProcessed import *
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName, varBinName

#Create Chain with MC
WJETS_MC = getChain(WJetsHTToLNu)
TTJETSCSA14_MC = getChain(ttJetsCSA1450ns)

#Create Chain with Signal
SIGNAL1200_1000 = getChain(T5Full_1200_1000_800)
SIGNAL1500_800 = getChain(T5Full_1500_800_100)

#defining ht, st and njets for SR
#ht = 'htJet40ja>500'
#st = '(met_pt+leptonPt)>450'
#cut = "singleMuonic==1&&nBJetLoose25==0&&nJet>=6&&"+ht+"&&"+st
#isoTrackPrefix = 'isoTrpt<15_isoTrpdg_211_isoTrdz<005'
streg = [(200, 250), (250, 350), (350, 450), (450, -1)]                         
htreg = [(500,750),(750,1000),(1000,-1)]
njreg = [(5,5),(6,-1)]
presel="singleMuonic&&nVetoMuons==1&&nVetoElectrons==0"
preprefix = 'singleMuonic_nBjet0_'
wwwDir = 'testpng/'

#use small to check some changes faster
small = 1
if small == 1:
  streg = [(250,-1)]
  htreg = [(400,500)]
  njreg = [(0,-1)]

allVariables = []

#met = {'name':'mymet', 'varString':"met_pt", 'legendName':'#slash{E}_{T}', 'binning':[30,0,1500]}
#isoTrack = {'name':'myisoTrack', 'legendName':'isoTrack', 'binning':[10,0,10]}
#relIso = {'name':'myrelIso', 'legendName':'relIso', 'binning':[100,0,1.0]}
#dPhi = {'name':'mydeltaPhi','legendName':'#Delta#Phi(W,l)','binning':[6,0,3.2]} 
#dPhi = {'name':'mydeltaPhi','legendName':'#Delta#Phi(W,l)','binning':[0,0.5,1,1.5,2,2.5,pi], 'binningIsExplicit':True} 
nJets = {'name':'mynJets', 'varString':'nJet40a', 'legendName':'Jets', 'binning':[6,-0.5,5.5]}

#allVariables.append(met)
#allVariables.append(isoTrack)
#allVariables.append(relIso)
#allVariables.append(dPhi)
allVariables.append(nJets)


dPhiStr = "acos((leptonPt+met*cos(leptonPhi-metPhi))/sqrt(leptonPt**2+met**2+2*met*leptonPt*cos(leptonPhi-metPhi)))"
def getdPhi(c):
  met = c.GetLeaf('met_pt').GetValue()
  metPhi = c.GetLeaf('met_phi').GetValue()
  leptonPt = c.GetLeaf('leptonPt').GetValue()
  leptonPhi = c.GetLeaf('leptonPhi').GetValue()
  dPhi = acos((leptonPt+met*cos(leptonPhi-metPhi))/sqrt(leptonPt**2+met**2+2*met*leptonPt*cos(leptonPhi-metPhi)))
  return dPhi

#def getWPhi(c):
#  metPt = c.GetLeaf('met_pt').GetValue()
#  metPhi = c.GetLeaf('met_phi').GetValue()
#  lepPt = c.GetLeaf('leptonPt').GetValue()
#  lepPhi = c.GetLeaf('leptonPhi').GetValue()
#  X = metPt*cos(metPhi)+lepPt*cos(lepPhi)
#  Y = metPt*sin(metPhi)+lepPt*sin(lepPhi)
#  return atan2(Y,X)

#def nJetBinName(njb):
#  if njb[0]==njb[1]:
#    return "n_{jet}="+str(njb[0])
#  n=str(list(njb)[0])+"\leq n_{jet}"
#  if len(njb)>1 and njb[1]>0:
#    n+='\leq '+str(njb[1])
#  return n
#
#def varBinName(vb, var):
#  n=str(list(vb)[0])+"< "+var
#  if len(vb)>1 and vb[1]>0:
#    n+='< '+str(vb[1])
#  return n

#Define two samples; I used dicts. Adapt as you need.
#data        = {"name":"Data",          "chain":data,                    "weight":1,        "color":ROOT.kBlack}
#qcd_mc      = {"name":"QCD",           "chain":QCD_MC,                  "weight":"weight", "color":ROOT.kBlue - 4}
#singletop_mc     = {"name":"singleTop",     "chain":SINGLETOP_MC,            "weight":"weight", "color":ROOT.kOrange + 4}
wjets_pos_mc = {"name":"W^{+} Jets", "chain":WJETS_MC,        "weight":"weight", "color":ROOT.kYellow, "addcut":"&&leptonPdg<0"}
wjets_neg_mc = {"name":"W^{-} Jets", "chain":WJETS_MC,        "weight":"weight", "color":ROOT.kYellow-9, "addcut":"&&leptonPdg>0"}
ttjets_mc  = {"name":"TTJets", "chain":TTJETSCSA14_MC,         "weight":"weight", "color":ROOT.kRed - 3}
#wjets_mc = {"name":"W+Jets", "chain":WJETS_MC,        "weight":"weight", "color":ROOT.kYellow}
signal1200 = {'name':'T5Full_1200_1000_800', 'chain':SIGNAL1200_1000, 'weight':'weight', 'color':ROOT.kBlack}
signal1500 = {'name':'T5Full_1500_800_100', 'chain':SIGNAL1500_800, 'weight':'weight', 'color':ROOT.kBlue+2}

bkgSamples = [wjets_pos_mc, wjets_neg_mc, ttjets_mc]
#extraSamples = [data]
signals = [signal1200, signal1500]

histos = {}

for i_htb, htb in enumerate(htreg):
  for stb in streg:
    for srNJet in njreg:
      print 'Var region => ht: ',htb,'st: ',stb,'NJet: ',srNJet
      
      for sample in bkgSamples + signals: #Loop over samples
        histos[sample['name']] = {}
      
        for var in allVariables:
          if var.has_key('binningIsExplicit') and var['binningIsExplicit']:
            histos[sample['name']][var['name']] = ROOT.TH1F(sample['name']+'_'+var['name'], sample['name']+'_'+var['name'], len(var['binning'])-1, array('d', var['binning']))
          else:
            histos[sample['name']][var['name']] = ROOT.TH1F(sample['name']+'_'+var['name'], sample['name']+'_'+var['name'], *var['binning'])
          histos[sample['name']][var['name']].Reset()
          #sample['chain'].Draw("Sum$(isoTrack_pt<15&&abs(isoTrack_pdgId)==211&&abs(isoTrack_dz)<0.05)"+">>"+sample["name"]+"_"+var["name"])
          #sample['chain'].Draw(var['varString']+">>"+sample['name']+'_'+var['name'], sample["weight"]+"*("+cut+")")
        
        namestr, cut = nameAndCut(stb, htb, (0,8), btb=(0,0), presel=presel, btagVar = 'nBJetMedium25')
        print cut
        if sample.has_key('addcut'):
          if type(sample['addcut'])==type(''):
            cut = cut + sample["addcut"]

        sample["chain"].Draw(">>eList",cut) #Get the event list 'eList' which has all the events satisfying the cut
        elist = ROOT.gDirectory.Get("eList")
        number_events = elist.GetN()
        print "Sample ",sample["name"],": Will loop over", number_events,"events" #Number of events satisfying the cut
      
      #Event loop
        for i in range(number_events): #Loop over those events
          sample["chain"].GetEntry(elist.GetEntry(i))  #Set the chain to the current event (it's the i-th event of the eList). This is the central line in this file!
          for var in allVariables: 
#            if var == dPhi:
              #WPhi = getWPhi(sample['chain'])
              #lPhi = getVarValue(sample['chain'],'leptonPhi')
              #varValue = deltaPhi(WPhi,lPhi)
#              varValue = getdPhi(sample['chain'])
             # print 'WPhi: ',WPhi,' lPhi: ',lPhi,'deltaPhi: ',varValue
#            else:
            varValue = getVarValue(sample["chain"], var['varString'])   #Get the value of the variable
            weight = 1
            if sample.has_key('weight'):
              if type(sample['weight'])==type(''):
                weight = getVarValue(sample['chain'], sample['weight'])
              else:
                weight = sample['weight']
            histos[sample['name']][var['name']].Fill(varValue, weight)
        del elist
      
      #for sample in signals:
      #  for var in allVariables:
      #    if histos[sample['name']][var['name']].Integral()>0:
      #      histos[sample['name']][var['name']].Scale(histos['TTJets'][var['name']].Integral()/histos[sample['name']][var['name']].Integral())
      
      #Define and stack the histograms...
      for var in allVariables:
        canvas = ROOT.TCanvas(var['name']+' Window',var['name']+' Window')
        pad1 = ROOT.TPad(var['name']+' Pad',var['name']+' Pad',0.,0.3,1.,1.)
        pad1.SetBottomMargin(0)
        pad1.SetLogy()
        pad1.Draw()
        pad1.cd()
        l = ROOT.TLegend(0.6,0.7,0.95,0.95)
        l.SetFillColor(0)
        l.SetBorderSize(1)
        l.SetShadowColor(ROOT.kWhite)
        stack = ROOT.THStack('stack','Stacked Histograms')
      
        text = ROOT.TLatex()
        #text.SetTextAlign(12)
        text.SetNDC()
        #text.SetTextSizePixels(15) 
      
        for sample in bkgSamples:
          histos[sample['name']][var['name']].SetLineColor(ROOT.kBlack)
          histos[sample['name']][var['name']].SetFillColor(sample['color'])
          histos[sample['name']][var['name']].SetMarkerStyle(0)
          histos[sample['name']][var['name']].GetXaxis().SetTitle(var['legendName'])
          histos[sample['name']][var['name']].GetYaxis().SetTitle('Events')# / '+ str( (var['binning'][2] - var['binning'][1])/var['binning'][0])+'GeV')
          histos[sample['name']][var['name']].GetXaxis().SetLabelSize(0.04)
          histos[sample['name']][var['name']].GetYaxis().SetLabelSize(0.04)
          stack.Add(histos[sample['name']][var['name']])
          l.AddEntry(histos[sample['name']][var['name']], sample['name'],'f')
      
        stack.Draw()
        stack.GetXaxis().SetTitle(var['legendName'])
        stack.GetYaxis().SetTitle('Events')# / '+ str( (var['binning'][2] - var['binning'][1])/var['binning'][0])+'GeV')
        stack.SetMinimum(10**(-3))
      
        #for extra in extraSamples:
        #  histos[extra['name']][var['name']].SetMarkerStyle(21)
        #  histos[extra['name']][var['name']].Draw('same E')
        #  l.AddEntry(histos[extra['name']][var['name']],extra['name'])
      
        for sig in signals:
          histos[sig['name']][var['name']].SetLineColor(sig['color'])
          histos[sig['name']][var['name']].SetLineWidth(2)
          histos[sig['name']][var['name']].SetFillColor(0)
          histos[sig['name']][var['name']].SetMarkerStyle(0)
          histos[sig['name']][var['name']].Draw('same')
          l.AddEntry(histos[sig['name']][var['name']], sig['name'])
      
        l.Draw()
      
        text.DrawLatex(0.15,.96,"CMS Simulation")
        text.DrawLatex(0.7,0.96,"L=1 fb^{-1} (13 TeV)")
      
        canvas.cd()
        pad2 = ROOT.TPad(var['name']+" Ratio",var['name']+" Ratio",0.,0.,1.,0.3)
        pad2.SetTopMargin(0)
        pad2.SetBottomMargin(0.3)
        pad2.Draw()
        pad2.cd()
      
        if var.has_key('binningIsExplicit') and var['binningIsExplicit']:
          histo_merge = ROOT.TH1F(var['name']+" Ratio",var['name']+" Ratio", len(var['binning'])-1, array('d', var['binning']))
        else:
          histo_merge = ROOT.TH1F(var['name']+" Ratio",var['name']+" Ratio", *var['binning'])
      #  histo_merge = ROOT.TH1F(var['name']+" Ratio",var['name']+" Ratio", len(var['binning'])-1, array('d', var['binning']))
        histo_merge.Merge(stack.GetHists())
        h_ratio = histos['T5Full_1200_1000_800'][var['name']].Clone('h_ratio')
        h_ratio.SetLineColor(signal1200['color'])
        h_ratio.SetLineWidth(2)
      # h_ratio.SetMinimum(0.0)
      #  h_ratio.SetMaximum(0.02)
        h_ratio.Sumw2()
        h_ratio.SetStats(0)
        h_ratio.Divide(histo_merge)
        h_ratio.SetMarkerStyle(21)
        h_ratio.Draw("ep")
        h_ratio.GetXaxis().SetTitle(var['legendName'])
        h_ratio.GetYaxis().SetTitle("Signal/MC")
        h_ratio.GetYaxis().SetNdivisions(505)
        h_ratio.GetYaxis().SetTitleSize(23)
        h_ratio.GetYaxis().SetTitleFont(43)
        h_ratio.GetYaxis().SetTitleOffset(1.8)
        h_ratio.GetYaxis().SetLabelFont(43)
        h_ratio.GetYaxis().SetLabelSize(20)
        h_ratio.GetYaxis().SetLabelOffset(0.015)
      #  h_ratio.GetXaxis().SetNdivisions(510)
        h_ratio.GetXaxis().SetTitleSize(23)
        h_ratio.GetXaxis().SetTitleFont(43)
        h_ratio.GetXaxis().SetTitleOffset(3.4)
        h_ratio.GetXaxis().SetLabelFont(43)
        h_ratio.GetXaxis().SetLabelSize(20)
        h_ratio.GetXaxis().SetLabelOffset(0.04)
      
        h_ratio2 = histos['T5Full_1500_800_100'][var['name']].Clone('h_ratio2')
        h_ratio2.SetLineColor(signal1500['color'])
        h_ratio2.SetLineWidth(2)
        h_ratio2.Sumw2()
        h_ratio2.SetStats(0)
        h_ratio2.Divide(histo_merge)
        h_ratio2.SetMarkerStyle(21)
        h_ratio2.SetMarkerColor(ROOT.kBlue+2)
        h_ratio2.Draw("same")
      
        canvas.cd()
        #canvas.Print('/afs/hephy.at/user/d/dhandl/www/'+wwwDir+preprefix+namestr+'_'+var['name']+'.png')
        #canvas.Print('/afs/hephy.at/user/d/dhandl/www/'+wwwDir+preprefix+namestr+'_'+var['name']+'.root')
        #canvas.Print('/afs/hephy.at/user/d/dhandl/www/'+wwwDir+preprefix+namestr+'_'+var['name']+'.pdf')

