''' Module for CMG object selection
'''

# imports python standard modules or functions

import logging
import pprint
from math import *

# imports user modules or functions

from Workspace.HEPHYPythonTools.helpers import findClosestObject, deltaR, deltaR2, getVarValue, getObjFromFile, getObjDict

# logger
logger = logging.getLogger(__name__)   

# classes and functions


class cmgObject():
    ''' Class for CMG objects.
    
    '''
    
    logger = logging.getLogger(__name__ + '.cmgObject')   

    def __init__(self, readTree, splitTree, obj , varList=[]):
        self.nObj = cmgObjLen(readTree, obj)
        self.obj = obj
        self.readTree = readTree  
        self.splitTree = splitTree

        # def getattr(self, name, tree= readTree):
        #    return cmgObjVar(readTree, self.obj, name)        

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
    
    # def sort(self, readTree, key, objList):
    #    pass       

    

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
    

    def printObjects(self, indexList=[], varList=[]):
        ''' Print for each object from indexList the values of variables from varList.
        
        If the indexList is not given, it will print all objects from the collection.
        FIXME
        '''

        logger = logging.getLogger(__name__ + '.cmgObject' + '.printObjects')   
                    
        treeBranches = self.splitTree.GetListOfBranches()

        objBranchList = []
        for i in range(treeBranches.GetEntries()):
            branchName = treeBranches.At(i).GetName()
            if branchName.startswith(self.obj):
                objBranchList.append(branchName)
            
        logger.trace(
            "\n List of all branches for object %s \n %s \n",
            self.obj, pprint.pformat(objBranchList)
            )

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


def lepSelectorFuncOld(lepSel):
    muSel = lepSel["mu"] if lepSel.has_key("mu") else None
    elSel = lepSel["el"] if lepSel.has_key("el") else None

    def lepSelector(readTree, lep, i):
        if muSel and (abs(lep.pdgId[i]) == muSel['pdgId']): 
            if muSel.has_key('pt') : 
                if not (lep.pt[i] > muSel['pt']):  
                    # print lep.pt[i]
                    return False
            if muSel.has_key('ptMax') : 
                if not (lep.pt[i] < muSel['ptMax']):  
                    # print lep.pt[i]
                    return False
            if muSel.has_key('eta') : 
                if not abs(lep.eta[i]) < muSel['eta']: 
                    # print lep.eta[i]
                    return False
            if muSel.has_key('dxy') : 
                if not abs(lep.dxy[i]) < muSel['dxy']: 
                    # print lep.dxy[i]
                    return False
            if muSel.has_key('dz') : 
                if not abs(lep.dz[i]) < muSel['dz']: 
                    # print lep.dz[i]
                    return False
            if muSel.has_key('sip3d') : 
                if not lep.sip3d[i] < muSel['sip3d'] : 
                    # print lep.sip3d[i]
                    return False
            if muSel.has_key('mediumMuonId') : 
                if not lep.mediumMuonId[i] == muSel['mediumMuonId']: 
                    # print lep.mediumMuonId[i]
                    return False
            if muSel.has_key('hybIso') : 
                if not ((lep.pt[i] >= muSel['hybIso']['ptSwitch'] and lep.relIso04[i] < muSel['hybIso']['relIso']) \
                or (lep.pt[i] < muSel['hybIso']['ptSwitch']  and lep.relIso04[i] * lep.pt[i] < muSel['hybIso']['absIso'])): 
                    # print lep.pt, lep.relIso04, 
                    return False
            #
            return True
        elif elSel and (abs(lep.pdgId[i]) == elSel['pdgId']): 
            if elSel.has_key('pt') : 
                if not (lep.pt[i] > elSel['pt']):  
                    # print lep.pt[i]
                    return False
            if elSel.has_key('ptMax') : 
                if not (lep.pt[i] < elSel['ptMax']):  
                    # print lep.pt[i]
                    return False
            if elSel.has_key('eta') : 
                if not abs(lep.eta[i]) < elSel['eta']: 
                    # print lep.eta[i]
                    return False
            if elSel.has_key('dxy') : 
                if not abs(lep.dxy[i]) < elSel['dxy']: 
                    # print lep.dxy[i]
                    return False
            if elSel.has_key('dz') : 
                if not abs(lep.dz[i]) < elSel['dz']: 
                    # print lep.dz[i]
                    return False
            if elSel.has_key('sip3d') : 
                if not lep.sip3d[i] < elSel['sip3d'] : 
                    # print lep.sip3d[i]
                    return False
            if elSel.has_key('SPRING15_25ns_v1') : 
                if not abs(lep.SPRING15_25ns_v1[i]) > elSel['SPRING15_25ns_v1']: 
                    # print lep.SPRING15_25ns_v1[i]
                    return False
            #
            return True
        else:
            # print "Lep Selector Fail", lep.pdgId[i], lep.pt[i]
            # assert False
            return False 

    return lepSelector


                
def jetSelectorFuncOld(jetSel):
    def jetSelector(readTree, jet, i):
        if jetSel: 
            if jetSel.has_key('pt') : 
                if not (jet.pt[i] > jetSel['pt']):  
                    # print jet.pt[i]
                    return False
            if jetSel.has_key('ptMax') : 
                if not (jet.pt[i] < jetSel['ptMax']):  
                    # print jet.pt[i]
                    return False
            if jetSel.has_key('eta') : 
                if not abs(jet.eta[i]) < jetSel['eta']: 
                    # print jet.eta[i]
                    return False
            if jetSel.has_key('id') :  # non-standard operator >=
                if not abs(jet.id[i]) >= jetSel['id']: 
                    # print jet.id[i]
                    return False
            if jetSel.has_key('btag') : 
                if jetSel['btag'] == 'btagCSV':
                    if not jet.btagCSV[i] > jetSel['cutDiscriminator']: 
                        # print jet.btagCSV[i]
                        return False
                else:
                    raise Exception("\n No comparison operator defined for " + jetSel['btag'])

            #
            return True

    return jetSelector


def objSelectorFunc(objSel):
    '''Object selection for cuts given in a dictionary.
        
    The format of the dictionary is
    
        objSel = {
        'set_name': {
            'cut_name': ('variable_name', operator, cut_value),
            'cut_name1': ('variable_name', operator, cut_value, operator_on_variable),
            },
        }

    Multiple cut_name can be given, and multiple set_name can be defined.
    For operators, use the python standard module "operator" https://docs.python.org/2/library/operator.html
    
    For cut_name with complex expression (e.g. hyb_iso) a function must be defined separately, see hyb_iso
    implementation.
    '''
        
    def hybIso(readTree, obj, i, objSel):
        ''' Hybrid isolation function for muons
        
        '''
        
        if not (
            (obj.pt[i] >= objSel['hybIso']['ptSwitch'] and obj.relIso04[i] < objSel['hybIso']['relIso'])
            or 
            (obj.pt[i] < objSel['hybIso']['ptSwitch']  and obj.relIso04[i] * obj.pt[i] < objSel['hybIso']['absIso'])
            ):
            
            return False
        #
        return True 

        
    def objSelector(readTree, obj, i):
        
        selector = True
            
        for key, keyValue in objSel.iteritems(): 
            
            if key == 'hybIso':
                selector &= hybIso(readTree, obj, i, objSel)
            else:
                varValue = getattr(obj, keyValue[0])[i]
            
                # operators with two arguments
                operat = keyValue[1]
                varCut = keyValue[2]
            
                if len(keyValue) > 3:
                    # apply varOperat operator on variable value
                    varOperat = keyValue[3]
                    selector &= operat(varOperat(varValue), varCut)
                else:
                    selector &= operat(varValue, varCut)
                    
            #
            if not selector:
                break
            
        return selector

    return objSelector
    
    
###############################################################################################
#######################################                    ####################################
#######################################   OLD FUNCTIONS    ####################################
#######################################                    ####################################
###############################################################################################


def isGoodLepton(lep, ptCut=5, etaCut = 2.4, hybridIso04={"ptSwitch":25,"relIso":0.2,'absIso':5} , dzCut=0.2 , dxyCut=0.05 ,sip3dCut=4.0 ):
  if abs(lep['pdgId'])==13:
    if lep['mediumMuonId']==1 and abs(lep['dz'])<dzCut and abs(lep['dxy']) < dxyCut and lep['sip3d'] < sip3dCut and lep['pt'] > ptCut and abs(lep['eta']) < etaCut and hybridIso04ID(lep):
      return True
    else: return False
  elif abs(lep['pdgId'])==11:
    return False

def isGoodLepFunc(ptCut=5, ptMax=999999 ,etaCut = 2.4, hybridIso04={"ptSwitch":25,"relIso":0.2,'absIso':5} , dzCut=0.2 , dxyCut=0.05 ,sip3dCut=4.0):
    def isGoodLepton(lep, ptCut=ptCut, etaCut=etaCut, hybridIso04=hybridIso04, dzCut=dzCut, dxyCut=dxyCut, sip3dCut=sip3dCut ):
        if abs(lep['pdgId'])==13:
          if lep['mediumMuonId']==1 and abs(lep['dz'])<dzCut and abs(lep['dxy']) < dxyCut and lep['sip3d'] < sip3dCut and lep['pt'] > ptCut and lep['pt'] < ptMax and abs(lep['eta']) < etaCut and hybridIso04ID(lep):
            return True
          else: return False
        elif abs(lep['pdgId'])==11:
          return False
    return isGoodLepton

isGoodLepton30 = isGoodLepFunc(ptMax=30)



def hybridIso04ID(lep,hybridIso04={"ptSwitch":25,"relIso":0.2,'absIso':5}):
  return (lep["pt"]>=hybridIso04['ptSwitch'] and lep["relIso04"]<hybridIso04['relIso']) or (lep["pt"]<hybridIso04['ptSwitch'] and lep["relIso04"]*lep["pt"]<hybridIso04['absIso'])



def cmgLooseLepID(readTree, nLep, ptCuts, absEtaCuts, ele_MVAID_cuts,lepton="LepGood"):
  if lepton=="LepGood":
    if abs(readTree.LepGood_pdgId[nLep])==11: return cmgLooseEleID(readTree, nLep=nLep, ptCut=ptCuts[0], absEtaCut=absEtaCuts[0], ele_MVAID_cuts=ele_MVAID_cuts,lepton=lepton)
    elif abs(readTree.LepGood_pdgId[nLep])==13: return cmgLooseMuID(readTree, nLep=nLep, ptCut=ptCuts[1], absEtaCut=absEtaCuts[1],lepton=lepton)
  elif lepton=="LepOther":
    if abs(readTree.LepOther_pdgId[nLep])==11: return cmgLooseEleID(readTree, nLep=nLep, ptCut=ptCuts[0], absEtaCut=absEtaCuts[0], ele_MVAID_cuts=ele_MVAID_cuts,lepton=lepton)
    elif abs(readTree.LepOther_pdgId[nLep])==13: return cmgLooseMuID(readTree, nLep=nLep, ptCut=ptCuts[1], absEtaCut=absEtaCuts[1],lepton=lepton)


#def cmgTrackIndices(r, ptCuts=1, absEtaCuts=(2.5,2.4), , nMax=300 ):
#  return [i for i in range(min(nMax,r.ntrack) ) if cmgTrackID(r,nTrk=i) ]





#def hybridIso03ID(r, nLep, hybridIso03):
#  return (r.LepGood_pt[nLep]>=hybridIso03['ptSwitch'] and r.LepGood_relIso03[nLep]<hybridIso03['relIso']) or (r.LepGood_pt[nLep]<hybridIso03['ptSwitch'] and r.LepGood_relIso03[nLep]*r.LepGood_pt[nLep]<hybridIso03['absIso'])
#  
   
#def hybridIso04ID(r, nLep, hybridIso04={"ptSwitch":25,"relIso":0.2,'absIso':5}):
#  if lepton=="LepGood":
#    return (r.LepGood_pt[nLep]>=hybridIso04['ptSwitch'] and r.LepGood_relIso04[nLep]<hybridIso04['relIso']) or (r.LepGood_pt[nLep]<hybridIso04['ptSwitch'] and r.LepGood_relIso04[nLep]*r.LepGood_pt[nLep]<hybridIso04['absIso'])
#  if lepton=="LepOther":
#    return (r.LepOther_pt[nLep]>=hybridIso04['ptSwitch'] and r.LepOther_relIso04[nLep]<hybridIso04['relIso']) or (r.LepOther_pt[nLep]<hybridIso04['ptSwitch'] and r.LepOther_relIso04[nLep]*r.LepOther_pt[nLep]<hybridIso04['absIso'])

def ele_ID_eta(r,nLep,ele_MVAID_cuts):
  if abs(r.LepGood_eta[nLep]) < 0.8 and r.LepGood_mvaIdPhys14[nLep] > ele_MVAID_cuts['eta08'] : return True
  elif abs(r.LepGood_eta[nLep]) > 0.8 and abs(r.LepGood_eta[nLep]) < 1.44 and r.LepGood_mvaIdPhys14[nLep] > ele_MVAID_cuts['eta104'] : return True
  elif abs(r.LepGood_eta[nLep]) > 1.57 and r.LepGood_mvaIdPhys14[nLep] > ele_MVAID_cuts['eta204'] : return True
  return False



 
#def cmgLooseMuID(r, nLep, ptCut, absEtaCut, hybridIso03):
#  return r.LepGood_pt[nLep]>=ptCut and abs(r.LepGood_eta[nLep])<absEtaCut and hybridIso03ID(r,nLep,hybridIso03)

def cmgLooseMuID(r, nLep, ptCut, absEtaCut,lepton="LepGood"):
  return r.LepGood_mediumMuonId[nLep]==1 and r.LepGood_miniRelIso[nLep]<0.4 and r.LepGood_sip3d[nLep]<4.0 and r.LepGood_pt[nLep]>=ptCut and abs(r.LepGood_eta[nLep])<absEtaCut

#def cmgLooseEleID(r, nLep, ptCut, absEtaCut):
#  return r.LepGood_pt[nLep]>=ptCut and abs(r.LepGood_eta[nLep])<absEtaCut and hybridIso03ID(r,nLep,hybridIso03)

def cmgLooseEleID(r, nLep, ptCut , absEtaCut, ele_MVAID_cuts,lepton="LepGood"):
  if lepton=="LepGood":
    return r.LepGood_pt[nLep]>=ptCut and (abs(r.LepGood_eta[nLep])   <1.44 or abs(r.LepGood_eta[nLep])>1.57) and abs(r.LepGood_eta[nLep])<absEtaCut and r.LepGood_miniRelIso[nLep]<0.4 and ele_ID_eta(r,nLep,ele_MVAID_cuts) and r.LepGood_lostHits[nLep]<=1 and r.LepGood_convVeto[nLep] and r.LepGood_sip3d[nLep] < 4.0 
  if lepton=="LepOther":
    return r.LepOther_pt[nLep]>=ptCut and (abs(r.LepOther_eta[nLep]) <1.44 or abs(r.LepOther_eta[nLep])>1.57) and abs(r.LepOther_eta[nLep])<absEtaCut and r.LepOther_miniRelIso[nLep]<0.4 and ele_ID_eta(r,nLep,ele_MVAID_cuts) and r.LepOther_lostHits[nLep]<=1 and r.LepOther_convVeto[nLep] and r.LepOther_sip3d[nLep] < 4.0 

#def cmgLooseLepID(r, nLep, ptCuts, absEtaCuts, hybridIso03):
#  if abs(r.LepGood_pdgId[nLep])==11: return cmgLooseEleID(r, nLep=nLep, ptCut=ptCuts[0], absEtaCut=absEtaCuts[0],hybridIso03=hybridIso03)
#  elif abs(r.LepGood_pdgId[nLep])==13: return cmgLooseMuID(r, nLep=nLep, ptCut=ptCuts[1], absEtaCut=absEtaCuts[1],hybridIso03=hybridIso03)

def cmgLooseLepID(r, nLep, ptCuts, absEtaCuts, ele_MVAID_cuts,lepton="LepGood"):
  if lepton=="LepGood":
    if abs(r.LepGood_pdgId[nLep])==11: return cmgLooseEleID(r, nLep=nLep, ptCut=ptCuts[0], absEtaCut=absEtaCuts[0], ele_MVAID_cuts=ele_MVAID_cuts,lepton=lepton)
    elif abs(r.LepGood_pdgId[nLep])==13: return cmgLooseMuID(r, nLep=nLep, ptCut=ptCuts[1], absEtaCut=absEtaCuts[1],lepton=lepton)
  elif lepton=="LepOther":
    if abs(r.LepOther_pdgId[nLep])==11: return cmgLooseEleID(r, nLep=nLep, ptCut=ptCuts[0], absEtaCut=absEtaCuts[0], ele_MVAID_cuts=ele_MVAID_cuts,lepton=lepton)
    elif abs(r.LepOther_pdgId[nLep])==13: return cmgLooseMuID(r, nLep=nLep, ptCut=ptCuts[1], absEtaCut=absEtaCuts[1],lepton=lepton)

#def cmgLooseLepIndices(r, ptCuts=(7.,5.), absEtaCuts=(2.4,2.1), hybridIso03={'ptSwitch':25, 'absIso':7.5, 'relIso':0.3}, nMax=8):
#  return [i for i in range(min(nMax, r.nLepGood)) if cmgLooseLepID(r, nLep=i, ptCuts=ptCuts, absEtaCuts=absEtaCuts, hybridIso03=hybridIso03) ]

def cmgLooseLepIndices(r, ptCuts=(7.,5.), absEtaCuts=(2.5,2.4),ele_MVAID_cuts = {'eta08':0.35 , 'eta104':0.20,'eta204': -0.52} , nMax=8,lepton="LepGood"):
  if lepton=="LepGood":
    return [i for i in range(min(nMax, r.nLepGood)) if cmgLooseLepID(r, nLep=i, ptCuts=ptCuts, absEtaCuts=absEtaCuts,ele_MVAID_cuts=ele_MVAID_cuts,lepton=lepton) ]
  elif lepton=="LepOther":
    return [i for i in range(min(nMax, r.nLepOther)) if cmgLooseLepID(r, nLep=i, ptCuts=ptCuts, absEtaCuts=absEtaCuts,ele_MVAID_cuts=ele_MVAID_cuts,lepton=lepton) ]


    
    
def splitIndList(var, l, val):
  resLow = []
  resHigh = []
  for x in l:
    if var[x]>val:
      resHigh.append(x)
    else:
      resLow.append(x)
  return resLow, resHigh

def splitListOfObjects(var, val, s):
  resLow = []
  resHigh = []
  for x in s:
    if x[var]<val:
      resLow.append(x)
    else:
      resHigh.append(x)
  return resLow, resHigh

def get_cmg_jets(c):
  return [getObjDict(c, 'Jet_', ['eta','pt','phi','btagCMVA','btagCSV','mcMatchFlav' ,'partonId', 'id'], i) for i in range(int(getVarValue(c, 'nJet')))]
def get_cmg_jets_fromStruct(r,j_list):
  return [{p:getattr(r, 'Jet'+'_'+p)[i] for p in j_list} for i in range(r.nJet)]
def get_cmg_fatJets(c):
  return [getObjDict(c, 'FatJet_', ['eta','pt','phi','btagCMVA','btagCSV','mcPt','mcFlavour' ,'prunedMass','tau2', 'tau1'], i) for i in range(int(getVarValue(c, 'nFatJet')))]
def get_cmg_index_and_DR(objs,objPhi,objEta):
  obj = findClosestObject(objs,{'phi':objPhi, 'eta':objEta})
  if obj and obj['index']<10:
    index = obj['index']
    dr =sqrt(obj['distance'])
  else:
    index=-1
    dr=float('nan')
  return index , dr

def get_cmg_genLeps(c):
  return [getObjDict(c, 'genLep_', ['eta','pt','phi','charge', 'pdgId', 'sourceId'], i) for i in range(int(getVarValue(c, 'ngenLep')))]

def get_cmg_genParts(c):
  return [getObjDict(c, 'GenPart_', ['eta','pt','phi','charge', 'pdgId', 'motherId', 'grandmotherId'], i) for i in range(int(getVarValue(c, 'nGenPart')))]

def get_cmg_genPartsAll(c):
  return [getObjDict(c, 'genPartAll_', ['eta','pt','phi','charge', 'pdgId', 'motherId', 'grandmotherId'], i) for i in range(int(getVarValue(c, 'ngenPartAll')))]

def get_cmg_recoMuons(c):
  res = [getObjDict(c, 'LepGood_', ['eta','pt','phi','charge', 'dxy', 'dz', 'relIso03','tightId', 'pdgId'], i) for i in range(int(getVarValue(c, 'nLepGood')))]
  return filter(lambda m:abs(m['pdgId'])==13, res)



#def cmgGoodLepID(r,  nLep, ptCut=10., absEtaCut=2.4, relIso03Cut=0.3):
#  return cmgLooseLepID(r, nLep, ptCut, absEtaCut, relIso03Cut) and r.LepGood_tightId[nLep]
#
#def cmgLooseLepIndices(r, ptCut=10, absEtaCut=2.4, relIso03Cut=0.3):
#  return [i for i in range(r.nLepGood) if cmgLooseLepID(r, i, ptCut, absEtaCut, relIso03Cut) ]
#
#def cmgGetLeptonAtIndex(r, i):
#  return {'pt':r.LepGood_pt[i], 'phi':r.LepGood_phi[i], 'pdg':r.LepGood_pdgId[i], 'eta':r.LepGood_eta[i], 'relIso03':r.LepGood_relIso03[i], 'tightID':r.LepGood_tightId[i]}
