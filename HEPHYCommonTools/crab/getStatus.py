import os, sys

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--dpmDir", dest="dpmDir", default="/dpm/oeaw.ac.at/home/cms/store/user/schoef/pat_140314", type="string", action="store", help="dpmDir: What to do.")
parser.add_option("--searchString", dest="searchString", default="mc/8*TeV", type="string", action="store", help="which subDirs to look at")
#parser.add_option("--small", dest="small", action="store_true", help="Just do a small subset.")

(options, args) = parser.parse_args()
print "dpmDir:",options.dpmDir, 'searchString', options.searchString

#dpmDir = "/dpm/oeaw.ac.at/home/cms/store/user/schoef/pat_140314"
p1 = os.popen("ls "+options.searchString+" -d")
subDirs=[]
while True:
  l=p1.readline()
  if not l:break
  subDirs.append(l[:-1])
p1.close()


totNJobs = {}
dataset={}
for s in subDirs:
  p1 = os.popen("grep --binary-files=text 'total # of jobs' "+s+"/log/crab.log | tail -n1")
  l=p1.readline()
  p1.close()
  if l:
    totNJobs[s] = int(l[:-1].split()[-1])

  p1 = os.popen("grep 'Requested dataset:' "+s+"/log/crab.log | tail -n1")
  l=p1.readline()
  p1.close()
  if l: 
    dataset[s] = l[:-1].split('Requested dataset:')[1].split()[0] 

finishedJobs = {}
for s in subDirs:
  p1 = os.popen("dpns-ls -l "+options.dpmDir+"/"+(s.split('/')[-1])+"|wc -l")
  l=p1.readline()
  p1.close()
  if not l: continue
  finishedJobs[s] = int(l[:-1].split()[-1])

print totNJobs, finishedJobs, dataset
tot=0 
done=0
for k in sorted(totNJobs.keys()):
  tot+=totNJobs[k]
  done+=finishedJobs[k]
  if dataset.has_key(k):
    print k,"tot",totNJobs[k],"fin",finishedJobs[k]," -> ",round(finishedJobs[k]/float(totNJobs[k])*100,1),"%", dataset[k]
  else:
    print k,"tot",totNJobs[k],"fin",finishedJobs[k]," -> ",round(finishedJobs[k]/float(totNJobs[k])*100,1),"%"

print "\nTotal number of jobs:",done,"/",tot

#p2 = os.popen(["grep", "ERROR"], stdin=p1.stdout, stdout=PIPE)
#output = p2.communicate()[0]
#
#for line in open("file"):
# if "search_string" in line:
#   print line
