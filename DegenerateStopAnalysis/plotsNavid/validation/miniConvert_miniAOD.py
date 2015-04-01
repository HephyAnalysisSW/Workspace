from DataFormats.FWLite import Events, Handle
#from PhysicsTools.PythonAnalysis import *
from math import *
import ROOT
#import numpy
import os


rootFilesIn= lambda dir : [dir+fn for fn in os.listdir(dir) if any([fn.endswith(ext) for ext in ['.root'] ])];

#Select item in stepDict
step=0 
doStuff = 0
outputDir="./"


stepDict=[
        #{'name':'test',               'filelist': rootFilesIn("/data/nrad/T2DegStop13TeV/GEN/t2degen1step/")  },
        {'name':'stop',               'filelist': ['root://hephyse.oeaw.ac.at//dpm/oeaw.ac.at/home/cms/store/user/nrad/T2DegStop2j_300_270_GENSIM/T2DegStop2j_300_270_MINIAOD/a279b5108ada7c3c0926210c2a95f22e/T2DegStop2j_300_270_miniAOD_2_1_yQN.root'] },
        #{'name':'test',               'filelist': ['root://xrootd.unl.edu//store/mc/Phys14DR/ADDmonoPhoton_MD-3_d-3_Tune4C_13TeV-pythia8/MINIAODSIM/AVE30BX50_tsg_PHYS14_ST_V1-v1/30000/38E6C54E-EF88-E411-A646-E0CB4E29C4DB.root']  },
        #{'name':'MG_GEN_qcut50',     'filelist': ["/data/nrad/T2DegStop13TeV/GEN/T2DegStop2j_300_270_GEN.root",] },
        #{'name':'MG_GEN_qcut44',     'filelist': ["/data/nrad/T2DegStop13TeV/GEN/T2DegStop_300_270_GEN_qcut44.root",] },
        #{'name':'MG_GEN_qcut55',     'filelist': ["/data/nrad/T2DegStop13TeV/GEN/T2DegStop_300_270_GEN_qcut55.root",] },
        #{'name':'MG_GEN_qcut525',    'filelist': ["/data/nrad/T2DegStop13TeV/GEN/T2DegStop_300_270_GEN_qcut525.root",] },
        #{'name':'MG_GEN_qcut60',     'filelist': ["/data/nrad/T2DegStop13TeV/GEN/T2DegStop_300_270_GEN_qcut60.root",] },
         ]




varList= [
               { 'dataType' : ('Int_t','I')  , 'vars': (
                   {'varName':'pdgId', 'varFunc': lambda ev: ev.pdgId()},
                                                       )    
               } ,
               { 'dataType' : ('Float_t','F'), 'vars': (
                  {'varName':'pt',                  'varFunc': lambda ev: ev.pt()               } ,
                  {'varName':'eta',                 'varFunc': lambda ev: ev.eta()              } ,
                  {'varName':'phi',                 'varFunc': lambda ev: ev.phi()              } ,  
                                                       ) 
               }
         ]

lepVarList= [
               { 'dataType' : ('Int_t','I')  , 'vars': (
                   {'varName':'pdgId', 'varFunc': lambda ev: ev.pdgId()},
                                                       )    
               } ,
               { 'dataType' : ('Float_t','F'), 'vars': (
                  {'varName':'pt',                  'varFunc': lambda ev: ev.pt()               }, 
                  {'varName':'eta',                 'varFunc': lambda ev: ev.eta()              },  
                  {'varName':'phi',                 'varFunc': lambda ev: ev.phi()              },     
                  {'varName':'ecalIso',             'varFunc': lambda ev: ev.ecalIso()          },  
                  {'varName':'hcalIso',             'varFunc': lambda ev: ev.hcalIso()          },    
                  {'varName':'trackIso',            'varFunc': lambda ev: ev.trackIso()         },      
                  {'varName':'neutralHadronIso',    'varFunc': lambda ev: ev.neutralHadronIso() },  
                  {'varName':'chargedHadronIso',    'varFunc': lambda ev: ev.chargedHadronIso() },  
                  {'varName':'numberOfMothers',     'varFunc': lambda ev: ev.numberOfMothers()  },  
                  {'varName':'mass',                'varFunc': lambda ev: ev.mass()             },    
                  {'varName':'energy',              'varFunc': lambda ev: ev.energy()           },  
                                                       ) 
               }
         ]

genVarList= [
               { 'dataType' : ('Int_t','I')  , 'vars': (
                   {'varName':'pdgId', 'varFunc': lambda ev: ev.pdgId()},
                                                       )    
               } ,
               { 'dataType' : ('Float_t','F'), 'vars': (
                  {'varName':'pt',                  'varFunc': lambda ev: ev.pt()               }, 
                  {'varName':'eta',                 'varFunc': lambda ev: ev.eta()              },  
                  {'varName':'phi',                 'varFunc': lambda ev: ev.phi()              },     
                  {'varName':'numberOfMothers',     'varFunc': lambda ev: ev.numberOfMothers()  },  
                  {'varName':'mother_pt',           'varFunc': lambda ev: ev.mother(0).pt()     },  
                  {'varName':'mother_pdgId',        'varFunc': lambda ev: ev.mother(0).pdgId()  },  
                  {'varName':'mother_eta',          'varFunc': lambda ev: ev.mother(0).eta()    },  
                  {'varName':'mother_phi',          'varFunc': lambda ev: ev.mother(0).phi()    },  
                  {'varName':'mother_mass',         'varFunc': lambda ev: ev.mother(0).mass()   },  
                  {'varName':'mother_energy',       'varFunc': lambda ev: ev.mother(0).energy() },  
                  {'varName':'mass',                'varFunc': lambda ev: ev.mass()             },    
                  {'varName':'energy',              'varFunc': lambda ev: ev.energy()           },  
                                                       ) 
               }
         ]

#Label and Type for Handling
labelTypeList = [\
                  {'name':"jet"           , 'type':"vector<pat::Jet> ",               'label':"slimmedJets",   'varCount':100,              'varList': varList },  
                  {'name':"met"           , 'type':"vector<pat::MET> ",               'label':"slimmedMETs",   'varCount':100,              'varList': varList },  
                  {'name':"el"            , 'type':"vector<pat::Electron> ",           'label':"slimmedElectrons",   'varCount':100,     'varList': lepVarList },  
                  {'name':"mu"            , 'type':"vector<pat::Muon> ",               'label':"slimmedMuons",   'varCount':100,             'varList': lepVarList },  
                  {'name':"genP"          ,'type':"vector<pat::PackedGenParticle>"   ,'label':"packedGenParticles", 'varCount':2000       ,'varList': genVarList },
                  #{'name':"ak4Jets",  'type':"vector<reco::GenJet> ",       'label':"ak4GenJets",   'varCount':100,              'varList': varList },  
                  #{'name':"genP",     'type':"vector<reco::GenParticle>",   'label':"genParticles", 'varCount':20000,            'varList': varList },  
                  #{'name':"genMet",   'type':"vector<reco::GenMET>",        'label':"genMetTrue",   'varCount':200,              'varList': varList },
                ]

########## Adding chains and creating the struct ################

#stepDict[step]['output'] = ROOT.TFile(stepDict[step]['name']+'.root','RECREATE')
#stepDict[step]['output'] = ROOT.TFile(stepDict[step]['filelist'][0].replace('.root','_miniConvert.root'),'RECREATE')



events = Events(stepDict[step]['filelist'])
events.toBegin()
c = ROOT.TChain('Events')
for f in stepDict[step]['filelist']:
  c.Add(f)






#################################################################



if doStuff:

  structString="struct MyStruct{ "
  structString+="Int_t " + ' , '.join(x['name']+'Count' for x in labelTypeList) + ';'
  #structString+="Float_t " + ' , '.join(x['name']+'_'+y+'[20000]' for x in labelTypeList for y in x['vars']) + ';'
  #python abuse! make this more readable?
  for iStruct in [x['varList'][dT]['dataType'][0]+' ' + ' , '.join( x['name'] +'_' + y['varName'] + '['+ str(x['varCount'])  +']' for y in x['varList'][dT]['vars'] ) +'; ' for x in labelTypeList for dT in range(len(x['varList']))]:
    structString += iStruct
  structString+="};" 
  ROOT.gROOT.ProcessLine(structString)
  s = ROOT.MyStruct()

  nEvents=c.GetEntries()
  nEvents=500
  nVerbose=int(nEvents/100)

  stepDict[step]['output'] = ROOT.TFile(outputDir + stepDict[step]['name'] + '_miniConvert.root','RECREATE')
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
        varName = name+'_'+vvar['varName']
        print varName, v['dataType'][1]
        treeDict['tree'].Branch(varName,ROOT.AddressOf(s,varName),varName+'['+nameCount+']/'+v['dataType'][1])

  #################################################################


  #################   Even Loop, Filling Tree   ###################

  for iEvent in range(nEvents):

    if iEvent%500 == 0: print iEvent
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
            varName = name+'_'+vvar['varName']
            
            #getattr(s, varName)[j] = getattr(lgp[j],vvar)()
            getattr(s, varName)[j] = vvar['varFunc'](lgp[j])

    treeDict['tree'].Fill()
  stepDict[step]['output'].Write()
  stepDict[step]['output'].Close()

    

def getHandle(iTree,iEvent,iTyp,iLabel):

  #events = Events(iTree)
  #events.toBegin()

  iTree.GetEntry(iEvent)
  events.to(iEvent)
  gps = Handle(iTyp)
  lgp = iLabel
  events.getByLabel(lgp,gps)
  gps = gps.product()
  lgp = list(gps)

  print lgp

  return lgp 

