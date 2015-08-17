import ROOT
from math import pi, sqrt, cos, sin, sinh, log
from array import array

def test():
  return 1

def scatterOnTH2(data, h, ofile, markerType):
  assert type(h)==type(ROOT.TH2F()) or type(h)==type(ROOT.TH2D()), "Wrong type of histogram! %s" % repr(type(h))
  for d in data:
    h.Fill(d[0], d[1], 0) 
  c1 = ROOT.TCanvas()
  xmin = h.GetXaxis().GetXmin()
  xmax = h.GetXaxis().GetXmax()
  ymin = h.GetYaxis().GetXmin()
  ymax = h.GetYaxis().GetXmax()
  data.sort(key=lambda x:x[2])
  zvals = [d[2] for d in data] 
  zmin, zmax = min(zvals), max(zvals)
  h.GetZaxis().SetRangeUser(zmin,zmax)
  c1.Update()
  h.Draw("COLZ")
  c1.SetLogz()
  stuff=[]
  for d in data:
    if d[0]>xmin and d[0]<xmax and d[1]>ymin and d[1]<ymax:
      zRatio = (log(d[2])-log(zmin))/(log(zmax) - log(zmin))
      color = ROOT.gStyle.GetColorPalette(int(round(zRatio*(ROOT.gStyle.GetNumberOfColors()-1))))
      print 'zR', zRatio, 'color',color
      e = ROOT.TMarker(d[0], d[1], markerType) 
      e.SetMarkerColor(color) 
      stuff.append(e)
    h.Fill(d[0], d[1], 0) 
  for s in stuff:
    s.Draw()
  c1.Print(ofile)
  

def bStr(s): 
  "make string bold."
  assert type(s)==type(""), "bStr needs string, got %s" % str(type(s))
  return "\033[1m"+s+"\033[0;0m"

def wrapStr(s="", char="#", maxL = 100):
  "Wrap a string with a char"
  assert type(s)==type(""), "wrapStr needs string, got %s" % str(type(s))
  assert type(char)==type(""), "wrapStr needs character, got %s" % str(type(char))
  if s=="":
    return char.join(["" for i in range(maxL+1)])
  char=char[:1]
  l = len(s) 
  if l>=maxL:
    return s
  frontL = (maxL - l )/2
  backL  = maxL-l-frontL
  return char.join(["" for i in range(frontL)]) + " "+s+" "+char.join(["" for i in range(backL)])


def getFileList(dir, minAgeDPM=0, histname='histo', xrootPrefix='root://hephyse.oeaw.ac.at/', maxN=-1):
  import os, subprocess, datetime
  monthConv = {'Jan':1, 'Feb':2,'Mar':3,'Apr':4,"May":5, "Jun":6,"Jul":7,"Aug":8, "Sep":9, "Oct":10, "Nov":11, "Dec":12}
  if dir[0:5] != "/dpm/":
    filelist = os.listdir(dir)
    filelist = [dir+'/'+f for f in filelist if histname in f]
  else:
    filelist = []
    p = subprocess.Popen(["dpns-ls -l "+ dir], shell = True , stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
      if not (histname=="" or line.count(histname)):continue
      line=line[:-1]
      sline = line.split()
      fname = sline[-1]
      size = sline[4]
      if int(size)!=0:
        month, day = sline[5:7]
        hour, minute = sline[7].split(':')
        age = (datetime.datetime.now() - datetime.datetime(2014, monthConv[month], int(day), int(hour), int(minute))).total_seconds()/3600
        if age>=minAgeDPM:
          filelist.append(fname)
        else:
          print "Omitting",fname,'too young:',str(age)+'h'
    filelist = [xrootPrefix+dir+'/'+f for f in filelist]
  if maxN>=0:
    filelist = filelist[:maxN]
  return filelist

def getChain(sL, minAgeDPM=0, histname='histo', xrootPrefix='root://hephyse.oeaw.ac.at/', maxN=-1, treeName="Events"):
  if not type(sL)==type([]):
    sList = [sL]
  else:
    sList= sL 
  c = ROOT.TChain(treeName)
  i=0
  for s in sList:
    if type(s)==type(""):
      for f in getFileList(s, minAgeDPM, histname, xrootPrefix, maxN):
        i+=1
        c.Add(f)
    if type(s)==type({}):
      if s.has_key('file'):
        c.Add(s['file'])
        i+=1
      if s.has_key('fromDPM') and s['fromDPM']:
        for f in getFileList(s['dir'], minAgeDPM, histname, xrootPrefix, maxN):
          i+=1
          c.Add(f)
      if s.has_key('bins'):
        for b in s['bins']:
          dir = s['dirname'] if s.has_key('dirname') else s['dir']
          for f in getFileList(dir+'/'+b, minAgeDPM, histname, xrootPrefix, maxN):
            i+=1
            c.Add(f)
  print "Added ",i #,'files from sample',s['name']
  return c

def getChunks(sample, maxN=-1):
#  if '/dpm/' in sample['dir']:
#    return getChunksFromDPM(sample, maxN=maxN)
#  elif '/eoscms.cern.ch/' in sample['dir']:
#    return getSampleFromEOS(sample)
#  else:
#    fromDPM =  sample.has_key('fromDPM') and sample.has_key('fromDPM')
#    #print "from dpm:" , fromDPM 
#    if fromDPM:
#      return getChunksFromDPM(sample, fromDPM=fromDPM, maxN=maxN)
#    else:
      #print "not from DPM"
      return getChunksFromNFS(sample, maxN=maxN)
    
def getChunksFromNFS(sample,  maxN=-1):
#  print "sample" , sample , maxN
  import os, subprocess, datetime
  #sample['dir']=sample['dir']+'/'+sample['name']
  print "sample dir:" , sample['dir']
  chunks = [{'name':x} for x in os.listdir(sample['dir']) if x.startswith(sample['chunkString']+'_Chunk') or x==sample['name']]
  print chunks
  chunks=chunks[:maxN] if maxN>0 else chunks
  sumWeights=0
  allFiles=[]
  failedChunks=[]
  const = 'All Events' if sample['isData'] else 'Sum Weights'
  for i, s in enumerate(chunks):
      if not sample.has_key("skimAnalyzerDir"):
        logfile = sample['dir']+'/'+s['name']+'/SkimReport.txt'
      else:
        logfile = sample['dir']+'/'+s['name']+"/"+sample["skimAnalyzerDir"]+'/SkimReport.txt'
      if os.path.isfile(logfile):
        line = [x for x in subprocess.check_output(["cat", logfile]).split('\n') if x.count(const)]
        assert len(line)==1,"Didn't find normalization constant '%s' in  number in file %s"%(const, logfile)
        #n = int(float(line[0].split()[2]))
        sumW = float(line[0].split()[2])
        inputFilename = sample['dir']+'/'+s['name']+'/'+sample['rootFileLocation']
        #print sumW, inputFilename
        if os.path.isfile(inputFilename):
          sumWeights+=sumW
          allFiles.append(inputFilename)
          s['file']=inputFilename
        else:
          failedChunks.append(chunks[i])
      else:
        print "log file not found:  ", logfile
        failedChunks.append(chunks[i])
#    except: print "Chunk",s,"could not be added"
  print "Found",len(chunks),"chunks for sample",sample["name"],'with a normalization constant of',sumWeights,
  if len(chunks) > 0: print ". Failed for:",",".join([c['name'] for c in failedChunks]),"(",round(100*len(failedChunks)/float(len(chunks)),1),")%"
  del sample
  return chunks, sumWeights

#def getChunksFromDPM(sample, fromDPM=False, maxN=-1):
#  fileList = getFileList(sample['dir'], minAgeDPM=0, histname='', xrootPrefix='root://hephyse.oeaw.ac.at/' if not fromDPM else '')
#  chunks = [{'file':x,'name':x.split('/')[-1].replace('.root','')} for x in fileList]
#  chunks=chunks[:maxN] if maxN>0 else chunks
#  nTotEvents=0
#  failedChunks=[]
#  goodChunks=[]
#  for c in chunks:
#    try:
#      nEvents=int(c['name'].split('nEvents')[-1])
#    except:
#      nEvents=-1
#    if nEvents>0:
#      c.update({'nEvents':int(c['name'].split('nEvents')[-1])})
#      nTotEvents+=c['nEvents']
#      goodChunks.append(c)
#    else:
#      failedChunks.append(c)
#  print "Found",len(goodChunks),"chunks for sample",sample["name"],'with a total of',nTotEvents,"events. Failed for:",",".join([c['name'] for c in failedChunks]),"(",round(100*len(failedChunks)/float(len(chunks)),1),")%"
#  return goodChunks, nTotEvents

def getObjFromFile(fname, hname):
  f = ROOT.TFile(fname)
  assert not f.IsZombie()
  f.cd()
  htmp = f.Get(hname)
  if not htmp:  return htmp
  ROOT.gDirectory.cd('PyROOT:/')
  res = htmp.Clone()
  f.Close()
  return res

def passPUJetID(flag, level="Tight"): #Medium, #Loose,  kTight  = 0,   kMedium = 1,   kLoose  = 2
  if type(level)==type(0):
    return ( flag & (1 << level) ) != 0
  if level=="Tight":
    l=0
  if level=="Medium":
    l=1
  if level=="Loose":
    l=2
  return ( flag & (1 << l) ) != 0

def getVar(c, var, n=0):
    l = c.GetLeaf(var)
    try:
       return l.GetValue(n)
    except:
      raise Exception("Unsuccessful getVarValue for leaf %s and index %i"%(var, n))

def getVarValue(c, var, n=0):
  varNameHisto = var
  leaf = c.GetAlias(varNameHisto)
  if leaf!='':
    try:
      return c.GetLeaf(leaf).GetValue(n)
    except:
      raise Exception("Unsuccessful getVarValue for leaf %s and index %i"%(leaf, n))
  else:
    l = c.GetLeaf(var)
    if l:return l.GetValue(n)
    return float('nan')

def getCutYieldFromChain(c, cutString = "(1)", cutFunc = None, weight = "weight", weightFunc = None, returnVar=False):
  c.Draw(">>eList", cutString)
  elist = ROOT.gDirectory.Get("eList")
  number_events = elist.GetN()
  res = 0.
  resVar=0.
  for i in range(number_events): 
    c.GetEntry(elist.GetEntry(i))
    if (not cutFunc) or cutFunc(c):
      if weight:
        w = c.GetLeaf(weight).GetValue()
      else:
        w=1.
      if weightFunc:
        w*=weightFunc(c)
      res += w
      resVar += w**2
  del elist
  if returnVar:
    return res, resVar
  return res

def getYieldFromChain(c, cutString = "(1)", weight = "weight", returnError=False):
  h = ROOT.TH1F('h_tmp', 'h_tmp', 1,0,2)
  h.Sumw2()
  c.Draw("1>>h_tmp", "("+weight+")*("+cutString+")", 'goff')
  res = h.GetBinContent(1)
  resErr = h.GetBinError(1)
#  print "1>>h_tmp", weight+"*("+cutString+")",res,resErr
  del h
  if returnError:
    return res, resErr
  return res 

def getPlotFromChain(c, var, binning, cutString = "(1)", weight = "weight", binningIsExplicit=False, addOverFlowBin=''):
  if binningIsExplicit:
    h = ROOT.TH1F('h_tmp', 'h_tmp', len(binning)-1, array('d', binning))
#    h.SetBins(len(binning), array('d', binning))
  else:
    if len(binning)==6:
      h = ROOT.TH2F('h_tmp', 'h_tmp', *binning)
    else:
      h = ROOT.TH1F('h_tmp', 'h_tmp', *binning)
  c.Draw(var+">>h_tmp", weight+"*("+cutString+")", 'goff')
  res = h.Clone()
  h.Delete()
  del h
  if addOverFlowBin.lower() == "upper" or addOverFlowBin.lower() == "both":
    nbins = res.GetNbinsX()
#    print "Adding", res.GetBinContent(nbins + 1), res.GetBinError(nbins + 1)
    res.SetBinContent(nbins , res.GetBinContent(nbins) + res.GetBinContent(nbins + 1))
    res.SetBinError(nbins , sqrt(res.GetBinError(nbins)**2 + res.GetBinError(nbins + 1)**2))
  if addOverFlowBin.lower() == "lower" or addOverFlowBin.lower() == "both":
    res.SetBinContent(1 , res.GetBinContent(0) + res.GetBinContent(1))
    res.SetBinError(1 , sqrt(res.GetBinError(0)**2 + res.GetBinError(1)**2))
  return res

def getEList(chain, cut, newname='eListTMP'):
  chain.Draw('>>eListTMP_t', cut)
  elistTMP_t = ROOT.gROOT.Get('eListTMP_t')
  elistTMP = elistTMP_t.Clone(newname)
  del elistTMP_t
  return elistTMP

def deltaPhi(phi1, phi2):
  dphi = phi2-phi1
  if  dphi > pi:
    dphi -= 2.0*pi
  if dphi <= -pi:
    dphi += 2.0*pi
  return abs(dphi)

def deltaPhiNA(phi1, phi2):
  dphi = phi2-phi1
  if  dphi > pi:
    dphi -= 2.0*pi
  if dphi <= -pi:
    dphi += 2.0*pi
  return dphi

def minAbsDeltaPhi(phi, phis):
  if len(phis) > 0:
    return min([abs(deltaPhi(phi, x)) for x in phis])
  else: return float('inf')

def minAbsPiMinusDeltaPhi(phi, phis):
  if len(phis)>0:
    return min([abs(abs(deltaPhi(phi, x)) - pi) for x in phis])
  else: return float('inf')

def invMassOfLightObjects(p31, p32):
  [px1, py1, pz1] = p31
  [px2, py2, pz2] = p32
  px = px1+px2
  py = py1+py2
  pz = pz1+pz2
  p1 = sqrt(px1*px1+py1*py1+pz1*pz1)
  p2 = sqrt(px2*px2+py2*py2+pz2*pz2)
  p = sqrt(px*px+py*py+pz*pz)
  return   sqrt((p1 + p2)*(p1 + p2) - p*p)

def deltaR2(l1, l2):
  return deltaPhi(l1['phi'], l2['phi'])**2 + (l1['eta'] - l2['eta'])**2
def deltaR(l1, l2):
  return sqrt(deltaR2(l1,l2))
#Get an object with name-prefix (e.g. LepGood) as a dictionary by specifying index i and variables ['pt','eta',...]
def getObjDict(c, prefix, variables, i):
 return {var: c.GetLeaf(prefix+var).GetValue(i) for var in variables}

#FIXME: Move this selection specific stuff to the analysis directory (Deg stop)
#def getJets(c):
#  njets = int(c.GetLeaf('njetCount').GetValue())
#  jets =[]
#  for i in range(njets):
#    jets.append({'pt':getVarValue(c, 'jetPt', i), 'eta':getVarValue(c, 'jetEta', i), 'phi':getVarValue(c, 'jetPhi', i)})
#  return jets
#
#def minDeltaRLeptonJets(c):
#  jets = getJets(c)
#  return min([deltaR(j, {'phi':getVarValue(c, 'softIsolatedMuPhi'), 'eta':getVarValue(c, 'softIsolatedMuEta')}) for j in jets])
#
##def getSoftIsolatedMu(c):
##  return {'pt':c.GetLeaf('softIsolatedMuPt').GetValue(), 'eta':c.GetLeaf('softIsolatedMuEta').GetValue(), 'phi':c.GetLeaf('softIsolatedMuPhi').GetValue()}
#def htRatio(c):
#  jets = getJets(c)
#  metPhi = c.GetLeaf('type1phiMetphi').GetValue()
##  print calcHTRatio(jets, metPhi)
#  return calcHTRatio(jets, metPhi)
#def getISRweightString(mode="Central", var="ptISR"):
#    if mode.lower()=="down"   : return "(1.*("+var+"<120) + "+".90*( "+var+">120&&"+var+"<150) + "+".80*( "+var+">150&&"+var+"<250) + "+".60*( "+var+">250))"
#    if mode.lower()=="up": return "(1)"
#    return "(1.*("+var+"<120) + "+".95*( "+var+">120&&"+var+"<150) + "+".90*( "+var+">150&&"+var+"<250) + "+".80*( "+var+">250))"


def calcHTRatio(jets, metPhi):
  htRatio = -1
  den=0.
  num=0.
  for j in jets:
    den+=j["pt"]
    if abs(deltaPhi(metPhi, j["phi"])) <= pi/2:
      num+=j["pt"]
  if len(jets)>0:
    htRatio = num/den
  return htRatio

def findClosestObject(jets, obj, sortFunc=lambda o1, o2: deltaR2(o1,o2)):
##  jets = getJets(c)
  res=[]
  for i,j in enumerate(jets):
    res.append([sortFunc(j, obj), j, i])
  res.sort()
  if len(res)>0:
    return {'distance':res[0][0], 'obj':res[0][1], 'index':res[0][2]}

#def closestMuJetDeltaR(c):
#  return findClosestObject(c, getSoftIsolatedMu(c))['deltaR']

def invMass(p1 , p2):
  pxp1 = p1['pt']*cos(p1['phi']) 
  pyp1 = p1['pt']*sin(p1['phi']) 
  pzp1 = p1['pt']*sinh(p1['eta'])
  Ep1 = sqrt(pxp1**2 + pyp1**2 + pzp1**2)

  pxp2 = p2['pt']*cos(p2['phi'])
  pyp2 = p2['pt']*sin(p2['phi'])
  pzp2 = p2['pt']*sinh(p2['eta'])
  Ep2 = sqrt(pxp2**2 + pyp2**2 + pzp2**2)

  return sqrt( (Ep1 + Ep2)**2 - (pxp1 + pxp2)**2 - (pyp1 + pyp2)**2 - (pzp1 + pzp2)**2)

def KolmogorovDistance(s0, s1): #Kolmogorov distance from two list of values (unbinned, discrete)
  from fractions import Fraction, gcd

  s0.sort()
  s1.sort()

  tot = [[x,0] for x in s0] + [[x,1] for x in s1]
  tot.sort()
  F={}
  lenS={}
  lenS[0] = len(s0)
  lenS[1] = len(s1)
  F[0] = 0
  F[1] = 0
  l = len(tot)
#  print tot
  maxDist = Fraction(0,1)
  for i, t in enumerate(tot):
#    print "Now",F
    F[t[1]]+=1#lenS[t[1]]
#    print "...",F
    if i+1<l and tot[i+1][0]==t[0]:
      continue
#    print "Calc dist..."
    dist= abs(Fraction(F[0],lenS[0])-Fraction(F[1],lenS[1]))
    if dist>maxDist:
      maxDist=dist
#    print dist, maxDist
  return maxDist

def KolmogorovProbability(s0, s1):
  ksDist = float(KolmogorovDistance(s0, s1))
  return ROOT.TMath.KolmogorovProb(ksDist*sqrt(len(s0)*len(s1)/float(len(s0)+len(s1))))

def getISRweight(c, mode="Central"):
  ptISR = c.GetLeaf('ptISR').GetValue()
  if mode.lower()=='central':
    if ptISR<120:return 1.
    if ptISR<150:return .95
    if ptISR<250:return .90
    return 0.80
  if mode.lower()=='down':
    if ptISR<120:return 1.
    if ptISR<150:return .90
    if ptISR<250:return .80
    return 0.60
  if mode.lower()=='up':
    return 1.0

def calcMT(lepton, met):
  if lepton and met:
    return sqrt(2.*met['pt']*lepton['pt']*(1-cos(lepton['phi'] - met['phi'])))
  else:
    return float('nan')
