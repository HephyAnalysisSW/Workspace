#include "FWCore/Framework/interface/MakerMacros.h"
#include "Workspace/HEPHYCMSSWTools/plugins/TauTupelizer.h"
#include "Workspace/HEPHYCMSSWTools/interface/EdmHelper.h"

using namespace std;

namespace {

  string prefix ("[TauTupelizer] ");
 
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
 
}

TauTupelizer::~TauTupelizer() {}

TauTupelizer::TauTupelizer( const edm::ParameterSet & pset):
  Tupelizer(pset),
  params_ ( pset ),
  verbose_ ( pset.getUntrackedParameter< bool >("verbose")),
  input_ ( pset.getUntrackedParameter< edm::InputTag >("input") ),
  ptThreshold_ (pset.getUntrackedParameter< double >("lowLeptonPtThreshold") )
{
  addAllVars();
}


void TauTupelizer::beginJob ( )
{
  cout << "[TauTupelizer] starting ... " << endl;
}

void TauTupelizer::endJob()
{
  cout << endl;
  cout << "[TauTupelizer] shutting down ... " << endl;
}

void TauTupelizer::beginRun ( edm::Run & iRun, edm::EventSetup const & iSetup )
{
}

void TauTupelizer::produce( edm::Event & ev, const edm::EventSetup & setup) {
  ev_ = &ev;
  vector<pat::Tau> taus (EdmHelper::getObjs<pat::Tau>(ev, input_));
  int ntaus(0);
  std::vector<int> tausPdg, tausisPF, taushasMCMatch, tausByLooseCombinedIsolationDBSumPtCorr, tausDecayModeFinding, tausAgainstMuonLoose, tausAgainstElectronLoose;
  std::vector<float> tausPt, tausEta, tausPhi;
  for (unsigned i = 0; i<taus.size();i++) {
    int byLooseCombinedIsolationDeltaBetaCorr = taus[i].tauID("byLooseCombinedIsolationDeltaBetaCorr");
    int decayModeFinding = taus[i].tauID("decayModeFinding");
    int againstMuonLoose = taus[i].tauID("againstMuonLoose");
    int againstElectronLoose = taus[i].tauID("againstElectronLoose");
// if (taus[i].pt()>10. && (byLooseCombinedIsolationDeltaBetaCorr&&decayModeFinding&&againstMuonLoose&&againstElectronLoose)) {
    if (taus[i].pt()>10. && (decayModeFinding)) {
      ntaus++;
      tausPt.push_back(taus[i].pt());
      tausEta.push_back(taus[i].eta());
      tausPhi.push_back(taus[i].phi());
      tausPdg.push_back(taus[i].pdgId());
      tausisPF.push_back(taus[i].isPFTau());
      tausByLooseCombinedIsolationDBSumPtCorr.push_back(byLooseCombinedIsolationDeltaBetaCorr);
      tausDecayModeFinding.push_back(decayModeFinding);
      tausAgainstMuonLoose.push_back(againstMuonLoose);
      tausAgainstElectronLoose.push_back(againstElectronLoose);
      getGenTau(taus[i])? taushasMCMatch.push_back(1):taushasMCMatch.push_back(0);
    }
    if ((verbose_) and (taus[i].pt() > 10)) cout<<"[tau "<<i<<"/"<<ntaus<<"] "<<" pt "<<taus[i].pt()<<" eta "<<taus[i].eta()<<" phi "<<taus[i].phi()
       <<" tausPdg "<<taus[i].pdgId()<<boolalpha<<" tausisPF "<< taus[i].isPFTau() <<" tausByLooseCombinedIsolationDBSumPtCorr "<<byLooseCombinedIsolationDeltaBetaCorr
       <<" tausDecayModeFinding "<<decayModeFinding<<" tausAgainstMuonLoose "<<againstMuonLoose<<" tausAgainstElectronLoose "<<againstElectronLoose<<" taushasMCMatch "<<getGenTau(taus[i])<<endl;
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

void TauTupelizer::addAllVars( )
{
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

DEFINE_FWK_MODULE(TauTupelizer);
