#
# submission script for GANGA 
# 
# the job is tested to work on the hephy-vienna grid nodes only

j=Job()
j.application.exe=File('Workspace/MonoJetAnalysis/lheFileProduction/test/runLheProduction_grid.sh')
j.splitter=ArgSplitter()
j.splitter.args=[ 
                 ['jobParameters_process', '200', '200',   '0',  '50', '10'], \
                 ['jobParameters_process', '200', '200',   '0',  '50', '20'], \
                 ['jobParameters_process', '200', '200',   '0',  '50', '30'], \
                 ['jobParameters_process', '200', '200',   '0',  '50', '40'], \
                 ['jobParameters_process', '200', '200',   '0',  '50', '50'], \
                 ['jobParameters_process', '200', '200',   '0',  '50', '60'], \
                 ['jobParameters_process', '200', '200',   '0',  '50', '70'], \
                 ['jobParameters_process', '200', '200',   '0',  '50', '80'], \
                 ['jobParameters_process', '200', '200',  '75', '100', '10'], \
                 ['jobParameters_process', '200', '200',  '75', '100', '20'], \
                 ['jobParameters_process', '200', '200',  '75', '100', '30'], \
                 ['jobParameters_process', '200', '200',  '75', '100', '40'], \
                 ['jobParameters_process', '200', '200',  '75', '100', '50'], \
                 ['jobParameters_process', '200', '200',  '75', '100', '60'], \
                 ['jobParameters_process', '200', '200',  '75', '100', '70'], \
                 ['jobParameters_process', '200', '200',  '75', '100', '80'] \
                ]
j.backend=LCG()
j.backend.CE='creamce.hephy.oeaw.ac.at:8443/cream-pbs-cms'
j.submit()
