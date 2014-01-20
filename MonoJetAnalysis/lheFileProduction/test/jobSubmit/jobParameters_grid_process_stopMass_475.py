#
# submission script for GANGA 
# 
# the job is tested to work on the hephy-vienna grid nodes only

j=Job()
j.application.exe=File('Workspace/MonoJetAnalysis/lheFileProduction/test/runLheProduction_grid.sh')
j.splitter=ArgSplitter()
j.splitter.args=[ 
                 ['jobParameters_process', '475', '475',    '0',  '50', '10'], \
                 ['jobParameters_process', '475', '475',    '0',  '50', '20'], \
                 ['jobParameters_process', '475', '475',    '0',  '50', '30'], \
                 ['jobParameters_process', '475', '475',    '0',  '50', '40'], \
                 ['jobParameters_process', '475', '475',    '0',  '50', '50'], \
                 ['jobParameters_process', '475', '475',    '0',  '50', '60'], \
                 ['jobParameters_process', '475', '475',    '0',  '50', '70'], \
                 ['jobParameters_process', '475', '475',    '0',  '50', '80'], \
                 ['jobParameters_process', '475', '475',   '75', '125', '10'], \
                 ['jobParameters_process', '475', '475',   '75', '125', '20'], \
                 ['jobParameters_process', '475', '475',   '75', '125', '30'], \
                 ['jobParameters_process', '475', '475',   '75', '125', '40'], \
                 ['jobParameters_process', '475', '475',   '75', '125', '50'], \
                 ['jobParameters_process', '475', '475',   '75', '125', '60'], \
                 ['jobParameters_process', '475', '475',   '75', '125', '70'], \
                 ['jobParameters_process', '475', '475',   '75', '125', '80'], \
                 ['jobParameters_process', '475', '475',  '150', '200', '10'], \
                 ['jobParameters_process', '475', '475',  '150', '200', '20'], \
                 ['jobParameters_process', '475', '475',  '150', '200', '30'], \
                 ['jobParameters_process', '475', '475',  '150', '200', '40'], \
                 ['jobParameters_process', '475', '475',  '150', '200', '50'], \
                 ['jobParameters_process', '475', '475',  '150', '200', '60'], \
                 ['jobParameters_process', '475', '475',  '150', '200', '70'], \
                 ['jobParameters_process', '475', '475',  '150', '200', '80'], \
                 ['jobParameters_process', '475', '475',  '225', '275', '10'], \
                 ['jobParameters_process', '475', '475',  '225', '275', '20'], \
                 ['jobParameters_process', '475', '475',  '225', '275', '30'], \
                 ['jobParameters_process', '475', '475',  '225', '275', '40'], \
                 ['jobParameters_process', '475', '475',  '225', '275', '50'], \
                 ['jobParameters_process', '475', '475',  '225', '275', '60'], \
                 ['jobParameters_process', '475', '475',  '225', '275', '70'], \
                 ['jobParameters_process', '475', '475',  '225', '275', '80'], \
                 ['jobParameters_process', '475', '475',  '300', '375', '10'], \
                 ['jobParameters_process', '475', '475',  '300', '375', '20'], \
                 ['jobParameters_process', '475', '475',  '300', '375', '30'], \
                 ['jobParameters_process', '475', '475',  '300', '375', '40'], \
                 ['jobParameters_process', '475', '475',  '300', '375', '50'], \
                 ['jobParameters_process', '475', '475',  '300', '375', '60'], \
                 ['jobParameters_process', '475', '475',  '300', '375', '70'], \
                 ['jobParameters_process', '475', '475',  '300', '375', '80'] \
                ]
j.backend=LCG()
j.backend.CE='creamce.hephy.oeaw.ac.at:8443/cream-pbs-cms'
j.submit()
