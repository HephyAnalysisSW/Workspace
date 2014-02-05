#ifndef Workspace_EarlyDataAnalysis_SUSYTupelizer_H
#define Workspace_EarlyDataAnalysis_SUSYTupelizer_H

#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/FWLite/interface/Handle.h"
#include "DataFormats/JetReco/interface/CaloJet.h"
#include "DataFormats/JetReco/interface/JetID.h"
#include "DataFormats/JetReco/interface/PFJet.h"
#include "DataFormats/Math/interface/Point3D.h"
#include "DataFormats/METReco/interface/CaloMET.h"
#include "DataFormats/MuonReco/interface/MuonFwd.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"

#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/MHT.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Isolation.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/Scalers/interface/DcsStatus.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"

#include "MagneticField/Engine/interface/MagneticField.h"
#include "MagneticField/Records/interface/IdealMagneticFieldRecord.h"

#include "PhysicsTools/SelectorUtils/interface/JetIDSelectionFunctor.h"
#include "PhysicsTools/SelectorUtils/interface/SimpleCutBasedElectronIDSelectionFunctor.h"

#include "SimGeneral/HepPDTRecord/interface/ParticleDataTable.h"

#include "Workspace/HEPHYCommonTools/interface/RecoHelper.h"
#include "Workspace/HEPHYCommonTools/interface/MathHelper.h"
#include "Workspace/HEPHYCommonTools/interface/ModelParameters.h"

#include "TNtuple.h"
#include "TTree.h"
#include <vector>
#include <typeinfo>
#include <string>


class SUSYTupelizer : public edm::EDProducer
{
public:

//  template <class T> variable {
//    public:
//      variable(std::string name, T defaultValue) {name_ = name; defaultValue_ = defaultValue;}
//      std::string name_;
//      T defaultValue_;
//  };
  std::vector<std::string> variables;
//  std::map<std::string, void *>     defaultObjects;
  std::map<std::string, std::string>  types;
//  std::map<std::string, bool> hasbeenWritten;
  int prescale(edm::Event & ev, const edm::EventSetup & setup, std::string hlt);


  void addVar(const std::string & name) {
    std::string varname = name;
    std::string tname = name;
    std::size_t spos = varname.find('/');
    varname.resize(spos);
    variables.push_back(varname);
    std::string fullvarname("");
    if (defaultAlias_) {
      fullvarname = varname;
    } else {
      fullvarname = moduleLabel_+"_"+varname;
    }
    tname.replace(0, spos+1, "");
//    std::cout<<"Name: "<<varname<<" Type: "<<tname<<std::endl;
    types[varname] = tname; 
    if (tname.find("[]")!=std::string::npos) {
      switch (tname.at(0)) {
              case 'B' : {produces<std::vector<Char_t> >(varname)    .setBranchAlias(fullvarname); break;}
              case 'b' : {produces<std::vector<UChar_t> >(varname)   .setBranchAlias(fullvarname); break;}
              case 'S' : {produces<std::vector<Short_t> >(varname)   .setBranchAlias(fullvarname); break;}
              case 's' : {produces<std::vector<UShort_t> >(varname)  .setBranchAlias(fullvarname); break;}
              case 'I' : {produces<std::vector<Int_t> >(varname)     .setBranchAlias(fullvarname); break;}
              case 'i' : {produces<std::vector<UInt_t> >(varname)    .setBranchAlias(fullvarname); break;}
              case 'F' : {produces<std::vector<Float_t> >(varname)   .setBranchAlias(fullvarname); break;}
              case 'D' : {produces<std::vector<Double_t> >(varname)  .setBranchAlias(fullvarname); break;}
              case 'L' : {produces<std::vector<Long64_t> >(varname)  .setBranchAlias(fullvarname); break;}
              case 'l' : {produces<std::vector<ULong64_t> >(varname) .setBranchAlias(fullvarname); break;}
              case 'O' : {produces<std::vector<Bool_t> >(varname)    .setBranchAlias(fullvarname); break;}
      }
    } else {
      switch (tname.at(0)) {
              case 'B' : {produces<Char_t>(varname)    .setBranchAlias(fullvarname); break;}
              case 'b' : {produces<UChar_t>(varname)   .setBranchAlias(fullvarname); break;}
              case 'S' : {produces<Short_t>(varname)   .setBranchAlias(fullvarname); break;}
              case 's' : {produces<UShort_t>(varname)  .setBranchAlias(fullvarname); break;}
              case 'I' : {produces<Int_t>(varname)     .setBranchAlias(fullvarname); break;}
              case 'i' : {produces<UInt_t>(varname)    .setBranchAlias(fullvarname); break;}
              case 'F' : {produces<Float_t>(varname)   .setBranchAlias(fullvarname); break;}
              case 'D' : {produces<Double_t>(varname)  .setBranchAlias(fullvarname); break;}
              case 'L' : {produces<Long64_t>(varname)  .setBranchAlias(fullvarname); break;}
              case 'l' : {produces<ULong64_t>(varname) .setBranchAlias(fullvarname); break;}
              case 'O' : {produces<Bool_t>(varname)    .setBranchAlias(fullvarname); break;}
      }
    }
//    produces<T> (varname.resize(varname.size()-2));

//    T * defObject_ptr =  new T(def); //use copy constructor
//    defaultObjects[name] = defObject_ptr;
//    defaultTypes[name] = &typeid(T);
//    hasbeenWritten[name] = false;
  }
 

  template < class U > 
  void putVar(const std::string & name, U value) {
//    std::cout<<"Name: "<<name<<" typePtr: "<<defaultTypes[name]<<std::endl;
//    dynamic_cast<defaultTypes[name]> 
    std::auto_ptr<U> myvar( new U );
    *myvar = value;
//    std::type_info const * mytype (defaultTypes[name]);
//    dynamic_cast<mytype> (&value);
    ev_->put<U>(myvar, name);
//    hasbeenWritten[name] = true;
  }
//  template < class U > 
//  void putVar(const std::string & name, std::vector<U> value) {
//    std::auto_ptr<U> myvar( new std::vector<U> );
//    *myvar = value;
//    ev_->put<std::vector<U> >(myvar, name);
//  }
  template <class U>  
  void put (const std::string & name, std::vector< U > & values) {
    if (types[name].find("[]")!=std::string::npos) {
        putVar<std::vector<U> >(name, values);   
    } else {
      std::cout<<"[SUSYTupelizer] Warning! Var:" << name<<"  Type "<<types[name]<<" can't be filled with std::vector<> !"<<std::endl;
    }
  }

  template < class T > 
  void put (const std::string & name, T value) {
//    std::cout<<"Put typename      :"<<name<<" Type: "<<types[name]<<"X"<<std::endl;
//    std::cout<<"Put typename.at(0):"<<name<<" Type: "<<types[name].at(0)<<"X"<<std::endl;
    try {
      switch (types[name].at(0)) {
              case 'B' : {putVar<Char_t>(name, value);    break;}
              case 'b' : {putVar<UChar_t>(name, value);   break;}
              case 'S' : {putVar<Short_t>(name, value);   break;}
              case 's' : {putVar<UShort_t>(name, value);  break;}
              case 'I' : {putVar<Int_t>(name, value);     break;}
              case 'i' : {putVar<UInt_t>(name, value);    break;}
              case 'F' : {putVar<Float_t>(name, value);   break;}
              case 'D' : {putVar<Double_t>(name, value);  break;}
              case 'L' : {putVar<Long64_t>(name, value);  break;}
              case 'l' : {putVar<ULong64_t>(name, value); break;}
              case 'O' : {putVar<Bool_t>(name, value);    break;}
      }
    } catch (cms::Exception & e) {
        std::cout  << "[SUSYTupelizer] Error in put() for variable "<<name<<" (forgot the addVar?) with type "<<types[name]<< e.what() << std::endl;
    }

  }

  edm::Event * ev_; 
//  template < class T > 
//  void putDef(edm::Event & ev, const std::string & name) {
//    std::auto_ptr<T> myvar( new T );
//    *myvar = value;
//    ev.put<T>(myvar, name);
//    hasbeenWritten[name] = true;
//  }

  explicit SUSYTupelizer ( const edm::ParameterSet & );
  ~SUSYTupelizer();

  void beginJob(  );
  void beginRun ( edm::Run & iRun, edm::EventSetup const& iSetup );
  void endJob();

  void produce( edm::Event &, const edm::EventSetup &  );

  void addAllVars( );

  edm::ParameterSet params_;
  bool verbose_;

  std::string triggerCollection_;
  edm::InputTag patJets_;
  edm::InputTag patMET_;
//  edm::InputTag rawMET_;
//  edm::InputTag type01MET_;
//  edm::InputTag type1phiMET_;
//  edm::InputTag type01phiMET_;
  edm::InputTag patMuons_;
  edm::InputTag patElectrons_;
  edm::InputTag patTaus_;
  edm::InputTag vertices_;

  double lowLeptonPtThreshold_;
  double softJetPtThreshold_;

  // steerables Mu:
  double muonPt_;
  double muonEta_;
  bool muonIsGlobal_;
  bool muonHasPFMatch_;
  bool muonIsPF_;
  double muonNormChi2_;
  int muonNumValMuonHits_;
  int muonNumMatchedStations_;
  int muonNumPixelHits_;
  int muonNumTrackerLayersWithMeasurement_;
  double muonPFRelIso_;
  double muonPFRelIsoDeltaBeta_;
  double muonDxy_;
  double muonDz_;


  // steerables VetoMu:
  double vetoMuonPt_;
  double vetoMuonEta_;
  bool vetoMuonIsGlobalOrIsTracker_;
  bool vetoMuonIsPF_;
  double vetoMuonPFRelIso_;
  double vetoMuonPFRelIsoDeltaBeta_;
  double vetoMuonDxy_;
  double vetoMuonDz_;

  // steerables Ele:
  double elePt_;
  double eleEta_;
  double eleOneOverEMinusOneOverP_;
  double eleDxy_;
  double eleDz_;
  double elePFRelIsoBarrel_;
  double elePFRelIsoEndcap_;
  bool   elePFRelIsoAreaCorrected_;
  edm::InputTag   eleRho_;
  double eleSigmaIEtaIEtaBarrel_;
  double eleSigmaIEtaIEtaEndcap_;
  double eleHoEBarrel_;
  double eleHoEEndcap_;
  double eleDPhiBarrel_;
  double eleDPhiEndcap_;
  double eleDEtaBarrel_;
  double eleDEtaEndcap_;
  int    eleMissingHits_;
  bool   eleConversionRejection_;
  bool   eleHasPFMatch_;

  // steerables veto Ele:
  double vetoElePt_;
  double vetoEleEta_;
  double vetoEleDxy_;
  double vetoEleDz_;
  double vetoElePFRelIsoBarrel_;
  double vetoElePFRelIsoEndcap_;
  double vetoEleSigmaIEtaIEtaBarrel_;
  double vetoEleSigmaIEtaIEtaEndcap_;
  double vetoEleHoEBarrel_;
  double vetoEleHoEEndcap_;
  double vetoEleDPhiBarrel_;
  double vetoEleDPhiEndcap_;
  double vetoEleDEtaBarrel_;
  double vetoEleDEtaEndcap_;

  double minJetPt_;
  double maxJetEta_;
  std::string btag_;
  double btagWP_;
  std::string btagPure_;
  double btagPureWP_;
  bool hasL1Trigger_;
  edm::InputTag puJetIdCutBased_;
  edm::InputTag puJetIdFull53X_;
  edm::InputTag puJetIdMET53X_;

  private:
  bool hlt_initialized_;
  std::vector<std::string> HLT_names_;
  HLTConfigProvider hltConfig_;
  ModelParameters modelParameters_;
  std::string moduleLabel_;

  bool addRA4AnalysisInfo_;
  bool addTriggerInfo_;
  std::vector<std::string> triggersToMonitor_, trigNames_, prescNames_, metsToMonitor_;
  bool addMetUncertaintyInfo_;
  bool addFullBTagInfo_;
  bool addFullJetInfo_;
  bool addFullLeptonInfo_;
//  bool addFullMETInfo_;
  bool addFullMuonInfo_;
  bool addFullEleInfo_;
  bool addFullTauInfo_;
  bool addGeneratorInfo_;
  bool addMSugraOSETInfo_;
  bool addPDFWeights_;

  bool defaultAlias_;
};
#endif

//  template <class O>
//  const O * getObjects (const edm::Event& event, const std::string & name, const bool & verbose = true) const {
//    edm::Handle< O > handle;
//    try {
//      event.getByLabel(name.c_str(), handle);
//    } catch (cms::Exception & e ) {
//      std::cout << "[SUSYTupelizer] error: " << e.what() << std::endl;
//    }
//    if (handle.isValid()) {
//      return &(*handle);
//    } else {
//      if (verbose) std::cout << "[SUSYTupelizer] " << " edm::Handle not valid for "<<name<<std::endl;
//      return NULL;
//    }
//  }


