#include "TFile.h"
#include "Math/Boost.h"


typedef ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<float> > LorentzVector;
float ttbarPolarizationAngle(LorentzVector p4top,LorentzVector p4w, LorentzVector p4lepton){

  LorentzVector genp4_tplus_;
  LorentzVector genp4_Wplus_;
  LorentzVector genp4_lplus_;
  LorentzVector genp4_Wplus_tCM_;
  LorentzVector genp4_lplus_WCM_;
  LorentzVector genp4_lplus_tCM_;


  genp4_tplus_=p4top;
  genp4_Wplus_=p4w;    
  genp4_lplus_=p4lepton;    
  

  
  // Boost from the LAB to the top CM
  ROOT::Math::Boost boost_tplus_CM( genp4_tplus_.BoostToCM().x(), genp4_tplus_.BoostToCM().y(), genp4_tplus_.BoostToCM().z() );

  // Boost from the LAB to the W CM
  ROOT::Math::Boost boost_Wplus_CM( genp4_Wplus_.BoostToCM().x(), genp4_Wplus_.BoostToCM().y(), genp4_Wplus_.BoostToCM().z() );
  
  // Get the W, lepton, and neutrino 4-vectors in the top rest frame
  genp4_Wplus_tCM_        = boost_tplus_CM  * genp4_Wplus_;
  genp4_lplus_tCM_        = boost_tplus_CM  * genp4_lplus_;

  // Boost from the top CM to the W CM ( tW notation )
  ROOT::Math::Boost boost_Wplus_tWCM( genp4_Wplus_tCM_.BoostToCM().x(), genp4_Wplus_tCM_.BoostToCM().y(), genp4_Wplus_tCM_.BoostToCM().z() );
  
  // Boost from the W CM to the top CM ( Wt notation )
  ROOT::Math::Boost boost_Wplus_WtCM  = boost_Wplus_tWCM.Inverse();
  
  // Get the lepton and neutrino 4-vectors in the W rest frame
  
  //--- LAB -> top CM -> W CM ---//
    genp4_lplus_WCM_        = boost_Wplus_tWCM  * genp4_lplus_tCM_;

  
  float theta_lplus_nu_WCM_ = -999.;
  // cos(theta) - should rename variables
  // theta is the angle between the lepton in the W rest frame and the W in the top rest frame
    theta_lplus_nu_WCM_     = genp4_lplus_WCM_.Px()*genp4_Wplus_tCM_.Px() +
      genp4_lplus_WCM_.Py()*genp4_Wplus_tCM_.Py() +
      genp4_lplus_WCM_.Pz()*genp4_Wplus_tCM_.Pz();
    
    theta_lplus_nu_WCM_     /= genp4_lplus_WCM_.P()*genp4_Wplus_tCM_.P();

  return theta_lplus_nu_WCM_;
}



float GetWeight(float x,float var ){

  float original_value = 0.693*(1-x*x)+0.5*0.307*(1-x)*(1-x);

  //  float new_value = 0.65853*(1-x*x)+0.5*0.34165*(1-x)*(1-x);
  //  cout<<"New_value"<<new_value<<endl;  
 float new_value = (0.693+var*0.01*0.693)*(1-x*x)+0.5*(0.307-var*0.01*0.693)*(1-x)*(1-x);
 //  cout<<"New_value1"<<new_value1<<endl;  
  float w = 1;
  if(original_value!=0){
    w = new_value/original_value; }
  else{cout<< "ERROR"<< endl; exit(1);}
  return w;

}



float weightTTbarPolarization(LorentzVector p4top,LorentzVector p4w, LorentzVector p4lepton,float PercentVariation){

  float final_weight=1;

  float cos_theta = ttbarPolarizationAngle(p4top,p4w,p4lepton);
  final_weight  = GetWeight( cos_theta,PercentVariation );
  
  return final_weight;
  
  
}//end of function

//lazy accessor for python
float weightTTbarPolarization(float tx, float ty, float tz, float tE, float Wx, float Wy, float Wz, float WE, float lx, float ly, float lz, float lE, float PercentVariation) {
  LorentzVector t, W, l;
  l.SetPxPyPzE(lx, ly, lz, lE);
  W.SetPxPyPzE(Wx, Wy, Wz, WE);
  t.SetPxPyPzE(tx, ty, tz, tE);
  return weightTTbarPolarization(t, W, l, PercentVariation);
}
