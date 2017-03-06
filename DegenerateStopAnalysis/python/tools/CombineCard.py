from Workspace.DegenerateStopAnalysis.tools.cardFileWriter import cardFileWriter
import Workspace.DegenerateStopAnalysis.tools.degTools as degTools


def safe_int(x):
    try:
        return int(x.val)
    except:
        return int(x)

def safe_val(x, func=None):
    try:
        val =  x.val
    except AttributeError:
        val = x

    if func:
        ret =func(val)
    else:
        ret = val
    if ret < 0:
        assert False
    return ret

def getGoodKeyForDict(dict, key, niceNames={} , reverse_search = True):
    #print "================================================ + ", key
    #print key
    #print niceNames
    if key in dict:
        goodKey = key
        pass
    elif key in niceNames and niceNames[key] in dict:
        goodKey = niceNames[key]
    elif reverse_search:
        niceNamesReverse={}
        for k,v in niceNames.iteritems():
            niceNamesReverse[v]=k
        goodKey = getGoodKeyForDict(dict, key, niceNamesReverse, reverse_search=False)
    else:
        raise Exception("key %s, or its niceName were not found in dict (dict keys: %r)"%(key, dict.keys()) )
    #print "================================================ -", goodKey
    return goodKey #, dict[goodKey]

class CombinedCard(cardFileWriter):
    #def __init__(self):
    def __init__(self, niceProcessNames = {'tt':'TTJets', 'w':'WJets', }, niceBinNames={},
                 defWidth = 15  , maxUncNameWidth = 20  , maxUncStrWidth= 10 , percision = 6,
                 verbose = False,
                ):
        cardFileWriter.__init__(self)
        self.niceProcessNames = niceProcessNames
        self.niceBinNames     = niceBinNames
        self.processNames     = ['signal']

        self.defWidth          = defWidth
        self.maxUncNameWidth   = maxUncNameWidth
        self.maxUncStrWidth    = maxUncStrWidth
        self.precision         = percision



    def getProcValFromYieldDict(self, yieldDict, p, b, func=None):
        pName = getGoodKeyForDict(yieldDict, p, self.niceProcessNames)
        bName = getGoodKeyForDict(yieldDict[pName],b , self.niceBinNames)
        val = yieldDict[pName][bName]
        if func:
            val = func(val)
        return val

    def addBins(self, processes, bins):
        processNames = []
        for p in processes:
            if p in self.niceProcessNames:
                processNames.append( self.niceProcessNames[p])
            else:
                processNames.append(p)
        for b in bins:
            niceBinName = self.niceBinNames[b] if b in self.niceBinNames else b
            self.addBin(b,processNames,niceBinName)
            #self.processNames = processes

    def specifyObservations(self, yieldDict, obsProcess="Data", makeInt=True ):
        for b in self.bins:
            obs = self.getProcValFromYieldDict( yieldDict, obsProcess, b,  func=safe_int) 
            self.specifyObservation(b,obs)

    def specifyBackgroundExpectations(self, yieldDict, bkgProcesses ):
        for b in self.bins:
            for p in bkgProcesses:
                if p not in self.processNames:
                    self.processNames.append(p)
                #pName = getGoodKeyForDict( yieldDict, p, self.niceProcessNames)
                exp = yieldDict[p][b]
                exp = safe_val(exp)
                pName = self.niceProcessNames[p] if p in self.niceProcessNames else p
                self.specifyExpectation(b,pName , exp)

    def specifySignalExpectations(self, yieldDict, sigProcess):
        self.niceProcessNames['signal']=sigProcess
        self.signalProcess = sigProcess
        for b in self.bins:
            exp = yieldDict[sigProcess][b]
            exp = safe_val(exp)
            self.specifyExpectation(b,'signal', exp)

    def specifyFlatUncertainty(self, u,  val, bins=None, processes=None):
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

    def specifyUncertaintiesFromDict(self, uncert_dict , uncerts=[], processes=[], bins=[], prefix=""):
        for syst_name, syst_info in uncert_dict.iteritems():
            if uncerts and not syst_name in uncerts:
                #print "skipping uncert: %s, not in the requested list:%s"%(syst_name, uncerts)
                continue
            stype = syst_info['type']
            sbins = syst_info['bins']

            if syst_info.get("uncorr"):
                print "Adding %s as uncorrelated"%syst_name
                somethingWrong = False
                if not processes or len(processes)!=1:
                    somethingWrong = True
                if somethingWrong: 
                    raise Exception("for uncorrelated systematics you must specify exactly one process")
                p = processes[0]
                for b in self.bins:
                    if not b in sbins.keys():
                        raise Exception("bin %s not found in the syst_dict....(maybe I should just continue?)"%b)
                        #continue
                    #sname = syst_name +b+"Sys"
                    print  p 
                    pName = getGoodKeyForDict(sbins[b], p, self.niceProcessNames)
                    sname = p + b + "Sys"
                    self.addUncertainty(sname, stype)
                    uncert_val = safe_val(sbins[b][pName])
                    #print syst_name, p, b, uncert_val
                    self.specifyUncertainty(  sname, b, p, uncert_val )

            else:
                sname = prefix+syst_name 
                self.addUncertainty(sname, stype)
                for b in sbins:
                    if not b in self.bins:
                        continue
                    for p in self.processes[b]:
                        if processes and p not in processes:
                            continue
                        #print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~' ,p
                        pName = getGoodKeyForDict(sbins[b], p, self.niceProcessNames)
                        if not pName in sbins[b]: 
                            raise Exception("process %s (%s) not found in %s"%(p,pName, sbins[b].keys()))
                        #print sname, b, p
                        try:
                            uncert_val = safe_val(sbins[b][pName])
                        except AssertionError:
                            uncert_val = safe_val(sbins[b][pName] , func = lambda x: x if x>0 else 0  )
                            
                        #print '-----------------------------------------', sname, b, p, pName, uncert_val
                        self.specifyUncertainty( sname, b, p, uncert_val)
    
    def addStatisticalUncertainties(self, yieldDict, processes=[], bins=[]) :
        for b in self.bins:
            #print '--------', b
            if bins and b not in bins:
                continue   
            for p in self.processes[b]:
                if processes and p not in processes: 
                    continue
                #print '=============', p
                pName = getGoodKeyForDict(yieldDict, p, self.niceProcessNames)
                sname = p+ b + "Sta"
                #print sname
                #pList = [x for x in bkgs+[sig] if processNames[x]==pName ] 
                pList = [pName]
                value = degTools.u_float(0) 
                for p_ in pList:                  ### Combining Yields for "other" samples... 
                    if hasattr( yieldDict[p_][b], "sigma"):         
                        value += yieldDict[p_][b] 
                    else: 
                        raise NotImplementedError("yield dict values should be instance of the u_float class") 
                #print b, sname, pName 
                v = value.val 
                sigma = value.sigma 
                #print "STAT UNCERT", sname, b, pName  
                lnn_gmn_threshold = 100 
                if v >= lnn_gmn_threshold:    #Use logNormal: 
                    self.addUncertainty(sname, 'lnN') 
                    unc = 1 + round(sigma/v,4) if v else 1    ## relative unc.  
                else: 
                    #n = int(sigma) if int(sigma) else 1 
                    n = int(round(v*v/(sigma*sigma))) if sigma else 1 
                    if not n: n = 1 
                    #print sname, "gmN", n 
                    self.addUncertainty( sname, "gmN", n  )  
                    unc = 1  ## this is irrelevant, as the actual value will be calculated by cardFileWriter based on the rate and N 
                self.specifyUncertainty(sname,b,p,unc) 



#uncerts = []
#for syst_name, syst_info in syst_dict.iteritems():
#    uncert_dict ={'name':syst_name, 'type':syst_info['type'] }
#    bins = syst_info['bins'].keys()
#    for b in bins:
#        syst_info['bins'][b]

