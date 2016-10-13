import ROOT
import  Workspace.DegenerateStopAnalysis.tools.degTools as degTools

save_dir = "/afs/hephy.at/user/n/nrad/www/signals/80X/nIsrNorm"

cmg_dir = "/data/nrad/cmgTuples/8012_mAODv2_v3/RunIISpring16MiniAODv2"

sig_dir_tot  = cmg_dir +"/" + "T2tt_dM_30to80/"
sig_dir_pass = cmg_dir +"/" + "T2tt_dM_30to80_genHT_160_genMET_80/"

treeProdDir  = "treeProducerSusySingleLepton/"
sig_tree_dir_tot  = sig_dir_tot  + "/" + treeProdDir +"/tree.root"  
sig_tree_dir_pass = sig_dir_pass + "/" + treeProdDir +"/tree.root" 

tot_tree  = ROOT.TChain("tree")
pass_tree = ROOT.TChain("tree")


tot_tree.Add( sig_tree_dir_tot  )
pass_tree.Add( sig_tree_dir_pass )




isrRwgtString = "{normFact} * ( (nIsr==0) + (nIsr==1)*0.882  + (nIsr==2)*0.792  + (nIsr==3)*0.702  + (nIsr==4)*0.648  + (nIsr==5)*0.601  + (nIsr>=6)*0.515 ) "
isrRwgt = lambda normFact: isrRwgtString.format( normFact=normFact )


mstops_range = (250,801,25)
dms_range    = (30,81,10)
mstops       = range(*mstops_range)
dms          = range(*dms_range)


nisr_bins = (12,0,12)


results={}

normFact = 1.
isrweight = isrRwgt(normFact)
noweight  = '(1)'




if True:  ### as a function of stop and lsp

    mstop_cut_func = lambda mstop : "(GenSusyMStop=={mstop})".format(mstop=mstop, mlsp=mlsp)
    
    for mstop in mstops:
        results[mstop]={}
        mstop_cut = mstop_cut_func(mstop)
        results[mstop]['plt_rwgt']  = degTools.getPlotFromChain( tot_tree,"nIsr", nisr_bins, cutString=mstop_cut, weight= isrweight , uniqueName=True )
        results[mstop]['plt_nowgt'] = degTools.getPlotFromChain( tot_tree,"nIsr", nisr_bins, cutString=mstop_cut, weight= noweight  , uniqueName=True )
        
        results[mstop]['plt_rwgt'].SetName("nIsr_rwgt_%s"%(mstop))
        results[mstop]['plt_nowgt'].SetName("nIsr_nowgt_%s"%(mstop))
    
        results[mstop]['area_rwgt'] = results[mstop]['plt_rwgt'].Integral()
        results[mstop]['area_nowgt'] = results[mstop]['plt_nowgt'].Integral()
    
        results[mstop]['normFact']   = results[mstop]['area_nowgt']/results[mstop]['area_rwgt']  
    
        print "mStop: %s"%mstop,  "normFact: %s"%results[mstop]['normFact']
    
    
    
    dstops = 25
    bins = [ len(mstops), min(mstops) - 0.5*dstops , max(mstops) + 0.5*dstops, (max(mstops) + min(dms) - ( min(mstops)-max(dms))) /5  ,min(mstops)-max(dms)-5 , max(mstops) + min(dms)+5 ]
    
    
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptFit(1) 

    canvs = degTools.makeCanvasMultiPads("normFacts", 1600,1000 , pads=[], padRatios=[1,1])


    plots = {}
    plots['normFact']       = ROOT.TH1D("plot_normFact","normFacts",*bins[0:3])
    plots['area_rwgt'] = ROOT.TH1D("plot_ISRWgt"  ,"ISRWgt"   ,*bins[0:3])
    plots['area_nowgt'] = ROOT.TH1D("plot_NoWgt"   ,"NoWgt"    ,*bins[0:3])

    for mstop in mstops:
        for plot_var, plt in plots.iteritems():
            b = plt.FindBin( mstop )
            v = results[mstop][plot_var]
            plt.SetBinContent(b,v)

    canvs[1].cd()
    plots['area_nowgt'].SetTitle("nISR Normalizations")
    plots['area_nowgt'].GetXaxis().SetTitle("mStop")
    plots['area_nowgt'].Draw()
    plots['area_nowgt'].SetMinimum( plots['area_nowgt'].GetMinimum()*0.8)
    plots['area_rwgt'].Draw("same")

    canvs[2].cd()
    plots['normFact'].GetXaxis().SetTitle("mStop")
    plots['normFact'].GetXaxis().SetTitleSize(0.1)
    plots['normFact'].GetYaxis().SetTitle("Norm. Factor")
    plots['normFact'].GetYaxis().SetTitleSize(0.1)
    plots['normFact'].GetYaxis().SetTitleOffset(0.3)
    plots['normFact'].Draw()


    myline = ROOT.TF1("myline","[0]*x + [1]" )
    myline.SetParName(0,"m")
    myline.SetParName(1, "b")
    myline.SetParameter(0,0.0007)
    myline.SetParameter(1,0)
    plt = plots['normFact']
    fit = plt.Fit("myline","S")
  
    myline.Draw("same") 
    eq = "%0.3e * mStop + %0.3f"%(myline.GetParameter(0), myline.GetParameter(1))
    lambdaeq = "(%0.3e *(GenSusyMStop) + %0.3f)"%(myline.GetParameter(0), myline.GetParameter(1))

    canvs[0].SaveAs(save_dir +"/nISR_normFactors_stop.png")

 
    
    
    allNormFacts = [ results[mstop]['normFact'] for mstop in mstops    ]
    average = sum(allNormFacts)/len(allNormFacts)
    
    print "\nAverage Normalizaton Factor: ", average

    print "Fit Eq:" , eq
    print lambdaeq















if False:  ### as a function of stop and lsp

    mstop_mlsp_cut_func = lambda mstop,mlsp : "(GenSusyMStop=={mstop})&&(GenSusyMNeutralino=={mlsp})".format(mstop=mstop, mlsp=mlsp)
    
    
    
    for mstop in mstops:
        results[mstop]={}
        for dm in dms:
            mlsp = mstop-dm
            mstop_mlsp_cut = mstop_mlsp_cut_func(mstop,mlsp)
            results[mstop][mlsp]={}
            results[mstop][mlsp]['plt_rwgt']  = degTools.getPlotFromChain( tot_tree,"nIsr", nisr_bins, cutString=mstop_mlsp_cut, weight= isrweight , uniqueName=True )
            results[mstop][mlsp]['plt_nowgt'] = degTools.getPlotFromChain( tot_tree,"nIsr", nisr_bins, cutString=mstop_mlsp_cut, weight= noweight  , uniqueName=True )
            
            results[mstop][mlsp]['plt_rwgt'].SetName("nIsr_rwgt_%s_%s"%(mstop,mlsp))
            results[mstop][mlsp]['plt_nowgt'].SetName("nIsr_nowgt_%s_%s"%(mstop,mlsp))
    
            results[mstop][mlsp]['area_rwgt'] = results[mstop][mlsp]['plt_rwgt'].Integral()
            results[mstop][mlsp]['area_nowgt'] = results[mstop][mlsp]['plt_nowgt'].Integral()
    
            results[mstop][mlsp]['normFact']   = results[mstop][mlsp]['area_nowgt']/results[mstop][mlsp]['area_rwgt']  
    
            print "mStop: %s"%mstop, "mLSP: %s"%mlsp, "normFact: %s"%normFact
    
    
    
    dstops = 25
    bins = [ len(mstops), min(mstops) - 0.5*dstops , max(mstops) + 0.5*dstops, (max(mstops) + min(dms) - ( min(mstops)-max(dms))) /5  ,min(mstops)-max(dms)-5 , max(mstops) + min(dms)+5 ]
    
    
    ROOT.gStyle.SEtOptStat(0)
    
    plot_normFacts    = degTools.makeStopLSPPlot( "nISR_normFactors", results, "nISR_normFactors", bins, lambda x: x['normFact'] )
    plot_normFacts.Draw("COLZ TEXT")
    plot_normFacts.SetMarkerSize(0.8)
    ROOT.c1.SaveAs(save_dir +"/nISR_normFactors.png")
    
    plot_integ_isrwgt = degTools.makeStopLSPPlot( "nISR_Integral_ISRWgt", results, "nISR_Integral_ISRWgt", bins, lambda x: x['area_rwgt'] )
    plot_integ_isrwgt.Draw("COLZ TEXT")
    plot_integ_isrwgt.SetMarkerSize(0.8)
    ROOT.c1.SaveAs(save_dir +"/nISR_Integral_ISRWgt.png")
    
    plot_integ_nowgt  = degTools.makeStopLSPPlot( "nISR_Integral_NoWgt", results, "nISR_Integral_NoWgt", bins, lambda x: x['area_nowgt'] )
    plot_integ_nowgt.Draw("COLZ TEXT")
    plot_integ_nowgt.SetMarkerSize(0.8)
    ROOT.c1.SaveAs(save_dir +"/nISR_Integral_NoWgt.png")
    
    
    allNormFacts = [ results[mstop][mstop-dm]['normFact'] for mstop in mstops for dm in dms   ]
    average = sum(allNormFacts)/len(allNormFacts)
    
    print "\nAverage Normalizaton Factor: ", average







