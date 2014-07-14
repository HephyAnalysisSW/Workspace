#ifndef Workspace_EarlyDataAnalysis_TauTupelizer_H
#define Workspace_EarlyDataAnalysis_TauTupelizer_H

#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/FWLite/interface/Handle.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"

#include "DataFormats/PatCandidates/interface/Tau.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "Workspace/HEPHYCMSSWTools/interface/RecoHelper.h"
#include "Workspace/HEPHYCMSSWTools/interface/MathHelper.h"
#include "Workspace/HEPHYCMSSWTools/interface/ModelParameters.h"

#include "Workspace/HEPHYCMSSWTools/plugins/Tupelizer.h"

#include "TNtuple.h"
#include "TTree.h"
#include <vector>
#include <typeinfo>
#include <string>


class TauTupelizer : public Tupelizer
{
public:
  int prescale(edm::Event & ev, const edm::EventSetup & setup, std::string hlt);

  explicit TauTupelizer ( const edm::ParameterSet & );
  ~TauTupelizer();

  void beginJob(  );
  void beginRun ( edm::Run & iRun, edm::EventSetup const& iSetup );
  void endJob();

  void produce( edm::Event &, const edm::EventSetup &  );

  void addAllVars( );

  edm::ParameterSet params_;
  bool verbose_;

  edm::InputTag input_;
  double ptThreshold_;
  std::vector<edm::ParameterSet> tauIDs_;

  private:
};
#endif
