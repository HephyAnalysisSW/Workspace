model=$6

for i in `seq $1 $5 $2`; 
do
  tops="-99"
  for j in `seq $3 $5 $4`; 
    do
    unset diff
    diff=`echo "scale=2;${i} - ${j}" |bc`
    unset n1stop
    n1stop=`echo "scale=2;${i} - 90" |bc`
    echo  model $model and $diff

    if [ $diff -ge $tops  ] ; then
      echo Working for GoGo_2j_${i}_${j}...
      name=${model}_${i}_${j}
      #ls /pnfs/iihe/cms/store/user/alkaloge/8TeV/T2tt_2j_MG5v1.5.4/T2tt_2j_noProcessed/8TeV_T2tt_2j_${i}_${j}_*unw*.lhe*  > files
      ls /data/schoef/lhe/undecayed_gluino_gluino/gz/8TeV_GoGo_2j_${i}_${j}_*unw*.lhe*  > files
      #just 400k per point...
      cat files | head -4 > files2 ; mv files2 files

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
      grep -c "<event>" temp_dir/8TeV_${name}_run*.lhe >> 8TeV_${name}
      unset events
      #events=`cat 8TeV_${name}  | head -4 | awk -F ":" '{print $2}' | gawk '{ sum += $1 }; END { print sum }'`
      events=`cat 8TeV_${name}  | awk -F ":" '{print $2}' | gawk '{ sum += $1 }; END { print sum }'`
      rm 8TeV_${name}

      echo Now will merge all events...for a total of $events
      #skip this if you want to use a template banner for a specific Model

      #preparing the banner

      #cp param_card_${model}_template.dat banner.txt
      cp template_param_card_T5lnu_AllDecays.dat banner.txt

#      echo "Here" $i $j 
#      while read line
#        do
#        unset stop
#        unset n1
#        unset width
#        stop=`echo $line | awk '{print $1}'`
#        n1=`echo $line | awk '{print $2}'`
#        width=`echo $line | awk '{print $3}'`
#        echo "Here", $stop $n1 $width
#        if [[ $i == $stop && $j == $n1 ]] ; then
#
#          echo $i = stop $j= $n1 and width $width
#
#          sed -i 's/MCHA/200/g' banner.txt
#          sed -i 's/MGLUINO/'$stop'/g'  banner.txt
#          sed -i 's/MLSP/'$n1'/g'  banner.txt
#        fi
#        done<Widths_incl
      sed -i 's/MCHA/200/g' banner.txt
      sed -i 's/MGLUINO/'$i'/g'  banner.txt
      sed -i 's/MLSP/'$j'/g'  banner.txt
      perl merge-pl temp_dir/8TeV_GoGo_2j_${i}_${j}_*.lhe  8TeV_${name}_run1_${events}evnt.lhe.gz  banner.txt

      cat 8TeV_GoGo |  awk 'BEGIN{FS="'$i' GeV"}//{print $2}' |  awk 'BEGIN{FS="±"}//{print $1}' > xsec
      #sed -i '/^$/d' xsec
      unset nlo
      nlo=`cat xsec`
      rm xsec
      #echo $nlo

      events="400000"
      unset file
      file=8TeV_${name}_run1_${events}evnt.lhe
      gzip -d $file.gz


      #slha_line=`awk '/<slha>/{print NR }' 8TeV_${name}_run1_${events}evnt.lhe`
      #sed -e '/<slha>/,/<\/slha>/d' 8TeV_${name}_run1_${events}evnt.lhe > temp_lhe
      #sed -i ''$slha_line'r param_card_${i}_${j}.dat' temp_lhe
      tag_model=GoGo_${i}_${j}
      echo please check that the model is $model , $name  and the xsec if $nlo for $i GeV mass
      #sed  -e 's/<\/event>/# model '${tag_model}'  '${nlo}' \n<\/event>/g' $file > temp 

      echo sed  -e 's/<\/event>/# model '${tag_model}' '${nlo}'\n<\/event>/g' $file  > com ; sed -i "s/ s/ 's/g" com ; sed -i "s/g/ g'/g" com
      source com > temp.lhe

      mkdir PostProcessed

      if [ $i -lt 550 ]
        then
          qcut=44
        fi

      if [ $i -gt 550 ]
        then
          qcut=46
        fi
      python  mgPostProcv2.py  -o temp2.lhe -j 5 -q 44 -e 5 -s temp.lhe
      mv temp2.lhe PostProcessed/8TeV_${name}_run1_${events}evnt.lhe

      #slha_line=`awk '/<slha>/{print NR }' 8TeV_${name}_run1_${events}evnt.lhe`
      #sed -e '/<slha>/,/<\/slha>/d' 8TeV_${name}_run1_${events}evnt.lhe > temp_lhe
      #sed -i ''$slha_line'r param_card_${i}_${j}.dat' temp_lhe

      fi
    fi
  done
done
