from Workspace.DegenerateStopAnalysis.navidTools.NavidTools import Weight



isrWeightFunc = lambda norm: '(1.+{norm}*GenPart_mass[stopIndex1]) *(1.*(stops_pt<120.)+0.95*(stops_pt>=120.&&stops_pt<150.)+0.9*(stops_pt>=150.&&stops_pt<250.)+0.8*(stops_pt>=250.))'.format(norm=norm)
isrWeight = isrWeightFunc(9.5e-5)



#isrWeight_8tev = "puWeight*wpts4X*(1.+7.5e-5*Max$(gpM*(gpPdg==1000006)))*(1.*(ptISR<120.)+0.95*(ptISR>=120.&&ptISR<150.)+0.9*(ptISR>=150.&&ptISR<250.)+0.8*(ptISR>=250.))"
isrWeight_8tev = "(1.+7.5e-5*Max$(gpM*(gpPdg==1000006)))*(1.*(ptISR<120.)+0.95*(ptISR>=120.&&ptISR<150.)+0.9*(ptISR>=150.&&ptISR<250.)+0.8*(ptISR>=250.))"


wpt = "sqrt((  lepPt*cos(lepPhi) + met_pt*cos(met_phi) ) **2 + ( lepPt*sin(lepPhi)+met_pt*sin(met_phi) )**2 )"


wptweight_a_template = "(({wpt}<200)*1.+({wpt}>200&&{wpt}<250)*1.008+({wpt}>250&&{wpt}<350)*1.063+({wpt}>350&&{wpt}<450)*0.992+({wpt}>450&&{wpt}<650)*0.847+({wpt}>650&&{wpt}<800)*0.726+({wpt}>800)*0.649)"
wptweight_p_template = "(({wpt}<200)*1.+({wpt}>200&&{wpt}<250)*1.016+({wpt}>250&&{wpt}<350)*1.028+({wpt}>350&&{wpt}<450)*0.991+({wpt}>450&&{wpt}<650)*0.842+({wpt}>650&&{wpt}<800)*0.749+({wpt}>800)*0.704)"
wptweight_n_template = "(({wpt}<200)*1.+({wpt}>200&&{wpt}<250)*0.997+({wpt}>250&&{wpt}<350)*1.129+({wpt}>350&&{wpt}<450)*1.003+({wpt}>450&&{wpt}<650)*0.870+({wpt}>650&&{wpt}<800)*0.687+({wpt}>800)*0.522)"



wptweight_a = wptweight_a_template.format(wpt=wpt)
wptweight_n = wptweight_n_template.format(wpt=wpt)
wptweight_p = wptweight_p_template.format(wpt=wpt)

wpt_8tev = "muWPt[mediumMuonIndex]"
wptweight_a_8tev = wptweight_a_template.format(wpt=wpt_8tev)
wptweight_n_8tev = wptweight_n_template.format(wpt=wpt_8tev)
wptweight_p_8tev = wptweight_p_template.format(wpt=wpt_8tev)


ttptweight = "1.24*exp(0.156-0.5*0.00137*({top1pt}+{top2pt}))".format(top1pt="Max$(GenPart_pt*(GenPart_pdgId==6))" , top2pt="Max$(GenPart_pt*(GenPart_pdgId==-6))")


ttptweight_8tev = "1.24*exp(0.156-0.5*0.00137*(gpPt[6]+gpPt[7]))"

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
              "s10FS":{
                    "gen_filter_eff": 0.2546 ,
                    },
              "s30FS":{
                    "gen_filter_eff": 0.2647 , 
                    },
              "s60FS":{
                    "gen_filter_eff": 0.3520 ,
                    },
              "t2tt30FS":{
                    "gen_filter_eff": 0.2783 ,
                    },
             "sigScan": {
                    "baseWeight": "weight",
                    "isrWeight": isrWeight,
                   },


             "tt8tev": {
                    "baseWeight": "puWeight",
                    "ttpt": ttptweight_8tev,
                    "cuts":{ 
                                #"SR1":      ""  , 
                                #"SR2":      ""  ,
                                #"default":  ""  ,
                                }
                   },
             "w8tev": {
                    "baseWeight": "puWeight",
                    "cuts":{ 
                                #"SR1":      wptweight_n_8tev  , 
                                #"SR2":      wptweight_a_8tev  ,
                                #"default":  wptweight_a_8tev  ,
                                }
                   },

             "sigScan_8tev": {
                    "baseWeight": "puWeight*wpts4X",
                    "isrWeight":  isrWeight_8tev,
                   },


           }


def_weights = {

            "baseWeight":"weight",
            "lumis":{      
                            "target_lumi"      :    2300, 
                            "mc_lumi"          :    10000, 
                            "DataBlind_lumi"   :    2245.386 ,
                            "DataUnblind_lumi" :    139.63,
                    },

            "cuts":{
                        "SR1":"",
                        "SR2":"",
                        "presel":"",
                        "default":"",
                   },

           }
                        






weights={}

for samp in weightDict:
    weights[samp]= Weight( weightDict[samp], def_weights )
















"""
Branching Ratio reweight = 1.022  ,  
Pythia ignores the given SLHA BR for stop decay to leptons (vs taus) and uses equal BR of 10.8%.
The reweighting factor to come to 11.1% is 1.028 for one stop, and 1.022 for two stops.

"""

