#include "FWCore/Framework/interface/MakerMacros.h"
#include "Workspace/HEPHYCommonTools/plugins/SUSYTupelizer.h"
#include "Workspace/HEPHYCommonTools/interface/EdmHelper.h"
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
//#include "CMGTools/External/interface/PileupJetIdentifier.h"
#include "DataFormats/JetReco/interface/PileupJetIdentifier.h"
#include "DataFormats/METReco/interface/GenMET.h"
#include "DataFormats/METReco/interface/GenMETCollection.h"
#include "DataFormats/METReco/interface/PFMET.h"
#include "DataFormats/PatCandidates/interface/TriggerEvent.h"
#include "Workspace/HEPHYCommonTools/interface/ElectronEffectiveArea.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "JetMETCorrections/Objects/interface/JetCorrectionsRecord.h"
#include "PhysicsTools/PatAlgos/plugins/PATElectronProducer.h"
#include "PhysicsTools/SelectorUtils/interface/PFJetIDSelectionFunctor.h"
#include "RecoEgamma/EgammaTools/interface/ConversionTools.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
//#include "ElectroWeakAnalysis/Utilities/src/PdfWeightProducer.cc"

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

  double getDeltaPt(const math::XYZTLorentzVector & p4,  const reco::PFCandidateCollection & pfCands, reco::PFCandidate::ParticleType t ) {
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
    if (p->status()!=3)     return false;
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
  params_ ( pset ),
  verbose_      ( pset.getUntrackedParameter< bool >("verbose")),
  triggerCollection_ ( pset.getUntrackedParameter< std::string >("triggerCollection") ),
  patJets_      ( pset.getUntrackedParameter< edm::InputTag >("patJets") ),
  patMET_       ( pset.getUntrackedParameter< edm::InputTag >("patMETs") ),
//  rawMET_       ( pset.getUntrackedParameter< edm::InputTag >("rawMETs") ),
//  type01MET_       ( pset.getUntrackedParameter< edm::InputTag >("type01METs") ),
//  type1phiMET_       ( pset.getUntrackedParameter< edm::InputTag >("type1phiMETs") ),
//  type01phiMET_       ( pset.getUntrackedParameter< edm::InputTag >("type01phiMETs") ),

  patMuons_     ( pset.getUntrackedParameter< edm::InputTag >("patMuons") ),
  patElectrons_ ( pset.getUntrackedParameter< edm::InputTag >("patElectrons") ),
  patTaus_ ( pset.getUntrackedParameter< edm::InputTag >("patTaus") ),

  vertices_ ( pset.getUntrackedParameter< edm::InputTag >("vertices") ),
  lowLeptonPtThreshold_ (pset.getUntrackedParameter< double >("lowLeptonPtThreshold") ),
  softJetPtThreshold_ (pset.getUntrackedParameter< double >("softJetPtThreshold") ),

  muonPt_ (pset.getUntrackedParameter< double >("muonPt") ),
  muonEta_ (pset.getUntrackedParameter< double >("muonEta") ),
  muonIsGlobal_ (pset.getUntrackedParameter< bool >("muonIsGlobal") ),
  muonHasPFMatch_ (pset.getUntrackedParameter< bool >("muonHasPFMatch") ),
  muonIsPF_ (pset.getUntrackedParameter< bool >("muonIsPF") ),
  muonNormChi2_ (pset.getUntrackedParameter< double >("muonNormChi2") ),
  muonNumValMuonHits_ (pset.getUntrackedParameter< int >("muonNumValMuonHits") ),
  muonNumMatchedStations_ (pset.getUntrackedParameter< int >("muonNumMatchedStations") ),
  muonNumPixelHits_ (pset.getUntrackedParameter< int >("muonNumPixelHits") ),
  muonNumTrackerLayersWithMeasurement_ (pset.getUntrackedParameter< int >("muonNumTrackerLayersWithMeasurement") ),
  muonPFRelIso_ (pset.getUntrackedParameter< double >("muonPFRelIso") ),
  muonPFRelIsoDeltaBeta_ (pset.getUntrackedParameter< bool >("muonPFRelIsoDeltaBeta") ),
  muonDxy_ (pset.getUntrackedParameter< double >("muonDxy") ),
  muonDz_ (pset.getUntrackedParameter< double >("muonDz") ),

  vetoMuonPt_ (pset.getUntrackedParameter< double >("vetoMuonPt") ),
  vetoMuonEta_ (pset.getUntrackedParameter< double >("vetoMuonEta") ),
  vetoMuonIsGlobalOrIsTracker_ (pset.getUntrackedParameter< bool >("vetoMuonIsGlobalOrIsTracker") ),
  vetoMuonIsPF_ (pset.getUntrackedParameter< bool >("vetoMuonIsPF") ),
  vetoMuonPFRelIso_ (pset.getUntrackedParameter< double >("vetoMuonPFRelIso") ),
  vetoMuonPFRelIsoDeltaBeta_ (pset.getUntrackedParameter< bool >("vetoMuonPFRelIsoDeltaBeta") ),
  vetoMuonDxy_ (pset.getUntrackedParameter< double >("vetoMuonDxy") ),
  vetoMuonDz_ (pset.getUntrackedParameter< double >("vetoMuonDz") ),
  // steerables Ele:
  elePt_ ( pset.getUntrackedParameter< double >("elePt") ),
  eleEta_ (pset.getUntrackedParameter< double >("eleEta") ),
  eleOneOverEMinusOneOverP_ ( pset.getUntrackedParameter< double >("eleOneOverEMinusOneOverP") ),
  eleDxy_ ( pset.getUntrackedParameter< double >("eleDxy") ),
  eleDz_ ( pset.getUntrackedParameter< double >("eleDz") ),
  elePFRelIsoBarrel_ ( pset.getUntrackedParameter< double >("elePFRelIsoBarrel") ),
  elePFRelIsoEndcap_ ( pset.getUntrackedParameter< double >("elePFRelIsoEndcap") ),
  elePFRelIsoAreaCorrected_ ( pset.getUntrackedParameter< bool   >("elePFRelIsoAreaCorrected") ),
  eleRho_ ( pset.getUntrackedParameter< edm::InputTag  >("eleRho") ),
  eleSigmaIEtaIEtaBarrel_ ( pset.getUntrackedParameter< double >("eleSigmaIEtaIEtaBarrel") ),
  eleSigmaIEtaIEtaEndcap_ ( pset.getUntrackedParameter< double >("eleSigmaIEtaIEtaEndcap") ),
  eleHoEBarrel_ ( pset.getUntrackedParameter< double >("eleHoEBarrel") ),
  eleHoEEndcap_ ( pset.getUntrackedParameter< double >("eleHoEEndcap") ),
  eleDPhiBarrel_ ( pset.getUntrackedParameter< double >("eleDPhiBarrel") ),
  eleDPhiEndcap_ ( pset.getUntrackedParameter< double >("eleDPhiEndcap") ),
  eleDEtaBarrel_ ( pset.getUntrackedParameter< double >("eleDEtaBarrel") ),
  eleDEtaEndcap_ ( pset.getUntrackedParameter< double >("eleDEtaEndcap") ),
  eleMissingHits_ ( pset.getUntrackedParameter< int    >("eleMissingHits") ),
  eleConversionRejection_ ( pset.getUntrackedParameter< bool >("eleConversionRejection") ),
  eleHasPFMatch_ (pset.getUntrackedParameter< bool >("eleHasPFMatch") ),
  // steerables veto Ele:
  vetoElePt_ ( pset.getUntrackedParameter< double >("vetoElePt") ),
  vetoEleEta_ (pset.getUntrackedParameter< double >("vetoEleEta") ),
  vetoEleDxy_ ( pset.getUntrackedParameter< double >("vetoEleDxy") ),
  vetoEleDz_ ( pset.getUntrackedParameter< double >("vetoEleDz") ),
  vetoElePFRelIsoBarrel_ ( pset.getUntrackedParameter< double >("vetoElePFRelIsoBarrel") ),
  vetoElePFRelIsoEndcap_ ( pset.getUntrackedParameter< double >("vetoElePFRelIsoEndcap") ),
  vetoEleSigmaIEtaIEtaBarrel_ ( pset.getUntrackedParameter< double >("vetoEleSigmaIEtaIEtaBarrel") ),
  vetoEleSigmaIEtaIEtaEndcap_ ( pset.getUntrackedParameter< double >("vetoEleSigmaIEtaIEtaEndcap") ),
  vetoEleHoEBarrel_ ( pset.getUntrackedParameter< double >("vetoEleHoEBarrel") ),
  vetoEleHoEEndcap_ ( pset.getUntrackedParameter< double >("vetoEleHoEEndcap") ),
  vetoEleDPhiBarrel_ ( pset.getUntrackedParameter< double >("vetoEleDPhiBarrel") ),
  vetoEleDPhiEndcap_ ( pset.getUntrackedParameter< double >("vetoEleDPhiEndcap") ),
  vetoEleDEtaBarrel_ ( pset.getUntrackedParameter< double >("vetoEleDEtaBarrel") ),
  vetoEleDEtaEndcap_ ( pset.getUntrackedParameter< double >("vetoEleDEtaEndcap") ),

  minJetPt_     ( pset.getUntrackedParameter< double >("minJetPt") ),
  maxJetEta_    ( pset.getUntrackedParameter< double >("maxJetEta") ),
  btag_         ( pset.getUntrackedParameter< std::string >("btag") ),
  btagWP_       ( pset.getUntrackedParameter< double >("btagWP") ),
  btagPure_     ( pset.getUntrackedParameter< std::string >("btagPure") ),
  btagPureWP_       ( pset.getUntrackedParameter< double >("btagPureWP") ),
  hasL1Trigger_ ( pset.getUntrackedParameter< bool >("hasL1Trigger") ),
  puJetIdCutBased_( pset.getUntrackedParameter< edm::InputTag >("puJetIdCutBased") ),
  puJetIdFull53X_( pset.getUntrackedParameter< edm::InputTag >("puJetIdFull53X") ),
  puJetIdMET53X_( pset.getUntrackedParameter< edm::InputTag >("puJetIdMET53X") ),

  moduleLabel_( params_.getParameter<std::string>("@module_label") ),
  addRA4AnalysisInfo_( pset.getUntrackedParameter<bool>("addRA4AnalysisInfo")),
  addTriggerInfo_(pset.getUntrackedParameter<bool>("addTriggerInfo")),
  triggersToMonitor_(pset.getUntrackedParameter<std::vector<std::string> > ("triggersToMonitor") ), 
  metsToMonitor_(pset.getUntrackedParameter<std::vector<std::string> > ("metsToMonitor") ), 
  addMetUncertaintyInfo_(pset.getUntrackedParameter<bool>("addMetUncertaintyInfo")),
  addFullBTagInfo_(pset.getUntrackedParameter<bool>("addFullBTagInfo")),
  addFullJetInfo_(pset.getUntrackedParameter<bool>("addFullJetInfo")),
  addFullLeptonInfo_(pset.getUntrackedParameter<bool>("addFullLeptonInfo")),
//  addFullMETInfo_(pset.getUntrackedParameter<bool>("addFullMETInfo")),
  addFullMuonInfo_(pset.getUntrackedParameter<bool>("addFullMuonInfo")),
  addFullEleInfo_(pset.getUntrackedParameter<bool>("addFullEleInfo")),
  addFullTauInfo_(pset.getUntrackedParameter<bool>("addFullTauInfo")),
  addGeneratorInfo_(pset.getUntrackedParameter<bool>("addGeneratorInfo")),
  addMSugraOSETInfo_(pset.getUntrackedParameter<bool>("addMSugraOSETInfo")),
  addPDFWeights_(pset.getUntrackedParameter<bool>("addPDFWeights")),

  defaultAlias_(pset.getUntrackedParameter<bool>("useForDefaultAlias"))

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
  if (hltConfig_.init(iRun,iSetup,triggerCollection_,changed)) {
  } else {
    edm::LogError(prefix) << " HLT config extraction failure with process name " << triggerCollection_;
  }
}

int SUSYTupelizer::prescale(edm::Event & ev, const edm::EventSetup & setup, std::string hlt) {
//  return prod(hltConfig_.prescaleValues( ev, setup, hlt.c_str()));
  return hltConfig_.prescaleValue( ev, setup, hlt.c_str());
}


void SUSYTupelizer::produce( edm::Event & ev, const edm::EventSetup & setup) {
  ev_ = &ev;
  int peng(0);
  put("event",ev.id().event());
  put("run",ev.id().run());
  put("lumi",ev.luminosityBlock());
  put("bx",ev.bunchCrossing());
  bool isData;
  isData=ev.eventAuxiliary().isRealData();
  put("isMC",!isData);
  
  if (!isData){
    edm::Handle<std::vector< PileupSummaryInfo > >  PupInfo;
    try {
      ev.getByLabel(edm::InputTag("addPileupInfo"), PupInfo);

//       if (!PupInfo.isValid() || PupInfo.failedToGet()) {
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

    edm::Handle<unsigned int >  flavHist;
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
  edm::InputTag HLTTag = edm::InputTag("TriggerResults", "", triggerCollection_.c_str());
  ev.getByLabel(HLTTag, HLTR);
  if (HLTR.isValid()) {
//    cout << "Init HLT info" << endl;
    edm::TriggerNames triggerNames =  ev.triggerNames(*HLTR);
    HLT_names_ = triggerNames.triggerNames();
    if (! this->hlt_initialized_ ) {
      cout<<"HLT: "<<triggerCollection_.c_str()<<endl;
      for (unsigned i=0;i<HLT_names_.size();i++) {
        cout<<HLT_names_[i]<<endl;
      }
      SUSYTupelizer::hlt_initialized_ = true;
    }
  }
  bool muonTriggerUnprescaled = false;
  bool electronTriggerUnprescaled = false;
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
    cout  << prefix << " error (BeamSpot): " << e.what() << endl;
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

/*  ____   _  _____   __  __
   |  _ \ / \|_   _| |  \/  |_   _  ___  _ __  ___
   | |_) / _ \ | |   | |\/| | | | |/ _ \| '_ \/ __|
   |  __/ ___ \| |   | |  | | |_| | (_) | | | \__ \
   |_| /_/   \_\_|   |_|  |_|\__,_|\___/|_| |_|___/
*/
  vector<pat::Muon> patMuons (EdmHelper::getObjs<pat::Muon> (ev, patMuons_));
  // Muon Selection
  vector<pat::Muon> good_muons, veto_muons;
  std::vector<float> muonsPt, muonsEta, muonsPhi, muonsPFRelIso, muonsNormChi2, muonsDxy, muonsDz, muonsPFDeltaPT, muonsIso03sumChargedHadronPt, muonsIso03sumNeutralHadronEt, muonsIso03sumPhotonEt, muonsIso03sumPUChargedHadronPt;
  std::vector<int>   muonsPdg,  muonsNValMuonHits, muonsNumMatchedStations, muonsPixelHits, muonsNumtrackerLayerWithMeasurement;
  std::vector<int>  muonsisPF, muonsisGlobal, muonsisTracker;
  int muonCounter=0;
  edm::Handle<reco::PFCandidateCollection> pfCandidates;
  ev.getByLabel("particleFlow",pfCandidates);
  reco::PFCandidateCollection pfCands = *pfCandidates;

  if (verbose_) cout<<"\nrun "<< ev.id().run()<<" lumi "<<ev.luminosityBlock()<<" event "<<ev.id().event()<<endl;
  if (verbose_) cout<<"vertex: x "<<goodVertices[0].x()<<" y "<<goodVertices[0].y()<<" z "<<goodVertices[0].z()<<" rho "<<goodVertices[0].position().rho()<<" ndof "<<goodVertices[0].ndof()<< endl;

  for (vector<pat::Muon>::const_iterator muon = patMuons.begin(); muon!=patMuons.end();muon++){

    bool isGlobal      = muon->isGlobalMuon();
    bool isPF          = muon->isPFMuon();
    bool isTracker     = muon->isTrackerMuon();
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
      dz =  fabs(muon->innerTrack()->dz(vertexPosition));
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
    double deltapT = getDeltaPt(muon->p4(), pfCands, reco::PFCandidate::mu);
    bool hasPFMatch = (deltapT<5.);
    //construct muon collection for vetoing
    bool isGoodVeto =  ( (muon->pt() >= vetoMuonPt_) &&
       (isPF || !vetoMuonIsPF_) && ( (isGlobal || isTracker ) || !vetoMuonIsGlobalOrIsTracker_) &&
       (fabs(muon->eta()) <= vetoMuonEta_) &&
       (pfRelIso < vetoMuonPFRelIso_ ) &&
       (dxy < vetoMuonDxy_) &&
       (dz < vetoMuonDz_));
    if (isGoodVeto) veto_muons.push_back(*muon);
    bool isGood =  ( (muon->pt() >= muonPt_ ) &&
       (fabs(muon->eta()) <= muonEta_) &&
       (isPF || !muonIsPF_) &&  (isGlobal || !muonIsGlobal_) &&
       (hasPFMatch || !muonHasPFMatch_) && 
       (pfRelIso < muonPFRelIso_ ) &&
       (normChi2 <= muonNormChi2_) &&
       (nValMuonHits > muonNumValMuonHits_) &&
       (numMatchedStations > muonNumMatchedStations_) &&
       (pixelHits > muonNumPixelHits_) &&
       (numTrackerLayersWithMeasurement > muonNumTrackerLayersWithMeasurement_) &&
       (dxy < muonDxy_) &&
       (dz < muonDz_));
    if (isGood) good_muons.push_back(*muon);

    if(addFullMuonInfo_ and (muon->pt() >= lowLeptonPtThreshold_)) {
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
        muonsPFDeltaPT.push_back(deltapT);
    }
    if (verbose_) {
      cout<<"[muon "<< muon - patMuons.begin()<<boolalpha<<"] isGood? "<<isGood<<" isGoodVeto "<<isGoodVeto<<endl;
      cout<<"         pt "<<muon->pt()<<" eta "<<muon->eta()<<" phi "<<muon->phi()<<" isPF "<<isPF<<" isGlobal "<<isGlobal <<" isTracker "<<isTracker<<" pfRelIso "<<pfRelIso<<" normChi2 "<<normChi2<<" pfDeltaPT "<< deltapT<<endl;
      cout<<"         nValMuonHits "<<nValMuonHits<<" numMatchedStations "<<numMatchedStations<<" pixelHits "<<pixelHits<<" numTrackerLayersWithMeasurement "<<numTrackerLayersWithMeasurement<<" dxy "<<dxy<<" dz "<<dz<<endl;
      cout<<"         chargedHadronIso "<<muon->pfIsolationR03().sumChargedHadronPt<<" neutralHadronIso "<<muon->pfIsolationR03().sumNeutralHadronEt<<" gammaIso "<< muon->pfIsolationR03().sumPhotonEt<<" chargedPUIso "<<muon->pfIsolationR03().sumPUPt<<" doDeltaBeta "<<muonPFRelIsoDeltaBeta_<<endl;
      cout<<"         ecalIso "<<muon->ecalIso()<<" hcalIso "<<muon->hcalIso()<<" trackIso "<<muon->trackIso()<<endl;
    }
  }

  if(addFullMuonInfo_){
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
    put("muonsPFDeltaPT",muonsPFDeltaPT);
  }
  if (addRA4AnalysisInfo_) {
    sort(good_muons.begin(), good_muons.end(), MathHelper::greaterPt<pat::Muon> );
    put("ngoodMuons", good_muons.size());
    sort(veto_muons.begin(), veto_muons.end(), MathHelper::greaterPt<pat::Muon> );
    put("nvetoMuons", veto_muons.size());
  }
  
/*  ____   _  _____   _____ _           _
   |  _ \ / \|_   _| | ____| | ___  ___| |_ _ __ ___  _ __  ___
   | |_) / _ \ | |   |  _| | |/ _ \/ __| __| '__/ _ \| '_ \/ __|
   |  __/ ___ \| |   | |___| |  __/ (__| |_| | | (_) | | | \__ \
   |_| /_/   \_\_|   |_____|_|\___|\___|\__|_|  \___/|_| |_|___/
*/
  vector<pat::Electron> patElectrons (EdmHelper::getObjs<pat::Electron>(ev,  patElectrons_));
  vector<pat::Electron> veto_electrons, good_electrons;
  edm::Handle<reco::ConversionCollection> hConversions;
  ev.getByLabel("allConversions", hConversions);
  edm::Handle<double> eleRho;
  ev.getByLabel(eleRho_, eleRho);
  put("eleRho", *eleRho);
  std::vector<float> elesPt, elesEta, elesPhi, elesAeff, eles03ChargedHadronIso, eles03NeutralHadronIso, eles03GammaIso, elesOneOverEMinusOneOverP, elesPfRelIso, elesSigmaIEtaIEta, elesHoE, elesDPhi, elesDEta, elesDxy, elesDz, elesPFDeltaPT;

  std::vector<int> elesPdg, elesMissingHits;
  std::vector<int> elesPassConversionRejection, elesPassPATConversionVeto;
  int eleCounter=0;

//   //electron PFiso variables
  typedef std::vector< edm::Handle< edm::ValueMap<reco::IsoDeposit> > > IsoDepositMaps;
  typedef std::vector< edm::Handle< edm::ValueMap<double> > > IsoDepositVals;
  IsoDepositVals electronIsoValPFId(3);
  const IsoDepositVals * electronIsoVals = &electronIsoValPFId;
  ev.getByLabel("elPFIsoValueCharged03PFIdPFIso", electronIsoValPFId[0]);
  ev.getByLabel("elPFIsoValueGamma03PFIdPFIso", electronIsoValPFId[1]);
  ev.getByLabel("elPFIsoValueNeutral03PFIdPFIso", electronIsoValPFId[2]); 

//  IsoDepositVals electronIsoValPFId04(3);
//  const IsoDepositVals * electronIsoVals04 = &electronIsoValPFId04;
//  ev.getByLabel("elPFIsoValueCharged04PFIdPFIso", electronIsoValPFId[0]);
//  ev.getByLabel("elPFIsoValueGamma04PFIdPFIso", electronIsoValPFId[1]);
//  ev.getByLabel("elPFIsoValueNeutral04PFIdPFIso", electronIsoValPFId[2]); 

  for (vector<pat::Electron>::const_iterator ele = patElectrons.begin(); ele!=patElectrons.end();ele++){
    double pt            = ele->pt();
    double eta           = fabs(ele->superCluster()->eta());
    bool isBarrel        = ele->isEB();//(eta < 1.4442); 
    bool isEndcap        = ele->isEE();//((eta>1.566) and (eta<2.5)); 
    double oneOverEMinusOneOverP = fabs(1./ele->ecalEnergy() - 1./ele->trackMomentumAtVtx().R());
    double sigmaIEtaIEta = ele->scSigmaIEtaIEta();
    double HoE = ele->hadronicOverEm();
    double DPhi = fabs(ele->deltaPhiSuperClusterTrackAtVtx());
    double DEta = fabs(ele->deltaEtaSuperClusterTrackAtVtx());
    double dxy(NAN), dz(NAN);
    int missingHits(999);
    if (!ele->gsfTrack().isNull()){
      dxy = fabs(ele->gsfTrack()->dxy(vertexPosition));
      dz =  fabs(ele->gsfTrack()->dz(vertexPosition));
      missingHits = ele->gsfTrack()->trackerExpectedHitsInner().numberOfHits();
    }

    // UCSB accessors via dicts
    //get PF isolation
    edm::Ptr< reco::GsfElectron > gsfel = (edm::Ptr< reco::GsfElectron >) ele->originalObjectRef();
    bool passConversionRejection = gsfel.isNull() ? false : !ConversionTools::hasMatchedConversion(*gsfel,hConversions,beamSpotPosition);
    double charged =  (*(*electronIsoVals)[0])[gsfel];
    double photon = (*(*electronIsoVals)[1])[gsfel];
    double neutral = (*(*electronIsoVals)[2])[gsfel];
    //cout<<charged<<" "<<photon<<" "<<neutral<<endl;
    
    double Aeff= isData ? ElectronEffectiveArea::GetElectronEffectiveArea(ElectronEffectiveArea::kEleGammaAndNeutralHadronIso03, eta, ElectronEffectiveArea::kEleEAData2011):
                   ElectronEffectiveArea::GetElectronEffectiveArea(ElectronEffectiveArea::kEleGammaAndNeutralHadronIso03, eta, ElectronEffectiveArea::kEleEAFall11MC);

    double pfRelIso = elePFRelIsoAreaCorrected_?( charged + max (0., photon + neutral - (*eleRho)*Aeff) ) / pt : ( charged +  photon + neutral ) / pt;

    double deltapT = getDeltaPt(ele->p4(), pfCands, reco::PFCandidate::e);
    bool hasPFMatch = (deltapT<10.);

    bool isGood =  ( ( pt >= elePt_ ) && (eta <= eleEta_) && (isBarrel||isEndcap) &&
       (oneOverEMinusOneOverP < eleOneOverEMinusOneOverP_) &&
       (  (isBarrel && (pfRelIso < elePFRelIsoBarrel_)) || (isEndcap && (pfRelIso < elePFRelIsoEndcap_)) ) &&
       (  (isBarrel && (sigmaIEtaIEta < eleSigmaIEtaIEtaBarrel_)) || (isEndcap && (sigmaIEtaIEta < eleSigmaIEtaIEtaEndcap_)) ) &&
       (  (isBarrel && (HoE < eleHoEBarrel_)) || (isEndcap && (HoE < eleHoEEndcap_)) ) &&
       (  (isBarrel && (DPhi < eleDPhiBarrel_)) || (isEndcap && (DPhi < eleDPhiEndcap_)) ) &&
       (  (isBarrel && (DEta < eleDEtaBarrel_)) || (isEndcap && (DEta < eleDEtaEndcap_)) ) &&
       ( hasPFMatch || !eleHasPFMatch_ ) && 
       ( missingHits <= eleMissingHits_ ) &&
       ( dxy < eleDxy_ ) &&
       ( dz < eleDz_ ) &&
       ( passConversionRejection || !eleConversionRejection_)); 
    if (isGood ) good_electrons.push_back(*ele);

    bool isGoodVeto =  ( ( pt >= vetoElePt_ )  && (eta < vetoEleEta_) && (isBarrel||isEndcap) &&
       (  (isBarrel && (pfRelIso < vetoElePFRelIsoBarrel_)) || (isEndcap && (pfRelIso < vetoElePFRelIsoEndcap_)) ) &&
       (  (isBarrel && (sigmaIEtaIEta < vetoEleSigmaIEtaIEtaBarrel_)) || (isEndcap && (sigmaIEtaIEta < vetoEleSigmaIEtaIEtaEndcap_)) ) &&
       (  (isBarrel && (HoE < vetoEleHoEBarrel_)) || (isEndcap && ( (HoE < vetoEleHoEEndcap_) || vetoEleHoEEndcap_ < 0.)) ) &&
       (  (isBarrel && (DPhi < vetoEleDPhiBarrel_)) || (isEndcap && (DPhi < vetoEleDPhiEndcap_)) ) &&
       (  (isBarrel && (DEta < vetoEleDEtaBarrel_)) || (isEndcap && (DEta < vetoEleDEtaEndcap_)) ) && 
       (dxy < vetoEleDxy_) &&
       (dz < vetoEleDz_) ); 
    if (isGoodVeto) veto_electrons.push_back(*ele);
    if (verbose_) {
      cout<<"[ele "<< ele - patElectrons.begin()<<"] "<<boolalpha<<"isBarrel? "<<isBarrel<<" isEndcap? "<<isEndcap<<" isGood "<<isGood<<" isGoodVeto "<<isGoodVeto<<endl;
      cout<<"        pt "<<ele->pt()<<" eta "<<ele->superCluster()->eta()<<" phi "<<ele->phi()<<" oneOverEMinusOneOverP "<<oneOverEMinusOneOverP<<" sigmaIEtaIEta "<<sigmaIEtaIEta <<" pfRelIso "<<pfRelIso<<" HoE "<<HoE<<endl;
      cout<<"        DPhi "<<DPhi<<" DEta "<<DEta<<" missingHits "<<missingHits<<" passConversionRejection "<<passConversionRejection<<" dxy "<<dxy<<" dz "<<dz<<" pfDeltaPT "<<deltapT<<endl;
      cout<<"        chargedHadronIso03 "<<charged<<" neutralHadronIso03 "<<neutral<<" gammaIso03 "<< photon<<" Aeff "<<Aeff<<" rho "<<*eleRho<<endl;
      cout<<"        ecalIso "<<ele->ecalIso()<<" hcalIso "<<ele->hcalIso()<<" trackIso "<<ele->trackIso()<<endl;
    }
    if((addFullEleInfo_) and (pt > lowLeptonPtThreshold_)) //j#
    {
        eleCounter++;  // increment number of electrons in event
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
        elesPFDeltaPT.push_back(deltapT);
    }
  }

  if(addFullEleInfo_) {
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
    put("elesPFDeltaPT", elesPFDeltaPT);
  }

  sort(good_electrons.begin(), good_electrons.end(), MathHelper::greaterPt<pat::Electron> );
//  sort(good_electrons_fullID.begin(), good_electrons_fullID.end(), MathHelper::greaterPt<pat::Electron> );
  sort(veto_electrons.begin(), veto_electrons.end(), MathHelper::greaterPt<pat::Electron> );
  if (addRA4AnalysisInfo_) {
    put("ngoodElectrons", good_electrons.size());
    put("nvetoElectrons", veto_electrons.size());
 } 
// ____   _  _____   _____               
//|  _ \ / \|_   _| |_   _|_ _ _   _ ___ 
//| |_) / _ \ | |     | |/ _` | | | / __|
//|  __/ ___ \| |     | | (_| | |_| \__ \
//|_| /_/   \_\_|     |_|\__,_|\__,_|___/

  if (addFullTauInfo_) {
    vector<pat::Tau> patTaus (EdmHelper::getObjs<pat::Tau>(ev,  patTaus_));
    int ntaus(0);
    std::vector<int> tausPdg, tausisPF, taushasMCMatch, tausByLooseCombinedIsolationDBSumPtCorr, tausDecayModeFinding, tausAgainstMuonLoose, tausAgainstElectronLoose;
    std::vector<float> tausPt, tausEta, tausPhi;
    for (unsigned i = 0; i<patTaus.size();i++) {
      int byLooseCombinedIsolationDeltaBetaCorr = patTaus[i].tauID("byLooseCombinedIsolationDeltaBetaCorr");
      int decayModeFinding = patTaus[i].tauID("decayModeFinding");
      int againstMuonLoose = patTaus[i].tauID("againstMuonLoose");
      int againstElectronLoose = patTaus[i].tauID("againstElectronLoose");
//      if (patTaus[i].pt()>10. && (byLooseCombinedIsolationDeltaBetaCorr&&decayModeFinding&&againstMuonLoose&&againstElectronLoose)) {
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

// ____   _  _____       _      _       
//|  _ \ / \|_   _|     | | ___| |_ ___ 
//| |_) / _ \ | |    _  | |/ _ \ __/ __|
//|  __/ ___ \| |   | |_| |  __/ |_\__ \
//|_| /_/   \_\_|    \___/ \___|\__|___/


//  vector<pat::Jet> patJets (EdmHelper::getObjs<pat::Jet> (ev,  patJets_));
  edm::Handle< edm::View<pat::Jet > > patJets;
  ev.getByLabel( patJets_, patJets );
//  vector<edm::Ref<pat::Jet, pat::Jet> > patJetRefs (EdmHelper::getObjRefs<pat::Jet> (ev, patJets_));
//  sort(patJets.begin(), patJets.end(), MathHelper::greaterPt<pat::Jet> ); //Scaled Jets need not be sorted!
  JetIDSelectionFunctor jetPURE09LOOSE(JetIDSelectionFunctor::PURE09, JetIDSelectionFunctor::LOOSE );
  PFJetIDSelectionFunctor pfjetFIRSTDATALOOSE( PFJetIDSelectionFunctor::FIRSTDATA, PFJetIDSelectionFunctor::LOOSE );
  edm::ESHandle<JetCorrectorParametersCollection> JetCorParColl;
  setup.get<JetCorrectionsRecord>().get("AK5PF",JetCorParColl); 
  JetCorrectorParameters const & JetCorPar = (*JetCorParColl)["Uncertainty"];
  JetCorrectionUncertainty *jecUnc = new JetCorrectionUncertainty(JetCorPar);

//  edm::Handle<edm::ValueMap<float> > cutbasedPUJetIdMVA;
//  ev.getByLabel("cutbasedDiscriminant",cutbasedPUJetIdMVA);
  edm::Handle<edm::ValueMap<int> > cutbasedPUJetIdFlag;
  ev.getByLabel(puJetIdCutBased_, cutbasedPUJetIdFlag);
//  edm::Handle<edm::ValueMap<float> > full53XPUJetIdMVA;
//  ev.getByLabel("full53XDiscriminant",full53XPUJetIdMVA);
  edm::Handle<edm::ValueMap<int> > full53XPUJetIdFlag;
  ev.getByLabel(puJetIdFull53X_,full53XPUJetIdFlag);
//  edm::Handle<edm::ValueMap<float> > met53XPUJetIdMVA;
//  ev.getByLabel("met53XDiscriminant",met53XPUJetIdMVA);
  edm::Handle<edm::ValueMap<int> > met53XPUJetIdFlag;
  ev.getByLabel(puJetIdMET53X_,met53XPUJetIdFlag);

  bool hasNoBadJet = true;
  double delta_met_x (0.), delta_met_y(0.), deltaHT(0.);
  double delta_met_x_unclustered (0.), delta_met_y_unclustered(0.), deltaHT_unclustered(0.);
  int njetsJESUp(0), njetsJESDown(0);
  vector<pat::Jet> good_Jets;
  int ngoodUncleandJets(0), ngoodEleCleanedJets(0), ngoodMuCleanedJets(0);
  std::vector<float> jetspt, jetsptUncorr, jetseta, jetsbtag, jetsSVMass, jetsphi, jetsUnc, jetsMass2;
  std::vector<int> jetsparton, jetsEleCleaned, jetsMuCleaned, jetsID, jetsCutBasedPUJetIDFlag, jetsMET53XPUJetIDFlag, jetsFull53XPUJetIDFlag;

  std::vector<float> jetsChargedHadronEnergyFraction, jetsNeutralHadronEnergyFraction, jetsChargedEmEnergyFraction, jetsNeutralEmEnergyFraction, jetsPhotonEnergyFraction, jetsElectronEnergyFraction, jetsMuonEnergyFraction, jetsHFHadronEnergyFraction, jetsHFEMEnergyFraction;
  int numBPartons(0), numCPartons(0);
  for (unsigned i = 0; i<patJets->size();i++) {
    const pat::Jet & patJet = patJets->at(i);
//    if (not (patJets[i].pt() > softJetThreshold)) continue;
    bool jetID;
    if ( patJet.isPFJet() ) {
//    if ( false ) {
    //https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetID

      jetID = pfjetFIRSTDATALOOSE(patJet);

    } else {
      jetID = jetPURE09LOOSE(patJet);
    }
    bool jetPassesEleCleaning = EdmHelper::passesDeltaRCleaning(patJet, veto_electrons, 0.3);
    bool jetPassesMuCleaning = EdmHelper::passesDeltaRCleaning(patJet, veto_muons, 0.3);

    bool jet_is_good = (jetID and (patJet.pt() >= minJetPt_)  and (fabs( patJet.eta() ) <= maxJetEta_));
    bool jet_is_soft = (patJet.pt() >= softJetPtThreshold_);
    if ((patJet.pt() > minJetPt_) and (fabs( patJet.eta() ) <  5.0) and not jetID) hasNoBadJet = false;
    if (jet_is_good and jetPassesEleCleaning and jetPassesMuCleaning) good_Jets.push_back(patJet);
    if (addGeneratorInfo_) {
      if (jet_is_good and jetPassesEleCleaning and jetPassesMuCleaning and abs(patJet.partonFlavour())==4) numCPartons+=1; 
      if (jet_is_good and jetPassesEleCleaning and jetPassesMuCleaning and abs(patJet.partonFlavour())==5) numBPartons+=1;
    } 
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

//      int idflag = (*cutbasedPUJetIdFlag)[patJets->refAt(i)];
//      cout<<i<<" "<<idflag<<endl;
//      cout<< PileupJetIdentifier::passJetId( idflag, PileupJetIdentifier::kLoose )<<endl;
      jetsCutBasedPUJetIDFlag.push_back((*cutbasedPUJetIdFlag)[patJets->refAt(i)]);
      jetsMET53XPUJetIDFlag.push_back((*met53XPUJetIdFlag)[patJets->refAt(i)]);
      jetsFull53XPUJetIDFlag.push_back((*full53XPUJetIdFlag)[patJets->refAt(i)]);
      const reco::SecondaryVertexTagInfo  * SVtagInfo = patJet.tagInfoSecondaryVertex();
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
      jetsEleCleaned.push_back(jetPassesEleCleaning);
      jetsMuCleaned.push_back(jetPassesMuCleaning);
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
    if (jet_is_good) ngoodUncleandJets++;
    if (jet_is_good and jetPassesEleCleaning) ngoodEleCleanedJets++;
    if (jet_is_good and jetPassesMuCleaning) ngoodMuCleanedJets++;
    
    if ((verbose_) and (patJet.pt() > softJetPtThreshold_)) cout<<"[jet "<<i<<"] "<<" pt "<<patJet.pt()<<" eta "<<patJet.eta()<<" phi "<<patJet.phi()<<boolalpha<<" jetID? "<<jetID<<" jetID+pt+eta cut?"<< jet_is_good <<" passes Ele c.c? "<<jetPassesEleCleaning<<" passes Mu c.c? "<<jetPassesMuCleaning<<endl;
    jecUnc->setJetEta(patJet.eta());
    jecUnc->setJetPt(patJet.pt()); // here you must use the CORRECTED jet pt
    double unc = (patJet.pt() > 10. && fabs(patJet.eta()<5)) ? jecUnc->getUncertainty(true) : 0.1;
    pat::Jet scaledJet = patJet;
    scaledJet.scaleEnergy(1+unc);
    delta_met_x += - scaledJet.px() + patJet.px();    
    delta_met_y += - scaledJet.py() + patJet.py();  
    deltaHT     += scaledJet.pt() - patJet.pt();
    if (patJet.pt()<10.) {
      delta_met_x_unclustered += - scaledJet.px() + patJet.px();    
      delta_met_y_unclustered += - scaledJet.py() + patJet.py();  
      deltaHT_unclustered     += scaledJet.pt() - patJet.pt();
    }
    if (jetID and (fabs( patJet.eta() ) < maxJetEta_) and jetPassesEleCleaning and jetPassesMuCleaning and scaledJet.pt()>minJetPt_) njetsJESUp++;
    scaledJet.scaleEnergy((1-unc)/(1+unc));
    if (jetID and (fabs( patJet.eta() ) < maxJetEta_) and jetPassesEleCleaning and jetPassesMuCleaning and scaledJet.pt()>minJetPt_) njetsJESDown++;
  }
  if (addFullJetInfo_){
    put("jetsPt", jetspt);
    put("jetsPtUncorr", jetsptUncorr);
    put("jetsEta", jetseta);
    put("jetsPhi", jetsphi);
    put("jetsMass2", jetsMass2);
    put("jetsParton", jetsparton);
    put("jetsBtag", jetsbtag);
    put("jetsSVMass", jetsSVMass);
    put("jetsUnc", jetsUnc);
    put("jetsEleCleaned", jetsEleCleaned);
    put("jetsMuCleaned", jetsMuCleaned);
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
  }
  delete jecUnc;
  put  ("nsoftjets", jetspt.size());
  if (addRA4AnalysisInfo_) {
    put ("hasNoBadJet", hasNoBadJet);
    put  ("ngoodUncleanedJets", ngoodUncleandJets); 
    put  ("ngoodEleCleanedJets", ngoodEleCleanedJets); 
    put  ("ngoodMuCleanedJets",  ngoodMuCleanedJets); 
    if (addGeneratorInfo_) {
      put("numBPartons", numBPartons);
      put("numCPartons", numCPartons);
    }
    put("deltaMETx", delta_met_x);
    put("deltaMETy", delta_met_y);
    put("deltaHT", deltaHT);
    put("deltaMETxUnclustered", delta_met_x_unclustered);
    put("deltaMETyUnclustered", delta_met_y_unclustered);
    put("deltaHTUnclustered", deltaHT_unclustered);
    put("njetsJESUp", njetsJESUp);
    put("njetsJESDown", njetsJESDown);
    sort(good_Jets.begin(), good_Jets.end(), MathHelper::greaterPt<pat::Jet> );
    //number of jets above 50 GeV
    put  ("njets"  , good_Jets.size());
    //Calculating some Observables
    put("m3", RecoHelper::M3(good_Jets));
    put("jet0pt", good_Jets.size() < 1 ? NAN : good_Jets[0].pt());
    put("jet1pt", good_Jets.size() < 2 ? NAN : good_Jets[1].pt());
    put("jet2pt", good_Jets.size() < 3 ? NAN : good_Jets[2].pt());
    put("jet3pt", good_Jets.size() < 4 ? NAN : good_Jets[3].pt());
    put("jet0ptUncorr", good_Jets.size() < 1 ? NAN : good_Jets[0].correctedJet("Uncorrected").pt());
    put("jet1ptUncorr", good_Jets.size() < 2 ? NAN : good_Jets[1].correctedJet("Uncorrected").pt());
    put("jet2ptUncorr", good_Jets.size() < 3 ? NAN : good_Jets[2].correctedJet("Uncorrected").pt());
    put("jet3ptUncorr", good_Jets.size() < 4 ? NAN : good_Jets[3].correctedJet("Uncorrected").pt());
    put("jet0eta", good_Jets.size() < 1 ? NAN : good_Jets[0].eta());
    put("jet0phi", good_Jets.size() < 1 ? NAN : good_Jets[0].phi());
    put("jet1eta", good_Jets.size() < 2 ? NAN : good_Jets[1].eta());
    put("jet1phi", good_Jets.size() < 2 ? NAN : good_Jets[1].phi());
    put("jet2eta", good_Jets.size() < 3 ? NAN : good_Jets[2].eta());
    put("jet2phi", good_Jets.size() < 3 ? NAN : good_Jets[2].phi());
    put("jet3eta", good_Jets.size() < 4 ? NAN : good_Jets[3].eta());
    put("jet3phi", good_Jets.size() < 4 ? NAN : good_Jets[3].phi());

    put("jet0btag", good_Jets.size() < 1 ? NAN : good_Jets[0].bDiscriminator(btag_));
    put("jet1btag", good_Jets.size() < 2 ? NAN : good_Jets[1].bDiscriminator(btag_));
    put("jet2btag", good_Jets.size() < 3 ? NAN : good_Jets[2].bDiscriminator(btag_));
    put("jet3btag", good_Jets.size() < 4 ? NAN : good_Jets[3].bDiscriminator(btag_));

    
    std::vector<pat::Jet > btaggedJets = good_Jets; 
    sort(btaggedJets.begin(), btaggedJets.end(), greaterBTag(btag_));
    put("btag0", btaggedJets.size() < 1 ? NAN : btaggedJets[0].bDiscriminator(btag_));
    put("btag1", btaggedJets.size() < 2 ? NAN : btaggedJets[1].bDiscriminator(btag_));
    put("btag2", btaggedJets.size() < 3 ? NAN : btaggedJets[2].bDiscriminator(btag_));
    put("btag3", btaggedJets.size() < 4 ? NAN : btaggedJets[3].bDiscriminator(btag_));
    
    Int_t nbtags=0;
    Int_t nbtagsPure=0;
    Int_t nbjets=0;
    for (unsigned i = 0; i < good_Jets.size(); i++){
      if(good_Jets[i].bDiscriminator(btag_)>=btagWP_){nbtags++;}
      if(good_Jets[i].bDiscriminator(btagPure_)>=btagPureWP_){nbtagsPure++;}    
      if (!isData) {
        if(abs(good_Jets[i].partonFlavour())==5){nbjets++;}
      }
    }
    put("nbtags",nbtags);
    put("nbtagsPure",nbtagsPure);
    put("nbjets",nbjets);
    
    if (addFullBTagInfo_) {
      if (!isData) {
        put("jet0parton", good_Jets.size() < 1 ? NAN : good_Jets[0].partonFlavour());
        put("jet1parton", good_Jets.size() < 2 ? NAN : good_Jets[1].partonFlavour());
        put("jet2parton", good_Jets.size() < 3 ? NAN : good_Jets[2].partonFlavour());
        put("jet3parton", good_Jets.size() < 4 ? NAN : good_Jets[3].partonFlavour());
      }
      for (unsigned i = 0; i < good_Jets.size(); i++){
        const reco::SecondaryVertexTagInfo  &SVtagInfo = *good_Jets[i].tagInfoSecondaryVertex();
        if(good_Jets[i].tagInfoSecondaryVertex()){
          if(SVtagInfo.nVertices()>0){
            const reco::Vertex &SVertex=SVtagInfo.secondaryVertex(0);
            if(i==0){put("jet0btagMass",SVertex.p4().M());}
            if(i==1){put("jet1btagMass",SVertex.p4().M());}
            if(i==2){put("jet2btagMass",SVertex.p4().M());}
            if(i==3){put("jet3btagMass",SVertex.p4().M());}
          }
        }
      }
      vector<std::pair<float, float> > btags;
      vector<std::pair<float, float> > btagsParton;
       

      if (!isData) {
        put("btag0parton", btaggedJets.size() < 1 ? NAN : btaggedJets[0].partonFlavour());
        put("btag1parton", btaggedJets.size() < 2 ? NAN : btaggedJets[1].partonFlavour());
        put("btag2parton", btaggedJets.size() < 3 ? NAN : btaggedJets[2].partonFlavour());
        put("btag3parton", btaggedJets.size() < 4 ? NAN : btaggedJets[3].partonFlavour());
      }
      
      put("btag0pt", btaggedJets.size() < 1 ? NAN : btaggedJets[0].pt());
      put("btag1pt", btaggedJets.size() < 2 ? NAN : btaggedJets[1].pt());
      put("btag2pt", btaggedJets.size() < 3 ? NAN : btaggedJets[2].pt());
      put("btag3pt", btaggedJets.size() < 4 ? NAN : btaggedJets[3].pt());
      
      put("btag0eta", btaggedJets.size() < 1 ? NAN : btaggedJets[0].eta());
      put("btag1eta", btaggedJets.size() < 2 ? NAN : btaggedJets[1].eta());
      put("btag2eta", btaggedJets.size() < 3 ? NAN : btaggedJets[2].eta());
      put("btag3eta", btaggedJets.size() < 4 ? NAN : btaggedJets[3].eta());
      
      //   vector<jet > btaggedJets;
      for (unsigned i = 0; i < btaggedJets.size(); i++){  
        const reco::SecondaryVertexTagInfo  &SVtagInfo = *btaggedJets[i].tagInfoSecondaryVertex();
        if(btaggedJets[i].tagInfoSecondaryVertex()){
          if(SVtagInfo.nVertices()>0){
            const reco::Vertex &SVertex=SVtagInfo.secondaryVertex(0);
            if(i==0){put("btag0Mass",SVertex.p4().M());}
            if(i==1){put("btag1Mass",SVertex.p4().M());}
            if(i==2){put("btag2Mass",SVertex.p4().M());}
            if(i==3){put("btag3Mass",SVertex.p4().M());}
          }
        }
      }
    }
  }

  /////////////////////////////////////MET////////////////////////////////////////////////////
  vector<pat::MET> patMET (EdmHelper::getObjs<pat::MET > (ev,  patMET_));
  math::XYZTLorentzVector patMET_p4 = MathHelper::nanVector();
  float metpx(NAN);
  float metpy(NAN);
  float met(NAN);

  if (addMetUncertaintyInfo_) {
    for (std::vector<std::string>::iterator s = metsToMonitor_.begin(); s != metsToMonitor_.end(); s++) {
        vector<pat::MET> patCorrMET (EdmHelper::getObjs<pat::MET > (ev,  *s));  // get PATCorr Objects
        std::string metName = *s;
        float metVal = patCorrMET[0].pt();
        float metValphi = patCorrMET[0].phi();
        float metValsumEt = patCorrMET[0].sumEt();
        //cout<<prefix<<"Monitoring the following met: "<<*s<<": "<<metVal<<endl;
        put(metName, metVal);
        put(metName+"phi", metValphi);
        put(metName+"sumEt", metValsumEt);
    }
  }

  if (patMET.size()>0) {
    metpx = patMET[0].px();// + delta_met_x;//Apply changes from JES
    metpy = patMET[0].py();// + delta_met_y;//Apply changes from JES
    met = sqrt(metpx*metpx + metpy*metpy);
    put("met", met);
    put("metpx", metpx);
    put("metpy", metpy);

    patMET_p4.SetPz(0.);
    patMET_p4.SetPx(metpx);
    patMET_p4.SetPy(metpy);
    patMET_p4.SetE (met );

    put("metphi", patMET_p4.phi());
    put("sumEt", patMET[0].sumEt());

  }
//  float barepfmetpx(NAN); 
//  float barepfmetpy(NAN); 
//  float barepfmet(NAN); 
//  vector<reco::PFMET> recoPFMET (EdmHelper::getObjs< reco::PFMET > (ev, edm::InputTag("pfMet") ) );
//  if (recoPFMET.size()>0) {
//    barepfmetpx = recoPFMET[0].px();// + delta_met_x; 
//    barepfmetpy = recoPFMET[0].py();// + delta_met_y; 
//    barepfmet   =  sqrt(barepfmetpx*barepfmetpx + barepfmetpy*barepfmetpy);
//    put("barepfmetpx", barepfmetpx);     //Apply changes from JES
//    put("barepfmetpy", barepfmetpy);     //Apply changes from JES
//    put("barepfmet", barepfmet);
//    put("barepfmetsumEt", recoPFMET[0].sumEt()); // NAN);
//    
//  }
  //GenMET
  edm::Handle<reco::GenMETCollection> genmet;
  if (ev.getByLabel("genMetTrue", genmet) && genmet->size() > 0) {
    put("genmetpx", genmet->front().px());
    put("genmetpy", genmet->front().py());
    put("genmet", genmet->front().pt());
    put("genmetphi", genmet->front().phi());
    if (addGeneratorInfo_){
      put("genmetChargedEM", genmet->front().ChargedEMEt());
      put("genmetChargedHad", genmet->front().ChargedHadEt());
      put("genmetMuonEt", genmet->front().MuonEt());
      put("genmetNeutralEM", genmet->front().NeutralEMEt());
      put("genmetNeutralHad", genmet->front().NeutralHadEt());
      put("genmetSumEt", genmet->front().sumEt());
    }
  }
  
///  if(addFullMETInfo_){
///    vector<pat::MET> rawMET (EdmHelper::getObjs<pat::MET > (ev,  rawMET_));
/////     math::XYZTLorentzVector rawMET_p4 = MathHelper::nanVector();
///    if (rawMET.size()>0) {
///      put("rawMetpx", rawMET[0].px());//Apply changes from JES
///      put("rawMetpy", rawMET[0].py());//Apply changes from JES
///      put("rawMet", rawMET[0].pt()); //sqrt(rawmetpx*rawmetpx + rawmetpy*rawmetpy);
///      put("rawMetphi",rawMET[0].phi());
///      put("rawMetSignificance",rawMET[0].significance());
///    }
///    
///    vector<pat::MET> type01MET (EdmHelper::getObjs<pat::MET > (ev,  type01MET_));
/////     math::XYZTLorentzVector type01MET_p4 = MathHelper::nanVector();
///    if (type01MET.size()>0) {
///      put("type01Metpx", type01MET[0].px());//Apply changes from JES
///      put("type01Metpy", type01MET[0].py());//Apply changes from JES
///      put("type01Met", type01MET[0].pt()); //sqrt(type01metpx*type01metpx + type01metpy*type01metpy);
///      put("type01Metphi",type01MET[0].phi());
///    }
///    
///    vector<pat::MET> type1phiMET (EdmHelper::getObjs<pat::MET > (ev,  type1phiMET_));
/////     math::XYZTLorentzVector type1phiMET_p4 = MathHelper::nanVector();
///    if (type1phiMET.size()>0) {
///      put("type1phiMetpx", type1phiMET[0].px());//Apply changes from JES
///      put("type1phiMetpy", type1phiMET[0].py());//Apply changes from JES
///      put("type1phiMet", type1phiMET[0].pt()); //sqrt(type1phimetpx*type1phimetpx + type1phimetpy*type1phimetpy);
///      put("type1phiMetphi",type1phiMET[0].phi());
///    }
    
//    vector<pat::MET> type01phiMET (EdmHelper::getObjs<pat::MET > (ev,  type01phiMET_));
////     math::XYZTLorentzVector type01phiMET_p4 = MathHelper::nanVector();
//    if (type01phiMET.size()>0) {
//      put("type01phiMetpx", type01phiMET[0].px());//Apply changes from JES
//      put("type01phiMetpy", type01phiMET[0].py());//Apply changes from JES
//      put("type01phiMet", type01phiMET[0].pt()); //sqrt(type01phimetpx*type01phimetpx + type01phimetpy*type01phimetpy);
//      put("type01phiMetphi",type01phiMET[0].phi());
//    }
//
//  }

/*  ____      _   _  _     ____       _           _   _
   |  _ \    / \ | || |   / ___|  ___| | ___  ___| |_(_) ___  _ __
   | |_) |  / _ \| || |_  \___ \ / _ \ |/ _ \/ __| __| |/ _ \| '_ \
   |  _ <  / ___ \__   _|  ___) |  __/ |  __/ (__| |_| | (_) | | | |
   |_| \_\/_/   \_\ |_|   |____/ \___|_|\___|\___|\__|_|\___/|_| |_|
*/
  if (addRA4AnalysisInfo_) {
    bool singleMuonic     = (good_muons.size()==1)  && (good_electrons.size() == 0);
    bool Muonic           = (good_muons.size() > 0) && (good_electrons.size() == 0);
    bool singleElectronic = (good_muons.size()==0)  && (good_electrons.size() == 1);
    bool Electronic       = (good_muons.size()==0)  && (good_electrons.size() > 0);
    bool mixed            = (good_muons.size() > 0) && (good_electrons.size() > 0);
    bool multiMuonic      = (good_muons.size() > 1) && (good_electrons.size() == 0);
    bool multiElectronic  = (good_muons.size() == 0) && (good_electrons.size() > 1);
    bool mixedMuonic=0;
    bool mixedElectronic=0;

    put("singleMuonic", singleMuonic);
    put("muonic", Muonic);
    put("singleElectronic", singleElectronic);
    put("electronic", Electronic);

    //Define the lepton!
    reco::Particle leading_lepton;
    leading_lepton.setCharge(0);
    leading_lepton.setP4(MathHelper::nanVector());
    reco::Particle second_lepton;
    second_lepton.setCharge(0);
    second_lepton.setP4(MathHelper::nanVector());

    //There is a second good lepton.
    if  (multiMuonic){
      second_lepton = reco::Particle(good_muons[1].charge(), good_muons[1].p4(), good_muons[1].vertex(), good_muons[1].pdgId());
    }
  //       cout<<"smu"<<endl;
    if (multiElectronic ){
      second_lepton = reco::Particle(good_electrons[1].charge(), good_electrons[1].p4(), good_electrons[1].vertex(), good_electrons[1].pdgId());
    }
  //       cout<<"sele"<<endl;
    if (mixed) {
  //       cout<<"mix!!"<<endl;
  //   cout<<"mu"<<good_muons[0].pt()<<"ele"<<good_electrons[0].pt()<<endl;
  //   cout<<"Sizemu: "<<good_muons.size()<<"  Sizeele: "<<good_electrons.size()<<endl;
      if (good_muons[0].pt()>good_electrons[0].pt()) {
  //     cout<<"mixMu";
        mixedMuonic=1;
        second_lepton = reco::Particle(good_electrons[0].charge(), good_electrons[0].p4(), good_electrons[0].vertex(), good_electrons[0].pdgId());
      } else {
        mixedElectronic=1;
        second_lepton = reco::Particle(good_muons[0].charge(), good_muons[0].p4(), good_muons[0].vertex(), good_muons[0].pdgId());
      }
  //   cout<<"MIX"<<mixedMuonic<<" "<<mixedElectronic<<endl;
    }
  //     cout<<"MIX2"<<mixedMuonic<<" "<<mixedElectronic<<endl;      
  //     cout<<"MIX2a"<<mixedMuonic<<" "<<mixedElectronic<<endl;  
    put("mixedMuonic", mixedMuonic);
    put("mixedElectronic", mixedElectronic);

    put("lepton2Pt" , second_lepton.pt());
    put("lepton2Eta", second_lepton.eta());
    put("lepton2Phi", second_lepton.phi());
    put("lepton2Pdg", second_lepton.pdgId());

    if (Muonic || mixedMuonic)   {
      leading_lepton = reco::Particle(good_muons[0].charge(), good_muons[0].p4(), good_muons[0].vertex(), good_muons[0].pdgId());
    }
    if (Electronic || mixedElectronic) {
      leading_lepton = reco::Particle(good_electrons[0].charge(), good_electrons[0].p4(), good_electrons[0].vertex(), good_electrons[0].pdgId());
    }
   
    if (Muonic || Electronic || mixedElectronic || mixedMuonic) {
      if (addFullLeptonInfo_) { 
        float lepton_hasMCMatch(NAN);
        if (Muonic || mixedMuonic)   {
          std::vector<reco::GenParticleRef> genPartRefs = good_muons[0].genParticleRefs();
          if (genPartRefs.size() > 0) {
            lepton_hasMCMatch = 1;
          }
          else {
            lepton_hasMCMatch = 0;
          }
        }
        if (Electronic || mixedElectronic) {
          std::vector<reco::GenParticleRef> genPartRefs = good_electrons[0].genParticleRefs();
          if (genPartRefs.size() > 0) {
            lepton_hasMCMatch = 1;
          }
          else {
            lepton_hasMCMatch = 0;
          }
        }
        put("leptonHasMCMatch", lepton_hasMCMatch);
        if (Muonic || mixedMuonic) {
          pat::Muon * mu = &(good_muons[0]);
          reco::TrackRef ref_iT = good_muons[0].innerTrack();
          if (!ref_iT.isNull()) {
            put("leptonVertexDxy", fabs(ref_iT->dxy(vertexPosition)));
            put("leptonVertexDz", ref_iT->dz(vertexPosition));
            put("leptonDxy", fabs(ref_iT->dxy(beamSpotPosition)));
          }
          reco::TrackRef refT = good_muons[0].globalTrack();
          if (refT.isNonnull()) {
            put("muonNValTrackerHits", refT->hitPattern().numberOfValidTrackerHits());
            put("leptonNormChi2", refT->chi2() / refT->ndof());
          }
          put("muonisGlobalMuonPromptTight", mu->isGood("GlobalMuonPromptTight"));
          put("muonisTrackerMuon", mu->isGood("AllTrackerMuons"));
          put("leptonEcalIso", mu->ecalIso());
          put("leptonHcalIso", mu->hcalIso());
          put("leptonTrackIso", mu->trackIso());

          put("leptonAeff", NAN); 
          put("leptonEleScEta", NAN); 
          put("leptonPF03ChargedHadronIso", mu->pfIsolationR03().sumChargedHadronPt);
          put("leptonPF03NeutralHadronIso", mu->pfIsolationR03().sumNeutralHadronEt);
          put("leptonPF03PhotonIso", mu->pfIsolationR03().sumPhotonEt);
          put("leptonPF03PUChargedHadronIso", mu->pfIsolationR03().sumPUPt);

          double pfRelIso (NAN);
          if (mu->pt()>0) {
            pfRelIso = muonPFRelIsoDeltaBeta_ ?
              (mu->pfIsolationR03().sumChargedHadronPt
               + max(0., mu->pfIsolationR03().sumNeutralHadronEt
                       + mu->pfIsolationR03().sumPhotonEt
                   - 0.5*mu->pfIsolationR03().sumPUPt ) ) / mu->pt() :
              ( mu->pfIsolationR03().sumChargedHadronPt
             + mu->pfIsolationR03().sumNeutralHadronEt
             + mu->pfIsolationR03().sumPhotonEt ) / mu->pt();
          }
          put("leptonRelIso", pfRelIso);
          put("leptonPF03RelIso", pfRelIso);

          put("leptonPF04ChargedHadronIso", mu->pfIsolationR04().sumChargedHadronPt);
          put("leptonPF04NeutralHadronIso", mu->pfIsolationR04().sumNeutralHadronEt);
          put("leptonPF04PhotonIso", mu->pfIsolationR04().sumPhotonEt);
          put("leptonPF04PUChargedHadronIso", mu->pfIsolationR04().sumPUPt);
          double pf04RelIso (NAN);
          if (mu->pt()>0) {
            pf04RelIso = muonPFRelIsoDeltaBeta_ ?
              (mu->pfIsolationR04().sumChargedHadronPt
               + max(0., mu->pfIsolationR04().sumNeutralHadronEt
                       + mu->pfIsolationR04().sumPhotonEt
                   - 0.5*mu->pfIsolationR04().sumPUPt ) ) / mu->pt() :
              ( mu->pfIsolationR04().sumChargedHadronPt
             + mu->pfIsolationR04().sumNeutralHadronEt
             + mu->pfIsolationR04().sumPhotonEt ) / mu->pt();
          }
          put("leptonPF04RelIso", pf04RelIso);
        }
        if (Electronic || mixedElectronic) {
    //       cout<<"5"<<endl;
          pat::Electron * el = &(good_electrons[0]);
          double pt = el->pt();
          edm::Ptr< reco::GsfElectron > gsfel = (edm::Ptr< reco::GsfElectron >) el->originalObjectRef();
          double charged =  (*(*electronIsoVals)[0])[gsfel];
          double photon = (*(*electronIsoVals)[1])[gsfel];
          double neutral = (*(*electronIsoVals)[2])[gsfel];

          put("leptonEleID", el->electronID("eidTight"));
          put("leptonEleHoE", el->hadronicOverEm());
          put("leptonEledPhi", el->deltaPhiSuperClusterTrackAtVtx());
          put("leptonEledEta", el->deltaEtaSuperClusterTrackAtVtx());
          put("leptonElesIeta", el->sigmaIetaIeta());
          put("leptonElemHits", el->gsfTrack()->trackerExpectedHitsInner().numberOfHits());
          bool passConversionRejection = gsfel.isNull()?false : !ConversionTools::hasMatchedConversion(*gsfel,hConversions,beamSpotPosition);
          put("leptonElePassingConversion", passConversionRejection);
          put("leptonEcalIso", el->dr03EcalRecHitSumEt());
          put("leptonHcalIso", el->dr03HcalTowerSumEt());
          put("leptonTrackIso", el->dr03TkSumPt());
   
          double Aeff= isData ? ElectronEffectiveArea::GetElectronEffectiveArea(ElectronEffectiveArea::kEleGammaAndNeutralHadronIso03, el->superCluster()->eta(), ElectronEffectiveArea::kEleEAData2011):
                           ElectronEffectiveArea::GetElectronEffectiveArea(ElectronEffectiveArea::kEleGammaAndNeutralHadronIso03, el->superCluster()->eta(), ElectronEffectiveArea::kEleEAFall11MC);

          double pfRelIso = elePFRelIsoAreaCorrected_?( charged + max (0., photon + neutral - (*eleRho)*Aeff) ) / pt : ( charged +  photon + neutral ) / pt;

          put("leptonRelIso", pfRelIso); 
          put("leptonAeff", Aeff); 
          put("leptonEleScEta", el->superCluster()->eta()); 

          put("leptonPF03ChargedHadronIso", charged);
          put("leptonPF03NeutralHadronIso", neutral);
          put("leptonPF03PhotonIso",        photon);
          put("leptonPF03PUChargedHadronIso", el->isoDeposit(pat::PfPUChargedHadronIso)->depositWithin(0.3));
          put("leptonPF03RelIso", pfRelIso);

  //        double charged04 =  (*(*electronIsoVals04)[0])[gsfel];
  //        double photon04 =  (*(*electronIsoVals04)[1])[gsfel];
  //        double neutral04 =  (*(*electronIsoVals04)[2])[gsfel];
  //        double Aeff04 = isData ? ElectronEffectiveArea::GetElectronEffectiveArea(ElectronEffectiveArea::kEleGammaAndNeutralHadronIso04, el->superCluster()->eta(), ElectronEffectiveArea::kEleEAData2011):
  //                       ElectronEffectiveArea::GetElectronEffectiveArea(ElectronEffectiveArea::kEleGammaAndNeutralHadronIso04, el->superCluster()->eta(), ElectronEffectiveArea::kEleEAFall11MC);
  //        double pfRelIso04 = elePFRelIsoAreaCorrected_?( charged04 + max (0., photon04 + neutral04 - (*eleRho)*Aeff04) ) / pt : ( charged04 +  photon04 + neutral04 ) / pt;
  //        put("leptonPF04PUChargedHadronIso", el->isoDeposit(pat::PfPUChargedHadronIso)->depositWithin(0.4));
          put("leptonPF04PUChargedHadronIso", NAN);
          put("leptonPF04RelIso", NAN);

          reco::GsfTrackRef refT = el->gsfTrack();
          if (refT.isNonnull()) {
            put("electronNHits", refT->trackerExpectedHitsInner().numberOfHits());
            put("leptonNormChi2", refT->chi2() / refT->ndof());
            put("leptonDxy", fabs(refT->dxy(beamSpotPosition)));
            put("leptonVertexDxy", fabs(refT->dxy(vertexPosition)));
            put("leptonVertexDz", refT->dz(vertexPosition));
          }
        }
        
        vector<double> deltaRs;
        for (unsigned j = 0; j<good_Jets.size(); j++) {
          deltaRs.push_back(reco::deltaR(leading_lepton.p4(), good_Jets[j].p4()));
        }
        sort(deltaRs.begin(),deltaRs.end());
        put("leptonDeltaR", deltaRs.size()==0 ? 999:deltaRs[0]);
      }
      put("leptonPt" , leading_lepton.pt());
      put("leptonEta", leading_lepton.eta());
      put("leptonPhi", leading_lepton.phi());
      put("leptonPdg", leading_lepton.pdgId());
    }
    put("mT", (patMET.size() == 0) ? NAN : MathHelper::mT( leading_lepton.p4(), patMET_p4, false).mass());

    /*Compute ht2 (HT with leading jet missing) from basicJets*/
    float ht = 0.;
    float ht2 = 0.;
    float mht_x = 0.;
    float mht_y = 0.;
    for (unsigned i = 0; i < good_Jets.size(); i++) {
      ht += good_Jets[i].pt();
      if (i>0) ht2+=good_Jets[i].pt();
      mht_x -= good_Jets[i].px();
      mht_y -= good_Jets[i].py();
    }
    put("ht", ht);
    put("ht2", ht2);
    put("mht", sqrt(mht_x*mht_x + mht_y*mht_y));
    put("mhtpx", mht_x); 
    put("mhtpy", mht_y);

    if (verbose_) cout<<"[Summary] type-I pfMET "<<met<<" HT "<<ht<<" njets "<<good_Jets.size()<<" good Mu "<<good_muons.size()<<" good Ele "<<good_electrons.size()<<" veto Mu "<<veto_muons.size()<<" veto Ele "<<veto_electrons.size()<<endl<<endl;

    float ht_lep = ht + leading_lepton.pt();
    float delta_HT = fabs(ht - leading_lepton.pt());//delta-HT of leading_pat-Lepton-jets system

    put("ra4AlphaTLep", .5*(ht_lep - delta_HT) /sqrt( ht_lep*ht_lep - (mht_x*mht_x + mht_y*mht_y)));
    /*Compute metsig as met/Sqrt(HT)*/
    put("kinMetSig", met/sqrt(ht));

    //Met Isolation
    std::vector<float> met_isos;
    for (unsigned i = 0;i<good_Jets.size(); i++) {
      if (patMET.size()>0) { 
        met_isos.push_back(fabs(reco::deltaPhi(patMET_p4, good_Jets[i])));
        met_isos.push_back(fabs(fabs(reco::deltaPhi(patMET_p4, good_Jets[i])) - 3.1415926));
      }
    }
    std::sort(met_isos.begin(),met_isos.end());
    put("metiso", ( met_isos.size()>0 ) ? met_isos[0] : NAN);
    // GenParticles
    edm::InputTag genParticleTag = edm::InputTag("genParticles");
    edm::Handle< vector< reco::GenParticle > > genParticleHandle;
    try {
      ev.getByLabel(genParticleTag, genParticleHandle );
      if (!genParticleHandle.isValid() || genParticleHandle.failedToGet()) {
  //      if (verbose_) cout << prefix << "GenParticles not valid!." << endl;
      }
    } catch (exception & e) {
      cout << prefix << "error (GenParticles): " << e.what() << endl;
    }
    bool hasGluonSplitting = false;
    vector< const reco::GenParticle *> genParticles;
    vector< const reco::GenParticle *> allGenParticles;
    if ( genParticleHandle.isValid() and (!genParticleHandle.failedToGet())) {
      for( unsigned i = 0; i < genParticleHandle->size(); i++ ) {
        allGenParticles.push_back ( &( (*genParticleHandle)[i] ) );
        if ( (*genParticleHandle)[i].status() == 3) genParticles.push_back( &( (*genParticleHandle)[i] ));

        if ((abs((*genParticleHandle)[i].pdgId())==4)||(abs((*genParticleHandle)[i].pdgId())==5)) {
          if ((*genParticleHandle)[i].numberOfMothers()>0) {
            if (abs((*genParticleHandle)[i].mother(0)->pdgId())==21) hasGluonSplitting = true;
          }

        }
      }

  //    std::auto_ptr< vector<int> > selectedIds(new vector<int>());
    } else {
  //    if (verbose_) cout<<prefix << "no genParticles Collection" << endl;
    }

    double isr30_x = 0.;
    double isr30_y = 0.;
    double isr_x = 0.;
    double isr_y = 0.;
    double ttbar_x = 0.;
    double ttbar_y = 0.;
    double bMinusFromTopPt = NAN;
    double bMinusFromTopEta = NAN;
    double bPlusFromTopPt = NAN;
    double bPlusFromTopEta = NAN;
    for (unsigned i = 0; i<genParticles.size(); i++) {
      //find top in decay chain
  //    cout<<prefix<<" At "<<i<<endl;
      if ( (genParticles[i]->status()==3) and (abs(genParticles[i]->pdgId())==6) ) {
        ttbar_x += genParticles[i]->px(); 
        ttbar_y += genParticles[i]->py(); 
      }
      if ( (genParticles[i]->status()!=3) or (not ( (abs(genParticles[i]->pdgId())<5) or (abs(genParticles[i]->pdgId())==21))) or (not decaysIntoTop(genParticles[i]))) continue; //Only look at quarks or gluons
  //    cout<<prefix<<i<<" pdgId "<<genParticles[i]->pdgId()<<" status "<< genParticles[i]->status()<<" decays_to_top "<< boolalpha<<decaysIntoTop(genParticles[i])<<endl;
  //    cout<<prefix<<" Done with "<<i<<endl;
      if (genParticles[i]->numberOfDaughters()>=2) {
  //      bool to_top0 = decaysIntoTop(genParticles[i]->daughter(0));
  //      bool to_top1 = decaysIntoTop(genParticles[i]->daughter(1));
  //      cout<<prefix<<boolalpha<<" to_top0 "<<to_top0<<" to_top1 "<< to_top1<<endl;
  //      if ((to_top0) and (!to_top1)) cout<<"At "<<i<<" ISR comp. daughter 1: pdgId "<<genParticles[i]->daughter(1)->pdgId()<<" status "<< genParticles[i]->daughter(1)->status()<<" pT "<<genParticles[i]->daughter(1)->p4().pt()<<endl;
  //      if ((!to_top0) and (to_top1)) cout<<"At "<<i<<" ISR comp. daughter 0: pdgId "<<genParticles[i]->daughter(0)->pdgId()<<" status "<< genParticles[i]->daughter(0)->status()<<" pT "<<genParticles[i]->daughter(0)->p4().pt()<<endl;
        for (unsigned j = 0; j < genParticles[i]->numberOfDaughters(); j++) {
          if (not decaysIntoTop(genParticles[i]->daughter(j))) {
           isr_x+=genParticles[i]->daughter(j)->px();
           isr_y+=genParticles[i]->daughter(j)->py();
           if (genParticles[i]->daughter(j)->p4().pt() > 30.) {
  //          cout<<"At "<<i<<" per particle: ISR comp. daughter "<<j<<": pdgId "<<genParticles[i]->daughter(j)->pdgId()<<" status "<< genParticles[i]->daughter(j)->status()<<" pT "<<genParticles[i]->daughter(j)->p4().pt()<<endl;
            isr30_x+=genParticles[i]->daughter(j)->px();
            isr30_y+=genParticles[i]->daughter(j)->py();
            }
          }
        }
      }
    }
    double isr = sqrt(isr_x*isr_x + isr_y*isr_y);
    double isr30 = sqrt(isr30_x*isr30_x + isr30_y*isr30_y);
    double ttbar = sqrt(ttbar_x*ttbar_x + ttbar_y*ttbar_y);
  //  if (isr>0.) {
  //    cout<<prefix<<"Total ISR30 pT:" <<isr30<<endl;
  //    cout<<prefix<<"Total ISR   pT:" <<isr<<endl;
  //    cout<<prefix<<"Total ttbar pT:" <<ttbar<<endl;
  //  }

    const reco::GenParticle * leading_genlepton = 0;
    float genleptonpt=0.;

  //  if (verbose_) cout << "[SUSYTupelizer] looking through " << genParticles.size() << " particles." << endl;

    if (addGeneratorInfo_){
      put("hasGluonSplitting", hasGluonSplitting);
      bool firstTop = true;
      bool firstProton = true;
      for ( vector< const reco::GenParticle * >::const_iterator 
            gp=genParticles.begin(); gp!=genParticles.end() ; ++gp )
      {
    //    if  ( (**gp).pdgId()  == 2212 ) {
    //      cout<<prefix<<"incident proton: "<< (**gp).p4()<<endl;
    //      for (unsigned i=0;i<(**gp).numberOfDaughters();i++) {
  //      cout<<prefix<<"  particle "<<gp - genParticles.begin()<<"/"<<genParticles.size()<<" pdgId "<<(**gp).pdgId()<<endl;
    //      }
    //    }
        if ( ( abs ( (**gp).pdgId() ) == 2212)) {
          if ((**gp).numberOfDaughters()>0) {
  //          cout<<"proton daughter "<<(**gp).daughter(0)->pdgId()<<endl;
            if (firstProton) { put("protonDaughter0Pdg", (**gp).daughter(0)->pdgId()); firstProton=false;}
            else {put("protonDaughter1Pdg", (**gp).daughter(0)->pdgId());}

          }
        }
        if ( ( abs ( (**gp).pdgId() ) == 6 )) {
          if (!firstTop) {
            put("top1Px", (**gp).px());
            put("top1Py", (**gp).py());
            put("top1Pz", (**gp).pz());
            put("top1Pdg", (**gp).pdgId());
            std::vector<const reco::Candidate *> b  = getDaughterParticles((*gp), 5, 3);
            if (b.size()>0) {
  //            cout<<"Found top1->b "<<b[0]->pdgId()<<endl;
              put("top1bPx",  b[0]->px());
              put("top1bPy",  b[0]->py());
              put("top1bPz",  b[0]->pz());
              put("top1bPdg", b[0]->pdgId());
              const reco::Candidate * B =  getDaughterParticles(b[0], b[0]->pdgId() , -1)[0];
              put("top1bPxStat2",  B->px());
              put("top1bPyStat2",  B->py());
              put("top1bPzStat2",  B->pz());
              put("top1bPdgStat2", B->pdgId());
            }
            std::vector<const reco::Candidate *> W = getDaughterParticles((*gp), 24, 3);
            if (W.size()>0) {
  //          cout<<"Found top1->b "<<W[0]->pdgId()<<endl;
              put("top1WPx",  W[0]->px());
              put("top1WPy",  W[0]->py());
              put("top1WPz",  W[0]->pz());
              put("top1WPdg", W[0]->pdgId());
              std::vector<const reco::Candidate *> Wdaughters = getDaughterParticles(W[0], -1, 3);
              std::vector<const reco::Candidate *> W_stat2 = getDaughterParticles(getDaughterParticles(W[0], 24, 2)[0], 24,2);
              if (W_stat2.size()>0){
                put("top1WPxStat2",  W_stat2[0]->px());
                put("top1WPyStat2",  W_stat2[0]->py());
                put("top1WPzStat2",  W_stat2[0]->pz());
                put("top1WPdgStat2", W_stat2[0]->pdgId());
              }
  //            cout<<prefix<<"top1W_stat2 "<<W_stat2[0]->px()<<endl;
  //            cout<<prefix<<"top1WD0_stat2 "<< getDaughterParticles(Wdaughters[0], Wdaughters[0]->pdgId() , -1)[0]->px()<<" "<<endl;
  //            cout<<prefix<<"top1WD1_stat2 "<< getDaughterParticles(Wdaughters[1], Wdaughters[1]->pdgId() , -1)[0]->px()<<" "<<endl;
              if (Wdaughters.size()>1) {
  //              cout<<"Found top1->W daughter "<<Wdaughters[0]->pdgId()<<" "<<Wdaughters[1]->pdgId()<<endl;
                put("top1WDaughter0Px",  Wdaughters[0]->px());
                put("top1WDaughter0Py",  Wdaughters[0]->py());
                put("top1WDaughter0Pz",  Wdaughters[0]->pz());
                put("top1WDaughter0Pdg", Wdaughters[0]->pdgId());
                put("top1WDaughter1Px",  Wdaughters[1]->px());
                put("top1WDaughter1Py",  Wdaughters[1]->py());
                put("top1WDaughter1Pz",  Wdaughters[1]->pz());
                put("top1WDaughter1Pdg", Wdaughters[1]->pdgId());
                std::vector<const reco::Candidate *> D0 =  getDaughterParticles(Wdaughters[0], Wdaughters[0]->pdgId() , -1);
                std::vector<const reco::Candidate *> D1 =  getDaughterParticles(Wdaughters[1], Wdaughters[1]->pdgId() , -1);
                if (D0.size()>0) {
                  put("top1WDaughter0PxStat2",  D0[0]->px());
                  put("top1WDaughter0PyStat2",  D0[0]->py());
                  put("top1WDaughter0PzStat2",  D0[0]->pz());
                  put("top1WDaughter0PdgStat2", D0[0]->pdgId());
                }
                if (D1.size()>0) {
                  put("top1WDaughter1PxStat2",  D1[0]->px());
                  put("top1WDaughter1PyStat2",  D1[0]->py());
                  put("top1WDaughter1PzStat2",  D1[0]->pz());
                  put("top1WDaughter1PdgStat2", D1[0]->pdgId());
                }
              }
            }
            break; //There can be more than 2 tops and that would cause an exception at the 2nd put of top1Px
          }
          if (firstTop) {
            firstTop=false;
            put("top0Px", (**gp).px());
            put("top0Py", (**gp).py());
            put("top0Pz", (**gp).pz());
            put("top0Pdg", (**gp).pdgId());
            std::vector<const reco::Candidate *> b  = getDaughterParticles((*gp), 5, 3);
            if (b.size()>0) {
  //            cout<<"Found top0->b "<<b[0]->pdgId()<<endl;
              put("top0bPx",  b[0]->px());
              put("top0bPy",  b[0]->py());
              put("top0bPz",  b[0]->pz());
              put("top0bPdg", b[0]->pdgId());
              const reco::Candidate * B =  getDaughterParticles(b[0], b[0]->pdgId() , -1)[0];
              put("top0bPxStat2",  B->px());
              put("top0bPyStat2",  B->py());
              put("top0bPzStat2",  B->pz());
              put("top0bPdgStat2", B->pdgId());
            }
            std::vector<const reco::Candidate *> W = getDaughterParticles((*gp), 24, 3);
            if (W.size()>0) {
              put("top0WPx",  W[0]->px());
              put("top0WPy",  W[0]->py());
              put("top0WPz",  W[0]->pz());
              put("top0WPdg", W[0]->pdgId());
              std::vector<const reco::Candidate *> W_stat2 = getDaughterParticles(getDaughterParticles(W[0], 24, 2)[0], 24,2);
              if (W_stat2.size()) {
                put("top0WPxStat2",  W_stat2[0]->px());
                put("top0WPyStat2",  W_stat2[0]->py());
                put("top0WPzStat2",  W_stat2[0]->pz());
                put("top0WPdgStat2", W_stat2[0]->pdgId());
              }
  //            cout<<prefix<<"top0W_stat2 "<<W_stat2[0]->px()<<endl;
  //            cout<<prefix<<"top0WD0_stat2 "<< getDaughterParticles(Wdaughters[0], Wdaughters[0]->pdgId() , -1)[0]->px()<<" "<<endl;
  //            cout<<prefix<<"top0WD1_stat2 "<< getDaughterParticles(Wdaughters[1], Wdaughters[1]->pdgId() , -1)[0]->px()<<" "<<endl;
              std::vector<const reco::Candidate *> Wdaughters = getDaughterParticles(W[0], -1, 3);
              if (Wdaughters.size()>1) {
  //              cout<<"Found top0->W daughter "<<Wdaughters[0]->pdgId()<<" "<<Wdaughters[1]->pdgId()<<endl;
                put("top0WDaughter0Px",  Wdaughters[0]->px());
                put("top0WDaughter0Py",  Wdaughters[0]->py());
                put("top0WDaughter0Pz",  Wdaughters[0]->pz());
                put("top0WDaughter0Pdg", Wdaughters[0]->pdgId());
                put("top0WDaughter1Px",  Wdaughters[1]->px());
                put("top0WDaughter1Py",  Wdaughters[1]->py());
                put("top0WDaughter1Pz",  Wdaughters[1]->pz());
                put("top0WDaughter1Pdg", Wdaughters[1]->pdgId());
                std::vector<const reco::Candidate *> D0 =  getDaughterParticles(Wdaughters[0], Wdaughters[0]->pdgId() , -1);
                std::vector<const reco::Candidate *> D1 =  getDaughterParticles(Wdaughters[1], Wdaughters[1]->pdgId() , -1);
                if (D0.size()>0) {
                  put("top0WDaughter0PxStat2",  D0[0]->px());
                  put("top0WDaughter0PyStat2",  D0[0]->py());
                  put("top0WDaughter0PzStat2",  D0[0]->pz());
                  put("top0WDaughter0PdgStat2", D0[0]->pdgId());
                }
                if (D1.size()>0) {
                  put("top0WDaughter1PxStat2",  D1[0]->px());
                  put("top0WDaughter1PyStat2",  D1[0]->py());
                  put("top0WDaughter1PzStat2",  D1[0]->pz());
                  put("top0WDaughter1PdgStat2", D1[0]->pdgId());
                }
              }
            }
          }
        }
        if ( ( (**gp).pt()>20.) and ( ( abs ( (**gp).pdgId() ) == 13 ) or (abs ( (**gp).pdgId() ) == 11 )) )
        {
          // leading?
          if ( (**gp).pt() > genleptonpt )
          {
            genleptonpt = (**gp).pt();
            leading_genlepton=*gp;
          }
          // now check if the leading muon is 
        }
      }
      if ( leading_genlepton )
      {
        // we have a leading generator-level muon, now see if
        // the leading pat muon matches
        put("genleptonpt", genleptonpt);
        put("genleptonphi", leading_genlepton->phi());
        put("genleptoneta", leading_genlepton->eta());
        put("genleptonpdg", leading_genlepton->pdgId());
        bool genleptonmatch = false;
        math::XYZTLorentzVector recop = leading_lepton.p4();
        if ( ( fabs ( recop.pt() - genleptonpt ) / genleptonpt < 1. ) &&
             MathHelper::deltaR ( recop, leading_genlepton->p4() ) < 0.2 )
        {
          genleptonmatch = true;
        }
        put("genleptonmatch", genleptonmatch);
  //      cout<<prefix<<" leading genlepton "<<genleptonpt<<" "<<leading_genlepton->eta()<<" "<<leading_genlepton->pdgId()<<endl;
  //      for ( unsigned i = 0; i < leading_genlepton->numberOfMothers(); i++) {
  //        cout<<prefix<<" mother "<<i<<" "<<leading_genlepton->mother(i)->pdgId()<<endl;
  //      }
      }
      // The number neutrino multiplicity and the neutrino-from-W multiplicity uniquely determines the decay type of TT and W (13 channels!)
      int nuE(0);
      int nuMu(0);
      int nuTau(0);
      int antinuE(0);
      int antinuMu(0);
      int antinuTau(0);
      for (unsigned i=0; i < genParticles.size(); i++){
        switch (genParticles[i]->pdgId()) {
          case  12:  {nuE++;break;}
          case -12:  {antinuE++;break;}
          case  14:  {nuMu++;break;}
          case -14:  {antinuMu++;break;}
          case  16:  {nuTau++;break;}
          case -16:  {antinuTau++;break;}
        }
      }
      put("nuE", nuE);
      put("nuMu", nuMu);
      put("nuTau", nuTau);
      put("antinuE", antinuE);
      put("antinuMu", antinuMu);
      put("antinuTau", antinuTau);
      int sumNu = nuMu + nuE + nuTau;
      int sumantiNu = antinuMu + antinuE + antinuTau;

      vector<const reco::GenParticle* > genTausFromWs;
  //    vector<const reco::GenParticle* > genNuFromW;
      vector<const reco::GenParticle* > genWs;

      for (unsigned i = 0; i< genParticles.size(); i++) {
        if (abs(genParticles[i]->pdgId()) == 15) {             //if it's a tau
          if (genParticles[i]->numberOfMothers()>0) {          //which has a mother
            if (abs(genParticles[i]->mother(0)->pdgId()) == 24) {      //which is a W
              genTausFromWs.push_back(genParticles[i]);            //then store it
            }
          }
        }
  //      if ( (abs(genParticles[i]->pdgId()) == 12) or (abs(genParticles[i]->pdgId()) == 14) or (abs(genParticles[i]->pdgId()) == 16)){             //if it's a neutrino
  //        if (genParticles[i]->numberOfMothers()>0) {          //which has a mother
  //          if (abs(genParticles[i]->mother(0)->pdgId()) == 24) {      //which is a W
  //            genNuFromW.push_back(genParticles[i]);            //then store it
  //          }
  //        }
  //      }
        if (abs(genParticles[i]->pdgId()) == 24) {
          genWs.push_back(genParticles[i]);
        }
      }
      put("tausFromW", genTausFromWs.size());
      if (genWs.size()>0) {


        put("W0Px", genWs[0]->px());
        put("W0Py", genWs[0]->py());
        put("W0Eta", genWs[0]->eta());
        put("W0Pdg", genWs[0]->pdgId());
        std::vector<const reco::Candidate *> W_stat2 = getDaughterParticles(getDaughterParticles(genWs[0], 24, 2)[0], 24,2);
        if (W_stat2.size()>0) {
          put("W0PxStat2",  W_stat2[0]->px());
          put("W0PyStat2",  W_stat2[0]->py());
          put("W0PzStat2",  W_stat2[0]->pz());
          put("W0PdgStat2", W_stat2[0]->pdgId());
        }
        std::vector<const reco::Candidate *> Wdaughters = getDaughterParticles(genWs[0], -1, 3);
        if (Wdaughters.size()>1){
    //      const reco::Candidate * W0D1 =  getDaughterParticles(Wdaughters[0], Wdaughters[0]->pdgId() , -1)[0];
          put("W0Daughter0Pdg", Wdaughters[0]->pdgId());
          put("W0Daughter0Pt",  Wdaughters[0]->pt());
          put("W0Daughter0Eta", Wdaughters[0]->eta());
          put("W0Daughter0Phi", Wdaughters[0]->phi());
          put("W0Daughter1Pdg", Wdaughters[1]->pdgId());
          put("W0Daughter1Pt",  Wdaughters[1]->pt());
          put("W0Daughter1Eta", Wdaughters[1]->eta());
          put("W0Daughter1Phi", Wdaughters[1]->phi());
          std::vector<const reco::Candidate *> D0 =  getDaughterParticles(Wdaughters[0], Wdaughters[0]->pdgId() , -1);
          std::vector<const reco::Candidate *> D1 =  getDaughterParticles(Wdaughters[1], Wdaughters[1]->pdgId() , -1);
          if (D0.size()>0) {
            put("W0Daughter0PdgStat2", D0[0]->pdgId());
            put("W0Daughter0PtStat2",  D0[0]->pt());
            put("W0Daughter0EtaStat2", D0[0]->eta());
            put("W0Daughter0PhiStat2", D0[0]->phi());
          }
          if (D1.size()>0) {
            put("W0Daughter1PdgStat2", D1[0]->pdgId());
            put("W0Daughter1PtStat2",  D1[0]->pt());
            put("W0Daughter1EtaStat2", D1[0]->eta());
            put("W0Daughter1PhiStat2", D1[0]->phi());
          }
        }
      }
      if (genWs.size()>1) {
        put("W1Px", genWs[1]->px());
        put("W1Py", genWs[1]->py());
        put("W1Eta", genWs[1]->eta());
        put("W1Pdg", genWs[1]->pdgId());
        std::vector<const reco::Candidate * > W_stat2 = getDaughterParticles(getDaughterParticles(genWs[1], 24, 2)[0], 24,2);
        if (W_stat2.size()>0) {
          put("W1PxStat2",  W_stat2[0]->px());
          put("W1PyStat2",  W_stat2[0]->py());
          put("W1PzStat2",  W_stat2[0]->pz());
          put("W1PdgStat2", W_stat2[0]->pdgId());
        }
        std::vector<const reco::Candidate *> Wdaughters = getDaughterParticles(genWs[1], -1, 3);
        if (Wdaughters.size()>1){
    //      const reco::Candidate * W0D1 =  getDaughterParticles(Wdaughters[0], Wdaughters[0]->pdgId() , -1)[0];
          put("W1Daughter0Pdg", Wdaughters[0]->pdgId());
          put("W1Daughter0Pt",  Wdaughters[0]->pt());
          put("W1Daughter0Eta", Wdaughters[0]->eta());
          put("W1Daughter0Phi", Wdaughters[0]->phi());
          put("W1Daughter1Pdg", Wdaughters[1]->pdgId());
          put("W1Daughter1Pt",  Wdaughters[1]->pt());
          put("W1Daughter1Eta", Wdaughters[1]->eta());
          put("W1Daughter1Phi", Wdaughters[1]->phi());
          std::vector<const reco::Candidate *> D0 =  getDaughterParticles(Wdaughters[0], Wdaughters[0]->pdgId() , -1);
          std::vector<const reco::Candidate *> D1 =  getDaughterParticles(Wdaughters[1], Wdaughters[1]->pdgId() , -1);
          if (D0.size()>0) {
            put("W1Daughter0PdgStat2", D0[0]->pdgId());
            put("W1Daughter0PtStat2",  D0[0]->pt());
            put("W1Daughter0EtaStat2", D0[0]->eta());
            put("W1Daughter0PhiStat2", D0[0]->phi());
          }
          if (D1.size()>0) {
            put("W1Daughter1PdgStat2", D1[0]->pdgId());
            put("W1Daughter1PtStat2",  D1[0]->pt());
            put("W1Daughter1EtaStat2", D1[0]->eta());
            put("W1Daughter1PhiStat2", D1[0]->phi());
          }
        }
      }

      int nuEFromTausFromWs(0);
      int nuMuFromTausFromWs(0);
      int nuTauFromTausFromWs(0);
      int nmcTaus(0);
      vector<float>  mcTausPt, mcTausEta, mcTausPhi, mcTausMetX, mcTausMetY;
      vector<int>    mcTausPdg;
      for (unsigned i = 0; i < genTausFromWs.size(); i++) {
        int nd = genTausFromWs[i]->numberOfDaughters();
        int tau_daughter2_index(-1);
        for (int j = 0; j<nd; j++) {
          if (genTausFromWs[i]->daughter(j)!=NULL) {
            if ( (abs(genTausFromWs[i]->daughter(j)->pdgId())==15) and (genTausFromWs[i]->daughter(j)->status()==2) ) tau_daughter2_index = j;
          }
        }
        if (tau_daughter2_index < 0) {
        } else {
          if (genTausFromWs[i]->daughter(tau_daughter2_index) == NULL) {
            cout<<prefix<<"daughter "<<tau_daughter2_index<<" of tau "<<i<<" is 0!!"<<endl;
            continue;
          }
          if ( (abs(genTausFromWs[i]->daughter(tau_daughter2_index)->pdgId()) != 15) or (genTausFromWs[i]->daughter(tau_daughter2_index)->status()!=2))
            cout<<prefix<<"Warning!! This status-3 tau from a W does not have a status-2 tau daughter!!"<<endl;
      
          double tauPt = genTausFromWs[i]->daughter(tau_daughter2_index)->pt();
          double tauEta = genTausFromWs[i]->daughter(tau_daughter2_index)->eta();
          double tauPhi = genTausFromWs[i]->daughter(tau_daughter2_index)->phi();
          double tauPdg = genTausFromWs[i]->daughter(tau_daughter2_index)->pdgId();
          double tauMetX = 0.;
          double tauMetY = 0.;
          for (unsigned j = 0; j < genTausFromWs[i]->daughter(tau_daughter2_index)->numberOfDaughters(); j++) {//looping over the daughters of the status-2 tau (coming from the status-3 tau) from a W
            const reco::Candidate * candidate ( genTausFromWs[i]->daughter(tau_daughter2_index)->daughter(j) );
            int pdgid = abs(candidate->pdgId());
    //            cout<<prefix<<"Checking status "<<candidate->status()<<" and pdgId "<<pdgid<<endl;
            if ((candidate->status() == 1) and ( ( pdgid == 12) )) {
              nuEFromTausFromWs++;
              tauMetX+=candidate->px();
              tauMetY+=candidate->py();
            }
            if ((candidate->status() == 1) and ( ( pdgid == 14) )) {
              nuMuFromTausFromWs++;
              tauMetX+=candidate->px();
              tauMetY+=candidate->py();
            }
            if ((candidate->status() == 1) and ( ( pdgid == 16) )) {
              nuTauFromTausFromWs++;
              tauMetX+=candidate->px();
              tauMetY+=candidate->py();
            }
          }
          nmcTaus++;
          mcTausPt.push_back(tauPt);
          mcTausEta.push_back(tauEta);
          mcTausPhi.push_back(tauPhi);
          mcTausPdg.push_back(tauPdg);
          mcTausMetX.push_back(tauMetX);
          mcTausMetY.push_back(tauMetY);
        }
      }
      put("nmcTaus", nmcTaus);
      put("mcTausPt", mcTausPt);
      put("mcTausEta", mcTausEta);
      put("mcTausPhi", mcTausPhi);
      put("mcTausPdg", mcTausPdg);
      put("mcTausMetX", mcTausMetX);
      put("mcTausMetY", mcTausMetY);
      
      put("nuEFromTausFromWs", nuEFromTausFromWs);
      put("nuMuFromTausFromWs", nuMuFromTausFromWs);
      put("nuTauFromTausFromWs", nuTauFromTausFromWs);
      put("nuFromTausFromWs", nuTauFromTausFromWs + nuMuFromTausFromWs + nuEFromTausFromWs);
  //    if (verbose_) {
  //      cout << prefix<<" Total status-3 Neutrinos: " << sumNu + sumantiNu << " (" << sumNu << "/" << sumantiNu << ")";
  //      cout         <<" Mu " <<nuMu  <<" aMu " <<antinuMu;
  //      cout         <<" E "  <<nuE   <<" aE "  <<antinuE;
  //      cout         <<" Tau "<<nuTau <<" aTau "<<antinuTau;
  //      cout<<endl;
  //      cout<<prefix<<"Found taus from W "<<genTausFromWs.size()<<" and nuFromTausFromWs "<<nuTauFromTausFromWs + nuMuFromTausFromWs + nuEFromTausFromWs;
  //      cout<<" = ("<<nuEFromTausFromWs<<", "<<nuMuFromTausFromWs<<", "<<nuTauFromTausFromWs<<")"<<endl;
  //      cout<<endl;
  //    }
      float genmetx_fromJets(0.);
      float genmety_fromJets(0.);

      for (unsigned i = 0; i< allGenParticles.size(); i++) {
        if (allGenParticles[i]->status()!=1) continue;

        int pdgId = abs(allGenParticles[i]->pdgId());
        if (not ((pdgId == 12) or (pdgId == 14) or (pdgId==16))) continue;
  //      for (unsigned nm = 0; nm<allGenParticles[i]->numberOfMothers(); nm++) {
  //        cout<<prefix<<"pdgId "<<pdgId<<" nm "<<nm<<" status "<<allGenParticles[i]->mother(nm)->status()<<" pdgId "<<allGenParticles[i]->mother(nm)->pdgId()<<endl;
  //      }
        if (abs(allGenParticles[i]->mother(0)->pdgId())==24) continue;
        if ( (abs(allGenParticles[i]->mother(0)->pdgId())==12) or (abs(allGenParticles[i]->mother(0)->pdgId())==14) or (abs(allGenParticles[i]->mother(0)->pdgId())==16)) {
          continue;
  //        if (abs(allGenParticles[i]->mother(0)->mother(0)->pdgId())==24) continue;
  //        if ( (abs(allGenParticles[i]->mother(0)->mother(0)->pdgId())==12) or (abs(allGenParticles[i]->mother(0)->mother(0)->pdgId())==14) or (abs(allGenParticles[i]->mother(0)->mother(0)->pdgId())==16)) {
  //          if (abs(allGenParticles[i]->mother(0)->mother(0)->mother(0)->pdgId())==24) continue;
  //        }
        }
  //      cout<<"Found Neutrino with pdg "<<pdgId<<" and mother pdgid "<<abs(allGenParticles[i]->mother(0)->pdgId())<<" granny: "<<abs(allGenParticles[i]->mother(0)->mother(0)->pdgId())<<endl;
        bool isNeutrinoFromTau(true);
        if (abs(allGenParticles[i]->mother(0)->pdgId())!=15) isNeutrinoFromTau = false;
  //      cout<<"It is from a tau: "<<boolalpha<<isNeutrinoFromTau<<endl;
        bool isNeutrinoFromTauFromW = isNeutrinoFromTau;
        if (isNeutrinoFromTau) {
          if (abs(allGenParticles[i]->mother(0)->mother(0)->pdgId())==15) {
            if (abs(allGenParticles[i]->mother(0)->mother(0)->mother(0)->pdgId())==24) isNeutrinoFromTauFromW = true;
          }
        }
  //      cout<<".. which is from a W: (exclude) "<<boolalpha<<isNeutrinoFromTauFromW<<endl;
        if (isNeutrinoFromTauFromW) continue;
        genmetx_fromJets -= allGenParticles[i]->px();
        genmety_fromJets -= allGenParticles[i]->py();
      }
      put("genmetxFromJets", genmetx_fromJets);
      put("genmetyFromJets", genmety_fromJets);
      put("genmetFromJets", sqrt(genmetx_fromJets*genmetx_fromJets + genmety_fromJets*genmety_fromJets) );

      //get genMu and genEle in accaptance
      vector<reco::GenParticle > acceptedGenMu, acceptedGenEle;
      for (unsigned i = 0; i< genParticles.size(); i++) {
        if (abs(genParticles[i]->pdgId()) == 11) {
          if ( ( genParticles[i]->pt() >= 20) and (fabs(genParticles[i]->eta()) <= 2.4) and not ( ( fabs(genParticles[i]->eta())>1.4442) and (fabs(genParticles[i]->eta())<1.566))) {
            acceptedGenEle.push_back(*(genParticles[i]));
          }
        }
        if (abs(genParticles[i]->pdgId()) == 13) {
          if ( ( genParticles[i]->pt() >= 15) and (fabs(genParticles[i]->eta()) <= 2.1)) {
            acceptedGenMu.push_back(*(genParticles[i]));
          }
        }
      }
      std::sort(acceptedGenMu.begin(), acceptedGenMu.end(), MathHelper::greaterPt<reco::GenParticle>);
      std::sort(acceptedGenEle.begin(), acceptedGenEle.end(), MathHelper::greaterPt<reco::GenParticle>);
      //check whether these particles have reconstructed objects
      bool leadingMCMumatched =  false;
      if (acceptedGenMu.size()>0) {
        for (unsigned j = 0; j<good_muons.size(); j++) {
          if (reco::deltaR(acceptedGenMu[0].p4(), good_muons[j].p4()) < 0.3 ) {
            leadingMCMumatched = true;
          }
        }
      }
      put("leadingMCMumatched", leadingMCMumatched);
      bool leadingMCElematched =  false;
      if (acceptedGenEle.size()>0) {
        for (unsigned j = 0; j<good_muons.size(); j++) {
          if (reco::deltaR(acceptedGenEle[0].p4(), good_muons[j].p4()) < 0.3 ) {
            leadingMCElematched = true;
          }
        }
      }
      put("leadingMCElematched", leadingMCElematched);
    } 
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
  //      if (verbose_) cout << prefix << "GenParticles not valid!." << endl;
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
       if (abs(p.pdgId()) < 1000000)  continue;

       bool hasSMMother(true);
       for (unsigned int j=0; j<p.numberOfMothers(); ++j) {
         if ( !(abs(p.mother(j)->pdgId())<1000000) ) {
           hasSMMother = false;
           break;
         }
       }
       if ( hasSMMother )  selectedIds.push_back(p.pdgId());
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
//    put("osetType", modelParameters_.get ( "type", ev ));
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
  if(addFullMuonInfo_)
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
     addVar("muonsPFDeltaPT/F[]");
  }
  if(addFullEleInfo_)
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
      addVar("elesPFDeltaPT/F[]");
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
  if (addFullJetInfo_){
    addVar("jetsPt/F[]");
    addVar("jetsPtUncorr/F[]");
    addVar("jetsEta/F[]");
    addVar("jetsPhi/F[]");
    addVar("jetsMass2/F[]");
    addVar("jetsParton/I[]");
    addVar("jetsBtag/F[]");
    addVar("jetsSVMass/F[]");
    addVar("jetsUnc/F[]");
    addVar("jetsEleCleaned/I[]");
    addVar("jetsMuCleaned/I[]");
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
  addVar("nsoftjets/I"); // NAN);

  if (addRA4AnalysisInfo_) {
    addVar("ngoodMuons/I"); // -1);
    addVar("nvetoMuons/I"); // -1);
    addVar("ngoodElectrons/I"); // -1);
    addVar("nvetoElectrons/I"); // -1);
    addVar("deltaMETx/F");
    addVar("deltaMETy/F");
    addVar("deltaHT/F"); 
    addVar("deltaMETxUnclustered/F");
    addVar("deltaMETyUnclustered/F");
    addVar("deltaHTUnclustered/F"); 
    addVar("njetsJESUp/I");
    addVar("njetsJESDown/I");

    addVar("hasNoBadJet/O"); // NAN);
    addVar("ngoodUncleanedJets/I");
    addVar("ngoodEleCleanedJets/I");
    addVar("ngoodMuCleanedJets/I");

    addVar("njets/I"); // NAN);

    addVar("m3/F"); // NAN);
    addVar("jet0pt/F"); // NAN);
    addVar("jet1pt/F"); // NAN);
    addVar("jet2pt/F"); // NAN);
    addVar("jet3pt/F"); // NAN);
    addVar("jet0ptUncorr/F"); // NAN);
    addVar("jet1ptUncorr/F"); // NAN);
    addVar("jet2ptUncorr/F"); // NAN);
    addVar("jet3ptUncorr/F"); // NAN);

    addVar("jet0eta/F"); // NAN);
    addVar("jet0phi/F"); // NAN);
    addVar("jet1eta/F"); // NAN);
    addVar("jet1phi/F"); // NAN);
    addVar("jet2eta/F"); // NAN);
    addVar("jet2phi/F"); // NAN);
    addVar("jet3eta/F"); // NAN);
    addVar("jet3phi/F"); // NAN);

    addVar("jet0btag/F"); // NAN);
    addVar("jet1btag/F"); // NAN);
    addVar("jet2btag/F"); // NAN);
    addVar("jet3btag/F"); // NAN);
    addVar("btag0/F"); // NAN);
    addVar("btag1/F"); // NAN);
    addVar("btag2/F"); // NAN);
    addVar("btag3/F"); // NAN);
    
    addVar("nbtags/I"); // NAN);
    addVar("nbtagsPure/I"); // NAN);
    addVar("nbjets/I"); // NAN);

    if (addFullBTagInfo_) {
      addVar("jet0parton/I"); // NAN);
      addVar("jet1parton/I"); // NAN);
      addVar("jet2parton/I"); // NAN);
      addVar("jet3parton/I"); // NAN);

      addVar("jet0btagMass/F"); // NAN);
      addVar("jet1btagMass/F"); // NAN);
      addVar("jet2btagMass/F"); // NAN);
      addVar("jet3btagMass/F"); // NAN);

      addVar("btag0parton/I"); // NAN);
      addVar("btag1parton/I"); // NAN);
      addVar("btag2parton/I"); // NAN);
      addVar("btag3parton/I"); // NAN);

      addVar("btag0pt/F"); // NAN);
      addVar("btag1pt/F"); // NAN);
      addVar("btag2pt/F"); // NAN);
      addVar("btag3pt/F"); // NAN);

      addVar("btag0eta/F"); // NAN);
      addVar("btag1eta/F"); // NAN);
      addVar("btag2eta/F"); // NAN);
      addVar("btag3eta/F"); // NAN);

      addVar("btag0Mass/F"); // NAN);
      addVar("btag1Mass/F"); // NAN);
      addVar("btag2Mass/F"); // NAN);
      addVar("btag3Mass/F"); // NAN);
    }
  }
  addVar("met/F"); // NAN);
  addVar("metpx/F"); // NAN);
  addVar("metpy/F"); // NAN);
  addVar("metphi/F"); // NAN);
  addVar("sumEt/F"); // NAN);
//  addVar("barepfmetpx/F"); // NAN);
//  addVar("barepfmetpy/F"); // NAN);
//  addVar("barepfmet/F"); // NAN);
//  addVar("barepfmetsumEt/F"); // NAN);
  addVar("genmetpx/F"); // NAN);
  addVar("genmetpy/F"); // NAN);
  addVar("genmet/F"); // NAN);
  addVar("genmetphi/F"); // NAN);
  if (addGeneratorInfo_) {
    addVar("genmetChargedEM/F"); // NAN);
    addVar("genmetChargedHad/F"); // NAN);
    addVar("genmetMuonEt/F"); // NAN);
    addVar("genmetNeutralEM/F"); // NAN);
    addVar("genmetNeutralHad/F"); // NAN);
    addVar("genmetSumEt/F"); // NAN);
  }

//  if (addFullMETInfo_){
//    addVar("rawMetpx/F"); // NAN);
//    addVar("rawMetpy/F"); // NAN);
//    addVar("rawMet/F"); // NAN);
//    addVar("rawMetphi/F"); // NAN);
//    addVar("rawMetSignificance/F");
//    addVar("type01Metpx/F"); // NAN);
//    addVar("type01Metpy/F"); // NAN);
//    addVar("type01Met/F"); // NAN);
//    addVar("type01Metphi/F"); // NAN);
//    addVar("type1phiMetpx/F"); // NAN);
//    addVar("type1phiMetpy/F"); // NAN);
//    addVar("type1phiMet/F"); // NAN);
//    addVar("type1phiMetphi/F"); // NAN);
//    addVar("type01phiMetpx/F"); // NAN);
//    addVar("type01phiMetpy/F"); // NAN);
//    addVar("type01phiMet/F"); // NAN);
//    addVar("type01phiMetphi/F"); // NAN);    
//  }

  if (addRA4AnalysisInfo_) {
    addVar("singleMuonic/I"); // -1);
    addVar("mixedMuonic/I"); // -1);
    addVar("muonic/I"); // -1);
    addVar("singleElectronic/I"); // -1);
    addVar("mixedElectronic/I"); // -1);
    addVar("electronic/I"); // -1);

    addVar("lepton2Pt/F"); // NAN);
    addVar("lepton2Eta/F"); // NAN);
    addVar("lepton2Phi/F"); // NAN);
    addVar("lepton2Pdg/F"); // NAN);

    if (addFullLeptonInfo_) {
      addVar("leptonHasMCMatch/O"); // NAN);
      addVar("muonNValTrackerHits/F"); // NAN);
      addVar("electronNHits/F"); // NAN);
      addVar("leptonNormChi2/F"); // NAN);
      addVar("leptonDxy/F"); // NAN);
      addVar("leptonVertexDxy/F"); // NAN);
      addVar("leptonVertexDz/F"); // NAN);
      addVar("muonisGlobalMuonPromptTight/F"); // NAN);
      addVar("muonisTrackerMuon/F"); // NAN);
      addVar("leptonEcalIso/F"); // NAN);
      addVar("leptonHcalIso/F"); // NAN);
      addVar("leptonTrackIso/F"); // NAN);
      addVar("leptonRelIso/F"); // NAN);
      addVar("leptonAeff/F"); // NAN);
      addVar("leptonEleScEta/F");

      addVar("leptonPF03ChargedHadronIso/F");
  //    addVar("leptonPF03AllParticleIso/F");
      addVar("leptonPF03NeutralHadronIso/F");
      addVar("leptonPF03PhotonIso/F");
      addVar("leptonPF03PUChargedHadronIso/F");
      addVar("leptonPF03RelIso/F");

      addVar("leptonPF04ChargedHadronIso/F");
  //    addVar("leptonPF04AllParticleIso/F");
      addVar("leptonPF04NeutralHadronIso/F");
      addVar("leptonPF04PhotonIso/F");
      addVar("leptonPF04PUChargedHadronIso/F");
      addVar("leptonPF04RelIso/F");

      addVar("leptonEleID/F"); // NAN);
      addVar("leptonEleHoE/F"); // NAN);
      addVar("leptonEledPhi/F"); // NAN);
      addVar("leptonEledEta/F"); // NAN);
      addVar("leptonElesIeta/F"); // NAN);
      addVar("leptonElemHits/F"); // NAN);
      addVar("leptonElePassingConversion/O");
      addVar("leptonDeltaR/F"); // NAN);
    }


    addVar("leptonPt/F"); // NAN);
    addVar("leptonEta/F"); // NAN);
    addVar("leptonPhi/F"); // NAN);
    addVar("leptonPdg/F"); // NAN);

    addVar("mT/F"); // NAN);
    addVar("ht/F"); // NAN);
    addVar("ht2/F"); // NAN);
    addVar("mht/F"); // NAN);
    addVar("mhtpx/F"); // NAN);
    addVar("mhtpy/F"); // NAN);
    addVar("ra4AlphaTLep/F"); // NAN);
    addVar("kinMetSig/F"); // NAN);
    addVar("metiso/F"); // NAN);


    addVar("bMinusFromTopPt/F");
    addVar("bMinusFromTopEta/F");
    addVar("bPlusFromTopPt/F");
    addVar("bPlusFromTopEta/F");

    if (addGeneratorInfo_) {
      addVar("numBPartons/I");
      addVar("numCPartons/I");
      addVar("hasGluonSplitting/O");
      addVar("protonDaughter0Pdg/I");
      addVar("protonDaughter1Pdg/I");
      addVar("topM0PdgId/I"); // NAN);
      addVar("topM1PdgId/I"); // NAN);
      addVar("topM0Pt/F"); // NAN);
      addVar("topM1Pt/F"); // NAN);
      addVar("topM0Pz/F"); // NAN);
      addVar("topM1Pz/F"); // NAN);
      addVar("top0Px/F"); // NAN);
      addVar("top0Py/F"); // NAN);
      addVar("top0Pz/F"); // NAN);
      addVar("top0Pdg/I"); // NAN);
      addVar("top1Px/F"); // NAN);
      addVar("top1Py/F"); // NAN);
      addVar("top1Pz/F"); // NAN);
      addVar("top1Pdg/I"); // NAN);

      addVar("top1bPx/F");
      addVar("top1bPy/F");
      addVar("top1bPz/F");
      addVar("top1bPdg/I");
      addVar("top0bPx/F");
      addVar("top0bPy/F");
      addVar("top0bPz/F");
      addVar("top0bPdg/I");
      addVar("top1WPx/F");
      addVar("top1WPy/F");
      addVar("top1WPz/F");
      addVar("top1WPdg/I");
      addVar("top0WPx/F");
      addVar("top0WPy/F");
      addVar("top0WPz/F");
      addVar("top0WPdg/I");

      addVar("top1bPxStat2/F");
      addVar("top1bPyStat2/F");
      addVar("top1bPzStat2/F");
      addVar("top1bPdgStat2/I");
      addVar("top0bPxStat2/F");
      addVar("top0bPyStat2/F");
      addVar("top0bPzStat2/F");
      addVar("top0bPdgStat2/I");
      addVar("top1WPxStat2/F");
      addVar("top1WPyStat2/F");
      addVar("top1WPzStat2/F");
      addVar("top1WPdgStat2/I");
      addVar("top0WPxStat2/F");
      addVar("top0WPyStat2/F");
      addVar("top0WPzStat2/F");
      addVar("top0WPdgStat2/I");

      addVar("top0WDaughter0Px/F");
      addVar("top0WDaughter0Py/F");
      addVar("top0WDaughter0Pz/F");
      addVar("top0WDaughter0Pdg/I");
      addVar("top0WDaughter1Px/F");
      addVar("top0WDaughter1Py/F");
      addVar("top0WDaughter1Pz/F");
      addVar("top0WDaughter1Pdg/I");
      addVar("top1WDaughter0Px/F");
      addVar("top1WDaughter0Py/F");
      addVar("top1WDaughter0Pz/F");
      addVar("top1WDaughter0Pdg/I");
      addVar("top1WDaughter1Px/F");
      addVar("top1WDaughter1Py/F");
      addVar("top1WDaughter1Pz/F");
      addVar("top1WDaughter1Pdg/I");

      addVar("top0WDaughter0PxStat2/F");
      addVar("top0WDaughter0PyStat2/F");
      addVar("top0WDaughter0PzStat2/F");
      addVar("top0WDaughter0PdgStat2/I");
      addVar("top0WDaughter1PxStat2/F");
      addVar("top0WDaughter1PyStat2/F");
      addVar("top0WDaughter1PzStat2/F");
      addVar("top0WDaughter1PdgStat2/I");
      addVar("top1WDaughter0PxStat2/F");
      addVar("top1WDaughter0PyStat2/F");
      addVar("top1WDaughter0PzStat2/F");
      addVar("top1WDaughter0PdgStat2/I");
      addVar("top1WDaughter1PxStat2/F");
      addVar("top1WDaughter1PyStat2/F");
      addVar("top1WDaughter1PzStat2/F");
      addVar("top1WDaughter1PdgStat2/I");

      addVar("genleptonpt/F"); // NAN);
      addVar("genleptoneta/F"); // NAN);
      addVar("genleptonphi/F"); // NAN);
      addVar("genleptonpdg/I"); // NAN);
      addVar("genleptonmatch/O"); // -1);
      addVar("nuE/I"); // -1);
      addVar("nuMu/I"); // -1);
      addVar("nuTau/I"); // -1);
      addVar("antinuE/I"); // -1);
      addVar("antinuMu/I"); // -1);
      addVar("antinuTau/I"); // -1);
      addVar("W0Px/F");
      addVar("W0Py/F");
      addVar("W0Eta/F");
      addVar("W0Pdg/I");
      addVar("W0PxStat2/F");
      addVar("W0PyStat2/F");
      addVar("W0PzStat2/F");
      addVar("W0PdgStat2/F");
      addVar("W0Daughter0Pdg/I");
      addVar("W0Daughter0Pt/F");
      addVar("W0Daughter0Eta/F");
      addVar("W0Daughter0Phi/F");
      addVar("W0Daughter1Pdg/I");
      addVar("W0Daughter1Pt/F");
      addVar("W0Daughter1Eta/F");
      addVar("W0Daughter1Phi/F");
      addVar("W0Daughter0PdgStat2/I");
      addVar("W0Daughter0PtStat2/F");
      addVar("W0Daughter0EtaStat2/F");
      addVar("W0Daughter0PhiStat2/F");
      addVar("W0Daughter1PdgStat2/I");
      addVar("W0Daughter1PtStat2/F");
      addVar("W0Daughter1EtaStat2/F");
      addVar("W0Daughter1PhiStat2/F");

      addVar("W1Px/F");
      addVar("W1Py/F");
      addVar("W1Eta/F");
      addVar("W1Pdg/I");
      addVar("W1PxStat2/F");
      addVar("W1PyStat2/F");
      addVar("W1PzStat2/F");
      addVar("W1PdgStat2/F");
      addVar("W1Daughter0Pdg/I");
      addVar("W1Daughter0Pt/F");
      addVar("W1Daughter0Eta/F");
      addVar("W1Daughter0Phi/F");
      addVar("W1Daughter1Pdg/I");
      addVar("W1Daughter1Pt/F");
      addVar("W1Daughter1Eta/F");
      addVar("W1Daughter1Phi/F");
      addVar("W1Daughter0PdgStat2/I");
      addVar("W1Daughter0PtStat2/F");
      addVar("W1Daughter0EtaStat2/F");
      addVar("W1Daughter0PhiStat2/F");
      addVar("W1Daughter1PdgStat2/I");
      addVar("W1Daughter1PtStat2/F");
      addVar("W1Daughter1EtaStat2/F");
      addVar("W1Daughter1PhiStat2/F");

      addVar("nmcTaus/I");
      addVar("mcTausPt/F[]");
      addVar("mcTausEta/F[]");
      addVar("mcTausPhi/F[]");
      addVar("mcTausPdg/I[]");
      addVar("mcTausMetX/F[]");
      addVar("mcTausMetY/F[]");

      addVar("tausFromW/I"); // -1);
      addVar("nuFromTausFromWs/I"); // -1);
      addVar("nuEFromTausFromWs/I"); // -1);
      addVar("nuMuFromTausFromWs/I"); // -1);
      addVar("nuTauFromTausFromWs/I"); // -1);

      addVar("genmetxFromJets/F");
      addVar("genmetyFromJets/F");
      addVar("genmetFromJets/F");

      addVar("leadingMCMumatched/O"); // NAN);
      addVar("leadingMCElematched/O"); // NAN);
    }
  }
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
