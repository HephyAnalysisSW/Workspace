#include "RooFit.h"
#include "Riostream.h"
//#include "owens.h"
#include "RooSkewErf.h"
#include "TMath.h"
#ifndef __CINT__

#include <boost/math/special_functions/owens_t.hpp>
#endif

double owens_t(double arg, double a);

#ifndef __CINT__
double owens_t(double arg, double a) {
  return boost::math::owens_t<double>(arg, a);
}
#endif

using namespace std;

ClassImp(RooSkewErf)



//_____________________________________________________________________________
RooSkewErf::RooSkewErf(const char *name, const char *title, RooAbsReal& _x, RooAbsReal& _mean, RooAbsReal& _scale, RooAbsReal& _skew) :
	RooAbsReal(name,title),
	x("x","x",this,_x),
	mean("mean","mean",this,_mean),
	scale("scale","scale",this,_scale),
	skew("skew","skew",this,_skew)
{}



//_____________________________________________________________________________
RooSkewErf::RooSkewErf(const RooSkewErf& other, const char* name) :
	RooAbsReal(other, name),
	x("x",this,other.x),
	mean("mean",this,other.mean),
	scale("scale",this,other.scale),
	skew("skew",this,other.skew)
{
	// Copy constructor
}



//_____________________________________________________________________________
RooSkewErf::~RooSkewErf()
{
	// Destructor
}



Double_t RooSkewErf::cdf(int version) const
{
	Double_t ret(0.);
	Double_t arg( (x-mean)/scale );
	if (version==1) {
		ret = 0.5*(1.0 + TMath::Erf((arg)/TMath::Sqrt2())) - 2*owens_t(arg,skew);
	}
	if (version==2) {
		if (skew != 0.) {
			arg = -1./skew*TMath::Log(1-skew*arg);
		}
		if (skew>0) {
			if (x < mean+scale/skew) {
				return 0.5*(1.0 + TMath::Erf((arg)/TMath::Sqrt2()));
			} else {
				return 1.;
			}
		}
		if (skew<0) {
			if (x > mean+scale/skew) {
				return 0.5*(1.0 + TMath::Erf((arg)/TMath::Sqrt2()));
			} else {
				return 0.;
			}
		}
		if (skew==0) return 0.5*(1.0 + TMath::Erf((arg)/TMath::Sqrt2()));
	}
	return ret;
}



//_____________________________________________________________________________
Double_t RooSkewErf::evaluate() const
{
	double ret(cdf(1));
	ret = ret>0?ret:0;
	ret = ret<1?ret:1;
	return ret;
}


