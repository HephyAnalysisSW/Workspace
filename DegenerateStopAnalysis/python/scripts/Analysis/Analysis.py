"""
Execute this script after running
ipython -i degStop.py -- --cfg=EPS17_v0 --task=yields "" --skim=filterMETHT250JEC "" --generalTag=TestTag  --lepCol=LepGood --lep=lep --sigOpt=bm --bkgs ttx vv qcd st z dy tt_1l tt_2l w --nProc=10 --jetThresh=def --lepThresh=lowpt --data="" --weights STXSECFIX sf prompt pu isr_tt wpt trig_eff lepsffix --cut=bins_mtct_sum_sig ""

will produce a test card test_T2tt_300_270_testcard.txt
calculate limit with ./../tools/.calcLimit.py test_T2tt_300_270_testcard.txt
"""


import Workspace.DegenerateStopAnalysis.tools.limitTools as limitTools
import Workspace.DegenerateStopAnalysis.tools.degTools as degTools
import Workspace.DegenerateStopAnalysis.tools.sysTools as sysTools
import Workspace.DegenerateStopAnalysis.tools.fakeEstimate as fakeEstimate
import Workspace.DegenerateStopAnalysis.samples.baselineSamplesInfo as sampleInfo
import Workspace.DegenerateStopAnalysis.tools.CombineCard as CombineCard
CombinedCard = CombineCard.CombinedCard
#from   Workspace.DegenerateStopAnalysis.tools.regionsInfo import *
from Workspace.DegenerateStopAnalysis.scripts.addSigToResults import *
import subprocess
import pickle
from copy import deepcopy

mstop_scale_threshold = 0
XSEC_SCALE            = 100.
scale_rule            = lambda mstop, mlsp: 1/XSEC_SCALE if mstop <= mstop_scale_threshold else False  ## to rescale the r value since xsec was already scaled

GAUSTHRESH            = 50
RATEPARAM             = True
LEPSFSYSTFIX          = True
LnU                   = False
OLDWTTPTSYST          = False
OTHERSXSECCORR        = True
prefix                = ''


rerunSysts  = False
rerunMLF    = False
doCalcLimit = True

#if prefix:
#    SPLIT_BINS = False


sigModelTags = degTools.sigModelTags 


from collections import OrderedDict




modelsInfoSystHist = deepcopy( degTools.modelsInfo ) 
for model in modelsInfoSystHist.keys():
    if "T2" in model:
        modelsInfoSystHist[model]['binning_dm'] = [23, 237.5, 812.5, 8, 5, 85 ]


def niceRegionName(r):
    ret = r.replace("sr","SR").replace("cr","CR").replace("vl","VL").replace("l","L").replace("v","V").replace("h","H").replace("m","M")
    return ret



def getYieldsSummary(yld, samples_summary, card_regions_map = None, include_rest = True):
    """
        Prepare instance of Yields class for card writing.
    """

    bkgList = yld.bkgList
    yldsByBins = yld.getByBins( yld.yieldDict )
    ylds_sums = {}
    defined_samps = [x  for y  in samples_summary.values() for x in y]
    samples_summary = deepcopy( samples_summary)
    rest_of_samples = [samp for samp in yld.sampleList if samp not in defined_samps] 
    if card_regions_map : 
        yldsByBins = getYieldsCardRegions( yldsByBins, card_regions_map)
    for b in yldsByBins.keys():
        ylds_sums[b] = {}
        for p, slist in samples_summary.items():
            pNiceName = p #FIXME 
            #pNiceName = sampleInfo.sampleName(p, name_opt = 'niceName')
            ylds_sums[b][pNiceName] = degTools.dict_operator(yldsByBins[b] , slist , func  = lambda *x: sum(x) if x else degTools.u_float(0))
        if include_rest:
            for p in rest_of_samples:
                pNiceName = p #FIXME 
                #pNiceName = sampleInfo.sampleName(p, name_opt = 'niceName')
                ylds_sums[b][pNiceName] = yldsByBins[b][p]
    return ylds_sums

def getYieldsCardRegions( yldByBins, card_regions_map ):
    yldsCardRegions= {}
    for b , blist in card_regions_map.iteritems():
        if all( [b_ in yldByBins.keys() for b_ in blist] ):
            yldsCardRegions[b]    = degTools.dict_manipulator( [ yldByBins[b_] for b_ in blist], func = lambda *args: sum(args)  ) 
        elif b in yldByBins.keys() :
            yldsCardRegions[b] = yldByBins[b]
        elif '2' in b:
            r1 = b.replace('2','1')
            if r1 in card_regions_map:
                blist_ = [ b_.replace('1','2') for b_  in card_regions_map[r1] ] 
                if all([b_ in yldByBins.keys() for b_ in blist_]):
                    print b, "is not in there, but this is", r1, 'will use these', blist_
                    yldsCardRegions[b]    = degTools.dict_manipulator( [ yldByBins[b_] for b_ in blist_], func = lambda *args: sum(args)  ) 
    return yldsCardRegions




def makeSignalCard(yldByBin, bkgList, sig, data, card_syst_dicts, bins_order, cr_sr_map, blind = True, blindProcName = "Total",  output_dir = "./", name = "test", post_fix="testcard"):
    avail_systs  = card_syst_dicts.keys()
    avail_systs  = sorted( sorted( avail_systs ), key = lambda x: 'sig' in x.lower()  )
    sample_list = bkgList + [sig] + [data] 


    print "Sample_list", sample_list
 
    print "!!!!!!!!!!!!!", yldByBin[yldByBin.keys()[0]]
 
    yieldDict    = { samp: { b: yldByBin[b][samp] for b in yldByBin.keys()}  for samp in sample_list+["Total"]}

    map_name_niceName  = {
                      'w'       :  'WJets'      ,
                      'tt'      :  'TTJets'   ,
                      'z'       :  'ZJetsInv' ,
                      'qcd'     :  'QCD'     ,
                      'dy'      :  'DYJetsM50',
                      'vv'      :  'Diboson'  ,
                      'st'      :   'ST'      ,
                      #'other'   :   'Other'      ,
                      }
    niceProcessNames = map_name_niceName
    
    cfw        = CombinedCard( niceProcessNames = niceProcessNames , maxUncNameWidth = 20 , lnn_gmn_threshold = GAUSTHRESH);
    cfw.addBins( bkgList , bins_order )
    

    if blind:
        if FULLBLIND:
            cfw.allowNonIntegerObservation = True
            cfw.specifyObservations(           yieldDict , blindProcName , makeInt = lambda x: x.val )

        else:
            cfw.specifyObservations(           yieldDict , sampleInfo.sampleName(data), bins = [b for b in bins_order if  'cr' in b])
            cfw.specifyObservations(           yieldDict , blindProcName , makeInt = lambda x: int(round(x.val)) , bins = [b for b in bins_order if  'sr' in b])
        
    else:
        cfw.specifyObservations(           yieldDict , sampleInfo.sampleName(data))
    cfw.specifyBackgroundExpectations( yieldDict , bkgList )


    cr_regions = [r for r in bins_order if 'cr' in r]
    doRateParam=RATEPARAM
    if doRateParam:
        yieldDictOrig = degTools.deepcopy(yieldDict)    


    for cr in cr_regions:
        if not cr in bins_order:
            continue
        srs_ = cr_sr_map[cr]
        srs  = [sr for sr in srs_ if sr in bins_order ] 
        #bkgProc = ["TTJets"] if "rtt" in cr else ["WJets"]
        
        bkgProcs = [ "WJets","TTJets"]
        bkgProcShortNames = {"TTJets":"TT", "WJets":"W"}
        #if doRateParam:
        crCorDist = "lnN" if not LnU else "lnU"
        if False:
            for bkgProc in bkgProcs:
                crVal = None
                for r in [cr] + srs:
                    isCR =  r==cr
                    bkgProcShortName = bkgProcShortNames[bkgProc] 
                    rateParamName = r+bkgProcShortName
                    expectationKey = ( r, bkgProc) 
                    if expectationKey not in cfw.expectation:
                        raise Exception("For safety specify expectation first before using the rate param!")
                    bkgVal = cfw.expectation[ expectationKey ]
                    cfw.specifyExpectation( expectationKey[0], expectationKey[1], 1.0 )
                    assert cfw.expectation[ expectationKey ] == 1.0
                    if isCR:
                        crVal = bkgVal
                        crRateParamName = rateParamName
                        cfw.addRateParam( crRateParamName, cr, bkgProc, crVal , [0,3*crVal])
                    else:
                        srVal = bkgVal
                        assert crVal != None, (bkgProc, r, [crs]+srs , srVal, crVal)  
                        sf = srVal/crVal
                        eq="({sf}*@0)".format(sf=sf)
                        args = crRateParamName
                        cfw.addRateParam( rateParamName, r, bkgProc, eq, args)
        if doRateParam:
            crVal = 0
            crVals=[]
            crParamNames=[]
            cr_wtt_vals = [ cfw.expectation[ (r,bkg) ] for r in [cr] for bkg in bkgProcs]
            sr_wtt_vals = [ cfw.expectation[ (r,bkg) ] for r in  srs for bkg in bkgProcs]
             
            for r in [cr] + srs:
                isCR     =  r==cr
                firstBkg =  True
                for bkgProc in bkgProcs:
                    bkgProcShortName = bkgProcShortNames[bkgProc] 
                    rateParamName    = r+bkgProcShortName
                    expectationKey   = ( r, bkgProc) 
                    if expectationKey not in cfw.expectation:
                        raise Exception("For safety specify expectation first before using the rate param!")
                    bkgVal = cfw.expectation[ expectationKey ]
                    cfw.specifyExpectation( expectationKey[0], expectationKey[1], 1.0 )
                    assert cfw.expectation[ expectationKey ] == 1.0
                        


                    if isCR:
                        if firstBkg:  #use the nominal value
                            firstCRBkgRateParam = rateParamName
                            firstCRBkgVal = bkgVal
                            cfw.addRateParam( rateParamName, cr, bkgProc, bkgVal , [0,3*bkgVal])
                            firstBkg = False
                        else:  #lock to the firstBkg
                            args=firstCRBkgRateParam
                            sf=bkgVal/firstCRBkgVal
                            eq="({sf}*(@0))".format(sf=sf)
                            cfw.addRateParam( rateParamName, cr, bkgProc, eq, args)
                        #crVal += bkgVal
                        #crVals.append(bkgVal)
                        #crRateParamName   = rateParamName
                        #crParamNames.append(crRateParamName)
                    else:   
                        if firstBkg: #lock to the firstCrBkg
                            firstSRBkgRateParam = rateParamName
                            firstSRBkgVal = bkgVal
                            tf_crsr = bkgVal/firstCRBkgVal
                            eq="({tf_crsr}*(@0))".format(tf_crsr=tf_crsr)
                            args = firstCRBkgRateParam
                            cfw.addRateParam( rateParamName, r, bkgProc, eq, args)
                            firstBkg = False
                        else:
                            sf = bkgVal/firstSRBkgVal
                            tf_crsr = firstSRBkgVal/firstCRBkgVal
                            eq="({tf_crsr}*{sf}*(@0))".format( tf_crsr=tf_crsr, sf=sf)
                            args = firstCRBkgRateParam
                            cfw.addRateParam( rateParamName, r, bkgProc, eq, args)
                        
        elif False:
        #if True:
            crVal = 0
            crVals=[]
            crParamNames=[]
            cr_wtt_vals = [ cfw.expectation[ (r,bkg) ] for r in [cr] for bkg in bkgProcs]
            sr_wtt_vals = [ cfw.expectation[ (r,bkg) ] for r in  srs for bkg in bkgProcs]
             
            for r in [cr] + srs:
                isCR =  r==cr
                for bkgProc in bkgProcs:
                    bkgProcShortName = bkgProcShortNames[bkgProc] 
                    rateParamName    = r+bkgProcShortName
                    expectationKey   = ( r, bkgProc) 
                    if expectationKey not in cfw.expectation:
                        raise Exception("For safety specify expectation first before using the rate param!")
                    bkgVal = cfw.expectation[ expectationKey ]
                    cfw.specifyExpectation( expectationKey[0], expectationKey[1], 1.0 )
                    assert cfw.expectation[ expectationKey ] == 1.0
                    if isCR:
                        crVal += bkgVal
                        crVals.append(bkgVal)
                        crRateParamName   = rateParamName
                        crParamNames.append(crRateParamName)
                        cfw.addRateParam( crRateParamName, cr, bkgProc, bkgVal , [0,3*crVal])
                    else:
                        srVal = bkgVal
                        assert crVal != 0, (bkgProc, r, [cr]+srs , srVal, crVal)  
                        assert len(crVals)==2, crVals
                        assert sum(crVals)==crVal, (crVals, crVal)
                        print r, bkgVal, crVals
                        sf = srVal/crVal
                        eq="({sf}*(@0+@1))".format(sf=sf)
                        args = ",".join(crParamNames)
                        cfw.addRateParam( rateParamName, r, bkgProc, eq, args)
                        

                #for r in srs+[cr]:
                #    yieldDict[r][bkgProc]=degTools.u_float(1)
                #    #addRateParam( name, bin, process, val_or_form , minmax_or_arg = None )

        elif WTT_CRCORR:
            sname   = cr+"_corr"
            cfw.addUncertainty        ( sname ,  crCorDist)
            cfw.specifyFlatUncertainty( sname ,  CRCORR, bins=[cr], processes = bkgProcs)
            cfw.specifyFlatUncertainty( sname ,  CRCORR, bins=srs , processes = bkgProcs)
        else:
            for bkgProc in bkgProcs:
                sname   = cr + bkgProcShortNames[bkgProc] +"_corr"
                cfw.addUncertainty        ( sname , crCorDist )
                cfw.specifyFlatUncertainty( sname ,  2, bins=[cr], processes = [bkgProc])
                cfw.specifyFlatUncertainty( sname ,  2, bins=srs , processes = [bkgProc])


    mstop, mlsp = degTools.getMasses( sig )
    scale = 1.0
    cfw.comment = "Signal: %s "%sig
    if mstop <= mstop_scale_threshold:
        scale        =   1/XSEC_SCALE
        cfw.comment +=   " Scaled by %s"%scale
    cfw.specifySignalExpectations(  yieldDict , sig  , scale = scale)





    for sname in avail_systs:
    #for sname in ['SigISR', 'BTag_l']:
        print sname
        if sname in systTypes['BkgSig']:
            print "SigBkg", bkgList +[sig]
            cfw.specifyUncertaintiesFromDict(  card_syst_dicts ,  [sname] , bkgList +['signal'], bins = bins_order)
        elif sname in systTypes['Bkg']:
            print "Bkg", bkgList
            cfw.specifyUncertaintiesFromDict(  card_syst_dicts ,  [sname] , bkgList, bins = bins_order)
        elif sname in systTypes['Sig']:
            print "Sig", sig
            cfw.specifyUncertaintiesFromDict(  card_syst_dicts ,  [sname] , ['signal'], bins = bins_order)
        else:
            raise Exception("Syst %s is not sigSyst and is not bkgSyst... then WHAT IS IT? HUH? \n systTypes %s"%(sname,systTypes) ) 

    #assert False 
    #if True:
    #    return {'cardname': '' , 'cfw':cfw}

    cfw.addUncertainty        ( "lepEff"   ,"lnN")
    if LEPSFSYSTFIX:
        cfw.specifyFlatUncertainty( "lepEff"   , 1.01 , bins = [b for b in cfw.bins if "sr" in b] )# , processes =['signal','WJets','TTJets', 'Fakes','Others'] )
    else:
        cfw.specifyFlatUncertainty( "lepEff"   , 1.05 , bins = [b for b in cfw.bins if "sr" in b] )# , processes =['signal','WJets','TTJets', 'Fakes','Others'] )

    #stat uncert for lepton sf
    lepsf_stat_uncert_file = os.path.expandvars( "$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/data/leptonSFs/lepSF_stat_uncerts.pkl")
    lepsf_stat_uncert = pickle.load( file( lepsf_stat_uncert_file ) )
    cfw.addUncertainty( "lepSFStat", "lnN")
    for b in lepsf_stat_uncert.keys():
        bName = prefix + b
        sysval = lepsf_stat_uncert[b]
        if prefix == 'vw':
            bName  = bName.replace("X","").replace("Y","")
            sysval = (lepsf_stat_uncert[b.replace("X","Y")] + lepsf_stat_uncert[b.replace("Y","X")] ) /2.0 ## average x and y
        if prefix == 'vb' and bName not in cfw.bins:
            bName = bName.replace("X","").replace("Y","")
            sysval = (lepsf_stat_uncert[b.replace("X","Y")] + lepsf_stat_uncert[b.replace("Y","X")] ) /2.0
        #if prefix and bName not in cfw.bins:
        #    continue
        if bName not in cfw.bins:
            continue
        for p in ["signal", "TTJets","WJets","Fakes","Others" ]:
            cfw.specifyUncertainty( "lepSFStat", bName, p, sysval )


    #w tt pt reweight
    if OLDWTTPTSYST:
        wttpt_syst_file = os.path.expandvars( "$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/data/WTTPtSystematics.pkl")
        wttpt_syst      = pickle.load( file( wttpt_syst_file ) )
        cfw.addUncertainty( "WttPt", "lnN")
        for b in wttpt_syst.keys():
            bName = prefix + b
            sysval = wttpt_syst[b]
            if prefix == 'vw':
                bName  = bName.replace("X","").replace("Y","")
                sysval = (wttpt_syst[b.replace("X","Y")] + wttpt_syst[b.replace("Y","X")] ) /2.0 ## average x and y
            if prefix == 'vb' and bName not in cfw.bins:
                bName = bName.replace("X","").replace("Y","")
                sysval = (wttpt_syst[b.replace("X","Y")] + wttpt_syst[b.replace("Y","X")] ) /2.0
            #if prefix == 'vw':
            ##    bName = bName.replace("X","").replace("Y","")
            #print bName
            #if prefix and  bName not in cfw.bins:
            #    continue
            if bName not in cfw.bins:
                continue
            cfw.specifyUncertainty( "WttPt", bName, "WJets" , sysval  )
            cfw.specifyUncertainty( "WttPt", bName, "TTJets", sysval  )


            

    cfw.addUncertainty        ( "trigEff"   ,"lnN")
    cfw.specifyFlatUncertainty( "trigEff"   , 1.01 , bins = [b for b in cfw.bins if "sr" in b] )# , processes =['signal','WJets','TTJets', 'Fakes','Others'] )
    cfw.addUncertainty        ( "lumi"      ,"lnN")
    cfw.specifyFlatUncertainty( "lumi"      , 1.025 , processes=['signal'] )
    cfw.addUncertainty        ( "sigFastFull"   ,"lnN")
    cfw.specifyFlatUncertainty( "sigFastFull"   , 1.02 , processes=['signal'] )
    cfw.addUncertainty        ( "lepSigEff"   ,"lnN")
    cfw.specifyFlatUncertainty( "lepSigEff"   , 1.02 , processes=['signal'] )
    cfw.addUncertainty        ( "sigPU"   ,"lnN")
    cfw.specifyFlatUncertainty( "sigPU"   , 1.01 , processes=['signal'] )



    if OTHERSXSECCORR:
        if True: 
            sys_val = 1.5
            sname   = "OthersXSecSysSR1"
            cfw.addUncertainty( sname , "lnN" )
            cfw.specifyFlatUncertainty( sname, sys_val, processes = ["Others"], bins = [ b for b in cfw.bins if 'sr1' in b] )
            sname = "OthersXSecSysSR2"
            cfw.addUncertainty( sname , "lnN" )
            cfw.specifyFlatUncertainty( sname, sys_val, processes = ["Others"], bins = [ b for b in cfw.bins if 'sr2' in b] )
            sname   = "OthersXSecSysCR1"
            cfw.addUncertainty( sname , "lnN" )
            cfw.specifyFlatUncertainty( sname, sys_val, processes = ["Others"], bins = [ b for b in cfw.bins if 'cr1' in b] )
            sname = "OthersXSecSysCR2"
            cfw.addUncertainty( sname , "lnN" )
            cfw.specifyFlatUncertainty( sname, sys_val, processes = ["Others"], bins = [ b for b in cfw.bins if 'cr2' in b] )
        else: # fully correlated ... probably much too aggressive 
            for p, sys_val in ( ('Others', 1.5 ), ):
                sname = "%sXSecSys"%(p)
                cfw.addUncertainty( sname , "lnN" )
                cfw.specifyFlatUncertainty( sname, sys_val, processes = [p], bins = [] )
    else: # add 50% for others uncorrelated
        for b in bins_order:
            for p, sys_val in ( ('Others', 1.5 ), ):
                sname = "%s%sSys"%(b,p)
                cfw.addUncertainty( sname , "lnN" )
                cfw.specifyFlatUncertainty( sname, sys_val, processes = [p], bins = [b] )
        
    cfw.addStatisticalUncertainties(yieldDict= yieldDict)



    cardname =  output_dir+"/"+ "%s_%s_%s.txt"%(name, sig, post_fix) 
    print "Card Written to: %s"%cardname
    cfw.writeToFile(cardname)
    #assert False
    return {'cardname': cardname , 'cfw':cfw}



if __name__ == "__main__":

    cutName     = cfg.cutInstList[0].name
    cutNameFull = cfg.cutInstList[0].fullName 
    yld = pickle.load(file(cfg.yieldPkls[cutNameFull]))
    bkgs = ['w', 'tt', 'others', 'fakes', 'Total'] #cfg.bkgList  yld.bkgList 

    samples_summary = {
                        'w':['w'],
                       'tt':['tt_2l', 'tt_1l'],
                    'others': [ 'dy', 'vv','st', 'ttx' ],
                    'fakes':['qcd','z'],
                    #'Total':['w','tt_2l','tt_1l', 'dy','vv','st','ttx'],
                    'Total':['w','tt_2l','tt_1l', 'dy','vv','st','ttx', 'qcd', 'z'],
                      }

    try:
        from   Workspace.DegenerateStopAnalysis.tools.regionsInfo import RegionsInfo
        print "************ Using RegionsInfo Module ************* "
        opt = "MTCTLepPtVL2"
        regions_info = RegionsInfo( yld.cutNames )
        card_regions_info = regions_info.getCardInfo( opt )
        card_regions   = card_regions_info['card_regions']
        card_cr_sr_map = card_regions_info['card_cr_sr_map']
    except ImportError:
        card_regions     = ['sr1vlaX', 'sr1laX', 'sr1maX', 'sr1haX', 'sr1vlaY', 'sr1laY', 'sr1maY', 'sr1haY', 'sr1vlbX', 'sr1lbX', 'sr1mbX', 'sr1hbX', 'sr1vlbY', 'sr1lbY', 'sr1mbY', 'sr1hbY', 'sr1lcX', 'sr1mcX', 'sr1hcX', 'sr1lcY', 'sr1mcY', 'sr1hcY', 'sr2vlaX', 'sr2laX', 'sr2maX', 'sr2haX', 'sr2vlaY', 'sr2laY', 'sr2maY', 'sr2haY', 'sr2vlbX', 'sr2lbX', 'sr2mbX', 'sr2hbX', 'sr2vlbY', 'sr2lbY', 'sr2mbY', 'sr2hbY', 'sr2lcX', 'sr2mcX', 'sr2hcX', 'sr2lcY', 'sr2mcY', 'sr2hcY', 'cr1aX', 'cr1aY', 'cr1bX', 'cr1bY', 'cr1cX', 'cr1cY', 'cr2aX', 'cr2aY', 'cr2bX', 'cr2bY', 'cr2cX', 'cr2cY'] 
        card_cr_sr_map = {
                          'cr1aX': ['sr1vlaX', 'sr1laX', 'sr1maX', 'sr1haX'],
                          'cr1aY': ['sr1vlaY', 'sr1laY', 'sr1maY', 'sr1haY'],
                          'cr1bX': ['sr1vlbX', 'sr1lbX', 'sr1mbX', 'sr1hbX'],
                          'cr1bY': ['sr1vlbY', 'sr1lbY', 'sr1mbY', 'sr1hbY'],
                          'cr1cX': ['sr1lcX' , 'sr1mcX', 'sr1hcX'          ],
                          'cr1cY': ['sr1lcY' , 'sr1mcY', 'sr1hcY'          ],
                          'cr2aX': ['sr2vlaX', 'sr2laX', 'sr2maX', 'sr2haX'],
                          'cr2aY': ['sr2vlaY', 'sr2laY', 'sr2maY', 'sr2haY'],
                          'cr2bX': ['sr2vlbX', 'sr2lbX', 'sr2mbX', 'sr2hbX'],
                          'cr2bY': ['sr2vlbY', 'sr2lbY', 'sr2mbY', 'sr2hbY'],
                          'cr2cX': ['sr2lcX' , 'sr2mcX', 'sr2hcX'          ],
                          'cr2cY': ['sr2lcY' , 'sr2mcY', 'sr2hcY'          ]
                         }

    yldsum = getYieldsSummary(yld, samples_summary )

  


    card = makeSignalCard(yldsum, bkgs, 'T2tt_300_270', 'Total', {}, card_regions , card_cr_sr_map , blind = False)
    res  = limitTools.calcLimit( card['cardname'] )
