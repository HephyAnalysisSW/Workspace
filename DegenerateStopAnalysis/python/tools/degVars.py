import os
import ROOT
import collections
import itertools
from copy import deepcopy
import Workspace.DegenerateStopAnalysis.tools.degTools as degTools
from Workspace.DegenerateStopAnalysis.samples.baselineSamplesInfo import getCutWeightOptions, triggers

cutWeightOptions = getCutWeightOptions()
settings = cutWeightOptions['settings']

leptkeffscr = os.path.expandvars("$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/data/leptonSFs/GetLepTkEff.C");
ROOT.gROOT.ProcessLineSync(".L  %s"%leptkeffscr)

script = os.path.expandvars("$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/data/leptonSFs/FixEleDoubleSF.C")
ROOT.gROOT.ProcessLineSync(".L  %s"%script)



#from Workspace.DegenerateStopAnalysis.samples.baselineSamplesInfo import lumis, triggers, sample_names 

sidebands = {
               'sr1_vr' : {
                                    'baseCut'     : ['presel_EVR1', ['EVR1' , 'lepEta_lt_1p5'] ] ,
                                    #'baseCut'     : ['presel_EVR1', ['EVR1'  ] ] ,
                                    'common_name' : 'EVR1'  ,
                                    'common'      : ['EVR1' , 'lepEta_lt_1p5', 'BSR1'],
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
    @staticmethod
    def _getListOfBaseCuts( regions, region_name ):
        region = regions[region_name]
        baseCut = region.get("baseCut")
        if baseCut:
            baseCuts = VarsCutsWeightsRegions._getListOfBaseCuts(regions, baseCut)
            return [baseCut] + baseCuts
        else:
            return []

    @staticmethod
    def _getCutListsFromBaseCuts( regions, region_name ):
        baseCuts = VarsCutsWeightsRegions._getListOfBaseCuts( regions, region_name)
        cuts = [region_name] + baseCuts
        ret = []
        for c in cuts:
            clist = VarsCutsWeightsRegions._getRegionCutNames( regions, c, recursive = False)
            ret.append( [c, clist] )
        return ret 

    @staticmethod
    def _getRegionCutNames( regions, region_name, recursive = True):
        region  = regions[region_name]
        region_cut_names = region['cuts'] if 'cuts' in region.keys() else []
        baseCut_cutListNames = []
        ret = [] 
        if recursive: 
            baseCut_cutListNames = VarsCutsWeightsRegions._getRegionCutNames( regions, region['baseCut'] ) if region['baseCut'] else []
            ret.extend( baseCut_cutListNames ) 
        ret.extend([c for c in region_cut_names if c not in baseCut_cutListNames])
        return ret

    @staticmethod
    def getNewCutList( regions, old_region, new_region, cuts_to_replace = [] , cuts_to_remove=[], cuts_to_add =[]):
        """
            creates a new region based on the cuts_to_replace, remove and add
            cuts_to_replace should have a format like this  [ ['c_old1', 'c_new1' ], 
                                                              ['c_old2', ['c_new2', 'c_new3'] ] ...]
        """
        oldRegion   = regions[old_region]
        oldCutListNames = VarsCutsWeightsRegions._getRegionCutNames( regions, old_region)       
        newCutListNames = [c for c in oldCutListNames if c not in cuts_to_remove ] + cuts_to_add
        for c_old, c_news in cuts_to_replace:
            if not type(c_news) in [ list, tuple] : c_news = [ c_news ] 
            if c_old in newCutListNames:
                c_old_index =  newCutListNames.index(c_old)
                newCutListNames.pop(c_old_index)
                for c_new in c_news:
                    newCutListNames.insert( c_old_index , c_new )
        return newCutListNames
    
    @staticmethod
    def makeNewRegion( regions, old_region, new_region, cuts_to_add  ):
        """
        """
        oldRegion       = regions[old_region]
        newRegion       = deepcopy( oldRegion )
        newRegion['cuts'].extend(cuts_to_add) 
        regions[new_region] = newRegion
        #return newRegion
    
    


    def __init__(
                self, 
                year      = settings['year'],
                lepCol    = settings['lepCol'],
                lep       = settings['lep'],
                lepTag    = settings['lepTag'],
                tightWP   = settings['tightWP'],
                jetTag    = settings['jetTag'],
                btagSF    = settings['btagSF'],
                bdtcut_sr = settings['bdtcut_sr'],
                bdtcut_cr = settings['bdtcut_cr'],
                mvaId     = settings['mvaId'],
                lumis     = settings['lumis'],
                ** kwargs
                ):
        
        jetTag = "_" + jetTag if jetTag and not jetTag.startswith("_") else jetTag
        lepTag = "_" + lepTag if lepTag and not lepTag.startswith("_") else lepTag

        self.settings = {
                 'year'   : year,     
                 'lepCol' : lepCol,     
                 'lep'    : lep,        
                 'lepTag' : lepTag,    
                 'tightWP': tightWP,
                 'jetTag' : jetTag,        
                 'btagSF' : btagSF, 
                 'lumis'  : lumis,
        }
        if kwargs:
            self.settings.update(kwargs)

        mva_options = [mvaId, bdtcut_sr, bdtcut_cr] 
        self.isMVASetup  = all( mva_options )
        if not self.isMVASetup and any(mva_options):
            raise Exception("Seems only not all MVA options are given... %s"%mva_options)
        
        if self.isMVASetup:
            self.settings.update({
                 'mvaId'    : mvaId,
                 'bdtcut_sr': bdtcut_sr,
                 'bdtcut_cr': bdtcut_cr,
                 'bdttag'   : ('%s_%s'%(bdtcut_sr,bdtcut_cr)).replace(".","p").replace("-","m"),
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
                            'x'  : "MET_pt"  ,
        }

        ##https://indico.cern.ch/event/592621/contributions/2398559/attachments/1383909/2105089/16-12-05_ana_manuelf_isr.pdf
        moriond17_isr_reweight_params = {
                                    'a0'  :   1     ,
                                    'a1'  :   0.920 ,
                                    'a2'  :   0.821 ,
                                    'a3'  :   0.715 ,
                                    'a4'  :   0.662 ,
                                    'a5'  :   0.561 ,
                                    'a6'  :   0.511 ,
                                 }
        looseWP  = "_loose"
        if self.settings['lepTag'] == "_lowpt":
            looseWP += "_lowpt"
        #isLnTSel = "loose" in settings['lepTag']
        #if isLnTSel:
        #    LnTCuts = ['notTight' , 'prompt_LnT']
        #    tightWP = settings['lepTag'].replace("_loose","")
        #else:
        #    LnTCuts = []
        
        tightWP  = self.settings.get('tightWP')
        if not tightWP:
            tightWP = self.settings['lepTag']

        LnTCuts       = ['notTight']
        promptCuts    = ['prompt']
        promptLnTCuts = ['prompt_LnT']
        
        # dRmin Cuts
        deltaR_template = "(deltaR(GenPart_eta, {col}_eta[{idx}], GenPart_phi, {col}_phi[{idx}]))"
        deltaR_template2 = "(deltaR(genPartAll_eta, {col}_eta[{idx}], genPartAll_phi, {col}_phi[{idx}]))"
        
        genTauCond =   "(abs(GenPart_pdgId) == 15 && (abs(GenPart_motherId) == 24 || abs(GenPart_motherId) == 23 || (GenPart_motherId == -9999 && Iteration$ < 3)))"
        genGammaCond = "abs(GenPart_pdgId) == 22"
        
        genIsrCond = "(abs(genPartAll_pdgId) == 15 || abs(genPartAll_pdgId) == 1 || abs(genPartAll_pdgId) == 2 || abs(genPartAll_pdgId) == 3 || abs(genPartAll_pdgId) == 4 || abs(genPartAll_pdgId) == 5 || abs(genPartAll_pdgId) == 6 || abs(genPartAll_pdgId) == 21) && ((genPartAll_status == 71 || genPartAll_status == 23) && (abs(genPartAll_motherId) == 2212 || genPartAll_motherId == 21))"
        #genIsrCond = "((GenPart_motherId == -9999 && (abs(GenPart_pdgId) == 1 || abs(GenPart_pdgId) == 2 || abs(GenPart_pdgId) == 3 || abs(GenPart_pdgId) == 4 || abs(GenPart_pdgId) == 5 || abs(GenPart_pdgId) == 6 || abs(GenPart_pdgId) == 21 || abs(GenPart_pdgId) == 1000006 || abs(GenPart_pdgId) == 24)) && Iteration$ <= 5)"
        #genIsrCond = "(GenPart_motherId == -9999 && Iteration$ < 6)"
        #genIsrCond = "((GenPart_motherId == -9999 || (abs(GenPart_pdgId) == 22 && abs(GenPart_motherId) == 2212)) && Iteration$ < 6)"
        #genIsrCond = "(GenPart_motherId == -9999 && (abs(GenPart_pdgId) == 1 || abs(GenPart_pdgId) == 2 || abs(GenPart_pdgId) == 3 || abs(GenPart_pdgId) == 4 || abs(GenPart_pdgId) == 5 || abs(GenPart_pdgId) == 6 || abs(GenPart_pdgId) == 21 || abs(GenPart_pdgId) == 22))"

        genTauCondFalse =   "(Sum$(%s) == 0)"%genTauCond
        genGammaCondFalse = "(Sum$(%s) == 0)"%genGammaCond

        dRminTau     =  "MinIf$(%s,%s)"%(deltaR_template.format(idx="{lepIndex1}", col = "{lepCol}"), genTauCond)
        dRminGamma   =  "MinIf$(%s,%s)"%(deltaR_template.format(idx="{lepIndex1}", col = "{lepCol}"), genGammaCond)
        dRminIsr   =    "MinIf$(%s,%s)"%(deltaR_template2.format(idx="0", col = "Jet"), genIsrCond)
        #dRminGenIsr   = "MinIf$(%s,%s)"%(deltaR_template2.format(idx="0", col = "GenJet"), genIsrCond)
        #dRminTau_LnT = "MinIf$(%s,%s)"%(deltaR_template.format(idx="{lepIndex_loose1}"), genTauCond)

        pdgIdIsr =    "genPartAll_pdgId*(%s == %s)"%(deltaR_template2.format(idx="0", col = "Jet"),    dRminIsr)
        #pdgIdIsr =    "GenPart_pdgId*(%s == %s)"%(deltaR_template.format(idx="0", col = "Jet"),    dRminIsr)
        #pdgIdGenIsr = "GenPart_pdgId*(%s == %s)"%(deltaR_template.format(idx="0", col = "GenJet"), dRminGenIsr)

        vars_dict = {
            'jt'        :       {    'var' : self.settings['jetTag']                      ,   'latex':""            },
            'lt'        :       {    'var' : self.settings['lepTag']                      ,   'latex':""            },
            'looseWP'   :       {    'var' : looseWP                                 ,   'latex':""            },
            'tightWP'   :       {    'var' : tightWP                                 ,   'latex':""            },
            'lepCol'    :       {    'var' : self.settings['lepCol']                      ,   'latex':""            },
            'lep'       :       {    'var' : self.settings['lep']                         ,   'latex':""            },
            'mtCut1'    :       {    'var' : "60"                                    ,   'latex':''            },
            'mtCut2'    :       {    'var' : "95"                                    ,   'latex':''            },
            
            # jets 
            'jetRawPt'  :       {    'var' : 'Jet_rawPt'                             ,   'latex':'' },
            
            # ISR
            'isrIndex'  :       {    'var' : 'IndexJet_basJet{jt}[0]'                ,   'latex':""            },
            'isrPt'     :       {    'var' : 'Max$(Jet_pt * (abs(Jet_eta)<2.4  && (Jet_id)))'        ,   'latex':""            },
            #'isrPt'     :       {    'var' : 'Max$(Jet_pt[{isrIndex}])'        ,   'latex':""            },
            'GenIsrPt'  :       {    'var' : 'Max$(GenJet_pt * (abs(GenJet_eta)<2.4  && (Jet_id)))'        ,   'latex':""            },
            #'GenISR_recoil'  :   {   'var' : '(Max$(GenJet_pt * (abs(GenJet_eta)<2.4  && (Jet_id))))/met_genPt'        ,   'latex':""            },
            #'GenISR_dRmin'  :    {   'var' : dRminGenIsr                 ,   'latex':""            },
            #'GenISR_pdgId'  :    {   'var' : pdgIdGenIsr                 ,   'latex':""            },
            'ISR_recoil'     :   {   'var' : '(Max$(Jet_pt * (abs(Jet_eta)<2.4  && (Jet_id))))/met'        ,   'latex':""            },
            'ISR_dRmin'     :    {   'var' : dRminIsr                          ,   'latex':""            },
            'ISR_pdgId'  :       {   'var' : pdgIdIsr                          ,   'latex':""            },
            'ISR_mcFlavour'  :   {   'var' : "Jet_mcFlavour[{isrIndex}]"       ,   'latex':""            },
            'ISR_partonFlavour' :{   'var' : "Jet_partonFlavour[{isrIndex}]"   ,   'latex':""            },
            'ISR_mcMatchFlav'  : {   'var' : "Jet_mcMatchFlav[{isrIndex}]"     ,   'latex':""            },
            'ISR_partonId'     : {   'var' : "Jet_partonId[{isrIndex}]"        ,   'latex':""            },
            'ISR_partonMotherId': {  'var' : "Jet_partonMotherId[{isrIndex}]"  ,   'latex':""            },
            'ISR_qgl'   :       {    'var' : "Jet_qgl[{isrIndex}]"             ,   'latex':""            },
            'nIsr'      :       {    'var' : 'nJet_isrJet{jt}'                 ,   'latex':""            },
            'nHardIsr'  :       {    'var' : 'nJet_isrHJet{jt}'                ,   'latex':""            },
            'nSoftJet'  :       {    'var' : 'nJet_softJet{jt}'                ,   'latex':""            },
            'nHardJet'  :       {    'var' : 'nJet_HardJet{jt}'                ,   'latex':""            },
            'nJet'      :       {    'var' : 'nJet_basJet{jt}'                 ,   'latex':""            },
            'nVetoJet'  :       {    'var' : 'nJet_vetoJet{jt}'                ,   'latex':""            },
            'dPhi'      :       {    'var' : 'dPhi_j1j2_vetoJet{jt}'           ,   'latex':""            },
            'ht'        :       {    'var' : 'ht_basJet{jt}'             ,   'latex':""            },
            'CT1'       :       {    'var' : 'min(met,{ht}-100)'         ,   'latex':""            },
            'CT2'       :       {    'var' : 'min(met,{isrPt}-25)'       ,   'latex':""            },
            'nBSoftJet' :       {    'var' : 'nJet_bJetSoft{jt}'         ,   'latex':""            },
            'nBHardJet' :       {    'var' : 'nJet_bJetHard{jt}'         ,   'latex':""            },
            'nBJet'     :       {    'var' : 'nJet_bJet{jt}'             ,   'latex':""            },

             # leptons
            'nLep'      :       {    'var' : 'n{lepCol}_{lep}{lt}'       ,   'latex':""            }, 
            'nLep_lep'  :       {    'var' : 'n{lepCol}_lep{lt}'       ,   'latex':""            }, 

            'lepIndex'     :     {    'var' : 'Index{lepCol}_{lep}{lt}',   'latex':""            },
            'lepIndex1'    :     {    'var' : '{lepIndex}[0]',   'latex':""            },
            'lepIndex_lep' :     {    'var' : 'Index{lepCol}_lep{lt}',     'latex':""            },
            'lepIndex_veto':     {    'var' : 'Index{lepCol}_lep{lt}',     'latex':""            },
            'lepIndex_lep1':     {    'var' : '{lepIndex_lep}[0]',     'latex':""            },

            'lepIndex2' :       {    'var' : 'Max$(Alt$(Index{lepCol}_{lep}{lt}[1],-999))',   'latex':""            },
            '_lepIndex2' :       {    'var' : 'Max$(Alt$(Index{lepCol}_lep{lt}[1],-999))',   'latex':""            },

            'isFakeFromTau1':       {'var' : '({lepCol}_genPartFlav[{lepIndex1}] == 15)',       'latex':''}, # FIXME: x-check if just matching to prompt taus is sufficient
            'isFakeFromTau_loose1': {'var' : '({lepCol}_genPartFlav[{lepIndex_loose1}] == 15)', 'latex':''}, # FIXME: x-check if just matching to prompt taus is sufficient

            'lepMT'     :       {    'var' : '{lepCol}_mt[{lepIndex1}]'   ,   'latex':""            },
            'lepPt'     :       {    'var' : '{lepCol}_pt[{lepIndex1}]'   ,   'latex':""            },
            'lepPhi'    :       {    'var' : '{lepCol}_phi[{lepIndex1}]'  ,   'latex':""            },
            'lepEta'    :       {    'var' : '{lepCol}_eta[{lepIndex1}]'  ,   'latex':""            },
            'lepPdgId'  :       {    'var' : '{lepCol}_pdgId[{lepIndex1}]',   'latex':""            },
            'lepPdgId_loose'  :       {    'var' : '{lepCol}_pdgId[{lepIndex_loose1}]',   'latex':""            },
            'lepCharge'  :      {    'var' : '{lepCol}_charge[{lepIndex1}]',  'latex':""            },

            # loose leptons
            'lepIndex_loose'  : {    'var' : 'Index{lepCol}_{lep}{looseWP}',   'latex':""            },
            'lepIndex_loose1' : {    'var' : '{lepIndex_loose}[0]',   'latex':""            },
            'lepIndex_lep_loose'  : {'var' : 'Index{lepCol}_lep{looseWP}',   'latex':""            },
            'lepIndex_lep_loose1' : {'var' : '{lepIndex_lep_loose}[0]',   'latex':""            },
            'lepMT_loose'     : {    'var' : '{lepCol}_mt[{lepIndex_loose1}]'   ,   'latex':""            },
            'nLep_loose'      : {    'var' : 'n{lepCol}_{lep}{looseWP}'       ,   'latex':""            }, 
            'lepEta_loose'    : {    'var' : '{lepCol}_eta[{lepIndex_loose1}]'  ,   'latex':""            },
            'lepPt_loose'     : {    'var' : '{lepCol}_pt[{lepIndex_loose1}]'   ,   'latex':""            },

            # tight leptons
            'lepIndex_tight_lep': {    'var' : 'Index{lepCol}_lep{tightWP}',   'latex':""            },
            'lepIndex_tight'  : {    'var' : 'Index{lepCol}_{lep}{tightWP}',   'latex':""            },
            'lepIndex_tight1' : {    'var' : '{lepIndex_tight}[0]',   'latex':""            },
            'lepIndex_lep_tight'  : {    'var' : 'Index{lepCol}_lep{tightWP}',   'latex':""            },
            'lepIndex_lep_tight1' : {    'var' : '{lepIndex_lep_tight}[0]',   'latex':""            },
            'lepMT_tight'     : {    'var' : '{lepCol}_mt[{lepIndex_tight1}]'   ,   'latex':""            },
            'nLep_tight'      : {    'var' : 'n{lepCol}_{lep}{tightWP}'       ,   'latex':""            }, 
            'lepEta_tight'    : {    'var' : '{lepCol}_eta[{lepIndex_tight1}]'  ,   'latex':""            },
            'lepPt_tight'     : {    'var' : '{lepCol}_pt[{lepIndex_tight1}]'   ,   'latex':""            },

            # taus
            'tauId'     : {    'var' : 'Tau_idMVAnewDM'   ,   'latex':""            },

            # MET 
            'met'       :       {    'var' : 'MET_pt'                       ,   'latex':""            },
            'metPt'       :       {    'var' : 'MET_pt'                       ,   'latex':""            },
            'metPhi'   :       {    'var' : 'MET_phi'                   ,   'latex':""            },
            'weight'    :       {    'var' : ''                          ,   'latex':""            },
            
            # Fake rate 
            # MR2
            'tagIndex1' :       {    'var' : 'Index{lepCol}_lep_def[0]',    'latex':"" }, # index of leading tight lepton = tag
            'tagPdgId1':        {    'var' : '{lepCol}_pdgId[{tagIndex1}]',  'latex':""},
            'tagCharge1':       {    'var' : '{lepCol}_charge[{tagIndex1}]',  'latex':""},
            # MR3
            'tagIndex2' :       {    'var' : 'Index{lepCol}_lep_def[1]',    'latex':"" }, # 2 tags 
            'tagPdgId2':        {    'var' : '{lepCol}_pdgId[{tagIndex2}]',  'latex':""},
            'tagCharge2':       {    'var' : '{lepCol}_charge[{tagIndex2}]',  'latex':""},

            # Triggers
            'trig_MET'       : {'var': triggers['MET']                  , 'latex':''},
            'trig_El'        : {'var': triggers['El']                  , 'latex':''},
            'trig_Mu'        : {'var': triggers['Mu']                  , 'latex':''},
            'trig_Lep'       : {'var': triggers['Lep']                  , 'latex':''},
            'trig_Jet'       : {'var': triggers['Jet']                  , 'latex':''},
        }
      
        # year-specific variables 
        if self.settings['year'] == "2017": 
            vars_dict['tauId']['var'] = "Tau_idMVAnewDM2017v2"

        if self.isMVASetup:
            mva_dict = {
                'bdtcut_sr'  :       {     'var' :  self.settings['bdtcut_sr']                       , 'latex':""               },
                'bdtcut_cr'  :       {     'var' :  self.settings['bdtcut_cr']                       , 'latex':""               },
                'mvaId'      :       {     'var' :  self.settings['mvaId']                           , 'latex':""               },
                'mvaIdIndex' :       {     'var' : 'Sum$((mva_methodId=={mvaId}) * Iteration$)' , 'latex':''  },
                 }
            
            self.settings.update(mva_dict)
            vars_dict.update(mva_dict)


        ######################################################################################
        ######################################################################################
        ##                                                                                  ##
        ##                                CUT DEFINITIONS                                   ##
        ##                                                                                  ##
        ######################################################################################
        ######################################################################################

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
                    'MTInc_LnT'         : {'cut': '(1)'                                           , 'latex':'' },
                    'MTa_LnT'           : {'cut': '{lepMT_loose} < {mtCut1}'                               , 'latex':''},
                    'MTb_LnT'           : {'cut': '({lepMT_loose} > {mtCut1}) && ({lepMT_loose} < {mtCut2})'     , 'latex':''},
                    'MTc_LnT'           : {'cut': '{lepMT_loose} > {mtCut2}'                               , 'latex':''},
                    'MTab_LnT'          : {'cut': '{lepMT_loose} < {mtCut2}'                               , 'latex':''},

                    # presel
                    'AntiQCD'           : {'cut': '{dPhi} < 2.5'                                   , 'latex':''},
                    'invAntiQCD'        : {'cut': '({dPhi} > 2.5 || {nVetoJet} <= 1)'              , 'latex':''}, # NOTE: 'OR' required for inclusion of monojet events
                    'trig_MET'          : {'cut': '{trig_MET}'                                , 'latex':''},
                    'trig_El'           : {'cut': '{trig_El}'                                 , 'latex':''},
                    'trig_Mu'           : {'cut': '{trig_Mu}'                                 , 'latex':''},
                    'trig_Lep'          : {'cut': '{trig_Lep}'                                , 'latex':''},
                    'trig_Jet'          : {'cut': '{trig_Jet}'                                , 'latex':''},
                    
                    '3rdJetVeto'        : {'cut': '{nVetoJet} <= 2'                                        , 'latex':'' },
                    'TauVeto'           : {'cut': '(Sum$({tauId} && Tau_pt > 20 && abs(Tau_eta) < 2.4) == 0)'       , 'latex':'' },
                    '1Lep'              : {'cut': 'Sum$({lepCol}_pt[{lepIndex}]>3.5)&&({lepIndex1}=={lepIndex_lep1})' , 'latex':''},
                    #'1Lep'              : {'cut': '({nLep} >= 1 && ({lepIndex1} == {lepIndex_lep1}))' , 'latex':'' },
                    '2ndLep20Veto'      : {'cut': '(Sum$({lepCol}_pt[{lepIndex_veto}]>20)<2)' , 'latex':''},
                    #'1Lep-2ndLep20Veto' : {'cut': '({nLep} >= 1 && {lepPt} > 3.5 && (Sum$({lepCol}_pt[{lepIndex_lep}] > 20) <= 1) && ({lepIndex1} == {lepIndex_lep1}))' , 'latex':''},
                    
                    #'exact1Lep'        : {'cut': '({nLep} == 1 && ({lepIndex1} == {lepIndex_lep1}))' , 'latex':'' },
                    #'1TightLep'        : {'cut': 'Sum$({lepCol}_pt[{lepIndex}]>3.5)&&({lepIndex1}=={lepIndex_lep1})' , 'latex':''},
                    '1LooseLep'         : {'cut': 'Sum$({lepCol}_pt[{lepIndex_lep_loose}]>3.5)&&({lepIndex_loose1}=={lepIndex_lep_loose1})' , 'latex':''},
                    '2ndLep20Veto'      : {'cut': '(Sum$({lepCol}_pt[{lepIndex_lep}]>20)<2)' , 'latex':''},
                    '2ndLep5Veto'       : {'cut': '(Sum$({lepCol}_pt[{lepIndex_lep}]>5)<2)' , 'latex':''},
                    '2ndLooseLep20Veto' : {'cut': '(Sum$({lepCol}_pt[{lepIndex_lep_loose}]>20)<2)' , 'latex':''},
                    '2ndLooseLep5Veto'  : {'cut': '(Sum$({lepCol}_pt[{lepIndex_lep_loose}]>5)<2)' , 'latex':''},
                    'notTight'          : {'cut':  "!Sum$({lepCol}_pt[{lepIndex_tight_lep}]>3.5)" , 'latex': '' } ,         
    
                    'muMediumId'         : {'cut': '((abs({lepPdgId})==11) || (abs({lepPdgId})==13 && ({lepCol}_mediumMuonId[{lepIndex1}])) )' , 'latex':''},
                    'elLooseId'          : {'cut': '((abs({lepPdgId})==11 && ({lepCol}_SPRING15_25ns_v1)>=1) || (abs({lepPdgId})==13))' , 'latex':''},

                    # BTag Regions
                    'BSR1'              : {'cut': '({nBSoftJet} == 0) && ({nBHardJet} == 0)', 'latex':''},
                    'BSR2'              : {'cut': '({nBSoftJet} >= 1) && ({nBHardJet} == 0)', 'latex':''},
                    'BVR'               : {'cut': '({nBSoftJet} == 0) && ({nBHardJet} == 1)', 'latex':''},
                    'BCR'               : {'cut': '({nBJet} >= 2) &&  ({nBHardJet} >= 1)',    'latex':''},
                    
                    'BVR12'             : {'cut': '({nBHardJet} >= 1)',    'latex':''},
                    'BVR1'              : {'cut': '({nBSoftJet} == 0) && ({nBHardJet} >= 1)', 'latex':''},
                    'BVR2'              : {'cut': '({nBSoftJet} >= 1) && ({nBHardJet} >= 1)', 'latex':''},
                    
                    "B0"                : {'cut': '({nBJet} == 0)',                           'latex':""},
                    "B1"                : {'cut': '({nBJet} == 1)',                           'latex':""},
                    "B2"                : {'cut': '({nBJet} == 2)',                           'latex':""},
                    "B1p"               : {'cut': '({nBJet} >= 1)',                           'latex':""},
                    "B2p"               : {'cut': '({nBJet} >= 2)',                           'latex':""},

                    # SR1
                    'ptVL'              : {'cut':'({lepPt} >= 3.5  && {lepPt} < 5)'          ,'latex':''},
                    'ptL'               : {'cut':'({lepPt} >= 5  && {lepPt} < 12)'           ,'latex':''},
                    'ptM'               : {'cut':'({lepPt} >= 12 && {lepPt} < 20)'           ,'latex':''},
                    'ptH'               : {'cut':'({lepPt} >= 20 && {lepPt} < 30)'           ,'latex':''},
                    'lepPt_lt_30'       : {'cut':'{lepPt} < 30'                              ,'latex':''},
                    'lepPt_gt_30'       : {'cut':'{lepPt} > 30'                              ,'latex':''},
                    
                    'lepPt_30to50'      : {'cut':'({lepPt} >= 30  && {lepPt} < 50)'          ,'latex':''},
                    'lepPt_50to80'      : {'cut':'({lepPt} >= 50  && {lepPt} < 80)'          ,'latex':''},
                    'lepPt_80to200'     : {'cut':'({lepPt} >= 80  && {lepPt} < 200)'         ,'latex':''},
                    'lepPt_gt_200'      : {'cut':'({lepPt} >= 200)'                          ,'latex':''},
                    'lepEta_lt_1p5'     : {'cut':'abs({lepEta}) < 1.5'                        ,'latex':''},
                    'lepEta_gt_1p5'     : {'cut':'abs({lepEta}) >= 1.5'                       ,'latex':''},

                    # SR1 LnT
                    'ptVL_LnT'          : {'cut':'({lepPt_loose} >= 3.5  && {lepPt_loose} < 5)'          ,'latex':''},
                    'ptL_LnT'           : {'cut':'({lepPt_loose} >= 5  && {lepPt_loose} < 12)'           ,'latex':''},
                    'ptM_LnT'           : {'cut':'({lepPt_loose} >= 12 && {lepPt_loose} < 20)'           ,'latex':''},
                    'ptH_LnT'           : {'cut':'({lepPt_loose} >= 20 && {lepPt_loose} < 30)'           ,'latex':''},
                    'lepPt_lt_30_LnT'   : {'cut':'{lepPt_loose} < 30'                              ,'latex':''},
                    'lepPt_gt_30_LnT'   : {'cut':'{lepPt_loose} > 30'                              ,'latex':''},

                    'lepPt_30to50_LnT'  : {'cut':'({lepPt_loose} >= 30  && {lepPt_loose} < 50)'          ,'latex':''},
                    'lepPt_50to80_LnT'  : {'cut':'({lepPt_loose} >= 50  && {lepPt_loose} < 80)'          ,'latex':''},
                    'lepPt_80to200_LnT' : {'cut':'({lepPt_loose} >= 80  && {lepPt_loose} < 200)'         ,'latex':''},
                    'lepPt_gt_200_LnT'  : {'cut':'({lepPt_loose} >= 200)'                          ,'latex':''},
                    'lepEta_lt_1p5_LnT'     : {'cut':'abs({lepEta_loose}) < 1.5'                       ,'latex':''},
                    'lepEta_gt_1p5_LnT'     : {'cut':'abs({lepEta_loose}) >= 1.5'                       ,'latex':''},

                    # SR2
                    'ISR100'            : {'cut' : '{nIsr} > 0'                 ,'latex':''},
                    'ISR325'            : {'cut' : '{nHardIsr} > 0'             ,'latex':''},
                    'negLep'            : {'cut' : '({lepPdgId} > 0)'              ,'latex':''},
                    'posLep'            : {'cut' : '({lepPdgId} < 0)'              ,'latex':''},
                    'negLep_LnT'        : {'cut' : '({lepPdgId_loose} > 0)'              ,'latex':''},
                    'posLep_LnT'        : {'cut' : '({lepPdgId_loose} < 0)'              ,'latex':''},
                    'ChargeInc'         : {'cut' : '(1)'              ,'latex':''},

                    # CR
                    'twomu'             : {'cut': '(nLepGood+nLepOther >=2)' , 'latex':'' },
                    #'twomu'             : {'cut': '(nLepGood+nLepOther >=2 && (abs(LepGood_pdgId[0])==13 && abs(LepGood_pdgId[1])==13 ))' , 'latex':'' },
                  
                    # SR
                    'ESR1'               : {'cut': '({CT1} > 300)'                 , 'latex':'' },
                    'ESR2'               : {'cut': '({CT2} > 300)'                 , 'latex':'' },
                    'CT1_300to400'       : {'cut': '({CT1} > 300)&&({CT1} <= 400)' , 'latex':'' },
                    'CT1_400'            : {'cut': '({CT1} > 400)'                 , 'latex':'' },
                    'CT2_300to400'       : {'cut': '({CT2} > 300)&&({CT2} <= 400)' , 'latex':'' },
                    'CT2_400'            : {'cut': '({CT2} > 400)'                 , 'latex':'' },

                    # VR
                    'EVR1'              : {'cut': '({CT1} > 200)&&({CT1} <= 300)' , 'latex':'' },
                    'EVR2'              : {'cut': '({CT2} > 200)&&({CT2} <= 300)' , 'latex':'' },
                    'VL_TEST'           : {'cut': "Flag_Filters&&met_pt>200.&&Jet_pt[IndexJet_basJet_lowpt[0]]>100.&&ht_basJet_def>300.&&dPhi_j1j2_vetoJet_lowpt<2.5&&Sum$(Tau_pt[0]>20.&&abs(Tau_eta)<2.4)==0&&Sum$(LepGood_pt[IndexLepGood_lep_lowpt]>20)<2&&LepGood_pt[IndexLepGood_mu_lowpt[0]]>3.5&&Sum$(Jet_pt[IndexJet_basJet_lowpt]>60)<3&&ht_basJet_def>300.&&met_pt>200.&&!(ht_basJet_def>400.&&met_pt>300.)" , 'latex':''},
                    'VL_TEST_ETACUT'    : {'cut': "Flag_Filters&&met_pt>200.&&Jet_pt[IndexJet_basJet_lowpt[0]]>100.&&ht_basJet_def>300.&&dPhi_j1j2_vetoJet_lowpt<2.5&&Sum$(Tau_pt[0]>20.&&abs(Tau_eta)<2.4)==0&&Sum$(LepGood_pt[IndexLepGood_lep_lowpt]>20)<2&&LepGood_pt[IndexLepGood_mu_lowpt[0]]>3.5&&abs(LepGood_eta[IndexLepGood_mu_lowpt[0]])<1.5&&Sum$(Jet_pt[IndexJet_basJet_lowpt]>60)<3&&ht_basJet_def>300.&&met_pt>200.&&!(ht_basJet_def>400.&&met_pt>300.)" , 'latex':''},

                    # Sideband 
                    'CT2_200'           : {'cut' : '{CT2} > 200'                 ,'latex':''}, # CT2 ISR sideband
                    
                    'ptBin'               : {'cut':'1'           ,'latex':''}, #NOTE: cut updated by other script
                    
                    'pu_gt_20'            : {'cut':'nTrueInt >= 20' ,'latex':''},
                    'pu_lt_20'            : {'cut':'nTrueInt < 20' , 'latex':''},
                    'noCut'               : {'cut':'1' , 'latex':''},
                    
                    ### Fake Rate Cuts ###
                    # Muon_genPartFlav: Flavour of genParticle for MC matching to status==1 muons: 1 = prompt muon (including gamma*->mu mu), 15 = muon from prompt tau, 5 = muon from b, 4 = muon from c, 3 = muon from light or unknown, 0 = unmatched
                    # Electron_genPartFlav: Flavour of genParticle for MC matching to status==1 electrons or photons: 1 = prompt electron (including gamma*->mu mu), 15 = electron from prompt tau, 22 = prompt photon (likely conversion), 5 = electron from b, 4 = electron from c, 3 = electron from light or unknown, 0 = unmatched
                    'fake'              : {'cut' : '{lepCol}_genPartFlav[{lepIndex1}] != 1', 'latex':''}, 
                    'prompt'            : {'cut' : '{lepCol}_genPartFlav[{lepIndex1}] == 1', 'latex':''},
                    
                    'fake_LnT'          : {'cut' : '({isFakeFromTau_loose1}==0)&&({lepCol}_genPartFlav[{lepIndex_loose1}] == 0 || {lepCol}_genPartFlav[{lepIndex_loose1}] == 99 || {lepCol}_genPartFlav[{lepIndex_loose1}] == 100)', 'latex':''},
                    'prompt_LnT'        : {'cut' : '({isFakeFromTau_loose1}==1)||({lepCol}_genPartFlav[{lepIndex_loose1}] != 0 && {lepCol}_genPartFlav[{lepIndex_loose1}] != 99 && {lepCol}_genPartFlav[{lepIndex_loose1}] != 100)', 'latex':''},

                    'fakeGammaVeto'      : {'cut' : '({nLep} > 0) && ((%s) || ((%s) > 0.15))'%(genGammaCondFalse, dRminGamma), 'latex':''},
                    #'fakeTauVeto'       : {'cut' : '({nLep} > 0) && ((%s) || ((%s) > 0.15))'%(genTauCondFalse, dRminTau), 'latex':''},

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
                    
                    # MR1
                    'exact1Lep'         : {'cut':  '{nLep} == 1',   'latex':''},
                    'HT900'             : {'cut' : '{ht} > 900',   'latex':''},
                    'MET_lt_40'         : {'cut' : '{metPt} < 40',   'latex':''},
                    'MT_lt_30'          : {'cut' : '{lepMT} < 30', 'latex':''},
                    'MET_lt_20'         : {'cut' : '{met} < 20',   'latex':''},
                    'MT_lt_20'          : {'cut' : '{lepMT} < 20', 'latex':''},
                    'min3Jets'          : {'cut' : '{nJet}>=3', 'latex':'' },
                   
                    # MR2 and MR3
                    '1Probe'            : {'cut': '{nLep} >= 1',  'latex':''}, # 1 probe
                    'ProbeFlav'         : {'cut': 'abs({lepPdgId}) == abs(LepGood_pdgId[Index{lepCol}_{lep}{lt}[0]])', 'latex':''}, # probe flavour
                    'Tag1Pt_gt_30'      : {'cut': '{lepCol}_pt[{tagIndex1}] > 30',  'latex':''}, # NOTE: Hardcoded for tight leptons
                    'Tag1ID_tight'      : {'cut': '(abs({tagPdgId1}) == 11 && {lepCol}_SPRING15_25ns_v1[{tagIndex1}] >= 4) + (abs({tagPdgId1}) == 13 && {lepCol}_mediumMuonId[{tagIndex1}] >= 1)',  'latex':''}, # NOTE: Hardcoded for tight leptons
                    #'Tag1MT_lt_100'     : {'cut': '{lepCol}_mt[{tagIndex1}] < 100', 'latex':''}, # NOTE: Hardcoded for tight leptons
                    'max2Jets'          : {'cut': '{nJet}<=2', 'latex':'' },
                     #             'looseMuonId': ('looseMuonId', operator.ge, 1),
#                              'SPRING15_25ns_v1': ('SPRING15_25ns_v1', operator.ge, 1), # EG POG Veto ID (no relIsoWithEA cut)

                    # MR2
                    '1Tag1Probe'        : {'cut': 'n{lepCol}_lep{lt} == 2',  'latex':''}, # 1 tag, 1 lepton
                    '1Tag'              : {'cut': 'n{lepCol}_lep_def >= 1',  'latex':''}, # 1 tight tag
                    'ProbeNotTag'       : {'cut': '{lepIndex1} != {tagIndex1}',  'latex':''}, # tag not equal to probe (for loose leptons) 
                    'SS_TagProbe'       : {'cut': '{lepCharge} == {tagCharge1}', 'latex':'' }, 
                    
                    # MR3
                    '3Lep'              : {'cut': 'n{lepCol}_lep{lt} == 3',  'latex':''}, # 2 tags, 1 lepton
                    '2Tags'             : {'cut': 'n{lepCol}_lep_def >= 2',  'latex':''}, # 2 tight tags
                    'Tag2Pt_gt_30'      : {'cut': '{lepCol}_pt[{tagIndex2}] > 30',  'latex':''}, # NOTE: Hardcoded for tight leptons
                    #'Tag2MT_lt_100'     : {'cut': '{lepCol}_mt[{tagIndex2}] < 100', 'latex':''}, # NOTE: Hardcoded for tight leptons
                    
                    'OS_Tag1Tag2'       : {'cut': '{tagCharge1} != {tagCharge2}', 'latex':'' },
                    
                    # MR4
                    'lepPt_gt_50'       : {'cut':'{lepPt} > 50'                              ,'latex':''},
                    
                    'highWeightVeto'    : {'cut' : '(weight_lumi < 5)', 'latex':''},
                    
                    # ISR
                    'ISRinEvt'           : {'cut' : 'Sum$(Jet_isTrueIsr) > 0', 'latex':''},
                    'matchedISR'         : {'cut' : 'Jet_isTrueIsr[0] == 1', 'latex':''},
                    'ISRfromGluon'       : {'cut' : 'abs(Jet_flavIsr[0]) == 21', 'latex':''},
                    #'ISRinEvt'           : {'cut' : 'nIsr > 0', 'latex':''},
                    #'matchedISR'         : {'cut' : '((%s) < 0.3)'%dRminIsr, 'latex':''},
                    #'matchedGenISR'      : {'cut' : '((%s) < 0.3)'%dRminGenIsr, 'latex':''},
                    #'ISRinEvt'           : {'cut' : 'Sum$(%s) >= 3'%genIsrCond, 'latex':''},
                    #'ISRfromGluon'       : {'cut' : 'abs(Jet_mcFlavour[0]) == 21', 'latex':''},
                }
        
        if 'lowpt' in settings['lepTag']:
           cuts_dict['notTight']['cut'] = cuts_dict['notTight']['cut'].replace('def', 'lowpt')

        if self.isMVASetup:
            cuts_dict.update({
                    #MVA
                    'mva_presel_cut'         : {'cut' : 'mva_preselectedEvent[{mvaIdIndex}]' ,'latex':''},
                    'bdt_gt'                 : {'cut' : 'mva_response[{mvaIdIndex}]>{bdtcut_sr}' , 'latex':''},
                    'bdt_lt'                 : {'cut' : 'mva_response[{mvaIdIndex}]<{bdtcut_cr} && mva_response[{mvaIdIndex}] != -99999' , 'latex':''},
                    #'bdt_gt_0p4'            : {'cut' : 'mva_response[{mvaIdIndex}]>0.4'  , 'latex':''},
                    #'bdt_lt_0p4'            : {'cut' : 'mva_response[{mvaIdIndex}]<0.4'  , 'latex':''},
                    #'bdt_gt_0p55'           : {'cut' : 'mva_response[{mvaIdIndex}]>0.55' , 'latex':''},
                    #'bdt_lt_0p55'           : {'cut' : 'mva_response[{mvaIdIndex}]<0.55' , 'latex':''},
                })

        for methtCut in [70, 100, 150, 160, 200, 250, 260, 280, 300, 350, 400]:
            cuts_dict['MET%s'%methtCut] =   {'cut'  :   '{met}>%s'%methtCut , 'latex':''}
            cuts_dict['HT%s'%methtCut]  =   {'cut'  :   '{ht}>%s'%methtCut  , 'latex':''}
            cuts_dict['CT1_%s'%methtCut]  =   {'cut'  :   '{CT1}>%s'%methtCut , 'latex':''}
            cuts_dict['CT2_%s'%methtCut]  =   {'cut'  :   '{CT2}>%s'%methtCut , 'latex':''}
        for cutVal in [100,110]:
            cuts_dict['isrPt%s'%cutVal]={'cut':'{isrPt}>%s'%cutVal, 'latex':''}

        ############# Update Cuts and Vars for MET, JEC and JER variations
    
        if settings.get("corrs"):
            corr_tag = settings.get('corrs')
            jet_corrs     = {
                      'jec_up'     : 'Jet_corr_JECUp{index}  *( 100*(Jet_corr_JER{index}==-99) + Jet_corr_JER{index} )'    ,
                      'jec_central': 'Jet_corr{index}        *( 100*(Jet_corr_JER{index}==-99) + Jet_corr_JER{index} )'    ,
                      'jec_down'   : 'Jet_corr_JECDown{index}*( 100*(Jet_corr_JER{index}==-99) + Jet_corr_JER{index} )'    ,

                      'jer_up'     : 'Jet_corr{index}*  ( 100*(Jet_corr_JER{index}==-99) + Jet_corr_JERUp{index}   ) '      ,
                      'jer_central': 'Jet_corr{index}*  ( 100*(Jet_corr_JER{index}==-99) + Jet_corr_JER{index}     ) '      ,
                      'jer_down'   : 'Jet_corr{index}*  ( 100*(Jet_corr_JER{index}==-99) + Jet_corr_JERDown{index} ) '      ,

                      'genMet'     : 'Jet_pt' ,
                        }
            met_corrs = {

                       #'jec_up'     : ["met_JetEnUp_Pt"   ,"met_JetEnUp_Phi"     ]             ,
                       #'jec_central': ["met_pt"           ,"met_phi"             ]             ,
                       #'jec_down'   : ["met_JetEnDown_Pt" ,"met_JetEnDown_Phi"   ]               ,

                       #'jer_up'     : ["met_JetResUp_Pt"  ,"met_JetResUp_Phi"    ]              ,
                       #'jer_central': ["met_pt"           ,"met_phi"             ]             ,
                       #'jer_down'   : ["met_JetResDown_Pt","met_JetResDown_Phi"  ]                ,

                       'jec_up'     : ["met_JECUp_pt"   ,"met_JECUp_phi"     ]             ,
                       'jec_central': ["met_pt"           ,"met_phi"             ]             ,
                       'jec_down'   : ["met_JECDown_pt" ,"met_JECDown_phi"   ]               ,

                       'jer_up'     : ["met_JERUp_pt"  ,"met_JERUp_phi"    ]              ,
                       'jer_central': ["met_pt"           ,"met_phi"             ]             ,
                       'jer_down'   : ["met_JERDown_pt","met_JERDown_phi"  ]                ,

                        'genMet'    : ['met_genPt', 'met_genPhi'],
                        }
            jet_corr = jet_corrs[corr_tag]
            metPt, metPhi  = met_corrs[corr_tag]

            mt_var = "sqrt(2*{{lepCol}}_pt[{index}]*{{metPt}}*(1-cos( {{lepCol}}_phi[{index}] - {{metPhi}})))"
            #mt_var_temp     = lambda metpt, metphi : mt_var_template_string.format(lepCol=lepCollection,lepIndex=lepIndex, metpt = metpt, metphi = metphi)
            vars_dict.update({
                       'lepMT'        : {    'var' : mt_var.format( index = '{lepIndex1}' )          ,   'latex':""  },
                       'lepMT_loose'  : {    'var' : mt_var.format( index = '{lepIndex_loose1}' )    ,   'latex':""  },
                       'lepMT_tight'  : {    'var' : mt_var.format( index = '{lepIndex_tight1}' )    ,   'latex':""  },
                       'metPt'   : {    'var' : metPt                       ,   'latex':""            },
                       'metPhi'  : {    'var' : metPhi                   ,   'latex':""            },
                             })
            if 'jer' in corr_tag.lower() or 'jec' in corr_tag.lower():
                vars_dict.update({
                    'jet_corr'   : {    'var' : jet_corr.format(index="")       ,   'latex':""            },
                    'jetPt'      : {    'var' : '( {jetRawPt}*( {jet_corr} ) * ( abs(Jet_eta)<2.4  && (Jet_id) ) )'        ,   'latex':""            },
                    'isrPt'      : {    'var' : '(Max$({jetPt}))'        ,   'latex':""            },
                    'ht'         : {    'var' : '(Sum$({jetPt}*({jetPt}>30)))'        ,   'latex':""            },
                    'nVetoJet'   : {    'var' : '(Sum$({jetPt}) > 60)  ' , 'latex':'' },
                    'nJet'       : {    'var' : '(Sum$({jetPt}) > 30)  ' , 'latex':'' },
                    #'isrPt'      : {    'var' : 'Max$({jetRawPt}*({jet_corr}) * (abs(Jet_eta)<2.4  && (Jet_id)) )'        ,   'latex':""            },

                      # 'ht'     : { 'var': ''}

                   })
            cuts_dict.update({
                    'ISR100'     : {    'cut' : '{isrPt} > 100'                 ,'latex':''},
                    'ISR325'     : {    'cut' : '{isrPt} > 325'             ,'latex':''},
                            })
        ######################################################################################
        ######################################################################################
        ##                                                                                  ##
        ##                            BINS AND REGIONS DEFINITIONS                          ##
        ##                                                                                  ##
        ######################################################################################
        ######################################################################################

        regions = collections.OrderedDict()   ### Order matters because of baseCuts
        regions['none']        = {'baseCut': None     , 'cuts': ['noCut']                , 'latex': '' } 

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


        regions['presel_muMediumId']        = {'baseCut': None     , 'cuts': ['MET200', 'ISR100', 'HT300', 'AntiQCD', '3rdJetVeto', 'TauVeto', '1Lep', '2ndLep20Veto' , 'muMediumId' ]                , 'latex': '' } 
        regions['presel_elLooseId']        = {'baseCut': None     , 'cuts': ['MET200', 'ISR100', 'HT300', 'AntiQCD', '3rdJetVeto', 'TauVeto', '1Lep', '2ndLep20Veto' , 'elLooseId' ]                , 'latex': '' } 
        regions['presel_inclep']   = {'baseCut': None     , 'cuts': ['MET200', 'ISR100', 'HT300', 'AntiQCD', '3rdJetVeto', 'TauVeto' ]                        , 'latex': '' } 

        regions['presel_base']   = {'baseCut': None     , 'cuts': ['MET200', 'ISR100', 'HT300', 'AntiQCD', '3rdJetVeto', 'TauVeto', '2ndLep20Veto' ]                        , 'latex': '' } 
        regions['presel']        = {'baseCut': None     , 'cuts': ['MET200', 'ISR100', 'HT300', 'AntiQCD', '3rdJetVeto', 'TauVeto', '1Lep', '2ndLep20Veto' ]                , 'latex': '' } 
        regions['presel_prompt'] = {'baseCut': None     , 'cuts': ['MET200', 'ISR100', 'HT300', 'AntiQCD', '3rdJetVeto', 'TauVeto', '1Lep', '2ndLep20Veto'      ]           , 'latex': '' } 
        regions['presel_LnT']    = {'baseCut': None     , 'cuts': ['MET200', 'ISR100', 'HT300', 'AntiQCD', '3rdJetVeto', 'TauVeto', '1LooseLep', '2ndLep20Veto' ] + LnTCuts , 'latex': '' } 


        regions['presel_EVR1_base']   = {'baseCut': None     , 'cuts': ['EVR1', 'ISR100',  'AntiQCD', '3rdJetVeto', 'TauVeto' , '2ndLep20Veto' ]                          , 'latex': '' } 
        regions['presel_EVR1']        = {'baseCut': None     , 'cuts': ['EVR1', 'ISR100',  'AntiQCD', '3rdJetVeto', 'TauVeto', '1Lep', '2ndLep20Veto' ]                   , 'latex': '' } 
        regions['presel_EVR1_prompt'] = {'baseCut': None     , 'cuts': ['EVR1', 'ISR100',  'AntiQCD', '3rdJetVeto', 'TauVeto', '1Lep', '2ndLep20Veto' ]                   , 'latex': '' } 
        regions['presel_EVR1_LnT']    = {'baseCut': None     , 'cuts': ['EVR1', 'ISR100',  'AntiQCD', '3rdJetVeto', 'TauVeto', '1LooseLep', '2ndLep20Veto' ]   + LnTCuts  , 'latex': '' } 

        regions['presel_EVR2_base']   = {'baseCut': None     , 'cuts': ['EVR2', 'HT300',  'AntiQCD', '3rdJetVeto', 'TauVeto' , '2ndLep20Veto' ]                          , 'latex': '' } 
        regions['presel_EVR2']        = {'baseCut': None     , 'cuts': ['EVR2', 'HT300',  'AntiQCD', '3rdJetVeto', 'TauVeto', '1Lep', '2ndLep20Veto' ]                   , 'latex': '' } 
        regions['presel_EVR2_prompt'] = {'baseCut': None     , 'cuts': ['EVR2', 'HT300',  'AntiQCD', '3rdJetVeto', 'TauVeto', '1Lep', '2ndLep20Veto' ]                   , 'latex': '' } 
        regions['presel_EVR2_LnT']    = {'baseCut': None     , 'cuts': ['EVR2', 'HT300',  'AntiQCD', '3rdJetVeto', 'TauVeto', '1LooseLep', '2ndLep20Veto' ]   + LnTCuts  , 'latex': '' } 

        regions['presel_EVR_base']   = {'baseCut': None     , 'cuts': ['AntiQCD', '3rdJetVeto', 'TauVeto', '2ndLep20Veto' ]                        , 'latex': '' } 
        regions['presel_EVR']        = {'baseCut': None     , 'cuts': ['AntiQCD', '3rdJetVeto', 'TauVeto', '1Lep', '2ndLep20Veto' ]                , 'latex': '' } 
        regions['presel_EVR_prompt'] = {'baseCut': None     , 'cuts': ['AntiQCD', '3rdJetVeto', 'TauVeto', '1Lep', '2ndLep20Veto'      ]           , 'latex': '' } 
        regions['presel_EVR_LnT']    = {'baseCut': None     , 'cuts': ['AntiQCD', '3rdJetVeto', 'TauVeto', '1LooseLep', '2ndLep20Veto' ] + LnTCuts , 'latex': '' } 

        #regions['presel_base_nvtx_gt_20']   = {'baseCut': None     , 'cuts': ['MET200', 'ISR100', 'HT300', 'AntiQCD', '3rdJetVeto', 'TauVeto', '2ndLep20Veto', 'nvtx_gt_20' ]                        , 'latex': '' } 
        #regions['presel_base_nvtx_lt_20']   = {'baseCut': None     , 'cuts': ['MET200', 'ISR100', 'HT300', 'AntiQCD', '3rdJetVeto', 'TauVeto', '2ndLep20Veto', 'nvtx_lt_20' ]                        , 'latex': '' } 
        #regions['presel_BVR_base']   = {'baseCut': None     , 'cuts': ['BVR' , 'AntiQCD', '3rdJetVeto', 'TauVeto', '2ndLep20Veto' ]                        , 'latex': '' } 
        #regions['presel_BVR']        = {'baseCut': None     , 'cuts': ['BVR' , 'AntiQCD', '3rdJetVeto', 'TauVeto', '1Lep', '2ndLep20Veto' ]                , 'latex': '' } 
        #regions['presel_BVR_prompt'] = {'baseCut': None     , 'cuts': ['BVR' , 'AntiQCD', '3rdJetVeto', 'TauVeto', '1Lep', '2ndLep20Veto'      ]           , 'latex': '' } 
        #regions['presel_BVR_LnT']    = {'baseCut': None     , 'cuts': ['BVR' , 'AntiQCD', '3rdJetVeto', 'TauVeto', '1LooseLep', '2ndLep20Veto' ] + LnTCuts , 'latex': '' } 

        regions['r1'   ]       = {'baseCut': 'presel_prompt' , 'cuts': ['CT1_300', 'BSR1', 'lepEta_lt_1p5' ]        , 'latex': '' }
        regions['r1a'  ]       = {'baseCut': 'r1'    , 'cuts': ['negLep', 'MTa']                                    , 'latex': '' }
        regions['r1b'  ]       = {'baseCut': 'r1'    , 'cuts': ['negLep', 'MTb']                                    , 'latex': '' }
        regions['r1c'  ]       = {'baseCut': 'r1'    , 'cuts': ['MTc' ]                                             , 'latex': '' }
        regions['r1ab' ]       = {'baseCut': 'r1'    , 'cuts': ['negLep', 'MTab']                                   , 'latex': '' }
        regions['r2'   ]       = {'baseCut': 'presel_prompt' , 'cuts': ['CT2_300', 'BSR2'  ]                        , 'latex': '' }
        regions['r2_barrel' ]  = {'baseCut': 'r2'     , 'cuts': ['lepEta_lt_1p5' ]        , 'latex': '' }
        regions['r2_endcap' ]  = {'baseCut': 'r2'     , 'cuts': ['lepEta_gt_1p5' ]        , 'latex': '' }



        regions['sr1'   ] = {'baseCut': 'presel_prompt' , 'cuts': ['CT1_300', 'BSR1', 'lepEta_lt_1p5', 'lepPt_lt_30']                                                   , 'latex': '' }
        regions['sr1a'  ] = {'baseCut': 'sr1'    , 'cuts': ['negLep', 'MTa']                                                                                , 'latex': '' }
        regions['sr1b'  ] = {'baseCut': 'sr1'    , 'cuts': ['negLep', 'MTb']                                                                                , 'latex': '' }
        regions['sr1c'  ] = {'baseCut': 'sr1'    , 'cuts': ['MTc' ]                                                                                         , 'latex': '' }
        regions['sr1ab' ] = {'baseCut': 'sr1'    , 'cuts': ['negLep', 'MTab']                                                                               , 'latex': '' }

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
        
        # SR2
        regions['sr2'   ] = {'baseCut': 'presel_prompt' , 'cuts': ['CT2_300', 'BSR2' , 'lepPt_lt_30']                                                    , 'latex': '' }
        #regions['sr2'   ] = {'baseCut': 'presel_prompt' , 'cuts': ['MET300', 'ISR325', 'BSR2' , 'lepPt_lt_30']                                                    , 'latex': '' }
        regions['sr2a'  ] = {'baseCut': 'sr2'    , 'cuts': ['MTa']                                                                                         , 'latex': '' }
        regions['sr2b'  ] = {'baseCut': 'sr2'    , 'cuts': ['MTb']                                                                                         , 'latex': '' }
        regions['sr2c'  ] = {'baseCut': 'sr2'    , 'cuts': ['MTc']                                                                                         , 'latex': '' }
        regions['sr2ab' ] = {'baseCut': 'sr2'    , 'cuts': ['MTab']                                                                                        , 'latex': '' }
        
        regions['sr2vl'  ] = {'baseCut': 'sr2'     , 'cuts': ['ptVL']                                                                               , 'latex': '' }
        regions['sr2l'  ]  = {'baseCut': 'sr2'     , 'cuts': ['ptL']                                                                               , 'latex': '' }
        regions['sr2m'  ]  = {'baseCut': 'sr2'     , 'cuts': ['ptM']                                                                               , 'latex': '' }
        regions['sr2h'  ]  = {'baseCut': 'sr2'     , 'cuts': ['ptH']                                                                               , 'latex': '' }

        regions['sr2vla' ] = {'baseCut': 'sr2a'    , 'cuts': ['ptVL']                                                                               , 'latex': '' }
        regions['sr2la' ]  = {'baseCut': 'sr2a'    , 'cuts': ['ptL']                                                                               , 'latex': '' }
        regions['sr2ma' ]  = {'baseCut': 'sr2a'    , 'cuts': ['ptM']                                                                               , 'latex': '' }
        regions['sr2ha' ]  = {'baseCut': 'sr2a'    , 'cuts': ['ptH']                                                                               , 'latex': '' }
        regions['sr2vlb' ] = {'baseCut': 'sr2b'    , 'cuts': ['ptVL']                                                                               , 'latex': '' }
        regions['sr2lb' ]  = {'baseCut': 'sr2b'    , 'cuts': ['ptL']                                                                               , 'latex': '' }
        regions['sr2mb' ]  = {'baseCut': 'sr2b'    , 'cuts': ['ptM']                                                                               , 'latex': '' }
        regions['sr2hb' ]  = {'baseCut': 'sr2b'    , 'cuts': ['ptH']                                                                               , 'latex': '' }
        regions['sr2vlc' ] = {'baseCut': 'sr2c'    , 'cuts': ['ptVL']                                                                               , 'latex': '' }
        regions['sr2lc' ]  = {'baseCut': 'sr2c'    , 'cuts': ['ptL']                                                                               , 'latex': '' }
        regions['sr2mc' ]  = {'baseCut': 'sr2c'    , 'cuts': ['ptM']                                                                               , 'latex': '' }
        regions['sr2hc' ]  = {'baseCut': 'sr2c'    , 'cuts': ['ptH']                                                                               , 'latex': '' }
        
        regions['sr2vl_barrel' ]  = {'baseCut': 'sr2'     , 'cuts': ['lepEta_lt_1p5', 'ptVL']                                                                               , 'latex': '' }
        regions['sr2l_barrel'  ]  = {'baseCut': 'sr2'     , 'cuts': ['lepEta_lt_1p5', 'ptL']                                                                               , 'latex': '' }
        regions['sr2m_barrel'  ]  = {'baseCut': 'sr2'     , 'cuts': ['lepEta_lt_1p5', 'ptM']                                                                               , 'latex': '' }
        regions['sr2h_barrel'  ]  = {'baseCut': 'sr2'     , 'cuts': ['lepEta_lt_1p5', 'ptH']                                                                               , 'latex': '' }
        
        regions['sr2vl_endcap' ]  = {'baseCut': 'sr2'     , 'cuts': ['lepEta_gt_1p5', 'ptVL']                                                                               , 'latex': '' }
        regions['sr2l_endcap'  ]  = {'baseCut': 'sr2'     , 'cuts': ['lepEta_gt_1p5', 'ptL']                                                                               , 'latex': '' }
        regions['sr2m_endcap'  ]  = {'baseCut': 'sr2'     , 'cuts': ['lepEta_gt_1p5', 'ptM']                                                                               , 'latex': '' }
        regions['sr2h_endcap'  ]  = {'baseCut': 'sr2'     , 'cuts': ['lepEta_gt_1p5', 'ptH']                                                                               , 'latex': '' }



        regions['src' ]  = {'baseCut': 'presel_prompt'    , 'cuts': ['lepPt_lt_30', 'MTc']           , 'latex': '' }
        regions['crc' ]  = {'baseCut': 'presel_prompt'    , 'cuts': ['lepPt_gt_30', 'MTc']           , 'latex': '' }


        regions['sr1aX' ] = {'baseCut': 'sr1a'    , 'cuts': ['MTa', "CT1_300to400"]                                                                               , 'latex': '' }
        regions['sr1bX' ] = {'baseCut': 'sr1b'    , 'cuts': ['MTb', "CT1_300to400"]                                                                               , 'latex': '' }
        regions['sr1cX' ] = {'baseCut': 'sr1c'    , 'cuts': ['MTc', "CT1_300to400"]                                                                               , 'latex': '' }
        regions['sr2aX' ] = {'baseCut': 'sr2a'    , 'cuts': ['MTa', "CT2_300to400"]                                                                               , 'latex': '' }
        regions['sr2bX' ] = {'baseCut': 'sr2b'    , 'cuts': ['MTb', "CT2_300to400"]                                                                               , 'latex': '' }
        regions['sr2cX' ] = {'baseCut': 'sr2c'    , 'cuts': ['MTc', "CT2_300to400"]                                                                               , 'latex': '' }

        regions['sr1aY' ] = {'baseCut': 'sr1a'    , 'cuts': ['MTa', "CT1_400" ]                                                                               , 'latex': '' }
        regions['sr1bY' ] = {'baseCut': 'sr1b'    , 'cuts': ['MTb', "CT1_400" ]                                                                               , 'latex': '' }
        regions['sr1cY' ] = {'baseCut': 'sr1c'    , 'cuts': ['MTc', "CT1_400" ]                                                                               , 'latex': '' }
        regions['sr2aY' ] = {'baseCut': 'sr2a'    , 'cuts': ['MTa', "CT2_400" ]                                                                               , 'latex': '' }
        regions['sr2bY' ] = {'baseCut': 'sr2b'    , 'cuts': ['MTb', "CT2_400" ]                                                                               , 'latex': '' }
        regions['sr2cY' ] = {'baseCut': 'sr2c'    , 'cuts': ['MTc', "CT2_400" ]                                                                               , 'latex': '' }



        #regions['cr1'   ]  = {'baseCut': 'presel_prompt'  , 'cuts': ['CT1_300', 'BSR1', 'lepEta_lt_1p5', 'lepPt_gt_30']                                                   , 'latex': '' }
        #regions['cr1a'  ]  = {'baseCut': 'cr1'     , 'cuts': ['negLep', 'MTa']                                                                               , 'latex': '' }
        #regions['cr1b'  ]  = {'baseCut': 'cr1'     , 'cuts': ['negLep', 'MTb']                                                                               , 'latex': '' }
        #regions['cr1c'  ]  = {'baseCut': 'cr1'     , 'cuts': ['MTc']                                                                                         , 'latex': '' }
        #regions['cr2'   ]  = {'baseCut': 'presel_prompt'  , 'cuts': ['MET300', 'ISR325', 'BSR2' , 'lepPt_gt_30']                                                    , 'latex': '' }
        #regions['cr2_barrel']  = {'baseCut': 'cr2'  , 'cuts': ['MET300', 'ISR325', 'BSR2' , 'lepPt_gt_30', 'lepEta_lt_1p5']                                                    , 'latex': '' }
        #regions['cr2_endcap']  = {'baseCut': 'cr2'  , 'cuts': ['MET300', 'ISR325', 'BSR2' , 'lepPt_gt_30', 'lepEta_gt_1p5']                                                    , 'latex': '' }
        #regions['crtt'  ]  = {'baseCut': 'presel_prompt'  , 'cuts': ['BCR']                                                    , 'latex': '' }

        cr_lep_tags = {
                        '' : '_gt_30',
                    #'_30to80': '_30to80',
                    '_30to50': '_30to50',
                    '_50to80': '_50to80',
                    '_80to200': '_80to200',
                    '_gt_200': '_gt_200',
                        }
        for lpt_tag, lpt_cut_postfix in cr_lep_tags.items():
            regions['cr1'+lpt_tag   ]  = {'baseCut': 'presel_prompt'  , 'cuts': ['CT1_300', 'BSR1', 'lepEta_lt_1p5', 'lepPt%s'%lpt_cut_postfix]                                                   , 'latex': '' }
            regions['cr1a'+lpt_tag  ]  = {'baseCut': 'cr1'+lpt_tag     , 'cuts': ['negLep', 'MTa']                                                                               , 'latex': '' }
            regions['cr1b'+lpt_tag  ]  = {'baseCut': 'cr1'+lpt_tag     , 'cuts': ['negLep', 'MTb']                                                                               , 'latex': '' }
            regions['cr1c'+lpt_tag ]  = {'baseCut': 'cr1'+lpt_tag     , 'cuts': ['MTc']                                                                                         , 'latex': '' }
            #regions['cr2'+lpt_tag   ]  = {'baseCut': 'presel_prompt'  , 'cuts': ['MET300', 'ISR325', 'BSR2' , 'lepPt%s'%lpt_cut_postfix]                                                    , 'latex': '' }
            regions['cr2'+lpt_tag   ]  = {'baseCut': 'presel_prompt'  , 'cuts': [ 'CT2_300', 'BSR2' , 'lepPt%s'%lpt_cut_postfix]                                                    , 'latex': '' }
            regions['cr2_barrel'+lpt_tag]  = {'baseCut': 'cr2'+lpt_tag  , 'cuts': ['lepEta_lt_1p5']                                                    , 'latex': '' }
            regions['cr2_endcap'+lpt_tag]  = {'baseCut': 'cr2'+lpt_tag  , 'cuts': ['lepEta_gt_1p5']                                                    , 'latex': '' }
        regions['crtt']        = {'baseCut': 'presel_prompt'  , 'cuts': ['BCR']   , 'latex': '' }
        crtt_lep_tags = {
                    '_ptVL'    : 'ptVL'           ,
                    '_ptL'     : 'ptL'           ,
                    '_ptM'     : 'ptM'           ,
                    '_ptH'     : 'ptH'           ,
                    #'_30to80' : 'lepPt_30to80'   ,
                    '_30to50' : 'lepPt_30to50',
                    '_50to80' : 'lepPt_50to80',
                    '_80to200': 'lepPt_80to200'  ,
                    '_gt_200' : 'lepPt_gt_200'   ,
                        }
        for lpt_tag, lpt_cut in crtt_lep_tags.items():
            regions['crtt_barrel'+lpt_tag]        = {'baseCut': 'crtt'  , 'cuts': ['lepEta_lt_1p5', lpt_cut]   , 'latex': '' }
            regions['crtt_endcap'+lpt_tag]        = {'baseCut': 'crtt'  , 'cuts': ['lepEta_gt_1p5', lpt_cut]   , 'latex': '' }

        regions['cr_lepPt_gt_30']             = {'baseCut': 'presel_prompt'  , 'cuts': ['lepPt_gt_30']   , 'latex': '' }
        regions['cr_BCR_lepPt_gt_30']         = {'baseCut': 'presel_prompt'  , 'cuts': ['BCR', 'lepPt_gt_30']   , 'latex': '' }
        regions['cr_BSR1_lepPt_gt_30']        = {'baseCut': 'presel_prompt'  , 'cuts': ['BSR1', 'lepPt_gt_30']   , 'latex': '' }
        regions['cr_BSR2_lepPt_gt_30']        = {'baseCut': 'presel_prompt'  , 'cuts': ['BSR2', 'lepPt_gt_30']   , 'latex': '' }
        regions['cr_BVR_lepPt_gt_30']         = {'baseCut': 'presel_prompt'  , 'cuts': ['BVR', 'lepPt_gt_30']   , 'latex': '' }
        regions['cr_BVR1_lepPt_gt_30']        = {'baseCut': 'presel_prompt'  , 'cuts': ['BVR1', 'lepPt_gt_30']   , 'latex': '' }
        regions['cr_BVR2_lepPt_gt_30']        = {'baseCut': 'presel_prompt'  , 'cuts': ['BVR2', 'lepPt_gt_30']   , 'latex': '' }


        ##
        ## Add MT bins for SR2
        ##

        mt_tags = ['a','b','c']
        r2s = ['sr2', 'sr2vl', 'sr2l', 'sr2m', 'sr2h', 'sr2vl_barrel', 'sr2l_barrel', 'sr2m_barrel', 'sr2h_barrel', 'sr2vl_endcap', 'sr2l_endcap', 'sr2m_endcap', 'sr2h_endcap']
        r2s.extend( [r for r in regions if r.startswith('cr2') ] )

        for rname in r2s: 
            main_name  , tags = rname.rsplit("_")[0] , rname.rsplit("_")[1:]
            rtag = '_'.join( tags)
            rtag = '_'+rtag if rtag else rtag
            for mt_tag  in mt_tags:
                #new_region = deepcopy( regions[rname] ) 
                new_name   = main_name + mt_tag + rtag
                new_region = {'baseCut': rname, 'cuts':['MT%s'%mt_tag], 'latex':''}
                regions[new_name] = new_region

        srs   = ['sr1', 'sr2']
        crs   = [ 'cr1','cr2', ]# 'crtt' ]
        srcrs = srs + crs

        #
        # Add Extra CT Bins
        #
        sr_regions = [x for x in regions.keys() if degTools.anyIn(srs, x ) ] 
        ct_bins_dict = {
                   'r1'    : [
                              {'tag':'X' , 'cuts': ['CT1_300to400'] },
                              {'tag':'Y' , 'cuts': ['CT1_400'] },
                             ],
                   'r2'    : [
                               {'tag':'X' , 'cuts': ['CT2_300to400'] },
                               {'tag':'Y' , 'cuts': ['CT2_400'] },
                              ],
                        }
        crtt_extra_bins_dict = {
                   'rtt'    : [
                               {'tag':'X1' , 'cuts': ['CT1_300to400'] },
                               {'tag':'Y1' , 'cuts': ['CT1_400'] },
                               {'tag':'X2' , 'cuts': ['CT2_300to400'] },
                               {'tag':'Y2' , 'cuts': ['CT2_400'] },
                               {'tag':'a' , 'cuts': ['MTa', ] },
                               {'tag':'b' , 'cuts': ['MTb', ] },
                               {'tag':'c' , 'cuts': ['MTc', ] },
                              ],
                  }         

        def addCTTag(r, ct_tag):
            spl = r.split("_")
            st  = spl[0]
            end = "_".join( r.split("_")[1:] )
            end = "_" + end if end else end
            return st + ct_tag + end

        for sr_tag , ct_bins in ct_bins_dict.items() + crtt_extra_bins_dict.items():
            srs_to_use = [ x for x in regions.keys() if sr_tag in x]
            #print sr_tag, srs_to_use
            for sr in srs_to_use:
                for ct_bin in ct_bins:
                    #new_sr_name = sr.rsplit("_")[0] + ct_bin['tag']
                    new_sr_name = addCTTag(sr, ct_bin['tag'])
                    #print new_sr_name
                    VarsCutsWeightsRegions.makeNewRegion( regions, sr, new_sr_name, ct_bin['cuts'] )


    
        #
        # Add LnT regions
        #
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
                     #'lepPt_30to80'  : 'lepPt_30to80_LnT'  ,
                     'lepPt_30to50'  : 'lepPt_30to50_LnT'  ,
                     'lepPt_50to80'  : 'lepPt_50to80_LnT'  ,
                     'lepPt_80to200' : 'lepPt_80to200_LnT' , 
                     'lepPt_gt_200'  : 'lepPt_gt_200_LnT'  ,
                     'lepPt_lt_30': 'lepPt_lt_30_LnT', 
                     'lepEta_lt_1p5'  : 'lepEta_lt_1p5_LnT',
                     'lepEta_gt_1p5'  : 'lepEta_gt_1p5_LnT',
                        'negLep'  : 'negLep_LnT',
                        'posLep'  : 'posLep_LnT',
                         }

        #print regions.keys()
        LnTTag = "_LnT"
        srcr_regions = [x for x in regions.keys() if degTools.anyIn(srcrs+['r1','r2'] , x) ]
        #print srcr_regions
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

        validation_regions = { 
                                 'vr1' : {'baseRegion':'bins_sum' , 'baseCut': 'presel_EVR1', 'prefix':'v1' , 'cutsToRemove' : ['CT1_300', 'CT1_300to400', 'CT1_400', 'CT2_300', 'CT2_300to400', 'CT2_400' ]  } ,
                                 'vr2' : {'baseRegion':'bins_sum' , 'baseCut': 'presel_EVR2', 'prefix':'v2' , 'cutsToRemove' : ['CT1_300', 'CT1_300to400', 'CT1_400', 'CT2_300', 'CT2_300to400', 'CT2_400' ] },
                                 'vrw': {'baseRegion':'bins_mt_sum' , 'baseCut': 'presel_EVR' , 'prefix':'vw' , 'cutsToReplace': {
                                                                                                      'CT1_300' : ['ISR100' , 'EVR1'], 
                                                                                                      'CT2_300' : ['HT300', 'EVR2'],
                                                                                                     },
                                                                                     'regionsToExclude': ['crtt'], 
                                         },
                                 'vrtt': {'baseRegion':'bins_mtct_sum' , 'baseCut': 'presel' , 'prefix':'vtt' , 'cutsToReplace': {
                                                                                                                                        'BSR1':'BVR1',
                                                                                                                                        'BSR2':'BVR2',
                                                                                                                                       } , 
                                                                                                                                    'regionsToExclude': ['crtt'], 
                                         },
                                 'vrb': {'baseRegion':'bins_mtct_sum' , 'baseCut': 'presel' , 'prefix':'vb' , 'cutsToReplace': {
                                                                                                                                        'BSR1':'BVR12',
                                                                                                                                        'BSR2':'BVR12',
                                                                                                                                       } , 
                                                                                                                                    'regionsToExclude': ['crtt'], 
                                         }
                                 #'vr1' : {'baseCut': 'presel_EVR1', 'prefix':'v1' , 'cutsToRemove':['CT1_300']  } ,
                                 #'vr2' : {'baseCut': 'presel_EVR2', 'prefix':'v2' , 'cutsToRemove':['CT2_300'] },
                              }

        ## EVR1 Create VSRs 
        srcr_and_LnT_regions = srcr_regions + [x+LnTTag for x in srcr_regions]

        for vr, vr_info in validation_regions.items():        
            prefix = vr_info.get( 'prefix', vr )
            cutsToRemove = vr_info.get("cutsToRemove", [] )
            cutsToReplace = vr_info.get("cutsToReplace", {} )
            for region in srcr_regions + [x+LnTTag for x in srcr_regions]:
                newRegion = deepcopy(regions[region])
                if "presel" in newRegion['baseCut']:
                    newRegion['baseCut'] = newRegion['baseCut'].replace("presel",  vr_info['baseCut']) 
                elif newRegion['baseCut'] in srcr_and_LnT_regions:
                    newRegion['baseCut'] = prefix + newRegion['baseCut'] 
                for cutName in  newRegion.get('cuts',[]):
                    if cutName in vr_info.get('cutsToRemove', [] ):
                        newRegion['cuts'].remove(cutName)
                    if cutName in cutsToReplace.keys():
                        newCuts = cutsToReplace[cutName]
                        newCuts = newCuts if type(newCuts) == list else [newCuts]
                        oldCutIndex = newRegion['cuts'].index(cutName)
                        newRegion['cuts'] = newRegion['cuts'][:oldCutIndex] + newCuts + newRegion['cuts'][oldCutIndex+1:]
                        #newRegion['cuts'][ newRegion['cuts'].index(cutName) ] = cutsToReplace[cutName]
                regions[prefix+region] = newRegion
        
        regions['bins_sum'  ] = {'baseCut': 'presel_base' , 'regions': [ 'presel_base',
                                                                       'sr1a',  
                                                                       'sr1b',  
                                                                       'sr1c',  
                                                                       'sr2' ,

                                                                       'sr1vla' ,'sr1la' , 'sr1ma', 'sr1ha',
                                                                       'sr1vlb' ,'sr1lb' , 'sr1mb', 'sr1hb',
                                                                       'sr1vlc' ,'sr1lc' , 'sr1mc', 'sr1hc',
 
                                                                       'sr2vl_barrel'  ,'sr2l_barrel'  , 'sr2m_barrel' , 'sr2h_barrel' ,
                                                                       'sr2vl_endcap'  ,'sr2l_endcap'  , 'sr2m_endcap' , 'sr2h_endcap' ,
                                                                       #'cr1a_30to80' , 'cr1b_30to80' , 'cr1c_30to80', 'cr2_barrel_30to80', 'cr2_endcap_30to80' , 
                                                                       'cr1a_30to50' , 'cr1b_30to50' , 'cr1c_30to50', 'cr2_barrel_30to50', 'cr2_endcap_30to50' , 
                                                                       'cr1a_50to80' , 'cr1b_50to80' , 'cr1c_50to80', 'cr2_barrel_50to80', 'cr2_endcap_50to80' , 
                                                                       'cr1a_80to200' , 'cr1b_80to200' , 'cr1c_80to200', 'cr2_barrel_80to200', 'cr2_endcap_80to200' , 
                                                                       'cr1a_gt_200' , 'cr1b_gt_200' , 'cr1c_gt_200', 'cr2_barrel_gt_200', 'cr2_endcap_gt_200' , 
                                                                       'cr1a' , 'cr1b' , 'cr1c', 
                                                                       'cr2_barrel', 'cr2_endcap' , 
                                                                       #'crtt_endcap_30to50', 'crtt_endcap_50to80', 'crtt_endcap_80to200', 'crtt_endcap_gt_200', 'crtt_endcap_ptVL','crtt_endcap_ptL',  'crtt_endcap_ptM', 'crtt_endcap_ptH', 
                                                                       #'crtt_barrel_30to50', 'crtt_barrel_50to80', 'crtt_barrel_80to200', 'crtt_barrel_gt_200', 'crtt_barrel_ptVL','crtt_barrel_ptL',  'crtt_barrel_ptM', 'crtt_barrel_ptH', 
                                                                       #'crtt',


                                                                       'sr1a_LnT',  'sr1vla_LnT' ,'sr1la_LnT' , 'sr1ma_LnT', 'sr1ha_LnT',
                                                                       'sr1b_LnT',  'sr1vlb_LnT' ,'sr1lb_LnT' , 'sr1mb_LnT', 'sr1hb_LnT',
                                                                       'sr1c_LnT',  'sr1vlc_LnT' ,'sr1lc_LnT' , 'sr1mc_LnT', 'sr1hc_LnT',
                                                                       'sr2_LnT' ,  
                                                                       'sr2vl_barrel_LnT'  ,'sr2l_barrel_LnT'  , 'sr2m_barrel_LnT' , 'sr2h_barrel_LnT' ,
                                                                       'sr2vl_endcap_LnT'  ,'sr2l_endcap_LnT'  , 'sr2m_endcap_LnT' , 'sr2h_endcap_LnT' ,
                                                                       #'cr1a_30to80_LnT' , 'cr1b_30to80_LnT' , 'cr1c_30to80_LnT', 'cr2_barrel_30to80_LnT', 'cr2_endcap_30to80_LnT' , 
                                                                       'cr1a_30to50_LnT' , 'cr1b_30to50_LnT' , 'cr1c_30to50_LnT', 'cr2_barrel_30to50_LnT', 'cr2_endcap_30to50_LnT' , 
                                                                       'cr1a_50to80_LnT' , 'cr1b_50to80_LnT' , 'cr1c_50to80_LnT', 'cr2_barrel_50to80_LnT', 'cr2_endcap_50to80_LnT' , 
                                                                       'cr1a_80to200_LnT' , 'cr1b_80to200_LnT' , 'cr1c_80to200_LnT', 'cr2_barrel_80to200_LnT', 'cr2_endcap_80to200_LnT' , 
                                                                       'cr1a_gt_200_LnT' , 'cr1b_gt_200_LnT' , 'cr1c_gt_200_LnT', 
                                                                       'cr2_barrel_gt_200_LnT', 'cr2_endcap_gt_200_LnT' , 
                                                                       #'crtt_endcap_30to50_LnT', 'crtt_endcap_50to80_LnT', 'crtt_endcap_80to200_LnT', 'crtt_endcap_gt_200_LnT', 'crtt_endcap_ptVL_LnT','crtt_endcap_ptL_LnT',  'crtt_endcap_ptM_LnT', 'crtt_endcap_ptH_LnT', 
                                                                       #'crtt_barrel_30to50_LnT', 'crtt_barrel_50to80_LnT', 'crtt_barrel_80to200_LnT', 'crtt_barrel_gt_200_LnT', 'crtt_barrel_ptVL_LnT','crtt_barrel_ptL_LnT',  'crtt_barrel_ptM_LnT', 'crtt_barrel_ptH_LnT', 
                                                                       #'crtt_LnT',
                                                                   ]       , 'latex':''}

        regions['bins_mtct_sum_sig'  ] = {'baseCut': 'presel_base' , 'regions': [ 'presel_base',
                                                                       #'sr1a',  
                                                                       #'sr1b',  
                                                                       #'sr1c',  
                                                                       #'sr2' ,

                                                                       #'sr1vla' ,'sr1la' , 'sr1ma', 'sr1ha',
                                                                       #'sr1vlb' ,'sr1lb' , 'sr1mb', 'sr1hb',
                                                                       #'sr1vlc' ,'sr1lc' , 'sr1mc', 'sr1hc',
 
                                                                       'sr1vlaX' ,'sr1laX' , 'sr1maX', 'sr1haX',
                                                                       'sr1vlbX' ,'sr1lbX' , 'sr1mbX', 'sr1hbX',
                                                                       'sr1vlcX' ,'sr1lcX' , 'sr1mcX', 'sr1hcX',
 
                                                                       'sr1vlaY' ,'sr1laY' , 'sr1maY', 'sr1haY',
                                                                       'sr1vlbY' ,'sr1lbY' , 'sr1mbY', 'sr1hbY',
                                                                       'sr1vlcY' ,'sr1lcY' , 'sr1mcY', 'sr1hcY',
 
                                                                       #'sr2vla' ,'sr2la' , 'sr2ma', 'sr2ha',
                                                                       #'sr2vlb' ,'sr2lb' , 'sr2mb', 'sr2hb',
                                                                       #'sr2vlc' ,'sr2lc' , 'sr2mc', 'sr2hc',
 
                                                                       'sr2vlaX' ,'sr2laX' , 'sr2maX', 'sr2haX',
                                                                       'sr2vlbX' ,'sr2lbX' , 'sr2mbX', 'sr2hbX',
                                                                       'sr2vlcX' ,'sr2lcX' , 'sr2mcX', 'sr2hcX',
 
                                                                       'sr2vlaY' ,'sr2laY' , 'sr2maY', 'sr2haY',
                                                                       'sr2vlbY' ,'sr2lbY' , 'sr2mbY', 'sr2hbY',
                                                                       'sr2vlcY' ,'sr2lcY' , 'sr2mcY', 'sr2hcY',


                                                                      'cr1aX', 'cr2aX', 'cr1aY', 'cr2aY',   
                                                                      'cr1bX', 'cr2bX', 'cr1bY', 'cr2bY',   
                                                                      'cr1cX', 'cr2cX', 'cr1cY', 'cr2cY',   
 
                                                                   ]       , 'latex':''}



        # add CT bins
        base_region = 'bins_sum'
        new_region  = 'bins_ct_sum'
        regions[new_region] = deepcopy( regions[base_region] )
        newRegions  = ['presel']
        regions[new_region]['regions']= newRegions
        old_sum_regions = regions[base_region]['regions']
        for cttag in ['X','Y']:
            for r in old_sum_regions:
                if degTools.anyIn( ct_bins_dict.keys(), r):
                    new_ct_r = addCTTag( r, cttag )
                    r_to_add = new_ct_r
                else:
                    r_to_add = r
                if not r_to_add in newRegions: 
                    newRegions.append( r_to_add )

        # add MT bins
        base_region = 'bins_sum'
        new_region  = 'bins_mt_sum'
        regions[new_region] = deepcopy( regions[base_region] )
        newRegions  = []
        old_sum_regions = regions[base_region]['regions']
        r2s = [r for r in old_sum_regions if 'sr2' in r or 'cr2' in r ] 
        for r in old_sum_regions:
            if not r in r2s:
                newRegions.append(r)
            else:
                for mttag in ['a','b','c']:
                    newbin = addCTTag( r, mttag ) 
                    newRegions.append(newbin) 
        regions[new_region]['regions']= newRegions
         
 
        # add MTCT bins
        base_region = 'bins_mt_sum'
        new_region  = 'bins_mtct_sum'
        regions[new_region] = deepcopy( regions[base_region] )
        newRegions  = ['presel_base', 'presel']
        regions[new_region]['regions']= newRegions
        old_sum_regions = regions[base_region]['regions']
        for r in old_sum_regions:
            if degTools.anyIn( crtt_extra_bins_dict.keys() , r):
                for mttag in mt_tags:
                    new_ct_r = addCTTag( r, mttag )
                    r_to_add = new_ct_r
                    newRegions.append( r_to_add )       
                continue        

            for cttag in ['X','Y']:
                if degTools.anyIn( ct_bins_dict.keys(), r):
                    new_ct_r = addCTTag( r, cttag )
                    r_to_add = new_ct_r
                else:
                    r_to_add = r
                if not r_to_add in newRegions: 
                    newRegions.append( r_to_add )


        for vr, vr_info in validation_regions.items():
            regionsToExclude = vr_info.get("regionsToExclude", [] )
            baseRegion       = vr_info.get("baseRegion", "bins_sum")
            vrname = baseRegion + "_" + vr
            newRegion = deepcopy( regions[baseRegion] )
            newRegion['baseCut'] = newRegion['baseCut'].replace('presel',  vr_info['baseCut'])
            oldRegions = newRegion.pop('regions')
            #newRegion['regions']=[ vr_info['baseCut'] ]
            newRegion['regions']=[ ]
            prefix = vr_info.get( 'prefix', vr )
            for r in oldRegions:
                if degTools.anyIn( regionsToExclude, r):
                    continue
                if 'presel' in r:
                    continue
                    #newRegion['regions'].append( r.replace('presel', vr_info['baseCut'] ))
                else:
                    newRegion['regions'].append( prefix + r )
            regions[vrname] = newRegion

        #regions['bins_sum_v1r'  ] = {'baseCut': 'presel_EVR1_base' , 'regions': [ 'presel_EVR1_base',
        #                                                               'v1sr1a',  'v1sr1vla' ,'v1sr1la' , 'v1sr1ma', 'v1sr1ha',
        #                                                               'v1sr1b',  'v1sr1vlb' ,'v1sr1lb' , 'v1sr1mb', 'v1sr1hb',
        #                                                               'v1sr1c',  'v1sr1vlc' ,'v1sr1lc' , 'v1sr1mc', 'v1sr1hc',
        #                                                               'v1sr2' ,  'v1sr2vl'  ,'v1sr2l'  , 'v1sr2m' , 'v1sr2h' ,
        #                                                               'v1cr1a' , 'v1cr1b' , 'v1cr1c', 'v1cr2' , 'v1crtt',

        #                                                               'v1sr1a_LnT',  'v1sr1vla_LnT' ,'v1sr1la_LnT' , 'v1sr1ma_LnT', 'v1sr1ha_LnT',
        #                                                               'v1sr1b_LnT',  'v1sr1vlb_LnT' ,'v1sr1lb_LnT' , 'v1sr1mb_LnT', 'v1sr1hb_LnT',
        #                                                               'v1sr1c_LnT',  'v1sr1vlc_LnT' ,'v1sr1lc_LnT' , 'v1sr1mc_LnT', 'v1sr1hc_LnT',
        #                                                               'v1sr2_LnT' ,  'v1sr2vl_LnT'  ,'v1sr2l_LnT'  , 'v1sr2m_LnT' , 'v1sr2h_LnT' ,
        #                                                               'v1cr1a_LnT' , 'v1cr1b_LnT' , 'v1cr1c_LnT', 'v1cr2_LnT' , 'v1crtt_LnT',
        #                                                           ]       , 'latex':''}
        #regions['bins_sum_v2r'  ] = {'baseCut': 'presel_EVR2_base' , 'regions': [ 'presel_EVR2_base',
        #                                                               'v2sr1a',  'v2sr1vla' ,'v2sr1la' , 'v2sr1ma', 'v2sr1ha',
        #                                                               'v2sr1b',  'v2sr1vlb' ,'v2sr1lb' , 'v2sr1mb', 'v2sr1hb',
        #                                                               'v2sr1c',  'v2sr1vlc' ,'v2sr1lc' , 'v2sr1mc', 'v2sr1hc',
        #                                                               'v2sr2' ,  'v2sr2vl'  ,'v2sr2l'  , 'v2sr2m' , 'v2sr2h' ,
        #                                                               'v2cr1a' , 'v2cr1b' , 'v2cr1c', 'v2cr2' , 'v2crtt',

        #                                                               'v2sr1a_LnT',  'v2sr1vla_LnT' ,'v2sr1la_LnT' , 'v2sr1ma_LnT', 'v2sr1ha_LnT',
        #                                                               'v2sr1b_LnT',  'v2sr1vlb_LnT' ,'v2sr1lb_LnT' , 'v2sr1mb_LnT', 'v2sr1hb_LnT',
        #                                                               'v2sr1c_LnT',  'v2sr1vlc_LnT' ,'v2sr1lc_LnT' , 'v2sr1mc_LnT', 'v2sr1hc_LnT',
        #                                                               'v2sr2_LnT' ,  'v2sr2vl_LnT'  ,'v2sr2l_LnT'  , 'v2sr2m_LnT' , 'v2sr2h_LnT' ,
        #                                                               'v2cr1a_LnT' , 'v2cr1b_LnT' , 'v2cr1c_LnT', 'v2cr2_LnT' , 'v2crtt_LnT',
        #                                                           ]       , 'latex':''}

        
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

        if self.isMVASetup:
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



        #for vr_name in sidebands.keys():
        #    validation_regions_info = sidebands[vr_name]
        #    validation_regions      = validation_regions_info['sideband_regions']
        #    vr_common               = validation_regions_info['common']
        #    vr_common_name          = validation_regions_info['common_name']
        #    vr_baseCut              = validation_regions_info['baseCut']
        #    if len(vr_baseCut)==1:
        #        pass
        #    elif len(vr_baseCut)==2:
        #        vr_baseCut , vr_baseCut_cutList =  vr_baseCut
        #        regions[vr_baseCut]   = {'baseCut': 'presel'  , 'cuts'    : vr_baseCut_cutList                     , 'latex':''}

        #    #validation_regions_cutlists = [ list(x) for x in itertools.product( *validation_regions ) ] 
        #    validation_regions_cutlists = validation_regions_info['cutLists'] #[ list(x) for x in itertools.product( *validation_regions ) ] 

        #    validation_region_names = []
        #    for cutListNames in validation_regions_cutlists:
        #        sideband_name = '_'.join([vr_common_name] + cutListNames)
        #        validation_region_names.append(sideband_name)
        #        regions[sideband_name] = {'baseCut': vr_baseCut          , 'cuts'    :  vr_common + cutListNames       , 'latex':''}
        #    regions[vr_name]   = {'baseCut': vr_baseCut   , 'regions' :  validation_region_names , 'latex':''}


        #regions['sr1ValidationRegion'] = {'baseCut': 'presel' , 'regions': ["EVR1"] , 'latex':''}



        # VR + BJetVeto + lepEta + [ MT , LepPt, Charge ] 

        regions['EVR1_VL' ]  = {'baseCut': 'presel_EVR1'    , 'cuts': ['ptVL']                                                                               , 'latex': '' }
        regions['VL' ]  = {'baseCut': 'presel'    , 'cuts': ['ptVL']                                                                               , 'latex': '' }

        def makeValidationRegion():
            pass

        ### Fake Rate Regions ###
        
        # Measurement Regions
        
        # MR1
        regions['measurement1_kin']  =    {'baseCut': None,               'cuts': ['HT900', 'MET_lt_40'],  'latex': ''} #'min3Jets' 'MET_lt_20'
        regions['measurement1']  =        {'baseCut': 'measurement1_kin', 'cuts': ['exact1Lep', 'MT_lt_30'], 'latex': ''} # 'MT_lt_20' 
        
        # MR2
        regions['measurement2_kin']  =    {'baseCut': None,               'cuts': ['HT70', 'MET100'],     'latex': ''} #, 'max2Jets'
        regions['measurement2']  =        {'baseCut': 'measurement2_kin', 'cuts': ['1Tag1Probe', '1Tag', 'Tag1Pt_gt_30', '1Probe', 'ProbeNotTag', 'ProbeFlav', 'SS_TagProbe'], 'latex': ''} #'Tag1ID_tight', 
        
        regions['measurement2_BVeto']  =  {'baseCut': 'measurement2', 'cuts': ['BSR1'], 'latex': ''}
        regions['measurement2_BVeto_kin']  = regions['measurement2_kin'] 
        
        # MR3 (based on MR2 but with 2 tags)
        regions['measurement3_kin']  = regions['measurement2_kin'] 
        regions['measurement3']  =        {'baseCut': 'measurement3_kin', 'cuts': ['3Lep', '2Tags', 'Tag1Pt_gt_30', 'Tag2Pt_gt_30', '1Probe', 'ProbeFlav', 'OS_Tag1Tag2'], 'latex': ''}
        
        # MR4 (based on MR1)
        regions['measurement4_kin']  =    {'baseCut': None,               'cuts': ['MET_lt_40', 'ISR100'],  'latex': ''}
        regions['measurement4']  =        {'baseCut': 'measurement4_kin', 'cuts': ['exact1Lep', 'lepPt_gt_50', 'MT_lt_30'], 'latex': ''}
        
        # Application Region
        regions['sr1_kin']  =  {'baseCut': None, 'cuts': ['MET200', 'ISR100', 'HT300', 'AntiQCD', '3rdJetVeto', 'TauVeto', 'CT1_300'], 'latex': ''} 
        regions['sr1a_kin'] = regions['sr1b_kin'] = regions['sr1c_kin'] = regions['sr1ab_kin'] = regions['sr1_kin']
        regions['sr2_kin']  =  {'baseCut': None, 'cuts': ['MET200', 'ISR100', 'HT300', 'AntiQCD', '3rdJetVeto', 'TauVeto', 'CT2_300'], 'latex': '' }
        
        if self.isMVASetup:
            regions['srBDT_kin'] = {'baseCut': None, 'cuts': ['MET280', 'HT200', 'isrPt110', 'AntiQCD', '3rdJetVeto'], 'latex': ''} 
            regions['crBDT_kin'] = regions['BDT_kin'] = regions['srBDT_kin'] 
 
            regions['srBDT'] =     {'baseCut': 'presel_mvaTrain', 'cuts': ['bdt_gt'], 'latex': ''}
            regions['crBDT'] =     {'baseCut': 'presel_mvaTrain', 'cuts': ['bdt_lt'], 'latex': ''}
            regions['BDT'] =       regions['presel_mvaTrain']

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
                    'looseWP'   :       {    'var' : looseWP                                 ,   'latex':""            },
                    'lepIndex1'  :       {    'var' : 'Index{lepCol}_{lep}{lt}[0]',   'latex':""            },
   

                    'lepIndex_loose'      : {    'var' : 'Index{lepCol}_{lep}{looseWP}',   'latex':""            },
                    'lepIndex_loose1'     : {    'var' : '{lepIndex_loose}[0]',   'latex':""            },
                    'lepIndex_lep_loose'  : {    'var' : 'Index{lepCol}_lep{looseWP}',   'latex':""            },
                    'lepIndex_lep_loose1' : {    'var' : '{lepIndex_lep_loose}[0]',   'latex':""            },

                    '2ndLep20Veto'      : {'var': '(Sum$({lepCol}_pt[{lepIndex_lep}]>20)<2)' , 'latex':''},
                    '2ndLep5Veto'       : {'var': '(Sum$({lepCol}_pt[{lepIndex_lep}]>5)<2)' , 'latex':''},
                    '2ndLooseLep20Veto' : {'var': '(Sum$({lepCol}_pt[{lepIndex_lep_loose}]>20)<2)' , 'latex':''},
                    '2ndLooseLep5Veto'  : {'var': '(Sum$({lepCol}_pt[{lepIndex_lep_loose}]>5)<2)' , 'latex':''},

 
                    'noweight'  :  {'var': "(1)",                                            "latex":""},
                    'weight_lumi'    :  {'var': "weight_lumi",                                            "latex":""},
    
                    'isr_Wpt'     : {'var': 'weight_isr_Wpt'                                  ,               "latex":""},
                    'isr_Wpt_LnT' : {'var': wpt_weight_a.replace("{wpt}","{wpt_loose}")   ,               "latex":""}, # FIXME
                    #'wpt_p' : {'var': wpt_weight_p  ,               "latex":""},
                    #'wpt_n' : {'var': wpt_weight_n  ,               "latex":""},
    
                    #'wpt'         : {'var':  "(sqrt(({lepCol}_pt[max(0,{lepIndex1}[0])]*cos({lepCol}_phi[max(0,{lepIndex1}[0])]) + met_pt*cos(met_phi) ) **2 + ( {lepCol}_pt[max(0,{lepIndex1}[0])]*sin({lepCol}_phi[max(0,{lepIndex1}[0])])+met_pt*sin(met_phi) )^2 ))",               "latex":""},
                    'wpt'             : {'var': "{lepCol}_Wpt[{lepIndex1}]",                "latex":""},
                    'wpt_loose'       : {'var': "{lepCol}_Wpt[{lepIndex_loose1}]",                "latex":""},
    
                    'top1pt'      :  {'var': "Max$(GenPart_pt*(GenPart_pdgId==6))",               "latex":""},
                    'top2pt'      :  {'var': "Max$(GenPart_pt*(GenPart_pdgId==-6))",                "latex":""},
                    'ttpt'        :  {'var': "1.24*exp(0.156-0.5*0.00137*({top1pt}+{top2pt}))",               "latex":""},
                    'trigeff'     :  {'var': "{p0}*0.5*(1+TMath::Erf(({x}-{p1})/{p2}))".format( **trig_eff_params) ,                "latex":""},
                    'lepSF'       :  {'var': "{lepCol}_SF[{lepIndex1}]"     ,                "latex":""},
                    'lepSFLoose'  :  {'var': "{lepCol}_SF[{lepIndex_loose1}]"     ,                "latex":""},

                    'lepSFFix'       :  {'var': "LepGood_sftot[{lepIndex1}]"     ,                "latex":""},
                    'lepSFFixLoose'  :  {'var': "LepGood_sftot[{lepIndex_loose1}]"     ,                "latex":""},
                    #'lepTkSF'     :  {'var': "(GetLepTkEff( LepGood_pdgId[{ind}], LepGood_eta[{ind}]*(abs(LepGood_pdgId[{ind}])==13) +  (LepGood_etaSc[{ind}]*LepGood_etaSc[{ind}]!=0 + LepGood_eta[{ind}]*(LepGood_etaSc[{ind}]==0))*(abs(LepGood_pdgId[{ind}])==11), LepGood_pt[{ind}] ) <0.8 )".format(ind="{lepIndex1}")     ,                "latex":""},


                    #"elDblCorr"       : {'var' : "GetElDblCntCorr( LepGood_pdgId[{lepIndex1}], LepGood_eta[{lepIndex1}], LepGood_pt[{lepIndex1}] )"                                                    , "latex":""    },        
                    #"lepTkSF"         : {'var' : "GetLepTkEff( LepGood_pdgId[{lepIndex1}], LepGood_etaSc[{lepIndex1}], LepGood_eta[{lepIndex1}], LepGood_pt[{lepIndex1}])"                             , "latex":""    },            
                    #"elDblCorrLoose"  : {'var' : "GetElDblCntCorr( LepGood_pdgId[{lepIndex_loose1}], LepGood_eta[{lepIndex_loose1}], LepGood_pt[{lepIndex_loose1}] )"                                  , "latex":""    },                    
                    #"lepTkSFLoose"    : {'var' : "GetLepTkEff( LepGood_pdgId[{lepIndex_loose1}], LepGood_etaSc[{lepIndex_loose1}], LepGood_eta[{lepIndex_loose1}], LepGood_pt[{lepIndex_loose1}])"     , "latex":""    },                    

                    #"lepSFTot"        : {'var' : "{lepSF}*{elDblCorr}*{lepTkSF}"                , "latex":""},
                    #"lepSFTotLoose"   : {'var' : "{lepSFLoose}*{elDblCorrLoose}*{lepTkSFLoose}" , "latex":""},

    
                    #"isrNormFact" : {'var': "(7.279e-05 *(GenSusyMStop) + 1.108)",               "latex":""},
                    "isrNormFactM17" : {'var': "(6.974e-05 *(GenSusyMStop) + 1.086)",               "latex":""},
                    #"isr"   : {'var': "{isrNormFact} * ( (nIsr==0) + (nIsr==1)*0.882  + (nIsr==2)*0.792  + (nIsr==3)*0.702  + (nIsr==4)*0.648  + (nIsr==5)*0.601  + (nIsr>=6)*0.515 ) ",               "latex":""},
                    "isr_sig"     : {'var': "({isrNormFactM17} * (%s))"%isr_reweight.format( **moriond17_isr_reweight_params) , 'latex':''},

                    "isr_nIsr"      : {'var': "weight_isr_nIsr" , 'latex':''},
                    #"isr_nIsr"      : {'var': "({isrNormFact_tt} * (%s))"%isr_reweight.format( **moriond17_isr_reweight_params) , 'latex':''},
                    "isrNormFact_tt" : {'var': "(1.071)",               "latex":""},
                    "pu"          : {'var': "puWeight",                                        "latex":""},
                    "pu_up"       : {'var': "puWeight_up",                                        "latex":""},
                    "pu_down"     : {'var': "puWeight_down",                                        "latex":""},
    
                    'bTagSF'      : {'var': "{sf}{jt}",                                            "latex":""},
                    'BSR1'        : {'var': "(weightBTag0_{bTagSF})"  ,                         "latex":""},
                    'BSR2'        : {'var': "(weightSBTag1p_{bTagSF} * weightHBTag0_{bTagSF})",                                     "latex":""},
                    'BCR'         : {'var': "(weightHBTag1p_{bTagSF}-(weightSBTag0_{bTagSF}*weightHBTag1_{bTagSF}))",               "latex":""},
                    'BVR12'       : {'var': "( weightHBTag1p_{bTagSF} )",                                     "latex":""},
                    'BVR'         : {'var': "( weightSBTag0_{bTagSF}  * weightHBTag1_{bTagSF})",                                     "latex":""},
                    'BVR1'        : {'var': "( weightSBTag0_{bTagSF}  * weightHBTag1p_{bTagSF} )",                                     "latex":""},
                    'BVR2'        : {'var': "( weightSBTag1p_{bTagSF} * weightHBTag1p_{bTagSF} )",                                     "latex":""},
    
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

                    'nvtx_gt_20'        : {'var' : '(nTrueInt>=20)', 'latex':''},
                    'nvtx_lt_20'        : {'var' : '(nTrueInt<20)', 'latex':''},

                    'isSTBartch': {'var':"(((Sum$(GenPart_pdgId == -6 && GenPart_motherId==-9999)==1 ) &&Sum$(abs(GenPart_pdgId)==24 && GenPart_motherId==-9999)==0))", 'latex':'' },
                    'STBarCorr' : {'var':"({isSTBartch}*(80.95/136.02 - 1) + 1)" , 'latex':'' },

                    })
    
        lumis = settings['lumis']
        
        for lumi_name, lumi in lumis[settings['year']].items():
            if lumi_name not in weights_dict:
                weights_dict[lumi_name] = {'var' : "(%s/lumi_norm)"%(settings['lumis'][settings['year']][lumi_name]), 'latex':''}

        lhe_order = {
                        0: 'Q2central_central'   ,     ## <weight id="1001"> muR=1 muF=1 
                        1: 'Q2central_up'        ,     ## <weight id="1002"> muR=1 muF=2 
                        2: 'Q2central_down'      ,     ## <weight id="1003"> muR=1 muF=0.5 
                        3: 'Q2up_central'        ,     ## <weight id="1004"> muR=2 muF=1 
                        4: 'Q2up_up'             ,     ## <weight id="1005"> muR=2 muF=2 
                        5: 'Q2up_down'           ,     ## <weight id="1006"> muR=2 muF=0.5 
                        6: 'Q2down_central'      ,     ## <weight id="1007"> muR=0.5 muF=1 
                        7: 'Q2down_up'           ,     ## <weight id="1008"> muR=0.5 muF=2 
                        8: 'Q2down_down'         ,     ## <weight id="1009"> muR=0.5 muF=0.5 
                      }
        lheWeights = {
                        'Q2central_central': '(1.0)*(LHEweight_wgt[%s])'%0,
                        'Q2central_up'     : '(1.062e+00 + ( 1.817e-04 * (GenSusyMStop)) + ( -9.773e-08 * (GenSusyMStop)*(GenSusyMStop) ) )*(LHEweight_wgt[%s])  '%1,
                        'Q2central_down'   : '(9.394e-01 + ( -1.747e-04 * (GenSusyMStop)) + ( 9.838e-08 * (GenSusyMStop)*(GenSusyMStop) ) )*(LHEweight_wgt[%s])  '%2,
                        'Q2up_central'     : '(1.217e+00 + ( -1.113e-04 * (GenSusyMStop)) + ( 6.175e-08 * (GenSusyMStop)*(GenSusyMStop) ) )*(LHEweight_wgt[%s])  '%3,
                        #'Q2up_up'          : '(1.294e+00 + ( 9.238e-05 * (GenSusyMStop)) + ( -4.909e-08 * (GenSusyMStop)*(GenSusyMStop) ) )*(LHEweight_wgt[%s])  '%4
                        'Q2up_down'        : '(1.142e+00 + ( -3.070e-04 * (GenSusyMStop)) + ( 1.733e-07 * (GenSusyMStop)*(GenSusyMStop) ) )*(LHEweight_wgt[%s])  '%5,
                        'Q2down_central'   : '(8.039e-01 + ( 9.310e-05 * (GenSusyMStop)) + ( -5.135e-08 * (GenSusyMStop)*(GenSusyMStop) ) )*(LHEweight_wgt[%s])  '%6,
                        'Q2down_up'        : '(8.524e-01 + ( 2.537e-04 * (GenSusyMStop)) + ( -1.366e-07 * (GenSusyMStop)*(GenSusyMStop) ) )*(LHEweight_wgt[%s])  '%7,
                        #'Q2down_down'      : '(7.564e-01 + ( -6.149e-05 * (GenSusyMStop)) + ( 3.450e-08 * (GenSusyMStop)*(GenSusyMStop) ) )*(LHEweight_wgt[%s])  '%8,
                       }
        for lheWeightName, lheWeightString in lheWeights.items():
             weights_dict[lheWeightName] = {'var':lheWeightString, 'latex':''}

        #for iLHEWeight, lheWeight in lhe_order.items():
        #        lheWeightString     = "LHEWeights_wgt[%s]"%iLHEWeight
        #        lheWeightNormalized = "((%s)*(%s))"%(lheWeightNorms[lheWeight],lheWeightString)
        #        weights_dict[lheWeight]= {'var':lheWeightNormalized , 'latex': '' }

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
                                    'if_this_cut_in_list'  : 'remove_the_cut_and_add_this_weight_to_weightList'
                                         }
        """

        cut_weight_options = {
                            "prompt"  : { "sample_list" : lambda sample: not sample.isSignal and not  sample.isData
                                                                           ,                 "cut_options":{
                                                                                                "1Lep"       : promptCuts   ,
                                                                                                "1LooseLep"  : promptLnTCuts      ,
                                                                                               }
                                        },
                            "lepSF"     : { "sample_list" : lambda sample: not  sample.isData
                                                                           ,                 "weight_options":{
                                                                                                "1Lep"       : 'lepSF'      ,
                                                                                                "1LooseLep"  : 'lepSFLoose'      ,
                                                                                               }
                                          },
                            #"lepsftot"  : { "sample_list" : lambda sample: not  sample.isData
                            #                                               ,                 "weight_options":{
                            #                                                                    "1Lep"       : 'lepSFTot'      ,
                            #                                                                    "1LooseLep"  : 'lepSFTotLoose'      ,
                            #                                                                   }
                            #              },
                            "lepsffix"  : { "sample_list" : lambda sample: not  sample.isData
                                                                           ,                 "weight_options":{
                                                                                                "1Lep"       : 'lepSFFix'      ,
                                                                                                "1LooseLep"  : 'lepSFFixLoose'      ,
                                                                                               }
                                          },
                            "trig_eff"  : { "sample_list" : lambda sample: not  sample.isData
                                                                           ,                 "weight_options":{
                                                                                                "default"    : "trigeff"      ,
                                                                                                #"1Lep"       : 'trigeff'      ,
                                                                                                #"1LooseLep"  : 'trigeff'      ,
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
                            "isr_Wpt"   : { "sample_list" : ["WJets"] ,                 "weight_options":{
                                                                                                  #"default"    : "wpt_a",
                                                                                                  "1Lep"       : "isr_Wpt",
                                                                                                  "1LooseLep"  : "isr_Wpt_LnT",
                                                                                                  #"negLep"   : "wpt_n",
                                                                                                  #"posLep"   : "wpt_p",
                                                                                               }
                                      },
                            
                            "isr_nIsr"    : { "sample_list" :["TTJets", "TT_1l", "TT_2l"],       'weight_options' : {
                                                                                                  "default":"isr_nIsr"
                                                                                                 }
                                       },
                            "ttpt"  : { "sample_list" :['TT_pow' ] ,                'weight_options' : { "default": "ttpt" } },
                            "sf"    : { "sample_list" : None,                        'weight_options' : {
                                                                                                   "BCR":"BCR",
                                                                                                   "BVR1":"BVR1",
                                                                                                   "BVR2":"BVR2",
                                                                                                   "BVR":"BVR",
                                                                                                   "BSR1":"BSR1",
                                                                                                   "BSR2":"BSR2",
                                                                                                   "BVR12":"BVR12",
                                                                                                 }
                                       },
                            "isr_sig"    : { "sample_list" :["T2tt", "T2bW"],            'weight_options' : {
                                                                                                  "default":"isr_sig"
                                                                                                 }          
                                       },
                            "lepveto"    : { "sample_list" : lambda sample: True,            'cut_options' : {  
                                                                                                  #"2ndLep20Veto":[ "2ndLep5Veto"],
                                                                                                  "1Lep": ["2ndLep5Veto"],
                                                                                                  "1LooseLep": ["2ndLooseLep5Veto"],
                                                                                                 }
                                       },
                            "STXSECFIX"   : { "sample_list" : lambda sample: sample['name'] == 'Single top',
                                                                                               "weight_options":{
                                                                                                "default"  : "STBarCorr",
                                                                                               },
                                            },
                            "medmu"        : { "sample_list" : lambda sample: True,
                                                                                               "cut_options":{
                                                                                                "default"  : "muMediumId",
                                                                                               },
                                            },
                            "nohiwgt"        : { "sample_list" : lambda sample: not sample.isData and not sample.isSignal,
                                                                                               "weight_options":{
                                                                                                "default"  : "nohiwgt",
                                                                                               },
                                            },
                            "nvtx_gt_20"   : { "sample_list" : lambda sample: not sample.isData ,
                                                                                            "weight_options":{
                                                                                                "default"  : "nvtx_gt_20",
                                                                                               }
                                      },
                            "nvtx_lt_20"   : { "sample_list" : lambda sample: not sample.isData ,
                                                                                            "weight_options":{
                                                                                                "default"  : "nvtx_lt_20",
                                                                                               }
                                      },
                         }
        for lheWeightName, lheWeightString in lheWeights.items():
            lheWeightOption = { "sample_list" : lambda sample: sample.isSignal   ,            'weight_options' : {
                                                                                                  "default": lheWeightName
                                                                                                 }
                                       }
            cut_weight_options[lheWeightName] = lheWeightOption

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
        
        self.weights_dict   =   weights_dict
        self.vars_dict      =   vars_dict
        self.cuts_dict      =   cuts_dict
        self.regions        =   regions
        self.cut_weight_options =   cut_weight_options
