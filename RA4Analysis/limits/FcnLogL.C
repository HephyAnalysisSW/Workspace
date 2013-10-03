#ifndef MN_FcnLogL_H_
#define MN_FcnLogL_H_
#include "Minuit2/FCNBase.h"
#include "Triplet.h"
#include "TMath.h"

#if !defined(__CINT__) && !defined(__MAKECINT__)

#include <vector>
#include <iostream>
#endif

class FcnLogL : public ROOT::Minuit2::FCNBase {
public:
//   FcnLogL() {}
  FcnLogL(const std::vector<BinContentTriplet>& triplets, int nTot) : theTriplets(triplets), nTot_(nTot), theErrorDef(0.5) {}
  // ~FcnLogL() {delete thePVLogL;}
  double Up() const {return theErrorDef;}
  double operator()(const std::vector<double>&) const;
private:
  double logBinomial (double x, double par) const;
  double logL (const BinContentTriplet& triplet, const std::vector<double>& pars) const;
private:
  std::vector<BinContentTriplet> theTriplets;
  int nTot_;
  double theErrorDef;
};
#endif //MN_FcnLogL_H_

double 
FcnLogL::logBinomial (double x, double par) const
{
  if ( par<=0. || par>=1. )  return -1.e30;
  int k = int(x*nTot_+0.5);
  if ( k<0 )  k = 0;
  if ( k>nTot_ )  k = nTot_;

  double result(0.);

//   double fact(0.);
//   if ( k>0 && k<nTot_ ) {
//     int k1 = min(k,nTot_-k);
//     int k2 = nTot_ - k1;
//     fact = log(k2+1.);
//     for (int i=k1; i>1; --i )  fact += log((k2+i)/double(i));
//     result += fact;
//   }
//   std::cout << "k, par = " << k << " " << nTot_ << " " << par <<std::endl;
//   std::cout << fact << " " << k*log(par) << " " << (nTot_-k)*log(1.-par) << std::endl;
//   return -(fact+k*log(par)+(nTot_-k)*log(1.-par));
  return -(k*log(par)+(nTot_-k)*log(1.-par));
}

double
FcnLogL::logL (const BinContentTriplet& triplet, const std::vector<double>& pars) const
{
  double x = triplet.x();
  double y = triplet.y();
  double z = triplet.z();
  double lambda(0);
  //
  // linear interpolation
  //
  lambda = pars[0] + x*pars[1] + y*pars[2];
  if ( pars.size() == 6 ) {
    lambda += x*x*pars[3] + x*y*pars[4] + y*y*pars[5];
  }
//   if ( lambda < 0 )  lambda = 0.;
  lambda = exp(lambda);
  double result = logBinomial(z,lambda);
//   std::cout << "z = " << z << " lambda for " << x << " " << y << " = " << lambda 
//          << " / " << result << std::endl;
  return result;
}

double
FcnLogL::operator() (const std::vector<double>& pars) const
{
  assert(pars.size()==3||pars.size()==6);
  double sumL(0.);
  for ( size_t i=0; i<theTriplets.size(); ++i ) {
    sumL += logL(theTriplets[i],pars);
  }
//   std::cout << "sumL = " << sumL << std::endl;
  return sumL;
}

