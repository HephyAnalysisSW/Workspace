from Workspace.DegenerateStopAnalysis.cmgPostProcessing.btagEfficiency import btagEfficiency

#execfile("btagEfficiency.py")
#btagEff = btagEfficiency( )

#readTree, splitTree, saveTree , processJets_rtuple  , params = ret

#splitTree.GetEntry(100)
saveTree, processJets_rtuple  = processJets(args, readTree, splitTree, saveTree, params )


effFile          =   params['beff']['effFile']
#effFile         =   params['beff']['effFile'] 
sfFile           =   params['beff']['sfFile']
sfFile_FastSim   =   params['beff']['sfFile_FastSim']

btagEff          =   params['beff']['btagEff']








jObj = processJets_rtuple.jetObj

jetList = processJets_rtuple.basJetList
bJetList = processJets_rtuple.bJetList
bSoftJetList = processJets_rtuple.bSoftJetList
bHardJetList = processJets_rtuple.bHardJetList
softJetList  = processJets_rtuple.softJetList
hardJetList  = processJets_rtuple.hardJetList

nonBJetList     = [x for x in jetList if x not in bJetList]
nonBSoftJetList = [x for x in jetList if x not in bSoftJetList]
nonBHardJetList = [x for x in jetList if x not in bHardJetList]



for i in processJets_rtuple.basJetList:
    btagEff.addBTagEffToJet(jObj,i)
setattr(readTree, "%s_%s" % (jObj.obj, 'beff'),jObj.beff)  ## in order for th getObjDict to work with beff



varList = ['pt', 'eta', 'phi', 'mass', 'hadronFlavour', 'beff' ]

nonBJetList = [x for x in jetList if x not in bJetList]

jets     = jObj.getObjDictList(  varList , jetList )
softJets = jObj.getObjDictList(  varList , softJetList ) 
hardJets = jObj.getObjDictList(  varList , hardJetList ) 

bJets     = jObj.getObjDictList(  varList , bJetList )
bSoftJets = jObj.getObjDictList(  varList , bSoftJetList )
bHardJets = jObj.getObjDictList(  varList , bHardJetList )

nonBJets     = jObj.getObjDictList(  varList , nonBJetList )
nonBSoftJets = jObj.getObjDictList(  varList , nonBSoftJetList )
nonBHardJets = jObj.getObjDictList(  varList , nonBHardJetList )


#btagEff.getBTagSF_1a( "SF",bHardJetList, nonBJetList , j )




btagEff.getWeightDict_1b([jObj.beff[x]['MC'] for x in jObj.beff] , 3)



btag_nonbtag_list_pairs = {
                        'BTag'  : ( bJetList, nonBJetList ),
                        'SBTag' : ( bSoftJetList , nonBSoftJetList ),
                        'HBTag' : ( bHardJetList , nonBHardJetList ),
                    }

btag_nonbtag_pairs = {
                        'BTag'  : ( bJets, nonBJets , jets),
                        'SBTag' : ( bSoftJets , nonBSoftJets , softJets),
                        'HBTag' : ( bHardJets , nonBHardJets , hardJets),
                     }

maxMultBTagWeight = 2
for bTagName, bJets_nonBJets_jets in btag_nonbtag_pairs.iteritems():
    bj , nonbj , j = bJets_nonBJets_jets
    for var in btagEff.btagWeightNames:
        if var!='MC':
            setattr(readTree, "weight1a%s_%s"%(bTagName, var), btagEff.getBTagSF_1a( var, bj, nonbj))
            multiBTagWeightDict = btagEff.getWeightDict_1b( [  jj['beff'][var] for jj in j  ] , maxMultBTagWeight)
            for nB in range(maxMultBTagWeight+1):
                setattr(readTree, "weight%s%s_%s"%(bTagName, nB, var), multiBTagWeightDict[nB])
            setattr(readTree, "weight%s%sp_%s"%(bTagName, nB, var), 1- sum( multiBTagWeightDict.values() )   )  # more than maxMultiBTag



#for j in jets:
#    btagEff.addBTagEffToJet(j)
#for var in btagEff.btagWeightNames:
#    if var!='MC':
#        btagEff.getBTagSF_1a( var, bJets, nonBJets ) 
#        btagEff.getWeightDict_1b([jObj.beff[x]['MC'] for x in jObj.beff] , 3)
#        #setattr(s, 'reweightBTag_'+var, btagEff.getBTagSF_1a( var, bJets, nonBJets ) )
