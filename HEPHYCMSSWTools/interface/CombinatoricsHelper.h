#ifndef HEPHYCMSSWTools_CombinatoricsHelper_H
#define HEPHYCMSSWTools_CombinatoricsHelper_H

#include "Workspace/HEPHYCMSSWTools/interface/combination.h"
#include "Workspace/HEPHYCMSSWTools/interface/MathHelper.h"
#include "DataFormats/PatCandidates/interface/Particle.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include <vector>

namespace CombinatoricsHelper
{
  using namespace std;
  /**
   *  small helpers for recurrent reco/combinatorics tasks
   */

  /**
   * template function for filling combinations: returns a vector with all n-element-combinations 
   * (each combination being a vector again).
   */
  template <class S, class T, class U>
  vector< S > join (const vector< T > & v1, const vector< U > & v2)
  {
    vector <S> res;
    for (typename vector<T>::const_iterator it = v1.begin();it!=v1.end();it++) res.push_back(*it);
    for (typename vector<U>::const_iterator it = v2.begin();it!=v2.end();it++) res.push_back(*it);
    return res;
  }


  template<class S, class T, class U>
  void join( const vector<const T*>& v1, const vector<const U*>& v2, vector<const S*>& res )
  {
    for ( typename vector<const T*>::const_iterator it = v1.begin(); it!=v1.end(); ++it ) res.push_back(*it);
    for ( typename vector<const U*>::const_iterator it = v2.begin(); it!=v2.end(); ++it ) res.push_back(*it);
  }


  template <class T>
  vector< vector<T> > makeCombinations( const vector< T > & _vec, unsigned n, bool verbose = false)
  {
    vector< T > vec = _vec;
    vector<vector<  T  > > res;
    if (vec.size() < n) return res;
    vector< T > comb;
    for (unsigned i=0;i<n;i++) comb.push_back(vec[i]);
    do {
      res.push_back(comb);
    } while ( stdcomb::next_combination(vec.begin(),vec.end(),comb.begin(),comb.end()) );

    if (verbose) { 
      string prefix = "[CombinatoricsHelper::makeCombinations] ";
      cout<<prefix<<"got "<< vec.size() << " jets and found "<<res.size()<<" combinations" <<endl;
      for (unsigned i=0;i<res.size();i++)
        cout<<prefix<<"Combination "<<i<<" has size "<< res[i].size()<<endl;
    }
    return res;
  }


  template <class T, class Func>
  vector< vector<  T  > > makeCombinations( const vector< T > & _vec, unsigned n, Func func, bool verbose = false){
    vector< T > vec = _vec;
    vector<vector<  T  > > res;
    if (vec.size() < n) return res;
    vector< T > comb;
    for (unsigned i=0;i<n;i++) comb.push_back(vec[i]);
    do {
      res.push_back(comb);
    } while ( stdcomb::next_combination(vec.begin(),vec.end(),comb.begin(),comb.end(), func) );

    if (verbose) { 
      string prefix = "[CombinatoricsHelper::makeCombinations] ";
      cout<<prefix<<"got "<< vec.size() << " jets and found "<<res.size()<<" combinations" <<endl;
      for (unsigned i=0;i<res.size();i++)
	cout<<prefix<<"Combination "<<i<<" has size "<< res[i].size()<<endl;
    }
    return res;
  }


  /**template for finding the position(s) of a (vector of) element(s) in a vector w.r.t a functor*/
  template <class T, class Func>
  vector< int > getPos( const vector< T > & _vec1, const vector< T > & _vec2, Func func, bool verbose = false){
    vector< int > res;
    for (typename vector< T >::const_iterator it = _vec2.begin();it!=_vec2.end();it++) res.push_back(getPos(_vec1, *it, func, verbose));
    if (verbose) {
      string prefix="[CombinatoricsHelper::getPos] ";
      cout<<prefix<<"got "<<_vec2.size()<<" elements to look for in "<<_vec1.size()<<" elements."<<endl;
      if (true) for ( vector< int >::const_iterator it = res.begin();it!=res.end();it++) 
		  cout<<prefix<<"found element "<<it - res.begin()<<" in pos. "<< *it<<endl;
    }
    return res;
  }


  template <class T, class Func>
  int getPos( const vector< T > & _vec, const T element, Func func, bool verbose = false){
    int res = -1;
    for (typename vector< T >::const_iterator it = _vec.begin();it!=_vec.end();it++) {
      if (func(*it, element)) {
	res=it - _vec.begin();
	break;
      }
    }
    return res;
  }


  /*
   * returns a vector<T> with elements of v1 not in v2 according to eq.
   */
  template <class T, class U>
  vector<T> complement(const vector<T> & v1, const vector<U> & v2)
  {
    vector<T> res;
    MathHelper::samep4 eq;
    for (typename vector<T>::const_iterator it1 = v1.begin();it1!=v1.end();it1++) {
      bool it1_is_in_v2 = false;
      for (typename vector<U>::const_iterator it2 = v2.begin();it2!=v2.end();it2++)
	if (eq(*it1,*it2)) it1_is_in_v2 = true;
      if (!it1_is_in_v2) res.push_back(*it1);
    }
    return res;
  }


  template <class T, class U>
  vector<const T*> complement(const vector<const T*> & v1, const vector<const U*> & v2) {
    vector<const T*> res;
    MathHelper::samep4 eq;
    for (typename vector<const T*>::const_iterator it1 = v1.begin();it1!=v1.end();++it1) {
      bool it1_is_in_v2 = false;
      for (typename vector<const U*>::const_iterator it2 = v2.begin();it2!=v2.end();it2++)
	if (eq(*it1,*it2)) it1_is_in_v2 = true;
      if (!it1_is_in_v2) res.push_back(*it1);
    }
    return res;
  }


  template<class Func, class T>
  void getLeading( const vector<const T*>& data, vector<const T*>& res, Func func, unsigned n, bool verbose = false )
  {
    for ( typename vector<const T*>::const_iterator it = data.begin(); it!=data.end(); ++it ) res.push_back(*it);
    sort( res.begin(), res.end(), func );

    if ( res.size() >= n )
    {
      res.erase( res.begin()+n, res.end() );
      if (verbose) cout<<"[getLeading]: take "<<n<<" objects from a total of " << data.size()<<endl;
    }
    else if (verbose) cout<<"[getLeading]: warning: not enough objs! objs.size(): "<<res.size()<<" n: "<< n <<endl;
  }

}


#endif
