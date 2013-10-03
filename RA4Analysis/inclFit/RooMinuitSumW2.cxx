/*****************************************************************************
 * Extension to RooMinuit to allow for a correct treatment of SumW2Errors    *
 *****************************************************************************/
#include "RooMinuitSumW2.h"
#include "RooNLLVar.h"
#include "RooArgSet.h"
#include "RooFitResult.h"
#include "TIterator.h"
#include "TMatrixD.h"
#include "TMatrixDSym.h"
#include "TString.h"

#include <list>

ClassImp(RooMinuitSumW2);

//_____________________________________________________________________________
RooMinuitSumW2::RooMinuitSumW2(RooAbsReal& function) : RooMinuit(function)
{
	_nll = &function;
	_fitstatus = -1;
}



//_____________________________________________________________________________
RooMinuitSumW2::~RooMinuitSumW2()
{
	// Destructor
}



//_____________________________________________________________________________
RooFitResult* RooMinuitSumW2::fit(const char* options, bool sumW2)
{
	TString opts(options);
	TString o = options;
	if (!opts.Contains("m")) {
		cout << "RooMinuitSumW2::fit() Minos not supported, use RooMinuit class instead. Will run Migrad only!" << endl ;
		o += "m";
	}
	RooMinuit::fit(o.Data());
	_fitstatus = save()->status();
	if (sumW2 and (_fitstatus != -1)) correctForSumW2Errors();
	return (opts.Contains("r")) ? save() : 0 ;
}

//_____________________________________________________________________________
Int_t RooMinuitSumW2::migrad(bool sumW2)
{
	_fitstatus = RooMinuit::migrad();
	if (sumW2 and (_fitstatus !=  -1)) correctForSumW2Errors();
	return _fitstatus;
}

//_____________________________________________________________________________
Int_t RooMinuitSumW2::hesse(bool sumW2)
{
	Int_t status = RooMinuit::hesse();
	if (sumW2 and (_fitstatus !=  -1)) correctForSumW2Errors();
	return status;
}

//_____________________________________________________________________________
Int_t RooMinuitSumW2::minos()
{
	cout << "RooMinuitSumW2::minos() Minos not supported, use RooMinuit class instead." << endl ;
	return -1 ;
}

//_____________________________________________________________________________
Int_t RooMinuitSumW2::minos(const RooArgSet& minosParamList)
{
	minosParamList.getSize();
	cout << "RooMinuitSumW2::minos() Minos not supported, use RooMinuit class instead." << endl ;
	return -1 ;
}


//_____________________________________________________________________________
Int_t RooMinuitSumW2::seek()
{
	Int_t status = RooMinuit::seek();
	return status;
}

//_____________________________________________________________________________
Int_t RooMinuitSumW2::simplex()
{
	Int_t status = RooMinuit::simplex();
	return status;
}

//_____________________________________________________________________________
Int_t RooMinuitSumW2::improve(bool sumW2)
{
	Int_t status = RooMinuit::improve();
	if (sumW2 and (status !=  -1)) correctForSumW2Errors();
	return status;
}

//_____________________________________________________________________________
void RooMinuitSumW2::correctForSumW2Errors()
{
	// Make list of RooNLLVar components of FCN
	list<RooNLLVar*> nllComponents ;
	RooArgSet* comps = _nll->getComponents() ;
	RooAbsArg* arg ;
	TIterator* citer = comps->createIterator() ;
	while((arg=(RooAbsArg*)citer->Next())) {
		RooNLLVar* nllComp = dynamic_cast<RooNLLVar*>(arg) ;
		if (nllComp) {
			nllComponents.push_back(nllComp) ;
		}
	}
	delete citer ;
	delete comps ;

	// Calculated corrected errors for weighted likelihood fits
	RooFitResult* rw = save() ;
	for (list<RooNLLVar*>::iterator iter1=nllComponents.begin() ; iter1!=nllComponents.end() ; iter1++) {
		(*iter1)->applyWeightSquared(kTRUE) ;
	}
	cout << "RooMinuitSumW2::correctSumW2Errors() Calculating sum-of-weights-squared correction matrix for covariance matrix" << endl ;
	hesse(false);
	RooFitResult* rw2 = save() ;
	for (list<RooNLLVar*>::iterator iter2=nllComponents.begin() ; iter2!=nllComponents.end() ; iter2++) {
		(*iter2)->applyWeightSquared(kFALSE) ;
	}

	// Apply correction matrix
	TMatrixDSym V = rw->covarianceMatrix() ;
	TMatrixDSym C = rw2->covarianceMatrix() ;

	// Invert C
	Double_t det(0) ;
	C.Invert(&det) ;
	if (det==0) {
		cout << "RooMinuitSumW2::correctSumW2Errors() ERROR: Cannot apply sum-of-weights correction to covariance matrix: correction matrix calculated with weight-squared is singular" <<endl ;
	} else {

		// Calculate corrected covariance matrix = V C-1 V
		TMatrixD VCV(V,TMatrixD::kMult,TMatrixD(C,TMatrixD::kMult,V)) ;

		// Make matrix explicitly symmetric
		Int_t n = VCV.GetNrows() ;
		TMatrixDSym VCVsym(n) ;
		for (Int_t i=0 ; i<n ; i++) {
			for (Int_t j=i ; j<n ; j++) {
				if (i==j) {
					VCVsym(i,j) = VCV(i,j) ;
				}
				if (i!=j) {
					Double_t deltaRel = (VCV(i,j)-VCV(j,i))/sqrt(VCV(i,i)*VCV(j,j)) ;
					if (fabs(deltaRel)>1e-3) {
						cout << "RooMinuitSumW2::correctSumW2Errors() WARNING: Corrected covariance matrix is not (completely) symmetric: V[" << i << "," << j << "] = "
								<< VCV(i,j) << " V[" << j << "," << i << "] = " << VCV(j,i) << " explicitly restoring symmetry by inserting average value" << endl ;
					}
					VCVsym(i,j) = (VCV(i,j)+VCV(j,i))/2 ;
					VCVsym(j,i) = (VCV(i,j)+VCV(j,i))/2 ;
				}
			}
		}
		cout << "corrected covariance matrix:" << endl;
		VCVsym.Print();
		// Propagate corrected errors to parameters objects
		applyCovarianceMatrix(VCVsym);
		for (Int_t i = 0; i < getNPar(); i++) {
			clearPdfParamAsymErr(i);
		}
	}
	delete rw ;
	delete rw2;
}


