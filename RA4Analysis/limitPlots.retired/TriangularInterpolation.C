#include "TFile.h"
#include "TKey.h"
#include "TCanvas.h"
#include "TH2.h"
#include "TAxis.h"
#include <algorithm>
#include <vector>
#include <iostream>

using namespace std;

TH2* findHisto (TFile* file)
{
  TH2* result(0);

  TObject* obj;
  TKey* key;
  TCanvas* canvas(0);
  TIter iKey(file->GetListOfKeys());
  while ( (key=(TKey*)iKey.Next()) ) {
    obj = key->ReadObj();
    if ( obj->InheritsFrom(TCanvas::Class()) ) {
      if ( canvas ) {
	cout << "More than one Canvas in file" << endl;
	return result;
      }
      else {
	canvas = (TCanvas*)obj;
      }
    }
  }
  if ( canvas == 0 ) {
    cout << "No Canvas in file" << endl;
    return result;
  }

  TIter iCnv(canvas->GetListOfPrimitives());
  while ( (obj=iCnv.Next()) ) {
    if ( obj->InheritsFrom(TH2::Class()) ) {
      if ( result ) {
	cout << "More than one histogram in Canvas" << endl;
	return (TH2*)0;
      }
      else {
	result = (TH2*)obj;
	cout << "Found histograms " << result->GetName() << endl;
      }
    }
  }
  return result;
}

struct Triplet {
  Triplet () : first(0.), second(0.), third(0.) {}
  Triplet (double x, double y, double z) : first(x), second(y), third(z) {}
  double first;
  double second;
  double third;
};

// struct SmallerDistance {
//   SmallerDistance (int ix, int iy) : ix_(ix), iy_(iy) {}
//   bool operator() (const pair<int,int>& p1, const pair<int,int>& p2) {
//     int drSq1 = (p1.first-ix_)*(p1.first-ix_) + (p1.second-iy_)*(p1.second-iy_);
//     int drSq2 = (p2.first-ix_)*(p2.first-ix_) + (p2.second-iy_)*(p2.second-iy_);
//     return drSq1<drSq2;
//   }
//   int ix_;
//   int iy_;
// };
struct SmallerDistance {
  SmallerDistance (double x, double y) : x_(x), y_(y) {}
  bool operator() (const Triplet& p1, const Triplet& p2) {
//     double drSq1 = (p1.first-x_)*(p1.first-x_) + (p1.second-y_)*(p1.second-y_);
//     double drSq2 = (p2.first-x_)*(p2.first-x_) + (p2.second-y_)*(p2.second-y_);
    return distSquare(p1)<distSquare(p2);
  }
  inline double distSquare (const Triplet& p) const {
    return (p.first-x_)*(p.first-x_) + (p.second-y_)*(p.second-y_);
  }
  double x_;
  double y_;
};

inline double sideOfLine (double x, double y, const Triplet& a, const Triplet& b) 
{
  return (x-a.first)*(b.second-a.second)-(y-a.second)*(b.first-a.first);
}

bool insideTriangle (double x, double y, const Triplet& a, const Triplet& b, const Triplet& c)
{
  double d1 = sideOfLine(x,y,a,b);
  double d2 = sideOfLine(x,y,b,c);
  double d3 = sideOfLine(x,y,c,a);
  return ( d1<0. && d2<0. && d3<0. ) || ( d1>0. && d2>0. && d3>0. );
}

double solve (double x, double y, const vector<Triplet>& nonZeroBins)
{
  if ( nonZeroBins.empty() )  return -1.;

  vector<Triplet> closest(nonZeroBins);
  sort(closest.begin(),closest.end(),SmallerDistance(x,y));
  if ( closest.size()<3 )  return closest[0].third;

  vector<double> xs;
  vector<double> ys;
  vector<double> zs;

  SmallerDistance dist(x,y);
//   cout << "Closest dist = " << dist.distSquare(closest[0]) << " "
//        << closest[0].first << " " << closest[0].second << " "
//        << closest[0].third << endl;
  if ( dist.distSquare(closest[0])<0.01 )  return closest[0].third;

  bool done(false);
  for ( size_t ia=0; ia<closest.size(); ++ia ) {
    Triplet pa(closest[ia]);
    for ( size_t ib=ia+1; ib<closest.size(); ++ib ) {
      Triplet pb(closest[ib]);
      for ( size_t ic=ib+1; ic<closest.size(); ++ic ) {
	Triplet pc(closest[ic]);
	if ( insideTriangle(x,y,pa,pb,pc) ) {
	  xs.push_back(pa.first);
	  ys.push_back(pa.second);
	  zs.push_back(log(pa.third));
	  xs.push_back(pb.first);
	  ys.push_back(pb.second);
	  zs.push_back(log(pb.third));
	  xs.push_back(pc.first);
	  ys.push_back(pc.second);
	  zs.push_back(log(pc.third));
	  done = true;
	  break;
	}
      }
      if ( done )  break;
    }
    if ( done )  break;
  }
//   if ( !done )  cout << "Not done " << x << " " << y << " " 
// 		     << closest[0].first << " " << closest[0].second << " " 
// 		     << closest[0].third << endl;
  if ( !done )  return closest[0].third;

  double dx1 = xs[1] - xs[0];
  double dx2 = xs[2] - xs[1];
  double dy1 = ys[1] - ys[0];
  double dy2 = ys[2] - ys[1];
  double dz1 = zs[1] - zs[0];
  double dz2 = zs[2] - zs[1];
  double denom = dx2*dy1 - dx1*dy2;

  double a = (dy1*dz2-dy2*dz1)/denom;
  double b = (dx2*dz1-dx1*dz2)/denom;
  double c = zs[0] - a*xs[0] - b*ys[0];
//   if (  exp(a*x+b*y+c)>10 ) {
//     cout << "Found points for " << x << " " << y << " : " << endl;
//     cout << "   " << xs[0] << " " << ys[0] << " " << zs[0] << endl;
//     cout << "   " << xs[1] << " " << ys[1] << " " << zs[1] << endl;
//     cout << "   " << xs[2] << " " << ys[2] << " " << zs[2] << endl;
//     cout << dx1 << " " << dy1 << " " << dz1 << endl;
//     cout << dx2 << " " << dy2 << " " << dz2 << endl;
//     cout << denom << endl;
//     cout << "result = " << a*x+b*y+c << endl;
//     cout << "result = " << exp(a*x+b*y+c) << endl;
//   }
//   cout << a*xs[0]+b*ys[0]+c << " / " << zs[0] << endl;
//   cout << a*xs[1]+b*ys[1]+c << " / " << zs[1] << endl;
//   cout << a*xs[2]+b*ys[2]+c << " / " << zs[2] << endl;
  return exp(a*x+b*y+c);
}

TH2* triangular (TH2* histo, const TH2* refHisto)
{
  vector<Triplet> nonZeroBins;
  TAxis* xaxis = refHisto->GetXaxis();
  TAxis* yaxis = refHisto->GetYaxis();
  for ( int ix=1; ix<=refHisto->GetNbinsX(); ++ix ) {
    for ( int iy=1; iy<=refHisto->GetNbinsY(); ++iy ) {
      if ( refHisto->GetBinContent(ix,iy)>1.e-10 ) {
	Triplet triplet(xaxis->GetBinCenter(ix),yaxis->GetBinCenter(iy),refHisto->GetBinContent(ix,iy));
	nonZeroBins.push_back(triplet);
      }
    }
  }

  int nbx = histo->GetNbinsX();
  int nby = histo->GetNbinsY();
  xaxis = histo->GetXaxis();
  yaxis = histo->GetYaxis();
  for ( int ix=1; ix<=nbx; ++ix ) {
    double x = xaxis->GetBinCenter(ix);
    for ( int iy=1; iy<=nby; ++iy ) {
      if ( histo->GetBinContent(ix,iy)<1.e-10 )  continue;
      double y = yaxis->GetBinCenter(iy);
//       for ( size_t i=0; i<min(closestBins.size(),size_t(5)); ++i ) {
// 	cout << i << " " << closestBins[i].first << " " << closestBins[i].second << " / "
// 	     << ix << " " << iy << endl;
//       }
      double res = solve(x,y,nonZeroBins);
      histo->SetBinContent(ix,iy,res);
    }
  }

  return histo;
}

TH2* triangular (TH2* histo, TFile* file)
{
  TH2* hIn = findHisto(file);
  if ( hIn == 0 )  return 0;
  return triangular(histo,hIn);
}

