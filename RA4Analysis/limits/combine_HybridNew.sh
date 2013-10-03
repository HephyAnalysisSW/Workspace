#!/bin/sh
#########################
#
# Driver script for Toy Monte Carlo submission with CRAB 
#
# author: Luca Lista, INFN
#                      
#########################

if [ -e outputToy ]; then 
  rm -rf outputToy 
fi
mkdir outputToy

i="$1"
if [ "$i" == "help" ]; then
  echo "usage: combine_crab.sh <job index> [<max events>]"
  exit 0;
fi
if [ "$i" = "" ]; then
  echo "Error: missing job index"
  exit 1;
fi
echo "max events from CRAB: $MaxEvents"
n="$MaxEvents" 
if [ "$n" = "" ]; then
  n="$2"
fi
if [ "$n" = "" ]; then
  echo "Error: missing number of experiments"
  exit 2;
fi

# first, link locally the executable:
# ln -s ../../../../bin/slc5_amd64_gcc434/combine .

set -x

quantiles=( '--expectedFromGrid=0.16' '--expectedFromGrid=0.50' '--expectedFromGrid=0.84'  '--expectedFromGrid=0.025' '--expectedFromGrid=0.975' )

n=1
while read -a line
do
if [ "$n" = "$i" ]; then break; fi
let "n += 1"
done < m0m12.lis
echo $line
echo ${#line}


n=0
until [ "${line[$n]}" = "" ]
do
  m0=${line[$n]}
  let "n += 1"
  m12=${line[$n]}

  tar -xf models.tar model_${m0}_${m12}.root
  let "seed = 10000 * ${m0} + ${m12}"
  ./combine model_${m0}_${m12}.root -M Asymptotic > asymptotic.log 2>&1
  if [ $? -ne 0 ]; then
    let "n += 1"
    rm -f model_${m0}_${m12}.root
    continue
  fi
  lim=( `awk -f asymptotic.awk asymptotic.log` )
  if [ $? -ne 0 ]; then
    let "n += 1"
    rm -f model_${m0}_${m12}.root
    continue
  fi
  if [ ${#lim[@]} -lt 2 ]; then
    let "n += 1"
    rm -f model_${m0}_${m12}.root
    continue
  fi

  nr=1
  cargs="model_${m0}_${m12}.root -M HybridNew --frequentist --testStat LHC -T 500 -i 25 --fork 0 -s ${seed}"
  for r in ${lim[@]}; do
    ./combine ${cargs} --singlePoint ${r} --clsAcc 0 --saveToys --saveHybridResult -n Toys${nr}
    let "nr += 1"
  done
  ls higgsCombineToys*.${seed}.root > /dev/null 2>&1
  if [ $? -eq 0 ]; then 
    hadd higgsCombineToys.HybridNew.mH120.${seed}.root higgsCombineToys*.${seed}.root
    rm higgsCombineToys[0-9]*.${seed}.root

    ./combine ${cargs} -H Asymptotic --grid higgsCombineToys.*.${seed}.root --readHybridResult
    for quant in ${quantiles[@]}; do
      ./combine ${cargs} -H Asymptotic --grid higgsCombineToys.*.${seed}.root --readHybridResult ${quant}
    done

    ls higgsCombineTest.*.${seed}*root > /dev/null 2>&1
    if [ $? -eq 0 ]; then
      hadd tmp.root higgsCombineTest.*.${seed}*root
      rm higgsCombineTest.*.${seed}*root
      mv tmp.root higgsCombineTest.HybridNew.mH120.${seed}.root
    fi
  fi

  rm -f model_${m0}_${m12}.root

  let "n += 1"
done

ls
echo "job number: seed #$i with $n toys"
mv higgs*.root outputToy/
cp *.txt outputToy/
mv *.log outputToy/
echo "pack the results"
tar cvfz outputToy.tgz outputToy/
