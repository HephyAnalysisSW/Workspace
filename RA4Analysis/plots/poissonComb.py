from math import *

def poissonCDF(n,l):
  if not n<float('inf') or not l<float('inf'):
    return float('nan')
  res = 0.
#  expml = exp(-l)
#  if
  for i in range(0, n+1):
#    sum+=expml*l**i/factorial(i)
    res+=exp(-l + sum([log(l) - log(k) for k in range(1, i+1)])) 
  return res

from scipy.special import gammaln
def smearedPoissonCDF(n,l,s):
  if not n<float('inf') or not l<float('inf') or not s<float('inf'):
    return float('nan')
  res=0.
#  print n,l,s
  for i in range(0, n+1):
#    res+=exp((l**2*log(l))/s**2 + 2*i*log(s) + (-i - l**2/s**2)*log(l + s**2) - gammaln(1 + i) + gammaln(i + l**2/s**2) - gammaln(l**2/s**2))
    res+=exp(i*log(l) + 2*i*log(s) + (-i - 1./(s*s))*log(1. + l*s*s) - gammaln(1 + i) + gammaln(i + 1./(s*s)) - gammaln(1./(s*s)))
#  print res
  return res


#L = 1
#
#nb1 = 5
#lb1 = nb1
#sigEff_1=0.5
#
#nb2 = 5
#lb2 = nb2
#sigEff_2=0.5

#pbg1 = pcdf(nb1, lb1)
#pbg2 = pcdf(nb2, lb2)
#
#stest=0
#while 1:
#  stest+=.1
#  p1 = pcdf ( nb1, lb1 + sigEff_1*L*stest ) / pbg1
#  if p1<0.05:
#    print "Excluded",stest
#    break
#
#stest=0
#while 1:
#  stest+=.1
#  p1 = pcdf ( nb1, lb1 + sigEff_1*L*stest ) / pbg1
#  p2 = pcdf ( nb2, lb2 + sigEff_2*L*stest ) / pbg2
#  if p1*p2<0.05:
#    print "Excluded",stest
#    break
#del p1, p2

from scipy.optimize import fsolve

L = 1

nb1 = 5
lb1 = nb1
sigEff_1=0.25

nb2 = 5
lb2 = nb2
sigEff_2=0.5

def p(s, nb, lb, sigEff, smearing=0):
  if lb<=0. or nb<0.:
    return float('nan')
  if smearing==0:
    norm = poissonCDF(nb, lb)
    if norm==0:
      print "Warning! poissonCDF(nb, lb) = 0 for nb, lb", nb, lb
    return poissonCDF (nb, lb + sigEff*L*s)/poissonCDF(nb, lb)
  else:
    return smearedPoissonCDF (nb, lb + sigEff*L*s, smearing)/smearedPoissonCDF(nb, lb, smearing)
#def p2(s, nb2):
#  return pcdf (nb2, lb2 + sigEff_2*L*s)/pcdf(nb2, lb2)

for smearing in [0, 0.01, 0.1, 0.2]:
  ulim1  =  fsolve(lambda s: p(s, int(nb1), lb1, sigEff_1, smearing)-0.05, 0.) 
  ulim2  =  fsolve(lambda s: p(s, int(nb2), lb2, sigEff_2, smearing)-0.05, 0.) 
  ulim12 =  fsolve(lambda s: p(s, int(nb1), lb1, sigEff_1, smearing)*p(s, nb2, lb2, sigEff_2, smearing)-0.05, 0.) 
  ulimSum =  fsolve(lambda s: p(s, int(nb1+nb2), lb1+lb2, sigEff_1+sigEff_2, smearing) - 0.05, 0. )
  print "Example: nb1",nb1,"lb1",lb1,"eff1",sigEff_1,"nb2",nb2,"sigEff_2",sigEff_2, "using smearing", smearing
  print "Combining limits with known background estimates: ulim1", ulim1, "ulim2",ulim2, "ulim12", ulim12,"ulimSum", ulimSum

L = 1

#nb1 = 5
s95_1 = 10.
eff_1=0.5

s95_2 = 10.
eff_2=0.5

for smearing in [0, .01,  0.1, 0.2]:
  bgeff_1 = fsolve(lambda b: p(s95_1, round(b), b, eff_1, smearing)-0.05, 10)
  bgeff_2 = fsolve(lambda b: p(s95_2, round(b), b, eff_2, smearing)-0.05, 10)
  print "Example: s95_1",s95_1,"eff1",eff_1,"s95_2",s95_2,"eff2",eff_2, "found bgeff1 ",bgeff_1, "bgeff2",bgeff_2, " w/ smearing",smearing
  ulim12 =  fsolve(lambda s: p(s, round(bgeff_1), bgeff_1, eff_1, smearing)*p(s, round(bgeff_2), bgeff_2, eff_2,smearing)-0.05, 0.1)
#  print ulim12 
  print "Combining s95 exclusion limits: ulim1", s95_1, "ulim2",s95_2, "ulim12", ulim12, "smearing",smearing

