import ROOT, array
from math import pi, sqrt, cos, sin, sinh, cosh

ROOT.gROOT.ProcessLine(".L ../../HEPHYPythonTools/scripts/root/mt2_bisect.cpp+")
def getJetArray(j):
  px = j['pt']*cos(j['phi'] )
  py = j['pt']*sin(j['phi'] )
#  pz = j['pt']*sinh(j['eta'] )
#  E = sqrt(px*px+py*py)
  return array.array('d', [0., px, py])

def addTwoObj(o1, o2):
  m = sqrt(2*o1['pt']*o2['pt']*(cosh(o1['eta']-o2['eta'])-cos(o1['phi']-o2['phi'])))
  px = o1['pt']*cos(o1['phi'] ) + o2['pt']*cos(o2['phi'] ) 
  py = o1['pt']*sin(o1['phi'] ) + o2['pt']*sin(o2['phi'] )
  return array.array('d',[m,px,py])

def mt2(met, l, ljets, bjets):
  mt2 = ROOT.mt2()
#  pxLep = l['pt']*cos( l['phi'])
#  pyLep = l['pt']*sin( l['phi'])
#  ELep_t = sqrt(pxLep*pxLep + pyLep*pyLep)
#  lep    =array.array('d',[ELep, pxLep, pyLep] )
  pmiss  =array.array('d',[  0., met['pt']*cos(met['phi']), met['pt']*sin(met['phi'])] )
  mn = 0.
  mt2.set_mn(mn)
  mt2_values=[]

  if len(bjets)==0 and len(ljets)>=3: #All combinations from the highest three light (or b-) jets
    b0=getJetArray(ljets[0])
    b1=getJetArray(ljets[1])
    b2=getJetArray(ljets[2])

    b0_l=addTwoObj(l, ljets[0])
    b1_l=addTwoObj(l, ljets[1])
    b2_l=addTwoObj(l, ljets[2])    

    mt2.set_momenta(b0, b1_l, pmiss)
    mt2_values.append(mt2.get_mt2())
    mt2.set_momenta(b0_l, b1, pmiss)
    mt2_values.append(mt2.get_mt2())

    mt2.set_momenta(b0, b2_l, pmiss)
    mt2_values.append(mt2.get_mt2())
    mt2.set_momenta(b0_l, b2, pmiss)
    mt2_values.append(mt2.get_mt2())

    mt2.set_momenta(b2, b1_l, pmiss)
    mt2_values.append(mt2.get_mt2())
    mt2.set_momenta(b2_l, b1, pmiss)
    mt2_values.append(mt2.get_mt2())


  if len(bjets)==1 and len(ljets)>=2: #All combinations from one b and the highest two light jets
    b0=getJetArray(bjets[0])
    b1=getJetArray(ljets[0])
    b2=getJetArray(ljets[1])

    b0_l=addTwoObj(l, bjets[0])
    b1_l=addTwoObj(l, ljets[0])
    b2_l=addTwoObj(l, ljets[1])

    mt2.set_momenta(b0, b1_l, pmiss)
    mt2_values.append(mt2.get_mt2())
    mt2.set_momenta(b0_l, b1, pmiss)
    mt2_values.append(mt2.get_mt2())

    mt2.set_momenta(b0, b2_l, pmiss)
    mt2_values.append(mt2.get_mt2())
    mt2.set_momenta(b0_l, b2, pmiss)
    mt2_values.append(mt2.get_mt2())

  if len(bjets)==2:
    b0=getJetArray(bjets[0])
    b1=getJetArray(bjets[1])

    b0_l=addTwoObj(l, bjets[0])    
    b1_l=addTwoObj(l, bjets[1])    

    mt2.set_momenta(b0, b1_l, pmiss)
    mt2_values.append(mt2.get_mt2())
    mt2.set_momenta(b0_l, b1, pmiss)
    mt2_values.append(mt2.get_mt2())


  if len(bjets)>=3: #All combinations from the highest three light (or b-) jets

    bjets= sorted(bjets, key=lambda k: -k['pt'])
    bjets= sorted(bjets, key=lambda k: -k['pt'])

    b0=getJetArray(bjets[0])
    b1=getJetArray(bjets[1])
    b2=getJetArray(bjets[2])

    b0_l=addTwoObj(l, bjets[0])
    b1_l=addTwoObj(l, bjets[1])
    b2_l=addTwoObj(l, bjets[2])

    mt2.set_momenta(b0, b1_l, pmiss)
    mt2_values.append(mt2.get_mt2())
    mt2.set_momenta(b0_l, b1, pmiss)
    mt2_values.append(mt2.get_mt2())

    mt2.set_momenta(b0, b2_l, pmiss)
    mt2_values.append(mt2.get_mt2())
    mt2.set_momenta(b0_l, b2, pmiss)
    mt2_values.append(mt2.get_mt2())

    mt2.set_momenta(b2, b1_l, pmiss)
    mt2_values.append(mt2.get_mt2())
    mt2.set_momenta(b2_l, b1, pmiss)
    mt2_values.append(mt2.get_mt2())


  del mt2
  if len(mt2_values)>0:
    return min(mt2_values)
  return float('nan')

