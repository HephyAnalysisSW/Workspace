#include "FWCore/Framework/interface/MakerMacros.h"
#include "Workspace/HEPHYCMSSWTools/plugins/MuonTupelizer.h"
#include "Workspace/HEPHYCMSSWTools/interface/EdmHelper.h"

using namespace std;

namespace {

  string prefix ("[MuonTupelizer] ");
 
}

MuonTupelizer::~MuonTupelizer() {}

MuonTupelizer::MuonTupelizer( const edm::ParameterSet & pset):
  Tupelizer(pset),
  params_ ( pset ),
  verbose_ ( pset.getUntrackedParameter< bool >("verbose")),
  input_ ( pset.getUntrackedParameter< edm::InputTag >("input") ),
  ptThreshold_ (pset.getUntrackedParameter< double >("ptThreshold") ),
  vertices_ ( pset.getUntrackedParameter< edm::InputTag >("vertices") ),

  muonPFRelIsoDeltaBeta_ (pset.getUntrackedParameter< bool >("muonPFRelIsoDeltaBeta") )
{
  addAllVars();
}


void MuonTupelizer::beginJob ( )
{
  cout << "[MuonTupelizer] starting ... " << endl;
}

void MuonTupelizer::endJob()
{
  cout << endl;
  cout << "[MuonTupelizer] shutting down ... " << endl;
}

void MuonTupelizer::beginRun ( edm::Run & iRun, edm::EventSetup const & iSetup )
{
}

void MuonTupelizer::produce( edm::Event & ev, const edm::EventSetup & setup) {
  ev_ = &ev;
//  bool isData(ev.eventAuxiliary().isRealData());

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
  math::XYZPoint vertexPosition(NAN, NAN, NAN);
  if (goodVertices.size()>0) {
    vertexPosition = goodVertices[0].position();
  }

  vector<pat::Muon> muons (EdmHelper::getObjs<pat::Muon> (ev, input_));
  // Muon Selection
// vector<pat::Muon> good_muons, veto_muons;
  std::vector<float> muonsPt, muonsEta, muonsPhi, muonsPFRelIso, muonsNormChi2, muonsDxy, muonsDz, muonsIso03sumChargedHadronPt, muonsIso03sumNeutralHadronEt, muonsIso03sumPhotonEt, muonsIso03sumPUChargedHadronPt;
  std::vector<int> muonsPdg, muonsNValMuonHits, muonsNumMatchedStations, muonsPixelHits, muonsNumtrackerLayerWithMeasurement;
  std::vector<int> muonsisPF, muonsisGlobal, muonsisTracker;
  int muonCounter=0;
// edm::Handle<reco::PFCandidateCollection> pfCandidates;
// ev.getByLabel("particleFlow",pfCandidates);
// reco::PFCandidateCollection pfCands = *pfCandidates;

  if (verbose_) cout<<"\nrun "<< ev.id().run()<<" lumi "<<ev.luminosityBlock()<<" event "<<ev.id().event()<<endl;
  if (verbose_) cout<<"vertex: x "<<goodVertices[0].x()<<" y "<<goodVertices[0].y()<<" z "<<goodVertices[0].z()<<" rho "<<goodVertices[0].position().rho()<<" ndof "<<goodVertices[0].ndof()<< endl;

  for (vector<pat::Muon>::const_iterator muon = muons.begin(); muon!=muons.end();muon++){

    bool isGlobal = muon->isGlobalMuon();
    bool isPF = muon->isPFMuon();
    bool isTracker = muon->isTrackerMuon();
    int nValMuonHits(-1);
    double normChi2(NAN);
    if ( !muon->globalTrack().isNull() ) {
      nValMuonHits = muon->globalTrack()->hitPattern().numberOfValidMuonHits();
      normChi2 = muon->globalTrack()->chi2() / muon->globalTrack()->ndof();
    }
    int numMatchedStations = muon->numberOfMatchedStations();
    int pixelHits(0);
    double dxy(NAN);
    double dz(NAN);
    if (!muon->innerTrack().isNull()) {
      dxy = fabs(muon->innerTrack()->dxy(vertexPosition));
      dz = fabs(muon->innerTrack()->dz(vertexPosition));
      pixelHits = muon->innerTrack()->hitPattern().numberOfValidPixelHits();
    }
    int numTrackerLayersWithMeasurement(-1);
    if (!muon->track().isNull()) {
      numTrackerLayersWithMeasurement = muon->track()->hitPattern().trackerLayersWithMeasurement();
    }
    double pfRelIso (NAN);
    if (muon->pt()>0) {
      pfRelIso = muonPFRelIsoDeltaBeta_ ?
        (muon->pfIsolationR03().sumChargedHadronPt
         + max(0., muon->pfIsolationR03().sumNeutralHadronEt
                 + muon->pfIsolationR03().sumPhotonEt
             - 0.5*muon->pfIsolationR03().sumPUPt ) ) / muon->pt() :
        ( muon->pfIsolationR03().sumChargedHadronPt
       + muon->pfIsolationR03().sumNeutralHadronEt
       + muon->pfIsolationR03().sumPhotonEt ) / muon->pt();
    }
    if(muon->pt() >= ptThreshold_) {
        muonCounter++; // increment number of muons in this event
        muonsPt.push_back(muon->pt());
        muonsEta.push_back(muon->eta());
        muonsPhi.push_back(muon->phi());
        muonsPdg.push_back(muon->pdgId());
        muonsisPF.push_back(isPF);
        muonsisGlobal.push_back(isGlobal);
        muonsisTracker.push_back(isTracker);
        muonsPFRelIso.push_back(pfRelIso);
        muonsIso03sumChargedHadronPt.push_back(muon->pfIsolationR03().sumChargedHadronPt);
        muonsIso03sumNeutralHadronEt.push_back(muon->pfIsolationR03().sumNeutralHadronEt);
        muonsIso03sumPhotonEt.push_back(muon->pfIsolationR03().sumPhotonEt);
        muonsIso03sumPUChargedHadronPt.push_back(muon->pfIsolationR03().sumPUPt);
        muonsNormChi2.push_back(normChi2);
        muonsNValMuonHits.push_back(nValMuonHits);
        muonsNumMatchedStations.push_back(numMatchedStations);
        muonsPixelHits.push_back(pixelHits);
        muonsNumtrackerLayerWithMeasurement.push_back(numTrackerLayersWithMeasurement);
        muonsDxy.push_back(dxy);
        muonsDz.push_back(dz);
    }
    if (verbose_) {
      cout<<"[muon "<< muon - muons.begin()<<boolalpha<<"]"<<endl;//isGood? "<<isGood<<" isGoodVeto "<<isGoodVeto<<endl;
      cout<<" pt "<<muon->pt()<<" eta "<<muon->eta()<<" phi "<<muon->phi()<<" isPF "<<isPF<<" isGlobal "<<isGlobal <<" isTracker "<<isTracker<<" pfRelIso "<<pfRelIso<<" normChi2 "<<normChi2<<endl;//" pfDeltaPT "<< deltapT<<endl;
      cout<<" nValMuonHits "<<nValMuonHits<<" numMatchedStations "<<numMatchedStations<<" pixelHits "<<pixelHits<<" numTrackerLayersWithMeasurement "<<numTrackerLayersWithMeasurement<<" dxy "<<dxy<<" dz "<<dz<<endl;
      cout<<" chargedHadronIso "<<muon->pfIsolationR03().sumChargedHadronPt<<" neutralHadronIso "<<muon->pfIsolationR03().sumNeutralHadronEt<<" gammaIso "<< muon->pfIsolationR03().sumPhotonEt<<" chargedPUIso "<<muon->pfIsolationR03().sumPUPt<<" doDeltaBeta "<<muonPFRelIsoDeltaBeta_<<endl;
      cout<<" ecalIso "<<muon->ecalIso()<<" hcalIso "<<muon->hcalIso()<<" trackIso "<<muon->trackIso()<<endl;
    }
  }

  put("nmuons", muonCounter);
  put("muonsPt", muonsPt);
  put("muonsEta",muonsEta);
  put("muonsPdg",muonsPdg);
  put("muonsPhi", muonsPhi);
  put("muonsisPF", muonsisPF);
  put("muonsisGlobal",muonsisGlobal);
  put("muonsisTracker",muonsisTracker);
  put("muonsPFRelIso",muonsPFRelIso);
  put("muonsIso03sumChargedHadronPt", muonsIso03sumChargedHadronPt);
  put("muonsIso03sumNeutralHadronEt", muonsIso03sumNeutralHadronEt);
  put("muonsIso03sumPhotonEt", muonsIso03sumPhotonEt);
  put("muonsIso03sumPUChargedHadronPt", muonsIso03sumPUChargedHadronPt);
  put("muonsNormChi2",muonsNormChi2);
  put("muonsNValMuonHits",muonsNValMuonHits);
  put("muonsNumMatchedStations",muonsNumMatchedStations);
  put("muonsPixelHits",muonsPixelHits);
  put("muonsNumtrackerLayerWithMeasurement",muonsNumtrackerLayerWithMeasurement);
  put("muonsDxy",muonsDxy);
  put("muonsDz",muonsDz);
}

void MuonTupelizer::addAllVars( )
{
   addVar("nmuons/I");
   addVar("muonsPt/F[]");
   addVar("muonsEta/F[]");
   addVar("muonsPdg/I[]");
   addVar("muonsPhi/F[]");
   addVar("muonsisPF/I[]");
   addVar("muonsisGlobal/I[]");
   addVar("muonsisTracker/I[]");
   addVar("muonsPFRelIso/F[]");
   addVar("muonsIso03sumChargedHadronPt/F[]");
   addVar("muonsIso03sumNeutralHadronEt/F[]");
   addVar("muonsIso03sumPhotonEt/F[]");
   addVar("muonsIso03sumPUChargedHadronPt/F[]");
   addVar("muonsNormChi2/F[]");
   addVar("muonsNValMuonHits/I[]");
   addVar("muonsNumMatchedStations/I[]");
   addVar("muonsPixelHits/I[]");
   addVar("muonsNumtrackerLayerWithMeasurement/I[]");
   addVar("muonsDxy/F[]");
   addVar("muonsDz/F[]");
}

DEFINE_FWK_MODULE(MuonTupelizer);
