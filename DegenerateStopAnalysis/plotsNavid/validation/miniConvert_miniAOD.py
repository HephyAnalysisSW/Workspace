from DataFormats.FWLite import Events, Handle
from Workspace.DegenerateStopAnalysis.navidValidationTools import getHandle, calcDeltaR
#from PhysicsTools.PythonAnalysis import *
from math import *
import ROOT
#import numpy
import os


rootFilesIn= lambda dir : [dir+fn for fn in os.listdir(dir) if any([fn.endswith(ext) for ext in ['.root'] ])];

#Select item in stepDict
step=0
doStuff = 1
prefix="RUNII_vtx_genMatch_IP_wrt_0_"
#nEvents -1 for all events
nEvents=1000
outputDir="./"



#recM=getHandle(trees['stop'],events['stop'],labelTypeList[5]['type'],labelTypeList[5]['label'],iEvent=517)
#genP=getHandle(trees['stop'],events['stop'],labelTypeList[6]['type'],labelTypeList[6]['label'],iEvent=517)
#genMu=[ig for ig in genP if (abs(ig.pdgId())==13 and abs(ig.mother(0).pdgId())==1000006) ]
#
#[(ig,jr, calcDeltaR(i.phi(),j.phi(),i.eta(),j.eta())) for (ig,i) in enumerate(genMu) for (jr,j) in enumerate(recM)  ]


def isGenMatchedFromSUSY(tree, fwlEvt, iEvt,Mother=1000006):
  maxDeltaR=0.4
  pdgId=13
  p1='mu'
  p2='genP'
  recoMu = getHandle(tree, fwlEvt, "vector<pat::Muon>",                "slimmedMuons",         iEvent=iEvt)
  genP   = getHandle(tree, fwlEvt, "vector<pat::PackedGenParticle>",   "packedGenParticles",   iEvent=iEvt)
  nRecoMu=len(recoMu)
  ret = [ 0 for i in range(nRecoMu)]
  nGenP=len(genP)
  #genMu=[]
  #genMu= [ (i,igp) for i,igp in enumerate(genP) if abs(igp.pdgId())==13]
  #genMuFromStop= [ (i,iGenMu) for (i,iGenMu) in genMu if abs(iGenMu.mother(0).pdgId())==Mother if len(genMu)!=0]
  #print genMuFromStop
  #for gMu in range(len(igmfsDict):
  best_dR=100
  dRList=[]
  first=1
  #print 'n gp', nGenP, ' nRecoMu', nRecoMu
  if nGenP > 0:
    for ig,igp in enumerate(genP):
      if abs(igp.pdgId()) == pdgId and abs(igp.mother(0).pdgId()) == Mother:
        #print 'genP is Mu', igp
        if nRecoMu  > 0:
          dRList=[]
          for ir,iRecoMu in enumerate(recoMu):
            #if first:
            #  ret = [ 0 for i in range(nRecoMu)] 
            #  first = 0
            dR = calcDeltaR( igp.phi(), iRecoMu.phi(), igp.eta(), iRecoMu.eta() )
            if dR < maxDeltaR:
              dRList.append(dR)
            else:
              dRList.append(99999)
          minDr, iMinDr = min((val, idx) for (idx, val) in enumerate(dRList))
          if minDr != 99999:
            ret[iMinDr]=1
          #print ig, ir
           #ret.append(match)
  return ret


def isGenMatched(tree, fwlEvt, iEvt):
  maxDeltaR=0.4
  pdgId=13
  p1='mu'
  p2='genP'
  recoMu = getHandle(tree, fwlEvt, "vector<pat::Muon>",                "slimmedMuons",         iEvent=iEvt)
  genP   = getHandle(tree, fwlEvt, "vector<pat::PackedGenParticle>",   "packedGenParticles",   iEvent=iEvt)
  nRecoMu=len(recoMu)
  ret = [ 0 for i in range(nRecoMu)]
  nGenP=len(genP)
  #genMu=[]
  #genMu= [ (i,igp) for i,igp in enumerate(genP) if abs(igp.pdgId())==13]
  #genMuFromStop= [ (i,iGenMu) for (i,iGenMu) in genMu if abs(iGenMu.mother(0).pdgId())==Mother if len(genMu)!=0]
  #print genMuFromStop
  #for gMu in range(len(igmfsDict):
  best_dR=100
  dRList=[]
  first=1
  #print 'n gp', nGenP, ' nRecoMu', nRecoMu
  if nGenP > 0:
    for ig,igp in enumerate(genP):
      if abs(igp.pdgId()) == pdgId:
        #print 'genP is Mu', igp
        if nRecoMu  > 0:
          dRList=[]
          for ir,iRecoMu in enumerate(recoMu):
            #if first:
            #  ret = [ 0 for i in range(nRecoMu)] 
            #  first = 0
            dR = calcDeltaR( igp.phi(), iRecoMu.phi(), igp.eta(), iRecoMu.eta() )
            if dR < maxDeltaR:
              dRList.append(dR)
            else:
              dRList.append(99999)
          minDr, iMinDr = min((val, idx) for (idx, val) in enumerate(dRList))
          if minDr != 99999:
            ret[iMinDr]=1
          #print ig, ir
           #ret.append(match)
  return ret

def testGoodVertex(vertex):
    if vertex.isFake():
        return False
    if vertex.ndof()<=4:
        return False
    if abs(vertex.z())>24:
        return False
    if vertex.position().Rho()>2:
        return False
    return True

def innerTrack_dz_PV(tree, fwlEvt, iEvt):
  recoMu = getHandle(tree, fwlEvt, "vector<pat::Muon>",            "slimmedMuons",                          iEvent=iEvt)
  vtx    = getHandle(tree, fwlEvt, "vector<reco::Vertex>",         "offlineSlimmedPrimaryVertices",         iEvent=iEvt)
  nRecoMu=len(recoMu)
  ret = [ -1000 for i in range(nRecoMu)]
  for ir,iRecoMu in enumerate(recoMu):
    if iRecoMu.innerTrack().isNonnull():
      if testGoodVertex(vtx[0]):
        vertex=vtx[0]
      else: vertex=vtx[1]
      ret[ir]= iRecoMu.innerTrack().dz( vertex.position() )
    else: ret[ir]=-1000
  return ret

def innerTrack_dxy_PV(tree, fwlEvt, iEvt):
  recoMu = getHandle(tree, fwlEvt, "vector<pat::Muon>",            "slimmedMuons",                          iEvent=iEvt)
  vtx    = getHandle(tree, fwlEvt, "vector<reco::Vertex>",         "offlineSlimmedPrimaryVertices",         iEvent=iEvt)
  nRecoMu=len(recoMu)
  ret = [ -1000 for i in range(nRecoMu)]
  for ir,iRecoMu in enumerate(recoMu):
    if iRecoMu.innerTrack().isNonnull():
      if testGoodVertex(vtx[0]):
        vertex=vtx[0]
      else: vertex=vtx[1]
      ret[ir]= iRecoMu.innerTrack().dxy( vertex.position() )
    else: ret[ir]=-1000
  return ret

def innerTrack_dz_BS(tree, fwlEvt, iEvt):
  recoMu = getHandle(tree, fwlEvt, "vector<pat::Muon>",            "slimmedMuons",                          iEvent=iEvt)
  bs    = getHandle(tree, fwlEvt, "<reco::BeamSpot>",         "offlineBeamSpot",         iEvent=iEvt)
  nRecoMu=len(recoMu)
  ret = [ -1000 for i in range(nRecoMu)]
  for ir,iRecoMu in enumerate(recoMu):
    if iRecoMu.innerTrack().isNonnull():
      ret[ir]= iRecoMu.innerTrack().dz( bs[0].position() )
    else: ret[ir]=-1000
  return ret


def innerTrack_dxy_BS(tree, fwlEvt, iEvt): 
  recoMu = getHandle(tree, fwlEvt, "vector<pat::Muon>",            "slimmedMuons",                          iEvent=iEvt)
  bs    = getHandle(tree, fwlEvt, "<reco::BeamSpot>",         "offlineBeamSpot",         iEvent=iEvt)
  nRecoMu=len(recoMu)
  ret = [-1000 for i in range(nRecoMu)]
  for ir,iRecoMu in enumerate(recoMu):
    if iRecoMu.innerTrack().isNonnull():
      ret[ir]= iRecoMu.innerTrack().dxy( bs[0].position() ) 
    else: ret[ir]=-1000
  return ret





#def innerTrack_dxy_0(tree, fwlEvt, iEvt): 
#  recoMu = getHandle(tree, fwlEvt, "vector<pat::Muon>",            "slimmedMuons",                          iEvent=iEvt)
#  bs    = getHandle(tree, fwlEvt, "<reco::BeamSpot>",         "offlineBeamSpot",         iEvent=iEvt)
#  nRecoMu=len(recoMu)
#  ret = [-1000 for i in range(nRecoMu)]
#  for ir,iRecoMu in enumerate(recoMu):
#    if iRecoMu.innerTrack().isNonnull():
#      ret[ir]= iRecoMu.innerTrack().dxy(  ) 
#    else: ret[ir]=-1000
#  return ret
#
#
#def innerTrack_dz_0(tree, fwlEvt, iEvt): 
#  recoMu = getHandle(tree, fwlEvt, "vector<pat::Muon>",            "slimmedMuons",                          iEvent=iEvt)
#  bs    = getHandle(tree, fwlEvt, "<reco::BeamSpot>",         "offlineBeamSpot",         iEvent=iEvt)
#  nRecoMu=len(recoMu)
#  ret = [-1000 for i in range(nRecoMu)]
#  for ir,iRecoMu in enumerate(recoMu):
#    if iRecoMu.innerTrack().isNonnull():
#      ret[ir]= iRecoMu.innerTrack().dz( bs[0].position() ) 
#    else: ret[ir]=-1000
#  return ret





stepDict=[
        #{'name':'test',               'filelist': rootFilesIn("/data/nrad/T2DegStop13TeV/GEN/t2degen1step/")  },
        #{'name':'stop',               'filelist': ['root://hephyse.oeaw.ac.at//dpm/oeaw.ac.at/home/cms/store/user/nrad/T2DegStop2j_300_270_GENSIM/T2DegStop2j_300_270_MINIAOD/a279b5108ada7c3c0926210c2a95f22e/T2DegStop2j_300_270_miniAOD_2_1_yQN.root'] },
        #{'name':'WJets',              'filelist': ['root://xrootd.unl.edu//store/mc/Phys14DR/WJetsToLNu_13TeV-madgraph-pythia8-tauola/MINIAODSIM/PU20bx25_PHYS14_25_V1-v1/00000/02215B44-2D70-E411-90A3-0025905A60B8.root']},
        #{'name':'stop',               'filelist': ['/data/nrad/T2DegStop13TeV/T2DegStop2j_sample_miniAOD.root']},
        {'name':'stop',               'filelist': ['/data/nrad/T2DegStop13TeV/RunII/step3_PAT.root']},
        {'name':'WJets',              'filelist': ['../WJetsToLNu_13TeV_Phys14_miniAOD.root']},
        {'name':'TT',                 'filelist': ['../TT_13TeV_Phys14PU40bx25_miniAOD.root']},

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
                   {'varName':'pdgId',               'varFunc': lambda ev: ev.pdgId()},
                   {'varName':'isLoose',             'varFunc': lambda ev: int(ev.isLooseMuon()) if abs(ev.pdgId()) == 13 else -11},  
                   {'varName':'isGenMatched',        'varCompFunc': isGenMatched    }, 
                   {'varName':'isGenMatchedSUSY',        'varCompFunc': isGenMatchedFromSUSY    }, 
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
                  {'varName':'mass',                'varFunc': lambda ev: ev.mass()             },    
                  {'varName':'energy',              'varFunc': lambda ev: ev.energy()           },  

                  {'varName':'vtx_x',              'varFunc': lambda ev: ev.vertex().x()           },  
                  {'varName':'vtx_y',              'varFunc': lambda ev: ev.vertex().y()           },  
                  {'varName':'vtx_z',              'varFunc': lambda ev: ev.vertex().z()           },  


                  {'varName':'track_dxy',       'varFunc': lambda ev: ev.track().dxy() if ev.track().isNonnull() else -1000                },  
                  {'varName':'track_dxy_vtx',       'varFunc': lambda ev: ev.track().dxy(ev.vertex()) if ev.track().isNonnull() else -1000     },  
                  {'varName':'innerTrack_dxy',  'varFunc': lambda ev: ev.innerTrack().dxy() if ev.track().isNonnull() else -1000           },  
                  {'varName':'innerTrack_dxy_vtx',  'varFunc': lambda ev: ev.innerTrack().dxy(ev.vertex()) if ev.track().isNonnull() else -1000},  

                  {'varName':'track_dz',       'varFunc': lambda ev: ev.track().dz() if ev.track().isNonnull() else -1000                },  
                  {'varName':'track_dz_vtx',       'varFunc': lambda ev: ev.track().dz(ev.vertex()) if ev.track().isNonnull() else -1000     },  
                  {'varName':'innerTrack_dz',  'varFunc': lambda ev: ev.innerTrack().dz() if ev.track().isNonnull() else -1000           },  
                  {'varName':'innerTrack_dz_vtx',  'varFunc': lambda ev: ev.innerTrack().dz(ev.vertex()) if ev.track().isNonnull() else -1000}, 

                  {'varName':'innerTrack_dz_PV',  'varCompFunc': innerTrack_dz_PV}, 
                  {'varName':'innerTrack_dxy_PV',  'varCompFunc': innerTrack_dxy_PV}, 
                  {'varName':'innerTrack_dz_BS',  'varCompFunc': innerTrack_dz_BS}, 
                  {'varName':'innerTrack_dxy_BS',  'varCompFunc': innerTrack_dxy_BS}, 


                  {'varName':'innerTrack_dxy_0',  'varFunc': lambda ev: ev.innerTrack().dxy(ROOT.Math.XYZPoint(0.0,0.0,0.0)) if ev.track().isNonnull() else -1000 }, 
                  {'varName':'innerTrack_dz_0',  'varFunc': lambda ev: ev.innerTrack().dz(ROOT.Math.XYZPoint(0.0,0.0,0.0)) if ev.track().isNonnull() else -1000 }, 
 
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





vtxVarList= [
               { 'dataType' : ('Int_t','I')  , 'vars': (
  
                   {'varName':'isGood',     'varFunc': lambda vtx: int(testGoodVertex(vtx))               },
                   {'varName':'isFake',     'varFunc': lambda vtx: int(vtx.isFake())               },
                   {'varName':'ndof',       'varFunc': lambda vtx: int(vtx.ndof())                 },
                                                       )    
               } ,
               { 'dataType' : ('Float_t','F'), 'vars': (
                  {'varName':'x',          'varFunc': lambda vtx: vtx.x()                     },
                  {'varName':'y',          'varFunc': lambda vtx: vtx.y()                     },
                  {'varName':'z',          'varFunc': lambda vtx: vtx.z()                     },
                  {'varName':'rho',        'varFunc': lambda vtx: vtx.position().Rho()        },
                                                       ) 
               }
         ]



bsVarList= [
               { 'dataType' : ('Int_t','I')  , 'vars': (
                   {'varName':'type',     'varFunc': lambda vtx: int(vtx.type())               },
                                                       )    
               } ,
               { 'dataType' : ('Float_t','F'), 'vars': (
                  {'varName':'x',          'varFunc': lambda bs: bs.position().x()                     },
                  {'varName':'y',          'varFunc': lambda bs: bs.position().y()                     },
                  {'varName':'z',          'varFunc': lambda bs: bs.position().z()                     },
                  {'varName':'rho',        'varFunc': lambda bs: bs.position().Rho()        },
                                                       ) 
               }
         ]




#Label and Type for Handling
labelTypeList = [\
                  {'name':"bs"            , 'type':"<reco::BeamSpot>"              , 'label':"offlineBeamSpot", 'varCount':1       ,'varList': bsVarList },
                  {'name':"vtx"           , 'type':"vector<reco::Vertex>"           ,'label':"offlineSlimmedPrimaryVertices", 'varCount':100       ,'varList': vtxVarList },
                  {'name':"jet"           , 'type':"vector<pat::Jet> ",               'label':"slimmedJets",   'varCount':100,              'varList': varList },  
                  {'name':"met"           , 'type':"vector<pat::MET> ",               'label':"slimmedMETs",   'varCount':100,              'varList': varList },  
                  #{'name':"el"            , 'type':"vector<pat::Electron> ",           'label':"slimmedElectrons",   'varCount':100,     'varList': lepVarList },  
                  {'name':"mu"            , 'type':"vector<pat::Muon> ",               'label':"slimmedMuons",   'varCount':100,             'varList': lepVarList },  
                  {'name':"genP"          ,'type':"vector<pat::PackedGenParticle>"   ,'label':"packedGenParticles", 'varCount':2000       ,'varList': genVarList },
                  #{'name':"ak4Jets",  'type':"vector<reco::GenJet> ",       'label':"ak4GenJets",   'varCount':100,              'varList': varList },  
                  #{'name':"genP",     'type':"vector<reco::GenParticle>",   'label':"genParticles", 'varCount':20000,            'varList': varList },  
                  #{'name':"genMet",   'type':"vector<reco::GenMET>",        'label':"genMetTrue",   'varCount':200,              'varList': varList },
                ]

########## Adding chains and creating the struct ################

#stepDict[step]['output'] = ROOT.TFile(stepDict[step]['name']+'.root','RECREATE')
#stepDict[step]['output'] = ROOT.TFile(stepDict[step]['filelist'][0].replace('.root','_miniConvert.root'),'RECREATE')


#events = Events(stepDict[step]['filelist'])
#events.toBegin()


trees = {}
events = {}
for s in stepDict:
  events[s['name']] = Events(s['filelist'])  
  events[s['name']].toBegin()
  trees[s['name']] = ROOT.TChain('Events')
  for f in stepDict[step]['filelist']:
    trees[s['name']].Add(f)


c=trees[stepDict[step]['name']]
evt = events[stepDict[step]['name']]
evt.toBegin()


#################################################################



if doStuff:

  print evt._filenames

  structString="struct MyStruct{ "
  structString+="Int_t " + ' , '.join(x['name']+'Count' for x in labelTypeList) + ';'
  #structString+="Float_t " + ' , '.join(x['name']+'_'+y+'[20000]' for x in labelTypeList for y in x['vars']) + ';'
  #python abuse! make this more readable?
  for iStruct in [x['varList'][dT]['dataType'][0]+' ' + ' , '.join( x['name'] +'_' + y['varName'] + '['+ str(x['varCount'])  +']' for y in x['varList'][dT]['vars'] ) +'; ' for x in labelTypeList for dT in range(len(x['varList']))]:
    structString += iStruct
  structString+="};" 
  ROOT.gROOT.ProcessLine(structString)
  s = ROOT.MyStruct()

  if nEvents==-1:
    nEvents=c.GetEntries()

  nVerbose=int(nEvents/100)

  stepDict[step]['output'] = ROOT.TFile(outputDir + stepDict[step]['name'] + '%s_miniConvert.root'%prefix,'RECREATE')
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

    if iEvent%100 == 0: print iEvent
    c.GetEntry(iEvent)
    evt.to(iEvent)

    for item in labelTypeList:
      #if iEvent%100 == 0: print name 
      name = item['name']; typ = item['type'];  label = item['label'];  nameCount = name + 'Count'
      lgp=getHandle(c,evt,typ,label)
      #print lgp
      #gps = Handle(typ)
      #lgp = label
      #evt.getByLabel(lgp,gps)
      #gps = gps.product()
      #try:
      #  lgp = list(gps)
      #except TypeError:
      #  lgp=[0]
      #  lgp[0]=gps
      setattr(s,nameCount,len(lgp))
      for j in range(len(lgp)):
        for v in item['varList']:
          for vvar in v['vars']:
            varName = name+'_'+vvar['varName']
            #getattr(s, varName)[j] = getattr(lgp[j],vvar)()i
            if vvar.has_key('varFunc'):
              getattr(s, varName)[j] = vvar['varFunc'](lgp[j])
            elif vvar.has_key('varCompFunc'):
              if j==0:
                #getattr(s,varName)[j] = vvar['varCompFunc'](c,evt,iEvent)[j]
              
                outList = vvar['varCompFunc'](c,evt,iEvent)
                #print j,vvar['varName'], iEvent, outList
                for jj in range(len(lgp)):
                  getattr(s,varName)[jj] = outList[jj]
              else: pass
  
    treeDict['tree'].Fill()
  stepDict[step]['output'].Write()
  stepDict[step]['output'].Close()

    

#def getHandle(iTree,fwEvt,iEvent,iTyp,iLabel):
#  #events = Events(iTree)
#  #events.toBegin()
#  iTree.GetEntry(iEvent)
#  fwEvt.to(iEvent)
#  gps = Handle(iTyp)
#  lgp = iLabel
#  fwEvt.getByLabel(lgp,gps)
#  gps = gps.product()
#  try:
#    lgp = list(gps)
#    return lgp
#    print lgp
#  except TypeError:
#    return gps
#  #return gps 

