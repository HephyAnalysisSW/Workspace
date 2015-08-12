#ifndef ROO_BINNEDPDF
#define ROO_BINNEDPDF

#include "RooAbsPdf.h"
#include "RooRealProxy.h"
#include "RooListProxy.h"
#include "RooBinning.h"

class RooRealVar;
class RooBinnedPDF : public RooAbsPdf {
public:
//  typedef std::pair<double,double> bin;
//  typedef std::vector<bin> bins;
  // Constructors, assignment etc
  RooBinnedPDF() {};
  RooBinnedPDF(const char *name, const char *title, RooAbsReal& _x, RooArgList & args,  RooBinning & binning);
  RooBinnedPDF(const RooBinnedPDF& other, const char* name=0);
  virtual TObject* clone(const char* newname) const { return new RooBinnedPDF(*this, newname); }
  inline virtual ~RooBinnedPDF() {}

  Int_t getAnalyticalIntegral(RooArgSet& allVars, RooArgSet& analVars, const char* rangeName=0) const;
  Double_t analyticalIntegral(Int_t code, const char* rangeName=0) const;

//  Double_t median(Double_t min=0, Double_t max = -1) const;

//protected:
  // Function evaluation
  virtual Double_t evaluate() const ;
  RooRealProxy x_;
  int nbins_;
  RooListProxy args_;
  RooBinning binning_;

  ClassDef(RooBinnedPDF,1)
};

#endif


