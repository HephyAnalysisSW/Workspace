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
    sample_legends = bkg + [ total, data ]
    if signal: sample_legends += [signal]
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



def makeCRTable(cfg, args, syst):

    d = {k:{s:y for s,y in v.iteritems() if s in ['Fakes', 'TTJets','WJets','Total','Others', 'DataBlind'] } for k,v in syst.variations_yld_sums['central']['lep'].iteritems() if 'cr' in k.lower() and ('X' in k or 'Y' in k) and len(k)>4 }

    table = makeTableFromDict( d )
    tx = makeSimpleLatexTable( table, "CRswStat", cfg.saveDir +"/SystSummaries/" )
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
            for sr in sr_regions:
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


