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
              'dy1':           ROOT.kMagenta       ,
              'dy2':           ROOT.kYellow        ,



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
                50: ROOT.kYellow   ,
                60: ROOT.kGreen   ,
                70: ROOT.kSpring   ,
                80: ROOT.kRed   ,
            }

for mstop in  range(100, 601, 25):
    for dm in range(10, 81,  10):
        colors['s%s_%s'%(mstop,mstop-dm)] = dm_color_dict[dm]
        



