#!/usr/bin/env python
"""
Usage:
submitBatch.py path/to/file_with_commands
or
submitBatch.py "command"

Will submit a batch job for each command line in the file_with_commands.
--dpm: Will create proxy certificate.
"""

from optparse import OptionParser
import hashlib, time
import os
import re

parser = OptionParser()

# user info
hephy_user = os.getenv("USER")
hephy_user_initial = os.getenv("USER")[0]

# Host Info
hostname = os.getenv("HOSTNAME")
hosts_info = {
            'heplx' : {'site': 'hephy.at' , 'batch':'slurm'   ,'def_opts':''},
            'lxplus': {'site': 'cern.ch'  , 'batch':'lxbatch' ,'def_opts':'-q 8nh'}
        }
host   = [ h for h in hosts_info.keys() if h in hostname ]
if not len(host)==1:
    raise Exception("Host name (%s) was not recognized in hosts_info=%s"%(hostname, hosts_info) )
else:
    host = host[0]
host_info = hosts_info[host]
submit_time = time.strftime("%a%H%M%S", time.localtime())

# Parser
parser.add_option("--title", dest="title",
                  help="Job Title on batch", default = "batch" )
parser.add_option("--output", dest="output", 
                  default="/afs/hephy.at/work/%s/%s/batch_output/"%(hephy_user_initial, hephy_user),
                  help="path for batch output ")
parser.add_option("--qos", dest="qos",
                  help="Job Title viewied in squeue", default = "" )
parser.add_option("--opts", dest="opts",
                  help="Give a string for any extra options", default = host_info['def_opts'] )
parser.add_option('--dpm', dest="dpm", default=False, action='store_true', help="Use dpm?")
parser.add_option('--expandvars', dest="expandvars", default=False, action='store_true', help="Expand environmental variables in each line before submiting them")


(options,args) = parser.parse_args()

batch_job_title  = options.title
batch_output_dir = options.output

batch_job_file = "batch_job_" + batch_job_title

qos        = options.qos
qos_options = ['1h']
if qos and qos not in qos_options:
    raise Exception("The queue option (%s) is not recognized .... it should be one of %s"%(qos, qos_options))

def make_batch_job(batch_job_file, batch_job_title, batch_output_dir, command):
    # If X509_USER_PROXY is set, use existing proxy.
    if options.dpm:
       pass
       # if host == 'lxplus':
       #     from StopsDilepton.tools.user import cern_proxy_certificate
       #     proxy_location = cern_proxy_certificate
       # else:
       #     proxy_location = None

       # from RootTools.core.helpers import renew_proxy
       # proxy = renew_proxy( proxy_location )

       # print "Using proxy certificate %s" % proxy
       #proxy_cmd = "export X509_USER_PROXY=%s"%proxy
       proxy_cmd = "export X509_USER_PROXY=/afs/cern.ch/user/{username_init}/{username}/.proxy".format(username_init = hephy_user_initial, username = hephy_user )
    else:
        proxy_cmd = ""            

    import subprocess

    if host == 'heplx':
        template =\
"""\
#!/bin/sh
#SBATCH -J {batch_job_title}
#SBATCH -D {pwd}
#SBATCH -o {batch_output_dir}{batch_job_file}.%j.out

{proxy_cmd}
voms-proxy-info -all
eval \`"scram runtime -sh"\` 
echo CMSSW_BASE: {cmssw_base} 
echo Executing user command  
echo "{command}"
{command} 

voms-proxy-info -all

""".format(\
                command          = command,
                cmssw_base       = os.getenv("CMSSW_BASE"),
                batch_output_dir = batch_output_dir,
                batch_job_file   = batch_job_file,
                batch_job_title  = batch_job_title,
                pwd              = os.getenv("PWD"),
                proxy_cmd = proxy_cmd
              )
    elif host == 'lxplus':
        template =\
"""\
#!/bin/bash
export CMSSW_PROJECT_SRC={cmssw_base}/src

cd $CMSSW_PROJECT_SRC
eval `scramv1 ru -sh`

alias python={python_release}
which python
python --version

{proxy_cmd}
voms-proxy-info -all
echo CMSSW_BASE: $CMSSW_BASE
cd {pwd}
echo Executing user command while in $PWD
echo "{command}"
{command} 

voms-proxy-info -all

""".format(\
                command          = command,
                cmssw_base       = os.getenv("CMSSW_BASE"),
                #batch_output_dir = batch_output_dir,
                #batch_job_title  = batch_job_title,
                pwd              = os.getenv("PWD"),
                proxy_cmd = proxy_cmd,
                python_release = subprocess.check_output(['which', 'python']).rstrip(), 
              )

    batch_job = file(batch_job_file, "w")
    batch_job.write(template)
    batch_job.close()
    return

def getCommands( line , expandvars = False ):
    commands = []
    split = None
    try:
        m=re.search(r"SPLIT[0-9][0-9]*", line)
        split=int(m.group(0).replace('SPLIT',''))
    except:
        pass
    line = line.split('#')[0]
    if line:
        if expandvars and "{" in line:
            print "before", line
            #line = os.path.expandvars(line)
            line = line.format(**fargs)#os.path.expandvars(line)
            print "after", line
        if split:
            print "Splitting in %i jobs" % split
            for i in range(split):
                commands.append(line+" --nJobs %i --job %i"%( split, i ))
        else:
            commands.append(line)
    return commands

if __name__ == '__main__':
    if not len(args) == 1:
        raise Exception("Only one argument accepted! Instead this was given: %s"%args)
    if os.path.isfile(args[0]):
        print "Reading commands from file: %s"%args[0]
        commands = []
        fargs    = {}
        with open(args[0]) as f:
            for line in f.xreadlines():
                if options.expandvars and line.startswith("!"):
                    line = line.split("#")[0].replace("!","").replace(" ","").replace("\n","")
                    k,v = line.split("=",1)
                    fargs[k]=v
                    
                    continue
                commands.extend( getCommands( line.rstrip("\n") , expandvars = options.expandvars) )
        print fargs    
    elif type(args[0]) == type(""):
        commands = getCommands( args[0] , expandvars = options.expandvars) 
    if commands:
        print "host:", host
        if host == 'heplx':
            if not os.path.isdir(batch_output_dir):
                os.mkdir(batch_output_dir)

            print "\n Batch system .out file to be written in directory \n %s \n "%batch_output_dir

            for command in commands:
                #job_file = tmp_job_dir +"/" + batch_job_file
                hash_string = hashlib.md5("%s"%time.time()).hexdigest()
                job_file = batch_job_file.rstrip(".sh")+"_%s.sh"%hash_string
                make_batch_job( job_file , batch_job_title, batch_output_dir , command  )
                os.system("sbatch %s %s"%(job_file , qos))
                os.remove(job_file)

        elif host == 'lxplus':
            opts = options.opts
            title= options.title
            title_opt = "-J %s"%title
            for command in commands:
                hash_string = hashlib.md5("%s"%time.time()).hexdigest()
                job_file = batch_job_file.rstrip(".sh")+"_%s.sh"%hash_string
                make_batch_job( job_file , batch_job_title, batch_output_dir , command  )
                submit_command = "bsub %s '%s'  < %s"%(opts , title_opt , job_file )
                os.system(submit_command)
                os.remove(job_file)
