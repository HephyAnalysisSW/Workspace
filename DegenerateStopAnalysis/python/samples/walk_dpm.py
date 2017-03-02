# Standard imports
import subprocess
import os, re
import shutil
import commands
import subprocess
import uuid
import os
hostname = os.getenv("HOSTNAME")

# Logging
import logging
logger = logging.getLogger(__name__)

# multiprocessing
from multiprocessing import Pool

def is_nonemptydir( line ):
    '''Checks whether a line of output from dpns-ls corresponds to an non-empty directory
    '''
    try:
        lsplit = line.split()
        return lsplit[4]=='0' and int(lsplit[1])>0
    except:
        pass
    return False

def is_nonemptyfile( line ):
    '''Checks whether a line of output from dpns-ls corresponds to an non-empty file
    '''
    try:
        lsplit = line.split()
        return int(lsplit[4])>0 and int(lsplit[1])==1
    except:
        pass
    return False


def is_cmgdirectory( res ):
    ''' Returns true if the directory looks like a cmg directory
    '''
    treeFiles = len(filter(lambda f:f['is_treefile'], res))
    logFiles = len(filter(lambda f:f['is_logfile'], res))
    isCMG = treeFiles>0 and logFiles>0
    if isCMG:
        logger.debug("Found %i tree files and %i log files -> This is a cmg directory.", treeFiles, logFiles)

    return isCMG

def get_job_number(f):
    s=f['path'].split('/')[-1]
    ints = map(int, re.findall(r'\d+', s))
    assert len(ints)>0, 'Couldn\'nt find number in %s'%f['path']
    assert len(ints)<=1, 'Found more than one number in  %s'%f['path']
    return ints[0]

def read_normalization( filename, skimReport_file = 'skimAnalyzerCount/SkimReport.txt'):
    
    #string = commands.getoutput('/usr/bin/rfcat %s | tar xzOf - Output/%s' % (filename, skimReport_file) )
    # string = commands.getoutput('sleep .1;/usr/bin/rfcat %s | tar xzOf - Output/%s' % (filename, skimReport_file) )
    unique_filename = '/tmp/%s' % str(uuid.uuid1())
    #print 'xrdcp root://hephyse.oeaw.ac.at/%s %s; cat %s | tar xzOf - Output/%s' % (filename, unique_filename, unique_filename, skimReport_file) 
    string = commands.getoutput('xrdcp root://hephyse.oeaw.ac.at/%s %s; cat %s | tar xzOf - Output/%s' % (filename, unique_filename, unique_filename, skimReport_file) )
    commands.getoutput('rm %s' % unique_filename )
#    print '/usr/bin/rfcat %s | tar xzOf - Output/%s' % (filename, skimReport_file)
#    process = subprocess.Popen(['sleep.1; /usr/bin/rfcat %s | tar xzOf - Output/%s' % (filename, skimReport_file)], stdout=subprocess.PIPE)
#    string, err = process.communicate()
#    print(string)

    sumW = None
    allEvents = None

    for line in string.split('\n'):
      if "Sum Weights" in line: sumW = float(line.split()[2])
      if 'All Events'  in line: allEvents = float(line.split()[2])

    if sumW is not None: 
        logger.debug( "Read 'Sum Weights' normalization %3.2f from file %s.", sumW, filename )  
        return sumW
    else:                
        logger.debug( "Read 'All Events' normalization %3.2f from file %s.", allEvents, filename )  
        return allEvents

def _wrapper( job ):
    jobID, tree_file, log_file = job
    return ( jobID,tree_file,read_normalization( log_file ) )

class walk_dpm:

    def __init__( self, path ):
        # self.cp_cmd = "/usr/bin/rfcp"
        # self.pretend = False
        self.path = path
        self.tree_filename_prefix = "tree_"
        self.log_filename_prefix  = "output.log_"

    def abs_path( self, rel_path ):
        return os.path.join( self.path, rel_path ).replace('/./', '/')

    def is_treefilename( self, filename ):
        return filename.endswith('.root') and filename.split('/')[-1].startswith( self.tree_filename_prefix )

    def is_logfilename( self, filename ):
        return filename.endswith('.tgz') and filename.split('/')[-1].startswith( self.log_filename_prefix )

    def ls( self, rel_path ):
        ''' Perform ls of the relative dp path
        '''
        abs_path = self.abs_path( rel_path )
        if hostname.startswith("heplx"):
            p = subprocess.Popen(["dpns-ls -l %s" % abs_path], shell = True , stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        elif hostname.startswith("lxplus"):
            abs_path = "srm://hephyse.oeaw.ac.at//" + abs_path
            p = subprocess.Popen(["gfal-ls -l %s" % abs_path], shell = True , stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        res=[]
        for line in p.stdout.readlines():
                line = line[:-1]
                filename = line.split()[-1] # The filename is the last string of the output of dpns-ls
                if is_nonemptydir( line ):
                    res.append( { 'is_dir':True, 'is_file':False, 'path':rel_path+'/'+filename, 'is_logfile':False, 'is_treefile':False } )
                elif is_nonemptyfile( line ):
                    res.append( { 'is_dir':False, 'is_file':True, 'path':rel_path+'/'+filename,\
                        'is_logfile':self.is_logfilename( filename ), 
                        'is_treefile':self.is_treefilename( filename ) } 
                    )
                else:
                    logger.debug( "Skipping line:\n%s", line )
        return res

    def cmg_directory_content( self, rel_path, maxN = -1):
        everything = self.ls( rel_path )

        tree_files = {get_job_number(f): f for f in everything if f['is_treefile']}
        log_files  = {get_job_number(f): f for f in everything if f['is_logfile']}

        result = []

        pairs = [n for n in tree_files.keys() if n in log_files.keys()]
        logger.info( "Now loading %i of %i files from directory %s", min( [ maxN, len(pairs)]) if maxN>0 else len(pairs), len(pairs), self.abs_path( rel_path ) ) 
        for jobID in pairs:
            #normalization = read_normalization( self.abs_path( log_files[jobID]['path'] ) )
            #if normalization is not None:
            result.append( (jobID, self.abs_path(tree_files[jobID]['path']), self.abs_path(log_files[jobID]['path']) ) )

            if maxN > 0 and len(result)>=maxN:
                break
         
        return result 

    def walk_dpm_cmgdirectories( self, rel_path = '.', __result = {}, maxN = -1, path_substrings = []):
        ''' Recursively looks for directories that look like cmg directories
        '''
        res = self.ls( rel_path )
        result = {}
        result.update( __result )
        if is_cmgdirectory( res ):
            logger.debug( "Found CMG dir: %s", rel_path )
            abs_path = self.abs_path(rel_path)
            # If we're not interested, return
            for substr in path_substrings:
                if not substr in abs_path:
                    logger.debug( "Couldn't find %s in %s. Skip.", substr, abs_path )
                    return result
            # Otherwise update
            result[ self.abs_path(rel_path) ] = self.cmg_directory_content( rel_path, maxN = maxN)
        else:
            dirs = filter( lambda f:f['is_dir'], res )
            if len(dirs)>0:
                for f in dirs:
                    logger.debug( "Stepping into %s", f['path'] )
                    result.update( self.walk_dpm_cmgdirectories( f['path'], maxN = maxN, path_substrings = path_substrings) )

            else:
                logger.debug( "Nothing found in %s", rel_path )
        return result


    @staticmethod
    def combine_cmg_directories( cmg_directories, multithreading = True):
        import operator
        all_jobs_ = sum(cmg_directories.values(),[])
        logger.info( "Now reading normalization of %i files. %s", len( all_jobs_ ), "Using multithreading." if multithreading else "Sequential." )
        #all_jobs = [ ( jobID,tree_file,read_normalization( log_file )) for jobID, tree_file, log_file in all_jobs_ ]

        # Read normalization
        if multithreading:
            pool = Pool(processes=20)
            all_jobs = pool.map(_wrapper, all_jobs_)
            pool.close()
            pool.join()
        else:
            all_jobs = map(_wrapper, all_jobs_)

        # Remove the ones I could not read the normalization
        len_all = len(all_jobs)
        all_jobs = filter(lambda j:j[2] is not None, all_jobs)        
        logger.debug("Removing files where I could not read normalization. Reduce all_jobs from %i to %i", len_all, len(all_jobs) )

        all_jobIDs = set( map(operator.itemgetter(0), all_jobs ) )
        all_jobIDs_withNorm = set( map(operator.itemgetter(0,2), all_jobs ) ) 
        for jobID in all_jobIDs:
            if len(filter( lambda w:w[0]==jobID, all_jobIDs_withNorm ))>1:
                instances = filter( lambda w:w[0]==jobID, all_jobIDs_withNorm )
                logger.error( "cmg_directories:\n%r", cmg_directories)
                logger.error( 'Found %i instances of job %i with different normalizations: %r', len(instances), jobID, instances )
                counter = 0
                for job in all_jobs:
                    if job[0] == jobID:
                        logger.error("Duplicate %i %r", counter, job )
                raise RuntimeError( "Found multiple instances of job %i with different normalizations!" % jobID )
        files = [] 
        normalization = 0.
        for jobID in all_jobIDs:
            jobID_, file_, normalization_ = next(tup for tup in all_jobs if tup[0]==jobID)
            if normalization_ is not None:
                normalization += normalization_
                keepFileNormalization = True
                if keepFileNormalization:
                    files.append( (file_ , normalization_))
                else:
                    files.append( file_ )

        return normalization, files

if __name__ == "__main__":

    from RootTools.core.helpers import renew_proxy
    proxy = renew_proxy()
    logger.info( "Using proxy %s"%proxy )
    logger = logging.getLogger(__name__)
    logger.propagate = False



    walker = walk_dpm('/dpm/oeaw.ac.at/home/cms/store/user/schoef/cmgTuples/80X_2/JetHT')
    cmg_directories = walker.walk_dpm_cmgdirectories('.', maxN = 1,  path_substrings = [ 'Run2016B' ] )
