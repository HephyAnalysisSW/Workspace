#from Workspace.DegenerateStopAnalysis.cardFileWriter import cardFileWriter
from Workspace.DegenerateStopAnalysis.tools.cardFileWriter import cardFileWriter
from Workspace.DegenerateStopAnalysis.navidTools.FOM import get_float
from copy import deepcopy

import pickle
import yaml

import glob
from os.path import basename, splitext

import ROOT
import re





#pickleFiles = ["/afs/hephy.at/user/n/nrad/CMSSW/CMSSW_7_4_7/src/Workspace/DegenerateStopAnalysis/plotsNavid/analysis/pkl/SR1_r1_a.pkl"]


def getLimit(yld, sig=None          , outDir    = "./cards/", postfix = ""     , 
                  sys_uncorr=1.2    , sys_corr  = 1.06      , sys_pkl = None   , 
                  new_systs_map  = {}   ,  new_bins_map = {},  
                  calc_limit=False  , debug     = False     , simplify_processes = True, 
                  defWidth = 15, maxUncNameWidth = 20, maxUncStrWidth= 10 , percision = 6,

                ):
    """
    sys_map = { 'new_bin':'old_bin'  } can be used for bins which are not in the sys_pkl
    in order to assign a uncert value based on another bin which does exist in sys_pkl
    """

    c = cardFileWriter()
    c.defWidth          = defWidth
    c.maxUncNameWidth   = maxUncNameWidth
    c.maxUncStrWidth    = maxUncStrWidth
    c.precision         = percision

    bins = yld.cutNames
      
    if not sig:
        sig  = yld.sigList[0]
    elif sig in yld.sigList:
        pass
    else:
        assert False, "Signal %s not in the yield dictionary signal list:%s" %(sig, yld.sigList)
        


    if simplify_processes:

        main_bkgs = ['w', 'tt']
        rest_bkgs = ['qcd', 'z'] 

        main_bkgs = [bkg for bkg in main_bkgs if bkg in yld.sampleNames ]
        rest_bkgs = [bkg for bkg in rest_bkgs if bkg in yld.sampleNames ]

        main_processes = [ yld.sampleNames[p] for p in main_bkgs ]
        other_processes= [ yld.sampleNames[p] for p in rest_bkgs ]

        bkgs = main_bkgs + rest_bkgs
        processes = ['signal'] + main_processes + ['other']
        processNames = {sig:'signal'}
        for p in main_bkgs:
            ### super ugly to get the key from value.... maybe implement this in the YieldClass instead
            #if yld.sampleNames.values().count(p) =! 1:
            #    raise Exception("Either multiple processes with the same name, or unknown process name, too vauge to proceed! %s , %s "%(p, yld_bkg_list))
            #yld_process = yld.sampleNames[ yld.sampleNames.keys()[yld.sampleNames.values().index(p)] ]
            ###
            processNames.update( {p : yld.sampleNames[p] }  )
        for p in rest_bkgs:
            processNames.update( {p : 'other' }  )
            

    else:
        bkgs = yld.bkgList
        processNames = yld.sampleNames
        processNames.update(  { sig:'signal'} )

        processes = ['signal'] + [yld.sampleNames[p] for p in bkgs]


    #print "ProcessNames:",  processNames


    use_simple_sys = True if not sys_pkl else False

    add_stat_uncer = True

    lnn_gmn_threshold = 100     ## for stat_uncert

    ####################################### Simple systs as specified by sys_corr and sys_uncorr
    #! this part is not maintained
    if use_simple_sys:                        
        c.addUncertainty("Sys", 'lnN')
        for iBin, bin in enumerate(bins,1):
            c.addBin(bin, processes ,bin)
            c.specifyObservation(bin,int( get_float(yld.yieldDictFull["Total"][bin]) ))
            sysName = "Sys_%s"%(bin)
            c.addUncertainty(sysName, 'lnN')
            c.addUncertainty(sysName+"_sig", 'lnN')
            for bkg in main_bkgs:
              c.specifyExpectation(bin, processNames[bkg] ,get_float(yld.yieldDictFull[bkg][bin]) )
              c.specifyUncertainty('Sys',bin,processNames[bkg],sys_corr)
              #sysName = "Sys_%s"%bkg
              c.specifyUncertainty(sysName,bin,processNames[bkg],sys_uncorr)
            other_exp = sum([get_float(yld.yieldDict[rest_bkg][bin])  for rest_bkg in rest_bkgs])            
            c.specifyExpectation(bin,"other", other_exp)
            c.specifyUncertainty(sysName+"_other",bin,'other',sys_uncorr)
            c.specifyExpectation(bin,"signal",get_float(yld.yieldDictFull[sig][bin]))
            c.specifyUncertainty(sysName+"_sig",bin,'signal',sys_uncorr)
            #c.specifyUncertainty('Sys',bin,"signal",sys_corr)
    #!

    ####################################### Full systs based on sys_pkl
    else:
        for iBin, bin in enumerate(bins,1):
            c.addBin(bin,processes,bin)
            c.specifyObservation(bin,int( get_float(yld.yieldDictFull["Total"][bin]) ))
            for bkg in bkgs:
                c.specifyExpectation(bin,processNames[bkg],get_float(yld.yieldDictFull[bkg][bin]))
            other_exp = sum([get_float(yld.yieldDict[rest_bkg][bin])  for rest_bkg in rest_bkgs])
            c.specifyExpectation(bin,"other", other_exp)
            c.specifyExpectation(bin,"signal",get_float(yld.yieldDictFull[sig][bin]))

        if sys_pkl.endswith(".pkl"):
            card    = pickle.load(open(sys_pkl,"r"))
        elif sys_pkl.endswith(".json"):
            card    = yaml.safe_load(open(sys_pkl,"r"))
        else:
            raise Exception("sys_pkl should be either json or pkl, but it's neither: %s"%sys_pkl)
        systs   = card['systs']

        def_syst_map = {
                        "TTJetsSRL1cSys" : "TTJetsSRL1bSys",
                     }
        new_systs_map.update( def_syst_map)
        #new_bins_map = {
        #                "met300"         : "SRH1a",
        #            }

        #
        # sort systs in a semi-nice way
        #

        types_to_keep   = ["_corr", "Sys"]
        types_to_ignore = ["Sta"]           #######  Statistical Uncert should not be read from the pickle file
        types   = types_to_keep + types_to_ignore
        samples = c.processes.keys()
        systs_sorted   = []
        systs_unsorted = systs.keys()
        for t in types:
            l = [ x for x in systs_unsorted if t in x and any([samp in x for samp in samples]) ]

            #print "l=" , l
            #print "processes=" , processes
            #print "types=", types

            if t in types_to_keep:
                systs_sorted.extend( sortBy(l,bins,processes) ) 
            for x in l: 
                systs_unsorted.pop( systs_unsorted.index(x) )
        systs_sorted= sorted(systs_unsorted) + systs_sorted

        #
        ##  Copying Systematics which are correlated across bins
        #

        #### !!!!!!!!!!!!!!!!!!!!!!!!!!! FIX ME: Need to also include the any new bins not in the sys pkl (using the syst_map)

        systs_to_keep = []

        for sname in systs:
            if any([pName in sname for pName in processes]):    ### Process based systs will be added later
                continue 
            if any([b in sname for b in processes]):            ### Bin based systs will be added later
                continue 
            #print "=============== ", sname
            systs_to_keep.append(sname)
        systs_to_keep = sorted(systs_to_keep, key= lambda x: ("CR" in x)*5 or ("sig" in x)*4 or ("W" in x)*3, reverse=True)

        #
        # Simply Copy the systs from the pkl file to the new card (Don't care if they don't match)
        #

        #print "systs to keep: ", systs_to_keep
        for sname  in systs_to_keep:
            if new_bins_map:                        ## if there are new bins which aren't in the current systs, add them to the new_sbins based on the map
                new_sbins = make_bin_proc_dict_from_systs( 
                                                            bins = systs[sname]['bins'].keys() + new_bins_map.keys() ,
                                                            processes = processes,
                                                            syst     = systs[sname],
                                                            new_bins_map = new_bins_map, ) 
                assign_uncert_to_cfw(  c, sname, systs[sname]['type'], new_sbins  )                                           
            else:
                assign_syst_to_cfw( c, sname, systs[sname] )
            #value = systs[sname]
            #stype = value['type']
            #sbins = value['bins']
            #if stype=="gmN":
            #    sn = value['n'] 
            #    #c.addUncertainty(sname,stype, sn )
            #    c.addUncertainty(sname,stype, sn )
            #else:
            #    c.addUncertainty(sname,stype)
            ## each systematics contains entries for bins ...
            #for b in sbins:
            #    # ... and processes
            #    for p in sbins[b]:
            #        # extract value and add it, if non-zero
            #        v = sbins[b][p]
            #        if v>1.e-6:
            #            c.specifyUncertainty(sname,b,p,v)



        #
        ## Adding systematics 
        #
        for b in bins:
            for pName in main_processes + ['other']:
                sysname = pName + b + "Sys"
                if   sysname in systs:      # if syst exists in the pkl use the value given in the pkl file
                    #print "-----------------------", sysname
                    assign_syst_to_cfw(c,sysname,systs[sysname])
                elif sysname in new_systs_map:  # if bin is not in the pkl, a map be given to assign a syst from the pkl to the new bin.
                    ##### !!!!!!!!! FIX ME: Dublicate Systematics in the old bin and newbin
                    print "---------------------!------------------- assigning systematics to %s from %s"%(sysname, new_systs_map[sysname])

                    sysname_old = new_systs_map[sysname]
                    bin_name_old   = sysname_old.replace(pName,"").replace('Sys','')
                    print bin_name_old, sysname_old
                    new_syst = deepcopy( systs[sysname_old] )
                    new_syst['bins'][b][pName] = systs[sysname_old]['bins'][bin_name_old][pName]
                    new_syst['bins'][bin_name_old][pName] = 0.0 


                    assign_syst_to_cfw(c,sysname, new_syst )
                elif b in new_bins_map:
                    bin_name_old = new_bins_map[b]
                    sysname_old = pName + bin_name_old + "Sys"
                    print bin_name_old, b, new_bins_map, new_bins_map[b]
                    if not sysname_old in systs:
                        raise Exception("Unable to assign a value for %s. Does not match to any item in %s \n \n or \n \n %s"%(sysname_old, systs.keys(), new_bins_map  ))
                    new_syst = deepcopy( systs[sysname_old] )
                    if not new_syst['bins'].has_key(b): 
                        new_syst['bins'][b]={}
                    new_syst['bins'][b][pName] = systs[sysname_old]['bins'][bin_name_old][pName]  
                    new_syst['bins'][bin_name_old][pName] = 0.0 
                    assign_syst_to_cfw(c, sysname, new_syst )
                    #assign_uncert_to_cfw(cfw, sysname, systs[sysname_old]['type'] , new_syst['bins'] , sn = 0.0)
                    print "-----------------!----------- Assigning systematics for: ", b, bin_name_old , sysname, sysname_old
                elif "CR" in b:
                    print "No Systematics for bin: %s"%b
                else:  # I don't know what to do now!
                    print "No Systematics for %s"%sysname
                    raise Exception("Unable to assign a value for %s. Does not match to any item in %s \n \n or \n \n %s"%(sysname, systs.keys(), new_systs_map  ) )

        #
        # Adding stat uncert based on yields
        #
        if add_stat_uncer:
            for b in bins:
                for pName in processes:
                    sname = pName + b + "Sta"
                    pList = [x for x in bkgs+[sig] if processNames[x]==pName ]
                    #print "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz" , pName, pList    
                    value = 0
                    for p in pList:                  ### Combining Yields for "other" samples...
                        if hasattr( yld.yieldDictFull[p][b], "sigma"):        
                            value += yld.yieldDictFull[p][b]
                            #print "--------------", p,value
                        else:
                            raise NotImplementedError("yield dict values should be instance of the u_float class")

                    v = value.val
                    sigma = value.sigma
                    if v >= lnn_gmn_threshold:    #Use logNormal:
                        c.addUncertainty(sname, 'lnN')
                        unc = 1 + round(sigma/v,4) if v else 1    ## relative unc. 
                        c.specifyUncertainty(sname, b, pName, unc)  
                    else:
                        #n = int(sigma) if int(sigma) else 1
                        n = int(round(v*v/(sigma*sigma))) if sigma else 1
                        #print sname, "gmN", n
                        c.addUncertainty( sname, "gmN", n  ) 
                        unc = 1  ## this is irrelevant, as the actual value will be calculated by cardFileWriter based on the rate and N
                        c.specifyUncertainty(sname,b,pName,unc)
                                    
            #stat_uncerts = sortBy(stat_uncerts, bins, processes)             

            #for b in c.bins:
            #    for p in yld.bkgList + [sig]:
            #        pName = processNames[p]
            #        sname = pName + b + "Sta"
            #        v = get_float(yld.yieldDictFull[p][b] )
            #        sigma = get_float(yld.yieldDictFull[p][b] , sigma=True )
            #        if v >= lnn_gmn_threshold:    #Use logNormal:
            #            c.addUncertainty(sname, 'lnN')
            #            unc = 1 + round(sigma/v,4) if v else 1    ## relative unc. 
            #            c.specifyUncertainty(sname, b, pName, unc)  
            #        else:
            #            #n = int(sigma) if int(sigma) else 1
            #            n = int(round(v*v/(sigma*sigma))) if sigma else 1
            #            print sname, "gmN", n
            #            c.addUncertainty( sname, "gmN", n  ) 
            #            unc = 1  ## this is irrelevant, as the actual value will be calculated by cardFileWriter based on the rate and N
            #            c.specifyUncertainty(sname,b,pName,unc)


    badBins=[]
    ############################### Check for problematic* bins    
    #  return c
    if debug:
        print "--------debug-------------"
        print c.bins
        print c.processes
        print c.expectation
        print "--------debug-------------"

    for bin in c.bins:
        expectations = [c.expectation[( bin, process )] for process in c.processes[bin]] 
        bkgExpectations = [ c.expectation[(bin,processNames[process])] for process in bkgs]
        print bin, any(expectations), c.processes[bin], expectations
        if not any(expectations):
          print "############ no processes contributing to the bin %s, to make life easier the bin will be removed from card but make sure everything is ok"%bin
          print bin, c.processes[bin], expectations   
          badBins.append(bin)
          #print c.bins
        if not any(bkgExpectations):
          print "############ no background contributing to the bin %s, a small non zero value (0.001) has been assigned to the bin"%bin
          print bkgs, process, c.expectation
          #c.expectation[(bin,process[bkgs[0] ])]=0.001
          c.expectation[(bin, process)]=0.001
          print bin, c.processes[bin], expectations   
          
    for bin in badBins:
        c.bins.remove(bin)
    
    #sigName  =  yld.yieldDictFull[sig][0]
    sigName  =  yld.sampleNames[sig]
    filename =  sigName + "_" + yld.tableName
    if postfix:
        if not postfix.startswith("_"):
            postfix = "_" + postfix
        filename += postfix

    
    cardName='%s.txt'%filename
    c.writeToFile('%s/%s'%(outDir,cardName))
    print "Card Written To: %s/%s"%(outDir,cardName)
    print "---------------------------------------------", sigName, sig
    #limits=c.calcLimit("./output/%s"%cardName)

    if calc_limit:
        limits = c.calcLimit()
    else:
        limits = None
    #print cardName,   "median:  ", limits['0.500']
    return (c, limits)


#
# Uncert Tools
#


def make_bin_proc_dict(bins,processes,def_val=0):
    return { b:{p:def_val for p in processes} for b in bins}

def make_bin_proc_dict_from_systs(bins,processes,syst,new_bins_map):
    new_syst = make_bin_proc_dict(bins,processes)
    for b in bins:
        if b in syst['bins']:
            bin_name = b
        elif b in new_bins_map:
            bin_name = new_bins_map[b]
        else:
            raise Exception("bin not recognized %s"%b)
        for p in processes:
            #print p, b, bin_name, syst['bins'][bin_name], syst
            new_syst[b][p] = syst['bins'][bin_name][p]
    return new_syst 


def assign_syst_to_cfw(cfw, sname, syst):
    stype = syst['type']
    sbins = syst['bins']
    if stype=="gmN":
        sn = syst['n']
        #c.addUncertainty(sname,stype, sn )
        cfw.addUncertainty(sname,stype, sn )
    else:
        cfw.addUncertainty(sname,stype)
    # each systematics contains entries for bins ...
    for b in sbins:
        # ... and processes
        for p in sbins[b]:
            # extract value and add it, if non-zero
            v = sbins[b][p]
            if v>1.e-6:
                cfw.specifyUncertainty(sname,b,p,v)


def assign_uncert_to_cfw(cfw, sname, stype, sbins, sn = 0.0):
    if stype=="gmN":
        cfw.addUncertainty(sname,stype, sn )
    else:
        cfw.addUncertainty(sname,stype)
    # each systematics contains entries for bins ...
    for b in sbins:
        # ... and processes
        for p in sbins[b]:
            # extract value and add it, if non-zero
            v = sbins[b][p]
            if v>1.e-6:
                cfw.specifyUncertainty(sname,b,p,v)






def get_index(string,by):
    sort_indices = [ i1 in string for i1 in by ]
    try: 
        return sort_indices.index(True)
    except ValueError:
        return 0 


def sortBy(l,by_l1,by_l2):
    return sorted(l , key = lambda x: ( get_index(x,by_l1), get_index(x, by_l2))   ) ## ordering first by bin, then by processes 



def try_int(s):
    "Convert to integer if possible."
    try: return int(s)
    except: return s

def natsort_key(s):
    "Used internally to get a tuple by which s is sorted."
    import re
    return map(try_int, re.findall(r'(\d+|\D+)', s))
 

def plotLimits(limitDict):
  nLimits = len(limitDict)
  limitPlot = ROOT.TH1F("limitPlot","limitPlot",nLimits,0,nLimits)
  for i,fname in enumerate(sorted(limitDict, key=natsort_key),1):
    limit=limitDict[fname][1]['0.500']
    limitPlot.GetXaxis().SetBinLabel(i,fname)
    limitPlot.SetBinContent(i,limit)

  limitPlot.GetYaxis().SetTitle("r")
  limitPlot.SetTitle("Median Expected Limits")
  return limitPlot





import subprocess

#def calcLimitFromCard(card="./cards/T2DegStop_300_270_cards.txt"): 
def calcLimitFromCard(card="./cards/T2DegStop_300_270_cards.txt", name="", mass=""):
    command = ['combine', '--saveWorkspace', '-M', 'Asymptotic'] 
    if name:
        command.extend(["--name", name])
    if mass:
        command.extend(["--mass, mass"])
    command.append(card)
    out = subprocess.Popen(command, stdout = subprocess.PIPE)
    start = False
    end   = False
    limit = {}
    ret = []
    for line in out.stdout.readlines():
        if "-- Asymptotic --" in line:
            start = True
            continue
        if not start:
            continue
        if line == "\n":
            break
        #print line
        for v in [":","%", "\n", "r <"]:
            line = line.replace(v,"")
        ret.append(line)
        limit_sig, limit_val = line.rsplit()[1:]
        if "limit" in limit_sig.lower(): # this should be the observed limit
            limit_sig = "-1"
        else:
            limit_sig = "%0.3f"%(float ( limit_sig ) / 100.)
        
        limit[limit_sig]=limit_val
    return limit









#if __name__==False:
if False:

  bkgs=["TTJets", "WJets"]
  sig="T2Deg300_270"
  saveDir     =  "/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/analysis/RunII/cutbased/dmt_regions/"
  pickleDir   =  "/afs/hephy.at/user/n/nrad/CMSSW/CMSSW_7_4_7/src/Workspace/DegenerateStopAnalysis/plotsNavid/analysis/cutbased/pkl/dmt_regions/r1/"
  pickleFiles = glob.glob(pickleDir+"/*.pkl")

  if len(pickleFiles)==0:
    print "############   WARNING    no pickle files found!  #####"
  else:
    print "############ %s ickle files ound: "%len(pickleFiles),
    print pickleFiles

  limitDict={}
  yields={}

  yieldInstPickleFiles = [x for x in pickleFiles if "YieldInstance" in x]
  for pickleFile in yieldInstPickleFiles:
    filename = splitext(basename(pickleFile))[0].replace("YieldInstance_","")
    print "############ making a limit card for %s"%filename
    yields[filename]=pickle.load(open(pickleFile,"rb") )
    bins = yields[filename].cutLegend[0][1:]
    limitDict[filename] = getLimit(yields[filename])

  import ROOT

  nLimits = len(limitDict)
  limitPlot = ROOT.TH1F("limitPlot","limitPlot",nLimits,0,nLimits)
  for i,fname in enumerate(sorted(limitDict),1):
    limit=limitDict[fname][1]['0.500']
    limitPlot.GetXaxis().SetBinLabel(i,fname)
    limitPlot.SetBinContent(i,limit)

  limitPlot.GetYaxis().SetTitle("r")
  limitPlot.SetTitle("Median Expected Limits")
  limitPlot.Draw()
  #ROOT.c1.SaveAs("/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/analysis/RunII/cutbased/dmt_regions/ExpectedLimits.png")
  ROOT.c1.SaveAs(saveDir+"/ExpectedLimits.png")
    















