import sys
import Workspace.DegenerateStopAnalysis.tools.degTools as degTools
import pickle
import ROOT
import os
u_float = degTools.u_float 


def getPkl( pkl_path, def_dict={}):
    pkl_path = os.path.expandvars(pkl_path)
    print 'get pkl %s'%pkl_path
    if os.path.isfile( pkl_path):
        try:
            ret = pickle.load( open(pkl_path,'r') )

        except:
            print "Something wrong with the pickle file:\n %s \n Got this Error: \n %s"%(pkl_path, sys.exc_info()[0] )
            raise
    else:
        ret = deepcopy( def_dict )
        print "def", ret.keys()
    return ret


absSysFunc    = lambda a,b : (abs(1.- (b/a).val)   * 100) if a.val else 0
#SignedSysFunc = lambda a,b : ((-1.+ (b/a).val)   * 100) if a.val else 0
SignedSysFunc = lambda a,b : (((b-a)/a.val)   * 100) if a.val else u_float( 0 )
mean          = lambda l :   sum(l)/float(len(l)) if len(l) else None


def meanSys(*a):
    """assume first value is the central value"""
    central = a[0]
    variations = a[1:]
    if not variations:
        raise Exception("No Variations Given! %s"%a)
    systs = []
    for var in variations:
        systs.append( absSysFunc(central, var) )
    #print systs, mean(systs)
    return mean(systs)


def round_sig(x, sig=2):
    return round(x, sig - int(floor(log10(abs(x) )))-1) 


def meanSysSigned(*a): ### keep track of the signs somehow for systematics in cards
    """assume first value is the central value
    """
    central = a[0]
    variations = a[1:]
    if not variations:
        raise Exception("No Variations Given! %s"%a)
    systs = []
    sign = 1
    #signed_systs = []
    for var in variations:
        syst_val = sign*SignedSysFunc(central, var)
        #syst_val = SignedSysFunc(central, var) 
        systs.append( syst_val)
        #signed_systs.append( sign* syst_val ) 
        sign *= -1
    #print systs
    syst_sign = (sum(systs).val < 0)*(-1) + (sum(systs).val >= 0)*(1)
    syst_mean = mean([abs(x.val) for x in systs])
    stat_errs = mean(systs).sigma ## do we want to include stat error in syst?
    #return u_float( syst_sign * syst_mean, stat_errs)
    return syst_sign * syst_mean

getSysts = lambda *vals: [ meanSys(*vals) , meanSysSigned(*vals) ] 

def getBkgSysts(varYlds, varTypes, keys = []):
    assert varTypes[0]=='central'
    return { k:degTools.dict_manipulator( [varYlds[varType][k] for varType in varTypes], meanSysSigned ) for k in keys }
    #return degTools.dict_manipulator( [ bkgPreds[varType][bkg] for varType in varTypes], getSysts )


def getValFrom1BinnedHistOrGraph( hist ):
    if type(hist) in [ ROOT.TH1F , ROOT.TH1D ]:
        v = hist.GetBinContent(1)
        e = hist.GetBinError(1)
    if type(hist) in [ ROOT.TH2F , ROOT.TH2D ]:
        v = hist.GetBinContent(1,1)
        e = hist.GetBinError(1,1)
    if type(hist) in [ROOT.TGraphAsymmErrors]:
        v = hist.GetY()[0]
        el = hist.GetEYlow()[0]
        eh = hist.GetEYhigh()[0]
        e  = max(abs(el),abs(eh))
    return degTools.u_float(v,e)

def getPrePostFitFromMLF( mlfit ):
    shape_dirs = ['shapes_prefit', 'shapes_fit_b', 'shapes_fit_s']
    shape_hists = {}
    for shape_dir_name in shape_dirs:
        shape_dir = mlfit.Get(shape_dir_name)
        list_of_channels = [x.GetName() for x in shape_dir.GetListOfKeys() if x.IsFolder()]
        shape_hists[shape_dir_name] = {}
        for channel_name in list_of_channels:
            channel  = shape_dir.Get(channel_name)
            bin_name = channel_name.replace("ch1_","")
            list_of_hists = [x.GetName() for x in channel.GetListOfKeys() ]
            shape_hists[shape_dir_name][bin_name] = {}
            for hist in list_of_hists:
                shape_hists[shape_dir_name][bin_name][hist] = channel.Get(hist) 
    shape_results = degTools.dict_function( shape_hists, func = getValFrom1BinnedHistOrGraph )
    return {'hists':shape_hists, 'results':shape_results }


h_colors ={
                    "Total": ROOT.kBlack,
                    "WJets": ROOT.kGreen,
                    "Fakes": ROOT.kViolet,
                   "TTJets": ROOT.kAzure,
                   "Others": ROOT.kOrange,
                   'signal': ROOT.kRed,
                  }

uniqueHash = degTools.uniqueHash

def plotResults( result_dict , bkg_procs , data_tag = "data" , sig_tag = "signal" , bin_order=[], prefix="" , hist_colors = {} , hist_decors = {}):
    if not bin_order:
        bin_order = result_dict.keys()
    hists = {}
    for proc in bkg_procs + [ data_tag ] + [sig_tag] :
        hists[proc] = degTools.makeHistoFromDict( result_dict , name = prefix + proc +"_"+ uniqueHash() ,bin_order = bin_order , func = lambda x: x.get(proc, degTools.u_float(0)) )
        if hist_colors:
            if proc == data_tag:
                hists[proc].SetMarkerStyle(20)
                hists[proc].SetMarkerSize(0.9)
                hists[proc].SetLineColor(ROOT.kBlack)
                hists[proc].SetMarkerColor(ROOT.kBlack)
            elif proc == sig_tag  and proc in hist_colors :
                hists[proc].SetLineStyle(5)
                hists[proc].SetLineWidth(3)
                hists[proc].SetLineColor( hist_colors[proc] )
            elif proc in bkg_procs and proc in hist_colors:
                hists[proc].SetFillColor( hist_colors[proc])
                hists[proc].SetLineColor( hist_colors[proc])
            
        if proc in hist_decors:
            hist_decors[proc](hists[proc])

    stack = ROOT.THStack(prefix + "stack", prefix + "stack" )    
    for proc in bkg_procs:
        stack.Add(hists[proc])
    print "getting ratio"
    ratio = hists[data_tag].Clone( prefix + "ratio")
    total = stack.GetHists()[0].Clone(prefix + "total")
    total.Reset()
    total.Merge( stack.GetHists() )
    ratio.Divide( total ) 
    hists['ratio'] = ratio
    hists['total'] = total
    hists['stack'] = stack
    return hists




def getDataMCRatios( data_hist, mc_hist ):
    import array as ar
    efill = 3002
    
    if type(mc_hist) == ROOT.THStack :
        stack = mc_hist.Clone("stack"+uniqueHash())
        mc_hist = stack.GetHists().Last().Clone("mc_hist" + uniqueHash() )
        mc_hist.Reset()
        mc_hist.Merge( stack.GetHists() )
        

    unity = mc_hist.Clone( "IAmOne" +uniqueHash())
    unity.SetLineColor(1)
    unity.SetLineWidth(1)
    unity.SetFillColor(0)
    nBins = unity.GetNbinsX()
    mc_noe = mc_hist.Clone( "mc_noerror" + uniqueHash())
    #mc_noe.Sumw2(0)
    mc_noe.SetError(ar.array( "d",[0]*(nBins+1) ) ) 
    
    mc_e = mc_hist.Clone( "mc_error" + uniqueHash())
    mc_e.Divide(mc_noe)
    mc_e.SetFillStyle(efill)
    mc_e.SetFillColor(1)
    mc_e.SetMarkerSize(0)

    for ib in range( nBins+1 ):
        unity.SetBinContent(ib, 1)
        unity.SetBinError(ib, 0)

    data_ratio = data_hist.Clone( "data_ratio" + uniqueHash() )
    data_ratio.Divide( mc_noe )

    mc_eb = mc_hist.Clone("mc_errorbar" + uniqueHash())
    mc_eb.SetFillStyle( efill )
    mc_eb.SetMarkerSize(0)
    mc_eb.SetFillColor(ROOT.kBlue-5)

    return data_ratio, mc_e, mc_eb , unity, mc_noe


def testdivide(mc_hist):
    import array as ar
    nBins = mc_hist.GetNbinsX()
    mc_noe = mc_hist.Clone( "mc_noerror" + uniqueHash())
    mc_noe.SetError(ar.array( "d",[0]*(nBins+1) ) )
    mc_e = mc_hist.Clone( "mc_error" + uniqueHash())
    mc_e.Divide(mc_noe)
    lb = mc_noe.GetBinError( nBins)
    if lb>100000:
        return mc_e
    else:
        return  True



def drawCMSHeader( preliminary = "Preliminary", lumi = 35.9, lxy = [0.16,0.91], rxy=[0.77,0.91]):
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.04)
    font=22
    latex.SetTextFont(font)
    #latexTextL = "#font[%s]{CMS %s}"%(font, preliminary)
    latexTextL = "CMS %s"%(preliminary)
    latexTextR = "\\mathrm{%0.1f\, fb^{-1} (13\, TeV)}"%(lumi)
    latex.DrawLatex(lxy[0],lxy[1],  latexTextL)
    latex.DrawLatex(rxy[0],rxy[1],  latexTextR)


def drawNiceDataPlot( data_hist, mc_stack, sig_stack = None , options={} , saveDir = "./" , name = "plot"):
    canv = []
    ratios = [] 
    uq    = name+"_"+uniqueHash()
    print uq
    canv  = degTools.makeCanvasMultiPads( uq , 800,800, pads=[], padRatios =[2,1] )
    print canv
    canv[1].cd()
    setLogY = options.get('logy',1)
    canv[1].SetLogy( setLogY )
    ratios = getDataMCRatios( data_hist  , mc_stack )
    data_ratio , mc_e, mc_eb, unity, mc_noe = ratios
    ymax = max( degTools.getHistMax( mc_noe )[1] , degTools.getHistMax( data_hist )[1] )
    mc_stack.Draw("hist")
    mc_stack.SetMaximum(ymax* ( 1.5 + 15*setLogY) )
    mc_eb.Draw("E2same")
    mc_e.Print("all")
    data_hist.Draw("same")
    if sig_stack:
        sig_stack.Draw("same hist")

    drawCMSHeader()
    canv[2].cd()
    unity.Draw()
    mc_e.Draw("E2same")
    unity.GetYaxis().SetLabelSize( unity.GetYaxis().GetLabelSize()*2)
    unity.SetNdivisions(505, "y")
    unity.GetXaxis().SetLabelSize(0.12)
    mc_e.Draw("E2same")
    data_ratio.Draw("same")
    data_ratio.SetMaximum(2)
    data_ratio.SetMinimum(0)
    degTools.saveCanvas( canv[0], saveDir , name)
    return canv, ratios

def getSFsFromPostPreFitPlots( plots , plotDir , saveDir , bins = [] , keys = [ 'WJets', 'TTJets', 'Fakes', 'stack' ] , name = "PostPre", hist_colors=h_colors) :
    plot_values = degTools.dict_function( plots, lambda x: degTools.getTH1FbinContent( x )  ) #if type( x ) in [ ROOT.TH1F , ROOT.TH2F] else None ) 
    #SFs = {'WJets':{}, 'TTJets':{} , 'Fakes':{} , 'stack':{}}
    SFs = {k:{} for k in keys}
    SF_hists = degTools.deepcopy(SFs)
    canv_sfs = ROOT.TCanvas( "SFs", "SFs", 1000,800 )
    dOpt = 'hist text'
    ROOT.gStyle.SetPaintTextFormat("0.2f")
    for bkg in SFs:
        SFs[bkg]      = degTools.dict_manipulator( [ plot_values[f][bkg] for f in ['fit_b', 'prefit' ] ] ,  lambda a,b: a/b if b else 1.0)
        SF_hists[bkg] = degTools.makeHistoFromDict( SFs[bkg], bin_order = bins, name = "TF_%s"%bkg)
        SF_hists[bkg].GetXaxis().SetLabelSize(0.05)
        SF_hists[bkg].SetLineColor( hist_colors[bkg] )
        SF_hists[bkg].SetMarkerColor( hist_colors[bkg] )
        SF_hists[bkg].Draw(dOpt)
        SF_hists[bkg].SetMinimum(0.65)
        SF_hists[bkg].SetMaximum(1.7)
        dOpt='same text'
    #output_name = name.replace(".pkl", "_SFs.pkl")
    name = name if name.endswith(".pkl") else "%s.pkl"%name
    degTools.pickle.dump( SFs, file('%s/%s'%(saveDir, name) , 'w') )
    degTools.saveCanvas( canv_sfs, plotDir, name.replace(".pkl","") )
    return SFs



class MaxLikelihoodResult():
    """
        Runs the MLF, starting from card to the post/pre plots
        input bins will be masked , i.e. for CR only fit
    """
    fits = ['prefit', 'fit_b', 'fit_s']
    
    h_colors ={
                "Total": ROOT.kBlack,
                "stack": ROOT.kBlack,
                "WJets": ROOT.kGreen,
                "Fakes": ROOT.kViolet,
               "TTJets": ROOT.kAzure,
               "Others": ROOT.kOrange,
               "signal": ROOT.kRed,
              }


    def __init__(self, mlf_file , bins  , plotDir ="./", saveDir = "./", output_name = "mlf_output.pkl" , hist_colors = h_colors, fits = fits , rerun=True):

        sr_bins = [ b for b in bins if 'sr' in b ] 
        cr_bins = [ b for b in bins if 'cr' in b ] 

        if mlf_file.endswith(".root"):
            pass
        if mlf_file.endswith(".txt"):
            card = mlf_file[:]
            import Workspace.DegenerateStopAnalysis.tools.limitTools as limitTools
            mlf_basename = card.replace(".txt","_mlf.root")
            mlf_file     = mlf_basename.replace("_mlf.root", "_mlf_SRMasked.root")
            if rerun or not os.path.isfile(mlf_file):
                print '\n Running MLF on %s , the output will be %s \n '%(card, mlf_file) 
                limitTools.runMLF( card , mlf_basename , bins = sr_bins ) 
        print mlf_file
        if not os.path.isfile( mlf_file):
            raise Exception(" File not found : %s"%mlf_file )
        self.mlfit         = ROOT.TFile(mlf_file)
        self.mlf_out       = getPrePostFitFromMLF( self.mlfit )
        self.mlf_results   = self.mlf_out['results']
        self.file_basename = degTools.get_filename( mlf_file )

        degTools.makeDir( saveDir)
        degTools.makeDir( plotDir)
        pickle.dump( self.mlf_results , file(saveDir + "/" + output_name , "w")) 
    
        plots   = {}
        self.plots = plots 


        hists      = {}
        hists_crs  = {}
        plots      = {}
        degTools.makeDir(saveDir)
        degTools.makeDir(plotDir)

        drawCRs = False
        for fit in fits : 
            hists[fit] = plotResults(    
                                        self.mlf_results['shapes_%s'%fit] , list( reversed( ["WJets", "TTJets", "Fakes","Others"] )) , 
                                        bin_order = sr_bins + cr_bins   , 
                                        prefix = fit                    ,   
                                        hist_colors = hist_colors          ,
                                    )
            if drawCRs:
                ROOT.gStyle.SetPaintTextFormat("0.2f") 
                hists_crs[fit] = plotResults(    
                                            self.mlf_results['shapes_%s'%fit] , list( reversed( ["WJets", "TTJets", "Fakes","Others"] )) , 
                                            bin_order = cr_bins   , 
                                            prefix = fit                    ,   
                                            hist_colors = hist_colors          ,
                                        )
                stack = hists_crs[fit]['stack']
                hsh = degTools.uniqueHash()
                normalized_stack = degTools.normalizeStack( stack ) 
                canv = ROOT.TCanvas( "Canv_%s_%s"%(fit, hsh), "Canv_%s_%s"%(fit, hsh), 1000, 800)
                normalized_stack.Draw("hist text0")
                degTools.saveCanvas( canv, plotDir, "CRsComposition_%s"%fit ) 
                
                stack.Draw("hist text0")
                canv.SetLogy(1)
                degTools.saveCanvas( canv, plotDir, "CRs_%s"%fit ) 

            #canvs[fit] = degTools.makeCanvasMultiPads( fit, 800,800, pads=[], padRatios =[2,1] )
            print 'got hists %s'%fit
            plots[fit] = drawNiceDataPlot( 
                                            data_hist = hists[fit]['data'] , 
                                            mc_stack  = hists[fit]['stack'] , 
                                            sig_stack = hists[fit]['signal'] , 
                                            options   = {'logy':1} , 
                                            saveDir   = plotDir           , 
                                            name      = fit , 
                                         )
            print 'made plots %s'%fit
        sf_output_file = output_name.replace(".pkl","_SFs.pkl") 
        self.SFs = getSFsFromPostPreFitPlots( hists , plotDir, saveDir , bins = bins , hist_colors = hist_colors, name = sf_output_file  )  

        self.hists = hists
        self.plots = plots



CR_SF_map={
 #'presel': None 
 'sr1a'  :  'cr1a'  , 
 'sr1la' :  'cr1a'  , 
 'sr1ma' :  'cr1a'  , 
 'sr1ha' :  'cr1a'  , 
 'sr1b'  :  'cr1b'  ,
 'sr1lb' :  'cr1b'  ,
 'sr1mb' :  'cr1b'  ,
 'sr1hb' :  'cr1b'  ,
 'sr1c'  :  'cr1c'  ,
 'sr1lc' :  'cr1c'  ,
 'sr1mc' :  'cr1c'  ,
 'sr1hc' :  'cr1c'  ,
 'sr2'   :  'cr2'  ,
 'sr2l'  :  'cr2'  ,
 'sr2m'  :  'cr2'  ,
 'sr2h'  :  'cr2'  ,
 'cr1a'  :  'cr1a'  , 
 'cr1b'  :  'cr1b'  ,
 'cr1c'  :  'cr1b'  , 
 'cr2'   :  'cr1b'  , 
 'crtt'  :  'crtt'  ,
 }

TransferFactorMap ={

    "WJets": 
            { 
                 'sr1a'  :  'cr1a'  ,
                 'sr1la' :  'cr1a'  ,
                 'sr1ma' :  'cr1a'  ,
                 'sr1ha' :  'cr1a'  ,
                 'sr1b'  :  'cr1b'  ,
                 'sr1lb' :  'cr1b'  ,
                 'sr1mb' :  'cr1b'  ,
                 'sr1hb' :  'cr1b'  ,
                 'sr1c'  :  'cr1c'  ,
                 'sr1lc' :  'cr1c'  ,
                 'sr1mc' :  'cr1c'  ,
                 'sr1hc' :  'cr1c'  ,
                 'sr2'   :  'cr2'  ,
                 'sr2l'  :  'cr2'  ,
                 'sr2m'  :  'cr2'  ,
                 'sr2h'  :  'cr2'  ,
                 'cr1a'  :  'cr1a'  , 
                 'cr1b'  :  'cr1b'  ,
                 'cr1c'  :  'cr1b'  , 
                 'cr2'   :  'cr2'  , 
            },
    "TTJets":
            { 
                 'sr1a'  :  'crtt'  ,
                 'sr1la' :  'crtt'  ,
                 'sr1ma' :  'crtt'  ,
                 'sr1ha' :  'crtt'  ,
                 'sr1b'  :  'crtt'  ,
                 'sr1lb' :  'crtt'  ,
                 'sr1mb' :  'crtt'  ,
                 'sr1hb' :  'crtt'  ,
                 'sr1c'  :  'crtt'  ,
                 'sr1lc' :  'crtt'  ,
                 'sr1mc' :  'crtt'  ,
                 'sr1hc' :  'crtt'  ,
                 'sr2'   :  'crtt'  ,
                 'sr2l'  :  'crtt'  ,
                 'sr2m'  :  'crtt'  ,
                 'sr2h'  :  'crtt'  ,
                 'cr1a'  :  'crtt'  , 
                 'cr1b'  :  'crtt'  ,
                 'cr1c'  :  'crtt'  , 
                 'cr2'   :  'crtt'  , 
                 'crtt'  :  'crtt'  , 
            },

        }



def applySFsToYields( yldInst, SFs, TF_Map=TransferFactorMap, bkgList = None, bins = None):
    
    bkgYldsOrig = {}
    bkgEst      = {}

    for bkg in bkgList:
        bkgYldsOrig[bkg] = {}
        bkgEst[bkg]      = {}
        applyTF = bkg in TF_Map
        for b in bins:
            v = yldInst[bkg][b]
            sf = 1
            if applyTF:
                transferFrom = TF_Map[bkg].get(b)
                if transferFrom : 
                    sf  = SFs[transferFrom][bkg]
                    print bkg, b, sf
            bkgYldsOrig[bkg][b] = v 
            bkgEst[bkg][b]        = v*sf

    return bkgYldsOrig, bkgEst


if __name__ == '__main__':
    pass
