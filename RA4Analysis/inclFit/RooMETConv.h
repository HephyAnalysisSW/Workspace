#ifndef ROO_METCONV
#define ROO_METCONV

#include "RooAbsPdf.h"
#include "RooArgSet.h"
#include "RooRealProxy.h"
#include "RooRealVar.h"
#include "RooDataHist.h"
#include "RooHistPdf.h"
#include "RooProdPdf.h"
#include "RooAddPdf.h"
#include "RooPareto.h"

#include "TH1D.h"
#include <vector>

class RooRealVar;
class RooAbsReal;

template <typename T>
class RooMETConv : public RooAbsPdf {
public:
  RooMETConv() {} ;
  RooMETConv(const char *name, const char *title,
		  RooAbsReal& _met, RooAbsReal& _res, RooAbsReal& _phi, T& _metPdf, RooAbsPdf& _resPdf, RooAbsPdf& _phiPdf, double _metShift, double _resBinsWidth, double _lowMETCont);

  RooMETConv(const RooMETConv& other,const char* name=0) ;

  virtual TObject* clone(const char* newname) const { return new RooMETConv(*this,newname);	}
  virtual ~RooMETConv();
  virtual TH1D* getHistSum() {return (TH1D*)h_sum->Clone("convolutionHist");}

protected:
  RooRealProxy met;
  RooRealProxy res;
  RooRealProxy phi;
  RooRealProxy metPdf;
  RooRealProxy resPdf;
  RooRealProxy phiPdf;

  double lowMETCont;
  double norm_min;
  double norm_max;
  double bcLowMET;
  RooAbsReal* lowMETNorm;
  RooArgSet* current_params;
  mutable RooRealVar* current_arg_met;
  unsigned int neval_prod;

  TH1D* h_sum;
  vector<double> prod_met;
  vector<double> prod_sum;
  vector<double> prod_vol_const;

  Double_t evaluate() const;
  bool changedParams() const;
  void updateConv() const;
  void saveParams() const;
  RooArgSet* floatingParams(RooArgSet* pars = 0) const;
  void setConst(RooArgSet* pars = 0) const;
  void setParams(RooArgSet* pars = 0) const;
  Double_t expInterpolate(Double_t x, Double_t *par) const;

private:
  ClassDef(RooMETConv,1)
};

typedef RooMETConv<RooPareto> RooParetoConv;
typedef RooMETConv<RooAddPdf> RooAddConv;

#endif


#ifdef __CINT__
//#pragma link C++ class RooMETConv<RooPareto>+;
#pragma link C++ class RooParetoConv+;
#pragma link C++ class RooAddConv+;
#endif

