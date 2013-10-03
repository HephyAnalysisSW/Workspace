//
// pdf uncertainties for T1t1t from Paul (as used by UCSB)
//
void pdfT1t1t (int whichHT, double Mstop, double mLSP,
	       double& pdfMETbin1, double& pdfMETbin2, double& pdfMETbin3) {
 
	//PDF uncertainty
      	double PDFunc_METbin1=0.0, PDFunc_METbin2=0.0, PDFunc_METbin3=0.0;
	double  x1l1, y1l1, x2l1, y2l1, x1l2, y1l2, x2l2, y2l2;
	//	double mLSP, Mstop;
	if(whichHT==500) {
	  x1l1=825.0; y1l1=575.0; x2l1=750.0; y2l1=600.0;
	  if(0>1) PDFunc_METbin1 = 0.5;
	  else if(mLSP>=(y2l1-y1l1)/(x2l1-x1l1)*(Mstop-x1l1)+y1l1) PDFunc_METbin1 = 0.3;  
	  else PDFunc_METbin1 = 0.15;
	  x1l1=825.0; y1l1=525.0; x2l1=750.0; y2l1=550.0; x1l2=825.0; y1l2=600.0; x2l2=750.0; y2l2=625.0;
	  if(mLSP>=(y2l2-y1l2)/(x2l2-x1l2)*(Mstop-x1l2)+y1l2) PDFunc_METbin2 = 0.5;
	  else if(mLSP>=(y2l1-y1l1)/(x2l1-x1l1)*(Mstop-x1l1)+y1l1) PDFunc_METbin2 = 0.3;  
	  else PDFunc_METbin2 = 0.15;
	  x1l1=825.0; y1l1=375.0; x2l1=750.0; y2l1=400.0; x1l2=825.0; y1l2=525.0; x2l2=750.0; y2l2=550.0;
	  if(mLSP>=(y2l2-y1l2)/(x2l2-x1l2)*(Mstop-x1l2)+y1l2) PDFunc_METbin3 = 0.5;
	  else if(mLSP>=(y2l1-y1l1)/(x2l1-x1l1)*(Mstop-x1l1)+y1l1) PDFunc_METbin3 = 0.3;  
	  else PDFunc_METbin3 = 0.15;
	}
	if(whichHT==750) {
	  x1l1=825.0; y1l1=500.0; x2l1=750.0; y2l1=525.0; 
	  if(0>1) PDFunc_METbin1 = 0.5;
	  else if(mLSP>=(y2l1-y1l1)/(x2l1-x1l1)*(Mstop-x1l1)+y1l1) PDFunc_METbin1 = 0.3;  
	  else PDFunc_METbin1 = 0.15;
	  x1l1=825.0; y1l1=500.0; x2l1=750.0; y2l1=525.0; x1l2=825.0; y1l2=600.0; x2l2=750.0; y2l2=625.0;
	  if(mLSP>=(y2l2-y1l2)/(x2l2-x1l2)*(Mstop-x1l2)+y1l2) PDFunc_METbin2 = 0.5;
	  else if(mLSP>=(y2l1-y1l1)/(x2l1-x1l1)*(Mstop-x1l1)+y1l1) PDFunc_METbin2 = 0.3;  
	  else PDFunc_METbin2 = 0.15;
	  x1l1=825.0; y1l1=350.0; x2l1=750.0; y2l1=375.0; x1l2=825.0; y1l2=550.0; x2l2=750.0; y2l2=575.0;
	  if(mLSP>=(y2l2-y1l2)/(x2l2-x1l2)*(Mstop-x1l2)+y1l2) PDFunc_METbin3 = 0.5;
	  else if(mLSP>=(y2l1-y1l1)/(x2l1-x1l1)*(Mstop-x1l1)+y1l1) PDFunc_METbin3 = 0.3;  
	  else PDFunc_METbin3 = 0.15;
	}
	if(whichHT==1000) {
	  x1l1=825.0; y1l1=350.0; x2l1=750.0; y2l1=375.0; x1l2=825.0; y1l2=600.0; x2l2=750.0; y2l2=625.0;
	  if(mLSP>=(y2l2-y1l2)/(x2l2-x1l2)*(Mstop-x1l2)+y1l2) PDFunc_METbin1 = 0.5;
	  else if(mLSP>=(y2l1-y1l1)/(x2l1-x1l1)*(Mstop-x1l1)+y1l1) PDFunc_METbin1 = 0.3;  
	  else PDFunc_METbin1 = 0.15;
	  x1l1=825.0; y1l1=300.0; x2l1=750.0; y2l1=325.0; x1l2=825.0; y1l2=600.0; x2l2=750.0; y2l2=625.0;
	  if(mLSP>=(y2l2-y1l2)/(x2l2-x1l2)*(Mstop-x1l2)+y1l2) PDFunc_METbin2 = 0.5;
	  else if(mLSP>=(y2l1-y1l1)/(x2l1-x1l1)*(Mstop-x1l1)+y1l1) PDFunc_METbin2 = 0.3;  
	  else PDFunc_METbin2 = 0.15;
	  x1l1=825.0; y1l1=275.0; x2l1=750.0; y2l1=300.0; x1l2=825.0; y1l2=475.0; x2l2=750.0; y2l2=500.0;
	  if(mLSP>=(y2l2-y1l2)/(x2l2-x1l2)*(Mstop-x1l2)+y1l2) PDFunc_METbin3 = 0.5;
	  else if(mLSP>=(y2l1-y1l1)/(x2l1-x1l1)*(Mstop-x1l1)+y1l1) PDFunc_METbin3 = 0.3;  
	  else PDFunc_METbin3 = 0.15;
	}

        pdfMETbin1 = PDFunc_METbin1;
        pdfMETbin2 = PDFunc_METbin2;
        pdfMETbin3 = PDFunc_METbin3;

}
