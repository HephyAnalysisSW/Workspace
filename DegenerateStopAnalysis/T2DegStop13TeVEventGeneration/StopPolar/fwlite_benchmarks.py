''' Benchmark samples for TopEFT (EDM)'''

# standard imports
import os

# RootTools
from RootTools.core.standard import *

# Top EFT
from TopEFT.Tools.user import results_directory 

dbFile = os.path.join( results_directory, 'sample_cache', 'fwlite_benchmarks.db')

# Logging
if __name__ == "__main__":
    import TopEFT.Tools.logger as logger
    logger = logger.get_logger('DEBUG')
    import RootTools.core.logger as logger_rt
    logger_rt = logger_rt.get_logger('DEBUG')

# FWLite TTZ benchmarks, first shot with approx same x-Sec of 0.5pb
#fwlite_ttZ_sm   = FWLiteSample.fromFiles( "SM", texName = "SM", files = ["/data/rschoefbeck/TopEFT/GEN/ewkDM_ttZ.root"] , dbFile = dbFile)
#fwlite_ttZ_bm1  = FWLiteSample.fromFiles( "C1Vm1p0_C1A0p5", texName = "C1V=-1.0 C1A=0.5", files = ["/data/rschoefbeck/TopEFT/GEN/ewkDM_ttZ_DC1A_0.500000_DC1V_-1.000000.root"] , dbFile = dbFile)
#fwlite_ttZ_bm2  = FWLiteSample.fromFiles( "C1V0p5_C1A0p5",  texName = "C1V=0.5 C1A=0.5", files = ["/data/rschoefbeck/TopEFT/GEN/ewkDM_ttZ_DC1A_0.500000_DC1V_0.500000.root"] , dbFile = dbFile)

# dipole moments = 0, approx SM LO x-sec
# fwlite_ttZ_ll_LO_sm                   = FWLiteSample.fromDAS("ttZ_ll_LO_sm", "/ewkDM_ttZ_ll/schoef-ewkDM-e1a069162e896efecc10f859afdda0d0/USER", "phys03", dbFile = dbFile)
# fwlite_ttZ_ll_LO_DC1V_0p5_DC1A_0p5    = FWLiteSample.fromDAS("ttZ_ll_LO_DC1V_0p5_DC1A_0p5", "/ewkDM_ttZ_ll_DC1A_0p500000_DC1V_0p500000/schoef-ewkDM-863d441c1e97429a518397b2b60fd1be/USER", "phys03", dbFile = dbFile, overwrite=False)
# fwlite_ttZ_ll_LO_DC1V_m1_DC1A0p5      = FWLiteSample.fromDAS("ttZ_ll_LO_DC1V_m1_DC1A0p5", "/ewkDM_ttZ_ll_DC1A_0p500000_DC1V_m1p000000/schoef-ewkDM-ff3cbbd709193316b9c63feda6313fd2/USER", "phys03", dbFile = dbFile, overwrite=False)

# benchmark from https://arxiv.org/pdf/1501.05939.pdf
#dim6top_LO_ttZ_ll_ctZ_1p20_ctZI_2p00    = FWLiteSample.fromFiles("dim6top_LO_ttZ_ll_ctZ_1p20_ctZI_2p00"   , texName="", files = ["/afs/hephy.at/data/dspitzbart01/TopEFT/genSamples//dim6top_LO_ttZ_ll_ctZ_1p200000_ctZI_2p000000/events.root"])

T2tt_mStop_500_mLSP_460_test = FWLiteSample.fromFiles("T2tt_mStop_500_mLSP_460_test" , files = ["./Generation/production/T2tt_dM-10to80_privGridpack_LHE-GEN_mStop-500_mLSP-460_noPU.root"] )
T2tt_test = FWLiteSample.fromFiles("test_GEN", files = ["./Generation/production/test_GEN.root"] )
T2tt_off = FWLiteSample.fromFiles("T2ttoff", files = ["./Generation/production/T2ttoff_GEN.root"] )

