




btag_veto_soft_bjet          = '(nBSoftJet == 0 )'
btag_one_soft_bjet           = '(nBSoftJet == 1 )'
btag_one_or_more_soft_bjet   = '(nBSoftJet >= 1 )'
btag_veto_hard_bjet          = '(nBHardJet == 0 )'
btag_one_hard_bjet           = '(nBHardJet == 1 )'
btag_one_or_more_hard_bjet   = '(nBHardJet >= 1 )'
btag_veto_bjet               = '((nBHardJet + nBSoftJet)== 0 )'
btag_one_bjet                = '((nBHardJet + nBSoftJet)== 1 )'
btag_one_or_more_bjet        = '((nBHardJet + nBSoftJet)>= 1 )'
btag_two_or_more_bjet        = '((nBHardJet + nBSoftJet)>= 2 )'
btag_sr1_bjet                =  btag_veto_bjet
btag_sr2_bjet                =  "( (nBSoftJet>=1) && (nBHardJet==0) )"
btag_cr1_bjet                =  btag_veto_bjet
btag_cr2_bjet                =  "( (nBSoftJet>=1) && (nBHardJet==0)  )"
btag_crtt1_bjet              =  "( (nBSoftJet==0) && (nBHardJet==1)  )"
btag_crtt2_bjet              =  "( (nBJet>=2)     && (nBHardJet>=1) )"




sf_veto_soft_bjet         = '(weightSBTag0_SF)'
sf_one_soft_bjet          = '(weightSBTag1_SF)'
sf_one_or_more_soft_bjet  = '(weightSBTag1p_SF)'
sf_veto_hard_bjet         = '(weightHBTag0_SF)'
sf_one_hard_bjet          = '(weightHBTag1_SF)'
sf_one_or_more_hard_bjet  = '(weightHBTag1p_SF)'
sf_veto_bjet              = '(weightBTag0_SF)'
sf_one_bjet               = '(weightBTag1_SF)'
sf_one_or_more_bjet       = '(weightBTag1p_SF)'
sf_two_or_more_bjet       = '(weightBTag2p_SF)'

sf_sr1_bjet                =  sf_veto_bjet
sf_sr2_bjet                =  "(weightSBTag1p_SF * weightHBTag0_SF)"
sf_cr1_bjet                =  sf_veto_bjet
sf_cr2_bjet                =  "(weightSBTag1p_SF * weightHBTag0_SF)" #"( (nBSoftJet>=1) && (nBHardJet==0)  )"
sf_crtt1_bjet              =  "(weightSBTag0_SF  * weightHBTag1_SF)" #"( (nBSoftJet==0) && (nBHardJet==1)  )"
sf_crtt2_bjet              =  "((weightHBTag1p_SF-(weightSBTag0_SF*weightHBTag1_SF)))"#"( (nBJet>=2)     && (nBHardJet>=1) )"



btag_to_sf = {
                    btag_veto_soft_bjet        :  sf_veto_soft_bjet          ,  
                    btag_one_soft_bjet         :  sf_one_soft_bjet           , 
                    btag_one_or_more_soft_bjet :  sf_one_or_more_soft_bjet   , 
                    btag_veto_hard_bjet        :  sf_veto_hard_bjet          , 
                    btag_one_hard_bjet         :  sf_one_hard_bjet           , 
                    btag_one_or_more_hard_bjet :  sf_one_or_more_hard_bjet   , 
                    btag_veto_bjet             :  sf_veto_bjet               ,     
                    btag_one_bjet              :  sf_one_bjet                , 
                    btag_one_or_more_bjet      :  sf_one_or_more_bjet        ,
                    btag_two_or_more_bjet      :  sf_two_or_more_bjet        , 

                    btag_sr1_bjet              :  sf_sr1_bjet                , 
                    btag_sr2_bjet              :  sf_sr2_bjet                , 
                    btag_cr1_bjet              :  sf_cr1_bjet                , 
                    btag_cr2_bjet              :  sf_cr2_bjet                , 
                    btag_crtt1_bjet            :  sf_crtt1_bjet              , 
                    btag_crtt2_bjet            :  sf_crtt2_bjet              , 
               }
    
sf_to_btag = dict(   (reversed(item) for item in btag_to_sf.items() ) )



btag_to_weight_vars ={
                        'nBJet'     :   'weightBTag%s_SF'     , 
                        'nBSoftJet' :   'weightSBTag%s_SF'     , 
                        'nBHardJet' :   'weightHBTag%s_SF'     , 
                      }

weight_to_btag_vars = dict(   (reversed(item) for item in btag_to_weight_vars.items() ) )

