#ifndef HEPHYCommonTools_MathHelper_H
#define HEPHYCommonTools_MathHelper_H
#include <vector>
#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/Candidate/interface/Particle.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
//#include "Workspace/HEPHYCommonTools/interface/TaggedParticle.h"

class TLorentzVector;

/**adding particles*/
reco::Particle operator+( const reco::Particle& , const reco::Particle& );


/**
 *  A collection of simple math functions.
 */

namespace MathHelper
{
  /** compute mT from a lepton and a neutrino, given "mass"
   *  The Mass of the LorentzVector is mT */
  math::XYZTLorentzVector mT( const math::XYZTLorentzVector& lepton,
                              const math::XYZTLorentzVector& neutrino,
                              bool lepton_is_electron );

  double mT( const math::XYZTLorentzVector& lepton,
                              const math::XYZTLorentzVector& neutrino);
  /** a particle that has NANs all over the place */
  reco::Particle nanParticle();
//  TaggedParticle nanTaggedParticle(); 
  reco::Particle zeroParticle();

  /** a 4-vector filled with NANs */
  math::XYZTLorentzVector nanVector();
  math::XYZTLorentzVector zeroVector();

  math::XYZTLorentzVector convert( const TLorentzVector& v );

  /**summing reco::Particles*/
  reco::Particle sum( const std::vector<reco::Particle >& );

  /**summing everything else via cast to reco::Particle*/
  template <class T>
  reco::Particle sum( const std::vector<T>& v )
  {
    std::vector<reco::Particle> interm;
    typename std::vector<T>::const_iterator it;
    for ( it = v.begin(); it!=v.end(); ++it ) interm.push_back( dynamic_cast<reco::Particle>(*it) );
    return sum( interm );
  }

  // templated stuff. sorting.
  template <class T> 
  bool greaterPt( const T& a, const T& b )
  {
    return (a.pt() > b.pt() );
  }

  // templated stuff. sorting.
  template <class T> 
  bool ptrGreaterPt( const T* a, const T* b )
  {
    return (a->pt() > b->pt() );
  }

  /** functor class comparing reco::Particle w.r.t p4()*/
  class samep4
  {
  public:
    const bool operator()( const pat::Jet & a, const pat::Jet & b );
    const bool operator()( const pat::Electron & a, const pat::Electron & b );
    const bool operator()( const pat::Muon & a, const pat::Muon & b );
    const bool operator()( const reco::Particle& a, const reco::Particle& b );
    const bool operator()( const reco::Candidate* a, const reco::Candidate* b );
    const bool operator()( const math::XYZTLorentzVector& a, const math::XYZTLorentzVector& b );
  };

  float relP( const math::XYZTLorentzVector& p1, const math::XYZTLorentzVector& p2 );

  float deltaEta( const math::XYZTLorentzVector& p1, const math::XYZTLorentzVector& p2 );

  float deltaPhi( const math::XYZTLorentzVector& p1, const math::XYZTLorentzVector& p2 );

  float deltaPhi( const reco::Particle& p1, const reco::Particle& p2 );

  float deltaR( const math::XYZTLorentzVector& p1, const math::XYZTLorentzVector& p2 );
  float angle ( const math::XYZTLorentzVector& p1, const math::XYZTLorentzVector& p2 );

  int findVecInHemi( const math::XYZTLorentzVector& vec,
		     const std::vector< std::vector<math::XYZTLorentzVector> >& HemisphereVecs ); 

  bool splitVecHemi( const math::XYZTLorentzVector& lepton, 
		     const std::vector< std::vector<math::XYZTLorentzVector> >& HemisphereVecs, 
		     const std::vector<const pat::Jet*>& jets,
		     std::vector<const pat::Jet*>& hadJets, 
		     std::vector<const pat::Jet*>& lepJets,
		     const bool verbose = false );
 
  template <class T>
  bool findMember( const math::XYZTLorentzVector& p, const std::vector<T>& vec )
  {
    MathHelper::samep4 samep4_;
    bool res = false;
    for (unsigned i = 0; i<vec.size(); i++) { if ( samep4_(vec[i],p) ) res = true; }
    return res;
  }
}

#endif
