#ifndef HEPHECommonTools_EventCounter_H
#define HEPHECommonTools_EventCounter_H
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/LuminosityBlock.h"
#include "FWCore/Framework/interface/Run.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
// #include "SimGeneral/HepPDTRecord/interface/ParticleDataTable.h"                                                                               
#include "FWCore/Framework/interface/ESHandle.h"                                                                                               

#include <string>

class EventCounter : public edm::EDProducer {
public:
  explicit EventCounter( const edm::ParameterSet & );
  ~EventCounter() {}

  void produce( edm::Event &, const edm::EventSetup &  ) {++countsByLumi_; ++countsByRun_;}
  void beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&) {countsByLumi_ = 0;}
  void endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);
  void beginRun(edm::Run&, edm::EventSetup const&) {countsByRun_ = 0;}
  void endRun(edm::Run&, edm::EventSetup const&);

private:
  std::string moduleLabel_;
  bool byLumi_;
  bool byRun_;

  unsigned int countsByLumi_;
  unsigned int countsByRun_;
};
#endif
