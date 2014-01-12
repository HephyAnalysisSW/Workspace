#
# submission script for GANGA 
# 
# the job will work only on the hephy-vienna grid nodes, due to the need
# to have gfalFS installed and enabled on worker nodes

j=Job()
j.application.exe=File('Workspace/MonoJetAnalysis/lheFileProduction/test/runLheProduction_grid.sh')
j.splitter=ArgSplitter()
j.splitter.args=[ ['jobParameters_heplx_process_stopMass_300', '10', 'job_1'], \
                  ['jobParameters_heplx_process_stopMass_300', '30', 'job_2'], 
                  ['jobParameters_heplx_process_stopMass_300', '50', 'job_3'] ]
j.backend=LCG()
j.backend.CE='creamce.hephy.oeaw.ac.at:8443/cream-pbs-cms'
j.submit()
