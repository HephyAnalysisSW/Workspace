from Workspace.DegenerateStopAnalysis.tools.cardFileWriter import cardFileWriter
import Workspace.DegenerateStopAnalysis.tools.degTools as degTools

GAUSSIAN_THRESHOLD = 100  # counts above this will be represented with gaussian instead of poisonian distribution

def safe_int(x):
    try:
        return int(round(x.val))
    except:
        return int(round(x))

def safe_zero(v, default = 1e-6):
    v = getattr(v, 'val', v)
    if v == 0:
        v = default
    return v

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




def isAsymFloat( x , make_tuple = False):
    keys = ['central', 'up','down']
    typ = None
    ret = []
    if all( [hasattr(x,k) for k in keys] ):
        ret = [ getattr(x,k) for k in keys] 
        typ =  "asym_float"
    if type(x)==dict and all([ x.has_key(k) for k in keys ]):
        ret = [ x[k] for k in keys] 
        typ =  "asym_dict"
    if type(x) in [list, tuple] and len(x) == 3:
        ret = x 
        typ =  "asym_list"
    if not make_tuple:
        return typ
    else:
        return ret 

def convertAsymFloatToSym( x , opt="max" ):
    asym = isAsymFloat(x, make_tuple = True)
    if not asym:
        return x
    val, up, down = asym
    if opt == "max":
        sigma = max( up, down )
    elif opt == "ave":
        sigma = (up+down)/2.
    elif opt == "up":
        sigma = up
    elif opt == "down":
        sigma = down
    return degTools.u_float( val, sigma )


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
                 defWidth = 18  , maxUncNameWidth = 20  , maxUncStrWidth= 10 , percision = 6,
                 lnn_gmn_threshold = 100,
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

        self.lnn_gmn_threshold = lnn_gmn_threshold


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

    def specifyObservations(self, yieldDict, obsProcess="Data", makeInt=True , bins = None):
        bins = bins if bins else self.bins
        func = safe_int if makeInt==True else makeInt
        for b in bins:
            obs = self.getProcValFromYieldDict( yieldDict, obsProcess, b,  func=func) 
            self.specifyObservation(b,obs)

    def specifyBackgroundExpectations(self, yieldDict, bkgProcesses ):
        for b in self.bins:
            for p in bkgProcesses:
                if p not in self.processNames:
                    self.processNames.append(p)
                #pName = getGoodKeyForDict( yieldDict, p, self.niceProcessNames)
                exp   = yieldDict[p][b]
                if  getattr(exp,"val", exp) < 0:
                    print "------------\n WARNING Negative Value ( %s ) %s %s"%(exp, b, p )
                    exp.val = 0
                    print "seeting it to %s"%exp
                exp   = safe_val(exp , func = safe_zero)
                pName = self.niceProcessNames[p] if p in self.niceProcessNames else p
                self.specifyExpectation(b,pName , exp)

    def specifySignalExpectations(self, yieldDict, sigProcess, scale=1.0):
        '''
            scale can be used in case signal xsec is too large for combine
            Just make sure to rescale the output limits
        '''
        self.niceProcessNames['signal']=sigProcess
        self.signalProcess = sigProcess
        for b in self.bins:
            exp = yieldDict[sigProcess][b]
            exp = safe_val(exp)
            if  getattr(exp,"val", exp) < 0:
                print "------------\n WARNING Negative Value ( %s ) %s %s"%(exp, b, p )
                exp.val = 0
                print "seeting it to %s"%exp
                exp = safe_val( exp, func = safe_zero )
            exp *= scale
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
        #for syst_name, syst_info in uncert_dict.iteritems():
        #    if uncerts and not syst_name in uncerts:
        #        #print "skipping uncert: %s, not in the requested list:%s"%(syst_name, uncerts)
        #        continue
        for syst_name in uncerts:
            syst_info = uncert_dict[syst_name]

            isSimpleSystDict = False if syst_info.get('bins') else True
                 
            if not isSimpleSystDict:
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
                        #print  p 
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
                            assert False
                            if p in self.processes[b]:
                                self.specifyUncertainty( sname, b, p, uncert_val)
                            elif pName in self.processes[b]:
                                self.specifyUncertainty( sname, b, pName, uncert_val)
                            else:
                                raise Exception("Neither %s or its niceName (%s) are in the process list for bin %s:%s"%(p,pName, b, self.processes[b] ) )
 
        
            else:
                sname = prefix+syst_name
                stype = 'lnN' 
                self.addUncertainty(sname, stype)
                #print bins
                for b in bins:
                    bName = getGoodKeyForDict( syst_info , b, self.niceBinNames )
                    for p in self.processes[bName]:
                        if processes and p not in processes:
                            continue
                        try:
                            pName = getGoodKeyForDict(syst_info[bName], p, self.niceProcessNames)
                        except Exception:
                            print "%s Doesnt seem to be there for bin %s and syst %s"%(p, bName, sname)
                            #print p in syst_info[bName]
                            #print syst_info[bName].keys()
                            #print p in self.niceProcessNames
                            #print self.niceProcessNames.get(p,'') in syst_info[bName]
                            continue
                        try:
                            uncert_val = safe_val(syst_info[bName][pName])
                        except AssertionError:
                            uncert_val = safe_val(syst_info[bName][pName] , func = lambda x: x if x>0 else 0  )
                        if uncert_val == 1:
                            continue

                        if p in self.processes[b]:
                            self.specifyUncertainty( sname, bName, p, uncert_val)
                        elif pName in self.processes[b]:
                            self.specifyUncertainty( sname, bName, pName, uncert_val)
                        else:
                            raise Exception("Neither %s or its niceName (%s) are in the process list for bin %s:%s"%(p,pName, b, self.processes[b] ) )
                        #self.specifyUncertainty( sname, bName, p, uncert_val)
    
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
                #pList = [pName]
                #value = degTools.u_float(0)
                value = yieldDict[pName][b]  
                #for p_ in pList:                  ### Combining Yields for "other" samples... 
                #    if hasattr( yieldDict[p_][b], "sigma"):         
                #        value += yieldDict[p_][b] 
                #    else: 
                #        raise NotImplementedError("yield dict values should be instance of the u_float class") 
                #print b, sname, pName 
                #if pName == "Fakes":
                #    print pName, value
                is_asym = isAsymFloat(value, make_tuple = True)
                if is_asym:
                    v, up, down = is_asym
                    self.addUncertainty(sname, 'lnN')
                    if up == down:
                        # I'm doing this just to trick cfw to put lnN values here
                        unc = 1 + round( up/v, 4 )
                    else:
                        down_e = (v-abs(down))/v if v else 1.0
                        up_e = (v+abs(up))/v if v else 1.0
                        unc = "%0.3f/%0.3f"%(safe_zero(down_e, 1e-3),up_e)
                    self.specifyUncertainty(sname, b, p, unc) 
                    #print pName, sname, unc
                    #assert False
                else:
                    v = value.val 
                    sigma = value.sigma 
                    n = int(round(v*v/(sigma*sigma))) if sigma else 1 
                    #print "STAT UNCERT", sname, b, pName  
                    #if v >= lnn_gmn_threshold:    #Use logNormal: 
                    if n >= self.lnn_gmn_threshold:    #Use logNormal: 
                        self.addUncertainty(sname, 'lnN') 
                        unc = 1 + round(sigma/v,4) if v else 1    ## relative unc.  
                    else: 
                        #n = int(sigma) if int(sigma) else 1 
                        if not n: n = 1 
                        #print '----------', sname, "gmN", pName, value, v, sigma, n 
                        WRONGSTAT= False
                        if WRONGSTAT:
                            import math
                            self.addUncertainty( sname, "lnN" )  
                            unc =  1+1/math.sqrt( v ) ## this is irrelevant, as the actual value will be calculated by cardFileWriter based on the rate and N 
                            
                        else: 
                            self.addUncertainty( sname, "gmN", n  )  
                            unc = 1  ## this is irrelevant, as the actual value will be calculated by cardFileWriter based on the rate and N 
                    self.specifyUncertainty(sname,b,p,unc) 

    def addRateParam( self, name, bin, process, val_or_form , minmax_or_arg = None ):
        isFormula=True if "@" in str(val_or_form) else False
        if not minmax_or_arg:
            if isFormula:
                raise Exception("ERROR: rateParam: formula given but no args! Formula: %s , %s"%(val_or_form, minmax_or_arg))
        else:
            if not isFormula and minmax_or_arg and not type(minmax_or_arg)==list :
                raise Exception("ERROR: rateParam: min-max need to be a list! Value: %s, min-max:%s"%(val_or_form, minmax_or_arg) )
            else:
                minmax_or_arg = str(minmax_or_arg).replace(" ","") # combine doesn't like extra spaces in rateparam
        line = "{name} rateParam {bin} {process} {val_or_form} {minmax_or_arg}".format( name=name, bin=bin, process=process, val_or_form=val_or_form, minmax_or_arg=minmax_or_arg)
        self.addExtraLine(line)


#uncerts = []
#for syst_name, syst_info in syst_dict.iteritems():
#    uncert_dict ={'name':syst_name, 'type':syst_info['type'] }
#    bins = syst_info['bins'].keys()
#    for b in bins:
#        syst_info['bins'][b]

