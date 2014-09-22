import string

lastF0 = ""
lastF1 = ""
lastF4 = ""
minFields = 7
lastFs = [ ]
for i in range(minFields):
    lastFs.append("")
tmpSysts = { }
for line in file("Things-to-be-recalled.csv"):
    fields = line.split(",")
    if len(fields)<minFields or fields[6]=="": continue
    for i in range(minFields):
        if len(fields[i])>0:
            fields[i] = filter(lambda x: ord(x)>=32, fields[i])
            fields[i] = fields[i].lstrip()
            fields[i] = fields[i].rstrip()
        if fields[i] != "":
            fields[i] = fields[i].replace('"',"")
            lastFs[i] = fields[i]
        else:
            fields[i] = lastFs[i]
    if fields[2].count("same as Jes Ref")>0:
        fields[2] = "weight"
    tmpSysts[(fields[0],fields[1])] = fields[:minFields]

#
# special tweaks
#
tmpKeys = tmpSysts.keys()
tmpKeys.sort()
for tmpKey in tmpKeys:
    if ( tmpKey[0] == "W+bb" ) and ( tmpKey[1].count("include")>0 and tmpKey[1].count("Wbb")>0 ): 
        tmpSysts[tmpKey][1] = '+'
    ind = tmpSysts[tmpKey][4].find(" (_seperateBTagWeights)")
    if ind >= 0:  tmpSysts[tmpKey][4] = tmpSysts[tmpKey][4][:ind]

allSysts = [ ]
for tmpKey in tmpKeys:
    allSysts.append(tmpSysts[tmpKey])

print "allSysts = ",allSysts
