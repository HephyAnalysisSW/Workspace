#ifndef Workspace_EarlyDataAnalysis_TriggerTupelizer_H
#define Workspace_EarlyDataAnalysis_TriggerTupelizer_H

#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/FWLite/interface/Handle.h"
#include "DataFormats/Math/interface/Point3D.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"

#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/Scalers/interface/DcsStatus.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"

//#include "SimGeneral/HepPDTRecord/interface/ParticleDataTable.h"

#include "Workspace/HEPHYCMSSWTools/interface/ModelParameters.h"

#include "Workspace/HEPHYCMSSWTools/plugins/Tupelizer.h"

#include "TNtuple.h"
#include "TTree.h"
#include <vector>
#include <typeinfo>
#include <string>


class TriggerTupelizer : public Tupelizer
{
public:
  int prescale(edm::Event & ev, const edm::EventSetup & setup, std::string hlt);

  explicit TriggerTupelizer ( const edm::ParameterSet & );
  ~TriggerTupelizer();

  void beginJob(  );
  void beginRun ( edm::Run & iRun, edm::EventSetup const& iSetup );
  void endJob();

  void produce( edm::Event &, const edm::EventSetup &  );

  edm::ParameterSet params_;
  bool verbose_;

  edm::InputTag triggerCollection_;

  private:
  bool hlt_initialized_;
  std::vector<std::string> HLT_names_;
  HLTConfigProvider hltConfig_;

  bool addTriggerInfo_;
  std::vector<std::string> triggersToMonitor_, trigNames_, prescNames_;

};
#endif
