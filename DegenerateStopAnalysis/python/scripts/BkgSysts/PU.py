from Workspace.DegenerateStopAnalysis.tools.degTools import fixForLatex


def fix_region_name(name):
    return name.replace("_","/").replace("pos","Q+").replace("neg","Q-")

def dict_operator ( yldsByBin , keys = [] , func =  lambda *x: sum(x) ):
    """
    use like this dict_operator( yields_sr, keys = ['DataBlind', 'Total'] , func = lambda a,b: a/b)
    """ 
    args = [ yldsByBin[x] for x in keys]
    return func(*args) 



if __name__ == '__main__':

    lepCol = "LepAll"
    lep    = "lep"


    make_lumi_tag = lambda l: "%0.0fpbm1"%(l)

    sys_label = "AdjustedSys"
    cut_name = cfg.cutInstList[0].fullName

    puTags = ["pu_up", "pu_down" , 'pu'] 

    yieldPkls=  {}
    yields   =  {}
    yieldDict = {}
    yieldTotals={}
    for puTag in puTags:
        runTag = 'PreApp_Mt95_Inccharge_{lepCol}_{lep}_{puTag}_SF'.format(lepCol=lepCol,lep=lep, puTag=puTag)
        saveDir              =  cfg.saveDirBase+'/%s/%s'%(runTag,cfg.htString)
        results_dir          =  cfg.cardDirBase + "/13TeV/{ht}/{run}/".format( ht = cfg.htString , run = runTag )
        #lumiTag              =  make_lumi_tag( cfg.lumi_info['DataUnblind_lumi'] )
        lumiTag              =  make_lumi_tag( cfg.lumi_info['DataBlind_lumi'] )
        yieldPkls[puTag]     =  results_dir + sys_label  + "/" + cfg.baseCutSaveDir  + "/Yields_%s_%s_%s.pkl"%( lumiTag , runTag, cut_name)    
        yields[puTag]        =  pickle.load(file( yieldPkls[puTag]  ))
        yieldDict[puTag]     =  yields[puTag].getNiceYieldDict()
        yieldTotals[puTag]   =  yieldDict[puTag]['Total']


    res =    dict_manipulator( [ yields['pu_down'].getNiceYieldDict()['Total'] , yields['pu_up'].getNiceYieldDict()['Total'] , yields['pu'].getNiceYieldDict()['Total'] ] , lambda a,b,c: ( abs(1.-(a/c).val) + abs(1.-(b/c).val) )/2. * 100)




    #bkgList  = yields[puTag]
    #otherBkg = [x for x in ]
    #other = dict_operator( yieldDict , keys = [ bkg for bkg in cfg.bkgList if bkg not in ['TTJets','WJets']] , func = yield_adder_func2 )




    tags         = puTags
    res_dir      = os.path.expandvars("$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/results/2016/%s_%s_%s/"%(cfg.cmgTag, cfg.ppTag, cfg.runTag) )
    yldinsts_dir = "%s/YieldInsts/"%(res_dir)
    ylds_dir     = "%s/YieldDicts/"%(res_dir)
    global_yield_dict = res_dir + "/YieldDictWithVars.pkl"
    makeDir(ylds_dir)
    makeDir(yldinsts_dir)
    for tag in tags:
        pickle.dump(  yields[tag] , open( "%s/YieldInst_%s.pkl"%(yldinsts_dir, tag) ,'w' ) )
        pickle.dump(  yieldDict[tag] , open( "%s/YieldDict_%s.pkl"%(ylds_dir, tag) ,'w' ) )
    
    for tag in tags:
        if os.path.isfile(global_yield_dict):
            global_pkl = pickle.load( file(global_yield_dict) )
        else:
            global_pkl = {}
        global_pkl[tag] = yieldDict[tag]
        pickle.dump(  global_pkl , open( "%s/YieldDictWithVars.pkl"%(res_dir ) ,'w' ) )


    syst_name = "PU"
    #sample_systs = {}
    sample_card_systs = {} 
    for samp in yieldDict[tag].keys():
         #sample_systs[samp]     =  dict_manipulator( [yieldDict[x][samp] for x in tags  ] , lambda a,b,c: ( abs(1.-(a/c).val) + abs(1.-(b/c).val) )/2. * 100 if c.val else 0 )   
         sample_card_systs[samp]=  dict_manipulator( [yieldDict[x][samp] for x in tags  ] , lambda a,b,c: 1+ round( ( abs(1.-(a/c).val) + abs(1.-(b/c).val) )/2. , 3)  if c.val else 0 )   
    global_syst_pkl =  "%s/SystDictRaw.pkl"%(res_dir)
    bins_card_systs  =  Yields.getByBins(yields[tag], sample_card_systs)
    if os.path.isfile(global_syst_pkl):
        global_syst_dict = pickle.load( file(global_syst_pkl) )
    else:
        global_syst_dict = {}
    global_syst_dict[syst_name] = {'bins':bins_card_systs , 'type':'lnN'}
    #global_syst_dict[syst_name] = bins_card_systs 
    pickle.dump( global_syst_dict ,  open( "%s/SystDictRaw.pkl"%(res_dir ) ,'w' ) ) 

    
    ##FIX ME
    #regions = yld.cutNames

    regions =  [\
             'SRL1a',
             'SRH1a',
             'SRV1a',
             '\hline',
             'SR1a',
             '\hline',
             'SRL1b',
             'SRH1b',
             'SRV1b',
             '\hline',
             'SR1b',
             '\hline',
             'SRL1c',
             'SRH1c',
             'SRV1c',
             '\hline',
             'SR1c',
             '\hline',
             'SRL2',
             'SRH2',
             'SRV2',
             '\hline',
             'SR2',
             '\hline',
                ]

    region_names = regions
    
    first_row = True
    table_list = [] 
    for region_name in region_names:
            if region_name == "\hline":
                table_list.append([region_name])
                continue
            region   = region_name
    
    
            toPrint = [   
                          ["Region"     ,  fix_region_name( region_name )], 
                          ['PU Down'    ,  yieldTotals['pu_down'][region_name]    ],
                          ['PU Central' ,  yieldTotals['pu'][region_name]         ],
                          ['PU Up'      , yieldTotals['pu_up'][region_name]      ],
                          ['Syst. ' , round (res[region_name] ,2)      ],
    
                       ]#dataCR( dataMCsf * yldDict[tt][region]).round(2)  ]
    
    
            align = "{:<20}"*len(toPrint)
    
            if first_row:
                print align.format(*[x[0] for x in toPrint])
                first_row = False
                table_list.append( [x[0] for x in toPrint]  ) 
    
            print align.format(*[x[1] for x in toPrint])
            table_list.append( [x[1] for x in toPrint])
    
    
    bkg_systs_dir = "$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/results/2016/%s_%s_%s/BkgSysts/"%(cfg.cmgTag, cfg.ppTag, cfg.runTag)
    makeDir(os.path.expandvars(bkg_systs_dir))
    pickle.dump(res , open( os.path.expandvars( bkg_systs_dir+"/PU.pkl")  ,"w"))
    table = makeSimpleLatexTable( table_list, "PU.tex", cfg.saveDirBase+"/BkgSysts/", align_char = "c" ,  align_func= lambda char, table: "c|"+ (char *(len(table[1])-1)).rstrip("|") )
    
    
    print table
