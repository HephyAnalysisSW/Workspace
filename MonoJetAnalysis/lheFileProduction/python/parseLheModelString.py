# parse the model string in the LHE event and return 
#     stopMass()            stop mass [GeV]
#     lspGeneratedMass()    LSP generated mass    
#     runNumber()           run number
#     lspMass()             LSP mass
#     deltaMassStopLsp()    mass difference between stop and LSP
#     processPrefix()       process prefix
#     parseLheModelString   a list of [stopMass, lspGeneratedMass, runNumber, deltaMassStopLsp, processPrefix]
#     lheFileNameUndecayed  name of the undecayed LHE file 
#     lheFileNameMerged     name of the merged LHE file

# module imports
#
import re

def stopMass(modelString):
    
    listParameters = parseLheModelString(modelString)
    stopMassValue = listParameters[1]
    return stopMassValue

def lspGeneratedMass(modelString):
    
    listParameters = parseLheModelString(modelString)
    lspGeneratedMassValue = listParameters[2]
    return lspGeneratedMassValue

def runNumber(modelString):
    
    listParameters = parseLheModelString(modelString)
    runNumberValue = listParameters[3]
    return runNumberValue

def lspMass(modelString):
    
    listParameters = parseLheModelString(modelString)
    lspMassValue = listParameters[4]
    return lspMassValue

def deltaMassStopLsp(modelString):
    
    listParameters = parseLheModelString(modelString)
    deltaMassStopLspValue = listParameters[5]
    return deltaMassStopLspValue

def processPrefix(modelString):
    
    listParameters = parseLheModelString(modelString)
    processPrefixValue = listParameters[0]
    return processPrefixValue

def parseLheModelString(modelString):
    
    listParameters = []
               
    splitModelString = modelString.split('_', 9)
    
    processPrefixValue = splitModelString[0] + '_' +  splitModelString[1] + '_' +  splitModelString[2] + '_'
    listParameters.append(processPrefixValue)
    
    stopMassValue = int(splitModelString[3])
    listParameters.append(stopMassValue)
    
    lspGenMassValue = int(splitModelString[4])
    listParameters.append(lspGenMassValue)

    matchObject = re.search(r'run(\d+)', splitModelString[5])
    runNumber = matchObject.group(1)
    listParameters.append(int(runNumber))
    
    lspMassValue = int(splitModelString[8][0:str(splitModelString[8]).find('.')])
    listParameters.append(lspMassValue)
    
    deltaMassStopLspValue = stopMassValue - lspMassValue
    listParameters.append(deltaMassStopLspValue)
    

    return listParameters


