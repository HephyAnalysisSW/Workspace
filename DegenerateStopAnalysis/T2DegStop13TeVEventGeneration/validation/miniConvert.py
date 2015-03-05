from DataFormats.FWLite import Events, Handle
from PhysicsTools.PythonAnalysis import *
from math import *
import ROOT
import numpy
import os


rootFilesIn= lambda dir : [dir+fn for fn in os.listdir(dir) if any([fn.endswith(ext) for ext in ['.root'] ])];

#Select item in stepDict
step=1 # 0 MGDecayed, 1 PythiaDecayed 
outputDir="./"


stepDict=[
        {'name':'MGDecayed',     'filelist': rootFilesIn("/data/nrad/T2DegStop13TeV/GEN/t2degen1step/")  },
        {'name':'PythiaDecayed', 'filelist': rootFilesIn("/data/nrad/T2DegStop13TeV/GEN/t2degen2step/")  }
        #{'name':'MG_GEN_qcut50',     'filelist':["/data/nrad/T2DegStop13TeV/GEN/T2DegStop2j_300_270_GEN.root",] },
        #{'name':'MG_GEN_qcut44',     'filelist':["/data/nrad/T2DegStop13TeV/GEN/T2DegStop_300_270_GEN_qcut44.root",] },
        #{'name':'MG_GEN_qcut55',     'filelist':["/data/nrad/T2DegStop13TeV/GEN/T2DegStop_300_270_GEN_qcut55.root",] },
        #{'name':'MG_GEN_qcut525',    'filelist':["/data/nrad/T2DegStop13TeV/GEN/T2DegStop_300_270_GEN_qcut525.root",] },
        #{'name':'MG_GEN_qcut60',     'filelist':["/data/nrad/T2DegStop13TeV/GEN/T2DegStop_300_270_GEN_qcut60.root",] },
         ]


varList= ( 
            { 'dataType' : ('Int_t','I')  , 'vars': ('pdgId',)         } ,
            { 'dataType' : ('Float_t','F'), 'vars': ('pt','eta','phi') } 
         )

#Label and Type for Handling
labelTypeList = [\
                  {'name':"ak4Jets",  'type':"vector<reco::GenJet> ",       'label':"ak4GenJets",   'varCount':100,              'varList': varList },  
                  {'name':"genP",     'type':"vector<reco::GenParticle>",   'label':"genParticles", 'varCount':20000,            'varList': varList },  
                  {'name':"genMet",   'type':"vector<reco::GenMET>",        'label':"genMetTrue",   'varCount':200,              'varList': varList },
                ]

########## Adding chains and creating the struct ################

#stepDict[step]['output'] = ROOT.TFile(stepDict[step]['name']+'.root','RECREATE')
#stepDict[step]['output'] = ROOT.TFile(stepDict[step]['filelist'][0].replace('.root','_miniConvert.root'),'RECREATE')
stepDict[step]['output'] = ROOT.TFile(outputDir + stepDict[step]['name'] + '_miniConvert.root','RECREATE')

events = Events(stepDict[step]['filelist'])
events.toBegin()
c = ROOT.TChain('Events')
for f in stepDict[step]['filelist']:
  c.Add(f)


structString="struct MyStruct{ "
structString+="Int_t " + ' , '.join(x['name']+'Count' for x in labelTypeList) + ';'
#structString+="Float_t " + ' , '.join(x['name']+'_'+y+'[20000]' for x in labelTypeList for y in x['vars']) + ';'
#python abuse! make this more readable?
for iStruct in [x['varList'][dT]['dataType'][0]+' ' + ' , '.join( x['name'] +'_' + y + '['+ str(x['varCount'])  +']' for y in x['varList'][dT]['vars'] ) +'; ' for x in labelTypeList for dT in range(len(x['varList']))]:
  structString += iStruct
structString+="};" 
ROOT.gROOT.ProcessLine(structString)
s = ROOT.MyStruct()

#################################################################


nEvents=c.GetEntries()
nEvents=1


########
print 'output: ',stepDict[step]['output']
print 'total number of events', c.GetEntries()
print 'using:' , nEvents, 'events'
print stepDict[step]['name']
########


###################   Preparing Tree and Branches  ##############

treeDict={}
treeDict['tree']=ROOT.TTree('Events','Events')
#tree.SetDirectory(0);
for item in labelTypeList:
  name = item['name']; typ = item['type'];  label = item['label'];  nameCount = name + 'Count'
  treeDict['tree'].Branch(name+'Count',ROOT.AddressOf(s,name+'Count'),name+'Count/I')
  for v in item['varList']:
    for vvar in v['vars']:
      varName = name+'_'+vvar
      print varName, v['dataType'][1]
      treeDict['tree'].Branch(varName,ROOT.AddressOf(s,varName),varName+'['+nameCount+']/'+v['dataType'][1])

#################################################################


#################   Even Loop, Filling Tree   ###################

for iEvent in range(nEvents):

  if iEvent%1000 == 0: print iEvent
  c.GetEntry(iEvent)
  events.to(iEvent)

  for item in labelTypeList:
    #if iEvent%100 == 0: print name 
    name = item['name']; typ = item['type'];  label = item['label'];  nameCount = name + 'Count'
    gps = Handle(typ)
    lgp = label
    events.getByLabel(lgp,gps)
    gps = gps.product()
    lgp = list(gps)
    setattr(s,nameCount,len(lgp))
    for j in range(len(lgp)):
      for v in item['varList']:
        for vvar in v['vars']:
          varName = name+'_'+vvar
          getattr(s, varName)[j] = getattr(lgp[j],vvar)()

  treeDict['tree'].Fill()
stepDict[step]['output'].Write()
stepDict[step]['output'].Close()

    


