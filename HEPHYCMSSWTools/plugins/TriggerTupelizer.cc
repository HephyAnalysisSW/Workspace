#include "FWCore/Framework/interface/MakerMacros.h"
#include "Workspace/HEPHYCMSSWTools/plugins/TriggerTupelizer.h"
#include "Workspace/HEPHYCMSSWTools/interface/EdmHelper.h"
#include <SimDataFormats/GeneratorProducts/interface/HepMCProduct.h>
#include <SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h>
#include "L1Trigger/GlobalTriggerAnalyzer/interface/L1GtUtils.h"
#include "CondFormats/L1TObjects/interface/L1GtTriggerMenu.h"
#include "CondFormats/DataRecord/interface/L1GtTriggerMenuRcd.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerReadoutSetupFwd.h"
#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerReadoutSetup.h"
#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerReadoutRecord.h"
#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerObjectMapRecord.h"
#include "HLTrigger/HLTfilters/interface/HLTLevel1GTSeed.h"
//#include "DataFormats/HLTReco/interface/TriggerEvent.h"
//#include "DataFormats/PatCandidates/interface/TriggerEvent.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"

using namespace std;

namespace {
  string prefix ("[TriggerTupelizer] ");
}

TriggerTupelizer::~TriggerTupelizer() {}

TriggerTupelizer::TriggerTupelizer( const edm::ParameterSet & pset):
  Tupelizer(pset),
  params_ ( pset ),
  verbose_ ( pset.getUntrackedParameter< bool >("verbose")),
  triggerCollection_ ( pset.getUntrackedParameter< edm::InputTag >("triggerCollection") ),
  isValidHltConfig_(false),
  hltPrescale_(pset, consumesCollector(), *this),
  hltPrescaleSet_(-1),
  hltConfig_(NULL),
  triggersToMonitor_(pset.getUntrackedParameter<std::vector<std::string> > ("triggersToMonitor") ),
  addL1Prescales_(pset.getUntrackedParameter<bool> ("addL1Prescales") )
{
  for (std::vector<std::string>::iterator s = triggersToMonitor_.begin(); s != triggersToMonitor_.end(); s++) {
    cout<<prefix<<"Monitoring the following trigger:"<<*s<<endl;
    std::string trigName = *s;
    std::string::size_type k = 0;
    while((k=trigName.find('_',k))!=trigName.npos) {
      trigName.erase(k, 1);
    }
    addVar(trigName+"/I");
    trigNames_.push_back(trigName);
    if (addL1Prescales_) {
      std::string prescName = trigName;
      prescName.replace(0, 3, "pre");
      addVar(prescName+"/I");
      prescNames_.push_back(prescName);
    }
  }
}


void TriggerTupelizer::beginJob ( )
{
  cout << "[TriggerTupelizer] starting ... " << endl;
  hlt_initialized_ = false;
}

void TriggerTupelizer::endJob()
{
  cout << endl;
  cout << "[TriggerTupelizer] shutting down ... " << endl;
}

void TriggerTupelizer::beginRun ( edm::Run & iRun, edm::EventSetup const & iSetup )
{
  bool changed(true);

  bool isConfigChanged(false);
  isValidHltConfig_ =
    hltPrescale_.init(iRun, iSetup, "HLT", isConfigChanged);
  // if (hltConfig_.init(iRun,iSetup,triggerCollection_.label(),changed)) {
  // } else {
  if ( !isValidHltConfig_ ) {
    edm::LogError(prefix) << " HLT config extraction failure with process name " << triggerCollection_;
  }
}

int TriggerTupelizer::prescale(edm::Event & ev, const edm::EventSetup & setup, std::string hlt) {
// return prod(hltConfig_.prescaleValues( ev, setup, hlt.c_str()));
  return hltConfig_->prescaleValue( hltPrescaleSet_, hlt);
}


void TriggerTupelizer::produce( edm::Event & ev, const edm::EventSetup & setup) {
  ev_ = &ev;
//  bool isData (ev.eventAuxiliary().isRealData());
  
//  //HLT - Triggers
//  edm::Handle<trigger::TriggerEvent> triggerEvent;
//  ev.getByLabel(triggerLabel_, triggerEvent);
//  if (not triggerEvent.isValid()) {
//    std::cout << "HLT Results with label: " << triggerLabel_
//              << " not found" << std::endl;
//    }
//  cout<<triggerCollection_.label().c_str()<<endl;

  hltPrescaleSet_ = hltPrescale_.prescaleSet(ev,setup);
  hltConfig_ = &hltPrescale_.hltConfigProvider();

  edm::Handle<edm::TriggerResults> HLTR;
//  edm::InputTag HLTTag = edm::InputTag(triggerLabel_, "", triggerCollection_.label().c_str());
  ev.getByLabel(triggerCollection_, HLTR);
//  cout << "Init HLT info valid? " <<boolalpha<< HLTR.isValid()<<endl;
  if (HLTR.isValid()) {
    edm::TriggerNames triggerNames = ev.triggerNames(*HLTR);
    HLT_names_ = triggerNames.triggerNames();
    if (! this->hlt_initialized_ ) {
      cout<<"HLT: "<<triggerCollection_.label().c_str()<<endl;
      for (unsigned i=0;i<HLT_names_.size();i++) {
        cout<<HLT_names_[i]<<endl;
      }
      TriggerTupelizer::hlt_initialized_ = true;
    }
  }
  for (unsigned i=0; i<HLT_names_.size(); ++i){
    for (unsigned j = 0; j< triggersToMonitor_.size(); j++) {
      if (std::strstr(HLT_names_[i].c_str(), (triggersToMonitor_[j]+"_v").c_str())) {
        put(trigNames_[j], HLTR->accept(i));
        if (addL1Prescales_) put(prescNames_[j], prescale( ev, setup, HLT_names_[i].c_str()));
      };
    }
  }

}

DEFINE_FWK_MODULE(TriggerTupelizer);
