from Workspace.DegenerateStopAnalysis.tools.degTools import fixForLatex


def fix_region_name(name):
    return name.replace("_","/").replace("pos","Q+").replace("neg","Q-")

if __name__ == '__main__':


    sig1           =    'S300-270Fast'
    sig2           =    'S300-240Fast'
    
    
    tt             =   'TTJets'
    w              =   "WJets"
    otherBkg       = ['DYJetsM50', "QCD", "ZJetsInv", "ST", "Diboson"]
    allBkg         = [w,tt] + otherBkg
    data           = 'DataBlind'
    sigs           = [sig1, sig2]
    sigs = []
    allSamps       = allBkg + sigs + [data]
    
    #side_band_name = 'presel_CRs'
    side_band_name = task_ret['bkg_est'][0].keys()[0]
    
    
    
    mtabc       = ["a","b","c"]
    pts         = ["sr","cr"]
    #charges    = ["pos","neg"]
    charges     = ["pos", "neg"]
    side_bands  = [ "ECR1", "ECR2" ] 
    
    
    #def subtractAndDivide( a,b,c,d,
    
    
    bkg_est_dir = "$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/results/2016/%s_%s_%s/BkgEst/"%(cfg.cmgTag, cfg.ppTag, cfg.runTag) 
    bkg_est_dir = os.path.expandvars( bkg_est_dir ) 
    makeDir(bkg_est_dir)
    
    
    yld = task_ret['bkg_est'][0][side_band_name]
    yldDict = yld.getNiceYieldDict()
    
    
    sampleMCFraction = lambda s : dict_manipulator( [ yldDict[b] for b in [s,'Total'] ] , func = (lambda a,b: "%s"%round((a/b).val*100,2) ))
    
    
    sampleFractions = { s:sampleMCFraction(s) for s in  sigs +[w,tt] }
    
    
    
    yldsByBins = yld.getByBins(yieldDict=yldDict)
    def dict_operator ( yldsByBin , keys = [] , func =  lambda *x: sum(x) ):
        """
        use like this dict_operator( yields_sr, keys = ['DataBlind', 'Total'] , func = lambda a,b: a/b)
        """ 
        args = [ yldsByBin[x] for x in keys]
        return func(*args) 
    
    
    table_legend = [  "region" , "sig_cont_sr", "sig_cont_cr", "w_frac", "w_sf_cr", "closure"  ] 
    
    first_row = True
    tt_table_list = []
    
    corrected_yields = {}
    
    
    
    
    
    
    
    
    
    
    ##FIX ME
    regions = [x for x in yld.cutNames if "CR" in x]
    region_names = regions
    tt_region_names = [x for x in region_names if "CRTT2" in x ]
    w_region_names  = [x for x in region_names if x not in tt_region_names]
    ##
    ## TT SideBand
    ##
    
    tt_table_list.append(["\hline"])
    
    
    
    tt_sf_crtt     = dict_operator ( yldsByBins[tt_region_names[0]] , keys = [ data , w, tt] + otherBkg  , func = lambda a,b,c,*d: (a-b-sum(d))/c)
    
    cr_sf_dict = {} 
    for region_name in region_names:
            region   = region_name
            yields = yldsByBins[region]
            otherSum = dict_operator ( yields , keys = otherBkg )
            yield_tt = yields[tt]
            MCTTFrac = yields[tt] / yields['Total']  * 100  
    
            if region in tt_region_names:
                w_sf = "-"
                tt_sf = tt_sf_crtt.round(2)
            else:
                w_sf     = dict_operator ( yldsByBins[region] , keys = [ data ,  tt, w] + otherBkg  , func = lambda a,b,c,*d: (a-b*tt_sf_crtt-sum(d))/c).round(2)
                tt_sf    = "-" #, u_float( 1. )
            cr_sf_dict[region]={  
                                    tt  : (tt_sf if not tt_sf == "-" else u_float(1.))   , 
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
    
    
    pickle.dump( cr_sf_dict ,   open( bkg_est_dir + "/CR_SFs.pkl", "w")  ) 
    table = makeSimpleLatexTable( tt_table_list, "CR_ScaleFactors.tex", cfg.saveDirs[side_band_name])
    
    
    print table
