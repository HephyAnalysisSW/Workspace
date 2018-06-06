#! /bin/sh

mStop=500
mLSP=460

olddir='/dpm/oeaw.ac.at/home/cms/store/user/mzarucki/SMS-T2tt_dM-10to80_mStop-500_mLSP-420_privGridpack_GEN-SIM/T2tt_dM-10to80_mStop-500_mLSP-420_SoftMuPlusHardJet-V5_HLT_PU/180309_052904/0000/'
newdir='/dpm/oeaw.ac.at/home/cms/store/user/mzarucki/SMS-T2tt_dM-10to80_mStop-500_mLSP-420_privGridpack_GEN-SIM/T2tt_dM-10to80_mStop-500_mLSP-420_SoftMuPlusHardJet-V5_HLT_PU/180309_052904/0000/'

#olddir='/dpm/oeaw.ac.at/home/cms/store/user/mzarucki/SMS-T2tt_dM-10to80_mStop-500_mLSP-460_privGridpack_GEN-SIM/T2tt_dM-10to80_mStop-500_mLSP-460_SoftMuPlusHardJet-V5_HLT_PU/180309_052837/0000'
#newdir='/dpm/oeaw.ac.at/home/cms/store/user/mzarucki/SMS-T2tt_dM-10to80_mStop-500_mLSP-460_privGridpack_GEN-SIM/T2tt_dM-10to80_mStop-500_mLSP-460_SoftMuPlusHardJet-V5_HLT_PU/180309_052837/0000'

#olddir='/dpm/oeaw.ac.at/home/cms/store/user/mzarucki/SMS-T2tt_dM-10to80_mStop-500_mLSP-490_privGridpack_GEN-SIM/T2tt_dM-10to80_mStop-500_mLSP-490_SoftMuPlusHardJet-V5_HLT_PU/180309_052937/0000'
#newdir='/dpm/oeaw.ac.at/home/cms/store/user/mzarucki/SMS-T2tt_dM-10to80_mStop-500_mLSP-490_privGridpack_GEN-SIM/T2tt_dM-10to80_mStop-500_mLSP-490_SoftMuPlusHardJet-V5_HLT_PU/180309_052937/0000'

nameTemplate='T2tt_dM-10to80_mStop-'$mStop'_mLSP-'$mLSP'_SoftMuPlusHardJet-V5_HLT_PU_'
nameTemplateNew='T2tt_mStop-'$mStop'_mLSP-'$mLSP'_SoftMuPlusHardJet-V5_HLT_PU_'

for name in `dpns-ls $olddir`
do
  if [[ $name =~ ^$nameTemplate([0-9]+).root$ ]]
  then
      newname=$nameTemplateNew"${BASH_REMATCH[1]}.root"
      dpns-rename $olddir/$name $newdir/$newname
  fi
done
