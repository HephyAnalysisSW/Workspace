#include "TH2.h"
#include "TMatrixD.h"
#include "TVectorD.h"
#include "TCanvas.h"
#include "TFile.h"
#include "TKey.h"
#include "Triplet.h"
#include "FcnLogL.C"
#include "TFitterMinuit.h"

#include <string>
#include <vector>
#include <iostream>
#include "assert.h"

using namespace std;

TH2* HEffErr(0);
TH2* HEffWidth(0);

//
// identify empty bins
//
bool isEmpty (double contents) {
  return fabs(contents)<1.e-10;
}
bool isEmpty (TH2* h, int ix, int iy) {
  return isEmpty(h->GetBinContent(ix,iy));
}

bool fit (const std::vector<BinContentTriplet>& triplets, double& value, double& error)
{
  bool result(false);
  value = 0.;
  error = 0.;

  FcnLogL* fcn = new FcnLogL(triplets,10000);

  double ave(0.);
  for ( size_t i=0; i<triplets.size(); ++i ) ave += triplets[i].z();
  ave /= triplets.size();

  // move to logarithmic scale
  ave = log(ave);
  double delta = sqrt(triplets.size())/2.;
  TFitterMinuit* minuitx = new TFitterMinuit();
  minuitx->SetMinuitFCN(fcn);
  minuitx->SetParameter(0,"a",ave,log(0.001),log(1.e-10),0.);
  minuitx->SetParameter(1,"ax",0.,fabs(log(1.e-10)/delta/100.),-100,100);
  minuitx->SetParameter(2,"ay",0.,fabs(log(1.e-10)/delta/100.),-100,100);
  minuitx->SetParameter(3,"axx",0.,fabs(log(1.e-10)/delta/delta/10.),-100,100);
  minuitx->SetParameter(4,"axy",0.,fabs(log(1.e-10)/delta/delta/10.),-100,100);
  minuitx->SetParameter(5,"ayy",0.,fabs(log(1.e-10)/delta/delta/10.),-100,100);
  // first fit: constant
  minuitx->FixParameter(1);
  minuitx->FixParameter(2);
  minuitx->FixParameter(3);
  minuitx->FixParameter(4);
  minuitx->FixParameter(5);
  minuitx->SetMaxIterations(100);
  minuitx->SetPrintLevel(0);
  minuitx->CreateMinimizer();
  int ierr = minuitx->Minimize();
  if ( ierr == 0 ) {
    result = true;
    value = minuitx->GetParameter(0);
    error = minuitx->GetParError(0);
  }
  // second fit: linear
  minuitx->ReleaseParameter(1);
  minuitx->ReleaseParameter(2);
  ierr = minuitx->Minimize();
  if ( ierr == 0 ) {
    result = true;
    value = minuitx->GetParameter(0);
    error = minuitx->GetParError(0);
  }
  // third fit: quadratic
  minuitx->ReleaseParameter(3);
  minuitx->ReleaseParameter(4);
  minuitx->ReleaseParameter(5);
  ierr = minuitx->Minimize();
  if ( ierr == 0 ) {
    result = true;
    value = minuitx->GetParameter(0);
    error = minuitx->GetParError(0);
  }

  delete minuitx;
  //
  // back from logarithmic scale
  //
  value = exp(value);
  error *= value;

  return result;
}

// Smoothing of distributions in the msugra plane
//

//
// extract histogram with limits from
//   a canvas in a root file
//
TH2* findLimitHisto (TFile* file, std::string hname) {
  // result == 0 : failure
  TH2* result(0);
  //
  // find TCanvas in TFile
  //
  TIter itKey(file->GetListOfKeys());
  TObject* obj;
  TKey* key;
  TCanvas* cnv(0);
  while ( (key=(TKey*)itKey.Next()) ) {
    obj = key->ReadObj();
    if ( obj->IsA()==TCanvas::Class() ) {
      if ( cnv ) {
  cout << "Found multiple canvases" << endl;
  return result;
      }
      cnv = (TCanvas*)obj;
    }
  }
  if ( cnv == 0 ) {
    cout << "No canvas" << endl;
    return result;
  }
  //
  // find TH2 in TCanvas
  //
  vector<TPad*> pads(1,(TPad*)cnv);
  for ( size_t ipad=0; ipad<pads.size(); ++ipad ) {
    TIter itC(pads[ipad]->GetListOfPrimitives());
    while ( (obj=(TObject*)itC.Next()) ) {
      if ( obj->InheritsFrom(TH2::Class()) ) {
  TH2* h = (TH2*)obj;
  if ( string(h->GetName()) == hname )  return h;
//  cout << "Found histogram " << h->GetName() << endl;
//  if ( result ) {
//    cout << "Found multiple histograms" << endl;
//    return (TH2*)0;
//  }
//  result = (TH2*)obj;
      }
      else if ( obj->InheritsFrom(TPad::Class()) ) {
//  cout << "Found " << obj->ClassName() << endl;
  pads.push_back((TPad*)obj);
      }
    }
  }
//   return result;
  cout << "Did not find histogram" << endl;
  return (TH2*)0;
}
//
// extract histogram with JES signal systematics from
//   a canvas in a root file
//
TH2* findJesHisto (TFile* file) {
  // result == 0 : failure
  TH2* result(0);
  //
  // find TCanvas in TFile
  //
  TIter itKey(file->GetListOfKeys());
  TObject* obj;
  TKey* key;
  TCanvas* cnv(0);
  while ( (key=(TKey*)itKey.Next()) ) {
    obj = key->ReadObj();
    if ( obj->IsA()==TCanvas::Class() ) {
      if ( cnv ) {
  cout << "Found multiple canvases" << endl;
  return result;
      }
      cnv = (TCanvas*)obj;
    }
  }
  if ( cnv == 0 ) {
    cout << "No canvas" << endl;
    return result;
  }
  //
  // find TH2 in TCanvas
  //
  TIter itC(cnv->GetListOfPrimitives());
  while ( (obj=(TObject*)itC.Next()) ) {
    if ( obj->InheritsFrom(TH2::Class()) ) {
      if ( result ) {
  cout << "Found multiple histograms" << endl;
  return (TH2*)0;
      }
      result = (TH2*)obj;
    }
  }
  return result;
}

void fillTriplets (std::vector<BinContentTriplet>& triplets, TH2* h, int nbx, int nby,
       int ix, int iy, int delta, int prevDelta=-1 )
{
  for ( int jx=-delta; jx<=delta; ++jx ) {
    for ( int jy=-delta; jy<=delta; ++jy ) {
      if ( abs(jx)<=prevDelta && abs(jy)<=prevDelta ) continue;
      if ( (ix+jx)<1 || (ix+jx)>nbx )  continue;
      if ( (iy+jy)<1 || (iy+jy)>nby )  continue;
      // skip empty neighbours
      double z =  h->GetBinContent(ix+jx,iy+jy);
      if ( z<1.e-10 )  continue;
      triplets.push_back(BinContentTriplet(jx,jy,z));
    }
  }
}

TH2* fitMissing (TH2* h) {
  HEffErr = (TH2*)h->Clone("HEffErr");
  HEffErr->SetTitle("EffErr");
  HEffErr->Reset();
  HEffWidth = (TH2*)h->Clone("HEffWidth");
  HEffWidth->SetTitle("EffWidth");
  HEffWidth->Reset();

  TH2* hNew = (TH2*)h->Clone("hSmoothFit");
  hNew->Reset();
  hNew->SetTitle("hSmoothFit");
  int nbx = h->GetNbinsX();
  int nby = h->GetNbinsY();

  //
  // loop over histogram (excluding a 1-bin wide margin)
  //
  bool fitSucceeded(false);
  double fittedValue(0);
  double fittedError(0);
  std::vector<BinContentTriplet> triplets;
  for ( int ix=1; ix<=nbx; ++ix ) {
    for ( int iy=1; iy<=nby; ++iy ) {

      // clear matrix and vector used for fit
      fitSucceeded = false;
      triplets.clear();

      int delta(1);
      int prevDelta(-1);
      double maxErr(0.05);
      for ( delta=1; delta<10; ++delta ) {
  // loop over neighbours
  fillTriplets (triplets,h,nbx,nby,ix,iy,delta,prevDelta);
  prevDelta = delta;
  if ( triplets.size()>=max(8,(2*delta+1)*(2*delta+1)/2) ) {
    fitSucceeded = fit(triplets,fittedValue,fittedError);
    if ( fitSucceeded && fittedError<maxErr*fittedValue )  break;
  }
      }
      if ( fitSucceeded && fittedError<0.2*fittedValue ) {
  hNew->SetBinContent(ix,iy,fittedValue);
  HEffErr->SetBinContent(ix,iy,fittedError/fittedValue);
  HEffWidth->SetBinContent(ix,iy,2*delta+1);
      }
    }
  }
  delete HEffErr;
  delete HEffWidth;
  return hNew;
}

//
// fill missing bins in histogram h fitting a plane to the 
//   surrounding bins 
//   nmin: minimum number of non-empty neighbours
//
TH2* fillMissing (TH2* h, int nmin=5, int nmin2=14, bool useLog = false) {
  //
  // prepare histogram
  //
  TH2* hNew = (TH2*)h->Clone("hFilled");
  hNew->SetTitle("hFilled");
  int nbx = h->GetNbinsX();
  int nby = h->GetNbinsY();
  //
  // matrix and vector for fit
  //
  TMatrixD mat(3,3);
  TVectorD cvec(3);
  //
  // loop over histogram (excluding a 1-bin wide margin)
  //
  for ( int ix=1; ix<=nbx; ++ix ) {
    for ( int iy=1; iy<=nby; ++iy ) {
      // check only empty bins
      if ( !isEmpty(h,ix,iy) )  continue;
      // clear matrix and vector used for fit
      int nn(0);
      for ( int i=0; i<3; ++i ) {
	cvec(i) = 0.;
	for ( int j=0; j<3; ++j ) mat(i,j) = 0.;
      }
      // loop over neighbours
      for ( int jx=-1; jx<2; ++jx ) {
	for ( int jy=-1; jy<2; ++jy ) {
	  // skip the central bin (the one to be filled)
	  if ( jx==0 && jy==0 )  continue;
	  if ( (ix+jx)<1 || (ix+jx)>nbx )  continue;
	  if ( (iy+jy)<1 || (iy+jy)>nby )  continue;
	  // skip empty neighbours
	  double z =  h->GetBinContent(ix+jx,iy+jy);
	  if ( isEmpty(z) )  continue;
	  if ( useLog )  z = log(z);
	  // update matrix and vector
	  ++nn;
	  mat(0,0) += jx*jx; mat(0,1) += jx*jy; mat(0,2) += jx;
	  mat(1,0) += jx*jy; mat(1,1) += jy*jy; mat(1,2) += jy;
	  mat(2,0) += jx;    mat(2,1) += jy;    mat(2,2) += 1;
	  cvec(0)  += jx*z;  cvec(1)  += jy*z;  cvec(2)  += z;
	}
      }
      // if < nmin neighbours in delta_i==1: try to add delta_i==2
      if ( nn<nmin ) {
	// loop over neighbours
	for ( int jx=-2; jx<3; ++jx ) {
	  for ( int jy=-2; jy<3; ++jy ) {
	    // skip the central bin (the one to be filled)
	    if ( abs(jx)<2 && abs(jy)<2 )  continue;
	    if ( (ix+jx)<1 || (ix+jx)>nbx )  continue;
	    if ( (iy+jy)<1 || (iy+jy)>nby )  continue;
	    // skip empty neighbours
	    double z =  h->GetBinContent(ix+jx,iy+jy);
	    if ( isEmpty(z) )  continue;
	    if ( useLog )  z = log(z);
	    // update matrix and vector
	    ++nn;
	    mat(0,0) += jx*jx; mat(0,1) += jx*jy; mat(0,2) += jx;
	    mat(1,0) += jx*jy; mat(1,1) += jy*jy; mat(1,2) += jy;
	    mat(2,0) += jx;    mat(2,1) += jy;    mat(2,2) += 1;
	    cvec(0)  += jx*z;  cvec(1)  += jy*z;  cvec(2)  += z;
	  }
	}
	// drop bin if <nmin2 in 5x5 area
	if ( nn<nmin2 ) continue;
      }
//       cout << "x / y = " << h->GetXaxis()->GetBinCenter(ix) << " " 
//                          << h->GetYaxis()->GetBinCenter(iy) << endl;
      // 
      // linear 2D fit to neighbours (in units of bin number): 
      //   par(0)*(x-ix)+par(1)*(y-iy)+par(2)
      //
      double det = mat.Determinant();
      if ( det < 1.e-6 )  continue;
//       TMatrixD mat1(mat);
      mat.Invert(&det);
      TVectorD par = mat*cvec;
//       TVectorD tmp = mat1*par;
      if ( useLog )
	hNew->SetBinContent(ix,iy,exp(par(2)));
      else
	hNew->SetBinContent(ix,iy,par(2));
    }
  }
  return hNew;
}
//
// clear bins which were empty in a reference histogram
//
void clearBins (TH2* histo, TH2* refHisto) {
  int nbx = refHisto->GetNbinsX();
  int nby = refHisto->GetNbinsY();
  // loop over bins
  for ( int ix=1; ix<=nbx; ++ix ) {
    for ( int iy=1; iy<=nby; ++iy ) {
      if ( isEmpty(refHisto,ix,iy) )
	histo->SetBinContent(ix,iy,0.);
    }
  }
}
// //
// // clear bins with more than nmax empty neighbours
// //   (remove artefacts of smoothing at the edges of
// //    the physical region)
// //
// void clearBins (TH2* histo, TH2* refHisto, int nmax = 1) {
//   int nbx = refHisto->GetNbinsX();
//   int nby = refHisto->GetNbinsY();
//   // loop over bins
//   for ( int ix=1; ix<=nbx; ++ix ) {
//     for ( int iy=1; iy<=nby; ++iy ) {
//       int nempty(0);
//       // loop over neighbours
//       for ( int jx=ix-1; jx<ix+2; ++jx ) {
//  if ( jx<1 || jx>nbx )  continue;
//  for ( int jy=iy-1; jy<iy+2; ++jy ) {
//    if ( jy<1 || jy>nby )  continue;
//    if ( fabs(refHisto->GetBinContent(jx,jy))<1.e-10 )  ++nempty;
//  }
//       }
//       // clear bin if > nmax empty neighbours
//       if ( nempty>nmax )  histo->SetBinContent(ix,iy,0.);
//     }
//   }
// }

//
// perform filling of (isolated) empty bins and smoothing
//   on an efficiency histogram in the msugra plane
//   algo:   name of smoothing algorithm
//   nTimes: # of times the algorithm is applied
//   ratio:  if true return ratio smoothed / raw; else smoothed
//
TH2* doSmoothEff (TH2* hRaw, bool ratio = true, bool draw = false) {
  //
  // fill isolated empty bins
  //
  TH2* hFilled = fillMissing(hRaw);
//   TH2* hFilledLoose = fillMissing(hRaw,4,6);

  TCanvas* c(0);
//   if ( draw ) {
//     c = new TCanvas("cFilled","cFilled");
//     hFilled->Draw("ZCOL");
//   }
  //
  // smooth histogram 
  //
  TH2* hSmooth = fitMissing(hFilled);
  delete hFilled;
  hSmooth->SetName("hSmooth");
  hSmooth->SetTitle("hSmooth");
//   if ( draw ) {
//     c = new TCanvas("cSmooth","cSmooth");
//     hSmooth->Draw("ZCOL");
//   }
  //
  // relative difference smoothed/raw (cross check)
  //
//   if ( draw ) {
//     TH2* hRelDiff = (TH2*)hFilled->Clone("hRelDiff");
//     hRelDiff->SetTitle("hRelDiff");
//     hRelDiff->Add(hSmooth,-1);
//     hRelDiff->Divide(hSmooth);
//     hRelDiff->SetMinimum(-0.15);
//     hRelDiff->SetMaximum(0.15);
//     hRelDiff->Smooth();
//     hRelDiff->Smooth();
//     c = new TCanvas("cRelDiff","cRelDiff");
//     hRelDiff->Draw("ZCOL");
//   }
//   //
//   // ratio smoothed / raw
//   //
  TH2* hRatio(0);
//   if ( draw || ratio ) {
//     hRatio = (TH2*)hSmooth->Clone("hRatio");
//     hRatio->SetTitle("hRatio");
//     hRatio->Divide(hFilled);
//     hRatio->SetMinimum(0.5);
//     hRatio->SetMaximum(1.5);
// //   hRatio->Smooth();
// //   hRatio->Smooth();
//     if ( draw ) {
//       c = new TCanvas("cRatio","cRatio");
//       hRatio->Draw("ZCOL");
//     }
//   }

  return ratio ? hRatio : hSmooth;
}
//
// perform filling of (isolated) empty bins and smoothing
//   on an efficiency histogram in the msugra plane
//   algo:   name of smoothing algorithm
//   nTimes: # of times the algorithm is applied
//   ratio:  if true return ratio smoothed / raw; else smoothed
//
TH2* doSmooth (TH2* hRaw, const char* algo = "k3a", int nTimes = 2, bool ratio = true, bool draw = false, bool useLog = false) {
  //
  // fill isolated empty bins
  //
  TH2* hFilled = fillMissing(hRaw,5,14,useLog);
  TH2* hFilledLoose = fillMissing(hRaw,4,6,useLog);
  //
  // if required: draw histogram after filling step
  //
  TCanvas* c(0);
  if ( draw ) {
    c = new TCanvas("cFilled","cFilled");
//     hFilledLoose->Draw("ZCOL");
//     hFilled->Draw("same box");
    TH2* hTmp = (TH2*)hFilledLoose->Clone("hTmp");
    for ( int ix=1; ix<=hTmp->GetNbinsX(); ++ix ) {
      for ( int iy=1; iy<=hTmp->GetNbinsY(); ++iy ) {
	if ( !isEmpty(hFilled,ix,iy) )  hTmp->SetBinContent(ix,iy,0.);
      }
    }
    if ( useLog ) {
      hTmp->SetMinimum(1.e-10);
      c->SetLogz(1);
    }
    hTmp->Draw("ZCOL");
    c = new TCanvas("cRaw","cRaw");
    hRaw->Draw("ZCOL");
    c = new TCanvas("cFill","cFill");
    hFilled->Draw("ZCOL");
//     hRaw->Draw("same box");
  }
  //
  // smooth histogram 
  //
  TH2* hSmooth = (TH2*)hFilledLoose->Clone("hSmooth");
  hSmooth->SetTitle("hSmooth");
  // (first parameter in Smooth is dummy)
  for ( int i=0; i<nTimes; ++i )  hSmooth->Smooth(1,algo);
  // remove artefacts on edges of the filled region
  clearBins(hSmooth,hFilled);
  if ( draw ) {
    c = new TCanvas("cSmooth","cSmooth");
    hSmooth->Draw("ZCOL");
  }
  //
  // relative difference smoothed/raw (cross check)
  //
  if ( draw ) {
    TH2* hRelDiff = (TH2*)hFilled->Clone("hRelDiff");
    hRelDiff->SetTitle("hRelDiff");
    hRelDiff->Add(hSmooth,-1);
    hRelDiff->Divide(hSmooth);
    hRelDiff->SetMinimum(-0.15);
    hRelDiff->SetMaximum(0.15);
    hRelDiff->Smooth();
    hRelDiff->Smooth();
    c = new TCanvas("cRelDiff","cRelDiff");
    hRelDiff->Draw("ZCOL");
  }
  //
  // ratio smoothed / raw
  //
  TH2* hRatio(0);
  if ( draw || ratio ) {
    hRatio = (TH2*)hSmooth->Clone("hRatio");
    hRatio->SetTitle("hRatio");
    hRatio->Divide(hFilled);
    hRatio->SetMinimum(0.5);
    hRatio->SetMaximum(1.5);
//   hRatio->Smooth();
//   hRatio->Smooth();
    if ( draw ) {
      c = new TCanvas("cRatio","cRatio");
      hRatio->Draw("ZCOL");
    }
  }

  return ratio ? hRatio : hSmooth;
}
//
// default settings for smoothing efficiency histograms
//
TH2* doEffFit (TH2* hEff, TH2* hEvt, bool draw = false) {
  TH2* hEffFit = doSmoothEff(hEff,false);
  TH2* hXsec = (TH2*)hEvt->Clone("hXsec");
  hXsec->Divide(hEff);

  if ( draw ) {
    cout << "In draw" << endl;
    TH2* hEffFitDraw = (TH2*)hEffFit->Clone("hEffFitDraw");
    TH2* hEffRatio = (TH2*)hEff->Clone("hEffRatio");
    hEffRatio->Divide(hEffFitDraw);
    cout << "Histos " << hEff << " " << hEffFitDraw << " " << hEffRatio
   << " " << HEffErr << " " << HEffWidth << endl;
    TCanvas* c = new TCanvas();
    c->Divide(2,3);
    c->cd(1);
    hEff->Draw("zcol");
    c->cd(2);
    hEffFitDraw->Draw("zcol");
    c->cd(3);
    hEffRatio->Draw("zcol");
    if ( HEffErr ) {
      c->cd(5);
      HEffErr->Draw("zcol");
    }
    if ( HEffWidth ) {
      c->cd(6);
      HEffWidth->Draw("zcol");
    }
  }  
//   TH2* hXsecFilled = fillMissing(hXsec,5,14,true);
  TH2* hXsecFilled = fillMissing(hXsec,4,6,true);

  int nbx = hEff->GetNbinsX();
  int nby = hEff->GetNbinsY();
  for ( int ix=1; ix<=nbx; ++ix ) {
    for ( int iy=1; iy<=nby; ++iy ) {
      double vEff = hEffFit->GetBinContent(ix,iy);
      if ( vEff < 1.e-10 )  continue;
      double vXsec = hXsecFilled->GetBinContent(ix,iy);
      if ( vXsec > 1.e-10 )
  hEffFit->SetBinContent(ix,iy,vEff*vXsec);
      else
  hEffFit->SetBinContent(ix,iy,0.);
    }
  }

//   hEffFit->Draw("zcol");
// //   TH2* hFilledLoose = fillMissing(hRaw,4,6);

  return hEffFit;
}
//
// default settings for smoothing efficiency histograms
//
TH2* doEff (TH2* hRaw, bool ratio = true, bool draw = false) {
  return doSmooth(hRaw,"k3a",2,ratio,draw);
}
//
// default settings for smoothing JES signal systematics
//
TH2* doJES (TH2* histo, bool ratio = true, bool draw = false) {
  return doSmooth(histo,"",2,ratio,draw);
}
TH2* doJES (TFile* file, bool ratio = true, bool draw = false) {
  TH2* hRaw = findJesHisto(file);
  if ( hRaw == 0 )  return hRaw;
  return doJES (hRaw,ratio,draw);
}
//
// default settings for smoothing limits
//
TH2* doLimits (TFile* file, string name = "hObs", bool ratio = true, bool draw = false) {
  TH2* hRaw = findLimitHisto(file,name);
  if ( hRaw == 0 )  return hRaw;
  return doSmooth(hRaw,"",2,ratio,draw);
}

