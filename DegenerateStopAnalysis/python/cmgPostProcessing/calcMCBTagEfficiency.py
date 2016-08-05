from Workspace.DegenerateStopAnalysis.cmgPostProcessing.btagEfficiency import *
import time, hashlib
# get MC truth efficiencies for a specific sample
def getBTagMCTruthEfficiencies(c, cut="(1)"):
    mceff = {}
    c.SetEventList(0)
    if cut and cut.replace(" ","")!= "(1)":
        print "Setting Event List with cut: %s"%cut
        eListName = "eList_%s"%hashlib.md5("%s"%time.time()).hexdigest()
        c.Draw(">>%s"%eListName,cut,'goff')
        c.SetEventList( getattr(ROOT,eListName))
    for ptBin in ptBins:
        mceff[tuple(ptBin)] = {}
        for etaBin in etaBins:
            mceff[tuple(ptBin)][tuple(etaBin)] = {}
            etaCut = "abs(Jet_eta)>"+str(etaBin[0])+"&&abs(Jet_eta)<"+str(etaBin[1])
            ptCut = "abs(Jet_pt)>"+str(ptBin[0])
            if ptBin[1]>0:
                ptCut += "&&abs(Jet_pt)<"+str(ptBin[1])
            c.Draw("(Jet_btagCSV>0.80)>>hbQuark(100,-1,2)",cut+"&&Jet_id>0&&abs(Jet_hadronFlavour)==5&&                     "+etaCut+"&&"+ptCut)
            c.Draw("(Jet_btagCSV>0.80)>>hcQuark(100,-1,2)",cut+"&&Jet_id>0&&abs(Jet_hadronFlavour)==4&&                     "+etaCut+"&&"+ptCut)
            c.Draw("(Jet_btagCSV>0.80)>>hOther(100,-1,2)" ,cut+"&&Jet_id>0&&(abs(Jet_hadronFlavour) < 4  || abs(Jet_hadronFlavour) > 5)&&  "+etaCut+"&&"+ptCut)
            hbQuark = ROOT.gDirectory.Get("hbQuark")
            hcQuark = ROOT.gDirectory.Get("hcQuark")
            hOther = ROOT.gDirectory.Get("hOther")
            mceff[tuple(ptBin)][tuple(etaBin)]["b"]     = hbQuark.GetMean()
            mceff[tuple(ptBin)][tuple(etaBin)]["c"]     = hcQuark.GetMean()
            mceff[tuple(ptBin)][tuple(etaBin)]["other"] = hOther.GetMean()
            print "Eta",etaBin,etaCut,"Pt",ptBin,ptCut,"Found b/c/other", mceff[tuple(ptBin)][tuple(etaBin)]["b"], mceff[tuple(ptBin)][tuple(etaBin)]["c"], mceff[tuple(ptBin)][tuple(etaBin)]["other"]
            del hbQuark, hcQuark, hOther
    return mceff


def getBTagMCTruthEfficiencies2D(c, cut="(1)"):
    from array import array
    mceff = {}
    c.SetEventList(0)
    if cut and cut.replace(" ","")!= "(1)":
        print "Setting Event List with cut: %s"%cut
        eListName = "eList_%s"%hashlib.md5("%s"%time.time()).hexdigest()
        c.Draw(">>%s"%eListName,cut)
        c.SetEventList( getattr(ROOT,eListName))

    passed_hists = {}
    total_hists = {}
    ratios = {}

    btag_var = "Jet_btagCSV"
    btag_wp  = "0.80"
    jet_quality_cut = "Jet_id>0"
    
    flavor_cuts = {
                        'b':'abs(Jet_hadronFlavour)==5', 
                        'c':'abs(Jet_hadronFlavour)==4',      
                        'other':'(abs(Jet_hadronFlavour) < 4  || abs(Jet_hadronFlavour) > 5)', 
                   }
   
    flavors = flavor_cuts.keys()
 
    for flavor in flavors:
        passed_name = 'passed_%s'%flavor
        passed_hists[flavor] = ROOT.TH2D( passed_name, passed_name , len(ptBorders)-1, array('d',ptBorders), len(etaBorders)-1, array('d', etaBorders) )
        total_name = 'total_%s'%flavor
        total_hists[flavor] = ROOT.TH2D( total_name, total_name , len(ptBorders)-1, array('d',ptBorders), len(etaBorders)-1, array('d', etaBorders) )
        c.Draw("abs(Jet_eta):Jet_pt>>%s"%passed_name, ' && '.join("(%s)"%x for x in [cut,jet_quality_cut, flavor_cuts[flavor], '%s>%s'%(btag_var, btag_wp)]))
        #c.Draw("abs(Jet_eta):Jet_pt>>%s"%total_name, ' && '.join("(%s)"%x for x in [cut,jet_quality_cut, flavor_cuts[flavor], '%s<%s'%(btag_var, btag_wp)]))
        c.Draw("abs(Jet_eta):Jet_pt>>%s"%total_name, ' && '.join("(%s)"%x for x in [cut,jet_quality_cut, flavor_cuts[flavor] ]))
        ratios[flavor] = passed_hists[flavor].Clone("ratio_%s"%flavor)
        ratios[flavor].Divide( total_hists[flavor]) 


    for ipt, ptBin in enumerate( ptBins ,1):
        mceff[tuple(ptBin)]={}
        for jeta, etaBin in enumerate( etaBins ,1):
            mceff[tuple(ptBin)][tuple(etaBin)] = {}
            for flavor in flavors:
                mceff[tuple(ptBin)][tuple(etaBin)][flavor] = ratios[flavor].GetBinContent(ipt, jeta)

    #return passed_hists, total_hists, ratios
    return mceff



if __name__ == '__main__':

    import ROOT, pickle, os
    from Workspace.DegenerateStopAnalysis.tools.getSamples_8011 import getSamples 

    #sample_info    =  {
    #                                    "sampleList"   :    sampleList  ,
    #                                    "wtau"         :    False       ,
    #                                    "useHT"        :    True        ,
    #                                    "skim"         :    'preIncLep',
    #                                    "kill_low_qcd_ht":  False       ,
    #                                    "scan"         :    False        ,
    #                                    #"massPoints"   :    task_info['massPoints']  ,
    #                                    "getData"      :    task_info.get("data",False)    ,
    #                                    "weights"      :    task_weight.weights     ,
    #                                    "def_weights"  :    def_weights     ,
    #                                    "data_filters" :    ' && '.join(data_filters_list),
    #                                    'lumis':def_weights['lumis'],
    #                                  }

    mc_path     = '/afs/hephy.at/data/mzarucki01//cmgTuples/postProcessed_mAODv2/8011_mAODv2_v1/80X_postProcessing_v5/analysisHephy_13TeV_2016_v0/step1/RunIISpring16MiniAODv2_v1/'
    signal_path = '/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/8011_mAODv2_v1/80X_postProcessing_v5/analysisHephy_13TeV_2016_v0/step1/RunIISpring16MiniAODv2_v1/'
    data_path   = '/afs/hephy.at/data/mzarucki01//cmgTuples/postProcessed_mAODv2/8011_mAODv2_v1_1/80X_postProcessing_v5/analysisHephy_13TeV_2016_v0/step1/Data2016_v1_1/'

    from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_2016 import cmgTuplesPostProcessed
    cmgPP         = cmgTuplesPostProcessed( mc_path, signal_path, data_path)
    samples   =   getSamples(   cmgPP = cmgPP, sampleList = ['tt','w'] , useHT = True, skim='preIncLep', scan = True  )

    skimPresel = '((met_pt>200)&&(Sum$(Jet_pt*(Jet_pt>30 && abs(Jet_eta)<2.4 && (Jet_id)) ) >200)) && ((Max$(Jet_pt*(abs(Jet_eta)<2.4 && Jet_id) ) > 90 ) >=1)'
    jetCut1j   = "(Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id))>=1"

    setups = { 
                'presel' : {'tag': '_presel',  'cut': skimPresel },
                '1j'     : {'tag': '_1j'    ,  'cut': jetCut1j   },
             }

    setup = setups['presel']


    for samp in ['tt','w' ]:
    #for samp in ['sig']:
        if samp == 'sig': 
            import glob
            tree = ROOT.TChain("tree")
            
            signal_cmg_files = "/data/nrad/cmgTuples/8011_mAODv2_v1/RunIISpring16MiniAODv2/SMS-T2tt_dM-10to80_genHT-160_genMET-80_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/" 
            for f in glob.glob(signal_cmg_files+"/*/tree.root"):
                tree.Add(f)
            jetcut        = setup['cut']
            tag           = setup['tag']
            dms = {
                        'allDM'  : "(1)",
                        'lowDM'  : "(  (GenSusyMStop-GenSusyMNeutralino) < 31)",
                        'midDM'  : "(( (GenSusyMStop-GenSusyMNeutralino) > 31) && (  (GenSusyMStop-GenSusyMNeutralino) < 61 ))",
                        'highDM' : "(( (GenSusyMStop-GenSusyMNeutralino) > 61))",
                    }

            for dm, dm_cut in dms.iteritems():
                cut = ' && '.join([ dm_cut,  jetcut] )
                print 'using cut for signal : %s'%cut    

                res=  getBTagMCTruthEfficiencies2D( tree,
                    cut=cut
                )
                print "Signal Efficiencies:", dm
                print res

                pickle.dump(res, \
                    #file(os.path.expandvars('$CMSSW_BASE/src/StopsDilepton/tools/data/btagEfficiencyData/TTJets_DiLepton_comb_2j_2l.pkl'), 'w')
                    file(os.path.expandvars('$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/data/btagEfficiencyData/T2tt_%s_%s.pkl'%(dm,tag) ), 'w')
                )

        else:
            tree = samples[samp]['tree']
            sample_name = samples[samp]['name']
            tag = setup['tag']

            res=  getBTagMCTruthEfficiencies2D( tree,
                #cut="(Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id))>=1"
                cut=setup['cut']
            )
            print "%s Efficiencies:"%sample_name
            print res

            pickle.dump(res, \
                #file(os.path.expandvars('$CMSSW_BASE/src/StopsDilepton/tools/data/btagEfficiencyData/TTJets_DiLepton_comb_2j_2l.pkl'), 'w')
                file(os.path.expandvars('$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/data/btagEfficiencyData/%s_2D%s.pkl'%(sample_name,tag)), 'w')
            )
    #for samp in ['tt','w']:
    #    tree = samples[samp]['tree']
    #    sample_name = samples[samp]['name']
    #    res=  getBTagMCTruthEfficiencies( tree,
    #        cut="(Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id))>=1"
    #    )
    #    print "%s Efficiencies:"%sample_name
    #    print res

    #    pickle.dump(res, \
    #        #file(os.path.expandvars('$CMSSW_BASE/src/StopsDilepton/tools/data/btagEfficiencyData/TTJets_DiLepton_comb_2j_2l.pkl'), 'w')
    #        file(os.path.expandvars('$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/data/btagEfficiencyData/%s_1j.pkl'%sample_name), 'w')
    #    )

