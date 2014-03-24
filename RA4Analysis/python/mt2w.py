import ROOT, array
from math import pi, sqrt, cos, sin, sinh

ROOT.gROOT.ProcessLine(".L ../../HEPHYCommonTools/scripts/root/mt2w_bisect.cpp+")
def getJetArray(j):
  px = j['pt']*cos(j['phi'] )
  py = j['pt']*sin(j['phi'] )
  pz = j['pt']*sinh(j['eta'] )
  E = sqrt(px*px+py*py+pz*pz)
  return array.array('d', [E, px, py,pz])

def mt2w(met, l, ljets, bjets):
  mt2w = ROOT.mt2w(500, 499, 0.5)
  pxLep = l['pt']*cos( l['phi'])
  pyLep = l['pt']*sin( l['phi'])
  pzLep = l['pt']*sinh( l['eta'])
  ELep = sqrt(pxLep*pxLep + pyLep*pyLep + pzLep*pzLep)
  lep    =array.array('d',[ELep, pxLep, pyLep, pzLep] )
  pmiss  =array.array('d',[  0., met['pt']*cos(met['phi']), met['pt']*sin(met['phi'])] )

  mt2w_values=[]
  if len(bjets)==0 and len(ljets)>=3: #All combinations from the highest three light (or b-) jets
    b0=getJetArray(ljets[0])
    b1=getJetArray(ljets[1])
    b2=getJetArray(ljets[2])

    mt2w.set_momenta(lep, b0, b1, pmiss)
    mt2w_values.append(mt2w.get_mt2w())
    mt2w.set_momenta(lep, b1, b0, pmiss)
    mt2w_values.append(mt2w.get_mt2w())

    mt2w.set_momenta(lep, b0, b2, pmiss)
    mt2w_values.append(mt2w.get_mt2w())
    mt2w.set_momenta(lep, b2, b0, pmiss)
    mt2w_values.append(mt2w.get_mt2w())

    mt2w.set_momenta(lep, b2, b1, pmiss)
    mt2w_values.append(mt2w.get_mt2w())
    mt2w.set_momenta(lep, b1, b2, pmiss)
    mt2w_values.append(mt2w.get_mt2w())
  if len(bjets)==1 and len(ljets)>=2: #All combinations from one b and the highest two light jets
    b0=getJetArray(bjets[0])
    b1=getJetArray(ljets[0])
    b2=getJetArray(ljets[1])

    mt2w.set_momenta(lep, b0, b1, pmiss)
    mt2w_values.append(mt2w.get_mt2w())
    mt2w.set_momenta(lep, b1, b0, pmiss)
    mt2w_values.append(mt2w.get_mt2w())

    mt2w.set_momenta(lep, b0, b2, pmiss)
    mt2w_values.append(mt2w.get_mt2w())
    mt2w.set_momenta(lep, b2, b0, pmiss)
    mt2w_values.append(mt2w.get_mt2w())

  if len(bjets)==2:
    b0=getJetArray(bjets[0])
    b1=getJetArray(bjets[1])
#              print lep, pmiss, b0, b1
    mt2w.set_momenta(lep, b0, b1, pmiss)
    mt2w_values.append(mt2w.get_mt2w())
    mt2w.set_momenta(lep, b1, b0, pmiss)
    mt2w_values.append(mt2w.get_mt2w())
  if len(bjets)>=3: #All combinations from the highest three light (or b-) jets

    bjets= sorted(bjets, key=lambda k: -k['pt'])
    bjets= sorted(bjets, key=lambda k: -k['pt'])

    b0=getJetArray(bjets[0])
    b1=getJetArray(bjets[1])
    b2=getJetArray(bjets[2])

    mt2w.set_momenta(lep, b0, b1, pmiss)
    mt2w_values.append(mt2w.get_mt2w())
    mt2w.set_momenta(lep, b1, b0, pmiss)
    mt2w_values.append(mt2w.get_mt2w())

    mt2w.set_momenta(lep, b0, b2, pmiss)
    mt2w_values.append(mt2w.get_mt2w())
    mt2w.set_momenta(lep, b2, b0, pmiss)
    mt2w_values.append(mt2w.get_mt2w())

    mt2w.set_momenta(lep, b2, b1, pmiss)
    mt2w_values.append(mt2w.get_mt2w())
    mt2w.set_momenta(lep, b1, b2, pmiss)
    mt2w_values.append(mt2w.get_mt2w())
#            print len(bjets), len(ljets), len(jets), mt2w_values
  del mt2w
  if len(mt2w_values)>0:
    return min(mt2w_values)
  return float('nan')

