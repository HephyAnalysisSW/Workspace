#!/bin/sh
######### This step will do the Pythia Decays and puts the banner...Assumes that the in put is a gz file 

for i in `seq $1 $5 $2`
do
for j in `seq $3 $5 $4`
do

dif=` echo "scale=1;$i-$j" |bc`

cent=99


###find file

if [  $dif -gt $cent  ] ;then


#if  [  -f 8TeV_T2tt_2j_${i}_${j}_run1_*.lhe.gz ] ; then
if  [  ! -f files/8TeV_T2tt_${i}_${j}.lhe.gz  ] ; then

unset file
file=`ls 8TeV_T2tt_2j_${i}_${j}_run1*.lhe.gz | awk -F ".gz" '{print $1}'`
unset name
name=T2tt_2j_${i}_${j}

gzip -d $file.gz

##prepare pythia decay , each point one working dir which will be deleted at the end
mkdir work_${i}_${j}
cd work_${i}_${j}


cp ../pythia_decay_template pythia.py
cp ../$file .
sed -i 's/FILEIN/'$file'/g' pythia.py

FILEOUT=${file}_pythia
echo for $file and $FILEOUT

### run decays in pythia and rename fort.69 - This step assumes that you have already setup the correct CMSSW env with the patches provides by Steve -  Before proceeding follow these steps 

#   cvs co UserCode/Mrenna/GeneratorInterface
#   cp -r UserCode/Mrenna/GeneratorInterface/ .
#   cd GeneratorInterface/Pythia6Interface
#   scramv1 b ; cd ../..

### the T2tt_stop_top_neutralino_Woffshell.dat is just a workign example of the SLHA file that tells Pythia how to decay the particles - You can use your own

cp ../T2tt_stop_top_neutralino_Woffshell.dat decay_T2tt_${i}_${j}.dat
sed -i 's/STOPMASS/'${i}'/g' decay_T2tt_${i}_${j}.dat
sed -i 's/LSP/'${j}'/g' decay_T2tt_${i}_${j}.dat

sed -i 's/SLHACARD/decay_T2tt_'${i}'_'${j}'.dat/g' pythia.py

pwd
cmsRun pythia.py
mv fort.69 $FILEOUT


#sed -i 's/QCUT/'$qcut'/'  banner
##ready to hashtag model and matching scales

cp ../hashtag_py hashtag${i}_${j}.py

##put the matching scales into file

#first stip the model hash tag

sed -i '/model T2tt_/d' $file
sed -i 's/first/'$file'/g' hashtag${i}_${j}.py
sed -i 's/second/'$FILEOUT'/g' hashtag${i}_${j}.py
python hashtag${i}_${j}.py
rm hashtag${i}_${j}.py


##tag model
tag_model=T2tt_${i}_${j}

cat ../8TeV_stop |  awk 'BEGIN{FS="'$i' GeV"}//{print $2}' |  awk 'BEGIN{FS="±"}//{print $1}' >xsec${i}_${j}
#sed -i '/^$/d' xsec
unset nlo
nlo=`cat xsec${i}_${j}`
rm xsec${i}_${j}
#echo $nlo
##put model hastag into <event> block
echo  sed -e '1d'   -e 's/<\/event>/# model '${tag_model}' '${nlo}'\n<\/event>/g' $FILEOUT > com${i}_${j} ; sed -i "s/ s/ 's/g" com${i}_${j} ; sed -i "s/g/ g'/g" com${i}_${j}
source com${i}_${j} > temp${i}_${j} ; 
cat ../banner_template > ../files/8TeV_T2tt_${i}_${j}.lhe
cat temp${i}_${j} >> ../files/8TeV_T2tt_${i}_${j}.lhe
#sed -e '1d'  -e '1r banner'  ../files/8TeV_T2tt_${i}_${j}.lhe > temp${i}_${j}${i}_${j}  ; mv temp${i}_${j}${i}_${j}   ../files/8TeV_T2tt_${i}_${j}.lhe 

rm $FILEOUT
rm $FILEOUT~
gzip ../files/8TeV_T2tt_${i}_${j}.lhe

gzip ../8TeV_T2tt_2j_${i}_${j}_run1*.lhe

echo please check that the model is $model , $name  and the xsec if $nlo for $i GeV mass

cd ..

ls work_${i}_${j}
rm -fr work_${i}_${j}
fi
fi
done
done

