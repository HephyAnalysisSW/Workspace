./testMenu2016 -b 1866 -m menu/Slim2E34_SoftTriggers-v5.txt -l ntuple/ntuple_ZeroBias_fill6358_v97p7.list -d results/results_L1Menu-v5_ZeroBias-2017F_fill6358_v97p7      --UseUnpackTree --doPrintPU -u menu/runlumi_fill_6358.csv
./testMenu2016 -b 1866 -m menu/Slim2E34_SoftTriggers-v5.txt -l ntuple/ntuple_ZeroBias_fill6358_v97p7.list -d results/results_L1Menu-v5_ZeroBias-2017F_fill6358_v97p7/PU55 --UseUnpackTree --SelectLS '[535,584]' --SelectRun 306091
./testMenu2016 -b 1866 -m menu/Slim2E34_SoftTriggers-v5.txt -l ntuple/ntuple_ZeroBias_fill6358_v97p7.list -d results/results_L1Menu-v5_ZeroBias-2017F_fill6358_v97p7/PU50 --UseUnpackTree --SelectLS '[36,93]'   --SelectRun 306092

./testMenu2016 -b 1866 -m menu/Slim2E34_SoftTriggers-v5.txt -l ntuple/ntuple_ZeroBias_fill6358_Hui.list -d results/results_L1Menu-v5_ZeroBias-2017F_fill6358_Hui      --UseUnpackTree --doPrintPU -u menu/runlumi_fill_6358.csv 
./testMenu2016 -b 1866 -m menu/Slim2E34_SoftTriggers-v5.txt -l ntuple/ntuple_ZeroBias_fill6358_Hui.list -d results/results_L1Menu-v5_ZeroBias-2017F_fill6358_Hui/PU55 --UseUnpackTree --SelectLS '[535,584]' --SelectRun 306091
./testMenu2016 -b 1866 -m menu/Slim2E34_SoftTriggers-v5.txt -l ntuple/ntuple_ZeroBias_fill6358_Hui.list -d results/results_L1Menu-v5_ZeroBias-2017F_fill6358_Hui/PU50 --UseUnpackTree --SelectLS '[36,93]'   --SelectRun 306092

./testMenu2016 -b 1866 -m menu/Slim2E34_SoftTriggers-v5.txt -l ntuple/ntuple_ZeroBiasBunchTrains_PU55.list -d results/results_L1Menu-v5_ZeroBiasBunchTrains_PU55 --UseUnpackTree
