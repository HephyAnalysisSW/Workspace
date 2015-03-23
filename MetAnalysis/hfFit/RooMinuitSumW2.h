/*****************************************************************************
 * Extension to RooMinuit to allow for a correct treatment of SumW2Errors    *
 *****************************************************************************/
#ifndef ROO_MINUITSUMW2
#define ROO_MINUITSUMW2

#include "RooMinuit.h"

class RooMinuit;

class RooMinuitSumW2 : public RooMinuit {
public:
	RooMinuitSumW2(RooAbsReal& function) ;
	virtual ~RooMinuitSumW2();

	RooFitResult* fit(const char* options, bool sumW2);
	Int_t migrad(bool sumW2);
	Int_t hesse(bool sumW2);
	Int_t minos();
	Int_t minos(const RooArgSet& minosParamList) ;  // added FMV, 08/18/03
	Int_t seek();
	Int_t simplex();
	Int_t improve(bool sumW2);

	void correctForSumW2Errors();
private:
	RooAbsReal * _nll;
	Int_t _fitstatus;

	ClassDef(RooMinuitSumW2,0) // RooFit minimizer based on MINUIT
};


#endif
