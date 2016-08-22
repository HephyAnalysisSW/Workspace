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

    #tags = ["SF","SF_b_Down", "SF_b_Up", "SF_l_Down", "SF_l_Up"] 
    tags = ["SF","SF_B_DOWN", "SF_B_UP", "SF_L_DOWN", "SF_L_UP"] 

    yieldPkls=  {}
    yields   =  {}
    yieldDict = {}
    yieldTotals={}
    yieldW={}
    relsys = lambda a,b : abs(1.- (a/b).val)
    for tag in tags:
        runTag = 'PreApp_Mt95_Inccharge_{lepCol}_{lep}_pu_{tag}'.format(lepCol=lepCol,lep=lep, tag= "%s"%tag  )
        saveDir              =  cfg.saveDirBase+'/%s/%s'%(runTag,cfg.htString)
        results_dir          =  cfg.cardDirBase + "/13TeV/{ht}/{run}/".format( ht = cfg.htString , run = runTag )
        #lumiTag              =  make_lumi_tag( cfg.lumi_info['DataUnblind_lumi'] )
        lumiTag              =  make_lumi_tag( cfg.lumi_info['DataBlind_lumi'] )
        yieldPkls[tag]     =  results_dir + sys_label  + "/" + cfg.baseCutSaveDir  + "/Yields_%s_%s_%s.pkl"%( lumiTag , runTag, cut_name)    
        yields[tag]        =  pickle.load(file( yieldPkls[tag]  ))
        yieldDict[tag]     =  yields[tag].getNiceYieldDict()
        yieldTotals[tag]   =  yieldDict[tag]['Total']
        yieldW[tag]        =  yieldDict[tag]['WJets']

    #res_wpt  =    dict_manipulator( [ yieldTotals['wpt'] , yieldTotals['']  ] , lambda a,b: ( abs(1.-(a/b).val) ) * 100)
    #res_2wpt =    dict_manipulator( [ yieldTotals['2wpt'] , yieldTotals[''] ] , lambda a,b: ( abs(1.-(a/b).val) ) * 100)
    res_b  =    dict_manipulator( [ yieldTotals['SF_B_DOWN'] , yieldTotals['SF_B_UP'] , yieldTotals['SF']  ] , lambda a,b,c: ( relsys(a,c) + relsys(b,c) ) /2.  * 100)
    res_l  =    dict_manipulator( [ yieldTotals['SF_L_DOWN'] , yieldTotals['SF_L_UP'] , yieldTotals['SF']  ] , lambda a,b,c: ( relsys(a,c) + relsys(b,c) ) /2.  * 100)
    res    =    dict_manipulator( [ yieldTotals['SF_L_DOWN'] , yieldTotals['SF_L_UP'] , yieldTotals['SF_B_DOWN'] , yieldTotals['SF_B_UP'] , yieldTotals['SF']  ] , lambda a,b,c,d,e: (relsys(a,e) + relsys(a,e)+ relsys(c,e) + relsys(d,e) )/4. * 100)


    tags         = tags
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
    sample_card_systs_b = {} 
    sample_card_systs_l = {} 
    for samp in yieldDict[tag].keys():
         #sample_systs[samp]     =  dict_manipulator( [yieldDict[x][samp] for x in tags  ] , lambda a,b,c: ( abs(1.-(a/c).val) + abs(1.-(b/c).val) )/2. * 100 if c.val else 0 )   
         sample_card_systs_b[samp]=  dict_manipulator( [yieldDict[x][samp] for x in ['SF_B_DOWN', 'SF_B_UP', 'SF']  ] , lambda a,b,c: 1+ round( ( abs(1.-(a/c).val) + abs(1.-(b/c).val) )/2. , 3)  if c.val else 0 )   
         sample_card_systs_l[samp]=  dict_manipulator( [yieldDict[x][samp] for x in ['SF_L_DOWN', 'SF_L_UP', 'SF']  ] , lambda a,b,c: 1+ round( ( abs(1.-(a/c).val) + abs(1.-(b/c).val) )/2. , 3)  if c.val else 0 )   

    bins_card_systs_b  =  Yields.getByBins(yields[tag], sample_card_systs_b)
    bins_card_systs_l  =  Yields.getByBins(yields[tag], sample_card_systs_l)
    global_syst_pkl =  "%s/SystDictRaw.pkl"%(res_dir)
    if os.path.isfile(global_syst_pkl):
        global_syst_dict = pickle.load( file(global_syst_pkl) )
    else:
        global_syst_dict = {}
    global_syst_dict["Bb"] = {'bins':bins_card_systs_b , 'type':'lnN'}
    global_syst_dict["Bl"] = {'bins':bins_card_systs_l , 'type':'lnN'}
    #global_syst_dict["Bb"] = bins_card_systs_b
    #global_syst_dict["Bl"] = bins_card_systs_l
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
                          ["Region"           ,  fix_region_name( region_name )           ], 
                          ['SF'               ,  yieldTotals['SF'][region_name]           ],
                          ['SF_b_Down'        ,  yieldTotals['SF_B_DOWN'][region_name]    ],
                          ['SF_b_Up'          ,  yieldTotals['SF_B_UP'][region_name]      ],
                          ['SF_L_Down'        ,  yieldTotals['SF_L_DOWN'][region_name]    ],
                          ['SF_L_Up'          ,  yieldTotals['SF_L_UP'][region_name]      ],
                          ['Syst. B'          ,  round (res_b[region_name] ,2)            ],
                          ['Syst. L'          ,  round (res_l[region_name] ,2)            ],
                          ['Syst. '           ,  round (res[region_name]   ,2)            ],
    
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


    pickle.dump(res   , open( os.path.expandvars( bkg_systs_dir+"/BTag.pkl")  ,"w"))
    pickle.dump(res_b , open( os.path.expandvars( bkg_systs_dir+"/BTag_b.pkl")  ,"w"))
    pickle.dump(res_l , open( os.path.expandvars( bkg_systs_dir+"/BTag_l.pkl")  ,"w"))
    #pickle.dump(jer_res , open( os.path.expandvars( bkg_systs_dir+"/JER.pkl")  ,"w"))
    table = makeSimpleLatexTable( table_list, "BTag.tex", cfg.saveDirBase+"/BkgSysts/"       , align_char = "c" ,  align_func= lambda char, table: "c|ccccc|c|c|c" )
    table = makeSimpleLatexTable( table_list, "BTag.tex", os.path.expandvars( bkg_systs_dir ), align_char = "c" ,  align_func= lambda char, table: "c|ccccc|c|c|c" )
    
    
    print table
