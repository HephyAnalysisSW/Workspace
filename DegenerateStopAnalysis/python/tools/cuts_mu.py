import math
from Workspace.DegenerateStopAnalysis.navidTools.NavidTools import CutClass, joinCutStrings, splitCutInPt, btw, less, more
#from Workspace.DegenerateStopAnalysis.cuts.common import presel_common
from Workspace.DegenerateStopAnalysis.tools.cuts_common import presel_common

## --------------------------------------------------------------
##                           Variables
## --------------------------------------------------------------

minAngle = lambda phi1, phi2 : "TMath::Min( (2*pi) - abs({phi1}-{phi2}) , abs({phi1}-{phi2}) )".format(phi1=phi1,phi2=phi2)  


## --------------------------------------------------------------
##                            CUT LISTS
## --------------------------------------------------------------

lepCollection = "LepGood"

class MuonCuts():
    def __init__( self,  LepCollection="LepGood" ):

        self.presel_common = presel_common


        self.muSel = CutClass ("muSel", [
                                      #["TauElVeto","(Sum$(TauGood_idMVA)==0) && (Sum$(abs({LepCol}_pdgId)==11 && {LepCol}_SPRING15_25ns_v1==1)==0)"],
                                      ["TauElVeto","(Sum$(TauGood_idMVANewDM && TauGood_pt > 20 )==0) && (Sum$(abs({LepCol}_pdgId)==11 && {LepCol}_SPRING15_25ns_v1>=1 && {LepCol}_pt > 20)==0)".format(LepCol=LepCollection)],
                                      ["1Mu-2ndMu20Veto", "(n{LepCol}_mu==1 || (n{LepCol}_mu ==2 && {LepCol}_pt[Index{LepCol}_mu[1]] < 20) )".format(LepCol=LepCollection)],
                                     ],
                        baseCut=self.presel_common,
                        )
        
        
        self.presel = CutClass('presel', [], baseCut=None)
        self.presel.add(self.presel_common)
        self.presel.add(self.muSel)
        
        
        
        self.sr1   = CutClass ("SR1",    [
                                      ["CT300","min(met,ht_basJet-100) > 300 "],
                                      ["BVeto","(nBSoftJet == 0 && nBHardJet ==0)"],
                                      ["negMuon","{LepCol}_pdgId[Index{LepCol}_mu[0]]==13".format(LepCol=LepCollection)],
                                      ["MuEta1.5","abs({LepCol}_eta[Index{LepCol}_mu[0]])<1.5".format(LepCol=LepCollection)],
                                      ["MuPt30","{LepCol}_pt[Index{LepCol}_mu[0]]<30".format(LepCol=LepCollection)],
                                   ] , 
                          baseCut = self.presel,
                          )
        
        
        
        self.sr2      = CutClass ("SR2",   [ 
                                        ["ISR325","nIsrHJet>0"],
                                        ["Met300","met>300"],
                                        ["SoftBJet","(nBSoftJet>=1) && ( nBHardJet==0 ) "],
                                        ["MuPt<30","{LepCol}_pt[Index{LepCol}_mu[0]]<30".format(LepCol=LepCollection)],
                                      ],
                          baseCut = self.presel,
                          )
        
        
        
        
        self.mtabc   = CutClass ("MTabc",    [
                                       ["MTa","{LepCol}_mt[Index{LepCol}_mu[0]]<60".format(LepCol=LepCollection)],
                                       ["MTb",btw("{LepCol}_mt[Index{LepCol}_mu[0]]".format(LepCol=LepCollection),60,88)],
                                       ["MTc","{LepCol}_mt[Index{LepCol}_mu[0]]>88".format(LepCol=LepCollection)],
                                   ] , 
                          baseCut = self.sr1,
                          )
        
        
        self.mtabc_pt = splitCutInPt(self.mtabc)
        
        
        
        self.sr1Loose   = CutClass ("SR1Loose",    [
                                      #["CT300","min(met,ht_basJet-100) > 300 "],
                                      ["CT200","min(met,ht_basJet-100) > 200 "],
                                      ["BVeto","(nBSoftJet == 0 && nBHardJet ==0)"],
                                      ["negMuon","{LepCol}_pdgId[Index{LepCol}_mu[0]]==13".format(LepCol=LepCollection)],
                                      ["MuEta1.5","abs({LepCol}_eta[Index{LepCol}_mu[0]])<1.5".format(LepCol=LepCollection)],
                                      ["MuPt30","{LepCol}_pt[Index{LepCol}_mu[0]]<30".format(LepCol=LepCollection)],
                                   ] , 
                          baseCut = self.presel,
                          )
        
        
        self.sr1abc_ptbin   = CutClass ("SR1abc_PtBinned",    [
                                       #["SR1a","{LepCol}_mt[Index{LepCol}_mu[0]]<60"],
                                          ["SRL1a",joinCutStrings(   ["{LepCol}_mt[Index{LepCol}_mu[0]]<60".format(LepCol=LepCollection),         btw("{LepCol}_pt[Index{LepCol}_mu[0]]".format(LepCol=LepCollection),5,12)]  )],
                                          ["SRH1a",joinCutStrings(   ["{LepCol}_mt[Index{LepCol}_mu[0]]<60".format(LepCol=LepCollection),         btw("{LepCol}_pt[Index{LepCol}_mu[0]]".format(LepCol=LepCollection),12,20)] )],
                                          ["SRV1a",joinCutStrings(   ["{LepCol}_mt[Index{LepCol}_mu[0]]<60".format(LepCol=LepCollection),         btw("{LepCol}_pt[Index{LepCol}_mu[0]]".format(LepCol=LepCollection),20,30)] )],
                                       #["SR1b",btw("{LepCol}_mt[Index{LepCol}_mu[0]]",60,88)],
                                          ["SRL1b",joinCutStrings(   [btw("{LepCol}_mt[Index{LepCol}_mu[0]]".format(LepCol=LepCollection),60,88), btw("{LepCol}_pt[Index{LepCol}_mu[0]]".format(LepCol=LepCollection),5,12)]  )],
                                          ["SRH1b",joinCutStrings(   [btw("{LepCol}_mt[Index{LepCol}_mu[0]]".format(LepCol=LepCollection),60,88), btw("{LepCol}_pt[Index{LepCol}_mu[0]]".format(LepCol=LepCollection),12,20)] )],
                                          ["SRV1b",joinCutStrings(   [btw("{LepCol}_mt[Index{LepCol}_mu[0]]".format(LepCol=LepCollection),60,88), btw("{LepCol}_pt[Index{LepCol}_mu[0]]".format(LepCol=LepCollection),20,30)] )],
                                       #["SR1c","{LepCol}_mt[Index{LepCol}_mu[0]]>88"],
                                          ["SRL1c",joinCutStrings(   ["{LepCol}_mt[Index{LepCol}_mu[0]]>88".format(LepCol=LepCollection),         btw("{LepCol}_pt[Index{LepCol}_mu[0]]".format(LepCol=LepCollection),5,12)]  )],
                                          ["SRH1c",joinCutStrings(   ["{LepCol}_mt[Index{LepCol}_mu[0]]>88".format(LepCol=LepCollection),         btw("{LepCol}_pt[Index{LepCol}_mu[0]]".format(LepCol=LepCollection),12,20)] )],
                                          ["SRV1c",joinCutStrings(   ["{LepCol}_mt[Index{LepCol}_mu[0]]>88".format(LepCol=LepCollection),         btw("{LepCol}_pt[Index{LepCol}_mu[0]]".format(LepCol=LepCollection),20,30)] )],
                                   ] , 
                          baseCut = self.sr1,
                          )
        
        
        self.sr1abc   = CutClass ("SR1abc",    [
                                       ["SR1a","{LepCol}_mt[Index{LepCol}_mu[0]]<60".format(LepCol=LepCollection)],
                                       ["SR1b",btw("{LepCol}_mt[Index{LepCol}_mu[0]]".format(LepCol=LepCollection),60,88)],
                                       ["SR1c","{LepCol}_mt[Index{LepCol}_mu[0]]>88".format(LepCol=LepCollection)],
                                   ] , 
                          baseCut = self.sr1,
                          )
        
        
        self.sr1a   = CutClass ("SR1a",    [
                                       ["SR1a","{LepCol}_mt[Index{LepCol}_mu[0]]<60".format(LepCol=LepCollection)],
                                   ] , 
                          baseCut = self.sr1,
                          )
        
        
        self.sr1b   = CutClass ("SR1b",    [
                                       ["SR1b",btw("{LepCol}_mt[Index{LepCol}_mu[0]]".format(LepCol=LepCollection),60,88)],
                                   ] , 
                          baseCut = self.sr1,
                          )
        
        
        self.sr1c   = CutClass ("SR1c",    [
                                       ["SR1c","{LepCol}_mt[Index{LepCol}_mu[0]]>88".format(LepCol=LepCollection)],
                                   ] , 
                          baseCut = self.sr1,
                          )
        
        
        self.sr2_ptbin   = CutClass ("SR2_PtBinned",    [
                                          ["SRL2",  btw("{LepCol}_pt[Index{LepCol}_mu[0]]".format(LepCol=LepCollection),5,12)    ],
                                          ["SRH2",  btw("{LepCol}_pt[Index{LepCol}_mu[0]]".format(LepCol=LepCollection),12,20)   ],
                                          ["SRV2",  btw("{LepCol}_pt[Index{LepCol}_mu[0]]".format(LepCol=LepCollection),20,30)   ],
                                   ] , 
                          baseCut = self.sr2,
                          )
        
        ################################################################################################
        ####################################                 ###########################################
        #################################### Control Regions ###########################################
        ####################################                 ###########################################
        ################################################################################################
        
        
        
        
        self.cr1Loose    = CutClass ( "cr1Loose", [
                                      ["CT200","min(met,ht_basJet-100) > 200 "],
                                      #["CT300","min(met,ht_basJet-100) > 300 "],
                                      ["BVeto","(nBSoftJet == 0 && nBHardJet ==0)"],
                                      ["negMuon","{LepCol}_pdgId[Index{LepCol}_mu[0]]==13".format(LepCol=LepCollection)],
                                      ["MuEta1.5","abs({LepCol}_eta[Index{LepCol}_mu[0]])<1.5".format(LepCol=LepCollection)],
                                      ["MuPt30","{LepCol}_pt[Index{LepCol}_mu[0]]>30".format(LepCol=LepCollection)],
                            ],
                            baseCut= self.presel,
                        )
        
        
        self.crtt2    = CutClass ( "CRTT2", [
                              ["CRTT2","( (nBSoftJet + nBHardJet) > 1 ) && ( nBHardJet > 0  )"],
                                     ],
                            baseCut= self.presel ,
                        )
        
        self.cr1   = CutClass ("CR1",    [
                                      ["MuPt_gt_30","{LepCol}_pt[Index{LepCol}_mu[0]]>30".format(LepCol=LepCollection)],
                                      ["BVeto","(nBSoftJet == 0 && nBHardJet ==0)"],
                                      ["negMuon","{LepCol}_pdgId[Index{LepCol}_mu[0]]==13".format(LepCol=LepCollection)],
                                      ["MuEta1.5","abs({LepCol}_eta[Index{LepCol}_mu[0]])<1.5".format(LepCol=LepCollection)],
                                      #["BVeto_Medium25","nBJetMedium25==0"],
                                      ["CT300","min(met,ht_basJet-100) > 300 "],
                                      #["HT400 ","ht_basJet>400"],
                                      #["met300","met>300"],
                                   ] , 
                          baseCut = self.presel,
                          )
        
        
        self.cr1abc   = CutClass ("CR1abc",    [
                                       ["CR1a", "{LepCol}_mt[Index{LepCol}_mu[0]]<60".format(LepCol=LepCollection)],
                                       ["CR1b", btw("{LepCol}_mt[Index{LepCol}_mu[0]]".format(LepCol=LepCollection),60,88)],
                                       ["CR1c", "{LepCol}_mt[Index{LepCol}_mu[0]]>88".format(LepCol=LepCollection)],
                                   ] , 
                          baseCut = self.cr1,
                          )
        self.cr1a   = CutClass ("CR1a",    [
                                       ["CR1a", "{LepCol}_mt[Index{LepCol}_mu[0]]<60".format(LepCol=LepCollection)],
                                   ] , 
                          baseCut = self.cr1,
                          )
        self.cr1b   = CutClass ("CR1b",    [
                                       ["CR1b", btw("{LepCol}_mt[Index{LepCol}_mu[0]]".format(LepCol=LepCollection),60,88)],
                                   ] , 
                          baseCut = self.cr1,
                          )
        self.cr1c   = CutClass ("CR1c",    [
                                       ["CR1c", "{LepCol}_mt[Index{LepCol}_mu[0]]>88".format(LepCol=LepCollection)],
                                   ] , 
                          baseCut = self.cr1,
                          )
        self.cr2      = CutClass ("CR2",   [
                                        ["Jet325","nIsrHJet>0"],
                                        #["met300","met>300"],
                                        ["OneOrMoreSoftB","nBSoftJet>=1"],
                                        ["noHardB","nBHardJet==0"],
                                        ["MuPt_gt_30","{LepCol}_pt[Index{LepCol}_mu[0]]>30".format(LepCol=LepCollection)],
                                      ],
                          baseCut = self.presel,
                          )
        self.cr2_      = CutClass( "CR2", [ ["CR2", "(1)"] ],
                            baseCut = self.cr2
                            ) 
        
        
        
        self.runI        =   CutClass( "Reload" , [] , baseCut = self.presel )
        self.runI.add(   self.sr1abc_ptbin    , baseCutString =  self.sr1.inclCombined )
        self.runI.add(   self.sr2_ptbin       , baseCutString =  self.sr2.inclCombined ) 
        self.runI.add(   self.cr1abc          , baseCutString =  self.cr1.inclCombined )
        self.runI.add(   self.cr2_             , baseCutString = self.cr2.inclCombined ) 
        self.runI.add(   self.crtt2        ) 
        
        
        
        
        self.runIflow   =    CutClass( "ReloadSRCutFlow", [], baseCut = None)
        self.runIflow.add( self.presel, 'flow', baseCutString = None)
        self.runIflow.add( self.sr1, 'inclFlow', baseCutString = self.presel.combined)
        self.runIflow.add( self.sr2, 'inclFlow', baseCutString = self.presel.combined)





cuts = MuonCuts(LepCollection="LepGood")

