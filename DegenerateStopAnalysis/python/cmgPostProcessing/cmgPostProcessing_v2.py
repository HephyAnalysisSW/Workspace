''' Post processing script for CMG ntuples. 

'''
    
# imports python standard modules or functions
import argparse
import logging
import sys
import tempfile
import os
import shutil
import glob
import pprint
import math
import time
import importlib
import copy
import operator
import functools
import collections
import errno
import subprocess
import pickle


# imports user modules or functions

import ROOT

import Workspace.DegenerateStopAnalysis.cmgPostProcessing.cmgObjectSelection as cmgObjectSelection
import Workspace.DegenerateStopAnalysis.cmgPostProcessing.cmgPostProcessing_parser as cmgPostProcessing_parser
import Workspace.DegenerateStopAnalysis.tools.helpers as helpers

import Workspace.HEPHYPythonTools.helpers as hephyHelpers
import Workspace.HEPHYPythonTools.convertHelpers as convertHelpers

import Workspace.HEPHYPythonTools.user as user

from  veto_event_list import get_veto_list

def get_parser():
    ''' Argument parser for post-processing module.
    
    '''
     
    argParser = argparse.ArgumentParser(
        description="Argument parser for cmgPostProcessing", 
        parents=[cmgPostProcessing_parser.get_parser()]
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

    #
    # arguments to build the parameter set
    parameterSet = args.parameterSet
    processTracks = args.processTracks

    processLepAll = args.processLepAll
    storeOnlyLepAll = args.storeOnlyLepAll

    # parameter sets
    parSetFullName = 'Workspace.DegenerateStopAnalysis.cmgPostProcessing.parameterSets.' + parameterSet
    
    try:
        parameters = importlib.import_module(parSetFullName)
    except ImportError, err:      
        print 'ImportError:', err
        print "\n The required parameter set {0} \n ".format(parSetFullName) + \
            "can not be imported.", \
            "\n Correct the name and re-run the script. \n Exiting."
        sys.exit()

    # 
    params = parameters.getParameterSet(args)
    
    if  args.processBTagWeights:

        from Workspace.DegenerateStopAnalysis.cmgPostProcessing.btagEfficiency import btagEfficiency

        sampleName = args.processSample
        btagwp = "CSVv2M"
        eff_dict_map = [
                        #( "TTJets_1j"                          , { 'sampleList' : ["TTJets_FastSIM" , ]  ,     'isFastSim':True              }   ),
                        #( "WJets_2D_presel_CSVv2M"                  , { 'sampleList' : ["ZInv", "ZJets", "WJets", "DYJets" ,"ZZ", "WZ", "WW" ] ,  }   ),
                        #( "TTJets_2D_presel_CSVv2M"                 , { 'sampleList' : ["TTJets_LO" ]  ,                           }   ),
                        ( "WJets_HT_2D_presel_CSVv2M"                  , { 'sampleList' : ["ZInv", "ZJets", "WJets", "DYJets" ,"ZZ", "WZ", "WW" ] ,  }   ),
                        ( "TT_pow_2D_presel_CSVv2M"                    , { 'sampleList' : ["TT_pow" ]  ,                           }   ),
                        ( "TTJets_HT_2D_presel_CSVv2M"                 , { 'sampleList' : ["TTJets_LO" ]  ,                           }   ),


                        ( "T2tt_mWMin0p1_allDM_presel_CSVv2M"          , { 'sampleList' : ["SMS_T2tt_dM_10to80_genHT_160_genMET_80_mWMin_0p1"     , ],       'isFastSim':True      }   ),
                        ( "T2bW_mWMin0p1_allDM_presel_CSVv2M"          , { 'sampleList' : ["SMS_T2bW_X05_dM_10to80_genHT_160_genMET_80_mWMin_0p1" , ],       'isFastSim':True      }   ),
                        ( "T2tt_allDM_presel_CSVv2M"                   , { 'sampleList' : ["SMS_T2tt_dM_10to80_genHT_160_genMET_80"               , ],       'isFastSim':True                    }   ),
                       ]
        eff_to_use = "TTJets_HT_2D_presel_CSVv2M" #default
        isFastSim = False
        for eff_samp, info in eff_dict_map:
            if any([ samp in sampleName for samp in info['sampleList'] ]):
                eff_to_use = eff_samp
                isFastSim = info.get("isFastSim",False)
                break

        print "Decided to use %s for the jet efficiency for %s"%(eff_to_use, sampleName)
        if isFastSim: print "Including the FastSim/FullSim SF" 
        print info

        params['beff']={}

        #params['beff']['effFile']        = '$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/data/btagEfficiencyData/%s.pkl'%eff_to_use
        #params['beff']['sfFile']         = '$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/data/btagEfficiencyData/CSVv2_ichep.csv'
        #params['beff']['sfFile']         = '$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/data/btagEfficiencyData/CSVv2_4invfb_systJuly15.csv'
        params['beff']['sfFile_FastSim']  = '$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/data/btagEfficiencyData/CSV_13TEV_Combined_14_7_2016.csv'
        params['beff']['effFile']         = '$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/data/btagEfficiencyData/8025_mAODv2_v7/RunIISummer16MiniAODv2/%s.pkl'%eff_to_use
        params['beff']['sfFile']          = '$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/data/btagEfficiencyData/CSVv2_Moriond17_B_H.csv'
        #params['beff']['sfFile_FastSim']  = '$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/data/btagEfficiencyData/fastsim_csvv2_ttbar_26_1_2017.csv'
        params['beff']['btagEff']         = btagEfficiency( 
                                                            fastSim        = isFastSim,  
                                                            effFile        = params['beff']['effFile'], 
                                                            sfFile         = params['beff']['sfFile'], 
                                                            sfFile_FastSim =  params['beff']['sfFile_FastSim']  
                                                       )



    puWeightDict = params.get("puWeightDict")
    if puWeightDict:
        for pu, pu_dict in puWeightDict.iteritems():
            pu_var = pu_dict['var']
            pu_dict['pu_tfile'] = ROOT.TFile( pu_dict['pu_root_file'] ) 
            pu_dict['pu_thist'] = getattr( pu_dict['pu_tfile'], pu_dict['pu_hist_name'])

    ## setup hists for lepton sfs
    leptonSFsDict = params.get("leptonSFsDict")
    if leptonSFsDict:
        for sfname, sfdict in leptonSFsDict.items():
            if sfdict.get("hist_file"):
                sf_root_file = ROOT.TFile( os.path.expandvars( sfdict["hist_file"] ) )
                leptonSFsDict[sfname]['sf_root_file'] = sf_root_file
                leptonSFsDict[sfname]['sf_hist'] = getattr(sf_root_file, sfdict['hist_name'])
                #print sf_root_file
                #print leptonSFsDict[sfname]['sf_hist']        

    #
    return params

def get_logger(logLevel, logFile):
    ''' Logger for post-processing module.
    
    Use the basic definition of the logger from helpers.
    
    '''

    get_logger_rtuple = helpers.get_logger('cmgPostProcessing', logLevel, logFile)
    logger = get_logger_rtuple.logger
    numeric_level = get_logger_rtuple.numeric_level
    fileHandler = get_logger_rtuple.fileHandler

    cmgObjectSelection.logger.setLevel(numeric_level)
    cmgObjectSelection.logger.addHandler(fileHandler)

    return logger        

def getSamples(args):
    '''Return a list of components to be post-processed.
    
    No logger here, as the log file is determined with variables computed here.
    Simply exit if the required cmgTuples set or one of the samples do not exist, 
    printing the non-existing required set name.
    
    The sample processed will be written eventually in the logger,
    after a call to this function.
    
    Return also the output main directory, to be created eventually.
    '''

    cmgTuples = args.cmgTuples
    processSample = args.processSample
    
    targetDir = args.targetDir
    
    processingEra = args.processingEra
    cmgProcessingTag = args.cmgProcessingTag
    cmgPostProcessingTag = args.cmgPostProcessingTag
    parameterSet = args.parameterSet


    # cmg samples definition file
    cmgTuplesFullName = 'Workspace.DegenerateStopAnalysis.samples.cmgTuples.' + cmgTuples
    cmssw_base = os.environ['CMSSW_BASE']
    sampleFile = os.path.join(cmssw_base, 'src/Workspace/DegenerateStopAnalysis/python/samples/cmgTuples') + \
        '/' + cmgTuples + '.py'
    
    try:
        cmgSamples = importlib.import_module(cmgTuplesFullName)
    except ImportError, err:      
        print "\n The required set of CMG tuples \n cmgTuples: {0} \n ".format(cmgTuples) + \
            "with expected sample definition file \n {0} \n does not exist.".format(sampleFile), \
            "\n Correct the name and re-run the script. \n Exiting."
        sys.exit()


    if args.skimPreselect:
        outDir = os.path.join(
            targetDir, processingEra, cmgProcessingTag, cmgPostProcessingTag, parameterSet, 'step1',
            cmgTuples, args.skimGeneral, 'skimPreselect', args.skimLepton
            )
    else:
        outDir = os.path.join(
            targetDir, processingEra, cmgProcessingTag, cmgPostProcessingTag, parameterSet, 'step1',
            cmgTuples, args.skimGeneral, args.skimLepton
            )
    

    # samples
    
    allComponentsList = [] 
    
    processSampleList = [processSample]
    for sampleName in processSampleList:
        foundSample = False
        
        # cmgSamples.allComponents contains components or list of components  
        try:
            sampleRequested = getattr(cmgSamples, sampleName)
            
            if isinstance(sampleRequested, dict):
                # single component
                if (sampleName == sampleRequested['cmgName']):
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
            sampleRequested = cmgSamples.allComponents + cmgSamples.allSignals

            if isinstance(sampleRequested, dict):
                # single component
                if (sampleName == sampleRequested['cmgName']):
                    allComponentsList.append(sampleRequested)
                    foundSample = True
                    break            
            elif isinstance(sampleRequested, list):
                # list of components
                for comp in sampleRequested:
                    print "\n sampleRequested \n", (pprint.pformat(comp)), "\n"
                    if (sampleName == comp['cmgName']):
                        allComponentsList.append(comp)
                        foundSample = True
                        break 
            else:
                print "\n Not possible to build list of components for {0}".format(sampleName), \
                "\n Exiting."
                sys.exit()
                
                
        
        if not foundSample:
            print "\n List of available samples in cmgTuples set {0}: \n {1} \n".format(
                cmgTuples, pprint.pformat(cmgSamples.allComponents)
                )
            print "\n List of available signal samples in cmgTuples set {0}: \n {1} \n".format(
                cmgTuples, pprint.pformat(cmgSamples.allSignals)
                )
                    
            print "\n Requested sample {0} not available in CMG samples.".format(sampleName), \
                "\n Re-run the job with existing samples.", \
                "\n Exiting."
            sys.exit() 
    
    # define the named tuple to return the values
    rtuple = collections.namedtuple(
        'rtuple', 
        [
            'sampleFile',
            'cmgSamples',
            'componentList', 
            'outputDirectory', 
            ]
        )
    
    getSample_rtuple = rtuple(sampleFile, cmgSamples, allComponentsList, outDir) 
    
    #    
    return getSample_rtuple
    

def eventsSkimPreselect(skimGeneral, skimLepton, skimPreselectFlag, params, skimSignalMasses=[]):
    '''Define the skim condition, including preselection if required.
    
    The skim condition depends on the general skim name, the lepton skim selection, and on the
    event preselection. 
    
    '''

    logger = logging.getLogger('cmgPostProcessing.eventsSkimPreselect')
    
    #
    SkimParameters = params['SkimParameters']
    
    lheHThighIncoming = SkimParameters['lheHThigh']['lheHTIncoming']
    lheHTlowIncoming = SkimParameters['lheHTlow']['lheHTIncoming']
    
    skimCond = "(1)"
    
    if not skimGeneral:
        pass
    elif skimGeneral.startswith('met'):
        skimCond = "met_pt>" + str(float(skimGeneral[3:]))
    elif skimGeneral == 'lheHThigh': 
        skimCond += "&&(lheHTIncoming>={0})".format(lheHThighIncoming)
    elif skimGeneral == 'lheHTlow': 
        skimCond += "&&(lheHTIncoming<{0})".format(lheHTlowIncoming)
    else:
        raise Exception("Skim Condition not recognized: %s"%skimGeneral)
        pass
    
    # lepton skimming, loop only over events fulfilling the lepton skimming condition 
    skimLeptonCondition = SkimParameters['skimLepton']
    if skimLeptonCondition:
        skimCond += "&&%s"%skimLeptonCondition
    
    logger.info(
        "\n Jobs running with \n skimGeneral = '%s' \n skimLepton = '%s' \n Skimming condition: \n  %s \n ", 
        skimGeneral, skimLepton,
        skimCond)
    
    if skimPreselectFlag:
        skimPreselectionCuts = SkimParameters['skimPreselect']
        skimCond += "&&%s"%skimPreselectionCuts

        logger.info("\n Applying preselection cuts for skimming: %s ", skimPreselectionCuts)
        logger.info("\n Skimming condition with preselection: \n  %s \n", skimCond)
    else:
        logger.info("\n No preselection cuts are applied for skim %s \n Skimming condition unchanged \n", skimGeneral)
        pass

    if skimSignalMasses:
        massVar1 , mass1 = skimSignalMasses[0]
        massVar2 , mass2  = skimSignalMasses[1]
        #skimCond +="&& (GenSusyMStop==%s && GenSusyMNeutralino==%s)"%(mstop,mass2)
        skimCond +="&& ({massVar1}=={mass1} && {massVar2}=={mass2})".format(massVar1 = massVar1, massVar2=massVar2, mass1=mass1, mass2=mass2)
        logger.info("\n Processing Signal Scan for %s:%s  %s: %s "%(massVar1, mass1, massVar2, mass2 ))

    #
    return skimCond


def indexObjNames(obj_selector):

    branchPrefix = obj_selector['branchPrefix']
    object = obj_selector['object']
    selectorId = obj_selector['selectorId']

    nObjName = ''.join(['n', branchPrefix, '_', object, '_', selectorId])

    prefixToAdd = ''.join(['Index', branchPrefix])
    indexName = ''.join(
        [prefixToAdd, '_', object, '_', selectorId]
    )

    varToAdd = ''.join([object, '_', selectorId])

    rtuple = collections.namedtuple(
        'rtuple',
        [
            'nObjName',
            'prefix',
            'indexName',
            'var',
        ]
    )

    my_rtuple = rtuple(
        nObjName,
        prefixToAdd,
        indexName,
        varToAdd
    )
    #
    return my_rtuple
   

    
 
def rwTreeClasses(sample, isample, args, temporaryDir, varsNameTypeTreeLep, params={} ):
    '''Define the read / write tree classes for data and MC.
    
    '''
    logger = logging.getLogger('cmgPostProcessing.rwTreeClasses')

    # get the variables defined in the parameter file
    treeVariables_params = params['treeVariables']

    # sum up branches to be defined for each sample, depending on the sample
    # type (data or MC)

    readVariables = []
    newVariables = []

    readVectors = []
    newVectors = []
            
    #
    # add variables to extend existing collections

    def appendExtendQuantities(obj_collection, new_vectors):
        ''' Add new variables, extending existing object collections (e.g. LepGood, Jet, etc).
                        '''

        extendVariables   = obj_collection.get( 'extendVariables' )
        if not extendVariables:
            return []
        collection_prefix = obj_collection['branchPrefix']

        varList = []
        for var in extendVariables:

            if var.get("drop_branch"):
                continue
            var_name = var['var']
            varList.append(var_name)


        new_vec = {
            'prefix': collection_prefix,
            'nMax': obj_collection['nMax'],
            'size': { ''.join([collection_prefix, '_', helpers.getVariableName(var_name)]): 'n' + collection_prefix for var_name in varList } ,
            'vars': varList,
        }

        logger.trace(
            "\n Extend collection {collection_prefix} with variables {extendVariables}: \n new vector {new_vec} \n".format(
                collection_prefix=collection_prefix, extendVariables=extendVariables, new_vec=new_vec)
        )

        new_vectors.extend([new_vec])

        #
        return new_vectors

    extendCollectionList = params.get('extendCollectionList', [] )

    for obj_collection in extendCollectionList:
        
        collection_prefix = obj_collection['branchPrefix']
        extendVariables =  obj_collection['extendVariables']
        
        logger.trace(
            "\n Extend collection {collection_prefix} with variables {extendVariables}: \n".format(
                collection_prefix=collection_prefix, extendVariables=extendVariables)
        )

        collection_sampleType = obj_collection['sampleType']

        if (
            (('data' in collection_sampleType) and sample['isData'])
            or
            (('mc' in collection_sampleType)
             and (not sample['isData']))
        ):

            appendExtendQuantities(
                obj_collection, newVectors
            )

    # add variables and vectors from the selectors

    def appendNewQuantities(
            nObjName, prefixToAdd, indexName, varInIndex, nMax,
            computeVars, computeVectors,
            new_variables, new_vectors):
        ''' Append variable and vectors defined in each selector. 

                '''

        varToAdd = ''.join([varInIndex, '/I/-1'])

        if nObjName not in new_variables:
            new_variables.extend([
                ''.join([nObjName, '/I/-1'])
            ])
            logger.trace("\n Add variable: \n %s \n", nObjName)
        else:
            raise Exception(
                '\n Multiple definition of variable {var}.'.format(var=nObjName))
            sys.exit()

        for var in computeVars:
            if var not in new_variables:
                new_variables.append(var)
                logger.trace("\n Add variable: \n %s \n", var)
            else:
                raise Exception(
                    '\n Multiple definition of variable {var}.'.format(var=var))
                sys.exit()
            

        # FIXME add computeVectors
        
        prefixFound = False

        for vec in new_vectors:

            if prefixToAdd == vec['prefix']:
                prefixFound = True
                logger.trace(
                    "\n Found prefix: \n %s \n", pprint.pformat(prefixToAdd))

                if nMax != vec['nMax']:
                    raise Exception(
                        ''.join([
                            '\n nMax from selector for {indexName}  = {nMax}',
                            ' different from nMax = {nMaxEx} for existing prefix'
                        ]).format(
                            indexName=indexName, nMax=nMax, nMaxEx=vec[
                                'nMax']
                        )
                    )
                    sys.exit()

                if varToAdd not in vec['vars']:
                    vec['vars'].append(varToAdd)
                    vec['size'].update({indexName:nObjName})
                    logger.trace(
                        "\n Add variable: \n %s \n to vector \n %s \n", varToAdd, vec)
                else:
                    raise Exception(
                        '\n Multiple definition of variable {var}.'.format(var=varToAdd))
                    sys.exit()

        if not prefixFound:
            new_vec = {'prefix': prefixToAdd, 'nMax': nMax, 'size': {indexName:nObjName},
                       'vars': [varToAdd]
                       }
            logger.trace(
                "\n Append new vector: \n %s \n", pprint.pformat(new_vec))

            new_vectors.extend([new_vec])

    def appendReadQuantities(branchPrefix, nObjName, branchesToRead, nMax, read_variables, read_vectors):
        ''' Append variable and vectors defined in each selector. 

        '''

        if nObjName not in read_variables:
            read_variables.extend([nObjName])
            logger.trace("\n Add variable: \n %s \n", nObjName)

        prefixFound = False

        for vec in read_vectors:

            if branchPrefix == vec['prefix']:
                prefixFound = True
                logger.trace(
                    "\n Found prefix: \n %s \n", pprint.pformat(branchPrefix))

                if nMax != vec['nMax']:
                    raise Exception(
                        ''.join([
                            '\n nMax from selector for {indexName}  = {nMax}',
                            ' different from nMax = {nMaxEx} for existing prefix'
                        ]).format(
                            indexName=indexName, nMax=nMax, nMaxEx=vec[
                                'nMax']
                        )
                    )
                    sys.exit()

                for var in branchesToRead:

                    if var not in vec['vars']:
                        vec['vars'].append(var)
                        logger.trace(
                            "\n Add variable: \n %s \n to vector \n %s \n", var, vec)
                    else:
                        logger.trace(
                            "\n Variable: \n %s \n already in vector \n %s \n", var, vec)

        if not prefixFound:
            new_vec = {'prefix': branchPrefix, 'nMax': nMax, 'size': nObjName,
                       'vars': branchesToRead
                       }
            logger.trace(
                "\n Append new vector: \n %s \n", pprint.pformat(new_vec))

            read_vectors.extend([new_vec])

    def appendSelectorQuantities(obj_selector, read_variables, new_variables, read_vectors, new_vectors):
        ''' Append variable and vectors defined in each selector. 

                    '''

        branchPrefix = obj_selector['branchPrefix']
        object = obj_selector['object']
        selectorId = obj_selector['selectorId']

        branchesToRead = obj_selector['branchesToRead']
        nMax = obj_selector['nMax']

        nObjNameColl = ''.join(['n', branchPrefix, '/I'])

        index_rtuple = indexObjNames(obj_selector)

        nObjName = index_rtuple.nObjName
        indexName = index_rtuple.indexName
        prefixToAdd = index_rtuple.prefix
        varInIndex = index_rtuple.var

        # read computeVariables, change their name to make them selector dependent, and save the names
        # to a dictionary key

        computeVariables = obj_selector.get('computeVariables', None)

        # lists to collect the computeVariables (simple variables or array)
        computeVectors = []
        computeVars = []

        if computeVariables is None:
            logger.trace(
                '\n No computeVariables defined for {indexName} \n'.format(
                    indexName=indexName
                )
            )
        else:
            computeVariablesList = computeVariables['variableList']
            computeVariablesName = []
            for var in computeVariablesList:
                var_name = helpers.getVariableName(var)
                var_size = helpers.getVariableSize(var)
                var_type = helpers.getVariableType(var)

                var_initializer = helpers.getVariableInitializer(var)
                # do not accept variables without initializer
                if var_initializer is None:
                    raise Exception(
                        ''.join([
                                "\n Variable [var] has no initializer defined.\n".format(
                                    var=var),
                                "\n Define variable in the format 'name[size]/type/initializer' or 'name/type/initializer'"
                                ])
                    )
                    sys.exit()

                # change name
                new_name = ''.join([var_name, '_', object, '_', selectorId])

                if var_size > 1:
                    new_var = ''.join(
                        [new_name, '[', str(var_size), ']', '/', var_type, '/', str(var_initializer)])
                    computeVectors.append(new_var)
                else:
                    new_var = ''.join(
                        [new_name, '/', var_type, '/', str(var_initializer)])
                    computeVars.append(new_var)

                computeVariablesName.append(new_name)

            computeVariables['computeVariablesName'] = computeVariablesName
            obj_selector['computeVariables'] = computeVariables

        appendReadQuantities(
            branchPrefix, nObjNameColl, branchesToRead, nMax,
            read_variables, read_vectors)
        appendNewQuantities(
            nObjName, prefixToAdd, indexName, varInIndex, nMax,
            computeVars, computeVectors,
            new_variables, new_vectors)

    selectorList = params['selectorList']

    for obj_selector in selectorList:

        logger.trace(
            "\n Append variables and vectors for selector: \n %s \n", pprint.pformat(
                obj_selector)
        )

        selector_sampleType = obj_selector['sampleType']

        if (
            (('data' in selector_sampleType) and sample['isData'])
            or
            (('mc' in selector_sampleType) and (not sample['isData']))
        ):

            appendSelectorQuantities(
                obj_selector,
                readVariables, newVariables,
                readVectors, newVectors
            )
            
    mergeLeptonSelectors = params['mergeLeptonSelectors']

    for sels in mergeLeptonSelectors:
        muSelector = sels[0]
        elSelector = sels[1]

        index_rtuple_mu = indexObjNames(muSelector)
        index_rtuple_el = indexObjNames(elSelector)

        nObjName = index_rtuple_mu.nObjName.replace('_mu_', '_lep_')
        prefixToAdd = index_rtuple_mu.prefix
        indexName = index_rtuple_mu.indexName.replace('_mu_', '_lep_')
        varInIndex = index_rtuple_mu.var.replace('mu_', 'lep_')

        nMax = muSelector['nMax']

        # dummy lists to match appendNewQuantities calls
        computeVectors = []
        computeVars = []

        selector_sampleType = muSelector['sampleType']

        if (
            (('data' in selector_sampleType) and sample['isData'])
            or
            (('mc' in selector_sampleType) and (not sample['isData']))
        ):
            appendNewQuantities(
                nObjName, prefixToAdd, indexName, varInIndex, nMax,
                computeVars, computeVectors,
                newVariables, newVectors
            )


    # create the variables for btag weights
    # FIXME the addition of manually entered bTagWeightVars is not checked for
    # consistency
    if args.processBTagWeights:
        
        BTagWeights_conf_names = params['BTagWeights_conf_names']


        for conf_name in BTagWeights_conf_names:

            BTagWeights_conf = params[conf_name]
            
            bTagNames = BTagWeights_conf['bTagNames']
            bTagWeightNames = BTagWeights_conf['bTagWeightNames']
            maxMultBTagWeight = BTagWeights_conf['maxMultBTagWeight']

            bTagWeightVars = []
            for bTagName in bTagNames:
                jetSelectorId = BTagWeights_conf['jetSelectorId']
                for var in bTagWeightNames:
                    varName = "_%s_%s" % (var, jetSelectorId)
                    if var != 'MC':
                        bTagWeightVars.append(
                            "weight1a%s%s/F" % (bTagName, varName))
                    for nB in range(maxMultBTagWeight + 1):
                        bTagWeightVars.append(
                            "weight%s%s%s/F" % (bTagName, nB, varName))
                        if nB > 0:
                            bTagWeightVars.append(
                                "weight%s%sp%s/F" % (bTagName, nB, varName))
            bTagWeightVars.sort()
            
            newVariables.extend(bTagWeightVars)

    # sum up branches to be defined for each sample, depending on the sample
    # type (data or MC)
    # FIXME the addition of manually entered quantities is not checked for consistency

    readVariables.extend(treeVariables_params.readVariables_DATAMC)
    readVectors.extend(treeVariables_params.readVectors_DATAMC)
    
    newVariables.extend(treeVariables_params.newVariables_DATAMC)
    newVectors.extend(treeVariables_params.newVectors_DATAMC)
   
    if sample['isData']:
        keepBranches = treeVariables_params.keepBranches_DATAMC + treeVariables_params.keepBranches_DATA
        dropBranches = treeVariables_params.dropBranches_DATAMC + treeVariables_params.dropBranches_DATA

        aliases = treeVariables_params.aliases_DATAMC + treeVariables_params.aliases_DATA

        readVariables.extend(treeVariables_params.readVariables_DATA)        
        readVectors.extend(treeVariables_params.readVectors_DATA)
        
        newVariables.extend(treeVariables_params.newVariables_DATA)        
        newVectors.extend(treeVariables_params.newVectors_DATA)
    else:
        keepBranches = treeVariables_params.keepBranches_DATAMC + treeVariables_params.keepBranches_MC
        dropBranches = treeVariables_params.dropBranches_DATAMC + treeVariables_params.dropBranches_MC
        aliases = treeVariables_params.aliases_DATAMC + treeVariables_params.aliases_MC

        readVariables.extend(treeVariables_params.readVariables_MC)        
        readVectors.extend(treeVariables_params.readVectors_MC)
        
        newVariables.extend(treeVariables_params.newVariables_MC)        
        newVectors.extend(treeVariables_params.newVectors_MC)

    readVars = [convertHelpers.readVar(v, allowRenaming=False, isWritten=False, isRead=True) for v in readVariables]
    newVars = [convertHelpers.readVar(v, allowRenaming=False, isWritten = True, isRead=False) for v in newVariables]
  
    for v in readVectors:
        v['vars'] = [convertHelpers.readVar(
            v['prefix']+'_'+vvar, allowRenaming=False, isWritten=False, isRead=True) for vvar in v['vars']
            ]


    for v in newVectors:
        v['vars'] = [convertHelpers.readVar(
            v['prefix']+'_'+vvar, allowRenaming=False, isWritten=True, isRead=False
            ) for vvar in v['vars']
            ]

    logger.debug("\n keepBranches definition: \n %s \n", pprint.pformat(keepBranches))
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

    # define the named tuple to return the values
    rtuple = collections.namedtuple(
        'rtuple', 
        [
            'keepBranches', 
            'dropBranches',
            'readVars', 
            'aliases', 
            'readVectors',
            'newVars',
            'newVectors',
            'readTree',
            'saveTree',
            ]
        )
    
    rwTreeClasses_rtuple = rtuple(
        keepBranches, 
        dropBranches,
        readVars, 
        aliases, 
        readVectors, 
        newVars, 
        newVectors, 
        readTree, 
        saveTree
        )
    #    
    return rwTreeClasses_rtuple
   
   
def getTreeFromChunk(c, skimCond, iSplit, nSplit):
    '''Get a tree from a chunk.
    
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


def getRunLumiEvt(splitTree, saveTree):
    
    run = int(splitTree.GetLeaf('run').GetValue())
    lumi = int(splitTree.GetLeaf('lumi').GetValue())
    evt = int(splitTree.GetLeaf('evt').GetValue())

    run_lumi_evt = "%s:%s:%s\n" % (run, lumi, evt)
    
    saveTree.run_lumi_evt = run_lumi_evt
    
    # 
    return saveTree


def getListFromSaveTree(saveTree, listName):
    '''Get a list from saveTree.

    TODO a more decent way to retrieve the list of indices?
    '''

    logger = logging.getLogger('cmgPostProcessing.getListFromSaveTree')

    if listName is not None:
        savedList = []
        list_ptr = getattr(saveTree, listName)
        for i in range(len(list_ptr)):
            idx = list_ptr[i]
            if idx >= 0:
                savedList.append(idx)

    else:
        savedList = None

    logger.debug(
        '\n {name} list retrieved from saveTree \n {indexList} \n'.format(
            name=listName,
            indexList=pprint.pformat(savedList)
        )
    )

    #
    return savedList


def evaluateExtenders(readTree, splitTree, saveTree, params, isDataSample, eval_begin, extendVariablesFunctions):
    '''Evaluate all extenders defined in the parameter file. 

    '''

    logger = logging.getLogger('cmgPostProcessing.evaluateExtenders')

    extenderList = params.get('extendCollectionList',[])

    for obj_extender in extenderList:

        # evaluate the extender only on sample type it was requested for

        extender_sampleType = obj_extender['sampleType']
        if isDataSample and (not ('data' in extender_sampleType)):
            continue
        if (not isDataSample) and (not ('mc' in extender_sampleType)):
            continue

        branchPrefix = obj_extender['branchPrefix']
        extendVariables = obj_extender['extendVariables']

        # call the corresponding functions

        for var in extendVariables:

            if var['eval_begin'] != eval_begin:
                continue

            var_function = var['function']
            var_args = var['args']
            if var_function in extendVariablesFunctions:
                extendVariablesFunctions[var_function](
                    args, readTree, splitTree, saveTree, params, var, var_args)
            else:
                logger.warning(
                    ''.join([
                        '\n No implementation available for {func} required by variable {var}.'.format(
                            func=var_function, var=var['var']),
                        '\n Skipping evaluation of this variable.'
                    ])

                )

                continue

    return saveTree


def evaluateSelectors(readTree, splitTree, saveTree, params, isDataSample):
    '''Evaluate all selectors defined in the parameter file. 

    For each selector, produce the index array Index{branchPrefix}_{obj}_{selectorId} 
    and the number of objects in the selected list n{Object}
    '''

    logger = logging.getLogger('cmgPostProcessing.evaluateSelectors')

    selectorList = params['selectorList']

    for obj_selector in selectorList:
        
        # evaluate the selector only on sample type it was requested for
        
        selector_sampleType = obj_selector['sampleType']
        if isDataSample and (not ('data' in selector_sampleType)):
            continue
        if (not isDataSample) and (not ('mc' in selector_sampleType)):
            continue

        #
        
        branchPrefix = obj_selector['branchPrefix']
        object = obj_selector['object']
        selectorId = obj_selector['selectorId']
        
        branchesToRead = obj_selector['branchesToRead']
        branchesToPrint = obj_selector['branchesToPrint']

        # get from saveTree the actual list for inputIndexList_str, if not None
        # TODO a more decent way to retrieve the list of indices?

        inputIndexList_str = obj_selector['inputIndexList']

        if inputIndexList_str is not None:
            inputIndexList =[]
            inputIndexList_ptr = getattr(saveTree, inputIndexList_str)
            for i in range(len(inputIndexList_ptr)):
                idx = inputIndexList_ptr[i]
                if idx >= 0:
                    inputIndexList.append(idx)
            
        else:
            inputIndexList = None

        logger.debug(
            '\n Input list of object indices for selector {prefix}_{obj}_{name} \n {indexList} \n'.format(
                prefix=branchPrefix, obj=object, name=selectorId,
                indexList=pprint.pformat(inputIndexList)
            )
        )
        
        #
        
        cmgObj = cmgObjectSelection.cmgObject(
            readTree, splitTree, branchPrefix)

        if logger.isEnabledFor(logging.DEBUG):
            printStr = ''.join([
                '\n List of ',
                branchPrefix,
                ' ',
                object, ' before selector: ',
                cmgObj.printObjects(inputIndexList, branchesToPrint)
            ])
            logger.debug(printStr)

        #
        selector_expression = obj_selector['selector']
        selector_function = cmgObjectSelection.objSelectorFunc(
            selector_expression)
        objList = cmgObj.selectionIndexList(
            readTree, selector_function, inputIndexList)

        index_rtuple = indexObjNames(obj_selector)
        nObjName = index_rtuple.nObjName
        indexName = index_rtuple.indexName
        
        # check if sorting after another variable is requested
        # if requested, sort and replace the original list with the sorted list 
        
        sortVariable = obj_selector.get('sort', None)

        if sortVariable is not None:
            sortedList = cmgObj.sort(sortVariable, objList)
            objList = sortedList

        setattr(saveTree, nObjName, len(objList))
        for idx, val in enumerate(objList):
            var = getattr(saveTree, indexName)
            var[idx] = val

        if logger.isEnabledFor(logging.DEBUG):
            printStr = ''.join([
                '\n ',
                branchPrefix,
                ' ',
                object, ' selector \n\n',
                cmgObj.printObjects(objList, branchesToPrint),
                '\n',
                'saveTree.', nObjName, ' = %i',
                '\n ', indexName, ': ', pprint.pformat(objList),
                '\n'
            ])
            logger.debug(printStr, getattr(saveTree, nObjName))

    return saveTree


def computeVariablesSelectors(readTree, splitTree, saveTree, params, isDataSample, computeVariablesFunctions):
    '''Evaluate 'computeVariables' for all selectors.

    The variables depend only on the selector indices and on quantities 
    already existing in the tree.

    '''

    logger = logging.getLogger('cmgPostProcessing.computeVariablesSelectors')

    selectorList = params['selectorList']

    for obj_selector in selectorList:

        # evaluate the selector only on sample type it was requested for
        
        selector_sampleType = obj_selector['sampleType']
        if isDataSample and (not ('data' in selector_sampleType)):
            continue
        if (not isDataSample) and (not ('mc' in selector_sampleType)):
            continue

        branchPrefix = obj_selector['branchPrefix']
        object = obj_selector['object']
        selectorId = obj_selector['selectorId']

        index_rtuple = indexObjNames(obj_selector)
        index_name = index_rtuple.indexName

        computeVariables = obj_selector.get('computeVariables', None)
        if computeVariables is None:
            logger.trace(
                '\n No computeVariables defined for {index_name} \n'.format(
                    index_name=index_name
                )
            )

            continue

        # get from saveTree the actual list of indices for the selector and the
        # collection objects from the readTree

        indexList = getListFromSaveTree(saveTree, index_name)

        if indexList is None:
            logger.warning(
                '\n List of object indices {index_name} is None. \n Skipping computeVariables\n'.format(
                    index_name=index_name
                )
            )

            continue

        cmgObj = cmgObjectSelection.cmgObject(
            readTree, splitTree, branchPrefix)

        # call the corresponding function

        vars_function = computeVariables['function']
        if vars_function in computeVariablesFunctions:
            computeVariablesFunctions[vars_function](
                args, readTree, splitTree, saveTree, params, computeVariables, cmgObj, indexList)
        else:
            logger.warning(
                '\n No implementation available for {func}. \n Skipping computeVariables for {index_name}\n'.format(
                    func=vars_function, index_name=index_name
                )
            )

            continue

    return saveTree


# some auxiliary functions, identical for mu, el, lep 

def saveTreeLepObject(saveTree, LepColl, objName, objList):
    ''' Save number of selected lepton objects and their indices.

    '''
    setattr(saveTree, 'n' + LepColl + '_' + objName, len(objList))
    for idx, val in enumerate(objList):
        var = getattr(saveTree, 'Index' + LepColl + '_' + objName)
        var[idx] = val
        
    return saveTree


def mergeLeptons(readTree, splitTree, saveTree, params):
    '''Merge muons and electrons for a muon and an electron selectors. 

    The two selectors must have the same branchPrefix and the same selectorId.
    '''

    logger = logging.getLogger('cmgPostProcessing.mergeLeptons')

    mergeLeptonSelectors = params['mergeLeptonSelectors']

    for sels in mergeLeptonSelectors:
        muSelector = sels[0]
        elSelector = sels[1]

        index_rtuple_mu = indexObjNames(muSelector)
        muListName = index_rtuple_mu.indexName

        index_rtuple_el = indexObjNames(elSelector)
        elListName = index_rtuple_el.indexName

        nObjName = index_rtuple_mu.nObjName.replace('_mu_', '_lep_')
        indexName = index_rtuple_mu.indexName.replace('_mu_', '_lep_')

        lepColl = muSelector['branchPrefix']

        muList = getListFromSaveTree(saveTree, muListName)
        elList = getListFromSaveTree(saveTree, elListName)
        #
        sumElMuList = muList + elList

        lepObj = cmgObjectSelection.cmgObject(readTree, splitTree, lepColl)

        lepList = lepObj.sort('pt', sumElMuList)

        # save number of selected objects and their indices

        setattr(saveTree, nObjName, len(lepList))
        for idx, val in enumerate(lepList):
            var = getattr(saveTree, indexName)
            var[idx] = val

        if logger.isEnabledFor(logging.DEBUG):
            printStr = ''.join([
                '\n ',
                lepColl,
                ' ',
                ' lep ', ' selector \n\n',
                lepObj.printObjects(lepList, muSelector['branchesToPrint']),
                '\n',
                'saveTree.', nObjName, ' = %i',
                '\n ', indexName, ': ', pprint.pformat(lepList),
                '\n'
            ])
            logger.debug(printStr, getattr(saveTree, nObjName))

    return saveTree

def extend_LepGood_func(args, readTree, splitTree, saveTree, params, extend_var, var_args):
    '''Extend LepGood collection. 

    Compute quantities required to extend the LepGood collection
    '''

    #
    logger = logging.getLogger('cmgPostProcessing.extend_LepGood_func')
    debug_log = logger.isEnabledFor(logging.DEBUG)
    
    # get the LepGood collection
    branchPrefix = 'LepGood'
    lepObj = cmgObjectSelection.cmgObject(readTree, splitTree, branchPrefix)

    if not lepObj.nObj:
        return saveTree

    var_name    = helpers.getVariableName(extend_var['var'])    
    branch_name = ''.join([branchPrefix, '_', var_name])

    if 'sf' in var_name:
        leptonSFsDict = params.get("leptonSFsDict")
        if not leptonSFsDict:
            return saveTree

        sfs_to_get  = [ sf_name for sf_name in leptonSFsDict if leptonSFsDict[sf_name].has_key("hist_file") ]
        sf          = var_name #[ sf_name for sf_name in leptonSFsDict if leptonSFsDict.has_key("merge_sfs") ] 
        if not sfs_to_get:
            raise Exception("Expected only 1 sf... but got these instead sfs_to_get: %s,  sf_to_merge %s"%(sfs_to_get, sf))
        #else:
        #    sf_to_merge = sf_to_merge[0]
        
        leptonSFs={}
        minPtEl = 5
        minPtMu = 3.5
        for sf_name in sfs_to_get:
            sfdict        =   leptonSFsDict[sf_name]
            sf_hist       =   sfdict['sf_hist']
            maxPt         =   sfdict['maxPt'] 
            maxEta        =   sfdict['maxEta'] 
            requirement   =   sfdict['requirement']

            leptonSFs[sf_name]=[0]*lepObj.nObj
            for idx in range(lepObj.nObj):
                if requirement( lepObj, idx ):
                    minPt = minPtMu if abs( lepObj.pdgId[idx] ) == minPtMu else minPtEl
                    sf = getLeptonSF( lepObj.pt[idx], lepObj.eta[idx], sf_hist , maxPt = maxPt , maxEta = maxEta, minPt=minPt)            
                else:
                    sf = 1.0
                 
                leptonSFs[sf_name][idx]=sf    
                
                printStr = [ "SF:", idx, lepObj.nObj, lepObj.pt[idx], lepObj.eta[idx], lepObj.pdgId[idx], sf ]
                printStr = [ str(s) for s in printStr ]
                if debug_log: logger.debug(' '.join(printStr))
        
        var = getattr( saveTree, branch_name)
        for idx in range(lepObj.nObj):
            sfs        = [ leptonSFs[var_name][idx] for var_name in sfs_to_get ] 
            assert not [x for x in sfs if x in [0, -999, None] ]
            mergedSF = functools.reduce( operator.mul , sfs) 
            var[idx]   = mergedSF

            printStr = ["MERGED SF:", branch_name, idx, lepObj.nObj, lepObj.pt[idx], lepObj.eta[idx], lepObj.pdgId[idx], mergedSF]
            printStr = [str(s) for s in printStr]
            if debug_log: logger.debug(' '.join(printStr))
        


        areYouCrazy = False
        if areYouCrazy:
            addLeptonSF     = False
            mergeLeptonSFs  = False
            
            if var_name in leptonSFsDict:
                #leptonSFs[var_name] = [ 0 for idx in range(lepObj.nObj) ]
                sfdict        = leptonSFsDict[var_name]
                if sfdict.get("merge_sfs"):
                    mergeLeptonSFs= True
                else:
                    addLeptonSF = True
   

            if extend_var.get("drop_branch"):
                setattr( saveTree, branch_name, [0]*lepObj.nObj ) ## latch a list onto the tree since this branch won't be written
            var = getattr( saveTree, branch_name)

            minPtEl = 5
            minPtMu = 3.5

            if addLeptonSF:
                sf_hist       =   sfdict['sf_hist']
                maxPt         =   sfdict['maxPt'] 
                maxEta        =   sfdict['maxEta'] 
                requirement   =   sfdict['requirement']

                for idx in range(lepObj.nObj):
                    
                    if requirement( lepObj, idx ):
                        minPt = minPtMu if abs( lepObj.pdgId[idx] ) == minPtMu else minPtEl
                        #sf = getLeptonSF( lepObj.pt[idx], lepObj.eta[idx], sf_hist , maxPt = maxPt , maxEta = maxEta, minPt=10 )            
                        sf = getLeptonSF( lepObj.pt[idx], lepObj.eta[idx], sf_hist , maxPt = maxPt , maxEta = maxEta, minPt=minPt)            
                    else:
                        sf = 1.0
                     
                    var[idx] = sf
                    #leptonSFs[var_name][idx]=sf    
                    
                    printStr = [ "SF:", idx, lepObj.nObj, lepObj.pt[idx], lepObj.eta[idx], lepObj.pdgId[idx], sf ]
                    printStr = [ str(s) for s in printStr ]
                    if debug_log: logger.debug(' '.join(printStr))

            elif mergeLeptonSFs:
                sfs_to_merge = sfdict['merge_sfs']
                for idx in range(lepObj.nObj):
                    sfs      = [ getattr(saveTree, lepObj.obj + "_" +sf_name)[idx] for sf_name in sfs_to_merge ] 
                    assert not [x for x in sfs if x in [0, -999, None] ]
                    
                    mergedSF = functools.reduce( operator.mul , sfs) 
                    
                    var[idx] = mergedSF
                    printStr = ["MERGED SF:", branch_name, idx, lepObj.nObj, lepObj.pt[idx], lepObj.eta[idx], lepObj.pdgId[idx], mergedSF]
                    printStr = [str(s) for s in printStr]
                    if debug_log: logger.debug(' '.join(printStr))

    
    # calculation of Wpt
    if var_name == "Wpt": 
        for idx in range(lepObj.nObj):
            var = getattr(saveTree, branch_name)
            var[idx] = processWpt(readTree, splitTree, params, lepObj.pdgId[idx], lepObj.pt[idx], lepObj.eta[idx], lepObj.phi[idx]) 
    
    # determination of isFakeFromTau
    if var_name == "isFakeFromTau": 
        for idx in range(lepObj.nObj):
            if not (lepObj.mcMatchId[idx] == 0 or lepObj.mcMatchId[idx] == 99 or lepObj.mcMatchId[idx] == 100): continue # selecting fakes only 
            var = getattr(saveTree, branch_name)
            var[idx] = processFakesFromTaus(readTree, splitTree, params, var_args['dRcut'], lepObj.eta[idx], lepObj.phi[idx]) 
 
 
    if debug_log:
        printStr = ["\n Quantities computed in extend_LepGood_func"]
        for idx in range(lepObj.nObj):
            printStr.append('\n saveTree.')
            printStr.append(branch_name)
            printStr.append('[')
            printStr.append(str(idx))
            printStr.append(']')
            printStr.append(' = ')
            printStr.append(str(getattr(saveTree, branch_name, )[idx]))
        printStr.append('\n')
        logger.debug(''.join(printStr))
    return saveTree
    
    
def getLeptonSF( lepPt, lepEta, sf_hist, maxPt = None, maxEta = None , minPt = None, def_val = 1):
    lepEta_ = abs(lepEta)
    if minPt and lepPt < minPt:
        lepPt_  = minPt
    elif maxPt and lepPt > maxPt:
        lepPt_  = maxPt*0.99
    else:
        lepPt_  = lepPt

    if maxEta and lepEta_ > maxEta:
        lepEta_ = maxEta*0.99
    else:
        lepEta_ = lepEta_

    if type(sf_hist) in [ ROOT.TH1D, ROOT.TH1F ] :
        b   = sf_hist.FindBin(lepPt_)
    elif type(sf_hist) in [ROOT.TH2D , ROOT.TH2F]:
        b   = sf_hist.FindBin(lepPt_,lepEta_)

    sf  = sf_hist.GetBinContent(b)
    if not sf:
        sf_hist.Print("all")
        assert False
    return sf


def processWpt(readTree, splitTree, params, recoLep_pdgId, recoLep_pt, recoLep_eta, recoLep_phi):
    ''' Calculates Wpt based on reco quantities. Wpt = lepPt + MET
        NOTE: No selection on recoLep requiring that it comes from a W (motherId = +-24) applied. It can be done before calling the function.
    '''

    logger = logging.getLogger('cmgPostProcessing.processWpt')

    # Missing Transverse Energy Vector 
    #met = hephyHelpers.getObjDict(splitTree, "met_", ['pt', 'phi'], 0)
    met_pt =  readTree.met_pt
    met_phi = readTree.met_phi

    MET = ROOT.TLorentzVector()
    MET.SetPtEtaPhiM(met_pt, 0, met_phi, 0)
  
    W = ROOT.TLorentzVector()
    W.SetPtEtaPhiM(recoLep_pt, recoLep_eta, recoLep_phi, 0) # setting lepton quantities
    
    W+=MET # adding MET to the lepton pT = Wpt

    Wpt = W.Pt()

    ##Alternatives:
    #Wpt = math.sqrt((recoLep_pt*math.cos(recoLep_phi) + met_pt*math.cos(met_phi))**2 + (recoLep_pt*math.sin(recoLep_phi) + met_pt*math.sin(met_phi))**2)
    #Wpt = math.sqrt(recoLep_pt*recoLep_pt + met_pt*met_pt + 2*met_pt*recoLep_pt*math.cos(recoLep_phi - met_phi))

    printStr = []
    printStr.append('\nReco lep pdgId: ' + str(recoLep_pdgId))
    printStr.append('\nReco lep pt: ' + str(recoLep_pt))
    printStr.append('\nReco lep eta: ' + str(recoLep_eta))
    printStr.append('\nReco lep phi: ' + str(recoLep_phi))
    printStr.append('\nmet_pt: ' + str(met_pt)) 
    printStr.append('\nmet_phi: ' + str(met_phi)) 
    printStr.append('\n')
    logger.trace(''.join(printStr))
 
    return Wpt 


def processFakesFromTaus(readTree, splitTree, params, dRcut, recoLep_eta, recoLep_phi, genPartColl = "GenPart"):
    '''Tags (fake) leptons which come from Taus (hadron punch-through or neutral pions misidentified in ECAL) 
       NOTE: Here is no selection requiring that the recoLep is a fake (via mcMatchId) - this is done before calling the function.
    '''

    logger = logging.getLogger('cmgPostProcessing.processFakesFromTaus')

    genPartObj = cmgObjectSelection.cmgObject(readTree, splitTree, genPartColl)
    
    isFakeFromTau = False

    for iGenPart in range(genPartObj.nObj):
        if abs(genPartObj.pdgId[iGenPart]) != 15: continue # selecting Taus
        if abs(genPartObj.motherId[iGenPart]) not in [24, 23] and not (genPartObj.motherId[iGenPart] == -9999 and iGenPart < 3): continue # ensuring that the Tau comes from W/Z/gamma

        recoLep_genPart_dR = helpers.dR_alt((recoLep_eta, recoLep_phi), (genPartObj.eta[iGenPart], genPartObj.phi[iGenPart]))

        printStr = []
        printStr.append('\nReco lep eta: ' + str(recoLep_eta))
        printStr.append('\nReco lep phi: ' + str(recoLep_phi))
        printStr.append('\ngenPart index: ' + str(iGenPart)) 
        printStr.append('\ngenPart pdgId: ' + str(genPartObj.pdgId[iGenPart])) 
        printStr.append('\ngenPart motherId: ' + str(genPartObj.motherId[iGenPart])) 
        printStr.append('\ngenPart eta: ' + str(genPartObj.eta[iGenPart]))
        printStr.append('\ngenPart phi: ' + str(genPartObj.phi[iGenPart]))
        printStr.append('\ndRcut: ' + str(dRcut)) 
        printStr.append('\ndR: ' + str(recoLep_genPart_dR)) 
        printStr.append('\n')
        logger.trace(''.join(printStr))
 
        logger.trace(
            '\n dR of reconstructed lepton and generated particle with index %i, recoLep_genPart_dR = %f \n', 
            iGenPart, 
            recoLep_genPart_dR
            )
        if recoLep_genPart_dR < dRcut:
            isFakeFromTau = True
            logger.trace('isFakeFromTau True. Breaking loop. \n')
            break
    
    return isFakeFromTau 

def processJets_func(args, readTree, splitTree, saveTree, params, computeVariables, cmgObj, indexList):
    '''Process jets. 

    Compute computeVariables quantities required in a jet selector, using 
    the cmgObj collection of jets and indices from the selector.
    '''
    #
    logger = logging.getLogger('cmgPostProcessing.processJets_func')

    verbose = args.verbose

    computeVariablesName = computeVariables['computeVariablesName']

    for var in computeVariablesName:
        if 'ht' in var:
            # HT as sum of jets from the given collection
            ht = sum(cmgObj.pt[idx] for idx in indexList)

            setattr(saveTree, var, ht)

        # dR and dPhi between the first two jets

        if 'dR_j1j2' in var:
            if len(indexList) > 1:
                dR_j1j2 = helpers.dR(indexList[0], indexList[1], cmgObj)

                setattr(saveTree, var, dR_j1j2)

        if 'dPhi_j1j2' in var:
            if len(indexList) > 1:
                dPhi_j1j2 = helpers.dPhi(indexList[0], indexList[1], cmgObj)

                setattr(saveTree, var, dPhi_j1j2)

    if logger.isEnabledFor(logging.DEBUG):
        printStr = ["\n Quantities computed in processJets_func"]

        for var in computeVariablesName:
            printStr.append('\n saveTree.')
            printStr.append(var)
            printStr.append(' = ')
            printStr.append(str(getattr(saveTree, var)))

        logger.debug(''.join(printStr))
        

def processBTagWeights(
        args, readTree, splitTree, saveTree,
        params
        ):
    '''Process BTag Weights using Robert's btagEfficiency class. 
    
    TODO describe here the processing.
    '''

    logger = logging.getLogger('cmgPostProcessing.processBTagWeights')

    # get the configuration parameters for this function

    BTagWeights_conf_names = params['BTagWeights_conf_names']  
    
    
    for conf_name in BTagWeights_conf_names:

        BTagWeights_conf = params[conf_name]
        jetSelectorId    = BTagWeights_conf['jetSelectorId']
        
        maxMultBTagWeight = BTagWeights_conf['maxMultBTagWeight']

        effFile          =   params['beff']['effFile']
        sfFile           =   params['beff']['sfFile']
        sfFile_FastSim   =   params['beff']['sfFile_FastSim']
        
        btagEff          =   params['beff']['btagEff']
   
        # get the lists of indices 
        
        jetColl = BTagWeights_conf['jetColl']
        jetObj = cmgObjectSelection.cmgObject(readTree, splitTree, jetColl)
        
        jetList      = getListFromSaveTree(saveTree, BTagWeights_conf['jet'])
        bJetList     = getListFromSaveTree(saveTree, BTagWeights_conf['bjet'])
        bSoftJetList = getListFromSaveTree(saveTree, BTagWeights_conf['bJetSoft'])
        bHardJetList = getListFromSaveTree(saveTree, BTagWeights_conf['bJetHard'])
        softJetList  = getListFromSaveTree(saveTree, BTagWeights_conf['jetSoft'])
        hardJetList  = getListFromSaveTree(saveTree, BTagWeights_conf['jetHard'])
        
        nonBJetList     = [x for x in jetList if x not in bJetList]
        nonBSoftJetList = [x for x in jetList if x not in bSoftJetList]
        nonBHardJetList = [x for x in jetList if x not in bHardJetList]
        
        for i in jetList:
            btagEff.addBTagEffToJet(jetObj,i)
        
        ## in order for th getObjDict to work with beff
        setattr(readTree, "%s_%s" % (jetObj.obj, 'beff'),jetObj.beff)  
        
        varList = ['pt', 'eta', 'phi', 'mass', 'hadronFlavour', 'beff' ]
        
        jets         = jetObj.getObjDictList(  varList , jetList         )
        softJets     = jetObj.getObjDictList(  varList , softJetList     ) 
        hardJets     = jetObj.getObjDictList(  varList , hardJetList     ) 
        bJets        = jetObj.getObjDictList(  varList , bJetList        )
        bSoftJets    = jetObj.getObjDictList(  varList , bSoftJetList    )
        bHardJets    = jetObj.getObjDictList(  varList , bHardJetList    )
        nonBJets     = jetObj.getObjDictList(  varList , nonBJetList     )
        nonBSoftJets = jetObj.getObjDictList(  varList , nonBSoftJetList )
        nonBHardJets = jetObj.getObjDictList(  varList , nonBHardJetList )
        
        #btag_nonbtag_list_pairs = {
        #                        'BTag'  : ( bJetList, nonBJetList ),
        #                        'SBTag' : ( bSoftJetList , nonBSoftJetList ),
        #                        'HBTag' : ( bHardJetList , nonBHardJetList ),
        #                          }
        btag_nonbtag_pairs = {
                                'BTag'  : ( bJets, nonBJets , jets),
                                'SBTag' : ( bSoftJets , nonBSoftJets , softJets),
                                'HBTag' : ( bHardJets , nonBHardJets , hardJets),
                             }

        if False:
            print "\n==================================================================================="
            print "Conf Name   "  ,  conf_name
            print "jets        "  ,  [ [x['pt']] for x in jets         ] 
            print "sofJets     "  ,  [ [x['pt']] for x in softJets     ]  
            print "hardJets    "  ,  [ [x['pt']] for x in hardJets     ] 
            print "bJets       "  ,  [ [x['pt']] for x in bJets        ]
            print "bSoftJets   "  ,  [ [x['pt']] for x in bSoftJets    ] 
            print "bHardJets   "  ,  [ [x['pt']] for x in bHardJets    ] 
            print "nonBJets    "  ,  [ [x['pt']] for x in nonBJets     ] 
            print "nonBSoftJets"  ,  [ [x['pt']] for x in nonBSoftJets ]     
            print "nonBHardJets"  ,  [ [x['pt']] for x in nonBHardJets ] 
            print "===================================================================================\n"

       
        for bTagName, bJets_nonBJets_jets in btag_nonbtag_pairs.iteritems():
            bj , nonbj , j = bJets_nonBJets_jets
            #print "  ", bTagName, "  -----------"*10
            for var in btagEff.btagWeightNames:
                #varName = "_%s"%var if var!="MC" else ""
                varName = "_%s_%s"%(var, jetSelectorId)
                #
                # Method 1a:
                #
                if var!= 'MC':
                    setattr(saveTree, "weight1a%s%s"%(bTagName, varName), btagEff.getBTagSF_1a( var, bj, nonbj))
                #
                # Method 1b:
                #
                #print "\nVAR:"  , var
                #print "\nBJets:", bj
                #print "\nNonBJets:", nonbj
                #print "\nAllJets:", j
                multiBTagWeightDict = btagEff.getWeightDict_1b( [  jj['beff'][var] for jj in j  ] , maxMultBTagWeight)
                #print "-----------"*10, var
                #pprint.pprint(multiBTagWeightDict)
                for nB in range(maxMultBTagWeight+1):
                    #print nB 
                    setattr(saveTree, "weight%s%s%s"%(bTagName, nB, varName), multiBTagWeightDict[nB])
                    if nB>0:
                        #pprint.pprint( "  %s"%multiBTagWeightDict.values()[:nB]  ) 
                        #print 1 - sum( multiBTagWeightDict.values()[:nB] )
                        #print "weight%s%sp%s"%(bTagName, nB, varName) 
                        setattr(saveTree, "weight%s%sp%s"%(bTagName, nB, varName), 1 - sum( multiBTagWeightDict.values()[:nB] )   )  # more than nB  (i.e. 1p,2p)


    processBTagWeights_rtuple = None #FIXME
    
    return saveTree, processBTagWeights_rtuple


def processEventVetoList(readTree, splitTree, saveTree, veto_event_list):
    ''' 
        
    '''
    
    logger = logging.getLogger('cmgPostProcessing.processEventVetoList')

    run_lumi_evt = saveTree.run_lumi_evt 
    
    if run_lumi_evt in veto_event_list:
        flag_Veto_Event_List = 0
        logger.debug(
            "\n Run:LS:Event %s failed veto list",
            run_lumi_evt
            )
    else:
        flag_Veto_Event_List = 1
        logger.trace(
            "\n Run:LS:Event %s passed veto list",
            run_lumi_evt
            )
        
    #
    return flag_Veto_Event_List    

def processEventVetoFilters(sample, readTree, splitTree, saveTree, params):
    ''' 
    Flag for vetoing events which do not pass the specified filters      
    '''
    
    logger = logging.getLogger('cmgPostProcessing.processEventVetoFilters')

    run_lumi_evt = saveTree.run_lumi_evt 
    
    # sample type (data or MC, taken from CMG component)
    isDataSample = sample['isData']
   
    if isDataSample: filters = params['filters']['data']
    else:            filters = params['filters']['MC']

    filterFlags = hephyHelpers.getObjDict(splitTree, "Flag_", filters, 0)
 
    if 0 in filterFlags.values():
        flag_Filters = 0
        logger.debug(
            "\n Run:LS:Event %s failed filters",
            run_lumi_evt
            )
    else:
        flag_Filters = 1
        logger.trace(
            "\n Run:LS:Event %s passed filters",
            run_lumi_evt
            )
        
    return flag_Filters

def processEventVetoFastSimJets(readTree, splitTree, saveTree, params):
    ''' Flag for vetoing events for FastSim samples, as resulted from 2016 "corridor studies".
    
          = 0: fails event
          = 1: pass event

    '''

    logger = logging.getLogger('cmgPostProcessing.processEventVetoFastSimJets')

    run_lumi_evt = saveTree.run_lumi_evt 

    # get the configuration parameters for this function
    
    Veto_fastSimJets_conf = params['Veto_fastSimJets_conf']

    # selection of reco jets
    
    recoJet_selector = Veto_fastSimJets_conf['recoJet']
    recoJet_obj_branches = recoJet_selector['branchPrefix']
    
    recoJet_index_rtuple = indexObjNames(recoJet_selector)
    recoJet_index_name = recoJet_index_rtuple.indexName
    
    recoJetObj = cmgObjectSelection.cmgObject(readTree, splitTree, recoJet_obj_branches)
    recoJetList = getListFromSaveTree(saveTree, recoJet_index_name)

    # selection of generated jets
        
    genJet_selector = Veto_fastSimJets_conf['genJet']
    genJet_obj_branches = genJet_selector['branchPrefix']
    
    genJet_index_rtuple = indexObjNames(genJet_selector)
    genJet_index_name = genJet_index_rtuple.indexName
    
    genJetObj = cmgObjectSelection.cmgObject(readTree, splitTree, genJet_obj_branches)
    genJetList = getListFromSaveTree(saveTree, genJet_index_name)

    # compute the criteria

    criteria_dR = Veto_fastSimJets_conf['criteria']['dR']
    noMatchedRecoJet = False

    for recoJetIdx, recoJet in enumerate(recoJetList):
        matchedRecoJet = False
        for genJetIdx, genJet in enumerate(genJetList):
            recoJet_genJet_dR = helpers.dR(recoJetList[recoJetIdx], genJetList[genJetIdx], recoJetObj, genJetObj)
            selector = helpers.evalCutOperator(recoJet_genJet_dR, criteria_dR)

            logger.trace(
                '\n Reconstructed jet with index %i, generated jet with index %i: recoJet_genJet_dR = %f \n', 
                recoJetList[recoJetIdx], 
                genJetList[genJetIdx], 
                recoJet_genJet_dR
                )

            if selector:
                matchedRecoJet = True
                logger.trace('Match True. Break for this reconstructed jet. \n')
                break
            else:
                logger.trace('Match False. \n')
                
        if not matchedRecoJet:
            noMatchedRecoJet = True
            logger.debug(
                '\n Reconstructed jet with index %i does not match any generated jet.', recoJetList[recoJetIdx]
                )
            break

    if noMatchedRecoJet:
        flag_veto_event_fastSimJets = 0
        logger.debug(
            "\n Run:LS:Event %s failed Veto_fastSimJets \n",
            run_lumi_evt
            )
    else:
        flag_veto_event_fastSimJets = 1
        logger.trace(
            "\n Run:LS:Event %s passed Veto_fastSimJets \n",
            run_lumi_evt
            )

    #
    return flag_veto_event_fastSimJets
    
def computeWeight(sample, sumWeight,  splitTree, saveTree, params, xsec=None , filterEfficiency=1.0):
    ''' Compute the weight of each event.
    
    Include all the weights used:
        genWeight - weight of generated events (MC only, set to 1 for data)
        luminosity weight 
    '''

    target_lumi = params['target_lumi']
    logger = logging.getLogger('cmgPostProcessing.computeWeight')
        
    # sample type (data or MC, taken from CMG component)
    isDataSample = sample['isData']
    


    # weight according to required luminosity 
    
    genWeight = 1 if isDataSample else splitTree.GetLeaf('genWeight').GetValue()

    if isDataSample: 
        lumiScaleFactor = 1
    else:
        if not xsec:
            xSection = sample['xsec']
        else:
            xSection = xsec
        lumiScaleFactor = filterEfficiency*xSection * target_lumi / float(sumWeight)
        
    saveTree.weight = lumiScaleFactor * genWeight
    
    logger.debug(
        "\n Computing weight for: %s sample " + \
        "\n    target luminosity: %f "
        "\n    genWeight: %f " + \
        "\n    %s" + \
        "\n    %s" + \
        "\n    sum of event weights: %f" + \
        "\n    luminosity scale factor: %f " + \
        "\n    Event weight: %f \n",
        ('Data ' + sample['cmgName'] if isDataSample else 'MC ' + sample['cmgName']),
        target_lumi, genWeight,
        ('' if isDataSample else 'cross section: ' + str(xSection) + ' pb^{-1}'),
        ('' if int(filterEfficiency) == 1 else 'filter efficiency: %s'%filterEfficiency),
        sumWeight, lumiScaleFactor, saveTree.weight)

    puWeightDict = params.get('puWeightDict')    
    if isDataSample:
        pass
    elif puWeightDict:
        nTrueInt = splitTree.GetLeaf("nTrueInt").GetValue()
        for pu, pu_dict in puWeightDict.iteritems():
            pu_var   = pu_dict['var']
            pu_thist = pu_dict['pu_thist'] 
            pu_w     = pu_thist.GetBinContent( pu_thist.FindBin(nTrueInt) )
            setattr(saveTree, pu_var, pu_w)
        logger.debug(
            "\n Computing PU weight for: %s sample \n" + \
            "\n    ".join(["%s : %s "%(pu['var'], getattr(saveTree,pu['var']) )   for pu in puWeightDict.itervalues() ] ),
            ('Data ' + sample['cmgName'] if isDataSample else 'MC ' + sample['cmgName']),

            )
        
    #
    return saveTree


def haddFiles(sample_name, root_output_file_prefix, filesForHadd, temporaryDir, outputWriteDirectory):
    ''' Add the histograms using ROOT hadd script
        
        If
            input files to be hadd-ed sum to more than maxFileSize MB or
            the number of files to be added is greater than  maxNumberFiles
        then split the hadd
    '''

    logger = logging.getLogger('cmgPostProcessing.haddFiles')
        
    maxFileSize = 100 # split into maxFileSize MB
    maxNumberFiles = 100
    logger.debug(
        "\n " + \
        "\n Sum up the split files in files smaller as %f MB \n",
         maxFileSize
         )

    size = 0
    counter = 0
    root_files = []
    for f in filesForHadd:
        size += os.path.getsize(temporaryDir + '/' + f)
        root_files.append(f)
        if size > (maxFileSize * (10 ** 6)) or f == filesForHadd[-1] or len(root_files) > maxNumberFiles:
            output_file = ''.join([
                root_output_file_prefix,
                str(counter),
                '.root'
                ])

            os.chdir(temporaryDir)
            logger.info(
                "\n Running hadd on directory \n %s \n files: \n %s \n",
                os.getcwd(), pprint.pformat(root_files)
                )
            subprocess.check_call(['hadd', output_file] + root_files)

            logger.debug(
                "\n Move file \n %s \n to directory \n %s \n",
                output_file, outputWriteDirectory
                )
            shutil.move(output_file, outputWriteDirectory)
            logger.debug("\n Written output file \n %s \n", output_file)
            size = 0
            counter += 1
            root_files = []
    
    # remove the temporary directory
    os.chdir(outputWriteDirectory)
    shutil.rmtree(temporaryDir, onerror=helpers.retryRemove)
    if not os.path.exists(temporaryDir): 
        logger.debug("\n Temporary directory \n    %s \n deleted. \n", temporaryDir)
    else:
        logger.info(
            "\n Temporary directory \n    %s \n not deleted. \n" + \
            "\n Delete it by hand. \n", 
            temporaryDir
            )
        
    return


def varsTreeLep(chunks, skimCond):
    ''' List of variables corresponding to LepGood branches.
      
    Some variables, defined as new in the parameter set, are added in rwTreeClasses.
    '''
    
    logger = logging.getLogger('cmgPostProcessing.varsTreeLep')

    for chunk in chunks:
        splitTreeKludge = getTreeFromChunk(chunk, skimCond, 0, 1)
    
        if not splitTreeKludge: 
            logger.warning("\n Tree object %s not found\n", splitTreeKludge)
            continue
        else:
            logger.debug("\n varsTreeLep on tree object %s \n from split fragment %i \n", splitTreeKludge, 0)
    
        # get the variables from LepGood
        branchPrefix = 'LepGood'
        lepGoodObj = cmgObjectSelection.cmgObject(None, splitTreeKludge, branchPrefix)
        objBranchList, objBranchNameType = lepGoodObj.getAllObjBranches()
        
        objVarNameType = [ var.replace(branchPrefix + '_', '')  for var in objBranchNameType]

        logger.debug(
            "\n List of all variables for object %s \n %s \n",
            branchPrefix, pprint.pformat(objVarNameType)
            )
        
        break
    
    return objVarNameType


def cmgPostProcessing(argv=None):
    
    if argv is None:
        argv = sys.argv[1:]
    
    # parse command line arguments
    args = get_parser().parse_args()
    

    # job control parameters
    
    verbose = args.verbose
    overwriteOutputDir = args.overwriteOutputDir
    overwriteOutputFiles = args.overwriteOutputFiles
    
    skimGeneral = args.skimGeneral
    skimLepton = args.skimLepton
    skimPreselect = args.skimPreselect
    
    processLepAll = args.processLepAll
    storeOnlyLepAll = args.storeOnlyLepAll
    
    args_processEventVetoList = args.processEventVetoList
    args_processEventVetoFilters = args.processEventVetoFilters
    args_processEventVetoFastSimJets = args.processEventVetoFastSimJets
    args_discardEvents = args.discardEvents
    
    if args_discardEvents:
        raise Exception("\n args.discardEvents not fully implemented yet.\n")
        sys.exit()
    
    if not processLepAll:
        if storeOnlyLepAll:
            raise Exception("\n storeOnlyLepAll option can only be used with processLepAll\n")
            sys.exit()
    
    testMethods = args.testMethods
        
    
#     # load FWLite libraries
#     
#     ROOT.gSystem.Load("libFWCoreFWLite.so")
#     ROOT.AutoLibraryLoader.enable()
#     
    # choose the sample(s) to process (allSamples), with results saved in outputDirectory
    
    cmgTuples = args.cmgTuples
    
    getSamples_rtuple = getSamples(args)
    
    allSamples = getSamples_rtuple.componentList
    outputDirectory = getSamples_rtuple.outputDirectory
    
    try:
        os.makedirs(outputDirectory)
        msg_logger_debug = \
            "\n Requested output directory \n {0} \n does not exists.".format(outputDirectory) + \
            "\n Created new directory. \n"
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
        else:
            msg_logger_debug = \
                "\n Requested output directory \n {0} \n already exists.\n".format(outputDirectory)
    
     
    # logging configuration

    logLevel = args.logLevel
    
    # use a unique name for the log file, write file in the dataset directory
    prefixLogFile = 'cmgPostProcessing_' + '_'.join([sample['cmgName'] for sample in allSamples]) + \
         '_' + logLevel + '_'
    logFile = tempfile.NamedTemporaryFile(suffix='.log', prefix=prefixLogFile, dir=outputDirectory, delete=False) 

    logger = get_logger(logLevel, logFile.name)
    
    if verbose:
        print "\n Log file stored in: \n", logFile.name
        print "\n Output directory: \n", outputDirectory 

    #
    logger.info("\n Job arguments: \n\n %s \n", pprint.pformat(vars(args)))

    #
    logger.info(
        "\n Running on CMG ntuples %s \n defined in the file \n %s" + \
        "\n Samples to be processed: %i \n\n %s \n\n Detailed sample description: \n\n  %s \n" + \
        "\n Results will be written to directory \n %s \n",
        cmgTuples, getSamples_rtuple.sampleFile, len(allSamples), 
        pprint.pformat([sample['cmgName'] for sample in allSamples]),
        pprint.pformat(allSamples),
        outputDirectory
        )
    
    # write the debug message kept in the msg_logger_debug
    logger.debug(msg_logger_debug)


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
    
    # create the dictionary of functions available to compute the 'extendCollection' from the defined extenders
    # this dictionary must be updated whenever new functions are defined
    extendVariablesFunctions = {
        'extend_LepGood_func': extend_LepGood_func,
        }

    # create the dictionary of functions available to compute the 'computeVariables' from the defined selectors
    # this dictionary must be updated whenever new functions are defined
    computeVariablesFunctions = {
        'processJets_func': processJets_func,
        }
    
    
    # get the event veto list FIXME: are the values updated properly?   
    if args_processEventVetoList:
        event_veto_list = get_veto_list()['all']
    else:
        event_veto_list = {}

    # loop over each sample, process all variables and fill the saved tree
    
    for isample, sample in enumerate(allSamples):
        
        sample_cmgName = sample['cmgName']
        sample_name = sample['name']
        
        isDataSample = sample.get('isData', False)
        isFastSimSample = sample.get('isFastSim', False)

        sampleType = 'Data' if isDataSample else ('MC Fast Simulation' if isFastSimSample else 'MC Full Simulation')
                              
        logger.info(
            "\n Running on CMG sample component %s of type %s \n",
            sample_cmgName, sampleType
            ) 

        #   prepare for signal scan
        
        if args.processSignalScan:
            
            mass_dict_file = sample.get('mass_dict', None)
            if mass_dict_file is not None: 
                if os.path.isfile(mass_dict_file):
                    mass_dict = pickle.load(open(mass_dict_file, "r"))
                else:
                    print "Pickle file {0} with mass dictionary for sample {1} does not exist. \nExiting.".format(
                        mass_dict_file, sample_cmgName)
                    raise Exception(
                        "Pickle file {0} with mass dictionary for sample {1} does not exist. \nExiting.".format(
                            mass_dict_file, sample_cmgName
                            )
                        )
            else:
                print "No pickle file defined for mass dictionary of signal scan mass points {0}. \nExiting job".format(
                    sample_cmgName
                    )
                raise Exception(
                    "No pickle file defined for mass dictionary of signal scan mass points {0}. \nExiting job".format(
                        sample_cmgName
                        )
                    )

            logger.info("\n Mass dictionary: \n \n %s \n ", pprint.pformat(mass_dict))

            if len(mass_dict) == 0:
                print "Empty mass dictionary loaded from pickle file {0} for sample {1}. \nExiting job.".format(
                    sample_cmgName
                    )
                raise Exception(
                    "Empty mass dictionary loaded from pickle file {0} for sample {1}. \nExiting job.".format(
                        sample_cmgName
                        )
                    )

            mass1   = args.processSignalScan[0]
            mass2    = args.processSignalScan[1]
            massVar1, massVar2 = sample['massVars']
            xsec    = mass_dict[int(mass1)][int(mass2)]['xSec']
            genFilterEff = mass_dict[int(mass1)][int(mass2)].get( 'genFilterEff', 1.)
            nEntries     = mass_dict[int(mass1)][int(mass2)]['nEvents']
    
        # skim condition
        skimSignalMasses = [ (massVar1, mass1) ,  (massVar2, mass2) ] if args.processSignalScan else []
        skimCond = eventsSkimPreselect(skimGeneral, skimLepton, skimPreselect, params, skimSignalMasses)
        logger.info("\n Final skimming condition: \n  %s \n", skimCond)

        #skimSignalMasses = [mstop, mlsp] if args.processSignalScan else []
        #skimCond = eventsSkimPreselect(skimGeneral, skimLepton, skimPreselect, params, skimSignalMasses)
        #logger.info("\n Final skimming condition: \n  %s \n", skimCond)

        # create the output sample directory, if it does not exist. 
        # If it exists and overwriteOutputDir is set to True, clean up the directory; if overwriteOutputDir is 
        # set to False: 
        #   if overwriteOutputFiles is False, skip the post-processing of this component
        #   if overwriteOutputFiles is True, clean up the corresponding root files only and post-processthis component
        #
        # create also a temporary directory (within the output directory)
        # that will be deleted automatically at the end of the job. If the directory exists,
        # it will be deleted and re-created.


        if args.processSignalScan:
            #sample_name = "SMS_T2_4bd_mStop_%s_mLSP_%s"%(mstop,mlsp)
            sample_name = sample['mass_template']%(mass1,mass2)
            #sample_name = "SMS_T2tt_mStop_%s_mLSP_%s"%(mstop,mlsp)
                
        logger.info(
            "\n Sample name (from sample file)  %s of type %s \n",
            sample_name, sampleType
            ) 

        outputWriteDirectory = os.path.join(outputDirectory, sample_name)

        if not os.path.exists(outputWriteDirectory):
            os.makedirs(outputWriteDirectory)
            logger.debug(
                "\n Requested sample directory \n %s \n does not exists." + \
                "\n Created new directory. \n", 
                outputWriteDirectory
                )
        else:
            if overwriteOutputDir:
                shutil.rmtree(outputWriteDirectory, onerror=helpers.retryRemove)
                os.makedirs(outputWriteDirectory)
                logger.info(
                    "\n Requested sample directory \n %s \n exists, and overwriteOutputDir is set to True." + \
                    "\n Cleaned up and recreated the directory done. \n", 
                    outputWriteDirectory
                    )
            else:
                if overwriteOutputFiles:
                    logger.info(
                        ''.join([
                            "\n Requested sample directory \n %s \n exists", 
                            "\n  overwriteOutputDir is set to False",
                            "\n  overwriteOutputFiles is set to True", 
                            "\n ==>  only the corresponding root files for this chunk range are cleaned later\n"
                            ]),
                        outputWriteDirectory
                        )
                    pass
                else:

                    logger.info(
                        ''.join([
                            "\n Requested sample directory \n %s \n exists", 
                            "\n  overwriteOutputDir is set to False",
                            "\n  overwriteOutputFiles is set to False",
                            "\n if root files for this chunk range exist, skip post-processing sample \n %s \n"
                            ]),
                        outputWriteDirectory, sample_name
                        )
        
        # python 2.7 version - must be removed by hand, preferably in a try: ... finalize:
        tmpPrefix = ''.join(['tmp_postProcessing_', sample_cmgName, '_'])
        temporaryDir = tempfile.mkdtemp(prefix=tmpPrefix, dir=outputDirectory) 
        #
        # for 3.X use
        # temporaryDir = tempfile.TemporaryDirectory(suffix=None, prefix=None, dir=None)
             
        logger.info("\n Output sample directory \n  %s \n", outputWriteDirectory) 
        logger.debug("\n Temporary directory \n  %s \n", temporaryDir) 
        
        allChunks, sampleSumWeight = hephyHelpers.getChunks(sample)
        allChunkIndices = helpers.getChunkIndex(sample, allChunks)

        logger.info(
            ''.join([
                "\n Sample %s of type %s has in total",
                "\n   number of chunks: %i",
                "\n   chunk index range: %i - %i \n",
                "\n   sampleSumWeight: %s \n",
                ]),
                sample_cmgName, sampleType, len(allChunks), allChunkIndices[0], allChunkIndices[-1], 
                sampleSumWeight
            )
        logger.debug(
            "\n List of all chunks for the sample: \n \n %s \n\n All chunk indices: \n %s \n", 
            pprint.pformat(allChunks), pprint.pformat(allChunkIndices)
            )

        selectedChunks = []
        selectedChunkIndices = []

        runChunks = args.runChunks

        if runChunks:
            chunkRange = [runChunks[0], runChunks[1]]
            for chunk in allChunks:
                chunkIndex = helpers.getChunkIndex(sample, [chunk])[0]
                if (chunkIndex >= chunkRange[0])  and (chunkIndex <= chunkRange[1]):
                    selectedChunks.extend([chunk])
                    selectedChunkIndices.append(chunkIndex)
        else:
           selectedChunks = allChunks
           selectedChunkIndices = allChunkIndices
           chunkRange = [allChunkIndices[0], allChunkIndices[1]]
        
        logger.info(
            ''.join([
                "\n Chunks selected to run over in this job: ",
                "\n   chunk index range: %i - %i",
                "\n   actual number of chunks: %i",
                "\n"
                ]),
                chunkRange[0], chunkRange[-1], len(selectedChunks) 
            )
        logger.debug(
            "\n Chunks selected to run over in this job: \n\n %s \n\n Selected chunk indices: \n %s \n",
            pprint.pformat(selectedChunks),
            pprint.pformat(selectedChunkIndices)
            )
        
        # the prefix of the ROOT files with saved tree - a counter (starting from 0) is added
        # to the prefix in haddFiles 
        root_output_file_prefix = ''.join([
                sample_name, '_Chunks_',
                str(chunkRange[0]), '_', str(chunkRange[-1]), '_',
                ])

        # cleanup the corresponding root files, if overwriteOutputFiles is set to True
        # Note: this option cleans up only the root files for the selected chunk range, if they exist, the
        # directory and the root files for the other chunk ranges are not touched
           
        if os.path.exists(outputWriteDirectory):
            
            os.chdir(outputWriteDirectory)
            filelist_root = glob.glob(root_output_file_prefix + "*.root")
            
            if overwriteOutputFiles and filelist_root:
                
                for f_root in filelist_root:
                    os.remove(f_root)
                
                logger.info(
                    "\n The following files were removed from directory \n %s: \n\n %s \n",
                    outputWriteDirectory, pprint.pformat(filelist_root)
                    )
            else:
                if filelist_root:
                    logger.error(
                        ''.join([
                            "\n The following files, corresponding to the same chunk range,", 
                            " exist in the directory \n %s: \n\n",
                            "%s \n", 
                            " and overwriteOutputFiles is set to False.",
                            "\n Skip post-processing sample %s \n"
                            ]), 
                        outputWriteDirectory, pprint.pformat(filelist_root), sample_name
                        )
                
                    continue
        
        # sum all the weights for samples having extended datasets
        
        sumWeight = 0.
        if 'ext' in sample:

            printString = []
            for sExt in sample['ext']:
                extSample = getattr(getSamples_rtuple.cmgSamples, sExt)
                if extSample:
                    chunkExt, weightExt = hephyHelpers.getChunks(extSample)
                    sumWeight += weightExt

                    printString.append("\n  sample: ")
                    printString.append(sExt)
                    printString.append("\n    weight sum: ")
                    printString.append(str(weightExt))
                else:
                    raise Exception("\n Extended dataset {0} requested for sample {1}, but not defined in {2}.".format(
                        sExt, sample_cmgName, getSamples_rtuple.sampleFile)
                        )
                    sys.exit()


            logger.info(
                ''.join([
                    "\n Sum of weights summed for all extended samples \n %s",
                    "\n   sumWeight: %s \n obtained from %s \n"
                    ]),
                sample['ext'], sumWeight, ''.join(printString)
                )
        else:
            sumWeight = sampleSumWeight
        
        # stupid kludge to get the list of branches for an objects, to be able to add a merged collection to tree
        varsNameTypeTreeLep = varsTreeLep(allChunks, skimCond)
          
        # get the tree structure      
        rwTreeClasses_rtuple = rwTreeClasses(sample, isample, args, temporaryDir, varsNameTypeTreeLep, params) 
        #
        keepBranches = rwTreeClasses_rtuple.keepBranches 
        dropBranches = rwTreeClasses_rtuple.dropBranches
             
        readVars = rwTreeClasses_rtuple.readVars
        aliases = rwTreeClasses_rtuple.aliases 
        readVectors = rwTreeClasses_rtuple.readVectors 
        
        newVars = rwTreeClasses_rtuple.newVars 
        newVectors = rwTreeClasses_rtuple.newVectors 
        
        readTree = rwTreeClasses_rtuple.readTree 
        saveTree = rwTreeClasses_rtuple.saveTree
        #
        
        filesForHadd=[]

        nEvents_total = 0
        
        for chunk in selectedChunks:
            
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
                        if v.has_key('size'):
                            #print v
                            vecSize = v['size'][var['stage2Name']]
                        else:
                            vecSize = str(v['nMax'])
                        var['branch'] = splitTree.Branch(
                            var['stage2Name'], 
                            ROOT.AddressOf(saveTree,var['stage2Name']), 
                            var['stage2Name']+'[' + vecSize + ']/'+var['stage2Type']
                            )

                # get entries for tree and loop over events
                
            
                logger.debug(
                    "\n Number of events after skimming and preselection: \n    chunk: %s \n    " + \
                    "split fragment %i of %i fragments in this chunk: \n    %i events \n", 
                    chunk['name'], iSplit, nSplit, nEvents
                    )

                start_time = int(time.time())
                last_time = start_time
                nVerboseEvents = 5000
                smallSampleEvents = 500
               
                runSmallSample = args.runSmallSample
 
                for iEv in xrange(nEvents):
                    
                    if runSmallSample and iEv >= smallSampleEvents: break # running over 100 events only if runSmallSample set to True
                 
                    nEvents_total +=1
                    if (nEvents_total%nVerboseEvents == 0) and nEvents_total>0:
                        passed_time = int(time.time() ) - last_time
                        last_time = time.time()
                        if passed_time:
                            if verbose:
                                print "Event:{:<8}".format(nEvents_total), "@ {} events/sec".format(
                                    round(float(nVerboseEvents)/passed_time )
                                    )                      
                            logger.info(
                                "\n Processing event %i from %i events from chunk \n %s \n" + \
                                "\n Total processed events from all chunks: %i \n",
                                iEv, nEvents, chunk['name'], nEvents_total
                                )
            
                    saveTree.init()
                    readTree.init()
                    splitTree.GetEntry(iEv)
                    
                    saveTree = getRunLumiEvt(splitTree, saveTree)
                    
                    logger.debug(
                        "\n " + \
                        "\n ================================================" + \
                        "\n * Processing Run:LS:Event %s \n",
                        saveTree.run_lumi_evt 
                        )

                    # compute first a flag for keeping / discarding the event
                    # if flag_keepEvent is 1, the event is kept
                    flag_keepEvent = 1
                    
                    # process event veto list flags
                    if isDataSample and args_processEventVetoList:
                        flag_Veto_Event_List = processEventVetoList(readTree, splitTree, saveTree, event_veto_list)
                        flag_keepEvent = flag_keepEvent and flag_Veto_Event_List
                        if not args_discardEvents:
                            saveTree.Flag_Veto_Event_List = flag_Veto_Event_List

                    # process event veto filters flags
                    if args_processEventVetoFilters:
                        flag_Filters = processEventVetoFilters(sample, readTree, splitTree, saveTree, params)
                        flag_keepEvent = flag_keepEvent and flag_Filters
                        if not args_discardEvents:
                            saveTree.Flag_Filters = flag_Filters

                    # compute flag for event veto for FastSim jets
                    if isFastSimSample and args_processEventVetoFastSimJets:
                        flag_veto_event_fastSimJets = processEventVetoFastSimJets(readTree, splitTree, saveTree, params)
                        flag_keepEvent = flag_keepEvent and flag_veto_event_fastSimJets
                        if not args_discardEvents:
                            saveTree.Flag_veto_event_fastSimJets = flag_veto_event_fastSimJets

                    if args_discardEvents and (not flag_keepEvent):
                        logger.debug(
                            "\n Run:LS:Event %s discarded. \n",
                            saveTree.run_lumi_evt
                        )
                        continue
                    
                    # extend all collections with variables requested to be
                    # computed at the beginning of the event loop
                    eval_begin = 1
                    saveTree = evaluateExtenders(
                        readTree, splitTree, saveTree, params, isDataSample, eval_begin, extendVariablesFunctions)

                    # evaluate all selectors
                    saveTree = evaluateSelectors(
                        readTree, splitTree, saveTree, params, isDataSample)

                    # merge muon and electrons for the required selectors
                    saveTree = mergeLeptons(
                        readTree, splitTree, saveTree, params)

                    # evaluate 'computeVariables' for all selectors
                    # the variables depend on the selector indices and on
                    # quantities already existing in the tree only

                    saveTree = computeVariablesSelectors(
                        readTree, splitTree, saveTree, params, isDataSample, computeVariablesFunctions)

                    if args.processBTagWeights:
                        saveTree, processBTagWeights_rtuple = processBTagWeights(
                            args, readTree, splitTree, saveTree,
                            params
                        )

                    # compute the weight of the event
                    if not args.processSignalScan:
                        saveTree = computeWeight(sample, sumWeight, splitTree, saveTree, params)
                    else:
                        saveTree = computeWeight(sample, nEntries, splitTree, saveTree, params, xsec=xsec, filterEfficiency=genFilterEff )
                            
                    # extend all collections with variables requested to be
                    # computed at the end of the event loop
                    eval_begin = 0
                    saveTree = evaluateExtenders(
                        readTree, splitTree, saveTree, params, isDataSample, eval_begin, extendVariablesFunctions)

                
                    # fill all the new variables and the new vectors        
                    for v in newVars:
                        v['branch'].Fill()
                        
                    for v in newVectors:
                        for var in v['vars']:
                            var['branch'].Fill()
                            
                # 
                
                fileTreeSplit_full = ''.join([
                    sample_name, '_', 
                    chunk['name'], '_', 
                    str(iSplit), '.root'
                    ])
                
                file_length_limit = 256
                if len(fileTreeSplit_full)> file_length_limit:
                    fileTreeSplit = ''.join([
                        sample_name[:50].rsplit('_', 1)[0], '___', 
                        chunk['name'][50:].split('_', 1)[1], '_', 
                        str(iSplit), '.root'
                        ])
                    logger.debug(
                        "\n Length of fileTreeSplit name over 256 characters, shortened to %d\n New file name: \n %s \n", 
                        len(fileTreeSplit), fileTreeSplit)
                else:
                    fileTreeSplit = fileTreeSplit_full
                
                filesForHadd.append(fileTreeSplit)

                if not testMethods:
                    tfileTreeSplit = ROOT.TFile(temporaryDir + '/' + fileTreeSplit, 'CREATE')

                    splitTree.SetBranchStatus("*", 0)
                    for b in (keepBranches + 
                              [v['stage2Name'] for v in newVars] + 
                              [v.split(':')[1] for v in aliases]):
                        splitTree.SetBranchStatus(b, 1)
                    for b in dropBranches:
                        splitTree.SetBranchStatus(b,0)
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
            haddFiles(
                sample_name,  
                root_output_file_prefix,
                filesForHadd, 
                temporaryDir, 
                outputWriteDirectory
                )
        
        end_message =  "\n " + \
            "\n ******** End of post-processing sample \n ******** {0}.".format(sample_name) + \
            "\n Total number of events processed for this sample: {0}".format(nEvents_total) + \
            '\n'
              
        logger.info(end_message)
        
        if verbose:
            print end_message
    
    if verbose:
        print '\n End of cmgPostProcessing script.\n'
 
if __name__ == "__main__":

    args = get_parser().parse_args()
    if args.runInteractively:
        ret = cmgPostProcessing()

    else:
        sys.exit(cmgPostProcessing())
