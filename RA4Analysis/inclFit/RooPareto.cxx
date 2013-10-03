#include "RooFit.h"
#include "Riostream.h"

#include "RooPareto.h"
#include "RooRandom.h"
#include "TMath.h"
using namespace std;

ClassImp(RooPareto)



//_____________________________________________________________________________
RooPareto::RooPareto(const char *name, const char *title, RooAbsReal& _x, RooAbsReal& _location, RooAbsReal& _scale, RooAbsReal& _shape, const RooArgList& _efflist) :
	RooAbsPdf(name,title),
	x("x","x",this,_x),
	location("location","location",this,_location),
	scale("scale","scale",this,_scale),
	shape("shape","shape",this,_shape),
	efflist("efflist","List of Efficiencies",this)
{
	// constructor
	if (_efflist.getSize()<=2) {
		TIterator* iter = _efflist.createIterator();
		RooAbsArg* arg ;
		while((arg=(RooAbsArg*)iter->Next())) {
			RooAbsReal* eff = dynamic_cast<RooAbsReal*>(arg) ;
			if (!eff) {
				cout << "Error in RooPareto constructor: efficiency " << arg->GetName() << " does not derive from RooAbsReal and will be ignored" << endl ;
				continue ;
			}
			efflist.add(*eff) ;
		}
	} else {
		cout << "Error in RooPareto constructor: more than 2 efficiency functions" << endl;
	}
}



//_____________________________________________________________________________
RooPareto::RooPareto(const RooPareto& other, const char* name) :
	RooAbsPdf(other, name),
	x("x",this,other.x),
	location("location",this,other.location),
	scale("scale",this,other.scale),
	shape("shape",this,other.shape),
	efflist("efflist",this,other.efflist)
{
	// copy constructor
}



//_____________________________________________________________________________
Double_t RooPareto::evaluate() const
{
	double ret = 0.;
	double z = (x-location)/scale;
	if (x>=location) {
		if ((shape>0) or ((shape<0) and (x<=(location-scale/shape)))) ret = TMath::Power(1+shape*z,-1-1/shape)/scale;
		if (shape==0) ret = TMath::Exp(-z)/scale;
	}
	double eff(1);
	for (int i = 0; i < efflist.getSize(); i++) {
		eff *= ((RooAbsReal*)(efflist.at(i)))->getVal();
	}
	return eff*ret;
}

//_____________________________________________________________________________
Int_t RooPareto::getAnalyticalIntegral(RooArgSet& allVars, RooArgSet& analVars, const char* /*rangeName*/) const
{
  if (efflist.getSize()==0) {
	  if (matchArgs(allVars,analVars,x)) return 1;
  }
  return 0;
}



//_____________________________________________________________________________
Double_t RooPareto::analyticalIntegral(Int_t code, const char* rangeName) const
{
	assert(code==1);
	double ret = 1.;
	if(code==1){
		Double_t xmin = x.min(rangeName);
		Double_t xmax = x.max(rangeName);
		if (xmin<xmax) {
			if (xmin<location) xmin=location;
			if (xmax<location) xmax=location;
			double zmin = (xmin-location)/scale;
			double zmax = (xmax-location)/scale;
			double retmin = 0.;
			double retmax = 0.;
			if (shape>0) {
				retmin = 1-TMath::Power(1+shape*zmin,-1/shape);
				retmax = 1-TMath::Power(1+shape*zmax,-1/shape);
			}
			if (shape<0) {
				if (xmin<=(location-scale/shape)) {
					retmin = 1-TMath::Power(1+shape*zmin,-1/shape);
				}
				else retmin = 1.;
				if (xmax<=(location-scale/shape)) {
					retmax = 1-TMath::Power(1+shape*zmax,-1/shape);
				}
				else retmax = 1.;
			}
			if (shape==0) {
				retmin = TMath::Exp(-zmin);
				retmax = TMath::Exp(-zmax);
			}
			ret = retmax-retmin;
		}
	} else {
		cout << "Error in RooPareto::analyticalIntegral" << endl;
	}
	return ret;
}
