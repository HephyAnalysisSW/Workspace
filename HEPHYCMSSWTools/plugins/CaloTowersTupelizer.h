#ifndef Workspace_EarlyDataAnalysis_CaloTowersTupelizer_H
#define Workspace_EarlyDataAnalysis_CaloTowersTupelizer_H

#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/FWLite/interface/Handle.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "Workspace/HEPHYCMSSWTools/plugins/Tupelizer.h"

#include "TNtuple.h"
#include "TTree.h"
#include <vector>
#include <typeinfo>
#include <string>


class CaloTowersTupelizer : public Tupelizer
{
public:

  explicit CaloTowersTupelizer ( const edm::ParameterSet & );
  ~CaloTowersTupelizer();

  void beginJob(  );
  void beginRun ( edm::Run & iRun, edm::EventSetup const& iSetup );
  void endJob();

  void produce( edm::Event &, const edm::EventSetup &  );

  void addAllVars( );

  private:
  edm::ParameterSet params_;
  bool verbose_;
  edm::InputTag hfCaloTowers_;

};
#endif

