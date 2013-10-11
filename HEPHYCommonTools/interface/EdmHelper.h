#ifndef HEPHYCommonTools_EdmHelper_H
#define HEPHYCommonTools_EdmHelper_H

#include "FWCore/Framework/interface/Event.h"

#ifndef FWLITE_HEADER_PROTECT
#include "FWCore/Framework/interface/EDProducer.h"
#endif

#include "DataFormats/PatCandidates/interface/Particle.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Hemisphere.h"

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

// #include "PhysicsTools/UtilAlgos/interface/StringCutObjectSelector.h"
#include "CommonTools/UtilAlgos/interface/StringCutObjectSelector.h"

#include "Workspace/HEPHYCommonTools/interface/MathHelper.h"

//#include "TLorentzVector.h"

#include <vector>
#include <string>
#include <ostream>


std::ostream& operator<<( std::ostream& , const reco::Particle& ); 


/**
 *  A collection of simple helper functions.
 */
namespace EdmHelper {

  std::vector<pat::Jet> electronCleanedJets(std::vector<pat::Jet> & jets, std::vector<pat::Electron> & electrons, double deltaRCut = 0.3);
//  std::vector<pat::Jet> electronCleanedJets(std::vector<pat::Jet> & jets, const pat::Electron & electron, double deltaRCut = 0.3);
  std::vector<pat::Jet> muonCleanedJets(std::vector<pat::Jet> & jets, std::vector<pat::Muon> & muons, double deltaRCut = 0.3);

  template<class T>
  bool passesDeltaRCleaning (pat::Jet & jet, std::vector<T> & leptons, double deltaRCut)
  {
    for(unsigned i=0; i<leptons.size(); i++)
    {
      if (deltaR(leptons[i],jet)<deltaRCut){
        return false;
      }
    }
    return true;
  }

  /**
   * is hardest lepton an electron? 
   **/
  bool hardestLeptonIsElectron ( const std::vector<pat::Electron>&,
                                 const std::vector<pat::Muon>& );

  /**
   * do we have any positive trigger?
   **/
  bool hasTriggered( const edm::Event&,
         const edm::InputTag& results );

  /**
   * does InputPath have triggered?
   **/
  bool hasTriggered( const edm::Event&,
         const edm::InputTag& results,
         const edm::InputTag& path );

  /**
   * puts a list of all trigger paths to stdout
   **/
  void printTriggerNames( const edm::Event& event,
        const edm::InputTag& hlTriggerResults );

  /**
   * retrieve a list that contains all trigger path names
   **/
  std::vector<std::string> getAllTriggerNames( const edm::Event& event,
                                               const edm::InputTag& hlTriggerResults );

  /** rename variables names such that they are legal edm names!
   *  turns '_' and ':' into '.'
   **/
  std::string rename( const std::string& old );

  /**
   * Wrapper for StringCutObjectSelector
   **/
  template<class T>
  std::vector<T> vecselector( const std::vector<T>& input,
            const std::string& cutstring,
            const bool verbose = false )
  {
    std::vector<T> res;
    StringCutObjectSelector<T> select( cutstring );

    for(typename std::vector<T>::const_iterator it = input.begin();it!=input.end();it++)
      if (select(*it)) res.push_back(*it);
    
    if (verbose) std::cout<<"[selector<Vector<T>>] taken "<<res.size()<<" objects from "
        <<input.size()<<" cutstring "<<cutstring<<std::endl;
    return res;
  }


  /**
   * Wrapper for StringCutObjectSelector
   **/
  template <class T>
  void vecselector( const std::vector<T>& input,
        std::vector<T>& res,
        const std::string& cutstring,
        const bool verbose = false )
  {
    StringCutObjectSelector<T> select( cutstring );

    for(typename std::vector<T>::const_iterator it = input.begin();it!=input.end();it++)
      if (select(*it)) res.push_back(*it);
    
    if (verbose) std::cout<<"[selector<Vector<T>>] taken "<<res.size()<<" objects from "
        <<input.size()<<" cutstring "<<cutstring<<std::endl;
  }

  /**
   * Wrapper for StringCutObjectSelector
   **/
  template <class T>
  void ptrVecSelector( const std::vector<T>& input,
           std::vector<const T*>& res,
           const std::string& cutstring,
           const bool verbose = false )
  {
    StringCutObjectSelector<T> select( cutstring );

    for(typename std::vector<T>::const_iterator it = input.begin();it!=input.end();++it)
      if (select(*it)) res.push_back(&*it);
    
    if (verbose) std::cout<<"[selector<Vector<T>>] taken "<<res.size()<<" objects from "
        <<input.size()<<" cutstring "<<cutstring<<std::endl;
  }


  template <class T>
  void ptrVecSelector( const std::vector<const T*>& input,
           std::vector<const T*>& res,
           const std::string& cutstring,
           const bool verbose = false )
  {
    StringCutObjectSelector<T> select( cutstring );

    for(typename std::vector<const T*>::const_iterator it = input.begin();it!=input.end();++it)
      if (select(**it)) res.push_back(*it);
    
    if (verbose) std::cout<<"[selector<Vector<T>>] taken "<<res.size()<<" objects from "
        <<input.size()<<" cutstring "<<cutstring<<std::endl;
  }

  template <class T>
  bool selector( const T& input, const std::string& cutstring )
  { 
    StringCutObjectSelector< reco::Particle > select( cutstring );
    return select(input);
  }

#ifndef FWLITE_HEADER_PROTECT

  /**
   * Initialize a producer for writing a vector of a certain data-type to file.
   **/
  template<class Type>
  void initProducer( edm::EDProducer& producer, std::string tag )
  {
    ( producer.produces<Type>( tag ) ).setBranchAlias( tag );
  }

#endif

  /**
   * retrieve a single object by name
   **/
  template <class T>
  T getObj( const edm::Event& event, const edm::InputTag& name )
  {
    edm::Handle< std::vector<T> > objHandle;
    event.getByLabel( name, objHandle);
    int nobjs = objHandle->size();
    if ( nobjs == 0 ) return  T();
    return (*objHandle)[0];
  }

  /**
   * retrieve a vector of objects by name
   **/
  template<class T>
  std::vector<T> getObjs( const edm::Event& event, const edm::InputTag& name,
        const std::string& cutstring = "", const bool verbose = false )
  {
    // std::cout << "[EdmHelper] getObjs begins" <<  std::endl;
    edm::Handle< std::vector<T> > objsHandle;
    event.getByLabel( name, objsHandle );
    if ( !objsHandle.isValid() )
    {
      edm::LogError("EdmHelper") << "problem reading collection ``" << name << "''";
      return std::vector<T>();
    }
    std::vector<T> ret = vecselector<T>(*objsHandle, cutstring);
    sort( ret.begin(), ret.end(), MathHelper::greaterPt<T> );
    if (verbose) std::cout<<"[getObjs] taken "<<ret.size()<<" \""<<name.instance()<<"\" (\""<<name.label()<<"\") from "
                          <<objsHandle->size()<<", cutstring: "<<cutstring<<std::endl;
    // std::cout << "[EdmHelper] getObjs ends" << std::endl;
    return ret;
  }

  /**
   * retrieve a vector of objects by name
   **/
  template <class T>
  void getObjs( const edm::Event& event, const edm::InputTag& name, std::vector<const T*>& ret,
    const std::string& cutstring = "", const bool verbose = false )
  {
    ret.clear();

    edm::Handle< std::vector<T> > objsHandle;
    event.getByLabel( name, objsHandle );
    if ( !objsHandle.isValid() )
    {
      edm::LogError("EdmHelper") << "problem reading collection ``" << name << "''";
      return;
    }

    ret.reserve( objsHandle->size() );
    ptrVecSelector<T>(*objsHandle, ret, cutstring);
    sort( ret.begin(), ret.end(), MathHelper::ptrGreaterPt<T> );

    if (verbose) std::cout<<"[getObjs] taken "<<ret.size()<<" \""<<name.instance()<<"\" (\""<<name.label()<<"\") from "
                          <<objsHandle->size()<<", cutstring: "<<cutstring<<std::endl;
  }


  pat::Jet produceTaggedPseudoPatJet( const math::XYZTLorentzVector& p4,
              const std::string& bTagName, float bTagValue );


  template<class PatObject, class RecoObject>
  PatObject producePseudoPatObject( int charge, const math::XYZTLorentzVector& p4 )
  {
    RecoObject pseudoRecoObject;
    pseudoRecoObject.setCharge( charge );
    pseudoRecoObject.setP4( p4 );

    PatObject pseudoPatObject( pseudoRecoObject );
    return pseudoPatObject;
  }


  /**
   * Create a pseudo pat-object from a reco-candidate. Useful for filling MC-info into pat-objects.
   **/
  template<class PatObject, class RecoObject>
  PatObject producePseudoPatObject( const reco::Candidate & particle )
  {
    RecoObject pseudoRecoObject;
    pseudoRecoObject.setCharge( particle.charge() );
    pseudoRecoObject.setP4( particle.p4() );
    pseudoRecoObject.setMass( particle.mass() );
    pseudoRecoObject.setVertex( particle.vertex() );

    PatObject pseudoPatObject( pseudoRecoObject );
    return pseudoPatObject;
  }

  template<class PatObject, class RecoObject>
  PatObject producePseudoPatObject( const reco::Particle & particle )
  {
    RecoObject pseudoRecoObject;
    pseudoRecoObject.setCharge( particle.charge() );
    pseudoRecoObject.setP4( particle.p4() );
    pseudoRecoObject.setMass( particle.mass() );
    pseudoRecoObject.setVertex( particle.vertex() );

    PatObject pseudoPatObject( pseudoRecoObject );
    return pseudoPatObject;
  }

  /**
   * helper funtions for retrieving certain types of GenParticles from a given GenParticleRefVector
   **/
  std::vector<const reco::GenParticle*> getQuarks( const reco::GenParticleRefVector& particles );
  const reco::GenParticle* getQuark( const reco::GenParticleRefVector& particles, int absPdgId );
  const reco::GenParticle* getLepton( const reco::GenParticleRefVector& particles );
  const reco::GenParticle* getNeutrino( const reco::GenParticleRefVector& particles );


  /**
   * group 4-vectors into two hemispheres
   **/
  std::vector< std::vector<math::XYZTLorentzVector> >
  getHemisphereVecs( const edm::Event& event, const edm::InputTag& hemisphereTag, bool verbose = false );

//   /**
//    * split jets acc. to hemispheres
//    **/
//   bool groupHemJets( const std::vector<TaggedParticle>& jets, const math::XYZTLorentzVector leptonp4&,
//          std::vector<TaggedParticle> lepJets, std::vector<TaggedParticle> hadJets );

  /**
   * get leading lepton
   **/
  void getLepton( const std::vector<const pat::Electron*>& electrons,
      const std::vector<const pat::Muon*>& muons,
      std::vector<const reco::Candidate*>& result,
      int nlead, const std::string& cutstring, bool verbose );

}

#endif
