#include "TH2.h"
#include "TMatrixD.h"
#include "TVectorD.h"

#include <iostream>
//
// check for empty bins
//
//
// identify empty bins
//
inline bool isEmpty (double contents) {
  return contents<1.e-10;
}
inline bool isEmpty (TH2* h, int ix, int iy) {
  return isEmpty(h->GetBinContent(ix,iy));
}
//
// fill matrix and vector for quadratic fit
//
void fillForQuadFit (TH2* hOrig, TH2* refHisto, int ix, int iy, int jx, int jy,
		     int& nn, TMatrixD& mat, TVectorD& cvec) {
  // skip empty neighbours
  if ( isEmpty(refHisto,ix+jx,iy+jy) ) return;
  double z =  hOrig->GetBinContent(ix+jx,iy+jy);
  // update matrix and vector
  ++nn;
  mat(0,0) += jx*jx*jx*jx; mat(0,1) += jx*jx*jx*jy; mat(0,2) += jx*jx*jy*jy;
  mat(0,3) += jx*jx*jx;    mat(0,4) += jx*jx*jy;    mat(0,5) += jx*jx;
  mat(1,1) += jx*jx*jy*jy; mat(1,2) += jx*jy*jy*jy; mat(1,3) += jx*jx*jy;
  mat(1,4) += jx*jy*jy;    mat(1,5) += jx*jy;
  mat(2,2) += jy*jy*jy*jy; mat(2,3) += jx*jy*jy; mat(2,4) += jy*jy*jy;
  mat(2,5) += jy*jy;
  mat(3,3) += jx*jx; mat(3,4) += jx*jy; mat(3,5) += jx;
  mat(4,4) += jy*jy; mat(4,5) += jy;
  mat(5,5) += 1;
  cvec(0)  += jx*jx*z;  cvec(1)  += jx*jy*z;  cvec(2)  += jy*jy*z;
  cvec(3)  += jx*z;  cvec(4)  += jy*z;  cvec(5)  += z;
}
//
// fill missing bins in histogram h fitting a plane to the 
//   surrounding bins 
//
void fitQuadratic (TH2* h, TH2* refHisto, int nmin=9, int nmin2=12) {
  //
  // prepare histogram
  //
  TH2* hOrig = (TH2*)h->Clone();
  int nbx = hOrig->GetNbinsX();
  int nby = hOrig->GetNbinsY();
  //
  // matrix and vector for fit
  //
  TMatrixD mat(6,6);
  TVectorD cvec(6);
  //
  // loop over histogram 
  //
  for ( int ix=1; ix<=nbx; ++ix ) {
    for ( int iy=1; iy<=nby; ++iy ) {
      // clear matrix and vector used for fit
      int nn(0);
      for ( int i=0; i<6; ++i ) {
	cvec(i) = 0.;
	for ( int j=0; j<6; ++j ) mat(i,j) = 0.;
      }
      // loop over neighbours
      for ( int jx=-1; jx<2; ++jx ) {
	for ( int jy=-1; jy<2; ++jy ) {
	  if ( (ix+jx)<1 || (ix+jx)>nbx )  continue;
	  if ( (iy+jy)<1 || (iy+jy)>nby )  continue;
	  // fill vector and matrix
	  fillForQuadFit(hOrig,refHisto,ix,iy,jx,jy,nn,mat,cvec);
	}
      }
      for ( int jx=1; jx<6; ++jx ) {
	for ( int jy=0; jy<jx; ++jy )  mat(jx,jy) = mat(jy,jx);
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
	    // fill vector and matrix
	    fillForQuadFit(hOrig,refHisto,ix,iy,jx,jy,nn,mat,cvec);
	  }
	}
	for ( int jx=1; jx<6; ++jx ) {
	  for ( int jy=0; jy<jx; ++jy )  mat(jx,jy) = mat(jy,jx);
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
      if ( det < 1.e-6 )  std::cout << "************* " << det << std::endl;
      if ( det < 1.e-6 )  continue;
//       TMatrixD mat1(mat);
      mat.Invert(&det);
      TVectorD par = mat*cvec;
//       TVectorD tmp = mat1*par;
      h->SetBinContent(ix,iy,par(5));
    }
  }
  delete hOrig;
}
//
// fill matrix and vector for linear fit
//
void fillForLinFit (TH2* hOrig, TH2* refHisto, int ix, int iy, int jx, int jy,
		    int& nn, TMatrixD& mat, TVectorD& cvec) {
  // skip empty neighbours
  if ( isEmpty(refHisto,ix+jx,iy+jy) ) return;
  double z =  hOrig->GetBinContent(ix+jx,iy+jy);
  // update matrix and vector
  ++nn;
  mat(0,0) += jx*jx; mat(0,1) += jx*jy; mat(0,2) += jx;
  mat(1,0) += jx*jy; mat(1,1) += jy*jy; mat(1,2) += jy;
  mat(2,0) += jx;    mat(2,1) += jy;    mat(2,2) += 1;
  cvec(0)  += jx*z;  cvec(1)  += jy*z;  cvec(2)  += z;
}
//
// fill missing bins in histogram h fitting a plane to the 
//   surrounding bins 
//
void fitLinear (TH2* h, TH2* refHisto, int nmin=5, int nmin2=14) {
  //
  // prepare histogram
  //
  TH2* hOrig = (TH2*)h->Clone();
  int nbx = hOrig->GetNbinsX();
  int nby = hOrig->GetNbinsY();
  //
  // matrix and vector for fit
  //
  TMatrixD mat(3,3);
  TVectorD cvec(3);
  //
  // loop over histogram 
  //
  for ( int ix=1; ix<=nbx; ++ix ) {
    for ( int iy=1; iy<=nby; ++iy ) {
      // clear matrix and vector used for fit
      int nn(0);
      for ( int i=0; i<3; ++i ) {
	cvec(i) = 0.;
	for ( int j=0; j<3; ++j ) mat(i,j) = 0.;
      }
      // loop over neighbours
      for ( int jx=-1; jx<2; ++jx ) {
	for ( int jy=-1; jy<2; ++jy ) {
	  if ( (ix+jx)<1 || (ix+jx)>nbx )  continue;
	  if ( (iy+jy)<1 || (iy+jy)>nby )  continue;
	  // fill vector and matrix
	  fillForLinFit(hOrig,refHisto,ix,iy,jx,jy,nn,mat,cvec);
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
	    // fill vector and matrix
	    fillForLinFit(hOrig,refHisto,ix,iy,jx,jy,nn,mat,cvec);
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
      h->SetBinContent(ix,iy,par(2));
    }
  }
  delete hOrig;
}



TH2* doSmooth (TH2* hRaw, bool useLog = true) {
  //
  // smooth histogram 
  //
  TH2* hSmooth = (TH2*)hRaw->Clone("hSmooth");
  hSmooth->SetTitle("hSmooth");
  if ( useLog ) {
    for ( int ix=1; ix<=hSmooth->GetNbinsX(); ++ix ) {
      for ( int iy=1; iy<=hSmooth->GetNbinsY(); ++iy ) {
	double c = hSmooth->GetBinContent(ix,iy);
	c = c>0. ? log(c) : -100.;
	hSmooth->SetBinContent(ix,iy,c);
      }
    }
  }
  fitLinear(hSmooth,hRaw);

  if ( useLog ) {
    for ( int ix=1; ix<=hSmooth->GetNbinsX(); ++ix ) {
      for ( int iy=1; iy<=hSmooth->GetNbinsY(); ++iy ) {
	double craw = hRaw->GetBinContent(ix,iy);
	double c = hSmooth->GetBinContent(ix,iy);
 	c = craw>0. ? exp(c) : 0.;
 	hSmooth->SetBinContent(ix,iy,c);
      }
    }
  }
  hSmooth->SetName(hRaw->GetName());

  return hSmooth;
}
