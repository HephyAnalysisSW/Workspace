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

from collections import namedtuple
from contextlib import contextmanager

# imports user modules or functions

import ROOT

import Workspace.DegenerateStopAnalysis.cmgObjectSelection as cmgObjectSelection
import Workspace.DegenerateStopAnalysis.helpers as helpers

import Workspace.HEPHYPythonTools.helpers as hephyHelpers
import Workspace.HEPHYPythonTools.convertHelpers as convertHelpers

import Workspace.HEPHYPythonTools.user as user

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
    
    argParser.add_argument('--overwriteOutputFiles',
        action='store_true',
        help="Overwrite existing output files, bool flag set to True  if used")
    
    argParser.add_argument('--cmgTuples',
        dest='cmgTuples',
        action='store',
        nargs='?',
        type=str,
        choices=['Data_25ns', 'Data_50ns', 'Spring15_25ns', 'Spring15_50ns', 'Spring15_25ns_packedGenPart_tracks'],
        default='Spring15_25ns',
        help="CMG ntuples to be post-processed"
        )
       
    argParser.add_argument('--processSamples',
        action='store',
        nargs='?',
        type=str,
        default='TTJets_LO',
        help="List of samples to be post-processed, given as CMG component name"
        )
    
    argParser.add_argument('--inputTreeName',
        action='store',
        nargs='?',
        type=str,
        default='treeProducerSusySingleLepton',
        help="Name of the input tree"
        )
    
    argParser.add_argument('--targetDir',
        action='store',
        nargs='?',
        type=str,
        default='/afs/hephy.at/data/' + user.afsDataName + '/cmgTuples',
        help="Name of the directory the post-processed files will be saved"
        )
    
    argParser.add_argument('--skim',
        action='store',
        nargs='?',
        type=str,
        default='',
        help="Skim conditions to be applied for post-processing"
        )
    
    argParser.add_argument('--leptonSelection',
        action='store',
        nargs='?',
        type=str,
        choices=['soft', 'hard', 'inc', 'dilep'],
        default='inc',
        help="Lepton selection to be applied for post-processing"
        )
    
    argParser.add_argument('--preselect',
        action='store_true',
        help="Apply preselection for the post processing, bool flag set to True if used"
        )
    
    argParser.add_argument('--processTracks',
        action='store_true',
        help="Process tracks for post-processing, bool flag set to True if used"
        )
    
    argParser.add_argument('--processPkdGenParts',
        action='store_true',
        help="Process packed generated particles for post-processing, bool flag set to True if used"
        )
     
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
     
    # create the logging file handler
    fileHandler = logging.FileHandler(logFile, mode='w')
 
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fileHandler.setFormatter(formatter)
 
    # add handler to logger object
    logger.addHandler(fileHandler)
  
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
        

def getSamples(cmgTuples, processSamples, targetDir):
    '''Return a list of components to be post-processed.
    
    No logger here, as the log file is determined with variables computed here.
    Simply exit if the required cmgTuples set or one of the samples do not exist, 
    printing the non-existing required set name.
    
    The sample processed will be written eventually in the logger,
    after a call to this function.
    '''

    subDir = ''
    
    if cmgTuples == "Data_25ns":
        # from Workspace.DegenerateStopAnalysis.cmgTuples_Data25ns import *
        import Workspace.DegenerateStopAnalysis.cmgTuples_Data25ns_fromArtur as cmgSamples
        subDir = "postProcessed_Data_25ns"
    elif cmgTuples == "Data_50ns":
        import Workspace.DegenerateStopAnalysis.cmgTuples_Data50ns_1l as cmgSamples
        subDir = "postProcessed_Data_50ns"
    elif cmgTuples == "Spring15_25ns":
        import Workspace.DegenerateStopAnalysis.cmgTuples_Spring15_7412pass2 as cmgSamples
        subDir = "postProcessed_Spring15_25ns_7412pass2"
    elif cmgTuples == "Spring15_50ns":
        import Workspace.DegenerateStopAnalysis.cmgTuples_Spring15_50ns as cmgSamples
        subDir = "postProcessed_Spring15_50ns"
    elif cmgTuples == "Spring15_25ns_packedGenPart_tracks":
        import Workspace.DegenerateStopAnalysis.cmgTuples_Spring15_packedGenPart_tracks as cmgSamples
        subDir = "postProcessed_Spring15_25ns_packedGenPart_tracks"
    else:
        print "\n The required set of CMG tuples \n cmgTuples: {0} does not exist.".format(cmgTuples), \
            "\n Correct the name and re-run the script. \n Exiting."
        sys.exit()
    
    outDir = targetDir + '/' + subDir
    
    # samples
    
    allComponentsList = [] 
    
    processSamples = processSamples.replace(' ', '')
    processSamplesList = []
    if len(processSamples):
        processSamplesList = processSamples.split(',')
        
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
            elif isinstance(sampleRequested, list):
                # list of components - add all components
                for comp in sampleRequested:
                        allComponentsList.append(comp)
                        foundSample = True
                continue 
            else:
                print "\n Not possible to build list of components for .".format(sampleName), \
                "\n Exiting."
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
                print "\n Not possible to build list of components for .".format(sampleName), \
                "\n Exiting."
                sys.exit()
                
                
        print "\n List of samples requested to be processed: \n {0} \n".format(pprint.pformat(processSamplesList))
        
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
    
    #
    return allComponentsList, outDir
    
     

def eventsSkimPreselect(skimName, leptonSelection, preselectFlag):
    '''Define the skim condition, including preselection if required.
    
    The skim condition depends on the skim name, the lepton selection, and on the
    event preselection. 
    '''

    logger = logging.getLogger('cmgPostProcessing.eventsSkimPreselect')
    
    # hard cut on lepton (fixed value, given here)
    lepton_soft_hard_cut  = 30 # GeV

    
    skimCond = "(1)"
    
    if skimName.startswith('met'):
        skimCond = "met_pt>" + str(float(skimName[3:]))
    elif skimName == 'HT400':
        skimCond = "Sum$(Jet_pt)>400"
    elif skimName == 'HT400ST200': 
        skimCond = "Sum$(Jet_pt)>400&&(LepGood_pt[0]+met_pt)>200"
    elif skimName == 'lheHThigh': 
        skimCond += "lheHTIncoming>=600"
    elif skimName == 'lheHTlow': 
        skimCond += "lheHTIncoming<600"
    else:
        pass
    
    # In case a lepton selection is required, loop only over events where there is one 
    if leptonSelection == 'soft':
        skimCond += "&&(Sum$(LepGood_pt>5&&LepGood_pt<{ptCut} &&abs(LepGood_eta)<2.4)>=1" + \
                   " || Sum$(LepOther_pt>5&&LepOther_pt<{ptCut} && abs(LepOther_eta)<2.4)>=1 " + \
                   ")".format(ptCut=lepton_soft_hard_cut)
    elif leptonSelection == 'hard':
        # skimCond += "&&Sum$(LepGood_pt>25&&LepGood_relIso03<0.4&&abs(LepGood_eta)<2.4)>=1"
        skimCond += "&&Sum$(LepGood_pt>%s&&abs(LepGood_eta)<2.4)>=1" % lepton_soft_hard_cut
    elif leptonSelection == 'dilep':
        # skimCond += "&&Sum$(LepGood_pt>25&&LepGood_relIso03<0.4&&abs(LepGood_eta)<2.4)>=1"
        skimCond += "&&Sum$(LepGood_pt>15&&abs(LepGood_eta)<2.4)>1"
    elif leptonSelection == 'inc':
        # skimCond += "&&Sum$(LepGood_pt>25&&LepGood_relIso03<0.4&&abs(LepGood_eta)<2.4)>=1"
        # skimCond += "&&Sum$(abs(LepGood_eta)< 2.5)>=1"
        skimCond += ""
    else:
        pass
    
    # overwrite lepton selection for inclusive skim     
    if skimName == 'inc':
        skimCond = "(1)"
      
    logger.info("\n Jobs running with skim = '%s' \n Skimming condition: \n  %s \n ", skimName, skimCond)
    
    if preselectFlag:
        # preselectionCuts = "(met_pt > 200 && Jet_pt[0]> 100 && Sum$(Jet_pt)>200 )"
        preselectionCuts = "(met_pt > 100 && Jet_pt[0]> 80 && Sum$(Jet_pt)>100 )"
        logger.info("\n Applying preselection cuts: %s ", preselectionCuts)
        skimCond += "&&%s" % preselectionCuts
        logger.info("\n Skimming condition with preselection: \n  %s \n", skimCond)
    else:
        logger.info("\n No preselection cuts are applied for skim %s \n Skimming condition unchanged \n", skimName)
        pass
 
    #
    return skimCond

 
 
def rwTreeClasses(sample, isample, args, temporaryDir, trackMinPtList):
    '''Define the read / write tree classes for data and MC.
    
    '''

    logger = logging.getLogger('cmgPostProcessing.rwTreeClasses')
    
    # define the branches and the variables to be kept and/or read for data and MC
    
    # data and MC samples 
    
    # common branches already defined in cmgTuples
    branchKeepStrings_DATAMC = [
        'run', 'lumi', 'evt', 'isData', 'rho', 'nVert', 
        'nJet25', 'nBJetLoose25', 'nBJetMedium25', 'nBJetTight25', 
        'nJet40', 'nJet40a', 'nBJetLoose40', 'nBJetMedium40', 'nBJetTight40', 
        'nLepGood20', 'nLepGood15', 'nLepGood10', 
        'htJet25', 'mhtJet25', 'htJet40j', 'htJet40', 'mhtJet40', 
        'nSoftBJetLoose25', 'nSoftBJetMedium25', 'nSoftBJetTight25', 
        'met*','puppi*','Flag_*','HLT_*',
        #'nFatJet','FatJet_*', 
        'nJet', 'Jet_*', 
        'nLepGood', 'LepGood_*', 
        'nLepOther', 'LepOther_*', 
        'nTauGood', 'TauGood_*',
        'track_*', 'isoTrack_*',
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
                    'miniRelIso/F','mass/F','sip3d/F','mediumMuonId/I', 
                    'mvaIdPhys14/F','lostHits/I', 'convVeto/I']},
        {'prefix':'LepGood',  'nMax':8, 
            'vars':['pt/F', 'eta/F', 'phi/F', 'pdgId/I', 'relIso03/F', 'tightId/I', 
                    'miniRelIso/F','mass/F','sip3d/F','mediumMuonId/I', 
                    'mvaIdPhys14/F','lostHits/I', 'convVeto/I']},
        {'prefix':'Jet',  'nMax':100, 
            'vars':['pt/F', 'eta/F', 'phi/F', 'id/I','btagCSV/F', 'btagCMVA/F', 'mass/F']},
      ])
     
    if args.leptonSelection in ['soft', 'hard', 'inc']:
        
        newVariables_DATAMC.extend([
            'nBJetMediumCSV30/I', 'nSoftBJetsCSV/F', 'nHardBJetsCSV/F',  
            'nJet30/I','htJet30j/F','nJet60/I','nJet110/I','nJet325/I' ,
            ])
        
        newVariables_DATAMC.extend([
            'nLooseSoftLeptons/I', 'nLooseSoftPt10Leptons/I', 'nLooseHardLeptons/I', 
            'nTightSoftLeptons/I', 'nTightHardLeptons/I',
            ])
        
        newVariables_DATAMC.extend([
            'singleMuonic/I', 'singleElectronic/I', 'singleLeptonic/I', 
            ])
        
        newVariables_DATAMC.extend([
            'leptonPt/F','leptonMiniRelIso/F','leptonRelIso03/F' ,
            'leptonEta/F',  'leptonPhi/F', 'leptonPdg/I/0', 'leptonInd/I/-1', 
            'leptonMass/F', 'leptonDz/F', 'leptonDxy/F', 
            
            'lepGoodPt/F','lepGoodMiniRelIso/F','lepGoodRelIso03/F' , 'lepGoodRelIso04/F',
            'lepGoodAbsIso/F' ,'lepGoodEta/F',  'lepGoodPhi/F', 'lepGoodPdgId/I/0', 'lepGoodInd/I/-1', 
            'lepGoodMass/F', 'lepGoodDz/F', 'lepGoodDxy/F','lepGoodMediumMuonId/I','lepGoodSip3d/F',
            
            'lepOtherPt/F','lepOtherMiniRelIso/F','lepOtherRelIso03/F' , 'lepOtherRelIso04/F',
            'lepOtherAbsIso/F' ,'lepOtherEta/F',  'lepOtherPhi/F', 'lepOtherPdgId/I/0', 'lepOtherInd/I/-1', 
            'lepOtherMass/F', 'lepOtherDz/F', 'lepOtherDxy/F','lepOtherMediumMuonId/I','lepOtherSip3d/F',
            
            'lepPt/F','lepMiniRelIso/F','lepRelIso03/F' , 'lepRelIso04/F',
            'lepAbsIso/F' ,'lepEta/F',  'lepPhi/F', 'lepPdgId/I/0', 'lepInd/I/-1', 
            'lepMass/F', 'lepDz/F', 'lepDxy/F','lepMediumMuonId/I','lepSip3d/F',
            'nlep/I',
            ])
            
        newVariables_DATAMC.extend([
            'Q80/F','CosLMet/F',
            'st/F', 'deltaPhi_Wl/F',
            'mt/F',
            ])
              
        newVariables_DATAMC.extend([
            'jet1Pt/F','jet1Eta/F','jet1Phi/F', 
            'jet2Pt/F','jet2Eta/F','jet2Phi/F',
            'deltaPhi_j12/F', 'dRJet1Jet2/F',
            'JetLepMass/F','dRJet1Lep/F',
            'J3Mass/F',
            ])
        
        #newVariables_DATAMC.extend([
        #    'mt2w/F'
        #    ] )
    
    
    if args.processTracks:
        
        newTrackVars = []
        for minTrkPt in trackMinPtList:
            ptString = str(minTrkPt).replace(".","p")
            newTrackVars.extend( [ x%ptString for x in  [ "ntracks_%s/I" ,"ntrackOppJet1_%s/I" ,"ntrackOppJet12_%s/I" , 
                                                         "ntrackOppJetAll_%s/I" ] ] )
        
        newVariables_DATAMC.extend(newTrackVars) 
    
        readVectors_DATAMC.extend([
            {'prefix':'track'  , 'nMax':1000, 
                'vars':['pt/F', 'eta/F', 'phi/F', 'pdgId/I' , 'dxy/F', 'dz/F', 'fromPV/I'] },
            ])
        
    
    
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
        'ngenPartAll','genPartAll_*' ,
        'ngenTau', 'genTau_*', 
        'ngenLepFromTau', 'genLepFromTau_*', 
        'GenJet_*',
         ]
    
    readVariables_MC = []
    aliases_MC = []
    newVariables_MC = []
    
    readVectors_MC = []
    
    aliases_MC.extend(['genMet:met_genPt', 'genMetPhi:met_genPhi'])
    
    if args.processPkdGenParts:
        branchKeepStrings_MC.extend(['genPartPkd_*'])
        
        newVariables_MC.extend([
            'genPartPkd_ISRdPhi/F' , 'genPartPkd_CosISRdPhi/F' ,
            'ngenPartPkd_1p5/I/0','ngenPartPkd_1/I/0','ngenPartPkd_2/I/0',
            'ngenPartPkdOppJet1_1/F','ngenPartPkdOppJet1_1p5/F', 'ngenPartPkdOppJet1_2/F',
            'ngenPartPkdO90isr_1/F', 'ngenPartPkdO90isr_1p5/F', 'ngenPartPkdO90isr_2/F', 
            ])
    
        readVectors_MC.extend([
            {'prefix':'genPartPkd'  , 'nMax':1000, 'vars':['pt/F', 'eta/F', 'phi/F', 'pdgId/I' ] },
            {'prefix':'GenJet'  , 'nMax':100, 'vars':['pt/F', 'eta/F', 'phi/F', 'mass/F' ] },
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

    logger.debug("\n read variables (readVars) definition: \n %s \n", pprint.pformat(readVars))
    logger.debug("\n aliases definition: \n %s \n", pprint.pformat(aliases))
    logger.debug("\n read vectors (readVectors) definition: \n %s \n", pprint.pformat(readVectors))
    logger.debug("\n new variable (newVars) definition: \n %s \n", pprint.pformat(newVars))

    convertHelpers.printHeader("Compiling class to write")
    writeClassName = "ClassToWrite_"+str(isample)
    writeClassString = convertHelpers.createClassString(className=writeClassName, vars= newVars, vectors=[], 
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
    return branchKeepStrings, readVars, aliases, readVectors, newVars, readTree, saveTree
   
   
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



def processLeptons(leptonSelection, readTree, splitTree, saveTree):
    '''Process leptons. 
    
    TODO describe here the processing.
    '''

    logger = logging.getLogger('cmgPostProcessing.processLeptons')
    
    # initialize returned variables (other than saveTree)
    
    lep = None

    if leptonSelection in ['soft','hard','inc']:

        # get all >=loose lepton indices
        looseLepInd = cmgObjectSelection.cmgLooseLepIndices(
            readTree, ptCuts=(7,5), absEtaCuts=(2.5,2.4), 
            ele_MVAID_cuts={'eta08':0.35 , 'eta104':0.20,'eta204': -0.52} 
            ) 
        
        # split loose leptons into soft (pT < lepton_soft_hard_cut) and hard 
        # leptons (> lepton_soft_hard_cut) 
        # FIXME: unify the cut from skimming with this cut?
        lepton_soft_hard_cut = 30.
        looseSoftLepInd, looseHardLepInd = cmgObjectSelection.splitIndList(
            readTree.LepGood_pt, looseLepInd, lepton_soft_hard_cut)
        
        # select tight hard leptons (use POG ID)
        tightHardLepInd = filter(lambda i:
            (
             abs(readTree.LepGood_pdgId[i])==11 and 
             readTree.LepGood_miniRelIso[i]<0.1 and 
             cmgObjectSelection.ele_ID_eta(
                readTree,nLep=i,ele_MVAID_cuts={'eta08':0.73 , 'eta104':0.57,'eta204':  0.05}) and 
             readTree.LepGood_tightId[i]>=3
             ) or 
            (
             abs(readTree.LepGood_pdgId[i])==13 and 
             readTree.LepGood_miniRelIso[i]<0.2 and 
             readTree.LepGood_tightId[i]), looseHardLepInd)  
        saveTree.nTightHardLeptons = len(tightHardLepInd)

        varList = ['pt', 'eta', 'phi', 'miniRelIso','relIso03','relIso04', 'dxy', 'dz', 'pdgId', 'sip3d','mediumMuonId']

        lepGoods =   [hephyHelpers.getObjDict(splitTree, 'LepGood_',varList, i ) for i in range(readTree.nLepGood)]
        lepOthers =  [hephyHelpers.getObjDict(splitTree, 'LepOther_',varList, i ) for i in range(readTree.nLepOther)]
        allLeptons = lepGoods + lepOthers
        
        selectedLeptons = filter(cmgObjectSelection.isGoodLepton , allLeptons)
        selectedLeptons = sorted(selectedLeptons ,key= lambda lep: lep['pt'], reverse=True)

        logger.debug(
            "\n nlepGood = %i,  nlepOther = %i " + \
            "\n Number of all leptons (Good + Other): %i (Good: %i + Other: %i)"  + \
            "\n Selected leptons:\n  %s  \n"  + \
            "\n Number of selected leptons: %i \n", 
            readTree.nLepGood, readTree.nLepOther, len(allLeptons), 
            len(lepGoods), len(lepOthers),
            pprint.pformat(selectedLeptons), len(selectedLeptons)
            )
                    
        varsToKeep = varList + []
        if selectedLeptons:
            lep = selectedLeptons[0]
            lepName = "lep"
            for var in varsToKeep:
                varName = lepName + var[0].capitalize() + var[1:]
                setattr(saveTree, varName, lep[var])
            saveTree.lepAbsIso = lep['relIso04'] * lep['pt'] 
            saveTree.nlep = len(selectedLeptons)
            saveTree.singleLeptonic = (saveTree.nlep == 1)
             
            if logger.isEnabledFor(logging.DEBUG):
                logString = "\n Leading selected lepton: "
                for var in varsToKeep:
                    logString += "\n " + lepName + var[0].capitalize() + var[1:] + " = %f"
                logString += "\n"
                logger.debug(
                    logString % 
                    (tuple(getattr(saveTree, lepName + var[0].capitalize() + var[1:]) for var in varsToKeep))
                    )
    
        if saveTree.singleLeptonic:
            saveTree.singleMuonic      =  abs(saveTree.leptonPdg)==13
            saveTree.singleElectronic  =  abs(saveTree.leptonPdg)==11
        else:
            saveTree.singleMuonic      = False 
            saveTree.singleElectronic  = False 

    #
    return saveTree, lep

def selectionJets(readTree, ptCut):
    '''Post-processing standard jet selection. 
    
    '''
    
    jetVariables = ['eta', 'pt', 'phi', 'btagCMVA', 'btagCSV', 'id', 'mass']
    
    jets = filter(lambda j:
        j['pt'] > ptCut and abs(j['eta']) < 2.4 and j['id'], 
        cmgObjectSelection.get_cmg_jets_fromStruct(readTree, jetVariables))
    
    return jets


def processJets(leptonSelection, readTree, splitTree, saveTree):
    '''Process jets. 
    
    TODO describe here the processing.
    '''

    logger = logging.getLogger('cmgPostProcessing.processJets')
    
    # initialize returned variables (other than saveTree)
    
    jets = None
    
    if leptonSelection in ['soft', 'hard', 'inc']:
        
        # selection of jets
        
        ptCut = 30 
        jets = selectionJets(readTree, ptCut)
        logger.debug("\n Selected jets: %i jets \n %s \n", len(jets), pprint.pformat(jets))
        
        ptCut = 60 
        jets60 = selectionJets(readTree, ptCut)

        ptCut = 110
        jets110 = selectionJets(readTree, ptCut)

        saveTree.nJet30 = len(jets)
        saveTree.nJet60 = len(jets60)
        saveTree.nJet110 = len(jets110)
        saveTree.nJet325 = len(filter(lambda j: j["pt"] > 325 , jets110))
       
        # separation of jets and bJets according to discriminant (CMVA;  CSV - default)
        
        discCMVA = 0.732
        discCSV = 0.890
        cutSoftHardBJets = 60
        
        lightJetsCMVA, bJetsCMVA = cmgObjectSelection.splitListOfObjects('btagCMVA', discCMVA, jets) 
        lightJetsCSV, bJetsCSV = cmgObjectSelection.splitListOfObjects('btagCSV', discCSV, jets)
        
        logger.debug("\n Selected CMVA b jets: %i jets \n %s \n", len(bJetsCMVA), pprint.pformat(bJetsCMVA))
        logger.debug("\n Selected CSV b jets: %i jets \n %s \n", len(bJetsCSV), pprint.pformat(bJetsCSV))

        bJets = filter(lambda j: j["btagCSV"] > discCSV , jets)
        
        softBJetsCSV, hardBJetsCSV = cmgObjectSelection.splitListOfObjects('pt', cutSoftHardBJets, bJets)
        
        saveTree.nSoftBJetsCSV = len(softBJetsCSV)
        saveTree.nHardBJetsCSV = len(hardBJetsCSV)
        saveTree.nBJetMediumCSV30 = len(bJetsCSV)
        
        logger.debug("\n Number of soft and hard b jets (CSV): \n  soft: %i \n  hard: %i \n  total: %i \n", 
                     saveTree.nSoftBJetsCSV  ,saveTree.nHardBJetsCSV,  saveTree.nBJetMediumCSV30)

        # HT as sum of jets pT > 30 GeV
        
        saveTree.htJet30j = sum([x['pt'] for x in jets])

        # save some additional jet quantities

        if saveTree.nJet30 > 0:    
            saveTree.jet1Pt = jets[0]['pt']
            saveTree.jet1Eta = jets[0]['eta']
            saveTree.jet1Phi = jets[0]['phi']

        if saveTree.nJet30 > 1:
            saveTree.jet2Pt = jets[1]['pt']
            saveTree.jet2Eta = jets[1]['eta']
            saveTree.jet2Phi = jets[1]['phi']
            
            saveTree.dRJet1Jet2 = hephyHelpers.deltaR(jets[0], jets[1])
            
        if saveTree.nJet60 == 0:
            saveTree.deltaPhi_j12 = 999
        elif saveTree.nJet60 == 1:
            saveTree.deltaPhi_j12 = 0.
        else:
            saveTree.deltaPhi_j12 = min(
                2 * math.pi - abs(jets60[1]['phi'] - jets60[0]['phi']),
                abs(jets60[1]['phi'] - jets60[0]['phi'])
                )
 
        
    
    #
    return saveTree, jets

def processLeptonJets(leptonSelection, readTree, splitTree, saveTree, lep, jets):
    '''Process correlations between the leading selected lepton and jets. 
    
    Compute:
        dR separation of selected lepton and first jet
        invariant mass of the selected leading lepton and the dR-closest jet
        invariant mass of 1, 2, 3 jets, other than the closest jet associated to lepton 
        
        Jets are considered having mass here, lepton have mass zero.

    '''
    
    logger = logging.getLogger('cmgPostProcessing.processLeptonJets')
    

    if leptonSelection in ['soft', 'hard', 'inc']:
         
        if (lep is not None) and (saveTree.nJet30 > 0):
            
            saveTree.dRJet1Lep = hephyHelpers.deltaR(jets[0], lep)
            
            # find the dR-closest jet to selected muon
            closestJetIndex = min(range(len(jets)), key=lambda j:hephyHelpers.deltaR(jets[j], lep))
            logger.debug("\n Lepton: \n %s, \n \n Closest jet index: %i, \n Jet: \n %s \n dR(lep, jet): %f \n",
                pprint.pformat(lep), closestJetIndex, pprint.pformat(jets[closestJetIndex]),
                hephyHelpers.deltaR(jets[closestJetIndex], lep))
                    
            # invariant mass of the selected leading lepton and the dR-closest jet            
            saveTree.JetLepMass = helpers.invMass([jets[closestJetIndex], lep])
            
            # invariant mass of 1, 2, 3 jets, other than the closest jet associated to lepton 
        
            indexList = [i for i in xrange(len(jets)) if i != closestJetIndex]  
            logger.debug(
                "\n Number of jets, excluding the closest jet: %i jets \n List of jet indices: \n %s \n ", 
                len(indexList), pprint.pformat(indexList)
                )
                   
            if saveTree.nJet30 == 1: 
                saveTree.J3Mass = 0.
            elif saveTree.nJet30 == 2:
                jetList = [jets[indexList[0]]]
                saveTree.J3Mass = helpers.invMass(jetList)
            elif saveTree.nJet30 == 3:
                jetList = [jets[indexList[0]], jets[indexList[1]]]
                saveTree.J3Mass = helpers.invMass(jetList)
            else:
                jetList = [jets[indexList[0]], jets[indexList[1]], jets[indexList[2]]]
                saveTree.J3Mass = helpers.invMass(jetList)
       
    
            logger.debug(
                "\n dRJet1Lep: %f \n JetLepMass: %f \n J3Mass: %f \n", 
                saveTree.dRJet1Lep, saveTree.JetLepMass, saveTree.J3Mass
                )
            
    #
    return saveTree


def processTracksFunction(readTree, splitTree, saveTree, trackMinPtList, disableTracksDebugLogging):
    '''Process tracks. 
    
    TODO describe here the processing.
    '''
    
    logger = logging.getLogger('cmgPostProcessing.processTracksFunction')
    
    if disableTracksLogging:
        logger.propagate = False

    varList = [
        'pt', 'eta', 'phi', "dxy", "dz", 'pdgId' ,
        "matchedJetIndex", "matchedJetDr",
        "CosPhiJet1", "CosPhiJet12", "CosPhiJetAll"
        ]
    tracks = (hephyHelpers.getObjDict(splitTree, 'track_', varList, i) for i in range(readTree.ntrack))
    
    ntrack = { minPt : 0 for minPt in trackMinPtList}
    ntrackOppJet1 = { minPt : 0 for minPt in trackMinPtList}
    ntrackOppJet12 = { minPt : 0 for minPt in trackMinPtList}
    ntrackOppJetAll = { minPt : 0 for minPt in trackMinPtList}
    ntrackOpp90Jet1 = { minPt : 0 for minPt in trackMinPtList}
    ntrackOpp90Jet12 = { minPt : 0 for minPt in trackMinPtList}
    ntrackOpp90JetAll = { minPt : 0 for minPt in trackMinPtList}
    
    for track in tracks:
        if not (
            abs(track['eta']) < 2.5 and abs(track['dxy']) < 0.02 and 
            abs(track['dz']) < 0.5 and track['pt'] >= 1.0
            ) :
            continue
        if not (
            track["matchedJetIndex"] == -1  and track['matchedJetDr'] > 0.4  
            ):
            # # also check jet pt  ## vetoing tracks that are matched to a jet 
            continue
        for minTrkPt in trackMinPtList:
            if track['pt'] > minTrkPt:
                ntrack[minTrkPt] += 1
                if track['CosPhiJet1'] < 0:
                    ntrackOppJet1[minTrkPt] += 1
                if track['CosPhiJet12'] < 0:
                    ntrackOppJet12[minTrkPt] += 1
                if track['CosPhiJetAll'] < 0:
                    ntrackOppJetAll[minTrkPt] += 1    
            logger.trace("\n Track: \n %s \n", pprint.pformat(track))
    
#         if cos(track['phi'] - saveTree.jet1Phi) < 0:
#             for trackMinPt in trackMinPtList:
#                 if track['pt'] > trackMinPt:
#                     ntracksOppISR[trackMinPt] += 1
#             if cos(track['phi'] - saveTree.jet1Phi) < -sqrt(2) / 2:
#                 for trackMinPt in trackMinPtList:
#                     if track['pt'] > trackMinPt:
#                         ntracksOpp90ISR[trackMinPt] += 1
# 
#         for trackMinPt in trackMinPtList:
#             if track['pt'] > trackMinPt:
#                 ntracks[trackMinPt] += 1
#                 logger.debug("\n added one track to %f \n %f", trackMinPt, ntracks[trackMinPt])
#                 FIXME check the message above if correct, when un-commening 
          
    for minTrkPt in trackMinPtList:
        trkPtString = str(minTrkPt).replace(".", "p")
        setattr(saveTree, "ntracks_%s" % trkPtString        , ntrack[minTrkPt])
        setattr(saveTree, "ntrackOppJet1_%s" % trkPtString  , ntrackOppJet1[minTrkPt])
        setattr(saveTree, "ntrackOppJet12_%s" % trkPtString , ntrackOppJet12[minTrkPt])  
        setattr(saveTree, "ntrackOppJetAll_%s" % trkPtString, ntrackOppJetAll[minTrkPt])
    
    #
    return saveTree
 

  
def processPkdGenPartsFunction(readTree, splitTree, saveTree):
    '''Process generated particles. 
    
    TODO describe here the processing.
    '''
    
    logger = logging.getLogger('cmgPostProcessing.processPkdGenPartsFunction')
    
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


def computeWeight(target_lumi, sample, sumWeight, splitTree, saveTree):
    ''' Compute the weight of each event.
    
    Include all the weights used:
        genWeight - weight of generated events (MC only, set to 1 for data)
        luminosity weight 
    '''

    logger = logging.getLogger('cmgPostProcessing.computeWeight')
        
    # sample type (data or MC, taken from CMG component)
    isDataSample = sample['cmgComp'].isData
    
    # weight according to required luminosity 
    
    genWeight = 1 if isDataSample else splitTree.GetLeaf('genWeight').GetValue()

    if isDataSample: 
        lumiScaleFactor = 1
    else:
        lumiScaleFactor = sample['cmgComp'].xSection * target_lumi / float(sumWeight)
        
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

def cmgPostProcessing(argv=None):
    
    if argv is None:
        argv = sys.argv[1:]
    
    # parse command line arguments
    args = get_parser().parse_args()
    
    # job control parameters
    
    overwriteOutputFiles = args.overwriteOutputFiles
    
    skim = args.skim
    leptonSelection = args.leptonSelection
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
    processSamples = args.processSamples
    
    allSamples, outputDirectory = getSamples(cmgTuples, processSamples, args.targetDir)
     
    # create the target output directory, if it does not exist
    if not os.path.exists(outputDirectory):
        os.makedirs(outputDirectory)

    # logging configuration

    logLevel = args.logLevel
    
    # use a unique name for the log file, write file in the dataset directory
    prefixLogFile = 'cmgPostProcessing_' + '_'.join([sample['cmgComp'].name for sample in allSamples]) + \
         '_' + logLevel + '_'
    logFile = tempfile.NamedTemporaryFile(suffix='.log', prefix=prefixLogFile, dir=outputDirectory, delete=False) 

    logger = get_logger(logLevel, logFile.name)

    #
    logger.info(
        "\n Running on CMG ntuples %s " + \
        "\n Samples to be processed: %i \n %s \n",  
        cmgTuples, len(allSamples), pprint.pformat([sample['cmgComp'].name for sample in allSamples])
        )
    logger.debug("\n Samples to be processed: %i \n %s \n",  
        len(allSamples), pprint.pformat(allSamples))
    
    # define job parameters
    # TODO include here all the selection parameters, to avoid hardcoded values in multiple places in the code 
    
    # target luminosity (fixed value, given here)
    target_lumi = 10000  # pb-1
    
    logger.info("\n Target luminosity: %f pb^{-1} \n", target_lumi)
    
    if args.processTracks:
        trackMinPtList= [1,1.5,2,2.5,3]
        logger.info("\n trackMinPtList: %s \n", pprint.pformat(trackMinPtList))
    else:
        trackMinPtList = []

    # skim condition 
    skimCond =  eventsSkimPreselect(skim, leptonSelection, preselect)
    logger.info("\n Final skimming condition: \n  %s \n", skimCond)
    
    # loop over each sample, process all variables and fill the saved tree
    
    for isample, sample in enumerate(allSamples):
        
        sampleName = sample['cmgComp'].name
        sampleType = 'Data' if sample['cmgComp'].isData else 'MC'
                      
        chunks, sumWeight = hephyHelpers.getChunks(sample)
                
        logger.info(
            "\n Running on sample %s of type %s" + \
            "\n Number of chunks: %i \n", sampleName, sampleType, len(chunks)
            ) 
        logger.debug("\n Chunks: %s", pprint.pformat(chunks)) 
        
        if runSmallSample: 
            chunks=chunks[:1]
            logger.debug("\n Chunks for runSmallSample option: \n %s\n", pprint.pformat(chunks)) 
        
        # create the output sample directory, if it does not exist. 
        # If it exists and overwriteOutputFiles is set to True, clean up the directory; if overwriteOutputFiles is 
        # set to False, skip the post-processing of this component.
        #
        # create also a temporary directory (within the output directory)
        # that will be deleted automatically at the end of the job. If the directory exists,
        # it will be deleted and re-created.
        
        outputWriteDirectory = os.path.join(outputDirectory, skim, leptonSelection, sample['name'])
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
                logger.debug(
                    "\n Requested sample directory \n %s \n exists, and overwriteOutputFiles is set to True." + \
                    "\n Cleaned up and recreated the directory done. \n", 
                    outputWriteDirectory
                    )
            else:
                logger.error(
                    "\n Requested sample directory \n %s \n exists, and overwriteOutputFiles is set to False." + \
                    "\n Skip post-processing sample %s \n", 
                    outputWriteDirectory, sample['name']
                    )
                
                continue
        
        # python 2.7 version - must be removed by hand, preferably in a try: ... finalize:
        temporaryDir = tempfile.mkdtemp(dir=outputDirectory) 
        #
        # for 3.X use
        # temporaryDir = tempfile.TemporaryDirectory(suffix=None, prefix=None, dir=None)
             
        logger.info("\n Output sample directory \n  %s \n" , outputWriteDirectory) 
        logger.debug("\n Temporary directory \n  %s \n" , temporaryDir) 
        
        branchKeepStrings, readVars, aliases, readVectors, newVars, readTree, saveTree = \
            rwTreeClasses(sample, isample, args, temporaryDir, trackMinPtList)
                   
        filesForHadd=[]

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
                
                # addresses for all variables (read and write) must be done here to take the correct address
                
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
    
                # get entries for tree and loop over events
                
                nEvents = splitTree.GetEntries()
                logger.debug(
                    "\n Number of events after skimming and preselection: \n    chunk: %s \n    " + \
                    "split fragment %i of %i fragments in this chunk: \n    %i events \n", 
                    chunk['name'], iSplit, nSplit, nEvents
                    )
                
                for iEv in range(nEvents):
                    
                    if (iEv%10000 == 0) and iEv>0 :
                        logger.debug(
                            "\n Processing event %i from %i events from chunck \n %s \n",
                            iEv, nEvents, chunk['name']
                            )
            
                    saveTree.init()
                    readTree.init()
                    splitTree.GetEntry(iEv)
                    
                    logger.debug(
                        "\n " + \
                        "\n ================================================" + \
                        "\n * Processing Run:Luminosity segment:Event number " + \
                        "\n *     %i : %i : %i \n", 
                        splitTree.run, splitTree.lumi, splitTree.evt 
                        )
                    
                    # leptons processing
                    saveTree, lep  = processLeptons(leptonSelection, readTree, splitTree, saveTree)
                    
                    # jets processing
                    saveTree, jets = processJets(leptonSelection, readTree, splitTree, saveTree)
                    
                    # selected leptons - jets processing
                    saveTree = processLeptonJets(leptonSelection, readTree, splitTree, saveTree, lep, jets)

                    if args.processTracks:
                        saveTree = processTracksFunction(readTree, splitTree, saveTree, trackMinPtList)

                    if args.processPkdGenParts:
                        saveTree = processPkdGenPartsFunction(readTree, splitTree, saveTree)
                    
                    # process various tranverse masses and other variables
                    saveTree = processMasses(readTree, saveTree)
              
                    # compute the weight of the event
                    saveTree = computeWeight(target_lumi, sample, sumWeight, splitTree, saveTree)
                    
                    # fill all the new variables          
                    for v in newVars:
                        v['branch'].Fill()
                        

                # 
                
                fileTreeSplit = sample['name'] + '_' + chunk['name'] + '_' + str(iSplit) + '.root' 
                filesForHadd.append(fileTreeSplit)
                
                if not testMethods:
                    tfileTreeSplit = ROOT.TFile(temporaryDir + '/' + fileTreeSplit, 'recreate')
                    splitTree.SetBranchStatus("*", 0)
                    for b in (branchKeepStrings + 
                              [v['stage2Name'] for v in newVars] + 
                              [v.split(':')[1] for v in aliases]):
                        splitTree.SetBranchStatus(b, 1)
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
    
        logger.debug(
            "\n " + \
            "\n End of processing events for sample %s . Start summing up the chunks. " + \
            "\n *******************************************************************************\n",
            sampleName
            )
        
        # add the histograms using ROOT hadd script
        # if
        #     input files to be hadd-ed sum to more than maxFileSize MB or
        #     the number of files to be added is greater than  maxNumberFiles
        # then split the hadd
         
        if not testMethods: 
            
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
                    ofile = outputWriteDirectory + '/' + sample['name'] + '_' + str(counter) + '.root'
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
                    "\n Delete it by hand.", 
                    temporaryDir
                    )
                    
    logger.info(
        "\n " + \
        "\n End of post-processing sample %s " + \
        "\n *******************************************************************************\n",
        sampleName
        )
   
    
 
if __name__ == "__main__":
    sys.exit(cmgPostProcessing())
