import ROOT
from array import array
import ctypes, pickle, os, sys, copy
from math import sqrt, cos, sin

ROOT.gROOT.ProcessLine(".L ../../HEPHYCommonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()

stuff=[]
p_c_float = ctypes.c_float * 1
#p_c_int = ctypes.c_int * 1

path = os.path.abspath('../../RA4Analysis/plots')
if not path in sys.path:
    sys.path.insert(1, path)
del path

def getObjFromFile(fname,hname):
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

def getVarValList( sample, variable, selection = ""):
  l = sample.GetLeaf(variable)
  res=[]
  if type(selection)==type(ROOT.TEventList()):
    for i in range(selection.GetN()) :
      sample.GetEntry(selection.GetEntry(i))
      val = l.GetValue()
      res.append(val)
  if type(selection)==type(""):
    sample.Draw(">>eListTMP", selection)
    eListTMP = ROOT.gDirectory.Get("eListTMP")
    for i in range(eListTMP.GetN()) :
      sample.GetEntry(eListTMP.GetEntry(i))
      val = l.GetValue()
      res.append(val)
    del eListTMP
  return res
  del l


def getEList(chain, cut, newname='eListTMP'):
  chain.Draw('>>eListTMP_t', cut)
  elistTMP_t = ROOT.gROOT.Get('eListTMP_t')
  elistTMP = elistTMP_t.Clone(newname)
  del elistTMP_t
  return elistTMP

def getPlot(chain, cut, var, binning=None):
# if (verbose):print 'chain:',chain,' cut:',cut,' var:',var,' binning:',binning[0],' ',binning[1],' ',binning[2]
  if binning:
    chain.Draw(var+'>>hTMP_t('+str(binning[0])+','+str(binning[1])+','+str(binning[2])+')', cut, 'goff')
  else:
    chain.Draw(var+'>>hTMP_t', cut, 'goff')
  
  hTMP_t = ROOT.gROOT.Get('hTMP_t')
  hTMP = hTMP_t.Clone(var)
  del hTMP_t
  return hTMP

#def makeLegend(Pos):
#  #Position: right up = rp
#  #Position: left up  = lp
#  if Pos == 'rp':
#    legend = r.TLegend(0.63,0.65,0.88,0.88)
#  if Pos == 'lp':
#    legend = r.TLegend(0.12,0.65,0.35,0.88)
#  legend.SetHeader("Legend of the Plot")
#  legend.SetFillColor(0)
#  return legend


#def getMacroPlots(TMVA_outputfile,macrotype,name

#def getMVACutPlot(chain, setup, cut, var, binning, weight='', nnBin = (-999, 999), weightFunc = None):
#  chain.Draw('>>eListTMP_t', cut)
#  eList = ROOT.gROOT.Get('eListTMP_t')
#  res  = ROOT.TH1F(var,var, *binning)
##  vars={}
##  for vn in setup['varsFromInputData']+setup['varsCalculated']:
##    vars[vn] = chain.GetLeaf(vn)
#  print 'var',var,'filling',eList.GetN()
#  for i in range(eList.GetN()):
#    chain.GetEntry(eList.GetEntry(i))
##    val = vars[var].GetValue()
#    if weight!='':
#      weightVal = vars[weight].GetValue()
#    if weightFunc:
#      weightVal = weightFunc(chain)
#    else:
#      weightVal = 1.
#    if nnBin[0]<=-999: #or nno>nnBin[0]:
#      if nnBin[1]>=999:#or nno<=nnBin[1]:
#        res.Fill(val, weightVal)
##        print i, val, weightVal, nno
#  del eList
#  return res.Clone()

#def getMVAOutput(tmlp, sample, eList, varNames, tinputs, result='plot', nbins=200, nnThreshold=-999.):
#  vars={}
##tmlp is 'MLP_ANN': output of TMVA
#  for vn in varNames:
#    vars[vn] = p_c_float(0.)
#  for k in vars.keys():
#    sample.SetBranchAddress(k, vars[k])
#  if result.lower()=='plot':
#    res =  ROOT.TH1F('bgh', 'NN output', nbins, -.5, 1.5)
#    res.Reset()
#  if result.lower()=='list':
#    res=[]
#  if result.lower()=='weightsum':
#    res=0.
#  for i in range(eList.GetN()) :
#    sample.GetEntry(eList.GetEntry(i))
###    if type(tmlp) == type(ROOT.TMultiLayerPerceptron()):
###      val = tmlp.Evaluate(0, array('d',[vars[k][0] for k in tinputs]))
###    else:
###      val = tmlp.value(0, *[vars[k][0] for k in tinputs])
#    if nnThreshold>-999. and val<=nnThreshold:continue
#    if result.lower()=='plot':
#      res.Fill(val)
#    if result.lower()=='list':
#      res.append(val)
#    if result.lower()=='weightsum':
#      res+=sample.GetLeaf('weight').GetValue()
#  return res

def getFOMPlot(bgDisc, sigDisc):
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

#if not ROOT.gROOT.GetClass('TMultiLayerPerceptron'):

def getVarName(v):
  return v.split('/')[0]
def getVarType(v):
  if v.count('/'): return v.split('/')[1]
  return 'F'

def constructDataset(setup, signal, background, overWrite = False, addAllTestEventsTree = False):
  if (not overWrite) and (not os.path.isfile(setup['dataFile'])):
    print "Not found:",setup['dataFile']
    return
  if (not os.path.isfile(setup['dataFile'])) or overWrite:
    print 'Creating MVA dataset',setup['dataFile']
    if overWrite and os.path.isfile(setup['dataFile']):
      print 'Warning! File will be overwritten'
    simu =  ROOT.TTree('MonteCarlo', 'Filtered Monte Carlo Events')
    test =  ROOT.TTree('allTestEvents', 'Filtered Monte Carlo Events')

    varType={}
    funcMapVarsFrominputSignal = {}
    listOfVarsFrominputSignal = []
    for v in setup['varsFromInputSignal']:
      if type(v)==type([]):
        listOfVarsFrominputSignal.append(v[0])
        funcMapVarsFrominputSignal[v[0]] = v[1]
      else:
        listOfVarsFrominputSignal.append(v)

    for vn in setup['varsFromInputData']+[v[0] for v in setup['varsCalculated']]+['weightForMVA'] + listOfVarsFrominputSignal:
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
#        print "Input data addresses", sample,k, vars[k], sample.GetBranch(k)
    f_testSampleScaleFac  = ctypes.c_float(0.) 

    for k in vars.keys():
      simu.Branch(k, vars[k], k+'/'+varType[k])
      if addAllTestEventsTree:
        test.Branch(k, vars[k], k+'/'+varType[k])
#      print k, vars[k], k+'/'+varType[k], simu.GetBranch(k)
    simu.Branch('type'  ,   ctypes.addressof(i_type),     'type/I')
    simu.Branch('isTraining',   ctypes.addressof(i_isTraining),   'isTraining/I')
    if addAllTestEventsTree:
      test.Branch('type'  ,   ctypes.addressof(i_type),     'type/I')
      test.Branch('testSampleScaleFac'  , ctypes.addressof(f_testSampleScaleFac),     'testSampleScaleFac/F')

    addVars = {}
    for v in [getVarName(vn) for vn in ['weightForMVA'] + [v[0] for v in setup['varsCalculated']] + listOfVarsFrominputSignal]:
      if varType[v]=='F': addVars[v] = ctypes.c_float(0.)
      if varType[v]=='I': addVars[v] = ctypes.c_int(0)
      if not ( varType[v]=='F' or varType[v]=='I') : print "Warning! Unknown varType'"+varType[v]+"'for variable", v
      simu.Branch(v,   ctypes.addressof(addVars[v]),   v+'/'+varType[v])
      if addAllTestEventsTree:
        test.Branch(v,   ctypes.addressof(addVars[v]),   v+'/'+varType[v])
      print v,   ctypes.addressof(addVars[v]),   v+'/'+varType[v]
#    eListSig = getEList(signal,        setup['preselection'], 'eListSig')
#    eListBkg = getEList(background,    setup['preselection'], 'eListBkg')

    for i_type.value , sample in [[ 1, signal], [0, background]]:
      mvaWeightFac=1
      if i_type.value==1:
        if setup.has_key('sigMVAWeightFac'):
          mvaWeightFac = setup["sigMVAWeightFac"]
      else:
        if setup.has_key('bkgMVAWeightFac'):
          mvaWeightFac = setup["bkgMVAWeightFac"]

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
          if type(setup['weightForMVA']['weight'])!=type(""):
            weight =  setup['weightForMVA']['weight']
          else: 
            weight = sample.GetLeaf(setup['weightForMVA']['weight']).GetValue()
          if i_type.value==1:
            for v in listOfVarsFrominputSignal:
              vn = getVarName(v)
              if funcMapVarsFrominputSignal.has_key(v):
                val = funcMapVarsFrominputSignal[v](sample)
              else:
                val = sample.GetLeaf(vn).GetValue()
              if varType[vn] =="I":
                addVars[vn].value  = int(val)
              if varType[vn] =="F":
                addVars[vn].value  = float(val) 
            addVars['weightForMVA'].value  = weight*setup['weightForMVA']['sigFac']*mvaWeightFac
  #          print addVars['weightForMVA'].value, weight, setup['weightForMVA']['sigFac'], mvaWeightFac
          else:
            for v in listOfVarsFrominputSignal:
              vn = getVarName(v)
              if varType[vn] =="I":
                addVars[vn].value  = 0
              if varType[vn] =="F":
                addVars[vn].value  = float('nan') 
            addVars['weightForMVA'].value  = weight*setup['weightForMVA']['bkgFac']*mvaWeightFac
  #          print addVars['weightForMVA'].value, weight, setup['weightForMVA']['bkgFac'], mvaWeightFac
          for v in setup["varsCalculated"]:
            vn = getVarName(v[0])
            if varType[vn] =="I":
              addVars[vn].value  = int(v[1](sample))
            if varType[vn] =="F":
              addVars[vn].value  = v[1](sample)
  #          print vn, addVars[vn].value#,      simu.GetLeaf(getVarName(v[0])).GetValue()
          simu.Fill()
    if addAllTestEventsTree:
      print "Make scaled test sample from the rest of events:"
      for i_type.value , sample in [[ 1, signal], [0, background]]:
        print 'signal?',i_type.value==1
        eventList = []
        if (i_type.value == 0):
          eventList = setup["backgroundAllTestEvents"] 
        elif (i_type.value == 1):
          eventList = setup["signalAllTestEvents"] 
        if len(eventList)==0:
          print "Warning!! Empty event list for type", i_type.value
        for i, ev_ in enumerate(eventList):
          ev, scaleFac = ev_
          if i%10000==0:print 'type',i_type.value, 'isTraining', i_isTraining.value, 'Event.:',i,'/',len(eventList)
  #          sample.GetEntry(eList.GetEntry(ev))
          sample.GetEntry(ev)
          f_testSampleScaleFac.value  = scaleFac
          if i_type.value==1:
            for v in listOfVarsFrominputSignal:
              vn = getVarName(v)
              if funcMapVarsFrominputSignal.has_key(v):
                val = funcMapVarsFrominputSignal[v](sample)
              else:
                val = sample.GetLeaf(vn).GetValue()
              if varType[vn] =="I":
                addVars[vn].value  = int(val)
              if varType[vn] =="F":
                addVars[vn].value  = float(val) 
          else:
            for v in listOfVarsFrominputSignal:
              vn = getVarName(v)
              if varType[vn] =="I":
                addVars[vn].value  = 0
              if varType[vn] =="F":
                addVars[vn].value  = float('nan') 
          for v in setup["varsCalculated"]:
            vn = getVarName(v[0])
            if varType[vn] =="I":
              addVars[vn].value  = int(v[1](sample))
            if varType[vn] =="F":
              addVars[vn].value  = v[1](sample)
  #          print vn, addVars[vn].value#,      simu.GetLeaf(getVarName(v[0])).GetValue()
          test.Fill()

    eListBkg          = getEList(simu,   'type==0&&'+ setup['preselection']    ,'eListBkg')
    eListSig          = getEList(simu,   'type==1&&'+ setup['preselection']    ,'eListSig')
    f = ROOT.TFile(setup['dataFile'], 'recreate')
    simu.Write()
    if addAllTestEventsTree:
      test.Write()
    eListBkg.Write()
    eListSig.Write()
    f.Close()

    print 'Written MVA dataset to', setup['dataFile']
    setup['dataSetConfigFile'] = setup['dataFile'].replace('.root', '.pkl')
    setupStripped = copy.deepcopy(setup)
    setupStripped['varsCalculated'] = [v[:-1]+['removedFunction'] for v in setupStripped['varsCalculated']]
    setupStripped['varsFromInputSignal'] = [v[:-1]+['removedFunction'] for v in setupStripped['varsFromInputSignal']]
    for v in ['backgroundTrainEvents', 'signalTrainEvents', 'backgroundTestEvents', 'backgroundTrainEvents',  'backgroundAllTestEvents', 'signalAllTestEvents']:
      setupStripped[v]='removed' 
    pickle.dump(setupStripped, file(setup['dataSetConfigFile'],"w"))

    print 'Written MVA setup to',setup['dataSetConfigFile'] 
    Events = ROOT.gDirectory.Get("Events")
    del Events
    del simu
    if addAllTestEventsTree:
      del test
    del eListBkg
    del eListSig
  print 'Loading MVA dataset from', setup['dataFile']
  g = ROOT.gDirectory.Get("MonteCarlo")
  if g: del g
  simu      = getObjFromFile(setup['dataFile'],'MonteCarlo')
  test      = getObjFromFile(setup['dataFile'],'allTestEvents')
  eListBkg      = getObjFromFile(setup['dataFile'],'eListBkg')
  eListSig      = getObjFromFile(setup['dataFile'],'eListSig')
  print'Datasets and eLists:',simu, test, eListBkg,' ',eListSig
  print '...done.'
#  return {'simu':simu, 'eListBkgTest':eListBkgTest, 'eListSigTest':eListSigTest, 'eListBkgTraining':eListBkgTraining, 'eListSigTraining':eListSigTraining, 'eListBkg':eListBkg, 'eListSig':eListSig, 'eListTest':eListTest, 'eListTraining':eListTraining}
  return {'simu':simu, 'allTestEvents':test, 'eListBkg':eListBkg, 'eListSig':eListSig}


def getConstSoverSqrtBFunc(l, bkgXsec, sigXsec, bkgPreselectionEff, sigPreselectionEff, const):
  return ROOT.TF1('func', '1. - '+str(l)+'*('+str(sigPreselectionEff)+'*'+str(sigXsec)+'*x/'+str(const)+')**2/('+str(bkgPreselectionEff)+'*'+str(bkgXsec)+')', 0, 1)


def setupMVAFrameWork(setup, data, methods, prefix):
  olddir = ROOT.gDirectory.CurrentDirectory().GetName()+':/'
  vstring=''
  for v in setup['mvaInputVars']:
    vstring+=getVarName(v)+','
  vstring = vstring[:-1]

#  lstring=':'.join(str(i) for i in setup['NN_layers'])

  print 'Instancing of TMVA Factory:'

  ROOT.TMVA.Tools.Instance()
  ROOT.TMVA.gConfig().GetIONames().fWeightFileDir = setup['weightDir']
  ROOT.TMVA.gConfig().GetVariablePlotting().fNbinsXOfROCCurve = 200

  fout = ROOT.TFile(setup['TMVAOutputFile'],"RECREATE")
  factory = ROOT.TMVA.Factory("TMVAClassification", fout,":".join(setup['TMVAFactoryOptions']))
  factory.DeleteAllMethods()


  varType={}
  for vn in setup['varsFromInputData']+[v[0] for v in setup['varsCalculated']]+['weightForMVA']:
    varType[getVarName(vn)] = getVarType(vn)

  for v in setup['mvaInputVars']:
    print "Adding to factory variable", v, 'of type', varType[v] 
    factory.AddVariable(getVarName(v), varType[v])

#  sigCut = ROOT.TCut("type==1&&"+setup['preselection'])
#  bgCut = ROOT.TCut("type==0&&"+setup['preselection'])
#  factory.PrepareTrainingAndTestTree(sigCut,bgCut,":".join(setup["datasetFactoryOptions"]))

#  nEvents = data['simu'].GetEntries()
#  nBkgTrain=0
#  nSigTrain=0
#  nBkgTest=0
#  nSigTest=0
#  for ievent in range(nEvents):
#    data['simu'].GetEntry(ievent)
#    isTraining =  int(data['simu'].GetLeaf('isTraining').GetValue())
#    type =  int(data['simu'].GetLeaf('type').GetValue())
##    print isTraining, type
#    if (type == 0 and isTraining == 1):
#      eventBookMethod = factory.AddBackgroundTrainingEvent
#      nBkgTrain+=1
#    if (type == 1 and isTraining ==1):
#      eventBookMethod = factory.AddSignalTrainingEvent
#      nSigTrain+=1
#    if (type == 0 and isTraining ==0):
#      eventBookMethod = factory.AddBackgroundTestEvent
#      nBkgTest+=1
#    if (type == 1 and isTraining ==0):
#      eventBookMethod = factory.AddSignalTestEvent
#      nSigTest+=1
#    if (not ( (type == 1) or (type == 0)) ) or not ((isTraining == 1) or (isTraining == 0)):
#      print "Warning!",isTraining,type
#    vals = ROOT.std.vector('double')()
#    for v in setup['mvaInputVars'] : vals.push_back(data['simu'].GetLeaf(v).GetValue())
##    print eventBookMethod, vals,isTraining,type
#    eventBookMethod(vals, data['simu'].GetLeaf('weightForMVA').GetValue()) 
#    del vals
#  print "Booked Events: Train(Bkg/Sig)", str(nBkgTrain)+"/"+str(nSigTrain),"Test(Bkg/Sig)",str(nBkgTest)+"/"+str(nSigTest)

  bkgTestTree =   data['simu'].CopyTree("isTraining==0&&type==0")
  sigTestTree =   data['simu'].CopyTree("isTraining==0&&type==1")
  bkgTrainTree =  data['simu'].CopyTree("isTraining==1&&type==0")
  sigTrainTree =  data['simu'].CopyTree("isTraining==1&&type==1")
  factory.AddBackgroundTree( bkgTrainTree,  1.0, "Training" );
  factory.AddBackgroundTree( bkgTestTree,   1.0,  "Test" );
  factory.AddSignalTree( sigTrainTree,      1.0, "Training" );
  factory.AddSignalTree( sigTestTree,       1.0,  "Test" );
  factory.SetBackgroundWeightExpression("weightForMVA")
  factory.SetSignalWeightExpression(    "weightForMVA")

#  factory.AddSignalTree(data['simu'])
#  factory.AddBackgroundTree(data['simu'])
  
  #Fill training/test dataset event by event  

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
  setupStripped = copy.deepcopy(setup)
  setupStripped['varsCalculated'] = [v[:-1]+['removedFunction'] for v in setupStripped['varsCalculated']]

  pickle.dump(setupStripped, file(pfile,"w"))
  print "Stored setup in",pfile

  mlpa_canvas = ROOT.TCanvas('mlpa_canvas', 'Network analysis', 1200, 400*(1+len(methods)))
  mlpa_canvas.SetFillColor(ROOT.kWhite)
  mlpa_canvas.Divide(2,1+len(methods))
  ROOT.setTDRStyle()

  nbinsFine = 2000

  for j, m in enumerate(methods):
    for i, treeName in enumerate(['Test', 'Train']):
      l = ROOT.TLegend(.65, .80, 0.99, 0.99)
      t = getObjFromFile(setup['TMVAOutputFile'], treeName+'Tree')
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
  print 'Now FOM from TMVA will be done...'
  pad.SetGrid()
  l5 = ROOT.TLegend(.16, .13, 0.5, 0.35)
  opt=""
  for m in methods:
    histFOM = getObjFromFile(setup['TMVAOutputFile'],'MVA_'+m['name']+'_rejBvsS')
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

  bkgPreselectionEff = data['simu'].GetEntries('type==0&&'+setup['preselection'])/float(data['simu'].GetEntries('type==0'))
  sigPreselectionEff = data['simu'].GetEntries('type==1&&'+setup['preselection'])/float(data['simu'].GetEntries('type==1'))
  lumi = 19400.
#  sigEffForOneEvent = 1./(sigPreselectionEff*setup['sigXsec']*lumi)

#  sOverSqrtBvalues = [1, 2, 3, 4, 5]
  sOverSqrtBvalues = []
  sOverSqrtBfuncs = {}
  for c in sOverSqrtBvalues:
    sOverSqrtBfuncs[c]=getConstSoverSqrtBFunc(lumi, setup['bkgXsec'], setup['sigXsec'], bkgPreselectionEff, sigPreselectionEff, c)
  pad.SetGrid()
  l3 = ROOT.TLegend(.16, .13, 0.5, 0.5)
  l3.SetFillColor(ROOT.kWhite)
  l3.SetShadowColor(ROOT.kWhite)
  l3.SetBorderSize(1)
  opt="AL"
  for m in methods:
    m['FOMFromFile'] = getObjFromFile(setup['TMVAOutputFile'],'MVA_'+m['name']+'_rejBvsS')
    m['FOMFromFile'].SetStats(False)
    m['FOMFromFile'].SetLineColor(m['lineColor'])

    m['FOMFromTree'] = getFOMPlot(m['hbgTestFine'], m['hsigTestFine'])
    m['FOMFromTree']['central'].SetLineColor(m['lineColor'])
    if setup.has_key('fomPlotZoomCoordinates'):
      coord = setup['fomPlotZoomCoordinates']
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
  t = getObjFromFile(setup['TMVAOutputFile'], 'TestTree')
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

  ROOT.gROOT.ProcessLine('.x ./../../HEPHYCommonTools/mva/tmvaMacros/correlations.C("'+setup['TMVAOutputFile']+'")')
  os.system('mv ./plots/CorrelationMatrix*.* '+setup['plotDir']+'/'+setup['plotSubDir']+'/')
  for s in setup['plotTransformations']:
    ROOT.gROOT.ProcessLine('.x ./../../HEPHYCommonTools/mva/tmvaMacros/variables.C("'+setup['TMVAOutputFile']+'", "InputVariables_'+s+'")')
    os.system('mv ./plots/variables_*  '+setup['plotDir']+'/'+setup['plotSubDir']+'/')
    if setup['makeCorrelationScatterPlots']:
      for v in setup['mvaInputVars']:
        ROOT.gROOT.ProcessLine('.x ./../../HEPHYCommonTools/mva/tmvaMacros/correlationscatters.C("'+setup['TMVAOutputFile']+'","'+v+'", "InputVariables_'+s+'")')
      os.system('mv ./plots/correlationscatter_* '+setup['plotDir']+'/'+setup['plotSubDir']+'/')

  for m in methods:
    if m['type']!=ROOT.TMVA.Types.kCuts:
      ROOT.gROOT.ProcessLine('.x ./../../HEPHYCommonTools/mva/tmvaMacros/network.C("'+setup['TMVAOutputFile']+'")')
      os.system('mv ./plots/'+m['name']+'.png  '+setup['plotDir']+'/'+setup['plotSubDir']+'/netStructure_'+m['name']+'.png')
      os.system('mv ./plots/'+m['name']+'.pdf  '+setup['plotDir']+'/'+setup['plotSubDir']+'/netStructure_'+m['name']+'.pdf')
      os.system('mv ./plots/'+m['name']+'.root '+setup['plotDir']+'/'+setup['plotSubDir']+'/netStructure_'+m['name']+'.root')
      ROOT.gROOT.ProcessLine('.x ./../../HEPHYCommonTools/mva/tmvaMacros/efficiencies.C("'+setup['TMVAOutputFile']+'")')
      os.system('mv ./plots/rejBvsS.png  '+setup['plotDir']+'/'+setup['plotSubDir']+'/rejBvsS_'+m['name']+'.png')
      os.system('mv ./plots/rejBvsS.pdf  '+setup['plotDir']+'/'+setup['plotSubDir']+'/rejBvsS_'+m['name']+'.pdf')
      os.system('mv ./plots/rejBvsS.root '+setup['plotDir']+'/'+setup['plotSubDir']+'/rejBvsS_'+m['name']+'.root')
      if setup['plotMVAEffs']:
        ROOT.gROOT.ProcessLine('.L ./../../HEPHYCommonTools/mva/tmvaMacros/mvaeffs.C+')
        ROOT.gROOT.ProcessLine('mvaeffs("'+setup['TMVAOutputFile']+'")')
        os.system('mv ./plots/mvaeffs_'+m['name']+'.png  '+setup['plotDir']+'/'+setup['plotSubDir']+'/mvaeffs_'+m['name']+'.png')
        os.system('mv ./plots/mvaeffs_'+m['name']+'.pdf  '+setup['plotDir']+'/'+setup['plotSubDir']+'/mvaeffs_'+m['name']+'.pdf')
        os.system('mv ./plots/mvaeffs_'+m['name']+'.root '+setup['plotDir']+'/'+setup['plotSubDir']+'/mvaeffs_'+m['name']+'.root')
      for i, fname in enumerate(['mva', 'proba', 'rarity', 'overtrain']):
#        print '.x ./../../HEPHYCommonTools/mva/tmvaMacros/mvas.C("'+setup['TMVAOutputFile']+','+str(i)+'")'
        ROOT.gROOT.ProcessLine('.x ./../../HEPHYCommonTools/mva/tmvaMacros/mvas.C("'+setup['TMVAOutputFile']+'",'+str(i)+')')
        os.system('mv ./plots/'+fname+'_'+m['name']+'.png  '+setup['plotDir']+'/'+setup['plotSubDir']+'/'+fname+'_'+m['name']+'.png')
        os.system('mv ./plots/'+fname+'_'+m['name']+'.pdf  '+setup['plotDir']+'/'+setup['plotSubDir']+'/'+fname+'_'+m['name']+'.pdf')
        os.system('mv ./plots/'+fname+'_'+m['name']+'.root '+setup['plotDir']+'/'+setup['plotSubDir']+'/'+fname+'_'+m['name']+'.root')
    if m['type']==ROOT.TMVA.Types.kMLP:
      ROOT.gROOT.ProcessLine('.x ./../../HEPHYCommonTools/mva/tmvaMacros/annconvergencetest.C("'+setup['TMVAOutputFile']+'")')
      os.system('mv ./plots/annconvergencetest.png  '+setup['plotDir']+'/'+setup['plotSubDir']+'/annconvergencetest_'+m['name']+'.png')
      os.system('mv ./plots/annconvergencetest.pdf  '+setup['plotDir']+'/'+setup['plotSubDir']+'/annconvergencetest_'+m['name']+'.pdf')
      os.system('mv ./plots/annconvergencetest.root '+setup['plotDir']+'/'+setup['plotSubDir']+'/annconvergencetest_'+m['name']+'.root')
    if m['type']==ROOT.TMVA.Types.kBDT:
      ROOT.gROOT.ProcessLine('.x ./../../HEPHYCommonTools/mva/tmvaMacros/BDTControlPlots.C("'+setup['TMVAOutputFile']+'")')
      os.system('mv ./plots/'+m['name']+'_ControlPlots.png  '+setup['plotDir']+'/'+setup['plotSubDir']+'/'+m['name']+'_ControlPlots.png')
      os.system('mv ./plots/'+m['name']+'_ControlPlots.pdf  '+setup['plotDir']+'/'+setup['plotSubDir']+'/'+m['name']+'_ControlPlots.pdf')
      os.system('mv ./plots/'+m['name']+'_ControlPlots.root '+setup['plotDir']+'/'+setup['plotSubDir']+'/'+m['name']+'_ControlPlots.root')
#      ROOT.gROOT.ProcessLine('.x ./../../HEPHYCommonTools/mva/tmvaMacros/BoostControlPlots.C("'+setup['TMVAOutputFile']+'")')
            

  ROOT.gROOT.cd(olddir)

  coord_canvas = ROOT.TCanvas('coord_canvas', 'Network Coordinates',1200, 400*(1+len(methods)))
  coord_canvas.SetFillColor(ROOT.kWhite)
  inp = ":".join(setup['mvaInputVars'])

  namesOfDrawnMethods = []
  for m in methods:
    if m.has_key("drawInParallelCoord") and m["drawInParallelCoord"]:
      inp+=":"+m["name"]
      namesOfDrawnMethods.append(m["name"])
  coord_canvas.Divide(1,2)
  coord_canvas.cd(1)
  t.Draw("classID:"+inp,"classID==1","PARA")
  para_sig=ROOT.gPad.GetListOfPrimitives().FindObject("ParaCoord")
# para_sig.SetGlobalLogScale(True)
#  print 'CoordAxis-Style ',para.GetGlobalScale()
  para_sig.SetAxisHistogramBinning(500)
  para_sig.SetTitle('Signal')
  para_sig.SetDotsSpacing(5)
  selVars={}
  for nm in namesOfDrawnMethods:
    selVars[nm] = para_sig.GetVarList().FindObject(nm);
    selVars[nm].AddRange(ROOT.TParallelCoordRange(selVars[nm],0.9,2))
    para_sig.AddSelection("highDisc")
    para_sig.GetCurrentSelection().SetLineColor(ROOT.kViolet)

  coord_canvas.cd(2)
  del para_sig
  t.Draw("classID:"+inp,"classID==0","PARA")
  para_bkg=ROOT.gPad.GetListOfPrimitives().FindObject("ParaCoord")
  para_bkg.SetAxisHistogramBinning(500)
# para_bkg.SetGlobalLogScale(True)
  para_bkg.SetTitle('Background')
  para_bkg.SetDotsSpacing(5)
  selVars={}
  for nm in namesOfDrawnMethods:
    selVars[nm] = para_bkg.GetVarList().FindObject(nm);
    selVars[nm].AddRange(ROOT.TParallelCoordRange(selVars[nm],0.7,2))
    para_bkg.AddSelection("highDisc")
    para_bkg.GetCurrentSelection().SetLineColor(ROOT.kViolet)


  coord_canvas.Print(setup['plotDir']+'/'+setup['plotSubDir']+'/nnCoord.png')
  t.IsA().Destructor(t)
  del t
  ROOT.gROOT.cd(olddir)
  return

def getYield(sample, setup, reader, method, cut, nnCutVal, weight='weight', weightFunc = None):
  res=0.
  l = getEList(sample, cut)
  for i in range(l.GetN()):
    sample.GetEntry(l.GetEntry(i))
    inputs = ROOT.std.vector('float')()
    for var in setup['mvaInputVars']:
      val = sample.GetLeaf(var).GetValue()
#      vars[var][0] = val
    #inputs = array('f', [sample.GetLeaf(var).GetValue() for var in setup['mvaInputVars']])
      inputs.push_back(val)
#    print inputs
    if method['type']!=ROOT.TMVA.Types.kCuts:
      nno =   reader.EvaluateMVA(inputs,  method['name'])
      if weightFunc:
        w = weightFunc(sample)
      else:
        w = sample.GetLeaf(weight).GetValue() 
      if nno>=nnCutVal:
        res+=w
    else:
      if nnCutVal<0:
        nno=1
      else:
        nno =   reader.EvaluateMVA(inputs,  method['name'], nnCutVal)
      if weightFunc:
        w = weightFunc(sample)
      else:
        w = sample.GetLeaf(weight).GetValue() 
      if nno:res+=w
  del l
  return res

def fillHistoAfterMVA(sample, setup, reader, method, cut, var, histo, mvaBin = [-999,999], weight=None, weightFunc = None):
  histo.Reset()
  l = getEList(sample, cut)
  for i in range(l.GetN()):
    sample.GetEntry(l.GetEntry(i))
    inputs = ROOT.std.vector('float')()
    for v in setup['mvaInputVars']:
      val = sample.GetLeaf(v).GetValue()
      inputs.push_back(val)
    if weight:
      if type(weight)!=type(""):
        w=weight
      else:
        w=sample.GetLeaf(weight).GetValue()
    if weightFunc:
      w = weightFunc(sample)
    if method['type']!=ROOT.TMVA.Types.kCuts:
      nno =   reader.EvaluateMVA(inputs,  method['name'])
    if nno>mvaBin[0] and nno<=mvaBin[1]:
      if type(var)==type(""):
        histo.Fill(sample.GetLeaf(var).GetValue(), w)
      else:
        histo.Fill(var(sample), w)
  return histo

def fillMVAHisto(sample, setup, reader, method, cut, histo, weight=None, weightFunc = None):
  histo.Reset()
  l = getEList(sample, cut)
  for i in range(l.GetN()):
    sample.GetEntry(l.GetEntry(i))
    inputs = ROOT.std.vector('float')()
    for var in setup['mvaInputVars']:
      val = sample.GetLeaf(var).GetValue()
      inputs.push_back(val)
    if weight:
      if type(weight)!=type(""):
        w=weight
      else:
        w=sample.GetLeaf(weight).GetValue()
    if weightFunc:
      w = weightFunc(sample)
    if method['type']!=ROOT.TMVA.Types.kCuts:
      nno =   reader.EvaluateMVA(inputs,  method['name'])
    histo.Fill(nno, w)
  return histo


def getYieldFromChain(c, cut, weight = "weight"):
  cut = weight+"*("+cut+")"
  c.Draw("1>>htmp(1,0,2)", cut, "goff")
  htmp =  ROOT.gDirectory.Get("htmp")
  res = htmp.Integral()
  del htmp
  return res

def getCutYieldFromChain(c, cutString = "(1)", cutFunc = None, weight = "weight"):
  c.Draw(">>eList", cutString)
  elist = ROOT.gDirectory.Get("eList")
  number_events = elist.GetN()
  res = 0.
  for i in range(number_events): #Loop over those events
    c.GetEntry(elist.GetEntry(i))
    if (not cutFunc) or cutFunc(c):
      w = c.GetLeaf(weight).GetValue()
      res += w
  del elist
  return res

