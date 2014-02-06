# select from the list of merged files the files up to a given statistics,
# such that one has minimum overlap of the original undecayed files 
# 
# for simplicity, assume a constant number of events per file nrEventsPerFile

# module imports
#
import sys
import imp

from LheFile import LheFile
import parseLheModelString

# module arguments
#
lheFiles = str(sys.argv[1])
statisticsPerPoint = int(sys.argv[2])
stopMassLowLimit = int(sys.argv[3])
stopMassHighLimit = int(sys.argv[4])
selectedLheFiles = str(sys.argv[5])

print '\nInput file:                           ', lheFiles
print 'Statistics per (stop mass, LSP mass):   ', statisticsPerPoint
print 'Low stop mass limit:                    ', stopMassLowLimit
print 'High stop mass limit:                   ', stopMassHighLimit
print 'File to save list of selected LHE file: ', selectedLheFiles

# module constant parameters 
#
nrEventsPerFile = 100000

deltaMassStopLspList = [10, 20, 30, 40, 50, 60, 70, 80]

# data directory for merged LHE files: dataDirRead  - source on SE, dataDirWrite  - destination
dataLheSet='T2tt_stopMass_0_500'
dataDirRead='/T2tt/stop_stop/output/' + dataLheSet + '_mergedFiles'   
dataDirWrite='/T2tt/stop_stop' + '/modifiedHeader/' + dataLheSet + '_mergedFiles'


def loopFileList(fileListLheLF, \
                 stopMassLF, lspMassLF, lspGeneratedMassLF, runNumberLF, \
                 listUsedUndecayedLheFileLF, \
                 nrEventsPointLF, \
                 selectedLheFilesObj, \
                 statisticsPerPointLF):
          
    for lheFile in fileListLheLF:
            
        stopMassValue = lheFile.stopMass
        if stopMassValue == stopMassLF:
            
            lspMassValue = lheFile.lspMass
            if lspMassValue == lspMassLF:
            
                lspGeneratedMassValue = lheFile.lspGeneratedMass
                if lspGeneratedMassValue == lspGeneratedMassLF:
                    
                    runNumberValue = lheFile.runNumber
                    if runNumberValue == runNumberLF:
                        
                        # skip undecayed LHE files already used
                        if [stopMassLF, lspGeneratedMassLF, runNumberLF] in listUsedUndecayedLheFileLF:
                            continue
                        
                        lheFileNrEvents = lheFile.nrEvents
                        if (lheFileNrEvents > 0):
                            
                            nrEventsPointLF += lheFileNrEvents
                            
                            if nrEventsPointLF > statisticsPerPointLF:
                                break
    
                            listUsedUndecayedLheFileLF.append([stopMassLF, lspGeneratedMassLF, runNumberLF])
                            selectedLheFilesObj.write(lheFile.name + '\n')
                        
                            print '  ', lheFile.name
                            print '   stop mass = ', stopMassLF, ' lspMass = ', lspMassLF, \
                                ' lspGeneratedMass = ', lspGeneratedMassLF, 'runNumber = ', runNumberLF, \
                                ' nrEventsPoint = ', nrEventsPointLF, '\n'
        
                                
    return nrEventsPointLF
    


# assign to each entry from lheFileObj the decay LSP mass to be used, according to 
# the statistics fraction if splitUndecayedSample is True
 
# get a set of unique, sorted values of stop masses, generated LSP masses, run numbers, 
# decayed LSP masses from the LHE files,

stopMassValuesUnsorted = set()
lspGeneratedMassValuesUnsorted = set()
runNumberValuesUnsorted = set()
lspMassValuesUnsorted = set()

nrEventsPerStopMass = dict()
nrFilesPerStopMass = dict()

fileListLhe = []   

lheFileObj =  open(lheFiles, 'r')       
selectedLheFilesObj = open(selectedLheFiles, 'a')       

for fileLine in lheFileObj:
    
    lheFile = fileLine[fileLine.find('8TeV'):].rstrip('\n')
    
    fullNameValue = lheFile
    nameValue = lheFile
    
    stopMassValue = parseLheModelString.stopMass(lheFile)  
    stopMassValuesUnsorted.add(stopMassValue)
  
    lspGeneratedMassValue = parseLheModelString.lspGeneratedMass(lheFile)
    lspGeneratedMassValuesUnsorted.add(lspGeneratedMassValue)
    
    runNumberValue = parseLheModelString.runNumber(lheFile)    
    runNumberValuesUnsorted.add(runNumberValue)
    
    lspMassValue = parseLheModelString.lspMass(lheFile)   
    lspMassValuesUnsorted.add(lspMassValue)

    processPrefixValue = parseLheModelString.processPrefix(lheFile)   
    lheFileNrEvents = nrEventsPerFile

    lheFileNew = LheFile(fullNameValue, nameValue, \
                        stopMassValue, lspGeneratedMassValue, \
                        runNumberValue, \
                        lspMassValue, processPrefixValue, lheFileNrEvents)
   
    fileListLhe.append(lheFileNew)    
 
stopMassValues = sorted(stopMassValuesUnsorted) 
lspGeneratedMassValues = sorted(lspGeneratedMassValuesUnsorted) 
runNumberValues = sorted(runNumberValuesUnsorted) 
lspMassValues = sorted(lspMassValuesUnsorted) 
                
lheFileObj.close()

print '\nNumber of existing stop mass bins: ', len(stopMassValues), '\n'

for stopMass in stopMassValues:
    
    if stopMass < stopMassLowLimit:
        continue

    if stopMass > stopMassHighLimit:
        break
    
    listUsedUndecayedLheFile = []
    
    for lspMass in lspMassValues:
        
        deltaMassStopLsp = stopMass - lspMass
        if deltaMassStopLsp not in deltaMassStopLspList:
            continue
        
        print '\nBegin loop: stop mass = ', stopMass, ' lspMass = ', lspMass, '( deltaMassStopLsp = ', deltaMassStopLsp,  ')\n'

        nrEventsPoint = 0
        nrEventsKeptPoint = 0

        while nrEventsPoint < statisticsPerPoint:
        
            for lspGeneratedMass in lspGeneratedMassValues:
                for runNumber in runNumberValues:

                    nrEventsKeptPoint = nrEventsPoint
                    
                    nrEventsPoint = loopFileList(fileListLhe, \
                                        stopMass, lspMass, lspGeneratedMass, runNumber, \
                                        listUsedUndecayedLheFile, \
                                        nrEventsPoint, \
                                        selectedLheFilesObj, \
                                        statisticsPerPoint)
                           
                    if nrEventsPoint > statisticsPerPoint:
                        print '\n        Break run loop'
                        break
                if nrEventsPoint > statisticsPerPoint:
                    print '        Break lspGeneratedMass loop'
                    break

            if nrEventsPoint > statisticsPerPoint:
                print '        Break while loop'
                break
            else:
                listUsedUndecayedLheFile = []
                

        print '\n  Number of events for stop mass = ', stopMass, ' lspMass = ', lspMass, '( deltaMassStopLsp = ', deltaMassStopLsp, \
             '): ', nrEventsKeptPoint, ' events'
            
 
selectedLheFilesObj.close() 


print '\nEnd of job'
 
           