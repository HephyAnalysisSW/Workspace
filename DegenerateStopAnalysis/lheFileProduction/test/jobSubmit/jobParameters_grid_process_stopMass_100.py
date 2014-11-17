#
# submission script for GANGA 
# 
# the job is tested to work on the hephy-vienna grid nodes only

j=Job()
j.application.exe=File('Workspace/MonoJetAnalysis/lheFileProduction/test/runLheProduction_grid.sh')
j.splitter=ArgSplitter()
j.splitter.args=[ 
                 ['jobParameters_process', '100', '100',   '0',  '0', '10'], \
                 ['jobParameters_process', '100', '100',   '0',  '0', '20'], \
                 ['jobParameters_process', '100', '100',   '0',  '0', '30'], \
                 ['jobParameters_process', '100', '100',   '0',  '0', '40'], \
                 ['jobParameters_process', '100', '100',   '0',  '0', '50'], \
                 ['jobParameters_process', '100', '100',   '0',  '0', '60'], \
                 ['jobParameters_process', '100', '100',   '0',  '0', '70'], \
                 ['jobParameters_process', '100', '100',   '0',  '0', '80'] \
                ]
j.backend=LCG()
j.backend.CE='creamce.hephy.oeaw.ac.at:8443/cream-pbs-cms'
j.submit()
