
import Workspace.DegenerateStopAnalysis.tools.limitTools as limitTools
import Workspace.DegenerateStopAnalysis.tools.degTools as degTools
import Workspace.DegenerateStopAnalysis.tools.sysTools as sysTools
import Workspace.DegenerateStopAnalysis.tools.fakeEstimate as fakeEstimate
import Workspace.DegenerateStopAnalysis.samples.baselineSamplesInfo as sampleInfo




#   weight_tag_list     = cfg.weight_tag_list
#   weight_tag          = cfg.weight_tag

mstop_scale_threshold = 800
WTT_CRCORR = False



bkgSystTags   =  {
                      "WPt":
                            {
                                'nowpt'  :   [ 'wpt',''  ],
                            },
                     "TTIsr":
                            {
                                '1x'  :   [ 'isr_tt',''  ],
                            },
                      "PU":
                            {
                                'up'    :   [ 'pu','pu_up'   ],
                                'down'  :   [ 'pu','pu_down' ],
                            },
                      "BTag_l":\
                            {
                                'up'    :   [ 'sf','sf_l_up'    ],
                                'down'  :   [ 'sf','sf_l_down'  ],
                            },
                      "BTag_b":\
                            {
                                'up'    :   [ 'sf','sf_b_up'    ],
                                'down'  :   [ 'sf','sf_b_down'  ],
                            },
                      "JEC":\
                            {
                                'up'    :   [ 'jec','jec_up'   ],
                                'down'  :   [ 'jec','jec_down' ],
                            },
                      "JER":\
                            {
                                'up'    :   [ 'jer','jer_up'   ],
                                'down'  :   [ 'jer','jer_down' ],
                            },
                }

systTags = {}
systTags.update(bkgSystTags)


# sorted(syst.regions['sr_pt_regions_all'] , key = lambda x: syst.regions['sr_pt_regions'].index(x) if x in syst.regions['sr_pt_regions'] else syst.regions['sr_pt_regions'].index(x.replace('el','l') ))
#rs = sorted(syst.regions['sr_pt_regions_all'] , key = lambda x: syst.regions['sr_pt_regions'].index(x) if x in syst.regions['sr_pt_regions'] else syst.regions['sr_pt_regions'].index(x.replace('el','l') ))
#res = sysTools.plotResults(syst.variations_yld_sums['central']['lep'] , ['Others', 'Fakes', 'TTJets', 'WJets'] , data_tag='DataBlind'  , hist_colors = sysTools.h_colors , bin_order = rs )
#p = sysTools.drawNiceDataPlot( res['DataBlind'] , res['stack'], res['signal'] )

class Systematic():

    test_sig = "T2tt300_270"

    def __init__( self, cfg, args, syst_name , syst_type = "Bkg" , sig = test_sig, rerun=False):
        lep = 'lep'
        print '\n' + "***"*25
        print syst_name
        print '\n' + "***"*25



        syst_info  = systTags[syst_name]
        central_weights      = args.weights
        lumiWeight           = cfg.lumiWeight
        self.generalTag      = cfg.generalTag
        self.syst_type = syst_type

        self.cardnames={}
        self.cfws={}
        self.mlf_outputs={}


        cutName = cfg.cutInstList[0].name
        self.cutName = cutName
        systDir      = cfg.results_dir + "/" + cfg.baseCutSaveDir + "/Systematics_%s/"%cutName
        self.systDir = systDir
        self.resDir  = systDir.replace("Systematics","Results")
        degTools.makeDir( systDir )
        degTools.makeDir( self.resDir )

        self_pkl = systDir +"/%s.pkl"%syst_name
        # Try To reload self
        if False:
            pass
        else:
            variations_weights = {}
            for var_name, [cen_w , var_w ] in syst_info.items():
                if not cen_w in central_weights:
                    raise Exception("There central weight (%s) tag doesn't seem to be there! (%s)"%(cen_w, central_weights) )                
                variations_weights[var_name] = [ w for w in central_weights +[var_w] if w and w!=cen_w]
                assert sorted( variations_weights[var_name])  != sorted( central_weights ) , "Central weight list and variation weight list seem to be the same!"
            variations_weights['central']= central_weights
            variations = ['central'] + syst_info.keys()
            
            variations_weight_tags = degTools.dict_function( variations_weights  ,
                                                              lambda weight_list : sampleInfo.evalInputWeights( weight_list, lumiWeight)['weight_tag']) 
            print variations_weight_tags
            fake_estimate_output_file      = cfg.results_dir + "/" + cfg.baseCutSaveDir +"/fakeEstimateOutput_%s.pkl"%cutName
            yld_sum_file      = cfg.results_dir + "/" + cfg.baseCutSaveDir +"/yields_summary_%s.pkl"%cutName
            yld_pkl_file_lep   = cfg.yieldPkls[ cfg.cutInstList[0].fullName]
            saveDir            = cfg.saveDirs[cfg.cutInstList[0].fullName ]
            self.saveDir       = saveDir
            print 'got files'

            assert variations_weight_tags['central'] in yld_pkl_file_lep, 'The central yield pkl doenst seem to correspond to the central weight tag'

            print 0
            variations_yld_pkl_files = degTools.dict_function(  variations_weight_tags,
                                                           lambda weight_tag : yld_pkl_file_lep.replace( variations_weight_tags['central'], weight_tag) )
            print variations_yld_pkl_files
            variations_yld_pkls = degTools.dict_function( variations_yld_pkl_files ,
                                                          lambda f: pickle.load(file(f)) )
            variations_yld_sum_files = degTools.dict_function( variations_weight_tags,
                                                          lambda weight_tag : yld_sum_file.replace( variations_weight_tags['central'], weight_tag) )
            variations_yld_sums = degTools.dict_function( variations_yld_sum_files ,
                                                          lambda f: pickle.load(file(f)) )
            variations_fake_estimate_outputs  = degTools.dict_function( variations_weight_tags,
                                                          lambda weight_tag: pickle.load( file ( fake_estimate_output_file.replace( variations_weight_tags['central'] , weight_tag))))
            variations_fake_estimate_files    = degTools.dict_function( variations_weight_tags,
                                                          lambda weight_tag:   fake_estimate_output_file.replace( variations_weight_tags['central'] , weight_tag))
            
            print 'getting files' 
            self.variations_yld_sums = variations_yld_sums
            self.variations_yld_sum_files = variations_yld_sum_files
            self.variations_yld_pkl_files = variations_yld_pkl_files
            #self.variations_fake_estimate_outputs = variations_fake_estimate_outputs 
            #self.variations_fake_estimate_files = variations_fake_estimate_files
            print 'got files'
            
            yld_dicts   = degTools.dict_function( variations_yld_pkls       , lambda yld: yld.getNiceYieldDict() ) 
            yldsByBin   = degTools.dict_function( variations_yld_pkls       , lambda yld: yld.getByBins( yld.getNiceYieldDict()) ) 
            yldSums     = variations_yld_sums #= degTools.dict_function( variations_yld_sum_files, lambda f  : pickle.load(file(f)) )
            
            ylds_lep = variations_yld_pkls['central']
            self.central_yld_sum     = variations_yld_sums['central'][lep]

            sampleNames = ylds_lep.sampleNames
            bkgList  = ylds_lep.bkgList
            w        = [bkg for bkg in bkgList if 'w' in bkg]
            tt       = [bkg for bkg in bkgList if 'tt' in bkg]
            others   = [bkg for bkg in bkgList if bkg not in w+tt]
            sigs     = ylds_lep.sigList
            data     = ylds_lep.dataList

            dataName = sampleInfo.sampleName(data[0])
            self.dataName = dataName 
            
            #cardBkgList = ["WJets","TTJets","Fakes", "Others" ] 
            cardProcList   = yldSums['central']['lep'][yldSums['central']['lep'].keys()[0]].keys() 
            cardMCList     = [ p for p in cardProcList if p not in [dataName, "Total"] ]
            cardBkgList    = [ p for p in cardMCList if p.lower() not in ['signal'] + ylds_lep.sigList and not anyIn(['t2tt', 't2bw'], p.lower()) ] 
            sigList        = [ p for p in cardMCList if anyIn(['t2tt', 't2bw'], p.lower()) ] 
            niceSigList    = [sampleInfo.sampleName(s) for s in sigList]
            self.cardProcList = cardProcList 
            self.cardMCList   = cardMCList
            self.cardBkgList  = cardBkgList
            self.sigList      = sigList
            self.niceSigList  = niceSigList
            h_colors ={
                        "Total": ROOT.kBlack,
                        "WJets": ROOT.kGreen,
                        "Fakes": ROOT.kViolet,
                       "TTJets": ROOT.kAzure,
                       "Others": ROOT.kOrange,
                        sig    : ROOT.kRed,
                      }
                        
            drawEstimates = False
            if drawEstimates :
                hists       = { 
                              proc: degTools.makeHistoFromDict(yldSums['central']['lep']    , 
                                                               bin_order = card_regions     , 
                                                               name      = "Ylds_%s_%s"%(sname, proc) , 
                                                               func      = lambda x: x[proc] ) 
                                    for proc in cardProcList   
                              }
                canv = degTools.makeCanvasMultiPads( 'Estimates_%s'%syst_name, c1ww=800, c1wh=800, pads=[], padRatios=[2,1] )
                dOpt = ""
                stack = ROOT.THStack("stack_%s"%syst_name, "stack_%s"%syst_name)
                for proc in reversed(cardBkgList):
                    h = hists[proc]
                    if proc in h_colors:
                        h.SetMarkerColor( h_colors[proc] )
                        h.SetLineColor( h_colors[proc] )
                        h.SetFillColor( h_colors[proc] )
                    if proc in cardBkgList:
                        stack.Add(h)
                ratio = hists[ dataName ].Clone("ratio_%s"%(sname))
                ratio.Divide( hists["Total"] )
                
                hists['ratio']=ratio
                hists['stack']=stack 
                
                canv[1].cd()
                canv[1].SetLogy(1)
                stack.Draw("hist")
                hists[ dataName ].Draw("same")
                
                hists[sig].SetLineColor(ROOT.kRed)
                hists[sig].SetLineStyle(5)
                hists[sig].SetLineWidth(3)
                hists[sig].Draw("hist same")
                
                canv[2].cd()
                ratio.GetXaxis().SetLabelSize(0.1)
                ratio.GetYaxis().SetTitle("Data/MC")
                ratio.Draw()
                #degTools.saveCanvas( canv[0], dir = saveDir, name = "Estimates" )
                self.hists = hists
            
            regions = variations_fake_estimate_outputs['central']['regions']
            self.regions = regions             

            ##
            ## Actually Calculating Systematics         
            ##

            syst_dict = sysTools.getBkgSysts( {v:yldSums[v]['lep'] for v in variations} , variations , keys = yldSums['central']['lep'].keys() )
            self.syst_dict = syst_dict
            card_syst_dict_with_crs =  degTools.dict_function( syst_dict, lambda x: (1+x/100.)   )
            self.card_syst_dict_with_crs = card_syst_dict_with_crs
            pickle.dump( card_syst_dict_with_crs , file( systDir +"/%s_syst_with_crs.pkl"%syst_name ,"w")) 
            pickle.dump( syst_dict      , file( systDir +"/%s_syst_dict.pkl"%syst_name ,"w")) 
            pickle.dump( self           , file( systDir +"/%s.pkl"%syst_name , "w" ))

            self.canvs = {}


    def plotSysts(self):
        syst_hists = {}
        for rname in ['card_regions', 'sr_pt_regions', 'cr_regions', 'main_sr_cr_regions'] : #regions.items():
            rlist = regions[rname]
            syst_hists[rname]  = {
                                   proc: degTools.makeHistoFromDict( 
                                                           self.syst_dict , 
                                                           bin_order = rlist, 
                                                           name = "Syst_%s_%s_%s"%(self.syst_name, proc,rname), 
                                                           func = lambda x: x[proc] 
                                                                    )
                                   for proc in cardBkgList + ["Total" , sig]   
                                 }
        for rname , rsyst_hists in syst_hists.items():
            for p, h in rsyst_hists.items():
                h.SetMarkerColor( h_colors[p])
 
        canv2 = ROOT.TCanvas("%s_Systematics"%syst_name,"%s_Systematics"%syst_name,  800, 800)
        canv2.cd()
        for rname , rsyst_hists in syst_hists.items():
            dOpt = "e0p"
            for proc, h in rsyst_hists.items():
                h.Draw(dOpt)
                dOpt="e0p same"
                h.Setaximum(20)
                h.SetMinimum(-20)
            degTools.saveCanvas( canv2, dir = saveDir +"/BkgSysts/" , name = "%s_%s"%(syst_name, rname) )
        self.canvs['bkg']=canv2

    def makeCard( self , sig = test_sig , output_dir = "./",  output_tag = "testcardtag" , bins_order = [], cr_sr_map = None,  syst_dict = None, blind = True):
        """
            If blind=True will set Total MC values for obserations in SR and Data only for CR observations.
        """
        if not syst_dict:
            syst_dict = self.card_syst_dicts

        if not bins_order:
            bins_order = self.regions['card_regions']
 
        self.getAllSystDicts()
        card = makeSignalCard(
                            #yldByBin        =   self.variations_yld_sums['central']['lep'] ,
                            yldByBin        =   self.central_yld_sum,
                            bkgList         =   self.cardBkgList , 
                            sig             =   sig        , 
                            data            =   self.dataName   , 
                            card_syst_dicts =   syst_dict, #self.card_syst_dicts ,  
                            bins_order      =   bins_order ,
                            cr_sr_map       =   cr_sr_map , 
                            blind           =   blind, #self.cutName == 'bins_sum'   ,
                            output_dir      =   output_dir +"/" + output_tag +"/" ,
                            name            =   self.generalTag + "_" + self.cutName , 
                            post_fix        =   output_tag
                        )
        self.cardnames[output_tag]  = card['cardname']
        self.cfws[output_tag]  = card['cfw']


    def getMLFResults( self , cardname, bins , output_name , output_tag = "", rerun = False ) :
        #if not hasattr(self, 'cardname'):
        #    raise Exception( "You need to run the makeCard command first in order to create the card before running MLF" )
        res      = sysTools.MaxLikelihoodResult( cardname , bins= bins , output_name = output_name, plotDir = self.saveDir +"/%s"%output_tag, saveDir = self.resDir +"/%s"%output_tag , rerun = rerun )
        self.res = res

    def makeCardForSensitivity( self , sig=test_sig, output_dir = "./" ,  output_tag = "testcards" , bins_order = [] , cr_sr_map = None, rerun = False, split_bins = False):
        """
            if blinded_ylds not availble already:
                1a. creates a card with a test signal, with data in CR observation and MC total in SR observation
                1b. runs MLF and extract the post-fit predictions
             
            2. creates blinded_ylds by replacing the data component of the yields with have MC prediction (from 1b.) 
            3. creates a new card for a given signal point with the blinded_ylds 
        """



        if not hasattr( self, "card_syst_dicts_with_crs_%s"%output_tag ):
            self.getAllSystDicts()
            card_syst_dicts_with_crs = self.card_syst_dicts_with_crs
            card_syst_dicts = self.getCardSystFromCRSRMap( card_syst_dicts_with_crs, cr_sr_map )
            setattr( self, "card_syst_dicts_with_crs_%s"%output_tag, card_syst_dicts )

        card_syst_dicts = getattr( self, "card_syst_dicts_with_crs_%s"%output_tag )

        if not hasattr(self, 'blinded_ylds_%s'%output_tag ):
            print "Making a Card for the MaxLikelihoodFit "
            #self.makeCard(sig=sig, blind = True, bins_order = self.regions['card_regions_map'].keys() , syst_dict = cards_syst_dict) 
            self.makeCard( sig=sig, blind = True, output_dir = output_dir , output_tag = output_tag, bins_order = bins_order , cr_sr_map = cr_sr_map , syst_dict = card_syst_dicts ) 
            cardname = self.cardnames[output_tag]
            name="PostPre"
            mlf_output = "mlf_output_%s.pkl"%output_tag
            self.mlf_outputs[output_tag] = mlf_output

            print "mlf_output:", mlf_output
            if rerun or not os.path.isfile( mlf_output):
                rerunMLF = False #not os.path.isfile(  mlf_output  )
                if rerunMLF:
                    print "\n" + "***"*30 + "Running MLF  ... this will take few minutes " + "***"*30 + "\n"
                
                self.getMLFResults( cardname= cardname, output_name = mlf_output, bins = bins_order, output_tag = output_tag , rerun = rerunMLF ) 
            mlf_results = pickle.load(file(self.resDir +"/" +output_tag +"/" + mlf_output))
    
            post_fit_res = mlf_results['shapes_fit_b']

            blinded_ylds = {}
            #bins = self.regions['card_regions']
            bins = self.regions['final_regions']
            sr_bins = [b for b in bins if 'sr' in b ] 
            for b in post_fit_res:
                blinded_ylds[b] = deepcopy( syst.central_yld_sum[b] )
                #if b in sr_bins:
                blinded_ylds[b][self.dataName] = post_fit_res[b]['total'] # replace data by post_fit total
            setattr( self, "blinded_ylds_%s"%output_tag , blinded_ylds  )


        if not bins_order:
            bins_order = self.regions['final_regions']
        card = makeSignalCard(
                            #yldByBin        =   self.variations_yld_sums['central']['lep'] ,
                            yldByBin        =   getattr( self, "blinded_ylds_%s"%output_tag ),
                            bkgList         =   self.cardBkgList ,
                            sig             =   sig   ,
                            data            =   self.dataName   ,
                            card_syst_dicts =   card_syst_dicts ,
                            bins_order      =   bins_order , #self.regions['card_regions'] ,
                            cr_sr_map       =   cr_sr_map   ,
                            blind           =   False, #the data has been replaced by total, so we're already blinded 
                            output_dir      =   output_dir +"/" + output_tag +"/" ,
                            #output_dir      =   output_dir ,
                            name            =   self.generalTag + "_" + self.cutName ,
                            post_fix        =   "srblinded"
                        )
        self.blinded_card = card['cardname']
        self.blinded_cfw  = card['cfw']


        #
        if split_bins:
            bins = []
            for cr, srs in cr_sr_map.items():
                if sorted( srs )  == sorted(  bins_order ):  # this is same as the whole thing
                    continue
                relevant_crs = []
                for sr in srs:
                    relevant_crs.extend(  [cr_ for cr_, srs_ in cr_sr_map.items() if sr in srs_ ] )
                relevant_crs = sorted( list ( set( relevant_crs ) ))
                print srs, 
                bin_tag = cr.replace("cr","sr") 
                output_bin_dir      =   output_dir +"/" + output_tag + "_Bins/"+ bin_tag + "/" 
                degTools.makeDir( output_bin_dir ) 
                card = makeSignalCard(
                                    #yldByBin        =   self.variations_yld_sums['central']['lep'] ,
                                    yldByBin        =   getattr( self, "blinded_ylds_%s"%output_tag ),
                                    bkgList         =   self.cardBkgList ,
                                    sig             =   sig   ,
                                    data            =   self.dataName   ,
                                    card_syst_dicts =   card_syst_dicts ,
                                    bins_order      =   srs +  relevant_crs ,   #self.regions['card_regions'] ,
                                    cr_sr_map       =   cr_sr_map   ,
                                    blind           =   False, #the data has been replaced by total, so we're already blinded 
                                    output_dir      =   output_bin_dir ,  
                                    #output_dir      =   output_dir ,
                                    name            =   self.generalTag + "_" + self.cutName ,
                                    post_fix        =   "srblinded"
                                )
                

                 
    def calcAndPlotLimits(self, output_dir, card_basename, output_tag  , plot_dir , docalc = True, text = None):
        limit_dir     = "{output_dir}/limits/".format(output_dir=output_dir)
        limit_calc_command =  "../tools/calcLimit.py '{output_dir}/{card_basename}*.txt' {limit_dir}".format(output_dir=output_dir , limit_dir = limit_dir, card_basename = card_basename)
        print "cards written in: ", "{output_dir}/{card_basename}*.txt".format(output_dir=output_dir, card_basename = card_basename)
        print "to calculate limits run this script and do what it says!"
        print limit_calc_command
        if docalc:
            os.system( limit_calc_command + " --paral" )
       
        scale_rule = lambda mstop, mlsp: 1/100.0 if mstop <= mstop_scale_threshold else False  ## to rescale the r value since xsec was already scaled
        limits_pattern = limit_dir + "/*%s*.pkl"%card_basename #, scale_rule = scale_rule ) 
        print "\n Collecting Limits from: \n %s \n "%limits_pattern
        limits = limitTools.collect_results( limits_pattern , scale_rule = scale_rule ) 
        pickle.dump( limits, file( limit_dir +  "/%s_limits.pkl"%output_tag  , "w" ))
        limit_plots = limitTools.drawExclusionLimit( limits , plot_dir +"/Limits.png" , text = text)
        #off_plot    = limitTools.makeOfficialLimitPlot( limits, tag = output_tag, plot_dir+"/OfficialPlots/" )
        return limits, limit_plots 


    def makeAllCardsForSensitivity( self, sigList= None, output_base_dir = "./" , output_tag = "testcards", bins_order = [], cr_sr_map = None , split_bins = False):
        output_dir = "%s/%s/"%(output_base_dir, output_tag)
        degTools.makeDir( output_dir ) 
        if not bins_order:
            bins_order = self.regions['card_regions']
        if not sigList:
            sigList = self.niceSigList
        for sig in sigList:
            print '\n making card for %s \n'%sig 
            self.makeCardForSensitivity( sig , output_dir = output_base_dir , output_tag = output_tag, bins_order = bins_order, cr_sr_map = cr_sr_map , split_bins = split_bins)            

        card_basename = self.generalTag + "_" + self.cutName
        
        calc_limits = False

        if calc_limits: 
            limits, limit_plots = self.calcAndPlotLimits( output_dir, card_basename, output_tag +"*srblinded*", plot_dir=self.saveDir + "/" + output_tag, docalc = True, text = None)

        if split_bins:
            for cr in cr_sr_map:
                bin_tag = cr.replace("cr","sr")
                #if not  'tt' in bin_tag:
                #    continue
                output_bin_dir = "%s/%s/"%(output_base_dir, output_tag+"_Bins") + "/%s/"%bin_tag
                degTools.makeDir( output_bin_dir ) 
                plot_bin_dir   = self.saveDir + "/" + output_tag + "_Bins/" + bin_tag +"/"
                #output_bin_dir = output_dir + "/" + output_tag + "_Bins/"+ bin_tag + "/" 
                limits, limit_plots = self.calcAndPlotLimits( output_bin_dir , card_basename  , output_tag , plot_dir = plot_bin_dir , text = bin_tag )   


        #   limit_dir     = "{output_dir}/limits/".format(output_dir=output_dir)
        #   limit_calc_command =  "../tools/calcLimit.py '{output_dir}/{card_basename}*.txt' {limit_dir}".format(output_dir=output_dir , limit_dir = limit_dir, card_basename = card_basename)
        #   print "cards written in: ", "{output_dir}/{card_basename}*.txt".format(output_dir=output_dir, card_basename = card_basename)
        #   print "to calculate limits run this script and do what it says!"
        #   print limit_calc_command
        #   os.system( limit_calc_command + " --paral" )
       
        #   scale_rule = lambda mstop, mlsp: 1/100.0 if mstop <=250 else False  ## to rescale the r value since xsec was already scaled
        #   limits = limitTools.collect_results( limit_dir + "/*%s*.pkl"%card_basename , scale_rule = scale_rule ) 
        #   pickle.dump( limits, file( limit_dir +  "/%s_limits.pkl"%output_tag  , "w" ))

        #   limit_plots = limitTools.drawExclusionLimit( limits , syst.saveDir+"/%s/Limits.png"%output_tag )



        #card = makeCard( yldByBin  , bkgList, sig, data,  card_syst_dicts , bins_order , regions , blind = True, name = "test", post_fix="testcard"):
        #       #fakeEstimateOutput = fakeEstimate.fakeEstimate(cfg, args)
        #       #prompt_fake_yields = fakeEstimateOutput['prompt_fake_yields']
        #       
        #       #sample_list = prompt_fake_yields['lep']['vcr1a'].keys()
        #       self.getAllSystDicts(cfg)
        #       card_syst_dicts = self.card_syst_dicts
        #       avail_systs     = self.avail_systs
        #       sample_list = self.cardProcList 
        #       yldByBin    = self.variations_yld_sums['central']['lep']
        #       yieldDict   = { samp: { b: yldByBin[b][samp] for b in yldByBin.keys()}  for samp in sample_list}
        #       bkgList     = self.cardBkgList 

        #       
        #        
        #       from Workspace.DegenerateStopAnalysis.tools.CombineCard import CombinedCard
        #       #import Workspace.DegenerateStopAnalysis.tools.CombineCard 
        #       #reload (Workspace.DegenerateStopAnalysis.tools.CombineCard)
        #       #CombinedCard  =  Workspace.DegenerateStopAnalysis.tools.CombineCard.CombinedCard
        #       
        #       map_name_niceName  = {
        #                         'w'       :  'WJets'      ,
        #                         'tt'      :  'TTJets'   ,
        #                         'z'       :  'ZJetsInv' ,
        #                         'qcd'     :  'QCD'     ,
        #                         'dy'      :  'DYJetsM50',
        #                         'vv'      :  'Diboson'  ,
        #                         'st'      :   'ST'      ,
        #                         #'other'   :   'Other'      ,
        #                         }
        #       niceProcessNames = map_name_niceName
        #       sig = "T2tt300_270"
        #       bins_order = self.regions['card_regions']
        #       cfw        = CombinedCard( niceProcessNames = niceProcessNames  );
        #       cfw.addBins( bkgList , bins_order )

        #       #self.cutName == 'bins_sum':
        #       if blind:
        #           cfw.specifyObservations(           yieldDict , sampleInfo.sampleName(self.dataName), bins = [b for b in bins_order if  'cr' in b])
        #           cfw.specifyObservations(           yieldDict , "Total" , makeInt = lambda x: int(round(x.val)) , bins = [b for b in bins_order if  'sr' in b])
        #           
        #       else:
        #           cfw.specifyObservations(           yieldDict , sampleInfo.sampleName(self.dataName))
        #       cfw.specifyBackgroundExpectations( yieldDict , bkgList )
        #       cfw.specifySignalExpectations(     yieldDict , sig  )
        #       for cr in self.regions['cr_regions']:
        #           srs = self.regions['cr_sr_map'][cr]
        #           bkgProc = ["TTJets"] if "tt" in cr else ["WJets"]
        #           sname   = cr+"_corr"
        #           cfw.addUncertainty        ( sname ,"lnN")
        #           cfw.specifyFlatUncertainty( sname ,  2, bins=[cr], processes = bkgProc)
        #           cfw.specifyFlatUncertainty( sname ,  2, bins=srs , processes = bkgProc)

        #       for sname in avail_systs:
        #           cfw.specifyUncertaintiesFromDict(  card_syst_dicts ,  [sname] , bkgList, bins = bins_order)
    
        #       cfw.addStatisticalUncertainties(yieldDict= yieldDict)
        #       cardname =  "%s_%s_%s_testcard.txt"%(cfg.generalTag, self.cutName , sig) 
        #       cfw.writeToFile(cardname)
        #       self.cfw = cfw
        #       #os.system("sh runMLF.sh %s "%(cfg.generalTag) )

    def getAllSystDicts(self ):
        systDir = self.systDir
        card_syst_dict_temp = "_syst_with_crs"
        syst_dict_temp      = "_syst_dict"
        card_syst_dict_pkls = degTools.glob.glob(systDir+"/*%s.pkl"%card_syst_dict_temp ) 
        syst_dict_pkls      = degTools.glob.glob(systDir+"/*%s.pkl"%syst_dict_temp      )    
    
        avail_systs = []
        self.avail_systs = avail_systs
        for syst_file in card_syst_dict_pkls:
            filename = degTools.get_basename( syst_file )
            sname    = filename.replace( card_syst_dict_temp , "" ).replace( ".pkl", "" )
            avail_systs.append(sname)
        
        syst_dicts = {}
        card_syst_dicts_with_crs = {}

        for sname in avail_systs:
            syst_dicts[sname]      = pickle.load(file( systDir + "/%s%s.pkl"%(sname, syst_dict_temp     )))
            card_syst_dicts_with_crs[sname] = pickle.load(file( systDir + "/%s%s.pkl"%(sname, card_syst_dict_temp)))

                     
        pickle.dump( card_syst_dicts_with_crs , file( systDir + "/syst_dict_with_crs.pkl", "w") )
        pickle.dump( syst_dicts      , file( systDir +"/syst_dict.pkl",'w'          ) )
        #pickle.dump( card_syst_dicts , file( systDir +"/syst_dict_for_cards.pkl","w") )

        self.syst_dicts = syst_dicts
        #self.card_syst_dicts = card_syst_dicts
        self.card_syst_dicts_with_crs = card_syst_dicts_with_crs

    @staticmethod
    def getCRProc( cr ) :
        if 'sr' in cr:
            raise Exception("This looks like a  SR not a CR: %s"%cr)
        if degTools.anyIn(['cr2', 'cr1'], cr):
            return 'WJets'
        if 'rtt' in cr.lower():
            return 'TTJets'

    def getCardSystFromCRSRMap( self, card_systs_dict_with_crs , cr_sr_map ):
        card_syst_dicts = degTools.deepcopy(card_systs_dict_with_crs)
        for syst_name in card_syst_dicts.keys():
            for cr_region in cr_sr_map:
                #proc  =  self.regions['cr_bkg_map'][cr_region]
                proc   =  Systematic.getCRProc( cr_region ) 
                for sr_region in cr_sr_map[cr_region] + [cr_region]:
                    cr_syst = card_syst_dicts[syst_name][cr_region][proc]
                    before_syst = card_syst_dicts[syst_name][sr_region][proc]
                    #card_syst_dicts[syst_name][sr_region][proc] /= cr_syst if cr_syst else 1.
                    card_syst_dicts[syst_name][sr_region][proc] =  1+ (cr_syst - before_syst) #if cr_syst else before_syst
                    after_syst = card_syst_dicts[syst_name][sr_region][proc]
                    print syst_name, cr_region , sr_region, proc, cr_syst, before_syst, after_syst
        return card_syst_dicts
                #for proc in self.cardProcList:


def makeSignalCard( yldByBin  , bkgList, sig, data,  card_syst_dicts , bins_order , cr_sr_map , blind = True, output_dir = "./" , name = "test", post_fix="testcard"):
    ##
    from Workspace.DegenerateStopAnalysis.tools.CombineCard import CombinedCard
    avail_systs  = card_syst_dicts.keys()
    sample_list = bkgList + [sig] + [data] 
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
    
    cfw        = CombinedCard( niceProcessNames = niceProcessNames , maxUncNameWidth = 20 );
    cfw.addBins( bkgList , bins_order )

    if blind:
        cfw.specifyObservations(           yieldDict , sampleInfo.sampleName(data), bins = [b for b in bins_order if  'cr' in b])
        cfw.specifyObservations(           yieldDict , "Total" , makeInt = lambda x: int(round(x.val)) , bins = [b for b in bins_order if  'sr' in b])
        
    else:
        cfw.specifyObservations(           yieldDict , sampleInfo.sampleName(data))
    cfw.specifyBackgroundExpectations( yieldDict , bkgList )
    mstop, mlsp = degTools.getMasses( sig )
    scale = 1.0
    cfw.comment = "Signal: %s "%sig
    if mstop <= mstop_scale_threshold:
        scale        =   1/100.
        cfw.comment +=   " Scaled by %s"%scale
    cfw.specifySignalExpectations(  yieldDict , sig  , scale = scale)


    cr_regions = [r for r in bins_order if 'cr' in r]
    for cr in cr_regions:
        if not cr in bins_order:
            continue
        srs_ = cr_sr_map[cr]
        srs  = [sr for sr in srs_ if sr in bins_order ] 
        #bkgProc = ["TTJets"] if "rtt" in cr else ["WJets"]

        if WTT_CRCORR:
            bkgProcs = ["TTJets", "WJets"]
            sname   = cr+"_corr"
            cfw.addUncertainty        ( sname ,"lnN")
            cfw.specifyFlatUncertainty( sname ,  2, bins=[cr], processes = bkgProcs)
            cfw.specifyFlatUncertainty( sname ,  2, bins=srs , processes = bkgProcs)
        else:
            bkgProcs = ["TTJets", "WJets"]
            bkgProcShort = {"TTJets":"TT", "WJets":"W"}
            for bkgProc in bkgProcs:
                sname   = cr + bkgProcShort[bkgProc] +"_corr"
                cfw.addUncertainty        ( sname ,"lnN")
                cfw.specifyFlatUncertainty( sname ,  2, bins=[cr], processes = [bkgProc])
                cfw.specifyFlatUncertainty( sname ,  2, bins=srs , processes = [bkgProc])

    for sname in avail_systs:
        cfw.specifyUncertaintiesFromDict(  card_syst_dicts ,  [sname] , bkgList, bins = bins_order)

    cfw.addUncertainty        ( "lepEff"   ,"lnN")
    cfw.specifyFlatUncertainty( "lepEff"   , 1.05 , bins = [b for b in cfw.bins if "sr" in b] )# , processes =['signal','WJets','TTJets', 'Fakes','Others'] )
    cfw.addUncertainty        ( "lumi"   ,"lnN")
    cfw.specifyFlatUncertainty( "lumi"   , 1.026 , processes=['signal'] )
    cfw.addUncertainty        ( "sigSys"   ,"lnN")
    cfw.specifyFlatUncertainty( "sigSys"   , 1.15 , processes=['signal'] )

    cfw.addUncertainty        ( "fakeSys"   ,"lnN")
    cfw.specifyFlatUncertainty( "fakeSys"   , 1.50 , processes=['Fakes'] )

    cfw.addStatisticalUncertainties(yieldDict= yieldDict)
    cardname =  output_dir+"/"+ "%s_%s_%s.txt"%(name, sig, post_fix) 
    print "Card Written to: %s"%cardname
    cfw.writeToFile(cardname)
    #assert False
    return {'cardname': cardname , 'cfw':cfw}



if __name__ == "__main__":
    #systs_to_run = ['TTIsr', 'PU', 'BTag_l', 'BTag_b' ]
    #systs_to_run = ['WPt','TTIsr', 'PU', 'BTag_l', 'BTag_b' ]
    systs_types = {
                'BkgSig': ['BTag_l', 'BTag_b']    ,
                'Bkg'   : ['WPt', 'TTIsr', 'PU' ] ,
            #    'Sig'   : ['BTag_fs'] ,
            }
    systs = {}
    rerun = False
    for syst_type, systs_to_run in systs_types.items():
        for sname in systs_to_run:
            systDir      = cfg.results_dir + "/" + cfg.baseCutSaveDir + "/Systematics_%s/"%cfg.cutInstList[0].name
            syst_pkl     = systDir +"/%s.pkl"%sname
            readSyst     = False
            if not rerun and os.path.isfile( syst_pkl ):
                print "Reading syst for %s: %s"%(sname, syst_pkl)
                print "WARNING SKIPPINg SYST CUZ!" , sname
                #syst = pickle.load( file(syst_pkl) )
                readSyst = True
            else:
                print "WARNING SKIPPINg SYST CUZ!" , sname
                #syst = Systematic( cfg, args, sname, syst_type=syst_type , rerun =rerun)
            #systs[sname] = syst
            break
    #syst = systs[ systs_to_run[0] ]
    syst = Systematic( cfg, args, "WPt", "Bkg", True)

    
    tag  = "WTTCORR" if WTT_CRCORR else "WTTUNCORR"

    card_regions_options = syst.regions['card_regions_options']
    opts = ['old', 'LepPtVL' , 'CTLepPtVL', 'LepPTExt' ]
    opts = card_regions_options.keys()
    opts = ['VRTTMTCTLepPtVL']
    split_bins = False
    for opt in opts:
        card_regions = card_regions_options[opt]
        cr_sr_map    = syst.regions['card_regions_cr_sr_maps'][opt]
        syst.makeAllCardsForSensitivity( output_base_dir = syst.resDir  , output_tag = '%s_%s'%(tag, opt) , bins_order = card_regions , cr_sr_map = cr_sr_map , split_bins= split_bins )

    #syst.makeAllCardsForSensitivity( output_tag = 'cardstest_%s'%opt, bins_order = syst.regions['card_regions_map'].keys() )
    #old_bins = [ b for b in syst.regions['card_regions'] if 'vl' not in b ]
    #syst.makeAllCardsForSensitivity( output_tag = 'cardstest_oldbins', bins_order = old_bins)
    #extended_bins = [ b.replace("l","el") for b in old_bins]
    #syst.makeAllCardsForSensitivity( output_tag = 'cardstest_extendedbins', bins_order = extended_bins)
 
