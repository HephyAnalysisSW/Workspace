import ROOT
import os, sys
import math
import argparse
import pickle
import json
from array import array
from math import pi, sqrt #cos, sin, sinh, log
from DataFormats.FWLite import Events, Handle

ROOT.gStyle.SetOptStat(0) #0 removes histogram statistics box #Name, Entries, Mean, RMS, Underflow, Overflow, Integral, Skewness, Kurtosis
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptFit(0) #1111) #1111 prints fits results on plot

ROOT.gStyle.SetPaintTextFormat("4.2f")
#ROOT.gStyle->SetTitleX(0.1)
#ROOT.gStyle->SetTitleW(0.8)

ROOT.gStyle.SetStatX(0.875)
ROOT.gStyle.SetStatY(0.75)
ROOT.gStyle.SetStatW(0.1)
ROOT.gStyle.SetStatH(0.1)

# Functions
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        #if exc.errno == errno.EEXIST and os.path.isdir(path):
        if os.path.isdir(path):
            pass
        else:
            raise

def makeDir(path):
    if "." in path[-5:]:
        path = path.replace(os.path.basename(path),"")
        #print path
    if os.path.isdir(path):
        return
    else:
        mkdir_p(path)

def getListFromFile(filename):
   f = open(filename,'r')
   outlist = []
   for l in f:
      l = l.strip('\n')
      outlist.append(l)
   f.close()
   return outlist

# Efficiency
def makeEffPlot(passed,total):
   a = passed.Clone()
   b = total.Clone()
   eff = ROOT.TEfficiency(a,b)
   eff.SetTitle("Efficiency Plot")
   eff.SetMarkerStyle(33)
   eff.SetMarkerSize(2)
   eff.SetLineWidth(2)
   return eff

def setupEffPlot(eff):
   ROOT.gPad.Modified()
   ROOT.gPad.Update()

   ROOT.gPad.SetGridx()
   ROOT.gPad.SetGridy()
   eff.GetPaintedGraph().GetYaxis().SetTitle("Efficiency")
   eff.GetPaintedGraph().SetMinimum(0)
   eff.GetPaintedGraph().SetMaximum(1)
   eff.GetPaintedGraph().GetXaxis().CenterTitle()
   eff.GetPaintedGraph().GetYaxis().CenterTitle()

   ROOT.gPad.Modified()
   ROOT.gPad.Update()

def drawText(text, x, y):        
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.015)
    latex.DrawLatex(x,y, "#font[42]{%s}"%text)

def check_json(runNo_in, LS):
    runNo = str(runNo_in)
    file1=open(json_file,'r')
    inp1={}
    text = ""
    for line1 in file1:
        text+=line1
    inp1 = json.loads(text)
    #print inp1.keys()
    if runNo in inp1:
        for part_LS in inp1[runNo]:
            if LS >= part_LS[0] and LS <= part_LS[1]:
                return True
    return False

def deltaR((eta1, phi1), (eta2, phi2)):
    ''' Compute dR, with eta and phi values of the two objects as input.
    
    '''

    dPhi = phi2 - phi1

    if  dPhi > math.pi:
        dPhi -= 2.0 * math.pi

    if dPhi <= -math.pi:
        dPhi += 2.0 * math.pi

    dEta = eta2 - eta1

    dRsq = dPhi ** 2 + dEta ** 2

    #
    return math.sqrt(dRsq)

parser = argparse.ArgumentParser(description="Input options")
parser.add_argument("--infiles", help = "Input files", type = str, nargs = "+", default = [None])
parser.add_argument("--paths", help = "Trigger paths", type = str, nargs = "+", default = ["HLT_Mu3er1p5_PFJet100er2p5_PFMET80_PFMHT80_IDTight"])
parser.add_argument("--PD", help = "PD", type = str, default = "MET", choices = ["MET", "SingleMuon"])
parser.add_argument("--muonID", help = "muonID", type = str, default = "loose", choices = ["loose", "CBloose", "CBmedium", 'None'])
parser.add_argument("--muonEta", help = "muonEta", type = str, default = "1p5", choices = ["1p5", "2p1", "2p4", "Barrel", "Endcap"])
parser.add_argument("--muonIso", help = "muonIso", type = int, default = 5)
parser.add_argument("--leadJetEta", help = "leadJetEta", type = str, default = "2p5", choices = ["2p5"])
parser.add_argument("--applyFilters", dest = "applyFilters",  help = "Apply filters", type = int, default = 1)
args = parser.parse_args()

infiles = args.infiles
PD = args.PD 
muonID = args.muonID 
muonEta = args.muonEta 
muonIso = args.muonIso 
leadJetEta = args.leadJetEta
applyFilters = args.applyFilters

if not len(sys.argv) > 1:
   print "No arguments given. Using default settings."

doFit = True
doName = True
doBox = False

baseSavedir = "/afs/hephy.at/user/m/mzarucki/www/plots/SoftTriggers/Data"

# Data
json_file = "Cert_314472-316723_13TeV_PromptReco_Collisions18_JSON.txt" # Golden JSON 2018

if PD == 'MET':
    denTrig = 'HLT_PFMET120_PFMHT120_IDTight'
    #sampName = "2018A_MET_MINIAOD_315974-316723"
    varsToPlot = ['MuPt']
    plateauCuts = {'MuPt':8, 'MET':200, 'LeadJetPt':150}
elif PD == 'SingleMuon':    
    denTrig = 'HLT_IsoMu24'
    #sampName = "2018A_SingleMuon_MINIAOD_315974-316723"
    varsToPlot = ['MET', 'LeadJetPt']
    plateauCuts = {'MuPt':40, 'MET':200, 'LeadJetPt':150} 
else:
    print "Wrong PD. Exiting."
    sys.exit()

fileTag = infiles[-1].split('/')[-1].replace('.root','')
savedir = "%s/%s/%s_Run2018A_%s"%(baseSavedir,PD,PD,fileTag)

filters = ["Flag_goodVertices", "Flag_globalTightHalo2016Filter", "Flag_HBHENoiseFilter", "Flag_HBHENoiseIsoFilter", "Flag_EcalDeadCellTriggerPrimitiveFilter", "Flag_BadPFMuonFilter", "Flag_BadChargedCandidateFilter", "Flag_eeBadScFilter", "Flag_ecalBadCalibFilter"]

if args.paths:
    triggers = args.paths # specified as arguments 
else:
    triggers = getListFromFile(triggerList) # from SoftTriggers-V*.list 

#infiles = [x.strip() for x in open('inputFiles/inputFiles_%s.txt'%sampName).readlines()]

suff = ''

# Offline cuts

if muonEta not in ['Barrel', 'Endcap', '2p4', '2p1', '1p5']:
    muonEta = 'BarrelPlusEndcap'

suff += '_MuEta' + muonEta

if not muonID or muonID == 'None':
    muonID = 'no'
    
suff += '_%sID'%muonID

if muonIso:
    suff += '_iso' + str(muonIso)
else:
    suff += '_noIso'
    
if leadJetEta:
    suff += '_leadJetEta' + leadJetEta

if applyFilters:
    suff += '_filters'
else:
    suff += '_noFilters'

variables = {'MET':'PFMET', 'LeadJetPt':'Jet', 'MuPt':'Mu'}# 'ElePt':'Ele', 'HT':'PFHT',
varNames = {'MET':'PF-MET', 'LeadJetPt':'Leading Jet p_{T}', 'MuPt':'Muon p_{T}', 'ElePt':'Electron p_{T}', 'HT':'PF-HT'}

varsCutOn = {}
                
for trig in triggers:
    varsCutOn[trig] = []
   
    for var in variables:
        if variables[var] in trig:
            varsCutOn[trig].append(var)
    
    if 'ETM' in trig and 'MET' not in varsCutOn[trig]: #NOTE: needs to be included for ETM
        varsCutOn[trig].append('MET')
    
#    varsToPlot[trig] = varsCutOn[trig][:]
#
#    #if 'MET' in varsToPlot[trig] and not 'HT' in varsToPlot[trig]:
#    #    varsToPlot[trig].append('HT')
#    #elif 'HT' in varsToPlot[trig] and not 'MET' in varsToPlot[trig]:
#    #    varsToPlot[trig].append('MET')
#    #if 'HT' in varsToPlot[trig] and not 'LeadJetPt' in varsToPlot[trig]:
#    #    varsToPlot[trig].append('LeadJetPt')

# Histograms
hists = {'dens':{}, 'nums':{}}
xmax = {'MET':600, 'HT':600, 'LeadJetPt':300, 'MuPt':30, 'ElePt':30}

for var in varsToPlot:
    hists['dens'][var] = {}
    hists['nums'][var] = {}

    for trig in triggers:
        hists['dens'][var][trig] = ROOT.TH1D("den_%s_%s"%(var,trig), "den_%s_%s"%(var,trig), 30, 0, xmax[var])
        #hists['dens'][var][trig].SetTitle("%s Distribution"%var)
        hists['dens'][var][trig].GetYaxis().SetTitle("Events")
        hists['dens'][var][trig].GetXaxis().SetTitle("%s / GeV"%varNames[var])
        hists['dens'][var][trig].GetXaxis().CenterTitle()
        hists['dens'][var][trig].GetYaxis().CenterTitle()
        hists['dens'][var][trig].GetXaxis().SetTitleOffset(1.2)
        hists['dens'][var][trig].GetYaxis().SetTitleOffset(1.4)
        hists['dens'][var][trig].SetFillColor(ROOT.kBlue-9)
        hists['dens'][var][trig].SetLineColor(ROOT.kBlack)
        hists['dens'][var][trig].SetLineWidth(2)

        hists['nums'][var][trig] = ROOT.TH1D("num_%s_%s"%(var, trig), "num_%s_%s"%(var, trig), 30, 0, xmax[var])
        hists['nums'][var][trig].SetFillColor(ROOT.kGreen+2)
        hists['nums'][var][trig].SetLineColor(ROOT.kBlack)
        hists['nums'][var][trig].SetLineWidth(2)

#f = ROOT.TFile(infile)
#tree = f.Get("Events")

#nEvents = nListEntries
#nEvents = tree.GetEntries() 

# Handles to get event products
triggerBits, triggerBitLabel = Handle("edm::TriggerResults"), ("TriggerResults::HLT") 
filterBits, filterBitLabel = Handle("edm::TriggerResults"), ("TriggerResults::RECO") 
handleMETs = Handle("std::vector<pat::MET>")
handleJets = Handle("std::vector<pat::Jet>")
handleMus  = Handle('std::vector<pat::Muon>')
handleEles = Handle('std::vector<pat::Electron>')

events = Events(infiles)

values = {}

trigNames = None
filtNames = None

runAndLsList = []

#for i in range(nEvents):
for i,event in enumerate(events):
    #print i
    #print "eList index", i
    #if i == 10: break
    runnbr = event.object().id().run()
    runls = event.object().id().luminosityBlock()
    runstr = str((runnbr,runls))   

    jsonCheck = check_json(runnbr, runls)
    #print runstr, jsonCheck
    if not jsonCheck: continue
    #if not runstr in runAndLsList:
    #   nLS = nLS +1
    #   runAndLsList.append(runstr)
    
    #tree.GetEntry(i)

    #tree.GetEntry(eList.GetEntry(i))
    #TTree:GetEntry(entry) = Read all branches of entry and return total number of bytes read. The function returns the number of bytes read from the input buffer. If entry does not exist the function returns 0. If an I/O error occurs,
    #TEventList:GetEntry(index) = Return value of entry at index in the list. Return -1 if index is not in the list range. 
    #TEventList:GetIndex(entry) Return index in the list of element with value entry array is supposed to be sorted prior to this call. If match is found, function returns position of element.
    
    #run = event.eventAuxiliary().run()
    #lumi = event.eventAuxiliary().luminosityBlock()
    #eventId = event.eventAuxiliary().event()
    
    # Muons 
    event.getByLabel(("slimmedMuons", '', 'RECO'), handleMus)
    muons = handleMus.product()
    
    if len(muons) > 0:
        muon = muons[0] # leading muon 
        values['MuPt'] = muon.pt()   
        
        if muonEta == "Barrel":
            if not abs(muon.eta()) < 1.2: continue
        elif muonEta == "Endcap":
            if not abs(muon.eta()) > 1.2: continue
        elif muonEta == "1p5":
            if not abs(muon.eta()) < 1.5: continue
        elif muonEta == "2p1":
            if not abs(muon.eta()) < 2.1: continue
        elif muonEta == "2p4":
            if not abs(muon.eta()) < 2.4: continue

        if muonID == "loose" and not muon.isLooseMuon():    continue
        #elif muonID == "CBloose"  and not muon.CutBasedIdLoose:  continue
        #elif muonID == "CBmedium" and not muon.CutBasedIdMedium: continue

        if muonIso:
            isoObj = muon.pfIsolationR03() # pfIsolationR04()
            #sumChargedHadronPt  = sum-pt of charged Hadron 
            #sumChargedParticlePt  =sum-pt of charged Particles(inludes e/mu) 
            #sumNeutralHadronEt = sum pt of neutral hadrons
            #sumPhotonEt = sum pt of PF photons
            #sumNeutralHadronEtHighThreshold = sum pt of neutral hadrons with a higher threshold
            #sumPhotonEtHighThreshold = sum pt of PF photons with a higher threshold
            #sumPUPt = sum pt of charged Particles not from PV  (for Pu corrections)
            
            isolation = isoObj.sumChargedHadronPt + isoObj.sumNeutralHadronEt #sumPhotonEt, sumChargedParticlePt sumNeutralHadronEtHighThreshold

            if isolation > muonIso: continue

    else:
        values['MuPt'] = -1
    
    ## Electrons 
    #event.getByLabel(("slimmedElectrons", '', 'RECO'), handleEles)
    #electrons = handleEles.product()
    #
    #if len(electrons) > 0:
    #    ele = electrons[0] 
    #    values['ElePt'] = ele.pt()   
    #else:
    #    values['ElePt'] = -1
    
    # MET    
    event.getByLabel(("slimmedMETs", '', 'RECO'), handleMETs)
    met = handleMETs.product().front()
    values['MET'] = met.pt()
    #MET = tree.GetLeaf("recoPFMETs_pfMet__RECO.obj").pt().GetValue(0)

    # Jets
    event.getByLabel(("slimmedJets", '', 'RECO'), handleJets)
    jets = handleJets.product()
   
    if len(jets) > 0:
        goodLeadJet = True
        if len(muons) > 0:
            for m in muons:
                dR = deltaR((jets[0].eta(), jets[0].phi()),(m.eta(),m.phi()))
                #print dR 
                if dR < 0.3: 
                    goodLeadJet = False 

        if not goodLeadJet: continue

        leadJet = jets[0]
        values['LeadJetPt'] = leadJet.pt()
        
        if leadJetEta == "2p5":
            if not abs(leadJet.eta()) < 2.5: continue
    
        ## HT Calculation
        #jetPtCut = 30.     
        #jetEtaCut = 2.4   

        #values['HT'] = 0.
        #for jet in jets:
        #    if(jet.pt() > jetPtCut and abs(jet.eta()) < jetEtaCut): 
        #         values['HT'] += jet.pt()
    else:
        values['LeadJetPt'] = -1
    
    # Filter Results
    event.getByLabel(filterBitLabel, filterBits)

    if applyFilters:
        passFilters = True 
        if not filtNames:
            filtNames = event.object().triggerNames(filterBits.product())
    
        for filt in filters: 
            filtIndex = filtNames.triggerIndex(filt)
            filtDecision = filterBits.product().accept(filtIndex)
            #print filt, filtDecision
            if not filtDecision: 
                passFilters = False
 
        if not passFilters: continue   
 
    # Trigger Results
    event.getByLabel(triggerBitLabel, triggerBits)

    if not trigNames:
        trigNames = event.object().triggerNames(triggerBits.product())
        trigList = []

        for trigName in trigNames.triggerNames():
            #print trigName
            trigName = str(trigName)
            if ("HLTriggerFirstPath" in trigName) or ("HLTriggerFinalPath" in trigName): continue
            if not (trigName.startswith("HLT_") or trigName.startswith("DST_")): continue
            trigList.append(trigName)
    
    trigFull = None
    denTrigFull = None

    for trig in triggers:
        for trig2 in trigList:
            if not trigFull and trig in trig2:
               trigFull = trig2 # includes version number
               #break
            if not denTrigFull and denTrig in trig2:
               denTrigFull = trig2 # includes version number
 
        if not trigFull:
            print "Warning: Trigger %s not found."%trigFull 
            break
        if not denTrigFull:
            print "Warning: Trigger %s not found."%denTrigFull 
            break
        
        denIndex = trigNames.triggerIndex(denTrigFull)
        denDecision = triggerBits.product().accept(denIndex)
  
        if not denDecision: continue
 
        index = trigNames.triggerIndex(trigFull)
        decision = triggerBits.product().accept(index)
        
        #decision = tree.GetLeaf(tree.GetAlias(trig)).GetValue(0) # if trigger saved as branch via TriggerDecisionAnalyzer
        
        #print "---"
        #print trig
        #print "Variables cut on:", varsCutOn[trig]
        #print "---"
        
        #print "---"
        #print "Trigger:", trig
        #print "Mu pt of %s GeV over %s GeV plateau?"%(values['MuPt'],plateauCuts['MuPt']), values['MuPt'] > plateauCuts['MuPt'] 
        #print "Leading Jet pt of %s GeV over %s GeV plateau?"%(values['LeadJetPt'],plateauCuts['LeadJetPt']), values['LeadJetPt'] > plateauCuts['LeadJetPt'] 
        #print "MET of %s GeV over %s GeV plateau?"%(values['MET'],plateauCuts['MET']), values['MET'] > plateauCuts['MET'] 
    
        for plot in varsToPlot:
            passEvent = True
            for var in varsCutOn[trig]:
                if plot != var and values[var] < plateauCuts[var]:
                    passEvent = False

            #print plot, "plot:", passEvent

            if passEvent:
                hists['dens'][plot][trig].Fill(values[plot])
                if decision:
                    hists['nums'][plot][trig].Fill(values[plot])
                    #print "Trigger fired!"
            
# Fit Function
if doFit:
    fitFunc = ROOT.TF1("f1", "[0]*TMath::Erf((x-[1])/[2]) + [3]", 0, 1000) #Error function scaled to [0,1]
    fitFunc.SetParNames("Norm.", "Edge", "Resolution", "Y-Offset")
    #fitFunc.SetLineColor(ROOT.kAzure-1)
    #fitFunc.SetParameter(0, 0.5)
    #fitFunc.SetParameter(1, 150)
    #fitFunc.SetParameter(2, 50)  
    
    #fitFunc.SetParLimits(0, 0.4, 0.65) 
    #fitFunc.SetParLimits(1, 0, 100)
    #fitFunc.SetParLimits(2, 0, 50)
    #fitFunc.SetParLimits(3, 0.4, 0.8)
    
    #fitFunc.SetParameters(0.5, 30, 20, 0.5)
    #fitFunc.SetParameters(0.5, 140, 40, 0.50)

for trig in triggers:
    makeDir("%s/%s/histos"%(savedir,trig)) 
    makeDir("%s/%s/root"%(savedir,trig)) 
    makeDir("%s/%s/pdf"%(savedir,trig))

    for var in varsToPlot:
        canv = ROOT.TCanvas("Canvas %s_%s"%(var,trig), "Canvas %s_%s"%(var,trig), 1500, 1500)
        canv.SetGrid()

        f = ROOT.TFile('%s/%s/histos/histos_%s_%s%s_%s.root'%(savedir,trig,var,trig,suff,fileTag), "recreate")

        # Histograms
        hists['dens'][var][trig].Write()               
        hists['nums'][var][trig].Write()               
        hists['dens'][var][trig].Draw('hist')
        hists['nums'][var][trig].Draw('hist same')
        
        ROOT.gPad.Modified()
        ROOT.gPad.Update()
        
        latex1 = ROOT.TLatex()
        latex1.SetNDC()
        latex1.SetTextSize(0.03)
        latex1.DrawLatex(0.12, 0.92, "CMS Simulation")
        #latex1.DrawLatex(0.12, 0.92, "#font[62]{CMS Simulation}")
       
        if doName: 
            latex2 = ROOT.TLatex()
            latex2.SetNDC()
            latex2.SetTextSize(0.025)
            latex2.SetTextColor(ROOT.kRed+1)
            latex2.DrawLatex(0.15, 0.87, trig)
            
        ## Efficiency
        overlay = ROOT.TPad("overlay", "", 0, 0, 1, 1)
        overlay.SetFillStyle(4000)
        overlay.SetFillColor(0)
        overlay.SetFrameFillStyle(4000)
        overlay.Draw()
        overlay.cd()

        frame = overlay.DrawFrame(0, 0, xmax[var], 1.1) # overlay.DrawFrame(pad.GetUxmin(), 0, pad.GetUxmax(), 1.2)
 
        eff = makeEffPlot(hists['nums'][var][trig],hists['dens'][var][trig])
        #eff.SetMarkerColor(ROOT.kAzure-1)
        #eff.SetTitle("%s Trigger Efficiency; %s; Trigger Efficiency"%(trig,var))
        eff.Draw("P")
       
        # axis on the right side
        axis = ROOT.TGaxis(ROOT.gPad.GetUxmax(), ROOT.gPad.GetUymin(), ROOT.gPad.GetUxmax(), ROOT.gPad.GetUymax(), ROOT.gPad.GetUymin(), ROOT.gPad.GetUymax(), 510, "+L")
        axis.SetTitle("#font[42]{Trigger Efficiency}")
        axis.CenterTitle()
        axis.SetLabelSize(0.03)
        axis.SetTitleSize(0.03)
        axis.SetTitleOffset(1.4)
        axis.SetLabelColor(ROOT.kAzure-1)
        axis.SetLineColor(ROOT.kAzure-1)
        axis.SetTextColor(ROOT.kAzure-1)
        axis.Draw()

        if doFit:
            if var in ['MuPt', 'ElePt']: 
                fitFunc.SetParameters(0.5, 5, 20, 0.5)
            elif 'Jet' in var:
                fitFunc.SetParameters(0.5, 120, 30, 0.5)
            else:
                fitFunc.SetParameters(0.5, 30, 50, 0.5)

            eff.Fit(fitFunc)

            # Fit Parameter Extraction
            fitParams = {}
            #fitFunc.GetParameters(fit)
            fitParams['chiSq'] = fitFunc.GetChisquare()
            for x in xrange(0, 4):
               fitParams['var%s'%x] = fitFunc.GetParameter(x)
               fitParams['var%s'%x] = fitFunc.GetParError(x)
            
               fitParams['val50'] =  fitFunc.GetX(0.5)
               fitParams['val75'] =  fitFunc.GetX(0.75)
               fitParams['val80'] =  fitFunc.GetX(0.80)
               fitParams['val85'] =  fitFunc.GetX(0.85)
               fitParams['val90'] =  fitFunc.GetX(0.90)
               fitParams['val95'] =  fitFunc.GetX(0.95)
               fitParams['val99'] =  fitFunc.GetX(0.99)
               fitParams['val100'] = fitFunc.GetX(1)
       
            #print 'Fit parameters', var, trig, fitParams
 
            ROOT.gPad.Modified()
            ROOT.gPad.Update()
   
            setupEffPlot(eff)
        
            pad = ROOT.TPad("pad", "", 0, 0, 1, 1)
            pad.SetFillStyle(0)
            pad.Draw()
            pad.cd()
           
            if doBox: 
                box = ROOT.TBox(0.7, 0.35, 0.875, 0.525)
                box.SetFillColor(0)
                box.Draw('l')

                drawText("#bf{Turn-on:}", 0.75, 0.5)
                drawText("100 %%: %.0f GeV"%fitParams['val100'], 0.725, 0.475)
                drawText("  99 %%: %.0f GeV"%fitParams['val99'],  0.725, 0.45)
                drawText("  95 %%: %.0f GeV"%fitParams['val95'],  0.725, 0.425)
                drawText("  90 %%: %.0f GeV"%fitParams['val90'],  0.725, 0.4)
                drawText("  85 %%: %.0f GeV"%fitParams['val85'],  0.725, 0.375)
 
            ROOT.gPad.Modified()
            ROOT.gPad.Update()
 
        #Save canvas
        canv.SaveAs("%s/%s/trigEff_%s_%s%s.png"%(savedir,trig,var,trig,suff))
        canv.SaveAs("%s/%s/pdf/trigEff_%s_%s%s.pdf"%(savedir,trig,var,trig,suff))
        canv.SaveAs("%s/%s/root/trigEff_%s_%s%s.root"%(savedir,trig,var,trig,suff))
