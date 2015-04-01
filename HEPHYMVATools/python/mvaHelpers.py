def getAnyObjFromFile(fname,hname):
  import ROOT
  olddir = ROOT.gDirectory.CurrentDirectory().GetName()+':/'
  if type(fname)==type(""):
    f = ROOT.TFile.Open(fname)
  else: f=fname
  obj_t = f.FindObjectAny(hname)
  if obj_t == None:
    print 'File ('+hname+') not found!'
    return
  ROOT.gDirectory.cd(olddir)
  if type(obj_t) == type(ROOT.TTree()):
    obj = obj_t.CloneTree()
  else:
    obj = obj_t.Clone()
  if type(fname)==type(""):
    f.Close()
  return obj

def getTrainingSampleSizes(countSignal, bkgs, fractionForTraining=0.5):
  """ 
  finds nbBkg1,...,nBkgN such that nBkg1+...+nBkgN is maximal while respecting
  nBkg1+nBkg2+...+nBkgN<=nSigTraining, nBkg1:nBkg2:...:nBkgN=yBkg1:yBkg2:...:yBkgN
  and nBkg1<=fractionForTraining*nBkg1Max, ...., fractionForTraining*nBkgNMax<=nBkgNMax
  arguments:
  countSignal: Total count of signal sample.
  bkgs: [{'count':nBkg1,'yield':yBkg1},...,{'count':nBkgN,'yield':yBkgN}]]
  """
  maxSignalCount=int(fractionForTraining*countSignal)
  assert maxSignalCount>0, "Too few signal events. Training events: %i"%maxSignalCount
  maxBkgYield = float(max([b['yield'] for b in bkgs ]))
  assert maxBkgYield>0, "Maximum background yield non-positive: %f"%maxBkgYield
  maxTrainingEvents=[ int(fractionForTraining*b['count']) for b in bkgs]
  for i, n in enumerate(maxTrainingEvents): assert maxTrainingEvents>0, "No training events found bkg sample nr. %i"%i
  weightList = [float(b['yield'])/int(fractionForTraining*b['count']) for b in bkgs]
  maxWeightIndex = weightList.index(max(weightList))
  maxAchievableBkg = [int(fractionForTraining*b['count']*b['yield']/bkgs[maxWeightIndex]['yield']) for b in bkgs]
  if sum(maxAchievableBkg)<maxSignalCount:
    print "Smallest background sample in position %i is limiting (%i total events, %i training events). Solution: Signal: %i, bkgs.: %s."%(maxWeightIndex,bkgs[maxWeightIndex]['count'],maxTrainingEvents[maxWeightIndex],sum(maxAchievableBkg),",".join([str(x) for x in maxAchievableBkg]))
    return {'bkgs':maxAchievableBkg,'signal':sum(maxAchievableBkg)}
  else:
    fac = maxSignalCount/float(sum(maxAchievableBkg))
    res = [int(fractionForTraining*b['count']*b['yield']/bkgs[maxWeightIndex]['yield']*fac) for b in bkgs]
    print "Signal sample is limiting: Scaling down backgrounds accordingly. Maximally achievable background would be %i. Solution: Signal: %i, bkgs.: %s"%(sum(maxAchievableBkg),maxSignalCount,",".join([str(x) for x in res]))
    return {'bkgs':res, 'sig':maxSignalCount}

def getObsName(v):
  return v.split('/')[0]
def getObsType(v):
  if v.count('/'): return v.split('/')[1]
  return 'F'

def createDatasetForTMVA(setup, signal, backgrounds, overWrite = False, maxEvents=-1):
  """
  create ROOT::TTree objects from a signal (TChain and event lists for test and training) 
  and a list of backgrounds. setup["obsFromInput"] and setup["obsCalculated"] specify the observables.
  arguments:
  setup dictionary, signal={'chain':ROOT.TChain, 'trainingEvents':[...], 'testEvents':[...]]}
  backgrounds=[{'chain':ROOT.TChain, 'trainingEvents':[...], 'testEvents':[...]}, {....}],
  overWrite = False
  """
  from Workspace.HEPHYPythonTools.helpers import getEList
  import os, ctypes, ROOT
  p_c_float = ctypes.c_float * 1
  p_c_double = ctypes.c_double * 1
  if (not overWrite) and os.path.isfile(setup['dataFile']):
    print "[createDatasetForTMVA] Found file",setup['dataFile'],"-> do nothing"
    return
  else:
    print 'Creating MVA dataset',setup['dataFile']
    if overWrite and os.path.isfile(setup['dataFile']):
      print 'Warning! File will be overwritten'
    tree = ROOT.TTree('Events', 'Train and test tree')

    obsType={}

    for vn in setup['obsFromInput']+[v[0] for v in setup['obsCalculated']]:
      obsType[getObsName(vn)] = getObsType(vn)
    observables={}
    for vn in setup['obsFromInput']:
      n = getObsName(vn)
      if obsType[n]=='F': observables[n] = p_c_float(0.)
      if obsType[n]=='D': observables[n] = p_c_double(0.)
      if obsType[n]=='I': observables[n] = ctypes.c_int(0)

    i_type      = ctypes.c_int(0)
    i_isTraining    = ctypes.c_int(0)
    for c in [signal['chain']]+ [b['chain'] for b in backgrounds]:
      for k in observables.keys():
        c.SetBranchAddress(k, observables[k])

    for k in observables.keys():
      tree.Branch(k, observables[k], k+'/'+obsType[k])
#      print k, observables[k], k+'/'+obsType[k], tree.GetBranch(k)
    tree.Branch('type'  ,   ctypes.addressof(i_type),     'type/I')
    tree.Branch('isTraining',   ctypes.addressof(i_isTraining),   'isTraining/I')
    addObs = {}
    for v in [getObsName(vn) for vn in  [v[0] for v in setup['obsCalculated']] ]:
      if obsType[v]=='F': addObs[v] = ctypes.c_float(0.)
      if obsType[v]=='D': addObs[v] = ctypes.c_double(0.)
      if obsType[v]=='I': addObs[v] = ctypes.c_int(0)
      if not ( obsType[v]=='F' or obsType[v]=='I') : print "Warning! Unknown obsType'"+obsType[v]+"'for observable", v
      tree.Branch(v,   ctypes.addressof(addObs[v]),   v+'/'+obsType[v])
#      print v,   ctypes.addressof(addObs[v]),   v+'/'+obsType[v]

    def fillTree(tree, chain, evlist):
#      chain.GetEntry(0)
      nmax = maxEvents if maxEvents>0 else len(evlist)
      for i, ev in enumerate(evlist[:nmax]):
        if i%1000==0:print 'Event.:',i,'/',len(evlist)
        chain.GetEntry(ev)
        for v in setup["obsCalculated"]:
          vn = getObsName(v[0])
          if obsType[vn] =="I":
            addObs[vn].value  = int(v[1](chain))
          if obsType[vn] =="F":
            addObs[vn].value  = v[1](chain)
        tree.Fill()

    print "Filling events from signal tree (training: %i, test: %i)"%(len(signal["trainingEvents"]),len(signal["testEvents"]))
    print "Training events..."
    i_type.value=1
    i_isTraining.value=1
    fillTree(tree, signal['chain'], signal['trainingEvents'])
    i_isTraining.value=0
    print "Test events..."
    fillTree(tree, signal['chain'], signal['testEvents'])

    i_type.value=0
    for j, b in enumerate(backgrounds):
      print "Filling events from background component %i (training: %i, test: %i)"%(j, len(b["trainingEvents"]),len(b["testEvents"]))
      print "Training events..."
      i_isTraining.value=1
      fillTree(tree, b['chain'], b['trainingEvents'])
      print "Test events..."
      i_isTraining.value=0
      fillTree(tree, b['chain'], b['testEvents'])

    eListBkg          = getEList(tree,   'type==0&&'+ setup['preselection']    ,'eListBkg')
    eListSig          = getEList(tree,   'type==1&&'+ setup['preselection']    ,'eListSig')
    eListBkgTraining  = getEList(tree,   'isTraining==1&&type==0&&'+ setup['preselection']    ,'eListBkgTraining')
    eListSigTraining  = getEList(tree,   'isTraining==1&&type==1&&'+ setup['preselection']    ,'eListSigTraining')
    eListBkgTest      = getEList(tree,   'isTraining==0&&type==0&&'+ setup['preselection']    ,'eListBkgTest')
    eListSigTest      = getEList(tree,   'isTraining==0&&type==1&&'+ setup['preselection']    ,'eListSigTest')
    f = ROOT.TFile(setup['dataFile'], 'recreate')
    tree.Write()
    eListBkg.Write()
    eListSig.Write()
    eListBkgTraining.Write()
    eListSigTraining.Write()
    eListBkgTest.Write()
    eListSigTest.Write()
    f.Close()
    print 'Written MVA dataset to', setup['dataFile']
    import copy, pickle
    setup['dataSetConfigFile'] = setup['dataFile'].replace('.root', '.pkl')
    setupStripped = copy.deepcopy(setup)
    setupStripped['obsCalculated'] = [v[:-1]+['removedFunction'] for v in setupStripped['obsCalculated']]
    pickle.dump(setupStripped, file(setup['dataSetConfigFile'],"w"))
    print 'Written MVA setup to',setup['dataSetConfigFile']
    Events = ROOT.gDirectory.Get("Events")
    del Events
    del eListBkg
    del eListSig
    del eListBkgTraining
    del eListSigTraining
    del eListBkgTest
    del eListSigTest

def loadDatasetForTMVA(dataFile):
  print 'Loading MVA dataset from', dataFile
  tree      = getAnyObjFromFile(dataFile,'Events')
  eListBkg      = getAnyObjFromFile(dataFile,'eListBkg')
  eListSig      = getAnyObjFromFile(dataFile,'eListSig')
  eListBkgTraining      = getAnyObjFromFile(dataFile,'eListBkgTraining')
  eListSigTraining      = getAnyObjFromFile(dataFile,'eListSigTraining')
  eListBkgTest      = getAnyObjFromFile(dataFile,'eListBkgTest')
  eListSigTest      = getAnyObjFromFile(dataFile,'eListSigTest')
  print'Dataset total entries:',tree.GetEntries()
  print '...done.'
  return {'tree':tree, \
    'eListBkg':eListBkg, 'eListSig':eListSig, 
    'eListBkgTraining':eListBkgTraining, 'eListSigTraining':eListSigTraining,
    'eListBkgTest':eListBkgTest, 'eListSigTest':eListSigTest,
    }

def getFOMPlot(bgDisc, sigDisc):
  import ROOT
  from array import array
  if not bgDisc.GetNbinsX()==sigDisc.GetNbinsX():
    print 'bkg and sig shapes have unequal binning'
    return
  zeros = []
  sigEff = []
  bkgRej = []
  sigEffPlus = []
  bkgRejPlus = []
  sigEffMinus = []
  bkgRejMinus = []
  normBkg = bgDisc.Integral()
  normSig = sigDisc.Integral()
  if not (normBkg>0 and normSig>0):return
  for i in range(1,1+bgDisc.GetNbinsX()):
    zeros.append(0.)
#    bkgRejErr_v = ROOT.Double()
    bkgRej_v = bgDisc.Integral(1, i)
    bkgRej    .append(bkgRej_v/float(normBkg))
#    print int(normBkg), int(bkgRej_v),ROOT.TEfficiency.ClopperPearson( int(normBkg), int(bkgRej_v), 0.683,0)
#    bkgRejErrLow.append(   -ROOT.TEfficiency.ClopperPearson(int(normBkg), int(bkgRej_v), 0.683,0) + bkgRej_v/float(normBkg))
#    bkgRejErrHigh.append(   ROOT.TEfficiency.ClopperPearson(int(normBkg), int(bkgRej_v), 0.683,1) - bkgRej_v/float(normBkg))
    bkgRejPlus.append(    ROOT.TEfficiency.ClopperPearson(int(normBkg), int(bkgRej_v), 0.683,1))
    bkgRejMinus.append(   ROOT.TEfficiency.ClopperPearson(int(normBkg), int(bkgRej_v), 0.683,0))

    sigEff_v = sigDisc.Integral(i+1, bgDisc.GetNbinsX())
    sigEff    .append(sigEff_v/float(normSig))
    sigEffPlus. append(   ROOT.TEfficiency.ClopperPearson(int(normSig), int(sigEff_v), 0.683,1))
    sigEffMinus.append(   ROOT.TEfficiency.ClopperPearson(int(normSig), int(sigEff_v), 0.683,0))
#    sigEffErrLow.append(   -ROOT.TEfficiency.ClopperPearson(int(normSig), int(sigEff_v), 0.683,0) + sigEff_v/float(normSig))
#    sigEffErrHigh.append(   ROOT.TEfficiency.ClopperPearson(int(normSig), int(sigEff_v), 0.683,1) - sigEff_v/float(normSig))
  grCentral = ROOT.TGraphErrors(len(sigEff), array('d', sigEff), array('d', bkgRej), array('d',zeros), array('d', zeros))
  grPlus  = ROOT.TGraphErrors(len(sigEff), array('d', sigEffPlus), array('d', bkgRejPlus), array('d',zeros), array('d', zeros))
  grMinus = ROOT.TGraphErrors(len(sigEff), array('d', sigEffMinus), array('d', bkgRejMinus), array('d',zeros), array('d', zeros))
  grCentral.GetXaxis().SetTitle('Signal efficiency')
  grCentral.GetYaxis().SetTitle('Background rejection')
  grCentral.SetMarkerColor(0)
  grCentral.SetLineColor(ROOT.kBlack)
  grCentral.SetMarkerStyle(0)
  grCentral.SetMarkerSize(0)
  grPlus.SetMarkerColor(0)
  grPlus.SetLineColor(ROOT.kBlue)
  grPlus.SetMarkerStyle(0)
  grPlus.SetMarkerSize(0)
  grMinus.SetMarkerColor(0)
  grMinus.SetLineColor(ROOT.kBlue)
  grMinus.SetMarkerStyle(0)
  grMinus.SetMarkerSize(0)
  return {'central':grCentral, 'plus':grPlus, 'minus':grMinus}


def setupMVAFrameWork(setup, data, methods, prefix):
  import ROOT
  import os
  if not os.path.exists(setup['weightDir']):
     os.makedirs(setup['weightDir'])
    
  olddir = ROOT.gDirectory.CurrentDirectory().GetName()+':/'
  vstring=''
  for v in setup['mvaInputObs']:
    vstring+=getObsName(v)+','
  vstring = vstring[:-1]

  print 'Instancing of TMVA Factory:'

  ROOT.TMVA.Tools.Instance()
  ROOT.TMVA.gConfig().GetIONames().fWeightFileDir = setup['weightDir']
  ROOT.TMVA.gConfig().GetVariablePlotting().fNbinsXOfROCCurve = 200
  
  fout = ROOT.TFile(setup['TMVAOutputFile'],"RECREATE")
  factory = ROOT.TMVA.Factory("TMVAClassification", fout,":".join(setup['TMVAFactoryOptions']))
  factory.DeleteAllMethods()


  varType={}
  for vn in setup['obsFromInput']+[v[0] for v in setup['obsCalculated']]:
    varType[getObsName(vn)] = getObsType(vn)

  for v in setup['mvaInputObs']:
    print "Adding to factory variable", v, 'of type', varType[v]
    factory.AddVariable(getObsName(v), varType[v])

  bkgTestTree =   data['tree'].CopyTree("isTraining==0&&type==0")
  sigTestTree =   data['tree'].CopyTree("isTraining==0&&type==1")
  bkgTrainTree =  data['tree'].CopyTree("isTraining==1&&type==0")
  sigTrainTree =  data['tree'].CopyTree("isTraining==1&&type==1")
  factory.AddBackgroundTree( bkgTrainTree,  1.0, "Training" );
  factory.AddBackgroundTree( bkgTestTree,   1.0,  "Test" );
  factory.AddSignalTree( sigTrainTree,      1.0, "Training" );
  factory.AddSignalTree( sigTestTree,       1.0,  "Test" );
#  factory.SetBackgroundWeightExpression("weightForMVA")
#  factory.SetSignalWeightExpression(    "weightForMVA")

  #Using all Methods:
  for m in methods:
    args = (m['type'], m['name'],':'.join(m['options']))
    print args
    methodBook = factory.BookMethod(*args)

  factory.TrainAllMethods()
  factory.TestAllMethods()
  factory.EvaluateAllMethods()
#  method.WriteWeightsToStream(fout)
  fout.Close()
  pfile = setup['TMVAOutputFile'].replace('.root','')+'.pkl'
  import copy, pickle
  setupStripped = copy.deepcopy(setup)
  setupStripped['obsCalculated'] = [v[:-1]+['removedFunction'] for v in setupStripped['obsCalculated']]
  pickle.dump(setupStripped, file(pfile,"w"))
  print "Stored setup in",pfile
  
  stuff=[]
  mlpa_canvas = ROOT.TCanvas('mlpa_canvas', 'Network analysis', 1200, 400*(1+len(methods)))
  mlpa_canvas.SetFillColor(ROOT.kWhite)
  mlpa_canvas.Divide(2,1+len(methods))
#  ROOT.gROOT.ProcesssetTDRStyle()
  nbinsFine = 2000

  for j, m in enumerate(methods):
    for i, treeName in enumerate(['Test', 'Train']):
      l = ROOT.TLegend(.65, .80, 0.99, 0.99)
      t = getAnyObjFromFile(setup['TMVAOutputFile'], treeName+'Tree')
      mlpa_canvas.cd(1 + 2*(j+1)+i)
      l.SetFillColor(ROOT.kWhite)
      l.SetShadowColor(ROOT.kWhite)
      l.SetBorderSize(1)
      print 'Now MVA Output Histogram Testing will be done...'
      m['hsig'+treeName] = ROOT.TH1F('hsig'+treeName,'hsig'+treeName, 200, -.5, 1.5)
      m['hbg'+treeName] = ROOT.TH1F('hbg'+treeName, 'hbg'+treeName, 200, -.5, 1.5)
      m['hsig'+treeName+'Fine'] = ROOT.TH1F('hsig'+treeName+'Fine','hsig'+treeName+'Fine', nbinsFine, -.5, 1.5)
      m['hbg'+treeName+'Fine'] = ROOT.TH1F('hbg'+treeName+'Fine', 'hbg'+treeName+'Fine', nbinsFine, -.5, 1.5)
      t.Draw(m['name']+'>>+hsig'+treeName,'classID==1','goff')
      t.Draw(m['name']+'>>+hbg'+treeName,'classID==0','goff')
      t.Draw(m['name']+'>>+hsig'+treeName+'Fine','classID==1','goff')
      t.Draw(m['name']+'>>+hbg'+treeName+'Fine','classID==0','goff')
      m['hsig'+treeName].SetLineColor(ROOT.kRed)
      m['hsig'+treeName].SetFillStyle(3003)
      m['hsig'+treeName].SetFillColor(ROOT.kRed)
      m['hsig'+treeName].SetStats(0)
      m['hsig'+treeName].SetMarkerSize(0)
      m['hsig'+treeName].SetMarkerStyle(0)
      m['hsig'+treeName].SetMarkerColor(ROOT.kRed)
      m['hbg'+treeName].SetLineColor(ROOT.kBlue)
      m['hbg'+treeName].SetFillStyle(3008)
      m['hbg'+treeName].SetFillColor(ROOT.kBlue)
      m['hbg'+treeName].SetMarkerSize(0)
      m['hbg'+treeName].SetMarkerStyle(0)
      m['hbg'+treeName].SetMarkerColor(ROOT.kBlue)
      m['hbg'+treeName].SetStats(0)
#      m['hbg'+treeName].SetTitle('Classifier '+m['name'])
      m['hbg'+treeName].GetYaxis().SetRangeUser(0, 1.2*max(m['hbg'+treeName].GetMaximum(), m['hsig'+treeName].GetMaximum()))
      m['hbg'+treeName].Draw()
      m['hsig'+treeName].Draw("same")
      l.AddEntry(m['hbg'+treeName],  'Bkg '+treeName.replace('Tree','')+' '+m['niceName']+' ')
      l.AddEntry(m['hsig'+treeName], 'Sig '+treeName.replace('Tree','')+' '+m['niceName']+' ')
      l.Draw()
      stuff.append(l)
      t.IsA().Destructor(t)
      del t

  pad=mlpa_canvas.cd(1)
  print 'Now FOM from TMVA ...'
  pad.SetGrid()
  l5 = ROOT.TLegend(.16, .13, 0.5, 0.35)
  opt=""
  for m in methods:
    histFOM = getAnyObjFromFile(setup['TMVAOutputFile'],'MVA_'+m['name']+'_rejBvsS')
#   print 'histFOM (pad1):',histFOM
    stuff.append(histFOM)
    histFOM.SetStats(False)
    histFOM.SetLineColor(m['lineColor'])
    histFOM.SetMarkerColor(m['lineColor'])
    histFOM.SetMarkerStyle(0)
 #    histFOM.SetTitle('Graph of FOM by TMVA')
    histFOM.Draw(opt)
    opt="same"
    l5.AddEntry(histFOM,m['niceName'])
  l5.SetFillColor(0)
  l5.SetShadowColor(ROOT.kWhite)
  l5.SetBorderSize(1)
  l5.Draw()

  pad = mlpa_canvas.cd(2)

#  bkgPreselectionEff = data['simu'].GetEntries('type==0&&'+setup['preselection'])/float(data['simu'].GetEntries('type==0'))
#  sigPreselectionEff = data['simu'].GetEntries('type==1&&'+setup['preselection'])/float(data['simu'].GetEntries('type==1'))
#  lumi = 19400.
#  sigEffForOneEvent = 1./(sigPreselectionEff*setup['sigXsec']*lumi)

##  sOverSqrtBvalues = [1, 2, 3, 4, 5]
#  sOverSqrtBvalues = []
#  sOverSqrtBfuncs = {}
#  for c in sOverSqrtBvalues:
#    sOverSqrtBfuncs[c]=getConstSoverSqrtBFunc(lumi, setup['bkgXsec'], setup['sigXsec'], bkgPreselectionEff, sigPreselectionEff, c)
  pad.SetGrid()
  l3 = ROOT.TLegend(.16, .13, 0.5, 0.5)
  l3.SetFillColor(ROOT.kWhite)
  l3.SetShadowColor(ROOT.kWhite)
  l3.SetBorderSize(1)
  opt="AL"
  for m in methods:
    m['FOMFromFile'] = getAnyObjFromFile(setup['TMVAOutputFile'],'MVA_'+m['name']+'_rejBvsS')
    m['FOMFromFile'].SetStats(False)
    m['FOMFromFile'].SetLineColor(m['lineColor'])

    m['FOMFromTree'] = getFOMPlot(m['hbgTestFine'], m['hsigTestFine'])
    m['FOMFromTree']['central'].SetLineColor(m['lineColor'])
    if setup.has_key('fomPlotZoomCoordinates'):
      coord=setup["fomPlotZoomCoordinates"]
      m['FOMFromTree']['central'].GetXaxis().SetRangeUser(coord[0],coord[2])
      m['FOMFromTree']['central'].GetYaxis().SetRangeUser(coord[1],coord[3])
    m['FOMFromTree']['central'].Draw(opt)
    if not  m['type']==ROOT.TMVA.Types.kCuts:
      l3.AddEntry(m['FOMFromTree']['central'],m['niceName'],'LP')
#    else:
#      l3.AddEntry(m['FOMFromFile'],m['niceName'],'LP')
    opt="L"
    if m.has_key('drawStatUncertainty') and m['drawStatUncertainty']:
      if not  m['type']==ROOT.TMVA.Types.kCuts:
        m['FOMFromTree']['plus'].SetLineStyle(3)
        m['FOMFromTree']['minus'].SetLineStyle(3)
        m['FOMFromTree']['plus'].Draw(opt)
        m['FOMFromTree']['minus'].Draw(opt)
        l3.AddEntry(m['FOMFromTree']['plus'], m['niceName']+' (#pm 1#sigma)', 'LP')
  latexArgs = []
#  for c in sOverSqrtBvalues:
#    xpos = 1.05
#    ypos = sOverSqrtBfuncs[c].Eval(xpos)
#    latexArgs.append([xpos, ypos, str(c)])
#    sOverSqrtBfuncs[c].SetLineWidth(1)
#    sOverSqrtBfuncs[c].SetLineStyle(2)
#    sOverSqrtBfuncs[c].Draw('same')

#  latex = ROOT.TLatex();
#  latex.SetNDC(0);
#  latex.SetTextSize(0.035);
#  latex.SetTextAlign(11); # align right
#  [latex.DrawLatex(*cArg) for cArg in latexArgs]
#
  t = getAnyObjFromFile(setup['TMVAOutputFile'], 'TestTree')
  fom_plots = {}
  for fom_var, fom_var_range, fom_var_color in setup['fom_plot_vars']:
    print fom_var, fom_var_range, fom_var_color
    fom_plots[fom_var]  = getFOMPlot(getPlot(t,'classID==0', fom_var, [nbinsFine] +fom_var_range),    getPlot(t, 'classID==1', fom_var, [nbinsFine] + fom_var_range))['central']
    if fom_plots[fom_var]:
      fom_plots[fom_var].SetLineColor( fom_var_color )
      fom_plots[fom_var].Draw('L')
      l3.AddEntry(fom_plots[fom_var], fom_var, 'LP')

    for k in fom_plots.keys():
      fom_plots[k].Draw('L')
#    histCutFOM.Draw('same')
  l3.Draw()

  os.system('rm -f ./plots/*.png')
  os.system('rm -f ./plots/*.root')
  os.system('rm -f ./plots/*.pdf')
  os.system('rm -f ./plots/*.gif')
  os.system('mkdir -p '+setup['plotDir']+'/'+setup['plotSubDir'])
  mlpa_canvas.Print(setup['plotDir']+'/'+setup['plotSubDir']+'/nnValidation'+'.pdf')
  mlpa_canvas.Print(setup['plotDir']+'/'+setup['plotSubDir']+'/nnValidation'+'.png')
  mlpa_canvas.Print(setup['plotDir']+'/'+setup['plotSubDir']+'/nnValidation'+'.root')
  del mlpa_canvas
#
#  ROOT.gROOT.ProcessLine('.x ./../../HEPHYPythonTools/mva/tmvaMacros/correlations.C("'+setup['TMVAOutputFile']+'")')
#  os.system('mv ./plots/CorrelationMatrix*.* '+setup['plotDir']+'/'+setup['plotSubDir']+'/')
#  for s in setup['plotTransformations']:
#    ROOT.gROOT.ProcessLine('.x ./../../HEPHYPythonTools/mva/tmvaMacros/variables.C("'+setup['TMVAOutputFile']+'", "InputVariables_'+s+'")')
#    os.system('mv ./plots/variables_*  '+setup['plotDir']+'/'+setup['plotSubDir']+'/')
#    if setup['makeCorrelationScatterPlots']:
#      for v in setup['mvaInputObs']:
#        ROOT.gROOT.ProcessLine('.x ./../../HEPHYPythonTools/mva/tmvaMacros/correlationscatters.C("'+setup['TMVAOutputFile']+'","'+v+'", "InputVariables_'+s+'")')
#      os.system('mv ./plots/correlationscatter_* '+setup['plotDir']+'/'+setup['plotSubDir']+'/')
#
#  for m in methods:
#    if m['type']!=ROOT.TMVA.Types.kCuts:
#      ROOT.gROOT.ProcessLine('.x ./../../HEPHYPythonTools/mva/tmvaMacros/network.C("'+setup['TMVAOutputFile']+'")')
#      os.system('mv ./plots/'+m['name']+'.png  '+setup['plotDir']+'/'+setup['plotSubDir']+'/netStructure_'+m['name']+'.png')
#      os.system('mv ./plots/'+m['name']+'.pdf  '+setup['plotDir']+'/'+setup['plotSubDir']+'/netStructure_'+m['name']+'.pdf')
#      os.system('mv ./plots/'+m['name']+'.root '+setup['plotDir']+'/'+setup['plotSubDir']+'/netStructure_'+m['name']+'.root')
#      ROOT.gROOT.ProcessLine('.x ./../../HEPHYPythonTools/mva/tmvaMacros/efficiencies.C("'+setup['TMVAOutputFile']+'")')
#      os.system('mv ./plots/rejBvsS.png  '+setup['plotDir']+'/'+setup['plotSubDir']+'/rejBvsS_'+m['name']+'.png')
#      os.system('mv ./plots/rejBvsS.pdf  '+setup['plotDir']+'/'+setup['plotSubDir']+'/rejBvsS_'+m['name']+'.pdf')
#      os.system('mv ./plots/rejBvsS.root '+setup['plotDir']+'/'+setup['plotSubDir']+'/rejBvsS_'+m['name']+'.root')
#      if setup['plotMVAEffs']:
#        ROOT.gROOT.ProcessLine('.L ./../../HEPHYPythonTools/mva/tmvaMacros/mvaeffs.C+')
#        ROOT.gROOT.ProcessLine('mvaeffs("'+setup['TMVAOutputFile']+'")')
#        os.system('mv ./plots/mvaeffs_'+m['name']+'.png  '+setup['plotDir']+'/'+setup['plotSubDir']+'/mvaeffs_'+m['name']+'.png')
#        os.system('mv ./plots/mvaeffs_'+m['name']+'.pdf  '+setup['plotDir']+'/'+setup['plotSubDir']+'/mvaeffs_'+m['name']+'.pdf')
#        os.system('mv ./plots/mvaeffs_'+m['name']+'.root '+setup['plotDir']+'/'+setup['plotSubDir']+'/mvaeffs_'+m['name']+'.root')
#      for i, fname in enumerate(['mva', 'proba', 'rarity', 'overtrain']):
##        print '.x ./../../HEPHYPythonTools/mva/tmvaMacros/mvas.C("'+setup['TMVAOutputFile']+','+str(i)+'")'
#        ROOT.gROOT.ProcessLine('.x ./../../HEPHYPythonTools/mva/tmvaMacros/mvas.C("'+setup['TMVAOutputFile']+'",'+str(i)+')')
#        os.system('mv ./plots/'+fname+'_'+m['name']+'.png  '+setup['plotDir']+'/'+setup['plotSubDir']+'/'+fname+'_'+m['name']+'.png')
#        os.system('mv ./plots/'+fname+'_'+m['name']+'.pdf  '+setup['plotDir']+'/'+setup['plotSubDir']+'/'+fname+'_'+m['name']+'.pdf')
#        os.system('mv ./plots/'+fname+'_'+m['name']+'.root '+setup['plotDir']+'/'+setup['plotSubDir']+'/'+fname+'_'+m['name']+'.root')
#    if m['type']==ROOT.TMVA.Types.kMLP:
#      ROOT.gROOT.ProcessLine('.x ./../../HEPHYPythonTools/mva/tmvaMacros/annconvergencetest.C("'+setup['TMVAOutputFile']+'")')
#      os.system('mv ./plots/annconvergencetest.png  '+setup['plotDir']+'/'+setup['plotSubDir']+'/annconvergencetest_'+m['name']+'.png')
#      os.system('mv ./plots/annconvergencetest.pdf  '+setup['plotDir']+'/'+setup['plotSubDir']+'/annconvergencetest_'+m['name']+'.pdf')
#      os.system('mv ./plots/annconvergencetest.root '+setup['plotDir']+'/'+setup['plotSubDir']+'/annconvergencetest_'+m['name']+'.root')
#    if m['type']==ROOT.TMVA.Types.kBDT:
#      ROOT.gROOT.ProcessLine('.x ./../../HEPHYPythonTools/mva/tmvaMacros/BDTControlPlots.C("'+setup['TMVAOutputFile']+'")')
#      os.system('mv ./plots/'+m['name']+'_ControlPlots.png  '+setup['plotDir']+'/'+setup['plotSubDir']+'/'+m['name']+'_ControlPlots.png')
#      os.system('mv ./plots/'+m['name']+'_ControlPlots.pdf  '+setup['plotDir']+'/'+setup['plotSubDir']+'/'+m['name']+'_ControlPlots.pdf')
#      os.system('mv ./plots/'+m['name']+'_ControlPlots.root '+setup['plotDir']+'/'+setup['plotSubDir']+'/'+m['name']+'_ControlPlots.root')
##      ROOT.gROOT.ProcessLine('.x ./../../HEPHYPythonTools/mva/tmvaMacros/BoostControlPlots.C("'+setup['TMVAOutputFile']+'")')
#
#
#  ROOT.gROOT.cd(olddir)
#
#  coord_canvas = ROOT.TCanvas('coord_canvas', 'Network Coordinates',1200, 400*(1+len(methods)))
#  coord_canvas.SetFillColor(ROOT.kWhite)
#  inp = ":".join(setup['mvaInputObs'])
#
#  namesOfDrawnMethods = []
#  for m in methods:
#    if m.has_key("drawInParallelCoord") and m["drawInParallelCoord"]:
#      inp+=":"+m["name"]
#      namesOfDrawnMethods.append(m["name"])
#  coord_canvas.Divide(1,2)
#  coord_canvas.cd(1)
#  t.Draw("classID:"+inp,"classID==1","PARA")
#  para_sig=ROOT.gPad.GetListOfPrimitives().FindObject("ParaCoord")
## para_sig.SetGlobalLogScale(True)
##  print 'CoordAxis-Style ',para.GetGlobalScale()
#  para_sig.SetAxisHistogramBinning(500)
#  para_sig.SetTitle('Signal')
#  para_sig.SetDotsSpacing(5)
#  selVars={}
#  for nm in namesOfDrawnMethods:
#    selVars[nm] = para_sig.GetVarList().FindObject(nm);
#    selVars[nm].AddRange(ROOT.TParallelCoordRange(selVars[nm],0.9,2))
#    para_sig.AddSelection("highDisc")
#    para_sig.GetCurrentSelection().SetLineColor(ROOT.kViolet)
#
#  coord_canvas.cd(2)
#  del para_sig
#  t.Draw("classID:"+inp,"classID==0","PARA")
#  para_bkg=ROOT.gPad.GetListOfPrimitives().FindObject("ParaCoord")
#  para_bkg.SetAxisHistogramBinning(500)
## para_bkg.SetGlobalLogScale(True)
#  para_bkg.SetTitle('Background')
#  para_bkg.SetDotsSpacing(5)
#  selVars={}
#  for nm in namesOfDrawnMethods:
#    selVars[nm] = para_bkg.GetVarList().FindObject(nm);
#    selVars[nm].AddRange(ROOT.TParallelCoordRange(selVars[nm],0.7,2))
#    para_bkg.AddSelection("highDisc")
#    para_bkg.GetCurrentSelection().SetLineColor(ROOT.kViolet)
#
#
#  coord_canvas.Print(setup['plotDir']+'/'+setup['plotSubDir']+'/nnCoord.png')
#  t.IsA().Destructor(t)
#  del t
#  ROOT.gROOT.cd(olddir)
#  return

