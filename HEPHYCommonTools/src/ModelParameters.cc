#include "Workspace/HEPHYCommonTools/interface/ModelParameters.h"
#include "Workspace/HEPHYCommonTools/interface/StringTools.h"
#include <algorithm>
#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h"

using namespace std;

void ModelParameters::lheMSUGRA ( const std::string & t )
{
  size_t foundLength = t.size();
  size_t found = t.find("msugra");
  // size_t found_ = t.find("_");
  /*
  cout << "[ModelParameters] interpreting ``"<< t << "'' as an MSUGRA model string"
       << endl;
  cout << "                  msugra=" << found << " _=" << found_ << endl;
  */

  std::string smaller = t.substr(found+1,foundLength);
  // std::string mmodel = t.substr(found,found_-found);
  found = smaller.find("_");
  smaller = smaller.substr(found+1,smaller.size());

  std::istringstream iss(smaller);
  double m0;
  iss >> m0;
  iss.clear();
  //
  found = smaller.find("_");
  smaller = smaller.substr(found+1,smaller.size());
  iss.str(smaller);
  double m12;
  iss >> m12;
  iss.clear();
  //
  found = smaller.find("_");
  smaller = smaller.substr(found+1,smaller.size());
  iss.str(smaller);
  double tanb;
  iss >> tanb;
  iss.clear();
  found = smaller.find("_");
  smaller = smaller.substr(found+1,smaller.size());
  iss.str(smaller);
  double A0;
  iss >> A0;
  iss.clear();
  found = smaller.find("_");
  smaller = smaller.substr(found+1,smaller.size());
  iss.str(smaller);
  double mu;
  iss >> mu;
  iss.clear();

  defaults_["m0"]=m0;
  defaults_["m12"]=m12;
  defaults_["tanbeta"]=tanb;
  defaults_["a0"]=A0;
  defaults_["mu"]= mu;

  /*
  cout << "[ModelParameters] here we go: " << endl
       << "                  m0=" << m0 << " m12=" << m12
       << " tanb=" << tanb << " A0=" << A0 << " mu=" << mu << endl;
       */

  if ( !isfinite ( m0 ) || !isfinite (m12 ) || !isfinite(tanb) || !isfinite(A0) || 
       !isfinite ( mu ) )
  {
    cout << "[ModelParameters] sth went wrong with the parsing of the comment line"
         << endl
         << "                  m0=" << m0 << " m12=" << m12
         << " tanb=" << tanb << " A0=" << A0 << " mu=" << mu << endl;
  }
}

void ModelParameters::lheSMS ( const std::string & t )
{
  if (debug_)  cout << "[ModelParameters::lheSMS] start" << endl;
  size_t foundLength = t.size();
  size_t found = t.find("T");
  size_t found_ = t.find("_");

  if (debug_)
  {
    cout << "[ModelParameters] interpreting ``"<< t << "'' as an SMS model string"
         << endl;
  }

  std::string smaller = t.substr(found+1,foundLength);
  std::string mmodel = t.substr(found,found_-found);
  found = smaller.find("_");
  smaller = smaller.substr(found+1,smaller.size());

  std::istringstream iss(smaller);
  double xCHI;
  iss >> xCHI;
  iss.clear();
  //
  found = smaller.find("_");
  smaller = smaller.substr(found+1,smaller.size());
  iss.str(smaller);
  double mGL;
  iss >> mGL;
  iss.clear();
  double mSQ=mGL;
  //
  found = smaller.find("_");
  smaller = smaller.substr(found+1,smaller.size());
  iss.str(smaller);
  double mLSP;
  iss >> mLSP;
  iss.clear();
  
  float mchi=xCHI * mLSP + ( 1. - xCHI ) * mGL;

  if ( mmodel == "T2" || mmodel=="T2tt" )
  {
    mLSP = mGL;
    mGL = xCHI;
    xCHI=0.;
    mchi=0.;
  }

  if ( mmodel.substr(0,3) == "TMM" )
  {
    mLSP = mGL;
    mGL = xCHI;
    mSQ = xCHI;
    xCHI=0.;
    mchi=mLSP+70.;
  }

  if ( mmodel == "TGQ" )
  {
    mSQ=mLSP;
    mLSP=xCHI*mSQ;
    mchi=0.;
  }

  if ( mmodel == "T1tttt" )
  { 
    mGL = xCHI;
    mSQ = 0.;
    mchi = 0.;
    xCHI = 0.;
  }
  if ( mmodel == "T1tt1" )
  { 
    mGL = 1000.;
    mSQ = xCHI;
    mchi = 0.;
    xCHI = 0.;
  }
  if ( mmodel == "T5tttt" )
  { 
    mGL = xCHI;
    mchi = 0.;
    xCHI=0.;
  }
  if ( mmodel.substr(0,6) == "T6bbzz" )
  { 
    mGL = 0.;
    mSQ = xCHI;
    mchi = 0.;
    xCHI = 0.;
  }

  defaults_["mgl"]=mGL;
  defaults_["msq"]=mSQ;
  defaults_["mn"]=mLSP;
  defaults_["xfrac"]=xCHI;
  defaults_["mc"]= mchi;
  if (debug_)
  {
    cout << "[ModelParameters] ==> gluino " << mGL 
         << " squark " << mSQ << " mc " << mchi 
         << " LSP " << mLSP  << " xFrac "<< xCHI << endl;
    if ( !isfinite ( mGL ) || !isfinite (mLSP ) || !isfinite(xCHI) )
    {
      cout << "[ModelParameters] sth went wrong with the parsing of the comment line"
           << endl
           << "                  mgl=" << mGL << " mlsp=" << mLSP
           << " mchi=" << mchi << endl;
    }
    cout << "[ModelParameters::lheSMS] end" << endl;
  }
}

void ModelParameters::lhe ( const edm::Event & iEvent )
{
  defaults_.clear();
  if (debug_) cout << "[ModelParameters::lhe] start" << endl;

  ////{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}
  ///// Filter MC truth
  ////{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}

  edm::Handle<LHEEventProduct> product;
  iEvent.getByLabel("source", product);

  if ( !(product.isValid()) )
  {
    cout << "[ModelParameters] couldnt retrieve product!" << endl;
    cout << "[ModelParameters::lhe] end" << endl;
    return;
  }

  LHEEventProduct::comments_const_iterator c_begin = product->comments_begin();
  LHEEventProduct::comments_const_iterator c_end = product->comments_end();

  for( LHEEventProduct::comments_const_iterator cit=c_begin; cit!=c_end; ++cit)
  {
    // cout << "[ModelParameters] cit=" << *cit << endl;
    size_t found = (*cit).find("model");
    if ( found == std::string::npos) continue;
    //# model T2_275.0_175.0
    //# model T5zz_0.5_925.0_400.0to1000.0_450.0.lhe
    //# model TGQ_0.2_600.0_525.0
    //# model msugra_620_280_10_0_1
    found = (*cit).find("msugra");
    if ( found != string::npos )
    {
     lheMSUGRA ( *cit );
     if (debug_) cout << "[ModelParameters::lhe] end" << endl;
     return;
    }
    found = (*cit).find("T");
    if ( found != string::npos )
    {
     lheSMS ( *cit );
     if (debug_) cout << "[ModelParameters::lhe] end" << endl;
     return;
    }
  }
  if (debug_) cout << "[ModelParameters::lhe] end" << endl;
}

void ModelParameters::setData ( bool d )
{
  data_ = d;
}

void ModelParameters::init()
{
  data_=false;
  lhe_=false;
  aliases_["mlsp"]="mn";
  aliases_["mchi+"]="mc";
  aliases_["mchi"]="mc";
  aliases_["mg"]="mgl";
  aliases_["mq"]="msq";
  aliases_["tanb"]="tanbeta";
  aliases_["signmu"]="mu";
  aliases_["sgnmu"]="mu";

  productNames_["mn"]=vector < string > ();
  productNames_["mn"].push_back ( "osetParameters:MLSP" );
  productNames_["mn"].push_back ( "scanParameters:MCHI10" );
  productNames_["mn"].push_back ( "susyScanMLSP" );

  productNames_["mc"]=vector < string > ();
  productNames_["mc"].push_back ( "osetParameters:MChi2" );
  productNames_["mc"].push_back ( "scanParameters:MCHI1P" );
  productNames_["mc"].push_back ( "susyScanMCH" );

  productNames_["mgl"]=vector < string > ();
  productNames_["mgl"].push_back ( "osetParameters:MGL" );
  productNames_["mgl"].push_back ( "scanParameters:MGLUINO" );
  productNames_["mgl"].push_back ( "scanParameters:MGL" );
  productNames_["mgl"].push_back ( "susyScanMG" );

  productNames_["msq"]=vector < string > ();
  productNames_["msq"].push_back ( "osetParameters:MSQ" );
  productNames_["msq"].push_back ( "scanParameters:MSQUARK" );
  productNames_["msq"].push_back ( "susyScanMQ" );
  productNames_["msq"].push_back ( "susyScanMG" );

  productNames_["tanbeta"]=vector < string > ();
  productNames_["tanbeta"].push_back ( "susyScantanbeta" );
  productNames_["m0"]=vector < string > ();
  productNames_["m0"].push_back ( "susyScanM0" );
  productNames_["m12"]=vector < string > ();
  productNames_["m12"].push_back ( "susyScanM12" );
  productNames_["a0"]=vector < string > ();
  productNames_["a0"].push_back ( "susyScanA0" );
  productNames_["mu"]=vector < string > ();
  productNames_["mu"].push_back ( "susyScanMu" );
  productNames_["xsec"]=vector < string > ();
  productNames_["xsec"].push_back ( "susyScanCrossSection" );
  productNames_["run"]=vector < string > ();
  productNames_["run"].push_back ( "susyScanRun" );
  productNames_["type"]=vector < string > ();
  productNames_["type"].push_back ( "susyScanOsetType" );
  productNames_["type"].push_back ( "osetParameters:jobId" );
  productNames_["type"].push_back ( "scanParameters:jobId" );
  isInt_["susyScanOsetType"]=true;
  isInt_["osetParameters:jobId"]=true;

}

ModelParameters::ModelParameters( ) : data_ ( false ),
  checkOnce_ ( true ), debug_ ( false )
{
  init();
}

ModelParameters::ModelParameters( const edm::ParameterSet & defaults ) :
  data_ ( false ), checkOnce_ ( true ), debug_ ( false )
{
  init();
  define ( defaults );
}

void ModelParameters::define ( const edm::ParameterSet & defaults )
{
  debug_ = defaults.getUntrackedParameter<bool>("verbose");
  vector < string > defs=defaults.getParameterNames();
  for ( vector< string >::const_iterator i=defs.begin();
        i!=defs.end() ; ++i )
  {
    string name=(*i);
    if ( aliases_.count(name)!=0 )
    {
      name=aliases_[*i];
    }
    if ( productNames_.count(name)==0 )
    {
      /* cout << "[ModelParameters] error, we have an unrecognized parameter in"
        << " our config: " << name << endl; */
    } else {
      try {
        defaults_[name]=defaults.getUntrackedParameter<double>(name);
      } catch ( ... ) {
        cout << "[ModelParameters] couldnt retrieve parameter " << name
             << "from config. maybe it's not a double?" << endl;
      }
    }
  }
}

double ModelParameters::get( std::string name, const edm::Event & ev )
{
  if ( checkOnce_ )
  {
    // check once for the presence of LHEEventProduct
    edm::Handle<LHEEventProduct> product;
    ev.getByLabel("source", product);
    lhe_=product.isValid();
    checkOnce_=false;
  }

  if ( lhe_ )
  {
    lhe ( ev );
    transform ( name.begin(), name.end(),  name.begin(), ::tolower );
    if ( aliases_.count ( name ) )
    {
      name=aliases_[name];
    }
    if ( defaults_.count ( name ) )
    {
      return defaults_[name];
    }
  }

  if ( data_ ) return NAN;
  transform ( name.begin(), name.end(),  name.begin(), ::tolower );
  if ( aliases_.count ( name ) )
  {
    name=aliases_[name];
  }

  if ( productNames_[name].size() == 0 )
  {
    cout << "[ModelParameters] error: " << name << " is unknown." << endl;
    cout << "[ModelParameters] I know:";
    for ( map < string, vector < string > >::const_iterator i=
        productNames_.begin(); i!=productNames_.end() ; ++i )
    {
      cout << " " << i->first;
    }
    cout << endl;
    return NAN;
  }

  vector < string > prods=productNames_[name];

  for ( vector< string >::const_iterator i=prods.begin(); i!=prods.end(); i++ )
  {
    list < string > parts = StringTools::msplit ( (*i), ":" );
    if (isInt_[name])
    {
      edm::Handle<int> handle;
      if ( parts.size() < 2 )
        ev.getByLabel( (*i), handle );
      else
        ev.getByLabel( *(parts.begin()), *(parts.rbegin()), handle );
      if ( handle.isValid() )
      {
        return (double) (*handle);
      }
    } else {
      edm::Handle<double> handle;
      if ( parts.size() < 2 )
        ev.getByLabel( (*i), handle );
      else
        ev.getByLabel( *(parts.begin()), *(parts.rbegin()), handle );
      if ( handle.isValid() )
      {
        return (*handle);
      }
    }
  }

  if ( defaults_.count(name) ) return defaults_[name];
  return NAN;
}

