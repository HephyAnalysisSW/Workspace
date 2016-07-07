''' Base argument parser for post processing script for CMG ntuples.

 
The arguments from this file are imported in cmgPostProcessing_v1 script and in 
runPostProcessing script, to avoid duplicate and inconsistent options.

'''
    
# imports python standard modules or functions
import argparse


# imports user modules or functions

import Workspace.HEPHYPythonTools.user as user

#

def get_parser():
    ''' Base argument parser for post processing script for CMG ntuples.
    
    '''
     
    argParser = argparse.ArgumentParser(description="Argument parser for cmgPostProcessing", add_help=False)
        
    argParser.add_argument('--logLevel',
        action='store',
        nargs='?',
        type=str,
        choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'],
        default='INFO',
        help="Log level for logging"
        )
    
    argParser.add_argument('--verbose',
        action='store_true',
        help="Switch for print statements, for those who can not survive a job without seeing something printed " + 
            "on the screen. \n bool flag set to True if used")

    argParser.add_argument('--targetDir',
        action='store',
        nargs='?',
        type=str,
        default='/afs/hephy.at/data/' + user.afsDataName + '/cmgTuples',
        help="Name of the directory the post-processed files will be saved"
        )
    
    argParser.add_argument('--overwriteOutputFiles',
        action='store_true',
        help="Overwrite existing output files, bool flag set to True  if used")
    
    
    argParser.add_argument('--cmgTuples',
        dest='cmgTuples',
        action='store',
        nargs='?',
        type=str,
        default='Spring15_7412pass2_mAODv2_v7',
        help="Sample definition file (w/o .py) for the CMG ntuples to be post-processed"
        )
       
    argParser.add_argument('--processSample',
        action='store',
        nargs='?',
        type=str,
        default='',
        help="Sample to be post-processed, given as CMG component name"
        )
    
    argParser.add_argument('--processingEra',
        action='store',
        nargs='?',
        type=str,
        default='postProcessed_mAODv2',
        help="Name of the processing era"
        )

    argParser.add_argument('--cmgProcessingTag',
        action='store',
        nargs='?',
        type=str,
        default='7412pass2_mAODv2_v6',
        help="Name of the CMG processing tag, preferably a tag for CMGTools"
        )

    argParser.add_argument('--cmgPostProcessingTag',
        action='store',
        nargs='?',
        type=str,
        default='cmgPostProc_v0',
        help="Name of the post-processing tag, preferably a tag for Workspace"
        )

    argParser.add_argument('--parameterSet',
        action='store',
        nargs='?',
        type=str,
        choices=['analysisHephy_13TeV_2016_v0', 'analysisHephy_13TeV_v0', 'analysisHephy_8vs13TeV_v0', 'syncLip_v0', ],
        default='analysisHephy_13TeV_2016_v0',
        help="Selection of the parameter set used for post-processing." 
        )

    argParser.add_argument('--skimGeneral',
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
        default='incLep',
        help="Lepton skimming to be applied for post-processing"
        )
    
    argParser.add_argument('--skimPreselect',
        action='store_true',
        help="Apply preselection for the post processing, bool flag set to True if used"
        )
    
    argParser.add_argument('--processSignalScan',
        action='store',
        nargs=2,
        type=int,
        help="Do Processing for a specific Stop and LSP mass"
        )
    
    argParser.add_argument('--processTracks',
        action='store_true',
        help="Process tracks for post-processing, bool flag set to True if used"
        )
    
    argParser.add_argument('--processGenTracks',
        action='store_true',
        help="Process packed generated particles for post-processing, bool flag set to True if used"
        )

    argParser.add_argument('--processLepAll',
        action='store_true',
        help="Process leptons from LepGood and LepOther, merging them in LepAll."
        )
     
    argParser.add_argument('--storeOnlyLepAll',
        action='store_true',
        help="Store only LepAll, do not store LepGood and LepOther. Effective only if processLepAll = True"
        )

    argParser.add_argument('--applyEventVetoList',
        action='store_true',
        help="Apply event veto list, if applyEventVetoList = True"
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

 
if __name__ == "__main__":
    sys.exit(get_parser())
