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
  ptThreshold_ (pset.getUntrackedParameter< double >("ptThreshold") ),  
  tauIDs_ ( pset.getUntrackedParameter< std::vector<edm::ParameterSet> >("tauIDs") )

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
  std::vector<int> tausPdg, tausisPF, taushasMCMatch;
  std::vector<float> tausPt, tausEta, tausPhi;
  std::vector<std::vector<int> > tauIDs;
  for (std::vector<edm::ParameterSet>::const_iterator it=tauIDs_.begin(); it!=tauIDs_.end();it++) {
    tauIDs.push_back(std::vector<int>()) ;
  }

  for (std::vector<pat::Tau>::const_iterator tau=taus.begin(); tau!=taus.end();tau++) {
    for (std::vector<edm::ParameterSet>::const_iterator it=tauIDs_.begin(); it!=tauIDs_.end();it++) {
      tauIDs[it-tauIDs_.begin()].push_back(tau->tauID(it->getUntrackedParameter<std::string>("accessTag")));
    }

    if (tau->pt()>ptThreshold_ ) {
      ntaus++;
      tausPt.push_back(tau->pt());
      tausEta.push_back(tau->eta());
      tausPhi.push_back(tau->phi());
      tausPdg.push_back(tau->pdgId());
      tausisPF.push_back(tau->isPFTau());
      getGenTau(*tau)? taushasMCMatch.push_back(1):taushasMCMatch.push_back(0);
    }
    if (verbose_) cout<<"[tau "<<tau-taus.begin()<<"/"<<ntaus<<"] "<<" pt "<<tau->pt()<<" eta "<<tau->eta()<<" phi "<<tau->phi()
       <<" tausPdg "<<tau->pdgId()<<boolalpha<<" tausisPF "<< tau->isPFTau() <<" taushasMCMatch "<<getGenTau(*tau)<<endl;
  }
  put("ntaus", ntaus);
  put("tausPt", tausPt);
  put("tausEta", tausEta);
  put("tausPhi", tausPhi);
  put("tausPdg", tausPdg);
  put("tausisPF", tausisPF);
  put("taushasMCMatch", taushasMCMatch);

  for (std::vector<edm::ParameterSet>::const_iterator it=tauIDs_.begin(); it!=tauIDs_.end();it++) {
    putVar( (std::string("taus")+it->getUntrackedParameter<std::string>("storeTag")).c_str(), tauIDs[it-tauIDs_.begin()]);
  }

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
  for (std::vector<edm::ParameterSet>::const_iterator it=tauIDs_.begin(); it!=tauIDs_.end();it++) {
    addVar( (std::string("taus")+it->getUntrackedParameter<std::string>("storeTag")+std::string("/I[]")).c_str());
  }

}

DEFINE_FWK_MODULE(TauTupelizer);
