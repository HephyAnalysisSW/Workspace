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

btag_wps= {
            #    "0.46" : { 'name': "CSVv2L" },
            #    "0.80"  : { 'name': "CSVv2M" },
            #    "0.935" : { 'name': "CSVv2T" },
            #  }
    "cMVAv2L" : {'discCut':'-0.715'     ,'discVar':'Jet_btagCMVA' }, 
    "cMVAv2M" : {'discCut':'0.185'      ,'discVar':'Jet_btagCMVA' }, 
    "cMVAv2T" : {'discCut':'0.875'      ,'discVar':'Jet_btagCMVA' }, 
    "CSVv2L"  : {'discCut':'0.460'      ,'discVar':'Jet_btagCSV'  }, 
    "CSVv2M"  : {'discCut':'0.80'       ,'discVar':'Jet_btagCSV'  }, 
    "CSVv2T"  : {'discCut':'0.935'      ,'discVar':'Jet_btagCSV'  }, 

       }

def getBTagMCTruthEfficiencies2D(c, cut="(1)", btag_wp_name = "CSVv2M"):
    from array import array
    mceff = {}
    c.SetEventList(0)
    if cut and cut.replace(" ","")!= "(1)":
        print "Setting Event List with cut: %s"%cut
        eListName = "eList_%s"%hashlib.md5("%s"%time.time()).hexdigest()
        print eListName
        print cut
        c.Draw(">>%s"%eListName,cut)
        c.SetEventList( getattr(ROOT,eListName))

    passed_hists = {}
    total_hists = {}
    ratios = {}

    #btag_var = "Jet_btagCSV"
    #btag_wp  = "0.80"
    if btag_wp_name not in btag_wps:
        raise Exception("BTag WP %s not recongnized in: %s"%(btag_wp_name, btag_wps))
    btag_var = btag_wps[btag_wp_name]['discVar']
    btag_wp  = btag_wps[btag_wp_name]['discCut']
    #btag_name = btag_wps[btag_wp]['name']



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
    #from Workspace.DegenerateStopAnalysis.tools.getSamples_8011 import getSamples 

    #btag_wp = "0.46"
    #btag_wp = "0.80"
    #btag_name = btag_wps[btag_wp]['name']

    btag_wp_name = "cMVAv2M"
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

    #from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_2016 import cmgTuplesPostProcessed
    #cmgPP         = cmgTuplesPostProcessed( mc_path, signal_path, data_path)
    #samples   =   getSamples(   cmgPP = cmgPP, sampleList = ['tt','w'] , useHT = True, skim='preIncLep', scan = True  )

    skimPresel        = '((met_pt>200)&&(Sum$(Jet_pt*(Jet_pt>20 && abs(Jet_eta)<2.4 && (Jet_id)) ) >200)) && ((Max$(Jet_pt*(abs(Jet_eta)<2.4 && Jet_id) ) > 90 ) >=1)'
    skimPreselBoosted = '((met_pt>200)&&(Sum$(Jet_pt*(Jet_pt>20 && abs(Jet_eta)<2.4 && (Jet_id)) ) >200)) && ((Max$(Jet_pt*(abs(Jet_eta)<2.4 && Jet_id) ) > 300 ) >=1)'
    jetCut1j   = "(Sum$(Jet_pt>20&&abs(Jet_eta)<2.4&&Jet_id))>=1"

    setups = {
                'boosted': {'tag': 'boosted', 'cut': skimPreselBoosted }, 
                'presel' : {'tag': 'presel',  'cut': skimPresel },
                '1j'     : {'tag': '1j'    ,  'cut': jetCut1j   },
             }

    setup = setups['presel']


    samples_dir = "/data/nrad/cmgTuples/8020_mAODv2_v0/RunIISpring16MiniAODv2/"
    samples_dir_8012 = "/data/nrad/cmgTuples/8012_mAODv2_v3/RunIISpring16MiniAODv2/"
    samples = {
                'TTJets': samples_dir + "/" +  "TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
                "WJets" : '',
                'T2ttold': samples_dir + "/" + "SMS-T2tt_dM-10to80_genHT-160_genMET-80_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/" ,
                'T2ttold_OldJetClean': samples_dir_8012 + "/" + "SMS-T2tt_dM-10to80_genHT-160_genMET-80_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/" ,
              }

    samples_to_use = [ 'T2ttold_OldJetClean']

    #for samp in ['tt','w' ]:
    for samp in samples_to_use:
        if "T2tt" in samp or "T2bw" in samp: 
            import glob
            tree = ROOT.TChain("tree")
            
            #signal_cmg_files = "/data/nrad/cmgTuples/8011_mAODv2_v1/RunIISpring16MiniAODv2/SMS-T2tt_dM-10to80_genHT-160_genMET-80_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/" 
            #signal_cmg_files = "/data/nrad/cmgTuples/8020_mAODv2_v0/RunIISpring16MiniAODv2/SMS-T2tt_dM-10to80_genHT-160_genMET-80_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/" 

            signal_cmg_files = samples[samp]

            for f in glob.glob(signal_cmg_files+"/*/tree.root"):
                tree.Add(f)

            jetcut        = setup['cut']
            tag           = setup['tag']
            dms = {
                        'allDM'  : "(1)",
                        #'lowDM'  : "(  (GenSusyMStop-GenSusyMNeutralino) < 31)",
                        #'midDM'  : "(( (GenSusyMStop-GenSusyMNeutralino) > 31) && (  (GenSusyMStop-GenSusyMNeutralino) < 61 ))",
                        #'highDM' : "(( (GenSusyMStop-GenSusyMNeutralino) > 61))",
                    }

            for dm, dm_cut in dms.iteritems():
                cut = ' && '.join([ dm_cut,  jetcut] )
                print 'using cut for signal : %s'%cut    

                res=  getBTagMCTruthEfficiencies2D( tree,
                    cut=cut,
                    btag_wp_name = btag_wp_name
                )
                print "Signal Efficiencies:", dm
                print res

                pickle.dump(res, \
                    #file(os.path.expandvars('$CMSSW_BASE/src/StopsDilepton/tools/data/btagEfficiencyData/TTJets_DiLepton_comb_2j_2l.pkl'), 'w')
                    file(os.path.expandvars('$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/data/btagEfficiencyData/%s_%s_%s_%s.pkl'%(samp, dm,tag,btag_wp_name) ), 'w')
                )
                print os.path.expandvars('$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/data/btagEfficiencyData/%s_%s_%s_%s.pkl'%(samp, dm,tag,btag_wp_name) )

        else:
            #tree = samples[samp]['tree']
            #sample_name = samples[samp]['name']
             
            import glob
            tree = ROOT.TChain("tree")
            cmg_files = samples[samp]
            sample_name = samp
            for f in glob.glob(cmg_files+"/*/tree.root"):
                tree.Add(f)

            


            tag = setup['tag']

            res=  getBTagMCTruthEfficiencies2D( tree,
                #cut="(Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id))>=1"
                cut=setup['cut'],
                btag_wp_name = btag_wp_name,
            )
            print "%s Efficiencies:"%sample_name
            print res

            pickle.dump(res, \
                #file(os.path.expandvars('$CMSSW_BASE/src/StopsDilepton/tools/data/btagEfficiencyData/TTJets_DiLepton_comb_2j_2l.pkl'), 'w')
                file(os.path.expandvars('$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/data/btagEfficiencyData/%s_2D_%s_%s.pkl'%(sample_name,tag, btag_wp_name)), 'w')
            )
            print os.path.expandvars('$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/data/btagEfficiencyData/%s_2D_%s_%s.pkl'%(sample_name,tag, btag_wp_name)) 
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

