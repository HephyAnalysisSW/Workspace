{
	#include <string>
	string includePath(gSystem->GetIncludePath());
	gSystem->SetIncludePath((includePath+" -I$ROOFITSYS/include").c_str());
    gSystem->Load("/afs/cern.ch/cms/slc5_amd64_gcc462/external/boost/1.51.0/lib/libboost_math_tr1.so");
	gSystem->AddIncludePath("-I/afs/cern.ch/cms/slc5_amd64_gcc462/external/boost/1.51.0/include");
	gROOT->ProcessLine(".L RooMinuitSumW2.cxx+");
//	gROOT->ProcessLine(".L owens.cxx+");
	gROOT->ProcessLine(".L RooSkewErf.cxx+");
	gROOT->ProcessLine(".L RooPareto.cxx+");
	gROOT->ProcessLine(".L RooMETConv.cxx+");

}
