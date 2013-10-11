import ROOT

ROOT.gROOT.ProcessLine(".L WPolarizationVariation.C+")
ROOT.gROOT.ProcessLine(".L TTbarPolarization.C+")

#x,y,z,E
Wpx = 100
Wpy = 100
Wpz = 20
lpx = 40
lpy = -110
lpz = 30

genp4_Wplus_ = ROOT.TLorentzVector(Wpx, Wpy, Wpz, ROOT.sqrt(80.4**2 + Wpx**2 + Wpy**2 + Wpz**2))
genp4_lplus_ = ROOT.TLorentzVector(lpx, lpy, lpz, ROOT.sqrt(80.4**2 + lpx**2 + lpy**2 + lpz**2))

Wplus_weight_flfr_plus        = ROOT.GetWeightWjetsPolarizationFLminusFR(genp4_Wplus_,genp4_lplus_,10,1); #10 means +10 percent variation and 1 means it is a W plus
Wplus_weight_flfr_plus_5per   = ROOT.GetWeightWjetsPolarizationFLminusFR(genp4_Wplus_,genp4_lplus_,5,1);
Wplus_weight_flfr_minus       = ROOT.GetWeightWjetsPolarizationFLminusFR(genp4_Wplus_,genp4_lplus_,-10,1);
Wplus_weight_flfr_minus_5per  = ROOT.GetWeightWjetsPolarizationFLminusFR(genp4_Wplus_,genp4_lplus_,-5,1);
Wplus_weight_f0_plus          = ROOT.GetWeightWjetsPolarizationF0(genp4_Wplus_,genp4_lplus_,10,1);                              
Wplus_weight_f0_minus         = ROOT.GetWeightWjetsPolarizationF0(genp4_Wplus_,genp4_lplus_,-10,1);

Wminus_weight_flfr_plus        = ROOT.GetWeightWjetsPolarizationFLminusFR(genp4_Wplus_,genp4_lplus_,10,0); #10 means +10 percent variation and 1 means it is a W plus
Wminus_weight_flfr_plus_5per   = ROOT.GetWeightWjetsPolarizationFLminusFR(genp4_Wplus_,genp4_lplus_,5,0);
Wminus_weight_flfr_minus       = ROOT.GetWeightWjetsPolarizationFLminusFR(genp4_Wplus_,genp4_lplus_,-10,0);
Wminus_weight_flfr_minus_5per  = ROOT.GetWeightWjetsPolarizationFLminusFR(genp4_Wplus_,genp4_lplus_,-5,0);
Wminus_weight_f0_plus          = ROOT.GetWeightWjetsPolarizationF0(genp4_Wplus_,genp4_lplus_,10,0);                              
Wminus_weight_f0_minus         = ROOT.GetWeightWjetsPolarizationF0(genp4_Wplus_,genp4_lplus_,-10,0);

print "Wplus_weight_flfr_plus      ",  Wplus_weight_flfr_plus 
print "Wplus_weight_flfr_plus_5per ",  Wplus_weight_flfr_plus_5per  
print "Wplus_weight_flfr_minus     ",  Wplus_weight_flfr_minus      
print "Wplus_weight_flfr_minus_5per",  Wplus_weight_flfr_minus_5per 
print "Wplus_weight_f0_plus        ",  Wplus_weight_f0_plus         
print "Wplus_weight_f0_minus       ",  Wplus_weight_f0_minus        
print "Wminus_weight_flfr_plus      ",  Wminus_weight_flfr_plus 
print "Wminus_weight_flfr_plus_5per ",  Wminus_weight_flfr_plus_5per  
print "Wminus_weight_flfr_minus     ",  Wminus_weight_flfr_minus      
print "Wminus_weight_flfr_minus_5per",  Wminus_weight_flfr_minus_5per 
print "Wminus_weight_f0_plus        ",  Wminus_weight_f0_plus         
print "Wminus_weight_f0_minus       ",  Wminus_weight_f0_minus        

