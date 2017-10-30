""" Helper methods for physics analysis. 

"""

# imports python standard modules or functions

import sys
import os
import logging
import random
import tempfile
import math
import collections
import operator
import time
import shutil
import pickle
import pprint

# imports user modules or functions

import ROOT

import Workspace.HEPHYPythonTools.helpers as hephyHelpers

# logger
logger = logging.getLogger(__name__)   
logger.propagate = False

# functions

def getEntryList(chain, cut, newname='entryListTMP'):
    """Get the list of entries from a TTree fulfilling cut 'cut'.
    
    Use TEntryList, which needs less memory for storage and is 
    better optimized for both very high and very low selectivity of cuts.
    """
    chain.Draw('>>entryListTMP_t', cut)
    entryListTMP_t = ROOT.gROOT.Get('entryListTMP_t')
    entryListTMP = entryListTMP_t.Clone(newname)
    del entryListTMP_t
    return entryListTMP


def redirectRootPrint(rootObject):
    """ Redirect the output of ROOT Print() to a string.
    
    Solution based on:
        https://root.cern.ch/phpBB3/viewtopic.php?t=10131
    Be however careful how long is the string resulting from Print(), 
    it's loaded in memory with read() - needs enough memory for long strings
    """
    rootObjectPrint = ''
    
    save = os.dup(sys.stdout.fileno())
    sys.stdout.flush() 
    
    temporaryFile = tempfile.NamedTemporaryFile()    
    newout = file(temporaryFile.name, 'w')
    os.dup2(newout.fileno(), sys.stdout.fileno())
    
    rootObject.Print()
    rootObjectPrint = temporaryFile.read()
    
    os.dup2( save, sys.stdout.fileno() )
    newout.close()
    
    return rootObjectPrint


def getRandomList(listLength, seed=None):
    """ Randomize a list of a given length .
    
    listLength is a positive integer. The function shuffle the range [0, listLength].
    """
    if seed:
        random.seed(seed)
    listRange = range(listLength)
    random.shuffle(listRange)
    return listRange


def prettyPrintCuts(cutName, cutExpression, printUnformated=False):
    """
    Pretty-print a cut expression, separating group of cuts per line, with && and || as separators.
    
    It returns a pretty-print format only if each cut is included in parentheses,
    otherwise it return the cut expression cleaned, but not formated.
    """
    
    def parenthetic_contents(myCut):
        """Generate parenthesized contents in string as pairs (level, contents).
        
        FIXME still wrong when formatting
        """
        
        stack = []
        for indexChar, valueChar in enumerate(myCut):
            if valueChar == '(':
                stack.append(indexChar)
            elif valueChar == ')' and stack:
                start = stack.pop()
                logicalOp = ''
                numberClosePar = 0
                numberOpenPar = 0
                for iPar, iChar in enumerate(myCut[indexChar:]):
                    if iChar != ')':
                        logicalOp = myCut[indexChar + iPar + 1: indexChar + iPar + 3]
                        logicalOp = logicalOp.strip()
                        break
                    elif iChar == ')':
                        numberClosePar += 1
                        
                yield (len(stack), myCut[start + 1: indexChar], numberClosePar, logicalOp)
                
    # add spaces around logical operators, remove multiple spaces, remove spaces between parentheses
    cutExpression = cutExpression.replace('&&', ' && ')    
    cutExpression = cutExpression.replace('||', ' || ')    
    cutExpression = ' '.join(cutExpression.split())
    cutExpression = cutExpression.replace(') )', '))')
    cutExpression = cutExpression.replace('( (', '((')

    prettyCutExpression = cutName + " = " + "\n "
    
    # check if the formats of the cuts can be parsed - if not,
    # return the cut expression just cleaned, but not formated
    
    nOpenPar = cutExpression.count('(')
    nClosePar = cutExpression.count(')')
    nLogicalOp = cutExpression.count('&&') + cutExpression.count('||')
    
    if (nOpenPar != nClosePar):
        return '\nCut expression not well formated. \n' + prettyCutExpression + cutExpression 

    # cut expression well formated, return pretty format with two levels (zero and one)
    
    myCuts = parenthetic_contents(cutExpression)
    
    previousLevel = 9999
    newLevel = True

    openingPar = ['(', '((', '(((', '((((', '(((((', '((((((']
    closingPar = [')', '))', ')))', '))))', ')))))', '))))))']
    
    for cut in myCuts:
                 
        currentLevel =  cut[0]
        logicalExp = cut[1]
        numberClosePar = cut[2]
        logicalOp = cut[3]
           
        newLevel = (not newLevel if (currentLevel == 0) else newLevel)
        
        if ((currentLevel == 0) and (previousLevel != 1)):
            openPar = openingPar[0]
            closePar = closingPar[0]
            prettyCutExpression += openPar + logicalExp + closePar + ' ' + logicalOp + ' \n '
        elif ((currentLevel == 1) and ((currentLevel < previousLevel) or (previousLevel == 0))):
            openPar = (('(\n  ' + openingPar[currentLevel - 1]) if newLevel else (' ' + openingPar[currentLevel - 1]))
            closePar = closingPar[numberClosePar - 1]
            prettyCutExpression += openPar + logicalExp + closePar + ' ' + logicalOp + ' \n '
            newLevel = False
        else:
            pass
        
        previousLevel = currentLevel
    
    # FIXME remove this after you fix parenthetic_contents
    printUnformated = True
    
    #
    if printUnformated: 
        return cutExpression

    return prettyCutExpression


def rootVariableType():
    """
    ROOT machine independent data types currently supported in TTree.
    https://root.cern.ch/root/html/TTree.html
    enum EDataType
    """    
    rootVariableTypeDict = {
            'C' :    'char*',
            'B' :    'Char_t',
            'b' :    'UChar_t',
            'S' :    'Short_t',
            's' :  'UShort_t',
            'I' :     'Int_t',
            'i' :    'UInt_t',
            'L' :  'Long64_t',
            'l' : 'ULong64_t',
            'F' :   'Float_t',
            'D' :  'Double_t',
            'O' :    'Bool_t',
            }
     
     #
    return rootVariableTypeDict

def rootShortVariableType():
    """
    ROOT machine independent data types currently supported in TTree.
    https://root.cern.ch/root/html/TTree.html
    enum EDataType
    """    
    rootShortVariableTypeDict = {
        'char*':    'C',
        'Char_t':    'B',
        'UChar_t':   'b',
        'Short_t':   'S',
        'UShort_t':  's',
        'Int_t':     'I',
        'UInt_t':    'i',
        'Long64_t':  'L',
        'ULong64_t': 'l',
        'Float_t':   'F',
        'Double_t':  'D',
        'Bool_t':    'O',
        }
     
     #
    return rootShortVariableTypeDict

def getVariableName(var):
    """ Return the variable name for a root variable in the format 'name[size]/type' or 'name/type'
    
    No default for name is returned.
    """
    if var.count('/'): 
        if var.count('['):
            return var.split('[')[0]
        else:
            return var.split('/')[0]
    else:
        raise Exception("Required format: 'name[size]/type' or 'name/type'. Incorrect format for ", var)
    
    return ''
  
  
def getVariableSize(var):
    """ Return the variable size for a root variable in the format 'name[size]/type' or 'name/type'

    For 'name/type' size 1 is returned.
    """
    if var.count('['): 
        varEnd = var.split('[')[1]
        
        if varEnd.count(']'):
            varSize = varEnd.split(']')[0]
            
        return varSize
    elif var.count('/'):
        varSize = 1
        return varSize
    else:      
        raise Exception("Required format: 'name[size]/type' or 'name/type'. Incorrect format for ", var)
   
    return ''


def getVariableType(var):
    """ Return the variable type for a root variable in the format 'name[size]/type' or 'name/type'

    The format is not checked, it is assumed to be correct. No default for type.
    """
    if var.count('/'): 
        return var.split('/')[1]
    else:
        print "\n Error: the variable " + var + " is not given in the format 'name/type'"
    
    return ''


def getVariableInitializer(var):
    """ Return the variable initializer.

    It assumes a root variable in the format 'name[size]/type/initializer' or 'name/type/initializer'

    The format is not checked, it is assumed to be correct. Return None if no initializer is given..
    """
    if var.count('/') == 2:
        return var.split('/')[2]
    else:
        print "\n Error: the variable " + var + \
            " is not given in the format 'name[size]/type/initializer' or 'name/type/initializer"

    return None

def getVariableNameList(rootVarList):
    """ Return a list of variable names for a list of root variables fiven
        in the format 'name[size]/type/initializer' or 'name/type/initializer'
        
    The initializer could be omitted. 
    """
    varList = []
    for var in rootVarList:
        varName = getVariableName(var)
        varList.append(varName)
            
    # 
    return varList

  

def variablesStruct(variableList, structName='Variables'): 
    """ Produce a C structure for a variable list, having the correct ROOT type.
    
    Used to get correct float / double representation in ROOT, python uses double only.
    The input is a dictionary, key: [rootDataType, rootMiDataType], with name as key and 
    [ROOT data type, ROOT machine-independent data type] as value.
    """

    logger = logging.getLogger(__name__ + '.variablesStruct')   
    
    varList = []
    structString = " struct " + structName + " {"
    
    for var in variableList :
        varSize = (variableList[var])[2]
        if varSize == 1:
            varSizeString = ''
        elif type(varSize)==type(""):
            print "Variable with a variable size! make sure this works! ", var, varSize
            varSizeString = '[' +  str(varSize) + ']'
        elif varSize > 1:
            varSizeString = '[' +  str(varSize) + ']'
        else:
            raise Exception("\n Incorrect size for variable "+ var, varSize)
        
        varList.append((variableList[var])[1] + " " + var + varSizeString + "; ")
        
    structString += ''.join(varList) 
    structString += "};"
    
    logger.info("\n Structure for variables: \n  %s ", str(structString) + '\n')
    # 
    return structString


def getVariableValue(chain, var, indexObj=0):
    """Return the value of a variable from a chain.
    
    Check first in friends, then in the local leaves.
    """

    leaf = chain.GetAlias(var)
    if leaf != '':
        try:
            return chain.GetLeaf(leaf).GetValue(indexObj)
        except:
            raise Exception("Unsuccessful getVariableValue for leaf %s and index %i"%(leaf, indexObj))
    else:
        leaf = chain.GetLeaf(var)
        if leaf:
            return leaf.GetValue(indexObj)
      
    #  return 'nan' if no value is retrieved from leaves or aliases 
    return float('nan')


def invMass(objList, massOption=True):
    '''Compute the invariant mass of objects in a list, objects defined as dictionaries.
    
    The invariant mass is computed converting the object to TLorentzVector(), then
    using the M() function.
    
    massOption=True: 
        Object mass is included in the calculation.
        If one of the objects has no mass defined, the mass is set to 0.
       
    massOption=False:
        Mass is not included in the calculation (actually, it is considered 0
        for all objects).
    '''
    
    invMassValue = 0.
        
    sumObj = ROOT.TLorentzVector()
    for obj in objList:
        mass = obj['mass'] if (obj.has_key('mass') and massOption) else 0.
        objTLV = ROOT.TLorentzVector() 
        objTLV.SetPtEtaPhiM(obj['pt'], obj['eta'], obj['phi'], mass)
        
        sumObj += objTLV
        
    invMassValue = sumObj.M()
    
    #
    return invMassValue


def dPhi(obj1Index, obj2Index, obj1Collection, obj2Collection=None):
    ''' Compute dPhi for two objects.
    
    dPhi is computed between object index obj1Index from obj1Collection and
    object index obj2Index from obj2Collection.

    If the second collection is not given, compute dPhi between the two objects from the same collection.    
    '''
    
    if obj2Collection is None:
        dPhiValue = obj1Collection.phi[obj2Index] - obj1Collection.phi[obj1Index]
    else:
        dPhiValue = obj2Collection.phi[obj2Index] - obj1Collection.phi[obj1Index]
    
    if  dPhiValue > math.pi:
        dPhiValue -= 2.0 * math.pi
    
    if dPhiValue <= -math.pi:
        dPhiValue += 2.0 * math.pi
        
    dPhiAbsValue = abs(dPhiValue)
        
    #
    return dPhiAbsValue


def dR_alt((eta1, phi1), (eta2, phi2)):
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
    
    
def dR(obj1Index, obj2Index, obj1Collection, obj2Collection=None):
    ''' Compute dR for two objects.
    
    dR is computed between object index obj1Index from obj1Collection and
    object index obj2Index from obj2Collection.
    
    If the second collection is not given, compute dR between the two objects from the same collection.        
    '''

    dPhiValue = dPhi(obj1Index, obj2Index, obj1Collection, obj2Collection)

    if obj2Collection is None:
        dEtaValue = obj1Collection.eta[obj2Index] - obj1Collection.eta[obj1Index]        
    else:
        dEtaValue = obj2Collection.eta[obj2Index] - obj1Collection.eta[obj1Index]
    
    dRValue = math.sqrt(dPhiValue ** 2 + dEtaValue ** 2)   

    #
    return dRValue


def get_logger(logModule, logLevel, logFile):
    ''' Generic logger.
    
    '''

    # add TRACE (numerical level 5, less than DEBUG) to logging (similar to apache) 
    # see default levels at https://docs.python.org/2/library/logging.html#logging-levels
    logging.TRACE = 5
    logging.addLevelName(logging.TRACE, 'TRACE')
    
    logging.Logger.trace = lambda inst, msg, *args, **kwargs: inst.log(logging.TRACE, msg, *args, **kwargs)
    logging.trace = lambda msg, *args, **kwargs: logging.log(logging.TRACE, msg, *args, **kwargs)

    logger = logging.getLogger(logModule)

    numeric_level = getattr(logging, logLevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: %s" % logLevel)
     
    logger.setLevel(numeric_level)
     
    # create the logging file handler
    fileHandler = logging.FileHandler(logFile, mode='w')
 
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    fileHandler.setFormatter(formatter)
 
    # add handler to logger object
    logger.addHandler(fileHandler)
  
    # log the exceptions to the logger
    def excepthook(*args):
        logger.error("Uncaught exception:", exc_info=args)

    sys.excepthook = excepthook
    
        # define the named tuple to return the values
    rtuple = collections.namedtuple(
        'rtuple', 
        [
            'logger', 
            'numeric_level', 
            'fileHandler',
            ]
        )
    
    get_logger_rtuple = rtuple(
        logger, 
        numeric_level, 
        fileHandler,
        )

    #    
    return get_logger_rtuple


def retryRemove(function, path, excinfo):
    ''' Take a nap and try again.
    
    Address AFS/NSF problems with left-over lock files which prevents
    the 'shutil.rmtree' to delete the directory. The idea is to wait at most 20 sec
    for the fs to automatically remove these lock files and try again.
    Inspired from some GANGA code.
    
    '''   
    
    logger = logging.getLogger(__name__ + '.retryRemove')   
    
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
        

def evalCutOperator(quantityValue, operatorDef):
    ''' Evaluate the operator operatorDef for quantity value quantityValue.
    
    The dictionary entry for operatorDef has the following format:
        ('quantity', operator.name, quantity_cut, operator_unary_quantity)
        
        'quantity': quantity name, not used here
        operator.name: the name of the operator, from python operator module
        quantity_cut: the numerical value of the cut to be applied
        operator_unary_quantity: if given, the operator is applied on the quantity value
    '''

    logger = logging.getLogger(__name__ + '.evaluateOperator')

    opResult = False
    
    # operators with two arguments
    opForCut = operatorDef[1]
    varCut = operatorDef[2]

    if len(operatorDef) > 3:
        # apply opForVar operator on variable value
        opForVar = operatorDef[3]
        opResult = opForCut(opForVar(quantityValue), varCut)
    else:
        opResult = opForCut(quantityValue, varCut)
        
    return opResult


def getChunkIndex(sample, chunks):
    ''' Return a list of indices for a list of chunks of a given sample.
    
    '''

    chunkIndex = []

    chunkFullString = ''.join([sample['chunkString'], '_Chunk_'])

    for chunk in chunks:
        chunkIndexStr = chunk['name'].replace(chunkFullString, '')
        try:
            idx = int(chunkIndexStr)
            chunkIndex.append(idx)
        except ValueError:
            print "\n Sample: %s ".format(sample['name'])
            print "\n Unable to convert string %s to integer for chunk %s \n".format(chunkIndexStr, chunk)
            return None

    # sort the indices
    chunkIndexSorted = sorted(chunkIndex, key=int)

    return chunkIndexSorted


def getMassDictionary(sample, sample_dict_file=None):
    ''' Get the mass dictionary for a sample, if it exists.

    If a mass dictionary is retrieved, check if it is empty. 

    For samples assumed to have mass dictionary, raise an exception if the pickle file does not exist
    or the dictionary is empty. 
    '''

    logger = logging.getLogger(__name__ + '.getMassDictionary')

    # get the sample name, either as cmgName (for cmg tuples) or as name for
    # post-processed tuples

    sample_name = sample.get('cmgName', None)
    if sample_name is None:
        sample_name = sample.get('name', None)

    if sample_name is None:
        print "\n No sample name can be retrieved for sample {sample}. \nExiting.".format(
            sample=pprint.pformat(sample))
        raise Exception(
            "\n No sample name can be retrieved for sample {sample}. \nExiting.".format(
                sample=pprint.pformat(sample)
            )
        )

    mass_dict_file_sample = sample.get('mass_dict', None)

    if mass_dict_file_sample is not None:
        # if the signal path is given, replace in the mass_dict_file the path with the new one
        # (concrete case: read it from /afs post-processed instead of /data cmg tuple) 
        if sample_dict_file is not None:
            mass_dict_file = sample_dict_file
            logger.debug(
                "\n Sample mass dictionary \n %s \n replaced with \n %s \n", mass_dict_file_sample, mass_dict_file
            )
        else:
            mass_dict_file = mass_dict_file_sample
            
        if os.path.isfile(mass_dict_file):
            mass_dict = pickle.load(open(mass_dict_file, "r"))
        else:
            print "Pickle file {0} with mass dictionary for sample {1} does not exist. \nExiting.".format(
                mass_dict_file, sample_name)
            raise Exception(
                "Pickle file {0} with mass dictionary for sample {1} does not exist. \nExiting.".format(
                    mass_dict_file, sample_name
                )
            )
    else:
        print "No pickle file defined for mass dictionary of signal scan mass points {0}. \nExiting job".format(
            sample_name
        )
        raise Exception(
            "No pickle file defined for mass dictionary of signal scan mass points {0}. \nExiting job".format(
                sample_name
            )
        )

    logger.info("\n Mass dictionary: \n \n %s \n ", pprint.pformat(mass_dict))

    if len(mass_dict) == 0:
        print "Empty mass dictionary loaded from pickle file {0} for sample {1}. \nExiting job.".format(
            sample_name
        )
        raise Exception(
            "Empty mass dictionary loaded from pickle file {0} for sample {1}. \nExiting job.".format(
                sample_name
            )
        )

    #
    return mass_dict

def checkRootFile(rootFile, checkForObjects=[]):
    ''' Checks a ROOT file.

    Check: whether a root file exists, was not recovered or otherwise broken and
           if the file contains the objects in 'checkForObjects'
    https://root.cern.ch/phpBB3/viewtopic.php?t=8303 & Robert script
    '''

    if hephyHelpers.isFileOnT2(rootFile):
        from subprocess import check_output
        try:
            check_output(["gfal-ls", rootFile])
        except Exception:
            raise IOError("\n File {0} not found\n".format(rootFile))
    else:
        if not os.path.exists(rootFile):
            raise IOError("\n File {0} not found\n".format(rootFile))

    rootTFile = ROOT.TFile.Open(rootFile)

    if not rootTFile:
        raise IOError(
            "\nFile {0} could not be opened. Not a root file?".format(rootFile))

    goodFile = (not rootTFile.IsZombie()) and (not rootTFile.TestBit(ROOT.TFile.kRecovered))

    if not goodFile:
        rootTFile.Close()
        return False

    for obj in checkForObjects:
        if not rootTFile.GetListOfKeys().Contains(obj):
            rootTFile.Close()
            return False

    rootTFile.Close()

    #
    return True
