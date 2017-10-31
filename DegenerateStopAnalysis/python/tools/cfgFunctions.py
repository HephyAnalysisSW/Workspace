from Workspace.HEPHYPythonTools.helpers import getYieldFromChain
from Workspace.HEPHYPythonTools.u_float import u_float
import pickle
from Workspace.DegenerateStopAnalysis.tools.degTools import cmsbase, getEfficiency, getPlots, drawPlots , saveCanvas, setEventListToChains , makeDir , decide_weight2 , JinjaTexTable, Yields, CutClass , setMVASampleEventList , drawYields  , dict_operator, yield_adder_func2 , dict_manipulator , makeSimpleLatexTable, setEventListToChainWrapper, setEventListsFromCutWeights

import Workspace.DegenerateStopAnalysis.tools.limitTools as limitTools

import pprint as pp
import re , os
import multiprocessing
#from subprocess import call
import subprocess 
import gc 


#
#   Common Tools
#
def round_(val, nDigit):
    if hasattr(val, "round"):
        return getattr(val, "round")(nDigit)
    else:
        return round(val, nDigit)
def str_round(val, nDigit):
    return str(round_(val, nDigit))

def fix_region_name(name):
    return name.replace("_","/").replace("pos","Q+").replace("neg","Q-")



#def setMVASampleEventList(samples, sample, killTrain = False):
#    if not ( hasattr( samples[sample], 'cut' ) and samples[sample]['cut'] ) :
#        return
#    cuts = [ samples[sample].cut ]
#    if killTrain:
#        cuts.append("!trainingEvent")
#    cutStr = "&&".join("(%s)"%cut for cut in cuts )
#    cutInst = CutClass( samples[sample].name, [[ samples[sample].name, cutStr ]] , baseCut = None )
#    setEventListToChains( samples, [sample], cutInst , verbose=False) 
#    return

#
# CFG Functions 
#



def fix_test_train_func(cfg, args):
    samples = cfg.samples
    output  = cfg.saveDir +"/" + "TestTrainEventsSummary.txt"
    text = ["    ", "Test+Train(Yield)",   "Train/Test(Yield)" , "Test Evt(Yield)", "Train Evt(Yield)", "MVA Weight Factor" ]
    col_len =  30
    line_template = '{:<%s}'%col_len
    line = (line_template*len(text)).format(*text)
    print line
    f = open(output,'w')
    f.write(line+"\n")
    yld_weight = "weight"
    evt_weight = "(1)"

    for samp in [ x for x in samples.bkgList() + samples.massScanList() if not 'train' in x ]:
        test_evts   =  getYieldFromChain( samples[samp]['tree'] , samples[samp]['cut'] , evt_weight )
        train_evts  =  getYieldFromChain( samples[samp+"_train"]['tree'] , samples[samp+"_train"]['cut'] , evt_weight )
        test_ylds   =  u_float( getYieldFromChain( samples[samp]['tree'] , samples[samp]['cut'] , yld_weight , returnError=True) )
        train_ylds  =  u_float( getYieldFromChain( samples[samp+"_train"]['tree'] , samples[samp+"_train"]['cut'] , yld_weight , returnError=True) )
        mva_weight_factor = (train_evts+test_evts)/(test_evts) if (test_evts) else 0
        text = [    samp,      
                    str_round( train_evts + test_evts ,3)   + " (%s)"%str_round((train_ylds+test_ylds) , 3), 
                    str_round( 1.*train_evts/test_evts, 3)  + " (%s)"%str_round((1.*train_ylds/test_ylds) , 3) if test_evts else 0 , 
                    str_round(test_evts,3)                  + " (%s)"%str_round((test_ylds)  , 3)  , 
                    str_round(train_evts,3)                 + " (%s)"%str_round((train_ylds) , 3)  , 
                    str_round(mva_weight_factor,3) 
                ]
        line = (line_template*len(text)).format(*text)
        print line
        f.write(line+"\n")
        #print samp, mva_weight_factor , str( round(mva_weight_factor,3) ) , round(mva_weight_factor,3) 
        samples[samp].weights.weight_dict.update( { "mva_test_train_weight_factor":str( round(mva_weight_factor,3) )})    
    print "Test/Train Events Summary written in: %s "%output
    f.close()
    del f



def fix_mva_evt_weights(cfg, args):
    samples = cfg.samples
    output  = cfg.saveDir +"/" + "TestTrainEventsSummary.txt"
    text = ["    ", "Test+Train(Yield)",   "Train/Test(Yield)" , "Test Evt(Yield)", "Train Evt(Yield)", "MVA Weight Factor" ]
    col_len =  30
    line_template = '{:<%s}'%col_len
    line = (line_template*len(text)).format(*text)
    print line
    f = open(output,'w')
    f.write(line+"\n")
    yld_weight = "eventWeight"
    evt_weight = "(1)"

    setEvtList=False
    for samp in [ x for x in samples.bkgList() + samples.massScanList() if not 'train' in x ]:
        if not samples[samp]['tree'].GetEventList(): 
            setEvtList = True  
            setMVASampleEventList(samples, samp ) 
        test_evts   =  getYieldFromChain( samples[samp]['tree'] , samples[samp]['cut'] + "&&(!trainingEvent)", evt_weight )
        train_evts  =  getYieldFromChain( samples[samp]['tree'] , samples[samp]['cut'] + "&&(trainingEvent)" , evt_weight )
        test_ylds   =  u_float( getYieldFromChain( samples[samp]['tree'] , samples[samp]['cut'] + "&&(!trainingEvent)" , yld_weight , returnError=True) )
        train_ylds  =  u_float( getYieldFromChain( samples[samp]['tree'] , samples[samp]['cut'] + "&&(trainingEvent)"  , yld_weight , returnError=True) )
        mva_weight_factor = (train_evts+test_evts)/(test_evts) if (test_evts) else 0
        text = [    samp,      
                    str_round( train_evts + test_evts ,3)   + " (%s)"%str_round((train_ylds+test_ylds) , 3), 
                    str_round( 1.*train_evts/test_evts, 3)  + " (%s)"%str_round((1.*train_ylds/test_ylds) , 3) if test_evts else 0 , 
                    str_round(test_evts,3)                  + " (%s)"%str_round((test_ylds)  , 3)  , 
                    str_round(train_evts,3)                 + " (%s)"%str_round((train_ylds) , 3)  , 
                    str_round(mva_weight_factor,3) 
                ]
        line = (line_template*len(text)).format(*text)
        print line
        f.write(line+"\n")
        #print samp, mva_weight_factor , str( round(mva_weight_factor,3) ) , round(mva_weight_factor,3) 
        samples[samp].weights.weight_dict.update( 
                                                  { 
                                                        'baseWeight' : "(%s)"%(yld_weight)
                                                  }
                                                  )    
        if getattr(cfg, "vetoTrainEvents", True):

            samples[samp].weights.weight_dict.update(  { 
                                                            
                                                           "mva_test_train_weight_factor":str( round(mva_weight_factor,3) ),
                                                           "vetoTrainEvents": "(!trainingEvent)" ,
                                                        }  )

        if setEvtList:
            samples[samp]['tree'].SetEventList(0)
            setEvtList=False
    print "Test/Train Events Summary written in: %s "%output
    f.close()
    del f




def yields(cfg, args):

    yields={}
    cut_weights = {}
    isMVASample = getattr(cfg, "isMVASample", False)
    redo_eventLists = "write" if getattr(cfg, "redo_eventLists", False) else "read"




    for cutInst in cfg.cutInstList:
        cutInstName = cutInst.name
        cut_name = cutInst.fullName
        #if cfg.signalList:
        #    signalList = ['s300_290','s300_270','s300_220']
        #else:
        #    signalList = []
        signalList = cfg.signalList
        sampleList = getattr(cfg, "bkgList") + signalList

        #if 'sr' in cut_name.lower():
        #    dataList = ['d']
        #elif ("cr" in cut_name.lower()) or ("sideband" in cut_name.lower()) or ( 'bins' in cut_name.lower()  ):
        #    dataList = ['dblind']
        #else:
        #    raise Exception("not sure which dataset to use! cut_name: %s"%cut_name)
        dataList = ['dblind']
        dataList = [getattr(args,'data')]
        if dataList[0] in cfg.samples.dataList():
            lumi = cfg.samples[dataList[0]].name +"_lumi"
        else:
            dataList = []
            lumi = "DataUnblind_lumi" # or "target_lumi"


        #cutSaveDir = cfg.saveDir + "/" + cutInst.saveDir
        #tableDir = cfg.tableDirs[cut_name]
        cutSaveDir = cfg.saveDirs[cut_name]
        data    = getattr(args, 'data' )
        useData = bool(data)
        if useData:
            cutSaveDir = cutSaveDir #+"/%s/"%cfg.samples[data].name
        else:
            cutSaveDir = cutSaveDir + "/MC/"
        tableDir = cutSaveDir +"/Tables/"
            

        

        yield_pkl= cfg.yieldPkls[cut_name]
        cut_weight_pkl= cfg.yieldPkls[cut_name].replace("/Yields_","/CutWeights_")
        makeDir(tableDir)
        makeDir(yield_pkl)
        redo_yields = args.redo_yields if args.redo_yields else cfg.redo_yields    # if args redo_yields overpower the cfg redo yields

        
    
    
    
        nProc   =   getattr(args, "nProc", 1) 
        #nProc   =   min(len(signalList) -1 , getattr(cfg, "nProc", 16) ) 
        nProc   =   min(nProc, 16)    ## num processess shouldn't be too much more than twice the number of cores ( according to the internets )
        limits  =   {}
        #yield_pkl =  cfg.results_dir + "/%s/Yields_%s_%s.pkl"%(cutInst.fullName , cfg.runTag , cfg.scan_tag)
        #yield_pkl   =   getattr(cfg, "yield_pkl", cfg.yield_pkl  )  ##huh?
        if os.path.isfile(yield_pkl) and not redo_yields:
                print "\n reading Yields from pickle: %s \n"%yield_pkl
                yields[cut_name] = pickle.load(file(yield_pkl)) 
                if hasattr( yields[cut_name] , "cut_weights" ):
                    print "This Yield Class has a cut_weights attached to it which is large! I will detach it and pickle it seperately!"
                    cut_weights[cut_name] = yields[cut_name].cut_weights
                    pickle.dump( cut_weights[cut_name], file(cut_weight_pkl, 'w') )
                    delattr( yields[cut_name] , 'cut_weights' )
                    pickle.dump( yields[cut_name], file(yield_pkl, 'w') )
                    print cut_weight_pkl
                    print  
                else:
                    #
                    #cut_weights[cut_name] = pickle.load(file(cut_weight_pkl,'w')) 
                    cut_weights[cut_name] = cut_weight_pkl 
                redo_plots_tables = True
        else:
            print "\n Will (re)create yields and pickle to: %s \n"%yield_pkl
            
            #if not isMVASample:
            #    setEventListToChains(cfg.samples, sampleList , cutInst.baseCut, opt=redo_eventLists )
                #seteventlists(cfg,args, cutInst)
            makeDir(yield_pkl)
            yields[cut_name]=Yields(     
                                        cfg.samples, 
                                        sampleList + dataList, 
                                        cutInst, 
                                        #cutOpt          =   "list2", 
                                        #cutOpt          =   "list2", 
                                        cutOpt          =   "list2", 
                                        weight          =   "",
                                        lumi            =   lumi,  
                                        pklOpt          =   True, 
                                        tableName       =   "{cut}_%s"%(cfg.runTag), 
                                        nDigits         =   10 , 
                                        err             =   True , 
                                        verbose         =   True,
                                        isMVASample     =   isMVASample, 
                                        cuts            =   [cfg.cuts, cutInstName ],
                                        nProc           =   nProc, 
                                     useELists          =   True,
                                   )
            cut_weights[cut_name] = yields[cut_name].cut_weights
            delattr( yields[cut_name], "cut_weights")
            pickle.dump( cut_weights[cut_name] , file(cut_weight_pkl ,'w')  ) 
            pickle.dump( yields[cut_name], open(yield_pkl,'w') )
            print "Yield pickle dumped: %s"%yield_pkl


        redo_plots_tables = False
        if redo_plots_tables:
            #pp.pprint(      yields[cut_name].cut_weights  ,       open( cutSaveDir +"/cuts_weights.txt" ,"w"), width = 100, indent = 4 )
            #pickle.dump(    yields[cut_name].cut_weights ,        open( cutSaveDir +"/cuts_weights.pkl" ,"w") )
            pp.pprint(      cut_weights[cut_name]  ,       open( cutSaveDir +"/cuts_weights.txt" ,"w"), width = 100, indent = 4 )
            #pickle.dump(    cut_weights[cut_name] ,        open( cutSaveDir +"/cuts_weights.pkl" ,"w") )




            #combineBkgs = [ ["DYJetsM50", "ZJetsInv", "QCD","ST","Diboson"] , "Other" ] 
            #seperators  = [  "DataBlind", "Total" ]

            others= ['dy', 'z', 'qcd', 'st','vv']
            
            combineBkgs =[ [ yields[cut_name].sampleNames[bkg] for bkg in others], "Other"]

            seperators  = [  yields[cut_name].sampleNames[dataList[0]] , "Total" ]

            JinjaTexTable( yields[cut_name], pdfDir = tableDir, caption="" , transpose=True)
            JinjaTexTable( yields[cut_name], pdfDir = tableDir, outputName = yields[cut_name].tableName+"_T.tex", caption="" , noFOM=True, transpose=False, seperators = seperators)
            JinjaTexTable( yields[cut_name], pdfDir = tableDir, outputName = yields[cut_name].tableName+"_CombinedBKG.tex", caption="" , noFOM=True, transpose=True , combineBkgs = combineBkgs)
            JinjaTexTable( yields[cut_name], pdfDir = tableDir, outputName = yields[cut_name].tableName+"_CombinedBKG_T.tex", caption="" , noFOM=True, transpose=False, combineBkgs = combineBkgs      , seperators = seperators)
            JinjaTexTable( yields[cut_name], pdfDir = tableDir, outputName = yields[cut_name].tableName+"FOM_CombinedBKG_T.tex", caption="" , noFOM=False, transpose=False , combineBkgs = combineBkgs , seperators = seperators)
            #drawYields( cut_name , cfg.yieldPkls[cut_name] , sampleList = cfg.bkgList  + ['s300_290' , 's300_270','s300_220'] , keys=[] , ratios=True , save= cfg.cutSaveDirs[cut_name] )
            
            yldplts = {}

            yldplts[1] = drawYields("BkgComp_%s"%cut_name, yields[cut_name] , sampleList = cfg.bkgList , ratios= False, save= cutSaveDir , normalize = True, logs = [0,0], plotMin=0, plotMax = 1.)
            yldplts[2] = drawYields("BkgVsData_%s"%cut_name, yields[cut_name] , sampleList = cfg.bkgList + dataList, ratios= True, save= cutSaveDir , normalize = False, logs = [0,0], plotMin=0)
            yldplts[3] = drawYields("BkgVsData_log_%s"%cut_name, yields[cut_name] , sampleList = cfg.bkgList + dataList, ratios= True, save = cutSaveDir, normalize = False, logs = [0,1], plotMin=0.1)

            if signalList:
                yldplts[4] = drawYields("BkgVsSig_%s"%cut_name, yields[cut_name] , sampleList = cfg.bkgList + signalList, ratios= True, save= cutSaveDir , normalize = False, logs = [0,1], plotMin=0.1)
                yldplts[5] = drawYields("BksVsDataVsSignal_%s"%cut_name, yields[cut_name] , sampleList = cfg.bkgList + dataList + signalList , ratios= True, save= cutSaveDir, normalize = False, logs = [0,1], plotMin=0.1)

            crbins = [x for x in yields[cut_name].cutNames if 'ECR' in x]

            yldplts[6] = drawYields("BkgVsData_ECR_log_%s"%cut_name, yields[cut_name] , sampleList = cfg.bkgList + dataList, keys=crbins, ratios= True, save= cutSaveDir, normalize = False, logs = [0,1], plotMin=0.1)

            #yldplts = [ yldplt1,yldplt2, yldplt3, yldplt4, yldplt5, yldplt6 ]


            yld = yields[cut_name] 
            yld.verbose = False
            print "\n Latex Table: \n"
            print yld.makeLatexTable( yld.makeNumpyFromDict( yld.yieldDictFull , rowList = list( reversed( cfg.bkgList ) )   + ['Total']+ dataList ) )
            print "\n Transvered: \n "
            print yld.makeLatexTable( yld.makeNumpyFromDict( yld.yieldDictFull , rowList = list( reversed( cfg.bkgList ) )   + ['Total']+ dataList ).T )


            doOthers = False
            if doOthers:
                other = dict_operator( yld.yieldDictFull , keys = [ bkg for bkg in cfg.bkgList if bkg not in ['tt','w']] , func = yield_adder_func2 )
                yld.yieldDictFull['Other'] = other
                print "\n Other BKG combined: \n "
                print yld.makeLatexTable( yld.makeNumpyFromDict( yld.yieldDictFull , rowList = ['w','tt','Other','Total']+ dataList ) )
                print "\n Transvered: \n "
                print yld.makeLatexTable( yld.makeNumpyFromDict( yld.yieldDictFull , rowList = ['w','tt','Other','Total']+ dataList ).T )
                tmp_ = yld.yieldDictFull.pop("Other")
        else:
            yldplts = []

            #yldplts
    #postFuncs = getattr(args, "postFuncs", None)
    #if postFuncs:
    #    print "Will run the following scripts: %s"%postFuncs
    #    #CR_SFs(cfg,args)
    #    for f in postFuncs:
    #        pass
    #        #print f
    #        #print(f+"(cfg,args)")
    #        #exec(f+"(cfg,args)")
    #            #print open(f).read() 
    #            #print "running %s"%f
    #            #execfile(f)    
    #            #exec(open(f).read() ,globals() ) 
    #            #execfile("CR_SFssss.py")    
                
    
    
    return yields, yldplts



bkg_est = yields





def pu_syst(cfg, args):
    #for weight in pu_weights():
    #    pass    
    return 




def cut_flow(cfg, args):

    yields={}
    #sampleList = getattr(cfg, "sampleList") +  
    if cfg.signalList:
        signalList = ['s300_290', 's300_270', 's300_220']
    #else:
    #    signalList = cfg.signalList
    #sampleList = getattr(cfg, "bkgList") +  getattr(cfg, "signalList")
    sampleList = getattr(cfg, "bkgList") +  signalList
    isMVASample = getattr(cfg, "isMVASample", False)
    redo_eventLists = "write" if getattr(cfg, "redo_eventLists", False) else "read"
    for cutInst in cfg.cutInstList:
        cut_name = cutInst.fullName
        tableDir = cfg.tableDirs[cut_name]
        yield_pkl= cfg.yieldPkls[cut_name]
        cutSaveDir = cfg.saveDirs[cut_name]
        makeDir(tableDir)
        makeDir(yield_pkl)
        redo_yields = args.redo_yields if args.redo_yields else cfg.redo_yields    # if args redo_yields overpower the cfg redo yields

        
        pp.pprint(      {    sample_name:decide_weight2(samp, weight=None, cut=cutInst.fullName, lumi='target_lumi' ) for sample_name, samp in cfg.samples.iteritems() if sample_name in sampleList} ,
                         open( cutSaveDir+"/weights.txt" ,"w") )
        pp.pprint(      cutInst.list ,  open( cutSaveDir +"/cuts.txt" ,"w"), width = 100, indent = 4 )
        pickle.dump(    cutInst,        open( cutSaveDir +"/%s.pkl"%cutInst.fullName ,"w") )
    
         
    
    
        nProc   =   getattr(cfg, "nProc", 16) 
        #nProc   =   min(len(signalList) -1 , getattr(cfg, "nProc", 16) ) 
        nProc   =   min(nProc, 16)    ## num processess shouldn't be too much more than twice the number of cores ( according to the internets )
        limits  =   {}
        #yield_pkl =  cfg.results_dir + "/%s/Yields_%s_%s.pkl"%(cutInst.fullName , cfg.runTag , cfg.scan_tag)

        #yield_pkl   =   getattr(cfg, "yield_pkl", cfg.yield_pkl  )  ##huh?
        if os.path.isfile(yield_pkl) and not redo_yields:
                print "reading Yields from pickle: %s"%yield_pkl
                yields[cut_name] = pickle.load(file(yield_pkl)) 
        else:
            if not isMVASample:
                setEventListToChains(cfg.samples, sampleList , cutInst.baseCut, opt=redo_eventLists )
            makeDir(yield_pkl)
            yields[cut_name]=Yields(     
                                        cfg.samples, 
                                        sampleList , 
                                        cutInst, 
                                        cutOpt          =   "list", 
                                        weight          =   "", 
                                        pklOpt          =   True, 
                                        pklDir          =   cfg.yieldPklDir, 
                                        tableName       =   "{cut}_%s"%(cfg.runTag), 
                                        nDigits         =   10 , 
                                        err             =   True , 
                                        verbose         =   True,
                                        isMVASample             =   isMVASample, 
                                   )
            pickle.dump( yields[cut_name], open(yield_pkl,'w') )
            print "Yield pickle dumped: %s"%yield_pkl
        combineBkgs = [ ["DYJetsM50", "ZJetsInv", "QCD","ST","Diboson"] , "Other" ] 
        seperators = ["CT300", "ISR325"]
        JinjaTexTable( yields[cut_name], pdfDir = tableDir, caption="" , transpose=True)
        JinjaTexTable( yields[cut_name], pdfDir = tableDir, outputName = yields[cut_name].tableName+"_T.tex", caption="" , noFOM=True, transpose=False, seperators = seperators)
        JinjaTexTable( yields[cut_name], pdfDir = tableDir, outputName = yields[cut_name].tableName+"_CombinedBKG.tex", caption="" , noFOM=True, transpose=True , combineBkgs = combineBkgs)
        JinjaTexTable( yields[cut_name], pdfDir = tableDir, outputName = yields[cut_name].tableName+"_CombinedBKG_T.tex", caption="" , noFOM=True, transpose=False, combineBkgs = combineBkgs      , seperators = seperators)
        JinjaTexTable( yields[cut_name], pdfDir = tableDir, outputName = yields[cut_name].tableName+"FOM_CombinedBKG_T.tex", caption="" , noFOM=False, transpose=False , combineBkgs = combineBkgs , seperators = seperators)
        #drawYields( cut_name , cfg.yieldPkls[cut_name] , sampleList = cfg.bkgList  + ['s300_290' , 's300_270','s300_220'] , keys=[] , ratios=True , save= cfg.cutSaveDirs[cut_name] )

    
    return yields




























#def data_plots(cfg,args):
def data_plots(cfg,args):

    nminus1s = getattr(cfg, "nminus1s", {})
    verbose  = getattr(cfg, "verbose", True)
    verbose  = True

    def getAndDrawFull(cutInst, bkgList, signalList,  data , plot , plotMin = 0.01 , plotDir = ""):
        mcList     = bkgList + signalList
        sampleList = mcList + [data]

        if verbose:
            print "----------"
            print cutInst
            print sampleList
            print "----------"
    
        postfix = "" 
        if cfg.isFancyCut: #Dealing with the EventLists for nminus1 plots
            def_nminus1s = getattr(cfg, "nminus1s",{})
            nminus_list = []
            if args.nMinus1:
                if plot in def_nminus1s:
                    print "in def nm1", def_nminus1s[plot]
                    nminus_list.extend( def_nminus1s[plot] )
                if type(cfg.plots[plot]['var']) ==  str :
                    nminus_list.append( cfg.plots[plot]['var'] )
                postfix = "_nminus1"
                eventListCutInst = False
            else:
                eventListCutInst = cutInst  
        else:
            if nminus1s.has_key(plot) and len(nminus1s[plot]) and nminus1s[plot][0]:
                nminus_list = nminus1s[plot]
                eventListCutInst = cutInst
                while eventListCutInst.baseCut:     ## get the most baseCut
                    eventListCutInst = eventListCutInst.baseCut
                if not eventListCutInst.nMinus1( nminus_list) == eventListCutInst.combined:   ## if baseCut still includes the Minus1 cut, then no eventList
                    eventListCutInst = None 
                #[samples[samp].tree.SetEventList(0) for samp in samples]
            else:
                eventListCutInst = cutInst
                nminus_list = []

        if verbose:
            print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
            print "Plot:", plot
            print "nMinus1List", nminus_list
            print eventListCutInst
            print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"

        #cutName = eventListCutInst.name
        #cut_weights = {cutName:{}}
        #for samp in mcList +[data]:
        #    cut_str, weight_str = cfg.cuts.getSampleFullCutWeights(cfg.samples[samp], [cutName] , nMinus1 = nminus_list )
        #    cut_weights[cutName][samp] = (cut_str, weight_str ) 
        #print cut_weights
        #if getattr(args, "setEventLists", True):
        #    #setEventListToChains( cfg.samples, mcList +[data] , eventListCutInst)
        #    #setEventListToChains(cfg.samples, mcList +[data] , cutInst.baseCut )
        #    #setEventListToChainWrapper( [chain_dict[samp] , samp, b, c, False, 'read'] )
        #    setEventListsFromCutWeights( cfg.samples, mcList +[data] , cut_weights, cutNames=[cutName], nProc = 15, redo = False , keep_chain_elist = True)
        if cfg.isFancyCut:
            #cutInst
            print 'nminus1 list:', nminus_list
            getPlots(cfg.samples, cfg.plots , [cfg.cuts, cutInst.name]  , sampleList = sampleList   , plotList=[plot] ,  nMinus1=nminus_list , addOverFlowBin='both',weight="" )
        else:
            getPlots(cfg.samples, cfg.plots , cutInst   , sampleList = sampleList      , plotList=[plot] , nMinus1=nminus_list , addOverFlowBin='both' , weight=""  )

        if bool(data) and not getattr(args,"fomplot", False):
            plt = drawPlots(cfg.samples,    cfg.plots , cutInst, sampleList = sampleList , # [ 'qcd','z','dy','tt','w','s300_250','s250_230' , 'dblind'],
                    plotList= [plot] ,save= plotDir, plotMin=plotMin , #mc_scale=1.05, 
                    normalize=False, denoms=["bkg"], noms=[data], fom="RATIO", fomLimits=[0,1.8], postfix = postfix )
        else: 
            if not signalList:
                raise Exception("No data or signal given... what ratio do you want")
            plt = drawPlots(cfg.samples,    cfg.plots , cutInst, sampleList = sampleList , # [ 'qcd','z','dy','tt','w','s300_250','s250_230' , 'dblind'],
                    plotList= [plot] ,save= plotDir, plotMin=plotMin,
                    normalize=False, denoms=["bkg"], noms=signalList, fom="AMSSYS", fomLimits=[] , postfix = postfix)
        
        print '\n==============================================================\n'
        print plt
        #print cut_weights
        print '\n==============================================================\n'

        gc.collect()
        return #plt

    result = {}
    ###
    ##cfg.cutInstList
    isFancyCut = True
    if hasattr(cfg.cuts, "getSampleCutWeight"):
        isFancyCut = True
    cfg.isFancyCut = isFancyCut
    for cutInst in cfg.cutInstList:
        cut_name = cutInst.fullName
        #print " . . . . . . . . . . . . . Cut: %s . . . . . . . . . . . . . . "%cut_name
        cutSaveDir = cfg.saveDir + "/" + cutInst.saveDir
        data    = getattr(args, 'data' )
        useData = bool(data)
        if useData and not getattr(args,"fomplot", False):
            plotDir = cutSaveDir 
        elif getattr(args,"fomplot", False):
            plotDir = cutSaveDir + "/FOMPlots/"

        signalList = getattr(cfg, "signalList", [] )
        sampleList = cfg.bkgList + signalList #cfgsample_info['sampleList']  + cfg.signalList 
        print "------------------- - - -- - --- - - - -- ", sampleList  
        result[cut_name]={}
        plotMin =  0.01 if "SR" in cut_name else 1.0
        for plot in cfg.plotList:
            result[cut_name][plot]  = getAndDrawFull(cutInst, bkgList = cfg.bkgList, signalList = signalList, data = data , plot = plot , plotMin = plotMin , plotDir = plotDir)
            #result[cut_name][plot]  = drawPlots(cfg.samples,    cfg.plots , cutInst, sampleList = sampleList +[data],
            #                                    plotList= [plot] ,save= plotDir, plotMin=plotMin,
            #                                    normalize=False, denoms=["bkg"], noms=[data], fom="RATIO", fomLimits=[0,2.8])
            print "Printing the Results ++++++++++++++++++++++++++++++++++++",
            print result[cut_name][plot]
            #print "results:", cutInst.fullName, plot
            #pp.pprint( result) 





def get_plots(cfg,args):
    nminus1s = getattr(cfg, "nminus1s", {})
    verbose  = getattr(cfg, "verbose", True)
    verbose  = False


    result = {}
    for cutInst in cfg.cutInstList:
        cut_name = cutInst.fullName
        cutSaveDir = cfg.saveDir + "/" + cutInst.saveDir
        plotDir = cutSaveDir +"/DataPlots/"
        result[cut_name]={}
        data = 'd' if 'SR' in cut_name else 'dblind'   ## safeside : 'dblind' if 'CR' in cut_name else 'd'
        plotMin =  0.01 if "SR" in cut_name else 1.0
        for plot in cfg.plotList:
            #result[cut_name][plot]  = getAndDrawFull(cutInst, mcList = sampleList, data = data , plot = plot , plotMin = plotMin , plotDir = plotDir)
            result[cut_name][plot]  = drawPlots(cfg.samples,    cfg.plots , cutInst, sampleList = cfg.sampleList +[data],
                                                plotList= [plot] ,save= plotDir, plotMin=plotMin,
                                                normalize=False, denoms=["bkg"], noms=[data], fom="RATIO", fomLimits=[0,2.8])
            print "Printing the Results ++++++++++++++++++++++++++++++++++++",
            print result[cut_name][plot]
            #print "results:", cutInst.fullName, plot
            #pp.pprint( result) 

    return result 




#
#   Background Estimation Tools 
#
def setEventListToChainsParal(cfg,args):
    postfix = "" 
    if cfg.isFancyCut: #Dealing with the EventLists for nminus1 plots
        def_nminus1s = getattr(cfg, "nminus1s",{})
        nminus_list = []
        if args.nMinus1:
            if plot in def_nminus1s:
                print "in def nm1", def_nminus1s[plot]
                nminus_list.extend( def_nminus1s[plot] )
            if type(cfg.plots[plot]['var']) ==  str :
                nminus_list.append( cfg.plots[plot]['var'] )
            postfix = "_nminus1"
            #postfix = "_nminus_" + '_'.join(nminus_list)
            eventListCutInst = False
        else:
            eventListCutInst = cutInst  
    else:
        if nminus1s.has_key(plot) and len(nminus1s[plot]) and nminus1s[plot][0]:
            nminus_list = nminus1s[plot]
            eventListCutInst = cutInst
            while eventListCutInst.baseCut:     ## get the most baseCut
                eventListCutInst = eventListCutInst.baseCut
            if not eventListCutInst.nMinus1( nminus_list) == eventListCutInst.combined:   ## if baseCut still includes the Minus1 cut, then no eventList
                eventListCutInst = None 
            #[samples[samp].tree.SetEventList(0) for samp in samples]
        else:
            eventListCutInst = cutInst
            nminus_list = []
    return { 'eventListCutInst' : eventListCutInst, 'nminus_list' :nminus_list , 'postfix': postfix }



def CR_SFs(cfg,args):
    sig1           =    'S300-270Fast'
    sig2           =    'S300-240Fast'

    #dy      = '#Z/\\gamma^{*} +jets'
    dy      = '$Z/\\gamma^{*} +jets$'
    qcd     = 'QCD'
    st      = 'Single top'
    #tt      = 'TTJets'
    tt_1l   = 'TT-1l'
    tt_2l   = 'TT-2l'
    vv      = 'VV'
    w       = 'WJets'
    #z       = '#Z\\rightarrow \\nu\\nu+jets'
    z       = '$Z\\rightarrow \\nu\\nu+jets$'


    #otherBkg       = ['DYJetsM50', "QCD", "ZJetsInv", "ST", "Diboson"]
    otherBkg       = [ dy, qcd, z, st, vv]
    #allBkg         = [w,tt] + otherBkg
    allBkg         = [w,tt_1l, tt_2l] + otherBkg


    #otherBkg       = ['DYJetsM50', "QCD", "ZJetsInv", "ST", "Diboson"]
    #allBkg         = [w,tt] + otherBkg
    data           = cfg.samples[args.data]['name']
    sigs           = [sig1, sig2]
    sigs = []
    allSamps       = allBkg + sigs + [data]
    #side_band_name = task_ret['bkg_est'][0].keys()[0]
    side_band_name = cfg.cutInstList[0].fullName
    
    #mtabc       = ["a","b","c"]
    #pts         = ["sr","cr"]
    
    #bkg_est_dir = "$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/results/2016/%s_%s_%s/BkgEst/"%(cfg.cmgTag, cfg.ppTag, cfg.runTag) 
    #bkg_est_dir = "$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/results/2016/%s/%s/%s/BkgEst/"%(cfg.cmgTag, cfg.ppTag, cfg.runTag) 
    bkg_est_dir = "/%s/BkgEst/"%(cfg.results_dir ) 
    bkg_est_dir = os.path.expandvars( bkg_est_dir ) 
    makeDir(bkg_est_dir)
    
    yld_pkl = cfg.yieldPkls[side_band_name]
    #yld = task_ret['bkg_est'][0][side_band_name]
    yld = pickle.load( file(yld_pkl) ) 
    yldDict = yld.getNiceYieldDict()
    
    
    sampleMCFraction = lambda s : dict_manipulator( [ yldDict[b] for b in [s,'Total'] ] , func = (lambda a,b: "%s"%round((a/b).val*100,2) ))
    sampleFractions = { s:sampleMCFraction(s) for s in  sigs +[w,tt_2l, tt_1l] }
    yldsByBins = yld.getByBins(yieldDict=yldDict)
    #def dict_operator ( yldsByBin , keys = [] , func =  lambda *x: sum(x) ):
    #    """
    #    use like this dict_operator( yields_sr, keys = ['DataBlind', 'Total'] , func = lambda a,b: a/b)
    #    """ 
    #    args = [ yldsByBin[x] for x in keys]
    #    return func(*args) 
    table_legend = [  "region" , "sig_cont_sr", "sig_cont_cr", "w_frac", "w_sf_cr", "closure"  ] 
    
    first_row = True
    tt_table_list = []
    
    corrected_yields = {}
    
    ##FIX ME
    regions = [x for x in yld.cutNames if "cr" in x]
    region_names = regions
    tt_region_names = [x for x in region_names if "crtt" in x ]
    w_region_names  = [x for x in region_names if x not in tt_region_names]
    ##
    ## TT SideBand
    ##
    
    tt_table_list.append(["\hline"])
    
    
    
    #tt_sf_crtt     = dict_operator ( yldsByBins[tt_region_names[0]] , keys = [ data , w, tt] + otherBkg  , func = lambda a,b,c,*d: (a-b-sum(d))/c)
    tt_sf_crtt     = dict_operator ( yldsByBins[tt_region_names[0]] , keys = [ data , w, tt_1l, tt_2l] + otherBkg  , func = lambda a,b,tt1,tt2,*d: (a-b-sum(d))/(tt1+tt2) )
    
    cr_sf_dict = {} 
    for region_name in region_names:
            region   = region_name
            yields = yldsByBins[region]
            otherSum = dict_operator ( yields , keys = otherBkg )
            #yield_tt = yields[tt]
            yield_tt = yields[tt_1l] + yields[tt_2l]
            MCTTFrac = yield_tt / yields['Total']  * 100  
    
            if region in tt_region_names:
                w_sf = "-"
                tt_sf = tt_sf_crtt.round(2)
            else:
                #w_sf     = dict_operator ( yldsByBins[region] , keys = [ data ,  tt, w] + otherBkg  , func = lambda a,b,c,*d: (a-b*tt_sf_crtt-sum(d))/c).round(2)
                w_sf     = dict_operator ( yldsByBins[region] , keys = [ data ,  tt_1l , tt_2l , w] + otherBkg  , func = lambda a,tt1,tt2 ,c,*d: (a-(tt1+tt2)*tt_sf_crtt-sum(d))/c).round(2)
                tt_sf    = "-" #, u_float( 1. )
            cr_sf_dict[region]={  
                                    #tt  : (tt_sf if not tt_sf == "-" else u_float(1.))   , 
                                    tt_1l  : (tt_sf if not tt_sf == "-" else u_float(1.))   , 
                                    tt_2l  : (tt_sf if not tt_sf == "-" else u_float(1.))   , 
                                    w   : (w_sf  if not  w_sf == "-" else u_float(1.))  ,
                               } 
            toPrint = [   
                          ["Region",                fix_region_name( region_name )], 
                          ['SFCR W'    , w_sf  ],
                          ['SFCR TT'   , tt_sf  ],
    
                       ]#dataCR( dataMCsf * yldDict[tt][region]).round(2)  ]
    
    
            align = "{:<15}"*len(toPrint)
    
            if first_row:
                print align.format(*[x[0] for x in toPrint])
                first_row = False
                tt_table_list.append( [x[0] for x in toPrint]  ) 
    
            print align.format(*[x[1] for x in toPrint])
            tt_table_list.append( [x[1] for x in toPrint])

    cutSaveDir = cfg.saveDirs[side_band_name]
    #cutSaveDir = cutSaveDir +"/%s/"%cfg.dataTag #cfg.samples[data].name
    
    pickle.dump( cr_sf_dict ,   open( bkg_est_dir + "/CR_SFs.pkl", "w")  ) 
    table = makeSimpleLatexTable( tt_table_list, "CR_ScaleFactors.tex", cutSaveDir )
    
    #print table

    print "CR_SFs stored in: " 
    print bkg_est_dir + "/CR_SFs.pkl"



