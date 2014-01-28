#
# dummy values for job parameters for LHE production, to be 
# replaced by the production shell script
# 

import os

# the stop mass values are fixed for the LHE files with undecayed stops, 
# one can only choose the range the files are selected and processed
#
# choose the range the files are selected and processed
# if stopMassLimits[0] is negative, it will process files for all existing stop mass values
# otherwise it will process all files having 
#     stopMassLimits[0] <= stop mass <= stopMassLimits[1]

# generated stop mass limits (GeV)
stopMassLimits = [REPLACE_stopMassLowLimit, REPLACE_stopMassHighLimit]

# there are no LSP particles in the undecayed files (stop and antistop are not decayed)
# the generated LSP mass values are, as such, dummy, but they are included in the file name
#
# choose the generated LSP mass values for which the files are selected and processed by MadGraph
# if generatedLspMass[0] is negative, it will process all the files corresponding to the stop mass(es) given above
# otherwise it will process all files having 
#     generatedLspMassLimits[0] <= generated LSP mass <= generatedLspMassLimits[1]
generatedLspMassLimits = [REPLACE_generatedLspMassLowLimit, REPLACE_generatedLspMassHighLimit]

# deltaMassStopLspSelected - list of mass differences selected from 
# deltaMassStopLsp to be processed in this job
deltaMassStopLspSelected = [REPLACE_deltaMassStopLspSelected]

# work directory for a job
workDirectory = os.getcwd()

# MadGraph home
madGraphDirectory = workDirectory + '/' + 'REPLACE_madGraphDirectory'

# directory where undecayed LHE file are to be found by a job 
undecayedFilesDirectory = workDirectory + '/' + 'REPLACE_undecayedFilesDirectory'

# directory to save the merged files by a job
mergedFilesDirectory = workDirectory + '/' + 'REPLACE_mergedFilesDirectory'

# directory to stage undecayed LHE file, or where files are already staged
# directory must be given as absolute path
# actual value will be set in the run shell script 
undecayedFilesStageDirectory = 'REPLACE_undecayedFilesStageDirectory'


