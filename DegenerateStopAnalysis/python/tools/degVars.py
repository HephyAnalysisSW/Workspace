import collections
from Workspace.DegenerateStopAnalysis.samples.baselineSamplesInfo import cutWeightOptions
import itertools 
settings = cutWeightOptions['settings']



sidebands = {
               'sr1_vr' : {
                                    'baseCut'     : ['presel_EVR1', ['EVR1' , 'lepEta1p5'] ] ,
                                    'common_name' : 'EVR1'  ,
                                    'common'      : ['EVR1' , 'lepEta1p5', 'BSR1'],
                                    'sideband_regions': [
                                                    [ 'MTInc' , 'MTa', 'MTb','MTc' ],
                                                    #[ 'ptL', 'ptM','ptH' , 'lepPt_lt_30', 'lepPt_gt_30'],
                                                    [ 'ptVL', 'ptL', 'ptM','ptH' , 'lepPt_lt_30', 'lepPt_gt_30'],
                                                    [ 'ChargeInc', 'posLep', 'negLep' ],
                                                 ],
                                 }
            }
for vr_name, vr_info in sidebands.items():
    vr_info['cutLists'] = [ list(x) for x in itertools.product( *vr_info['sideband_regions'] ) ] 
            #validation_regions_cutlists = [ list(x) for x in itertools.product( *validation_regions ) ] 
    
vr_name = sidebands.keys()[0]
vrs_info               = sidebands[vr_name]
vrs                    = vrs_info['sideband_regions']
vr_common              = vrs_info['common']
vr_common_name         = vrs_info['common_name']





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
                lepCol   =   settings['lepCol'],
                lep      =   settings['lep'],
                lepTag   =   settings['lepTag'],
                jetTag   =   settings['jetTag'],
                btagSF   =   settings['btagSF'],
                bdtcut   =   settings['bdtcut'],
                mvaId    =   settings['mvaId'],
                lumis    =   settings['lumis'],
                ):
        
        jetTag = "_" + jetTag if jetTag and not jetTag.startswith("_") else jetTag
        lepTag = "_" + lepTag if lepTag and not lepTag.startswith("_") else lepTag

        self.settings = {
                 'lepCol'  :  lepCol,     
                 'lep'     :  lep,        
                 'lepTag'  :  lepTag,    
                 'jetTag'  :  jetTag,        
                 'btagSF'  :  btagSF, 
                 'lumis'   :  lumis,
        }

        mva_options = [mvaId, bdtcut] 
        self.isMVASetup  = all( mva_options )
        if not self.isMVASetup and any(mva_options):
            raise Exception("Seems only not all MVA options are given... %s"%mva_options)
        
        if self.isMVASetup:
            self.settings.update({
                 'mvaId'   :  mvaId,
                 'bdtcut'  :  bdtcut,
                 'bdttag'  :  ('%s'%bdtcut).replace(".","p").replace("-","m"),
            })

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



        # https://indico.cern.ch/event/613194/contributions/2472149/attachments/1410488/2157133/17-02-internal-mikulec.pdf
        wpt_reweight_params = {
                                'a0': 1.00,  
                                'a1': 0.98,   
                                'a2': 0.96,   
                                'a3': 0.90,   
                                'a4': 0.84,  
                                'a5': 0.78,  
                                'a6': 0.74,
        }

        trig_eff_params = { 
                            'p0':0.9673,
                            'p1':127.2 ,
                            'p2':76.58 ,
                            'x':"met"  ,
        }

        ##https://indico.cern.ch/event/592621/contributions/2398559/attachments/1383909/2105089/16-12-05_ana_manuelf_isr.pdf
        tt_isr_reweight_params = {
                                    'a0'  :   1     , 
                                    'a1'  :   0.920 , 
                                    'a2'  :   0.821 , 
                                    'a3'  :   0.715 , 
                                    'a4'  :   0.662 , 
                                    'a5'  :   0.561 , 
                                    'a6'  :   0.511 ,
                                 } 

        vars_dict=        {\
                       'jt'        :       {    'var' : settings['jetTag']                      ,   'latex':""            },
                       'lt'        :       {    'var' : settings['lepTag']                      ,   'latex':""            },
                       'lepCol'    :       {    'var' : settings['lepCol']                      ,   'latex':""            },
                       'lep'       :       {    'var' : settings['lep']                         ,   'latex':""            },
                       'mtCut1'    :       {    'var' : "60"                        ,   'latex':''            },
                       'mtCut2'    :       {    'var' : "95"                        ,   'latex':''            },
                       # Jets 
                       'isrIndex'  :       {    'var' : 'IndexJet_basJet{jt}[0]'    ,   'latex':""            },
                       #'isrPt'     :       {    'var' : 'Max$(Jet_pt[{isrIndex}]'        ,   'latex':""            },
                       'isrPt'     :       {    'var' : 'Max$(Jet_pt * (abs(Jet_eta)<2.4  && (Jet_id)) )'        ,   'latex':""            },
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
                       #'lepIndex2' :       {    'var' : 'Alt$(Index{lepCol}_{lep}{lt}[1],-999)',   'latex':""            },
                       'lepIndex2' :       {    'var' : 'Max$(Alt$(Index{lepCol}_{lep}{lt}[1],-999))',   'latex':""            },
                       'lepMT'     :       {    'var' : '{lepCol}_mt[{lepIndex}]'   ,   'latex':""            },
                       'lepPt'     :       {    'var' : '{lepCol}_pt[{lepIndex}]'   ,   'latex':""            },
                       'lepPhi'    :       {    'var' : '{lepCol}_phi[{lepIndex}]'  ,   'latex':""            },
                       'lepEta'    :       {    'var' : '{lepCol}_eta[{lepIndex}]'  ,   'latex':""            },
                       'lepPdgId'  :       {    'var' : '{lepCol}_pdgId[{lepIndex}]',   'latex':""            },
                       # MET 
                       'met'       :       {    'var' : 'met_pt'                    ,   'latex':""            },
                       'met_phi'   :       {    'var' : 'met_phi'                   ,   'latex':""            },
                       'weight'    :       {    'var' : ''                          ,   'latex':""            },
                  }

        if settings.get('mvaId'):
            vars_dict.update( {
                           'bdtcut'     :       {     'var' :  settings['bdtcut']                       , 'latex':""               },
                           'mvaId'      :       {     'var' :  "%s"%settings['mvaId']                       , 'latex':""               },
                           'mvaIdIndex' :       {     'var' : 'Sum$((mva_methodId=={mvaId} ) * Iteration$)' , 'latex':''  },
                            } )

        ######################################################################################
        ######################################################################################
        ##                                                                                  ##
        ##                                CUT DEFINITIONS                                   ##
        ##                                                                                  ##
        ######################################################################################
        ######################################################################################

        cuts_dict = {
                    # MT
                    'MTInc'             : {'cut': '(1)'                                           , 'latex':'' },
                    'MTa'               : {'cut': '{lepMT}<{mtCut1}'                                           , 'latex':'' },
                    'MTb'               : {'cut': '({lepMT}>{mtCut1}) && ({lepMT}<{mtCut2})'                   , 'latex':'' },
                    'MTc'               : {'cut': '{lepMT}>{mtCut2}'                                           , 'latex':'' },
                    # presel
                    'AntiQCD'           : {'cut': '{dPhi} < 2.5'                                                  , 'latex':'' },
                    '3rdJetVeto'        : {'cut': '{nVetoJet}<=2'                                        , 'latex':'' },
                    'TauVeto'           : {'cut': '(Sum$(TauGood_idMVANewDM && TauGood_pt > 20)==0)'       , 'latex':'' },
                    '1Lep-2ndLep20Veto' : {'cut': '{nLep}==1 || ( {nLep}==2 && {lepCol}_pt[{lepIndex2}]<20 )' , 'latex':'' },
                    #'1Lep-2ndLep20Veto' : {'cut': '{nLep}==1 || ( {nLep}>=2 && {lepCol}_pt[{lepIndex2}]<20 )' , 'latex':'' },
    
                    # BTag Regions
                    'BSR1'              : {'cut': '({nBSoftJet} == 0) && ({nBHardJet}==0)'                     , 'latex':'' },
                    'BSR2'              : {'cut': '({nBSoftJet} >= 1) && ({nBHardJet}==0)', 'latex':'' },
                    'BVR'               : {'cut': '({nBSoftJet} == 0) && ({nBHardJet}==1)', 'latex':'' },
                    'BCR'               : {'cut': '({nBJet} >= 2) &&  ({nBHardJet}>=1)', 'latex':'' },
                    # SR1
                    'ptVL'              : {'cut':'({lepPt}>=3.5  && {lepPt}<5)'              ,'latex':''},
                    'ptL'               : {'cut':'({lepPt}>=5  && {lepPt}<12)'              ,'latex':''},
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
                    'ChargeInc'         : {'cut' : '(1)'              ,'latex':''},
                    #''                  : {'cut' :  ''               ,'latex':''},
                    # CR
                    #'twomu'             : {'cut': '(nLepGood+nLepOther >=2 && (abs(LepGood_pdgId[0])==13 && abs(LepGood_pdgId[1])==13 ))' , 'latex':'' },
                    'twomu'             : {'cut': '(nLepGood+nLepOther >=2)' , 'latex':'' },

                    # VR
                    'EVR1'              : {'cut': '({CT1} > 200)&&({CT1} <= 300)' , 'latex':'' },
                    'EVR2'              : {'cut': '({CT2} > 200)&&({CT2} <= 300)' , 'latex':'' },
                }

        if settings.get('mvaId'):
            cuts_dict.update({
                    #MVA
                    'mva_presel_cut'         : {'cut' : 'mva_preselectedEvent[{mvaIdIndex}]' ,'latex':''},
                    'bdt_gt'                 : {'cut' : 'mva_response[{mvaIdIndex}]>{bdtcut}' , 'latex':''},
                    'bdt_lt'                 : {'cut' : 'mva_response[{mvaIdIndex}]<{bdtcut}' , 'latex':''},
                    #'bdt_gt_0p4'            : {'cut' : 'mva_response[{mvaIdIndex}]>0.4'  , 'latex':''},
                    #'bdt_lt_0p4'            : {'cut' : 'mva_response[{mvaIdIndex}]<0.4'  , 'latex':''},
                    #'bdt_gt_0p55'           : {'cut' : 'mva_response[{mvaIdIndex}]>0.55' , 'latex':''},
                    #'bdt_lt_0p55'           : {'cut' : 'mva_response[{mvaIdIndex}]<0.55' , 'latex':''},
                })

        for methtCut in [200,280, 250, 280, 300, 350, 400]:
            cuts_dict['MET%s'%methtCut] =   {'cut'  :   '{met}>%s'%methtCut , 'latex':''}
            cuts_dict['HT%s'%methtCut]  =   {'cut'  :   '{ht}>%s'%methtCut  , 'latex':''}
            cuts_dict['CT%s'%methtCut]  =   {'cut'  :   '{CT1}>%s'%methtCut , 'latex':''}
        for cutVal in [100,110]:
            cuts_dict['isrPt%s'%cutVal]={'cut':'{isrPt}>%s'%cutVal, 'latex':''}




        ######################################################################################
        ######################################################################################
        ##                                                                                  ##
        ##                            BINS AND REGIONS DEFINITIONS                          ##
        ##                                                                                  ##
        ######################################################################################
        ######################################################################################

        regions = collections.OrderedDict()   ### Order matters because of baseCuts
       
        regions['lip_sync'] = {'baseCut': None     , 'cuts': [ 'MET300', 'isrPt100' , 'HT200', 'AntiQCD', 'lepPt_lt_30' ]          , 'latex': '' } 


        #regions['presel_EVR1']  = {'baseCut': None     , 'cuts': sidebands['validation_regions']['baseCut']     , 'latex': '' } 
        #regions['presel_EVR1'] = {'baseCut': None     , 'cuts': ['EVR1' , 'lepEta1p5', 'BSR1']     , 'latex': '' } 

 
        regions['presel_LIP_incLepPt'] = {'baseCut': None     , 'cuts': ['MET300','HT200', 'isrPt110',  'AntiQCD' ]          , 'latex': '' } 
        regions['presel_Cristovao']    = {'baseCut': None     , 'cuts': ['MET280','HT200', 'isrPt110',  'AntiQCD'  ,'1Lep-2ndLep20Veto'   ]          , 'latex': '' } 
        regions['presel_LIP']           = {'baseCut': None     , 'cuts': ['MET300','HT200', 'isrPt110',  'AntiQCD'  , '3rdJetVeto' ,'1Lep-2ndLep20Veto',  'lepPt_lt_30' ]          , 'latex': '' } 

        regions['presel_train_LIP']  = {'baseCut': None     , 'cuts': ['MET280','HT200', 'isrPt110',  'AntiQCD'   ,'1Lep-2ndLep20Veto',  'lepPt_lt_30' ]          , 'latex': '' } 
        regions['presel_app_LIP']    = {'baseCut': None     , 'cuts': ['MET300','HT200', 'isrPt110',  'AntiQCD'   ,'1Lep-2ndLep20Veto',  'lepPt_lt_30' ]          , 'latex': '' } 

        regions['presel_twomu'] = {'baseCut': None     , 'cuts': ['MET200','HT200',  'twomu' ]          , 'latex': '' } 
        regions['presel'] = {'baseCut': None     , 'cuts': ['MET200', 'ISR100', 'HT300', 'AntiQCD', '3rdJetVeto', 'TauVeto', '1Lep-2ndLep20Veto']          , 'latex': '' } 
        regions['sr1'   ] = {'baseCut': 'presel' , 'cuts': ['CT300', 'BSR1', 'lepEta1p5', 'lepPt_lt_30']                                                   , 'latex': '' }
        regions['sr1a'  ] = {'baseCut': 'sr1'    , 'cuts': ['negLep', 'MTa']                                                                               , 'latex': '' }
        regions['sr1b'  ] = {'baseCut': 'sr1'    , 'cuts': ['negLep', 'MTb']                                                                               , 'latex': '' }
        regions['sr1c'  ] = {'baseCut': 'sr1'    , 'cuts': ['MTc']                                                                                         , 'latex': '' }
        regions['sr2'   ] = {'baseCut': 'presel' , 'cuts': ['MET300', 'ISR325', 'BSR2' , 'lepPt_lt_30']                                                    , 'latex': '' }
        
        regions['sr1vla' ] = {'baseCut': 'sr1a'    , 'cuts': ['ptVL']                                                                               , 'latex': '' }
        regions['sr1la' ] = {'baseCut': 'sr1a'    , 'cuts': ['ptL']                                                                               , 'latex': '' }
        regions['sr1ma' ] = {'baseCut': 'sr1a'    , 'cuts': ['ptM']                                                                               , 'latex': '' }
        regions['sr1ha' ] = {'baseCut': 'sr1a'    , 'cuts': ['ptH']                                                                               , 'latex': '' }
        regions['sr1vlb' ] = {'baseCut': 'sr1b'    , 'cuts': ['ptVL']                                                                               , 'latex': '' }
        regions['sr1lb' ] = {'baseCut': 'sr1b'    , 'cuts': ['ptL']                                                                               , 'latex': '' }
        regions['sr1mb' ] = {'baseCut': 'sr1b'    , 'cuts': ['ptM']                                                                               , 'latex': '' }
        regions['sr1hb' ] = {'baseCut': 'sr1b'    , 'cuts': ['ptH']                                                                               , 'latex': '' }
        regions['sr1vlc' ] = {'baseCut': 'sr1c'    , 'cuts': ['ptVL']                                                                               , 'latex': '' }
        regions['sr1lc' ] = {'baseCut': 'sr1c'    , 'cuts': ['ptL']                                                                               , 'latex': '' }
        regions['sr1mc' ] = {'baseCut': 'sr1c'    , 'cuts': ['ptM']                                                                               , 'latex': '' }
        regions['sr1hc' ] = {'baseCut': 'sr1c'    , 'cuts': ['ptH']                                                                               , 'latex': '' }
        regions['sr2vl'  ] = {'baseCut': 'sr2'     , 'cuts': ['ptVL']                                                                               , 'latex': '' }
        regions['sr2l'  ] = {'baseCut': 'sr2'     , 'cuts': ['ptL']                                                                               , 'latex': '' }
        regions['sr2m'  ] = {'baseCut': 'sr2'     , 'cuts': ['ptM']                                                                               , 'latex': '' }
        regions['sr2h'  ] = {'baseCut': 'sr2'     , 'cuts': ['ptH']                                                                               , 'latex': '' }
        
        regions['cr1'   ] = {'baseCut': 'presel'  , 'cuts': ['CT300', 'BSR1', 'lepEta1p5', 'lepPt_gt_30']                                                   , 'latex': '' }
        regions['cr1a'  ] = {'baseCut': 'cr1'     , 'cuts': ['negLep', 'MTa']                                                                               , 'latex': '' }
        regions['cr1b'  ] = {'baseCut': 'cr1'     , 'cuts': ['negLep', 'MTb']                                                                               , 'latex': '' }
        regions['cr1c'  ] = {'baseCut': 'cr1'     , 'cuts': ['MTc']                                                                                         , 'latex': '' }
        regions['cr2'   ] = {'baseCut': 'presel'  , 'cuts': ['MET300', 'ISR325', 'BSR2' , 'lepPt_gt_30']                                                    , 'latex': '' }
        regions['crtt'  ] = {'baseCut': 'presel'  , 'cuts': ['BCR']                                                    , 'latex': '' }


        
        regions['bins_sum_old'  ] = {'baseCut': 'presel' , 'regions': [ 'presel', 
                                                                       'sr1a', 'sr1la' , 'sr1ma', 'sr1ha', 
                                                                       'sr1b', 'sr1lb' , 'sr1mb', 'sr1hb', 
                                                                       'sr1c', 'sr1lc' , 'sr1mc', 'sr1hc', 
                                                                       'sr2' , 'sr2l'  , 'sr2m' , 'sr2h' , 
                                                                       'cr1a' , 'cr1b' , 'cr1c', 'cr2' , 'crtt',
                                                                   ]       , 'latex':''}
        regions['bins_sum'  ] = {'baseCut': 'presel' , 'regions': [ 'presel', 
                                                                       'sr1a',  'sr1vla' ,'sr1la' , 'sr1ma', 'sr1ha', 
                                                                       'sr1b',  'sr1vlb' ,'sr1lb' , 'sr1mb', 'sr1hb', 
                                                                       'sr1c',  'sr1vlc' ,'sr1lc' , 'sr1mc', 'sr1hc', 
                                                                       'sr2' ,  'sr2vl'  ,'sr2l'  , 'sr2m' , 'sr2h' , 
                                                                       'cr1a' , 'cr1b' , 'cr1c', 'cr2' , 'crtt',
                                                                   ]       , 'latex':''}
        regions['bins_cr']     = {'baseCut': 'presel' , 'regions': [ 'presel',  'cr1a' , 'cr1b' , 'cr1c', 'cr2', 'crtt',    ]       , 'latex':''}
        regions['bins_mainsr'] = {'baseCut': 'presel' , 'regions': [ 'presel',  'sr1a'  , 'sr1b' , 'sr1c' , 'sr2'    ]       , 'latex':''}
        regions['bins_srpt_old']   = {'baseCut': 'presel' , 'regions': [ 'presel', 
                                                                       'sr1la' , 'sr1ma', 'sr1ha', 
                                                                       'sr1lb' , 'sr1mb', 'sr1hb', 
                                                                       'sr1lc' , 'sr1mc', 'sr1hc', 
                                                                       'sr2l'  , 'sr2m' , 'sr2h' , 
                                                                    ]       , 'latex':''}
        regions['bins_srpt']   = {'baseCut': 'presel' , 'regions': [ 'presel', 
                                                                      'sr1vla' , 'sr1la' , 'sr1ma', 'sr1ha', 
                                                                      'sr1vlb' , 'sr1lb' , 'sr1mb', 'sr1hb', 
                                                                      'sr1vlc' , 'sr1lc' , 'sr1mc', 'sr1hc', 
                                                                      'sr2vl'  , 'sr2l'  , 'sr2m' , 'sr2h' , 
                                                                    ]       , 'latex':''}
        
        regions['Cristovao']                          = {'baseCut': 'presel_Cristovao'  , 'regions': ['presel_Cristovao'] , 'cuts': ['MET300']                       , 'latex': '' }
        if settings.get('mvaId'):
            regions['srBDT_LIP']                      = {'baseCut': 'presel_LIP'  , 'cuts': ['bdt_gt']                       , 'latex': '' }
            regions['crBDT_LIP']                      = {'baseCut': 'presel_LIP'  , 'cuts': ['bdt_lt']                       , 'latex': '' }
            regions['bdt%s_LIP'%settings['bdttag']]   = {'baseCut': 'presel_LIP'  , 'regions': ['presel_LIP', 'srBDT_LIP', 'crBDT_LIP' ] , 'latex': '' }

            regions['srBDT_app_LIP']                      = {'baseCut': 'presel_app_LIP'  , 'cuts': ['bdt_gt']                       , 'latex': '' }
            regions['crBDT_app_LIP']                      = {'baseCut': 'presel_app_LIP'  , 'cuts': ['bdt_lt']                       , 'latex': '' }
            regions['bdt%s_app_LIP'%settings['bdttag']]   = {'baseCut': 'presel_app_LIP'  , 'regions': ['presel_app_LIP', 'srBDT_app_LIP', 'crBDT_app_LIP' ] , 'latex': '' }

            regions['mva_presel']                     = {'baseCut':  None         , 'cuts': ['mva_presel_cut']               , 'latex': '' } 
            regions['srBDT']                          = {'baseCut': 'mva_presel'  , 'cuts': ['bdt_gt']                       , 'latex': '' }
            regions['crBDT']                          = {'baseCut': 'mva_presel'  , 'cuts': ['bdt_lt']                       , 'latex': '' }
            regions['bdt%s'%settings['bdttag']]       = {'baseCut': 'mva_presel'  , 'regions': ['presel', 'srBDT', 'crBDT' ] , 'latex': '' }


        vr_name = 'sr1_vr'

        for vr_name in sidebands.keys():
            validation_regions_info = sidebands[vr_name]
            validation_regions      = validation_regions_info['sideband_regions'] 
            vr_common              = validation_regions_info['common'] 
            vr_common_name         = validation_regions_info['common_name']
            vr_baseCut             = validation_regions_info['baseCut'] 
            if len(vr_baseCut)==1:
                pass
            elif len(vr_baseCut)==2:
                vr_baseCut , vr_baseCut_cutList =  vr_baseCut
                regions[vr_baseCut]   = {'baseCut': 'presel'  , 'cuts'    : vr_baseCut_cutList                     , 'latex':''}

            #validation_regions_cutlists = [ list(x) for x in itertools.product( *validation_regions ) ] 
            validation_regions_cutlists = validation_regions_info['cutLists'] #[ list(x) for x in itertools.product( *validation_regions ) ] 

            validation_region_names = []
            for cutListNames in validation_regions_cutlists:
                sideband_name = '_'.join([vr_common_name] + cutListNames)
                validation_region_names.append(sideband_name)
                regions[sideband_name] = {'baseCut': None          , 'cuts'    :  vr_common + cutListNames       , 'latex':''}
            regions[vr_name]   = {'baseCut': vr_baseCut   , 'regions' :  validation_region_names , 'latex':''}

        
        #regions['sr1ValidationRegion'] = {'baseCut': 'presel' , 'regions': ["EVR1"] , 'latex':''}



        # VR + BJetVeto + lepEta + [ MT , LepPt, Charge ] 
        # 
        

        regions['EVR1_VL' ]  = {'baseCut': 'presel_EVR1'    , 'cuts': ['ptVL']                                                                               , 'latex': '' }
        regions['VL' ]  = {'baseCut': 'presel'    , 'cuts': ['ptVL']                                                                               , 'latex': '' }

        def makeValidationRegion():
            pass 


        wpt_weight_a = "(({{wpt}}<200)*{a0}+({{wpt}}>200&&{{wpt}}<250)*{a1}+({{wpt}}>250&&{{wpt}}<350)*{a2}+({{wpt}}>350&&{{wpt}}<450)*{a3}+({{wpt}}>450&&{{wpt}}<650)*{a4}+({{wpt}}>650&&{{wpt}}<800)*{a5}+({{wpt}}>800)*{a6})".format(**wpt_reweight_params)

        #isr_reweight = "( {isrNormFact} * ( (nIsr==0)*{a0} + (nIsr==1)*{a1}  + (nIsr==2)*{a2}  + (nIsr==3)*{a3}  + (nIsr==4)*{a4}  + (nIsr==5)*{a5}  + (nIsr>=6)*{a6} )) "
        isr_reweight = "( (nIsr==0)*{a0} + (nIsr==1)*{a1}  + (nIsr==2)*{a2}  + (nIsr==3)*{a3}  + (nIsr==4)*{a4}  + (nIsr==5)*{a5}  + (nIsr>=6)*{a6} ) "


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
                    #'wpt_p' : {'var': wpt_weight_p  ,               "latex":""},
                    #'wpt_n' : {'var': wpt_weight_n  ,               "latex":""},
    
                    #'wpt'         : {'var':  "(sqrt(({lepCol}_pt[max(0,{lepIndex}[0])]*cos({lepCol}_phi[max(0,{lepIndex}[0])]) + met_pt*cos(met_phi) ) **2 + ( {lepCol}_pt[max(0,{lepIndex}[0])]*sin({lepCol}_phi[max(0,{lepIndex}[0])])+met_pt*sin(met_phi) )^2 ))",               "latex":""},
                    'wpt'         : {'var': "{lepCol}_Wpt[{lepIndex}]",                "latex":""},
    
                    'top1pt'      : {'var': "Max$(GenPart_pt*(GenPart_pdgId==6))",               "latex":""},
                    'top2pt'      : {'var': "Max$(GenPart_pt*(GenPart_pdgId==-6))",                "latex":""},
                    'ttpt'  : {'var': "1.24*exp(0.156-0.5*0.00137*({top1pt}+{top2pt}))",               "latex":""},
                    'trigeff'     : {'var': "{p0}*0.5*(1+TMath::Erf(({x}-{p1})/{p2}))".format( **trig_eff_params) ,                "latex":""},
    
                    "isr"   : {'var': "{isrNormFact} * ( (nIsr==0) + (nIsr==1)*0.882  + (nIsr==2)*0.792  + (nIsr==3)*0.702  + (nIsr==4)*0.648  + (nIsr==5)*0.601  + (nIsr>=6)*0.515 ) ",               "latex":""},
                    "isrNormFact" : {'var': "(7.279e-05 *(GenSusyMStop) + 1.108)",               "latex":""},

                    "isr_tt"   : {'var': "({isrNormFact_tt} * (%s))"%isr_reweight.format( **tt_isr_reweight_params) , 'latex':''}, 
                    "isrNormFact_tt" : {'var': "(1.071)",               "latex":""},

                    "pu"          : {'var': "puReweight",                                        "latex":""},
                    "pu_up"       : {'var': "puReweight_up",                                        "latex":""},
                    "pu_down"     : {'var': "puReweight_down",                                        "latex":""},
    
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
    
        lumis = settings['lumis']

        weights_dict.update({
                    #"DataBlind"   : {'var': "(%s/%s)"%(settings['lumis']['DataBlind_lumi'],   settings['lumis']['MC_lumi'])                 ,"latex":""},
                    #"DataUnblind" : {'var': "(%s/%s)"%(settings['lumis']['DataUnblind_lumi'], settings['lumis']['MC_lumi'])                 ,"latex":""},
                    #"DataICHEP"   : {'var': "(%s/%s)"%(12864.4, settings['lumis']['MC_lumi'])                 ,"latex":""},
                    "MC_lumi"      : {'var': settings['lumis']['MC_lumi'],                                             "latex":""},
                    #"target_lumi"  : {'var': settings['lumis']['target_lumi'],                                             "latex":""},
                    })

        for lumi_name, lumi in lumis.items() :
            if lumi_name not in weights_dict:
                weights_dict[lumi_name] = {'var' : "(%s/%s)"%(settings['lumis'][lumi_name],settings['lumis']['MC_lumi'])  , 'latex':'' } 


        lhe_order = {
                        1: 'Q2central_central'   ,     ## <weight id="1001"> muR=1 muF=1 
                        2: 'Q2central_up'        ,     ## <weight id="1002"> muR=1 muF=2 
                        3: 'Q2central_down'      ,     ## <weight id="1003"> muR=1 muF=0.5 
                        4: 'Q2up_central'        ,     ## <weight id="1004"> muR=2 muF=1 
                        5: 'Q2up_up'             ,     ## <weight id="1005"> muR=2 muF=2 
                        6: 'Q2up_down'           ,     ## <weight id="1006"> muR=2 muF=0.5 
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


        weight_options = {
                            "wpt"   : { "sample_list" : ["WJets"] ,                 "cut_options":{
                                                                                                  "default"  : "wpt_a",
                                                                                                  #"negLep"   : "wpt_n",
                                                                                                  #"posLep"   : "wpt_p",
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
                            "isr_tt"    : { "sample_list" :["TTJets", "TT_1l", "TT_2l" ],            'cut_options' : {  
                                                                                                  "default":"isr_tt"
                                                                                                 }
                                       },
                         }
        
        self.weights_dict     =   weights_dict
        self.vars_dict        =   vars_dict
        self.cuts_dict        =   cuts_dict
        self.regions          =   regions
        self.weight_options   =   weight_options
