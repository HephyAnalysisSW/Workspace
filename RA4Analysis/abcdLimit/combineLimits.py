#
# Loop over all limit_*_*.log files in a directory and produce a summary.
# The summary is indexed by m_gluino, m_lsp, and the quantile (as in the combine output).
# Arguments:
#   - directory with the input files
#   - name of the output pickle file (optional; default = <directory name>.pkl
#
import os,sys
from fnmatch import fnmatch
import pickle

#
# Read results from the log file:
#   compare mass info with file name
#   read dictionary string with results
#
def parseLogFile(fn,smglu,smlsp):
    fields = None
    for i,l in enumerate(open(fn)):
        if i>1:
            print "*** log file parsing failed for ",fn
            return None
        idx = l.find("{")
        if idx<0:
            print "*** log file parsing failed for ",fn
            return None
        hdr = l[:idx]
        lims = eval(l[idx:-1])
        fields = hdr.split()
        if not ( len(fields)==7 and fields[0]=="Result" ):
            print "*** log file parsing failed for ",fn
            return None
        if not ( fields[4]==smglu and fields[5]==smlsp ):
            print "*** log file parsing failed for ",fn
            return None
    if fields==None:
        print "No results for ",fn
        return None
    return [ int(fields[4]), int(fields[5]), lims ]
#
# require at least one argument
#
assert len(sys.argv)>=2
# directory
indir = sys.argv[1]
assert os.path.isdir(indir)
# output file (do not overwrite)
if len(sys.argv)>2:
    out = sys.argv[2]
else:
    out = os.path.basename(os.path.normpath(indir))
    assert len(out)>0
    out += ".pkl"
#
# loop over files and keep count of successful reads
#
results = { }
nsucc = 0
nfail = 0
for f in os.listdir(indir):
    if not fnmatch(f,"limit_[0-9]*_[0-9]*.log"):
        continue
    ffields = f.split(".")[0].split("_")
    assert len(ffields)==3
    assert ffields[1].isdigit() and ffields[2].isdigit()
    parseRes = parseLogFile(indir+"/"+f,ffields[1],ffields[2])
    if parseRes==None:
        nfail += 1
        continue
    mglu,mlsp,lims = parseRes
    if not mglu in results:
        results[mglu] = { }
    assert not ( mlsp in results[mglu])
    ## *** temporary
    #if mglu<1000:
    #    for l in lims:
    #        lims[l] /= 100.
    ## *** temporary
    results[mglu][mlsp] = lims
    nsucc += 1

print "Successfully parsed",nsucc,"files (",nfail,"files failed)"
#
# write summary to pickle file
#
assert not os.path.exists(out)
fout = open(out,"wb")
pickle.dump(results,fout)
fout.close()
