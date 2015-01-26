import pickle

if not globals().has_key("myList"):
  globals()["myList"] = pickle.load(file("/afs/hephy.at/scratch/k/kancsar/CMSSW_5_3_3_patch2/src/Workspace/RA4Analysis/plots/topDiLepton_Met100Corr.pkl"))

for entry in myList:       
  entry["event"] = int(entry["event"])

allEventNumbers = sorted(list(set([ k["event"] for k in myList ])))

Events = []

for e in allEventNumbers[:20]:
  solutions = filter(lambda x: x["event"]==e, myList)
  for s in solutions:
#    print "before sorting:", s['Filename'], '\t', s["t1ptMin"], s['t2ptMin'], '\t','(', int(round(s['nu1ptMin'])),',', int(round(s['nu2ptMin'])), ')', '\t', s["t1ptTrue"], s['t2ptTrue'],'(', int(round(s['nu1ptTrue'])),',',int(round(s['nu2ptTrue'])),')'
    print s['Filename'], '\t', s["deltaPhiMin"], s["deltaPhiTrue"],'(', int(round(s['nu1ptMin'])),'/',int(round(s['nu2ptMin'])),') (',int(round(s['nu1ptTrue'])),'/',int(round(s['nu2ptTrue'])),')'
  solutions = sorted(solutions, key=lambda k: abs(k["deltaPhiMin"]))
#  for s in solutions:
#    print "TTbarMomentum after sorting:", s["t1ptMin"], s['t2ptMin']

  print "Found greatest solution for deltaPhi:", solutions[3]["deltaPhiMin"]
  Events.append(solutions[0])
  print

# EOF  
