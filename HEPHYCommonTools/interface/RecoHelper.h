#ifndef Workspace_HEPHYCommonTools_RecoHelper_H
#define Workspace_HEPHYCommonTools_RecoHelper_H

#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/Candidate/interface/Candidate.h"
// RECO Includes
#include "DataFormats/JetReco/interface/CaloJet.h"
#include <iostream>

namespace RecoHelper
{
  double
  M3base (const std::vector<math::XYZTLorentzVector> jetp4s, const bool verbose);

  template<class T> double
  M3 (const std::vector< T > & jets, const bool verbose = false) {
    // get the Jet Lorentz-Vectors
    std::vector<math::XYZTLorentzVector> jetp4s;
    for (typename std::vector< T >::const_iterator it =  jets.begin(); it !=  jets.end(); ++it)
      jetp4s.push_back( it->p4() );
   
    return M3base( jetp4s, verbose);

  }
  double
    maxPt3 (const std::vector<pat::Jet> & jets, const bool verbose = false);
  bool
    vPlusJetsSelected (const pat::Muon& muon, const edm::Event& event, const bool verbose = false);
  bool
    vPlusJetsSelected (const pat::Electron& electron, const edm::Event& event, const bool verbose = false);
  bool 
    vPlusJetsSelected (const pat::Muon& muon, const math::XYZPoint & beamSpotPosition, bool verbose = false) ;
  bool
    vPlusJetsSelected (const pat::Electron& electron, const math::XYZPoint &, const bool verbose = false);
  bool 
    aC3Selected (const pat::Muon& muon, const edm::Event& event, bool verbose = false) ;
  // Workaround for having this selection easily in FWLite
  bool 
    aC3Selected (const pat::Muon& muon, const math::XYZPoint & beamSpotPosition, bool verbose = false) ;

 
  template<class T>  std::vector< T > 
  vPlusJetsSelected( const std::vector< T > & vec, const edm::Event& event, const bool verbose = false) {
    // std::cout << "[RecoHelper] vPlusJetsSelected template: " << vec.size() << std::endl;
    std::vector< T > res;
      for (typename std::vector< T >::const_iterator it = vec.begin();it!=vec.end();it++) 
      {
        try {
          // std::cout << "[RecoHelper] ptr=" << (void *) (&(*it)) << std::endl;
          if ( vPlusJetsSelected(*it, event, verbose)) res.push_back(*it);
        } catch ( cms::Exception & e ) {
          std::cout << "[RecoHelper]  " << e.what() << ". skipping object." << std::endl;
        }
      }
    // std::cout << "[RecoHelper] vPlusJetsSelected template end!" << std::endl;
    return res;
  }

  float 
  alphaT (std::vector<pat::Jet> & );
  float 
  alphaTHemi (const std::vector< std::vector<math::XYZTLorentzVector> >& );
  float 
  deltaPhiHemi (const std::vector< std::vector<math::XYZTLorentzVector> >& );

  float 
  chi2(std::vector<pat::Jet> jets, const pat::MET & met, const reco::Candidate & lepton);	
	float
	chi2(std::vector<pat::Jet> jets, const pat::MET & met, const math::XYZTLorentzVector & lepton);

	float
	METoverSumEt( const std::vector<pat::Jet> & jets, const pat::MET & met, const math::XYZTLorentzVector & lepton );
  enum IsoCorrectionType {TRK, ECAL, HCAL};

  float eleIsoCorrectionArea(const pat::Electron & ele, IsoCorrectionType type);
  float muIsoCorrectionArea (const pat::Muon & mu, IsoCorrectionType type);

  double 
  lepJetInvariantMass(std::vector<pat::Jet> & jets, reco::Particle lepton); 
  double 
  deltaPhiOfBestTCHEJets (std::vector<pat::Jet> & jets);

}
#endif
