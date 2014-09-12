#
# submission script for GANGA 
# 
# the job is tested to work on the hephy-vienna grid nodes only

j=Job()
j.application.exe=File('Workspace/MonoJetAnalysis/lheFileProduction/test/runLheProduction_grid.sh')
j.splitter=ArgSplitter()
j.splitter.args=[ 
                 ['jobParameters_process', '350', '350',    '0',  '50', '10'], \
                 ['jobParameters_process', '350', '350',    '0',  '50', '20'], \
                 ['jobParameters_process', '350', '350',    '0',  '50', '30'], \
                 ['jobParameters_process', '350', '350',    '0',  '50', '40'], \
                 ['jobParameters_process', '350', '350',    '0',  '50', '50'], \
                 ['jobParameters_process', '350', '350',    '0',  '50', '60'], \
                 ['jobParameters_process', '350', '350',    '0',  '50', '70'], \
                 ['jobParameters_process', '350', '350',    '0',  '50', '80'], \
                 ['jobParameters_process', '350', '350',   '75', '125', '10'], \
                 ['jobParameters_process', '350', '350',   '75', '125', '20'], \
                 ['jobParameters_process', '350', '350',   '75', '125', '30'], \
                 ['jobParameters_process', '350', '350',   '75', '125', '40'], \
                 ['jobParameters_process', '350', '350',   '75', '125', '50'], \
                 ['jobParameters_process', '350', '350',   '75', '125', '60'], \
                 ['jobParameters_process', '350', '350',   '75', '125', '70'], \
                 ['jobParameters_process', '350', '350',   '75', '125', '80'], \
                 ['jobParameters_process', '350', '350',  '150', '200', '10'], \
                 ['jobParameters_process', '350', '350',  '150', '200', '20'], \
                 ['jobParameters_process', '350', '350',  '150', '200', '30'], \
                 ['jobParameters_process', '350', '350',  '150', '200', '40'], \
                 ['jobParameters_process', '350', '350',  '150', '200', '50'], \
                 ['jobParameters_process', '350', '350',  '150', '200', '60'], \
                 ['jobParameters_process', '350', '350',  '150', '200', '70'], \
                 ['jobParameters_process', '350', '350',  '150', '200', '80'], \
                 ['jobParameters_process', '350', '350',  '225', '250', '10'], \
                 ['jobParameters_process', '350', '350',  '225', '250', '20'], \
                 ['jobParameters_process', '350', '350',  '225', '250', '30'], \
                 ['jobParameters_process', '350', '350',  '225', '250', '40'], \
                 ['jobParameters_process', '350', '350',  '225', '250', '50'], \
                 ['jobParameters_process', '350', '350',  '225', '250', '60'], \
                 ['jobParameters_process', '350', '350',  '225', '250', '70'], \
                 ['jobParameters_process', '350', '350',  '225', '250', '80'] \
                ]
j.backend=LCG()
j.backend.CE='creamce.hephy.oeaw.ac.at:8443/cream-pbs-cms'
j.submit()
