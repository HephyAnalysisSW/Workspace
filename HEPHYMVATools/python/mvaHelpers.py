def getTrainingSampleSizes(countSignal, bkgs, fractionForTraining=0.5):
  """countSignal: Total count of signal sample.
  bkgs: [{'count':nBkg1,'yield':yBkg1},...,{'count':nBkgN,'yield':yBkgN}]]
  finds nbBkg1,...,nBkgN such that nBkg1+...+nBkgN is maximal while respecting
  nBkg1+nBkg2+...+nBkgN<=nSigTraining, nBkg1:nBkg2:...:nBkgN=yBkg1:yBkg2:...:yBkgN
  and nBkg1<=fractionForTraining*nBkg1Max, ...., fractionForTraining*nBkgNMax<=nBkgNMax
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

def constructDataset(setup, signal, backgrounds, overWrite = False):
  import os
  def getVarName(v):
    return v.split('/')[0]
  def getVarType(v):
    if v.count('/'): return v.split('/')[1]
    return 'F'

  if (not overWrite) and (not os.path.isfile(setup['dataFile'])):
    print "Not found:",setup['dataFile']
    return
  if (not os.path.isfile(setup['dataFile'])) or overWrite:
    print 'Creating MVA dataset',setup['dataFile']
    if overWrite and os.path.isfile(setup['dataFile']):
      print 'Warning! File will be overwritten'
    tree = ROOT.TTree('Events', 'Filtered Monte Carlo Events')

    varType={}

    for vn in setup['varsFromInputData']+[v[0] for v in setup['varsCalculated']]:
      varType[getVarName(vn)] = getVarType(vn)
    vars={}
    for vn in setup['varsFromInputData']:
      n = getVarName(vn)
      if varType[n]=='F': vars[n] = p_c_float(0.)
      if varType[n]=='I': vars[n] = ctypes.c_int(0)

    i_type      = ctypes.c_int(0)
    i_isTraining    = ctypes.c_int(0)
    for sample in [signal, background]:
      for k in vars.keys():
        sample.SetBranchAddress(k, vars[k])

    for k in vars.keys():
      tree.Branch(k, vars[k], k+'/'+varType[k])
#      print k, vars[k], k+'/'+varType[k], tree.GetBranch(k)
    tree.Branch('type'  ,   ctypes.addressof(i_type),     'type/I')
    tree.Branch('isTraining',   ctypes.addressof(i_isTraining),   'isTraining/I')
    addVars = {}
    for v in [getVarName(vn) for vn in  [v[0] for v in setup['varsCalculated']] ]:
      if varType[v]=='F': addVars[v] = ctypes.c_float(0.)
      if varType[v]=='I': addVars[v] = ctypes.c_int(0)
      if not ( varType[v]=='F' or varType[v]=='I') : print "Warning! Unknown varType'"+varType[v]+"'for variable", v
      tree.Branch(v,   ctypes.addressof(addVars[v]),   v+'/'+varType[v])
#      print v,   ctypes.addressof(addVars[v]),   v+'/'+varType[v]
#    eListSig = getEList(signal,        setup['preselection'], 'eListSig')
#    eListBkg = getEList(background,    setup['preselection'], 'eListBkg')

    for i_type.value , sample in [[ 1, signal], [0, background]]:
      if len(set(setup["backgroundTrainEvents"]) & set(setup["backgroundTestEvents"])) !=0:
        print "Warning: Bkg. train/test sets not exclusive!"
      if len(set(setup["signalTrainEvents"]) & set(setup["signalTestEvents"])) !=0:
        print "Warning: Sig. train/test sets not exclusive!"

      for i_isTraining.value in [0,1]:
        print 'signal?',i_type.value==1, ", train sample?",i_isTraining.value==0
        eventList = []
        if   (i_type.value == 0 and i_isTraining.value ==1):
          eventList = setup["backgroundTrainEvents"]
        elif (i_type.value == 1 and i_isTraining.value ==1):
          eventList = setup["signalTrainEvents"]
        elif (i_type.value == 0 and i_isTraining.value ==0):
          eventList = setup["backgroundTestEvents"]
        elif (i_type.value == 1 and i_isTraining.value ==0):
          eventList = setup["signalTestEvents"]
        if len(eventList)==0:
          print "Warning!! Empty event list for type", i_type.value,"isTraining", i_isTraining.value
        for i, ev in enumerate(eventList):
          if i%1000==0:print 'type',i_type.value, 'isTraining', i_isTraining.value, 'Event.:',i,'/',len(eventList)
#          sample.GetEntry(eList.GetEntry(ev))
          sample.GetEntry(ev)

          for v in setup["varsCalculated"]:
            vn = getVarName(v[0])
            if varType[vn] =="I":
              addVars[vn].value  = int(v[1](sample))
            if varType[vn] =="F":
              addVars[vn].value  = v[1](sample)
  #          print vn, addVars[vn].value#,      tree.GetLeaf(getVarName(v[0])).GetValue()
          tree.Fill()

    eListBkg          = getEList(tree,   'type==0&&'+ setup['preselection']    ,'eListBkg')
    eListSig          = getEList(tree,   'type==1&&'+ setup['preselection']    ,'eListSig')
    f = ROOT.TFile(setup['dataFile'], 'recreate')
    tree.Write()
    eListBkg.Write()
    eListSig.Write()
    f.Close()

    print 'Written MVA dataset to', setup['dataFile']
    setup['dataSetConfigFile'] = setup['dataFile'].replace('.root', '.pkl')
    setupStripped = copy.deepcopy(setup)
    setupStripped['varsCalculated'] = [v[:-1]+['removedFunction'] for v in setupStripped['varsCalculated']]

    for v in ['backgroundTrainEvents', 'signalTrainEvents', 'backgroundTestEvents', 'backgroundTrainEvents',  'backgroundAllTestEvents', 'signalAllTestEvents']:
      setupStripped[v]='removed'
    pickle.dump(setupStripped, file(setup['dataSetConfigFile'],"w"))

    print 'Written MVA setup to',setup['dataSetConfigFile']
    Events = ROOT.gDirectory.Get("Events")
    del Events
    del tree
    del eListBkg
    del eListSig
  print 'Loading MVA dataset from', setup['dataFile']
  g = ROOT.gDirectory.Get("Events")
  if g: del g
  tree      = getAnyObjFromFile(setup['dataFile'],'Events')
  eListBkg      = getAnyObjFromFile(setup['dataFile'],'eListBkg')
  eListSig      = getAnyObjFromFile(setup['dataFile'],'eListSig')
  print'Datasets and eLists:',tree, eListBkg,' ',eListSig
  print '...done.'
  return {'tree':tree, 'eListBkg':eListBkg, 'eListSig':eListSig}

