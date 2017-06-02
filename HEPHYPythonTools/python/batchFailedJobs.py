''' 
Find batch failed jobs and create a shell file with commands to resubmit the jobs.

    disappearing jobs: jobs submitted for which no batch .out file is created
    un-successful jobs: jobs submitted for which the "success string" is not found in the batch .out file 

In case a clean up is necessary when resubmitting the jobs, this is done either with the argument 
"overwriteOutputFiles", if implemented in the program to be run, otherwise has to be done by hand. 
FIXME: overwriteOutputFiles not integrated


As of now, the script is tailored for slurm batch system.
'''
# imports python standard modules or functions

import argparse
import logging
import sys
import tempfile
import os
import pprint
import glob

# imports user modules or functions

import Workspace.DegenerateStopAnalysis.tools.helpers as helpers
import collections

__author__ = "Vasile Mihai Ghete"

# classes and functions

# functions


def get_parser():
    ''' Argument parser.

    Include all the options from parent parsers, if any.

    '''
    argParser = argparse.ArgumentParser(
        description="Argument parser for batchFailedJobs",
    )

    argParser.add_argument(
        '--logLevel',
        action='store',
        nargs='?',
        type=str,
        choices=[
            'CRITICAL', 'ERROR', 'WARNING',
            'INFO', 'DEBUG', 'TRACE', 'NOTSET'
        ],
        default='INFO',
        help="Log level for logging"
    )

    argParser.add_argument(
        '--verbose',
        action='store_true',
        help=''.join([
            "Switch for print statements, ",
            "for those who can not survive a job without seeing something printed ",
            "on the screen. \n bool flag set to True if used"
        ])
    )

    argParser.add_argument(
        '--overwriteOutputFiles',
        action='store_true',
        help="Overwrite existing output files, bool flag set to True if used"
    )

    argParser.add_argument(
        '--batch_input_script',
        action='store',
        nargs='?',
        type=str,
        default=None,
        help="Input sh file used to submit the jobs. If None, disapearring jobs are not tested for"
    )

    argParser.add_argument(
        '--str_job_command',
        action='store',
        nargs='?',
        type=str,
        default='python ',
        help="Substring needed to identify the beginning of the job command"
    )

    argParser.add_argument(
        '--batch_output_dir',
        action='store',
        nargs='?',
        type=str,
        help="Directory containing all '.out' files produced by the batch system"
    )

    argParser.add_argument(
        '--str_batch_output_file',
        action='store',
        nargs='?',
        type=str,
        help="Fixed part of '.out' file names produced by the batch system"
    )

    argParser.add_argument(
        '--str_successful_job',
        action='store',
        nargs='?',
        type=str,
        default='End of ',
        help="String indicating that a job has finished successfully."
    )

    argParser.add_argument(
        '--sh_file',
        action='store',
        nargs='?',
        type=str,
        default='batchFailedJobs.sh',
        help="Name of the sh file containing the failed commands, in the batch_output_dir or current directory"
    )

    #
    return argParser


def get_logger(logLevel, logFile):
    ''' Logger definition.

    Use the basic definition of the logger from helpers.

    '''

    get_logger_rtuple = helpers.get_logger(
        'batchFailedJobs', logLevel, logFile)
    logger = get_logger_rtuple.logger
    numeric_level = get_logger_rtuple.numeric_level
    fileHandler = get_logger_rtuple.fileHandler

    logger.propagate = False

    # set logging level for additional modules, including imported modules
    helpers.logger.setLevel(numeric_level)

    # set handlers for additional modules, including imported modules
    helpers.logger.addHandler(fileHandler)

    return logger


def get_job_command(out_file):
    ''' Get the job command for the submitted job.

    '''

    str_executing = "Executing user command"
    found_executing = False

    full_command = None

    for line in open(out_file).readlines():
        if found_executing:

            full_command = line.strip()
            break

        if str_executing in line:
            found_executing = True

    # the full command must be found
    if full_command is None:
        raise Exception(
            '\n No command was found for .out file \n {of} \n Review arguments.'.format(of=out_file))
        sys.exit()

    return full_command


def get_job_status(out_file, str_successful_job):
    ''' Get the job status for the submitted job, based on the "success string".
    
    Returns True for successful, False for failed.

    '''

    # this command put the whole file in the memory, so it
    # could fail for large files
    # TODO implement reverse reading with generator
    good_job = False
    for line in reversed(open(out_file).readlines()):
        if str_successful_job in line:
            good_job = True
            break

    return good_job


def batchFailedJobs(argv=None):
    ''' Yields and event numbers for samples.

    '''

    if argv is None:
        argv = sys.argv[1:]

    # parse command line arguments
    args = get_parser().parse_args()

    verbose = args.verbose

    batch_input_script = args.batch_input_script

    batch_output_dir = args.batch_output_dir
    str_batch_output_file = args.str_batch_output_file
    str_successful_job = args.str_successful_job
    str_job_command = args.str_job_command

    print '\n Arguments parsed: \n', args, '\n'

    # check if the batch_output_dir is writable by the user,
    # if yes, write the log file and the sh file there
    # otherwise, write in the current directory the script is executed

    if os.access(batch_output_dir, os.W_OK):
        out_dir = batch_output_dir
    else:
        out_dir = '.'

    sh_file = os.path.join(out_dir, args.sh_file)

    # logger

    # logging configuration
    logLevel = args.logLevel

    # job logger, write file in the dataset directory
    prefixLogFile = 'batchFailedJobs' + '_' + logLevel + '_'
    jobLogFile = tempfile.NamedTemporaryFile(
        suffix='.log', prefix=prefixLogFile, dir=out_dir, delete=False
    )

    logger = get_logger(logLevel, jobLogFile.name)

    print "\nLog file stored in: \n", jobLogFile.name, '\n'
    print "\nsh file written in: \n", sh_file,  '\n'
    #
    logger.info(
        "\n Log file for module batchFailedJobs \n"
    )

    logger.info(
        ''.join([
            "\n Job arguments: \n\n %s \n",
        ]),
        pprint.pformat(vars(args))
    )

    # find the '.out' files in the batch_output_dir

    filelist_out = []

    try:
        if os.path.exists(batch_output_dir):

            filelist_out = glob.glob(
                os.path.join(
                    batch_output_dir,
                    ''.join([str_batch_output_file, '*.out'])
                )
            )

    except IOError:
        logger.warning(
            "\n Directory \n  %s \n requested for output files %s does not exist. \n",
            batch_output_dir,
            str_batch_output_file
        )
        sys.exit(1)

    # make a list of submitted commands having a batch .out file and their job
    # status

    commands_and_status = []

    for f in filelist_out:

        cmd = get_job_command(f)
        js = get_job_status(f, str_successful_job)

        commands_and_status.append({'job_command': cmd, 'job_status': js})

    # make a list of commands requested to be submitted from the batch
    # submission input script

    jobs_to_submit = []
    jobs_failed = []

    n_jobs_to_submit = 0
    n_out_files = len(filelist_out)

    n_good_jobs = 0
    n_bad_jobs = 0
    n_dis_jobs = 0

    if batch_input_script is None:
        logger.info(
            ''.join([
                "\n Batch submission input script is None \n",
                "\n No search of jobs w/o out file will be done \n",
                "\n Number of jobs requested to be submitted: N/A \n"

            ])
        )

        # find only the number of jobs that have not finished successfully
        fjl = filter(
            lambda x: not x['job_status'], commands_and_status
        )

        jobs_failed = [jc['job_command'] for jc in fjl]

        n_jobs_to_submit = 0

        n_bad_jobs = len(jobs_failed)
        n_good_jobs = n_out_files - n_bad_jobs
        n_dis_jobs = 0

    else:
        # check if the file batch_input_script exists, then add all commands to
        # a list
        try:
            with open(batch_input_script) as b_file:

                for line in b_file:
                    if line.lstrip().startswith(str_job_command):
                        full_command = line.strip()

                        jobs_to_submit.append(full_command)

                n_jobs_to_submit = len(jobs_to_submit)

                # compare jobs_to_submit to commands_and_status

                for job_cmd in jobs_to_submit:

                    jcl = filter(
                        lambda x: x['job_command'] == job_cmd, commands_and_status
                    )

                    if len(jcl) == 0:
                        # job has no .out file
                        jobs_failed.append(job_cmd)
                        n_dis_jobs += 1

                    elif len(jcl) == 1:
                        if not jcl[0]['job_status']:
                            # job did not finished successfully
                            jobs_failed.append(job_cmd)
                            n_bad_jobs += 1
                        else:
                           n_good_jobs += 1
                    else:
                        # more than one job with that command - should not
                        # happen...
                        logger.warning(
                            "\n More than on job with command \n  %s \n",
                            job_cmd
                        )

        except IOError:
            logger.warning(
                "\n Unable to open file \n  %s \n Exiting. \n",
                batch_input_script
            )

            sys.exit(2)

    logger.info(
        ''.join([
            '\n Number of jobs requested to be submitted: {nr_jobs}'.format(
                nr_jobs=n_jobs_to_submit if n_jobs_to_submit > 0 else "N/A"),
            '\n Number of jobs having an batch .out file: {nr_jobs}'.format(
                nr_jobs=n_out_files),
            '\n Number of jobs having no batch .out file: {nr_jobs}'.format(
                nr_jobs=n_dis_jobs if n_dis_jobs > 0 else "N/A"),
            '\n Number of successful jobs: {nr_jobs}'.format(
                nr_jobs=n_good_jobs),
            '\n Number of jobs with errors {nr_jobs}'.format(
                nr_jobs=n_bad_jobs),
            '\n Total number of failed jobs {nr_jobs}\n'.format(
                nr_jobs=(n_bad_jobs + n_dis_jobs)),
        ])
    )

    # write failed jobs to a new sh file

    with open(sh_file, "w") as text_file:
        for cmd in jobs_failed:

            text_file.write(cmd)
            text_file.write('\n\n')

    logger.info(
        "\n Wrote %i failed jobs to \n  %s file \n",
        len(jobs_failed),
        sh_file
    )

    eoj_success = '\n End of batchFailedJobs script.\n'

    logger.info(eoj_success)
    print eoj_success


if __name__ == "__main__":
    sys.exit(batchFailedJobs())
