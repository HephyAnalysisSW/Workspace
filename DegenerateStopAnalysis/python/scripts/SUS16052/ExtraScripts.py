# run Systematics.py first

def convertRelSystToLNN(relsyst):
    """ input relsyst in % gives lnn values for combine"""
    if relsyst >= 0:
        ret = 1+relsyst/100.
    else:
        ret = 1./(1+abs(relsyst)/100.)
    return round(ret,4)


def makeTableFromDict( res_dict , bins = [] , data='DataBlind', signal='signal', total='Total' , bkg=['WJets', 'TTJets', 'Fakes', 'Others'] ,
                                       niceNames = {} ,
                                       niceNameFunc = niceRegionName,
                                       func = lambda x, samp: int(x.val) if samp=='DataBlind' else x.round(2) ):
    sample_legends = bkg[:] if bkg else [] #+ [ total, data ]
    if total: sample_legends +=[total]
    if data: sample_legends +=[data]
    if signal: sample_legends += [signal]
    print sample_legends
    bins_ = bins[:]
    table_list = []
    bins = bins_ if bins_ else sorted( [b for b in res_dict.keys() if 'cr' in b] )
    table_list.append( [''] + [ niceNames.get(samp, samp) for samp in sample_legends] )
    for b in bins :
        table_list.append( [niceNameFunc( niceNames.get(b,b) )]+[func(res_dict[b].get(samp, u_float(-0,0)), samp) for samp in sample_legends] )
    return table_list



if False:
    def CRTable():
        {k:{s:y for s,y in v.iteritems() if s in ['Fakes', 'TTJets','WJets','Total','Others', 'DataBlind'] } for k,v in syst.variations_yld_sums['central']['lep'].iteritems() if 'cr' in k.lower() and ('X' in k or 'Y' in k) and len(k)>4 }
    d = {k:{s:y for s,y in v.iteritems() if s in ['Fakes', 'TTJets','WJets','Total','Others', 'DataBlind'] } for k,v in syst.variations_yld_sums['central']['lep'].iteritems() if 'cr' in k.lower() and ('X' in k or 'Y' in k) and len(k)>4 }
    table = makeTableFromDict( d )
    tx = makeSimpleLatexTable( table, "CRwStat", "/afs/hephy.at/user/n/nrad/www/T2Deg13TeV//8025_mAODv2_v7/80X_postProcessing_v0/Summer16_v1/May17v0/LepGood_lep_lowpt_Jet_def_SF_Prompt_PU_TTIsr_Wpt_TrigEff/DataBlind/presel_base/bins_mtct_sum/19MayStatusUpdate_MTCTLepPtVL2/" )
    sfs = [(b,dict_operator( d[b], ['DataBlind', 'Fakes', 'Others', 'WJets','TTJets'], lambda d,f,o,w,t : ((d-f-o)/(w+t)).round(3) )) for b in d.keys() ]
    sfs.sort()






def getElMuRatios():
    yldsSumAll = pickle.load(file("/afs/hephy.at/work/n/nrad/results/cards_and_limits//13TeV/8025_mAODv2_v7/80X_postProcessing_v0/EPS17_v0/May17_v2/LepGood_lep_lowpt_Jet_def_SF_Prompt_PU_TTIsr_Wpt_TrigEff_lepSFFix/DataBlind/presel_base/yields_summary_allregions_bins_mtct_sum.pkl"))
    regions = sorted( [x for x in yldsSumAll['lep'].keys() 
                       if ('1l' in x or '1vl' in x or '2l' in x or '2vl' in x )
                       and ("X" in x or "Y" in x)  and ("la" in x or "lb" in x or "lc" in x) 
                       and "vlc" not in x 
                       ])
    regions_info = RegionsInfo( regions )
    regions_map = {k:v for k,v in regions_info.card_regions_map.items() if k in regions}


    sorted_regions = regions_info.sort_regions( regions_map.keys() )

    proc = "SimpleTotal"
    ylds = {flav: { r:yldsSumAll[flav ][r][proc] for r in regions } for flav in ["mu","el"] }

    mu  = degTools.makeHistoFromDict( ylds['mu'], bin_order = sorted( regions )  , name="mu")
    mu.SetLineColor(ROOT.kBlue)
    mu.SetMarkerColor(ROOT.kBlue)
    el  = degTools.makeHistoFromDict( ylds['el'], bin_order = sorted( regions )  , name="mu")
    el.SetLineColor(  ROOT.kRed)
    el.SetMarkerColor(ROOT.kRed)

    def makeFunc( rel_mu, rel_el, rel_el_bar, rel_el_end ):
        def func( sfmu, sfelbar, sfelend):
            return rel_mu * sfmu + rel_el*( rel_el_bar* sfelbar + rel_el_end * sfelend) 
        return func

    funcs = {}
    vals  = {}
    for r, subr in regions_map.items():
        mu  = yldsSumAll['mu'][r][proc] 
        el  = yldsSumAll['el'][r][proc] 
        lep = el + mu
        rel_mu = mu / lep
        rel_el = el / lep        

        rels = [rel_mu, rel_el]
        if el.val and len(subr)>1:
            el_bar = yldsSumAll['el'][r+"_barrel"][proc]
            el_end = yldsSumAll['el'][r+"_endcap"][proc]
            rel_el_bar = el_bar / el 
            rel_el_end = el_end / el
        else:
            rel_el_bar = u_float( 1.)
            rel_el_end = u_float( 0.)
        rels.extend([  rel_el_bar, rel_el_end ]) 
        rels = [ round(x.val, 2)  for x in  rels ] 
        #funcs[r] =  lambda sfmu, sfelbar, sfelend  : rel_mu * sfmu + rel_el*( rel_el_bar* sfelbar + rel_el_end * sfelend) 
        vals[r] = rels
        funcs[r] = makeFunc( *rels ) # lambda sfmu, sfelbar, sfelend  : rel_mu * sfmu + rel_el*( rel_el_bar* sfelbar + rel_el_end * sfelend) 


    #   vals=\
    #           {'sr1laX': [0.68, 0.32, 1.0, 0.0],
    #            'sr1laY': [0.63, 0.37, 1.0, 0.0],
    #            'sr1lbX': [0.65, 0.35, 1.0, 0.0],
    #            'sr1lbY': [0.65, 0.35, 1.0, 0.0],
    #            'sr1lcX': [0.51, 0.49, 1.0, 0.0],
    #            'sr1lcY': [0.63, 0.37, 1.0, 0.0],
    #            'sr1vlaX': [1.0, 0.0, 1.0, 0.0],
    #            'sr1vlaY': [1.0, 0.0, 1.0, 0.0],
    #            'sr1vlbX': [1.0, 0.0, 1.0, 0.0],
    #            'sr1vlbY': [1.0, 0.0, 1.0, 0.0],
    #            'sr2laX': [0.67, 0.33, 0.84, 0.16],
    #            'sr2laY': [0.69, 0.31, 0.7, 0.3],
    #            'sr2lbX': [0.73, 0.27, 0.83, 0.17],
    #            'sr2lbY': [0.69, 0.31, 0.92, 0.08],
    #            'sr2lcX': [0.64, 0.36, 0.57, 0.43],
    #            'sr2lcY': [0.62, 0.38, 0.15, 0.85],
    #            'sr2vlaX': [1.0, 0.0, 1.0, 0.0],
    #            'sr2vlaY': [1.0, 0.0, 1.0, 0.0],
    #            'sr2vlbX': [1.0, 0.0, 1.0, 0.0],
    #            'sr2vlbY': [1.0, 0.0, 1.0, 0.0]}



 
    lep=el.Clone("lep")
    lep.Add(mu)
    lep.LabelsOption("V")

    [0.016, 0.02, 0.005, 0.012, 0.008, 0.014]

    el_stat_sfs = [
        [ 0, 0.016, 0.02 ],
        [ 0, 0.005, 0.012],
    ]   
 
    mu_stat_sfs = [
        [ 0.008, 0, 0    ],
        [ 0.014, 0, 0    ]
    ]

    #statsfs_mu_vl = [ [1.015,1,1    ] ,  [1.01, 1.0, 1 ] ] 
    #statsfs_el_l  = [ [1,1.005, 1.01],   [ 1, 1.02,1.02] ] 
    
    el_barr_ends_uncerts = dict_function( { k:v for k,v in funcs.iteritems() if '1l' in k  or '2l' in k }, lambda x:[ x( *  el_stat_sfs[0] ) , x( *  el_stat_sfs[1]) ] )
    mu_uncerts           = dict_function( { k:v for k,v in funcs.iteritems() if '1vl' in k or '2vl' in k }, lambda x:[ x( * mu_stat_sfs[0] )  , x( * mu_stat_sfs[1]) ] )

    el_final_uncerts = dict_function( el_barr_ends_uncerts , lambda x: round( 1+addInQuad(x) ,5) )
    mu_final_uncerts = dict_function( mu_uncerts , lambda x: round( 1 + addInQuad(x) ,5) )

    final_uncerts = deepcopy( el_final_uncerts )
    final_uncerts.update( mu_final_uncerts )



def getBkgSum():
    fakeEstimateOutput = pickle.load(file( cfg.results_dir +"/presel_base/fakeEstimateOutput_bins_mtct_sum.pkl" ))
    samps = fakeEstimateOutput['prompt_fake_yields']['lep']['sr1maX'].keys()
    bkgs = [ x for x in samps  if 'T2' not in x]
    bins = fakeEstimateOutput['prompt_fake_yields']['lep'].keys()
    bkgYields = { b:{ s:fakeEstimateOutput['prompt_fake_yields']['lep'][b][s] for s in bkgs} for b in bins }

    regions_info = fakeEstimateOutput['regions_info']
    crmap = regions_info.getCardInfo("MTCTLepPtSum")['card_cr_sr_map']

    p="WJets"
    [(cr,(bkgYields[srs[0]][p]/ bkgYields[cr][p]).round(3))  for cr,srs in sorted(crmap.items())  ]
    p="TTJets"
    [(cr,(bkgYields[srs[0]][p]/ bkgYields[cr][p]).round(3))  for cr,srs in sorted(crmap.items())  ]


    double_ratio = [ (bkgYields[srs[0]]["WJets"]/ bkgYields[cr]["WJets"]).round(3)/(bkgYields[srs[0]]["TTJets"]/ bkgYields[cr]["TTJets"]).round(3)  
                     for cr,srs in crmap.items()  ]
   

 
    #    makeRow     = lambda sr,cr : [  
    #                                    by[sr][w].round(2) , 
    #                                    #by[cr][w].round(2) if not cr==sr.replace("vl","").replace('sr','cr') else 0, 
    #                                    "\multirow{4}{*}{%s}"%(by[cr][w].round(2)) if cr==sr.replace("vla","a").replace("vlb","b").replace('sr','cr') 
    #                                        else ( "\multirow{3}{*}{%s}"%(by[cr][w].round(2)) if cr==sr.replace("lc","c").replace('sr','cr') else "" ), 
    #                                    by[sr][tt].round(2),  
    #                                    #by[cr][tt].round(2), 
    #                                    "\multirow{4}{*}{%s}"%(by[cr][tt].round(2)) if cr==sr.replace("vla","a").replace("vlb","b").replace('sr','cr') 
    #                                        else ( "\multirow{3}{*}{%s}"%(by[cr][tt].round(2)) if cr==sr.replace("lc","c").replace('sr','cr') else "" ), 
    #                                    round( (by[sr][w] / by[cr][w]).val ,3)  , 
    #                                    round( (by[sr][tt]/ by[cr][tt]).val,3) , 
    #                                    round( (doubleRatio(sr,cr)).val    ,3) ,
    #                                     
    #                                    round( 1- ( 0.20 * (1-doubleRatio(sr,cr).val) ) ,2) 
    #                                    ] 


def getSummaryRegions(syst):
    regions_info = syst.regions_info
    #regions_info = fakeEstimateOutput['regions_info']
    crmap_pt = regions_info.getCardInfo("MTCTLepPtVL2")['card_cr_sr_map']
    card_regions_pt = regions_info.getCardInfo("MTCTLepPtVL2")['card_regions']
    crmap_ptinc        = regions_info.getCardInfo("MTCTLepPtSum")['card_cr_sr_map']
    card_regions_ptinc = regions_info.getCardInfo("MTCTLepPtSum")['card_regions']
    crmap = {}
    for cr in crmap_pt.keys():
        crmap[cr]= crmap_pt[cr] + crmap_ptinc[cr]
    card_regions = list(set( card_regions_pt + card_regions_ptinc ) )
    card_regions = regions_info.sort_regions( card_regions )
    sr_regions   = [ sr for sr in card_regions if 'sr' in sr]
    cr_regions   = [ cr for cr in card_regions if 'cr' in cr]
    sr_map = {sr:[ cr for cr,srs in crmap.items() if sr in srs][0] for sr in sr_regions}
    cr_map = crmap
    return sr_regions, cr_regions, sr_map, cr_map


def getWTTPtSyst( cfg, args ) :  # bkgYields, regions_info):
    fakeEstimateOutput = pickle.load(file( cfg.results_dir +"/presel_base/fakeEstimateOutput_bins_mtct_sum.pkl" ))
    samps = fakeEstimateOutput['prompt_fake_yields']['lep']['sr1maX'].keys()
    bkgs = [ x for x in samps  if 'T2' not in x]
    bins = fakeEstimateOutput['prompt_fake_yields']['lep'].keys()
    bkgYields = { b:{ s:fakeEstimateOutput['prompt_fake_yields']['lep'][b][s] for s in bkgs} for b in bins }
    by = bkgYields

    #regions_info = fakeEstimateOutput['regions_info']
    #crmap = regions_info.getCardInfo("MTCTLepPtVL2")['card_cr_sr_map']
    #card_regions = regions_info.getCardInfo("MTCTLepPtVL2")['card_regions']
    #sr_regions   = [ sr for sr in card_regions if 'sr' in sr]
    #cr_regions   = [ cr for cr in card_regions if 'cr' in cr]

    regions_info = fakeEstimateOutput['regions_info']
    crmap_pt = regions_info.getCardInfo("MTCTLepPtVL2")['card_cr_sr_map']
    card_regions_pt = regions_info.getCardInfo("MTCTLepPtVL2")['card_regions']
    crmap_ptinc        = regions_info.getCardInfo("MTCTLepPtSum")['card_cr_sr_map']
    card_regions_ptinc = regions_info.getCardInfo("MTCTLepPtSum")['card_regions']

    crmap = {}
    for cr in crmap_pt.keys():
        crmap[cr]= crmap_pt[cr] + crmap_ptinc[cr]

    card_regions = list(set( card_regions_pt + card_regions_ptinc ) )
    card_regions = regions_info.sort_regions( card_regions )

    sr_regions   = [ sr for sr in card_regions if 'sr' in sr]
    cr_regions   = [ cr for cr in card_regions if 'cr' in cr]





    sr_map = {sr:[ cr for cr,srs in crmap.items() if sr in srs][0] for sr in sr_regions}

    w  = "WJets"        
    tt = "TTJets"       
    doubleRatio = lambda sr,cr : (bkgYields[sr][w]/bkgYields[cr][w])/( bkgYields[sr][tt]/bkgYields[cr][tt] )
    R           = lambda sr,cr : ( bkgYields[cr][tt] / bkgYields[cr][w] )
    def makeRow(sr,cr):
        srw  = by[sr][w].round(2) 
        crw  = by[cr][w].round(2)
        crwl  =   "\multirow{4}{*}{%s}"%(by[cr][w].round(2)) if cr==sr.replace("vla","a").replace("vlb","b").replace('sr','cr')\
                     else ( "\multirow{3}{*}{%s}"%(by[cr][w].round(2)) if cr==sr.replace("lc","c").replace('sr','cr') else "" )    
        srtt  = by[sr][tt].round(2)
        crtt  = by[cr][tt].round(2)
        crttl = "\multirow{4}{*}{%s}"%(by[cr][tt].round(2)) if cr==sr.replace("vla","a").replace("vlb","b").replace('sr','cr')\
                                        else ( "\multirow{3}{*}{%s}"%(by[cr][tt].round(2)) if cr==sr.replace("lc","c").replace('sr','cr') else "" )
        tfw  = round( (srw / crw).val ,3)
        tftt = round( (srtt/ crtt).val ,3)
        tftot= round( ( (srw+srtt)/(crw+crtt) ).val , 3)
        dtf  = round( tftt-tfw ,3)
        dbrat= round( (doubleRatio(sr,cr)).val   , 3)
        rval = R(sr,cr).val
        rfac = round( rval/( (1+rval)*(1+rval) ) , 3)
        reltf= round( dtf/tftot,3)
        #syst = round( ( 0.20 * (1 - dbrat ) )*100 , 2)
        syst = round( ( 0.20 * (reltf) ) * rfac *100 , 2)
        ret = [
                srw,
                crwl,
                srtt,
                crttl,
                tfw,
                tftt,
                tftot,
                #dbrat,
                reltf ,
                rfac,
                syst,
               ]
        return ret, syst
    
    legend        = [
                      "Region",
                      "$N^{W}_{SR}$",
                      "$N^{W}_{CR}$",
                      "$N^{tt}_{SR}$",
                      "$N^{tt}_{CR}$",
                      "$TF^{W}_{SR/CR}$",
                      "$TF^{tt}_{SR/CR}$",
                      "$TF_{SR/CR}$",
                      #"$TF^{W}/TF^{tt}$",
                      "$\Delta TF/TF$",
                      "$R/(1+R)^2$",
                      "Syst.(\%)",
                    ]

    #double_ratio = [ doubleRatio(sr,cr) for sr,cr in sr_map.items() ]


    #nuises       = [ round( 1+(0.2* doubleRatio(sr,cr).val ),2) for sr, cr in sr_map.items() ]

    table = [legend] + [ [niceRegionName(sr)]+makeRow(sr,sr_map[sr])[0] for sr in sr_regions if sr in card_regions_pt]
    syst_dict     = { sr: { 'WJets': makeRow(sr,sr_map[sr])[1] , 'TTJets': makeRow(sr,sr_map[sr])[1] } for sr in sr_regions}
    syst_with_crs = { sr: { 'WJets': convertRelSystToLNN(  makeRow(sr,sr_map[sr])[1]) , 
                            'TTJets': convertRelSystToLNN( makeRow(sr,sr_map[sr])[1]) } 
                      for sr in sr_regions }
    makeSimpleLatexTable( np.array(table), "WTTPt3", cfg.saveDir , align_char = 'l')

    #systs       = { sr:  degTools.u_float( makeRow(sr,sr_map[sr])[1] )  for sr in sr_regions }
    systDir     = cfg.results_dir + "/" + cfg.cutInstList[0].baseCut.saveDir +"/Systematics_%s"%cfg.cutInstList[0].name
    output_file = systDir + "/" + "WTTPtShape_Systematics.pkl"
    pickle.dump( syst_dict, file( output_file ,'w')  )


    #output_file = systDir + "/" + "WTTPtShape_syst_dict.pkl"
    #pickle.dump( syst_dict, file( output_file ,'w')  )
    #output_file = systDir + "/" + "WTTPtShape_syst_with_crs.pkl"
    #pickle.dump( syst_with_crs, file( output_file ,'w')  )
    #systs = { sr:round( 1- ( 0.20 * (1-doubleRatio(sr,sr_map[sr]).val) ) ,2) for sr in sr_regions }
    return syst_dict, syst_with_crs


def getCovarMatrix( cfg, args, syst ):
    res = syst.res
    regions_info = syst.regions_info
    c1=ROOT.TCanvas('covar','covar', 1500,900 )


    srbins = [ x for x in regions_info.getCardInfo("MTCTLepPtVL2")['card_regions'] if 'sr' in x]
    fullcovar = res['overalls']['shapes_fit_b']['fullcovar']
    hist      = makeTH2FromDict(fullcovar, 'fullcovar' , xbins=srbins, ybins=srbins )
    hist.Draw("COLZ")
    saveCanvas(c1, cfg.saveDir +"/SystSummaries/" , "Covar_SRs" )


    srbins    = [ x for x in regions_info.getCardInfo("MTCTLepPtSum")['card_regions'] if 'sr' in x]
    histptinc = makeTH2FromDict(fullcovar, 'fullcovar' , xbins=srbins, ybins=srbins )
    histptinc.Draw("COLZ")
    saveCanvas(c1, cfg.saveDir +"/SystSummaries/" , "Covar_SRsPtInc" )
    

    return hist

main_regions = ['sr1vlaX', 'sr1laX', 'sr1maX', 'sr1haX', 'sr1vlaY', 'sr1laY', 'sr1maY', 'sr1haY', 'sr1vlbX', 'sr1lbX', 'sr1mbX', 'sr1hbX', 'sr1vlbY', 'sr1lbY', 'sr1mbY', 'sr1hbY', 'sr1lcX', 'sr1mcX', 'sr1hcX', 'sr1lcY', 'sr1mcY', 'sr1hcY', 'sr2vlaX', 'sr2laX', 'sr2maX', 'sr2haX', 'sr2vlaY', 'sr2laY', 'sr2maY', 'sr2haY', 'sr2vlbX', 'sr2lbX', 'sr2mbX', 'sr2hbX', 'sr2vlbY', 'sr2lbY', 'sr2mbY', 'sr2hbY', 'sr2lcX', 'sr2mcX', 'sr2hcX', 'sr2lcY', 'sr2mcY', 'sr2hcY', 'cr1aX', 'cr1aY', 'cr1bX', 'cr1bY', 'cr1cX', 'cr1cY', 'cr2aX', 'cr2aY', 'cr2bX', 'cr2bY', 'cr2cX', 'cr2cY']

def makeCRTable(cfg, args, syst):

    d = {k:{s:y for s,y in v.iteritems() if s in ['Fakes', 'TTJets','WJets','Total','Others', 'DataBlind'] } 
                for k,v in syst.variations_yld_sums['central']['lep'].iteritems() if 'cr' in k.lower() and ('X' in k or 'Y' in k) and len(k)>4 }

    table = makeTableFromDict( d, signal='' , func =lambda x, samp: int(x.val) if samp=='DataBlind' else round_figures(x,2) )
    tx = makeSimpleLatexTable( table, "CRswStat2", cfg.saveDir +"/SystSummaries/" )
    sfs = [(b,dict_operator( d[b], ['DataBlind', 'Fakes', 'Others', 'WJets','TTJets'], lambda d,f,o,w,t : ((d-f-o)/(w+t)).round(3) )) for b in d.keys() ]
    sfs.sort()
    print sfs
    return sfs





def makeSystTable( cfg, args , syst_dicts , syst_types) :  # bkgYields, regions_info):

    sigSysts = syst_types['Sig'] + syst_types['BkgSig']
    bkgSysts = syst_types['Bkg'] + syst_types['BkgSig']


    fakeEstimateOutput = pickle.load(file( cfg.results_dir +"/presel_base/fakeEstimateOutput_bins_mtct_sum.pkl" ))
    samps = fakeEstimateOutput['prompt_fake_yields']['lep']['sr1maX'].keys()
    bkgs = [ x for x in samps  if 'T2' not in x]
    bins = fakeEstimateOutput['prompt_fake_yields']['lep'].keys()
    bkgYields = { b:{ s:fakeEstimateOutput['prompt_fake_yields']['lep'][b][s] for s in bkgs} for b in bins }
    by = bkgYields

    regions_info = fakeEstimateOutput['regions_info']
    crmap_pt = regions_info.getCardInfo("MTCTLepPtVL2")['card_cr_sr_map']
    card_regions_pt = regions_info.getCardInfo("MTCTLepPtVL2")['card_regions']
    crmap_ptinc        = regions_info.getCardInfo("MTCTLepPtSum")['card_cr_sr_map']
    card_regions_ptinc = regions_info.getCardInfo("MTCTLepPtSum")['card_regions']
    
    crmap = {}
    for cr in crmap_pt.keys():
        crmap[cr]= crmap_pt[cr] + crmap_ptinc[cr]

    card_regions = list(set( card_regions_pt + card_regions_ptinc ) )
    card_regions = regions_info.sort_regions( card_regions ) 

    sr_regions   = [ sr for sr in card_regions if 'sr' in sr]
    cr_regions   = [ cr for cr in card_regions if 'cr' in cr]

    srmap = {sr:[ cr for cr,srs in crmap.items() if sr in srs][0] for sr in sr_regions}


    w  = "WJets"        
    tt = "TTJets"       
    f  = "Fakes"
    o  = "Others"
    tot= "Total"
    d  = "DataBlind"
    bkgs = [w,tt,f, o]

    varFromSyst = lambda b, p, syst_dict:  (1+ syst_dict[b].get(p,0)*0.01)* by[b][p].val 
    deltaVal    = lambda b, p, syst_dict:  ( syst_dict[b].get(p,0)*0.01 ) * by[b][p].val

    getTF = lambda sr : (( by[sr][w] + by[sr][tt] ) / ( by[srmap[sr]][w] + by[srmap[sr]][tt]  )).round(4).val 

    getSF    = lambda sr : (( by[srmap[sr]][d] - by[srmap[sr]][o] - by[srmap[sr]][f] ) / ( by[srmap[sr]][w] + by[srmap[sr]][tt]  )).round(4) 
    getSFVar = lambda sr ,syst_dict : round(( by[srmap[sr]][d].val - varFromSyst( srmap[sr],o,syst_dict)-varFromSyst( srmap[sr],f,syst_dict ) )/\
                                     ( varFromSyst( srmap[sr] , w , syst_dict) + varFromSyst( srmap[sr] , tt, syst_dict) )  ,4)
    
    
    

 
    #NSRTrue  = lambda sr : by[sr][w] + by[sr][tt]+by[sr][o]+by[sr][f] 
    #NSRPred = lambda sr : (by[sr][w] + by[sr][tt])*getSF(sr) +by[sr][o]+by[sr][f] 

    #NSRTrueVar = lambda sr, syst_dict : varFromSyst(sr,w,syst_dict)+varFromSyst(sr,tt,syst_dict)+varFromSyst(sr,o,syst_dict)+varFromSyst(sr,f,syst_dict)
    #NSRPredVar = lambda sr, syst_dict : getSFVar(sr,syst_dict ).val*(varFromSyst(sr,w,syst_dict) + varFromSyst(sr,tt,syst_dict))+\
    #                                         varFromSyst(sr,o,syst_dict)+varFromSyst(sr,f,syst_dict)

    #SRSyst = lambda sr, syst_dict:  (NSRPredVar(sr, syst_dict) /NSRTrueVar(sr,syst_dict) )/ ( NSRPred(sr)/NSRTrue(sr) ).val

    #
    #
    #

    #NSRPred = lambda sr : getTF(sr) * (by[sr][d]- by[sr][o] - by[sr][f] )
    NSRTrue  = lambda sr : by[sr][w] + by[sr][tt]+by[sr][o]+by[sr][f] 
    NSRPred  = lambda sr : getTF(sr) * ( by[srmap[sr]][w] + by[srmap[sr]][tt]  ) + by[sr][o] + by[sr][f]
 
    NSRTrueVar = lambda sr, syst_dict: varFromSyst(sr,w,syst_dict)+varFromSyst(sr,tt,syst_dict)+varFromSyst(sr,o,syst_dict)+varFromSyst(sr,f,syst_dict)
    NSRPredVar = lambda sr, syst_dict: getTF(sr)*(varFromSyst(srmap[sr],w,syst_dict)+varFromSyst(srmap[sr],tt,syst_dict))+\
                                                   varFromSyst(sr,o,syst_dict)+varFromSyst(sr,f,syst_dict) 
    
    #NSRPredVar = lambda sr, syst_dict : getTF(sr ).val*( by[srmap[sr]][d].val - varFromSyst(srmap[sr],o,syst_dict) - varFromSyst(srmap[sr],f,syst_dict))+\
    #                                         varFromSyst(sr,o,syst_dict)+varFromSyst(sr,f,syst_dict)
    SRSyst = lambda sr, syst_dict:  (NSRPredVar(sr, syst_dict) /NSRTrueVar(sr,syst_dict) )/ ( NSRPred(sr)/NSRTrue(sr) ).val


    ptIncSRs   = [ sr for sr in sr_regions if not anyIn(['vl', 'l', 'm','h'] , sr) ]
    #ptIncSRs   = [ sr for sr in sr_regions if  anyIn(['vl', 'l', 'm','h'] , sr) ]
    bkgsysttable = [ ["Systematic"] + [ niceRegionName(sr) for sr in ptIncSRs ] ]
    for systname in bkgSysts:
        bkgsysttable.append( [systname] + [ round( abs( (SRSyst(sr,syst_dicts[systname] )-1 )*100) , 2) for sr in ptIncSRs ])
    makeSimpleLatexTable( np.array(bkgsysttable).T, "BkgSystSummary", cfg.saveDir +"/SystSummaries/" , align_char = 'l')
    makeSimpleLatexTable( np.array(bkgsysttable), "BkgSystSummary_T", cfg.saveDir +"/SystSummaries/" , align_char = 'l')
    ptIncSRs   = [ sr for sr in sr_regions if not anyIn(['vl', 'l', 'm','h'] , sr) ]

    bkgsysttablefull = [ ["Systematic"] + [ niceRegionName(sr) for sr in sr_regions ] ]
    for systname in bkgSysts:
        bkgsysttablefull.append( [systname] + [ round( abs( (SRSyst(sr,syst_dicts[systname] )-1 )*100) , 2) for sr in sr_regions ])
    makeSimpleLatexTable( np.array(bkgsysttablefull).T, "BkgSystSummary_AllSRBins", cfg.saveDir +"/SystSummaries/" , align_char = 'l')

    bkgsysttablefull = [ ["Systematic"] + [ niceRegionName(sr) for sr in ptIncSRs ] ]
    for systname in bkgSysts:
        if 'Fakes' in systname: continue
        bkgsysttablefull.append( [systname] + [ round( abs(syst_dicts[systname][sr][tot]- syst_dicts[systname][srmap[sr]][tot])  , 2) for sr in ptIncSRs ])
    makeSimpleLatexTable( np.array(bkgsysttablefull).T, "BkgSystCRMinusSR", cfg.saveDir +"/SystSummaries/" , align_char = 'l')
    makeSimpleLatexTable( np.array(bkgsysttablefull), "BkgSystCRMinusSR_T", cfg.saveDir +"/SystSummaries/" , align_char = 'l')

    
    
 
    #
    # Sig Systs
    #
   
    sampleList = samps
    sigModels = [ x for x in set( [ degTools.getSignalModel(s_) for s_ in sampleList ] ) if x]
    sigModelLists = { sigModel:[s_ for s_ in sampleList if sigModel in s_] for sigModel in sigModels}
    sig_syst_summary= {sigModel: { systname:{} for systname in sigSysts}  for sigModel in sigModels}
    bms = ['300_270', '500_470', '425_415', '450_380' ]

    leg1 = [ "Systematic", "range (mean\pmstdev)" ]
    rows = {}
    bmrows = {}
    tables   = {sigModel:[ ['Systematic']  +[niceRegionName(sr) for sr in sr_regions]]  for sigModel in sigModels}
    bmtables = {sigModel:[ ['Systematic']  +[niceRegionName(sr) for sr in sr_regions]]  for sigModel in sigModels}


    for sigModel in sigModels:
        for systname in sigSysts:
            syst_dict = syst_dicts[systname] 
            print systname
            for sr in sr_regions:
                print sr
                #sigvals = np.array( [ abs(syst_dict[sr].get(s,0)) for s in sigModelLists[sigModel]  ] )
                sigvals = np.array( [ abs(syst_dict[sr][s]) for s in sigModelLists[sigModel]   if s in syst_dict[sr]] )
 
                summary = {
                            'max' : sigvals.max(),
                            'min' : sigvals.min(),
                         'median' : np.median(sigvals),
                            'mean': sigvals.mean(),
                            'std' : sigvals.std(), 
                          }
                sigbms = { sigModel+"_"+bm: syst_dict[sr].get( sigModel+"_"+bm , 0 ) for bm in bms }
                summary.update(sigbms)
                sig_syst_summary[sigModel][systname][sr]=summary 

        for systname in sigSysts:
            row = [  systname  ]
            bmrow = [ systname ]
            for sr in sr_regions:
                summary = sig_syst_summary[sigModel][systname][sr]
                row.extend(   ["[%0.2f-%0.2f] (%0.2f$\pm$%0.2f)"%(summary['min'] , summary['max'], summary['mean'], summary['std'] )] ) 
                bmrow.extend( [','.join(['%0.2f'%summary[sigModel+"_"+bm] for bm in bms ])] )
            tables[sigModel].append( row )         
            bmtables[sigModel].append( bmrow )         
        makeSimpleLatexTable( np.array(tables[sigModel]).T, "%s_SigSystsSummary"%sigModel, cfg.saveDir +"/SystSummaries/" , align_char = 'l')
        makeSimpleLatexTable( np.array(bmtables[sigModel]).T, "%s_SigSystsBMPoints"%sigModel, cfg.saveDir +"/SystSummaries/" , align_char = 'l')
        lepPtIncTable    =  np.array( filter( lambda x: not anyIn( ['VL','L','M','H'] , x[0] ) , np.array( tables[sigModel] ).T ) )
        makeSimpleLatexTable( lepPtIncTable.T , "%s_SigSystsSummary_LepPtInc"%sigModel, cfg.saveDir +"/SystSummaries/" , align_char = 'l')
        lepPtIncBMTable  = np.array(  filter( lambda x: not anyIn( ['VL','L','M','H'] , x[0] ) , np.array( bmtables[sigModel] ).T ) )
        makeSimpleLatexTable( lepPtIncBMTable.T , "%s_SigSystsBMPoints_LepPtInc"%sigModel, cfg.saveDir +"/SystSummaries/" , align_char = 'l')


    return tables, bmtables
        

    #legend        = [
    #                  "Region",
    #                  "$N^{W}_{SR}$",
    #                  "$N^{W}_{CR}$",
    #                  "$N^{tt}_{SR}$",
    #                  "$N^{tt}_{CR}$",
    #                  "$TF^{W}_{SR/CR}$",
    #                  "$TF^{tt}_{SR/CR}$",
    #                  "$TF_{SR/CR}$",
    #                  #"$TF^{W}/TF^{tt}$",
    #                  "$\Delta TF/TF$",
    #                  "$R/(1+R)^2$",
    #                  "Syst.(\%)",
    #                ]

    ##double_ratio = [ doubleRatio(sr,cr) for sr,cr in sr_map.items() ]


    ##nuises       = [ round( 1+(0.2* doubleRatio(sr,cr).val ),2) for sr, cr in sr_map.items() ]

    #table = [legend] + [ [niceRegionName(sr)]+makeRow(sr,sr_map[sr])[0] for sr in sr_regions]
    #syst_dict     = { sr: { 'WJets': makeRow(sr,sr_map[sr])[1] , 'TTJets': makeRow(sr,sr_map[sr])[1] } for sr in sr_regions }
    #syst_with_crs = { sr: { 'WJets': convertRelSystToLNN(  makeRow(sr,sr_map[sr])[1]) ,
    #                        'TTJets': convertRelSystToLNN( makeRow(sr,sr_map[sr])[1]) }
    #                  for sr in sr_regions }
    #makeSimpleLatexTable( np.array(table), "WTTPt3", cfg.saveDir , align_char = 'l')





def getOtherComposition():
    card_regions = regions_info.getCardInfo("MTCTLepPtSum")['card_regions']
    othersComp   = {bkg: {r:bkgYields[r][bkg]  for r in card_regions  }  for bkg in ["QCD","DY","Single top","VV","ttX"] }

    otherCompHists = {bkg: degTools.makeHistoFromDict(v, name=bkg, bin_order=card_regions) for bkg,v in othersComp.items() }
    h_color= {
                'QCD'    :  619   , 
               'DY'      :  1715  ,    
             'Single top':  1710  , 
            'VV'         :  813   ,   
            'ttX'        :  856   , 
            }

    for bkg,hist in otherCompHists.items():
        hist.SetFillColor( h_color[bkg] )
        hist.SetLineColor( h_color[bkg] )

    stack = degTools.getStackFromHists( otherCompHists.values() )
    norm_stack = degTools.normalizeStack( stack )

    norm_stack.Draw("hist")
    norm_stack.Draw("same")
    saveCanvas( ROOT.c1, cfg.saveDir, "BkgCompositionOthers_PtSum" )


def simpleSignif( mlf):
    signif = lambda di : (di['data'] - di['total_background'] ).val / math.sqrt( di['total_covar'].val + (di['data'].sigma)**2)
    signifs = dict( [ (b,signif( mlf.mlf_results['shapes_fit_b'][b])) for b in card_regions if 'sr' in b])
    sighist = makeHistoFromDict(signifs, name="Signifs", bin_order = [sr for sr in card_regions if 'sr' in sr] )
    sighist.GetYaxis().SetTitle("(obs-exp)/(#sigma)")
    sighist.LabelsOption("V")
    sighist.Draw()
    saveCanvas( ROOT.gPad, saveDir , "Signifs")


    pull = lambda pre, post ,b : ( post[b]['total_background'] - pre[b]['total_background'] ).val / math.sqrt( ( post[b]['total_covar'] ).val )
    pulls = dict( [ (b,pull( mlf.mlf_results['shapes_prefit'], mlf.mlf_results['shapes_fit_b'], b) ) for b in card_regions if 'sr' in b])
    pullshist = makeHistoFromDict(pulls, name="pulls", bin_order = [sr for sr in card_regions if 'sr' in sr] )
    pullshist.LabelsOption("V")
    pullshist.GetYaxis().SetTitle("(post-pre)/(#sigma_{post})")
    pullshist.Draw()
    saveCanvas( ROOT.gPad, saveDir , "Pulls")

    #
    pullhist = ROOT.TH1D("pullh","pullh", 30,-3,3)
    for i,sv in enumerate( signifs.values() ): pullhist.Fill( sv)
    pullhist.Draw()
    saveCanvas( ROOT.gPad, saveDir , "Pulls2")


#
#di = {}
#sr= 'sr1laX'
#di['cr_central'] = dict( [ (bkg, by[srmap[sr]][bkg].round(3).val) for bkg in bkgs ] + [ ('data', int(by[srmap[sr]]['DataBlind'].val ))] )
#di['sr_central'] = dict( [ (bkg, by[sr][bkg].round(3).val) for bkg in bkgs ] )#+ [ ('data', by[sr]['DataBlind'] )]
#di['cr_wpt']     = dict( [ (bkg, round( varFromSyst(srmap[sr] , bkg , syst.syst_dicts['WPt'] ),3) ) for bkg in bkgs ] )#+ [ ('data', by[sr]['DataBlind'] )]
#di['sr_wpt']     = dict( [ (bkg, round( varFromSyst(sr , bkg , syst.syst_dicts['WPt'] ) ,3)       ) for bkg in bkgs ] ) #+ [ ('data', by[sr]['DataBlind'] )]
#
#
#di['sr_central'] = [ (bkg, by[sr][bkg].round(3).val) for bkg in bkgs ] #+ [ int('data', by[sr]['DataBlind'].val) )]
#di
#di['cr_central'] = [ (bkg, by[srmap[sr]][bkg].round(3).val) for bkg in bkgs ] + [ 'data', int(by[srmap[sr]]['DataBlind'].val) )]

    #return bkgsysttable


    #NSRPredVar = lambda sr, syst_dict : getTF(sr).val( 




   #getTFprime = lambda sr , syst_dict : (varFromSyst(sr,w,syst_dict) + varFromSyst(sr,tt,syst_dict))/\
    #                                     (varFromSyst( srmap[sr],w,syst_dict) + varFromSyst(srmap[sr],tt,syst_dict))

    #predSyst = lambda  srsyst, crsyst : ((1 + srsyst*0.01 )/(1  + crsyst*0.01) - 1 ) * 100   # (1+srsig)/(1+crsig) -1  ~= srsig - crsig  
    #def totSyst (sr, syst_dict):
    #    cr      = srmap[sr]
    #    bkgTot  = by[sr][tot]
    #    tf      = getTF(sr).val
    #    dCR     = ( deltaVal(cr, f, syst_dict) + deltaVal(cr, o, syst_dict ) ) 
    #    dSR     = ( deltaVal(sr, f, syst_dict) + deltaVal(sr, o, syst_dict ) ) 
    #    #systTot = (-dCR*tf + dSR) / bkgTot.val  * 100
    #    tfprime = getTFprime(sr, syst_dict) 
    #    wttsum  = (by[cr][w] + by[cr][tt]).val
    #    systTot = ( (tfprime-tf)*wttsum  -dCR*tf + dSR) / bkgTot.val * 100 
    #    print "(%s + %s + %s )/( %s ) "%((tfprime-tf)*wttsum, -dCR*tf, dSR , bkgTot.val )
    #    return systTot

    #bkg_syst_summaries = {systname:{} for systname in avail_systs}

     
    #for sr in sr_regions:
    #    for systname in ['WPt', 'TTIsr']:
    #        srsyst = syst_dicts[systname][sr][tot]
    #        crsyst = syst_dicts[systname][srmap[sr]][tot]
    #        bkg_syst_summaries[systname][sr] = predSyst( srsyst, crsyst ) 

    #di = {}
    #di['cr_wpt'] = [ (bkg, varFromSyst(srmap[sr] , bkg , syst.syst_dicts['WPt'] ) ) for bkg in bkgs ] #+ [ ('data', by[sr]['DataBlind'] )]
    #di['cr_central'] = [ (bkg, by[srmap[sr]][bkg].round(3).val) for bkg in bkgs ] + [ ('data', by[srmap[sr]]['DataBlind'] )]
    #di['sr_central'] = [ (bkg, by[sr][bkg].round(3).val) for bkg in bkgs ] #+ [ ('data', by[sr]['DataBlind'] )]
    #di['sr_wpt'] = [ (bkg, varFromSyst(sr , bkg , syst.syst_dicts['WPt'] ) ) for bkg in bkgs ] #+ [ ('data', by[sr]['DataBlind'] )]
    #di
    #di['sr_central'] = [ (bkg, by[sr][bkg].round(3).val) for bkg in bkgs ] #+ [ int('data', by[sr]['DataBlind'].val) )]
    #di
    #di['cr_central'] = [ (bkg, by[srmap[sr]][bkg].round(3).val) for bkg in bkgs ] + [ 'data', int(by[srmap[sr]]['DataBlind'].val) )]
    #di['cr_central'] = [ (bkg, by[srmap[sr]][bkg].round(3).val) for bkg in bkgs ] + [ 'data', int(by[srmap[sr]]['DataBlind'].val )]
    #di



    #tot_systs = {}
    #for systname in bkgSysts:
    #    tot_systs[systname] = {}
    #    for sr in sr_regions:
    #        tot_systs[systname][sr] = syst_dicts[systname][sr][tot] 

        #for systname in [ 'FakesNonUniv', 'FakesNonClosure']:


samples_summary_others = {
                    'w':['w'],
                   'tt_2l':['tt_2l'],
                   'tt_1l':['tt_1l'],
                'others': [ 'dy', 'vv','st', 'ttx' ],
                'dy'    : ['dy'],
                'st'    : ['st'],
                'vv'    : ['vv'],
                'qcd'    : ['qcd'],
                'z'    : ['z'],
                'ttx'    : ['ttx'],
                'fakes':['qcd','z'],
                'Total':['w','tt_2l','tt_1l', 'dy','vv','st','ttx'],
                'dblind':['dblind']
                #'Total':['w','tt_2l','tt_1l', 'dy','vv','st','ttx', 'qcd', 'z'],
                  }


samples_summary_tt = {
                    'w':['w'],
                   'tt_2l':['tt_2l'],
                   'tt_1l':['tt_1l'],
                'others': [ 'dy', 'vv','st', 'ttx' ],
                'fakes':['qcd','z'],
                'Total':['w','tt_2l','tt_1l', 'dy','vv','st','ttx'],
                #'Total':['w','tt_2l','tt_1l', 'dy','vv','st','ttx', 'qcd', 'z'],
                  }


def decomposeOthers( cfg, args, syst , samples_summary = samples_summary_others):
    yld = pickle.load(file( cfg.yieldPkls[ cfg.cutInstList[0].fullName ]  )) 
    yldSums = getYieldsSummary( yld,  samples_summary, syst.regions_info.card_regions_map )

    sr_regions, cr_regions, sr_map, cr_map = getSummaryRegions( syst )
    sr_regions = [x for x in sr_regions if anyIn(['vl','l','m','h'] , x) ]

    for b in yldSums.keys():
        others = yldSums[b]['Others']
        yldSums[b]['StatUnc'] = round( (others.sigma/others.val*100) ,2) if others.val else 0
        

    table = makeTableFromDict( yldSums, sr_regions, data='', signal='', total='', bkg=['DY','VV','ttX','Single top', 'Others', 'StatUnc'], 
                                    niceNames={'Others':"Rare Total", 'StatUnc':'Stat. Unc.(\%)'} , 
                                    func = lambda v,samp: v.round(2) if not samp=='StatUnc' else round(v,1) )

    makeSimpleLatexTable(table, "OthersDecomposed", cfg.saveDir +"/OthersDecompos/")





def getYieldSums2( cfg, args, syst):
    yld = cfg.yieldPkls[cfg.cutInstList[0].fullName]
    yldSums =  getYieldsSummary(pickle.load(file(yld)), samples_summary_others , syst.regions_info.card_regions_map )
    regions_info = syst.regions_info
    srbins = [ x for x in regions_info.getCardInfo("MTCTLepPtVL2")['card_regions'] if 'sr' in x]
    yldSums = {sr:yldSums[sr] for sr in srbins}
    return yldSums



def mlfOutput( cfg, args , tag = "AppPASv3_1__MTCTLepPtVL2"):
    resDir = cfg.results_dir + "/" + cfg.cutInstList[0].baseCut.name + "/Results_" + cfg.cutInstList[0].name
    mlfrespath = resDir + "/{tag}/mlf_output_{tag}.pkl".format(tag=tag) 
    mlfres = pickle.load(file(mlfrespath))

    return mlfres


def sigInRegions( cfg, args, syst , tag = "AppPASv3_1__MTCTLepPtVL2"):
    #yldSums = getYieldSums2( cfg, args, syst)

    #if not getattr(syst, "PFMETGENMETAVERAGED", False):
    #    syst.averagePFMetGenMET()

    mlf_results = mlfOutput(cfg,args , tag=tag)
    yldSumsSig = syst.central_yld_sum
    bkgPostFit = mlf_results['shapes_fit_b']


    regions_info = syst.regions_info
    srbins = [ x for x in regions_info.getCardInfo("MTCTLepPtVL2")['card_regions'] if 'sr' in x]

    sigList = ['T2tt_500_470','T2tt_375_365']
    contam  = {}
    for sr in srbins:
        sigs = {}
        #tot = yldSums[sr]['Total']
        contam[sr]={}
        tot = bkgPostFit[sr]['total_background']
        data_stat = math.sqrt(bkgPostFit[sr]['data'].val)
        contam[sr]['Total']=   bkgPostFit[sr]['total_background']
        tot = bkgPostFit[sr]['total_background'] + u_float(0, data_stat) 
        contam[sr]['Total_mcsys_datastat']=  tot
        contam[sr]['data'] = int( bkgPostFit[sr]['data'].val )
        contam[sr]['\sigma(data)'] = data_stat
        
        for sig in sigList:
            sigs[sig] = yldSumsSig[sr][sig]
            contam[sr][sig] = sigs[sig]
            contam[sr][sig+"/Bkg(\%)"   ] =  ( yldSumsSig[sr][sig].val  / tot.val   )*100 
            contam[sr][sig+"/\sigma"] =  ( yldSumsSig[sr][sig].val  / tot.sigma )
            contam[sr]["BkgErr"]      =  ( yldSumsSig[sr][sig].sigma            )
    
    table = makeTableFromDict( contam, bins = srbins , data='', signal='', total='', 
                               bkg= sigList + ['Total', '\sigma(data)' ] + [x+"/Bkg(\%)" for x in sigList ] + [x+"/\sigma" for x in sigList] , 
                               niceNameFunc=lambda x: x , 
                               func = lambda x, samp: safe_round(x,2),
                               ) 
    makeSimpleLatexTable( table, "%s_SigContam"%(prefix.upper()) , cfg.saveDir + "/SystSummaries/")


def compareNLOVV( ):
    yldSums      = pickle.load(file('final_yields.pkl'))
    yldSumsNLOVV = pickle.load(file('final_yields_nlovv2.pkl'))

    colors = {c:sample_colors[sampleInfo.sampleName(c,'shortName')] for c in [ 'VV' ,'WJets','TT_2l', 'TT_1l']}
    colors.update( {'Others':ROOT.kOrange, 'Total':ROOT.kBlack} )

    hists = {}
    for ys, yld  in ( ('incvv',yldSums), ('nlovv',yldSumsNLOVV)):
        hists[ys]={}
        for samp in ['Others','VV','Total','WJets','TT_2l', 'TT_1l']:
            hists[ys][samp] = makeHistoFromDict(  {sr:yld[sr][samp] for sr in srbins}, name='%s_%s'%(ys,samp), bin_order = srbins )
            hists[ys][samp].SetLineColor( colors[samp] )
            hists[ys][samp].LabelsOption("V") 
            if ys =='incvv':
                hists[ys][samp].SetLineStyle(9)

def getYieldSums( cfg, args , samples_summary, syst):
    yld = pickle.load(file( cfg.yieldPkls[ cfg.cutInstList[0].fullName ]  )) 
    yldSums = getYieldsSummary( yld,  samples_summary, syst.regions_info.card_regions_map )

    sr_regions, cr_regions, sr_map, cr_map = getSummaryRegions( syst )
    sr_regions = [x for x in sr_regions if anyIn(['vl','l','m','h'] , x) ]
    

    bkgYields = { b:{ s:yldSums[b][s] for s in ['WJets','TT_2l','TT_1l', 'Fakes','Others'] } for b in sr_regions + cr_regions }

    tt_info = deepcopy(bkgYields)


    for b in sr_regions:
        cr   = sr_map[b]
        tt1l = bkgYields[b]['TT_1l']
        tt2l = bkgYields[b]['TT_2l'] 
        tt   = tt1l + tt2l
        tt_info[b]['2l/tt (SR)']= tt2l/tt if tt.val else u_float(0) 
        tt_info[b]['TT_1l(SR)'] = tt1l
        tt_info[b]['TT_2l(SR)'] = tt2l
        tt1l_cr = bkgYields[cr]['TT_1l']
        tt2l_cr = bkgYields[cr]['TT_2l']
        tt_cr = tt1l_cr + tt2l_cr 
        tt_info[b]['TT_1l(CR)'] = tt1l_cr
        tt_info[b]['TT_2l(CR)'] = tt2l_cr
        tt_info[b]['2l/tt (CR)'] = tt2l_cr/tt_cr if tt_cr.val else u_float(0)

    table = makeTableFromDict( tt_info , sr_regions  , data='', signal='', total='', bkg=[ 'TT_1l(SR)','TT_2l(SR)','TT_1l(CR)','TT_2l(CR)', '2l/tt (SR)', '2l/tt (CR)'] )
    makeSimpleLatexTable( table, "TTSeperated", cfg.saveDir )

    src_regions = [sr for sr in sr_regions if 'c' in sr]
    table = makeTableFromDict( tt_info , src_regions  ,data='', signal='', total='', bkg=[ 'TT_1l(SR)','TT_2l(SR)','TT_1l(CR)','TT_2l(CR)', '2l/tt (SR)', '2l/tt (CR)'] )
    makeSimpleLatexTable( table, "TTSRCSeperated", cfg.saveDir )
   
    hsrs= makeHistoFromDict( {b:tt_info[b]['2l/tt (SR)'] for b in src_regions}, name='RatioSRs', bin_order = src_regions )
    hcrs= makeHistoFromDict( {b:tt_info[b]['2l/tt (CR)'] for b in src_regions}, name='RatioCRs', bin_order = src_regions )
    hsrs.SetLineColor(ROOT.kBlue)
    hsrs.SetMarkerSize(0)
    hcrs.SetLineColor(ROOT.kRed)
    hcrs.SetMarkerSize(0)


    hsrs.LabelsOption("V") 
    hsrs.SetMaximum(2)
    
    doubler = hsrs.Clone("doubleratio")
    doubler.Divide(hcrs)
    doubler.SetMaximum(2)
    unity = hsrs.Clone('one')
    unity.Divide(hsrs)
    unity.SetLineColor(ROOT.kBlack)
    unity.SetLineStyle(3)

 
    canvs = makeCanvasMultiPads('ttcomp' , pads=[], padRatios = [2,1] ) 
    canvs[1].cd()
    hsrs.Draw()
    hcrs.Draw('same')
    leg = ROOT.TLegend(0.2,0.6,0.5,0.8)  
    leg.AddEntry( hsrs , "tt2l/tt (SR)" )
    leg.AddEntry( hcrs , "tt2l/tt (CR)" )
    leg.Draw()
    canvs[2].cd()
    doubler.SetMarkerSize(1)   
    doubler.GetYaxis().SetTitle("SR / CR ")
    doubler.GetXaxis().SetLabelSize(0.09)
    doubler.GetYaxis().SetLabelSize(0.08)
    doubler.Draw()
    unity.Draw('hist same')

    saveCanvas( canvs[0], cfg.saveDir, "TTDoubleR_wrtTot" )



    #def lookAtJECs():
    ##JEC/JER
    jer = pickle.load(file("/afs/hephy.at/work/n/nrad/results/cards_and_limits//13TeV/8025_mAODv2_v7/80X_postProcessing_v1/EPS17_v0/June17_v3/LepGood_lep_lowpt_Jet_def_SF_Prompt_PU_TTIsr_Wpt_TrigEff_lepSFFix/DataBlind/presel_base/JECs/JER.pkl"))
    jec = pickle.load(file("/afs/hephy.at/work/n/nrad/results/cards_and_limits//13TeV/8025_mAODv2_v7/80X_postProcessing_v1/EPS17_v0/June17_v3/LepGood_lep_lowpt_Jet_def_SF_Prompt_PU_TTIsr_Wpt_TrigEff_lepSFFix/DataBlind/presel_base/JECs/JEC.pkl"))
    jec = pickle.load(file("/afs/hephy.at/work/n/nrad/results/cards_and_limits//13TeV/8025_mAODv2_v7/80X_postProcessing_v1/EPS17_v0/June17_v3/LepGood_lep_lowpt_Jet_def_SF_Prompt_PU_TTIsr_Wpt_TrigEff_lepSFFix/DataBlind/presel_base//Systematics_bins_mtct_sum/JEC.pkl"))
    jer = pickle.load(file("/afs/hephy.at/work/n/nrad/results/cards_and_limits//13TeV/8025_mAODv2_v7/80X_postProcessing_v1/EPS17_v0/June17_v3/LepGood_lep_lowpt_Jet_def_SF_Prompt_PU_TTIsr_Wpt_TrigEff_lepSFFix/DataBlind/presel_base//Systematics_bins_mtct_sum/JER.pkl"))

    
    jecinfo={}
    tot="Total"
    for sr in src_regions:
        if sr not in jer.syst_dict.keys(): continue
        cr = sr_map[sr]
        print b, cr
        jecinfo[sr] = {
                        'JER (SR)' : jer.syst_dict[sr][tot] , 
                        'JER (CR)' : jer.syst_dict[cr][tot] , 
                        'JEC (SR)' : jec.syst_dict[sr][tot] , 
                        'JEC (CR)' : jec.syst_dict[cr][tot] , 
                     }

    
    t = makeTableFromDict( jecinfo, src_regions  ,data='', signal='', total='', bkg=['JER (SR)','JER (CR)' , 'JEC (SR)','JEC (CR)'] , func = lambda x, samp: round(x,2))
    makeSimpleLatexTable( t, "JECJERs", cfg.saveDir )





def wtfjec():
    jer = pickle.load(file("/afs/hephy.at/work/n/nrad/results/cards_and_limits//13TeV/8025_mAODv2_v7/80X_postProcessing_v1/EPS17_v0/June17_v3/LepGood_lep_lowpt_Jet_def_SF_Prompt_PU_TTIsr_Wpt_TrigEff_lepSFFix/DataBlind/presel_base/JECs/JER.pkl"))
    jec = pickle.load(file("/afs/hephy.at/work/n/nrad/results/cards_and_limits//13TeV/8025_mAODv2_v7/80X_postProcessing_v1/EPS17_v0/June17_v3/LepGood_lep_lowpt_Jet_def_SF_Prompt_PU_TTIsr_Wpt_TrigEff_lepSFFix/DataBlind/presel_base/JECs/JEC.pkl"))
    jec_cutweights = degTools.dict_function( jec.variations_yld_pkl_files, lambda x: pickle.load(file(x.replace("Yields_","CutWeights_"))))
    jer_cutweights = degTools.dict_function( jer.variations_yld_pkl_files, lambda x: pickle.load(file(x.replace("Yields_","CutWeights_"))))
    jec_ylds = degTools.dict_function( jec.variations_yld_pkl_files, lambda x: pickle.load(file(x)))
    jer_ylds = degTools.dict_function( jer.variations_yld_pkl_files, lambda x: pickle.load(file(x)))


    jet_corrs     = {
              'jec_up'     : 'Jet_corr_JECUp{index}  *( 100*(Jet_corr_JER{index}==-99) + Jet_corr_JER{index} )'.format(index='IndexJet_basJet_def[0]')    ,
              'jec_central': 'Jet_corr{index}        *( 100*(Jet_corr_JER{index}==-99) + Jet_corr_JER{index} )'.format(index='IndexJet_basJet_def[0]')    ,
              'jec_down'   : 'Jet_corr_JECDown{index}*( 100*(Jet_corr_JER{index}==-99) + Jet_corr_JER{index} )'.format(index='IndexJet_basJet_def[0]')    ,

              'jer_up'     : 'Jet_corr{index}*  ( 100*(Jet_corr_JER{index}==-99) + Jet_corr_JERUp{index}   ) '.format(index='IndexJet_basJet_def[0]')      ,
              'jer_central': 'Jet_corr{index}*  ( 100*(Jet_corr_JER{index}==-99) + Jet_corr_JER{index}     ) '.format(index='IndexJet_basJet_def[0]')      ,
              'jer_down'   : 'Jet_corr{index}*  ( 100*(Jet_corr_JER{index}==-99) + Jet_corr_JERDown{index} ) '.format(index='IndexJet_basJet_def[0]')      ,

              'genMet'     : 'Jet_pt' ,
                }
    met_corrs = {

               'jec_up'     : ["met_JetEnUp_Pt"   ,"met_JetEnUp_Phi"     ]             ,
               'jec_central': ["met_pt"           ,"met_phi"             ]             ,
               'jec_down'   : ["met_JetEnDown_Pt" ,"met_JetEnDown_Phi"   ]               ,

               'jer_up'     : ["met_JetResUp_Pt"  ,"met_JetResUp_Phi"    ]              ,
               'jer_central': ["met_pt"           ,"met_phi"             ]             ,
               'jer_down'   : ["met_JetResDown_Pt","met_JetResDown_Phi"  ]                ,

                'genMet'    : ['met_genPt', 'met_genPhi'],
                }

    samples.tt_2l.tree.Draw("(Max$(Jet_rawPt)-Max$(( Jet_rawPt*( 1*  ( 100*(Jet_corr_JER==-99) + Jet_corr_JERUp   )  ) * ( abs(Jet_eta)<2.4  && (Jet_id) ) )))/Max$(Jet_rawPt)>>(100,-1,1)","")
    samples.tt_2l.tree.Draw("(Sum$(Jet_pt/Jet_corr)-Sum$(( Jet_pt*( Jet_corr * ( 100*(Jet_corr_JER==-99) + Jet_corr_JERUp   )  ) * ( abs(Jet_eta)<2.4  && (Jet_id) ) )))/(Sum$(Jet_pt/Jet_corr))","")




def makeOfficialPlots(): 
#if True:
    limits_dir = "/afs/hephy.at/work/n/nrad/results/cards_and_limits//13TeV/8025_mAODv2_v7/80X_postProcessing_v1/EPS17_v0/June17_v4/LepGood_lep_lowpt_Jet_def_SF_Prompt_STXSECFIX_PU_TTIsr_Wpt_TrigEff_lepSFFix/DataBlind/presel_base/Results_bins_mtct_sum/PreAppANv6_3__MTCTLepPtVL2_Bins/"
    plotDir = "/afs/hephy.at/user/n/nrad/www/T2Deg13TeV//8025_mAODv2_v7/80X_postProcessing_v1/EPS17_v0/June17_v4/LepGood_lep_lowpt_Jet_def_SF_Prompt_STXSECFIX_PU_TTIsr_Wpt_TrigEff_lepSFFix/DataBlind/presel_base/bins_mtct_sum/PreAppANv6_3__MTCTLepPtVL2_Bins/"
    limitpkls = glob.glob( limits_dir +"/*/*/limits/Limits_*.pkl")
    for limitpkl in limitpkls:
        l = pickle.load(file(limitpkl))
        dm_limit = sysTools.transformMassDict( l )
        dm_limit_file = limitpkl.replace("/Limits_","/DMLimits_")
        pickle.dump(dm_limit , file(dm_limit_file,'w') )
        model, region = limitpkl.rsplit("/")[-4:-2]
        limitTools.makeOfficialLimitPlot( dm_limit_file , tag="%s_%s"%(model,region), savePlotDir= plotDir, model= model if model=="T2bW" else "T2DegStop")
        assert False

def makeSignifPlots():
    import functools
    t2ttsignif_file ="/afs/hephy.at/work/n/nrad/results/cards_and_limits//13TeV/8025_mAODv2_v7/80X_postProcessing_v1/EPS17_v0/June17_v4/LepGood_lep_lowpt_Jet_def_SF_Prompt_STXSECFIX_PU_TTIsr_Wpt_TrigEff_lepSFFix/DataBlind/presel_base/Results_bins_mtct_sum/PreAppANv6_3__MTCTLepPtVL2/T2tt//signif/Signif_T2tt_PreAppANv6_3__MTCTLepPtVL2.pkl" 
    t2ttsignif = pickle.load(file(t2ttsignif_file))
    dmt2ttsignif =sysTools.transformMassDict(t2ttsignif)
    t2bwsignif   = pickle.load(file(t2ttsignif_file.replace("T2tt","T2bW")))
    dmt2bwsignif = sysTools.transformMassDict(t2bwsignif)

    t2ttsigplot = makeStopLSPPlot("T2tt_Signif", dmt2ttsignif, "T2tt_Signifs", bins=[23, 237.5, 812.5, 8, 5, 85], key = functools.partial( getValueFromDict, val='-1.000') )
    t2bwsigplot = makeStopLSPPlot("T2bW_Signif", dmt2bwsignif, "T2bW_Signifs", bins=[23, 237.5, 812.5, 8, 5, 85], key = functools.partial( getValueFromDict, val='-1.000') )
    ROOT.gStyle.SetPalette(ROOT.kRainBow);

    t2ttsigplot.GetZaxis().SetRangeUser(-1,3)
    t2bwsigplot.GetZaxis().SetRangeUser(-1,3)

    t2ttsigplot.Draw("COLZ TEXT89");
    ROOT.gPad.SaveAs("/afs/hephy.at/user/n/nrad/www/T2Deg13TeV//8025_mAODv2_v7/80X_postProcessing_v1/EPS17_v0/June17_v4/LepGood_lep_lowpt_Jet_def_SF_Prompt_STXSECFIX_PU_TTIsr_Wpt_TrigEff_lepSFFix/DataBlind/LimitPlotTests/T2tt_Signif.png")
    t2bwsigplot.Draw("COLZ TEXT89");
    ROOT.gPad.SaveAs("/afs/hephy.at/user/n/nrad/www/T2Deg13TeV//8025_mAODv2_v7/80X_postProcessing_v1/EPS17_v0/June17_v4/LepGood_lep_lowpt_Jet_def_SF_Prompt_STXSECFIX_PU_TTIsr_Wpt_TrigEff_lepSFFix/DataBlind/LimitPlotTests/T2bW_Signif.png")

    t2ttsigplot_smooth = ROOT.doSmooth( t2ttsigplot , 0 ) 
    t2ttsigplot_smooth.Draw("COLZ TEXT89")
    ROOT.gPad.SaveAs("/afs/hephy.at/user/n/nrad/www/T2Deg13TeV//8025_mAODv2_v7/80X_postProcessing_v1/EPS17_v0/June17_v4/LepGood_lep_lowpt_Jet_def_SF_Prompt_STXSECFIX_PU_TTIsr_Wpt_TrigEff_lepSFFix/DataBlind/LimitPlotTests/T2tt_Smooth_Signif.png")    

    t2bwsigplot_smooth = ROOT.doSmooth( t2bwsigplot , 0 ) 
    t2bwsigplot_smooth.Draw("COLZ TEXT89")
    ROOT.gPad.SaveAs("/afs/hephy.at/user/n/nrad/www/T2Deg13TeV//8025_mAODv2_v7/80X_postProcessing_v1/EPS17_v0/June17_v4/LepGood_lep_lowpt_Jet_def_SF_Prompt_STXSECFIX_PU_TTIsr_Wpt_TrigEff_lepSFFix/DataBlind/LimitPlotTests/T2bW_Smooth_Signif.png")    


ROOT.gROOT.ProcessLine(".L /afs/hephy.at/work/n/nrad/CMSSW/CMSSW_8_0_20/src/Workspace/DegenerateStopAnalysis/python/limits/MonoJetAnalysis/limits/interpolate.h+")

def makeSignifPlots(output_tag = "AppPASv3_1__MTCTLepPtVL2", docalc=False):
    #output_tag="AppPASv3_0__MTCTLepPtVL2"
    outputdir_temp = syst.resDir + "/{output_tag}/{model}/"
    card_basename = "%s"%(cfg.generalTag)

    plts=[]
    import functools
    #ROOT.gStyle.SetPalette(ROOT.kRainBow)
    #ROOT.gStyle.SetPalette(ROOT.kRainBow);
    ROOT.TCanvas()
    plots = []
    pkls  = []
    models = ['T2bW','T2tt']
    for model in models: 
        output_dir = outputdir_temp.format(output_tag=output_tag, model=model)
        syst.calcAndPlotLimits(output_dir, card_basename,output_tag,syst.saveDir+"/%s/"%output_tag,sigModelName=model,docalc=docalc, runMode='--paral', signif=True,scale_rule=lambda m1,m2:1)
        output_pkl = output_dir + "/signif/Signif_%s_%s.pkl"%(model,output_tag)
        signif    = pickle.load(file(output_pkl))
        signifsdm = sysTools.transformMassDict(signif)
        plt= makeStopLSPPlot("%s_Signif"%model, signifsdm, "%s_Signifs"%model, bins=[23, 237.5, 812.5, 8, 5, 85], 
                                                key = functools.partial( getValueFromDict, val='-1.000') )
        pkls.append( (model, signifsdm) )
        plt.GetZaxis().SetRangeUser(-1.5,2.5)
        plt.Draw("COLZ TEXT89")
        sysTools.drawCMSHeader( lxy=[0.16, 0.955], rxy=[0.72, 0.955], cmsinside=False )
        plots.append(plt)
        #saveCanvas( ROOT.gPad, syst.saveDir +"/%s/"%output_tag, "%s_Signif"%model)
    
        pltsmooth = ROOT.doSmooth( plt, 0)
        pltsmooth.Draw("COLZ TEXT89")
        sysTools.drawCMSHeader( lxy=[0.16, 0.955], rxy=[0.72, 0.955], cmsinside=False )
        #saveCanvas( ROOT.gPad, syst.saveDir +"/%s/"%output_tag, "%s_Smooth_Signif"%model)
        plots.append(pltsmooth)

    fakepkls = []
    lkeys = ['0.500', '0.840', '0.975', '0.160', '-1.000', '0.025']
    for i, model in enumerate( models ):
        fake = {m1:{dm: {x:pkls[i][1][m1][dm]['-1.000'] for x in lkeys } for dm in pkls[i][1][m1].keys()} for m1 in pkls[i][1].keys() }
        output_pkl = output_dir + "/signif/Signif2_%s_%s.pkl"%(model,output_tag)
        pickle.dump( fake, file(output_pkl,'w') )
        limitTools.makeOfficialLimitPlot( output_pkl, tag=output_tag, savePlotDir=syst.saveDir + "/%s/%s/"%(output_tag, model), model={'T2bW':'T2bW', 'T2tt':'T2DegStop'}[model], dmplot=True, signif=True)
        #shifted_fake = dict_function( fake , lambda x: x+10)
        
        
    return plots , pkls





def makeSRDiagrams( cfg,args, output_tag = "AppPASv3_1__MTCTLepPtVL2" ):
    mlf_res_pkl = cfg.results_dir + "/postfit_results.pkl"
    bkg_ylds     = pickle.load( file(mlf_res_pkl) )['shapes_fit_b']
    
    sig_ylds     = pickle.load( file( cfg.results_dir +"/yld_sums_all_June17_v4_VVNLO_v2.pkl" ) )['main']
    ewk_ylds     = pickle.load( file("/afs/hephy.at/work/n/nrad/results/cards_and_limits//13TeV/8025_mAODv2_v7/80X_postProcessing_v1/EPS17_v0/June17_v4__EWK_/LepGood_lep_lowpt_Jet_def_SF_Prompt_STXSECFIX_PU_TTIsr_Wpt_TrigEff_lepSFFix/DataBlind/ylds_sum_ewk.pkl" ))
    for b in ewk_ylds.keys():
        if b in sig_ylds.keys():
            sig_ylds[b].update( ewk_ylds[b] )     


    models = list(set([getSigModelMasses(x)[0] for x in sig_ylds[b].keys() if getSigModelMasses(x) ]))
    all_sigs = [x for x in sig_ylds[b].keys() if anyIn(models, x) ]
    sigModels = {model:[x for x in all_sigs if model in x] for model in models }
    
    sig = 'T2tt_375_365'

    srbins = [x for x in main_regions if 'sr' in x]
    

    sigOverSigma = lambda sig: "%s/sigma"%sig

    yldinfo = {}
    for b in bkg_ylds.keys():
        yldinfo[b] = {}
        yldinfo[b]['bkg_tot'] = bkg_ylds[b]['total_background']
        #yldinfo[b]['bkg_sigma'] = round( yldinfo[b]['bkg_tot'].sigma/yldinfo[b]['bkg_tot'].val , 4 ) if yldinfo[b]['bkg_tot'].val else 0
        yldinfo[b]['bkg_sigma'] =  yldinfo[b]['bkg_tot'].sigma 
        yldinfo[b]['data']      = bkg_ylds[b]['data']
        yldinfo[b]['data_stat'] =  math.sqrt( yldinfo[b]['data'].val )
        yldinfo[b]['tot_sigma'] =  (yldinfo[b]['bkg_tot'] + u_float(0, yldinfo[b]['data_stat'] ) ).sigma

    for sig in all_sigs:
        for b in bkg_ylds.keys():
            yldinfo[b][sig] = sig_ylds[b][sig]
            yldinfo[b][sigOverSigma(sig)] = (sig_ylds[b][sig] / yldinfo[b]['tot_sigma']).round(3).val
    
    mtct_tags = [ ''.join(x) for x in itertools.product( ['a','b','c'] , ['X','Y']  )   ]
    #ptbins    = ['vl','l','m','h', ]
    ptbins    = ['sr1vl','sr1l','sr1m','sr1h','sr2vl','sr2l','sr2m','sr2h' ]

    htemp = ROOT.TH2D('temp','temp', 8,0,8, 6, 0 , 6) 

    setAxisLabels( htemp, axis='Y', labels = mtct_tags )
    setAxisLabels( htemp, axis='X', labels = [x.upper() for x in ptbins] ) 
    htemp.GetZaxis().SetRangeUser(0,3)

    

    def getSigDiag(sig):
        for sr in ['']:
            h = htemp.Clone("%s_%s"%(sig,sr))
            for ix, ptbin in enumerate( ptbins) :
                for iy, mtct_tag in enumerate( mtct_tags ):
                    if 'vl' in ptbin and 'c' in mtct_tag:
                        continue
                    srname = sr +ptbin + mtct_tag
                    h.SetBinContent(ix+1,iy+1, yldinfo[srname][sigOverSigma(sig)] ) 
        return h

    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.04)

    main_dir = cfg.saveDir + "/SRDiagrams/"
    for model, sigList in sigModels.items():
        d = main_dir + "/" + model +"/"
        makeDir(d)
        for sig in sigList:
            h = getSigDiag( sig ) 
            h.Draw("COLZ TEXT")
            latex.DrawLatex(0.5,0.96, sig)
            ROOT.gPad.SaveAs(d+"/%s.png"%sig)


