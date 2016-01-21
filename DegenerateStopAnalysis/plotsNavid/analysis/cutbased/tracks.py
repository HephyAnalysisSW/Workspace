from Workspace.DegenerateStopAnalysis.navidTools.NavidTools import *
from Workspace.DegenerateStopAnalysis.cuts import *


import ROOT
import math



hemiList    =   [ 180, 90, 60 ]
hemicos=lambda x: round( math.cos(math.pi- 0.5*(x* math.pi/180)),3)
cosines = {  x:hemicos(x) for x in hemiList }   ### corresponding to 90, 135, 150 degree diff between jet and track


class Tracks(object):
    """
    """
    #def __init__(self, trk="Tracks",trkPt=1,trkEta=2.5 ,pdgs=[13],jetPt=30,jetOpt="",dxy=0.2, dz=0.2, hemi=0, opp="12", mcMatch=False ):
    def __init__(self, **kwargs):
        self.params = { x:kwargs[x] for x in kwargs }
        self.trackCut = "trkcut"

def trackCut(trk="Tracks",trkPt=1,trkEta=2.5 ,pdgs=[13],jetPt=30,jetOpt="",dxy=0.2, dz=0.2, hemi=0, opp="12", mcMatch=False):
    trackCuts = []
    if trk=="Tracks":
        jt= "Jet"
        if dz:
            trackCuts.append("abs(Tracks_dz)<%s"%dz)
        if dxy:
            trackCuts.append("abs(Tracks_dxy)<%s"%dxy)
        if mcMatch:
            x = 0.1
            tracksCuts.append( btw("Tracks_mcMatchPtRatio",1-x , 1+x )) 
            tracksCuts.append( "Tracks_mcMatchDr < 0.1" ) 

    elif trk=="GenTracks":
        jt= "GenJet"
    trackCuts.extend(["abs(%s_pdgId)!=%s"%(trk,pdgId) for pdgId in pdgs])
    trackCuts.append( "%s_pt>%s"%(trk,trkPt)   )
    trackCuts.append( "abs( %s_eta) <%s"%(trk,trkEta) )

    if hemi and opp:
        if not opp in ["12", "1", "All"] : assert False 
        trackCuts.append( "{trk}_CosPhiJet{opp} < {hemicos}".format(trk=trk,opp=opp, hemicos=hemicos(hemi) ) ) 
    if jetOpt.lower()=='veto':  ## veto tracks associated to a jet with pt greater than jetpt
        trackCuts.append( "({trk}_matchedJetDr > 0.4 || {jt}_pt[{trk}_matchedJetIndex] < {jetPt} )".format( jt=jt ,trk=trk, jetPt=jetPt))
    elif jetOpt.lower()=='only':  ## only include tracks associated to a jet with pt greater than jetPt
        trackCuts.append( "({trk}_matchedJetDr >=0.4 || {jt}_pt[{trk}_matchedJetIndex] >= {jetPt} )".format( jt=jt ,trk=trk, jetPt=jetPt))
    #trackCuts.append( "( {%s}_CosPhiJet12 < 0.5  )" )
    return "(%s)"%" && ".join(trackCuts) 


def trkSelName ( d , multip=True):
    if multip:
        name = "n"
    else:
        name = ""

    name += "{trk}".format(**d)
    if d.has_key("trkPt"):
        name += "_Pt{trkPt}".format( **d) 
    name = name.replace(".","p")

    if d.has_key('pdgs') and d['pdgs']:
        pdgs = d['pdgs']
        if pdgs == [13]:
            lepName = "Mu"
        if pdgs == [11]:
            lepName = "El"
        if 11 in pdgs and 13 in pdgs:
            lepName = "Lep"
        name += "_%sVeto"%lepName    

    if d.has_key('jetOpt'):
        if not d['jetOpt']:
            name += ""
            #name += "_allTrks"
        else:
            assert d['jetOpt'].lower() in ['veto','only']
            name += "_{jetOpt}Jet{jetPt}Trks".format( **d) 
    if d.has_key('hemi'):
        if not d['hemi'] or d['hemi']==360:
            name += "".format( **d) 
        else:
            assert d['opp'] in ["12", "1", "All"]
            name += "_Opp{hemi}Jet{opp}".format( **d) 
    #name = "n{trk}_Pt{trkPt}_{jetOpt}Jets_Opp{hemi}Jet{opp}".format( trk=trk, trkPt=trkPt, jetPt=jetPt, jetOpt=jetOpt, hemi=hemi, opp=opp )
    name.format(**d)
    return name


def trkTitle(paramDict, multip=True):
    d= paramDict.copy()
    name = "{trk}"
    if multip:
        name += " Multip"
    if d.has_key("trkPt"):
        name += " w/ trkPt>{trkPt}"

    if d.has_key('pdgs') and d['pdgs']:
        pdgs = d['pdgs']
        if pdgs == [13]:
            lepName = "Mu"
        if pdgs == [11]:
            lepName = "El"
        if 11 in pdgs and 13 in pdgs:
            lepName = "Lep"
        name += " %sVeto"%lepName


    if d.has_key('jetOpt'):
        if not d['jetOpt']:
            name += " AllTracks"
        else:
            assert d['jetOpt'].lower() in ['veto','only']
            d['jetOpt']=d['jetOpt'].upper()
            name += " JetTrks {jetOpt} For JetPt>{jetPt}"
            
    if d.has_key('hemi'):
        if not d['hemi'] or d['hemi']==360:
            name += ""
        else:
            assert d['opp'] in ["12", "1", "All"]
            name += " {hemi}Sector Opp To Jet{opp}"
    #name = "n{trk}_Pt{trkPt}_{jetOpt}Jets_Opp{hemi}Jet{opp}".format( trk=trk, trkPt=trkPt, jetPt=jetPt, jetOpt=jetOpt, hemi=hemi, opp=opp )
    name= name.format(**d)
    name = name.replace(".","p")
    return name

def nTracks(trk="Tracks",trkPt=2.5,trkEta=2.5 ,pdgs=[13],jetPt=30,jetOpt="veto",dxy=0.1, dz=0.1, hemi=0, opp="12",makeName=False, gt=None):
    trackCuts = trackCut(trk=trk,trkPt=trkPt, trkEta=trkEta, pdgs=pdgs, jetPt=jetPt,jetOpt=jetOpt, dxy=dxy, dz=dz, hemi=hemi, opp=opp)
    nTrks = "Sum$(%s)"%trackCuts 
    if gt:
        nTrks = "(%s > %s)"%(nTrks,gt)
    if makeName:
        name = trkSelName({}) 
        return [name, nTrks ]
    else:
        return nTrks


#trkMultipParams = [ 
#                 { 'trk':"Tracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':30,'jetOpt':"",'dxy':0.1, 'dz':0.1, 'hemi':0, 'opp':"12"  } ,  
#                 { 'trk':"GenTracks",'trkPt':2.5,'trkEta':2.5 ,'pdgs':[13],'jetPt':60,'jetOpt':"veto",'dxy':0.1, 'dz':0.1, 'hemi':270, 'opp':"12"  } ,  
#              ] 


trkMultipParams = [
        { 'trk':trkVar,'trkPt':trkPt,'trkEta':2.5 , 'pdgs':pdgs,'jetPt':jetPt,'jetOpt':jetOpt,'dxy':0.1, 'dz':0.1, 'hemi':hemi, 'opp':opp  } 
            for trkVar in ["Tracks","GenTracks"]
            for trkPt in [1,1.5,2,2.5,3,3.5]
            for pdgs in [[13],[11],[13,11],[] ] 
            for jetPt in [30,45,60]
            for jetOpt in ['veto','only','']  
            for hemi in [270,180,90]
            for opp in ['1','12','All']
            ]
trkMultipParams.extend([
        { 'trk':trkVar,'trkPt':trkPt,'trkEta':2.5 ,'pdgs':pdgs,'jetPt':jetPt,'jetOpt':jetOpt,'dxy':0.1, 'dz':0.1, 'hemi':hemi, 'opp':opp  } 
            for trkVar in ["Tracks","GenTracks"]
            for trkPt in [1,1.5,2,2.5,3,3.5]
            for pdgs in [[13],[11],[13,11],[] ] 
            for jetPt in [30,45,60]
            for jetOpt in ['veto','only','']  
            for hemi in ['']
            for opp in ['']
           ])


#unique= set()
#for d in trkMultipParams:
#    d['pdgs'] = str(d['pdgs'])
#    unique.add( tuple( d.iteritems()) ) 


 

sr1TrkCuts= {}
for trkCut in trkMultipParams: 
    #print trkCut
    trkCutName = trkSelName(trkCut)
    sr1TrkCuts[trkCutName]={}
    sr1TrkCuts[trkCutName]['bin'] = [30,0,60]
    if "_JetTrks" in trkCutName:
        sr1TrkCuts[trkCutName]['bin'] = [60,0,60]
    if "_onlyJetTrks" in trkCutName:
        sr1TrkCuts[trkCutName]['bin'] = [60,0,60]
    if any([ x in trkCutName for x in  ["_Opp270","_Opp180","_Opp90"]]):
        sr1TrkCuts[trkCutName]['bin'] = [30,0,30]


    maxNTrk = sr1TrkCuts[trkCutName]['bin'][2]
    sr1TrkCuts[trkCutName]['params']=trkCut
    sr1TrkCuts[trkCutName]['var'] = nTracks(**trkCut)
    sr1TrkCuts[trkCutName]['cut'] = CutClass( trkCutName, 
                                    [ [ trkCutName+" $>$ %s"%x, nTracks(gt=x, **trkCut)   ] for x in range(maxNTrk) ]                        
                        ,baseCut = sr1Loose 
                        )  






trackPlotDict =\
      {
        "nTrks_jetPt30":            {'var':nTracks(jetPt=30)                            ,"bins":[30,0,60]          ,"decor":{"title":"Track Count  Outside Jets Above 30"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nTrks_jetPt45":            {'var':nTracks(jetPt=45)                            ,"bins":[30,0,60]          ,"decor":{"title":"Track Count  Outside Jets Above 45"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nTrks_jetPt60":            {'var':nTracks(jetPt=60)                            ,"bins":[30,0,60]          ,"decor":{"title":"Track Count  Outside Jets Above 60"  ,"x":"Track Multiplicity","y":"nEvents"   }  },

        "nGenTrks_jetPt30":         {'var':nTracks(trk="GenTracks",jetPt=30)            ,"bins":[30,0,60]          ,"decor":{"title":"GenTrack Count  Outside Jets Above 30"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nGenTrks_jetPt45":         {'var':nTracks(trk="GenTracks",jetPt=45)            ,"bins":[30,0,60]          ,"decor":{"title":"GenTrack Count  Outside Jets Above 45"  ,"x":"Track Multiplicity","y":"nEvents"   }  },
        "nGenTrks_jetPt60":         {'var':nTracks(trk="GenTracks",jetPt=60)            ,"bins":[30,0,60]          ,"decor":{"title":"GenTrack Count  Outside Jets Above 60"  ,"x":"Track Multiplicity","y":"nEvents"   }  },

      }


trkPlotsParams=\
    {



    }

binDict={
            "pt":[100,0,100],
            "eta":[20,-3,3],
            "pdgId":[500,-250,250],
            "charge":[3,0,3],
            "dxy":[50,-0.5,0.5],
            "dz":[50,-0.5,0.5],
            "dxyError":[100,0,1],
             "dzError":[100,0,1],
             "numberOfPixleHits":[10,0,10],
             "numberOfHits":[20,0,20],
             "trackHighPurity":[2,0,2],
             "mcMatchId": [10,-2,3],
         }


trackQuantPlotDict={}
for trkCut in trkMultipParams:
    trkCutName= trkSelName(trkCut,multip=False)
    varList = ["pt","eta","pdgId","charge"]
    if trkCut['trk']=="Tracks":
        varList.extend(["dxy","dz","dxyError", "dzError", "numberOfPixleHits", "numberOfHits", "trackHighPurity", "mcMatchId" ]) 
        

    for var in varList:
        varName = trkCut['trk']+"_"+var
        plotName = var+"_"+trkCutName
        cutString = trackCut(**trkCut)
        trackQuantPlotDict[plotName]={}
        trackQuantPlotDict[plotName]['cut']=cutString
        trackQuantPlotDict[plotName]['var']=varName
        trackQuantPlotDict[plotName]['name']=plotName
        trackQuantPlotDict[plotName]['bins']=binDict[var]
        trackQuantPlotDict[plotName]['decor']={
                                'title':var+ " " + trkTitle(trkCut),
                                'x':var,
                                'y':'nEvents',
                                'log':[0,1,0],
                                }

quantPlots=Plots(**trackQuantPlotDict)


trackMultipPlotDict={}
for trkCut in trkMultipParams:
    trkCutName= trkSelName(trkCut)

    if trkCutName in trackMultipPlotDict:
        print "-------"*6
        print trkCut
        print trkCutName
    trackMultipPlotDict[trkCutName]={}
    trackMultipPlotDict[trkCutName]['var']=nTracks(**trkCut)
    trackMultipPlotDict[trkCutName]['name']=trkCutName
    if "nGenTracks" in trkCutName:
        trackMultipPlotDict[trkCutName]['bins']=[40,0,40]
    else:
        trackMultipPlotDict[trkCutName]['bins']=[30,0,30]
    trackMultipPlotDict[trkCutName]['decor']={
                            'title':trkTitle(trkCut),
                            'x':"Track Multiplicity",
                            'y':'nEvents',
                            'log':[0,1,0],
                            }

multipPlots=Plots(**trackMultipPlotDict)







