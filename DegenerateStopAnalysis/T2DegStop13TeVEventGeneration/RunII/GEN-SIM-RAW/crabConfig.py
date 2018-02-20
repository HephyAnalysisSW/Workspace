#Crab3 Configuration File

from CRABClient.UserUtilities import config
config = config()
#from WMCore.Configuration import Configuration
#config = Configuration()

mStop = "500"
mLSP = "460"

gridpack = 'SMS-StopStop_mStop-%s_slc6_amd64_gcc481_CMSSW_7_1_30_tarball.tar.xz'%mStop
signalName = 'T2tt_dM-10to80_mStop-%s_mLSP-%s_privGridpack_GEN-SIM'%(mStop,mLSP)
#config.section_('General')
config.General.requestName = signalName 
config.General.transferOutputs = True
config.General.transferLogs = True
#config.General.workArea = 'crab_projects'

#config.section_('JobType')
config.JobType.inputFiles = ['/afs/hephy.at/data/mzarucki02/gridpacks/%s'%gridpack]
config.JobType.pyCfgParams = ['gridpack=../'+gridpack, 'mStop='+mStop, 'mLSP='+mLSP]
config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = 'T2tt_dM-10to80_privGridpack_LHE-GEN-SIM.py' # Name of the CMSSW configuration file
config.JobType.outputFiles = ['%s.root'%signalName]
config.JobType.numCores = 8
config.JobType.maxMemoryMB = 16000 # 2000*numCores 
#config.JobType.generator = 'lhe'

#config.section_('Data')
#config.Data.inputDataset = 'None'
#config.Data.inputDBS = 'global'
config.Data.outputDatasetTag = signalName # This string is used to construct the output dataset name
config.Data.outputPrimaryDataset = signalName # This string determines the primary dataset of the newly-produced outputs.
config.Data.splitting = 'EventBased'
config.Data.publication = True
config.Data.totalUnits = 1500000
config.Data.unitsPerJob = 5000
#config.Data.ignoreLocality = True # Set to True to allow the jobs to run at sites regardless of where the input dataset is hosted (this parameter has effect only when Data.inputDataset is used). The parameter Site.whitelist is mandatory and Site.blacklist can also be used and it is respected. This parameter is useful to allow the jobs to run on other sites when for example a dataset is hosted only on sites which are not running CRAB jobs. 

#config.section_('Site')
config.Site.storageSite = 'T2_AT_Vienna' #Where the output files will be transmitted to
#config.Site.whitelist = ['T2_CH_CERN','T2_AT_Vienna'] # needs to be commented out for maxMemoryMB > 2000 in Vienna

#if __name__ == '__main__':
#    from CRABAPI.RawCommand import crabCommand
#    crabCommand('submit', config = config)
