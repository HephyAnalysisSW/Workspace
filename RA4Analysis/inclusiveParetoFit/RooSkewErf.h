#ifndef ROO_SKEWERF
#define ROO_SKEWERF

#include "RooRealProxy.h"

class RooArgSet ;

class RooSkewErf : public RooAbsReal {
public:
  // Constructors, assignment etc
  inline RooSkewErf() { }
  RooSkewErf(const char *name, const char *title, RooAbsReal& _x, RooAbsReal& _mean, RooAbsReal& _scale, RooAbsReal& _skew);
  RooSkewErf(const RooSkewErf& other, const char* name=0);
  virtual TObject* clone(const char* newname) const { return new RooSkewErf(*this,newname); }
  virtual ~RooSkewErf();

protected:

  // Function evaluation
  virtual Double_t evaluate() const;
  virtual Double_t cdf(int version) const;
  RooRealProxy x;
  RooRealProxy mean;
  RooRealProxy scale;
  RooRealProxy skew;


  ClassDef(RooSkewErf,1) // Real-valued function of other RooAbsArgs calculated by a TFormula expression
};

#endif


