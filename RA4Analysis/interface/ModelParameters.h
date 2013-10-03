#ifndef Workspace_RA4Analysis_ModelParameters_H
#define Workspace_RA4Analysis_ModelParameters_H

#include <string>
#include <vector>
#include <map>
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

class ModelParameters
{
public:
  /** simple class that encapsulates retrieval of model parameters
   *  from the event files, hiding different naming conventions,
   *  in e.g. Sanjay's versus Ed' scans. Additionally -- if
   *  no information is kept in the event files,
   *  the values can also be configured via the config file.
   */
  ModelParameters( const edm::ParameterSet & defaults );
  void define ( const edm::ParameterSet & defaults );

  /** dont specify defaults 
   */ 
  ModelParameters();
  
  /** get the value of <name>, known parameters are:
   *  m0, m12, tanb, a0, signmu
   *  mgl, msq, mc, mn
   *  case doesnt matter, a few alternative spellings
   *  are recognized */
  double get ( std::string name, const edm::Event & );

  /** set to real data mode (return NAN for everything)
   */
  void setData ( bool d=true );

private:
  void init();
  void lhe ( const edm::Event & );
  void lheSMS ( const std::string & );
  void lheMSUGRA ( const std::string & );
  
  /// if it's real data, we set this to true, and make sure
  /// everything returns NAN
  bool data_; 
  bool lhe_;
  bool checkOnce_;
  bool debug_;

  std::map < std::string, double > defaults_;
  std::map < std::string, std::vector 
    < std::string > > productNames_;
  std::map < std::string, std::string > aliases_;
  std::map < std::string, bool > isInt_;
};

#endif
