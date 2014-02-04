#!/bin/sh
#
# job index
#
i="$1"
if [ "$i" = "" ]; then
  echo "Error: missing job index"
  exit 1;
fi

set -x

#
# pick ith entry from list of directories
#
n=1
while read -a line
do
if [ "$n" = "$i" ]; then break; fi
let "n += 1"
done < lhedirs.lis
echo $line
echo ${#line}
#
# build comma-separated list of files
#
dpns-ls $line
files=`dpns-ls $line | awk '/.lhe.gz/{print $NF}'`
files=`echo $files | sed 's/ /,/g'`
#
# launch python validation script
#
python -u LHEValidationGrid.py $line $files

exit 0
