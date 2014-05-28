#ifndef Workspace_EarlyDataAnalysis_SUSYTupelizer_H
#define Workspace_EarlyDataAnalysis_SUSYTupelizer_H

#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/FWLite/interface/Handle.h"
#include "DataFormats/JetReco/interface/CaloJet.h"
#include "DataFormats/JetReco/interface/JetID.h"
#include "DataFormats/JetReco/interface/PFJet.h"
#include "DataFormats/Math/interface/Point3D.h"
#include "DataFormats/METReco/interface/CaloMET.h"
#include "DataFormats/MuonReco/interface/MuonFwd.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"

#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/MHT.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Isolation.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/Scalers/interface/DcsStatus.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"

#include "MagneticField/Engine/interface/MagneticField.h"
#include "MagneticField/Records/interface/IdealMagneticFieldRecord.h"

#include "PhysicsTools/SelectorUtils/interface/JetIDSelectionFunctor.h"
#include "PhysicsTools/SelectorUtils/interface/SimpleCutBasedElectronIDSelectionFunctor.h"

#include "SimGeneral/HepPDTRecord/interface/ParticleDataTable.h"

#include "Workspace/HEPHYCMSSWTools/interface/RecoHelper.h"
#include "Workspace/HEPHYCMSSWTools/interface/MathHelper.h"
#include "Workspace/HEPHYCMSSWTools/interface/ModelParameters.h"

#include "Workspace/HEPHYCMSSWTools/plugins/Tupelizer.h"

#include "TNtuple.h"
#include "TTree.h"
#include <vector>
#include <typeinfo>
#include <string>


class SUSYTupelizer : public Tupelizer
{
public:
  int prescale(edm::Event & ev, const edm::EventSetup & setup, std::string hlt);

  explicit SUSYTupelizer ( const edm::ParameterSet & );
  ~SUSYTupelizer();

  void beginJob(  );
  void beginRun ( edm::Run & iRun, edm::EventSetup const& iSetup );
  void endJob();

  void produce( edm::Event &, const edm::EventSetup &  );

  void addAllVars( );

  edm::ParameterSet params_;
  bool verbose_;

  edm::InputTag triggerCollection_;
  edm::InputTag patJets_;
  edm::InputTag patMuons_;
  edm::InputTag patElectrons_;
  edm::InputTag patTaus_;
  edm::InputTag vertices_;

  double lowLeptonPtThreshold_;
  double softJetPtThreshold_;

  double muonPFRelIsoDeltaBeta_;
  bool   elePFRelIsoAreaCorrected_;
  edm::InputTag   eleRho_;
  std::string btag_;
  bool hasL1Trigger_;
  edm::InputTag puJetIdCutBased_;
  edm::InputTag puJetIdFull53X_;
  edm::InputTag puJetIdMET53X_;

  private:
  bool hlt_initialized_;
  std::vector<std::string> HLT_names_;
  HLTConfigProvider hltConfig_;
  ModelParameters modelParameters_;
//  std::string moduleLabel_;

  bool addTriggerInfo_;
  std::vector<std::string> triggersToMonitor_, trigNames_, prescNames_, metsToMonitor_;
  bool addMetUncertaintyInfo_;
//  bool addFullBTagInfo_;
  bool addJetVector_;
  bool addMuonVector_;
  bool addEleVector_;
  bool addFullTauInfo_;
//  bool addGeneratorInfo_;
  bool addMSugraOSETInfo_;
  bool addPDFWeights_;

};
#endif
