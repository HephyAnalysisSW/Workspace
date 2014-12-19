#ifndef HEPHECommonTools_multMETCorrInfoWriter_H
#define HEPHECommonTools_multMETCorrInfoWriter_H
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/LuminosityBlock.h"
#include "FWCore/Framework/interface/Run.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
// #include "SimGeneral/HepPDTRecord/interface/ParticleDataTable.h"                                                                               
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"

#include <string>
#include <vector>
#include <TProfile.h>
#include <TH2F.h>

class multMETCorrInfoWriter : public edm::EDAnalyzer {
public:
  multMETCorrInfoWriter( const edm::ParameterSet & );

private:
  edm::EDGetTokenT<std::vector<reco::PFCandidate> > pflowToken_;

  void analyze( const edm::Event& , const edm::EventSetup& );
  edm::InputTag vertices_;
  std::string moduleLabel_;
  std::vector<edm::ParameterSet> cfgCorrParameters_;
  std::vector<TProfile* > profile_x_ , profile_y_;
  std::vector<TH2F* > occupancy_ , energy_, pt_;
  std::vector<TH1F* > variable_;

  std::vector<double> etaMin_, etaMax_, MEx_, MEy_, sumPt_;
  std::vector<int> type_, varType_, nbins_, counts_, etaNBins_;


};

#endif


