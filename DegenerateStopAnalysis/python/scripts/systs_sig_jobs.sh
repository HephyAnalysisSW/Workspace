#                   
#                   python   degStop.py -- --cfg=ApprovalSys --task=met_gen  --lepCol=LepAll --lep=lep  --weight=nopu --btag=SF --redo_yields
#                   python   degStop.py -- --cfg=ApprovalSys --task=met_met  --lepCol=LepAll --lep=lep  --weight=nopu --btag=SF --redo_yields
#                   python   degStop.py -- --cfg=ApprovalSys --task=bkg_est  --lepCol=LepAll --lep=lep  --cutInst bins_sum         --weight=nopu_noisr --btag=sf --redo_yields
#                   
#                   
#                   
#                   #python   degStop.py -- --cfg=ApprovalSys --task=bkg_est  --lepCol=LepAll --lep=lep --cutInst bins_sum         --weight=pu --btag=sf --redo_yields  --postFuncs=CF_SFs
#                   #
#                   
#                   python   degStop.py -- --cfg=ApprovalSys --task=bkg_est  --lepCol=LepAll --lep=lep  --cut=bins_sum --weight=pu   --btag=SF_FS_Down   --redo_yields     --postFuncs CR_SFs 
#                   python   degStop.py -- --cfg=ApprovalSys --task=bkg_est  --lepCol=LepAll --lep=lep  --cut=bins_sum --weight=pu   --btag=SF_FS_Up     --redo_yields     --postFuncs CR_SFs 
#                   #
#                   #
#                   #
#                   python   degStop.py -- --cfg=ApprovalSys --task=met_gen --lepCol=LepAll --lep=lep  --weight=pu --btag=SF --redo_yields
#                   python   degStop.py -- --cfg=ApprovalSys --task=met_met --lepCol=LepAll --lep=lep  --weight=pu --btag=SF --redo_yields
#                   #
#                   #

ipython   degStop.py -- --cfg=ApprovalSys --task=bkg_est --lepCol=LepAll --lep=lep  --weight=pu_Q2centralup     --btag=SF  --cut=bins_sum
ipython   degStop.py -- --cfg=ApprovalSys --task=bkg_est --lepCol=LepAll --lep=lep  --weight=pu_Q2centraldown   --btag=SF  --cut=bins_sum
ipython   degStop.py -- --cfg=ApprovalSys --task=bkg_est --lepCol=LepAll --lep=lep  --weight=pu_Q2upcentral     --btag=SF  --cut=bins_sum

#ipython   degStop.py -- --cfg=ApprovalSys --task=bkg_est --lepCol=LepAll --lep=lep  --weight=pu_Q2upup          --btag=SF  --cut=bins_sum

ipython   degStop.py -- --cfg=ApprovalSys --task=bkg_est --lepCol=LepAll --lep=lep  --weight=pu_Q2updown        --btag=SF  --cut=bins_sum
ipython   degStop.py -- --cfg=ApprovalSys --task=bkg_est --lepCol=LepAll --lep=lep  --weight=pu_Q2downcentral   --btag=SF  --cut=bins_sum
ipython   degStop.py -- --cfg=ApprovalSys --task=bkg_est --lepCol=LepAll --lep=lep  --weight=pu_Q2downup        --btag=SF  --cut=bins_sum


#ipython   degStop.py -- --cfg=ApprovalSys --task=bkg_est --lepCol=LepAll --lep=lep  --weight=pu_Q2downdown      --btag=SF --redo_yields --cut=bins_sum

#                   #
#                   #
#                   #
#                   python   degStop.py -- --cfg=ApprovalSys --task=bkg_est  --lepCol=LepAll --lep=lep --cutInst bins_sum         --weight=pu_noisr --btag=sf --redo_yields 
#                   
#                   
#                   
