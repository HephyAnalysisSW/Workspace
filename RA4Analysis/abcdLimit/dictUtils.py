#!/usr/bin/env python
import cPickle
import os

def countValues (filename):

    nv = 0
    if filename.endswith(".pkl"):
        mydict = cPickle.load(file(filename))
    elif filename.endswith(".py"):
        exec("from "+os.path.splitext(filename)[0]+ " import "+options.dictName+" as mydict")
    if options.pre!=None:
        preList = options.pre.split(",")
        for p in preList:
            try:
                ip = int(p)
                mydict = mydict[ip]
            except:
                mydict = mydict[p]
    dicts = [ mydict ]
    while len(dicts) > 0:
        d = dicts[0]
        for k in d:
            if type(d[k]) == dict:
                dicts.append(d[k])
            else:
                nv += 1
        dicts.pop(0)
    print "Number of values = ",nv

def dictLayers (filename):
    prefix = ""
#    mydict = cPickle.load(file(filename))
    if filename.endswith(".pkl"):
        mydict = cPickle.load(file(filename))
    elif filename.endswith(".py"):
        exec("from "+os.path.splitext(filename)[0]+ " import "+options.dictName+" as mydict")
    if options.pre!=None:
        preList = options.pre.split(",")
        for p in preList:
            try:
                ip = int(p)
                mydict = mydict[ip]
            except:
                mydict = mydict[p]
    while type(mydict) == dict:
        keys = mydict.keys()
        print prefix,sorted(keys[:options.maxKeys])
        if len(keys) < 1:  break
        mydict = mydict[keys[0]]
        prefix += "  "
        
def dictDump (filename):
    dicts = [ ]
    dicts.append( ( cPickle.load(file(filename)), [ ] ) )
    while len(dicts) > 0:
        if type(dicts[0][0]) == dict:
            keys = dicts[0][0].keys()
            keys.sort()
            keyList = dicts[0][1]
            for key in keys:
                dicts.append( ( dicts[0][0][key], keyList + [ key ] ) )
        else:
            if type(dicts[0][0]) in ( int, float, str ):
                print dicts[0][1]," : ",dicts[0][0]
        dicts.pop(0)

def dictDumpValue (filename,keys):
    dict = cPickle.load(file(filename))
    for key in keys:
        try:
            k = int(key)
        except:
            k = key
        dict = dict[k]
    print keys,dict
#
# find range and spacing of a 1D grid of masses
#   returns tuple of ( delta, min, max )
#
def findRange (ms):
  dm0 = None
  m0 = None
  m0min = None
  m0max = None
  for im in ms:
    if m0 == None:
      m0min = im
      m0max = im
    else:
      dm = abs(im-m0)
      if dm > 0 and ( dm0 == None or dm < dm0 ):  dm0 = dm
      if im < m0min:  m0min = im
      if im > m0max:  m0max = im
    m0 = im;
  return ( dm0,m0min,m0max)
  
def dictToHm0m12 (filename,preTemps,postTemps):
    import ROOT
    from ROOT import gROOT
    from ROOT import gStyle
    gROOT.ProcessLine(".L useNiceColorPalette.C")
    gROOT.ProcessLine("useNiceColorPalette()")
    gStyle.SetOptStat(0)
    d0 = cPickle.load(file(filename))
    d = d0
    msugras = []
    for temp in preTemps:
        print temp
        try:
            itemp = int(temp)
            d = d[itemp]
        except:
            d = d[temp]
    allSugras = d.keys()
#    print d0[1000][250]['msugra_1100_180_10_0_1']
#    print d.keys()[:5]
#    print d['msugra_1100_180_10_0_1']
    first = True
    for msugra in allSugras:
        d1 = d[msugra]
        found = True
        if first:
            print d1
            first = False
        for temp in postTemps:
            if temp == '':  continue
            if temp in d1:
                d1 = d1[temp]
            else:
                found = False
                break
        if found:  msugras.append(msugra)
#    print d['msugra_1100_180_10_0_1']
    m0s = []
    m12s = []
    for msugra in msugras:
        fields = msugra.split('_')
        m0 = int(fields[1])
        m12 = int(fields[2])
        if not m0 in m0s:  m0s.append(m0)
        if not  m12 in m12s:  m12s.append(m12)
    m0s.sort()
    m12s.sort()
    print m0s
    print m12s
    m0range = findRange(m0s)
    m12range = findRange(m12s)

    print m0range
    print m12range
    nb0 = int((m0range[2]-m0range[1])/float(m0range[0])+1.5)
    nb12 = int((m12range[2]-m12range[1])/float(m12range[0])+1.5)
    print nb0,nb12
    h = ROOT.TH2F("h","h",nb0,m0range[1]-m0range[0]/2.,m0range[2]+m0range[0]/2., \
                          nb12,m12range[1]-m12range[0]/2.,m12range[2]+m12range[0]/2.)
    for msugra in msugras:
        fields = msugra.split('_')
        m0 = int(fields[1])
        m12 = int(fields[2])
        d1 = d[msugra]
        for temp in postTemps:
            if temp != '':  d1 = d1[temp]
#        if d1 < 0.0001 :  d1 = 0.0001
        h.Fill(m0,m12,d1)
    h.Draw("zcol")
    try:
        input("Press enter")
    except:
        pass
    

import sys
from optparse import OptionParser
parser = OptionParser()
parser.add_option("-m", "--mode", dest="mode", default="countValues", type="choice", choices=["countValues","dictLayers","dictDump","dictDumpValue","dictToHm0m12"], action="store")
parser.add_option("--count", dest="count", default=False, action="store_true")
parser.add_option("--layers", dest="layers", default=False, action="store_true")
parser.add_option("--dump", dest="dump", default=False, action="store_true")
parser.add_option("--dumpValue", dest="dumpValue", default=False, action="store_true")
parser.add_option("--toHist", dest="toHist", default=False, action="store_true")
parser.add_option("--maxKeys", dest="maxKeys", default=5, type="int", action="store")
parser.add_option("--keys", dest="keys", default="", type="string", action="store")
parser.add_option("--pre", dest="pre", default=None, type="string", action="store")
parser.add_option("--post", dest="post", default=None, type="string", action="store")
parser.add_option("--dictName", dest="dictName", default=None, type="string", action="store")
(options, args) = parser.parse_args()
if len(args) != 1:  sys.exit(1)
if options.count:
    countValues(args[0])
    sys.exit(0)
elif options.layers:
    dictLayers(args[0])
    sys.exit(0)
elif options.dump:
    dictDump(args[0])
    sys.exit(0)
elif options.dumpValue:
    dictDumpValue(args[0],options.keys.split(","))
    sys.exit(0)
elif options.toHist:
    if options.pre == None or options.post == None:  sys.exit(1)
    print options.pre.split(",")
    print options.post.split(",")
    dictToHm0m12(args[0],options.pre.split(","),options.post.split(","))
    sys.exit(0)
