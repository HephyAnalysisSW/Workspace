import ROOT
colors ={
              'w':             ROOT.kSpring-5       , 
              'tt':            ROOT.kAzure-5        , 
              'z':             ROOT.kOrange + 1     , #ROOT.kOrange + 5         ,#ROOT.kSpring+10       
              #'qcd':           ROOT.kViolet         , 
              'qcd':           ROOT.kMagenta + 3, #ROOT.kRed -6         , 
              'qcdem':         ROOT.kMagenta - 3, #ROOT.kRed -6         , 
              'wtau':          ROOT.kSpring-2       ,
              'wnotau':        ROOT.kSpring+2       ,
              'dy5to50':       ROOT.kMagenta       ,
              'dy5to50Inc':    ROOT.kViolet        ,
              'dy':            ROOT.kViolet-3        ,
              'dyInv':         ROOT.kViolet+3        ,



              "s30":           ROOT.kRed+1          , 
              "s60FS":         ROOT.kOrange +7      , 
              "s30FS":         ROOT.kYellow -3       , 
              "s10FS":         ROOT.kAzure  +7      , 
              "t2tt30FS":      ROOT.kOrange-1       , 
            }



dm_color_dict ={
                10: ROOT.kBlue     ,
                20: ROOT.kViolet   ,
                30: ROOT.kMagenta   ,
                40: ROOT.kOrange      ,
                50: ROOT.kYellow + 3  ,
                60: ROOT.kGreen   ,
                70: ROOT.kSpring   ,
                80: ROOT.kRed   ,
            }

new_colors = {}


max_mstop = 600
min_mstop = 100
max_dm   = 80
min_dm   = 10
mstop_range = range(min_mstop, max_mstop+1, 25)
dm_range    = range(min_dm, max_dm+1,  10)
for ims , mstop in  enumerate( mstop_range):
    for idm , dm in enumerate(dm_range):
        mlsp = mstop - dm
        #ic = int( 300+ims*10 + idm  )
        #r   = 1. * mstop / max_mstop   
        #g   = 1. * mstop / max_mstop
        #b   = 1. * dm    / max_dm
        #new_colors[ic] = ROOT.TColor(ic, r,g,b)
        #print ic
        colors['s%s_%s'%(mstop,mstop-dm)] = dm_color_dict[dm] # + int(mstop/10.) -10
        #colors['s%s_%s'%(mstop,mstop-dm)] = ic
        



