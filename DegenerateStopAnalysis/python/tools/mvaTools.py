# mvaTools.py
# Gets MVA trees

#mvaId   = getattr(args, "mvaId" )
#bdtcut  = getattr(args, "bdtcut")
#
#mva_params =[ mvaId, bdtcut ] 
#
#if any( mva_params):
#    if not all( mva_params):
#        raise Exception("MVA Parameters set partially! need both bdtCut and mvaId %s"%mva_params)
#    isMVA = True
#else:
#    isMVA = False

mva_friendtree_map  = [
                        ["nrad01", "vghete02"],
                        #["step1", "step2_2017_v0/mvaSet_30"],
                        #["step1", "step2_LipSync_2017_v0/mvaSet_30/"],
                        #["step1", "step2_Lip_2017_v0/mvaSet_30/"],
                        #["step1", "step2_mvaLip_job_2017-v2_0_1_Hephy_pre_gt0lep/mvaSet_30"], #loose presel
                        #["step1", "step2_mvaLip_job_2017-v2_0_1_Hephy_Zinv_pre_gt0lep/mvaSet_300"],  #Zinv 
                        #["step1", "step2_mvaLip_job_2017-v2_0_1_Hephy_pre_gt0lep_loose/mvaSet_30"], #loose indices 
                        #["step1",  "step2_mvaLip_job_2017-v2_2_0_LipWeights_pre_gt0lep_loose/mvaSet_30"], #loose indices 8025
                        #["step1",  "step2_mvaLip_job_2017-v2_2_0_LipWeights_pre_none_loose/mvaSet_30"], # no presel
                        ["step1",  "step2_mvaLip_job_2017-v2_2_0_1_LipWeights_pre_none_loose/mvaSet_30"], # loose fix
                      ]

def getMVATrainWeightCorr(sample, mvaIdIndex, train_var="mva_trainingEvent"):
   if sample.isData:
       return
  
   presel_events  = sample.tree.Draw("(1)", "mva_preselectedEvent[{mvaIdIndex}]".format(mvaIdIndex = mvaIdIndex),'goff')
   
   if not presel_events:
       return 
   
   presel_not_trained_events = sample.tree.Draw("(1)", "(!mva_trainingEvent[{mvaIdIndex}])*(mva_preselectedEvent[{mvaIdIndex}])".format(mvaIdIndex = mvaIdIndex), 'goff')
   if int(presel_not_trained_events)==int(presel_events):
       return 
   lumiWeightCorr =  float(presel_events)/ presel_not_trained_events
   #sample.weight = "( ({mvaLumiCorFactor:0.4f}* (!mva_trainingEvent[{mvaIdIndex}])*(mva_preselectedEvent[{mvaIdIndex}]))  )".format(mvaLumiCorFactor = lumiWeightCorr , mvaIdIndex = mvaIdIndex)
   sample.weight = "( ({mvaLumiCorFactor:0.4f}* (!mva_trainingEvent[{mvaIdIndex}])*(mva_preselectedEvent[{mvaIdIndex}])) +(!mva_preselectedEvent[{mvaIdIndex}])  )".format(mvaLumiCorFactor = lumiWeightCorr , mvaIdIndex = mvaIdIndex)
   print sample.name, sample.weight
   return 

def getMVATrees(samples, mvaIdIndex, mva_friendtree_map = mva_friendtree_map):
   for s in samples.keys():
      print "***"
      print "Adding Friend Trees for :", samples[s].name
      samples[s].addFriendTrees("Events", mva_friendtree_map, check_nevents=False, alias='step2')
      print samples[s].tree.GetListOfFriends().ls()
      getMVATrainWeightCorr(samples[s], mvaIdIndex)
