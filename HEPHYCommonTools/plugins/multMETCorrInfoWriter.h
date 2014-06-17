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

class multMETCorrInfoWriter : public edm::EDAnalyzer {
public:
  multMETCorrInfoWriter( const edm::ParameterSet & );

private:
//  edm::EDGetTokenT<std::vector<reco::PFCandidate> > pflowToken_;
  std::string moduleLabel_;
  edm::InputTag pflowLabel_;
  std::vector<edm::ParameterSet> cfgCorrParameters_;
  void analyze( const edm::Event& , const edm::EventSetup& );

  std::vector<TProfile* > profile_x_ , profile_y_;

  std::vector<double> etaMin_, etaMax_, MEx_, MEy_;
  std::vector<int> type_, nbins_, counts_;


};

#endif


