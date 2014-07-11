#include "FWCore/Framework/interface/MakerMacros.h"
#include "Workspace/HEPHYCMSSWTools/plugins/JetTupelizer.h"
#include "Workspace/HEPHYCMSSWTools/interface/EdmHelper.h"
#include <SimDataFormats/GeneratorProducts/interface/HepMCProduct.h>
#include <SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h>
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "DataFormats/JetReco/interface/PileupJetIdentifier.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "JetMETCorrections/Objects/interface/JetCorrectionsRecord.h"
#include "PhysicsTools/SelectorUtils/interface/PFJetIDSelectionFunctor.h"

using namespace std;

namespace {

  string prefix ("[JetTupelizer] ");
}

JetTupelizer::~JetTupelizer() {}

JetTupelizer::JetTupelizer( const edm::ParameterSet & pset):
  Tupelizer(pset),
  params_ ( pset ),
  verbose_ ( pset.getUntrackedParameter< bool >("verbose")),
  input_ ( pset.getUntrackedParameter< edm::InputTag >("input") ),
  ptThreshold_ (pset.getUntrackedParameter< double >("ptThreshold") ),
  btag_ ( pset.getUntrackedParameter< std::string >("btag") ),
  puJetIdCutBased_( pset.getUntrackedParameter< edm::InputTag >("puJetIdCutBased") ),
  puJetIdFull53X_( pset.getUntrackedParameter< edm::InputTag >("puJetIdFull53X") ),
  puJetIdMET53X_( pset.getUntrackedParameter< edm::InputTag >("puJetIdMET53X") )
{
  addAllVars();
}

void JetTupelizer::beginJob ( )
{
  cout << "[JetTupelizer] starting ... " << endl;
}

void JetTupelizer::endJob()
{
  cout << endl;
  cout << "[JetTupelizer] shutting down ... " << endl;
}

void JetTupelizer::beginRun ( edm::Run & iRun, edm::EventSetup const & iSetup )
{
}

void JetTupelizer::produce( edm::Event & ev, const edm::EventSetup & setup) {
  ev_ = &ev;
  bool isData(ev.eventAuxiliary().isRealData());

  edm::Handle< edm::View<pat::Jet > > jets;
  ev.getByLabel( input_, jets );
  JetIDSelectionFunctor jetPURE09LOOSE(JetIDSelectionFunctor::PURE09, JetIDSelectionFunctor::LOOSE );
  PFJetIDSelectionFunctor pfjetFIRSTDATALOOSE( PFJetIDSelectionFunctor::FIRSTDATA, PFJetIDSelectionFunctor::LOOSE );
  edm::ESHandle<JetCorrectorParametersCollection> JetCorParColl;
  setup.get<JetCorrectionsRecord>().get("AK5PF",JetCorParColl);
  JetCorrectorParameters const & JetCorPar = (*JetCorParColl)["Uncertainty"];
  JetCorrectionUncertainty *jecUnc = new JetCorrectionUncertainty(JetCorPar);
  edm::Handle<edm::ValueMap<int> > cutbasedPUJetIdFlag;
  ev.getByLabel(puJetIdCutBased_, cutbasedPUJetIdFlag);
  edm::Handle<edm::ValueMap<int> > full53XPUJetIdFlag;
  ev.getByLabel(puJetIdFull53X_,full53XPUJetIdFlag);
  edm::Handle<edm::ValueMap<int> > met53XPUJetIdFlag;
  ev.getByLabel(puJetIdMET53X_,met53XPUJetIdFlag);

  double delta_met_x (0.), delta_met_y(0.);
  double delta_met_x_unclustered (0.), delta_met_y_unclustered(0.);
  std::vector<float> jetspt, jetsptUncorr, jetseta, jetsbtag, jetsSVMass, jetsphi, jetsUnc, jetsMass2;
  std::vector<int> jetsparton, jetsID, jetsCutBasedPUJetIDFlag, jetsMET53XPUJetIDFlag, jetsFull53XPUJetIDFlag;

  std::vector<float> jetsChargedHadronEnergyFraction, jetsNeutralHadronEnergyFraction, jetsChargedEmEnergyFraction, jetsNeutralEmEnergyFraction, jetsPhotonEnergyFraction, jetsElectronEnergyFraction, jetsMuonEnergyFraction, jetsHFHadronEnergyFraction, jetsHFEMEnergyFraction;
  for (unsigned i = 0; i<jets->size();i++) {
    const pat::Jet & jet = jets->at(i);
    bool jetID;
    if ( jet.isPFJet() ) {
    //https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetID

      jetID = pfjetFIRSTDATALOOSE(jet);

    } else {
      jetID = jetPURE09LOOSE(jet);
    }

// bool jet_is_good = (jetID and (jet.pt() >= minJetPt_) and (fabs( jet.eta() ) <= maxJetEta_));
    bool jet_is_soft = (jet.pt() >= ptThreshold_);
    if (jet_is_soft) {
      jetspt.push_back(jet.pt());
      jetsptUncorr.push_back(jet.correctedJet("Uncorrected").pt());
      jetseta.push_back(jet.eta());
      jetsphi.push_back(jet.phi());
      jetsMass2.push_back(jet.p4().mass2());
      if (!isData) {
        jetsparton.push_back(jet.partonFlavour());
      } else {jetsparton.push_back(0);}
      jetsbtag.push_back(jet.bDiscriminator(btag_));

      jetsCutBasedPUJetIDFlag.push_back((*cutbasedPUJetIdFlag)[jets->refAt(i)]);
      jetsMET53XPUJetIDFlag.push_back((*met53XPUJetIdFlag)[jets->refAt(i)]);
      jetsFull53XPUJetIDFlag.push_back((*full53XPUJetIdFlag)[jets->refAt(i)]);
      const reco::SecondaryVertexTagInfo * SVtagInfo = jet.tagInfoSecondaryVertex();
      bool hasSVMass(false);
      if(SVtagInfo){
        if(SVtagInfo->nVertices()>0){
          const reco::Vertex &SVertex=SVtagInfo->secondaryVertex(0);
          jetsSVMass.push_back(SVertex.p4().M());
          hasSVMass = true;
        }
      }
      if (not hasSVMass) jetsSVMass.push_back(-1.);

      jecUnc->setJetEta(jet.eta());
      jecUnc->setJetPt(jet.pt()); // here you must use the CORRECTED jet pt
      double unc = (jet.pt() > 10. && fabs(jet.eta())<5.) ? jecUnc->getUncertainty(true) : 0.1;
      jetsUnc.push_back(unc);
      jetsID.push_back(jetID);
      jetsChargedHadronEnergyFraction.push_back(jet.chargedHadronEnergyFraction());
      jetsNeutralHadronEnergyFraction.push_back(jet.neutralHadronEnergyFraction());
      jetsChargedEmEnergyFraction.push_back(jet.chargedEmEnergyFraction());
      jetsNeutralEmEnergyFraction.push_back(jet.neutralEmEnergyFraction());
      jetsPhotonEnergyFraction.push_back(jet.photonEnergyFraction());
      jetsElectronEnergyFraction.push_back(jet.electronEnergyFraction());
      jetsMuonEnergyFraction.push_back(jet.muonEnergyFraction());
      jetsHFHadronEnergyFraction.push_back(jet.HFHadronEnergyFraction());
      jetsHFEMEnergyFraction.push_back(jet.HFEMEnergyFraction());
    }
    
    if ((verbose_) and (jet.pt() > ptThreshold_)) cout<<"[jet "<<i<<"] "<<" pt "<<jet.pt()<<" eta "<<jet.eta()<<" phi "<<jet.phi()<<boolalpha<<" jetID? "<<jetID<<endl;//" jetID+pt+eta cut?"<< jet_is_good <<endl;//" passes Ele c.c? "<<jetPassesEleCleaning<<" passes Mu c.c? "<<jetPassesMuCleaning<<endl;
    jecUnc->setJetEta(jet.eta());
    jecUnc->setJetPt(jet.pt()); // here you must use the CORRECTED jet pt
    double unc = (jet.pt() > 10. && fabs(jet.eta()<5)) ? jecUnc->getUncertainty(true) : 0.1;
    pat::Jet scaledJet = jet;
    scaledJet.scaleEnergy(1+unc);
    delta_met_x += - scaledJet.px() + jet.px();
    delta_met_y += - scaledJet.py() + jet.py();
    if (jet.pt()<10.) {
      delta_met_x_unclustered += - scaledJet.px() + jet.px();
      delta_met_y_unclustered += - scaledJet.py() + jet.py();
    }
  }
  put("jetsPt", jetspt);
  put("jetsPtUncorr", jetsptUncorr);
  put("jetsEta", jetseta);
  put("jetsPhi", jetsphi);
  put("jetsMass2", jetsMass2);
  put("jetsParton", jetsparton);
  put("jetsBtag", jetsbtag);
  put("jetsSVMass", jetsSVMass);
  put("jetsUnc", jetsUnc);
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

  put("nsoftjets", jetspt.size());
  put("deltaMETx", delta_met_x);
  put("deltaMETy", delta_met_y);
  put("deltaMETxUnclustered", delta_met_x_unclustered);
  put("deltaMETyUnclustered", delta_met_y_unclustered);
  delete jecUnc;
}

void JetTupelizer::addAllVars( )
{
  addVar("jetsPt/F[]");
  addVar("jetsPtUncorr/F[]");
  addVar("jetsEta/F[]");
  addVar("jetsPhi/F[]");
  addVar("jetsMass2/F[]");
  addVar("jetsParton/I[]");
  addVar("jetsBtag/F[]");
  addVar("jetsSVMass/F[]");
  addVar("jetsUnc/F[]");
// addVar("jetsEleCleaned/I[]");
// addVar("jetsMuCleaned/I[]");
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
  addVar("nsoftjets/I"); // NAN);
  addVar("deltaMETx/F");
  addVar("deltaMETy/F");
  addVar("deltaMETxUnclustered/F");
  addVar("deltaMETyUnclustered/F");
}

DEFINE_FWK_MODULE(JetTupelizer);
