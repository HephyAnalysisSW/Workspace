#/bin/env bash


CMDDIR=$LCG_LOCATION/bin/dpm
[ "$LCG_LOCATION" == "/opt/lcg" ] && CMDDIR=$LCG_LOCATION/bin

ROOT=/dpm/oeaw.ac.at/home/cms/store/user/$USER

IS_FILE=`echo $1 | grep root | wc -l`;

[ $IS_FILE -eq 1 ] &&
{
  $CMDDIR/rfcp $ROOT/$1 $2;
  exit 0;
}

# NUMS=`seq 10000`;
NUMS=`ls.sh $1 | sed -e 's/.* //'`; ## | grep edproducts | sed -e 's/.*edproducts_//' | sed -e 's/.root//'`

echo "nums $NUMS"

/usr/bin/test -e $2 || mkdir -p $2

for i in $NUMS; do
  echo "$CMDDIR/rfcp $ROOT/$1/$i $2/"
  test -e $2/$i && echo "skipping existing $2/$i"
  test -e $2/$i || $CMDDIR/rfcp $ROOT/$1/$i $2/
done
