import ROOT, random
from array import array
from math import fabs, exp
from fractions import Fraction, gcd
hequal = ROOT.TH1D("vals", "vals",1000,0.,1.)
for i in range(1000):
  hequal.SetBinContent(i+1, 1)
hequal.Scale(1./hequal.Integral())

hrising = ROOT.TH1D("vals", "vals",1000,0.,1.)
for i in range(1000):
  hrising.SetBinContent(i+1, i)
hrising.Scale(1./hrising.Integral())

hexp = ROOT.TH1D("vals", "vals",1000,0.,1.)
for i in range(1000):
  hexp.SetBinContent(i+1, exp(i/1000.))
hexp.Scale(1./hexp.Integral())


def KolmDist(s0, s1):
  s0.sort()
  s1.sort()

  tot = [[x,0] for x in s0] + [[x,1] for x in s1]
  tot.sort()
  F={}
  lenS={}  
  lenS[0] = len(s0)
  lenS[1] = len(s1)
  F[0] = 0
  F[1] = 0
  l = len(tot)
#  print tot
  maxDist = Fraction(0,1)
  for i, t in enumerate(tot):
#    print "Now",F
    F[t[1]]+=1#lenS[t[1]]
#    print "...",F
    if i+1<l and tot[i+1][0]==t[0]:
      continue
#    print "Calc dist..."
    dist= abs(Fraction(F[0],lenS[0])-Fraction(F[1],lenS[1]))
    if dist>maxDist:
      maxDist=dist
#    print dist, maxDist
  return maxDist 

#dist1 = hrising 
#dist2 = hrising 

NSamples=10000
Nsize1 = 30 
Nsize2 = 29

def getN(N1, N2):
  m     = gcd(N1, N2)
  Nbar1 = N1/m
  Nbar2 = N2/m
  return 1 + m +m*(Nbar1 - 1)*(Nbar2 -1) +m*(Nbar1 + Nbar2 - 2)

#Calculating reference distances
dist1 = hequal
dist2 = hequal
kolmRef = {}
hKolmRef = ROOT.TH1D("ks", "ks",100,0,1)
for i in range(NSamples):
  if (1+i)%(NSamples/10)==0:print (1+i)/(NSamples/10)*10,"%"
  s1=[]
  s2=[]
  for j in range(Nsize1):
    s1.append(dist1.GetRandom())
  for j in range(Nsize2):
    s2.append(dist2.GetRandom())
#  kolmDist = ROOT.TMath.KolmogorovTest(len(s1), array('d',s1), len(s2), array('d', s2), ' ')
  kolmDist = KolmDist(s1, s2) 
#  print kolmDist
  hKolmRef.Fill(kolmDist)
  if not kolmRef.has_key(kolmDist):
    kolmRef[kolmDist]=0
  kolmRef[kolmDist]+=1
  
hKolmRef.Draw()

NSamples=10000
dist1 = hexp
dist2 = hexp
hKolmValues = ROOT.TH1D("ks_Val", "ks",100,0,1)
kolmValues = {}
for i in range(NSamples):
  if (1+i)%(NSamples/10)==0:print (1+i)/(NSamples/10)*10,"%"
  s1=[]
  s2=[]
  for j in range(Nsize1):
    s1.append(dist1.GetRandom())
  for j in range(Nsize2):
    s2.append(dist2.GetRandom())
#  kolmDist = ROOT.TMath.KolmogorovTest(len(s1), array('d',s1), len(s2), array('d', s2), ' ')
  kolmDist = KolmDist(s1, s2) 
#  print kolmDist
  hKolmValues.Fill(kolmDist)
  if not kolmValues.has_key(kolmDist):
    kolmValues[kolmDist]=0
  kolmValues[kolmDist]+=1

hValidation = ROOT.TH1D("val", "val",30,0.,1.)
tot = sum([kolmRef[k] for k in kolmRef.keys()])
#for v in kolmRef.keys():
#  hValidation.Fill(Fraction(sum([kolmRef[k] for k in filter(lambda x:x<=v, kolmRef.keys())]),tot), kolmRef[v])
for v in kolmValues.keys():
  hValidation.Fill(Fraction(sum([kolmRef[k] for k in filter(lambda x:x<=v, kolmRef.keys())]),tot), kolmValues[v])

hValidation.Draw()

#hValidation2 = ROOT.TH1D("val", "val",30,0.,1.)
#for v in kolmValues.keys():
#  hValidation2.Fill(Fraction(sum([kolmRef[k] for k in filter(lambda x:x<v, kolmRef.keys())]),tot), kolmValues[v])

#hValidation.SetLineColor(ROOT.kRed)
#hValidation2.Draw("same")
#
#size=30
#random.seed(100)
#hksBinned = ROOT.TH1D("ks", "ks",110,-0.05,1.05)
#hksUnbinned = ROOT.TH1D("ksU", "ks",110,-0.05,1.05)
#
#hchk = ROOT.TH1D("hchk", "vals",1000,0.,1.)
#for k in range(5000):
#  vals=[]
#  vals2=[]
#  hvals = ROOT.TH1D("vals", "vals",1000,0.,1.)
#  hvals2 = ROOT.TH1D("vals", "vals",1000,0.,1.)
#  for i in range(size):
#    r=random.random()
#    hchk.Fill(r)
#    hvals.Fill(r)
#    vals.append(r)
#    r=random.random()
#    hchk.Fill(r)
#    hvals2.Fill(r)
#    vals2.append(r)
##  ks=  hvals.KolmogorovTest(hequal)
#  ks=  hequal.KolmogorovTest(hvals)
##  ks=  hvals2.KolmogorovTest(hvals)
#  del hvals
#  del hvals2
#  ksU = ROOT.TMath.KolmogorovTest(len(vals), array('d',vals), len(vals2), array('d', vals2), 'D')
#  print ks, ksU 
#  hksBinned.Fill(ks)
#  hksUnbinned.Fill(ksU)
#
#hksBinned.SetLineColor(ROOT.kRed)
#hksBinned.Draw()
#hksUnbinned.Draw("same")
##hksTest = ROOT.TH1D("ks", "ks",110,-0.05,1.05)
##for s in range(3000):
##  random.seed(s)
##  sequence = range(size)
##  random.shuffle(sequence)
##  set1 = sequence[:size/2]
##  set2 = sequence[size/2:]
##
###  ks = ROOT.TMath.KolmogorovTest(len(set1), array('d', [vals[i] for i in set1]), len(set1), array('d', [vals[i] for i in set2]), 'D')
##  print ks 
##  hksTest.Fill(ks)

