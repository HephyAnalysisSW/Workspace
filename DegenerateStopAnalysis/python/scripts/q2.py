import pickle
yield_temp = "/afs/hephy.at/work/n/nrad/results/cards_and_limits/8012_mAODv2_v3/80X_postProcessing_v10/13TeV/HT/ApprovalSys_Mt95_Inccharge_LepAll_lep_pu_{qvar}_SF/AdjustedSys/presel/Yields_12864pbm1_ApprovalSys_Mt95_Inccharge_LepAll_lep_pu_{qvar}_SF_presel_BinsSummary.pkl"







qvars     ={1: 'Q2centralcentral',
            2: 'Q2upcentral',
            3: 'Q2downcentral',
            4: 'Q2centralup',
            5: 'Q2upup',
            6: 'Q2downup',
            7: 'Q2centraldown',
            8: 'Q2updown',
            9: 'Q2downdown'}

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
for b in bins:
    mins = min([ (syst_env[sig][b], sig) for sig in sigList])
    maxs = max([ (syst_env[sig][b], sig) for sig in sigList])
    systs_range_samples[b] = [mins, maxs]
    
