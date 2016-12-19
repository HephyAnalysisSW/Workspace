from Workspace.DegenerateStopAnalysis.tools.degTools import *
from Workspace.DegenerateStopAnalysis.tools.limitTools2 import *

from Workspace.DegenerateStopAnalysis.tools.CombineCard import CombinedCard

import copy


saveDir = "/afs/hephy.at/user/n/nrad/www/validations/lowPtThreshold_v5/"

setup_style() 
#ylds_def_file = "/afs/hephy.at/work/n/nrad/results/cards_and_limits/8020_mAODv2_v0/80X_postProcessing_v0/13TeV/HT/Moriond17_v1_Mt95_Inccharge_LepGood_lep_def_Jet_def_SF/AdjustedSys/presel/Yields_12864pbm1_Moriond17_v1_Mt95_Inccharge_LepGood_lep_def_Jet_def_SF_presel_bins_sum.pkl"
ylds_def_file = "/afs/hephy.at/work/n/nrad/results/cards_and_limits/8020_mAODv2_v0/80X_postProcessing_v0/13TeV/HT/Moriond17_v2_Mt95_Inccharge_LepGood_lep_def_Jet_def_SF/AdjustedSys/presel/Yields_12864pbm1_Moriond17_v2_Mt95_Inccharge_LepGood_lep_def_Jet_def_SF_presel_bins_sum.pkl"
ylds_lowpt_file  = "/afs/hephy.at/work/n/nrad/results/cards_and_limits/8020_mAODv2_v0/80X_postProcessing_v0/13TeV/HT/Moriond17_v2_Mt95_Inccharge_LepGood_lep_lowpt_Jet_lowpt_SF/AdjustedSys/presel/Yields_12864pbm1_Moriond17_v2_Mt95_Inccharge_LepGood_lep_lowpt_Jet_lowpt_SF_presel_bins_sum.pkl"

ylds={}
ylds['def'] = pickle.load(file(ylds_def_file))
ylds['lowpt'] = pickle.load(file(ylds_lowpt_file))

def getYieldMaps(ylds, sigList):
        yld_mass_map = {}
        for cut_name in ylds.cutNames:
            yieldDict = ylds.getByBin(cut_name)
            yld_mass_map[cut_name] = {}
            for sig in sigList:
                yld_value = yieldDict[sig]
                mstop, mlsp = getMasses(sig)
                set_dict_key_val( yld_mass_map[cut_name], mstop, {} )
                set_dict_key_val( yld_mass_map[cut_name][mstop] , mlsp, yld_value)
        return yld_mass_map


bkgNames = {
      'DYJetsM50'  :     'dy'       ,
     'QCD'         :     'qcd'         ,
      'TTJets'     :     'tt'       ,
       'WJets'     :     'w'         ,
       'ZJetsInv'  :     'z'     , 
       'ST'        :     'st'           , 
       'Diboson'        :     'vv'          ,
}


newoldmap={
 'sr1la':'SRL1a',
 'sr1ma':'SRH1a',
 'sr1ha':'SRV1a',
 'sr1lb':'SRL1b',
 'sr1mb':'SRH1b',
 'sr1hb':'SRV1b',
 'sr1lc':'SRL1c',
 'sr1mc':'SRH1c',
 'sr1hc':'SRV1c',
 'sr2l' :'SRL2',
 'sr2m' :'SRH2',
 'sr2h' :'SRV2',
 'sr1a' :'SR1a',
 'sr1b' :'SR1b',
 'sr1c' :'SR1c',
 'sr2'  :'SR2',
 'cr1a'  :'CR1a',
 'cr1b' :'CR1b',
 'cr1c' :'CR1c',
 'cr2'  :'CR2',
 'crtt' :'CRTT2',
}
oldnewmap={}
for new, old in newoldmap.items():
    oldnewmap[old]=new

maps={}
sigtypes = [ 't2ttold', 't2tt', 't2bw' ] 
sigLists = {}

for sigtype in sigtypes:
    sigLists[sigtype] = [ x for x in ylds['lowpt'].sigList if sigtype == x[:-7]]

for thresh, yld in ylds.items():
    fullSigList = yld.sigList
    maps[thresh]={}
    for sigtype in sigtypes:
        #sigList = [ x for x in fullSigList if sigtype == x[:-7]]
        maps[thresh][sigtype] = getYieldMaps(yld, sigLists[sigtype])



bins = [23, 237.5, 812.5, 62, 167.5, 792.5]
cutNames = yld.cutNames
plts={}
for thresh in ylds:
    plts[thresh] = {}
    for sigtype in sigtypes:
        plts[thresh][sigtype]={}
        for cutName in cutNames:
            plts[thresh][sigtype][cutName] =  makeStopLSPPlot( sigtype +"_"+cutName + "_" + thresh, maps[thresh][sigtype][cutName] , key = lambda x: x.val ,bins = bins)

##
## getting the syst dict and changing names to new names
##
syst_dict_pickle = "/afs/hephy.at/user/n/nrad/CMSSW/CMSSW_8_0_11/src/Workspace/DegenerateStopAnalysis/results/2016/8012_mAODv2_v3/80X_postProcessing_v10//ApprovalSys_Mt95_Inccharge_LepAll_lep_pu_SF/SystDictForCards.pkl"
syst_dict_old = pickle.load(file(syst_dict_pickle))
syst_dict = copy.deepcopy(syst_dict_old)
#sigtype = "t2ttold"


uncorr_systs = ['WPtShape','ttPtShape', 'ZInvEst', 'QCDEst',   'DYJetsM50XSec', 'DibosonXSec', 'STXSec']
for syst in uncorr_systs:
    syst_dict[syst]['uncorr']=True

uncert_dict = {}

bins_order =  [ 'sr1la', 'sr1ma', 'sr1ha', 'sr1lb', 'sr1mb', 'sr1hb',  'sr1lc', 'sr1mc', 'sr1hc', 'sr2l', 'sr2m', 'sr2h', 'cr1a', 'cr1b', 'cr1c', 'cr2', 'crtt']


def makeCard(yld, sig, syst_dict):
    bkgList =  ['w','tt','qcd', 'z', 'dy', 'st','vv' ]
    cfw=CombinedCard(niceProcessNames = {bkg:yld.sampleNames[bkg] for bkg in yld.bkgList} ); 
    cfw.addBins(bkgList , bins_order )

    cfw.specifyObservations( yld.yieldDictFull , obsProcess="dblind")
    cfw.specifyBackgroundExpectations(yld.yieldDictFull, bkgList )
    cfw.specifySignalExpectations( yld.yieldDictFull, sig)
    cfw.specifyUncertaintiesFromDict( syst_dict, uncerts = ['PU', 'jer', 'jec',  'WPt', 'ttpt','BTag_b', 'BTag_l', 'WPol'] , processes=[yld.sampleNames[bkg] for bkg in yld.bkgList])
    cfw.addUncertainty        ( "lepEff"   ,"lnN") 
    cfw.specifyFlatUncertainty( "lepEff"   , 1.05 , bins = [b for b in cfw.bins if "sr" not in b]  ) 

    cfw.specifyUncertaintiesFromDict( syst_dict, uncerts = ['PU', 'jer', 'jec', 'ISR', 'met', 'BTag_b', 'BTag_l', 'BTag_FS', "Q2" ] , processes=['signal'],prefix="SIG")

    cfw.addUncertainty        ( "cr1a_corr","lnN")
    cfw.specifyFlatUncertainty( "cr1a_corr",  2, bins=['cr1a','sr1la', 'sr1ma', 'sr1ha'], processes=['WJets'])
    cfw.addUncertainty        ( "cr1b_corr","lnN")
    cfw.specifyFlatUncertainty( "cr1b_corr",  2, bins=['cr1b','sr1lb', 'sr1mb', 'sr1hb'], processes=['WJets'])
    cfw.addUncertainty        ( "cr1c_corr","lnN")
    cfw.specifyFlatUncertainty( "cr1c_corr",  2, bins=['cr1c','sr1lc', 'sr1mc', 'sr1hc'], processes=['WJets'])
    cfw.addUncertainty        ( "cr2_corr","lnN")
    cfw.specifyFlatUncertainty( "cr2_corr",  2,  bins=['cr2' ,'sr2l' , 'sr2m' , 'sr2h'], processes=['WJets'])
    cfw.addUncertainty        ( "crtt_corr","lnN")
    cfw.specifyFlatUncertainty( "crtt_corr",  2, bins=[], processes=['TTJets'])

    uncorr_proc_systs =[ ['WJets'    ,   'WPtShape'     ], 
                         ['TTJets'   ,   'ttPtShape'    ], 
                         ['ZJetsInv' ,   'ZInvEst'      ], 
                         ['QCD'      ,   'QCDEst'       ], 
                         ['DYJetsM50',   'DYJetsM50XSec'],
                         ['Diboson'  ,   'DibosonXSec'  ],
                         [ 'ST'      ,   'STXSec'       ],         
                       ]
    for proc, syst_name in uncorr_proc_systs:
        cfw.specifyUncertaintiesFromDict( syst_dict, uncerts = [syst_name] , processes=[proc])


    cfw.addStatisticalUncertainties(yieldDict=yld.yieldDictFull )

    return cfw 

syst_dicts = {}
for sigtype in sigtypes:
    syst_dicts[sigtype] = copy.deepcopy( syst_dict  )
    for systname in syst_dicts[sigtype].keys():
        syst = syst_dicts[sigtype][systname]['bins']
        for b in syst.keys():
            bname = oldnewmap[b] if b in oldnewmap else b
            syst[bname] = syst.pop(b)
            for proc in syst[bname]:
                masses = getMasses(proc) 
                #masses = getMasses2(proc) if getMasses2(proc)  else getMasses2(proc) 
                #if not masses:
                #    try:
                #        print "didnt work", masses, proc
                #        masses= getMasses(proc)
                #        print "maybe now..", masses
                #    except:
                #        pass
                if masses:
                    oldproc = proc
                    proc = sigtype+"%s_%s"%(masses[0],masses[1])
                    syst[bname][proc] = syst[bname].pop(oldproc)
                    #if proc == 't2ttold325_255':
                    #    print syst[bname][proc]
                    #    assert False, [proc, masses]
                    print ("{:^20}"*4).format( proc , oldproc , "==>", proc)
                elif proc in bkgNames:
                    oldproc = proc
                    proc = bkgNames[proc]
                    syst[bname][proc] = syst[bname].pop(oldproc) 
                else:
                    pass
                    #print proc 
    
    for thresh, yld in  ylds.items():
        limitDir = saveDir +"/Limits/%s/%s/"%(sigtype,thresh)
        makeDir(limitDir)
        for signame in sigLists[sigtype]:
            #getLimit(yld, sig=signame, outDir =limitDir, postfix="_"+thresh, calc_limit=False , sys_pkl = syst_dicts[sigtype], data='dblind', bins_order = bins_order)       
            cfw = makeCard(yld, signame, syst_dicts[sigtype] ) 
            cfw.writeToFile(limitDir+"/%s_%s.txt"%(signame,thresh))
            #if not signame in syst_dicts[sigtype]['met']['bins']['sr1la']:
            #    assert False, signame
            #    pass
            print "----------------------- card written:", limitDir+"/%s_%s.txt"%(signame,thresh)
print "\n\n"
for sigtype in sigtypes:
    print "------", sigtype
    for thresh in ylds.keys():
        print "  ", thresh
        print "./calc_cards_limit.py '{saveDir}/Limits/{sigtype}/{thresh}/{sigtype}*.txt'  {saveDir}/Limits/{sigtype}_{thresh}.pkl".format(saveDir=saveDir, sigtype=sigtype, thresh=thresh)
    print "\n"    

print "### To Draw"
print "from Workspace.DegenerateStopAnalysis.tools.limitTools import drawExclusionLimit"
plotDir = saveDir +"/LimitPlots/" 
print "bins = [15, 237.5, 612.5, 42, 167.5, 592.5]"
for sigtype in sigtypes:
    for thresh in ylds.keys():
        pkl_path = "{saveDir}/Limits/{sigtype}_{thresh}.pkl".format(saveDir=saveDir, sigtype=sigtype, thresh=thresh)
        plot_path = "{plotDir}/{sigtype}/{thresh}.png".format( plotDir=plotDir , sigtype = sigtype , thresh = thresh )
        print "drawExpectedLimit( '{pkl_path}' , '{plot_path}' , bins=bins)".format( plot_path = plot_path , pkl_path=pkl_path )
    #        break
    #    break
    #break
#


#execfile("../tools/CombineCard.py"); 

sig_legs = {
             't2ttold':'T2tt(mWMin5)',
             't2tt'   :'T2tt(mWMin0.1)',
             't2bw'   :'T2bw(mWMin0.1)',
             's'      :'T2tt(mWMin5) OldPP',
            }





makePlots = False
if makePlots:

    ratios = {}
    saveDirs = {}
    for sigtype in sigtypes:
        ratioDir = saveDir + "/%s/signalRatios/"%sigtype
        yieldDir = saveDir + "/%s/signalYields/"%sigtype
        diffDir  = saveDir + "/%s/signalDiff/"%sigtype
        makeDir(ratioDir)
        makeDir(yieldDir)
        makeDir(diffDir)
        saveDirs[sigtype]={ 'ratio':ratioDir, 'yield':yieldDir, 'diff':diffDir}


    c1= ROOT.TCanvas("c1","c1", 2100,1400)
    ROOT.gStyle.SetPaintTextFormat("0.2f")
    
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.038)
    
    ratios = {}
    nom = 'lowpt'
    denom = 'def'
    
    unity = plts[nom][sigtype]['presel'].Clone("unity")
    unity.Divide(unity)
    #unity100 = unity.Clone("unity100")
    #unity.Multiply(100)
    for sigtype in sigtypes:
        ratios[sigtype] = {}
        for b in plts[nom][sigtype].keys():
            nomplt = plts[nom][sigtype][b].Clone()
            ratioplt = nomplt.Clone()
            denomplt = plts[denom][sigtype][b]
            ratioplt.Divide(denomplt)
            ratioplt.Draw("COLZ TEXT")
    
            ratios[sigtype][b] = ratioplt
            latex.DrawLatex(0.2,0.7, "#frac{%s}{%s}    %s "%(nom, denom, sig_legs[sigtype]) +"   %s"%b.upper())
            c1.SaveAs(saveDirs[sigtype]['ratio'] +"/%s.png"%b)
    
            nomplt.Draw("COLZ TEXT")
            latex.DrawLatex(0.2,0.7, "Yields %s    %s "%(nom , sig_legs[sigtype]) +"   %s"%b.upper())
            c1.SaveAs(saveDirs[sigtype]['yield'] +"/%s_%s.png"%(b,nom))
    
            denomplt.Draw("COLZ TEXT")
            latex.DrawLatex(0.2,0.7, "Yields %s    %s "%(denom , sig_legs[sigtype]) +"   %s"%b.upper())
            c1.SaveAs(saveDirs[sigtype]['yield'] +"/%s_%s.png"%(b,denom))
    
            diffplt = nomplt.Clone()
            subplt  = denomplt.Clone()
            subplt.Scale(-1)
            diffplt.Add(subplt)
            diffplt.Divide(nomplt)
            diffplt.Scale(100)
            diffplt.Draw("COLZ TEXT")
            latex.DrawLatex(0.2,0.7, "#frac{%s-%s}{%s}*100    %s "%(nom,denom,nom , sig_legs[sigtype] ) +"   %s"%b.upper())
            c1.SaveAs(saveDirs[sigtype]['diff'] +"/%s.png"%(b))
     
    
           # c1.SaveAs( ratioDir+"/"+sigtype+"/%s.png"%b)
    
