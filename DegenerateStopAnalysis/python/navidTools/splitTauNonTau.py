import ROOT
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain, getChunks
from Workspace.DegenerateStopAnalysis.cmgTuplesPostProcessed_mAODv2_7412pass2 import *

from glob import glob
from os.path import basename, isdir, isfile
from os import mkdir


def splitTauNoTau(sample , histname='', treeName="Events", outputDir = "/data/nrad/test/"):

    sampleDir = sample['dir']
    for sampleBin in sample['bins']:
        fileList = glob( sampleDir+"/"+sampleBin+"/*.root")
        print "-------", sampleBin, fileList


        noTauOutputBinDir = outputDir +"/NoTau"+sampleBin
        if not isdir(noTauOutputBinDir): mkdir(noTauOutputBinDir)
        tauOutputBinDir = outputDir +"/Tau"+sampleBin
        if not isdir(tauOutputBinDir): mkdir(tauOutputBinDir)


        for rootFile in fileList:
            chain = ROOT.TChain(treeName)
            chain.Add(rootFile)
                    
            if chain.GetEntries():
                rootFileName = basename(rootFile)    
                noTauOutput = noTauOutputBinDir+"/"+"NoTau_"+rootFileName
                tauOutput   = tauOutputBinDir+"/"+"Tau_"+rootFileName
                print  noTauOutput
                print  tauOutput

                notau = chain.CopyTree("Sum$(abs(GenPart_pdgId)==15)==0")
                writeTreeToFile(notau, noTauOutput ,"create")
                tau   = chain.CopyTree("Sum$(abs(GenPart_pdgId)==15)>=1")
                writeTreeToFile(tau, tauOutput ,"create" )
                #notau = chain.CopyTree("Sum$(abs(GenPart_pdgId)==15)==0")
                #fnotau     = ROOT.TFile(outputDir+"/"+"NoTau_"+rootFileName,"create")
                #notau.Write()
                #fnotau.Close()
                #ftau     = ROOT.TFile(outputDir+"/"+"Tau_"+rootFileName,"create")
                #tau   = chain.CopyTree("Sum$(abs(GenPart_pdgId)==15)>=1")
                #tau.Write()
                #fnotau.Close()
            else:
                print "-----------Warning: File being ignored, no Events in it:" , rootFile



def writeTreeToFile(tree,filepath, option="create"):
    newFile = ROOT.TFile(filepath, option)
    tree.Write()
    newFile.Close()
    return 

