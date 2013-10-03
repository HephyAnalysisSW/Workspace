#ifndef ROO_PARETO
#define ROO_PARETO

#include "RooAbsPdf.h"
#include "RooRealProxy.h"
#include "RooArgList.h"
#include "RooListProxy.h"
#include <vector>

class RooRealVar;
class RooPareto : public RooAbsPdf {
public:
  // Constructors, assignment etc
  RooPareto() {};
  RooPareto(const char *name, const char *title, RooAbsReal& _x, RooAbsReal& _location, RooAbsReal& _scale, RooAbsReal& _shape, const RooArgList& _efflist=RooArgList() );
  RooPareto(const RooPareto& other, const char* name=0);
  virtual TObject* clone(const char* newname) const { return new RooPareto(*this, newname); }
  inline virtual ~RooPareto() {}

  Int_t getAnalyticalIntegral(RooArgSet& allVars, RooArgSet& analVars, const char* rangeName=0) const;
  Double_t analyticalIntegral(Int_t code, const char* rangeName=0) const;

protected:

  // Function evaluation
  virtual Double_t evaluate() const ;
  RooRealProxy x;
  RooRealProxy location;
  RooRealProxy scale;
  RooRealProxy shape;
  RooListProxy efflist;

  ClassDef(RooPareto,1)
};

#endif


