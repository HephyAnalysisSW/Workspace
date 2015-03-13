#ifndef Workspace_EarlyDataAnalysis_PFCandTupelizer_H
#define Workspace_EarlyDataAnalysis_PFCandTupelizer_H

#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/FWLite/interface/Handle.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "Workspace/HEPHYCMSSWTools/plugins/Tupelizer.h"

#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"

#include <vector>
#include <string>


class PFCandTupelizer : public Tupelizer
{
public:

  explicit PFCandTupelizer ( const edm::ParameterSet & );
  ~PFCandTupelizer();

  void beginJob(  );
  void beginRun ( edm::Run & iRun, edm::EventSetup const& iSetup );
  void endJob();

  void produce( edm::Event &, const edm::EventSetup &  );

  void addAllVars( );

  private:
  edm::EDGetTokenT<std::vector<reco::PFCandidate> > pflowToken_;
  bool fillIsolatedChargedHadrons_;
};
#endif

