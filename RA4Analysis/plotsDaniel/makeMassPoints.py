import pickle

massPoints = pickle.load(file('/afs/hephy.at/data/easilar01/Ra40b/pickleDir/T5qqqqWW_mass_nEvents_xsec_pkl'))

allMassPoints = []

for mgluino in massPoints.keys():
  for mneutralino in massPoints[mgluino]:
    allMassPoints.append((mgluino,mneutralino))

deltaM = [1000,800,600,400,200,0]

massPointDict = {}

for dM in deltaM:
  massPointDict[dM] = []

for massPoint in allMassPoints:
  for dM in deltaM:
    if dM < (massPoint[0]-massPoint[1]): break
  massPointDict[dM].append(massPoint)
#  print dM, (massPoint[0]-massPoint[1])


binBorders = [0,200,400,600,800,1000]
bins = []

for i,b in enumerate(binBorders):
  lowerBound = binBorders[i]
  print i
  if i>len(binBorders)-2: upperBound = -1
  else: upperBound = binBorders[i+1]
  bins.append((lowerBound, upperBound))
  
