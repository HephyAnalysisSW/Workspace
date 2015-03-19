import ROOT
import pickle
from commons import label
from Workspace.HEPHYPythonTools.helpers import getVarValue
from math import pi, cos, sin, sqrt, atan2
sample = 'dy53X'

def getShiftCorr(sample, mapName):
  res = pickle.load(file('/data/schoef/tools/metPhiShifts/shift_'+sample+'_'+mapName+'.pkl'))
  return res

from commons import *
  
name = 'multPhiCorr_'+sample
filename = name+'_cfi.py'
ofile = file(filename, 'w')
ofile.write('import FWCore.ParameterSet.Config as cms\n')
ofile.write(name+' = cms.VPSet(\n')
for map in allMaps:
  res = getShiftCorr(sample, map['name'])
  ofile.write('    cms.PSet(\n')
  ofile.write('      name=cms.string("'+map['name'].replace('_','')+'"),\n')
  ofile.write('      type=cms.int32('+str(label[map['type']])+'),\n')
  ofile.write('      etaMin=cms.double('+str(map['binning'][1])+'),\n')
  ofile.write('      etaMax=cms.double('+str(map['binning'][2])+'),\n')
  ofile.write('      fx=cms.string("'+res['fx'].GetExpFormula().Data()+'"),\n')
  ofile.write('      px=cms.vdouble('+','.join(str(res['fx'].GetParameter(i)) for i in range(res['fx'].GetNpar()))+'),\n')
  ofile.write('      fy=cms.string("'+res['fy'].GetExpFormula().Data()+'"),\n')
  ofile.write('      py=cms.vdouble('+','.join(str(res['fy'].GetParameter(i)) for i in range(res['fy'].GetNpar()))+'),\n')
  
  ofile.write('    ),\n')
ofile.write(')\n')
ofile.close()
