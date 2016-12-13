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

    puTags = ["pu", "pu_up", "pu_down" ] 

    yieldPkls=  {}
    yields   =  {}
    yieldDict = {}
    yieldTotals={}
    for puTag in puTags:
        runTag = 'PreApp_Mt95_Inccharge_{lepCol}_{lep}_{puTag}_SF'.format(lepCol=lepCol,lep=lep, puTag=puTag)
        saveDir              =  cfg.saveDirBase+'/%s/%s'%(runTag,cfg.htString)
        results_dir          =  cfg.cardDirBase + "/13TeV/{ht}/{run}/".format( ht = cfg.htString , run = runTag )
        lumiTag              =  make_lumi_tag( cfg.lumi_info['DataUnblind_lumi'] )
        yieldPkls[puTag]     =  results_dir + sys_label  + "/" + cfg.baseCutSaveDir  + "/Yields_%s_%s_%s.pkl"%( lumiTag , runTag, cut_name)    
        yields[puTag]        =  pickle.load(file( yieldPkls[puTag]  ))
        yieldDict[puTag]     =  yields[puTag].getNiceYieldDict()
        yieldTotals[puTag]   =  yieldDict[puTag]['Total']

    res =    dict_manipulator( [ yields['pu_down'].getNiceYieldDict()['Total'] , yields['pu_up'].getNiceYieldDict()['Total'] , yields['pu'].getNiceYieldDict()['Total'] ] , lambda a,b,c: ( abs(1.-(a/c).val) + abs(1.-(b/c).val) )/2. * 100)

    
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
    
    
    bkg_systs_dir = "$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/results/2016/BkgSysts/"
    pickle.dump(res , open( os.path.expandvars( bkg_systs_dir+"/PU.pkl")  ,"w"))
    table = makeSimpleLatexTable( table_list, "PU.tex", cfg.saveDirBase+"/BkgSysts/PU/", align_char = "c" ,  align_func= lambda char, table: "c|"+ (char *(len(table[1])-1)).rstrip("|") )
    
    
    print table
