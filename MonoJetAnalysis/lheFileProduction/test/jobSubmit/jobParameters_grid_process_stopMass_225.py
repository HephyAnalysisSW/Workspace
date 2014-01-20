#
# submission script for GANGA 
# 
# the job is tested to work on the hephy-vienna grid nodes only

j=Job()
j.application.exe=File('Workspace/MonoJetAnalysis/lheFileProduction/test/runLheProduction_grid.sh')
j.splitter=ArgSplitter()
j.splitter.args=[ 
                 ['jobParameters_process', '225', '225',   '0',  '50', '10'], \
                 ['jobParameters_process', '225', '225',   '0',  '50', '20'], \
                 ['jobParameters_process', '225', '225',   '0',  '50', '30'], \
                 ['jobParameters_process', '225', '225',   '0',  '50', '40'], \
                 ['jobParameters_process', '225', '225',   '0',  '50', '50'], \
                 ['jobParameters_process', '225', '225',   '0',  '50', '60'], \
                 ['jobParameters_process', '225', '225',   '0',  '50', '70'], \
                 ['jobParameters_process', '225', '225',   '0',  '50', '80'], \
                 ['jobParameters_process', '225', '225',  '75', '125', '10'], \
                 ['jobParameters_process', '225', '225',  '75', '125', '20'], \
                 ['jobParameters_process', '225', '225',  '75', '125', '30'], \
                 ['jobParameters_process', '225', '225',  '75', '125', '40'], \
                 ['jobParameters_process', '225', '225',  '75', '125', '50'], \
                 ['jobParameters_process', '225', '225',  '75', '125', '60'], \
                 ['jobParameters_process', '225', '225',  '75', '125', '70'], \
                 ['jobParameters_process', '225', '225',  '75', '125', '80'] \
                ]
j.backend=LCG()
j.backend.CE='creamce.hephy.oeaw.ac.at:8443/cream-pbs-cms'
j.submit()
