from Workspace.DegenerateStopAnalysis.tools.CombineCard import CombinedCard
import Workspace.DegenerateStopAnalysis.tools.degTools as degTools
import re
import glob


makeLimitPlot = True


cutInstName       = cfg.cutInstList[0].fullName
ylds_file         = cfg.yieldPkls[cutInstName]

yld = pickle.load(file(ylds_file))


map_niceName_name  = {v:k for k,v in yld.sampleNames.items() if k in yld.bkgList}
map_name_latexName = {k:v for k,v in yld.sampleNames.items() if k in yld.bkgList}

bins_order = ['srBDT_app_LIP']


def makeCard(yld, sig, syst_dict):
    simpleBkgs = False
    map_name_niceName  = {
                        'w'       :  'WJets'      ,
                        'tt'       :  'TTJets'   ,
                        'z'       :  'ZJetsInv' ,
                        'qcd'       :  'QCD'     ,
                        'dy'       :  'DYJetsM50',
                        'vv'       :  'Diboson'  ,
                        'st'       :   'ST'      ,
                      }

    if simpleBkgs:
        bkgList =  ['w'   ]
        yld.yieldDictFull["Total"] = dict_operator(yld.yieldDictFull , keys=bkgList , func = yield_adder_func )
    else:
        #bkgList =  ['w','tt','qcd', 'z', 'dy', 'st','vv' ]
        bkgList =  yld.bkgList
        #map_name_niceName.update( yld.sampleNames )
        names = deepcopy(yld.sampleNames)
        names.update( map_name_niceName )
        map_name_niceName = names
    #cfw=CombinedCard(niceProcessNames = {bkg:yld.sampleNames[bkg] for bkg in yld.bkgList} ); 
    cfw=CombinedCard(niceProcessNames = {bkg:map_name_niceName[bkg] for bkg in yld.bkgList} );
    cfw.maxUncNameWidth=30
    cfw.addBins(bkgList , bins_order )

    cfw.specifyObservations( yld.yieldDictFull , obsProcess="Total")
    cfw.specifyBackgroundExpectations(yld.yieldDictFull, bkgList )
    cfw.specifySignalExpectations( yld.yieldDictFull, sig)

    simpleCard=True

    if simpleCard:
        cfw.addUncertainty        ( "SysLumi", "lnN" )
        cfw.specifyFlatUncertainty( "SysLumi", 1.062, processes=["signal"] )
        cfw.addUncertainty        ( "SysPU", "lnN" )
        cfw.specifyFlatUncertainty( "SysPU", 1.01, processes=["signal"] )
        cfw.addUncertainty        ( "SysES", "lnN" )
        cfw.specifyFlatUncertainty( "SysES", 1.04, processes=["signal"] )
        cfw.addUncertainty        ( "SysID", "lnN" )
        cfw.specifyFlatUncertainty( "SysID", 1.10, processes=["signal"] )
        cfw.addUncertainty        ( "SysISR", "lnN" )
        cfw.specifyFlatUncertainty( "SysISR", 1.06, processes=["signal"] )
        cfw.addStatisticalUncertainties(yieldDict=yld.yieldDictFull , processes=["signal"])

        cfw.addUncertainty        ( "SysBckg", "lnN" )
        cfw.specifyFlatUncertainty( "SysBckg", 1.20, processes= map_name_niceName.values())
    

    else:

        #cfw.specifyUncertaintiesFromDict( syst_dict, uncerts = ['PU', 'jer', 'jec',  'WPt', 'ttpt','BTag_b', 'BTag_l', 'WPol'] , processes=[yld.sampleNames[bkg] for bkg in y
        cfw.addUncertainty        ( "lepEff"   ,"lnN")
        cfw.specifyFlatUncertainty( "lepEff"   , 1.05 , bins = [b for b in cfw.bins if "sr" not in b]  )

        #cfw.specifyUncertaintiesFromDict( syst_dict, uncerts = ['PU', 'jer', 'jec', 'ISR', 'met', 'BTag_b', 'BTag_l', 'BTag_FS', "Q2" ] , processes=['signal'],prefix="SIG")

        cfw.addUncertainty        ( "cr1a_corr","lnN")
        cfw.specifyFlatUncertainty( "cr1a_corr",  2, bins=['cr1a','sr1la', 'sr1ma', 'sr1ha'], processes=['WJets'])
        cfw.addUncertainty        ( "cr1b_corr","lnN")
        cfw.specifyFlatUncertainty( "cr1b_corr",  2, bins=['cr1b','sr1lb', 'sr1mb', 'sr1hb'], processes=['WJets'])
        cfw.addUncertainty        ( "cr1c_corr","lnN")
        cfw.specifyFlatUncertainty( "cr1c_corr",  2, bins=['cr1c','sr1lc', 'sr1mc', 'sr1hc'], processes=['WJets'])
        cfw.addUncertainty        ( "cr2_corr","lnN")
        cfw.specifyFlatUncertainty( "cr2_corr",  2,  bins=['cr2' ,'sr2l' , 'sr2m' , 'sr2h'], processes=['WJets'])
        cfw.addUncertainty        ( "crtt_corr","lnN")
        cfw.specifyFlatUncertainty( "crtt_corr",  2, bins=[], processes=['TTJets'])

        uncorr_proc_systs =[ ['WJets'    ,   'WPtShape'     ],
                             ['TTJets'   ,   'ttPtShape'    ],
                             ['ZJetsInv' ,   'ZInvEst'      ],
                             ['QCD'      ,   'QCDEst'       ],
                             ['DYJetsM50',   'DYJetsM50XSec'],
                             ['Diboson'  ,   'DibosonXSec'  ],
                             [ 'ST'      ,   'STXSec'       ],
                           ]
        for proc, syst_name in uncorr_proc_systs:
            cfw.specifyUncertaintiesFromDict( syst_dict, uncerts = [syst_name] , processes=[proc])


        cfw.addStatisticalUncertainties(yieldDict=yld.yieldDictFull )

    return cfw




def getBDTTagFromFileName(ylds_file):

    filename = os.path.splitext(os.path.basename( ylds_file))[0]
    bdt_tag  = re.search("bdt\dp\d\d", filename )
    if bdt_tag:
        bdt_tag = bdt_tag.group()
        #bdt_tag = bdt_tag.replace("bdt","").replace(".pkl","")
        bdt_tag = bdt_tag
    return bdt_tag

orig_bdt_tag = getBDTTagFromFileName(ylds_file)

bdt_yld_template = ylds_file.replace(orig_bdt_tag, "{bdttag}")

avail_bdt_ylds =  glob.glob(bdt_yld_template.format(bdttag="*"))

#mva_card_dir = "./MVASimpleCards/"

mva_card_dir = cfg.results_dir + "/%s/"%cfg.cutInstList[0].baseCut.saveDir  + "/MVASimpleCards/" 
makeDir(mva_card_dir)

signals = {'t2ttold': 'T2ttOld' ,
           't2tt'   : 'T2tt'    ,
           't2bw'   : 'T2bW'    ,
          }

masspoint = "300_270"
sigtype   = "t2ttold"

sig       = sigtype + masspoint



for bdt_yld_file in avail_bdt_ylds:
    bdt_yld = pickle.load(file(bdt_yld_file))
    bdt_tag = getBDTTagFromFileName( bdt_yld_file )
    print bdt_tag, bdt_yld_file 
    
    cfw = makeCard(bdt_yld,  sig ,{})
    cfw.writeToFile("%s/SimpleMVACard_%s_%s.txt"%(mva_card_dir, sigtype+masspoint, bdt_tag) )



print """
to calc limits run:

comb
mkdir {mva_card_dir}/limits/
./calcLimit.py "{mva_card_dir}/*{sig}*.txt" {mva_card_dir}/limits/
""".format(mva_card_dir = mva_card_dir , sig=sig)



saveDir = cfg.saveDir + "/%s/"%cfg.cutInstList[0].baseCut.saveDir
if makeLimitPlot:
    limits_dir = mva_card_dir + "/limits/"
    limit_pkls = glob.glob( limits_dir +"/*.pkl")

    results = {}
    for limit_pkl in limit_pkls:
        bdt_tag = getBDTTagFromFileName( limit_pkl)
        res     = pickle.load(file(limit_pkl))
        results[bdt_tag] = res
    hist = degTools.makeHistoFromDict( results ,   func = lambda x: x['0.500'] , bin_order= sorted(results.keys())[-20:] )
    hist.SetLabelSize(0.03)
    c1=ROOT.TCanvas("c1","c1", 1000,800)

    hist.Draw()
    c1.SaveAs( saveDir +"/Limits_%s_BDTcuts.png"%(sigtype+masspoint))

    minbdt = min( results, key = lambda x: results[x]['0.500'] )
    print "Best BDT Cut: "
    print minbdt , results[minbdt]['0.500']

