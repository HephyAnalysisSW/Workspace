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


    sig1           =    'S300-270Fast'
    sig2           =    'S300-240Fast'
    
    
    tt             =   'TTJets'
    w              =   "WJets"
    qcd            =   "QCD"
    z              =   "ZJetsInv"
    #otherBkg       = ['DYJetsM50', "QCD", "ZJetsInv", "ST", "Diboson"]
    otherBkg       = ['DYJetsM50' , "ST", "Diboson"]
    allBkg         = [w,tt] + otherBkg
    data           = 'DataBlind'
    sigs           = [sig1, sig2]
    sigs = []
    allSamps       = allBkg + sigs + [data]
    
    #side_band_name = 'presel_SRs_PtBinned'
    side_band_name = 'presel_SRs_PtBinnedSum'
    
    
    mtabc       = ["a","b","c"]
    pts         = ["sr","cr"]
    #charges     = ["pos","neg"]
    charges     = ["pos", "neg"]
    side_bands  = [ "ECR1", "ECR2" ] 
    
    

    tt_sf     = u_float(0.72,0.2)
    w_sf_sr1a = u_float(0.99,0.04)
    w_sf_sr1b = u_float(0.96,0.05)
    w_sf_sr1c = u_float(1.24,0.07)
    w_sf_sr2  = u_float(0.91,0.08)
   

 
    
    SFs={
     'SRL1a':{qcd:1.0 , z:1.0 , w: w_sf_sr1a , tt: tt_sf },
     'SRH1a':{qcd:1.0 , z:1.0 , w: w_sf_sr1a , tt: tt_sf },
     'SRV1a':{qcd:1.0 , z:1.0 , w: w_sf_sr1a , tt: tt_sf },
     'SR1a':{qcd:1.0 , z:1.0 , w: w_sf_sr1a , tt: tt_sf },
     'SRL1b':{qcd:1.0 , z:1.0 , w: w_sf_sr1b , tt: tt_sf },
     'SRH1b':{qcd:1.0 , z:1.0 , w: w_sf_sr1b , tt: tt_sf },
     'SRV1b':{qcd:1.0 , z:1.0 , w: w_sf_sr1b , tt: tt_sf },
     'SR1b':{qcd:1.0 , z:1.0 , w: w_sf_sr1b , tt: tt_sf },
     'SRL1c':{qcd:1.0 , z:1.0 , w: w_sf_sr1c , tt: tt_sf },
     'SRH1c':{qcd:1.0 , z:1.0 , w: w_sf_sr1c , tt: tt_sf },
     'SRV1c':{qcd:1.0 , z:1.0 , w: w_sf_sr1c , tt: tt_sf },
     'SR1c':{qcd:1.0 , z:1.0 , w: w_sf_sr1c , tt: tt_sf },
     'SRL2' :{qcd:1.0 , z:1.0 , w: w_sf_sr2  , tt: tt_sf },
     'SRH2' :{qcd:1.0 , z:1.0 , w: w_sf_sr2  , tt: tt_sf },
     'SRV2' :{qcd:1.0 , z:1.0 , w: w_sf_sr2  , tt: tt_sf },
     'SR2' :{qcd:1.0 , z:1.0 , w: w_sf_sr2  , tt: tt_sf },
    } 
    
    
    
    yld = task_ret['bkg_est'][0][side_band_name]
    yldDict = yld.getNiceYieldDict()

    estYields = yldDict.copy()
    #estYields.pop("Total")

    yldsByBins = yld.getByBins(yieldDict=estYields)

 
    
    
    
    
    
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
    
            estTotal     = dict_operator ( yldsByBins[region] , keys = [ w, tt , z, qcd] + otherBkg  , func = lambda a,b,c,d, *e: a*SFs[region][w] + b*SFs[region][tt] + c*SFs[region][z] + d*SFs[region][qcd]  + sum( e )     )
            mcTotal      = yldsByBins[region]['Total']
            observed     = int( yldsByBins[region]['DataUnblind'].val)
    
            toPrint = [   
                          ["Region"     ,  fix_region_name( region_name )], 
                          ['MC. S.M'    ,  mcTotal   ],
                          ['Estim. S.M' ,  estTotal.round(2)  ],
                          ['Data'       ,  observed  ],
    
                       ]#dataCR( dataMCsf * yldDict[tt][region]).round(2)  ]
    
    
            align = "{:<20}"*len(toPrint)
    
            if first_row:
                print align.format(*[x[0] for x in toPrint])
                first_row = False
                table_list.append( [x[0] for x in toPrint]  ) 
    
            print align.format(*[x[1] for x in toPrint])
            table_list.append( [x[1] for x in toPrint])
    
    
    
    table = makeSimpleLatexTable( table_list, "SR_Estim.tex", cfg.saveDirs[side_band_name])
    
    
    print table
