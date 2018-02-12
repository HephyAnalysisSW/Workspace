#!/bin/env python
#
# @author: Takashi MATSUSHITA
#

import argparse

import tmEventSetup


def print_line(algorithm):
  comment = ''
  if 'comment' in algorithm: comment = algorithm['comment']
  print '{:60} {:>3} {}'.format(algorithm['name'], algorithm['index'], comment)


if __name__ == '__main__':
  xml = 'L1Menu_Collisions2016_v5.xml'
  output = 'menu.txt'

  parser = argparse.ArgumentParser()

  parser.add_argument("--menu", dest="xml", default=xml, type=str, action="store", required=True, help="path to the level1 trigger menu xml file")
  parser.add_argument("--output", dest="output", default=output, type=str, action="store", help="output menu text file name")

  options = parser.parse_args()

  menu = tmEventSetup.getTriggerMenu(options.xml)
  algorithms = menu.getAlgorithmMapPtr()

  header = '''#============================================================================#          
#-------------------------------     Menu     -------------------------------#          
#============================================================================#          
# L1Seed                                                     Bit  Prescale POG     PAG 
'''
  fp = open(options.output, "wb")
  fp.write(header)

  for name, algorithm in algorithms.iteritems():
    fp.write('{:60} {:>3}         1\n'.format(name, algorithm.getIndex()))

  fp.close()

# eof
