#Crab3 Configuration File

from CRABClient.UserUtilities import config
config = config()
#from WMCore.Configuration import Configuration
#config = Configuration()

menuName = 'SoftMuPlusHardJet'
menuVersion = 'V5'
dataset = 'EphemeralZeroBias1/Run2017F-v1'
#dataset = 'ZeroBias1/Run2017F-v1'
datasetName = dataset.replace('/','_')
outputName = '%s_%s-%s_HLT'%(datasetName,menuName,menuVersion)

#config.section_('General')
config.General.requestName = outputName 
config.General.transferOutputs = True
config.General.transferLogs = True
#config.General.workArea = 'crab_projects'

#config.section_('JobType')
config.JobType.pyCfgParams = ['outputName='+outputName]
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'run_steamflow_crab_cfg.py' # Name of the CMSSW configuration file
config.JobType.outputFiles = ['%s.root'%outputName]
config.JobType.numCores = 8
config.JobType.maxMemoryMB = 8000 # 2000*numCores 
#config.JobType.generator = 'lhe'

#config.section_('Data')
config.Data.inputDataset =  '/%s/RAW'%dataset
config.Data.inputDBS = 'global'
#config.Data.userInputFiles = [x.strip() for x in open('inputFiles_GEN-SIM.txt').readlines()] #NOTE: careful that the string is not too long
config.Data.outputDatasetTag = outputName # This string is used to construct the output dataset name
#config.Data.outputPrimaryDataset = outputName # This string determines the primary dataset of the newly-produced outputs.
config.Data.splitting = 'LumiBased' #'FileBased'
config.Data.publication = False
#config.Data.totalUnits = -1 # all
config.Data.unitsPerJob = 1 #5000 #NOTE: if FileBased splitting, # files per job
config.Data.ignoreLocality = True # Set to True to allow the jobs to run at sites regardless of where the input dataset is hosted (this parameter has effect only when Data.inputDataset is used). The parameter Site.whitelist is mandatory and Site.blacklist can also be used and it is respected. This parameter is useful to allow the jobs to run on other sites when for example a dataset is hosted only on sites which are not running CRAB jobs. 
#config.Data.lumiMask = 'JSON_Run2017F-ZB_1p5e34_PU55.txt' # Run2017F
config.Data.lumiMask = 'Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt' # Run2017F Golden JSON
#config.Data.lumiMask = 'json_HLTPhysicsL1v4_2p0e34.txt' # Run2017E

#config.section_('Site')
config.Site.storageSite = 'T2_AT_Vienna' #Where the output files will be transmitted to
config.Site.whitelist = ['T2_AT_Vienna','T2_CH*','T2_US*','T2_UK*','T2_IT*', 'T2_FR*', 'T2_PT*']
config.Site.blacklist = ['T2_EE_Estonia']

#if __name__ == '__main__':
#    from CRABAPI.RawCommand import crabCommand
#    crabCommand('submit', config = config)
