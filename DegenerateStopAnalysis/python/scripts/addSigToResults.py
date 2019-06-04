import Workspace.DegenerateStopAnalysis.samples.samplesInfo as samplesInfo
import Workspace.DegenerateStopAnalysis.tools.degTools as degTools
import Workspace.DegenerateStopAnalysis.tools.sysTools as sysTools
import ROOT
reload( sysTools )

#try:
#    mlfres
#except NameError:
#    srbins = [x for x in syst.regions_info.getCardInfo('MTCTLepPtVL2')['card_regions'] if 'sr' in x]
#    mlfres = sysTools.MaxLikelihoodResult( "/afs/hephy.at/work/n/nrad/results/cards_and_limits//13TeV/8025_mAODv2_v7/80X_postProcessing_v1/EPS17_v0/June17_v3/LepGood_lep_lowpt_Jet_def_SF_Prompt_PU_TTIsr_Wpt_TrigEff_lepSFFix/DataBlind/presel_base/Results_bins_mtct_sum/PreAppANv6_3__MTCTLepPtVL2/June17_v3_bins_mtct_sum_T2tt_300_270_PreAppANv6_3__MTCTLepPtVL2.txt" ,
#                                            srbins, 'test', syst.saveDir +"/" +'testtag', rerun=False)


sigPoints = {
                "T2tt_375_365" :{'funcs':{'SetLineColor':ROOT.kAzure  ,'SetFillColor':0,'SetLineWidth':3,'SetLineStyle':1}}, 
                "T2tt_500_470" :{'funcs':{'SetLineColor':ROOT.kRed    ,'SetFillColor':0,'SetLineWidth':3,'SetLineStyle':1}}, 
                #"T2tt_375_295" :{'funcs':{'SetLineColor':ROOT.kGreen+2    ,'SetFillColor':0,'SetLineWidth':3,'SetLineStyle':6}}, 
             }

sigPointsT2tt = {
                "T2tt_375_365" :{'funcs':{'SetLineColor':ROOT.kBlue,'SetFillColor':0,'SetLineWidth':3,'SetLineStyle':5}}, 
                "T2tt_500_470" :{'funcs':{'SetLineColor':ROOT.kRed    ,'SetFillColor':0,'SetLineWidth':3,'SetLineStyle':6}}, 
                "T2tt_375_295" :{'funcs':{'SetLineColor':ROOT.kBlack    ,'SetFillColor':0,'SetLineWidth':3,'SetLineStyle':7}}, 
             }

sigPointsT2bW = {
                "T2bW_375_365" :{'funcs':{'SetLineColor':ROOT.kBlue,'SetFillColor':0,'SetLineWidth':3,'SetLineStyle':5}}, 
                "T2bW_500_470" :{'funcs':{'SetLineColor':ROOT.kRed    ,'SetFillColor':0,'SetLineWidth':3,'SetLineStyle':6}}, 
                "T2bW_375_295" :{'funcs':{'SetLineColor':ROOT.kBlack    ,'SetFillColor':0,'SetLineWidth':3,'SetLineStyle':7}}, 
             }


sigPointsMSSM = {
                'MSSM_120_1000'    :  {'funcs':{'SetLineColor':ROOT.kBlue     ,'SetFillColor':0,'SetLineWidth':3,'SetLineStyle':1}},     
                'MSSM_160_500'     :  {'funcs':{'SetLineColor':ROOT.kRed      ,'SetFillColor':0,'SetLineWidth':3,'SetLineStyle':1}},  
                'MSSM_220_300'     :  {'funcs':{'SetLineColor':ROOT.kBlack    ,'SetFillColor':0,'SetLineWidth':3,'SetLineStyle':1}},     
                }


 #'C1C1H_150_120'    :  {'funcs':{'SetLineColor':ROOT.kBlue     ,'SetFillColor':0,'SetLineWidth':3,'SetLineStyle':1}},       
 #'C1C1H_175_167.5'  :  {'funcs':{'SetLineColor':ROOT.kRed      ,'SetFillColor':0,'SetLineWidth':3,'SetLineStyle':1}},    
 #'C1C1H_225_205'    :  {'funcs':{'SetLineColor':ROOT.kBlack    ,'SetFillColor':0,'SetLineWidth':3,'SetLineStyle':1}},      

 #'C1N1H_140_110'    :  {'funcs':{'SetLineColor':ROOT.kBlue     ,'SetFillColor':0,'SetLineWidth':3,'SetLineStyle':1}},     
 #'C1N1H_180_172.5'  :  {'funcs':{'SetLineColor':ROOT.kRed      ,'SetFillColor':0,'SetLineWidth':3,'SetLineStyle':1}},     
 #'C1N1H_220_200'    :  {'funcs':{'SetLineColor':ROOT.kBlack    ,'SetFillColor':0,'SetLineWidth':3,'SetLineStyle':1}},     


 #'N2N1H_140_110'    :  {'funcs':{'SetLineColor':ROOT.kBlue     ,'SetFillColor':0,'SetLineWidth':3,'SetLineStyle':1}},         
 #'N2N1H_160_152.5'  :  {'funcs':{'SetLineColor':ROOT.kRed      ,'SetFillColor':0,'SetLineWidth':3,'SetLineStyle':1}},         
 #'N2N1H_180_160'    :  {'funcs':{'SetLineColor':ROOT.kBlack    ,'SetFillColor':0,'SetLineWidth':3,'SetLineStyle':1}},         

sigPointsTChiWZ = {
      'TChiWZ_150_140'   :  {'funcs':{'SetLineColor':ROOT.kBlue     ,'SetFillColor':0,'SetLineWidth':3,'SetLineStyle':1}},         
      'TChiWZ_175_170' :  {'funcs':{'SetLineColor':ROOT.kRed      ,'SetFillColor':0,'SetLineWidth':3,'SetLineStyle':1}},         
      'TChiWZ_250_230'   :  {'funcs':{'SetLineColor':ROOT.kBlack    ,'SetFillColor':0,'SetLineWidth':3,'SetLineStyle':1}},         
    }

#sigPoints = sigPointsNew


sigPointsModels = {
                'T2tt':    sigPointsT2tt,
                'T2bW':    sigPointsT2bW,
                'TChiWZ':  sigPointsTChiWZ,
                'MSSM':    sigPointsMSSM,
            }

def addSigToRes(  syst, mlfres , sigPoints = sigPoints, outputTag = "/Modified/", postfix="") :
    hists= mlfres.hists_srs
    fit  = 'fit_b'
    plotDir = syst.saveDir +"/"+ outputTag
    
    
    bkg_list= ["WJets","TTJets","Fakes","Others"]
    
    
    loc = [0.7, 0.7, 0.9, 0.85]
    leg = ROOT.TLegend(*loc)
    leg.SetFillColor(0)
    leg.SetFillColorAlpha(0,0)
    leg.SetBorderSize( 0 )
    hists_info =  [{'hist':hists[fit][name], 'name':samplesInfo.sampleName(name,"latexName") , 'opt':'f'} for name in bkg_list ]
    degTools.addHistsToLeg(leg, hists_info)
    
    #sysTools.drawNiceDataPlot(
    #                  data_hist = hists[fit]['data'] ,
    #                  mc_stack  = hists[fit]['stack'] ,
    #                  sig_stack = hists[fit]['signal'] ,
    #                  mc_total  = hists[fit]['total_background'],
    #                  options   = {'logy':1} ,
    #                  saveDir   = plotDir           ,
    #                  name      = fit ,
    #                  leg       = leg ,
    #                )
    
    
    sigOrder = sorted( sigPoints.keys(), key = lambda x: degTools.getMasses(x)[0] - degTools.getMasses(x)[1] , reverse = False)

    bins      = [hists['fit_b']['data'].GetXaxis().GetBinLabel(i+1) for i in range( hists['fit_b']['data'].GetNbinsX() ) ] 
    srbins    = [x for x in bins if 'sr' in x]
    sigHists  = {s:degTools.makeHistoFromList( [ syst.central_yld_sum[sr][s] for sr in srbins] , name=s , func=lambda x:x.val ) for s in sigPoints }
    
    for sig, hist in sigHists.items() :
        funcs = sigPoints[sig].get('funcs',{})
        for func, funcarg in funcs.items():
            getattr(hist, func)(funcarg)
    
    sigStack = degTools.getStackFromHists( sigHists.values(), 'sigstack' )
    
    
    loc = [0.5, 0.7, 0.7, 0.85]
    leg2 = ROOT.TLegend(*loc)
    leg2.SetFillColor(0)
    leg2.SetFillColorAlpha(0,0)
    leg2.SetBorderSize( 0 )
    hists_info = [ {'hist':sigHists[sigName] , 'name':"%s(%s,%s)"%tuple(sigName.rsplit("_")), 'opt':'l'} for sigName  in sigOrder ]
    hists_info.append( {'hist':hists[fit]['data'] , 'name':"Data" ,'opt':'p'})
    degTools.addHistsToLeg(leg2, hists_info)
    
    
    
    
    out = sysTools.drawNiceDataPlot(
                      data_hist = hists[fit]['data'] ,
                      mc_stack  = hists[fit]['stack'] ,
                      sig_stack = sigStack,
                      mc_total  = hists[fit]['total_background'],
                      options   = {'logy':1} ,
                      saveDir   = plotDir           ,
                      name      = fit + "_WithSigs"+postfix ,
                      leg       = [leg,leg2], #leg ,
                    )
    
    return out
