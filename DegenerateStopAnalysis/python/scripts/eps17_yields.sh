!redoyields="" #--redo_yields
!fakeEst=--postFuncs=fakeEstimate
!cuts=bins_mtct_sum
!sigOpt=t2tt
!jetThresh=def
!skim=filterMETHT250
!generalTag="" #--generalTag=May17_v3

#!redoyields="" #--redo_yields
#!fakeEst=--postFuncs=fakeEstimate
#!cuts=bins_sum
#!sigOpt=t2tt

#!redoyields="" #--redo_yields
#!fakeEst=--postFuncs=fakeEstimate
#!cuts=bins_sum_vr1
#!sigOpt=bm

#central 
python  degStop.py -- --cfg=EPS17_v0 --task=yields  --skim={skim} {generalTag} --lepCol=LepGood --lep=lep  --sigOpt={sigOpt}  --bkgs ttx vv qcd st z dy tt_1l tt_2l w --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights sf prompt pu isr_tt  wpt trig_eff lepsffix  --cut={cuts}   {redoyields}  {fakeEst}
python  degStop.py -- --cfg=EPS17_v0 --task=yields  --skim={skim} {generalTag} --lepCol=LepGood --lep=el   --sigOpt={sigOpt}  --bkgs ttx vv qcd st z dy tt_1l tt_2l w --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights sf prompt pu isr_tt  wpt trig_eff lepsffix  --cut={cuts}   {redoyields}  
python  degStop.py -- --cfg=EPS17_v0 --task=yields  --skim={skim} {generalTag} --lepCol=LepGood --lep=mu   --sigOpt={sigOpt}  --bkgs ttx vv qcd st z dy tt_1l tt_2l w --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights sf prompt pu isr_tt  wpt trig_eff lepsffix  --cut={cuts}   {redoyields} 

#wpt
python  degStop.py -- --cfg=EPS17_v0 --task=yields  --skim={skim} {generalTag} --lepCol=LepGood --lep=lep  --sigOpt=bm        --bkgs ttx vv qcd st z dy tt_1l tt_2l w --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights sf prompt pu isr_tt  trig_eff lepsffix  --cut={cuts}   {redoyields}  {fakeEst}
python  degStop.py -- --cfg=EPS17_v0 --task=yields  --skim={skim} {generalTag} --lepCol=LepGood --lep=el   --sigOpt=bm        --bkgs ttx vv qcd st z dy tt_1l tt_2l w --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights sf prompt pu isr_tt  trig_eff lepsffix  --cut={cuts}   {redoyields}  
python  degStop.py -- --cfg=EPS17_v0 --task=yields  --skim={skim} {generalTag} --lepCol=LepGood --lep=mu   --sigOpt=bm        --bkgs ttx vv qcd st z dy tt_1l tt_2l w --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights sf prompt pu isr_tt  trig_eff lepsffix  --cut={cuts}   {redoyields} 

#tt_isr
python  degStop.py -- --cfg=EPS17_v0 --task=yields  --skim={skim} {generalTag} --lepCol=LepGood --lep=lep  --sigOpt=bm        --bkgs ttx vv qcd st z dy tt_1l tt_2l w  --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights sf prompt pu  wpt trig_eff lepsffix  --cut={cuts}   {redoyields}  {fakeEst}
python  degStop.py -- --cfg=EPS17_v0 --task=yields  --skim={skim} {generalTag} --lepCol=LepGood --lep=el   --sigOpt=bm        --bkgs ttx vv qcd st z dy tt_1l tt_2l w  --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights sf prompt pu  wpt trig_eff lepsffix  --cut={cuts}   {redoyields}  
python  degStop.py -- --cfg=EPS17_v0 --task=yields  --skim={skim} {generalTag} --lepCol=LepGood --lep=mu   --sigOpt=bm        --bkgs ttx vv qcd st z dy tt_1l tt_2l w  --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights sf prompt pu  wpt trig_eff lepsffix  --cut={cuts}   {redoyields} 

#pu down
python  degStop.py -- --cfg=EPS17_v0 --task=yields  --skim={skim} {generalTag} --lepCol=LepGood --lep=lep  --sigOpt=bm        --bkgs ttx vv qcd st z dy tt_1l tt_2l w --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights sf prompt pu_down  isr_tt wpt trig_eff lepsffix  --cut={cuts}   {redoyields}  {fakeEst} 
python  degStop.py -- --cfg=EPS17_v0 --task=yields  --skim={skim} {generalTag} --lepCol=LepGood --lep=el   --sigOpt=bm        --bkgs ttx vv qcd st z dy tt_1l tt_2l w --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights sf prompt pu_down  isr_tt wpt trig_eff lepsffix  --cut={cuts}   {redoyields}  
python  degStop.py -- --cfg=EPS17_v0 --task=yields  --skim={skim} {generalTag} --lepCol=LepGood --lep=mu   --sigOpt=bm        --bkgs ttx vv qcd st z dy tt_1l tt_2l w --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights sf prompt pu_down  isr_tt wpt trig_eff lepsffix  --cut={cuts}   {redoyields}  

#pu up
python  degStop.py -- --cfg=EPS17_v0 --task=yields  --skim={skim} {generalTag} --lepCol=LepGood --lep=lep  --sigOpt=bm        --bkgs ttx vv qcd st z dy tt_1l tt_2l w --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights sf prompt pu_up  isr_tt wpt trig_eff lepsffix  --cut={cuts}   {redoyields}  {fakeEst} 
python  degStop.py -- --cfg=EPS17_v0 --task=yields  --skim={skim} {generalTag} --lepCol=LepGood --lep=el   --sigOpt=bm        --bkgs ttx vv qcd st z dy tt_1l tt_2l w --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights sf prompt pu_up  isr_tt wpt trig_eff lepsffix  --cut={cuts}   {redoyields} 
python  degStop.py -- --cfg=EPS17_v0 --task=yields  --skim={skim} {generalTag} --lepCol=LepGood --lep=mu   --sigOpt=bm        --bkgs ttx vv qcd st z dy tt_1l tt_2l w --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights sf prompt pu_up  isr_tt wpt trig_eff lepsffix  --cut={cuts}   {redoyields} 

#b_l_down
python  degStop.py -- --cfg=EPS17_v0 --task=yields  --skim={skim} {generalTag} --lepCol=LepGood --lep=lep  --sigOpt={sigOpt}  --bkgs ttx vv qcd st z dy tt_1l tt_2l w --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights sf_l_down prompt pu  isr_tt wpt trig_eff lepsffix  --cut={cuts}   {redoyields}  {fakeEst} 
python  degStop.py -- --cfg=EPS17_v0 --task=yields  --skim={skim} {generalTag} --lepCol=LepGood --lep=el   --sigOpt={sigOpt}  --bkgs ttx vv qcd st z dy tt_1l tt_2l w --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights sf_l_down prompt pu  isr_tt wpt trig_eff lepsffix  --cut={cuts}   {redoyields} 
python  degStop.py -- --cfg=EPS17_v0 --task=yields  --skim={skim} {generalTag} --lepCol=LepGood --lep=mu   --sigOpt={sigOpt}  --bkgs ttx vv qcd st z dy tt_1l tt_2l w --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights sf_l_down prompt pu  isr_tt wpt trig_eff lepsffix  --cut={cuts}   {redoyields} 

#b_l_up
python  degStop.py -- --cfg=EPS17_v0 --task=yields  --skim={skim} {generalTag} --lepCol=LepGood --lep=lep  --sigOpt={sigOpt}  --bkgs ttx vv qcd st z dy tt_1l tt_2l w --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights sf_l_up prompt pu  isr_tt wpt trig_eff lepsffix  --cut={cuts}   {redoyields}   {fakeEst} 
python  degStop.py -- --cfg=EPS17_v0 --task=yields  --skim={skim} {generalTag} --lepCol=LepGood --lep=el   --sigOpt={sigOpt}  --bkgs ttx vv qcd st z dy tt_1l tt_2l w --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights sf_l_up prompt pu  isr_tt wpt trig_eff lepsffix  --cut={cuts}   {redoyields} 
python  degStop.py -- --cfg=EPS17_v0 --task=yields  --skim={skim} {generalTag} --lepCol=LepGood --lep=mu   --sigOpt={sigOpt}  --bkgs ttx vv qcd st z dy tt_1l tt_2l w --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights sf_l_up prompt pu  isr_tt wpt trig_eff lepsffix  --cut={cuts}   {redoyields} 

#b_b_down
python  degStop.py -- --cfg=EPS17_v0 --task=yields  --skim={skim} {generalTag} --lepCol=LepGood --lep=lep  --sigOpt={sigOpt}  --bkgs ttx vv qcd st z dy tt_1l tt_2l w --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights sf_b_down prompt pu  isr_tt wpt trig_eff lepsffix  --cut={cuts}   {redoyields}   {fakeEst}
python  degStop.py -- --cfg=EPS17_v0 --task=yields  --skim={skim} {generalTag} --lepCol=LepGood --lep=el   --sigOpt={sigOpt}  --bkgs ttx vv qcd st z dy tt_1l tt_2l w --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights sf_b_down prompt pu  isr_tt wpt trig_eff lepsffix  --cut={cuts}   {redoyields} 
python  degStop.py -- --cfg=EPS17_v0 --task=yields  --skim={skim} {generalTag} --lepCol=LepGood --lep=mu   --sigOpt={sigOpt}  --bkgs ttx vv qcd st z dy tt_1l tt_2l w --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights sf_b_down prompt pu  isr_tt wpt trig_eff lepsffix  --cut={cuts}   {redoyields} 

#b_b_up
python  degStop.py -- --cfg=EPS17_v0 --task=yields  --skim={skim} {generalTag} --lepCol=LepGood --lep=lep  --sigOpt={sigOpt}  --bkgs ttx vv qcd st z dy tt_1l tt_2l w --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights sf_b_up prompt pu  isr_tt wpt trig_eff lepsffix  --cut={cuts}   {redoyields}   {fakeEst}
python  degStop.py -- --cfg=EPS17_v0 --task=yields  --skim={skim} {generalTag} --lepCol=LepGood --lep=el   --sigOpt={sigOpt}  --bkgs ttx vv qcd st z dy tt_1l tt_2l w --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights sf_b_up prompt pu  isr_tt wpt trig_eff lepsffix  --cut={cuts}   {redoyields} 
python  degStop.py -- --cfg=EPS17_v0 --task=yields  --skim={skim} {generalTag} --lepCol=LepGood --lep=mu   --sigOpt={sigOpt}  --bkgs ttx vv qcd st z dy tt_1l tt_2l w --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights sf_b_up prompt pu  isr_tt wpt trig_eff lepsffix  --cut={cuts}   {redoyields} 

#jec
#python  degStop.py -- --cfg=EPS17_v0 --task=yields --skim={skim} {generalTag}  --lepCol=LepGood --lep=lep --sigOpt={sigOpt}  --bkgs ttx vv qcd st z dy tt_1l tt_2l w --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data="" --weights sf prompt pu  isr_tt wpt trig_eff lepsffix jec_up --cut={cuts}   {redoyields}   {fakeEst}
#python  degStop.py -- --cfg=EPS17_v0 --task=yields --skim={skim} {generalTag}  --lepCol=LepGood --lep=el  --sigOpt={sigOpt}  --bkgs ttx vv qcd st z dy tt_1l tt_2l w --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data="" --weights sf prompt pu  isr_tt wpt trig_eff lepsffix jec_up --cut={cuts}   {redoyields} 
#python  degStop.py -- --cfg=EPS17_v0 --task=yields --skim={skim} {generalTag}  --lepCol=LepGood --lep=mu  --sigOpt={sigOpt}  --bkgs ttx vv qcd st z dy tt_1l tt_2l w --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data="" --weights sf prompt pu  isr_tt wpt trig_eff lepsffix jec_up --cut={cuts}   {redoyields} 
#
#python  degStop.py -- --cfg=EPS17_v0 --task=yields --skim={skim} {generalTag}  --lepCol=LepGood --lep=lep --sigOpt={sigOpt}  --bkgs ttx vv qcd st z dy tt_1l tt_2l w --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data="" --weights sf prompt pu  isr_tt wpt trig_eff lepsffix jec_down --cut={cuts}   {redoyields}   {fakeEst}
#python  degStop.py -- --cfg=EPS17_v0 --task=yields --skim={skim} {generalTag}  --lepCol=LepGood --lep=el  --sigOpt={sigOpt}  --bkgs ttx vv qcd st z dy tt_1l tt_2l w --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data="" --weights sf prompt pu  isr_tt wpt trig_eff lepsffix jec_down --cut={cuts}   {redoyields} 
#python  degStop.py -- --cfg=EPS17_v0 --task=yields --skim={skim} {generalTag}  --lepCol=LepGood --lep=mu  --sigOpt={sigOpt}  --bkgs ttx vv qcd st z dy tt_1l tt_2l w --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data="" --weights sf prompt pu  isr_tt wpt trig_eff lepsffix jec_down --cut={cuts}   {redoyields} 
#
#python  degStop.py -- --cfg=EPS17_v0 --task=yields --skim={skim} {generalTag}  --lepCol=LepGood --lep=lep --sigOpt={sigOpt}  --bkgs ttx vv qcd st z dy tt_1l tt_2l w --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data="" --weights sf prompt pu  isr_tt wpt trig_eff lepsffix jec_central --cut={cuts}   {redoyields}   {fakeEst}
#python  degStop.py -- --cfg=EPS17_v0 --task=yields --skim={skim} {generalTag}  --lepCol=LepGood --lep=el  --sigOpt={sigOpt}  --bkgs ttx vv qcd st z dy tt_1l tt_2l w --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data="" --weights sf prompt pu  isr_tt wpt trig_eff lepsffix jec_central --cut={cuts}   {redoyields} 
#python  degStop.py -- --cfg=EPS17_v0 --task=yields --skim={skim} {generalTag}  --lepCol=LepGood --lep=mu  --sigOpt={sigOpt}  --bkgs ttx vv qcd st z dy tt_1l tt_2l w --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data="" --weights sf prompt pu  isr_tt wpt trig_eff lepsffix jec_central --cut={cuts}   {redoyields} 
#
#python  degStop.py -- --cfg=EPS17_v0 --task=yields --skim={skim} {generalTag}  --lepCol=LepGood --lep=lep --sigOpt={sigOpt}  --bkgs ttx vv qcd st z dy tt_1l tt_2l w --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data="" --weights sf prompt pu  isr_tt wpt trig_eff lepsffix jer_up --cut={cuts}   {redoyields}   {fakeEst}
#python  degStop.py -- --cfg=EPS17_v0 --task=yields --skim={skim} {generalTag}  --lepCol=LepGood --lep=el  --sigOpt={sigOpt}  --bkgs ttx vv qcd st z dy tt_1l tt_2l w --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data="" --weights sf prompt pu  isr_tt wpt trig_eff lepsffix jer_up --cut={cuts}   {redoyields} 
#python  degStop.py -- --cfg=EPS17_v0 --task=yields --skim={skim} {generalTag}  --lepCol=LepGood --lep=mu  --sigOpt={sigOpt}  --bkgs ttx vv qcd st z dy tt_1l tt_2l w --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data="" --weights sf prompt pu  isr_tt wpt trig_eff lepsffix jer_up --cut={cuts}   {redoyields} 
#
#python  degStop.py -- --cfg=EPS17_v0 --task=yields --skim={skim} {generalTag}  --lepCol=LepGood --lep=lep --sigOpt={sigOpt}  --bkgs ttx vv qcd st z dy tt_1l tt_2l w --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data="" --weights sf prompt pu  isr_tt wpt trig_eff lepsffix jer_down --cut={cuts}   {redoyields}   {fakeEst}
#python  degStop.py -- --cfg=EPS17_v0 --task=yields --skim={skim} {generalTag}  --lepCol=LepGood --lep=el  --sigOpt={sigOpt}  --bkgs ttx vv qcd st z dy tt_1l tt_2l w --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data="" --weights sf prompt pu  isr_tt wpt trig_eff lepsffix jer_down --cut={cuts}   {redoyields} 
#python  degStop.py -- --cfg=EPS17_v0 --task=yields --skim={skim} {generalTag}  --lepCol=LepGood --lep=mu  --sigOpt={sigOpt}  --bkgs ttx vv qcd st z dy tt_1l tt_2l w --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data="" --weights sf prompt pu  isr_tt wpt trig_eff lepsffix jer_down --cut={cuts}   {redoyields} 
#
#python  degStop.py -- --cfg=EPS17_v0 --task=yields --skim={skim} {generalTag}  --lepCol=LepGood --lep=lep --sigOpt={sigOpt}  --bkgs ttx vv qcd st z dy tt_1l tt_2l w --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data="" --weights sf prompt pu  isr_tt wpt trig_eff lepsffix jer_central --cut={cuts}   {redoyields}   {fakeEst}
#python  degStop.py -- --cfg=EPS17_v0 --task=yields --skim={skim} {generalTag}  --lepCol=LepGood --lep=el  --sigOpt={sigOpt}  --bkgs ttx vv qcd st z dy tt_1l tt_2l w --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data="" --weights sf prompt pu  isr_tt wpt trig_eff lepsffix jer_central --cut={cuts}   {redoyields} 
#python  degStop.py -- --cfg=EPS17_v0 --task=yields --skim={skim} {generalTag}  --lepCol=LepGood --lep=mu  --sigOpt={sigOpt}  --bkgs ttx vv qcd st z dy tt_1l tt_2l w --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data="" --weights sf prompt pu  isr_tt wpt trig_eff lepsffix jer_central --cut={cuts}   {redoyields} 


##
## Sig Systs
## 


# isr
#python  degStop.py -- --cfg=EPS17_v0 --task=yields  --skim={skim} {generalTag} --lepCol=LepGood --lep=lep  --sigOpt={sigOpt}  --bkgs vv --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights noisrsig sf prompt pu isr_tt  wpt trig_eff lepsffix  --cut={cuts}   {redoyields}  {fakeEst}
#python  degStop.py -- --cfg=EPS17_v0 --task=yields  --skim={skim} {generalTag} --lepCol=LepGood --lep=el   --sigOpt={sigOpt}  --bkgs vv --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights noisrsig sf prompt pu isr_tt  wpt trig_eff lepsffix  --cut={cuts}   {redoyields}  
#python  degStop.py -- --cfg=EPS17_v0 --task=yields  --skim={skim} {generalTag} --lepCol=LepGood --lep=mu   --sigOpt={sigOpt}  --bkgs vv --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights noisrsig sf prompt pu isr_tt  wpt trig_eff lepsffix  --cut={cuts}   {redoyields} 
#
## btag fs up
#python  degStop.py -- --cfg=EPS17_v0 --task=yields  --skim={skim} {generalTag} --lepCol=LepGood --lep=lep  --sigOpt={sigOpt}  --bkgs vv --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights sf_fs_up prompt pu isr_tt  wpt trig_eff lepsffix  --cut={cuts}   {redoyields}  {fakeEst}
#python  degStop.py -- --cfg=EPS17_v0 --task=yields  --skim={skim} {generalTag} --lepCol=LepGood --lep=el   --sigOpt={sigOpt}  --bkgs vv --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights sf_fs_up prompt pu isr_tt  wpt trig_eff lepsffix  --cut={cuts}   {redoyields}  
#python  degStop.py -- --cfg=EPS17_v0 --task=yields  --skim={skim} {generalTag} --lepCol=LepGood --lep=mu   --sigOpt={sigOpt}  --bkgs vv --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights sf_fs_up prompt pu isr_tt  wpt trig_eff lepsffix  --cut={cuts}   {redoyields} 
#
## btag fs down
#python  degStop.py -- --cfg=EPS17_v0 --task=yields  --skim={skim} {generalTag} --lepCol=LepGood --lep=lep  --sigOpt={sigOpt}  --bkgs vv --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights sf_fs_down prompt pu isr_tt  wpt trig_eff lepsffix  --cut={cuts}   {redoyields}  {fakeEst}
#python  degStop.py -- --cfg=EPS17_v0 --task=yields  --skim={skim} {generalTag} --lepCol=LepGood --lep=el   --sigOpt={sigOpt}  --bkgs vv --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights sf_fs_down prompt pu isr_tt  wpt trig_eff lepsffix  --cut={cuts}   {redoyields}  
#python  degStop.py -- --cfg=EPS17_v0 --task=yields  --skim={skim} {generalTag} --lepCol=LepGood --lep=mu   --sigOpt={sigOpt}  --bkgs vv --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights sf_fs_down prompt pu isr_tt  wpt trig_eff lepsffix  --cut={cuts}   {redoyields} 
#
## genmet
#python  degStop.py -- --cfg=EPS17_v0 --task=yields  --skim={skim} {generalTag} --lepCol=LepGood --lep=lep  --sigOpt={sigOpt}  --bkgs vv --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights genmet sf prompt pu isr_tt  wpt trig_eff lepsffix  --cut={cuts}   {redoyields}  {fakeEst}
#python  degStop.py -- --cfg=EPS17_v0 --task=yields  --skim={skim} {generalTag} --lepCol=LepGood --lep=el   --sigOpt={sigOpt}  --bkgs vv --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights genmet sf prompt pu isr_tt  wpt trig_eff lepsffix  --cut={cuts}   {redoyields}  
#python  degStop.py -- --cfg=EPS17_v0 --task=yields  --skim={skim} {generalTag} --lepCol=LepGood --lep=mu   --sigOpt={sigOpt}  --bkgs vv --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights genmet sf prompt pu isr_tt  wpt trig_eff lepsffix  --cut={cuts}   {redoyields} 

python  degStop.py -- --cfg=EPS17_v0 --task=yields   --skim={skim} {generalTag} --lepCol=LepGood --lep=lep   --sigOpt={sigOpt}  --bkgs vv --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights Q2central_central sf prompt pu isr_tt  wpt trig_eff lepsffix  --cut=bins_mtct_sum_sig   {redoyields} 
python  degStop.py -- --cfg=EPS17_v0 --task=yields   --skim={skim} {generalTag} --lepCol=LepGood --lep=lep   --sigOpt={sigOpt}  --bkgs vv --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights Q2central_up      sf prompt pu isr_tt  wpt trig_eff lepsffix  --cut=bins_mtct_sum_sig   {redoyields} 
python  degStop.py -- --cfg=EPS17_v0 --task=yields   --skim={skim} {generalTag} --lepCol=LepGood --lep=lep   --sigOpt={sigOpt}  --bkgs vv --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights Q2central_down    sf prompt pu isr_tt  wpt trig_eff lepsffix  --cut=bins_mtct_sum_sig   {redoyields} 
python  degStop.py -- --cfg=EPS17_v0 --task=yields   --skim={skim} {generalTag} --lepCol=LepGood --lep=lep   --sigOpt={sigOpt}  --bkgs vv --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights Q2up_central      sf prompt pu isr_tt  wpt trig_eff lepsffix  --cut=bins_mtct_sum_sig   {redoyields} 
python  degStop.py -- --cfg=EPS17_v0 --task=yields   --skim={skim} {generalTag} --lepCol=LepGood --lep=lep   --sigOpt={sigOpt}  --bkgs vv --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights Q2up_down         sf prompt pu isr_tt  wpt trig_eff lepsffix  --cut=bins_mtct_sum_sig   {redoyields} 
python  degStop.py -- --cfg=EPS17_v0 --task=yields   --skim={skim} {generalTag} --lepCol=LepGood --lep=lep   --sigOpt={sigOpt}  --bkgs vv --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights Q2down_central    sf prompt pu isr_tt  wpt trig_eff lepsffix  --cut=bins_mtct_sum_sig   {redoyields} 
python  degStop.py -- --cfg=EPS17_v0 --task=yields   --skim={skim} {generalTag} --lepCol=LepGood --lep=lep   --sigOpt={sigOpt}  --bkgs vv --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights Q2down_up         sf prompt pu isr_tt  wpt trig_eff lepsffix  --cut=bins_mtct_sum_sig   {redoyields} 
#python  degStop.py -- --cfg=EPS17_v0 --task=yields   --skim={skim} {generalTag} --lepCol=LepGood --lep=lep   --sigOpt={sigOpt}  --bkgs vv --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights Q2up_up           sf prompt pu isr_tt  wpt trig_eff lepsffix  --cut=bins_mtct_sum_sig   {redoyields} 
#python  degStop.py -- --cfg=EPS17_v0 --task=yields   --skim={skim} {generalTag} --lepCol=LepGood --lep=lep   --sigOpt={sigOpt}  --bkgs vv --nProc=10  --jetThresh={jetThresh}   --lepThresh=lowpt   --data=dblind --weights Q2down_down       sf prompt pu isr_tt  wpt trig_eff lepsffix  --cut=bins_mtct_sum_sig   {redoyields} 

