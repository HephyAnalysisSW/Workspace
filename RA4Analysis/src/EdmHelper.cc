#include "Workspace/RA4Analysis/interface/EdmHelper.h"
#include "Workspace/RA4Analysis/interface/MathHelper.h"
#include "Workspace/RA4Analysis/interface/CombinatoricsHelper.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include <iostream>

using namespace std;
using namespace edm;
using namespace reco;


ostream & operator<<( ostream& os, const reco::Particle& p )
{
  os <<"Charge: "<<p.charge()<<" px: "<<p.px()<<" py: "<<p.py()<<" pz: "
     <<p.pz()<<" pt: "<<p.pt()<<" E: "<<p.energy()<<" m: "<<p.mass();
  return os;
}


vector<pat::Jet> EdmHelper::electronCleanedJets (vector<pat::Jet> & jets, vector<pat::Electron> & electrons, double deltaRCut)
{
  vector<pat::Jet> goodJets;
  for(unsigned i=0; i<jets.size(); i++)
  {
    bool isGood(true);
    for(unsigned j=0; j<electrons.size(); j++)
    {
      if (deltaR(electrons[j],jets[i])<deltaRCut){
        isGood = false;
        continue;  
      } 
    }
    if (isGood) goodJets.push_back(jets[i]);
  }
  return goodJets;
}

vector<pat::Jet> EdmHelper::muonCleanedJets (vector<pat::Jet> & jets, vector<pat::Muon> & muons, double deltaRCut)
{
  vector<pat::Jet> goodJets;
  for(unsigned i=0; i<jets.size(); i++)
  {
    bool isGood(true);
    for(unsigned j=0; j<muons.size(); j++)
    {
      if (deltaR(muons[j],jets[i])<deltaRCut){
        isGood = false;
        continue;  
      } 
    }
    if (isGood) goodJets.push_back(jets[i]);
  }
  return goodJets;
}

bool EdmHelper::hardestLeptonIsElectron ( const vector<pat::Electron> & electrons,
            const vector<pat::Muon>& muons )
{
  if ( electrons.size() == 0 ) return false;
  if ( muons.size() == 0 ) return true;
  double hardestelectron=0.;
  for ( vector< pat::Electron >::const_iterator i=electrons.begin(); 
        i!=electrons.end() ; ++i )
  {
    if (i->pt() > hardestelectron ) hardestelectron = i->pt();
  }
  double hardestmuon=0.;
  for ( vector< pat::Muon >::const_iterator i=muons.begin(); 
        i!=muons.end() ; ++i )
  {
    if (i->pt() > hardestmuon ) hardestmuon = i->pt();
  }

  return ( hardestelectron > hardestmuon );
}


bool EdmHelper::hasTriggered( const Event& event,
            const InputTag& hlTriggerResults )
{
  // cout << "[EdmHelper] trying to get trigger bit" << hlTriggerResults << endl;
  bool accept=false;
  try {
    Handle<TriggerResults> HLTR;
    event.getByLabel(hlTriggerResults,HLTR);
    if (HLTR.isValid() && (!HLTR.failedToGet()) ) {
       return HLTR->accept();
    } else {
      cout << "[EdmHelper] Trigger " << hlTriggerResults << " not valid!. Will return false." << endl;
      // printTriggerNames ( event, hlTriggerResults );
    }
  } catch ( exception & e ) {
    cout << "[EdmHelper] could not get trigger bit: " << e.what()
         << "Will return false." << endl;
  }
  return accept;
}


vector<string> EdmHelper::getAllTriggerNames( const Event& event, const InputTag& hlTriggerResults )
{
  try {
    Handle<TriggerResults> HLTR;
    event.getByLabel(hlTriggerResults,HLTR);
    if (HLTR.isValid() && (!HLTR.failedToGet()) ) {
       TriggerNames names = event.triggerNames(*HLTR);
       return names.triggerNames();
    } else {
      cout << "[EdmHelper] Trigger Results not valid!." << endl;
      return vector < string > ();
    }
  } catch ( exception & e ) {
    cout << "[EdmHelper] could not get trigger bit: " << e.what() << endl;
    return vector < string > ();
  }
}

void EdmHelper::printTriggerNames( const Event& event,
           const InputTag& hlTriggerResults )
{
  try {
    Handle<TriggerResults> HLTR;
    event.getByLabel(hlTriggerResults,HLTR);
    if (HLTR.isValid() && (!HLTR.failedToGet()) )
    {
      TriggerNames names = event.triggerNames(*HLTR);
      vector < string > n=names.triggerNames();
      for ( vector< string >::const_iterator i=n.begin(); i!=n.end() ; ++i )
      {
       cout << "[EdmHelper] " << *i << ", " << names.triggerIndex ( *i ) << ", " << HLTR->accept ( names.triggerIndex ( *i ) ) << endl;
      }
    } else {
      cout << "[EdmHelper::printTriggerNames] invalid hlTriggerResults." << endl;
    }
  } catch ( exception & e ) {
    cout << "[EdmHelper] could not get trigger bit: " << e.what() << endl;
  }
}


bool EdmHelper::hasTriggered ( const Event& event,
             const InputTag& hlTriggerResults,
             const InputTag& path )
{
  bool accept=false;
  try {
    Handle<TriggerResults> HLTR;
    event.getByLabel(hlTriggerResults,HLTR);
    if (HLTR.isValid() && (!HLTR.failedToGet()) ) {
       // cout << "[EdmHelper] we have TriggerResults. Now ask for " << path << endl;
       TriggerNames names = event.triggerNames(*HLTR);
       unsigned index = names.triggerIndex  ( path.label() );
       if ( index >= names.size() )
       {
         cout << "[EdmHelper] path " << path << " does not exist! Returning false!" << endl;
         vector < string > snames = names.triggerNames();
         for ( vector< string >::const_iterator i=snames.begin(); i!=snames.end() ; ++i )
         {
           cout << "    `-- " << *i << endl;
         }
         return false;
       }
       //cout << "[EdmHelper] index is " << index << endl;
       accept = HLTR->accept( index );
       //cout << "[EdmHelper] trigger bit " << index << " is " << accept << endl;
       //cout << "[EdmHelper] trigger size is " << names.size() << endl;
    } else {
      cout << "[EdmHelper] Trigger " << hlTriggerResults << ", " << path 
           << " not valid!. Will return false." << endl;
      // printTriggerNames ( event, hlTriggerResults );
    }
  } catch ( exception & e ) {
    cout << "[EdmHelper] could not get trigger bit for " << path << ": " << e.what()
         << "Will return false." << endl;
  }
  return accept;
}


string EdmHelper::rename( const string& old )
{
  // rename variables names such that they are legal edm names!
  string ret=old;
  for ( unsigned int i=0; i<ret.length(); ++i ) {
    if ( ret[i] == ':' ) ret[i] = '.';
    else if ( ret[i] == '_' ) ret[i] = '.';
  }
  return ret;
}


pat::Jet
EdmHelper::produceTaggedPseudoPatJet( const math::XYZTLorentzVector& p4,
              const std::string& bTagName, float bTagValue )
{
  reco::Jet pseudoRecoJet;
  pseudoRecoJet.setCharge( 0 );
  pseudoRecoJet.setP4( p4 );

  pat::Jet pseudoPatJet( pseudoRecoJet );
  pseudoPatJet.addBDiscriminatorPair( make_pair( bTagName, bTagValue ) );
  return pseudoPatJet;
}


const reco::GenParticle*
EdmHelper::getQuark( const reco::GenParticleRefVector& particles, int absPdgId )
{
  for ( reco::GenParticleRefVector::const_iterator it = particles.begin(); it != particles.end(); ++it )
  {
    if ( abs( (*it)->pdgId() ) == absPdgId ) return &**it;
  }
  return 0;
}


std::vector<const reco::GenParticle*>
EdmHelper::getQuarks( const reco::GenParticleRefVector& particles )
{
  std::vector<const reco::GenParticle*> result;
  for ( reco::GenParticleRefVector::const_iterator it = particles.begin(); it != particles.end(); ++it )
  {
    int absPdgId = abs( (*it)->pdgId() );
    if ( absPdgId <= 6 ) result.push_back( &**it );
  }
  return result;
}


const reco::GenParticle*
EdmHelper::getLepton( const reco::GenParticleRefVector& particles )
{
  for ( reco::GenParticleRefVector::const_iterator it = particles.begin(); it != particles.end(); ++it )
  {
    int absPdgId = abs( (*it)->pdgId() );
    if ( ( absPdgId == 11 ) || ( absPdgId == 13 ) || ( absPdgId == 15 ) ) return &**it;
  }
  return 0;
}


const reco::GenParticle*
EdmHelper::getNeutrino( const reco::GenParticleRefVector& particles )
{
  for ( reco::GenParticleRefVector::const_iterator it = particles.begin(); it != particles.end(); ++it )
  {
    int absPdgId = abs( (*it)->pdgId() );
    if ( ( absPdgId == 12 ) || ( absPdgId == 14 ) || ( absPdgId == 16 ) ) return &**it;
  }
  return 0;
}


vector< vector<math::XYZTLorentzVector> >
EdmHelper::getHemisphereVecs( const Event& event,
            const InputTag& hemisphereTag,
            bool verbose)
{
  string prefix("[EdmHelper::getHemisphereVecs] ");
  //vector< pair<const pat::Jet*,unsigned int> > hemisphereJets;
  vector< vector <math::XYZTLorentzVector> > hemisphereJets;
  Handle< View<pat::Hemisphere> > hemisphereHandle;
  event.getByLabel(hemisphereTag, hemisphereHandle);
 
  if ( !hemisphereHandle.isValid() ) LogError("SusyTestAnalyzer") << "problem reading hemisphere collection";

  //vector<const reco::Candidate*> daughters;
  for ( unsigned int ih=0; ih<hemisphereHandle->size(); ++ih ) {
    hemisphereJets.push_back(*(new vector<math::XYZTLorentzVector>));
    const pat::Hemisphere& hemi = (*hemisphereHandle)[ih];
    //daughters.clear();
    //daughters.reserve(hemi.numberOfDaughters());
    for ( unsigned int jh=0; jh<hemi.numberOfDaughters(); ++jh ) {
      hemisphereJets[ih].push_back(hemi.daughter(jh)->p4());
      if (verbose) cout<<prefix<<"Hemisphere: "<<ih<<" jet: "<<jh<<" with p4()"<<hemi.daughter(jh)->p4()<<endl;
      //const pat::Jet* jet = dynamic_cast<const pat::Jet*>(hemi.daughter(jh));
      //if ( jet ) hemisphereJets.push_back(make_pair(jet,ih));
      //daughters.push_back(hemi.daughter(jh));
    }
    //sort(daughters.begin(),daughters.end(),GreaterByEt<const reco::Candidate*>());
  }
  return hemisphereJets;
}



void EdmHelper::getLepton( const vector<const pat::Electron*>& electrons, const vector<const pat::Muon*>& muons,
         vector<const reco::Candidate*>& result, int nlead, const string& cutstring, bool verbose )
{
  vector<const reco::Candidate*> allLeptons;
  CombinatoricsHelper::join<reco::Candidate, pat::Electron, pat::Muon>( electrons, muons, allLeptons );

  vector<const reco::Candidate*> cutLeptons;
  EdmHelper::ptrVecSelector( allLeptons, cutLeptons, cutstring, verbose);
 
  CombinatoricsHelper::getLeading( cutLeptons, result, MathHelper::ptrGreaterPt<reco::Candidate>, nlead , verbose );
 
  if (verbose) {
    string prefix( "[EdmHelper::getLepton] " );
    cout<<prefix<<cutLeptons.size()<<" leptons survived the cuts."<<endl;
  }

}

