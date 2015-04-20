import ROOT
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
#from Workspace.RA4Analysis.cmgTuples_v5_Phys14 import ttJets_fromEOS, 

#from Workspace.DegenerateStopAnalysis.cmgTuplesPostProcessed_v6_Phys14V3 import WJetsToLNu_HT100to200, WJetsToLNu_HT200to400, WJetsToLNu_HT400to600,  WJetsToLNu_HT600toInf, allSignals
from Workspace.DegenerateStopAnalysis.cmgTuplesPostProcessed_v1_Phys14V3 import *
from Workspace.DegenerateStopAnalysis.navidPlotTools import saveCanvas,decorate,decorateAxis


plotDir="/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/analysis/firstLook"
ROOT.gStyle.SetOptStat ( 000000)

sampleDict={
            'W':  {'tree':getChain(WJetsHTToLNu['soft'],histname='') ,         'color':41    , 'isSignal':0 , 'isData':0       },
            'st': {'tree':getChain(T2DegStop_300_270['soft'],histname=''),     'color':ROOT.kRed     , 'isSignal':1 , 'isData':0       },
            #'TTs': {'tree':getChain(ttJets['soft'],histname='') ,               'color':1    , 'isSignal':0 , 'isData':0       },            
         }

#samples_hard={
#            'W':  {'tree':getChain(WJetsHTToLNu['hard'],histname='') ,         'color':1    , 'isSignal':0 , 'isData':0       },
#            'TT': {'tree':getChain(ttJets['hard'],histname='') ,               'color':1    , 'isSignal':0 , 'isData':0       },
#        }


###Cuts and Preselction
muPdg="(abs(LepGood_pdgId)==13)"
muId="(LepGood_mediumMuonId==1)"
muPt5_25="(LepGood_pt > 5 && LepGood_pt < 25)"
muEta="abs(LepGood_eta)<2.4"
muMiniIso="(LepGood_miniRelIso < 0.2 || LepGood_pt < 15)&&(LepGood_miniRelIso < 0.4 || LepGood_pt > 15)"
muSelect= "(%s)"%" && ".join([muId,muPt5_25,muEta,muMiniIso]) 

preMET="(met>200)"
preHT="(htJet30j > 300)"
preISR="(Jet_pt[0]>110 && Jet_pt[1]>60)"
preSelection = "("+" && ".join([preMET,preHT,preISR  ]) + ")"

### Additional Variables:


mt0=80
invMassTemplate="sqrt(2*%(TYPE)s_pt*met*(cosh(%(TYPE)s_phi-metPhi)-cos(%(TYPE)s_phi-metPhi)))"
mtTemplate="sqrt(2*%(TYPE)s_pt*met*(1-cos(%(TYPE)s_phi-metPhi)))"
QTemplate="1-%(mt0)s^2/(2*met*%(TYPE)s_pt)"



invMass = invMassTemplate%{"TYPE":"LepGood"}
mt = mtTemplate%{"TYPE":"LepGood"}
Q=QTemplate%{"TYPE":"LepGood","mt0":mt0}
cos='cos(metPhi-LepGood_phi)'

dmt=Q+":"+cos

#mtsquared="(2*%(TYPE)s_pt*met*(1-cos(%(TYPE)s_phi-metPhi)))"





#Qtemp="1-("+mtsquared+")/(2*met*%(TYPE)s_pt*cosh(%(TYPE)s_eta)*cosh(%(TYPE)s_eta))"





#Q1=Qtemp%100
#Q="1-%(mt0)s/(2*met*%(TYPE)s_pt)"%{"mt0":mtsquared%{"TYPE":"mu"},"TYPE":"mu"}
#Q=lambda()
mtQline = lambda mt1: "-1*("+str(mt0)+"/"+str(mt1) +')^2*(1 - cos(metPhi-muPhi))+1:cos(metPhi-muPhi)'
#Qcut = lambda mt1: "-1*("+str(mt0)+"/"+str(mt1) +')^2*(cos(metPhi-muPhi)):cos(metPhi-muPhi)'
arbQcut = lambda m,b: ""+str(m)+'*cos(metPhi-muPhi)+'+str(b)
arbQcutline = lambda m,b: arbQcut(m,b)+':cos(metPhi-muPhi)'
arbQcutStr= lambda m, b: '('+Q+')>('+arbQcut(m,b)+')'



binPT=[100,0,300]
binMT=binPT
binDMT=[20,1.5,-5,20,-1,1]




plotDict = {


      #'lep_pt':  {'var':"LepGood_pt",    "presel":preSelection,              "cut":"(1)", "fillColor":"" ,"color":"fill" ,"lineWidth":1 , "bin":binPT,  "title":""    ,"xLabel":"lep_pt",    "yLabel":"",     "xLog":0, "yLog":1                  },
      #'lep_MT':     {'var':mt,           "presel":preSelection,              "cut":"(1)", "fillColor":"" ,"color":"fill" ,"lineWidth":1 , "bin":binMT,  "title":""    ,"xLabel":"lep_MT",    "yLabel":"",     "xLog":0, "yLog":1                  },
      #'lep_dmt':    {'var':dmt,          "presel":preSelection,              "cut":"(1)", "fillColor":"" ,"color":""     ,"lineWidth":1 , "bin":binDMT, "title":""    ,"xLabel":"cos(\phi)", "yLabel":"Q",    "xLog":0, "yLog":0    ,"zLog":1     },

      'mu_pt':  {'var':"LepGood_pt",    "presel":"(%s&&%s)"%(muSelect,preSelection), "cut":"(1)", "fillColor":"" ,"color":"fill" ,"lineWidth":1 , "bin":binPT,  "title":"Muon P_{T}"    ,"xLabel":"mu_pt",     "yLabel":"",     "xLog":0, "yLog":1                  },
      'mu_MT':     {'var':mt,           "presel":"(%s&&%s)"%(muSelect,preSelection), "cut":"(1)", "fillColor":"" ,"color":"fill" ,"lineWidth":1 , "bin":binMT,  "title":"MT"    ,"xLabel":"MT",        "yLabel":"",     "xLog":0, "yLog":1                  },
      'mu_dmt':    {'var':dmt,          "presel":"(%s&&%s)"%(muSelect,preSelection), "cut":"(1)", "fillColor":"" ,"color":""     ,"lineWidth":1 , "bin":binDMT, "title":"Deconstructed_MT"    ,"xLabel":"cos(\phi)", "yLabel":"Q",    "xLog":0, "yLog":0 ,"zLog":1        },

      }



getAllAlph = lambda str: ''.join(ch for ch in str if ch not in "Kl13@$%[]{}();'\"")


### Move To PlotTools

def getGoodPlotFromChain(c, var, binning,varName='', cutString='(1)', weight='weight', color='', lineWidth='',fillColor='',  binningIsExplicit=False, addOverFlowBin=''): 
  ret=  getPlotFromChain(c, var, binning, cutString=cutString, weight=weight, binningIsExplicit=binningIsExplicit, addOverFlowBin=addOverFlowBin) 
  if not varName:
    varName=getAllAlph(var)
    print varName
  ret.SetTitle(varName)
  ret.SetName(varName)
  if color:
    ret.SetLineColor(color)
  if lineWidth:
    ret.SetLineWidth(lineWidth)
  if fillColor:
    ret.SetFillColor(fillColor)
  return ret

def getStackFromHists(histList):
  stk=ROOT.THStack()
  for h in histList:
    stk.Add(h)
  return stk






########################################



print "doing stuff"

if 1:
  for s in sampleDict:
    sampleDict[s]['plots']={}
    for p in plotDict:
      lineWidth=plotDict[p]['lineWidth']
      if plotDict[p]['color'].lower()=="fill" and not sampleDict[s]['isSignal']:
        color = ROOT.kBlack
        fcolor = sampleDict[s]['color']
      else:
        color  = sampleDict[s]['color']
        fcolor = 0 
        if sampleDict[s]['isSignal']:
          lineWidth=2
      sampleDict[s]['plots'][p] = getGoodPlotFromChain(sampleDict[s]['tree'] , plotDict[p]['var'], plotDict[p]['bin'],\
                                                       cutString   = "(%s) && (%s)"%(plotDict[p]['presel'],plotDict[p]['cut']),                      
                                                       color       = color,
                                                       fillColor   = fcolor,
                                                       lineWidth   = lineWidth)



if 1:
  treeList=['W','st']
  varList=plotDict.keys()
  sDict=sampleDict

  bkgStackDict={}
  sigStackDict={}
  for v in varList:
    if len(plotDict[v]['bin'])!=6:
      bkgStackDict[v]=getStackFromHists([ sDict[t]['plots'][v] for t in treeList if not sDict[t]['isSignal']])
      sigStackDict[v]=getStackFromHists([ sDict[t]['plots'][v] for t in treeList if sDict[t]['isSignal']])
    

if 1:
  treeList=['W','st']
  varList=plotDict.keys()
  for v in varList:
  #for stk in sigStackDict.keys():
    if len(plotDict[v]['bin'])!=6:
      c1=ROOT.TCanvas("c1","c1")
      bkgStackDict[v].Draw()
      sigStackDict[v].Draw("samenostack")
      decorateAxis(bkgStackDict[v],xAxisTitle=plotDict[v]['xLabel'],yAxisTitle=plotDict[v]['yLabel'])
    #plotDict[v]['yAxis']
      c1.SetLogy(plotDict[v]['yLog'])
      c1.SetLogx(plotDict[v]['xLog'])
      c1.Update()
      saveCanvas(c1,v,plotDir=plotDir)
      del c1
    ### 2D plots:
    elif len(plotDict[v]['bin'])==6:
      for t in treeList:
        c1=ROOT.TCanvas("c1","c1")
        sDict[t]['plots'][v].SetTitle(t+"_"+plotDict[v]['title'])
        sDict[t]['plots'][v].Draw("colz")
        decorateAxis(sDict[t]['plots'][v],xAxisTitle=plotDict[v]['xLabel'],yAxisTitle=plotDict[v]['yLabel'])
        c1.SetLogx(plotDict[v]['xLog'])
        c1.SetLogy(plotDict[v]['yLog'])
        c1.SetLogz(plotDict[v]['zLog'])
        saveCanvas(c1,v+"_"+t,plotDir=plotDir)
        del c1


###############################################################################
###############################################################################
##########################                    #################################
##########################      YIELDS        #################################
##########################                    #################################
###############################################################################
###############################################################################




muFromTau="mediumMuIndex>-1&&muIgpMatch[mediumMuIndex]>-1&&gpTag[muIgpMatch[mediumMuIndex]]==2"
preselIvan="(type1phiMet>200.&&isrJetPt>110.&&ht>300.)"+"&&"+"(isrJetBTBVetoPassed)"+"&&"+"((nHardElectrons+nHardTaus)==0)"+"&&"+\
             "(mediumMuIndex>-1&&(muPt[mediumMuIndex]<20.||nHardMuonsMediumWP==1))"+"&&"+"(njet60<3)"
preselRobert="(type1phiMet>200.&&isrJetPt>110.&&ht>300.)"+"&&"+"(isrJetBTBVetoPassed)"+"&&"+"((nHardElectrons+nHardTaus)==0)"+"&&"+\
             "(mediumMuIndex>-1&&(muPt[mediumMuIndex]<20.))"+"&&"+"(njet60<3)"
preselection=preselRobert
SR1="(ht>400.&&type1phiMet>300.)"+"&&"+"(nbtags==0)"+"&&"+"(abs(muEta[mediumMuIndex])<1.5)"+"&&"+"(muPdg[mediumMuIndex]>0)"
SR1a=SR1+"&&"+"("+MT + "<60)"
SR1b=SR1+"&&"+"("+MT + ">60)&&("+ MT + "< 88)"
SR1c=SR1+"&&"+"("+MT + ">88)"
SR2="(isrJetPt>325.&&type1phiMet>300.)"+"&&"+"(nHardbtags==0&&nSoftbtags>0)"
mtcut = MT+">80"

SR1="( (htJet30j > 300) && met>300 && Sum$(nBJetLoose40+nBJetMedium40+nBJetTight40)==0 && LepGood_pdgId==13 && abs(LepGood_eta)<1.5)"
SR1a=SR1+"&&(%s<60)"%mt
SR1b=SR1+"&&(%s>60)&&(%s<88)"%(mt,mt)
SR1c=SR1+"&&(%s>88)"%mt


getYields=1

cutDict = [
      {"noCut": "(1)" } ,
      {"preSel": preSelection} ,
      {"muIndex": muSelect} ,
      {"preSel_muIndex": muSelect} ,
      {"SR1": SR1 } ,
      {"presel_SR1": "(%s&&%s)"%(preSelection,SR1) } ,
      {"presel_SR1a": "(%s&&%s)"%(preSelection,SR1a) } ,
      {"presel_SR1b": "(%s&&%s)"%(preSelection,SR1b) } ,
      {"presel_SR1c": "(%s&&%s)"%(preSelection,SR1c) } ,
      
           ]


if getYields:
  treeList = ['W','st']
  #varList=plotDict.keys()
  yieldDict={}
  for t in treeList:
    yieldDict[t]={}
    for cut in cutDict:
      cutName=cut.keys()[0]
      cutString=cut[cutName]
      #cutString = "(%s) && (%s)"%(plotDict[p]['presel'],plotDict[p]['cut'])
      yieldDict[t][cutName] = getYieldFromChain(sampleDict[t]['tree'],cutString,weight="weight")
     






#plots = [
#          ['sqrt(2*leptonPt*met*(1-cos(metPhi-leptonPhi)))', [20,0,800], 'mt'],\
#          ['acos((leptonPt + met*cos(leptonPhi - metPhi))/sqrt(leptonPt**2 + met**2+2*met*leptonPt*cos(leptonPhi-metPhi)))', [16,0,3.2], 'd
#phi']
#    ]
#
#
#
#for var, binning, fname in plots:
#  c1 = ROOT.TCanvas() 
#  hPresel = getPlotFromChain(c, var, binning, presel, 'weight')
#  hPresel.SetLineColor(ROOT.kBlack)
#  hPresel.SetTitle("")
#  hPresel.GetYaxis().SetRangeUser(0.1, 1.5*hPresel.GetMaximum())
#  hPresel.Draw()
#
#  for sig in signals:
#    sig['hPresel'] = getPlotFromChain(sig['c'], var, binning, presel, 'weight')
#    sig['hPresel'].SetLineColor(sig['color'])
#    sig['hPresel'].SetLineWidth(2)
#    sig['hPresel'].SetTitle("")
#
#

#
#
#
#
#
#
#
#
#
