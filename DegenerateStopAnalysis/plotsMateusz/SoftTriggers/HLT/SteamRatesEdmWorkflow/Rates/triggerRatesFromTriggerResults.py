import os
import ROOT,math,json
from DataFormats.FWLite import Handle, Events
from aux import physicsStreamOK,scoutingStreamOK
from aux import datasets_for_corr as good_datasets

# inputs
menuVersion = 'V18'

sampName = "Run2017E-EphemeralZeroBias1"
#sampName = "Run2017E-EphemeralHLTPhysics1"
json_file = '/afs/cern.ch/user/n/ndaci/public/STEAM/Production/Xudong_HLTv4/json_HLTPhysicsL1v4_2p0e34.txt'

#sampName = "Run2017F-ZeroBias_EOS"
#json_file = 'Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt'

sampOpt = "originalL1PS_switchL1PSFalse_full"

filesInput = ["../Prod/outputSamples/SoftTriggers-{menuVersion}/{sampName}/hlt_SoftTriggers-{menuVersion}_{sampName}_{sampOpt}.root".format(menuVersion=menuVersion,sampName=sampName,sampOpt=sampOpt)]
outputDir = "rateResults/SoftTriggers-%s/SF_ZB/%s/rateResults_%s_%s"%(menuVersion,sampName, sampName, sampOpt)

if not os.path.isdir(outputDir): os.makedirs(outputDir)

#auxiliary functions
def checkTriggerIndex(name,index, names):
    if not 'firstTriggerError' in globals():
        global firstTriggerError
        firstTriggerError = True
    if index>=names.size():
        if firstTriggerError:
            for tr in names: print tr
            print
            print name," not found!"
            print
            firstTriggerError = False
            return False
        else:
            return False
    else:
        return True

def check_json(runNo_in, LS):
    runNo = str(runNo_in)
    file1=open(json_file,'r')
    inp1={}
    text = ""
    for line1 in file1:
        text+=line1
    inp1 = json.loads(text)
    #print inp1.keys()
    if runNo in inp1:
        for part_LS in inp1[runNo]:
            if LS >= part_LS[0] and LS <= part_LS[1]:
                return True
    return False


#Dataset
from Menu_HLT import groupMap as triggersGroupMap
from Menu_HLT import datasetMap as  triggersDatasetMap
from Menu_HLT import streamMap as  triggersStreamMap



triggerList = []
primaryDatasetList = []
primaryDatasetCounts = {}
datasets = {}

groupList = []
groupCounts = {}
groupCountsShared = {}
groupCountsPure = {}
groups = {}

streamList = []
streamCounts = {}

root_file=ROOT.TFile("%s/corr_histos.root"%outputDir,"RECREATE")

#Handles and labels
triggerBits, triggerBitLabel = Handle("edm::TriggerResults"), ("TriggerResults::MYHLT")


#Looping over the inputfiles
n = 0
nPassed_Physics = 0
nPassed_Scouting = 0

#List of triggers
myPaths = []
reducedDatasets = []
myPassedEvents = {}

nLS = 0


triggerDatasetCorrMatrix = {}
datasetDatasetCorrMatrix = {}

nFiles = len(filesInput)
iFile  = 0

for inputfile in filesInput:

    print "Processing file #",iFile,"/",nFiles
    iFile += 1

    events = Events (inputfile)

    #Looping over events in inputfile

    runAndLsList = []
    for event in events: 
        #if n == 100000: break
        #taking trigger informations: names, bits and products
        event.getByLabel(triggerBitLabel, triggerBits)
        names = event.object().triggerNames(triggerBits.product())    
        runnbr = event.object().id().run()
        runls = event.object().id().luminosityBlock()
        runstr = str((runnbr,runls))
        if not check_json(runnbr, runls): continue
        if not runstr in runAndLsList:
            nLS = nLS +1
            runAndLsList.append(runstr)

        #initializing stuff
        if n<1:
            for name in names.triggerNames():
                name = str(name)
                if ("HLTriggerFirstPath" in name) or ("HLTriggerFinalPath" in name): continue
                if not (name.startswith("HLT_") or name.startswith("DST_")): continue
                myPaths.append(name)
                triggerKey = name.rstrip("0123456789")
                if not triggerKey in triggersDatasetMap: continue
                datasets.update({str(triggerKey):triggersDatasetMap[triggerKey]})
                groups.update({str(triggerKey):triggersGroupMap[triggerKey]})
                if not (name in triggerList) :triggerList.append(name)
                for dataset in triggersDatasetMap[triggerKey]:
                    if not dataset in primaryDatasetList: primaryDatasetCounts.update({str(dataset):0}) 
                    if not dataset in primaryDatasetList: primaryDatasetList.append(dataset)
                for group in triggersGroupMap[triggerKey]:
                    if not group in groupList: groupCounts.update({str(group):0}) 
                    if not group in groupList: groupCountsShared.update({str(group):0}) 
                    if not group in groupList: groupCountsPure.update({str(group):0}) 
                    if not group in groupList: groupList.append(group)
                for stream in triggersStreamMap[triggerKey]:
                    if not stream in streamList:
                        streamCounts.update({str(stream):0})
                        streamList.append(stream)
                


            #inizialize the number of passed events
            for i in range(len(myPaths)):
                myPassedEvents[myPaths[i]]=0

            #Initialize the correlation matrices
            for dataset1 in primaryDatasetList:
                reducedDatasets.append(dataset1)
                aux_dic = {}
                for dataset2 in primaryDatasetList:
                    aux_dic[dataset2] = 0
                datasetDatasetCorrMatrix[dataset1] = aux_dic
                aux_dic={}
                for trigger in myPaths:
                    triggerKey = trigger.rstrip("0123456789")
                    aux_dic[triggerKey] = 0
                triggerDatasetCorrMatrix[dataset1] = aux_dic





        iPath = 0       

        #here we initialize the counter per dataset to avoid counting a DS twice
        kPassedEvent = False
        datasetsCountsBool = primaryDatasetCounts.fromkeys(primaryDatasetCounts.keys(),False)
        groupCountsBool = groupCounts.fromkeys(groupCounts.keys(),False)
        streamCountsBool = streamCounts.fromkeys(streamCounts.keys(),False)
        triggerCountsBool = {}
        for i in range(0, len(myPaths)):
            triggerCountsBool[myPaths[i]] = False
        myGroupFired = []
        for triggerName in myPaths:
            index = names.triggerIndex(triggerName)
            if checkTriggerIndex(triggerName,index,names.triggerNames()):
                #checking if the event has been accepted by a given trigger
                if triggerBits.product().accept(index):
                    myPassedEvents[triggerName]=myPassedEvents[triggerName]+1 
                    triggerCountsBool[triggerName] = True
                    #we loop over the dictionary keys to see if the paths is in that key, and in case we increase the counter
                    triggerKey = triggerName.rstrip("0123456789")
                    if triggerKey in datasets.keys():
                        for dataset in datasets[triggerKey]:
                            if datasetsCountsBool[dataset] == False :
                                datasetsCountsBool[dataset] = True
                                primaryDatasetCounts[dataset] = primaryDatasetCounts[dataset] + 1
                    if triggerKey in groups.keys():
                        for group in groups[triggerKey]:
                            if not physicsStreamOK(triggerKey): continue
                            if group not in myGroupFired: 
                                myGroupFired.append(group)
                                groupCounts[group] = groupCounts[group] + 1
                    if triggerKey in triggersStreamMap.keys():
                        for stream in triggersStreamMap[triggerKey]:
                            if streamCountsBool[stream] == False:
                                streamCountsBool[stream] = True
                                streamCounts[stream] += 1

                        



                    if kPassedEvent == False:
                        #We only want to count physics streams in the total rate
                        if physicsStreamOK(triggerKey): nPassed_Physics += 1
                        if scoutingStreamOK(triggerKey): nPassed_Scouting += 1
                        kPassedEvent = True

            iPath = iPath+1        
        for dataset1 in primaryDatasetList:
            if not datasetsCountsBool[dataset1]: continue
            for dataset2 in primaryDatasetList:
                if not datasetsCountsBool[dataset2]: continue
                datasetDatasetCorrMatrix[dataset1][dataset2] += 1
            for trigger in myPaths:
                if not triggerCountsBool[trigger]: continue
                triggerKey = trigger.rstrip("0123456789")
                triggerDatasetCorrMatrix[dataset1][triggerKey] += 1

        if len(myGroupFired) == 1:
            groupCountsPure[myGroupFired[0]] = groupCountsPure[myGroupFired[0]] + 1            

        for group in myGroupFired:
            groupCountsShared[group] = groupCountsShared[group] + 1./len(myGroupFired)

            
        n = n+1




#Printing output

#for run 296786
#scalingFactor = round((3352./23.31)*250*(55./46)*(2544./973.)/float(n) ,2)

#for run 297219
#scalingFactor  = round((7*75*107)/float(n) ,2)

#for run 297674
#scalingFactor = round((8.6*75*107)/float(n) ,2)
nu_LHC = 11245.45
n_bunch = 1866 #1909 # projection: 2556/1909 

#PS_dataset = 580. # EphemeralPhysics1
PS_dataset = 12503*72 # L1_ZeroBias * HLT_ZeroBias 
SF_lumi = 1.5e34/1.34e34 # projection 2.2e34/1.34e34 
#SF_bunches = n_bunch/1909 
#SF_PU = ... 

SF_general = SF_lumi*PS_dataset/(nLS*23.31) # works for ZB as well
SF_ZB =      SF_lumi*nu_LHC*n_bunch/n # n = total number of (presaled ZB) events

#scalingFactor = SF_general
scalingFactor = SF_ZB

print 'nLS:', nLS
print 'scalingFactor:', scalingFactor
#print 'scalingFactor_general:', SF_general
#print 'scalingFactor_ZB:', SF_ZB

physics_path_file = open('%s/output.path.physics.csv'%outputDir, 'w')
physics_path_file.write("Path, Groups, Counts, Rates (Hz)\n")
physics_path_file.write("Rate SF, , , " + str(scalingFactor)+"\n")
physics_path_file.write("N_LS, , , " + str(nLS)+"\n")
physics_path_file.write("N_processed, , , " + str(n)+"\n")
totalRate = float(nPassed_Physics)*scalingFactor
physics_path_file.write("Total Physics Rate (Hz), , , " + str(totalRate)+"\n")
physics_path_file.write('\n')



scouting_path_file = open('%s/output.path.scouting.csv'%outputDir, 'w')
scouting_path_file.write("Path, Groups, Counts, Rates (Hz)\n")
totalRate = float(nPassed_Scouting)*scalingFactor
scouting_path_file.write("Total Scouting Rate (Hz), , , " + str(totalRate))
scouting_path_file.write('\n')



#2d histograms for the correlation matrices
triggerDataset_histo=ROOT.TH2F("trigger_dataset_corr","Trigger-Dataset Correlations",len(primaryDatasetList),0,len(primaryDatasetList),len(myPaths),0,len(myPaths))
datasetDataset_histo=ROOT.TH2F("dataset_dataset_corr","Dataset-Dataset Correlations",len(primaryDatasetList),0,len(primaryDatasetList),len(primaryDatasetList),0,len(primaryDatasetList))

triggerDataset_file = open('%s/output.trigger_dataset_corr.csv'%outputDir, 'w')
datasetDataset_file = open('%s/output.dataset_dataset_corr.csv'%outputDir, 'w')
triggerDataset_file.write("Trigger-Dataset correlations\n")
datasetDataset_file.write("Dataset-Dataset correlations\n")


i = 0
for dataset in primaryDatasetList:
    i += 1
    triggerDataset_file.write(", " + dataset)
    datasetDataset_file.write(", " + dataset)
    triggerDataset_histo.GetXaxis().SetBinLabel(i, dataset)
    datasetDataset_histo.GetXaxis().SetBinLabel(i, dataset)
triggerDataset_file.write("\n")
datasetDataset_file.write("\n")




for i in range(0,len(myPaths)):
    #print myPaths[i], myPassedEvents[i], myPassedEvents[i]*scalingFactor 
    trigger = myPaths[i]
    triggerKey = trigger.rstrip("0123456789")
    group_string = ""
    if triggerKey in groups.keys():
        for group in groups[triggerKey]:
            group_string = group_string + group + " "
    if physicsStreamOK(triggerKey):
        physics_path_file.write('{}, {}, {}, {}'.format(trigger, group_string, myPassedEvents[trigger], round(myPassedEvents[trigger]*scalingFactor, 2)))
        physics_path_file.write('\n')
    if scoutingStreamOK(triggerKey):
        scouting_path_file.write('{}, {}, {}, {}'.format(trigger, group_string, myPassedEvents[trigger], round(myPassedEvents[trigger]*scalingFactor, 2)))
        scouting_path_file.write('\n')


    triggerDataset_file.write(triggerKey)
    j = 0
    triggerDataset_histo.GetYaxis().SetBinLabel(i+1, triggerKey)
    for dataset in primaryDatasetList:
        j += 1
        if (myPassedEvents[trigger] > 0): triggerDatasetCorrMatrix[dataset][triggerKey] = triggerDatasetCorrMatrix[dataset][triggerKey]*scalingFactor #/myPassedEvents[trigger]
        triggerDataset_file.write(", " + str(round(triggerDatasetCorrMatrix[dataset][triggerKey], 2)))
        triggerDataset_histo.SetBinContent(j, i, round(triggerDatasetCorrMatrix[dataset][triggerKey], 2))
    triggerDataset_file.write("\n")
    


physics_dataset_file = open('%s/output.dataset.physics.csv'%outputDir, 'w')
scouting_dataset_file = open('%s/output.dataset.scouting.csv'%outputDir, 'w')

physics_dataset_file.write("Dataset, Counts, Rates (Hz)\n")
scouting_dataset_file.write("Dataset, Counts, Rates (Hz)\n")
i = 0
for key in primaryDatasetList:
    isPhysicsDataset = False
    isScoutingDataset = False

    for trigger in myPaths:
        triggerKey = trigger.rstrip("0123456789")
        if physicsStreamOK(triggerKey) and (key in triggersDatasetMap[triggerKey]): isPhysicsDataset = True
        if scoutingStreamOK(triggerKey) and (key in triggersDatasetMap[triggerKey]): isScoutingDataset = True
    if isPhysicsDataset:
        physics_dataset_file.write(str(key) + ", " + str(primaryDatasetCounts[key]) +", " + str(round(primaryDatasetCounts[key]*scalingFactor, 2)))
        physics_dataset_file.write('\n')
    if isScoutingDataset:
        scouting_dataset_file.write(str(key) + ", " + str(primaryDatasetCounts[key]) +", " + str(round(primaryDatasetCounts[key]*scalingFactor, 2)))
        scouting_dataset_file.write('\n')

    i += 1
    datasetDataset_file.write(key)
    datasetDataset_histo.GetYaxis().SetBinLabel(i, key)
    j = 0
    for key2 in primaryDatasetList:
        j += 1
        if (primaryDatasetCounts[key] > 0): datasetDatasetCorrMatrix[key2][key] = datasetDatasetCorrMatrix[key2][key]*scalingFactor #/primaryDatasetCounts[key]
        datasetDataset_file.write(", " + str(round(datasetDatasetCorrMatrix[key2][key],2)))
        datasetDataset_histo.SetBinContent(j, i, round(datasetDatasetCorrMatrix[key2][key], 2))
    datasetDataset_file.write("\n")


group_file = open('%s/output.group.csv'%outputDir,'w')
group_file.write('Groups, Counts, Rates (Hz), Pure Counts, Pure Rates (Hz), Pure+Shared Counts, Pure+Shared Rates (Hz)\n')
for key in groupCounts.keys():
    group_file.write(str(key) + ", " + str(groupCounts[key]) +", " + str(round(groupCounts[key]*scalingFactor, 2)) + ", " + str(groupCountsPure[key]) +", " + str(round(groupCountsPure[key]*scalingFactor, 2)) + ", " + str(groupCountsShared[key]) +", " + str(round(groupCountsShared[key]*scalingFactor, 2)))
    group_file.write('\n')


stream_file = open('%s/output.stream.csv'%outputDir,'w')
stream_file.write('Streams, Counts, Rates (Hz)\n')
for stream in streamCounts.keys():
    stream_file.write(str(stream) + ", " + str(streamCounts[stream]) +", " + str(round(streamCounts[stream]*scalingFactor, 2)) + "\n")

#Save histos
root_file.cd()
triggerDataset_histo.Write()
datasetDataset_histo.Write()
root_file.Close()
