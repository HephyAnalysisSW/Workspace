#include "Workspace/HEPHYCommonTools/interface/StringTools.h"
#include <cmath>
#include <iostream>

using namespace std;

int StringTools::number_quotes ( const string & src, string::size_type pos )
{
  int ret=0;
  // how many quotes until pos?
  pos = src.size() < pos ? src.size() : pos;
  for ( unsigned i=0; i< pos ; i++ )
  {
    if ( src[i]=='\"' )
    {
      if ( i == 0 || src[i-1]!='\\' ) ret++;
    }
  }
  return ret;
}

string::size_type StringTools::find_unescaped( const string & src, const string & sub )
{
  /* cout << "[StringTools] find_unescaped >>" << src << "<< sub >>" << sub << "<<"
       << endl; */
  // before doing fancy stuff we look simply, globally
  string::size_type pos = src.find ( sub );
  // we didnt find anything? lets return here?
  if ( pos == string::npos ) return pos;
  
  pos=0;
  // walk the string WHILE finding escaped....
  do
  {
     pos = src.find( sub, pos );
     if ( pos==string::npos )  break;
     //cout << "[find_unescaped]: found pos " << pos << endl;
     if( pos > 0 && src[pos-1] == '\\' )
     {
       pos++;
       //cout << "escaped !!!" << endl;
       continue;
     };

     // also ignore if number of quotes is odd. (i.e. if it is quoted)
     int n_quotes = number_quotes ( src, pos );
     if ( fmod ( n_quotes, (float) 2. ) > 0.001 )
     {
       pos++;
       continue;
     }
     else
       break;
  }
  while( pos != string::npos );

  // cout << "[StringTools] return: " << (int) pos << endl;
  return pos;
}

list< string > StringTools::msplit( string source, string sep )
{
  /* cout << "[StringTools] split " << source << " >>" << sep << "<<"
       << endl; */
  list< string > ret;
  string::size_type foundpos(0);
  const string::size_type sep_size( sep.size());
  unsigned int found = 0;

  while( (foundpos = find_unescaped( source, sep )) !=
      string::npos )
  {
    string sub = source.substr( 0, foundpos );
    //cout << __FUNCTION__ << ": " << sub << endl;
    if( sub.size() )
    {
      found++;
      ret.push_back( sub );
    }
    source.replace( 0, foundpos + sep_size, "" );
    // quit splitting if required times have been done
  };
  if( source.size() )
    ret.push_back( source );

  // cout << "[StringTools] /split " << ret.size() << endl;
  return ret;
}
