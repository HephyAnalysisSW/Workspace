import math 


## --------------------------------------------------------------
##                        Figure of Merit Tools
## --------------------------------------------------------------

def AMSSYS (s,b,sysUnc=0.2):
  #print s, b
  if s==0: 
    return 0
  if b==0: 
    return -1
  #return (lambda s,b : math.sqrt(2*( (s+b)*math.log(((s+b)*(b+sysUnc*b))/(b*b+(s+b)*sysUnc*b))  - b*b/(sysUnc*b)*math.log(1+sysUnc*b*s/(b*(b+sysUnc*b))) )) if b!=0 else -1)(s,b)
  ret = math.sqrt(2*( (s+b)*math.log(((s+b)*(b+ (sysUnc*sysUnc*b*b) ))/(b*b+(s+b)* (sysUnc*sysUnc*b*b) ))  - b*b/( (sysUnc*sysUnc*b*b) )*math.log(1+ (sysUnc*sysUnc*b*b) *s/(b*(b+ (sysUnc*sysUnc*b*b) ))))) 
  return ret 

fomFuncs= {
                "SOB"         : lambda s,b,sysUnc  : s/math.sqrt(b) if b!=0 else -1 ,
                "SOBSYS"      : lambda s,b,sysUnc : s/math.sqrt(b+(sysUnc*sysUnc*b*b) ) if b!=0 else -1 ,
                "AMS"         : lambda s,b,sysUnc : math.sqrt(2*((s+b)*math.log(1+1.*s/b)-s) ) if b!=0 else -1 ,
                "AMSSYS"      : AMSSYS ,
            }

def calcFOMs(s,b,sysUnc=0.2,fom=None):
  if fom: 
    return fomFuncs[fom](s,b,sysUnc)
  else:
    ret = {}
    for f in fomFuncs:
      ret[f]=fomFuncs[f](s,b,sysUnc)
    return ret

