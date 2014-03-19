#include "TFile.h"
#include "TH1F.h"
#include "TLorentzVector.h"
#include "Math/Boost.h"


typedef ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<float> > LorentzVector;

float WjetPolarizationAngle(LorentzVector p4w, LorentzVector p4lepton){

  LorentzVector genp4_Wplus_;
  LorentzVector genp4_lplus_;
  LorentzVector genp4_Wplus_WCM_;
  LorentzVector genp4_lplus_WCM_;

  genp4_Wplus_=p4w;    
  genp4_lplus_=p4lepton;    

  ROOT::Math::Boost boost_Wplus_CM( genp4_Wplus_.BoostToCM().x(), genp4_Wplus_.BoostToCM().y(), genp4_Wplus_.BoostToCM().z() );
//  cout<<" boost_Wplus_CM "<<boost_Wplus_CM<<endl;
  // Get the W, lepton, and neutrino 4-vectors in the top rest frame
  genp4_Wplus_WCM_        = boost_Wplus_CM  * genp4_Wplus_;
  genp4_lplus_WCM_        = boost_Wplus_CM  * genp4_lplus_;
   
  float theta_lplus_nu_WCM_ = -999.;
  // cos(theta) - should rename variables
  // theta is the angle between the lepton in the W rest frame and the W in the lab frame
    theta_lplus_nu_WCM_     = genp4_lplus_WCM_.Px()*genp4_Wplus_.Px() +
      genp4_lplus_WCM_.Py()*genp4_Wplus_.Py() +
      genp4_lplus_WCM_.Pz()*genp4_Wplus_.Pz();
    
    theta_lplus_nu_WCM_     /= genp4_lplus_WCM_.P()*genp4_Wplus_.P();

//  cout<<"theta_lplus_nu_WCM_: "<<theta_lplus_nu_WCM_<<endl;

  return theta_lplus_nu_WCM_;
}



float GetWeightFLminusFR(float x,float var,LorentzVector p4W, bool Wplus ){
  // variable x is cos(theta) here

  //  TFile *_file0 = TFile::Open("Wpolarization_es_taus_too.root");
  //  TFile *_file0 = TFile::Open("new_file_HT300.root");
  TFile _file0("/data/schoef/tools/polSys/new_file_HT300.root");
//  if (!_file0) {
//    cout<<"Polarization data not found"<<endl;
//    return -999.;
//  }
  //  TH1F* h_polarization_Wplus[4][3];
  //  TH1F* h_polarization_Wminus[4][3];
  
  float pt_bins[5] = {50,100,300,500,10000};
  float eta_bins[4] = {0,1,2,5};

  //  TString bin_names_pt[4] = {"pt_50_100_","pt_100_300_","pt_300_500_","pt_500_up_"};
  //  TString bin_names_eta[3] = {"eta_0_1","eta_1_2","eta_2_5"};

  float fl_plus = 0;
  float fr_plus = 0;
  float f0_plus = 0;
  
  float fl_minus = 0;  
  float fr_minus = 0; 
  float f0_minus = 0;
  
  
  for(int i=0;i<4;i++){
    for(int ii=0;ii<3;ii++){
      if(p4W.Pt()>pt_bins[i]&&p4W.Pt()<pt_bins[i+1]&&fabs(p4W.Rapidity())>eta_bins[ii]&&fabs(p4W.Rapidity())<eta_bins[ii+1]){

	if(i==3&&ii==2){
	  //in highest rapidity and highest ptW bin do nothing because the statistics is lousy
	}
	else{
	  
	  if(Wplus){
	    TH1F* h_polarization_Wplus_fl;
	    TH1F* h_polarization_Wplus_fr;
	    TH1F* h_polarization_Wplus_f0;
	    h_polarization_Wplus_fl = (TH1F*)_file0.Get("h_W_plus_fl");
	    h_polarization_Wplus_fr = (TH1F*)_file0.Get("h_W_plus_fr");
	    h_polarization_Wplus_f0 = (TH1F*)_file0.Get("h_W_plus_f0");
	    fl_plus = h_polarization_Wplus_fl->GetBinContent(i,ii);
	    fr_plus = h_polarization_Wplus_fr->GetBinContent(i,ii);
	    //	    f0_plus = h_polarization_Wplus_f0->GetBinContent(i,ii);
	    f0_plus = 1-fl_plus-fr_plus;
	  }//end of Wplus
	  if(!Wplus){
	    TH1F* h_polarization_Wminus_fl;
	    TH1F* h_polarization_Wminus_fr;
	    TH1F* h_polarization_Wminus_f0;
	    h_polarization_Wminus_fl = (TH1F*)_file0.Get("h_W_minus_fl");
	    h_polarization_Wminus_fr = (TH1F*)_file0.Get("h_W_minus_fr");
	    h_polarization_Wminus_f0 = (TH1F*)_file0.Get("h_W_minus_f0");
	    fl_minus = h_polarization_Wminus_fl->GetBinContent(i,ii);
	    fr_minus = h_polarization_Wminus_fr->GetBinContent(i,ii);
	    //	    f0_minus = h_polarization_Wminus_f0->GetBinContent(i,ii);
	    f0_minus = 1-fl_minus-fr_minus;
	  }//end of Wminus
	}//end of requiring that last bin in helicity not be used 
      }//end of if statement for W pt and helicity
    }}//end of for loop




  float f0=0;
  float fl=0;
  float fr=0;
  float fl_variation = 0;
  float fr_variation = 0;
  float original_value = 0;
  float new_value = 0;
  if(Wplus){f0=f0_plus;fl=fl_plus;fr=fr_plus;    
    fl_variation = fl+(fl-fr)*var*0.01;
    fr_variation = fr-(fl-fr)*var*0.01;
    if(fl_variation>1||fr_variation<0){fl_variation=1-f0;fr_variation=0;}
    /*
    cout<<"W plus event"<<endl;
    cout<<"W pt: "<<p4W.Pt()<<endl;
    cout<<"W y:  "<<fabs(p4W.Rapidity())<<endl;
    cout<<"fl original: "<<fl<<", fl vary: "<<fl_variation<<endl;
    cout<<"fr original: "<<fr<<", fr vary: "<<fr_variation<<endl;
    cout<<"fo original: "<<f0<<endl;
    */
    original_value = f0*(1-x*x)+0.5*fl*(1-x)*(1-x)+0.5*fr*(1+x)*(1+x);
    new_value = f0*(1-x*x)+0.5*fl_variation*(1-x)*(1-x)+0.5*fr_variation*(1+x)*(1+x);
  }
  if(!Wplus){f0=f0_minus;fl=fl_minus;fr=fr_minus;
    fl_variation = fl+(fl-fr)*var*0.01;
    fr_variation = fr-(fl-fr)*var*0.01;    
    if(fl_variation>1||fr_variation<0){fl_variation=1-f0;fr_variation=0;}
    /*
    cout<<"W minus event"<<endl;
    cout<<"W pt: "<<p4W.Pt()<<endl;
    cout<<"W y:  "<<fabs(p4W.Rapidity())<<endl;
    cout<<"fl original: "<<fl<<", fl vary: "<<fl_variation<<endl;
    cout<<"fr original: "<<fr<<", fr vary: "<<fr_variation<<endl;
    cout<<"fo original: "<<f0<<endl;
    */
    original_value = f0*(1-x*x)+0.5*fr*(1-x)*(1-x)+0.5*fl*(1+x)*(1+x);
    new_value = f0*(1-x*x)+0.5*fr_variation*(1-x)*(1-x)+0.5*fl_variation*(1+x)*(1+x);
  }

  float w = 1;

  //  cout<<"original_value: "<<original_value<<endl;
  //  cout<<"new_value: "<<new_value<<endl;

  if((f0+fl+fr)!=0){
    if(original_value!=0){
      w = new_value/original_value; }
    else{cout<< "ERROR"<< endl; exit(1);}
  }

  _file0.Close();
  //  cout<<"Weight is: "<<w<<endl;
  return w;

}


float GetWeightF0(float x,float var,LorentzVector p4W, bool Wplus ){
  // variable x is cos(theta) here

  //  TFile *_file0 = TFile::Open("Wpolarization_es_taus_too.root");
//  TFile _file0("new_file_HT300.root");
  TFile _file0("/data/schoef/tools/polSys/new_file_HT300.root");
//  if (!_file0) {
//    cout<<"Polarization data not found"<<endl;
//    return -999.;
//  }

  //  TH1F* h_polarization_Wplus[4][3];
  //  TH1F* h_polarization_Wminus[4][3];
  
  float pt_bins[5] = {50,100,300,500,10000};
  float eta_bins[4] = {0,1,2,5};

  //  TString bin_names_pt[4] = {"pt_50_100_","pt_100_300_","pt_300_500_","pt_500_up_"};
  //  TString bin_names_eta[3] = {"eta_0_1","eta_1_2","eta_2_5"};



  float fl_plus = 0;
  float fr_plus = 0;
  float f0_plus = 0;
  
  float fl_minus = 0;  
  float fr_minus = 0; 
  float f0_minus = 0;
  
  
  for(int i=0;i<4;i++){
    for(int ii=0;ii<3;ii++){
      if(p4W.Pt()>pt_bins[i]&&p4W.Pt()<pt_bins[i+1]&&fabs(p4W.Rapidity())>eta_bins[ii]&&fabs(p4W.Rapidity())<eta_bins[ii+1]){

	if(i==3&&ii==2){
	  //in highest rapidity and highest ptW bin do nothing because the statistics is lousy
	}
	else{

	  if(Wplus){
	    TH1F* h_polarization_Wplus_fl;
	    TH1F* h_polarization_Wplus_fr;
	    TH1F* h_polarization_Wplus_f0;
	    h_polarization_Wplus_fl = (TH1F*)_file0.Get("h_W_plus_fl");
	    h_polarization_Wplus_fr = (TH1F*)_file0.Get("h_W_plus_fr");
	    h_polarization_Wplus_f0 = (TH1F*)_file0.Get("h_W_plus_f0");
	    fl_plus = h_polarization_Wplus_fl->GetBinContent(i,ii);
	    fr_plus = h_polarization_Wplus_fr->GetBinContent(i,ii);
	    //	    f0_plus = h_polarization_Wplus_f0->GetBinContent(i,ii);
	    f0_plus = 1-fl_plus-fr_plus;
	  }//end of Wplus
	  if(!Wplus){
	    TH1F* h_polarization_Wminus_fl;
	    TH1F* h_polarization_Wminus_fr;
	    TH1F* h_polarization_Wminus_f0;
	    h_polarization_Wminus_fl = (TH1F*)_file0.Get("h_W_minus_fl");
	    h_polarization_Wminus_fr = (TH1F*)_file0.Get("h_W_minus_fr");
	    h_polarization_Wminus_f0 = (TH1F*)_file0.Get("h_W_minus_f0");
	    fl_minus = h_polarization_Wminus_fl->GetBinContent(i,ii);
	    fr_minus = h_polarization_Wminus_fr->GetBinContent(i,ii);
	    f0_plus = 1-fl_plus-fr_plus;
	    //	    f0_minus = h_polarization_Wminus_f0->GetBinContent(i,ii);
	  }//end of Wminus
	}//end of requiring that last bin in helicity not be used 
      }//end of if statement for W pt and helicity
    }}//end of for loop




  float f0=0;
  float fl=0;
  float fr=0;
  float f0_variation = 0;
  float fl_variation = 0;
  float fr_variation = 0;
  float original_value = 0;
  float new_value = 0;
  if(Wplus){f0=f0_plus;fl=fl_plus;fr=fr_plus;
    f0_variation = f0+f0*var*0.01;
    fl_variation = fl-0.5*f0*var*0.01;
    fr_variation = fr-0.5*f0*var*0.01;    
    /*
    cout<<"W plus event"<<endl;
    cout<<"W pt: "<<p4W.Pt()<<endl;
    cout<<"W y:  "<<fabs(p4W.Rapidity())<<endl;
    cout<<"fl original: "<<fl<<", fl vary: "<<fl_variation<<endl;
    cout<<"fr original: "<<fr<<", fr vary: "<<fr_variation<<endl;
    cout<<"f0 original: "<<f0<<", f0 vary: "<<f0_variation<<endl;
    */
    original_value = f0*(1-x*x)+0.5*fl*(1-x)*(1-x)+0.5*fr*(1+x)*(1+x);
    new_value = f0_variation*(1-x*x)+0.5*fl_variation*(1-x)*(1-x)+0.5*fr_variation*(1+x)*(1+x);
  }
  if(!Wplus){f0=f0_minus;fl=fl_minus;fr=fr_minus;
    f0_variation = f0+f0*var*0.01;
    fl_variation = fl-0.5*f0*var*0.01;
    fr_variation = fr-0.5*f0*var*0.01;    
    /*
    cout<<"W minus event"<<endl;
    cout<<"W pt: "<<p4W.Pt()<<endl;
    cout<<"W y:  "<<fabs(p4W.Rapidity())<<endl;
    cout<<"fl original: "<<fl<<", fl vary: "<<fl_variation<<endl;
    cout<<"fr original: "<<fr<<", fr vary: "<<fr_variation<<endl;
    cout<<"f0 original: "<<f0<<", f0 vary: "<<f0_variation<<endl;
    */
    original_value = f0*(1-x*x)+0.5*fr*(1-x)*(1-x)+0.5*fl*(1+x)*(1+x);
    new_value = f0_variation*(1-x*x)+0.5*fr_variation*(1-x)*(1-x)+0.5*fl_variation*(1+x)*(1+x);
  }

  float w = 1;

  if((f0+fl+fr)!=0){
    if(original_value!=0){
      w = new_value/original_value; }
    else{cout<< "ERROR"<< endl; exit(1);}
  }

  _file0.Close();

  return w;

}


//float weightTTbarPolarization(LorentzVector p4w, LorentzVector p4lepton,float PercentVariation){
float GetWeightWjetsPolarizationFLminusFR(TLorentzVector _p4W, TLorentzVector _p4lepton,float PercentVariation, bool isWplus){

  LorentzVector p4W, p4lepton;
  p4W.SetPx(_p4W.Px());
  p4W.SetPy(_p4W.Py());
  p4W.SetPz(_p4W.Pz());
  p4W.SetE(_p4W.E());
  p4lepton.SetPx(_p4lepton.Px());
  p4lepton.SetPy(_p4lepton.Py());
  p4lepton.SetPz(_p4lepton.Pz());
  p4lepton.SetE(_p4lepton.E());
//  cout<<" MW: "<< p4W.M()<<" "<<p4lepton.M()<<endl;
  float final_weight=1;

  float cos_theta = WjetPolarizationAngle(p4W,p4lepton);
  //  final_weight  = GetWeight( cos_theta,PercentVariation );
  final_weight  = GetWeightFLminusFR( cos_theta,PercentVariation,p4W, isWplus );
  //  final_weight  = GetWeightF0( cos_theta,PercentVariation,p4W );
  
  return final_weight;
  
  
}//end of function

float GetWeightWjetsPolarizationF0(TLorentzVector _p4W, TLorentzVector _p4lepton,float PercentVariation, bool isWplus){

  LorentzVector p4W, p4lepton;
  p4W.SetPx(_p4W.Px());
  p4W.SetPy(_p4W.Py());
  p4W.SetPz(_p4W.Pz());
  p4W.SetE(_p4W.E());
  p4lepton.SetPx(_p4lepton.Px());
  p4lepton.SetPy(_p4lepton.Py());
  p4lepton.SetPz(_p4lepton.Pz());
  p4lepton.SetE(_p4lepton.E());

  float final_weight=1;

  float cos_theta = WjetPolarizationAngle(p4W,p4lepton);
  //  final_weight  = GetWeight( cos_theta,PercentVariation );
  //final_weight  = GetWeightFLminusFR( cos_theta,PercentVariation,p4W, isWplus );
  final_weight  = GetWeightF0( cos_theta,PercentVariation,p4W,isWplus );
  
  return final_weight;
  
  
}//end of function
