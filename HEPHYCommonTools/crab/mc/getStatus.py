import os, sys
dpmDir = "/dpm/oeaw.ac.at/home/cms/store/user/schoef/pat_140212"
p1 = os.popen("ls 8TeV-* -d")
subDirs=[]
while True:
  l=p1.readline()
  if not l:break
  subDirs.append(l[:-1])
p1.close()

totNJobs = {}
dataset={}
for s in subDirs:
  p1 = os.popen("grep 'total # of jobs' "+s+"/log/crab.log | tail -n1")
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
  p1 = os.popen("dpns-ls "+dpmDir+"/"+s+"|wc -l")
  l=p1.readline()
  p1.close()
  if not l: continue
  finishedJobs[s] = int(l[:-1].split()[-1])

tot=0 
done=0
for k in sorted(totNJobs.keys()):
  tot+=totNJobs[k]
  done+=finishedJobs[k]
  print k,"tot",totNJobs[k],"fin",finishedJobs[k]," -> ",round(finishedJobs[k]/float(totNJobs[k])*100,1),"%", dataset[k]

print "\nTotal number of jobs:",done,"/",tot

#p2 = os.popen(["grep", "ERROR"], stdin=p1.stdout, stdout=PIPE)
#output = p2.communicate()[0]
#
#for line in open("file"):
# if "search_string" in line:
#   print line
