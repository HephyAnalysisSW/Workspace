''' Module for CMG object selection
'''

# imports python standard modules or functions

import logging
import pprint

# imports user modules or functions
import Workspace.DegenerateStopAnalysis.tools.helpers as helpers

# logger
logger = logging.getLogger(__name__)   

# classes and functions


class cmgObject():
    ''' Class for CMG objects.
    
    '''
    
    logger = logging.getLogger(__name__ + '.cmgObject')   

    def __init__(self, readTree, splitTree, obj, varList=[]):
        self.readTree = readTree  
        self.splitTree = splitTree
        self.obj = obj
        if readTree is not None:
            self.nObj = cmgObjLen(readTree, obj)


    def __getattr__(self, name):
        var = cmgObjVar(self.readTree, self.obj, name)
        return var

    def __ge__(self, y):
        raise Exception("cmgObject can't be compared. Item index is probably missing")
    def __gt__(self, y):
        raise Exception("cmgObject can't be compared. Item index is probably missing")
    def __le__(self, y):
        raise Exception("cmgObject can't be compared. Item index is probably missing")
    def __lt__(self, y):
        raise Exception("cmgObject can't be compared. Item index is probably missing")
    def __eq__(self, y):
        raise Exception("cmgObject can't be compared. Item index is probably missing")

    
    def getPassFailList(self, readTree , selectorFunc, objPassFailList=None): 
        """Outputs a list of of True/False depending on whether object pass or fail the SelectorFunc.
        
        SelectorFunc should take readTree, cmgObject instance and object index.
        
        If another PassFailList is given as input,  it will evaluate SelectorFunc only 
        for the indices which are True in objPassFailList, instead of looping over the entire collection.
        """

        logger = logging.getLogger(__name__ + '.cmgObject' + '.getPassFailList')   

        passFailList = []
        
        if not objPassFailList:
            # loop over all objs in the collection, if no list is given as input
            objList = enumerate(range(self.nObj))
        else:
            if len(objPassFailList) == self.nObj:
                objList = enumerate(objPassFailList)
            else:
                objList = enumerate([i in objPassFailList  for i in range(self.nObj) ])

        for iObj , passed in objList:   
            if passed is False :
                passFailList.append(False)
                continue
            passFailList.append(selectorFunc(readTree, self, iObj))
            
        return passFailList

    def getIndexList(self, passFailList):
        return getIndexList(passFailList)

    
    def sort(self, key, indexList):
        ''' Sort a list of objects given as indices in indexList according to key.
        
        Return a list of object indices.
        '''
        
        logger = logging.getLogger(__name__ + '.cmgObject' + '.sort')   

        #
        
        indexListSort = []
        
        if not indexList: 
            return indexListSort
        
        keyIndexList = []
        for ind in indexList:
            keyValue = cmgObjVar(self.readTree, self.obj, key)[ind]
            keyIndexList.append([keyValue, ind])
            
        keyIndexListSort = sorted(keyIndexList, key=lambda tup: tup[0], reverse=True)
        
        for tup in keyIndexListSort:
            indexListSort.append(tup[1])
        
        logger.trace(
            "\n List of indices, before sorting after key %s: \n" + pprint.pformat(indexList) + \
            "\n Unsorted list: \n" + pprint.pformat(keyIndexList) + \
            "\n Sorted list: \n" + pprint.pformat(keyIndexListSort) + \
            "\n List of indices, after %s sorting: \n" + pprint.pformat(indexListSort) + "\n",
            key, key
            )
        
        return indexListSort
    

    def getSelectionIndexList(self, readTree , selectorFunc, objPassFailList=None): 
        """Outputs a list of indices of the objects that have passed the selectorFunc.
        
        SelectorFunc should take readTree, cmgObject instance and object index.
        
        If another PassFailList is given as input,  it will evaluate SelectorFunc only 
        for the indices which are True in objPassFailList, instead of looping over the entire collection.
        
        TODO modify the getSelectionIndexList to take as input a list of indices, instead of 
        a PassFailList.

        """
        return getIndexList(self.getPassFailList(readTree, selectorFunc, objPassFailList=objPassFailList))
    

    def splitIndexList(self, var, varCutValue, indexList=[]):
        ''' Split a list of object indices in two lists, for a given variable and the corresponding cut value.  
        
        Test the value of the variable for the corresponding index, put the index in the indexListHigh if 
        the value is higher than the cut value, otherwise put the index in indexListLow.
        Return the two list of indices.
        '''
        
        indexListLow = []
        indexListHigh = []
        
        for ind in indexList:
            varValue = cmgObjVar(self.readTree, self.obj, var)[ind]
            

            if varValue > varCutValue:
                indexListHigh.append(ind)
            else:
                indexListLow.append(ind)
        
        return indexListLow, indexListHigh
    
    
    def getObjDictList(self, varList, indexList):
        ''' Create a list of objects as dictionaries for variables from varList, for objects with indices in indexList.
        
        '''

        objDictList = []
                
        for ind in indexList:
            objDict = {var: cmgObjVar(self.readTree, self.obj, var)[ind] for var in varList}
            objDictList.append(objDict)
            
        return objDictList
    
    def getAllObjBranches(self):
        ''' Create a list of all branches existing in splitTree.
        
        '''

        treeBranches = self.splitTree.GetListOfBranches()
        typeDict = helpers.rootShortVariableType()

        objBranchList = []
        objBranchNameType = []
        
        for i in range(treeBranches.GetEntries()):
            branchName = treeBranches.At(i).GetName()
            
            branchType = treeBranches.At(i).GetClassName()
            if not branchType:
                branchType = treeBranches.At(i).GetListOfLeaves()[0].GetTypeName()
                
                
            branchNameType = branchName + '/' + typeDict[branchType]
            if branchName.startswith(self.obj):
                objBranchList.append(branchName)
                objBranchNameType.append(branchNameType)
                
        logger.trace(
            "\n List of all branches for object %s \n %s \n\n  List of branches and type \n %s",
            self.obj, pprint.pformat(objBranchList), pprint.pformat(objBranchNameType)
            )

        return objBranchList, objBranchNameType

    def printObjects(self, indexList=[], varList=[]):
        ''' Print for each object from indexList the values of variables from varList.
        
        If the indexList is not given, it will print all objects from the collection.
        '''

        logger = logging.getLogger(__name__ + '.cmgObject' + '.printObjects')   
                    
        objBranchList, objBranchNameType = self.getAllObjBranches()
        
        varListCurrent = []
        for var in varList:
            branchName = self.obj + '_' + var
            if branchName in objBranchList:
                varListCurrent.append(var)

        logger.trace(
            "\n List of variables to print for object %s \n %s \n",
            self.obj, pprint.pformat(varListCurrent)
            )

        printStr = ''
        
        if indexList == None:
            printStr += "\n Number of {0} objects: {1} \n".format(self.obj, self.nObj)
            indexList = list(range(self.nObj))
        else:
            printStr += "\n Number of selected {0} objects: {1} \n".format(self.obj, len(indexList))

        for ind in indexList:
            printStr += "\n + " + self.obj + " object index: " + str(ind) + '\n'
            logger.trace(printStr)
            for var in varListCurrent:
                varValue = cmgObjVar(self.readTree, self.obj, var)[ind]
                varName = self.obj + '_' + var
                printStr += varName + " = " + str(varValue) + '\n'
            printStr += '\n'

        #
        return printStr
        


def getIndexList(passFailList):
    indexList = []
    for ix, x in enumerate(passFailList):
        if x:
            indexList.append(ix)
    return indexList

def cmgObjVar(readTree, obj, var):                
    return getattr(readTree, "%s_%s" % (obj, var))


def cmgObjLen(readTree, obj):
    return getattr(readTree, "n%s" % obj)


def cmgLeaf(readTree, obj, var):                
    leaf = readTree.GetLeaf("%s_%s" % (obj, var))
    return

class Leaf:
    def __init__(self, readTree, obj, var):
        self.leaf = readTree.GetLeaf("%s_%s" % (obj, var))
    def __getitem__(self, name):
        return self.leaf.GetValue(name)


def objSelectorFunc(objSel):
    '''Object selection for cuts given in a dictionary.
        
    The format of the dictionary for objSelector function is
    
        objSel = {
        'set_name': {
            'cut_name': ('variable_name', operator, cut_value),
            'cut_name1': ('variable_name', operator, cut_value, operator_on_variable),
            },
        }

    Multiple cut_name can be given, and multiple set_name can be defined.
    For operators, use the python standard module "operator" https://docs.python.org/2/library/operator.html
    
    For cut_name with complex expression (e.g. hyb_iso) a dedicated function must be defined separately, see hyb_iso
    implementation. The format of the dictionary depends on the deduicated function implementation.
    '''
        
    def hybIso(readTree, obj, objIndex, objSel):
        ''' Hybrid isolation function for muons
        
        '''
        
        objSelHybIso = objSel['hybIso']
        
        objSel_ptSwitch = objSelHybIso['ptSwitch']
        
        objSel_relIso_cut = objSelHybIso['relIso']['cut']
        objSel_relIso_type = objSelHybIso['relIso']['type']
        
        objSel_absIso = objSelHybIso['absIso']
        
        obj_pt = obj.pt[objIndex]
        obj_reIso = getattr(obj, objSel_relIso_type)[objIndex]
        
        passCut = False
                       
        if obj_pt < objSel_ptSwitch:
            if (obj_reIso * obj_pt < objSel_absIso):
                passCut = True
        else:
            if (obj_reIso < objSel_relIso_cut):
                passCut = True

        # 
        return passCut


    def elWP(readTree, obj, objIndex, objSel):
        ''' Supplementary electron selection for a working point.
        
        '''
        
        # get once the values for the key and eta, to speed up the code
        elWPSel = objSel['elWP']
        elWPSelVars = elWPSel['vars']
        
        elWP_eta_EB = elWPSel['eta_EB']
        elWP_eta_EE = elWPSel['eta_EE']
        
        objEta = abs(obj.eta[objIndex])
        
        def cut_EB_EE(obj, varName, objIndex, elWPSelVars):
            
            elWPSelVars_var = elWPSelVars[varName]
            opVar = elWPSelVars_var['opVar']
            opCut = elWPSelVars_var['opCut']

            varValue = getattr(obj, varName)[objIndex] 
            if opVar is not None:
                varValue = opVar(varValue)
             
            passCut = False
                       
            if objEta <= elWP_eta_EB:
                if opCut(varValue, elWPSelVars_var['EB']):
                    passCut = True
            elif ((elWP_eta_EB < objEta) and (objEta < elWP_eta_EE)):
                if opCut(varValue, elWPSelVars_var['EE']):
                    passCut = True
            else:
                # for eta outside ['eta_EB', 'eta_EE'] range, set it to False
                passCut = False
                

            # 
            return passCut
               
        # evaluate each cut, exit if False immediately
        for var in elWPSelVars:
            if not cut_EB_EE(obj, var, objIndex, elWPSelVars):
                return False
        
        #
        return True
     
        
    def objSelector(readTree, obj, objIndex):
        
        selector = True
            
        for key, keyValue in objSel.iteritems(): 
            
            if key == 'hybIso':
                selector &= hybIso(readTree, obj, objIndex, objSel)
            elif key == 'elWP':
                selector &= elWP(readTree, obj, objIndex, objSel)                
            else:
                varValue = getattr(obj, keyValue[0])[objIndex]
            
                # operators with two arguments
                opCut = keyValue[1]
                varCut = keyValue[2]
            
                if len(keyValue) > 3:
                    # apply opVar operator on variable value
                    opVar = keyValue[3]
                    selector &= opCut(opVar(varValue), varCut)
                else:
                    selector &= opCut(varValue, varCut)
                    
            #
            if not selector:
                break
            
        return selector

    return objSelector
    
