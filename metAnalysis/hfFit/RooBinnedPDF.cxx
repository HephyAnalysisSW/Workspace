#include "RooFit.h"
#include "RooRealVar.h"
#include "Riostream.h"

#include "RooBinnedPDF.h"
#include "TMath.h"
using namespace std;

ClassImp(RooBinnedPDF)

RooBinnedPDF::RooBinnedPDF(const char *name, const char *title, RooAbsReal& _x, RooArgList & args, RooBinning & binning): 
RooAbsPdf(name,title),
x_("x","x",this,_x),
nbins_(args.getSize()),
args_("args","args",this),
binning_(binning)
{
  TIterator* coefIter = args.createIterator() ;
  RooAbsArg* coef;
  while((coef = (RooAbsArg*)coefIter->Next())) {
    if (!dynamic_cast<RooAbsReal*>(coef)) {
      cout << "ERROR: RooBinnedPDF::RooBinnedPDF(" << GetName() << ") coefficient " << coef->GetName() << " is not of type RooAbsReal" << endl;
      assert(0);
    }
    args_.add(*coef) ;    
  }
  delete coefIter;

  if (nbins_!=binning_.numBins()) cout<<"[RooBinnedPDF] Warning! Number of args ("<<nbins_<<") and numBins ("<<binning_.numBins()<<") inconsistent!"<<endl; 
  for (int i = 0; i<nbins_; i++){
    cout<<"Arg "<<i<<" bin: "<<binning_.binLow(i)<<" "<<binning_.binHigh(i)<<" val: "; args.at(i)->Print(); cout<<endl;
  }
}

//_____________________________________________________________________________
RooBinnedPDF::RooBinnedPDF(const RooBinnedPDF& other, const char* name) :
      RooAbsPdf(other, name),
      x_("x",this,other.x_),
      nbins_(other.args_.getSize()),
      args_("args", this, other.args_),
      binning_(other.binning_)
{
 // cout<<"In copy constr."<<endl;  // copy constructor
}

//_____________________________________________________________________________
Double_t RooBinnedPDF::evaluate() const
{
//  cout<<"x_ "<<x_<<" "<<nbins_<<endl;
  double ret = 0.;
  for (int i = 0; i<nbins_; i++){
//    cout<<"b "<<binning_.binLow(i)<<" "<<binning_.binHigh(i)<<endl;  
    if ( (x_>=binning_.binLow(i)) and (x_<binning_.binHigh(i))) {
//      cout<<i; args_.at(i)->Print();
      ret = ((RooRealVar*)args_.at(i))->getVal();
      break;
    }
  }
  return ret;
}



//_____________________________________________________________________________
Int_t RooBinnedPDF::getAnalyticalIntegral(RooArgSet& allVars, RooArgSet& analVars, const char* /*rangeName*/) const
{
  if (matchArgs(allVars,analVars,x_)) return 1;
  return 0;
}



//_____________________________________________________________________________
Double_t RooBinnedPDF::analyticalIntegral(Int_t code, const char* rangeName) const
{
  assert(code==1);
  double ret = 0.;
  if(code==1){
    Double_t xmin = x_.min(rangeName);
    Double_t xmax = x_.max(rangeName);
//    cout<<"xmin,xmax "<<xmin<<" "<<xmax<<endl;
    if (xmin<xmax) {
      for (int i=0; i<nbins_; i++) {
        double bL = binning_.binLow(i);
        double bH = binning_.binHigh(i);
        if ((xmin>bH) or (xmax<bL)) continue;
        if (xmin>bL) bL=xmin;
        if (xmax<bH) bH=xmax; 
        ret += (bH - bL)*((RooRealVar*)args_.at(i))->getVal();
//        cout<<"Adding for bin "<<i<<": bH-bL "<<bH-bL<<" * "<<((RooRealVar*)args_.at(i))->getVal()<<", ret now "<<ret<<endl;
      }
    } else {
      cout << "Error in RooBinnedPDF::analyticalIntegral" << endl;
    }
//    cout<<" Integral: "<<ret<<endl;
    return ret;
  }
}



////_____________________________________________________________________________
//Double_t RooBinnedPDF::median(Double_t min, Double_t max) const
//{
//  double r = scale/shape+location;
//  double invshape = 1/shape;
//  double zmin = TMath::Power(1+min/r,-invshape);
//  double zmax = (max!=-1) ? TMath::Power(1+max/r,-invshape) : 0;
//  double ret = (TMath::Power((zmin+zmax)/2,-shape)-1)*scale/shape+location;
//  return ret;
//}
