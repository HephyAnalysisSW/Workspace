from Workspace.DegenerateStopAnalysis.cmgPostProcessing.btagEfficiency import *
import Workspace.DegenerateStopAnalysis.tools.degTools as degTools
import time, hashlib
import glob

from optparse import OptionParser
parser = OptionParser()
(options,args) = parser.parse_args()



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

# ICHEP WS
#       btag_wps= {
#           "cMVAv2L" : {'discCut':'-0.715'     ,'discVar':'Jet_btagCMVA' }, 
#           "cMVAv2M" : {'discCut':'0.185'      ,'discVar':'Jet_btagCMVA' }, 
#           "cMVAv2T" : {'discCut':'0.875'      ,'discVar':'Jet_btagCMVA' }, 
#           "CSVv2L"  : {'discCut':'0.460'      ,'discVar':'Jet_btagCSV'  }, 
#           "CSVv2M"  : {'discCut':'0.80'       ,'discVar':'Jet_btagCSV'  }, 
#           "CSVv2T"  : {'discCut':'0.935'      ,'discVar':'Jet_btagCSV'  }, 
#              }

#Moriond 17 WP
btag_wps= {
    "cMVAv2L" : {'discCut':"-0.5884"     ,'discVar':'Jet_btagCMVA' }, 
    "cMVAv2M" : {'discCut':"0.4432"      ,'discVar':'Jet_btagCMVA' }, 
    "cMVAv2T" : {'discCut':"0.9432"      ,'discVar':'Jet_btagCMVA' }, 
    "CSVv2L"  : {'discCut':"0.5426"      ,'discVar':'Jet_btagCSV'  }, 
    "CSVv2M"  : {'discCut':"0.8484"      ,'discVar':'Jet_btagCSV'  }, 
    "CSVv2T"  : {'discCut':"0.9535"      ,'discVar':'Jet_btagCSV'  }, 
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
    btag_wp_name = "CSVv2M"


    skimPresel        = '((met_pt>200)&&(Sum$(Jet_pt*(Jet_pt>30 && abs(Jet_eta)<2.4 && (Jet_id)) ) >200)) && ((Max$(Jet_pt*(abs(Jet_eta)<2.4 && Jet_id) ) > 90 ) >=1)'
    skimPreselBoosted = '((met_pt>200)&&(Sum$(Jet_pt*(Jet_pt>30 && abs(Jet_eta)<2.4 && (Jet_id)) ) >200)) && ((Max$(Jet_pt*(abs(Jet_eta)<2.4 && Jet_id) ) > 300 ) >=1)'
    jetCut1j   = "(Sum$(Jet_pt>20&&abs(Jet_eta)<2.4&&Jet_id))>=1"

    setups = {
                'boosted': {'tag': 'boosted', 'cut': skimPreselBoosted }, 
                'presel' : {'tag': 'presel',  'cut': skimPresel },
                '1j'     : {'tag': '1j'    ,  'cut': jetCut1j   },
             }

    setup = setups['presel']


    wjet_bins = [
                    


                ]

    cmgTag="8025_mAODv2_v7"
    sampleEra="RunIISummer16MiniAODv2"

    samples_dir = "/data/nrad/cmgTuples/%s/%s/"%(cmgTag, sampleEra)
    #samples_dir = "/data/nrad/cmgTuples/8020_mAODv2_v5/RunIISpring16MiniAODv2/"
    #samples_dir_8012 = "/data/nrad/cmgTuples/8012_mAODv2_v3/RunIISpring16MiniAODv2/"
    #samples = {
    #            'TTJets'             : [
    #                                     samples_dir + "/" +  "TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
    #                                     samples_dir + "/" +  "TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1", 
    #                                     samples_dir + "/" +  "TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
    #                                     samples_dir + "/" +  "TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
    #                                     samples_dir + "/" +  "TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1" ,
    #                                   ],
    #            "WJets"              : [
    #                                        #samples_dir + "/" + "WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
    #                                        samples_dir + "/" + "WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
    #                                        samples_dir + "/" + "WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
    #                                        samples_dir + "/" + "WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
    #                                        samples_dir + "/" + "WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
    #                                        samples_dir + "/" + "WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
    #                                        samples_dir + "/" + "WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
    #                                        samples_dir + "/" + "WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
    #                                        samples_dir + "/" + "WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
    #                                   ],
    #            'T2tt'               : [
    #                                     samples_dir + "/" + "SMS-T2tt_dM-10to80_genHT-160_genMET-80_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/" ,
    #                                   ],
    #            'T2tt_mWMin0p1'      : [
    #                                     samples_dir + "/" + "SMS-T2tt_dM-10to80_genHT-160_genMET-80_mWMin-0p1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/" , 
    #                                   ],
    #            'T2bW_mWMin0p1'      : [
    #                                     samples_dir + "/" + "SMS-T2bW_X05_dM-10to80_genHT-160_genMET-80_mWMin-0p1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/" ,
    #                                   ],
    #            'T2ttold_OldJetClean': [
    #                                     samples_dir_8012 + "/" + "SMS-T2tt_dM-10to80_genHT-160_genMET-80_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/" ,
    #                                   ],
    #          } 


    sample_patterns={
                     "TT_pow"     : samples_dir + "/" + "TT_*powheg*",
                     "TTJets_HT"  : samples_dir + "/" + "TTJets_HT*",
                     "WJets_HT"   : samples_dir + "/" + "WJetsToLNu_HT*",
                     "WJets_NLO"  : samples_dir + "/" + "WJetsToLNu_Tune*",
                     "ZJets_HT"   : samples_dir + "/" + "ZJetsToNuNu_HT*",

                     "T2bW_mWMin0p1"       : samples_dir + "/" + "SMS-T2bW_X05_dM-10to80_genHT-160_genMET-80_mWMin-0p1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8*", 
                     "T2tt_mWMin0p1"       : samples_dir + "/" + "SMS-T2tt_dM-10to80_genHT-160_genMET-80_mWMin-0p1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8*", 
                     "T2tt"                : samples_dir + "/" + "SMS-T2tt_dM-10to80_genHT-160_genMET-80_TuneCUETP8M1_13TeV-madgraphMLM-pythia8*", 
    
                    }

    samples = {}
    for sample, pattern in sample_patterns.items():
        directories = glob.glob( pattern)
        if not directories:
            print "No Directories found for:", sample, pattern
        samples[sample] = directories



    import Workspace.DegenerateStopAnalysis.samples.cmgTuples.RunIISpring16MiniAODv2_v5 as cmgTuples


    samples2 = {
                'WJets': [  cmgTuples.WJetsToLNu_HT100to200      ,   
                            cmgTuples.WJetsToLNu_HT100to200_ext  ,       
                            cmgTuples.WJetsToLNu_HT1200to2500    ,   
                            cmgTuples.WJetsToLNu_HT200to400      ,   
                            cmgTuples.WJetsToLNu_HT200to400_ext  ,       
                            cmgTuples.WJetsToLNu_HT2500toInf     ,   
                            cmgTuples.WJetsToLNu_HT400to600      , 
                            cmgTuples.WJetsToLNu_HT600to800      ,
                            cmgTuples.WJetsToLNu_HT800to1200     ,
                            cmgTuples.WJetsToLNu_HT800to1200_ext ,   
                        ], 
                 'TTJets':[
                            cmgTuples.TTJets_LO                   ,    
                            cmgTuples.TTJets_LO_HT1200to2500_ext  ,    
                            cmgTuples.TTJets_LO_HT2500toInf       ,         
                            cmgTuples.TTJets_LO_HT600to800_ext    ,        
                            cmgTuples.TTJets_LO_HT800to1200_ext   ,        
                          ],
                 'T2tt' :[
                           cmgTuples.SMS_T2tt_dM_10to80_genHT_160_genMET_80,
                         ],
                 'T2tt_mWMin0p1' :[
                           cmgTuples.SMS_T2tt_dM_10to80_genHT_160_genMET_80_mWMin_0p1,
                         ],
                 'T2bW_mWMin0p1' :[
                           cmgTuples.SMS_T2bW_X05_dM_10to80_genHT_160_genMET_80_mWMin_0p1,
                         ],
              }

    #samples_to_use = ['WJets']

    if args:
        samples_to_use = args
        for samp in samples_to_use:
            print samples[samp]
    else: 
        #samples_to_use = [ 'TT_pow' , 'TTJets_HT' , "WJets_HT", "WJets_NLO", "ZJets_HT" ]
        samples_to_use = samples.keys() 

    #for samp in ['tt','w' ]:

    output_dir =  os.path.expandvars('$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/data/btagEfficiencyData/%s/%s/'%(cmgTag, sampleEra ) )
    degTools.makeDir(output_dir)
    for samp in samples_to_use:

        #sample_name = samp
        #cmgTupleDicts = samples[samp]
        #chains = [cmgDict['getChain']() for cmgDict in cmgTupleDicts]
        #for cmgDict in cmgTupleDicts:
        #    cmgComp.

        tree = ROOT.TChain("tree")
        cmg_files_ = [ glob.glob( samp_dir + "/*/tree.root") for samp_dir in  samples[samp] ]
        cmg_files = [ f for ff in cmg_files_ for f in ff]
        sample_name = samp
        for f in cmg_files:
            tree.Add(f)
        #assert False


        if "T2tt" in samp or "T2bw" in samp: 
            import glob
            #tree = ROOT.TChain("tree")
            
            #signal_cmg_files = "/data/nrad/cmgTuples/8011_mAODv2_v1/RunIISpring16MiniAODv2/SMS-T2tt_dM-10to80_genHT-160_genMET-80_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/" 
            #signal_cmg_files = "/data/nrad/cmgTuples/8020_mAODv2_v0/RunIISpring16MiniAODv2/SMS-T2tt_dM-10to80_genHT-160_genMET-80_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/" 

            #signal_cmg_files = samples[samp]

            #for f in glob.glob(signal_cmg_files+"/*/tree.root"):
            #    tree.Add(f)

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
                    file(os.path.expandvars('$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/data/btagEfficiencyData/%s/%s/%s_%s_%s_%s.pkl'%(cmgTag, sampleEra, samp, dm,tag,btag_wp_name) ), 'w')
                )
                print os.path.expandvars('$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/data/btagEfficiencyData/%s/%s/%s_%s_%s_%s.pkl'%(cmgTag, sampleEra, samp, dm,tag,btag_wp_name) )

        else:
            #tree = samples[samp]['tree']
            #sample_name = samples[samp]['name']
             
            import glob
            #tree = ROOT.TChain("tree")
            #cmg_files = samples[samp]
            #sample_name = samp
            #for f in glob.glob(cmg_files+"/*/tree.root"):
            #    tree.Add(f)

            


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
                file(os.path.expandvars('$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/data/btagEfficiencyData/%s/%s/%s_2D_%s_%s.pkl'%(cmgTag, sampleEra, sample_name,tag, btag_wp_name)), 'w')
            )
            print os.path.expandvars('$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/data/btagEfficiencyData/%s/%s/%s_2D_%s_%s.pkl'%(cmgTag, sampleEra, sample_name,tag, btag_wp_name)) 
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

