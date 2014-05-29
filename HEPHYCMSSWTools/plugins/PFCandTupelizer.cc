#include "Workspace/HEPHYCMSSWTools/plugins/PFCandTupelizer.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"

using namespace std;

namespace {
  string prefix ("[PFCandTupelizer] ");
}

PFCandTupelizer::~PFCandTupelizer() {}

PFCandTupelizer::PFCandTupelizer( const edm::ParameterSet & pset):
  Tupelizer(pset),
  pflowToken_  (consumes<std::vector<reco::PFCandidate> >(pset.getParameter<edm::InputTag>("srcPFlow")))

{
  addAllVars();
}


void PFCandTupelizer::beginJob ( )
{
  cout << "[PFCandTupelizer] starting ... " << endl;
}

void PFCandTupelizer::endJob()
{
  cout << endl;
  cout << "[PFCandTupelizer] shutting down ... " << endl;
}

void PFCandTupelizer::beginRun ( edm::Run & iRun, edm::EventSetup const & iSetup )
{
}


void PFCandTupelizer::produce( edm::Event & ev, const edm::EventSetup & setup) {
  ev_ = &ev;//Needed for base class
  int nCand(0);
  std::vector<float> c_pt, c_eta, c_phi,c_energy;
  std::vector<int> c_id, c_charge;

  edm::Handle<std::vector<reco::PFCandidate> > particleFlow;
  ev.getByToken(pflowToken_, particleFlow);
  for (unsigned i = 0; i < particleFlow->size(); ++i) {
    const reco::PFCandidate& c = particleFlow->at(i);
    nCand+=1;
    c_id.push_back(c.particleId());
    c_pt.push_back(c.pt());
    c_phi.push_back(c.phi());
    c_eta.push_back(c.eta());
    c_energy.push_back(c.p4().E());
    c_charge.push_back(c.charge());
  }

  put("nCand", nCand); // NAN);

  put("candEta", c_eta); // NAN);
  put("candPhi", c_phi); // NAN);
  put("candPt", c_pt); // NAN);
  put("candEnergy", c_energy); // NAN);
  put("candId", c_id); // NAN);
  put("candCharge", c_charge); // NAN);
}

void PFCandTupelizer::addAllVars( )
{
  addVar("nCand/I");
  addVar("candEta/F[]");
  addVar("candPhi/F[]");
  addVar("candPt/F[]");
  addVar("candEnergy/F[]");
  addVar("candId/I[]");
  addVar("candCharge/I[]");
}

DEFINE_FWK_MODULE(PFCandTupelizer);
