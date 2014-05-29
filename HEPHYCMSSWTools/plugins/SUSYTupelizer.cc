#include "FWCore/Framework/interface/MakerMacros.h"
#include "Workspace/HEPHYCMSSWTools/plugins/SUSYTupelizer.h"
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
#include "DataFormats/HLTReco/interface/TriggerEvent.h"
#include "DataFormats/JetReco/interface/PileupJetIdentifier.h"
#include "DataFormats/METReco/interface/GenMET.h"
#include "DataFormats/METReco/interface/GenMETCollection.h"
#include "DataFormats/METReco/interface/PFMET.h"
#include "DataFormats/PatCandidates/interface/TriggerEvent.h"
#include "Workspace/HEPHYCMSSWTools/interface/ElectronEffectiveArea.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "JetMETCorrections/Objects/interface/JetCorrectionsRecord.h"
#include "PhysicsTools/PatAlgos/plugins/PATElectronProducer.h"
#include "PhysicsTools/SelectorUtils/interface/PFJetIDSelectionFunctor.h"
#include "RecoEgamma/EgammaTools/interface/ConversionTools.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"

using namespace std;

namespace {

  string prefix ("[SUSYTupelizer] ");
 
  const reco::GenParticle* getGenTau(const pat::Tau& patTau)
  {
    std::vector<reco::GenParticleRef> associatedGenParticles = patTau.genParticleRefs();
    for ( std::vector<reco::GenParticleRef>::const_iterator it = associatedGenParticles.begin();
          it != associatedGenParticles.end(); ++it ) {
      if ( it->isAvailable() ) {
        const reco::GenParticleRef& genParticle = (*it);
        if ( genParticle->pdgId() == -15 || genParticle->pdgId() == +15 ) return genParticle.get();
      }
    }
  
    return 0;
  }
 
  int prod(std::pair<int,int> p) {
  return p.first*p.second;
  }

  class greaterBTag {
    public:
    greaterBTag(std::string tagger) {tag_ = tagger;};
    bool operator()(pat::Jet a, pat::Jet b) {
      if (a.bDiscriminator(tag_) == b.bDiscriminator(tag_)){
return a.pt() > b.pt();
      }else{
return a.bDiscriminator(tag_) > b.bDiscriminator(tag_);
      }
    }
    private:
    std::string tag_;
  };
  void myReplace(std::string& str, const std::string& oldStr, const std::string& newStr)
  {
    size_t pos = 0;
    while((pos = str.find(oldStr, pos)) != std::string::npos)
    {
       str.replace(pos, oldStr.length(), newStr);
       pos += newStr.length();
    }
  }

  double getDeltaPt(const math::XYZTLorentzVector & p4, const reco::PFCandidateCollection & pfCands, reco::PFCandidate::ParticleType t ) {
    double deltaRVal =999.;
    double deltapT=999.;
    for (reco::PFCandidateCollection::const_iterator ipf = pfCands.begin(); ipf != pfCands.end(); ++ipf) {
      if (((*ipf).particleId() == t) and ((*ipf).pt()>10.)) {
        if (reco::deltaR((*ipf).p4(), p4) < deltaRVal) {
          deltaRVal = reco::deltaR((*ipf).p4(), p4);
          deltapT = fabs(p4.pt() - (*ipf).pt());
        }
      }
    }
    return deltapT;
  }

  bool decaysIntoTop(const reco::Candidate * p){

    if (p==NULL) return false;
    if (p->numberOfDaughters()==0) return false;
    if (p->status()!=3) return false;
    if (abs(p->pdgId())==6) return true;

    for (unsigned i = 0; i<p->numberOfDaughters(); i++){
      if (decaysIntoTop(p->daughter(i))) return true;
    }
    return false;
  }

  std::vector<const reco::Candidate * > getDaughterParticles(const reco::Candidate * p , int absPdgId = -1, int status = 3) {
    std::vector<const reco::Candidate * > res;
    for (unsigned i=0; i<p->numberOfDaughters();i++) {
      if (
          ( (status==p->daughter(i)->status() or status<0) and
          ( ( abs(p->daughter(i)->pdgId()) == absPdgId) or absPdgId < 0) ) )
        res.push_back(p->daughter(i));
    }
    return res;
  }
}

SUSYTupelizer::~SUSYTupelizer() {}

SUSYTupelizer::SUSYTupelizer( const edm::ParameterSet & pset):
  Tupelizer(pset),
  params_ ( pset ),
  verbose_ ( pset.getUntrackedParameter< bool >("verbose")),
  triggerCollection_ ( pset.getUntrackedParameter< edm::InputTag >("triggerCollection") ),
  patJets_ ( pset.getUntrackedParameter< edm::InputTag >("patJets") ),
  patMuons_ ( pset.getUntrackedParameter< edm::InputTag >("patMuons") ),
  patElectrons_ ( pset.getUntrackedParameter< edm::InputTag >("patElectrons") ),
  patTaus_ ( pset.getUntrackedParameter< edm::InputTag >("patTaus") ),

  vertices_ ( pset.getUntrackedParameter< edm::InputTag >("vertices") ),
  lowLeptonPtThreshold_ (pset.getUntrackedParameter< double >("lowLeptonPtThreshold") ),
  softJetPtThreshold_ (pset.getUntrackedParameter< double >("softJetPtThreshold") ),

// muonPt_ (pset.getUntrackedParameter< double >("muonPt") ),
// muonEta_ (pset.getUntrackedParameter< double >("muonEta") ),
// muonIsGlobal_ (pset.getUntrackedParameter< bool >("muonIsGlobal") ),
// muonHasPFMatch_ (pset.getUntrackedParameter< bool >("muonHasPFMatch") ),
// muonIsPF_ (pset.getUntrackedParameter< bool >("muonIsPF") ),
// muonNormChi2_ (pset.getUntrackedParameter< double >("muonNormChi2") ),
// muonNumValMuonHits_ (pset.getUntrackedParameter< int >("muonNumValMuonHits") ),
// muonNumMatchedStations_ (pset.getUntrackedParameter< int >("muonNumMatchedStations") ),
// muonNumPixelHits_ (pset.getUntrackedParameter< int >("muonNumPixelHits") ),
// muonNumTrackerLayersWithMeasurement_ (pset.getUntrackedParameter< int >("muonNumTrackerLayersWithMeasurement") ),
// muonPFRelIso_ (pset.getUntrackedParameter< double >("muonPFRelIso") ),
  muonPFRelIsoDeltaBeta_ (pset.getUntrackedParameter< bool >("muonPFRelIsoDeltaBeta") ),
// muonDxy_ (pset.getUntrackedParameter< double >("muonDxy") ),
// muonDz_ (pset.getUntrackedParameter< double >("muonDz") ),
//
// vetoMuonPt_ (pset.getUntrackedParameter< double >("vetoMuonPt") ),
// vetoMuonEta_ (pset.getUntrackedParameter< double >("vetoMuonEta") ),
// vetoMuonIsGlobalOrIsTracker_ (pset.getUntrackedParameter< bool >("vetoMuonIsGlobalOrIsTracker") ),
// vetoMuonIsPF_ (pset.getUntrackedParameter< bool >("vetoMuonIsPF") ),
// vetoMuonPFRelIso_ (pset.getUntrackedParameter< double >("vetoMuonPFRelIso") ),
// vetoMuonPFRelIsoDeltaBeta_ (pset.getUntrackedParameter< bool >("vetoMuonPFRelIsoDeltaBeta") ),
// vetoMuonDxy_ (pset.getUntrackedParameter< double >("vetoMuonDxy") ),
// vetoMuonDz_ (pset.getUntrackedParameter< double >("vetoMuonDz") ),
// // steerables Ele:
// elePt_ ( pset.getUntrackedParameter< double >("elePt") ),
// eleEta_ (pset.getUntrackedParameter< double >("eleEta") ),
// eleOneOverEMinusOneOverP_ ( pset.getUntrackedParameter< double >("eleOneOverEMinusOneOverP") ),
// eleDxy_ ( pset.getUntrackedParameter< double >("eleDxy") ),
// eleDz_ ( pset.getUntrackedParameter< double >("eleDz") ),
// elePFRelIsoBarrel_ ( pset.getUntrackedParameter< double >("elePFRelIsoBarrel") ),
// elePFRelIsoEndcap_ ( pset.getUntrackedParameter< double >("elePFRelIsoEndcap") ),
  elePFRelIsoAreaCorrected_ ( pset.getUntrackedParameter< bool >("elePFRelIsoAreaCorrected") ),
  eleRho_ ( pset.getUntrackedParameter< edm::InputTag >("eleRho") ),
// eleSigmaIEtaIEtaBarrel_ ( pset.getUntrackedParameter< double >("eleSigmaIEtaIEtaBarrel") ),
// eleSigmaIEtaIEtaEndcap_ ( pset.getUntrackedParameter< double >("eleSigmaIEtaIEtaEndcap") ),
// eleHoEBarrel_ ( pset.getUntrackedParameter< double >("eleHoEBarrel") ),
// eleHoEEndcap_ ( pset.getUntrackedParameter< double >("eleHoEEndcap") ),
// eleDPhiBarrel_ ( pset.getUntrackedParameter< double >("eleDPhiBarrel") ),
// eleDPhiEndcap_ ( pset.getUntrackedParameter< double >("eleDPhiEndcap") ),
// eleDEtaBarrel_ ( pset.getUntrackedParameter< double >("eleDEtaBarrel") ),
// eleDEtaEndcap_ ( pset.getUntrackedParameter< double >("eleDEtaEndcap") ),
// eleMissingHits_ ( pset.getUntrackedParameter< int >("eleMissingHits") ),
// eleConversionRejection_ ( pset.getUntrackedParameter< bool >("eleConversionRejection") ),
// eleHasPFMatch_ (pset.getUntrackedParameter< bool >("eleHasPFMatch") ),
  // steerables veto Ele:
// vetoElePt_ ( pset.getUntrackedParameter< double >("vetoElePt") ),
// vetoEleEta_ (pset.getUntrackedParameter< double >("vetoEleEta") ),
// vetoEleDxy_ ( pset.getUntrackedParameter< double >("vetoEleDxy") ),
// vetoEleDz_ ( pset.getUntrackedParameter< double >("vetoEleDz") ),
// vetoElePFRelIsoBarrel_ ( pset.getUntrackedParameter< double >("vetoElePFRelIsoBarrel") ),
// vetoElePFRelIsoEndcap_ ( pset.getUntrackedParameter< double >("vetoElePFRelIsoEndcap") ),
// vetoEleSigmaIEtaIEtaBarrel_ ( pset.getUntrackedParameter< double >("vetoEleSigmaIEtaIEtaBarrel") ),
// vetoEleSigmaIEtaIEtaEndcap_ ( pset.getUntrackedParameter< double >("vetoEleSigmaIEtaIEtaEndcap") ),
// vetoEleHoEBarrel_ ( pset.getUntrackedParameter< double >("vetoEleHoEBarrel") ),
// vetoEleHoEEndcap_ ( pset.getUntrackedParameter< double >("vetoEleHoEEndcap") ),
// vetoEleDPhiBarrel_ ( pset.getUntrackedParameter< double >("vetoEleDPhiBarrel") ),
// vetoEleDPhiEndcap_ ( pset.getUntrackedParameter< double >("vetoEleDPhiEndcap") ),
// vetoEleDEtaBarrel_ ( pset.getUntrackedParameter< double >("vetoEleDEtaBarrel") ),
// vetoEleDEtaEndcap_ ( pset.getUntrackedParameter< double >("vetoEleDEtaEndcap") ),

// minJetPt_ ( pset.getUntrackedParameter< double >("minJetPt") ),
// maxJetEta_ ( pset.getUntrackedParameter< double >("maxJetEta") ),
  btag_ ( pset.getUntrackedParameter< std::string >("btag") ),
  hasL1Trigger_ ( pset.getUntrackedParameter< bool >("hasL1Trigger") ),
  puJetIdCutBased_( pset.getUntrackedParameter< edm::InputTag >("puJetIdCutBased") ),
  puJetIdFull53X_( pset.getUntrackedParameter< edm::InputTag >("puJetIdFull53X") ),
  puJetIdMET53X_( pset.getUntrackedParameter< edm::InputTag >("puJetIdMET53X") ),

  addTriggerInfo_(pset.getUntrackedParameter<bool>("addTriggerInfo")),
  triggersToMonitor_(pset.getUntrackedParameter<std::vector<std::string> > ("triggersToMonitor") ),
  metsToMonitor_(pset.getUntrackedParameter<std::vector<std::string> > ("metsToMonitor") ),
  addMetUncertaintyInfo_(pset.getUntrackedParameter<bool>("addMetUncertaintyInfo")),
  addJetVector_(pset.getUntrackedParameter<bool>("addJetVector")),
  addMuonVector_(pset.getUntrackedParameter<bool>("addMuonVector")),
  addEleVector_(pset.getUntrackedParameter<bool>("addEleVector")),
  addFullTauInfo_(pset.getUntrackedParameter<bool>("addFullTauInfo")),
// addGeneratorInfo_(pset.getUntrackedParameter<bool>("addGeneratorInfo")),
  addMSugraOSETInfo_(pset.getUntrackedParameter<bool>("addMSugraOSETInfo")),
  addPDFWeights_(pset.getUntrackedParameter<bool>("addPDFWeights"))

{
  addAllVars();
  if (addTriggerInfo_) {
    for (std::vector<std::string>::iterator s = triggersToMonitor_.begin(); s != triggersToMonitor_.end(); s++) {
      cout<<prefix<<"Monitoring the following trigger:"<<*s<<endl;
      std::string trigName = *s;
      std::string::size_type k = 0;
      while((k=trigName.find('_',k))!=trigName.npos) {
        trigName.erase(k, 1);
      }
      std::string prescName = trigName;
      prescName.replace(0, 3, "pre");
      addVar(trigName+"/I");
      trigNames_.push_back(trigName);
      addVar(prescName+"/I");
      prescNames_.push_back(prescName);
    }
  }
}


void SUSYTupelizer::beginJob ( )
{
  cout << "[SUSYTupelizer] starting ... " << endl;

  hlt_initialized_ = false;

}

void SUSYTupelizer::endJob()
{
  cout << endl;
  cout << "[SUSYTupelizer] shutting down ... " << endl;
}

void SUSYTupelizer::beginRun ( edm::Run & iRun, edm::EventSetup const & iSetup )
{
  bool changed(true);
  if (hltConfig_.init(iRun,iSetup,triggerCollection_.label(),changed)) {
  } else {
    edm::LogError(prefix) << " HLT config extraction failure with process name " << triggerCollection_;
  }
}

int SUSYTupelizer::prescale(edm::Event & ev, const edm::EventSetup & setup, std::string hlt) {
// return prod(hltConfig_.prescaleValues( ev, setup, hlt.c_str()));
  return hltConfig_.prescaleValue( ev, setup, hlt.c_str());
}


void SUSYTupelizer::produce( edm::Event & ev, const edm::EventSetup & setup) {
  ev_ = &ev;
// int peng(0);
  put("event",ev.id().event());
  put("run",ev.id().run());
  put("lumi",ev.luminosityBlock());
  put("bx",ev.bunchCrossing());
  bool isData;
  isData=ev.eventAuxiliary().isRealData();
  put("isMC",!isData);
  
  if (!isData){
    edm::Handle<std::vector< PileupSummaryInfo > > PupInfo;
    try {
      ev.getByLabel(edm::InputTag("addPileupInfo"), PupInfo);

// if (!PupInfo.isValid() || PupInfo.failedToGet()) {
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

    edm::Handle<unsigned int > flavHist;
    ev.getByLabel("flavorHistoryFilter", flavHist);
    const unsigned int flavorPath = *flavHist;
    put("flavorHistory", flavorPath);
  }
  //HLT - Triggers
  edm::Handle<trigger::TriggerEvent> triggerEvent;
  ev.getByLabel("hltTriggerSummaryAOD", triggerEvent);
  if (not triggerEvent.isValid()) {
    std::cout << "HLT Results with label: " << "hltTriggerSummaryAOD"
              << " not found" << std::endl;
    }
  edm::Handle<edm::TriggerResults> HLTR;
  edm::InputTag HLTTag = edm::InputTag("TriggerResults", "", triggerCollection_.label().c_str());
  ev.getByLabel(HLTTag, HLTR);
  if (HLTR.isValid()) {
// cout << "Init HLT info" << endl;
    edm::TriggerNames triggerNames = ev.triggerNames(*HLTR);
    HLT_names_ = triggerNames.triggerNames();
    if (! this->hlt_initialized_ ) {
      cout<<"HLT: "<<triggerCollection_.label().c_str()<<endl;
      for (unsigned i=0;i<HLT_names_.size();i++) {
        cout<<HLT_names_[i]<<endl;
      }
      SUSYTupelizer::hlt_initialized_ = true;
    }
  }
// bool muonTriggerUnprescaled = false;
// bool electronTriggerUnprescaled = false;
  for (unsigned i=0; i<HLT_names_.size(); ++i){
    if (addTriggerInfo_) {
      for (unsigned j = 0; j< triggersToMonitor_.size(); j++) {
        if (std::strstr(HLT_names_[i].c_str(), (triggersToMonitor_[j]+"_v").c_str())) {put(trigNames_[j], HLTR->accept(i));put(prescNames_[j], prescale( ev, setup, HLT_names_[i].c_str()));};
      }
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

  if(addMuonVector_){
    vector<pat::Muon> patMuons (EdmHelper::getObjs<pat::Muon> (ev, patMuons_));
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

    for (vector<pat::Muon>::const_iterator muon = patMuons.begin(); muon!=patMuons.end();muon++){

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
      if(muon->pt() >= lowLeptonPtThreshold_) {
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
  // muonsPFDeltaPT.push_back(deltapT);
      }
      if (verbose_) {
        cout<<"[muon "<< muon - patMuons.begin()<<boolalpha<<"]"<<endl;//isGood? "<<isGood<<" isGoodVeto "<<isGoodVeto<<endl;
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
  
/* ____ _ _____ _____ _ _
| _ \ / \|_ _| | ____| | ___ ___| |_ _ __ ___ _ __ ___
| |_) / _ \ | | | _| | |/ _ \/ __| __| '__/ _ \| '_ \/ __|
| __/ ___ \| | | |___| | __/ (__| |_| | | (_) | | | \__ \
|_| /_/ \_\_| |_____|_|\___|\___|\__|_| \___/|_| |_|___/
*/
  if(addEleVector_) {
    vector<pat::Electron> patElectrons (EdmHelper::getObjs<pat::Electron>(ev, patElectrons_));
  // vector<pat::Electron> veto_electrons, good_electrons;
    edm::Handle<reco::ConversionCollection> hConversions;
    ev.getByLabel("allConversions", hConversions);
    edm::Handle<double> eleRho;
    ev.getByLabel(eleRho_, eleRho);
    put("eleRho", *eleRho);
    std::vector<float> elesPt, elesEta, elesPhi, elesAeff, eles03ChargedHadronIso, eles03NeutralHadronIso, eles03GammaIso, elesOneOverEMinusOneOverP, elesPfRelIso, elesSigmaIEtaIEta, elesHoE, elesDPhi, elesDEta, elesDxy, elesDz;//, elesPFDeltaPT;

    std::vector<int> elesPdg, elesMissingHits;
    std::vector<int> elesPassConversionRejection, elesPassPATConversionVeto;
    int eleCounter=0;

  // //electron PFiso variables
    typedef std::vector< edm::Handle< edm::ValueMap<reco::IsoDeposit> > > IsoDepositMaps;
    typedef std::vector< edm::Handle< edm::ValueMap<double> > > IsoDepositVals;
    IsoDepositVals electronIsoValPFId(3);
    const IsoDepositVals * electronIsoVals = &electronIsoValPFId;
    ev.getByLabel("elPFIsoValueCharged03PFIdPFIso", electronIsoValPFId[0]);
    ev.getByLabel("elPFIsoValueGamma03PFIdPFIso", electronIsoValPFId[1]);
    ev.getByLabel("elPFIsoValueNeutral03PFIdPFIso", electronIsoValPFId[2]);

    for (vector<pat::Electron>::const_iterator ele = patElectrons.begin(); ele!=patElectrons.end();ele++){
      double pt = ele->pt();
      double eta = fabs(ele->superCluster()->eta());
      double oneOverEMinusOneOverP = fabs(1./ele->ecalEnergy() - 1./ele->trackMomentumAtVtx().R());
      double sigmaIEtaIEta = ele->scSigmaIEtaIEta();
      double HoE = ele->hadronicOverEm();
      double DPhi = fabs(ele->deltaPhiSuperClusterTrackAtVtx());
      double DEta = fabs(ele->deltaEtaSuperClusterTrackAtVtx());
      double dxy(NAN), dz(NAN);
      int missingHits(999);
      if (!ele->gsfTrack().isNull()){
        dxy = fabs(ele->gsfTrack()->dxy(vertexPosition));
        dz = fabs(ele->gsfTrack()->dz(vertexPosition));
        missingHits = ele->gsfTrack()->trackerExpectedHitsInner().numberOfHits();
      }

      edm::Ptr< reco::GsfElectron > gsfel = (edm::Ptr< reco::GsfElectron >) ele->originalObjectRef();
      bool passConversionRejection = gsfel.isNull() ? false : !ConversionTools::hasMatchedConversion(*gsfel,hConversions,beamSpotPosition);
      double charged = (*(*electronIsoVals)[0])[gsfel];
      double photon = (*(*electronIsoVals)[1])[gsfel];
      double neutral = (*(*electronIsoVals)[2])[gsfel];
      //cout<<charged<<" "<<photon<<" "<<neutral<<endl;
      
      double Aeff= isData ? ElectronEffectiveArea::GetElectronEffectiveArea(ElectronEffectiveArea::kEleGammaAndNeutralHadronIso03, eta, ElectronEffectiveArea::kEleEAData2011):
                     ElectronEffectiveArea::GetElectronEffectiveArea(ElectronEffectiveArea::kEleGammaAndNeutralHadronIso03, eta, ElectronEffectiveArea::kEleEAFall11MC);

      double pfRelIso = elePFRelIsoAreaCorrected_?( charged + max (0., photon + neutral - (*eleRho)*Aeff) ) / pt : ( charged + photon + neutral ) / pt;

      if (verbose_) {
        cout<<"[ele "<< ele - patElectrons.begin()<<"] "<<endl;//<<boolalpha<<"isBarrel? "<<isBarrel<<" isEndcap? "<<isEndcap<<" isGood "<<isGood<<" isGoodVeto "<<isGoodVeto<<endl;
        cout<<" pt "<<ele->pt()<<" eta "<<ele->superCluster()->eta()<<" phi "<<ele->phi()<<" oneOverEMinusOneOverP "<<oneOverEMinusOneOverP<<" sigmaIEtaIEta "<<sigmaIEtaIEta <<" pfRelIso "<<pfRelIso<<" HoE "<<HoE<<endl;
        cout<<" DPhi "<<DPhi<<" DEta "<<DEta<<" missingHits "<<missingHits<<" passConversionRejection "<<passConversionRejection<<" dxy "<<dxy<<" dz "<<dz<<endl;//" pfDeltaPT "<<deltapT<<endl;
        cout<<" chargedHadronIso03 "<<charged<<" neutralHadronIso03 "<<neutral<<" gammaIso03 "<< photon<<" Aeff "<<Aeff<<" rho "<<*eleRho<<endl;
        cout<<" ecalIso "<<ele->ecalIso()<<" hcalIso "<<ele->hcalIso()<<" trackIso "<<ele->trackIso()<<endl;
      }
      if(pt > lowLeptonPtThreshold_) //j#
      {
          eleCounter++; // increment number of electrons in event
          elesPt.push_back(pt);
          elesEta.push_back(ele->superCluster()->eta());
          elesPhi.push_back(ele->phi());
          elesPdg.push_back(ele->pdgId());
          elesOneOverEMinusOneOverP.push_back(oneOverEMinusOneOverP);
          elesPfRelIso.push_back(pfRelIso);
          elesAeff.push_back(Aeff);
          eles03ChargedHadronIso.push_back(charged);
          eles03NeutralHadronIso.push_back(neutral);
          eles03GammaIso.push_back(photon);
          elesSigmaIEtaIEta.push_back(sigmaIEtaIEta);
          elesHoE.push_back(HoE);
          elesDPhi.push_back(DPhi);
          elesDEta.push_back(DEta);
          elesMissingHits.push_back(missingHits);
          elesDxy.push_back(dxy);
          elesDz.push_back(dz);
          elesPassConversionRejection.push_back(passConversionRejection);
          elesPassPATConversionVeto.push_back(ele->passConversionVeto());
  // elesPFDeltaPT.push_back(deltapT);
      }
    }
    put("neles", eleCounter);
    put("elesPt", elesPt);
    put("elesEta", elesEta);
    put("elesPhi", elesPhi);
    put("elesPdg", elesPdg);
    put("elesOneOverEMinusOneOverP", elesOneOverEMinusOneOverP);
    put("elesPfRelIso", elesPfRelIso);
    put("eles03ChargedHadronIso", eles03ChargedHadronIso);
    put("eles03NeutralHadronIso", eles03NeutralHadronIso);
    put("eles03GammaIso", eles03GammaIso);
    put("elesAeff", elesAeff);
    put("elesSigmaIEtaIEta", elesSigmaIEtaIEta);
    put("elesHoE", elesHoE);
    put("elesDPhi", elesDPhi);
    put("elesDEta", elesDEta);
    put("elesMissingHits", elesMissingHits);
    put("elesDxy", elesDxy);
    put("elesDz", elesDz);
    put("elesPassConversionRejection", elesPassConversionRejection);
    put("elesPassPATConversionVeto", elesPassPATConversionVeto);
  }

  if (addFullTauInfo_) {
    vector<pat::Tau> patTaus (EdmHelper::getObjs<pat::Tau>(ev, patTaus_));
    int ntaus(0);
    std::vector<int> tausPdg, tausisPF, taushasMCMatch, tausByLooseCombinedIsolationDBSumPtCorr, tausDecayModeFinding, tausAgainstMuonLoose, tausAgainstElectronLoose;
    std::vector<float> tausPt, tausEta, tausPhi;
    for (unsigned i = 0; i<patTaus.size();i++) {
      int byLooseCombinedIsolationDeltaBetaCorr = patTaus[i].tauID("byLooseCombinedIsolationDeltaBetaCorr");
      int decayModeFinding = patTaus[i].tauID("decayModeFinding");
      int againstMuonLoose = patTaus[i].tauID("againstMuonLoose");
      int againstElectronLoose = patTaus[i].tauID("againstElectronLoose");
// if (patTaus[i].pt()>10. && (byLooseCombinedIsolationDeltaBetaCorr&&decayModeFinding&&againstMuonLoose&&againstElectronLoose)) {
      if (patTaus[i].pt()>10. && (decayModeFinding)) {
        ntaus++;
        tausPt.push_back(patTaus[i].pt());
        tausEta.push_back(patTaus[i].eta());
        tausPhi.push_back(patTaus[i].phi());
        tausPdg.push_back(patTaus[i].pdgId());
        tausisPF.push_back(patTaus[i].isPFTau());
        tausByLooseCombinedIsolationDBSumPtCorr.push_back(byLooseCombinedIsolationDeltaBetaCorr);
        tausDecayModeFinding.push_back(decayModeFinding);
        tausAgainstMuonLoose.push_back(againstMuonLoose);
        tausAgainstElectronLoose.push_back(againstElectronLoose);
        getGenTau(patTaus[i])? taushasMCMatch.push_back(1):taushasMCMatch.push_back(0);
      }
      if ((verbose_) and (patTaus[i].pt() > 10)) cout<<"[tau "<<i<<"/"<<ntaus<<"] "<<" pt "<<patTaus[i].pt()<<" eta "<<patTaus[i].eta()<<" phi "<<patTaus[i].phi()
         <<" tausPdg "<<patTaus[i].pdgId()<<boolalpha<<" tausisPF "<< patTaus[i].isPFTau() <<" tausByLooseCombinedIsolationDBSumPtCorr "<<byLooseCombinedIsolationDeltaBetaCorr
         <<" tausDecayModeFinding "<<decayModeFinding<<" tausAgainstMuonLoose "<<againstMuonLoose<<" tausAgainstElectronLoose "<<againstElectronLoose<<" taushasMCMatch "<<getGenTau(patTaus[i])<<endl;
    }
    put("ntaus", ntaus);
    put("tausPt", tausPt);
    put("tausEta", tausEta);
    put("tausPhi", tausPhi);
    put("tausPdg", tausPdg);
    put("tausisPF", tausisPF);
    put("tausByLooseCombinedIsolationDBSumPtCorr", tausByLooseCombinedIsolationDBSumPtCorr);
    put("tausDecayModeFinding", tausDecayModeFinding);
    put("tausAgainstMuonLoose", tausAgainstMuonLoose);
    put("tausAgainstElectronLoose", tausAgainstElectronLoose);
    put("taushasMCMatch", taushasMCMatch);
  }

  if (addJetVector_){
    edm::Handle< edm::View<pat::Jet > > patJets;
    ev.getByLabel( patJets_, patJets );
    JetIDSelectionFunctor jetPURE09LOOSE(JetIDSelectionFunctor::PURE09, JetIDSelectionFunctor::LOOSE );
    PFJetIDSelectionFunctor pfjetFIRSTDATALOOSE( PFJetIDSelectionFunctor::FIRSTDATA, PFJetIDSelectionFunctor::LOOSE );
    edm::ESHandle<JetCorrectorParametersCollection> JetCorParColl;
    setup.get<JetCorrectionsRecord>().get("AK5PF",JetCorParColl);
    JetCorrectorParameters const & JetCorPar = (*JetCorParColl)["Uncertainty"];
    JetCorrectionUncertainty *jecUnc = new JetCorrectionUncertainty(JetCorPar);
    edm::Handle<edm::ValueMap<int> > cutbasedPUJetIdFlag;
    ev.getByLabel(puJetIdCutBased_, cutbasedPUJetIdFlag);
    edm::Handle<edm::ValueMap<int> > full53XPUJetIdFlag;
    ev.getByLabel(puJetIdFull53X_,full53XPUJetIdFlag);
    edm::Handle<edm::ValueMap<int> > met53XPUJetIdFlag;
    ev.getByLabel(puJetIdMET53X_,met53XPUJetIdFlag);

    double delta_met_x (0.), delta_met_y(0.);
    double delta_met_x_unclustered (0.), delta_met_y_unclustered(0.);
    std::vector<float> jetspt, jetsptUncorr, jetseta, jetsbtag, jetsSVMass, jetsphi, jetsUnc, jetsMass2;
    std::vector<int> jetsparton, jetsID, jetsCutBasedPUJetIDFlag, jetsMET53XPUJetIDFlag, jetsFull53XPUJetIDFlag;

    std::vector<float> jetsChargedHadronEnergyFraction, jetsNeutralHadronEnergyFraction, jetsChargedEmEnergyFraction, jetsNeutralEmEnergyFraction, jetsPhotonEnergyFraction, jetsElectronEnergyFraction, jetsMuonEnergyFraction, jetsHFHadronEnergyFraction, jetsHFEMEnergyFraction;
    for (unsigned i = 0; i<patJets->size();i++) {
      const pat::Jet & patJet = patJets->at(i);
      bool jetID;
      if ( patJet.isPFJet() ) {
      //https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetID

        jetID = pfjetFIRSTDATALOOSE(patJet);

      } else {
        jetID = jetPURE09LOOSE(patJet);
      }

// bool jet_is_good = (jetID and (patJet.pt() >= minJetPt_) and (fabs( patJet.eta() ) <= maxJetEta_));
      bool jet_is_soft = (patJet.pt() >= softJetPtThreshold_);
      if (jet_is_soft) {
        jetspt.push_back(patJet.pt());
        jetsptUncorr.push_back(patJet.correctedJet("Uncorrected").pt());
        jetseta.push_back(patJet.eta());
        jetsphi.push_back(patJet.phi());
        jetsMass2.push_back(patJet.p4().mass2());
        if (!isData) {
          jetsparton.push_back(patJet.partonFlavour());
        } else {jetsparton.push_back(0);}
        jetsbtag.push_back(patJet.bDiscriminator(btag_));

        jetsCutBasedPUJetIDFlag.push_back((*cutbasedPUJetIdFlag)[patJets->refAt(i)]);
        jetsMET53XPUJetIDFlag.push_back((*met53XPUJetIdFlag)[patJets->refAt(i)]);
        jetsFull53XPUJetIDFlag.push_back((*full53XPUJetIdFlag)[patJets->refAt(i)]);
        const reco::SecondaryVertexTagInfo * SVtagInfo = patJet.tagInfoSecondaryVertex();
        bool hasSVMass(false);
        if(SVtagInfo){
          if(SVtagInfo->nVertices()>0){
            const reco::Vertex &SVertex=SVtagInfo->secondaryVertex(0);
            jetsSVMass.push_back(SVertex.p4().M());
            hasSVMass = true;
          }
        }
        if (not hasSVMass) jetsSVMass.push_back(-1.);

        jecUnc->setJetEta(patJet.eta());
        jecUnc->setJetPt(patJet.pt()); // here you must use the CORRECTED jet pt
        double unc = (patJet.pt() > 10. && fabs(patJet.eta())<5.) ? jecUnc->getUncertainty(true) : 0.1;
        jetsUnc.push_back(unc);
        jetsID.push_back(jetID);
        jetsChargedHadronEnergyFraction.push_back(patJet.chargedHadronEnergyFraction());
        jetsNeutralHadronEnergyFraction.push_back(patJet.neutralHadronEnergyFraction());
        jetsChargedEmEnergyFraction.push_back(patJet.chargedEmEnergyFraction());
        jetsNeutralEmEnergyFraction.push_back(patJet.neutralEmEnergyFraction());
        jetsPhotonEnergyFraction.push_back(patJet.photonEnergyFraction());
        jetsElectronEnergyFraction.push_back(patJet.electronEnergyFraction());
        jetsMuonEnergyFraction.push_back(patJet.muonEnergyFraction());
        jetsHFHadronEnergyFraction.push_back(patJet.HFHadronEnergyFraction());
        jetsHFEMEnergyFraction.push_back(patJet.HFEMEnergyFraction());
      }
      
      if ((verbose_) and (patJet.pt() > softJetPtThreshold_)) cout<<"[jet "<<i<<"] "<<" pt "<<patJet.pt()<<" eta "<<patJet.eta()<<" phi "<<patJet.phi()<<boolalpha<<" jetID? "<<jetID<<endl;//" jetID+pt+eta cut?"<< jet_is_good <<endl;//" passes Ele c.c? "<<jetPassesEleCleaning<<" passes Mu c.c? "<<jetPassesMuCleaning<<endl;
      jecUnc->setJetEta(patJet.eta());
      jecUnc->setJetPt(patJet.pt()); // here you must use the CORRECTED jet pt
      double unc = (patJet.pt() > 10. && fabs(patJet.eta()<5)) ? jecUnc->getUncertainty(true) : 0.1;
      pat::Jet scaledJet = patJet;
      scaledJet.scaleEnergy(1+unc);
      delta_met_x += - scaledJet.px() + patJet.px();
      delta_met_y += - scaledJet.py() + patJet.py();
      if (patJet.pt()<10.) {
        delta_met_x_unclustered += - scaledJet.px() + patJet.px();
        delta_met_y_unclustered += - scaledJet.py() + patJet.py();
      }
    }
    put("jetsPt", jetspt);
    put("jetsPtUncorr", jetsptUncorr);
    put("jetsEta", jetseta);
    put("jetsPhi", jetsphi);
    put("jetsMass2", jetsMass2);
    put("jetsParton", jetsparton);
    put("jetsBtag", jetsbtag);
    put("jetsSVMass", jetsSVMass);
    put("jetsUnc", jetsUnc);
    put("jetsID", jetsID);
    put("jetsCutBasedPUJetIDFlag", jetsCutBasedPUJetIDFlag);
    put("jetsMET53XPUJetIDFlag", jetsMET53XPUJetIDFlag);
    put("jetsFull53XPUJetIDFlag", jetsFull53XPUJetIDFlag);
    put("jetsChargedHadronEnergyFraction", jetsChargedHadronEnergyFraction);
    put("jetsNeutralHadronEnergyFraction", jetsNeutralHadronEnergyFraction);
    put("jetsChargedEmEnergyFraction", jetsChargedEmEnergyFraction);
    put("jetsNeutralEmEnergyFraction", jetsNeutralEmEnergyFraction);
    put("jetsPhotonEnergyFraction", jetsPhotonEnergyFraction);
    put("jetsElectronEnergyFraction", jetsElectronEnergyFraction);
    put("jetsMuonEnergyFraction", jetsMuonEnergyFraction);
    put("jetsHFHadronEnergyFraction", jetsHFHadronEnergyFraction);
    put("jetsHFEMEnergyFraction", jetsHFEMEnergyFraction);

    put("nsoftjets", jetspt.size());
    put("deltaMETx", delta_met_x);
    put("deltaMETy", delta_met_y);
    put("deltaMETxUnclustered", delta_met_x_unclustered);
    put("deltaMETyUnclustered", delta_met_y_unclustered);
    delete jecUnc;
  }

  edm::Handle<reco::GenMETCollection> genmet;
  if (ev.getByLabel("genMetTrue", genmet) && genmet->size() > 0) {
    put("genmetpx", genmet->front().px());
    put("genmetpy", genmet->front().py());
    put("genmet", genmet->front().pt());
    put("genmetphi", genmet->front().phi());
  }
  
  if (addMSugraOSETInfo_) {
    put("osetMgl", modelParameters_.get ( "mgl", ev ));
    put("osetMsq", modelParameters_.get ( "msq", ev ));
    put("osetMC", modelParameters_.get ( "mC", ev ));
    put("osetMN", modelParameters_.get ( "mN", ev ));

    edm::InputTag genParticleTag = edm::InputTag("genParticles");
    edm::Handle< vector< reco::GenParticle > > genParticleHandle;
    try {
      ev.getByLabel(genParticleTag, genParticleHandle );
      if (!genParticleHandle.isValid() || genParticleHandle.failedToGet()) {
  // if (verbose_) cout << prefix << "GenParticles not valid!." << endl;
      }
    } catch (exception & e) {
      cout << prefix << "error (GenParticles): " << e.what() << endl;
    }

    vector< const reco::GenParticle *> gluinos;
    if ( genParticleHandle.isValid() and (!genParticleHandle.failedToGet())) {
      for( unsigned i = 0; i < genParticleHandle->size(); i++ ) {
        if (((*genParticleHandle)[i].pdgId() == 1000021) && ( (*genParticleHandle)[i].status() == 3)) gluinos.push_back( &( (*genParticleHandle)[i] ));
      }
    }
    std::vector<int> selectedIds;
    for (unsigned int i=0; i<genParticleHandle->size(); ++i) {
      const reco::GenParticle& p = (*genParticleHandle)[i];
       if (p.status() != 3) continue;
       if (abs(p.pdgId()) < 1000000) continue;

       bool hasSMMother(true);
       for (unsigned int j=0; j<p.numberOfMothers(); ++j) {
         if ( !(abs(p.mother(j)->pdgId())<1000000) ) {
           hasSMMother = false;
           break;
         }
       }
       if ( hasSMMother ) selectedIds.push_back(p.pdgId());
    }
    sort(selectedIds.begin(),selectedIds.end());
    put("sparticles", selectedIds);
    if (gluinos.size()>0) {
      put("gluino0Pt", gluinos[0]->pt());
      put("gluino0Eta", gluinos[0]->eta());
      put("gluino0Phi", gluinos[0]->phi());
      put("gluino0Pdg", gluinos[0]->pdgId());
    }
    if (gluinos.size()>1) {
      put("gluino1Pt", gluinos[1]->pt());
      put("gluino1Eta", gluinos[1]->eta());
      put("gluino1Phi", gluinos[1]->phi());
      put("gluino1Pdg", gluinos[1]->pdgId());
    }
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

void SUSYTupelizer::addAllVars( )
{
  if(addMuonVector_)
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
  if(addEleVector_)
  {
    addVar("neles/I");
    addVar("elesPt/F[]");
    addVar("elesEta/F[]");
    addVar("elesPhi/F[]");
    addVar("elesPdg/I[]");
    addVar("elesOneOverEMinusOneOverP/F[]");
    addVar("elesPfRelIso/F[]");
    addVar("eles03ChargedHadronIso/F[]");
    addVar("eles03NeutralHadronIso/F[]");
    addVar("eles03GammaIso/F[]");
    addVar("elesAeff/F[]");
    addVar("elesSigmaIEtaIEta/F[]");
    addVar("elesHoE/F[]");
    addVar("elesDPhi/F[]");
    addVar("elesDEta/F[]");
    addVar("elesMissingHits/I[]");
    addVar("elesDxy/F[]");
    addVar("elesDz/F[]");
    addVar("elesPassConversionRejection/I[]");
    addVar("elesPassPATConversionVeto/I[]");
  }
  if (addFullTauInfo_) {
    addVar("ntaus/I");
    addVar("tausPt/F[]");
    addVar("tausEta/F[]");
    addVar("tausPhi/F[]");
    addVar("tausPdg/I[]");
    addVar("taushasMCMatch/I[]");
    addVar("tausisPF/I[]");
    addVar("tausByLooseCombinedIsolationDBSumPtCorr/I[]");
    addVar("tausDecayModeFinding/I[]");
    addVar("tausAgainstMuonLoose/I[]");
    addVar("tausAgainstElectronLoose/I[]");
  }
  if (addJetVector_){
    addVar("jetsPt/F[]");
    addVar("jetsPtUncorr/F[]");
    addVar("jetsEta/F[]");
    addVar("jetsPhi/F[]");
    addVar("jetsMass2/F[]");
    addVar("jetsParton/I[]");
    addVar("jetsBtag/F[]");
    addVar("jetsSVMass/F[]");
    addVar("jetsUnc/F[]");
// addVar("jetsEleCleaned/I[]");
// addVar("jetsMuCleaned/I[]");
    addVar("jetsCutBasedPUJetIDFlag/I[]");
    addVar("jetsMET53XPUJetIDFlag/I[]");
    addVar("jetsFull53XPUJetIDFlag/I[]");
    addVar("jetsID/I[]");
    addVar("jetsChargedHadronEnergyFraction/F[]");
    addVar("jetsNeutralHadronEnergyFraction/F[]");
    addVar("jetsChargedEmEnergyFraction/F[]");
    addVar("jetsNeutralEmEnergyFraction/F[]");
    addVar("jetsPhotonEnergyFraction/F[]");
    addVar("jetsElectronEnergyFraction/F[]");
    addVar("jetsMuonEnergyFraction/F[]");
    addVar("jetsHFHadronEnergyFraction/F[]");
    addVar("jetsHFEMEnergyFraction/F[]");
    addVar("nsoftjets/I"); // NAN);
    addVar("deltaMETx/F");
    addVar("deltaMETy/F");
    addVar("deltaMETxUnclustered/F");
    addVar("deltaMETyUnclustered/F");
  }
  if(addMetUncertaintyInfo_) {
    for (std::vector<std::string>::iterator s = metsToMonitor_.begin(); s != metsToMonitor_.end(); s++) {
      std::string metName = *s;
      addVar(metName+"/F");
      addVar(metName+"phi/F");
      addVar(metName+"sumEt/F");
    }
  }

  addVar("event/l"); // 0);
  addVar("run/I"); // NAN);
  addVar("lumi/I"); // NAN);
  addVar("bx/I"); // NAN);
  addVar("isMC/O"); // NAN);
  addVar("ngenVertices/I"); // -1);
  addVar("nTrueGenVertices/F"); // -1);

  addVar("flavorHistory/i"); // 0);
  addVar("ngoodVertices/I"); // -1);

  addVar("eleRho/F");


  addVar("genmetpx/F"); // NAN);
  addVar("genmetpy/F"); // NAN);
  addVar("genmet/F"); // NAN);
  addVar("genmetphi/F"); // NAN);

  if (addMSugraOSETInfo_) {
    addVar("sparticles/I[]");
    addVar("gluino0Pt/F");
    addVar("gluino0Eta/F");
    addVar("gluino0Phi/F");
    addVar("gluino0Pdg/I");
    addVar("gluino1Pt/F");
    addVar("gluino1Eta/F");
    addVar("gluino1Phi/F");
    addVar("gluino1Pdg/I");
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

DEFINE_FWK_MODULE(SUSYTupelizer);
