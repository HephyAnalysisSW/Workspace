from Workspace.HEPHYPythonTools.helpers import getYieldFromChain
from Workspace.HEPHYPythonTools.u_float import u_float
import pickle
from Workspace.DegenerateStopAnalysis.tools.degTools import cmsbase, getEfficiency, getPlots, drawPlots , saveCanvas, setEventListToChains , makeDir , decide_weight2 , JinjaTexTable, Yields, CutClass , setMVASampleEventList , drawYields 
import Workspace.DegenerateStopAnalysis.tools.limitTools as limitTools

import pprint as pp
import re , os
import multiprocessing
#from subprocess import call
import subprocess 

def round_(val, nDigit):
    if hasattr(val, "round"):
        return getattr(val, "round")(nDigit)
    else:
        return round(val, nDigit)
def str_round(val, nDigit):
    return str(round_(val, nDigit))


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








def bdt_eff(cfg, args):
    #cutInst_tot = getattr(cfg,"cutInst_total", cfg.cutInstList[-1])
    res = {}
    #effPlotDir = cfg.saveDir + "/EffPlots/"
    for cutInst in cfg.cutInstList:
        getPlots(cfg.samples, cfg.plots , cutInst, sampleList= cfg.plotSampleList   , plotList= cfg.plotList , nMinus1=None , addOverFlowBin='both',weight="weight" )
    for samp in cfg.plotSampleList:
        for cutInst in cfg.cutInstList:
            #cutInst_tot = cutInst.baseCut
            cutInst_tot = cutInst.baseCut
            c_ = re.search( 'DM_(.*)_SR|DM_(.*)_CR' , cutInst.fullName)
            foundCutInstTot = False
            if c_ and c_.group(1):
                cutInst_tot_name = cutInst.fullName.replace("_"+c_.group(1),"")
                cutInst_tot = filter( lambda x: x.fullName == cutInst_tot_name, cfg.cutInstList)
                if cutInst_tot:
                    cutInst_tot = cutInst_tot[0]
                    foundCutInstTot = True
                else: print cutInst_tot_name, cutInst_tot
            if not foundCutInstTot:
                print "cant determine the total cutInst....skipping %s"%cutInst.fullName
                continue

            #if not cutInst.baseCut in cfg.cutInstList:
            #    print cutInst_tot.fullName, " not included in the cutInstList...  will be skipped!"
            #    continue
            cut_name = cutInst.fullName
            res[cut_name] = {}
            for plot in cfg.plotList:
                getEfficiency(cfg.samples, samp, plot, cutInst, cutInst_tot, ret=False )

    for cutInst in cfg.cutInstList:
        cutInst_tot = cutInst.baseCut
        c_ = re.search( 'DM_(.*)_SR|DM_(.*)_CR' , cutInst.fullName)
        foundCutInstTot = False
        
        if c_ and c_.groups() :
            for c__ in c_.groups():
                if c__:
                    string = c__
                    break
            print string , c_.groups()
            cutInst_tot_name = cutInst.fullName.replace("_"+string,"")
            cutInst_tot = filter( lambda x: x.fullName == cutInst_tot_name, cfg.cutInstList)
            if cutInst_tot:
                cutInst_tot = cutInst_tot[0]
                foundCutInstTot = True
            else: print cutInst_tot_name, cutInst_tot
        if not foundCutInstTot:
            print "cant determine the total cutInst....skipping %s"%cutInst.fullName
            continue

        #cutInst_tot = cutInst.baseCut
        cut_name = cutInst.fullName
        cutSaveDir = cfg.saveDir + "/" + cutInst.saveDir
        effPlotDir = cutSaveDir + "/EffPlots/"

        for plot in cfg.plotList:
            res[cut_name][plot] = drawPlots(  cfg.samples, cfg.plots, cutInst, sampleList = cfg.plotSampleList,  plotList = [plot] , save=False, plotMin=0.01,  normalize=False, denoms=['bkg'], noms=cfg.noms , fom="RATIO", fomLimits=[0,1.05] )
            res[cut_name][plot]['canvs'][plot][2].cd()
            dOpt=""

            first = cfg.samples[samp]['cuts'][cut_name][plot].Clone()
            first.Reset()
            first.GetYaxis().SetTitle("#frac{%s}{%s}"%(cut_name, cutInst_tot.fullName))
            first.GetYaxis().SetTitleOffset(1.0)
            first.Draw()
            
            dOpt = "same"
            for samp in cfg.plotSampleList:
                eff_plot_name = '%s_EFF_%s_WRT_%s'%(plot, cutInst.fullName, cutInst_tot.fullName)
                cfg.samples[samp]['plots'][eff_plot_name].Draw(dOpt)
            res[cut_name][plot]['canvs'][plot][2].Update()
            
            saveCanvas(res[cut_name][plot]['canvs'][plot][0], effPlotDir, eff_plot_name  )
                
        
    return res 
#plt = drawPlots(  samples, cfg.plots, "EFF_BDT_ALL_WRT_BDT_ALL" , sampleList = cfg.plotSampleList,  plotList =[ plot ] , save=effDir, plotMin=0.01,  normalize=False, denoms=[], noms=[], fom=False, fomLimits=[] )







def calc_mva_limit(cfg, args):

    yields={}
    signalList = getattr(cfg, "signalList", cfg.samples.massScanList() )
    sampleList = getattr(cfg, "sampleList") +  signalList

    isMVASample = getattr(cfg, "isMVASample", False)
    redo_eventLists = "write" if getattr(cfg, "redo_eventLists", False) else "read"
    sys_pkl      = getattr(cfg, "sys_pkl", None)
    sys_map      = getattr(cfg, "sys_map",      {} )
    new_bins_map = getattr(cfg, "new_bins_map", {} )
    print "---sigList" , signalList
    print "---sampleList",sampleList
    print "---SampleList2", getattr(cfg, "sampleList")
    for cutInst in cfg.cutInstList:
        ##
        cut_name = cutInst.fullName
        print " . . . . . . . . . . . . . Cut: %s . . . . . . . . . . . . . . "%cut_name
        cutSaveDir = cfg.saveDir + "/" + cutInst.saveDir
        tableDir = cutSaveDir +"/Tables/"
        limitDir = cutSaveDir +"/Limits/"
        cardDir = cfg.cardDir + "/" + cutInst.saveDir
        print "card dir:", cardDir
        makeDir(cardDir)
        makeDir(tableDir)
        makeDir(limitDir)
        

        pp.pprint(      {    sample_name:decide_weight2(samp, weight=None, cut=cutInst.fullName, lumi='target_lumi' ) for sample_name, samp in cfg.samples.iteritems() } ,
                         open( limitDir+"/weights.txt" ,"w") )
        pp.pprint(      cutInst.list ,  open( limitDir+"/cuts.txt" ,"w"), width = 100, indent = 4 )
        pickle.dump(    cutInst,        open( limitDir+"/%s.pkl"%cutInst.fullName ,"w") )
    
    
        ##
        #cfg.cutInst.name = cfg.runTag
    
        def getValueFromDict(x, val="0.500", default=999):                                                                                                    
            try:                                      
                ret = x[1][val]
            except KeyError:
                    ret = default
            except TypeError:
                    ret = default 
            return float(ret)
    
    
        redo_limit  = args.redo_limit  if args.redo_limit  else cfg.redo_limit    # if args redo_limit overpower the cfg redo limit
        redo_yields = args.redo_yields if args.redo_yields else cfg.redo_yields    # if args redo_yields overpower the cfg redo yields
    
        print "----------------------------------"
        print args.redo_limit , args.redo_yields
        print cfg.redo_limit  , cfg.redo_yields
        print redo_limit      , redo_yields #, redo_eventLists
        print "----------------------------------"
    
    
        limit_pkl =  cfg.limitPkls[cut_name] #cfg.cardDir +"/"+ cutInst.baseCut.saveDir +"/Limits_%s_%s.pkl"%(cfg.runTag, cutInst.fullName)
        yield_pkl =  cfg.yieldPkls[cut_name] #cfg.cardDir +"/"+ cutInst.baseCut.saveDir +"/Yields_%s_%s.pkl"%(cfg.runTag, cutInst.fullName)
        if os.path.isfile(limit_pkl) and not redo_limit:
            print "---- Reading Limit Dict from: %s"%limit_pkl
            limits = pickle.load( file(limit_pkl) )
            pp.pprint(limits) 
        else:
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
                                            cutOpt          =   "list2", 
                                            weight          =   "weight", 
                                            pklOpt          =   True, 
                                            tableName       =   "{cut}_%s%s"%(cfg.runTag,cfg.scan_tag), 
                                            nDigits         =   2 , 
                                            err             =   True , 
                                            verbose         =   True,
                                            isMVASample             =   isMVASample, 
                                       )
                pickle.dump( yields[cut_name], open(yield_pkl,'w') )
                print "Yield pickle dumped: %s"%yield_pkl
                JinjaTexTable( yields[cut_name], pdfDir = tableDir, caption="" , transpose=True)
            yldplts = drawYields( "BkgComposition_" +cut_name , cfg.yieldPkls[cut_name] , sampleList = cfg.bkgList  + ['s300_290' , 's300_270','s300_220'] , keys=[] , ratios=True , save= cfg.saveDirs[cut_name] )
    
            def makeSignalCard(sig):
                lim =  limitTools.getLimit(
                                   yields[cut_name]      , 
                                   sig = sig            , 
                                   outDir =  cardDir, 
                                   postfix = ""         , 
    
                                   defWidth        = 15 , 
                                   maxUncNameWidth = 25 , 
                                   maxUncStrWidth = 20  , 
                                   percision       = 6  ,   
    
                                   calc_limit = False   ,

                                   sys_uncorr = 1.2     ,
                                   sys_corr   = 1.06    ,

                                   sys_pkl       = sys_pkl,
                                   new_systs_map = sys_map,
                                   new_bins_map  = new_bins_map,
                                   #new_systs_map = getattr(cfg, 'new_systs_map',{} ),
                               ) 
                mstop, mlsp = [int(x) for x in sig[1:].rsplit("_")]
        
                #print "---------------------------------------- %s , %s -------------------------------"%(mstop,mlsp)
                return mstop, mlsp ,  lim
    
            if args.only_yields:
                raise Exception("Not calculating limits! for limit calculation run without --only_yields")

            
    
               
            if nProc>=1:
                ###########################################            Multiprocessing part
                #pool    =   multiprocessing.Pool( processes = nProc )
                #results = pool.map(getSigLimit, signalList )
                #pool.close()
                #pool.join()
                
                # make cards but calc limits seperately
                cards = map( makeSignalCard, signalList)
            
                #limit_calc_script_dir = "/afs/hephy.at/user/n/nrad/CMSSW/CMSSW_7_4_12_patch4/src/Workspace/DegenerateStopAnalysis/python/tools/"
                limit_calc_script_dir = cmsbase + "/src/Workspace/DegenerateStopAnalysis/python/tools/"
                limit_calc_script = limit_calc_script_dir + 'calc_cards_limit.py'
                commands = [limit_calc_script, "%s/T2*4bd*%s*%s*.txt"%(cardDir,cutInst.fullName,cfg.runTag) , limit_pkl]

                print "command:", ' '.join(commands)
                subprocess.call(commands)

                if os.path.isfile(limit_pkl):
                    print "---- Ran Limit Calc and Saved LimitDict: %s"%limit_pkl
                    limits = pickle.load( file(limit_pkl) )
                else:
                    raise Exception( "Ran Limit Calc, but no output found :\n command: %s \n output: %s \n"%(' '.join(commands) , limit_pkl) )

                ########################################### 
            else:
                results = map( makeSignalCard, signalList)
    
                for mstop, mlsp, lim in results:
                    try: 
                        limits[mstop]
                    except KeyError:
                        limits[mstop]   = {}
                    limits[mstop][mlsp] = lim
    
            
                pickle.dump( limits, open(limit_pkl,'w') )
        print "---------------------------------- LIMIT CALCULATION FINISHED -----------------------------------------"
        canv , exclplot = limitTools.drawExpectedLimit( 
                                                            limits , 
                                                            #plotDir = cfg.saveDir+"/"+cutInst.saveDir+"/ExpectedLimit_%s.png"%( cfg.lumi_tag ) , 
                                                            plotDir = limitDir+"/ExpectedLimit_%s.png"%( cfg.lumi_tag ) , 
                                                            bins = None , 
                                                            key  = getValueFromDict ,
                                                                      )


        write_tfile = False
        if write_tfile:                                               
            canv.SetName( "ExpectedLimit_%s_%s_%s.pkl"%(cfg.htString,cfg.runTag,cfg.lumi_tag ) )
    
            tfile.cd()
            canv.Write()
            tfile.Close()
    return limits


def bkg_est(cfg, args):

    yields={}
    isMVASample = getattr(cfg, "isMVASample", False)
    redo_eventLists = "write" if getattr(cfg, "redo_eventLists", False) else "read"
    for cutInst in cfg.cutInstList:
        cut_name = cutInst.fullName
        sampleList = getattr(cfg, "bkgList") + getattr(cfg,"signalList")

        if "CR" in cut_name or "sideband" in cut_name.lower():
            dataList = ['dblind']
        else:
            dataList = ['d']


        lumi = cfg.samples[dataList[0]].name +"_lumi"
        tableDir = cfg.tableDirs[cut_name]
        yield_pkl= cfg.yieldPkls[cut_name]
        cutSaveDir = cfg.saveDirs[cut_name]
        makeDir(tableDir)
        makeDir(yield_pkl)
        redo_yields = args.redo_yields if args.redo_yields else cfg.redo_yields    # if args redo_yields overpower the cfg redo yields

        
        pp.pprint(      {    sample_name:decide_weight2(samp, weight=None, cut=cutInst.fullName, lumi=lumi ) for sample_name, samp in cfg.samples.iteritems() if sample_name in sampleList} ,
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
                                        sampleList + dataList, 
                                        cutInst, 
                                        cutOpt          =   "list2", 
                                        weight          =   "weight",
                                        lumi            =   lumi,  
                                        pklOpt          =   True, 
                                        tableName       =   "{cut}_%s%s"%(cfg.runTag,cfg.scan_tag), 
                                        nDigits         =   2 , 
                                        err             =   True , 
                                        verbose         =   True,
                                        isMVASample             =   isMVASample, 
                                   )
            pickle.dump( yields[cut_name], open(yield_pkl,'w') )
            print "Yield pickle dumped: %s"%yield_pkl
        combineBkgs = [ ["DYJetsM50", "ZJetsInv", "QCD"] , "Other" ] 
        seperators = ["DataBlind", "Total"]
        JinjaTexTable( yields[cut_name], pdfDir = tableDir, caption="" , transpose=True)
        JinjaTexTable( yields[cut_name], pdfDir = tableDir, outputName = yields[cut_name].tableName+"_T.tex", caption="" , noFOM=True, transpose=False, seperators = seperators)
        JinjaTexTable( yields[cut_name], pdfDir = tableDir, outputName = yields[cut_name].tableName+"_CombinedBKG.tex", caption="" , noFOM=True, transpose=True , combineBkgs = combineBkgs)
        JinjaTexTable( yields[cut_name], pdfDir = tableDir, outputName = yields[cut_name].tableName+"_CombinedBKG_T.tex", caption="" , noFOM=True, transpose=False, combineBkgs = combineBkgs      , seperators = seperators)
        JinjaTexTable( yields[cut_name], pdfDir = tableDir, outputName = yields[cut_name].tableName+"FOM_CombinedBKG_T.tex", caption="" , noFOM=False, transpose=False , combineBkgs = combineBkgs , seperators = seperators)
        #drawYields( cut_name , cfg.yieldPkls[cut_name] , sampleList = cfg.bkgList  + ['s300_290' , 's300_270','s300_220'] , keys=[] , ratios=True , save= cfg.cutSaveDirs[cut_name] )
        
        yldplts = []

        yldplt1 = drawYields("BkgComp_%s"%cut_name, yields[cut_name] , sampleList = cfg.bkgList , ratios= False, save=cfg.saveDirs[cut_name], normalize = True, logs = [0,0], plotMin=0)
        yldplt2 = drawYields("BkgVsData_%s"%cut_name, yields[cut_name] , sampleList = cfg.bkgList + dataList, ratios= True, save=cfg.saveDirs[cut_name], normalize = False, logs = [0,0], plotMin=0)
        yldplt3 = drawYields("BkgVsData_log_%s"%cut_name, yields[cut_name] , sampleList = cfg.bkgList + dataList, ratios= True, save=cfg.saveDirs[cut_name], normalize = False, logs = [0,1], plotMin=0.01)
        yldplt4 = drawYields("BkgVsSig_%s"%cut_name, yields[cut_name] , sampleList = cfg.bkgList + cfg.signalList, ratios= True, save=cfg.saveDirs[cut_name], normalize = False, logs = [0,1], plotMin=0.01)
        yldplt5 = drawYields("BksVsDataVsSignal_%s"%cut_name, yields[cut_name] , sampleList = cfg.bkgList + dataList + cfg.signalList , ratios= True, save=cfg.saveDirs[cut_name], normalize = False, logs = [0,1], plotMin=0.01)

        yldplts = [ yldplt1,yldplt2, yldplt3, yldplt4, yldplt5, ]

        #yldplts
    
    return yields, yldplts





def cut_flow(cfg, args):

    yields={}
    #sampleList = getattr(cfg, "sampleList") +  
    sampleList = getattr(cfg, "bkgList") +  getattr(cfg, "signalList")
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
                                        weight          =   "weight", 
                                        pklOpt          =   True, 
                                        tableName       =   "{cut}_%s%s"%(cfg.runTag,cfg.scan_tag), 
                                        nDigits         =   2 , 
                                        err             =   True , 
                                        verbose         =   True,
                                        isMVASample             =   isMVASample, 
                                   )
            pickle.dump( yields[cut_name], open(yield_pkl,'w') )
            print "Yield pickle dumped: %s"%yield_pkl
        combineBkgs = [ ["DYJetsM50", "ZJetsInv", "QCD"] , "Other" ] 
        seperators = ["CT300", "ISR325"]
        JinjaTexTable( yields[cut_name], pdfDir = tableDir, caption="" , transpose=True)
        JinjaTexTable( yields[cut_name], pdfDir = tableDir, outputName = yields[cut_name].tableName+"_T.tex", caption="" , noFOM=True, transpose=False, seperators = seperators)
        JinjaTexTable( yields[cut_name], pdfDir = tableDir, outputName = yields[cut_name].tableName+"_CombinedBKG.tex", caption="" , noFOM=True, transpose=True , combineBkgs = combineBkgs)
        JinjaTexTable( yields[cut_name], pdfDir = tableDir, outputName = yields[cut_name].tableName+"_CombinedBKG_T.tex", caption="" , noFOM=True, transpose=False, combineBkgs = combineBkgs      , seperators = seperators)
        JinjaTexTable( yields[cut_name], pdfDir = tableDir, outputName = yields[cut_name].tableName+"FOM_CombinedBKG_T.tex", caption="" , noFOM=False, transpose=False , combineBkgs = combineBkgs , seperators = seperators)
        #drawYields( cut_name , cfg.yieldPkls[cut_name] , sampleList = cfg.bkgList  + ['s300_290' , 's300_270','s300_220'] , keys=[] , ratios=True , save= cfg.cutSaveDirs[cut_name] )

    
    return yields






def data_plots(cfg,args):

    nminus1s = getattr(cfg, "nminus1s", {})
    verbose  = getattr(cfg, "verbose", True)

    def getAndDrawFull(cutInst, mcList, data , plot , plotMin = 0.01 , plotDir = ""):
        sampleList = mcList + [data]
        if verbose:
            print "----------"
            print cutInst
            print sampleList
            print "----------"
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

        setEventListToChains(cfg.samples, mcList +[data] , eventListCutInst)
        getPlots(cfg.samples, cfg.plots , cutInst  , sampleList = sampleList      , plotList=[plot] , nMinus1=nminus_list , addOverFlowBin='both',weight="weight"  )
        plt = drawPlots(cfg.samples,    cfg.plots , cutInst, sampleList = sampleList , # [ 'qcd','z','dy','tt','w','s300_250','s250_230' , 'dblind'],
                plotList= [plot] ,save= plotDir, plotMin=plotMin,
                normalize=False, denoms=["bkg"], noms=[data], fom="RATIO", fomLimits=[0,2.8])
        return plt

    result = {}
    for cutInst in cfg.cutInstList:
        cut_name = cutInst.fullName
        #print " . . . . . . . . . . . . . Cut: %s . . . . . . . . . . . . . . "%cut_name
        cutSaveDir = cfg.saveDir + "/" + cutInst.saveDir
        plotDir = cutSaveDir +"/DataPlots/"

        sampleList = cfg.bkgList + cfg.signalList #cfg.sample_info['sampleList']  + cfg.signalList 
        print "------------------- - - -- - --- - - - -- ", sampleList  
        result[cut_name]={}
        data = 'd' if 'SR' in cut_name else 'dblind'   ## safeside : 'dblind' if 'CR' in cut_name else 'd'
        #data = 'dblind' if 'CR' in cut_name else 'd'   ## safeside : 'dblind' if 'CR' in cut_name else 'd'
        plotMin =  0.001 if "SR" in cut_name else 0.1
        for plot in cfg.plotList:
            result[cut_name][plot] = getAndDrawFull(cutInst, mcList = sampleList, data = data , plot = plot , plotMin = plotMin , plotDir = plotDir)
            #print "results:", cutInst.fullName, plot
            #pp.pprint( result) 
    
