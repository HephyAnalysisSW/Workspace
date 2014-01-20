#
# submission script for GANGA 
# 
# the job is tested to work on the hephy-vienna grid nodes only

j=Job()
j.application.exe=File('Workspace/MonoJetAnalysis/lheFileProduction/test/runLheProduction_grid.sh')
j.splitter=ArgSplitter()
j.splitter.args=[ 
                 ['jobParameters_process', '250', '250',   '0',  '50', '10'], \
                 ['jobParameters_process', '250', '250',   '0',  '50', '20'], \
                 ['jobParameters_process', '250', '250',   '0',  '50', '30'], \
                 ['jobParameters_process', '250', '250',   '0',  '50', '40'], \
                 ['jobParameters_process', '250', '250',   '0',  '50', '50'], \
                 ['jobParameters_process', '250', '250',   '0',  '50', '60'], \
                 ['jobParameters_process', '250', '250',   '0',  '50', '70'], \
                 ['jobParameters_process', '250', '250',   '0',  '50', '80'], \
                 ['jobParameters_process', '250', '250',  '75', '150', '10'], \
                 ['jobParameters_process', '250', '250',  '75', '150', '20'], \
                 ['jobParameters_process', '250', '250',  '75', '150', '30'], \
                 ['jobParameters_process', '250', '250',  '75', '150', '40'], \
                 ['jobParameters_process', '250', '250',  '75', '150', '50'], \
                 ['jobParameters_process', '250', '250',  '75', '150', '60'], \
                 ['jobParameters_process', '250', '250',  '75', '150', '70'], \
                 ['jobParameters_process', '250', '250',  '75', '150', '80'] \
                ]
j.backend=LCG()
j.backend.CE='creamce.hephy.oeaw.ac.at:8443/cream-pbs-cms'
j.submit()
