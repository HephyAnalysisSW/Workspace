import math
from Workspace.DegenerateStopAnalysis.tools.degTools import CutClass, joinCutStrings, splitCutInPt, btw, less, more
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

class LepCuts():
    def __init__( self,  lepCollection="LepGood" , lep="mu"):
        self.collection = lepCollection
        self.lep = lep 
        lepIndex = "Index{lepCol}_{Lep}".format(lepCol=lepCollection, Lep=lep)



        self.presel_common = presel_common
   
        lepSelCuts = [
                                      ["TauVeto","(Sum$(TauGood_idMVANewDM && TauGood_pt > 20 )==0)".format(lepCol=lepCollection)],
                                      ["1{lep}-2nd{lep}20Veto".format(lep=lep.title()), "(n{lepCol}_{lep}==1 || (n{lepCol}_{lep} ==2 && {lepCol}_pt[{lepIndex}[1]] < 20) )".format(lepCol=lepCollection, lepIndex=lepIndex , lep=lep)]
                      ]
    
        elVeto =               ["ElVeto","(Sum$(abs({lepCol}_pdgId)==11 && {lepCol}_SPRING15_25ns_v1>=1 && {lepCol}_pt > 20)==0)".format(lepCol=lepCollection)]
        muVeto =               ["MuVeto","( nLepGood_mu ==0 || (nLepGood_mu==1 && LepGood_pt[IndexLepGood_mu[0]] < 20) )".format(lepCol=lepCollection)       ]

        if lep == 'mu':
            otherLepVeto = elVeto
        elif lep =='el':
            otherLepVeto = muVeto
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
        
        
        
        self.sr1   = CutClass ("SR1",    [
                                      ["CT300","min(met,ht_basJet-100) > 300 "],
                                      ["BVeto","(nBSoftJet == 0 && nBHardJet ==0)"],
                                      ["neg{lep}".format(lep=lep.title()),"({lepCol}_pdgId[{lepIndex}[0]]==13 || {lepCol}_pdgId[{lepIndex}[0]]==11 )".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                      ["{lep}Eta1.5".format(lep=lep.title()),"abs({lepCol}_eta[{lepIndex}[0]])<1.5".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                      ["{lep}Pt30".format(lep=lep.title()),"{lepCol}_pt[{lepIndex}[0]]<30".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                   ] , 
                          baseCut = self.presel,
                          )
        
        self.sr2      = CutClass ("SR2",   [ 
                                        ["ISR325","nIsrHJet>0"],
                                        ["Met300","met>300"],
                                        ["SoftBJet","(nBSoftJet>=1) && ( nBHardJet==0 ) "],
                                        ["{lep}Pt<30".format(lep=lep.title()),"{lepCol}_pt[{lepIndex}[0]]<30".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                      ],
                          baseCut = self.presel,
                          )
        
        
        self.mtabc   = CutClass ("MTabc",    [
                                       ["MTa","{lepCol}_mt[{lepIndex}[0]]<60".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                       ["MTb",btw("{lepCol}_mt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex),60,88,)],
                                       ["MTc","{lepCol}_mt[{lepIndex}[0]]>88".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                   ] , 
                          baseCut = self.sr1,
                          )
        
        
        self.mtabc_pt = splitCutInPt(self.mtabc)
        
        
        
        self.sr1Loose   = CutClass ("SR1Loose",    [
                                      #["CT300","min(met,ht_basJet-100) > 300 "],
                                      ["CT200","min(met,ht_basJet-100) > 200 "],
                                      ["BVeto","(nBSoftJet == 0 && nBHardJet ==0)"],
                                      ["neg{lep}".format(lep=lep.title()),"({lepCol}_pdgId[{lepIndex}[0]]==13 || {lepCol}_pdgId[{lepIndex}[0]]==11 )".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                      ["{lep}Eta1.5".format(lep=lep.title()),"abs({lepCol}_eta[{lepIndex}[0]])<1.5".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                      ["{lep}Pt30".format(lep=lep.title()),"{lepCol}_pt[{lepIndex}[0]]<30".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                   ] , 
                          baseCut = self.presel,
                          )
        
        
        self.sr1abc_ptbin   = CutClass ("SR1abc_PtBinned",    [
                                       #["SR1a","{lepCol}_mt[{lepIndex}[0]]<60"],
                                          ["SRL1a",joinCutStrings(   ["{lepCol}_mt[{lepIndex}[0]]<60".format(lepCol=lepCollection, lepIndex=lepIndex),         btw("{lepCol}_pt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex),5,12)]  )],
                                          ["SRH1a",joinCutStrings(   ["{lepCol}_mt[{lepIndex}[0]]<60".format(lepCol=lepCollection, lepIndex=lepIndex),         btw("{lepCol}_pt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex),12,20)] )],
                                          ["SRV1a",joinCutStrings(   ["{lepCol}_mt[{lepIndex}[0]]<60".format(lepCol=lepCollection, lepIndex=lepIndex),         btw("{lepCol}_pt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex),20,30)] )],
                                       #["SR1b",btw("{lepCol}_mt[{lepIndex}[0]]",60,88)],
                                          ["SRL1b",joinCutStrings(   [btw("{lepCol}_mt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex),60,88), btw("{lepCol}_pt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex),5,12)]  )],
                                          ["SRH1b",joinCutStrings(   [btw("{lepCol}_mt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex),60,88), btw("{lepCol}_pt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex),12,20)] )],
                                          ["SRV1b",joinCutStrings(   [btw("{lepCol}_mt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex),60,88), btw("{lepCol}_pt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex),20,30)] )],
                                       #["SR1c","{lepCol}_mt[{lepIndex}[0]]>88"],
                                          ["SRL1c",joinCutStrings(   ["{lepCol}_mt[{lepIndex}[0]]>88".format(lepCol=lepCollection, lepIndex=lepIndex),         btw("{lepCol}_pt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex),5,12)]  )],
                                          ["SRH1c",joinCutStrings(   ["{lepCol}_mt[{lepIndex}[0]]>88".format(lepCol=lepCollection, lepIndex=lepIndex),         btw("{lepCol}_pt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex),12,20)] )],
                                          ["SRV1c",joinCutStrings(   ["{lepCol}_mt[{lepIndex}[0]]>88".format(lepCol=lepCollection, lepIndex=lepIndex),         btw("{lepCol}_pt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex),20,30)] )],
                                   ] , 
                          baseCut = self.sr1,
                          )
        
        
        self.sr1abc   = CutClass ("SR1abc",    [
                                       ["SR1a","{lepCol}_mt[{lepIndex}[0]]<60".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                       ["SR1b",btw("{lepCol}_mt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex),60,88)],
                                       ["SR1c","{lepCol}_mt[{lepIndex}[0]]>88".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                   ] , 
                          baseCut = self.sr1,
                          )
        
        
        self.sr1a   = CutClass ("SR1a",    [
                                       ["SR1a","{lepCol}_mt[{lepIndex}[0]]<60".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                   ] , 
                          baseCut = self.sr1,
                          )
        
        
        self.sr1b   = CutClass ("SR1b",    [
                                       ["SR1b",btw("{lepCol}_mt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex),60,88)],
                                   ] , 
                          baseCut = self.sr1,
                          )
        
        
        self.sr1c   = CutClass ("SR1c",    [
                                       ["SR1c","{lepCol}_mt[{lepIndex}[0]]>88".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                   ] , 
                          baseCut = self.sr1,
                          )
        
        
        self.sr2_ptbin   = CutClass ("SR2_PtBinned",    [
                                          ["SRL2",  btw("{lepCol}_pt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex),5,12)    ],
                                          ["SRH2",  btw("{lepCol}_pt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex),12,20)   ],
                                          ["SRV2",  btw("{lepCol}_pt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex),20,30)   ],
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
                                      ["neg{lep}".format(lep=lep.title()),"({lepCol}_pdgId[{lepIndex}[0]]==13 || {lepCol}_pdgId[{lepIndex}[0]]==11 )".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                      ["{lep}Eta1.5".format(lep=lep.title()),"abs({lepCol}_eta[{lepIndex}[0]])<1.5".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                      ["{lep}Pt30".format(lep=lep.title()),"{lepCol}_pt[{lepIndex}[0]]>30".format(lepCol=lepCollection, lepIndex=lepIndex)],
                            ],
                            baseCut= self.presel,
                        )
        
        
        self.crtt2    = CutClass ( "CRTT2", [
                              ["CRTT2","( (nBSoftJet + nBHardJet) > 1 ) && ( nBHardJet > 0  )"],
                                     ],
                            baseCut= self.presel ,
                        )
        
        self.cr1   = CutClass ("CR1",    [
                                      ["{lep}Pt_gt_30".format(lep=lep.title()),"{lepCol}_pt[{lepIndex}[0]]>30".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                      ["BVeto","(nBSoftJet == 0 && nBHardJet ==0)"],
                                      ["neg{lep}".format(lep=lep.title()),"( {lepCol}_pdgId[{lepIndex}[0]]==13 || {lepCol}_pdgId[{lepIndex}[0]]==11  )".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                      ["{lep}Eta1.5".format(lep=lep.title()),"abs({lepCol}_eta[{lepIndex}[0]])<1.5".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                      #["BVeto_Medium25","nBJetMedium25==0"],
                                      ["CT300","min(met,ht_basJet-100) > 300 "],
                                      #["HT400 ","ht_basJet>400"],
                                      #["met300","met>300"],
                                   ] , 
                          baseCut = self.presel,
                          )
        
        
        self.cr1abc   = CutClass ("CR1abc",    [
                                       ["CR1a", "{lepCol}_mt[{lepIndex}[0]]<60".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                       ["CR1b", btw("{lepCol}_mt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex),60,88)],
                                       ["CR1c", "{lepCol}_mt[{lepIndex}[0]]>88".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                   ] , 
                          baseCut = self.cr1,
                          )
        self.cr1a   = CutClass ("CR1a",    [
                                       ["CR1a", "{lepCol}_mt[{lepIndex}[0]]<60".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                   ] , 
                          baseCut = self.cr1,
                          )
        self.cr1b   = CutClass ("CR1b",    [
                                       ["CR1b", btw("{lepCol}_mt[{lepIndex}[0]]".format(lepCol=lepCollection, lepIndex=lepIndex),60,88)],
                                   ] , 
                          baseCut = self.cr1,
                          )
        self.cr1c   = CutClass ("CR1c",    [
                                       ["CR1c", "{lepCol}_mt[{lepIndex}[0]]>88".format(lepCol=lepCollection, lepIndex=lepIndex)],
                                   ] , 
                          baseCut = self.cr1,
                          )
        self.cr2      = CutClass ("CR2",   [
                                        ["Jet325","nIsrHJet>0"],
                                        #["met300","met>300"],
                                        ["OneOrMoreSoftB","nBSoftJet>=1"],
                                        ["noHardB","nBHardJet==0"],
                                        ["{lep}Pt_gt_30".format(lep=lep.title()),"{lepCol}_pt[{lepIndex}[0]]>30".format(lepCol=lepCollection, lepIndex=lepIndex)],
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



if __name__ == "__main__":
    lepCuts = LepCuts(  "LepGood",  "lep")
    muCuts  = LepCuts(  "LepGood",  "mu")
    elCuts  = LepCuts(  "LepGood",  "el")

