""" CMG ntuples from RunIISpring15DR74 MC production at 25 ns for the degenerate stop analysis.
 
Each set of ntuples is produced with a git tag of HephySusySW.cmg-cmssw repository
    tag = cmgProcessing_{identifier}
and saved in a directory 
    {path}/cmgTuples/{tag}/{campaign}/sample.name
where the campaign is :
    MC production campaign for MC samples  (e.g. RunIISpring15DR74)
    Energy, reconstruction tag, era for data (e.g. 13TeV_PromptReco_Collisions15_25ns, taken 
        from JSON name file)
    
The corresponding py sample files are called 
    cmgTuples_RunIISpring15DR74_25ns_{other identifier}.py
    cmgTuples_Data_25ns__{other identifier}.py
where other identifier is usually the version of miniAOD.
"""

import os 

# definition of samples from CMGTools file
import CMGTools.RootTools.samples.samples_13TeV_RunIISpring15MiniAODv2 as cmgSamples

# available CMG ntuple paths

# HephySusySW.cmg-cmssw tag: N/A (put arbitrary identifier 2015_11_07)
data_path__cmgProcessing_2015_11_07 = "/data/nrad/cmgTuples/RunII/7412pass2/RunIISpring15MiniAODv2"

# add only the minimum to arrive at "HEPHY format"; for all the quantities defined in CMGTools 
# use those quantities directly

for sample in cmgSamples,samples:
    sample.chunkString = sample
    sample.rootFileLocation = 'tree.root'
    sample.treeName = 'tree'
    
    
    
    





