import ROOT
import  Workspace.DegenerateStopAnalysis.tools.degTools as degTools

save_dir = "/afs/hephy.at/user/n/nrad/www/signals/80X/Q2Norm"

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







mstops_range = (250,801,25)
dms_range    = (30,81,10)
mstops       = range(*mstops_range)
dms          = range(*dms_range)




results={}
plots   = {}


lhe_weights = {
                1:  {'muR': 'central'     ,'muF':  'central'          } ,        ## <weight id="1001"> muR=1 muF=1 
                2:  {'muR': 'central'     ,'muF':  'up'               } ,        ## <weight id="1002"> muR=1 muF=2 
                3:  {'muR': 'central'     ,'muF':  'down'             } ,        ## <weight id="1003"> muR=1 muF=0.5 
                4:  {'muR': 'up'          ,'muF':  'central'          } ,        ## <weight id="1004"> muR=2 muF=1 
                5:  {'muR': 'up'          ,'muF':  'up'               } ,        ## <weight id="1005"> muR=2 muF=2 
                6:  {'muR': 'up'          ,'muF':  'down'             } ,        ## <weight id="1006"> muR=2 muF=0.5 
                7:  {'muR': 'down'        ,'muF':  'central'          } ,        ## <weight id="1007"> muR=0.5 muF=1 
                8:  {'muR': 'down'        ,'muF':  'up'               } ,        ## <weight id="1008"> muR=0.5 muF=2 
                9:  {'muR': 'down'        ,'muF':  'down'             } ,        ## <weight id="1009"> muR=0.5 muF=0.5 
              }






q2weights={}
for weight_id, lhe_weight in lhe_weights.iteritems():
    weight_name             = "Q2"+lhe_weight['muR'] +"_" + lhe_weight['muF']
    weight                  = "LHEWeights_wgt[%s]"%weight_id
    q2weights[weight_name] = weight

noweight = "LHEWeights_wgt[1]"

normEqs={}
eqs = {}
for wn, weight in q2weights.iteritems(): 


    mstop_cut_func = lambda mstop : "(GenSusyMStop=={mstop})".format(mstop=mstop )

    print '\n\n\n'
    print "Q2 Variation", wn, weight
    print '\n'
    

    results[wn]={}    
    for mstop in mstops:
        results[wn][mstop]={}
        mstop_cut = mstop_cut_func(mstop)
        results[wn][mstop]['plt_rwgt']  = degTools.getPlotFromChain( tot_tree,"(1)", (2,0,2), cutString=mstop_cut, weight= weight    , uniqueName=True )
        results[wn][mstop]['plt_nowgt'] = degTools.getPlotFromChain( tot_tree,"(1)", (2,0,2), cutString=mstop_cut, weight= noweight  , uniqueName=True )
        
        results[wn][mstop]['plt_rwgt'].SetName("%s_rwgt_%s"%(wn, mstop))
        results[wn][mstop]['plt_nowgt'].SetName("%s_nowgt_%s"%(wn, mstop))
    
        results[wn][mstop]['area_rwgt'] = results[wn][mstop]['plt_rwgt'].Integral()
        results[wn][mstop]['area_nowgt'] = results[wn][mstop]['plt_nowgt'].Integral()
    
        results[wn][mstop]['normFact']   = results[wn][mstop]['area_nowgt']/results[wn][mstop]['area_rwgt']  
    
        print "mStop: %s"%mstop,  "normFact: %s"%results[wn][mstop]['normFact']
    
    
    
    dstops = 25
    bins = [ len(mstops), min(mstops) - 0.5*dstops , max(mstops) + 0.5*dstops, (max(mstops) + min(dms) - ( min(mstops)-max(dms))) /5  ,min(mstops)-max(dms)-5 , max(mstops) + min(dms)+5 ]
    
    
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptFit(1) 

    canvs = degTools.makeCanvasMultiPads("normFacts", 1600,1000 , pads=[], padRatios=[1,1])


    plots[wn] = {}
    plots[wn]['normFact']       = ROOT.TH1D("plot_normFact","normFacts",*bins[0:3])
    plots[wn]['area_rwgt'] = ROOT.TH1D("plot_%s"%wn  ,wn   ,*bins[0:3])
    plots[wn]['area_nowgt'] = ROOT.TH1D("plot_NoWgt"   ,"NoWgt"    ,*bins[0:3])

    for mstop in mstops:
        for plot_var, plt in plots[wn].iteritems():
            b = plt.FindBin( mstop )
            v = results[wn][mstop][plot_var]
            plt.SetBinContent(b,v)

    canvs[1].cd()
    plots[wn]['area_nowgt'].SetTitle("%s Normalizations"%wn)
    plots[wn]['area_nowgt'].GetXaxis().SetTitle("mStop")
    plots[wn]['area_nowgt'].Draw()
    plots[wn]['area_nowgt'].SetMinimum( plots[wn]['area_nowgt'].GetMinimum())
    plots[wn]['area_rwgt'].SetLineStyle(2)
    plots[wn]['area_rwgt'].Draw("same")
    #canvs[1].SetLogy(1)

    canvs[2].cd()
    plots[wn]['normFact'].GetXaxis().SetTitle("mStop")
    plots[wn]['normFact'].GetXaxis().SetTitleSize(0.1)
    plots[wn]['normFact'].GetYaxis().SetTitle("Norm. Factor")
    plots[wn]['normFact'].GetYaxis().SetTitleSize(0.1)
    plots[wn]['normFact'].GetYaxis().SetTitleOffset(0.3)
    plots[wn]['normFact'].Draw()


    myline = ROOT.TF1("myline","[0]+[1]*x+[2]*x*x" )
    myline.SetParName(0,"c")
    myline.SetParName(1, "b")
    myline.SetParName(2, "a")
    myline.SetParameter(0,1.1)
    myline.SetParameter(1,0)
    myline.SetParameter(2,0)
    #myline.SetParameter(2,300)
    plt = plots[wn]['normFact']
    fit = plt.Fit("myline","S")
  
    myline.Draw("same")
    params = (myline.GetParameter(0), myline.GetParameter(1) , myline.GetParameter(2))
    #eq = "%0.3f * exp(%0.3e * mStop )"%params
    #lambdaeq = "%0.3f * exp(%0.3e * (GenSusyMStop)  )"%params
    lambdaeq = "(%0.3e + ( %0.3e * (GenSusyMStop)) + ( %0.3e * (GenSusyMStop)*(GenSusyMStop) ) )  "%params
    results[wn]['eq']=lambdaeq
    canvs[0].SaveAs(save_dir +"/Q2%s_normFactors_stop.png"%wn)

 
    
    
    allNormFacts = [ results[wn][mstop]['normFact'] for mstop in mstops    ]
    average = sum(allNormFacts)/len(allNormFacts)
    
    print "\nAverage Normalizaton Factor: ", average

    print "Fit Eq:" ,
    print lambdaeq
    normEqs[wn]=lambdaeq   
    eqs[wn] = lambdaeq
    
print normEqs


















