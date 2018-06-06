/* automatically generated from L1Menu_Collisions2017_v4slim_my_SoftMuPlusHardJet_FullMenu_v1 with menu2lib.py */
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
CaloCaloCorrelation_12094985861278072376
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
    bool pass = false;
  size_t nobj0 = 0;
  for (size_t ii = 0; ii < data->egBx.size(); ii++)
  {
    if (not (data->egBx.at(ii) == 0)) continue;
    nobj0++;
          
        bool etaWindow1;
                              // EG26: ET >= 52 at BX = 0
      if (not (data->egIEt.at(ii) >= 52)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->egIEta.at(ii)) and (data->egIEta.at(ii) <= 48));
            
                        // isolation : 0xc
      if (not ((12 >> data->egIso.at(ii)) & 1)) continue;

          if (not etaWindow1) continue;

    size_t nobj1 = 0;
    for (size_t jj = 0; jj < data->jetBx.size(); jj++)
    {
      if (not (data->jetBx.at(jj) == 0)) continue;
      nobj1++;
              
                                      // JET34: ET >= 68 at BX = 0
      if (not (data->jetIEt.at(jj) >= 68)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(jj)) and (data->jetIEta.at(jj) <= 61));
            
          if (not etaWindow1) continue;
          long long minimum;
  long long maximum;
    int iEta = -9999999; unsigned int deltaIEta = 9999999;
        // 0.30 <= DeltaR <= 11.80
      iEta = data->egIEta.at(ii);
    deltaIEta = abs(iEta - data->jetIEta.at(jj));
      unsigned int deltaEta = LUT_DETA_EG_JET[deltaIEta];
  
    int iPhi = data->egIPhi.at(ii);
  
  unsigned int deltaIPhi = abs(iPhi - data->jetIPhi.at(jj));
  if (deltaIPhi >= 72) deltaIPhi = 2*72 - deltaIPhi;
      unsigned int deltaPhi = LUT_DPHI_EG_JET[deltaIPhi];
  
  long long deltaR2 = deltaEta*deltaEta + deltaPhi*deltaPhi;
    minimum = (long long)(0.09 * POW10[6]);
  maximum = (long long)(139.24 * POW10[6]);
  if (not ((minimum <= deltaR2) and (deltaR2 <= maximum))) continue;

    
      pass = true;
      break;
    }
    if (pass) break;
  }

  return pass;
}


      





bool
CaloCaloCorrelation_12094985861278072888
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
    bool pass = false;
  size_t nobj0 = 0;
  for (size_t ii = 0; ii < data->egBx.size(); ii++)
  {
    if (not (data->egBx.at(ii) == 0)) continue;
    nobj0++;
          
        bool etaWindow1;
                              // EG28: ET >= 56 at BX = 0
      if (not (data->egIEt.at(ii) >= 56)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->egIEta.at(ii)) and (data->egIEta.at(ii) <= 48));
            
                        // isolation : 0xc
      if (not ((12 >> data->egIso.at(ii)) & 1)) continue;

          if (not etaWindow1) continue;

    size_t nobj1 = 0;
    for (size_t jj = 0; jj < data->jetBx.size(); jj++)
    {
      if (not (data->jetBx.at(jj) == 0)) continue;
      nobj1++;
              
                                      // JET34: ET >= 68 at BX = 0
      if (not (data->jetIEt.at(jj) >= 68)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(jj)) and (data->jetIEta.at(jj) <= 61));
            
          if (not etaWindow1) continue;
          long long minimum;
  long long maximum;
    int iEta = -9999999; unsigned int deltaIEta = 9999999;
        // 0.30 <= DeltaR <= 11.80
      iEta = data->egIEta.at(ii);
    deltaIEta = abs(iEta - data->jetIEta.at(jj));
      unsigned int deltaEta = LUT_DETA_EG_JET[deltaIEta];
  
    int iPhi = data->egIPhi.at(ii);
  
  unsigned int deltaIPhi = abs(iPhi - data->jetIPhi.at(jj));
  if (deltaIPhi >= 72) deltaIPhi = 2*72 - deltaIPhi;
      unsigned int deltaPhi = LUT_DPHI_EG_JET[deltaIPhi];
  
  long long deltaR2 = deltaEta*deltaEta + deltaPhi*deltaPhi;
    minimum = (long long)(0.09 * POW10[6]);
  maximum = (long long)(139.24 * POW10[6]);
  if (not ((minimum <= deltaR2) and (deltaR2 <= maximum))) continue;

    
      pass = true;
      break;
    }
    if (pass) break;
  }

  return pass;
}


      





bool
CaloCaloCorrelation_12094985861278103608
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
    bool pass = false;
  size_t nobj0 = 0;
  for (size_t ii = 0; ii < data->egBx.size(); ii++)
  {
    if (not (data->egBx.at(ii) == 0)) continue;
    nobj0++;
          
        bool etaWindow1;
                              // EG30: ET >= 60 at BX = 0
      if (not (data->egIEt.at(ii) >= 60)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->egIEta.at(ii)) and (data->egIEta.at(ii) <= 48));
            
                        // isolation : 0xc
      if (not ((12 >> data->egIso.at(ii)) & 1)) continue;

          if (not etaWindow1) continue;

    size_t nobj1 = 0;
    for (size_t jj = 0; jj < data->jetBx.size(); jj++)
    {
      if (not (data->jetBx.at(jj) == 0)) continue;
      nobj1++;
              
                                      // JET34: ET >= 68 at BX = 0
      if (not (data->jetIEt.at(jj) >= 68)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(jj)) and (data->jetIEta.at(jj) <= 61));
            
          if (not etaWindow1) continue;
          long long minimum;
  long long maximum;
    int iEta = -9999999; unsigned int deltaIEta = 9999999;
        // 0.30 <= DeltaR <= 11.80
      iEta = data->egIEta.at(ii);
    deltaIEta = abs(iEta - data->jetIEta.at(jj));
      unsigned int deltaEta = LUT_DETA_EG_JET[deltaIEta];
  
    int iPhi = data->egIPhi.at(ii);
  
  unsigned int deltaIPhi = abs(iPhi - data->jetIPhi.at(jj));
  if (deltaIPhi >= 72) deltaIPhi = 2*72 - deltaIPhi;
      unsigned int deltaPhi = LUT_DPHI_EG_JET[deltaIPhi];
  
  long long deltaR2 = deltaEta*deltaEta + deltaPhi*deltaPhi;
    minimum = (long long)(0.09 * POW10[6]);
  maximum = (long long)(139.24 * POW10[6]);
  if (not ((minimum <= deltaR2) and (deltaR2 <= maximum))) continue;

    
      pass = true;
      break;
    }
    if (pass) break;
  }

  return pass;
}


      





bool
CaloCaloCorrelation_3813196582576312175
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
    size_t nobj0 = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj0++;
                   candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      bool etaWindow1;
      const int idx0 = candidates.at(set.at(indicies.at(0)));
      const int idx1 = candidates.at(set.at(indicies.at(1)));
                                // JET32: ET >= 64 at BX = 0
      if (not (data->jetIEt.at(idx0) >= 64)) continue;

                        // -2.3055 <= eta <= 2.3055
              etaWindow1 = ((-53 <= data->jetIEta.at(idx0)) and (data->jetIEta.at(idx0) <= 52));
            
          if (not etaWindow1) continue;
                                // JET32: ET >= 64 at BX = 0
      if (not (data->jetIEt.at(idx1) >= 64)) continue;

                        // -2.3055 <= eta <= 2.3055
              etaWindow1 = ((-53 <= data->jetIEta.at(idx1)) and (data->jetIEta.at(idx1) <= 52));
            
          if (not etaWindow1) continue;
          long long minimum;
  long long maximum;

  int iEta = -9999999; unsigned int deltaIEta = 9999999;
        // 0.0 <= DeltaEta <= 1.6
      iEta = data->jetIEta.at(idx0);
    deltaIEta = abs(iEta - data->jetIEta.at(idx1));
      unsigned int deltaEta = LUT_DETA_JET_JET[deltaIEta];
  
    minimum = (long long)(0.0 * POW10[3]);
  maximum = (long long)(1.6 * POW10[3]);
  if (not ((minimum <= deltaEta) and (deltaEta <= maximum))) continue;

    
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}



      





bool
CaloCaloCorrelation_3813196582576378703
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
    size_t nobj0 = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj0++;
                   candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      bool etaWindow1;
      const int idx0 = candidates.at(set.at(indicies.at(0)));
      const int idx1 = candidates.at(set.at(indicies.at(1)));
                                // JET40: ET >= 80 at BX = 0
      if (not (data->jetIEt.at(idx0) >= 80)) continue;

                        // -2.3055 <= eta <= 2.3055
              etaWindow1 = ((-53 <= data->jetIEta.at(idx0)) and (data->jetIEta.at(idx0) <= 52));
            
          if (not etaWindow1) continue;
                                // JET40: ET >= 80 at BX = 0
      if (not (data->jetIEt.at(idx1) >= 80)) continue;

                        // -2.3055 <= eta <= 2.3055
              etaWindow1 = ((-53 <= data->jetIEta.at(idx1)) and (data->jetIEta.at(idx1) <= 52));
            
          if (not etaWindow1) continue;
          long long minimum;
  long long maximum;

  int iEta = -9999999; unsigned int deltaIEta = 9999999;
        // 0.0 <= DeltaEta <= 1.6
      iEta = data->jetIEta.at(idx0);
    deltaIEta = abs(iEta - data->jetIEta.at(idx1));
      unsigned int deltaEta = LUT_DETA_JET_JET[deltaIEta];
  
    minimum = (long long)(0.0 * POW10[3]);
  maximum = (long long)(1.6 * POW10[3]);
  if (not ((minimum <= deltaEta) and (deltaEta <= maximum))) continue;

    
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}



      





bool
CaloCaloCorrelation_7041035331702023693
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
    size_t nobj0 = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj0++;
                   candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      bool etaWindow1;
      const int idx0 = candidates.at(set.at(indicies.at(0)));
      const int idx1 = candidates.at(set.at(indicies.at(1)));
                                // JET100: ET >= 200 at BX = 0
      if (not (data->jetIEt.at(idx0) >= 200)) continue;

                        // -2.3055 <= eta <= 2.3055
              etaWindow1 = ((-53 <= data->jetIEta.at(idx0)) and (data->jetIEta.at(idx0) <= 52));
            
          if (not etaWindow1) continue;
                                // JET100: ET >= 200 at BX = 0
      if (not (data->jetIEt.at(idx1) >= 200)) continue;

                        // -2.3055 <= eta <= 2.3055
              etaWindow1 = ((-53 <= data->jetIEta.at(idx1)) and (data->jetIEta.at(idx1) <= 52));
            
          if (not etaWindow1) continue;
          long long minimum;
  long long maximum;

  int iEta = -9999999; unsigned int deltaIEta = 9999999;
        // 0.0 <= DeltaEta <= 1.6
      iEta = data->jetIEta.at(idx0);
    deltaIEta = abs(iEta - data->jetIEta.at(idx1));
      unsigned int deltaEta = LUT_DETA_JET_JET[deltaIEta];
  
    minimum = (long long)(0.0 * POW10[3]);
  maximum = (long long)(1.6 * POW10[3]);
  if (not ((minimum <= deltaEta) and (deltaEta <= maximum))) continue;

    
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}



      





bool
CaloCaloCorrelation_7041035331710545453
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
    size_t nobj0 = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj0++;
                   candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      bool etaWindow1;
      const int idx0 = candidates.at(set.at(indicies.at(0)));
      const int idx1 = candidates.at(set.at(indicies.at(1)));
                                // JET112: ET >= 224 at BX = 0
      if (not (data->jetIEt.at(idx0) >= 224)) continue;

                        // -2.3055 <= eta <= 2.3055
              etaWindow1 = ((-53 <= data->jetIEta.at(idx0)) and (data->jetIEta.at(idx0) <= 52));
            
          if (not etaWindow1) continue;
                                // JET112: ET >= 224 at BX = 0
      if (not (data->jetIEt.at(idx1) >= 224)) continue;

                        // -2.3055 <= eta <= 2.3055
              etaWindow1 = ((-53 <= data->jetIEta.at(idx1)) and (data->jetIEta.at(idx1) <= 52));
            
          if (not etaWindow1) continue;
          long long minimum;
  long long maximum;

  int iEta = -9999999; unsigned int deltaIEta = 9999999;
        // 0.0 <= DeltaEta <= 1.6
      iEta = data->jetIEta.at(idx0);
    deltaIEta = abs(iEta - data->jetIEta.at(idx1));
      unsigned int deltaEta = LUT_DETA_JET_JET[deltaIEta];
  
    minimum = (long long)(0.0 * POW10[3]);
  maximum = (long long)(1.6 * POW10[3]);
  if (not ((minimum <= deltaEta) and (deltaEta <= maximum))) continue;

    
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}



      





bool
CaloCaloCorrelation_911641433388533200
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
    bool pass = false;
  size_t nobj0 = 0;
  for (size_t ii = 0; ii < data->egBx.size(); ii++)
  {
    if (not (data->egBx.at(ii) == 0)) continue;
    nobj0++;
          
        bool etaWindow1;
                              // EG22: ET >= 44 at BX = 0
      if (not (data->egIEt.at(ii) >= 44)) continue;

                        // isolation : 0xc
      if (not ((12 >> data->egIso.at(ii)) & 1)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->egIEta.at(ii)) and (data->egIEta.at(ii) <= 48));
            
          if (not etaWindow1) continue;

    size_t nobj1 = 0;
    for (size_t jj = 0; jj < data->tauBx.size(); jj++)
    {
      if (not (data->tauBx.at(jj) == 0)) continue;
      nobj1++;
              if (nobj1 > 12) break;
              
                                      // TAU26: ET >= 52 at BX = 0
      if (not (data->tauIEt.at(jj) >= 52)) continue;

                        // isolation : 0xe
      if (not ((14 >> data->tauIso.at(jj)) & 1)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->tauIEta.at(jj)) and (data->tauIEta.at(jj) <= 48));
            
          if (not etaWindow1) continue;
          long long minimum;
  long long maximum;
    int iEta = -9999999; unsigned int deltaIEta = 9999999;
        // 0.30 <= DeltaR <= 11.80
      iEta = data->egIEta.at(ii);
    deltaIEta = abs(iEta - data->tauIEta.at(jj));
      unsigned int deltaEta = LUT_DETA_EG_TAU[deltaIEta];
  
    int iPhi = data->egIPhi.at(ii);
  
  unsigned int deltaIPhi = abs(iPhi - data->tauIPhi.at(jj));
  if (deltaIPhi >= 72) deltaIPhi = 2*72 - deltaIPhi;
      unsigned int deltaPhi = LUT_DPHI_EG_TAU[deltaIPhi];
  
  long long deltaR2 = deltaEta*deltaEta + deltaPhi*deltaPhi;
    minimum = (long long)(0.09 * POW10[6]);
  maximum = (long long)(139.24 * POW10[6]);
  if (not ((minimum <= deltaR2) and (deltaR2 <= maximum))) continue;

    
      pass = true;
      break;
    }
    if (pass) break;
  }

  return pass;
}


      





bool
CaloCaloCorrelation_911641502108141008
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
    bool pass = false;
  size_t nobj0 = 0;
  for (size_t ii = 0; ii < data->egBx.size(); ii++)
  {
    if (not (data->egBx.at(ii) == 0)) continue;
    nobj0++;
          
        bool etaWindow1;
                              // EG24: ET >= 48 at BX = 0
      if (not (data->egIEt.at(ii) >= 48)) continue;

                        // isolation : 0xc
      if (not ((12 >> data->egIso.at(ii)) & 1)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->egIEta.at(ii)) and (data->egIEta.at(ii) <= 48));
            
          if (not etaWindow1) continue;

    size_t nobj1 = 0;
    for (size_t jj = 0; jj < data->tauBx.size(); jj++)
    {
      if (not (data->tauBx.at(jj) == 0)) continue;
      nobj1++;
              if (nobj1 > 12) break;
              
                                      // TAU27: ET >= 54 at BX = 0
      if (not (data->tauIEt.at(jj) >= 54)) continue;

                        // isolation : 0xe
      if (not ((14 >> data->tauIso.at(jj)) & 1)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->tauIEta.at(jj)) and (data->tauIEta.at(jj) <= 48));
            
          if (not etaWindow1) continue;
          long long minimum;
  long long maximum;
    int iEta = -9999999; unsigned int deltaIEta = 9999999;
        // 0.30 <= DeltaR <= 11.80
      iEta = data->egIEta.at(ii);
    deltaIEta = abs(iEta - data->tauIEta.at(jj));
      unsigned int deltaEta = LUT_DETA_EG_TAU[deltaIEta];
  
    int iPhi = data->egIPhi.at(ii);
  
  unsigned int deltaIPhi = abs(iPhi - data->tauIPhi.at(jj));
  if (deltaIPhi >= 72) deltaIPhi = 2*72 - deltaIPhi;
      unsigned int deltaPhi = LUT_DPHI_EG_TAU[deltaIPhi];
  
  long long deltaR2 = deltaEta*deltaEta + deltaPhi*deltaPhi;
    minimum = (long long)(0.09 * POW10[6]);
  maximum = (long long)(139.24 * POW10[6]);
  if (not ((minimum <= deltaR2) and (deltaR2 <= maximum))) continue;

    
      pass = true;
      break;
    }
    if (pass) break;
  }

  return pass;
}


      





bool
CaloCaloCorrelation_9825171649083341880
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
    bool pass = false;
  size_t nobj0 = 0;
  for (size_t ii = 0; ii < data->egBx.size(); ii++)
  {
    if (not (data->egBx.at(ii) == 0)) continue;
    nobj0++;
          
        bool etaWindow1;
                              // EG24: ET >= 48 at BX = 0
      if (not (data->egIEt.at(ii) >= 48)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->egIEta.at(ii)) and (data->egIEta.at(ii) <= 48));
            
                        // isolation : 0xc
      if (not ((12 >> data->egIso.at(ii)) & 1)) continue;

          if (not etaWindow1) continue;

    size_t nobj1 = 0;
    for (size_t jj = 0; jj < data->jetBx.size(); jj++)
    {
      if (not (data->jetBx.at(jj) == 0)) continue;
      nobj1++;
              
                                      // JET26: ET >= 52 at BX = 0
      if (not (data->jetIEt.at(jj) >= 52)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(jj)) and (data->jetIEta.at(jj) <= 61));
            
          if (not etaWindow1) continue;
          long long minimum;
  long long maximum;
    int iEta = -9999999; unsigned int deltaIEta = 9999999;
        // 0.30 <= DeltaR <= 11.80
      iEta = data->egIEta.at(ii);
    deltaIEta = abs(iEta - data->jetIEta.at(jj));
      unsigned int deltaEta = LUT_DETA_EG_JET[deltaIEta];
  
    int iPhi = data->egIPhi.at(ii);
  
  unsigned int deltaIPhi = abs(iPhi - data->jetIPhi.at(jj));
  if (deltaIPhi >= 72) deltaIPhi = 2*72 - deltaIPhi;
      unsigned int deltaPhi = LUT_DPHI_EG_JET[deltaIPhi];
  
  long long deltaR2 = deltaEta*deltaEta + deltaPhi*deltaPhi;
    minimum = (long long)(0.09 * POW10[6]);
  maximum = (long long)(139.24 * POW10[6]);
  if (not ((minimum <= deltaR2) and (deltaR2 <= maximum))) continue;

    
      pass = true;
      break;
    }
    if (pass) break;
  }

  return pass;
}


      




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
CaloMuonCorrelation_1722762447326210349
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
    bool pass = false;
  size_t nobj0 = 0;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj0++;
          
        bool etaWindow1;
                              // JET32: ET >= 64 at BX = 0
      if (not (data->jetIEt.at(ii) >= 64)) continue;

                        // -2.3055 <= eta <= 2.3055
              etaWindow1 = ((-53 <= data->jetIEta.at(ii)) and (data->jetIEta.at(ii) <= 52));
            
          if (not etaWindow1) continue;
    size_t nobj1 = 0;
    for (size_t jj = 0; jj < data->muonBx.size(); jj++)
    {
      if (not (data->muonBx.at(jj) == 0)) continue;
      nobj1++;
        
                                      // MU10: ET >= 21 at BX = 0
      if (not (data->muonIEt.at(jj) >= 21)) continue;

                        // -2.3000625 <= eta <= 2.3000625
              etaWindow1 = ((-211 <= data->muonIEtaAtVtx.at(jj)) and (data->muonIEtaAtVtx.at(jj) <= 211));
            
                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(jj)) & 1)) continue;

          if (not etaWindow1) continue;
          long long minimum;
  long long maximum;
    int iEta = -9999999; unsigned int deltaIEta = 9999999;
        // 0.00 <= DeltaR <= 0.40
      iEta = data->jetIEta.at(ii);
      if (iEta < 0) iEta += 256;
    iEta = LUT_ETA_JET2MU[iEta];
    deltaIEta = abs(iEta - data->muonIEtaAtVtx.at(jj));
      unsigned int deltaEta = LUT_DETA_JET_MU[deltaIEta];
  
    int iPhi = data->jetIPhi.at(ii);
      iPhi = LUT_PHI_JET2MU[iPhi];
  
  unsigned int deltaIPhi = abs(iPhi - data->muonIPhiAtVtx.at(jj));
  if (deltaIPhi >= 288) deltaIPhi = 2*288 - deltaIPhi;
      unsigned int deltaPhi = LUT_DPHI_JET_MU[deltaIPhi];
  
  long long deltaR2 = deltaEta*deltaEta + deltaPhi*deltaPhi;
    minimum = (long long)(0.0 * POW10[6]);
  maximum = (long long)(0.161 * POW10[6]);
  if (not ((minimum <= deltaR2) and (deltaR2 <= maximum))) continue;

    
      pass = true;
      break;
    }
    if (pass) break;
  }

  return pass;
}

      






bool
CaloMuonCorrelation_3992576659521005869
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
    bool pass = false;
  size_t nobj0 = 0;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj0++;
          
        bool etaWindow1;
                              // JET40: ET >= 80 at BX = 0
      if (not (data->jetIEt.at(ii) >= 80)) continue;

                        // -2.3055 <= eta <= 2.3055
              etaWindow1 = ((-53 <= data->jetIEta.at(ii)) and (data->jetIEta.at(ii) <= 52));
            
          if (not etaWindow1) continue;
    size_t nobj1 = 0;
    for (size_t jj = 0; jj < data->muonBx.size(); jj++)
    {
      if (not (data->muonBx.at(jj) == 0)) continue;
      nobj1++;
        
                                      // MU12: ET >= 25 at BX = 0
      if (not (data->muonIEt.at(jj) >= 25)) continue;

                        // -2.3000625 <= eta <= 2.3000625
              etaWindow1 = ((-211 <= data->muonIEtaAtVtx.at(jj)) and (data->muonIEtaAtVtx.at(jj) <= 211));
            
                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(jj)) & 1)) continue;

          if (not etaWindow1) continue;
          long long minimum;
  long long maximum;
    int iEta = -9999999; unsigned int deltaIEta = 9999999;
        // 0.00 <= DeltaR <= 0.40
      iEta = data->jetIEta.at(ii);
      if (iEta < 0) iEta += 256;
    iEta = LUT_ETA_JET2MU[iEta];
    deltaIEta = abs(iEta - data->muonIEtaAtVtx.at(jj));
      unsigned int deltaEta = LUT_DETA_JET_MU[deltaIEta];
  
    int iPhi = data->jetIPhi.at(ii);
      iPhi = LUT_PHI_JET2MU[iPhi];
  
  unsigned int deltaIPhi = abs(iPhi - data->muonIPhiAtVtx.at(jj));
  if (deltaIPhi >= 288) deltaIPhi = 2*288 - deltaIPhi;
      unsigned int deltaPhi = LUT_DPHI_JET_MU[deltaIPhi];
  
  long long deltaR2 = deltaEta*deltaEta + deltaPhi*deltaPhi;
    minimum = (long long)(0.0 * POW10[6]);
  maximum = (long long)(0.161 * POW10[6]);
  if (not ((minimum <= deltaR2) and (deltaR2 <= maximum))) continue;

    
      pass = true;
      break;
    }
    if (pass) break;
  }

  return pass;
}

      


bool
DoubleEG_13299746526186732683
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // EG8: ET >= 16 at BX = 0
      if (not (data->egIEt.at(idx) >= 16)) continue;

                        // -2.61 <= eta <= 2.61
              etaWindow1 = ((-60 <= data->egIEta.at(idx)) and (data->egIEta.at(idx) <= 59));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // EG8: ET >= 16 at BX = 0
      if (not (data->egIEt.at(idx) >= 16)) continue;

                        // -2.61 <= eta <= 2.61
              etaWindow1 = ((-60 <= data->egIEta.at(idx)) and (data->egIEta.at(idx) <= 59));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleEG_13782406706523981474
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // EG24: ET >= 48 at BX = 0
      if (not (data->egIEt.at(idx) >= 48)) continue;

                        // isolation : 0xc
      if (not ((12 >> data->egIso.at(idx)) & 1)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // EG10: ET >= 20 at BX = 0
      if (not (data->egIEt.at(idx) >= 20)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleEG_14367260113818400607
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // EG10: ET >= 20 at BX = 0
      if (not (data->egIEt.at(idx) >= 20)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // EG10: ET >= 20 at BX = 0
      if (not (data->egIEt.at(idx) >= 20)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleEG_14367282104050956127
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // EG15: ET >= 30 at BX = 0
      if (not (data->egIEt.at(idx) >= 30)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // EG10: ET >= 20 at BX = 0
      if (not (data->egIEt.at(idx) >= 20)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleEG_14367290900143979231
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // EG17: ET >= 34 at BX = 0
      if (not (data->egIEt.at(idx) >= 34)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // EG17: ET >= 34 at BX = 0
      if (not (data->egIEt.at(idx) >= 34)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleEG_14367295298190490335
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // EG18: ET >= 36 at BX = 0
      if (not (data->egIEt.at(idx) >= 36)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // EG17: ET >= 34 at BX = 0
      if (not (data->egIEt.at(idx) >= 34)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleEG_14367823063771822943
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // EG20: ET >= 40 at BX = 0
      if (not (data->egIEt.at(idx) >= 40)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // EG18: ET >= 36 at BX = 0
      if (not (data->egIEt.at(idx) >= 36)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleEG_14367831859864844127
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // EG22: ET >= 44 at BX = 0
      if (not (data->egIEt.at(idx) >= 44)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // EG10: ET >= 20 at BX = 0
      if (not (data->egIEt.at(idx) >= 20)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleEG_14367831859864844383
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // EG22: ET >= 44 at BX = 0
      if (not (data->egIEt.at(idx) >= 44)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // EG12: ET >= 24 at BX = 0
      if (not (data->egIEt.at(idx) >= 24)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleEG_14367831859864844767
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // EG22: ET >= 44 at BX = 0
      if (not (data->egIEt.at(idx) >= 44)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // EG15: ET >= 30 at BX = 0
      if (not (data->egIEt.at(idx) >= 30)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleEG_14367836257911355231
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // EG23: ET >= 46 at BX = 0
      if (not (data->egIEt.at(idx) >= 46)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // EG10: ET >= 20 at BX = 0
      if (not (data->egIEt.at(idx) >= 20)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleEG_14367840655957867231
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // EG24: ET >= 48 at BX = 0
      if (not (data->egIEt.at(idx) >= 48)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // EG17: ET >= 34 at BX = 0
      if (not (data->egIEt.at(idx) >= 34)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleEG_14367845054004377695
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // EG25: ET >= 50 at BX = 0
      if (not (data->egIEt.at(idx) >= 50)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // EG12: ET >= 24 at BX = 0
      if (not (data->egIEt.at(idx) >= 24)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleEG_14367845054004377823
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // EG25: ET >= 50 at BX = 0
      if (not (data->egIEt.at(idx) >= 50)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // EG13: ET >= 26 at BX = 0
      if (not (data->egIEt.at(idx) >= 26)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleEG_14367845054004377951
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // EG25: ET >= 50 at BX = 0
      if (not (data->egIEt.at(idx) >= 50)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // EG14: ET >= 28 at BX = 0
      if (not (data->egIEt.at(idx) >= 28)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleEG_2355036583129339571
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // EG22: ET >= 44 at BX = 0
      if (not (data->egIEt.at(idx) >= 44)) continue;

                        // isolation : 0xc
      if (not ((12 >> data->egIso.at(idx)) & 1)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->egIEta.at(idx)) and (data->egIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // EG22: ET >= 44 at BX = 0
      if (not (data->egIEt.at(idx) >= 44)) continue;

                        // isolation : 0xc
      if (not ((12 >> data->egIso.at(idx)) & 1)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->egIEta.at(idx)) and (data->egIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleEG_2931778810409473715
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // EG24: ET >= 48 at BX = 0
      if (not (data->egIEt.at(idx) >= 48)) continue;

                        // isolation : 0xc
      if (not ((12 >> data->egIso.at(idx)) & 1)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->egIEta.at(idx)) and (data->egIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // EG24: ET >= 48 at BX = 0
      if (not (data->egIEt.at(idx) >= 48)) continue;

                        // isolation : 0xc
      if (not ((12 >> data->egIso.at(idx)) & 1)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->egIEta.at(idx)) and (data->egIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleEG_8902241742241126126
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // EG6: ET >= 12 at BX = 0
      if (not (data->egIEt.at(idx) >= 12)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // EG6: ET >= 12 at BX = 0
      if (not (data->egIEt.at(idx) >= 12)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleEG_9170720688096593570
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // EG23: ET >= 46 at BX = 0
      if (not (data->egIEt.at(idx) >= 46)) continue;

                        // isolation : 0xc
      if (not ((12 >> data->egIso.at(idx)) & 1)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // EG10: ET >= 20 at BX = 0
      if (not (data->egIEt.at(idx) >= 20)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleJET_10840719965249128790
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

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

                        // -2.61 <= eta <= 2.61
              etaWindow1 = ((-60 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 59));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET30: ET >= 60 at BX = 0
      if (not (data->jetIEt.at(idx) >= 60)) continue;

                        // -2.61 <= eta <= 2.61
              etaWindow1 = ((-60 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 59));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleJET_15894403592514695266
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

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

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET100: ET >= 200 at BX = 0
      if (not (data->jetIEt.at(idx) >= 200)) continue;

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
DoubleJET_15903553762640785506
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET112: ET >= 224 at BX = 0
      if (not (data->jetIEt.at(idx) >= 224)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET112: ET >= 224 at BX = 0
      if (not (data->jetIEt.at(idx) >= 224)) continue;

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
DoubleJET_15912422389070688354
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

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

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET120: ET >= 240 at BX = 0
      if (not (data->jetIEt.at(idx) >= 240)) continue;

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
DoubleJET_15939450583904677986
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET150: ET >= 300 at BX = 0
      if (not (data->jetIEt.at(idx) >= 300)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET150: ET >= 300 at BX = 0
      if (not (data->jetIEt.at(idx) >= 300)) continue;

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
DoubleJET_16307690244847013269
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

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

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET30: ET >= 60 at BX = 0
      if (not (data->jetIEt.at(idx) >= 60)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleJET_16307690244847013909
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

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

          
            idx = candidates.at(set.at(indicies.at(1)));
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
DoubleJET_16379747838884941845
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

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

          
            idx = candidates.at(set.at(indicies.at(1)));
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
DoubleJET_16379747838884957589
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

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

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET40: ET >= 80 at BX = 0
      if (not (data->jetIEt.at(idx) >= 80)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleJET_16382562588652048405
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET115: ET >= 230 at BX = 0
      if (not (data->jetIEt.at(idx) >= 230)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
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
DoubleJET_16382562588652064149
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET115: ET >= 230 at BX = 0
      if (not (data->jetIEt.at(idx) >= 230)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET40: ET >= 80 at BX = 0
      if (not (data->jetIEt.at(idx) >= 80)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleJET_17504692923644168291
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

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

                        // -5.0 <= eta <= -3.0015
              etaWindow1 = ((-115 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= -70));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET30: ET >= 60 at BX = 0
      if (not (data->jetIEt.at(idx) >= 60)) continue;

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
DoubleJET_3730266969229109735
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET30: ET >= 60 at BX = 0
      if (not (data->jetIEt.at(idx) >= 60)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET30: ET >= 60 at BX = 0
      if (not (data->jetIEt.at(idx) >= 60)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleJET_3805139313034161255
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET45: ET >= 90 at BX = 0
      if (not (data->jetIEt.at(idx) >= 90)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET45: ET >= 90 at BX = 0
      if (not (data->jetIEt.at(idx) >= 90)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleJET_3851467703317088356
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

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

                        // 3.0015 <= eta <= 5.0
              etaWindow1 = ((69 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 114));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET30: ET >= 60 at BX = 0
      if (not (data->jetIEt.at(idx) >= 60)) continue;

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
DoubleJET_3851467703875127396
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

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

                        // 3.0015 <= eta <= 5.0
              etaWindow1 = ((69 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 114));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET30: ET >= 60 at BX = 0
      if (not (data->jetIEt.at(idx) >= 60)) continue;

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
DoubleJET_4162612533456677351
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

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

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET30: ET >= 60 at BX = 0
      if (not (data->jetIEt.at(idx) >= 60)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleJET_7821119012726214247
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

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

                        // -2.61 <= eta <= 2.61
              etaWindow1 = ((-60 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 59));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET30: ET >= 60 at BX = 0
      if (not (data->jetIEt.at(idx) >= 60)) continue;

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
DoubleJET_7821119013284253287
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

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

                        // -2.61 <= eta <= 2.61
              etaWindow1 = ((-60 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 59));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET30: ET >= 60 at BX = 0
      if (not (data->jetIEt.at(idx) >= 60)) continue;

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
DoubleJET_8659155958470085331
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET40: ET >= 80 at BX = 0
      if (not (data->jetIEt.at(idx) >= 80)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET40: ET >= 80 at BX = 0
      if (not (data->jetIEt.at(idx) >= 80)) continue;

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
DoubleJET_8659228526237518547
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

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

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET50: ET >= 100 at BX = 0
      if (not (data->jetIEt.at(idx) >= 100)) continue;

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
DoubleJET_8659301094004951763
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

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

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET60: ET >= 120 at BX = 0
      if (not (data->jetIEt.at(idx) >= 120)) continue;

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
DoubleJET_8659446229539818195
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET80: ET >= 160 at BX = 0
      if (not (data->jetIEt.at(idx) >= 160)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET80: ET >= 160 at BX = 0
      if (not (data->jetIEt.at(idx) >= 160)) continue;

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
DoubleMU_13627348644483379947
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // MU4p5: ET >= 10 at BX = 0
      if (not (data->muonIEt.at(idx) >= 10)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx)) & 1)) continue;

                        // -2.0064375 <= eta <= 2.0064375
              etaWindow1 = ((-184 <= data->muonIEtaAtVtx.at(idx)) and (data->muonIEtaAtVtx.at(idx) <= 184));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // MU4p5: ET >= 10 at BX = 0
      if (not (data->muonIEt.at(idx) >= 10)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx)) & 1)) continue;

                        // -2.0064375 <= eta <= 2.0064375
              etaWindow1 = ((-184 <= data->muonIEtaAtVtx.at(idx)) and (data->muonIEtaAtVtx.at(idx) <= 184));
            
          if (not etaWindow1) continue;
            
      // charge correlation
      bool equal = true;
      bool invalid = false;
      for (size_t mm = 0; mm < 2 -1; mm++)
      {
        int idx0 = candidates.at(set.at(indicies.at(mm)));
        int idx1 = candidates.at(set.at(indicies.at(mm+1)));
        if ((data->muonChg.at(idx0) == 0) or (data->muonChg.at(idx1) == 0))
        {
          invalid = true;
          break;
        }
        if (data->muonChg.at(idx0) != data->muonChg.at(idx1))
        {
          equal = false;
          break;
        }
      }
      if (invalid) continue;

      // charge correlation: "os"
      if (equal) continue;

      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleMU_14585777620730815295
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

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

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // MU0: ET >= 1 at BX = 0
      if (not (data->muonIEt.at(idx) >= 1)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleMU_14585778268989477695
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

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

          
            idx = candidates.at(set.at(indicies.at(1)));
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
DoubleMU_14585786515326686015
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

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

          
            idx = candidates.at(set.at(indicies.at(1)));
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
DoubleMU_14585796862184301375
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

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

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // MU7: ET >= 15 at BX = 0
      if (not (data->muonIEt.at(idx) >= 15)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleMU_14585797510442963775
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

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

          
            idx = candidates.at(set.at(indicies.at(1)));
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
DoubleMU_14585800259222033215
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

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

          
            idx = candidates.at(set.at(indicies.at(1)));
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
DoubleMU_14617142003772573591
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

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

                        // -1.5061875 <= eta <= 1.5061875
              etaWindow1 = ((-138 <= data->muonIEtaAtVtx.at(idx)) and (data->muonIEtaAtVtx.at(idx) <= 138));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // MU0: ET >= 1 at BX = 0
      if (not (data->muonIEt.at(idx) >= 1)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx)) & 1)) continue;

                        // -1.5061875 <= eta <= 1.5061875
              etaWindow1 = ((-138 <= data->muonIEtaAtVtx.at(idx)) and (data->muonIEtaAtVtx.at(idx) <= 138));
            
          if (not etaWindow1) continue;
            
      // charge correlation
      bool equal = true;
      bool invalid = false;
      for (size_t mm = 0; mm < 2 -1; mm++)
      {
        int idx0 = candidates.at(set.at(indicies.at(mm)));
        int idx1 = candidates.at(set.at(indicies.at(mm+1)));
        if ((data->muonChg.at(idx0) == 0) or (data->muonChg.at(idx1) == 0))
        {
          invalid = true;
          break;
        }
        if (data->muonChg.at(idx0) != data->muonChg.at(idx1))
        {
          equal = false;
          break;
        }
      }
      if (invalid) continue;

      // charge correlation: "os"
      if (equal) continue;

      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleMU_16323903523977050720
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // MU18: ET >= 37 at BX = 0
      if (not (data->muonIEt.at(idx) >= 37)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx)) & 1)) continue;

                        // -2.1043125 <= eta <= 2.1043125
              etaWindow1 = ((-193 <= data->muonIEtaAtVtx.at(idx)) and (data->muonIEtaAtVtx.at(idx) <= 193));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // MU18: ET >= 37 at BX = 0
      if (not (data->muonIEt.at(idx) >= 37)) continue;

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
DoubleMU_16961154507842811908
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // MU11: ET >= 23 at BX = 0
      if (not (data->muonIEt.at(idx) >= 23)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // MU4: ET >= 9 at BX = 0
      if (not (data->muonIEt.at(idx) >= 9)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleMU_16961157256621881348
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // MU12: ET >= 25 at BX = 0
      if (not (data->muonIEt.at(idx) >= 25)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // MU5: ET >= 11 at BX = 0
      if (not (data->muonIEt.at(idx) >= 11)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleMU_16961158905889323012
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

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

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // MU5: ET >= 11 at BX = 0
      if (not (data->muonIEt.at(idx) >= 11)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleMU_16961159554147985412
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

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

          
            idx = candidates.at(set.at(indicies.at(1)));
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
DoubleMU_16961160005400950788
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // MU13: ET >= 27 at BX = 0
      if (not (data->muonIEt.at(idx) >= 27)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // MU6: ET >= 13 at BX = 0
      if (not (data->muonIEt.at(idx) >= 13)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleMU_16961163303935834116
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

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

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // MU7: ET >= 15 at BX = 0
      if (not (data->muonIEt.at(idx) >= 15)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleMU_16961163853691648004
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // MU12: ET >= 25 at BX = 0
      if (not (data->muonIEt.at(idx) >= 25)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // MU8: ET >= 17 at BX = 0
      if (not (data->muonIEt.at(idx) >= 17)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleMU_16961163952194496516
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

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

          
            idx = candidates.at(set.at(indicies.at(1)));
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
DoubleMU_17582786187978172426
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // MU4p5: ET >= 10 at BX = 0
      if (not (data->muonIEt.at(idx) >= 10)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx)) & 1)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // MU4p5: ET >= 10 at BX = 0
      if (not (data->muonIEt.at(idx) >= 10)) continue;

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
DoubleMU_2011765979326275391
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // MU4p5: ET >= 10 at BX = 0
      if (not (data->muonIEt.at(idx) >= 10)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx)) & 1)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // MU4p5: ET >= 10 at BX = 0
      if (not (data->muonIEt.at(idx) >= 10)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx)) & 1)) continue;

          
            
      // charge correlation
      bool equal = true;
      bool invalid = false;
      for (size_t mm = 0; mm < 2 -1; mm++)
      {
        int idx0 = candidates.at(set.at(indicies.at(mm)));
        int idx1 = candidates.at(set.at(indicies.at(mm+1)));
        if ((data->muonChg.at(idx0) == 0) or (data->muonChg.at(idx1) == 0))
        {
          invalid = true;
          break;
        }
        if (data->muonChg.at(idx0) != data->muonChg.at(idx1))
        {
          equal = false;
          break;
        }
      }
      if (invalid) continue;

      // charge correlation: "os"
      if (equal) continue;

      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleMU_2488845469206592112
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // MU22: ET >= 45 at BX = 0
      if (not (data->muonIEt.at(idx) >= 45)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx)) & 1)) continue;

                        // -2.1043125 <= eta <= 2.1043125
              etaWindow1 = ((-193 <= data->muonIEtaAtVtx.at(idx)) and (data->muonIEtaAtVtx.at(idx) <= 193));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // MU22: ET >= 45 at BX = 0
      if (not (data->muonIEt.at(idx) >= 45)) continue;

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
DoubleMU_3139255731352238604
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

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

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // MU0: ET >= 1 at BX = 0
      if (not (data->muonIEt.at(idx) >= 1)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx)) & 1)) continue;

          
            
      // charge correlation
      bool equal = true;
      bool invalid = false;
      for (size_t mm = 0; mm < 2 -1; mm++)
      {
        int idx0 = candidates.at(set.at(indicies.at(mm)));
        int idx1 = candidates.at(set.at(indicies.at(mm+1)));
        if ((data->muonChg.at(idx0) == 0) or (data->muonChg.at(idx1) == 0))
        {
          invalid = true;
          break;
        }
        if (data->muonChg.at(idx0) != data->muonChg.at(idx1))
        {
          equal = false;
          break;
        }
      }
      if (invalid) continue;

      // charge correlation: "os"
      if (equal) continue;

      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleMU_3224017188937267724
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // MU4: ET >= 9 at BX = 0
      if (not (data->muonIEt.at(idx) >= 9)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // MU4: ET >= 9 at BX = 0
      if (not (data->muonIEt.at(idx) >= 9)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            
      // charge correlation
      bool equal = true;
      bool invalid = false;
      for (size_t mm = 0; mm < 2 -1; mm++)
      {
        int idx0 = candidates.at(set.at(indicies.at(mm)));
        int idx1 = candidates.at(set.at(indicies.at(mm+1)));
        if ((data->muonChg.at(idx0) == 0) or (data->muonChg.at(idx1) == 0))
        {
          invalid = true;
          break;
        }
        if (data->muonChg.at(idx0) != data->muonChg.at(idx1))
        {
          equal = false;
          break;
        }
      }
      if (invalid) continue;

      // charge correlation: "os"
      if (equal) continue;

      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleMU_3229327723899648524
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // MU4: ET >= 9 at BX = 0
      if (not (data->muonIEt.at(idx) >= 9)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx)) & 1)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // MU4: ET >= 9 at BX = 0
      if (not (data->muonIEt.at(idx) >= 9)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx)) & 1)) continue;

          
            
      // charge correlation
      bool equal = true;
      bool invalid = false;
      for (size_t mm = 0; mm < 2 -1; mm++)
      {
        int idx0 = candidates.at(set.at(indicies.at(mm)));
        int idx1 = candidates.at(set.at(indicies.at(mm+1)));
        if ((data->muonChg.at(idx0) == 0) or (data->muonChg.at(idx1) == 0))
        {
          invalid = true;
          break;
        }
        if (data->muonChg.at(idx0) != data->muonChg.at(idx1))
        {
          equal = false;
          break;
        }
      }
      if (invalid) continue;

      // charge correlation: "os"
      if (equal) continue;

      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleMU_3246535187074120204
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

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

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // MU5: ET >= 11 at BX = 0
      if (not (data->muonIEt.at(idx) >= 11)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            
      // charge correlation
      bool equal = true;
      bool invalid = false;
      for (size_t mm = 0; mm < 2 -1; mm++)
      {
        int idx0 = candidates.at(set.at(indicies.at(mm)));
        int idx1 = candidates.at(set.at(indicies.at(mm+1)));
        if ((data->muonChg.at(idx0) == 0) or (data->muonChg.at(idx1) == 0))
        {
          invalid = true;
          break;
        }
        if (data->muonChg.at(idx0) != data->muonChg.at(idx1))
        {
          equal = false;
          break;
        }
      }
      if (invalid) continue;

      // charge correlation: "os"
      if (equal) continue;

      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleMU_3251845722036501004
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

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

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // MU5: ET >= 11 at BX = 0
      if (not (data->muonIEt.at(idx) >= 11)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx)) & 1)) continue;

          
            
      // charge correlation
      bool equal = true;
      bool invalid = false;
      for (size_t mm = 0; mm < 2 -1; mm++)
      {
        int idx0 = candidates.at(set.at(indicies.at(mm)));
        int idx1 = candidates.at(set.at(indicies.at(mm+1)));
        if ((data->muonChg.at(idx0) == 0) or (data->muonChg.at(idx1) == 0))
        {
          invalid = true;
          break;
        }
        if (data->muonChg.at(idx0) != data->muonChg.at(idx1))
        {
          equal = false;
          break;
        }
      }
      if (invalid) continue;

      // charge correlation: "os"
      if (equal) continue;

      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleMU_3274363720173353484
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

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

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // MU6: ET >= 13 at BX = 0
      if (not (data->muonIEt.at(idx) >= 13)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx)) & 1)) continue;

          
            
      // charge correlation
      bool equal = true;
      bool invalid = false;
      for (size_t mm = 0; mm < 2 -1; mm++)
      {
        int idx0 = candidates.at(set.at(indicies.at(mm)));
        int idx1 = candidates.at(set.at(indicies.at(mm+1)));
        if ((data->muonChg.at(idx0) == 0) or (data->muonChg.at(idx1) == 0))
        {
          invalid = true;
          break;
        }
        if (data->muonChg.at(idx0) != data->muonChg.at(idx1))
        {
          equal = false;
          break;
        }
      }
      if (invalid) continue;

      // charge correlation: "os"
      if (equal) continue;

      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleTAU_10196652277112847102
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->tauBx.size(); ii++)
  {
    if (not (data->tauBx.at(ii) == 0)) continue;
    nobj++;
          if (nobj > 12) break;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // TAU36: ET >= 72 at BX = 0
      if (not (data->tauIEt.at(idx) >= 72)) continue;

                        // isolation : 0xe
      if (not ((14 >> data->tauIso.at(idx)) & 1)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->tauIEta.at(idx)) and (data->tauIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // TAU36: ET >= 72 at BX = 0
      if (not (data->tauIEt.at(idx) >= 72)) continue;

                        // isolation : 0xe
      if (not ((14 >> data->tauIso.at(idx)) & 1)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->tauIEta.at(idx)) and (data->tauIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleTAU_14808338227894500078
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->tauBx.size(); ii++)
  {
    if (not (data->tauBx.at(ii) == 0)) continue;
    nobj++;
          if (nobj > 12) break;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // TAU28: ET >= 56 at BX = 0
      if (not (data->tauIEt.at(idx) >= 56)) continue;

                        // isolation : 0xe
      if (not ((14 >> data->tauIso.at(idx)) & 1)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->tauIEta.at(idx)) and (data->tauIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // TAU28: ET >= 56 at BX = 0
      if (not (data->tauIEt.at(idx) >= 56)) continue;

                        // isolation : 0xe
      if (not ((14 >> data->tauIso.at(idx)) & 1)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->tauIEta.at(idx)) and (data->tauIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleTAU_14808338292319009533
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->tauBx.size(); ii++)
  {
    if (not (data->tauBx.at(ii) == 0)) continue;
    nobj++;
          if (nobj > 12) break;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // TAU30: ET >= 60 at BX = 0
      if (not (data->tauIEt.at(idx) >= 60)) continue;

                        // isolation : 0xe
      if (not ((14 >> data->tauIso.at(idx)) & 1)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->tauIEta.at(idx)) and (data->tauIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // TAU30: ET >= 60 at BX = 0
      if (not (data->tauIEt.at(idx) >= 60)) continue;

                        // isolation : 0xe
      if (not ((14 >> data->tauIso.at(idx)) & 1)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->tauIEta.at(idx)) and (data->tauIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleTAU_14808338296613976830
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->tauBx.size(); ii++)
  {
    if (not (data->tauBx.at(ii) == 0)) continue;
    nobj++;
          if (nobj > 12) break;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // TAU38: ET >= 76 at BX = 0
      if (not (data->tauIEt.at(idx) >= 76)) continue;

                        // isolation : 0xe
      if (not ((14 >> data->tauIso.at(idx)) & 1)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->tauIEta.at(idx)) and (data->tauIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // TAU38: ET >= 76 at BX = 0
      if (not (data->tauIEt.at(idx) >= 76)) continue;

                        // isolation : 0xe
      if (not ((14 >> data->tauIso.at(idx)) & 1)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->tauIEta.at(idx)) and (data->tauIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleTAU_15233202657361500387
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->tauBx.size(); ii++)
  {
    if (not (data->tauBx.at(ii) == 0)) continue;
    nobj++;
          if (nobj > 12) break;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // TAU50: ET >= 100 at BX = 0
      if (not (data->tauIEt.at(idx) >= 100)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->tauIEta.at(idx)) and (data->tauIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // TAU50: ET >= 100 at BX = 0
      if (not (data->tauIEt.at(idx) >= 100)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->tauIEta.at(idx)) and (data->tauIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleTAU_17539608616528615651
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->tauBx.size(); ii++)
  {
    if (not (data->tauBx.at(ii) == 0)) continue;
    nobj++;
          if (nobj > 12) break;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // TAU70: ET >= 140 at BX = 0
      if (not (data->tauIEt.at(idx) >= 140)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->tauIEta.at(idx)) and (data->tauIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // TAU70: ET >= 140 at BX = 0
      if (not (data->tauIEt.at(idx) >= 140)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->tauIEta.at(idx)) and (data->tauIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleTAU_3279123247861152510
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->tauBx.size(); ii++)
  {
    if (not (data->tauBx.at(ii) == 0)) continue;
    nobj++;
          if (nobj > 12) break;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // TAU33: ET >= 66 at BX = 0
      if (not (data->tauIEt.at(idx) >= 66)) continue;

                        // isolation : 0xe
      if (not ((14 >> data->tauIso.at(idx)) & 1)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->tauIEta.at(idx)) and (data->tauIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // TAU33: ET >= 66 at BX = 0
      if (not (data->tauIEt.at(idx) >= 66)) continue;

                        // isolation : 0xe
      if (not ((14 >> data->tauIso.at(idx)) & 1)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->tauIEta.at(idx)) and (data->tauIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleTAU_5584966257611717374
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->tauBx.size(); ii++)
  {
    if (not (data->tauBx.at(ii) == 0)) continue;
    nobj++;
          if (nobj > 12) break;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // TAU34: ET >= 68 at BX = 0
      if (not (data->tauIEt.at(idx) >= 68)) continue;

                        // isolation : 0xe
      if (not ((14 >> data->tauIso.at(idx)) & 1)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->tauIEta.at(idx)) and (data->tauIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // TAU34: ET >= 68 at BX = 0
      if (not (data->tauIEt.at(idx) >= 68)) continue;

                        // isolation : 0xe
      if (not ((14 >> data->tauIso.at(idx)) & 1)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->tauIEta.at(idx)) and (data->tauIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleTAU_7890809267362282238
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->tauBx.size(); ii++)
  {
    if (not (data->tauBx.at(ii) == 0)) continue;
    nobj++;
          if (nobj > 12) break;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // TAU35: ET >= 70 at BX = 0
      if (not (data->tauIEt.at(idx) >= 70)) continue;

                        // isolation : 0xe
      if (not ((14 >> data->tauIso.at(idx)) & 1)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->tauIEta.at(idx)) and (data->tauIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // TAU35: ET >= 70 at BX = 0
      if (not (data->tauIEt.at(idx) >= 70)) continue;

                        // isolation : 0xe
      if (not ((14 >> data->tauIso.at(idx)) & 1)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->tauIEta.at(idx)) and (data->tauIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
DoubleTAU_973280238110587646
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->tauBx.size(); ii++)
  {
    if (not (data->tauBx.at(ii) == 0)) continue;
    nobj++;
          if (nobj > 12) break;
               candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // TAU32: ET >= 64 at BX = 0
      if (not (data->tauIEt.at(idx) >= 64)) continue;

                        // isolation : 0xe
      if (not ((14 >> data->tauIso.at(idx)) & 1)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->tauIEta.at(idx)) and (data->tauIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // TAU32: ET >= 64 at BX = 0
      if (not (data->tauIEt.at(idx) >= 64)) continue;

                        // isolation : 0xe
      if (not ((14 >> data->tauIso.at(idx)) & 1)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->tauIEta.at(idx)) and (data->tauIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

                          

  



bool
InvariantMassOvRm_10967205787862279205
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
        // remove overlap -- reference: TAU45
  std::vector<int> reference;
    size_t nref = 0;
  for (size_t ii = 0; ii < data->tauBx.size(); ii++)
  {
    if (not (data->tauBx.at(ii) == 0)) continue;
    nref++;
          if (nref > 12) break;
          
                              // TAU45: ET >= 90 at BX = 0
      if (not (data->tauIEt.at(ii) >= 90)) continue;

                        // isolation : 0xe
      if (not ((14 >> data->tauIso.at(ii)) & 1)) continue;

          
    reference.push_back(ii);
  }
  if (not reference.size()) return false;

    size_t nobj0 = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj0++;
                     int iEta = -9999999; unsigned int deltaIEta = 9999999;
                          
  // remove overlap -- target: JET35
       // 0.00 <= DeltaR <= 0.20
  long long minDeltaR2 = std::numeric_limits<long long>::max();
  const long long cutDeltaR2Min = (long long)(0.0 * POW10[6]);
  const long long cutDeltaR2Max = (long long)(0.041 * POW10[6]);
         
  // compute minimum distance to reference objects
  for (size_t _jj = 0; _jj < reference.size(); _jj++)
  {
    const int index = reference.at(_jj);
                iEta = data->jetIEta.at(ii);
    deltaIEta = abs(iEta - data->tauIEta.at(index));
      unsigned int deltaEta = LUT_DETA_JET_TAU[deltaIEta];
  
    int iPhi = data->jetIPhi.at(ii);
  
  unsigned int deltaIPhi = abs(iPhi - data->tauIPhi.at(index));
  if (deltaIPhi >= 72) deltaIPhi = 2*72 - deltaIPhi;
      unsigned int deltaPhi = LUT_DPHI_JET_TAU[deltaIPhi];
  
  long long deltaR2 = deltaEta*deltaEta + deltaPhi*deltaPhi;
      if (deltaR2 < minDeltaR2) minDeltaR2 = deltaR2;
                  }

  // skip if needed
      if ((cutDeltaR2Min <= minDeltaR2) and (minDeltaR2 <= cutDeltaR2Max)) continue;

        
        candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      
      const int idx0 = candidates.at(set.at(indicies.at(0)));
      const int idx1 = candidates.at(set.at(indicies.at(1)));
                                // JET35: ET >= 70 at BX = 0
      if (not (data->jetIEt.at(idx0) >= 70)) continue;

          
                                // JET35: ET >= 70 at BX = 0
      if (not (data->jetIEt.at(idx1) >= 70)) continue;

          
          long long minimum;
  long long maximum;

  int iEta = -9999999; unsigned int deltaIEta = 9999999;
            // 450.0 <= mass <= 14000.0
      iEta = data->jetIEta.at(idx0);
    deltaIEta = abs(iEta - data->jetIEta.at(idx1));
  
    int iPhi = data->jetIPhi.at(idx0);
  
  unsigned int deltaIPhi = abs(iPhi - data->jetIPhi.at(idx1));
  if (deltaIPhi >= 72) deltaIPhi = 2*72 - deltaIPhi;
  
  long long coshDeltaEta = LUT_COSH_DETA_JET_JET[deltaIEta];
  long long cosDeltaPhi = LUT_COS_DPHI_JET_JET[deltaIPhi];
  long long pt0 = LUT_JET_ET[data->jetIEt.at(idx0)];
  long long pt1 = LUT_JET_ET[data->jetIEt.at(idx1)];
  long long mass2 = pt0*pt1*(coshDeltaEta - cosDeltaPhi);
    minimum = (long long)(101250.0 * POW10[5]);
  maximum = (long long)(98000000.0 * POW10[5]);
  if (not ((minimum <= mass2) and (mass2 <= maximum))) continue;

    
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}


    
                    





bool
InvariantMass_13689376201502793133
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      bool etaWindow1;
      const int idx0 = candidates.at(set.at(indicies.at(0)));
      const int idx1 = candidates.at(set.at(indicies.at(1)));
                                // MU5: ET >= 11 at BX = 0
      if (not (data->muonIEt.at(idx0) >= 11)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx0)) & 1)) continue;

                        // -2.3000625 <= eta <= 2.3000625
              etaWindow1 = ((-211 <= data->muonIEtaAtVtx.at(idx0)) and (data->muonIEtaAtVtx.at(idx0) <= 211));
            
          if (not etaWindow1) continue;
                                // MU5: ET >= 11 at BX = 0
      if (not (data->muonIEt.at(idx1) >= 11)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx1)) & 1)) continue;

                        // -2.3000625 <= eta <= 2.3000625
              etaWindow1 = ((-211 <= data->muonIEtaAtVtx.at(idx1)) and (data->muonIEtaAtVtx.at(idx1) <= 211));
            
          if (not etaWindow1) continue;
          long long minimum;
  long long maximum;

  int iEta = -9999999; unsigned int deltaIEta = 9999999;
        const std::string OS = "os";
    const std::string SS = "ls";
    if (data->muonChg.at(idx0) == 0) continue;  // charge valid bit not set
    if (data->muonChg.at(idx1) == 0) continue;  // charge valid bit not set
    if ("os" == OS)
    {
      if (not (data->muonChg.at(idx0) != data->muonChg.at(idx1))) continue;
    }
    else if ("os" == SS)
    {
      if (not (data->muonChg.at(idx0) == data->muonChg.at(idx1))) continue;
    }
          // 8.0 <= mass <= 14.0
      iEta = data->muonIEtaAtVtx.at(idx0);
    deltaIEta = abs(iEta - data->muonIEtaAtVtx.at(idx1));
  
    int iPhi = data->muonIPhiAtVtx.at(idx0);
  
  unsigned int deltaIPhi = abs(iPhi - data->muonIPhiAtVtx.at(idx1));
  if (deltaIPhi >= 288) deltaIPhi = 2*288 - deltaIPhi;
  
  long long coshDeltaEta = LUT_COSH_DETA_MU_MU[deltaIEta];
  long long cosDeltaPhi = LUT_COS_DPHI_MU_MU[deltaIPhi];
  long long pt0 = LUT_MU_ET[data->muonIEt.at(idx0)];
  long long pt1 = LUT_MU_ET[data->muonIEt.at(idx1)];
  long long mass2 = pt0*pt1*(coshDeltaEta - cosDeltaPhi);
    minimum = (long long)(32.0 * POW10[6]);
  maximum = (long long)(98.0 * POW10[6]);
  if (not ((minimum <= mass2) and (mass2 <= maximum))) continue;

    
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}


    
                    





bool
InvariantMass_14086745238924011567
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      
      const int idx0 = candidates.at(set.at(indicies.at(0)));
      const int idx1 = candidates.at(set.at(indicies.at(1)));
                                // MU5: ET >= 11 at BX = 0
      if (not (data->muonIEt.at(idx0) >= 11)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx0)) & 1)) continue;

          
                                // MU5: ET >= 11 at BX = 0
      if (not (data->muonIEt.at(idx1) >= 11)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx1)) & 1)) continue;

          
          long long minimum;
  long long maximum;

  int iEta = -9999999; unsigned int deltaIEta = 9999999;
        const std::string OS = "os";
    const std::string SS = "ls";
    if (data->muonChg.at(idx0) == 0) continue;  // charge valid bit not set
    if (data->muonChg.at(idx1) == 0) continue;  // charge valid bit not set
    if ("os" == OS)
    {
      if (not (data->muonChg.at(idx0) != data->muonChg.at(idx1))) continue;
    }
    else if ("os" == SS)
    {
      if (not (data->muonChg.at(idx0) == data->muonChg.at(idx1))) continue;
    }
          // 7.0 <= mass <= 18.0
      iEta = data->muonIEtaAtVtx.at(idx0);
    deltaIEta = abs(iEta - data->muonIEtaAtVtx.at(idx1));
  
    int iPhi = data->muonIPhiAtVtx.at(idx0);
  
  unsigned int deltaIPhi = abs(iPhi - data->muonIPhiAtVtx.at(idx1));
  if (deltaIPhi >= 288) deltaIPhi = 2*288 - deltaIPhi;
  
  long long coshDeltaEta = LUT_COSH_DETA_MU_MU[deltaIEta];
  long long cosDeltaPhi = LUT_COS_DPHI_MU_MU[deltaIPhi];
  long long pt0 = LUT_MU_ET[data->muonIEt.at(idx0)];
  long long pt1 = LUT_MU_ET[data->muonIEt.at(idx1)];
  long long mass2 = pt0*pt1*(coshDeltaEta - cosDeltaPhi);
    minimum = (long long)(24.5 * POW10[6]);
  maximum = (long long)(162.0 * POW10[6]);
  if (not ((minimum <= mass2) and (mass2 <= maximum))) continue;

    
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}


    
                    





bool
InvariantMass_15191958030943548804
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      
      const int idx0 = candidates.at(set.at(indicies.at(0)));
      const int idx1 = candidates.at(set.at(indicies.at(1)));
                                // MU5: ET >= 11 at BX = 0
      if (not (data->muonIEt.at(idx0) >= 11)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx0)) & 1)) continue;

          
                                // MU2p5: ET >= 6 at BX = 0
      if (not (data->muonIEt.at(idx1) >= 6)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx1)) & 1)) continue;

          
          long long minimum;
  long long maximum;

  int iEta = -9999999; unsigned int deltaIEta = 9999999;
        const std::string OS = "os";
    const std::string SS = "ls";
    if (data->muonChg.at(idx0) == 0) continue;  // charge valid bit not set
    if (data->muonChg.at(idx1) == 0) continue;  // charge valid bit not set
    if ("os" == OS)
    {
      if (not (data->muonChg.at(idx0) != data->muonChg.at(idx1))) continue;
    }
    else if ("os" == SS)
    {
      if (not (data->muonChg.at(idx0) == data->muonChg.at(idx1))) continue;
    }
          // 5.0 <= mass <= 17.0
      iEta = data->muonIEtaAtVtx.at(idx0);
    deltaIEta = abs(iEta - data->muonIEtaAtVtx.at(idx1));
  
    int iPhi = data->muonIPhiAtVtx.at(idx0);
  
  unsigned int deltaIPhi = abs(iPhi - data->muonIPhiAtVtx.at(idx1));
  if (deltaIPhi >= 288) deltaIPhi = 2*288 - deltaIPhi;
  
  long long coshDeltaEta = LUT_COSH_DETA_MU_MU[deltaIEta];
  long long cosDeltaPhi = LUT_COS_DPHI_MU_MU[deltaIPhi];
  long long pt0 = LUT_MU_ET[data->muonIEt.at(idx0)];
  long long pt1 = LUT_MU_ET[data->muonIEt.at(idx1)];
  long long mass2 = pt0*pt1*(coshDeltaEta - cosDeltaPhi);
    minimum = (long long)(12.5 * POW10[6]);
  maximum = (long long)(144.5 * POW10[6]);
  if (not ((minimum <= mass2) and (mass2 <= maximum))) continue;

    
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}


    
                    





bool
InvariantMass_15192153509407276420
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      
      const int idx0 = candidates.at(set.at(indicies.at(0)));
      const int idx1 = candidates.at(set.at(indicies.at(1)));
                                // MU5: ET >= 11 at BX = 0
      if (not (data->muonIEt.at(idx0) >= 11)) continue;

                        // quality : 0xfff0
      if (not ((65520 >> data->muonQual.at(idx0)) & 1)) continue;

          
                                // MU2p5: ET >= 6 at BX = 0
      if (not (data->muonIEt.at(idx1) >= 6)) continue;

                        // quality : 0xfff0
      if (not ((65520 >> data->muonQual.at(idx1)) & 1)) continue;

          
          long long minimum;
  long long maximum;

  int iEta = -9999999; unsigned int deltaIEta = 9999999;
        const std::string OS = "os";
    const std::string SS = "ls";
    if (data->muonChg.at(idx0) == 0) continue;  // charge valid bit not set
    if (data->muonChg.at(idx1) == 0) continue;  // charge valid bit not set
    if ("os" == OS)
    {
      if (not (data->muonChg.at(idx0) != data->muonChg.at(idx1))) continue;
    }
    else if ("os" == SS)
    {
      if (not (data->muonChg.at(idx0) == data->muonChg.at(idx1))) continue;
    }
          // 5.0 <= mass <= 17.0
      iEta = data->muonIEtaAtVtx.at(idx0);
    deltaIEta = abs(iEta - data->muonIEtaAtVtx.at(idx1));
  
    int iPhi = data->muonIPhiAtVtx.at(idx0);
  
  unsigned int deltaIPhi = abs(iPhi - data->muonIPhiAtVtx.at(idx1));
  if (deltaIPhi >= 288) deltaIPhi = 2*288 - deltaIPhi;
  
  long long coshDeltaEta = LUT_COSH_DETA_MU_MU[deltaIEta];
  long long cosDeltaPhi = LUT_COS_DPHI_MU_MU[deltaIPhi];
  long long pt0 = LUT_MU_ET[data->muonIEt.at(idx0)];
  long long pt1 = LUT_MU_ET[data->muonIEt.at(idx1)];
  long long mass2 = pt0*pt1*(coshDeltaEta - cosDeltaPhi);
    minimum = (long long)(12.5 * POW10[6]);
  maximum = (long long)(144.5 * POW10[6]);
  if (not ((minimum <= mass2) and (mass2 <= maximum))) continue;

    
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}


    
                    





bool
InvariantMass_15192160106477018500
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      
      const int idx0 = candidates.at(set.at(indicies.at(0)));
      const int idx1 = candidates.at(set.at(indicies.at(1)));
                                // MU5: ET >= 11 at BX = 0
      if (not (data->muonIEt.at(idx0) >= 11)) continue;

                        // quality : 0xfff0
      if (not ((65520 >> data->muonQual.at(idx0)) & 1)) continue;

          
                                // MU2p5: ET >= 6 at BX = 0
      if (not (data->muonIEt.at(idx1) >= 6)) continue;

                        // quality : 0xfff0
      if (not ((65520 >> data->muonQual.at(idx1)) & 1)) continue;

          
          long long minimum;
  long long maximum;

  int iEta = -9999999; unsigned int deltaIEta = 9999999;
        const std::string OS = "os";
    const std::string SS = "ls";
    if (data->muonChg.at(idx0) == 0) continue;  // charge valid bit not set
    if (data->muonChg.at(idx1) == 0) continue;  // charge valid bit not set
    if ("os" == OS)
    {
      if (not (data->muonChg.at(idx0) != data->muonChg.at(idx1))) continue;
    }
    else if ("os" == SS)
    {
      if (not (data->muonChg.at(idx0) == data->muonChg.at(idx1))) continue;
    }
          // 8.0 <= mass <= 14.0
      iEta = data->muonIEtaAtVtx.at(idx0);
    deltaIEta = abs(iEta - data->muonIEtaAtVtx.at(idx1));
  
    int iPhi = data->muonIPhiAtVtx.at(idx0);
  
  unsigned int deltaIPhi = abs(iPhi - data->muonIPhiAtVtx.at(idx1));
  if (deltaIPhi >= 288) deltaIPhi = 2*288 - deltaIPhi;
  
  long long coshDeltaEta = LUT_COSH_DETA_MU_MU[deltaIEta];
  long long cosDeltaPhi = LUT_COS_DPHI_MU_MU[deltaIPhi];
  long long pt0 = LUT_MU_ET[data->muonIEt.at(idx0)];
  long long pt1 = LUT_MU_ET[data->muonIEt.at(idx1)];
  long long mass2 = pt0*pt1*(coshDeltaEta - cosDeltaPhi);
    minimum = (long long)(32.0 * POW10[6]);
  maximum = (long long)(98.0 * POW10[6]);
  if (not ((minimum <= mass2) and (mass2 <= maximum))) continue;

    
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}


    
                    





bool
InvariantMass_15577908206133012537
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      
      const int idx0 = candidates.at(set.at(indicies.at(0)));
      const int idx1 = candidates.at(set.at(indicies.at(1)));
                                // MU20: ET >= 41 at BX = 0
      if (not (data->muonIEt.at(idx0) >= 41)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx0)) & 1)) continue;

          
                                // MU2: ET >= 5 at BX = 0
      if (not (data->muonIEt.at(idx1) >= 5)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx1)) & 1)) continue;

          
          long long minimum;
  long long maximum;

  int iEta = -9999999; unsigned int deltaIEta = 9999999;
        // 0.0 <= mass <= 20.0
      iEta = data->muonIEtaAtVtx.at(idx0);
    deltaIEta = abs(iEta - data->muonIEtaAtVtx.at(idx1));
  
    int iPhi = data->muonIPhiAtVtx.at(idx0);
  
  unsigned int deltaIPhi = abs(iPhi - data->muonIPhiAtVtx.at(idx1));
  if (deltaIPhi >= 288) deltaIPhi = 2*288 - deltaIPhi;
  
  long long coshDeltaEta = LUT_COSH_DETA_MU_MU[deltaIEta];
  long long cosDeltaPhi = LUT_COS_DPHI_MU_MU[deltaIPhi];
  long long pt0 = LUT_MU_ET[data->muonIEt.at(idx0)];
  long long pt1 = LUT_MU_ET[data->muonIEt.at(idx1)];
  long long mass2 = pt0*pt1*(coshDeltaEta - cosDeltaPhi);
    minimum = (long long)(0.0 * POW10[6]);
  maximum = (long long)(200.0 * POW10[6]);
  if (not ((minimum <= mass2) and (mass2 <= maximum))) continue;

    
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}


    
                    





bool
InvariantMass_16981538589298500419
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
    size_t nobj0 = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->egBx.size(); ii++)
  {
    if (not (data->egBx.at(ii) == 0)) continue;
    nobj0++;
                   candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      bool etaWindow1;
      const int idx0 = candidates.at(set.at(indicies.at(0)));
      const int idx1 = candidates.at(set.at(indicies.at(1)));
                                // EG7p5: ET >= 15 at BX = 0
      if (not (data->egIEt.at(idx0) >= 15)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->egIEta.at(idx0)) and (data->egIEta.at(idx0) <= 48));
            
          if (not etaWindow1) continue;
                                // EG7p5: ET >= 15 at BX = 0
      if (not (data->egIEt.at(idx1) >= 15)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->egIEta.at(idx1)) and (data->egIEta.at(idx1) <= 48));
            
          if (not etaWindow1) continue;
          long long minimum;
  long long maximum;

  int iEta = -9999999; unsigned int deltaIEta = 9999999;
        // 0.0 <= mass <= 20.0
      iEta = data->egIEta.at(idx0);
    deltaIEta = abs(iEta - data->egIEta.at(idx1));
  
    int iPhi = data->egIPhi.at(idx0);
  
  unsigned int deltaIPhi = abs(iPhi - data->egIPhi.at(idx1));
  if (deltaIPhi >= 72) deltaIPhi = 2*72 - deltaIPhi;
  
  long long coshDeltaEta = LUT_COSH_DETA_EG_EG[deltaIEta];
  long long cosDeltaPhi = LUT_COS_DPHI_EG_EG[deltaIPhi];
  long long pt0 = LUT_EG_ET[data->egIEt.at(idx0)];
  long long pt1 = LUT_EG_ET[data->egIEt.at(idx1)];
  long long mass2 = pt0*pt1*(coshDeltaEta - cosDeltaPhi);
    minimum = (long long)(0.0 * POW10[5]);
  maximum = (long long)(200.0 * POW10[5]);
  if (not ((minimum <= mass2) and (mass2 <= maximum))) continue;

    
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}


    
                    





bool
InvariantMass_2342552854377181621
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      bool etaWindow1;
      const int idx0 = candidates.at(set.at(indicies.at(0)));
      const int idx1 = candidates.at(set.at(indicies.at(1)));
                                // MU4p5: ET >= 10 at BX = 0
      if (not (data->muonIEt.at(idx0) >= 10)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx0)) & 1)) continue;

                        // -2.0064375 <= eta <= 2.0064375
              etaWindow1 = ((-184 <= data->muonIEtaAtVtx.at(idx0)) and (data->muonIEtaAtVtx.at(idx0) <= 184));
            
          if (not etaWindow1) continue;
                                // MU4p5: ET >= 10 at BX = 0
      if (not (data->muonIEt.at(idx1) >= 10)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx1)) & 1)) continue;

                        // -2.0064375 <= eta <= 2.0064375
              etaWindow1 = ((-184 <= data->muonIEtaAtVtx.at(idx1)) and (data->muonIEtaAtVtx.at(idx1) <= 184));
            
          if (not etaWindow1) continue;
          long long minimum;
  long long maximum;

  int iEta = -9999999; unsigned int deltaIEta = 9999999;
        const std::string OS = "os";
    const std::string SS = "ls";
    if (data->muonChg.at(idx0) == 0) continue;  // charge valid bit not set
    if (data->muonChg.at(idx1) == 0) continue;  // charge valid bit not set
    if ("os" == OS)
    {
      if (not (data->muonChg.at(idx0) != data->muonChg.at(idx1))) continue;
    }
    else if ("os" == SS)
    {
      if (not (data->muonChg.at(idx0) == data->muonChg.at(idx1))) continue;
    }
          // 7.0 <= mass <= 18.0
      iEta = data->muonIEtaAtVtx.at(idx0);
    deltaIEta = abs(iEta - data->muonIEtaAtVtx.at(idx1));
  
    int iPhi = data->muonIPhiAtVtx.at(idx0);
  
  unsigned int deltaIPhi = abs(iPhi - data->muonIPhiAtVtx.at(idx1));
  if (deltaIPhi >= 288) deltaIPhi = 2*288 - deltaIPhi;
  
  long long coshDeltaEta = LUT_COSH_DETA_MU_MU[deltaIEta];
  long long cosDeltaPhi = LUT_COS_DPHI_MU_MU[deltaIPhi];
  long long pt0 = LUT_MU_ET[data->muonIEt.at(idx0)];
  long long pt1 = LUT_MU_ET[data->muonIEt.at(idx1)];
  long long mass2 = pt0*pt1*(coshDeltaEta - cosDeltaPhi);
    minimum = (long long)(24.5 * POW10[6]);
  maximum = (long long)(162.0 * POW10[6]);
  if (not ((minimum <= mass2) and (mass2 <= maximum))) continue;

    
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}


    
                    





bool
InvariantMass_2443380592745462540
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
    size_t nobj0 = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->egBx.size(); ii++)
  {
    if (not (data->egBx.at(ii) == 0)) continue;
    nobj0++;
                   candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      bool etaWindow1;
      const int idx0 = candidates.at(set.at(indicies.at(0)));
      const int idx1 = candidates.at(set.at(indicies.at(1)));
                                // EG3: ET >= 6 at BX = 0
      if (not (data->egIEt.at(idx0) >= 6)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->egIEta.at(idx0)) and (data->egIEta.at(idx0) <= 48));
            
          if (not etaWindow1) continue;
                                // EG3: ET >= 6 at BX = 0
      if (not (data->egIEt.at(idx1) >= 6)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->egIEta.at(idx1)) and (data->egIEta.at(idx1) <= 48));
            
          if (not etaWindow1) continue;
          long long minimum;
  long long maximum;

  int iEta = -9999999; unsigned int deltaIEta = 9999999;
        // 0.0 <= mass <= 20.0
      iEta = data->egIEta.at(idx0);
    deltaIEta = abs(iEta - data->egIEta.at(idx1));
  
    int iPhi = data->egIPhi.at(idx0);
  
  unsigned int deltaIPhi = abs(iPhi - data->egIPhi.at(idx1));
  if (deltaIPhi >= 72) deltaIPhi = 2*72 - deltaIPhi;
  
  long long coshDeltaEta = LUT_COSH_DETA_EG_EG[deltaIEta];
  long long cosDeltaPhi = LUT_COS_DPHI_EG_EG[deltaIPhi];
  long long pt0 = LUT_EG_ET[data->egIEt.at(idx0)];
  long long pt1 = LUT_EG_ET[data->egIEt.at(idx1)];
  long long mass2 = pt0*pt1*(coshDeltaEta - cosDeltaPhi);
    minimum = (long long)(0.0 * POW10[5]);
  maximum = (long long)(200.0 * POW10[5]);
  if (not ((minimum <= mass2) and (mass2 <= maximum))) continue;

    
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}


    
                    





bool
InvariantMass_2940638391871890823
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
    size_t nobj0 = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj0++;
                   candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      
      const int idx0 = candidates.at(set.at(indicies.at(0)));
      const int idx1 = candidates.at(set.at(indicies.at(1)));
                                // JET30: ET >= 60 at BX = 0
      if (not (data->jetIEt.at(idx0) >= 60)) continue;

          
                                // JET30: ET >= 60 at BX = 0
      if (not (data->jetIEt.at(idx1) >= 60)) continue;

          
          long long minimum;
  long long maximum;

  int iEta = -9999999; unsigned int deltaIEta = 9999999;
        // 400.0 <= mass <= 14000.0
      iEta = data->jetIEta.at(idx0);
    deltaIEta = abs(iEta - data->jetIEta.at(idx1));
  
    int iPhi = data->jetIPhi.at(idx0);
  
  unsigned int deltaIPhi = abs(iPhi - data->jetIPhi.at(idx1));
  if (deltaIPhi >= 72) deltaIPhi = 2*72 - deltaIPhi;
  
  long long coshDeltaEta = LUT_COSH_DETA_JET_JET[deltaIEta];
  long long cosDeltaPhi = LUT_COS_DPHI_JET_JET[deltaIPhi];
  long long pt0 = LUT_JET_ET[data->jetIEt.at(idx0)];
  long long pt1 = LUT_JET_ET[data->jetIEt.at(idx1)];
  long long mass2 = pt0*pt1*(coshDeltaEta - cosDeltaPhi);
    minimum = (long long)(80000.0 * POW10[5]);
  maximum = (long long)(98000000.0 * POW10[5]);
  if (not ((minimum <= mass2) and (mass2 <= maximum))) continue;

    
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}


    
                    





bool
InvariantMass_2940638391876117895
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
    size_t nobj0 = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj0++;
                   candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      
      const int idx0 = candidates.at(set.at(indicies.at(0)));
      const int idx1 = candidates.at(set.at(indicies.at(1)));
                                // JET30: ET >= 60 at BX = 0
      if (not (data->jetIEt.at(idx0) >= 60)) continue;

          
                                // JET30: ET >= 60 at BX = 0
      if (not (data->jetIEt.at(idx1) >= 60)) continue;

          
          long long minimum;
  long long maximum;

  int iEta = -9999999; unsigned int deltaIEta = 9999999;
        // 620.0 <= mass <= 14000.0
      iEta = data->jetIEta.at(idx0);
    deltaIEta = abs(iEta - data->jetIEta.at(idx1));
  
    int iPhi = data->jetIPhi.at(idx0);
  
  unsigned int deltaIPhi = abs(iPhi - data->jetIPhi.at(idx1));
  if (deltaIPhi >= 72) deltaIPhi = 2*72 - deltaIPhi;
  
  long long coshDeltaEta = LUT_COSH_DETA_JET_JET[deltaIEta];
  long long cosDeltaPhi = LUT_COS_DPHI_JET_JET[deltaIPhi];
  long long pt0 = LUT_JET_ET[data->jetIEt.at(idx0)];
  long long pt1 = LUT_JET_ET[data->jetIEt.at(idx1)];
  long long mass2 = pt0*pt1*(coshDeltaEta - cosDeltaPhi);
    minimum = (long long)(192200.0 * POW10[5]);
  maximum = (long long)(98000000.0 * POW10[5]);
  if (not ((minimum <= mass2) and (mass2 <= maximum))) continue;

    
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}


    
                    





bool
InvariantMass_2940649386995017095
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
    size_t nobj0 = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj0++;
                   candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      
      const int idx0 = candidates.at(set.at(indicies.at(0)));
      const int idx1 = candidates.at(set.at(indicies.at(1)));
                                // JET35: ET >= 70 at BX = 0
      if (not (data->jetIEt.at(idx0) >= 70)) continue;

          
                                // JET35: ET >= 70 at BX = 0
      if (not (data->jetIEt.at(idx1) >= 70)) continue;

          
          long long minimum;
  long long maximum;

  int iEta = -9999999; unsigned int deltaIEta = 9999999;
        // 620.0 <= mass <= 14000.0
      iEta = data->jetIEta.at(idx0);
    deltaIEta = abs(iEta - data->jetIEta.at(idx1));
  
    int iPhi = data->jetIPhi.at(idx0);
  
  unsigned int deltaIPhi = abs(iPhi - data->jetIPhi.at(idx1));
  if (deltaIPhi >= 72) deltaIPhi = 2*72 - deltaIPhi;
  
  long long coshDeltaEta = LUT_COSH_DETA_JET_JET[deltaIEta];
  long long cosDeltaPhi = LUT_COS_DPHI_JET_JET[deltaIPhi];
  long long pt0 = LUT_JET_ET[data->jetIEt.at(idx0)];
  long long pt1 = LUT_JET_ET[data->jetIEt.at(idx1)];
  long long mass2 = pt0*pt1*(coshDeltaEta - cosDeltaPhi);
    minimum = (long long)(192200.0 * POW10[5]);
  maximum = (long long)(98000000.0 * POW10[5]);
  if (not ((minimum <= mass2) and (mass2 <= maximum))) continue;

    
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}


    
                    





bool
InvariantMass_2940919866919937415
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
    size_t nobj0 = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj0++;
                   candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      
      const int idx0 = candidates.at(set.at(indicies.at(0)));
      const int idx1 = candidates.at(set.at(indicies.at(1)));
                                // JET40: ET >= 80 at BX = 0
      if (not (data->jetIEt.at(idx0) >= 80)) continue;

          
                                // JET40: ET >= 80 at BX = 0
      if (not (data->jetIEt.at(idx1) >= 80)) continue;

          
          long long minimum;
  long long maximum;

  int iEta = -9999999; unsigned int deltaIEta = 9999999;
        // 620.0 <= mass <= 14000.0
      iEta = data->jetIEta.at(idx0);
    deltaIEta = abs(iEta - data->jetIEta.at(idx1));
  
    int iPhi = data->jetIPhi.at(idx0);
  
  unsigned int deltaIPhi = abs(iPhi - data->jetIPhi.at(idx1));
  if (deltaIPhi >= 72) deltaIPhi = 2*72 - deltaIPhi;
  
  long long coshDeltaEta = LUT_COSH_DETA_JET_JET[deltaIEta];
  long long cosDeltaPhi = LUT_COS_DPHI_JET_JET[deltaIPhi];
  long long pt0 = LUT_JET_ET[data->jetIEt.at(idx0)];
  long long pt1 = LUT_JET_ET[data->jetIEt.at(idx1)];
  long long mass2 = pt0*pt1*(coshDeltaEta - cosDeltaPhi);
    minimum = (long long)(192200.0 * POW10[5]);
  maximum = (long long)(98000000.0 * POW10[5]);
  if (not ((minimum <= mass2) and (mass2 <= maximum))) continue;

    
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}


    
                    





bool
InvariantMass_3063833799189854821
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      
      const int idx0 = candidates.at(set.at(indicies.at(0)));
      const int idx1 = candidates.at(set.at(indicies.at(1)));
                                // MU5: ET >= 11 at BX = 0
      if (not (data->muonIEt.at(idx0) >= 11)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx0)) & 1)) continue;

          
                                // MU3: ET >= 7 at BX = 0
      if (not (data->muonIEt.at(idx1) >= 7)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx1)) & 1)) continue;

          
          long long minimum;
  long long maximum;

  int iEta = -9999999; unsigned int deltaIEta = 9999999;
        const std::string OS = "os";
    const std::string SS = "ls";
    if (data->muonChg.at(idx0) == 0) continue;  // charge valid bit not set
    if (data->muonChg.at(idx1) == 0) continue;  // charge valid bit not set
    if ("os" == OS)
    {
      if (not (data->muonChg.at(idx0) != data->muonChg.at(idx1))) continue;
    }
    else if ("os" == SS)
    {
      if (not (data->muonChg.at(idx0) == data->muonChg.at(idx1))) continue;
    }
          // 0.0 <= mass <= 9.0
      iEta = data->muonIEtaAtVtx.at(idx0);
    deltaIEta = abs(iEta - data->muonIEtaAtVtx.at(idx1));
  
    int iPhi = data->muonIPhiAtVtx.at(idx0);
  
  unsigned int deltaIPhi = abs(iPhi - data->muonIPhiAtVtx.at(idx1));
  if (deltaIPhi >= 288) deltaIPhi = 2*288 - deltaIPhi;
  
  long long coshDeltaEta = LUT_COSH_DETA_MU_MU[deltaIEta];
  long long cosDeltaPhi = LUT_COS_DPHI_MU_MU[deltaIPhi];
  long long pt0 = LUT_MU_ET[data->muonIEt.at(idx0)];
  long long pt1 = LUT_MU_ET[data->muonIEt.at(idx1)];
  long long mass2 = pt0*pt1*(coshDeltaEta - cosDeltaPhi);
    minimum = (long long)(0.0 * POW10[6]);
  maximum = (long long)(40.5 * POW10[6]);
  if (not ((minimum <= mass2) and (mass2 <= maximum))) continue;

    
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}


    
                    





bool
InvariantMass_3136996817261618632
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      
      const int idx0 = candidates.at(set.at(indicies.at(0)));
      const int idx1 = candidates.at(set.at(indicies.at(1)));
                                // MU15: ET >= 31 at BX = 0
      if (not (data->muonIEt.at(idx0) >= 31)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx0)) & 1)) continue;

          
                                // MU7: ET >= 15 at BX = 0
      if (not (data->muonIEt.at(idx1) >= 15)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx1)) & 1)) continue;

          
          long long minimum;
  long long maximum;

  int iEta = -9999999; unsigned int deltaIEta = 9999999;
        // 4.0 <= mass <= 151982.0
      iEta = data->muonIEtaAtVtx.at(idx0);
    deltaIEta = abs(iEta - data->muonIEtaAtVtx.at(idx1));
  
    int iPhi = data->muonIPhiAtVtx.at(idx0);
  
  unsigned int deltaIPhi = abs(iPhi - data->muonIPhiAtVtx.at(idx1));
  if (deltaIPhi >= 288) deltaIPhi = 2*288 - deltaIPhi;
  
  long long coshDeltaEta = LUT_COSH_DETA_MU_MU[deltaIEta];
  long long cosDeltaPhi = LUT_COS_DPHI_MU_MU[deltaIPhi];
  long long pt0 = LUT_MU_ET[data->muonIEt.at(idx0)];
  long long pt1 = LUT_MU_ET[data->muonIEt.at(idx1)];
  long long mass2 = pt0*pt1*(coshDeltaEta - cosDeltaPhi);
    minimum = (long long)(8.0 * POW10[6]);
  maximum = (long long)(11549264162.0 * POW10[6]);
  if (not ((minimum <= mass2) and (mass2 <= maximum))) continue;

    
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}


    
                    





bool
InvariantMass_3160746219321117174
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
    size_t nobj0 = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj0++;
                   candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      
      const int idx0 = candidates.at(set.at(indicies.at(0)));
      const int idx1 = candidates.at(set.at(indicies.at(1)));
                                // JET30: ET >= 60 at BX = 0
      if (not (data->jetIEt.at(idx0) >= 60)) continue;

          
                                // JET30: ET >= 60 at BX = 0
      if (not (data->jetIEt.at(idx1) >= 60)) continue;

          
          long long minimum;
  long long maximum;

  int iEta = -9999999; unsigned int deltaIEta = 9999999;
        // 0.0 <= DeltaEta <= 1.5
      iEta = data->jetIEta.at(idx0);
    deltaIEta = abs(iEta - data->jetIEta.at(idx1));
      unsigned int deltaEta = LUT_DETA_JET_JET[deltaIEta];
  
    minimum = (long long)(0.0 * POW10[3]);
  maximum = (long long)(1.5 * POW10[3]);
  if (not ((minimum <= deltaEta) and (deltaEta <= maximum))) continue;

          // 300.0 <= mass <= 151982.0
      iEta = data->jetIEta.at(idx0);
    deltaIEta = abs(iEta - data->jetIEta.at(idx1));
  
    int iPhi = data->jetIPhi.at(idx0);
  
  unsigned int deltaIPhi = abs(iPhi - data->jetIPhi.at(idx1));
  if (deltaIPhi >= 72) deltaIPhi = 2*72 - deltaIPhi;
  
  long long coshDeltaEta = LUT_COSH_DETA_JET_JET[deltaIEta];
  long long cosDeltaPhi = LUT_COS_DPHI_JET_JET[deltaIPhi];
  long long pt0 = LUT_JET_ET[data->jetIEt.at(idx0)];
  long long pt1 = LUT_JET_ET[data->jetIEt.at(idx1)];
  long long mass2 = pt0*pt1*(coshDeltaEta - cosDeltaPhi);
    minimum = (long long)(45000.0 * POW10[5]);
  maximum = (long long)(11549264162.0 * POW10[5]);
  if (not ((minimum <= mass2) and (mass2 <= maximum))) continue;

    
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}


    
                    





bool
InvariantMass_3160750617367628278
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
    size_t nobj0 = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj0++;
                   candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      
      const int idx0 = candidates.at(set.at(indicies.at(0)));
      const int idx1 = candidates.at(set.at(indicies.at(1)));
                                // JET30: ET >= 60 at BX = 0
      if (not (data->jetIEt.at(idx0) >= 60)) continue;

          
                                // JET30: ET >= 60 at BX = 0
      if (not (data->jetIEt.at(idx1) >= 60)) continue;

          
          long long minimum;
  long long maximum;

  int iEta = -9999999; unsigned int deltaIEta = 9999999;
        // 320.0 <= mass <= 151982.0
      iEta = data->jetIEta.at(idx0);
    deltaIEta = abs(iEta - data->jetIEta.at(idx1));
  
    int iPhi = data->jetIPhi.at(idx0);
  
  unsigned int deltaIPhi = abs(iPhi - data->jetIPhi.at(idx1));
  if (deltaIPhi >= 72) deltaIPhi = 2*72 - deltaIPhi;
  
  long long coshDeltaEta = LUT_COSH_DETA_JET_JET[deltaIEta];
  long long cosDeltaPhi = LUT_COS_DPHI_JET_JET[deltaIPhi];
  long long pt0 = LUT_JET_ET[data->jetIEt.at(idx0)];
  long long pt1 = LUT_JET_ET[data->jetIEt.at(idx1)];
  long long mass2 = pt0*pt1*(coshDeltaEta - cosDeltaPhi);
    minimum = (long long)(51200.0 * POW10[5]);
  maximum = (long long)(11549264162.0 * POW10[5]);
  if (not ((minimum <= mass2) and (mass2 <= maximum))) continue;

          // 0.0 <= DeltaEta <= 1.5
      iEta = data->jetIEta.at(idx0);
    deltaIEta = abs(iEta - data->jetIEta.at(idx1));
      unsigned int deltaEta = LUT_DETA_JET_JET[deltaIEta];
  
    minimum = (long long)(0.0 * POW10[3]);
  maximum = (long long)(1.5 * POW10[3]);
  if (not ((minimum <= deltaEta) and (deltaEta <= maximum))) continue;

    
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}


    
                    





bool
InvariantMass_3160755015414139382
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
    size_t nobj0 = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj0++;
                   candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      
      const int idx0 = candidates.at(set.at(indicies.at(0)));
      const int idx1 = candidates.at(set.at(indicies.at(1)));
                                // JET30: ET >= 60 at BX = 0
      if (not (data->jetIEt.at(idx0) >= 60)) continue;

          
                                // JET30: ET >= 60 at BX = 0
      if (not (data->jetIEt.at(idx1) >= 60)) continue;

          
          long long minimum;
  long long maximum;

  int iEta = -9999999; unsigned int deltaIEta = 9999999;
        // 340.0 <= mass <= 151982.0
      iEta = data->jetIEta.at(idx0);
    deltaIEta = abs(iEta - data->jetIEta.at(idx1));
  
    int iPhi = data->jetIPhi.at(idx0);
  
  unsigned int deltaIPhi = abs(iPhi - data->jetIPhi.at(idx1));
  if (deltaIPhi >= 72) deltaIPhi = 2*72 - deltaIPhi;
  
  long long coshDeltaEta = LUT_COSH_DETA_JET_JET[deltaIEta];
  long long cosDeltaPhi = LUT_COS_DPHI_JET_JET[deltaIPhi];
  long long pt0 = LUT_JET_ET[data->jetIEt.at(idx0)];
  long long pt1 = LUT_JET_ET[data->jetIEt.at(idx1)];
  long long mass2 = pt0*pt1*(coshDeltaEta - cosDeltaPhi);
    minimum = (long long)(57800.0 * POW10[5]);
  maximum = (long long)(11549264162.0 * POW10[5]);
  if (not ((minimum <= mass2) and (mass2 <= maximum))) continue;

          // 0.0 <= DeltaEta <= 1.5
      iEta = data->jetIEta.at(idx0);
    deltaIEta = abs(iEta - data->jetIEta.at(idx1));
      unsigned int deltaEta = LUT_DETA_JET_JET[deltaIEta];
  
    minimum = (long long)(0.0 * POW10[3]);
  maximum = (long long)(1.5 * POW10[3]);
  if (not ((minimum <= deltaEta) and (deltaEta <= maximum))) continue;

    
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}


    
                    





bool
InvariantMass_3160759413460650486
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
    size_t nobj0 = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj0++;
                   candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      
      const int idx0 = candidates.at(set.at(indicies.at(0)));
      const int idx1 = candidates.at(set.at(indicies.at(1)));
                                // JET30: ET >= 60 at BX = 0
      if (not (data->jetIEt.at(idx0) >= 60)) continue;

          
                                // JET30: ET >= 60 at BX = 0
      if (not (data->jetIEt.at(idx1) >= 60)) continue;

          
          long long minimum;
  long long maximum;

  int iEta = -9999999; unsigned int deltaIEta = 9999999;
        // 360.0 <= mass <= 151982.0
      iEta = data->jetIEta.at(idx0);
    deltaIEta = abs(iEta - data->jetIEta.at(idx1));
  
    int iPhi = data->jetIPhi.at(idx0);
  
  unsigned int deltaIPhi = abs(iPhi - data->jetIPhi.at(idx1));
  if (deltaIPhi >= 72) deltaIPhi = 2*72 - deltaIPhi;
  
  long long coshDeltaEta = LUT_COSH_DETA_JET_JET[deltaIEta];
  long long cosDeltaPhi = LUT_COS_DPHI_JET_JET[deltaIPhi];
  long long pt0 = LUT_JET_ET[data->jetIEt.at(idx0)];
  long long pt1 = LUT_JET_ET[data->jetIEt.at(idx1)];
  long long mass2 = pt0*pt1*(coshDeltaEta - cosDeltaPhi);
    minimum = (long long)(64800.0 * POW10[5]);
  maximum = (long long)(11549264162.0 * POW10[5]);
  if (not ((minimum <= mass2) and (mass2 <= maximum))) continue;

          // 0.0 <= DeltaEta <= 1.5
      iEta = data->jetIEta.at(idx0);
    deltaIEta = abs(iEta - data->jetIEta.at(idx1));
      unsigned int deltaEta = LUT_DETA_JET_JET[deltaIEta];
  
    minimum = (long long)(0.0 * POW10[3]);
  maximum = (long long)(1.5 * POW10[3]);
  if (not ((minimum <= deltaEta) and (deltaEta <= maximum))) continue;

    
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}


    
                    





bool
InvariantMass_3160763811507161590
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
    size_t nobj0 = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj0++;
                   candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      
      const int idx0 = candidates.at(set.at(indicies.at(0)));
      const int idx1 = candidates.at(set.at(indicies.at(1)));
                                // JET30: ET >= 60 at BX = 0
      if (not (data->jetIEt.at(idx0) >= 60)) continue;

          
                                // JET30: ET >= 60 at BX = 0
      if (not (data->jetIEt.at(idx1) >= 60)) continue;

          
          long long minimum;
  long long maximum;

  int iEta = -9999999; unsigned int deltaIEta = 9999999;
        // 0.0 <= DeltaEta <= 1.5
      iEta = data->jetIEta.at(idx0);
    deltaIEta = abs(iEta - data->jetIEta.at(idx1));
      unsigned int deltaEta = LUT_DETA_JET_JET[deltaIEta];
  
    minimum = (long long)(0.0 * POW10[3]);
  maximum = (long long)(1.5 * POW10[3]);
  if (not ((minimum <= deltaEta) and (deltaEta <= maximum))) continue;

          // 380.0 <= mass <= 151982.0
      iEta = data->jetIEta.at(idx0);
    deltaIEta = abs(iEta - data->jetIEta.at(idx1));
  
    int iPhi = data->jetIPhi.at(idx0);
  
  unsigned int deltaIPhi = abs(iPhi - data->jetIPhi.at(idx1));
  if (deltaIPhi >= 72) deltaIPhi = 2*72 - deltaIPhi;
  
  long long coshDeltaEta = LUT_COSH_DETA_JET_JET[deltaIEta];
  long long cosDeltaPhi = LUT_COS_DPHI_JET_JET[deltaIPhi];
  long long pt0 = LUT_JET_ET[data->jetIEt.at(idx0)];
  long long pt1 = LUT_JET_ET[data->jetIEt.at(idx1)];
  long long mass2 = pt0*pt1*(coshDeltaEta - cosDeltaPhi);
    minimum = (long long)(72200.0 * POW10[5]);
  maximum = (long long)(11549264162.0 * POW10[5]);
  if (not ((minimum <= mass2) and (mass2 <= maximum))) continue;

    
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}


    
                    





bool
InvariantMass_3161027694297827830
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
    size_t nobj0 = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->jetBx.size(); ii++)
  {
    if (not (data->jetBx.at(ii) == 0)) continue;
    nobj0++;
                   candidates.push_back(ii);
  }

  bool pass = false;
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      
      const int idx0 = candidates.at(set.at(indicies.at(0)));
      const int idx1 = candidates.at(set.at(indicies.at(1)));
                                // JET30: ET >= 60 at BX = 0
      if (not (data->jetIEt.at(idx0) >= 60)) continue;

          
                                // JET30: ET >= 60 at BX = 0
      if (not (data->jetIEt.at(idx1) >= 60)) continue;

          
          long long minimum;
  long long maximum;

  int iEta = -9999999; unsigned int deltaIEta = 9999999;
        // 400.0 <= mass <= 14000.0
      iEta = data->jetIEta.at(idx0);
    deltaIEta = abs(iEta - data->jetIEta.at(idx1));
  
    int iPhi = data->jetIPhi.at(idx0);
  
  unsigned int deltaIPhi = abs(iPhi - data->jetIPhi.at(idx1));
  if (deltaIPhi >= 72) deltaIPhi = 2*72 - deltaIPhi;
  
  long long coshDeltaEta = LUT_COSH_DETA_JET_JET[deltaIEta];
  long long cosDeltaPhi = LUT_COS_DPHI_JET_JET[deltaIPhi];
  long long pt0 = LUT_JET_ET[data->jetIEt.at(idx0)];
  long long pt1 = LUT_JET_ET[data->jetIEt.at(idx1)];
  long long mass2 = pt0*pt1*(coshDeltaEta - cosDeltaPhi);
    minimum = (long long)(80000.0 * POW10[5]);
  maximum = (long long)(98000000.0 * POW10[5]);
  if (not ((minimum <= mass2) and (mass2 <= maximum))) continue;

          // 0.0 <= DeltaEta <= 1.5
      iEta = data->jetIEta.at(idx0);
    deltaIEta = abs(iEta - data->jetIEta.at(idx1));
      unsigned int deltaEta = LUT_DETA_JET_JET[deltaIEta];
  
    minimum = (long long)(0.0 * POW10[3]);
  maximum = (long long)(1.5 * POW10[3]);
  if (not ((minimum <= deltaEta) and (deltaEta <= maximum))) continue;

    
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}


    
                    





bool
InvariantMass_3324232561693118895
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      
      const int idx0 = candidates.at(set.at(indicies.at(0)));
      const int idx1 = candidates.at(set.at(indicies.at(1)));
                                // MU2p5: ET >= 6 at BX = 0
      if (not (data->muonIEt.at(idx0) >= 6)) continue;

                        // quality : 0xfff0
      if (not ((65520 >> data->muonQual.at(idx0)) & 1)) continue;

          
                                // MU3p5: ET >= 8 at BX = 0
      if (not (data->muonIEt.at(idx1) >= 8)) continue;

                        // quality : 0xfff0
      if (not ((65520 >> data->muonQual.at(idx1)) & 1)) continue;

          
          long long minimum;
  long long maximum;

  int iEta = -9999999; unsigned int deltaIEta = 9999999;
        // 20.0 <= mass <= 151982.0
      iEta = data->muonIEtaAtVtx.at(idx0);
    deltaIEta = abs(iEta - data->muonIEtaAtVtx.at(idx1));
  
    int iPhi = data->muonIPhiAtVtx.at(idx0);
  
  unsigned int deltaIPhi = abs(iPhi - data->muonIPhiAtVtx.at(idx1));
  if (deltaIPhi >= 288) deltaIPhi = 2*288 - deltaIPhi;
  
  long long coshDeltaEta = LUT_COSH_DETA_MU_MU[deltaIEta];
  long long cosDeltaPhi = LUT_COS_DPHI_MU_MU[deltaIPhi];
  long long pt0 = LUT_MU_ET[data->muonIEt.at(idx0)];
  long long pt1 = LUT_MU_ET[data->muonIEt.at(idx1)];
  long long mass2 = pt0*pt1*(coshDeltaEta - cosDeltaPhi);
    minimum = (long long)(200.0 * POW10[6]);
  maximum = (long long)(11549264162.0 * POW10[6]);
  if (not ((minimum <= mass2) and (mass2 <= maximum))) continue;

    
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}


    
                    





bool
InvariantMass_4461482972834602413
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      bool etaWindow1;
      const int idx0 = candidates.at(set.at(indicies.at(0)));
      const int idx1 = candidates.at(set.at(indicies.at(1)));
                                // MU3: ET >= 7 at BX = 0
      if (not (data->muonIEt.at(idx0) >= 7)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx0)) & 1)) continue;

                        // -2.3000625 <= eta <= 2.3000625
              etaWindow1 = ((-211 <= data->muonIEtaAtVtx.at(idx0)) and (data->muonIEtaAtVtx.at(idx0) <= 211));
            
          if (not etaWindow1) continue;
                                // MU3: ET >= 7 at BX = 0
      if (not (data->muonIEt.at(idx1) >= 7)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx1)) & 1)) continue;

                        // -2.3000625 <= eta <= 2.3000625
              etaWindow1 = ((-211 <= data->muonIEtaAtVtx.at(idx1)) and (data->muonIEtaAtVtx.at(idx1) <= 211));
            
          if (not etaWindow1) continue;
          long long minimum;
  long long maximum;

  int iEta = -9999999; unsigned int deltaIEta = 9999999;
        // 0.0 <= mass <= 14.0
      iEta = data->muonIEtaAtVtx.at(idx0);
    deltaIEta = abs(iEta - data->muonIEtaAtVtx.at(idx1));
  
    int iPhi = data->muonIPhiAtVtx.at(idx0);
  
  unsigned int deltaIPhi = abs(iPhi - data->muonIPhiAtVtx.at(idx1));
  if (deltaIPhi >= 288) deltaIPhi = 2*288 - deltaIPhi;
  
  long long coshDeltaEta = LUT_COSH_DETA_MU_MU[deltaIEta];
  long long cosDeltaPhi = LUT_COS_DPHI_MU_MU[deltaIPhi];
  long long pt0 = LUT_MU_ET[data->muonIEt.at(idx0)];
  long long pt1 = LUT_MU_ET[data->muonIEt.at(idx1)];
  long long mass2 = pt0*pt1*(coshDeltaEta - cosDeltaPhi);
    minimum = (long long)(0.0 * POW10[6]);
  maximum = (long long)(98.0 * POW10[6]);
  if (not ((minimum <= mass2) and (mass2 <= maximum))) continue;

          const std::string OS = "os";
    const std::string SS = "ls";
    if (data->muonChg.at(idx0) == 0) continue;  // charge valid bit not set
    if (data->muonChg.at(idx1) == 0) continue;  // charge valid bit not set
    if ("os" == OS)
    {
      if (not (data->muonChg.at(idx0) != data->muonChg.at(idx1))) continue;
    }
    else if ("os" == SS)
    {
      if (not (data->muonChg.at(idx0) == data->muonChg.at(idx1))) continue;
    }
    
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}


    
      





bool
MuonMuonCorrelation_12923126501326425857
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      
      const int idx0 = candidates.at(set.at(indicies.at(0)));
      const int idx1 = candidates.at(set.at(indicies.at(1)));
                                // MU4p5: ET >= 10 at BX = 0
      if (not (data->muonIEt.at(idx0) >= 10)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx0)) & 1)) continue;

          
                                // MU4p5: ET >= 10 at BX = 0
      if (not (data->muonIEt.at(idx1) >= 10)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx1)) & 1)) continue;

          
          long long minimum;
  long long maximum;

  int iEta = -9999999; unsigned int deltaIEta = 9999999;
        const std::string OS = "os";
    const std::string SS = "ls";
    if (data->muonChg.at(idx0) == 0) continue;  // charge valid bit not set
    if (data->muonChg.at(idx1) == 0) continue;  // charge valid bit not set
    if ("os" == OS)
    {
      if (not (data->muonChg.at(idx0) != data->muonChg.at(idx1))) continue;
    }
    else if ("os" == SS)
    {
      if (not (data->muonChg.at(idx0) == data->muonChg.at(idx1))) continue;
    }
          // 0.00 <= DeltaR <= 1.20
      iEta = data->muonIEtaAtVtx.at(idx0);
    deltaIEta = abs(iEta - data->muonIEtaAtVtx.at(idx1));
      unsigned int deltaEta = LUT_DETA_MU_MU[deltaIEta];
  
    int iPhi = data->muonIPhiAtVtx.at(idx0);
  
  unsigned int deltaIPhi = abs(iPhi - data->muonIPhiAtVtx.at(idx1));
  if (deltaIPhi >= 288) deltaIPhi = 2*288 - deltaIPhi;
      unsigned int deltaPhi = LUT_DPHI_MU_MU[deltaIPhi];
  
  long long deltaR2 = deltaEta*deltaEta + deltaPhi*deltaPhi;
    minimum = (long long)(0.0 * POW10[6]);
  maximum = (long long)(1.441 * POW10[6]);
  if (not ((minimum <= deltaR2) and (deltaR2 <= maximum))) continue;

    
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}



      





bool
MuonMuonCorrelation_15199048927445899759
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      bool etaWindow1;
      const int idx0 = candidates.at(set.at(indicies.at(0)));
      const int idx1 = candidates.at(set.at(indicies.at(1)));
                                // MU0: ET >= 1 at BX = 0
      if (not (data->muonIEt.at(idx0) >= 1)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx0)) & 1)) continue;

                        // -1.5061875 <= eta <= 1.5061875
              etaWindow1 = ((-138 <= data->muonIEtaAtVtx.at(idx0)) and (data->muonIEtaAtVtx.at(idx0) <= 138));
            
          if (not etaWindow1) continue;
                                // MU0: ET >= 1 at BX = 0
      if (not (data->muonIEt.at(idx1) >= 1)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx1)) & 1)) continue;

                        // -1.5061875 <= eta <= 1.5061875
              etaWindow1 = ((-138 <= data->muonIEtaAtVtx.at(idx1)) and (data->muonIEtaAtVtx.at(idx1) <= 138));
            
          if (not etaWindow1) continue;
          long long minimum;
  long long maximum;

  int iEta = -9999999; unsigned int deltaIEta = 9999999;
        // 0.00 <= DeltaR <= 1.40
      iEta = data->muonIEtaAtVtx.at(idx0);
    deltaIEta = abs(iEta - data->muonIEtaAtVtx.at(idx1));
      unsigned int deltaEta = LUT_DETA_MU_MU[deltaIEta];
  
    int iPhi = data->muonIPhiAtVtx.at(idx0);
  
  unsigned int deltaIPhi = abs(iPhi - data->muonIPhiAtVtx.at(idx1));
  if (deltaIPhi >= 288) deltaIPhi = 2*288 - deltaIPhi;
      unsigned int deltaPhi = LUT_DPHI_MU_MU[deltaIPhi];
  
  long long deltaR2 = deltaEta*deltaEta + deltaPhi*deltaPhi;
    minimum = (long long)(0.0 * POW10[6]);
  maximum = (long long)(1.961 * POW10[6]);
  if (not ((minimum <= deltaR2) and (deltaR2 <= maximum))) continue;

    
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}



      





bool
MuonMuonCorrelation_15199048929593776303
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      bool etaWindow1;
      const int idx0 = candidates.at(set.at(indicies.at(0)));
      const int idx1 = candidates.at(set.at(indicies.at(1)));
                                // MU0: ET >= 1 at BX = 0
      if (not (data->muonIEt.at(idx0) >= 1)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx0)) & 1)) continue;

                        // -2.0064375 <= eta <= 2.0064375
              etaWindow1 = ((-184 <= data->muonIEtaAtVtx.at(idx0)) and (data->muonIEtaAtVtx.at(idx0) <= 184));
            
          if (not etaWindow1) continue;
                                // MU0: ET >= 1 at BX = 0
      if (not (data->muonIEt.at(idx1) >= 1)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx1)) & 1)) continue;

                        // -2.0064375 <= eta <= 2.0064375
              etaWindow1 = ((-184 <= data->muonIEtaAtVtx.at(idx1)) and (data->muonIEtaAtVtx.at(idx1) <= 184));
            
          if (not etaWindow1) continue;
          long long minimum;
  long long maximum;

  int iEta = -9999999; unsigned int deltaIEta = 9999999;
        // 0.00 <= DeltaR <= 1.40
      iEta = data->muonIEtaAtVtx.at(idx0);
    deltaIEta = abs(iEta - data->muonIEtaAtVtx.at(idx1));
      unsigned int deltaEta = LUT_DETA_MU_MU[deltaIEta];
  
    int iPhi = data->muonIPhiAtVtx.at(idx0);
  
  unsigned int deltaIPhi = abs(iPhi - data->muonIPhiAtVtx.at(idx1));
  if (deltaIPhi >= 288) deltaIPhi = 2*288 - deltaIPhi;
      unsigned int deltaPhi = LUT_DPHI_MU_MU[deltaIPhi];
  
  long long deltaR2 = deltaEta*deltaEta + deltaPhi*deltaPhi;
    minimum = (long long)(0.0 * POW10[6]);
  maximum = (long long)(1.961 * POW10[6]);
  if (not ((minimum <= deltaR2) and (deltaR2 <= maximum))) continue;

    
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}



      





bool
MuonMuonCorrelation_16784489743460462578
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      
      const int idx0 = candidates.at(set.at(indicies.at(0)));
      const int idx1 = candidates.at(set.at(indicies.at(1)));
                                // MU4: ET >= 9 at BX = 0
      if (not (data->muonIEt.at(idx0) >= 9)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx0)) & 1)) continue;

          
                                // MU4: ET >= 9 at BX = 0
      if (not (data->muonIEt.at(idx1) >= 9)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx1)) & 1)) continue;

          
          long long minimum;
  long long maximum;

  int iEta = -9999999; unsigned int deltaIEta = 9999999;
        const std::string OS = "os";
    const std::string SS = "ls";
    if (data->muonChg.at(idx0) == 0) continue;  // charge valid bit not set
    if (data->muonChg.at(idx1) == 0) continue;  // charge valid bit not set
    if ("os" == OS)
    {
      if (not (data->muonChg.at(idx0) != data->muonChg.at(idx1))) continue;
    }
    else if ("os" == SS)
    {
      if (not (data->muonChg.at(idx0) == data->muonChg.at(idx1))) continue;
    }
          // 0.00 <= DeltaR <= 1.20
      iEta = data->muonIEtaAtVtx.at(idx0);
    deltaIEta = abs(iEta - data->muonIEtaAtVtx.at(idx1));
      unsigned int deltaEta = LUT_DETA_MU_MU[deltaIEta];
  
    int iPhi = data->muonIPhiAtVtx.at(idx0);
  
  unsigned int deltaIPhi = abs(iPhi - data->muonIPhiAtVtx.at(idx1));
  if (deltaIPhi >= 288) deltaIPhi = 2*288 - deltaIPhi;
      unsigned int deltaPhi = LUT_DPHI_MU_MU[deltaIPhi];
  
  long long deltaR2 = deltaEta*deltaEta + deltaPhi*deltaPhi;
    minimum = (long long)(0.0 * POW10[6]);
  maximum = (long long)(1.441 * POW10[6]);
  if (not ((minimum <= deltaR2) and (deltaR2 <= maximum))) continue;

    
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
MuonMuonCorrelation_7972376774213455602
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      bool etaWindow1;
      const int idx0 = candidates.at(set.at(indicies.at(0)));
      const int idx1 = candidates.at(set.at(indicies.at(1)));
                                // MU0: ET >= 1 at BX = 0
      if (not (data->muonIEt.at(idx0) >= 1)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx0)) & 1)) continue;

                        // -1.4083125 <= eta <= 1.4083125
              etaWindow1 = ((-129 <= data->muonIEtaAtVtx.at(idx0)) and (data->muonIEtaAtVtx.at(idx0) <= 129));
            
          if (not etaWindow1) continue;
                                // MU0: ET >= 1 at BX = 0
      if (not (data->muonIEt.at(idx1) >= 1)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx1)) & 1)) continue;

                        // -1.4083125 <= eta <= 1.4083125
              etaWindow1 = ((-129 <= data->muonIEtaAtVtx.at(idx1)) and (data->muonIEtaAtVtx.at(idx1) <= 129));
            
          if (not etaWindow1) continue;
          long long minimum;
  long long maximum;

  int iEta = -9999999; unsigned int deltaIEta = 9999999;
        const std::string OS = "os";
    const std::string SS = "ls";
    if (data->muonChg.at(idx0) == 0) continue;  // charge valid bit not set
    if (data->muonChg.at(idx1) == 0) continue;  // charge valid bit not set
    if ("os" == OS)
    {
      if (not (data->muonChg.at(idx0) != data->muonChg.at(idx1))) continue;
    }
    else if ("os" == SS)
    {
      if (not (data->muonChg.at(idx0) == data->muonChg.at(idx1))) continue;
    }
          // 0.0 <= DeltaEta <= 1.8
      iEta = data->muonIEtaAtVtx.at(idx0);
    deltaIEta = abs(iEta - data->muonIEtaAtVtx.at(idx1));
      unsigned int deltaEta = LUT_DETA_MU_MU[deltaIEta];
  
    minimum = (long long)(0.0 * POW10[3]);
  maximum = (long long)(1.8 * POW10[3]);
  if (not ((minimum <= deltaEta) and (deltaEta <= maximum))) continue;

    
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}



      





bool
MuonMuonCorrelation_8772456668275224612
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      
      const int idx0 = candidates.at(set.at(indicies.at(0)));
      const int idx1 = candidates.at(set.at(indicies.at(1)));
                                // MU10: ET >= 21 at BX = 0
      if (not (data->muonIEt.at(idx0) >= 21)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx0)) & 1)) continue;

          
                                // MU0: ET >= 1 at BX = 0
      if (not (data->muonIEt.at(idx1) >= 1)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx1)) & 1)) continue;

          
          long long minimum;
  long long maximum;

  int iEta = -9999999; unsigned int deltaIEta = 9999999;
        // 0.0 <= DeltaEta <= 1.8
      iEta = data->muonIEtaAtVtx.at(idx0);
    deltaIEta = abs(iEta - data->muonIEtaAtVtx.at(idx1));
      unsigned int deltaEta = LUT_DETA_MU_MU[deltaIEta];
  
    minimum = (long long)(0.0 * POW10[3]);
  maximum = (long long)(1.8 * POW10[3]);
  if (not ((minimum <= deltaEta) and (deltaEta <= maximum))) continue;

    
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}



      





bool
MuonMuonCorrelation_9513481109949270451
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      bool etaWindow1;
      const int idx0 = candidates.at(set.at(indicies.at(0)));
      const int idx1 = candidates.at(set.at(indicies.at(1)));
                                // MU0: ET >= 1 at BX = 0
      if (not (data->muonIEt.at(idx0) >= 1)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx0)) & 1)) continue;

                        // -1.4083125 <= eta <= 1.4083125
              etaWindow1 = ((-129 <= data->muonIEtaAtVtx.at(idx0)) and (data->muonIEtaAtVtx.at(idx0) <= 129));
            
          if (not etaWindow1) continue;
                                // MU0: ET >= 1 at BX = 0
      if (not (data->muonIEt.at(idx1) >= 1)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx1)) & 1)) continue;

                        // -1.4083125 <= eta <= 1.4083125
              etaWindow1 = ((-129 <= data->muonIEtaAtVtx.at(idx1)) and (data->muonIEtaAtVtx.at(idx1) <= 129));
            
          if (not etaWindow1) continue;
          long long minimum;
  long long maximum;

  int iEta = -9999999; unsigned int deltaIEta = 9999999;
        const std::string OS = "os";
    const std::string SS = "ls";
    if (data->muonChg.at(idx0) == 0) continue;  // charge valid bit not set
    if (data->muonChg.at(idx1) == 0) continue;  // charge valid bit not set
    if ("os" == OS)
    {
      if (not (data->muonChg.at(idx0) != data->muonChg.at(idx1))) continue;
    }
    else if ("os" == SS)
    {
      if (not (data->muonChg.at(idx0) == data->muonChg.at(idx1))) continue;
    }
          // 0.00 <= DeltaR <= 1.40
      iEta = data->muonIEtaAtVtx.at(idx0);
    deltaIEta = abs(iEta - data->muonIEtaAtVtx.at(idx1));
      unsigned int deltaEta = LUT_DETA_MU_MU[deltaIEta];
  
    int iPhi = data->muonIPhiAtVtx.at(idx0);
  
  unsigned int deltaIPhi = abs(iPhi - data->muonIPhiAtVtx.at(idx1));
  if (deltaIPhi >= 288) deltaIPhi = 2*288 - deltaIPhi;
      unsigned int deltaPhi = LUT_DPHI_MU_MU[deltaIPhi];
  
  long long deltaR2 = deltaEta*deltaEta + deltaPhi*deltaPhi;
    minimum = (long long)(0.0 * POW10[6]);
  maximum = (long long)(1.961 * POW10[6]);
  if (not ((minimum <= deltaR2) and (deltaR2 <= maximum))) continue;

    
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}



      





bool
MuonMuonCorrelation_9513481109957663155
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
  if (candidates.size() < 2) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 2, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(2, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      bool etaWindow1;
      const int idx0 = candidates.at(set.at(indicies.at(0)));
      const int idx1 = candidates.at(set.at(indicies.at(1)));
                                // MU0: ET >= 1 at BX = 0
      if (not (data->muonIEt.at(idx0) >= 1)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx0)) & 1)) continue;

                        // -1.5061875 <= eta <= 1.5061875
              etaWindow1 = ((-138 <= data->muonIEtaAtVtx.at(idx0)) and (data->muonIEtaAtVtx.at(idx0) <= 138));
            
          if (not etaWindow1) continue;
                                // MU0: ET >= 1 at BX = 0
      if (not (data->muonIEt.at(idx1) >= 1)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx1)) & 1)) continue;

                        // -1.5061875 <= eta <= 1.5061875
              etaWindow1 = ((-138 <= data->muonIEtaAtVtx.at(idx1)) and (data->muonIEtaAtVtx.at(idx1) <= 138));
            
          if (not etaWindow1) continue;
          long long minimum;
  long long maximum;

  int iEta = -9999999; unsigned int deltaIEta = 9999999;
        const std::string OS = "os";
    const std::string SS = "ls";
    if (data->muonChg.at(idx0) == 0) continue;  // charge valid bit not set
    if (data->muonChg.at(idx1) == 0) continue;  // charge valid bit not set
    if ("os" == OS)
    {
      if (not (data->muonChg.at(idx0) != data->muonChg.at(idx1))) continue;
    }
    else if ("os" == SS)
    {
      if (not (data->muonChg.at(idx0) == data->muonChg.at(idx1))) continue;
    }
          // 0.00 <= DeltaR <= 1.40
      iEta = data->muonIEtaAtVtx.at(idx0);
    deltaIEta = abs(iEta - data->muonIEtaAtVtx.at(idx1));
      unsigned int deltaEta = LUT_DETA_MU_MU[deltaIEta];
  
    int iPhi = data->muonIPhiAtVtx.at(idx0);
  
  unsigned int deltaIPhi = abs(iPhi - data->muonIPhiAtVtx.at(idx1));
  if (deltaIPhi >= 288) deltaIPhi = 2*288 - deltaIPhi;
      unsigned int deltaPhi = LUT_DPHI_MU_MU[deltaIPhi];
  
  long long deltaR2 = deltaEta*deltaEta + deltaPhi*deltaPhi;
    minimum = (long long)(0.0 * POW10[6]);
  maximum = (long long)(1.961 * POW10[6]);
  if (not ((minimum <= deltaR2) and (deltaR2 <= maximum))) continue;

    
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}



      


bool
QuadJET_17630949366336433287
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
  if (candidates.size() < 4) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 4, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(4, permutation);

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

                        // -2.523 <= eta <= 2.523
              etaWindow1 = ((-58 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 57));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET55: ET >= 110 at BX = 0
      if (not (data->jetIEt.at(idx) >= 110)) continue;

                        // -2.523 <= eta <= 2.523
              etaWindow1 = ((-58 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 57));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(2)));
                                // JET40: ET >= 80 at BX = 0
      if (not (data->jetIEt.at(idx) >= 80)) continue;

                        // -2.523 <= eta <= 2.523
              etaWindow1 = ((-58 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 57));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(3)));
                                // JET35: ET >= 70 at BX = 0
      if (not (data->jetIEt.at(idx) >= 70)) continue;

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
QuadJET_17665570788471843975
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
  if (candidates.size() < 4) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 4, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(4, permutation);

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

                        // -2.523 <= eta <= 2.523
              etaWindow1 = ((-58 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 57));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET55: ET >= 110 at BX = 0
      if (not (data->jetIEt.at(idx) >= 110)) continue;

                        // -2.523 <= eta <= 2.523
              etaWindow1 = ((-58 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 57));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(2)));
                                // JET40: ET >= 80 at BX = 0
      if (not (data->jetIEt.at(idx) >= 80)) continue;

                        // -2.523 <= eta <= 2.523
              etaWindow1 = ((-58 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 57));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(3)));
                                // JET40: ET >= 80 at BX = 0
      if (not (data->jetIEt.at(idx) >= 80)) continue;

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
QuadJET_17666978163355397295
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
  if (candidates.size() < 4) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 4, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(4, permutation);

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

                        // -2.523 <= eta <= 2.523
              etaWindow1 = ((-58 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 57));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET55: ET >= 110 at BX = 0
      if (not (data->jetIEt.at(idx) >= 110)) continue;

                        // -2.523 <= eta <= 2.523
              etaWindow1 = ((-58 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 57));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(2)));
                                // JET45: ET >= 90 at BX = 0
      if (not (data->jetIEt.at(idx) >= 90)) continue;

                        // -2.523 <= eta <= 2.523
              etaWindow1 = ((-58 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 57));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(3)));
                                // JET45: ET >= 90 at BX = 0
      if (not (data->jetIEt.at(idx) >= 90)) continue;

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
QuadJET_2680035217249740980
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
  if (candidates.size() < 4) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 4, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(4, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET36: ET >= 72 at BX = 0
      if (not (data->jetIEt.at(idx) >= 72)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET36: ET >= 72 at BX = 0
      if (not (data->jetIEt.at(idx) >= 72)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(2)));
                                // JET36: ET >= 72 at BX = 0
      if (not (data->jetIEt.at(idx) >= 72)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(3)));
                                // JET36: ET >= 72 at BX = 0
      if (not (data->jetIEt.at(idx) >= 72)) continue;

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
QuadJET_2750930524417894580
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
  if (candidates.size() < 4) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 4, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(4, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET40: ET >= 80 at BX = 0
      if (not (data->jetIEt.at(idx) >= 80)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET40: ET >= 80 at BX = 0
      if (not (data->jetIEt.at(idx) >= 80)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(2)));
                                // JET40: ET >= 80 at BX = 0
      if (not (data->jetIEt.at(idx) >= 80)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(3)));
                                // JET40: ET >= 80 at BX = 0
      if (not (data->jetIEt.at(idx) >= 80)) continue;

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
QuadJET_2825312486036940980
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
  if (candidates.size() < 4) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 4, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(4, permutation);

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

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET50: ET >= 100 at BX = 0
      if (not (data->jetIEt.at(idx) >= 100)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(2)));
                                // JET50: ET >= 100 at BX = 0
      if (not (data->jetIEt.at(idx) >= 100)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(3)));
                                // JET50: ET >= 100 at BX = 0
      if (not (data->jetIEt.at(idx) >= 100)) continue;

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
QuadJET_2899694447655987380
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
  if (candidates.size() < 4) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 4, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(4, permutation);

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

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET60: ET >= 120 at BX = 0
      if (not (data->jetIEt.at(idx) >= 120)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(2)));
                                // JET60: ET >= 120 at BX = 0
      if (not (data->jetIEt.at(idx) >= 120)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(3)));
                                // JET60: ET >= 120 at BX = 0
      if (not (data->jetIEt.at(idx) >= 120)) continue;

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
QuadJET_2969443065613019316
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
  if (candidates.size() < 4) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 4, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(4, permutation);

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
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET55: ET >= 110 at BX = 0
      if (not (data->jetIEt.at(idx) >= 110)) continue;

                        // -2.3925 <= eta <= 2.3925
              etaWindow1 = ((-55 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 54));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(2)));
                                // JET40: ET >= 80 at BX = 0
      if (not (data->jetIEt.at(idx) >= 80)) continue;

                        // -2.3925 <= eta <= 2.3925
              etaWindow1 = ((-55 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 54));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(3)));
                                // JET40: ET >= 80 at BX = 0
      if (not (data->jetIEt.at(idx) >= 80)) continue;

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
QuadMU_509409160461874775
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
  if (candidates.size() < 4) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 4, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(4, permutation);

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

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // MU0: ET >= 1 at BX = 0
      if (not (data->muonIEt.at(idx) >= 1)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            idx = candidates.at(set.at(indicies.at(2)));
                                // MU0: ET >= 1 at BX = 0
      if (not (data->muonIEt.at(idx) >= 1)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            idx = candidates.at(set.at(indicies.at(3)));
                                // MU0: ET >= 1 at BX = 0
      if (not (data->muonIEt.at(idx) >= 1)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            
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
SingleEG_1139637
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
                                // EG5: ET >= 10 at BX = 0
      if (not (data->egIEt.at(idx) >= 10)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_1139639
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
                                // EG7: ET >= 14 at BX = 0
      if (not (data->egIEt.at(idx) >= 14)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_12507428088042853184
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
                                // EG6: ET >= 12 at BX = 0
      if (not (data->egIEt.at(idx) >= 12)) continue;

                        // isolation : 0xc
      if (not ((12 >> data->egIso.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_12507579852048143168
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
                                // EG10: ET >= 20 at BX = 0
      if (not (data->egIEt.at(idx) >= 20)) continue;

                        // isolation : 0xc
      if (not ((12 >> data->egIso.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_12507579852056531520
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
                                // EG18: ET >= 36 at BX = 0
      if (not (data->egIEt.at(idx) >= 36)) continue;

                        // isolation : 0xa
      if (not ((10 >> data->egIso.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_12507579852056531776
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
                                // EG18: ET >= 36 at BX = 0
      if (not (data->egIEt.at(idx) >= 36)) continue;

                        // isolation : 0xc
      if (not ((12 >> data->egIso.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_12507579852182360640
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
                                // EG20: ET >= 40 at BX = 0
      if (not (data->egIEt.at(idx) >= 40)) continue;

                        // isolation : 0xa
      if (not ((10 >> data->egIso.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_12507579852182360896
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
                                // EG20: ET >= 40 at BX = 0
      if (not (data->egIEt.at(idx) >= 40)) continue;

                        // isolation : 0xc
      if (not ((12 >> data->egIso.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_12507579852184457792
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
                                // EG22: ET >= 44 at BX = 0
      if (not (data->egIEt.at(idx) >= 44)) continue;

                        // isolation : 0xa
      if (not ((10 >> data->egIso.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_12507579852185506624
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
                                // EG23: ET >= 46 at BX = 0
      if (not (data->egIEt.at(idx) >= 46)) continue;

                        // isolation : 0xc
      if (not ((12 >> data->egIso.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_12507579852186554944
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
                                // EG24: ET >= 48 at BX = 0
      if (not (data->egIEt.at(idx) >= 48)) continue;

                        // isolation : 0xa
      if (not ((10 >> data->egIso.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_12507579852188652096
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
                                // EG26: ET >= 52 at BX = 0
      if (not (data->egIEt.at(idx) >= 52)) continue;

                        // isolation : 0xa
      if (not ((10 >> data->egIso.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_12507579852190749248
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
                                // EG28: ET >= 56 at BX = 0
      if (not (data->egIEt.at(idx) >= 56)) continue;

                        // isolation : 0xa
      if (not ((10 >> data->egIso.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_12507579852316578368
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
                                // EG30: ET >= 60 at BX = 0
      if (not (data->egIEt.at(idx) >= 60)) continue;

                        // isolation : 0xa
      if (not ((10 >> data->egIso.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_12507579852318675520
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
                                // EG32: ET >= 64 at BX = 0
      if (not (data->egIEt.at(idx) >= 64)) continue;

                        // isolation : 0xa
      if (not ((10 >> data->egIso.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_12507579852320772672
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
                                // EG34: ET >= 68 at BX = 0
      if (not (data->egIEt.at(idx) >= 68)) continue;

                        // isolation : 0xa
      if (not ((10 >> data->egIso.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_12507579852321821248
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
                                // EG35: ET >= 70 at BX = 0
      if (not (data->egIEt.at(idx) >= 70)) continue;

                        // isolation : 0xa
      if (not ((10 >> data->egIso.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_12507579852322869824
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
                                // EG36: ET >= 72 at BX = 0
      if (not (data->egIEt.at(idx) >= 72)) continue;

                        // isolation : 0xa
      if (not ((10 >> data->egIso.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_12507579852323918400
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
                                // EG37: ET >= 74 at BX = 0
      if (not (data->egIEt.at(idx) >= 74)) continue;

                        // isolation : 0xa
      if (not ((10 >> data->egIso.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_12507579852324966976
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
                                // EG38: ET >= 76 at BX = 0
      if (not (data->egIEt.at(idx) >= 76)) continue;

                        // isolation : 0xa
      if (not ((10 >> data->egIso.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_12507579852450796096
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
                                // EG40: ET >= 80 at BX = 0
      if (not (data->egIEt.at(idx) >= 80)) continue;

                        // isolation : 0xa
      if (not ((10 >> data->egIso.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_14262501742662192051
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
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // EG25: ET >= 50 at BX = 0
      if (not (data->egIEt.at(idx) >= 50)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->egIEta.at(idx)) and (data->egIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_14262501742930627507
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
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // EG27: ET >= 54 at BX = 0
      if (not (data->egIEt.at(idx) >= 54)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->egIEta.at(idx)) and (data->egIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_14262501759707843507
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
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // EG34: ET >= 68 at BX = 0
      if (not (data->egIEt.at(idx) >= 68)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->egIEta.at(idx)) and (data->egIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_14262501759976278963
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
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // EG36: ET >= 72 at BX = 0
      if (not (data->egIEt.at(idx) >= 72)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->egIEta.at(idx)) and (data->egIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_14262501760244714419
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
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // EG38: ET >= 76 at BX = 0
      if (not (data->egIEt.at(idx) >= 76)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->egIEta.at(idx)) and (data->egIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_145873072
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
                                // EG10: ET >= 20 at BX = 0
      if (not (data->egIEt.at(idx) >= 20)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_145873074
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
                                // EG12: ET >= 24 at BX = 0
      if (not (data->egIEt.at(idx) >= 24)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_145873077
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
                                // EG15: ET >= 30 at BX = 0
      if (not (data->egIEt.at(idx) >= 30)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_145873079
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
                                // EG17: ET >= 34 at BX = 0
      if (not (data->egIEt.at(idx) >= 34)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_145873080
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
                                // EG18: ET >= 36 at BX = 0
      if (not (data->egIEt.at(idx) >= 36)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_145873200
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
                                // EG20: ET >= 40 at BX = 0
      if (not (data->egIEt.at(idx) >= 40)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_145873203
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
                                // EG23: ET >= 46 at BX = 0
      if (not (data->egIEt.at(idx) >= 46)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_145873204
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
                                // EG24: ET >= 48 at BX = 0
      if (not (data->egIEt.at(idx) >= 48)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_145873206
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
                                // EG26: ET >= 52 at BX = 0
      if (not (data->egIEt.at(idx) >= 52)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_145873208
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
                                // EG28: ET >= 56 at BX = 0
      if (not (data->egIEt.at(idx) >= 56)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_145873328
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
                                // EG30: ET >= 60 at BX = 0
      if (not (data->egIEt.at(idx) >= 60)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_145873330
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
                                // EG32: ET >= 64 at BX = 0
      if (not (data->egIEt.at(idx) >= 64)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_145873332
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
                                // EG34: ET >= 68 at BX = 0
      if (not (data->egIEt.at(idx) >= 68)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_145873334
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
                                // EG36: ET >= 72 at BX = 0
      if (not (data->egIEt.at(idx) >= 72)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_145873336
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
                                // EG38: ET >= 76 at BX = 0
      if (not (data->egIEt.at(idx) >= 76)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_145873456
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
                                // EG40: ET >= 80 at BX = 0
      if (not (data->egIEt.at(idx) >= 80)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_145873458
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
                                // EG42: ET >= 84 at BX = 0
      if (not (data->egIEt.at(idx) >= 84)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_145873461
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
                                // EG45: ET >= 90 at BX = 0
      if (not (data->egIEt.at(idx) >= 90)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_145873584
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
                                // EG50: ET >= 100 at BX = 0
      if (not (data->egIEt.at(idx) >= 100)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_6872811427209405681
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
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // EG18: ET >= 36 at BX = 0
      if (not (data->egIEt.at(idx) >= 36)) continue;

                        // isolation : 0xa
      if (not ((10 >> data->egIso.at(idx)) & 1)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->egIEta.at(idx)) and (data->egIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_6872943368604738801
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
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // EG20: ET >= 40 at BX = 0
      if (not (data->egIEt.at(idx) >= 40)) continue;

                        // isolation : 0xa
      if (not ((10 >> data->egIso.at(idx)) & 1)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->egIEta.at(idx)) and (data->egIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_6872945567627994353
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
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // EG22: ET >= 44 at BX = 0
      if (not (data->egIEt.at(idx) >= 44)) continue;

                        // isolation : 0xa
      if (not ((10 >> data->egIso.at(idx)) & 1)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->egIEta.at(idx)) and (data->egIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_6872947766651249905
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
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // EG24: ET >= 48 at BX = 0
      if (not (data->egIEt.at(idx) >= 48)) continue;

                        // isolation : 0xa
      if (not ((10 >> data->egIso.at(idx)) & 1)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->egIEta.at(idx)) and (data->egIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_6872949965674505457
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
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // EG26: ET >= 52 at BX = 0
      if (not (data->egIEt.at(idx) >= 52)) continue;

                        // isolation : 0xa
      if (not ((10 >> data->egIso.at(idx)) & 1)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->egIEta.at(idx)) and (data->egIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_6872952164697761009
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
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // EG28: ET >= 56 at BX = 0
      if (not (data->egIEt.at(idx) >= 56)) continue;

                        // isolation : 0xa
      if (not ((10 >> data->egIso.at(idx)) & 1)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->egIEta.at(idx)) and (data->egIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_6873084106093094129
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
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // EG30: ET >= 60 at BX = 0
      if (not (data->egIEt.at(idx) >= 60)) continue;

                        // isolation : 0xa
      if (not ((10 >> data->egIso.at(idx)) & 1)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->egIEta.at(idx)) and (data->egIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_6873086305116349681
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
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // EG32: ET >= 64 at BX = 0
      if (not (data->egIEt.at(idx) >= 64)) continue;

                        // isolation : 0xa
      if (not ((10 >> data->egIso.at(idx)) & 1)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->egIEta.at(idx)) and (data->egIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_6873087404627977457
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
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // EG33: ET >= 66 at BX = 0
      if (not (data->egIEt.at(idx) >= 66)) continue;

                        // isolation : 0xa
      if (not ((10 >> data->egIso.at(idx)) & 1)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->egIEta.at(idx)) and (data->egIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_6873088504139605233
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
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // EG34: ET >= 68 at BX = 0
      if (not (data->egIEt.at(idx) >= 68)) continue;

                        // isolation : 0xa
      if (not ((10 >> data->egIso.at(idx)) & 1)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->egIEta.at(idx)) and (data->egIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_6873089603651233009
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
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // EG35: ET >= 70 at BX = 0
      if (not (data->egIEt.at(idx) >= 70)) continue;

                        // isolation : 0xa
      if (not ((10 >> data->egIso.at(idx)) & 1)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->egIEta.at(idx)) and (data->egIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_9244738805910375422
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
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // EG24: ET >= 48 at BX = 0
      if (not (data->egIEt.at(idx) >= 48)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->egIEta.at(idx)) and (data->egIEta.at(idx) <= 48));
            
                        // isolation : 0xc
      if (not ((12 >> data->egIso.at(idx)) & 1)) continue;

          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_9244741004933630974
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
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // EG26: ET >= 52 at BX = 0
      if (not (data->egIEt.at(idx) >= 52)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->egIEta.at(idx)) and (data->egIEta.at(idx) <= 48));
            
                        // isolation : 0xc
      if (not ((12 >> data->egIso.at(idx)) & 1)) continue;

          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_9244743203956886526
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
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // EG28: ET >= 56 at BX = 0
      if (not (data->egIEt.at(idx) >= 56)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->egIEta.at(idx)) and (data->egIEta.at(idx) <= 48));
            
                        // isolation : 0xc
      if (not ((12 >> data->egIso.at(idx)) & 1)) continue;

          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_9244881742421986046
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
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // EG36: ET >= 72 at BX = 0
      if (not (data->egIEt.at(idx) >= 72)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->egIEta.at(idx)) and (data->egIEta.at(idx) <= 48));
            
                        // isolation : 0xa
      if (not ((10 >> data->egIso.at(idx)) & 1)) continue;

          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_9244883941445241598
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
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // EG38: ET >= 76 at BX = 0
      if (not (data->egIEt.at(idx) >= 76)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->egIEta.at(idx)) and (data->egIEta.at(idx) <= 48));
            
                        // isolation : 0xa
      if (not ((10 >> data->egIso.at(idx)) & 1)) continue;

          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleEG_9245015882840574718
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
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // EG40: ET >= 80 at BX = 0
      if (not (data->egIEt.at(idx) >= 80)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->egIEta.at(idx)) and (data->egIEta.at(idx) <= 48));
            
                        // isolation : 0xa
      if (not ((10 >> data->egIso.at(idx)) & 1)) continue;

          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
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
SingleETM_18699475637
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kMissingEt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // ETM55: ET >= 110 at BX = 0
      if (not (data->sumIEt.at(ii) >= 110)) continue;
      

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
SingleETM_18699475765
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kMissingEt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // ETM65: ET >= 130 at BX = 0
      if (not (data->sumIEt.at(ii) >= 130)) continue;
      

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
SingleHTT_2496626710837
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  bool pass = false;

  
  for (size_t ii = 0; ii < data->sumBx.size(); ii++)
  {
    if (not (data->sumType.at(ii) == L1Analysis::kTotalHt)) continue;
    if (not (data->sumBx.at(ii) == 0)) continue;
                        // HTT125: ET >= 250 at BX = 0
      if (not (data->sumIEt.at(ii) >= 250)) continue;
      

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
SingleJET_3448182530626688965
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
SingleJET_5967545309672598855
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
                                // JET20: ET >= 40 at BX = 0
      if (not (data->jetIEt.at(idx) >= 40)) continue;

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
SingleJET_5967545344434990407
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
                                // JET43: ET >= 86 at BX = 0
      if (not (data->jetIEt.at(idx) >= 86)) continue;

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
SingleJET_5967545344837643591
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
                                // JET46: ET >= 92 at BX = 0
      if (not (data->jetIEt.at(idx) >= 92)) continue;

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
SingleMU_17494117756195063635
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
                                // MU22: ET >= 45 at BX = 0
      if (not (data->muonIEt.at(idx) >= 45)) continue;

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
SingleMU_17545683021081726533
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
                                // MU10: ET >= 21 at BX = 0
      if (not (data->muonIEt.at(idx) >= 21)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleMU_17545683025133343173
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
                                // MU10: ET >= 21 at BX = 0
      if (not (data->muonIEt.at(idx) >= 21)) continue;

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
SingleMU_17545683038261595717
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
                                // MU11: ET >= 23 at BX = 0
      if (not (data->muonIEt.at(idx) >= 23)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleMU_17545683059493081541
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
                                // MU12: ET >= 25 at BX = 0
      if (not (data->muonIEt.at(idx) >= 25)) continue;

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
SingleMU_17545685275696206277
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
                                // MU23: ET >= 47 at BX = 0
      if (not (data->muonIEt.at(idx) >= 47)) continue;

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
SingleMU_6225176160372139651
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
                                // MU22: ET >= 45 at BX = 0
      if (not (data->muonIEt.at(idx) >= 45)) continue;

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
SingleMU_6945763095867696771
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
                                // MU22: ET >= 45 at BX = 0
      if (not (data->muonIEt.at(idx) >= 45)) continue;

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
SingleMU_7069342828816371872
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
                                // MU12: ET >= 25 at BX = 0
      if (not (data->muonIEt.at(idx) >= 25)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

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
SingleMU_7145648846602061216
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
                                // MU16: ET >= 33 at BX = 0
      if (not (data->muonIEt.at(idx) >= 33)) continue;

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
SingleMU_7181677643621025184
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
                                // MU18: ET >= 37 at BX = 0
      if (not (data->muonIEt.at(idx) >= 37)) continue;

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
SingleMU_7270359269352285314
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
                                // MU12: ET >= 25 at BX = 0
      if (not (data->muonIEt.at(idx) >= 25)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

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
SingleMU_7990946204847842434
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
                                // MU12: ET >= 25 at BX = 0
      if (not (data->muonIEt.at(idx) >= 25)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

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
SingleMU_9343405464758863264
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
                                // MU20: ET >= 41 at BX = 0
      if (not (data->muonIEt.at(idx) >= 41)) continue;

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
SingleMU_9379434261777827232
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
                                // MU22: ET >= 45 at BX = 0
      if (not (data->muonIEt.at(idx) >= 45)) continue;

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
SingleMU_9379434265999970464
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
                                // MU22: ET >= 45 at BX = 0
      if (not (data->muonIEt.at(idx) >= 45)) continue;

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
SingleTAU_12210388642533153582
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->tauBx.size(); ii++)
  {
    if (not (data->tauBx.at(ii) == 0)) continue;
    nobj++;
          if (nobj > 12) break;
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
                                // TAU40: ET >= 80 at BX = 0
      if (not (data->tauIEt.at(idx) >= 80)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->tauIEta.at(idx)) and (data->tauIEta.at(idx) <= 48));
            
                        // isolation : 0xe
      if (not ((14 >> data->tauIso.at(idx)) & 1)) continue;

          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleTAU_14552260448765811502
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->tauBx.size(); ii++)
  {
    if (not (data->tauBx.at(ii) == 0)) continue;
    nobj++;
          if (nobj > 12) break;
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
                                // TAU52: ET >= 104 at BX = 0
      if (not (data->tauIEt.at(idx) >= 104)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->tauIEta.at(idx)) and (data->tauIEta.at(idx) <= 48));
            
                        // isolation : 0xe
      if (not ((14 >> data->tauIso.at(idx)) & 1)) continue;

          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleTAU_16608831008486494024
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->tauBx.size(); ii++)
  {
    if (not (data->tauBx.at(ii) == 0)) continue;
    nobj++;
          if (nobj > 12) break;
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
                                // TAU24: ET >= 48 at BX = 0
      if (not (data->tauIEt.at(idx) >= 48)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->tauIEta.at(idx)) and (data->tauIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleTAU_16608837536836783944
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->tauBx.size(); ii++)
  {
    if (not (data->tauBx.at(ii) == 0)) continue;
    nobj++;
          if (nobj > 12) break;
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
                                // TAU50: ET >= 100 at BX = 0
      if (not (data->tauIEt.at(idx) >= 100)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->tauIEta.at(idx)) and (data->tauIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleTAU_16608841934883295048
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->tauBx.size(); ii++)
  {
    if (not (data->tauBx.at(ii) == 0)) continue;
    nobj++;
          if (nobj > 12) break;
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
                                // TAU70: ET >= 140 at BX = 0
      if (not (data->tauIEt.at(idx) >= 140)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->tauIEta.at(idx)) and (data->tauIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleTAU_16608844133906550600
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->tauBx.size(); ii++)
  {
    if (not (data->tauBx.at(ii) == 0)) continue;
    nobj++;
          if (nobj > 12) break;
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
                                // TAU80: ET >= 160 at BX = 0
      if (not (data->tauIEt.at(idx) >= 160)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->tauIEta.at(idx)) and (data->tauIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleTAU_218368042610145022
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->tauBx.size(); ii++)
  {
    if (not (data->tauBx.at(ii) == 0)) continue;
    nobj++;
          if (nobj > 12) break;
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
                                // TAU26: ET >= 52 at BX = 0
      if (not (data->tauIEt.at(idx) >= 52)) continue;

                        // isolation : 0xe
      if (not ((14 >> data->tauIso.at(idx)) & 1)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->tauIEta.at(idx)) and (data->tauIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleTAU_22686292272
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->tauBx.size(); ii++)
  {
    if (not (data->tauBx.at(ii) == 0)) continue;
    nobj++;
          if (nobj > 12) break;
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
                                // TAU20: ET >= 40 at BX = 0
      if (not (data->tauIEt.at(idx) >= 40)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleTAU_22686292658
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->tauBx.size(); ii++)
  {
    if (not (data->tauBx.at(ii) == 0)) continue;
    nobj++;
          if (nobj > 12) break;
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
                                // TAU52: ET >= 104 at BX = 0
      if (not (data->tauIEt.at(idx) >= 104)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleTAU_236382441119627006
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->tauBx.size(); ii++)
  {
    if (not (data->tauBx.at(ii) == 0)) continue;
    nobj++;
          if (nobj > 12) break;
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
                                // TAU27: ET >= 54 at BX = 0
      if (not (data->tauIEt.at(idx) >= 54)) continue;

                        // isolation : 0xe
      if (not ((14 >> data->tauIso.at(idx)) & 1)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->tauIEta.at(idx)) and (data->tauIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleTAU_2416124660766947070
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->tauBx.size(); ii++)
  {
    if (not (data->tauBx.at(ii) == 0)) continue;
    nobj++;
          if (nobj > 12) break;
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
                                // TAU30: ET >= 60 at BX = 0
      if (not (data->tauIEt.at(idx) >= 60)) continue;

                        // isolation : 0xe
      if (not ((14 >> data->tauIso.at(idx)) & 1)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->tauIEta.at(idx)) and (data->tauIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleTAU_2452153457785911038
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->tauBx.size(); ii++)
  {
    if (not (data->tauBx.at(ii) == 0)) continue;
    nobj++;
          if (nobj > 12) break;
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
                                // TAU32: ET >= 64 at BX = 0
      if (not (data->tauIEt.at(idx) >= 64)) continue;

                        // isolation : 0xe
      if (not ((14 >> data->tauIso.at(idx)) & 1)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->tauIEta.at(idx)) and (data->tauIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleTAU_2470167856295393022
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->tauBx.size(); ii++)
  {
    if (not (data->tauBx.at(ii) == 0)) continue;
    nobj++;
          if (nobj > 12) break;
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
                                // TAU33: ET >= 66 at BX = 0
      if (not (data->tauIEt.at(idx) >= 66)) continue;

                        // isolation : 0xe
      if (not ((14 >> data->tauIso.at(idx)) & 1)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->tauIEta.at(idx)) and (data->tauIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleTAU_2488182254804875006
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->tauBx.size(); ii++)
  {
    if (not (data->tauBx.at(ii) == 0)) continue;
    nobj++;
          if (nobj > 12) break;
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
                                // TAU34: ET >= 68 at BX = 0
      if (not (data->tauIEt.at(idx) >= 68)) continue;

                        // isolation : 0xe
      if (not ((14 >> data->tauIso.at(idx)) & 1)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->tauIEta.at(idx)) and (data->tauIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleTAU_2506196653314356990
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->tauBx.size(); ii++)
  {
    if (not (data->tauBx.at(ii) == 0)) continue;
    nobj++;
          if (nobj > 12) break;
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
                                // TAU35: ET >= 70 at BX = 0
      if (not (data->tauIEt.at(idx) >= 70)) continue;

                        // isolation : 0xe
      if (not ((14 >> data->tauIso.at(idx)) & 1)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->tauIEta.at(idx)) and (data->tauIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleTAU_2524211051823838974
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->tauBx.size(); ii++)
  {
    if (not (data->tauBx.at(ii) == 0)) continue;
    nobj++;
          if (nobj > 12) break;
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
                                // TAU36: ET >= 72 at BX = 0
      if (not (data->tauIEt.at(idx) >= 72)) continue;

                        // isolation : 0xe
      if (not ((14 >> data->tauIso.at(idx)) & 1)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->tauIEta.at(idx)) and (data->tauIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleTAU_254396839629108990
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->tauBx.size(); ii++)
  {
    if (not (data->tauBx.at(ii) == 0)) continue;
    nobj++;
          if (nobj > 12) break;
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
                                // TAU28: ET >= 56 at BX = 0
      if (not (data->tauIEt.at(idx) >= 56)) continue;

                        // isolation : 0xe
      if (not ((14 >> data->tauIso.at(idx)) & 1)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->tauIEta.at(idx)) and (data->tauIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleTAU_2560239848842802942
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->tauBx.size(); ii++)
  {
    if (not (data->tauBx.at(ii) == 0)) continue;
    nobj++;
          if (nobj > 12) break;
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
                                // TAU38: ET >= 76 at BX = 0
      if (not (data->tauIEt.at(idx) >= 76)) continue;

                        // isolation : 0xe
      if (not ((14 >> data->tauIso.at(idx)) & 1)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->tauIEta.at(idx)) and (data->tauIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleTAU_3484211327656040900
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->tauBx.size(); ii++)
  {
    if (not (data->tauBx.at(ii) == 0)) continue;
    nobj++;
          if (nobj > 12) break;
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
                                // TAU100: ET >= 200 at BX = 0
      if (not (data->tauIEt.at(idx) >= 200)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->tauIEta.at(idx)) and (data->tauIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleTAU_3484215725702552004
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->tauBx.size(); ii++)
  {
    if (not (data->tauBx.at(ii) == 0)) continue;
    nobj++;
          if (nobj > 12) break;
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
                                // TAU120: ET >= 240 at BX = 0
      if (not (data->tauIEt.at(idx) >= 240)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->tauIEta.at(idx)) and (data->tauIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleTAU_3484217924725807556
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->tauBx.size(); ii++)
  {
    if (not (data->tauBx.at(ii) == 0)) continue;
    nobj++;
          if (nobj > 12) break;
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
                                // TAU130: ET >= 260 at BX = 0
      if (not (data->tauIEt.at(idx) >= 260)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->tauIEta.at(idx)) and (data->tauIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
SingleTAU_3484220123749063108
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
  size_t nobj = 0;
  std::vector<int> candidates;
  for (size_t ii = 0; ii < data->tauBx.size(); ii++)
  {
    if (not (data->tauBx.at(ii) == 0)) continue;
    nobj++;
          if (nobj > 12) break;
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
                                // TAU140: ET >= 280 at BX = 0
      if (not (data->tauIEt.at(idx) >= 280)) continue;

                        // -2.1315 <= eta <= 2.1315
              etaWindow1 = ((-49 <= data->tauIEta.at(idx)) and (data->tauIEta.at(idx) <= 48));
            
          if (not etaWindow1) continue;
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

                    




bool
TransverseMass_1757817201761093878
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
    bool pass = false;
  size_t nobj = 0;
  
  for (size_t ii = 0; ii < data->egBx.size(); ii++)
  {
    if (not (data->egBx.at(ii) == 0)) continue;
    nobj++;
          
                                  // EG33: ET >= 66 at BX = 0
      if (not (data->egIEt.at(ii) >= 66)) continue;

                        // isolation : 0xa
      if (not ((10 >> data->egIso.at(ii)) & 1)) continue;

          

    for (size_t jj = 0; jj < data->sumBx.size(); jj++)
    {
      if (not (data->sumType.at(jj) == L1Analysis::kMissingEt)) continue;
      if (not (data->sumBx.at(jj) == 0)) continue;
                          // ETM10: ET >= 20 at BX = 0
      if (not (data->sumIEt.at(jj) >= 20)) continue;
      
          long long minimum;
  long long maximum;
        // 40.0 <= Mt <= 151982.0
      int iPhi = data->egIPhi.at(ii);
  
  unsigned int deltaIPhi = abs(iPhi - data->sumIPhi.at(jj));
  if (deltaIPhi >= 72) deltaIPhi = 2*72 - deltaIPhi;
  
  long long cosDeltaPhi = LUT_COS_DPHI_EG_ETM[deltaIPhi];
  long long pt0 = LUT_EG_ET[data->egIEt.at(ii)];
  long long pt1 = LUT_ETM_ET[data->sumIEt.at(jj)];
  long long mt2 = pt0*pt1*(1*POW10[3] - cosDeltaPhi);
    minimum = (long long)(800.0 * POW10[5]);
  maximum = (long long)(11549264162.0 * POW10[5]);
  if (not ((minimum <= mt2) and (mt2 <= maximum))) continue;

    
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}
    
                    




bool
TransverseMass_3639674040417019497
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
    bool pass = false;
  size_t nobj = 0;
  
  for (size_t ii = 0; ii < data->egBx.size(); ii++)
  {
    if (not (data->egBx.at(ii) == 0)) continue;
    nobj++;
          
                                  // EG33: ET >= 66 at BX = 0
      if (not (data->egIEt.at(ii) >= 66)) continue;

                        // isolation : 0xa
      if (not ((10 >> data->egIso.at(ii)) & 1)) continue;

          

    for (size_t jj = 0; jj < data->sumBx.size(); jj++)
    {
      if (not (data->sumType.at(jj) == L1Analysis::kMissingEt)) continue;
      if (not (data->sumBx.at(jj) == 0)) continue;
                          // ETM10: ET >= 20 at BX = 0
      if (not (data->sumIEt.at(jj) >= 20)) continue;
      
          long long minimum;
  long long maximum;
        // 44.0 <= Mt <= 151982.0
      int iPhi = data->egIPhi.at(ii);
  
  unsigned int deltaIPhi = abs(iPhi - data->sumIPhi.at(jj));
  if (deltaIPhi >= 72) deltaIPhi = 2*72 - deltaIPhi;
  
  long long cosDeltaPhi = LUT_COS_DPHI_EG_ETM[deltaIPhi];
  long long pt0 = LUT_EG_ET[data->egIEt.at(ii)];
  long long pt1 = LUT_ETM_ET[data->sumIEt.at(jj)];
  long long mt2 = pt0*pt1*(1*POW10[3] - cosDeltaPhi);
    minimum = (long long)(968.0 * POW10[5]);
  maximum = (long long)(11549264162.0 * POW10[5]);
  if (not ((minimum <= mt2) and (mt2 <= maximum))) continue;

    
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}
    
                    




bool
TransverseMass_3639674040417019753
(L1Analysis::L1AnalysisL1UpgradeDataFormat* data)
{
    bool pass = false;
  size_t nobj = 0;
  
  for (size_t ii = 0; ii < data->egBx.size(); ii++)
  {
    if (not (data->egBx.at(ii) == 0)) continue;
    nobj++;
          
                                  // EG33: ET >= 66 at BX = 0
      if (not (data->egIEt.at(ii) >= 66)) continue;

                        // isolation : 0xa
      if (not ((10 >> data->egIso.at(ii)) & 1)) continue;

          

    for (size_t jj = 0; jj < data->sumBx.size(); jj++)
    {
      if (not (data->sumType.at(jj) == L1Analysis::kMissingEt)) continue;
      if (not (data->sumBx.at(jj) == 0)) continue;
                          // ETM10: ET >= 20 at BX = 0
      if (not (data->sumIEt.at(jj) >= 20)) continue;
      
          long long minimum;
  long long maximum;
        // 48.0 <= Mt <= 151982.0
      int iPhi = data->egIPhi.at(ii);
  
  unsigned int deltaIPhi = abs(iPhi - data->sumIPhi.at(jj));
  if (deltaIPhi >= 72) deltaIPhi = 2*72 - deltaIPhi;
  
  long long cosDeltaPhi = LUT_COS_DPHI_EG_ETM[deltaIPhi];
  long long pt0 = LUT_EG_ET[data->egIEt.at(ii)];
  long long pt1 = LUT_ETM_ET[data->sumIEt.at(jj)];
  long long mt2 = pt0*pt1*(1*POW10[3] - cosDeltaPhi);
    minimum = (long long)(1152.0 * POW10[5]);
  maximum = (long long)(11549264162.0 * POW10[5]);
  if (not ((minimum <= mt2) and (mt2 <= maximum))) continue;

    
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}
    
      


bool
TripleEG_4430569450691365292
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
  if (candidates.size() < 3) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 3, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(3, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // EG14: ET >= 28 at BX = 0
      if (not (data->egIEt.at(idx) >= 28)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // EG10: ET >= 20 at BX = 0
      if (not (data->egIEt.at(idx) >= 20)) continue;

          
            idx = candidates.at(set.at(indicies.at(2)));
                                // EG8: ET >= 16 at BX = 0
      if (not (data->egIEt.at(idx) >= 16)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
TripleEG_4430569691209534124
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
  if (candidates.size() < 3) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 3, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(3, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // EG18: ET >= 36 at BX = 0
      if (not (data->egIEt.at(idx) >= 36)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // EG17: ET >= 34 at BX = 0
      if (not (data->egIEt.at(idx) >= 34)) continue;

          
            idx = candidates.at(set.at(indicies.at(2)));
                                // EG8: ET >= 16 at BX = 0
      if (not (data->egIEt.at(idx) >= 16)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
TripleEG_667988932384139803
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
  if (candidates.size() < 3) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 3, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(3, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // EG20: ET >= 40 at BX = 0
      if (not (data->egIEt.at(idx) >= 40)) continue;

                        // isolation : 0xc
      if (not ((12 >> data->egIso.at(idx)) & 1)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // EG10: ET >= 20 at BX = 0
      if (not (data->egIEt.at(idx) >= 20)) continue;

          
            idx = candidates.at(set.at(indicies.at(2)));
                                // EG5: ET >= 10 at BX = 0
      if (not (data->egIEt.at(idx) >= 10)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
TripleJET_10368473821548883594
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
  if (candidates.size() < 3) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 3, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(3, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET26: ET >= 52 at BX = 0
      if (not (data->jetIEt.at(idx) >= 52)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET26: ET >= 52 at BX = 0
      if (not (data->jetIEt.at(idx) >= 52)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(2)));
                                // JET26: ET >= 52 at BX = 0
      if (not (data->jetIEt.at(idx) >= 52)) continue;

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
TripleJET_1514927488963884831
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
  if (candidates.size() < 3) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 3, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(3, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET85: ET >= 170 at BX = 0
      if (not (data->jetIEt.at(idx) >= 170)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET72: ET >= 144 at BX = 0
      if (not (data->jetIEt.at(idx) >= 144)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(2)));
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
TripleJET_1514927488965982623
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
  if (candidates.size() < 3) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 3, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(3, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET85: ET >= 170 at BX = 0
      if (not (data->jetIEt.at(idx) >= 170)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET76: ET >= 152 at BX = 0
      if (not (data->jetIEt.at(idx) >= 152)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(2)));
                                // JET105: ET >= 210 at BX = 0
      if (not (data->jetIEt.at(idx) >= 210)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
TripleJET_1776207310752122438
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
  if (candidates.size() < 3) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 3, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(3, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET30: ET >= 60 at BX = 0
      if (not (data->jetIEt.at(idx) >= 60)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET30: ET >= 60 at BX = 0
      if (not (data->jetIEt.at(idx) >= 60)) continue;

          
            idx = candidates.at(set.at(indicies.at(2)));
                                // JET30: ET >= 60 at BX = 0
      if (not (data->jetIEt.at(idx) >= 60)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
TripleJET_4911751765552035770
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
  if (candidates.size() < 3) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 3, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(3, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET68: ET >= 136 at BX = 0
      if (not (data->jetIEt.at(idx) >= 136)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET48: ET >= 96 at BX = 0
      if (not (data->jetIEt.at(idx) >= 96)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(2)));
                                // JET84: ET >= 168 at BX = 0
      if (not (data->jetIEt.at(idx) >= 168)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
TripleJET_4911751765568543162
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
  if (candidates.size() < 3) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 3, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(3, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET72: ET >= 144 at BX = 0
      if (not (data->jetIEt.at(idx) >= 144)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET56: ET >= 112 at BX = 0
      if (not (data->jetIEt.at(idx) >= 112)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(2)));
                                // JET88: ET >= 176 at BX = 0
      if (not (data->jetIEt.at(idx) >= 176)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
TripleJET_4911751765569599162
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
  if (candidates.size() < 3) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 3, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(3, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET76: ET >= 152 at BX = 0
      if (not (data->jetIEt.at(idx) >= 152)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET64: ET >= 128 at BX = 0
      if (not (data->jetIEt.at(idx) >= 128)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(2)));
                                // JET92: ET >= 184 at BX = 0
      if (not (data->jetIEt.at(idx) >= 184)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
TripleJET_4911751765585033658
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
  if (candidates.size() < 3) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 3, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(3, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET84: ET >= 168 at BX = 0
      if (not (data->jetIEt.at(idx) >= 168)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET48: ET >= 96 at BX = 0
      if (not (data->jetIEt.at(idx) >= 96)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(2)));
                                // JET68: ET >= 136 at BX = 0
      if (not (data->jetIEt.at(idx) >= 136)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
TripleJET_4911751765586049466
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
  if (candidates.size() < 3) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 3, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(3, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET84: ET >= 168 at BX = 0
      if (not (data->jetIEt.at(idx) >= 168)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET68: ET >= 136 at BX = 0
      if (not (data->jetIEt.at(idx) >= 136)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(2)));
                                // JET48: ET >= 96 at BX = 0
      if (not (data->jetIEt.at(idx) >= 96)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
TripleJET_4911751765586089658
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
  if (candidates.size() < 3) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 3, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(3, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET88: ET >= 176 at BX = 0
      if (not (data->jetIEt.at(idx) >= 176)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET56: ET >= 112 at BX = 0
      if (not (data->jetIEt.at(idx) >= 112)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(2)));
                                // JET72: ET >= 144 at BX = 0
      if (not (data->jetIEt.at(idx) >= 144)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
TripleJET_4911751765586495930
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
  if (candidates.size() < 3) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 3, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(3, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET83: ET >= 166 at BX = 0
      if (not (data->jetIEt.at(idx) >= 166)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET71: ET >= 142 at BX = 0
      if (not (data->jetIEt.at(idx) >= 142)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(2)));
                                // JET98: ET >= 196 at BX = 0
      if (not (data->jetIEt.at(idx) >= 196)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
TripleJET_4911751765587089594
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
  if (candidates.size() < 3) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 3, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(3, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET88: ET >= 176 at BX = 0
      if (not (data->jetIEt.at(idx) >= 176)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET72: ET >= 144 at BX = 0
      if (not (data->jetIEt.at(idx) >= 144)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(2)));
                                // JET56: ET >= 112 at BX = 0
      if (not (data->jetIEt.at(idx) >= 112)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
TripleJET_4911751765602597050
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
  if (candidates.size() < 3) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 3, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(3, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET92: ET >= 184 at BX = 0
      if (not (data->jetIEt.at(idx) >= 184)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET64: ET >= 128 at BX = 0
      if (not (data->jetIEt.at(idx) >= 128)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(2)));
                                // JET76: ET >= 152 at BX = 0
      if (not (data->jetIEt.at(idx) >= 152)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
TripleJET_4911751765603112890
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
  if (candidates.size() < 3) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 3, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(3, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET92: ET >= 184 at BX = 0
      if (not (data->jetIEt.at(idx) >= 184)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET76: ET >= 152 at BX = 0
      if (not (data->jetIEt.at(idx) >= 152)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(2)));
                                // JET64: ET >= 128 at BX = 0
      if (not (data->jetIEt.at(idx) >= 128)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
TripleJET_4911751765603911482
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
  if (candidates.size() < 3) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 3, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(3, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET98: ET >= 196 at BX = 0
      if (not (data->jetIEt.at(idx) >= 196)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET71: ET >= 142 at BX = 0
      if (not (data->jetIEt.at(idx) >= 142)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(2)));
                                // JET83: ET >= 166 at BX = 0
      if (not (data->jetIEt.at(idx) >= 166)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
TripleJET_4911751765604427322
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
  if (candidates.size() < 3) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 3, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(3, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET98: ET >= 196 at BX = 0
      if (not (data->jetIEt.at(idx) >= 196)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET83: ET >= 166 at BX = 0
      if (not (data->jetIEt.at(idx) >= 166)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(2)));
                                // JET71: ET >= 142 at BX = 0
      if (not (data->jetIEt.at(idx) >= 142)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
TripleJET_655678244564243471
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
  if (candidates.size() < 3) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 3, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(3, permutation);

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

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET72: ET >= 144 at BX = 0
      if (not (data->jetIEt.at(idx) >= 144)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(2)));
                                // JET85: ET >= 170 at BX = 0
      if (not (data->jetIEt.at(idx) >= 170)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
TripleJET_655678244564763279
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
  if (candidates.size() < 3) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 3, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(3, permutation);

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

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET85: ET >= 170 at BX = 0
      if (not (data->jetIEt.at(idx) >= 170)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(2)));
                                // JET72: ET >= 144 at BX = 0
      if (not (data->jetIEt.at(idx) >= 144)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
TripleJET_655678244564915215
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
  if (candidates.size() < 3) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 3, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(3, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET105: ET >= 210 at BX = 0
      if (not (data->jetIEt.at(idx) >= 210)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET76: ET >= 152 at BX = 0
      if (not (data->jetIEt.at(idx) >= 152)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(2)));
                                // JET85: ET >= 170 at BX = 0
      if (not (data->jetIEt.at(idx) >= 170)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
TripleJET_655678244565419151
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
  if (candidates.size() < 3) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 3, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(3, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      bool etaWindow1;
            idx = candidates.at(set.at(indicies.at(0)));
                                // JET105: ET >= 210 at BX = 0
      if (not (data->jetIEt.at(idx) >= 210)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(1)));
                                // JET85: ET >= 170 at BX = 0
      if (not (data->jetIEt.at(idx) >= 170)) continue;

                        // -2.697 <= eta <= 2.697
              etaWindow1 = ((-62 <= data->jetIEta.at(idx)) and (data->jetIEta.at(idx) <= 61));
            
          if (not etaWindow1) continue;
            idx = candidates.at(set.at(indicies.at(2)));
                                // JET76: ET >= 152 at BX = 0
      if (not (data->jetIEt.at(idx) >= 152)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
TripleMU_15692838580664758508
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
  if (candidates.size() < 3) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 3, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(3, permutation);

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

                        // quality : 0xfff0
      if (not ((65520 >> data->muonQual.at(idx)) & 1)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // MU3p5: ET >= 8 at BX = 0
      if (not (data->muonIEt.at(idx) >= 8)) continue;

                        // quality : 0xfff0
      if (not ((65520 >> data->muonQual.at(idx)) & 1)) continue;

          
            idx = candidates.at(set.at(indicies.at(2)));
                                // MU2p5: ET >= 6 at BX = 0
      if (not (data->muonIEt.at(idx) >= 6)) continue;

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
TripleMU_3324682852515662879
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
  if (candidates.size() < 3) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 3, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(3, permutation);

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

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // MU0: ET >= 1 at BX = 0
      if (not (data->muonIEt.at(idx) >= 1)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            idx = candidates.at(set.at(indicies.at(2)));
                                // MU0: ET >= 1 at BX = 0
      if (not (data->muonIEt.at(idx) >= 1)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
TripleMU_3324683353497813023
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
  if (candidates.size() < 3) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 3, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(3, permutation);

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

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // MU0: ET >= 1 at BX = 0
      if (not (data->muonIEt.at(idx) >= 1)) continue;

                        // quality : 0xfff0
      if (not ((65520 >> data->muonQual.at(idx)) & 1)) continue;

          
            idx = candidates.at(set.at(indicies.at(2)));
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
TripleMU_3324683539710430239
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
  if (candidates.size() < 3) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 3, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(3, permutation);

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

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // MU0: ET >= 1 at BX = 0
      if (not (data->muonIEt.at(idx) >= 1)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            idx = candidates.at(set.at(indicies.at(2)));
                                // MU0: ET >= 1 at BX = 0
      if (not (data->muonIEt.at(idx) >= 1)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
TripleMU_3324685351042537503
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
  if (candidates.size() < 3) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 3, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(3, permutation);

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

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // MU3: ET >= 7 at BX = 0
      if (not (data->muonIEt.at(idx) >= 7)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx)) & 1)) continue;

          
            idx = candidates.at(set.at(indicies.at(2)));
                                // MU0: ET >= 1 at BX = 0
      if (not (data->muonIEt.at(idx) >= 1)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
TripleMU_3324685732743223327
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
  if (candidates.size() < 3) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 3, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(3, permutation);

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

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // MU3: ET >= 7 at BX = 0
      if (not (data->muonIEt.at(idx) >= 7)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx)) & 1)) continue;

          
            idx = candidates.at(set.at(indicies.at(2)));
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
TripleMU_3324690130789734431
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
  if (candidates.size() < 3) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 3, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(3, permutation);

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

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // MU3: ET >= 7 at BX = 0
      if (not (data->muonIEt.at(idx) >= 7)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx)) & 1)) continue;

          
            idx = candidates.at(set.at(indicies.at(2)));
                                // MU2: ET >= 5 at BX = 0
      if (not (data->muonIEt.at(idx) >= 5)) continue;

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
TripleMU_3324691511169731615
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
  if (candidates.size() < 3) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 3, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(3, permutation);

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

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // MU3: ET >= 7 at BX = 0
      if (not (data->muonIEt.at(idx) >= 7)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            idx = candidates.at(set.at(indicies.at(2)));
                                // MU3: ET >= 7 at BX = 0
      if (not (data->muonIEt.at(idx) >= 7)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
TripleMU_3324691786047638559
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
  if (candidates.size() < 3) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 3, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(3, permutation);

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

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // MU3: ET >= 7 at BX = 0
      if (not (data->muonIEt.at(idx) >= 7)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            idx = candidates.at(set.at(indicies.at(2)));
                                // MU3: ET >= 7 at BX = 0
      if (not (data->muonIEt.at(idx) >= 7)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
TripleMU_3324692191841327135
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
  if (candidates.size() < 3) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 3, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(3, permutation);

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

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // MU3: ET >= 7 at BX = 0
      if (not (data->muonIEt.at(idx) >= 7)) continue;

                        // quality : 0xf000
      if (not ((61440 >> data->muonQual.at(idx)) & 1)) continue;

          
            idx = candidates.at(set.at(indicies.at(2)));
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
TripleMU_3324692885559266335
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
  if (candidates.size() < 3) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 3, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(3, permutation);

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

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // MU5: ET >= 11 at BX = 0
      if (not (data->muonIEt.at(idx) >= 11)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            idx = candidates.at(set.at(indicies.at(2)));
                                // MU3: ET >= 7 at BX = 0
      if (not (data->muonIEt.at(idx) >= 7)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
TripleMU_3324694397387754527
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
  if (candidates.size() < 3) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 3, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(3, permutation);

  for (size_t ii = 0; ii < combination.size(); ii++)
  {
    const std::vector<int>& set = combination.at(ii);
    for (size_t jj = 0; jj < permutation.size(); jj++)
    {
      const std::vector<int>& indicies = permutation.at(jj);
      int idx = -1;
      
            idx = candidates.at(set.at(indicies.at(0)));
                                // MU4: ET >= 9 at BX = 0
      if (not (data->muonIEt.at(idx) >= 9)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // MU4: ET >= 9 at BX = 0
      if (not (data->muonIEt.at(idx) >= 9)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            idx = candidates.at(set.at(indicies.at(2)));
                                // MU4: ET >= 9 at BX = 0
      if (not (data->muonIEt.at(idx) >= 9)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
TripleMU_6936497366859389375
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
  if (candidates.size() < 3) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 3, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(3, permutation);

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

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // MU4: ET >= 9 at BX = 0
      if (not (data->muonIEt.at(idx) >= 9)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            idx = candidates.at(set.at(indicies.at(2)));
                                // MU2p5: ET >= 6 at BX = 0
      if (not (data->muonIEt.at(idx) >= 6)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            
      pass = true;
      break;
    }

    if (pass) break;
  }

  return pass;
}

      


bool
TripleMU_9287399899537551596
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
  if (candidates.size() < 3) return pass;

  std::vector<std::vector<int> > combination;
  getCombination(candidates.size(), 3, combination);
  std::vector<std::vector<int> > permutation;
  getPermutation(3, permutation);

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

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            idx = candidates.at(set.at(indicies.at(1)));
                                // MU3p5: ET >= 8 at BX = 0
      if (not (data->muonIEt.at(idx) >= 8)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            idx = candidates.at(set.at(indicies.at(2)));
                                // MU2p5: ET >= 6 at BX = 0
      if (not (data->muonIEt.at(idx) >= 6)) continue;

                        // quality : 0xff00
      if (not ((65280 >> data->muonQual.at(idx)) & 1)) continue;

          
            
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
L1_DoubleEG6_HTT240er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleEG_8902241742241126126(data) and SingleHTT_2496626727472(data);
}
bool
L1_DoubleEG6_HTT250er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleEG_8902241742241126126(data) and SingleHTT_2496626727600(data);
}
bool
L1_DoubleEG6_HTT255er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleEG_8902241742241126126(data) and SingleHTT_2496626727605(data);
}
bool
L1_DoubleEG6_HTT270er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleEG_8902241742241126126(data) and SingleHTT_2496626727856(data);
}
bool
L1_DoubleEG6_HTT300er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleEG_8902241742241126126(data) and SingleHTT_2496626743344(data);
}
bool
L1_DoubleEG8er2p6_HTT255er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleEG_13299746526186732683(data) and SingleHTT_2496626727605(data);
}
bool
L1_DoubleEG8er2p6_HTT270er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleEG_13299746526186732683(data) and SingleHTT_2496626727856(data);
}
bool
L1_DoubleEG8er2p6_HTT300er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleEG_13299746526186732683(data) and SingleHTT_2496626743344(data);
}
bool
L1_DoubleEG_15_10(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleEG_14367282104050956127(data);
}
bool
L1_DoubleEG_18_17(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleEG_14367295298190490335(data);
}
bool
L1_DoubleEG_20_18(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleEG_14367823063771822943(data);
}
bool
L1_DoubleEG_22_10(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleEG_14367831859864844127(data);
}
bool
L1_DoubleEG_22_12(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleEG_14367831859864844383(data);
}
bool
L1_DoubleEG_22_15(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleEG_14367831859864844767(data);
}
bool
L1_DoubleEG_23_10(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleEG_14367836257911355231(data);
}
bool
L1_DoubleEG_24_17(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleEG_14367840655957867231(data);
}
bool
L1_DoubleEG_25_12(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleEG_14367845054004377695(data);
}
bool
L1_DoubleEG_25_13(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleEG_14367845054004377823(data);
}
bool
L1_DoubleEG_25_14(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleEG_14367845054004377951(data);
}
bool
L1_DoubleEG_LooseIso23_10(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleEG_9170720688096593570(data);
}
bool
L1_DoubleEG_LooseIso24_10(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleEG_13782406706523981474(data);
}
bool
L1_DoubleIsoTau28er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleTAU_14808338227894500078(data);
}
bool
L1_DoubleIsoTau30er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleTAU_14808338292319009533(data);
}
bool
L1_DoubleIsoTau32er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleTAU_973280238110587646(data);
}
bool
L1_DoubleIsoTau33er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleTAU_3279123247861152510(data);
}
bool
L1_DoubleIsoTau34er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleTAU_5584966257611717374(data);
}
bool
L1_DoubleIsoTau35er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleTAU_7890809267362282238(data);
}
bool
L1_DoubleIsoTau36er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleTAU_10196652277112847102(data);
}
bool
L1_DoubleIsoTau38er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleTAU_14808338296613976830(data);
}
bool
L1_DoubleJet100er2p3_dEta_Max1p6(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return CaloCaloCorrelation_7041035331702023693(data);
}
bool
L1_DoubleJet100er2p7(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleJET_15894403592514695266(data);
}
bool
L1_DoubleJet112er2p3_dEta_Max1p6(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return CaloCaloCorrelation_7041035331710545453(data);
}
bool
L1_DoubleJet112er2p7(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleJET_15903553762640785506(data);
}
bool
L1_DoubleJet120er2p7(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleJET_15912422389070688354(data);
}
bool
L1_DoubleJet150er2p7(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleJET_15939450583904677986(data);
}
bool
L1_DoubleJet30_Mass_Min300_dEta_Max1p5(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return InvariantMass_3160746219321117174(data);
}
bool
L1_DoubleJet30_Mass_Min320_dEta_Max1p5(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return InvariantMass_3160750617367628278(data);
}
bool
L1_DoubleJet30_Mass_Min340_dEta_Max1p5(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return InvariantMass_3160755015414139382(data);
}
bool
L1_DoubleJet30_Mass_Min360_dEta_Max1p5(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return InvariantMass_3160759413460650486(data);
}
bool
L1_DoubleJet30_Mass_Min380_dEta_Max1p5(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return InvariantMass_3160763811507161590(data);
}
bool
L1_DoubleJet30_Mass_Min400_Mu10(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17545683025133343173(data) and InvariantMass_2940638391871890823(data);
}
bool
L1_DoubleJet30_Mass_Min400_Mu6(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293122775847365(data) and InvariantMass_2940638391871890823(data);
}
bool
L1_DoubleJet30_Mass_Min400_dEta_Max1p5(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return InvariantMass_3161027694297827830(data);
}
bool
L1_DoubleJet35_rmovlp_IsoTau45_Mass_Min450(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return InvariantMassOvRm_10967205787862279205(data);
}
bool
L1_DoubleJet40er2p7(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleJET_8659155958470085331(data);
}
bool
L1_DoubleJet50er2p7(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleJET_8659228526237518547(data);
}
bool
L1_DoubleJet60er2p7(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleJET_8659301094004951763(data);
}
bool
L1_DoubleJet60er2p7_ETM100(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleJET_8659301094004951763(data) and SingleETM_2393532815408(data);
}
bool
L1_DoubleJet60er2p7_ETM60(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleJET_8659301094004951763(data) and SingleETM_18699475760(data);
}
bool
L1_DoubleJet60er2p7_ETM70(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleJET_8659301094004951763(data) and SingleETM_18699475888(data);
}
bool
L1_DoubleJet60er2p7_ETM80(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleJET_8659301094004951763(data) and SingleETM_18699476016(data);
}
bool
L1_DoubleJet60er2p7_ETM90(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleJET_8659301094004951763(data) and SingleETM_18699476144(data);
}
bool
L1_DoubleJet80er2p7(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleJET_8659446229539818195(data);
}
bool
L1_DoubleJet_100_30_DoubleJet30_Mass_Min620(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleJET_16307690244847013269(data) and InvariantMass_2940638391876117895(data);
}
bool
L1_DoubleJet_100_35_DoubleJet35_Mass_Min620(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleJET_16307690244847013909(data) and InvariantMass_2940649386995017095(data);
}
bool
L1_DoubleJet_110_35_DoubleJet35_Mass_Min620(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleJET_16379747838884941845(data) and InvariantMass_2940649386995017095(data);
}
bool
L1_DoubleJet_110_40_DoubleJet40_Mass_Min620(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleJET_16379747838884957589(data) and InvariantMass_2940919866919937415(data);
}
bool
L1_DoubleJet_115_35_DoubleJet35_Mass_Min620(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleJET_16382562588652048405(data) and InvariantMass_2940649386995017095(data);
}
bool
L1_DoubleJet_115_40_DoubleJet40_Mass_Min620(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleJET_16382562588652064149(data) and InvariantMass_2940919866919937415(data);
}
bool
L1_DoubleJet_90_30_DoubleJet30_Mass_Min620(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleJET_4162612533456677351(data) and InvariantMass_2940638391876117895(data);
}
bool
L1_DoubleLooseIsoEG22er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleEG_2355036583129339571(data);
}
bool
L1_DoubleLooseIsoEG24er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleEG_2931778810409473715(data);
}
bool
L1_DoubleMu0(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleMU_14585777620730815295(data);
}
bool
L1_DoubleMu0_ETM40(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleMU_14585777620730815295(data) and SingleETM_18699475504(data);
}
bool
L1_DoubleMu0_ETM55(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleMU_14585777620730815295(data) and SingleETM_18699475637(data);
}
bool
L1_DoubleMu0_ETM60(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleMU_14585777620730815295(data) and SingleETM_18699475760(data);
}
bool
L1_DoubleMu0_ETM65(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleMU_14585777620730815295(data) and SingleETM_18699475765(data);
}
bool
L1_DoubleMu0_ETM70(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleMU_14585777620730815295(data) and SingleETM_18699475888(data);
}
bool
L1_DoubleMu0_SQ(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleMU_14585778268989477695(data);
}
bool
L1_DoubleMu0_SQ_OS(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleMU_3139255731352238604(data);
}
bool
L1_DoubleMu0er1p4_SQ_OS_dR_Max1p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return MuonMuonCorrelation_9513481109949270451(data);
}
bool
L1_DoubleMu0er1p4_dEta_Max1p8_OS(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return MuonMuonCorrelation_7972376774213455602(data);
}
bool
L1_DoubleMu0er1p5_SQ_OS(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleMU_14617142003772573591(data);
}
bool
L1_DoubleMu0er1p5_SQ_OS_dR_Max1p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return MuonMuonCorrelation_9513481109957663155(data);
}
bool
L1_DoubleMu0er1p5_SQ_dR_Max1p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return MuonMuonCorrelation_15199048927445899759(data);
}
bool
L1_DoubleMu0er2_SQ_dR_Max1p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return MuonMuonCorrelation_15199048929593776303(data);
}
bool
L1_DoubleMu18er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleMU_16323903523977050720(data);
}
bool
L1_DoubleMu22er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleMU_2488845469206592112(data);
}
bool
L1_DoubleMu3_OS_DoubleEG7p5Upsilon(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return InvariantMass_16981538589298500419(data) and InvariantMass_4461482972834602413(data);
}
bool
L1_DoubleMu3_SQ_ETMHF40_Jet60_OR_DoubleJet30(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleMU_14585786515326686015(data) and SingleETMHF_306372248967728(data) and (DoubleJET_3730266969229109735(data) or SingleJET_20010310448(data));
}
bool
L1_DoubleMu3_SQ_ETMHF50_Jet60_OR_DoubleJet30(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleMU_14585786515326686015(data) and SingleETMHF_306372248967856(data) and (DoubleJET_3730266969229109735(data) or SingleJET_20010310448(data));
}
bool
L1_DoubleMu3_SQ_ETMHF60_Jet60_OR_DoubleJet30(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleMU_14585786515326686015(data) and SingleETMHF_306372248967984(data) and (DoubleJET_3730266969229109735(data) or SingleJET_20010310448(data));
}
bool
L1_DoubleMu3_SQ_ETMHF70_Jet60_OR_DoubleJet30(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleMU_14585786515326686015(data) and SingleETMHF_306372248968112(data) and (DoubleJET_3730266969229109735(data) or SingleJET_20010310448(data));
}
bool
L1_DoubleMu3_SQ_ETMHF80_Jet60_OR_DoubleJet30(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleMU_14585786515326686015(data) and SingleETMHF_306372248968240(data) and (DoubleJET_3730266969229109735(data) or SingleJET_20010310448(data));
}
bool
L1_DoubleMu3_SQ_HTT100er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleMU_14585786515326686015(data) and SingleHTT_2496626710576(data);
}
bool
L1_DoubleMu3_SQ_HTT200er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleMU_14585786515326686015(data) and SingleHTT_2496626726960(data);
}
bool
L1_DoubleMu3_SQ_HTT220er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleMU_14585786515326686015(data) and SingleHTT_2496626727216(data);
}
bool
L1_DoubleMu3_SQ_HTT240er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleMU_14585786515326686015(data) and SingleHTT_2496626727472(data);
}
bool
L1_DoubleMu4_OS_EG12(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleMU_3224017188937267724(data) and SingleEG_145873074(data);
}
bool
L1_DoubleMu4_SQ_OS(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleMU_3229327723899648524(data);
}
bool
L1_DoubleMu4_SQ_OS_dR_Max1p2(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return MuonMuonCorrelation_16784489743460462578(data);
}
bool
L1_DoubleMu4p5_SQ(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleMU_17582786187978172426(data);
}
bool
L1_DoubleMu4p5_SQ_OS(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleMU_2011765979326275391(data);
}
bool
L1_DoubleMu4p5_SQ_OS_dR_Max1p2(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return MuonMuonCorrelation_12923126501326425857(data);
}
bool
L1_DoubleMu4p5er2p0_SQ_OS(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleMU_13627348644483379947(data);
}
bool
L1_DoubleMu4p5er2p0_SQ_OS_Mass7to18(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return InvariantMass_2342552854377181621(data);
}
bool
L1_DoubleMu5Upsilon_OS_DoubleEG3(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return InvariantMass_13689376201502793133(data) and InvariantMass_2443380592745462540(data);
}
bool
L1_DoubleMu5_OS_EG12(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleMU_3246535187074120204(data) and SingleEG_145873074(data);
}
bool
L1_DoubleMu5_SQ_OS(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleMU_3251845722036501004(data);
}
bool
L1_DoubleMu5_SQ_OS_Mass7to18(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return InvariantMass_14086745238924011567(data);
}
bool
L1_DoubleMu6_SQ_OS(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleMU_3274363720173353484(data);
}
bool
L1_DoubleMu7_EG7(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleMU_14585796862184301375(data) and SingleEG_1139639(data);
}
bool
L1_DoubleMu7_SQ_EG7(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleMU_14585797510442963775(data) and SingleEG_1139639(data);
}
bool
L1_DoubleMu8_SQ(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleMU_14585800259222033215(data);
}
bool
L1_DoubleMu_10_0_dEta_Max1p8(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return MuonMuonCorrelation_8772456668275224612(data);
}
bool
L1_DoubleMu_11_4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleMU_16961154507842811908(data);
}
bool
L1_DoubleMu_12_5(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleMU_16961157256621881348(data);
}
bool
L1_DoubleMu_12_8(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleMU_16961163853691648004(data);
}
bool
L1_DoubleMu_13_6(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleMU_16961160005400950788(data);
}
bool
L1_DoubleMu_15_5(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleMU_16961158905889323012(data);
}
bool
L1_DoubleMu_15_5_SQ(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleMU_16961159554147985412(data);
}
bool
L1_DoubleMu_15_7(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleMU_16961163303935834116(data);
}
bool
L1_DoubleMu_15_7_SQ(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleMU_16961163952194496516(data);
}
bool
L1_DoubleMu_15_7_SQ_Mass_Min4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleMU_16961163952194496516(data) and InvariantMass_3136996817261618632(data);
}
bool
L1_DoubleMu_20_2_SQ_Mass_Max20(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return InvariantMass_15577908206133012537(data);
}
bool
L1_DoubleTau50er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleTAU_15233202657361500387(data);
}
bool
L1_DoubleTau70er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return DoubleTAU_17539608616528615651(data);
}
bool
L1_EG25er2p1_HTT125er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_14262501742662192051(data) and SingleHTT_2496626710837(data);
}
bool
L1_EG27er2p1_HTT200er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_14262501742930627507(data) and SingleHTT_2496626726960(data);
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
L1_ETMHF100_Jet60_OR_DiJet30woTT28(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETMHF_39215647867820080(data) and (DoubleJET_10840719965249128790(data) or DoubleJET_7821119013284253287(data) or DoubleJET_7821119012726214247(data) or DoubleJET_3851467703875127396(data) or DoubleJET_17504692923644168291(data) or DoubleJET_3851467703317088356(data) or SingleJET_20010310448(data));
}
bool
L1_ETMHF100_Jet60_OR_DoubleJet30(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETMHF_39215647867820080(data) and (DoubleJET_3730266969229109735(data) or SingleJET_20010310448(data));
}
bool
L1_ETMHF100_Jet90_OR_DoubleJet45_OR_TripleJet30(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETMHF_39215647867820080(data) and (TripleJET_1776207310752122438(data) or DoubleJET_3805139313034161255(data) or SingleJET_20010310832(data));
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
L1_ETMHF110_Jet60_OR_DiJet30woTT28(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETMHF_39215647867820208(data) and (DoubleJET_10840719965249128790(data) or DoubleJET_7821119013284253287(data) or DoubleJET_7821119012726214247(data) or DoubleJET_3851467703875127396(data) or DoubleJET_17504692923644168291(data) or DoubleJET_3851467703317088356(data) or SingleJET_20010310448(data));
}
bool
L1_ETMHF110_Jet90_OR_DoubleJet45_OR_TripleJet30(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETMHF_39215647867820208(data) and (TripleJET_1776207310752122438(data) or DoubleJET_3805139313034161255(data) or SingleJET_20010310832(data));
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
L1_ETMHF120_Jet60_OR_DiJet30woTT28(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETMHF_39215647867820336(data) and (DoubleJET_10840719965249128790(data) or DoubleJET_7821119013284253287(data) or DoubleJET_7821119012726214247(data) or DoubleJET_3851467703875127396(data) or DoubleJET_17504692923644168291(data) or DoubleJET_3851467703317088356(data) or SingleJET_20010310448(data));
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
L1_ETMHF70_Jet90_OR_DoubleJet45_OR_TripleJet30(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETMHF_306372248968112(data) and (TripleJET_1776207310752122438(data) or DoubleJET_3805139313034161255(data) or SingleJET_20010310832(data));
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
L1_ETMHF80_Jet90_OR_DoubleJet45_OR_TripleJet30(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETMHF_306372248968240(data) and (TripleJET_1776207310752122438(data) or DoubleJET_3805139313034161255(data) or SingleJET_20010310832(data));
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
L1_ETMHF90_Jet90_OR_DoubleJet45_OR_TripleJet30(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleETMHF_306372248968368(data) and (TripleJET_1776207310752122438(data) or DoubleJET_3805139313034161255(data) or SingleJET_20010310832(data));
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
L1_HTT250er_QuadJet_70_55_40_35_er2p5(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleHTT_2496626727600(data) and QuadJET_17630949366336433287(data);
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
L1_HTT280er_QuadJet_70_55_40_35_er2p5(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleHTT_2496626727984(data) and QuadJET_17630949366336433287(data);
}
bool
L1_HTT300er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleHTT_2496626743344(data);
}
bool
L1_HTT300er_QuadJet_70_55_40_35_er2p5(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleHTT_2496626743344(data) and QuadJET_17630949366336433287(data);
}
bool
L1_HTT320er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleHTT_2496626743600(data);
}
bool
L1_HTT320er_QuadJet_70_55_40_40_er2p4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleHTT_2496626743600(data) and QuadJET_2969443065613019316(data);
}
bool
L1_HTT320er_QuadJet_70_55_40_40_er2p5(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleHTT_2496626743600(data) and QuadJET_17665570788471843975(data);
}
bool
L1_HTT320er_QuadJet_70_55_45_45_er2p5(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleHTT_2496626743600(data) and QuadJET_17666978163355397295(data);
}
bool
L1_HTT340er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleHTT_2496626743856(data);
}
bool
L1_HTT340er_QuadJet_70_55_40_40_er2p5(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleHTT_2496626743856(data) and QuadJET_17665570788471843975(data);
}
bool
L1_HTT340er_QuadJet_70_55_45_45_er2p5(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleHTT_2496626743856(data) and QuadJET_17666978163355397295(data);
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
L1_IsoEG33_Mt40(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return TransverseMass_1757817201761093878(data);
}
bool
L1_IsoEG33_Mt44(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return TransverseMass_3639674040417019497(data);
}
bool
L1_IsoEG33_Mt48(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return TransverseMass_3639674040417019753(data);
}
bool
L1_IsoTau40er_ETM100(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleTAU_12210388642533153582(data) and SingleETM_2393532815408(data);
}
bool
L1_IsoTau40er_ETM105(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleTAU_12210388642533153582(data) and SingleETM_2393532815413(data);
}
bool
L1_IsoTau40er_ETM110(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleTAU_12210388642533153582(data) and SingleETM_2393532815536(data);
}
bool
L1_IsoTau40er_ETM115(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleTAU_12210388642533153582(data) and SingleETM_2393532815541(data);
}
bool
L1_IsoTau40er_ETM120(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleTAU_12210388642533153582(data) and SingleETM_2393532815664(data);
}
bool
L1_IsoTau40er_ETM80(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleTAU_12210388642533153582(data) and SingleETM_18699476016(data);
}
bool
L1_IsoTau40er_ETM85(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleTAU_12210388642533153582(data) and SingleETM_18699476021(data);
}
bool
L1_IsoTau40er_ETM90(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleTAU_12210388642533153582(data) and SingleETM_18699476144(data);
}
bool
L1_IsoTau40er_ETM95(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleTAU_12210388642533153582(data) and SingleETM_18699476149(data);
}
bool
L1_IsoTau40er_ETMHF100(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleTAU_12210388642533153582(data) and SingleETMHF_39215647867820080(data);
}
bool
L1_IsoTau40er_ETMHF110(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleTAU_12210388642533153582(data) and SingleETMHF_39215647867820208(data);
}
bool
L1_IsoTau40er_ETMHF120(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleTAU_12210388642533153582(data) and SingleETMHF_39215647867820336(data);
}
bool
L1_IsoTau40er_ETMHF80(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleTAU_12210388642533153582(data) and SingleETMHF_306372248968240(data);
}
bool
L1_IsoTau40er_ETMHF90(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleTAU_12210388642533153582(data) and SingleETMHF_306372248968368(data);
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
L1_LooseIsoEG22er2p1_IsoTau26er2p1_dR_Min0p3(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return CaloCaloCorrelation_911641433388533200(data);
}
bool
L1_LooseIsoEG24er2p1_HTT100er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_9244738805910375422(data) and SingleHTT_2496626710576(data);
}
bool
L1_LooseIsoEG24er2p1_IsoTau27er2p1_dR_Min0p3(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return CaloCaloCorrelation_911641502108141008(data);
}
bool
L1_LooseIsoEG24er2p1_Jet26er2p7_dR_Min0p3(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return CaloCaloCorrelation_9825171649083341880(data);
}
bool
L1_LooseIsoEG24er2p1_TripleJet_26er2p7_26_26er2p7(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_9244738805910375422(data) and TripleJET_10368473821548883594(data);
}
bool
L1_LooseIsoEG26er2p1_HTT100er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_9244741004933630974(data) and SingleHTT_2496626710576(data);
}
bool
L1_LooseIsoEG26er2p1_Jet34er2p7_dR_Min0p3(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return CaloCaloCorrelation_12094985861278072376(data);
}
bool
L1_LooseIsoEG28er2p1_HTT100er(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_9244743203956886526(data) and SingleHTT_2496626710576(data);
}
bool
L1_LooseIsoEG28er2p1_Jet34er2p7_dR_Min0p3(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return CaloCaloCorrelation_12094985861278072888(data);
}
bool
L1_LooseIsoEG30er2p1_Jet34er2p7_dR_Min0p3(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return CaloCaloCorrelation_12094985861278103608(data);
}
bool
L1_MU20_EG15(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17545685224156598725(data) and SingleEG_145873077(data);
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
L1_Mu10er2p3_Jet32er2p3_dR_Max0p4_DoubleJet32er2p3_dEta_Max1p6(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return CaloMuonCorrelation_1722762447326210349(data) and CaloCaloCorrelation_3813196582576312175(data);
}
bool
L1_Mu12_EG10(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17545683059493081541(data) and SingleEG_145873072(data);
}
bool
L1_Mu12er2p3_Jet40er2p3_dR_Max0p4_DoubleJet40er2p3_dEta_Max1p6(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return CaloMuonCorrelation_3992576659521005869(data) and CaloCaloCorrelation_3813196582576378703(data);
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
L1_Mu18er2p1_IsoTau26er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_7181677643621025184(data) and SingleTAU_218368042610145022(data);
}
bool
L1_Mu18er2p1_Tau24er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_7181677643621025184(data) and SingleTAU_16608831008486494024(data);
}
bool
L1_Mu20_EG10(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17545685224156598725(data) and SingleEG_145873072(data);
}
bool
L1_Mu20_EG17(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17545685224156598725(data) and SingleEG_145873079(data);
}
bool
L1_Mu20_LooseIsoEG6(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17545685224156598725(data) and SingleEG_12507428088042853184(data);
}
bool
L1_Mu20er2p1_IsoTau26er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_9343405464758863264(data) and SingleTAU_218368042610145022(data);
}
bool
L1_Mu20er2p1_IsoTau27er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_9343405464758863264(data) and SingleTAU_236382441119627006(data);
}
bool
L1_Mu22er2p1_IsoTau28er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_9379434261777827232(data) and SingleTAU_254396839629108990(data);
}
bool
L1_Mu22er2p1_IsoTau30er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_9379434261777827232(data) and SingleTAU_2416124660766947070(data);
}
bool
L1_Mu22er2p1_IsoTau32er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_9379434261777827232(data) and SingleTAU_2452153457785911038(data);
}
bool
L1_Mu22er2p1_IsoTau33er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_9379434261777827232(data) and SingleTAU_2470167856295393022(data);
}
bool
L1_Mu22er2p1_IsoTau34er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_9379434261777827232(data) and SingleTAU_2488182254804875006(data);
}
bool
L1_Mu22er2p1_IsoTau35er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_9379434261777827232(data) and SingleTAU_2506196653314356990(data);
}
bool
L1_Mu22er2p1_IsoTau36er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_9379434261777827232(data) and SingleTAU_2524211051823838974(data);
}
bool
L1_Mu22er2p1_IsoTau38er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_9379434261777827232(data) and SingleTAU_2560239848842802942(data);
}
bool
L1_Mu22er2p1_IsoTau40er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17494117756195063635(data) and SingleTAU_12210388642533153582(data);
}
bool
L1_Mu22er2p1_Tau50er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_9379434261777827232(data) and SingleTAU_16608837536836783944(data);
}
bool
L1_Mu22er2p1_Tau70er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_9379434261777827232(data) and SingleTAU_16608841934883295048(data);
}
bool
L1_Mu23_EG10(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17545685275696206277(data) and SingleEG_145873072(data);
}
bool
L1_Mu23_LooseIsoEG10(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17545685275696206277(data) and SingleEG_12507579852048143168(data);
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
L1_Mu5_EG15(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293105595978181(data) and SingleEG_145873077(data);
}
bool
L1_Mu5_EG20(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293105595978181(data) and SingleEG_145873200(data);
}
bool
L1_Mu5_EG23(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293105595978181(data) and SingleEG_145873203(data);
}
bool
L1_Mu5_LooseIsoEG18(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293105595978181(data) and SingleEG_12507579852056531776(data);
}
bool
L1_Mu5_LooseIsoEG20(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293105595978181(data) and SingleEG_12507579852182360896(data);
}
bool
L1_Mu6_DoubleEG10(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293122775847365(data) and DoubleEG_14367260113818400607(data);
}
bool
L1_Mu6_DoubleEG17(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293122775847365(data) and DoubleEG_14367290900143979231(data);
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
L1_Mu7_EG23(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293139955716549(data) and SingleEG_145873203(data);
}
bool
L1_Mu7_LooseIsoEG20(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293139955716549(data) and SingleEG_12507579852182360896(data);
}
bool
L1_Mu7_LooseIsoEG23(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293139955716549(data) and SingleEG_12507579852185506624(data);
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
L1_QuadJet36er2p7_IsoTau52er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return QuadJET_2680035217249740980(data) and SingleTAU_14552260448765811502(data);
}
bool
L1_QuadJet36er2p7_Tau52(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return QuadJET_2680035217249740980(data) and SingleTAU_22686292658(data);
}
bool
L1_QuadJet40er2p7(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return QuadJET_2750930524417894580(data);
}
bool
L1_QuadJet50er2p7(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return QuadJET_2825312486036940980(data);
}
bool
L1_QuadJet60er2p7(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return QuadJET_2899694447655987380(data);
}
bool
L1_QuadMu0(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return QuadMU_509409160461874775(data);
}
bool
L1_SingleEG10(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_145873072(data);
}
bool
L1_SingleEG15(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_145873077(data);
}
bool
L1_SingleEG18(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_145873080(data);
}
bool
L1_SingleEG24(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_145873204(data);
}
bool
L1_SingleEG26(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_145873206(data);
}
bool
L1_SingleEG28(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_145873208(data);
}
bool
L1_SingleEG2_BptxAND(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_1139634(data) and SingleEXT_1189548080491112364(data);
}
bool
L1_SingleEG30(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_145873328(data);
}
bool
L1_SingleEG32(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_145873330(data);
}
bool
L1_SingleEG34(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_145873332(data);
}
bool
L1_SingleEG34er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_14262501759707843507(data);
}
bool
L1_SingleEG36(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_145873334(data);
}
bool
L1_SingleEG36er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_14262501759976278963(data);
}
bool
L1_SingleEG38(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_145873336(data);
}
bool
L1_SingleEG38er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_14262501760244714419(data);
}
bool
L1_SingleEG40(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_145873456(data);
}
bool
L1_SingleEG42(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_145873458(data);
}
bool
L1_SingleEG45(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_145873461(data);
}
bool
L1_SingleEG5(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_1139637(data);
}
bool
L1_SingleEG50(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_145873584(data);
}
bool
L1_SingleIsoEG18(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_12507579852056531520(data);
}
bool
L1_SingleIsoEG18er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_6872811427209405681(data);
}
bool
L1_SingleIsoEG20(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_12507579852182360640(data);
}
bool
L1_SingleIsoEG20er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_6872943368604738801(data);
}
bool
L1_SingleIsoEG22(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_12507579852184457792(data);
}
bool
L1_SingleIsoEG22er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_6872945567627994353(data);
}
bool
L1_SingleIsoEG24(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_12507579852186554944(data);
}
bool
L1_SingleIsoEG24er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_6872947766651249905(data);
}
bool
L1_SingleIsoEG26(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_12507579852188652096(data);
}
bool
L1_SingleIsoEG26er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_6872949965674505457(data);
}
bool
L1_SingleIsoEG28(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_12507579852190749248(data);
}
bool
L1_SingleIsoEG28er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_6872952164697761009(data);
}
bool
L1_SingleIsoEG30(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_12507579852316578368(data);
}
bool
L1_SingleIsoEG30er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_6873084106093094129(data);
}
bool
L1_SingleIsoEG32(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_12507579852318675520(data);
}
bool
L1_SingleIsoEG32er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_6873086305116349681(data);
}
bool
L1_SingleIsoEG33er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_6873087404627977457(data);
}
bool
L1_SingleIsoEG34(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_12507579852320772672(data);
}
bool
L1_SingleIsoEG34er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_6873088504139605233(data);
}
bool
L1_SingleIsoEG35(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_12507579852321821248(data);
}
bool
L1_SingleIsoEG35er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_6873089603651233009(data);
}
bool
L1_SingleIsoEG36(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_12507579852322869824(data);
}
bool
L1_SingleIsoEG36er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_9244881742421986046(data);
}
bool
L1_SingleIsoEG37(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_12507579852323918400(data);
}
bool
L1_SingleIsoEG38(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_12507579852324966976(data);
}
bool
L1_SingleIsoEG38er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_9244883941445241598(data);
}
bool
L1_SingleIsoEG40(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_12507579852450796096(data);
}
bool
L1_SingleIsoEG40er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleEG_9245015882840574718(data);
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
L1_SingleJet20er2p7_NotBptxOR(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleJET_5967545309672598855(data) and ( not SingleEXT_6102799243448260461(data));
}
bool
L1_SingleJet20er2p7_NotBptxOR_3BX(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleJET_5967545309672598855(data) and ( not SingleEXT_6909925150529645533(data)) and ( not SingleEXT_6102799243448260461(data)) and ( not SingleEXT_6909925150529645277(data));
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
L1_SingleJet43er2p7_NotBptxOR_3BX(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleJET_5967545344434990407(data) and ( not SingleEXT_6909925150529645533(data)) and ( not SingleEXT_6102799243448260461(data)) and ( not SingleEXT_6909925150529645277(data));
}
bool
L1_SingleJet46er2p7_NotBptxOR_3BX(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleJET_5967545344837643591(data) and ( not SingleEXT_6909925150529645533(data)) and ( not SingleEXT_6102799243448260461(data)) and ( not SingleEXT_6909925150529645277(data));
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
L1_SingleMu10_LowQ(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17545683021081726533(data);
}
bool
L1_SingleMu11_LowQ(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17545683038261595717(data);
}
bool
L1_SingleMu12_LowQ_BMTF(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_7069342828816371872(data);
}
bool
L1_SingleMu12_LowQ_EMTF(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_7270359269352285314(data);
}
bool
L1_SingleMu12_LowQ_OMTF(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_7990946204847842434(data);
}
bool
L1_SingleMu14er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_7109620049583097248(data);
}
bool
L1_SingleMu16(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17545683128212558277(data);
}
bool
L1_SingleMu16er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_7145648846602061216(data);
}
bool
L1_SingleMu18(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17545683162572296645(data);
}
bool
L1_SingleMu18er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_7181677643621025184(data);
}
bool
L1_SingleMu20(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17545685224156598725(data);
}
bool
L1_SingleMu20er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_9343405464758863264(data);
}
bool
L1_SingleMu22(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17545685258516337093(data);
}
bool
L1_SingleMu22_BMTF(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_9379434265999970464(data);
}
bool
L1_SingleMu22_EMTF(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_6225176160372139651(data);
}
bool
L1_SingleMu22_OMTF(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_6945763095867696771(data);
}
bool
L1_SingleMu22er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_9379434261777827232(data);
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
L1_SingleMu3er1p5_SingleJet100er2p5_ETMHF40(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_17416866089078942815(data) and SingleJET_3448182530626688965(data) and SingleETMHF_306372248967728(data);
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
L1_SingleMuOpen_NotBptxOR(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293018627052229(data) and ( not SingleEXT_6102799243448260461(data));
}
bool
L1_SingleMuOpen_NotBptxOR_3BX(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleMU_14769293018627052229(data) and ( not SingleEXT_6909925150529645533(data)) and ( not SingleEXT_6102799243448260461(data)) and ( not SingleEXT_6909925150529645277(data));
}
bool
L1_SingleTau100er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleTAU_3484211327656040900(data);
}
bool
L1_SingleTau120er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleTAU_3484215725702552004(data);
}
bool
L1_SingleTau130er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleTAU_3484217924725807556(data);
}
bool
L1_SingleTau140er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleTAU_3484220123749063108(data);
}
bool
L1_SingleTau20(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleTAU_22686292272(data);
}
bool
L1_SingleTau80er2p1(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return SingleTAU_16608844133906550600(data);
}
bool
L1_TripleEG_14_10_8(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return TripleEG_4430569450691365292(data);
}
bool
L1_TripleEG_18_17_8(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return TripleEG_4430569691209534124(data);
}
bool
L1_TripleEG_LooseIso20_10_5(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return TripleEG_667988932384139803(data);
}
bool
L1_TripleJet_100_85_72_VBF(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return TripleJET_655678244564763279(data) or TripleJET_655678244564243471(data) or TripleJET_1514927488963884831(data);
}
bool
L1_TripleJet_105_85_76_VBF(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return TripleJET_655678244565419151(data) or TripleJET_655678244564915215(data) or TripleJET_1514927488965982623(data);
}
bool
L1_TripleJet_84_68_48_VBF(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return TripleJET_4911751765586049466(data) or TripleJET_4911751765585033658(data) or TripleJET_4911751765552035770(data);
}
bool
L1_TripleJet_88_72_56_VBF(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return TripleJET_4911751765587089594(data) or TripleJET_4911751765586089658(data) or TripleJET_4911751765568543162(data);
}
bool
L1_TripleJet_92_76_64_VBF(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return TripleJET_4911751765603112890(data) or TripleJET_4911751765602597050(data) or TripleJET_4911751765569599162(data);
}
bool
L1_TripleJet_98_83_71_VBF(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return TripleJET_4911751765604427322(data) or TripleJET_4911751765603911482(data) or TripleJET_4911751765586495930(data);
}
bool
L1_TripleMu0(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return TripleMU_3324682852515662879(data);
}
bool
L1_TripleMu0_OQ(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return TripleMU_3324683353497813023(data);
}
bool
L1_TripleMu3(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return TripleMU_3324691511169731615(data);
}
bool
L1_TripleMu3_SQ(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return TripleMU_3324692191841327135(data);
}
bool
L1_TripleMu_4_4_4(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return TripleMU_3324694397387754527(data);
}
bool
L1_TripleMu_5OQ_3p5OQ_2p5OQ_DoubleMu_5_2p5_OQ_OS_Mass_5to17(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return TripleMU_15692838580664758508(data) and InvariantMass_15192153509407276420(data) and ( not InvariantMass_3324232561693118895(data));
}
bool
L1_TripleMu_5OQ_3p5OQ_2p5OQ_DoubleMu_5_2p5_OQ_OS_Mass_8to14(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return TripleMU_15692838580664758508(data) and InvariantMass_15192160106477018500(data) and ( not InvariantMass_3324232561693118895(data));
}
bool
L1_TripleMu_5SQ_3SQ_0OQ(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return TripleMU_3324690130789734431(data);
}
bool
L1_TripleMu_5SQ_3SQ_0OQ_DoubleMu_5_3_SQ_OS_Mass_Max9(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return TripleMU_3324685732743223327(data) and InvariantMass_3063833799189854821(data);
}
bool
L1_TripleMu_5SQ_3SQ_0_DoubleMu_5_3_SQ_OS_Mass_Max9(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return TripleMU_3324685351042537503(data) and InvariantMass_3063833799189854821(data);
}
bool
L1_TripleMu_5_0_0(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return TripleMU_3324683539710430239(data);
}
bool
L1_TripleMu_5_3_3(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return TripleMU_3324691786047638559(data);
}
bool
L1_TripleMu_5_3p5_2p5(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return TripleMU_9287399899537551596(data);
}
bool
L1_TripleMu_5_3p5_2p5_DoubleMu_5_2p5_OS_Mass_5to17(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return TripleMU_9287399899537551596(data) and InvariantMass_15191958030943548804(data);
}
bool
L1_TripleMu_5_4_2p5_DoubleMu_5_2p5_OS_Mass_5to17(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return TripleMU_6936497366859389375(data) and InvariantMass_15191958030943548804(data);
}
bool
L1_TripleMu_5_5_3(L1Analysis::L1AnalysisL1UpgradeDataFormat* data, L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  return TripleMU_3324692885559266335(data);
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
          std::make_pair(465, "L1_AlwaysTrue"),          std::make_pair(477, "L1_BPTX_AND_Ref1_VME"),          std::make_pair(481, "L1_BPTX_AND_Ref3_VME"),          std::make_pair(485, "L1_BPTX_AND_Ref4_VME"),          std::make_pair(471, "L1_BPTX_BeamGas_B1_VME"),          std::make_pair(472, "L1_BPTX_BeamGas_B2_VME"),          std::make_pair(469, "L1_BPTX_BeamGas_Ref1_VME"),          std::make_pair(470, "L1_BPTX_BeamGas_Ref2_VME"),          std::make_pair(480, "L1_BPTX_NotOR_VME"),          std::make_pair(482, "L1_BPTX_OR_Ref3_VME"),          std::make_pair(486, "L1_BPTX_OR_Ref4_VME"),          std::make_pair(483, "L1_BPTX_RefAND_VME"),          std::make_pair(475, "L1_BptxMinus"),          std::make_pair(476, "L1_BptxOR"),          std::make_pair(474, "L1_BptxPlus"),          std::make_pair(467, "L1_BptxXOR"),          std::make_pair(504, "L1_CDC_SingleMu_3_er1p2_TOP120_DPHI2p618_3p142"),          std::make_pair(336, "L1_DoubleEG6_HTT240er"),          std::make_pair(337, "L1_DoubleEG6_HTT250er"),          std::make_pair(439, "L1_DoubleEG6_HTT255er"),          std::make_pair(338, "L1_DoubleEG6_HTT270er"),          std::make_pair(339, "L1_DoubleEG6_HTT300er"),          std::make_pair(340, "L1_DoubleEG8er2p6_HTT255er"),          std::make_pair(341, "L1_DoubleEG8er2p6_HTT270er"),          std::make_pair(342, "L1_DoubleEG8er2p6_HTT300er"),          std::make_pair(100, "L1_DoubleEG_15_10"),          std::make_pair(101, "L1_DoubleEG_18_17"),          std::make_pair(102, "L1_DoubleEG_20_18"),          std::make_pair(103, "L1_DoubleEG_22_10"),          std::make_pair(104, "L1_DoubleEG_22_12"),          std::make_pair(105, "L1_DoubleEG_22_15"),          std::make_pair(106, "L1_DoubleEG_23_10"),          std::make_pair(107, "L1_DoubleEG_24_17"),          std::make_pair(108, "L1_DoubleEG_25_12"),          std::make_pair(109, "L1_DoubleEG_25_13"),          std::make_pair(110, "L1_DoubleEG_25_14"),          std::make_pair(279, "L1_DoubleEG_LooseIso23_10"),          std::make_pair(280, "L1_DoubleEG_LooseIso24_10"),          std::make_pair(123, "L1_DoubleIsoTau28er2p1"),          std::make_pair(124, "L1_DoubleIsoTau30er2p1"),          std::make_pair(125, "L1_DoubleIsoTau32er2p1"),          std::make_pair(126, "L1_DoubleIsoTau33er2p1"),          std::make_pair(127, "L1_DoubleIsoTau34er2p1"),          std::make_pair(128, "L1_DoubleIsoTau35er2p1"),          std::make_pair(129, "L1_DoubleIsoTau36er2p1"),          std::make_pair(130, "L1_DoubleIsoTau38er2p1"),          std::make_pair(251, "L1_DoubleJet100er2p3_dEta_Max1p6"),          std::make_pair(155, "L1_DoubleJet100er2p7"),          std::make_pair(252, "L1_DoubleJet112er2p3_dEta_Max1p6"),          std::make_pair(156, "L1_DoubleJet112er2p7"),          std::make_pair(157, "L1_DoubleJet120er2p7"),          std::make_pair(158, "L1_DoubleJet150er2p7"),          std::make_pair(216, "L1_DoubleJet30_Mass_Min300_dEta_Max1p5"),          std::make_pair(217, "L1_DoubleJet30_Mass_Min320_dEta_Max1p5"),          std::make_pair(218, "L1_DoubleJet30_Mass_Min340_dEta_Max1p5"),          std::make_pair(219, "L1_DoubleJet30_Mass_Min360_dEta_Max1p5"),          std::make_pair(220, "L1_DoubleJet30_Mass_Min380_dEta_Max1p5"),          std::make_pair(290, "L1_DoubleJet30_Mass_Min400_Mu10"),          std::make_pair(289, "L1_DoubleJet30_Mass_Min400_Mu6"),          std::make_pair(221, "L1_DoubleJet30_Mass_Min400_dEta_Max1p5"),          std::make_pair(292, "L1_DoubleJet35_rmovlp_IsoTau45_Mass_Min450"),          std::make_pair(151, "L1_DoubleJet40er2p7"),          std::make_pair(152, "L1_DoubleJet50er2p7"),          std::make_pair(153, "L1_DoubleJet60er2p7"),          std::make_pair(278, "L1_DoubleJet60er2p7_ETM100"),          std::make_pair(429, "L1_DoubleJet60er2p7_ETM60"),          std::make_pair(275, "L1_DoubleJet60er2p7_ETM70"),          std::make_pair(276, "L1_DoubleJet60er2p7_ETM80"),          std::make_pair(277, "L1_DoubleJet60er2p7_ETM90"),          std::make_pair(154, "L1_DoubleJet80er2p7"),          std::make_pair(283, "L1_DoubleJet_100_30_DoubleJet30_Mass_Min620"),          std::make_pair(284, "L1_DoubleJet_100_35_DoubleJet35_Mass_Min620"),          std::make_pair(285, "L1_DoubleJet_110_35_DoubleJet35_Mass_Min620"),          std::make_pair(286, "L1_DoubleJet_110_40_DoubleJet40_Mass_Min620"),          std::make_pair(287, "L1_DoubleJet_115_35_DoubleJet35_Mass_Min620"),          std::make_pair(288, "L1_DoubleJet_115_40_DoubleJet40_Mass_Min620"),          std::make_pair(282, "L1_DoubleJet_90_30_DoubleJet30_Mass_Min620"),          std::make_pair(111, "L1_DoubleLooseIsoEG22er2p1"),          std::make_pair(112, "L1_DoubleLooseIsoEG24er2p1"),          std::make_pair(30, "L1_DoubleMu0"),          std::make_pair(432, "L1_DoubleMu0_ETM40"),          std::make_pair(433, "L1_DoubleMu0_ETM55"),          std::make_pair(434, "L1_DoubleMu0_ETM60"),          std::make_pair(435, "L1_DoubleMu0_ETM65"),          std::make_pair(436, "L1_DoubleMu0_ETM70"),          std::make_pair(390, "L1_DoubleMu0_SQ"),          std::make_pair(391, "L1_DoubleMu0_SQ_OS"),          std::make_pair(381, "L1_DoubleMu0er1p4_SQ_OS_dR_Max1p4"),          std::make_pair(440, "L1_DoubleMu0er1p4_dEta_Max1p8_OS"),          std::make_pair(395, "L1_DoubleMu0er1p5_SQ_OS"),          std::make_pair(375, "L1_DoubleMu0er1p5_SQ_OS_dR_Max1p4"),          std::make_pair(223, "L1_DoubleMu0er1p5_SQ_dR_Max1p4"),          std::make_pair(222, "L1_DoubleMu0er2_SQ_dR_Max1p4"),          std::make_pair(37, "L1_DoubleMu18er2p1"),          std::make_pair(38, "L1_DoubleMu22er2p1"),          std::make_pair(402, "L1_DoubleMu3_OS_DoubleEG7p5Upsilon"),          std::make_pair(323, "L1_DoubleMu3_SQ_ETMHF40_Jet60_OR_DoubleJet30"),          std::make_pair(324, "L1_DoubleMu3_SQ_ETMHF50_Jet60_OR_DoubleJet30"),          std::make_pair(325, "L1_DoubleMu3_SQ_ETMHF60_Jet60_OR_DoubleJet30"),          std::make_pair(326, "L1_DoubleMu3_SQ_ETMHF70_Jet60_OR_DoubleJet30"),          std::make_pair(327, "L1_DoubleMu3_SQ_ETMHF80_Jet60_OR_DoubleJet30"),          std::make_pair(328, "L1_DoubleMu3_SQ_HTT100er"),          std::make_pair(329, "L1_DoubleMu3_SQ_HTT200er"),          std::make_pair(330, "L1_DoubleMu3_SQ_HTT220er"),          std::make_pair(331, "L1_DoubleMu3_SQ_HTT240er"),          std::make_pair(380, "L1_DoubleMu4_OS_EG12"),          std::make_pair(396, "L1_DoubleMu4_SQ_OS"),          std::make_pair(377, "L1_DoubleMu4_SQ_OS_dR_Max1p2"),          std::make_pair(392, "L1_DoubleMu4p5_SQ"),          std::make_pair(393, "L1_DoubleMu4p5_SQ_OS"),          std::make_pair(382, "L1_DoubleMu4p5_SQ_OS_dR_Max1p2"),          std::make_pair(394, "L1_DoubleMu4p5er2p0_SQ_OS"),          std::make_pair(376, "L1_DoubleMu4p5er2p0_SQ_OS_Mass7to18"),          std::make_pair(401, "L1_DoubleMu5Upsilon_OS_DoubleEG3"),          std::make_pair(383, "L1_DoubleMu5_OS_EG12"),          std::make_pair(397, "L1_DoubleMu5_SQ_OS"),          std::make_pair(378, "L1_DoubleMu5_SQ_OS_Mass7to18"),          std::make_pair(384, "L1_DoubleMu6_SQ_OS"),          std::make_pair(406, "L1_DoubleMu7_EG7"),          std::make_pair(365, "L1_DoubleMu7_SQ_EG7"),          std::make_pair(389, "L1_DoubleMu8_SQ"),          std::make_pair(441, "L1_DoubleMu_10_0_dEta_Max1p8"),          std::make_pair(31, "L1_DoubleMu_11_4"),          std::make_pair(32, "L1_DoubleMu_12_5"),          std::make_pair(33, "L1_DoubleMu_12_8"),          std::make_pair(34, "L1_DoubleMu_13_6"),          std::make_pair(35, "L1_DoubleMu_15_5"),          std::make_pair(332, "L1_DoubleMu_15_5_SQ"),          std::make_pair(36, "L1_DoubleMu_15_7"),          std::make_pair(333, "L1_DoubleMu_15_7_SQ"),          std::make_pair(334, "L1_DoubleMu_15_7_SQ_Mass_Min4"),          std::make_pair(379, "L1_DoubleMu_20_2_SQ_Mass_Max20"),          std::make_pair(121, "L1_DoubleTau50er2p1"),          std::make_pair(122, "L1_DoubleTau70er2p1"),          std::make_pair(427, "L1_EG25er2p1_HTT125er"),          std::make_pair(428, "L1_EG27er2p1_HTT200er"),          std::make_pair(193, "L1_ETM100"),          std::make_pair(273, "L1_ETM100_Jet60_dPhi_Min0p4"),          std::make_pair(194, "L1_ETM105"),          std::make_pair(195, "L1_ETM110"),          std::make_pair(274, "L1_ETM110_Jet60_dPhi_Min0p4"),          std::make_pair(196, "L1_ETM115"),          std::make_pair(197, "L1_ETM120"),          std::make_pair(198, "L1_ETM150"),          std::make_pair(183, "L1_ETM30"),          std::make_pair(184, "L1_ETM40"),          std::make_pair(185, "L1_ETM50"),          std::make_pair(186, "L1_ETM60"),          std::make_pair(187, "L1_ETM70"),          std::make_pair(188, "L1_ETM75"),          std::make_pair(431, "L1_ETM75_Jet60_dPhi_Min0p4"),          std::make_pair(189, "L1_ETM80"),          std::make_pair(271, "L1_ETM80_Jet60_dPhi_Min0p4"),          std::make_pair(190, "L1_ETM85"),          std::make_pair(191, "L1_ETM90"),          std::make_pair(272, "L1_ETM90_Jet60_dPhi_Min0p4"),          std::make_pair(192, "L1_ETM95"),          std::make_pair(202, "L1_ETMHF100"),          std::make_pair(368, "L1_ETMHF100_HTT60er"),          std::make_pair(357, "L1_ETMHF100_Jet60_OR_DiJet30woTT28"),          std::make_pair(349, "L1_ETMHF100_Jet60_OR_DoubleJet30"),          std::make_pair(363, "L1_ETMHF100_Jet90_OR_DoubleJet45_OR_TripleJet30"),          std::make_pair(203, "L1_ETMHF110"),          std::make_pair(369, "L1_ETMHF110_HTT60er"),          std::make_pair(358, "L1_ETMHF110_Jet60_OR_DiJet30woTT28"),          std::make_pair(364, "L1_ETMHF110_Jet90_OR_DoubleJet45_OR_TripleJet30"),          std::make_pair(204, "L1_ETMHF120"),          std::make_pair(370, "L1_ETMHF120_HTT60er"),          std::make_pair(359, "L1_ETMHF120_Jet60_OR_DiJet30woTT28"),          std::make_pair(205, "L1_ETMHF150"),          std::make_pair(199, "L1_ETMHF70"),          std::make_pair(360, "L1_ETMHF70_Jet90_OR_DoubleJet45_OR_TripleJet30"),          std::make_pair(200, "L1_ETMHF80"),          std::make_pair(366, "L1_ETMHF80_HTT60er"),          std::make_pair(361, "L1_ETMHF80_Jet90_OR_DoubleJet45_OR_TripleJet30"),          std::make_pair(201, "L1_ETMHF90"),          std::make_pair(367, "L1_ETMHF90_HTT60er"),          std::make_pair(362, "L1_ETMHF90_Jet90_OR_DoubleJet45_OR_TripleJet30"),          std::make_pair(457, "L1_ETT100_BptxAND"),          std::make_pair(458, "L1_ETT110_BptxAND"),          std::make_pair(448, "L1_ETT40_BptxAND"),          std::make_pair(449, "L1_ETT50_BptxAND"),          std::make_pair(450, "L1_ETT60_BptxAND"),          std::make_pair(451, "L1_ETT70_BptxAND"),          std::make_pair(452, "L1_ETT75_BptxAND"),          std::make_pair(453, "L1_ETT80_BptxAND"),          std::make_pair(454, "L1_ETT85_BptxAND"),          std::make_pair(455, "L1_ETT90_BptxAND"),          std::make_pair(456, "L1_ETT95_BptxAND"),          std::make_pair(417, "L1_FirstBunchAfterTrain"),          std::make_pair(416, "L1_FirstBunchInTrain"),          std::make_pair(484, "L1_FirstCollisionInOrbit"),          std::make_pair(488, "L1_FirstCollisionInTrain"),          std::make_pair(168, "L1_HTT120er"),          std::make_pair(169, "L1_HTT160er"),          std::make_pair(170, "L1_HTT200er"),          std::make_pair(171, "L1_HTT220er"),          std::make_pair(172, "L1_HTT240er"),          std::make_pair(243, "L1_HTT250er_QuadJet_70_55_40_35_er2p5"),          std::make_pair(173, "L1_HTT255er"),          std::make_pair(174, "L1_HTT270er"),          std::make_pair(175, "L1_HTT280er"),          std::make_pair(244, "L1_HTT280er_QuadJet_70_55_40_35_er2p5"),          std::make_pair(176, "L1_HTT300er"),          std::make_pair(245, "L1_HTT300er_QuadJet_70_55_40_35_er2p5"),          std::make_pair(177, "L1_HTT320er"),          std::make_pair(246, "L1_HTT320er_QuadJet_70_55_40_40_er2p4"),          std::make_pair(247, "L1_HTT320er_QuadJet_70_55_40_40_er2p5"),          std::make_pair(249, "L1_HTT320er_QuadJet_70_55_45_45_er2p5"),          std::make_pair(178, "L1_HTT340er"),          std::make_pair(248, "L1_HTT340er_QuadJet_70_55_40_40_er2p5"),          std::make_pair(250, "L1_HTT340er_QuadJet_70_55_45_45_er2p5"),          std::make_pair(179, "L1_HTT380er"),          std::make_pair(180, "L1_HTT400er"),          std::make_pair(181, "L1_HTT450er"),          std::make_pair(182, "L1_HTT500er"),          std::make_pair(97, "L1_IsoEG33_Mt40"),          std::make_pair(98, "L1_IsoEG33_Mt44"),          std::make_pair(99, "L1_IsoEG33_Mt48"),          std::make_pair(259, "L1_IsoTau40er_ETM100"),          std::make_pair(260, "L1_IsoTau40er_ETM105"),          std::make_pair(261, "L1_IsoTau40er_ETM110"),          std::make_pair(262, "L1_IsoTau40er_ETM115"),          std::make_pair(263, "L1_IsoTau40er_ETM120"),          std::make_pair(255, "L1_IsoTau40er_ETM80"),          std::make_pair(256, "L1_IsoTau40er_ETM85"),          std::make_pair(257, "L1_IsoTau40er_ETM90"),          std::make_pair(258, "L1_IsoTau40er_ETM95"),          std::make_pair(266, "L1_IsoTau40er_ETMHF100"),          std::make_pair(267, "L1_IsoTau40er_ETMHF110"),          std::make_pair(268, "L1_IsoTau40er_ETMHF120"),          std::make_pair(264, "L1_IsoTau40er_ETMHF80"),          std::make_pair(265, "L1_IsoTau40er_ETMHF90"),          std::make_pair(415, "L1_IsolatedBunch"),          std::make_pair(487, "L1_LastCollisionInTrain"),          std::make_pair(294, "L1_LooseIsoEG22er2p1_IsoTau26er2p1_dR_Min0p3"),          std::make_pair(229, "L1_LooseIsoEG24er2p1_HTT100er"),          std::make_pair(295, "L1_LooseIsoEG24er2p1_IsoTau27er2p1_dR_Min0p3"),          std::make_pair(225, "L1_LooseIsoEG24er2p1_Jet26er2p7_dR_Min0p3"),          std::make_pair(232, "L1_LooseIsoEG24er2p1_TripleJet_26er2p7_26_26er2p7"),          std::make_pair(230, "L1_LooseIsoEG26er2p1_HTT100er"),          std::make_pair(226, "L1_LooseIsoEG26er2p1_Jet34er2p7_dR_Min0p3"),          std::make_pair(231, "L1_LooseIsoEG28er2p1_HTT100er"),          std::make_pair(227, "L1_LooseIsoEG28er2p1_Jet34er2p7_dR_Min0p3"),          std::make_pair(228, "L1_LooseIsoEG30er2p1_Jet34er2p7_dR_Min0p3"),          std::make_pair(423, "L1_MU20_EG15"),          std::make_pair(459, "L1_MinimumBiasHF0_AND_BptxAND"),          std::make_pair(460, "L1_MinimumBiasHF0_OR_BptxAND"),          std::make_pair(461, "L1_Mu10er2p1_ETM30"),          std::make_pair(253, "L1_Mu10er2p3_Jet32er2p3_dR_Max0p4_DoubleJet32er2p3_dEta_Max1p6"),          std::make_pair(421, "L1_Mu12_EG10"),          std::make_pair(254, "L1_Mu12er2p3_Jet40er2p3_dR_Max0p4_DoubleJet40er2p3_dEta_Max1p6"),          std::make_pair(462, "L1_Mu14er2p1_ETM30"),          std::make_pair(317, "L1_Mu15_HTT100er"),          std::make_pair(233, "L1_Mu18_HTT100er"),          std::make_pair(234, "L1_Mu18_Jet24er2p7"),          std::make_pair(302, "L1_Mu18er2p1_IsoTau26er2p1"),          std::make_pair(299, "L1_Mu18er2p1_Tau24er2p1"),          std::make_pair(422, "L1_Mu20_EG10"),          std::make_pair(235, "L1_Mu20_EG17"),          std::make_pair(424, "L1_Mu20_LooseIsoEG6"),          std::make_pair(303, "L1_Mu20er2p1_IsoTau26er2p1"),          std::make_pair(304, "L1_Mu20er2p1_IsoTau27er2p1"),          std::make_pair(305, "L1_Mu22er2p1_IsoTau28er2p1"),          std::make_pair(306, "L1_Mu22er2p1_IsoTau30er2p1"),          std::make_pair(307, "L1_Mu22er2p1_IsoTau32er2p1"),          std::make_pair(308, "L1_Mu22er2p1_IsoTau33er2p1"),          std::make_pair(309, "L1_Mu22er2p1_IsoTau34er2p1"),          std::make_pair(310, "L1_Mu22er2p1_IsoTau35er2p1"),          std::make_pair(311, "L1_Mu22er2p1_IsoTau36er2p1"),          std::make_pair(312, "L1_Mu22er2p1_IsoTau38er2p1"),          std::make_pair(269, "L1_Mu22er2p1_IsoTau40er2p1"),          std::make_pair(300, "L1_Mu22er2p1_Tau50er2p1"),          std::make_pair(301, "L1_Mu22er2p1_Tau70er2p1"),          std::make_pair(236, "L1_Mu23_EG10"),          std::make_pair(237, "L1_Mu23_LooseIsoEG10"),          std::make_pair(445, "L1_Mu3_Jet120er2p7_dEta_Max0p4_dPhi_Max0p4"),          std::make_pair(443, "L1_Mu3_Jet16er2p7_dEta_Max0p4_dPhi_Max0p4"),          std::make_pair(371, "L1_Mu3_Jet30er2p5"),          std::make_pair(444, "L1_Mu3_Jet60er2p7_dEta_Max0p4_dPhi_Max0p4"),          std::make_pair(418, "L1_Mu5_EG15"),          std::make_pair(419, "L1_Mu5_EG20"),          std::make_pair(238, "L1_Mu5_EG23"),          std::make_pair(420, "L1_Mu5_LooseIsoEG18"),          std::make_pair(239, "L1_Mu5_LooseIsoEG20"),          std::make_pair(442, "L1_Mu6_DoubleEG10"),          std::make_pair(405, "L1_Mu6_DoubleEG17"),          std::make_pair(425, "L1_Mu6_HTT200er"),          std::make_pair(315, "L1_Mu6_HTT240er"),          std::make_pair(316, "L1_Mu6_HTT250er"),          std::make_pair(240, "L1_Mu7_EG23"),          std::make_pair(241, "L1_Mu7_LooseIsoEG20"),          std::make_pair(242, "L1_Mu7_LooseIsoEG23"),          std::make_pair(426, "L1_Mu8_HTT150er"),          std::make_pair(466, "L1_NotBptxOR"),          std::make_pair(270, "L1_QuadJet36er2p7_IsoTau52er2p1"),          std::make_pair(430, "L1_QuadJet36er2p7_Tau52"),          std::make_pair(165, "L1_QuadJet40er2p7"),          std::make_pair(166, "L1_QuadJet50er2p7"),          std::make_pair(167, "L1_QuadJet60er2p7"),          std::make_pair(45, "L1_QuadMu0"),          std::make_pair(51, "L1_SingleEG10"),          std::make_pair(52, "L1_SingleEG15"),          std::make_pair(53, "L1_SingleEG18"),          std::make_pair(54, "L1_SingleEG24"),          std::make_pair(55, "L1_SingleEG26"),          std::make_pair(56, "L1_SingleEG28"),          std::make_pair(446, "L1_SingleEG2_BptxAND"),          std::make_pair(57, "L1_SingleEG30"),          std::make_pair(58, "L1_SingleEG32"),          std::make_pair(59, "L1_SingleEG34"),          std::make_pair(66, "L1_SingleEG34er2p1"),          std::make_pair(60, "L1_SingleEG36"),          std::make_pair(67, "L1_SingleEG36er2p1"),          std::make_pair(61, "L1_SingleEG38"),          std::make_pair(68, "L1_SingleEG38er2p1"),          std::make_pair(62, "L1_SingleEG40"),          std::make_pair(63, "L1_SingleEG42"),          std::make_pair(64, "L1_SingleEG45"),          std::make_pair(50, "L1_SingleEG5"),          std::make_pair(65, "L1_SingleEG50"),          std::make_pair(69, "L1_SingleIsoEG18"),          std::make_pair(83, "L1_SingleIsoEG18er2p1"),          std::make_pair(70, "L1_SingleIsoEG20"),          std::make_pair(84, "L1_SingleIsoEG20er2p1"),          std::make_pair(71, "L1_SingleIsoEG22"),          std::make_pair(85, "L1_SingleIsoEG22er2p1"),          std::make_pair(72, "L1_SingleIsoEG24"),          std::make_pair(86, "L1_SingleIsoEG24er2p1"),          std::make_pair(73, "L1_SingleIsoEG26"),          std::make_pair(87, "L1_SingleIsoEG26er2p1"),          std::make_pair(74, "L1_SingleIsoEG28"),          std::make_pair(88, "L1_SingleIsoEG28er2p1"),          std::make_pair(75, "L1_SingleIsoEG30"),          std::make_pair(89, "L1_SingleIsoEG30er2p1"),          std::make_pair(76, "L1_SingleIsoEG32"),          std::make_pair(90, "L1_SingleIsoEG32er2p1"),          std::make_pair(91, "L1_SingleIsoEG33er2p1"),          std::make_pair(77, "L1_SingleIsoEG34"),          std::make_pair(92, "L1_SingleIsoEG34er2p1"),          std::make_pair(78, "L1_SingleIsoEG35"),          std::make_pair(93, "L1_SingleIsoEG35er2p1"),          std::make_pair(79, "L1_SingleIsoEG36"),          std::make_pair(94, "L1_SingleIsoEG36er2p1"),          std::make_pair(80, "L1_SingleIsoEG37"),          std::make_pair(81, "L1_SingleIsoEG38"),          std::make_pair(95, "L1_SingleIsoEG38er2p1"),          std::make_pair(82, "L1_SingleIsoEG40"),          std::make_pair(96, "L1_SingleIsoEG40er2p1"),          std::make_pair(136, "L1_SingleJet120"),          std::make_pair(146, "L1_SingleJet120_FWD"),          std::make_pair(447, "L1_SingleJet12_BptxAND"),          std::make_pair(137, "L1_SingleJet140"),          std::make_pair(138, "L1_SingleJet150"),          std::make_pair(131, "L1_SingleJet16"),          std::make_pair(139, "L1_SingleJet160"),          std::make_pair(140, "L1_SingleJet170"),          std::make_pair(141, "L1_SingleJet180"),          std::make_pair(132, "L1_SingleJet20"),          std::make_pair(142, "L1_SingleJet200"),          std::make_pair(212, "L1_SingleJet20er2p7_NotBptxOR"),          std::make_pair(213, "L1_SingleJet20er2p7_NotBptxOR_3BX"),          std::make_pair(133, "L1_SingleJet35"),          std::make_pair(143, "L1_SingleJet35_FWD"),          std::make_pair(148, "L1_SingleJet35_HFm"),          std::make_pair(147, "L1_SingleJet35_HFp"),          std::make_pair(214, "L1_SingleJet43er2p7_NotBptxOR_3BX"),          std::make_pair(215, "L1_SingleJet46er2p7_NotBptxOR_3BX"),          std::make_pair(134, "L1_SingleJet60"),          std::make_pair(144, "L1_SingleJet60_FWD"),          std::make_pair(150, "L1_SingleJet60_HFm"),          std::make_pair(149, "L1_SingleJet60_HFp"),          std::make_pair(135, "L1_SingleJet90"),          std::make_pair(145, "L1_SingleJet90_FWD"),          std::make_pair(5, "L1_SingleMu0_BMTF"),          std::make_pair(7, "L1_SingleMu0_EMTF"),          std::make_pair(6, "L1_SingleMu0_OMTF"),          std::make_pair(11, "L1_SingleMu10_LowQ"),          std::make_pair(12, "L1_SingleMu11_LowQ"),          std::make_pair(13, "L1_SingleMu12_LowQ_BMTF"),          std::make_pair(15, "L1_SingleMu12_LowQ_EMTF"),          std::make_pair(14, "L1_SingleMu12_LowQ_OMTF"),          std::make_pair(25, "L1_SingleMu14er2p1"),          std::make_pair(16, "L1_SingleMu16"),          std::make_pair(26, "L1_SingleMu16er2p1"),          std::make_pair(17, "L1_SingleMu18"),          std::make_pair(27, "L1_SingleMu18er2p1"),          std::make_pair(18, "L1_SingleMu20"),          std::make_pair(28, "L1_SingleMu20er2p1"),          std::make_pair(19, "L1_SingleMu22"),          std::make_pair(20, "L1_SingleMu22_BMTF"),          std::make_pair(22, "L1_SingleMu22_EMTF"),          std::make_pair(21, "L1_SingleMu22_OMTF"),          std::make_pair(29, "L1_SingleMu22er2p1"),          std::make_pair(23, "L1_SingleMu25"),          std::make_pair(8, "L1_SingleMu3"),          std::make_pair(24, "L1_SingleMu30"),          std::make_pair(511, "L1_SingleMu3er1p5_SingleJet100er2p5_ETMHF40"),          std::make_pair(9, "L1_SingleMu5"),          std::make_pair(10, "L1_SingleMu7"),          std::make_pair(0, "L1_SingleMuCosmics"),          std::make_pair(2, "L1_SingleMuCosmics_BMTF"),          std::make_pair(4, "L1_SingleMuCosmics_EMTF"),          std::make_pair(3, "L1_SingleMuCosmics_OMTF"),          std::make_pair(1, "L1_SingleMuOpen"),          std::make_pair(210, "L1_SingleMuOpen_NotBptxOR"),          std::make_pair(211, "L1_SingleMuOpen_NotBptxOR_3BX"),          std::make_pair(117, "L1_SingleTau100er2p1"),          std::make_pair(118, "L1_SingleTau120er2p1"),          std::make_pair(119, "L1_SingleTau130er2p1"),          std::make_pair(120, "L1_SingleTau140er2p1"),          std::make_pair(115, "L1_SingleTau20"),          std::make_pair(116, "L1_SingleTau80er2p1"),          std::make_pair(113, "L1_TripleEG_14_10_8"),          std::make_pair(114, "L1_TripleEG_18_17_8"),          std::make_pair(281, "L1_TripleEG_LooseIso20_10_5"),          std::make_pair(164, "L1_TripleJet_100_85_72_VBF"),          std::make_pair(163, "L1_TripleJet_105_85_76_VBF"),          std::make_pair(159, "L1_TripleJet_84_68_48_VBF"),          std::make_pair(160, "L1_TripleJet_88_72_56_VBF"),          std::make_pair(161, "L1_TripleJet_92_76_64_VBF"),          std::make_pair(162, "L1_TripleJet_98_83_71_VBF"),          std::make_pair(39, "L1_TripleMu0"),          std::make_pair(399, "L1_TripleMu0_OQ"),          std::make_pair(40, "L1_TripleMu3"),          std::make_pair(335, "L1_TripleMu3_SQ"),          std::make_pair(41, "L1_TripleMu_4_4_4"),          std::make_pair(404, "L1_TripleMu_5OQ_3p5OQ_2p5OQ_DoubleMu_5_2p5_OQ_OS_Mass_5to17"),          std::make_pair(403, "L1_TripleMu_5OQ_3p5OQ_2p5OQ_DoubleMu_5_2p5_OQ_OS_Mass_8to14"),          std::make_pair(400, "L1_TripleMu_5SQ_3SQ_0OQ"),          std::make_pair(387, "L1_TripleMu_5SQ_3SQ_0OQ_DoubleMu_5_3_SQ_OS_Mass_Max9"),          std::make_pair(388, "L1_TripleMu_5SQ_3SQ_0_DoubleMu_5_3_SQ_OS_Mass_Max9"),          std::make_pair(42, "L1_TripleMu_5_0_0"),          std::make_pair(43, "L1_TripleMu_5_3_3"),          std::make_pair(398, "L1_TripleMu_5_3p5_2p5"),          std::make_pair(385, "L1_TripleMu_5_3p5_2p5_DoubleMu_5_2p5_OS_Mass_5to17"),          std::make_pair(386, "L1_TripleMu_5_4_2p5_DoubleMu_5_2p5_OS_Mass_5to17"),          std::make_pair(44, "L1_TripleMu_5_5_3"),          std::make_pair(479, "L1_UnpairedBunchBptxMinus"),          std::make_pair(478, "L1_UnpairedBunchBptxPlus"),          std::make_pair(473, "L1_ZeroBias"),          std::make_pair(468, "L1_ZeroBias_copy")      };

  static const std::map<int, std::string> Id2Name(id2name, id2name + sizeof(id2name) / sizeof(id2name[0]));
  const std::map<int, std::string>::const_iterator rc = Id2Name.find(index);
  std::string name;
  if (rc != Id2Name.end()) name = rc->second;
  return name;
}


int getIdFromName(const std::string& name)
{
  static const std::pair<std::string, int> name2id[] = {
          std::make_pair("L1_AlwaysTrue", 465),          std::make_pair("L1_BPTX_AND_Ref1_VME", 477),          std::make_pair("L1_BPTX_AND_Ref3_VME", 481),          std::make_pair("L1_BPTX_AND_Ref4_VME", 485),          std::make_pair("L1_BPTX_BeamGas_B1_VME", 471),          std::make_pair("L1_BPTX_BeamGas_B2_VME", 472),          std::make_pair("L1_BPTX_BeamGas_Ref1_VME", 469),          std::make_pair("L1_BPTX_BeamGas_Ref2_VME", 470),          std::make_pair("L1_BPTX_NotOR_VME", 480),          std::make_pair("L1_BPTX_OR_Ref3_VME", 482),          std::make_pair("L1_BPTX_OR_Ref4_VME", 486),          std::make_pair("L1_BPTX_RefAND_VME", 483),          std::make_pair("L1_BptxMinus", 475),          std::make_pair("L1_BptxOR", 476),          std::make_pair("L1_BptxPlus", 474),          std::make_pair("L1_BptxXOR", 467),          std::make_pair("L1_CDC_SingleMu_3_er1p2_TOP120_DPHI2p618_3p142", 504),          std::make_pair("L1_DoubleEG6_HTT240er", 336),          std::make_pair("L1_DoubleEG6_HTT250er", 337),          std::make_pair("L1_DoubleEG6_HTT255er", 439),          std::make_pair("L1_DoubleEG6_HTT270er", 338),          std::make_pair("L1_DoubleEG6_HTT300er", 339),          std::make_pair("L1_DoubleEG8er2p6_HTT255er", 340),          std::make_pair("L1_DoubleEG8er2p6_HTT270er", 341),          std::make_pair("L1_DoubleEG8er2p6_HTT300er", 342),          std::make_pair("L1_DoubleEG_15_10", 100),          std::make_pair("L1_DoubleEG_18_17", 101),          std::make_pair("L1_DoubleEG_20_18", 102),          std::make_pair("L1_DoubleEG_22_10", 103),          std::make_pair("L1_DoubleEG_22_12", 104),          std::make_pair("L1_DoubleEG_22_15", 105),          std::make_pair("L1_DoubleEG_23_10", 106),          std::make_pair("L1_DoubleEG_24_17", 107),          std::make_pair("L1_DoubleEG_25_12", 108),          std::make_pair("L1_DoubleEG_25_13", 109),          std::make_pair("L1_DoubleEG_25_14", 110),          std::make_pair("L1_DoubleEG_LooseIso23_10", 279),          std::make_pair("L1_DoubleEG_LooseIso24_10", 280),          std::make_pair("L1_DoubleIsoTau28er2p1", 123),          std::make_pair("L1_DoubleIsoTau30er2p1", 124),          std::make_pair("L1_DoubleIsoTau32er2p1", 125),          std::make_pair("L1_DoubleIsoTau33er2p1", 126),          std::make_pair("L1_DoubleIsoTau34er2p1", 127),          std::make_pair("L1_DoubleIsoTau35er2p1", 128),          std::make_pair("L1_DoubleIsoTau36er2p1", 129),          std::make_pair("L1_DoubleIsoTau38er2p1", 130),          std::make_pair("L1_DoubleJet100er2p3_dEta_Max1p6", 251),          std::make_pair("L1_DoubleJet100er2p7", 155),          std::make_pair("L1_DoubleJet112er2p3_dEta_Max1p6", 252),          std::make_pair("L1_DoubleJet112er2p7", 156),          std::make_pair("L1_DoubleJet120er2p7", 157),          std::make_pair("L1_DoubleJet150er2p7", 158),          std::make_pair("L1_DoubleJet30_Mass_Min300_dEta_Max1p5", 216),          std::make_pair("L1_DoubleJet30_Mass_Min320_dEta_Max1p5", 217),          std::make_pair("L1_DoubleJet30_Mass_Min340_dEta_Max1p5", 218),          std::make_pair("L1_DoubleJet30_Mass_Min360_dEta_Max1p5", 219),          std::make_pair("L1_DoubleJet30_Mass_Min380_dEta_Max1p5", 220),          std::make_pair("L1_DoubleJet30_Mass_Min400_Mu10", 290),          std::make_pair("L1_DoubleJet30_Mass_Min400_Mu6", 289),          std::make_pair("L1_DoubleJet30_Mass_Min400_dEta_Max1p5", 221),          std::make_pair("L1_DoubleJet35_rmovlp_IsoTau45_Mass_Min450", 292),          std::make_pair("L1_DoubleJet40er2p7", 151),          std::make_pair("L1_DoubleJet50er2p7", 152),          std::make_pair("L1_DoubleJet60er2p7", 153),          std::make_pair("L1_DoubleJet60er2p7_ETM100", 278),          std::make_pair("L1_DoubleJet60er2p7_ETM60", 429),          std::make_pair("L1_DoubleJet60er2p7_ETM70", 275),          std::make_pair("L1_DoubleJet60er2p7_ETM80", 276),          std::make_pair("L1_DoubleJet60er2p7_ETM90", 277),          std::make_pair("L1_DoubleJet80er2p7", 154),          std::make_pair("L1_DoubleJet_100_30_DoubleJet30_Mass_Min620", 283),          std::make_pair("L1_DoubleJet_100_35_DoubleJet35_Mass_Min620", 284),          std::make_pair("L1_DoubleJet_110_35_DoubleJet35_Mass_Min620", 285),          std::make_pair("L1_DoubleJet_110_40_DoubleJet40_Mass_Min620", 286),          std::make_pair("L1_DoubleJet_115_35_DoubleJet35_Mass_Min620", 287),          std::make_pair("L1_DoubleJet_115_40_DoubleJet40_Mass_Min620", 288),          std::make_pair("L1_DoubleJet_90_30_DoubleJet30_Mass_Min620", 282),          std::make_pair("L1_DoubleLooseIsoEG22er2p1", 111),          std::make_pair("L1_DoubleLooseIsoEG24er2p1", 112),          std::make_pair("L1_DoubleMu0", 30),          std::make_pair("L1_DoubleMu0_ETM40", 432),          std::make_pair("L1_DoubleMu0_ETM55", 433),          std::make_pair("L1_DoubleMu0_ETM60", 434),          std::make_pair("L1_DoubleMu0_ETM65", 435),          std::make_pair("L1_DoubleMu0_ETM70", 436),          std::make_pair("L1_DoubleMu0_SQ", 390),          std::make_pair("L1_DoubleMu0_SQ_OS", 391),          std::make_pair("L1_DoubleMu0er1p4_SQ_OS_dR_Max1p4", 381),          std::make_pair("L1_DoubleMu0er1p4_dEta_Max1p8_OS", 440),          std::make_pair("L1_DoubleMu0er1p5_SQ_OS", 395),          std::make_pair("L1_DoubleMu0er1p5_SQ_OS_dR_Max1p4", 375),          std::make_pair("L1_DoubleMu0er1p5_SQ_dR_Max1p4", 223),          std::make_pair("L1_DoubleMu0er2_SQ_dR_Max1p4", 222),          std::make_pair("L1_DoubleMu18er2p1", 37),          std::make_pair("L1_DoubleMu22er2p1", 38),          std::make_pair("L1_DoubleMu3_OS_DoubleEG7p5Upsilon", 402),          std::make_pair("L1_DoubleMu3_SQ_ETMHF40_Jet60_OR_DoubleJet30", 323),          std::make_pair("L1_DoubleMu3_SQ_ETMHF50_Jet60_OR_DoubleJet30", 324),          std::make_pair("L1_DoubleMu3_SQ_ETMHF60_Jet60_OR_DoubleJet30", 325),          std::make_pair("L1_DoubleMu3_SQ_ETMHF70_Jet60_OR_DoubleJet30", 326),          std::make_pair("L1_DoubleMu3_SQ_ETMHF80_Jet60_OR_DoubleJet30", 327),          std::make_pair("L1_DoubleMu3_SQ_HTT100er", 328),          std::make_pair("L1_DoubleMu3_SQ_HTT200er", 329),          std::make_pair("L1_DoubleMu3_SQ_HTT220er", 330),          std::make_pair("L1_DoubleMu3_SQ_HTT240er", 331),          std::make_pair("L1_DoubleMu4_OS_EG12", 380),          std::make_pair("L1_DoubleMu4_SQ_OS", 396),          std::make_pair("L1_DoubleMu4_SQ_OS_dR_Max1p2", 377),          std::make_pair("L1_DoubleMu4p5_SQ", 392),          std::make_pair("L1_DoubleMu4p5_SQ_OS", 393),          std::make_pair("L1_DoubleMu4p5_SQ_OS_dR_Max1p2", 382),          std::make_pair("L1_DoubleMu4p5er2p0_SQ_OS", 394),          std::make_pair("L1_DoubleMu4p5er2p0_SQ_OS_Mass7to18", 376),          std::make_pair("L1_DoubleMu5Upsilon_OS_DoubleEG3", 401),          std::make_pair("L1_DoubleMu5_OS_EG12", 383),          std::make_pair("L1_DoubleMu5_SQ_OS", 397),          std::make_pair("L1_DoubleMu5_SQ_OS_Mass7to18", 378),          std::make_pair("L1_DoubleMu6_SQ_OS", 384),          std::make_pair("L1_DoubleMu7_EG7", 406),          std::make_pair("L1_DoubleMu7_SQ_EG7", 365),          std::make_pair("L1_DoubleMu8_SQ", 389),          std::make_pair("L1_DoubleMu_10_0_dEta_Max1p8", 441),          std::make_pair("L1_DoubleMu_11_4", 31),          std::make_pair("L1_DoubleMu_12_5", 32),          std::make_pair("L1_DoubleMu_12_8", 33),          std::make_pair("L1_DoubleMu_13_6", 34),          std::make_pair("L1_DoubleMu_15_5", 35),          std::make_pair("L1_DoubleMu_15_5_SQ", 332),          std::make_pair("L1_DoubleMu_15_7", 36),          std::make_pair("L1_DoubleMu_15_7_SQ", 333),          std::make_pair("L1_DoubleMu_15_7_SQ_Mass_Min4", 334),          std::make_pair("L1_DoubleMu_20_2_SQ_Mass_Max20", 379),          std::make_pair("L1_DoubleTau50er2p1", 121),          std::make_pair("L1_DoubleTau70er2p1", 122),          std::make_pair("L1_EG25er2p1_HTT125er", 427),          std::make_pair("L1_EG27er2p1_HTT200er", 428),          std::make_pair("L1_ETM100", 193),          std::make_pair("L1_ETM100_Jet60_dPhi_Min0p4", 273),          std::make_pair("L1_ETM105", 194),          std::make_pair("L1_ETM110", 195),          std::make_pair("L1_ETM110_Jet60_dPhi_Min0p4", 274),          std::make_pair("L1_ETM115", 196),          std::make_pair("L1_ETM120", 197),          std::make_pair("L1_ETM150", 198),          std::make_pair("L1_ETM30", 183),          std::make_pair("L1_ETM40", 184),          std::make_pair("L1_ETM50", 185),          std::make_pair("L1_ETM60", 186),          std::make_pair("L1_ETM70", 187),          std::make_pair("L1_ETM75", 188),          std::make_pair("L1_ETM75_Jet60_dPhi_Min0p4", 431),          std::make_pair("L1_ETM80", 189),          std::make_pair("L1_ETM80_Jet60_dPhi_Min0p4", 271),          std::make_pair("L1_ETM85", 190),          std::make_pair("L1_ETM90", 191),          std::make_pair("L1_ETM90_Jet60_dPhi_Min0p4", 272),          std::make_pair("L1_ETM95", 192),          std::make_pair("L1_ETMHF100", 202),          std::make_pair("L1_ETMHF100_HTT60er", 368),          std::make_pair("L1_ETMHF100_Jet60_OR_DiJet30woTT28", 357),          std::make_pair("L1_ETMHF100_Jet60_OR_DoubleJet30", 349),          std::make_pair("L1_ETMHF100_Jet90_OR_DoubleJet45_OR_TripleJet30", 363),          std::make_pair("L1_ETMHF110", 203),          std::make_pair("L1_ETMHF110_HTT60er", 369),          std::make_pair("L1_ETMHF110_Jet60_OR_DiJet30woTT28", 358),          std::make_pair("L1_ETMHF110_Jet90_OR_DoubleJet45_OR_TripleJet30", 364),          std::make_pair("L1_ETMHF120", 204),          std::make_pair("L1_ETMHF120_HTT60er", 370),          std::make_pair("L1_ETMHF120_Jet60_OR_DiJet30woTT28", 359),          std::make_pair("L1_ETMHF150", 205),          std::make_pair("L1_ETMHF70", 199),          std::make_pair("L1_ETMHF70_Jet90_OR_DoubleJet45_OR_TripleJet30", 360),          std::make_pair("L1_ETMHF80", 200),          std::make_pair("L1_ETMHF80_HTT60er", 366),          std::make_pair("L1_ETMHF80_Jet90_OR_DoubleJet45_OR_TripleJet30", 361),          std::make_pair("L1_ETMHF90", 201),          std::make_pair("L1_ETMHF90_HTT60er", 367),          std::make_pair("L1_ETMHF90_Jet90_OR_DoubleJet45_OR_TripleJet30", 362),          std::make_pair("L1_ETT100_BptxAND", 457),          std::make_pair("L1_ETT110_BptxAND", 458),          std::make_pair("L1_ETT40_BptxAND", 448),          std::make_pair("L1_ETT50_BptxAND", 449),          std::make_pair("L1_ETT60_BptxAND", 450),          std::make_pair("L1_ETT70_BptxAND", 451),          std::make_pair("L1_ETT75_BptxAND", 452),          std::make_pair("L1_ETT80_BptxAND", 453),          std::make_pair("L1_ETT85_BptxAND", 454),          std::make_pair("L1_ETT90_BptxAND", 455),          std::make_pair("L1_ETT95_BptxAND", 456),          std::make_pair("L1_FirstBunchAfterTrain", 417),          std::make_pair("L1_FirstBunchInTrain", 416),          std::make_pair("L1_FirstCollisionInOrbit", 484),          std::make_pair("L1_FirstCollisionInTrain", 488),          std::make_pair("L1_HTT120er", 168),          std::make_pair("L1_HTT160er", 169),          std::make_pair("L1_HTT200er", 170),          std::make_pair("L1_HTT220er", 171),          std::make_pair("L1_HTT240er", 172),          std::make_pair("L1_HTT250er_QuadJet_70_55_40_35_er2p5", 243),          std::make_pair("L1_HTT255er", 173),          std::make_pair("L1_HTT270er", 174),          std::make_pair("L1_HTT280er", 175),          std::make_pair("L1_HTT280er_QuadJet_70_55_40_35_er2p5", 244),          std::make_pair("L1_HTT300er", 176),          std::make_pair("L1_HTT300er_QuadJet_70_55_40_35_er2p5", 245),          std::make_pair("L1_HTT320er", 177),          std::make_pair("L1_HTT320er_QuadJet_70_55_40_40_er2p4", 246),          std::make_pair("L1_HTT320er_QuadJet_70_55_40_40_er2p5", 247),          std::make_pair("L1_HTT320er_QuadJet_70_55_45_45_er2p5", 249),          std::make_pair("L1_HTT340er", 178),          std::make_pair("L1_HTT340er_QuadJet_70_55_40_40_er2p5", 248),          std::make_pair("L1_HTT340er_QuadJet_70_55_45_45_er2p5", 250),          std::make_pair("L1_HTT380er", 179),          std::make_pair("L1_HTT400er", 180),          std::make_pair("L1_HTT450er", 181),          std::make_pair("L1_HTT500er", 182),          std::make_pair("L1_IsoEG33_Mt40", 97),          std::make_pair("L1_IsoEG33_Mt44", 98),          std::make_pair("L1_IsoEG33_Mt48", 99),          std::make_pair("L1_IsoTau40er_ETM100", 259),          std::make_pair("L1_IsoTau40er_ETM105", 260),          std::make_pair("L1_IsoTau40er_ETM110", 261),          std::make_pair("L1_IsoTau40er_ETM115", 262),          std::make_pair("L1_IsoTau40er_ETM120", 263),          std::make_pair("L1_IsoTau40er_ETM80", 255),          std::make_pair("L1_IsoTau40er_ETM85", 256),          std::make_pair("L1_IsoTau40er_ETM90", 257),          std::make_pair("L1_IsoTau40er_ETM95", 258),          std::make_pair("L1_IsoTau40er_ETMHF100", 266),          std::make_pair("L1_IsoTau40er_ETMHF110", 267),          std::make_pair("L1_IsoTau40er_ETMHF120", 268),          std::make_pair("L1_IsoTau40er_ETMHF80", 264),          std::make_pair("L1_IsoTau40er_ETMHF90", 265),          std::make_pair("L1_IsolatedBunch", 415),          std::make_pair("L1_LastCollisionInTrain", 487),          std::make_pair("L1_LooseIsoEG22er2p1_IsoTau26er2p1_dR_Min0p3", 294),          std::make_pair("L1_LooseIsoEG24er2p1_HTT100er", 229),          std::make_pair("L1_LooseIsoEG24er2p1_IsoTau27er2p1_dR_Min0p3", 295),          std::make_pair("L1_LooseIsoEG24er2p1_Jet26er2p7_dR_Min0p3", 225),          std::make_pair("L1_LooseIsoEG24er2p1_TripleJet_26er2p7_26_26er2p7", 232),          std::make_pair("L1_LooseIsoEG26er2p1_HTT100er", 230),          std::make_pair("L1_LooseIsoEG26er2p1_Jet34er2p7_dR_Min0p3", 226),          std::make_pair("L1_LooseIsoEG28er2p1_HTT100er", 231),          std::make_pair("L1_LooseIsoEG28er2p1_Jet34er2p7_dR_Min0p3", 227),          std::make_pair("L1_LooseIsoEG30er2p1_Jet34er2p7_dR_Min0p3", 228),          std::make_pair("L1_MU20_EG15", 423),          std::make_pair("L1_MinimumBiasHF0_AND_BptxAND", 459),          std::make_pair("L1_MinimumBiasHF0_OR_BptxAND", 460),          std::make_pair("L1_Mu10er2p1_ETM30", 461),          std::make_pair("L1_Mu10er2p3_Jet32er2p3_dR_Max0p4_DoubleJet32er2p3_dEta_Max1p6", 253),          std::make_pair("L1_Mu12_EG10", 421),          std::make_pair("L1_Mu12er2p3_Jet40er2p3_dR_Max0p4_DoubleJet40er2p3_dEta_Max1p6", 254),          std::make_pair("L1_Mu14er2p1_ETM30", 462),          std::make_pair("L1_Mu15_HTT100er", 317),          std::make_pair("L1_Mu18_HTT100er", 233),          std::make_pair("L1_Mu18_Jet24er2p7", 234),          std::make_pair("L1_Mu18er2p1_IsoTau26er2p1", 302),          std::make_pair("L1_Mu18er2p1_Tau24er2p1", 299),          std::make_pair("L1_Mu20_EG10", 422),          std::make_pair("L1_Mu20_EG17", 235),          std::make_pair("L1_Mu20_LooseIsoEG6", 424),          std::make_pair("L1_Mu20er2p1_IsoTau26er2p1", 303),          std::make_pair("L1_Mu20er2p1_IsoTau27er2p1", 304),          std::make_pair("L1_Mu22er2p1_IsoTau28er2p1", 305),          std::make_pair("L1_Mu22er2p1_IsoTau30er2p1", 306),          std::make_pair("L1_Mu22er2p1_IsoTau32er2p1", 307),          std::make_pair("L1_Mu22er2p1_IsoTau33er2p1", 308),          std::make_pair("L1_Mu22er2p1_IsoTau34er2p1", 309),          std::make_pair("L1_Mu22er2p1_IsoTau35er2p1", 310),          std::make_pair("L1_Mu22er2p1_IsoTau36er2p1", 311),          std::make_pair("L1_Mu22er2p1_IsoTau38er2p1", 312),          std::make_pair("L1_Mu22er2p1_IsoTau40er2p1", 269),          std::make_pair("L1_Mu22er2p1_Tau50er2p1", 300),          std::make_pair("L1_Mu22er2p1_Tau70er2p1", 301),          std::make_pair("L1_Mu23_EG10", 236),          std::make_pair("L1_Mu23_LooseIsoEG10", 237),          std::make_pair("L1_Mu3_Jet120er2p7_dEta_Max0p4_dPhi_Max0p4", 445),          std::make_pair("L1_Mu3_Jet16er2p7_dEta_Max0p4_dPhi_Max0p4", 443),          std::make_pair("L1_Mu3_Jet30er2p5", 371),          std::make_pair("L1_Mu3_Jet60er2p7_dEta_Max0p4_dPhi_Max0p4", 444),          std::make_pair("L1_Mu5_EG15", 418),          std::make_pair("L1_Mu5_EG20", 419),          std::make_pair("L1_Mu5_EG23", 238),          std::make_pair("L1_Mu5_LooseIsoEG18", 420),          std::make_pair("L1_Mu5_LooseIsoEG20", 239),          std::make_pair("L1_Mu6_DoubleEG10", 442),          std::make_pair("L1_Mu6_DoubleEG17", 405),          std::make_pair("L1_Mu6_HTT200er", 425),          std::make_pair("L1_Mu6_HTT240er", 315),          std::make_pair("L1_Mu6_HTT250er", 316),          std::make_pair("L1_Mu7_EG23", 240),          std::make_pair("L1_Mu7_LooseIsoEG20", 241),          std::make_pair("L1_Mu7_LooseIsoEG23", 242),          std::make_pair("L1_Mu8_HTT150er", 426),          std::make_pair("L1_NotBptxOR", 466),          std::make_pair("L1_QuadJet36er2p7_IsoTau52er2p1", 270),          std::make_pair("L1_QuadJet36er2p7_Tau52", 430),          std::make_pair("L1_QuadJet40er2p7", 165),          std::make_pair("L1_QuadJet50er2p7", 166),          std::make_pair("L1_QuadJet60er2p7", 167),          std::make_pair("L1_QuadMu0", 45),          std::make_pair("L1_SingleEG10", 51),          std::make_pair("L1_SingleEG15", 52),          std::make_pair("L1_SingleEG18", 53),          std::make_pair("L1_SingleEG24", 54),          std::make_pair("L1_SingleEG26", 55),          std::make_pair("L1_SingleEG28", 56),          std::make_pair("L1_SingleEG2_BptxAND", 446),          std::make_pair("L1_SingleEG30", 57),          std::make_pair("L1_SingleEG32", 58),          std::make_pair("L1_SingleEG34", 59),          std::make_pair("L1_SingleEG34er2p1", 66),          std::make_pair("L1_SingleEG36", 60),          std::make_pair("L1_SingleEG36er2p1", 67),          std::make_pair("L1_SingleEG38", 61),          std::make_pair("L1_SingleEG38er2p1", 68),          std::make_pair("L1_SingleEG40", 62),          std::make_pair("L1_SingleEG42", 63),          std::make_pair("L1_SingleEG45", 64),          std::make_pair("L1_SingleEG5", 50),          std::make_pair("L1_SingleEG50", 65),          std::make_pair("L1_SingleIsoEG18", 69),          std::make_pair("L1_SingleIsoEG18er2p1", 83),          std::make_pair("L1_SingleIsoEG20", 70),          std::make_pair("L1_SingleIsoEG20er2p1", 84),          std::make_pair("L1_SingleIsoEG22", 71),          std::make_pair("L1_SingleIsoEG22er2p1", 85),          std::make_pair("L1_SingleIsoEG24", 72),          std::make_pair("L1_SingleIsoEG24er2p1", 86),          std::make_pair("L1_SingleIsoEG26", 73),          std::make_pair("L1_SingleIsoEG26er2p1", 87),          std::make_pair("L1_SingleIsoEG28", 74),          std::make_pair("L1_SingleIsoEG28er2p1", 88),          std::make_pair("L1_SingleIsoEG30", 75),          std::make_pair("L1_SingleIsoEG30er2p1", 89),          std::make_pair("L1_SingleIsoEG32", 76),          std::make_pair("L1_SingleIsoEG32er2p1", 90),          std::make_pair("L1_SingleIsoEG33er2p1", 91),          std::make_pair("L1_SingleIsoEG34", 77),          std::make_pair("L1_SingleIsoEG34er2p1", 92),          std::make_pair("L1_SingleIsoEG35", 78),          std::make_pair("L1_SingleIsoEG35er2p1", 93),          std::make_pair("L1_SingleIsoEG36", 79),          std::make_pair("L1_SingleIsoEG36er2p1", 94),          std::make_pair("L1_SingleIsoEG37", 80),          std::make_pair("L1_SingleIsoEG38", 81),          std::make_pair("L1_SingleIsoEG38er2p1", 95),          std::make_pair("L1_SingleIsoEG40", 82),          std::make_pair("L1_SingleIsoEG40er2p1", 96),          std::make_pair("L1_SingleJet120", 136),          std::make_pair("L1_SingleJet120_FWD", 146),          std::make_pair("L1_SingleJet12_BptxAND", 447),          std::make_pair("L1_SingleJet140", 137),          std::make_pair("L1_SingleJet150", 138),          std::make_pair("L1_SingleJet16", 131),          std::make_pair("L1_SingleJet160", 139),          std::make_pair("L1_SingleJet170", 140),          std::make_pair("L1_SingleJet180", 141),          std::make_pair("L1_SingleJet20", 132),          std::make_pair("L1_SingleJet200", 142),          std::make_pair("L1_SingleJet20er2p7_NotBptxOR", 212),          std::make_pair("L1_SingleJet20er2p7_NotBptxOR_3BX", 213),          std::make_pair("L1_SingleJet35", 133),          std::make_pair("L1_SingleJet35_FWD", 143),          std::make_pair("L1_SingleJet35_HFm", 148),          std::make_pair("L1_SingleJet35_HFp", 147),          std::make_pair("L1_SingleJet43er2p7_NotBptxOR_3BX", 214),          std::make_pair("L1_SingleJet46er2p7_NotBptxOR_3BX", 215),          std::make_pair("L1_SingleJet60", 134),          std::make_pair("L1_SingleJet60_FWD", 144),          std::make_pair("L1_SingleJet60_HFm", 150),          std::make_pair("L1_SingleJet60_HFp", 149),          std::make_pair("L1_SingleJet90", 135),          std::make_pair("L1_SingleJet90_FWD", 145),          std::make_pair("L1_SingleMu0_BMTF", 5),          std::make_pair("L1_SingleMu0_EMTF", 7),          std::make_pair("L1_SingleMu0_OMTF", 6),          std::make_pair("L1_SingleMu10_LowQ", 11),          std::make_pair("L1_SingleMu11_LowQ", 12),          std::make_pair("L1_SingleMu12_LowQ_BMTF", 13),          std::make_pair("L1_SingleMu12_LowQ_EMTF", 15),          std::make_pair("L1_SingleMu12_LowQ_OMTF", 14),          std::make_pair("L1_SingleMu14er2p1", 25),          std::make_pair("L1_SingleMu16", 16),          std::make_pair("L1_SingleMu16er2p1", 26),          std::make_pair("L1_SingleMu18", 17),          std::make_pair("L1_SingleMu18er2p1", 27),          std::make_pair("L1_SingleMu20", 18),          std::make_pair("L1_SingleMu20er2p1", 28),          std::make_pair("L1_SingleMu22", 19),          std::make_pair("L1_SingleMu22_BMTF", 20),          std::make_pair("L1_SingleMu22_EMTF", 22),          std::make_pair("L1_SingleMu22_OMTF", 21),          std::make_pair("L1_SingleMu22er2p1", 29),          std::make_pair("L1_SingleMu25", 23),          std::make_pair("L1_SingleMu3", 8),          std::make_pair("L1_SingleMu30", 24),          std::make_pair("L1_SingleMu3er1p5_SingleJet100er2p5_ETMHF40", 511),          std::make_pair("L1_SingleMu5", 9),          std::make_pair("L1_SingleMu7", 10),          std::make_pair("L1_SingleMuCosmics", 0),          std::make_pair("L1_SingleMuCosmics_BMTF", 2),          std::make_pair("L1_SingleMuCosmics_EMTF", 4),          std::make_pair("L1_SingleMuCosmics_OMTF", 3),          std::make_pair("L1_SingleMuOpen", 1),          std::make_pair("L1_SingleMuOpen_NotBptxOR", 210),          std::make_pair("L1_SingleMuOpen_NotBptxOR_3BX", 211),          std::make_pair("L1_SingleTau100er2p1", 117),          std::make_pair("L1_SingleTau120er2p1", 118),          std::make_pair("L1_SingleTau130er2p1", 119),          std::make_pair("L1_SingleTau140er2p1", 120),          std::make_pair("L1_SingleTau20", 115),          std::make_pair("L1_SingleTau80er2p1", 116),          std::make_pair("L1_TripleEG_14_10_8", 113),          std::make_pair("L1_TripleEG_18_17_8", 114),          std::make_pair("L1_TripleEG_LooseIso20_10_5", 281),          std::make_pair("L1_TripleJet_100_85_72_VBF", 164),          std::make_pair("L1_TripleJet_105_85_76_VBF", 163),          std::make_pair("L1_TripleJet_84_68_48_VBF", 159),          std::make_pair("L1_TripleJet_88_72_56_VBF", 160),          std::make_pair("L1_TripleJet_92_76_64_VBF", 161),          std::make_pair("L1_TripleJet_98_83_71_VBF", 162),          std::make_pair("L1_TripleMu0", 39),          std::make_pair("L1_TripleMu0_OQ", 399),          std::make_pair("L1_TripleMu3", 40),          std::make_pair("L1_TripleMu3_SQ", 335),          std::make_pair("L1_TripleMu_4_4_4", 41),          std::make_pair("L1_TripleMu_5OQ_3p5OQ_2p5OQ_DoubleMu_5_2p5_OQ_OS_Mass_5to17", 404),          std::make_pair("L1_TripleMu_5OQ_3p5OQ_2p5OQ_DoubleMu_5_2p5_OQ_OS_Mass_8to14", 403),          std::make_pair("L1_TripleMu_5SQ_3SQ_0OQ", 400),          std::make_pair("L1_TripleMu_5SQ_3SQ_0OQ_DoubleMu_5_3_SQ_OS_Mass_Max9", 387),          std::make_pair("L1_TripleMu_5SQ_3SQ_0_DoubleMu_5_3_SQ_OS_Mass_Max9", 388),          std::make_pair("L1_TripleMu_5_0_0", 42),          std::make_pair("L1_TripleMu_5_3_3", 43),          std::make_pair("L1_TripleMu_5_3p5_2p5", 398),          std::make_pair("L1_TripleMu_5_3p5_2p5_DoubleMu_5_2p5_OS_Mass_5to17", 385),          std::make_pair("L1_TripleMu_5_4_2p5_DoubleMu_5_2p5_OS_Mass_5to17", 386),          std::make_pair("L1_TripleMu_5_5_3", 44),          std::make_pair("L1_UnpairedBunchBptxMinus", 479),          std::make_pair("L1_UnpairedBunchBptxPlus", 478),          std::make_pair("L1_ZeroBias", 473),          std::make_pair("L1_ZeroBias_copy", 468)      };

  static const std::map<std::string, int> Name2Id(name2id, name2id + sizeof(name2id) / sizeof(name2id[0]));
  const std::map<std::string, int>::const_iterator rc = Name2Id.find(name);
  int id = -1;
  if (rc != Name2Id.end()) id = rc->second;
  return id;
}


AlgorithmFunction getFuncFromId(const int index)
{
  static const std::pair<int, AlgorithmFunction> id2func[] = {
          std::make_pair(465, &L1_AlwaysTrue),          std::make_pair(477, &L1_BPTX_AND_Ref1_VME),          std::make_pair(481, &L1_BPTX_AND_Ref3_VME),          std::make_pair(485, &L1_BPTX_AND_Ref4_VME),          std::make_pair(471, &L1_BPTX_BeamGas_B1_VME),          std::make_pair(472, &L1_BPTX_BeamGas_B2_VME),          std::make_pair(469, &L1_BPTX_BeamGas_Ref1_VME),          std::make_pair(470, &L1_BPTX_BeamGas_Ref2_VME),          std::make_pair(480, &L1_BPTX_NotOR_VME),          std::make_pair(482, &L1_BPTX_OR_Ref3_VME),          std::make_pair(486, &L1_BPTX_OR_Ref4_VME),          std::make_pair(483, &L1_BPTX_RefAND_VME),          std::make_pair(475, &L1_BptxMinus),          std::make_pair(476, &L1_BptxOR),          std::make_pair(474, &L1_BptxPlus),          std::make_pair(467, &L1_BptxXOR),          std::make_pair(504, &L1_CDC_SingleMu_3_er1p2_TOP120_DPHI2p618_3p142),          std::make_pair(336, &L1_DoubleEG6_HTT240er),          std::make_pair(337, &L1_DoubleEG6_HTT250er),          std::make_pair(439, &L1_DoubleEG6_HTT255er),          std::make_pair(338, &L1_DoubleEG6_HTT270er),          std::make_pair(339, &L1_DoubleEG6_HTT300er),          std::make_pair(340, &L1_DoubleEG8er2p6_HTT255er),          std::make_pair(341, &L1_DoubleEG8er2p6_HTT270er),          std::make_pair(342, &L1_DoubleEG8er2p6_HTT300er),          std::make_pair(100, &L1_DoubleEG_15_10),          std::make_pair(101, &L1_DoubleEG_18_17),          std::make_pair(102, &L1_DoubleEG_20_18),          std::make_pair(103, &L1_DoubleEG_22_10),          std::make_pair(104, &L1_DoubleEG_22_12),          std::make_pair(105, &L1_DoubleEG_22_15),          std::make_pair(106, &L1_DoubleEG_23_10),          std::make_pair(107, &L1_DoubleEG_24_17),          std::make_pair(108, &L1_DoubleEG_25_12),          std::make_pair(109, &L1_DoubleEG_25_13),          std::make_pair(110, &L1_DoubleEG_25_14),          std::make_pair(279, &L1_DoubleEG_LooseIso23_10),          std::make_pair(280, &L1_DoubleEG_LooseIso24_10),          std::make_pair(123, &L1_DoubleIsoTau28er2p1),          std::make_pair(124, &L1_DoubleIsoTau30er2p1),          std::make_pair(125, &L1_DoubleIsoTau32er2p1),          std::make_pair(126, &L1_DoubleIsoTau33er2p1),          std::make_pair(127, &L1_DoubleIsoTau34er2p1),          std::make_pair(128, &L1_DoubleIsoTau35er2p1),          std::make_pair(129, &L1_DoubleIsoTau36er2p1),          std::make_pair(130, &L1_DoubleIsoTau38er2p1),          std::make_pair(251, &L1_DoubleJet100er2p3_dEta_Max1p6),          std::make_pair(155, &L1_DoubleJet100er2p7),          std::make_pair(252, &L1_DoubleJet112er2p3_dEta_Max1p6),          std::make_pair(156, &L1_DoubleJet112er2p7),          std::make_pair(157, &L1_DoubleJet120er2p7),          std::make_pair(158, &L1_DoubleJet150er2p7),          std::make_pair(216, &L1_DoubleJet30_Mass_Min300_dEta_Max1p5),          std::make_pair(217, &L1_DoubleJet30_Mass_Min320_dEta_Max1p5),          std::make_pair(218, &L1_DoubleJet30_Mass_Min340_dEta_Max1p5),          std::make_pair(219, &L1_DoubleJet30_Mass_Min360_dEta_Max1p5),          std::make_pair(220, &L1_DoubleJet30_Mass_Min380_dEta_Max1p5),          std::make_pair(290, &L1_DoubleJet30_Mass_Min400_Mu10),          std::make_pair(289, &L1_DoubleJet30_Mass_Min400_Mu6),          std::make_pair(221, &L1_DoubleJet30_Mass_Min400_dEta_Max1p5),          std::make_pair(292, &L1_DoubleJet35_rmovlp_IsoTau45_Mass_Min450),          std::make_pair(151, &L1_DoubleJet40er2p7),          std::make_pair(152, &L1_DoubleJet50er2p7),          std::make_pair(153, &L1_DoubleJet60er2p7),          std::make_pair(278, &L1_DoubleJet60er2p7_ETM100),          std::make_pair(429, &L1_DoubleJet60er2p7_ETM60),          std::make_pair(275, &L1_DoubleJet60er2p7_ETM70),          std::make_pair(276, &L1_DoubleJet60er2p7_ETM80),          std::make_pair(277, &L1_DoubleJet60er2p7_ETM90),          std::make_pair(154, &L1_DoubleJet80er2p7),          std::make_pair(283, &L1_DoubleJet_100_30_DoubleJet30_Mass_Min620),          std::make_pair(284, &L1_DoubleJet_100_35_DoubleJet35_Mass_Min620),          std::make_pair(285, &L1_DoubleJet_110_35_DoubleJet35_Mass_Min620),          std::make_pair(286, &L1_DoubleJet_110_40_DoubleJet40_Mass_Min620),          std::make_pair(287, &L1_DoubleJet_115_35_DoubleJet35_Mass_Min620),          std::make_pair(288, &L1_DoubleJet_115_40_DoubleJet40_Mass_Min620),          std::make_pair(282, &L1_DoubleJet_90_30_DoubleJet30_Mass_Min620),          std::make_pair(111, &L1_DoubleLooseIsoEG22er2p1),          std::make_pair(112, &L1_DoubleLooseIsoEG24er2p1),          std::make_pair(30, &L1_DoubleMu0),          std::make_pair(432, &L1_DoubleMu0_ETM40),          std::make_pair(433, &L1_DoubleMu0_ETM55),          std::make_pair(434, &L1_DoubleMu0_ETM60),          std::make_pair(435, &L1_DoubleMu0_ETM65),          std::make_pair(436, &L1_DoubleMu0_ETM70),          std::make_pair(390, &L1_DoubleMu0_SQ),          std::make_pair(391, &L1_DoubleMu0_SQ_OS),          std::make_pair(381, &L1_DoubleMu0er1p4_SQ_OS_dR_Max1p4),          std::make_pair(440, &L1_DoubleMu0er1p4_dEta_Max1p8_OS),          std::make_pair(395, &L1_DoubleMu0er1p5_SQ_OS),          std::make_pair(375, &L1_DoubleMu0er1p5_SQ_OS_dR_Max1p4),          std::make_pair(223, &L1_DoubleMu0er1p5_SQ_dR_Max1p4),          std::make_pair(222, &L1_DoubleMu0er2_SQ_dR_Max1p4),          std::make_pair(37, &L1_DoubleMu18er2p1),          std::make_pair(38, &L1_DoubleMu22er2p1),          std::make_pair(402, &L1_DoubleMu3_OS_DoubleEG7p5Upsilon),          std::make_pair(323, &L1_DoubleMu3_SQ_ETMHF40_Jet60_OR_DoubleJet30),          std::make_pair(324, &L1_DoubleMu3_SQ_ETMHF50_Jet60_OR_DoubleJet30),          std::make_pair(325, &L1_DoubleMu3_SQ_ETMHF60_Jet60_OR_DoubleJet30),          std::make_pair(326, &L1_DoubleMu3_SQ_ETMHF70_Jet60_OR_DoubleJet30),          std::make_pair(327, &L1_DoubleMu3_SQ_ETMHF80_Jet60_OR_DoubleJet30),          std::make_pair(328, &L1_DoubleMu3_SQ_HTT100er),          std::make_pair(329, &L1_DoubleMu3_SQ_HTT200er),          std::make_pair(330, &L1_DoubleMu3_SQ_HTT220er),          std::make_pair(331, &L1_DoubleMu3_SQ_HTT240er),          std::make_pair(380, &L1_DoubleMu4_OS_EG12),          std::make_pair(396, &L1_DoubleMu4_SQ_OS),          std::make_pair(377, &L1_DoubleMu4_SQ_OS_dR_Max1p2),          std::make_pair(392, &L1_DoubleMu4p5_SQ),          std::make_pair(393, &L1_DoubleMu4p5_SQ_OS),          std::make_pair(382, &L1_DoubleMu4p5_SQ_OS_dR_Max1p2),          std::make_pair(394, &L1_DoubleMu4p5er2p0_SQ_OS),          std::make_pair(376, &L1_DoubleMu4p5er2p0_SQ_OS_Mass7to18),          std::make_pair(401, &L1_DoubleMu5Upsilon_OS_DoubleEG3),          std::make_pair(383, &L1_DoubleMu5_OS_EG12),          std::make_pair(397, &L1_DoubleMu5_SQ_OS),          std::make_pair(378, &L1_DoubleMu5_SQ_OS_Mass7to18),          std::make_pair(384, &L1_DoubleMu6_SQ_OS),          std::make_pair(406, &L1_DoubleMu7_EG7),          std::make_pair(365, &L1_DoubleMu7_SQ_EG7),          std::make_pair(389, &L1_DoubleMu8_SQ),          std::make_pair(441, &L1_DoubleMu_10_0_dEta_Max1p8),          std::make_pair(31, &L1_DoubleMu_11_4),          std::make_pair(32, &L1_DoubleMu_12_5),          std::make_pair(33, &L1_DoubleMu_12_8),          std::make_pair(34, &L1_DoubleMu_13_6),          std::make_pair(35, &L1_DoubleMu_15_5),          std::make_pair(332, &L1_DoubleMu_15_5_SQ),          std::make_pair(36, &L1_DoubleMu_15_7),          std::make_pair(333, &L1_DoubleMu_15_7_SQ),          std::make_pair(334, &L1_DoubleMu_15_7_SQ_Mass_Min4),          std::make_pair(379, &L1_DoubleMu_20_2_SQ_Mass_Max20),          std::make_pair(121, &L1_DoubleTau50er2p1),          std::make_pair(122, &L1_DoubleTau70er2p1),          std::make_pair(427, &L1_EG25er2p1_HTT125er),          std::make_pair(428, &L1_EG27er2p1_HTT200er),          std::make_pair(193, &L1_ETM100),          std::make_pair(273, &L1_ETM100_Jet60_dPhi_Min0p4),          std::make_pair(194, &L1_ETM105),          std::make_pair(195, &L1_ETM110),          std::make_pair(274, &L1_ETM110_Jet60_dPhi_Min0p4),          std::make_pair(196, &L1_ETM115),          std::make_pair(197, &L1_ETM120),          std::make_pair(198, &L1_ETM150),          std::make_pair(183, &L1_ETM30),          std::make_pair(184, &L1_ETM40),          std::make_pair(185, &L1_ETM50),          std::make_pair(186, &L1_ETM60),          std::make_pair(187, &L1_ETM70),          std::make_pair(188, &L1_ETM75),          std::make_pair(431, &L1_ETM75_Jet60_dPhi_Min0p4),          std::make_pair(189, &L1_ETM80),          std::make_pair(271, &L1_ETM80_Jet60_dPhi_Min0p4),          std::make_pair(190, &L1_ETM85),          std::make_pair(191, &L1_ETM90),          std::make_pair(272, &L1_ETM90_Jet60_dPhi_Min0p4),          std::make_pair(192, &L1_ETM95),          std::make_pair(202, &L1_ETMHF100),          std::make_pair(368, &L1_ETMHF100_HTT60er),          std::make_pair(357, &L1_ETMHF100_Jet60_OR_DiJet30woTT28),          std::make_pair(349, &L1_ETMHF100_Jet60_OR_DoubleJet30),          std::make_pair(363, &L1_ETMHF100_Jet90_OR_DoubleJet45_OR_TripleJet30),          std::make_pair(203, &L1_ETMHF110),          std::make_pair(369, &L1_ETMHF110_HTT60er),          std::make_pair(358, &L1_ETMHF110_Jet60_OR_DiJet30woTT28),          std::make_pair(364, &L1_ETMHF110_Jet90_OR_DoubleJet45_OR_TripleJet30),          std::make_pair(204, &L1_ETMHF120),          std::make_pair(370, &L1_ETMHF120_HTT60er),          std::make_pair(359, &L1_ETMHF120_Jet60_OR_DiJet30woTT28),          std::make_pair(205, &L1_ETMHF150),          std::make_pair(199, &L1_ETMHF70),          std::make_pair(360, &L1_ETMHF70_Jet90_OR_DoubleJet45_OR_TripleJet30),          std::make_pair(200, &L1_ETMHF80),          std::make_pair(366, &L1_ETMHF80_HTT60er),          std::make_pair(361, &L1_ETMHF80_Jet90_OR_DoubleJet45_OR_TripleJet30),          std::make_pair(201, &L1_ETMHF90),          std::make_pair(367, &L1_ETMHF90_HTT60er),          std::make_pair(362, &L1_ETMHF90_Jet90_OR_DoubleJet45_OR_TripleJet30),          std::make_pair(457, &L1_ETT100_BptxAND),          std::make_pair(458, &L1_ETT110_BptxAND),          std::make_pair(448, &L1_ETT40_BptxAND),          std::make_pair(449, &L1_ETT50_BptxAND),          std::make_pair(450, &L1_ETT60_BptxAND),          std::make_pair(451, &L1_ETT70_BptxAND),          std::make_pair(452, &L1_ETT75_BptxAND),          std::make_pair(453, &L1_ETT80_BptxAND),          std::make_pair(454, &L1_ETT85_BptxAND),          std::make_pair(455, &L1_ETT90_BptxAND),          std::make_pair(456, &L1_ETT95_BptxAND),          std::make_pair(417, &L1_FirstBunchAfterTrain),          std::make_pair(416, &L1_FirstBunchInTrain),          std::make_pair(484, &L1_FirstCollisionInOrbit),          std::make_pair(488, &L1_FirstCollisionInTrain),          std::make_pair(168, &L1_HTT120er),          std::make_pair(169, &L1_HTT160er),          std::make_pair(170, &L1_HTT200er),          std::make_pair(171, &L1_HTT220er),          std::make_pair(172, &L1_HTT240er),          std::make_pair(243, &L1_HTT250er_QuadJet_70_55_40_35_er2p5),          std::make_pair(173, &L1_HTT255er),          std::make_pair(174, &L1_HTT270er),          std::make_pair(175, &L1_HTT280er),          std::make_pair(244, &L1_HTT280er_QuadJet_70_55_40_35_er2p5),          std::make_pair(176, &L1_HTT300er),          std::make_pair(245, &L1_HTT300er_QuadJet_70_55_40_35_er2p5),          std::make_pair(177, &L1_HTT320er),          std::make_pair(246, &L1_HTT320er_QuadJet_70_55_40_40_er2p4),          std::make_pair(247, &L1_HTT320er_QuadJet_70_55_40_40_er2p5),          std::make_pair(249, &L1_HTT320er_QuadJet_70_55_45_45_er2p5),          std::make_pair(178, &L1_HTT340er),          std::make_pair(248, &L1_HTT340er_QuadJet_70_55_40_40_er2p5),          std::make_pair(250, &L1_HTT340er_QuadJet_70_55_45_45_er2p5),          std::make_pair(179, &L1_HTT380er),          std::make_pair(180, &L1_HTT400er),          std::make_pair(181, &L1_HTT450er),          std::make_pair(182, &L1_HTT500er),          std::make_pair(97, &L1_IsoEG33_Mt40),          std::make_pair(98, &L1_IsoEG33_Mt44),          std::make_pair(99, &L1_IsoEG33_Mt48),          std::make_pair(259, &L1_IsoTau40er_ETM100),          std::make_pair(260, &L1_IsoTau40er_ETM105),          std::make_pair(261, &L1_IsoTau40er_ETM110),          std::make_pair(262, &L1_IsoTau40er_ETM115),          std::make_pair(263, &L1_IsoTau40er_ETM120),          std::make_pair(255, &L1_IsoTau40er_ETM80),          std::make_pair(256, &L1_IsoTau40er_ETM85),          std::make_pair(257, &L1_IsoTau40er_ETM90),          std::make_pair(258, &L1_IsoTau40er_ETM95),          std::make_pair(266, &L1_IsoTau40er_ETMHF100),          std::make_pair(267, &L1_IsoTau40er_ETMHF110),          std::make_pair(268, &L1_IsoTau40er_ETMHF120),          std::make_pair(264, &L1_IsoTau40er_ETMHF80),          std::make_pair(265, &L1_IsoTau40er_ETMHF90),          std::make_pair(415, &L1_IsolatedBunch),          std::make_pair(487, &L1_LastCollisionInTrain),          std::make_pair(294, &L1_LooseIsoEG22er2p1_IsoTau26er2p1_dR_Min0p3),          std::make_pair(229, &L1_LooseIsoEG24er2p1_HTT100er),          std::make_pair(295, &L1_LooseIsoEG24er2p1_IsoTau27er2p1_dR_Min0p3),          std::make_pair(225, &L1_LooseIsoEG24er2p1_Jet26er2p7_dR_Min0p3),          std::make_pair(232, &L1_LooseIsoEG24er2p1_TripleJet_26er2p7_26_26er2p7),          std::make_pair(230, &L1_LooseIsoEG26er2p1_HTT100er),          std::make_pair(226, &L1_LooseIsoEG26er2p1_Jet34er2p7_dR_Min0p3),          std::make_pair(231, &L1_LooseIsoEG28er2p1_HTT100er),          std::make_pair(227, &L1_LooseIsoEG28er2p1_Jet34er2p7_dR_Min0p3),          std::make_pair(228, &L1_LooseIsoEG30er2p1_Jet34er2p7_dR_Min0p3),          std::make_pair(423, &L1_MU20_EG15),          std::make_pair(459, &L1_MinimumBiasHF0_AND_BptxAND),          std::make_pair(460, &L1_MinimumBiasHF0_OR_BptxAND),          std::make_pair(461, &L1_Mu10er2p1_ETM30),          std::make_pair(253, &L1_Mu10er2p3_Jet32er2p3_dR_Max0p4_DoubleJet32er2p3_dEta_Max1p6),          std::make_pair(421, &L1_Mu12_EG10),          std::make_pair(254, &L1_Mu12er2p3_Jet40er2p3_dR_Max0p4_DoubleJet40er2p3_dEta_Max1p6),          std::make_pair(462, &L1_Mu14er2p1_ETM30),          std::make_pair(317, &L1_Mu15_HTT100er),          std::make_pair(233, &L1_Mu18_HTT100er),          std::make_pair(234, &L1_Mu18_Jet24er2p7),          std::make_pair(302, &L1_Mu18er2p1_IsoTau26er2p1),          std::make_pair(299, &L1_Mu18er2p1_Tau24er2p1),          std::make_pair(422, &L1_Mu20_EG10),          std::make_pair(235, &L1_Mu20_EG17),          std::make_pair(424, &L1_Mu20_LooseIsoEG6),          std::make_pair(303, &L1_Mu20er2p1_IsoTau26er2p1),          std::make_pair(304, &L1_Mu20er2p1_IsoTau27er2p1),          std::make_pair(305, &L1_Mu22er2p1_IsoTau28er2p1),          std::make_pair(306, &L1_Mu22er2p1_IsoTau30er2p1),          std::make_pair(307, &L1_Mu22er2p1_IsoTau32er2p1),          std::make_pair(308, &L1_Mu22er2p1_IsoTau33er2p1),          std::make_pair(309, &L1_Mu22er2p1_IsoTau34er2p1),          std::make_pair(310, &L1_Mu22er2p1_IsoTau35er2p1),          std::make_pair(311, &L1_Mu22er2p1_IsoTau36er2p1),          std::make_pair(312, &L1_Mu22er2p1_IsoTau38er2p1),          std::make_pair(269, &L1_Mu22er2p1_IsoTau40er2p1),          std::make_pair(300, &L1_Mu22er2p1_Tau50er2p1),          std::make_pair(301, &L1_Mu22er2p1_Tau70er2p1),          std::make_pair(236, &L1_Mu23_EG10),          std::make_pair(237, &L1_Mu23_LooseIsoEG10),          std::make_pair(445, &L1_Mu3_Jet120er2p7_dEta_Max0p4_dPhi_Max0p4),          std::make_pair(443, &L1_Mu3_Jet16er2p7_dEta_Max0p4_dPhi_Max0p4),          std::make_pair(371, &L1_Mu3_Jet30er2p5),          std::make_pair(444, &L1_Mu3_Jet60er2p7_dEta_Max0p4_dPhi_Max0p4),          std::make_pair(418, &L1_Mu5_EG15),          std::make_pair(419, &L1_Mu5_EG20),          std::make_pair(238, &L1_Mu5_EG23),          std::make_pair(420, &L1_Mu5_LooseIsoEG18),          std::make_pair(239, &L1_Mu5_LooseIsoEG20),          std::make_pair(442, &L1_Mu6_DoubleEG10),          std::make_pair(405, &L1_Mu6_DoubleEG17),          std::make_pair(425, &L1_Mu6_HTT200er),          std::make_pair(315, &L1_Mu6_HTT240er),          std::make_pair(316, &L1_Mu6_HTT250er),          std::make_pair(240, &L1_Mu7_EG23),          std::make_pair(241, &L1_Mu7_LooseIsoEG20),          std::make_pair(242, &L1_Mu7_LooseIsoEG23),          std::make_pair(426, &L1_Mu8_HTT150er),          std::make_pair(466, &L1_NotBptxOR),          std::make_pair(270, &L1_QuadJet36er2p7_IsoTau52er2p1),          std::make_pair(430, &L1_QuadJet36er2p7_Tau52),          std::make_pair(165, &L1_QuadJet40er2p7),          std::make_pair(166, &L1_QuadJet50er2p7),          std::make_pair(167, &L1_QuadJet60er2p7),          std::make_pair(45, &L1_QuadMu0),          std::make_pair(51, &L1_SingleEG10),          std::make_pair(52, &L1_SingleEG15),          std::make_pair(53, &L1_SingleEG18),          std::make_pair(54, &L1_SingleEG24),          std::make_pair(55, &L1_SingleEG26),          std::make_pair(56, &L1_SingleEG28),          std::make_pair(446, &L1_SingleEG2_BptxAND),          std::make_pair(57, &L1_SingleEG30),          std::make_pair(58, &L1_SingleEG32),          std::make_pair(59, &L1_SingleEG34),          std::make_pair(66, &L1_SingleEG34er2p1),          std::make_pair(60, &L1_SingleEG36),          std::make_pair(67, &L1_SingleEG36er2p1),          std::make_pair(61, &L1_SingleEG38),          std::make_pair(68, &L1_SingleEG38er2p1),          std::make_pair(62, &L1_SingleEG40),          std::make_pair(63, &L1_SingleEG42),          std::make_pair(64, &L1_SingleEG45),          std::make_pair(50, &L1_SingleEG5),          std::make_pair(65, &L1_SingleEG50),          std::make_pair(69, &L1_SingleIsoEG18),          std::make_pair(83, &L1_SingleIsoEG18er2p1),          std::make_pair(70, &L1_SingleIsoEG20),          std::make_pair(84, &L1_SingleIsoEG20er2p1),          std::make_pair(71, &L1_SingleIsoEG22),          std::make_pair(85, &L1_SingleIsoEG22er2p1),          std::make_pair(72, &L1_SingleIsoEG24),          std::make_pair(86, &L1_SingleIsoEG24er2p1),          std::make_pair(73, &L1_SingleIsoEG26),          std::make_pair(87, &L1_SingleIsoEG26er2p1),          std::make_pair(74, &L1_SingleIsoEG28),          std::make_pair(88, &L1_SingleIsoEG28er2p1),          std::make_pair(75, &L1_SingleIsoEG30),          std::make_pair(89, &L1_SingleIsoEG30er2p1),          std::make_pair(76, &L1_SingleIsoEG32),          std::make_pair(90, &L1_SingleIsoEG32er2p1),          std::make_pair(91, &L1_SingleIsoEG33er2p1),          std::make_pair(77, &L1_SingleIsoEG34),          std::make_pair(92, &L1_SingleIsoEG34er2p1),          std::make_pair(78, &L1_SingleIsoEG35),          std::make_pair(93, &L1_SingleIsoEG35er2p1),          std::make_pair(79, &L1_SingleIsoEG36),          std::make_pair(94, &L1_SingleIsoEG36er2p1),          std::make_pair(80, &L1_SingleIsoEG37),          std::make_pair(81, &L1_SingleIsoEG38),          std::make_pair(95, &L1_SingleIsoEG38er2p1),          std::make_pair(82, &L1_SingleIsoEG40),          std::make_pair(96, &L1_SingleIsoEG40er2p1),          std::make_pair(136, &L1_SingleJet120),          std::make_pair(146, &L1_SingleJet120_FWD),          std::make_pair(447, &L1_SingleJet12_BptxAND),          std::make_pair(137, &L1_SingleJet140),          std::make_pair(138, &L1_SingleJet150),          std::make_pair(131, &L1_SingleJet16),          std::make_pair(139, &L1_SingleJet160),          std::make_pair(140, &L1_SingleJet170),          std::make_pair(141, &L1_SingleJet180),          std::make_pair(132, &L1_SingleJet20),          std::make_pair(142, &L1_SingleJet200),          std::make_pair(212, &L1_SingleJet20er2p7_NotBptxOR),          std::make_pair(213, &L1_SingleJet20er2p7_NotBptxOR_3BX),          std::make_pair(133, &L1_SingleJet35),          std::make_pair(143, &L1_SingleJet35_FWD),          std::make_pair(148, &L1_SingleJet35_HFm),          std::make_pair(147, &L1_SingleJet35_HFp),          std::make_pair(214, &L1_SingleJet43er2p7_NotBptxOR_3BX),          std::make_pair(215, &L1_SingleJet46er2p7_NotBptxOR_3BX),          std::make_pair(134, &L1_SingleJet60),          std::make_pair(144, &L1_SingleJet60_FWD),          std::make_pair(150, &L1_SingleJet60_HFm),          std::make_pair(149, &L1_SingleJet60_HFp),          std::make_pair(135, &L1_SingleJet90),          std::make_pair(145, &L1_SingleJet90_FWD),          std::make_pair(5, &L1_SingleMu0_BMTF),          std::make_pair(7, &L1_SingleMu0_EMTF),          std::make_pair(6, &L1_SingleMu0_OMTF),          std::make_pair(11, &L1_SingleMu10_LowQ),          std::make_pair(12, &L1_SingleMu11_LowQ),          std::make_pair(13, &L1_SingleMu12_LowQ_BMTF),          std::make_pair(15, &L1_SingleMu12_LowQ_EMTF),          std::make_pair(14, &L1_SingleMu12_LowQ_OMTF),          std::make_pair(25, &L1_SingleMu14er2p1),          std::make_pair(16, &L1_SingleMu16),          std::make_pair(26, &L1_SingleMu16er2p1),          std::make_pair(17, &L1_SingleMu18),          std::make_pair(27, &L1_SingleMu18er2p1),          std::make_pair(18, &L1_SingleMu20),          std::make_pair(28, &L1_SingleMu20er2p1),          std::make_pair(19, &L1_SingleMu22),          std::make_pair(20, &L1_SingleMu22_BMTF),          std::make_pair(22, &L1_SingleMu22_EMTF),          std::make_pair(21, &L1_SingleMu22_OMTF),          std::make_pair(29, &L1_SingleMu22er2p1),          std::make_pair(23, &L1_SingleMu25),          std::make_pair(8, &L1_SingleMu3),          std::make_pair(24, &L1_SingleMu30),          std::make_pair(511, &L1_SingleMu3er1p5_SingleJet100er2p5_ETMHF40),          std::make_pair(9, &L1_SingleMu5),          std::make_pair(10, &L1_SingleMu7),          std::make_pair(0, &L1_SingleMuCosmics),          std::make_pair(2, &L1_SingleMuCosmics_BMTF),          std::make_pair(4, &L1_SingleMuCosmics_EMTF),          std::make_pair(3, &L1_SingleMuCosmics_OMTF),          std::make_pair(1, &L1_SingleMuOpen),          std::make_pair(210, &L1_SingleMuOpen_NotBptxOR),          std::make_pair(211, &L1_SingleMuOpen_NotBptxOR_3BX),          std::make_pair(117, &L1_SingleTau100er2p1),          std::make_pair(118, &L1_SingleTau120er2p1),          std::make_pair(119, &L1_SingleTau130er2p1),          std::make_pair(120, &L1_SingleTau140er2p1),          std::make_pair(115, &L1_SingleTau20),          std::make_pair(116, &L1_SingleTau80er2p1),          std::make_pair(113, &L1_TripleEG_14_10_8),          std::make_pair(114, &L1_TripleEG_18_17_8),          std::make_pair(281, &L1_TripleEG_LooseIso20_10_5),          std::make_pair(164, &L1_TripleJet_100_85_72_VBF),          std::make_pair(163, &L1_TripleJet_105_85_76_VBF),          std::make_pair(159, &L1_TripleJet_84_68_48_VBF),          std::make_pair(160, &L1_TripleJet_88_72_56_VBF),          std::make_pair(161, &L1_TripleJet_92_76_64_VBF),          std::make_pair(162, &L1_TripleJet_98_83_71_VBF),          std::make_pair(39, &L1_TripleMu0),          std::make_pair(399, &L1_TripleMu0_OQ),          std::make_pair(40, &L1_TripleMu3),          std::make_pair(335, &L1_TripleMu3_SQ),          std::make_pair(41, &L1_TripleMu_4_4_4),          std::make_pair(404, &L1_TripleMu_5OQ_3p5OQ_2p5OQ_DoubleMu_5_2p5_OQ_OS_Mass_5to17),          std::make_pair(403, &L1_TripleMu_5OQ_3p5OQ_2p5OQ_DoubleMu_5_2p5_OQ_OS_Mass_8to14),          std::make_pair(400, &L1_TripleMu_5SQ_3SQ_0OQ),          std::make_pair(387, &L1_TripleMu_5SQ_3SQ_0OQ_DoubleMu_5_3_SQ_OS_Mass_Max9),          std::make_pair(388, &L1_TripleMu_5SQ_3SQ_0_DoubleMu_5_3_SQ_OS_Mass_Max9),          std::make_pair(42, &L1_TripleMu_5_0_0),          std::make_pair(43, &L1_TripleMu_5_3_3),          std::make_pair(398, &L1_TripleMu_5_3p5_2p5),          std::make_pair(385, &L1_TripleMu_5_3p5_2p5_DoubleMu_5_2p5_OS_Mass_5to17),          std::make_pair(386, &L1_TripleMu_5_4_2p5_DoubleMu_5_2p5_OS_Mass_5to17),          std::make_pair(44, &L1_TripleMu_5_5_3),          std::make_pair(479, &L1_UnpairedBunchBptxMinus),          std::make_pair(478, &L1_UnpairedBunchBptxPlus),          std::make_pair(473, &L1_ZeroBias),          std::make_pair(468, &L1_ZeroBias_copy)      };

  static const std::map<int, AlgorithmFunction> Id2Func(id2func, id2func + sizeof(id2func) / sizeof(id2func[0]));
  const std::map<int, AlgorithmFunction>::const_iterator rc = Id2Func.find(index);
  AlgorithmFunction fp = 0;
  if (rc != Id2Func.end()) fp = rc->second;
  return fp;
}


AlgorithmFunction getFuncFromName(const std::string& name)
{
  static const std::pair<std::string, AlgorithmFunction> name2func[] = {
          std::make_pair("L1_AlwaysTrue", &L1_AlwaysTrue),          std::make_pair("L1_BPTX_AND_Ref1_VME", &L1_BPTX_AND_Ref1_VME),          std::make_pair("L1_BPTX_AND_Ref3_VME", &L1_BPTX_AND_Ref3_VME),          std::make_pair("L1_BPTX_AND_Ref4_VME", &L1_BPTX_AND_Ref4_VME),          std::make_pair("L1_BPTX_BeamGas_B1_VME", &L1_BPTX_BeamGas_B1_VME),          std::make_pair("L1_BPTX_BeamGas_B2_VME", &L1_BPTX_BeamGas_B2_VME),          std::make_pair("L1_BPTX_BeamGas_Ref1_VME", &L1_BPTX_BeamGas_Ref1_VME),          std::make_pair("L1_BPTX_BeamGas_Ref2_VME", &L1_BPTX_BeamGas_Ref2_VME),          std::make_pair("L1_BPTX_NotOR_VME", &L1_BPTX_NotOR_VME),          std::make_pair("L1_BPTX_OR_Ref3_VME", &L1_BPTX_OR_Ref3_VME),          std::make_pair("L1_BPTX_OR_Ref4_VME", &L1_BPTX_OR_Ref4_VME),          std::make_pair("L1_BPTX_RefAND_VME", &L1_BPTX_RefAND_VME),          std::make_pair("L1_BptxMinus", &L1_BptxMinus),          std::make_pair("L1_BptxOR", &L1_BptxOR),          std::make_pair("L1_BptxPlus", &L1_BptxPlus),          std::make_pair("L1_BptxXOR", &L1_BptxXOR),          std::make_pair("L1_CDC_SingleMu_3_er1p2_TOP120_DPHI2p618_3p142", &L1_CDC_SingleMu_3_er1p2_TOP120_DPHI2p618_3p142),          std::make_pair("L1_DoubleEG6_HTT240er", &L1_DoubleEG6_HTT240er),          std::make_pair("L1_DoubleEG6_HTT250er", &L1_DoubleEG6_HTT250er),          std::make_pair("L1_DoubleEG6_HTT255er", &L1_DoubleEG6_HTT255er),          std::make_pair("L1_DoubleEG6_HTT270er", &L1_DoubleEG6_HTT270er),          std::make_pair("L1_DoubleEG6_HTT300er", &L1_DoubleEG6_HTT300er),          std::make_pair("L1_DoubleEG8er2p6_HTT255er", &L1_DoubleEG8er2p6_HTT255er),          std::make_pair("L1_DoubleEG8er2p6_HTT270er", &L1_DoubleEG8er2p6_HTT270er),          std::make_pair("L1_DoubleEG8er2p6_HTT300er", &L1_DoubleEG8er2p6_HTT300er),          std::make_pair("L1_DoubleEG_15_10", &L1_DoubleEG_15_10),          std::make_pair("L1_DoubleEG_18_17", &L1_DoubleEG_18_17),          std::make_pair("L1_DoubleEG_20_18", &L1_DoubleEG_20_18),          std::make_pair("L1_DoubleEG_22_10", &L1_DoubleEG_22_10),          std::make_pair("L1_DoubleEG_22_12", &L1_DoubleEG_22_12),          std::make_pair("L1_DoubleEG_22_15", &L1_DoubleEG_22_15),          std::make_pair("L1_DoubleEG_23_10", &L1_DoubleEG_23_10),          std::make_pair("L1_DoubleEG_24_17", &L1_DoubleEG_24_17),          std::make_pair("L1_DoubleEG_25_12", &L1_DoubleEG_25_12),          std::make_pair("L1_DoubleEG_25_13", &L1_DoubleEG_25_13),          std::make_pair("L1_DoubleEG_25_14", &L1_DoubleEG_25_14),          std::make_pair("L1_DoubleEG_LooseIso23_10", &L1_DoubleEG_LooseIso23_10),          std::make_pair("L1_DoubleEG_LooseIso24_10", &L1_DoubleEG_LooseIso24_10),          std::make_pair("L1_DoubleIsoTau28er2p1", &L1_DoubleIsoTau28er2p1),          std::make_pair("L1_DoubleIsoTau30er2p1", &L1_DoubleIsoTau30er2p1),          std::make_pair("L1_DoubleIsoTau32er2p1", &L1_DoubleIsoTau32er2p1),          std::make_pair("L1_DoubleIsoTau33er2p1", &L1_DoubleIsoTau33er2p1),          std::make_pair("L1_DoubleIsoTau34er2p1", &L1_DoubleIsoTau34er2p1),          std::make_pair("L1_DoubleIsoTau35er2p1", &L1_DoubleIsoTau35er2p1),          std::make_pair("L1_DoubleIsoTau36er2p1", &L1_DoubleIsoTau36er2p1),          std::make_pair("L1_DoubleIsoTau38er2p1", &L1_DoubleIsoTau38er2p1),          std::make_pair("L1_DoubleJet100er2p3_dEta_Max1p6", &L1_DoubleJet100er2p3_dEta_Max1p6),          std::make_pair("L1_DoubleJet100er2p7", &L1_DoubleJet100er2p7),          std::make_pair("L1_DoubleJet112er2p3_dEta_Max1p6", &L1_DoubleJet112er2p3_dEta_Max1p6),          std::make_pair("L1_DoubleJet112er2p7", &L1_DoubleJet112er2p7),          std::make_pair("L1_DoubleJet120er2p7", &L1_DoubleJet120er2p7),          std::make_pair("L1_DoubleJet150er2p7", &L1_DoubleJet150er2p7),          std::make_pair("L1_DoubleJet30_Mass_Min300_dEta_Max1p5", &L1_DoubleJet30_Mass_Min300_dEta_Max1p5),          std::make_pair("L1_DoubleJet30_Mass_Min320_dEta_Max1p5", &L1_DoubleJet30_Mass_Min320_dEta_Max1p5),          std::make_pair("L1_DoubleJet30_Mass_Min340_dEta_Max1p5", &L1_DoubleJet30_Mass_Min340_dEta_Max1p5),          std::make_pair("L1_DoubleJet30_Mass_Min360_dEta_Max1p5", &L1_DoubleJet30_Mass_Min360_dEta_Max1p5),          std::make_pair("L1_DoubleJet30_Mass_Min380_dEta_Max1p5", &L1_DoubleJet30_Mass_Min380_dEta_Max1p5),          std::make_pair("L1_DoubleJet30_Mass_Min400_Mu10", &L1_DoubleJet30_Mass_Min400_Mu10),          std::make_pair("L1_DoubleJet30_Mass_Min400_Mu6", &L1_DoubleJet30_Mass_Min400_Mu6),          std::make_pair("L1_DoubleJet30_Mass_Min400_dEta_Max1p5", &L1_DoubleJet30_Mass_Min400_dEta_Max1p5),          std::make_pair("L1_DoubleJet35_rmovlp_IsoTau45_Mass_Min450", &L1_DoubleJet35_rmovlp_IsoTau45_Mass_Min450),          std::make_pair("L1_DoubleJet40er2p7", &L1_DoubleJet40er2p7),          std::make_pair("L1_DoubleJet50er2p7", &L1_DoubleJet50er2p7),          std::make_pair("L1_DoubleJet60er2p7", &L1_DoubleJet60er2p7),          std::make_pair("L1_DoubleJet60er2p7_ETM100", &L1_DoubleJet60er2p7_ETM100),          std::make_pair("L1_DoubleJet60er2p7_ETM60", &L1_DoubleJet60er2p7_ETM60),          std::make_pair("L1_DoubleJet60er2p7_ETM70", &L1_DoubleJet60er2p7_ETM70),          std::make_pair("L1_DoubleJet60er2p7_ETM80", &L1_DoubleJet60er2p7_ETM80),          std::make_pair("L1_DoubleJet60er2p7_ETM90", &L1_DoubleJet60er2p7_ETM90),          std::make_pair("L1_DoubleJet80er2p7", &L1_DoubleJet80er2p7),          std::make_pair("L1_DoubleJet_100_30_DoubleJet30_Mass_Min620", &L1_DoubleJet_100_30_DoubleJet30_Mass_Min620),          std::make_pair("L1_DoubleJet_100_35_DoubleJet35_Mass_Min620", &L1_DoubleJet_100_35_DoubleJet35_Mass_Min620),          std::make_pair("L1_DoubleJet_110_35_DoubleJet35_Mass_Min620", &L1_DoubleJet_110_35_DoubleJet35_Mass_Min620),          std::make_pair("L1_DoubleJet_110_40_DoubleJet40_Mass_Min620", &L1_DoubleJet_110_40_DoubleJet40_Mass_Min620),          std::make_pair("L1_DoubleJet_115_35_DoubleJet35_Mass_Min620", &L1_DoubleJet_115_35_DoubleJet35_Mass_Min620),          std::make_pair("L1_DoubleJet_115_40_DoubleJet40_Mass_Min620", &L1_DoubleJet_115_40_DoubleJet40_Mass_Min620),          std::make_pair("L1_DoubleJet_90_30_DoubleJet30_Mass_Min620", &L1_DoubleJet_90_30_DoubleJet30_Mass_Min620),          std::make_pair("L1_DoubleLooseIsoEG22er2p1", &L1_DoubleLooseIsoEG22er2p1),          std::make_pair("L1_DoubleLooseIsoEG24er2p1", &L1_DoubleLooseIsoEG24er2p1),          std::make_pair("L1_DoubleMu0", &L1_DoubleMu0),          std::make_pair("L1_DoubleMu0_ETM40", &L1_DoubleMu0_ETM40),          std::make_pair("L1_DoubleMu0_ETM55", &L1_DoubleMu0_ETM55),          std::make_pair("L1_DoubleMu0_ETM60", &L1_DoubleMu0_ETM60),          std::make_pair("L1_DoubleMu0_ETM65", &L1_DoubleMu0_ETM65),          std::make_pair("L1_DoubleMu0_ETM70", &L1_DoubleMu0_ETM70),          std::make_pair("L1_DoubleMu0_SQ", &L1_DoubleMu0_SQ),          std::make_pair("L1_DoubleMu0_SQ_OS", &L1_DoubleMu0_SQ_OS),          std::make_pair("L1_DoubleMu0er1p4_SQ_OS_dR_Max1p4", &L1_DoubleMu0er1p4_SQ_OS_dR_Max1p4),          std::make_pair("L1_DoubleMu0er1p4_dEta_Max1p8_OS", &L1_DoubleMu0er1p4_dEta_Max1p8_OS),          std::make_pair("L1_DoubleMu0er1p5_SQ_OS", &L1_DoubleMu0er1p5_SQ_OS),          std::make_pair("L1_DoubleMu0er1p5_SQ_OS_dR_Max1p4", &L1_DoubleMu0er1p5_SQ_OS_dR_Max1p4),          std::make_pair("L1_DoubleMu0er1p5_SQ_dR_Max1p4", &L1_DoubleMu0er1p5_SQ_dR_Max1p4),          std::make_pair("L1_DoubleMu0er2_SQ_dR_Max1p4", &L1_DoubleMu0er2_SQ_dR_Max1p4),          std::make_pair("L1_DoubleMu18er2p1", &L1_DoubleMu18er2p1),          std::make_pair("L1_DoubleMu22er2p1", &L1_DoubleMu22er2p1),          std::make_pair("L1_DoubleMu3_OS_DoubleEG7p5Upsilon", &L1_DoubleMu3_OS_DoubleEG7p5Upsilon),          std::make_pair("L1_DoubleMu3_SQ_ETMHF40_Jet60_OR_DoubleJet30", &L1_DoubleMu3_SQ_ETMHF40_Jet60_OR_DoubleJet30),          std::make_pair("L1_DoubleMu3_SQ_ETMHF50_Jet60_OR_DoubleJet30", &L1_DoubleMu3_SQ_ETMHF50_Jet60_OR_DoubleJet30),          std::make_pair("L1_DoubleMu3_SQ_ETMHF60_Jet60_OR_DoubleJet30", &L1_DoubleMu3_SQ_ETMHF60_Jet60_OR_DoubleJet30),          std::make_pair("L1_DoubleMu3_SQ_ETMHF70_Jet60_OR_DoubleJet30", &L1_DoubleMu3_SQ_ETMHF70_Jet60_OR_DoubleJet30),          std::make_pair("L1_DoubleMu3_SQ_ETMHF80_Jet60_OR_DoubleJet30", &L1_DoubleMu3_SQ_ETMHF80_Jet60_OR_DoubleJet30),          std::make_pair("L1_DoubleMu3_SQ_HTT100er", &L1_DoubleMu3_SQ_HTT100er),          std::make_pair("L1_DoubleMu3_SQ_HTT200er", &L1_DoubleMu3_SQ_HTT200er),          std::make_pair("L1_DoubleMu3_SQ_HTT220er", &L1_DoubleMu3_SQ_HTT220er),          std::make_pair("L1_DoubleMu3_SQ_HTT240er", &L1_DoubleMu3_SQ_HTT240er),          std::make_pair("L1_DoubleMu4_OS_EG12", &L1_DoubleMu4_OS_EG12),          std::make_pair("L1_DoubleMu4_SQ_OS", &L1_DoubleMu4_SQ_OS),          std::make_pair("L1_DoubleMu4_SQ_OS_dR_Max1p2", &L1_DoubleMu4_SQ_OS_dR_Max1p2),          std::make_pair("L1_DoubleMu4p5_SQ", &L1_DoubleMu4p5_SQ),          std::make_pair("L1_DoubleMu4p5_SQ_OS", &L1_DoubleMu4p5_SQ_OS),          std::make_pair("L1_DoubleMu4p5_SQ_OS_dR_Max1p2", &L1_DoubleMu4p5_SQ_OS_dR_Max1p2),          std::make_pair("L1_DoubleMu4p5er2p0_SQ_OS", &L1_DoubleMu4p5er2p0_SQ_OS),          std::make_pair("L1_DoubleMu4p5er2p0_SQ_OS_Mass7to18", &L1_DoubleMu4p5er2p0_SQ_OS_Mass7to18),          std::make_pair("L1_DoubleMu5Upsilon_OS_DoubleEG3", &L1_DoubleMu5Upsilon_OS_DoubleEG3),          std::make_pair("L1_DoubleMu5_OS_EG12", &L1_DoubleMu5_OS_EG12),          std::make_pair("L1_DoubleMu5_SQ_OS", &L1_DoubleMu5_SQ_OS),          std::make_pair("L1_DoubleMu5_SQ_OS_Mass7to18", &L1_DoubleMu5_SQ_OS_Mass7to18),          std::make_pair("L1_DoubleMu6_SQ_OS", &L1_DoubleMu6_SQ_OS),          std::make_pair("L1_DoubleMu7_EG7", &L1_DoubleMu7_EG7),          std::make_pair("L1_DoubleMu7_SQ_EG7", &L1_DoubleMu7_SQ_EG7),          std::make_pair("L1_DoubleMu8_SQ", &L1_DoubleMu8_SQ),          std::make_pair("L1_DoubleMu_10_0_dEta_Max1p8", &L1_DoubleMu_10_0_dEta_Max1p8),          std::make_pair("L1_DoubleMu_11_4", &L1_DoubleMu_11_4),          std::make_pair("L1_DoubleMu_12_5", &L1_DoubleMu_12_5),          std::make_pair("L1_DoubleMu_12_8", &L1_DoubleMu_12_8),          std::make_pair("L1_DoubleMu_13_6", &L1_DoubleMu_13_6),          std::make_pair("L1_DoubleMu_15_5", &L1_DoubleMu_15_5),          std::make_pair("L1_DoubleMu_15_5_SQ", &L1_DoubleMu_15_5_SQ),          std::make_pair("L1_DoubleMu_15_7", &L1_DoubleMu_15_7),          std::make_pair("L1_DoubleMu_15_7_SQ", &L1_DoubleMu_15_7_SQ),          std::make_pair("L1_DoubleMu_15_7_SQ_Mass_Min4", &L1_DoubleMu_15_7_SQ_Mass_Min4),          std::make_pair("L1_DoubleMu_20_2_SQ_Mass_Max20", &L1_DoubleMu_20_2_SQ_Mass_Max20),          std::make_pair("L1_DoubleTau50er2p1", &L1_DoubleTau50er2p1),          std::make_pair("L1_DoubleTau70er2p1", &L1_DoubleTau70er2p1),          std::make_pair("L1_EG25er2p1_HTT125er", &L1_EG25er2p1_HTT125er),          std::make_pair("L1_EG27er2p1_HTT200er", &L1_EG27er2p1_HTT200er),          std::make_pair("L1_ETM100", &L1_ETM100),          std::make_pair("L1_ETM100_Jet60_dPhi_Min0p4", &L1_ETM100_Jet60_dPhi_Min0p4),          std::make_pair("L1_ETM105", &L1_ETM105),          std::make_pair("L1_ETM110", &L1_ETM110),          std::make_pair("L1_ETM110_Jet60_dPhi_Min0p4", &L1_ETM110_Jet60_dPhi_Min0p4),          std::make_pair("L1_ETM115", &L1_ETM115),          std::make_pair("L1_ETM120", &L1_ETM120),          std::make_pair("L1_ETM150", &L1_ETM150),          std::make_pair("L1_ETM30", &L1_ETM30),          std::make_pair("L1_ETM40", &L1_ETM40),          std::make_pair("L1_ETM50", &L1_ETM50),          std::make_pair("L1_ETM60", &L1_ETM60),          std::make_pair("L1_ETM70", &L1_ETM70),          std::make_pair("L1_ETM75", &L1_ETM75),          std::make_pair("L1_ETM75_Jet60_dPhi_Min0p4", &L1_ETM75_Jet60_dPhi_Min0p4),          std::make_pair("L1_ETM80", &L1_ETM80),          std::make_pair("L1_ETM80_Jet60_dPhi_Min0p4", &L1_ETM80_Jet60_dPhi_Min0p4),          std::make_pair("L1_ETM85", &L1_ETM85),          std::make_pair("L1_ETM90", &L1_ETM90),          std::make_pair("L1_ETM90_Jet60_dPhi_Min0p4", &L1_ETM90_Jet60_dPhi_Min0p4),          std::make_pair("L1_ETM95", &L1_ETM95),          std::make_pair("L1_ETMHF100", &L1_ETMHF100),          std::make_pair("L1_ETMHF100_HTT60er", &L1_ETMHF100_HTT60er),          std::make_pair("L1_ETMHF100_Jet60_OR_DiJet30woTT28", &L1_ETMHF100_Jet60_OR_DiJet30woTT28),          std::make_pair("L1_ETMHF100_Jet60_OR_DoubleJet30", &L1_ETMHF100_Jet60_OR_DoubleJet30),          std::make_pair("L1_ETMHF100_Jet90_OR_DoubleJet45_OR_TripleJet30", &L1_ETMHF100_Jet90_OR_DoubleJet45_OR_TripleJet30),          std::make_pair("L1_ETMHF110", &L1_ETMHF110),          std::make_pair("L1_ETMHF110_HTT60er", &L1_ETMHF110_HTT60er),          std::make_pair("L1_ETMHF110_Jet60_OR_DiJet30woTT28", &L1_ETMHF110_Jet60_OR_DiJet30woTT28),          std::make_pair("L1_ETMHF110_Jet90_OR_DoubleJet45_OR_TripleJet30", &L1_ETMHF110_Jet90_OR_DoubleJet45_OR_TripleJet30),          std::make_pair("L1_ETMHF120", &L1_ETMHF120),          std::make_pair("L1_ETMHF120_HTT60er", &L1_ETMHF120_HTT60er),          std::make_pair("L1_ETMHF120_Jet60_OR_DiJet30woTT28", &L1_ETMHF120_Jet60_OR_DiJet30woTT28),          std::make_pair("L1_ETMHF150", &L1_ETMHF150),          std::make_pair("L1_ETMHF70", &L1_ETMHF70),          std::make_pair("L1_ETMHF70_Jet90_OR_DoubleJet45_OR_TripleJet30", &L1_ETMHF70_Jet90_OR_DoubleJet45_OR_TripleJet30),          std::make_pair("L1_ETMHF80", &L1_ETMHF80),          std::make_pair("L1_ETMHF80_HTT60er", &L1_ETMHF80_HTT60er),          std::make_pair("L1_ETMHF80_Jet90_OR_DoubleJet45_OR_TripleJet30", &L1_ETMHF80_Jet90_OR_DoubleJet45_OR_TripleJet30),          std::make_pair("L1_ETMHF90", &L1_ETMHF90),          std::make_pair("L1_ETMHF90_HTT60er", &L1_ETMHF90_HTT60er),          std::make_pair("L1_ETMHF90_Jet90_OR_DoubleJet45_OR_TripleJet30", &L1_ETMHF90_Jet90_OR_DoubleJet45_OR_TripleJet30),          std::make_pair("L1_ETT100_BptxAND", &L1_ETT100_BptxAND),          std::make_pair("L1_ETT110_BptxAND", &L1_ETT110_BptxAND),          std::make_pair("L1_ETT40_BptxAND", &L1_ETT40_BptxAND),          std::make_pair("L1_ETT50_BptxAND", &L1_ETT50_BptxAND),          std::make_pair("L1_ETT60_BptxAND", &L1_ETT60_BptxAND),          std::make_pair("L1_ETT70_BptxAND", &L1_ETT70_BptxAND),          std::make_pair("L1_ETT75_BptxAND", &L1_ETT75_BptxAND),          std::make_pair("L1_ETT80_BptxAND", &L1_ETT80_BptxAND),          std::make_pair("L1_ETT85_BptxAND", &L1_ETT85_BptxAND),          std::make_pair("L1_ETT90_BptxAND", &L1_ETT90_BptxAND),          std::make_pair("L1_ETT95_BptxAND", &L1_ETT95_BptxAND),          std::make_pair("L1_FirstBunchAfterTrain", &L1_FirstBunchAfterTrain),          std::make_pair("L1_FirstBunchInTrain", &L1_FirstBunchInTrain),          std::make_pair("L1_FirstCollisionInOrbit", &L1_FirstCollisionInOrbit),          std::make_pair("L1_FirstCollisionInTrain", &L1_FirstCollisionInTrain),          std::make_pair("L1_HTT120er", &L1_HTT120er),          std::make_pair("L1_HTT160er", &L1_HTT160er),          std::make_pair("L1_HTT200er", &L1_HTT200er),          std::make_pair("L1_HTT220er", &L1_HTT220er),          std::make_pair("L1_HTT240er", &L1_HTT240er),          std::make_pair("L1_HTT250er_QuadJet_70_55_40_35_er2p5", &L1_HTT250er_QuadJet_70_55_40_35_er2p5),          std::make_pair("L1_HTT255er", &L1_HTT255er),          std::make_pair("L1_HTT270er", &L1_HTT270er),          std::make_pair("L1_HTT280er", &L1_HTT280er),          std::make_pair("L1_HTT280er_QuadJet_70_55_40_35_er2p5", &L1_HTT280er_QuadJet_70_55_40_35_er2p5),          std::make_pair("L1_HTT300er", &L1_HTT300er),          std::make_pair("L1_HTT300er_QuadJet_70_55_40_35_er2p5", &L1_HTT300er_QuadJet_70_55_40_35_er2p5),          std::make_pair("L1_HTT320er", &L1_HTT320er),          std::make_pair("L1_HTT320er_QuadJet_70_55_40_40_er2p4", &L1_HTT320er_QuadJet_70_55_40_40_er2p4),          std::make_pair("L1_HTT320er_QuadJet_70_55_40_40_er2p5", &L1_HTT320er_QuadJet_70_55_40_40_er2p5),          std::make_pair("L1_HTT320er_QuadJet_70_55_45_45_er2p5", &L1_HTT320er_QuadJet_70_55_45_45_er2p5),          std::make_pair("L1_HTT340er", &L1_HTT340er),          std::make_pair("L1_HTT340er_QuadJet_70_55_40_40_er2p5", &L1_HTT340er_QuadJet_70_55_40_40_er2p5),          std::make_pair("L1_HTT340er_QuadJet_70_55_45_45_er2p5", &L1_HTT340er_QuadJet_70_55_45_45_er2p5),          std::make_pair("L1_HTT380er", &L1_HTT380er),          std::make_pair("L1_HTT400er", &L1_HTT400er),          std::make_pair("L1_HTT450er", &L1_HTT450er),          std::make_pair("L1_HTT500er", &L1_HTT500er),          std::make_pair("L1_IsoEG33_Mt40", &L1_IsoEG33_Mt40),          std::make_pair("L1_IsoEG33_Mt44", &L1_IsoEG33_Mt44),          std::make_pair("L1_IsoEG33_Mt48", &L1_IsoEG33_Mt48),          std::make_pair("L1_IsoTau40er_ETM100", &L1_IsoTau40er_ETM100),          std::make_pair("L1_IsoTau40er_ETM105", &L1_IsoTau40er_ETM105),          std::make_pair("L1_IsoTau40er_ETM110", &L1_IsoTau40er_ETM110),          std::make_pair("L1_IsoTau40er_ETM115", &L1_IsoTau40er_ETM115),          std::make_pair("L1_IsoTau40er_ETM120", &L1_IsoTau40er_ETM120),          std::make_pair("L1_IsoTau40er_ETM80", &L1_IsoTau40er_ETM80),          std::make_pair("L1_IsoTau40er_ETM85", &L1_IsoTau40er_ETM85),          std::make_pair("L1_IsoTau40er_ETM90", &L1_IsoTau40er_ETM90),          std::make_pair("L1_IsoTau40er_ETM95", &L1_IsoTau40er_ETM95),          std::make_pair("L1_IsoTau40er_ETMHF100", &L1_IsoTau40er_ETMHF100),          std::make_pair("L1_IsoTau40er_ETMHF110", &L1_IsoTau40er_ETMHF110),          std::make_pair("L1_IsoTau40er_ETMHF120", &L1_IsoTau40er_ETMHF120),          std::make_pair("L1_IsoTau40er_ETMHF80", &L1_IsoTau40er_ETMHF80),          std::make_pair("L1_IsoTau40er_ETMHF90", &L1_IsoTau40er_ETMHF90),          std::make_pair("L1_IsolatedBunch", &L1_IsolatedBunch),          std::make_pair("L1_LastCollisionInTrain", &L1_LastCollisionInTrain),          std::make_pair("L1_LooseIsoEG22er2p1_IsoTau26er2p1_dR_Min0p3", &L1_LooseIsoEG22er2p1_IsoTau26er2p1_dR_Min0p3),          std::make_pair("L1_LooseIsoEG24er2p1_HTT100er", &L1_LooseIsoEG24er2p1_HTT100er),          std::make_pair("L1_LooseIsoEG24er2p1_IsoTau27er2p1_dR_Min0p3", &L1_LooseIsoEG24er2p1_IsoTau27er2p1_dR_Min0p3),          std::make_pair("L1_LooseIsoEG24er2p1_Jet26er2p7_dR_Min0p3", &L1_LooseIsoEG24er2p1_Jet26er2p7_dR_Min0p3),          std::make_pair("L1_LooseIsoEG24er2p1_TripleJet_26er2p7_26_26er2p7", &L1_LooseIsoEG24er2p1_TripleJet_26er2p7_26_26er2p7),          std::make_pair("L1_LooseIsoEG26er2p1_HTT100er", &L1_LooseIsoEG26er2p1_HTT100er),          std::make_pair("L1_LooseIsoEG26er2p1_Jet34er2p7_dR_Min0p3", &L1_LooseIsoEG26er2p1_Jet34er2p7_dR_Min0p3),          std::make_pair("L1_LooseIsoEG28er2p1_HTT100er", &L1_LooseIsoEG28er2p1_HTT100er),          std::make_pair("L1_LooseIsoEG28er2p1_Jet34er2p7_dR_Min0p3", &L1_LooseIsoEG28er2p1_Jet34er2p7_dR_Min0p3),          std::make_pair("L1_LooseIsoEG30er2p1_Jet34er2p7_dR_Min0p3", &L1_LooseIsoEG30er2p1_Jet34er2p7_dR_Min0p3),          std::make_pair("L1_MU20_EG15", &L1_MU20_EG15),          std::make_pair("L1_MinimumBiasHF0_AND_BptxAND", &L1_MinimumBiasHF0_AND_BptxAND),          std::make_pair("L1_MinimumBiasHF0_OR_BptxAND", &L1_MinimumBiasHF0_OR_BptxAND),          std::make_pair("L1_Mu10er2p1_ETM30", &L1_Mu10er2p1_ETM30),          std::make_pair("L1_Mu10er2p3_Jet32er2p3_dR_Max0p4_DoubleJet32er2p3_dEta_Max1p6", &L1_Mu10er2p3_Jet32er2p3_dR_Max0p4_DoubleJet32er2p3_dEta_Max1p6),          std::make_pair("L1_Mu12_EG10", &L1_Mu12_EG10),          std::make_pair("L1_Mu12er2p3_Jet40er2p3_dR_Max0p4_DoubleJet40er2p3_dEta_Max1p6", &L1_Mu12er2p3_Jet40er2p3_dR_Max0p4_DoubleJet40er2p3_dEta_Max1p6),          std::make_pair("L1_Mu14er2p1_ETM30", &L1_Mu14er2p1_ETM30),          std::make_pair("L1_Mu15_HTT100er", &L1_Mu15_HTT100er),          std::make_pair("L1_Mu18_HTT100er", &L1_Mu18_HTT100er),          std::make_pair("L1_Mu18_Jet24er2p7", &L1_Mu18_Jet24er2p7),          std::make_pair("L1_Mu18er2p1_IsoTau26er2p1", &L1_Mu18er2p1_IsoTau26er2p1),          std::make_pair("L1_Mu18er2p1_Tau24er2p1", &L1_Mu18er2p1_Tau24er2p1),          std::make_pair("L1_Mu20_EG10", &L1_Mu20_EG10),          std::make_pair("L1_Mu20_EG17", &L1_Mu20_EG17),          std::make_pair("L1_Mu20_LooseIsoEG6", &L1_Mu20_LooseIsoEG6),          std::make_pair("L1_Mu20er2p1_IsoTau26er2p1", &L1_Mu20er2p1_IsoTau26er2p1),          std::make_pair("L1_Mu20er2p1_IsoTau27er2p1", &L1_Mu20er2p1_IsoTau27er2p1),          std::make_pair("L1_Mu22er2p1_IsoTau28er2p1", &L1_Mu22er2p1_IsoTau28er2p1),          std::make_pair("L1_Mu22er2p1_IsoTau30er2p1", &L1_Mu22er2p1_IsoTau30er2p1),          std::make_pair("L1_Mu22er2p1_IsoTau32er2p1", &L1_Mu22er2p1_IsoTau32er2p1),          std::make_pair("L1_Mu22er2p1_IsoTau33er2p1", &L1_Mu22er2p1_IsoTau33er2p1),          std::make_pair("L1_Mu22er2p1_IsoTau34er2p1", &L1_Mu22er2p1_IsoTau34er2p1),          std::make_pair("L1_Mu22er2p1_IsoTau35er2p1", &L1_Mu22er2p1_IsoTau35er2p1),          std::make_pair("L1_Mu22er2p1_IsoTau36er2p1", &L1_Mu22er2p1_IsoTau36er2p1),          std::make_pair("L1_Mu22er2p1_IsoTau38er2p1", &L1_Mu22er2p1_IsoTau38er2p1),          std::make_pair("L1_Mu22er2p1_IsoTau40er2p1", &L1_Mu22er2p1_IsoTau40er2p1),          std::make_pair("L1_Mu22er2p1_Tau50er2p1", &L1_Mu22er2p1_Tau50er2p1),          std::make_pair("L1_Mu22er2p1_Tau70er2p1", &L1_Mu22er2p1_Tau70er2p1),          std::make_pair("L1_Mu23_EG10", &L1_Mu23_EG10),          std::make_pair("L1_Mu23_LooseIsoEG10", &L1_Mu23_LooseIsoEG10),          std::make_pair("L1_Mu3_Jet120er2p7_dEta_Max0p4_dPhi_Max0p4", &L1_Mu3_Jet120er2p7_dEta_Max0p4_dPhi_Max0p4),          std::make_pair("L1_Mu3_Jet16er2p7_dEta_Max0p4_dPhi_Max0p4", &L1_Mu3_Jet16er2p7_dEta_Max0p4_dPhi_Max0p4),          std::make_pair("L1_Mu3_Jet30er2p5", &L1_Mu3_Jet30er2p5),          std::make_pair("L1_Mu3_Jet60er2p7_dEta_Max0p4_dPhi_Max0p4", &L1_Mu3_Jet60er2p7_dEta_Max0p4_dPhi_Max0p4),          std::make_pair("L1_Mu5_EG15", &L1_Mu5_EG15),          std::make_pair("L1_Mu5_EG20", &L1_Mu5_EG20),          std::make_pair("L1_Mu5_EG23", &L1_Mu5_EG23),          std::make_pair("L1_Mu5_LooseIsoEG18", &L1_Mu5_LooseIsoEG18),          std::make_pair("L1_Mu5_LooseIsoEG20", &L1_Mu5_LooseIsoEG20),          std::make_pair("L1_Mu6_DoubleEG10", &L1_Mu6_DoubleEG10),          std::make_pair("L1_Mu6_DoubleEG17", &L1_Mu6_DoubleEG17),          std::make_pair("L1_Mu6_HTT200er", &L1_Mu6_HTT200er),          std::make_pair("L1_Mu6_HTT240er", &L1_Mu6_HTT240er),          std::make_pair("L1_Mu6_HTT250er", &L1_Mu6_HTT250er),          std::make_pair("L1_Mu7_EG23", &L1_Mu7_EG23),          std::make_pair("L1_Mu7_LooseIsoEG20", &L1_Mu7_LooseIsoEG20),          std::make_pair("L1_Mu7_LooseIsoEG23", &L1_Mu7_LooseIsoEG23),          std::make_pair("L1_Mu8_HTT150er", &L1_Mu8_HTT150er),          std::make_pair("L1_NotBptxOR", &L1_NotBptxOR),          std::make_pair("L1_QuadJet36er2p7_IsoTau52er2p1", &L1_QuadJet36er2p7_IsoTau52er2p1),          std::make_pair("L1_QuadJet36er2p7_Tau52", &L1_QuadJet36er2p7_Tau52),          std::make_pair("L1_QuadJet40er2p7", &L1_QuadJet40er2p7),          std::make_pair("L1_QuadJet50er2p7", &L1_QuadJet50er2p7),          std::make_pair("L1_QuadJet60er2p7", &L1_QuadJet60er2p7),          std::make_pair("L1_QuadMu0", &L1_QuadMu0),          std::make_pair("L1_SingleEG10", &L1_SingleEG10),          std::make_pair("L1_SingleEG15", &L1_SingleEG15),          std::make_pair("L1_SingleEG18", &L1_SingleEG18),          std::make_pair("L1_SingleEG24", &L1_SingleEG24),          std::make_pair("L1_SingleEG26", &L1_SingleEG26),          std::make_pair("L1_SingleEG28", &L1_SingleEG28),          std::make_pair("L1_SingleEG2_BptxAND", &L1_SingleEG2_BptxAND),          std::make_pair("L1_SingleEG30", &L1_SingleEG30),          std::make_pair("L1_SingleEG32", &L1_SingleEG32),          std::make_pair("L1_SingleEG34", &L1_SingleEG34),          std::make_pair("L1_SingleEG34er2p1", &L1_SingleEG34er2p1),          std::make_pair("L1_SingleEG36", &L1_SingleEG36),          std::make_pair("L1_SingleEG36er2p1", &L1_SingleEG36er2p1),          std::make_pair("L1_SingleEG38", &L1_SingleEG38),          std::make_pair("L1_SingleEG38er2p1", &L1_SingleEG38er2p1),          std::make_pair("L1_SingleEG40", &L1_SingleEG40),          std::make_pair("L1_SingleEG42", &L1_SingleEG42),          std::make_pair("L1_SingleEG45", &L1_SingleEG45),          std::make_pair("L1_SingleEG5", &L1_SingleEG5),          std::make_pair("L1_SingleEG50", &L1_SingleEG50),          std::make_pair("L1_SingleIsoEG18", &L1_SingleIsoEG18),          std::make_pair("L1_SingleIsoEG18er2p1", &L1_SingleIsoEG18er2p1),          std::make_pair("L1_SingleIsoEG20", &L1_SingleIsoEG20),          std::make_pair("L1_SingleIsoEG20er2p1", &L1_SingleIsoEG20er2p1),          std::make_pair("L1_SingleIsoEG22", &L1_SingleIsoEG22),          std::make_pair("L1_SingleIsoEG22er2p1", &L1_SingleIsoEG22er2p1),          std::make_pair("L1_SingleIsoEG24", &L1_SingleIsoEG24),          std::make_pair("L1_SingleIsoEG24er2p1", &L1_SingleIsoEG24er2p1),          std::make_pair("L1_SingleIsoEG26", &L1_SingleIsoEG26),          std::make_pair("L1_SingleIsoEG26er2p1", &L1_SingleIsoEG26er2p1),          std::make_pair("L1_SingleIsoEG28", &L1_SingleIsoEG28),          std::make_pair("L1_SingleIsoEG28er2p1", &L1_SingleIsoEG28er2p1),          std::make_pair("L1_SingleIsoEG30", &L1_SingleIsoEG30),          std::make_pair("L1_SingleIsoEG30er2p1", &L1_SingleIsoEG30er2p1),          std::make_pair("L1_SingleIsoEG32", &L1_SingleIsoEG32),          std::make_pair("L1_SingleIsoEG32er2p1", &L1_SingleIsoEG32er2p1),          std::make_pair("L1_SingleIsoEG33er2p1", &L1_SingleIsoEG33er2p1),          std::make_pair("L1_SingleIsoEG34", &L1_SingleIsoEG34),          std::make_pair("L1_SingleIsoEG34er2p1", &L1_SingleIsoEG34er2p1),          std::make_pair("L1_SingleIsoEG35", &L1_SingleIsoEG35),          std::make_pair("L1_SingleIsoEG35er2p1", &L1_SingleIsoEG35er2p1),          std::make_pair("L1_SingleIsoEG36", &L1_SingleIsoEG36),          std::make_pair("L1_SingleIsoEG36er2p1", &L1_SingleIsoEG36er2p1),          std::make_pair("L1_SingleIsoEG37", &L1_SingleIsoEG37),          std::make_pair("L1_SingleIsoEG38", &L1_SingleIsoEG38),          std::make_pair("L1_SingleIsoEG38er2p1", &L1_SingleIsoEG38er2p1),          std::make_pair("L1_SingleIsoEG40", &L1_SingleIsoEG40),          std::make_pair("L1_SingleIsoEG40er2p1", &L1_SingleIsoEG40er2p1),          std::make_pair("L1_SingleJet120", &L1_SingleJet120),          std::make_pair("L1_SingleJet120_FWD", &L1_SingleJet120_FWD),          std::make_pair("L1_SingleJet12_BptxAND", &L1_SingleJet12_BptxAND),          std::make_pair("L1_SingleJet140", &L1_SingleJet140),          std::make_pair("L1_SingleJet150", &L1_SingleJet150),          std::make_pair("L1_SingleJet16", &L1_SingleJet16),          std::make_pair("L1_SingleJet160", &L1_SingleJet160),          std::make_pair("L1_SingleJet170", &L1_SingleJet170),          std::make_pair("L1_SingleJet180", &L1_SingleJet180),          std::make_pair("L1_SingleJet20", &L1_SingleJet20),          std::make_pair("L1_SingleJet200", &L1_SingleJet200),          std::make_pair("L1_SingleJet20er2p7_NotBptxOR", &L1_SingleJet20er2p7_NotBptxOR),          std::make_pair("L1_SingleJet20er2p7_NotBptxOR_3BX", &L1_SingleJet20er2p7_NotBptxOR_3BX),          std::make_pair("L1_SingleJet35", &L1_SingleJet35),          std::make_pair("L1_SingleJet35_FWD", &L1_SingleJet35_FWD),          std::make_pair("L1_SingleJet35_HFm", &L1_SingleJet35_HFm),          std::make_pair("L1_SingleJet35_HFp", &L1_SingleJet35_HFp),          std::make_pair("L1_SingleJet43er2p7_NotBptxOR_3BX", &L1_SingleJet43er2p7_NotBptxOR_3BX),          std::make_pair("L1_SingleJet46er2p7_NotBptxOR_3BX", &L1_SingleJet46er2p7_NotBptxOR_3BX),          std::make_pair("L1_SingleJet60", &L1_SingleJet60),          std::make_pair("L1_SingleJet60_FWD", &L1_SingleJet60_FWD),          std::make_pair("L1_SingleJet60_HFm", &L1_SingleJet60_HFm),          std::make_pair("L1_SingleJet60_HFp", &L1_SingleJet60_HFp),          std::make_pair("L1_SingleJet90", &L1_SingleJet90),          std::make_pair("L1_SingleJet90_FWD", &L1_SingleJet90_FWD),          std::make_pair("L1_SingleMu0_BMTF", &L1_SingleMu0_BMTF),          std::make_pair("L1_SingleMu0_EMTF", &L1_SingleMu0_EMTF),          std::make_pair("L1_SingleMu0_OMTF", &L1_SingleMu0_OMTF),          std::make_pair("L1_SingleMu10_LowQ", &L1_SingleMu10_LowQ),          std::make_pair("L1_SingleMu11_LowQ", &L1_SingleMu11_LowQ),          std::make_pair("L1_SingleMu12_LowQ_BMTF", &L1_SingleMu12_LowQ_BMTF),          std::make_pair("L1_SingleMu12_LowQ_EMTF", &L1_SingleMu12_LowQ_EMTF),          std::make_pair("L1_SingleMu12_LowQ_OMTF", &L1_SingleMu12_LowQ_OMTF),          std::make_pair("L1_SingleMu14er2p1", &L1_SingleMu14er2p1),          std::make_pair("L1_SingleMu16", &L1_SingleMu16),          std::make_pair("L1_SingleMu16er2p1", &L1_SingleMu16er2p1),          std::make_pair("L1_SingleMu18", &L1_SingleMu18),          std::make_pair("L1_SingleMu18er2p1", &L1_SingleMu18er2p1),          std::make_pair("L1_SingleMu20", &L1_SingleMu20),          std::make_pair("L1_SingleMu20er2p1", &L1_SingleMu20er2p1),          std::make_pair("L1_SingleMu22", &L1_SingleMu22),          std::make_pair("L1_SingleMu22_BMTF", &L1_SingleMu22_BMTF),          std::make_pair("L1_SingleMu22_EMTF", &L1_SingleMu22_EMTF),          std::make_pair("L1_SingleMu22_OMTF", &L1_SingleMu22_OMTF),          std::make_pair("L1_SingleMu22er2p1", &L1_SingleMu22er2p1),          std::make_pair("L1_SingleMu25", &L1_SingleMu25),          std::make_pair("L1_SingleMu3", &L1_SingleMu3),          std::make_pair("L1_SingleMu30", &L1_SingleMu30),          std::make_pair("L1_SingleMu3er1p5_SingleJet100er2p5_ETMHF40", &L1_SingleMu3er1p5_SingleJet100er2p5_ETMHF40),          std::make_pair("L1_SingleMu5", &L1_SingleMu5),          std::make_pair("L1_SingleMu7", &L1_SingleMu7),          std::make_pair("L1_SingleMuCosmics", &L1_SingleMuCosmics),          std::make_pair("L1_SingleMuCosmics_BMTF", &L1_SingleMuCosmics_BMTF),          std::make_pair("L1_SingleMuCosmics_EMTF", &L1_SingleMuCosmics_EMTF),          std::make_pair("L1_SingleMuCosmics_OMTF", &L1_SingleMuCosmics_OMTF),          std::make_pair("L1_SingleMuOpen", &L1_SingleMuOpen),          std::make_pair("L1_SingleMuOpen_NotBptxOR", &L1_SingleMuOpen_NotBptxOR),          std::make_pair("L1_SingleMuOpen_NotBptxOR_3BX", &L1_SingleMuOpen_NotBptxOR_3BX),          std::make_pair("L1_SingleTau100er2p1", &L1_SingleTau100er2p1),          std::make_pair("L1_SingleTau120er2p1", &L1_SingleTau120er2p1),          std::make_pair("L1_SingleTau130er2p1", &L1_SingleTau130er2p1),          std::make_pair("L1_SingleTau140er2p1", &L1_SingleTau140er2p1),          std::make_pair("L1_SingleTau20", &L1_SingleTau20),          std::make_pair("L1_SingleTau80er2p1", &L1_SingleTau80er2p1),          std::make_pair("L1_TripleEG_14_10_8", &L1_TripleEG_14_10_8),          std::make_pair("L1_TripleEG_18_17_8", &L1_TripleEG_18_17_8),          std::make_pair("L1_TripleEG_LooseIso20_10_5", &L1_TripleEG_LooseIso20_10_5),          std::make_pair("L1_TripleJet_100_85_72_VBF", &L1_TripleJet_100_85_72_VBF),          std::make_pair("L1_TripleJet_105_85_76_VBF", &L1_TripleJet_105_85_76_VBF),          std::make_pair("L1_TripleJet_84_68_48_VBF", &L1_TripleJet_84_68_48_VBF),          std::make_pair("L1_TripleJet_88_72_56_VBF", &L1_TripleJet_88_72_56_VBF),          std::make_pair("L1_TripleJet_92_76_64_VBF", &L1_TripleJet_92_76_64_VBF),          std::make_pair("L1_TripleJet_98_83_71_VBF", &L1_TripleJet_98_83_71_VBF),          std::make_pair("L1_TripleMu0", &L1_TripleMu0),          std::make_pair("L1_TripleMu0_OQ", &L1_TripleMu0_OQ),          std::make_pair("L1_TripleMu3", &L1_TripleMu3),          std::make_pair("L1_TripleMu3_SQ", &L1_TripleMu3_SQ),          std::make_pair("L1_TripleMu_4_4_4", &L1_TripleMu_4_4_4),          std::make_pair("L1_TripleMu_5OQ_3p5OQ_2p5OQ_DoubleMu_5_2p5_OQ_OS_Mass_5to17", &L1_TripleMu_5OQ_3p5OQ_2p5OQ_DoubleMu_5_2p5_OQ_OS_Mass_5to17),          std::make_pair("L1_TripleMu_5OQ_3p5OQ_2p5OQ_DoubleMu_5_2p5_OQ_OS_Mass_8to14", &L1_TripleMu_5OQ_3p5OQ_2p5OQ_DoubleMu_5_2p5_OQ_OS_Mass_8to14),          std::make_pair("L1_TripleMu_5SQ_3SQ_0OQ", &L1_TripleMu_5SQ_3SQ_0OQ),          std::make_pair("L1_TripleMu_5SQ_3SQ_0OQ_DoubleMu_5_3_SQ_OS_Mass_Max9", &L1_TripleMu_5SQ_3SQ_0OQ_DoubleMu_5_3_SQ_OS_Mass_Max9),          std::make_pair("L1_TripleMu_5SQ_3SQ_0_DoubleMu_5_3_SQ_OS_Mass_Max9", &L1_TripleMu_5SQ_3SQ_0_DoubleMu_5_3_SQ_OS_Mass_Max9),          std::make_pair("L1_TripleMu_5_0_0", &L1_TripleMu_5_0_0),          std::make_pair("L1_TripleMu_5_3_3", &L1_TripleMu_5_3_3),          std::make_pair("L1_TripleMu_5_3p5_2p5", &L1_TripleMu_5_3p5_2p5),          std::make_pair("L1_TripleMu_5_3p5_2p5_DoubleMu_5_2p5_OS_Mass_5to17", &L1_TripleMu_5_3p5_2p5_DoubleMu_5_2p5_OS_Mass_5to17),          std::make_pair("L1_TripleMu_5_4_2p5_DoubleMu_5_2p5_OS_Mass_5to17", &L1_TripleMu_5_4_2p5_DoubleMu_5_2p5_OS_Mass_5to17),          std::make_pair("L1_TripleMu_5_5_3", &L1_TripleMu_5_5_3),          std::make_pair("L1_UnpairedBunchBptxMinus", &L1_UnpairedBunchBptxMinus),          std::make_pair("L1_UnpairedBunchBptxPlus", &L1_UnpairedBunchBptxPlus),          std::make_pair("L1_ZeroBias", &L1_ZeroBias),          std::make_pair("L1_ZeroBias_copy", &L1_ZeroBias_copy)      };

  static const std::map<std::string, AlgorithmFunction> Name2Func(name2func, name2func + sizeof(name2func) / sizeof(name2func[0]));
  const std::map<std::string, AlgorithmFunction>::const_iterator rc = Name2Func.find(name);
  AlgorithmFunction fp = 0;
  if (rc != Name2Func.end()) fp = rc->second;
  if (fp == 0)
  {
    std::stringstream ss;
    ss << "fat> algorithm '" << name << "' is not defined in L1Menu_Collisions2017_v4slim_my_SoftMuPlusHardJet_FullMenu_v1\n";
    throw std::runtime_error(ss.str());
  }
  return fp;
}


bool addFuncFromName(std::map<std::string, std::function<bool()>> &L1SeedFun,
                     L1Analysis::L1AnalysisL1UpgradeDataFormat* upgrade,
                     L1Analysis::L1AnalysisL1CaloTowerDataFormat* calo_tower)
{
  static const std::pair<std::string, AlgorithmFunction> name2func[] = {
          std::make_pair("L1_AlwaysTrue", &L1_AlwaysTrue),          std::make_pair("L1_BPTX_AND_Ref1_VME", &L1_BPTX_AND_Ref1_VME),          std::make_pair("L1_BPTX_AND_Ref3_VME", &L1_BPTX_AND_Ref3_VME),          std::make_pair("L1_BPTX_AND_Ref4_VME", &L1_BPTX_AND_Ref4_VME),          std::make_pair("L1_BPTX_BeamGas_B1_VME", &L1_BPTX_BeamGas_B1_VME),          std::make_pair("L1_BPTX_BeamGas_B2_VME", &L1_BPTX_BeamGas_B2_VME),          std::make_pair("L1_BPTX_BeamGas_Ref1_VME", &L1_BPTX_BeamGas_Ref1_VME),          std::make_pair("L1_BPTX_BeamGas_Ref2_VME", &L1_BPTX_BeamGas_Ref2_VME),          std::make_pair("L1_BPTX_NotOR_VME", &L1_BPTX_NotOR_VME),          std::make_pair("L1_BPTX_OR_Ref3_VME", &L1_BPTX_OR_Ref3_VME),          std::make_pair("L1_BPTX_OR_Ref4_VME", &L1_BPTX_OR_Ref4_VME),          std::make_pair("L1_BPTX_RefAND_VME", &L1_BPTX_RefAND_VME),          std::make_pair("L1_BptxMinus", &L1_BptxMinus),          std::make_pair("L1_BptxOR", &L1_BptxOR),          std::make_pair("L1_BptxPlus", &L1_BptxPlus),          std::make_pair("L1_BptxXOR", &L1_BptxXOR),          std::make_pair("L1_CDC_SingleMu_3_er1p2_TOP120_DPHI2p618_3p142", &L1_CDC_SingleMu_3_er1p2_TOP120_DPHI2p618_3p142),          std::make_pair("L1_DoubleEG6_HTT240er", &L1_DoubleEG6_HTT240er),          std::make_pair("L1_DoubleEG6_HTT250er", &L1_DoubleEG6_HTT250er),          std::make_pair("L1_DoubleEG6_HTT255er", &L1_DoubleEG6_HTT255er),          std::make_pair("L1_DoubleEG6_HTT270er", &L1_DoubleEG6_HTT270er),          std::make_pair("L1_DoubleEG6_HTT300er", &L1_DoubleEG6_HTT300er),          std::make_pair("L1_DoubleEG8er2p6_HTT255er", &L1_DoubleEG8er2p6_HTT255er),          std::make_pair("L1_DoubleEG8er2p6_HTT270er", &L1_DoubleEG8er2p6_HTT270er),          std::make_pair("L1_DoubleEG8er2p6_HTT300er", &L1_DoubleEG8er2p6_HTT300er),          std::make_pair("L1_DoubleEG_15_10", &L1_DoubleEG_15_10),          std::make_pair("L1_DoubleEG_18_17", &L1_DoubleEG_18_17),          std::make_pair("L1_DoubleEG_20_18", &L1_DoubleEG_20_18),          std::make_pair("L1_DoubleEG_22_10", &L1_DoubleEG_22_10),          std::make_pair("L1_DoubleEG_22_12", &L1_DoubleEG_22_12),          std::make_pair("L1_DoubleEG_22_15", &L1_DoubleEG_22_15),          std::make_pair("L1_DoubleEG_23_10", &L1_DoubleEG_23_10),          std::make_pair("L1_DoubleEG_24_17", &L1_DoubleEG_24_17),          std::make_pair("L1_DoubleEG_25_12", &L1_DoubleEG_25_12),          std::make_pair("L1_DoubleEG_25_13", &L1_DoubleEG_25_13),          std::make_pair("L1_DoubleEG_25_14", &L1_DoubleEG_25_14),          std::make_pair("L1_DoubleEG_LooseIso23_10", &L1_DoubleEG_LooseIso23_10),          std::make_pair("L1_DoubleEG_LooseIso24_10", &L1_DoubleEG_LooseIso24_10),          std::make_pair("L1_DoubleIsoTau28er2p1", &L1_DoubleIsoTau28er2p1),          std::make_pair("L1_DoubleIsoTau30er2p1", &L1_DoubleIsoTau30er2p1),          std::make_pair("L1_DoubleIsoTau32er2p1", &L1_DoubleIsoTau32er2p1),          std::make_pair("L1_DoubleIsoTau33er2p1", &L1_DoubleIsoTau33er2p1),          std::make_pair("L1_DoubleIsoTau34er2p1", &L1_DoubleIsoTau34er2p1),          std::make_pair("L1_DoubleIsoTau35er2p1", &L1_DoubleIsoTau35er2p1),          std::make_pair("L1_DoubleIsoTau36er2p1", &L1_DoubleIsoTau36er2p1),          std::make_pair("L1_DoubleIsoTau38er2p1", &L1_DoubleIsoTau38er2p1),          std::make_pair("L1_DoubleJet100er2p3_dEta_Max1p6", &L1_DoubleJet100er2p3_dEta_Max1p6),          std::make_pair("L1_DoubleJet100er2p7", &L1_DoubleJet100er2p7),          std::make_pair("L1_DoubleJet112er2p3_dEta_Max1p6", &L1_DoubleJet112er2p3_dEta_Max1p6),          std::make_pair("L1_DoubleJet112er2p7", &L1_DoubleJet112er2p7),          std::make_pair("L1_DoubleJet120er2p7", &L1_DoubleJet120er2p7),          std::make_pair("L1_DoubleJet150er2p7", &L1_DoubleJet150er2p7),          std::make_pair("L1_DoubleJet30_Mass_Min300_dEta_Max1p5", &L1_DoubleJet30_Mass_Min300_dEta_Max1p5),          std::make_pair("L1_DoubleJet30_Mass_Min320_dEta_Max1p5", &L1_DoubleJet30_Mass_Min320_dEta_Max1p5),          std::make_pair("L1_DoubleJet30_Mass_Min340_dEta_Max1p5", &L1_DoubleJet30_Mass_Min340_dEta_Max1p5),          std::make_pair("L1_DoubleJet30_Mass_Min360_dEta_Max1p5", &L1_DoubleJet30_Mass_Min360_dEta_Max1p5),          std::make_pair("L1_DoubleJet30_Mass_Min380_dEta_Max1p5", &L1_DoubleJet30_Mass_Min380_dEta_Max1p5),          std::make_pair("L1_DoubleJet30_Mass_Min400_Mu10", &L1_DoubleJet30_Mass_Min400_Mu10),          std::make_pair("L1_DoubleJet30_Mass_Min400_Mu6", &L1_DoubleJet30_Mass_Min400_Mu6),          std::make_pair("L1_DoubleJet30_Mass_Min400_dEta_Max1p5", &L1_DoubleJet30_Mass_Min400_dEta_Max1p5),          std::make_pair("L1_DoubleJet35_rmovlp_IsoTau45_Mass_Min450", &L1_DoubleJet35_rmovlp_IsoTau45_Mass_Min450),          std::make_pair("L1_DoubleJet40er2p7", &L1_DoubleJet40er2p7),          std::make_pair("L1_DoubleJet50er2p7", &L1_DoubleJet50er2p7),          std::make_pair("L1_DoubleJet60er2p7", &L1_DoubleJet60er2p7),          std::make_pair("L1_DoubleJet60er2p7_ETM100", &L1_DoubleJet60er2p7_ETM100),          std::make_pair("L1_DoubleJet60er2p7_ETM60", &L1_DoubleJet60er2p7_ETM60),          std::make_pair("L1_DoubleJet60er2p7_ETM70", &L1_DoubleJet60er2p7_ETM70),          std::make_pair("L1_DoubleJet60er2p7_ETM80", &L1_DoubleJet60er2p7_ETM80),          std::make_pair("L1_DoubleJet60er2p7_ETM90", &L1_DoubleJet60er2p7_ETM90),          std::make_pair("L1_DoubleJet80er2p7", &L1_DoubleJet80er2p7),          std::make_pair("L1_DoubleJet_100_30_DoubleJet30_Mass_Min620", &L1_DoubleJet_100_30_DoubleJet30_Mass_Min620),          std::make_pair("L1_DoubleJet_100_35_DoubleJet35_Mass_Min620", &L1_DoubleJet_100_35_DoubleJet35_Mass_Min620),          std::make_pair("L1_DoubleJet_110_35_DoubleJet35_Mass_Min620", &L1_DoubleJet_110_35_DoubleJet35_Mass_Min620),          std::make_pair("L1_DoubleJet_110_40_DoubleJet40_Mass_Min620", &L1_DoubleJet_110_40_DoubleJet40_Mass_Min620),          std::make_pair("L1_DoubleJet_115_35_DoubleJet35_Mass_Min620", &L1_DoubleJet_115_35_DoubleJet35_Mass_Min620),          std::make_pair("L1_DoubleJet_115_40_DoubleJet40_Mass_Min620", &L1_DoubleJet_115_40_DoubleJet40_Mass_Min620),          std::make_pair("L1_DoubleJet_90_30_DoubleJet30_Mass_Min620", &L1_DoubleJet_90_30_DoubleJet30_Mass_Min620),          std::make_pair("L1_DoubleLooseIsoEG22er2p1", &L1_DoubleLooseIsoEG22er2p1),          std::make_pair("L1_DoubleLooseIsoEG24er2p1", &L1_DoubleLooseIsoEG24er2p1),          std::make_pair("L1_DoubleMu0", &L1_DoubleMu0),          std::make_pair("L1_DoubleMu0_ETM40", &L1_DoubleMu0_ETM40),          std::make_pair("L1_DoubleMu0_ETM55", &L1_DoubleMu0_ETM55),          std::make_pair("L1_DoubleMu0_ETM60", &L1_DoubleMu0_ETM60),          std::make_pair("L1_DoubleMu0_ETM65", &L1_DoubleMu0_ETM65),          std::make_pair("L1_DoubleMu0_ETM70", &L1_DoubleMu0_ETM70),          std::make_pair("L1_DoubleMu0_SQ", &L1_DoubleMu0_SQ),          std::make_pair("L1_DoubleMu0_SQ_OS", &L1_DoubleMu0_SQ_OS),          std::make_pair("L1_DoubleMu0er1p4_SQ_OS_dR_Max1p4", &L1_DoubleMu0er1p4_SQ_OS_dR_Max1p4),          std::make_pair("L1_DoubleMu0er1p4_dEta_Max1p8_OS", &L1_DoubleMu0er1p4_dEta_Max1p8_OS),          std::make_pair("L1_DoubleMu0er1p5_SQ_OS", &L1_DoubleMu0er1p5_SQ_OS),          std::make_pair("L1_DoubleMu0er1p5_SQ_OS_dR_Max1p4", &L1_DoubleMu0er1p5_SQ_OS_dR_Max1p4),          std::make_pair("L1_DoubleMu0er1p5_SQ_dR_Max1p4", &L1_DoubleMu0er1p5_SQ_dR_Max1p4),          std::make_pair("L1_DoubleMu0er2_SQ_dR_Max1p4", &L1_DoubleMu0er2_SQ_dR_Max1p4),          std::make_pair("L1_DoubleMu18er2p1", &L1_DoubleMu18er2p1),          std::make_pair("L1_DoubleMu22er2p1", &L1_DoubleMu22er2p1),          std::make_pair("L1_DoubleMu3_OS_DoubleEG7p5Upsilon", &L1_DoubleMu3_OS_DoubleEG7p5Upsilon),          std::make_pair("L1_DoubleMu3_SQ_ETMHF40_Jet60_OR_DoubleJet30", &L1_DoubleMu3_SQ_ETMHF40_Jet60_OR_DoubleJet30),          std::make_pair("L1_DoubleMu3_SQ_ETMHF50_Jet60_OR_DoubleJet30", &L1_DoubleMu3_SQ_ETMHF50_Jet60_OR_DoubleJet30),          std::make_pair("L1_DoubleMu3_SQ_ETMHF60_Jet60_OR_DoubleJet30", &L1_DoubleMu3_SQ_ETMHF60_Jet60_OR_DoubleJet30),          std::make_pair("L1_DoubleMu3_SQ_ETMHF70_Jet60_OR_DoubleJet30", &L1_DoubleMu3_SQ_ETMHF70_Jet60_OR_DoubleJet30),          std::make_pair("L1_DoubleMu3_SQ_ETMHF80_Jet60_OR_DoubleJet30", &L1_DoubleMu3_SQ_ETMHF80_Jet60_OR_DoubleJet30),          std::make_pair("L1_DoubleMu3_SQ_HTT100er", &L1_DoubleMu3_SQ_HTT100er),          std::make_pair("L1_DoubleMu3_SQ_HTT200er", &L1_DoubleMu3_SQ_HTT200er),          std::make_pair("L1_DoubleMu3_SQ_HTT220er", &L1_DoubleMu3_SQ_HTT220er),          std::make_pair("L1_DoubleMu3_SQ_HTT240er", &L1_DoubleMu3_SQ_HTT240er),          std::make_pair("L1_DoubleMu4_OS_EG12", &L1_DoubleMu4_OS_EG12),          std::make_pair("L1_DoubleMu4_SQ_OS", &L1_DoubleMu4_SQ_OS),          std::make_pair("L1_DoubleMu4_SQ_OS_dR_Max1p2", &L1_DoubleMu4_SQ_OS_dR_Max1p2),          std::make_pair("L1_DoubleMu4p5_SQ", &L1_DoubleMu4p5_SQ),          std::make_pair("L1_DoubleMu4p5_SQ_OS", &L1_DoubleMu4p5_SQ_OS),          std::make_pair("L1_DoubleMu4p5_SQ_OS_dR_Max1p2", &L1_DoubleMu4p5_SQ_OS_dR_Max1p2),          std::make_pair("L1_DoubleMu4p5er2p0_SQ_OS", &L1_DoubleMu4p5er2p0_SQ_OS),          std::make_pair("L1_DoubleMu4p5er2p0_SQ_OS_Mass7to18", &L1_DoubleMu4p5er2p0_SQ_OS_Mass7to18),          std::make_pair("L1_DoubleMu5Upsilon_OS_DoubleEG3", &L1_DoubleMu5Upsilon_OS_DoubleEG3),          std::make_pair("L1_DoubleMu5_OS_EG12", &L1_DoubleMu5_OS_EG12),          std::make_pair("L1_DoubleMu5_SQ_OS", &L1_DoubleMu5_SQ_OS),          std::make_pair("L1_DoubleMu5_SQ_OS_Mass7to18", &L1_DoubleMu5_SQ_OS_Mass7to18),          std::make_pair("L1_DoubleMu6_SQ_OS", &L1_DoubleMu6_SQ_OS),          std::make_pair("L1_DoubleMu7_EG7", &L1_DoubleMu7_EG7),          std::make_pair("L1_DoubleMu7_SQ_EG7", &L1_DoubleMu7_SQ_EG7),          std::make_pair("L1_DoubleMu8_SQ", &L1_DoubleMu8_SQ),          std::make_pair("L1_DoubleMu_10_0_dEta_Max1p8", &L1_DoubleMu_10_0_dEta_Max1p8),          std::make_pair("L1_DoubleMu_11_4", &L1_DoubleMu_11_4),          std::make_pair("L1_DoubleMu_12_5", &L1_DoubleMu_12_5),          std::make_pair("L1_DoubleMu_12_8", &L1_DoubleMu_12_8),          std::make_pair("L1_DoubleMu_13_6", &L1_DoubleMu_13_6),          std::make_pair("L1_DoubleMu_15_5", &L1_DoubleMu_15_5),          std::make_pair("L1_DoubleMu_15_5_SQ", &L1_DoubleMu_15_5_SQ),          std::make_pair("L1_DoubleMu_15_7", &L1_DoubleMu_15_7),          std::make_pair("L1_DoubleMu_15_7_SQ", &L1_DoubleMu_15_7_SQ),          std::make_pair("L1_DoubleMu_15_7_SQ_Mass_Min4", &L1_DoubleMu_15_7_SQ_Mass_Min4),          std::make_pair("L1_DoubleMu_20_2_SQ_Mass_Max20", &L1_DoubleMu_20_2_SQ_Mass_Max20),          std::make_pair("L1_DoubleTau50er2p1", &L1_DoubleTau50er2p1),          std::make_pair("L1_DoubleTau70er2p1", &L1_DoubleTau70er2p1),          std::make_pair("L1_EG25er2p1_HTT125er", &L1_EG25er2p1_HTT125er),          std::make_pair("L1_EG27er2p1_HTT200er", &L1_EG27er2p1_HTT200er),          std::make_pair("L1_ETM100", &L1_ETM100),          std::make_pair("L1_ETM100_Jet60_dPhi_Min0p4", &L1_ETM100_Jet60_dPhi_Min0p4),          std::make_pair("L1_ETM105", &L1_ETM105),          std::make_pair("L1_ETM110", &L1_ETM110),          std::make_pair("L1_ETM110_Jet60_dPhi_Min0p4", &L1_ETM110_Jet60_dPhi_Min0p4),          std::make_pair("L1_ETM115", &L1_ETM115),          std::make_pair("L1_ETM120", &L1_ETM120),          std::make_pair("L1_ETM150", &L1_ETM150),          std::make_pair("L1_ETM30", &L1_ETM30),          std::make_pair("L1_ETM40", &L1_ETM40),          std::make_pair("L1_ETM50", &L1_ETM50),          std::make_pair("L1_ETM60", &L1_ETM60),          std::make_pair("L1_ETM70", &L1_ETM70),          std::make_pair("L1_ETM75", &L1_ETM75),          std::make_pair("L1_ETM75_Jet60_dPhi_Min0p4", &L1_ETM75_Jet60_dPhi_Min0p4),          std::make_pair("L1_ETM80", &L1_ETM80),          std::make_pair("L1_ETM80_Jet60_dPhi_Min0p4", &L1_ETM80_Jet60_dPhi_Min0p4),          std::make_pair("L1_ETM85", &L1_ETM85),          std::make_pair("L1_ETM90", &L1_ETM90),          std::make_pair("L1_ETM90_Jet60_dPhi_Min0p4", &L1_ETM90_Jet60_dPhi_Min0p4),          std::make_pair("L1_ETM95", &L1_ETM95),          std::make_pair("L1_ETMHF100", &L1_ETMHF100),          std::make_pair("L1_ETMHF100_HTT60er", &L1_ETMHF100_HTT60er),          std::make_pair("L1_ETMHF100_Jet60_OR_DiJet30woTT28", &L1_ETMHF100_Jet60_OR_DiJet30woTT28),          std::make_pair("L1_ETMHF100_Jet60_OR_DoubleJet30", &L1_ETMHF100_Jet60_OR_DoubleJet30),          std::make_pair("L1_ETMHF100_Jet90_OR_DoubleJet45_OR_TripleJet30", &L1_ETMHF100_Jet90_OR_DoubleJet45_OR_TripleJet30),          std::make_pair("L1_ETMHF110", &L1_ETMHF110),          std::make_pair("L1_ETMHF110_HTT60er", &L1_ETMHF110_HTT60er),          std::make_pair("L1_ETMHF110_Jet60_OR_DiJet30woTT28", &L1_ETMHF110_Jet60_OR_DiJet30woTT28),          std::make_pair("L1_ETMHF110_Jet90_OR_DoubleJet45_OR_TripleJet30", &L1_ETMHF110_Jet90_OR_DoubleJet45_OR_TripleJet30),          std::make_pair("L1_ETMHF120", &L1_ETMHF120),          std::make_pair("L1_ETMHF120_HTT60er", &L1_ETMHF120_HTT60er),          std::make_pair("L1_ETMHF120_Jet60_OR_DiJet30woTT28", &L1_ETMHF120_Jet60_OR_DiJet30woTT28),          std::make_pair("L1_ETMHF150", &L1_ETMHF150),          std::make_pair("L1_ETMHF70", &L1_ETMHF70),          std::make_pair("L1_ETMHF70_Jet90_OR_DoubleJet45_OR_TripleJet30", &L1_ETMHF70_Jet90_OR_DoubleJet45_OR_TripleJet30),          std::make_pair("L1_ETMHF80", &L1_ETMHF80),          std::make_pair("L1_ETMHF80_HTT60er", &L1_ETMHF80_HTT60er),          std::make_pair("L1_ETMHF80_Jet90_OR_DoubleJet45_OR_TripleJet30", &L1_ETMHF80_Jet90_OR_DoubleJet45_OR_TripleJet30),          std::make_pair("L1_ETMHF90", &L1_ETMHF90),          std::make_pair("L1_ETMHF90_HTT60er", &L1_ETMHF90_HTT60er),          std::make_pair("L1_ETMHF90_Jet90_OR_DoubleJet45_OR_TripleJet30", &L1_ETMHF90_Jet90_OR_DoubleJet45_OR_TripleJet30),          std::make_pair("L1_ETT100_BptxAND", &L1_ETT100_BptxAND),          std::make_pair("L1_ETT110_BptxAND", &L1_ETT110_BptxAND),          std::make_pair("L1_ETT40_BptxAND", &L1_ETT40_BptxAND),          std::make_pair("L1_ETT50_BptxAND", &L1_ETT50_BptxAND),          std::make_pair("L1_ETT60_BptxAND", &L1_ETT60_BptxAND),          std::make_pair("L1_ETT70_BptxAND", &L1_ETT70_BptxAND),          std::make_pair("L1_ETT75_BptxAND", &L1_ETT75_BptxAND),          std::make_pair("L1_ETT80_BptxAND", &L1_ETT80_BptxAND),          std::make_pair("L1_ETT85_BptxAND", &L1_ETT85_BptxAND),          std::make_pair("L1_ETT90_BptxAND", &L1_ETT90_BptxAND),          std::make_pair("L1_ETT95_BptxAND", &L1_ETT95_BptxAND),          std::make_pair("L1_FirstBunchAfterTrain", &L1_FirstBunchAfterTrain),          std::make_pair("L1_FirstBunchInTrain", &L1_FirstBunchInTrain),          std::make_pair("L1_FirstCollisionInOrbit", &L1_FirstCollisionInOrbit),          std::make_pair("L1_FirstCollisionInTrain", &L1_FirstCollisionInTrain),          std::make_pair("L1_HTT120er", &L1_HTT120er),          std::make_pair("L1_HTT160er", &L1_HTT160er),          std::make_pair("L1_HTT200er", &L1_HTT200er),          std::make_pair("L1_HTT220er", &L1_HTT220er),          std::make_pair("L1_HTT240er", &L1_HTT240er),          std::make_pair("L1_HTT250er_QuadJet_70_55_40_35_er2p5", &L1_HTT250er_QuadJet_70_55_40_35_er2p5),          std::make_pair("L1_HTT255er", &L1_HTT255er),          std::make_pair("L1_HTT270er", &L1_HTT270er),          std::make_pair("L1_HTT280er", &L1_HTT280er),          std::make_pair("L1_HTT280er_QuadJet_70_55_40_35_er2p5", &L1_HTT280er_QuadJet_70_55_40_35_er2p5),          std::make_pair("L1_HTT300er", &L1_HTT300er),          std::make_pair("L1_HTT300er_QuadJet_70_55_40_35_er2p5", &L1_HTT300er_QuadJet_70_55_40_35_er2p5),          std::make_pair("L1_HTT320er", &L1_HTT320er),          std::make_pair("L1_HTT320er_QuadJet_70_55_40_40_er2p4", &L1_HTT320er_QuadJet_70_55_40_40_er2p4),          std::make_pair("L1_HTT320er_QuadJet_70_55_40_40_er2p5", &L1_HTT320er_QuadJet_70_55_40_40_er2p5),          std::make_pair("L1_HTT320er_QuadJet_70_55_45_45_er2p5", &L1_HTT320er_QuadJet_70_55_45_45_er2p5),          std::make_pair("L1_HTT340er", &L1_HTT340er),          std::make_pair("L1_HTT340er_QuadJet_70_55_40_40_er2p5", &L1_HTT340er_QuadJet_70_55_40_40_er2p5),          std::make_pair("L1_HTT340er_QuadJet_70_55_45_45_er2p5", &L1_HTT340er_QuadJet_70_55_45_45_er2p5),          std::make_pair("L1_HTT380er", &L1_HTT380er),          std::make_pair("L1_HTT400er", &L1_HTT400er),          std::make_pair("L1_HTT450er", &L1_HTT450er),          std::make_pair("L1_HTT500er", &L1_HTT500er),          std::make_pair("L1_IsoEG33_Mt40", &L1_IsoEG33_Mt40),          std::make_pair("L1_IsoEG33_Mt44", &L1_IsoEG33_Mt44),          std::make_pair("L1_IsoEG33_Mt48", &L1_IsoEG33_Mt48),          std::make_pair("L1_IsoTau40er_ETM100", &L1_IsoTau40er_ETM100),          std::make_pair("L1_IsoTau40er_ETM105", &L1_IsoTau40er_ETM105),          std::make_pair("L1_IsoTau40er_ETM110", &L1_IsoTau40er_ETM110),          std::make_pair("L1_IsoTau40er_ETM115", &L1_IsoTau40er_ETM115),          std::make_pair("L1_IsoTau40er_ETM120", &L1_IsoTau40er_ETM120),          std::make_pair("L1_IsoTau40er_ETM80", &L1_IsoTau40er_ETM80),          std::make_pair("L1_IsoTau40er_ETM85", &L1_IsoTau40er_ETM85),          std::make_pair("L1_IsoTau40er_ETM90", &L1_IsoTau40er_ETM90),          std::make_pair("L1_IsoTau40er_ETM95", &L1_IsoTau40er_ETM95),          std::make_pair("L1_IsoTau40er_ETMHF100", &L1_IsoTau40er_ETMHF100),          std::make_pair("L1_IsoTau40er_ETMHF110", &L1_IsoTau40er_ETMHF110),          std::make_pair("L1_IsoTau40er_ETMHF120", &L1_IsoTau40er_ETMHF120),          std::make_pair("L1_IsoTau40er_ETMHF80", &L1_IsoTau40er_ETMHF80),          std::make_pair("L1_IsoTau40er_ETMHF90", &L1_IsoTau40er_ETMHF90),          std::make_pair("L1_IsolatedBunch", &L1_IsolatedBunch),          std::make_pair("L1_LastCollisionInTrain", &L1_LastCollisionInTrain),          std::make_pair("L1_LooseIsoEG22er2p1_IsoTau26er2p1_dR_Min0p3", &L1_LooseIsoEG22er2p1_IsoTau26er2p1_dR_Min0p3),          std::make_pair("L1_LooseIsoEG24er2p1_HTT100er", &L1_LooseIsoEG24er2p1_HTT100er),          std::make_pair("L1_LooseIsoEG24er2p1_IsoTau27er2p1_dR_Min0p3", &L1_LooseIsoEG24er2p1_IsoTau27er2p1_dR_Min0p3),          std::make_pair("L1_LooseIsoEG24er2p1_Jet26er2p7_dR_Min0p3", &L1_LooseIsoEG24er2p1_Jet26er2p7_dR_Min0p3),          std::make_pair("L1_LooseIsoEG24er2p1_TripleJet_26er2p7_26_26er2p7", &L1_LooseIsoEG24er2p1_TripleJet_26er2p7_26_26er2p7),          std::make_pair("L1_LooseIsoEG26er2p1_HTT100er", &L1_LooseIsoEG26er2p1_HTT100er),          std::make_pair("L1_LooseIsoEG26er2p1_Jet34er2p7_dR_Min0p3", &L1_LooseIsoEG26er2p1_Jet34er2p7_dR_Min0p3),          std::make_pair("L1_LooseIsoEG28er2p1_HTT100er", &L1_LooseIsoEG28er2p1_HTT100er),          std::make_pair("L1_LooseIsoEG28er2p1_Jet34er2p7_dR_Min0p3", &L1_LooseIsoEG28er2p1_Jet34er2p7_dR_Min0p3),          std::make_pair("L1_LooseIsoEG30er2p1_Jet34er2p7_dR_Min0p3", &L1_LooseIsoEG30er2p1_Jet34er2p7_dR_Min0p3),          std::make_pair("L1_MU20_EG15", &L1_MU20_EG15),          std::make_pair("L1_MinimumBiasHF0_AND_BptxAND", &L1_MinimumBiasHF0_AND_BptxAND),          std::make_pair("L1_MinimumBiasHF0_OR_BptxAND", &L1_MinimumBiasHF0_OR_BptxAND),          std::make_pair("L1_Mu10er2p1_ETM30", &L1_Mu10er2p1_ETM30),          std::make_pair("L1_Mu10er2p3_Jet32er2p3_dR_Max0p4_DoubleJet32er2p3_dEta_Max1p6", &L1_Mu10er2p3_Jet32er2p3_dR_Max0p4_DoubleJet32er2p3_dEta_Max1p6),          std::make_pair("L1_Mu12_EG10", &L1_Mu12_EG10),          std::make_pair("L1_Mu12er2p3_Jet40er2p3_dR_Max0p4_DoubleJet40er2p3_dEta_Max1p6", &L1_Mu12er2p3_Jet40er2p3_dR_Max0p4_DoubleJet40er2p3_dEta_Max1p6),          std::make_pair("L1_Mu14er2p1_ETM30", &L1_Mu14er2p1_ETM30),          std::make_pair("L1_Mu15_HTT100er", &L1_Mu15_HTT100er),          std::make_pair("L1_Mu18_HTT100er", &L1_Mu18_HTT100er),          std::make_pair("L1_Mu18_Jet24er2p7", &L1_Mu18_Jet24er2p7),          std::make_pair("L1_Mu18er2p1_IsoTau26er2p1", &L1_Mu18er2p1_IsoTau26er2p1),          std::make_pair("L1_Mu18er2p1_Tau24er2p1", &L1_Mu18er2p1_Tau24er2p1),          std::make_pair("L1_Mu20_EG10", &L1_Mu20_EG10),          std::make_pair("L1_Mu20_EG17", &L1_Mu20_EG17),          std::make_pair("L1_Mu20_LooseIsoEG6", &L1_Mu20_LooseIsoEG6),          std::make_pair("L1_Mu20er2p1_IsoTau26er2p1", &L1_Mu20er2p1_IsoTau26er2p1),          std::make_pair("L1_Mu20er2p1_IsoTau27er2p1", &L1_Mu20er2p1_IsoTau27er2p1),          std::make_pair("L1_Mu22er2p1_IsoTau28er2p1", &L1_Mu22er2p1_IsoTau28er2p1),          std::make_pair("L1_Mu22er2p1_IsoTau30er2p1", &L1_Mu22er2p1_IsoTau30er2p1),          std::make_pair("L1_Mu22er2p1_IsoTau32er2p1", &L1_Mu22er2p1_IsoTau32er2p1),          std::make_pair("L1_Mu22er2p1_IsoTau33er2p1", &L1_Mu22er2p1_IsoTau33er2p1),          std::make_pair("L1_Mu22er2p1_IsoTau34er2p1", &L1_Mu22er2p1_IsoTau34er2p1),          std::make_pair("L1_Mu22er2p1_IsoTau35er2p1", &L1_Mu22er2p1_IsoTau35er2p1),          std::make_pair("L1_Mu22er2p1_IsoTau36er2p1", &L1_Mu22er2p1_IsoTau36er2p1),          std::make_pair("L1_Mu22er2p1_IsoTau38er2p1", &L1_Mu22er2p1_IsoTau38er2p1),          std::make_pair("L1_Mu22er2p1_IsoTau40er2p1", &L1_Mu22er2p1_IsoTau40er2p1),          std::make_pair("L1_Mu22er2p1_Tau50er2p1", &L1_Mu22er2p1_Tau50er2p1),          std::make_pair("L1_Mu22er2p1_Tau70er2p1", &L1_Mu22er2p1_Tau70er2p1),          std::make_pair("L1_Mu23_EG10", &L1_Mu23_EG10),          std::make_pair("L1_Mu23_LooseIsoEG10", &L1_Mu23_LooseIsoEG10),          std::make_pair("L1_Mu3_Jet120er2p7_dEta_Max0p4_dPhi_Max0p4", &L1_Mu3_Jet120er2p7_dEta_Max0p4_dPhi_Max0p4),          std::make_pair("L1_Mu3_Jet16er2p7_dEta_Max0p4_dPhi_Max0p4", &L1_Mu3_Jet16er2p7_dEta_Max0p4_dPhi_Max0p4),          std::make_pair("L1_Mu3_Jet30er2p5", &L1_Mu3_Jet30er2p5),          std::make_pair("L1_Mu3_Jet60er2p7_dEta_Max0p4_dPhi_Max0p4", &L1_Mu3_Jet60er2p7_dEta_Max0p4_dPhi_Max0p4),          std::make_pair("L1_Mu5_EG15", &L1_Mu5_EG15),          std::make_pair("L1_Mu5_EG20", &L1_Mu5_EG20),          std::make_pair("L1_Mu5_EG23", &L1_Mu5_EG23),          std::make_pair("L1_Mu5_LooseIsoEG18", &L1_Mu5_LooseIsoEG18),          std::make_pair("L1_Mu5_LooseIsoEG20", &L1_Mu5_LooseIsoEG20),          std::make_pair("L1_Mu6_DoubleEG10", &L1_Mu6_DoubleEG10),          std::make_pair("L1_Mu6_DoubleEG17", &L1_Mu6_DoubleEG17),          std::make_pair("L1_Mu6_HTT200er", &L1_Mu6_HTT200er),          std::make_pair("L1_Mu6_HTT240er", &L1_Mu6_HTT240er),          std::make_pair("L1_Mu6_HTT250er", &L1_Mu6_HTT250er),          std::make_pair("L1_Mu7_EG23", &L1_Mu7_EG23),          std::make_pair("L1_Mu7_LooseIsoEG20", &L1_Mu7_LooseIsoEG20),          std::make_pair("L1_Mu7_LooseIsoEG23", &L1_Mu7_LooseIsoEG23),          std::make_pair("L1_Mu8_HTT150er", &L1_Mu8_HTT150er),          std::make_pair("L1_NotBptxOR", &L1_NotBptxOR),          std::make_pair("L1_QuadJet36er2p7_IsoTau52er2p1", &L1_QuadJet36er2p7_IsoTau52er2p1),          std::make_pair("L1_QuadJet36er2p7_Tau52", &L1_QuadJet36er2p7_Tau52),          std::make_pair("L1_QuadJet40er2p7", &L1_QuadJet40er2p7),          std::make_pair("L1_QuadJet50er2p7", &L1_QuadJet50er2p7),          std::make_pair("L1_QuadJet60er2p7", &L1_QuadJet60er2p7),          std::make_pair("L1_QuadMu0", &L1_QuadMu0),          std::make_pair("L1_SingleEG10", &L1_SingleEG10),          std::make_pair("L1_SingleEG15", &L1_SingleEG15),          std::make_pair("L1_SingleEG18", &L1_SingleEG18),          std::make_pair("L1_SingleEG24", &L1_SingleEG24),          std::make_pair("L1_SingleEG26", &L1_SingleEG26),          std::make_pair("L1_SingleEG28", &L1_SingleEG28),          std::make_pair("L1_SingleEG2_BptxAND", &L1_SingleEG2_BptxAND),          std::make_pair("L1_SingleEG30", &L1_SingleEG30),          std::make_pair("L1_SingleEG32", &L1_SingleEG32),          std::make_pair("L1_SingleEG34", &L1_SingleEG34),          std::make_pair("L1_SingleEG34er2p1", &L1_SingleEG34er2p1),          std::make_pair("L1_SingleEG36", &L1_SingleEG36),          std::make_pair("L1_SingleEG36er2p1", &L1_SingleEG36er2p1),          std::make_pair("L1_SingleEG38", &L1_SingleEG38),          std::make_pair("L1_SingleEG38er2p1", &L1_SingleEG38er2p1),          std::make_pair("L1_SingleEG40", &L1_SingleEG40),          std::make_pair("L1_SingleEG42", &L1_SingleEG42),          std::make_pair("L1_SingleEG45", &L1_SingleEG45),          std::make_pair("L1_SingleEG5", &L1_SingleEG5),          std::make_pair("L1_SingleEG50", &L1_SingleEG50),          std::make_pair("L1_SingleIsoEG18", &L1_SingleIsoEG18),          std::make_pair("L1_SingleIsoEG18er2p1", &L1_SingleIsoEG18er2p1),          std::make_pair("L1_SingleIsoEG20", &L1_SingleIsoEG20),          std::make_pair("L1_SingleIsoEG20er2p1", &L1_SingleIsoEG20er2p1),          std::make_pair("L1_SingleIsoEG22", &L1_SingleIsoEG22),          std::make_pair("L1_SingleIsoEG22er2p1", &L1_SingleIsoEG22er2p1),          std::make_pair("L1_SingleIsoEG24", &L1_SingleIsoEG24),          std::make_pair("L1_SingleIsoEG24er2p1", &L1_SingleIsoEG24er2p1),          std::make_pair("L1_SingleIsoEG26", &L1_SingleIsoEG26),          std::make_pair("L1_SingleIsoEG26er2p1", &L1_SingleIsoEG26er2p1),          std::make_pair("L1_SingleIsoEG28", &L1_SingleIsoEG28),          std::make_pair("L1_SingleIsoEG28er2p1", &L1_SingleIsoEG28er2p1),          std::make_pair("L1_SingleIsoEG30", &L1_SingleIsoEG30),          std::make_pair("L1_SingleIsoEG30er2p1", &L1_SingleIsoEG30er2p1),          std::make_pair("L1_SingleIsoEG32", &L1_SingleIsoEG32),          std::make_pair("L1_SingleIsoEG32er2p1", &L1_SingleIsoEG32er2p1),          std::make_pair("L1_SingleIsoEG33er2p1", &L1_SingleIsoEG33er2p1),          std::make_pair("L1_SingleIsoEG34", &L1_SingleIsoEG34),          std::make_pair("L1_SingleIsoEG34er2p1", &L1_SingleIsoEG34er2p1),          std::make_pair("L1_SingleIsoEG35", &L1_SingleIsoEG35),          std::make_pair("L1_SingleIsoEG35er2p1", &L1_SingleIsoEG35er2p1),          std::make_pair("L1_SingleIsoEG36", &L1_SingleIsoEG36),          std::make_pair("L1_SingleIsoEG36er2p1", &L1_SingleIsoEG36er2p1),          std::make_pair("L1_SingleIsoEG37", &L1_SingleIsoEG37),          std::make_pair("L1_SingleIsoEG38", &L1_SingleIsoEG38),          std::make_pair("L1_SingleIsoEG38er2p1", &L1_SingleIsoEG38er2p1),          std::make_pair("L1_SingleIsoEG40", &L1_SingleIsoEG40),          std::make_pair("L1_SingleIsoEG40er2p1", &L1_SingleIsoEG40er2p1),          std::make_pair("L1_SingleJet120", &L1_SingleJet120),          std::make_pair("L1_SingleJet120_FWD", &L1_SingleJet120_FWD),          std::make_pair("L1_SingleJet12_BptxAND", &L1_SingleJet12_BptxAND),          std::make_pair("L1_SingleJet140", &L1_SingleJet140),          std::make_pair("L1_SingleJet150", &L1_SingleJet150),          std::make_pair("L1_SingleJet16", &L1_SingleJet16),          std::make_pair("L1_SingleJet160", &L1_SingleJet160),          std::make_pair("L1_SingleJet170", &L1_SingleJet170),          std::make_pair("L1_SingleJet180", &L1_SingleJet180),          std::make_pair("L1_SingleJet20", &L1_SingleJet20),          std::make_pair("L1_SingleJet200", &L1_SingleJet200),          std::make_pair("L1_SingleJet20er2p7_NotBptxOR", &L1_SingleJet20er2p7_NotBptxOR),          std::make_pair("L1_SingleJet20er2p7_NotBptxOR_3BX", &L1_SingleJet20er2p7_NotBptxOR_3BX),          std::make_pair("L1_SingleJet35", &L1_SingleJet35),          std::make_pair("L1_SingleJet35_FWD", &L1_SingleJet35_FWD),          std::make_pair("L1_SingleJet35_HFm", &L1_SingleJet35_HFm),          std::make_pair("L1_SingleJet35_HFp", &L1_SingleJet35_HFp),          std::make_pair("L1_SingleJet43er2p7_NotBptxOR_3BX", &L1_SingleJet43er2p7_NotBptxOR_3BX),          std::make_pair("L1_SingleJet46er2p7_NotBptxOR_3BX", &L1_SingleJet46er2p7_NotBptxOR_3BX),          std::make_pair("L1_SingleJet60", &L1_SingleJet60),          std::make_pair("L1_SingleJet60_FWD", &L1_SingleJet60_FWD),          std::make_pair("L1_SingleJet60_HFm", &L1_SingleJet60_HFm),          std::make_pair("L1_SingleJet60_HFp", &L1_SingleJet60_HFp),          std::make_pair("L1_SingleJet90", &L1_SingleJet90),          std::make_pair("L1_SingleJet90_FWD", &L1_SingleJet90_FWD),          std::make_pair("L1_SingleMu0_BMTF", &L1_SingleMu0_BMTF),          std::make_pair("L1_SingleMu0_EMTF", &L1_SingleMu0_EMTF),          std::make_pair("L1_SingleMu0_OMTF", &L1_SingleMu0_OMTF),          std::make_pair("L1_SingleMu10_LowQ", &L1_SingleMu10_LowQ),          std::make_pair("L1_SingleMu11_LowQ", &L1_SingleMu11_LowQ),          std::make_pair("L1_SingleMu12_LowQ_BMTF", &L1_SingleMu12_LowQ_BMTF),          std::make_pair("L1_SingleMu12_LowQ_EMTF", &L1_SingleMu12_LowQ_EMTF),          std::make_pair("L1_SingleMu12_LowQ_OMTF", &L1_SingleMu12_LowQ_OMTF),          std::make_pair("L1_SingleMu14er2p1", &L1_SingleMu14er2p1),          std::make_pair("L1_SingleMu16", &L1_SingleMu16),          std::make_pair("L1_SingleMu16er2p1", &L1_SingleMu16er2p1),          std::make_pair("L1_SingleMu18", &L1_SingleMu18),          std::make_pair("L1_SingleMu18er2p1", &L1_SingleMu18er2p1),          std::make_pair("L1_SingleMu20", &L1_SingleMu20),          std::make_pair("L1_SingleMu20er2p1", &L1_SingleMu20er2p1),          std::make_pair("L1_SingleMu22", &L1_SingleMu22),          std::make_pair("L1_SingleMu22_BMTF", &L1_SingleMu22_BMTF),          std::make_pair("L1_SingleMu22_EMTF", &L1_SingleMu22_EMTF),          std::make_pair("L1_SingleMu22_OMTF", &L1_SingleMu22_OMTF),          std::make_pair("L1_SingleMu22er2p1", &L1_SingleMu22er2p1),          std::make_pair("L1_SingleMu25", &L1_SingleMu25),          std::make_pair("L1_SingleMu3", &L1_SingleMu3),          std::make_pair("L1_SingleMu30", &L1_SingleMu30),          std::make_pair("L1_SingleMu3er1p5_SingleJet100er2p5_ETMHF40", &L1_SingleMu3er1p5_SingleJet100er2p5_ETMHF40),          std::make_pair("L1_SingleMu5", &L1_SingleMu5),          std::make_pair("L1_SingleMu7", &L1_SingleMu7),          std::make_pair("L1_SingleMuCosmics", &L1_SingleMuCosmics),          std::make_pair("L1_SingleMuCosmics_BMTF", &L1_SingleMuCosmics_BMTF),          std::make_pair("L1_SingleMuCosmics_EMTF", &L1_SingleMuCosmics_EMTF),          std::make_pair("L1_SingleMuCosmics_OMTF", &L1_SingleMuCosmics_OMTF),          std::make_pair("L1_SingleMuOpen", &L1_SingleMuOpen),          std::make_pair("L1_SingleMuOpen_NotBptxOR", &L1_SingleMuOpen_NotBptxOR),          std::make_pair("L1_SingleMuOpen_NotBptxOR_3BX", &L1_SingleMuOpen_NotBptxOR_3BX),          std::make_pair("L1_SingleTau100er2p1", &L1_SingleTau100er2p1),          std::make_pair("L1_SingleTau120er2p1", &L1_SingleTau120er2p1),          std::make_pair("L1_SingleTau130er2p1", &L1_SingleTau130er2p1),          std::make_pair("L1_SingleTau140er2p1", &L1_SingleTau140er2p1),          std::make_pair("L1_SingleTau20", &L1_SingleTau20),          std::make_pair("L1_SingleTau80er2p1", &L1_SingleTau80er2p1),          std::make_pair("L1_TripleEG_14_10_8", &L1_TripleEG_14_10_8),          std::make_pair("L1_TripleEG_18_17_8", &L1_TripleEG_18_17_8),          std::make_pair("L1_TripleEG_LooseIso20_10_5", &L1_TripleEG_LooseIso20_10_5),          std::make_pair("L1_TripleJet_100_85_72_VBF", &L1_TripleJet_100_85_72_VBF),          std::make_pair("L1_TripleJet_105_85_76_VBF", &L1_TripleJet_105_85_76_VBF),          std::make_pair("L1_TripleJet_84_68_48_VBF", &L1_TripleJet_84_68_48_VBF),          std::make_pair("L1_TripleJet_88_72_56_VBF", &L1_TripleJet_88_72_56_VBF),          std::make_pair("L1_TripleJet_92_76_64_VBF", &L1_TripleJet_92_76_64_VBF),          std::make_pair("L1_TripleJet_98_83_71_VBF", &L1_TripleJet_98_83_71_VBF),          std::make_pair("L1_TripleMu0", &L1_TripleMu0),          std::make_pair("L1_TripleMu0_OQ", &L1_TripleMu0_OQ),          std::make_pair("L1_TripleMu3", &L1_TripleMu3),          std::make_pair("L1_TripleMu3_SQ", &L1_TripleMu3_SQ),          std::make_pair("L1_TripleMu_4_4_4", &L1_TripleMu_4_4_4),          std::make_pair("L1_TripleMu_5OQ_3p5OQ_2p5OQ_DoubleMu_5_2p5_OQ_OS_Mass_5to17", &L1_TripleMu_5OQ_3p5OQ_2p5OQ_DoubleMu_5_2p5_OQ_OS_Mass_5to17),          std::make_pair("L1_TripleMu_5OQ_3p5OQ_2p5OQ_DoubleMu_5_2p5_OQ_OS_Mass_8to14", &L1_TripleMu_5OQ_3p5OQ_2p5OQ_DoubleMu_5_2p5_OQ_OS_Mass_8to14),          std::make_pair("L1_TripleMu_5SQ_3SQ_0OQ", &L1_TripleMu_5SQ_3SQ_0OQ),          std::make_pair("L1_TripleMu_5SQ_3SQ_0OQ_DoubleMu_5_3_SQ_OS_Mass_Max9", &L1_TripleMu_5SQ_3SQ_0OQ_DoubleMu_5_3_SQ_OS_Mass_Max9),          std::make_pair("L1_TripleMu_5SQ_3SQ_0_DoubleMu_5_3_SQ_OS_Mass_Max9", &L1_TripleMu_5SQ_3SQ_0_DoubleMu_5_3_SQ_OS_Mass_Max9),          std::make_pair("L1_TripleMu_5_0_0", &L1_TripleMu_5_0_0),          std::make_pair("L1_TripleMu_5_3_3", &L1_TripleMu_5_3_3),          std::make_pair("L1_TripleMu_5_3p5_2p5", &L1_TripleMu_5_3p5_2p5),          std::make_pair("L1_TripleMu_5_3p5_2p5_DoubleMu_5_2p5_OS_Mass_5to17", &L1_TripleMu_5_3p5_2p5_DoubleMu_5_2p5_OS_Mass_5to17),          std::make_pair("L1_TripleMu_5_4_2p5_DoubleMu_5_2p5_OS_Mass_5to17", &L1_TripleMu_5_4_2p5_DoubleMu_5_2p5_OS_Mass_5to17),          std::make_pair("L1_TripleMu_5_5_3", &L1_TripleMu_5_5_3),          std::make_pair("L1_UnpairedBunchBptxMinus", &L1_UnpairedBunchBptxMinus),          std::make_pair("L1_UnpairedBunchBptxPlus", &L1_UnpairedBunchBptxPlus),          std::make_pair("L1_ZeroBias", &L1_ZeroBias),          std::make_pair("L1_ZeroBias_copy", &L1_ZeroBias_copy)      };

  for (auto pair : name2func)
  {
    L1SeedFun[pair.first] = std::bind(pair.second, upgrade, calo_tower);
  }

  return true;
}
// eof