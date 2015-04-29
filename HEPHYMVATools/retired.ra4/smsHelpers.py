import ROOT

smsBlockBinning={}
smsBlockBinning['T1tttt-madgraph'] = [100,200] #Binning in mN and mg-mN
smsBlockBinning['T1tttt'] = [100,100] #Binning in mN and mg-mN

def getBlock(mgl, mN, model='T1tttt-madgraph'):
  if model=='T1tttt-madgraph' or model=='T1tttt':
    mNLow = smsBlockBinning[model][0]*int(mN/smsBlockBinning[model][0])
    mNHigh = smsBlockBinning[model][0]+mNLow
    mDelta=mgl-mN
    mDeltaLow = smsBlockBinning[model][1]*int(mDelta/smsBlockBinning[model][1])
    mDeltaHigh = smsBlockBinning[model][1]+mDeltaLow
    return {'mN':[mNLow, mNHigh], 'mD':[mDeltaLow, mDeltaHigh]}

def getBlockString(mgl, mN, model='T1tttt-madgraph'):
  if model=='T1tttt-madgraph' or model=='T1tttt':
    r  = getBlock(mgl, mN, model)
    mDeltaLow, mDeltaHigh = r['mD'] 
    mNLow, mNHigh = r['mN'] 
    return 'mD_'+str(mDeltaLow)+'_'+str(mDeltaHigh)+'_mN_'+str(mNLow)+"_"+str(mNHigh)
  
def getAllBlocks(mglMax, mNMax=1200, model='T1tttt-madgraph'):
  if model=='T1tttt-madgraph' or model=='T1tttt':
    allBlocks=[]
    for mgl in range(400, mglMax + 25, 25):
      for mN in range(0, mNMax + 25, 25):
        if mgl-mN>=200:
          r = getBlock(mgl, mN, model)
          if not allBlocks.count(r):
            allBlocks.append(r)
    return allBlocks

def getAllInBlock(a1, a2=-1, model='T1tttt-madgraph'):
  if model=='T1tttt-madgraph' or model=='T1tttt':
    res=[]
    if a2<0:
      r=a1
    else: 
      r = getBlock(a1, a2, model)
    for mgl_ in range(400, 1400 + 25, 25):
      for mN_ in range(0, 1200 + 25, 25):
        if mgl_-mN_>=200:
          rp = getBlock(mgl_, mN_, model)
          if r==rp:
            res.append((mgl_, mN_))
    return res

def getColouredRegionPlot(model='T1tttt-madgraph'):
  if model=='T1tttt-madgraph' or model=='T1tttt':
    c=1
    blockVals={}
    h = ROOT.TH2F (model+'_ColouredRegionPlot', model+'_ColouredRegionPlot', 48, 400, 1600, 52, 0, 1300)
    allBlocks = getAllBlocks(1400, 1200, model)
    for mgl in range(400, 1400 + 25, 25):
      for mN in range(0, 1200 + 25, 25):
        rb = getBlock(mgl, mN, model)
        r = getBlockString(mgl, mN, model)
        if not rb in allBlocks: continue
        if not blockVals.has_key(r):
          blockVals[r]=c
          c+=1
        h.SetBinContent( h.FindBin(mgl, mN), blockVals[r])
    return h
     
def getSignalChain(mgl, mN, model="T1tttt-madgraph"):
  import os
  signal      = ROOT.TChain('Events')
  fstringMu  = '/data/schoef/convertedTuples_v20/copyMET/Mu/'+model+'_'+str(mgl)+'_'+str(mN)+'/histo_'+model+'_'+str(mgl)+'_'+str(mN)+'.root'
  fstringEle = '/data/schoef/convertedTuples_v20/copyMET/Ele/'+model+'_'+str(mgl)+'_'+str(mN)+'/histo_'+model+'_'+str(mgl)+'_'+str(mN)+'.root'
  if (os.path.isfile(fstringMu) and os.path.isfile(fstringEle)):
    signal.Add(fstringMu)
    signal.Add(fstringEle)
  entries = signal.GetEntries()
  if entries:
    return signal
  else:
    return
 
