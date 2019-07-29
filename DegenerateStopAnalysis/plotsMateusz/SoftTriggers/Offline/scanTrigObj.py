# scanTrigObj.py

import ROOT
import os, sys
import argparse
import importlib

import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import makeHist, makeEffPlot, setupEffPlot, makeLine
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import setup_style, makeLumiTag, makeDir
from Workspace.DegenerateStopAnalysis.tools.degCuts import CutsWeights
from Workspace.DegenerateStopAnalysis.tools.degPlots import Plots
from Workspace.DegenerateStopAnalysis.samples.getSamples import getSamples
from Workspace.DegenerateStopAnalysis.samples.samplesInfo import getCutWeightOptions

# input options
parser = argparse.ArgumentParser(description = "Input options")
parser.add_argument("--triggers",   help = "Triggers",              type = str, default = "",           nargs = "+")
parser.add_argument("--dataset",    help = "Primary dataset",       type = str, default = "SingleMuon")
parser.add_argument("--dataEra",    help = "Data era",              type = str, default = "C")
parser.add_argument("--options",    help = "Options",               type = str, default = ['noweight'], nargs = '+')
parser.add_argument("--year",       help = "Year",                  type = str, default = "2018")
parser.add_argument("--lepTag",     help = "Lepton tag",            type = str, default = "def", choices = ["bare", "loose", "def"])
parser.add_argument("--region",     help = "Region",                type = str, default = "none")
parser.add_argument("--minLepPt",   help = "Lower lepton pT cut",   type = str, default = None, choices = ['30', '40', '50'])
parser.add_argument("--maxLepPt",   help = "Upper lepton pT cut",   type = str, default = None, choices = ['30', '40', '50'])
parser.add_argument("--maxElePt",   help = "Upper electron pT cut", type = str, default = None, choices = ['30', '40', '50'])
parser.add_argument("--maxPtZ",     help = "Upper ptZ cut",         type = str, default = None, choices = ['20', '30', '50'])
parser.add_argument("--applyJetId", help = "Apply jet ID",          type = int, default = 0)
parser.add_argument("--oneLep",     help = "Exactly one lepton",    type = int, default = 1)
parser.add_argument("--variables",  help = "Variables to plot",     type = str, default = ["leadBasJetPt"],           nargs = '+')
parser.add_argument("--doFit",      help = "Do fit",                type = int, default = 1)
parser.add_argument("--doName",     help = "Write name",            type = int, default = 0)
parser.add_argument("--doBox",      help = "Draw box",              type = int, default = 0)
parser.add_argument("--logy",       help = "Toggle logy",           type = int, default = 0)
parser.add_argument("--save",       help = "Toggle save",           type = int, default = 1)
parser.add_argument("--verbose",    help = "Verbosity switch",      type = int, default = 0)
parser.add_argument("--matchJetTrigObj", help = "Match reco jet to trigger obj jet", type = int, default = 1)
args = parser.parse_args()
if not len(sys.argv) > 1:
    print makeLine()
    print "No arguments given. Using default settings."
    print makeLine()

# arguments
triggers   = args.triggers
dataset    = args.dataset
dataEra    = args.dataEra
options    = args.options
year       = args.year
lepTag     = args.lepTag
region     = args.region
minLepPt   = args.minLepPt
maxLepPt   = args.maxLepPt
maxElePt   = args.maxElePt
maxPtZ     = args.maxPtZ
applyJetId = args.applyJetId
oneLep     = args.oneLep
variables  = args.variables
doFit      = args.doFit
doName     = args.doName
doBox      = args.doBox
logy       = args.logy
save       = args.save
verbose    = args.verbose
matchJetTrigObj = args.matchJetTrigObj

# samples
if year == "2016":
    era = "Summer16"
    campaign = "05Feb2018"
elif year == "2017":
    era = "Fall17"
    campaign = "14Dec2018"
elif year == "2018":
    era = "Autumn18"
    campaign = "14Dec2018"
else:
    print "Wrong year %s. Exiting."%year
    sys.exit()

dataset_name = "%s_Run%s%s_%s"%(dataset, year, dataEra, campaign)
samplesList = [dataset_name]

skim = 'oneLep'
if dataset == 'MET':
    denTrig = 'HLT_PFMET120_PFMHT120_IDTight'
    if not variables:
        variables = ['lepPt']
    if "leadBasJetPt" in variables:
        denTrig = 'HLT_PFMET120_PFMHT120_IDTight && HLT_IsoMu24'
        plateauCuts = {'lepPt':30, 'metPt':100, 'leadBasJetPt':150}
    else:
        plateauCuts = {'lepPt':15, 'metPt':250, 'leadBasJetPt':150}
elif dataset == 'SingleMuon':
    skim = 'oneLepTight'
    denTrig = ['HLT_IsoMu24', 'HLT_IsoMu27']
    if not variables:
        variables = ['metPt', 'leadBasJetPt']
    plateauCuts = {'lepPt':30, 'metPt':250, 'leadBasJetPt':150}
elif dataset == 'EGamma':
    denTrig = 'HLT_Ele32_WPTight_Gsf'
    if not variables:
        variables = ['metPt', 'leadBasJetPt', 'lepPt']
    plateauCuts = {'lepPt':15, 'metPt':250, 'leadBasJetPt':150}
elif dataset == 'Charmonium':
    skim = 'twoLep'
    denTrig = ['HLT_DoubleMu4_3_Jpsi', 'HLT_Dimuon25_Jpsi', 'HLT_Dimuon25_Jpsi_noCorrL1', 'HLT_Dimuon0_Jpsi3p5_Muon2', 'HLT_DoubleMu2_Jpsi_DoubleTkMu0_Phi', 'HLT_DoubleMu2_Jpsi_DoubleTrk1_Phi1p05']
    if not variables:
        variables = ['metPt', 'leadBasJetPt', 'lepPt']
    plateauCuts = {'lepPt':15, 'metPt':250, 'leadBasJetPt':150}
elif dataset == 'DoubleMuon':
    skim = 'twoLepLoose'
    denTrig = ["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL", "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ", "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL", "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ", "HLT_TkMu17_TrkIsoVVL_TkMu8_TrkIsoVVL", "HLT_TkMu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ", "HLT_Mu30_TkMu11"]

    if not variables:
        variables = ['metPt', 'leadBasJetPt', 'lepPt']
    plateauCuts = {'lepPt':15, 'metPt':250, 'leadBasJetPt':150}
else:
    print "Wrong dataset. Exiting."
    sys.exit()

plateauTag = 'plateau_lepPt%s_metPt%s_leadBasJetPt%s'%(plateauCuts['lepPt'], plateauCuts['metPt'], plateauCuts['leadBasJetPt'])

if type(denTrig) == type([]):
    denTrig = '(%s)'%'||'.join(denTrig)

# cut and weight options
cutWeightOptions = getCutWeightOptions(
    lepCol = 'Lepton',
    lep = 'mu',
    lepTag = lepTag,
    year = year,
    dataset = dataset,
    campaign = campaign,
    options = options
    )

sampleDefPath = 'Workspace.DegenerateStopAnalysis.samples.nanoAOD_postProcessed.nanoAOD_postProcessed_' + era
sampleDef = importlib.import_module(sampleDefPath)

if dataset in ['EGamma', 'Charmonium']:
    ppDir = "/afs/hephy.at/data/mzarucki02/nanoAOD/DegenerateStopAnalysis/postProcessing/processing_RunII_v6_2/nanoAOD_v6_2-0"
elif dataset in ['SingleMuon', 'DoubleMuon']:
    if "metNoMuPt" in variables: 
        ppDir = "/afs/hephy.at/data/mzarucki02/nanoAOD/DegenerateStopAnalysis/postProcessing/processing_RunII_v6_4/nanoAOD_v6_4-0"
    else:
        ppDir = "/afs/hephy.at/data/mzarucki02/nanoAOD/DegenerateStopAnalysis/postProcessing/processing_RunII_v6_3/nanoAOD_v6_3-0"
elif dataset in ['MET']:
    ppDir = "/afs/hephy.at/data/mzarucki02/nanoAOD/DegenerateStopAnalysis/postProcessing/processing_RunII_v6_6/nanoAOD_v6_6-0"

mc_path     = ppDir + "/Autumn18_14Dec2018"
data_path   = ppDir + "/Run2018_14Dec2018"
signal_path = mc_path

PP = sampleDef.nanoPostProcessed(mc_path, signal_path, data_path)
samples = getSamples(PP = PP, skim = skim, sampleList = samplesList, scan = False, useHT = True, getData = True, settings = cutWeightOptions['settings'])

# cuts
#alt_vars = {'lepIndex':{'var':'Index{lepCol}_{lep}{lt}', 'latex':''}} # considering leading loose lepton
#alt_vars = {'lepPt':{'var':'{lepPt_loose}', 'latex':''}} # considering leading loose lepton

cuts_weights = CutsWeights(samples, cutWeightOptions)#, alternative_vars = alt_vars)
regDef = region
    
regDef = cuts_weights.cuts.addCut(regDef, 'lepEta_lt_1p5')
regDef = cuts_weights.cuts.addCut(regDef, 'leadBasJetEta_lt_2p4')

if minLepPt:
    regDef = cuts_weights.cuts.addCut(regDef, 'lepPt_gt_' + minLepPt)

if maxLepPt:
    regDef = cuts_weights.cuts.addCut(regDef, 'lepPt_lt_' + maxLepPt)

if maxElePt:
    regDef = cuts_weights.cuts.addCut(regDef, 'bareElePt_lt_' + maxLepPt)

if applyJetId:
    regDef = cuts_weights.cuts.addCut(regDef, 'leadBasJetId')

if matchJetTrigObj:
    regDef = cuts_weights.cuts.addCut(regDef, 'dRJetTrigObjJet_lt_0p15')
    #regDef = cuts_weights.cuts.addCut(regDef, 'dRminJetTrigObj_lt_0p3')

if oneLep:
    regDef = cuts_weights.cuts.addCut(regDef, 'exact1Lep')

if region == "Zpeak":
    regDef = cuts_weights.cuts.addCut(regDef, 'ptZ_lt_' + maxPtZ)

if 'leadBasJetPt' in variables: 
    regDef = cuts_weights.cuts.addCut(regDef, 'leadBasJetPt_lt_100')

cuts_weights.cuts._update(reset = False)
cuts_weights._update()

# save
if save:
    tag = samples[samples.keys()[0]].dir.split('/')[9]
    suff = '_' + '_'.join([tag, dataset, region])
    savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/softTrigEff/%s/%s/softTrigEff/%s/%s/%s/%s"%(tag, year, lepTag, dataset_name, regDef, plateauTag)

allTrig = [
    'HLT_Mu3er1p5_PFJet100er2p5_PFMET70_PFMHT70_IDTight',
    'HLT_Mu3er1p5_PFJet100er2p5_PFMET80_PFMHT80_IDTight',
    'HLT_Mu3er1p5_PFJet100er2p5_PFMET90_PFMHT90_IDTight',
    'HLT_Mu3er1p5_PFJet100er2p5_PFMET100_PFMHT100_IDTight',
    'HLT_Mu3er1p5_PFJet100er2p5_PFMETNoMu70_PFMHTNoMu70_IDTight',
    'HLT_Mu3er1p5_PFJet100er2p5_PFMETNoMu80_PFMHTNoMu80_IDTight',
    'HLT_Mu3er1p5_PFJet100er2p5_PFMETNoMu90_PFMHTNoMu90_IDTight',
    'HLT_Mu3er1p5_PFJet100er2p5_PFMETNoMu100_PFMHTNoMu100_IDTight'
    ]

if not triggers:
    triggers = allTrig

varStrings = cuts_weights.cuts.vars_dict_format
varNames = {'metPt':"E^{miss}_{T}", 'caloMetPt':"Calo. E^{miss}_{T}", 'metNoMuPt':"E^{miss}_{T} (#mu Sub.)", 'leadBasJetPt':"Leading Jet p_{T}", 'lepPt':"Muon p_{T}"} 
plateauCutStrings = {key:varStrings[key] + " > " + str(val) for key,val in plateauCuts.iteritems()} 

regCutStr = getattr(cuts_weights.cuts, regDef).combined

for trig in triggers:

    if save:
        makeDir("%s/%s/histos"%(savedir, trig))
        makeDir("%s/%s/root"%(savedir, trig))
        makeDir("%s/%s/pdf"%(savedir, trig))

    if trig == 'OR_ALL':
        trigCut = '(%s)'%'||'.join(allTrig)
    else:
        trigCut = trig

    for var in variables:
        denSelList = ["Flag_Filters", "run >= 315974", regCutStr, denTrig]

        # plateau cuts
        for cut in plateauCuts:
            if var not in ['caloMetPt', 'metNoMuPt']:
                if cut != var:
                    denSelList.append(plateauCutStrings[cut])
            else:
                if cut != 'metPt':
                    denSelList.append(plateauCutStrings[cut]) # NOTE: do not cut on MET when variable is CaloMET

        denSel = combineCutsList(denSelList)
        numSel = combineCuts(denSel, trigCut)

        cutString = numSel

        cutString += "&& TrigObj_id == 1"

        # Scan
        varGeneral = ["event"]
        varJet     = ["pt", "eta", "phi"]
        varTrigObj = ["pt", "eta", "phi"]#, "id", "filterBits"]
        
        jetIdx = "IndexJetClean_basJet_def[0]"       
        varJet     = ["JetClean_%s[%s]"%(x, jetIdx) for x in varJet]
        varTrigObj = ["TrigObj_" + x for x in varTrigObj]
 
        varExtra = []
        #varJet.insert(0, 'nJetClean_basJet_def')
        #varTrigObj.insert(0, 'nTrigObj')
        
        scanVars = ":".join(varGeneral+varJet+varTrigObj+varExtra)
        
        if verbose:
           print makeLine()
           print "Cut: ", cutString
           print makeLine()
           print "Variables: ", scanVars
           print makeLine()
        
        t = samples[dataset_name].tree

        if save:
           suff2 = '_%s_%s%s'%(trig, var, suff)

           t.SetScanField(0)
           t.GetPlayer().SetScanRedirect(True)
           t.GetPlayer().SetScanFileName(savedir + "/scan%s.txt"%suff2)
        
        t.Scan(scanVars, cutString)
