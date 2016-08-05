


#sig2           =   'T2-4bd-300-220'
#sig1           =   'T2-4bd-300-270'

sig1           =    'S300-270Fast'
sig2           =    'S300-240Fast'


tt             =   'TTJets'
w              =   "WJets"
otherBkg       = ['DYJetsM50', "QCD", "ZJetsInv", "ST", "Diboson"]
allBkg         = [w,tt] + otherBkg
data           = 'DataBlind'
sigs           = [sig1, sig2]
sigs = []
allSamps       = allBkg + sigs + [data]
side_band_name = 'presel_sideBands'
#side_band_name = 'presel_CRs'

mtabc       = ["a","b","c"]
pts         = ["sr","cr"]
#charges     = ["pos","neg"]
charges     = ["pos", "neg"]
side_bands  = [ "ECR1", "ECR2" ] 


#def subtractAndDivide( a,b,c,d,






yld = task_ret['bkg_est'][0][side_band_name]
yldDict = yld.getNiceYieldDict()


sampleMCFraction = lambda s : dict_manipulator( [ yldDict[b] for b in [s,'Total'] ] , func = (lambda a,b: "%s"%round((a/b).val*100,2) ))


sampleFractions = { s:sampleMCFraction(s) for s in  sigs +[w,tt] }

#   #dataMCFraction = lambda s : dict_manipulator( [ yld.getNiceYieldDict()[b] for b in [s,'DataBlind'] ] , func = (lambda a,b: (a/b).round(2) )) 
#   #dataWFraction = dataMCFraction("WJets")
#   
#   MCTTFrac = dict_manipulator( [ yldDict[b] for b in ["DataBlind", "WJets", 'DYJetsM50', "QCD", "ZJetsInv", "TTJets"] ] , func = lambda a,b,c,d,e,f: ( (a-b-c-d-e)/f).round(2) if f.val else 0 )
#   dataWFrac = dict_manipulator(  [ yldDict[b] for b in  ["DataBlind", "TTJets", 'DYJetsM50', "QCD", "ZJetsInv", "WJets"] ] , func = lambda a,b,c,d,e,f: ( (a-b-c-d-e)/f).round(2) if f.val else 0 )
#   
#   dataWBkgSubtracted   = dict_manipulator( [ yldDict[b] for b in ["DataBlind", "TTJets", 'DYJetsM50', "QCD", "ZJetsInv"] ] , func = lambda a,b,c,d,e: ( (a-b-c-d-e)).round(2) )
#   dataTTBkgSubtracted  = dict_manipulator( [ yldDict[b] for b in ["DataBlind", "WJets" , 'DYJetsM50', "QCD", "ZJetsInv"] ] , func = lambda a,b,c,d,e: ( (a-b-c-d-e)).round(2) )
#   
#   ## fract1 = dict_manipulator(  [ subtr ] + [ yldDict[b] for b in  ["WJets"] ] , func = lambda e,f: ( (e)/f).round(2) if f.val else 0 ) 
#   
#   
#   
#   titles  = [ "Region" , "Signal Cont. SR",  "Signal Cont. CR", "TT Frac", "W Frac", "dataMCSF", "Closure" , "Closure CR"]
#   titles2 = [ " "      , "%s/%s"%(sig1[-7:],sig2[-7:]),   "%s/%s"%(sig1[-7:],sig2[-7:])   , ""     ,""  , " "       , ""      , ""  ]
#   align = "{:^20}"*len(titles)
#   print align.format(*titles)
#   print align.format(*titles2)





def fix_region_name(name):
    return name.replace("_","/").replace("pos","Q+").replace("neg","Q-")

yldsByBins = yld.getByBins(yieldDict=yldDict)
def dict_operator ( yldsByBin , keys = [] , func =  lambda *x: sum(x) ):
    """
    use like this dict_operator( yields_sr, keys = ['DataBlind', 'Total'] , func = lambda a,b: a/b)
    """ 
    args = [ yldsByBin[x] for x in keys]
    return func(*args) 


table_legend = [  "region" , "sig_cont_sr", "sig_cont_cr", "w_frac", "w_sf_cr", "closure"  ] 

first_row = True
tt_table_list = []

corrected_yields = {}




#regions =\
#['MTa_ECR1_neg_PTCR',
# 'MTa_ECR1_neg_PTSR',
# 'MTa_ECR1_pos_PTCR',
# 'MTa_ECR1_pos_PTSR',
# 'MTa_ESR1_neg_PTCR',
# 'MTa_ESR1_neg_PTSR',
# 'MTa_ESR1_pos_PTCR',
# 'MTa_ESR1_pos_PTSR',
# 'MTb_ECR1_neg_PTCR',
# 'MTb_ECR1_neg_PTSR',
# 'MTb_ECR1_pos_PTCR',
# 'MTb_ECR1_pos_PTSR',
# 'MTb_ESR1_neg_PTCR',
# 'MTb_ESR1_neg_PTSR',
# 'MTb_ESR1_pos_PTCR',
# 'MTb_ESR1_pos_PTSR',
# 'MTc_ECR1_neg_PTCR',
# 'MTc_ECR1_neg_PTSR',
# 'MTc_ECR1_pos_PTCR',
# 'MTc_ECR1_pos_PTSR',
# 'MTc_ESR1_neg_PTCR',
# 'MTc_ESR1_neg_PTSR',
# 'MTc_ESR1_pos_PTCR',
# 'MTc_ESR1_pos_PTSR',
# 'BCR2_PTCR',
# 'BCR2_PTSR',
# 'BCR2_neg_PTCR',
# 'BCR2_neg_PTSR',
# 'BCR2_pos_PTCR',
# 'BCR2_pos_PTSR']


regions = yld.cutNames 
region_names = sorted( list( set( [x.replace("_PTSR","").replace("_PTCR","") for x in regions] )) )

tt_region_names = [x for x in region_names if "BCR2" in x]
sr1_region_names = [x for x in region_names if "ECR1" in x]

sr2_regions_names = [x for x in region_names if 'BCR1' in x or 'ECR2' in x]

w_region_names = sr1_region_names+sr2_regions_names

##FIX ME
#regions = yld.cutNames
#region_names = regions
#tt_region_names = [x for x in region_names if "CRTT2" in x ]

##
## TT SideBand
##

tt_table_list.append(["\hline"])
for region_name in tt_region_names:
        #region_name = "MT%s"%mt +"_" + side_band +"_"+charge 
        region_sr   = region_name + "_PTSR" 
        region_cr   = region_name + "_PTCR"

        yields_cr = yldsByBins[region_cr]
        yields_sr = yldsByBins[region_sr]

        otherSum_cr = dict_operator ( yields_cr , keys = otherBkg )
        otherSum_sr = dict_operator ( yields_sr , keys = otherBkg )

        yield_tt_cr = yields_cr[tt]
        yield_tt_sr = yields_sr[tt]

        MCTTFrac_cr = yields_cr[tt] / yields_cr['Total']  * 100  
        MCTTFrac_sr = yields_sr[tt] / yields_sr['Total']  * 100

        tt_sf_cr     = dict_operator ( yldsByBins[region_cr] , keys = [ data , w, tt] + otherBkg  , func = lambda a,b,c,*d: (a-b-sum(d))/c)
        tt_sf_sr     = dict_operator ( yldsByBins[region_sr] , keys = [ data , w, tt] + otherBkg  , func = lambda a,b,c,*d: (a-b-sum(d))/c)

        dataTT_cr_mcw    = dict_operator ( yldsByBins[region_cr] , keys = [ data , w] + otherBkg  , func = lambda a,b,*c: a-b-sum(c))
        dataTT_sr_mcw    = dict_operator ( yldsByBins[region_sr] , keys = [ data , w] + otherBkg  , func = lambda a,b,*c: a-b-sum(c))


        exp_tt_cr     = yields_cr[tt] * tt_sf_cr       
        exp_tt_sr     = yields_sr[tt] * tt_sf_cr      
        exp_tt_sr_sr  = yields_sr[tt] * tt_sf_sr   


        closure_tt_cr      =  dataTT_cr_mcw / exp_tt_cr  if exp_tt_cr.val else u_float(0)
        closure_tt_sr      =  dataTT_sr_mcw / exp_tt_sr  if exp_tt_sr.val else u_float(0)
        closure_tt_sr_sr   =  dataTT_sr_mcw / exp_tt_sr_sr  if exp_tt_sr_sr.val else u_float(0)


        exp_w_cr     = yields_cr[w] # MC       
        exp_w_sr     = yields_sr[w] # MC      
        exp_w_sr_sr  = yields_sr[w] # MC   


        exp_cr     =  exp_w_cr      +  exp_tt_cr    + otherSum_cr    
        exp_sr     =  exp_w_sr      +  exp_tt_sr    + otherSum_sr  
        exp_sr_sr  =  exp_w_sr_sr   +  exp_tt_sr_sr + otherSum_sr  

        closure_cr      =  yields_cr[data] / exp_cr  if exp_cr.val else u_float(0)
        closure_sr      =  yields_sr[data] / exp_sr  if exp_sr.val else u_float(0)
        closure_sr_sr   =  yields_sr[data] / exp_sr_sr  if exp_sr_sr.val else 0

        
        exp_cr_mctt     =  exp_w_cr      +  yields_cr[tt]      +  otherSum_cr    
        exp_sr_mctt     =  exp_w_sr      +  yields_sr[tt]      +  otherSum_sr  
        exp_sr_sr_mctt  =  exp_w_sr_sr   +  yields_sr[tt]      +  otherSum_sr  
        closure_cr_mctt      =  yields_cr[data] / exp_cr_mctt  if exp_cr.val else u_float(0)
        closure_sr_mctt      =  yields_sr[data] / exp_sr_mctt  if exp_sr.val else u_float(0)
        closure_sr_sr_mctt   =  yields_sr[data] / exp_sr_sr_mctt  if exp_sr_sr.val else 0


        toPrint = [   
                      ["Region",                fix_region_name( region_name )], 
                      #["Sig. Cont. SR",         sig_cont_ptsr], 
                      #["Sig. Cont. CR",         sig_cont_ptcr], 
                      #["Closure CR",            closure_cr.round(2)],
                      #["Closure SR",            closure_sr_sr.round(2)],
                      ["TT Frac. SR/CR",         "%s/%s"%(MCTTFrac_sr.round(2).val, MCTTFrac_cr.round(2).val )],
                      ['TT SFCR'   , tt_sf_cr.round(2)  ],
                      #['TT SF SR'   , tt_sf_sr.round(2)  ],
                      #["TT Closure SR SFSR",       closure_tt_sr_sr.round(2)],
                      ["TT Closure SR",            closure_tt_sr.round(2)],
                      #["TT Closure CR",         closure_tt_cr.round(2)],
                      #["Closure",               closure_sr.round(2)],

                   ]#dataCR( dataMCsf * yldDict[tt][region_cr]).round(2)  ]


        align = "{:<15}"*len(toPrint)

        if first_row:
            print align.format(*[x[0] for x in toPrint])
            first_row = False
            tt_table_list.append( [x[0] for x in toPrint]  ) 

        print align.format(*[x[1] for x in toPrint])
        tt_table_list.append( [x[1] for x in toPrint])



tt_table = makeSimpleLatexTable( tt_table_list, "TTPtShape.tex", cfg.saveDirs[side_band_name])


tt_region_cr = "BCR2_PTCR"
tt_region_sr = "BCR2_PTSR"

tt_sf_cr     = dict_operator ( yldsByBins[tt_region_cr] , keys = [ data , w, tt] + otherBkg  , func = lambda a,b,c,*d: (a-b-sum(d))/c)
tt_sf_sr     = dict_operator ( yldsByBins[tt_region_sr] , keys = [ data , w, tt] + otherBkg  , func = lambda a,b,c,*d: (a-b-sum(d))/c)

first_row=True
w_table_list = []
#
# W SideBand
#


for region_name in w_region_names:

        region_sr   = region_name + "_PTSR" 
        region_cr   = region_name + "_PTCR"

        w_region_sr   = region_sr 
        w_region_cr   = region_cr

        w_frac = "%s/%s"%( sampleFractions[w][region_sr], sampleFractions[w][region_cr] )

        yields_cr = yldsByBins[region_cr]
        yields_sr = yldsByBins[region_sr]

        otherSum_cr = dict_operator ( yields_cr , keys = otherBkg )
        otherSum_sr = dict_operator ( yields_sr , keys = otherBkg )

        yield_tt_cr = yields_cr[tt]
        yield_tt_sr = yields_sr[tt]

        dataW_cr    = yields_cr[data] - ( yields_cr[tt] * tt_sf_cr  + otherSum_cr )
        dataW_sr    = yields_sr[data] - ( yields_sr[tt] * tt_sf_sr  + otherSum_sr )

        dataW_cr_mctt    = yields_cr[data] - ( yields_cr[tt]  + otherSum_cr )
        dataW_sr_mctt    = yields_sr[data] - ( yields_sr[tt]  + otherSum_sr )

        MCTTFrac_cr = yields_cr[tt] / yields_cr['Total'] 
        MCTTFrac_sr = yields_sr[tt] / yields_sr['Total']

        dataWFrac_cr = yields_cr[w] / yields_cr['Total'] 
        dataWFrac_sr = yields_sr[w] / yields_sr['Total']

        w_sf_cr = dataW_cr / yields_cr[w] if yields_cr[w].val else u_float(0) 
        w_sf_sr = dataW_sr / yields_sr[w] if yields_sr[w].val else u_float(0)
        w_sf_cr_2 = dict_operator ( yields_cr , keys = [ data , tt, w] + otherBkg  , func = lambda a,b,c,*d: (a-b*tt_sf_cr-sum(d))/c if c.val else 0 )

        w_sf_sr_mctt = dict_operator ( yields_sr , keys = [ data , tt, w] + otherBkg  , func = lambda a,b,c,*d: (a-b-sum(d))/c if c.val else 0 )
        w_sf_cr_mctt = dict_operator ( yields_cr , keys = [ data , tt, w] + otherBkg  , func = lambda a,b,c,*d: (a-b-sum(d))/c if c.val else 0 )

        dataTT_cr_mcw    = dict_operator ( yldsByBins[region_cr] , keys = [ data , w] + otherBkg  , func = lambda a,b,*c: a-b-sum(c))
        dataTT_sr_mcw    = dict_operator ( yldsByBins[region_sr] , keys = [ data , w] + otherBkg  , func = lambda a,b,*c: a-b-sum(c))

        dataTT_cr    = dict_operator ( yldsByBins[region_cr] , keys = [ data , w] + otherBkg  , func = lambda a,b,*c: a-b*w_sf_cr-sum(c))
        dataTT_sr    = dict_operator ( yldsByBins[region_sr] , keys = [ data , w] + otherBkg  , func = lambda a,b,*c: a-b*w_sf_sr-sum(c))

        exp_tt_cr     = yields_cr[tt] * tt_sf_cr       
        exp_tt_sr     = yields_sr[tt] * tt_sf_cr      
        exp_tt_sr_sr  = yields_sr[tt] * tt_sf_sr   

        exp_w_cr     = yields_cr[w] * w_sf_cr       
        exp_w_sr     = yields_sr[w] * w_sf_cr      
        exp_w_sr_sr  = yields_sr[w] * w_sf_sr   

        closure_w_cr      =  dataW_cr / exp_w_cr  if exp_w_cr.val else u_float(0)
        closure_w_sr      =  dataW_sr / exp_w_sr  if exp_w_sr.val else u_float(0)
        closure_w_sr_sr   =  dataW_sr / exp_w_sr_sr  if exp_w_sr_sr.val else u_float(0)

        closure_w_cr_mctt      =  dataW_cr_mctt / exp_w_cr  if exp_w_cr.val else u_float(0)
        closure_w_sr_mctt      =  dataW_sr_mctt / exp_w_sr  if exp_w_sr.val else u_float(0)
        closure_w_sr_sr_mctt   =  dataW_sr_mctt / exp_w_sr_sr  if exp_w_sr_sr.val else u_float(0)

        closure_tt_cr      =  dataTT_cr_mcw / exp_tt_cr  if exp_tt_cr.val else u_float(0)
        closure_tt_sr      =  dataTT_sr_mcw / exp_tt_sr  if exp_tt_sr.val else u_float(0)
        closure_tt_sr_sr   =  dataTT_sr_mcw / exp_tt_sr_sr  if exp_tt_sr_sr.val else u_float(0)

        exp_cr     =  exp_w_cr      +  exp_tt_cr    + otherSum_cr    
        exp_sr     =  exp_w_sr      +  exp_tt_sr    + otherSum_sr  
        exp_sr_sr  =  exp_w_sr_sr   +  exp_tt_sr_sr + otherSum_sr  

        closure_cr      =  yields_cr[data] / exp_cr  if exp_cr.val else u_float(0)
        closure_sr      =  yields_sr[data] / exp_sr  if exp_sr.val else u_float(0)
        closure_sr_sr   =  yields_sr[data] / exp_sr_sr  if exp_sr_sr.val else 0

        exp_cr_mctt     =  exp_w_cr      +  yields_cr[tt]      +  otherSum_cr    
        exp_sr_mctt     =  exp_w_sr      +  yields_sr[tt]      +  otherSum_sr  
        exp_sr_sr_mctt  =  exp_w_sr_sr   +  yields_sr[tt]      +  otherSum_sr  
        closure_cr_mctt      =  yields_cr[data] / exp_cr_mctt  if exp_cr.val else u_float(0)
        closure_sr_mctt      =  yields_sr[data] / exp_sr_mctt  if exp_sr.val else u_float(0)
        closure_sr_sr_mctt   =  yields_sr[data] / exp_sr_sr_mctt  if exp_sr_sr.val else 0

        toPrint = [   
                      ["Region",                fix_region_name( region_name) ], 
                      #["Sig. Cont. SR",         sig_cont_ptsr], 
                      #["Sig. Cont. CR",         sig_cont_ptcr], 
                      #["Closure CR",            closure_cr.round(2)],
                      #["Closure SR",            closure_sr_sr.round(2)],
                      ["TT Frac. SR/CR",         "%s/%s"%(MCTTFrac_sr.round(2).val, MCTTFrac_cr.round(2).val )],
                      ['TT SFCR'   , tt_sf_cr.round(2)  ],
                      ["W Frac. SR/CR",         "%s/%s"%(dataWFrac_sr.round(2).val, dataWFrac_cr.round(2).val )],
                      ["W SFSR",             w_sf_sr.round(2)],
                      ["W SFCR",             w_sf_cr.round(2)],
                      ["W SFCR(MCTT)",      w_sf_cr_mctt.round(2)],
                      #['TT SF SR'   , tt_sf_sr.round(2)  ],
                      ["W Closure",             closure_w_sr.round(2)],
                      ["W Closure CR",          closure_w_cr.round(2)],
                      ["W Closure(MCTT)",       closure_w_sr_mctt.round(2)],
                      ["TT Closure",            closure_tt_sr.round(2)],
                      ["TT Closure CR",            closure_tt_cr.round(2)],
                      ["Closure",               closure_sr.round(2)],

                   ]
        toPrint = [   
                      ["Region",                fix_region_name( region_name) ], 
                      ["W Frac. SR/CR",         "%s/%s"%(dataWFrac_sr.round(2).val, dataWFrac_cr.round(2).val )],
                      ["W SFCR",          w_sf_cr_mctt.round(2)],
                      #["W SFCR (corr. TT)",                w_sf_cr.round(2)],
                      ["W Closure",       closure_w_sr_mctt.round(2)],
                      #["W Closure (Corr. TT)",             closure_w_sr.round(2)],
                      ["Closure",               closure_sr_mctt.round(2)],
                      #["Closure (Corr. TT)",               closure_sr.round(2)],

                   ]#dataCR( dataMCsf * yldDict[tt][region_cr]).round(2)  ]

        #toPrint = [   
        #              ["Region",                region_name], 
        #              #["Sig. Cont. SR",         sig_cont_ptsr], 
        #              #["Sig. Cont. CR",         sig_cont_ptcr], 
        #              ["TT Frac. SR/CR",         "%s/%s"%(MCTTFrac_sr.round(2).val, MCTTFrac_cr.round(2).val )],
        #              ["W Frac. SR/CR",         "%s/%s"%(dataWFrac_sr.round(2).val, dataWFrac_cr.round(2).val )],
        #              #["W SFCR",             w_sf_cr.round(2)],
        #              ["W SFCR(MCTT)",      w_sf_cr_mctt.round(2)],
        #              #['TT SF SR'   , tt_sf_sr.round(2)  ],
        #              ["W Closure(MCTT)",             closure_w_sr_mctt.round(2)],
        #              #["TT Closure",            closure_tt_sr.round(2)],
        #              #["TT Closure CR",            closure_tt_cr.round(2)],
        #              #["Closure",               closure_sr.round(2)],
        #              ["Closure(MCTT)",         closure_sr_mctt.round(2)],

        #           ]#dataCR( dataMCsf * yldDict[tt][region_cr]).round(2)  ]


        align = "{:<15}"*len(toPrint)

        if first_row:
            print align.format(*[x[0] for x in toPrint])
            first_row = False
            w_table_list.append( [x[0] for x in toPrint]  ) 

        print align.format(*[x[1] for x in toPrint])
        w_table_list.append( [x[1] for x in toPrint])



w_table = makeSimpleLatexTable( w_table_list, "WPtShape.tex", cfg.saveDirs[side_band_name])

print tt_table
print w_table
