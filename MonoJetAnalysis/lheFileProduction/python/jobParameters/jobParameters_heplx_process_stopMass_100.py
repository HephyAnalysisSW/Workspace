#
# job parameters for LHE production
# 
# parameters defined here will overwrite the default parameters
# the significance of the parameters is defined, as well as their 
# default values are defined in the file
# jobParameters/runLheProduction_parameters 

# import default parameters for LHE production
from runLheProduction_parameters import *

# modified parameters

# generated stop mass limits (GeV)
stopMassLimits = [100, 100]

# work directory, where the MadGraph is installed and the files are staged
workDirectory = '/data/DegenerateLightStop/LheProduction'

# MadGraph home
madGraphDirectory = workDirectory + '/' + 'MadGraph/MG5v1.5.11'

# EOS location of the T2tt undecayed LHE files
# directory to stage undecayed LHE file, or where files are already staged 
# directory to save the merged files
# 
# lheSample: T2tt or stop_stop

lheSample = 'stop_stop'

if lheSample == 'stop_stop':
    lheUndecayedEosDirectory = '/store/group/phys_susy/LHE/stop_stop/T2tt_Undecayed'
    undecayedFilesStageDirectory = workDirectory + '/' + 'T2tt' + '/' + 'stop_stop' + '/' + 'T2tt_undecayedFiles'
    mergedFilesDirectory =         workDirectory + '/' + 'T2tt' + '/' + 'stop_stop' + '/' + 'T2tt_mergedFiles'
elif lheSample == 'T2tt':   
    lheUndecayedEosDirectory = '/store/group/phys_susy/LHE/T2tt'
    undecayedFilesStageDirectory = workDirectory + '/' + 'T2tt' + '/' + 'T2tt' + '/' + 'T2tt_undecayedFiles'
    mergedFilesDirectory =         workDirectory + '/' + 'T2tt' + '/' + 'T2tt' + '/' + 'T2tt_mergedFiles'
else:
    sys.exit('No valid EOS LHE sample.')
