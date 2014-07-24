#ifndef BTAGWEIGHT_H
#define BTAGWEIGHT_H

//#include <math.h>
#include <iostream>
//#include <vector>
////#include "SFlightFuncs.h"
//#include "SFlightFuncs_Moriond2013.C"
//#include "TF1.h"
//#include <map>
#include <string>

double getFastSimCorr(std::string flavor, double pt, std::string SFvary, double eta=0)
{

  double highPtErrFac = 1;
  if(pt>=670){
    pt=670;
    highPtErrFac = 2;
  }
  if(pt<40) {
//    std::cout<<"Error, pt too low"<<std::endl;
//    exit(1);
    pt=40; //Dirty fix for DegStop SMS
  }

  double ptBins[14] = {40, 50, 60, 70, 80, 100, 120, 160, 210, 260, 320, 400, 500, 670};
  double CFb[13] = {0.980998,0.992014,0.994472,0.996825,0.999822,1.00105,1.00023,0.991994,0.979123,0.947207,0.928006,0.874260,0.839610};
  double CFb_err[13] = {0.00296453,0.00113963,0.00128363,0.00232566,0.00232353,0.00219086,0.00156856,0.00322279,0.00400414,0.00737465,0.0105033,0.0171706,0.0344172};
  double CFb_T1tttt_syst[13] = {0.0127103,0.0107696,0.0105987,0.0102283,0.00953639,0.0107003,0.0118546,0.00837368,0.000790179,-0.00111371,-0.0146178,-0.00818416,-0.0197257};
  double CFc[13] = {0.981714,1.00946,1.01591,1.02810,1.02195,1.02590,1.01936,0.991228,0.955343,0.944433,0.917282,0.935018,1.06375};
  double CFc_err[13] = {0.00661831,0.00968682,0.00751322,0.00675507,0.00562821,0.00862890,0.00768003,0.0188981,0.0261163,0.0450601,0.0448453,0.148805,0.177157};
  double CFc_T1tttt_syst[13] = {0.00246567,0.00672805,0.00625175,0.0121922,0.0183616,0.0224260,0.0350031,0.0361672,0.0372230,0.0116431,0.0207569,0.0382855,0.0252644};
  double CFl_central[13] = {1.28615,1.37535,1.38966,1.40320,1.49835,1.44308,1.58198,1.55687,1.65790,1.90233,1.92259,2.66174,3.08688};
  double CFl_central_err[13] = {0.0373732,0.0461870,0.0288973,0.0333528,0.0513836,0.0420353,0.106627,0.0658359,0.117285,0.185533,0.214071,0.487274,0.871502};
  double CFl_central_T1tttt_syst[13] = {0.162964,0.223318,0.220063,0.222306,0.267305,0.222287,0.283804,0.252221,0.324747,0.527015,0.659528,1.19317,1.50547};
  double CFl_forward[13] = {1.48732,1.69024,1.64494,1.79297,1.90760,1.99867,2.21659,2.20103,2.42645,2.67594,4.24735,3.98979,15.0457};
  double CFl_forward_err[13] = {0.0392025,0.106315,0.115751,0.106807,0.0642086,0.138742,0.182345,0.169922,0.297889,0.320088,0.927736,1.24666,15.1860};
  double CFl_forward_T1tttt_syst[13] = {0.874528,1.19814,1.24806,1.49608,1.73841,2.00430,2.54257,3.27898,4.35726,5.31846,7.44186,9.19039,15.6896};

  int ipt;
  for(ipt=12; ipt>=0; ipt--) {
    if(pt>=ptBins[ipt]) {
      break;
    }
  }

  double mean_corr=0;

  if(flavor=="b") mean_corr = CFb[ipt];
  if(flavor=="c") mean_corr = CFb[ipt];
  if(flavor=="other" && fabs(eta)<=1.2) mean_corr = CFl_central[ipt];
  if(flavor=="other" && fabs(eta)>1.2) mean_corr = CFl_forward[ipt];

  if(SFvary=="mean") return mean_corr;

  double temp_error;
  if(flavor=="b") temp_error = sqrt(pow(CFb_err[ipt],2)+pow(CFb_T1tttt_syst[ipt],2));
  if(flavor=="c") temp_error = sqrt(pow(CFc_err[ipt],2)+pow(CFc_T1tttt_syst[ipt],2));
  if(flavor=="other" && fabs(eta)<=1.2) temp_error = sqrt(pow(CFl_central_err[ipt],2)+pow(CFl_central_T1tttt_syst[ipt],2));
  if(flavor=="other" && fabs(eta)>1.2) temp_error = sqrt(pow(CFl_forward_err[ipt],2)+pow(CFl_forward_T1tttt_syst[ipt],2));

  if(SFvary=="down" || SFvary=="min") return mean_corr-temp_error*highPtErrFac;
  else if(SFvary=="up" || SFvary=="max") return mean_corr+temp_error*highPtErrFac;
  else return 0;

}

#endif //BTAGWEIGHT_H
