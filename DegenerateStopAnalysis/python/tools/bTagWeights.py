import math
from Workspace.DegenerateStopAnalysis.tools.degTools import CutClass, joinCutStrings, splitCutInPt, btw, less, more
from Workspace.DegenerateStopAnalysis.tools.btag_sf_map import BTagSFMap

## --------------------------------------------------------------
##                           Variables
## --------------------------------------------------------------

#default values 
btag_sf_map = BTagSFMap("sf")
btag_to_sf  = btag_sf_map.btag_to_sf
sf_to_btag  = btag_sf_map.sf_to_btag

def bTagWeights(btag = 'sf'):
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

   cutdict = {}
   weightdict = {}

   if btag == 'btag':
       cutdict['veto_soft_bjet']          = btag_sf_map.btag_veto_soft_bjet       #'(nBSoftJet == 0 )'
       cutdict['one_soft_bjet']           = btag_sf_map.btag_one_soft_bjet        #'(nBSoftJet == 1 )'
       cutdict['one_or_more_soft_bjet']   = btag_sf_map.btag_one_or_more_soft_bjet#'(nBSoftJet >= 1 )'
       cutdict['veto_hard_bjet']          = btag_sf_map.btag_veto_hard_bjet       #'(nBHardJet == 0 )'
       cutdict['one_hard_bjet']           = btag_sf_map.btag_one_hard_bjet        #'(nBHardJet == 1 )'
       cutdict['one_or_more_hard_bjet']   = btag_sf_map.btag_one_or_more_hard_bjet#'(nBHardJet >= 1 )'
       cutdict['veto_bjet']               = btag_sf_map.btag_veto_bjet            #'(  nBJet   == 0 )'
       cutdict['one_bjet']                = btag_sf_map.btag_one_bjet             #'(  nBJet   == 1 )'
       cutdict['one_or_more_bjet']        = btag_sf_map.btag_one_or_more_bjet     #'(  nBJet   >= 1 )'
       cutdict['two_or_more_bjet']        = btag_sf_map.btag_two_or_more_bjet     #'(  nBJet   >= 2 )'
   
       cutdict['sr1_bjet']                = btag_sf_map.btag_sr1_bjet             # veto_bjet 
       cutdict['sr2_bjet']                = btag_sf_map.btag_sr2_bjet             # "( (nBSoftJet>=1) && (nBHardJet==0) )"
       cutdict['cr1_bjet']                = btag_sf_map.btag_cr1_bjet             # veto_bjet
       cutdict['cr2_bjet']                = btag_sf_map.btag_cr2_bjet             # "( (nBSoftJet>=1) && (nBHardJet==0)  )"
       cutdict['crtt1_bjet']              = btag_sf_map.btag_crtt1_bjet           # "( (nBSoftJet==0) && (nBHardJet==1)  )"
       cutdict['crtt2_bjet']              = btag_sf_map.btag_crtt2_bjet           # "( (nBJet>=2)     && (nBHardJet>=1) )"
      
       return cutdict      
 
   elif btag == 'sf':
       weightdict['veto_soft_bjet']          = btag_sf_map.sf_veto_soft_bjet           #'(weightSBTag0_SF)' 
       weightdict['one_soft_bjet']           = btag_sf_map.sf_one_soft_bjet            #'(weightSBTag1_SF)' 
       weightdict['one_or_more_soft_bjet']   = btag_sf_map.sf_one_or_more_soft_bjet    #'(weightSBTag1p_SF)'
       weightdict['veto_hard_bjet']          = btag_sf_map.sf_veto_hard_bjet           #'(weightHBTag0_SF)' 
       weightdict['one_hard_bjet']           = btag_sf_map.sf_one_hard_bjet            #'(weightHBTag1_SF)' 
       weightdict['one_or_more_hard_bjet']   = btag_sf_map.sf_one_or_more_hard_bjet    #'(weightHBTag1p_SF)'
       weightdict['veto_bjet']               = btag_sf_map.sf_veto_bjet                #'(weightBTag0_SF)'   
       weightdict['one_bjet']                = btag_sf_map.sf_one_bjet                 #'(weightBTag1_SF)'   
       weightdict['one_or_more_bjet']        = btag_sf_map.sf_one_or_more_bjet         #'(weightBTag1p_SF)'  
       weightdict['two_or_more_bjet']        = btag_sf_map.sf_two_or_more_bjet         #'(weightBTag2p_SF)'  
       
       weightdict['sr1_bjet']                = btag_sf_map.sf_sr1_bjet                 # veto_bjet 
       weightdict['sr2_bjet']                = btag_sf_map.sf_sr2_bjet                 # "(weightSBTag1p_SF * weightHBTag0_SF)" 
       weightdict['cr1_bjet']                = btag_sf_map.sf_cr1_bjet                 # veto_bjet
       weightdict['cr2_bjet']                = btag_sf_map.sf_cr2_bjet                 # "(weightSBTag1p_SF * weightHBTag0_SF)" #"( (nBSoftJet>=1) && (nBHardJet==0)  )"
       weightdict['crtt1_bjet']              = btag_sf_map.sf_crtt1_bjet               # "(weightSBTag0_SF  * weightHBTag1_SF)" #"( (nBSoftJet==0) && (nBHardJet==1)  )"
       weightdict['crtt2_bjet']              = btag_sf_map.sf_crtt2_bjet               # "(weightHBTag1p_SF-(weightSBTag0_SF*weightHBTag1_SF))"#"( (nBJet>=2)     && (nBHardJet>=1) )"
  
       return weightdict 
       pass
   else:
       raise Exception("btag option not recongized: %s"%btag)
