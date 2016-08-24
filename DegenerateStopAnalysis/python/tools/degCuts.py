import math
from Workspace.DegenerateStopAnalysis.tools.degTools import CutClass, joinCutStrings, splitCutInPt, btw, less, more
from Workspace.DegenerateStopAnalysis.tools.btag_sf_map import BTagSFMap 

## --------------------------------------------------------------
##                           Variables
## --------------------------------------------------------------

minAngle = lambda phi1, phi2 : "TMath::Min( (2*pi) - abs({phi1}-{phi2}) , abs({phi1}-{phi2}) )".format(phi1=phi1,phi2=phi2)  


## --------------------------------------------------------------
##                            CUT LISTS
## --------------------------------------------------------------

lepCollection = "LepGood"

class Cuts():
    def __init__( self,  lepCollection="LepGood" , lep="mu", sr1c_opt = "reload" , isrpt=110, btag = 'btag' ):
        """
        sr1c_opt = [ "reload" , "MT95" , "MT95_IncCharge", "MT105_IncCharge_CT250" ]

        """
        if btag == 'btag':
            sf = 'sf'
        else:
            sf = btag
        btag_sf_map = BTagSFMap(btag)

        self.collection = lepCollection
        self.lep = lep 
        lepIndex = "Index{lepCol}_{Lep}".format(lepCol=lepCollection, Lep=lep)




        #self.presel_common = presel_common
        """
        cutdict["B1"] = "nBJet==1"
        cutdict["B1p"] = "nBJet>0"
        cutdict["B2"] = "nBJet==2"
        cutdict["Bsr2"] = "nBHardJet==0&&nBSoftJet>0"
        cutdict["Bcrb0"] = "nBHardJet>0&&nBJet==2"
        cutdict["Bcrb12"] = "nBHardJet>0"
        cutdict["Bcrb02"] = "nBHardJet0&&nBJet>1"
        cutdict["Bcrb01"] = "nBHardJet==1&&nBSoftJet==0"


        weightdict["BV"] = "weightSBTag0_SF*weightHBTag0_SF"
        weightdict["B1"] = "((weightSBTag1_SF*weightHBTag0_SF)+(weightSBTag0_SF*weightHBTag1_SF))"
        weightdict["B1p"] = "(1.-(weightSBTag0_SF*weightHBTag0_SF))"
        weightdict["B2"] = "((weightSBTag2_SF*weightHBTag0_SF)+(weightSBTag1_SF*weightHBTag1_SF)+(weightSBTag0_SF*weightHBTag2_SF))"
        weightdict["Bsr2"] = "weightHBTag0_SF*weightSBTag1p_SF"
        weightdict["Bcrb0"] = "((weightSBTag1_SF*weightHBTag1_SF)+(weightSBTag0_SF*weightHBTag2_SF))"
        weightdict["Bcrb12"] = "weightHBTag1p_SF"
        weightdict["Bcrb02"] = "(weightHBTag1p_SF-(weightSBTag0_SF*weightHBTag1_SF))"
        weightdict["Bcrb01"] = "weightSBTag0_SF*weightHBTag1_SF"
        """




        if btag == 'btag':
            veto_soft_bjet          = btag_sf_map.btag_veto_soft_bjet       #'(nBSoftJet == 0 )'
            one_soft_bjet           = btag_sf_map.btag_one_soft_bjet        #'(nBSoftJet == 1 )'
            one_or_more_soft_bjet   = btag_sf_map.btag_one_or_more_soft_bjet#'(nBSoftJet >= 1 )'
            veto_hard_bjet          = btag_sf_map.btag_veto_hard_bjet       #'(nBHardJet == 0 )'
            one_hard_bjet           = btag_sf_map.btag_one_hard_bjet        #'(nBHardJet == 1 )'
            one_or_more_hard_bjet   = btag_sf_map.btag_one_or_more_hard_bjet#'(nBHardJet >= 1 )'
            veto_bjet               = btag_sf_map.btag_veto_bjet            #'(  nBJet   == 0 )'
            one_bjet                = btag_sf_map.btag_one_bjet             #'(  nBJet   == 1 )'
            one_or_more_bjet        = btag_sf_map.btag_one_or_more_bjet     #'(  nBJet   >= 1 )'
            two_or_more_bjet        = btag_sf_map.btag_two_or_more_bjet     #'(  nBJet   >= 2 )'

            sr1_bjet                = btag_sf_map.btag_sr1_bjet             # veto_bjet 
            sr2_bjet                = btag_sf_map.btag_sr2_bjet             # "( (nBSoftJet>=1) && (nBHardJet==0) )"
            cr1_bjet                = btag_sf_map.btag_cr1_bjet             # veto_bjet
            cr2_bjet                = btag_sf_map.btag_cr2_bjet             # "( (nBSoftJet>=1) && (nBHardJet==0)  )"
            crtt1_bjet              = btag_sf_map.btag_crtt1_bjet           # "( (nBSoftJet==0) && (nBHardJet==1)  )"
            crtt2_bjet              = btag_sf_map.btag_crtt2_bjet           # "( (nBJet>=2)     && (nBHardJet>=1) )"
            


        else: # btag == 'sf':
            veto_soft_bjet          = btag_sf_map.sf_veto_soft_bjet           #'(weightSBTag0_SF)' 
            one_soft_bjet           = btag_sf_map.sf_one_soft_bjet            #'(weightSBTag1_SF)' 
            one_or_more_soft_bjet   = btag_sf_map.sf_one_or_more_soft_bjet    #'(weightSBTag1p_SF)'
            veto_hard_bjet          = btag_sf_map.sf_veto_hard_bjet           #'(weightHBTag0_SF)' 
            one_hard_bjet           = btag_sf_map.sf_one_hard_bjet            #'(weightHBTag1_SF)' 
            one_or_more_hard_bjet   = btag_sf_map.sf_one_or_more_hard_bjet    #'(weightHBTag1p_SF)'
            veto_bjet               = btag_sf_map.sf_veto_bjet                #'(weightBTag0_SF)'   
            one_bjet                = btag_sf_map.sf_one_bjet                 #'(weightBTag1_SF)'   
            one_or_more_bjet        = btag_sf_map.sf_one_or_more_bjet         #'(weightBTag1p_SF)'  
            two_or_more_bjet        = btag_sf_map.sf_two_or_more_bjet         #'(weightBTag2p_SF)'  
                                                                              #
            sr1_bjet                = btag_sf_map.sf_sr1_bjet                 # veto_bjet 
            sr2_bjet                = btag_sf_map.sf_sr2_bjet                 # "(weightSBTag1p_SF * weightHBTag0_SF)" 
            cr1_bjet                = btag_sf_map.sf_cr1_bjet                 # veto_bjet
            cr2_bjet                = btag_sf_map.sf_cr2_bjet                 # "(weightSBTag1p_SF * weightHBTag0_SF)" #"( (nBSoftJet>=1) && (nBHardJet==0)  )"
            crtt1_bjet              = btag_sf_map.sf_crtt1_bjet               # "(weightSBTag0_SF  * weightHBTag1_SF)" #"( (nBSoftJet==0) && (nBHardJet==1)  )"
            crtt2_bjet              = btag_sf_map.sf_crtt2_bjet               # "(weightHBTag1p_SF-(weightSBTag0_SF*weightHBTag1_SF))"#"( (nBJet>=2)     && (nBHardJet>=1) )"

        #else:
        #    raise   Exception("btag option not recongized: %s"%btag)



        #self.presel_noAntiQCD = CutClass ("PreselNoAntiQCD", [
        self.presel_noAntiQCD = CutClass ("MET200_ISR%s_HT300"%isrpt, [
                                      ["MET200","met>200"],
                                      ["ISR110","nIsrJet>=1" ],
                                      #["ISR%s"%isrpt,"nBasJet>=0 && Jet_pt[IndexJet_basJet[0]] > %s"%isrpt ],
                                      ["HT300","ht_basJet>300"],
                                      #["No3rdJet60","nVetoJet<3"],
                                      #["TauElVeto","(Sum$(TauGood_idMVA)==0) && (Sum$(abs(LepGood_pdgId)==11 && LepGood_SPRING15_25ns_v1==1)==0)"],
                                      #["1Mu-2ndMu20Veto", "(nLepGood_mu==1 || (nLepGood_mu ==2 && LepGood_pt[IndexLepGood_mu[1]] < 20) )"],
                                     ],
                        baseCut=None,
                        )
        
        
        
        self.presel_antiQCD = CutClass ("presel_antiQCD", [
                                      ["AntiQCD", " (vetoJet_dPhi_j1j2 < 2.5)" ], # old
                                      ["No3rdJet60","nVetoJet<=2"],
                                     ],
                        baseCut=None,
                        )
        
        self.presel_common = CutClass('presel_common', [], baseCut=None)
        self.presel_common.add( self.presel_noAntiQCD )
        self.presel_common.add( self.presel_antiQCD   )











   
        lepSelCuts = [
                                      ["TauVeto","(Sum$(TauGood_idMVANewDM && TauGood_pt > 20 )==0)".format(lepCol=lepCollection)],
                                      ["1{lep}-2nd{lep}20Veto".format(lep=lep.title()), "(n{lepCol}_{lep}==1 || (n{lepCol}_{lep} ==2 && {lepCol}_pt[{lepIndex}[1]] < 20) )".format(lepCol=lepCollection, lepIndex=lepIndex , lep=lep)]
                      ]
    
        #elVeto =               ["ElVeto","( Sum$(abs({lepCol}_pdgId)==11      && {lepCol}_SPRING15_25ns_v1>=1  && {lepCol}_pt > 20)==0)".format(lepCol=lepCollection)]
        #muVeto =               ["MuVeto","( nLepGood_mu == 0  || (nLepGood_mu==1  && LepGood_pt[IndexLepGood_mu[0]] < 20) )".format(lepCol=lepCollection)       ]
        otherLepVetoCutString   =    "( n{lepCol}_{otherLep}  == 0  || (n{lepCol}_{otherLep}==1 && {lepCol}_pt[Index{lepCol}_{otherLep}[0]] < 20) )"


        if lep == 'mu':
            otherLepVeto = ['ElVeto', otherLepVetoCutString.format(lepCol = lepCollection , otherLep='el') ]
            #otherLepVeto = elVeto
        elif lep =='el':
            otherLepVeto = ['MuVeto', otherLepVetoCutString.format(lepCol = lepCollection , otherLep='mu') ]
            #otherLepVeto = muVeto
        elif lep == 'lep':
            otherLepVeto = None
        else:
            raise Exception("Lep should be either one of mu,el,lep but it was %s"%lep)

        if otherLepVeto:
            lepSelCuts.insert(1,otherLepVeto)

        


        self.lepSel = CutClass ("{lep}Sel".format(lep=lep),  lepSelCuts, 
                                baseCut=self.presel_common,
                                )
        
        
        self.presel = CutClass('presel', [], baseCut=None)
        self.presel.add(self.presel_common)
        self.presel.add(self.lepSel)
        
        
        
        
        self.sr1IncCharge   = CutClass ("SR1IncCharge",    [
                                      ["CT300","min(met,ht_basJet-100) > 300 "],
                                      #["Veto Soft BJet",veto_soft_bjet],
                                      #["Veto Hard BJet",veto_hard_bjet],
                                      ["Veto BJets",veto_bjet],
                                      ["{lep}Eta1.5".format(lep=lep.title()),"abs({lepCol}_eta[{lepIndex}[0]])<1.5".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                      ["{lep}Pt30".format(lep=lep.title()),"{lepCol}_pt[{lepIndex}[0]]<30".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                   ] , 
                          baseCut = self.presel,
                          )

        self.negCharge = CutClass("NegCharge", [
                                      ["neg{lep}".format(lep=lep.title()),"({lepCol}_pdgId[{lepIndex}[0]]==13 || {lepCol}_pdgId[{lepIndex}[0]]==11 )".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                   ] , 
                          baseCut = self.sr1IncCharge,
                          )
        self.posCharge = CutClass("PosCharge", [
                                      ["pos{lep}".format(lep=lep.title()),"({lepCol}_pdgId[{lepIndex}[0]]==-13 || {lepCol}_pdgId[{lepIndex}[0]]==-11 )".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                   ] , 
                          baseCut = self.sr1IncCharge,
                          )


        self.sr1   = CutClass ("SR1",    [] , baseCut = self.presel )
        self.sr1.add(self.sr1IncCharge)
        self.sr1.add(self.negCharge)


        self.sr2      = CutClass ("SR2",   [ 
                                        ["ISR325","nIsrHJet>0"],
                                        ["Met300","met>300"],
                                        #["At Least 1 Soft BJet", one_or_more_soft_bjet],
                                        #["No Hard BJet",veto_hard_bjet],
                                        ["1 or More Soft but no Hard BJet", sr2_bjet],
                                        ["{lep}Pt_lt_30".format(lep=lep.title()),"{lepCol}_pt[{lepIndex}[0]]<30".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                      ],
                          baseCut = self.presel,
                          )
        
        
        
        
        
        self.sr1CT250   = CutClass ("SR1_CT250",    [
                                      ["CT250","min(met,ht_basJet-100) > 250 "],
                                      #["Veto Soft BJet",veto_soft_bjet],
                                      #["Veto Hard BJet",veto_hard_bjet],
                                      ["Veto BJet",veto_bjet],
                                      ["neg{lep}".format(lep=lep.title()),"({lepCol}_pdgId[{lepIndex}[0]]==13 || {lepCol}_pdgId[{lepIndex}[0]]==11 )".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                      ["{lep}Eta1.5".format(lep=lep.title()),"abs({lepCol}_eta[{lepIndex}[0]])<1.5".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                      ["{lep}Pt30".format(lep=lep.title()),"{lepCol}_pt[{lepIndex}[0]]<30".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                   ] , 
                          baseCut = self.presel,
                          )

        self.sr1CT200   = CutClass ("SR1_CT200",    [
                                      ["CT200","min(met,ht_basJet-100) > 200 "],
                                      #["Veto Soft BJet",veto_soft_bjet],
                                      #["Veto Hard BJet",veto_hard_bjet],
                                      ["Veto BJet",veto_bjet],
                                      ["neg{lep}".format(lep=lep.title()),"({lepCol}_pdgId[{lepIndex}[0]]==13 || {lepCol}_pdgId[{lepIndex}[0]]==11 )".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                      ["{lep}Eta1.5".format(lep=lep.title()),"abs({lepCol}_eta[{lepIndex}[0]])<1.5".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                      ["{lep}Pt30".format(lep=lep.title()),"{lepCol}_pt[{lepIndex}[0]]<30".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                   ] , 
                          baseCut = self.presel,
                          )




        self.sr1IncChargeCT300   = CutClass ("SR1IncChargeCT300",    [
                                      ["CT300","min(met,ht_basJet-100) > 300 "],
                                      #["Veto Soft BJet",veto_soft_bjet],
                                      #["Veto Hard BJet",veto_hard_bjet],
                                      ["Veto BJet",veto_bjet],
                                      ["{lep}Eta1.5".format(lep=lep.title()),"abs({lepCol}_eta[{lepIndex}[0]])<1.5".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                      ["{lep}Pt30".format(lep=lep.title()),"{lepCol}_pt[{lepIndex}[0]]<30".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                   ] , 
                          baseCut = self.presel,
                          )
        self.sr1IncChargeCT250   = CutClass ("SR1IncChargeCT250",    [
                                      ["CT250","min(met,ht_basJet-100) > 250 "],
                                      #["Veto Soft BJet",veto_soft_bjet],
                                      #["Veto Hard BJet",veto_hard_bjet],
                                      ["Veto BJet",veto_bjet],
                                      ["{lep}Eta1.5".format(lep=lep.title()),"abs({lepCol}_eta[{lepIndex}[0]])<1.5".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                      ["{lep}Pt30".format(lep=lep.title()),"{lepCol}_pt[{lepIndex}[0]]<30".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                   ] , 
                          baseCut = self.presel,
                          )
        self.sr1IncChargeCT200   = CutClass ("SR1IncChargeCT200",    [
                                      ["CT200","min(met,ht_basJet-100) > 200 "],
                                      #["Veto Soft BJet",veto_soft_bjet],
                                      #["Veto Hard BJet",veto_hard_bjet],
                                      ["Veto BJet",veto_bjet],
                                      ["{lep}Eta1.5".format(lep=lep.title()),"abs({lepCol}_eta[{lepIndex}[0]])<1.5".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                      ["{lep}Pt30".format(lep=lep.title()),"{lepCol}_pt[{lepIndex}[0]]<30".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                   ] , 
                          baseCut = self.presel,
                          )

        # sr1 no eta, incCharge
        #self.sr1IncChargeIncEtaCT300   = CutClass ("SR1IncChargeIncEtaCT300",    [
        #                              ["CT300","min(met,ht_basJet-100) > 300 "],
        #                              ["BVeto","(nBSoftJet == 0 && nBHardJet ==0)"],
        #                              ["{lep}Pt30".format(lep=lep.title()),"{lepCol}_pt[{lepIndex}[0]]<30".format(lepCol=lepCollection, lepIndex=lepIndex)],
        #                           ] , 
        #                  baseCut = self.presel,
        #                  )

        #self.sr1IncChargeIncEtaCT250   = CutClass ("SR1IncChargeIncEtaCT250",    [
        #                              ["CT250","min(met,ht_basJet-100) > 250 "],
        #                              ["BVeto","(nBSoftJet == 0 && nBHardJet ==0)"],
        #                              ["{lep}Pt30".format(lep=lep.title()),"{lepCol}_pt[{lepIndex}[0]]<30".format(lepCol=lepCollection, lepIndex=lepIndex)],
        #                           ] , 
        #                  baseCut = self.presel,
        #                  )
        #self.sr1IncChargeIncEtaCT200   = CutClass ("SR1IncChargeIncEtaCT200",    [
        #                              ["CT200","min(met,ht_basJet-100) > 200 "],
        #                              ["BVeto","(nBSoftJet == 0 && nBHardJet ==0)"],
        #                              ["{lep}Pt30".format(lep=lep.title()),"{lepCol}_pt[{lepIndex}[0]]<30".format(lepCol=lepCollection, lepIndex=lepIndex)],
        #                           ] , 
        #                  baseCut = self.presel,
        #                  )

        


        if sr1c_opt.lower() == "reload":
            mt = [ 60, 88  ]
            sr1c_baseCut = self.sr1
        elif sr1c_opt == "MT95":
            mt = [ 60, 95  ]
            #sr1c_baseCut = self.sr1CT300
            sr1c_baseCut = self.sr1
        elif sr1c_opt == "MT95_IncCharge":
            mt = [ 60, 95  ]
            sr1c_baseCut = self.sr1IncChargeCT300
        elif sr1c_opt == "MT105_IncCharge_CT250":
            mt = [ 60, 105 ]    
            sr1c_baseCut = self.sr1IncChargeCT250
        else:
            raise Exception("sr1c_opt not recongized %s"%sr1c_opt)

        self.sr1c_baseCut = sr1c_baseCut

        mts = {
                'mt0' : mt[0],
                'mt1' : mt[1],
                #'mt2' : mt[0],
              }
        self.mtabc   = CutClass ("MTabc",    [
                                       ["MTa","{lepCol}_mt[{lepIndex}[0]]< {mt0}".format(lepCol=lepCollection, lepIndex=lepIndex, **mts )],
                                       ["MTb",btw("{lepCol}_mt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex), mt[0],mt[1] )],
                                       ["MTc","{lepCol}_mt[{lepIndex}[0]]> {mt1}".format(lepCol=lepCollection, lepIndex=lepIndex, **mts )],
                                   ] , 
                          baseCut = self.sr1,
                          )
        self.mtabc_pt = splitCutInPt(self.mtabc)


        #self.sr1abc   = CutClass ("SR1abc",    [
        #                               ["SR1a","{lepCol}_mt[{lepIndex}[0]]<{mt0}".format(lepCol=lepCollection, lepIndex=lepIndex, **mts)],
        #                               ["SR1b",btw("{lepCol}_mt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex),mt[0],mt[1])],
        #                               ["SR1c","{lepCol}_mt[{lepIndex}[0]]>{mt1}".format(lepCol=lepCollection, lepIndex=lepIndex, **mts)],
        #                           ] , 
        #                  baseCut = self.sr1,
        #                  )
        
        self.sr1ab_ptbin   = CutClass ("SR1ab_PtBinned",    [
                                       #["SR1a","{lepCol}_mt[{lepIndex}[0]]<{mt0}"],
                                          ["SRL1a",joinCutStrings(   ["{lepCol}_mt[{lepIndex}[0]]<{mt0}".format(lepCol=lepCollection, lepIndex=lepIndex, **mts),         btw("{lepCol}_pt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex),5,12)]  )],
                                          ["SRH1a",joinCutStrings(   ["{lepCol}_mt[{lepIndex}[0]]<{mt0}".format(lepCol=lepCollection, lepIndex=lepIndex, **mts),         btw("{lepCol}_pt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex),12,20)] )],
                                          ["SRV1a",joinCutStrings(   ["{lepCol}_mt[{lepIndex}[0]]<{mt0}".format(lepCol=lepCollection, lepIndex=lepIndex, **mts),         btw("{lepCol}_pt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex),20,30)] )],
                                       #["SR1b",btw("{lepCol}_mt[{lepIndex}[0]]",mt[0],mt[1])],
                                          ["SRL1b",joinCutStrings(   [btw("{lepCol}_mt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex),mt[0],mt[1]), btw("{lepCol}_pt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex),5,12)]  )],
                                          ["SRH1b",joinCutStrings(   [btw("{lepCol}_mt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex),mt[0],mt[1]), btw("{lepCol}_pt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex),12,20)] )],
                                          ["SRV1b",joinCutStrings(   [btw("{lepCol}_mt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex),mt[0],mt[1]), btw("{lepCol}_pt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex),20,30)] )],
                                       #["SR1c","{lepCol}_mt[{lepIndex}[0]]>{mt1}"],
                                   ] , 
                          baseCut = self.sr1,
                          )




        self.sr1c_ptbin     = CutClass ("SR1C_PtBinned",  [
                                       ["SRL1c",joinCutStrings(   ["{lepCol}_mt[{lepIndex}[0]]>{mt1}".format(lepCol=lepCollection, lepIndex=lepIndex, **mts),         btw("{lepCol}_pt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex),5,12)]  )],
                                       ["SRH1c",joinCutStrings(   ["{lepCol}_mt[{lepIndex}[0]]>{mt1}".format(lepCol=lepCollection, lepIndex=lepIndex, **mts),         btw("{lepCol}_pt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex),12,20)] )],
                                       ["SRV1c",joinCutStrings(   ["{lepCol}_mt[{lepIndex}[0]]>{mt1}".format(lepCol=lepCollection, lepIndex=lepIndex, **mts),         btw("{lepCol}_pt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex),20,30)] )],
                                    ], 
                          baseCut = self.sr1c_baseCut
                          )

        self.sr1abc_ptbin   = CutClass ("SR1abc_PtBinned",    [], baseCut= self.presel )
        self.sr1abc_ptbin.add( self.sr1ab_ptbin, baseCutString = self.sr1.inclCombined )
        self.sr1abc_ptbin.add( self.sr1c_ptbin,  baseCutString = self.sr1c_baseCut.inclCombined )
        
        
        
        self.sr1a   = CutClass ("SR1a",    [
                                       ["SR1a","{lepCol}_mt[{lepIndex}[0]]<{mt0}".format(lepCol=lepCollection, lepIndex=lepIndex, **mts)],
                                   ] , 
                          baseCut = self.sr1,
                          )
        
        
        self.sr1b   = CutClass ("SR1b",    [
                                       ["SR1b",btw("{lepCol}_mt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex),mt[0],mt[1])],
                                   ] , 
                          baseCut = self.sr1,
                          )
        
        
        self.sr1c   = CutClass ("SR1c",    [
                                       ["SR1c","{lepCol}_mt[{lepIndex}[0]]>{mt1}".format(lepCol=lepCollection, lepIndex=lepIndex, **mts)],
                                   ] , 
                          baseCut = sr1c_baseCut,
                          )
        
        self.sr1cNegCharge   = CutClass ("SR1cNegCharge",    [
                                       ["SR1cNegCharge","{lepCol}_mt[{lepIndex}[0]]>{mt1}".format(lepCol=lepCollection, lepIndex=lepIndex, **mts)],
                                   ] , 
                          baseCut = self.negCharge,
                          )
        self.sr1cPosCharge   = CutClass ("SR1cPosCharge",    [
                                       ["SR1cPosCharge","{lepCol}_mt[{lepIndex}[0]]>{mt1}".format(lepCol=lepCollection, lepIndex=lepIndex, **mts)],
                                   ] , 
                          baseCut = self.posCharge,
                          )
        
        self.sr2_ptbin   = CutClass ("SR2_PtBinned",    [
                                          ["SRL2",  btw("{lepCol}_pt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex),5,12)    ],
                                          ["SRH2",  btw("{lepCol}_pt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex),12,20)   ],
                                          ["SRV2",  btw("{lepCol}_pt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex),20,30)   ],
                                   ] , 
                          baseCut = self.sr2,
                          )
        self.srl1c   = CutClass ("SR1c",    [
                                       ["SR1c","{lepCol}_mt[{lepIndex}[0]]>{mt1}".format(lepCol=lepCollection, lepIndex=lepIndex, **mts)],
                                       ["SRL2",  btw("{lepCol}_pt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex),5,12)    ],
                                   ] , 
                          baseCut = sr1c_baseCut,
                          )
        self.srh1c   = CutClass ("SR1c",    [
                                       ["SR1c","{lepCol}_mt[{lepIndex}[0]]>{mt1}".format(lepCol=lepCollection, lepIndex=lepIndex, **mts)],
                                       ["SRH2",  btw("{lepCol}_pt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex),12,20)   ],
                                   ] , 
                          baseCut = sr1c_baseCut,
                          )
        self.srv1c   = CutClass ("SR1c",    [
                                       ["SR1c","{lepCol}_mt[{lepIndex}[0]]>{mt1}".format(lepCol=lepCollection, lepIndex=lepIndex, **mts)],
                                       ["SRV2",  btw("{lepCol}_pt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex),20,30)   ],
                                   ] , 
                          baseCut = sr1c_baseCut,
                          )
        self.srh1c_neg_nj2   = CutClass ("SR1c_neg_nj2",    [
                                       ["SR1c","{lepCol}_mt[{lepIndex}[0]]>{mt1}".format(lepCol=lepCollection, lepIndex=lepIndex, **mts)],
                                       ["SRH2",  btw("{lepCol}_pt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex),12,20)   ],
                                       ["neg{lep}".format(lep=lep.title()),"({lepCol}_pdgId[{lepIndex}[0]]==13 || {lepCol}_pdgId[{lepIndex}[0]]==11 )".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                       ["nj2"   ,  "nBasJet==2"],
                                       #["SRH2"  ,  btw("{lepCol}_pt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex),12,20)   ],
                                   ] , 
                          baseCut = sr1c_baseCut,
                          )
        
        self.srs_ptbin   = CutClass ("SRs_PtBinned",    [], baseCut= self.presel ) 
        self.srs_ptbin.add( self.sr1ab_ptbin ,  baseCutString = self.sr1.inclCombined          )
        self.srs_ptbin.add( self.sr1c_ptbin  ,  baseCutString = self.sr1c_baseCut.inclCombined )
        self.srs_ptbin.add( self.sr2_ptbin   ,  baseCutString = self.sr2.inclCombined          )


        self.srs_ptbin_sum   = CutClass ("SRs_PtBinnedSum",    [], baseCut= self.presel ) 
        self.srs_ptbin_sum.add( self.sr1ab_ptbin ,  baseCutString = self.sr1.inclCombined          )
        self.srs_ptbin_sum.add( self.sr1c_ptbin  ,  baseCutString = self.sr1c_baseCut.inclCombined )
        self.srs_ptbin_sum.add( self.sr2_ptbin   ,  baseCutString = self.sr2.inclCombined          )
        self.srs_ptbin_sum.add(   self.sr1a          , baseCutString =  self.sr1.combined           )
        self.srs_ptbin_sum.add(   self.sr1b          , baseCutString =  self.sr1.combined           )
        self.srs_ptbin_sum.add(   self.sr1c          , baseCutString =  self.sr1c_baseCut.combined  )
        self.srs_ptbin_sum.add(   self.sr2   ,'inclCombinedList'     , baseCutString =  self.sr2.baseCut.combined  )

        ################################################################################################
        ####################################                 ###########################################
        #################################### Control Regions ###########################################
        ####################################                 ###########################################
        ################################################################################################

        #self.cr1MuCut    = CutClass ( "cr1MuCut", [
        #                              ["{lep}Eta1.5".format(lep=lep.title()),"abs({lepCol}_eta[{lepIndex}[0]])<1.5".format(lepCol=lepCollection, lepIndex=lepIndex)],
        #                              ["{lep}Pt30".format(lep=lep.title()),"{lepCol}_pt[{lepIndex}[0]]>30".format(lepCol=lepCollection, lepIndex=lepIndex)],
        #                    ],
        #                    baseCut= self.presel,
        #                )
        
        self.cr1c_baseCut = CutClass( self.sr1c_baseCut.name.replace("SR","CR") , 
                                      self.sr1c_baseCut.inclList[:-1] + # ["{lep}Pt30".format(lep=lep.title()),"{lepCol}_pt[{lepIndex}[0]]>30".format(lepCol=lepCollection, lepIndex=lepIndex)] ], 
                                      [  ["{lep}Pt30".format(lep=lep.title()),"{lepCol}_pt[{lepIndex}[0]]>30".format(lepCol=lepCollection, lepIndex=lepIndex)] ], 
                                      baseCut = self.presel
                                     )

        
        self.cr1Loose    = CutClass ( "cr1Loose", [
                                      ["CT200","min(met,ht_basJet-100) > 200 "],
                                      #["CT300","min(met,ht_basJet-100) > 300 "],
                                      #["Veto Soft BJet",veto_soft_bjet],
                                      #["Veto Hard BJet",veto_hard_bjet],
                                      ["Veto BJet",veto_bjet],

                                      ["neg{lep}".format(lep=lep.title()),"({lepCol}_pdgId[{lepIndex}[0]]==13 || {lepCol}_pdgId[{lepIndex}[0]]==11 )".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                      ["{lep}Eta1.5".format(lep=lep.title()),"abs({lepCol}_eta[{lepIndex}[0]])<1.5".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                      ["{lep}Pt30".format(lep=lep.title()),"{lepCol}_pt[{lepIndex}[0]]>30".format(lepCol=lepCollection, lepIndex=lepIndex)],
                            ],
                            baseCut= self.presel,
                        )
        
        
        self.crtt1    = CutClass ( "CRTT1", [
                              #["No Soft BJets", veto_soft_bjet],
                              #["Exactly 1 Hard BJet", one_hard_bjet],
                              ["0 Soft 1 Hard BJet", crtt1_bjet],
                                     ],
                            baseCut= self.presel ,
                        )
        self.crtt2    = CutClass ( "CRTT2", [
                              #["2 or more BJets", two_or_more_bjet],
                              #["At least 1 Hard BJet", one_or_more_hard_bjet],
                              ["2p Soft 1 Hard BJet", crtt2_bjet],
                                     ],
                            baseCut= self.presel ,
                        )
        
        self.cr1IncCharge   = CutClass ("CR1IncCharge",    [
                                      ["CT300","min(met,ht_basJet-100) > 300 "],
                                      ["{lep}Pt_gt_30".format(lep=lep.title()),"{lepCol}_pt[{lepIndex}[0]]>30".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                      #["Veto Soft BJet",veto_soft_bjet],
                                      #["Veto Hard BJet",veto_hard_bjet],
                                      ["Veto BJet",veto_bjet],
                                      ["{lep}Eta1.5".format(lep=lep.title()),"abs({lepCol}_eta[{lepIndex}[0]])<1.5".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                      #["neg{lep}".format(lep=lep.title()),"( {lepCol}_pdgId[{lepIndex}[0]]==13 || {lepCol}_pdgId[{lepIndex}[0]]==11  )".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                      #["BVeto_Medium25","nBJetMedium25==0"],
                                      #["HT400 ","ht_basJet>400"],
                                      #["met300","met>300"],
                                   ] , 
                          baseCut = self.presel,
                          )


        self.cr1   = CutClass ("CR1",    [] , baseCut = self.presel )
        self.cr1.add(self.cr1IncCharge)
        self.cr1.add(self.negCharge)


        
        
        self.cr1abc   = CutClass ("CR1abc",    [
                                       ["CR1a", "{lepCol}_mt[{lepIndex}[0]]<{mt0}".format(lepCol=lepCollection, lepIndex=lepIndex, **mts)],
                                       ["CR1b", btw("{lepCol}_mt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex),mt[0],mt[1])],
                                       ["CR1c", "{lepCol}_mt[{lepIndex}[0]]>{mt1}".format(lepCol=lepCollection, lepIndex=lepIndex, **mts)],
                                   ] , 
                          baseCut = self.cr1,
                          )
        self.cr1a   = CutClass ("CR1a",    [
                                       ["CR1a", "{lepCol}_mt[{lepIndex}[0]]<{mt0}".format(lepCol=lepCollection, lepIndex=lepIndex, **mts)],
                                   ] , 
                          baseCut = self.cr1,
                          )
        self.cr1b   = CutClass ("CR1b",    [
                                       ["CR1b", btw("{lepCol}_mt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex),mt[0],mt[1])],
                                   ] , 
                          baseCut = self.cr1,
                          )
        self.cr1c   = CutClass ("CR1c",    [
                                       ["CR1c", "{lepCol}_mt[{lepIndex}[0]]>{mt1}".format(lepCol=lepCollection, lepIndex=lepIndex, **mts)],
                                   ] , 
                          baseCut = self.cr1c_baseCut,
                          )

        self.cr2      = CutClass ("CR2",   [
                                        ["Jet325","nIsrHJet>0"],
                                        #["met300","met>300"],
                                        #["OneOrMoreSoftB", one_or_more_soft_bjet],
                                        #["noHardB", veto_hard_bjet],
                                        ["1p Soft 0 Hard BJet", cr2_bjet],
                                        ["{lep}Pt_gt_30".format(lep=lep.title()),"{lepCol}_pt[{lepIndex}[0]]>30".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                      ],
                          baseCut = self.presel,
                          )
        self.cr2_      = CutClass( "CR2", [ ["CR2", "(1)"] ],
                            baseCut = self.cr2
                            ) 

        ################################################################################################
        ####################################                 ###########################################
        ####################################   SIDE BANDS    ###########################################
        ####################################                 ###########################################
        ################################################################################################

        """
        Hadronic / missing energy:
        ESR1: min(MET, HT-100) > 300 GeV
        ECR1: 200 < min(MET, HT-100) < 300 GeV
        ESR2: min(MET,isrJetPt-25) > 300 GeV
        ECR2: 200 < min(MET,isrJetPt-25) < 300 GeV
        
        
        
        """



        self.esr1      = CutClass( "ESR1", [ ["ESR1", "min(met, ht_basJet - 100 ) > 300"] ],
                            baseCut = None
                            ) 
        self.ecr1      = CutClass( "ECR1", [ ["ECR1", "(min(met, ht_basJet - 100) < 300 )&&(min(met, ht_basJet - 100) > 200 )"] ],
                            baseCut = None
                            ) 
        self.esr2      = CutClass( "ESR2", [ ["ESR2", "min(met, Jet_pt[IndexJet_isrJet[0]] - 25 ) > 300"] ],
                            baseCut = None
                            ) 
        self.ecr2      = CutClass( "ECR2", [ ["ECR2", "(min(met, Jet_pt[IndexJet_isrJet[0]] - 25) < 300 )&&(min(met, Jet_pt[IndexJet_isrJet[0]] - 25) > 200 )"] ],
                            baseCut = None
                            ) 


        esr1      =  "(min(met, ht_basJet - 100 ) > 300)"
        ecr1      =  "((min(met, ht_basJet - 100) < 300 )&&(min(met, ht_basJet - 100) > 200 ))"
        esr2      =  "(min(met, Jet_pt[IndexJet_isrJet[0]] - 25 ) > 300)"
        ecr2      =  "((min(met, Jet_pt[IndexJet_isrJet[0]] - 25) < 300 )&&(min(met, Jet_pt[IndexJet_isrJet[0]] - 25) > 200 ))"



        ##
        ##  W SideBands
        ##

        #
        #   sr1 side bands
        #    

        def makeSR1SideBand( side_band_cut_name, side_band_cut, mt, charge, pt,  baseCut=self.presel ):
            cutLists= [ [side_band_cut_name, side_band_cut ] ]
            cutLists.extend(      [
                                      #["Veto Soft BJet",veto_soft_bjet],
                                      #["Veto Hard BJet",veto_hard_bjet],
                                      ["Veto BJet" , veto_bjet ] , 
                                      ["{lep}Eta1.5".format(lep=lep.title()),"abs({lepCol}_eta[{lepIndex}[0]])<1.5".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                    ]
                            )

            if pt == "sr":
                cutLists.append( ["{lep}Pt_lt_30".format(lep=lep.title()),"{lepCol}_pt[{lepIndex}[0]]<30".format(lepCol=lepCollection, lepIndex=lepIndex)] )
            if pt == "cr":
                cutLists.append(    ["{lep}Pt_gt_30".format(lep=lep.title()),"{lepCol}_pt[{lepIndex}[0]]>30".format(lepCol=lepCollection, lepIndex=lepIndex)] )
            else:
                pass


            if charge == "pos":
                cutLists.append( ["pos{lep}".format(lep=lep.title()),"({lepCol}_pdgId[{lepIndex}[0]]==-13 || {lepCol}_pdgId[{lepIndex}[0]]==-11 )".format(lepCol=lepCollection, lepIndex=lepIndex)] )
            elif charge == "neg":
                cutLists.append( ["neg{lep}".format(lep=lep.title()),"({lepCol}_pdgId[{lepIndex}[0]]==13 || {lepCol}_pdgId[{lepIndex}[0]]==11 )".format(lepCol=lepCollection, lepIndex=lepIndex)] )
            else:
                print "no charge...."
                pass

            if mt == "a":
                cutLists.append( ["MTa","{lepCol}_mt[{lepIndex}[0]]< {mt0}".format(lepCol=lepCollection, lepIndex=lepIndex, **mts )]   )
            elif mt == "b":
                cutLists.append( ["MTb",btw("{lepCol}_mt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex), mts['mt0'], mts['mt1'] )]   )
            elif mt == "c":
                cutLists.append( ["MTc","{lepCol}_mt[{lepIndex}[0]]> {mt1}".format(lepCol=lepCollection, lepIndex=lepIndex, **mts )]   )
            else:
                print "no MT....."
                pass
            return CutClass(  "MT%s"%mt +"_"+ side_band_cut_name +"_"+charge +"_PT%s"%(pt.upper()), cutLists, baseCut=baseCut)
    




        mtabc = ["a","b","c"]
        pts = ["sr","cr"]
        charges = ["neg", "pos"]
        sr1_side_band_cuts  = [ 
                                #["ESR1", "min(met, ht_basJet - 100 ) > 300"],
                                ["ECR1", "(min(met, ht_basJet - 100) < 300 )&&(min(met, ht_basJet - 100) > 200 )"],
                                #["ESR2", "min(met, Jet_pt[IndexJet_isrJet[0]] - 25 ) > 300"],
                                #["ECR2", "(min(met, Jet_pt[IndexJet_isrJet[0]] - 25) < 300 )&&(min(met, Jet_pt[IndexJet_isrJet[0]] - 25) > 200 )"],
                          ]

        self.sr1_side_band_dict = { }
        self.sr1_side_bands     = { }
        for mt_ in mtabc:
            for side_band_cut_name, side_band_cut in sr1_side_band_cuts:
                for charge in charges:
                    for pt in pts:
                        side_band ="MT%s"%mt_ +"_" + side_band_cut_name +"_"+charge +"_PT%s"%(pt.upper()) 
                        self.sr1_side_band_dict[side_band] = {'side_band_cut_name':side_band_cut_name, 'side_band_cut':side_band_cut, 'mt':mt_, 'charge':charge, 'pt':pt}
                        #print self.side_band_dict
                        self.sr1_side_bands[side_band] = makeSR1SideBand(**self.sr1_side_band_dict[side_band]) 



        self.sr1SideBands = CutClass( "sr1SideBands",
                                      [ [sb, sbInst.inclCombined] for  sb, sbInst in sorted( self.sr1_side_bands.iteritems() ) ]  
                            ,
                            baseCut = self.presel
                            )


        #
        #   sr1 side bands
        #    
        

        def makeSR2SideBand( side_band_cut_name, side_band_cut,  pt,  baseCut=self.presel ):
            cutLists= [ [side_band_cut_name, side_band_cut ] ]
            cutLists.extend(      [
                                      #["Veto Soft BJet",veto_soft_bjet],
                                      #["Veto Hard BJet",veto_hard_bjet],
                                      #["Veto BJet" , veto_bjet ] , 
                                      #["{lep}Eta1.5".format(lep=lep.title()),"abs({lepCol}_eta[{lepIndex}[0]])<1.5".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                    ]
                            )

            if pt == "sr":
                cutLists.append(    ["{lep}Pt_lt_30".format(lep=lep.title()),"{lepCol}_pt[{lepIndex}[0]]<30".format(lepCol=lepCollection, lepIndex=lepIndex)]  )
            if pt == "cr":
                cutLists.append(    ["{lep}Pt_gt_30".format(lep=lep.title()),"{lepCol}_pt[{lepIndex}[0]]>30".format(lepCol=lepCollection, lepIndex=lepIndex)]  )
            else:
                pass

            return CutClass(  side_band_cut_name + "_PT%s"%(pt.upper()), cutLists, baseCut=baseCut)
    


        pts = ["sr","cr"]
        sr2_side_band_cuts  = [ 
                                #["ESR2", "min(met, ht_basJet - 100 ) > 300"],
                                ["ECR2", " (min(met, Jet_pt[IndexJet_isrJet[0]] - 25) < 300 )&&(min(met, Jet_pt[IndexJet_isrJet[0]] - 25) > 200 )"],
                                ["BCR1",  crtt1_bjet ],
                                ["BCR1_ESR1","(%s) && (%s)"%(crtt1_bjet, esr1 )],
                                ["BCR1_ESR2","(%s) && (%s)"%(crtt1_bjet, esr2 )],

                          ]

        self.sr2_side_band_dict = { }
        self.sr2_side_bands     = { }
        for side_band_cut_name, side_band_cut in sr2_side_band_cuts:
            for pt in pts:
                side_band = side_band_cut_name + "_PT%s"%(pt.upper()) 
                self.sr2_side_band_dict[side_band] = {'side_band_cut_name':side_band_cut_name, 'side_band_cut':side_band_cut, 'pt':pt}
                self.sr2_side_bands[side_band] = makeSR2SideBand(**self.sr2_side_band_dict[side_band]) 



        self.sr2SideBands = CutClass( "sr2SideBands",
                                      [ [sb, sbInst.inclCombined] for  sb, sbInst in sorted( self.sr2_side_bands.iteritems() ) ]  
                            ,
                            baseCut = self.presel
                            )


        ##
        ##  TT SideBands
        ##

        # do the same with crtt, split in mt, charge etc
        def makeTTSideBand( side_band_cut_name, side_band_cut, mt, charge, pt,  baseCut=self.presel ):
            cutLists= [ [side_band_cut_name, side_band_cut ] ]
            cutLists.extend(      [
                                      #["2 or more BJets", two_or_more_bjet],
                                      #["At least 1 Hard BJet", one_or_more_hard_bjet],
                                      ["2p BJet atleast 1 Hard" , crtt2_bjet ] ,
                                      #["Veto Soft BJet",veto_soft_bjet],
                                      #["Veto Hard BJet",veto_hard_bjet],
                                      #["{lep}Eta1.5".format(lep=lep.title()),"abs({lepCol}_eta[{lepIndex}[0]])<1.5".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                    ]
                            )

            if pt == "sr":
                cutLists.append(    ["{lep}Pt_lt_30".format(lep=lep.title()),"{lepCol}_pt[{lepIndex}[0]]<30".format(lepCol=lepCollection, lepIndex=lepIndex)] )
            if pt == "cr":
                cutLists.append(    ["{lep}Pt_gt_30".format(lep=lep.title()),"{lepCol}_pt[{lepIndex}[0]]>30".format(lepCol=lepCollection, lepIndex=lepIndex)] )
            else:
                pass
            if charge == "pos":
                cutLists.append( ["pos{lep}".format(lep=lep.title()),"({lepCol}_pdgId[{lepIndex}[0]]==-13 || {lepCol}_pdgId[{lepIndex}[0]]==-11 )".format(lepCol=lepCollection, lepIndex=lepIndex)] )
            elif charge == "neg":
                cutLists.append( ["neg{lep}".format(lep=lep.title()),"({lepCol}_pdgId[{lepIndex}[0]]==13 || {lepCol}_pdgId[{lepIndex}[0]]==11 )".format(lepCol=lepCollection, lepIndex=lepIndex)] )
            else:
                print "no charge...."
                pass

            if mt == "a":
                cutLists.append( ["MTa","{lepCol}_mt[{lepIndex}[0]]< {mt0}".format(lepCol=lepCollection, lepIndex=lepIndex, **mts )]   )
            elif mt == "b":
                cutLists.append( ["MTb",btw("{lepCol}_mt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex), mts['mt0'], mts['mt1'] )]   )
            elif mt == "c":
                cutLists.append( ["MTc","{lepCol}_mt[{lepIndex}[0]]> {mt1}".format(lepCol=lepCollection, lepIndex=lepIndex, **mts )]   )
            else:
                print "no MT....."
                pass
            return CutClass(  ( "MT%s_"%mt if mt else "" )+ side_band_cut_name + ("_%s"%charge if charge else "") +"_PT%s"%(pt.upper()), cutLists, baseCut=baseCut)


        pts = ["sr","cr"]
        #mtabc = ["a","b","c", ""]
        #charges = ["neg", "pos", ""]
        mtabc   = [""]
        charges = ["pos", "neg", ""]
        tt_side_band_cuts  = [ 
                                #["ESR1", "min(met, ht_basJet - 100 ) > 300"],
                                #["ECR1", "(min(met, ht_basJet - 100) < 300 )&&(min(met, ht_basJet - 100) > 200 )"],
                                #["ESR2", "min(met, Jet_pt[IndexJet_isrJet[0]] - 25 ) > 300"],
                                #["ECR2", "(min(met, Jet_pt[IndexJet_isrJet[0]] - 25) < 300 )&&(min(met, Jet_pt[IndexJet_isrJet[0]] - 25) > 200 )"],
                                ["BCR2", "(1)"],
                                #["{lep}Eta1.5".format(lep=lep.title()),"abs({lepCol}_eta[{lepIndex}[0]])<1.5".format(lepCol=lepCollection, lepIndex=lepIndex)],
                          ]


        self.tt_side_band_dict = { }
        self.tt_side_bands     = { }
        tt_side_band_legend = []
        for mt_ in mtabc:
            for side_band_cut_name, side_band_cut in tt_side_band_cuts:
                for charge in charges:
                    for pt in pts:
                        side_band = ("MT%s_"%mt_ if mt_ else "")  + side_band_cut_name + ("_%s"%charge if charge else "") +"_PT%s"%(pt.upper()) 
                        self.tt_side_band_dict[side_band] = {'side_band_cut_name':side_band_cut_name, 'side_band_cut':side_band_cut, 'mt':mt_, 'charge':charge, 'pt':pt}
                        #print self.side_band_dict
                        self.tt_side_bands[side_band] = makeTTSideBand(**self.tt_side_band_dict[side_band]) 


        self.ttSideBands = CutClass( "ttSideBands",
                                      [ [sb, sbInst.inclCombined] for  sb, sbInst in sorted( self.tt_side_bands.iteritems() ) ]  
                            ,
                            baseCut = self.presel
                            )


        self.sideBands = CutClass( "sideBands",
                                      [ [sb, sbInst.inclCombined] for  sb, sbInst in sorted( self.sr1_side_bands.iteritems() ) ] + 
                                      [ [sb, sbInst.inclCombined] for  sb, sbInst in sorted( self.sr2_side_bands.iteritems() ) ] +
                                      [ [sb, sbInst.inclCombined] for  sb, sbInst in sorted( self.tt_side_bands.iteritems()  ) ] 
                            ,
                            baseCut = self.presel
                            )


        #self.ttSideBands = CutClass("ttSideBands",[], baseCut = self.presel)
        #self.ttSideBands.add( self.crtt2    , 'inclCombinedList' )
        #self.ttSideBands.add( self.crtt1    , 'inclCombinedList' )
        



        ################################################################################################
        ####################################                 ###########################################
        ####################################     FINAL BINS  ###########################################
        ####################################                 ###########################################
        ################################################################################################
        self.srPosNeg        =   CutClass( "SRsPosNeg" , [] , baseCut = self.presel )
        self.srPosNeg.add(   self.sr1a           , baseCutString =  self.sr1.combined           )
        self.srPosNeg.add(   self.sr1b           , baseCutString =  self.sr1.combined           )
        self.srPosNeg.add(   self.sr1cNegCharge  , baseCutString =  self.sr1cNegCharge.baseCut.combined  )
        self.srPosNeg.add(   self.sr1cPosCharge  , baseCutString =  self.sr1cPosCharge.baseCut.combined  )
        self.srPosNeg.add(   self.sr2            , 'inclCombinedList'  , baseCutString =  self.sr2.baseCut.combined  )



        self.srs        =   CutClass( "SRs" , [] , baseCut = self.presel )
        self.srs.add(   self.sr1a          , baseCutString =  self.sr1.combined           )
        self.srs.add(   self.sr1b          , baseCutString =  self.sr1.combined           )
        self.srs.add(   self.sr1c          , baseCutString =  self.sr1c_baseCut.combined  )
        self.srs.add(   self.sr2   ,'inclCombinedList'     , baseCutString =  self.sr2.baseCut.combined  )


        
        self.crs        =   CutClass( "CRs" , [] , baseCut = self.presel )
        self.crs.add(   self.cr1a          , baseCutString =  self.cr1.inclCombined           )
        self.crs.add(   self.cr1b          , baseCutString =  self.cr1.inclCombined           )
        self.crs.add(   self.cr1c          , baseCutString =  self.cr1c_baseCut.inclCombined  )
        self.crs.add(   self.cr2_             , baseCutString = self.cr2.inclCombined         ) 
        self.crs.add(   self.crtt2     ,'inclCombinedList',  ) 
        
        
        self.bins        =   CutClass( "Bins" , [] , baseCut = self.presel )
        self.bins.add( self.sr1ab_ptbin ,  baseCutString = self.sr1.inclCombined          )
        self.bins.add( self.sr1c_ptbin  ,  baseCutString = self.sr1c_baseCut.inclCombined )
        self.bins.add(   self.sr2_ptbin       , baseCutString =  self.sr2.inclCombined ) 
        #selfbinsI.add(   self.cr1abc          , baseCutString =  self.cr1.inclCombined )
        self.bins.add(   self.cr1a          , baseCutString =  self.cr1.inclCombined           )
        self.bins.add(   self.cr1b          , baseCutString =  self.cr1.inclCombined           )
        self.bins.add(   self.cr1c          , baseCutString =  self.cr1c_baseCut.inclCombined  )
        self.bins.add(   self.cr2_             , baseCutString = self.cr2.inclCombined         ) 
        self.bins.add(   self.crtt2     ,'inclCombinedList',   ) 
        


        self.bins_sum   = CutClass ("BinsSummary",    [], baseCut= self.presel ) 
        self.bins_sum.add( self.sr1ab_ptbin ,  baseCutString = self.sr1.inclCombined          )
        self.bins_sum.add( self.sr1c_ptbin  ,  baseCutString = self.sr1c_baseCut.inclCombined )
        self.bins_sum.add( self.sr2_ptbin   ,  baseCutString = self.sr2.inclCombined          )
        self.bins_sum.add(   self.sr1a          , baseCutString =  self.sr1.combined           )
        self.bins_sum.add(   self.sr1b          , baseCutString =  self.sr1.combined           )
        self.bins_sum.add(   self.sr1c          , baseCutString =  self.sr1c_baseCut.combined  )
        self.bins_sum.add(   self.sr2   ,'inclCombinedList'     , baseCutString =  self.sr2.baseCut.combined  )
        self.bins_sum.add(   self.cr1a          , baseCutString =  self.cr1.inclCombined           )
        self.bins_sum.add(   self.cr1b          , baseCutString =  self.cr1.inclCombined           )
        self.bins_sum.add(   self.cr1c          , baseCutString =  self.cr1c_baseCut.inclCombined  )
        self.bins_sum.add(   self.cr2_             , baseCutString = self.cr2.inclCombined         ) 
        self.bins_sum.add(   self.crtt2     ,'inclCombinedList',   ) 

        
        
        #self.presel_common = CutClass('presel_common', [], baseCut=None)
        #self.presel_common.add( self.presel_noAntiQCD )
        #self.presel_common.add( self.presel_antiQCD   )


         
        self.cutflow   =    CutClass( "SRCutFlow", [], baseCut = None)
        #self.cutflow.add( self.presel, 'flow', baseCutString = None)
        self.cutflow.add( self.presel_noAntiQCD , 'combinedList', baseCutString = None)
        self.cutflow.add( self.presel_antiQCD   , 'inclFlow'        , baseCutString = self.presel_noAntiQCD.combined)
        self.cutflow.add( self.lepSel           , 'inclFlow'        , baseCutString = self.presel_common.combined)
        self.cutflow.add( self.sr1              , 'inclFlow'    , baseCutString = self.presel.combined)
        self.cutflow.add( self.sr2              , 'inclFlow'    , baseCutString = self.presel.combined)



if __name__ == "__main__":
    lepCuts = Cuts(  "LepGood",  "lep")
    muCuts  = Cuts(  "LepGood",  "mu")
    elCuts  = Cuts(  "LepGood",  "el")

