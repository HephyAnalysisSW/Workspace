#include "FWCore/Framework/interface/MakerMacros.h"
#include "Workspace/HEPHYCMSSWTools/plugins/ElectronTupelizer.h"
#include "Workspace/HEPHYCMSSWTools/interface/EdmHelper.h"
#include "Workspace/HEPHYCMSSWTools/interface/ElectronEffectiveArea.h"
#include "PhysicsTools/PatAlgos/plugins/PATElectronProducer.h"
#include "RecoEgamma/EgammaTools/interface/ConversionTools.h"

using namespace std;

namespace {
  string prefix ("[ElectronTupelizer] ");
}

ElectronTupelizer::~ElectronTupelizer() {}

ElectronTupelizer::ElectronTupelizer( const edm::ParameterSet & pset):
  Tupelizer(pset),
  params_ ( pset ),
  verbose_ ( pset.getUntrackedParameter< bool >("verbose")),
  input_ ( pset.getUntrackedParameter< edm::InputTag >("input") ),
  ptThreshold_ (pset.getUntrackedParameter< double >("ptThreshold") ),
  vertices_ ( pset.getUntrackedParameter< edm::InputTag >("vertices") ),
  elePFRelIsoAreaCorrected_ ( pset.getUntrackedParameter< bool >("elePFRelIsoAreaCorrected") ),
  eleRho_ ( pset.getUntrackedParameter< edm::InputTag >("eleRho") ) 
{
  addAllVars();
}


void ElectronTupelizer::beginJob ( )
{
  cout << "[ElectronTupelizer] starting ... " << endl;
}

void ElectronTupelizer::endJob()
{
  cout << endl;
  cout << "[ElectronTupelizer] shutting down ... " << endl;
}

void ElectronTupelizer::beginRun ( edm::Run & iRun, edm::EventSetup const & iSetup )
{
}


void ElectronTupelizer::produce( edm::Event & ev, const edm::EventSetup & setup) {
  ev_ = &ev;
  vector<pat::Electron> electrons (EdmHelper::getObjs<pat::Electron>(ev, input_));
  bool isData (ev.eventAuxiliary().isRealData());
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
  math::XYZPoint vertexPosition(NAN, NAN, NAN);
  if (goodVertices.size()>0) {
    vertexPosition = goodVertices[0].position();
  }


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

  for (vector<pat::Electron>::const_iterator ele = electrons.begin(); ele!=electrons.end();ele++){
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
      cout<<"[ele "<< ele - electrons.begin()<<"] "<<endl;//<<boolalpha<<"isBarrel? "<<isBarrel<<" isEndcap? "<<isEndcap<<" isGood "<<isGood<<" isGoodVeto "<<isGoodVeto<<endl;
      cout<<" pt "<<ele->pt()<<" eta "<<ele->superCluster()->eta()<<" phi "<<ele->phi()<<" oneOverEMinusOneOverP "<<oneOverEMinusOneOverP<<" sigmaIEtaIEta "<<sigmaIEtaIEta <<" pfRelIso "<<pfRelIso<<" HoE "<<HoE<<endl;
      cout<<" DPhi "<<DPhi<<" DEta "<<DEta<<" missingHits "<<missingHits<<" passConversionRejection "<<passConversionRejection<<" dxy "<<dxy<<" dz "<<dz<<endl;//" pfDeltaPT "<<deltapT<<endl;
      cout<<" chargedHadronIso03 "<<charged<<" neutralHadronIso03 "<<neutral<<" gammaIso03 "<< photon<<" Aeff "<<Aeff<<" rho "<<*eleRho<<endl;
      cout<<" ecalIso "<<ele->ecalIso()<<" hcalIso "<<ele->hcalIso()<<" trackIso "<<ele->trackIso()<<endl;
    }
    if(pt > ptThreshold_) //j#
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

void ElectronTupelizer::addAllVars( )
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

DEFINE_FWK_MODULE(ElectronTupelizer);
