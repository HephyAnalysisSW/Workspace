import ROOT


custom_colors_rgb = {
    "violet"      : (189, 61,235)      ,    
    "violet2"     : (102, 0,102)      ,    
    "pink"        : (255, 228,206)      ,    
    #"light_blue"  : (0,164,214)         ,        
    "light_blue"  : (74,95,245)         ,        
    "light_blue2" : (27,193,209)         ,        
    "dark_blue"   : (0,26,80)           ,    
    "orange"      : (254,189,38)        ,        
    "red"         : (230,72,30)         ,        
    "dark_green"  : (43,150,82)         ,        
    #"light_green" : (141,185,66)        ,        
    "light_green" : (22,209,92)        ,        
    "grey_green"  : (193,197,158)       ,        
    "yellow"      : (245,208,38)        ,
    "sorkh"       : (235,27,54)         ,



    'z'        :   (254,189,38)  , 
    'dy'       :   (189, 61,235) ,
    'qcd'      :   (102, 0,102)  , 
    'st'       :   (64,224,208)     ,
    'tt'       :   (74,95,245)   ,
    'vv'       :   (43,150,82)   ,
    'w'        :   (22,209,92)   , 
}

custom_colors_rgb_rel = {}
for color, rgb in custom_colors_rgb.iteritems():
    custom_colors_rgb_rel[color] = ( rgb[0]/255. , rgb[1]/255., rgb[2]/255.)

color0 = 1700
custom_colors = {}
i = 0
custom_colors_tc = {} 
for color, rgb in custom_colors_rgb_rel.iteritems():
    custom_colors_tc[color]  = ROOT.TColor(color0+i, *rgb )
    custom_colors[color] = color0+i
    i+=1






colors ={
              'w':             ROOT.kSpring-5       , 
              'tt':            ROOT.kAzure-2        , 
              'tt_1l':         ROOT.kAzure-7        , 
              'tt_2l':         ROOT.kAzure-5        , 
              'z':             ROOT.kOrange + 1     , #ROOT.kOrange + 5         ,#ROOT.kSpring+10       
              #'qcd':           ROOT.kViolet         , 
              'qcd':           ROOT.kMagenta + 3, #ROOT.kRed -6         , 
              'qcdem':         ROOT.kMagenta - 3, #ROOT.kRed -6         , 
              'wtau':          ROOT.kSpring-2       ,
              'wnotau':        ROOT.kSpring+2       ,
              'dy5to50':       ROOT.kMagenta       ,
              'dy5to50Inc':    ROOT.kViolet        ,
              'dy':            ROOT.kViolet-3        ,
              'dyInv':         ROOT.kViolet-4        ,

              'st_tch_lep':    ROOT.kAzure-10        ,
              'st':        ROOT.kAzure+5        ,
              'st_tch':        ROOT.kAzure+5        ,
              'st_wch':        ROOT.kCyan-3        ,
              'vv':            ROOT.kSpring-7        ,

              "s30":           ROOT.kRed+1          , 
              "s60FS":         ROOT.kOrange +7      , 
              "s30FS":         ROOT.kYellow -3       , 
              "s10FS":         ROOT.kAzure  +7      , 
              "t2tt30FS":      ROOT.kOrange-1       , 

              'ttx':            ROOT.kAzure-4        , 
              #'tt':            ROOT.kAzure-2        , 
            }

for htbin in range(8):
    colors['w%s'%htbin]=ROOT.kSpring-i

colors.update({
        'w0': ROOT.kGreen   ,  
        'w1': ROOT.kSpring - 6  ,  
        'w2': ROOT.kTeal  -7   ,  
        'w3': ROOT.kGreen + 2   ,  
        'w4': ROOT.kYellow -3  ,  
        'w5': ROOT.kGreen - 6  ,  
        #'w6': ROOT.kGreen - 7  ,  
        'w6': ROOT.kYellow - 5  ,  
        'w7': ROOT.kTeal -9  ,  
        'w8': ROOT.kGreen - 8  ,  
        })


new_colors ={
              #'z'        :     custom_colors['z'  ],
              'dy'       :     custom_colors['dy' ],
              #'qcd'      :     custom_colors['qcd'],
              'st'       :     custom_colors['st' ],
              #'tt'       :     custom_colors['tt' ],
              #'vv'       :     custom_colors['vv' ],
              #'w'        :     custom_colors['w'  ],
}

colors.update(new_colors)


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


max_mstop = 800
min_mstop = 250
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
        colors['%s_%s'%(mstop,mstop-dm)] = dm_color_dict[dm] # + int(mstop/10.) -10
        #colors['s%s_%s'%(mstop,mstop-dm)] = ic
        

sampleNames = {
 'dy': 'DYJetsM50',
 'qcd': 'QCD',
 #'s300_220': 'T2tt-300-220',
 #'s300_270': 'T2tt-300-270',
 #'s300_290': 'T2tt-300-290',
 'st': 'ST',
 'tt': 'TTJets',
 'vv': 'Diboson',
 'w': 'WJets',
 'z': 'ZJetsInv'}

for samp in sampleNames:
    colors[sampleNames[samp]]=colors[samp]

