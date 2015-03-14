#include "Workspace/HEPHYCMSSWTools/plugins/PFCandTupelizer.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"

#include "DataFormats/ParticleFlowReco/interface/PFBlock.h"
#include "DataFormats/ParticleFlowReco/interface/PFBlockElementTrack.h"
#include "DataFormats/ParticleFlowReco/interface/PFBlockElementCluster.h"
#include "DataFormats/ParticleFlowReco/interface/PFCluster.h"

using namespace std;

namespace {
  string prefix ("[PFCandTupelizer] ");
}

PFCandTupelizer::~PFCandTupelizer() {}

PFCandTupelizer::PFCandTupelizer( const edm::ParameterSet & pset):
  Tupelizer(pset),
  pflowToken_  (consumes<std::vector<reco::PFCandidate> >(pset.getParameter<edm::InputTag>("srcPFlow"))),
  fillIsolatedChargedHadrons_(pset.getUntrackedParameter<bool>("fillIsolatedChargedHadrons"))

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
  std::vector<float> c_pt, c_eta, c_phi,c_energy, c_ecalRawE, c_hcalRawE;
  std::vector<float> c_trackPt, c_trackEta, c_trackPhi;
  std::vector<float> c_ecalE;//, c_ecalEta, c_ecalPhi;
  std::vector<float> c_hcalE;//, c_hcalEta, c_hcalPhi;
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

    //fill quantities for isolated charged hadron quantities
    if (fillIsolatedChargedHadrons_) {
      c_ecalRawE.push_back(c.rawEcalEnergy());
      c_hcalRawE.push_back(c.rawHcalEnergy());
      const reco::PFCandidate::ElementsInBlocks& theElements = c.elementsInBlocks();
      if( theElements.empty() ) continue;
      unsigned int iTrack=-999;
      std::vector<unsigned int> iECAL;// =999;
      std::vector<unsigned int> iHCAL;// =999;
      const reco::PFBlockRef blockRef = theElements[0].first;
      const edm::OwnVector<reco::PFBlockElement>& elements = blockRef->elements();
      // Check that there is only one track in the block.
      unsigned int nTracks = 0;
      if (c.particleId() == 1) {
        for(unsigned int iEle=0; iEle<elements.size(); iEle++) {  
        // Find the tracks in the block
          reco::PFBlockElement::Type type = elements[iEle].type();
          switch( type ) {
          case reco::PFBlockElement::TRACK:
            iTrack = iEle;
            nTracks++;
            break;
          case reco::PFBlockElement::ECAL:
            iECAL.push_back( iEle );
            break;
          case reco::PFBlockElement::HCAL:
            iHCAL.push_back( iEle );
            break;
          default:
            continue;
          }
        } 
      }
      if ( nTracks == 1 ){
        // Characteristics of the track
        const reco::PFBlockElementTrack& et = dynamic_cast<const reco::PFBlockElementTrack &>( elements[iTrack] );
        c_trackPt.push_back(et.trackRef()->pt());
        c_trackEta.push_back(et.trackRef()->eta());
        c_trackPhi.push_back(et.trackRef()->phi());
        c_ecalE.push_back(0.);
//        c_ecalEta.push_back(0.);
//        c_ecalPhi.push_back(0.);
        c_hcalE.push_back(0.);
//        c_hcalEta.push_back(0.);
//        c_hcalPhi.push_back(0.);
        //ECAL element
        for(unsigned ii=0;ii<iECAL.size();ii++) {
          const reco::PFBlockElementCluster& eecal = dynamic_cast<const reco::PFBlockElementCluster &>( elements[ iECAL[ii] ] );
          c_ecalE.back()+=eecal.clusterRef()->E();
//          c_ecalEta.push_back(eecal.clusterRef()->eta());
//          c_ecalPhi.push_back(eecal.clusterRef()->phi());
//        } else {
//          c_ecalE.push_back(NAN);
//          c_ecalEta.push_back(NAN);
//          c_ecalPhi.push_back(NAN);
        }
        for(unsigned ii=0;ii<iHCAL.size();ii++) {
          const reco::PFBlockElementCluster& ehcal = dynamic_cast<const reco::PFBlockElementCluster &>( elements[ iHCAL[ii] ] );
          c_hcalE.back()+=ehcal.clusterRef()->E();
//          c_hcalEta.push_back(ehcal.clusterRef()->eta());
//          c_hcalPhi.push_back(ehcal.clusterRef()->phi());
//        } else {
//          c_hcalE.push_back(NAN);
//          c_hcalEta.push_back(NAN);
//          c_hcalPhi.push_back(NAN);
        }
      } else {
        c_trackPt.push_back(NAN);
        c_trackEta.push_back(NAN);
        c_trackPhi.push_back(NAN);
        c_ecalE.push_back(NAN);
//        c_ecalEta.push_back(NAN);
//        c_ecalPhi.push_back(NAN);
        c_hcalE.push_back(NAN);
//        c_hcalEta.push_back(NAN);
//        c_hcalPhi.push_back(NAN);
      }
    } 
  }
  put("nCand", nCand); // NAN);
  put("candEta", c_eta); // NAN);
  put("candPhi", c_phi); // NAN);
  put("candPt", c_pt); // NAN);
  put("candEnergy", c_energy); // NAN);
  put("candId", c_id); // NAN);
  put("candCharge", c_charge); // NAN);
  if (fillIsolatedChargedHadrons_) {
    put("candECalRawE",c_ecalRawE);
    put("candHCalRawE",c_hcalRawE);
    put("candTrackPt",c_trackPt);
    put("candTrackEta",c_trackEta);
    put("candTrackPhi",c_trackPhi);
    put("candECalClusterE",c_ecalE);
//    put("candECalClusterEta",c_ecalEta);
//    put("candECalClusterPhi",c_ecalPhi);
    put("candHCalClusterE",c_hcalE);
//    put("candHCalClusterEta",c_hcalEta);
//    put("candHCalClusterPhi",c_hcalPhi);
  }
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
  if (fillIsolatedChargedHadrons_) {
    addVar("candECalRawE/F[]");
    addVar("candHCalRawE/F[]");
    addVar("candTrackPt/F[]");
    addVar("candTrackEta/F[]");
    addVar("candTrackPhi/F[]");
    addVar("candECalClusterE/F[]");
//    addVar("candECalClusterEta/F[]");
//    addVar("candECalClusterPhi/F[]");
    addVar("candHCalClusterE/F[]");
//    addVar("candHCalClusterEta/F[]");
//    addVar("candHCalClusterPhi/F[]");
  }
}

DEFINE_FWK_MODULE(PFCandTupelizer);
