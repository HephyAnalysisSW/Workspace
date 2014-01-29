#
# job parameters for LHE production
# 
# parameters defined here will overwrite the default parameters defined in
# jobParameters/runLheProduction_parameters 
# where one can also see the significance of the parameters

# import default parameters for LHE production
from runLheProduction_parameters import *

# replaceable parameters, via job shell script
from runLheProduction_parameters_replace import *

# hard-coded modified parameters

# directory to stage undecayed LHE file, or where files are already staged 
undecayedFilesStageDirectory = workDirectory + '/' + 'T2tt' + '/' + 'stop_stop' + '/' + \
    'T2tt_stopMass_' + stopMassLimits[0] + '_' + stopMassLimits[0] + '_undecayedFiles'

stageUndecayedLheFiles = True


