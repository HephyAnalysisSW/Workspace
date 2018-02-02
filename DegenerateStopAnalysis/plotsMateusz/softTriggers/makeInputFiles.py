import os
from subprocess import check_output

mStop = 500
mLSP = 460

userDir = "/dpm/oeaw.ac.at/home/cms/store/user/mzarucki"

#sampName = 'T2tt_dM-10to80_mStop-%s_mLSP-%s_SoftTriggers-V15_AODSIM_PU_small'%(mStop,mLSP)
#primaryDataset = ''

sampName = 'T2tt_dM-10to80_mStop-%s_mLSP-%s_HLT_SoftTriggers-V15_PU_HLTDEBUG'%(mStop,mLSP)
primaryDataset = 'T2tt_dM-10to80_mStop-%s_mLSP-%s_privGridpack_GEN-SIM'%(mStop,mLSP)

#sampName = 'TT_SoftTriggers-V15_AODSIM_small'
#sampName = 'WJetsToLNu_SoftTriggers-V15_AODSIM_small'
#primaryDataset = ''

#sampName = 'TT_HLT_SoftTriggers-V15' 
#primaryDataset = 'TT_TuneCUETP8M2T4_13TeV-powheg-pythia8'

#sampName = 'WJetsToLNu_HLT_SoftTriggers-V15'
#primaryDataset = 'WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'

if not primaryDataset:
    primaryDataset = sampName

baseDir = "%s/%s/%s"%(userDir, primaryDataset, sampName)

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

if not os.path.isdir('inputFiles'): os.makedirs('inputFiles')

saveFileName = "inputFiles_%s.txt"%sampName

saveFile = open('inputFiles/%s'%saveFileName, "w")

for i, p in enumerate(rootFilesDirs):
    for f in dpm_ls(p):
        if 'log' in f or 'failed' in f: continue
        saveFile.write("root://hephyse.oeaw.ac.at/{}/{}\n".format(p, f).replace('//dpm/oeaw.ac.at/home/cms/','//'))

print "Saved copy script to inputFiles/", saveFileName 

saveFile.close()
