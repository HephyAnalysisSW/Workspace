"""
To be used after having ran, BkgSysts/Systematics.py, results.py 

Run after running 




"""

import Workspace.DegenerateStopAnalysis.tools.limitTools as limitTools
from Workspace.DegenerateStopAnalysis.tools.degTools import makeDir , getMasses
from copy import deepcopy
import multiprocessing



prefix      = "SigWMassCorr_v2"
#postfix     = "13TeV_RunII2016_12p9fbm1"
postfix     = ""
#limit_pkl    = 
card_dir     = cfg.cardDirs[cfg.cardDirs.keys()[0]]+"/" + prefix
base_res_dir = os.path.expandvars("$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/results/2016/%s/%s/%s/"%(cfg.cmgTag, cfg.ppTag, cfg.runTag) )

makeDir(card_dir+"/Full")

syst_pkl     = base_res_dir +"/"  + "SystDictForCards.pkl"  
bkg_pred_pkl = base_res_dir + "/" + "BkgPredWithVars.pkl"
mc_yield_pkl = base_res_dir + "/" + "YieldDictWithVars.pkl"



systs       = pickle.load(file(syst_pkl))
bkg_pred    = pickle.load(file(bkg_pred_pkl))
mc_yields   = pickle.load(file(mc_yield_pkl))



sig_yields_dict        = mc_yields['PU_central']
sig_yields_dict_genmet = mc_yields['met_GenMET']       # 
sig_yields_dict_met    = mc_yields['met_MET']          # these three are (should be) with no pu 
sig_yields_dict_avemet = mc_yields['met_central']      # 

mc_yields_dict         = mc_yields['PU_central']
pred_yields_dict       = bkg_pred['PU_central']



sigList         = [x for x in sig_yields_dict.keys() if 'T2tt' in x and "FOM" not in x]
mc_bkg_list     = ['WJets','TTJets',  'DYJetsM50',  'Diboson', 'ST' ]
pred_bkg_list   = ['ZJetsInv', 'QCD' ] 

bins = mc_yields_dict[mc_bkg_list[0]].keys()

card_yields         = {}







fastfull_sfs={
            'el':{
                'SRL':  1.     ,
                'SRH':  1.     ,
                'SRV':  1.     ,
                'CR' :  1.     ,
              },
            'mu':{
                'SRL':  1.     ,
                'SRH':  1.     ,
                'SRV':  1.     ,
                'CR' :  1.     ,
              },
            }

applyGenWSignalCorr = True
if applyGenWSignalCorr:
    corrFactDir = base_res_dir.replace("_SF","_BTAG_mcMatch").replace("LepAll","LepGood").replace("lep","mu")  ## cor factors based on LepGood(no mcMatch for lepall) Mu( loose el selection in 74x) and NoPU noISR (not avail. in 74x)
    yldMCmatchPkl = cfg.yieldPkls['presel_BinsSummary'].replace("_SF","_SF_mcMatch").replace("LepAll","LepGood")
    yldMCmatch = pickle.load(file(yldMCmatchPkl)).getNiceYieldDict()
    genWMassCorrFacts  = pickle.load(file(corrFactDir+"/SignalCorrFactors.pkl"))
    
applyFastFullSF = False

raw_card_yields = {}
for sig in sigList:
    raw_card_yields[sig]={}
    card_yields[sig] = {} 
    print "-----------------------------------------------------", sig

    for b in bins:
        met_val     =  sig_yields_dict_met[sig][b]
        genmet_val  =  sig_yields_dict_genmet[sig][b]
        avemet_val  =  sig_yields_dict_avemet[sig][b]
        genMETcorrFactor      =  avemet_val/met_val if met_val.val else 1.
        new_val      =  genMETcorrFactor * mc_yields['PU_central'][sig][b]

        raw_card_yields[sig][b] = u_float(new_val.val, new_val.sigma)
        print  '         GenMETave: ', b, "before: ", mc_yields['PU_central'][sig][b], "after: ", new_val, "genmet factor: ", genMETcorrFactor
        if applyGenWSignalCorr:
            mstop, mlsp = getMasses(sig)
            dm = mstop - mlsp
            yld_mcmatch = yldMCmatch[sig][b] 
            
            if ( dm == 10 and ( 'SRL' in b )) or (dm == 20 and ('SR' in b)):
                genWCorrFact = genWMassCorrFacts[b][dm]       
                before_val   = new_val
                #new_val      = before_val - yld_mcmatch*( u_float(1) - genWCorrFact )
                genWCorrFactError = genWCorrFact.sigma * (yld_mcmatch.val/before_val.val) if before_val.val else genWCorrFact.sigma
                new_val      = before_val - yld_mcmatch*( u_float(1) - u_float(genWCorrFact.val, genWCorrFactError  ))
                #new_val      = before_val - yld_mcmatch*( 1.0 - genWCorrFact.val )
                print  '        -- genWMass:  ', b, "before: ", before_val, "after: ", new_val, "corr factor: ",  genWCorrFact
        if applyFastFullSF:
            matched_bin = [  x for x in fastfull_sfs['el'].keys() if x in b ]
            assert len(matched_bin)==1
            mu_sf   = fastfull_sfs['mu'][matched_bin]
            el_sf   = fastfull_sfs['el'][matched_bin]
            fastfull_combined_sf = (mu_yld* mu_sf + el_yld * el_sf)/(mu_yld + el_yld)
        else:
            fastfull_combined_sf = 1.0            


        card_yields[sig][b] =  new_val
    #card_yields[sig] = deepcopy( sig_yields_dict[sig])
for bkg in mc_bkg_list:
    raw_card_yields[bkg] = deepcopy( mc_yields_dict[bkg] )
    card_yields[bkg] = deepcopy( mc_yields_dict[bkg] )
for bkg in pred_bkg_list:
    raw_card_yields[bkg] = deepcopy( pred_yields_dict[bkg] )
    card_yields[bkg] = deepcopy( pred_yields_dict[bkg] )

#card_yields["Total"] = deepcopy( mc_yields_dict['Total'] )
card_yields['Data']  = deepcopy( sig_yields_dict['DataBlind'] )

pickle.dump( card_yields, open( base_res_dir+"/CardYields.pkl", 'w') )
pickle.dump( raw_card_yields, open( base_res_dir+"/RawCardYields.pkl", 'w') )


def makeSignalCard(sig):
    ret = limitTools.getLimit( 
                card_yields                             , 
                sig             = sig                   , 
                outDir          = card_dir+"/Full"      ,      
                postfix         = postfix               ,  
                calc_limit      = False                 , 
                sys_pkl         = syst_pkl              ,
                data            = 'Data'
            )
    mstop, mlsp = getMasses(sig)
    return mstop, mlsp, ret

nProc = 20
#nProc = False
if not nProc:
    cards =[]
    #for sig in sigList:
    for sig in ['T2tt-300-270']:
        cards.append( makeSignalCard(sig))
else:
    pool        =   multiprocessing.Pool( processes = nProc )
    cards       =   pool.map(makeSignalCard, sigList )
    pool.close()
    pool.join()



limit_dir = cfg.limitDirs[cfg.limitDirs.keys()[0]] + "/" + prefix
makeDir(limit_dir)
limit_keys = {
               "up1":"0.160"         ,   
               "up2":"0.025"         ,
               "exp":"0.500"         ,
               "obs":"-1.000"         ,
               "down1":"0.840"       ,
               "down2":"0.975"       ,
            }







#       print "======================================= DONE MAKING CARDS ======================================"
#       print "to calculate limits:"
#       print "comb"
#       print "cd -"
#       print "./calc_cards_limit.py '{card_dir}/Full/T2tt-*'  {card_dir}/Full_Limits.pkl".format(card_dir = card_dir)
#       #print python  run_splitCardIntoBins.py "/afs/hephy.at/work/n/nrad/results/cards_and_limits/8012_mAODv2_v3/80X_postProcessing_v10/13TeV/HT/ApprovalSys_Mt95_Inccharge_LepAll_lep_pu_SF/AdjustedSys/presel/BinsSummary/TEST3/*.txt" ./splitBins/TEST3/
#       print "\n"
#       print "\n"
#       print "####################################"
#       print "\n"
#       print "\n"
#       print "## To Draw:"
#       print "python"
#       print "from Workspace.DegenerateStopAnalysis.tools.limitTools import drawExpectedLimit"
#       print "drawExclusionLimit('/afs/hephy.at/user/n/nra_pu_SF/HT/presel/BinsSummary/Limits/TEST___')
#       print "drawExclusionLimit('{card_dir}_Limits.pkl', '{limit_dir}/{limit_var}.png' , key='{k}') ".format(card_dir = card_dir, limit_dir = limit_dir, limit_var = limit_var , k = k )
#       
#       print "\n"
#       print "\n"
#       print "## To Split cards into bins: "
#       print "python  run_splitCardIntoBins.py  '{card_dir}/Full/T2tt-*.txt'  {card_dir}/".format(card_dir = card_dir)
#       print "####################################"
#       
#       
#       print './calc_cards_limit.py "{card_dir}/SR1a/*.txt" {card_dir}/SR1a_Limits.pkl'.format(card_dir = card_dir) 
#       print './calc_cards_limit.py "{card_dir}/SR1b/*.txt" {card_dir}/SR1b_Limits.pkl'.format(card_dir = card_dir)
#       print './calc_cards_limit.py "{card_dir}/SR1c/*.txt" {card_dir}/SR1c_Limits.pkl'.format(card_dir = card_dir)
#       print './calc_cards_limit.py "{card_dir}/SR2/*.txt"  {card_dir}/SR2_Limits.pkl'.format(card_dir = card_dir)
#       
#       print "\n"
#       print "from Workspace.DegenerateStopAnalysis.tools.limitTools import drawExpectedLimit"
#       for sr in ['SR1a', 'SR1b', 'SR1c', 'SR2']:
#           print "\n ## SR: %s"%sr
#           for limit_var, k in limit_keys.iteritems():
#               print "drawExpectedLimit('{card_dir}/{sr}_Limits.pkl', '{limit_dir}/{sr}/{limit_var}.png' , key='{k}') ".format(card_dir = card_dir, sr=sr, limit_dir = limit_dir, limit_var = limit_var , k = k )
#       



postjob = ""
postjob += "\n"+ "# ======================================= DONE MAKING CARDS ======================================"
postjob += "\n"+ "## to calculate limits:"
postjob += "\n"+ "comb  ## go to area with with HiggsCombTool and cmsenv" 
postjob += "\n"+ "tls ## go back the tools dir in the 80X env   /Workspace/DegenerateStopAnalysis/python/tools"  
postjob += "\n"+ "./calc_cards_limit.py '{card_dir}/Full/T2tt-*'  {card_dir}/Full_Limits.pkl".format(card_dir = card_dir)
postjob += "\n"+ "\n"
postjob += "\n"+ "\n"
postjob += "\n"+ "####################################"
postjob += "\n"+ "\n"
postjob += "\n"+ "\n"
postjob += "\n"+ "## To Draw:"
postjob += "\n"+ "python"
postjob += "\n"+ "\n from Workspace.DegenerateStopAnalysis.tools.limitTools import drawExclusionLimit"
postjob += "\n"+ "drawExclusionLimit('{card_dir}/Full_Limits.pkl', '{limit_dir}/Full/Limits.png' ) ".format(card_dir = card_dir, limit_dir = limit_dir   )
postjob += "\n"+ "\n"
postjob += "\n"+ "\n"
postjob += "\n"+ "## To Split cards into bins: "
postjob += "\n"+ "python  run_splitCardIntoBins.py  '{card_dir}/Full/T2tt-*.txt'  {card_dir}/".format(card_dir = card_dir)
postjob += "\n"+ "####################################"


postjob += "\n"+ './calc_cards_limit.py "{card_dir}/SR1a/*.txt" {card_dir}/SR1a_Limits.pkl'.format(card_dir = card_dir) 
postjob += "\n"+ './calc_cards_limit.py "{card_dir}/SR1b/*.txt" {card_dir}/SR1b_Limits.pkl'.format(card_dir = card_dir)
postjob += "\n"+ './calc_cards_limit.py "{card_dir}/SR1c/*.txt" {card_dir}/SR1c_Limits.pkl'.format(card_dir = card_dir)
postjob += "\n"+ './calc_cards_limit.py "{card_dir}/SR2/*.txt"  {card_dir}/SR2_Limits.pkl'.format(card_dir = card_dir)
postjob += "\n"+ './calc_cards_limit.py "{card_dir}/SR1ab2/*.txt"  {card_dir}/SR1ab2_Limits.pkl'.format(card_dir = card_dir)


postjob += "\n"+ "from Workspace.DegenerateStopAnalysis.tools.limitTools import drawExclusionLimit"
for sr in ['SR1a', 'SR1b', 'SR1c', 'SR2' , 'SR1ab2']:
    postjob += "\n"+ "\n ## SR: %s"%sr
    #postjob += "\n"+ "drawExclusionLimit('{card_dir}/{sr}_Limits.pkl', '{limit_dir}/{sr}/{limit_var}.png') ".format(card_dir = card_dir, sr=sr, limit_dir = limit_dir  )
    postjob += "\n"+ "drawExclusionLimit('{card_dir}/{sr}_Limits.pkl', '{limit_dir}/{sr}/Limits.png') ".format(card_dir = card_dir, sr=sr, limit_dir = limit_dir  )


f= open("%s.sh"%prefix, 'w' )
f.write( postjob ) 
f.close()
print postjob


#print "## To Split cards into bins:",
#print "python  run_splitCardIntoBins.py  '{card_dir}/T2tt-*.txt' "
#print "####################################"

print "To calc limits and draw and split into bins run the jobs in %s"%("%s.sh"%prefix)




if applyGenWSignalCorr:

    ROOT.gStyle.SetPaintTextFormat("0.2f")
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.04)



    plts_raw = {}
    plts_corr= {}
    ratios   = {}
    c1 = ROOT.TCanvas("c1","c1", 1400, 950)  
    saveDir = cfg.saveDir +"/Results/%s/"%prefix
    makeDir(saveDir)

    for b in bins:
        plts_raw[b]  = makeStopLSPPlot("RAW_%s"%b,raw_card_yields, bins= [ 23, 237.5, 812.5, 63, 167.5, 795] , key= lambda x:x[b].val, massFunc = getMasses2 )
        plts_corr[b] = makeStopLSPPlot("CORR_%s"%b,card_yields   , bins= [ 23, 237.5, 812.5, 63, 167.5, 795] , key= lambda x:x[b].val, massFunc = getMasses2 )
        ratios[b]=plts_corr[b].Clone("Ratio_%s"%b)
        ratios[b].Divide(plts_raw[b])
        plts_raw[b].Draw("COLZ TEXT")
        latex.DrawLatex(0.2,0.7, "Yields (METAverage) %s"%b)
        c1.SaveAs(saveDir+"YldsMETAve_%s.png"%(b))
        plts_corr[b].Draw("COLZ TEXT")
        latex.DrawLatex(0.2,0.7, "Yields (Gen W Corr.) %s"%b)
        c1.SaveAs(saveDir+"YldsGenWCorr_%s.png"%(b))
        ratios[b].Draw("COLZ TEXT")
        latex.DrawLatex(0.2,0.7, "#frac{MET Ave}{Gen W Corr} %s"%b)
        c1.SaveAs(saveDir+"RatioMETAVEoGenWCorr_%s.png"%(b))


drawEffMap = False
if drawEffMap:

    c1 = ROOT.TCanvas("c2","c2", 1400, 950)  
    saveDir = cfg.saveDir +"/EffMaps/%s/"%prefix
    makeDir(saveDir)

    for b in bins:
       plts_raw[b]  = makeStopLSPPlot("RAW_%s"%b,raw_card_yields, bins= [ 23, 237.5, 812.5, 63, 167.5, 795] , key= lambda x:x[b].val, massFunc = getMasses2 ) 


