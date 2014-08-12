import FWCore.ParameterSet.Config as cms

lheAnalysis = cms.EDAnalyzer ("LheAnalysis",
                              
    # LHE sample 
     LheSample=cms.string("T2DegenerateStop"),
     
    # input tag for LHEEventProduct
    InputTagLHEEventProduct=cms.InputTag("source")
    
                          
        
) 


