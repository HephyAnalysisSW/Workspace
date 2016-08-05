

class BTagSFMap():
    def __init__(self,sfvar):

        sfvar_dict = {
                       "mc"         :"MC"             ,
                       "btag"       :"SF"             ,
                       "sf"         :"SF"             ,
                       "sf_b_down"  :"SF_b_Down"      ,
                       "sf_b_up"    :"SF_b_Up"        ,
                       "sf_l_down"  :"SF_l_Down"      ,
                       "sf_l_up"    :"SF_l_Up"        ,
                        }

        if not sfvar in sfvar_dict.values():
            sfvar = sfvar_dict[sfvar]        



        self.btag_veto_soft_bjet          = '(nBSoftJet == 0 )'
        self.btag_one_soft_bjet           = '(nBSoftJet == 1 )'
        self.btag_one_or_more_soft_bjet   = '(nBSoftJet >= 1 )'
        self.btag_veto_hard_bjet          = '(nBHardJet == 0 )'
        self.btag_one_hard_bjet           = '(nBHardJet == 1 )'
        self.btag_one_or_more_hard_bjet   = '(nBHardJet >= 1 )'
        self.btag_veto_bjet               = '((nBHardJet + nBSoftJet)== 0 )'
        self.btag_one_bjet                = '((nBHardJet + nBSoftJet)== 1 )'
        self.btag_one_or_more_bjet        = '((nBHardJet + nBSoftJet)>= 1 )'
        self.btag_two_or_more_bjet        = '((nBHardJet + nBSoftJet)>= 2 )'
        self.btag_sr1_bjet                =  self.btag_veto_bjet
        self.btag_sr2_bjet                =  "( (nBSoftJet>=1) && (nBHardJet==0) )"
        self.btag_cr1_bjet                =  self.btag_veto_bjet
        self.btag_cr2_bjet                =  "( (nBSoftJet>=1) && (nBHardJet==0)  )"
        self.btag_crtt1_bjet              =  "( (nBSoftJet==0) && (nBHardJet==1)  )"
        self.btag_crtt2_bjet              =  "( (nBJet>=2)     && (nBHardJet>=1) )"
        
        
        
        
        self.sf_veto_soft_bjet         = '(weightSBTag0_%s)'%sfvar
        self.sf_one_soft_bjet          = '(weightSBTag1_%s)'%sfvar
        self.sf_one_or_more_soft_bjet  = '(weightSBTag1p_%s)'%sfvar
        self.sf_veto_hard_bjet         = '(weightHBTag0_%s)'%sfvar
        self.sf_one_hard_bjet          = '(weightHBTag1_%s)'%sfvar
        self.sf_one_or_more_hard_bjet  = '(weightHBTag1p_%s)'%sfvar
        self.sf_veto_bjet              = '(weightBTag0_%s)'%sfvar
        self.sf_one_bjet               = '(weightBTag1_%s)'%sfvar
        self.sf_one_or_more_bjet       = '(weightBTag1p_%s)'%sfvar
        self.sf_two_or_more_bjet       = '(weightBTag2p_%s)'%sfvar
        
        self.sf_sr1_bjet                =  self.sf_veto_bjet
        self.sf_sr2_bjet                =  "(weightSBTag1p_{sfvar} * weightHBTag0_{sfvar})".format(sfvar=sfvar)
        self.sf_cr1_bjet                =  self.sf_veto_bjet
        self.sf_cr2_bjet                =  "(weightSBTag1p_{sfvar} * weightHBTag0_{sfvar})".format(sfvar=sfvar) #"( (nBSoftJet>=1) && (nBHardJet==0)  )"
        self.sf_crtt1_bjet              =  "(weightSBTag0_{sfvar}  * weightHBTag1_{sfvar})".format(sfvar=sfvar) #"( (nBSoftJet==0) && (nBHardJet==1)  )"
        self.sf_crtt2_bjet              =  "((weightHBTag1p_{sfvar}-(weightSBTag0_{sfvar}*weightHBTag1_{sfvar})))".format(sfvar=sfvar)#"( (nBJet>=2)     && (nBHardJet>=1) )"
        
        
        
        self.btag_to_sf = {
                             self.btag_veto_soft_bjet        :  self.sf_veto_soft_bjet          ,  
                             self.btag_one_soft_bjet         :  self.sf_one_soft_bjet           , 
                             self.btag_one_or_more_soft_bjet :  self.sf_one_or_more_soft_bjet   , 
                             self.btag_veto_hard_bjet        :  self.sf_veto_hard_bjet          , 
                             self.btag_one_hard_bjet         :  self.sf_one_hard_bjet           , 
                             self.btag_one_or_more_hard_bjet :  self.sf_one_or_more_hard_bjet   , 
                             self.btag_veto_bjet             :  self.sf_veto_bjet               ,     
                             self.btag_one_bjet              :  self.sf_one_bjet                , 
                             self.btag_one_or_more_bjet      :  self.sf_one_or_more_bjet        ,
                             self.btag_two_or_more_bjet      :  self.sf_two_or_more_bjet        , 
         
                             self.btag_sr1_bjet              :  self.sf_sr1_bjet                , 
                             self.btag_sr2_bjet              :  self.sf_sr2_bjet                , 
                             self.btag_cr1_bjet              :  self.sf_cr1_bjet                , 
                             self.btag_cr2_bjet              :  self.sf_cr2_bjet                , 
                             self.btag_crtt1_bjet            :  self.sf_crtt1_bjet              , 
                             self.btag_crtt2_bjet            :  self.sf_crtt2_bjet              , 
                        }
             
        self.sf_to_btag = dict(   (reversed(item) for item in self.btag_to_sf.items() ) )

        self.btag_to_weight_vars ={
                                'nBJet'     :   'weightBTag%s_{sfvar}'.format(sfvar=sfvar)     , 
                                'nBSoftJet' :   'weightSBTag%s_{sfvar}'.format(sfvar=sfvar)     , 
                                'nBHardJet' :   'weightHBTag%s_{sfvar}'.format(sfvar=sfvar)     , 
                                #'nBSoftJet' :   'weightSBTag%s_{sfvar} * weightHBTag0_{sfvar}'.format(sfvar=sfvar)     , 
                                #'nBHardJet' :   'weightHBTag%s_{sfvar} * weightSBTag0_{sfvar}'.format(sfvar=sfvar)     , 
                              }
        
        self.weight_to_btag_vars = dict(   (reversed(item) for item in self.btag_to_weight_vars.items() ) )

