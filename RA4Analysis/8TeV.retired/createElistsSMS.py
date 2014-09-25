#
# create elists of events for each mass combination in an SMS sample
#
import ROOT
import cPickle
import os
#
# input directory and sample name
#
dirname = "/data/mhickel/pat_121012/sms"
sample = "8-TeV-T1tttt"
# list of files in directory
filenames = [ ]
subdirname = dirname + "/"
if sample!="":  subdirname += sample + "/"
for file in os.listdir(subdirname):
    if os.path.isfile(subdirname+file) and file[-5:]==".root" and file.count("histo")==1:
        filenames.append(subdirname+file)
#        if len(filenames)>10: break
#        if len(filenames)>100: break

# input chain and dictionary with entries / mass combination
entryDict = { }
c = ROOT.TChain("Events")
for file in filenames:  c.Add(file)
# fill elists / mass combination
#   could be accelerated by reading only the two leaves from the tree
nev = c.GetEntries()
for i in range(nev):
    if i%100000==0: print "At entry ",i
    c.GetEntry(i)
    mgl = int(c.GetLeaf("float_RA4Tupelizer_osetMgl_PAT.obj").GetValue()+0.5)
    mN = int(c.GetLeaf("float_RA4Tupelizer_osetMN_PAT.obj").GetValue()+0.5)
    if not mgl in entryDict:  entryDict[mgl] = { }
    if not mN in entryDict[mgl]:
        entryDict[mgl][mN] = ROOT.TEventList("elist_"+str(mgl)+"_"+str(mN))
    entryDict[mgl][mN].Enter(i)
#
# output file list (in order to guarantee same file sequence when using the elists)
#   could be written as TCollection to the root file ...
#
f1 = open("sms_"+sample+"_files.lis","w")
for file in filenames:  f1.write(file+"\n")
f1.close()
#
# output file with event lists / mass combination
#
f2 = ROOT.TFile("sms_"+sample+"_entries.root","recreate")
for mgl in entryDict:
    for mN in entryDict[mgl]:
        entryDict[mgl][mN].Write()
f2.Close()
#f2 = open("sms_"+sample+"_entries.pkl","wb")
#cPickle.dump(entryDict,f2)
#f2.close()
