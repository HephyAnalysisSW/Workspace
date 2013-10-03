//
// pdf uncertainties for T1tttt from Paul (as used by UCSB)
//
void pdfT1tttt (int whichHT, double Mgluino, double mLSP,
		double& pdfMETbin1, double& pdfMETbin2, double& pdfMETbin3) {
	//PDF uncertainty
      	double PDFunc_METbin1=0.0, PDFunc_METbin2=0.0, PDFunc_METbin3=0.0;
	double  x1l1, y1l1, x2l1, y2l1, x1l2, y1l2, x2l2, y2l2;
	//	double mLSP, Mgluino;
	if(whichHT==500) {
	  x1l1=1400.0; y1l1=950.0; x2l1=1401.0; y2l1=950.0+0.55882; x1l2=1400.0; y1l2=1050.0; x2l2=1401.0; y2l2=1050.0+0.55882;
	  if(mLSP>=(y2l2-y1l2)/(x2l2-x1l2)*(Mgluino-x1l2)+y1l2) PDFunc_METbin1 = 0.5;
	  else if(mLSP>=(y2l1-y1l1)/(x2l1-x1l1)*(Mgluino-x1l1)+y1l1) PDFunc_METbin1 = 0.3;  
	  else PDFunc_METbin1 = 0.15;
	  x1l1=1400.0; y1l1=750.0; x2l1=1401.0; y2l1=750.0+0.55882; x1l2=1400.0; y1l2=950.0; x2l2=1401.0; y2l2=950.0+0.55882;
	  if(mLSP>=(y2l2-y1l2)/(x2l2-x1l2)*(Mgluino-x1l2)+y1l2) PDFunc_METbin2 = 0.5;
	  else if(mLSP>=(y2l1-y1l1)/(x2l1-x1l1)*(Mgluino-x1l1)+y1l1) PDFunc_METbin2 = 0.3;  
	  else PDFunc_METbin2 = 0.15;
	  x1l1=1400.0; y1l1=650.0; x2l1=1401.0; y2l1=650.0+0.55882; x1l2=1400.0; y1l2=875.0; x2l2=1401.0; y2l2=875.0+0.55882;
	  if(mLSP>=(y2l2-y1l2)/(x2l2-x1l2)*(Mgluino-x1l2)+y1l2) PDFunc_METbin3 = 0.5;
	  else if(mLSP>=(y2l1-y1l1)/(x2l1-x1l1)*(Mgluino-x1l1)+y1l1) PDFunc_METbin3 = 0.3;  
	  else PDFunc_METbin3 = 0.15;
	}
	if(whichHT==750) {
	  x1l1=1400.0; y1l1=825.0; x2l1=1401.0; y2l1=825.0+0.55882; x1l2=1400.0; y1l2=975.0; x2l2=1401.0; y2l2=975.0+0.55882;
	  if(mLSP>=(y2l2-y1l2)/(x2l2-x1l2)*(Mgluino-x1l2)+y1l2) PDFunc_METbin1 = 0.5;
	  else if(mLSP>=(y2l1-y1l1)/(x2l1-x1l1)*(Mgluino-x1l1)+y1l1) PDFunc_METbin1 = 0.3;  
	  else PDFunc_METbin1 = 0.15;
	  x1l1=1400.0; y1l1=700.0; x2l1=1401.0; y2l1=700.0+0.55882; x1l2=1400.0; y1l2=875.0; x2l2=1401.0; y2l2=875.0+0.55882;
	  if(mLSP>=(y2l2-y1l2)/(x2l2-x1l2)*(Mgluino-x1l2)+y1l2) PDFunc_METbin2 = 0.5;
	  else if(mLSP>=(y2l1-y1l1)/(x2l1-x1l1)*(Mgluino-x1l1)+y1l1) PDFunc_METbin2 = 0.3;  
	  else PDFunc_METbin2 = 0.15;
	  x1l1=1400.0; y1l1=600.0; x2l1=1401.0; y2l1=600.0+0.55882; x1l2=1400.0; y1l2=850.0; x2l2=1401.0; y2l2=850.0+0.55882;
	  if(mLSP>=(y2l2-y1l2)/(x2l2-x1l2)*(Mgluino-x1l2)+y1l2) PDFunc_METbin3 = 0.5;
	  else if(mLSP>=(y2l1-y1l1)/(x2l1-x1l1)*(Mgluino-x1l1)+y1l1) PDFunc_METbin3 = 0.3;  
	  else PDFunc_METbin3 = 0.15;
	}
	if(whichHT==1000) {
	  x1l1=1400.0; y1l1=650.0; x2l1=1401.0; y2l1=650.0+0.55882; x1l2=1400.0; y1l2=825.0; x2l2=1401.0; y2l2=825.0+0.55882;
	  if(mLSP>=(y2l2-y1l2)/(x2l2-x1l2)*(Mgluino-x1l2)+y1l2) PDFunc_METbin1 = 0.5;
	  else if(mLSP>=(y2l1-y1l1)/(x2l1-x1l1)*(Mgluino-x1l1)+y1l1) PDFunc_METbin1 = 0.3;  
	  else PDFunc_METbin1 = 0.15;
	  x1l1=1400.0; y1l1=625.0; x2l1=1401.0; y2l1=625.0+0.55882; x1l2=1400.0; y1l2=775.0; x2l2=1401.0; y2l2=775.0+0.55882;
	  if(mLSP>=(y2l2-y1l2)/(x2l2-x1l2)*(Mgluino-x1l2)+y1l2) PDFunc_METbin2 = 0.5;
	  else if(mLSP>=(y2l1-y1l1)/(x2l1-x1l1)*(Mgluino-x1l1)+y1l1) PDFunc_METbin2 = 0.3;  
	  else PDFunc_METbin2 = 0.15;
	  x1l1=1400.0; y1l1=550.0; x2l1=1401.0; y2l1=550.0+0.55882; x1l2=1400.0; y1l2=750.0; x2l2=1401.0; y2l2=750.0+0.55882;
	  if(mLSP>=(y2l2-y1l2)/(x2l2-x1l2)*(Mgluino-x1l2)+y1l2) PDFunc_METbin3 = 0.5;
	  else if(mLSP>=(y2l1-y1l1)/(x2l1-x1l1)*(Mgluino-x1l1)+y1l1) PDFunc_METbin3 = 0.3;  
	  else PDFunc_METbin3 = 0.15;
	}

	pdfMETbin1 = PDFunc_METbin1;
	pdfMETbin2 = PDFunc_METbin2;
	pdfMETbin3 = PDFunc_METbin3;
    
}
