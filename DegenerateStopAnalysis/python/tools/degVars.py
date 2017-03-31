import collections
from Workspace.DegenerateStopAnalysis.samples.baselineSamplesInfo import cutWeightOptions, triggers, degTools
import itertools
from copy import deepcopy
settings = cutWeightOptions['settings']

#from Workspace.DegenerateStopAnalysis.samples.baselineSamplesInfo import lumis, triggers, sample_names 



sidebands = {
               'sr1_vr' : {
                                    'baseCut'     : ['presel_EVR1', ['EVR1' , 'lepEta1p5'] ] ,
                                    #'baseCut'     : ['presel_EVR1', ['EVR1'  ] ] ,
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

#vr_name = sidebands.keys()[0]
#vrs_info               = sidebands[vr_name]
#vrs                    = vrs_info['sideband_regions']
#vr_common              = vrs_info['common']
#vr_common_name         = vrs_info['common_name']


def getAllRegionsWithCut( regions, cutName):
    regionsWithCut = []
    foundAll = False
    
    while not foundAll:
        foundThese = []
        for region_name, region_info in regions.iteritems():
            if region_name in regionsWithCut:
                continue
            if cutName in region_info.get('cuts',[]):
                foundThese.append(region_name)
                continue
            if cutName in region_info.get('regions',[]):
                foundThese.append(region_name)
                continue
            if region_info.get('baseCut') and degTools.anyIn( regionsWithCut, region_info['baseCut']):
                foundThese.append(region_name)
                continue
        if foundThese:
            regionsWithCut.extend(foundThese)
        else:
            foundAll = True 
    return regionsWithCut


class VarsCutsWeightsRegions():
    """
    Simple class for easy use of variable, cut and region dictionaries.
    To be used with degCuts

    Variables can be defined in terms of one another for example 
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
        #wpt_reweight_params = {
        #                        'a0': 1.00,  
        #                        'a1': 0.98,   
        #                        'a2': 0.96,   
        #                        'a3': 0.90,   
        #                        'a4': 0.84,  
        #                        'a5': 0.78,  
        #                        'a6': 0.74,
        #}
        #wpt_weight_a = "(({{wpt}}<200)*{a0}+({{wpt}}>200&&{{wpt}}<250)*{a1}+({{wpt}}>250&&{{wpt}}<350)*{a2}+({{wpt}}>350&&{{wpt}}<450)*{a3}+({{wpt}}>450&&{{wpt}}<650)*{a4}+({{wpt}}>650&&{{wpt}}<800)*{a5}+({{wpt}}>800)*{a6})".format(**wpt_reweight_params)

        # https://indico.cern.ch/event/616816/contributions/2489809/attachments/1418579/2174166/17-02-22_ana_isr_ewk.pdf
        wpt_reweight_params = {
                          'normFact': 0.94 ,
                                'a0': 1.00 ,  
                                'a1': 1.052,   
                                'a2': 1.179,   
                                'a3': 1.150,   
                                'a4': 1.057,  
                                'a5': 1.000,  
                                'a6': 0.912,
                                'a7': 0.783,
        }
        wpt_weight_a = "{normFact}*(({{wpt}}<50)*{a0}+({{wpt}}>50&&{{wpt}}<100)*{a1}+({{wpt}}>100&&{{wpt}}<150)*{a2}+({{wpt}}>150&&{{wpt}}<200)*{a3}+({{wpt}}>200&&{{wpt}}<300)*{a4}+({{wpt}}>300&&{{wpt}}<400)*{a5}+({{wpt}}>400&&{{wpt}}<600)*{a6}+({{wpt}}>600)*{a7})".format(**wpt_reweight_params)

        #trig_eff_params = { 
        #                    'p0':0.9673,
        #                    'p1':127.2 ,
        #                    'p2':76.58 ,
        #                    'x':"met"  ,
        #}

        
        # https://www.dropbox.com/s/nqj5qfpikvws1rv/17-03-internal2-mikulec.pdf?dl=0
        trig_eff_params = { 
                            'p0' : 0.9899 ,
                            'p1' : 109.8  ,
                            'p2' : 94.26  ,
                            'x'  : "met"  ,
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
        looseWP  = "_loose"
        if settings['lepTag'] == "_lowpt":
            looseWP += "_lowpt"
        #isLnTSel = "loose" in settings['lepTag']
        #if isLnTSel:
        #    LnTCuts = ['notTight' , 'prompt_LnT']
        #    tightWP = settings['lepTag'].replace("_loose","")
        #else:
        #    LnTCuts = []
        tightWP = settings['lepTag']

        LnTCuts    = [  'notTight' ]
        promptCuts    = [  'prompt'    ]
        promptLnTCuts = [  'prompt_LnT'    ]

        vars_dict=        {\
                       'jt'        :       {    'var' : settings['jetTag']                      ,   'latex':""            },
                       #'lt'        :       {    'var' : settings['lepTag']                      ,   'latex':""            },
                       'lt'        :       {    'var' : settings['lepTag']                      ,   'latex':""            },
                       'looseWP'   :       {    'var' : looseWP                                 ,   'latex':""            },
                       'tightWP'   :       {    'var' : tightWP                                 ,   'latex':""            },
                       'lepCol'    :       {    'var' : settings['lepCol']                      ,   'latex':""            },
                       'lep'       :       {    'var' : settings['lep']                         ,   'latex':""            },
                       'mtCut1'    :       {    'var' : "60"                        ,   'latex':''            },
                       'mtCut2'    :       {    'var' : "95"                        ,   'latex':''            },
                       # Jets 
                       'isrIndex'  :       {    'var' : 'IndexJet_basJet{jt}[0]'    ,   'latex':""            },
                       #'isrPt'     :       {    'var' : 'Max$(Jet_pt[{isrIndex}])'        ,   'latex':""            },
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
                       'nLep_lep'   :       {    'var' : 'n{lepCol}_lep{lt}'       ,   'latex':""            }, 

                       'lepIndex1'  :       {    'var' : 'Index{lepCol}_{lep}{lt}[0]',   'latex':""            },
                       'lepIndex_lep':     {    'var' : 'Index{lepCol}_lep{lt}',     'latex':""            },
                       'lepIndex'  :        {    'var' : 'Index{lepCol}_{lep}{lt}',   'latex':""            },
                       'lepIndex_lep1':     {    'var' : '{lepIndex_lep}[0]',     'latex':""            },

                       #'lepIndex2' :       {    'var' : 'Alt$(Index{lepCol}_{lep}{lt}[1],-999)',   'latex':""            },
                       'lepIndex2' :       {    'var' : 'Max$(Alt$(Index{lepCol}_{lep}{lt}[1],-999))',   'latex':""            },
                       '_lepIndex2' :       {    'var' : 'Max$(Alt$(Index{lepCol}_lep{lt}[1],-999))',   'latex':""            },

                    'isFakeFromTau1':       {    'var' : '{lepCol}_isFakeFromTau[{lepIndex1}]'  , 'latex':''    },
                       'lepMT'     :       {    'var' : '{lepCol}_mt[{lepIndex1}]'   ,   'latex':""            },
                       'lepPt'     :       {    'var' : '{lepCol}_pt[{lepIndex1}]'   ,   'latex':""            },
                       'lepPhi'    :       {    'var' : '{lepCol}_phi[{lepIndex1}]'  ,   'latex':""            },
                       'lepEta'    :       {    'var' : '{lepCol}_eta[{lepIndex1}]'  ,   'latex':""            },
                       'lepPdgId'  :       {    'var' : '{lepCol}_pdgId[{lepIndex1}]',   'latex':""            },
                 'lepPdgId_loose'  :       {    'var' : '{lepCol}_pdgId[{lepIndex_loose1}]',   'latex':""            },
                       'lepCharge'  :      {    'var' : '{lepCol}_charge[{lepIndex1}]',  'latex':""            },

                       # loose leps
                       'lepIndex_loose'  : {    'var' : 'Index{lepCol}_{lep}{looseWP}',   'latex':""            },
                       'lepIndex_loose1' : {    'var' : '{lepIndex_loose}[0]',   'latex':""            },
                       'lepIndex_lep_loose'  : {    'var' : 'Index{lepCol}_lep{looseWP}',   'latex':""            },
                       'lepIndex_lep_loose1' : {    'var' : '{lepIndex_lep_loose}[0]',   'latex':""            },
                       'lepMT_loose'     : {    'var' : '{lepCol}_mt[{lepIndex_loose1}]'   ,   'latex':""            },
                       'nLep_loose'      : {    'var' : 'n{lepCol}_{lep}{looseWP}'       ,   'latex':""            }, 
                       'lepEta_loose'    : {    'var' : '{lepCol}_eta[{lepIndex_loose1}]'  ,   'latex':""            },
                       'lepPt_loose'     : {    'var' : '{lepCol}_pt[{lepIndex_loose1}]'   ,   'latex':""            },
                    'isFakeFromTau_loose1': {    'var' : '{lepCol}_isFakeFromTau[{lepIndex_loose1}]'  , 'latex':''    },

                       # tight leps
                       'lepIndex_tight_lep': {    'var' : 'Index{lepCol}_lep{tightWP}',   'latex':""            },
                       'lepIndex_tight'  : {    'var' : 'Index{lepCol}_{lep}{tightWP}',   'latex':""            },
                       'lepIndex_tight1' : {    'var' : '{lepIndex_tight}[0]',   'latex':""            },
                       'lepIndex_lep_tight'  : {    'var' : 'Index{lepCol}_lep{tightWP}',   'latex':""            },
                       'lepIndex_lep_tight1' : {    'var' : '{lepIndex_lep_tight}[0]',   'latex':""            },
                       'lepMT_tight'     : {    'var' : '{lepCol}_mt[{lepIndex_tight1}]'   ,   'latex':""            },
                       'nLep_tight'      : {    'var' : 'n{lepCol}_{lep}{tightWP}'       ,   'latex':""            }, 
                       'lepEta_tight'    : {    'var' : '{lepCol}_eta[{lepIndex_tight1}]'  ,   'latex':""            },
                       'lepPt_tight'     : {    'var' : '{lepCol}_pt[{lepIndex_tight1}]'   ,   'latex':""            },

                       # MET 
                       'met'       :       {    'var' : 'met'                       ,   'latex':""            },
                       'met_phi'   :       {    'var' : 'met_phi'                   ,   'latex':""            },
                       'weight'    :       {    'var' : ''                          ,   'latex':""            },
                       # Fake rate (measurement region 2)
                       'tagIndex'  :       {    'var' : 'Index{lepCol}_lep_def[0]',     'latex':""            }, # index of leading tight lepton = tag
                       'tagPdgId'  :       {    'var' : '{lepCol}_pdgId[{tagIndex}]',   'latex':""            },
                       'tagCharge'  :      {    'var' : '{lepCol}_charge[{tagIndex}]',  'latex':""            },

                        # Triggs
                        'data_met_trigs'        : {'var': triggers['data_met']                  , 'latex':''},
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

        # fakeTauVeto Cut
        genTauCond = "(abs(GenPart_pdgId) == 15 && (abs(GenPart_motherId) == 24 || abs(GenPart_motherId) == 23 || (GenPart_motherId == -9999 && Iteration$ < 3)))"
        genTauCondFalse = "(Sum$(%s) == 0)"%genTauCond

        deltaR = "(deltaR(GenPart_eta, {lepCol}_eta[{lepIndex1}], GenPart_phi, {lepCol}_phi[{lepIndex1}]))"
        deltaR_template = "(deltaR(GenPart_eta, {{lepCol}}_eta[{idx}], GenPart_phi, {{lepCol}}_phi[{idx}]))"
        dRmin     = "MinIf$(%s,%s)"%(deltaR_template.format(idx="{lepIndex1}"), genTauCond)
        dRmin_LnT = "MinIf$(%s,%s)"%(deltaR_template.format(idx="{lepIndex_loose1}"), genTauCond)
    

        #loose_weird = '((met>200) && (nJet_isrJet_def > 0) && (ht_basJet_def>300) && (dPhi_j1j2_vetoJet_def < 2.5) && (nJet_vetoJet_def <= 2) && ((Sum$(TauGood_idMVANewDM && TauGood_pt > 20 && abs(TauGood_eta) < 2.4)==0)) && (( Sum$( LepGood_pt[IndexLepGood_lep_loose_lowpt[0]]>3.5))&&( Sum$(LepGood_pt[IndexLepGood_lep_loose_lowpt]>20)<2 ))) '
        #tight = '((met>200) && (nJet_isrJet_def > 0) && (ht_basJet_def>300) && (dPhi_j1j2_vetoJet_def < 2.5) && (nJet_vetoJet_def <= 2) && ((Sum$(TauGood_idMVANewDM && TauGood_pt > 20 && abs(TauGood_eta) < 2.4)==0)) && ((Sum$(LepGood_pt[IndexLepGood_lep_lowpt]>3.5))&&(1)&&( Sum$(LepGood_pt[IndexLepGood_lep_lowpt]>20)<2 )))'
        #loose ='((met>200) && (nJet_isrJet_def > 0) && (ht_basJet_def>300) && (dPhi_j1j2_vetoJet_def < 2.5) && (nJet_vetoJet_def <= 2) && ((Sum$(TauGood_idMVANewDM && TauGood_pt > 20 && abs(TauGood_eta) < 2.4)==0)) && (( Sum$( LepGood_pt[IndexLepGood_lep_loose_lowpt ]>3.5))&&( Sum$(LepGood_pt[IndexLepGood_lep_lowpt]>20) <2) && (1)))'
        #notTight = "!Sum$(LepGood_pt[IndexLepGood_lep_lowpt]>3.5)"

        cuts_dict = {
                    # pT
                    'lepPt_gt_3p5'      : {'cut':'{lepPt} > 3.5'                                     ,'latex':''},
                    # MT
                    'MTInc'             : {'cut': '(1)'                                           , 'latex':'' },
                    'MTa'               : {'cut': '{lepMT} < {mtCut1}'                               , 'latex':''},
                    'MTb'               : {'cut': '({lepMT} > {mtCut1}) && ({lepMT} < {mtCut2})'     , 'latex':''},
                    'MTc'               : {'cut': '{lepMT} > {mtCut2}'                               , 'latex':''},
                    'MTab'              : {'cut': '{lepMT} < {mtCut2}'                               , 'latex':''},
                    ## MT LOOSE
                    'MTInc_LnT'             : {'cut': '(1)'                                           , 'latex':'' },
                    'MTa_LnT'               : {'cut': '{lepMT_loose} < {mtCut1}'                               , 'latex':''},
                    'MTb_LnT'               : {'cut': '({lepMT_loose} > {mtCut1}) && ({lepMT_loose} < {mtCut2})'     , 'latex':''},
                    'MTc_LnT'               : {'cut': '{lepMT_loose} > {mtCut2}'                               , 'latex':''},
                    'MTab_LnT'              : {'cut': '{lepMT_loose} < {mtCut2}'                               , 'latex':''},
                    # presel
                    'AntiQCD'           : {'cut': '{dPhi} < 2.5'                                   , 'latex':''},
                    'invAntiQCD'        : {'cut': '({dPhi} > 2.5 || {nVetoJet} <= 1)'              , 'latex':''}, # NOTE: or required for inclusion of monojet events
                    'mc_trigs'          : {'cut': '{data_met_trigs}'                                   , 'latex':''},
                    

                    '3rdJetVeto'        : {'cut': '{nVetoJet} <= 2'                                        , 'latex':'' },
                    'TauVeto'           : {'cut': '(Sum$(TauGood_idMVANewDM && TauGood_pt > 20 && abs(TauGood_eta) < 2.4) == 0)'       , 'latex':'' },
                    #'1Lep-2ndLep20Veto' : {'cut': '({nLep} >= 1 && {lepPt} > 3.5 && (Sum$({lepCol}_pt[{lepIndex_lep}] > 20) <= 1) && ({lepIndex1} == {lepIndex_lep1}))' , 'latex':''},
                    '1Lep'              : {'cut': 'Sum$({lepCol}_pt[{lepIndex}]>3.5)&&({lepIndex1}=={lepIndex_lep1})' , 'latex':''},
                    #'1TightLep'        : {'cut': 'Sum$({lepCol}_pt[{lepIndex}]>3.5)&&({lepIndex1}=={lepIndex_lep1})' , 'latex':''},
                    '1LooseLep'         : {'cut': 'Sum$({lepCol}_pt[{lepIndex_lep_loose}]>3.5)&&({lepIndex_loose1}=={lepIndex_lep_loose1})' , 'latex':''},
                    '2ndLep20Veto'      : {'cut': '(Sum$({lepCol}_pt[{lepIndex_lep}]>20)<2)' , 'latex':''},
                    'notTight'          : {'cut':  "!Sum$({lepCol}_pt[{lepIndex_tight_lep}]>3.5)" , 'latex': '' } ,         
    
                    #'1Lep'              : {'cut': '({nLep} == 1 && ({lepIndex1} == {lepIndex_lep1}))' , 'latex':'' },
    
                    # BTag Regions
                    'BSR1'              : {'cut': '({nBSoftJet} == 0) && ({nBHardJet} == 0)', 'latex':''},
                    'BSR2'              : {'cut': '({nBSoftJet} >= 1) && ({nBHardJet} == 0)', 'latex':''},
                    'BVR'               : {'cut': '({nBSoftJet} == 0) && ({nBHardJet} == 1)', 'latex':''},
                    'BCR'               : {'cut': '({nBJet} >= 2) &&  ({nBHardJet} >= 1)',    'latex':''},
                    # SR1
                    'ptVL'              : {'cut':'({lepPt} >= 3.5  && {lepPt} < 5)'          ,'latex':''},
                    'ptL'               : {'cut':'({lepPt} >= 5  && {lepPt} < 12)'           ,'latex':''},
                    'ptM'               : {'cut':'({lepPt} >= 12 && {lepPt} < 20)'           ,'latex':''},
                    'ptH'               : {'cut':'({lepPt} >= 20 && {lepPt} < 30)'           ,'latex':''},
                    'lepPt_lt_30'       : {'cut':'{lepPt} < 30'                              ,'latex':''},
                    'lepPt_gt_30'       : {'cut':'{lepPt} > 30'                              ,'latex':''},
                    'lepEta1p5'         : {'cut':'abs({lepEta}) < 1.5'                       ,'latex':''},
                    # SR1 LnT
                    'ptVL_LnT'          : {'cut':'({lepPt_loose} >= 3.5  && {lepPt_loose} < 5)'          ,'latex':''},
                    'ptL_LnT'           : {'cut':'({lepPt_loose} >= 5  && {lepPt_loose} < 12)'           ,'latex':''},
                    'ptM_LnT'           : {'cut':'({lepPt_loose} >= 12 && {lepPt_loose} < 20)'           ,'latex':''},
                    'ptH_LnT'           : {'cut':'({lepPt_loose} >= 20 && {lepPt_loose} < 30)'           ,'latex':''},
                    'lepPt_lt_30_LnT'   : {'cut':'{lepPt_loose} < 30'                              ,'latex':''},
                    'lepPt_gt_30_LnT'   : {'cut':'{lepPt_loose} > 30'                              ,'latex':''},
                    'lepEta1p5_LnT'     : {'cut':'abs({lepEta_loose}) < 1.5'                       ,'latex':''},
                    # SR2
                    'ISR100'            : {'cut' : '{nIsr} > 0'                 ,'latex':''},
                    'ISR325'            : {'cut' : '{nHardIsr} > 0'             ,'latex':''},
                    'negLep'            : {'cut' : '({lepPdgId} > 0)'              ,'latex':''},
                    'posLep'            : {'cut' : '({lepPdgId} < 0)'              ,'latex':''},
                    'negLep_LnT'        : {'cut' : '({lepPdgId_loose} > 0)'              ,'latex':''},
                    'posLep_LnT'        : {'cut' : '({lepPdgId_loose} < 0)'              ,'latex':''},
                    'ChargeInc'         : {'cut' : '(1)'              ,'latex':''},
                    # CR
                    #'twomu'             : {'cut': '(nLepGood+nLepOther >=2 && (abs(LepGood_pdgId[0])==13 && abs(LepGood_pdgId[1])==13 ))' , 'latex':'' },
                    'twomu'             : {'cut': '(nLepGood+nLepOther >=2)' , 'latex':'' },
                  
                    # VR
                    'EVR1'              : {'cut': '({CT1} > 200)&&({CT1} <= 300)' , 'latex':'' },
                    'EVR2'              : {'cut': '({CT2} > 200)&&({CT2} <= 300)' , 'latex':'' },
                    'VL_TEST'           : {'cut': "Flag_Filters&&met_pt>200.&&Jet_pt[IndexJet_basJet_lowpt[0]]>100.&&ht_basJet_def>300.&&dPhi_j1j2_vetoJet_lowpt<2.5&&Sum$(TauGood_pt[0]>20.&&abs(TauGood_eta)<2.4)==0&&Sum$(LepGood_pt[IndexLepGood_lep_lowpt]>20)<2&&LepGood_pt[IndexLepGood_mu_lowpt[0]]>3.5&&Sum$(Jet_pt[IndexJet_basJet_lowpt]>60)<3&&ht_basJet_def>300.&&met_pt>200.&&!(ht_basJet_def>400.&&met_pt>300.)" , 'latex':''},
                    'VL_TEST_ETACUT'    : {'cut': "Flag_Filters&&met_pt>200.&&Jet_pt[IndexJet_basJet_lowpt[0]]>100.&&ht_basJet_def>300.&&dPhi_j1j2_vetoJet_lowpt<2.5&&Sum$(TauGood_pt[0]>20.&&abs(TauGood_eta)<2.4)==0&&Sum$(LepGood_pt[IndexLepGood_lep_lowpt]>20)<2&&LepGood_pt[IndexLepGood_mu_lowpt[0]]>3.5&&abs(LepGood_eta[IndexLepGood_mu_lowpt[0]])<1.5&&Sum$(Jet_pt[IndexJet_basJet_lowpt]>60)<3&&ht_basJet_def>300.&&met_pt>200.&&!(ht_basJet_def>400.&&met_pt>300.)" , 'latex':''},

                    # Sideband 
                    'CT2_200'           : {'cut' : '{CT2} > 200'                 ,'latex':''}, # CT2 ISR sideband
                    
                    ### Fake Rate Cuts ###
                    'fake'              : {'cut' : '({isFakeFromTau1}==0)&&({lepCol}_mcMatchId[{lepIndex1}] == 0 || {lepCol}_mcMatchId[{lepIndex1}] == 99 || {lepCol}_mcMatchId[{lepIndex1}] == 100)', 'latex':''},
                    'prompt'            : {'cut' : '({isFakeFromTau1}==1)||({lepCol}_mcMatchId[{lepIndex1}] != 0 && {lepCol}_mcMatchId[{lepIndex1}] != 99 && {lepCol}_mcMatchId[{lepIndex1}] != 100)', 'latex':''},

                    'fake_LnT'          : {'cut' : '({isFakeFromTau_loose1}==0)&&({lepCol}_mcMatchId[{lepIndex_loose1}] == 0 || {lepCol}_mcMatchId[{lepIndex_loose1}] == 99 || {lepCol}_mcMatchId[{lepIndex_loose1}] == 100)', 'latex':''},
                    'prompt_LnT'        : {'cut' : '({isFakeFromTau_loose1}==1)||({lepCol}_mcMatchId[{lepIndex_loose1}] != 0 && {lepCol}_mcMatchId[{lepIndex_loose1}] != 99 && {lepCol}_mcMatchId[{lepIndex_loose1}] != 100)', 'latex':''},


                    #'fakeTauVeto'       : {'cut' : '({nLep} > 0) && ((%s) || ((%s) > 0.15))'%(genTauCondFalse, dRmin), 'latex':''},

                    #'allowFakesFromTau'       : {'cut' : '({nLep} > 0) && ((%s) || ((%s) > 0.15))'%(genTauCondFalse, dRmin), 'latex':''},
                    #'allowFakesFromTau_LnT'   : {'cut' : '({nLep} > 0) && ((%s) || ((%s) > 0.15))'%(genTauCondFalse, dRmin_LnT), 'latex':''},
                    #'isFakeFromTau'       : {'cut' : '({isFakeFromTau} == 1)'  , 'latex':'' },
                    #'isFakeFromTau_LnT'   : {'cut' : '({isFakeFromTau_loose} == 1)'  , 'latex':'' },

                    'fakeTauVeto'         : {'cut' : '({isFakeFromTau1} == 0)', 'latex':''},
                    'fakeTauVeto_LnT'     : {'cut' : '({isFakeFromTau_loose1}== 0)', 'latex':''},
                    #mateusz 'notTight'          : {'cut' : 'n{lepCol}_{lep}_def == 0', 'latex':''},
                    #'notTight'         : {'cut' : '(n{lepCol}_{lep}_def == 0) || (n{lepCol}_{lep}_def == 1 && {lepIndex1} != Max$(Alt$(Index{lepCol}_{lep}_def[0],-999)))', 'latex':''},
                    #'notTight'          : {'cut' : '(n{lepCol}_{lep}{lt} == 0) || (n{lepCol}_{lep}{lt} >= 1 && n{lepCol}_{lep}{looseWP}[0] != Max$(Alt$(Index{lepCol}_{lep}_def[0],-999)))', 'latex':''},
                    #'notTight'          : {'cut' : '(n{lepCol}_{lep}{lt} == 0) || (n{lepCol}_{lep}{lt} >= 1 && n{lepCol}_{lep}{looseWP}[0] != Max$(Alt$(Index{lepCol}_{lep}_def[0],-999)))', 'latex':''},
                    #'notTight'          : {'cut' : '({nLep} == 0) || ({nLep} >= 1 && {lepIndex_loose}[0] != Max$(Alt$({lepIndex1},-999)))'  , 'latex':''},
                    #'notTight'          : {'cut':  "!Sum$({lepCol}_pt[{lepIndex_lep}]>3.5)" , 'latex': '' } ,         
                    #'notTight'          : {'cut':  "({nLep_lep}==0||Sum$({lepIndex_lep_loose}!={lepIndex_lep1})==0)" , 'latex': '' } ,         
                    #'notTight'          : {'cut':  "Sum$({lepCol}_pt[{lepIndex_lep1}]>20)==0" , 'latex': '' } ,         
                    #'notTight'          : {'cut':  "Sum$( {lepCol}_pt[{lepIndex}[0]]3.5)" , 'latex': '' } ,         
                    # Measurement region 1 
                    'min1Lep'           : {'cut':  '{nLep} > 0',   'latex':''},
                    'HT900'             : {'cut' : '{ht} > 900',   'latex':''},
                    'MET_lt_40'         : {'cut' : '{met} < 40',   'latex':''},
                    'MT_lt_30'          : {'cut' : '{lepMT} < 30', 'latex':''},
                    
                    # Measurement region 2 
                    '2Lep'              : {'cut': 'n{lepCol}_lep{lt} == 2',  'latex':''}, #1 tag, 1 lepton
                    '1Tag'              : {'cut': 'n{lepCol}_lep_def >= 1',  'latex':''}, #1 tight tag
                    '1Probe'            : {'cut': '{nLep} >= 1',  'latex':''}, #1 probe
                    'probeFlav'         : {'cut': 'abs({lepPdgId}) == abs(LepGood_pdgId[Index{lepCol}_{lep}{lt}[0]])', 'latex':''}, # NOTE: Hardcoded for tight leptons
                    'tagPt_gt_30'       : {'cut': '{lepCol}_pt[{tagIndex}] > 30',  'latex':''}, # NOTE: Hardcoded for tight leptons
                    'tagMT_lt_100'      : {'cut': '{lepCol}_mt[{tagIndex}] < 100', 'latex':''}, # NOTE: Hardcoded for tight leptons
                    
                    'SS'                : {'cut': '{lepCharge} == {tagCharge}', 'latex':'' },
                    'max2Jets'          : {'cut': '{nJet}<=2', 'latex':'' },
                }
        
        #if 'lowpt' in settings['lepTag']:
        #   cuts_dict['notTight']['cut'] = cuts_dict['notTight']['cut'].replace('def', 'lowpt')

        if settings.get('mvaId'):
            cuts_dict.update({
                    #MVA
                    'mva_presel_cut'         : {'cut' : 'mva_preselectedEvent[{mvaIdIndex}]' ,'latex':''},
                    'bdt_gt'                 : {'cut' : 'mva_response[{mvaIdIndex}]>{bdtcut}' , 'latex':''},
                    'bdt_lt'                 : {'cut' : 'mva_response[{mvaIdIndex}]<{bdtcut} && mva_response[{mvaIdIndex}] != -99999' , 'latex':''},
                    #'bdt_gt_0p4'            : {'cut' : 'mva_response[{mvaIdIndex}]>0.4'  , 'latex':''},
                    #'bdt_lt_0p4'            : {'cut' : 'mva_response[{mvaIdIndex}]<0.4'  , 'latex':''},
                    #'bdt_gt_0p55'           : {'cut' : 'mva_response[{mvaIdIndex}]>0.55' , 'latex':''},
                    #'bdt_lt_0p55'           : {'cut' : 'mva_response[{mvaIdIndex}]<0.55' , 'latex':''},
                })

        for methtCut in [100, 200, 280, 250, 280, 300, 350, 400]:
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

        regions['vltest']   = {'baseCut': None     , 'cuts': ['VL_TEST'] , 'latex':''}
        regions['vltest_etacut']   = {'baseCut': None     , 'cuts': ['VL_TEST_ETACUT'] , 'latex':''}
        regions['vltest_pt_lt_30']   = {'baseCut': None     , 'cuts': ['VL_TEST', "lepPt_lt_30"] , 'latex':''}
        regions['vltest_pt_lt_5']   = {'baseCut': None     , 'cuts': ['VL_TEST', "ptVL"] , 'latex':''}


        #regions['presel_EVR1']  = {'baseCut': None     , 'cuts': sidebands['validation_regions']['baseCut']     , 'latex': '' } 
        #regions['presel_EVR1'] = {'baseCut': None     , 'cuts': ['EVR1' , 'lepEta1p5', 'BSR1']     , 'latex': '' } 
 
        regions['presel_LIP_incLepPt'] = {'baseCut': None     , 'cuts': ['MET300','HT200', 'isrPt110',  'AntiQCD' ]          , 'latex': '' } 
        regions['presel_Cristovao']    = {'baseCut': None     , 'cuts': ['MET280','HT200', 'isrPt110',  'AntiQCD'  ,'1Lep', '2ndLep20Veto']          , 'latex': '' } 
        regions['presel_LIP']           = {'baseCut': None     , 'cuts': ['MET300','HT200', 'isrPt110',  'AntiQCD'  , '3rdJetVeto' ,'1Lep', '2ndLep20Veto', 'lepPt_lt_30' ]          , 'latex': '' } 

        regions['presel_train_LIP']  = {'baseCut': None     , 'cuts': ['MET280','HT200', 'isrPt110',  'AntiQCD'   ,'1Lep', '2ndLep20Veto', 'lepPt_lt_30' ]       , 'latex': '' } 
        regions['presel_app_LIP']    = {'baseCut': None     , 'cuts': ['MET300','HT200', 'isrPt110',  'AntiQCD'   ,'1Lep', '2ndLep20Veto', 'lepPt_lt_30' ]       , 'latex': '' } 
        
        regions['presel_mvaTrain'] = {'baseCut': None, 'cuts': ['MET280', 'HT200','isrPt110', 'AntiQCD', '3rdJetVeto', '1Lep', '2ndLep20Veto', 'lepPt_lt_30'], 'latex': ''} 

        regions['presel_twomu'] = {'baseCut': None     , 'cuts': ['MET200','HT200',  'twomu' ]          , 'latex': '' } 

        regions['presel_base']   = {'baseCut': None     , 'cuts': ['MET200', 'ISR100', 'HT300', 'AntiQCD', '3rdJetVeto', 'TauVeto', '2ndLep20Veto' ]                        , 'latex': '' } 
        regions['presel']        = {'baseCut': None     , 'cuts': ['MET200', 'ISR100', 'HT300', 'AntiQCD', '3rdJetVeto', 'TauVeto', '1Lep', '2ndLep20Veto' ]                , 'latex': '' } 
        regions['presel_prompt'] = {'baseCut': None     , 'cuts': ['MET200', 'ISR100', 'HT300', 'AntiQCD', '3rdJetVeto', 'TauVeto', '1Lep', '2ndLep20Veto'      ]           , 'latex': '' } 
        regions['presel_LnT']    = {'baseCut': None     , 'cuts': ['MET200', 'ISR100', 'HT300', 'AntiQCD', '3rdJetVeto', 'TauVeto', '1LooseLep', '2ndLep20Veto' ] + LnTCuts , 'latex': '' } 

        regions['presel_EVR_base']   = {'baseCut': None     , 'cuts': [ 'AntiQCD', '3rdJetVeto', 'TauVeto' , '2ndLep20Veto' ]                          , 'latex': '' } 

        regions['presel_EVR1_base']   = {'baseCut': None     , 'cuts': ['EVR1', 'ISR100',  'AntiQCD', '3rdJetVeto', 'TauVeto' , '2ndLep20Veto' ]                          , 'latex': '' } 
        regions['presel_EVR1']        = {'baseCut': None     , 'cuts': ['EVR1', 'ISR100',  'AntiQCD', '3rdJetVeto', 'TauVeto', '1Lep', '2ndLep20Veto' ]                   , 'latex': '' } 
        regions['presel_EVR1_prompt'] = {'baseCut': None     , 'cuts': ['EVR1', 'ISR100',  'AntiQCD', '3rdJetVeto', 'TauVeto', '1Lep', '2ndLep20Veto' ]                   , 'latex': '' } 
        regions['presel_EVR1_LnT']    = {'baseCut': None     , 'cuts': ['EVR1', 'ISR100',  'AntiQCD', '3rdJetVeto', 'TauVeto', '1LooseLep', '2ndLep20Veto' ]   + LnTCuts  , 'latex': '' } 

        regions['presel_EVR2_base']   = {'baseCut': None     , 'cuts': ['EVR2', 'ISR100',  'AntiQCD', '3rdJetVeto', 'TauVeto' , '2ndLep20Veto' ]                          , 'latex': '' } 
        regions['presel_EVR2']        = {'baseCut': None     , 'cuts': ['EVR2', 'ISR100',  'AntiQCD', '3rdJetVeto', 'TauVeto', '1Lep', '2ndLep20Veto' ]                   , 'latex': '' } 
        regions['presel_EVR2_prompt'] = {'baseCut': None     , 'cuts': ['EVR2', 'ISR100',  'AntiQCD', '3rdJetVeto', 'TauVeto', '1Lep', '2ndLep20Veto' ]                   , 'latex': '' } 
        regions['presel_EVR2_LnT']    = {'baseCut': None     , 'cuts': ['EVR2', 'ISR100',  'AntiQCD', '3rdJetVeto', 'TauVeto', '1LooseLep', '2ndLep20Veto' ]   + LnTCuts  , 'latex': '' } 

        regions['sr1'   ] = {'baseCut': 'presel_prompt' , 'cuts': ['CT300', 'BSR1', 'lepEta1p5', 'lepPt_lt_30']                                                   , 'latex': '' }
        regions['sr1a'  ] = {'baseCut': 'sr1'    , 'cuts': ['negLep', 'MTa']                                                                               , 'latex': '' }
        regions['sr1b'  ] = {'baseCut': 'sr1'    , 'cuts': ['negLep', 'MTb']                                                                               , 'latex': '' }
        regions['sr1c'  ] = {'baseCut': 'sr1'    , 'cuts': ['MTc']                                                                                         , 'latex': '' }
        regions['sr1ab' ] = {'baseCut': 'sr1'   , 'cuts': ['negLep', 'MTab']                                                                               , 'latex': '' }
        regions['sr2'   ] = {'baseCut': 'presel_prompt' , 'cuts': ['MET300', 'ISR325', 'BSR2' , 'lepPt_lt_30']                                                    , 'latex': '' }

        regions['sr1vla' ] = {'baseCut': 'sr1a'    , 'cuts': ['ptVL']                                                                               , 'latex': '' }
        regions['sr1la' ]  = {'baseCut': 'sr1a'    , 'cuts': ['ptL']                                                                               , 'latex': '' }
        regions['sr1ma' ]  = {'baseCut': 'sr1a'    , 'cuts': ['ptM']                                                                               , 'latex': '' }
        regions['sr1ha' ]  = {'baseCut': 'sr1a'    , 'cuts': ['ptH']                                                                               , 'latex': '' }
        regions['sr1vlb' ] = {'baseCut': 'sr1b'    , 'cuts': ['ptVL']                                                                               , 'latex': '' }
        regions['sr1lb' ]  = {'baseCut': 'sr1b'    , 'cuts': ['ptL']                                                                               , 'latex': '' }
        regions['sr1mb' ]  = {'baseCut': 'sr1b'    , 'cuts': ['ptM']                                                                               , 'latex': '' }
        regions['sr1hb' ]  = {'baseCut': 'sr1b'    , 'cuts': ['ptH']                                                                               , 'latex': '' }
        regions['sr1vlc' ] = {'baseCut': 'sr1c'    , 'cuts': ['ptVL']                                                                               , 'latex': '' }
        regions['sr1lc' ]  = {'baseCut': 'sr1c'    , 'cuts': ['ptL']                                                                               , 'latex': '' }
        regions['sr1mc' ]  = {'baseCut': 'sr1c'    , 'cuts': ['ptM']                                                                               , 'latex': '' }
        regions['sr1hc' ]  = {'baseCut': 'sr1c'    , 'cuts': ['ptH']                                                                               , 'latex': '' }
        regions['sr2vl'  ] = {'baseCut': 'sr2'     , 'cuts': ['ptVL']                                                                               , 'latex': '' }
        regions['sr2l'  ]  = {'baseCut': 'sr2'     , 'cuts': ['ptL']                                                                               , 'latex': '' }
        regions['sr2m'  ]  = {'baseCut': 'sr2'     , 'cuts': ['ptM']                                                                               , 'latex': '' }
        regions['sr2h'  ]  = {'baseCut': 'sr2'     , 'cuts': ['ptH']                                                                               , 'latex': '' }
        
        regions['cr1'   ]  = {'baseCut': 'presel_prompt'  , 'cuts': ['CT300', 'BSR1', 'lepEta1p5', 'lepPt_gt_30']                                                   , 'latex': '' }
        regions['cr1a'  ]  = {'baseCut': 'cr1'     , 'cuts': ['negLep', 'MTa']                                                                               , 'latex': '' }
        regions['cr1b'  ]  = {'baseCut': 'cr1'     , 'cuts': ['negLep', 'MTb']                                                                               , 'latex': '' }
        regions['cr1c'  ]  = {'baseCut': 'cr1'     , 'cuts': ['MTc']                                                                                         , 'latex': '' }
        regions['cr2'   ]  = {'baseCut': 'presel_prompt'  , 'cuts': ['MET300', 'ISR325', 'BSR2' , 'lepPt_gt_30']                                                    , 'latex': '' }
        regions['crtt'  ]  = {'baseCut': 'presel_prompt'  , 'cuts': ['BCR']                                                    , 'latex': '' }


        srcrs = ['sr1', 'sr2', 'cr1','cr2', 'crtt']
        fake_prompt_map ={
                          'MTInc' : 'MTInc_LnT',
                            'MTa' : 'MTa_LnT', 
                            'MTb' : 'MTb_LnT', 
                            'MTc' : 'MTc_LnT',
                            'ptVL': 'ptVL_LnT', 
                            'ptL' : 'ptL_LnT',  
                            'ptM' : 'ptM_LnT',  
                            'ptH' : 'ptH_LnT',
                     'lepPt_gt_30': 'lepPt_gt_30_LnT',  
                     'lepPt_lt_30': 'lepPt_lt_30_LnT', 
                     'lepEta1p5'  : 'lepEta1p5_LnT',
                        'negLep'  : 'negLep_LnT',
                        'posLep'  : 'posLep_LnT',
                         }

        print regions.keys()
        LnTTag = "_LnT"
        srcr_regions = [x for x in regions.keys() if degTools.anyIn(srcrs , x) ]
        print srcr_regions
        for region in srcr_regions:
            newRegion = deepcopy(regions[region])
            if newRegion['baseCut']:
                newRegion['baseCut'] = newRegion['baseCut'].replace( "_prompt", LnTTag )
            if newRegion['baseCut'] in srcr_regions:
                newRegion['baseCut'] += LnTTag
            for cutName in newRegion.get('cuts',[]):
                if cutName in fake_prompt_map.keys():
                    idx_ = newRegion['cuts'].index(cutName)
                    newRegion['cuts'].pop(idx_)
                    newRegion['cuts'].insert(idx_, cutName + LnTTag )
            regions[region+"_LnT"] = newRegion


        ## EVR1 Create Validation Regions For SR1 
        srcr_and_LnT_regions = srcr_regions + [x+LnTTag for x in srcr_regions]
        for region in srcr_regions + [x+LnTTag for x in srcr_regions]:
            newRegion = deepcopy(regions[region])
            if "presel" in newRegion['baseCut']:
                newRegion['baseCut'] = newRegion['baseCut'].replace("presel", "presel_EVR1") 
            elif newRegion['baseCut'] in srcr_and_LnT_regions:
                newRegion['baseCut'] = 'v' + newRegion['baseCut'] 
            for cutName in  newRegion.get('cuts',[]):
                if cutName in ['CT300']:
                    newRegion['cuts'].remove(cutName)
            regions["v"+region] = newRegion

            #if 

        # LnT Regions
        #regions['presel_LnT'] = {'baseCut': None     , 'cuts': ['MET200', 'ISR100', 'HT300', 'AntiQCD', '3rdJetVeto', 'TauVeto', '1Lep', '2ndLep20Veto']          , 'latex': '' } 
        #regions['sr1_LnT'   ] = {'baseCut': 'presel_LnT' , 'cuts': ['CT300', 'BSR1', 'lepEta1p5', 'lepPt_lt_30']                                                   , 'latex': '' }
        #regions['sr1a_LnT'  ] = {'baseCut': 'sr1_LnT'    , 'cuts': ['negLep', 'MTa']                                                                               , 'latex': '' }
        #regions['sr1b_LnT'  ] = {'baseCut': 'sr1_LnT'    , 'cuts': ['negLep', 'MTb']                                                                               , 'latex': '' }
        #regions['sr1c_LnT'  ] = {'baseCut': 'sr1_LnT'    , 'cuts': ['MTc']                                                                                         , 'latex': '' }
        #regions['sr1ab_LnT' ] = {'baseCut': 'sr1_LnT'   , 'cuts': ['negLep', 'MTab']                                                                               , 'latex': '' }
        #regions['sr2_LnT'   ] = {'baseCut': 'presel_LnT' , 'cuts': ['MET300', 'ISR325', 'BSR2' , 'lepPt_lt_30']                                                    , 'latex': '' }

        #regions['sr1vla_LnT' ] = {'baseCut': 'sr1a_LnT'    , 'cuts': ['ptVL']                                                                               , 'latex': '' }
        #regions['sr1la_LnT' ] = {'baseCut': 'sr1a_LnT'    , 'cuts': ['ptL']                                                                               , 'latex': '' }
        #regions['sr1ma_LnT' ] = {'baseCut': 'sr1a_LnT'    , 'cuts': ['ptM']                                                                               , 'latex': '' }
        #regions['sr1ha_LnT' ] = {'baseCut': 'sr1a_LnT'    , 'cuts': ['ptH']                                                                               , 'latex': '' }
        #regions['sr1vlb_LnT' ] = {'baseCut': 'sr1b_LnT'    , 'cuts': ['ptVL']                                                                               , 'latex': '' }
        #regions['sr1lb_LnT' ] = {'baseCut': 'sr1b_LnT'    , 'cuts': ['ptL']                                                                               , 'latex': '' }
        #regions['sr1mb_LnT' ] = {'baseCut': 'sr1b_LnT'    , 'cuts': ['ptM']                                                                               , 'latex': '' }
        #regions['sr1hb_LnT' ] = {'baseCut': 'sr1b_LnT'    , 'cuts': ['ptH']                                                                               , 'latex': '' }
        #regions['sr1vlc_LnT' ] = {'baseCut': 'sr1c_LnT'    , 'cuts': ['ptVL']                                                                               , 'latex': '' }
        #regions['sr1lc_LnT' ] = {'baseCut': 'sr1c_LnT'    , 'cuts': ['ptL']                                                                               , 'latex': '' }
        #regions['sr1mc_LnT' ] = {'baseCut': 'sr1c_LnT'    , 'cuts': ['ptM']                                                                               , 'latex': '' }
        #regions['sr1hc_LnT' ] = {'baseCut': 'sr1c_LnT'    , 'cuts': ['ptH']                                                                               , 'latex': '' }
        #regions['sr2vl_LnT'  ] = {'baseCut': 'sr2_LnT'     , 'cuts': ['ptVL']                                                                               , 'latex': '' }
        #regions['sr2l_LnT'  ] = {'baseCut': 'sr2_LnT'     , 'cuts': ['ptL']                                                                               , 'latex': '' }
        #regions['sr2m_LnT'  ] = {'baseCut': 'sr2_LnT'     , 'cuts': ['ptM']                                                                               , 'latex': '' }
        #regions['sr2h_LnT'  ] = {'baseCut': 'sr2_LnT'     , 'cuts': ['ptH']                                                                               , 'latex': '' }
        #
        #regions['cr1_LnT'   ] = {'baseCut': 'presel_LnT'  , 'cuts': ['CT300', 'BSR1', 'lepEta1p5', 'lepPt_gt_30']                                                   , 'latex': '' }
        #regions['cr1a_LnT'  ] = {'baseCut': 'cr1_LnT'     , 'cuts': ['negLep', 'MTa']                                                                               , 'latex': '' }
        #regions['cr1b_LnT'  ] = {'baseCut': 'cr1_LnT'     , 'cuts': ['negLep', 'MTb']                                                                               , 'latex': '' }
        #regions['cr1c_LnT'  ] = {'baseCut': 'cr1_LnT'     , 'cuts': ['MTc']                                                                                         , 'latex': '' }
        #regions['cr2_LnT'   ] = {'baseCut': 'presel_LnT'  , 'cuts': ['MET300', 'ISR325', 'BSR2' , 'lepPt_gt_30']                                                    , 'latex': '' }
        #regions['crtt_LnT'  ] = {'baseCut': 'presel_LnT'  , 'cuts': ['BCR']                                                    , 'latex': '' }




        regions['bins_sum'  ] = {'baseCut': 'presel_base' , 'regions': [ 'presel_base',
                                                                       'sr1a',  'sr1vla' ,'sr1la' , 'sr1ma', 'sr1ha',
                                                                       'sr1b',  'sr1vlb' ,'sr1lb' , 'sr1mb', 'sr1hb',
                                                                       'sr1c',  'sr1vlc' ,'sr1lc' , 'sr1mc', 'sr1hc',
                                                                       'sr2' ,  'sr2vl'  ,'sr2l'  , 'sr2m' , 'sr2h' ,
                                                                       'cr1a' , 'cr1b' , 'cr1c', 'cr2' , 'crtt',

                                                                       'sr1a_LnT',  'sr1vla_LnT' ,'sr1la_LnT' , 'sr1ma_LnT', 'sr1ha_LnT',
                                                                       'sr1b_LnT',  'sr1vlb_LnT' ,'sr1lb_LnT' , 'sr1mb_LnT', 'sr1hb_LnT',
                                                                       'sr1c_LnT',  'sr1vlc_LnT' ,'sr1lc_LnT' , 'sr1mc_LnT', 'sr1hc_LnT',
                                                                       'sr2_LnT' ,  'sr2vl_LnT'  ,'sr2l_LnT'  , 'sr2m_LnT' , 'sr2h_LnT' ,
                                                                       'cr1a_LnT' , 'cr1b_LnT' , 'cr1c_LnT', 'cr2_LnT' , 'crtt_LnT',
                                                                   ]       , 'latex':''}

        regions['bins_sum_vr'  ] = {'baseCut': 'presel_EVR1_base' , 'regions': [ 'presel_EVR1_base',
                                                                       'vsr1a',  'vsr1vla' ,'vsr1la' , 'vsr1ma', 'vsr1ha',
                                                                       'vsr1b',  'vsr1vlb' ,'vsr1lb' , 'vsr1mb', 'vsr1hb',
                                                                       'vsr1c',  'vsr1vlc' ,'vsr1lc' , 'vsr1mc', 'vsr1hc',
                                                                       'vsr2' ,  'vsr2vl'  ,'vsr2l'  , 'vsr2m' , 'vsr2h' ,
                                                                       'vcr1a' , 'vcr1b' , 'vcr1c', 'vcr2' , 'vcrtt',

                                                                       'vsr1a_LnT',  'vsr1vla_LnT' ,'vsr1la_LnT' , 'vsr1ma_LnT', 'vsr1ha_LnT',
                                                                       'vsr1b_LnT',  'vsr1vlb_LnT' ,'vsr1lb_LnT' , 'vsr1mb_LnT', 'vsr1hb_LnT',
                                                                       'vsr1c_LnT',  'vsr1vlc_LnT' ,'vsr1lc_LnT' , 'vsr1mc_LnT', 'vsr1hc_LnT',
                                                                       'vsr2_LnT' ,  'vsr2vl_LnT'  ,'vsr2l_LnT'  , 'vsr2m_LnT' , 'vsr2h_LnT' ,
                                                                       'vcr1a_LnT' , 'vcr1b_LnT' , 'vcr1c_LnT', 'vcr2_LnT' , 'vcrtt_LnT',
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



        for vr_name in sidebands.keys():
            validation_regions_info = sidebands[vr_name]
            validation_regions      = validation_regions_info['sideband_regions']
            vr_common               = validation_regions_info['common']
            vr_common_name          = validation_regions_info['common_name']
            vr_baseCut              = validation_regions_info['baseCut']
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
                regions[sideband_name] = {'baseCut': vr_baseCut          , 'cuts'    :  vr_common + cutListNames       , 'latex':''}
            regions[vr_name]   = {'baseCut': vr_baseCut   , 'regions' :  validation_region_names , 'latex':''}


        #regions['sr1ValidationRegion'] = {'baseCut': 'presel' , 'regions': ["EVR1"] , 'latex':''}



        # VR + BJetVeto + lepEta + [ MT , LepPt, Charge ] 

        regions['EVR1_VL' ]  = {'baseCut': 'presel_EVR1'    , 'cuts': ['ptVL']                                                                               , 'latex': '' }
        regions['VL' ]  = {'baseCut': 'presel'    , 'cuts': ['ptVL']                                                                               , 'latex': '' }

        def makeValidationRegion():
            pass

        ### Fake Rate Regions ###
        
        # Measurement Region
        regions['measurement1_kin']  =    {'baseCut': None,               'cuts': ['HT900', 'MET_lt_40'],  'latex': ''} 
        regions['measurement1']  =        {'baseCut': 'measurement1_kin', 'cuts': ['min1Lep', 'MT_lt_30', 'lepEta1p5'], 'latex': ''} 
        
        regions['measurement2_kin']  =    {'baseCut': None,               'cuts': ['HT200', 'MET100'],     'latex': ''} #, 'max2Jets'
        regions['measurement2']  =        {'baseCut': 'measurement2_kin', 'cuts': ['2Lep', '1Tag', 'tagPt_gt_30', '1Probe', 'probeFlav', 'lepEta1p5', 'SS'], 'latex': ''}
        regions['measurement2_BVeto']  =  {'baseCut': 'measurement2', 'cuts': ['BSR1'], 'latex': ''}
        regions['measurement2_BVeto_kin']  = regions['measurement2_kin'] 
        
        # Application Region
        regions['sr1_kin']  =  {'baseCut': None, 'cuts': ['MET200', 'ISR100', 'HT300', 'AntiQCD', '3rdJetVeto', 'TauVeto', 'CT300'], 'latex': ''} 
        regions['sr1a_kin'] = regions['sr1b_kin'] = regions['sr1c_kin'] = regions['sr1ab_kin'] = regions['sr1_kin']
        regions['sr2_kin']  =  {'baseCut': None, 'cuts': ['MET200', 'ISR100', 'HT300', 'AntiQCD', '3rdJetVeto', 'TauVeto', 'MET300', 'ISR325'], 'latex': '' }
        
        if settings.get('mvaId'):
            regions['srBDT_kin'] = {'baseCut': None, 'cuts': ['MET280', 'HT200', 'isrPt110', 'AntiQCD', '3rdJetVeto'], 'latex': ''} 
            regions['crBDT_kin'] = regions['srBDT_kin']
 
            regions['srBDT'] =     {'baseCut': 'presel_mvaTrain', 'cuts': ['bdt_gt'], 'latex': ''}
            regions['crBDT'] =     {'baseCut': 'presel_mvaTrain', 'cuts': ['bdt_lt'], 'latex': ''}



        #leptonCut     = '1TightLep'#, '2ndLep20Veto'
        #leptonRegions = getAllRegionsWithCut( regions, leptonCut )
        #looseNotTightTag = "looseNotTight"
        #newRegions = []
        #for region_name in leptonRegions:
        #    newRegionName = region_name +"_"+looseNotTightTag
        #    newRegion  = deepcopy( regions[region_name] ) 
        #    if newRegion.get('baseCut') and newRegion['baseCut'] in leptonRegions:
        #        newRegion['baseCut'] += "_"+looseNotTightTag
        #    if leptonCut in newRegion.get('cuts', []):
        #        cutIndex = newRegion['cuts'].index(leptonCut)
        #        newRegion['cuts'].pop(cutIndex)
        #        newRegion['cuts'].insert( cutIndex  , leptonCut.replace("Tight","Loose") )
        #        newRegion['cuts'].insert( cutIndex + 1 , "notTight" )
        #    for cutName in newRegion.get('cuts',[]):
        #        if cutName in leptonRegions:
        #            cutName += "_" + looseNotTightTag 
        #    for cutName in newRegion.get('regions',[]):
        #        if cutName in leptonRegions:
        #            cutName += "_" + looseNotTightTag 
        #    regions[newRegionName] = newRegion
        #    newRegions.append(newRegionName)
        #print newRegions
        #print leptonRegions

        #if otherLep:
        #    for reg in [x for x in regions if 'cuts' in regions[x] and '1Lep-2ndLep20Veto' in regions[x]['cuts']]: #NOTE: Careful when changing 1Lep-2ndLep20Veto
        #       regions[reg]['cuts'].append('otherLep20Veto')


        #isr_reweight = "( {isrNormFact} * ( (nIsr==0)*{a0} + (nIsr==1)*{a1}  + (nIsr==2)*{a2}  + (nIsr==3)*{a3}  + (nIsr==4)*{a4}  + (nIsr==5)*{a5}  + (nIsr>=6)*{a6} )) "
        isr_reweight = "( (nIsr==0)*{a0} + (nIsr==1)*{a1}  + (nIsr==2)*{a2}  + (nIsr==3)*{a3}  + (nIsr==4)*{a4}  + (nIsr==5)*{a5}  + (nIsr>=6)*{a6} ) "


        ######################################################################################
        ######################################################################################
        ##                                                                                  ##
        ##                                  WEIGHT DEFINITIONS                              ##
        ##                                                                                  ##
        ######################################################################################
        ######################################################################################
        weights_dict = deepcopy(vars_dict)
    
        weights_dict.update({
    
                    'sf'        :       {    'var' : settings['btagSF']                      ,   'latex':""            },
                    'jt'        :       {    'var' : settings['jetTag']                      ,   'latex':""            },
                    'lt'        :       {    'var' : settings['lepTag']                      ,   'latex':""            },
                    'lepCol'    :       {    'var' : settings['lepCol']                      ,   'latex':""            },
                    'lep'       :       {    'var' : settings['lep']                         ,   'latex':""            },
                    'lepIndex1'  :       {    'var' : 'Index{lepCol}_{lep}{lt}[0]',   'latex':""            },
    
                    "noweight"  :  {'var': "(1)",                                            "latex":""},
                    "weight"    :  {'var': "weight",                                            "latex":""},
    
                    'wpt_a'     : {'var': wpt_weight_a                                  ,               "latex":""},
                    'wpt_a_LnT' : {'var': wpt_weight_a.replace("{wpt}","{wpt_loose}")   ,               "latex":""},
                    #'wpt_p' : {'var': wpt_weight_p  ,               "latex":""},
                    #'wpt_n' : {'var': wpt_weight_n  ,               "latex":""},
    
                    #'wpt'         : {'var':  "(sqrt(({lepCol}_pt[max(0,{lepIndex1}[0])]*cos({lepCol}_phi[max(0,{lepIndex1}[0])]) + met_pt*cos(met_phi) ) **2 + ( {lepCol}_pt[max(0,{lepIndex1}[0])]*sin({lepCol}_phi[max(0,{lepIndex1}[0])])+met_pt*sin(met_phi) )^2 ))",               "latex":""},
                    'wpt'             : {'var': "{lepCol}_Wpt[{lepIndex1}]",                "latex":""},
                    'wpt_loose'       : {'var': "{lepCol}_Wpt[{lepIndex_loose1}]",                "latex":""},
    
                    'top1pt'      : {'var': "Max$(GenPart_pt*(GenPart_pdgId==6))",               "latex":""},
                    'top2pt'      : {'var': "Max$(GenPart_pt*(GenPart_pdgId==-6))",                "latex":""},
                    'ttpt'        : {'var': "1.24*exp(0.156-0.5*0.00137*({top1pt}+{top2pt}))",               "latex":""},
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
                    })
    
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
        """
            "opt" : { "sample_list": bool func(samp) / [ sampleNames ] 
                      "cut_options" :{
                                        'default': 'new_cut'
                                    'if_this_cut_in_list'   : 'add_this_cut_too'   
                                    'cut_a'   : ['cut_b', 'cut_c']  # if cut_a in cutListNames, cutListNames.extend(['cut_b',...])
                                     }
                      "weight_options" : {
                                        'default' : 'new_weight'
                                    'if_this_cut_in_list'  : 'remove_the_cut_add_this_weight_to_weightList'
                                         }

        """

        cut_weight_options = {
                            "prompt"  : { "sample_list" : lambda sample: not sample.isSignal and not  sample.isData
                                                                           ,                 "cut_options":{
                                                                                                "1Lep"       : promptCuts   ,
                                                                                                "1LooseLep"  : promptLnTCuts      ,
                                                                                               }
                                        },
                            "trig_eff"  : { "sample_list" : lambda sample: not  sample.isData
                                                                           ,                 "weight_options":{
                                                                                                "default"  : 'trigeff'      ,
                                                                                               }
                                          },
                            "trig_mc"   : { "sample_list" : lambda sample: not sample.isSignal and not  sample.isData
                                                                           ,                 "cut_options":{
                                                                                                "default"  : 'mc_trigs'     ,
                                                                                               }
                                          },
                            "pu"   : { "sample_list" : lambda sample: not sample.isSignal and not sample.isData
                                                                           ,                 "weight_options":{
                                                                                                "default"  : "pu",
                                                                                               }
                                      },
                            "wpt"   : { "sample_list" : ["WJets"] ,                 "weight_options":{
                                                                                                  #"default"    : "wpt_a",
                                                                                                  "1Lep"       : "wpt_a",
                                                                                                  "1LooseLep"  : "wpt_a_LnT",
                                                                                                  #"negLep"   : "wpt_n",
                                                                                                  #"posLep"   : "wpt_p",
                                                                                               }
                                      },
                            "ttpt"  : { "sample_list" :['TTJets' ] ,                'weight_options' : { "default": "ttpt" } },
                            "sf"    : { "sample_list" :None,                        'weight_options' : {  
                                                                                                   "BCR":"BCR",
                                                                                                   "BVR":"BVR",
                                                                                                   "BSR1":"BSR1",
                                                                                                   "BSR2":"BSR2",
                                                                                                 }
                                       },
                            "isr"    : { "sample_list" :["T2tt", "T2bw"],            'weight_options' : {  
                                                                                                  "default":"isr"
                                                                                                 }
                                       },
                            "isr_tt"    : { "sample_list" :["TTJets", "TT_1l", "TT_2l" ],            'weight_options' : {  
                                                                                                  "default":"isr_tt"
                                                                                                 }
                                       },
                         }


        variations_dict = {
                        'pu' : ['up', 'down'],
                     }
        
        for weight_opt, variations in variations_dict.items():
            for variation in variations:
                new_weight_opt_name = weight_opt + "_" + variation
                new_weight_opt_dict     = deepcopy( cut_weight_options[weight_opt] )
                new_weight_options      = new_weight_opt_dict.get("weight_options",{})
                if new_weight_options.get('default'):
                    new_weight_options['default'] = new_weight_options['default'] + "_" + variation
                new_cut_optionss      = new_weight_opt_dict.get("cut_optionss",{})
                if new_cut_optionss.get('default'):
                    new_cut_optionss['default'] = new_cut_optionss['default'] + "_" + variation
                cut_weight_options[new_weight_opt_name ] = new_weight_opt_dict 
                print 'variations', new_weight_opt_name, new_weight_opt_dict 
        self.weights_dict   =   weights_dict
        self.vars_dict      =   vars_dict
        self.cuts_dict      =   cuts_dict
        self.regions        =   regions
        self.cut_weight_options =   cut_weight_options
