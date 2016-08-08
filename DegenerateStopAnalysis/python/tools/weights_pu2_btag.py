import re
from Workspace.DegenerateStopAnalysis.tools.degTools import Weight
from Workspace.DegenerateStopAnalysis.tools.btag_sf_map import BTagSFMap


btag_sf_map = BTagSFMap('sf')
btag_to_sf  = btag_sf_map.btag_to_sf
sf_to_btag  = btag_sf_map.sf_to_btag


def make_match_func(tothis):
   def match_func ( x ):
   ##      should use search instead, and then replace to make things less messy!
   ##      re.search( ".*%s"%(tothis.replace("(","\(").replace(")","\)").replace("*","\*")), x )
   ##
      return re.match( ".*%s"%(tothis.replace("(","\(").replace(")","\)").replace("*","\*")), x )
   return match_func

weightDict={
             "w": {
                    "cuts":{ 
                                #"SR1":      wptweight_n  , 
                                #"SR2":      wptweight_a  ,
                                #"default":  wptweight_a  ,
                           }
                   },
             "tt": {
                    #"top_pt": ttptweight
                   },
             "z": {
                    #"xsec_fix": "( 1 +  (-1+0.15404) * (xsec<1.4546&&xsec>1.4545) + ( (-1+0.42 ) * (xsec<9.44271&&xsec>9.4427) ))"
                    #"top_pt": ttptweight
                   },
              "s10FS":{
                    "gen_filter_eff": "0.2546" ,
                    },
              "s30FS":{
                    "gen_filter_eff": "0.2647" , 
                    },
              "s60FS":{
                    "gen_filter_eff": "0.3520" ,
                    },
              "t2tt30FS":{
                    "gen_filter_eff": "0.2783" ,
                    },
             "sigScan": {
                    "baseWeight": "weight",
                   },



           }


def_weights = {
            "baseWeight":"puReweight*weight",
            "cuts": dict( [ (sf, (sf, make_match_func(sf))  )  for sf in sf_to_btag.keys()  ]) ,

            #"lumis":{      
            #                "target_lumi"      :    2300, 
            #                "mc_lumi"          :    10000, 
            #                "DataBlind_lumi"   :    2245.386 ,
            #                "DataUnblind_lumi" :    139.63,
            #        },

            #"cuts":{
            #            "SR1":"",
            #            "SR2":"",
            #            "presel":"",
            #            "default":"",
            #       },

           }
                        






weights={}

for samp in weightDict:
    weights[samp]= Weight( weightDict[samp], def_weights )
















"""
Branching Ratio reweight = 1.022  ,  
Pythia ignores the given SLHA BR for stop decay to leptons (vs taus) and uses equal BR of 10.8%.
The reweighting factor to come to 11.1% is 1.028 for one stop, and 1.022 for two stops.

"""

