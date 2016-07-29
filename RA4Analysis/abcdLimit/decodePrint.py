#
# decode http://www.hephy.at/user/easilar/tests/print.txt
#
#var = "NONE"
var = "_slope_Up"

res = { }

subres = None
nreg = 0
regs = [ ]
for l in open("print_fixW.txt"):
    fields = l[:-1].split()
    if l.startswith("("):
        assert len(fields)==6
        l1 = l[:-1].replace("("," ")
        l1 = l1.replace(")"," ")
        l1 = l1.replace(","," ")
        fields = l1.split()
        assert len(fields)==6
        ifields = [ int(x) for x in fields ]
        ir1 = ( ifields[0], ifields[1] )
        ir2 = ( ifields[2], ifields[3] )
        ir3 = ( ifields[4], ifields[5] )
        regs.append((ir1,ir2,ir3))
        res[nreg] = { }
        subres = res[nreg]
        nreg += 1
        continue

    ipar = l.find("{")
    if ipar>=0:
        subres[fields[0]] = l[ipar:-1]
        continue

    if len(fields)==2:
        subres[fields[0]] = float(fields[1])
        continue

    if len(fields)==4 and fields[0]=="kappa:":
        if not "kappa" in subres:
            subres["kappa"] = float(fields[1])
        else:
            assert subres["kappa"]==float(fields[1])
        if not "kappa_constUp" in subres:
            subres["kappa_constUp"] = float(fields[2])
            subres["kappa_constDown"] = float(fields[3])
        else:
            subres["kappa_slopeUp"] = float(fields[2])
            subres["kappa_slopeDown"] = float(fields[3])
        continue

    if len(fields)==4 and fields[0].startswith("rCS"):
        for i in range(0,4,2):
            assert not fields[i] in subres
            subres[fields[i]] = float(fields[i+1])
        continue

    if len(fields)==5 and ( fields[0]=="constant" or fields[0]=="slope" ):
        assert fields[1]=="Up" and fields[3]=="down:"
        assert not fields[0]+"Up" in subres
        subres[fields[0]+"Up"] = float(fields[2])
        assert not fields[0]+"Down" in subres
        subres[fields[0]+"Down"] = float(fields[4])
        continue

assert nreg==len(regs)

import ROOT

samples = [
"rest_DY",
"diLep_DY",
"rest_W",
"rest_EWK",
"diLep_tt",
"rest_tt"]

hDYdiLepSB = ROOT.TH1F("hDYdiLepSB","hDYdiLepSB",nreg,-0.5,nreg-0.5)
hTTdiLepSB = ROOT.TH1F("hTTdiLepSB","hTTdiLepSB",nreg,-0.5,nreg-0.5)
hDYdiLepMB = ROOT.TH1F("hDYdiLepMB","hDYdiLepMB",nreg,-0.5,nreg-0.5)
hTTdiLepMB = ROOT.TH1F("hTTdiLepMB","hTTdiLepMB",nreg,-0.5,nreg-0.5)
for ireg in range(nreg):
    reg = regs[ireg]
    if reg[0][1]==-1:
        nj = reg[0][0]
    else:
        nj = (reg[0][0]+reg[0][1])/2.

    subres = res[ireg]
#    for k in subres:
#        if k.startswith("yield_") and not ( k.endswith("Up") or k.endswith("down") or k.endswith("Down") ):
#            print k

    sumYields = { }
    for b in "SB", "MB":
        sumYields[b] = { }
        for phi in "CR", "SR":
            sumY = 0.
            for s in samples:
                k = "yield_"+s+"_"+b+"_in_"+phi+var
                if k in subres:
                    sumY += subres[k]
                else:
                    k = "yield_"+s+"_"+b+"_in_"+phi
                    sumY += subres[k]
            print b,phi,sumY
            sumYields[b][phi] = sumY
    print "RCS/MB = ",sumYields["MB"]["SR"]/sumYields["MB"]["CR"]
    print "RCS/SB = ",sumYields["SB"]["SR"]/sumYields["SB"]["CR"]
    print "kappa = ",(sumYields["MB"]["SR"]/sumYields["MB"]["CR"])/ \
        (sumYields["SB"]["SR"]/sumYields["SB"]["CR"])

#!#     for b in "SB", "MB":
#!#         for phi in "CR", "SR":
#!#             if "yield_diLep_DY_"+b+"_in_"+phi in subres:
#!# #                print ireg,b,phi,subres["yield_diLep_DY_"+b+"_in_"+phi+"_constant_Up"]/subres["yield_diLep_DY_"+b+"_in_"+phi]-1., \
#!# #                    subres["yield_diLep_DY_"+b+"_in_"+phi+"_constant_Down"]/subres["yield_diLep_DY_"+b+"_in_"+phi]-1.
#!#                 if b=="SB":
#!#                     njj = 3.5
#!#                 else:
#!#                     njj = nj
#!#                     print ireg,b,phi,(subres["yield_diLep_DY_"+b+"_in_"+phi+"_slope_Up"]/subres["yield_diLep_DY_"+b+"_in_"+phi]-1.)/(njj-5.2), \
#!#                         (subres["yield_diLep_DY_"+b+"_in_"+phi+"_slope_down"]/subres["yield_diLep_DY_"+b+"_in_"+phi]-1.)/(njj-5.2)

#!#         sumYield = 0.
#!#         for s in samples:
#!#             sumYield += subres["yield_"+s+"_"+b+"_in_CR"]
#!#         print b,sumYield

#!# #    print ireg,(subres["constantUp"]-subres["constantDown"])/2.
