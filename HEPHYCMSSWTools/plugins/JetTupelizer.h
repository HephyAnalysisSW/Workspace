#ifndef Workspace_EarlyDataAnalysis_JetTupelizer_H
#define Workspace_EarlyDataAnalysis_JetTupelizer_H

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/FWLite/interface/Handle.h"
#include "DataFormats/JetReco/interface/CaloJet.h"
#include "DataFormats/JetReco/interface/JetID.h"
#include "DataFormats/JetReco/interface/PFJet.h"

#include "DataFormats/PatCandidates/interface/Jet.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "PhysicsTools/SelectorUtils/interface/JetIDSelectionFunctor.h"

#include "Workspace/HEPHYCMSSWTools/interface/RecoHelper.h"
#include "Workspace/HEPHYCMSSWTools/interface/MathHelper.h"
#include "Workspace/HEPHYCMSSWTools/interface/ModelParameters.h"

#include "Workspace/HEPHYCMSSWTools/plugins/Tupelizer.h"

#include "TNtuple.h"
#include "TTree.h"
#include <vector>
#include <typeinfo>
#include <string>


class JetTupelizer : public Tupelizer
{
public:
  explicit JetTupelizer ( const edm::ParameterSet & );
  ~JetTupelizer();

  void beginJob(  );
  void beginRun ( edm::Run & iRun, edm::EventSetup const& iSetup );
  void endJob();

  void produce( edm::Event &, const edm::EventSetup &  );

  void addAllVars( );

  edm::ParameterSet params_;
  bool verbose_;

  edm::InputTag input_;

  double ptThreshold_;

  std::string btag_;
  edm::InputTag puJetIdCutBased_;
  edm::InputTag puJetIdFull53X_;
  edm::InputTag puJetIdMET53X_;

  private:

};
#endif
