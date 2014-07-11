#ifndef Workspace_EarlyDataAnalysis_Tupelizer_H
#define Workspace_EarlyDataAnalysis_Tupelizer_H

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/FWLite/interface/Handle.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/ServiceRegistry/interface/Service.h"


#include "TNtuple.h"
#include "TTree.h"
#include <vector>
#include <typeinfo>
#include <string>

class Tupelizer : public edm::EDProducer
{
public:
  std::vector<std::string> variables;
//  std::map<std::string, void *>     defaultObjects;
  std::map<std::string, std::string>  types;
//  std::map<std::string, bool> hasbeenWritten;
  std::string moduleLabel_;
  bool defaultAlias_;

  void addVar(const std::string & name) {
    std::string varname = name;
    std::string tname = name;
    std::size_t spos = varname.find('/');
    varname.resize(spos);
    variables.push_back(varname);
    std::string fullvarname("");
    if (defaultAlias_) {
      fullvarname = varname;
    } else {
      fullvarname = moduleLabel_+"_"+varname;
    }
    tname.replace(0, spos+1, "");
    types[varname] = tname; 
//    std::cout<<"Varname "<<varname<<" tname "<<tname<<std::endl;
    if (tname.find("[]")!=std::string::npos) {
      switch (tname.at(0)) {
              case 'B' : {produces<std::vector<Char_t> >(varname)    .setBranchAlias(fullvarname); break;}
              case 'b' : {produces<std::vector<UChar_t> >(varname)   .setBranchAlias(fullvarname); break;}
              case 'S' : {produces<std::vector<Short_t> >(varname)   .setBranchAlias(fullvarname); break;}
              case 's' : {produces<std::vector<UShort_t> >(varname)  .setBranchAlias(fullvarname); break;}
              case 'I' : {produces<std::vector<Int_t> >(varname)     .setBranchAlias(fullvarname); break;}
              case 'i' : {produces<std::vector<UInt_t> >(varname)    .setBranchAlias(fullvarname); break;}
              case 'F' : {produces<std::vector<Float_t> >(varname)   .setBranchAlias(fullvarname); break;}
              case 'D' : {produces<std::vector<Double_t> >(varname)  .setBranchAlias(fullvarname); break;}
              case 'L' : {produces<std::vector<Long64_t> >(varname)  .setBranchAlias(fullvarname); break;}
              case 'l' : {produces<std::vector<ULong64_t> >(varname) .setBranchAlias(fullvarname); break;}
              case 'O' : {produces<std::vector<Bool_t> >(varname)    .setBranchAlias(fullvarname); break;}
      }
    } else {
      switch (tname.at(0)) {
              case 'B' : {produces<Char_t>(varname)    .setBranchAlias(fullvarname); break;}
              case 'b' : {produces<UChar_t>(varname)   .setBranchAlias(fullvarname); break;}
              case 'S' : {produces<Short_t>(varname)   .setBranchAlias(fullvarname); break;}
              case 's' : {produces<UShort_t>(varname)  .setBranchAlias(fullvarname); break;}
              case 'I' : {produces<Int_t>(varname)     .setBranchAlias(fullvarname); break;}
              case 'i' : {produces<UInt_t>(varname)    .setBranchAlias(fullvarname); break;}
              case 'F' : {produces<Float_t>(varname)   .setBranchAlias(fullvarname); break;}
              case 'D' : {produces<Double_t>(varname)  .setBranchAlias(fullvarname); break;}
              case 'L' : {produces<Long64_t>(varname)  .setBranchAlias(fullvarname); break;}
              case 'l' : {produces<ULong64_t>(varname) .setBranchAlias(fullvarname); break;}
              case 'O' : {produces<Bool_t>(varname)    .setBranchAlias(fullvarname); break;}
      }
    }
  }
 

  template < class U > 
  void putVar(const std::string & name, U value) {
//    std::cout<<"Name: "<<name<<" typePtr: "<<defaultTypes[name]<<std::endl;
//    dynamic_cast<defaultTypes[name]>
    std::auto_ptr<U> myvar( new U );
    *myvar = value;
//    std::type_info const * mytype (defaultTypes[name]);
//    dynamic_cast<mytype> (&value);
    ev_->put<U>(myvar, name);
//    hasbeenWritten[name] = true;
  }
//  template < class U > 
//  void putVar(const std::string & name, std::vector<U> value) {
//    std::auto_ptr<U> myvar( new std::vector<U> );
//    *myvar = value;
//    ev_->put<std::vector<U> >(myvar, name);
//  }
  template <class U>  
  void put (const std::string & name, std::vector< U > & values) {
    if (types[name].find("[]")!=std::string::npos) {
        putVar<std::vector<U> >(name, values);   
    } else {
      std::cout<<"[Tupelizer] Warning! Var:" << name<<"  Type "<<types[name]<<" can't be filled with std::vector<> !"<<std::endl;
    }
  }

  template < class T > 
  void put (const std::string & name, T value) {
    try {
      switch (types[name].at(0)) {
              case 'B' : {putVar<Char_t>(name, value);    break;}
              case 'b' : {putVar<UChar_t>(name, value);   break;}
              case 'S' : {putVar<Short_t>(name, value);   break;}
              case 's' : {putVar<UShort_t>(name, value);  break;}
              case 'I' : {putVar<Int_t>(name, value);     break;}
              case 'i' : {putVar<UInt_t>(name, value);    break;}
              case 'F' : {putVar<Float_t>(name, value);   break;}
              case 'D' : {putVar<Double_t>(name, value);  break;}
              case 'L' : {putVar<Long64_t>(name, value);  break;}
              case 'l' : {putVar<ULong64_t>(name, value); break;}
              case 'O' : {putVar<Bool_t>(name, value);    break;}
      }
    } catch (cms::Exception & e) {
        std::cout  << "[Tupelizer] Error in put() for variable "<<name<<" (forgot the addVar?) with type "<<types[name]<< e.what() << std::endl;
    }

  }

  explicit Tupelizer( const edm::ParameterSet & pset):
  moduleLabel_( pset.getParameter<std::string>("@module_label") ),
  defaultAlias_(pset.getUntrackedParameter<bool>("useForDefaultAlias"))
  {};

//  ~Tupelizer();

protected:
  edm::Event * ev_; 

};
#endif

