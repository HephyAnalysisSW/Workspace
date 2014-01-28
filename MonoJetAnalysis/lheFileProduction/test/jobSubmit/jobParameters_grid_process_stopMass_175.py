#
# submission script for GANGA 
# 
# the job is tested to work on the hephy-vienna grid nodes only

j=Job()
j.application.exe=File('Workspace/MonoJetAnalysis/lheFileProduction/test/runLheProduction_grid.sh')
j.splitter=ArgSplitter()
j.splitter.args=[ 
                 ['jobParameters_process', '175', '175',   '0', '25', '10'], \
                 ['jobParameters_process', '175', '175',   '0', '25', '20'], \
                 ['jobParameters_process', '175', '175',   '0', '25', '30'], \
                 ['jobParameters_process', '175', '175',   '0', '25', '40'], \
                 ['jobParameters_process', '175', '175',   '0', '25', '50'], \
                 ['jobParameters_process', '175', '175',   '0', '25', '60'], \
                 ['jobParameters_process', '175', '175',   '0', '25', '70'], \
                 ['jobParameters_process', '175', '175',   '0', '25', '80'], \
                 ['jobParameters_process', '175', '175',  '50', '75', '10'], \
                 ['jobParameters_process', '175', '175',  '50', '75', '20'], \
                 ['jobParameters_process', '175', '175',  '50', '75', '30'], \
                 ['jobParameters_process', '175', '175',  '50', '75', '40'], \
                 ['jobParameters_process', '175', '175',  '50', '75', '50'], \
                 ['jobParameters_process', '175', '175',  '50', '75', '60'], \
                 ['jobParameters_process', '175', '175',  '50', '75', '70'], \
                 ['jobParameters_process', '175', '175',  '50', '75', '80'] \
                ]
j.backend=LCG()
j.backend.CE='creamce.hephy.oeaw.ac.at:8443/cream-pbs-cms'
j.submit()
