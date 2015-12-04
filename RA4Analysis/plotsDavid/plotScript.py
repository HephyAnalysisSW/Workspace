import ROOT
ROOT.gROOT.LoadMacro("../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()
ROOT.TH1F().SetDefaultSumw2()
from math import *
import os, copy, sys
from array import array

from Workspace.HEPHYPythonTools.helpers import *
from Workspace.HEPHYPythonTools.xsec import *
from Workspace.HEPHYPythonTools.user import *
from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_postProcessed_antiSel import *
from Workspace.RA4Analysis.helpers import *
from draw_helpers import *
from eleID_helper import *

preprefix = 'plots/1p55fb'
wwwDir = '/afs/hephy.at/user/'+username[0]+'/'+username+'/www/RunII/Spring15_25ns/'+preprefix+'/'
prefix = 'singleLeptonic_'

if not os.path.exists(wwwDir):
  os.makedirs(wwwDir)

def makeWeight(lumi=3., sampleLumi=3.,debug=False):
  if debug:
    print 'No lumi-reweighting done!!'
    return 'weight', 'weight*weight'
  else:
    weight_str = '(((weight)/'+str(sampleLumi)+')*'+str(lumi)+')'
    weight_err_str = '('+weight_str+'*'+weight_str+')'
    return weight_str, weight_err_str
lumi=1550.
sampleLumi=1550.
debugReweighting = True
weight_str, weight_err_str = makeWeight(lumi, sampleLumi=sampleLumi, debug=debugReweighting)

#Bkg chains 
allBkg=[
        {'name':'DY',         'sample':DY_25ns,           'legendName':'DY+jets',          'weight':weight_str, 'isData':False},
        {'name':'singletop',  'sample':singleTop_25ns,    'legendName':'single top',       'weight':weight_str, 'isData':False},
        {'name':'QCD',        'sample':QCDHT_25ns,        'legendName':'QCD',              'weight':weight_str, 'isData':False},
        {'name':'TTV',        'sample':TTV_25ns,          'legendName':'t#bar{t}V(W/Z/H)', 'weight':weight_str, 'isData':False},
        {'name':'W+Jets',     'sample':WJetsHTToLNu_25ns, 'legendName':'W+jets',           'weight':weight_str, 'isData':False},
        {'name':'tt+Jets',    'sample':TTJets_HTLO_25ns,  'legendName':'t#bar{t}+jets',    'weight':weight_str, 'isData':False}
      ]

for bkg in allBkg:
  bkg['chain'] = getChain(bkg['sample'],histname='')
  bkg['color'] = color(bkg['name'])
#  bkg['chain'].SetAlias('dPhi',dPhiStr)

#Data
data=[
     {'name':'date_ele_25ns', 'sample':data_ele_25ns, 'legendName':'Data', 'chain':getChain(data_ele_25ns,histname=''), 'isData':True},
     {'name':'data_mu_25ns',  'sample':data_mu_25ns,  'legendName':'Data', 'chain':getChain(data_mu_25ns, histname=''), 'isData':True}
]

#Signal chains
#allSignals=[
            #"SMS_T1tttt_2J_mGl1200_mLSP800",
            #"SMS_T1tttt_2J_mGl1500_mLSP100",
            #"SMS_T2tt_2J_mStop425_mLSP325",
            #"SMS_T2tt_2J_mStop500_mLSP325",
            #"SMS_T2tt_2J_mStop650_mLSP325",
            #"SMS_T2tt_2J_mStop850_mLSP100",
            #{'name':'T5q^{4} 1.2/1.0/0.8', 'sample':T5qqqqWW_mGo1200_mCh1000_mChi800[lepSel], 'weight':'weight', 'color':ROOT.kBlack},
            #{'name':'T5q^{4} 1.5/0.8/0.1',  'sample':T5qqqqWW_mGo1500_mCh800_mChi100[lepSel],  'weight':'weight', 'color':ROOT.kMagenta},
            #{'name':'T5q^{4} 1.0/0.8/0.7', 'sample':T5qqqqWW_mGo1000_mCh800_mChi700[lepSel], 'weight':'weight', 'color':ROOT.kBlue},
            #"T1ttbbWW_mGo1000_mCh725_mChi715",
            #"T1ttbbWW_mGo1000_mCh725_mChi720",
            #"T1ttbbWW_mGo1300_mCh300_mChi290",
            #"T1ttbbWW_mGo1300_mCh300_mChi295",
            #"T5ttttDeg_mGo1000_mStop300_mCh285_mChi280",
            #"T5ttttDeg_mGo1000_mStop300_mChi280",
            #"T5ttttDeg_mGo1300_mStop300_mCh285_mChi280",
            #"T5ttttDeg_mGo1300_mStop300_mChi280",
#]

#for s in allSignals:
#  s['chain'] = getChain(s['sample'],histname='')
#  s['chain'].SetAlias('dPhi',dPhiStr)

#defining ht, st and njets for SR
streg = [(250,350),(350,450),(450,-1)]                         
htreg = [(500,750),(750,1000),(1000,1250),(1250,-1)]
njreg = [(3,4),(5,5),(6,7),(8,-1)]
btb = (0,0)

#trigger and filters for real Data
trigger = "&&(HLT_EleHT350||HLT_MuHT350)"
filters = "&&Flag_goodVertices&&Flag_HBHENoiseFilter_fix&&Flag_CSCTightHaloFilter&&Flag_eeBadScFilter&&Flag_HBHENoiseIsoFilter"

presel = 'nLep==1&&nVeto==0&&nTightLep==1&&leptonPt>25&&Jet2_pt>80'
antiSelStr = presel+filters+'&&Selected==-1&&leptonHoverE>0.01'
SelStr = presel+filters+'&&Selected==1'


#use small to check some changes faster
small = True
if small:
  streg = [(250,-1)]
  htreg = [(500,-1)]
  njreg = [(3,4)]
  btb   = (0,0)

allVariables = []

nJets =      {'name':'mynJets',      'varString':'nJet30',      'legendName':'n_{jets}',           'Ytitle':'# of Events',         'binning':[15,-0.5,14.5]}
lMomentum =  {'name':'myleptonPt',   'varString':'leptonPt',    'legendName':'p_{T}(l)',           'Ytitle':'# of Events / 25GeV', 'binning':[40,0,1000]}
leadingJet = {'name':'myleadingJet', 'varString':'Jet1_pt',     'legendName':'p_{T}(leading Jet)', 'Ytitle':'# of Events / 50GeV', 'binning':[32,0,1600]}
ht =         {'name':'myht',         'varString':'htJet30j',    'legendName':'H_{T}',              'Ytitle':'# of Events / 25GeV', 'binning':[64,0,1600]}
Lt =         {'name':'mylt',         'varString':'Lt',          'legendName':'L_{T}',              'Ytitle':'# of Events / 25GeV', 'binning':[64,0,1600]}
met =        {'name':'mymet',        'varString':"met_pt",      'legendName':'E^{miss}_{T}',       'Ytitle':'# of Events / 25GeV', 'binning':[64,0,1600]}
dPhi =       {'name':'mydeltaPhi',   'varString':'deltaPhi_Wl', 'legendName':'#Delta#Phi(W,l)',    'Ytitle':'# of Events',         'binning':[30,0,pi]} 
eta =        {'name':'myeta',        'varString':'leptonEta',   'legendName':'#eta(l)',            'Ytitle':'# of Events',         'binning':[50,-2.5,2.5]} 

allVariables.append(nJets)
allVariables.append(lMomentum)
allVariables.append(leadingJet)
allVariables.append(ht)
allVariables.append(Lt)
allVariables.append(met)
allVariables.append(dPhi)
allVariables.append(eta)

histos = {}
h_ratio = {}

for i_htb, htb in enumerate(htreg):
  for stb in streg:
    for srNJet in njreg:
      print 'Var region => ht: ',htb,'st: ',stb, 'NJet: ',srNJet
      for sample in allBkg + data: #Loop over samples
        histos[sample['name']] = {}

        for var in allVariables:
          if var.has_key('binningIsExplicit') and var['binningIsExplicit']:
            histos[sample['name']][var['name']] = ROOT.TH1F(sample['name']+'_'+var['name'], sample['name']+'_'+var['name'], len(var['binning'])-1, array('d', var['binning']))
          else:
            histos[sample['name']][var['name']] = ROOT.TH1F(sample['name']+'_'+var['name'], sample['name']+'_'+var['name'], *var['binning'])
          histos[sample['name']][var['name']].Reset()
          #sample['chain'].Draw("Sum$(isoTrack_pt<15&&abs(isoTrack_pdgId)==211&&abs(isoTrack_dz)<0.05)"+">>"+sample["name"]+"_"+var["name"])
          #sample['chain'].Draw(var['varString']+">>"+sample['name']+'_'+var['name'], sample["weight"]+"*("+cut+")")
        
        if sample['isData']:
          if 'mu' in sample['name']:  
            namestr,cut = nameAndCut(stb, htb, srNJet, btb=(0,0), presel=SelStr+'&&nTightMu==1'+trigger, btagVar = 'nBJetMediumCSV30')
          elif 'ele' in sample['name']:
            namestr,cut = nameAndCut(stb, htb, srNJet, btb=(0,0), presel=SelStr+'&&nTightEl==1'+trigger, btagVar = 'nBJetMediumCSV30')
        else:
          namestr,cut = nameAndCut(stb, htb, srNJet, btb=(0,0), presel=SelStr, btagVar = 'nBJetMediumCSV30')
        #cut = presel+'&&'+nJetCut(srNJet, minPt=30, maxEta=2.4)+'&&'+nBTagCut(btb, minPt=30, maxEta=2.4, minCSVTag=0.890)#+'&&'+htCut(htb, minPt=30, maxEta=2.4, njCorr=0.)#+'&&'+nJetCut(2, minPt=30, maxEta=2.4)
        
        sample["chain"].Draw(">>eList",cut) #Get the event list 'eList' which has all the events satisfying the cut
        elist = ROOT.gDirectory.Get("eList")
        number_events = elist.GetN()
        print "Sample ",sample["name"],": Will loop over", number_events,"events" #Number of events satisfying the cut
        
        #Event loop
        for i in range(number_events): #Loop over those events
          if i%10000==0:
            print "At %i of %i for sample %s"%(i,number_events,sample['name'])

          sample["chain"].GetEntry(elist.GetEntry(i))  #Set the chain to the current event (it's the i-th event of the eList). This is the central line in this file!
          weight = 1.
          if sample.has_key('weight'):
            if type(sample['weight'])==type(''):
              weight = getVarValue(sample['chain'],sample['weight'])
            else:
              weight = sample['weight']

          for var in allVariables:
            assert (var.has_key('varString') or var.has_key('varFunc')), "Error: Did not specify 'varString' or 'varFunc' for var %s" % repr(var)
            assert not (var.has_key('varString') and var.has_key('varFunc')), "Error: Specified both 'varString' and 'varFunc' for var %s" % repr(var)
            varValue = getVarValue(sample["chain"], var['varString']) if var.has_key('varString') else var['varFunc'](sample["chain"])
            histos[sample['name']][var['name']].Fill(varValue, weight)
        del elist
        
        #for sample in signals:
        #  for var in allVariables:
        #    if histos[sample['name']][var['name']].Integral()>0:
        #      histos[sample['name']][var['name']].Scale(histos['TTJets'][var['name']].Integral()/histos[sample['name']][var['name']].Integral())
        
        #Define and stack the histograms...
      for var in allVariables:
        canvas = ROOT.TCanvas(var['name']+'_Window',var['name']+'_Window')
        pad1 = ROOT.TPad(var['name']+'_Pad',var['name']+'_Pad',0.,0.3,1.,1.)
        pad1.SetBottomMargin(0.01)
        pad1.SetLogy()
        pad1.Draw()
        pad1.cd()
        l = ROOT.TLegend(0.65,0.75,0.98,0.95)
        l.SetFillColor(0)
        l.SetBorderSize(1)
        l.SetShadowColor(ROOT.kWhite)
        stack = ROOT.THStack('stack','Stacked Histograms')
       
        text = ROOT.TLatex()
        text.SetNDC()
        text.SetTextSize(0.045)
        text.SetTextAlign(11) 

        for sample in allBkg:
          histos[sample['name']][var['name']].SetLineColor(ROOT.kBlack)
          histos[sample['name']][var['name']].SetFillColor(sample['color'])
          histos[sample['name']][var['name']].SetMarkerStyle(0)
          histos[sample['name']][var['name']].GetXaxis().SetTitle(var['legendName'])
          histos[sample['name']][var['name']].GetYaxis().SetTitle(var['Ytitle'])# / '+ str( (var['binning'][2] - var['binning'][1])/var['binning'][0])+'GeV')
          histos[sample['name']][var['name']].GetXaxis().SetLabelSize(0.04)
          histos[sample['name']][var['name']].GetYaxis().SetLabelSize(0.04)
          stack.Add(histos[sample['name']][var['name']])
          l.AddEntry(histos[sample['name']][var['name']], sample['legendName'],'f')
       
        stack.Draw('hist')
        stack.GetXaxis().SetTitle(var['legendName'])
        stack.GetYaxis().SetTitle(var['Ytitle'])# / '+ str( (var['binning'][2] - var['binning'][1])/var['binning'][0])+'GeV')
        stack.SetMinimum(10**(-1))
        stack.SetMaximum(100*stack.GetMaximum())
 
        first = True
        for extra in data:
          histos[extra['name']][var['name']].SetMarkerStyle(20)
          if first:
            histData = histos[extra['name']][var['name']].Clone()
            l.AddEntry(histos[extra['name']][var['name']],extra['legendName'])
            first = False
          else:
            histData.Add(histos[extra['name']][var['name']])
        histData.Draw('same ep')
       
        #for sig in allSignals:
        #  histos[sig['name']][var['name']].SetLineColor(sig['color'])
        #  histos[sig['name']][var['name']].SetLineWidth(2)
        #  histos[sig['name']][var['name']].SetFillColor(0)
        #  histos[sig['name']][var['name']].SetMarkerStyle(0)
        #  histos[sig['name']][var['name']].Draw('same')
        #  l.AddEntry(histos[sig['name']][var['name']], sig['name'])
       
        l.Draw()

        text.DrawLatex(0.16,.96,"CMS #bf{#it{Preliminary}}")
        text.DrawLatex(0.67,0.96,"#bf{L="+str(lumi)+" fb^{-1} (13 TeV)}")
        
        canvas.cd()
        pad2 = ROOT.TPad(var['name']+"_Ratio",var['name']+"_Ratio",0.,0.,1.,0.3)
        pad2.SetTopMargin(0.01)
        pad2.SetBottomMargin(0.3)
        pad2.SetGrid()
        pad2.Draw()
        pad2.cd()
        
        if var.has_key('binningIsExplicit') and var['binningIsExplicit']:
          histo_merge = ROOT.TH1F(var['name']+"_Ratio",var['name']+"_Ratio", len(var['binning'])-1, array('d', var['binning']))
        else:
          histo_merge = ROOT.TH1F(var['name']+"_Ratio",var['name']+"_Ratio", *var['binning'])
        histo_merge.Merge(stack.GetHists())

        h_ratio = histData.Clone()
        h_ratio.SetMinimum(-0.4)
        h_ratio.SetMaximum(2.4)
        h_ratio.Sumw2()
        h_ratio.SetStats(0)
        h_ratio.Divide(histo_merge)
        h_ratio.SetMarkerStyle(20)
        h_ratio.SetLineStyle(1)
        h_ratio.SetLineWidth(1)
        h_ratio.Draw("ep")
        h_ratio.GetXaxis().SetTitle(var['legendName'])
        h_ratio.GetYaxis().SetTitle("Data/MC")
        h_ratio.GetYaxis().SetNdivisions(505)
        h_ratio.GetYaxis().SetTitleSize(23)
        h_ratio.GetYaxis().SetTitleFont(43)
        h_ratio.GetYaxis().SetTitleOffset(1.8)
        h_ratio.GetYaxis().SetLabelFont(43)
        h_ratio.GetYaxis().SetLabelSize(20)
        h_ratio.GetYaxis().SetLabelOffset(0.015)
        h_ratio.GetXaxis().SetNdivisions(510)
        h_ratio.GetXaxis().SetTitleSize(23)
        h_ratio.GetXaxis().SetTitleFont(43)
        h_ratio.GetXaxis().SetTitleOffset(3.4)
        h_ratio.GetXaxis().SetLabelFont(43)
        h_ratio.GetXaxis().SetLabelSize(20)
        h_ratio.GetXaxis().SetLabelOffset(0.04)
          
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
        canvas.Print(wwwDir+prefix+namestr+'_'+var['name']+'.png')
        canvas.Print(wwwDir+prefix+namestr+'_'+var['name']+'.root')
        canvas.Print(wwwDir+prefix+namestr+'_'+var['name']+'.pdf')
        canvas.Clear()

