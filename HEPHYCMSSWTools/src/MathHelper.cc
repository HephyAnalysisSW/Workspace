
#include "Workspace/HEPHYCMSSWTools/interface/MathHelper.h"

#include "TLorentzVector.h"

#include <float.h>
#include <math.h>
#include <numeric>

using namespace math;
using namespace std;

namespace
{
  bool debug = false;
  float smallNumber = 1e-3;

  float sqr ( float a ) { return a*a; }

  struct pplus
  {
  public:
    reco::Particle operator()(const reco::Particle& p1, const reco::Particle& p2 )
    {
      return reco::Particle ( p1 + p2 );
    }
  };
}

reco::Particle operator+(const reco::Particle& p1, const reco::Particle& p2 )
{
  return reco::Particle ( p1.charge() + p2.charge() , p1.p4() + p2.p4());
}


XYZTLorentzVector MathHelper::zeroVector() { return XYZTLorentzVector ( 0., 0., 0., 0.); }


XYZTLorentzVector MathHelper::nanVector() { return XYZTLorentzVector ( NAN, NAN, NAN, NAN); }


XYZTLorentzVector MathHelper::convert( const TLorentzVector& v ) { return XYZTLorentzVector( v.X(), v.Y(), v.Z(), v.E() ); }


reco::Particle MathHelper::zeroParticle() { return reco::Particle (0, MathHelper::zeroVector() ); }


reco::Particle MathHelper::nanParticle() { return reco::Particle (0, MathHelper::nanVector() ); }


//TaggedParticle MathHelper::nanTaggedParticle() { return TaggedParticle (MathHelper::nanParticle()); }

double MathHelper::mT (const XYZTLorentzVector& lepton,
          const XYZTLorentzVector& neutrino) {
  XYZTLorentzVector sum( lepton.px() + neutrino.px(),lepton.py() + neutrino.py(), 0., 
    sqrt( sqr(lepton.px())+sqr(lepton.py())) + sqrt( sqr(neutrino.px())+sqr(neutrino.py())) 
      ) ;
  return sum.mass();

}

XYZTLorentzVector MathHelper::mT( const XYZTLorentzVector& lepton,
				  const XYZTLorentzVector& neutrino,
				  bool is_electron )
{
  double mass = 0.105;
  if ( is_electron ) mass = 0.000511;
  XYZTLorentzVector lep( lepton.px(),lepton.py(), 0., sqrt( sqr(mass)+sqr(lepton.px())+sqr(lepton.py()) ) ) ;
  XYZTLorentzVector neu( neutrino.px(),neutrino.py(), 0., sqrt( sqr(neutrino.px())+sqr(neutrino.py()) )  ) ;
  return (lep + neu);
}


reco::Particle MathHelper::sum ( const vector<reco::Particle>& v )
{
  return accumulate( v.begin(), v.end(), MathHelper::zeroParticle(), pplus() ); // , plus<reco::Particle>());
}


const bool MathHelper::samep4::operator()( const reco::Particle& a, const reco::Particle& b )
{
  return MathHelper::samep4::operator()(a.p4(),b.p4());
}

const bool MathHelper::samep4::operator()( const pat::Jet & a, const pat::Jet & b )
{
  return MathHelper::samep4::operator()(a.p4(),b.p4());
}

const bool MathHelper::samep4::operator()( const pat::Electron & a, const pat::Electron & b )
{
  return MathHelper::samep4::operator()(a.p4(),b.p4());
}

const bool MathHelper::samep4::operator()( const pat::Muon & a, const pat::Muon & b )
{
  return MathHelper::samep4::operator()(a.p4(),b.p4());
}

const bool MathHelper::samep4::operator()( const reco::Candidate* a, const reco::Candidate* b )
{
  return MathHelper::samep4::operator()(a->p4(),b->p4());
}


const bool MathHelper::samep4::operator()( const XYZTLorentzVector& a, const XYZTLorentzVector& b )
{
//   if ( ( fabs( a.px()-b.px() ) < (float)FLT_EPSILON)&&( fabs( a.py()-b.py() ) < (float)FLT_EPSILON) &&
//        ( fabs( a.pz()-b.pz() ) < (float)FLT_EPSILON)&& ( fabs( a.energy()-b.energy() ) < (float)FLT_EPSILON)) {
  if ( ( fabs( a.px()-b.px() ) < smallNumber)&&( fabs( a.py()-b.py() ) < smallNumber) &&
       ( fabs( a.pz()-b.pz() ) < smallNumber)&& ( fabs( a.energy()-b.energy() ) < smallNumber)) {
    return true;
  } else {
    return false;
  };
}


int MathHelper::findVecInHemi( const XYZTLorentzVector& vec,
			       const vector< vector<XYZTLorentzVector> >& HemisphereVecs )
{
  int res = -1;
  MathHelper::samep4 samep4;
  for ( vector< vector<XYZTLorentzVector> >::const_iterator hemi = HemisphereVecs.begin(); hemi!=HemisphereVecs.end(); ++hemi )
  {
    for ( vector<XYZTLorentzVector>::const_iterator member = hemi->begin(); member!=hemi->end(); ++member )
    {
      if (samep4(*member, vec))
      {
        res = hemi - HemisphereVecs.begin();
        break;
      }
    }
  }
  return res;
}


bool MathHelper::splitVecHemi( const XYZTLorentzVector& lepton,
			       const std::vector< std::vector<XYZTLorentzVector> >& hemisphereVecs,
			       const std::vector<const pat::Jet*>& jets,
			       std::vector<const pat::Jet*>& hadJets,
			       std::vector<const pat::Jet*>& lepJets,
			       const bool verbose )
{
  bool proper = false;
  string prefix = "[MathHelper::splitVecHemi] ";
  if (hemisphereVecs.size()==2) {
    int lepHemisphere = -1;
    int hadHemisphere = -1;
    bool foundLepIn0 = false;
    bool foundLepIn1 = false;
    if (debug) cout<<prefix<<"looking for lepton in hemisphere 0: lepton "<<lepton<<endl;
    if (MathHelper::findMember(lepton, hemisphereVecs[0])) {
      foundLepIn0 = true;
      lepHemisphere = 0;
      hadHemisphere = 1;
    if (debug) cout<<prefix<<"lepton in hemisphere 0     FOUND"<<endl;
    } else {
      if (debug) cout<<prefix<<"lepton in hemisphere 0 NOT FOUND"<<endl;
    }
    if (debug) cout<<prefix<<"looking for lepton in hemisphere 1"<<endl;
    if (MathHelper::findMember(lepton, hemisphereVecs[1])) {
      foundLepIn1 = true;
      lepHemisphere = 1;
      hadHemisphere = 0;
      if (debug) cout<<prefix<<"lepton in hemisphere 1     FOUND"<<endl;
    }
    else {
      if (debug) cout<<prefix<<"lepton in hemisphere 1 NOT FOUND"<<endl;
    }
    if (verbose) cout<<prefix<<"Lepton Hemispheres: foundLepIn0 "<<boolalpha<<foundLepIn0<<" foundLepIn1 "<<foundLepIn1<<endl;
    if ((foundLepIn0&&(!foundLepIn1))||(foundLepIn1&&(!foundLepIn0))) {
      proper = true;
    }
    else {
      if (verbose) cout<<prefix<<"Error in associating lepton to hemispheres!"<<endl;
      proper = false;
    }
    if (proper) {
      //split jets into leptonic & hadronic acc. to the Hemisphere they belong to
      if (verbose) cout<<prefix<<"lepHemisphere "<<lepHemisphere<<" hadHemisphere "<<hadHemisphere<<endl;
      for (vector<const pat::Jet*>::const_iterator it = jets.begin(); it!=jets.end();it++){
        if (MathHelper::findMember((*it)->p4(), hemisphereVecs[lepHemisphere])) {
          lepJets.push_back(*it);
        }
        else {
          hadJets.push_back(*it);
        }
      }
    }    
  }
  return proper;
}


float MathHelper::relP( const XYZTLorentzVector& p1, const XYZTLorentzVector& p2 )
{
  return p1.P()/p2.P();
}


float MathHelper::deltaEta( const XYZTLorentzVector& p1, const XYZTLorentzVector& p2 )
{
  float ret = fabs ( p1.eta() - p2.eta() );
  return ret;
}


float MathHelper::deltaPhi( const XYZTLorentzVector& p1, const XYZTLorentzVector& p2 )
{
  float ret = fabs ( p1.phi() - p2.phi() );
  return ret < M_PI ? ret : 2*M_PI - ret;
}


float MathHelper::deltaPhi( const reco::Particle& p1, const reco::Particle& p2 )
{
  return deltaPhi (p1.p4(),p2.p4());
}


float MathHelper::deltaR( const XYZTLorentzVector& p1, const XYZTLorentzVector& p2 )
{
  float etarel = deltaEta(p1, p2);
  float phirel = deltaPhi(p1, p2);
  return sqrt(etarel*etarel+phirel*phirel);
}


float MathHelper::angle( const XYZTLorentzVector& p1, const XYZTLorentzVector& p2 )
{
  return acos(
	      (p1.px()*p2.px()+p1.py()*p2.py()+p1.pz()*p2.pz())
	      /(  sqrt(p1.px()*p1.px()+p1.py()*p1.py()+p1.pz()*p1.pz()) 
		  * sqrt(p2.px()*p2.px()+p2.py()*p2.py()+p2.pz()*p2.pz()) )
	      );
}
