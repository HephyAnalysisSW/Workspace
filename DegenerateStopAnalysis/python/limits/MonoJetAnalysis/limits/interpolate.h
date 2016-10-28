#include "TH2F.h"
#include <string>
#include <iostream>

// interpolate() implements a two step smearing. Its arguments are the histogram that should be interpolated
// and the direction in which to interpolate first (normally the direction in which the histogram changes 
// most slowly)
// Allowed types are SW (equivalently NE), SE (equivalently NW), NS, EW
// The second interpolation uses a "Swiss Cross" average (non-zero N, S, E, W neighbors)
TH2F* interpolate(const TH2F* hist, std::string firstInterpolationDirection);
// increases binning by factor of two and interpolates in specified direction
TH2F* rebin(TH2F* hist, std::string firstInterpolationDirection);

void getHistMaxMinBins(TH2F* h, int &xMin, int &xMax, int &yMin, int &yMax);
void omitEven(TH2F*h);
void omitOdd(TH2F*h);
bool alongDiagonal(TH2F* h, int iX, int iY);

TH2F* interpolate(const TH2F* hist, std::string firstInterpolationDirection) 
{
  TH2F *histCopy = (TH2F*)hist->Clone();

  int xStepPlus, xStepMinus, yStepPlus, yStepMinus;
  if(firstInterpolationDirection=="SW" || firstInterpolationDirection=="NE" || firstInterpolationDirection=="Santa Fe") {
    xStepPlus = 1;
    xStepMinus = -1;
    yStepPlus = 1;
    yStepMinus = -1;
  }
  else if(firstInterpolationDirection=="NW" || firstInterpolationDirection=="SE") {
    xStepPlus = -1;
    xStepMinus = 1;
    yStepPlus = 1;
    yStepMinus = -1;
  }
  else if(firstInterpolationDirection=="N" || firstInterpolationDirection=="S" || firstInterpolationDirection=="NS" || firstInterpolationDirection=="SN") {
    xStepPlus = 0;
    xStepMinus = 0;
    yStepPlus = 1;
    yStepMinus = -1;
  }
  else if(firstInterpolationDirection=="E" || firstInterpolationDirection=="W" || firstInterpolationDirection=="EW" || firstInterpolationDirection=="WE") {
    xStepPlus = 1;
    xStepMinus = -1;
    yStepPlus = 0;
    yStepMinus = 0;
  }
  else {
    // to avoid uninitialized variable warnings
    xStepPlus=xStepMinus=yStepPlus=yStepMinus=0;
    std::cout << firstInterpolationDirection << " is not an allowed smearing first interpolation direction.\n Allowed first interpolation directions are SW (equivalently NE), SE (equivalently NW), NS, EW" << std::endl;
    return 0;
  }

  // make temporary histograms to store the results of both steps
  TH2F *hist_step1 = (TH2F*)histCopy->Clone();
  hist_step1->Reset();
  TH2F *hist_step2 = (TH2F*)histCopy->Clone();
  hist_step2->Reset();

  int nBinsX = histCopy->GetNbinsX();
  int nBinsY = histCopy->GetNbinsY();

  int xMin, xMax, yMin, yMax;
  getHistMaxMinBins(histCopy, xMin, xMax, yMin, yMax);
   
   for(int i=1; i<=nBinsX; i++) {
     for(int j=1; j<=nBinsY; j++) {
       // do not extrapolate outside the scan
       if(i<xMin || i>xMax || j<yMin || j>yMax || alongDiagonal(histCopy, i,j)) continue; 
       double binContent = histCopy->GetBinContent(i, j);
       double binContentPlusStep = histCopy->GetBinContent(i+xStepPlus, j+yStepPlus);
       double binContentMinusStep = histCopy->GetBinContent(i+xStepMinus, j+yStepMinus);
       int nFilled = 0;
       if(binContentPlusStep>0) nFilled++;
       if(binContentMinusStep>0) nFilled++;
       // if we are at an empty bin and there are neighbors
       // in specified direction with non-zero entries
       if(binContent==0 && nFilled>0) {
   // average over non-zero entries
   binContent = (binContentPlusStep+binContentMinusStep)/nFilled;
   hist_step1->SetBinContent(i,j,binContent);
       }
     }
   }

   // add result of interpolation
   histCopy->Add(hist_step1);

   for(int i=1; i<=nBinsX; i++) {
     for(int j=1; j<=nBinsY; j++) {
       if(i<xMin || i>xMax || j<yMin || j>yMax || alongDiagonal(histCopy, i,j)) continue; 
       double binContent = histCopy->GetBinContent(i, j);
       // get entries for "Swiss Cross" average
       double binContentUp = histCopy->GetBinContent(i, j+1);
       double binContentDown = histCopy->GetBinContent(i, j-1);
       double binContentLeft = histCopy->GetBinContent(i-1, j);
       double binContentRight = histCopy->GetBinContent(i+1, j);
       int nFilled=0;
       if(binContentUp>0) nFilled++;
       if(binContentDown>0) nFilled++;
       if(binContentRight>0) nFilled++;
       if(binContentLeft>0) nFilled++;
       if(binContent==0 && nFilled>0) {
   // only average over non-zero entries
   binContent = (binContentUp+binContentDown+binContentRight+binContentLeft)/nFilled;
   hist_step2->SetBinContent(i,j,binContent);
       }
     }
   }
   // add "Swiss Cross" average
   histCopy->Add(hist_step2);

   return histCopy;
}

// find absolute boundaries of the scan
// in most inefficient way possible (inefficient => simpler => hopefully fewer typos)
void getHistMaxMinBins(TH2F* h, int &xMin, int &xMax, int &yMin, int &yMax)
{
  xMin=h->GetNbinsX(); // maximum possible minimum -- large dummy value
  yMin=h->GetNbinsY(); // large dummy value
  xMax=yMax=0;

  for(int iX=1; iX<=h->GetNbinsX(); iX++) {
    for(int iY=1; iY<=h->GetNbinsY(); iY++) {
      if(h->GetBinContent(iX, iY)>1e-10) {
        if(iX<xMin) xMin=iX;
  if(iY<yMin) yMin=iY;
        if(iX>xMax) xMax=iX;
  if(iY>yMax) yMax=iY;
      }
    }
  }
}

// Omit bins with even bin index.
// Use for test in which known values are omitted
// to determine bias from interpolation
void omitEven(TH2F* h)
{
  for(int i=0; i<=h->GetNbinsX(); i++) {
    for(int j=0; j<=h->GetNbinsY(); j++) {
      if(i%2==0 || j%2==0) h->SetBinContent(i, j, 0);
    }
  }
}

// Omit bins with odd bin index.
// Use for test in which known values are omitted
// to determine bias from interpolation
void omitOdd(TH2F* h)
{
  for(int i=0; i<=h->GetNbinsX(); i++) {
    for(int j=0; j<=h->GetNbinsY(); j++) {
      if((i+1)%2==0 || (j+1)%2==0) h->SetBinContent(i, j, 0);
    }
  }
}

// Tests if a bin is along a diagonal of the scan.
// Don't want to extrapolate past edge of scan in diagonal direction
bool alongDiagonal(TH2F* h, int iX, int iY)
{
  // calculate three most "northwestern" neigbors
  double sumNW = h->GetBinContent(iX, iY+1)+h->GetBinContent(iX-1, iY-1)+h->GetBinContent(iX-1, iY);
  // calculate three most "southeastern" neigbors
  double sumSE = h->GetBinContent(iX, iY-1)+h->GetBinContent(iX+1, iY-1)+h->GetBinContent(iX+1, iY);
  // etc.
  double sumSW = h->GetBinContent(iX, iY-1)+h->GetBinContent(iX-1, iY-1)+h->GetBinContent(iX-1, iY);
  double sumNE = h->GetBinContent(iX, iY+1)+h->GetBinContent(iX+1, iY+1)+h->GetBinContent(iX+1, iY);

  if((sumNW==0 && sumSE!=0) || (sumNW!=0 && sumSE==0) || 
     (sumSW==0 && sumNE!=0) || (sumSW!=0 && sumNE==0)
     ) return true;
  else return false;
}

TH2F* rebin(TH2F* hist, std::string firstInterpolationDirection)
{
  TString histName(hist->GetName());
  histName+="_rebin";

  // bin widths are needed so as to not shift histogram by half a bin with each rebinning
  // assume constant binning
  double binWidthX = hist->GetXaxis()->GetBinWidth(1);
  double binWidthY = hist->GetYaxis()->GetBinWidth(1);

  TH2F * histRebinned = new TH2F(histName, histName,
        2*hist->GetNbinsX(),
        hist->GetXaxis()->GetXmin()+binWidthX/4,
        hist->GetXaxis()->GetXmax()+binWidthX/4,
        2*hist->GetNbinsY(),
        hist->GetYaxis()->GetXmin()+binWidthY/4,
        hist->GetYaxis()->GetXmax()+binWidthY/4);

  // copy results from previous histogram
  for(int iX=0; iX<=hist->GetNbinsX(); iX++) {
    for(int iY=0; iY<=hist->GetNbinsY(); iY++) {
      double binContent = hist->GetBinContent(iX, iY);
      histRebinned->SetBinContent(2*iX-1, 2*iY-1, binContent);
    }
  }
  histRebinned->SetMaximum(hist->GetMaximum());
  histRebinned->SetMinimum(hist->GetMinimum());
  
  // use interpolation to re-fill histogram
  TH2F* histRebinnedInterpolated = interpolate(histRebinned, firstInterpolationDirection);
  
  return histRebinnedInterpolated;
}

