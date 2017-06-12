
import Workspace.DegenerateStopAnalysis.tools.limitTools as limitTools
import Workspace.DegenerateStopAnalysis.tools.degTools as degTools
import Workspace.DegenerateStopAnalysis.tools.sysTools as sysTools
import Workspace.DegenerateStopAnalysis.tools.fakeEstimate as fakeEstimate
import Workspace.DegenerateStopAnalysis.samples.baselineSamplesInfo as sampleInfo
#from Workspace.DegenerateStopAnalysis.tools.CombineCard import CombinedCard
import Workspace.DegenerateStopAnalysis.tools.CombineCard as CombineCard

from   Workspace.DegenerateStopAnalysis.tools.regionsInfo import *

reload( sysTools )
reload( CombineCard )
CombinedCard = CombineCard.CombinedCard

ROOT.gROOT.ProcessLine(".L /afs/hephy.at/work/n/nrad/CMSSW/CMSSW_8_0_20/src/Workspace/DegenerateStopAnalysis/python/limits/MonoJetAnalysis/limits/LimitSmoothing.C+")
ROOT.gStyle.SetPaintTextFormat("0.3f")




#   weight_tag_list     = cfg.weight_tag_list
#   weight_tag          = cfg.weight_tag

#mstop_scale_threshold = 325
mstop_scale_threshold = 350
XSEC_SCALE = 100.

scale_rule = lambda mstop, mlsp: 1/XSEC_SCALE if mstop <= mstop_scale_threshold else False  ## to rescale the r value since xsec was already scaled

WTT_CRCORR = True


drawSystHists = True


#OPTS       = [ "MTLepPtVL2", "MTLepPtVL3",  "MTLepPtExt", "MTLepPtL","MTLepPtSum" , "MTLepPtVL" ] 
#OPTS       = [ "MTLepPtL","MTLepPtSum" , "MTLepPtVL" ]

#OPTS      = [ "MTCTLepPtVL2", "MTCTLepPtVL3", "MTCTLepPtExt", "MTCTLepPtL","MTCTLepPtSum" , "MTCTLepPtVL" ]
#OPTS      = [ "MTLepPtVL2"]#, "MTLepPtVL2" ]
#OPTS       = [ "MTLepPtVL2" ] 
#OPTS       = [ "MTLepPtVL2" ] 


cutName = cfg.cutInstList[0].name
if 'vrw' in cutName:
    OPTS       = [ "MTLepPtVL2" ] # "MTLepPtSum"]
else:
    #OPTS       = ["MTCTLepPtVL2", "MTCTLepPtSum", "MTLepPtVL2", "LepPtL", "CTLepPtL","MTCTLepPtL"  ]
    OPTS       = [  "MTCTLepPtVL2" , 'MTCTLepPtSum' ]#,  "MTCTLepPtSum" ]#, "MTCTLepPtSum" ] #, #"MTLepPtVL2", "LepPtL", "CTLepPtL","MTCTLepPtL"  ]
    #OPTS       = ["MTCTLepPtL", "CTLepPtL", "LepPtL", "MTLepPtL"] 
if 'vrw' in cutName:
    prefix = 'vw'
elif 'vrb' in cutName:
    prefix = 'vb'
else:
    prefix = ''

if prefix:
    drawSystHists = False

print cutName
print OPTS

SPLIT_BINS = False


rerunSysts  = False
rerunMLF    = False
doCalcLimit = True


if prefix:
    SPLIT_BINS = False
    doCalcLimit = False
#sigModelTags =['t2tt', 't2bw', 'c1c1h', 'c1n1h', 'n2n1h'] 
sigModelTags = degTools.sigModelTags 

from collections import OrderedDict
TEST_TAGS = OrderedDict([
                          [  "TESTING"        , False   ] ,    
                          [  "FIXTHIS"        , False   ] ,    
                          [  "FULLBLIND"      , False   ] ,    
                          [  "CRCORR"         ,  2      ] ,    
                          [  "LnU"            , False   ] , 
                          [  "GAUSTHRESH"     , 50      ] ,
                          [  "RATEPARAM"      , True    ] , 

                          [  "LEPSFSYSTFIX"   , True    ] , 
                          [  "OLDFAKESYS"     , False   ] , 
                          [  "OTHERSXSECCORR" , True    ] , 
                          [  "OLDWTTPTSYST"      , False    ] , 
            ])
for TAGKEY, TAGVAL in TEST_TAGS.items():
    exec( "%s=%s"%(TAGKEY, TAGVAL) )


fakeSystTag="old_FS" if OLDFAKESYS else ""

try:
    res_
except NameError:
    res_ = []



modelsInfoSystHist = deepcopy( degTools.modelsInfo ) 
for model in modelsInfoSystHist.keys():
    if "T2" in model:
        modelsInfoSystHist[model]['binning_dm'] = [23, 237.5, 812.5, 8, 5, 85 ]






bkgSystTags   =  {
                      "WPt":{
                               'variations': {
                                    'nowpt'  :   [ 'wpt',''  ],
                                             },
                                'processes': ['WJets', "Fakes", "SimpleFakes", "Total"],
                               },
                     "TTIsr":{
                                'variations':{
                                    '1x'  :   [ 'isr_tt',''  ],
                                             },
                                'processes': ['TTJets',  "Fakes", "Total"],
                               },
                      "PU":{
                                'variations':{
                                    'up'    :   [ 'pu','pu_up'   ],
                                    'down'  :   [ 'pu','pu_down' ],
                                          },
                                'processes': ['TTJets','WJets','Others',"Total"],
                               },
                      "BTag_l":{\
                                'variations':{
                                    'up'    :   [ 'sf','sf_l_up'    ],
                                    'down'  :   [ 'sf','sf_l_down'  ],
                                            },
                                'processes': ['TTJets','WJets','Others',"Total"],
                               },
                      "BTag_b":{\
                                'variations':{
                                    'up'    :   [ 'sf','sf_b_up'    ],
                                    'down'  :   [ 'sf','sf_b_down'  ],
                                             },
                                'processes': ['TTJets','WJets','Others',"Total"],
                               },
                      "JEC":{\
                                'variations':{
                                   'central':   [ 'jec_central','jec_central'   ],
                                    'up'    :   [ 'jec_central','jec_up'   ],
                                    'down'  :   [ 'jec_central','jec_down' ],
                                          },
                                'replace':{
                                              'DataBlind':'MC',
                                           'Yields_35855pbm1':'Yields_35700pbm1',
                                           },
                                'processes': ['TTJets','WJets','Others',"Total"],
                            },
                      "JER":{\
                                'variations':{
                                   'central':   [ 'jer_central','jer_central'   ],
                                    'up'    :   [ 'jer_central','jer_up'   ],
                                    'down'  :   [ 'jer_central','jer_down' ],
                                          },

                                'replace':{
                                              'DataBlind':'MC',
                                           'Yields_35855pbm1':'Yields_35700pbm1',
                                           },
                                'processes': ['TTJets','WJets','Others',"Total"],
                            },
                 "FakesNonUniv":{\
                                  'variations':{\
                                        'pkl': ["Fakes", "/afs/hephy.at/user/m/mzarucki/public/results2017/fakeRate/final/8025_mAODv2_v7/80X_postProcessing_v0/MR14/systematics/%s/fakeSystematics_MR14_NonUniv.pkl"%fakeSystTag],
                                               },
                                'processes': ["Fakes","Total"],
                               },
                 "FakesNonClosure": {\
                                  'variations':{\
                                        'pkl':    ["Fakes", "/afs/hephy.at/user/m/mzarucki/public/results2017/fakeRate/final/8025_mAODv2_v7/80X_postProcessing_v0/MR14/systematics/%s/fakeSystematics_MR14_NonClosure.pkl"%fakeSystTag],
                                               },
                                  'processes': ["Fakes", "Total"],
                               },
                 "WPol": {\
                                  'variations':{\
                                        #'pkl':    ["WJets", "/afs/hephy.at/user/m/mzarucki/public/results2017/Wpol/WpolSys_FLminusFR.pkl" ], 
                                        'pkl':    ["WJets", "Wpolsyst.pkl" ], 
                                               },
                                  'processes': ["WJets", "Total"],
                               },

                 "WTTPtShape": {\
                                  'variations':{\
                                        #'pkl':    ["WJets", "/afs/hephy.at/user/m/mzarucki/public/results2017/Wpol/WpolSys_FLminusFR.pkl" ], 
                                        'pkl':    [ "WJets", cfg.results_dir + "/" + cfg.cutInstList[0].baseCut.saveDir +"/Systematics_%s"%cfg.cutInstList[0].name +"/WTTPtShape_Systematics.pkl" ], 
                                               },
                                  'processes': ["WJets", "TTJets" , "Total"],
                               },

                }

systTags = {
                      "BTag_fs":{\
                                'variations':{
                                    'up'    :   [ 'sf','sf_fs_up'    ],
                                    'down'  :   [ 'sf','sf_fs_down'  ],
                                             },
                               },
                      "SigISR":{\
                                'variations':{
                                    'cent'     :   [ 'isr_sig','isr_sig'  ] , # To take half of the effect as uncert.
                                    'noisr'    :   [ 'isr_sig','noisrsig' ] ,
                                             },
                               },
                      "SigMET":{\
                                'variations':{
                                    'central' : [ 'genmet','genmet' ] ,
                                    'pfmet'   : [ 'genmet', '' ] ,
                                    'genmet'  : [ 'genmet', 'genmet']  , ## to take half of the effect as uncert
                                             },
                                'processes': [ ],
                               },
            }

systTags.update(bkgSystTags)



systTypes = {
            'BkgSig': ['BTag_l' , 'BTag_b' , 'JEC', 'JER'     ]  ,
            'Sig'   : ['BTag_fs', 'SigISR' , "SigMET"     ]  ,
            'Bkg'   : ['WPt'    , 'TTIsr' ,  'PU'  ,  "FakesNonUniv", "FakesNonClosure" , "WPol" , "WTTPtShape" ] ,
        }


# sorted(syst.regions['sr_pt_regions_all'] , key = lambda x: syst.regions['sr_pt_regions'].index(x) if x in syst.regions['sr_pt_regions'] else syst.regions['sr_pt_regions'].index(x.replace('el','l') ))
#rs = sorted(syst.regions['sr_pt_regions_all'] , key = lambda x: syst.regions['sr_pt_regions'].index(x) if x in syst.regions['sr_pt_regions'] else syst.regions['sr_pt_regions'].index(x.replace('el','l') ))
#res = sysTools.plotResults(syst.variations_yld_sums['central']['lep'] , ['Others', 'Fakes', 'TTJets', 'WJets'] , data_tag='DataBlind'  , hist_colors = sysTools.h_colors , bin_order = rs )
#p = sysTools.drawNiceDataPlot( res['DataBlind'] , res['stack'], res['signal'] )


def niceRegionName(r):
    ret = r.replace("sr","SR").replace("cr","CR").replace("vl","VL").replace("l","L").replace("v","V").replace("h","H").replace("m","M")
    return ret

class Systematic():

    test_sig = "T2tt_300_270"
    #test_sig = "C1N1H_140_110"
    #test_sig = "T2tt_500_470"

    def __init__( self, cfg, args, syst_name , syst_type = "Bkg" , test_sig = test_sig, rerun=False):
        lep = 'lep'
        print '\n' + "***"*25
        print syst_name
        print '\n' + "***"*25


        self.name = syst_name


        syst_info = systTags[syst_name]
        variations_info  = syst_info.get( 'variations', syst_info) 
        #variations_info  = systTags[syst_name]
        central_weights      = args.weights[:]
        lumiWeight           = cfg.lumiWeight
        self.generalTag      = cfg.generalTag
        self.syst_type = syst_type
        self.test_sig  = test_sig

        self.cardnames={}
        self.cfws={}
        self.mlf_outputs={}

        inputSystProcesses = syst_info.get( 'processes', [] )

        cutName = cfg.cutInstList[0].name
        self.cutName = cutName
        systDir      = cfg.results_dir + "/" + cfg.baseCutSaveDir + "/Systematics_%s/"%cutName
        self.systDir = systDir
        self.resDir  = systDir.replace("Systematics","Results")
        degTools.makeDir( systDir )
        degTools.makeDir( self.resDir )

        self_pkl = systDir +"/%s.pkl"%syst_name
        # Try To reload self
        print variations_info
        if variations_info.get("pkl"):
            bkg, pklFile = variations_info['pkl']
            systPkl    = pickle.load(file(pklFile))
            systPklBkg = bkg
            self.systPkl = systPkl
            self.systPklBkg = systPklBkg
        else:
            systPkl = None
            systPklBkg = None 

        variations_weights = {}
       

        centralGiven  = variations_info.has_key('central')
        default_central_weights = central_weights[:]
        if centralGiven:
            inputCentralTag = variations_info['central'][0]
            central_weights += [inputCentralTag]
        

        replace_keys    = syst_info.get("replace", {})
        def replaceFunc( path ):
            for k,v in replace_keys.items():
                path = path.replace(k,v)
            return path

        variations_weights['central'] = central_weights 
        variations = ['central'] 

        #print variations_weights

        #print variations_info
        print ' \n this ' , central_weights
        if not systPklBkg:
            for var_name, [cen_w , var_w ] in variations_info.items():
                if not cen_w in central_weights and cen_w not in cfg.cuts.options:
                    raise Exception("The central weight (%s) tag doesn't seem to be there! (%s)"%(cen_w, central_weights) )                
                if var_name == 'central':
                    continue
                if self.name.lower() != 'sigmet':
                    variations_weights[var_name] = [ w for w in central_weights + [var_w] if w and w!=cen_w ]
                else:
                    variations_weights[var_name] = [ w for w in central_weights if w and w!=cen_w] + [w for w in [var_w] if w]
                    
                variations += [var_name]
                if sorted( variations_weights[var_name])  == sorted( central_weights ): 
                    print "\n" + "****"*20
                    print "!! WARNING !!!"
                    print "Central weight list and variation weight list seem to be the same!"
                    print "This is OK if for example you want to consider 1/2 of the variation as the uncertainty!"
                    print "Hopefully that's what you intended!"
                    print variations_weights
                    print central_weights
                    print "****"*20 + "\n"
            #variations += [ x for x in variations_info.keys() if x != 'central'] 
        else:
            variations += [self.name] 

        self.variations = variations 
        #print variations
        print variations_weights
        variations_weight_tags = degTools.dict_function( variations_weights  ,
                                                          lambda weight_list : sampleInfo.evalInputWeights( weight_list, lumiWeight)['weight_tag']) 
        print variations_weight_tags
        fake_estimate_output_file      = cfg.results_dir + "/" + cfg.baseCutSaveDir +"/fakeEstimateOutput_%s.pkl"%cutName
        yld_sum_file      = cfg.results_dir + "/" + cfg.baseCutSaveDir +"/yields_summary_%s.pkl"%cutName
        #yld_pkl_file_lep   = replaceFunc( cfg.yieldPkls[ cfg.cutInstList[0].fullName] )
        yld_pkl_file_lep   =  cfg.yieldPkls[ cfg.cutInstList[0].fullName] 
        saveDir            = cfg.saveDirs[cfg.cutInstList[0].fullName ]
        self.saveDir       = saveDir
        print 'got files'

        default_central_weight_tags = sampleInfo.evalInputWeights( default_central_weights, lumiWeight)['weight_tag'] 

    
        if centralGiven:
            #new_yld_pkl_file_lep = yld_pkl_file_lep.replace(  sampleInfo.evalInputWeights( default_central_weights, lumiWeight)['weight_tag'], variations_weight_tags['central'] )
            new_yld_pkl_file_lep = yld_pkl_file_lep.replace(  default_central_weight_tags , variations_weight_tags['central'] )
            #print default_central_weights
            #print  sampleInfo.evalInputWeights( default_central_weights, lumiWeight)['weight_tag']
            #print (new_yld_pkl_file_lep , yld_pkl_file_lep )

            print "Central Option given...for central yields will use this \n %s \n instead of \n %s \n "%(new_yld_pkl_file_lep , yld_pkl_file_lep )
            yld_pkl_file_lep = new_yld_pkl_file_lep

        print 0
        print variations
        #print variations_weight_tags
        variations_yld_pkl_files = degTools.dict_function(  variations_weight_tags,
                                                       lambda weight_tag : replaceFunc( yld_pkl_file_lep.replace( variations_weight_tags['central'], weight_tag)) )
        print variations_yld_pkl_files
        variations_yld_pkls = degTools.dict_function( variations_yld_pkl_files ,
                                                      lambda f: pickle.load(file(f)) )
        variations_yld_sum_files = degTools.dict_function( variations_weight_tags,
                                                      #lambda weight_tag : yld_sum_file.replace( variations_weight_tags['central'], weight_tag) )
                                                      lambda weight_tag : replaceFunc( yld_sum_file.replace( default_central_weight_tags , weight_tag)) )

        variations_yld_sums = degTools.dict_function( variations_yld_sum_files ,
                                                      lambda f: pickle.load(file(f)) )
        #variations_fake_estimate_outputs  = degTools.dict_function( variations_weight_tags,
        #                                              lambda weight_tag: pickle.load( file ( fake_estimate_output_file.replace( variations_weight_tags['central'] , weight_tag))))
        #variations_fake_estimate_files    = degTools.dict_function( variations_weight_tags,
        #                                              lambda weight_tag:   fake_estimate_output_file.replace( variations_weight_tags['central'] , weight_tag))

        #assert variations_weight_tags['central'] in yld_pkl_file_lep, 'The central yield pkl doenst seem to correspond to the central weight tag'
        assert variations_weight_tags['central'] in variations_yld_pkl_files['central'], \
                'The central yield pkl doenst seem to correspond to the central weight tag %s, %s'%(variations_weight_tags['central'], variations_yld_pkl_files['central'])
         
        print 'getting files' 
        self.variations_yld_sums = variations_yld_sums
        self.variations_yld_sum_files = variations_yld_sum_files
        self.variations_yld_pkl_files = variations_yld_pkl_files
        #self.variations_fake_estimate_outputs = variations_fake_estimate_outputs 
        #self.variations_fake_estimate_files = variations_fake_estimate_files
        print 'got files'
        
        #yld_dicts   = degTools.dict_function( variations_yld_pkls       , lambda yld: yld.getNiceYieldDict() ) 
        #yldsByBin   = degTools.dict_function( variations_yld_pkls       , lambda yld: yld.getByBins( yld.getNiceYieldDict()) ) 
        yldSums     = variations_yld_sums #= degTools.dict_function( variations_yld_sum_files, lambda f  : pickle.load(file(f)) )
        
        ylds_lep = variations_yld_pkls['central']
        self.central_yld_sum     = variations_yld_sums['central'][lep]

        sampleNames = ylds_lep.sampleNames
        bkgList  = ylds_lep.bkgList
        w        = [bkg for bkg in bkgList if 'w' in bkg      ]
        tt       = [bkg for bkg in bkgList if 'tt' in bkg     ]
        others   = [bkg for bkg in bkgList if bkg not in w+tt ]
        sigs     = ylds_lep.sigList
        data     = ylds_lep.dataList

        print data
        dataName = sampleInfo.sampleName(data[0]) if data else ""
        self.dataName = dataName 
      
        #cardBkgList = ["WJets","TTJets","Fakes", "Others" ] 
        cardProcList   = yldSums['central']['lep'][yldSums['central']['lep'].keys()[0]].keys() 
        cardMCList     = [ p for p in cardProcList if p not in [dataName, "Total"] ]
        cardBkgList    = [ p for p in cardMCList if p.lower() not in ['signal'] + ylds_lep.sigList and not anyIn( sigModelTags, p.lower()) and not p.startswith("_") and not p.startswith("Simple") ] 
        sigList        = [ p for p in cardMCList if anyIn( sigModelTags , p.lower()) ] 
        niceSigList    = [sampleInfo.sampleName(s) for s in sigList]
        self.cardProcList = cardProcList 
        self.cardMCList   = cardMCList
        self.cardBkgList  = cardBkgList
        self.sigList      = sigList
        self.niceSigList  = niceSigList

        isBkgSyst = False
        isSigSyst = False
        if syst_type.lower() == "bkg":
            systProcesses = inputSystProcesses if inputSystProcesses else self.cardBkgList +["Total"] 
            isBkgSyst = True
        elif syst_type.lower() == "sig":
            systProcesses = [] # sigSysts will be calculated and smoothed with histograms
            isSigSyst = True
        elif syst_type.lower() in [ "both", 'bkgsig', 'sigbkg' ] :
            #systProcesses = self.niceSigList + self.cardBkgList +["Total"]
            systProcesses  = inputSystProcesses if inputSystProcesses else self.cardBkgList +["Total"]#self.niceSigList + self.cardBkgList +["Total"]
            #systProcesses += self.niceSigList  # sigSysts will be calculated and smoothed with histograms 
            isSigSyst = True
            isBkgSyst = True
        else:
            raise Exception("Syst Type Not Recognized! Bkg, Sig or Both? %s"%syst_type)
        
         

        print "Will Evaluate Systematic for", systProcesses
        self.systProcesses = systProcesses
    
        all_regions   =  ylds_lep.cutNames #variations_fake_estimate_outputs['central']['regions_info'].all_regions
        regions_info  =  RegionsInfo( all_regions )
        self.regions_info = regions_info             

        if systPklBkg:
            flavs = ["lep"]
            variation_ylds = {flav:{} for flav in flavs}
            processes = ["Fakes","TTJets","WJets","Others" ] 
            missing_regions = [] 
            for flav in flavs:
                for b in yldSums['central'][flav]:        
                    variation_ylds[flav][b] = {}
                    print flav, b
                    for p in processes:
                        systVal = 1
                        #if p == systPklBkg:
                        if p in inputSystProcesses:
                            systBin = self.findBinFromSystPkl( b, systPkl)
                            if systBin:
                                if not type(systBin)==list:
                                    relSyst = systPkl[systBin][p]
                                    systVal = 1 + relSyst/100.
                                else:
                                    relSyst = sum( [ abs( systPkl[sb][p] ) for sb in systBin ]) / len(systBin)
                                    systVal  = 1+ relSyst/100.
                                    
                            else:
                                missing_regions.append( b )
                        variation_ylds[flav][b][p] = yldSums['central'][flav][b][p]*systVal

           
            for b in yldSums['central'][flav].keys():
                variation_ylds[flav][b]["Total"] = sum([ variation_ylds[flav][b][p] for p in self.cardBkgList ])


            regions_map = { r:self.regions_info.getCompRegions( r, self.regions_info.card_region_definition ) for r in variation_ylds[flav].keys() }
            for main_region, sub_regions in regions_map.iteritems(): 
                if main_region not in missing_regions:
                    print "this region is there already", main_region
                    continue 
                variation_ylds[flav][main_region] = degTools.dict_manipulator(
                                                        [ variation_ylds[flav][r] for r in sub_regions ] , func = lambda *args: sum(args) )
            print missing_regions
            #assert False 

 
            yldSums[self.name] = variation_ylds
            print variation_ylds[flav][b]
            print yldSums['central'][lep][b] 
            print 

        h_colors ={
                    "Total": ROOT.kBlack,
                    "WJets": ROOT.kGreen,
                    "Fakes": ROOT.kViolet,
                   "TTJets": ROOT.kAzure,
                   "Others": ROOT.kOrange,
                    test_sig    : ROOT.kRed,
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
        
        #regions_info = variations_fake_estimate_outputs['central']['regions_info']
        ##
        ## Actually Calculating Systematics         
        ##
        #if systPklBkg:
        #    return 
        #syst_dict = sysTools.getBkgSysts( {v:yldSums[v]['lep'] for v in variations} , variations , keys = yldSums['central']['lep'].keys() )
        #proxyProcesses = { "SimpleFakes":"Fakes" } 
        proxyProcesses = { } 
        syst_dict = sysTools.getSystsFromVariations( { v : yldSums[v]['lep'] for v in variations} , 
                                                      variations , bins = yldSums['central']['lep'].keys(), processes= self.systProcesses, niceNames = proxyProcesses )
        for b in syst_dict.keys():
            binSysts = syst_dict[b]
            if "Fakes" in binSysts and "SimpleFakes" in binSysts:
                fakeVariations = [ yldSums[v]['lep'][b]["Fakes"] for v in variations ]
                simpleFakeVariations = [ yldSums[v]['lep'][b]["SimpleFakes"]  for v in variations ]  

                if  fakeVariations == simpleFakeVariations:
                    pass
                else:
                    fakeTypes = [ x.__class__ for x in fakeVariations  ]
                    fakeTypesTest =  set( fakeTypes ) 
            
                    if not len( fakeTypesTest ) == 1 :
                        # one variation was calculated with combine one with simple subtraction! 
                        # calc systematics as the difference of the simple subtraction variation normalized to central value 
                        #binSysts["Fakes"] = binSysts["SimpleFakes"]
                        #print "========> Took Systematics from SimpleFakes as opposed to Fakes from MLF"
                        centralFakesVal          = yldSums['central']['lep'][b]['Fakes']
                        variationsSimpleFakesVal = [ yldSums[v]['lep'][b]['SimpleFakes'] for v in variations  ]
                        variationsSyst =[]
                        for varVal in variationsSimpleFakesVal[1:]:
                            varSyst = (varVal - variationsSimpleFakesVal[0] ) / centralFakesVal.val if centralFakesVal.val else 0.0
                            variationsSyst.append( varSyst )
                        systVal = round( sysTools.mean( variationsSyst ).val,4) * 100 
                        print "\n ----------------------------------------"
                        print b 
                        print fakeVariations, simpleFakeVariations 
                        print binSysts["Fakes"], binSysts["SimpleFakes"]
                        print systVal
                        print len( fakeTypesTest ) 
                        print "========> Took Systematics from SimpleFakes as opposed to Fakes from MLF"
                        syst_dict[b]['Fakes'] = systVal


        self.canvs = {}

        self.isSigSyst = isSigSyst
        self.isBkgSyst = isBkgSyst
        #main_srs = [''.join(x) for x in itertools.product( ['sr1','sr2'],['a','b','c'],['', 'X','Y'] )]
        if isSigSyst:
            #regions  = list(set(card_regions + main_srs ))
            #regions  = self.regions_info.getCardInfo( "MTCTLepPtSum" )['card_regions'] + self.regions_info.getCardInfo( "MTCTLepPtVL2" )['card_regions']
            #regions  = list(set(regions))  
            regions  = yldSums['central']['lep'].keys()
            c1 = ROOT.TCanvas("sigylds","sigylds", 1200,800) 

            variation_hists = {}
            for variation in self.variations[:]:
                variationName = self.name +"_" + variation
                sigYlds, sigYldHists = degTools.getSignalYieldMap( yldSums[variation]['lep'] , bins = regions,  make_hists=True , models_info=modelsInfoSystHist )
                for model in sigYldHists.keys():
                    degTools.set_dict_key_val( variation_hists, model , {} )
                    for b in sigYldHists[model].keys():
                        if drawSystHists:
                            h = sigYldHists[model][b].Draw("COLZ TEXT89E") 
                            saveCanvas( c1 ,  self.saveDir+"/Signals/%s/Yields/%s"%(model, variationName), "Yields_%s_%s"%(model, b) )
                        degTools.set_dict_key_val( variation_hists[model], b , {} )
                        degTools.set_dict_key_val( variation_hists[model][b], variation, sigYldHists[model][b] )
            self.variation_hists = variation_hists
            self.variation_syst_hists = {}
            self.variation_syst_vars  = {}
            syst_dict_smooth       = {b:{} for b in self.variation_hists[model].keys() }
            self.syst_dict_smooth = syst_dict_smooth
            for model in self.variation_hists:
                self.variation_syst_hists[model] = {}
                self.variation_syst_vars[model]  = {}
                for b in self.variation_hists[model].keys():
                    systh = sysTools.meanSysSignedHist( *[self.variation_hists[model][b][v] for v in variations])
                    if drawSystHists:
                        systh[0].Draw( "COLZ TEXT89" )
                        saveCanvas( c1 ,  self.saveDir+"/Signals/%s/Systs/%s"%(model, self.name), "Syst_%s_%s"%(model, b) )
                    smoothhist = ROOT.doSmooth(systh[0], 0 )
                    smoothhist.SetName( "Smooth_" + systh[0].GetName() )
                    if drawSystHists:
                        smoothhist.Draw( "COLZ TEXT89" )
                        saveCanvas( c1 ,  self.saveDir+"/Signals/%s/Systs/%s"%(model, self.name), "SystSmooth_%s_%s"%(model, b) )
                    self.variation_syst_hists[model][b] = ( smoothhist, systh )
                    smoothsyst_mass_dict = degTools.getTH2FbinContent(  smoothhist , legFunc = lambda x,y : (x,x-y) )
                    for m1, m2di in smoothsyst_mass_dict.items():
                        for m2, val in m2di.items():
                            label = "%s_%s_%s"%(model, m1, m2)
                            syst_dict_smooth[b][label] = round( val,4)
                    
                    # degTools.set_dict_key_val( variation_syst_hists[model][b], self.name, systh[0]  )
                    # degTools.set_dict_key_val( variation_syst_vars[model][b] , self.name, systh[1:] )
            #print "\n"*5
            #print syst_dict['sr1laX'].keys()
            #print syst_dict_smooth['sr1laX'].keys()
            #print "\n"*5
            for b in syst_dict.keys():
                syst_dict[b].update( syst_dict_smooth[b] )
            #print syst_dict['sr1laX'].keys()


        self.syst_dict = syst_dict
        card_syst_dict_with_crs  =  degTools.dict_function( syst_dict, lambda x: sysTools.convertRelSysForCard(x/100.)   )
        if False: # this is the wrong way!
            card_syst_dict_with_crs  =  degTools.dict_function( syst_dict, lambda x: (1+x/100.)   )
        self.card_syst_dict_with_crs = card_syst_dict_with_crs
        pickle.dump( card_syst_dict_with_crs , file( systDir +"/%s_syst_with_crs.pkl"%syst_name ,"w")) 
        pickle.dump( syst_dict      , file( systDir +"/%s_syst_dict.pkl"%syst_name ,"w")) 
        pickle.dump( self           , file( systDir +"/%s.pkl"%syst_name , "w" ))

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
            bins_order = self.regions_info.final_regions 
 
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


    def averagePFMetGenMET(self):
        print '\n\n' , 'AVERAGING GENMET WITH PFMET'
        if getattr(self, "PFMETGENMETAVERAGED", False):
            print "WARNING!!! yOU ALREADY AVERAGED GENMET AND PFMET!!! SO I WILL SKIPP THIS!!!!"
            return 
        genMETSystPkl = self.systDir + "/" + "SigMET.pkl"
        genmetsyst = pickle.load(file (genMETSystPkl))
        pfmetylds  = pickle.load(file( genmetsyst.variations_yld_sum_files['pfmet']  ))['lep']
        genmetylds = pickle.load(file( genmetsyst.variations_yld_sum_files['genmet'] ))['lep']
        old_yld_sum = deepcopy( self.central_yld_sum    )
        new_central = {}
        for b in self.central_yld_sum.keys():
            for s in self.central_yld_sum[b]:
                if not s in syst.sigList:
                    continue
                pfmet = pfmetylds[b][s]
                genmet = genmetylds[b][s]
                new_val = u_float(  (pfmet+genmet).val/2. , pfmet.sigma)
                self.central_yld_sum[b][s] = new_val

        self.PFMETGENMETAVERAGED=True
        return 
 

    def getMLFResults( self , cardname, bins , output_name , output_tag = "", sig_name = None, rerun = False ) :
        #if not hasattr(self, 'cardname'):
        #    raise Exception( "You need to run the makeCard command first in order to create the card before running MLF" )
        #m1, m2 = degTools.getMasses(sig_name)
        #sigScale = 1/scale_rule(m1,m2) if scale_rule(m1,m2) else False
        res      = sysTools.MaxLikelihoodResult( cardname , bins= bins , output_name = output_name, plotDir = self.saveDir +"/%s"%output_tag, saveDir = self.resDir +"/%s"%output_tag , rerun = rerun , sig_name = sig_name,) # sigScale = sigScale )  
        self.res = res
        res_.append( res )


    def makeCardForSensitivity( self , sig=test_sig, output_dir = "./" ,  output_tag = "testcards" , 
                                bins_order = [] , cr_sr_map = None, rerun = False, split_bins = False, blind_opt='sensitivity'):
        """
            if blinded_ylds not availble already:
                1a. creates a card with a test signal, with data in CR observation and MC total in SR observation
                1b. runs MLF and extract the post-fit predictions
             
            2. creates blinded_ylds by replacing the data component of the yields with have MC prediction (from 1b.) 
            3. creates a new card for a given signal point with the blinded_ylds 
        """

    
        ##
        ##  First need to run MLF to get post/prefit results
        ##

        if not hasattr( self, "card_syst_dicts_with_crs_%s"%output_tag ):
            self.getAllSystDicts( make_tables = rerunSysts)
            card_syst_dicts_with_crs = self.card_syst_dicts_with_crs
            card_syst_dicts, sr_syst_dicts = self.getCardSystFromCRSRMap( card_syst_dicts_with_crs, self.syst_dicts , cr_sr_map )
            setattr( self, "card_syst_dicts_with_crs_%s"%output_tag, card_syst_dicts )
            setattr( self, "syst_dicts_srs_%s"%output_tag, sr_syst_dicts )

        card_syst_dicts = getattr( self, "card_syst_dicts_with_crs_%s"%output_tag )

        blind_opts = {
                    #'sensitivity'   :  {'ylds_name': 'blinded_ylds_%s'%output_tag     ,'tag':'srblinded'  , 'blind': True  },
                    'unblind'       :  {'ylds_name': 'unblinded_ylds_%s'%output_tag         ,'tag':'unblinded'  , 'blind': False  },
                    'validation'    :  {'ylds_name': 'validation_ylds_%s'%output_tag  ,'tag':'validation' , 'blind': False }, 
                      }

        ylds_name = blind_opts[blind_opt]['ylds_name']  #'blinded_ylds_%s'%output_tag
        isBlinded = blind_opts[blind_opt]['blind']        
        blind_tag = blind_opts[blind_opt]['tag']



        if isBlinded:
            obsName = "PostFitMC"
        else:
            obsName = self.dataName

        if not hasattr(self, ylds_name ):
            print "Making a Card for the MaxLikelihoodFit "
            #self.makeCard(sig=sig, blind = True, bins_order = self.regions['card_regions_map'].keys() , syst_dict = cards_syst_dict) 
            self.makeCard( sig=self.test_sig, blind = isBlinded , output_dir = output_dir , output_tag = output_tag, bins_order = bins_order , cr_sr_map = cr_sr_map , syst_dict = card_syst_dicts ) 
            cardname = self.cardnames[output_tag]
            name="PostPre"
            mlf_output = "mlf_output_%s.pkl"%output_tag
            self.mlf_outputs[output_tag] = mlf_output

            print "mlf_output:", mlf_output
            if rerun or rerunMLF or not os.path.isfile( mlf_output):
                if rerunMLF:
                    print "\n" + "***"*30 + "Running MLF  ... this will take few minutes " + "***"*30 + "\n"
                
                self.getMLFResults( cardname= cardname, output_name = mlf_output, bins = bins_order, output_tag = output_tag , sig_name = self.test_sig, rerun = rerunMLF ) 

            mlf_results = pickle.load(file(self.resDir +"/" +output_tag +"/" + mlf_output))
    
            post_fit_res = mlf_results['shapes_fit_b']

            ylds = {}
            #bins = self.regions_info.final_regions
            #sr_bins = [b for b in bins if 'sr' in b ] 
            #if FULLBLIND:
            #    self.FULLBLIND = FULLBLIND
            #    sr_bins = bins 

            for b in post_fit_res:
                ylds[b] = deepcopy( syst.central_yld_sum[b] )
                #if b in sr_bins:
                if isBlinded:
                    ylds[b]["postFitMC"]   = post_fit_res[b]['total_background'] # replace data by post_fit mc total
                    ylds[b][self.dataName] = post_fit_res[b]['total_background'] # replace data by post_fit mc total
            setattr( self, ylds_name , ylds  )

            sr_bins = [b for b in bins_order if 'sr' in b ]
            cr_bins = [b for b in bins_order if 'cr' in b ]
            if True:
                fits = ['shapes_fit_b', 'shapes_prefit', 'shapes_fit_s']
                mlf_res = mlf_results
                bins    = bins_order #mlf_res[fits[0]]
                niceNames = {'total_background': 'Total MC', 'data':'Data', 'signal':self.test_sig} 
                for b in bins:
                    niceNames[b]= b.replace("sr","SR").replace("cr","CR")
            
                tables={}
                self.tables =tables 
                for srcr, bins in ( ("SR",sr_bins), ("CR",cr_bins) ):
                    for fit in fits:
                        table_name = fit+"_"+srcr+"_table"
                        print table_name
                        tables[ table_name ] = sysTools.makeTableFromMLFResults( mlf_res[fit] , bins = bins , niceNames = niceNames )
                        
                        tables[ table_name +"tx"]=makeSimpleLatexTable( tables[table_name], "%s_%sTable"%(fit,srcr), outDir=self.saveDir +"/%s/Tables/"%output_tag, 
                                              align_func = lambda ac, table: ( ac *( len(table[1])-2)).strip("|") +"||c||c"  )

                        ##
                        ## Table with SFs, Closure, etc
                        ##
                        npTable   = np.array( tables[table_name] )
                        tables['blah'] = npTable.T
                        print tables['blah']
                        data_vals  = npTable.T[-2][1:]
                        #data_vals  = np.concatenate( [data_vals[0:1] ,  map(u_float, data_vals[1:])] )
                        data_vals_with_stat = np.array( map( lambda x: u_float(x, math.sqrt(x) ) , data_vals ) )
                        data_vals  = map( u_float, data_vals ) #np.concatenate( [data_vals[0:1] ,  map(u_float, data_vals[1:])] )
                        tot_vals   =  npTable.T[-3][1:]
                        w_vals     = npTable.T[1][1:]
                        tt_vals    = npTable.T[2][1:]
                        fake_vals  = npTable.T[3][1:]
                        other_vals = npTable.T[4][1:]

                        print npTable.T
                        wtt_vals    = map( lambda x: x if x.val else u_float(1e-6), w_vals+tt_vals )
                        tot_vals    = map( lambda x: x if x.val else u_float(1e-6), tot_vals ) 
                        print type(wtt_vals), wtt_vals
                        print type(tot_vals), tot_vals
 
                        sf_vals          = ( data_vals_with_stat - other_vals - fake_vals) / ( wtt_vals )
                        print sf_vals
                        sf_vals          = map( lambda x: x.round(3) , sf_vals )
                        sf_row           = np.concatenate( [ ["SF"], sf_vals ] ) 
                        ratio_data_mc_row= np.concatenate( [ ["Data/MC"], data_vals_with_stat/tot_vals])
                        closure_vals     = map(lambda x: u_float(1) , tot_vals ) + ( (data_vals_with_stat-tot_vals) / map( lambda x: u_float( x.val) , tot_vals) ) # 1+ (data-mc)/mc.val
                        closure_vals     = map( lambda x: x.round(3) , closure_vals )
                        closure_row      = np.concatenate( [ ["Closure"], closure_vals ]  )
                        new_table = np.concatenate( [ npTable.T[:-1] , [sf_row] , [closure_row]] )

                        new_table_name = table_name + "_Closure"
                        tables[ new_table_name ] = new_table.T
                        tables[ new_table_name +"tx"]=makeSimpleLatexTable( tables[new_table_name], "%s_%sTable_Closure"%(fit,srcr), outDir=self.saveDir +"/%s/Tables/"%output_tag, 
                                              align_func = lambda ac, table: ( ac *( len(table[1])-3)).strip("|") +"|c|c|c"  )


        ##
        ## 
        ##

        sigModel = degTools.getSignalModel( sig )
        sigModelTitle = sampleInfo.sampleName( sigModel, "latexName")

        if not bins_order:
            bins_order = self.regions_info.final_regions
        output_sig_dir = output_dir +"/" + output_tag +"/" + sigModelTitle +"/"
        degTools.makeDir( output_sig_dir )
        card = makeSignalCard(
                            #yldByBin        =   self.variations_yld_sums['central']['lep'] ,
                            yldByBin        =   getattr( self, ylds_name ),
                            bkgList         =   self.cardBkgList ,
                            sig             =   sig   ,
                            data            =   self.dataName   ,
                            card_syst_dicts =   card_syst_dicts ,
                            bins_order      =   bins_order , #self.regions['card_regions'] ,
                            cr_sr_map       =   cr_sr_map   ,
                            blind           =   False, #the data has been replaced by total, so we're already blinded 
                            output_dir      =   output_sig_dir,
                            #output_dir      =   output_dir ,
                            name            =   self.generalTag + "_" + self.cutName ,
                            post_fix        =   blind_opt,
                        )

        getattr( self , ylds_name.replace("ylds","card") ,   card['cardname'] )
        getattr( self , ylds_name.replace("ylds","cfw")  ,   card['cfw']      )

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
                output_bin_dir      =   output_dir +"/" + output_tag + "_Bins/"+ sigModelTitle + "/" + bin_tag + "/" 
                degTools.makeDir( output_bin_dir ) 
                card = makeSignalCard(
                                    #yldByBin        =   self.variations_yld_sums['central']['lep'] ,
                                    yldByBin        =   getattr( self, ylds_name ),
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
                                    post_fix        =   blind_opt
                                )
                

                 
    def calcAndPlotLimits(self, output_dir, card_basename, output_tag  , plot_dir ,sigModelName="", docalc = True, text = None):
        limit_dir     = "{output_dir}/limits/".format(output_dir=output_dir)
        degTools.makeDir(limit_dir)
        limit_calc_command =  "../tools/calcLimit.py '{output_dir}/{card_basename}*.txt' {limit_dir}".format(output_dir=output_dir , limit_dir = limit_dir, card_basename = card_basename)
        print "cards written in: ", "{output_dir}/{card_basename}*.txt".format(output_dir=output_dir, card_basename = card_basename)
        print "to calculate limits run this script and do what it says!"
        paralOption = "--paral"
        #paralOption = "--batch"
        calc_limit_script_name = "tmp_calc_all_limits_%s.sh"%(sigModelName+output_tag)
        limit_calc_command +=  " "+ paralOption +"  --output_script=%s"%calc_limit_script_name
        print limit_calc_command
        print docalc
        if docalc:
            print "Calculating Limits!"
            print limit_calc_command
            os.system( limit_calc_command ) 
            print "Finished Calculating Limits"       

        limits_pattern = limit_dir + "/*%s*.pkl"%card_basename #, scale_rule = scale_rule ) 
        print "\n Collecting Limits from: \n %s \n "%limits_pattern
        limits = limitTools.collect_results( limits_pattern , scale_rule = scale_rule ) 
        pickle.dump( limits, file( limit_dir +  "/Limits_%s_%s.pkl"%(sigModelName, output_tag)  , "w" ))
    
        limit_plots = limitTools.drawExclusionLimit( limits , plot_dir +"/Limits.png" , bins=degTools.sigModelBinnings[sigModelName],  text = text)
        #off_plot    = limitTools.makeOfficialLimitPlot( limits, tag = output_tag, plot_dir+"/OfficialPlots/" )

        #limitTools.makeOfficialLimitPlot( input_pkl, "TAG", plotDir )
        return limits, limit_plots 


    def makeAllCardsForSensitivity( self, sigList= None, output_base_dir = "./" , output_tag = "testcards", bins_order = [], cr_sr_map = None , split_bins = False, blind_opt = 'sensitivity'):
        output_dir = "%s/%s/"%(output_base_dir, output_tag)
        degTools.makeDir( output_dir ) 
        if not bins_order:
            bins_order = self.regions_info.final_regions 
        if not sigList:
            sigList = self.niceSigList


        sigModels = list(set( [ degTools.getSignalModel(s_) for s_ in sigList ] ))
        sigModelLists = { sigModel:[s_ for s_ in sigList if sigModel in s_] for sigModel in sigModels}
        
        #sigModelLists.pop("T2bW")

        #sigModelLists = {'T2tt':[
        #                         #'T2tt_300_270', 'T2tt_600_550', 
        #                         'T2tt_500_490', 'T2tt_500_480','T2tt_500_470','T2tt_500_460', 'T2tt_500_450', 'T2tt_500_440', 'T2tt_500_430', 'T2tt_500_420', 
        #                         'T2tt_300_290', 'T2tt_300_280','T2tt_300_270','T2tt_300_260', 'T2tt_300_250', 'T2tt_300_240', 'T2tt_300_230', 'T2tt_300_220',
        #                         'T2tt_400_390', 'T2tt_400_380','T2tt_400_370','T2tt_400_360', 'T2tt_400_350', 'T2tt_400_340', 'T2tt_400_330', 'T2tt_400_320',
        #                        ] }

        for sigModel, sigModelList in sigModelLists.iteritems():
            sigsNotFound = [sig for sig in sigModelList if sig not in sigList ] 
            if sigsNotFound:
                sigModelList = [sig for sig in sigModelList if sig not in sigsNotFound]
                print "These signal points are not availabe in the yields, so they will be skipped! %s"%sigsNotFound
                if not sigModelList:
                    sigModelList = sigList
                print "instead these will be used: %s"%sigModelList
            print '\n making card for %s \n'% sigModel
            try:
                sigModelTitle = sampleInfo.sampleName( sigModel, 'latexName')
            except:
                sigModelTitle = ''
            for sig in sigModelList:
                self.makeCardForSensitivity( sig , output_dir = output_base_dir , output_tag = output_tag, bins_order = bins_order, cr_sr_map = cr_sr_map , split_bins = split_bins, blind_opt = blind_opt)            

            card_basename = self.generalTag + "_" + self.cutName
            
            calc_limits = doCalcLimit

            #if calc_limits: 
            limits, limit_plots = self.calcAndPlotLimits( "%s/%s/%s/"%(output_base_dir, output_tag, sigModelTitle ) , card_basename + "*%s*"%blind_opt, output_tag , plot_dir=self.saveDir + "/" + output_tag+"/"+sigModelTitle, sigModelName = sigModelTitle, docalc = doCalcLimit, text = "%s %s"%(sigModelTitle , output_tag) )

            if split_bins:
                for cr in cr_sr_map:
                    bin_tag = cr.replace("cr","sr")
                    #if not  'tt' in bin_tag:
                    #    continue
                    output_bin_dir = "%s/%s/%s/"%(output_base_dir, output_tag+"_Bins", sigModelTitle) + "/%s/"%bin_tag
                    degTools.makeDir( output_bin_dir )
                    plot_bin_dir   = self.saveDir + "/" + output_tag + "_Bins/" + sigModelTitle +"/"+ bin_tag +"/"
                    #output_bin_dir = output_dir + "/" + output_tag + "_Bins/"+ bin_tag + "/" 
                    limits, limit_plots = self.calcAndPlotLimits( output_bin_dir , card_basename  , output_tag , plot_dir = plot_bin_dir , sigModelName = sigModelTitle, text = bin_tag )   


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

    def findBinFromSystPkl( self , region, systPkl):
        region_types = self.regions_info.region_types
        r = region.replace( self.regions_info.prefix, "")
        ret = False
        if r in systPkl:
            ret =  r
        elif r.replace("X","").replace("Y","") in systPkl:
            ret =  r.replace("X","").replace("Y","") 
        elif r.replace("el","l") in systPkl:
            ret =  r.replace("el","l")
        for mtbin in ['a','b','c']:
            for b in systPkl.keys():
                nb = b.replace(mtbin, "")
                if nb==r.replace("el","l").replace("X","").replace("Y",""):
                    ret =  nb
                    break
        if not ret:
            if r +"X" in systPkl and r+"Y" in systPkl:
                ret = [ r+"Y" , r+"X" ]         
                return ret
        if not ret in systPkl:
            ret = False
        return ret

    def getAllSystDicts(self , make_tables = False):
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
        
        if make_tables:

            self.makeSystPlot()
            opts = [ "MTLepPtSum" , "MTLepPtVL2" , "MTCTLepPtVL2", 'MTCTLepPtSum' ]
            for opt in opts:
                if not opt in self.regions_info.card_region_definition_options.keys():
                    continue
                # make dict with relative syst between cr and sr
                sr_syst_dicts   = {}  #degTools.deepcopy(rel_syst_dicts)
                cr_sr_map = syst.regions_info.getCardInfo( opt )['card_cr_sr_map']
                for syst_name in self.syst_dicts.keys():
                    sr_syst_dicts[syst_name] = {}
                    for cr_region in cr_sr_map:
                        for sr_region in cr_sr_map[cr_region]:
                            sr_syst_dicts[syst_name][sr_region] = {}
                            #for proc in self.syst_dicts[syst_name][sr_region].keys():
                            for proc in self.systProcesses: #[self.syst_dicts[syst_name][sr_region].keys() ]:
                                if proc not in self.syst_dicts[syst_name][cr_region] or proc not in self.syst_dicts[syst_name][sr_region]:
                                    continue
                                cr_rel_syst = self.syst_dicts[syst_name][cr_region][proc]
                                sr_rel_syst = self.syst_dicts[syst_name][sr_region][proc]
                                final_syst  = cr_rel_syst - sr_rel_syst 
                                sr_syst_dicts[syst_name][sr_region][proc] = final_syst
                #for p in self.systProcesses:
                for p in self.cardBkgList + ["Total"]:
                    for transpose in [True, False]:
                        self.makeSystPlot( process    = p , card_region_opt = opt , transpose = transpose, prefix="_" ) 
                        self.makeSystPlot( syst_dicts = sr_syst_dicts , process = p , card_region_opt = opt , transpose = transpose, prefix="SR_" ) 


    def makeSystPlot( self , syst_dicts = None , process = "Total", niceValFunc = lambda x: abs(round(x,2)), niceNameFunc = niceRegionName, 
                             card_region_opt = "MTLepPtSum", transpose = False, prefix = ""):
        if not hasattr(self, "syst_dicts"):
            syst.getAllSystDicts()
        card_syst_dicts = self.syst_dicts if not syst_dicts else syst_dicts
        avail_systs  = card_syst_dicts.keys()
        print avail_systs
    
        bkgList = ["WJets","TTJets","Fakes","Others","Total"]
        bkgList = self.cardBkgList + ["Total"]
    
        cardInfo = syst.regions_info.getCardInfo( card_region_opt )
        card_cr_sr_map = cardInfo["card_cr_sr_map"]
        card_regions   = cardInfo["card_regions"]

        avail_regions = [region for region in card_regions if region in card_syst_dicts[avail_systs[0]] ] 
        table =  [ ["Systematic Effect"] + [ niceNameFunc( region ) for region in avail_regions ]  ] 
        p = process
        for sname in avail_systs: 
            #row = [ sname ] + [ niceValFunc( card_syst_dicts[sname][region][p] )  for region in avail_regions ]
            row = [ sname ] + [ niceValFunc( card_syst_dicts[sname][region].get(p, 0) )  for region in avail_regions ]
            table.append(row)
        npTable = np.array( table ) 
        if transpose: npTable = npTable.T
    
        makeSimpleLatexTable( npTable , "%s%s_%s_BkgSyst%s"%( prefix + "_" if prefix else "", card_region_opt, p, "_T" if transpose else ""), 
                                                  outDir=self.saveDir +"/Tables/",
                                                  align_func = lambda ac, table: ( ac *( len(table[1]))).strip("|")   )
        return table


    @staticmethod
    def getCRProc( cr ) :
        if 'sr' in cr:
            raise Exception("This looks like a  SR not a CR: %s"%cr)
        if degTools.anyIn(['cr2', 'cr1'], cr):
            return 'WJets'
        if 'rtt' in cr.lower():
            return 'TTJets'

    def getCardSystFromCRSRMap( self, card_systs_dict_with_crs , rel_syst_dicts , cr_sr_map):
        """
            Takes relative uncertainty between correlated CR and SR
        """
        card_syst_dicts = degTools.deepcopy(card_systs_dict_with_crs)
        sr_syst_dicts   = {}#degTools.deepcopy(rel_syst_dicts)

        for syst_name in card_syst_dicts.keys():
            sr_syst_dicts[syst_name] = {}
            for cr_region in cr_sr_map:
                proc   =  Systematic.getCRProc( cr_region ) 
                for sr_region in cr_sr_map[cr_region] + [cr_region]:
                    sr_syst_dicts[syst_name][sr_region] = {}

                    
                    for proc in card_syst_dicts[syst_name][cr_region].keys():
                        if "t2" in proc.lower(): continue
                        cr_syst = card_syst_dicts[syst_name][cr_region][proc]
                        before_syst = card_syst_dicts[syst_name][sr_region][proc]
                        cr_rel_syst = rel_syst_dicts[syst_name][cr_region][proc]
                        sr_rel_syst = rel_syst_dicts[syst_name][sr_region][proc]
                        final_syst  = cr_rel_syst - sr_rel_syst 
                        sr_syst_dicts[syst_name][sr_region][proc] = final_syst

                        if not RATEPARAM:    
                            eps_cr    = 1 - cr_syst if cr_syst >=1 else 1-(1/cr_syst)  ### cr_syst or sr_syst shouldnt be zero since negative correlation needs to be quoted as  1/(1+eps)! if its zero there is underlying problem!
                            eps_sr    = 1 - before_syst if before_syst >=1 else 1-(1/before_syst)  
                            delta_eps = eps_cr-eps_sr
                            new_syst  = 1+abs(delta_eps) if delta_eps >0 else 1/(1+abs(delta_eps)) 
                            card_syst_dicts[syst_name][sr_region][proc] = new_syst 
                    #else:
                    #    if not RATEPARAM:
                    #        card_syst_dicts[syst_name][sr_region][proc] =  1+ (cr_syst - before_syst) #if cr_syst else before_syst
                    #after_syst = card_syst_dicts[syst_name][sr_region][proc]
                    #print syst_name, cr_region , sr_region, proc, cr_syst, before_syst, after_syst
        return card_syst_dicts, sr_syst_dicts
                #for proc in self.cardProcList:


def makeSignalCard( yldByBin  , bkgList, sig, data,  card_syst_dicts , bins_order , cr_sr_map , blind = True, blindProcName="Total",  output_dir = "./" , name = "test", post_fix="testcard"):
    ##
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
    cfw.specifyFlatUncertainty( "lumi"      , 1.026 , processes=['signal'] )
    cfw.addUncertainty        ( "sigFastFull"   ,"lnN")
    cfw.specifyFlatUncertainty( "sigFastFull"   , 1.02 , processes=['signal'] )
    #cfw.addUncertainty        ( "sigSys"    ,"lnN")
    #cfw.specifyFlatUncertainty( "sigSys"    , 1.15 , processes=['signal'] )

    #cfw.addUncertainty        ( "fakeSys"   ,"lnN")
    #cfw.specifyFlatUncertainty( "fakeSys"   , 1.50 , processes=['Fakes'] )


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
    #systs_to_run = ['TTIsr', 'PU', 'BTag_l', 'BTag_b' ]
    #systs_to_run = ['WPt','TTIsr', 'PU', 'BTag_l', 'BTag_b' ]
    systs = {}

    #blind_opt = 'sensitivity'
    blind_opt = 'unblind'
    if 'vr' in cfg.cutInstList[0].name:
        blind_opt = 'validation'
    print blind_opt


    #syst = Systematic( cfg, args, "JEC", "Bkg", rerun= True)
    #syst = Systematic( cfg, args, "BTag_fs", "Sig", rerun= True)
    for syst_type, systs_to_run in systTypes.items():
        if prefix and syst_type.lower() == 'sig':
            continue
    #for syst_type, systs_to_run in []:
        for sname in systs_to_run:
            if prefix in ['vw','vb'] and sname in ['JEC', 'JER']:
                continue
            systDir      = cfg.results_dir + "/" + cfg.baseCutSaveDir + "/Systematics_%s/"%cfg.cutInstList[0].name
            syst_pkl     = systDir +"/%s.pkl"%sname
            readSyst     = False
            if not rerunSysts and os.path.isfile( syst_pkl ):
                print "Reading syst for %s: %s"%(sname, syst_pkl)
                readSyst = True
            else:
                syst = Systematic( cfg, args, sname, syst_type=syst_type , rerun =rerunSysts)
            #systs[sname] = syst
    #syst = Systematic( cfg, args, "BTag_l", "BkgSig", rerun= True)
    syst = Systematic( cfg, args, "PU", "Bkg", rerun= True)
    
    tag=""
    if TESTING: tag += "_TEST_"
    if FIXTHIS: tag += "_lnNFix_"
    if FULLBLIND: tag+= "_FULLBLIND_"
    #tag+="NOgmN"
    #tag+="GausLimitVal"
    #tag += "FixFixNegFakes2_"
    #tag += "GausLimitNum%s"%GAUSTHRESH
    #tag += "RATEPARAM" if RATEPARAM else ""
    #tag += "_LnU_" if LnU else ""
    #tag += "" if CRCORR == 2 else "CRCORR%s"%CRCORR
    #tag += "WTTCORR" if WTT_CRCORR else "WTTUNCORR"
    #tag += "_%s"%blind_opt.upper()
    #tag += "_ERRFIX" #before MC erros were added in quad because of mc_stack

    #tag = "19MayStatusUpdate"
    tag = "ANUpdate_v6_"
    tag += ""  if OLDFAKESYS   else "NewFakeSysts_"
    tag += "lepEff1perc_" if LEPSFSYSTFIX else ""
    tag += "OtherXSecSRCRsCorr_" if OTHERSXSECCORR else ""
    tag += "OLDWTTPtSyst_"  if OLDWTTPTSYST else ""

    if (not OLDFAKESYS) and LEPSFSYSTFIX and OTHERSXSECCORR and (not OLDWTTPTSYST):
        tag = "PreAppANv6_2_"  
    tag += "OLDWTTPtSyst_"  if OLDWTTPTSYST else ""

    print "\n" ,"**"*50 
    print tag 
    print "**"*50 , "\n"

    card_region_definition_options = syst.regions_info.card_region_definition_options
    opts = card_region_definition_options.keys() 
    #opts = ['LepPtVL' , 'LepPtSum', "LepPtL",'LepPtExt' ]
    #opts = ['LepPtVL' , 'LepPtSum', "LepPtL",'LepPtExt' ]
    #opts = [ 'LepPtL', 'LepPtSum', 'LepPtVL', 'LepPtExt' ] 
    #opts = [ 'LepPtL', 'LepPtSum', 'LepPtVL', 'LepPtExt' ] 
    pt_tags = ['VL','L',"Ext", 'Sum']
    #opts = [ 'MTCTLepPtVL',  'CTLepPtVL',   'MTLepPtVL',   'LepPtVL' ]
    pt_tag = pt_tags[3]
    opts = [ 'MTCTLepPt%s'%pt_tag,  'CTLepPt%s'%pt_tag,   'MTLepPt%s'%pt_tag,   'LepPt%s'%pt_tag ]
    opts = [ "MTCTLepPtVL" ]
    opts = OPTS
    #opts = ["MTCTLepPtVL2", "MTCTLepPtL", "MTCTLepPtSum"]
    split_bins = SPLIT_BINS

    if not prefix:
        syst.averagePFMetGenMET()

    for opt in opts:
        card_regions_info = syst.regions_info.getCardInfo( opt )
        card_regions = card_regions_info['card_regions']
        cr_sr_map    = card_regions_info['card_cr_sr_map'] 
        syst.makeAllCardsForSensitivity( output_base_dir = syst.resDir  , output_tag = '%s_%s'%(tag, opt) , bins_order = card_regions , 
                                         cr_sr_map = cr_sr_map , split_bins = split_bins , blind_opt = blind_opt )


    
    #syst.makeAllCardsForSensitivity( output_tag = 'cardstest_%s'%opt, bins_order = syst.regions['card_regions_map'].keys() )
    #old_bins = [ b for b in syst.regions['card_regions'] if 'vl' not in b ]
    #syst.makeAllCardsForSensitivity( output_tag = 'cardstest_oldbins', bins_order = old_bins)
    #extended_bins = [ b.replace("l","el") for b in old_bins]
    #syst.makeAllCardsForSensitivity( output_tag = 'cardstest_extendedbins', bins_order = extended_bins)




    #raise Exception("Did not find region %s in syst pickle %s"%( r, systPkl.keys() ) )



