#!/bin/env python
#
# @author: Takashi MATSUSHITA
#

import argparse
import math
import os
import re
import string
from jinja2 import Environment, FileSystemLoader

import tmGrammar
import tmEventSetup


#
# constants
#
CUTS = {
  0: 'Threshold',
  1: 'Eta',
  2: 'Phi',
  3: 'Charge',
  4: 'Quality',
  5: 'Isolation',
  6: 'DeltaEta',
  7: 'DeltaPhi',
  8: 'DeltaR',
  9: 'Mass',
 10: 'ChargeCorrelation',
 11: 'Count',
 14: 'DeltaEta',
 15: 'DeltaPhi',
 16: 'DeltaR',
}

#
# filters
#
def toMass(value):
  return math.sqrt(2.*value)


def toDeltaR(value):
  return "%.2f" % math.sqrt(value)


def getAlgorithms(menu):
  algorithms = {}
  for name, algo in menu.getAlgorithmMapPtr().iteritems():
    algorithms[algo.getIndex()] = name
  return algorithms


def getHash2Name(condMap):
  translator = {}
  for x in condMap:
    key = x.split('_')[1]
    translator.update({key: x})

  return translator


def getCondition2Grammar(algorithm, translator):
  tmGrammar.Algorithm_Logic.clear()
  tmGrammar.Algorithm_parser(algorithm.getExpression())

  dictionary = {}
  for token in tmGrammar.Algorithm_Logic.getTokens():
    if token in tmGrammar.gateName: continue;
    key = "%s" % tmEventSetup.getHashUlong(token)
    dictionary[translator[key]] = token

  return dictionary


def getCutName(cut):
  return CUTS[cut]



THIS_DIR = os.path.dirname(os.path.abspath(__file__)) + "/templates"


def render(menu, template, name):
  j2_env = Environment(loader=FileSystemLoader(THIS_DIR), trim_blocks=True)

  j2_env.add_extension('jinja2.ext.loopcontrols')
  j2_env.filters['toMass'] = toMass
  j2_env.filters['toDeltaR'] = toDeltaR
  j2_env.filters['getAlgorithms'] = getAlgorithms
  j2_env.filters['getHash2Name'] = getHash2Name
  j2_env.filters['getCondition2Grammar'] = getCondition2Grammar
  j2_env.filters['getCutName'] = getCutName

  association = {
      "tmGrammar": tmGrammar,
      "tmEventSetup": tmEventSetup,
      "menu": menu
      }

  return j2_env.get_template(template).render(association)


if __name__ == '__main__':
  xml = 'L1Menu_Collisions2016_v5.xml'
  output = 'menu.html'

  parser = argparse.ArgumentParser()

  parser.add_argument("--menu", dest="xml", default=xml, type=str, action="store", required=True, help="path to the level1 trigger menu xml file")
  parser.add_argument("--output", dest="output", default=output, type=str, action="store", help="output c++ file name")

  options = parser.parse_args()

  menu = tmEventSetup.getTriggerMenu(options.xml)

  name = os.path.basename(output)
  name, ext = os.path.splitext(name)

  text = render(menu, 'reporter.html', name)
  with open(options.output, "wb") as fp:
    fp.write(text)

# eof
