from Workspace.DegenerateStopAnalysis.cuts import *
from Workspace.DegenerateStopAnalysis.navidTools.getSamples_PP_7412pass2_GenTracks import *
from makeTable import *
from limitCalc import *

from Tracks import *

from trackPlotDict import *


from Workspace.DegenerateStopAnalysis.navidTools.NavidTools import *
from Workspace.DegenerateStopAnalysis.navidTools.getRatioPlot import *


#saveDir = '/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/analysis/RunII/cutbased/GenTracks/Multip/2stIter'
saveDir = '/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/analysis/RunII/cutbased/GenTracks/test'
######## Track Validation commands ######
sampleList=['s','w']
plotList=[]
if not samples.s.tree.GetEventList():
  setEventListToChains(samples,sampleList,sr1Loose)


getPlotOpt=False
if getPlotOpt:
    print "Getting Plots:"
    if not hasattr(samples.s,"cuts"):
        getPlots2(samples,trackPlots,sr1Loose,sampleList=sampleList,plotList=plotList)




plotList=[
          {"name":"Tracks_dxy__dz01_vetoJet",   
                            "var":"Tracks_dxy",   'cut':trackCut(dxy=0.5, dz=0.1,jetOpt="veto")    ,'bins':[20,-0.5,0.5],'weight':"weight",'min':0.1,'logy':1,'fom':"ratio",'save':True}, 
          #{"name":"Tracks_dxy__dz05_vetoJet",   
          #                  "var":"Tracks_dxy",   'cut':trackCut(dxy=0.5, dz=0.5,jetOpt="veto")    ,'bins':[20,-0.5,0.5],'weight':"weight",'min':0.1,'logy':1,'fom':"ratio",'save':True}, 
          #{"name":"Tracks_dz__dxy05_vetoJet",   
          #                  "var":"Tracks_dz",   'cut':trackCut(dz=0.5, dxy=0.5,jetOpt="veto")    ,'bins':[20,-0.5,0.5],'weight':"weight",'min':0.1,'logy':1,'fom':"ratio",'save':True}, 
          #{"name":"Tracks_dz__dxy05_onlyJet",   
          #                  "var":"Tracks_dz",   'cut':trackCut(dz=0.5, dxy=0.5, jetOpt="only")    ,'bins':[20,-0.5,0.5],'weight':"weight",'min':0.1,'logy':1,'fom':"ratio",'save':True}, 
          #{"name":"Tracks_dz__dxy01_vetoJet",   
          #                  "var":"Tracks_dz",   'cut':trackCut(dz=0.5, dxy=0.1,jetOpt="veto")    ,'bins':[20,-0.5,0.5],'weight':"weight",'min':0.1,'logy':1,'fom':"ratio",'save':True}, 
          #{"name":"Tracks_dz__dxy01_onlyJet",   
          #                  "var":"Tracks_dz",   'cut':trackCut(dz=0.5, dxy=0.1, jetOpt="only")    ,'bins':[20,-0.5,0.5],'weight':"weight",'min':0.1,'logy':1,'fom':"ratio",'save':True}, 
          {"name":"Tracks_pt_onlyJetTracks",   
                            "var":"Tracks_pt",   'cut':trackCut(dz=0.1, dxy=0.1, jetOpt="only")    ,'bins':[100,0,300],'weight':"weight",'min':0.1,'logy':1,'fom':"ratio",'save':True}, 
          {"name":"Tracks_pt_vetoJetTracks",   
                            "var":"Tracks_pt",   'cut':trackCut(trkPt=1, dz=0.1, dxy=0.1, jetOpt="veto")    ,'bins':[100,0,50],'weight':"weight",'min':0.1,'logy':1,'fom':"ratio",'save':True}, 

          {"name":"nTracks_dz__dxy01_onlyJet",   
                            "var":nTracks(dz=0.1,dxy=0.1, jetOpt="veto"),   'cut':"(1)"    ,'bins':[20,0,20],'weight':"weight",'min':0.1,'logy':1,'fom':True,'save':True}, 
          {"name":"nGenTracks_dz__dxy01_onlyJet",   
                            "var":nTracks(trk="GenTracks", jetOpt="veto"),   'cut':"(1)"    ,'bins':[50,0,50],'weight':"weight",'min':0.1,'logy':1,'fom':True,'save':True}, 



          ]

plots={}

plotOpt=False
if plotOpt:
  for p in plotList:
      plots[p['name']]=getAndDraw(**p)




canvs={}
foms={}
fomCanvs={}


drawOpt=False
if drawOpt:
    for plot in plotList:
        canvs[plot]=drawPlot( samples, sampleList, plot,save=True )
        foms[plot]=getFOMFromTH1F(samples.s.cuts.sr1Loose[plot], samples.w.cuts.sr1Loose[plot] )
        foms[plot].GetXaxis().SetTitle("Track Multip > X")
        foms[plot].GetYaxis().SetTitle("FOM")
        fomCanvs[plot]=ROOT.TCanvas( "FOM_%s"%plot, "FOM_%s"%plot, 600, 600)
        foms[plot].SetLineColor(ROOT.kMagenta)
        foms[plot].SetLineWidth(2)
        foms[plot].SetMinimum(0)
        foms[plot].Draw()
        fomCanvs[plot].SaveAs(saveDir+"/%s.png"%"FOM_%s"%plot)

pklDir= "./pkl/Tracks/1stIter/"
#tableDir = saveDir+"/table/" 
tableDir = saveDir+"" 



getYieldsOpt=False
if getYieldsOpt:
    print "Getting Yields:"
    print "Pickle Dir: ", pklDir
    print "Tables: ", tableDir
    yDict={}
    hists={}
    for trkCut in sr1TrkCuts:
        name = trkCut
        cutInst = sr1TrkCuts[trkCut]['cut']
        #canv={}
        #regDict[name] = QCosRegion(*r, x=xvar,y=yvar)
        #print "----------------------------------------------------------------"
        #print getattr(regDict[name],cut).list
        print " --------------------------------- Getting Yields:     %s"%name
        yDict[name] =  Yields(samples,['w','s'], cutInst , cutOpt='list', tableName='{cut}',pklOpt=True,pklDir=pklDir )
        JinjaTexTable(yDict[name], pdfDir=tableDir)
        print " ------------------- Drawing :     %s"%name
        hists[name] = getAndDraw(name, sr1TrkCuts[name]['var'], bins=sr1TrkCuts[name]['bin'],   sampleList=['w'], min=0.1, logy=1, fom='AMSSYS'   , save=True)
        #canv[name]=ROOT.TCanvas(name,name,800,800)
        #fomHistW.Draw("COLZ")
        #regDict[name].r1.r.Draw("same")
        #regDict[name].r2.r.Draw("same")
        #regDict[name].r3.r.Draw("same")
        #canv[name].SaveAs(saveDir+"/%s.png"%name)









