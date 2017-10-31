import glob
import ROOT
import os
import pickle
import Workspace.DegenerateStopAnalysis.samples.cmgTuples.RunIISummer16MiniAODv2_v7 as cmgTuples
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain, getChunks, getYieldFromChain

from  Workspace.DegenerateStopAnalysis.cmgPostProcessing.signal_content import signals

genFilterEff_file = os.path.expandvars( '$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/data/filterEfficiency/{sample}/filterEffs_{sample}.pkl' )

cmgNames = [x['cmgName'] for x in cmgTuples.allComponents]


#newsigs = [x for x in cmgNames if ( 'SMS' in x and 'T2' not in x ) or 'MSSM' in x ]
newsigs = [x for x in cmgNames if  'MSSM' in x or 'TChiWZ' in x and '_3p' not in x ]


#cmgComp = cmgTuples.SMS_C1C1_higgsino_genHT_160_genMET_80_3p


def getXSec( xsecs, *masses):
    if hasattr(xsecs, "__call__"):
        return xsecs(*masses)[0]
    else:
        if len(masses)>1:
            raise Exception("more than one mass given but no function for xsec, what do i do?")
        return xsecs[masses[0]]


#def getSigMasses(cmgComp):
def intFloat( v ):
    if int(v)==float(v):
        return int(v)
    else:
        return float(v)


def getMassDict(cmgComp):
    chunkNtot = getChunks( cmgComp, maxN=-1)
    chunks, nTot = chunkNtot
    chain = getChain(chunks, minAgeDPM=0, histname='histo', xrootPrefix='root://hephyse.oeaw.ac.at/', maxN=-1, treeName='tree')
 
    nEvents = chain.GetEntries()
    assert nEvents == nTot

    genFilterEffpkl = genFilterEff_file.format(sample=cmgComp['cmgName'])
    genFilterEff = pickle.load(file(genFilterEffpkl))

    massVar1, massVar2 = cmgComp['massVars']

    xsecs = signals[cmgComp['cmgName']]['xsec']

    mass_dict = {}
    for m1, m2s in genFilterEff.iteritems():
        mass_dict[m1]={}
        for m2, eff  in m2s.iteritems():
            nevt = getYieldFromChain( chain , "(%s==%s)&&(%s==%s)"%(massVar1, m1, massVar2, m2) , '(1)')
            if not nevt: print "!! WARNING !! no events found for %s, %s"%(cmgComp['cmgName'], "(%s==%s)&&(%s==%s)"%(massVar1, m1, massVar2, m2)   )
            mass_dict[m1][intFloat(m2)]={'genFilterEff':eff, 'nEvents':nevt , 'xSec': getXSec( xsecs, m1, m2) }
    return mass_dict


for sig in newsigs:
    cmgComp = getattr(cmgTuples, sig)
    print "\n Getting MassDict For %s"%cmgComp['cmgName']
    mass_dict = getMassDict(cmgComp)
    output_file = cmgTuples.sample_path +"/%s_mass_dict.pkl"%cmgComp['cmgName']
    pickle.dump(mass_dict, file(output_file,"w") )
    print mass_dict
    print "Mass Dict saved! %s"%output_file

