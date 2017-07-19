import sys,os

#from Workspace.DegenerateStopAnalysis.tools.degTools import *
#from Workspace.DegenerateStopAnalysis.cmgTuplesPostProcessed_mAODv2 import cmgTuplesPostProcessed
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_2016 import cmgTuplesPostProcessed
#from Workspace.DegenerateStopAnalysis.tools.getSamples_8011 import getSamples , weights
from Workspace.DegenerateStopAnalysis.tools.getSamples import getSamples , weights






make_lumi_tag = lambda l: "%0.0fpbm1"%(l)

def make_lumi_tag(l):
    if type(l)==type(""):
        l = float(l)
    lumi_tag = "%0.0fpbm1"%(l)
    return lumi_tag


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
                     #'lumi_target'         :   2300.,
                     #'lumi_data_blinded'   :   2245.386,
                     #'lumi_data_unblinded' :   139.63,
                      }



class TaskConfig():
    """
    
    """
    def __init__(self,  
                 taskList     ,
                 cfgTag       ,
                 runTag       ,
                 ppTag        ,
                 cutInst      ,  
                 #ppUser       = 'nrad', 
                 sample_info  = {},
                 samples      = None,
                 lumi_info    = {},
                 taskModules  = [],
                 saveDirBase = '%s/www/T2Deg13TeV/mAODv2_7412pass2_v6/Optimization_v0/'%os.path.expandvars("$HOME"),
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
        #self.kwargs = kwargs
        for key, value in kwargs.iteritems():
            setattr(self,key,value)
        if type(taskList)==type(""):
            taskList = [taskList]
        #if any ( [ task.lower()  in tasks   for task in taskList] ): 
        #    pass
        #else:
        #    if 
        #    raise Exception("task, %s , not defined %s"%(taskList, tasks))
        self.taskFuncs= {}
        for task in taskList:
            task_is_ok = False
            if hasattr(self,task):
                task_is_ok = True
                self.taskFuncs[task] = getattr( self, task )
            elif taskModules:
                for taskMod in taskModules:
                    foundtask = getattr( taskMod, task, "")
                    print taskMod, foundtask
                    if foundtask:
                        self.taskFuncs[task]= getattr(taskMod, task)
                        task_is_ok = True
            if not task_is_ok:
                raise Exception("Task ( {task} ) either needs to be a predifined task or it needs to have a user defined func, self.{task} or it should be a function in one of the modules specified in the taskModules option ({modules})".format(task=task , modules=taskModules) )



        args = ['cfgTag', 'taskList','runTag','ppTag', 'saveDirBase' ]
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
        workDir         =   os.path.expandvars("$WORK")
        self.lumi_info  =   lumi_info
        #self.lumi_tag   =   make_lumi_tag(lumi_info['lumi_target'])


        #self.tableDir   =   self.saveDir+"/Tables/"
        #self.dataPlotDir=   self.saveDir+"/DataPlots/"
        #self.plotDir    =   self.saveDir+"/FOMPlots/"

        #self.cardDirBase=   "/afs/hephy.at/work/n/nrad/results/cards_and_limits/%s/%s"%(self.cmgTag, self.ppTag)
        #self.yieldPklDir =  "/afs/hephy.at/work/n/nrad/results/yields/%s/%s/"%(self.cmgTag, self.ppTag) 
        #self.yieldPklDir =  "%s/results/yields/%s/%s/"%(workDir, self.cmgTag, self.ppTag) 
        #self.scan_tag   =   "Scan" if sample_info['scan'] else ""
        #self.lumi_tag   =   make_lumi_tag(lumi_info['target_lumi'])
        #self.results_dir =   self.cardDirBase + "/13TeV/{ht}/{run}/{lumi}/{cut}/".format( ht = self.htString, lumi = self.lumi_tag, run = self.runTag, cut=cutName) 
        #self.cardDir    =   self.results_dir + "BasicSys"
        #self.yield_pkl  =   self.results_dir + "/Yields_%s_%s_%s.pkl"%(cutName , self.runTag, self.scan_tag)

        default_keys       = {  
                                #"limit_pkl" : self.results_dir + "%s.pkl"%sys_label,
                                "redo_limit"     :   False      ,
                                "redo_yields"    :   False       ,
                            }
        for key, value in default_keys.iteritems():
            setattr(self,key, getattr(self,key,value) ) 

        self.parameterSet =  getattr(self, "parameterSet","analysisHephy_13TeV_2016_v0")
        mc_path_tag       =  getattr(self, "mcDir", "RunIISpring16MiniAODv2")
        data_path_tag     =  getattr(self, "dataDir", "Data2016")

        self.mc_path       = "/afs/hephy.at/data/{ppUser}/cmgTuples/postProcessed_mAODv2/{cmgTag}/{ppTag}/{parameterSet}/{ppStep}/{mc_path_tag}_{cmgTagV}/".format(ppTag=ppTag,ppStep=self.ppStep, ppUser = self.ppUser , cmgTag = self.cmgTag, cmgTagV = self.cmgTagVer, parameterSet=self.parameterSet, mc_path_tag= mc_path_tag)
        if '8012' in self.cmgTag or '8011' in self.cmgTag:
            self.signal_path   = "/afs/hephy.at/data/{ppUser}/cmgTuples/postProcessed_mAODv2/{cmgTag}_1/{ppTag}_1/{parameterSet}/{ppStep}/{mc_path_tag}_{cmgTagV}/".format(ppTag=ppTag,ppStep=self.ppStep, ppUser = self.ppUser , cmgTag = self.cmgTag, cmgTagV = self.cmgTagVer, parameterSet=self.parameterSet, mc_path_tag= mc_path_tag)
            #self.signal_path   = "/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/{cmgTag}/{ppTag}/{parameterSet}/{ppStep}/{mc_path_tag}_{cmgTagV}/".format(ppTag=ppTag,ppStep=self.ppStep, ppUser = self.ppUser , cmgTag = self.cmgTag, cmgTagV = self.cmgTagVer, parameterSet=self.parameterSet, mc_path_tag= mc_path_tag)
        else:
            self.signal_path   = "/afs/hephy.at/data/{ppUser}/cmgTuples/postProcessed_mAODv2/{cmgTag}/{ppTag}/{parameterSet}/{ppStep}/{mc_path_tag}_{cmgTagV}/".format(ppTag=ppTag,ppStep=self.ppStep, ppUser = self.ppUser , cmgTag = self.cmgTag, cmgTagV = self.cmgTagVer, parameterSet=self.parameterSet, mc_path_tag= mc_path_tag)
            #self.signal_path   = "/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/{cmgTag}_1/{ppTag}_1/{parameterSet}/{ppStep}/{mc_path_tag}_{cmgTagV}/".format(ppTag=ppTag,ppStep=self.ppStep, ppUser = self.ppUser , cmgTag = self.cmgTag, cmgTagV = self.cmgTagVer, parameterSet=self.parameterSet, mc_path_tag= mc_path_tag)
        self.data_path     = "/afs/hephy.at/data/{ppUser}/cmgTuples/postProcessed_mAODv2/{cmgTag}/{ppTag}/{parameterSet}/{ppStep}/{data_path_tag}_{cmgTagV}/".format(ppTag=ppTag,ppStep=self.ppStep, ppUser = self.ppUser , cmgTag = self.cmgTag, cmgTagV = self.cmgTagVer, parameterSet=self.parameterSet, data_path_tag= data_path_tag)
        #self.data_path     = "/afs/hephy.at/data/{ppUser}/cmgTuples/postProcessed_mAODv2/{cmgTag}/{ppTag}/{parameterSet}/{ppStep}/{data_path_tag}_{cmgTagV}/".format(ppTag=ppTag,ppStep=self.ppStep, ppUser = self.ppUser , cmgTag = self.cmgTag, cmgTagV = self.cmgTagVer, parameterSet=self.parameterSet, data_path_tag= data_path_tag)
    
        if not samples:

            if '74' in self.cmgTag:
                from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2 import cmgTuplesPostProcessed
            elif '8020' in self.cmgTag:
                from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_2016 import cmgTuplesPostProcessed
            else:
                from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_Summer16 import cmgTuplesPostProcessed
                
            ichepdata          = False
            self.cmgPP         = cmgTuplesPostProcessed( self.mc_path, self.signal_path, self.data_path, ichepdata = ichepdata)
            print self.cmgPP
            self.samples   =   getSamples(   cmgPP = self.cmgPP, **sample_info   )
        else:
            self.samples   =   samples


        sys_label       =   getattr(self, "sys_label", "AdjustedSys")
        self.cardDirs ={}
        self.limitDirs ={}
        self.dataPlotDirs ={}
        self.fomPlotDirs ={}
        self.limitPkls ={}
        self.yieldPkls ={}
        self.tableDirs ={}
        self.saveDirs ={}

        self.cutLumiTags ={}
        useData = getattr(self, "data" , False)
        dataTag = self.samples[useData]['name'] if useData else "MC"
        self.dataTag = dataTag 
        self.cardDirBase=   "%s/results/cards_and_limits/"%(workDir)
        #self.cardDirBase =   os.path.expandvars("$CMSSW_BASE") + "/src/Workspace/DegenerateStopAnalysis/results/2016/"
        #self.cardDir    =   self.results_dir + sys_label
        self.taskTag     =  "_".join([x for x in  [ self.cfgTag, self.generalTag, self.runTag] if x ] )
        self.results_dir =   self.cardDirBase + "/13TeV/{cmgTag}/{ppTag}/{cfgTag}/{generalTag}/{run}/{dataTag}".format(cmgTag = self.cmgTag, ppTag = self.ppTag,   run = self.runTag, generalTag = self.generalTag, cfgTag = self.cfgTag , dataTag = dataTag) 
        self.saveDir     =   self.saveDirBase +       "/{cmgTag}/{ppTag}/{cfgTag}/{generalTag}/{run}/{dataTag}".format(cmgTag = self.cmgTag, ppTag = self.ppTag,   run = self.runTag, generalTag = self.generalTag, cfgTag = self.cfgTag , dataTag = dataTag)
        for cutInst in self.cutInstList:
            cut_name = cutInst.fullName
            cutSaveDir = self.saveDir + "/" + cutInst.saveDir

            
            if useData:
                print useData,
                print lumi_info
                print self.samples[useData]
                lumi_info.update( {self.samples[useData]['name']+"_lumi" : self.samples[useData]['lumi'] })
                print lumi_info
                if 'sr' in cut_name.lower():
                    #lumi = 'DataUnblind_lumi'
                    #lumi = 'DataICHEP_lumi'
                    print "WARNING: SR in CutName ... "
                    lumi = self.samples[useData]['name']+"_lumi"
    
                else:
                    lumi = self.samples[useData]['name']+"_lumi"
                #if useData == 'd':
                #    lumi = 'DataUnblind_lumi'
                #elif useData =='dblind':
                #    lumi = 'DataBlind_lumi'
                #elif useData =='dichep':
                #    lumi = 'DataICHEP_lumi'
                #elif useData =='dgh':
                #    lumi = 'DataGH_lumi'
                #elif useData =='dbcdef':
                #    lumi = 'DataBCDEF_lumi'
                #else:   
                #    raise Exception("Data name not recognized: %s"%useData)
            else:
                lumi = 'target_lumi'
            
             
            print lumi_info
            print lumi
            print lumi_info[lumi]
            print type(lumi_info[lumi])

            self.cutLumiTags[cut_name]= make_lumi_tag( lumi_info[lumi] )

            
            self.baseCutSaveDir = cutInst.baseCut.saveDir if getattr(cutInst,"baseCut") else cutInst.saveDir
            self.saveDirs[cut_name]  =  cutSaveDir
            self.fomPlotDirs[cut_name]   =  cutSaveDir +"/FOMPlots/"
            self.dataPlotDirs[cut_name]  =  cutSaveDir +"/DataPlots/"
            self.limitDirs[cut_name] =  cutSaveDir +"/Limits/"  
            self.tableDirs[cut_name] =  cutSaveDir +"/Tables/"
            self.cardDirs[cut_name]  =  self.results_dir + "/" + self.baseCutSaveDir  + "/" + sys_label + "/" + cutInst.name + "/"
            self.limitPkls[cut_name] =  self.results_dir + "/" + self.baseCutSaveDir  + "/" + sys_label + "/Limits_%s_%s_%s.pkl"%(self.cutLumiTags[cut_name], self.taskTag, cut_name)
            self.yieldPkls[cut_name] =  self.results_dir + "/" + self.baseCutSaveDir                    + "/Yields_%s_%s_%s.pkl"%(self.cutLumiTags[cut_name], self.taskTag, cut_name)



    #def save_info(self):
    #    for cutInst in self.cutInstList:

    #        pp.pprint(      self.cutInst.list ,  open( self.saveDir+"/cut.txt" ,"w"), width = 100, indent = 4 )
    #        pickle.dump(    self.cutInst,        open( self.saveDir+"/cut.pkl" ,"w") )

    #    pp.pprint(      samples,            open( self.saveDir+"/samples.txt" ,"w") )
    #    pp.pprint(      {    sample_name:decide_weight2(samp, weight=None, cut=self.cutInst.name, lumi='target_lumi' ) for sample_name, samp in samples.iteritems() } ,
    #                         open( self.saveDir+"/weights.txt" ,"w") )
        
    











