#Crab3 Configuration File

from CRABClient.UserUtilities import config
config = config()
#from WMCore.Configuration import Configuration
#config = Configuration()

menuName = 'SoftMuPlusHardJet'
menuVersion = 'V5'
PU = 'PU' # 'noPU'

mStop = "500"
mLSP = "490"

outputName = 'T2tt_dM-10to80_mStop-%s_mLSP-%s_%s-%s_AODSIM_%s_partial'%(mStop,mLSP,menuName,menuVersion,PU)
#config.section_('General')
config.General.requestName = outputName
config.General.transferOutputs = True
config.General.transferLogs = True
#config.General.workArea = 'crab_projects'

#config.section_('JobType')
#config.JobType.inputFiles = ['/afs/hephy.at/data/mzarucki02/gridpacks/%s'%gridpack]
config.JobType.pyCfgParams = ['outputName='+outputName]
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'SoftTriggers_10X_RAW2DIGI_L1Reco_RECO.py' # Name of the CMSSW configuration file
config.JobType.outputFiles = ['%s.root'%outputName]
config.JobType.numCores = 8
config.JobType.maxMemoryMB = 4000 # 2000*numCores #NOTE: effective if Data.ignoreLocality False? (Data.inputDataset not used)
#config.JobType.generator = 'lhe'

#config.section_('Data')
#config.Data.inputDataset = '/T2tt_dM-10to80_mStop-{mStop}_mLSP-{mLSP}_privGridpack_GEN-SIM/mzarucki-T2tt_dM-10to80_mStop-{mStop}_mLSP-{mLSP}_privGridpack_GEN-SIM_RAWSIMoutput-{datasetHash}/USER'.format(mStop = mStop, mLSP = mLSP, datasetHash = datasetHashes['%s_%s'%(mStop, mLSP)])
#config.Data.inputDBS = 'phys03'
config.Data.userInputFiles = [x.strip() for x in open('inputFiles/inputFiles_T2tt_dM-10to80_mStop-%s_mLSP-%s_%s-%s_HLT_%s.txt'%(mStop,mLSP,menuName,menuVersion,PU)).readlines()] #NOTE: careful that the string is not too long
config.Data.outputDatasetTag = outputName # This string is used to construct the output dataset name
config.Data.outputPrimaryDataset = outputName # This string determines the primary dataset of the newly-produced outputs.
config.Data.splitting = 'FileBased'
config.Data.publication = False
#config.Data.totalUnits = 300 #500000
config.Data.unitsPerJob = 1 #5000 #NOTE: if FileBased splitting, # files per job
#config.Data.ignoreLocality = True # Set to True to allow the jobs to run at sites regardless of where the input dataset is hosted (this parameter has effect only when Data.inputDataset is used). The parameter Site.whitelist is mandatory and Site.blacklist can also be used and it is respected. This parameter is useful to allow the jobs to run on other sites when for example a dataset is hosted only on sites which are not running CRAB jobs. 

#config.section_('Site')
config.Site.storageSite = 'T2_AT_Vienna' #Where the output files will be transmitted to
#config.Site.whitelist = ['T2_CH_CERN','T2_AT_Vienna'] # needs to be commented out for maxMemoryMB > 2000 in Vienna
config.Site.blacklist = ['T2_EE_Estonia']

#if __name__ == '__main__':
#    from CRABAPI.RawCommand import crabCommand
#    crabCommand('submit', config = config)
