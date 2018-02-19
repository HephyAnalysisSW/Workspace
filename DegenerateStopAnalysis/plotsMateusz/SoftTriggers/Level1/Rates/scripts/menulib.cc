/* automatically generated from L1Menu_Collisions2017_v4_SoftTriggers_v4 with menu2lib.py */
/* https://gitlab.cern.ch/cms-l1t-utm/scripts */

#include <algorithm>
#include <map>
#include <string>
#include <sstream>

#include "menulib.hh"

//
// common functions for algorithm implementations
//
std::pair<double, double>
get_missing_et(L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower,
               const int max_eta,
               const double threshold)
{
  // https://github.com/cms-sw/cmssw/blob/CMSSW_9_0_X/L1Trigger/L1TCalorimeter/src/CaloTools.cc#L13=L15
  const int64_t cos_coeff[72] = {1023, 1019, 1007, 988, 961, 927, 886, 838, 784, 723, 658, 587, 512, 432, 350, 265, 178, 89, 0, -89, -178, -265, -350, -432, -512, -587, -658, -723, -784, -838, -886, -927, -961, -988, -1007, -1019, -1023, -1019, -1007, -988, -961, -927, -886, -838, -784, -723, -658, -587, -512, -432, -350, -265, -178, -89, 0, 89, 178, 265, 350, 432, 511, 587, 658, 723, 784, 838, 886, 927, 961, 988, 1007, 1019};

  const int64_t sin_coeff[72] = {0, 89, 178, 265, 350, 432, 512, 587, 658, 723, 784, 838, 886, 927, 961, 988, 1007, 1019, 1023, 1019, 1007, 988, 961, 927, 886, 838, 784, 723, 658, 587, 512, 432, 350, 265, 178, 89, 0, -89, -178, -265, -350, -432, -512, -587, -658, -723, -784, -838, -886, -927, -961, -988, -1007, -1019, -1023, -1019, -1007, -988, -961, -927, -886, -838, -784, -723, -658, -587, -512, -432, -350, -265, -178, -89};

  if (not calo_tower) return std::make_pair(-1., -9999.);

  double ex = 0.;
  double ey = 0.;

  for (int ii = 0; ii < calo_tower->nTower; ii++)
  {
    if (abs(calo_tower->ieta.at(ii)) <= max_eta)
    {
      const double et = calo_tower->iet.at(ii) * 0.5;
      if (et > threshold)
      {
        const int index = calo_tower->iphi.at(ii) - 1;
        ex += (et*cos_coeff[index]/1024.);
        ey += (et*sin_coeff[index]/1024.);
      }
    }
  }

  return std::make_pair(sqrt(ex*ex + ey*ey), atan2(-ey, -ex));
}


double
get_total_ht(L1Analysis::L1AnalysisL1UpgradeDataFormat* upgrade,
             const int max_eta,
             const double threshold)
{
  double sum = 0.;

  for (int ii = 0; ii < upgrade->nJets; ii++)
  {
    if (upgrade->jetBx.at(ii) != 0) continue;

    if (abs(upgrade->jetIEta.at(ii)) <= 2*max_eta)
    {
      const double et = upgrade->jetEt.at(ii);
      if (et > threshold)
      {
        sum += et;
      }
    }
  }

  return sum;
} 


double
get_transverse_mass(L1Analysis::L1AnalysisL1UpgradeDataFormat* upgrade,
                    const double threshold_eg,
                    const double threshold_met)
{
  double mt = -1.;

  if (upgrade->nEGs == 0) return mt;

  // leading-eg
  int id_leading_eg = -1;
  for (int ii = 0; ii < upgrade->nEGs; ii++)
  {
    if (upgrade->egBx.at(ii) != 0) continue;
    if (id_leading_eg < 0)
    {
      id_leading_eg = ii;
      break;
    }
  }

  if (id_leading_eg < 0) return mt;

  const double eg_et = upgrade->egEt.at(id_leading_eg);
  const double eg_phi = upgrade->egPhi.at(id_leading_eg);

  if (eg_et < threshold_eg) return mt;


  // missing-Et
  int id_missing_et = -1;
  for (int ii = 0; ii < upgrade->nSums; ii++)
  {
    if (upgrade->sumBx.at(ii) != 0) continue;
    if (upgrade->sumType.at(ii) == L1Analysis::kMissingEt)
    {
      id_missing_et = ii;
      break;
    }
  }

  if (id_missing_et < 0) return mt;

  const double met_et = upgrade->sumEt.at(id_missing_et);
  const double met_phi = upgrade->sumPhi.at(id_missing_et);

  if (met_et < threshold_met) return mt;


  // mt
  double delta_phi = eg_phi - met_phi;
  while (delta_phi >= M_PI) delta_phi -= 2.*M_PI;
  while (delta_phi < -M_PI) delta_phi += 2.*M_PI;

  mt = sqrt(2.*eg_et*met_et*(1. - cos(delta_phi)));
  return mt;
}


// utility methods
void
getCombination(int N,
               int K,
               std::vector<std::vector<int> >& combination)
{
  std::string bitmask(K, 1);
  bitmask.resize(N, 0);

  do
  {
    std::vector<int> set;
    for (int ii = 0; ii < N; ++ii)
    {
      if (bitmask[ii]) set.push_back(ii);
    }
    combination.push_back(set);
  }
  while (std::prev_permutation(bitmask.begin(), bitmask.end()));
}


void
getPermutation(int N,
               std::vector<std::vector<int> >& permutation)
{
  std::vector<int> indicies(N);
  for (int ii = 0; ii < N; ii++) indicies.at(ii) = ii;

  do
  {
    std::vector<int> set;
    for (int ii = 0; ii < N; ++ii)
    {
      set.push_back(indicies.at(ii));
    }
    permutation.push_back(set);
  }
  while (std::next_permutation(indicies.begin(), indicies.end()));
}




//
// NB: tmEventSetup.XxxWithOverlapRemoval was removed between utm-overlapRemoval-xsd330 and utm_0.6.5
//
// generate conditions
    




bool
CaloEsumCorrelation_13491612199618123042
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
    bool pass = false;
  size_t nobj = 0;
  
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj++;
          
                                  // JET60: ET >= 120 at BX = 0
      if (not (data->jetIEt.at(ii) >= 120)) continue;

          

    for (size_t jj = 0; jj < data->sumBx.size(); jj++)
    {
      if (not (data->sumType.at(jj) == L1Analysis::kMissingEt)) continue;
      if (not (data->sumBx.at(jj) == 0)) continue;
                          // ETM100: ET >= 200 at BX = 0
      if (not (data->sumIEt.at(jj) >= 200)) continue;
      
          long long minimum;
  long long maximum;
        // 0.4 <= DeltaPhi <= 3.15
      int iPhi = data->sumIPhi.at(jj);
  
  unsigned int deltaIPhi = abs(iPhi - data->jetIPhi.at(ii));
  if (deltaIPhi >= 72) deltaIPhi = 2*72 - deltaIPhi;
      unsigned int deltaPhi = LUT_DPHI_JET_ETM[deltaIPhi];
  
    minimum = (long long)(0.4 * POW10[3]);
  maximum = (long long)(3.15 * POW10[3]);
  if (not ((minimum <= deltaPhi) and (deltaPhi <= maximum))) continue;
    
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      




bool
CaloEsumCorrelation_13491612199685231906
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
    bool pass = false;
  size_t nobj = 0;
  
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj++;
          
                                  // JET60: ET >= 120 at BX = 0
      if (not (data->jetIEt.at(ii) >= 120)) continue;

          

    for (size_t jj = 0; jj < data->sumBx.size(); jj++)
    {
      if (not (data->sumType.at(jj) == L1Analysis::kMissingEt)) continue;
      if (not (data->sumBx.at(jj) == 0)) continue;
                          // ETM110: ET >= 220 at BX = 0
      if (not (data->sumIEt.at(jj) >= 220)) continue;
      
          long long minimum;
  long long maximum;
        // 0.4 <= DeltaPhi <= 3.15
      int iPhi = data->sumIPhi.at(jj);
  
  unsigned int deltaIPhi = abs(iPhi - data->jetIPhi.at(ii));
  if (deltaIPhi >= 72) deltaIPhi = 2*72 - deltaIPhi;
      unsigned int deltaPhi = LUT_DPHI_JET_ETM[deltaIPhi];
  
    minimum = (long long)(0.4 * POW10[3]);
  maximum = (long long)(3.15 * POW10[3]);
  if (not ((minimum <= deltaPhi) and (deltaPhi <= maximum))) continue;
    
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      




bool
CaloEsumCorrelation_16768129600233686289
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
    bool pass = false;
  size_t nobj = 0;
  
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj++;
          
                                  // JET60: ET >= 120 at BX = 0
      if (not (data->jetIEt.at(ii) >= 120)) continue;

          

    for (size_t jj = 0; jj < data->sumBx.size(); jj++)
    {
      if (not (data->sumType.at(jj) == L1Analysis::kMissingEt)) continue;
      if (not (data->sumBx.at(jj) == 0)) continue;
                          // ETM75: ET >= 150 at BX = 0
      if (not (data->sumIEt.at(jj) >= 150)) continue;
      
          long long minimum;
  long long maximum;
        // 0.4 <= DeltaPhi <= 3.15
      int iPhi = data->sumIPhi.at(jj);
  
  unsigned int deltaIPhi = abs(iPhi - data->jetIPhi.at(ii));
  if (deltaIPhi >= 72) deltaIPhi = 2*72 - deltaIPhi;
      unsigned int deltaPhi = LUT_DPHI_JET_ETM[deltaIPhi];
  
    minimum = (long long)(0.4 * POW10[3]);
  maximum = (long long)(3.15 * POW10[3]);
  if (not ((minimum <= deltaPhi) and (deltaPhi <= maximum))) continue;
    
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      




bool
CaloEsumCorrelation_16768129600298173713
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
    bool pass = false;
  size_t nobj = 0;
  
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj++;
          
                                  // JET60: ET >= 120 at BX = 0
      if (not (data->jetIEt.at(ii) >= 120)) continue;

          

    for (size_t jj = 0; jj < data->sumBx.size(); jj++)
    {
      if (not (data->sumType.at(jj) == L1Analysis::kMissingEt)) continue;
      if (not (data->sumBx.at(jj) == 0)) continue;
                          // ETM80: ET >= 160 at BX = 0
      if (not (data->sumIEt.at(jj) >= 160)) continue;
      
          long long minimum;
  long long maximum;
        // 0.4 <= DeltaPhi <= 3.15
      int iPhi = data->sumIPhi.at(jj);
  
  unsigned int deltaIPhi = abs(iPhi - data->jetIPhi.at(ii));
  if (deltaIPhi >= 72) deltaIPhi = 2*72 - deltaIPhi;
      unsigned int deltaPhi = LUT_DPHI_JET_ETM[deltaIPhi];
  
    minimum = (long long)(0.4 * POW10[3]);
  maximum = (long long)(3.15 * POW10[3]);
  if (not ((minimum <= deltaPhi) and (deltaPhi <= maximum))) continue;
    
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      




bool
CaloEsumCorrelation_16768129600365282577
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
    bool pass = false;
  size_t nobj = 0;
  
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj++;
          
                                  // JET60: ET >= 120 at BX = 0
      if (not (data->jetIEt.at(ii) >= 120)) continue;

          

    for (size_t jj = 0; jj < data->sumBx.size(); jj++)
    {
      if (not (data->sumType.at(jj) == L1Analysis::kMissingEt)) continue;
      if (not (data->sumBx.at(jj) == 0)) continue;
                          // ETM90: ET >= 180 at BX = 0
      if (not (data->sumIEt.at(jj) >= 180)) continue;
      
          long long minimum;
  long long maximum;
        // 0.4 <= DeltaPhi <= 3.15
      int iPhi = data->sumIPhi.at(jj);
  
  unsigned int deltaIPhi = abs(iPhi - data->jetIPhi.at(ii));
  if (deltaIPhi >= 72) deltaIPhi = 2*72 - deltaIPhi;
      unsigned int deltaPhi = LUT_DPHI_JET_ETM[deltaIPhi];
  
    minimum = (long long)(0.4 * POW10[3]);
  maximum = (long long)(3.15 * POW10[3]);
  if (not ((minimum <= deltaPhi) and (deltaPhi <= maximum))) continue;
    
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      






bool
CaloMuonCorrelation_15993852977789877467
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
    bool pass = false;
  size_t nobj0 = 0;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj0++;
          
        bool etaWindow1;
                              // JET120: ET >= 240 at BX = 0
      if (not (data->jetIEt.at(ii) >= 240)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(ii)) and (data->jetIEta.at(ii) <= 61));
            
          if (not etaWindow1) continue;
    size_t nobj1 = 0;
    for (size_t jj = 0; jj < data->muonBx.size(); jj++)
    {
      if (not (data->muonBx.at(jj) == 0)) continue;
      nobj1++;
        
                                      // MU3: ET >= 7 at BX = 0
      if (not (data->muonIEt.at(jj) >= 7)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(jj)) & 1)) continue;

          
          long long minimum;
  long long maximum;
    int iEta = -9999999; unsigned int deltaIEta = 9999999;
        // 0.0 <= DeltaPhi <= 0.4
      int iPhi = data->jetIPhi.at(ii);
      iPhi = LUT_PHI_JET2MU[iPhi];
  
  unsigned int deltaIPhi = abs(iPhi - data->muonIPhiAtVtx.at(jj));
  if (deltaIPhi >= 288) deltaIPhi = 2*288 - deltaIPhi;
      unsigned int deltaPhi = LUT_DPHI_JET_MU[deltaIPhi];
  
    minimum = (long long)(0.0 * POW10[3]);
  maximum = (long long)(0.4 * POW10[3]);
  if (not ((minimum <= deltaPhi) and (deltaPhi <= maximum))) continue;

          // 0.0 <= DeltaEta <= 0.4
      iEta = data->jetIEta.at(ii);
      if (iEta < 0) iEta += 256;
    iEta = LUT_ETA_JET2MU[iEta];
    deltaIEta = abs(iEta - data->muonIEtaAtVtx.at(jj));
      unsigned int deltaEta = LUT_DETA_JET_MU[deltaIEta];
  
    minimum = (long long)(0.0 * POW10[3]);
  maximum = (long long)(0.4 * POW10[3]);
  if (not ((minimum <= deltaEta) and (deltaEta <= maximum))) continue;

    
      pass = true;
      break;
    }
    if (pass) break;
  }

  return pass;
}

      






bool
CaloMuonCorrelation_16240387826298544129
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
    bool pass = false;
  size_t nobj0 = 0;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj0++;
          
        bool etaWindow1;
                              // JET16: ET >= 32 at BX = 0
      if (not (data->jetIEt.at(ii) >= 32)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(ii)) and (data->jetIEta.at(ii) <= 61));
            
          if (not etaWindow1) continue;
    size_t nobj1 = 0;
    for (size_t jj = 0; jj < data->muonBx.size(); jj++)
    {
      if (not (data->muonBx.at(jj) == 0)) continue;
      nobj1++;
        
                                      // MU3: ET >= 7 at BX = 0
      if (not (data->muonIEt.at(jj) >= 7)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(jj)) & 1)) continue;

          
          long long minimum;
  long long maximum;
    int iEta = -9999999; unsigned int deltaIEta = 9999999;
        // 0.0 <= DeltaPhi <= 0.4
      int iPhi = data->jetIPhi.at(ii);
      iPhi = LUT_PHI_JET2MU[iPhi];
  
  unsigned int deltaIPhi = abs(iPhi - data->muonIPhiAtVtx.at(jj));
  if (deltaIPhi >= 288) deltaIPhi = 2*288 - deltaIPhi;
      unsigned int deltaPhi = LUT_DPHI_JET_MU[deltaIPhi];
  
    minimum = (long long)(0.0 * POW10[3]);
  maximum = (long long)(0.4 * POW10[3]);
  if (not ((minimum <= deltaPhi) and (deltaPhi <= maximum))) continue;

          // 0.0 <= DeltaEta <= 0.4
      iEta = data->jetIEta.at(ii);
      if (iEta < 0) iEta += 256;
    iEta = LUT_ETA_JET2MU[iEta];
    deltaIEta = abs(iEta - data->muonIEtaAtVtx.at(jj));
      unsigned int deltaEta = LUT_DETA_JET_MU[deltaIEta];
  
    minimum = (long long)(0.0 * POW10[3]);
  maximum = (long long)(0.4 * POW10[3]);
  if (not ((minimum <= deltaEta) and (deltaEta <= maximum))) continue;

    
      pass = true;
      break;
    }
    if (pass) break;
  }

  return pass;
}

      






bool
CaloMuonCorrelation_16240389187803176961
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
    bool pass = false;
  size_t nobj0 = 0;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj0++;
          
        bool etaWindow1;
                              // JET60: ET >= 120 at BX = 0
      if (not (data->jetIEt.at(ii) >= 120)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(ii)) and (data->jetIEta.at(ii) <= 61));
            
          if (not etaWindow1) continue;
    size_t nobj1 = 0;
    for (size_t jj = 0; jj < data->muonBx.size(); jj++)
    {
      if (not (data->muonBx.at(jj) == 0)) continue;
      nobj1++;
        
                                      // MU3: ET >= 7 at BX = 0
      if (not (data->muonIEt.at(jj) >= 7)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(jj)) & 1)) continue;

          
          long long minimum;
  long long maximum;
    int iEta = -9999999; unsigned int deltaIEta = 9999999;
        // 0.0 <= DeltaPhi <= 0.4
      int iPhi = data->jetIPhi.at(ii);
      iPhi = LUT_PHI_JET2MU[iPhi];
  
  unsigned int deltaIPhi = abs(iPhi - data->muonIPhiAtVtx.at(jj));
  if (deltaIPhi >= 288) deltaIPhi = 2*288 - deltaIPhi;
      unsigned int deltaPhi = LUT_DPHI_JET_MU[deltaIPhi];
  
    minimum = (long long)(0.0 * POW10[3]);
  maximum = (long long)(0.4 * POW10[3]);
  if (not ((minimum <= deltaPhi) and (deltaPhi <= maximum))) continue;

          // 0.0 <= DeltaEta <= 0.4
      iEta = data->jetIEta.at(ii);
      if (iEta < 0) iEta += 256;
    iEta = LUT_ETA_JET2MU[iEta];
    deltaIEta = abs(iEta - data->muonIEtaAtVtx.at(jj));
      unsigned int deltaEta = LUT_DETA_JET_MU[deltaIEta];
  
    minimum = (long long)(0.0 * POW10[3]);
  maximum = (long long)(0.4 * POW10[3]);
  if (not ((minimum <= deltaEta) and (deltaEta <= maximum))) continue;

    
      pass = true;
      break;
    }
    if (pass) break;
  }

  return pass;
}

      





bool
MuonMuonCorrelation_5013507948943010765
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
    bool pass = false;
  size_t nobj0 = 0;
  for (size_t ii = 0; ii < data->muonBx.size(); ii++)
  {
    if (not (data->muonBx.at(ii) == -1)) continue;
    nobj0++;
      
        const int idx0 = ii;
    bool etaWindow1;bool phiWindow1;
                              // MU3-1: ET >= 7 at BX = -1
      if (not (data->muonIEt.at(idx0) >= 7)) continue;

                        // -1.2016875 <= eta <= 1.2016875
              etaWindow1 = ((-110 <= data->muonIEtaAtVtx.at(idx0)) and (data->muonIEtaAtVtx.at(idx0) <= 110));
            
                        // 0.523598775598 <= phi <= 2.61799387799
              phiWindow1 = ((48 <= data->muonIPhiAtVtx.at(idx0)) and (data->muonIPhiAtVtx.at(idx0) <= 239));
            
                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx0)) & 1)) continue;

          if (not etaWindow1) continue;if (not phiWindow1) continue;

    size_t nobj1 = 0;
    for (size_t jj = 0; jj < data->muonBx.size(); jj++)
    {
      if (not (data->muonBx.at(jj) == 0)) continue;
      nobj1++;
        
            const int idx1 = jj;
                                // MU3: ET >= 7 at BX = 0
      if (not (data->muonIEt.at(idx1) >= 7)) continue;

                        // -1.2016875 <= eta <= 1.2016875
              etaWindow1 = ((-110 <= data->muonIEtaAtVtx.at(idx1)) and (data->muonIEtaAtVtx.at(idx1) <= 110));
            
                        // 3.66519142919 <= phi <= 5.75958653158
              phiWindow1 = ((336 <= data->muonIPhiAtVtx.at(idx1)) and (data->muonIPhiAtVtx.at(idx1) <= 527));
            
                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx1)) & 1)) continue;

          if (not etaWindow1) continue;if (not phiWindow1) continue;
          long long minimum;
  long long maximum;

  
        // 2.618 <= DeltaPhi <= 3.142
      int iPhi = data->muonIPhiAtVtx.at(idx0);
  
  unsigned int deltaIPhi = abs(iPhi - data->muonIPhiAtVtx.at(idx1));
  if (deltaIPhi >= 288) deltaIPhi = 2*288 - deltaIPhi;
      unsigned int deltaPhi = LUT_DPHI_MU_MU[deltaIPhi];
  
    minimum = (long long)(2.618 * POW10[3]);
  maximum = (long long)(3.142 * POW10[3]);
  if (not ((minimum <= deltaPhi) and (deltaPhi <= maximum))) continue;

    
      pass = true;
      break;
    }
    if (pass) break;
  }

  return pass;
}


      


bool
SingleEG_1139634
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->egBx.size(); ii++)
  {
    if (not (data->egBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // EG2: ET >= 4 at BX = 0
      if (not (data->egIEt.at(idx) >= 4)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      
bool
SingleETMHF_306372248967472
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kMissingEtHF)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // ETMHF20: ET >= 40 at BX = 0
      if (not (data->sumIEt.at(ii) >= 40)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleETMHF_306372248967600
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kMissingEtHF)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // ETMHF30: ET >= 60 at BX = 0
      if (not (data->sumIEt.at(ii) >= 60)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleETMHF_306372248967728
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kMissingEtHF)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // ETMHF40: ET >= 80 at BX = 0
      if (not (data->sumIEt.at(ii) >= 80)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleETMHF_306372248967856
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kMissingEtHF)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // ETMHF50: ET >= 100 at BX = 0
      if (not (data->sumIEt.at(ii) >= 100)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleETMHF_306372248967984
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kMissingEtHF)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // ETMHF60: ET >= 120 at BX = 0
      if (not (data->sumIEt.at(ii) >= 120)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleETMHF_306372248968112
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kMissingEtHF)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // ETMHF70: ET >= 140 at BX = 0
      if (not (data->sumIEt.at(ii) >= 140)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleETMHF_306372248968240
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kMissingEtHF)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // ETMHF80: ET >= 160 at BX = 0
      if (not (data->sumIEt.at(ii) >= 160)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleETMHF_306372248968368
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kMissingEtHF)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // ETMHF90: ET >= 180 at BX = 0
      if (not (data->sumIEt.at(ii) >= 180)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleETMHF_39215647867820080
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kMissingEtHF)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // ETMHF100: ET >= 200 at BX = 0
      if (not (data->sumIEt.at(ii) >= 200)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleETMHF_39215647867820208
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kMissingEtHF)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // ETMHF110: ET >= 220 at BX = 0
      if (not (data->sumIEt.at(ii) >= 220)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleETMHF_39215647867820336
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kMissingEtHF)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // ETMHF120: ET >= 240 at BX = 0
      if (not (data->sumIEt.at(ii) >= 240)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleETMHF_39215647867820720
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kMissingEtHF)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // ETMHF150: ET >= 300 at BX = 0
      if (not (data->sumIEt.at(ii) >= 300)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleETM_18699475376
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kMissingEt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // ETM30: ET >= 60 at BX = 0
      if (not (data->sumIEt.at(ii) >= 60)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleETM_18699475504
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kMissingEt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // ETM40: ET >= 80 at BX = 0
      if (not (data->sumIEt.at(ii) >= 80)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleETM_18699475632
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kMissingEt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // ETM50: ET >= 100 at BX = 0
      if (not (data->sumIEt.at(ii) >= 100)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleETM_18699475760
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kMissingEt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // ETM60: ET >= 120 at BX = 0
      if (not (data->sumIEt.at(ii) >= 120)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleETM_18699475888
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kMissingEt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // ETM70: ET >= 140 at BX = 0
      if (not (data->sumIEt.at(ii) >= 140)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleETM_18699475893
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kMissingEt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // ETM75: ET >= 150 at BX = 0
      if (not (data->sumIEt.at(ii) >= 150)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleETM_18699476016
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kMissingEt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // ETM80: ET >= 160 at BX = 0
      if (not (data->sumIEt.at(ii) >= 160)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleETM_18699476021
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kMissingEt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // ETM85: ET >= 170 at BX = 0
      if (not (data->sumIEt.at(ii) >= 170)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleETM_18699476144
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kMissingEt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // ETM90: ET >= 180 at BX = 0
      if (not (data->sumIEt.at(ii) >= 180)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleETM_18699476149
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kMissingEt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // ETM95: ET >= 190 at BX = 0
      if (not (data->sumIEt.at(ii) >= 190)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleETM_2393532815408
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kMissingEt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // ETM100: ET >= 200 at BX = 0
      if (not (data->sumIEt.at(ii) >= 200)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleETM_2393532815413
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kMissingEt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // ETM105: ET >= 210 at BX = 0
      if (not (data->sumIEt.at(ii) >= 210)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleETM_2393532815536
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kMissingEt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // ETM110: ET >= 220 at BX = 0
      if (not (data->sumIEt.at(ii) >= 220)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleETM_2393532815541
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kMissingEt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // ETM115: ET >= 230 at BX = 0
      if (not (data->sumIEt.at(ii) >= 230)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleETM_2393532815664
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kMissingEt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // ETM120: ET >= 240 at BX = 0
      if (not (data->sumIEt.at(ii) >= 240)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleETM_2393532816048
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kMissingEt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // ETM150: ET >= 300 at BX = 0
      if (not (data->sumIEt.at(ii) >= 300)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleETT_18699590192
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kTotalEt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // ETT40: ET >= 80 at BX = 0
      if (not (data->sumIEt.at(ii) >= 80)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleETT_18699590320
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kTotalEt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // ETT50: ET >= 100 at BX = 0
      if (not (data->sumIEt.at(ii) >= 100)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleETT_18699590448
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kTotalEt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // ETT60: ET >= 120 at BX = 0
      if (not (data->sumIEt.at(ii) >= 120)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleETT_18699590576
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kTotalEt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // ETT70: ET >= 140 at BX = 0
      if (not (data->sumIEt.at(ii) >= 140)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleETT_18699590581
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kTotalEt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // ETT75: ET >= 150 at BX = 0
      if (not (data->sumIEt.at(ii) >= 150)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleETT_18699590704
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kTotalEt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // ETT80: ET >= 160 at BX = 0
      if (not (data->sumIEt.at(ii) >= 160)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleETT_18699590709
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kTotalEt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // ETT85: ET >= 170 at BX = 0
      if (not (data->sumIEt.at(ii) >= 170)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleETT_18699590832
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kTotalEt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // ETT90: ET >= 180 at BX = 0
      if (not (data->sumIEt.at(ii) >= 180)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleETT_18699590837
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kTotalEt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // ETT95: ET >= 190 at BX = 0
      if (not (data->sumIEt.at(ii) >= 190)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleETT_2393547495472
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kTotalEt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // ETT100: ET >= 200 at BX = 0
      if (not (data->sumIEt.at(ii) >= 200)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleETT_2393547495600
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kTotalEt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // ETT110: ET >= 220 at BX = 0
      if (not (data->sumIEt.at(ii) >= 220)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleETT_2393547496240
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kTotalEt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // ETT160: ET >= 320 at BX = 0
      if (not (data->sumIEt.at(ii) >= 320)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleEXT_10333571492674155900
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  // for now return false always
  // could check decision available in ugt data
  bool pass = false;
  return pass;
}

      
bool
SingleEXT_10333571493211026812
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  // for now return false always
  // could check decision available in ugt data
  bool pass = false;
  return pass;
}

      
bool
SingleEXT_10333571493479462268
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  // for now return false always
  // could check decision available in ugt data
  bool pass = false;
  return pass;
}

      
bool
SingleEXT_1189548080491112364
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  // for now return false always
  // could check decision available in ugt data
  bool pass = false;
  return pass;
}

      
bool
SingleEXT_15141600570663550655
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  // for now return false always
  // could check decision available in ugt data
  bool pass = false;
  return pass;
}

      
bool
SingleEXT_16249626042834147010
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  // for now return false always
  // could check decision available in ugt data
  bool pass = false;
  return pass;
}

      
bool
SingleEXT_17417807877912935668
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  // for now return false always
  // could check decision available in ugt data
  bool pass = false;
  return pass;
}

      
bool
SingleEXT_17960169865075597331
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  // for now return false always
  // could check decision available in ugt data
  bool pass = false;
  return pass;
}

      
bool
SingleEXT_4108951444235007726
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  // for now return false always
  // could check decision available in ugt data
  bool pass = false;
  return pass;
}

      
bool
SingleEXT_6102798787913291629
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  // for now return false always
  // could check decision available in ugt data
  bool pass = false;
  return pass;
}

      
bool
SingleEXT_6102798788181727085
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  // for now return false always
  // could check decision available in ugt data
  bool pass = false;
  return pass;
}

      
bool
SingleEXT_6102799243448260461
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  // for now return false always
  // could check decision available in ugt data
  bool pass = false;
  return pass;
}

      
bool
SingleEXT_6909925150529645277
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  // for now return false always
  // could check decision available in ugt data
  bool pass = false;
  return pass;
}

      
bool
SingleEXT_6909925150529645278
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  // for now return false always
  // could check decision available in ugt data
  bool pass = false;
  return pass;
}

      
bool
SingleEXT_6909925150529645533
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  // for now return false always
  // could check decision available in ugt data
  bool pass = false;
  return pass;
}

      
bool
SingleEXT_6909925150529645534
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  // for now return false always
  // could check decision available in ugt data
  bool pass = false;
  return pass;
}

      
bool
SingleEXT_6953200472440552930
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  // for now return false always
  // could check decision available in ugt data
  bool pass = false;
  return pass;
}

      
bool
SingleEXT_866206785869629780
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  // for now return false always
  // could check decision available in ugt data
  bool pass = false;
  return pass;
}

      
bool
SingleEXT_866206786138065236
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  // for now return false always
  // could check decision available in ugt data
  bool pass = false;
  return pass;
}

      
bool
SingleEXT_8736797827952386068
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  // for now return false always
  // could check decision available in ugt data
  bool pass = false;
  return pass;
}

      
bool
SingleEXT_9794008929098471889
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  // for now return false always
  // could check decision available in ugt data
  bool pass = false;
  return pass;
}

      
bool
SingleEXT_9794008929098471890
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  // for now return false always
  // could check decision available in ugt data
  bool pass = false;
  return pass;
}

      
bool
SingleEXT_9794008929098472145
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  // for now return false always
  // could check decision available in ugt data
  bool pass = false;
  return pass;
}

      
bool
SingleEXT_9794008929098472146
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  // for now return false always
  // could check decision available in ugt data
  bool pass = false;
  return pass;
}

      
bool
SingleEXT_9945386644737729380
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  // for now return false always
  // could check decision available in ugt data
  bool pass = false;
  return pass;
}

      
bool
SingleEXT_9945386645006164836
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  // for now return false always
  // could check decision available in ugt data
  bool pass = false;
  return pass;
}

      
bool
SingleEXT_9960888781174681113
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  // for now return false always
  // could check decision available in ugt data
  bool pass = false;
  return pass;
}

      
bool
SingleEXT_9960888781443116569
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  // for now return false always
  // could check decision available in ugt data
  bool pass = false;
  return pass;
}

      
bool
SingleHTM_19504782000
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kMissingHt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // HTM50: ET >= 100 at BX = 0
      if (not (data->sumIEt.at(ii) >= 100)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleHTT_19504896816
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kTotalHt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // HTT60: ET >= 120 at BX = 0
      if (not (data->sumIEt.at(ii) >= 120)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleHTT_2496626710576
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kTotalHt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // HTT100: ET >= 200 at BX = 0
      if (not (data->sumIEt.at(ii) >= 200)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleHTT_2496626710832
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kTotalHt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // HTT120: ET >= 240 at BX = 0
      if (not (data->sumIEt.at(ii) >= 240)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleHTT_2496626711088
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kTotalHt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // HTT140: ET >= 280 at BX = 0
      if (not (data->sumIEt.at(ii) >= 280)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleHTT_2496626711216
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kTotalHt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // HTT150: ET >= 300 at BX = 0
      if (not (data->sumIEt.at(ii) >= 300)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleHTT_2496626711344
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kTotalHt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // HTT160: ET >= 320 at BX = 0
      if (not (data->sumIEt.at(ii) >= 320)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleHTT_2496626711600
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kTotalHt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // HTT180: ET >= 360 at BX = 0
      if (not (data->sumIEt.at(ii) >= 360)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleHTT_2496626726960
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kTotalHt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // HTT200: ET >= 400 at BX = 0
      if (not (data->sumIEt.at(ii) >= 400)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleHTT_2496626727216
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kTotalHt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // HTT220: ET >= 440 at BX = 0
      if (not (data->sumIEt.at(ii) >= 440)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleHTT_2496626727472
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kTotalHt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // HTT240: ET >= 480 at BX = 0
      if (not (data->sumIEt.at(ii) >= 480)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleHTT_2496626727600
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kTotalHt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // HTT250: ET >= 500 at BX = 0
      if (not (data->sumIEt.at(ii) >= 500)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleHTT_2496626727605
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kTotalHt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // HTT255: ET >= 510 at BX = 0
      if (not (data->sumIEt.at(ii) >= 510)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleHTT_2496626727856
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kTotalHt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // HTT270: ET >= 540 at BX = 0
      if (not (data->sumIEt.at(ii) >= 540)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleHTT_2496626727984
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kTotalHt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // HTT280: ET >= 560 at BX = 0
      if (not (data->sumIEt.at(ii) >= 560)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleHTT_2496626743344
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kTotalHt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // HTT300: ET >= 600 at BX = 0
      if (not (data->sumIEt.at(ii) >= 600)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleHTT_2496626743600
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kTotalHt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // HTT320: ET >= 640 at BX = 0
      if (not (data->sumIEt.at(ii) >= 640)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleHTT_2496626743856
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kTotalHt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // HTT340: ET >= 680 at BX = 0
      if (not (data->sumIEt.at(ii) >= 680)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleHTT_2496626744368
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kTotalHt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // HTT380: ET >= 760 at BX = 0
      if (not (data->sumIEt.at(ii) >= 760)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleHTT_2496626759728
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kTotalHt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // HTT400: ET >= 800 at BX = 0
      if (not (data->sumIEt.at(ii) >= 800)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleHTT_2496626760368
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kTotalHt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // HTT450: ET >= 900 at BX = 0
      if (not (data->sumIEt.at(ii) >= 900)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleHTT_2496626776112
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kTotalHt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // HTT500: ET >= 1000 at BX = 0
      if (not (data->sumIEt.at(ii) >= 1000)) continue;
      

    pass = true;
    break;
  }

  return pass;
}

      


bool
SingleJET_13432253330323567498
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET35: ET >= 70 at BX = 0
      if (not (data->jetIEt.at(idx) >= 70)) continue;

                        // -5.0 <= eta <= -3.0015
              etaWindow1 = ((-115 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= -70));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleJET_13432253330327927178
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET35: ET >= 70 at BX = 0
      if (not (data->jetIEt.at(idx) >= 70)) continue;

                        // 3.0015 <= eta <= 5.0
              etaWindow1 = ((69 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 114));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleJET_15014918485909531609
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET100: ET >= 200 at BX = 0
      if (not (data->jetIEt.at(idx) >= 200)) continue;

                        // -2.3925 <= eta <= 2.3925
              etaWindow1 = ((-55 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 54));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleJET_15014918503089400793
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET110: ET >= 220 at BX = 0
      if (not (data->jetIEt.at(idx) >= 220)) continue;

                        // -2.3925 <= eta <= 2.3925
              etaWindow1 = ((-55 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 54));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleJET_15014918520269269977
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET120: ET >= 240 at BX = 0
      if (not (data->jetIEt.at(idx) >= 240)) continue;

                        // -2.3925 <= eta <= 2.3925
              etaWindow1 = ((-55 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 54));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleJET_15873314001121770945
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET35: ET >= 70 at BX = 0
      if (not (data->jetIEt.at(idx) >= 70)) continue;

                        // -5.0 <= eta <= -2.61
              etaWindow1 = ((-115 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= -61));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleJET_15873314001126130625
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET35: ET >= 70 at BX = 0
      if (not (data->jetIEt.at(idx) >= 70)) continue;

                        // 2.61 <= eta <= 5.0
              etaWindow1 = ((60 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 114));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleJET_15873314026556030401
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET60: ET >= 120 at BX = 0
      if (not (data->jetIEt.at(idx) >= 120)) continue;

                        // -5.0 <= eta <= -2.61
              etaWindow1 = ((-115 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= -61));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleJET_15873314026560390081
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET60: ET >= 120 at BX = 0
      if (not (data->jetIEt.at(idx) >= 120)) continue;

                        // 2.61 <= eta <= 5.0
              etaWindow1 = ((60 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 114));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleJET_15873314052325834177
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET90: ET >= 180 at BX = 0
      if (not (data->jetIEt.at(idx) >= 180)) continue;

                        // -5.0 <= eta <= -2.61
              etaWindow1 = ((-115 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= -61));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleJET_15873314052330193857
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET90: ET >= 180 at BX = 0
      if (not (data->jetIEt.at(idx) >= 180)) continue;

                        // 2.61 <= eta <= 5.0
              etaWindow1 = ((60 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 114));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleJET_1950256523785076171
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET120: ET >= 240 at BX = 0
      if (not (data->jetIEt.at(idx) >= 240)) continue;

                        // -5.0 <= eta <= -2.61
              etaWindow1 = ((-115 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= -61));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleJET_1950256523789435851
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET120: ET >= 240 at BX = 0
      if (not (data->jetIEt.at(idx) >= 240)) continue;

                        // 2.61 <= eta <= 5.0
              etaWindow1 = ((60 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 114));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleJET_20010309810
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET12: ET >= 24 at BX = 0
      if (not (data->jetIEt.at(idx) >= 24)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleJET_20010309814
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET16: ET >= 32 at BX = 0
      if (not (data->jetIEt.at(idx) >= 32)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleJET_20010309936
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET20: ET >= 40 at BX = 0
      if (not (data->jetIEt.at(idx) >= 40)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleJET_20010310069
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET35: ET >= 70 at BX = 0
      if (not (data->jetIEt.at(idx) >= 70)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleJET_20010310320
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET50: ET >= 100 at BX = 0
      if (not (data->jetIEt.at(idx) >= 100)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleJET_20010310448
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET60: ET >= 120 at BX = 0
      if (not (data->jetIEt.at(idx) >= 120)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleJET_20010310576
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET70: ET >= 140 at BX = 0
      if (not (data->jetIEt.at(idx) >= 140)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleJET_20010310832
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET90: ET >= 180 at BX = 0
      if (not (data->jetIEt.at(idx) >= 180)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleJET_2561319655472
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET100: ET >= 200 at BX = 0
      if (not (data->jetIEt.at(idx) >= 200)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleJET_2561319655600
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET110: ET >= 220 at BX = 0
      if (not (data->jetIEt.at(idx) >= 220)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleJET_2561319655728
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET120: ET >= 240 at BX = 0
      if (not (data->jetIEt.at(idx) >= 240)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleJET_2561319655984
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET140: ET >= 280 at BX = 0
      if (not (data->jetIEt.at(idx) >= 280)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleJET_2561319656112
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET150: ET >= 300 at BX = 0
      if (not (data->jetIEt.at(idx) >= 300)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleJET_2561319656240
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET160: ET >= 320 at BX = 0
      if (not (data->jetIEt.at(idx) >= 320)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleJET_2561319656368
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET170: ET >= 340 at BX = 0
      if (not (data->jetIEt.at(idx) >= 340)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleJET_2561319656496
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET180: ET >= 360 at BX = 0
      if (not (data->jetIEt.at(idx) >= 360)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleJET_2561319671856
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET200: ET >= 400 at BX = 0
      if (not (data->jetIEt.at(idx) >= 400)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleJET_5967545310209469767
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET24: ET >= 48 at BX = 0
      if (not (data->jetIEt.at(idx) >= 48)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleJET_5967545361212206023
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET50: ET >= 100 at BX = 0
      if (not (data->jetIEt.at(idx) >= 100)) continue;

                        // -2.3925 <= eta <= 2.3925
              etaWindow1 = ((-55 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 54));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleJET_5967545395571944391
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET70: ET >= 140 at BX = 0
      if (not (data->jetIEt.at(idx) >= 140)) continue;

                        // -2.3925 <= eta <= 2.3925
              etaWindow1 = ((-55 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 54));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleJET_5967545429931682759
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET90: ET >= 180 at BX = 0
      if (not (data->jetIEt.at(idx) >= 180)) continue;

                        // -2.3925 <= eta <= 2.3925
              etaWindow1 = ((-55 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 54));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleJET_7529294815024254598
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET30: ET >= 60 at BX = 0
      if (not (data->jetIEt.at(idx) >= 60)) continue;

                        // -2.523 <= eta <= 2.523
              etaWindow1 = ((-58 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 57));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleJET_8640423326801359755
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET60: ET >= 120 at BX = 0
      if (not (data->jetIEt.at(idx) >= 120)) continue;

                        // -5.0 <= eta <= -3.0015
              etaWindow1 = ((-115 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= -70));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleJET_8640423326805719435
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET60: ET >= 120 at BX = 0
      if (not (data->jetIEt.at(idx) >= 120)) continue;

                        // 3.0015 <= eta <= 5.0
              etaWindow1 = ((69 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 114));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      
bool
SingleMBT0HFM_43640316738250417
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kMinBiasHFM0)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // MBT0HFM1: Count >= 1 at BX = 0
      if (not (data->sumIEt.at(ii) >= 1)) continue;
          

    pass = true;
    break;
  }

  return pass;
}

      
bool
SingleMBT0HFP_43640316738250801
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kMinBiasHFP0)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // MBT0HFP1: Count >= 1 at BX = 0
      if (not (data->sumIEt.at(ii) >= 1)) continue;
          

    pass = true;
    break;
  }

  return pass;
}

      


bool
SingleMU_1272496
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->muonBx.size(); ii++)
  {
    if (not (data->muonBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // MU0: ET >= 1 at BX = 0
      if (not (data->muonIEt.at(idx) >= 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleMU_14243093768255232179
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->muonBx.size(); ii++)
  {
    if (not (data->muonBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // MU0: ET >= 1 at BX = 0
      if (not (data->muonIEt.at(idx) >= 1)) continue;

                        // -0.7993125 <= eta <= 0.7993125
              etaWindow1 = ((-73 <= data->muonIEtaAtVtx.at(idx)) and (data->muonIEtaAtVtx.at(idx) <= 73));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleMU_14769293018627052229
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->muonBx.size(); ii++)
  {
    if (not (data->muonBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // MU0: ET >= 1 at BX = 0
      if (not (data->muonIEt.at(idx) >= 1)) continue;

                        // quality : 0xfff0
      if (not ((65520 >> data->muonQual.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleMU_14769293019696632261
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->muonBx.size(); ii++)
  {
    if (not (data->muonBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // MU0: ET >= 1 at BX = 0
      if (not (data->muonIEt.at(idx) >= 1)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleMU_14769293071236239813
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->muonBx.size(); ii++)
  {
    if (not (data->muonBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // MU3: ET >= 7 at BX = 0
      if (not (data->muonIEt.at(idx) >= 7)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleMU_14769293105595978181
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->muonBx.size(); ii++)
  {
    if (not (data->muonBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // MU5: ET >= 11 at BX = 0
      if (not (data->muonIEt.at(idx) >= 11)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleMU_14769293122775847365
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->muonBx.size(); ii++)
  {
    if (not (data->muonBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // MU6: ET >= 13 at BX = 0
      if (not (data->muonIEt.at(idx) >= 13)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleMU_14769293139955716549
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->muonBx.size(); ii++)
  {
    if (not (data->muonBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // MU7: ET >= 15 at BX = 0
      if (not (data->muonIEt.at(idx) >= 15)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleMU_14769293157135585733
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->muonBx.size(); ii++)
  {
    if (not (data->muonBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // MU8: ET >= 17 at BX = 0
      if (not (data->muonIEt.at(idx) >= 17)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleMU_16260934496621930532
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->muonBx.size(); ii++)
  {
    if (not (data->muonBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // MU0: ET >= 1 at BX = 0
      if (not (data->muonIEt.at(idx) >= 1)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx)) & 1)) continue;

                        // -0.7993125 <= eta <= 0.7993125
              etaWindow1 = ((-73 <= data->muonIEtaAtVtx.at(idx)) and (data->muonIEtaAtVtx.at(idx) <= 73));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleMU_17416866089078942815
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->muonBx.size(); ii++)
  {
    if (not (data->muonBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // MU3: ET >= 7 at BX = 0
      if (not (data->muonIEt.at(idx) >= 7)) continue;

                        // -1.5061875 <= eta <= 1.5061875
              etaWindow1 = ((-138 <= data->muonIEtaAtVtx.at(idx)) and (data->muonIEtaAtVtx.at(idx) <= 138));
            
                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx)) & 1)) continue;

          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleMU_17545683111032689093
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->muonBx.size(); ii++)
  {
    if (not (data->muonBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // MU15: ET >= 31 at BX = 0
      if (not (data->muonIEt.at(idx) >= 31)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleMU_17545683128212558277
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->muonBx.size(); ii++)
  {
    if (not (data->muonBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // MU16: ET >= 33 at BX = 0
      if (not (data->muonIEt.at(idx) >= 33)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleMU_17545683162572296645
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->muonBx.size(); ii++)
  {
    if (not (data->muonBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // MU18: ET >= 37 at BX = 0
      if (not (data->muonIEt.at(idx) >= 37)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleMU_17545685224156598725
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->muonBx.size(); ii++)
  {
    if (not (data->muonBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // MU20: ET >= 41 at BX = 0
      if (not (data->muonIEt.at(idx) >= 41)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleMU_17545685258516337093
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->muonBx.size(); ii++)
  {
    if (not (data->muonBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // MU22: ET >= 45 at BX = 0
      if (not (data->muonIEt.at(idx) >= 45)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleMU_17545685310055944645
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->muonBx.size(); ii++)
  {
    if (not (data->muonBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // MU25: ET >= 51 at BX = 0
      if (not (data->muonIEt.at(idx) >= 51)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleMU_17545687423179854277
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->muonBx.size(); ii++)
  {
    if (not (data->muonBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // MU30: ET >= 61 at BX = 0
      if (not (data->muonIEt.at(idx) >= 61)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleMU_5290897791608380091
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->muonBx.size(); ii++)
  {
    if (not (data->muonBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1, etaWindow2;
            idx = candidates.at(set.at(indicies.at(0)));
                                // MU0: ET >= 1 at BX = 0
      if (not (data->muonIEt.at(idx) >= 1)) continue;

                        // 1.2451875 <= eta <= 2.45
              etaWindow1 = ((115 <= data->muonIEtaAtVtx.at(idx)) and (data->muonIEtaAtVtx.at(idx) <= 225));
            
                        // -2.45 <= eta <= -1.2451875
              etaWindow2 = ((-225 <= data->muonIEtaAtVtx.at(idx)) and (data->muonIEtaAtVtx.at(idx) <= -115));
            
          if (not (etaWindow1 or etaWindow2)) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleMU_5982917108635918040
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->muonBx.size(); ii++)
  {
    if (not (data->muonBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // MU3: ET >= 7 at BX = 0
      if (not (data->muonIEt.at(idx) >= 7)) continue;

                        // -2.1043125 <= eta <= 2.1043125
              etaWindow1 = ((-193 <= data->muonIEtaAtVtx.at(idx)) and (data->muonIEtaAtVtx.at(idx) <= 193));
            
                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx)) & 1)) continue;

          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleMU_6011484727103937211
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->muonBx.size(); ii++)
  {
    if (not (data->muonBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1, etaWindow2;
            idx = candidates.at(set.at(indicies.at(0)));
                                // MU0: ET >= 1 at BX = 0
      if (not (data->muonIEt.at(idx) >= 1)) continue;

                        // 0.7993125 <= eta <= 1.2451875
              etaWindow1 = ((74 <= data->muonIEtaAtVtx.at(idx)) and (data->muonIEtaAtVtx.at(idx) <= 114));
            
                        // -1.2451875 <= eta <= -0.7993125
              etaWindow2 = ((-114 <= data->muonIEtaAtVtx.at(idx)) and (data->muonIEtaAtVtx.at(idx) <= -74));
            
          if (not (etaWindow1 or etaWindow2)) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleMU_6225176159725710459
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->muonBx.size(); ii++)
  {
    if (not (data->muonBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1, etaWindow2;
            idx = candidates.at(set.at(indicies.at(0)));
                                // MU0: ET >= 1 at BX = 0
      if (not (data->muonIEt.at(idx) >= 1)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx)) & 1)) continue;

                        // 1.2451875 <= eta <= 2.45
              etaWindow1 = ((115 <= data->muonIEtaAtVtx.at(idx)) and (data->muonIEtaAtVtx.at(idx) <= 225));
            
                        // -2.45 <= eta <= -1.2451875
              etaWindow2 = ((-225 <= data->muonIEtaAtVtx.at(idx)) and (data->muonIEtaAtVtx.at(idx) <= -115));
            
          if (not (etaWindow1 or etaWindow2)) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleMU_6549603580525534936
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->muonBx.size(); ii++)
  {
    if (not (data->muonBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // MU3: ET >= 7 at BX = 0
      if (not (data->muonIEt.at(idx) >= 7)) continue;

                        // -0.7993125 <= eta <= 0.7993125
              etaWindow1 = ((-73 <= data->muonIEtaAtVtx.at(idx)) and (data->muonIEtaAtVtx.at(idx) <= 73));
            
                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx)) & 1)) continue;

          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleMU_6945763095221267579
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->muonBx.size(); ii++)
  {
    if (not (data->muonBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1, etaWindow2;
            idx = candidates.at(set.at(indicies.at(0)));
                                // MU0: ET >= 1 at BX = 0
      if (not (data->muonIEt.at(idx) >= 1)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx)) & 1)) continue;

                        // 0.7993125 <= eta <= 1.2451875
              etaWindow1 = ((74 <= data->muonIEtaAtVtx.at(idx)) and (data->muonIEtaAtVtx.at(idx) <= 114));
            
                        // -1.2451875 <= eta <= -0.7993125
              etaWindow2 = ((-114 <= data->muonIEtaAtVtx.at(idx)) and (data->muonIEtaAtVtx.at(idx) <= -74));
            
          if (not (etaWindow1 or etaWindow2)) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleMU_7037562455545169312
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->muonBx.size(); ii++)
  {
    if (not (data->muonBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // MU10: ET >= 21 at BX = 0
      if (not (data->muonIEt.at(idx) >= 21)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx)) & 1)) continue;

                        // -2.1043125 <= eta <= 2.1043125
              etaWindow1 = ((-193 <= data->muonIEtaAtVtx.at(idx)) and (data->muonIEtaAtVtx.at(idx) <= 193));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleMU_7109620049583097248
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->muonBx.size(); ii++)
  {
    if (not (data->muonBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // MU14: ET >= 29 at BX = 0
      if (not (data->muonIEt.at(idx) >= 29)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx)) & 1)) continue;

                        // -2.1043125 <= eta <= 2.1043125
              etaWindow1 = ((-193 <= data->muonIEtaAtVtx.at(idx)) and (data->muonIEtaAtVtx.at(idx) <= 193));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleMU_8201562577786424033
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->muonBx.size(); ii++)
  {
    if (not (data->muonBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // MU3: ET >= 7 at BX = 0
      if (not (data->muonIEt.at(idx) >= 7)) continue;

                        // charge : negative
      if (not (-1 == data->muonChg.at(idx))) continue;
                    // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleMU_8202147724130831073
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->muonBx.size(); ii++)
  {
    if (not (data->muonBx.at(ii) == 0)) continue;
    nobj++;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 1) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 1, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(1, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // MU3: ET >= 7 at BX = 0
      if (not (data->muonIEt.at(idx) >= 7)) continue;

                        // charge : positive
      if (not (1 == data->muonChg.at(idx))) continue;
                    // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

  

// generate algorithms
bool
L1_AlwaysTrue(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEXT_1189548080491112364(data) or ( not SingleEXT_1189548080491112364(data));
}
bool
L1_BPTX_AND_Ref1_VME(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEXT_10333571492674155900(data);
}
bool
L1_BPTX_AND_Ref3_VME(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEXT_10333571493211026812(data);
}
bool
L1_BPTX_AND_Ref4_VME(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEXT_10333571493479462268(data);
}
bool
L1_BPTX_BeamGas_B1_VME(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEXT_9960888781174681113(data);
}
bool
L1_BPTX_BeamGas_B2_VME(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEXT_9960888781443116569(data);
}
bool
L1_BPTX_BeamGas_Ref1_VME(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEXT_866206785869629780(data);
}
bool
L1_BPTX_BeamGas_Ref2_VME(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEXT_866206786138065236(data);
}
bool
L1_BPTX_NotOR_VME(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEXT_17417807877912935668(data);
}
bool
L1_BPTX_OR_Ref3_VME(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEXT_9945386644737729380(data);
}
bool
L1_BPTX_OR_Ref4_VME(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEXT_9945386645006164836(data);
}
bool
L1_BPTX_RefAND_VME(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEXT_15141600570663550655(data);
}
bool
L1_BptxMinus(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEXT_6102798788181727085(data);
}
bool
L1_BptxOR(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEXT_6102799243448260461(data);
}
bool
L1_BptxPlus(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEXT_6102798787913291629(data);
}
bool
L1_BptxXOR(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return (SingleEXT_6102798787913291629(data) and ( not SingleEXT_6102798788181727085(data))) or (SingleEXT_6102798788181727085(data) and ( not SingleEXT_6102798787913291629(data)));
}
bool
L1_CDC_SingleMu_3_er1p2_TOP120_DPHI2p618_3p142(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return MuonMuonCorrelation_5013507948943010765(data);
}
bool
L1_ETM100(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETM_2393532815408(data);
}
bool
L1_ETM100_Jet60_dPhi_Min0p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return CaloEsumCorrelation_13491612199618123042(data);
}
bool
L1_ETM105(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETM_2393532815413(data);
}
bool
L1_ETM110(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETM_2393532815536(data);
}
bool
L1_ETM110_Jet60_dPhi_Min0p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return CaloEsumCorrelation_13491612199685231906(data);
}
bool
L1_ETM115(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETM_2393532815541(data);
}
bool
L1_ETM120(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETM_2393532815664(data);
}
bool
L1_ETM150(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETM_2393532816048(data);
}
bool
L1_ETM30(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETM_18699475376(data);
}
bool
L1_ETM40(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETM_18699475504(data);
}
bool
L1_ETM50(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETM_18699475632(data);
}
bool
L1_ETM60(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETM_18699475760(data);
}
bool
L1_ETM70(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETM_18699475888(data);
}
bool
L1_ETM75(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETM_18699475893(data);
}
bool
L1_ETM75_Jet60_dPhi_Min0p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return CaloEsumCorrelation_16768129600233686289(data);
}
bool
L1_ETM80(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETM_18699476016(data);
}
bool
L1_ETM80_Jet60_dPhi_Min0p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return CaloEsumCorrelation_16768129600298173713(data);
}
bool
L1_ETM85(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETM_18699476021(data);
}
bool
L1_ETM90(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETM_18699476144(data);
}
bool
L1_ETM90_Jet60_dPhi_Min0p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return CaloEsumCorrelation_16768129600365282577(data);
}
bool
L1_ETM95(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETM_18699476149(data);
}
bool
L1_ETMHF100(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETMHF_39215647867820080(data);
}
bool
L1_ETMHF100_HTT60er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETMHF_39215647867820080(data) and SingleHTT_19504896816(data);
}
bool
L1_ETMHF110(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETMHF_39215647867820208(data);
}
bool
L1_ETMHF110_HTT60er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETMHF_39215647867820208(data) and SingleHTT_19504896816(data);
}
bool
L1_ETMHF120(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETMHF_39215647867820336(data);
}
bool
L1_ETMHF120_HTT60er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETMHF_39215647867820336(data) and SingleHTT_19504896816(data);
}
bool
L1_ETMHF150(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETMHF_39215647867820720(data);
}
bool
L1_ETMHF70(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETMHF_306372248968112(data);
}
bool
L1_ETMHF70_HTT180er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETMHF_306372248968112(data) and SingleHTT_2496626711600(data);
}
bool
L1_ETMHF70_SingleJet90(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETMHF_306372248968112(data) and SingleJET_20010310832(data);
}
bool
L1_ETMHF80(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETMHF_306372248968240(data);
}
bool
L1_ETMHF80_HTT60er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETMHF_306372248968240(data) and SingleHTT_19504896816(data);
}
bool
L1_ETMHF90(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETMHF_306372248968368(data);
}
bool
L1_ETMHF90_HTT60er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETMHF_306372248968368(data) and SingleHTT_19504896816(data);
}
bool
L1_ETT100_BptxAND(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETT_2393547495472(data) and SingleEXT_1189548080491112364(data);
}
bool
L1_ETT110_BptxAND(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETT_2393547495600(data) and SingleEXT_1189548080491112364(data);
}
bool
L1_ETT40_BptxAND(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETT_18699590192(data) and SingleEXT_1189548080491112364(data);
}
bool
L1_ETT50_BptxAND(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETT_18699590320(data) and SingleEXT_1189548080491112364(data);
}
bool
L1_ETT60_BptxAND(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETT_18699590448(data) and SingleEXT_1189548080491112364(data);
}
bool
L1_ETT70_BptxAND(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETT_18699590576(data) and SingleEXT_1189548080491112364(data);
}
bool
L1_ETT75_BptxAND(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETT_18699590581(data) and SingleEXT_1189548080491112364(data);
}
bool
L1_ETT80_BptxAND(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETT_18699590704(data) and SingleEXT_1189548080491112364(data);
}
bool
L1_ETT85_BptxAND(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETT_18699590709(data) and SingleEXT_1189548080491112364(data);
}
bool
L1_ETT90_BptxAND(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETT_18699590832(data) and SingleEXT_1189548080491112364(data);
}
bool
L1_ETT95_BptxAND(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETT_18699590837(data) and SingleEXT_1189548080491112364(data);
}
bool
L1_FirstBunchAfterTrain(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEXT_9794008929098472146(data) and SingleEXT_9794008929098472145(data) and ( not SingleEXT_6102799243448260461(data)) and ( not SingleEXT_6909925150529645277(data)) and ( not SingleEXT_6909925150529645278(data));
}
bool
L1_FirstBunchInTrain(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return ( not SingleEXT_6909925150529645534(data)) and ( not SingleEXT_6909925150529645533(data)) and SingleEXT_1189548080491112364(data) and SingleEXT_9794008929098471889(data) and SingleEXT_9794008929098471890(data);
}
bool
L1_FirstCollisionInOrbit(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEXT_4108951444235007726(data);
}
bool
L1_FirstCollisionInTrain(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEXT_16249626042834147010(data);
}
bool
L1_HTT120er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleHTT_2496626710832(data);
}
bool
L1_HTT160er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleHTT_2496626711344(data);
}
bool
L1_HTT200er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleHTT_2496626726960(data);
}
bool
L1_HTT220er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleHTT_2496626727216(data);
}
bool
L1_HTT240er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleHTT_2496626727472(data);
}
bool
L1_HTT255er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleHTT_2496626727605(data);
}
bool
L1_HTT270er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleHTT_2496626727856(data);
}
bool
L1_HTT280er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleHTT_2496626727984(data);
}
bool
L1_HTT300er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleHTT_2496626743344(data);
}
bool
L1_HTT320er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleHTT_2496626743600(data);
}
bool
L1_HTT340er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleHTT_2496626743856(data);
}
bool
L1_HTT380er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleHTT_2496626744368(data);
}
bool
L1_HTT400er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleHTT_2496626759728(data);
}
bool
L1_HTT450er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleHTT_2496626760368(data);
}
bool
L1_HTT500er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleHTT_2496626776112(data);
}
bool
L1_IsolatedBunch(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return ( not SingleEXT_6909925150529645534(data)) and ( not SingleEXT_6909925150529645533(data)) and SingleEXT_1189548080491112364(data) and ( not SingleEXT_6909925150529645277(data)) and ( not SingleEXT_6909925150529645278(data));
}
bool
L1_LastCollisionInTrain(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEXT_6953200472440552930(data);
}
bool
L1_MinimumBiasHF0_AND_BptxAND(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return (SingleMBT0HFP_43640316738250801(data) and SingleMBT0HFM_43640316738250417(data)) and SingleEXT_1189548080491112364(data);
}
bool
L1_MinimumBiasHF0_OR_BptxAND(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return (SingleMBT0HFP_43640316738250801(data) or SingleMBT0HFM_43640316738250417(data)) and SingleEXT_1189548080491112364(data);
}
bool
L1_Mu10er2p1_ETM30(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_7037562455545169312(data) and SingleETM_18699475376(data);
}
bool
L1_Mu14er2p1_ETM30(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_7109620049583097248(data) and SingleETM_18699475376(data);
}
bool
L1_Mu15_HTT100er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17545683111032689093(data) and SingleHTT_2496626710576(data);
}
bool
L1_Mu18_HTT100er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17545683162572296645(data) and SingleHTT_2496626710576(data);
}
bool
L1_Mu18_Jet24er2p7(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17545683162572296645(data) and SingleJET_5967545310209469767(data);
}
bool
L1_Mu3_Jet120er2p7_dEta_Max0p4_dPhi_Max0p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return CaloMuonCorrelation_15993852977789877467(data);
}
bool
L1_Mu3_Jet16er2p7_dEta_Max0p4_dPhi_Max0p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return CaloMuonCorrelation_16240387826298544129(data);
}
bool
L1_Mu3_Jet30er2p5(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleJET_7529294815024254598(data);
}
bool
L1_Mu3_Jet60er2p7_dEta_Max0p4_dPhi_Max0p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return CaloMuonCorrelation_16240389187803176961(data);
}
bool
L1_Mu6_HTT200er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293122775847365(data) and SingleHTT_2496626726960(data);
}
bool
L1_Mu6_HTT240er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293122775847365(data) and SingleHTT_2496626727472(data);
}
bool
L1_Mu6_HTT250er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293122775847365(data) and SingleHTT_2496626727600(data);
}
bool
L1_Mu8_HTT150er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293157135585733(data) and SingleHTT_2496626711216(data);
}
bool
L1_NotBptxOR(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return not SingleEXT_6102799243448260461(data);
}
bool
L1_SingleEG2_BptxAND(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_1139634(data) and SingleEXT_1189548080491112364(data);
}
bool
L1_SingleJet120(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleJET_2561319655728(data);
}
bool
L1_SingleJet120_FWD(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleJET_1950256523785076171(data) or SingleJET_1950256523789435851(data);
}
bool
L1_SingleJet12_BptxAND(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleJET_20010309810(data) and SingleEXT_1189548080491112364(data);
}
bool
L1_SingleJet140(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleJET_2561319655984(data);
}
bool
L1_SingleJet150(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleJET_2561319656112(data);
}
bool
L1_SingleJet16(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleJET_20010309814(data);
}
bool
L1_SingleJet160(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleJET_2561319656240(data);
}
bool
L1_SingleJet170(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleJET_2561319656368(data);
}
bool
L1_SingleJet180(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleJET_2561319656496(data);
}
bool
L1_SingleJet20(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleJET_20010309936(data);
}
bool
L1_SingleJet200(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleJET_2561319671856(data);
}
bool
L1_SingleJet35(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleJET_20010310069(data);
}
bool
L1_SingleJet35_FWD(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleJET_15873314001121770945(data) or SingleJET_15873314001126130625(data);
}
bool
L1_SingleJet35_HFm(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleJET_13432253330323567498(data);
}
bool
L1_SingleJet35_HFp(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleJET_13432253330327927178(data);
}
bool
L1_SingleJet60(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleJET_20010310448(data);
}
bool
L1_SingleJet60_FWD(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleJET_15873314026556030401(data) or SingleJET_15873314026560390081(data);
}
bool
L1_SingleJet60_HFm(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleJET_8640423326801359755(data);
}
bool
L1_SingleJet60_HFp(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleJET_8640423326805719435(data);
}
bool
L1_SingleJet90(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleJET_20010310832(data);
}
bool
L1_SingleJet90_FWD(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleJET_15873314052325834177(data) or SingleJET_15873314052330193857(data);
}
bool
L1_SingleMu0(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293019696632261(data);
}
bool
L1_SingleMu0_BMTF(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_16260934496621930532(data);
}
bool
L1_SingleMu0_EMTF(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_6225176159725710459(data);
}
bool
L1_SingleMu0_OMTF(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_6945763095221267579(data);
}
bool
L1_SingleMu16(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17545683128212558277(data);
}
bool
L1_SingleMu18(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17545683162572296645(data);
}
bool
L1_SingleMu20(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17545685224156598725(data);
}
bool
L1_SingleMu22(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17545685258516337093(data);
}
bool
L1_SingleMu25(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17545685310055944645(data);
}
bool
L1_SingleMu3(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data);
}
bool
L1_SingleMu30(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17545687423179854277(data);
}
bool
L1_SingleMu3Neg(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_8201562577786424033(data);
}
bool
L1_SingleMu3Neg_ETMHF50_SingleJet70(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_8201562577786424033(data) and SingleETMHF_306372248967856(data) and SingleJET_20010310576(data);
}
bool
L1_SingleMu3Neg_ETMHF50_SingleJet90(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_8201562577786424033(data) and SingleETMHF_306372248967856(data) and SingleJET_20010310832(data);
}
bool
L1_SingleMu3Neg_ETMHF70_SingleJet70(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_8201562577786424033(data) and SingleETMHF_306372248968112(data) and SingleJET_20010310576(data);
}
bool
L1_SingleMu3Neg_ETMHF70_SingleJet90(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_8201562577786424033(data) and SingleETMHF_306372248968112(data) and SingleJET_20010310832(data);
}
bool
L1_SingleMu3Pos(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_8202147724130831073(data);
}
bool
L1_SingleMu3_BMTF(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_6549603580525534936(data);
}
bool
L1_SingleMu3_BMTF_ETMHF20(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_6549603580525534936(data) and SingleETMHF_306372248967472(data);
}
bool
L1_SingleMu3_BMTF_ETMHF20_SingleJet100(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_6549603580525534936(data) and SingleETMHF_306372248967472(data) and SingleJET_2561319655472(data);
}
bool
L1_SingleMu3_BMTF_ETMHF20_SingleJet100er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_6549603580525534936(data) and SingleETMHF_306372248967472(data) and SingleJET_15014918485909531609(data);
}
bool
L1_SingleMu3_BMTF_ETMHF20_SingleJet110(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_6549603580525534936(data) and SingleETMHF_306372248967472(data) and SingleJET_2561319655600(data);
}
bool
L1_SingleMu3_BMTF_ETMHF20_SingleJet110er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_6549603580525534936(data) and SingleETMHF_306372248967472(data) and SingleJET_15014918503089400793(data);
}
bool
L1_SingleMu3_BMTF_ETMHF20_SingleJet120(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_6549603580525534936(data) and SingleETMHF_306372248967472(data) and SingleJET_2561319655728(data);
}
bool
L1_SingleMu3_BMTF_ETMHF20_SingleJet120er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_6549603580525534936(data) and SingleETMHF_306372248967472(data) and SingleJET_15014918520269269977(data);
}
bool
L1_SingleMu3_BMTF_ETMHF20_SingleJet90(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_6549603580525534936(data) and SingleETMHF_306372248967472(data) and SingleJET_20010310832(data);
}
bool
L1_SingleMu3_BMTF_ETMHF20_SingleJet90er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_6549603580525534936(data) and SingleETMHF_306372248967472(data) and SingleJET_5967545429931682759(data);
}
bool
L1_SingleMu3_ETM50(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETM_18699475632(data);
}
bool
L1_SingleMu3_ETM50_HTT160er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETM_18699475632(data) and SingleHTT_2496626711344(data);
}
bool
L1_SingleMu3_ETM50_SingleJet70(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETM_18699475632(data) and SingleJET_20010310576(data);
}
bool
L1_SingleMu3_ETMHF20_SingleJet100(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967472(data) and SingleJET_2561319655472(data);
}
bool
L1_SingleMu3_ETMHF20_SingleJet100er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967472(data) and SingleJET_15014918485909531609(data);
}
bool
L1_SingleMu3_ETMHF20_SingleJet110(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967472(data) and SingleJET_2561319655600(data);
}
bool
L1_SingleMu3_ETMHF20_SingleJet110er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967472(data) and SingleJET_15014918503089400793(data);
}
bool
L1_SingleMu3_ETMHF20_SingleJet120(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967472(data) and SingleJET_2561319655728(data);
}
bool
L1_SingleMu3_ETMHF20_SingleJet120er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967472(data) and SingleJET_15014918520269269977(data);
}
bool
L1_SingleMu3_ETMHF20_SingleJet50(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967472(data) and SingleJET_20010310320(data);
}
bool
L1_SingleMu3_ETMHF20_SingleJet70(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967472(data) and SingleJET_20010310576(data);
}
bool
L1_SingleMu3_ETMHF20_SingleJet90(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967472(data) and SingleJET_20010310832(data);
}
bool
L1_SingleMu3_ETMHF20_SingleJet90er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967472(data) and SingleJET_5967545429931682759(data);
}
bool
L1_SingleMu3_ETMHF30(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967600(data);
}
bool
L1_SingleMu3_ETMHF30_HTT140er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967600(data) and SingleHTT_2496626711088(data);
}
bool
L1_SingleMu3_ETMHF30_HTT160er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967600(data) and SingleHTT_2496626711344(data);
}
bool
L1_SingleMu3_ETMHF30_HTT180er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967600(data) and SingleHTT_2496626711600(data);
}
bool
L1_SingleMu3_ETMHF30_SingleJet100(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967600(data) and SingleJET_2561319655472(data);
}
bool
L1_SingleMu3_ETMHF30_SingleJet100er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967600(data) and SingleJET_15014918485909531609(data);
}
bool
L1_SingleMu3_ETMHF30_SingleJet110(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967600(data) and SingleJET_2561319655600(data);
}
bool
L1_SingleMu3_ETMHF30_SingleJet110er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967600(data) and SingleJET_15014918503089400793(data);
}
bool
L1_SingleMu3_ETMHF30_SingleJet120(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967600(data) and SingleJET_2561319655728(data);
}
bool
L1_SingleMu3_ETMHF30_SingleJet120er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967600(data) and SingleJET_15014918520269269977(data);
}
bool
L1_SingleMu3_ETMHF30_SingleJet50(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967600(data) and SingleJET_20010310320(data);
}
bool
L1_SingleMu3_ETMHF30_SingleJet70(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967600(data) and SingleJET_20010310576(data);
}
bool
L1_SingleMu3_ETMHF30_SingleJet90(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967600(data) and SingleJET_20010310832(data);
}
bool
L1_SingleMu3_ETMHF30_SingleJet90er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967600(data) and SingleJET_5967545429931682759(data);
}
bool
L1_SingleMu3_ETMHF40_SingleJet100(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967728(data) and SingleJET_2561319655472(data);
}
bool
L1_SingleMu3_ETMHF40_SingleJet100er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967728(data) and SingleJET_15014918485909531609(data);
}
bool
L1_SingleMu3_ETMHF40_SingleJet110(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967728(data) and SingleJET_2561319655600(data);
}
bool
L1_SingleMu3_ETMHF40_SingleJet110er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967728(data) and SingleJET_15014918503089400793(data);
}
bool
L1_SingleMu3_ETMHF40_SingleJet120(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967728(data) and SingleJET_2561319655728(data);
}
bool
L1_SingleMu3_ETMHF40_SingleJet120er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967728(data) and SingleJET_15014918520269269977(data);
}
bool
L1_SingleMu3_ETMHF40_SingleJet90(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967728(data) and SingleJET_20010310832(data);
}
bool
L1_SingleMu3_ETMHF40_SingleJet90er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967728(data) and SingleJET_5967545429931682759(data);
}
bool
L1_SingleMu3_ETMHF50(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967856(data);
}
bool
L1_SingleMu3_ETMHF50_ETT160(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967856(data) and SingleETT_2393547496240(data);
}
bool
L1_SingleMu3_ETMHF50_HTT140er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967856(data) and SingleHTT_2496626711088(data);
}
bool
L1_SingleMu3_ETMHF50_HTT160er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967856(data) and SingleHTT_2496626711344(data);
}
bool
L1_SingleMu3_ETMHF50_HTT180er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967856(data) and SingleHTT_2496626711600(data);
}
bool
L1_SingleMu3_ETMHF50_SingleJet100(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967856(data) and SingleJET_2561319655472(data);
}
bool
L1_SingleMu3_ETMHF50_SingleJet100er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967856(data) and SingleJET_15014918485909531609(data);
}
bool
L1_SingleMu3_ETMHF50_SingleJet110(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967856(data) and SingleJET_2561319655600(data);
}
bool
L1_SingleMu3_ETMHF50_SingleJet110er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967856(data) and SingleJET_15014918503089400793(data);
}
bool
L1_SingleMu3_ETMHF50_SingleJet120(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967856(data) and SingleJET_2561319655728(data);
}
bool
L1_SingleMu3_ETMHF50_SingleJet120er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967856(data) and SingleJET_15014918520269269977(data);
}
bool
L1_SingleMu3_ETMHF50_SingleJet50(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967856(data) and SingleJET_20010310320(data);
}
bool
L1_SingleMu3_ETMHF50_SingleJet70(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967856(data) and SingleJET_20010310576(data);
}
bool
L1_SingleMu3_ETMHF50_SingleJet70er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967856(data) and SingleJET_5967545395571944391(data);
}
bool
L1_SingleMu3_ETMHF50_SingleJet90(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967856(data) and SingleJET_20010310832(data);
}
bool
L1_SingleMu3_ETMHF50_SingleJet90er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967856(data) and SingleJET_5967545429931682759(data);
}
bool
L1_SingleMu3_ETMHF60_SingleJet100(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967984(data) and SingleJET_2561319655472(data);
}
bool
L1_SingleMu3_ETMHF60_SingleJet100er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967984(data) and SingleJET_15014918485909531609(data);
}
bool
L1_SingleMu3_ETMHF60_SingleJet110(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967984(data) and SingleJET_2561319655600(data);
}
bool
L1_SingleMu3_ETMHF60_SingleJet110er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967984(data) and SingleJET_15014918503089400793(data);
}
bool
L1_SingleMu3_ETMHF60_SingleJet120(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967984(data) and SingleJET_2561319655728(data);
}
bool
L1_SingleMu3_ETMHF60_SingleJet120er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967984(data) and SingleJET_15014918520269269977(data);
}
bool
L1_SingleMu3_ETMHF60_SingleJet90(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967984(data) and SingleJET_20010310832(data);
}
bool
L1_SingleMu3_ETMHF60_SingleJet90er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248967984(data) and SingleJET_5967545429931682759(data);
}
bool
L1_SingleMu3_ETMHF70(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248968112(data);
}
bool
L1_SingleMu3_ETMHF70_HTT140er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248968112(data) and SingleHTT_2496626711088(data);
}
bool
L1_SingleMu3_ETMHF70_HTT160er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248968112(data) and SingleHTT_2496626711344(data);
}
bool
L1_SingleMu3_ETMHF70_HTT180er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248968112(data) and SingleHTT_2496626711600(data);
}
bool
L1_SingleMu3_ETMHF70_SingleJet50(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248968112(data) and SingleJET_20010310320(data);
}
bool
L1_SingleMu3_ETMHF70_SingleJet70(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248968112(data) and SingleJET_20010310576(data);
}
bool
L1_SingleMu3_ETMHF70_SingleJet70er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248968112(data) and SingleJET_5967545395571944391(data);
}
bool
L1_SingleMu3_ETMHF70_SingleJet90(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248968112(data) and SingleJET_20010310832(data);
}
bool
L1_SingleMu3_ETMHF70_SingleJet90er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleETMHF_306372248968112(data) and SingleJET_5967545429931682759(data);
}
bool
L1_SingleMu3_HTM50(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleHTM_19504782000(data);
}
bool
L1_SingleMu3_HTM50_HTT160er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleHTM_19504782000(data) and SingleHTT_2496626711344(data);
}
bool
L1_SingleMu3_HTM50_SingleJet70(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleHTM_19504782000(data) and SingleJET_20010310576(data);
}
bool
L1_SingleMu3_SingleJet100(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleJET_2561319655472(data);
}
bool
L1_SingleMu3_SingleJet100er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleJET_15014918485909531609(data);
}
bool
L1_SingleMu3_SingleJet110(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleJET_2561319655600(data);
}
bool
L1_SingleMu3_SingleJet110er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleJET_15014918503089400793(data);
}
bool
L1_SingleMu3_SingleJet120(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleJET_2561319655728(data);
}
bool
L1_SingleMu3_SingleJet120er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleJET_15014918520269269977(data);
}
bool
L1_SingleMu3_SingleJet50(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleJET_20010310320(data);
}
bool
L1_SingleMu3_SingleJet50er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleJET_5967545361212206023(data);
}
bool
L1_SingleMu3_SingleJet70(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleJET_20010310576(data);
}
bool
L1_SingleMu3_SingleJet70er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleJET_5967545395571944391(data);
}
bool
L1_SingleMu3_SingleJet90(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleJET_20010310832(data);
}
bool
L1_SingleMu3_SingleJet90er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293071236239813(data) and SingleJET_5967545429931682759(data);
}
bool
L1_SingleMu3er1p5(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17416866089078942815(data);
}
bool
L1_SingleMu3er1p5_ETMHF30(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17416866089078942815(data) and SingleETMHF_306372248967600(data);
}
bool
L1_SingleMu3er1p5_ETMHF30_SingleJet100(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17416866089078942815(data) and SingleETMHF_306372248967600(data) and SingleJET_2561319655472(data);
}
bool
L1_SingleMu3er1p5_ETMHF30_SingleJet100er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17416866089078942815(data) and SingleETMHF_306372248967600(data) and SingleJET_15014918485909531609(data);
}
bool
L1_SingleMu3er1p5_ETMHF30_SingleJet110(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17416866089078942815(data) and SingleETMHF_306372248967600(data) and SingleJET_2561319655600(data);
}
bool
L1_SingleMu3er1p5_ETMHF30_SingleJet110er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17416866089078942815(data) and SingleETMHF_306372248967600(data) and SingleJET_15014918503089400793(data);
}
bool
L1_SingleMu3er1p5_ETMHF30_SingleJet120(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17416866089078942815(data) and SingleETMHF_306372248967600(data) and SingleJET_2561319655728(data);
}
bool
L1_SingleMu3er1p5_ETMHF30_SingleJet120er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17416866089078942815(data) and SingleETMHF_306372248967600(data) and SingleJET_15014918520269269977(data);
}
bool
L1_SingleMu3er1p5_ETMHF30_SingleJet90(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17416866089078942815(data) and SingleETMHF_306372248967600(data) and SingleJET_20010310832(data);
}
bool
L1_SingleMu3er1p5_ETMHF30_SingleJet90er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17416866089078942815(data) and SingleETMHF_306372248967600(data) and SingleJET_5967545429931682759(data);
}
bool
L1_SingleMu3er1p5_ETMHF50(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17416866089078942815(data) and SingleETMHF_306372248967856(data);
}
bool
L1_SingleMu3er1p5_ETMHF50_HTT160er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17416866089078942815(data) and SingleETMHF_306372248967856(data) and SingleHTT_2496626711344(data);
}
bool
L1_SingleMu3er1p5_ETMHF50_SingleJet100(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17416866089078942815(data) and SingleETMHF_306372248967856(data) and SingleJET_2561319655472(data);
}
bool
L1_SingleMu3er1p5_ETMHF50_SingleJet100er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17416866089078942815(data) and SingleETMHF_306372248967856(data) and SingleJET_15014918485909531609(data);
}
bool
L1_SingleMu3er1p5_ETMHF50_SingleJet110(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17416866089078942815(data) and SingleETMHF_306372248967856(data) and SingleJET_2561319655600(data);
}
bool
L1_SingleMu3er1p5_ETMHF50_SingleJet120(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17416866089078942815(data) and SingleETMHF_306372248967856(data) and SingleJET_2561319655728(data);
}
bool
L1_SingleMu3er1p5_ETMHF50_SingleJet70(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17416866089078942815(data) and SingleETMHF_306372248967856(data) and SingleJET_20010310576(data);
}
bool
L1_SingleMu3er1p5_ETMHF50_SingleJet70er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17416866089078942815(data) and SingleETMHF_306372248967856(data) and SingleJET_5967545395571944391(data);
}
bool
L1_SingleMu3er1p5_ETMHF50_SingleJet90(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17416866089078942815(data) and SingleETMHF_306372248967856(data) and SingleJET_20010310832(data);
}
bool
L1_SingleMu3er1p5_ETMHF50_SingleJet90er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17416866089078942815(data) and SingleETMHF_306372248967856(data) and SingleJET_5967545429931682759(data);
}
bool
L1_SingleMu3er1p5_ETMHF70_SingleJet90(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17416866089078942815(data) and SingleETMHF_306372248968112(data) and SingleJET_20010310832(data);
}
bool
L1_SingleMu3er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_5982917108635918040(data);
}
bool
L1_SingleMu3er2p1_ETMHF50(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_5982917108635918040(data) and SingleETMHF_306372248967856(data);
}
bool
L1_SingleMu3er2p1_ETMHF50_HTT160er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_5982917108635918040(data) and SingleETMHF_306372248967856(data) and SingleHTT_2496626711344(data);
}
bool
L1_SingleMu3er2p1_ETMHF50_SingleJet100(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_5982917108635918040(data) and SingleETMHF_306372248967856(data) and SingleJET_2561319655472(data);
}
bool
L1_SingleMu3er2p1_ETMHF50_SingleJet100er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_5982917108635918040(data) and SingleETMHF_306372248967856(data) and SingleJET_15014918485909531609(data);
}
bool
L1_SingleMu3er2p1_ETMHF50_SingleJet110(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_5982917108635918040(data) and SingleETMHF_306372248967856(data) and SingleJET_2561319655600(data);
}
bool
L1_SingleMu3er2p1_ETMHF50_SingleJet110er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_5982917108635918040(data) and SingleETMHF_306372248967856(data) and SingleJET_15014918503089400793(data);
}
bool
L1_SingleMu3er2p1_ETMHF50_SingleJet120(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_5982917108635918040(data) and SingleETMHF_306372248967856(data) and SingleJET_2561319655728(data);
}
bool
L1_SingleMu3er2p1_ETMHF50_SingleJet120er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_5982917108635918040(data) and SingleETMHF_306372248967856(data) and SingleJET_15014918520269269977(data);
}
bool
L1_SingleMu3er2p1_ETMHF50_SingleJet70(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_5982917108635918040(data) and SingleETMHF_306372248967856(data) and SingleJET_20010310576(data);
}
bool
L1_SingleMu3er2p1_ETMHF50_SingleJet70er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_5982917108635918040(data) and SingleETMHF_306372248967856(data) and SingleJET_5967545395571944391(data);
}
bool
L1_SingleMu3er2p1_ETMHF50_SingleJet90(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_5982917108635918040(data) and SingleETMHF_306372248967856(data) and SingleJET_20010310832(data);
}
bool
L1_SingleMu3er2p1_ETMHF50_SingleJet90er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_5982917108635918040(data) and SingleETMHF_306372248967856(data) and SingleJET_5967545429931682759(data);
}
bool
L1_SingleMu3er2p1_ETMHF70_SingleJet90(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_5982917108635918040(data) and SingleETMHF_306372248968112(data) and SingleJET_20010310832(data);
}
bool
L1_SingleMu5(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293105595978181(data);
}
bool
L1_SingleMu7(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293139955716549(data);
}
bool
L1_SingleMuCosmics(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_1272496(data);
}
bool
L1_SingleMuCosmics_BMTF(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14243093768255232179(data);
}
bool
L1_SingleMuCosmics_EMTF(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_5290897791608380091(data);
}
bool
L1_SingleMuCosmics_OMTF(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_6011484727103937211(data);
}
bool
L1_SingleMuOpen(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293018627052229(data);
}
bool
L1_SingleMuOpen_ETMHF50(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293018627052229(data) and SingleETMHF_306372248967856(data);
}
bool
L1_SingleMuOpen_ETMHF50_HTT160er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293018627052229(data) and SingleETMHF_306372248967856(data) and SingleHTT_2496626711344(data);
}
bool
L1_SingleMuOpen_ETMHF50_SingleJet70(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293018627052229(data) and SingleETMHF_306372248967856(data) and SingleJET_20010310576(data);
}
bool
L1_SingleMuOpen_ETMHF50_SingleJet90(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293018627052229(data) and SingleETMHF_306372248967856(data) and SingleJET_20010310832(data);
}
bool
L1_SingleMuOpen_ETMHF70_SingleJet90(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293018627052229(data) and SingleETMHF_306372248968112(data) and SingleJET_20010310832(data);
}
bool
L1_UnpairedBunchBptxMinus(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEXT_8736797827952386068(data);
}
bool
L1_UnpairedBunchBptxPlus(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEXT_17960169865075597331(data);
}
bool
L1_ZeroBias(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEXT_1189548080491112364(data);
}
bool
L1_ZeroBias_copy(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEXT_1189548080491112364(data);
}


std::string getNameFromId(const int index)
{
  static const std::pair<int, std::string> id2name[] = {
          std::make_pair(465, "L1_AlwaysTrue"),          std::make_pair(477, "L1_BPTX_AND_Ref1_VME"),          std::make_pair(481, "L1_BPTX_AND_Ref3_VME"),          std::make_pair(485, "L1_BPTX_AND_Ref4_VME"),          std::make_pair(471, "L1_BPTX_BeamGas_B1_VME"),          std::make_pair(472, "L1_BPTX_BeamGas_B2_VME"),          std::make_pair(469, "L1_BPTX_BeamGas_Ref1_VME"),          std::make_pair(470, "L1_BPTX_BeamGas_Ref2_VME"),          std::make_pair(480, "L1_BPTX_NotOR_VME"),          std::make_pair(482, "L1_BPTX_OR_Ref3_VME"),          std::make_pair(486, "L1_BPTX_OR_Ref4_VME"),          std::make_pair(483, "L1_BPTX_RefAND_VME"),          std::make_pair(475, "L1_BptxMinus"),          std::make_pair(476, "L1_BptxOR"),          std::make_pair(474, "L1_BptxPlus"),          std::make_pair(467, "L1_BptxXOR"),          std::make_pair(504, "L1_CDC_SingleMu_3_er1p2_TOP120_DPHI2p618_3p142"),          std::make_pair(193, "L1_ETM100"),          std::make_pair(273, "L1_ETM100_Jet60_dPhi_Min0p4"),          std::make_pair(194, "L1_ETM105"),          std::make_pair(195, "L1_ETM110"),          std::make_pair(274, "L1_ETM110_Jet60_dPhi_Min0p4"),          std::make_pair(196, "L1_ETM115"),          std::make_pair(197, "L1_ETM120"),          std::make_pair(198, "L1_ETM150"),          std::make_pair(183, "L1_ETM30"),          std::make_pair(184, "L1_ETM40"),          std::make_pair(185, "L1_ETM50"),          std::make_pair(186, "L1_ETM60"),          std::make_pair(187, "L1_ETM70"),          std::make_pair(188, "L1_ETM75"),          std::make_pair(431, "L1_ETM75_Jet60_dPhi_Min0p4"),          std::make_pair(189, "L1_ETM80"),          std::make_pair(271, "L1_ETM80_Jet60_dPhi_Min0p4"),          std::make_pair(190, "L1_ETM85"),          std::make_pair(191, "L1_ETM90"),          std::make_pair(272, "L1_ETM90_Jet60_dPhi_Min0p4"),          std::make_pair(192, "L1_ETM95"),          std::make_pair(202, "L1_ETMHF100"),          std::make_pair(368, "L1_ETMHF100_HTT60er"),          std::make_pair(203, "L1_ETMHF110"),          std::make_pair(369, "L1_ETMHF110_HTT60er"),          std::make_pair(204, "L1_ETMHF120"),          std::make_pair(370, "L1_ETMHF120_HTT60er"),          std::make_pair(205, "L1_ETMHF150"),          std::make_pair(199, "L1_ETMHF70"),          std::make_pair(410, "L1_ETMHF70_HTT180er"),          std::make_pair(407, "L1_ETMHF70_SingleJet90"),          std::make_pair(200, "L1_ETMHF80"),          std::make_pair(366, "L1_ETMHF80_HTT60er"),          std::make_pair(201, "L1_ETMHF90"),          std::make_pair(367, "L1_ETMHF90_HTT60er"),          std::make_pair(457, "L1_ETT100_BptxAND"),          std::make_pair(458, "L1_ETT110_BptxAND"),          std::make_pair(448, "L1_ETT40_BptxAND"),          std::make_pair(449, "L1_ETT50_BptxAND"),          std::make_pair(450, "L1_ETT60_BptxAND"),          std::make_pair(451, "L1_ETT70_BptxAND"),          std::make_pair(452, "L1_ETT75_BptxAND"),          std::make_pair(453, "L1_ETT80_BptxAND"),          std::make_pair(454, "L1_ETT85_BptxAND"),          std::make_pair(455, "L1_ETT90_BptxAND"),          std::make_pair(456, "L1_ETT95_BptxAND"),          std::make_pair(417, "L1_FirstBunchAfterTrain"),          std::make_pair(416, "L1_FirstBunchInTrain"),          std::make_pair(484, "L1_FirstCollisionInOrbit"),          std::make_pair(488, "L1_FirstCollisionInTrain"),          std::make_pair(168, "L1_HTT120er"),          std::make_pair(169, "L1_HTT160er"),          std::make_pair(170, "L1_HTT200er"),          std::make_pair(171, "L1_HTT220er"),          std::make_pair(172, "L1_HTT240er"),          std::make_pair(173, "L1_HTT255er"),          std::make_pair(174, "L1_HTT270er"),          std::make_pair(175, "L1_HTT280er"),          std::make_pair(176, "L1_HTT300er"),          std::make_pair(177, "L1_HTT320er"),          std::make_pair(178, "L1_HTT340er"),          std::make_pair(179, "L1_HTT380er"),          std::make_pair(180, "L1_HTT400er"),          std::make_pair(181, "L1_HTT450er"),          std::make_pair(182, "L1_HTT500er"),          std::make_pair(415, "L1_IsolatedBunch"),          std::make_pair(487, "L1_LastCollisionInTrain"),          std::make_pair(459, "L1_MinimumBiasHF0_AND_BptxAND"),          std::make_pair(460, "L1_MinimumBiasHF0_OR_BptxAND"),          std::make_pair(461, "L1_Mu10er2p1_ETM30"),          std::make_pair(462, "L1_Mu14er2p1_ETM30"),          std::make_pair(317, "L1_Mu15_HTT100er"),          std::make_pair(233, "L1_Mu18_HTT100er"),          std::make_pair(234, "L1_Mu18_Jet24er2p7"),          std::make_pair(445, "L1_Mu3_Jet120er2p7_dEta_Max0p4_dPhi_Max0p4"),          std::make_pair(443, "L1_Mu3_Jet16er2p7_dEta_Max0p4_dPhi_Max0p4"),          std::make_pair(371, "L1_Mu3_Jet30er2p5"),          std::make_pair(444, "L1_Mu3_Jet60er2p7_dEta_Max0p4_dPhi_Max0p4"),          std::make_pair(425, "L1_Mu6_HTT200er"),          std::make_pair(315, "L1_Mu6_HTT240er"),          std::make_pair(316, "L1_Mu6_HTT250er"),          std::make_pair(426, "L1_Mu8_HTT150er"),          std::make_pair(466, "L1_NotBptxOR"),          std::make_pair(446, "L1_SingleEG2_BptxAND"),          std::make_pair(136, "L1_SingleJet120"),          std::make_pair(146, "L1_SingleJet120_FWD"),          std::make_pair(447, "L1_SingleJet12_BptxAND"),          std::make_pair(137, "L1_SingleJet140"),          std::make_pair(138, "L1_SingleJet150"),          std::make_pair(131, "L1_SingleJet16"),          std::make_pair(139, "L1_SingleJet160"),          std::make_pair(140, "L1_SingleJet170"),          std::make_pair(141, "L1_SingleJet180"),          std::make_pair(132, "L1_SingleJet20"),          std::make_pair(142, "L1_SingleJet200"),          std::make_pair(133, "L1_SingleJet35"),          std::make_pair(143, "L1_SingleJet35_FWD"),          std::make_pair(148, "L1_SingleJet35_HFm"),          std::make_pair(147, "L1_SingleJet35_HFp"),          std::make_pair(134, "L1_SingleJet60"),          std::make_pair(144, "L1_SingleJet60_FWD"),          std::make_pair(150, "L1_SingleJet60_HFm"),          std::make_pair(149, "L1_SingleJet60_HFp"),          std::make_pair(135, "L1_SingleJet90"),          std::make_pair(145, "L1_SingleJet90_FWD"),          std::make_pair(46, "L1_SingleMu0"),          std::make_pair(5, "L1_SingleMu0_BMTF"),          std::make_pair(7, "L1_SingleMu0_EMTF"),          std::make_pair(6, "L1_SingleMu0_OMTF"),          std::make_pair(16, "L1_SingleMu16"),          std::make_pair(17, "L1_SingleMu18"),          std::make_pair(18, "L1_SingleMu20"),          std::make_pair(19, "L1_SingleMu22"),          std::make_pair(23, "L1_SingleMu25"),          std::make_pair(8, "L1_SingleMu3"),          std::make_pair(24, "L1_SingleMu30"),          std::make_pair(502, "L1_SingleMu3Neg"),          std::make_pair(114, "L1_SingleMu3Neg_ETMHF50_SingleJet70"),          std::make_pair(160, "L1_SingleMu3Neg_ETMHF50_SingleJet90"),          std::make_pair(159, "L1_SingleMu3Neg_ETMHF70_SingleJet70"),          std::make_pair(161, "L1_SingleMu3Neg_ETMHF70_SingleJet90"),          std::make_pair(503, "L1_SingleMu3Pos"),          std::make_pair(64, "L1_SingleMu3_BMTF"),          std::make_pair(65, "L1_SingleMu3_BMTF_ETMHF20"),          std::make_pair(67, "L1_SingleMu3_BMTF_ETMHF20_SingleJet100"),          std::make_pair(71, "L1_SingleMu3_BMTF_ETMHF20_SingleJet100er2p4"),          std::make_pair(68, "L1_SingleMu3_BMTF_ETMHF20_SingleJet110"),          std::make_pair(72, "L1_SingleMu3_BMTF_ETMHF20_SingleJet110er2p4"),          std::make_pair(69, "L1_SingleMu3_BMTF_ETMHF20_SingleJet120"),          std::make_pair(73, "L1_SingleMu3_BMTF_ETMHF20_SingleJet120er2p4"),          std::make_pair(66, "L1_SingleMu3_BMTF_ETMHF20_SingleJet90"),          std::make_pair(70, "L1_SingleMu3_BMTF_ETMHF20_SingleJet90er2p4"),          std::make_pair(208, "L1_SingleMu3_ETM50"),          std::make_pair(350, "L1_SingleMu3_ETM50_HTT160er"),          std::make_pair(348, "L1_SingleMu3_ETM50_SingleJet70"),          std::make_pair(490, "L1_SingleMu3_ETMHF20_SingleJet100"),          std::make_pair(112, "L1_SingleMu3_ETMHF20_SingleJet100er2p4"),          std::make_pair(13, "L1_SingleMu3_ETMHF20_SingleJet110"),          std::make_pair(14, "L1_SingleMu3_ETMHF20_SingleJet110er2p4"),          std::make_pair(491, "L1_SingleMu3_ETMHF20_SingleJet120"),          std::make_pair(113, "L1_SingleMu3_ETMHF20_SingleJet120er2p4"),          std::make_pair(463, "L1_SingleMu3_ETMHF20_SingleJet50"),          std::make_pair(464, "L1_SingleMu3_ETMHF20_SingleJet70"),          std::make_pair(489, "L1_SingleMu3_ETMHF20_SingleJet90"),          std::make_pair(111, "L1_SingleMu3_ETMHF20_SingleJet90er2p4"),          std::make_pair(47, "L1_SingleMu3_ETMHF30"),          std::make_pair(319, "L1_SingleMu3_ETMHF30_HTT140er"),          std::make_pair(320, "L1_SingleMu3_ETMHF30_HTT160er"),          std::make_pair(321, "L1_SingleMu3_ETMHF30_HTT180er"),          std::make_pair(15, "L1_SingleMu3_ETMHF30_SingleJet100"),          std::make_pair(25, "L1_SingleMu3_ETMHF30_SingleJet100er2p4"),          std::make_pair(20, "L1_SingleMu3_ETMHF30_SingleJet110"),          std::make_pair(26, "L1_SingleMu3_ETMHF30_SingleJet110er2p4"),          std::make_pair(21, "L1_SingleMu3_ETMHF30_SingleJet120"),          std::make_pair(27, "L1_SingleMu3_ETMHF30_SingleJet120er2p4"),          std::make_pair(293, "L1_SingleMu3_ETMHF30_SingleJet50"),          std::make_pair(296, "L1_SingleMu3_ETMHF30_SingleJet70"),          std::make_pair(48, "L1_SingleMu3_ETMHF30_SingleJet90"),          std::make_pair(22, "L1_SingleMu3_ETMHF30_SingleJet90er2p4"),          std::make_pair(29, "L1_SingleMu3_ETMHF40_SingleJet100"),          std::make_pair(33, "L1_SingleMu3_ETMHF40_SingleJet100er2p4"),          std::make_pair(30, "L1_SingleMu3_ETMHF40_SingleJet110"),          std::make_pair(34, "L1_SingleMu3_ETMHF40_SingleJet110er2p4"),          std::make_pair(31, "L1_SingleMu3_ETMHF40_SingleJet120"),          std::make_pair(35, "L1_SingleMu3_ETMHF40_SingleJet120er2p4"),          std::make_pair(28, "L1_SingleMu3_ETMHF40_SingleJet90"),          std::make_pair(32, "L1_SingleMu3_ETMHF40_SingleJet90er2p4"),          std::make_pair(49, "L1_SingleMu3_ETMHF50"),          std::make_pair(414, "L1_SingleMu3_ETMHF50_ETT160"),          std::make_pair(344, "L1_SingleMu3_ETMHF50_HTT140er"),          std::make_pair(346, "L1_SingleMu3_ETMHF50_HTT160er"),          std::make_pair(322, "L1_SingleMu3_ETMHF50_HTT180er"),          std::make_pair(36, "L1_SingleMu3_ETMHF50_SingleJet100"),          std::make_pair(39, "L1_SingleMu3_ETMHF50_SingleJet100er2p4"),          std::make_pair(37, "L1_SingleMu3_ETMHF50_SingleJet110"),          std::make_pair(40, "L1_SingleMu3_ETMHF50_SingleJet110er2p4"),          std::make_pair(38, "L1_SingleMu3_ETMHF50_SingleJet120"),          std::make_pair(41, "L1_SingleMu3_ETMHF50_SingleJet120er2p4"),          std::make_pair(297, "L1_SingleMu3_ETMHF50_SingleJet50"),          std::make_pair(313, "L1_SingleMu3_ETMHF50_SingleJet70"),          std::make_pair(505, "L1_SingleMu3_ETMHF50_SingleJet70er2p4"),          std::make_pair(206, "L1_SingleMu3_ETMHF50_SingleJet90"),          std::make_pair(506, "L1_SingleMu3_ETMHF50_SingleJet90er2p4"),          std::make_pair(43, "L1_SingleMu3_ETMHF60_SingleJet100"),          std::make_pair(51, "L1_SingleMu3_ETMHF60_SingleJet100er2p4"),          std::make_pair(44, "L1_SingleMu3_ETMHF60_SingleJet110"),          std::make_pair(52, "L1_SingleMu3_ETMHF60_SingleJet110er2p4"),          std::make_pair(45, "L1_SingleMu3_ETMHF60_SingleJet120"),          std::make_pair(53, "L1_SingleMu3_ETMHF60_SingleJet120er2p4"),          std::make_pair(42, "L1_SingleMu3_ETMHF60_SingleJet90"),          std::make_pair(50, "L1_SingleMu3_ETMHF60_SingleJet90er2p4"),          std::make_pair(207, "L1_SingleMu3_ETMHF70"),          std::make_pair(345, "L1_SingleMu3_ETMHF70_HTT140er"),          std::make_pair(347, "L1_SingleMu3_ETMHF70_HTT160er"),          std::make_pair(343, "L1_SingleMu3_ETMHF70_HTT180er"),          std::make_pair(298, "L1_SingleMu3_ETMHF70_SingleJet50"),          std::make_pair(314, "L1_SingleMu3_ETMHF70_SingleJet70"),          std::make_pair(507, "L1_SingleMu3_ETMHF70_SingleJet70er2p4"),          std::make_pair(318, "L1_SingleMu3_ETMHF70_SingleJet90"),          std::make_pair(508, "L1_SingleMu3_ETMHF70_SingleJet90er2p4"),          std::make_pair(411, "L1_SingleMu3_HTM50"),          std::make_pair(412, "L1_SingleMu3_HTM50_HTT160er"),          std::make_pair(413, "L1_SingleMu3_HTM50_SingleJet70"),          std::make_pair(437, "L1_SingleMu3_SingleJet100"),          std::make_pair(162, "L1_SingleMu3_SingleJet100er2p4"),          std::make_pair(11, "L1_SingleMu3_SingleJet110"),          std::make_pair(12, "L1_SingleMu3_SingleJet110er2p4"),          std::make_pair(438, "L1_SingleMu3_SingleJet120"),          std::make_pair(163, "L1_SingleMu3_SingleJet120er2p4"),          std::make_pair(209, "L1_SingleMu3_SingleJet50"),          std::make_pair(509, "L1_SingleMu3_SingleJet50er2p4"),          std::make_pair(224, "L1_SingleMu3_SingleJet70"),          std::make_pair(510, "L1_SingleMu3_SingleJet70er2p4"),          std::make_pair(291, "L1_SingleMu3_SingleJet90"),          std::make_pair(511, "L1_SingleMu3_SingleJet90er2p4"),          std::make_pair(354, "L1_SingleMu3er1p5"),          std::make_pair(74, "L1_SingleMu3er1p5_ETMHF30"),          std::make_pair(76, "L1_SingleMu3er1p5_ETMHF30_SingleJet100"),          std::make_pair(80, "L1_SingleMu3er1p5_ETMHF30_SingleJet100er2p4"),          std::make_pair(77, "L1_SingleMu3er1p5_ETMHF30_SingleJet110"),          std::make_pair(81, "L1_SingleMu3er1p5_ETMHF30_SingleJet110er2p4"),          std::make_pair(78, "L1_SingleMu3er1p5_ETMHF30_SingleJet120"),          std::make_pair(82, "L1_SingleMu3er1p5_ETMHF30_SingleJet120er2p4"),          std::make_pair(75, "L1_SingleMu3er1p5_ETMHF30_SingleJet90"),          std::make_pair(79, "L1_SingleMu3er1p5_ETMHF30_SingleJet90er2p4"),          std::make_pair(356, "L1_SingleMu3er1p5_ETMHF50"),          std::make_pair(409, "L1_SingleMu3er1p5_ETMHF50_HTT160er"),          std::make_pair(60, "L1_SingleMu3er1p5_ETMHF50_SingleJet100"),          std::make_pair(63, "L1_SingleMu3er1p5_ETMHF50_SingleJet100er2p4"),          std::make_pair(61, "L1_SingleMu3er1p5_ETMHF50_SingleJet110"),          std::make_pair(62, "L1_SingleMu3er1p5_ETMHF50_SingleJet120"),          std::make_pair(373, "L1_SingleMu3er1p5_ETMHF50_SingleJet70"),          std::make_pair(501, "L1_SingleMu3er1p5_ETMHF50_SingleJet70er2p4"),          std::make_pair(496, "L1_SingleMu3er1p5_ETMHF50_SingleJet90"),          std::make_pair(500, "L1_SingleMu3er1p5_ETMHF50_SingleJet90er2p4"),          std::make_pair(497, "L1_SingleMu3er1p5_ETMHF70_SingleJet90"),          std::make_pair(353, "L1_SingleMu3er2p1"),          std::make_pair(355, "L1_SingleMu3er2p1_ETMHF50"),          std::make_pair(408, "L1_SingleMu3er2p1_ETMHF50_HTT160er"),          std::make_pair(54, "L1_SingleMu3er2p1_ETMHF50_SingleJet100"),          std::make_pair(57, "L1_SingleMu3er2p1_ETMHF50_SingleJet100er2p4"),          std::make_pair(55, "L1_SingleMu3er2p1_ETMHF50_SingleJet110"),          std::make_pair(58, "L1_SingleMu3er2p1_ETMHF50_SingleJet110er2p4"),          std::make_pair(56, "L1_SingleMu3er2p1_ETMHF50_SingleJet120"),          std::make_pair(59, "L1_SingleMu3er2p1_ETMHF50_SingleJet120er2p4"),          std::make_pair(372, "L1_SingleMu3er2p1_ETMHF50_SingleJet70"),          std::make_pair(499, "L1_SingleMu3er2p1_ETMHF50_SingleJet70er2p4"),          std::make_pair(494, "L1_SingleMu3er2p1_ETMHF50_SingleJet90"),          std::make_pair(498, "L1_SingleMu3er2p1_ETMHF50_SingleJet90er2p4"),          std::make_pair(495, "L1_SingleMu3er2p1_ETMHF70_SingleJet90"),          std::make_pair(9, "L1_SingleMu5"),          std::make_pair(10, "L1_SingleMu7"),          std::make_pair(0, "L1_SingleMuCosmics"),          std::make_pair(2, "L1_SingleMuCosmics_BMTF"),          std::make_pair(4, "L1_SingleMuCosmics_EMTF"),          std::make_pair(3, "L1_SingleMuCosmics_OMTF"),          std::make_pair(1, "L1_SingleMuOpen"),          std::make_pair(374, "L1_SingleMuOpen_ETMHF50"),          std::make_pair(351, "L1_SingleMuOpen_ETMHF50_HTT160er"),          std::make_pair(352, "L1_SingleMuOpen_ETMHF50_SingleJet70"),          std::make_pair(492, "L1_SingleMuOpen_ETMHF50_SingleJet90"),          std::make_pair(493, "L1_SingleMuOpen_ETMHF70_SingleJet90"),          std::make_pair(479, "L1_UnpairedBunchBptxMinus"),          std::make_pair(478, "L1_UnpairedBunchBptxPlus"),          std::make_pair(473, "L1_ZeroBias"),          std::make_pair(468, "L1_ZeroBias_copy")      };

  static const std::map<int, std::string> Id2Name(id2name, id2name + sizeof(id2name) / sizeof(id2name[0]));
  const std::map<int, std::string>::const_iterator rc = Id2Name.find(index);
  std::string name;
  if (rc != Id2Name.end()) name = rc->second;
  return name;
}


int getIdFromName(const std::string& name)
{
  static const std::pair<std::string, int> name2id[] = {
          std::make_pair("L1_AlwaysTrue", 465),          std::make_pair("L1_BPTX_AND_Ref1_VME", 477),          std::make_pair("L1_BPTX_AND_Ref3_VME", 481),          std::make_pair("L1_BPTX_AND_Ref4_VME", 485),          std::make_pair("L1_BPTX_BeamGas_B1_VME", 471),          std::make_pair("L1_BPTX_BeamGas_B2_VME", 472),          std::make_pair("L1_BPTX_BeamGas_Ref1_VME", 469),          std::make_pair("L1_BPTX_BeamGas_Ref2_VME", 470),          std::make_pair("L1_BPTX_NotOR_VME", 480),          std::make_pair("L1_BPTX_OR_Ref3_VME", 482),          std::make_pair("L1_BPTX_OR_Ref4_VME", 486),          std::make_pair("L1_BPTX_RefAND_VME", 483),          std::make_pair("L1_BptxMinus", 475),          std::make_pair("L1_BptxOR", 476),          std::make_pair("L1_BptxPlus", 474),          std::make_pair("L1_BptxXOR", 467),          std::make_pair("L1_CDC_SingleMu_3_er1p2_TOP120_DPHI2p618_3p142", 504),          std::make_pair("L1_ETM100", 193),          std::make_pair("L1_ETM100_Jet60_dPhi_Min0p4", 273),          std::make_pair("L1_ETM105", 194),          std::make_pair("L1_ETM110", 195),          std::make_pair("L1_ETM110_Jet60_dPhi_Min0p4", 274),          std::make_pair("L1_ETM115", 196),          std::make_pair("L1_ETM120", 197),          std::make_pair("L1_ETM150", 198),          std::make_pair("L1_ETM30", 183),          std::make_pair("L1_ETM40", 184),          std::make_pair("L1_ETM50", 185),          std::make_pair("L1_ETM60", 186),          std::make_pair("L1_ETM70", 187),          std::make_pair("L1_ETM75", 188),          std::make_pair("L1_ETM75_Jet60_dPhi_Min0p4", 431),          std::make_pair("L1_ETM80", 189),          std::make_pair("L1_ETM80_Jet60_dPhi_Min0p4", 271),          std::make_pair("L1_ETM85", 190),          std::make_pair("L1_ETM90", 191),          std::make_pair("L1_ETM90_Jet60_dPhi_Min0p4", 272),          std::make_pair("L1_ETM95", 192),          std::make_pair("L1_ETMHF100", 202),          std::make_pair("L1_ETMHF100_HTT60er", 368),          std::make_pair("L1_ETMHF110", 203),          std::make_pair("L1_ETMHF110_HTT60er", 369),          std::make_pair("L1_ETMHF120", 204),          std::make_pair("L1_ETMHF120_HTT60er", 370),          std::make_pair("L1_ETMHF150", 205),          std::make_pair("L1_ETMHF70", 199),          std::make_pair("L1_ETMHF70_HTT180er", 410),          std::make_pair("L1_ETMHF70_SingleJet90", 407),          std::make_pair("L1_ETMHF80", 200),          std::make_pair("L1_ETMHF80_HTT60er", 366),          std::make_pair("L1_ETMHF90", 201),          std::make_pair("L1_ETMHF90_HTT60er", 367),          std::make_pair("L1_ETT100_BptxAND", 457),          std::make_pair("L1_ETT110_BptxAND", 458),          std::make_pair("L1_ETT40_BptxAND", 448),          std::make_pair("L1_ETT50_BptxAND", 449),          std::make_pair("L1_ETT60_BptxAND", 450),          std::make_pair("L1_ETT70_BptxAND", 451),          std::make_pair("L1_ETT75_BptxAND", 452),          std::make_pair("L1_ETT80_BptxAND", 453),          std::make_pair("L1_ETT85_BptxAND", 454),          std::make_pair("L1_ETT90_BptxAND", 455),          std::make_pair("L1_ETT95_BptxAND", 456),          std::make_pair("L1_FirstBunchAfterTrain", 417),          std::make_pair("L1_FirstBunchInTrain", 416),          std::make_pair("L1_FirstCollisionInOrbit", 484),          std::make_pair("L1_FirstCollisionInTrain", 488),          std::make_pair("L1_HTT120er", 168),          std::make_pair("L1_HTT160er", 169),          std::make_pair("L1_HTT200er", 170),          std::make_pair("L1_HTT220er", 171),          std::make_pair("L1_HTT240er", 172),          std::make_pair("L1_HTT255er", 173),          std::make_pair("L1_HTT270er", 174),          std::make_pair("L1_HTT280er", 175),          std::make_pair("L1_HTT300er", 176),          std::make_pair("L1_HTT320er", 177),          std::make_pair("L1_HTT340er", 178),          std::make_pair("L1_HTT380er", 179),          std::make_pair("L1_HTT400er", 180),          std::make_pair("L1_HTT450er", 181),          std::make_pair("L1_HTT500er", 182),          std::make_pair("L1_IsolatedBunch", 415),          std::make_pair("L1_LastCollisionInTrain", 487),          std::make_pair("L1_MinimumBiasHF0_AND_BptxAND", 459),          std::make_pair("L1_MinimumBiasHF0_OR_BptxAND", 460),          std::make_pair("L1_Mu10er2p1_ETM30", 461),          std::make_pair("L1_Mu14er2p1_ETM30", 462),          std::make_pair("L1_Mu15_HTT100er", 317),          std::make_pair("L1_Mu18_HTT100er", 233),          std::make_pair("L1_Mu18_Jet24er2p7", 234),          std::make_pair("L1_Mu3_Jet120er2p7_dEta_Max0p4_dPhi_Max0p4", 445),          std::make_pair("L1_Mu3_Jet16er2p7_dEta_Max0p4_dPhi_Max0p4", 443),          std::make_pair("L1_Mu3_Jet30er2p5", 371),          std::make_pair("L1_Mu3_Jet60er2p7_dEta_Max0p4_dPhi_Max0p4", 444),          std::make_pair("L1_Mu6_HTT200er", 425),          std::make_pair("L1_Mu6_HTT240er", 315),          std::make_pair("L1_Mu6_HTT250er", 316),          std::make_pair("L1_Mu8_HTT150er", 426),          std::make_pair("L1_NotBptxOR", 466),          std::make_pair("L1_SingleEG2_BptxAND", 446),          std::make_pair("L1_SingleJet120", 136),          std::make_pair("L1_SingleJet120_FWD", 146),          std::make_pair("L1_SingleJet12_BptxAND", 447),          std::make_pair("L1_SingleJet140", 137),          std::make_pair("L1_SingleJet150", 138),          std::make_pair("L1_SingleJet16", 131),          std::make_pair("L1_SingleJet160", 139),          std::make_pair("L1_SingleJet170", 140),          std::make_pair("L1_SingleJet180", 141),          std::make_pair("L1_SingleJet20", 132),          std::make_pair("L1_SingleJet200", 142),          std::make_pair("L1_SingleJet35", 133),          std::make_pair("L1_SingleJet35_FWD", 143),          std::make_pair("L1_SingleJet35_HFm", 148),          std::make_pair("L1_SingleJet35_HFp", 147),          std::make_pair("L1_SingleJet60", 134),          std::make_pair("L1_SingleJet60_FWD", 144),          std::make_pair("L1_SingleJet60_HFm", 150),          std::make_pair("L1_SingleJet60_HFp", 149),          std::make_pair("L1_SingleJet90", 135),          std::make_pair("L1_SingleJet90_FWD", 145),          std::make_pair("L1_SingleMu0", 46),          std::make_pair("L1_SingleMu0_BMTF", 5),          std::make_pair("L1_SingleMu0_EMTF", 7),          std::make_pair("L1_SingleMu0_OMTF", 6),          std::make_pair("L1_SingleMu16", 16),          std::make_pair("L1_SingleMu18", 17),          std::make_pair("L1_SingleMu20", 18),          std::make_pair("L1_SingleMu22", 19),          std::make_pair("L1_SingleMu25", 23),          std::make_pair("L1_SingleMu3", 8),          std::make_pair("L1_SingleMu30", 24),          std::make_pair("L1_SingleMu3Neg", 502),          std::make_pair("L1_SingleMu3Neg_ETMHF50_SingleJet70", 114),          std::make_pair("L1_SingleMu3Neg_ETMHF50_SingleJet90", 160),          std::make_pair("L1_SingleMu3Neg_ETMHF70_SingleJet70", 159),          std::make_pair("L1_SingleMu3Neg_ETMHF70_SingleJet90", 161),          std::make_pair("L1_SingleMu3Pos", 503),          std::make_pair("L1_SingleMu3_BMTF", 64),          std::make_pair("L1_SingleMu3_BMTF_ETMHF20", 65),          std::make_pair("L1_SingleMu3_BMTF_ETMHF20_SingleJet100", 67),          std::make_pair("L1_SingleMu3_BMTF_ETMHF20_SingleJet100er2p4", 71),          std::make_pair("L1_SingleMu3_BMTF_ETMHF20_SingleJet110", 68),          std::make_pair("L1_SingleMu3_BMTF_ETMHF20_SingleJet110er2p4", 72),          std::make_pair("L1_SingleMu3_BMTF_ETMHF20_SingleJet120", 69),          std::make_pair("L1_SingleMu3_BMTF_ETMHF20_SingleJet120er2p4", 73),          std::make_pair("L1_SingleMu3_BMTF_ETMHF20_SingleJet90", 66),          std::make_pair("L1_SingleMu3_BMTF_ETMHF20_SingleJet90er2p4", 70),          std::make_pair("L1_SingleMu3_ETM50", 208),          std::make_pair("L1_SingleMu3_ETM50_HTT160er", 350),          std::make_pair("L1_SingleMu3_ETM50_SingleJet70", 348),          std::make_pair("L1_SingleMu3_ETMHF20_SingleJet100", 490),          std::make_pair("L1_SingleMu3_ETMHF20_SingleJet100er2p4", 112),          std::make_pair("L1_SingleMu3_ETMHF20_SingleJet110", 13),          std::make_pair("L1_SingleMu3_ETMHF20_SingleJet110er2p4", 14),          std::make_pair("L1_SingleMu3_ETMHF20_SingleJet120", 491),          std::make_pair("L1_SingleMu3_ETMHF20_SingleJet120er2p4", 113),          std::make_pair("L1_SingleMu3_ETMHF20_SingleJet50", 463),          std::make_pair("L1_SingleMu3_ETMHF20_SingleJet70", 464),          std::make_pair("L1_SingleMu3_ETMHF20_SingleJet90", 489),          std::make_pair("L1_SingleMu3_ETMHF20_SingleJet90er2p4", 111),          std::make_pair("L1_SingleMu3_ETMHF30", 47),          std::make_pair("L1_SingleMu3_ETMHF30_HTT140er", 319),          std::make_pair("L1_SingleMu3_ETMHF30_HTT160er", 320),          std::make_pair("L1_SingleMu3_ETMHF30_HTT180er", 321),          std::make_pair("L1_SingleMu3_ETMHF30_SingleJet100", 15),          std::make_pair("L1_SingleMu3_ETMHF30_SingleJet100er2p4", 25),          std::make_pair("L1_SingleMu3_ETMHF30_SingleJet110", 20),          std::make_pair("L1_SingleMu3_ETMHF30_SingleJet110er2p4", 26),          std::make_pair("L1_SingleMu3_ETMHF30_SingleJet120", 21),          std::make_pair("L1_SingleMu3_ETMHF30_SingleJet120er2p4", 27),          std::make_pair("L1_SingleMu3_ETMHF30_SingleJet50", 293),          std::make_pair("L1_SingleMu3_ETMHF30_SingleJet70", 296),          std::make_pair("L1_SingleMu3_ETMHF30_SingleJet90", 48),          std::make_pair("L1_SingleMu3_ETMHF30_SingleJet90er2p4", 22),          std::make_pair("L1_SingleMu3_ETMHF40_SingleJet100", 29),          std::make_pair("L1_SingleMu3_ETMHF40_SingleJet100er2p4", 33),          std::make_pair("L1_SingleMu3_ETMHF40_SingleJet110", 30),          std::make_pair("L1_SingleMu3_ETMHF40_SingleJet110er2p4", 34),          std::make_pair("L1_SingleMu3_ETMHF40_SingleJet120", 31),          std::make_pair("L1_SingleMu3_ETMHF40_SingleJet120er2p4", 35),          std::make_pair("L1_SingleMu3_ETMHF40_SingleJet90", 28),          std::make_pair("L1_SingleMu3_ETMHF40_SingleJet90er2p4", 32),          std::make_pair("L1_SingleMu3_ETMHF50", 49),          std::make_pair("L1_SingleMu3_ETMHF50_ETT160", 414),          std::make_pair("L1_SingleMu3_ETMHF50_HTT140er", 344),          std::make_pair("L1_SingleMu3_ETMHF50_HTT160er", 346),          std::make_pair("L1_SingleMu3_ETMHF50_HTT180er", 322),          std::make_pair("L1_SingleMu3_ETMHF50_SingleJet100", 36),          std::make_pair("L1_SingleMu3_ETMHF50_SingleJet100er2p4", 39),          std::make_pair("L1_SingleMu3_ETMHF50_SingleJet110", 37),          std::make_pair("L1_SingleMu3_ETMHF50_SingleJet110er2p4", 40),          std::make_pair("L1_SingleMu3_ETMHF50_SingleJet120", 38),          std::make_pair("L1_SingleMu3_ETMHF50_SingleJet120er2p4", 41),          std::make_pair("L1_SingleMu3_ETMHF50_SingleJet50", 297),          std::make_pair("L1_SingleMu3_ETMHF50_SingleJet70", 313),          std::make_pair("L1_SingleMu3_ETMHF50_SingleJet70er2p4", 505),          std::make_pair("L1_SingleMu3_ETMHF50_SingleJet90", 206),          std::make_pair("L1_SingleMu3_ETMHF50_SingleJet90er2p4", 506),          std::make_pair("L1_SingleMu3_ETMHF60_SingleJet100", 43),          std::make_pair("L1_SingleMu3_ETMHF60_SingleJet100er2p4", 51),          std::make_pair("L1_SingleMu3_ETMHF60_SingleJet110", 44),          std::make_pair("L1_SingleMu3_ETMHF60_SingleJet110er2p4", 52),          std::make_pair("L1_SingleMu3_ETMHF60_SingleJet120", 45),          std::make_pair("L1_SingleMu3_ETMHF60_SingleJet120er2p4", 53),          std::make_pair("L1_SingleMu3_ETMHF60_SingleJet90", 42),          std::make_pair("L1_SingleMu3_ETMHF60_SingleJet90er2p4", 50),          std::make_pair("L1_SingleMu3_ETMHF70", 207),          std::make_pair("L1_SingleMu3_ETMHF70_HTT140er", 345),          std::make_pair("L1_SingleMu3_ETMHF70_HTT160er", 347),          std::make_pair("L1_SingleMu3_ETMHF70_HTT180er", 343),          std::make_pair("L1_SingleMu3_ETMHF70_SingleJet50", 298),          std::make_pair("L1_SingleMu3_ETMHF70_SingleJet70", 314),          std::make_pair("L1_SingleMu3_ETMHF70_SingleJet70er2p4", 507),          std::make_pair("L1_SingleMu3_ETMHF70_SingleJet90", 318),          std::make_pair("L1_SingleMu3_ETMHF70_SingleJet90er2p4", 508),          std::make_pair("L1_SingleMu3_HTM50", 411),          std::make_pair("L1_SingleMu3_HTM50_HTT160er", 412),          std::make_pair("L1_SingleMu3_HTM50_SingleJet70", 413),          std::make_pair("L1_SingleMu3_SingleJet100", 437),          std::make_pair("L1_SingleMu3_SingleJet100er2p4", 162),          std::make_pair("L1_SingleMu3_SingleJet110", 11),          std::make_pair("L1_SingleMu3_SingleJet110er2p4", 12),          std::make_pair("L1_SingleMu3_SingleJet120", 438),          std::make_pair("L1_SingleMu3_SingleJet120er2p4", 163),          std::make_pair("L1_SingleMu3_SingleJet50", 209),          std::make_pair("L1_SingleMu3_SingleJet50er2p4", 509),          std::make_pair("L1_SingleMu3_SingleJet70", 224),          std::make_pair("L1_SingleMu3_SingleJet70er2p4", 510),          std::make_pair("L1_SingleMu3_SingleJet90", 291),          std::make_pair("L1_SingleMu3_SingleJet90er2p4", 511),          std::make_pair("L1_SingleMu3er1p5", 354),          std::make_pair("L1_SingleMu3er1p5_ETMHF30", 74),          std::make_pair("L1_SingleMu3er1p5_ETMHF30_SingleJet100", 76),          std::make_pair("L1_SingleMu3er1p5_ETMHF30_SingleJet100er2p4", 80),          std::make_pair("L1_SingleMu3er1p5_ETMHF30_SingleJet110", 77),          std::make_pair("L1_SingleMu3er1p5_ETMHF30_SingleJet110er2p4", 81),          std::make_pair("L1_SingleMu3er1p5_ETMHF30_SingleJet120", 78),          std::make_pair("L1_SingleMu3er1p5_ETMHF30_SingleJet120er2p4", 82),          std::make_pair("L1_SingleMu3er1p5_ETMHF30_SingleJet90", 75),          std::make_pair("L1_SingleMu3er1p5_ETMHF30_SingleJet90er2p4", 79),          std::make_pair("L1_SingleMu3er1p5_ETMHF50", 356),          std::make_pair("L1_SingleMu3er1p5_ETMHF50_HTT160er", 409),          std::make_pair("L1_SingleMu3er1p5_ETMHF50_SingleJet100", 60),          std::make_pair("L1_SingleMu3er1p5_ETMHF50_SingleJet100er2p4", 63),          std::make_pair("L1_SingleMu3er1p5_ETMHF50_SingleJet110", 61),          std::make_pair("L1_SingleMu3er1p5_ETMHF50_SingleJet120", 62),          std::make_pair("L1_SingleMu3er1p5_ETMHF50_SingleJet70", 373),          std::make_pair("L1_SingleMu3er1p5_ETMHF50_SingleJet70er2p4", 501),          std::make_pair("L1_SingleMu3er1p5_ETMHF50_SingleJet90", 496),          std::make_pair("L1_SingleMu3er1p5_ETMHF50_SingleJet90er2p4", 500),          std::make_pair("L1_SingleMu3er1p5_ETMHF70_SingleJet90", 497),          std::make_pair("L1_SingleMu3er2p1", 353),          std::make_pair("L1_SingleMu3er2p1_ETMHF50", 355),          std::make_pair("L1_SingleMu3er2p1_ETMHF50_HTT160er", 408),          std::make_pair("L1_SingleMu3er2p1_ETMHF50_SingleJet100", 54),          std::make_pair("L1_SingleMu3er2p1_ETMHF50_SingleJet100er2p4", 57),          std::make_pair("L1_SingleMu3er2p1_ETMHF50_SingleJet110", 55),          std::make_pair("L1_SingleMu3er2p1_ETMHF50_SingleJet110er2p4", 58),          std::make_pair("L1_SingleMu3er2p1_ETMHF50_SingleJet120", 56),          std::make_pair("L1_SingleMu3er2p1_ETMHF50_SingleJet120er2p4", 59),          std::make_pair("L1_SingleMu3er2p1_ETMHF50_SingleJet70", 372),          std::make_pair("L1_SingleMu3er2p1_ETMHF50_SingleJet70er2p4", 499),          std::make_pair("L1_SingleMu3er2p1_ETMHF50_SingleJet90", 494),          std::make_pair("L1_SingleMu3er2p1_ETMHF50_SingleJet90er2p4", 498),          std::make_pair("L1_SingleMu3er2p1_ETMHF70_SingleJet90", 495),          std::make_pair("L1_SingleMu5", 9),          std::make_pair("L1_SingleMu7", 10),          std::make_pair("L1_SingleMuCosmics", 0),          std::make_pair("L1_SingleMuCosmics_BMTF", 2),          std::make_pair("L1_SingleMuCosmics_EMTF", 4),          std::make_pair("L1_SingleMuCosmics_OMTF", 3),          std::make_pair("L1_SingleMuOpen", 1),          std::make_pair("L1_SingleMuOpen_ETMHF50", 374),          std::make_pair("L1_SingleMuOpen_ETMHF50_HTT160er", 351),          std::make_pair("L1_SingleMuOpen_ETMHF50_SingleJet70", 352),          std::make_pair("L1_SingleMuOpen_ETMHF50_SingleJet90", 492),          std::make_pair("L1_SingleMuOpen_ETMHF70_SingleJet90", 493),          std::make_pair("L1_UnpairedBunchBptxMinus", 479),          std::make_pair("L1_UnpairedBunchBptxPlus", 478),          std::make_pair("L1_ZeroBias", 473),          std::make_pair("L1_ZeroBias_copy", 468)      };

  static const std::map<std::string, int> Name2Id(name2id, name2id + sizeof(name2id) / sizeof(name2id[0]));
  const std::map<std::string, int>::const_iterator rc = Name2Id.find(name);
  int id = -1;
  if (rc != Name2Id.end()) id = rc->second;
  return id;
}


AlgorithmFunction getFuncFromId(const int index)
{
  static const std::pair<int, AlgorithmFunction> id2func[] = {
          std::make_pair(465, &L1_AlwaysTrue),          std::make_pair(477, &L1_BPTX_AND_Ref1_VME),          std::make_pair(481, &L1_BPTX_AND_Ref3_VME),          std::make_pair(485, &L1_BPTX_AND_Ref4_VME),          std::make_pair(471, &L1_BPTX_BeamGas_B1_VME),          std::make_pair(472, &L1_BPTX_BeamGas_B2_VME),          std::make_pair(469, &L1_BPTX_BeamGas_Ref1_VME),          std::make_pair(470, &L1_BPTX_BeamGas_Ref2_VME),          std::make_pair(480, &L1_BPTX_NotOR_VME),          std::make_pair(482, &L1_BPTX_OR_Ref3_VME),          std::make_pair(486, &L1_BPTX_OR_Ref4_VME),          std::make_pair(483, &L1_BPTX_RefAND_VME),          std::make_pair(475, &L1_BptxMinus),          std::make_pair(476, &L1_BptxOR),          std::make_pair(474, &L1_BptxPlus),          std::make_pair(467, &L1_BptxXOR),          std::make_pair(504, &L1_CDC_SingleMu_3_er1p2_TOP120_DPHI2p618_3p142),          std::make_pair(193, &L1_ETM100),          std::make_pair(273, &L1_ETM100_Jet60_dPhi_Min0p4),          std::make_pair(194, &L1_ETM105),          std::make_pair(195, &L1_ETM110),          std::make_pair(274, &L1_ETM110_Jet60_dPhi_Min0p4),          std::make_pair(196, &L1_ETM115),          std::make_pair(197, &L1_ETM120),          std::make_pair(198, &L1_ETM150),          std::make_pair(183, &L1_ETM30),          std::make_pair(184, &L1_ETM40),          std::make_pair(185, &L1_ETM50),          std::make_pair(186, &L1_ETM60),          std::make_pair(187, &L1_ETM70),          std::make_pair(188, &L1_ETM75),          std::make_pair(431, &L1_ETM75_Jet60_dPhi_Min0p4),          std::make_pair(189, &L1_ETM80),          std::make_pair(271, &L1_ETM80_Jet60_dPhi_Min0p4),          std::make_pair(190, &L1_ETM85),          std::make_pair(191, &L1_ETM90),          std::make_pair(272, &L1_ETM90_Jet60_dPhi_Min0p4),          std::make_pair(192, &L1_ETM95),          std::make_pair(202, &L1_ETMHF100),          std::make_pair(368, &L1_ETMHF100_HTT60er),          std::make_pair(203, &L1_ETMHF110),          std::make_pair(369, &L1_ETMHF110_HTT60er),          std::make_pair(204, &L1_ETMHF120),          std::make_pair(370, &L1_ETMHF120_HTT60er),          std::make_pair(205, &L1_ETMHF150),          std::make_pair(199, &L1_ETMHF70),          std::make_pair(410, &L1_ETMHF70_HTT180er),          std::make_pair(407, &L1_ETMHF70_SingleJet90),          std::make_pair(200, &L1_ETMHF80),          std::make_pair(366, &L1_ETMHF80_HTT60er),          std::make_pair(201, &L1_ETMHF90),          std::make_pair(367, &L1_ETMHF90_HTT60er),          std::make_pair(457, &L1_ETT100_BptxAND),          std::make_pair(458, &L1_ETT110_BptxAND),          std::make_pair(448, &L1_ETT40_BptxAND),          std::make_pair(449, &L1_ETT50_BptxAND),          std::make_pair(450, &L1_ETT60_BptxAND),          std::make_pair(451, &L1_ETT70_BptxAND),          std::make_pair(452, &L1_ETT75_BptxAND),          std::make_pair(453, &L1_ETT80_BptxAND),          std::make_pair(454, &L1_ETT85_BptxAND),          std::make_pair(455, &L1_ETT90_BptxAND),          std::make_pair(456, &L1_ETT95_BptxAND),          std::make_pair(417, &L1_FirstBunchAfterTrain),          std::make_pair(416, &L1_FirstBunchInTrain),          std::make_pair(484, &L1_FirstCollisionInOrbit),          std::make_pair(488, &L1_FirstCollisionInTrain),          std::make_pair(168, &L1_HTT120er),          std::make_pair(169, &L1_HTT160er),          std::make_pair(170, &L1_HTT200er),          std::make_pair(171, &L1_HTT220er),          std::make_pair(172, &L1_HTT240er),          std::make_pair(173, &L1_HTT255er),          std::make_pair(174, &L1_HTT270er),          std::make_pair(175, &L1_HTT280er),          std::make_pair(176, &L1_HTT300er),          std::make_pair(177, &L1_HTT320er),          std::make_pair(178, &L1_HTT340er),          std::make_pair(179, &L1_HTT380er),          std::make_pair(180, &L1_HTT400er),          std::make_pair(181, &L1_HTT450er),          std::make_pair(182, &L1_HTT500er),          std::make_pair(415, &L1_IsolatedBunch),          std::make_pair(487, &L1_LastCollisionInTrain),          std::make_pair(459, &L1_MinimumBiasHF0_AND_BptxAND),          std::make_pair(460, &L1_MinimumBiasHF0_OR_BptxAND),          std::make_pair(461, &L1_Mu10er2p1_ETM30),          std::make_pair(462, &L1_Mu14er2p1_ETM30),          std::make_pair(317, &L1_Mu15_HTT100er),          std::make_pair(233, &L1_Mu18_HTT100er),          std::make_pair(234, &L1_Mu18_Jet24er2p7),          std::make_pair(445, &L1_Mu3_Jet120er2p7_dEta_Max0p4_dPhi_Max0p4),          std::make_pair(443, &L1_Mu3_Jet16er2p7_dEta_Max0p4_dPhi_Max0p4),          std::make_pair(371, &L1_Mu3_Jet30er2p5),          std::make_pair(444, &L1_Mu3_Jet60er2p7_dEta_Max0p4_dPhi_Max0p4),          std::make_pair(425, &L1_Mu6_HTT200er),          std::make_pair(315, &L1_Mu6_HTT240er),          std::make_pair(316, &L1_Mu6_HTT250er),          std::make_pair(426, &L1_Mu8_HTT150er),          std::make_pair(466, &L1_NotBptxOR),          std::make_pair(446, &L1_SingleEG2_BptxAND),          std::make_pair(136, &L1_SingleJet120),          std::make_pair(146, &L1_SingleJet120_FWD),          std::make_pair(447, &L1_SingleJet12_BptxAND),          std::make_pair(137, &L1_SingleJet140),          std::make_pair(138, &L1_SingleJet150),          std::make_pair(131, &L1_SingleJet16),          std::make_pair(139, &L1_SingleJet160),          std::make_pair(140, &L1_SingleJet170),          std::make_pair(141, &L1_SingleJet180),          std::make_pair(132, &L1_SingleJet20),          std::make_pair(142, &L1_SingleJet200),          std::make_pair(133, &L1_SingleJet35),          std::make_pair(143, &L1_SingleJet35_FWD),          std::make_pair(148, &L1_SingleJet35_HFm),          std::make_pair(147, &L1_SingleJet35_HFp),          std::make_pair(134, &L1_SingleJet60),          std::make_pair(144, &L1_SingleJet60_FWD),          std::make_pair(150, &L1_SingleJet60_HFm),          std::make_pair(149, &L1_SingleJet60_HFp),          std::make_pair(135, &L1_SingleJet90),          std::make_pair(145, &L1_SingleJet90_FWD),          std::make_pair(46, &L1_SingleMu0),          std::make_pair(5, &L1_SingleMu0_BMTF),          std::make_pair(7, &L1_SingleMu0_EMTF),          std::make_pair(6, &L1_SingleMu0_OMTF),          std::make_pair(16, &L1_SingleMu16),          std::make_pair(17, &L1_SingleMu18),          std::make_pair(18, &L1_SingleMu20),          std::make_pair(19, &L1_SingleMu22),          std::make_pair(23, &L1_SingleMu25),          std::make_pair(8, &L1_SingleMu3),          std::make_pair(24, &L1_SingleMu30),          std::make_pair(502, &L1_SingleMu3Neg),          std::make_pair(114, &L1_SingleMu3Neg_ETMHF50_SingleJet70),          std::make_pair(160, &L1_SingleMu3Neg_ETMHF50_SingleJet90),          std::make_pair(159, &L1_SingleMu3Neg_ETMHF70_SingleJet70),          std::make_pair(161, &L1_SingleMu3Neg_ETMHF70_SingleJet90),          std::make_pair(503, &L1_SingleMu3Pos),          std::make_pair(64, &L1_SingleMu3_BMTF),          std::make_pair(65, &L1_SingleMu3_BMTF_ETMHF20),          std::make_pair(67, &L1_SingleMu3_BMTF_ETMHF20_SingleJet100),          std::make_pair(71, &L1_SingleMu3_BMTF_ETMHF20_SingleJet100er2p4),          std::make_pair(68, &L1_SingleMu3_BMTF_ETMHF20_SingleJet110),          std::make_pair(72, &L1_SingleMu3_BMTF_ETMHF20_SingleJet110er2p4),          std::make_pair(69, &L1_SingleMu3_BMTF_ETMHF20_SingleJet120),          std::make_pair(73, &L1_SingleMu3_BMTF_ETMHF20_SingleJet120er2p4),          std::make_pair(66, &L1_SingleMu3_BMTF_ETMHF20_SingleJet90),          std::make_pair(70, &L1_SingleMu3_BMTF_ETMHF20_SingleJet90er2p4),          std::make_pair(208, &L1_SingleMu3_ETM50),          std::make_pair(350, &L1_SingleMu3_ETM50_HTT160er),          std::make_pair(348, &L1_SingleMu3_ETM50_SingleJet70),          std::make_pair(490, &L1_SingleMu3_ETMHF20_SingleJet100),          std::make_pair(112, &L1_SingleMu3_ETMHF20_SingleJet100er2p4),          std::make_pair(13, &L1_SingleMu3_ETMHF20_SingleJet110),          std::make_pair(14, &L1_SingleMu3_ETMHF20_SingleJet110er2p4),          std::make_pair(491, &L1_SingleMu3_ETMHF20_SingleJet120),          std::make_pair(113, &L1_SingleMu3_ETMHF20_SingleJet120er2p4),          std::make_pair(463, &L1_SingleMu3_ETMHF20_SingleJet50),          std::make_pair(464, &L1_SingleMu3_ETMHF20_SingleJet70),          std::make_pair(489, &L1_SingleMu3_ETMHF20_SingleJet90),          std::make_pair(111, &L1_SingleMu3_ETMHF20_SingleJet90er2p4),          std::make_pair(47, &L1_SingleMu3_ETMHF30),          std::make_pair(319, &L1_SingleMu3_ETMHF30_HTT140er),          std::make_pair(320, &L1_SingleMu3_ETMHF30_HTT160er),          std::make_pair(321, &L1_SingleMu3_ETMHF30_HTT180er),          std::make_pair(15, &L1_SingleMu3_ETMHF30_SingleJet100),          std::make_pair(25, &L1_SingleMu3_ETMHF30_SingleJet100er2p4),          std::make_pair(20, &L1_SingleMu3_ETMHF30_SingleJet110),          std::make_pair(26, &L1_SingleMu3_ETMHF30_SingleJet110er2p4),          std::make_pair(21, &L1_SingleMu3_ETMHF30_SingleJet120),          std::make_pair(27, &L1_SingleMu3_ETMHF30_SingleJet120er2p4),          std::make_pair(293, &L1_SingleMu3_ETMHF30_SingleJet50),          std::make_pair(296, &L1_SingleMu3_ETMHF30_SingleJet70),          std::make_pair(48, &L1_SingleMu3_ETMHF30_SingleJet90),          std::make_pair(22, &L1_SingleMu3_ETMHF30_SingleJet90er2p4),          std::make_pair(29, &L1_SingleMu3_ETMHF40_SingleJet100),          std::make_pair(33, &L1_SingleMu3_ETMHF40_SingleJet100er2p4),          std::make_pair(30, &L1_SingleMu3_ETMHF40_SingleJet110),          std::make_pair(34, &L1_SingleMu3_ETMHF40_SingleJet110er2p4),          std::make_pair(31, &L1_SingleMu3_ETMHF40_SingleJet120),          std::make_pair(35, &L1_SingleMu3_ETMHF40_SingleJet120er2p4),          std::make_pair(28, &L1_SingleMu3_ETMHF40_SingleJet90),          std::make_pair(32, &L1_SingleMu3_ETMHF40_SingleJet90er2p4),          std::make_pair(49, &L1_SingleMu3_ETMHF50),          std::make_pair(414, &L1_SingleMu3_ETMHF50_ETT160),          std::make_pair(344, &L1_SingleMu3_ETMHF50_HTT140er),          std::make_pair(346, &L1_SingleMu3_ETMHF50_HTT160er),          std::make_pair(322, &L1_SingleMu3_ETMHF50_HTT180er),          std::make_pair(36, &L1_SingleMu3_ETMHF50_SingleJet100),          std::make_pair(39, &L1_SingleMu3_ETMHF50_SingleJet100er2p4),          std::make_pair(37, &L1_SingleMu3_ETMHF50_SingleJet110),          std::make_pair(40, &L1_SingleMu3_ETMHF50_SingleJet110er2p4),          std::make_pair(38, &L1_SingleMu3_ETMHF50_SingleJet120),          std::make_pair(41, &L1_SingleMu3_ETMHF50_SingleJet120er2p4),          std::make_pair(297, &L1_SingleMu3_ETMHF50_SingleJet50),          std::make_pair(313, &L1_SingleMu3_ETMHF50_SingleJet70),          std::make_pair(505, &L1_SingleMu3_ETMHF50_SingleJet70er2p4),          std::make_pair(206, &L1_SingleMu3_ETMHF50_SingleJet90),          std::make_pair(506, &L1_SingleMu3_ETMHF50_SingleJet90er2p4),          std::make_pair(43, &L1_SingleMu3_ETMHF60_SingleJet100),          std::make_pair(51, &L1_SingleMu3_ETMHF60_SingleJet100er2p4),          std::make_pair(44, &L1_SingleMu3_ETMHF60_SingleJet110),          std::make_pair(52, &L1_SingleMu3_ETMHF60_SingleJet110er2p4),          std::make_pair(45, &L1_SingleMu3_ETMHF60_SingleJet120),          std::make_pair(53, &L1_SingleMu3_ETMHF60_SingleJet120er2p4),          std::make_pair(42, &L1_SingleMu3_ETMHF60_SingleJet90),          std::make_pair(50, &L1_SingleMu3_ETMHF60_SingleJet90er2p4),          std::make_pair(207, &L1_SingleMu3_ETMHF70),          std::make_pair(345, &L1_SingleMu3_ETMHF70_HTT140er),          std::make_pair(347, &L1_SingleMu3_ETMHF70_HTT160er),          std::make_pair(343, &L1_SingleMu3_ETMHF70_HTT180er),          std::make_pair(298, &L1_SingleMu3_ETMHF70_SingleJet50),          std::make_pair(314, &L1_SingleMu3_ETMHF70_SingleJet70),          std::make_pair(507, &L1_SingleMu3_ETMHF70_SingleJet70er2p4),          std::make_pair(318, &L1_SingleMu3_ETMHF70_SingleJet90),          std::make_pair(508, &L1_SingleMu3_ETMHF70_SingleJet90er2p4),          std::make_pair(411, &L1_SingleMu3_HTM50),          std::make_pair(412, &L1_SingleMu3_HTM50_HTT160er),          std::make_pair(413, &L1_SingleMu3_HTM50_SingleJet70),          std::make_pair(437, &L1_SingleMu3_SingleJet100),          std::make_pair(162, &L1_SingleMu3_SingleJet100er2p4),          std::make_pair(11, &L1_SingleMu3_SingleJet110),          std::make_pair(12, &L1_SingleMu3_SingleJet110er2p4),          std::make_pair(438, &L1_SingleMu3_SingleJet120),          std::make_pair(163, &L1_SingleMu3_SingleJet120er2p4),          std::make_pair(209, &L1_SingleMu3_SingleJet50),          std::make_pair(509, &L1_SingleMu3_SingleJet50er2p4),          std::make_pair(224, &L1_SingleMu3_SingleJet70),          std::make_pair(510, &L1_SingleMu3_SingleJet70er2p4),          std::make_pair(291, &L1_SingleMu3_SingleJet90),          std::make_pair(511, &L1_SingleMu3_SingleJet90er2p4),          std::make_pair(354, &L1_SingleMu3er1p5),          std::make_pair(74, &L1_SingleMu3er1p5_ETMHF30),          std::make_pair(76, &L1_SingleMu3er1p5_ETMHF30_SingleJet100),          std::make_pair(80, &L1_SingleMu3er1p5_ETMHF30_SingleJet100er2p4),          std::make_pair(77, &L1_SingleMu3er1p5_ETMHF30_SingleJet110),          std::make_pair(81, &L1_SingleMu3er1p5_ETMHF30_SingleJet110er2p4),          std::make_pair(78, &L1_SingleMu3er1p5_ETMHF30_SingleJet120),          std::make_pair(82, &L1_SingleMu3er1p5_ETMHF30_SingleJet120er2p4),          std::make_pair(75, &L1_SingleMu3er1p5_ETMHF30_SingleJet90),          std::make_pair(79, &L1_SingleMu3er1p5_ETMHF30_SingleJet90er2p4),          std::make_pair(356, &L1_SingleMu3er1p5_ETMHF50),          std::make_pair(409, &L1_SingleMu3er1p5_ETMHF50_HTT160er),          std::make_pair(60, &L1_SingleMu3er1p5_ETMHF50_SingleJet100),          std::make_pair(63, &L1_SingleMu3er1p5_ETMHF50_SingleJet100er2p4),          std::make_pair(61, &L1_SingleMu3er1p5_ETMHF50_SingleJet110),          std::make_pair(62, &L1_SingleMu3er1p5_ETMHF50_SingleJet120),          std::make_pair(373, &L1_SingleMu3er1p5_ETMHF50_SingleJet70),          std::make_pair(501, &L1_SingleMu3er1p5_ETMHF50_SingleJet70er2p4),          std::make_pair(496, &L1_SingleMu3er1p5_ETMHF50_SingleJet90),          std::make_pair(500, &L1_SingleMu3er1p5_ETMHF50_SingleJet90er2p4),          std::make_pair(497, &L1_SingleMu3er1p5_ETMHF70_SingleJet90),          std::make_pair(353, &L1_SingleMu3er2p1),          std::make_pair(355, &L1_SingleMu3er2p1_ETMHF50),          std::make_pair(408, &L1_SingleMu3er2p1_ETMHF50_HTT160er),          std::make_pair(54, &L1_SingleMu3er2p1_ETMHF50_SingleJet100),          std::make_pair(57, &L1_SingleMu3er2p1_ETMHF50_SingleJet100er2p4),          std::make_pair(55, &L1_SingleMu3er2p1_ETMHF50_SingleJet110),          std::make_pair(58, &L1_SingleMu3er2p1_ETMHF50_SingleJet110er2p4),          std::make_pair(56, &L1_SingleMu3er2p1_ETMHF50_SingleJet120),          std::make_pair(59, &L1_SingleMu3er2p1_ETMHF50_SingleJet120er2p4),          std::make_pair(372, &L1_SingleMu3er2p1_ETMHF50_SingleJet70),          std::make_pair(499, &L1_SingleMu3er2p1_ETMHF50_SingleJet70er2p4),          std::make_pair(494, &L1_SingleMu3er2p1_ETMHF50_SingleJet90),          std::make_pair(498, &L1_SingleMu3er2p1_ETMHF50_SingleJet90er2p4),          std::make_pair(495, &L1_SingleMu3er2p1_ETMHF70_SingleJet90),          std::make_pair(9, &L1_SingleMu5),          std::make_pair(10, &L1_SingleMu7),          std::make_pair(0, &L1_SingleMuCosmics),          std::make_pair(2, &L1_SingleMuCosmics_BMTF),          std::make_pair(4, &L1_SingleMuCosmics_EMTF),          std::make_pair(3, &L1_SingleMuCosmics_OMTF),          std::make_pair(1, &L1_SingleMuOpen),          std::make_pair(374, &L1_SingleMuOpen_ETMHF50),          std::make_pair(351, &L1_SingleMuOpen_ETMHF50_HTT160er),          std::make_pair(352, &L1_SingleMuOpen_ETMHF50_SingleJet70),          std::make_pair(492, &L1_SingleMuOpen_ETMHF50_SingleJet90),          std::make_pair(493, &L1_SingleMuOpen_ETMHF70_SingleJet90),          std::make_pair(479, &L1_UnpairedBunchBptxMinus),          std::make_pair(478, &L1_UnpairedBunchBptxPlus),          std::make_pair(473, &L1_ZeroBias),          std::make_pair(468, &L1_ZeroBias_copy)      };

  static const std::map<int, AlgorithmFunction> Id2Func(id2func, id2func + sizeof(id2func) / sizeof(id2func[0]));
  const std::map<int, AlgorithmFunction>::const_iterator rc = Id2Func.find(index);
  AlgorithmFunction fp = 0;
  if (rc != Id2Func.end()) fp = rc->second;
  return fp;
}


AlgorithmFunction getFuncFromName(const std::string& name)
{
  static const std::pair<std::string, AlgorithmFunction> name2func[] = {
          std::make_pair("L1_AlwaysTrue", &L1_AlwaysTrue),          std::make_pair("L1_BPTX_AND_Ref1_VME", &L1_BPTX_AND_Ref1_VME),          std::make_pair("L1_BPTX_AND_Ref3_VME", &L1_BPTX_AND_Ref3_VME),          std::make_pair("L1_BPTX_AND_Ref4_VME", &L1_BPTX_AND_Ref4_VME),          std::make_pair("L1_BPTX_BeamGas_B1_VME", &L1_BPTX_BeamGas_B1_VME),          std::make_pair("L1_BPTX_BeamGas_B2_VME", &L1_BPTX_BeamGas_B2_VME),          std::make_pair("L1_BPTX_BeamGas_Ref1_VME", &L1_BPTX_BeamGas_Ref1_VME),          std::make_pair("L1_BPTX_BeamGas_Ref2_VME", &L1_BPTX_BeamGas_Ref2_VME),          std::make_pair("L1_BPTX_NotOR_VME", &L1_BPTX_NotOR_VME),          std::make_pair("L1_BPTX_OR_Ref3_VME", &L1_BPTX_OR_Ref3_VME),          std::make_pair("L1_BPTX_OR_Ref4_VME", &L1_BPTX_OR_Ref4_VME),          std::make_pair("L1_BPTX_RefAND_VME", &L1_BPTX_RefAND_VME),          std::make_pair("L1_BptxMinus", &L1_BptxMinus),          std::make_pair("L1_BptxOR", &L1_BptxOR),          std::make_pair("L1_BptxPlus", &L1_BptxPlus),          std::make_pair("L1_BptxXOR", &L1_BptxXOR),          std::make_pair("L1_CDC_SingleMu_3_er1p2_TOP120_DPHI2p618_3p142", &L1_CDC_SingleMu_3_er1p2_TOP120_DPHI2p618_3p142),          std::make_pair("L1_ETM100", &L1_ETM100),          std::make_pair("L1_ETM100_Jet60_dPhi_Min0p4", &L1_ETM100_Jet60_dPhi_Min0p4),          std::make_pair("L1_ETM105", &L1_ETM105),          std::make_pair("L1_ETM110", &L1_ETM110),          std::make_pair("L1_ETM110_Jet60_dPhi_Min0p4", &L1_ETM110_Jet60_dPhi_Min0p4),          std::make_pair("L1_ETM115", &L1_ETM115),          std::make_pair("L1_ETM120", &L1_ETM120),          std::make_pair("L1_ETM150", &L1_ETM150),          std::make_pair("L1_ETM30", &L1_ETM30),          std::make_pair("L1_ETM40", &L1_ETM40),          std::make_pair("L1_ETM50", &L1_ETM50),          std::make_pair("L1_ETM60", &L1_ETM60),          std::make_pair("L1_ETM70", &L1_ETM70),          std::make_pair("L1_ETM75", &L1_ETM75),          std::make_pair("L1_ETM75_Jet60_dPhi_Min0p4", &L1_ETM75_Jet60_dPhi_Min0p4),          std::make_pair("L1_ETM80", &L1_ETM80),          std::make_pair("L1_ETM80_Jet60_dPhi_Min0p4", &L1_ETM80_Jet60_dPhi_Min0p4),          std::make_pair("L1_ETM85", &L1_ETM85),          std::make_pair("L1_ETM90", &L1_ETM90),          std::make_pair("L1_ETM90_Jet60_dPhi_Min0p4", &L1_ETM90_Jet60_dPhi_Min0p4),          std::make_pair("L1_ETM95", &L1_ETM95),          std::make_pair("L1_ETMHF100", &L1_ETMHF100),          std::make_pair("L1_ETMHF100_HTT60er", &L1_ETMHF100_HTT60er),          std::make_pair("L1_ETMHF110", &L1_ETMHF110),          std::make_pair("L1_ETMHF110_HTT60er", &L1_ETMHF110_HTT60er),          std::make_pair("L1_ETMHF120", &L1_ETMHF120),          std::make_pair("L1_ETMHF120_HTT60er", &L1_ETMHF120_HTT60er),          std::make_pair("L1_ETMHF150", &L1_ETMHF150),          std::make_pair("L1_ETMHF70", &L1_ETMHF70),          std::make_pair("L1_ETMHF70_HTT180er", &L1_ETMHF70_HTT180er),          std::make_pair("L1_ETMHF70_SingleJet90", &L1_ETMHF70_SingleJet90),          std::make_pair("L1_ETMHF80", &L1_ETMHF80),          std::make_pair("L1_ETMHF80_HTT60er", &L1_ETMHF80_HTT60er),          std::make_pair("L1_ETMHF90", &L1_ETMHF90),          std::make_pair("L1_ETMHF90_HTT60er", &L1_ETMHF90_HTT60er),          std::make_pair("L1_ETT100_BptxAND", &L1_ETT100_BptxAND),          std::make_pair("L1_ETT110_BptxAND", &L1_ETT110_BptxAND),          std::make_pair("L1_ETT40_BptxAND", &L1_ETT40_BptxAND),          std::make_pair("L1_ETT50_BptxAND", &L1_ETT50_BptxAND),          std::make_pair("L1_ETT60_BptxAND", &L1_ETT60_BptxAND),          std::make_pair("L1_ETT70_BptxAND", &L1_ETT70_BptxAND),          std::make_pair("L1_ETT75_BptxAND", &L1_ETT75_BptxAND),          std::make_pair("L1_ETT80_BptxAND", &L1_ETT80_BptxAND),          std::make_pair("L1_ETT85_BptxAND", &L1_ETT85_BptxAND),          std::make_pair("L1_ETT90_BptxAND", &L1_ETT90_BptxAND),          std::make_pair("L1_ETT95_BptxAND", &L1_ETT95_BptxAND),          std::make_pair("L1_FirstBunchAfterTrain", &L1_FirstBunchAfterTrain),          std::make_pair("L1_FirstBunchInTrain", &L1_FirstBunchInTrain),          std::make_pair("L1_FirstCollisionInOrbit", &L1_FirstCollisionInOrbit),          std::make_pair("L1_FirstCollisionInTrain", &L1_FirstCollisionInTrain),          std::make_pair("L1_HTT120er", &L1_HTT120er),          std::make_pair("L1_HTT160er", &L1_HTT160er),          std::make_pair("L1_HTT200er", &L1_HTT200er),          std::make_pair("L1_HTT220er", &L1_HTT220er),          std::make_pair("L1_HTT240er", &L1_HTT240er),          std::make_pair("L1_HTT255er", &L1_HTT255er),          std::make_pair("L1_HTT270er", &L1_HTT270er),          std::make_pair("L1_HTT280er", &L1_HTT280er),          std::make_pair("L1_HTT300er", &L1_HTT300er),          std::make_pair("L1_HTT320er", &L1_HTT320er),          std::make_pair("L1_HTT340er", &L1_HTT340er),          std::make_pair("L1_HTT380er", &L1_HTT380er),          std::make_pair("L1_HTT400er", &L1_HTT400er),          std::make_pair("L1_HTT450er", &L1_HTT450er),          std::make_pair("L1_HTT500er", &L1_HTT500er),          std::make_pair("L1_IsolatedBunch", &L1_IsolatedBunch),          std::make_pair("L1_LastCollisionInTrain", &L1_LastCollisionInTrain),          std::make_pair("L1_MinimumBiasHF0_AND_BptxAND", &L1_MinimumBiasHF0_AND_BptxAND),          std::make_pair("L1_MinimumBiasHF0_OR_BptxAND", &L1_MinimumBiasHF0_OR_BptxAND),          std::make_pair("L1_Mu10er2p1_ETM30", &L1_Mu10er2p1_ETM30),          std::make_pair("L1_Mu14er2p1_ETM30", &L1_Mu14er2p1_ETM30),          std::make_pair("L1_Mu15_HTT100er", &L1_Mu15_HTT100er),          std::make_pair("L1_Mu18_HTT100er", &L1_Mu18_HTT100er),          std::make_pair("L1_Mu18_Jet24er2p7", &L1_Mu18_Jet24er2p7),          std::make_pair("L1_Mu3_Jet120er2p7_dEta_Max0p4_dPhi_Max0p4", &L1_Mu3_Jet120er2p7_dEta_Max0p4_dPhi_Max0p4),          std::make_pair("L1_Mu3_Jet16er2p7_dEta_Max0p4_dPhi_Max0p4", &L1_Mu3_Jet16er2p7_dEta_Max0p4_dPhi_Max0p4),          std::make_pair("L1_Mu3_Jet30er2p5", &L1_Mu3_Jet30er2p5),          std::make_pair("L1_Mu3_Jet60er2p7_dEta_Max0p4_dPhi_Max0p4", &L1_Mu3_Jet60er2p7_dEta_Max0p4_dPhi_Max0p4),          std::make_pair("L1_Mu6_HTT200er", &L1_Mu6_HTT200er),          std::make_pair("L1_Mu6_HTT240er", &L1_Mu6_HTT240er),          std::make_pair("L1_Mu6_HTT250er", &L1_Mu6_HTT250er),          std::make_pair("L1_Mu8_HTT150er", &L1_Mu8_HTT150er),          std::make_pair("L1_NotBptxOR", &L1_NotBptxOR),          std::make_pair("L1_SingleEG2_BptxAND", &L1_SingleEG2_BptxAND),          std::make_pair("L1_SingleJet120", &L1_SingleJet120),          std::make_pair("L1_SingleJet120_FWD", &L1_SingleJet120_FWD),          std::make_pair("L1_SingleJet12_BptxAND", &L1_SingleJet12_BptxAND),          std::make_pair("L1_SingleJet140", &L1_SingleJet140),          std::make_pair("L1_SingleJet150", &L1_SingleJet150),          std::make_pair("L1_SingleJet16", &L1_SingleJet16),          std::make_pair("L1_SingleJet160", &L1_SingleJet160),          std::make_pair("L1_SingleJet170", &L1_SingleJet170),          std::make_pair("L1_SingleJet180", &L1_SingleJet180),          std::make_pair("L1_SingleJet20", &L1_SingleJet20),          std::make_pair("L1_SingleJet200", &L1_SingleJet200),          std::make_pair("L1_SingleJet35", &L1_SingleJet35),          std::make_pair("L1_SingleJet35_FWD", &L1_SingleJet35_FWD),          std::make_pair("L1_SingleJet35_HFm", &L1_SingleJet35_HFm),          std::make_pair("L1_SingleJet35_HFp", &L1_SingleJet35_HFp),          std::make_pair("L1_SingleJet60", &L1_SingleJet60),          std::make_pair("L1_SingleJet60_FWD", &L1_SingleJet60_FWD),          std::make_pair("L1_SingleJet60_HFm", &L1_SingleJet60_HFm),          std::make_pair("L1_SingleJet60_HFp", &L1_SingleJet60_HFp),          std::make_pair("L1_SingleJet90", &L1_SingleJet90),          std::make_pair("L1_SingleJet90_FWD", &L1_SingleJet90_FWD),          std::make_pair("L1_SingleMu0", &L1_SingleMu0),          std::make_pair("L1_SingleMu0_BMTF", &L1_SingleMu0_BMTF),          std::make_pair("L1_SingleMu0_EMTF", &L1_SingleMu0_EMTF),          std::make_pair("L1_SingleMu0_OMTF", &L1_SingleMu0_OMTF),          std::make_pair("L1_SingleMu16", &L1_SingleMu16),          std::make_pair("L1_SingleMu18", &L1_SingleMu18),          std::make_pair("L1_SingleMu20", &L1_SingleMu20),          std::make_pair("L1_SingleMu22", &L1_SingleMu22),          std::make_pair("L1_SingleMu25", &L1_SingleMu25),          std::make_pair("L1_SingleMu3", &L1_SingleMu3),          std::make_pair("L1_SingleMu30", &L1_SingleMu30),          std::make_pair("L1_SingleMu3Neg", &L1_SingleMu3Neg),          std::make_pair("L1_SingleMu3Neg_ETMHF50_SingleJet70", &L1_SingleMu3Neg_ETMHF50_SingleJet70),          std::make_pair("L1_SingleMu3Neg_ETMHF50_SingleJet90", &L1_SingleMu3Neg_ETMHF50_SingleJet90),          std::make_pair("L1_SingleMu3Neg_ETMHF70_SingleJet70", &L1_SingleMu3Neg_ETMHF70_SingleJet70),          std::make_pair("L1_SingleMu3Neg_ETMHF70_SingleJet90", &L1_SingleMu3Neg_ETMHF70_SingleJet90),          std::make_pair("L1_SingleMu3Pos", &L1_SingleMu3Pos),          std::make_pair("L1_SingleMu3_BMTF", &L1_SingleMu3_BMTF),          std::make_pair("L1_SingleMu3_BMTF_ETMHF20", &L1_SingleMu3_BMTF_ETMHF20),          std::make_pair("L1_SingleMu3_BMTF_ETMHF20_SingleJet100", &L1_SingleMu3_BMTF_ETMHF20_SingleJet100),          std::make_pair("L1_SingleMu3_BMTF_ETMHF20_SingleJet100er2p4", &L1_SingleMu3_BMTF_ETMHF20_SingleJet100er2p4),          std::make_pair("L1_SingleMu3_BMTF_ETMHF20_SingleJet110", &L1_SingleMu3_BMTF_ETMHF20_SingleJet110),          std::make_pair("L1_SingleMu3_BMTF_ETMHF20_SingleJet110er2p4", &L1_SingleMu3_BMTF_ETMHF20_SingleJet110er2p4),          std::make_pair("L1_SingleMu3_BMTF_ETMHF20_SingleJet120", &L1_SingleMu3_BMTF_ETMHF20_SingleJet120),          std::make_pair("L1_SingleMu3_BMTF_ETMHF20_SingleJet120er2p4", &L1_SingleMu3_BMTF_ETMHF20_SingleJet120er2p4),          std::make_pair("L1_SingleMu3_BMTF_ETMHF20_SingleJet90", &L1_SingleMu3_BMTF_ETMHF20_SingleJet90),          std::make_pair("L1_SingleMu3_BMTF_ETMHF20_SingleJet90er2p4", &L1_SingleMu3_BMTF_ETMHF20_SingleJet90er2p4),          std::make_pair("L1_SingleMu3_ETM50", &L1_SingleMu3_ETM50),          std::make_pair("L1_SingleMu3_ETM50_HTT160er", &L1_SingleMu3_ETM50_HTT160er),          std::make_pair("L1_SingleMu3_ETM50_SingleJet70", &L1_SingleMu3_ETM50_SingleJet70),          std::make_pair("L1_SingleMu3_ETMHF20_SingleJet100", &L1_SingleMu3_ETMHF20_SingleJet100),          std::make_pair("L1_SingleMu3_ETMHF20_SingleJet100er2p4", &L1_SingleMu3_ETMHF20_SingleJet100er2p4),          std::make_pair("L1_SingleMu3_ETMHF20_SingleJet110", &L1_SingleMu3_ETMHF20_SingleJet110),          std::make_pair("L1_SingleMu3_ETMHF20_SingleJet110er2p4", &L1_SingleMu3_ETMHF20_SingleJet110er2p4),          std::make_pair("L1_SingleMu3_ETMHF20_SingleJet120", &L1_SingleMu3_ETMHF20_SingleJet120),          std::make_pair("L1_SingleMu3_ETMHF20_SingleJet120er2p4", &L1_SingleMu3_ETMHF20_SingleJet120er2p4),          std::make_pair("L1_SingleMu3_ETMHF20_SingleJet50", &L1_SingleMu3_ETMHF20_SingleJet50),          std::make_pair("L1_SingleMu3_ETMHF20_SingleJet70", &L1_SingleMu3_ETMHF20_SingleJet70),          std::make_pair("L1_SingleMu3_ETMHF20_SingleJet90", &L1_SingleMu3_ETMHF20_SingleJet90),          std::make_pair("L1_SingleMu3_ETMHF20_SingleJet90er2p4", &L1_SingleMu3_ETMHF20_SingleJet90er2p4),          std::make_pair("L1_SingleMu3_ETMHF30", &L1_SingleMu3_ETMHF30),          std::make_pair("L1_SingleMu3_ETMHF30_HTT140er", &L1_SingleMu3_ETMHF30_HTT140er),          std::make_pair("L1_SingleMu3_ETMHF30_HTT160er", &L1_SingleMu3_ETMHF30_HTT160er),          std::make_pair("L1_SingleMu3_ETMHF30_HTT180er", &L1_SingleMu3_ETMHF30_HTT180er),          std::make_pair("L1_SingleMu3_ETMHF30_SingleJet100", &L1_SingleMu3_ETMHF30_SingleJet100),          std::make_pair("L1_SingleMu3_ETMHF30_SingleJet100er2p4", &L1_SingleMu3_ETMHF30_SingleJet100er2p4),          std::make_pair("L1_SingleMu3_ETMHF30_SingleJet110", &L1_SingleMu3_ETMHF30_SingleJet110),          std::make_pair("L1_SingleMu3_ETMHF30_SingleJet110er2p4", &L1_SingleMu3_ETMHF30_SingleJet110er2p4),          std::make_pair("L1_SingleMu3_ETMHF30_SingleJet120", &L1_SingleMu3_ETMHF30_SingleJet120),          std::make_pair("L1_SingleMu3_ETMHF30_SingleJet120er2p4", &L1_SingleMu3_ETMHF30_SingleJet120er2p4),          std::make_pair("L1_SingleMu3_ETMHF30_SingleJet50", &L1_SingleMu3_ETMHF30_SingleJet50),          std::make_pair("L1_SingleMu3_ETMHF30_SingleJet70", &L1_SingleMu3_ETMHF30_SingleJet70),          std::make_pair("L1_SingleMu3_ETMHF30_SingleJet90", &L1_SingleMu3_ETMHF30_SingleJet90),          std::make_pair("L1_SingleMu3_ETMHF30_SingleJet90er2p4", &L1_SingleMu3_ETMHF30_SingleJet90er2p4),          std::make_pair("L1_SingleMu3_ETMHF40_SingleJet100", &L1_SingleMu3_ETMHF40_SingleJet100),          std::make_pair("L1_SingleMu3_ETMHF40_SingleJet100er2p4", &L1_SingleMu3_ETMHF40_SingleJet100er2p4),          std::make_pair("L1_SingleMu3_ETMHF40_SingleJet110", &L1_SingleMu3_ETMHF40_SingleJet110),          std::make_pair("L1_SingleMu3_ETMHF40_SingleJet110er2p4", &L1_SingleMu3_ETMHF40_SingleJet110er2p4),          std::make_pair("L1_SingleMu3_ETMHF40_SingleJet120", &L1_SingleMu3_ETMHF40_SingleJet120),          std::make_pair("L1_SingleMu3_ETMHF40_SingleJet120er2p4", &L1_SingleMu3_ETMHF40_SingleJet120er2p4),          std::make_pair("L1_SingleMu3_ETMHF40_SingleJet90", &L1_SingleMu3_ETMHF40_SingleJet90),          std::make_pair("L1_SingleMu3_ETMHF40_SingleJet90er2p4", &L1_SingleMu3_ETMHF40_SingleJet90er2p4),          std::make_pair("L1_SingleMu3_ETMHF50", &L1_SingleMu3_ETMHF50),          std::make_pair("L1_SingleMu3_ETMHF50_ETT160", &L1_SingleMu3_ETMHF50_ETT160),          std::make_pair("L1_SingleMu3_ETMHF50_HTT140er", &L1_SingleMu3_ETMHF50_HTT140er),          std::make_pair("L1_SingleMu3_ETMHF50_HTT160er", &L1_SingleMu3_ETMHF50_HTT160er),          std::make_pair("L1_SingleMu3_ETMHF50_HTT180er", &L1_SingleMu3_ETMHF50_HTT180er),          std::make_pair("L1_SingleMu3_ETMHF50_SingleJet100", &L1_SingleMu3_ETMHF50_SingleJet100),          std::make_pair("L1_SingleMu3_ETMHF50_SingleJet100er2p4", &L1_SingleMu3_ETMHF50_SingleJet100er2p4),          std::make_pair("L1_SingleMu3_ETMHF50_SingleJet110", &L1_SingleMu3_ETMHF50_SingleJet110),          std::make_pair("L1_SingleMu3_ETMHF50_SingleJet110er2p4", &L1_SingleMu3_ETMHF50_SingleJet110er2p4),          std::make_pair("L1_SingleMu3_ETMHF50_SingleJet120", &L1_SingleMu3_ETMHF50_SingleJet120),          std::make_pair("L1_SingleMu3_ETMHF50_SingleJet120er2p4", &L1_SingleMu3_ETMHF50_SingleJet120er2p4),          std::make_pair("L1_SingleMu3_ETMHF50_SingleJet50", &L1_SingleMu3_ETMHF50_SingleJet50),          std::make_pair("L1_SingleMu3_ETMHF50_SingleJet70", &L1_SingleMu3_ETMHF50_SingleJet70),          std::make_pair("L1_SingleMu3_ETMHF50_SingleJet70er2p4", &L1_SingleMu3_ETMHF50_SingleJet70er2p4),          std::make_pair("L1_SingleMu3_ETMHF50_SingleJet90", &L1_SingleMu3_ETMHF50_SingleJet90),          std::make_pair("L1_SingleMu3_ETMHF50_SingleJet90er2p4", &L1_SingleMu3_ETMHF50_SingleJet90er2p4),          std::make_pair("L1_SingleMu3_ETMHF60_SingleJet100", &L1_SingleMu3_ETMHF60_SingleJet100),          std::make_pair("L1_SingleMu3_ETMHF60_SingleJet100er2p4", &L1_SingleMu3_ETMHF60_SingleJet100er2p4),          std::make_pair("L1_SingleMu3_ETMHF60_SingleJet110", &L1_SingleMu3_ETMHF60_SingleJet110),          std::make_pair("L1_SingleMu3_ETMHF60_SingleJet110er2p4", &L1_SingleMu3_ETMHF60_SingleJet110er2p4),          std::make_pair("L1_SingleMu3_ETMHF60_SingleJet120", &L1_SingleMu3_ETMHF60_SingleJet120),          std::make_pair("L1_SingleMu3_ETMHF60_SingleJet120er2p4", &L1_SingleMu3_ETMHF60_SingleJet120er2p4),          std::make_pair("L1_SingleMu3_ETMHF60_SingleJet90", &L1_SingleMu3_ETMHF60_SingleJet90),          std::make_pair("L1_SingleMu3_ETMHF60_SingleJet90er2p4", &L1_SingleMu3_ETMHF60_SingleJet90er2p4),          std::make_pair("L1_SingleMu3_ETMHF70", &L1_SingleMu3_ETMHF70),          std::make_pair("L1_SingleMu3_ETMHF70_HTT140er", &L1_SingleMu3_ETMHF70_HTT140er),          std::make_pair("L1_SingleMu3_ETMHF70_HTT160er", &L1_SingleMu3_ETMHF70_HTT160er),          std::make_pair("L1_SingleMu3_ETMHF70_HTT180er", &L1_SingleMu3_ETMHF70_HTT180er),          std::make_pair("L1_SingleMu3_ETMHF70_SingleJet50", &L1_SingleMu3_ETMHF70_SingleJet50),          std::make_pair("L1_SingleMu3_ETMHF70_SingleJet70", &L1_SingleMu3_ETMHF70_SingleJet70),          std::make_pair("L1_SingleMu3_ETMHF70_SingleJet70er2p4", &L1_SingleMu3_ETMHF70_SingleJet70er2p4),          std::make_pair("L1_SingleMu3_ETMHF70_SingleJet90", &L1_SingleMu3_ETMHF70_SingleJet90),          std::make_pair("L1_SingleMu3_ETMHF70_SingleJet90er2p4", &L1_SingleMu3_ETMHF70_SingleJet90er2p4),          std::make_pair("L1_SingleMu3_HTM50", &L1_SingleMu3_HTM50),          std::make_pair("L1_SingleMu3_HTM50_HTT160er", &L1_SingleMu3_HTM50_HTT160er),          std::make_pair("L1_SingleMu3_HTM50_SingleJet70", &L1_SingleMu3_HTM50_SingleJet70),          std::make_pair("L1_SingleMu3_SingleJet100", &L1_SingleMu3_SingleJet100),          std::make_pair("L1_SingleMu3_SingleJet100er2p4", &L1_SingleMu3_SingleJet100er2p4),          std::make_pair("L1_SingleMu3_SingleJet110", &L1_SingleMu3_SingleJet110),          std::make_pair("L1_SingleMu3_SingleJet110er2p4", &L1_SingleMu3_SingleJet110er2p4),          std::make_pair("L1_SingleMu3_SingleJet120", &L1_SingleMu3_SingleJet120),          std::make_pair("L1_SingleMu3_SingleJet120er2p4", &L1_SingleMu3_SingleJet120er2p4),          std::make_pair("L1_SingleMu3_SingleJet50", &L1_SingleMu3_SingleJet50),          std::make_pair("L1_SingleMu3_SingleJet50er2p4", &L1_SingleMu3_SingleJet50er2p4),          std::make_pair("L1_SingleMu3_SingleJet70", &L1_SingleMu3_SingleJet70),          std::make_pair("L1_SingleMu3_SingleJet70er2p4", &L1_SingleMu3_SingleJet70er2p4),          std::make_pair("L1_SingleMu3_SingleJet90", &L1_SingleMu3_SingleJet90),          std::make_pair("L1_SingleMu3_SingleJet90er2p4", &L1_SingleMu3_SingleJet90er2p4),          std::make_pair("L1_SingleMu3er1p5", &L1_SingleMu3er1p5),          std::make_pair("L1_SingleMu3er1p5_ETMHF30", &L1_SingleMu3er1p5_ETMHF30),          std::make_pair("L1_SingleMu3er1p5_ETMHF30_SingleJet100", &L1_SingleMu3er1p5_ETMHF30_SingleJet100),          std::make_pair("L1_SingleMu3er1p5_ETMHF30_SingleJet100er2p4", &L1_SingleMu3er1p5_ETMHF30_SingleJet100er2p4),          std::make_pair("L1_SingleMu3er1p5_ETMHF30_SingleJet110", &L1_SingleMu3er1p5_ETMHF30_SingleJet110),          std::make_pair("L1_SingleMu3er1p5_ETMHF30_SingleJet110er2p4", &L1_SingleMu3er1p5_ETMHF30_SingleJet110er2p4),          std::make_pair("L1_SingleMu3er1p5_ETMHF30_SingleJet120", &L1_SingleMu3er1p5_ETMHF30_SingleJet120),          std::make_pair("L1_SingleMu3er1p5_ETMHF30_SingleJet120er2p4", &L1_SingleMu3er1p5_ETMHF30_SingleJet120er2p4),          std::make_pair("L1_SingleMu3er1p5_ETMHF30_SingleJet90", &L1_SingleMu3er1p5_ETMHF30_SingleJet90),          std::make_pair("L1_SingleMu3er1p5_ETMHF30_SingleJet90er2p4", &L1_SingleMu3er1p5_ETMHF30_SingleJet90er2p4),          std::make_pair("L1_SingleMu3er1p5_ETMHF50", &L1_SingleMu3er1p5_ETMHF50),          std::make_pair("L1_SingleMu3er1p5_ETMHF50_HTT160er", &L1_SingleMu3er1p5_ETMHF50_HTT160er),          std::make_pair("L1_SingleMu3er1p5_ETMHF50_SingleJet100", &L1_SingleMu3er1p5_ETMHF50_SingleJet100),          std::make_pair("L1_SingleMu3er1p5_ETMHF50_SingleJet100er2p4", &L1_SingleMu3er1p5_ETMHF50_SingleJet100er2p4),          std::make_pair("L1_SingleMu3er1p5_ETMHF50_SingleJet110", &L1_SingleMu3er1p5_ETMHF50_SingleJet110),          std::make_pair("L1_SingleMu3er1p5_ETMHF50_SingleJet120", &L1_SingleMu3er1p5_ETMHF50_SingleJet120),          std::make_pair("L1_SingleMu3er1p5_ETMHF50_SingleJet70", &L1_SingleMu3er1p5_ETMHF50_SingleJet70),          std::make_pair("L1_SingleMu3er1p5_ETMHF50_SingleJet70er2p4", &L1_SingleMu3er1p5_ETMHF50_SingleJet70er2p4),          std::make_pair("L1_SingleMu3er1p5_ETMHF50_SingleJet90", &L1_SingleMu3er1p5_ETMHF50_SingleJet90),          std::make_pair("L1_SingleMu3er1p5_ETMHF50_SingleJet90er2p4", &L1_SingleMu3er1p5_ETMHF50_SingleJet90er2p4),          std::make_pair("L1_SingleMu3er1p5_ETMHF70_SingleJet90", &L1_SingleMu3er1p5_ETMHF70_SingleJet90),          std::make_pair("L1_SingleMu3er2p1", &L1_SingleMu3er2p1),          std::make_pair("L1_SingleMu3er2p1_ETMHF50", &L1_SingleMu3er2p1_ETMHF50),          std::make_pair("L1_SingleMu3er2p1_ETMHF50_HTT160er", &L1_SingleMu3er2p1_ETMHF50_HTT160er),          std::make_pair("L1_SingleMu3er2p1_ETMHF50_SingleJet100", &L1_SingleMu3er2p1_ETMHF50_SingleJet100),          std::make_pair("L1_SingleMu3er2p1_ETMHF50_SingleJet100er2p4", &L1_SingleMu3er2p1_ETMHF50_SingleJet100er2p4),          std::make_pair("L1_SingleMu3er2p1_ETMHF50_SingleJet110", &L1_SingleMu3er2p1_ETMHF50_SingleJet110),          std::make_pair("L1_SingleMu3er2p1_ETMHF50_SingleJet110er2p4", &L1_SingleMu3er2p1_ETMHF50_SingleJet110er2p4),          std::make_pair("L1_SingleMu3er2p1_ETMHF50_SingleJet120", &L1_SingleMu3er2p1_ETMHF50_SingleJet120),          std::make_pair("L1_SingleMu3er2p1_ETMHF50_SingleJet120er2p4", &L1_SingleMu3er2p1_ETMHF50_SingleJet120er2p4),          std::make_pair("L1_SingleMu3er2p1_ETMHF50_SingleJet70", &L1_SingleMu3er2p1_ETMHF50_SingleJet70),          std::make_pair("L1_SingleMu3er2p1_ETMHF50_SingleJet70er2p4", &L1_SingleMu3er2p1_ETMHF50_SingleJet70er2p4),          std::make_pair("L1_SingleMu3er2p1_ETMHF50_SingleJet90", &L1_SingleMu3er2p1_ETMHF50_SingleJet90),          std::make_pair("L1_SingleMu3er2p1_ETMHF50_SingleJet90er2p4", &L1_SingleMu3er2p1_ETMHF50_SingleJet90er2p4),          std::make_pair("L1_SingleMu3er2p1_ETMHF70_SingleJet90", &L1_SingleMu3er2p1_ETMHF70_SingleJet90),          std::make_pair("L1_SingleMu5", &L1_SingleMu5),          std::make_pair("L1_SingleMu7", &L1_SingleMu7),          std::make_pair("L1_SingleMuCosmics", &L1_SingleMuCosmics),          std::make_pair("L1_SingleMuCosmics_BMTF", &L1_SingleMuCosmics_BMTF),          std::make_pair("L1_SingleMuCosmics_EMTF", &L1_SingleMuCosmics_EMTF),          std::make_pair("L1_SingleMuCosmics_OMTF", &L1_SingleMuCosmics_OMTF),          std::make_pair("L1_SingleMuOpen", &L1_SingleMuOpen),          std::make_pair("L1_SingleMuOpen_ETMHF50", &L1_SingleMuOpen_ETMHF50),          std::make_pair("L1_SingleMuOpen_ETMHF50_HTT160er", &L1_SingleMuOpen_ETMHF50_HTT160er),          std::make_pair("L1_SingleMuOpen_ETMHF50_SingleJet70", &L1_SingleMuOpen_ETMHF50_SingleJet70),          std::make_pair("L1_SingleMuOpen_ETMHF50_SingleJet90", &L1_SingleMuOpen_ETMHF50_SingleJet90),          std::make_pair("L1_SingleMuOpen_ETMHF70_SingleJet90", &L1_SingleMuOpen_ETMHF70_SingleJet90),          std::make_pair("L1_UnpairedBunchBptxMinus", &L1_UnpairedBunchBptxMinus),          std::make_pair("L1_UnpairedBunchBptxPlus", &L1_UnpairedBunchBptxPlus),          std::make_pair("L1_ZeroBias", &L1_ZeroBias),          std::make_pair("L1_ZeroBias_copy", &L1_ZeroBias_copy)      };

  static const std::map<std::string, AlgorithmFunction> Name2Func(name2func, name2func + sizeof(name2func) / sizeof(name2func[0]));
  const std::map<std::string, AlgorithmFunction>::const_iterator rc = Name2Func.find(name);
  AlgorithmFunction fp = 0;
  if (rc != Name2Func.end()) fp = rc->second;
  if (fp == 0)
  {
    std::stringstream ss;
    ss << "fat> algorithm '" << name << "' is not defined in L1Menu_Collisions2017_v4_SoftTriggers_v4\n";
    throw std::runtime_error(ss.str());
  }
  return fp;
}


bool addFuncFromName(std::map<std::string, std::function<bool()>> &L1SeedFun,
                     L1Analysis::L1AnalysisL1UpgradeDataFormat* upgrade,
                     L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  static const std::pair<std::string, AlgorithmFunction> name2func[] = {
          std::make_pair("L1_AlwaysTrue", &L1_AlwaysTrue),          std::make_pair("L1_BPTX_AND_Ref1_VME", &L1_BPTX_AND_Ref1_VME),          std::make_pair("L1_BPTX_AND_Ref3_VME", &L1_BPTX_AND_Ref3_VME),          std::make_pair("L1_BPTX_AND_Ref4_VME", &L1_BPTX_AND_Ref4_VME),          std::make_pair("L1_BPTX_BeamGas_B1_VME", &L1_BPTX_BeamGas_B1_VME),          std::make_pair("L1_BPTX_BeamGas_B2_VME", &L1_BPTX_BeamGas_B2_VME),          std::make_pair("L1_BPTX_BeamGas_Ref1_VME", &L1_BPTX_BeamGas_Ref1_VME),          std::make_pair("L1_BPTX_BeamGas_Ref2_VME", &L1_BPTX_BeamGas_Ref2_VME),          std::make_pair("L1_BPTX_NotOR_VME", &L1_BPTX_NotOR_VME),          std::make_pair("L1_BPTX_OR_Ref3_VME", &L1_BPTX_OR_Ref3_VME),          std::make_pair("L1_BPTX_OR_Ref4_VME", &L1_BPTX_OR_Ref4_VME),          std::make_pair("L1_BPTX_RefAND_VME", &L1_BPTX_RefAND_VME),          std::make_pair("L1_BptxMinus", &L1_BptxMinus),          std::make_pair("L1_BptxOR", &L1_BptxOR),          std::make_pair("L1_BptxPlus", &L1_BptxPlus),          std::make_pair("L1_BptxXOR", &L1_BptxXOR),          std::make_pair("L1_CDC_SingleMu_3_er1p2_TOP120_DPHI2p618_3p142", &L1_CDC_SingleMu_3_er1p2_TOP120_DPHI2p618_3p142),          std::make_pair("L1_ETM100", &L1_ETM100),          std::make_pair("L1_ETM100_Jet60_dPhi_Min0p4", &L1_ETM100_Jet60_dPhi_Min0p4),          std::make_pair("L1_ETM105", &L1_ETM105),          std::make_pair("L1_ETM110", &L1_ETM110),          std::make_pair("L1_ETM110_Jet60_dPhi_Min0p4", &L1_ETM110_Jet60_dPhi_Min0p4),          std::make_pair("L1_ETM115", &L1_ETM115),          std::make_pair("L1_ETM120", &L1_ETM120),          std::make_pair("L1_ETM150", &L1_ETM150),          std::make_pair("L1_ETM30", &L1_ETM30),          std::make_pair("L1_ETM40", &L1_ETM40),          std::make_pair("L1_ETM50", &L1_ETM50),          std::make_pair("L1_ETM60", &L1_ETM60),          std::make_pair("L1_ETM70", &L1_ETM70),          std::make_pair("L1_ETM75", &L1_ETM75),          std::make_pair("L1_ETM75_Jet60_dPhi_Min0p4", &L1_ETM75_Jet60_dPhi_Min0p4),          std::make_pair("L1_ETM80", &L1_ETM80),          std::make_pair("L1_ETM80_Jet60_dPhi_Min0p4", &L1_ETM80_Jet60_dPhi_Min0p4),          std::make_pair("L1_ETM85", &L1_ETM85),          std::make_pair("L1_ETM90", &L1_ETM90),          std::make_pair("L1_ETM90_Jet60_dPhi_Min0p4", &L1_ETM90_Jet60_dPhi_Min0p4),          std::make_pair("L1_ETM95", &L1_ETM95),          std::make_pair("L1_ETMHF100", &L1_ETMHF100),          std::make_pair("L1_ETMHF100_HTT60er", &L1_ETMHF100_HTT60er),          std::make_pair("L1_ETMHF110", &L1_ETMHF110),          std::make_pair("L1_ETMHF110_HTT60er", &L1_ETMHF110_HTT60er),          std::make_pair("L1_ETMHF120", &L1_ETMHF120),          std::make_pair("L1_ETMHF120_HTT60er", &L1_ETMHF120_HTT60er),          std::make_pair("L1_ETMHF150", &L1_ETMHF150),          std::make_pair("L1_ETMHF70", &L1_ETMHF70),          std::make_pair("L1_ETMHF70_HTT180er", &L1_ETMHF70_HTT180er),          std::make_pair("L1_ETMHF70_SingleJet90", &L1_ETMHF70_SingleJet90),          std::make_pair("L1_ETMHF80", &L1_ETMHF80),          std::make_pair("L1_ETMHF80_HTT60er", &L1_ETMHF80_HTT60er),          std::make_pair("L1_ETMHF90", &L1_ETMHF90),          std::make_pair("L1_ETMHF90_HTT60er", &L1_ETMHF90_HTT60er),          std::make_pair("L1_ETT100_BptxAND", &L1_ETT100_BptxAND),          std::make_pair("L1_ETT110_BptxAND", &L1_ETT110_BptxAND),          std::make_pair("L1_ETT40_BptxAND", &L1_ETT40_BptxAND),          std::make_pair("L1_ETT50_BptxAND", &L1_ETT50_BptxAND),          std::make_pair("L1_ETT60_BptxAND", &L1_ETT60_BptxAND),          std::make_pair("L1_ETT70_BptxAND", &L1_ETT70_BptxAND),          std::make_pair("L1_ETT75_BptxAND", &L1_ETT75_BptxAND),          std::make_pair("L1_ETT80_BptxAND", &L1_ETT80_BptxAND),          std::make_pair("L1_ETT85_BptxAND", &L1_ETT85_BptxAND),          std::make_pair("L1_ETT90_BptxAND", &L1_ETT90_BptxAND),          std::make_pair("L1_ETT95_BptxAND", &L1_ETT95_BptxAND),          std::make_pair("L1_FirstBunchAfterTrain", &L1_FirstBunchAfterTrain),          std::make_pair("L1_FirstBunchInTrain", &L1_FirstBunchInTrain),          std::make_pair("L1_FirstCollisionInOrbit", &L1_FirstCollisionInOrbit),          std::make_pair("L1_FirstCollisionInTrain", &L1_FirstCollisionInTrain),          std::make_pair("L1_HTT120er", &L1_HTT120er),          std::make_pair("L1_HTT160er", &L1_HTT160er),          std::make_pair("L1_HTT200er", &L1_HTT200er),          std::make_pair("L1_HTT220er", &L1_HTT220er),          std::make_pair("L1_HTT240er", &L1_HTT240er),          std::make_pair("L1_HTT255er", &L1_HTT255er),          std::make_pair("L1_HTT270er", &L1_HTT270er),          std::make_pair("L1_HTT280er", &L1_HTT280er),          std::make_pair("L1_HTT300er", &L1_HTT300er),          std::make_pair("L1_HTT320er", &L1_HTT320er),          std::make_pair("L1_HTT340er", &L1_HTT340er),          std::make_pair("L1_HTT380er", &L1_HTT380er),          std::make_pair("L1_HTT400er", &L1_HTT400er),          std::make_pair("L1_HTT450er", &L1_HTT450er),          std::make_pair("L1_HTT500er", &L1_HTT500er),          std::make_pair("L1_IsolatedBunch", &L1_IsolatedBunch),          std::make_pair("L1_LastCollisionInTrain", &L1_LastCollisionInTrain),          std::make_pair("L1_MinimumBiasHF0_AND_BptxAND", &L1_MinimumBiasHF0_AND_BptxAND),          std::make_pair("L1_MinimumBiasHF0_OR_BptxAND", &L1_MinimumBiasHF0_OR_BptxAND),          std::make_pair("L1_Mu10er2p1_ETM30", &L1_Mu10er2p1_ETM30),          std::make_pair("L1_Mu14er2p1_ETM30", &L1_Mu14er2p1_ETM30),          std::make_pair("L1_Mu15_HTT100er", &L1_Mu15_HTT100er),          std::make_pair("L1_Mu18_HTT100er", &L1_Mu18_HTT100er),          std::make_pair("L1_Mu18_Jet24er2p7", &L1_Mu18_Jet24er2p7),          std::make_pair("L1_Mu3_Jet120er2p7_dEta_Max0p4_dPhi_Max0p4", &L1_Mu3_Jet120er2p7_dEta_Max0p4_dPhi_Max0p4),          std::make_pair("L1_Mu3_Jet16er2p7_dEta_Max0p4_dPhi_Max0p4", &L1_Mu3_Jet16er2p7_dEta_Max0p4_dPhi_Max0p4),          std::make_pair("L1_Mu3_Jet30er2p5", &L1_Mu3_Jet30er2p5),          std::make_pair("L1_Mu3_Jet60er2p7_dEta_Max0p4_dPhi_Max0p4", &L1_Mu3_Jet60er2p7_dEta_Max0p4_dPhi_Max0p4),          std::make_pair("L1_Mu6_HTT200er", &L1_Mu6_HTT200er),          std::make_pair("L1_Mu6_HTT240er", &L1_Mu6_HTT240er),          std::make_pair("L1_Mu6_HTT250er", &L1_Mu6_HTT250er),          std::make_pair("L1_Mu8_HTT150er", &L1_Mu8_HTT150er),          std::make_pair("L1_NotBptxOR", &L1_NotBptxOR),          std::make_pair("L1_SingleEG2_BptxAND", &L1_SingleEG2_BptxAND),          std::make_pair("L1_SingleJet120", &L1_SingleJet120),          std::make_pair("L1_SingleJet120_FWD", &L1_SingleJet120_FWD),          std::make_pair("L1_SingleJet12_BptxAND", &L1_SingleJet12_BptxAND),          std::make_pair("L1_SingleJet140", &L1_SingleJet140),          std::make_pair("L1_SingleJet150", &L1_SingleJet150),          std::make_pair("L1_SingleJet16", &L1_SingleJet16),          std::make_pair("L1_SingleJet160", &L1_SingleJet160),          std::make_pair("L1_SingleJet170", &L1_SingleJet170),          std::make_pair("L1_SingleJet180", &L1_SingleJet180),          std::make_pair("L1_SingleJet20", &L1_SingleJet20),          std::make_pair("L1_SingleJet200", &L1_SingleJet200),          std::make_pair("L1_SingleJet35", &L1_SingleJet35),          std::make_pair("L1_SingleJet35_FWD", &L1_SingleJet35_FWD),          std::make_pair("L1_SingleJet35_HFm", &L1_SingleJet35_HFm),          std::make_pair("L1_SingleJet35_HFp", &L1_SingleJet35_HFp),          std::make_pair("L1_SingleJet60", &L1_SingleJet60),          std::make_pair("L1_SingleJet60_FWD", &L1_SingleJet60_FWD),          std::make_pair("L1_SingleJet60_HFm", &L1_SingleJet60_HFm),          std::make_pair("L1_SingleJet60_HFp", &L1_SingleJet60_HFp),          std::make_pair("L1_SingleJet90", &L1_SingleJet90),          std::make_pair("L1_SingleJet90_FWD", &L1_SingleJet90_FWD),          std::make_pair("L1_SingleMu0", &L1_SingleMu0),          std::make_pair("L1_SingleMu0_BMTF", &L1_SingleMu0_BMTF),          std::make_pair("L1_SingleMu0_EMTF", &L1_SingleMu0_EMTF),          std::make_pair("L1_SingleMu0_OMTF", &L1_SingleMu0_OMTF),          std::make_pair("L1_SingleMu16", &L1_SingleMu16),          std::make_pair("L1_SingleMu18", &L1_SingleMu18),          std::make_pair("L1_SingleMu20", &L1_SingleMu20),          std::make_pair("L1_SingleMu22", &L1_SingleMu22),          std::make_pair("L1_SingleMu25", &L1_SingleMu25),          std::make_pair("L1_SingleMu3", &L1_SingleMu3),          std::make_pair("L1_SingleMu30", &L1_SingleMu30),          std::make_pair("L1_SingleMu3Neg", &L1_SingleMu3Neg),          std::make_pair("L1_SingleMu3Neg_ETMHF50_SingleJet70", &L1_SingleMu3Neg_ETMHF50_SingleJet70),          std::make_pair("L1_SingleMu3Neg_ETMHF50_SingleJet90", &L1_SingleMu3Neg_ETMHF50_SingleJet90),          std::make_pair("L1_SingleMu3Neg_ETMHF70_SingleJet70", &L1_SingleMu3Neg_ETMHF70_SingleJet70),          std::make_pair("L1_SingleMu3Neg_ETMHF70_SingleJet90", &L1_SingleMu3Neg_ETMHF70_SingleJet90),          std::make_pair("L1_SingleMu3Pos", &L1_SingleMu3Pos),          std::make_pair("L1_SingleMu3_BMTF", &L1_SingleMu3_BMTF),          std::make_pair("L1_SingleMu3_BMTF_ETMHF20", &L1_SingleMu3_BMTF_ETMHF20),          std::make_pair("L1_SingleMu3_BMTF_ETMHF20_SingleJet100", &L1_SingleMu3_BMTF_ETMHF20_SingleJet100),          std::make_pair("L1_SingleMu3_BMTF_ETMHF20_SingleJet100er2p4", &L1_SingleMu3_BMTF_ETMHF20_SingleJet100er2p4),          std::make_pair("L1_SingleMu3_BMTF_ETMHF20_SingleJet110", &L1_SingleMu3_BMTF_ETMHF20_SingleJet110),          std::make_pair("L1_SingleMu3_BMTF_ETMHF20_SingleJet110er2p4", &L1_SingleMu3_BMTF_ETMHF20_SingleJet110er2p4),          std::make_pair("L1_SingleMu3_BMTF_ETMHF20_SingleJet120", &L1_SingleMu3_BMTF_ETMHF20_SingleJet120),          std::make_pair("L1_SingleMu3_BMTF_ETMHF20_SingleJet120er2p4", &L1_SingleMu3_BMTF_ETMHF20_SingleJet120er2p4),          std::make_pair("L1_SingleMu3_BMTF_ETMHF20_SingleJet90", &L1_SingleMu3_BMTF_ETMHF20_SingleJet90),          std::make_pair("L1_SingleMu3_BMTF_ETMHF20_SingleJet90er2p4", &L1_SingleMu3_BMTF_ETMHF20_SingleJet90er2p4),          std::make_pair("L1_SingleMu3_ETM50", &L1_SingleMu3_ETM50),          std::make_pair("L1_SingleMu3_ETM50_HTT160er", &L1_SingleMu3_ETM50_HTT160er),          std::make_pair("L1_SingleMu3_ETM50_SingleJet70", &L1_SingleMu3_ETM50_SingleJet70),          std::make_pair("L1_SingleMu3_ETMHF20_SingleJet100", &L1_SingleMu3_ETMHF20_SingleJet100),          std::make_pair("L1_SingleMu3_ETMHF20_SingleJet100er2p4", &L1_SingleMu3_ETMHF20_SingleJet100er2p4),          std::make_pair("L1_SingleMu3_ETMHF20_SingleJet110", &L1_SingleMu3_ETMHF20_SingleJet110),          std::make_pair("L1_SingleMu3_ETMHF20_SingleJet110er2p4", &L1_SingleMu3_ETMHF20_SingleJet110er2p4),          std::make_pair("L1_SingleMu3_ETMHF20_SingleJet120", &L1_SingleMu3_ETMHF20_SingleJet120),          std::make_pair("L1_SingleMu3_ETMHF20_SingleJet120er2p4", &L1_SingleMu3_ETMHF20_SingleJet120er2p4),          std::make_pair("L1_SingleMu3_ETMHF20_SingleJet50", &L1_SingleMu3_ETMHF20_SingleJet50),          std::make_pair("L1_SingleMu3_ETMHF20_SingleJet70", &L1_SingleMu3_ETMHF20_SingleJet70),          std::make_pair("L1_SingleMu3_ETMHF20_SingleJet90", &L1_SingleMu3_ETMHF20_SingleJet90),          std::make_pair("L1_SingleMu3_ETMHF20_SingleJet90er2p4", &L1_SingleMu3_ETMHF20_SingleJet90er2p4),          std::make_pair("L1_SingleMu3_ETMHF30", &L1_SingleMu3_ETMHF30),          std::make_pair("L1_SingleMu3_ETMHF30_HTT140er", &L1_SingleMu3_ETMHF30_HTT140er),          std::make_pair("L1_SingleMu3_ETMHF30_HTT160er", &L1_SingleMu3_ETMHF30_HTT160er),          std::make_pair("L1_SingleMu3_ETMHF30_HTT180er", &L1_SingleMu3_ETMHF30_HTT180er),          std::make_pair("L1_SingleMu3_ETMHF30_SingleJet100", &L1_SingleMu3_ETMHF30_SingleJet100),          std::make_pair("L1_SingleMu3_ETMHF30_SingleJet100er2p4", &L1_SingleMu3_ETMHF30_SingleJet100er2p4),          std::make_pair("L1_SingleMu3_ETMHF30_SingleJet110", &L1_SingleMu3_ETMHF30_SingleJet110),          std::make_pair("L1_SingleMu3_ETMHF30_SingleJet110er2p4", &L1_SingleMu3_ETMHF30_SingleJet110er2p4),          std::make_pair("L1_SingleMu3_ETMHF30_SingleJet120", &L1_SingleMu3_ETMHF30_SingleJet120),          std::make_pair("L1_SingleMu3_ETMHF30_SingleJet120er2p4", &L1_SingleMu3_ETMHF30_SingleJet120er2p4),          std::make_pair("L1_SingleMu3_ETMHF30_SingleJet50", &L1_SingleMu3_ETMHF30_SingleJet50),          std::make_pair("L1_SingleMu3_ETMHF30_SingleJet70", &L1_SingleMu3_ETMHF30_SingleJet70),          std::make_pair("L1_SingleMu3_ETMHF30_SingleJet90", &L1_SingleMu3_ETMHF30_SingleJet90),          std::make_pair("L1_SingleMu3_ETMHF30_SingleJet90er2p4", &L1_SingleMu3_ETMHF30_SingleJet90er2p4),          std::make_pair("L1_SingleMu3_ETMHF40_SingleJet100", &L1_SingleMu3_ETMHF40_SingleJet100),          std::make_pair("L1_SingleMu3_ETMHF40_SingleJet100er2p4", &L1_SingleMu3_ETMHF40_SingleJet100er2p4),          std::make_pair("L1_SingleMu3_ETMHF40_SingleJet110", &L1_SingleMu3_ETMHF40_SingleJet110),          std::make_pair("L1_SingleMu3_ETMHF40_SingleJet110er2p4", &L1_SingleMu3_ETMHF40_SingleJet110er2p4),          std::make_pair("L1_SingleMu3_ETMHF40_SingleJet120", &L1_SingleMu3_ETMHF40_SingleJet120),          std::make_pair("L1_SingleMu3_ETMHF40_SingleJet120er2p4", &L1_SingleMu3_ETMHF40_SingleJet120er2p4),          std::make_pair("L1_SingleMu3_ETMHF40_SingleJet90", &L1_SingleMu3_ETMHF40_SingleJet90),          std::make_pair("L1_SingleMu3_ETMHF40_SingleJet90er2p4", &L1_SingleMu3_ETMHF40_SingleJet90er2p4),          std::make_pair("L1_SingleMu3_ETMHF50", &L1_SingleMu3_ETMHF50),          std::make_pair("L1_SingleMu3_ETMHF50_ETT160", &L1_SingleMu3_ETMHF50_ETT160),          std::make_pair("L1_SingleMu3_ETMHF50_HTT140er", &L1_SingleMu3_ETMHF50_HTT140er),          std::make_pair("L1_SingleMu3_ETMHF50_HTT160er", &L1_SingleMu3_ETMHF50_HTT160er),          std::make_pair("L1_SingleMu3_ETMHF50_HTT180er", &L1_SingleMu3_ETMHF50_HTT180er),          std::make_pair("L1_SingleMu3_ETMHF50_SingleJet100", &L1_SingleMu3_ETMHF50_SingleJet100),          std::make_pair("L1_SingleMu3_ETMHF50_SingleJet100er2p4", &L1_SingleMu3_ETMHF50_SingleJet100er2p4),          std::make_pair("L1_SingleMu3_ETMHF50_SingleJet110", &L1_SingleMu3_ETMHF50_SingleJet110),          std::make_pair("L1_SingleMu3_ETMHF50_SingleJet110er2p4", &L1_SingleMu3_ETMHF50_SingleJet110er2p4),          std::make_pair("L1_SingleMu3_ETMHF50_SingleJet120", &L1_SingleMu3_ETMHF50_SingleJet120),          std::make_pair("L1_SingleMu3_ETMHF50_SingleJet120er2p4", &L1_SingleMu3_ETMHF50_SingleJet120er2p4),          std::make_pair("L1_SingleMu3_ETMHF50_SingleJet50", &L1_SingleMu3_ETMHF50_SingleJet50),          std::make_pair("L1_SingleMu3_ETMHF50_SingleJet70", &L1_SingleMu3_ETMHF50_SingleJet70),          std::make_pair("L1_SingleMu3_ETMHF50_SingleJet70er2p4", &L1_SingleMu3_ETMHF50_SingleJet70er2p4),          std::make_pair("L1_SingleMu3_ETMHF50_SingleJet90", &L1_SingleMu3_ETMHF50_SingleJet90),          std::make_pair("L1_SingleMu3_ETMHF50_SingleJet90er2p4", &L1_SingleMu3_ETMHF50_SingleJet90er2p4),          std::make_pair("L1_SingleMu3_ETMHF60_SingleJet100", &L1_SingleMu3_ETMHF60_SingleJet100),          std::make_pair("L1_SingleMu3_ETMHF60_SingleJet100er2p4", &L1_SingleMu3_ETMHF60_SingleJet100er2p4),          std::make_pair("L1_SingleMu3_ETMHF60_SingleJet110", &L1_SingleMu3_ETMHF60_SingleJet110),          std::make_pair("L1_SingleMu3_ETMHF60_SingleJet110er2p4", &L1_SingleMu3_ETMHF60_SingleJet110er2p4),          std::make_pair("L1_SingleMu3_ETMHF60_SingleJet120", &L1_SingleMu3_ETMHF60_SingleJet120),          std::make_pair("L1_SingleMu3_ETMHF60_SingleJet120er2p4", &L1_SingleMu3_ETMHF60_SingleJet120er2p4),          std::make_pair("L1_SingleMu3_ETMHF60_SingleJet90", &L1_SingleMu3_ETMHF60_SingleJet90),          std::make_pair("L1_SingleMu3_ETMHF60_SingleJet90er2p4", &L1_SingleMu3_ETMHF60_SingleJet90er2p4),          std::make_pair("L1_SingleMu3_ETMHF70", &L1_SingleMu3_ETMHF70),          std::make_pair("L1_SingleMu3_ETMHF70_HTT140er", &L1_SingleMu3_ETMHF70_HTT140er),          std::make_pair("L1_SingleMu3_ETMHF70_HTT160er", &L1_SingleMu3_ETMHF70_HTT160er),          std::make_pair("L1_SingleMu3_ETMHF70_HTT180er", &L1_SingleMu3_ETMHF70_HTT180er),          std::make_pair("L1_SingleMu3_ETMHF70_SingleJet50", &L1_SingleMu3_ETMHF70_SingleJet50),          std::make_pair("L1_SingleMu3_ETMHF70_SingleJet70", &L1_SingleMu3_ETMHF70_SingleJet70),          std::make_pair("L1_SingleMu3_ETMHF70_SingleJet70er2p4", &L1_SingleMu3_ETMHF70_SingleJet70er2p4),          std::make_pair("L1_SingleMu3_ETMHF70_SingleJet90", &L1_SingleMu3_ETMHF70_SingleJet90),          std::make_pair("L1_SingleMu3_ETMHF70_SingleJet90er2p4", &L1_SingleMu3_ETMHF70_SingleJet90er2p4),          std::make_pair("L1_SingleMu3_HTM50", &L1_SingleMu3_HTM50),          std::make_pair("L1_SingleMu3_HTM50_HTT160er", &L1_SingleMu3_HTM50_HTT160er),          std::make_pair("L1_SingleMu3_HTM50_SingleJet70", &L1_SingleMu3_HTM50_SingleJet70),          std::make_pair("L1_SingleMu3_SingleJet100", &L1_SingleMu3_SingleJet100),          std::make_pair("L1_SingleMu3_SingleJet100er2p4", &L1_SingleMu3_SingleJet100er2p4),          std::make_pair("L1_SingleMu3_SingleJet110", &L1_SingleMu3_SingleJet110),          std::make_pair("L1_SingleMu3_SingleJet110er2p4", &L1_SingleMu3_SingleJet110er2p4),          std::make_pair("L1_SingleMu3_SingleJet120", &L1_SingleMu3_SingleJet120),          std::make_pair("L1_SingleMu3_SingleJet120er2p4", &L1_SingleMu3_SingleJet120er2p4),          std::make_pair("L1_SingleMu3_SingleJet50", &L1_SingleMu3_SingleJet50),          std::make_pair("L1_SingleMu3_SingleJet50er2p4", &L1_SingleMu3_SingleJet50er2p4),          std::make_pair("L1_SingleMu3_SingleJet70", &L1_SingleMu3_SingleJet70),          std::make_pair("L1_SingleMu3_SingleJet70er2p4", &L1_SingleMu3_SingleJet70er2p4),          std::make_pair("L1_SingleMu3_SingleJet90", &L1_SingleMu3_SingleJet90),          std::make_pair("L1_SingleMu3_SingleJet90er2p4", &L1_SingleMu3_SingleJet90er2p4),          std::make_pair("L1_SingleMu3er1p5", &L1_SingleMu3er1p5),          std::make_pair("L1_SingleMu3er1p5_ETMHF30", &L1_SingleMu3er1p5_ETMHF30),          std::make_pair("L1_SingleMu3er1p5_ETMHF30_SingleJet100", &L1_SingleMu3er1p5_ETMHF30_SingleJet100),          std::make_pair("L1_SingleMu3er1p5_ETMHF30_SingleJet100er2p4", &L1_SingleMu3er1p5_ETMHF30_SingleJet100er2p4),          std::make_pair("L1_SingleMu3er1p5_ETMHF30_SingleJet110", &L1_SingleMu3er1p5_ETMHF30_SingleJet110),          std::make_pair("L1_SingleMu3er1p5_ETMHF30_SingleJet110er2p4", &L1_SingleMu3er1p5_ETMHF30_SingleJet110er2p4),          std::make_pair("L1_SingleMu3er1p5_ETMHF30_SingleJet120", &L1_SingleMu3er1p5_ETMHF30_SingleJet120),          std::make_pair("L1_SingleMu3er1p5_ETMHF30_SingleJet120er2p4", &L1_SingleMu3er1p5_ETMHF30_SingleJet120er2p4),          std::make_pair("L1_SingleMu3er1p5_ETMHF30_SingleJet90", &L1_SingleMu3er1p5_ETMHF30_SingleJet90),          std::make_pair("L1_SingleMu3er1p5_ETMHF30_SingleJet90er2p4", &L1_SingleMu3er1p5_ETMHF30_SingleJet90er2p4),          std::make_pair("L1_SingleMu3er1p5_ETMHF50", &L1_SingleMu3er1p5_ETMHF50),          std::make_pair("L1_SingleMu3er1p5_ETMHF50_HTT160er", &L1_SingleMu3er1p5_ETMHF50_HTT160er),          std::make_pair("L1_SingleMu3er1p5_ETMHF50_SingleJet100", &L1_SingleMu3er1p5_ETMHF50_SingleJet100),          std::make_pair("L1_SingleMu3er1p5_ETMHF50_SingleJet100er2p4", &L1_SingleMu3er1p5_ETMHF50_SingleJet100er2p4),          std::make_pair("L1_SingleMu3er1p5_ETMHF50_SingleJet110", &L1_SingleMu3er1p5_ETMHF50_SingleJet110),          std::make_pair("L1_SingleMu3er1p5_ETMHF50_SingleJet120", &L1_SingleMu3er1p5_ETMHF50_SingleJet120),          std::make_pair("L1_SingleMu3er1p5_ETMHF50_SingleJet70", &L1_SingleMu3er1p5_ETMHF50_SingleJet70),          std::make_pair("L1_SingleMu3er1p5_ETMHF50_SingleJet70er2p4", &L1_SingleMu3er1p5_ETMHF50_SingleJet70er2p4),          std::make_pair("L1_SingleMu3er1p5_ETMHF50_SingleJet90", &L1_SingleMu3er1p5_ETMHF50_SingleJet90),          std::make_pair("L1_SingleMu3er1p5_ETMHF50_SingleJet90er2p4", &L1_SingleMu3er1p5_ETMHF50_SingleJet90er2p4),          std::make_pair("L1_SingleMu3er1p5_ETMHF70_SingleJet90", &L1_SingleMu3er1p5_ETMHF70_SingleJet90),          std::make_pair("L1_SingleMu3er2p1", &L1_SingleMu3er2p1),          std::make_pair("L1_SingleMu3er2p1_ETMHF50", &L1_SingleMu3er2p1_ETMHF50),          std::make_pair("L1_SingleMu3er2p1_ETMHF50_HTT160er", &L1_SingleMu3er2p1_ETMHF50_HTT160er),          std::make_pair("L1_SingleMu3er2p1_ETMHF50_SingleJet100", &L1_SingleMu3er2p1_ETMHF50_SingleJet100),          std::make_pair("L1_SingleMu3er2p1_ETMHF50_SingleJet100er2p4", &L1_SingleMu3er2p1_ETMHF50_SingleJet100er2p4),          std::make_pair("L1_SingleMu3er2p1_ETMHF50_SingleJet110", &L1_SingleMu3er2p1_ETMHF50_SingleJet110),          std::make_pair("L1_SingleMu3er2p1_ETMHF50_SingleJet110er2p4", &L1_SingleMu3er2p1_ETMHF50_SingleJet110er2p4),          std::make_pair("L1_SingleMu3er2p1_ETMHF50_SingleJet120", &L1_SingleMu3er2p1_ETMHF50_SingleJet120),          std::make_pair("L1_SingleMu3er2p1_ETMHF50_SingleJet120er2p4", &L1_SingleMu3er2p1_ETMHF50_SingleJet120er2p4),          std::make_pair("L1_SingleMu3er2p1_ETMHF50_SingleJet70", &L1_SingleMu3er2p1_ETMHF50_SingleJet70),          std::make_pair("L1_SingleMu3er2p1_ETMHF50_SingleJet70er2p4", &L1_SingleMu3er2p1_ETMHF50_SingleJet70er2p4),          std::make_pair("L1_SingleMu3er2p1_ETMHF50_SingleJet90", &L1_SingleMu3er2p1_ETMHF50_SingleJet90),          std::make_pair("L1_SingleMu3er2p1_ETMHF50_SingleJet90er2p4", &L1_SingleMu3er2p1_ETMHF50_SingleJet90er2p4),          std::make_pair("L1_SingleMu3er2p1_ETMHF70_SingleJet90", &L1_SingleMu3er2p1_ETMHF70_SingleJet90),          std::make_pair("L1_SingleMu5", &L1_SingleMu5),          std::make_pair("L1_SingleMu7", &L1_SingleMu7),          std::make_pair("L1_SingleMuCosmics", &L1_SingleMuCosmics),          std::make_pair("L1_SingleMuCosmics_BMTF", &L1_SingleMuCosmics_BMTF),          std::make_pair("L1_SingleMuCosmics_EMTF", &L1_SingleMuCosmics_EMTF),          std::make_pair("L1_SingleMuCosmics_OMTF", &L1_SingleMuCosmics_OMTF),          std::make_pair("L1_SingleMuOpen", &L1_SingleMuOpen),          std::make_pair("L1_SingleMuOpen_ETMHF50", &L1_SingleMuOpen_ETMHF50),          std::make_pair("L1_SingleMuOpen_ETMHF50_HTT160er", &L1_SingleMuOpen_ETMHF50_HTT160er),          std::make_pair("L1_SingleMuOpen_ETMHF50_SingleJet70", &L1_SingleMuOpen_ETMHF50_SingleJet70),          std::make_pair("L1_SingleMuOpen_ETMHF50_SingleJet90", &L1_SingleMuOpen_ETMHF50_SingleJet90),          std::make_pair("L1_SingleMuOpen_ETMHF70_SingleJet90", &L1_SingleMuOpen_ETMHF70_SingleJet90),          std::make_pair("L1_UnpairedBunchBptxMinus", &L1_UnpairedBunchBptxMinus),          std::make_pair("L1_UnpairedBunchBptxPlus", &L1_UnpairedBunchBptxPlus),          std::make_pair("L1_ZeroBias", &L1_ZeroBias),          std::make_pair("L1_ZeroBias_copy", &L1_ZeroBias_copy)      };

  for (auto pair : name2func)
  {
    L1SeedFun[pair.first] = std::bind(pair.second, upgrade, calo_tower);
  }

  return true;
}
// eof