import ROOT
import pickle
from commons import label
from Workspace.HEPHYPythonTools.helpers import getVarValue
from math import pi, cos, sin, sqrt, atan2
sample = 'dy53X'

from commons import *
  
name = 'multPhiCorr_multMETCorrInfoWriter_53X'
filename = name+'_cfi.py'
ofile = file(filename, 'w')
ofile.write('import FWCore.ParameterSet.Config as cms\n')
ofile.write(name+' = cms.VPSet(\n')
for map in allMaps:
  ofile.write('    cms.PSet(\n')
  ofile.write('      name=cms.string("'+map['name'].replace('_','')+'"),\n')
  ofile.write('      type=cms.int32('+str(label[map['type']])+'),\n')
  ofile.write('      nbins=cms.double('+str(map['candBinning'][0])+'),\n')
  ofile.write('      nMin=cms.int32('+str(map['candBinning'][1])+'),\n')
  ofile.write('      nMax=cms.int32('+str(map['candBinning'][2])+'),\n')
  ofile.write('      etaNBins=cms.int32('+str(map['binning'][0])+'),\n')
  ofile.write('      etaMin=cms.double('+str(map['binning'][1])+'),\n')
  ofile.write('      etaMax=cms.double('+str(map['binning'][2])+'),\n')
  ofile.write('      phiNBins=cms.int32('+str(map['binning'][3])+'),\n')
  ofile.write('      phiMin=cms.double('+str(map['binning'][4])+'),\n')
  ofile.write('      phiMax=cms.double('+str(map['binning'][5])+'),\n')
  
  ofile.write('    ),\n')
ofile.write(')\n')
ofile.close()
