import os
import glob
import pickle
import Workspace.DegenerateStopAnalysis.tools.degTools as degTools
import Workspace.DegenerateStopAnalysis.tools.limitTools as limitTools
from Workspace.HEPHYPythonTools.asym_float import asym_float 
from Workspace.DegenerateStopAnalysis.tools.CombineCard import CombinedCard, safe_int, safe_val

NPROC = 20

def round_safe_val(x):
    val = safe_val(x)
    return round(val,3)

def getFakeEstimateFromCombine( obs, exp, sig=1, bin_name = "bin1", systs=None , allowNonIntegerObs = True):
    #print bin_name
    cfw        = CombinedCard();

    ylds = {
                "prompts": {bin_name : exp },
                "obs"    : {bin_name : obs },
                "signal" : {bin_name : sig }
           }

    cfw.addBins( ["prompts"] , [ bin_name ]  )
    if allowNonIntegerObs:
        cfw.allowNonIntegerObservation = True
        makeIntFunc = round_safe_val
    else:
        makeIntFunc = safe_int    

    cfw.specifyObservations( ylds , obsProcess = "obs" , bins = [bin_name] , makeInt = makeIntFunc) 
    cfw.specifyBackgroundExpectations( ylds, ['prompts'] ) 
    cfw.specifySignalExpectations(  ylds , sigProcess = "signal" ) 
    cfw.addStatisticalUncertainties(yieldDict= ylds, processes=["prompts"], bins=[bin_name])


    tmp_dir = "tmp_fakeEst_%s_%s"%(bin_name, degTools.uniqueHash() )
    degTools.makeDir(tmp_dir)
    
    cardname = "card.txt"
    cardpath = "%s/%s"%(tmp_dir,cardname)
    cfw.writeToFile( cardpath )


    expFake = (obs-exp)
    rmax = 2* ( expFake.val + expFake.sigma )
    rmin = 0.5 * ( expFake.val-expFake.sigma) 
    rMaxOpt=""
    if rmax>20 or rmin>20:
        rMaxOpt="--rMax=%s  --rMin=%s"%(rmax,rmin)
    #print '\n\n\n', '------', obs, exp, obs-exp, rmax, rmin
    limitTools.runCombineCommand(cardname, combine_option = "-M MaxLikelihoodFit --forceRecreateNLL %s"%rMaxOpt, output_dir = tmp_dir , verbose = True)
    output_file = glob.glob( tmp_dir+"/*MaxLikelihoodFit*.root" )
    
    if not len(output_file)==1:
        raise Exception("No output found for MLF! This is where I looked: %s \nand this is what I found: %s"%( tmp_dir+"/*MaxLikelihoodFit*.root" , output_file) )

    output_file = output_file[0]
    result = limitTools.readResFile( output_file )
    #print result
    cen  = result['0.500']
    down = result['0.160'] - cen
    up   = result['0.840'] - cen

    youAreFancy = False
    if youAreFancy:
        output = asym_float( cen, down, up )
    else:
        output = {'central': cen , 'down': down, 'up':up } 
    return output  


def getFakeEstimateFromCombineWrapper( args ):
    return getFakeEstimateFromCombine( *args )

def getFakeEstimateParal( prompt_fake_yields, bins = None, data_key = "__Data_X_TL", prompt_key="__Prompts_X_TL", nProc = NPROC):
    bins = bins if not bins==None else prompt_fake_yields.keys()
    args = []
    simple_output = {}
    for b in bins:
        bin_args = [ prompt_fake_yields[b]['__Data_X_TL'] , prompt_fake_yields[b]['__Prompts_X_TL'] , 1, b]
        obs, exp, sig, bin_name = bin_args
        args.append( bin_args ) 
        simple_output[b]={'obs':obs, 'exp': exp, 'obs-exp':obs-exp}
    res = degTools.runFuncInParal( getFakeEstimateFromCombineWrapper , args , nProc = nProc) 
    output = dict(zip( bins, res))
    
    return {'simple_output':simple_output, 'combine_output':output}

def compareCombineVsSimpleFakes( simple_output, combine_output , bins = [], draw=False):
    hist_prompt_subtract = degTools.makeHistoFromDict( {b :  simple_output[b]['obs-exp'] for b in bins}, bin_order = bins  )
    h, graph = degTools.makeAsymTGraphFromDict( "fakeEstsAsymErr", combine_output , bins , func = lambda ite, cen: ite[cen] )
    hist_prompt_subtract.GetXaxis().LabelsOption("V")
    hist_prompt_subtract.GetXaxis().SetLabelSize(0.02)
    
    hist_prompt_subtract.SetMarkerStyle(20)
    hist_prompt_subtract.SetMarkerSize(0)
    hist_prompt_subtract.SetFillColor(880)
    #hist_prompt_subtract.SetFillStyle(1)
    graph.SetMarkerStyle(20)
    if draw:
        hist_prompt_subtract.Draw("E2")
        graph.Draw("p")

    return hist_prompt_subtract, graph

if __name__ == '__main__':
    #neg_bins = ['vbcr1b', 'vbcr1bX', 'vbcr1bY', 'vbcr2bY', 'vbsr1hX', 'vbsr1ha', 'vbsr1haX', 'vbsr1haY', 'vbsr1hb', 'vbsr1hbX', 'vbsr1hbY', 'vbsr1ma', 'vbsr1maX', 'vbsr1mb', 'vbsr1mbX', 'vbsr1mbY', 'vbsr2hY', 'vbsr2haY', 'vbsr2hb', 'vbsr2hbX', 'vbsr2hbY', 'vbsr2maY', 'vbsr2vlbY', 'vbsr2vlcX']
    import ROOT

    prompt_fake_file = "/afs/hephy.at/user/n/nrad/public/share/fakeEstimate/example/prompt_fake_yields_example.pkl"
    #prompt_fake_yields =  fakeEstimateOutput['prompt_fake_yields']['lep']
    prompt_fake_yields =  pickle.load(file(prompt_fake_file)) 

    neg_bins = [ b for b in prompt_fake_yields.keys() if prompt_fake_yields[b]['Fakes'].val - prompt_fake_yields[b]['Fakes'].sigma <= 0 ] 
    #neg_bins.sort()

    all_bins = prompt_fake_yields.keys()
    #neg_bins = all_bins#[-30:]

    simple_output  =  {}
    nProc   =  20
    for b in neg_bins:
        bin_args = [ prompt_fake_yields[b]['__Data_X_TL'] , prompt_fake_yields[b]['__Prompts_X_TL'] , 1, b]
        #simple_output[b]={'obs':obs, 'exp': exp, 'obs-exp':obs-exp}
    limit_output = getFakeEstimateParal( prompt_fake_yields, bins = neg_bins, data_key = "__Data_X_TL", prompt_key="__Prompts_X_TL", nProc = 20 ) 



    hist_prompt_subtract = degTools.makeHistoFromDict( {b :  simple_output[b]['obs-exp'] for b in neg_bins}, bin_order = neg_bins  )
    h, graph = degTools.makeAsymTGraphFromDict( "fakeEsts", limit_output , neg_bins , func = lambda ite, cen: ite[cen] )
    hist_prompt_subtract.GetXaxis().LabelsOption("V")
    hist_prompt_subtract.GetXaxis().SetLabelSize(0.02)

    hist_prompt_subtract.SetMarkerStyle(20)
    hist_prompt_subtract.SetMarkerSize(0)
    hist_prompt_subtract.SetFillColor(880)
    #hist_prompt_subtract.SetFillStyle(1)
    hist_prompt_subtract.Draw("E2")
    graph.SetMarkerStyle(20)
    graph.Draw("p")

    #c1 = ROOT.TCanvas("c1","c1")
    #degTools.saveCanvas( c1, "
    #obs, exp, sig, bin_name = args
    #res = getFakeEstimateFromCombine( obs, exp, sig, bin_name )
    #output[b]={'limit': res, 'obs':obs, 'exp': exp, 'obs-exp':obs-exp}


        
