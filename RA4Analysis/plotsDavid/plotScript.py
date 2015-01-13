import ROOT
ROOT.gROOT.ProcessLine('.L /afs/hephy.at/scratch/d/dhandl/CMSSW_7_0_6_patch1/src/Workspace/HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()
from math import *
import os, copy, sys
from array import array
from Workspace.HEPHYPythonTools.helpers import getVarValue, getChain, deltaPhi, getYieldFromChain
from Workspace.RA4Analysis.cmgTuplesPostProcessed_v3 import *
from Workspace.RA4Analysis.helpers import *

#Bkg chains 
allBkg=[
        {'name':'TTJets_hard',  'sample':'hard_ttJetsCSA1450ns',  'chain_hard':getChain(hard_ttJetsCSA1450ns), 'weight':'weight',   'color':ROOT.kRed-3},
        #{'name':'TTJets_soft',  'sample':'soft_ttJetsCSA1450ns',  'chain_soft':getChain(soft_ttJetsCSA1450ns), 'weight':'weight',   'color':ROOT.kRed-3},
        {'name':'WJets_hard',   'sample':'hard_WJetsHTToLNu',     'chain_hard':getChain(hard_WJetsHTToLNu),    'weight':'weight',   'color':ROOT.kYellow},
        #{'name':'WJets_soft',   'sample':'soft_WJetsHTToLNu',     'chain_soft':getChain(soft_WJetsHTToLNu),    'weight':'weight',   'color':ROOT.kYellow}
      ]

#Signal chains
allSignals=[
            #{'name':'T5Full_1200_1000_800'}, 
            #{'name':'T5Full_1500_800_100'},
            #{'name':'SMS_T1qqqq_2J_mGl1400_mLSP100_PU_S14_POSTLS170'},
            #{'name':'SMS_T1bbbb_2J_mGl1000_mLSP900_PU_S14_POSTLS170'},
            #{'name':'SMS_T1bbbb_2J_mGl1500_mLSP100_PU_S14_POSTLS170'},
            #{'name':'SMS_T1tttt_2J_mGl1200_mLSP800_PU_S14_POSTLS170'},
            #{'name':'SMS_T1tttt_2J_mGl1500_mLSP100_PU_S14_POSTLS170'},
            #{'name':'SMS_T2tt_2J_mStop425_mLSP325_PU_S14_POSTLS170'},
            #{'name':'SMS_T2tt_2J_mStop500_mLSP325_PU_S14_POSTLS170'},
            #{'name':'SMS_T2tt_2J_mStop650_mLSP325_PU_S14_POSTLS170'},
            #{'name':'SMS_T2tt_2J_mStop850_mLSP100_PU_S14_POSTLS170'},
            #{'name':'SMS_T2bb_2J_mStop600_mLSP580_PU_S14_POSTLS170'},
            #{'name':'SMS_T2bb_2J_mStop900_mLSP100_PU_S14_POSTLS170'},
            #{'name':'SMS_T2qq_2J_mStop600_mLSP550_PU_S14_POSTLS170'},
            #{'name':'SMS_T2qq_2J_mStop1200_mLSP100_PU_S14_POSTLS170'},
            {'name':'T5WW_2J_mGo1200_mCh1000_mChi800','weight':'weight', 'color':ROOT.kBlack, 'LegendName':'T5WW_1200_1000_800' },
            {'name':'T5WW_2J_mGo1500_mCh800_mChi100','weight':'weight', 'color':ROOT.kBlue, 'LegendName':'T5WW_1500_800_100'},
            #{'name':'T5WW_2J_mGo1400_mCh315_mChi300'},
            #{'name':'T1tttt_2J_mGo1300_mStop300_mCh285_mChi280'},
            #{'name':'T1tttt_2J_mGo1300_mStop300_mChi280',  'weight':'weight', 'color':ROOT.kBlack},
            #{'name':'T1tttt_2J_mGo800_mStop300_mCh285_mChi280'},
            #{'name':'T1tttt_2J_mGo800_mStop300_mChi280',   'weight':'weight', 'color':ROOT.kBlue},
            #{'name':'T6ttWW_2J_mSbot600_mCh425_mChi50'},
            #{'name':'T6ttWW_2J_mSbot650_mCh150_mChi50'},
            #{'name':'T1ttbb_2J_mGo1500_mChi100'},
            #{'name':'T1ttbbWW_2J_mGo1000_mCh725_mChi715_3bodydec'},
            #{'name':'T1ttbbWW_2J_mGo1000_mCh725_mChi720_3bodydec'},
            #{'name':'T1ttbbWW_2J_mGo1300_mCh300_mChi290_3bodydec'},
            #{'name':'T1ttbbWW_2J_mGo1300_mCh300_mChi295_3bodydec'},
            #{'name':'T1tttt_gluino_1300_LSP_100'},
            #{'name':'T1tttt_gluino_800_LSP_450'},
            #{'name':'T5qqqqWW_Gl_1400_LSP_100_Chi_325'},
            #{'name':'T5qqqqWW_Gl_1400_LSP_300_Chi_315',  'weight':'weight', 'color':ROOT.kGreen+4},
            #{'name':'T6qqWW_Sq_950_LSP_300_Chi_350',  'weight':'weight', 'color':ROOT.kMagenta+3}
            ]

for s in allSignals:
  s['chain_hard']=getChain(getSignalSample(s['name'],'hard'))
#for s in allSignals:
#  s['chain_soft']=getChain(getSignalSample(s['name'],'soft'))

#Create Chain with MC
#WJETS_MC = getChain(WJetsHTToLNu)
#TTJETSCSA14_MC = getChain(ttJetsCSA1450ns)

#Create Chain with Signal
#SIGNAL1200_1000 = getChain(T5Full_1200_1000_800)
#SIGNAL1500_800 = getChain(T5Full_1500_800_100)

#defining ht, st and njets for SR
streg = [(250, 350), (350,-1)]                         
htreg = [(500,750),(750,-1)]
njreg = [(5,5),(6,-1)]
dPhiStr = "acos((leptonPt+met*cos(leptonPhi-metPhi))/sqrt(leptonPt**2+met**2+2*met*leptonPt*cos(leptonPhi-metPhi)))"
presel='singleMuonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0'
preprefix = 'hardMuonic_0b_ht500_st450_nj6'
wwwDir = '/afs/hephy.at/user/d/dhandl/www/pngCMG/'+preprefix+'/'

if not os.path.exists(wwwDir):
  os.makedirs(wwwDir)

#use small to check some changes faster
small = 1
#small = 0
if small == 1:
  streg = [(450,-1)]
  htreg = [(500,-1)]
  njreg = [(6,-1)]

allVariables = []


def getdPhiMetJet(c):
  met = c.GetLeaf('met_pt').GetValue()
  metPhi = c.GetLeaf('met_phi').GetValue()
  JetPt = c.GetLeaf('leptonPt').GetValue(0)
  JetPhi = c.GetLeaf('leptonPhi').GetValue(0)
#  dPhi = acos((met*JetPt*cos(metPhi-JetPhi))/(met*JetPt))
  dPhi = deltaPhi(metPhi,JetPhi)
  return dPhi

def gethtRatio(c):
  ht = c.GetLeaf('htJet40ja').GetValue()
  Jet0 = c.GetLeaf('Jet_pt').GetValue(0)
  Jet1 = c.GetLeaf('Jet_pt').GetValue(1)
  ratio = (ht-Jet0-Jet1)/(Jet0+Jet1)
  return ratio

def getJetRatio(c):
  Jet0 = c.GetLeaf('Jet_pt').GetValue(0)
  Jet1 = c.GetLeaf('Jet_pt').GetValue(1)
  ratio = (Jet1)/(Jet0)
  return ratio

def getleadingJet(c):
  Jet0 = c.GetLeaf('Jet_pt').GetValue(0)
  return Jet0

def getsecondJet(c):
  Jet1 = c.GetLeaf('Jet_pt').GetValue(1)
  return Jet1

met = {'name':'mymet', 'varString':"met_pt", 'legendName':'#slash{E}_{T}', 'Ytitle':'# of Events / 50GeV', 'binning':[32,0,1600]}
ht = {'name':'myht', 'varString':"htJet40ja", 'legendName':'H_{T}', 'Ytitle':'# of Events / 50GeV', 'binning':[32,0,1600]}
St = {'name':'myst', 'varString':"st", 'legendName':'S_{T}', 'Ytitle':'# of Events / 50GeV', 'binning':[32,0,1600]}
#isoTrack = {'name':'myisoTrack', 'legendName':'isoTrack', 'binning':[10,0,10]}
#relIso = {'name':'myrelIso', 'legendName':'relIso', 'binning':[100,0,1.0]}
#dPhi = {'name':'mydeltaPhi','legendName':'#Delta#Phi(W,l)','binning':[6,0,3.2]} 
nJets = {'name':'mynJets', 'varString':'nJet40a', 'legendName':'Jets', 'Ytitle':'# of Events', 'binning':[17,-0.5,16.5]}
#nBJets = {'name':'mynBJets', 'varString':'nBJetMedium25', 'legendName':'B Jets', 'Ytitle':'# of Events', 'binning':[17,-0.5,16.5]}
dPhi = {'name':'mydeltaPhi', 'varFunc':cmgDPhi, 'legendName':'#Delta#Phi(W,l)','binning':[20,0,pi], 'Ytitle':'# of Events'}#, 'binningIsExplicit':True} 
lMomentum = {'name':'myleptonPt', 'varString':'leptonPt', 'legendName':'p_{T}(l)', 'Ytitle':'# of Events / 50GeV', 'binning':[20,0,1000]}
#htratio = {'name':'myhtratio', 'varFunc':gethtRatio, 'legendName':'H_{T,ratio}', 'Ytitle':'# of Events', 'binning':[25,0,2.5]}
#jetratio = {'name':'myjetratio', 'varFunc':getJetRatio, 'legendName':'2^{nd}Jet/1^{st}Jet', 'Ytitle':'# of Events', 'binning':[15,0,1.5]}
mt = {'name':'mymt', 'varFunc':cmgMT, 'legendName':'M_{T}', 'Ytitle':'# of Events / 10GeV', 'binning':[35,0,350]}
#dphimetjet = {'name':'mydPhimetjet', 'varFunc':getdPhiMetJet, 'legendName':'#Delta#Phi(#slash{E}_{T},J_{1})', 'Ytitle':'# of Events', 'binning':[20,0,pi]}#, 'binningIsExplicit':True}
#leadingJet = {'name':'myleadingJet', 'varFunc':getleadingJet, 'legendName':'p_{T}(leading Jet)', 'Ytitle':'# of Events / 50GeV', 'binning':[32,0,1600]}
#secondJet = {'name':'mysecondJet', 'varFunc':getsecondJet, 'legendName':'p_{T}(J_{2})', 'Ytitle':'# of Events / 50GeV', 'binning':[32,0,1600]}
#htOppRatio = {'name':'myhtOppRatio', 'varFunc':cmgHTRatio, 'legendName':'H^{opp. to #slash{E}_{T}}_{T}/H_{T}', 'Ytitle':'# of Events', 'binning':[20,0,1]}
#minDPhiMetJettwo = {'name':'myminDPhiMetJet12', 'varFunc':cmgMinDPhiJet, 'legendName':'min #Delta#Phi(#slash{E}_{T},J_{1,2})', 'Ytitle':'# of Events', 'binning':[20,0,pi]}#, 'binningIsExplicit':True}
#minDPhiMetJetthree = {'name':'myminDPhiMetJet123', 'varFunc':cmgMinDPhiJet, 'legendName':'min #Delta#Phi(#slash{E}_{T},J_{1,2,3})', 'Ytitle':'# of Events', 'binning':[20,0,pi]}#, 'binningIsExplicit':True}

allVariables.append(met)
allVariables.append(ht)
allVariables.append(St)
#allVariables.append(isoTrack)
#allVariables.append(relIso)
#allVariables.append(nBJets)
allVariables.append(dPhi)
allVariables.append(nJets)
allVariables.append(lMomentum)
#allVariables.append(htratio)
#allVariables.append(jetratio)
allVariables.append(mt)
#allVariables.append(dphimetjet)
#allVariables.append(leadingJet)
#allVariables.append(secondJet)
#allVariables.append(htOppRatio)
#allVariables.append(minDPhiMetJettwo)
#allVariables.append(minDPhiMetJetthree)

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
#wjets_pos_mc = {"name":"W^{+} Jets", "chain":WJETS_MC,        "weight":"weight", "color":ROOT.kYellow, "addcut":"&&leptonPdg<0"}
#wjets_neg_mc = {"name":"W^{-} Jets", "chain":WJETS_MC,        "weight":"weight", "color":ROOT.kYellow-9, "addcut":"&&leptonPdg>0"}
#ttjets_mc  = {"name":"TTJets", "chain":TTJETSCSA14_MC,         "weight":"weight", "color":ROOT.kRed - 3}
#wjets_mc = {"name":"W+Jets", "chain":WJETS_MC,        "weight":"weight", "color":ROOT.kYellow}
#signal1200 = {'name':'T5Full_1200_1000_800', 'chain':SIGNAL1200_1000, 'weight':'weight', 'color':ROOT.kBlack}
#signal1500 = {'name':'T5Full_1500_800_100', 'chain':SIGNAL1500_800, 'weight':'weight', 'color':ROOT.kBlue+2}

#bkgSamples = [wjets_mc, ttjets_mc]
#extraSamples = [data]
#signals = [signal1200, signal1500]

histos = {}
h_ratio = {}

for i_htb, htb in enumerate(htreg):
  for stb in streg:
    for srNJet in njreg:
      print 'Var region => ht: ',htb,'st: ',stb #'NJet: ',srNJet
      for sig in allSignals:            
        h_ratio[sig['name']] = {}     
      for sample in allBkg + allSignals: #Loop over samples
        histos[sample['name']] = {}



        for var in allVariables:
          if var.has_key('binningIsExplicit') and var['binningIsExplicit']:
            histos[sample['name']][var['name']] = ROOT.TH1F(sample['name']+'_'+var['name'], sample['name']+'_'+var['name'], len(var['binning'])-1, array('d', var['binning']))
          else:
            histos[sample['name']][var['name']] = ROOT.TH1F(sample['name']+'_'+var['name'], sample['name']+'_'+var['name'], *var['binning'])
          histos[sample['name']][var['name']].Reset()
          #sample['chain'].Draw("Sum$(isoTrack_pt<15&&abs(isoTrack_pdgId)==211&&abs(isoTrack_dz)<0.05)"+">>"+sample["name"]+"_"+var["name"])
          #sample['chain'].Draw(var['varString']+">>"+sample['name']+'_'+var['name'], sample["weight"]+"*("+cut+")")
          
        namestr, cut = nameAndCut(stb, htb, srNJet, btb=(0,0), presel=presel, btagVar = 'nBJetMedium25')
        print cut
        
        if sample.has_key('addcut'):
          if type(sample['addcut'])==type(''):
            cut = cut + sample["addcut"]
  
        sample["chain_hard"].Draw(">>eList",cut) #Get the event list 'eList' which has all the events satisfying the cut
        elist = ROOT.gDirectory.Get("eList")
        number_events = elist.GetN()
        print "Sample ",sample["name"],": Will loop over", number_events,"events" #Number of events satisfying the cut
        
        #Event loop
        for i in range(number_events): #Loop over those events
          sample["chain_hard"].GetEntry(elist.GetEntry(i))  #Set the chain to the current event (it's the i-th event of the eList). This is the central line in this file!
          for var in allVariables:
            assert (var.has_key('varString') or var.has_key('varFunc')), "Error: Did not specify 'varString' or 'varFunc' for var %s" % repr(var)
            assert not (var.has_key('varString') and var.has_key('varFunc')), "Error: Specified both 'varString' and 'varFunc' for var %s" % repr(var)
            #if var['name'] == 'myminDPhiMetJet12':
            #  varValue = getVarValue(sample["chain_soft"], var['varString']) if var.has_key('varString') else var['varFunc'](sample["chain_soft"],nJets=2)
            #else:
            varValue = getVarValue(sample["chain_hard"], var['varString']) if var.has_key('varString') else var['varFunc'](sample["chain_hard"])
#            if var == dPhi:
#              #WPhi = getWPhi(sample['chain'])
#              #lPhi = getVarValue(sample['chain'],'leptonPhi')
#              #varValue = deltaPhi(WPhi,lPhi)
#              varValue = getdPhi(sample['chain_soft'])
#             # print 'WPhi: ',WPhi,' lPhi: ',lPhi,'deltaPhi: ',varValue
#            if var == htratio:
#              varValue = gethtRatio(sample['chain_soft'])
#            else:
#              varValue = getVarValue(sample["chain_soft"], var['varString'])   #Get the value of the variable
            weight = 1
            if sample.has_key('weight'):
              if type(sample['weight'])==type(''):
                weight = getVarValue(sample['chain_hard'], sample['weight'])
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
        pad1 = ROOT.TPad(var['name']+' Pad',var['name']+' Pad',0.,0.0,1.,1.)
        #pad1.SetBottomMargin(0)
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
       
        for sample in allBkg:
          histos[sample['name']][var['name']].SetLineColor(ROOT.kBlack)
          histos[sample['name']][var['name']].SetFillColor(sample['color'])
          histos[sample['name']][var['name']].SetMarkerStyle(0)
          histos[sample['name']][var['name']].GetXaxis().SetTitle(var['legendName'])
          histos[sample['name']][var['name']].GetYaxis().SetTitle(var['Ytitle'])# / '+ str( (var['binning'][2] - var['binning'][1])/var['binning'][0])+'GeV')
          histos[sample['name']][var['name']].GetXaxis().SetLabelSize(0.04)
          histos[sample['name']][var['name']].GetYaxis().SetLabelSize(0.04)
          stack.Add(histos[sample['name']][var['name']])
          l.AddEntry(histos[sample['name']][var['name']], sample['name'],'f')
       
        stack.Draw()
        stack.GetXaxis().SetTitle(var['legendName'])
        stack.GetYaxis().SetTitle(var['Ytitle'])# / '+ str( (var['binning'][2] - var['binning'][1])/var['binning'][0])+'GeV')
        stack.SetMinimum(10**(-3))
        #stack.SetMaximum(10)
 
        #for extra in extraSamples:
        #  histos[extra['name']][var['name']].SetMarkerStyle(21)
        #  histos[extra['name']][var['name']].Draw('same E')
        #  l.AddEntry(histos[extra['name']][var['name']],extra['name'])
       
        for sig in allSignals:
          histos[sig['name']][var['name']].SetLineColor(sig['color'])
          histos[sig['name']][var['name']].SetLineWidth(2)
          histos[sig['name']][var['name']].SetFillColor(0)
          histos[sig['name']][var['name']].SetMarkerStyle(0)
          histos[sig['name']][var['name']].Draw('same')
          l.AddEntry(histos[sig['name']][var['name']], sig['LegendName'])
       
        l.Draw()
        
        text.DrawLatex(0.15,.96,"CMS Simulation")
        text.DrawLatex(0.65,0.96,"L=1 fb^{-1} (13 TeV)")
        
#        canvas.cd()
#        pad2 = ROOT.TPad(var['name']+" Ratio",var['name']+" Ratio",0.,0.,1.,0.3)
#        pad2.SetTopMargin(0)
#        pad2.SetBottomMargin(0.3)
#        pad2.Draw()
#        pad2.cd()
#        
#        if var.has_key('binningIsExplicit') and var['binningIsExplicit']:
#          histo_merge = ROOT.TH1F(var['name']+" Ratio",var['name']+" Ratio", len(var['binning'])-1, array('d', var['binning']))
#        else:
#          histo_merge = ROOT.TH1F(var['name']+" Ratio",var['name']+" Ratio", *var['binning'])
#        histo_merge.Merge(stack.GetHists())
#
#        for sig in allSignals:
#          h_ratio[sig['name']][var['name']] = histos[sig['name']][var['name']].Clone()
#          h_ratio[sig['name']][var['name']].SetLineColor(sig['color'])
#          h_ratio[sig['name']][var['name']].SetLineWidth(2)
#        # h_ratio[sig['name']][var['name']].SetMinimum(0.0)
#       #  h_ratio[sig['name']][var['name']].SetMaximum(0.02)
#          h_ratio[sig['name']][var['name']].Sumw2()
#          h_ratio[sig['name']][var['name']].SetStats(0)
#          h_ratio[sig['name']][var['name']].Divide(histo_merge)
#          h_ratio[sig['name']][var['name']].SetMarkerStyle(21)
#          h_ratio[sig['name']][var['name']].Draw("ep")
#          h_ratio[sig['name']][var['name']].GetXaxis().SetTitle(var['legendName'])
#          h_ratio[sig['name']][var['name']].GetYaxis().SetTitle("Signal/Bkg")
#          h_ratio[sig['name']][var['name']].GetYaxis().SetNdivisions(505)
#          h_ratio[sig['name']][var['name']].GetYaxis().SetTitleSize(23)
#          h_ratio[sig['name']][var['name']].GetYaxis().SetTitleFont(43)
#          h_ratio[sig['name']][var['name']].GetYaxis().SetTitleOffset(1.8)
#          h_ratio[sig['name']][var['name']].GetYaxis().SetLabelFont(43)
#          h_ratio[sig['name']][var['name']].GetYaxis().SetLabelSize(20)
#          h_ratio[sig['name']][var['name']].GetYaxis().SetLabelOffset(0.015)
#        #  h_ratio[sig['name']][var['name']].GetXaxis().SetNdivisions(510)
#          h_ratio[sig['name']][var['name']].GetXaxis().SetTitleSize(23)
#          h_ratio[sig['name']][var['name']].GetXaxis().SetTitleFont(43)
#          h_ratio[sig['name']][var['name']].GetXaxis().SetTitleOffset(3.4)
#          h_ratio[sig['name']][var['name']].GetXaxis().SetLabelFont(43)
#          h_ratio[sig['name']][var['name']].GetXaxis().SetLabelSize(20)
#          h_ratio[sig['name']][var['name']].GetXaxis().SetLabelOffset(0.04)
          
          #h_ratio2 = histos['T5Full_1500_800_100'][var['name']].Clone('h_ratio2')
          #h_ratio2.SetLineColor(signal1500['color'])
          #h_ratio2.SetLineWidth(2)
          #h_ratio2.Sumw2()
          #h_ratio2.SetStats(0)
          #h_ratio2.Divide(histo_merge)
          #h_ratio2.SetMarkerStyle(21)
          #h_ratio2.SetMarkerColor(ROOT.kBlue+2)
          #h_ratio2.Draw("same")
         
        canvas.cd()
        canvas.Print(wwwDir+preprefix+'_'+namestr+'_'+var['name']+'.png')
        canvas.Print(wwwDir+preprefix+'_'+namestr+'_'+var['name']+'.root')
        canvas.Print(wwwDir+preprefix+'_'+namestr+'_'+var['name']+'.pdf')

