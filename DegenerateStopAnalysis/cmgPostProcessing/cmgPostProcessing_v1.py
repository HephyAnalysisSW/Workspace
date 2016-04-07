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
import importlib
import copy
import operator
import collections


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
       
    argParser.add_argument('--processSample',
        action='store',
        nargs='?',
        type=str,
        default='TTJets_LO',
        help="Sample to be post-processed, given as CMG component name"
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
    
    argParser.add_argument('--skimPreselect',
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

    # internal functions
    
    def varFromBranch(objSel):
        ''' Return a list of variables from a list of branches, as given in object selector.
        
        '''
        
        varList = []
        for var in objSel:
            varName = helpers.getVariableName(var)
            varList.append(varName)
            
            # 
        return varList


    #
    # arguments to build the parameter set
    parameterSet = args.parameterSet
    processTracks = args.processTracks

    # parameter set definitions
        
    params = collections.OrderedDict()
    
    
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
    
    # lepton (electron and muon) selection
    
    LepSel = {
        # prefix, branches to be read and new branches to be written for leptons
        # 'common' 'branches' and 'newBranches' are common for electron and muons 
        'branchPrefix': 'LepGood',
        'branches': {
            'mu': [
                'tightId/I', 'mediumMuonId/I',
                ],
            'el': [
                'SPRING15_25ns_v1/I', 'mvaIdPhys14/F', 'mvaIdSpring15/F',
                'hadronicOverEm/F',
                'dEtaScTrkIn/F', 'dPhiScTrkIn/F', 'eInvMinusPInv/F', 'lostHits/I',
                'convVeto/I',
                ],
            'common': [
                'pdgId/I',
                'pt/F', 'eta/F', 'phi/F',
                'relIso03/F', 'relIso04/F', 'miniRelIso/F', 'sip3d/F',
                'dxy/F', 'dz/F',
                'mass/F',
                ],
            },
        'newBranches': {
            'mu': [],
            'el': [],
            'common': [        
                'q80/F', 'cosLMet/F',
                'lt/F', 'dPhi_Wl/F',
                'mt/F',
                'absIso/F',
                ],
            },
        #
        # maximum number of objects kept
        'nMax': 8,
        #
        # muon selection
        'mu': {
            'pdgId': ('pdgId', operator.eq, 13, operator.abs),
            'pt': ('pt', operator.gt, 5),
            'eta': ('eta', operator.lt, 2.4, operator.abs),
            'dxy': ('dxy', operator.lt, 0.05, operator.abs),
            'dz': ('dz', operator.lt, 0.2, operator.abs),
            'sip3d': ('sip3d', operator.lt, 4),
            'mediumMuonId': ('mediumMuonId', operator.eq, 1),
            'hybIso': {
                'ptSwitch': 25, 'relIso': 0.2, 'absIso': 5
                },
            },
        #
        # electron selection
        'el': {
            'pdgId': ('pdgId', operator.eq, 11, operator.abs),
            'pt': ('pt', operator.gt, 5),
            'eta': ('eta', operator.lt, 2.5, operator.abs),
            'convVeto': ('convVeto', operator.eq, 1),
            'elWP': {
                'eta_EB': 1.479, 'eta_EE': 2.5,
                'vars': {
                    'hadronicOverEm': {
                        'EB': 0.181, 'EE': 0.116, 'opCut': operator.lt, 'opVar': None,
                        },
                    'dEtaScTrkIn': {
                        'EB': 0.0152, 'EE': 0.0113, 'opCut': operator.lt, 'opVar': operator.abs,
                        },
                    'dPhiScTrkIn': {
                        'EB': 0.216, 'EE': 0.237, 'opCut': operator.lt, 'opVar': operator.abs,
                        },
                    'eInvMinusPInv': {
                        'EB': 0.207, 'EE':  0.174, 'opCut': operator.lt, 'opVar': operator.abs,
                        },
                    'dxy': {
                        'EB': 0.0564, 'EE': 0.222, 'opCut': operator.lt, 'opVar': operator.abs,
                        },
                    'dz': {
                        'EB': 0.472, 'EE': 0.921, 'opCut': operator.lt, 'opVar': operator.abs,
                        },
                    'lostHits': {
                        'EB': 2, 'EE': 3, 'opCut': operator.le, 'opVar': None,
                        },
                    },
                },
            },
        }



    if parameterSet == 'analysisHephy':
        params['LepSel'] = LepSel
    elif parameterSet == 'syncLip':
        LepSelPt30 = copy.deepcopy(LepSel)
        LepSelPt30['mu']['ptMax'] = ('pt', operator.lt, 30) 
        LepSelPt30['el']['ptMax'] = ('pt', operator.lt, 30)
        
        params['LepSel'] = LepSelPt30
     
        
    # list of variables for muon, electrons, leptons (electrons plus muons)
    
    # existing branches
    varsCommon = varFromBranch(LepSel['branches']['common'])
    varsMu = varFromBranch(LepSel['branches']['mu'])
    varsEl = varFromBranch(LepSel['branches']['el'])
    
    varListMu = varsCommon + varsMu
    varListEl = varsCommon + varsEl
    varListLep = varsCommon + varsMu + varsEl
    
    # new branches
    varsCommon = varFromBranch(LepSel['newBranches']['common'])
    varsMu = varFromBranch(LepSel['newBranches']['mu'])
    varsEl = varFromBranch(LepSel['newBranches']['el'])
    
    varListExtMu = varsCommon + varsMu
    varListExtEl = varsCommon + varsEl
    varListExtLep = varsCommon + varsMu + varsEl

    # add the lists to params
        
    LepVarList = {
        'mu': varListMu,
        'el': varListEl,
        'lep': varListLep,
        'extMu': varListExtMu,
        'extEl': varListExtEl,
        'extLep': varListExtLep,
        }

    params['LepVarList'] = LepVarList
    
    
    # jet selection
    #    bas: basic jets
    #    veto: jets used for QCD veto, selected from basic jets
    #    isr: ISR jets, selected from basic jets
    #    isrH: ISR jet, higher threshold for SR2, selected from basic jets
    #    bjet: b jets, tagged with algorithm btag, separated in soft and hard b jets 
        
    JetSel = {
        'branchPrefix': 'Jet',
        'branches': [
            'pt/F', 'eta/F', 'phi/F', 'id/I','btagCSV/F', 'mass/F'
            ],
        'nMax': 100,
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

    JetVarList = varFromBranch(JetSel['branches'])
    params['JetVarList'] = JetVarList


    # track selection
    # FIXME the analysis of tracks (reconstructed and generated) needs a serious clean up...
    
    if args.processTracks:
        TracksSel = {
            'branchPrefix': 'Tracks',
            'branches': [
                'pt/F', 'eta/F', 'phi/F', 'dxy/F', 'dz/F', 'pdgId/I', 'fromPV/I', 
                'matchedJetIndex/I', 'matchedJetDr/F', 'CosPhiJet1/F', 'CosPhiJet12/F', 'CosPhiJetAll/F',
                'mcMatchId/I', 'mcMatchIndex/I', 'mcMatchPtRatio/F', 'mcMatchDr/F',
                ],
            'nMax': 300,
            'bas': {
                'pt': 1.0,
                'eta': 2.5,
                'dxy': 0.1,
                'dz': 0.1,
                'pdgId': [11, 13],
                },
            'dRLepTrack': 0.1,
            'ratioPtLepTrackMin': 0.9,
            'ratioPtLepTrackMax': 1.1,
            'dRmatchJetTrack': 0.4,
            'ptMatchJet': 30,
            'trackMinPtList':  [1, 1.5, 2, 2.5, 3, 3.5],
            'hemiSectorList': [ 270, 180, 90, 60, 360],  
            'nISRsList': ['1', '12', 'All'],
            }
    else:
        TracksSel = {            
            'nMax': 300,
            'trackMinPtList': [],
            'hemiSectorList': [],
            'nISRsList': [],
            }
    
    params['TracksSel'] = TracksSel

    if args.processGenTracks:
        GenTracksSel = {
            'branchPrefix': 'GenTracks',
            'branches': [
                'pt/F', 'eta/F', 'phi/F', 'dxy/F', 'dz/F', 'pdgId/I', 'fromPV/I', 
                'matchedJetIndex/I', 'matchedJetDr/F', 'CosPhiJet1/F', 'CosPhiJet12/F', 'CosPhiJetAll/F',
                'mcMatchId/I', 'mcMatchIndex/I', 'mcMatchPtRatio/F', 'mcMatchDr/F',
                ],
            'nMax': 300,
            'bas': {
                'pt': 1.0,
                'eta': 2.5,
                },
            'genPartMinPtList': [1,1.5,2]
            }
        
        params['GenTracksSel'] = GenTracksSel

    # generated particles
        
    GenSel = {
        'branchPrefix': 'GenPart',
        'branches': [
            'pt/F', 'eta/F', 'phi/F', 'pdgId/I', 'mass/F', 'motherId/I',
            ],
        'nMax': 30,        
        }

    params['GenSel'] = GenSel
    
    
    # for the object selectors defined here, add the list of branches defined in the selector 

    vectors_DATAMC_List = [LepSel, JetSel]
    if args.processTracks:
        vectors_DATAMC_List.append(TracksSel)
        
    params['vectors_DATAMC_List'] = vectors_DATAMC_List

    vectors_MC_List = [GenSel]
    if args.processGenTracks:
        vectors_DATAMC_List.append(GenTracksSel)

    params['vectors_MC_List'] = vectors_MC_List
    
    
    
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
    processSample = args.processSample
    
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
   

    if args.skimPreselect:
        outDir = os.path.join(
            targetDir, processingEra, processingTag, cmgTuples, args.skim, 'skimPreselect', args.skimLepton
            )
    else:
        outDir = os.path.join(targetDir, processingEra, processingTag, cmgTuples, args.skim, args.skimLepton)
    

    # samples
    
    allComponentsList = [] 
    
    processSampleList = [processSample]
    for sampleName in processSampleList:
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
    
    #
    SkimParameters = params['SkimParameters']
    
    lheHThighIncoming = SkimParameters['lheHThigh']['lheHTIncoming']
    lheHTlowIncoming = SkimParameters['lheHTlow']['lheHTIncoming']
    
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
        skimCond += "&&(lheHTIncoming>={0})".format(lheHThighIncoming)
    elif skimName == 'lheHTlow': 
        skimCond += "&&(lheHTIncoming<{0})".format(lheHTlowIncoming)
    else:
        raise Exception("Skim Condition not recognized: %s"%skimName)
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

    # define some internal functions
    
    def appendVectors(params, key, vectorType, vectorsList):
        ''' Append to vectorsList the vectors defied as dictionary in the getParameterSet
        
        '''
        
        if params.has_key(key):
            
            for sel in params[key]:
                
                # get the list of branches 
                if vectorType == 'read':
                    if sel.has_key('branches'):
                        branches = sel['branches']
                    else:
                         return vectorsList                        
                elif vectorType == 'new':
                    if sel.has_key('newBranches'):
                        branches = sel['newBranches']
                    else:
                         return vectorsList
                else:
                    raise Exception("\n No such vector type defined to append to {0}.".format(vectorType))
                    sys.exit()
                    
                varList = []
                if isinstance(branches, dict):
                    # dictionary with list of branches
                    for key, value in branches.iteritems():
                        varList.extend(value)
                elif isinstance(branches, list):
                    # list of branches
                    varList = branches
                else:
                    raise Exception("\n Not possible to build list of branches for {0}.".format(branches))
                    sys.exit()
            
                vec = {
                    'prefix': sel['branchPrefix'], 'nMax': sel['nMax'],
                        'vars': varList,
                    }
                vectorsList.append(vec)
                
        #
        return vectorsList

    
    # define the branches and the variables to be kept and/or read for data and MC
        
    # common branches for data and MC samples 
    
    # common branches already defined in cmgTuples
    branchKeepStrings_DATAMC = [
        'run', 'lumi', 'evt', 'isData', 'rho', 'nVert', 
        'met*','puppi*',
        'Flag_*','HLT_*',
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
    
    readVectors_DATAMC = appendVectors(params, 'vectors_DATAMC_List', 'read', readVectors_DATAMC)
                        
    newVariables_DATAMC.extend([
        'Flag_Veto_Event_List/I/1',
        ])
        
    newVariables_DATAMC.extend([
        'weight/F/-999.',
        'ht_basJet/F/-999.'
        ])
    
    newVariables_DATAMC.extend([
        'nBasJet/I/-1', 'nVetoJet/I/-1', 'nIsrJet/I/-1', 'nIsrHJet/I/-1',
        'nBJets/I/-1', 'nBSoftJets/I/-1', 'nBHardJets/I/-1',
        ])
    
    newVariables_DATAMC.extend([
        "nMuons/I/-1", "nElectrons/I/-1", "nLeptons/I/-1",
        'singleMuonic/I/-1', 'singleElectronic/I/-1', 'singleLeptonic/I/-1', 
        ])
    
    newVariables_DATAMC.extend([
        'basJet_dR_j1j2/F/-999.', 'basJet_dPhi_j1j2/F/-999.', 'vetoJet_dPhi_j1j2/F/-999.',
        ])
    
    newVariables_DATAMC.extend([
        'basJet_mu_invMass_mu1jmindR/F/-999.','basJet_mu_dR_j1mu1/F/-999.', 'basJet_mu_invMass_3j/F/-999.',
        'basJet_el_invMass_el1jmindR/F/-999.','basJet_el_dR_j1el1/F/-999.', 'basJet_el_invMass_3j/F/-999.',
        'basJet_lep_invMass_lep1jmindR/F/-999.','basJet_lep_dR_j1lep1/F/-999.', 'basJet_lep_invMass_3j/F/-999.',
        'bJet_mu_dR_jHdmu1/F/-999.','bJet_el_dR_jHdel1/F/-999.', 'bJet_lep_dR_jHdlep1/F/-999.',
        ])

    newVectors_DATAMC = []
    
    newVectors_DATAMC = appendVectors(params, 'vectors_DATAMC_List', 'new', newVectors_DATAMC)

    # index sorting
    
    # leptons are sorted after pt
    newVectors_DATAMC.extend([
        {'prefix':'IndexLepton', 'nMax': params['LepSel']['nMax'], 
            'vars':[
                'mu/I/-1',
                'el/I/-1',
                'lep/I/-1',
                ] 
            },
        ])

    # basJet, vetoJet, isrJet, isrHJet are sorted after pt
    # bJet, bSoftJet, bHardJet are sorted also after pt
    newVectors_DATAMC.extend([
        {'prefix':'IndexJet', 'nMax': params['JetSel']['nMax'], 
            'vars':[
                'basJet/I/-1',
                'vetoJet/I/-1',
                'isrJet/I/-1',
                'isrHJet/I/-1',
                'bJet/I/-1',
                'bSoftJet/I/-1',
                'bHardJet/I/-1',
                'bJetDiscSort/I/-1',                
                ] 
            },
        ])
    

    # MC samples only
    
    # common branches already defined in cmgTuples
    branchKeepStrings_MC = [ 
        'nTrueInt', 'genWeight', 'xsec', 'puWeight', 
        'GenSusyMStop', 
        'GenSusyMNeutralino',        
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
    newVectors_MC = []
    
    aliases_MC.extend(['genMet:met_genPt', 'genMetPhi:met_genPhi'])
    
    newVariables_MC.extend([
        "Gen_stop_pt_12/F/-999.", "Gen_stop_eta_12/F/-999.", "Gen_stop_phi_12/F/-999.", 
        "Gen_lsp_pt_12/F/-999.", "Gen_lsp_eta_12/F/-999.", "Gen_lsp_phi_12/F/-999.", 
        ])

    
    readVectors_MC = appendVectors(params, 'vectors_MC_List', 'read', readVectors_MC)
    
    newVectors_MC.extend([
        {'prefix':'IndexGen', 'nMax': params['GenSel']['nMax'], 
            'vars':[
                'stop/I/-1',
                'lsp/I/-1',
                'b/I/-1',
                'lep/I/-1',
                ] 
            },
        ])

    # data samples only
    
    # branches already defined in cmgTuples
    branchKeepStrings_DATA = []
    
    readVariables_DATA = []
    aliases_DATA = []
    newVariables_DATA = []
    
    readVectors_DATA = []
    newVectors_DATA = []
    
    
    # branches for tracks (DATAMC/MC/DATA)
    TracksSel = params['TracksSel']
      
    trackMinPtList = TracksSel['trackMinPtList'] 
    hemiSectorList = TracksSel['hemiSectorList']
    nISRsList      = TracksSel['nISRsList']
       
    if args.processTracks:
        trkVar=TracksSel['branchPrefix']
        trkCountVars = [ "n%s"%trkVar ] 
        trkCountVars.extend([ 
                    "n%sOpp%sJet%s"%(trkVar,hemiSec,nISRs) for hemiSec in hemiSectorList  for nISRs in nISRsList     
                    ])
        newTrackVars = []
        for minTrkPt in trackMinPtList:
            ptString = str(minTrkPt).replace(".","p")
            newTrackVars.extend( [ x+"_pt%s"%ptString+"/I" for x in  trkCountVars  ] )
        newVariables_DATAMC.extend(newTrackVars) 
        
        # readVectors for tracks added already to readVectors_DATAMC via TracksSel
        
                      
    # branches for generated tracks (DATAMC/MC/DATA)

    if args.processGenTracks:
        genTrkVar=params['GenTracksSel']['branchPrefix']
        genTrkCountVars = [ "n%s"%genTrkVar ] 
        genTrkCountVars.extend([ 
                    "n%sOpp%sJet%s"%(genTrkVar,hemiSec,nISRs) for hemiSec in hemiSectorList  for nISRs in nISRsList     
                    ])
        newGenTrackVars = []
        for minGenTrkPt in trackMinPtList:
            ptString = str(minGenTrkPt).replace(".","p")
            newGenTrackVars.extend( [ x+"_pt%s"%ptString+"/I" for x in  genTrkCountVars  ] )
        newVariables_DATAMC.extend(newGenTrackVars)        

        # readVectors for generated tracks added already via GenTracksSel to 
        # readVectors_MC
   

    # sum up branches to be defined for each sample, depending on the sample type (data or MC)
    
    if sample['isData']: 
        branchKeepStrings = branchKeepStrings_DATAMC + branchKeepStrings_DATA
    
        readVariables = readVariables_DATAMC + readVariables_DATA
        aliases = aliases_DATAMC + aliases_DATA
        readVectors = readVectors_DATAMC + readVectors_DATA
        newVariables = newVariables_DATAMC + newVariables_DATA
        newVectors = newVectors_DATAMC + newVectors_DATA
    else:
        branchKeepStrings = branchKeepStrings_DATAMC + branchKeepStrings_MC
    
        readVariables = readVariables_DATAMC + readVariables_MC
        aliases = aliases_DATAMC + aliases_MC
        readVectors = readVectors_DATAMC + readVectors_MC
        newVariables = newVariables_DATAMC + newVariables_MC
        newVectors = newVectors_DATAMC + newVectors_MC


    readVars = [convertHelpers.readVar(v, allowRenaming=False, isWritten=False, isRead=True) for v in readVariables]
    newVars = [convertHelpers.readVar(v, allowRenaming=False, isWritten = True, isRead=False) for v in newVariables]
  
    for v in readVectors:
        readVars.append(convertHelpers.readVar('n'+v['prefix']+'/I', allowRenaming=False, isWritten=False, isRead=True))
        v['vars'] = [convertHelpers.readVar(
            v['prefix']+'_'+vvar, allowRenaming=False, isWritten=False, isRead=True) for vvar in v['vars']
            ]


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



def processGenSusyParticles(readTree, splitTree, saveTree, params):


    genPart = cmgObjectSelection.cmgObject(readTree, splitTree, params['GenSel']['branchPrefix'])

    stopIndices = genPart.getSelectionIndexList(readTree,
                            lambda readTree, gp, igp: abs(gp.pdgId[igp]) == 1000006
                            )
    if len(stopIndices) == 0:  # not a susy event... move on
        return 


    isrIndices = genPart.getSelectionIndexList(readTree,
                            lambda readTree, gp, igp: abs(gp.pdgId[igp]) != 1000006 and gp.motherId == -9999
                            )
    lspIndices = genPart.getSelectionIndexList(readTree,
                            lambda readTree, gp, igp: abs(gp.pdgId[igp]) == 1000022
                            )
    bIndices = genPart.getSelectionIndexList(readTree,
                            lambda readTree, gp, igp: abs(gp.pdgId[igp]) == 5
                            )
    lepIndices = genPart.getSelectionIndexList(readTree,
                            lambda readTree, gp, igp: abs(gp.pdgId[igp]) in [11, 13]
                            )

    for ind, val in enumerate(stopIndices):
        saveTree.IndexGen_stop[ind] = val

    for ind, val in enumerate(lspIndices):
        saveTree.IndexGen_lsp[ind] = val

    for ind, val in enumerate(bIndices):
        saveTree.IndexGen_b[ind] = val

    for ind, val in enumerate(lepIndices):
        saveTree.IndexGen_lep[ind] = val


    stop1_lv = ROOT.TLorentzVector()
    stop2_lv = ROOT.TLorentzVector()

    stop1_lv.SetPtEtaPhiM(
        genPart.pt[stopIndices[0]], genPart.eta[stopIndices[0]], genPart.phi[stopIndices[0]],
        genPart.mass[stopIndices[0]]
        )
    stop2_lv.SetPtEtaPhiM(
        genPart.pt[stopIndices[1]], genPart.eta[stopIndices[1]], genPart.phi[stopIndices[1]],
        genPart.mass[stopIndices[1]]
        )

    stops = stop1_lv + stop2_lv

    saveTree.Gen_stop_pt_12 = stops.Pt()
    saveTree.Gen_stop_eta_12 = stops.Eta()
    saveTree.Gen_stop_phi_12 = stops.Phi()



    lsp1_lv = ROOT.TLorentzVector()
    lsp2_lv = ROOT.TLorentzVector()
    
    lsp1_lv.SetPtEtaPhiM(
        genPart.pt[lspIndices[0]], genPart.eta[lspIndices[0]], genPart.phi[lspIndices[0]],
        genPart.mass[lspIndices[0]]
        )
    lsp2_lv.SetPtEtaPhiM(
        genPart.pt[lspIndices[1]], genPart.eta[lspIndices[1]], genPart.phi[lspIndices[1]],
        genPart.mass[lspIndices[1]]
        )
    lsps = lsp1_lv + lsp2_lv
    
    saveTree.Gen_lsp_pt_12 = lsps.Pt()
    saveTree.Gen_lsp_eta_12 = lsps.Eta()
    saveTree.Gen_lsp_phi_12 = lsps.Phi()


def processLeptons(readTree, splitTree, saveTree, params):
    '''Process leptons. 
    
    TODO describe here the processing.
    '''

    logger = logging.getLogger('cmgPostProcessing.processLeptons')
    
    # initialize returned variables (other than saveTree)
    
    lepObj = None
    
    # lepton selection
    
    LepVarList = params['LepVarList'] 
    LepSel = params['LepSel']
    
    objBranches = LepSel['branchPrefix']
    lepObj = cmgObjectSelection.cmgObject(readTree, splitTree, objBranches)
    
    # compute the additional quantities for leptons
    
    for lepIndex in range(lepObj.nObj):
        
        lep_pt = getattr(lepObj, 'pt')[lepIndex]
        lep_phi = getattr(lepObj, 'phi')[lepIndex]
        lep_relIso04 = getattr(lepObj, 'relIso04')[lepIndex]

        q80 = 1 - 80 ** 2 / (2 * lep_pt * readTree.met_pt)
        cosLMet = math.cos(lep_phi - readTree.met_phi)
    
        mt = math.sqrt(2 * lep_pt * readTree.met_pt * (1 - cosLMet))
        lt = readTree.met_pt + lep_pt
  
        dPhi_Wl = math.acos(
            (lep_pt + readTree.met_pt * math.cos(lep_phi - readTree.met_phi)) / 
            (math.sqrt(lep_pt ** 2 + readTree.met_pt ** 2 + 
                      2 * readTree.met_pt * lep_pt * math.cos(lep_phi - readTree.met_phi))
                )
            ) 
        
        absIso = lep_relIso04 * lep_pt
    
        saveTree.LepGood_q80[lepIndex] = q80
        saveTree.LepGood_cosLMet[lepIndex] = cosLMet
        saveTree.LepGood_mt[lepIndex] = mt
        saveTree.LepGood_lt[lepIndex] = lt
        saveTree.LepGood_dPhi_Wl[lepIndex] = dPhi_Wl
        saveTree.LepGood_absIso[lepIndex] = absIso 
        
              
    if logger.isEnabledFor(logging.DEBUG):
        printStr = "\n List of " + objBranches + " leptons before selector: " + \
            lepObj.printObjects(None, LepVarList['lep'])

        for ind in range(lepObj.nObj):
            printStr += "\n Extended quantities for " + objBranches + " leptons before selector: " + \
            "\n Lepton index {0}: \n".format(ind)
            for var in LepVarList['extLep']:
                varName = objBranches + '_' + var
                varValue = getattr(saveTree, varName)[ind]
                printStr += varName + " = " + str(varValue) + '\n'
            printStr += '\n'
            
        logger.debug(printStr)
        

    muSelector = cmgObjectSelection.objSelectorFunc(LepSel['mu'] )
    elSelector = cmgObjectSelection.objSelectorFunc(LepSel['el'])

    muList = lepObj.getSelectionIndexList(readTree, muSelector)
    elList = lepObj.getSelectionIndexList(readTree, elSelector)
    # 
    sumElMuList = muList + elList
    lepList = lepObj.sort('pt', sumElMuList)
 
    saveTree.nMuons = len(muList)
    for ind, val in enumerate(muList):
        saveTree.IndexLepton_mu[ind] = val
        
    saveTree.nElectrons = len(elList)
    for ind, val in enumerate(elList):
        saveTree.IndexLepton_el[ind] = val

    saveTree.nLeptons = len(lepList)
    for ind, val in enumerate(lepList):
        saveTree.IndexLepton_lep[ind] = val

    saveTree.singleLeptonic = (saveTree.nLeptons == 1)
    saveTree.singleMuonic = (saveTree.nLeptons == 1)
    saveTree.singleElectronic = (saveTree.nLeptons == 1)

    
    if logger.isEnabledFor(logging.DEBUG):

        printStr = "\n  " + objBranches + " muon selector \n " + \
            pprint.pformat(LepSel['mu']) + \
            '\n ' + lepObj.printObjects(muList, LepVarList['mu']) + \
            "\n saveTree.nMuons = %i \n  Index list: " + pprint.pformat(muList) + "\n "
        logger.debug(printStr, saveTree.nMuons)

        printStr = "\n  " + objBranches + " electron selector \n " + \
            pprint.pformat(LepSel['el']) + \
            '\n ' + lepObj.printObjects(elList, LepVarList['el']) + \
            "\n saveTree.nElectrons = %i \n  Index list: " + pprint.pformat(elList) + "\n "
        logger.debug(printStr, saveTree.nElectrons)

        printStr = "\n  " + objBranches + " lepton (mu + el) selection \n " + \
            '\n ' + lepObj.printObjects(lepList, LepVarList['lep']) + \
            "\n saveTree.nLeptons = %i \n  Index list:  " + pprint.pformat(lepList) + "\n "        
        logger.debug(printStr, saveTree.nLeptons)
        
    #
    return saveTree, lepObj, muList, elList, lepList

def processJets(args, readTree, splitTree, saveTree, params):
    '''Process jets. 
    
    TODO describe here the processing.
    '''

    #
    logger = logging.getLogger('cmgPostProcessing.processJets')
    
    verbose = args.verbose
    
    # selection of jets
    
    JetVarList = params['JetVarList'] 
    JetSel = params['JetSel']
    
    objBranches = JetSel['branchPrefix']
    jetObj = cmgObjectSelection.cmgObject(readTree, splitTree, objBranches)
    
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
    
    saveTree.nBasJet = len(basJetList)
    for ind, val in enumerate(basJetList):
        saveTree.IndexJet_basJet[ind] = val


    if logger.isEnabledFor(logging.DEBUG):
        printStr = "\n  " + objBranches + " basic jet selector \n " + \
            pprint.pformat(basJetSel) + \
            '\n ' + jetObj.printObjects(basJetList, JetVarList) + \
            "\n saveTree.nBasJet = %i \n  Index list: " + pprint.pformat(basJetList) + "\n "
        logger.debug(printStr, saveTree.nBasJet)

    # veto jets
    
    vetoJetSel = JetSel['veto']
    vetoJetSelector = cmgObjectSelection.objSelectorFunc(vetoJetSel)
    vetoJetList = jetObj.getSelectionIndexList(readTree, vetoJetSelector, basJetPassFailList)

    saveTree.nVetoJet = len(vetoJetList)
    for ind, val in enumerate(vetoJetList):
        saveTree.IndexJet_vetoJet[ind] = val

    if logger.isEnabledFor(logging.DEBUG):
        printStr = "\n  " + objBranches + " veto jet selector (from basic jets) \n " + \
            pprint.pformat(vetoJetSel) + \
            '\n ' + jetObj.printObjects(vetoJetList, JetVarList) + \
            "\n saveTree.nVetoJet = %i \n  Index list: " + pprint.pformat(vetoJetList) + "\n "
        logger.debug(printStr, saveTree.nVetoJet)

    
    # ISR jets

    isrJetSel = JetSel['isr']
    isrJetSelector = cmgObjectSelection.objSelectorFunc(isrJetSel)
    isrJetList = jetObj.getSelectionIndexList(readTree, isrJetSelector, basJetPassFailList)

    saveTree.nIsrJet = len(isrJetList)
    for ind, val in enumerate(isrJetList):
        saveTree.IndexJet_isrJet[ind] = val

    if logger.isEnabledFor(logging.DEBUG):
        printStr = "\n  " + objBranches + " isr jet selector (from basic jets) \n " + \
            pprint.pformat(isrJetSel) + \
            '\n ' + jetObj.printObjects(isrJetList, JetVarList) + \
            "\n saveTree.nIsrJet = %i \n  Index list: " + pprint.pformat(isrJetList) + "\n "
        logger.debug(printStr, saveTree.nIsrJet)


    # ISR jet, higher threshold for SR2
    
    isrHJetSel = JetSel['isrH']
    isrHJetSelector = cmgObjectSelection.objSelectorFunc(isrHJetSel)
    isrHJetList = jetObj.getSelectionIndexList(readTree, isrHJetSelector, basJetPassFailList)
    
    saveTree.nIsrHJet = len(isrHJetList)
    for ind, val in enumerate(isrHJetList):
        saveTree.IndexJet_isrHJet[ind] = val

    if logger.isEnabledFor(logging.DEBUG):
        printStr = "\n  " + objBranches + " isr high jet selector (from basic jets) \n " + \
            pprint.pformat(isrHJetSel) + \
            '\n ' + jetObj.printObjects(isrHJetList, JetVarList) + \
            "\n saveTree.nIsrHJet = %i \n  Index list: " + pprint.pformat(isrHJetList) + "\n "
        logger.debug(printStr, saveTree.nIsrHJet)
        
    
    # save some additional jet quantities
    
    if len(basJetList) > 1:
        basJet_dR_j1j2 = helpers.dR(basJetList[0], basJetList[1], jetObj)
        saveTree.basJet_dR_j1j2 = basJet_dR_j1j2
        
        basJet_dPhi_j1j2 = helpers.dPhi(basJetList[0], basJetList[1], jetObj)
        saveTree.basJet_dPhi_j1j2 = basJet_dPhi_j1j2
                
    else:
        saveTree.basJet_dR_j1j2 = -999.
        saveTree.basJet_dPhi_j1j2 = -999.
                
        
    if len(vetoJetList) > 1:
        vetoJet_dPhi_j1j2 = helpers.dPhi(vetoJetList[0], vetoJetList[1], jetObj)
        saveTree.vetoJet_dPhi_j1j2 = vetoJet_dPhi_j1j2
                    
    else:
        saveTree.vetoJet_dPhi_j1j2 = -999.
        

    logger.debug(
        "\n Number of jets: \n  basic jets: %i \n  veto jets: %i " + \
        "\n  isr jet: %i \n  isr high Jet: %i \n" +\
        "\n Jet separation: " + \
        "\n   basJet_dR_j1j2 = %f \n   basJet_dPhi_j1j2 = %f \n" + \
        "\n   vetoJet_dPhi_j1j2 = %f \n" ,
        saveTree.nBasJet, saveTree.nVetoJet, 
        saveTree.nIsrJet, saveTree.nIsrHJet,
        saveTree.basJet_dR_j1j2, saveTree.basJet_dPhi_j1j2,
        saveTree.vetoJet_dPhi_j1j2
        )
     
    # b jet selection: bJet, bSoftJet and bHardJet are sorted after pt value, like other jets
    
    bJetSel = JetSel['bjet']
    bJetSelector = cmgObjectSelection.objSelectorFunc(bJetSel)
    bJetList = jetObj.getSelectionIndexList(readTree, bJetSelector, basJetPassFailList)
    
    # sort after discriminant variable
    bTagDisc = bJetSel['btag'][0]
    bJetDiscSortList = jetObj.sort(bTagDisc, bJetList)


    bJetSepPtSoftHard = JetSel['bjetSep']['ptSoftHard'][2]
    bSoftJetList, bHardJetList = jetObj.splitIndexList('pt', bJetSepPtSoftHard, bJetList)
    
    nBJets = len(bJetList)
    saveTree.nBJets = nBJets
    for ind, val in enumerate(bJetList):
        saveTree.IndexJet_bJet[ind] = val

    for ind, val in enumerate(bJetDiscSortList):
        saveTree.IndexJet_bJetDiscSort[ind] = val

    nBSoftJets = len(bSoftJetList)
    saveTree.nBSoftJets = nBSoftJets
    for ind, val in enumerate(bSoftJetList):
        saveTree.IndexJet_bSoftJet[ind] = val

    nBHardJets = len(bHardJetList)
    saveTree.nBHardJets = nBHardJets
    for ind, val in enumerate(bHardJetList):
        saveTree.IndexJet_bHardJet[ind] = val
    
    if logger.isEnabledFor(logging.DEBUG):
        printStr = "\n  " + objBranches + " b jet selector (from basic jets), sorted after jet pt \n " + \
            pprint.pformat(bJetSel) + \
            '\n ' + jetObj.printObjects(bJetList, JetVarList) + \
            "\n saveTree.nBJet = %i \n  Index list: " + pprint.pformat(bJetList) + "\n "
        logger.debug(printStr, saveTree.nBJets)
        
        printStr = "\n  " + objBranches + " b jet selector (from basic jets), sorted after jet b discriminant \n " + \
            "\n saveTree.nBJet = %i \n  Index list: " + pprint.pformat(bJetDiscSortList) + "\n "
        logger.debug(printStr, saveTree.nBJets)

        printStr = "\n  " + objBranches + " b soft jet selector, sorted after jet pt \n " + \
            '\n pt soft/hard threshold: %f ' + \
            '\n ' + jetObj.printObjects(bSoftJetList, JetVarList) + \
            "\n saveTree.nSoftBJets = %i \n  Index list: " + pprint.pformat(bSoftJetList) + "\n "
        logger.debug(printStr, bJetSepPtSoftHard, saveTree.nBSoftJets)

        printStr = "\n  " + objBranches + " b hard jet selector, sorted after jet pt \n " + \
            '\n pt soft/hard threshold: %f ' + \
            '\n ' + jetObj.printObjects(bHardJetList, JetVarList) + \
            "\n saveTree.nHardBJets = %i \n  Index list: " + pprint.pformat(bHardJetList) + "\n "
        logger.debug(printStr, bJetSepPtSoftHard, saveTree.nBHardJets)

    # HT as sum of basic jets
    
    ht_basJet = sum (jetObj.pt[ind] for ind in basJetList)
    saveTree.ht_basJet = ht_basJet
    
    logger.debug(
        "\n Missing transverse energy: \n  met_pt =  %f GeV \n  met_phi = %f \n" + \
        "\n Total hadronic energy: \n  ht_basJet = %f \n\n ", 
            readTree.met_pt, readTree.met_phi, ht_basJet
            )
    
        
    return saveTree, jetObj, basJetList, bJetDiscSortList

def processLeptonJets(
        readTree, splitTree, saveTree, 
        lepObj, muList, elList, lepList, 
        jetObj, basJetList, bJetDiscSortList
        ):
    '''Process correlations between the leading selected lepton and jets. 
    
    Compute:
        dR separation of selected lepton and first jet
        invariant mass of the selected leading lepton and the dR-closest jet
        invariant mass of 1, 2, 3 jets, other than the closest jet associated to lepton 
        
        Jets are considered having mass here, lepton have mass zero.
        
    '''
    
    logger = logging.getLogger('cmgPostProcessing.processLeptonJets')

    def variablesLeptonJets (lepObj, jetObj, objList, basJetList, bJetDiscSortList):
        
        basJet_obj_dR_j1obj1 = helpers.dR(basJetList[0], objList[0], jetObj, lepObj)
        
        # find the dR-closest jet to selected muon / electron / lepton
        # basJet_obj1_indexClosestJet gives the position in basJetList of the jet index closestJetIndex 
        # giving the minimum dR
        basJet_obj1_indexClosestJet = min(
            range(len(basJetList)), key=lambda j:helpers.dR(basJetList[j], objList[0], jetObj, lepObj)
            )
        closestJetIndex = basJetList[basJet_obj1_indexClosestJet]
        logger.debug(
            "\n Leading lepton index: %i \n Closest basic jet index: %i \n dR(obj1, jet): %f \n",
            objList[0], closestJetIndex,
            helpers.dR(closestJetIndex, objList[0], jetObj, lepObj)
            )
        
        # list of variables needed to compute invariant mass        
        varList = ['pt', 'eta', 'phi', 'mass', ]

        # invariant mass of the selected leading lepton and the dR-closest jet  
        jlList = jetObj.getObjDictList(varList, [closestJetIndex]) + lepObj.getObjDictList(varList, [objList[0]])
        basJet_obj_invMass_obj1jmindR = helpers.invMass(jlList)
        
        # invariant mass of 1, 2, 3 jets, other than the closest jet associated to lepton 
    
        indexList = [i for i in basJetList if i != closestJetIndex]  
        logger.debug(
            "\n Number of jets, excluding the closest jet: %i jets \n List of jet indices: \n %s \n ", 
            len(indexList), pprint.pformat(indexList)
            )
         
        basJet_obj_invMass_3j = -999.
              
        if saveTree.nBasJet == 1: 
            basJet_obj_invMass_3j = 0.
        elif saveTree.nBasJet == 2:
            jetList = jetObj.getObjDictList(varList, [indexList[0]])
            basJet_obj_invMass_3j = helpers.invMass(jetList)
        elif saveTree.nBasJet == 3:
            jetList = jetObj.getObjDictList(varList, ([indexList[i] for i in range(2)]))
            basJet_obj_invMass_3j = helpers.invMass(jetList)
        else:
            jetList = jetObj.getObjDictList(varList, ([indexList[i] for i in range(3)]))
            basJet_obj_invMass_3j = helpers.invMass(jetList)
   
        # dR between leading lepton and b jet with highest discriminant
        if len(bJetDiscSortList) > 0:
            bJet_obj_dR_jHdobj1 = helpers.dR(bJetDiscSortList[0], objList[0], jetObj, lepObj)
        else:
            bJet_obj_dR_jHdobj1 = -999.
        #
        return basJet_obj_dR_j1obj1, basJet_obj_invMass_obj1jmindR, basJet_obj_invMass_3j, bJet_obj_dR_jHdobj1
        
    
    if (lepObj is not None) and (saveTree.nBasJet > 0):
        if (len(muList) > 0):
            basJet_mu_dR_j1mu1, basJet_mu_invMass_mu1jmindR, basJet_mu_invMass_3j, bJet_mu_dR_jHdmu1 = \
                variablesLeptonJets (
                    lepObj, jetObj, muList, basJetList, bJetDiscSortList
                    )
    
            saveTree.basJet_mu_dR_j1mu1 = basJet_mu_dR_j1mu1
            saveTree.basJet_mu_invMass_mu1jmindR = basJet_mu_invMass_mu1jmindR
            saveTree.basJet_mu_invMass_3j = basJet_mu_invMass_3j
            saveTree.bJet_mu_dR_jHdmu1 = bJet_mu_dR_jHdmu1
            
        if (len(elList) > 0):
            basJet_el_dR_j1el1, basJet_el_invMass_el1jmindR, basJet_el_invMass_3j, bJet_el_dR_jHdel1 = \
                variablesLeptonJets (
                    lepObj, jetObj, elList, basJetList, bJetDiscSortList
                    )
    
            saveTree.basJet_el_dR_j1el1 = basJet_el_dR_j1el1
            saveTree.basJet_el_invMass_el1jmindR = basJet_el_invMass_el1jmindR
            saveTree.basJet_el_invMass_3j = basJet_el_invMass_3j
            saveTree.bJet_el_dR_jHdel1 = bJet_el_dR_jHdel1
            
        if (len(lepList) > 0):
            basJet_lep_dR_j1lep1, basJet_lep_invMass_lep1jmindR, basJet_lep_invMass_3j, bJet_lep_dR_jHdlep1 = \
                variablesLeptonJets (
                    lepObj, jetObj, lepList, basJetList, bJetDiscSortList
                    )
    
            saveTree.basJet_lep_dR_j1lep1 = basJet_lep_dR_j1lep1
            saveTree.basJet_lep_invMass_lep1jmindR = basJet_lep_invMass_lep1jmindR
            saveTree.basJet_lep_invMass_3j = basJet_lep_invMass_3j
            saveTree.bJet_lep_dR_jHdlep1 = bJet_lep_dR_jHdlep1
            
            
            
    logger.debug(
        "\n basJet_mu_dR_j1mu1 = %f \n basJet_mu_invMass_mu1jmindR = %f \n basJet_mu_invMass_3j = %f \n\n" + \
        "\n basJet_el_dR_j1el1 = %f \n basJet_el_invMass_el1jmindR = %f \n basJet_el_invMass_3j = %f \n\n" + \
        "\n basJet_lep_dR_j1lep1 = %f \n basJet_lep_invMass_lep1jmindR = %f \n basJet_lep_invMass_3j = %f \n\n" + \
        "\n bJet_mu_dR_jHdmu1 = %f \n bJet_el_dR_jHdel1 = %f \n bJet_lep_dR_jHdlep1 = %f \n\n",
        saveTree.basJet_mu_dR_j1mu1, saveTree.basJet_mu_invMass_mu1jmindR, saveTree.basJet_mu_invMass_3j, 
        saveTree.basJet_el_dR_j1el1, saveTree.basJet_el_invMass_el1jmindR, saveTree.basJet_el_invMass_3j, 
        saveTree.basJet_lep_dR_j1lep1, saveTree.basJet_lep_invMass_lep1jmindR, saveTree.basJet_lep_invMass_3j, 
        saveTree.bJet_mu_dR_jHdmu1, saveTree.bJet_el_dR_jHdel1, saveTree.bJet_lep_dR_jHdlep1 
        )
        

            
    #
    return saveTree



def hemiSectorCosine(x):
    return round( math.cos(math.pi- 0.5*(x* math.pi/180)),3)


def processTracksFunction(readTree, splitTree, saveTree, params, lepObj, muList, elList, lepList, jetObj, basJetList):
    '''Process tracks. 
    
    TODO describe here the processing.
    FIXME the function needs a serious clean up...
    '''
    logger = logging.getLogger('cmgPostProcessing.processTracksFunction')
    
    # get the track parameters and matching parameters outside the track loop
    # to speed the program
    
    TracksSel = params['TracksSel']

    trackMinPtList = TracksSel['trackMinPtList']
    hemiSectorList = TracksSel['hemiSectorList']
    nISRsList      = TracksSel['nISRsList']
    
    # track selection
    TracksSelBas = TracksSel['bas']
    basTrackPt = TracksSelBas['pt']
    basTrackEta = TracksSelBas['eta']
    basTrackDxy = TracksSelBas['dxy']
    basTrackDz = TracksSelBas['dz']
    basTrackPdgId = TracksSelBas['pdgId']

    # track - jet matching
    jetPtThreshold = TracksSel['ptMatchJet']
    dRmatchJetTrack = TracksSel['dRmatchJetTrack']
    
    # track - leading lepton matching
    dRLepTrack = TracksSel['dRLepTrack']
    ratioPtLepTrackMin = TracksSel['ratioPtLepTrackMin']
    ratioPtLepTrackMax = TracksSel['ratioPtLepTrackMax']
    
    # leading lepton, jet collection as dictionaries
    if muList:
        lep = lepObj.getObjDictList(params['LepVarList']['mu'], muList[0])
    else:
        lep = {}
    jets = jetObj.getObjDictList(params['JetVarList'], basJetList)
     
    ### corresponding to 90, 135, 150 degree diff between jet and track
    hemiSectorCosines = {  x:hemiSectorCosine(x) for x in hemiSectorList } 
      
    varList = [
        'pt', 'eta', 'phi', "dxy", "dz", 'pdgId',
        "matchedJetIndex", "matchedJetDr",
        "CosPhiJet1", "CosPhiJet12", "CosPhiJetAll"
        ]
    trkVar=TracksSel['branchPrefix']
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
                abs(track['eta']) < basTrackEta and track['pt']>=basTrackPt and
                abs(track['dxy']) < basTrackDxy and abs( track['dz'] ) < basTrackDz 
                ) :
            continue
        if abs(track['pdgId']) in basTrackPdgId:
            #if len(selectedLeptons)>0 and hephyHelpers.deltaR(track, selectedLeptons[0] ) <0.1:
            if lep and hephyHelpers.deltaR(track, lep) < dRLepTrack and lep['pdgId']==track['pdgId'] :
                #Possible lepton track... shouldn't count the lepton that's being used, let's check Pt first ", deltaR(track, lep)
                if lep['pt']/track['pt'] < ratioPtLepTrackMax and lep['pt']/track['pt'] > ratioPtLepTrackMin:
                    #print "   yes most definitely is!"
                    continue
        if  (track['matchedJetDr'] < dRmatchJetTrack  ): 
            # Possible ISR track, will not count track if the jet pt greater than jetPtThreshold
            #matchedJet = allJets[int(track['matchedJetIndex'])]
            matchedJet = jets[int(track['matchedJetIndex'])]
            if matchedJet['pt'] > jetPtThreshold:
                # Track is matched with dr<dRmatchJetTrack to a jet with pt higher than jetpthtreshold. Dont want to count such a track!
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
    FIXME the function needs a serious clean up...
    '''
    
    logger = logging.getLogger('cmgPostProcessing.processGenTracksFunction')
    
    # get the generated track parameters and matching parameters outside the track loop
    # to speed the program
    
    GenTracksSel = params['GenTracksSel']

    genPartMinPtList = TracksSel['genPartMinPtList']
    hemiSectorList = TracksSel['hemiSectorList']
    nISRsList      = TracksSel['nISRsList']
    
    # track selection
    GenTracksSelBas = GenTracksSel['bas']
    basGenTrack_pt = GenTracksSelBas['pt']
    basGenTrack_eta = GenTracksSelBas['eta']

    # 
    varList = ['pt', 'eta', 'phi', 'pdgId' ]
    genPartPkds = (hephyHelpers.getObjDict(splitTree, 'genPartPkd_', varList, i) for i in range(readTree.ngenPartPkd))
    
    ngenPartPkds = { minPt : 0 for minPt in genPartMinPtList}
    ngenPartPkdsOppJet1 = { minPt : 0 for minPt in genPartMinPtList}
    ngenPartPkdsOpp90ISR = { minPt : 0 for minPt in genPartMinPtList}
    ngenPartPkdsOppJet12 = { minPt : 0 for minPt in genPartMinPtList}
    ngenPartPkdsOpp90ISR2 = { minPt : 0 for minPt in genPartMinPtList}
    
    for genPartPkd in genPartPkds:
        if not (abs(genPartPkd['eta']) < basGenTrack_eta and genPartPkd['pt'] >= basGenTrack_pt) :
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
    skimPreselect = args.skimPreselect
    
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

    # a more decent print of the dictionary of parameters 
    printParams = ''
    for key, value in params.iteritems():
        if 'vectors_' in key:
            continue
        printParams += "\n {0} =  \n {1} \n".format(key, pprint.pformat(value, indent=2))
        
    logger.info("\n Entries in the parameter dictionary: \n\n" + printParams + '\n\n')
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
    skimCond = eventsSkimPreselect(skim, skimLepton, skimPreselect, params, signalMasses)
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
                    saveTree, lepObj, muList, elList, lepList = processLeptons(
                        readTree, splitTree, saveTree, params
                        )
                    
                    # jets processing
                    saveTree, jetObj, basJetList, bJetDiscSortList = processJets(
                        args, readTree, splitTree, saveTree, params
                        )
                    
                    # selected leptons - jets processing
                    saveTree = processLeptonJets(
                        readTree, splitTree, saveTree, 
                        lepObj, muList, elList, lepList, 
                        jetObj, basJetList, bJetDiscSortList
                        )
                    
                    # tracks
                    if args.processTracks:
                        saveTree = processTracksFunction(
                            readTree, splitTree, saveTree, params, 
                            lepObj, muList, elList, lepList, 
                            jetObj, basJetList
                            )

                    if args.processGenTracks:
                        saveTree = processGenTracksFunction(readTree, splitTree, saveTree)
                    
                    # process event veto list flags
                    processEventVetoList(readTree, splitTree, saveTree, sample, event_veto_list)

                    if sampleType == 'MC':
                        processGenSusyParticles(readTree, splitTree, saveTree, params)


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
