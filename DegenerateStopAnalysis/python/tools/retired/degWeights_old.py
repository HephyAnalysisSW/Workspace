from Workspace.DegenerateStopAnalysis.tools.degTools import Weight
from Workspace.DegenerateStopAnalysis.tools.btag_sf_map import BTagSFMap
import re



#import Workspace.DegenerateStopAnalysis.tools.degCuts2 as degCuts



dataBlindLumi="12864.4"
dataUnblindLumi="804.2"
mcLumi="10000"
lepCol = "LepGood"
lep = 'lep'





wpt_weight_a = "(({wpt}<200)*1.+({wpt}>200&&{wpt}<250)*1.008+({wpt}>250&&{wpt}<350)*1.063+({wpt}>350&&{wpt}<450)*0.992+({wpt}>450&&{wpt}<650)*0.847+({wpt}>650&&{wpt}<800)*0.726+({wpt}>800)*0.649)"
wpt_weight_p = "(({wpt}<200)*1.+({wpt}>200&&{wpt}<250)*1.016+({wpt}>250&&{wpt}<350)*1.028+({wpt}>350&&{wpt}<450)*0.991+({wpt}>450&&{wpt}<650)*0.842+({wpt}>650&&{wpt}<800)*0.749+({wpt}>800)*0.704)"
wpt_weight_n = "(({wpt}<200)*1.+({wpt}>200&&{wpt}<250)*0.997+({wpt}>250&&{wpt}<350)*1.129+({wpt}>350&&{wpt}<450)*1.003+({wpt}>450&&{wpt}<650)*0.870+({wpt}>650&&{wpt}<800)*0.687+({wpt}>800)*0.522)"
weights_dict = {

                'sf'        :       {    'var' : 'SF'                      ,   'latex':""            },
                'jt'        :       {    'var' : '_def'                      ,   'latex':""            },
                'lt'        :       {    'var' : '_def'                      ,   'latex':""            },
                'lepCol'    :       {    'var' : lepCol                      ,   'latex':""            },
                'lep'       :       {    'var' : lep                         ,   'latex':""            },
                'lepIndex'  :       {    'var' : 'Index{lepCol}_{lep}{lt}[0]',   'latex':""            },

                "noweight"  :  {'var': "(1)",                                            "latex":""},
                "weight"    :  {'var': "weight",                                            "latex":""},

                'wpt_a' : {'var': wpt_weight_a  ,               "latex":""},
                'wpt_p' : {'var': wpt_weight_p  ,               "latex":""},
                'wpt_n' : {'var': wpt_weight_n  ,               "latex":""},

                'wpt'         : {'var':  "(sqrt(({lepCol}_pt[max(0,{lepIndex}[0])]*cos({lepCol}_phi[max(0,{lepIndex}[0])]) + met_pt*cos(met_phi) ) **2 + ( {lepCol}_pt[max(0,{lepIndex}[0])]*sin({lepCol}_phi[max(0,{lepIndex}[0])])+met_pt*sin(met_phi) )^2 ))",               "latex":""},

                'top1pt'      : {'var': "Max$(GenPart_pt*(GenPart_pdgId==6))",               "latex":""},
                'top2pt'      : {'var': "Max$(GenPart_pt*(GenPart_pdgId==-6))",                "latex":""},
                'ttpt'  : {'var': "1.24*exp(0.156-0.5*0.00137*({top1pt}+{top2pt}))",               "latex":""},
                'trigeff'     : {'var': "{p0}*0.5*(1+TMath::Erf(({x}-{p1})/{p2}))".format( p0=0.980, p1=102.5, p2=90.76, x="met") ,                "latex":""},

                "isr"   : {'var': "{isrNormFact} * ( (nIsr==0) + (nIsr==1)*0.882  + (nIsr==2)*0.792  + (nIsr==3)*0.702  + (nIsr==4)*0.648  + (nIsr==5)*0.601  + (nIsr>=6)*0.515 ) ",               "latex":""},
                "isrNormFact" : {'var': "(7.279e-05 *(GenSusyMStop) + 1.108)",               "latex":""},
                "pu"          : {'var': "puReweight",                                        "latex":""},
                "DataBlind"   : {'var': "(%s/%s)"%(dataBlindLumi,   mcLumi)                 ,"latex":""},
                "DataUnblind" : {'var': "(%s/%s)"%(dataUnblindLumi, mcLumi)                 ,"latex":""},
                "mcLumi"      : {'var': "10000",                                             "latex":""},

                'bTagSF'      : {'var': "{sf}{jt}",                                            "latex":""},
                'BSR1'        : {'var': "(weightSBTag0_{bTagSF})"  ,                         "latex":""},
                'BSR2'        : {'var': "(weightSBTag1p_{bTagSF} * weightHBTag0_{bTagSF})",                                     "latex":""},
                'BCR'         : {'var': "(weightHBTag1p_{bTagSF}-(weightSBTag0_{bTagSF}*weightHBTag1_{bTagSF}))",               "latex":""},
                'BVR'         : {'var': "(weightSBTag0_{bTagSF}  * weightHBTag1_{bTagSF})",                                     "latex":""},

                "BSoft0"      : {'var': '(weightSBTag0_{bTagSF})'    ,               "latex":""},
                "BSoft1"      : {'var': '(weightSBTag1_{bTagSF})'    ,               "latex":""},
                "BSoft2"      : {'var': '(weightSBTag2_{bTagSF})'    ,               "latex":""},
                "BSoft1p"     : {'var': '(weightSBTag1p_{bTagSF})'   ,               "latex":""},
                "BSoft2p"     : {'var': '(weightSBTag2p_{bTagSF})'   ,               "latex":""},
                "BHard0"      : {'var': '(weightHBTag0_{bTagSF})'    ,               "latex":""},
                "BHard1"      : {'var': '(weightHBTag1_{bTagSF})'    ,               "latex":""},
                "BHard2"      : {'var': '(weightHBTag2_{bTagSF})'    ,               "latex":""},
                "BHard1p"     : {'var': '(weightHBTag1p_{bTagSF})'   ,               "latex":""},
                "BHard2p"     : {'var': '(weightHBTag2p_{bTagSF})'   ,               "latex":""},
                "B0"          : {'var': '(weightBTag0_{bTagSF})'     ,               "latex":""},
                "B1"          : {'var': '(weightBTag1_{bTagSF})'     ,               "latex":""},
                "B2"          : {'var': '(weightBTag2_{bTagSF})'     ,               "latex":""},
                "B1p"         : {'var': '(weightBTag1p_{bTagSF})'    ,               "latex":""},
                "B2p"         : {'var': '(weightBTag2p_{bTagSF})'    ,               "latex":""},

                }


  #      
  #      sf_sr1_bjet                =  self.sf_veto_bjet
  #      sf_sr2_bjet                =  "(weightSBTag1p_{sfvar} * weightHBTag0_{sfvar})".format(sfvar=sfvar)
  #      sf_cr1_bjet                =  self.sf_veto_bjet
  #      sf_cr2_bjet                =  "(weightSBTag1p_{sfvar} * weightHBTag0_{sfvar})".format(sfvar=sfvar) #"( (nBSoftJet>=1) && (nBHardJet==0)  )"
  #      sf_crtt1_bjet              =  "(weightSBTag0_{sfvar}  * weightHBTag1_{sfvar})".format(sfvar=sfvar) #"( (nBSoftJet==0) && (nBHardJet==1)  )"
  #      sf_crtt2_bjet              =  "((weightHBTag1p_{sfvar}-(weightSBTag0_{sfvar}*weightHBTag1_{sfvar})))".format(sfvar=sfvar)#"( (nBJet>=2)     && (nBHardJet>=1) )"







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
lheWeightNorms = {
                'Q2central_central': '(1.0)',
                'Q2central_down'   : '(9.394e-01 + ( -1.747e-04 * (GenSusyMStop)) + ( 9.838e-08 * (GenSusyMStop)*(GenSusyMStop) ) )  ',
                'Q2central_up'     : '(1.062e+00 + ( 1.817e-04 * (GenSusyMStop)) + ( -9.773e-08 * (GenSusyMStop)*(GenSusyMStop) ) )  ',
                'Q2down_central'   : '(8.039e-01 + ( 9.310e-05 * (GenSusyMStop)) + ( -5.135e-08 * (GenSusyMStop)*(GenSusyMStop) ) )  ',
                'Q2down_down'      : '(7.564e-01 + ( -6.149e-05 * (GenSusyMStop)) + ( 3.450e-08 * (GenSusyMStop)*(GenSusyMStop) ) )  ',
                'Q2down_up'        : '(8.524e-01 + ( 2.537e-04 * (GenSusyMStop)) + ( -1.366e-07 * (GenSusyMStop)*(GenSusyMStop) ) )  ',
                'Q2up_central'     : '(1.217e+00 + ( -1.113e-04 * (GenSusyMStop)) + ( 6.175e-08 * (GenSusyMStop)*(GenSusyMStop) ) )  ',
                'Q2up_down'        : '(1.142e+00 + ( -3.070e-04 * (GenSusyMStop)) + ( 1.733e-07 * (GenSusyMStop)*(GenSusyMStop) ) )  ',
                'Q2up_up'          : '(1.294e+00 + ( 9.238e-05 * (GenSusyMStop)) + ( -4.909e-08 * (GenSusyMStop)*(GenSusyMStop) ) )  '
               }

for iLHEWeight, lheWeight in lhe_order.items():
        lheWeightString     = "LHEWeights_wgt[%s]"%iLHEWeight
        lheWeightNormalized = "((%s)*(%s))"%(lheWeightNorms[lheWeight],lheWeightString)
        weights_dict[lheWeight]= {'var':lheWeightNormalized , 'latex': '' }



#weights = degCuts.Variables(weights_dict)
#weights  = Weights(weights_dict)

weight_option_funcs = {}


#def wpt_cut_weight_func(sample, cutListNames, weightListNames)
#    if not sample in ["w"]:
#        return sample, cutListNames, weightListNames
#    cut_options= {
#                     "default"  : "wptweight_a",
#                     "negLep"   : "wptweight_n",
#                     "posLep"   : "wptweight_p",
#                  }
#    options = [x for x in cut_options if not x == "default"]
#    new_weights = []
#    for cut in options:
#        if cut in cutListNames:
#            new_weights.append(cut_options[cut])
#    if len(new_weights)>1: 
#        assert False, ["Seems like more than one option was applicable....", cutListNames, cut_options, new_weights]
#    if not new_weights:
#        if cut_options.get("default"):
#            new_weights.append( cut_options["default"])
#    return sample, cutListNames, weightListNames
    

#def makeCutWeightOptFunc( sample_list, cut_options):
#    """
#    Create a function to add weights based on sample name and cut
#    """
#    def cutWeightOptFunc(sample, cutListNames, weightListNames):
#        if "data" in sample.lower() or "dblind" in sample.lower() or "dunblind" in sample.lower():
#            return sample, cutListNames, weightListNames
#        if sample_list and not any([x in sample for x in sample_list]): #sample not in sample_list:
#            print "sample not in sample_list : ", sample_list
#            return sample, cutListNames, weightListNames
#        options = [x for x in cut_options if not x == "default"]
#        new_weights = []
#        for cut in options:
#            if cut in cutListNames:
#                new_weights.append(cut_options[cut])
#        if len(new_weights)>1: 
#            assert False, ["Seems like more than one option was applicable....", cutListNames, cut_options, new_weights]
#        if not new_weights:
#            if cut_options.get("default"):
#                new_weights.append( cut_options["default"])
#        weightListNames.extend(new_weights)
#        for w in new_weights:
#            if w in cutListNames:
#                print w, "poped from cutList!  %s"%cutListNames , "for ", sample
#                cutListNames.pop(cutListNames.index(w))
#        return sample, cutListNames, weightListNames
#    setattr( cutWeightOptFunc, "cut_options", cut_options)
#    setattr( cutWeightOptFunc, "sample_list", sample_list)
#    return cutWeightOptFunc




#wpt_cut_weight_options = {
#                     "default"  : "wptweight_a",
#                     "negLep"   : "wptweight_n",
#                     "posLep"   : "wptweight_p",
#                  }
#wpt_cut_weight_func = makeCutWeightOptFunc(["w"], wpt_cut_weight_options)
#
#ttpt_cut_weight_options = {
#                            "default" : "ttpt"
#                          }
#
#ttpt_cut_weight_func = makeCutWeightOptFunc(["tt", "ttInc"], ttpt_cut_weight_options)


weight_options ={
                    "wpt"   : { "sample_list" : ["WJets"] ,                 "cut_options":{
                                                                                          "default"  : "wpt_a",
                                                                                          "negLep"   : "wpt_n",
                                                                                          "posLep"   : "wpt_p",
                                                                                       }
                              },
                    "ttpt"  : { "sample_list" :['TTJets' ] ,        'cut_options' : { "default": "ttpt" } },

                    "sf"    : { "sample_list" :None,                    'cut_options' : {  
                                                                                           "BCR":"BCR",
                                                                                           "BVR":"BVR",
                                                                                           "BSR1":"BSR1",
                                                                                           "BSR2":"BSR2",
                                                                                         }
                               },
                    "isr"    : { "sample_list" :["T2tt", "T2bw"],                    'cut_options' : {  
                                                                                          "default":"isr"
                                                                                         }
                               }
                }

#cut_weight_funcs = {}
#for weight_option_name, weight_option in weight_options.items():
#    cut_weight_funcs[weight_option_name] = makeCutWeightOptFunc( weight_option['sample_list'], weight_option['cut_options'] )
    


#class Weights(degCuts.Variables):
#    def combine( self, weightList ):
#        #weights_to_combine = [ getattr(self.weights,wname) for wname in weightList]
#        weights_to_combine = [ getattr(self,wname) for wname in weightList]
#        return '*'.join(['(%s)'%w for w in weights_to_combine])
# 


def make_match_func(tothis):
   def match_func ( x ):
   ##      should use search instead, and then replace to make things less messy!
   ##      re.search( ".*%s"%(tothis.replace("(","\(").replace(")","\)").replace("*","\*")), x )
   ##
      return re.match( ".*%s"%(tothis.replace("(","\(").replace(")","\)").replace("*","\*")), x )
   return match_func




class WeightsOld():
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
            print wptOpt
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

        weightDict['sigScan']['isrReweight'] = 123#isrWeight
        if isr == 'noisr':
            weightDict['sigScan']['isrReweight']= "(1)"

        #
        # def_weights (i.e weights common to all MC samples)
        #

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






            lhenorms = {}
             #'Q2central_central': '(1.000e+00 + ( 6.359e-14 * (GenSusyMStop)) + ( -5.897e-17 * (GenSusyMStop)*(GenSusyMStop) ) )  ',

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


#weights_    = Weights(**default_weight_params)
#weights     = weights_.weights
#def_weights = weights_.def_weights


















"""
Branching Ratio reweight = 1.022  ,  
Pythia ignores the given SLHA BR for stop decay to leptons (vs taus) and uses equal BR of 10.8%.
The reweighting factor to come to 11.1% is 1.028 for one stop, and 1.022 for two stops.

"""

