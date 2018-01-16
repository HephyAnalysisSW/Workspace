import os
from subprocess import check_output

mStop = 500
mLSP = 420

sampName = "T2tt_dM-10to80_privGridpack_LHE-GEN-SIM-RAW_mStop-%s_mLSP-%s_PU"%(mStop, mLSP)
userDir = "/dpm/oeaw.ac.at/home/cms/store/user/mzarucki"
baseDir = "%s/%s/%s"%(userDir, sampName, sampName)

baseSaveDir = "/afs/hephy.at/data/mzarucki02/TriggerStudies/CMSSW_9_2_12/GEN-SIM-RAW"

def dpm_ls(d):
    stdout = check_output(["dpns-ls", d])
    dirsOrFiles = stdout.split()
    return dirsOrFiles

def fileInList(l, f=".root"):
    for il in l:
        if f in il:
            return True
    return False

def good_dpm_ls(path):
    try:
        return dpm_ls(path)
    except:
        print "Illegal path."
        return False

fileExt = '.root'

def walk_dpm(path): 

    dirsOrFiles = good_dpm_ls(path)
    ret = []
    if not dirsOrFiles:
        return False
    if fileInList(dirsOrFiles, fileExt):
        print "Found a %s file in %s"%(fileExt, path)
        return [path]
    for d in dirsOrFiles:
        if '.log.tar.gz' in d: continue # ignores tarred files
        new_path = path + "/" + d
        print "Looking in:", new_path
        ret_ = walk_dpm(new_path)
        if ret_:
            ret.extend(ret_)
    return ret

rootFilesDirs = walk_dpm(baseDir)

# Make a .sh script to copy the contents of the directory with the root files into a new dir in the baseSaveDir (named after the sample)

saveFileName = "copyFromDPM_%s.sh"%sampName

saveFile = open(saveFileName, "w")

for i, p in enumerate(rootFilesDirs):
    finalSaveDir = "%s/%s/%s"%(baseSaveDir, sampName, i)
    if not os.path.isdir(finalSaveDir): os.makedirs(finalSaveDir)
    for f in dpm_ls(p):
        saveFile.write("xrdcp root://hephyse.oeaw.ac.at/%s/%s %s\n"%(p, f, finalSaveDir))

print "Saved copy script to", saveFileName 

saveFile.close()
