#include "Workspace/HEPHYCommonTools/plugins/EventCounter.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include <iostream>

using namespace std;

EventCounter::EventCounter ( const edm::ParameterSet & pset ) :   
  moduleLabel_(pset.getParameter<std::string>("@module_label")),
  byLumi_(pset.getUntrackedParameter<bool>("byLumi",true)),
  byRun_(pset.getUntrackedParameter<bool>("byRun",true)),
  countsByLumi_(0), countsByRun_(0) {

//   std::cout << "Initialised EventCounter for label " << moduleLabel_ << std::endl;

  if ( byLumi_ )  produces<unsigned int,edm::InLumi>("lumiCounts").setBranchAlias(moduleLabel_+"_lumiCounts");
  if ( byRun_ )  produces<unsigned int,edm::InRun>("runCounts").setBranchAlias(moduleLabel_+"_runCounts");

//   std::cout << "Lumi / run options = " << byLumi_ << " " << byRun_ << std::endl;

}

void EventCounter::endLuminosityBlock (edm::LuminosityBlock& lumiBlock, edm::EventSetup const& setup) 
{
  if ( byLumi_ ) {
//     std::cout << "Writing lumi counts for " << moduleLabel_ << " : " << countsByLumi_ << std::endl;
    std::auto_ptr<unsigned int> counts(new unsigned int);
    *counts = countsByLumi_;
    lumiBlock.put<unsigned int>(counts, "lumiCounts");
    countsByLumi_ = 0;
  }
}

void EventCounter::endRun (edm::Run& run, edm::EventSetup const& setup)
{
  if ( byRun_ ) {
//     std::cout << "Writing run counts for " << moduleLabel_ << " : " << countsByRun_ << std::endl;
    std::auto_ptr<unsigned int> counts(new unsigned int);
    *counts = countsByRun_;
    run.put<unsigned int>(counts, "runCounts");
    countsByRun_ = 0;
  }
}


//define this as a plug-in
#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(EventCounter);
