import sys,os
import importlib

import Workspace.DegenerateStopAnalysis.samples.baselineSamplesInfo as sampleInfo
from Workspace.DegenerateStopAnalysis.tools.degCuts import CutsWeights
from Workspace.DegenerateStopAnalysis.samples.getSamples import getSamples

class TaskConfig():
    """
    
    """
    def __init__(self,  
                 cfgTag,
                 generalTag,
                 runTag,
                 sysTag,
                 taskList,
                 plotList,
                 nanoAOD,
                 ppSet,
                 ppDirs,
                 cutInst, 
                 cutWeightOptions, 
                 settings, 
                 mcEra, 
                 plots, 
                 saveDirBase = '%s/www/plots'%os.path.expandvars("$HOME"),
                 sample_info = sampleInfo.sample_info_default,
                 bkgList     = None,
                 sigList     = None,
                 samples     = None,
                 taskModules = [],
                 nProc       = 1,
                 **kwargs 
                ):

        for key, value in kwargs.iteritems():
            setattr(self,key,value)

        if type(taskList)==type(""):
            taskList = [taskList]

        self.taskFuncs = {}
        for task in taskList:
            task_is_ok = False
            if hasattr(self, task):
                task_is_ok = True
                self.taskFuncs[task] = getattr(self, task)
            elif taskModules:
                for taskMod in taskModules:
                    foundtask = getattr(taskMod, task, "")
                    if foundtask:
                        self.taskFuncs[task] = getattr(taskMod, task)
                        task_is_ok = True
            if not task_is_ok:
                raise Exception("Task ({task}) either needs to be a predifined task or it needs to have a user defined func, self.{task} or it should be a function in one of the modules specified in the taskModules option ({modules})".format(task=task , modules=taskModules) )


        args = ['cfgTag', 'taskList', 'bkgList', 'sigList', 'plotList', 'runTag', 'sysTag', 'saveDirBase', 'generalTag', 'plots', 'cutWeightOptions', 'settings', 'nanoAOD', 'ppSet', 'mcEra']

        for arg in args:
            setattr(self, arg, eval(arg))

        self.year     = self.settings['year']
        self.dataset  = self.settings['dataset']
        self.campaign = self.settings['campaign']

        if self.nanoAOD:
            self.datasetFull = '%s_Run%s_%s'%(self.dataset, self.year, self.campaign)
        else:
            self.datasetFull = self.dataset   
 
        if type(cutInst) == type([]):
            self.cutInstList = cutInst
            cutName      = ""
        else:
            self.cutInstList = [cutInst]
            self.cutInst = cutInst
            cutName      = self.cutInst.name
        self.cutName     = cutName

        
        self.sample_info = sample_info
        self.sampleList  = self.sample_info['sampleList']
        getData          = self.sample_info['getData']

        if getData:
            self.sampleList.append(self.datasetFull)
         
        self.plotSampleList = getattr(self, 'plotSampleList', self.sampleList) 

        workDir = os.path.expandvars("$WORK")
        self.lumis = self.settings['lumis']

        if samples:
            self.samples = samples
        else:
            if self.nanoAOD:
                sampleDefPath = 'Workspace.DegenerateStopAnalysis.samples.nanoAOD_postProcessed.nanoAOD_postProcessed_' + self.mcEra
                sampleDef = importlib.import_module(sampleDefPath)
                self.PP = sampleDef.nanoPostProcessed(**ppDirs)
            else:
                from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_Summer16 import cmgTuplesPostProcessed
                self.PP = cmgTuplesPostProcessed(**ppDirs)

            self.samples = getSamples(PP = self.PP, settings = settings, **sample_info)

        if getData:
            self.dataTag = self.datasetFull
            lumiTag = sampleInfo.makeLumiTag(self.lumis[self.year][self.datasetFull], latex = False)
        else:    
            self.dataTag = "MC"
            lumiTag = sampleInfo.makeLumiTag(self.lumis["target_lumi"], latex = False)

        # cuts and weights
        cuts_weights = CutsWeights(self.samples, self.cutWeightOptions)
        cuts_weights.cuts._update(reset = False)
        cuts_weights._update()

        self.cuts_weights = cuts_weights 
        self.cuts = self.cuts_weights.cuts

        self.cardDirs = {}
        self.limitDirs = {}
        self.dataPlotDirs = {}
        self.fomPlotDirs = {}
        self.limitPkls = {}
        self.yieldPkls = {}
        self.tableDirs = {}
        self.saveDirs = {}
        self.cutLumiTags = {}

        cardDirBase = "%s/results/cards_and_limits"%(workDir)
        taskTag     = "_".join([x for x in [self.cfgTag, self.generalTag, self.runTag] if x])
        taskDir     = "/".join([x for x in [self.cfgTag, self.generalTag, self.runTag] if x])
        relDir      = "{ppSet}/{taskDir}/{dataTag}".format(ppSet = self.ppSet, taskDir = taskDir, dataTag = self.dataTag)

        self.resultsDir = cardDirBase + "/" + relDir
        self.saveDir    = saveDirBase + "/" + relDir

        for cutInst in self.cutInstList:
            cut_name = cutInst.fullName

            self.cutLumiTags[cut_name]  = lumiTag

            cutSaveDir = self.saveDir + "/" + cutInst.saveDir
            self.saveDirs[cut_name]     = cutSaveDir
            self.fomPlotDirs[cut_name]  = cutSaveDir +"/FOMPlots/"
            self.dataPlotDirs[cut_name] = cutSaveDir +"/DataPlots/"
            self.limitDirs[cut_name]    = cutSaveDir +"/Limits/"  
            self.tableDirs[cut_name]    = cutSaveDir +"/Tables/"

            self.baseCutDir          = cutInst.baseCut.saveDir if getattr(cutInst,"baseCut") else cutInst.saveDir
            self.baseCutDirFull      = self.resultsDir + "/" + self.baseCutDir 
            self.cardDirs[cut_name]  = self.baseCutDirFull  + "/" + self.sysTag + "/" + cutInst.name + "/"
            self.limitPkls[cut_name] = self.baseCutDirFull  + "/" + self.sysTag + "/Limits_%s_%s_%s.pkl"%(self.cutLumiTags[cut_name], taskTag, cut_name)
            self.yieldPkls[cut_name] = self.baseCutDirFull                      + "/Yields_%s_%s_%s.pkl"%(self.cutLumiTags[cut_name], taskTag, cut_name)

        print "\n=================================================================================\n"
        print "Configuration Options:\n"
        print "cfg Tag:",         self.cfgTag
        print "General Tag:",     self.generalTag
        print "Run Tag:",         self.runTag
        print "Systematics Tag:", self.sysTag
        print "Tasks:",           self.taskList
        print "Plots:",           self.plotList
        print "Samples Set:",     self.ppSet
        print "cutInstList:",     [c.name for c in self.cutInstList]
        print "saveDir:",         self.saveDir
        print "resultsDir:",      self.resultsDir
        print "\n=================================================================================\n"
