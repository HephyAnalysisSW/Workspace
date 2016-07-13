


make_stop_lsp_list = lambda mstop_range, dm_range: [ (mstop,mstop-dm) for mstop in mstop_range for dm in dm_range ]
t2_4bd_sample_string = lambda mstop,mlsp : "SMS_T2_4bd_mStop_%s_mLSP_%s"%(mstop,mlsp)


mstop_range   = range(100,451, 25) 
dm_range_low  = range(10, 30,  10) 
dm_range_mid  = range(30, 60,  10) 
dm_range_high = range(60, 81,  10) 
dm_range_all  = range(10, 81,  10) 


dm_ranges =          { 
                        "lowDM":   dm_range_low     ,
                        "midDM":   dm_range_mid     ,
                        "highDM":  dm_range_high    ,
                        "allDM":   dm_range_all     ,     
                     }  




class MassPoints():
    def __init__(self, dm_range_string , mstop_range = (100,451,25) ):
        allowed_dm_ranges = dm_ranges.keys()
        if not dm_range_string in allowed_dm_ranges:
            raise Exception("DeltaM Range %s, Not Recognized in %s"%(dm_range_string, allowed_dm_ranges))
        self.dm_range = dm_ranges[dm_range_string]
        self.mstops = range(*mstop_range )

        mstops_lsps_ranges = { 
                        "lowDM":   make_stop_lsp_list(  self.mstops , dm_range_low) ,
                        "midDM":   make_stop_lsp_list(  self.mstops , dm_range_mid) ,
                        "highDM":  make_stop_lsp_list(  self.mstops , dm_range_high),
                        "allDM":   make_stop_lsp_list(  self.mstops , dm_range_all) ,   
                             } 
        self.mstop_lsps = mstops_lsps_ranges[dm_range_string]
        self.testPoints = [ (mstop,mlsp) for mstop,mlsp in self.mstop_lsps if mstop==300]
        self.sigList    = [ "s%s_%s"%(mstop,mlsp) for mstop,mlsp in self.mstop_lsps ]
        self.sampleStrings = [ t2_4bd_sample_string(mstop,mlsp) for mstop,mlsp in self.mstop_lsps ]
        #self.benchMarksMasses = [ (mstop,mlsp) for mstop,mlsp in self.mstop_lsps if mstop==300 ]

        

if __name__ == "__main__":
    lowDMs = MassPoints("lowDM")
    print lowDMs.sampleStrings

