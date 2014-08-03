#include "RooFit.h"
#include "RooMETConv.h"
#include "RooNumGenConfig.h"
#include "RooNumIntConfig.h"

#include "TMath.h"
#include "TString.h"
//#include "RooPlot.h"

using namespace TMath;
using namespace RooFit;

templateClassImp(RooMETConv)

//_____________________________________________________________________________
template <typename T> RooMETConv<T>::RooMETConv(const char *name, const char *title,
		RooAbsReal& _met, RooAbsReal& _res, RooAbsReal& _phi, T& _metPdf, RooAbsPdf& _resPdf, RooAbsPdf& _phiPdf, double _metShift, double _resBinsWidth, double _lowMETCont):
		//RooAbsReal& _met, RooAbsPdf& _metPdf, TH1D* _resHist, double _metShift, int _nBinsMET):
		RooAbsPdf(name, title),
		met("met","met",this,_met),
		res("res","res",this,_res),
		phi("phi","phi",this,_phi),
		metPdf("metPdf","metPdf",this,_metPdf),
		resPdf("resPdf","resPdf",this,_resPdf),
		phiPdf("phiPdf","phiPdf",this,_phiPdf)
{
	T* met_pdf = (T*)metPdf.absArg();
	RooAbsPdf* res_pdf = (RooAbsPdf*)resPdf.absArg();
	RooAbsPdf* phi_pdf = (RooAbsPdf*)phiPdf.absArg();

	RooRealVar* arg_met = (RooRealVar*)met.absArg();
	RooRealVar* arg_res = (RooRealVar*)res.absArg();
	RooRealVar* arg_phi = (RooRealVar*)phi.absArg();

	RooArgSet* res_observ = res_pdf->getObservables(RooArgSet(res.arg()));
	RooArgSet* res_params = res_pdf->getParameters(res_observ);
	setConst(res_observ);
	setConst(res_params);
	delete res_observ;
	delete res_params;

	double res_min = arg_res->getMin();
	double res_max = arg_res->getMax();
	int res_bins = int((res_max-res_min)/_resBinsWidth);
	//int res_bins = arg_res->getBins();//int((res_max-res_min)/_resBinsWidth);

	RooArgSet* phi_observ = phi_pdf->getObservables(RooArgSet(*arg_phi));
	RooArgSet* phi_params = phi_pdf->getParameters(phi_observ);
	setConst(phi_observ);
	setConst(phi_params);
	delete phi_observ;
	delete phi_params;

	double phi_min = arg_phi->getMin();
	double phi_max = arg_phi->getMax();
	int phi_bins = arg_phi->getBins();

	double met_min = arg_met->getMin();
	double met_max = arg_met->getMax();
	int met_bins = arg_met->getBins();

	lowMETCont = _lowMETCont;
	//// low MET templates
	//// as normalization range [norm_min,norm_max] is used, which should be the last bin of the template
	//if (lowMETTmpl!=0) {
	//	norm_min = lowMETTmpl->GetBinLowEdge(lowMETTmpl->GetNbinsX()-1);
	//	norm_max = norm_min+lowMETTmpl->GetBinWidth(lowMETTmpl->GetNbinsX());
	//	bcLowMET = lowMETTmpl->GetBinContent(lowMETTmpl->GetNbinsX()-1)+lowMETTmpl->GetBinContent(lowMETTmpl->GetNbinsX());
	//	arg_met->setRange("lowMETNormRange",norm_min,norm_max);
	//	lowMETNorm = met_pdf->createIntegral(RooArgSet(*arg_met),RooArgSet(*arg_met),"lowMETNormRange");
	//	//RooNumIntConfig* lowMETNorm_config = lowMETNorm->getIntegratorConfig();
	//	//lowMETNorm_config->Print();
	//} else {
	//	norm_min = 0;
	//	norm_max = 0;
	//	bcLowMET = 0;
	//	arg_met->setRange("lowMETNormRange",norm_min,norm_max);
	//	lowMETNorm = 0;
	//}

	RooProdPdf prod_pdf("prod_pdf","prod_pdf", RooArgList(*met_pdf,*res_pdf,*phi_pdf));

	RooArgSet* observ = prod_pdf.getObservables(RooArgSet(*arg_met,*arg_res,*arg_phi));
	cout << "[RooMETConv] " << GetName() << " observables: ";
	observ->Print();
	RooArgSet* params = prod_pdf.getParameters(observ);
	cout << "[RooMETConv] " << GetName() << " all parameters: ";
	params->Print();

	RooArgSet* floating_params = floatingParams(params);
	cout << "[RooMETConv] " << GetName() << " floating parameters: ";
	floating_params->Print();

	// save current parameters
	current_params = new RooArgSet("current_params");
	saveParams();
	current_params->Print();
	delete observ;
	delete params;
	delete floating_params;

	//cout << "[RooMETConv] " << GetName() << ": lowMETTemplate normalization range = [" << norm_min << "," << norm_max << "]" << endl;

	const char* namehsum( Form("h_sum_%s",name) );
	h_sum = new TH1D(namehsum,namehsum,met_bins,met_min,met_max);
	h_sum->Sumw2();

	neval_prod = 0;
//	res_max = 0;
	prod_met.reserve((met_bins+1)*(res_bins+1)*(phi_bins+1));
	prod_sum.reserve((met_bins+1)*(res_bins+1)*(phi_bins+1));
	prod_vol_const.reserve((met_bins+1)*(res_bins+1)*(phi_bins+1));
	double grid_met(met_min);
	arg_met->setVal(grid_met);
	for (int i=0; i<met_bins+1; i++) {
		double grid_res(res_min);
		arg_res->setVal(grid_res);
		for (int j=0; j<res_bins+1; j++) {
			double grid_phi(phi_min);
			arg_phi->setVal(grid_phi);
			for (int k=0; k<phi_bins+1; k++) {

				//if (j==0 && k==0) cout << "met = " << grid_met << endl;
				//if (i==0 && k==0) cout << "res = " << grid_res << endl;
				//if (i==0 && j==0) cout << "phi = " << grid_phi << endl;
				if (res_pdf->getVal()==0) {
					grid_phi += arg_phi->getBinWidth(k);
					arg_phi->setVal(grid_phi);
					continue;
				}
				double met_corr = grid_met+_metShift;
				double sum = sqrt(met_corr*met_corr + grid_res*grid_res - 2*met_corr*grid_res*cos(grid_phi));
				//if (sum>0.) continue;
				prod_sum.push_back( sum );
				prod_met.push_back(grid_met);

				prod_vol_const.push_back(arg_met->getBinWidth(i)*_resBinsWidth*arg_phi->getBinWidth(k)*res_pdf->getVal()*phi_pdf->getVal());
				//prod_vol_const.push_back(arg_met->getBinWidth(i)*arg_res->getBinWidth(j)*arg_phi->getBinWidth(k)*res_pdf->getVal()*phi_pdf->getVal());
				neval_prod++;

				grid_phi += arg_phi->getBinWidth(k);
				arg_phi->setVal(grid_phi);
			}
			//grid_res += 0.5*arg_res->getBinWidth(j);
			grid_res += _resBinsWidth;
			arg_res->setVal(grid_res);
		}
		grid_met += arg_met->getBinWidth(i);
		arg_met->setVal(grid_met);
	}
	cout << "[RooMETConv] \"" << GetName() << "\" initialized (#bins = " << prod_vol_const.size() << ")" << endl;
	cout << "[RooMETConv] \"" << GetName() << "\" met(" << met_bins << "," << met_min << "," << met_max << ")" << endl;
	cout << "[RooMETConv] \"" << GetName() << "\" res(" << res_bins << "," << res_min << "," << res_max << ")" << endl;
	cout << "[RooMETConv] \"" << GetName() << "\" phi(" << phi_bins << "," << phi_min << "," << phi_max << ")" << endl;
	updateConv();
	cout << "...done" << endl;
}

//_____________________________________________________________________________
template <typename T> RooMETConv<T>::RooMETConv(const RooMETConv& other, const char *name):
		RooAbsPdf(other,name),
		met("met",this,other.met),
		res("res",this,other.res),
		phi("phi",this,other.phi),
		metPdf("metPdf",this,other.metPdf),
		resPdf("resPdf",this,other.resPdf),
		phiPdf("phiPdf",this,other.phiPdf),

		neval_prod(other.neval_prod),
		h_sum(other.h_sum),
		prod_met(other.prod_met),
		prod_sum(other.prod_sum),
		prod_vol_const(other.prod_vol_const)
{
	// copy constructor
	lowMETCont = other.lowMETCont;

	// save current parameters
	current_params = new RooArgSet("current_params");
	saveParams();

	//if (lowMETTmpl!=0) {
	//	norm_min = lowMETTmpl->GetBinLowEdge(lowMETTmpl->GetNbinsX()-1);
	//	norm_max = norm_min+lowMETTmpl->GetBinWidth(lowMETTmpl->GetNbinsX());
	//	bcLowMET = lowMETTmpl->GetBinContent(lowMETTmpl->GetNbinsX()-1)+lowMETTmpl->GetBinContent(lowMETTmpl->GetNbinsX());
	//	arg_met->setRange("lowMETNormRange",norm_min,norm_max);
	//	lowMETNorm = met_pdf->createIntegral(RooArgSet(*arg_met),RooArgSet(*arg_met),"lowMETNormRange");
	//} else {
	//	norm_min = 0;
	//	norm_max = 0;
	//	bcLowMET = 0;
	//	arg_met->setRange("lowMETNormRange",norm_min,norm_max);
	//	lowMETNorm = 0;
	//}

	updateConv();
	cout << "[RooMETConv] \"" << other.GetName() << "\" copied with new name: " << name << endl;
}

//_____________________________________________________________________________
template <typename T> RooMETConv<T>::~RooMETConv()
{
	// destructor
	TIterator* itpar = current_params->createIterator();
	RooRealVar* par = 0;
	while ((par = (RooRealVar*)itpar->Next())) {
		current_params->remove(*par);
	}
	delete itpar;
	if (current_params) delete current_params;
}

//_____________________________________________________________________________
template <typename T> Double_t RooMETConv<T>::evaluate() const
{
	changedParams();
	double x = met;

	Double_t x0,x1,y0,y1;
	int nbins=h_sum->GetNbinsX();
	if (x<=h_sum->GetBinCenter(1)) {
		y0 = h_sum->GetBinContent(1);
		x0 = h_sum->GetBinCenter(1);
		y1 = h_sum->GetBinContent(2);
		x1 = h_sum->GetBinCenter(2);
	} else if(x>=h_sum->GetBinCenter(nbins)) {
		y0 = h_sum->GetBinContent(nbins-1);
		x0 = h_sum->GetBinCenter(nbins-1);
		y1 = h_sum->GetBinContent(nbins);
		x1 = h_sum->GetBinCenter(nbins);
	} else {
		Int_t xbin = h_sum->FindBin(x);
		if(x<=h_sum->GetBinCenter(xbin)) {
		  y0 = h_sum->GetBinContent(xbin-1);
		  x0 = h_sum->GetBinCenter(xbin-1);
		  y1 = h_sum->GetBinContent(xbin);
		  x1 = h_sum->GetBinCenter(xbin);
		} else {
		  y0 = h_sum->GetBinContent(xbin);
		  x0 = h_sum->GetBinCenter(xbin);
		  y1 = h_sum->GetBinContent(xbin+1);
		  x1 = h_sum->GetBinCenter(xbin+1);
		}
	}
	double ret = 0;
	if (y0==0) return ret;
	if (x<=lowMETCont) {
		//cout << x << " / " << y0*TMath::Power((y1/y0),(x-x0)/(x1-x0)) << endl;
		ret = y0*TMath::Power((y1/y0),(x-x0)/(x1-x0));
	}
	else {
		ret = y0*TMath::Power((y1/y0),(x-x0)/(x1-x0));
		//T* curr_pdf = (T*)metPdf.absArg();
		//RooRealVar* curr_met = (RooRealVar*)met.absArg();
		//curr_met->setVal(x0);
		//double fx0 = curr_pdf->getVal();
		//curr_met->setVal(x1);
		//double fx1 = curr_pdf->getVal();
		//curr_met->setVal(x);
		//double fx = curr_pdf->getVal();
		////cout << x << " / " << fx0 << " / " << fx1<< " / " << y0+(y0-y1)*(fx-fx0)/(fx0-fx1) << endl;
		//ret = y0+(y0-y1)*(fx-fx0)/(fx0-fx1);
	}
	return ret;
}

//_____________________________________________________________________________
template <typename T> bool RooMETConv<T>::changedParams() const
{
	T* curr_pdf = (T*)metPdf.absArg();
	RooRealVar* curr_met = (RooRealVar*)met.absArg();
	RooRealVar* curr_phi = (RooRealVar*)phi.absArg();
	RooRealVar* curr_res = (RooRealVar*)res.absArg();
	RooArgSet* obs = curr_pdf->getObservables(RooArgSet(*curr_met,*curr_res,*curr_phi));
	RooArgSet* pars = curr_pdf->getParameters(obs);
	bool anychanged = false;
	TIterator* itpar = pars->createIterator();
	RooRealVar* par = 0;
	while ((par = (RooRealVar*)itpar->Next())) {
		if (par->isConstant()) continue;
		RooRealVar* current_par = (RooRealVar*)current_params->find(Form("current_%s",par->GetName()));
		bool changed((par->getVal() != current_par->getVal()));
		if (changed) {
			//cout << current_par->GetName() << " has been changed from " << current_par->getVal() << " to " << par->getVal() << endl;
			current_par->setVal(par->getVal());
		}
		anychanged |= changed;
	}
	if (anychanged) {
		updateConv();
	}
	delete obs;
	delete pars;
	delete itpar;
	return anychanged;
}

//_____________________________________________________________________________
template <typename T> void RooMETConv<T>::updateConv() const
{
	cout << ">" << flush;
	T* curr_pdf = (T*)metPdf.absArg();
	RooRealVar* curr_met = (RooRealVar*)met.absArg();
	double curr_val = curr_met->getVal();
	h_sum->Reset();
	for ( unsigned int i=0; i<neval_prod; ++i ) {
		if (prod_met[i]>lowMETCont) {
			curr_met->setVal(prod_met[i]);
			h_sum->Fill(prod_sum[i], prod_vol_const[i]*curr_pdf->getVal());
		}
		else {
			double val = 0;
			//if (lowMETTmpl!=0) {
			//	val = lowMETTmpl->Interpolate(prod_met[i])*lowMETNorm->getVal(RooArgSet(*curr_met))/bcLowMET/(norm_max-norm_min);
			//}
			curr_met->setVal(lowMETCont);
			double dx0 = curr_pdf->getVal();
			curr_met->setVal(lowMETCont+1);
			double dx1 = curr_pdf->getVal();
			double alpha = 1/lowMETCont-(dx1-dx0)/dx0;
			double beta = dx0/lowMETCont*TMath::Exp(alpha*lowMETCont);
			val = beta*prod_met[i]*TMath::Exp(-alpha*prod_met[i]);
			h_sum->Fill(prod_sum[i], prod_vol_const[i]*val);
		}
	}
	curr_met->setVal(curr_val);
	h_sum->Smooth(1);
	cout << "<" << flush;
}

//_____________________________________________________________________________
template <typename T> void RooMETConv<T>::saveParams() const
{
	T* curr_pdf = (T*)metPdf.absArg();
	RooRealVar* arg_met = (RooRealVar*)met.absArg();
	RooRealVar* arg_phi = (RooRealVar*)phi.absArg();
	RooRealVar* arg_res = (RooRealVar*)res.absArg();
	RooArgSet* obs = curr_pdf->getObservables(RooArgSet(*arg_met,*arg_res,*arg_phi));
	RooArgSet* pars = curr_pdf->getParameters(obs);
	TIterator* itpar = pars->createIterator();
	RooRealVar* par = 0;
	if (current_params->getSize()==0) {
		while ((par = (RooRealVar*)itpar->Next())) {
			if (par->isConstant()) continue;
			RooRealVar* curr_par = (RooRealVar*)par->Clone(Form("current_%s",par->GetName()));
			current_params->add(*curr_par);
		}
	} else {
		while ((par = (RooRealVar*)itpar->Next())) {
			if (par->isConstant()) continue;
			((RooRealVar*)current_params->find(Form("current_%s",par->GetName())))->setVal(par->getVal());
		}
	}
	delete obs;
	delete pars;
	delete itpar;

}

//_____________________________________________________________________________
template <typename T> RooArgSet* RooMETConv<T>::floatingParams(RooArgSet* pars) const
{
	TIterator* itpar = pars->createIterator();
	RooRealVar* par = 0;
	RooArgSet* fargs = new RooArgSet("floating_parameters");
	while ((par = (RooRealVar*)itpar->Next())) {
		if (par->isConstant()) continue;
		fargs->add(*par);
	}
	delete itpar;
	return fargs;
}

//_____________________________________________________________________________
template <typename T> void RooMETConv<T>::setConst(RooArgSet* pars) const
{
	TIterator* itpar = pars->createIterator();
	RooRealVar* par = 0;
	while ((par = (RooRealVar*)itpar->Next())) {
		par->setConstant(true);
	}
	delete itpar;
}

//_____________________________________________________________________________
template <typename T> void RooMETConv<T>::setParams(RooArgSet* pars) const
{
	TIterator* itpar = pars->createIterator();
	RooRealVar* par = 0;
	while ((par = (RooRealVar*)itpar->Next())) {
		((RooRealVar*)current_params->find(par->GetName()))->setVal(par->getVal());
	}
	delete itpar;
}

//_____________________________________________________________________________
template <typename T> Double_t RooMETConv<T>::expInterpolate(Double_t x, Double_t *par) const
{
   //Double_t alpha = (TMath::Log(par[1])-TMath::Log(par[3]))/(par[0]-par[2]);
   //Double_t beta = par[1]/TMath::Exp(alpha*par[0]);

   //Double_t f = beta*TMath::Exp(alpha*x);
   Double_t f = par[1]*TMath::Power(par[3]/par[1],(x-par[0])/(par[2]-par[0]));
   return f;
}


