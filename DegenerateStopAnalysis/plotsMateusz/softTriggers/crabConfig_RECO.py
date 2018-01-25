#Crab3 Configuration File

from CRABClient.UserUtilities import config
config = config()
#from WMCore.Configuration import Configuration
#config = Configuration()

mStop = "500"
mLSP = "440"

signalName = 'T2tt_dM-10to80_mStop-%s_mLSP-%s_SoftTriggers-V15_AODSIM'%(mStop,mLSP)
#config.section_('General')
config.General.requestName = signalName 
config.General.transferOutputs = True
config.General.transferLogs = True
#config.General.workArea = 'crab_projects'

#config.section_('JobType')
#config.JobType.inputFiles = ['/afs/hephy.at/data/mzarucki02/gridpacks/%s'%gridpack]
config.JobType.pyCfgParams = ['mStop='+mStop, 'mLSP='+mLSP]
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'SoftTriggers_RAW2DIGI_L1Reco_RECO.py' # Name of the CMSSW configuration file
config.JobType.outputFiles = ['%s.root'%signalName]
config.JobType.numCores = 4
config.JobType.maxMemoryMB = 8000 # 2000*numCores 
#config.JobType.generator = 'lhe'

#config.section_('Data')
#config.Data.inputDataset = '/T2tt_dM-10to80_mStop-{mStop}_mLSP-{mLSP}_privGridpack_GEN-SIM/mzarucki-T2tt_dM-10to80_mStop-{mStop}_mLSP-{mLSP}_privGridpack_GEN-SIM_RAWSIMoutput-{datasetHash}/USER'.format(mStop = mStop, mLSP = mLSP, datasetHash = datasetHashes['%s_%s'%(mStop, mLSP)])
#config.Data.inputDBS = 'phys03'
config.Data.userInputFiles = [x.strip() for x in open('inputFiles/inputFiles_T2tt_dM-10to80_mStop-%s_mLSP-%s_HLT_SoftTriggers-V15.txt'%(mStop,mLSP)).readlines()] #NOTE: careful that the string is not too long
config.Data.outputDatasetTag = signalName # This string is used to construct the output dataset name
config.Data.outputPrimaryDataset = signalName # This string determines the primary dataset of the newly-produced outputs.
config.Data.splitting = 'FileBased'
config.Data.publication = False
#config.Data.totalUnits = 500000
config.Data.unitsPerJob = 1 #5000 #NOTE: if FileBased splitting, # files per job
config.Data.ignoreLocality = True # Set to True to allow the jobs to run at sites regardless of where the input dataset is hosted (this parameter has effect only when Data.inputDataset is used). The parameter Site.whitelist is mandatory and Site.blacklist can also be used and it is respected. This parameter is useful to allow the jobs to run on other sites when for example a dataset is hosted only on sites which are not running CRAB jobs. 

#config.section_('Site')
config.Site.storageSite = 'T2_AT_Vienna' #Where the output files will be transmitted to
#config.Site.whitelist = ['T2_CH_CERN','T2_AT_Vienna'] # needs to be commented out for maxMemoryMB > 2000 in Vienna

#if __name__ == '__main__':
#    from CRABAPI.RawCommand import crabCommand
#    crabCommand('submit', config = config)
