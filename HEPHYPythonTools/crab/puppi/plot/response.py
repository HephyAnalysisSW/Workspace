from plotDefinitions import *
from plotAliases import *
from plotChains import *

from math import *
import datetime

from Workspace.RA4Analysis.objectSelection import tightPOGMuID , vetoMuID , getLooseMuStage2


################ Options  ##################

AOD=1
getPlotIsOn=0

samples=['TTJets', 'NuGun', 'ZToMuMu']
sample=samples[2]

print sample

steps = ['Step1','Step2','Step3','Step4', 'Step5','Step6']
compList = ['gen','puppi','pf']

plotDir = '/afs/hephy.at/user/n/nrad/www/Puppi/{}/'.format(sample)

##########


getChains(sample)

################## START ####################
invMassHist = ROOT.TH1F('invMassHist','invMassHist',100,0,500)
hist2 = ROOT.TH2F()

#def calResp(chain):

chain=chainDict['Step6']['tChain']

preselection=''

zMass = 91

chain.Draw(">>cL",preselection)
cL = ROOT.gDirectory.Get("cL")
nEvents = cL.GetN()
zBosons=[]
muTMP=[]

for i in range(nEvents):
  if i % 1000==0: print 'eventNumber: ', i
  chain.GetEntry(cL.GetEntry(i))
  nmuCount = int(chain.GetLeaf('nmuCount').GetValue())
  ngoodMuons = chain.GetLeaf('ngoodMuons').GetValue()
  #ngNuMuFromW = chain.GetLeaf('ngNuMuFromW').GetValue()
  #ngNuEFromW = chain.GetLeaf('ngNuEFromW').GetValue()
  #if ngoodMuons: print i, ngoodMuons
  #if ngLep: print i, ngLep  
  if nmuCount>=2:
    muons={}
    for mu in range(int(nmuCount)):
      muons[mu]={}
      muons[mu]['pt'] = chain.GetLeaf('muPt').GetValue(mu)
      muons[mu]['eta'] = chain.GetLeaf('muEta').GetValue(mu)
      muons[mu]['phi'] = chain.GetLeaf('muPhi').GetValue(mu)
      muons[mu]['pdg'] = chain.GetLeaf('muPdg').GetValue(mu)
      muTMP.append({\
                   'event':i,
                   'p':mu,
                   'pt':muons[mu]['pt'],
                   'eta':muons[mu]['eta'],
                   'phi':muons[mu]['phi'],
                   'pdg':muons[mu]['pdg'],
                   })
    if len(muons.keys())>=2:
      for p1 in range(int(nmuCount)):
        for p2 in range(p1+1,int(nmuCount)):
          #print p1, 'vs',  p2, muons
          if muons[p1]['pdg'] == -1*muons[p2]['pdg']:
            invMass = sqrt(2*muons[p1]['pt']*muons[p2]['pt']*(cosh(muons[p1]['eta']-muons[p2]['eta'])-cos(muons[p1]['phi']-muons[p2]['eta'])))
            invMassHist.Fill(invMass)
            #print invMass

            if invMass <= zMass + 10 and invMass >= zMass - 10:
               p1x=muons[p1]['pt']*cos(muons[p1]['phi'])
               p1y=muons[p1]['pt']*sin(muons[p1]['phi'])
               p2x=muons[p2]['pt']*cos(muons[p2]['phi'])
               p2y=muons[p2]['pt']*sin(muons[p2]['phi'])

               zBosons.append({'eventN':i,
                              'mass':invMass,
                              'phi2':muons[p1]['phi']-muons[p2]['phi'],
                              'phi':tan((p2y-p1y)/(p2x-p1x)),
                              'pt2':muons[p1]['pt']*muons[p2]['pt']*cos(muons[p1]['phi']-muons[p2]['phi']),
                              'pt':sqrt((p1x-p2x)**2+(p1y-p2y)**2),
                              })
               #zBosons['mass']=invMass
#              zBosons[i][p]['pt']=muons[p1]['pt']*muons[p2]['pt']*cos(muons[p1]['phi']-muons[p1]['phi'])
               #zBosons.append((i,p,invMass,muons[p1]['phi']-muons[p2]['phi'],muons[p1]['pt']*muons[p2]['pt']*cos(muons[p1]['phi']-muons[p2]['phi'])))

          else: print i, 'muons not paired', muons[p1]['pdg'], muons[p2]['pdg']











'''
  if ngLep>=2:
    #print i, ngLep
    muons={}
    for p in range(int(ngLep)):
      #print p
      gLepPdg = chain.GetLeaf('gLepPdg').GetValue(p)
      gLepDR = chain.GetLeaf('gLepDR').GetValue(p)
      gLepPt = chain.GetLeaf('gLepPt').GetValue(p)
      gLepEta = chain.GetLeaf('gLepEta').GetValue(p)
      gLepInd = chain.GetLeaf('gLepInd').GetValue(p)
      gLepPhi = chain.GetLeaf('gLepPhi').GetValue(p)
      #if abs(gLepPdg) == 13 and gLepPt>20 and abs(gLepEta)<2.1 and ngNuMuFromW==2 and ngNuEFromW==0:
      if abs(gLepPdg)==13:
        muons[p]={}
        muons[p]['pt'] = chain.GetLeaf('gLepPt').GetValue(p)
        muons[p]['eta'] = chain.GetLeaf('gLepEta').GetValue(p)
        muons[p]['phi'] = chain.GetLeaf('gLepPhi').GetValue(p)
        muons[p]['pdg'] = chain.GetLeaf('gLepPdg').GetValue(p)
 
        muTMP.append({\
                     'event':i,
                     'p':p,
                     'pt':muons[p]['pt'],
                     'eta':muons[p]['eta'],
                     'phi':muons[p]['phi'],
                     'pdg':muons[p]['pdg'],
                     })        

    if len(muons.keys())>=2:
      for p1 in range(int(ngLep)):
        for p2 in range(p1+1,int(ngLep)):
          #print p1, 'vs',  p2, muons
          if muons[p1]['pdg'] == -1*muons[p2]['pdg']:
            invMass = sqrt(2*muons[p1]['pt']*muons[p2]['pt']*(cosh(muons[p1]['eta']-muons[p2]['eta'])-cos(muons[p1]['phi']-muons[p2]['eta'])))
            invMassHist.Fill(invMass)
            #print invMass
            
            if invMass <= zMass + 10 and invMass >= zMass - 10:
               p1x=muons[p1]['pt']*cos(muons[p1]['phi'])
               p1y=muons[p1]['pt']*sin(muons[p1]['phi'])
               p2x=muons[p2]['pt']*cos(muons[p2]['phi'])
               p2y=muons[p2]['pt']*sin(muons[p2]['phi'])
          
               zBosons.append({'eventN':i,
                              'mass':invMass,
                              'phi2':muons[p1]['phi']-muons[p2]['phi'],
                              'phi':tan((p2y-p1y)/(p2x-p1x)),
                              'pt2':muons[p1]['pt']*muons[p2]['pt']*cos(muons[p1]['phi']-muons[p2]['phi']),
                              'pt':sqrt((p1x-p2x)**2+(p1y-p2y)**2),
                              })
               #zBosons['mass']=invMass
#              zBosons[i][p]['pt']=muons[p1]['pt']*muons[p2]['pt']*cos(muons[p1]['phi']-muons[p1]['phi'])
               #zBosons.append((i,p,invMass,muons[p1]['phi']-muons[p2]['phi'],muons[p1]['pt']*muons[p2]['pt']*cos(muons[p1]['phi']-muons[p2]['phi'])))
          
          else: print i, 'muons not paired', muons[p1]['pdg'], muons[p2]['pdg']
'''

'''
        hist2.Fill(gLepPt,gLepEta)
        hist1.Fill(gLepPdg)
        if gLepInd>=0 and  gLepDR<0.4:
          k=int(gLepInd)
          muon = getLooseMuStage2(chain,k)
          muon['isTight'] = tightPOGMuID(muon)
          muon['isLoose'] = vetoMuID(muon,0.1)
          if muon['isLoose'] == 1 and abs(1-muon['pt']/gLepPt)<0.9:
              hist1.Fill(gLepEta)
'''


