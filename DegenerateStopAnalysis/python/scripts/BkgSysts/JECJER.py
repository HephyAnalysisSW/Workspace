from Workspace.DegenerateStopAnalysis.tools.degTools import fixForLatex
"""

#ipython -i   degStop.py -- --cfg=PreApp --task=jec_est --lepCol=LepAll --lep=lep  --weight=pu --btag=SF
ipython -i   degStop.py -- --cfg=PreApp --task=jec_est --lepCol=LepAll --lep=lep  --weight=pu --btag=SF
execfile("JECJER.py")

"""

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

    #bin_name_base = 'presel_SRs_PtBinnedSum'
    bin_name_base = 'presel_BinsSummary'

    jcTags = ['jer_up', 'jec_down', 'jer_down', 'jer_central', 'jec_up', '', 'jec_central']
        


    yieldPkls=  {}
    yields   =  {}
    yieldDict = {}
    yieldTotals={}

    taskret = task_ret['bkg_est'][0]
    for jc in jcTags:
        bin_name = bin_name_base +"_%s"%jc if jc else bin_name_base
        yieldPkls[jc]   =   taskret[bin_name]
        yields[jc]      =   yieldPkls[jc]
        yieldDict[jc]   =   yieldPkls[jc].getNiceYieldDict()
        yieldTotals[jc] =   yieldDict[jc]['Total']



    jec_res =    dict_manipulator( [ yieldTotals['jec_up'], yieldTotals['jec_central'] , yieldTotals['jec_down'] ] , lambda a,b,c: ( abs(1.-(a/c).val) + abs(1.-(b/c).val) )/2. * 100)
    jer_res =    dict_manipulator( [ yieldTotals['jer_up'], yieldTotals['jer_central'] , yieldTotals['jer_down'] ] , lambda a,b,c: ( abs(1.-(a/c).val) + abs(1.-(b/c).val) )/2. * 100)



    tags         = jcTags
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


    syst_name = ""
    #sample_systs = {}
    sample_card_systs_jec = {} 
    sample_card_systs_jer = {} 
    for samp in yieldDict[tag].keys():
         #sample_systs[samp]     =  dict_manipulator( [yieldDict[x][samp] for x in tags  ] , lambda a,b,c: ( abs(1.-(a/c).val) + abs(1.-(b/c).val) )/2. * 100 if c.val else 0 )   
         sample_card_systs_jec[samp]=  dict_manipulator( [yieldDict[x][samp] for x in ['jec_up', 'jec_down', 'jec_central']  ] , lambda a,b,c: 1+ round( ( abs(1.-(a/c).val) + abs(1.-(b/c).val) )/2. , 3)  if c.val else 0 )   
         sample_card_systs_jer[samp]=  dict_manipulator( [yieldDict[x][samp] for x in ['jer_up', 'jer_down', 'jer_central']  ] , lambda a,b,c: 1+ round( ( abs(1.-(a/c).val) + abs(1.-(b/c).val) )/2. , 3)  if c.val else 0 )   

    bins_card_systs_jec  =  Yields.getByBins(yields[tag], sample_card_systs_jec)
    bins_card_systs_jer  =  Yields.getByBins(yields[tag], sample_card_systs_jer)
    global_syst_pkl    =  "%s/SystDictRaw.pkl"%(res_dir)
    if os.path.isfile(global_syst_pkl):
        global_syst_dict = pickle.load( file(global_syst_pkl) )
    else:
        global_syst_dict = {}
    global_syst_dict["JEC"] = {'bins':bins_card_systs_jec , 'type':'lnN'}
    global_syst_dict["JER"] = {'bins':bins_card_systs_jer , 'type':'lnN'}
    #global_syst_dict["JEC"] = bins_card_systs_jec
    #global_syst_dict["JER"] = bins_card_systs_jer
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
             '\hline',
             'CR1a',
             'CR1b',
             'CR1c',
             'CR2',
             'CRTT2',
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
                          ["Region"      , fix_region_name( region_name )         ], 
                          ['JEC Down'    , yieldTotals['jec_down'][region_name]    ],
                          ['JEC Central' , yieldTotals['jec_central'][region_name]         ],
                          ['JEC Up'      , yieldTotals['jec_up'][region_name]      ],
                          ['JEC Syst. (\%s)'      , round (jec_res[region_name] ,2)            ],
                          ['JER Down'    , yieldTotals['jer_down'][region_name]    ],
                          ['JER Central' , yieldTotals['jer_central'][region_name]         ],
                          ['JER Up'      , yieldTotals['jer_up'][region_name]      ],
                          ['JER Syst. (\%) '      , round (jer_res[region_name] ,2)            ],
    
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
    pickle.dump(jec_res , open( os.path.expandvars( bkg_systs_dir+"/JEC.pkl")  ,"w"))
    pickle.dump(jer_res , open( os.path.expandvars( bkg_systs_dir+"/JER.pkl")  ,"w"))
    table = makeSimpleLatexTable( table_list, "JECJER.tex", cfg.saveDirBase+"/BkgSysts/", align_char = "c" ,  align_func= lambda char, table: "c|ccc|c|ccc|c" )
    table = makeSimpleLatexTable( table_list, "JECJER.tex", os.path.expandvars( bkg_systs_dir ), align_char = "c" ,  align_func= lambda char, table: "c|ccc|c|ccc|c" )
    
    
    print table
