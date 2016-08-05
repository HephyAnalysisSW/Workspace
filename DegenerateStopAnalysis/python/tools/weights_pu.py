from Workspace.DegenerateStopAnalysis.tools.degTools import Weight
import re




btag_veto_soft_bjet          = '(nBSoftJet == 0 )'
btag_one_soft_bjet           = '(nBSoftJet == 1 )'
btag_one_or_more_soft_bjet   = '(nBSoftJet >= 1 )'
btag_veto_hard_bjet          = '(nBHardJet == 0 )'
btag_one_hard_bjet           = '(nBHardJet == 1 )'
btag_one_or_more_hard_bjet   = '(nBHardJet >= 1 )'
btag_veto_bjet               = '((nBHardJet + nBSoftJet)== 0 )'
btag_one_bjet                = '((nBHardJet + nBSoftJet)== 1 )'
btag_one_or_more_bjet        = '((nBHardJet + nBSoftJet)>= 1 )'
btag_two_or_more_bjet        = '((nBHardJet + nBSoftJet)>= 2 )'


sf_veto_soft_bjet          = 'weightSBTag0_SF' 
sf_one_soft_bjet           = 'weightSBTag1_SF'
sf_one_or_more_soft_bjet   = 'weightSBTag1p_SF'
sf_veto_hard_bjet          = 'weightHBTag0_SF'
sf_one_hard_bjet           = 'weightHBTag1_SF'
sf_one_or_more_hard_bjet   = 'weightHBTag1p_SF'
sf_veto_bjet               = 'weightBTag0_SF'   
sf_one_bjet                = 'weightBTag1_SF'    
sf_one_or_more_bjet        = 'weightBTag1p_SF'  
sf_two_or_more_bjet        = 'weightBTag2p_SF'









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
             #"sigScan": {
             #       "baseWeight": "weight",
             #      },



           }


def_weights = {

            "baseWeight":"puReweight*weight",
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

