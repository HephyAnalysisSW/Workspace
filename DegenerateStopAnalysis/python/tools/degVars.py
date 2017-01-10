#import Workspace.DegenerateStopAnalysis.tools.degCuts2 as degCuts
import collections



settings = {
                    
                'lepCol':             "LepGood"             ,     
                'lep':                "lep"                 ,        
                'lepTag':             "def"                ,    
                'jetTag':             "def"                ,        
                'btagSF':             "SF"                 ,  
                'dataBlindLumi':       "12864.4"            ,         
                'dataUnblindLumi':     "804.2"              ,       
                'mcLumi':              "10000"              ,

            }        


class VarsCutsWeightsRegions():
    """
    Simple class for easy use of variable, cut and region dictionaries.
    To be used with degCuts

    Variables can be defined in terms of one another for exmaple 
            var1 : {'var':"SOMEVARSTRING" , .... },
            var2 : {'var':"2*{var1}" , .... }
    same with cuts and regions.

    weights_dict
    cuts_dict
    regions
    weight_options


 
    """

    def __init__(
                self, 
                lepCol           =  "LepGood"             ,     
                lep              =  "lep"                 ,        
                lepTag           =  "def"                 ,    
                jetTag           =  "def"                 ,        
                btagSF           =  "SF"                  ,
                dataBlindLumi    =  "12864.4"            ,         
                dataUnblindLumi  =  "804.2"              ,       
                mcLumi           =  "10000"              ,
                ):
        """
        """
        jetTag = "_" + jetTag if jetTag and not jetTag.startswith("_") else jetTag
        lepTag = "_" + lepTag if lepTag and not lepTag.startswith("_") else lepTag

        self.settings = {
                 "lepCol"          : lepCol                   ,     
                 "lep"             : lep                      ,        
                 "lepTag"          : lepTag                   ,    
                 "jetTag"          : jetTag                   ,        
                 "btagSF"          : btagSF                   , 
                 "dataBlindLumi"   : dataBlindLumi            ,         
                 "dataUnblindLumi" : dataUnblindLumi          ,       
                 "mcLumi"          : mcLumi                   ,
            
        }
        self.update()

    def update(self):
        self.evaluateSettings(self.settings)

    def evaluateSettings(self, settings):



        ######################################################################################
        ######################################################################################
        ##                                                                                  ##
        ##                            VARIABLE DEFINITIONS                                  ##
        ##                                                                                  ##
        ######################################################################################
        ######################################################################################


        vars_dict=        {\
                       'jt'        :       {    'var' : settings['jetTag']                      ,   'latex':""            },
                       'lt'        :       {    'var' : settings['lepTag']                      ,   'latex':""            },
                       'lepCol'    :       {    'var' : settings['lepCol']                      ,   'latex':""            },
                       'lep'       :       {    'var' : settings['lep']                         ,   'latex':""            },
                       'mtCut1'    :       {    'var' : "60"                        ,   'latex':''            },
                       'mtCut2'    :       {    'var' : "95"                        ,   'latex':''            },
                       # Jets 
                       'isrIndex'  :       {    'var' : 'IndexJet_basJet{jt}[0]'    ,   'latex':""            },
                       'isrPt'     :       {    'var' : 'Jet_pt[{isrIndex}]'        ,   'latex':""            },
                       'nIsr'      :       {    'var' : 'nJet_isrJet{jt}'           ,   'latex':""            },
                       'nHardIsr'  :       {    'var' : 'nJet_isrHJet{jt}'          ,   'latex':""            },
                       'nSoftJet'  :       {    'var' : 'nJet_softJet{jt}'          ,   'latex':""            },
                       'nHardJet'  :       {    'var' : 'nJet_HardJet{jt}'          ,   'latex':""            },
                       'nJet'      :       {    'var' : 'nJet_basJet{jt}'           ,   'latex':""            },
                       'nVetoJet'  :       {    'var' : 'nJet_vetoJet{jt}'          ,   'latex':""           },
                       'dPhi'      :       {    'var' : 'dPhi_j1j2_vetoJet{jt}'     ,   'latex':""             },
                       #'dPhi'     :       {    'var' : 'vetoJet_dPhi_j1j2'        ,   'latex':""             },
                       #'nIsr'     :       {    'var' : 'nIsrJet'                   ,   'latex':""            },
                       'ht'        :       {    'var' : 'ht_basJet{jt}'             ,   'latex':""            },
                       'CT1'       :       {    'var' : 'min(met,{ht}-100)'         ,   'latex':""            },
                       'CT2'       :       {    'var' : 'min(met,{isrPt}-25)'       ,   'latex':""            },
                       'nBSoftJet' :       {    'var' : 'nJet_bJetSoft{jt}'         ,   'latex':""            },
                       'nBHardJet' :       {    'var' : 'nJet_bJetHard{jt}'         ,   'latex':""            },
                       'nBJet'     :       {    'var' : 'nJet_bJet{jt}'             ,   'latex':""            },
                        # leptons:
                       'nLep'      :       {    'var' : 'n{lepCol}_{lep}{lt}'       ,   'latex':""            }, 
                       'lepIndex'  :       {    'var' : 'Index{lepCol}_{lep}{lt}[0]',   'latex':""            },
                       'lepIndex2' :       {    'var' : 'Alt$(Index{lepCol}_{lep}{lt}[1],-999)',   'latex':""            },
                       'lepMT'     :       {    'var' : '{lepCol}_mt[{lepIndex}]'   ,   'latex':""            },
                       'lepPt'     :       {    'var' : '{lepCol}_pt[{lepIndex}]'   ,   'latex':""            },
                       'lepPhi'    :       {    'var' : '{lepCol}_phi[{lepIndex}]'  ,   'latex':""            },
                       'lepEta'    :       {    'var' : '{lepCol}_eta[{lepIndex}]'  ,   'latex':""            },
                       'lepPdgId'  :       {    'var' : '{lepCol}_pdgId[{lepIndex}]',   'latex':""            },
                       # MET 
                       'met'       :       {    'var' : 'met_pt'                    ,   'latex':""            },
                       'met_phi'   :       {    'var' : 'met_phi'                   ,   'latex':""            },
                       ''          :       {    'var' : ''                          ,   'latex':""            },


                       'mvaId'    :       {     'var': 'Sum$((mva_methodId==35) * Iteration$)' , 'latex':''  },

                  }



        ######################################################################################
        ######################################################################################
        ##                                                                                  ##
        ##                                CUT DEFINITIONS                                   ##
        ##                                                                                  ##
        ######################################################################################
        ######################################################################################


        cuts_dict = {
                    # MT
                    'MTa'               : {'cut': '{lepMT}<{mtCut1}'                                           , 'latex':'' },
                    'MTb'               : {'cut': '({lepMT}>{mtCut1}) && ({lepMT}<{mtCut2})'                   , 'latex':'' },
                    'MTc'               : {'cut': '{lepMT}>{mtCut2}'                                           , 'latex':'' },
                    # presel
                    'AntiQCD'           : {'cut': '{dPhi} < 2.5'                                                  , 'latex':'' },
                    '3rdJetVeto'        : {'cut': '{nVetoJet}<=2'                                        , 'latex':'' },
                    'TauVeto'           : {'cut': '(Sum$(TauGood_idMVANewDM && TauGood_pt > 20 )==0)'       , 'latex':'' },
                    '1Lep-2ndLep20Veto' : {'cut': '{nLep}==1 || ( {nLep}==2 && {lepCol}_pt[{lepIndex2}]<20 )' , 'latex':'' },
                    #'1Lep-2ndLep20Veto' : {'cut': '{nLep}==1 || ( {nLep}>=2 && {lepCol}_pt[{lepIndex2}]<20 )' , 'latex':'' },
    
                    # BTag Regions
                    'BSR1'              : {'cut': '({nBSoftJet} == 0) && ({nBHardJet}==0)'                     , 'latex':'' },
                    'BSR2'              : {'cut': '({nBSoftJet} >= 1) && ({nBHardJet}==0)', 'latex':'' },
                    'BVR'               : {'cut': '({nBSoftJet} == 0) && ({nBHardJet}==1)', 'latex':'' },
                    'BCR'               : {'cut': '({nBJet} >= 2) &&  ({nBHardJet}>=1)', 'latex':'' },
                    # SR1
                    'ptL'               : {'cut':'({lepPt}>=3  && {lepPt}<12)'              ,'latex':''},
                    'ptM'               : {'cut':'({lepPt}>=12 && {lepPt}<20)'              ,'latex':''},
                    'ptH'               : {'cut':'({lepPt}>=20 && {lepPt}<30)'              ,'latex':''},
                    'lepPt_lt_30'       : {'cut':'{lepPt}<30'                               ,'latex':''},
                    'lepPt_gt_30'       : {'cut':'{lepPt}>30'                               ,'latex':''},
                    'lepEta1p5'         : {'cut':'abs({lepEta})<1.5'                        ,'latex':''},
                    # SR2
                    'ISR100'            : {'cut' : '{nIsr}>0'                 ,'latex':''},
                    'ISR325'            : {'cut' : '{nHardIsr}>0'                 ,'latex':''},
                    'negLep'            : {'cut' : '(({lepPdgId}==13) || ({lepPdgId}==11))'                ,'latex':''},
                    'posLep'            : {'cut' : '(({lepPdgId}==-13) || ({lepPdgId}==-11))'              ,'latex':''},
                    ''                  : {'cut' :  ''               ,'latex':''},
                    # CR

                    #MVA
                    'bdt_gt_0p48'           : {'cut' : 'mva_response[{mvaId}]>0.48' , 'latex':''},
                    'bdt_lt_0p48'           : {'cut' : 'mva_response[{mvaId}]<0.48' , 'latex':''},
                    'bdt_gt_0p4'           : {'cut' : 'mva_response[{mvaId}]>0.4' , 'latex':''},
                    'bdt_lt_0p4'           : {'cut' : 'mva_response[{mvaId}]<0.4' , 'latex':''},
                    'bdt_gt_0p55'           : {'cut' : 'mva_response[{mvaId}]>0.55' , 'latex':''},
                    'bdt_lt_0p55'           : {'cut' : 'mva_response[{mvaId}]<0.55' , 'latex':''},
                }

        for methtCut in [200,250, 300, 350, 400]:
            cuts_dict['MET%s'%methtCut] =   {'cut'  :   '{met}>%s'%methtCut , 'latex':''}
            cuts_dict['HT%s'%methtCut]  =   {'cut'  :   '{ht}>%s'%methtCut  , 'latex':''}
            cuts_dict['CT%s'%methtCut]  =   {'cut'  :   '{CT1}>%s'%methtCut , 'latex':''}
        for cutVal in [100,110]:
            cuts_dict['isrPt%s'%methtCut]={'cut':'{CT1}>%s'%methtCut, 'latex':''}

        mva_cuts = {



                    }


        ######################################################################################
        ######################################################################################
        ##                                                                                  ##
        ##                            BINS AND REGIONS DEFINITIONS                          ##
        ##                                                                                  ##
        ######################################################################################
        ######################################################################################

        regions = collections.OrderedDict()   ### Order matters because of baseCuts
        
        regions['presel'] = {'baseCut': None     , 'cuts': ['MET200', 'ISR100', 'HT300', 'AntiQCD', '3rdJetVeto', 'TauVeto', '1Lep-2ndLep20Veto']          , 'latex': '' } 
        regions['sr1'   ] = {'baseCut': 'presel' , 'cuts': ['CT300', 'BSR1', 'lepEta1p5', 'lepPt_lt_30']                                                   , 'latex': '' }
        regions['sr1a'  ] = {'baseCut': 'sr1'    , 'cuts': ['negLep', 'MTa']                                                                               , 'latex': '' }
        regions['sr1b'  ] = {'baseCut': 'sr1'    , 'cuts': ['negLep', 'MTb']                                                                               , 'latex': '' }
        regions['sr1c'  ] = {'baseCut': 'sr1'    , 'cuts': ['MTc']                                                                                         , 'latex': '' }
        regions['sr2'   ] = {'baseCut': 'presel' , 'cuts': ['MET300', 'ISR325', 'BSR2' , 'lepPt_lt_30']                                                    , 'latex': '' }
        
        regions['sr1la' ] = {'baseCut': 'sr1a'    , 'cuts': ['ptL']                                                                               , 'latex': '' }
        regions['sr1ma' ] = {'baseCut': 'sr1a'    , 'cuts': ['ptM']                                                                               , 'latex': '' }
        regions['sr1ha' ] = {'baseCut': 'sr1a'    , 'cuts': ['ptH']                                                                               , 'latex': '' }
        regions['sr1lb' ] = {'baseCut': 'sr1b'    , 'cuts': ['ptL']                                                                               , 'latex': '' }
        regions['sr1mb' ] = {'baseCut': 'sr1b'    , 'cuts': ['ptM']                                                                               , 'latex': '' }
        regions['sr1hb' ] = {'baseCut': 'sr1b'    , 'cuts': ['ptH']                                                                               , 'latex': '' }
        regions['sr1lc' ] = {'baseCut': 'sr1c'    , 'cuts': ['ptL']                                                                               , 'latex': '' }
        regions['sr1mc' ] = {'baseCut': 'sr1c'    , 'cuts': ['ptM']                                                                               , 'latex': '' }
        regions['sr1hc' ] = {'baseCut': 'sr1c'    , 'cuts': ['ptH']                                                                               , 'latex': '' }
        regions['sr2l'  ] = {'baseCut': 'sr2'     , 'cuts': ['ptL']                                                                               , 'latex': '' }
        regions['sr2m'  ] = {'baseCut': 'sr2'     , 'cuts': ['ptM']                                                                               , 'latex': '' }
        regions['sr2h'  ] = {'baseCut': 'sr2'     , 'cuts': ['ptH']                                                                               , 'latex': '' }
        
        regions['cr1'   ] = {'baseCut': 'presel'  , 'cuts': ['CT300', 'BSR1', 'lepEta1p5', 'lepPt_gt_30']                                                   , 'latex': '' }
        regions['cr1a'  ] = {'baseCut': 'cr1'     , 'cuts': ['negLep', 'MTa']                                                                               , 'latex': '' }
        regions['cr1b'  ] = {'baseCut': 'cr1'     , 'cuts': ['negLep', 'MTb']                                                                               , 'latex': '' }
        regions['cr1c'  ] = {'baseCut': 'cr1'     , 'cuts': ['MTc']                                                                                         , 'latex': '' }
        regions['cr2'   ] = {'baseCut': 'presel'  , 'cuts': ['MET300', 'ISR325', 'BSR2' , 'lepPt_gt_30']                                                    , 'latex': '' }
        regions['crtt'  ] = {'baseCut': 'presel'  , 'cuts': ['BCR']                                                    , 'latex': '' }

        regions['bdtgt0p48'] = {'baseCut': 'presel'  , 'cuts': ['bdt_gt_0p48']                                                    , 'latex': '' }
        regions['bdtlt0p48'] = {'baseCut': 'presel'  , 'cuts': ['bdt_lt_0p48']                                                    , 'latex': '' }

        
        regions['bins_sum'  ] = {'baseCut': 'presel' , 'regions': [ 'presel', 
                                                                       'sr1a', 'sr1la' , 'sr1ma', 'sr1ha', 
                                                                       'sr1b', 'sr1lb' , 'sr1mb', 'sr1hb', 
                                                                       'sr1c', 'sr1lc' , 'sr1mc', 'sr1hc', 
                                                                       'sr2' , 'sr2l'  , 'sr2m' , 'sr2h' , 
                                                                       'cr1a' , 'cr1b' , 'cr1c', 'cr2' , 'crtt',
                                                                   ]       , 'latex':''}
        regions['bins_cr']     = {'baseCut': 'presel' , 'regions': [ 'presel',  'cr1a' , 'cr1b' , 'cr1c', 'cr2', 'crtt',    ]       , 'latex':''}
        regions['bins_mainsr'] = {'baseCut': 'presel' , 'regions': [ 'presel',  'sr1a'  , 'sr1b' , 'sr1c' , 'sr2'    ]       , 'latex':''}
        regions['bins_srpt']   = {'baseCut': 'presel' , 'regions': [ 'presel', 
                                                                       'sr1la' , 'sr1ma', 'sr1ha', 
                                                                       'sr1lb' , 'sr1mb', 'sr1hb', 
                                                                       'sr1lc' , 'sr1mc', 'sr1hc', 
                                                                       'sr2l'  , 'sr2m' , 'sr2h' , 
                                                                    ]       , 'latex':''}
        
        regions['bdt0p48']    = {'baseCut':'presel'  , 'regions': ['presel', 'bdtgt0p48', 'bdtlt0p48' ] , 'latex':''}



        def_weights = ['weight', 'pu' ]
        options     = ['wpt']




        wpt_weight_a = "(({wpt}<200)*1.+({wpt}>200&&{wpt}<250)*1.008+({wpt}>250&&{wpt}<350)*1.063+({wpt}>350&&{wpt}<450)*0.992+({wpt}>450&&{wpt}<650)*0.847+({wpt}>650&&{wpt}<800)*0.726+({wpt}>800)*0.649)"
        wpt_weight_p = "(({wpt}<200)*1.+({wpt}>200&&{wpt}<250)*1.016+({wpt}>250&&{wpt}<350)*1.028+({wpt}>350&&{wpt}<450)*0.991+({wpt}>450&&{wpt}<650)*0.842+({wpt}>650&&{wpt}<800)*0.749+({wpt}>800)*0.704)"
        wpt_weight_n = "(({wpt}<200)*1.+({wpt}>200&&{wpt}<250)*0.997+({wpt}>250&&{wpt}<350)*1.129+({wpt}>350&&{wpt}<450)*1.003+({wpt}>450&&{wpt}<650)*0.870+({wpt}>650&&{wpt}<800)*0.687+({wpt}>800)*0.522)"



        ######################################################################################
        ######################################################################################
        ##                                                                                  ##
        ##                                  WEIGHT DEFINITIONS                              ##
        ##                                                                                  ##
        ######################################################################################
        ######################################################################################


        weights_dict = {
    
                    'sf'        :       {    'var' : settings['btagSF']                      ,   'latex':""            },
                    'jt'        :       {    'var' : settings['jetTag']                      ,   'latex':""            },
                    'lt'        :       {    'var' : settings['lepTag']                      ,   'latex':""            },
                    'lepCol'    :       {    'var' : settings['lepCol']                      ,   'latex':""            },
                    'lep'       :       {    'var' : settings['lep']                         ,   'latex':""            },
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
                    "pu_up"       : {'var': "puReweight_up",                                        "latex":""},
                    "pu_down"     : {'var': "puReweight_down",                                        "latex":""},
                    "DataBlind"   : {'var': "(%s/%s)"%(settings['dataBlindLumi'],   settings['mcLumi'])                 ,"latex":""},
                    "DataUnblind" : {'var': "(%s/%s)"%(settings['dataUnblindLumi'], settings['mcLumi'])                 ,"latex":""},
                    "DataICHEP"   : {'var': "(%s/%s)"%(12864.4, settings['mcLumi'])                 ,"latex":""},
                    "mcLumi"      : {'var': settings['mcLumi'],                                             "latex":""},
    
                    'bTagSF'      : {'var': "{sf}{jt}",                                            "latex":""},
                    'BSR1'        : {'var': "(weightBTag0_{bTagSF})"  ,                         "latex":""},
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


        ######################################################################################
        ######################################################################################
        ##                                                                                  ##
        ##                                 WEIGHT OPTIONS  (USE WITH CARE)                  ##
        ##                                                                                  ##
        ######################################################################################
        ######################################################################################


        weight_options ={
                            "wpt"   : { "sample_list" : ["WJets"] ,                 "cut_options":{
                                                                                                  "default"  : "wpt_a",
                                                                                                  "negLep"   : "wpt_n",
                                                                                                  "posLep"   : "wpt_p",
                                                                                               }
                                      },
                            "ttpt"  : { "sample_list" :['TTJets' ] ,                'cut_options' : { "default": "ttpt" } },
                            "sf"    : { "sample_list" :None,                        'cut_options' : {  
                                                                                                   "BCR":"BCR",
                                                                                                   "BVR":"BVR",
                                                                                                   "BSR1":"BSR1",
                                                                                                   "BSR2":"BSR2",
                                                                                                 }
                                       },
                            "isr"    : { "sample_list" :["T2tt", "T2bw"],            'cut_options' : {  
                                                                                                  "default":"isr"
                                                                                                 }
                                       },
                        }
        
        self.weights_dict   =   weights_dict
        self.vars_dict      =   vars_dict
        self.cuts_dict      =   cuts_dict
        self.regions        =   regions
        self.weight_options =   weight_options



