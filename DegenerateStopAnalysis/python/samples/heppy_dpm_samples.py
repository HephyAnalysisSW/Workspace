'''
Extract cmg samples from dpm'''

if __name__ == '__main__':
    # Parse args if main
    maxN_def = -1
    def get_parser():
        ''' Argument parser for post-processing module.
        '''
        import argparse
        argParser = argparse.ArgumentParser(description = "Argument parser for cmgPostProcessing")
        argParser.add_argument('--logLevel', action='store', nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'DEBUG', 'DEBUG', 'TRACE', 'NOTSET'], default='INFO', help="Log level for logging" )
        argParser.add_argument('--overwrite', action='store_true', default=False, help="Overwrite cache?" )
        argParser.add_argument('--nomultithreading', action='store_true', default=False, help="No multithreading?" )
        argParser.add_argument('--maxN', action='store', type=int, default=maxN_def, help="Overwrite cache?" )

        return argParser

    options = get_parser().parse_args()

    # Logging
    #import StopsDilepton.tools.logger as logger_
    import Workspace.DegenerateStopAnalysis.tools.helpers as helpers
    logger = helpers.get_logger('cmgPostProcessing',"DEBUG", "test.log").logger

    overwrite = options.overwrite
    maxN = options.maxN

else:
    # Logging
    #import logging
    #logger = logging.getLogger(__name__).logger

    options = None

    import Workspace.DegenerateStopAnalysis.tools.helpers as helpers
    logger = helpers.get_logger('cmgPostProcessing',"DEBUG", "test.log").logger

    overwrite = False 
    maxN =      -1

# StopsDilepton
from Workspace.DegenerateStopAnalysis.samples.walk_dpm import walk_dpm

# Standard imports
import os
import pickle

class heppy_mapper:

    def __init__(self, heppy_samples, dpm_directories, cache_file):
        # Read cache file, if exists
        if os.path.exists( cache_file ) and not overwrite:
            self.sample_map = pickle.load( file(cache_file) )
            logger.info( "Loaded cache file %s" % cache_file )
        else:
            logger.info( "Cache file %s not found. Recreate map.", cache_file)
            logger.info( "Check proxy.")

            # Proxy certificate
            from RootTools.core.helpers import renew_proxy
            # Make proxy in afs to allow batch jobs to run
            proxy_path = os.path.expandvars('$HOME/private/.proxy')
            proxy = renew_proxy( proxy_path )
            logger.info( "Using proxy %s"%proxy )

            # Read dpm directories
            self.cmg_directories = {}
            for data_path in dpm_directories:
                logger.info( "Walking dpm directory %s", data_path )
                walker = walk_dpm( data_path )
                self.cmg_directories[ data_path ] = walker.walk_dpm_cmgdirectories('.',  maxN = maxN )
                
                #del walker

            logger.info( "Now mapping directories to heppy samples" )
            fake_heppy_samples = []
            for heppy_sample in heppy_samples:
                if type(heppy_sample)==dict and heppy_sample.has_key("cmgName"):
                    # make a fake heppy_sample
                    from Workspace.DegenerateStopAnalysis.samples.FakeHeppySample import FakeHeppySample
                    #fake_heppy_samples.append(FakeHeppySample(**heppy_samples.remove(heppy_sample)))
                    fake_heppy_samples.append(FakeHeppySample(**heppy_sample))
            if fake_heppy_samples:
                heppy_samples = fake_heppy_samples
            for heppy_sample in heppy_samples:
                heppy_sample.candidate_directories = []
                pd, era = heppy_sample.dataset.split('/')[1:3]
                for data_path in self.cmg_directories.keys():
                    for dpm_directory in self.cmg_directories[data_path].keys():
                        if not ('/%s/'%pd in dpm_directory):
                            logger.debug( "/%s/ not in dpm_directory %s", pd, dpm_directory )
                            continue
                        if not ('/'+era in dpm_directory):
                            logger.debug( "/%s not in dpm_directory %s", era, dpm_directory )
                            continue
                        heppy_sample.candidate_directories.append([data_path, dpm_directory])
                        logger.debug( "heppy sample %s in %s", heppy_sample.name, dpm_directory)
                logger.info(  "Found heppy sample %s in %i directories.", heppy_sample.name, len(heppy_sample.candidate_directories) ) 

            # Merge
            from RootTools.core.Sample import Sample
            logger.info( "Now making new sample map from %i directories and for %i heppy samples to be stored in %s", len(dpm_directories), len(heppy_samples), cache_file )
            self.sample_map = {}
            getSamplePerFile = True
            for heppy_sample in heppy_samples:
                if len(heppy_sample.candidate_directories)==0:
                    logger.info("No directory found for %s", heppy_sample.name)
                else:
                    #normalization, files = walker.combine_cmg_directories(\
                    normalization, filesAndNorms= walker.combine_cmg_directories(\
                            cmg_directories = {dpm_directory:self.cmg_directories[data_path][dpm_directory] for data_path, dpm_directory in heppy_sample.candidate_directories }, 
                            multithreading = getattr( options , "nomultithreading", True) , 
                        )
                    filesAndNorms = [ ('root://hephyse.oeaw.ac.at/'+f[0],f[1] ) for f in filesAndNorms ]
                    files = [ f[0] for f in filesAndNorms]
                    logger.info( "Sample %s: Found a total of %i files with normalization %3.2f", heppy_sample.name, len(files), normalization)

                    #self.sample_map[heppy_sample] = Sample.fromFiles(
                    #    heppy_sample.name, 
                    #    #files = ['root://hephyse.oeaw.ac.at/'+f for f in files],
                    #    files = files,
                    #    normalization = normalization, 
                    #    treeName = 'tree', isData = heppy_sample.isData, maxN = maxN)
                    #self.sample_map[heppy_sample].filesAndNorms = filesAndNorms
                    heppy_sample.filesAndNorms    = filesAndNorms
                    heppy_sample.normalization    = normalization
                    self.sample_map[heppy_sample] = heppy_sample
                    logger.info("Combined %i directories for sample %s to a total of %i files with normalization %3.2f", len(heppy_sample.candidate_directories), heppy_sample.name, len(files), normalization)

            # Store cache file
            dir_name = os.path.dirname( cache_file ) 
            if len(self.sample_map.keys())>0:
                if not os.path.exists( dir_name ): os.makedirs( dir_name )
                pickle.dump( self.sample_map, file( cache_file, 'w') )
                logger.info( "Created MC sample cache %s", cache_file )
            else:
                logger.info( "Skipping to write %s because map is empty.", cache_file )

    @property                
    def heppy_sample_names( self ):
        return [s.name for s in self.sample_map.keys()]

    def from_heppy_sample( self, heppy_sample, maxN = -1):
        if self.sample_map.has_key( heppy_sample ):
            res = self.sample_map[heppy_sample]
            if maxN>0: res.files = res.files[:maxN]
            #res.heppy = heppy_sample
            return res
    def from_heppy_samplename( self, heppy_samplename, maxN = -1):
        for heppy_sample in self.sample_map.keys():
            if heppy_samplename==heppy_sample.name:
                res = self.sample_map[heppy_sample]
                if maxN>0: res.files = res.files[:maxN]
                #res.heppy = heppy_sample
                return res
        


if __name__ == "__main__":
    # Proxy certificate
    from RootTools.core.helpers import renew_proxy
    # Make proxy in afs to allow batch jobs to run
    proxy_path = os.path.expandvars('$HOME/private/.proxy')
    proxy = renew_proxy( proxy_path )
    logger.info( "Using proxy %s"%proxy )

    # Moriond MC
    mc_cache_file = '/afs/hephy.at/work/n/nrad/DegenerateStop/dpm_sample_caches/8020_mAODv2_v7.pkl'
    cmgTuples_8025_mAODv2_v7 = ['/dpm/oeaw.ac.at/home/cms/store/user/nrad/cmgTuples/8025_mAODv2_v7/', "/dpm/oeaw.ac.at/home/cms/store/user/nrad/cmgTuples/8025_mAODv2_v7_1/RunIISummer16MiniAODv2/" ]
    mc_Moriond_dpm_directories = cmgTuples_8025_mAODv2_v7
    #from CMGTools.RootTools.samples.samples_13TeV_RunIISummer16MiniAODv2 import mcSamples as heppy_mc_Moriond_samples
    #mc_heppy_mapper = heppy_mapper( heppy_mc_Moriond_samples, mc_Moriond_dpm_directories, mc_cache_file)
    
    
    
    # Moriond MC
    mc_cache_file = '/afs/hephy.at/work/n/nrad/DegenerateStop/dpm_sample_caches/8020_mAODv2_v7_test.pkl'
    cmgTuples_8025_mAODv2_v7 = [ "/dpm/oeaw.ac.at/home/cms/store/user/nrad/cmgTuples/8025_mAODv2_v7//RunIISummer16MiniAODv2/ZJetsToNuNu_HT-100To200_13TeV-madgraph/"]
    #mc_Moriond_dpm_directories = cmgTuples_8025_mAODv2_v7
    from Workspace.DegenerateStopAnalysis.samples.cmgTuples.RunIISummer16MiniAODv2_v7 import allComponents as cmgSamples
    #cmgTuples = 
    #from CMGTools.RootTools.samples.samples_13TeV_RunIISummer16MiniAODv2 import mcSamples as heppy_mc_Moriond_samples
    test_heppy_mapper = heppy_mapper( cmgSamples, cmgTuples_8025_mAODv2_v7, mc_cache_file)
