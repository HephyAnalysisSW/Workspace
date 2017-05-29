class cardFileWriter:
  def __init__(self):
    self.bins = [] 
    self.uncertainties = []
    self.uncertaintyVal = {}
    self.uncertaintyString = {}
    self.processes = {} 
    self.expectation = {} 
    self.observation = {} 
    self.contamination = {} 
    self.niceNames = {}
    self.defWidth = 30
    self.precision = 4
    self.maxUncNameWidth = 15
    self.maxUncStrWidth = 30
    self.maxNameStrWidth = 30
    self.maxProcessStrWidth= 30
    self.hasContamination=False
    self.allowNonIntegerObservation=False
    self.groups = {}
    self.extraLines = [ ]
    self.comment = ""

  def reset(self):
    self.__init__()	

  def addExtraLine(self,l):
    self.extraLines.append(l)

  def addBin(self, name, processes, niceName=""):
    if len(name)> self.maxNameStrWidth:
      print "Name for bin",name,"too long. Max. length is %s"%self.maxNameStrWidth
      return
    if self.niceNames.has_key(name):
      print "Bin already there! (",name,")"
      return
    for p in processes:
      if len(p)>self.maxProcessStrWidth:
        print "Name for process", p, "in bin", name, "is too long. Max. length is %s"%self.maxProcessStrWidth
        return 
    self.niceNames[name]=niceName
    self.bins.append(name)
    if not 'signal' in processes:
        processes = ['signal'] + processes
    self.processes[name] = processes

  def addUncertainty(self, name, t, n=0, group=None):
    if len(name)>self.maxUncNameWidth:
      print "That's too long:",name,"Max. length is", self.maxUncNameWidth
      del self.uncertaintyString[name]
      return
    if self.uncertainties.count(name):
      print "Uncertainty already there! (",name,")"
      return
    self.uncertainties.append(name)
    self.uncertaintyString[name] = t
    if t=="gmN": 
      if n==0:
        print "gmN Uncertainty with n=0! Specify n as third argument: addUncertainty(..., 'gmN', n)"
        return
      self.uncertaintyString[name] = t+' '+str(n)
    if len(self.uncertaintyString[name])>self.maxUncStrWidth:
      print "That's too long:",self.uncertaintyString[name],"Max. length is", self.maxUncStrWidth
      del self.uncertaintyString[name]
      return
    if group!=None:
      assert not group in self.uncertainties
      if not group in self.groups:
        self.groups[group] = [ ]
      self.groups[group].append(name)

  def specifyExpectation(self, b, p, exp):
    self.expectation[(b,p)] = exp

  def specifyObservation(self, b, obs):
    if not isinstance(obs, int) and not self.allowNonIntegerObservation:
      print "Observation not an integer! (",obs,")" 
      print "If you really have a good reason for doing this you can set cfw.allowNonIntegerObservation=True"
      return 
    self.observation[b] = obs

  def specifyContamination(self, b, cont):
    self.contamination[b] = cont
    self.hasContamination = True

  def specifyFlatUncertainty(self, u,  val, bins=None, processes=None):
    """
    will be moved to CombinedCard Class
    """
    if u not in self.uncertainties:
      print "This uncertainty has not been added yet!",u,"Available:",self.uncertainties
      return
    if not bins:
      bins = self.bins
    print "Adding ",u,"=",val,"for bins: %s and processes: %s!"%( bins , (processes if processes else self.processes[bins[0]] ))
    useDefaultProcesses = False if processes else True
    for b in bins:
      if useDefaultProcesses:
        processes_ = self.processes[b][:]
      else:
        processes_ = processes[:]
      for p in processes_:
        self.uncertaintyVal[(u,b,p)] = val

  def specifyUncertainty(self, u, b, p, val):
    if u not in self.uncertainties:
      print "This uncertainty has not been added yet!",u,"Available:",self.uncertainties
      return
    if b not in self.bins:
      print "This bin has not been added yet!",b,"Available:",self.bins
      assert b in self.bins
      return
    if p not in self.processes[b]:
      print "Process ", p," is not in bin",b,". Available for ", b,":",self.processes[b]
      return
    self.uncertaintyVal[(u,b,p)] = val

  def getUncertaintyString(self, k):
    u, b, p = k
    if self.uncertaintyString[u].count('gmN'):
      if self.uncertaintyVal.has_key((u,b,p)) and self.uncertaintyVal[(u,b,p)]>0.:
        n = float(self.uncertaintyString[u].split(" ")[1])
        return self.mfs(self.expectation[(b, p)]/float(n))
      else: return '-' 
    if self.uncertaintyVal.has_key((u,b,p)):
      return self.mfs(self.uncertaintyVal[(u,b,p)])
    return '-'

  def checkCompleteness(self):
    for b in self.bins:
      if not self.observation.has_key(b) or not self.observation[b]<float('inf'):
        print "No valid observation for bin",b
        return False
      if self.hasContamination and (not self.contamination.has_key(b) or not self.contamination[b] < float('inf')):
        print "No valid contamination for bin",b
        return False
      if len(self.processes[b])==0:
        print "Warning, bin",b,"has no processes"
      for p in self.processes[b]:
        if not self.expectation.has_key((b,p)) or not self.expectation[(b,p)]<float('inf'):
          print "No valid expectation for bin/process ",(b,p)
          return False
      for k in self.uncertaintyVal.keys():
        valsToCheck = []
        uncertVal = self.uncertaintyVal[k]
        if "/" in str( self.uncertaintyVal[k] ):
            valsToCheck.extend( str(uncertVal).rsplit("/") )
        else:
            valsToCheck.append( uncertVal )
        for v in valsToCheck:
            if not float(v)<float('inf'):
              print "Uncertainty invalid for",k,':',self.uncertaintyVal[k]
              return False
    return True

  def mfs(self, f):
    if type(f)==str and "/" in f:
        #vals = str(f).rsplit("/")
        #if len(vals) > 2: assert False, "No valid Asymmetric Uncert: %s"%f
        #return "%s/%s"%(self.mfs(vals[0]), self.mfs(vals[1]) )
        return f
    else:
        return str(round(float(f),self.precision)) 

  def writeToFile(self, fname):
    import datetime
    if not self.checkCompleteness():
      print "Incomplete specification."
      return
    allProcesses=[]
    numberID = {}
    i=1
    for b in self.bins:
      for p in self.processes[b]:
        if not p in allProcesses and not p=='signal':
          allProcesses.append(p)
          numberID[p] = i
          i+=1
    numberID['signal'] = 0
    lspace = self.maxUncStrWidth + self.maxUncNameWidth + 2
    outfile = file(fname, 'w')
    outfile.write('#cardFileWriter, '+datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")+ " %s"%self.comment +'\n')
    outfile.write('imax '+str(len(self.bins))+'\n')
    outfile.write('jmax *\n')
    outfile.write('kmax *\n')
    outfile.write('\n')
    #observation
    outfile.write( '#'.ljust(lspace)+''.join([self.niceNames[b].rjust(self.defWidth) for b in self.bins] ) +'\n')
    outfile.write( 'bin'.ljust(lspace)+''.join([b.rjust(self.defWidth) for b in self.bins] ) +'\n')
    outfile.write( 'observation'.ljust(lspace)+''.join([str(self.observation[b]).rjust(self.defWidth) for b in self.bins]) +'\n')
    if self.hasContamination:
      outfile.write( 'contamination'.ljust(lspace)+''.join([str(self.contamination[b]).rjust(self.defWidth) for b in self.bins]) +'\n')
    outfile.write('\n')
    outfile.write( 'bin'.ljust(lspace)+''.join( [''.join([b.rjust(self.defWidth) for p in self.processes[b]] ) for b in self.bins]) +'\n')
    outfile.write( 'process'.ljust(lspace)+''.join( [''.join([p.rjust(self.defWidth) for p in self.processes[b]] ) for b in self.bins]) +'\n')
    outfile.write( 'process'.ljust(lspace)+''.join( [''.join([str(numberID[p]).rjust(self.defWidth) for p in self.processes[b]] ) for b in self.bins]) +'\n')
    outfile.write( 'rate'.ljust(lspace)+''.join( [''.join([self.mfs(self.expectation[(b,p)]).rjust(self.defWidth) for p in self.processes[b]] ) for b in self.bins]) +'\n')
    outfile.write('\n')

    for u in self.uncertainties:
      outfile.write( u.ljust(self.maxUncNameWidth)+' '+self.uncertaintyString[u].ljust(self.maxUncStrWidth)+' '+
                     ''.join( [''.join([self.getUncertaintyString((u,b,p)).rjust(self.defWidth) for p in self.processes[b]] ) for b in self.bins]) +'\n')

    #if len(self.groups.keys())>0:
    #  outfile.write('\n')
    #  for g in sorted(self.groups.keys()):
    #    outfile.write(g+" group =")
    #    for gg in sorted(self.groups[g]):
    #      outfile.write(" "+gg)
    #    outfile.write('\n')

    for l in self.extraLines:
      outfile.write(l+"\n")

    outfile.close()

  def readResFile(self, fname):
    import ROOT
    f = ROOT.TFile.Open(fname)
    t = f.Get("limit")
    l = t.GetLeaf("limit")
    qE = t.GetLeaf("quantileExpected")
    limit = {}
    preFac = 1.
    for i in range(t.GetEntries()):
        t.GetEntry(i)
#        limit["{0:.3f}".format(round(qE.GetValue(),3))] = preFac*l.GetValue()
        limit["{0:.3f}".format(round(qE.GetValue(),3))] = preFac*l.GetValue()
    f.Close()
    return limit

  def calcLimit(self, fname="", options="", logfile=None):
    import uuid, os 
    uniqueDirname="."
    unique=False
    if fname=="":
      uniqueDirname = "tmp_"+str(uuid.uuid4())
      unique=True
      os.system('mkdir '+uniqueDirname)
      fname = str(uuid.uuid4())+".txt"
      self.writeToFile(uniqueDirname+"/"+fname)
    else:
      self.writeToFile(fname)
    cmd = "cd "+uniqueDirname+";combine --saveWorkspace -M Asymptotic "+options+" "+fname
    if logfile!=None:
      cmd = "( " + cmd + ") > "+logfile+" 2>&1"
    os.system(cmd)
    try:
      res= self.readResFile(uniqueDirname+"/higgsCombineTest.Asymptotic.mH120.root")
    except:
      res=None
      print "Did not succeed."
    os.system("rm -rf roostats-*")
    if unique:
       os.system("rm -rf "+uniqueDirname)
    else:
      if res:
        print res
        os.system("cp higgsCombineTest.Asymptotic.mH120.root "+fname.replace('.txt','')+'.root')
    
    return res


  def calcSignif(self, fname="", options=""):
    import uuid, os 
    uniqueDirname=""
    unique=False
    if fname=="":
      uniqueDirname = str(uuid.uuid4())
      unique=True
      os.system('mkdir '+uniqueDirname)
      fname = str(uuid.uuid4())+".txt"
      self.writeToFile(uniqueDirname+"/"+fname)
    else:
      self.writeToFile(fname)
    os.system("cd "+uniqueDirname+";combine --saveWorkspace  -M ProfileLikelihood --significance "+fname+" -t -1 --expectSignal=1 ")
    try:
      res= self.readResFile(uniqueDirname+"/higgsCombineTest.ProfileLikelihood.mH120.root")
    except:
      res=None
      print "Did not succeed."
    os.system("rm -rf roostats-*")
    if unique:
       os.system("rm -rf "+uniqueDirname)
    else:
      if res:
        print res
        os.system("cp higgsCombineTest.ProfileLikelihood.mH120.root "+fname.replace('.txt','')+'.root')

    return res

