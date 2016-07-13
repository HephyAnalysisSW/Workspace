import sys,os

#from Workspace.DegenerateStopAnalysis.tools.degTools import *
#from Workspace.DegenerateStopAnalysis.cmgTuplesPostProcessed_mAODv2 import cmgTuplesPostProcessed
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_2016 import cmgTuplesPostProcessed
from Workspace.DegenerateStopAnalysis.tools.getSamples_8011 import getSamples , weights






tasks = [ 'limit_calc', 'draw_plots' ]#'yields', 'fom_plot', 'data_plot']
make_lumi_tag = lambda l: "%0.0fpbm1"%(l)


sample_info_default  = {
                     "sampleList"   :    ['tt', 'w','qcd','z','s300_270']          , 
                     "wtau"         :    False          , 
                     "useHT"        :    False          , 
                     "skim"         :    'presel'       ,   
                     "scan"         :    True           ,
                     "getData"      :    False          ,
                     "weights"      :    weights        ,
                       }  

lumi_info_default   = {
                     'lumi_target'         :   2300.,
                     'lumi_data_blinded'   :   2245.386,
                     'lumi_data_unblinded' :   139.63,
                      }



class TaskConfig():
    """
    
    """
    def __init__(self,  
                 taskList     ,
                 runTag       ,
                 ppTag        ,
                 cutInst      ,  
                 #ppUser       = 'nrad', 
                 sample_info  = {},
                 samples      = None,
                 lumi_info    = {},
                 saveDirBase = '/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/mAODv2_7412pass2_v6/Optimization_v0/',
                 **kwargs 
                 #samples     , 
                 #plots       , 
                 #cuts        ,
                 #bins        ,
                 #weights     , 
                 #mc_sig_data_path = [mc_path, sig_path, data_path] ,
                 #bkg_sig_data_lists = [ bkgList,sigList,dataList ] 
                 #runTag          = 'test', 
                 #ppTag           = '7412pass2_SMSScan_v2', 
                 #sigList     ,
                 #bkgList     ,
                 #dataList    ,
                 #useHT       ,
                ):
        for key, value in kwargs.iteritems():
            setattr(self,key,value)
        if type(taskList)==type(""):
            taskList = [taskList]
        #if any ( [ task.lower()  in tasks   for task in taskList] ): 
        #    pass
        #else:
        #    if 
        #    raise Exception("task, %s , not defined %s"%(taskList, tasks))
        for task in taskList:
            if task.lower() in tasks:
                pass
            elif hasattr(self,task):
                pass
            else:
                raise Exception("Task {task} either needs to be a predifined task {tasks} or it needs to have a user defined func, self.{task}".format(task=task, tasks=tasks) )



        args = ['taskList','runTag','ppTag', 'saveDirBase' ]
        for arg in args:
            setattr(self, arg, eval(arg) )

        self.nProc      = getattr(self, 'nProc', 1 )
        self.taskList   = taskList
        self.runTag = runTag
        self.ppTag  = ppTag

        if type(cutInst) == type([]):
            self.cutInstList = cutInst
            cutName      = ""
        else:
            self.cutInstList = [cutInst]
            self.cutInst = cutInst
            cutName      = self.cutInst.name
        self.cutName     = cutName
        #self.saveDirBase = saveDirBase

        
        for key,val in sample_info_default.iteritems():
            sample_info.setdefault(key,val)
        for key,val in lumi_info_default.iteritems():
            lumi_info.setdefault(key,val)



        self.sample_info = sample_info
        self.sampleList  = sample_info['sampleList'] 
        self.plotSampleList = getattr(self, 'plotSampleList', self.sampleList + ( self.signalList[:3]  if self.signalList else []  )) 



        self.ppStep = getattr(self,'ppStep','')
        self.ppUser = getattr(self,'ppUser','nrad01')
        self.cmgTag = getattr(self,'cmgTag','7412pass2_mAODv2_v6')
        self.ppTagVer = self.ppTag[-2:]
        self.cmgTagVer = self.cmgTag[-2:]




        useHT           =   self.sample_info['useHT']
        self.htString   =   "HT" if useHT else "Inc"
        self.scan_tag   =   "Scan" if sample_info['scan'] else ""
        self.lumi_info  =   lumi_info
        #self.lumi_tag   =   make_lumi_tag(lumi_info['lumi_target'])
        self.lumi_tag   =   make_lumi_tag(lumi_info['target_lumi'])
        self.saveDir    =   self.saveDirBase+'/%s/%s'%(self.runTag,self.htString)
        self.tableDir   =   self.saveDir+"/Tables/"
        self.dataPlotDir=   self.saveDir+"/DataPlots/"
        self.plotDir    =   self.saveDir+"/FOMPlots/"
        #self.cardDirBase=   "/data/nrad/results/cards_and_limits/"

        self.cardDirBase=   "/afs/hephy.at/work/n/nrad/results/cards_and_limits/%s/%s"%(self.cmgTag, self.ppTag)


        #self.results_dir =   self.cardDirBase + "/13TeV/{ht}/{run}/{lumi}/{cut}/".format( ht = self.htString, lumi = self.lumi_tag, run = self.runTag, cut=cutName) 
        self.results_dir =   self.cardDirBase + "/13TeV/{lumi}/{ht}/{run}/".format( ht = self.htString, lumi = self.lumi_tag, run = self.runTag ) 
        #self.cardDir    =   self.results_dir + "BasicSys"
        sys_label       =   "AdjustedSys"
        self.cardDir    =   self.results_dir + sys_label
        self.yield_pkl  =   self.results_dir + "/Yields_%s_%s_%s.pkl"%(cutName , self.runTag, self.scan_tag)

        default_keys       = {  
                                #"limit_pkl" : "13TeV/%s/%s_%s/BasicSys.pkl"%( self.htString, self.lumi_tag, self.runTag ),
                                "limit_pkl" : self.results_dir + "%s.pkl"%sys_label,
                                "redo_limit"     :   False      ,
                                "redo_yields"    :   False       ,
                            }
        for key, value in default_keys.iteritems():
            setattr(self,key, getattr(self,key,value) ) 

        self.parameterSet = "analysisHephy_13TeV_2016_v0"
        mc_path_tag       =  "RunIISpring16MiniAODv2"
        data_path_tag     =  "Data2016"

        self.mc_path       = "/afs/hephy.at/data/{ppUser}/cmgTuples/postProcessed_mAODv2/{cmgTag}/{ppTag}/{parameterSet}/{ppStep}/{mc_path_tag}_{cmgTagV}/".format(ppTag=ppTag,ppStep=self.ppStep, ppUser = self.ppUser , cmgTag = self.cmgTag, cmgTagV = self.cmgTagVer, parameterSet=self.parameterSet, mc_path_tag= mc_path_tag)
        self.signal_path   = "/afs/hephy.at/data/{ppUser}/cmgTuples/postProcessed_mAODv2/{cmgTag}/{ppTag}/{parameterSet}/{ppStep}/{mc_path_tag}_{cmgTagV}/".format(ppTag=ppTag,ppStep=self.ppStep, ppUser = self.ppUser , cmgTag = self.cmgTag, cmgTagV = self.cmgTagVer, parameterSet=self.parameterSet, mc_path_tag= mc_path_tag)
        self.data_path     = "/afs/hephy.at/data/{ppUser}/cmgTuples/postProcessed_mAODv2/{cmgTag}/{ppTag}/{parameterSet}/{ppStep}/{data_path_tag}_{cmgTagV}/".format(ppTag=ppTag,ppStep=self.ppStep, ppUser = self.ppUser , cmgTag = self.cmgTag, cmgTagV = self.cmgTagVer, parameterSet=self.parameterSet, data_path_tag= data_path_tag)
    
        if not samples:
            self.cmgPP         = cmgTuplesPostProcessed( self.mc_path, self.signal_path, self.data_path)
            self.samples   =   getSamples(   cmgPP = self.cmgPP, **sample_info   )
        else:
            self.samples   =   samples


        self.cardDirs ={}
        self.limitDirs ={}
        self.dataPlotDirs ={}
        self.fomPlotDirs ={}
        self.limitPkls ={}
        self.yieldPkls ={}
        self.tableDirs ={}
        self.saveDirs ={}
        for cutInst in self.cutInstList:
            cut_name = cutInst.fullName
            cutSaveDir = self.saveDir + "/" + cutInst.saveDir
            self.baseCutSaveDir = cutInst.baseCut.saveDir if getattr(cutInst,"baseCut") else cutInst.saveDir
            self.saveDirs[cut_name]  =  cutSaveDir
            self.cardDirs[cut_name]  =  self.cardDir + "/" + cutInst.saveDir  
            self.fomPlotDirs[cut_name]   =  cutSaveDir +"/FOMPlots/"
            self.dataPlotDirs[cut_name]  =  cutSaveDir +"/DataPlots/"
            self.limitDirs[cut_name] =  cutSaveDir +"/Limits/"  
            self.tableDirs[cut_name] =  cutSaveDir +"/Tables/"
            self.limitPkls[cut_name] =  self.results_dir + sys_label  + "/" + self.baseCutSaveDir  + "/Limits_%s_%s_%s.pkl"%(self.lumi_tag, self.runTag, cutInst.fullName)
            self.yieldPkls[cut_name] =  self.results_dir + sys_label  + "/" + self.baseCutSaveDir  + "/Yields_%s_%s_%s.pkl"%(self.lumi_tag, self.runTag, cutInst.fullName)



    #def save_info(self):
    #    for cutInst in self.cutInstList:

    #        pp.pprint(      self.cutInst.list ,  open( self.saveDir+"/cut.txt" ,"w"), width = 100, indent = 4 )
    #        pickle.dump(    self.cutInst,        open( self.saveDir+"/cut.pkl" ,"w") )

    #    pp.pprint(      samples,            open( self.saveDir+"/samples.txt" ,"w") )
    #    pp.pprint(      {    sample_name:decide_weight2(samp, weight=None, cut=self.cutInst.name, lumi='target_lumi' ) for sample_name, samp in samples.iteritems() } ,
    #                         open( self.saveDir+"/weights.txt" ,"w") )
        
    











