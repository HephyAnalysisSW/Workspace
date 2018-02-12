#! /bin/sh

olddir='/dpm/oeaw.ac.at/home/cms/store/user/mzarucki/T2tt_dM-10to80_mStop-500_mLSP-460_privGridpack_GEN-SIM/T2tt_dM-10to80_mStop-500_mLSP-460_HLT_SoftTriggers-V15_PU_HLTDEBUG/180130_231149/0000'
newdir='/dpm/oeaw.ac.at/home/cms/store/user/mzarucki/T2tt_dM-10to80_mStop-500_mLSP-460_privGridpack_GEN-SIM/T2tt_dM-10to80_mStop-500_mLSP-460_HLT_SoftTriggers-V15_PU2/180130_231149/0000'

for name in `dpns-ls $olddir`
do
  if [[ $name =~ ^T2tt_dM-10to80_mStop-500_mLSP-460_HLT_SoftTriggers-V15_PU_HLTDEBUG_([0-9]+).root$ ]]
  then
      newname="T2tt_dM-10to80_mStop-500_mLSP-460_HLT_SoftTriggers-V15_PU2_${BASH_REMATCH[1]}.root"
      dpns-rename $olddir/$name $newdir/$newname
  fi
done
