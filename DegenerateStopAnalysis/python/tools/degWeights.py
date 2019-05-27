import re
from copy import deepcopy
from Workspace.DegenerateStopAnalysis.tools.btag_sf_map import BTagSFMap

def makeDefaultDict(d, default_dict):
        for key in default_dict:
            d.setdefault(key,deepcopy(default_dict[key]))
            if type( default_dict[key] ) == type({}):
                if not type(d[key]) == type({}):
                    raise Exception("There is inconsistancy between input dict and the default dict for key %s, dict:%s \n def_dict:%s \n"%(key,d, default_dict))
                else:
                    makeDefaultDict(d[key], default_dict[key])
            else:
                pass

class Weight(object):
    """

    """
    def __init__(self, weight_dict={}, def_weights={}):
        self.weight_dict = deepcopy(weight_dict)
        makeDefaultDict(self.weight_dict, def_weights)
    
    def getWeightList(self, weight_dict, cut="", lumi="target_lumi"):
        weight_list=[]
        for weight_key in weight_dict:
            #print weight_key
            new_weight = ""
            if weight_key == "cuts":
                found_a_match = False
                for cut_category in weight_dict['cuts']:
                    cut_weight , cut_finder_funct = weight_dict['cuts'][cut_category]
                    #print "looking for a match for", cut_category
                    #if cut_category in cut:
                    #    weight_list.append(cut_weight)
                    if True:
                        #### Should be careful of the weight_dict['cuts'] ...regex expresions confusing!
                        #print cut_category
                        if cut_finder_funct( cut ):
                            print "found a match to the cut string!", cut_category
                            weight_list.append(  cut_weight )
                            #assert not found_a_match, "WARNING! Multiple matches to the cutstring... using all matches! (could be dangerous!)"            
                            if found_a_match : print  "WARNING! Multiple matches to the cutstring... using all matches! (could be dangerous!)"
                            found_a_match = True
            elif weight_key == "lumis":
                weight_list.append(  "%s/%s"%(weight_dict['lumis'][lumi], weight_dict['lumis']["lumi_norm"]) )
            else:
                weight_list.append(  weight_dict[weight_key] )
            #if new_weight:
            #    weight_list.append(new_weight)
        return weight_list

    def combine(self, weight_dict=None, cut="default", lumi="target_lumi"):
        weights = self.weight_dict
        #if not weight_dict:
        #    weight_dict = self.weight_dict
        if weight_dict:
            weights.update(weight_dict)
        self.weight_list = self.getWeightList(weights, cut, lumi)
        return joinWeightList(self.weight_list)

def decide_weight2( sample, weight=None, cut="default" , lumi="target_lumi"):
    #print "Deciding weight:", sample.name, lumi, cut
    if sample.isData:
        weight_str = "(1)"
        return weight_str
    if not weight:
        weight = sample.weights

    #if isinstance(weight,Weight):
    if hasattr(weight,"combine"):
        weight_str = weight.combine(cut=cut, lumi=lumi)
    else:
        if "weight" in weight.lower():
            if sample.has_key("weight"):
                weight_str = sample['weight']
            if weight.endswith("_weight"):
                if sample.has_key(weight):
                    weight_str = sample[weight]
                    #print sample, weight_str, samples[sample]
        else:
            weight_str=weight
    return weight_str

def getSampleTriggersFilters(sample, cutString='', weightString=''):
    triggers = getattr(sample, 'triggers','')
    filters = getattr(sample, 'filters','')
    cuts = getattr(sample, 'cut','')
    weight = getattr(sample, 'weight','')

    weightList = [weightString] if weightString else []
    if weight and weight.replace("(","").replace(")","") != "weight":
        weightList.append(weight)
    ret_weights = "*".join(["(%s)"%w for w in weightList])

    cutList = []
    for cutItem in [cutString, triggers, filters, cuts] :
        if cutItem:
            cutList.append(cutItem)
    ret_cuts = "&&".join(["(%s)"%c for c in cutList])
    return ret_cuts, ret_weights


def decide_cut( sample, cut, plot=None, nMinus1=None):
    cuts = []

    if hasattr(cut, "nMinus1"):
        if nMinus1:
            main_cut_str = cut.nMinus1(nMinus1)
        else:
            main_cut_str = cut.combined
    else:
        main_cut_str = cut
    cuts.append(main_cut_str)
    if getattr(sample, "cut", None):
        cuts.append(   sample.cut  )
    if plot and getattr(plot, "cut", None):
        cuts.append(   plot.cut   )
    warn=False
    if getattr(sample,"triggers", None):
        cuts.append( "(%s)"%sample['triggers'] )
        #warn = True
    if getattr(sample,"filters" , None):
        cuts.append( "(%s)"%sample['filters']   )
        #warn = True
    if warn:
        print "-----"*10 , sample.name
        print "-----"*20
        print "Applying Triggers: %s"%sample['triggers']
        print "Applying Filters: %s"%sample['filters']
        print "-----"*20
        print "-----"*20
    cut_str =  " && ".join(["( %s )"% c for c in cuts])

    sf_list = ["SF","SF_b_Down", "SF_b_Up", "SF_l_Down", "SF_l_Up" ]

    modified = False
    new_cut = cut_str[:]
    for sfOpt in sf_list:
        btag_sf_map = BTagSFMap(sfOpt)
        btag_to_sf  = btag_sf_map.btag_to_sf
        sf_to_btag  = btag_sf_map.sf_to_btag
        sfs = sf_to_btag.keys()
        #print '----------------------'
        #print cut_str
        #print '----------------------'
        for sf in sfs:
            if sf in new_cut:
                #print ' found sf: %s in cut_str, \n%s'%(sf,new_cut)
                if sample.isData:
                    new_cut = new_cut.replace(sf, sf_to_btag[sf])
                    #print 'replacing sf: %s , with %s'%(sf, sf_to_btag[sf])
                else:
                    new_cut = new_cut.replace(sf, "(1)")
                    #print 'replacing sf: %s , with %s'%(sf, "(1)") 
                modified = True
    if "met_genPt" in new_cut and not sample.isSignal:
        print "-------------------- Detected non-signal with genmet cut!"
        print "BEFORE:", new_cut
        new_cut = new_cut.replace("met_genPt","met_pt").replace("met_genPhi","met_phi")
        print "AFTER:" , new_cut
        print "--------------------"

    return new_cut

def decide_cut_weight( sample, cutInst, weight=None,  lumi="target_lumi" , plot=None, nMinus1=None,  ):
    #print "     ", sample 
    #print "     ", cutInst 
    #print "     ", weight 
    #print "     ", lumi 
    #print "     ", plot
    #print "     ", nMinus1
    cutStr = getattr( cutInst, "combined", cutInst )
    weight_str = decide_weight2(sample, weight, cutStr , lumi)
    cut_str    = decide_cut(sample, cutInst, plot = plot, nMinus1 = nMinus1)
    return cut_str, weight_str

def decide_weight( sample, weight ):
    if sample.isData:
        weight_str = "(1)"
        return weight_str
    if "weight" in weight.lower():
        if sample.has_key("weight"):
            weight_str = sample['weight']
        if weight.endswith("_weight"):
            if sample.has_key(weight):
                weight_str = sample[weight]
                #print sample, weight_str, samples[sample]
    else:
        weight_str=weight
    return weight_str

#def decide_weight( sample, weight, cutInst=None, weightDict = None):
#    """
#    chooses the weight for the sample.
#    if an instance of CutClass is given as cutInst, the weightDict is also required.
#    in this case, the weight is chosen from the weightDict, based the sample, cutInst, and the origianl weight string.
#    otherwise, the weight is chosen based on weight keys in the sample
#
#    """
#
#    if sample.isData:
#        weight_str = "(1)"
#        return weight_str
#    if "weight" in weight.lower():
#        if sample.has_key("weight"):
#            weight_str = sample['weight']
#        if weight.endswith("_weight"):
#            if sample.has_key(weight):
#                weight_str = sample[weight]
#                #print sample, weight_str, samples[sample]
#    else:
#        weight_str=weight
#    if not cutInst:
#        return weight_str
#    elif weightDict:
#        sample_name =  sample['name']
#        if weightDict.has_key(sample_name):
#            if weightDict[sample_name]
#        extra_weight = 
#    else:
#        raise Exception("When an instance of CutClass is given, a weight Dictionary is also required.")
#

def make_match_func(tothis):
   def match_func ( x ):
   ##      should use search instead, and then replace to make things less messy!
   ##      re.search( ".*%s"%(tothis.replace("(","\(").replace(")","\)").replace("*","\*")), x )
   ##
      return re.match( ".*%s"%(tothis.replace("(","\(").replace(")","\)").replace("*","\*")), x )
   return match_func

class Weights():
    def __init__(   self,
                    lepCol="LepAll",
                    lep="lep",
                    btag="sf",
                    jet="",
                    pu="puReweight", 
                    wpt="", 
                    ttpt="", 
                    isr="",
                    teff="",
                    lumis="",
                    lhe  = '',
                ):


        weightDict={}
        weightDict['sigScan']= {}

        lepCol  = lepCol
        lep     = lep 
        lepIndex = "Index{lepCol}_{Lep}".format(lepCol=lepCol, Lep=lep)

        wptOpt = wpt
        if wptOpt:
            if wptOpt=='2wpt':
                wptweight_a_template = "(({wpt}<200)*1.+({wpt}>200&&{wpt}<250)*(2*1.008-1)+({wpt}>250&&{wpt}<350)*(2*1.063-1)+({wpt}>350&&{wpt}<450)*(2*0.992-1)+({wpt}>450&&{wpt}<650)*(2*0.847-1)+({wpt}>650&&{wpt}<800)*(2*0.726-1)+({wpt}>800)*(2*0.649-1))"
                wptweight_p_template = "(({wpt}<200)*1.+({wpt}>200&&{wpt}<250)*(2*1.016-1)+({wpt}>250&&{wpt}<350)*(2*1.028-1)+({wpt}>350&&{wpt}<450)*(2*0.991-1)+({wpt}>450&&{wpt}<650)*(2*0.842-1)+({wpt}>650&&{wpt}<800)*(2*0.749-1)+({wpt}>800)*(2*0.704-1))"
                wptweight_n_template = "(({wpt}<200)*1.+({wpt}>200&&{wpt}<250)*(2*0.997-1)+({wpt}>250&&{wpt}<350)*(2*1.129-1)+({wpt}>350&&{wpt}<450)*(2*1.003-1)+({wpt}>450&&{wpt}<650)*(2*0.870-1)+({wpt}>650&&{wpt}<800)*(2*0.687-1)+({wpt}>800)*(2*0.522-1))"
            else:
                wptweight_a_template = "(({wpt}<200)*1.+({wpt}>200&&{wpt}<250)*1.008+({wpt}>250&&{wpt}<350)*1.063+({wpt}>350&&{wpt}<450)*0.992+({wpt}>450&&{wpt}<650)*0.847+({wpt}>650&&{wpt}<800)*0.726+({wpt}>800)*0.649)"
                wptweight_p_template = "(({wpt}<200)*1.+({wpt}>200&&{wpt}<250)*1.016+({wpt}>250&&{wpt}<350)*1.028+({wpt}>350&&{wpt}<450)*0.991+({wpt}>450&&{wpt}<650)*0.842+({wpt}>650&&{wpt}<800)*0.749+({wpt}>800)*0.704)"
                wptweight_n_template = "(({wpt}<200)*1.+({wpt}>200&&{wpt}<250)*0.997+({wpt}>250&&{wpt}<350)*1.129+({wpt}>350&&{wpt}<450)*1.003+({wpt}>450&&{wpt}<650)*0.870+({wpt}>650&&{wpt}<800)*0.687+({wpt}>800)*0.522)"

            wpt = "(sqrt(({lepCol}_pt[max(0,{lepIndex}[0])]*cos({lepCol}_phi[max(0,{lepIndex}[0])]) + met_pt*cos(met_phi) ) **2 + ( {lepCol}_pt[max(0,{lepIndex}[0])]*sin({lepCol}_phi[max(0,{lepIndex}[0])])+met_pt*sin(met_phi) )^2 ))".format(lepCol = lepCol , lepIndex = lepIndex, Lep=lep)
            wptweight_a = wptweight_a_template.format(wpt=wpt)
            wptweight_n = wptweight_n_template.format(wpt=wpt)
            wptweight_p = wptweight_p_template.format(wpt=wpt)
            weightDict.update({
                     "w": {
                            "cuts":{ 
                                        #"neg_mu":      (wptweight_n  , lambda x: re.match( "n{lepCol}_{lep}==1".format(lepCol=lepCol, lep=lep), x ) and re.match( ".*{lepCol}_pdgId\[{lepIndex}\[0\]\]==-13.*".format(lepCol=lepCol, lepIndex=lepIndex) , x )  ),   ## cut_finder tries to match to the cutstring
                                        #"pos_mu":      (wptweight_p  , lambda x: re.match( "n{lepCol}_{lep}==1".format(lepCol=lepCol, lep=lep), x ) and re.match( ".*{lepCol}_pdgId\[{lepIndex}\[0\]\]==13.*".format(lepCol=lepCol, lepIndex=lepIndex) , x  )  ),
                                        #"mixed_mu":    (wptweight_a  , lambda x: re.match( "n{lepCol}_{lep}==1".format(lepCol=lepCol, lep=lep), x ) and not ( re.match( ".*{lepCol}_pdgId\[{lepIndex}\[0\]\]==13.*".format(lepCol=lepCol, lepIndex=lepIndex) , x  ) or re.match( ".*{lepCol}_pdgId\[{lepIndex}\[0\]\]==13.*".format(lepCol=lepCol, lepIndex=lepIndex) , x  ) ) ),
                                        "neg_mu":      (wptweight_n  , lambda x:  ("n{lepCol}_{lep}==1".format(lepCol=lepCol, lep=lep) in x) and ( "{lepCol}_pdgId[{lepIndex}[0]]==13".format(lepCol=lepCol, lepIndex=lepIndex) in x ) )  ,   ## cut_finder tries to match to the cutstring
                                        "pos_mu":      (wptweight_p  , lambda x: ( "n{lepCol}_{lep}==1".format(lepCol=lepCol, lep=lep) in x ) and ( "{lepCol}_pdgId[{lepIndex}[0]]==-13".format(lepCol=lepCol, lepIndex=lepIndex)  in x )),
                                        "mixed_mu":    ( wptweight_a  , lambda x: ( "n{lepCol}_{lep}==1".format(lepCol=lepCol, lep=lep) in x ) and not ( ( "{lepCol}_pdgId[{lepIndex}[0]]==13".format(lepCol=lepCol, lepIndex=lepIndex) in x  ) or ( "{lepCol}_pdgId[{lepIndex}[0]]==13".format(lepCol=lepCol, lepIndex=lepIndex) in x  ) )) ,
                                   }
                           }})
        if ttpt:
            if ttpt=='2ttpt':
                ttptweight = "(1.24)*exp(0.156-0.5*0.00137*({top1pt}+{top2pt}))".format(top1pt="Max$(GenPart_pt*(GenPart_pdgId==6))" , top2pt="Max$(GenPart_pt*(GenPart_pdgId==-6))")
            else:
                ttptweight = "1.24*exp(0.156-0.5*0.00137*({top1pt}+{top2pt}))".format(top1pt="Max$(GenPart_pt*(GenPart_pdgId==6))" , top2pt="Max$(GenPart_pt*(GenPart_pdgId==-6))")
            weightDict['tt'] = {
                            "top_pt": ttptweight
                           }

        isrWeightString = "{normFact} * ( (nIsr==0) + (nIsr==1)*0.882  + (nIsr==2)*0.792  + (nIsr==3)*0.702  + (nIsr==4)*0.648  + (nIsr==5)*0.601  + (nIsr>=6)*0.515 ) "
        isrWeightFunc   = lambda normFact: isrWeightString.format( normFact=normFact )
        isrWeight       = isrWeightFunc("(7.279e-05 *(GenSusyMStop) + 1.108)")
        weightDict['sigScan']['isrReweight'] = isrWeight
        if isr == 'noisr':
            weightDict['sigScan']['isrReweight']= "(1)"

        # def_weights (i.e weights common to all MC samples)
        def_weights = {}
        def_weights['baseWeight']= "weight"

        if teff:
            trigeff = "{p0}*0.5*(1+TMath::Erf(({x}-{p1})/{p2}))".format( p0=0.980, p1=102.5, p2=90.76, x="met")
            def_weights['teff']=trigeff

        if pu:
            def_weights['pu']=pu

        if lumis:
            def_weights['lumis']=lumis

        if not btag.lower() == 'btag':
            btag_sf_map = BTagSFMap(btag)
            btag_to_sf  = btag_sf_map.btag_to_sf
            sf_to_btag  = btag_sf_map.sf_to_btag
            def_weights["cuts"]=dict( [ (sf, (sf, make_match_func(sf))  )  for sf in sf_to_btag.keys()  ])

        if str(lhe):
            #lhe_order ={1: 'Q2central_central',
            #            2: 'Q2up_central',
            #            3: 'Q2down_central',
            #            4: 'Q2central_up',
            #            5: 'Q2up_up',
            #            6: 'Q2down_up',
            #            7: 'Q2central_down',
            #            8: 'Q2up_down',
            #            9: 'Q2down_down'}

            lhe_order = {
                            1: 'Q2central_central'   ,        ## <weight id="1001"> muR=1 muF=1 
                            2: 'Q2central_up'        ,        ## <weight id="1002"> muR=1 muF=2 
                            3: 'Q2central_down'      ,        ## <weight id="1003"> muR=1 muF=0.5 
                            4: 'Q2up_central'        ,   ## <weight id="1004"> muR=2 muF=1 
                            5: 'Q2up_up'             ,   ## <weight id="1005"> muR=2 muF=2 
                            6: 'Q2up_down'           ,   ## <weight id="1006"> muR=2 muF=0.5 
                            7: 'Q2down_central'      ,     ## <weight id="1007"> muR=0.5 muF=1 
                            8: 'Q2down_up'           ,     ## <weight id="1008"> muR=0.5 muF=2 
                            9: 'Q2down_down'         ,     ## <weight id="1009"> muR=0.5 muF=0.5 
                          }

            lhenorms = {
             #'Q2central_central': '(1.000e+00 + ( 6.359e-14 * (GenSusyMStop)) + ( -5.897e-17 * (GenSusyMStop)*(GenSusyMStop) ) )  ',
             'Q2central_central': '(1.0)',
             'Q2central_down': '(9.394e-01 + ( -1.747e-04 * (GenSusyMStop)) + ( 9.838e-08 * (GenSusyMStop)*(GenSusyMStop) ) )  ',
             'Q2central_up': '(1.062e+00 + ( 1.817e-04 * (GenSusyMStop)) + ( -9.773e-08 * (GenSusyMStop)*(GenSusyMStop) ) )  ',
             'Q2down_central': '(8.039e-01 + ( 9.310e-05 * (GenSusyMStop)) + ( -5.135e-08 * (GenSusyMStop)*(GenSusyMStop) ) )  ',
             'Q2down_down': '(7.564e-01 + ( -6.149e-05 * (GenSusyMStop)) + ( 3.450e-08 * (GenSusyMStop)*(GenSusyMStop) ) )  ',
             'Q2down_up': '(8.524e-01 + ( 2.537e-04 * (GenSusyMStop)) + ( -1.366e-07 * (GenSusyMStop)*(GenSusyMStop) ) )  ',
             'Q2up_central': '(1.217e+00 + ( -1.113e-04 * (GenSusyMStop)) + ( 6.175e-08 * (GenSusyMStop)*(GenSusyMStop) ) )  ',
             'Q2up_down': '(1.142e+00 + ( -3.070e-04 * (GenSusyMStop)) + ( 1.733e-07 * (GenSusyMStop)*(GenSusyMStop) ) )  ',
             'Q2up_up': '(1.294e+00 + ( 9.238e-05 * (GenSusyMStop)) + ( -4.909e-08 * (GenSusyMStop)*(GenSusyMStop) ) )  '}


            #lhenorms = {'Q2central_central': '1.000 * exp(0.000e+00 * (GenSusyMStop)  )',
            # 'Q2central_down': '0.312 * exp(9.930e-03 * (GenSusyMStop)  )',
            # 'Q2central_up': '0.283 * exp(9.882e-03 * (GenSusyMStop)  )',
            # 'Q2down_central': '0.305 * exp(9.799e-03 * (GenSusyMStop)  )',
            # 'Q2down_down': '0.257 * exp(9.963e-03 * (GenSusyMStop)  )',
            # 'Q2down_up': '0.234 * exp(9.915e-03 * (GenSusyMStop)  )',
            # 'Q2up_central': '0.255 * exp(9.826e-03 * (GenSusyMStop)  )',
            # 'Q2up_down': '0.373 * exp(9.903e-03 * (GenSusyMStop)  )',
            # 'Q2up_up': '0.338 * exp(9.854e-03 * (GenSusyMStop)  )'}
            
            lhenorm = lhenorms[lhe_order[lhe]]
            #lhenorm = "(1)"

            lheWeight = 'LHEWeights_wgt[%s]'%lhe
            weightDict['sigScan']['LHEWeight'] =   "( (%s)*(%s) )"%(lhenorm, lheWeight )

        self.def_weights = def_weights
        self.weights={}
        for samp in weightDict:
            self.weights[samp]= Weight( weightDict[samp], self.def_weights )

        self.weightDict= weightDict
        self.def_weights = def_weights

        pass

default_weight_params = {
                         'btag'  : 'sf',
                         'lepCol': 'LepGood',
                         'lep'   : 'lep',
                         'lumis' : {
                                    'DataBlind_lumi': 12864.4,
                                    'DataUnblind_lumi': 804.2,
                                    'mc_lumi': 10000.0,
                                    'target_lumi': 13000.0
                                   },
                         'pu'    : 'puReweight',
                         'ttpt'  : '',
                         'isr'   : '',
                         'wpt'   : ''
                         }

weights_    = Weights(**default_weight_params)
weights     = weights_.weights
def_weights = weights_.def_weights


"""
Branching Ratio reweight = 1.022  ,  
Pythia ignores the given SLHA BR for stop decay to leptons (vs taus) and uses equal BR of 10.8%.
The reweighting factor to come to 11.1% is 1.028 for one stop, and 1.022 for two stops.

"""
