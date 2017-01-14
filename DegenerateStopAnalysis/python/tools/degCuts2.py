import re
import math
import copy
import collections

from Workspace.DegenerateStopAnalysis.samples.baselineSamplesInfo import cutWeightOptions
from Workspace.DegenerateStopAnalysis.tools.degTools import CutClass, joinCutStrings, splitCutInPt, btw, less, more
from Workspace.DegenerateStopAnalysis.tools.degVars import VarsCutsWeightsRegions
from Workspace.DegenerateStopAnalysis.tools.degTools import getSampleTriggersFilters

#from Workspace.DegenerateStopAnalysis.tools.btag_sf_map import BTagSFMap 
#import Workspace.DegenerateStopAnalysis.tools.degWeights as degWeights

class Variable(object):
    def __init__(self, name, string, latex=None):
        self.name   = name
        self.string = string
        self.latex  = latex if latex else ''
    def __str__(self):
        return self.string
    def __repr__(self):
        return "<%s.%s %s: %s >"%(self.__module__, self.__class__.__name__, self.name, self.string)


class Variables():
    def __init__( self, vars_dict = None ):
        self.vars_dict_orig   = copy.deepcopy(vars_dict)
        #self.format_vars_dict()
        self.update()

    def update(self):
        self.format_vars_dict()

    def format_vars_dict( self ):
        """ formats the vars_dict for variables that depend on other variables , i.e. LepIndex, etc. can be done in a smarter way.  """
        self.vars_dict_format = { varName: varInfo['var'] for varName, varInfo in self.vars_dict_orig.iteritems() }
        #print self.vars_dict_format 
        self.vars_dict   = copy.deepcopy(self.vars_dict_orig)
        for varName, varInfo in self.vars_dict.items():
            #print varInfo['var']
            varFormatMaxDepth = 5
            varFormatDepth = 0
            while re.search(r'{(.*?)}',varInfo['var'] ) and varFormatDepth < varFormatMaxDepth: 
                varInfo['var']  = varInfo['var'].format(**self.vars_dict_format)
                varFormatDepth += 1
                #print varInfo['var']
            setattr(self, varName, Variable( varName, varInfo['var'], varInfo['latex'])) 
        self.vars_dict_format = { varName: varInfo['var'] for varName, varInfo in self.vars_dict.iteritems() } 

def isDataSample(sample):
    isDataSample = False
    dataSampleNames  = ['data', 'dblind', 'dunblind', 'dichep' ]
    if getattr( sample, "isData", ""):
        pass #isDataSample = True
    elif type(sample)==str:
        if any([dataSampleName in sample.lower() for dataSampleName in dataSampleNames]):
            isDataSample = True
    return isDataSample 

class Weights(Variables):
    def combine( self, weightList):
        #weights_to_combine = [ getattr(self.weights,wname) for wname in weightList]
        weights_to_combine = [ getattr(self,wname) for wname in weightList]
        return '*'.join(['(%s)'%w for w in weights_to_combine])


    def _makeCutWeightOptFunc( self, sample_list, cut_options):
        """
        Create a function to add weights based on sample name and cut
        """
        def cutWeightOptFunc(sample, cutListNames, weightListNames):
            if isDataSample(sample):
                #return sample, cutListNames, weightListNames
                return sample, cutListNames, ["noweight"]
            if sample_list and not any([x in sample for x in sample_list]): #sample not in sample_list:
                #print "sample not in sample_list : ", sample_list
                return sample, cutListNames, weightListNames
            #cutListNames
            options = [x for x in cut_options if not x == "default"]
            new_weights = []
            
            for cut in options:
                if cut in cutListNames:
                    new_weights.append(cut_options[cut])
            if len(new_weights)>1:
                assert False, ["Seems like more than one option was applicable....", cutListNames, cut_options, new_weights]
            if not new_weights:
                if cut_options.get("default"):
                    new_weights.append( cut_options["default"])
            weightListNames.extend(new_weights)
            for w in new_weights:
                if w in cutListNames:
                    print w, "poped from cutList!  %s"%cutListNames , "for ", sample
                    cutListNames.pop(cutListNames.index(w))
            return sample, cutListNames, weightListNames
        setattr( cutWeightOptFunc, "cut_options", cut_options)
        setattr( cutWeightOptFunc, "sample_list", sample_list)
        return cutWeightOptFunc

    def _makeCutWeightFuncs(self,  weight_options):
        self.cut_weight_funcs = {}
        for weight_option_name, weight_option in weight_options.items():
            self.cut_weight_funcs[weight_option_name] = self._makeCutWeightOptFunc( weight_option['sample_list'], weight_option['cut_options'] )
            ### Here I change the name of the func and add it to make it picklable..... a better solution?
            funcname = "cutWeightOptFunc_"+weight_option_name
            self.cut_weight_funcs[weight_option_name].__name__ = funcname


class Cuts():
    #def __init__( self, settings =None, cuts_dict = None , vars={}, regions ={}, weights = None, def_weights = None,options=None):
    def __init__( self, settings =None, def_weights = ["weight"], options=[], alternative_vars = {}):
        if settings:
            varsCutsWeightsRegions = VarsCutsWeightsRegions(**settings)
            weights_dict           = varsCutsWeightsRegions.weights_dict
            weight_options         = varsCutsWeightsRegions.weight_options
            regions                = varsCutsWeightsRegions.regions
            cuts_dict              = varsCutsWeightsRegions.cuts_dict
            weights                = Weights(weights_dict)
            weights._makeCutWeightFuncs(weight_options)

            vars                   = varsCutsWeightsRegions.vars_dict
            if alternative_vars:
                vars.update(alternative_vars)
            vars=Variables(vars)

            self.varsCutsWeightsRegions = varsCutsWeightsRegions
            
        else:
            pass
        if type(vars)==dict:
            vars = Variables(vars)
        if not getattr(vars, "vars_dict"):
            raise Exception("Variables must be from Variable Class or a dictionary of variables but it was: %s"%(vars))
        self.vars        =  vars
        self.vars_dict_format = vars.vars_dict_format
        self.cuts_dict_orig   = copy.deepcopy(cuts_dict)
        #self.cuts_dict   = cuts_dict
        self.cutInstList = []
        self.cutInsts    = {}
        self.regions     = regions
        
        self.weights     = weights
        self.def_weights = def_weights
        self.options     = options
        #print regions
        #self.makeRegions(self.regions)
        self.update()
    def update(self):
        self.vars.update()
        self.weights.update()
        self.vars_dict_format = self.vars.vars_dict_format
        self.format_cuts_dict()
        self.makeRegions(self.regions)

    def format_cuts_dict( self ):
        #self.vars_dict_format = { varName: varInfo['var'] for varName, varInfo in self.cuts_dict.iteritems() }
        self.cuts_dict = copy.deepcopy( self.cuts_dict_orig )
        for cutName, cutInfo in self.cuts_dict.items():
            cutInfo['cut'] = cutInfo['cut'].format(**self.vars_dict_format)

    def makeRegions(self, regions):
        for region_name, region_info in regions.iteritems():
            if region_info.has_key("cuts"):
                self.makeCutClass(region_name, cutListNames = region_info['cuts'], baseCut = region_info['baseCut'])
            elif region_info.has_key("regions"):
                #continue
                cutList = [ [subregion, getattr(self, subregion).combined] for subregion in region_info['regions'] ]
                #print cutList
                #cutList = [ [subregion]]
                self.makeCutClass( region_name, cutList = cutList, baseCut = region_info['baseCut'] )
    
    def makeCutClass( self, name, cutListNames=None , baseCut =None, cutList = None):
        #print 'making cut class', name
        if cutListNames:
            cutList = [ [cutName, self.cuts_dict[cutName]['cut']] for cutName in cutListNames]
        elif cutList:
            pass
        if type(baseCut)==type(""):
            if hasattr(self, baseCut):
                baseCut = getattr(self, baseCut)
            else:
                raise Exception("baseCut for %s (%s) is not recognized in the class... it must be defined first"%(name, baseCut) )
        cutInst = CutClass( name, cutList, baseCut)
        setattr(self, name, cutInst)
        self.cutInstList.append(name)
        self.cutInsts[name] = cutInst
        #print self.cutInstList
        #self.cuts_dict      = cutInst.combined
        #return cutInst

    def getRegionCutNames(self, regionName):
        if not regionName in self.regions:
            raise Exception("Region (%s) not found among regions: %s"%(regionName, self.regions.keys()))
        region  = self.regions[regionName]
        region_cut_names = region['cuts']
        baseCut_cut_names = self.getRegionCutNames( region['baseCut'] ) if region['baseCut'] else []
        return baseCut_cut_names + region_cut_names
        

    def getCut( self, cutListNames, returnString = True, namesOnly=False): 
        """
            get cut string either from cuts or from the regions
        """
        cuts_to_combine = []
        cut_names       = []
        for cutName in cutListNames:
            if cutName in self.cuts_dict.keys():
                cut_names.append( cutName )
                #cuts_to_combine.append( self.cuts_dict[cutName]['cut'] )
            elif cutName in self.regions:
                region_cut_names = self.getRegionCutNames( cutName)
                region_cuts = self.getCut( region_cut_names, returnString = False )
                cut_names.extend(region_cut_names)
                #cuts_to_combine.extend( region_cuts)
        unique_cut_names = []  ## in case of redundant cuts
        for cut in cut_names:
            if cut not in unique_cut_names:
                unique_cut_names.append(cut)
        if namesOnly:
            return unique_cut_names
        cuts_to_combine = [ self.cuts_dict[cutName]['cut'] for cutName in unique_cut_names ]
        if returnString:
            ret = '&&'.join(["(%s)"%c for c in cuts_to_combine])    
        else:
            ret = cuts_to_combine
        return ret

    def getCutWeight(self, cutListNames, weightListNames, options = None ):
        cutString    = self.getCut( cutListNames)
        weightString = self.weights.combine( weightListNames) 
        return cutString, weightString

    def getCutWeightString(self, cutListNames, weightNames, options = None):
        cutString , weightString = self.getCutWeight(cutListNames, weightNames)
        return "(%s)*(%s)"%(cutString, weightString)

    def evaluateWeightOptions(self, sample, cutListNames, weightListNames, options):
        cutListNames = cutListNames[:]
        weightListNames = weightListNames[:]

        for option in options:
            #print option
            if not option in self.weights.cut_weight_funcs:
                print "option not found"
                assert False
                #continue
            opt_func = self.weights.cut_weight_funcs[option]
            #print opt_func
            #print sample, cutListNames, weightListNames
            sample, cutListNames, weightListNames = opt_func(sample, cutListNames, weightListNames)
            #print sample, cutListNames, weightListNames
        return sample, cutListNames, weightListNames
            
    def getSampleTriggersFilters(self, sample, cutString=''):
        """ NOT FULLY IMPLEMENTED YET """
        triggers = getattr(sample, 'triggers','')
        filters = getattr(sample, 'filters','')
        cuts = getattr(sample, 'cuts','')
        cutList = []
        for cutItem in [cutString, triggers, filters, cuts] :
            if cutItem:
                cutList.append(cutItem)
        return "&&".join(["(%s)"%c for c in cutList])

    def getSampleFullCutWeights():
        # getsamplecutweight
        # getsampleTriggersFilters
        return 

    def getSampleCutWeight(self, sample, cutListNames, weightListNames=None,  options=None, returnString = False, returnCutWeight=True):
        if not weightListNames:
            weightListNames = self.def_weights
        if not options:
            options = self.options
        cutListNames = self.getCut(cutListNames, namesOnly=True)
        sample, cutListNames, weightListNames  = self.evaluateWeightOptions(sample, cutListNames, weightListNames, options)
        if returnString:
            return "(%s)*(%s)"%self.getCutWeight(cutListNames, weightListNames)
        if returnCutWeight:
            return self.getCutWeight(cutListNames, weightListNames)
        return sample, cutListNames, weightListNames


class CutsWeights():
   def __init__(self, samples, cutWeightOptions = cutWeightOptions):
      self.settings = cutWeightOptions['settings']
      self.def_weights = cutWeightOptions['def_weights']
      self.options = cutWeightOptions['options']

      self.cuts = Cuts(self.settings, self.def_weights, self.options)
      self.cuts_weights = self.getCutsWeights(cutWeightOptions, samples)     
 
   def getCutsWeights(self, cutWeightOptions, samples):
      cuts_weights = {}
      
      for reg in self.cuts.regions['bins_sum']['regions']:
         cuts_weights[reg] = {}
      
         for samp in samples:
            c,w = self.cuts.getSampleCutWeight(samples[samp].name, cutListNames = [reg])
            
            c,w = getSampleTriggersFilters(samples[samp], c, w)
            
            cuts_weights[reg][samp] = (c,w)
      
      return cuts_weights

if __name__ == '__main__':
    #from Workspace.DegenerateStopAnalysis.tools.degVars import *
    #weights     = Weights(degWeights.weights_dict)
    #cuts        = Cuts(cuts_dict, variables, regions, weights=weights, def_weights = def_weights, options = options)

    settings = cutWeightOptions['settings']

    cuts = Cuts(settings)
