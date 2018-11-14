from Workspace.DegenerateStopAnalysis.tools.sysTools import *
from Workspace.DegenerateStopAnalysis.tools.degTools import *
from Workspace.HEPHYPythonTools.xsecSMS import stop13TeV_NLONLL as xsecT2tt
import pickle
yld     = pickle.load(file("/afs/hephy.at/work/n/nrad/results/cards_and_limits//13TeV/8025_mAODv2_v7/80X_postProcessing_v1/EPS17_v0/June17_v4/LepGood_lep_lowpt_Jet_def_SF_Prompt_STXSECFIX_PU_TTIsr_Wpt_TrigEff_lepSFFix/DataBlind/presel_base/Yields_35855pbm1_EPS17_v0_June17_v4_LepGood_lep_lowpt_Jet_def_SF_Prompt_STXSECFIX_PU_TTIsr_Wpt_TrigEff_lepSFFix_presel_base_bins_mtct_sum_sig.pkl"))
#effmap  = yld.getSignalYieldMap()
lumi = 35854.9
effmap_, yldmap_  = yld.getSignalEffMap( xsecT2tt , 35854.9) 


yldmaps = getSignalYieldMap( yld.getByBins( yld.yieldDict ), yld.sigList , models_info=modelsInfo['T2tt'])[0]
effmaps = {}

models = yldmaps.keys()
#models = ['t2bw']

for model in models:
    effmaps[model]={}
    for b in yldmaps[model].keys():
        effmaps[model][b] = {}
        for mstop in yldmaps[model][b].keys():
            xsec_lumi = xsecT2tt[mstop] * lumi
            effmaps[model][b][mstop] = dict_function( yldmaps[model][b][mstop] , lambda v: v*1./xsec_lumi)

#effmap_dm, yldmap_dm = map( sysTools.transformMassDict , [effmap, yldmap])

#plotDir = "/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/8025_mAODv2_v7/80X_postProcessing_v1/EPS17_v0/June17_v4_/LepGood_lep_lowpt_Jet_def_SF_Prompt_STXSECFIX_PU_TTIsr_Wpt_TrigEff_lepSFFix/DataBlind"
plotDir = "/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/8025_mAODv2_v7/80X_postProcessing_v1/EPS17_v0/June17_v4_VVNLO_v2/LepGood_lep_lowpt_Jet_def_SF_Prompt_STXSECFIX_PU_TTIsr_Wpt_TrigEff_lepSFFix/DataBlind/EffMaps/"
#plotDir = cfg.saveDir

effmap = {}
yldmap = {}

ROOT.gStyle.SetPalette(ROOT.kViridis)
#ROOT.gStyle.SetPalette( ROOT.kInvertedDarkBodyRadiator )

model_names = {
                't2tt':'T2tt',
                't2bw':'T2bW',
              }

model_procs = {
                't2bw': {'proc':  "pp #rightarrow #tilde{t} #tilde{t}, #tilde{t} #rightarrow #tilde{#chi}^{#pm}_{1} b, #tilde{#chi}^{#pm}_{1} #rightarrow f f' #tilde{#chi}^{0}_{1}",
                         #'extra': "m(#tilde{#chi}^{#pm}_{1})=0.5*(m(#tilde{t})+m(#tilde{#chi}^{0}_{1}))",
                         'extra': "m_{#tilde{#chi}^{#pm}_{1}}=(m_{#tilde{t}}+m_{#tilde{#chi}^{0}_{1}})/2" 
                        },
                't2tt':{'proc': "pp #rightarrow #tilde{t} #tilde{t}, #tilde{t} #rightarrow b f f' #tilde{#chi}^{0}_{1}"}
             }




hists = {}

canv = ROOT.TCanvas()
ROOT.gPad.SetLogz(1)
ROOT.gPad.SetRightMargin(0.15)

def niceRegionName(r):
    ret = r.replace("sr","SR").replace("cr","CR").replace("vl","VL").replace("l","L").replace("v","V").replace("h","H").replace("m","M")
    return ret


regions = ['sr1vlaX', 'sr1laX', 'sr1maX', 'sr1haX', 'sr1vlaY', 'sr1laY', 'sr1maY', 'sr1haY', 'sr1vlbX', 'sr1lbX', 'sr1mbX', 'sr1hbX', 'sr1vlbY', 'sr1lbY', 'sr1mbY', 'sr1hbY', 'sr1lcX', 'sr1mcX', 'sr1hcX', 'sr1lcY', 'sr1mcY', 'sr1hcY', 'sr2vlaX', 'sr2laX', 'sr2maX', 'sr2haX', 'sr2vlaY', 'sr2laY', 'sr2maY', 'sr2haY', 'sr2vlbX', 'sr2lbX', 'sr2mbX', 'sr2hbX', 'sr2vlbY', 'sr2lbY', 'sr2mbY', 'sr2hbY', 'sr2lcX', 'sr2mcX', 'sr2hcX', 'sr2lcY', 'sr2mcY', 'sr2hcY', 'cr1aX', 'cr1aY', 'cr1bX', 'cr1bY', 'cr1cX', 'cr1cY', 'cr2aX', 'cr2aY', 'cr2bX', 'cr2bY', 'cr2cX', 'cr2cY']
ytitle = "#Deltam(#tilde{t},#tilde{#chi}^{0}_{1}) [GeV]"
binning = sigModelBinnings['T2tt_DM']
binning = [23, 237.5, 812.5, 10, 5, 105]


for model in models:
    effmap[model] = {}
    yldmap[model] = {}
    hists[model]  = {}
    modelname = model_names[model]
    modelInfo = modelsInfo[modelname]
    for k in effmaps[model].keys():
        effmap[model][k] = transformMassDict( effmaps[model][k] )
        yldmap[model][k] = transformMassDict( yldmaps[model][k] )
    
    MINVAL = 1E-6
    for k in effmaps[model].keys():
        p_tmp = makeStopLSPPlot( k, effmap[model][k], k , bins = binning , xtitle= modelInfo['xtitle'], ytitle= ytitle )
        p = th2Func2( p_tmp, lambda x,y,bc: bc if bc and bc>MINVAL else (MINVAL*1.9 if y<8 and x<23 else bc) ) # fill empty bins with small value
        #p.GetZaxis().SetRangeUser(0,10)
        p.GetZaxis().SetRangeUser(MINVAL,1E-3)
        #p.SetNdivisions(420,'z')
        p.SetNdivisions(10,'z')
        #p.SetMarkerSize(1)
        p.SetMarkerStyle(22)
        if 'presel' in k:
            p.GetZaxis().SetRangeUser(MINVAL,0.05)
            p.SetNdivisions(10,'z')
            
        p.GetZaxis().SetLabelSize(0.04)
        #pal = p.GetListOfFunctions().FindObject("palette") 
        p.Draw("COL")
        p.Draw("Zsame")
        drawCMSHeader("Simulation Preliminary", lxy=[0.16, 0.957], rxy=[0.66, 0.957], textR="#sqrt{s} = 13 TeV", cmsinside=False )
        #drawLatex("Accp.*Eff. : %s" % (model_names[model], niceRegionName(k)) , 0.2, 0.87, 42 ,0.03)
        drawLatex( "Accp.*Eff. in {:<15} ".format( niceRegionName(k) ) , 0.2, 0.89, 42 ,0.04)
        drawLatex( model_procs[model].get('extra')    , 0.58, 0.89, 42 ,0.04)
        drawLatex( model_procs[model]['proc']    , 0.2, 0.815, 42 ,0.04)
        saveCanvas( ROOT.gPad, plotDir + "/Plots/%s"%model_names[model], k)
        hists[model][k]=p


srplots = []
for model in models:
    modelname = model_names[model]
    f = ROOT.TFile( plotDir +"/AccpEffMap_%s.root"%modelname, "RECREATE") 
    for region in regions:
        if not 'sr' in region: continue
        #hists[model][region].SetDirectory(0)
        srplots.append( plotDir + "/Plots/%s"%model_names[model] +"/extras/%s.pdf"%region )
        hists[model][region].Write()
    f.Close()
        

pdfdirs = "/afs/hephy.at/work/n/nrad/CMSSW/CMSSW_8_0_20/src/Workspace/DegenerateStopAnalysis/python/scripts/pdf/effmaps"
for srplt in srplots:
    model = srplt.rsplit("/")[-3]
    r     = srplt.rsplit("/")[-1]
    newpath = pdfdirs +"/%s_%s"%(model, r)
    command = "cp %s %s"%(srplt, newpath)
    os.system(command)


frametemplate=\
r"""
%%
\begin{frame}{Acceptance * Efficiency Map:  %(nr)s}
\begin{figure}
\begin{center}
\subfigure{\includegraphics[width=0.49\textwidth]{effmaps/T2tt_%(r)s.pdf}} \hfil
\subfigure{\includegraphics[width=0.49\textwidth]{effmaps/T2bW_%(r)s.pdf}} \hfil
\end{center}
\end{figure}
\end{frame}

"""

frames = """  """
for r in regions:
    if not 'sr' in r: continue
    frames += frametemplate%{'r':r, 'nr':niceRegionName(r)}
f=file('/afs/hephy.at/work/n/nrad/CMSSW/CMSSW_8_0_20/src/Workspace/DegenerateStopAnalysis/python/scripts/pdf/frames.tex','w')
f.write(frames)
f.close()
