#
# copy limit output files from DPM to NFS (removing duplicates
#   and checking for failed jobs and files from previous submissions)
#
import sys,os
import subprocess
import time
#
# options / arguments
#  arguments are:
#  - DPM directory
#  - crab job directory
#
from optparse import OptionParser
parser = OptionParser()
parser.add_option("--copy", "-c", dest="copy", action="store_true", help="copy files",default=False)
parser.add_option("--target","-t", dest="target", default=None, action="store", help="target directory")
(options, args) = parser.parse_args()

assert len(args)>1

dpmDir = args[0]
dpmBase = os.path.basename(os.path.normpath(dpmDir))
crabDir = args[1]

p1 = subprocess.Popen(["dpns-ls","-l",dpmDir],stdout=subprocess.PIPE)
lines = p1.communicate()[0].splitlines()
retcode = p1.returncode

filelist = [ ]
for line in lines:
    assert line.find(".tgz")>=0
    fields = line.split()
    ttuple = time.strptime(fields[5],'%b')
    ttuple = time.strptime(" ".join(fields[5:8]),'%b %d %H:%M')
    t = time.mktime(ttuple)
    fn = fields[-1]
    fn = fn[0:fn.find(".tgz")]
    fnf = fn.split("_")
    filelist.append( ( int(fnf[1]), t, int(fnf[2]), fnf[3], fn, str(fields[5:8]) ) )

filelist.sort()

crablist = [ f for f in os.listdir(crabDir+"/res") if f.startswith("CMSSW_") and f.endswith(".stdout") ]

last = None
notInCrabDir = [ ]
missingJobs = [ ]
failedJobs = [ ]
duplicateJobs = [ ]
for fs in filelist:
    retcode = os.system("grep -Fq "+fs[4]+" "+crabDir+"/res/CMSSW_"+str(fs[0])+".stdout")
#    p2 = subprocess.Popen(["grep","-Fq",fs[4],crabDir+"/res/CMSSW_"+str(fs[0])+".stdout"],stdout=subprocess.PIPE)
#    p2out = p2.communicate()[0]
#    retcode = p2.returncode
    if retcode != 0:
        print "Not in CRAB: ",fs[4]
        notInCrabDir.append(fs)
    if last != None:
        if fs[0] == last[0]:
            print "Duplicate: ",last
            duplicateJobs.append(last)
        elif fs[0] > (last[0]+1):
            ind = last[0] + 1
            while ind < fs[0]:
                if "CMSSW_"+str(ind)+".stdout" in crablist:
                    print "Failed(?) job number ",ind
                    failedJobs.append(ind)
                else:
                    print "Missing job number ",ind
                    missingJobs.append(ind)
                ind += 1        
    last = fs
    
print ""
print "Last jobID = ",filelist[-1][4]
print  "Not in CRAB: ",[ x[4] for x in notInCrabDir ]
print "Duplicate: ",[ x[4] for x in duplicateJobs ]
print "Missing: ",missingJobs
print "Failed(?): ",failedJobs


if options.target != None:
    targetDir = options.target
else:
    targetDir = "/data/adamwo/"+dpmBase
lcg = os.environ['LCG_LOCATION']
rfcp = lcg+"/bin/rfcp"
toCopy = [ ]
if options.copy and not os.path.isdir(targetDir):
    assert not os.path.exists(targetDir)
    os.mkdir(targetDir)
for fs in filelist:
    fn = fs[4]+".tgz"
    if fs in notInCrabDir or fs in duplicateJobs:
        print "Skipping duplicate / nonCrab ",fs[4]
        continue
    if os.path.exists(targetDir+"/"+fn):
        print "Skipping existing file ",fs[4]
        continue    
    if options.copy:
        os.system(rfcp+" "+dpmDir+"/"+fn+" "+targetDir+"/"+fn)
    else:
        toCopy.append(rfcp+" "+dpmDir+"/"+fn+" "+targetDir+"/"+fn)

if not options.copy:
    print "Files to be copied:"
    for l in toCopy:
        print l
        

