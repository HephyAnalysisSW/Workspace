import os
import sys
import time
import re
import random
import string
import gzip

import lheMergeDecayedParticles

# classes and methods

class LheFile:
    def __init__(self, fullName, name, stopMass, lspGeneratedMass, runNumber, lspMass, processPrefix, nrEvents):
        self.fullName = fullName
        self.name = name
        self.stopMass = stopMass
        self.lspGeneratedMass = lspGeneratedMass        
        self.runNumber = runNumber        
        self.lspMass = lspMass 
        self.processPrefix = processPrefix 
        self.nrEvents = nrEvents           
  
    def __repr__(self):
        return '\n' + self.fullName + \
               '\n' + self.name + \
               '\n' + str(self.stopMass) + \
               '\n' + str(self.lspGeneratedMass) + \
               '\n' + str(self.runNumber) + \
               '\n' + str(self.lspMass) + \
               '\n' + str(self.nrEvents)
  
    def __str__(self):
        if (self.nrEvents > 0):
            nrEventsString = str(self.nrEvents)
        else:
            nrEventsString = 'N/A'
        
        if (self.lspMass > 0):
            lspMassString = str(self.lspMass)
        else:
            lspMassString = 'N/A'

        return '\nFull name:          ' + self.fullName + \
               '\nName:               ' + self.name + \
               '\nStop mass:          ' + str(self.stopMass) + \
               '\nGenerated LSP mass: ' + str(self.lspGeneratedMass) + \
               '\nRun number:         ' + str(self.runNumber) + \
               '\nDecay LSP mass:     ' + lspMassString + \
               '\nNumber of events:   ' + nrEventsString + \
               '\n'
        
def findNrEvents(fileName):

    if os.path.isfile(fileName):  
        
        lheFile = gzip.open(fileName, 'rb')
        nrEv = 0 
        nrEvLine = '#  Number of Events        :'
        for fileLine in lheFile:
            if (nrEvLine in fileLine):
                
                nrEv = int(((fileLine.split(':', 2)[1])).rstrip('\n'))
                break
            
        nrEventsPerFile = nrEv
        lheFile.close()
    else:
        nrEventsPerFile = -1
    
    return nrEventsPerFile


def extractListOfFiles (stageUndecayedLheFilesValue, \
                        lheUndecayedEosDir, \
                        undecayedFilesStageDir, \
                        undecayedFilesDir):
    
    # extract the full list of the LHE undecayed files, for all stop masses and generated LSP masses 
 
    debug = False
    
    # take the list of file from the EOS directory, if files are to be staged, 
    # or from the local undecayed LHE file directory
    tmpFileList = 'tmpListOfFiles.txt'
    
    if stageUndecayedLheFilesValue: 
        os.system('cmsLs ' + lheUndecayedEosDir + ' > ' + tmpFileList)  
        lheLsPrefix = lheUndecayedEosDir 
        prefixFullName = lheLsPrefix + '/'
    else:   
        os.system('cp ' + undecayedFilesDir + '.txt ' + tmpFileList)               
        lheLsPrefix = '' 
        prefixFullName = undecayedFilesStageDir + '/'
        

    fileList = []

    cmsLsList = open(tmpFileList, 'r')
    for fileLine in cmsLsList:
        if (lheLsPrefix in fileLine) or (not stageUndecayedLheFilesValue):
            if stageUndecayedLheFilesValue:
                fileNameStart = string.find(fileLine, lheLsPrefix) + len(lheLsPrefix) + 1
            else:
                fileNameStart = 0
                
            fileName = fileLine[fileNameStart:].rstrip('\n')
            
            splitFileName = fileName.split('_', 7)
            stopMassValue = int(splitFileName[3])
            lspGenMassValue = int(splitFileName[4])
            processPrefixValue = splitFileName[0] + '_' +  splitFileName[1] + '_' +  splitFileName[2] + '_'

            matchObject = re.search(r'run(\d+)', splitFileName[5])
            runNumber = matchObject.group(1)
            
            dummyLspMass = -1
            nrEventsPerFile = -1
                
            lheFile = LheFile(prefixFullName +  fileName, fileName, \
                              stopMassValue, lspGenMassValue, runNumber, dummyLspMass, \
                              processPrefixValue, nrEventsPerFile)
            
            
            fileList.append(lheFile)       
    
    
    print '\nLHE undecayed files, full sample: ' + str(len(fileList)) + ' files',\
    ' [extractListOfFiles]\n'
    
    if debug:
        for lheFile in fileList:
            print lheFile
       
    # close the temporary file and delete it     
    cmsLsList.close()   
    os.system('rm -f ' + tmpFileList)
   
    return fileList

    

def extractListOfUndecayedFiles (lheFileList, stopMassLimitsValues, generatedLspMassLimitsValues):
    
    # extract the list of LHE undecayed files corresponding to the given input parameters to be staged
    
    debug = True

    #
        
    fileList = []

    for lheFile in lheFileList:
        
        stopMassValue = lheFile.stopMass
        lspGenMassValue = lheFile.lspGeneratedMass
        
        if stopMassLimitsValues[0] < 0:
            if generatedLspMassLimitsValues[0] < 0:
                
                fileList.append(lheFile)
            else:
                if ( lspGenMassValue >= generatedLspMassLimitsValues[0] ) and \
                   ( lspGenMassValue <= generatedLspMassLimitsValues[1] ):
                    
                    fileList.append(lheFile)
                    
        elif ( stopMassValue >= stopMassLimitsValues[0] ) and ( stopMassValue <= stopMassLimitsValues[1] ):
            if generatedLspMassLimitsValues[0] < 0:
                
                fileList.append(lheFile)
                
            else:
                if ( lspGenMassValue >= generatedLspMassLimitsValues[0] ) and \
                   ( lspGenMassValue <= generatedLspMassLimitsValues[1] ):
                    
                    fileList.append(lheFile)
            

    print '\nUndecayed LHE files to be processed: ' + str(len(fileList)) + ' files',\
        ' [extractListOfUndecayedFiles]\n'
    
    if debug:
        print '\n'
        for lheFile in fileList:
            print lheFile
       
    return fileList


def stageLheFiles (fileList, lheStageDirectory):

    # stage the LHE files from fileList to the lheStageDirectory

    debug = False

    # clean up the stage directory
    if(os.path.exists(lheStageDirectory)):
        os.system('rm -r ' + lheStageDirectory)
    os.system('mkdir -p ' + lheStageDirectory)

    print '\nStaging LHE files: ', str(len(fileList)) + ' files to be staged',\
            ' [stageLheFiles]\n'

    for lheFile in fileList:
        eosFile = lheFile.fullName 
        localStagedFile = lheStageDirectory + '/' + lheFile.name
        if debug:
            print '    ' + 'cmsStage ' + eosFile + ' ' + localStagedFile
        os.system('cmsStage ' + eosFile + ' ' + localStagedFile)
    
        if debug:
            print
        
    return

def copyLheFiles(fileList, lheLocalDirectory):

    # copy the undecayed LHE files from fileList to the local job directory of undecayed files

    debug = False

    print '\nCopying LHE files to: ' + lheLocalDirectory + '\n    '
    print  str(len(fileList)) + ' files to be copied', \
            ' [copyLheFiles]\n'

    for lheFile in fileList:
        
        remoteFile = lheFile.fullName 
        localFile = lheLocalDirectory + '/' + lheFile.name
        
        # use cp for local source and destination files, and xrdcp if the remote file
        # is on the storage element 
        copyProtocol = 'cp'
        fileTypeIndicator = ':/'
        if (fileTypeIndicator in remoteFile):
            copyProtocol = 'xrdcp'
        
        if debug:
            print '    ' + copyProtocol + ' ' + remoteFile + ' ' + localFile
            
        os.system(copyProtocol + ' ' + remoteFile + ' ' + localFile)
    
        if debug:
            print
        
    return

def assignLspMass(lheFileList, deltaMassStopLspValues, deltaMassStopLspFractionsValues, splitUndecayedSampleValue, undecayedFilesDir):

    # assign to each entry from lheFileList the decay LSP mass to be used, according to 
    # the statistics fraction if splitUndecayedSample is True
 
    debug = False
 
    # get a set of unique, sorted values of stop masses from the LHE files,
    # the total number of events and the total number of files for each stop mass
    
    stopMassValuesUnsorted = set()
    nrEventsPerStopMass = dict()
    nrFilesPerStopMass = dict()
    nrEventsPerStopMassLocal = dict()
    nrFilesPerStopMassLocal = dict()

    fileListLhe = []   
                
    for lheFile in lheFileList:
        stopMassValue = lheFile.stopMass
        stopMassValuesUnsorted.add(stopMassValue)
        stagedFileName = undecayedFilesDir + '/' + lheFile.name
        lheFileNrEvents = findNrEvents(stagedFileName)

        lheFileNew = LheFile(lheFile.fullName, lheFile.name, \
                            lheFile.stopMass, lheFile.lspGeneratedMass, \
                            lheFile.runNumber, \
                            lheFile.lspMass, lheFile.processPrefix, lheFileNrEvents)
       
        fileListLhe.append(lheFileNew)    
     
    stopMassValues = sorted(stopMassValuesUnsorted) 
    
    print '\nNumber of events for stop mass bins',\
    ' [assignLspMass]\n'
    
    for stopMass in stopMassValues:
         nrEventsPerStopMass[stopMass] = 0
         nrFilesPerStopMass[stopMass] = 0
         nrEventsPerStopMassLocal[stopMass] = 0
         nrFilesPerStopMassLocal[stopMass] = 0
         nrEvents = 0
         nrFiles = 0
         nrEventsLocal = 0
         nrFilesLocal = 0
         
         for lheFile in fileListLhe:
             stopMassValue = lheFile.stopMass
             if stopMassValue == stopMass:
                 lheFileNrEvents = lheFile.nrEvents
                 if (lheFileNrEvents > 0):
                     nrEvents += lheFileNrEvents
                     nrEventsLocal += lheFileNrEvents
                     nrFilesLocal += 1
                 else:
                     nrEvents = -1
                 nrFiles += 1
       
         nrEventsPerStopMass[stopMass] = nrEvents
         nrFilesPerStopMass[stopMass] = nrFiles
         nrEventsPerStopMassLocal[stopMass] = nrEventsLocal
         nrFilesPerStopMassLocal[stopMass] = nrFilesLocal
         
         if (nrEventsPerStopMass[stopMass] > 0):
             print '    stop mass = ', stopMass, ' GeV',  \
                '\n      Total:     ', \
                nrFilesPerStopMass[stopMass], ' files; number of events: ', nrEventsPerStopMass[stopMass], \
                '\n      Job local: ', \
                nrFilesPerStopMassLocal[stopMass], ' files; number of events: ', nrEventsPerStopMassLocal[stopMass], \
                '\n'
                
         else:
             print '    stop mass = ', stopMass, ' GeV',  \
                '\n      Total:     ', \
                nrFilesPerStopMass[stopMass], ' files; number of events: N/A', \
                '\n      Job local: ', \
                nrFilesPerStopMassLocal[stopMass], ' files; number of events: ', nrEventsPerStopMassLocal[stopMass], \
                '\n'


    # check if all deltaMassStopLsp values are possible for each stop mass, otherwise re-adjust 
    # the fractions, increasing them proportionally FIXME implement it, if ever needed
                     
    # now assign to each entry from lheFileList the decay LSP mass to be used, 
    #     if splitUndecayedSampleValue is True, according to the statistics fraction
    #     else loop over all allowed values
    
    fileList = []   
    fileListDrop = []
    
    for stopMass in stopMassValues:
        for dMassIndex, dMass in enumerate(deltaMassStopLspValues):
            
            nrEventsdMassBin = 0
            lspMass = stopMass - dMass

            if lspMass >= 0:                
                for lheFile in fileListLhe:
                    
                    if lheFile.stopMass == stopMass:                        
                        lheFileNrEvents = lheFile.nrEvents
                        if splitUndecayedSampleValue:
                            if lheFile not in fileListDrop:
                                nrEventsBin = nrEventsdMassBin + lheFileNrEvents
                                eventFraction = float(nrEventsBin)/float(nrEventsPerStopMass[stopMass])
                            
                                if eventFraction  <= deltaMassStopLspFractionsValues[dMassIndex]:
                                    nrEventsdMassBin += lheFileNrEvents
                                    lheFileNew = LheFile(lheFile.fullName, lheFile.name, \
                                                         lheFile.stopMass, lheFile.lspGeneratedMass, \
                                                         lheFile.runNumber, \
                                                         lspMass, lheFile.processPrefix, lheFileNrEvents)
       
                                    fileList.append(lheFileNew)
                                    fileListDrop.append(lheFile)
                                    
                        else:
                            lheFileNew = LheFile(lheFile.fullName, lheFile.name, \
                                                lheFile.stopMass, lheFile.lspGeneratedMass, \
                                                lheFile.runNumber, \
                                                lspMass, lheFile.processPrefix, lheFileNrEvents)
       
                            fileList.append(lheFileNew)    
                            
    
    print '\nLHE files with assigned LSP mass: ' + str(len(fileList)) + ' files',\
        ' [assignLspMass]\n'
    if debug:
        for lheFile in fileList:
            print lheFile

    return fileList

def extractListOfFilesToProcess (lheFileList, stopMassLimitsValues, generatedLspMassLimitsValues, \
                                 deltaMassStopLspSelectedValues):
    
    # extract the list of files to process corresponding to the given input parameters
    
    debug = True

    #
        
    fileList = []

    for lheFile in lheFileList:
        
        stopMassValue = lheFile.stopMass
        lspGenMassValue = lheFile.lspGeneratedMass
        lspMassValue = lheFile.lspMass
        
        if stopMassLimitsValues[0] < 0:
            if generatedLspMassLimitsValues[0] < 0:
                
                for dMass in deltaMassStopLspSelectedValues:
                    diffMassStopLsp = stopMassValue - dMass
                    if lspMassValue == diffMassStopLsp:
                        fileList.append(lheFile)
            else:
                if ( lspGenMassValue >= generatedLspMassLimitsValues[0] ) and \
                   ( lspGenMassValue <= generatedLspMassLimitsValues[1] ):
                
                    for dMass in deltaMassStopLspSelectedValues:
                        diffMassStopLsp = stopMassValue - dMass
                        if lspMassValue == diffMassStopLsp:
                            fileList.append(lheFile)
                    
        elif ( stopMassValue >= stopMassLimitsValues[0] ) and ( stopMassValue <= stopMassLimitsValues[1] ):
            if generatedLspMassLimitsValues[0] < 0:
                
                for dMass in deltaMassStopLspSelectedValues:
                    diffMassStopLsp = stopMassValue - dMass
                    if lspMassValue == diffMassStopLsp:
                        fileList.append(lheFile)
                
            else:
                if ( lspGenMassValue >= generatedLspMassLimitsValues[0] ) and \
                   ( lspGenMassValue <= generatedLspMassLimitsValues[1] ):

                    for dMass in deltaMassStopLspSelectedValues:
                        diffMassStopLsp = stopMassValue - dMass
                        if lspMassValue == diffMassStopLsp:
                            fileList.append(lheFile)
            

    print '\nFiles to process in MadGraph: ' + str(len(fileList)) + ' files',\
        ' [extractListOfFilesToProcess]\n'
    
    if debug:
        print '\n'
        for lheFile in fileList:
            print lheFile
       
    return fileList



def processNameDef(lheFile, decayParticleValue):
    
    # define the process name for a given particle
           
    processName = str(lheFile.stopMass) + '_' + \
               str(lheFile.lspGeneratedMass) + '_' + \
               'run' + str(lheFile.runNumber)  + '_' + \
               decayParticleValue + str(lheFile.stopMass) + '_' + \
               str(lheFile.lspMass)
                  
    return processName

def madgraphDecayParticle (lheFile, decayParticleValue, madGraphDir, workingDir, numberEvents):
    
    debug = False

    # cards directory, relative to production directory
    workspaceCardDirectory = 'Workspace/MonoJetAnalysis/lheFileProduction/data/Cards'
    
    param_card_TEMPLATE = 'official_param_card_TEMPLATE.dat'
    param_card_TEMPLATE_wpath = workingDir + '/' + workspaceCardDirectory  + '/' + param_card_TEMPLATE

    run_card_decay_TEMPLATE = 'official_run_card_decay_TEMPLATE.dat'
    run_card_decay_TEMPLATE_wpath = workingDir + '/' + workspaceCardDirectory  + '/' + \
        run_card_decay_TEMPLATE
    
    input_card_decay_TEMPLATE_wpath = workingDir + '/' + workspaceCardDirectory  + '/' + \
        'production_input_card_decay_TEMPLATE.dat'

    input_card_decay_tmp = 'production_input_card_decay_tmp.dat'
    input_card_decay_tmp_wpath = workingDir + '/' + workspaceCardDirectory  + '/' + input_card_decay_tmp

    # define the process name and substitute the values in production_input_card_decay_TEMPLATE.dat
           
    processName = processNameDef(lheFile, decayParticleValue)
                      
    if decayParticleValue == 'decayStop':
        xcstop = ''
        xcanti = '#'
    elif decayParticleValue == 'decayAntiStop':
        xcstop = '#'
        xcanti = ''
    
    seed = int(904866561*random.random())
    os.system('perl -p -e "s/XSEED/' + str(seed) + '/;' \
                          's/XCSTOP/' + xcstop + '/;' \
                          's/XCANTI/' + xcanti + '/;' \
                          's/XLSPMASS/' + str(lheFile.lspMass) + '/;' \
                          's/XSTOPMASS/' + str(lheFile.stopMass) + '/;' \
                          's/PROC_NAME/PROC_' + processName + '/g;' \
                          '" ' + input_card_decay_TEMPLATE_wpath + ' > ' + input_card_decay_tmp_wpath)

    # copy the cards to the MadGraph directory
    os.system('cp  ' + input_card_decay_tmp_wpath + ' ' + madGraphDir)
    os.system('cp  ' + param_card_TEMPLATE_wpath + ' ' + madGraphDir)
    os.system('cp  ' + run_card_decay_TEMPLATE_wpath + ' ' + madGraphDir)
    
    workDir = os.getcwd()
    
    # change to MadGraph directory, change the number of events,
    #     clean up if needed, then run Madgraph
    os.chdir(madGraphDir)

    if numberEvents > 0: 
        oldNrEvents = '100000       = nevents'
        newNrEvents = str(numberEvents) + '      = nevents'
        os.system('perl -p -i -e "s/' + oldNrEvents + '/' + newNrEvents + '/' \
                          '" ' + run_card_decay_TEMPLATE)

    if(os.path.exists('PROC_' + processName)):
        os.system('rm -r PROC_' + processName)
   
    os.system('bin/mg5 ' + input_card_decay_tmp)
    
    # remove the cards to the MadGraph directory
    os.system('rm  ' + input_card_decay_tmp)
    os.system('rm  ' + param_card_TEMPLATE)
    os.system('rm  ' + run_card_decay_TEMPLATE)
    
    # remove the temporary input cards
    os.system('rm  ' + input_card_decay_tmp_wpath)
    
    # change back to work directory
    os.chdir(workDir)
       
    return

def madgraphProduceDecays (fileListDecay, \
                           decayParticleValue, decayAntiParticleValue, \
                           madGraphDir, workingDir, \
                           numberEvents):
    
    # decay in MadGraph the given particle
        
    for lheFile in fileListDecay:
        
        # decay particle
        madgraphDecayParticle (lheFile, decayParticleValue, madGraphDir, workingDir, numberEvents)
            
        # decay anti-particle
        madgraphDecayParticle (lheFile, decayAntiParticleValue, madGraphDir, workingDir, numberEvents)

  
    return

def mergeDecayedParticles(fileListDecay, \
                          madGraphDir, \
                          decayParticleValue, decayAntiParticleValue, \
                          undecayedFilesDir, mergedFilesDir):
    
    workDir = os.getcwd()
    
    # change to MadGraph directory, change the number of events, [FIXME put parameters]
    #     clean up if needed, then run Madgraph
    os.chdir(madGraphDir)

    for lheFile in fileListDecay:
        
        processName = processNameDef(lheFile, decayParticleValue)
        lheFileParticle = 'PROC_' + processName + '/Events/run_01/unweighted_events.lhe.gz'

        processName = processNameDef(lheFile, decayAntiParticleValue)
        lheFileAntiParticle = 'PROC_' + processName + '/Events/run_01/unweighted_events.lhe.gz'
        
        lheFileUndecayed = undecayedFilesDir + '/' + lheFile.name
        
        tmpMergedFilesDirectory = 'PROC_mergedFiles'
        if(not os.path.exists(tmpMergedFilesDirectory)):
            os.system('mkdir -p ' + tmpMergedFilesDirectory)

        processName = processNameDef(lheFile, 'merged_')
        modelCommentLine = lheFile.processPrefix + processName
        lheFileMergedName = lheFile.processPrefix + processName + '.lhe'
        lheFileMerged = tmpMergedFilesDirectory + '/' + lheFileMergedName
        
        lheMergeDecayedParticles.lheMergeDecayedParticles(lheFileParticle, lheFileAntiParticle, \
                                                          lheFileUndecayed, lheFileMerged, \
                                                          lheFile.lspGeneratedMass, lheFile.lspMass, \
                                                          modelCommentLine)
        
        # compress and copy the merged files to mergedFilesDir
        os.system('gzip -c ' + lheFileMerged + ' > ' + mergedFilesDir + '/' + lheFileMergedName + '.gz')
        
        # delete the file from the temporary directory 
        os.system('rm ' + lheFileMerged)
        
    # change back to work directory
    os.chdir(workDir)
               

#####

def runLheProduction(prodParameters):

    #
    # extract the full list of the LHE undecayed files, for all stop masses and generated LSP masses 
    # from the EOS directory (if stageUndecayedLheFiles is True) or from the local directory
    # (if stageUndecayedLheFiles is False)
        
    if not prodParameters.stageUndecayedLheFiles and prodParameters.splitUndecayedSample:
        print '\nWarning: for using already staged files, the full sample '\
            'for a mass stop value must be already staged, to get the ' \
            'correct statistics per each (stop - LSP mass) value' 
        
    fileListAllUndecayed = extractListOfFiles (prodParameters.stageUndecayedLheFiles, \
                                               prodParameters.lheUndecayedEosDirectory, \
                                               prodParameters.undecayedFilesStageDirectory, \
                                               prodParameters.undecayedFilesDirectory)
    
    #
    # extract the list of the LHE undecayed files corresponding to the given input parameters 

    #     and stage the files from EOS in the corresponding directory, if requested
    # FIXME: keep generatedLspMassLimitsStage = [-1]?
    
    if prodParameters.stageUndecayedLheFiles:
        generatedLspMassLimitsStage = [-1] 
        fileListStage = extractListOfUndecayedFiles (fileListAllUndecayed, \
                                                   prodParameters.stopMassLimits, \
                                                   generatedLspMassLimitsStage)
    
        stageLheFiles(fileListStage, prodParameters.undecayedFilesStageDirectory)
    
        # exit if staging the undecayed files was requested
        print '\n  Staging file complete. Exit as requested.'
        sys.exit(0)
    
    #     or copy them in the local job directory of undecayed files
    fileListLocalJob = extractListOfUndecayedFiles (fileListAllUndecayed, \
                                                   prodParameters.stopMassLimits, \
                                                   prodParameters.generatedLspMassLimits)
    copyLheFiles(fileListLocalJob, prodParameters.undecayedFilesDirectory)
    

    # assign to undecayed file the decay LSP mass to be used (if splitUndecayedSampleValue is True, 
    # according to the statistics fraction, otherwise loop over all requested LSP values)
    
    fileListAllLsp = assignLspMass(fileListAllUndecayed, \
                                   prodParameters.deltaMassStopLsp, prodParameters.deltaMassStopLspFractions, \
                                   prodParameters.splitUndecayedSample, \
                                   prodParameters.undecayedFilesDirectory)
    
    # list of files (with decay LSP mass defined) corresponding to the given input parameters, to be processed by MadGraph
    fileListProcess = extractListOfFilesToProcess (fileListAllLsp, \
                                                   prodParameters.stopMassLimits, prodParameters.generatedLspMassLimits, \
                                                   prodParameters.deltaMassStopLspSelected)
     
    #sys.exit('\n No MadGraph processing requested')
       
#   decay particles in MadGraph
        
    decayParticle = 'decayStop'
    decayAntiParticle = 'decayAntiStop'
    madgraphProduceDecays (fileListProcess, \
                           decayParticle, decayAntiParticle, \
                           prodParameters.madGraphDirectory, \
                           prodParameters.workDirectory, \
                           prodParameters.numberEvents)
    
    # merge undecayed files with decayed files, compress the resulting files and copy them in 
    
    if(not os.path.exists(prodParameters.mergedFilesDirectory)):
        os.system('mkdir -p ' + prodParameters.mergedFilesDirectory)
    
    mergeDecayedParticles(fileListProcess, \
                          prodParameters.madGraphDirectory, \
                          decayParticle, decayAntiParticle, \
                          prodParameters.undecayedFilesDirectory, \
                          prodParameters.mergedFilesDirectory)
       
#
# main program
# 
from datetime import datetime
print '\nJob starting time: ' + str(datetime.now()) + '\n'

jobParametersFile = 'jobParameters.' + str(sys.argv[1])
from jobParameters.runLheProduction_parameters import LheProductionParameters
lheProductionParameters = LheProductionParameters(jobParametersFile)
print lheProductionParameters

#sys.exit('\n Production parameters test only')

#
runLheProduction(lheProductionParameters)

print '\nJob ending time: ' + str(datetime.now()) + '\n'

