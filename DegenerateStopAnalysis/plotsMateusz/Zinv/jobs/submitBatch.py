#!/usr/bin/env python
"""
Usage:
submitBatch.py path/to/file_with_commands
or
submitBatch.py command

Will submit a batch job for each command line in the file_with_commands
"""

from optparse import OptionParser
import hashlib, time
import os

parser = OptionParser()
(options,args) = parser.parse_args()

cmssw_base = os.getenv("CMSSW_BASE"),
hephy_user = os.getenv("USER")
hephy_user_initial = os.getenv("USER")[0]
slurm_job_file="Zinv_batch_job"
slurm_job_title="Zinv_Mateusz"
slurm_output_dir="%s/src/Workspace/DegenerateStopAnalysis/plotsMateusz/Zinv/jobs/logs/"%(cmssw_base)
#slurm_output_dir="/afs/hephy.at/work/%s/%s/slurm_output"%(hephy_user_initial, hephy_user)

if not os.path.isdir(slurm_output_dir):
    os.mkdir(slurm_output_dir)


def make_slurm_job(slurm_job_file, slurm_job_title, slurm_output_dir, command):
    template =\
"""\
#!/bin/sh
#SBATCH -J {slurm_job_title}
#SBATCH -D {pwd}
#SBATCH -o {slurm_output_dir}{slurm_job_title}_%j.out

eval \`"scram runtime -sh"\` 
echo CMSSW_BASE: {cmssw_base} 
echo Executing user command  
echo "{command}"
{command} 

""".format(\
                command          = command,
                cmssw_base       = os.getenv("CMSSW_BASE"),
                slurm_output_dir = slurm_output_dir,
                slurm_job_title  = slurm_job_title,
                pwd              = os.getenv("PWD")
              )

    slurm_job = file(slurm_job_file, "w")
    slurm_job.write(template)
    slurm_job.close()
    return


if __name__ == '__main__':
    if not len(args) == 1:
        raise Exception("Only one argument accepted! Instead this was given: %s"%args)
    if os.path.isfile(args[0]):
        print "Reading commands from file: %s"%args[0]
        commands = []
        with open(args[0]) as f:
            for line in f.xreadlines():
                line = line.rstrip("\n")
                if line:
                    if line.startswith("#"):    
                        print "Skipping line, seems to be a comment %s"%line
                        continue
                    commands.append(line)
    elif type(args[0]) == type(""):
        commands = [args[0]]
    if commands:
        #hash_string = hashlib.md5("%s"%time.time()).hexdigest()
        #tmp_job_dir = "tmp_%s"%hash_string
        #os.mkdir(tmp_job_dir)
        for command in commands:
            #job_file = tmp_job_dir +"/" + slurm_job_file
            hash_string = hashlib.md5("%s"%time.time()).hexdigest()
            job_file = slurm_job_file.rstrip(".sh")+"_%s.sh"%hash_string
            make_slurm_job( job_file , slurm_job_title, slurm_output_dir , command  )
            os.system("sbatch %s"%job_file)
            os.remove(job_file)
