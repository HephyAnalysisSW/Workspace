#
# read observed / expected limit from file and create
#  20 grid points
#
BEGIN {
  obs=-1;
  ex=-1;
}
/Observed Limit:/ {
  obs = $NF;
}
/Expected 50.*:/ {
  ex = $NF;
}
END {
  if ( obs<=0 || ex<=0 )  exit 1;
  rmax = obs;
  if ( ex>rmax )  rmax = ex;
  rmin = obs;
  if ( ex<rmin )  rmin = ex;
  rmax = log(10*rmax);
  rmin = log(rmin/10);
  dr = (rmax-rmin)/20;
  line = "";
  for ( i=0; i<20; ++i )  line = line " " exp(rmin+(i+0.5)*dr);
  print line;
}
