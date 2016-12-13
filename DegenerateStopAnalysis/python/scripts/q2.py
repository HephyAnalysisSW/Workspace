import pickle
yield_temp = "/afs/hephy.at/work/n/nrad/results/cards_and_limits/8012_mAODv2_v3/80X_postProcessing_v10/13TeV/HT/ApprovalSys_Mt95_Inccharge_LepAll_lep_pu_{qvar}_SF/AdjustedSys/presel/Yields_12864pbm1_ApprovalSys_Mt95_Inccharge_LepAll_lep_pu_{qvar}_SF_presel_BinsSummary.pkl"







qvars     ={
                            1: 'Q2centralcentral'   ,        ## <weight id="1001"> muR=1 muF=1 
                            2: 'Q2centralup'        ,        ## <weight id="1002"> muR=1 muF=2 
                            3: 'Q2centraldown'      ,        ## <weight id="1003"> muR=1 muF=0.5 
                            4: 'Q2upcentral'        ,   ## <weight id="1004"> muR=2 muF=1 
                            5: 'Q2upup'             ,   ## <weight id="1005"> muR=2 muF=2 
                            6: 'Q2updown'           ,   ## <weight id="1006"> muR=2 muF=0.5 
                            7: 'Q2downcentral'      ,     ## <weight id="1007"> muR=0.5 muF=1 
                            8: 'Q2downup'           ,     ## <weight id="1008"> muR=0.5 muF=2 
                            9: 'Q2downdown'         ,     ## <weight id="1009"> muR=0.5 muF=0.5 
                          }



bins    =       [       'SRL1a', 'SRH1a', 'SRV1a',  'SR1a', 
                        'SRL1b', 'SRH1b', 'SRV1b',  'SR1b' ,
                        'SRL1c', 'SRH1c', 'SRV1c',  'SR1c' ,
                        'SRL2', 'SRH2', 'SRV2',     'SR2'  ,
                        'CR1a', 'CR1b', 'CR1c', 'CR2', 'CRTT2']

qyields = {}
qpkls = {}
qyieldDicts = {}
for qvar in qvars.itervalues():
    qpkls[qvar] = yield_temp.format(qvar=qvar)
    qyields[qvar]= pickle.load(file(qpkls[qvar]))
    qyieldDicts[qvar] = qyields[qvar].getNiceYieldDict() 



sigList = [ qyields[qvar].sampleNames[samp] for samp in qyields[qvar].sigList]


qpairs = [
           ( 'Q2centralup' , 'Q2centraldown'  )  ,
           ( 'Q2upcentral' , 'Q2downcentral'  )  ,
           ( 'Q2updown'    , 'Q2downup'  )          ,
          ]

ycen = qyieldDicts['Q2centralcentral']
systs = {}
syst_env ={}
for sig in sigList:
    systs [sig]={}
    syst_env[sig]={}
    for b in bins:
        systs[sig][b]=[]
        for iv, ( var1, var2 ) in enumerate( qpairs):
            y1 = qyieldDicts[var1][sig][b]
            y2 = qyieldDicts[var2][sig][b]
            yc = ycen[sig][b]

            relsys1 = 100 *  abs(1-(y1/yc).val) if yc.val else 0 
            relsys2 = 100 *  abs(1-(y2/yc).val) if yc.val else 0
            averel  = 0.5 * (relsys1 + relsys2 )
            systs[sig][b].append(averel)
        syst_env[sig][b] = max( systs[sig][b] )


systs_range_samples={}
systs_ave = {}
for b in bins:
    mins = min([ (syst_env[sig][b], sig) for sig in sigList])
    maxs = max([ (syst_env[sig][b], sig) for sig in sigList])
    ave =  sum([syst_env[sig][b] for sig in sigList])/len(sigList)
    systs_range_samples[b] = [mins, maxs]
    systs_ave[b] = ave
