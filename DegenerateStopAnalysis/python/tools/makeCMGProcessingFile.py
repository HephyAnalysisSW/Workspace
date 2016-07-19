

import re
import pickle


def getBin(name):
    name = name[:name.index("to")]
    return int( re.split('_|-|Pt|HT', name)[-1] )

l = lambda x: int(re.split('_|-|to' ,x[0])[-2])



import os





def printSample(compName, comp):
    sampleName = "_".join(comp.dataset.split("/")[1:3])
    xsec = comp.xSection if not comp.isData else None
    temp =\
"""

{compName} ={{
'cmgName':"{compName}"
"name" : "{sampleName}",
#"name" : comp.name,
"chunkString":"{sampleName}",
"dir": sample_path +"/" + "{sampleName}",
"dbsName" : "{dbsName}",
"rootFileLocation":"tree.root",
"treeName":"tree",
"isData": {isData},
"xsec": {xsec},
}}
allComponents.append({compName})

""".format(sampleName=sampleName, isData= comp.isData , dbsName = comp.dataset , xsec = xsec, compName = compName)
    print temp
    return temp

def printCMGProcessingFile(cmgPickle, mc_dir = "./", data_dir="./" , output_dir ="./", write = True):
    #output_dir  = "$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/python/samples/cmgTuples/"
    output_dir  = os.path.expandvars(output_dir)
    tag = os.path.splitext(os.path.basename(cmgPickle))[0]
    componentDict = pickle.load(file(cmgPickle))
    data_output = []
    mc_output   = []
    data_output.append("sample_path = '%s'"%data_dir)
    mc_output.append("sample_path = '%s'"%mc_dir)
    for compName, comp in  componentDict.iteritems():
        if not comp.isData:
            mc_output.append( printSample(compName, comp)) 
        else:
            data_output.append( printSample(compName, comp)  )
    if len(data_output)>1:
        data_file_path = output_dir +"/Data25ns_%s.py"%tag
        data_file = open( data_file_path ,'w')
        for l in data_output:
            data_file.write(l)
        print "Data CMGProcessing sample file written to %s"%data_file_path
        data_file.close()
    if len(mc_output)>1:
        mc_file_path = output_dir +"/RunIISpring16_%s.py"%tag
        mc_file = open( mc_file_path ,'w')
        for l in mc_output:
            mc_file.write(l)
        mc_file.close()
        print "MC CMGProcessing sample file written to %s"%mc_file_path
    return {'data': data_output, 'mc':mc_output }


if __name__ == '__main__':

    cmgPickle = "/afs/cern.ch/user/n/nrad/CMSSW/CMSSW_8_0_11/src/CMGTools/SUSYAnalysis/cfg/crab_with_das/8011_mAODv2_v1.pkl"
    out = printCMGProcessingFile(cmgPickle)

