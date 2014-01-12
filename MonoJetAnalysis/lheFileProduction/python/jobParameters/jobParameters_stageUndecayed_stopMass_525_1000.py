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
stopMassLimits = [525, 1000]

# directory to stage undecayed LHE file, or where files are already staged 
undecayedFilesStageDirectory = workDirectory + '/' + 'T2tt' + '/' + 'stop_stop' + '/' + 'T2tt_undecayedFiles_stopMass_525_1000'

stageUndecayedLheFiles = True

stageOnlyUndecayedLheFiles = True


