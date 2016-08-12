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
        yieldPkls[jc] = taskret[bin_name]
        yieldDict[jc]=yieldPkls[jc].getNiceYieldDict()
        yieldTotals[jc]=yieldDict[jc]['Total'] 


    jec_res =    dict_manipulator( [ yieldTotals['jec_up'], yieldTotals['jec_central'] , yieldTotals['jec_down'] ] , lambda a,b,c: ( abs(1.-(a/c).val) + abs(1.-(b/c).val) )/2. * 100)
    jer_res =    dict_manipulator( [ yieldTotals['jer_up'], yieldTotals['jer_central'] , yieldTotals['jer_down'] ] , lambda a,b,c: ( abs(1.-(a/c).val) + abs(1.-(b/c).val) )/2. * 100)

    
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
    
    
    bkg_systs_dir = "$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/results/2016/BkgSysts/"
    pickle.dump(jec_res , open( os.path.expandvars( bkg_systs_dir+"/JEC.pkl")  ,"w"))
    pickle.dump(jer_res , open( os.path.expandvars( bkg_systs_dir+"/JER.pkl")  ,"w"))
    table = makeSimpleLatexTable( table_list, "JECJER.tex", cfg.saveDirBase+"/BkgSysts/", align_char = "c" ,  align_func= lambda char, table: "c|ccc|c|ccc|c" )
    table = makeSimpleLatexTable( table_list, "JECJER.tex", os.path.expandvars( bkg_systs_dir ), align_char = "c" ,  align_func= lambda char, table: "c|ccc|c|ccc|c" )
    
    
    print table
