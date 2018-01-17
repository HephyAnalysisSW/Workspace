// -*- C++ -*-
//
// Package:    TriggerDecisionAnalyzer
// Class:      TriggerDecisionAnalyzer
// 
/**\class TriggerDecisionAnalyzer TriggerDecisionAnalyzer.cc

*/

// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDProducer.h"
//#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
//#include "FWCore/Utilities/interface/StreamID.h"

#include "FWCore/Common/interface/TriggerNames.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/HLTReco/interface/TriggerEvent.h"
//#include "DataFormats/HLTReco/interface/TriggerObject.h"
//#include "DataFormats/HLTReco/interface/TriggerFilterObjectWithRefs.h"
//#include "DataFormats/PatCandidates/interface/TriggerObjectStandAlone.h"
//#include "DataFormats/PatCandidates/interface/PackedTriggerPrescales.h"
//#include "DataFormats/Common/interface/AssociationMap.h"

//#include "DataFormats/PatCandidates/interface/Jet.h"
//#include "DataFormats/PatCandidates/interface/Muon.h"
//#include "DataFormats/PatCandidates/interface/Electron.h"
//#include "DataFormats/VertexReco/interface/Vertex.h"
//#include "DataFormats/RecoCandidate/interface/RecoEcalCandidate.h"

//#include "FWCore/ServiceRegistry/interface/Service.h"
//#include "CommonTools/UtilAlgos/interface/TFileService.h"

//
// class declaration
//

// If the analyzer does not use TFileService, please remove
// the template argument to the base class so the class inherits
// from  edm::one::EDProducer<> and also remove the line from
// constructor "usesResource("TFileService");"
// This will improve performance in multithreaded jobs.

class TriggerDecisionAnalyzer : public edm::one::EDProducer<edm::one::SharedResources>  {
   public:
      explicit TriggerDecisionAnalyzer(const edm::ParameterSet&);
      ~TriggerDecisionAnalyzer();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);
  

   private:
      virtual void beginJob() override;
      virtual void produce(edm::Event&, const edm::EventSetup&); //override;
      virtual void endJob() override;

      // ----------member data ---------------------------

  edm::EDGetTokenT<edm::TriggerResults> trgresultsORIGToken_;
  //edm::EDGetTokenT<edm::TriggerResults> trgresultsHLT2Token_;

  //edm::Service<TFileService> fs;
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
TriggerDecisionAnalyzer::TriggerDecisionAnalyzer(const edm::ParameterSet& iConfig)

{
  trgresultsORIGToken_= consumes<edm::TriggerResults>(edm::InputTag("TriggerResults")); //TriggerResults::HLT
  //trgresultsHLT2Token_= consumes<edm::TriggerResults>(edm::InputTag("TriggerResults::HLT2"));

  //now do what ever initialization is needed
  //   usesResource("TFileService");

  // paths to be saved as branches
  // custom trigger menu paths
  produces<bool>("HLTMu3L1SingleMuOpen").setBranchAlias("HLT_Mu3_L1_SingleMuOpen");
  produces<bool>("HLTMu3PFMET50L1SingleMuOpen").setBranchAlias("HLT_Mu3_PFMET50_L1_SingleMuOpen");
  produces<bool>("HLTMu3PFMET50L1ETM30").setBranchAlias("HLT_Mu3_PFMET50_L1_ETM30");
  produces<bool>("HLTMu3PFMET50PFHT50L1ETM30").setBranchAlias("HLT_Mu3_PFMET50_PFHT50_L1_ETM30");

  // standard trigger paths
  produces<bool>("HLTMu15IsoVVVLPFHT450PFMET50").setBranchAlias("HLT_Mu15_IsoVVVL_PFHT450_PFMET50");
  produces<bool>("HLTPFMET120PFMHT120IDTight").setBranchAlias("HLT_PFMET120_PFMHT120_IDTight");
}


TriggerDecisionAnalyzer::~TriggerDecisionAnalyzer()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}

  
//
// member functions
//

// ------------ method called for each event  ------------
void TriggerDecisionAnalyzer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{

   using namespace edm;
   using namespace reco;
   using namespace std;

   std::unique_ptr<bool> passHLT_Mu3L1SingleMuOpen(new bool(false));
   std::unique_ptr<bool> passHLT_Mu3PFMET50L1SingleMuOpen(new bool(false));
   std::unique_ptr<bool> passHLT_Mu3PFMET50L1ETM30(new bool(false));
   std::unique_ptr<bool> passHLT_Mu3PFMET50PFHT50L1ETM30(new bool(false));
   
   std::unique_ptr<bool> passHLT_Mu15IsoVVVLPFHT450PFMET50(new bool(false));
   std::unique_ptr<bool> passHLT_PFMET120PFMHT120IDTight(new bool(false));

   // Accessing trigger bits:
   // Here we access the decision provided by the HLT (i.e. original trigger step). This works in both RAW, AOD or MINIAOD. 
   edm::Handle<edm::TriggerResults> trigResults;
   iEvent.getByToken(trgresultsORIGToken_, trigResults);
   //iEvent.getByToken(trgresultsHLT2Token_, trigResults);
	 
   if(!trigResults.failedToGet()) {
       int N_Triggers = trigResults->size();
	   //cout << "N_Triggers: " << N_Triggers <<endl;
       const edm::TriggerNames & trigName = iEvent.triggerNames(*trigResults);

       for(int i_Trig = 0; i_Trig < N_Triggers; ++i_Trig) {
	       //cout << "i_Trig: " << i_Trig <<endl;
	       TString TrigPath =trigName.triggerName(i_Trig);
	       //cout << "Trigger path: " << TrigPath <<endl;
               if (trigResults.product()->accept(i_Trig)) {
                   //cout << "Passed path: " << TrigPath << endl;

	               //Special syntax, since the path version can change during data taking
                   if(TrigPath.Index("HLT_Mu3_L1_SingleMuOpen_v") >=0)           *passHLT_Mu3L1SingleMuOpen=true;
                   if(TrigPath.Index("HLT_Mu3_PFMET50_L1_SingleMuOpen_v") >= 0)  *passHLT_Mu3PFMET50L1SingleMuOpen = true;
                   if(TrigPath.Index("HLT_Mu3_PFMET50_L1_ETM30_v") >= 0)         *passHLT_Mu3PFMET50L1ETM30 = true;
                   if(TrigPath.Index("HLT_Mu3_PFMET50_PFHT50_L1_ETM30_v") >= 0)  *passHLT_Mu3PFMET50PFHT50L1ETM30 = true;
                   
                   if(TrigPath.Index("HLT_Mu15_IsoVVVL_PFHT450_PFMET50_v") >= 0) *passHLT_Mu15IsoVVVLPFHT450PFMET50 = true;
                   if(TrigPath.Index("HLT_PFMET120_PFMHT120_IDTight_v") >= 0)    *passHLT_PFMET120PFMHT120IDTight = true; 
	               
           }
       }
   }
       
   iEvent.put(std::move(passHLT_Mu3L1SingleMuOpen),         "HLTMu3L1SingleMuOpen");
   iEvent.put(std::move(passHLT_Mu3PFMET50L1SingleMuOpen),  "HLTMu3PFMET50L1SingleMuOpen");
   iEvent.put(std::move(passHLT_Mu3PFMET50L1ETM30),         "HLTMu3PFMET50L1ETM30");
   iEvent.put(std::move(passHLT_Mu3PFMET50PFHT50L1ETM30),   "HLTMu3PFMET50PFHT50L1ETM30");

   iEvent.put(std::move(passHLT_Mu15IsoVVVLPFHT450PFMET50), "HLTMu15IsoVVVLPFHT450PFMET50");
   iEvent.put(std::move(passHLT_PFMET120PFMHT120IDTight),   "HLTPFMET120PFMHT120IDTight");

}


// ------------ method called once each job just before starting event loop  ------------
void 
TriggerDecisionAnalyzer::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
TriggerDecisionAnalyzer::endJob() 
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
TriggerDecisionAnalyzer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(TriggerDecisionAnalyzer);
