from WMCore.Configuration import Configuration


samples={
          '300_270': {'outputFiles':['T2DegStop_300_270_RunII_25ns_miniAOD.root'] ,  "outputDatasetTag": 'T2DegStop_300_270',
                       'inputDataset': '/T2DegStop_300_270_GEN-SIM/nrad-T2DegStop_300_270_RECO-RunIISpring15-MCRUN2_74_V9-25ns-cdcc155817963320a88c2dd6cf768461/USER',
                        },
          '300_270FS': {'outputFiles':['T2DegStop_300_270_RunII_FastSim_miniAOD.root'] ,  "outputDatasetTag": 'T2DegStop_300_270FS',
                       'inputDataset': '/T2DegStop_300_270_FastSim_v3/mzarucki-T2DegStop_300_270_FastSim_v3-420683af1bb5170fe0b35a3c8f09b1ec/USER',
                        'testfile': 'root://hephyse.oeaw.ac.at//dpm/oeaw.ac.at/home/cms/store/user/mzarucki/T2DegStop_300_270_FastSim_v3/T2DegStop_300_270_FastSim_v3/151123_113332/0000/T2DegStop_300_270_FastSim_v3_415.root',
                        },
          '300_290FS': {'outputFiles':['T2DegStop_300_290_RunII_FastSim_miniAOD.root'] ,  "outputDatasetTag": 'T2DegStop_300_290FS',
                       'inputDataset':   '/T2DegStop_300_290_FastSim_v3/mzarucki-T2DegStop_300_290_FastSim_v3-420683af1bb5170fe0b35a3c8f09b1ec/USER' },
          '300_240FS': {'outputFiles':['T2DegStop_300_240_RunII_FastSim_miniAOD.root'] ,  "outputDatasetTag": 'T2DegStop_300_240FS',
                       'inputDataset': '/T2DegStop_300_240_FastSim_v3/mzarucki-T2DegStop_300_240_FastSim_v3-420683af1bb5170fe0b35a3c8f09b1ec/USER' }
        }


sample=samples['300_240FS']



config = Configuration()
config.section_('General')
config.General.transferOutputs = True
config.General.workArea = 'crab_%s'%sample['outputDatasetTag']
config.section_('JobType')
config.JobType.psetName = 'step3_miniAODv2_cfg.py'
config.JobType.pluginName = 'Analysis'
config.JobType.outputFiles = sample['outputFiles']
config.section_('Data')
config.Data.inputDataset = sample['inputDataset'] 
config.Data.outputDatasetTag = sample['outputDatasetTag']
config.Data.publication = True
config.Data.unitsPerJob = 100
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.section_('User')
config.section_('Site')
config.Site.whitelist = ['T2_AT_Vienna']
config.Site.storageSite = 'T2_AT_Vienna'
