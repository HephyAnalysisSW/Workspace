#include "Workspace/HEPHYCommonTools/interface/RecoHelper.h"
#include "Workspace/HEPHYCommonTools/interface/MathHelper.h"
#include "Workspace/HEPHYCommonTools/interface/CombinatoricsHelper.h"
#include "Validation/EcalClusters/interface/AnglesUtil.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/RecoCandidate/interface/IsoDeposit.h"
// first implementation of the V+Jet group recommendations
// for muon and electron selection
// https://twiki.cern.ch/twiki//bin/view/CMS/VplusJets=

namespace RecoHelper
{
  using namespace std;
  string prefix("[RecoHelper] ");

  bool debug (false);

  double M3ofComb(const std::vector<math::XYZTLorentzVector> & comb){
    if (comb.size()==3) {return (comb[0]+comb[1]+comb[2]).mass();}
    else return NAN;
  }
  double PTofComb(const std::vector<math::XYZTLorentzVector> & comb){
    if (comb.size()==3) {return (comb[0]+comb[1]+comb[2]).pt();}
    else return NAN;
  }
  double pTSum(const std::vector<math::XYZTLorentzVector> & comb){
    if (comb.size()==3) {return (comb[0]+comb[1]+comb[2]).pt();}
    else return NAN;
  }
  struct greaterSumPt {
    bool operator()(const std::vector<math::XYZTLorentzVector> & c1, const std::vector<math::XYZTLorentzVector> & c2)
    {
      //cout<<prefix<<" sizes "<<c1.size()<<" "<<c2.size()<<endl;
      if ((c1.size()==3)&&(c2.size()==3))
      {
       return (pTSum(c1)>pTSum(c2));
      }
      else return false;
    };
  };

  std::vector<std::vector<math::XYZTLorentzVector> >
  jet3Combinations (const std::vector<math::XYZTLorentzVector> jets, const bool verbose) {
    MathHelper::samep4 samep4_;
    std::vector< std::vector<math::XYZTLorentzVector> > combinations(CombinatoricsHelper::makeCombinations(jets, 3, samep4_));
    greaterSumPt sortCrit;
    sort( combinations.begin(), combinations.end(), sortCrit);
    return combinations;
  }

  double
  M3base (const std::vector<math::XYZTLorentzVector> jetp4s, const bool verbose) {

    std::vector< std::vector<math::XYZTLorentzVector> > combinations = jet3Combinations(jetp4s, verbose);

    if (verbose){
      cout<<prefix<<"found "<<combinations.size()<<" combinations; first 3: "<<endl;
      int maxprint = 3;
      if (combinations.size()<3) maxprint = combinations.size();
      for (int i = 0; i<maxprint; i++) {
        cout<<prefix<<"combination "<<i<<" M3: "<<M3ofComb(combinations[i])<<" pT: "<<pTSum(combinations[i])<<endl;
      }
    }
    if (combinations.size()>0) {
      return M3ofComb(combinations[0]);
    } else return NAN;
  }



//  double
//  M3 (const std::vector<pat::Jet> & jets, const bool verbose) {
//
//    // get the Jet Lorentz-Vectors
//    std::vector<math::XYZTLorentzVector> jetp4s;
//    for (std::vector<pat::Jet >::const_iterator it =  jets.begin(); it !=  jets.end(); ++it)
//      jetp4s.push_back( it->p4() );
//
//    return M3base( jetp4s, verbose);
//  }

//  double
//  M3 (const std::vector<reco::Jet> & jets, const bool verbose) {
//
//    // get the Jet Lorentz-Vectors
//    std::vector<math::XYZTLorentzVector> jetp4s;
//    for (std::vector<reco::Jet >::const_iterator it =  jets.begin(); it !=  jets.end(); ++it)
//      jetp4s.push_back( it->p4() );
//
//    return M3base( jetp4s, verbose);
//  }
//
//  double
//  M3 (const std::vector<reco::CaloJet> & jets, const bool verbose) {
//
//    // get the Jet Lorentz-Vectors
//    std::vector<math::XYZTLorentzVector> jetp4s;
//    for (std::vector<reco::CaloJet >::const_iterator it =  jets.begin(); it !=  jets.end(); ++it)
//      jetp4s.push_back( it->p4() );
//
//    return M3base( jetp4s, verbose);
//  }



  double
  max3JetSumPhi (const std::vector<pat::Jet> jets, const bool verbose) {

    std::vector<math::XYZTLorentzVector> jetp4s;
    for (std::vector<pat::Jet >::const_iterator it =  jets.begin(); it !=  jets.end(); ++it)
      jetp4s.push_back( it->p4() );

    std::vector< std::vector<math::XYZTLorentzVector> > combinations = jet3Combinations(jetp4s, verbose);
      if (combinations.size()>0) {
      double res;
      res =     fabs(MathHelper::deltaR(combinations[0][0], combinations[0][1]))
             +  fabs(MathHelper::deltaR(combinations[0][0], combinations[0][2]))
             +  fabs(MathHelper::deltaR(combinations[0][1], combinations[0][2]));
      return res;
    } else return NAN;

  }

  double
  maxPt3 (const std::vector<pat::Jet> & jets, const bool verbose) {

    std::vector<math::XYZTLorentzVector> jetp4s;
    for (std::vector<pat::Jet >::const_iterator it =  jets.begin(); it !=  jets.end(); ++it)
      jetp4s.push_back( it->p4() );

    std::vector< std::vector<math::XYZTLorentzVector> > combinations = jet3Combinations(jetp4s, verbose);
    if (verbose){
      cout<<prefix<<"found "<<combinations.size()<<" combinations; first 3: "<<endl;
      int maxprint = 3;
      if (combinations.size()<3) maxprint = combinations.size();
      for (int i = 0; i<maxprint; i++) {
	cout<<prefix<<"combination "<<i<<" M3: "<<M3ofComb(combinations[i])<<" pT: "<<pTSum(combinations[i])<<endl;
      }
    }
    if (combinations.size()>0) {
      return PTofComb(combinations[0]);
    } else return NAN;

  }

  // V+Jet recommendations (from Single-Lepton SUSY (RA4) Note 15.12.2009)
  // without kinematic cuts pt, eta.
  bool
  vPlusJetsSelected (const pat::Muon& muon, const math::XYZPoint & beamSpotPosition, bool verbose)
  {
    bool isPromptTight = muon.isGood("GlobalMuonPromptTight");
    if ( !isPromptTight )
      return false;

    double relIso = (muon.ecalIso()+muon.hcalIso()+muon.trackIso())/muon.pt();
    if ( relIso >= 0.1 )
      return false;

    if ( muon.globalTrack().isNull() )
    {
      cout << "[RecoHelper::vPlusJetsSelected] no globalTrack?!?" << endl;
      return false; // we dont have a track or what?
    }
    // number of hits
    int nValHits = muon.globalTrack()->numberOfValidHits();
    if ( nValHits<11 )
      return false;

    // chi2/dof
    double chi2_ndof = muon.globalTrack()->chi2()/muon.globalTrack()->ndof();
    if (chi2_ndof >= 10.)
      return false;

    // d0
    double correctedD0 = muon.globalTrack()->dxy(beamSpotPosition);
    if ( fabs(correctedD0)>=0.2 )
      return false;
    // energy in veto cone
    const reco::IsoDeposit* ecalDeposit = muon.isoDeposit(pat::EcalIso);
    const reco::IsoDeposit* hcalDeposit = muon.isoDeposit(pat::HcalIso);
    float vetoEcal = 0.;
    float vetoHcal = 0.;
    if (ecalDeposit!=NULL)
      vetoEcal = ecalDeposit->candEnergy();
    if (hcalDeposit!=NULL)
      vetoHcal = hcalDeposit->candEnergy();

    if ( vetoEcal>=4 || vetoHcal>=6 )
      return false;

    if (verbose) {
      cout<<prefix<<"pt:            "<<muon.pt()<<endl;
      cout<<prefix<<"eta:           "<<muon.eta()<<endl;
      cout<<prefix<<"glbPromptTight:"<<boolalpha<<isPromptTight<<endl;
      cout<<prefix<<"nValHits:      "<<nValHits<<endl;
      cout<<prefix<<"chi2_ndof:     "<<chi2_ndof<<endl;
      cout<<prefix<<"fabs(corr_d0): "<<fabs(correctedD0)<<endl;
      cout<<prefix<<"relIso:        "<<relIso<<endl;
      cout<<prefix<<"ecalDeposit:   "<<vetoEcal<<endl;
      cout<<prefix<<"hcalDeposit:   "<<vetoHcal<<endl;
    }
    return true;
  }

  // V+Jet recommendations (from Single-Lepton SUSY (RA4) Note 15.12.2009)
  // without kinematic cuts pt, eta.
  bool
  vPlusJetsSelected (const pat::Muon& muon, const edm::Event& event, bool verbose)
  {
    // cout << "[RecoHelper] hu!" << endl;
    bool isPromptTight = muon.isGood("GlobalMuonPromptTight");
    if ( !isPromptTight )
	  return false;

    double relIso = (muon.ecalIso()+muon.hcalIso()+muon.trackIso())/muon.pt();
    if ( relIso >= 0.1 )
      return false;

    if ( muon.globalTrack().isNull() )
    {
      cout << "[RecoHelper] null track!?!? " << endl;
      return false;
    }
    // number of hits
    int nValHits = muon.globalTrack()->numberOfValidHits();
    if ( nValHits<11 )
      return false;

    // chi2/dof
    double chi2_ndof = muon.globalTrack()->chi2()/muon.globalTrack()->ndof();
    if (chi2_ndof >= 10.)
      return false;

    // d0
    edm::Handle<reco::BeamSpot> bsHandle_;
    event.getByLabel("offlineBeamSpot",bsHandle_);
    double correctedD0 = muon.globalTrack()->dxy(bsHandle_->position());
    if ( fabs(correctedD0)>=0.2 )
      return false;

    // energy in veto cone
    const reco::IsoDeposit* ecalDeposit = muon.ecalIsoDeposit();
    if ( ecalDeposit!=NULL )
      if ( ecalDeposit->candEnergy() >=4 ) return false;

    const reco::IsoDeposit* hcalDeposit = muon.hcalIsoDeposit();
    if ( hcalDeposit!=NULL )
      if ( hcalDeposit->candEnergy() >=6 ) return false;

    if (verbose) {
      cout<<prefix<<"pt:            "<<muon.pt()<<endl;
      cout<<prefix<<"eta:           "<<muon.eta()<<endl;
      cout<<prefix<<"glbPromptTight:"<<boolalpha<<isPromptTight<<endl;
      cout<<prefix<<"nValHits:      "<<nValHits<<endl;
      cout<<prefix<<"chi2_ndof:     "<<chi2_ndof<<endl;
      cout<<prefix<<"fabs(corr_d0): "<<fabs(correctedD0)<<endl;
      cout<<prefix<<"relIso:        "<<relIso<<endl;
      int ecalCand=0;
      if ( ecalDeposit ) ecalCand = ecalDeposit->candEnergy();
      cout<<prefix<<"ecalDeposit:   "<< ecalCand<<endl;
      int hcalCand=0;
      if ( hcalDeposit ) hcalCand = hcalDeposit->candEnergy();
      cout<<prefix<<"hcalDeposit:   " << hcalCand << endl;
    }
    return true;
  }

  bool
  aC3Selected (const pat::Muon& muon, const edm::Event& event, bool verbose)
  {
    if ( !muon.isGood("GlobalMuonPromptTight") )
      return false;

      // #tracker hits
    int trackerHits = muon.globalTrack()->hitPattern().numberOfValidTrackerHits();
    if ( trackerHits<11 )
      return false;

      //chi2/dof
    double chi2_ndof = muon.globalTrack()->chi2()/muon.globalTrack()->ndof();
    if (chi2_ndof >= 10.)
      return false;
      // d0
    edm::Handle<reco::BeamSpot> bsHandle_;
    event.getByLabel("offlineBeamSpot",bsHandle_);
    double correctedD0 = muon.globalTrack()->dxy(bsHandle_->position());
      // d0_beamspot = d0_mutrack - beamspot_x*sin(phi_mutrack) + beampot_y*cos(phi_mutrack)
    if ( fabs(correctedD0)>0.2 )  return false;

      // Subsystem Isolations
    double trackerIso = muon.trackIso();
    double ecalIso = muon.ecalIso();
    double hcalIso = muon.hcalIso();
    if ( (trackerIso>=6) || (ecalIso>=6) || (hcalIso>=6) )  return false;

    if (verbose) {
      cout<<prefix<<"TrackerHits:   "<<trackerHits<<endl;
      cout<<prefix<<"chi2_ndof:     "<<chi2_ndof<<endl;
      cout<<prefix<<"fabs(corr_d0): "<<fabs(correctedD0)<<endl;
      cout<<prefix<<"TrackerIsolation: " << trackerIso <<endl;
      cout<<prefix<<"ECalIsolation: " << ecalIso <<endl;
      cout<<prefix<<"HCalIsolation: " << hcalIso <<endl;
    }
    return true;
  }

  bool
  aC3Selected (const pat::Muon& muon, const math::XYZPoint & beamSpotPosition, bool verbose)
  {
    if ( !muon.isGood("GlobalMuonPromptTight") )
      return false;

      // #tracker hits
    int trackerHits = muon.globalTrack()->hitPattern().numberOfValidTrackerHits();
    if ( trackerHits<11 )
      return false;

      //chi2/dof
    double chi2_ndof = muon.globalTrack()->chi2()/muon.globalTrack()->ndof();
    if (chi2_ndof >= 10.)
      return false;

      // d0
    double correctedD0 = muon.globalTrack()->dxy( beamSpotPosition );
      // d0_beamspot = d0_mutrack - beamspot_x*sin(phi_mutrack) + beampot_y*cos(phi_mutrack)
    if ( fabs(correctedD0)>=0.2 )  return false;

      // Subsystem Isolations
    double trackerIso = muon.trackIso();
    double ecalIso = muon.ecalIso();
    double hcalIso = muon.hcalIso();
    if ( (trackerIso>=6) || (ecalIso>=6) || (hcalIso>=6) )  return false;

    if (verbose) {
      cout<<prefix<<"TrackerHits:   "<<trackerHits<<endl;
      cout<<prefix<<"chi2_ndof:     "<<chi2_ndof<<endl;
      cout<<prefix<<"fabs(corr_d0): "<<fabs(correctedD0)<<endl;
      cout<<prefix<<"TrackerIsolation: " << trackerIso <<endl;
      cout<<prefix<<"ECalIsolation: " << ecalIso <<endl;
      cout<<prefix<<"HCalIsolation: " << hcalIso <<endl;
    }
    return true;
  }

  // to be updated!!!
  // compatible with definitions at "https://twiki.cern.ch/twiki/bin/viewauth/CMS/SusyRA4SingleMuonProjectTable"
  // definitions in RA4 Note (15.12.2009) differentiate between selection and veto! (not included in this implementation!)
  // without kinematic cuts pt, eta.
  bool
  vPlusJetsSelected (const pat::Electron& electron, const math::XYZPoint & beamSpotPosition, bool verbose)
  {
    // electronID
    const char * eid = "simpleEleId80relIso";
    // const char * eid = "eidRobustTight";
    if ( electron.isElectronIDAvailable( eid ) ) {
      if (!(electron.electronID( eid ))) return false;
      }
    //for debugging pleasure
    else std::cout<<"[RecoHelper::vPlusJetsSelected] <pat::Electron> Warning: no "
         << eid << " collection" << std::endl;
        /// Returns true if a specific ID is available in this pat::Electron

    // isolation
    if ( (electron.ecalIso()+electron.hcalIso()+electron.trackIso())/electron.pt()>=0.1 )
      return false;

    // d0
    double correctedD0 = electron.gsfTrack()->dxy(beamSpotPosition);
    if ( fabs(correctedD0)>=0.2 )  return false;

    return true;
  }

  // to be updated!!!
  // compatible with definitions at "https://twiki.cern.ch/twiki/bin/viewauth/CMS/SusyRA4SingleMuonProjectTable"
  // definitions in RA4 Note (15.12.2009) differentiate between selection and veto! (not included in this implementation!)
  // without kinematic cuts pt, eta.
  bool
  vPlusJetsSelected (const pat::Electron& electron, const edm::Event& event, bool verbose)
  {
    // electronID
    const char * eid = "simpleEleId80relIso";
    // const char * eid = "eidRobustTight";
    if ( electron.isElectronIDAvailable( eid ) ) {
      if (!(electron.electronID( eid ))) return false;
      }
    //for debugging pleasure
    else std::cout<<"[RecoHelper::vPlusJetsSelected] <pat::Electron> Warning: no "
                  << eid << " collection"<<std::endl;
    /// Returns true if a specific ID is available in this pat::Electron

    // isolation
    if ( (electron.ecalIso()+electron.hcalIso()+electron.trackIso())/electron.pt()>=0.1 )
      return false;

    // d0
    edm::Handle<reco::BeamSpot> bsHandle_;
    event.getByLabel("offlineBeamSpot",bsHandle_);
    double correctedD0 = electron.gsfTrack()->dxy(bsHandle_->position());
    if ( fabs(correctedD0)>0.2 )  return false;

    return true;
  }

  float alphaT (std::vector<pat::Jet> & vec) {
    if (vec.size()>=2) {
      std::sort(vec.begin(), vec.end(), MathHelper::greaterPt<pat::Jet> );
      math::XYZTLorentzVector j1 = vec[0].p4();
      math::XYZTLorentzVector j2 = MathHelper::zeroVector();
      for (unsigned i = 1; i<vec.size(); i++)
        j2+=vec[i].p4();
      float j1_Et = j1.Et();
      float j2_Et = j2.Et();
      float mT_j1j2 = MathHelper::mT(j1, j2);
      if (j1_Et>j2_Et) {
        return j2_Et/mT_j1j2;
      } else {
        return j1_Et/mT_j1j2;
      }
    } else return NAN;
  }

  float
  alphaTHemi (const std::vector< std::vector<math::XYZTLorentzVector> >& hemis) {
    if (hemis.size()==2) {
      math::XYZTLorentzVector j1 = MathHelper::zeroVector();
      math::XYZTLorentzVector j2 = MathHelper::zeroVector();
      if (hemis[0].size()==0 || hemis[1].size()==0) return NAN;
      for (unsigned i = 0; i<hemis[0].size(); i++)
        j1 += hemis[0][i];
      for (unsigned i = 0; i<hemis[1].size(); i++)
        j2 += hemis[1][i];
      //switch if not in pT-order
      if (j1.Et()<j2.Et()) {
        math::XYZTLorentzVector pTemp = j1;
        j1 = j2;
        j2 = pTemp;
      }
      return j2.Et()/(MathHelper::mT(j1,j2));
    } else return NAN;
  }
  float
  deltaPhiHemi (const std::vector< std::vector<math::XYZTLorentzVector> >& hemis) {
    if (hemis.size()==2) {
      math::XYZTLorentzVector j1 = MathHelper::zeroVector();
      math::XYZTLorentzVector j2 = MathHelper::zeroVector();
      if (hemis[0].size()==0 || hemis[1].size()==0) return NAN;
      for (unsigned i = 0; i<hemis[0].size(); i++)
        j1 += hemis[0][i];
      for (unsigned i = 0; i<hemis[1].size(); i++)
        j2 += hemis[1][i];
      //switch if not in pT-order
      return MathHelper::deltaPhi(j1,j2);
    } else return NAN;
  }

  float
  chi2(std::vector<pat::Jet> jets, const pat::MET & met, const reco::Candidate & lepton) {
  //Sigmas from Finn Rebassoo's talk http://indico.cern.ch/conferenceDisplay.py?confId=60206
    double sigmamlepT(31.2);
    double sigmamhadT(25.0);
    double sigmamhadW(15.2);
    double mW(80.4);
    double mT(175.);
    if (jets.size()>4) jets.resize(4);
    if (jets.size()<4) return NAN;
    double lepPx = lepton.px();
    double lepPy = lepton.py();
    double lepPz = lepton.pz();
    double lepPt2 = lepton.pt()*lepton.pt();
    double lepE = lepton.energy();
    double METPx = met.px();
    double METPy = met.py();
    double MET   = met.pt();

    double A = mW*mW + 2.*(lepPx*METPx + lepPy*METPy);
    double c1 = .5*A*lepPz/lepPt2;
    double c2 = .5*lepE*sqrt(A*A-MET*MET*lepPt2)/lepPt2;
    double pz_neu_1 = c1+c2;
    double pz_neu_2 = c1-c2;
    double pE_neu_1 = sqrt(pz_neu_1*pz_neu_1+MET*MET);
    double pE_neu_2 = sqrt(pz_neu_2*pz_neu_2+MET*MET);
    if (debug) {
      for (unsigned i = 0; i<jets.size(); i++) {
        cout<<prefix<<"jet "<<i<<"  pT "<<jets[i].pt()<<endl;
      }
      cout<<prefix<<"lepton pT "<<lepton.pt()<<endl;
      cout<<prefix<<"met    pT "<<met.pt()<<endl;
    }
    pat::Jet found_lepB, found_hadB;
    std::vector<pat::Jet> found_hadW;
    double min_disc = 10E10;
    MathHelper::samep4 samep4_;
    std::vector<std::vector< pat::Jet > > tops = CombinatoricsHelper::makeCombinations(jets, 3, samep4_);
    for (unsigned i = 0; i<tops.size(); i++) {
      pat::Jet lepB = CombinatoricsHelper::complement(jets, tops[i])[0];
      math::XYZTLorentzVector lep_top1 = lepton.p4()+lepB.p4()+math::XYZTLorentzVector(METPx,METPy,pz_neu_1,pE_neu_1);
      math::XYZTLorentzVector lep_top2 = lepton.p4()+lepB.p4()+math::XYZTLorentzVector(METPx,METPy,pz_neu_2,pE_neu_2);
      double disc1 = fabs((lep_top1.mass()-mT)/sigmamlepT);
      double disc2 = fabs((lep_top2.mass()-mT)/sigmamlepT);
      if (debug) cout<<prefix<<"found two top candidates with discr. "<<disc1<<" and "<<disc2<<endl;
      double disc_lepW = (disc1<disc2)?disc1:disc2;

      std::vector<std::vector< pat::Jet > > Ws = CombinatoricsHelper::makeCombinations(tops[i], 2, samep4_);
      for (unsigned j=0; j<Ws.size(); j++) {
        pat::Jet hadB = CombinatoricsHelper::complement(tops[i],Ws[j])[0];
        double disc_hadW = fabs(((Ws[j][0].p4()+ Ws[j][1].p4()).mass() - mW)/sigmamhadW);
        double disc_hadT = fabs(((Ws[j][0].p4()+ Ws[j][1].p4()+hadB.p4()).mass() - mT)/sigmamhadT);
        double this_disc = disc_hadW + disc_hadT + disc_lepW;
        if (debug) {
          cout<<prefix<<"found candidate: "<<this_disc<<" disc_hadW "<<disc_hadW<<" disc_hadT "<<disc_hadT<<" disc_lepW "<<disc_lepW<<endl;
          cout<<prefix<<"lepB pt "<<lepB.pt()<<endl;
          cout<<prefix<<"hadB pt "<<hadB.pt()<<endl;
          cout<<prefix<<"lj1  pt "<<Ws[j][0].pt()<<endl;
          cout<<prefix<<"lj2  pt "<<Ws[j][1].pt()<<endl;
        }
        if (this_disc < min_disc) {
          min_disc = this_disc;
          found_lepB = lepB; found_hadB = hadB;
          found_hadW = Ws[j];
          if (debug) cout<<prefix<<"--> better disc!"<<endl;
        }
      }
    }
    return min_disc;
  }



  float
  chi2(std::vector<pat::Jet> jets, const pat::MET & met, const math::XYZTLorentzVector & lepton) {
    //Sigmas from Finn Rebassoo's talk http://indico.cern.ch/conferenceDisplay.py?confId=60206
    double sigmamlepT(31.2);
    double sigmamhadT(25.0);
    double sigmamhadW(15.2);
    double mW(80.4);
    double mT(175.);
    if (jets.size()>4) jets.resize(4);
    if (jets.size()<4) return NAN;
    double lepPx = lepton.px();
    double lepPy = lepton.py();
    double lepPz = lepton.pz();
    double lepPt2 = lepton.pt()*lepton.pt();
    double lepE = lepton.energy();
    double METPx = met.px();
    double METPy = met.py();
    double MET   = met.pt();

    double A = mW*mW + 2.*(lepPx*METPx + lepPy*METPy);
    double c1 = .5*A*lepPz/lepPt2;
    double c2 = .5*lepE*sqrt(A*A-MET*MET*lepPt2)/lepPt2;
    double pz_neu_1 = c1+c2;
    double pz_neu_2 = c1-c2;
    double pE_neu_1 = sqrt(pz_neu_1*pz_neu_1+MET*MET);
    double pE_neu_2 = sqrt(pz_neu_2*pz_neu_2+MET*MET);
    if (debug) {
      for (unsigned i = 0; i<jets.size(); i++) {
        cout<<prefix<<"jet "<<i<<"  pT "<<jets[i].pt()<<endl;
      }
      cout<<prefix<<"lepton pT "<<lepton.pt()<<endl;
      cout<<prefix<<"met    pT "<<met.pt()<<endl;
    }
    pat::Jet found_lepB, found_hadB;
    std::vector<pat::Jet> found_hadW;
    double min_disc = 10E10;
    MathHelper::samep4 samep4_;
    std::vector<std::vector< pat::Jet > > tops = CombinatoricsHelper::makeCombinations(jets, 3, samep4_);
    for (unsigned i = 0; i<tops.size(); i++) {
      pat::Jet lepB = CombinatoricsHelper::complement(jets, tops[i])[0];
      math::XYZTLorentzVector lep_top1 = lepton+lepB.p4()+math::XYZTLorentzVector(METPx,METPy,pz_neu_1,pE_neu_1);
      math::XYZTLorentzVector lep_top2 = lepton+lepB.p4()+math::XYZTLorentzVector(METPx,METPy,pz_neu_2,pE_neu_2);
      double disc1 = fabs((lep_top1.mass()-mT)/sigmamlepT);
      double disc2 = fabs((lep_top2.mass()-mT)/sigmamlepT);
      if (debug) cout<<prefix<<"found two top candidates with discr. "<<disc1<<" and "<<disc2<<endl;
      double disc_lepW = (disc1<disc2)?disc1:disc2;

      std::vector<std::vector< pat::Jet > > Ws = CombinatoricsHelper::makeCombinations(tops[i], 2, samep4_);
      for (unsigned j=0; j<Ws.size(); j++) {
        pat::Jet hadB = CombinatoricsHelper::complement(tops[i],Ws[j])[0];
        double disc_hadW = fabs(((Ws[j][0].p4()+ Ws[j][1].p4()).mass() - mW)/sigmamhadW);
        double disc_hadT = fabs(((Ws[j][0].p4()+ Ws[j][1].p4()+hadB.p4()).mass() - mT)/sigmamhadT);
        double this_disc = disc_hadW + disc_hadT + disc_lepW;
        if (debug) {
          cout<<prefix<<"found candidate: "<<this_disc<<" disc_hadW "<<disc_hadW<<" disc_hadT "<<disc_hadT<<" disc_lepW "<<disc_lepW<<endl;
          cout<<prefix<<"lepB pt "<<lepB.pt()<<endl;
          cout<<prefix<<"hadB pt "<<hadB.pt()<<endl;
          cout<<prefix<<"lj1  pt "<<Ws[j][0].pt()<<endl;
          cout<<prefix<<"lj2  pt "<<Ws[j][1].pt()<<endl;
        }
        if (this_disc < min_disc) {
          min_disc = this_disc;
          found_lepB = lepB; found_hadB = hadB;
          found_hadW = Ws[j];
          if (debug) cout<<prefix<<"--> better disc!"<<endl;
        }
      }
    }
    return min_disc;
  }


  float
  METoverSumEt( const std::vector<pat::Jet> & jets, const pat::MET & met, const math::XYZTLorentzVector & lepton ){
  // Calculate MET divided by the sum of pts of Jets>50, MET and lepton

    double sumJetPt(0);
    for (unsigned ijet=0; ijet < jets.size(); ijet++){
      if (jets[ijet].pt()>50.){
        sumJetPt += jets[ijet].pt();
      }
    }
    double ret = met.et()/(met.et()+lepton.pt()+sumJetPt);
    return ret;
  } // end METoverSumEt


  double lepJetInvariantMass(std::vector<pat::Jet> & jets, reco::Particle lepton){
    double eleJetminDR = 999.;
    double eleJetMass = NAN;
    for(std::vector <pat::Jet>::const_iterator jet = jets.begin(); jet != jets.end(); ++jet){
      double dR = MathHelper::deltaR(lepton.p4(),jet->p4());
      if(dR < eleJetminDR){
        eleJetminDR = dR;
        eleJetMass = (jet->p4() + lepton.p4()).mass();
      }
    }
    return eleJetMass;
  }

  double deltaPhiOfBestTCHEJets (std::vector<pat::Jet> & jets){
    int mostblikeindex = -99;
    int jetIndex = 0;
    double maxTCHE = -99.;

    for(std::vector <pat::Jet>::const_iterator jet = jets.begin(); jet != jets.end(); ++jet){
      if(maxTCHE < jet->bDiscriminator("trackCountingHighEffBJetTags")){
        maxTCHE = jet->bDiscriminator("trackCountingHighEffBJetTags");
        mostblikeindex = jetIndex;
      }
      jetIndex++;
    }

    int mostblikeindex_2 = -99;
    int jetIndex_2 = 0;
    double maxTCHE_2 = -99.;

    for(std::vector <pat::Jet>::const_iterator jet = jets.begin(); jet != jets.end(); ++jet){
      if(jetIndex_2 == mostblikeindex) continue;
      if(maxTCHE_2 < jet->bDiscriminator("trackCountingHighEffBJetTags")){
        maxTCHE_2 = jet->bDiscriminator("trackCountingHighEffBJetTags");
        mostblikeindex_2 = jetIndex_2;
      }
      jetIndex_2++;
    }

    double bjet1bjet2dPhi;
    if(mostblikeindex != -99 && mostblikeindex_2 != -99) bjet1bjet2dPhi = kinem::delta_phi(jets.at(mostblikeindex).phi(),jets.at(mostblikeindex_2).phi());
    else bjet1bjet2dPhi = 3.;

    return bjet1bjet2dPhi;
  }


  float eleIsoCorrectionArea(const pat::Electron & ele, IsoCorrectionType type) {

    float AreaTracker[2] = {0., 0.}; //   barrel/endcap
    float AreaEcal[2]    = {0.101, 0.046}; //   barrel/endcap
    float AreaHcal[2]    = {0.021 , 0.040 }; //   barrel/endcap

    int ifid = -1;
    if (ele.isEB()) ifid =0;
    else if (ele.isEE()) ifid=1;
    if (ifid<0) return 0.;

    if (type == TRK) return AreaTracker[ifid];
    if (type == ECAL) return AreaEcal[ifid];
    if (type == HCAL) return AreaHcal[ifid];
    return 0.;
//    Double_t EleTkIso   = ele_tkSumPtEg4Hzz_dr03[iele]  - AreaTracker[ifid] * PU_rhoCorr;
//    Double_t EleEcalIso = ele_ecalRecHitSumEt_dr03[iele]- AreaEcal[ifid]  * PU_rhoCorr;
//    Double_t EleHcalIso = ele_hcalDepth1TowerSumEt_dr03[iele] + ele_hcalDepth2TowerSumEt_dr03[iele] - AreaHcal[ifid] * PU_rhoCorr;
//
//    Double_t EleCombIso = TkIso + EcalIso + HcalIso;
//    Double_t EleCombRelIso = CombIso / ele.pt();
  }
  float muIsoCorrectionArea(const pat::Muon & mu, IsoCorrectionType type) {
    float AreaTracker[2] = {0., 0.}; //   barrel/endcap
    float AreaEcal[2]    = {0.074, 0.045}; //   barrel/endcap
    float AreaHcal[2]    = {0.022 , 0.030 }; //   barrel/endcap
    Int_t ifid = (fabs(mu.eta()) < 1.479) ? 0 : 1;    //we distinguish beetwen EB and EE and HB and HE

    if (type == TRK) return AreaTracker[ifid];
    if (type == ECAL) return AreaEcal[ifid];
    if (type == HCAL) return AreaHcal[ifid];
    return 0.;
  }

} // close namespace RecoHelper

