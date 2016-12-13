"""
run after running::

ipython -i  degStop.py -- --cfg=ApprovalSys --task=bkg_est  --lepCol=LepGood --lep=mu --cutInst bins_sum   --weight=nopu_noisr  --btag=btag --mcMatch

"""

import pickle
import Workspace.HEPHYPythonTools.xsecSMS as xsecSMS
stop_xsecs = xsecSMS.stop13TeV_NLONLL

ROOT.gStyle.SetPaintTextFormat("0.2f")

saveDirBase = "/afs/hephy.at/user/n/nrad/www/signals/80X/"

res_dir = os.path.expandvars("$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/results/2016/%s/%s/%s/"%(cfg.cmgTag, cfg.ppTag, cfg.runTag)) 

lepCol="LepGood"
lep="mu"

lepCol = args.lepCol
lep    = args.lep

saveDir = saveDirBase + "genWSF/%s_%s/"%(lepCol,lep)
makeDir(saveDir)

yldpkls = {}

mcMatchTag="_mcMatch"
yldpkls['74x%s'%mcMatchTag]="/afs/hephy.at/work/n/nrad/results/cards_and_limits/7412pass2_mAODv2_v6/74X_postProcessing_v4/13TeV/HT/ApprovalSys_Mt95_Inccharge_{lepCol}_{lep}_nopu_noisr_BTAG{mcMatchTag}/AdjustedSys/presel/Yields_12864pbm1_ApprovalSys_Mt95_Inccharge_{lepCol}_{lep}_nopu_noisr_BTAG{mcMatchTag}_presel_BinsSummary.pkl".format(lepCol=lepCol,lep=lep, mcMatchTag = mcMatchTag)
yldpkls['80x%s'%mcMatchTag]="/afs/hephy.at/work/n/nrad/results/cards_and_limits/8012_mAODv2_v3/80X_postProcessing_v10/13TeV/HT/ApprovalSys_Mt95_Inccharge_{lepCol}_{lep}_nopu_noisr_BTAG{mcMatchTag}/AdjustedSys/presel/Yields_12864pbm1_ApprovalSys_Mt95_Inccharge_{lepCol}_{lep}_nopu_noisr_BTAG{mcMatchTag}_presel_BinsSummary.pkl".format(lepCol=lepCol,lep=lep, mcMatchTag = mcMatchTag)
mcMatchTag=""
yldpkls['74x%s'%mcMatchTag]="/afs/hephy.at/work/n/nrad/results/cards_and_limits/7412pass2_mAODv2_v6/74X_postProcessing_v4/13TeV/HT/ApprovalSys_Mt95_Inccharge_{lepCol}_{lep}_nopu_noisr_BTAG{mcMatchTag}/AdjustedSys/presel/Yields_12864pbm1_ApprovalSys_Mt95_Inccharge_{lepCol}_{lep}_nopu_noisr_BTAG{mcMatchTag}_presel_BinsSummary.pkl".format(lepCol=lepCol,lep=lep, mcMatchTag = mcMatchTag)
yldpkls['80x%s'%mcMatchTag]="/afs/hephy.at/work/n/nrad/results/cards_and_limits/8012_mAODv2_v3/80X_postProcessing_v10/13TeV/HT/ApprovalSys_Mt95_Inccharge_{lepCol}_{lep}_nopu_noisr_BTAG{mcMatchTag}/AdjustedSys/presel/Yields_12864pbm1_ApprovalSys_Mt95_Inccharge_{lepCol}_{lep}_nopu_noisr_BTAG{mcMatchTag}_presel_BinsSummary.pkl".format(lepCol=lepCol,lep=lep, mcMatchTag = mcMatchTag)


yldInsts = {}
yldDicts = {}
yldMaps  = {}
effMaps  = {}

yldPlots = {}
effPlots = {}
ratio80x74xPlots = {}
ratio13TeVvs8TeVPlots = {}






for era in yldpkls.keys():
    yldInsts[era] = pickle.load(file(yldpkls[era]))
    yldDicts[era] = yldInsts[era].getNiceYieldDict()
    #yldMaps[era]  = yldInsts[era].getSignalYieldMap()
    effMaps[era] , yldMaps[era] = yldInsts[era].getSignalEffMap(stop_xsecs, lumi = 12864.4)

    bins = yldInsts[era].cutNames
    for b in bins:
        yldPlots[era] = makeStopLSPPlot("Yields_"+b+"_"+era, yldMaps[era][b], "Yields_"+b +"_"+era, key = lambda x: x.val)
        effPlots[era] = makeStopLSPPlot("AccEff_"+b+"_"+era, effMaps[era][b], "AccEff_"+b +"_"+era, key = lambda x: x.val) 

    
        

corrFactPlots = {}
corrFacts = {}
corrFactsAll = {}

corrFactsWithErrors = {}
corrFactsAllWithErrors = {}
#corrFactsWith
if True:    
    c1 = ROOT.TCanvas("Ratios","Ratios", 1400,950)
    makeDir(saveDir+"/vs74x/")
    makeDir(saveDir+"/vs8TeV/")


    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.05)


    for b in bins:
        ratio80x74xPlots[b]      = makeStopLSPRatioPlot("Ratio80xVs74x%s"%b   , effMaps['80x'][b], effMaps['74x'][b], bins= [23, 237.5, 812.5, 125, 167.5, 792.5] , key =  lambda x: x.val )
        ratio80x74xPlots[b][0].Draw("COLZ TEXT")
        latex.DrawLatex(0.2,0.7, "#frac{Acc.*eff(80X)}{Acc.*eff(74X)}  %s"%b) 
        c1.SaveAs(saveDir+"/vs74x/%s.png"%b)

        ratio80x74xPlots[b+"_mcMatch"]      = makeStopLSPRatioPlot("Ratio80xVs74x%s_mcMatch"%b   , effMaps['80x_mcMatch'][b], effMaps['74x_mcMatch'][b], bins= [23, 237.5, 812.5, 125, 167.5, 792.5] , key =  lambda x: x.val )
        ratio80x74xPlots[b+"_mcMatch"][0].Draw("COLZ TEXT")
        latex.DrawLatex(0.2,0.7, "#frac{Acc.*eff(80X)}{Acc.*eff(74X)}  %s %s"%(b, "mcMatch")) 
        c1.SaveAs(saveDir+"/vs74x/%s_mcMatch.png"%b)


        ratio80x74xPlots[b+"mcMatchEff"]      = makeStopLSPRatioPlot("Ratio80xVs74x%s"%b   , effMaps['80x_mcMatch'][b], effMaps['80x'][b], bins= [23, 237.5, 812.5, 125, 167.5, 792.5] , key =  lambda x: x.val )
        ratio80x74xPlots[b+"mcMatchEff"][0].Draw("COLZ TEXT")
        latex.DrawLatex(0.2,0.7, "#frac{Acc.*eff(80X mcMatch)}{Acc.*eff(80X)}  %s"%b) 
        c1.SaveAs(saveDir+"/mcMatchEff_80x/%s.png"%b)


        corrFactPlots[b]   = makeStopLSPRatioPlot("Ratio74xVs80x%s_mcMatch"%b   , effMaps['74x_mcMatch'][b], effMaps['80x_mcMatch'][b], bins= [23, 237.5, 812.5, 125, 167.5, 792.5] , key =  lambda x: x.val )
        corrFactPlots[b][0].Draw("COLZ TEXT")
        latex.DrawLatex(0.2,0.7, "#frac{Acc.*eff(74X)}{Acc.*eff(80X)}  %s %s"%(b, "mcMatch")) 
        c1.SaveAs(saveDir+"/corrFacts/%s_mcMatch.png"%b)

        corrFacts[b]={}
        corrFactsAll[b]={}
        mstops = corrFactPlots[b][1].keys()
        for dm in range(10,81,10):
            dm_corrs = []
            for mstop in mstops:
                mlsp = mstop-dm
                corr = corrFactPlots[b][1][mstop].get(mlsp) 
                if corr:
                    dm_corrs.append(corr)
            dm_ave_corr = float( sum(dm_corrs) ) / len(dm_corrs) if dm_corrs else 1.
            corrFactsAll[b][dm]=dm_corrs
            corrFacts[b][dm]=dm_ave_corr


    ##
    ## Getting Correction Factors Directory (without plots)
    ##


    corrFactsAllWithErrors = {}
    corrFactsWithErrors = {}
    for b in bins:
        corrFactsAllWithErrors[b] = {}
        for mstop in yldMaps['74x_mcMatch'][b].keys():
            corrFactsAllWithErrors[b][mstop] = {}
            for mlsp in yldMaps['74x_mcMatch'][b][mstop].keys():
                dm = mstop-mlsp
                corrFactsAllWithErrors[b][mstop][dm]  = yldMaps['74x_mcMatch'][b][mstop][mlsp]/yldMaps['80x_mcMatch'][b][mstop][mlsp] if yldMaps['80x_mcMatch'][b][mstop].get(mlsp).val else u_float(0) 

    for b in bins:
        corrFactsWithErrors[b] = {}
        for dm in range(10,81,10):
            dm_corrs = []
            for mstop in corrFactsAllWithErrors[b].keys():
                mlsp = mstop-dm
                corr = corrFactsAllWithErrors[b][mstop].get(dm)
                if corr:
                    dm_corrs.append(corr)
            non_zero_dm_corrs = [x for x in dm_corrs if x.val]
            dm_ave_corr = sum(non_zero_dm_corrs) / len(non_zero_dm_corrs) if non_zero_dm_corrs else u_float(1.,0)
            if not dm_ave_corr.val:   
                print "couldn't calculate correction factor for corrFactsAllWithErrors['%s'], dm=%s "%(b,dm), " Setting it to 1.0+-0."
                dm_ave_corr = u_float(1.,0.)
            corrFactsWithErrors[b][dm]=dm_ave_corr



    finalCorrFacts = {}
    for b in bins:
        finalCorrFacts[b] = {}
        for dm in range(10,21,10):
            cfact = corrFactsWithErrors[b][dm]
            if cfact.sigma > cfact.val:
                print "For bin=%s, dm=%s, stat unc is 2* the value (%s).... correction will be set to 1.+-0."%(b,dm, cfact)
                cfact = u_float(1.,0)
            #if  abs(1-cfact.val) < 1.5*cfact.sigma :
            #    print "For bin=%s, dm=%s, corr fact is compatible with 1.0, will set value az zero"%(b,dm, cfact)
            #    cfact = u_float(1.,0)
            if  dm == 10 and not "SRL" in b:
                print "For bin=%s, dm=%s, Setting corr factor to 1+-0, instead of %s"%(b,dm, cfact )
                cfact = u_float(1.,0)
            finalCorrFacts[b][dm] = cfact 
    srbins = ['SRL1a', 'SRH1a', 'SRV1a', 'SRL1b', 'SRH1b', 'SRV1b', 'SRL1c', 'SRH1c', 'SRV1c', 'SRL2', 'SRH2', 'SRV2']
    for b in srbins:
        corrs = ["%s:    %s"%(k,"{:^4}+-{:^5},    ".format(v.round(2).val, v.round(2).sigma)) for k,v in finalCorrFacts[b].iteritems()]
        toprint = [b, ] + corrs
        print ("{:<10}"*len(toprint)).format(*toprint)


    dmplts={}
    dOpt = ""
    leg = ROOT.TLegend(0.7,0.7,0.9,0.9)
    for dm in range(10,21,10):
        dmplts[dm] = makeHistoFromDict({k:v[dm] for k,v in finalCorrFacts.iteritems() }, name="DM%s"%dm, bin_order=srbins)
        dmplts[dm].SetLineColor(3+dm/10)
        dmplts[dm].SetLineWidth(1)
        dmplts[dm].SetMarkerSize(0)
        dmplts[dm].SetMaximum(2)
        dmplts[dm].SetMinimum(0)
        
        dmplts[dm].Draw(dOpt)
        leg.AddEntry(dmplts[dm], "#Deltam = %s"%dm, "l")
        dOpt="same"

    unity = dmplts[dm].Clone()
    unity.Sumw2(0)
    unity.Divide(unity)
    unity.SetLineColor(ROOT.kBlack)
    unity.Draw("same")

    leg.Draw()
    c1.SaveAs(saveDir+"/CorrFacts.png")

    makeDir(res_dir)
    pickle.dump(finalCorrFacts,file(res_dir+"/SignalCorrFactors.pkl","w"))
    print "output saved in SignalCorrFactors.pkl"
