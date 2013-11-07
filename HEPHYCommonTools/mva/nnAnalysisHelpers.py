import ROOT
from array import array
import ctypes, pickle, os, sys, copy 
from math import sqrt, cos, sin

ROOT.gROOT.ProcessLine(".L ../../HEPHYCommonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()

stuff=[]
p_c_float = ctypes.c_float * 1
p_c_int = ctypes.c_int * 1

path = os.path.abspath('../../RA4Analysis/plots')
if not path in sys.path:
    sys.path.insert(1, path)
from xsecSMS import gluino8TeV_NLONLL, gluino14TeV_NLO
del path

def getObjFromFile(fname,hname):
  olddir = ROOT.gDirectory.CurrentDirectory().GetName()+':/'
  if type(fname)==type(""):
    f = ROOT.TFile.Open(fname)
  else: f=fname
  obj_t = f.FindObjectAny(hname)
  if obj_t == None: print 'File ('+hname+') not found!'
  ROOT.gDirectory.cd(olddir)

  if type(obj_t) == type(ROOT.TTree()):
    obj = obj_t.CloneTree()
  else:
    obj = obj_t.Clone()
  if type(fname)==type(""):
    f.Close()
  return obj             

def getVarValList( sample, eList, variable ):
  l = sample.GetLeaf(variable)
  res=[]
  for i in range(eList.GetN()) :
    sample.GetEntry(eList.GetEntry(i))
    val = l.GetValue()
    res.append(val)
#    print i, variable, val
  return res
  del l


def getEList(chain, cut, newname='eListTMP'):
  chain.Draw('>>eListTMP_t', cut)
  elistTMP_t = ROOT.gROOT.Get('eListTMP_t')
  elistTMP = elistTMP_t.Clone(newname) 
  del elistTMP_t
  return elistTMP

def getPlot(chain, cut, var, binning):
# if (verbose):print 'chain:',chain,' cut:',cut,' var:',var,' binning:',binning[0],' ',binning[1],' ',binning[2]
  chain.Draw(var+'>>hTMP_t('+str(binning[0])+','+str(binning[1])+','+str(binning[2])+')', cut, 'goff')
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


def getNNCutPlot(data, setup, cut, var, binning, weight, tmlp, nnBin = (-999, 999)):
  chain = data['simu']
  chain.Draw('>>eListTMP_t', cut)
  eList = ROOT.gROOT.Get('eListTMP_t')
  res  = ROOT.TH1F(var,var, *binning)
  vars={}
  for vn in setup['varNames']+setup['additionalVars']:
    vars[vn] = chain.GetLeaf(vn) 
  print 'var',var,'filling',eList.GetN()
  for i in range(eList.GetN()):
    chain.GetEntry(eList.GetEntry(i))
##    if type(tmlp) == type(ROOT.TMultiLayerPerceptron()):
##      nno = tmlp.Evaluate(0, array('d',[vars[k].GetValue() for k in setup['inputVars']]))
##    else:
##      nno = tmlp.value(0, *[vars[k].GetValue() for k in setup['inputVars']])
    val = vars[var].GetValue()
    if weight!='':
      weightVal = vars['weight'].GetValue()
    else:
      weightVal = 1.
    if nnBin[0]<=-999: #or nno>nnBin[0]:
      if nnBin[1]>=999:#or nno<=nnBin[1]:
        res.Fill(val, weightVal)
#        print i, val, weightVal, nno
  del eList
  return res.Clone()

def getNNOutput(tmlp, sample, eList, varNames, tinputs, result='plot', nbins=200, nnThreshold=-999.):
  vars={}
#tmlp is 'MLP_ANN': output of TMVA
  for vn in varNames:
    vars[vn] = p_c_float(0.)
  for k in vars.keys():
    sample.SetBranchAddress(k, vars[k])
  if result.lower()=='plot':
    res =  ROOT.TH1F('bgh', 'NN output', nbins, -.5, 1.5)
    res.Reset()
  if result.lower()=='list':
    res=[] 
  if result.lower()=='weightsum':
    res=0.
  for i in range(eList.GetN()) :
    sample.GetEntry(eList.GetEntry(i))
##    if type(tmlp) == type(ROOT.TMultiLayerPerceptron()):
##      val = tmlp.Evaluate(0, array('d',[vars[k][0] for k in tinputs]))
##    else:
##      val = tmlp.value(0, *[vars[k][0] for k in tinputs])
    if nnThreshold>-999. and val<=nnThreshold:continue
    if result.lower()=='plot':
      res.Fill(val)
    if result.lower()=='list':
      res.append(val)
    if result.lower()=='weightsum':
      res+=sample.GetLeaf('weight').GetValue()
  return res

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
#ROOT.gSystem.Load('libMLPXXX')

def constructDataset(setup, signal, background, overWrite = False):
#  modelVars = ["osetMN", "osetMgl", "osetMsq"]
#  setup['additionalVars'] = ['weightForMVA','weightLumi14']+['jet10pt', 'jet20pt', 'jet30pt', 'deltaPhi']

  if (not os.path.isfile(setup['dataFile'])) or overWrite:
    print 'Creating NN dataset',setup['dataFile']
    if overWrite and os.path.isfile(setup['dataFile']):
      print 'Warning! File will be overwritten'
    simu =  ROOT.TTree('MonteCarlo', 'Filtered Monte Carlo Events')
    print simu
    vars={}
    vartype={}
    for vn in setup['varNames']:
      vartype[vn]='F'
      if vn.count('/'):
        vn, tp = vn.split('/')
        vartype[vn] = tp

      if vartype[vn]=='F':
        vars[vn] = p_c_float(0.)
      elif vartype[vn]=='I':
        vars[vn] = p_c_int(0)
      else:
        print "Type ", vartype[vn], "not implemented! Using float"
        vartype[vn] = 'F'
      
    i_type    = ctypes.c_int(0) 
    for sample in [signal, background]:
      for k in vars.keys():
        sample.SetBranchAddress(k, vars[k])
    for k in vars.keys():
      simu.Branch(k, vars[k], k+'/'+vartype[k])
    simu.Branch('type',   ctypes.addressof(i_type),   'type/I')

    addVars = {} 
    for v in ['weightForMVA']+[v[0] for v in setup['additionalVars']]+setup['modelVars']:
      addVars[v] = ctypes.c_float(0.)
      simu.Branch(v,   ctypes.addressof(addVars[v]),   v+'/F')

    eListSig = getEList(signal,        setup['preselection'], 'eListSig')
    eListBkg = getEList(background,    setup['preselection'], 'eListBkg')

    for i_type.value , sample, eList in [[ 1, signal, eListSig], [0, background, eListBkg]]:
      mvaWeightFac=1
      if i_type.value==1:
        if setup.has_key('sigMVAWeightFac'):
          mvaWeightFac = setup["sigMVAWeightFac"]
      else:
        if setup.has_key('bkgMVAWeightFac'):
          mvaWeightFac = setup["bkgMVAWeightFac"]
    
      for i in range(eList.GetN()):
        if i%10000==0:print 'type',i_type.value, 'Event.:',i,'/',eList.GetN()
        sample.GetEntry(eList.GetEntry(i))
        if i_type.value==1:
          for v in setup['modelVars']:
            addVars[v].value = sample.GetLeaf(v).GetValue()
#          scaleTo14 = gluino14TeV_NLO[addVars['osetMgl'].value] /  gluino8TeV_NLONLL[addVars['osetMgl'].value]
#          addVars['weight14'].value = scaleTo14*vars['weight'].value
#          addVars['weightLumi14'].value = scaleTo14*vars['weightLumi'][0]
          addVars['weightForMVA'].value  = sample.GetLeaf(setup['weightForMVA']['weight']).GetValue()*setup['weightForMVA']['sigFac']*mvaWeightFac
        else:
          for v in setup['modelVars']:
            addVars[v].value = float('nan')
#          scaleTo14 = 882.29/225.197
#          addVars['weight14'].value = scaleTo14*vars['weight'].value
#          addVars['weightLumi14'].value = scaleTo14*vars['weightLumi'][0]
          addVars['weightForMVA'].value  = sample.GetLeaf(setup['weightForMVA']['weight']).GetValue()*setup['weightForMVA']['bkgFac']*mvaWeightFac
#        addVars['weightForMVA'].value  = sample.GetLeaf(setup['weightForMVA']).GetValue()*mvaWeightFac
        for v in setup["additionalVars"]:
          addVars[v[0]].value  = v[1](sample) 
        simu.Fill()

#    eListTest         = getEList(simu,    setup['preselection'] +'&&'+ setup['testRequ']       ,'eListTest')
#    eListTraining     = getEList(simu,    setup['preselection'] +'&&'+ setup['trainingRequ']   ,'eListTraining')
    eListBkg          = getEList(simu,   'type==0&&'+ setup['preselection']    ,'eListBkg')
    eListSig          = getEList(simu,   'type==1&&'+ setup['preselection']    ,'eListSig')
#    eListBkgTest      = getEList(simu,   'type==0&&'+ setup['preselection']+'&&'+ setup['testRequ']    ,'eListBkgTest')
#    eListSigTest      = getEList(simu,   'type==1&&'+ setup['preselection']+'&&'+ setup['testRequ']    ,'eListSigTest')
#    eListBkgTraining  = getEList(simu,   'type==0&&'+ setup['preselection']+'&&'+ setup['trainingRequ'],'eListBkgTraining')
#    eListSigTraining  = getEList(simu,   'type==1&&'+ setup['preselection']+'&&'+ setup['trainingRequ'],'eListSigTraining')
    f = ROOT.TFile(setup['dataFile'], 'recreate')
    simu.Write()
#    eListTest.Write()
#    eListTraining.Write()
    eListBkg.Write()
    eListSig.Write()
#    eListBkgTest.Write()
#    eListSigTest.Write()
#    eListBkgTraining.Write()
#    eListSigTraining.Write()
    f.Close()
    print 'Written NN dataset to', setup['dataFile']
    print simu
    Events = ROOT.gDirectory.Get("Events")
    del Events
    del simu
#    del eListTest
#    del eListTraining
    del eListBkg
    del eListSig
#    del eListBkgTest
#    del eListSigTest
#    del eListBkgTraining
#    del eListSigTraining
  print 'Loading NN dataset from', setup['dataFile']
  g = ROOT.gDirectory.Get("MonteCarlo")
  if g: del g
  simu      = getObjFromFile(setup['dataFile'],'MonteCarlo')
#  eListTest      = getObjFromFile(setup['dataFile'],'eListTest')
#  eListTraining      = getObjFromFile(setup['dataFile'],'eListTraining')
  eListBkg      = getObjFromFile(setup['dataFile'],'eListBkg')
  eListSig      = getObjFromFile(setup['dataFile'],'eListSig')
#  eListBkgTest      = getObjFromFile(setup['dataFile'],'eListBkgTest')
#  eListSigTest      = getObjFromFile(setup['dataFile'],'eListSigTest')
#  eListBkgTraining  = getObjFromFile(setup['dataFile'],'eListBkgTraining')
#  eListSigTraining  = getObjFromFile(setup['dataFile'],'eListSigTraining')
#  print'Datasets and eLists:',simu,'' ,eListTest,' ',eListTraining,' ',eListBkg,' ',eListSig,' ',eListBkgTest,' ',eListSigTest,' ',eListBkgTraining,' ',eListSigTraining
  print'Datasets and eLists:',simu, eListBkg,' ',eListSig
  print '...done.'
#  return {'simu':simu, 'eListBkgTest':eListBkgTest, 'eListSigTest':eListSigTest, 'eListBkgTraining':eListBkgTraining, 'eListSigTraining':eListSigTraining, 'eListBkg':eListBkg, 'eListSig':eListSig, 'eListTest':eListTest, 'eListTraining':eListTraining}
  return {'simu':simu, 'eListBkg':eListBkg, 'eListSig':eListSig}
  

def getConstSoverSqrtBFunc(l, bkgXsec, sigXsec, bkgPreselectionEff, sigPreselectionEff, const):
  return ROOT.TF1('func', '1. - '+str(l)+'*('+str(sigPreselectionEff)+'*'+str(sigXsec)+'*x/'+str(const)+')**2/('+str(bkgPreselectionEff)+'*'+str(bkgXsec)+')', 0, 1)


def setupMVAFrameWork(setup, data, methods, prefix):
  olddir = ROOT.gDirectory.CurrentDirectory().GetName()+':/' 
  vstring=''
  for v in setup['inputVars']:
    vstring+=v+','
  vstring = vstring[:-1]

#  lstring=':'.join(str(i) for i in setup['NN_layers'])

  print 'Instancing of TMVA Factory:'

  ROOT.TMVA.Tools.Instance()
  ROOT.TMVA.gConfig().GetIONames().fWeightFileDir = setup['weightDir']
  ROOT.TMVA.gConfig().GetVariablePlotting().fNbinsXOfROCCurve = 200

  fout = ROOT.TFile(setup['outputFile'],"RECREATE") 
  factory = ROOT.TMVA.Factory("TMVAClassification", fout,":".join(setup['TMVAFactoryOptions']))
  factory.DeleteAllMethods()
  factory.SetBackgroundWeightExpression("weightForMVA")
  factory.SetSignalWeightExpression(    "weightForMVA") 

  factory.AddSignalTree(data['simu'])
  factory.AddBackgroundTree(data['simu'])

  #There is a Bias-Neuron in the NN!
# bnode=ROOT.TMVA.TNeuron()
# bnode.SetBiasNeuron()
# print bnode
# bnode.ForceValue(0)
# print bnode  

  for i in setup['inputVars']:
    factory.AddVariable(i)

  sigCut = ROOT.TCut("type==1&&"+setup['preselection'])
  bgCut = ROOT.TCut("type==0&&"+setup['preselection']) 

  factory.PrepareTrainingAndTestTree(sigCut,bgCut,":".join(["nTrain_Signal=0", "nTrain_Background=0","SplitMode=Random","SplitSeed=100","NormMode=None","!V"]))
  
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

  pfile = setup['outputFile'].replace('.root','')+'.pkl'
  setupStripped = copy.deepcopy(setup)
  setupStripped.pop('additionalVars',None)
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
      t = getObjFromFile(setup['outputFile'], treeName+'Tree')
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
    histFOM = getObjFromFile(setup['outputFile'],'MVA_'+m['name']+'_rejBvsS')
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

  print '  '
  print '  '

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
    m['FOMFromFile'] = getObjFromFile(setup['outputFile'],'MVA_'+m['name']+'_rejBvsS')
    m['FOMFromFile'].SetStats(False) 
    m['FOMFromFile'].SetLineColor(m['lineColor'])
    
    m['FOMFromTree'] = getFOMPlot(m['hbgTestFine'], m['hsigTestFine'])
    m['FOMFromTree']['central'].SetLineColor(m['lineColor'])
    m['FOMFromTree']['central'].Draw(opt)
    if not  m['type']==ROOT.TMVA.Types.kCuts:
      l3.AddEntry(m['FOMFromTree']['central'],m['niceName'],'LP')
#    else:
#      l3.AddEntry(m['FOMFromFile'],m['niceName'],'LP')
    opt="L"
    if m.has_key('drawStatUncertainty') and m['drawStatUncertainty']:
      if not  m['type']==ROOT.TMVA.Types.kCuts:
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
  t = getObjFromFile(setup['outputFile'], 'TestTree')
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

  mlpa_canvas.Print(setup['plotDir']+'/nnValidation_'+prefix+'.pdf')
  mlpa_canvas.Print(setup['plotDir']+'/nnValidation_'+prefix+'.png')
  mlpa_canvas.Print(setup['plotDir']+'/nnValidation_'+prefix+'.root')
  del mlpa_canvas

  network_canvas = ROOT.gROOT.ProcessLine('.x ./../../HEPHYCommonTools/mva/tmvaMacros/network.C("'+setup['outputFile']+'")')
  
  for m in methods:
#   print m['name']
    if not m['name']=='myCut':
      os.system('mv ./plots/'+m['name']+'.png '+setup['plotDir']+'/netStructure_'+prefix+'_'+m['name']+'.png')

  ROOT.gROOT.cd(olddir)

  coord_canvas = ROOT.TCanvas('coord_canvas', 'Network Coordinates',1200, 400*(1+len(methods))) 
  coord_canvas.SetFillColor(ROOT.kWhite)
  inp = ":".join(setup['inputVars'])

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


  coord_canvas.Print(setup['plotDir']+'/nnCoord_'+prefix+'.png')       
  t.IsA().Destructor(t)
  del t
  ROOT.gROOT.cd(olddir)
  return

def getYield(c, cut, weight = "weight"):

  cut = weight+"*("+cut+")"
  print cut
  c.Draw("1>>htmp(1,0,2)", cut, "goff")
  htmp =  ROOT.gDirectory.Get("htmp")
  res = htmp.Integral()
  del htmp
  return res

