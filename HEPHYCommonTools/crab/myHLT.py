#!/usr/bin/env python 
from sys import stderr, exit
import commands
import json
import subprocess
import sys
#
# E.P., 27 July 2010
# query to the Run Reistry taken from a script by Giovanni Petrucianni
#


from optparse import OptionParser
parser = OptionParser(usage="usage: %prog [options] ")
parser.add_option("--json",  dest="json",  help="JSON file", type="string", default="")
parser.add_option("--dataSets",  dest="dataSets",  help="list of dataset names", type="string", default="")
parser.add_option("--groupName", dest="groupName", help="select runs of name like NAME", metavar="NAME", default="Collisions%")
parser.add_option("--rrurl",     dest="rrurl",     help="run registry xmlrpc url", metavar="URL", default="http://cms-service-runregistry-api.web.cern.ch/cms-service-runregistry-api/xmlrpc")
parser.add_option("--HLTkey",    dest="HLTkey",    help="name of the HLTkey e.g. /cdaq/physics/Run2010/v3.1/HLT_1.6E30/V1",metavar="HLT")
parser.add_option("--perKey",    action="store_true",default=False,dest="perKey",help="list the runs per HLT key",metavar="perKey")
(options, args) = parser.parse_args()

def queryRR(firstRun,lastRun):
    stderr.write("Querying run registry for range [%d, %d], group name like %s ...\n" % (firstRun, lastRun, options.groupName))
    import xmlrpclib
    import xml.dom.minidom
    server = xmlrpclib.ServerProxy(options.rrurl)
    run_data = server.DataExporter.export('RUN', 'GLOBAL', 'xml_datasets', "{runNumber} >= %d AND {runNumber} <= %d AND {groupName} like '%s' AND {datasetName} = '/Global/Online/ALL'"  % (firstRun, lastRun, options.groupName))
    ret = {}
    xml_data = xml.dom.minidom.parseString(run_data)
    xml_runs = xml_data.documentElement.getElementsByTagName("RUN_DATASET")
    for xml_run in xml_runs:
        ret[xml_run.getElementsByTagName("RUN_NUMBER")[0].firstChild.nodeValue] = xml_run.getElementsByTagName("RUN_HLTKEY")[0].firstChild.nodeValue
    return ret

assert options.json != ""
jsonFile = open(options.json)
fromJSON = json.load(jsonFile)
jsonFile.close()

datasetList = [ ]
if options.dataSets != "":  datasetList = options.dataSets.split(",")

#runsJSON = []
#for key in fromJSON:
#	runsJSON.append(int(key))
#runsJSON.sort()
runsJSON = fromJSON.keys()
runsJSON.sort()
assert len(runsJSON) > 0

print runsJSON[0],runsJSON[-1]

runKeys = queryRR(int(runsJSON[0]),int(runsJSON[-1]))
runsRR = runKeys.keys(); runsRR.sort()


lastKey = None
runsPerKey={}
for run in runsJSON:
	if not run in runsRR:
		print "run ",run," missing in ",runsRR
	assert run in runsRR
	
	key = runKeys[run]
	if lastKey == None or key != lastKey:
		if not key in runsPerKey.keys():
			tmpruns=[]
			tmpruns.append(run)
			runsPerKey[key] = tmpruns
			lastKey = key
		else:
			print "Back to key ",key," for run ",run," ?!!"
			runsPerKey[key].append(run)
			lastKey = key
	else:
		runsPerKey[key].append(run)
theKeys = runsPerKey.keys()


for key in theKeys:
    theruns = runsPerKey[key]
    topr=""
#    for r in theruns:
#        topr=topr+"\t"+r
#    print key,topr
    sys.stderr.write("\n")
    sys.stderr.write("*******************************************************************************************\n")
    sys.stderr.write("HLT Key "+key+"\n")
    sys.stderr.write("Runs    "+",".join(runsPerKey[key])+"\n")
    sys.stderr.write("*******************************************************************************************\n")
#    sys.stderr.write("\n")

    cmdline = "edmConfigFromDB --orcoff --configName "+key+" --format streams.list:A"
    p = subprocess.Popen(cmdline.split(),stdout=subprocess.PIPE)
    p.wait()
    pathsByDataset = {}
    for l in p.stdout.readlines():
        if len(l) > 1:
            l = l[0:-1]
            pathsByDataset[l] = [ ]
    datasetsByPath = {}
    for dset in pathsByDataset:
        if options.dataSets != "" and dset not in datasetList:  continue
        sys.stderr.write("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
        sys.stderr.write("Dataset "+dset+"\n")
        sys.stderr.write("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
        cmdline = "edmConfigFromDB --orcoff --configName "+key+" --format streams.list:A."+dset
        p = subprocess.Popen(cmdline.split(),stdout=subprocess.PIPE)
        p.wait()
        for l in p.stdout.readlines():
            if len(l) > 1:
                l = l[0:-1]
                pathsByDataset[dset].append(l)
                if not l in datasetsByPath:
                    datasetsByPath[l] = dset
                else:
                    print "**** multiple datasets for path ",l,dset,datasetsByPath[l]
        if len(pathsByDataset[dset]) == 0:  continue
        cmdline = "edmConfigFromDB --orcoff --configName "+key+" --paths "+",".join(pathsByDataset[dset])+" --format summary.ascii"
        p = subprocess.Popen(cmdline.split())
        p.wait()
        

exit
