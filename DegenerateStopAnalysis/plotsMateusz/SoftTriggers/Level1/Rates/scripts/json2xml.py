#!/bin/env python
#
# @author: Takashi MATSUSHITA
#

import argparse
import json
import sys
import types


##
## constants
##

TYPE2NAME = {
  0: "ETT",     # should be equal to L1Analysis::EtSumType::kTotalEt
  1: "HTT",     # should be equal to L1Analysis::EtSumType::kTotalHt
  2: "ETM",     # should be equal to L1Analysis::EtSumType::kMissingEt
  3: "HTM",     # should be equal to L1Analysis::EtSumType::kMissingHt
  8: "ETMHF",   # should be equal to L1Analysis::EtSumType::kMissingEtHF
  11: "MBT0HFP",    # should be equal to L1Analysis::EtSumType::kMinBiasHFP0
  12: "MBT0HFM",    # should be equal to L1Analysis::EtSumType::kMinBiasHFM0
  13: "MBT1HFP",    # should be equal to L1Analysis::EtSumType::kMinBiasHFP1
  14: "MBT1HFM",    # should be equal to L1Analysis::EtSumType::kMinBiasHFM1
  16: "ETTEM",      # should be equal to L1Analysis::EtSumType::kTotalEtEm
  21: "TOWERCOUNT", # should be equal to L1Analysis::EtSumType::kTowerCount
  10000: "MU",
  10001: "EG",
  10002: "JET",
  10003: "TAU",
  20000: "DETA",
  20001: "DPHI",
  20002: "DR",
  20003: "MASS",
}

BX2NAME = {
  -2: "-2",
  -1: "-1",
   0: "",
   1: "+1",
   2: "+2"
}

OP2NAME = {
    1: "AND",
    2: "OR",
    3: "NOT"
}


# algorithm block
ALGORITHM = """<algorithm>
  <name>{name}</name>
  <expression>{expression}</expression>
  <index>9999</index>
  <module_id>9999</module_id>
  <module_index>9999</module_index>{body}
</algorithm>
"""

# object block
OBJECT = """
  <object_requirement>
    <name>{name}</name>
    <type>{type}</type>
    <comparison_operator>.ge.</comparison_operator>
    <threshold>{threshold}</threshold>
    <bx_offset>{bx_offset}</bx_offset>
  </object_requirement>"""

# external block
EXTERNAL = """
  <external_requirement>
    <name>{name}</name>
    <bx_offset>{bx_offset}</bx_offset>
  </external_requirement>"""

# cut block
CUT = """
  <cut>
    <name>{name}</name>
    <object>{object}</object>
    <type>{type}</type>
    <minimum>{minimum}</minimum>
    <maximum>{maximum}</maximum>
    <data>{data}</data>
  </cut>"""



class Base:
  def __init__(self):
    pass

  def setAttributes(self, initial_data, kwargs):
    for dictionary in initial_data:
      for key in dictionary:
        setattr(self, key, dictionary[key])
      for key in kwargs:
        setattr(self, key, kwargs[key])

  def getAttributes(self):
    return [k for k in self.__dict__.keys() if not k.startswith('__') and not k.endswith('__')]



class Cut(Base):
  FORMAT="{0:+23.16E}"

  def __init__(self):
    Base.__init__(self)
    self.cuts = []
    self.called = False


  def getRangeName(self, boundary):
    rc = ""
    if (abs(boundary['minimum']) - (boundary['maximum'])) <= 2.*sys.float_info.epsilon:
      rc = "{0:4.2f}".format(boundary['maximum']).replace(".", "p")
    else:
      rc = "{0:4.2f}_{1:4.2f}".format(boundary['minimum'], boundary['maximum']).replace(".","p").replace("-","m")
    return rc


  def setRange(self, object_name, key, boundary):
    minimum = Cut.FORMAT.format(boundary['minimum'])
    maximum = Cut.FORMAT.format(boundary['maximum'])

    cut = ({"object": object_name})
    cut.update({"type": "%s" % key})
    cut.update({"minimum": minimum})
    cut.update({"maximum": maximum})
    cut.update({"data": ""})
    cut.update({"name": "%s" % (self.getName(object_name, key) + self.getRangeName(boundary))})
    self.cuts.append(cut)


  def getCuts(self):
    self.setCuts()

    rc = {}
    for cut in self.cuts:
      rc.update({cut['name']: CUT.format(**cut)})
    return rc



class ObjectCut(Cut):
  MAX_LUT_BITS = 4

  NO_QUALITY = 0xFFFF
  MU_QLTY_SNGL = 0xF000
  MU_QLTY_DBLE = 0xFF00
  MU_QLTY_OPEN = 0xFFF0
  NO_ISOLATION = 0xF

  def __init__(self, *initial_data, **kwargs):
    Cut.__init__(self)
    self.setAttributes(initial_data, kwargs)


  def getThreshold(self):
    exp = "%s" % self.threshold
    exp = exp.replace(".0", "")
    exp = exp.replace(".", "p")
    return exp


  def getBx(self):
    return BX2NAME[self.bx]


  def getObjectName(self):
    return "{0}{1}{2}".format(TYPE2NAME[self.type], self.getThreshold(), self.getBx())


  def getName(self, object_name, key):
    return "%s-%s_" % (object_name, key)


  def setCharge(self):
    cut = ({"object": TYPE2NAME[self.type]})
    cut.update({"type": "CHG"})
    cut.update({"minimum": '+0.0000000000000000E+00'})
    cut.update({"maximum": '+0.0000000000000000E+00'})

    charge = ""
    if self.charge == 1:
      charge = "positive"
    elif self.charge == -1:
      charge = "negative"

    cut.update({"name": "CHG_" + charge})
    cut.update({"data": charge})
    self.cuts.append(cut)


  def setQuality(self):
    object_name = TYPE2NAME[self.type]
    cut = ({"object": object_name})
    cut.update({"type": "QLTY"})
    cut.update({"minimum": '+0.0000000000000000E+00'})
    cut.update({"maximum": '+0.0000000000000000E+00'})

    quality = ""
    if object_name == "MU":
      if self.quality == ObjectCut.MU_QLTY_SNGL:
        quality = "MU-QLTY_SNGL"
      elif self.quality == ObjectCut.MU_QLTY_DBLE:
        quality = "MU-QLTY_DBLE"
      elif self.quality == ObjectCut.MU_QLTY_OPEN:
        quality = "MU-QLTY_OPEN"
    else:
      quality = "0x{:X}".format(self.isolation)

    cut.update({"name": quality})
    cut.update({"data": self.toData(self.quality)})
    self.cuts.append(cut)


  def setIsolation(self):
    object_name = TYPE2NAME[self.type]
    cut = ({"object": object_name})
    cut.update({"type": "ISO"})
    cut.update({"minimum": '+0.0000000000000000E+00'})
    cut.update({"maximum": '+0.0000000000000000E+00'})

    isolation = "0x{0:X}".format(self.isolation)

    cut.update({"name": object_name + "-ISO_" + isolation})
    cut.update({"data": self.toData(self.isolation)})
    self.cuts.append(cut)


  def toData(self, value):
    bits = []
    for bit in range(2**ObjectCut.MAX_LUT_BITS):
      if value & 1 << bit:
        bits.append("{0:d}".format(bit))

    return ",".join(bits)


  def setCuts(self):
    if not self.called:
      if self.eta1['minimum'] != self.eta1['maximum']:
        self.setRange(TYPE2NAME[self.type], "ETA", self.eta1)

        if self.eta2['minimum'] != self.eta2['maximum']:
          self.setRange(TYPE2NAME[self.type], "ETA", self.eta2)

      if self.phi1['minimum'] != self.phi1['maximum']:
        self.setRange(TYPE2NAME[self.type], "PHI", self.phi1)

        if self.phi2['minimum'] != self.phi2['maximum']:
          self.setRange(TYPE2NAME[self.type], "PHI", self.phi2)

      if self.charge:
        self.setCharge()

      if self.quality != ObjectCut.NO_QUALITY:
        self.setQuality()

      if self.isolation != ObjectCut.NO_ISOLATION:
        self.setIsolation()

    self.called = True


  def getObject(self):
    object = {}
    object.update({"name": self.getObjectName()})
    object.update({"type": TYPE2NAME[self.type]})
    object.update({"threshold": Cut.FORMAT.format(self.threshold)})
    object.update({"bx_offset": self.bx})
    return object


  def getExpression(self):
    self.setCuts()
    cuts = []
    for cut in self.cuts:
      cuts.append(cut['name'])
    cut = ",".join(cuts)
    if cut: cut = "[" + cut + "]"
    return "{0}{1}".format(self.getObjectName(), cut)



class CorrelationCut(Cut):

  def __init__(self, *initial_data, **kwargs):
    Cut.__init__(self)
    self.setAttributes(initial_data, kwargs)


  def getName(self, object_name, key):
    return "%s_" % key


  def getFunctionName(self):
    name = "dist"
    if self.mass['minimum'] != self.mass['maximum']:
      name = "mass"
    return name


  def setChargeCorrelation(self):
    function_name = "comb"
    cut = ({"object": function_name})
    cut.update({"type": "CHGCOR"})
    cut.update({"minimum": '+0.0000000000000000E+00'})
    cut.update({"maximum": '+0.0000000000000000E+00'})
    cut.update({"name": "CHGCOR" + "_" + "OS" if self.charge_correlation == -1 else "SS"})
    cut.update({"data": "os" if self.charge_correlation == -1 else "ss"})
    self.cuts.append(cut)


  def setCuts(self):
    if not self.called:
      if self.deltaEta['minimum'] != self.deltaEta['maximum']:
        self.setRange("dist", "DETA", self.deltaEta)

      if self.deltaPhi['minimum'] != self.deltaPhi['maximum']:
        self.setRange("dist", "DPHI", self.deltaPhi)

      if self.deltaR['minimum'] != self.deltaR['maximum']:
        self.setRange("dist", "DR", self.deltaR)

      if self.mass['minimum'] != self.mass['maximum']:
        self.setRange("mass", "MASS", self.mass)

      if self.charge_correlation:
        self.setChargeCorrelation()

    self.called = True



def Object2Xml(name, array):
  nn = len(array)

  expression = ""
  cuts = {}
  objects = {}
  parameters = []
  for cut in array:
    parameters.append(cut.getExpression())
    cuts.update(cut.getCuts())
    rc = cut.getObject()
    objects.update({rc['name']: rc})
  expression = cut.getExpression() if nn == 1 else "comb{{{0}}}".format(",".join(parameters))

  xml_cuts = ""
  xml_objects = ""
  for k, v in cuts.iteritems(): xml_cuts += "".join(v)
  for k, v in objects.iteritems(): xml_objects += OBJECT.format(**v)
  algorithm = {}
  algorithm.update({"name": name})
  algorithm.update({"expression": expression})
  algorithm.update({"body": xml_cuts+xml_objects})

  return ALGORITHM.format(**algorithm)



def Correlation2Xml(name, data):
  array = [ObjectCut(data['obj1']), ObjectCut(data['obj2'])]
  correlation = CorrelationCut(data['correlation'])

  cuts = {}
  objects = {}
  parameters = []
  for cut in array:
    parameters.append(cut.getExpression())
    cuts.update(cut.getCuts())
    rc = cut.getObject()
    objects.update({rc['name']: rc})

  xml_cuts = ""
  xml_objects = ""
  for k, v in cuts.iteritems(): xml_cuts += "".join(v)
  for k, v in objects.iteritems(): xml_objects += OBJECT.format(**v)
  expression = "{0}{{{1}}}".format(correlation.getFunctionName(), ",".join(parameters))

  rc = correlation.getCuts()
  expression += "[{0}]".format(",".join(rc.keys()))
  xml_cuts += "".join(rc.values())

  algorithm = {}
  algorithm.update({"name": name})
  algorithm.update({"expression": expression})
  algorithm.update({"body": xml_cuts+xml_objects})

  return ALGORITHM.format(**algorithm)



def Object2Condition(name, array):
  nn = len(array)

  expression = ""
  cuts = {}
  objects = {}
  if nn == 1:
    cut = array[0]
    expression = cut.getExpression()
    o = cut.getObject()
    objects.update({o['name']: OBJECT.format(**o)})
    cuts.update(cut.getCuts())
  else:
    parameters = []
    for cut in array:
      parameters.append(cut.getExpression())
      o = cut.getObject()
      objects.update({o['name']: OBJECT.format(**o)})
      cuts.update(cut.getCuts())
    expression = "comb{{{0}}}".format(",".join(parameters))

  return expression, cuts, objects


def Composite2Xml(name, data, cache_class, cache_instance):
  msb_32bit = 0x80000000

  rpn = []
  cuts = {}
  objects = {}
  for chunk in data:
    class_id = chunk['polymorphic_id']
    instance_id = chunk['ptr_wrapper']['id']
  
    if class_id & msb_32bit:
      cache_class.update({class_id: chunk['polymorphic_name']})
    else:
      class_id = class_id | msb_32bit
  
    if instance_id & msb_32bit:
      cache_instance.update({instance_id: chunk['ptr_wrapper']['data']})
    else:
      instance_id = instance_id | msb_32bit
  
    if cache_class[class_id] == 'MenuCondition::Object':
      conditions = []
      for x in cache_instance[instance_id]['value0']:
        conditions.append(ObjectCut(x))
      exp, cut, obj = Object2Condition(name, conditions)
      cuts.update(cut)
      objects.update(obj)
      rpn.append(exp)
  
    elif cache_class[class_id] == 'MenuCondition::Correlation':
      conditions = []
      data = cache_instance[instance_id]
      for key in ('obj1', 'obj2'):
        conditions.append(ObjectCut(data[key]))
      correlation = CorrelationCut(data['correlation'])

      parameters = []
      for cut in conditions:
        parameters.append(cut.getExpression())
        cuts.update(cut.getCuts())
        o = cut.getObject()
        objects.update({o['name']: OBJECT.format(**o)})

      expression = "{0}{{{1}}}".format(correlation.getFunctionName(), ",".join(parameters))
      cut = correlation.getCuts()
      cuts.update(cut)
      expression += "[{0}]".format(",".join(cut.keys()))
      rpn.append(expression)
  
    elif cache_class[class_id] == 'MenuCondition::Operator':
      rpn.append(OP2NAME[cache_instance[instance_id]['operator']])
  
  xml_cuts = "".join(cuts.values())
  xml_objects = "".join(objects.values())
  
  algorithm = {}
  algorithm.update({"name": name})
  algorithm.update({"expression": Rpn2Infix(rpn)})
  algorithm.update({"body": xml_cuts+xml_objects})

  return ALGORITHM.format(**algorithm)



def isComposite(data):
  rc = False
  for x in data:
    if "polymorphic_id" in x:
      rc = True
      break
  return rc


def Rpn2Infix(rpn):
  ii = 0
  stack = []
  while ii < len(rpn):
    token = rpn[ii]
    if token in ['AND', 'OR']:
      stack.append(' ({0} {1} {2}) '.format(stack.pop(), token, stack.pop()))
    elif token == 'NOT':
      stack.append(' ({0} {1}) '.format(token, stack.pop()))
    else:
      stack.append(token)
    ii += 1
  rc = stack.pop()
  rc = rc.strip()
  if rc[0] == '(': rc = rc[1:]
  if rc[-1] == ')': rc = rc[:-1]
  return rc.strip()


if __name__ == '__main__':
  path = 'parameters.json'
  output = None

  parser = argparse.ArgumentParser()

  parser.add_argument("--input", dest="path", default=path, type=str, action="store", required=True, help="path to a json L1 menu parameter file")
  parser.add_argument("--output", dest="output", default=output, type=str, action="store", help="output xml file name")

  options = parser.parse_args()

  fp = open(options.path)
  contents = json.load(fp)

  fp = open(options.output, 'wb') if options.output else sys.stdout

  cache_class = {}
  cache_instance = {}

  for name, data in contents.iteritems():
    # correlations
    if type(data) == types.DictType:
      fp.write(Correlation2Xml(name, data))

    # objects
    elif type(data) == types.ListType:
      if isComposite(data):
        fp.write(Composite2Xml(name, data, cache_class, cache_instance))
  
      else:
        array = []
        for x in data:
          array.append(ObjectCut(x))
        fp.write(Object2Xml(name, array))

# eof
