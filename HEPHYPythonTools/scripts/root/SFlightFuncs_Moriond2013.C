#include "TF1.h"
#include "TLegend.h"
#include <TCanvas.h>

//------------ Exemple of usage --------------
//
// In a root session:
// 	.L SFlightFuncs.C+g	//To load this program
// Then...
// To get a pointer to the SFlight function for CSV tagger Loose (L) in the eta range 0.0-0.5 for the data taking period A+B+C+D, use: 
//	TF1* SFlight = GetSFlmean("CSV","L",0.0, 0.5, "ABCD")
// To get a pointer to the SFlightmin function for CSV tagger Loose (L) in the eta range 0.0-0.5 for the data taking period A+B+C+D, use: 
//	TF1* SFlightmin = GetSFlmin("CSV","L",0.0, 0.5, "ABCD")
// To get a pointer to the SFlightmax function for CSV tagger Loose (L) in the eta range 0.0-0.5 for the data taking period A+B+C+D, use: 
//	TF1* SFlightmax = GetSFlmax("CSV","L",0.0, 0.5, "ABCD")
//
// Note:
// 1) SFlightmin and SFlightmax correspond to SFlight +- (stat+syst error).
// 2) If the specified combination of tagger/taggerstrength/etarange is not tabulated,
//    a NULL pointer is returned.
//
//-------------------------------------------
TF1* GetSFLight(TString meanminmax, TString tagger, TString TaggerStrength, Float_t Etamin, Float_t Etamax, TString DataPeriod);

TF1* GetSFlmean(TString tagger, TString TaggerStrength, float Etamin, float Etamax, TString DataPeriod)
{
  return GetSFLight("mean",tagger,TaggerStrength,Etamin,Etamax,DataPeriod);
}
TF1* GetSFlmin(TString tagger, TString TaggerStrength, float Etamin, float Etamax, TString DataPeriod)
{
  return GetSFLight("min",tagger,TaggerStrength,Etamin,Etamax,DataPeriod);
}
TF1* GetSFlmax(TString tagger, TString TaggerStrength, float Etamin, float Etamax, TString DataPeriod)
{
  return GetSFLight("max",tagger,TaggerStrength,Etamin,Etamax,DataPeriod);
}

TF1* plotmean(TString tagger, TString TaggerStrength, float Etamin, float Etamax, TString DataPeriod = "ABCD", TString opt = "" , int col = 1, float lineWidth = 1, int lineStyle = 1)
{
  TF1* f = GetSFlmean(tagger,TaggerStrength,Etamin,Etamax,DataPeriod);
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
TF1* plotmin(TString tagger, TString TaggerStrength, float Etamin, float Etamax, TString DataPeriod, TString opt = "" , int col = 1, float lineWidth = 1, int lineStyle = 1)
{
  TF1* f = GetSFlmin(tagger,TaggerStrength,Etamin,Etamax,DataPeriod);
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
TF1* plotmax(TString tagger, TString TaggerStrength, float Etamin, float Etamax, TString DataPeriod, TString opt = "" , int col = 1, float lineWidth = 1, int lineStyle = 1)
{
  TF1* f = GetSFlmax(tagger,TaggerStrength,Etamin,Etamax,DataPeriod);
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
void plotmean(TCanvas *yourC, int yourzone, TString tagger, TString TaggerStrength, TString DataPeriod)
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

  f[1] = plotmean(tagger,TaggerStrength,etamin[1], etamax[1], DataPeriod, "", 1, 1);
    //TString rangeEta = Form("Mean(SF(%1.1f #leq #eta %1.1f))",etamin[1],etamax[1]);
    TString rangeEta = Form("SF(%1.1f #leq #eta %1.1f)",etamin[1],etamax[1]);
    leg->AddEntry(f[1],rangeEta,"l");
  for( int i = 2; i <= N; ++i )
  {
    f[i] = plotmean(tagger,TaggerStrength,etamin[i], etamax[i], DataPeriod, "same", i, 1);
    //TString rangeEta = Form("Mean(SF(%1.1f #leq #eta %1.1f))",etamin[i],etamax[i]);
    TString rangeEta = Form("SF(%1.1f #leq #eta %1.1f)",etamin[i],etamax[i]);
    leg->AddEntry(f[i],rangeEta,"l");
  }
  //leg->AddEntry(gg," gluon jets","P");
  leg->Draw();
  //return cWork;
}
TCanvas *plotmean(TString tagger, TString TaggerStrength, TString DataPeriod)
{
 TCanvas *cWork = new TCanvas("cWork", "plots",200,10,700,750);
 plotmean(cWork, 0, tagger, TaggerStrength, DataPeriod);

 return cWork;
}
TCanvas *plotmean(TString selecter, TString DataPeriod)
{
 TCanvas *cWork = NULL; 
 if( selecter == "L" )
 {
   cWork = new TCanvas("cWork", "plots",200,10,700,500);
   cWork->Divide(1,2);
   plotmean(cWork, 1, "JP", selecter, DataPeriod);
   plotmean(cWork, 2, "CSV", selecter, DataPeriod);
 }
 else if( selecter == "M" )
 {
   cWork = new TCanvas("cWork", "plots",200,10,700,500);
   cWork->Divide(1,2);
   plotmean(cWork, 1, "JP", selecter, DataPeriod);
   plotmean(cWork, 2, "CSV", selecter, DataPeriod);
 }
 else if( selecter == "T" )
 {
   cWork = new TCanvas("cWork", "plots",200,10,700,750);
   cWork->Divide(1,3);
   plotmean(cWork, 1, "JP", selecter, DataPeriod);
   plotmean(cWork, 2, "CSV", selecter, DataPeriod);
   plotmean(cWork, 3, "TCHP", selecter, DataPeriod);
 }
 else if( selecter == "TCHP" )
 {
   cWork = new TCanvas("cWork", "plots",200,10,700,250);
   plotmean(cWork, 0, selecter, "T", DataPeriod);
 }
 else
 {
   cWork = new TCanvas("cWork", "plots",200,10,700,750);
   cWork->Divide(1,3);
   plotmean(cWork, 1, selecter, "L", DataPeriod);
   plotmean(cWork, 2, selecter, "M", DataPeriod);
   plotmean(cWork, 3, selecter, "T", DataPeriod);
 }

 cWork->WaitPrimitive();
 cWork->SaveAs("SFlightFunc_"+selecter+".pdf");
 return cWork;
}
TCanvas *plotmean(TString DataPeriod = "ABCD")
{
 TCanvas *cWork = new TCanvas("cWork", "plots",200,10,700,750);
 cWork->Divide(3,3, 0.002, 0.002);
 cWork->SetFillColor(10);
 cWork->SetFillStyle(4000);
 cWork->SetBorderSize(1);
 for( int i = 0; i < 3*3; ++i )
 {
   cWork->cd(i+1)->SetFillColor(10);
   cWork->cd(i+1)->SetFillStyle(4000);
   cWork->cd(i+1)->SetBorderSize(1);
 }
 plotmean(cWork, 1, "JP", "L", DataPeriod);
 plotmean(cWork, 2, "JP", "M", DataPeriod);
 plotmean(cWork, 3, "JP", "T", DataPeriod);
 plotmean(cWork, 4, "CSV", "L", DataPeriod);
 plotmean(cWork, 5, "CSV", "M", DataPeriod);
 plotmean(cWork, 6, "CSV", "T", DataPeriod);
 plotmean(cWork, 9, "TCHP", "T", DataPeriod);

 return cWork;
}


TF1* GetSFLight(TString meanminmax, TString tagger, TString TaggerStrength, Float_t Etamin, Float_t Etamax, TString DataPeriod)
{
  TF1 *tmpSFl = NULL;
  TString Atagger = tagger+TaggerStrength;
  TString sEtamin = Form("%1.1f",Etamin);
  TString sEtamax = Form("%1.1f",Etamax);
  cout << sEtamin << endl;
  cout << sEtamax << endl;

  if (DataPeriod=="ABCD") {

    // Begin of definition of functions from SF_12ABCD ---------------

    Double_t ptmax;
    if( sEtamin == "1.5" || sEtamin == "1.6" ) ptmax = 700;
    else ptmax = 800;
    
    if( Atagger == "CSVL" && sEtamin == "0.0" && sEtamax == "0.5")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.04901+(0.00152181*x))+(-3.43568e-06*(x*x)))+(2.17219e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.973773+(0.00103049*x))+(-2.2277e-06*(x*x)))+(1.37208e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.12424+(0.00201136*x))+(-4.64021e-06*(x*x)))+(2.97219e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "CSVL" && sEtamin == "0.5" && sEtamax == "1.0")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((0.991915+(0.00172552*x))+(-3.92652e-06*(x*x)))+(2.56816e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.921518+(0.00129098*x))+(-2.86488e-06*(x*x)))+(1.86022e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.06231+(0.00215815*x))+(-4.9844e-06*(x*x)))+(3.27623e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "CSVL" && sEtamin == "1.0" && sEtamax == "1.5")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((0.962127+(0.00192796*x))+(-4.53385e-06*(x*x)))+(3.0605e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.895419+(0.00153387*x))+(-3.48409e-06*(x*x)))+(2.30899e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.02883+(0.00231985*x))+(-5.57924e-06*(x*x)))+(3.81235e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "CSVL" && sEtamin == "1.5" && sEtamax == "2.4")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.06121+(0.000332747*x))+(-8.81201e-07*(x*x)))+(7.43896e-10*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.983607+(0.000196747*x))+(-3.98327e-07*(x*x)))+(2.95764e-10*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.1388+(0.000468418*x))+(-1.36341e-06*(x*x)))+(1.19256e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "CSVM" && sEtamin == "0.0" && sEtamax == "0.8")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.06238+(0.00198635*x))+(-4.89082e-06*(x*x)))+(3.29312e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.972746+(0.00104424*x))+(-2.36081e-06*(x*x)))+(1.53438e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.15201+(0.00292575*x))+(-7.41497e-06*(x*x)))+(5.0512e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "CSVM" && sEtamin == "0.8" && sEtamax == "1.6")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.08048+(0.00110831*x))+(-2.96189e-06*(x*x)))+(2.16266e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.9836+(0.000649761*x))+(-1.59773e-06*(x*x)))+(1.14324e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.17735+(0.00156533*x))+(-4.32257e-06*(x*x)))+(3.18197e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "CSVM" && sEtamin == "1.6" && sEtamax == "2.4")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.09145+(0.000687171*x))+(-2.45054e-06*(x*x)))+(1.7844e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((1.00616+(0.000358884*x))+(-1.23768e-06*(x*x)))+(6.86678e-10*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.17671+(0.0010147*x))+(-3.66269e-06*(x*x)))+(2.88425e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "CSVT" && sEtamin == "0.0" && sEtamax == "2.4")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.01739+(0.00283619*x))+(-7.93013e-06*(x*x)))+(5.97491e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.953587+(0.00124872*x))+(-3.97277e-06*(x*x)))+(3.23466e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.08119+(0.00441909*x))+(-1.18764e-05*(x*x)))+(8.71372e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "JPL" && sEtamin == "0.0" && sEtamax == "0.5")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.05617+(0.000986016*x))+(-2.05398e-06*(x*x)))+(1.25408e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.918762+(0.000749113*x))+(-1.48511e-06*(x*x)))+(8.78559e-10*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.19358+(0.00122182*x))+(-2.62078e-06*(x*x)))+(1.62951e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "JPL" && sEtamin == "0.5" && sEtamax == "1.0")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.02884+(0.000471854*x))+(-1.15441e-06*(x*x)))+(7.83716e-10*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.893017+(0.000369124*x))+(-8.68577e-07*(x*x)))+(5.79006e-10*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.16466+(0.000573985*x))+(-1.43899e-06*(x*x)))+(9.88387e-10*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "JPL" && sEtamin == "1.0" && sEtamax == "1.5")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.02463+(0.000907924*x))+(-2.07133e-06*(x*x)))+(1.37083e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.89415+(0.000712877*x))+(-1.57703e-06*(x*x)))+(1.02034e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.15511+(0.00110197*x))+(-2.56374e-06*(x*x)))+(1.72152e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "JPL" && sEtamin == "1.5" && sEtamax == "2.4")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.05387+(0.000951237*x))+(-2.35437e-06*(x*x)))+(1.66123e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.918611+(0.000781707*x))+(-1.8923e-06*(x*x)))+(1.312e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.1891+(0.00112006*x))+(-2.81586e-06*(x*x)))+(2.01249e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "JPM" && sEtamin == "0.0" && sEtamax == "0.8")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((0.980407+(0.00190765*x))+(-4.49633e-06*(x*x)))+(3.02664e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.813164+(0.00127951*x))+(-2.74274e-06*(x*x)))+(1.78799e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.14766+(0.00253327*x))+(-6.24447e-06*(x*x)))+(4.26468e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "JPM" && sEtamin == "0.8" && sEtamax == "1.6")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.01783+(0.00183763*x))+(-4.64972e-06*(x*x)))+(3.34342e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.860873+(0.00110031*x))+(-2.48023e-06*(x*x)))+(1.73776e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.17479+(0.00257252*x))+(-6.81377e-06*(x*x)))+(4.94891e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "JPM" && sEtamin == "1.6" && sEtamax == "2.4")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((0.866685+(0.00396887*x))+(-1.11342e-05*(x*x)))+(8.84085e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.740983+(0.00302736*x))+(-8.12284e-06*(x*x)))+(6.281e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((0.992297+(0.00490671*x))+(-1.41403e-05*(x*x)))+(1.14097e-08*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "JPT" && sEtamin == "0.0" && sEtamax == "2.4")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((0.89627+(0.00328988*x))+(-8.76392e-06*(x*x)))+(6.4662e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.666092+(0.00262465*x))+(-6.5345e-06*(x*x)))+(4.73926e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.12648+(0.00394995*x))+(-1.0981e-05*(x*x)))+(8.19134e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "TCHPT" && sEtamin == "0.0" && sEtamax == "2.4")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.1676+(0.00136673*x))+(-3.51053e-06*(x*x)))+(2.4966e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.988346+(0.000914722*x))+(-2.37077e-06*(x*x)))+(1.72082e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.34691+(0.00181637*x))+(-4.64484e-06*(x*x)))+(3.27122e-09*(x*(x*x)))", 20.,ptmax);
      }

    // End of definition of functions from SF_12ABCD ---------------

  } else if (DataPeriod=="AB") { 

    // Begin of definition of functions from SF_12AB ---------------

    Double_t ptmax;
    if( sEtamin == "1.5" || sEtamin == "1.6" ) ptmax = 700;
    else ptmax = 800;

    if( Atagger == "CSVL" && sEtamin == "0.0" && sEtamax == "0.5")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.00989+(0.00155686*x))+(-3.72647e-06*(x*x)))+(2.47025e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.947488+(0.00105091*x))+(-2.43972e-06*(x*x)))+(1.58902e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.07229+(0.00206098*x))+(-5.00971e-06*(x*x)))+(3.35179e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "CSVL" && sEtamin == "0.5" && sEtamax == "1.0")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((0.958598+(0.00173458*x))+(-4.12744e-06*(x*x)))+(2.83257e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.900024+(0.00129392*x))+(-3.01708e-06*(x*x)))+(2.06723e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.01716+(0.00217335*x))+(-5.23419e-06*(x*x)))+(3.5986e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "CSVL" && sEtamin == "1.0" && sEtamax == "1.5")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((0.963113+(0.00163674*x))+(-3.84776e-06*(x*x)))+(2.56918e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.90596+(0.00125465*x))+(-2.78863e-06*(x*x)))+(1.78602e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.02025+(0.0020171*x))+(-4.90389e-06*(x*x)))+(3.35329e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "CSVL" && sEtamin == "1.5" && sEtamax == "2.4")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.04996+(0.00031979*x))+(-8.43322e-07*(x*x)))+(6.9451e-10*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.983472+(0.000169396*x))+(-2.82848e-07*(x*x)))+(1.52744e-10*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.11645+(0.000469873*x))+(-1.40321e-06*(x*x)))+(1.23681e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "CSVM" && sEtamin == "0.0" && sEtamax == "0.8")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.02213+(0.00189078*x))+(-4.59419e-06*(x*x)))+(3.0366e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.946+(0.000940317*x))+(-1.99048e-06*(x*x)))+(1.18343e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.09827+(0.00283897*x))+(-7.19354e-06*(x*x)))+(4.89013e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "CSVM" && sEtamin == "0.8" && sEtamax == "1.6")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.0596+(0.00102926*x))+(-2.70312e-06*(x*x)))+(1.82871e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.974966+(0.000545735*x))+(-1.23123e-06*(x*x)))+(7.05661e-10*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.14423+(0.00151156*x))+(-4.17277e-06*(x*x)))+(2.95233e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "CSVM" && sEtamin == "1.6" && sEtamax == "2.4")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.04976+(0.000897158*x))+(-3.22829e-06*(x*x)))+(2.71316e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.977166+(0.000550586*x))+(-1.91114e-06*(x*x)))+(1.44817e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.12232+(0.00124269*x))+(-4.54368e-06*(x*x)))+(3.98079e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "CSVT" && sEtamin == "0.0" && sEtamax == "2.4")
    {
        if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((0.985589+(0.00302526*x))+(-8.73861e-06*(x*x)))+(6.65051e-09*(x*(x*x)))", 20.,ptmax);
        if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.93612+(0.00131596*x))+(-4.30052e-06*(x*x)))+(3.45957e-09*(x*(x*x)))", 20.,ptmax);
        if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.03505+(0.00472994*x))+(-1.31661e-05*(x*x)))+(9.84151e-09*(x*(x*x)))", 20.,ptmax);
    }
    if( Atagger == "JPL" && sEtamin == "0.0" && sEtamax == "0.5")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.01004+(0.000693171*x))+(-1.71673e-06*(x*x)))+(1.13601e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.920801+(0.00048556*x))+(-1.14573e-06*(x*x)))+(7.29722e-10*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.09929+(0.000899912*x))+(-2.28605e-06*(x*x)))+(1.54241e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "JPL" && sEtamin == "0.5" && sEtamax == "1.0")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((0.983323+(0.00021632*x))+(-8.21701e-07*(x*x)))+(6.67398e-10*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.893817+(0.000139244*x))+(-5.53288e-07*(x*x)))+(4.54312e-10*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.07283+(0.000292983*x))+(-1.08908e-06*(x*x)))+(8.80497e-10*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "JPL" && sEtamin == "1.0" && sEtamax == "1.5")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.00787+(0.00067391*x))+(-1.85829e-06*(x*x)))+(1.42239e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.922717+(0.000501621*x))+(-1.3493e-06*(x*x)))+(1.02068e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.09302+(0.000845356*x))+(-2.36546e-06*(x*x)))+(1.82448e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "JPL" && sEtamin == "1.5" && sEtamax == "2.4")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.03546+(0.000774019*x))+(-2.15928e-06*(x*x)))+(1.6934e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.946412+(0.000642931*x))+(-1.74696e-06*(x*x)))+(1.34402e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.12449+(0.000904468*x))+(-2.57084e-06*(x*x)))+(2.04473e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "JPM" && sEtamin == "0.0" && sEtamax == "0.8")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((0.95344+(0.00171952*x))+(-4.71763e-06*(x*x)))+(3.41607e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.821103+(0.0011014*x))+(-2.81576e-06*(x*x)))+(2.00088e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.08578+(0.00233518*x))+(-6.61409e-06*(x*x)))+(4.83128e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "JPM" && sEtamin == "0.8" && sEtamax == "1.6")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((0.994557+(0.00176506*x))+(-4.95785e-06*(x*x)))+(3.63594e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.874792+(0.000997253*x))+(-2.51511e-06*(x*x)))+(1.75184e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.11431+(0.0025305*x))+(-7.39562e-06*(x*x)))+(5.52077e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "JPM" && sEtamin == "1.6" && sEtamax == "2.4")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((0.850708+(0.00373619*x))+(-1.10196e-05*(x*x)))+(9.0243e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.756769+(0.0028841*x))+(-8.02579e-06*(x*x)))+(6.29964e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((0.944553+(0.00458472*x))+(-1.40078e-05*(x*x)))+(1.1758e-08*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "JPT" && sEtamin == "0.0" && sEtamax == "2.4")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((0.869428+(0.00338068*x))+(-9.51813e-06*(x*x)))+(7.08382e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.657456+(0.00279437*x))+(-7.29415e-06*(x*x)))+(5.28578e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.08141+(0.00396192*x))+(-1.17308e-05*(x*x)))+(8.88194e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "TCHPT" && sEtamin == "0.0" && sEtamax == "2.4")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.10796+(0.00168368*x))+(-4.50964e-06*(x*x)))+(3.21561e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.948977+(0.0011449*x))+(-3.05912e-06*(x*x)))+(2.17813e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.26699+(0.00221974*x))+(-5.95423e-06*(x*x)))+(4.25254e-09*(x*(x*x)))", 20.,ptmax);
      }
    
    // End of definition of functions from SF_12AB ---------------
    
  } else if (DataPeriod=="C") { 

    // Begin of definition of functions from SF_12C ---------------
    
    Double_t ptmax;
    if( sEtamin == "1.5" || sEtamin == "1.6" ) ptmax = 700;
    else ptmax = 800;
    
    if( Atagger == "CSVL" && sEtamin == "0.0" && sEtamax == "0.5")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.03512+(0.00172098*x))+(-4.10286e-06*(x*x)))+(2.72413e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.971321+(0.00117532*x))+(-2.71334e-06*(x*x)))+(1.77294e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.0989+(0.0022646*x))+(-5.48834e-06*(x*x)))+(3.67551e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "CSVL" && sEtamin == "0.5" && sEtamax == "1.0")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((0.977454+(0.00186222*x))+(-4.30874e-06*(x*x)))+(2.82227e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.917942+(0.00139264*x))+(-3.13422e-06*(x*x)))+(2.02475e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.03695+(0.00232982*x))+(-5.47968e-06*(x*x)))+(3.62048e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "CSVL" && sEtamin == "1.0" && sEtamax == "1.5")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((0.940154+(0.00214045*x))+(-5.30206e-06*(x*x)))+(3.75872e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.885078+(0.00170468*x))+(-4.08896e-06*(x*x)))+(2.85628e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((0.995215+(0.00257376*x))+(-6.5103e-06*(x*x)))+(4.66211e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "CSVL" && sEtamin == "1.5" && sEtamax == "2.4")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.04882+(0.000373418*x))+(-1.00316e-06*(x*x)))+(8.52325e-10*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.982642+(0.000211816*x))+(-4.11471e-07*(x*x)))+(2.88443e-10*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.11499+(0.000534645*x))+(-1.59409e-06*(x*x)))+(1.41682e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "CSVM" && sEtamin == "0.0" && sEtamax == "0.8")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.0444+(0.00216756*x))+(-5.4224e-06*(x*x)))+(3.69351e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.966203+(0.00112979*x))+(-2.56147e-06*(x*x)))+(1.65183e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.1226+(0.00320252*x))+(-8.27754e-06*(x*x)))+(5.73519e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "CSVM" && sEtamin == "0.8" && sEtamax == "1.6")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.05203+(0.00138588*x))+(-3.97677e-06*(x*x)))+(3.13655e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.966774+(0.000855535*x))+(-2.33883e-06*(x*x)))+(1.86063e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.13729+(0.00191432*x))+(-5.61018e-06*(x*x)))+(4.41282e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "CSVM" && sEtamin == "1.6" && sEtamax == "2.4")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.06547+(0.000850114*x))+(-2.76694e-06*(x*x)))+(1.75015e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.992673+(0.000455214*x))+(-1.29572e-06*(x*x)))+(3.89704e-10*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.13823+(0.00124422*x))+(-4.23813e-06*(x*x)))+(3.11339e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "CSVT" && sEtamin == "0.0" && sEtamax == "2.4")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.00197+(0.00266395*x))+(-6.95018e-06*(x*x)))+(4.91042e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.948887+(0.00103466*x))+(-2.88118e-06*(x*x)))+(2.07782e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.05505+(0.00428961*x))+(-1.10115e-05*(x*x)))+(7.74319e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "JPL" && sEtamin == "0.0" && sEtamax == "0.5")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.04676+(0.00112324*x))+(-2.52493e-06*(x*x)))+(1.65931e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.954301+(0.000859775*x))+(-1.83391e-06*(x*x)))+(1.17383e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.13922+(0.00138539*x))+(-3.21336e-06*(x*x)))+(2.14483e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "JPL" && sEtamin == "0.5" && sEtamax == "1.0")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.01822+(0.000554752*x))+(-1.44083e-06*(x*x)))+(9.9442e-10*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.925322+(0.00044089*x))+(-1.09668e-06*(x*x)))+(7.37906e-10*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.11112+(0.000667913*x))+(-1.78357e-06*(x*x)))+(1.25108e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "JPL" && sEtamin == "1.0" && sEtamax == "1.5")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.00672+(0.000952424*x))+(-2.24525e-06*(x*x)))+(1.49885e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.922111+(0.000746635*x))+(-1.68093e-06*(x*x)))+(1.07795e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.09131+(0.00115721*x))+(-2.80782e-06*(x*x)))+(1.92031e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "JPL" && sEtamin == "1.5" && sEtamax == "2.4")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.0346+(0.00102282*x))+(-2.61072e-06*(x*x)))+(1.91999e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.946009+(0.00085601*x))+(-2.11306e-06*(x*x)))+(1.5133e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.12316+(0.00118887*x))+(-3.10773e-06*(x*x)))+(2.32911e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "JPM" && sEtamin == "0.0" && sEtamax == "0.8")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((0.976097+(0.00191673*x))+(-4.58557e-06*(x*x)))+(3.10331e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.838655+(0.00127127*x))+(-2.69532e-06*(x*x)))+(1.73384e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.11354+(0.00255978*x))+(-6.47089e-06*(x*x)))+(4.47278e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "JPM" && sEtamin == "0.8" && sEtamax == "1.6")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.01871+(0.00173675*x))+(-4.58934e-06*(x*x)))+(3.38512e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.896752+(0.000935708*x))+(-2.09673e-06*(x*x)))+(1.47779e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.14066+(0.00253557*x))+(-7.07715e-06*(x*x)))+(5.29295e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "JPM" && sEtamin == "1.6" && sEtamax == "2.4")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((0.857254+(0.00402389*x))+(-1.15649e-05*(x*x)))+(9.37845e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.766329+(0.00306103*x))+(-8.27326e-06*(x*x)))+(6.43552e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((0.948081+(0.00498302*x))+(-1.48512e-05*(x*x)))+(1.23315e-08*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "JPT" && sEtamin == "0.0" && sEtamax == "2.4")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((0.911203+(0.00300921*x))+(-8.03854e-06*(x*x)))+(5.97264e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.698853+(0.00240605*x))+(-5.86773e-06*(x*x)))+(4.23559e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.12356+(0.00360804*x))+(-1.01996e-05*(x*x)))+(7.70949e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "TCHPT" && sEtamin == "0.0" && sEtamax == "2.4")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.1393+(0.00148115*x))+(-3.72335e-06*(x*x)))+(2.6087e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.977185+(0.000957694*x))+(-2.36635e-06*(x*x)))+(1.65373e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.30146+(0.00200233*x))+(-5.07544e-06*(x*x)))+(3.56314e-09*(x*(x*x)))", 20.,ptmax);
      }
    
    // End of definition of functions from SF_12C ---------------
    
  } else if (DataPeriod=="D") { 
    
    // Begin of definition of functions from SF_12D ---------------

    Double_t ptmax;
    if( sEtamin == "1.5" || sEtamin == "1.6" ) ptmax = 700;
    else ptmax = 800;
    
    if( Atagger == "CSVL" && sEtamin == "0.0" && sEtamax == "0.5")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.1121+(0.00156291*x))+(-3.72267e-06*(x*x)))+(2.54276e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((1.04345+(0.00100049*x))+(-2.27285e-06*(x*x)))+(1.53238e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.18074+(0.00212352*x))+(-5.16888e-06*(x*x)))+(3.55347e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "CSVL" && sEtamin == "0.5" && sEtamax == "1.0")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.05107+(0.0018085*x))+(-4.42378e-06*(x*x)))+(3.12722e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.986937+(0.00132072*x))+(-3.17261e-06*(x*x)))+(2.25152e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.11519+(0.00229425*x))+(-5.67093e-06*(x*x)))+(4.00366e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "CSVL" && sEtamin == "1.0" && sEtamax == "1.5")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((0.984747+(0.00233796*x))+(-5.84283e-06*(x*x)))+(4.21798e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.927306+(0.00186598*x))+(-4.5141e-06*(x*x)))+(3.21483e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.04217+(0.0028073*x))+(-7.16639e-06*(x*x)))+(5.2225e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "CSVL" && sEtamin == "1.5" && sEtamax == "2.4")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.0944+(0.000394694*x))+(-1.31095e-06*(x*x)))+(1.29556e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((1.0255+(0.000220197*x))+(-6.45505e-07*(x*x)))+(6.40579e-10*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.1633+(0.000568652*x))+(-1.97487e-06*(x*x)))+(1.95111e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "CSVM" && sEtamin == "0.0" && sEtamax == "0.8")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.13626+(0.00209868*x))+(-5.54303e-06*(x*x)))+(3.9911e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((1.05089+(0.00100001*x))+(-2.44384e-06*(x*x)))+(1.72918e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.22164+(0.00319447*x))+(-8.63596e-06*(x*x)))+(6.25306e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "CSVM" && sEtamin == "0.8" && sEtamax == "1.6")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.13291+(0.00128329*x))+(-3.79952e-06*(x*x)))+(3.03032e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((1.04112+(0.000728221*x))+(-2.04996e-06*(x*x)))+(1.64537e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.22469+(0.0018366*x))+(-5.54498e-06*(x*x)))+(4.4159e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "CSVM" && sEtamin == "1.6" && sEtamax == "2.4")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.18705+(0.000305854*x))+(-1.86925e-06*(x*x)))+(1.79183e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((1.10587+(-8.23503e-05*x))+(-3.06139e-07*(x*x)))+(2.38667e-10*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.26821+(0.000693404*x))+(-3.43071e-06*(x*x)))+(3.34622e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "CSVT" && sEtamin == "0.0" && sEtamax == "2.4")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.08603+(0.0027994*x))+(-8.44182e-06*(x*x)))+(6.847e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((1.02837+(0.00104078*x))+(-3.81136e-06*(x*x)))+(3.43028e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.14368+(0.00455363*x))+(-1.30615e-05*(x*x)))+(1.0264e-08*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "JPL" && sEtamin == "0.0" && sEtamax == "0.5")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.12238+(0.00152486*x))+(-3.2873e-06*(x*x)))+(2.17918e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((1.02366+(0.0012007*x))+(-2.45347e-06*(x*x)))+(1.58906e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.22108+(0.00184736*x))+(-4.11792e-06*(x*x)))+(2.76952e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "JPL" && sEtamin == "0.5" && sEtamax == "1.0")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.10302+(0.000874045*x))+(-1.99863e-06*(x*x)))+(1.39584e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((1.00257+(0.000719596*x))+(-1.5641e-06*(x*x)))+(1.07029e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.20346+(0.00102756*x))+(-2.43131e-06*(x*x)))+(1.72172e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "JPL" && sEtamin == "1.0" && sEtamax == "1.5")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.06244+(0.00149626*x))+(-3.55121e-06*(x*x)))+(2.51004e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.973582+(0.00122407*x))+(-2.81096e-06*(x*x)))+(1.94803e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.15128+(0.0017669*x))+(-4.28856e-06*(x*x)))+(3.07303e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "JPL" && sEtamin == "1.5" && sEtamax == "2.4")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.10432+(0.00129851*x))+(-3.26353e-06*(x*x)))+(2.32516e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((1.00996+(0.00109673*x))+(-2.66726e-06*(x*x)))+(1.84117e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.19864+(0.00149937*x))+(-3.85934e-06*(x*x)))+(2.81243e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "JPM" && sEtamin == "0.0" && sEtamax == "0.8")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.0075+(0.00257791*x))+(-5.91599e-06*(x*x)))+(4.142e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.867433+(0.00177435*x))+(-3.62606e-06*(x*x)))+(2.46206e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.14757+(0.00337847*x))+(-8.19968e-06*(x*x)))+(5.82223e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "JPM" && sEtamin == "0.8" && sEtamax == "1.6")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.02335+(0.00274819*x))+(-7.08829e-06*(x*x)))+(5.44469e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.903546+(0.0017276*x))+(-3.96021e-06*(x*x)))+(3.00594e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.14313+(0.00376554*x))+(-1.02094e-05*(x*x)))+(7.88496e-09*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "JPM" && sEtamin == "1.6" && sEtamax == "2.4")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((0.898963+(0.00428943*x))+(-1.12357e-05*(x*x)))+(8.35894e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.804719+(0.00322419*x))+(-7.66523e-06*(x*x)))+(5.18187e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((0.993109+(0.00535115*x))+(-1.48031e-05*(x*x)))+(1.15468e-08*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "JPT" && sEtamin == "0.0" && sEtamax == "2.4")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((0.887609+(0.00411151*x))+(-1.10861e-05*(x*x)))+(8.50678e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((0.681054+(0.00325624*x))+(-8.17194e-06*(x*x)))+(6.14789e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.09416+(0.00496121*x))+(-1.39877e-05*(x*x)))+(1.08667e-08*(x*(x*x)))", 20.,ptmax);
      }
    if( Atagger == "TCHPT" && sEtamin == "0.0" && sEtamax == "2.4")
      {
	if( meanminmax == "mean" ) tmpSFl = new TF1("SFlight","((1.25209+(0.00136201*x))+(-3.90275e-06*(x*x)))+(3.1283e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "min" ) tmpSFl = new TF1("SFlightMin","((1.07448+(0.000816207*x))+(-2.38176e-06*(x*x)))+(1.97453e-09*(x*(x*x)))", 20.,ptmax);
	if( meanminmax == "max" ) tmpSFl = new TF1("SFlightMax","((1.42974+(0.00190546*x))+(-5.41793e-06*(x*x)))+(4.28148e-09*(x*(x*x)))", 20.,ptmax);
      }

    // End of definition of functions from SF_12D ---------------
    
  } 
  
  if( tmpSFl == NULL ) cout << "NULL pointer returned... Function seems not to exist" << endl;

  return tmpSFl;
}

