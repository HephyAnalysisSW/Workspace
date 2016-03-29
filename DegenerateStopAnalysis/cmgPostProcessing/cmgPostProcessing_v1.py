''' Post processing script for CMG ntuples. 

'''
    
# imports python standard modules or functions
import argparse
import logging
import sys
import tempfile
import os
import shutil
import pprint
import math
import time
import io
import importlib
import copy
import pickle
import operator

# imports user modules or functions

import ROOT

import Workspace.DegenerateStopAnalysis.tools.cmgObjectSelection as cmgObjectSelection
import Workspace.DegenerateStopAnalysis.tools.helpers as helpers

import Workspace.HEPHYPythonTools.helpers as hephyHelpers
import Workspace.HEPHYPythonTools.convertHelpers as convertHelpers

import Workspace.HEPHYPythonTools.user as user

from  veto_event_list import get_veto_list

def get_parser():
    ''' Argument parser for post-processing module.
    
    '''
     
    argParser = argparse.ArgumentParser(description = "Argument parser for cmgPostProcessing")
        
    argParser.add_argument('--logLevel', 
        action='store',
        nargs='?',
        choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'],
        default='INFO',
        help="Log level for logging"
        )
    
    argParser.add_argument('--verbose',
        action='store_true',
        help="Switch for print statements, for those who can not survive a job without seeing something printed " + 
            "on the screen. \n bool flag set to True if used")

    argParser.add_argument('--cmgTuples',
        dest='cmgTuples',
        action='store',
        nargs='?',
        type=str,
        default='RunIISpring15DR74_25ns',
        help="CMG ntuples to be post-processed"
        )
       
    argParser.add_argument('--processSamples',
        action='store',
        nargs='*',
        type=str,
        default='TTJets_LO',
        help="List of samples to be post-processed, given as CMG component name"
        )
    
    argParser.add_argument('--targetDir',
        action='store',
        nargs='?',
        type=str,
        default='/afs/hephy.at/data/' + user.afsDataName + '/cmgTuples',
        help="Name of the directory the post-processed files will be saved"
        )
    
    argParser.add_argument('--processingEra',
        action='store',
        nargs='?',
        type=str,
        default='postProcessed_mAODv2',
        help="Name of the processing era"
        )

    argParser.add_argument('--processingTag',
        action='store',
        nargs='?',
        type=str,
        default='v0',
        help="Name of the processing tag, preferably a tag for Workspace"
        )

    argParser.add_argument('--skim',
        action='store',
        nargs='?',
        type=str,
        default='',
        help="Skim conditions to be applied for post-processing"
        )
    
    argParser.add_argument('--skimLepton',
        action='store',
        nargs='?',
        type=str,
        choices=['soft', 'hard', 'inc', 'dilep'],
        default='inc',
        help="Lepton skimming to be applied for post-processing"
        )
    
    argParser.add_argument('--processSignalScan',
        action='store',
        nargs='*',
        type=str,
        default='',
        help="Do Processing for a specific Stop and LSP mass"
        )
    
    argParser.add_argument('--preselect',
        action='store_true',
        help="Apply preselection for the post processing, bool flag set to True if used"
        )
    
    argParser.add_argument('--processTracks',
        action='store_true',
        help="Process tracks for post-processing, bool flag set to True if used"
        )
    
    argParser.add_argument('--processGenTracks',
        action='store_true',
        help="Process packed generated particles for post-processing, bool flag set to True if used"
        )
     
    argParser.add_argument('--parameterSet',
        action='store',
        nargs='?',
        type=str,
        choices=['syncLip', 'analysisHephy'],
        default='analysisHephy',
        help="Selection of the parameter set used for post-processing." +\
            "\n The choices have to be pre-defined in getParameters function."
        )

    argParser.add_argument('--overwriteOutputFiles',
        action='store_true',
        help="Overwrite existing output files, bool flag set to True  if used")
    
    argParser.add_argument('--runSmallSample',
        action='store_true',
        help="Run the file on a small sample (for test purpose), bool flag set to True if used"
        )
    
    argParser.add_argument('--testMethods',
        action='store_true',
        help="Testing only the post-processing methods, without saving ROOT files, on runSmallSample files " + \
            "\n bool flag set to True if used. \n runSmallSample will be set automatically to True"
        )
    # 
    return argParser

def getParameterSet(args):
    '''Return a dictionary containing all the parameters used for post-processing.
    
    Define in this function all the parameters used for post-processing. 
    No hard-coded values are allowed in the functions, explicitly or via "default value"
    
    More sets of parameters can be defined, with the set used in a job chosen via the argument parser,
    with the argument --parameterSet. 
    '''

    # arguments to build the parameter set
    parameterSet = args.parameterSet
    processTracks = args.processTracks

    # parameter set definitions
        
    params = {}
    
    
    # target luminosity (fixed value, given here)
    
    params['target_lumi'] = 10000  # pb-1

    # skimmimg parameters
    
    SkimParameters = {
        'lheHThigh': {
            'lheHTIncoming': 600
            },
        'lheHTlow': {
            'lheHTIncoming': 600
            },
        
        }
    
    params['SkimParameters'] = SkimParameters
    
    
    # lepton selection

#     LepSel = {
#         'mu': {
#             'pdgId': 13,
#             'pt': 5,
#             'eta': 2.4,
#             'dxy': 0.05,
#             'dz': 0.2,
#             'sip3d': 4,
#             'mediumMuonId': 1,
#             'hybIso':{  'ptSwitch': 25, 'relIso': 0.2, 'absIso': 5  }
#             },
#         'el': {
#             'pdgId': 11,
#             'pt'   : 5,
#             'eta'  : 2.5,
#             'dxy'  : 0.05,
#             'dz'   : 0.2,
#             'sip3d': 4,
#             'SPRING15_25ns_v1': 1,
#             }
#         }
# 
#     LepSelPt30 = copy.deepcopy(LepSel)
#     LepSelPt30['mu']['ptMax'] = 30 
#     LepSelPt30['el']['ptMax'] = 30 


    LepSel = {
        'mu': {
            'pdgId': ('pdgId', operator.eq, 13),
            'pt': ('pt', operator.gt, 5),
            'eta': ('eta', operator.lt, 2.4, operator.abs),
            'dxy': ('dxy', operator.lt, 0.05, operator.abs),
            'dz': ('dz', operator.lt, 0.2, operator.abs),
            'sip3d': ('sip3d', operator.lt, 4),
            'mediumMuonId': ('mediumMuonId', operator.eq, 1),
            'hybIso': { 'ptSwitch': 25, 'relIso': 0.2, 'absIso': 5  },
            },
        'el': {
            'pdgId': ('pdgId', operator.eq, 11),
            'pt': ('pt', operator.gt, 5),
            'eta': ('eta', operator.lt, 2.5, operator.abs),
            'dxy': ('dxy', operator.lt, 0.05),
            'dz': ('dz', operator.lt, 0.2),
            'sip3d': ('sip3d', operator.lt, 4),
            'mediumMuonId': ('SPRING15_25ns_v1', operator.eq, 1),
            }
        }

    LepSelPt30 = copy.deepcopy(LepSel)
    LepSelPt30['mu']['ptMax'] = ('pt', operator.lt, 30) 
    LepSelPt30['el']['ptMax'] = ('pt', operator.lt, 30)


    if parameterSet == 'analysisHephy':
        params['LepSel'] = LepSel
    elif parameterSet == 'syncLip':
        params['LepSel'] = LepSelPt30
     
        
    # list of variables for muon and electron to be used for printing and flat tree
    
    varListMu = [
        'pdgId',
        'pt', 'eta', 'phi', 
        'dxy', 'dz', 'sip3d', 
        'miniRelIso', 'relIso03', 'relIso04', 
        'mediumMuonId'
        ]

    varListEl = [
        'pdgId',
        'pt', 'eta', 'phi', 
        'dxy', 'dz', 'sip3d', 
        'SPRING15_25ns_v1',
        ]
        
    varListLep = []
    for var in varListMu+varListEl:
        if var not in varListLep:
            varListLep.append(var)  
         
    # variables added for leptons, not available in the readTree, but computed for saveTree            
    varListLepExt = [
        'q80','cosLMet',
        'st', 'dPhi_Wl',
        'mt',
        'absIso',
        ]

        
    LepVarList = {
        'mu': varListMu,
        'el': varListEl,
        'lep': varListLep,
        'ext': varListLepExt,
        }

    params['LepVarList'] = LepVarList
    
    
    # jet selection
    #    bas: basic jets
    #    veto: jets used for QCD veto, selected from basic jets
    #    isr: ISR jets, selected from basic jets
    #    isrH: ISR jet, higher threshold for SR2, selected from basic jets
    #    bjet: b jets, tagged with algorithm btag, separated in soft and hard b jets 
        
#     JetSel = {
#         'bas': {
#             'id': 1,
#             'pt': 30,
#             'eta': 2.4,
#             },
#         'veto': {
#             'pt': 60,
#             },
#         'isr': {
#             'pt': 110,
#             },
#         'isrH': {
#             'pt': 325,
#             },
#         'bjet': {
#             'btag': {
#                 'alg': 'btagCSV',
#                 'cutDiscriminator': 0.890,
#                 },
#             'cutSoftHardBJets': 60
#             },
#         }

    # list of variables for jets to be used for printing and flat tree
    
    JetVarList = ['pt', 'eta', 'phi', 'btagCSV', 'id', 'mass']
    params['JetVarList'] = JetVarList

    JetSel = {
        'bas': {
            'id': ('id', operator.ge, 1),
            'pt': ('pt', operator.gt, 30),
            'eta': ('eta', operator.lt, 2.4, operator.abs),
            },
        'veto': {
            'pt': ('pt', operator.gt, 60),
            },
        'isr': {
            'pt': ('pt', operator.gt, 110),
            },
        'isrH': {
            'pt': ('pt', operator.gt, 325),
            },
        'bjet': {
            'btag': ('btagCSV', operator.gt, 0.890),
            },
        'bjetSep': {
            'ptSoftHard':  ('pt', operator.gt, 60),
            },
        }

    params['JetSel'] = JetSel


    # track selection
    
    if processTracks:
        params.update({
            'trackMinPtList' :  [1, 1.5, 2, 2.5, 3, 3.5],
            'hemiSectorList' :  [ 270, 180, 90, 60, 360],  # 360 is here just to as to doublecheck. It should also be the same for jets 1,12 and All
            'nISRsList'      :  ['1', '12', 'All'],
                    })
    else:
        params.update({
            'trackMinPtList' :  [],
            'hemiSectorList' :  [],
            'nISRsList'      :  [],
                    })


    #
    return params

def get_logger(logLevel, logFile):
    ''' Logger for post-processing module.
    
    '''

    # add TRACE (numerical level 5, less than DEBUG) to logging (similar to apache) 
    # see default levels at https://docs.python.org/2/library/logging.html#logging-levels
    logging.TRACE = 5
    logging.addLevelName(logging.TRACE, 'TRACE')
    
    logging.Logger.trace = lambda inst, msg, *args, **kwargs: inst.log(logging.TRACE, msg, *args, **kwargs)
    logging.trace = lambda msg, *args, **kwargs: logging.log(logging.TRACE, msg, *args, **kwargs)

    logger = logging.getLogger('cmgPostProcessing')

    numeric_level = getattr(logging, logLevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: %s" % logLevel)
     
    logger.setLevel(numeric_level)
    cmgObjectSelection.logger.setLevel(numeric_level)
     
    # create the logging file handler
    fileHandler = logging.FileHandler(logFile, mode='w')
 
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    fileHandler.setFormatter(formatter)
 
    # add handler to logger object
    logger.addHandler(fileHandler)
    cmgObjectSelection.logger.addHandler(fileHandler)
  
    # log the exceptions to the logger
    def excepthook(*args):
        logger.error("Uncaught exception:", exc_info=args)

    sys.excepthook = excepthook

    return logger

def retryRemove(function, path, excinfo):
    ''' Take a nap and try again.
    
    Address AFS/NSF problems with left-over lock files which prevents
    the 'shutil.rmtree' to delete the directory. The idea is to wait at most 20 sec
    for the fs to automatically remove these lock files and try again.
    Inspired from some GANGA code.
    
    '''   
    
    logger = logging.getLogger('cmgPostProcessing.retryRemove')
    
    for delay in 1, 3, 6, 10:
        
        if not os.path.exists(path): 
            break
        
        time.sleep(delay) 
        shutil.rmtree(path, ignore_errors=True)
        
    # 
    if not os.path.exists(path): 
        logger.debug("\n Path \n    %s \n deleted \n", path)  
    else:
        os.system("lsof +D " + path) 
        
        # not nice, but try to force - however, even 'rm -rf' can fail for 'Device or resource busy'
        os.system("rm -rf " + path)
        logger.debug("\n Try to delete path \n    %s \n by force using 'rm -rf' \n", path)  
    
    # last check before giving up  
    if os.path.exists(path): 
        exctype, value = excinfo[:2]
        logger.debug(
            "\n Unable to remove path \n    %s \n from the system." + \
            "\n Reason: %s:%s" + \
            "\n There might be some AFS/NSF lock files left over. \n", 
            path, exctype, value
            )
        

def getSamples(args):
    '''Return a list of components to be post-processed.
    
    No logger here, as the log file is determined with variables computed here.
    Simply exit if the required cmgTuples set or one of the samples do not exist, 
    printing the non-existing required set name.
    
    The sample processed will be written eventually in the logger,
    after a call to this function.
    
    Create also the output main directory, if it does not exist.
    '''

    cmgTuples = args.cmgTuples
    processSamples = args.processSamples
    
    targetDir = args.targetDir
    processingEra = args.processingEra
    processingTag = args.processingTag



    if cmgTuples == "Data_25ns":
        # from Workspace.DegenerateStopAnalysis.cmgTuples_Data25ns import *
        #import Workspace.DegenerateStopAnalysis.cmgTuples_Data25ns as cmgSamples
        import Workspace.DegenerateStopAnalysis.samples.cmgTuples_Data25ns_scan as cmgSamples
    elif cmgTuples == "Data_50ns":
        import Workspace.DegenerateStopAnalysis.samples.cmgTuples_Data50ns_1l as cmgSamples
    elif cmgTuples == "RunIISpring15DR74_25ns":
        import Workspace.DegenerateStopAnalysis.samples.cmgTuples_Spring15_7412pass2_mAODv2_v4 as cmgSamples
    elif cmgTuples == "RunIISpring15DR74_50ns":
        import Workspace.DegenerateStopAnalysis.samples.cmgTuples_Spring15_50ns as cmgSamples
    else:
        # use the cmgTuples values to find the cmgSamples definition file
        moduleName = 'cmgTuples_'  + cmgTuples
        moduleFullName = 'Workspace.DegenerateStopAnalysis.samples.' + moduleName
        
        cmssw_base = os.environ['CMSSW_BASE']
        sampleFile = os.path.join(cmssw_base, 'src/Workspace/DegenerateStopAnalysis/python/samples') + \
            '/' + moduleName + '.py'

        try:
            cmgSamples = importlib.import_module(moduleFullName)
        except ImportError, err:      
            print 'ImportError:', err
            print "\n The required set of CMG tuples \n cmgTuples: {0} \n ".format(cmgTuples) + \
                "with expected sample definition file \n {0} \n does not exist.".format(sampleFile), \
                "\n Correct the name and re-run the script. \n Exiting."
            sys.exit()
   

    if args.preselect:
        outDir = os.path.join(targetDir, processingEra, processingTag, cmgTuples, args.skim, 'preselection',  args.skimLepton )
    else:
        outDir = os.path.join(targetDir, processingEra, processingTag, cmgTuples, args.skim, args.skimLepton )
    

    # samples
    
    allComponentsList = [] 
    
    #processSamples = processSamples.replace(' ', '')
    #if len(processSamples):
    #    processSamplesList = processSamples.split(',')
        
    processSamplesList = processSamples
    for sampleName in processSamplesList:
        foundSample = False
        
        # cmgSamples.samples contains components or list of components  
        try:
            sampleRequested = getattr(cmgSamples, sampleName)
            
            if isinstance(sampleRequested, dict):
                # single component
                if (sampleName == sampleRequested['cmgComp'].name):
                    allComponentsList.append(sampleRequested)
                    foundSample = True
                    continue      
                else:
                    print "WARNING:  Sample name is not consistant with the cmgComp name"
            elif isinstance(sampleRequested, list):
                # list of components - add all components
                for comp in sampleRequested:
                        allComponentsList.append(comp)
                        foundSample = True
                continue 
            else:
                print "\n Not possible to build list of components for {0} .".format(sampleName), \
                "\n Exiting."
                print "Requested Sample:", sampleRequested
                sys.exit()
                
                    
        except AttributeError:
            sampleRequested = cmgSamples.samples + cmgSamples.allSignals

            if isinstance(sampleRequested, dict):
                # single component
                if (sampleName == sampleRequested['cmgComp'].name):
                    allComponentsList.append(sampleRequested)
                    foundSample = True
                    break            
            elif isinstance(sampleRequested, list):
                # list of components
                for comp in sampleRequested:
                    print "\n sampleRequested \n", (pprint.pformat(comp)), "\n"
                    if (sampleName == comp['cmgComp'].name):
                        allComponentsList.append(comp)
                        foundSample = True
                        break 
            else:
                print "\n Not possible to build list of components for {0}".format(sampleName), \
                "\n Exiting."
                sys.exit()
                
                
        
        if not foundSample:
            print "\n List of available samples in cmgTuples set {0}: \n {1} \n".format(
                cmgTuples, pprint.pformat(cmgSamples.samples)
                )
            print "\n List of available signal samples in cmgTuples set {0}: \n {1} \n".format(
                cmgTuples, pprint.pformat(cmgSamples.allSignals)
                )
                    
            print "\n Requested sample {0} not available in CMG samples.".format(sampleName), \
                "\n Re-run the job with existing samples.", \
                "\n Exiting."
            sys.exit() 
    
    # create the target output directory, if it does not exist, if sample definition is OK
    if not os.path.exists(outDir):
        os.makedirs(outDir)

    if hasattr(cmgSamples,"mass_dict"):
        mass_dict = cmgSamples.mass_dict
    else:
        mass_dict = {}


    #    
    return allComponentsList, outDir, mass_dict
    

 
def getSignalScanSamples(args):


    #for mstop in mass_dict.keys():
    #    for mlsp in mass_dict[mstop].keys():
    #        skimCond = "Sum$(abs(GenPart_pdgId)==1000022&&abs(GenPart_motherId)==1000024&&abs(GenPart_grandmotherId)==1000021)==2&&(Sum$(abs(GenPart_pdgId)==24)==2)"
    #        skimCond += "(GenSusyMStop==%s) && (GenSusyMNeutralino==%s) "%(mstop,mlsp)
    #        outDir   = ""     


    mstop=args.processSignalScan[0]
    mlsp =args.processSignalScan[1]




def eventsSkimPreselect(skimName, skimLepton, preselectFlag, params, signalMasses=[]):
    '''Define the skim condition, including preselection if required.
    
    The skim condition depends on the skim name, the lepton skim selection, and on the
    event preselection. 
    
    FIXME remove hardcoded values, read them from params
    '''

    logger = logging.getLogger('cmgPostProcessing.eventsSkimPreselect')
    
    skimCond = "(1)"
    
    if not skimName:
        pass
    elif skimName.startswith('met'):
        skimCond = "met_pt>" + str(float(skimName[3:]))
    elif skimName == 'HT400':
        skimCond = "Sum$(Jet_pt)>400"
    elif skimName == 'HT400ST200': 
        skimCond = "Sum$(Jet_pt)>400&&(LepGood_pt[0]+met_pt)>200"
    elif skimName == 'lheHThigh': 
        skimCond += "&&(lheHTIncoming>=600)"
    elif skimName == 'lheHTlow': 
        skimCond += "&&(lheHTIncoming<600)"
    else:
        raise Exception("Skim Condition Not recognized: %s"%skimName)
        pass
    
    # lepton skimming, loop only over events fulfilling the lepton skimming condition 
    if skimLepton == 'inc':
        # no lepton skim selection is applied for the inclusive skim 
        skimCond += ""
    else:
        pass
    
    # for inclusive skim, no skim selection is done, the skim condition is reset 
    if skimName == 'inc':
        skimCond = "(1)"
      
    logger.info("\n Jobs running with skim = '%s' \n Skimming condition: \n  %s \n ", skimName, skimCond)
    
    if preselectFlag:
        metCut = "(met_pt>200)"
        leadingJet100 = "((Max$(Jet_pt*(abs(Jet_eta)<2.4 && Jet_id) ) > 100 ) >=1)"
        HTCut    = "(Sum$(Jet_pt*(Jet_pt>30 && abs(Jet_eta)<2.4 && (Jet_id)) ) >200)"

        preselectionCuts = "(%s)"%'&&'.join([metCut,leadingJet100,HTCut])
        skimCond += "&&%s"%preselectionCuts

        logger.info("\n Applying preselection cuts: %s ", preselectionCuts)
        logger.info("\n Skimming condition with preselection: \n  %s \n", skimCond)
    else:
        logger.info("\n No preselection cuts are applied for skim %s \n Skimming condition unchanged \n", skimName)
        pass

    if signalMasses:
        mstop = signalMasses[0]
        mlsp  = signalMasses[1]
        skimCond +="&& (GenSusyMStop==%s && GenSusyMNeutralino==%s)"%(mstop,mlsp)
        logger.info("\n Processing Signal Scan for MStop:%s  MLSP: %s "%(mstop, mlsp ))
        

    #
    return skimCond

 
 
def rwTreeClasses(sample, isample, args, temporaryDir, params={} ):
    '''Define the read / write tree classes for data and MC.
    
    '''
    logger = logging.getLogger('cmgPostProcessing.rwTreeClasses')
    
    # define the branches and the variables to be kept and/or read for data and MC
    
    # MC samples only
    
    # common branches already defined in cmgTuples
    branchKeepStrings_MC = [ 
        'nTrueInt', 'genWeight', 'xsec', 'puWeight', 
        'GenSusyMScan1', 'GenSusyMScan2', 'GenSusyMScan3', 'GenSusyMScan4', 'GenSusyMGluino', 
        'GenSusyMGravitino', 'GenSusyMStop', 'GenSusyMSbottom', 'GenSusyMStop2', 'GenSusyMSbottom2', 
        'GenSusyMSquark', 'GenSusyMNeutralino', 'GenSusyMNeutralino2', 'GenSusyMNeutralino3', 
        'GenSusyMNeutralino4', 'GenSusyMChargino', 'GenSusyMChargino2', 
        'ngenLep', 'genLep_*', 
        'nGenPart', 'GenPart_*',
        'ngenPartAll','genPartAll_*',
        'ngenTau', 'genTau_*', 
        'ngenLepFromTau', 'genLepFromTau_*', 
        'GenJet_*',
        'GenTracks_*',
                          ]
    
    readVariables_MC = []
    aliases_MC = []
    newVariables_MC = []
    
    readVectors_MC = []
    
    aliases_MC.extend(['genMet:met_genPt', 'genMetPhi:met_genPhi'])
    
    
    # data and MC samples 
    
    # common branches already defined in cmgTuples

    trackMinPtList = params['trackMinPtList'] 
    hemiSectorList = params['hemiSectorList']
    nISRsList      = params['nISRsList']


    branchKeepStrings_DATAMC = [
        'run', 'lumi', 'evt', 'isData', 'rho', 'nVert', 
        'nJet25', 'nBJetLoose25', 'nBJetMedium25', 'nBJetTight25', 
        'nJet40', 'nJet40a', 'nBJetLoose40', 'nBJetMedium40', 'nBJetTight40', 
        'nLepGood20', 'nLepGood15', 'nLepGood10', 
        'htJet25', 'mhtJet25', 'htJet40j', 'htJet40', 'mhtJet40', 
        'nSoftBJetLoose25', 'nSoftBJetMedium25', 'nSoftBJetTight25', 
        'met*','puppi*',
        'Flag_*','HLT_*',
        #'MET*','PFMET*','Calo*', 'Mono*', 'Mu*','TkMu*','L1Single*', 'L2Mu*',
        #'nFatJet','FatJet_*', 
        'nJet', 'Jet_*', 
        'nLepGood', 'LepGood_*', 
        'nLepOther', 'LepOther_*', 
        'nTauGood', 'TauGood_*',
        'Tracks_*', 'isoTrack_*',
        ] 
    
    readVariables_DATAMC = []
    aliases_DATAMC = []
    newVariables_DATAMC = []
    readVectors_DATAMC = []
    

    
    readVariables_DATAMC.extend(['met_pt/F', 'met_phi/F'])
    aliases_DATAMC.extend([ 'met:met_pt', 'metPhi:met_phi'])
    newVariables_DATAMC.extend(['weight/F'])
    
    readVectors_DATAMC.extend([
        {'prefix':'LepOther',  'nMax':8, 
            'vars':['pt/F', 'eta/F', 'phi/F', 'pdgId/I', 'relIso03/F', 'tightId/I', 
                    'miniRelIso/F', 'mass/F','sip3d/F',
                    'mediumMuonId/I', 'SPRING15_25ns_v1/I', 
                    'dxy/F', 'dz/F',  'relIso04/F',
                    'mvaIdPhys14/F','lostHits/I', 'convVeto/I']},
        {'prefix':'LepGood',  'nMax':8, 
            'vars':['pt/F', 'eta/F', 'phi/F', 'pdgId/I', 'relIso03/F', 'tightId/I', 
                    'miniRelIso/F', 'mass/F','sip3d/F',
                    'mediumMuonId/I', 'SPRING15_25ns_v1/I', 
                    'dxy/F', 'dz/F',  'relIso04/F',
                    'mvaIdPhys14/F','lostHits/I', 'convVeto/I']},
        {'prefix':'Jet',  'nMax':100, 
            'vars':['pt/F', 'eta/F', 'phi/F', 'id/I','btagCSV/F', 'btagCMVA/F', 'mass/F']},
        {'prefix':'GenPart',  'nMax':30, 
            'vars':['pt/F', 'eta/F', 'phi/F', 'pdgId/I', 'mass/F', 'motherId/I' ]},
      ])
     
    if args.skimLepton in ['soft', 'hard', 'inc']:
        
        newVariables_DATAMC.extend([
            'nBJetMediumCSV30/I', 'nSoftBJetsCSV/F', 'nHardBJetsCSV/F',  
            'nJet30/I','htJet30j/F','nJet60/I','nJet100/I', 'nJet110/I','nJet325/I',
            ])
        
        newVariables_DATAMC.extend([
            'nLooseSoftLeptons/I', 'nLooseSoftPt10Leptons/I', 'nLooseHardLeptons/I', 
            'nTightSoftLeptons/I', 'nTightHardLeptons/I',
            ])
        
        newVariables_DATAMC.extend([
            'singleMuonic/I', 'singleElectronic/I', 'singleLeptonic/I', 
            ])
        
        newVariables_DATAMC.extend([
            'leptonPt/F','leptonMiniRelIso/F','leptonRelIso03/F',
            'leptonEta/F',  'leptonPhi/F', 'leptonPdg/I/0', 'leptonInd/I/-1', 
            'leptonMass/F', 'leptonDz/F', 'leptonDxy/F', 
            
            'lepGoodPt/F','lepGoodMiniRelIso/F','lepGoodRelIso03/F', 'lepGoodRelIso04/F',
            'lepGoodAbsIso/F','lepGoodEta/F',  'lepGoodPhi/F', 'lepGoodPdgId/I/0', 'lepGoodInd/I/-1', 
            'lepGoodMass/F', 'lepGoodDz/F', 'lepGoodDxy/F','lepGoodMediumMuonId/I','lepGoodSip3d/F',
            
            'lepOtherPt/F','lepOtherMiniRelIso/F','lepOtherRelIso03/F', 'lepOtherRelIso04/F',
            'lepOtherAbsIso/F','lepOtherEta/F',  'lepOtherPhi/F', 'lepOtherPdgId/I/0', 'lepOtherInd/I/-1', 
            'lepOtherMass/F', 'lepOtherDz/F', 'lepOtherDxy/F','lepOtherMediumMuonId/I','lepOtherSip3d/F',
            
            'lepPt/F','lepMiniRelIso/F','lepRelIso03/F', 'lepRelIso04/F',
            'lepAbsIso/F','lepEta/F',  'lepPhi/F', 'lepPdgId/I/0', 'lepInd/I/-1', 
            'lepMass/F', 'lepDz/F', 'lepDxy/F','lepMediumMuonId/I','lepSip3d/F',
            'nlep/I',


            "Flag_Veto_Event_List/I/1",

            ])
            
        newVariables_DATAMC.extend([
            'Q80/F','CosLMet/F',
            'st/F', 'deltaPhi_Wl/F',
            'mt/F',
            ])
              
        newVariables_DATAMC.extend([
            'jet1Pt/F','jet1Eta/F','jet1Phi/F', 
            'jet2Pt/F','jet2Eta/F','jet2Phi/F',
            'deltaPhi_j12/F', 'dRJet1Jet2/F','deltaPhi30_j12/F', 'deltaPhi60_j12/F',
            'JetLepMass/F','dRJet1Lep/F',
            'J3Mass/F',


            "stopIndex1/I/-1", "stopIndex2/I/-1",
            "lspIndex1/I/-1", "lspIndex2/I/-1",
            "gpLepIndex1/I/-1", "gpLepIndex2/I/-1",
            "gpBIndex1/I/-1", "gpBIndex2/I/-1",
            "stops_pt/F/-1", "stops_eta/F/-999", "stops_phi/F/-999", 
            "lsps_pt/F/-1", "lsps_eta/F/-999", "lsps_phi/F/-999", 

        
            "jet1Index/I", "jet2Index/I", "jet3Index/I", 
            "b1Index/I", "b2Index/I",
            "nMuons/I", "nElectrons/I", "nLeptons/I",
            "looseMuonIndex1/I", "looseMuonIndex2/I",
            "looseElectronIndex1/I", "looseElectronIndex2/I",             
            "looseLeptonIndex1/I", "looseLeptonIndex2/I",
            ])
        
        #newVariables_DATAMC.extend([
        #    'mt2w/F'
        #    ] )
    
    
    if args.processTracks:
        trkVar="Tracks"
        trkCountVars = [ "n%s"%trkVar ] 
        trkCountVars.extend([ 
                    "n%sOpp%sJet%s"%(trkVar,hemiSec,nISRs) for hemiSec in hemiSectorList  for nISRs in nISRsList     
                    ])
        newTrackVars = []
        for minTrkPt in trackMinPtList:
            ptString = str(minTrkPt).replace(".","p")
            newTrackVars.extend( [ x+"_pt%s"%ptString+"/I" for x in  trkCountVars  ] )
        newVariables_DATAMC.extend(newTrackVars) 
        readVectors_DATAMC.append(
            {'prefix':'Tracks', 'nMax':300, 
                'vars':[
                          'pt/F', 'eta/F', 'phi/F', "dxy/F", "dz/F", 'pdgId/I', 'fromPV/I', 
                          "matchedJetIndex/I", "matchedJetDr/F", "CosPhiJet1/F", "CosPhiJet12/F", "CosPhiJetAll/F",
                          "mcMatchId/I", "mcMatchIndex/I", "mcMatchPtRatio/F", "mcMatchDr/F"
                       ]   })
                      


    if args.processGenTracks:
        genTrkVar="GenTracks"
        genTrkCountVars = [ "n%s"%genTrkVar ] 
        genTrkCountVars.extend([ 
                    "n%sOpp%sJet%s"%(genTrkVar,hemiSec,nISRs) for hemiSec in hemiSectorList  for nISRs in nISRsList     
                    ])
        newGenTrackVars = []
        for minGenTrkPt in trackMinPtList:
            ptString = str(minGenTrkPt).replace(".","p")
            newGenTrackVars.extend( [ x+"_pt%s"%ptString+"/I" for x in  genTrkCountVars  ] )
        newVariables_DATAMC.extend(newGenTrackVars)        
        readVectors_MC.append(
            {'prefix':genTrkVar, 'nMax':300, 
                'vars':[
                          'pt/F', 'eta/F', 'phi/F', "dxy/F", "dz/F", 'pdgId/I', 'fromPV/I', 
                          "matchedJetIndex/I", "matchedJetDr/F", "CosPhiJet1/F", "CosPhiJet12/F", "CosPhiJetAll/F",
                          "mcMatchId/I", "mcMatchIndex/I", "mcMatchPtRatio/F", "mcMatchDr/F"
                       ]})
        readVectors_MC.extend([
            {'prefix':'GenJet', 'nMax':100, 'vars':['pt/F', 'eta/F', 'phi/F', 'mass/F' ] },
            ])
   


 
    
    # data samples only
    
    # branches already defined in cmgTuples
    branchKeepStrings_DATA = []
    
    readVariables_DATA = []
    aliases_DATA = []
    newVariables_DATA = []
    
    readVectors_DATA = []
 

    # sample dependent part
    
    if sample['isData']: 
        branchKeepStrings = branchKeepStrings_DATAMC + branchKeepStrings_DATA
    
        readVariables = readVariables_DATAMC + readVariables_DATA
        aliases = aliases_DATAMC + aliases_DATA
        readVectors = readVectors_DATAMC + readVectors_DATA
        newVariables = newVariables_DATAMC + newVariables_DATA
    else:
        branchKeepStrings = branchKeepStrings_DATAMC + branchKeepStrings_MC
    
        readVariables = readVariables_DATAMC + readVariables_MC
        aliases = aliases_DATAMC + aliases_MC
        readVectors = readVectors_DATAMC + readVectors_MC
        newVariables = newVariables_DATAMC + newVariables_MC


    readVars = [convertHelpers.readVar(v, allowRenaming=False, isWritten=False, isRead=True) for v in readVariables]
    newVars = [convertHelpers.readVar(v, allowRenaming=False, isWritten = True, isRead=False) for v in newVariables]
  
    for v in readVectors:
        readVars.append(convertHelpers.readVar('n'+v['prefix']+'/I', allowRenaming=False, isWritten=False, isRead=True))
        v['vars'] = [convertHelpers.readVar(
            v['prefix']+'_'+vvar, allowRenaming=False, isWritten=False, isRead=True) for vvar in v['vars']
            ]

    newVectors = []
    
    # extend LepGood with additional quantities
    newVectors.extend([
        {'prefix':'LepGood', 'nMax':8, 
            'vars':[
                'q80/F','cosLMet/F',
                'st/F', 'dPhi_Wl/F',
                'mt/F',
                'absIso/F',
                ] 
         },
        ])

    for v in newVectors:
        v['vars'] = [convertHelpers.readVar(
            v['prefix']+'_'+vvar, allowRenaming=False, isWritten=True, isRead=False
            ) for vvar in v['vars']
            ]

    logger.debug("\n read variables (readVars) definition: \n %s \n", pprint.pformat(readVars))
    logger.debug("\n aliases definition: \n %s \n", pprint.pformat(aliases))
    logger.debug("\n read vectors (readVectors) definition: \n %s \n", pprint.pformat(readVectors))
    logger.debug("\n new variable (newVars) definition: \n %s \n", pprint.pformat(newVars))
    logger.debug("\n new vectors (newVectors) definition: \n %s \n", pprint.pformat(newVectors))

    convertHelpers.printHeader("Compiling class to write")
    writeClassName = "ClassToWrite_"+str(isample)
    writeClassString = convertHelpers.createClassString(className=writeClassName, vars= newVars, vectors=newVectors, 
        nameKey = 'stage2Name', typeKey = 'stage2Type')
    logger.debug("\n writeClassString definition: \n%s \n", writeClassString)
    saveTree = convertHelpers.compileClass(className=writeClassName, classString=writeClassString, tmpDir=temporaryDir)

    readClassName = "ClassToRead_"+str(isample)
    readClassString = convertHelpers.createClassString(className=readClassName, vars=readVars, vectors=readVectors, 
        nameKey = 'stage1Name', typeKey = 'stage1Type', stdVectors=False)
    convertHelpers.printHeader("Class to Read")
    logger.debug("\n readClassString definition: \n%s \n", readClassString)
    readTree = convertHelpers.compileClass(className=readClassName, classString=readClassString, tmpDir=temporaryDir)

    #
    return branchKeepStrings, readVars, aliases, readVectors, newVars, newVectors, readTree, saveTree
   
   
def getTreeFromChunk(c, skimCond, iSplit, nSplit):
    '''Get a tree from a chunck.
    
    '''
     
    logger = logging.getLogger('cmgPostProcessing.getTreeFromChunk')
   
    if not c.has_key('file'):return
    rf = ROOT.TFile.Open(c['file'])
    assert not rf.IsZombie()
    rf.cd()
    tc = rf.Get('tree')
    nTot = tc.GetEntries()
    fromFrac = iSplit/float(nSplit)
    toFrac   = (iSplit+1)/float(nSplit)
    start = int(fromFrac*nTot)
    stop  = int(toFrac*nTot)
    ROOT.gDirectory.cd('PyROOT:/')

    logger.debug(
        "\n Copy tree from source. Statistics before skimming and preselection: " + \
        "\n    total number of events found: %i " + \
        "\n    split counter: %i < %i, first event: %i, last event %i (%i events) \n",
        nTot, iSplit, nSplit, start, stop, stop-start)

    t = tc.CopyTree(skimCond,"",stop-start,start)
    
    nTotSkim = t.GetEntries()
    logger.debug(
        "\n Statistics after skimming and preselection: " + \
        "\n    total number of events found: %i \n",
        nTotSkim)

    tc.Delete()
    del tc
    rf.Close()
    del rf
    return t



def processGenSusyParticles(readTree,splitTree,saveTree):


    genPart           =  cmgObjectSelection.cmgObject(readTree, splitTree, "GenPart")

    stopIndices       =  genPart.getSelectionIndexList( readTree,
                            lambda readTree, gp, igp: abs( gp.pdgId[igp] ) == 1000006
                            )
    if len(stopIndices)==0:    # not a susy event... move on
        return 


    isrIndices       =  genPart.getSelectionIndexList( readTree,
                            lambda readTree, gp, igp: abs( gp.pdgId[igp] ) != 1000006 and gp.motherId==-9999
                            )
    lspIndices        =  genPart.getSelectionIndexList( readTree,
                            lambda readTree, gp, igp: abs( gp.pdgId[igp] ) == 1000022
                            )
    bIndices          =  genPart.getSelectionIndexList( readTree,
                            lambda readTree, gp, igp: abs( gp.pdgId[igp] ) == 5
                            )
    lepIndices        =  genPart.getSelectionIndexList( readTree,
                            lambda readTree, gp, igp: abs( gp.pdgId[igp] ) in [11,13]
                            )

    saveTree.stopIndex1 = stopIndices[0]
    saveTree.stopIndex2 = stopIndices[1]

    saveTree.lspIndex1 = lspIndices[0]
    saveTree.lspIndex2 = lspIndices[1]
    saveTree.gpBIndex1 = bIndices[0]
    saveTree.gpBIndex2 = bIndices[1]
    saveTree.gpLepIndex1 = lepIndices[0] if len(lepIndices) >0 else -1
    saveTree.gpLepIndex2 = lepIndices[1] if len(lepIndices) >1 else -1 

    stop1_lv = ROOT.TLorentzVector()
    stop2_lv = ROOT.TLorentzVector()

    stop1_lv.SetPtEtaPhiM( genPart.pt[saveTree.stopIndex1], genPart.eta[saveTree.stopIndex1], genPart.phi[saveTree.stopIndex1], genPart.mass[saveTree.stopIndex1]  )
    stop2_lv.SetPtEtaPhiM( genPart.pt[saveTree.stopIndex2], genPart.eta[saveTree.stopIndex2], genPart.phi[saveTree.stopIndex2], genPart.mass[saveTree.stopIndex2]  )

    stops = stop1_lv + stop2_lv

    saveTree.stops_pt = stops.Pt()
    saveTree.stops_eta = stops.Eta()
    saveTree.stops_phi = stops.Phi()



    lsp1_lv = ROOT.TLorentzVector()
    lsp2_lv = ROOT.TLorentzVector()
    lsp1_lv.SetPtEtaPhiM( genPart.pt[saveTree.lspIndex1], genPart.eta[saveTree.lspIndex1], genPart.phi[saveTree.lspIndex1], genPart.mass[saveTree.lspIndex1]  )
    lsp2_lv.SetPtEtaPhiM( genPart.pt[saveTree.lspIndex2], genPart.eta[saveTree.lspIndex2], genPart.phi[saveTree.lspIndex2], genPart.mass[saveTree.lspIndex2]  )
    lsps = lsp1_lv + lsp2_lv
    saveTree.lsps_pt = lsps.Pt()
    saveTree.lsps_eta = lsps.Eta()
    saveTree.lsps_phi = lsps.Phi()


def processLeptons(readTree, splitTree, saveTree, params):
    '''Process leptons. 
    
    TODO describe here the processing.
    '''

    logger = logging.getLogger('cmgPostProcessing.processLeptons')
    
    # initialize returned variables (other than saveTree)
    
    lepObj = None
    
    # lepton selection
    
    objBranches = 'LepGood'
    lepObj = cmgObjectSelection.cmgObject(readTree, splitTree, objBranches)
    
    LepVarList = params['LepVarList'] 
    LepSel = params['LepSel']
    
    # compute the additional quantities for leptons
    
    for lepIndex in range(lepObj.nObj):
        
        lepPt = getattr(lepObj, 'pt')[lepIndex]
        lepPhi = getattr(lepObj, 'phi')[lepIndex]
        lepRelIso04 = getattr(lepObj, 'relIso04')[lepIndex]

        q80 = 1 - 80 ** 2 / (2 * lepPt * readTree.met_pt)
        cosLMet = math.cos(lepPhi - readTree.met_phi)
    
        mt = math.sqrt(2 * lepPt * readTree.met_pt * (1 - cosLMet))
        st = readTree.met_pt + lepPt
  
        dPhi_Wl = math.acos(
            (lepPt + readTree.met_pt * math.cos(lepPhi - readTree.met_phi)) / 
            (math.sqrt(lepPt ** 2 + readTree.met_pt ** 2 + 
                      2 * readTree.met_pt * lepPt * math.cos(lepPhi - readTree.met_phi))
                )
            ) 
        
        absIso = lepRelIso04 * lepPt
    
        saveTree.LepGood_q80[lepIndex] = q80
        saveTree.LepGood_cosLMet[lepIndex] = cosLMet
        saveTree.LepGood_mt[lepIndex] = mt
        saveTree.LepGood_st[lepIndex] = st
        saveTree.LepGood_dPhi_Wl[lepIndex] = dPhi_Wl
        saveTree.LepGood_absIso[lepIndex] = absIso 
        
              
    if logger.isEnabledFor(logging.DEBUG):
        printStr = "\n List of " + objBranches + " leptons before selector: " + \
            lepObj.printObjects(None, LepVarList['lep'])

        for ind in range(lepObj.nObj):
            printStr += "\n Extended quantities for " + objBranches + " leptons before selector: " + \
            "\n Lepton index {0}: \n".format(ind)
            for var in LepVarList['ext']:
                varName = objBranches + '_' + var
                varValue = getattr(saveTree, varName)[ind]
                printStr += varName + " = " + str(varValue) + '\n'
            printStr += '\n'
            
        logger.debug(printStr)
        

    muSelector = cmgObjectSelection.objSelectorFunc(LepSel['mu'] )
    elSelector = cmgObjectSelection.objSelectorFunc(LepSel['el'])

    muList = lepObj.getSelectionIndexList(readTree, muSelector)
    elList = lepObj.getSelectionIndexList(readTree, elSelector)
    # TODO how to put electrons and muons together
    lepList = []
 
    saveTree.nMuons = len(muList)
    saveTree.looseMuonIndex1 = muList[0] if saveTree.nMuons > 0 else -1
    saveTree.looseMuonIndex2 = muList[1] if saveTree.nMuons > 1 else -1

    saveTree.nElectrons = len(elList)
    saveTree.looseElectronIndex1 = elList[0] if saveTree.nElectrons > 0 else -1
    saveTree.looseElectronIndex2 = elList[1] if saveTree.nElectrons > 1 else -1

    saveTree.nLeptons = len(lepList)
    saveTree.looseLeptonIndex1 = lepList[0] if saveTree.nLeptons > 0 else -1
    saveTree.looseLeptonIndex2 = lepList[1] if saveTree.nLeptons > 1 else -1

    saveTree.singleLeptonic = (saveTree.nLeptons == 1)
    saveTree.singleMuonic = (saveTree.nLeptons == 1)
    saveTree.singleElectronic = (saveTree.nLeptons == 1)

    
    if logger.isEnabledFor(logging.DEBUG):

        printStr = "\n  " + objBranches + " muon selector \n " + \
            pprint.pformat(LepSel['mu']) + \
            '\n ' + lepObj.printObjects(muList, LepVarList['mu'])
        logger.debug(printStr)

        printStr = "\n  " + objBranches + " electron selector \n " + \
            pprint.pformat(LepSel['el']) + \
            '\n ' + lepObj.printObjects(elList, LepVarList['el'])
        logger.debug(printStr)

        printStr = '\n ' + lepObj.printObjects(lepList, LepVarList['lep'])
        logger.debug(printStr)
        

    if muList:
        lepName = "lep"
        for var in LepVarList['mu']:
            varValue = getattr(lepObj, var)[muList[0]]
            varName = lepName + var[0].capitalize() + var[1:]
            setattr(saveTree, varName, varValue)
        saveTree.lepAbsIso = getattr(saveTree, 'lepRelIso04') * getattr(saveTree, 'lepPt') 
        saveTree.nlep = len(muList)
         
        if logger.isEnabledFor(logging.DEBUG):
            logString = "\n Leading selected muon: "
            for var in LepVarList['mu']:
                logString += "\n " + lepName + var[0].capitalize() + var[1:] + " = %f"
            logString = logString % \
                (tuple((getattr(saveTree, lepName + var[0].capitalize() + var[1:]) for var in LepVarList['mu'])))
            logString +=  "\n " + "lepAbsIso" + " = %f"
            logString += "\n"
            logger.debug(logString, saveTree.lepAbsIso)
    
        
    #
    return saveTree, lepObj, muList

def selectionJets(readTree, ptCut,etaCut=2.4):
    '''Post-processing standard jet selection. 
    
    '''
    
    jetVariables = ['eta', 'pt', 'phi', 'btagCMVA', 'btagCSV', 'id', 'mass']

    jets = filter(lambda j:
        j['pt'] > ptCut and abs(j['eta']) < etaCut and j['id'], 
        cmgObjectSelection.get_cmg_jets_fromStruct(readTree, jetVariables))
    
    return jets



def processJets(args, readTree, splitTree, saveTree, params):
    '''Process jets. 
    
    TODO describe here the processing.
    '''

    #
    logger = logging.getLogger('cmgPostProcessing.processJets')
    
    verbose = args.verbose
    
    # initialize returned variables (other than saveTree)
    jets = None

    # selection of jets
    
    objBranches = 'Jet'
    jetObj = cmgObjectSelection.cmgObject(readTree, splitTree, objBranches)
    
    JetVarList = params['JetVarList'] 
    JetSel = params['JetSel']
    
    if logger.isEnabledFor(logging.DEBUG):
        printStr = "\n List of " + objBranches + " jets before selector: " + \
            jetObj.printObjects(None, JetVarList)
        logger.debug(printStr)
    
    # TODO modify the getSelectionIndexList to take as input a list of indices, instead of 
    # a PassFailList, then get rid of the two steps in basic jet selection 

    # basics jets
        
    basJetSel = JetSel['bas']
    basJetSelector = cmgObjectSelection.objSelectorFunc(basJetSel)
    basJetPassFailList = jetObj.getPassFailList(readTree, basJetSelector)
    basJetList = jetObj.getSelectionIndexList(readTree, basJetSelector, basJetPassFailList)

    if logger.isEnabledFor(logging.DEBUG):
        printStr = "\n  " + objBranches + " basic jet selector \n " + \
            pprint.pformat(basJetSel) + \
            '\n ' + jetObj.printObjects(basJetList, JetVarList)
        logger.debug(printStr)

    jets = selectionJets(readTree, basJetSel['pt'][2])
    logger.debug(
        "\n Selected jets with pT threshold %i GeV: %i jets \n %s \n", basJetSel['pt'][2], len(jets), pprint.pformat(jets)
        )
    
    # veto jets
    
    vetoJetSel = JetSel['veto']
    vetoJetSelector = cmgObjectSelection.objSelectorFunc(vetoJetSel)
    vetoJetList = jetObj.getSelectionIndexList(readTree, vetoJetSelector, basJetPassFailList)

    if logger.isEnabledFor(logging.DEBUG):
        printStr = "\n  " + objBranches + " veto jet selector (from basic jets) \n " + \
            pprint.pformat(vetoJetSel) + \
            '\n ' + jetObj.printObjects(vetoJetList, JetVarList)
        logger.debug(printStr)

    jets60 = selectionJets(readTree, vetoJetSel['pt'][2])
    logger.debug(
        "\n Selected jets with pT threshold %i GeV: %i jets \n %s \n", 
        vetoJetSel['pt'][2], len(jets60), pprint.pformat(jets60)
        )
    
    # ISR jets

    isrJetSel = JetSel['isr']
    isrJetSelector = cmgObjectSelection.objSelectorFunc(isrJetSel)
    isrJetList = jetObj.getSelectionIndexList(readTree, isrJetSelector, basJetPassFailList)

    if logger.isEnabledFor(logging.DEBUG):
        printStr = "\n  " + objBranches + " isr jet selector (from basic jets) \n " + \
            pprint.pformat(isrJetSel) + \
            '\n ' + jetObj.printObjects(isrJetList, JetVarList)
        logger.debug(printStr)

    jets110 = selectionJets(readTree, isrJetSel['pt'][2])
    logger.debug(
        "\n Selected jets with pT threshold %i GeV: %i jets \n %s \n", 
        isrJetSel['pt'][2], len(jets110), pprint.pformat(jets110)
        )

    # ISR jet, higher threshold for SR2
    
    isrHJetSel = JetSel['isrH']
    isrHJetSelector = cmgObjectSelection.objSelectorFunc(isrHJetSel)
    isrHJetList = jetObj.getSelectionIndexList(readTree, isrHJetSelector, basJetPassFailList)
    
    if logger.isEnabledFor(logging.DEBUG):
        printStr = "\n  " + objBranches + " isr high jet selector (from basic jets) \n " + \
            pprint.pformat(isrHJetSel) + \
            '\n ' + jetObj.printObjects(isrHJetList, JetVarList)
        logger.debug(printStr)
        
    
    assert len(jets) == len(basJetList)
    assert len(jets60) == len(vetoJetList)
    assert len(jets110) == len(isrJetList)

    saveTree.nJet30 = len(basJetList)
    saveTree.nJet60 = len(vetoJetList)
    saveTree.nJet100 = -999
    saveTree.nJet110 = len(isrJetList)
    saveTree.nJet325 = len(isrHJetList)

    # save indices for the first three basic jets and some additional jet quantities
    
    if saveTree.nJet30 > 0:  
        basJet_1Index = basJetList[0]  
        saveTree.jet1Index = basJet_1Index
        
        saveTree.jet1Pt = jetObj.pt[basJet_1Index]
        saveTree.jet1Eta = jetObj.eta[basJet_1Index]
        saveTree.jet1Phi = jetObj.phi[basJet_1Index]
    else:
        saveTree.jet1Index = -1

        saveTree.jet1Pt = -999.
        saveTree.jet1Eta = -999.
        saveTree.jet1Phi = -999.
        

    if saveTree.nJet30 > 1:
        basJet_2Index = basJetList[1]  
        saveTree.jet2Index = basJet_2Index
        
        saveTree.jet2Pt = jetObj.pt[basJet_2Index]
        saveTree.jet2Eta = jetObj.eta[basJet_2Index]
        saveTree.jet2Phi = jetObj.phi[basJet_2Index]
        
        dR_basJet_j1j2 = helpers.dR(basJetList[0], basJetList[1], jetObj)
        saveTree.dRJet1Jet2 = dR_basJet_j1j2
        
        dRJet1Jet2_jets = hephyHelpers.deltaR(jets[0], jets[1]) 
        if verbose:
            print 'dR_basJet_j1j2 = ', dR_basJet_j1j2, ' dRJet1Jet2_jets = ', dRJet1Jet2_jets
        
        dPhi_basJet_j1j2 = helpers.dPhi(basJetList[0], basJetList[1], jetObj)
        saveTree.deltaPhi30_j12 = dPhi_basJet_j1j2
        
        deltaPhi30_j12_jets = hephyHelpers.deltaPhi(jetObj.phi[basJetList[0]], jetObj.phi[basJetList[1]])
        if verbose:
            print 'dPhi_basJet_j1j2 = ', dPhi_basJet_j1j2, ' deltaPhi30_j12_jets = ', deltaPhi30_j12_jets
        
    else:
        saveTree.jet2Index = -1

        saveTree.jet2Pt = -999.
        saveTree.jet2Eta = -999.
        saveTree.jet2Phi = -999.
    
        saveTree.dRJet1Jet2 = -999.
        saveTree.deltaPhi30_j12 = -999.
                
        
    if saveTree.nJet30 > 2:
        basJet_3Index = basJetList[2]  
        saveTree.jet3Index = basJet_3Index
    else:
        saveTree.jet3Index = -1
        

    if saveTree.nJet60 > 1:
        dPhi_vetoJet_j1j2 = helpers.dPhi(vetoJetList[0], vetoJetList[1], jetObj)
        saveTree.deltaPhi60_j12 = dPhi_vetoJet_j1j2
        
        deltaPhi60_j12 = hephyHelpers.deltaPhi(jetObj.phi[vetoJetList[0]], jetObj.phi[vetoJetList[1]])
        if verbose:
            print 'dPhi_vetoJet_j1j2 = ', dPhi_vetoJet_j1j2, ' deltaPhi60_j12 = ', deltaPhi60_j12
            
        # for backward compatibility
        saveTree.deltaPhi_j12 = saveTree.deltaPhi60_j12 
    else:
        saveTree.deltaPhi60_j12 = -999.
        saveTree.deltaPhi_j12 = -999. 
        

    logger.debug(
        "\n Number of jets: \n  basic jets: %i \n  veto jets: %i " + \
        "\n  isr jet: %i \n  isr high Jet: %i \n" +\
        "\n Basic jet, index of first jet: %i \n" + \
        "\n   jet1Pt = %f \n  jet1Eta = %f \n  jet1Phi = %f \n\n" + \
        "\n Basic jet, index of second jet: %i \n" + \
        "\n   jet2Pt = %f \n  jet2Eta = %f \n  jet2Phi = %f \n\n" + \
        "\n Basic jet, index of third jet: %i \n" + \
        "\n Jet separation: " + \
        "\n   dRJet1Jet2 = %f \n   deltaPhi_j12 = %f \n" + \
        "\n   deltaPhi30_j12 = %f \n   deltaPhi60_j12 = %f \n" ,
        saveTree.nJet30, saveTree.nJet60, saveTree.nJet110, saveTree.nJet325,
        saveTree.jet1Index,
        saveTree.jet1Pt, saveTree.jet1Eta, saveTree.jet1Phi,
        saveTree.jet2Index,
        saveTree.jet2Pt, saveTree.jet2Eta, saveTree.jet2Phi,
        saveTree.jet3Index,
        saveTree.dRJet1Jet2, saveTree.deltaPhi_j12,
        saveTree.deltaPhi30_j12, saveTree.deltaPhi60_j12
        )
     
    # b jet selection
    
    bJetSel = JetSel['bjet']
    bJetSelector = cmgObjectSelection.objSelectorFunc(bJetSel)
    bJetList = jetObj.getSelectionIndexList(readTree, bJetSelector, basJetPassFailList)
    
    bJetSep = JetSel['bjetSep']['ptSoftHard']
    bSoftJetList, bHardJetList = jetObj.splitIndexList('pt', bJetSep[2], bJetList)
    
    nBJets = len(bJetList)
    nBSoftJets = len(bSoftJetList)
    nBHardJets = len(bHardJetList)
    
    saveTree.nBJetMediumCSV30 = nBJets
    saveTree.nSoftBJetsCSV = nBSoftJets
    saveTree.nHardBJetsCSV = nBHardJets
    
    if logger.isEnabledFor(logging.DEBUG):
        printStr = "\n  " + objBranches + " b jet selector (from basic jets) \n " + \
            pprint.pformat(bJetSel) + \
            '\n ' + jetObj.printObjects(bJetList, JetVarList)
        logger.debug(printStr)
    
    logger.debug(
        "\n Number of b jets, pt separation at %f GeV: \n  soft: %i \n  hard: %i \n  total: %i \n",
        bJetSep[2], saveTree.nSoftBJetsCSV, saveTree.nHardBJetsCSV, saveTree.nBJetMediumCSV30
        )
    

    ### old-style b-jet selection TODO remove it
    lightJetsCSV, bJetsCSV = cmgObjectSelection.splitListOfObjects('btagCSV', bJetSel['btag'][2], jets)
    
    # logger.debug("\n Selected CMVA b jets: %i jets \n %s \n", len(bJetsCMVA), pprint.pformat(bJetsCMVA))
    logger.debug("\n Selected CSV b jets: %i jets \n %s \n", len(bJetsCSV), pprint.pformat(bJetsCSV))

    bJets = filter(lambda j: j["btagCSV"] > bJetSel['btag'][2], jets)
    
    softBJetsCSV, hardBJetsCSV = cmgObjectSelection.splitListOfObjects('pt', bJetSep[2], bJets)
    
    logger.debug(
        "\n Number of b jets - old style, pt separation at %f GeV: \n  soft: %i \n  hard: %i \n  total: %i \n",
        bJetSep[2], len(softBJetsCSV), len(hardBJetsCSV), len(bJetsCSV)
        )

    assert nBJets == len(bJetsCSV)
    assert nBSoftJets == len(softBJetsCSV)
    assert nBHardJets == len(hardBJetsCSV)
    

    # HT as sum of jets pT > 30 GeV
    
    ht_basJet = sum (jetObj.pt[ind] for ind in basJetList)
    saveTree.htJet30j = ht_basJet
    
    htJet30j = sum([x['pt'] for x in jets])
    if verbose:
        print 'ht_basJet = ', ht_basJet, ' htJet30j = ', htJet30j
    
    return saveTree, jetObj, basJetList

def processLeptonJets(readTree, splitTree, saveTree, lepObj, muList, jetObj, basJetList):
    '''Process correlations between the leading selected lepton and jets. 
    
    Compute:
        dR separation of selected lepton and first jet
        invariant mass of the selected leading lepton and the dR-closest jet
        invariant mass of 1, 2, 3 jets, other than the closest jet associated to lepton 
        
        Jets are considered having mass here, lepton have mass zero.

    '''
    
    logger = logging.getLogger('cmgPostProcessing.processLeptonJets')

         
    if (lepObj is not None) and (len(muList) > 0) and (saveTree.nJet30 > 0):
        
        dR_basJet_j1_mu1 = helpers.dR(basJetList[0], muList[0], jetObj, lepObj)
        saveTree.dRJet1Lep = dR_basJet_j1_mu1
        
        # find the dR-closest jet to selected muon
        # closestJet_basJetListIndex gives the position in basJetList of the jet index closestJetIndex 
        # giving the minimum dR
        closestJet_basJetListIndex = min(
            range(len(basJetList)), key=lambda j:helpers.dR(basJetList[j], muList[0], jetObj, lepObj)
            )
        closestJetIndex = basJetList[closestJet_basJetListIndex]
        logger.debug(
            "\n Leading lepton index: %i \n Closest basic jet index: %i \n dR(mu1, jet): %f \n",
            muList[0], closestJetIndex,
            helpers.dR(closestJetIndex, muList[0], jetObj, lepObj)
            )
        
        # list of variables needed to comput invariant mass        
        varList = ['pt', 'eta', 'phi', 'mass', ]

        # invariant mass of the selected leading lepton and the dR-closest jet  
        jlList = jetObj.getObjDictList(varList, [closestJetIndex]) + lepObj.getObjDictList(varList, [muList[0]])
        mass_basJet_mu1_mindR = helpers.invMass(jlList)
        saveTree.JetLepMass = mass_basJet_mu1_mindR
        
        # invariant mass of 1, 2, 3 jets, other than the closest jet associated to lepton 
    
        indexList = [i for i in basJetList if i != closestJetIndex]  
        logger.debug(
            "\n Number of jets, excluding the closest jet: %i jets \n List of jet indices: \n %s \n ", 
            len(indexList), pprint.pformat(indexList)
            )
               
        if saveTree.nJet30 == 1: 
            saveTree.J3Mass = 0.
        elif saveTree.nJet30 == 2:
            jetList = jetObj.getObjDictList(varList, [indexList[0]])
            saveTree.J3Mass = helpers.invMass(jetList)
        elif saveTree.nJet30 == 3:
            jetList = jetObj.getObjDictList(varList, ([indexList[i] for i in range(2)]))
            saveTree.J3Mass = helpers.invMass(jetList)
        else:
            jetList = jetObj.getObjDictList(varList, ([indexList[i] for i in range(3)]))
            saveTree.J3Mass = helpers.invMass(jetList)
   

        logger.debug(
            "\n dRJet1Lep: %f \n JetLepMass: %f \n J3Mass: %f \n", 
            saveTree.dRJet1Lep, saveTree.JetLepMass, saveTree.J3Mass
            )
            
    #
    return saveTree



def hemiSectorCosine(x):
    return round( math.cos(math.pi- 0.5*(x* math.pi/180)),3)


def processTracksFunction(readTree, splitTree, saveTree, lep, jets, params):
    '''Process tracks. 
    
    TODO describe here the processing.
    '''
    logger = logging.getLogger('cmgPostProcessing.processTracksFunction')

    trackMinPtList = params['trackMinPtList']
    hemiSectorList = params['hemiSectorList']
    nISRsList      = params['nISRsList']



    jets =  cmgObjectSelection.get_cmg_jets_fromStruct(readTree, ['eta', 'pt', 'phi', 'btagCMVA', 'btagCSV', 'id', 'mass'])  
    ### corresponding to 90, 135, 150 degree diff between jet and track
    hemiSectorCosines = {  x:hemiSectorCosine(x) for x in hemiSectorList }   
    jetPtThreshold = 30
    varList = [
        'pt', 'eta', 'phi', "dxy", "dz", 'pdgId',
        "matchedJetIndex", "matchedJetDr",
        "CosPhiJet1", "CosPhiJet12", "CosPhiJetAll"
        ]
    trkVar="Tracks"
    nTracks = getattr(readTree,"n%s"%trkVar)
    tracks = (hephyHelpers.getObjDict(splitTree, trkVar+"_", varList, i) for i in range(nTracks))
    nTrkDict = {
                 "nTracks": { minPt : 0 for minPt in trackMinPtList}
               }

    nTrkDict.update({
                "nTracksOpp%sJet%s"%(hemiSec,nISRs) : { minPt : 0 for minPt in trackMinPtList} 
                                         for nISRs in nISRsList for hemiSec in hemiSectorList          
                })
    for track in tracks:
        if not (
                abs(track['eta']) < 2.5 and track['pt']>=1.0 and
                abs(track['dxy']) < 0.1 and abs( track['dz'] ) < 0.1 
                ) :
            continue
        if abs(track['pdgId']) in [13,11]:
            #if len(selectedLeptons)>0 and hephyHelpers.deltaR(track, selectedLeptons[0] ) <0.1:
            if lep and hephyHelpers.deltaR(track, lep) < 0.1 and lep['pdgId']==track['pdgId'] :
                #Possible lepton track... shouldn't count the lepton that's being used, let's check Pt first ", deltaR(track, lep)
                if lep['pt']/track['pt'] < 1.1 and lep['pt']/track['pt'] > 0.9:
                    #print "   yes most definitely is!"
                    continue
        if  (track['matchedJetDr']<=0.4  ): 
            # Possible ISR track, will not count track if the jet pt greater than jetPtThreshold
            #matchedJet = allJets[int(track['matchedJetIndex'])]
            matchedJet = jets[int(track['matchedJetIndex'])]
            if matchedJet['pt'] > jetPtThreshold:
                # Track is matched with dr<0.4 to a jet with pt higher than jetpthtreshold. Dont want to count such a track!
                continue
        for minTrkPt in trackMinPtList:
            if track['pt'] > minTrkPt:
                nTrkDict['nTracks'][minTrkPt] +=1
                ## tracks in the opp sectors
                for hemiSector in hemiSectorList:
                    for nISRs in nISRsList:
                        nTrkVarName = "nTracksOpp%sJet%s"%(hemiSector,nISRs)
                        #print "trk cosine", track['CosPhiJet%s'%nISRs ], hemiSectorCosines[hemiSector]
                        if track['CosPhiJet%s'%nISRs ] < hemiSectorCosines[hemiSector]:
                            #print "  yes" 
                            nTrkDict[nTrkVarName][minTrkPt]+=1
    for minTrkPt in trackMinPtList:
        ptString = str(minTrkPt).replace(".","p")
        setattr(saveTree, "n"+trkVar+"_pt%s"%ptString, nTrkDict["n"+trkVar][minTrkPt] )
        for hemiSector in hemiSectorList:
            for nISRs in nISRsList:
                nTrkVarName = "nTracksOpp%sJet%s"%(hemiSector,nISRs)
                setattr(saveTree,nTrkVarName+"_pt%s"%ptString, nTrkDict[nTrkVarName][minTrkPt] )
    for hemiSector in hemiSectorList:
        for nISRs in nISRsList:
            nTrkVarName = "nTracksOpp%sJet%s"%(hemiSector,nISRs)
            #print nTrkVarName, { trkPt: getattr(saveTree,nTrkVarName+"_pt%s"%str(trkPt).replace(".","p") ) for trkPt in trackMinPtList }
    return saveTree 
 

  
def processGenTracksFunction(readTree, splitTree, saveTree):
    '''Process generated particles. 
    
    TODO describe here the processing.
    '''
    
    logger = logging.getLogger('cmgPostProcessing.processGenTracksFunction')
    
    # 
    genPartMinPtList = [1,1.5,2]

    varList = ['pt', 'eta', 'phi', 'pdgId' ]
    genPartPkds = (hephyHelpers.getObjDict(splitTree, 'genPartPkd_', varList, i) for i in range(readTree.ngenPartPkd))
    
    ngenPartPkds = { minPt : 0 for minPt in genPartMinPtList}
    ngenPartPkdsOppJet1 = { minPt : 0 for minPt in genPartMinPtList}
    ngenPartPkdsOpp90ISR = { minPt : 0 for minPt in genPartMinPtList}
    ngenPartPkdsOppJet12 = { minPt : 0 for minPt in genPartMinPtList}
    ngenPartPkdsOpp90ISR2 = { minPt : 0 for minPt in genPartMinPtList}
    
    for genPartPkd in genPartPkds:
        if not (abs(genPartPkd['eta']) < 2.5 and genPartPkd['pt'] >= 1.0) :
            continue
        
        logger.trace("\n Selected generated particle: \n %s \n", pprint.pformat(genPartPkd))

        if math.cos(genPartPkd['phi'] - saveTree.jet1Phi) < 0:
            for genPartPkdMinPt in genPartMinPtList:
                if genPartPkd['pt'] > genPartPkdMinPt:
                    ngenPartPkdsOppJet1[genPartPkdMinPt] += 1
            if math.cos(genPartPkd['phi'] - saveTree.jet1Phi) < - math.sqrt(2) / 2:
                for genPartPkdMinPt in genPartMinPtList:
                    if genPartPkd['pt'] > genPartPkdMinPt:
                        ngenPartPkdsOpp90ISR[genPartPkdMinPt] += 1

        for genPartPkdMinPt in genPartMinPtList:
            if genPartPkd['pt'] > genPartPkdMinPt:
                ngenPartPkds[genPartPkdMinPt] += 1
                logger.trace("\n added one genPartPkd to genPartPkdMinPt = %f with ngenPartPkds[genPartPkdMinPt] %i \n ", 
                    genPartPkdMinPt, ngenPartPkds[genPartPkdMinPt])
     
    saveTree.ngenPartPkd_1 = ngenPartPkds[1]    
    saveTree.ngenPartPkd_1p5 = ngenPartPkds[1.5]    
    saveTree.ngenPartPkd_2 = ngenPartPkds[2]    
     

    saveTree.ngenPartPkdOppJet1_1 = ngenPartPkdsOppJet1[1]  
    saveTree.ngenPartPkdOppJet1_1p5 = ngenPartPkdsOppJet1[1.5]  
    saveTree.ngenPartPkdOppJet1_2 = ngenPartPkdsOppJet1[2]  

    saveTree.ngenPartPkdO90isr_1 = ngenPartPkdsOpp90ISR[1]  
    saveTree.ngenPartPkdO90isr_1p5 = ngenPartPkdsOpp90ISR[1.5]  
    saveTree.ngenPartPkdO90isr_2 = ngenPartPkdsOpp90ISR[2]  

    #
    return saveTree

def processMasses(readTree, saveTree):
    '''Process various tranverse masses and other variables 
    
    TODO describe here the processing.
    '''

    logger = logging.getLogger('cmgPostProcessing.processMasses')
        
    if (saveTree.nlep >= 1):
        saveTree.Q80 = 1 - 80 ** 2 / (2 * saveTree.lepPt * readTree.met_pt)
        saveTree.CosLMet = math.cos(saveTree.lepPhi - readTree.met_phi)
    
        saveTree.mt = math.sqrt(2 * saveTree.lepPt * readTree.met_pt * (1 - saveTree.CosLMet))
        saveTree.st = readTree.met_pt + saveTree.lepPt
  
        saveTree.deltaPhi_Wl = math.acos(
            (saveTree.lepPt + readTree.met_pt * math.cos(saveTree.lepPhi - readTree.met_phi)) / 
            (math.sqrt(saveTree.lepPt ** 2 + readTree.met_pt ** 2 + 
                      2 * readTree.met_pt * saveTree.lepPt * math.cos(saveTree.lepPhi - readTree.met_phi))
                )
            ) 
    
    logger.debug(
        "\n Q80: %f \n CosLMet: %f \n mt: %f \n \n st: %f \n deltaPhi_Wl %f \n", 
        saveTree.Q80, saveTree.CosLMet, saveTree.mt, saveTree.st, saveTree.deltaPhi_Wl
        )

    #
    return saveTree

def processEventVetoList(readTree, splitTree, saveTree, sample, veto_event_list):
    ''' 
        
    '''
    
    logger = logging.getLogger('cmgPostProcessing.processEventVetoList')

    if not sample['cmgComp'].isData:
        return

    run = int(splitTree.GetLeaf('run').GetValue())
    lumi = int(splitTree.GetLeaf('lumi').GetValue())
    evt = int(splitTree.GetLeaf('evt').GetValue())

    run_lumi_evt = "%s:%s:%s\n" % (run, lumi, evt) 
    
    if run_lumi_evt in veto_event_list:
        saveTree.Flag_Veto_Event_List = 0
        logger.debug(
            "\n Run:LS:Event %s failed veto list",
            run_lumi_evt
            )
    else:
        logger.debug(
            "\n Run:LS:Event %s passed veto list",
            run_lumi_evt
            )
        

def computeWeight(sample, sumWeight,  splitTree, saveTree, params, xsec=None):
    ''' Compute the weight of each event.
    
    Include all the weights used:
        genWeight - weight of generated events (MC only, set to 1 for data)
        luminosity weight 
    '''

    target_lumi = params['target_lumi']
    logger = logging.getLogger('cmgPostProcessing.computeWeight')
        
    # sample type (data or MC, taken from CMG component)
    isDataSample = sample['cmgComp'].isData
    
    # weight according to required luminosity 
    
    genWeight = 1 if isDataSample else splitTree.GetLeaf('genWeight').GetValue()


    if isDataSample: 
        lumiScaleFactor = 1
    else:
        if not xsec:
            xSection = sample['cmgComp'].xSection
        else:
            xSection = xsec
        lumiScaleFactor = xSection * target_lumi / float(sumWeight)
        
    saveTree.weight = lumiScaleFactor * genWeight
    
    logger.debug(
        "\n Computing weight for: %s sample " + \
        "\n    target luminosity: %f "
        "\n    genWeight: %f " + \
        "\n    %s" + \
        "\n    sum of event weights: %f" + \
        "\n    luminosity scale factor: %f " + \
        "\n    Event weight: %f \n",
        ('Data ' + sample['cmgComp'].name if isDataSample else 'MC ' + sample['cmgComp'].name),
        target_lumi, genWeight,
        ('' if isDataSample else 'cross section: ' + str(sample['cmgComp'].xSection) + ' pb^{-1}'),
        sumWeight, lumiScaleFactor, saveTree.weight)
    
        
    #
    return saveTree


def haddFiles(sample_name, filesForHadd, temporaryDir, outputWriteDirectory):
    ''' Add the histograms using ROOT hadd script
        
        If
            input files to be hadd-ed sum to more than maxFileSize MB or
            the number of files to be added is greater than  maxNumberFiles
        then split the hadd
    '''

    logger = logging.getLogger('cmgPostProcessing.haddFiles')
        
    maxFileSize = 500 # split into maxFileSize MB
    maxNumberFiles = 200
    logger.debug(
        "\n " + \
        "\n Sum up the split files in files smaller as %f MB \n",
         maxFileSize
         )

    size = 0
    counter = 0
    files = []
    for f in filesForHadd:
        size += os.path.getsize(temporaryDir + '/' + f)
        files.append(f)
        if size > (maxFileSize * (10 ** 6)) or f == filesForHadd[-1] or len(files) > maxNumberFiles:
            #ofile = outputWriteDirectory + '/' + sample['name'] + '_' + str(counter) + '.root'
            ofile = outputWriteDirectory + '/' + sample_name+ '_' + str(counter) + '.root'
            logger.debug(
                "\n Running hadd on directory \n %s \n files: \n %s \n", 
                temporaryDir, pprint.pformat(files)
                )
            os.system('cd ' + temporaryDir + ';hadd -f -v 0 ' + ofile + ' ' + ' '.join(files))
            logger.debug("\n Written output file \n %s \n", ofile)
            size = 0
            counter += 1 
            files = []
    
    # remove the temporary directory  
    os.system('cd ' + outputWriteDirectory)
    ROOT.gDirectory.cd("..")
    shutil.rmtree(temporaryDir, onerror=retryRemove)
    if not os.path.exists(temporaryDir): 
        logger.debug("\n Temporary directory \n    %s \n deleted. \n", temporaryDir)
    else:
        logger.info(
            "\n Temporary directory \n    %s \n not deleted. \n" + \
            "\n Delete it by hand. \n", 
            temporaryDir
            )
        
    return



def cmgPostProcessing(argv=None):
    
    if argv is None:
        argv = sys.argv[1:]
    
    # parse command line arguments
    args = get_parser().parse_args()
    

    # job control parameters
    
    verbose = args.verbose
    overwriteOutputFiles = args.overwriteOutputFiles
    
    skim = args.skim
    skimLepton = args.skimLepton
    preselect = args.preselect
    
    runSmallSample = args.runSmallSample

    # for ipython, run always on small samples   
    if sys.argv[0].count('ipython'):
        runSmallSample = True
    
    testMethods = args.testMethods
    # for testMethods, run always on small samples 
    if testMethods:
        runSmallSample = True
        
    
    # load FWLite libraries
    
    ROOT.gSystem.Load("libFWCoreFWLite.so")
    ROOT.AutoLibraryLoader.enable()
    
    # choose the sample(s) to process (allSamples), with results saved in outputDirectory
    
    cmgTuples = args.cmgTuples
    allSamples, outputDirectory, mass_dict = getSamples(args)
     
    # logging configuration

    logLevel = args.logLevel
    
    # use a unique name for the log file, write file in the dataset directory
    prefixLogFile = 'cmgPostProcessing_' + '_'.join([sample['cmgComp'].name for sample in allSamples]) + \
         '_' + logLevel + '_'
    logFile = tempfile.NamedTemporaryFile(suffix='.log', prefix=prefixLogFile, dir=outputDirectory, delete=False) 

    logger = get_logger(logLevel, logFile.name)
    
    #
    logger.info("\n Job arguments: \n\n %s \n", pprint.pformat(vars(args)))

    #
    logger.info(
        "\n Running on CMG ntuples %s \n" + \
        "\n Samples to be processed: %i \n\n %s \n\n Detailed sample description: \n\n  %s \n" + \
        "\n Results will be written to directory \n %s \n",
        cmgTuples, len(allSamples), 
        pprint.pformat([sample['cmgComp'].name for sample in allSamples]),
        pprint.pformat(allSamples),
        outputDirectory
        )

    # define job parameters and log the parameters used in this job
    params = getParameterSet(args)

    logger.info("\n Parameters: \n\n %s \n", pprint.pformat(params, width=1))
    logger.info("\n Target luminosity: %f pb^{-1} \n", params['target_lumi'])
    
    # get the event veto list FIXME: are the values updated properly?   
    event_veto_list = get_veto_list()['all']

    #   prepare for signal scan
    
    if args.processSignalScan:
        #mass_dict = pickle.load( open("./mass_dicts/%s_mass_nEvents_xsec.pkl"%sample,"r"))
        #from mass_dict import mass_dict
        #mass_dict = pickle.load(open("mass_dict_all.pkl","r"))

        if len(mass_dict) ==0:
            print "Mass Dict Not Avail. It's needed to split signal scan mass points"
            assert False, "Mass Dict Not Avail. It's needed to split signal scan mass points"

        mstop = args.processSignalScan[0]
        mlsp = args.processSignalScan[1]
        xsec = mass_dict[int(mstop)][int(mlsp)]['xsec']
        nEntries = mass_dict[int(mstop)][int(mlsp)]['nEntry']

    # skim condition 
    signalMasses = [mstop, mlsp] if args.processSignalScan else []
    skimCond = eventsSkimPreselect(skim, skimLepton, preselect, params, signalMasses)
    logger.info("\n Final skimming condition: \n  %s \n", skimCond)
    
    # loop over each sample, process all variables and fill the saved tree
    
    for isample, sample in enumerate(allSamples):
        
        sampleName = sample['cmgComp'].name
        sampleType = 'Data' if sample['cmgComp'].isData else 'MC'
                              
        logger.info(
            "\n Running on sample %s of type %s \n",
            sampleName, sampleType
            ) 

        # create the output sample directory, if it does not exist. 
        # If it exists and overwriteOutputFiles is set to True, clean up the directory; if overwriteOutputFiles is 
        # set to False, skip the post-processing of this component.
        #
        # create also a temporary directory (within the output directory)
        # that will be deleted automatically at the end of the job. If the directory exists,
        # it will be deleted and re-created.


        sample_name = sample['name']
        if args.processSignalScan:
            sample_name = "SMS_T2_4bd_mStop_%s_mLSP_%s"%(mstop,mlsp)        
        outputWriteDirectory = os.path.join(outputDirectory, sample_name)

        if not os.path.exists(outputWriteDirectory):
            os.makedirs(outputWriteDirectory)
            logger.debug(
                "\n Requested sample directory \n %s \n does not exists." + \
                "\n Created new directory. \n", 
                outputWriteDirectory
                )
        else:
            if overwriteOutputFiles:
                shutil.rmtree(outputWriteDirectory, onerror=retryRemove)
                os.makedirs(outputWriteDirectory)
                logger.info(
                    "\n Requested sample directory \n %s \n exists, and overwriteOutputFiles is set to True." + \
                    "\n Cleaned up and recreated the directory done. \n", 
                    outputWriteDirectory
                    )
            else:
                logger.error(
                    "\n Requested sample directory \n %s \n exists, and overwriteOutputFiles is set to False." + \
                    "\n Skip post-processing sample %s \n", 
                    outputWriteDirectory, sample_name
                    )
                
                continue
        
        # python 2.7 version - must be removed by hand, preferably in a try: ... finalize:
        temporaryDir = tempfile.mkdtemp(dir=outputDirectory) 
        #
        # for 3.X use
        # temporaryDir = tempfile.TemporaryDirectory(suffix=None, prefix=None, dir=None)
             
        logger.info("\n Output sample directory \n  %s \n", outputWriteDirectory) 
        logger.debug("\n Temporary directory \n  %s \n", temporaryDir) 
        
        branchKeepStrings, readVars, aliases, readVectors, newVars, newVectors, readTree, saveTree = \
            rwTreeClasses(sample, isample, args, temporaryDir, params)
                   
        #
        
        chunks, sumWeight = hephyHelpers.getChunks(sample)
                
        logger.info(
            "\n Sample %s of type %s has " + \
            "\n   number of chunks: %i"\
            "\n   sumWeights: %s \n", sampleName, sampleType, len(chunks), sumWeight
            ) 
        logger.debug("\n Chunks: \n \n %s", pprint.pformat(chunks)) 
        
        if runSmallSample: 
            chunks=chunks[:1]
            logger.debug("\n\n Running with runSmallSample option. Run only over chunk \n %s\n", pprint.pformat(chunks)) 
        
        filesForHadd=[]

        nEvents_total = 0
        
        for chunk in chunks:
          
            sourceFileSize = os.path.getsize(chunk['file'])


            maxFileSize = 200 # split into maxFileSize MB
            
            #if args.processSignalScan:
            #    maxFileSize *= 5
            #    print "---------------------"*10
            #    print mstop, mlsp
            #    print "---------------------"*10

            nSplit = 1+int(sourceFileSize/(maxFileSize*10**6)) 
            if nSplit>1: 
                logger.debug("\n Chunk %s too large \n will split it in %i fragments of approx %i MB \n", 
                    chunk['name'], nSplit, maxFileSize)
            
            for iSplit in range(nSplit):
                
                splitTree = getTreeFromChunk(chunk, skimCond, iSplit, nSplit)
                if not splitTree: 
                    logger.warning("\n Tree object %s not found\n", splitTree)
                    continue
                else:
                    logger.debug("\n Running on tree object %s \n from split fragment %i \n", splitTree, iSplit)
                    
                splitTree.SetName("Events")
                nEvents = splitTree.GetEntries()
                if not nEvents:
                    if verbose:
                        print "Chunk empty....continuing"
                    continue
                
                # addresses for all variables (read and write) 
                # must be done here to take the correct address
                
                for v in readVars:
                    splitTree.SetBranchAddress(v['stage1Name'], ROOT.AddressOf(readTree, v['stage1Name']))
                for v in readVectors:
                    for var in v['vars']:
                        splitTree.SetBranchAddress(var['stage1Name'], ROOT.AddressOf(readTree, var['stage1Name']))
                for a in aliases:
                    splitTree.SetAlias(*(a.split(":")))
                
                for v in newVars:
                    v['branch'] = splitTree.Branch(v['stage2Name'], 
                        ROOT.AddressOf(saveTree,v['stage2Name']), v['stage2Name']+'/'+v['stage2Type'])
    
                for v in newVectors:
                    for var in v['vars']:
                        var['branch'] = splitTree.Branch(var['stage2Name'], 
                            ROOT.AddressOf(saveTree,var['stage2Name']), var['stage2Name']+'/'+var['stage2Type'])
                        

                # get entries for tree and loop over events
                
            
                logger.debug(
                    "\n Number of events after skimming and preselection: \n    chunk: %s \n    " + \
                    "split fragment %i of %i fragments in this chunk: \n    %i events \n", 
                    chunk['name'], iSplit, nSplit, nEvents
                    )


                #if args.processSignalScan:
                #    #mstop = args.processSignalScan[0]
                #    #mlsp  = args.processSignalScan[1]
                #    #eListName = "eList_%s_stp%s_lsp%s"%(iSplit, mstop,mlsp)
                #    #splitTree.Draw(">>%s"%eListName, "(GenSusyMStop==%s) && (GenSusyMNeutralino==%s)"%(mstop,mlsp)  )
                #    #eList = getattr(ROOT,eListName)
                #    #splitTree.SetEventList(eList)
                #    #nEvents_mscan = eList.GetN()
                #    ##assert nEvents_mscan, "CANNOT PROCESS SIGNAL SAMPL mStop:%s  mLSP:%s "%(mstop, mlsp)
                #    #print iSplit, mlsp, mstop, nEvents_mscan 
                #    logger.info(
                #        "Processing Signal Scan For iSplit:%s mStop:%s  mLSP:%s "%(iSplit, mstop, mlsp)
                #        )

                #    events = xrange(nEvents_mscan)
                #else:
                #    events = xrange(nEvents)

                
                #print "{:-^80}".format(" Processing Chunk with %s  Events "%(nEvents) )
                start_time = int(time.time())
                last_time = start_time
                nVerboseEvents = 10000
                
                for iEv in xrange(nEvents):
                    
                    nEvents_total +=1
                    if (nEvents_total%nVerboseEvents == 0) and nEvents_total>0:
                        passed_time = int(time.time() ) - last_time
                        last_time = time.time()
                        if passed_time:
                            if verbose:
                                print "Event:{:<8}".format(nEvents_total), "@ {} events/sec".format(
                                    round(float(nVerboseEvents)/passed_time )
                                    )                      
                            logger.debug(
                                "\n Processing event %i from %i events from chunck \n %s \n",
                                nEvents_total, iEv, nEvents, chunk['name']
                                )
            
                    saveTree.init()
                    readTree.init()
                    splitTree.GetEntry(iEv)
                    
                    logger.debug(
                        "\n " + \
                        "\n ================================================" + \
                        "\n * Processing Run:LS:Event %i:%i:%i \n",
                        splitTree.run, splitTree.lumi, splitTree.evt 
                        )
                    
                    # leptons processing
                    saveTree, lepObj, muList = processLeptons(readTree, splitTree, saveTree, params)
                    
                    # jets processing
                    saveTree, jetObj, basJetList = processJets(args, readTree, splitTree, saveTree, params)
                    
                    # selected leptons - jets processing
                    saveTree = processLeptonJets(readTree, splitTree, saveTree, lepObj, muList, jetObj, basJetList)
                    if args.processTracks:
                        saveTree = processTracksFunction(readTree, splitTree, saveTree, lep, jets, params)

                    if args.processGenTracks:
                        saveTree = processGenTracksFunction(readTree, splitTree, saveTree)
                    
                    # process various tranverse masses and other variables
                    saveTree = processMasses(readTree, saveTree)
              
                    # process event veto list flags
                    processEventVetoList(readTree, splitTree, saveTree, sample, event_veto_list)

                    processGenSusyParticles(readTree, splitTree, saveTree)


                    # compute the weight of the event
                    if not args.processSignalScan:
                        saveTree = computeWeight(sample, sumWeight, splitTree, saveTree, params)
                    else:
                        saveTree = computeWeight(sample, nEntries, splitTree, saveTree, params, xsec=xsec)
                            
                
                    # fill all the new variables and the new vectors        
                    for v in newVars:
                        v['branch'].Fill()
                        
                    for v in newVectors:
                        for var in v['vars']:
                            var['branch'].Fill()
                            

                # 
                
                # fileTreeSplit = sample['name'] + '_' + chunk['name'] + '_' + str(iSplit) + '.root' 
                fileTreeSplit = sample_name + '_' + chunk['name'] + '_' + str(iSplit) + '.root' 
                filesForHadd.append(fileTreeSplit)

                if not testMethods:
                    tfileTreeSplit = ROOT.TFile(temporaryDir + '/' + fileTreeSplit, 'recreate')

                    splitTree.SetBranchStatus("*", 0)
                    for b in (branchKeepStrings + 
                              [v['stage2Name'] for v in newVars] + 
                              [v.split(':')[1] for v in aliases]):
                        splitTree.SetBranchStatus(b, 1)
                    for v in newVectors:
                        for var in v['vars']:
                            splitTree.SetBranchStatus(var['stage2Name'], 1)
                        
                    t2 = splitTree.CloneTree()
                    t2.Write()
                    tfileTreeSplit.Close()
                    logger.debug("\n ROOT file \n %s \n written \n ", temporaryDir + '/' + fileTreeSplit)
                    del tfileTreeSplit
                    del t2
                    splitTree.Delete()
                    del splitTree
                    
                for v in newVars:
                    del v['branch']
                    
                for v in newVectors:
                    for var in v['vars']:
                        del var['branch']
    
        logger.debug(
            "\n " + \
            "\n End of processing events for sample %s." + \
            "\n Start summing up the chunks.\n",
            sample_name
            )
        
        # add the histograms using ROOT hadd script         
        if not testMethods: 
            haddFiles(sample_name, filesForHadd, temporaryDir, outputWriteDirectory)
                
    logger.info(
        "\n " + \
        "\n End of post-processing sample %s. \n Total number of event processed for this sample: %i" + \
        "\n *******************************************************************************\n",
        sample_name, nEvents_total
        )
    
    if verbose:
        print "Log File Stored in:"
        print logFile.name
        print "Output Directory:"
        print outputWriteDirectory 
 
if __name__ == "__main__":
    sys.exit(cmgPostProcessing())
