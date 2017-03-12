#include <math.h>
#include <vector>
#include "TBranch.h"
#include "TLeaf.h"

double deltaPhi(double phi1 = 0, double phi2 = 0)
{
  double dphi;

  dphi = phi2 - phi1;
  if (dphi > M_PI)
    {
        dphi -= 2.0*M_PI ;
    }
  if (dphi <= -M_PI)
    {
    dphi += 2.0*M_PI    ;
    }
  return dphi;
}

double deltaR2(double eta1 = 0, double eta2 = 0, double phi1 = 0, double phi2 = 0)
{
  double deta, deta2, dphi, dphi2;
  deta = eta2 - eta1;
  deta2 = deta*deta;
 
  dphi  = deltaPhi(phi1, phi2);
  dphi2 = dphi*dphi;
  
  return dphi2+deta2;
}

double deltaR(double eta1 = 0, double eta2 = 0, double phi1 = 0, double phi2 = 0)
{
  double deta, deta2, dphi, dphi2;
  deta = eta2 - eta1;
  deta2 = deta*deta;
 
  dphi  = deltaPhi(phi1, phi2);
  dphi2 = dphi*dphi;
  
  return sqrt(dphi2+deta2);
}

float testCol(TLeaf *obj)
{
  return obj->GetValue(0); 
}
