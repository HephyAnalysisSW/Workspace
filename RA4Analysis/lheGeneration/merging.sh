model=$6

for i in `seq $1 $5 $2`; 

do

tops="90"

xValue=0.8
xValue2=0.2

for j in `seq $3 $5 $4`; 

do
unset diff
unset chi
chi1=`echo "scale=2;${xValue} * ${j}" |bc`
chi2=`echo "scale=2;${xValue2} * ${i}" |bc`
chi=`echo "scale=2;${chi1} + ${chi2}" |bc`
diff=`echo "scale=2;${i} - ${j}" |bc`
echo  model $model and $diff

#Sufficient HT
if [ $diff -ge 90  ] ; then

echo Working for 8TeV_GoGo_2j_${i}_${j}...

name=${model}_${i}_${j}
#name=T2tt_2j_${i}_${j}

#ls /pnfs/iihe/cms/store/user/alkaloge/8TeV/T2tt_2j_MG5v1.5.4/T2tt_2j_noProcessed/8TeV_T2tt_2j_${i}_${j}_*unw*.lhe*  > files
ls /scratch/hpc/lesya/CMSSW_5_2_6_patch1/src/LHE_T1tttt_400_775/8TeV_GoGo_2j_${i}_${j}_*unw*.lhe*  > files 
#just 400k per point...
cat files | head -1 > files2 ; mv files2 files

if [ ! -f PostProcessed/8TeV_${name}_run1_*.lhe* ] ; then

if [ ! -d temp_dir ] 
then 
mkdir temp_dir
fi
while read line
do
dccp $line temp_dir/.
#echo files..
done<files
gzip -d temp_dir/8TeV_GoGo_2j_${i}_${j}_*.gz
echo Done with copying, and unzipping files...

ls temp_dir/8TeV_GoGo_2j_${i}_${j}_*.lhe > files

read -r firstline<files

#perl extract_banner.pl $firstline banner.txt

echo MODEL ===== $model  , $name
name1=GoGo_2j_${i}_${j}
grep -c "<event>" temp_dir/8TeV_${name1}_run*.lhe >> 8TeV_${name}
#grep -c "<event>" temp_dir/8TeV_T2tt_2j_300_200_run*.lhe >> 8TeV_${name}
unset events
#events=`cat 8TeV_${name}  | head -4 | awk -F ":" '{print $2}' | gawk '{ sum += $1 }; END { print sum }'`
events=`cat 8TeV_${name}  | awk -F ":" '{print $2}' | gawk '{ sum += $1 }; END { print sum }'`
rm 8TeV_${name}

echo Now will merge all events...for a total of $events
#skip this if you want to use a template banner for a specific Model

#preparing the banner

cp param_card_${model}_template.dat banner.txt

#sed -i 's/STOPWIDTH/'$width'/g' banner.txt
sed -i 's/CHARGINO/'$chi'/g'  banner.txt
sed -i 's/LSP/'$j'/g'  banner.txt
sed -i 's/GLUINO/'$i'/g'  banner.txt

gzip -f banner.txt
perl merge-pl temp_dir/8TeV_GoGo_2j_${i}_${j}_*.lhe  8TeV_${name}_run1_${events}evnt.lhe.gz  banner_old.txt banner.txt.gz

cat 8TeV_gluino |  awk 'BEGIN{FS="'$i' GeV"}//{print $2}' |  awk 'BEGIN{FS="±"}//{print $1}' > xsec
#sed -i '/^$/d' xsec
unset nlo
nlo=`cat xsec`
rm xsec
#echo $nlo


#events="400000"
unset file
file=8TeV_${name}_run1_${events}evnt.lhe
gzip -d $file.gz


#slha_line=`awk '/<slha>/{print NR }' 8TeV_${name}_run1_${events}evnt.lhe`
#sed -e '/<slha>/,/<\/slha>/d' 8TeV_${name}_run1_${events}evnt.lhe > temp_lhe
#sed -i ''$slha_line'r param_card_${i}_${j}.dat' temp_lhe
tag_model=T5lnu_${i}_${j}_${chi}_0.8
echo please check that the model is $model , $name  and the xsec if $nlo for $i GeV mass
#sed  -e 's/<\/event>/# model '${tag_model}'  '${nlo}' \n<\/event>/g' $file > temp 

echo sed  -e 's/<\/event>/# model '${tag_model}' '${nlo}'\n<\/event>/g' $file  > com ; sed -i "s/ s/ 's/g" com ; sed -i "s/g/ g'/g" com
source com > temp.lhe

mkdir PostProcessed

if [ $i -lt 760 ]
then
	qcut=45
fi

if [ $i -gt 750 ]
then
	qcut=50
fi
python  mgPostProcv2.py  -o temp2.lhe -j 5 -q 44 -e 5 -s temp.lhe
mv temp2.lhe PostProcessed/8TeV_${name}_run1_${events}evnt.lhe
#sed -i 's/1000006    1/1000005    1/g'  PostProcessed/8TeV_${name}_run1_${events}evnt.lhe
# ; gzip  PostProcessed/8TeV_${name}_run1_${events}evnt.lhe
name_new=${model}_Go_${i}_chi_${chi}_lsp_${j}
mv PostProcessed/8TeV_${name}_run1_${events}evnt.lhe PostProcessed/8TeV_${name_new}_run1_${events}evnt.lhe
gzip  PostProcessed/8TeV_${name_new}_run1_${events}evnt.lhe
#slha_line=`awk '/<slha>/{print NR }' 8TeV_${name}_run1_${events}evnt.lhe`
#sed -e '/<slha>/,/<\/slha>/d' 8TeV_${name}_run1_${events}evnt.lhe > temp_lhe
#sed -i ''$slha_line'r param_card_${i}_${j}.dat' temp_lhe

fi
fi
done
done
