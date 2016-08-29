from Workspace.DegenerateStopAnalysis.tools.degTools import fixForLatex , dict_operator, anyIn, whichIn
import os
import pickle

def fix_region_name(name):
    return name.replace("_","/").replace("pos","Q+").replace("neg","Q-")

#def dict_operator ( yldsByBin , keys = [] , func =  lambda *x: sum(x) ):
#    """
#    use like this dict_operator( yields_sr, keys = ['DataBlind', 'Total'] , func = lambda a,b: a/b)
#    """ 
#    args = [ yldsByBin[x] for x in keys]
#    return func(*args) 


def getPkl( pkl_path, def_dict={}):
    pkl_path = os.path.expandvars(pkl_path)
    print 'get pkl %s'%pkl_path
    if os.path.isfile( pkl_path):
        ret = pickle.load(file(pkl_path))
        print "pkl:", ret.keys()
    else:
        ret = deepcopy( def_dict )
        print "def", ret.keys()
    return ret


make_lumi_tag = lambda l: "%0.0fpbm1"%(l)
absSysFunc = lambda a,b : (abs(1.- (b/a).val)   * 100) if a.val else 0
#sysFunc    = lambda a,b : abs((b/a).val)  
#sysPercFunc= lambda a,b : abs(1.-(b/a).val)   
mean   = lambda l :   sum(l)/float(len(l)) if len(l) else None

def meanSys(*a):
    """assume first value is the central value"""
    central = a[0]
    variations = a[1:]
    if not variations:
        raise Exception("No Variations Given! %s"%a)
    systs = []
    for var in variations:
        systs.append( absSysFunc(central, var) ) 
    #print systs, mean(systs)
    return mean(systs)
    

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
                     #'\hline',
                     '\hline',
                     'CR1a',
                     'CR1b',
                     'CR1c',
                     'CR2',
                     'CRTT2',
                        ]

bins = [x for x in regions if 'hline' not in x]
main_sr =[
            'SR1a',
            'SR1b',
            'SR1c',
            'SR2',
         ]
main_cr =[
            'CR1a',
            'CR1b',
            'CR1c',
            'CR2',
         ]
card_bins =[ x for x in bins if x not in main_sr]
pt_srs = [x for x in bins if 'SR' in x and x not in main_sr]











lepCol = "LepAll"
lep    = "lep"
puRunTagParams ={   
                    'up'    :   { 'pu':'pu_up' },
                    'down'  :   { 'pu':'pu_down' },
                }
tagParams       = {
                      "PU":\
                            {
                                'up'    :   { 'pu':'pu_up' },
                                'down'  :   { 'pu':'pu_down' },
                            },
                      "BTag_l":\
                            {
                                'up'    :   { 'btag':'SF_L_UP'  },
                                'down'  :   { 'btag':'SF_L_DOWN'  },
                            },
                      "BTag_b":\
                            {
                                'up'    :   { 'btag':'SF_B_UP'  },
                                'down'  :   { 'btag':'SF_B_DOWN'  },
                            },
                      "WPt":\
                            {
                                '1x'  :   { 'wpt':'_wpt'  },
                            },
                      "ttpt":\
                            {
                                '1x'  :   { 'ttpt':'_ttpt'  },
                            },
                      "jec":\
                            {
                                'up'    :   { 'jec':'jec_up' },
                                'down'  :   { 'jec':'jec_down' },
                            },
                      "jer":\
                            {
                                'up'    :   { 'jer':'jer_up' },
                                'down'  :   { 'jer':'jer_down' },
                            },
                   }




centralParams = { 
                    'lepCol':lepCol,
                    'lep'   :lep,
                    'pu'    :'pu',
                    'btag'  :'SF',
                    'jec'   :'',
                    'jer'   :'',
                    'wpt'   :'',
                    'ttpt'  :'',
                }

class Systematics():
    def __init__(self, cfg, variationTagParams = puRunTagParams, centralParams = centralParams , name = "Syst"):
        self.name = name
        self.syst_name = name
        temp_dict = {}
        variations = ['%s_central'%self.name]
        for key, val in variationTagParams.iteritems():
            for def_key, def_val in centralParams.iteritems():
                val.setdefault(def_key, def_val)
            temp_dict["%s_%s"%(self.name, key)] = val
        variations.extend( temp_dict.keys() )
        temp_dict['%s_central'%self.name] = {}
        for def_key, def_val in centralParams.iteritems():
            temp_dict['%s_central'%self.name].setdefault(def_key, def_val)
        data          = 'DataBlind'
        data_lumi_tag = '%s_lumi'%data
        #for var, params in variationTagParams.iteritems():
        #    if params.get("jec"):
        #        isJEC = True
        #    if params.get("jer"):
        #        isJER = True
        self.variationTagParams = variationTagParams
        variationTagParams      = temp_dict
        #print variationTagParams
        sys_label = "AdjustedSys"
        cut_name = cfg.cutInstList[0].fullName
        self.yieldPkls=  {}
        self.yields   =  {}
        self.yieldDict = {}
        self.yieldTotals={}
        variation_dict = {}
        #variations = variationTagParams.keys()
        self.variations = variations
        tags            = variations
        self.runTags = {} 
        samples = self.yieldDict[tag].keys()
        self.samples =  samples
        for variation, params in variationTagParams.iteritems():
            runTag = 'PreApp_Mt95_Inccharge_{lepCol}_{lep}_{pu}{wpt}{ttpt}_{btag}'.format(**params)
            self.runTags[variation] = runTag
            results_dir          =  cfg.cardDirBase + "/13TeV/{ht}/{run}/".format( ht = cfg.htString , run = runTag )
            #lumiTag              =  make_lumi_tag( cfg.lumi_info['DataUnblind_lumi'] )
            lumiTag              =  make_lumi_tag( cfg.lumi_info[data_lumi_tag] )
            self.yieldPkls[variation]     =  results_dir + sys_label  + "/" + cfg.baseCutSaveDir  + "/Yields_%s_%s_%s.pkl"%( lumiTag , runTag, cut_name)    
            if params.get('jec') or params.get('jer'):
                self.yieldPkls[variation] = self.yieldPkls[variation].replace(u'/presel/', u'/presel_%s/'%variation)
                self.yieldPkls[variation] = self.yieldPkls[variation].replace(u'.pkl', u'_%s.pkl'%variation)
            self.yields[variation]        =  pickle.load(file( self.yieldPkls[variation]  ))
            self.yieldDict[variation]     =  self.yields[variation].getNiceYieldDict()
            self.yieldTotals[variation]   =  self.yieldDict[variation]['Total']
        #    print variation , params
        #    print params.get('jec')
        #assert False
        #self.res =    dict_manipulator( [ yields['pu_down'].getNiceYieldDict()['Total'] , yields['pu_up'].getNiceYieldDict()['Total'] , yields['pu'].getNiceYieldDict()['Total'] ] , lambda a,b,c: ( abs(1.-(a/c).val) + abs(1.-(b/c).val) )/2. * 100)

        self.tot_sys      =  dict_manipulator( [self.yieldDict[x]["Total"] for x in variations  ] , lambda *vals : meanSys(*vals)  )   

        self.res_dir      = os.path.expandvars("$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/results/2016/%s/%s/%s/"%(cfg.cmgTag, cfg.ppTag, cfg.runTag) )
        self.cr_sfs_path  = "%s/CR_SFs.pkl"%self.res_dir
        yldinsts_dir      = "%s/YieldInsts/"%(self.res_dir)
        ylds_dir          = "%s/YieldDicts/"%(self.res_dir)
        global_yield_pkl  = "%s/YieldDictWithVars.pkl"%(self.res_dir)
        makeDir(ylds_dir)
        makeDir(yldinsts_dir)

        #
        # Loading SF
        #

        bkg_est_dir = "$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/results/2016/%s_%s_%s/BkgEst/"%(cfg.cmgTag, cfg.ppTag, cfg.runTag)
        bkg_est_dir = os.path.expandvars( bkg_est_dir )
        self.CR_SFs = pickle.load(file(bkg_est_dir+"/CR_SFs.pkl"))

        sf_bin_keys = [ '1a' , '1b' , '1c', '2']
        SFs = {}
        for b in bins:
            SFs[b]={}
            for samp in samples:
                SFs[b][samp] = {}


        for samp, regions in self.yieldDict[tag].iteritems():
            for b,val in regions.iteritems():
                pass


        #
        # Storing YieldDicts for all variations
        # 
        for tag in tags:
            pickle.dump(  self.yields[tag] , open( "%s/YieldInst_%s.pkl"%(yldinsts_dir, tag) ,'w' ) )
            pickle.dump(  self.yieldDict[tag] , open( "%s/MCTruthDict_%s.pkl"%(ylds_dir, tag) ,'w' ) )
        global_yield_dict = getPkl( global_yield_pkl ) 
        for tag in tags:
            global_yield_dict[tag] = self.yieldDict[tag]
        pickle.dump(  global_yield_dict , open( global_yield_pkl ,'w' ) )
        self.all_yield_dict = global_yield_dict

        all_syst_cards_pkl       =  "%s/SystDictForCards.pkl"%(self.res_dir)
        all_syst_dict_pkl        =  "%s/SystDict.pkl"%(self.res_dir)

        if data in samples:
            samples.pop(samples.index(data))

        sample_card_systs = {}
        sample_systs = {}
        for samp in samples:
             sample_systs[samp]     =  dict_manipulator( [self.yieldDict[x][samp] for x in variations  ] , lambda *vals : meanSys(*vals)  )   
             sample_card_systs[samp]=  dict_manipulator( [self.yieldDict[x][samp] for x in variations  ] , lambda *vals : 1+ meanSys(*vals)/100.  )   

        bins_card_systs           =  Yields.getByBins(self.yields[tag], sample_card_systs)
        self.card_bins = bins_card_systs
    
        all_syst_cards_dict = getPkl( all_syst_cards_pkl )
        all_syst_dict       = getPkl( all_syst_dict_pkl  )
        
        print all_syst_dict_pkl
        print all_syst_dict.keys()
        if "WPt_central" in all_syst_dict: assert False,all_syst_dict.keys()

        all_syst_cards_dict[self.name] = {'bins':bins_card_systs , 'type':'lnN'}
        all_syst_dict[self.name]       = sample_systs

        pickle.dump( all_syst_cards_dict ,  open( all_syst_cards_pkl ,'w' ) ) 
        pickle.dump( all_syst_dict       ,  open( all_syst_dict_pkl , 'w' ) )  

        self.all_syst_cards = all_syst_cards_dict
        self.all_syst_dict  = all_syst_dict

        if "WPt_central" in all_syst_dict: assert False,all_syst_dict.keys()

        ##
        ##  Making Tables
        ##

        bkg_systs_dir = "$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/results/2016/%s_%s_%s/BkgSysts/"%(cfg.cmgTag, cfg.ppTag, cfg.runTag)
        bkg_systs_dir = os.path.expandvars(bkg_systs_dir)
        
        first_row = True
        table_list = [] 
        for region_name in regions:
                if region_name == "\hline":
                    table_list.append([region_name])
                    continue
                region   = region_name
                toPrint = [   
                              ["Region"     ,  fix_region_name( region_name )], 
                          ]
                for var in variations:
                    toPrint.append( [ var , self.yieldTotals[var][region_name] ] )
                toPrint.append(  ['Syst. ' , round (self.tot_sys[region_name] ,2)      ] )
                align = "{:<20}"*len(toPrint)
                if first_row:
                    print align.format(*[x[0] for x in toPrint])
                    first_row = False
                    table_list.append( [x[0] for x in toPrint]  ) 
        
                print align.format(*[x[1] for x in toPrint])
                table_list.append( [x[1] for x in toPrint])
        makeDir(os.path.expandvars(bkg_systs_dir))
        #pickle.dump(res , open( os.path.expandvars( bkg_systs_dir+"/%s.pkl"%self.name)  ,"w"))
        table = makeSimpleLatexTable( table_list, "%s.tex"%self.name, cfg.saveDir+"/BkgSysts/", align_char = "c" ,  align_func= lambda char, table: "c|"+ (char *(len(table[1])-2)).rstrip("|")+"|c" )
        print table

        #
        #   Syst and Yields per Sample
        #

        first_row = True
        table_list = []
        for region in regions:
                if region == "\hline":
                    table_list.append([region])
                    continue
                toPrint = [   
                              ["Region"     ,  fix_region_name( region )], 
                          ]
                for samp in samples:
                    #toPrint.append( [ samp , self.yieldDict[variations[1]][samp][region]  ] )
                    for var in variations:
                        toPrint.append( [ var , self.yieldDict[var][samp][region] ] )
                    toPrint.append(  ['%s Syst. '%samp , round (sample_systs[samp][region] ,4)      ] )

                    #toPrint.append( [ samp ,   round( sample_systs[samp][region] ,2 ) ] )
                #toPrint.append(  ['Syst. ' , round (self.tot_sys[region] ,2)      ] )
                align = "{:<20}"*len(toPrint)
                if first_row:
                    print align.format(*[x[0] for x in toPrint])
                    first_row = False
                    table_list.append( [x[0] for x in toPrint]  ) 
        
                print align.format(*[x[1] for x in toPrint])
                table_list.append( [x[1] for x in toPrint])
        makeDir(os.path.expandvars(bkg_systs_dir))
        #pickle.dump(res , open( os.path.expandvars( bkg_systs_dir+"/%s.pkl"%self.name)  ,"w"))
        table = makeSimpleLatexTable( table_list, "%s_YieldAndSystPerSample.tex"%self.name, cfg.saveDir+"/BkgSysts/", align_char = "c" ,  align_func= lambda char, table: "c|"+ ((char*(len(variations)+1) +"|") *(len(table[1])-1)).rstrip("|") )
        print table

        #
        #   Systematics per sample
        #

        first_row = True
        table_list = []
        for region in regions:
                if region == "\hline":
                    table_list.append([region])
                    continue
                toPrint = [   
                              ["Region"     ,  fix_region_name( region )], 
                          ]
                for samp in samples:
                    #toPrint.append( [ samp , self.yieldDict[variations[1]][samp][region]  ] )
                    toPrint.append( [ samp ,   round( sample_systs[samp][region] ,2 ) ] )
                #toPrint.append(  ['Syst. ' , round (self.tot_sys[region] ,2)      ] )
                align = "{:<20}"*len(toPrint)
                if first_row:
                    print align.format(*[x[0] for x in toPrint])
                    first_row = False
                    table_list.append( [x[0] for x in toPrint]  ) 
        
                print align.format(*[x[1] for x in toPrint])
                table_list.append( [x[1] for x in toPrint])
        makeDir(os.path.expandvars(bkg_systs_dir))
        #pickle.dump(res , open( os.path.expandvars( bkg_systs_dir+"/%s.pkl"%self.name)  ,"w"))
        table = makeSimpleLatexTable( table_list, "%s_SystPerSample.tex"%self.name, cfg.saveDir+"/BkgSysts/", align_char = "c" ,  align_func= lambda char, table: "c|"+ (char *(len(table[1])-1)).rstrip("|") )
        print table


        
        #
        #   Combined Systs Per Sample
        #

        if False:
    
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
            
            




if __name__ == "__main__":

    #jecSyst = Systematics(cfg, jecRunTagParams, centralParams, name="jec")
    #self = jecSyst
    systs = {}
    for syst_name, systTagParams in tagParams.iteritems():
       systs[syst_name] = Systematics(cfg, systTagParams, centralParams, name=syst_name) 
    self = systs[syst_name]
