#
# submission script for GANGA, to fix some production glitches 
# 
# the job is tested to work on the hephy-vienna grid nodes only

j=Job()
j.application.exe=File('Workspace/MonoJetAnalysis/lheFileProduction/test/runLheProduction_grid.sh')
j.splitter=ArgSplitter()
j.splitter.args=[ 
                 ['jobParameters_process', '350', '350',    '0',  '50', '60'], \
                 ['jobParameters_process', '350', '350',   '75', '125', '20'], \
                 ['jobParameters_process', '400', '400',    '0',   '0', '30'] \
                ]
j.backend=LCG()
j.backend.CE='creamce.hephy.oeaw.ac.at:8443/cream-pbs-cms'
j.submit()
