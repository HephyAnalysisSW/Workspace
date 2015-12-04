""" Helper methods for physics analysis. 

"""

# imports python standard modules or functions

import sys
import os
import logging
import random
import tempfile

# imports user modules or functions

import ROOT

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


def getRandomList(listLength):
    """ Randomize a list of a given length .
    
    listLength is a positive integer. The function shuffle the range [0, listLength].
    """
    
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
    
    if (nOpenPar != nClosePar) or (2*nLogicalOp < nOpenPar):
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
    """    
    rootVariableTypeDict = {
            'C' :    'Char_t',
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
            'o' :    'Bool_t',
            }
     
     #
    return rootVariableTypeDict


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


def variablesStruct(variableList, structName='Variables'): 
    """ Produce a C structure for a variable list, having the correct ROOT type.
    
    Used to get correct float / double representation in ROOT, python uses double only.
    The input is a dictionary, key: [rootDataType, rootMiDataType], with name as key and 
    [ROOT data type, ROOT machine-independent data type] as value.
    """
    
    varList = []
    structString = " struct " + structName + " {"
    
    for var in variableList :
        varSize = (variableList[var])[2]
        if varSize > 1:
            varSizeString = '[' +  str(varSize) + ']'
        elif varSize == 1:
            varSizeString = ''
        else:
            raise Exception("\n Incorrect size for variable "+ var, varSize)
        
        varList.append((variableList[var])[1] + " " + var + varSizeString + "; ")
        
    structString += ''.join(varList) 
    structString += "};"
    
    logging.info("\n Structure for variables: \n  %s ", str(structString) + '\n')
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

    
    
    

