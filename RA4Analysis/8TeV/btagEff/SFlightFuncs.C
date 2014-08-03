#include "TF1.h"
#include "TLegend.h"
#include <TCanvas.h>

//------------ Exemple of usage --------------
//
// In a root session:
// 	.L SFlightFuncs.C+g	//To load this program
// Then...
// To get a pointer to the SFlight function for CSV tagger Loose (L) in the eta range 0.0-0.5 use: 
//	TF1* SFlight = GetSFlmean("CSV","L",0.0, 0.5)
// To get a pointer to the SFlightmin function for CSV tagger Loose (L) in the eta range 0.0-0.5 use: 
//	TF1* SFlightmin = GetSFlmin("CSV","L",0.0, 0.5)
// To get a pointer to the SFlightmax function for CSV tagger Loose (L) in the eta range 0.0-0.5 use: 
//	TF1* SFlightmax = GetSFlmax("CSV","L",0.0, 0.5)
//
// Note:
// 1) SFlightmin and SFlightmax correspond to SFlight +- (stat+syst error).
// 2) If the specified combination of tagger/taggerstrength/etarange is not tabulated,
//    a NULL pointer is returned.
//
//-------------------------------------------
TF1* GetSFLight(TString meanminmax, TString tagger, TString TaggerStrength, Float_t Etamin, Float_t Etamax);

TF1* GetSFlmean(TString tagger, TString TaggerStrength, float Etamin, float Etamax)
{
  return GetSFLight("mean",tagger,TaggerStrength,Etamin,Etamax);
}
TF1* GetSFlmin(TString tagger, TString TaggerStrength, float Etamin, float Etamax)
{
  return GetSFLight("min",tagger,TaggerStrength,Etamin,Etamax);
}
TF1* GetSFlmax(TString tagger, TString TaggerStrength, float Etamin, float Etamax)
{
  return GetSFLight("max",tagger,TaggerStrength,Etamin,Etamax);
}

TF1* plotmean(TString tagger, TString TaggerStrength, float Etamin, float Etamax, TString opt = "" , int col = 1, float lineWidth = 1, int lineStyle = 1)
{
  TF1* f = GetSFlmean(tagger,TaggerStrength,Etamin,Etamax);
  if( f != NULL )
  {
    f->SetLineColor(col);
    f->SetMinimum(0.4);
    f->SetMaximum(1.6);
    f->SetLineWidth(lineWidth);
    f->SetLineStyle(lineStyle);
    f->Draw(opt);
  }
  //else cout << "NULL pointer returned... Function seems not to exist" << endl;
  return f;
}
TF1* plotmin(TString tagger, TString TaggerStrength, float Etamin, float Etamax, TString opt = "" , int col = 1, float lineWidth = 1, int lineStyle = 1)
{
  TF1* f = GetSFlmin(tagger,TaggerStrength,Etamin,Etamax);
  if( f != NULL )
  {
    f->SetLineColor(col);
    f->SetLineWidth(lineWidth);
    f->SetLineStyle(lineStyle);
    f->Draw(opt);
  }
  //else cout << "NULL pointer returned... Function seems not to exist" << endl;
  return f;
}
TF1* plotmax(TString tagger, TString TaggerStrength, float Etamin, float Etamax, TString opt = "" , int col = 1, float lineWidth = 1, int lineStyle = 1)
{
  TF1* f = GetSFlmax(tagger,TaggerStrength,Etamin,Etamax);
  if( f != NULL )
  {
    f->SetLineColor(col);
    f->SetLineWidth(lineWidth);
    f->SetLineStyle(lineStyle);
    f->Draw(opt);
  }
  //else cout << "NULL pointer returned... Function seems not to exist" << endl;
  return f;
}
void plotmean(TCanvas *yourC, int yourzone, TString tagger, TString TaggerStrength)
{
 TString legTitle = tagger + TaggerStrength;
 //TCanvas *cWork = new TCanvas("cWork", "plots",200,10,700,750);
 yourC->SetFillColor(10);
 yourC->SetFillStyle(4000);
 yourC->SetBorderSize(2);

 yourC->cd(yourzone);
 yourC->cd(yourzone)->SetFillColor(10);
 yourC->cd(yourzone)->SetFillStyle(4000);
 yourC->cd(yourzone)->SetBorderSize(2);
  TF1 *fmean, *fmin, *fmax;
  TF1* f[10];
  TLegend* leg= new TLegend(0.60,0.56,0.89,0.89);
    leg->SetBorderSize(0);
    leg->SetFillColor(kWhite);
    leg->SetTextFont(42);
    leg->SetHeader(legTitle);
  float etamin[10], etamax[10]; 
  int N=1;
  etamin[0] = 0.0; etamax[0] = 2.4;

  if( TaggerStrength == "L" )
  {
    N = 4;
    etamin[1] = 0.0; etamax[1] = 0.5;
    etamin[2] = 0.5; etamax[2] = 1.0;
    etamin[3] = 1.0; etamax[3] = 1.5;
    etamin[4] = 1.5; etamax[4] = 2.4;
  }
  else if( TaggerStrength == "M" )
  {
    N = 3;
    etamin[1] = 0.0; etamax[1] = 0.8;
    etamin[2] = 0.8; etamax[2] = 1.6;
    etamin[3] = 1.6; etamax[3] = 2.4;
  }
  else if( TaggerStrength == "T" )
  {
    N = 1;
    etamin[1] = 0.0; etamax[1] = 2.4;
  }

  //etamin = 0.0; etamax = 2.4;
/*
  fmean = plotmean(tagger,TaggerStrength,etamin[0], etamax[0], "", 1, 2, 1);
  leg->AddEntry(fmean,"Mean(SF)","l");
  fmin = plotmin(tagger,TaggerStrength,etamin[0], etamax[0], "same", 1, 2, 2);
  leg->AddEntry(fmin,"Min(SF)","l");
  fmax = plotmax(tagger,TaggerStrength,etamin[0], etamax[0], "same", 1, 2, 2);
  leg->AddEntry(fmax,"Max(SF)","l");
*/

    f[1] = plotmean(tagger,TaggerStrength,etamin[1], etamax[1], "", 1, 1);
    //TString rangeEta = Form("Mean(SF(%1.1f #leq #eta %1.1f))",etamin[1],etamax[1]);
    TString rangeEta = Form("SF(%1.1f #leq #eta %1.1f)",etamin[1],etamax[1]);
    leg->AddEntry(f[1],rangeEta,"l");
  for( int i = 2; i <= N; ++i )
  {
    f[i] = plotmean(tagger,TaggerStrength,etamin[i], etamax[i], "same", i, 1);
    //TString rangeEta = Form("Mean(SF(%1.1f #leq #eta %1.1f))",etamin[i],etamax[i]);
    TString rangeEta = Form("SF(%1.1f #leq #eta %1.1f)",etamin[i],etamax[i]);
    leg->AddEntry(f[i],rangeEta,"l");
  }
  //leg->AddEntry(gg," gluon jets","P");
  leg->Draw();
  //return cWork;
}
TCanvas *plotmean(TString tagger, TString TaggerStrength)
{
 TCanvas *cWork = new TCanvas("cWork", "plots",200,10,700,750);
 plotmean(cWork, 0, tagger, TaggerStrength);

 return cWork;
}
TCanvas *plotmean(TString selecter)
{
 TCanvas *cWork = NULL; 
 if( selecter == "L" )
 {
   cWork = new TCanvas("cWork", "plots",200,10,700,500);
   cWork->Divide(2,2);
   plotmean(cWork, 1, "JP", selecter);
   plotmean(cWork, 2, "JBP", selecter);
   plotmean(cWork, 3, "CSV", selecter);
   plotmean(cWork, 4, "TCHE", selecter);
 }
 else if( selecter == "M" )
 {
   cWork = new TCanvas("cWork", "plots",200,10,700,750);
   cWork->Divide(2,3);
   plotmean(cWork, 1, "JP", selecter);
   plotmean(cWork, 2, "JBP", selecter);
   plotmean(cWork, 3, "CSV", selecter);
   plotmean(cWork, 4, "TCHE", selecter);
   plotmean(cWork, 5, "TCHP", selecter);
   plotmean(cWork, 6, "SSVHE", selecter);
 }
 else if( selecter == "T" )
 {
   cWork = new TCanvas("cWork", "plots",200,10,700,750);
   cWork->Divide(2,3);
   plotmean(cWork, 1, "JP", selecter);
   plotmean(cWork, 2, "JBP", selecter);
   plotmean(cWork, 3, "CSV", selecter);
   //plotmean(cWork, 4, "TCHE", selecter);
   plotmean(cWork, 5, "TCHP", selecter);
   plotmean(cWork, 6, "SSVHP", selecter);
 }
 else if( selecter == "TCHE" )
 {
   cWork = new TCanvas("cWork", "plots",200,10,700,500);
   cWork->Divide(1,2);
   plotmean(cWork, 1, selecter, "L");
   plotmean(cWork, 2, selecter, "M");
 }
 else if( selecter == "TCHP" )
 {
   cWork = new TCanvas("cWork", "plots",200,10,700,500);
   cWork->Divide(1,2);
   plotmean(cWork, 1, selecter, "M");
   plotmean(cWork, 2, selecter, "T");
 }
 else if( selecter == "SSVHE" )
 {
   cWork = new TCanvas("cWork", "plots",200,10,700,250);
   plotmean(cWork, 0, selecter, "M");
 }
 else if( selecter == "SSVHP" )
 {
   cWork = new TCanvas("cWork", "plots",200,10,700,250);
   plotmean(cWork, 0, selecter, "T");
 }
 else
 {
   cWork = new TCanvas("cWork", "plots",200,10,700,750);
   cWork->Divide(1,3);
   plotmean(cWork, 1, selecter, "L");
   plotmean(cWork, 2, selecter, "M");
   plotmean(cWork, 3, selecter, "T");
 }

 cWork->WaitPrimitive();
 cWork->SaveAs("SFlightFunc_"+selecter+".pdf");
 return cWork;
}
TCanvas *plotmean()
{
 TCanvas *cWork = new TCanvas("cWork", "plots",200,10,700,750);
 cWork->Divide(3,6, 0.002, 0.002);
 cWork->SetFillColor(10);
 cWork->SetFillStyle(4000);
 cWork->SetBorderSize(1);
 for( int i = 0; i < 3*6; ++i )
 {
   cWork->cd(i+1)->SetFillColor(10);
   cWork->cd(i+1)->SetFillStyle(4000);
   cWork->cd(i+1)->SetBorderSize(1);
 }
   plotmean(cWork, 1, "JP", "L");
   plotmean(cWork, 2, "JP", "M");
   plotmean(cWork, 3, "JP", "T");
   plotmean(cWork, 4, "JBP", "L");
   plotmean(cWork, 5, "JBP", "M");
   plotmean(cWork, 6, "JBP", "T");
   plotmean(cWork, 7, "CSV", "L");
   plotmean(cWork, 8, "CSV", "M");
   plotmean(cWork, 9, "CSV", "T");
   plotmean(cWork, 10, "TCHE", "L");
   plotmean(cWork, 11, "TCHE", "M");
   plotmean(cWork, 14, "TCHP", "M");
   plotmean(cWork, 15, "TCHP", "T");
   plotmean(cWork, 17, "SSVHE", "M");
   plotmean(cWork, 18, "SSVHP", "T");

 return cWork;
}
/*
TCanvas *plotmean(TString tagger, TString TaggerStrength)
{
 TString legTitle = tagger + TaggerStrength;
 TCanvas *cWork = new TCanvas("cWork", "plots",200,10,700,750);
 cWork->SetFillColor(10);
 cWork->SetFillStyle(4000);
 cWork->SetBorderSize(2);
  TF1 *fmean, *fmin, *fmax;
  TF1* f[10];
  TLegend* leg= new TLegend(0.66,0.54,0.96,0.94);
    leg->SetBorderSize(0);
    leg->SetFillColor(kWhite);
    leg->SetTextFont(42);
    leg->SetHeader(legTitle);
  float etamin[10], etamax[10]; 
  int N=1;
  etamin[0] = 0.0; etamax[0] = 2.4;

  if( TaggerStrength == "L" )
  {
    N = 5;
    etamin[1] = 0.0; etamax[1] = 0.5;
    etamin[2] = 0.5; etamax[2] = 1.0;
    etamin[3] = 1.0; etamax[3] = 1.5;
    etamin[4] = 1.5; etamax[4] = 2.4;
  }
  else if( TaggerStrength == "M" )
  {
    N = 4;
    etamin[1] = 0.0; etamax[1] = 0.8;
    etamin[2] = 0.8; etamax[2] = 1.6;
    etamin[3] = 1.6; etamax[3] = 2.4;
  }
  else if( TaggerStrength == "M" )
  {
    N = 1;
  }

  //etamin = 0.0; etamax = 2.4;
  fmean = plotmean(tagger,TaggerStrength,etamin[0], etamax[0], "", 1, 3, 1);
  leg->AddEntry(fmean,"Mean(SF)","l");
  fmin = plotmin(tagger,TaggerStrength,etamin[0], etamax[0], "same", 1, 3, 2);
  leg->AddEntry(fmin,"Min(SF)","l");
  fmax = plotmax(tagger,TaggerStrength,etamin[0], etamax[0], "same", 1, 3, 2);
  leg->AddEntry(fmax,"Max(SF)","l");
  for( int i = 1; i < N; ++i )
  {
    f[i] = plotmean(tagger,TaggerStrength,etamin[i], etamax[i], "same", i+1, 2);
    TString rangeEta = Form("Mean(SF(%1.1f #leq #eta %1.1f))",etamin[i],etamax[i]);
    leg->AddEntry(f[i],rangeEta,"l");
  }
  //leg->AddEntry(gg," gluon jets","P");
  leg->Draw();
  return cWork;
}
*/


TF1* GetSFLight(TString meanminmax, TString tagger, TString TaggerStrength, Float_t Etamin, Float_t Etamax)
{
  TF1 *tmpSFl = NULL;
  TString Atagger = tagger+TaggerStrength;
  TString sEtamin = Form("%1.1f",Etamin);
  TString sEtamax = Form("%1.1f",Etamax);
  cout << sEtamin << endl;
  cout << sEtamax << endl;

// Definition of functions from plot33New.C ----------------------

if( Atagger == "CSVL" && sEtamin == "0.0" && sEtamax == "0.5")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.07536+(0.000175506*x))+(-8.63317e-07*(x*x)))+(3.27516e-10*(x*(x*x)))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.994425+(-8.66392e-05*x))+(-3.03813e-08*(x*x)))+(-3.52151e-10*(x*(x*x)))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.15628+(0.000437668*x))+(-1.69625e-06*(x*x)))+(1.00718e-09*(x*(x*x)))", 20.,670.);
}
if( Atagger == "CSVL" && sEtamin == "0.0" && sEtamax == "2.4")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.0344+(0.000962994*x))+(-3.65392e-06*(x*x)))+(3.23525e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.956023+(0.000825106*x))+(-3.18828e-06*(x*x)))+(2.81787e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.11272+(0.00110104*x))+(-4.11956e-06*(x*x)))+(3.65263e-09*(x*(x*x)))", 20.,670.);
}
if( Atagger == "CSVL" && sEtamin == "0.5" && sEtamax == "1.0")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.07846+(0.00032458*x))+(-1.30258e-06*(x*x)))+(8.50608e-10*(x*(x*x)))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.998088+(6.94916e-05*x))+(-4.82731e-07*(x*x)))+(1.63506e-10*(x*(x*x)))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.15882+(0.000579711*x))+(-2.12243e-06*(x*x)))+(1.53771e-09*(x*(x*x)))", 20.,670.);
}
if( Atagger == "CSVL" && sEtamin == "1.0" && sEtamax == "1.5")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.08294+(0.000474818*x))+(-1.43857e-06*(x*x)))+(1.13308e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((1.00294+(0.000289844*x))+(-7.9845e-07*(x*x)))+(5.38525e-10*(x*(x*x)))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.16292+(0.000659848*x))+(-2.07868e-06*(x*x)))+(1.72763e-09*(x*(x*x)))", 20.,670.);
}
if( Atagger == "CSVL" && sEtamin == "1.5" && sEtamax == "2.4")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.0617+(0.000173654*x))+(-5.29009e-07*(x*x)))+(5.55931e-10*(x*(x*x)))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.979816+(0.000138797*x))+(-3.14503e-07*(x*x)))+(2.38124e-10*(x*(x*x)))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.14357+(0.00020854*x))+(-7.43519e-07*(x*x)))+(8.73742e-10*(x*(x*x)))", 20.,670.);
}
if( Atagger == "CSVM" && sEtamin == "0.0" && sEtamax == "0.8")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.06182+(0.000617034*x))+(-1.5732e-06*(x*x)))+(3.02909e-10*(x*(x*x)))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.972455+(7.51396e-06*x))+(4.91857e-07*(x*x)))+(-1.47661e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.15116+(0.00122657*x))+(-3.63826e-06*(x*x)))+(2.08242e-09*(x*(x*x)))", 20.,670.);
}
if( Atagger == "CSVM" && sEtamin == "0.0" && sEtamax == "2.4")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.04318+(0.000848162*x))+(-2.5795e-06*(x*x)))+(1.64156e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.962627+(0.000448344*x))+(-1.25579e-06*(x*x)))+(4.82283e-10*(x*(x*x)))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.12368+(0.00124806*x))+(-3.9032e-06*(x*x)))+(2.80083e-09*(x*(x*x)))", 20.,670.);
}
if( Atagger == "CSVM" && sEtamin == "0.8" && sEtamax == "1.6")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.111+(-9.64191e-06*x))+(1.80811e-07*(x*x)))+(-5.44868e-10*(x*(x*x)))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((1.02055+(-0.000378856*x))+(1.49029e-06*(x*x)))+(-1.74966e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.20146+(0.000359543*x))+(-1.12866e-06*(x*x)))+(6.59918e-10*(x*(x*x)))", 20.,670.);
}
if( Atagger == "CSVM" && sEtamin == "1.6" && sEtamax == "2.4")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.08498+(-0.000701422*x))+(3.43612e-06*(x*x)))+(-4.11794e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.983476+(-0.000607242*x))+(3.17997e-06*(x*x)))+(-4.01242e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.18654+(-0.000795808*x))+(3.69226e-06*(x*x)))+(-4.22347e-09*(x*(x*x)))", 20.,670.);
}
if( Atagger == "CSVT" && sEtamin == "0.0" && sEtamax == "2.4")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((0.948463+(0.00288102*x))+(-7.98091e-06*(x*x)))+(5.50157e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.899715+(0.00102278*x))+(-2.46335e-06*(x*x)))+(9.71143e-10*(x*(x*x)))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((0.997077+(0.00473953*x))+(-1.34985e-05*(x*x)))+(1.0032e-08*(x*(x*x)))", 20.,670.);
}
if( Atagger == "JBPL" && sEtamin == "0.0" && sEtamax == "0.5")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((0.996303+(-0.00049586*x))+(1.48662e-06*(x*x)))+(-1.60955e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.909313+(-0.000483037*x))+(1.48507e-06*(x*x)))+(-1.60327e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.08332+(-0.000508763*x))+(1.48816e-06*(x*x)))+(-1.61583e-09*(x*(x*x)))", 20.,670.);
}
if( Atagger == "JBPL" && sEtamin == "0.0" && sEtamax == "2.4")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((0.974968+(-0.000192541*x))+(7.08162e-07*(x*x)))+(-9.7623e-10*(x*(x*x)))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.891217+(-0.000201377*x))+(7.41513e-07*(x*x)))+(-9.86349e-10*(x*(x*x)))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.05873+(-0.000183755*x))+(6.74811e-07*(x*x)))+(-9.6611e-10*(x*(x*x)))", 20.,670.);
}
if( Atagger == "JBPL" && sEtamin == "0.5" && sEtamax == "1.0")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.01607+(-0.000958122*x))+(3.12318e-06*(x*x)))+(-3.13777e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.925793+(-0.000877501*x))+(2.88538e-06*(x*x)))+(-2.9089e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.10639+(-0.0010389*x))+(3.36098e-06*(x*x)))+(-3.36665e-09*(x*(x*x)))", 20.,670.);
}
if( Atagger == "JBPL" && sEtamin == "1.0" && sEtamax == "1.5")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.04234+(-0.00109152*x))+(3.71686e-06*(x*x)))+(-3.57219e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.947786+(-0.000985917*x))+(3.39659e-06*(x*x)))+(-3.28635e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.13696+(-0.00119731*x))+(4.03713e-06*(x*x)))+(-3.85803e-09*(x*(x*x)))", 20.,670.);
}
if( Atagger == "JBPL" && sEtamin == "1.5" && sEtamax == "2.4")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((0.960685+(-0.000514241*x))+(2.69297e-06*(x*x)))+(-3.12123e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.875356+(-0.000455763*x))+(2.42337e-06*(x*x)))+(-2.83637e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.04606+(-0.000572874*x))+(2.96257e-06*(x*x)))+(-3.40609e-09*(x*(x*x)))", 20.,670.);
}
if( Atagger == "JBPM" && sEtamin == "0.0" && sEtamax == "0.8")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((0.932447+(0.000285676*x))+(-1.03771e-06*(x*x)))+(4.52275e-10*(x*(x*x)))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.822274+(0.000138316*x))+(-4.14616e-07*(x*x)))+(-9.7638e-11*(x*(x*x)))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.0426+(0.000433059*x))+(-1.6608e-06*(x*x)))+(1.00219e-09*(x*(x*x)))", 20.,670.);
}
if( Atagger == "JBPM" && sEtamin == "0.0" && sEtamax == "2.4")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((0.859232+(0.00117533*x))+(-3.51857e-06*(x*x)))+(2.63162e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.769143+(0.000865281*x))+(-2.47018e-06*(x*x)))+(1.72476e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((0.949262+(0.00148551*x))+(-4.56695e-06*(x*x)))+(3.53847e-09*(x*(x*x)))", 20.,670.);
}
if( Atagger == "JBPM" && sEtamin == "0.8" && sEtamax == "1.6")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((0.924959+(0.000170347*x))+(-1.56056e-07*(x*x)))+(-2.06751e-10*(x*(x*x)))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.822394+(-2.61379e-05*x))+(6.08356e-07*(x*x)))+(-9.28476e-10*(x*(x*x)))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.02752+(0.000366822*x))+(-9.20467e-07*(x*x)))+(5.14974e-10*(x*(x*x)))", 20.,670.);
}
if( Atagger == "JBPM" && sEtamin == "1.6" && sEtamax == "2.4")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((0.846053+(0.000224848*x))+(2.87503e-07*(x*x)))+(-5.93182e-10*(x*(x*x)))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.714511+(0.000568422*x))+(-7.56289e-07*(x*x)))+(2.61634e-10*(x*(x*x)))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((0.977599+(-0.000118755*x))+(1.3313e-06*(x*x)))+(-1.448e-09*(x*(x*x)))", 20.,670.);
}
if( Atagger == "JBPT" && sEtamin == "0.0" && sEtamax == "2.4")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((0.771257+(0.00238891*x))+(-6.2112e-06*(x*x)))+(4.33595e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.666101+(0.00163462*x))+(-3.92728e-06*(x*x)))+(2.48081e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((0.87631+(0.00314343*x))+(-8.49513e-06*(x*x)))+(6.19109e-09*(x*(x*x)))", 20.,670.);
}
if( Atagger == "JPL" && sEtamin == "0.0" && sEtamax == "0.5")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.02571+(-0.000391686*x))+(1.01948e-06*(x*x)))+(-1.16475e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.931859+(-0.00045457*x))+(1.25431e-06*(x*x)))+(-1.36433e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.11958+(-0.00032886*x))+(7.84649e-07*(x*x)))+(-9.65161e-10*(x*(x*x)))", 20.,670.);
}
if( Atagger == "JPL" && sEtamin == "0.0" && sEtamax == "2.4")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((0.978061+(0.000211142*x))+(-6.67003e-07*(x*x)))+(2.94232e-10*(x*(x*x)))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.889182+(0.000124259*x))+(-3.83838e-07*(x*x)))+(5.99164e-11*(x*(x*x)))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.06693+(0.00029804*x))+(-9.50169e-07*(x*x)))+(5.28547e-10*(x*(x*x)))", 20.,670.);
}
if( Atagger == "JPL" && sEtamin == "0.5" && sEtamax == "1.0")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.03375+(-0.00068776*x))+(2.13443e-06*(x*x)))+(-2.24163e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.936905+(-0.000681017*x))+(2.13885e-06*(x*x)))+(-2.22607e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.13063+(-0.000694616*x))+(2.13001e-06*(x*x)))+(-2.25719e-09*(x*(x*x)))", 20.,670.);
}
if( Atagger == "JPL" && sEtamin == "1.0" && sEtamax == "1.5")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.03597+(-0.000778058*x))+(3.02129e-06*(x*x)))+(-3.0478e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.938438+(-0.00074623*x))+(2.89732e-06*(x*x)))+(-2.92483e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.13355+(-0.000810039*x))+(3.14525e-06*(x*x)))+(-3.17077e-09*(x*(x*x)))", 20.,670.);
}
if( Atagger == "JPL" && sEtamin == "1.5" && sEtamax == "2.4")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((0.95897+(-0.000111286*x))+(1.6091e-06*(x*x)))+(-2.18387e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.867768+(-9.92078e-05*x))+(1.46903e-06*(x*x)))+(-2.02118e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.0502+(-0.000123474*x))+(1.74917e-06*(x*x)))+(-2.34655e-09*(x*(x*x)))", 20.,670.);
}
if( Atagger == "JPM" && sEtamin == "0.0" && sEtamax == "0.8")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((0.970028+(0.00118179*x))+(-4.23119e-06*(x*x)))+(3.61065e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.840326+(0.000626372*x))+(-2.08293e-06*(x*x)))+(1.57604e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.09966+(0.00173739*x))+(-6.37946e-06*(x*x)))+(5.64527e-09*(x*(x*x)))", 20.,670.);
}
if( Atagger == "JPM" && sEtamin == "0.0" && sEtamax == "2.4")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((0.871294+(0.00215201*x))+(-6.77675e-06*(x*x)))+(5.79197e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.7654+(0.00149792*x))+(-4.47192e-06*(x*x)))+(3.67664e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((0.977076+(0.00280638*x))+(-9.08158e-06*(x*x)))+(7.9073e-09*(x*(x*x)))", 20.,670.);
}
if( Atagger == "JPM" && sEtamin == "0.8" && sEtamax == "1.6")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((0.918387+(0.000898595*x))+(-2.00643e-06*(x*x)))+(1.26486e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.790843+(0.000548016*x))+(-6.70941e-07*(x*x)))+(1.90355e-11*(x*(x*x)))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.0459+(0.00124924*x))+(-3.34192e-06*(x*x)))+(2.51068e-09*(x*(x*x)))", 20.,670.);
}
if( Atagger == "JPM" && sEtamin == "1.6" && sEtamax == "2.4")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((0.790103+(0.00117865*x))+(-2.07334e-06*(x*x)))+(1.42608e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.667144+(0.00105593*x))+(-1.43608e-06*(x*x)))+(5.24039e-10*(x*(x*x)))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((0.913027+(0.00130143*x))+(-2.71061e-06*(x*x)))+(2.32812e-09*(x*(x*x)))", 20.,670.);
}
if( Atagger == "JPT" && sEtamin == "0.0" && sEtamax == "2.4")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((0.831392+(0.00269525*x))+(-7.33391e-06*(x*x)))+(5.73942e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.671888+(0.0020106*x))+(-5.03177e-06*(x*x)))+(3.74225e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((0.990774+(0.00338018*x))+(-9.63606e-06*(x*x)))+(7.73659e-09*(x*(x*x)))", 20.,670.);
}
if( Atagger == "SSVHEM" && sEtamin == "0.0" && sEtamax == "0.8")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((0.86318+(0.000801639*x))+(-1.64119e-06*(x*x)))+(2.59121e-10*(x*(x*x)))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.790364+(0.000463086*x))+(-4.35934e-07*(x*x)))+(-9.08296e-10*(x*(x*x)))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((0.935969+(0.0011402*x))+(-2.84645e-06*(x*x)))+(1.42654e-09*(x*(x*x)))", 20.,670.);
}
if( Atagger == "SSVHEM" && sEtamin == "0.0" && sEtamax == "2.4")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((0.890254+(0.000553319*x))+(-1.29993e-06*(x*x)))+(4.19294e-10*(x*(x*x)))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.817099+(0.000421567*x))+(-9.46432e-07*(x*x)))+(1.62339e-10*(x*(x*x)))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((0.963387+(0.000685092*x))+(-1.65343e-06*(x*x)))+(6.76249e-10*(x*(x*x)))", 20.,670.);
}
if( Atagger == "SSVHEM" && sEtamin == "0.8" && sEtamax == "1.6")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((0.958973+(-0.000269555*x))+(1.381e-06*(x*x)))+(-1.87744e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.865771+(-0.000279908*x))+(1.34144e-06*(x*x)))+(-1.75588e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.0522+(-0.000259296*x))+(1.42056e-06*(x*x)))+(-1.999e-09*(x*(x*x)))", 20.,670.);
}
if( Atagger == "SSVHEM" && sEtamin == "1.6" && sEtamax == "2.4")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((0.923033+(-0.000898227*x))+(4.74565e-06*(x*x)))+(-6.11053e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.828021+(-0.000731926*x))+(4.19613e-06*(x*x)))+(-5.81379e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.01812+(-0.00106483*x))+(5.29518e-06*(x*x)))+(-6.40728e-09*(x*(x*x)))", 20.,670.);
}
if( Atagger == "SSVHPT" && sEtamin == "0.0" && sEtamax == "2.4")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((0.97409+(0.000646241*x))+(-2.86294e-06*(x*x)))+(2.79484e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.807222+(0.00103676*x))+(-3.6243e-06*(x*x)))+(3.17368e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.14091+(0.00025586*x))+(-2.10157e-06*(x*x)))+(2.41599e-09*(x*(x*x)))", 20.,670.);
}
if( Atagger == "TCHEL" && sEtamin == "0.0" && sEtamax == "0.5")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","(1.13615*((1+(-0.00119852*x))+(1.17888e-05*(x*x))))+(-9.8581e-08*(x*(x*(x/(1+(0.00689317*x))))))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","(1.0369*((1+(-0.000945578*x))+(7.73273e-06*(x*x))))+(-4.47791e-08*(x*(x*(x/(1+(0.00499343*x))))))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","(1.22179*((1+(-0.000946228*x))+(7.37821e-06*(x*x))))+(-4.8451e-08*(x*(x*(x/(1+(0.0047976*x))))))", 20.,670.);
}
if( Atagger == "TCHEL" && sEtamin == "0.0" && sEtamax == "2.4")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","(1.10649*((1+(-9.00297e-05*x))+(2.32185e-07*(x*x))))+(-4.04925e-10*(x*(x*(x/(1+(-0.00051036*x))))))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","(1.01541*((1+(-6.04627e-05*x))+(1.38195e-07*(x*x))))+(-2.83043e-10*(x*(x*(x/(1+(-0.000633609*x))))))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","(1.19751*((1+(-0.000114197*x))+(3.08558e-07*(x*x))))+(-5.27598e-10*(x*(x*(x/(1+(-0.000422372*x))))))", 20.,670.);
}
if( Atagger == "TCHEL" && sEtamin == "0.5" && sEtamax == "1.0")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","(1.13277*((1+(-0.00084146*x))+(3.80313e-06*(x*x))))+(-8.75061e-09*(x*(x*(x/(1+(0.00118695*x))))))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","(0.983748*((1+(7.13613e-05*x))+(-1.08648e-05*(x*x))))+(2.96162e-06*(x*(x*(x/(1+(0.282104*x))))))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","(1.22714*((1+(-0.00085562*x))+(3.74425e-06*(x*x))))+(-8.91028e-09*(x*(x*(x/(1+(0.00109346*x))))))", 20.,670.);
}
if( Atagger == "TCHEL" && sEtamin == "1.0" && sEtamax == "1.5")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","(1.17163*((1+(-0.000828475*x))+(3.0769e-06*(x*x))))+(-4.692e-09*(x*(x*(x/(1+(0.000337759*x))))))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","(1.0698*((1+(-0.000731877*x))+(2.56922e-06*(x*x))))+(-3.0318e-09*(x*(x*(x/(1+(5.04118e-05*x))))))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","(1.27351*((1+(-0.000911891*x))+(3.5465e-06*(x*x))))+(-6.69625e-09*(x*(x*(x/(1+(0.000590847*x))))))", 20.,670.);
}
if( Atagger == "TCHEL" && sEtamin == "1.5" && sEtamax == "2.4")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","(1.14554*((1+(-0.000128043*x))+(4.10899e-07*(x*x))))+(-2.07565e-10*(x*(x*(x/(1+(-0.00118618*x))))))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","(1.04766*((1+(-6.87499e-05*x))+(2.2454e-07*(x*x))))+(-1.18395e-10*(x*(x*(x/(1+(-0.00128734*x))))))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","(1.24367*((1+(-0.000182494*x))+(5.92637e-07*(x*x))))+(-3.3745e-10*(x*(x*(x/(1+(-0.00107694*x))))))", 20.,670.);
}
if( Atagger == "TCHEM" && sEtamin == "0.0" && sEtamax == "0.8")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","(1.2875*((1+(-0.000356371*x))+(1.08081e-07*(x*x))))+(-6.89998e-11*(x*(x*(x/(1+(-0.0012139*x))))))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","(1.11418*((1+(-0.000442274*x))+(1.53463e-06*(x*x))))+(-4.93683e-09*(x*(x*(x/(1+(0.00152436*x))))))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","(1.47515*((1+(-0.000484868*x))+(2.36817e-07*(x*x))))+(-2.05073e-11*(x*(x*(x/(1+(-0.00142819*x))))))", 20.,670.);
}
if( Atagger == "TCHEM" && sEtamin == "0.0" && sEtamax == "2.4")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","(1.06268*((1+(0.00390509*x))+(-5.85405e-05*(x*x))))+(7.87135e-07*(x*(x*(x/(1+(0.01259*x))))))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","(0.967092*((1+(0.00201431*x))+(-1.49359e-05*(x*x))))+(6.94324e-08*(x*(x*(x/(1+(0.00459787*x))))))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","(1.22691*((1+(0.00211682*x))+(-2.07959e-05*(x*x))))+(1.72938e-07*(x*(x*(x/(1+(0.00658853*x))))))", 20.,670.);
}
if( Atagger == "TCHEM" && sEtamin == "0.8" && sEtamax == "1.6")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","(1.24986*((1+(-0.00039734*x))+(5.37486e-07*(x*x))))+(-1.74023e-10*(x*(x*(x/(1+(-0.00112954*x))))))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","(1.08828*((1+(-0.000208737*x))+(1.50487e-07*(x*x))))+(-2.54249e-11*(x*(x*(x/(1+(-0.00141477*x))))))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","(1.41211*((1+(-0.000559603*x))+(9.50754e-07*(x*x))))+(-5.81148e-10*(x*(x*(x/(1+(-0.000787359*x))))))", 20.,670.);
}
if( Atagger == "TCHEM" && sEtamin == "1.6" && sEtamax == "2.4")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","(1.10763*((1+(-0.000105805*x))+(7.11718e-07*(x*x))))+(-5.3001e-10*(x*(x*(x/(1+(-0.000821215*x))))))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","(0.958079*((1+(0.000327804*x))+(-4.09511e-07*(x*x))))+(-1.95933e-11*(x*(x*(x/(1+(-0.00143323*x))))))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","(1.26236*((1+(-0.000524055*x))+(2.08863e-06*(x*x))))+(-2.29473e-09*(x*(x*(x/(1+(-0.000276268*x))))))", 20.,670.);
}
if( Atagger == "TCHPM" && sEtamin == "0.0" && sEtamax == "0.8")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.27011+(-0.000869141*x))+(2.49796e-06*(x*x)))+(-2.62962e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((1.12949+(-0.000678492*x))+(2.02219e-06*(x*x)))+(-2.21675e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.41077+(-0.00105992*x))+(2.97373e-06*(x*x)))+(-3.0425e-09*(x*(x*x)))", 20.,670.);
}
if( Atagger == "TCHPM" && sEtamin == "0.0" && sEtamax == "2.4")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.27417+(-0.000449095*x))+(1.0719e-06*(x*x)))+(-1.35208e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((1.14205+(-0.000350151*x))+(8.43333e-07*(x*x)))+(-1.14104e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.4063+(-0.000548107*x))+(1.30047e-06*(x*x)))+(-1.56311e-09*(x*(x*x)))", 20.,670.);
}
if( Atagger == "TCHPM" && sEtamin == "0.8" && sEtamax == "1.6")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.36167+(-0.00153237*x))+(4.54567e-06*(x*x)))+(-4.38874e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((1.21289+(-0.00126411*x))+(3.81676e-06*(x*x)))+(-3.75847e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.51053+(-0.00180085*x))+(5.27457e-06*(x*x)))+(-5.01901e-09*(x*(x*x)))", 20.,670.);
}
if( Atagger == "TCHPM" && sEtamin == "1.6" && sEtamax == "2.4")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.22696+(0.000249231*x))+(9.55279e-08*(x*x)))+(-1.04034e-09*(x*(x*x)))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((1.07572+(0.00055366*x))+(-9.55796e-07*(x*x)))+(-3.73943e-11*(x*(x*x)))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.3782+(-5.52498e-05*x))+(1.14685e-06*(x*x)))+(-2.04329e-09*(x*(x*x)))", 20.,670.);
}
if( Atagger == "TCHPT" && sEtamin == "0.0" && sEtamax == "2.4")
{
if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.20711+(0.000681067*x))+(-1.57062e-06*(x*x)))+(2.83138e-10*(x*(x*x)))", 20.,670.);
if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((1.03418+(0.000428273*x))+(-5.43024e-07*(x*x)))+(-6.18061e-10*(x*(x*x)))", 20.,670.);
if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.38002+(0.000933875*x))+(-2.59821e-06*(x*x)))+(1.18434e-09*(x*(x*x)))", 20.,670.);
}

// End of definition of functions from plot33New.C ---------------
  if( tmpSFl == NULL ) cout << "NULL pointer returned... Function seems not to exist" << endl;

  return tmpSFl;
}

