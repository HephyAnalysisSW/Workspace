#ifndef Workspace_EarlyDataAnalysis_ElectronTupelizer_H
#define Workspace_EarlyDataAnalysis_ElectronTupelizer_H

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/FWLite/interface/Handle.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"

#include "DataFormats/PatCandidates/interface/Electron.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "Workspace/HEPHYCMSSWTools/interface/RecoHelper.h"
#include "Workspace/HEPHYCMSSWTools/interface/MathHelper.h"

#include "Workspace/HEPHYCMSSWTools/plugins/Tupelizer.h"

#include "TNtuple.h"
#include "TTree.h"
#include <vector>
#include <typeinfo>
#include <string>


class ElectronTupelizer : public Tupelizer
{
public:
  explicit ElectronTupelizer ( const edm::ParameterSet & );
  ~ElectronTupelizer();

  void beginJob(  );
  void beginRun ( edm::Run & iRun, edm::EventSetup const& iSetup );
  void endJob();

  void produce( edm::Event &, const edm::EventSetup &  );

  void addAllVars( );

  edm::ParameterSet params_;
  bool verbose_;

  edm::InputTag input_;
  double ptThreshold_;
  edm::InputTag vertices_;

  bool   elePFRelIsoAreaCorrected_;
  edm::InputTag   eleRho_;

  private:
};
#endif
