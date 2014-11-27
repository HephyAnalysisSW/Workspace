#include "FWCore/Framework/interface/MakerMacros.h"
#include "Workspace/HEPHYCMSSWTools/plugins/BasicTupelizer.h"
#include "Workspace/HEPHYCMSSWTools/interface/EdmHelper.h"
#include <SimDataFormats/GeneratorProducts/interface/HepMCProduct.h>
#include <SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h>
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "DataFormats/METReco/interface/GenMET.h"
#include "DataFormats/METReco/interface/GenMETCollection.h"
#include "DataFormats/METReco/interface/PFMET.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"

using namespace std;

namespace {
  string prefix ("[BasicTupelizer] ");
}

BasicTupelizer::~BasicTupelizer() {}

BasicTupelizer::BasicTupelizer( const edm::ParameterSet & pset):
  Tupelizer(pset),
  params_ ( pset ),
  verbose_ ( pset.getUntrackedParameter< bool >("verbose")),
  vertices_ ( pset.getUntrackedParameter< edm::InputTag >("vertices") ),

  metsToMonitor_(pset.getUntrackedParameter<std::vector<std::string> > ("metsToMonitor") ),
  genMetContainer_(pset.getUntrackedParameter<edm::InputTag > ("genMetContainer") ),
  storeGenMet_(pset.getUntrackedParameter<bool > ("storeGenMet") ),
  addMSugraOSETInfo_(pset.getUntrackedParameter<bool>("addMSugraOSETInfo")),
  addPDFWeights_(pset.getUntrackedParameter<bool>("addPDFWeights"))

{
  addAllVars();
}

void BasicTupelizer::beginJob ( )
{
  cout << "[BasicTupelizer] starting ... " << endl;
}

void BasicTupelizer::endJob()
{
  cout << endl;
  cout << "[BasicTupelizer] shutting down ... " << endl;
}

void BasicTupelizer::beginRun ( edm::Run & iRun, edm::EventSetup const & iSetup )
{
}


void BasicTupelizer::produce( edm::Event & ev, const edm::EventSetup & setup) {
  ev_ = &ev;
  put("event",ev.id().event());
  put("run",ev.id().run());
  put("lumi",ev.luminosityBlock());
  put("bx",ev.bunchCrossing());
  bool isData (ev.eventAuxiliary().isRealData());
  put("isMC",!isData);
  
  if (!isData){
    edm::Handle<std::vector< PileupSummaryInfo > > PupInfo;
    try {
      ev.getByLabel(edm::InputTag("addPileupInfo"), PupInfo);
      if (PupInfo.isValid()) {
        std::vector<PileupSummaryInfo>::const_iterator PVI;
        int npv = -1;
        float npv_true = -1;
        for(PVI = PupInfo->begin(); PVI != PupInfo->end(); ++PVI) {
          int BX = PVI->getBunchCrossing();
          if(BX == 0) {
            npv = PVI->getPU_NumInteractions();
            npv_true = PVI->getTrueNumInteractions();
            continue;
          }
        }
        put("ngenVertices",npv);
        put("nTrueGenVertices",npv_true);
      }
    } catch (cms::Exception & e){
      put("ngenVertices",-1);
      put("nTrueGenVertices",-1);
    }
  }

  //BeamSpot
  math::XYZPoint beamSpotPosition;
  beamSpotPosition.SetCoordinates(0,0,0);
  edm::Handle<reco::BeamSpot> bsHandle;
  try {
    ev.getByLabel("offlineBeamSpot", bsHandle);
    if (!bsHandle.isValid() || bsHandle.failedToGet()) {
      cout << prefix << " BeamSpot not valid!." << endl;
    } else {
      beamSpotPosition = bsHandle->position();
    }
  } catch (cms::Exception & e) {
    cout << prefix << " error (BeamSpot): " << e.what() << endl;
  }

  //get primary vertices
  edm::Handle<vector<reco::Vertex> > hpv;
  try {
    ev.getByLabel( vertices_, hpv );
  } catch ( cms::Exception & e ) {
    cout <<prefix<<"error: " << e.what() << endl;
  }
  vector<reco::Vertex> goodVertices;
  for (unsigned i = 0; i < hpv->size(); i++) {
    if ( (*hpv)[i].ndof() > 4 &&
       ( fabs((*hpv)[i].z()) <= 24. ) &&
       ( fabs((*hpv)[i].position().rho()) <= 2.0 ) )
       goodVertices.push_back((*hpv)[i]);
  }
  put( "ngoodVertices", goodVertices.size());
  //determine position of first good vertex
  math::XYZPoint vertexPosition(NAN, NAN, NAN);
  if (goodVertices.size()>0) {
    vertexPosition = goodVertices[0].position();
  }
  
  if (storeGenMet_) {
    edm::Handle<vector<pat::MET> > gmc;
    try {
      ev.getByLabel( genMetContainer_, gmc );
    } catch ( cms::Exception & e ) {
      cout <<prefix<<"error: " << e.what() << endl;
    }
    put("genMet", (*gmc)[0].genMET()->pt());
    put("genMetPhi", (*gmc)[0].genMET()->phi());
  }
  for (std::vector<std::string>::iterator s = metsToMonitor_.begin(); s != metsToMonitor_.end(); s++) {
    std::string metName = *s;
    edm::Handle<vector<pat::MET> > met;
    try {
      ev.getByLabel( edm::InputTag(*s), met );
    } catch ( cms::Exception & e ) {
      cout <<prefix<<"error: " << e.what() << endl;
    }
    put(metName, (*met)[0].pt());
    put(metName+"Phi", (*met)[0].phi());
    put(metName+"SumEt", (*met)[0].sumEt());
    put(metName+"Significance", (*met)[0].significance());
  }

  if (addMSugraOSETInfo_) {
    put("osetMgl", modelParameters_.get ( "mgl", ev ));
    put("osetMsq", modelParameters_.get ( "msq", ev ));
    put("osetMC", modelParameters_.get ( "mC", ev ));
    put("osetMN", modelParameters_.get ( "mN", ev ));

//    edm::InputTag genParticleTag = edm::InputTag("genParticles");
//    edm::Handle< vector< reco::GenParticle > > genParticleHandle;
//    try {
//      ev.getByLabel(genParticleTag, genParticleHandle );
//      if (!genParticleHandle.isValid() || genParticleHandle.failedToGet()) {
//  // if (verbose_) cout << prefix << "GenParticles not valid!." << endl;
//      }
//    } catch (exception & e) {
//      cout << prefix << "error (GenParticles): " << e.what() << endl;
//    }
//
//    vector< const reco::GenParticle *> gluinos;
//    if ( genParticleHandle.isValid() and (!genParticleHandle.failedToGet())) {
//      for( unsigned i = 0; i < genParticleHandle->size(); i++ ) {
//        if (((*genParticleHandle)[i].pdgId() == 1000021) && ( (*genParticleHandle)[i].status() == 3)) gluinos.push_back( &( (*genParticleHandle)[i] ));
//      }
//    }
//    std::vector<int> selectedIds;
//    for (unsigned int i=0; i<genParticleHandle->size(); ++i) {
//      const reco::GenParticle& p = (*genParticleHandle)[i];
//       if (p.status() != 3) continue;
//       if (abs(p.pdgId()) < 1000000) continue;
//
//       bool hasSMMother(true);
//       for (unsigned int j=0; j<p.numberOfMothers(); ++j) {
//         if ( !(abs(p.mother(j)->pdgId())<1000000) ) {
//           hasSMMother = false;
//           break;
//         }
//       }
//       if ( hasSMMother ) selectedIds.push_back(p.pdgId());
//    }
//    sort(selectedIds.begin(),selectedIds.end());
//    put("sparticles", selectedIds);
//    if (gluinos.size()>0) {
//      put("gluino0Pt", gluinos[0]->pt());
//      put("gluino0Eta", gluinos[0]->eta());
//      put("gluino0Phi", gluinos[0]->phi());
//      put("gluino0Pdg", gluinos[0]->pdgId());
//    }
//    if (gluinos.size()>1) {
//      put("gluino1Pt", gluinos[1]->pt());
//      put("gluino1Eta", gluinos[1]->eta());
//      put("gluino1Phi", gluinos[1]->phi());
//      put("gluino1Pdg", gluinos[1]->pdgId());
//    }
// put("osetType", modelParameters_.get ( "type", ev ));
  }

  if ( addPDFWeights_ and (!isData))
  {
    edm::InputTag cteqWeightTag("pdfWeights:cteq66"); // or any other PDF set
    edm::Handle<std::vector<double> > cteqWeightHandle;
    ev.getByLabel(cteqWeightTag, cteqWeightHandle);

    std::vector<double> cteqWeights = (*cteqWeightHandle);
    if (verbose_) {
      std::cout << "Event weight for central CTEQ PDF:" << cteqWeights[0] << std::endl;
      unsigned int nmembers = cteqWeights.size();
      for (unsigned int j=1; j<nmembers; j+=2) {
            std::cout << "Event weight for PDF variation +" << (j+1)/2 << ": " << cteqWeights[j] << std::endl;
            std::cout << "Event weight for PDF variation -" << (j+1)/2 << ": " << cteqWeights[j+1] << std::endl;
      }
    }
    put("cteqWeights", cteqWeights);

    edm::InputTag mstwWeightTag("pdfWeights:MSTW2008nlo68cl"); // or any other PDF set
    edm::Handle<std::vector<double> > mstwWeightHandle;
    ev.getByLabel(mstwWeightTag, mstwWeightHandle);
    std::vector<double> mstwWeights = (*mstwWeightHandle);
    put("mstwWeights", mstwWeights);

    edm::InputTag nnpdfWeightTag("pdfWeights:NNPDF20"); // or any other PDF set
    edm::Handle<std::vector<double> > nnpdfWeightHandle;
    ev.getByLabel(nnpdfWeightTag, nnpdfWeightHandle);
    std::vector<double> nnpdfWeights = (*nnpdfWeightHandle);
    put("nnpdfWeights", nnpdfWeights);

  }
}

void BasicTupelizer::addAllVars( )
{
  for (std::vector<std::string>::iterator s = metsToMonitor_.begin(); s != metsToMonitor_.end(); s++) {
    std::string metName = *s;
    addVar(metName+"/F");
    addVar(metName+"Phi/F");
    addVar(metName+"SumEt/F");
    addVar(metName+"Significance/F");
  }

  addVar("event/l"); // 0);
  addVar("run/I"); // NAN);
  addVar("lumi/I"); // NAN);
  addVar("bx/I"); // NAN);
  addVar("isMC/O"); // NAN);
  addVar("ngenVertices/I"); // -1);
  addVar("nTrueGenVertices/F"); // -1);

  addVar("ngoodVertices/I");
  if (storeGenMet_) { 
    addVar("genMet/F");
    addVar("genMetPhi/F");
  }

  if (addMSugraOSETInfo_) {
//    addVar("sparticles/I[]");
//    addVar("gluino0Pt/F");
//    addVar("gluino0Eta/F");
//    addVar("gluino0Phi/F");
//    addVar("gluino0Pdg/I");
//    addVar("gluino1Pt/F");
//    addVar("gluino1Eta/F");
//    addVar("gluino1Phi/F");
//    addVar("gluino1Pdg/I");
    addVar("osetMgl/F"); // NAN);
    addVar("osetMsq/F"); // NAN);
    addVar("osetMC/F"); // NAN);
    addVar("osetMN/F"); // NAN);
  }
  if (addPDFWeights_) {
    addVar("cteqWeights/D[]");
    addVar("mstwWeights/D[]");
    addVar("nnpdfWeights/D[]");
  }
}

DEFINE_FWK_MODULE(BasicTupelizer);
