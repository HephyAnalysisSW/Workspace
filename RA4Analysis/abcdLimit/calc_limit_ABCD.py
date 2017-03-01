from cardFileWriter import cardFileWriter
#from limit_helper import plotsignif , plotLimit , signal_bins_3fb
from math import exp,sqrt
import os,sys
import ROOT
import pickle
#import array
#from Workspace.RA4Analysis.signalRegions import *
import argparse

def dphiLimitToLabel(dphi):
  ndphi = int(100*dphi+0.5)
  result = None
  if ndphi==50:
    result = "1"
  elif ndphi==75:
    result = "2"
  elif ndphi==100:
    result = "3"
  assert result!=None
  return "D"+result

def njetBinToLabel(njBin):
  # simplified to lower boundary
  result = None
  if njBin[1]!=-1:
    result = "".join([str(x) for x in range(njBin[0],njBin[1]+1)])
  else:
    result = str(njBin[0])+"p"
  assert result!=None
  return "J"+result[0]
#  return "J"+result

def ltBinToLabel(ltBin):
  idxs = [ None, None ]
  for i in range(2):
    if ltBin[i]==250:
      idxs[i] = 1
    elif ltBin[i]==350:
      idxs[i] = 2
    elif ltBin[i]==450:
      idxs[i] = 3
    elif ltBin[i]==650:
      idxs[i] = 4
    elif ltBin[i]==-1:
      idxs[i] = 5
    assert idxs[i]!=None
  return "L"+"".join([str(x) for x in range(idxs[0],idxs[1])])

def htBinToLabel(htBin):
  # simplified to lower limit
  idx = None
  if htBin == (500,750):
    idx = 1
  elif htBin == (500,1000):
    idx = 2
  elif htBin == (500,1250):
    idx = 3
  elif htBin == (750, 1000):
    idx = 4
  elif htBin == (750, 1250):
    idx = 5
  elif htBin == (500, -1):
    idx = 9
  elif htBin == (750,-1):
    idx = 6
  elif htBin == (1000,-1):
    idx = 7
  elif htBin == (1250,-1):
    idx = 8
  assert idx!=None
  return "H"+str(idx)
#  return "H"+"".join([str(x) for x in range(idxs[0],idxs[1])])

regionToDPhi_2015 = {
  (5, 5) : {
    (250, 350) : {
      (500, -1) : 1.00
     }, 
    (350, 450) : {
      (500, -1) : 1.00
      }, 
    (450, -1) : {
      (500, -1) : 1.00
      }
    }, 
  (6, 7) : {
    (250, 350) : {
      (500, 750) : 1.00, (750, -1) : 1.00
     }, 
    (350, 450) : {
      (500, 750) : 1.00, (750, -1) : 1.00
      }, 
    (450, -1) : {
      (500, 1000) : 0.75, (1000, -1) : 0.75
      }
    }, 
  (8, -1) : {
    (250, 350) : {
      (500, 750) : 1.00, (750, -1) : 1.00
     }, 
    (350, 450) : {
      (500, -1) : 0.75
      }, 
    (450, -1) : {
      (500, -1) : 0.75
      }
    }

}
signalRegions_Moriond2017 = {(5,5): {(250, 350): {(500, 750):   {'deltaPhi': 1.0, 'njet':'5j','LT':'LT1','HT': 'HT1',  'tex':'\\textrm{LT1}, \\textrm{HT1}'},
                                          (750, -1):          {'deltaPhi': 1.0, 'njet':'5j','LT':'LT1','HT': 'HT2', 'tex':'\\textrm{LT1}, \\textrm{HT23}'}},
                             (350, 450): {(500, 750):         {'deltaPhi': 1.0, 'njet':'5j','LT':'LT2','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'},
                                          (750, -1):          {'deltaPhi': 1.0, 'njet':'5j','LT':'LT2','HT': 'HT2', 'tex':'\\textrm{LT2}, \\textrm{HT23}'}},
                             (450, 650): {(500, 750):         {'deltaPhi': 0.75, 'njet':'5j','LT':'LT3','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'},
                                          (750, 1250):         {'deltaPhi': 0.75, 'njet':'5j','LT':'LT3','HT': 'HT23',  'tex':'\\textrm{LT2}, \\textrm{HT1}'},
                                          (1250, -1):          {'deltaPhi': 0.75, 'njet':'5j','LT':'LT3','HT': 'HT3', 'tex':'\\textrm{LT2}, \\textrm{HT23}'}},
                             (650, -1): {(500, 750):         {'deltaPhi': 0.5, 'njet':'5j','LT':'LT4','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'},
                                          (750, 1250):         {'deltaPhi': 0.5, 'njet':'5j','LT':'LT4','HT': 'HT23',  'tex':'\\textrm{LT2}, \\textrm{HT1}'},
                                          (1250, -1):          {'deltaPhi': 0.5, 'njet':'5j','LT':'LT4','HT': 'HT3', 'tex':'\\textrm{LT2}, \\textrm{HT23}'}}},
                     (6,7): {(250, 350): {(500, 1000):         {'deltaPhi': 1.0, 'njet':'6-7j','LT':'LT1','HT': 'HT1',  'tex':'\\textrm{LT1}, \\textrm{HT1}'},
                                          (1000, -1):          {'deltaPhi': 1.0, 'njet':'6-7j','LT':'LT1','HT': 'HT23', 'tex':'\\textrm{LT1}, \\textrm{HT23}'}},
                             (350, 450): {(500, 1000):         {'deltaPhi': 1.0, 'njet':'6-7j','LT':'LT2','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'},
                                          (1000, -1):          {'deltaPhi': 1.0, 'njet':'6-7j','LT':'LT2','HT': 'HT23', 'tex':'\\textrm{LT2}, \\textrm{HT23}'}},
                             (450, 650): {(500, 750):         {'deltaPhi': 0.75, 'njet':'5j','LT':'LT3','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'},
                                          (750, 1250):         {'deltaPhi': 0.75, 'njet':'5j','LT':'LT3','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'},
                                          (1250, -1):          {'deltaPhi': 0.75, 'njet':'5j','LT':'LT3','HT': 'HT23', 'tex':'\\textrm{LT2}, \\textrm{HT23}'}},
                             (650, -1): {(500, 750):         {'deltaPhi': 0.5, 'njet':'5j','LT':'LT4','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'},
                                          (750, 1250):         {'deltaPhi': 0.5, 'njet':'5j','LT':'LT4','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'},
                                          (1250, -1):          {'deltaPhi': 0.5, 'njet':'5j','LT':'LT4','HT': 'HT23', 'tex':'\\textrm{LT2}, \\textrm{HT23}'}}},
                     (8,-1): {(250, 350):{(500, 1000):         {'deltaPhi': 1.0, 'njet':'#geq8j','LT':'LT1','HT': 'HT1',  'tex':'\\textrm{LT1}, \\textrm{HT1}'},
                                          (1000, -1):          {'deltaPhi': 1.0, 'njet':'#geq8j','LT':'LT1','HT': 'HT23', 'tex':'\\textrm{LT1}, \\textrm{HT23}'}},
                              (350, 450):{(500, 1000):         {'deltaPhi': 1.0, 'njet':'#geq8j','LT':'LT2','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'},
                                          (1000, -1):          {'deltaPhi': 1.0, 'njet':'#geq8j','LT':'LT2','HT': 'HT23', 'tex':'\\textrm{LT2}, \\textrm{HT23}'}},
                             (450, 650): {(500, 1250):         {'deltaPhi': 0.75, 'njet':'5j','LT':'LT3','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'},
                                          (1250, -1):          {'deltaPhi': 0.75, 'njet':'5j','LT':'LT3','HT': 'HT23', 'tex':'\\textrm{LT2}, \\textrm{HT23}'}},
                             (650, -1): {(500, 1250):         {'deltaPhi': 0.5, 'njet':'5j','LT':'LT4','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'},
                                          (1250, -1):          {'deltaPhi': 0.5, 'njet':'5j','LT':'LT4','HT': 'HT23', 'tex':'\\textrm{LT2}, \\textrm{HT23}'}}}}
aggregateRegions_Moriond2017_Test2_onebyone = [\
                                                {(5,-1):   {(650, -1):   {(750, -1):     {'deltaPhi': 0.5,  'njet':'#geq5j'    ,'LT':'LT2i' ,'HT': 'HT1i', 'tex':'\\textrm{LT2i},  \\textrm{HT1i}'  }}}},
                                                {(6,-1):   {(650, -1):   {(1000, -1):    {'deltaPhi': 0.5,  'njet':'#geq6j'  ,'LT':'LT2i' ,'HT': 'HT2i', 'tex':'\\textrm{LT2i},  \\textrm{HT2i}'  }}}},                                  
                                                {(6,-1):   {(450, -1):   {(500, -1):     {'deltaPhi': 0.75, 'njet':'#geq6j'  ,'LT':'LT1i' ,'HT': 'HT0i', 'tex':'\\textrm{LT1i},  \\textrm{HT0i}'  }}}},                         
                                                {(7,-1):   {(450, -1):   {(500, -1):     {'deltaPhi': 0.75, 'njet':'#geq7j'  ,'LT':'LT1i' ,'HT': 'HT0i', 'tex':'\\textrm{LT1i},  \\textrm{HT0i}'  }}}},                         
                                                {(7,-1):   {(650, -1):   {(500, -1):     {'deltaPhi': 0.5,  'njet':'#geq7j'  ,'LT':'LT2i' ,'HT': 'HT0i', 'tex':'\\textrm{LT2i},  \\textrm{HT0i}'  }}}},                         
                                                {(8,-1):  {(250, -1):   {(1250, -1):    {'deltaPhi': 1.0,  'njet':'#geq8j','LT':'LT0i' ,'HT': 'HT3i', 'tex':'\\textrm{LT0i},  \\textrm{HT3i}'}}}},
                                                {(8,-1):  {(450, -1):   {(1250, -1):    {'deltaPhi': 1.0,  'njet':'#geq8j','LT':'LT1i' ,'HT': 'HT3i', 'tex':'\\textrm{LT1i},  \\textrm{HT3i}'}}}},
                                            ]
signalRegions_Moriond2017_onebyone = [\
    {(5,5): {(250, 350): {(500, 750):  {'deltaPhi': 1.0, 'njet':'5j','LT':'LT1','HT': 'HT1',  'tex':'\\textrm{LT1}, \\textrm{HT1}'}}}},
    {(5,5): {(250, 350): {(750, -1):         {'deltaPhi': 1.0, 'njet':'5j','LT':'LT1','HT': 'HT2', 'tex':'\\textrm{LT1}, \\textrm{HT23}'}}}},
    {(5,5): {(350, 450): {(500, 750):        {'deltaPhi': 1.0, 'njet':'5j','LT':'LT2','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'}}}},
    {(5,5): {(350, 450): {(750, -1):    {'deltaPhi': 1.0, 'njet':'5j','LT':'LT2','HT': 'HT2', 'tex':'\\textrm{LT2}, \\textrm{HT23}'}}}},
    {(5,5): {(450, 650): {(500, 750):   {'deltaPhi': 0.75, 'njet':'5j','LT':'LT3','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'}}}},
    {(5,5): {(450, 650): {(750, 1250):   {'deltaPhi': 0.75, 'njet':'5j','LT':'LT3','HT': 'HT23',  'tex':'\\textrm{LT2}, \\textrm{HT1}'}}}},
    {(5,5): {(450, 650): {(1250, -1):    {'deltaPhi': 0.75, 'njet':'5j','LT':'LT3','HT': 'HT3', 'tex':'\\textrm{LT2}, \\textrm{HT23}'}}}},
    {(5,5): {(650, -1): {(500, 750):   {'deltaPhi': 0.5, 'njet':'5j','LT':'LT4','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'}}}},
    {(5,5): {(650, -1): {(750, 1250):   {'deltaPhi': 0.5, 'njet':'5j','LT':'LT4','HT': 'HT23',  'tex':'\\textrm{LT2}, \\textrm{HT1}'}}}},
    {(5,5): {(650, -1): {(1250, -1):    {'deltaPhi': 0.5, 'njet':'5j','LT':'LT4','HT': 'HT3', 'tex':'\\textrm{LT2}, \\textrm{HT23}'}}}},
    {(6,7): {(250, 350): {(500, 1000):  {'deltaPhi': 1.0, 'njet':'6-7j','LT':'LT1','HT': 'HT1',  'tex':'\\textrm{LT1}, \\textrm{HT1}'}}}},
    {(6,7): {(250, 350): {(1000, -1):   {'deltaPhi': 1.0, 'njet':'6-7j','LT':'LT1','HT': 'HT23', 'tex':'\\textrm{LT1}, \\textrm{HT23}'}}}},
    {(6,7): {(350, 450): {(500, 1000):  {'deltaPhi': 1.0, 'njet':'6-7j','LT':'LT2','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'}}}},
    {(6,7): {(350, 450): { (1000, -1):   {'deltaPhi': 1.0, 'njet':'6-7j','LT':'LT2','HT': 'HT23', 'tex':'\\textrm{LT2}, \\textrm{HT23}'}}}},
    {(6,7): {(450, 650): {(500, 750):  {'deltaPhi': 0.75, 'njet':'5j','LT':'LT3','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'}}}},
    {(6,7): {(450, 650): {(750, 1250):  {'deltaPhi': 0.75, 'njet':'5j','LT':'LT3','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'}}}},
    {(6,7): {(450, 650): {(1250, -1):   {'deltaPhi': 0.75, 'njet':'5j','LT':'LT3','HT': 'HT23', 'tex':'\\textrm{LT2}, \\textrm{HT23}'}}}},
    {(6,7): {(650, -1): {(500, 750):  {'deltaPhi': 0.5, 'njet':'5j','LT':'LT4','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'}}}},
    {(6,7): { (650, -1): {(750, 1250):{'deltaPhi': 0.5, 'njet':'5j','LT':'LT4','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'}}}},                                          {(6,7): { (650, -1): {(1250, -1):          {'deltaPhi': 0.5, 'njet':'5j','LT':'LT4','HT': 'HT23', 'tex':'\\textrm{LT2}, \\textrm{HT23}'}}}},
    {(8,-1): {(250, 350):{(500, 1000):{'deltaPhi': 1.0, 'njet':'#geq8j','LT':'LT1','HT': 'HT1',  'tex':'\\textrm{LT1}, \\textrm{HT1}'}}}},
    {(8,-1): {(250, 350):{ (1000, -1): {'deltaPhi': 1.0, 'njet':'#geq8j','LT':'LT1','HT': 'HT23', 'tex':'\\textrm{LT1}, \\textrm{HT23}'}}}},
    {(8,-1): {(350, 450):{(500, 1000):{'deltaPhi': 1.0, 'njet':'#geq8j','LT':'LT2','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'}}}},
    {(8,-1): {(350, 450):{ (1000, -1): {'deltaPhi': 1.0, 'njet':'#geq8j','LT':'LT2','HT': 'HT23', 'tex':'\\textrm{LT2}, \\textrm{HT23}'}}}},
    {(8,-1): {(450, 650): {(500, 1250): {'deltaPhi': 0.75, 'njet':'5j','LT':'LT3','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'}}}},
    {(8,-1): {(450, 650): {(1250, -1):  {'deltaPhi': 0.75, 'njet':'5j','LT':'LT3','HT': 'HT23', 'tex':'\\textrm{LT2}, \\textrm{HT23}'}}}},
    {(8,-1): {(650, -1): {(500, 1250): {'deltaPhi': 0.5, 'njet':'5j','LT':'LT4','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'}}}},
    {(8,-1): {(650, -1): {(1250, -1):  {'deltaPhi': 0.5, 'njet':'5j','LT':'LT4','HT': 'HT23', 'tex':'\\textrm{LT2}, \\textrm{HT23}'}}}}]

signalRegions2016_HT500_onebyone = [
                      {(5,5): {(250, 350): {(500, -1):   {'deltaPhi': 1.0, 'njet':'5j','LT':'LT1','HT': 'HT1',  'tex':'\\textrm{LT1}, \\textrm{HT1}'}}}},
                      {(5,5): {(350, 450): {(500, -1):   {'deltaPhi': 1.0, 'njet':'5j','LT':'LT2','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'}}}},
                      {(5,5): {(350, 650): {(500, -1):   {'deltaPhi': 1.0, 'njet':'5j','LT':'LT2','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'}}}},
                      {(5,5): {(350, 650): {(500, -1):   {'deltaPhi': 0.75, 'njet':'5j','LT':'LT2','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'}}}},
                      {(5,5): {(450, -1):  {(500, -1):   {'deltaPhi': 0.75, 'njet':'5j','LT':'LT3','HT': 'HT1', 'tex':'\\textrm{LT3}, \\textrm{HT1}'}}}},
                      {(5,5): {(650, -1):  {(500, -1):   {'deltaPhi': 0.75, 'njet':'5j','LT':'LT3','HT': 'HT1', 'tex':'\\textrm{LT3}, \\textrm{HT1}'}}}},
                      {(6,7): {(250, 350): {(500, -1):   {'deltaPhi': 1.0, 'njet':'6-7j','LT':'LT1','HT': 'HT1',  'tex':'\\textrm{LT1}, \\textrm{HT1}'}}}},
                      {(6,7): {(250, 350): {(500, -1):   {'deltaPhi': 1.0, 'njet':'6-7j','LT':'LT1','HT': 'HT23', 'tex':'\\textrm{LT1}, \\textrm{HT23}'}}}},
                      {(6,7): {(350, 450): {(500, -1):   {'deltaPhi': 1.0, 'njet':'6-7j','LT':'LT2','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'}}}},
                      {(6,7): {(350, 650): {(500, -1):   {'deltaPhi': 1.0, 'njet':'6-7j','LT':'LT2','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'}}}},
                      {(6,7): {(350, 650): {(500, -1):   {'deltaPhi': 0.75, 'njet':'6-7j','LT':'LT2','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'}}}},
                      {(6,7): {(450, -1):  {(500, -1):   {'deltaPhi': 0.75, 'njet':'6-7j','LT':'LT3','HT': 'HT1', 'tex':'\\textrm{LT3}, \\textrm{HT1}'}}}},
                      {(6,7): {(650, -1):  {(500, -1):   {'deltaPhi': 0.75, 'njet':'6-7j','LT':'LT3','HT': 'HT1', 'tex':'\\textrm{LT3}, \\textrm{HT1}'}}}},
                      {(8,-1):{(250, 350): {(500, -1):   {'deltaPhi': 1.0, 'njet':'#geq8j','LT':'LT1','HT': 'HT1',  'tex':'\\textrm{LT1}, \\textrm{HT1}'}}}},
                      {(8,-1):{(350, 450): {(500, -1):   {'deltaPhi': 1.0, 'njet':'#geq8j','LT':'LT2','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'}}}},
                      {(8,-1):{(350, 650): {(500, -1):   {'deltaPhi': 1.0, 'njet':'#geq8j','LT':'LT2','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'}}}},
                      {(8,-1):{(350, 650): {(500, -1):   {'deltaPhi': 0.75, 'njet':'#geq8j','LT':'LT2','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'}}}},
                      {(8,-1):{(450, -1):  {(500, -1):   {'deltaPhi': 0.75, 'njet':'#geq8j','LT':'LT3','HT': 'HT1', 'tex':'\\textrm{LT3}, \\textrm{HT1}'}}}},
                      {(8,-1):{(650, -1):  {(500, -1):   {'deltaPhi': 0.75, 'njet':'#geq8j','LT':'LT3','HT': 'HT23', 'tex':'\\textrm{LT3}, \\textrm{HT23}'}}}},
                        ]

signalRegions_Moriond2017_merge1 = [\
#{
#(6,7): {(650, -1): {(500, -1):  {'deltaPhi': 0.5, 'njet':'5j','LT':'LT1','HT': 'HT1',  'tex':'\\textrm{LT1}, \\textrm{HT1}'}}},
#(8,-1): {(650, -1): {(500, -1):  {'deltaPhi': 0.5, 'njet':'5j','LT':'LT1','HT': 'HT1',  'tex':'\\textrm{LT1}, \\textrm{HT1}'}}}
#},
{
(6,7): {\
      (450, 650): {\
      (500, 750):  {'deltaPhi': 0.75, 'njet':'5j','LT':'LT1','HT': 'HT1',  'tex':'\\textrm{LT1}, \\textrm{HT1}'},
      (750, 1250):  {'deltaPhi': 0.75, 'njet':'5j','LT':'LT1','HT': 'HT1',  'tex':'\\textrm{LT1}, \\textrm{HT1}'},
      (1250, -1):  {'deltaPhi': 0.75, 'njet':'5j','LT':'LT1','HT': 'HT1',  'tex':'\\textrm{LT1}, \\textrm{HT1}'}},
      (650, -1): {\
      (500, 750):  {'deltaPhi': 0.5, 'njet':'5j','LT':'LT1','HT': 'HT1',  'tex':'\\textrm{LT1}, \\textrm{HT1}'},
      (750, 1250):  {'deltaPhi': 0.5, 'njet':'5j','LT':'LT1','HT': 'HT1',  'tex':'\\textrm{LT1}, \\textrm{HT1}'},
      (1250, -1):  {'deltaPhi': 0.5, 'njet':'5j','LT':'LT1','HT': 'HT1',  'tex':'\\textrm{LT1}, \\textrm{HT1}'}},
      },
(8,-1): {(650, -1): {\
      (500, 1250):  {'deltaPhi': 0.5, 'njet':'5j','LT':'LT1','HT': 'HT1',  'tex':'\\textrm{LT1}, \\textrm{HT1}'},
      (1250, -1):  {'deltaPhi': 0.5, 'njet':'5j','LT':'LT1','HT': 'HT1',  'tex':'\\textrm{LT1}, \\textrm{HT1}'}}}
},
#{(6,7): {(650, -1): {(500, -1):  {'deltaPhi': 0.5, 'njet':'5j','LT':'LT1','HT': 'HT1',  'tex':'\\textrm{LT1}, \\textrm{HT1}'}}}},
#{(8,-1): {(650, -1): {(500, -1):  {'deltaPhi': 0.5, 'njet':'5j','LT':'LT1','HT': 'HT1',  'tex':'\\textrm{LT1}, \\textrm{HT1}'}}}},
]

regionToDPhi_ICHEP = {(5,5): {(250, 350): {(500, 750):   {'deltaPhi': 1.0, 'njet':'5j','LT':'LT1','HT': 'HT1',  'tex':'\\textrm{LT1}, \\textrm{HT1}'},
                                          (750, -1):    {'deltaPhi': 1.0, 'njet':'5j','LT':'LT1','HT': 'HT23', 'tex':'\\textrm{LT1}, \\textrm{HT23}'}},
                             (350, 450): {(500, 750):   {'deltaPhi': 1.0, 'njet':'5j','LT':'LT2','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'},
                                          (750, -1):    {'deltaPhi': 1.0, 'njet':'5j','LT':'LT2','HT': 'HT23', 'tex':'\\textrm{LT2}, \\textrm{HT23}'}},
                             (450, -1):  {(500, 750):   {'deltaPhi': 0.75, 'njet':'5j','LT':'LT3','HT': 'HT1', 'tex':'\\textrm{LT3}, \\textrm{HT1}'},                  
                                          (750, 1000):  {'deltaPhi': 0.75, 'njet':'5j','LT':'LT3','HT': 'HT2', 'tex':'\\textrm{LT3}, \\textrm{HT2}'},                  
                                          (1000, -1):   {'deltaPhi': 0.75, 'njet':'5j','LT':'LT3','HT': 'HT3', 'tex':'\\textrm{LT3}, \\textrm{HT3}'}}},                            
                     (6,7): {(250, 350): {(500, 750):   {'deltaPhi': 1.0, 'njet':'6-7j','LT':'LT1','HT': 'HT1',  'tex':'\\textrm{LT1}, \\textrm{HT1}'},                              
                                          (750, -1):    {'deltaPhi': 1.0, 'njet':'6-7j','LT':'LT1','HT': 'HT23', 'tex':'\\textrm{LT1}, \\textrm{HT23}'}},               
                             (350, 450): {(500, 750):   {'deltaPhi': 1.0, 'njet':'6-7j','LT':'LT2','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'},
                                          (750, -1):    {'deltaPhi': 1.0, 'njet':'6-7j','LT':'LT2','HT': 'HT23', 'tex':'\\textrm{LT2}, \\textrm{HT23}'}},                            
                             (450, -1):  {(500, 750):   {'deltaPhi': 0.75, 'njet':'6-7j','LT':'LT3','HT': 'HT1', 'tex':'\\textrm{LT3}, \\textrm{HT1}'},                              
                                          (750, 1000):  {'deltaPhi': 0.75, 'njet':'6-7j','LT':'LT3','HT': 'HT2', 'tex':'\\textrm{LT3}, \\textrm{HT2}'},                              
                                          (1000, -1):   {'deltaPhi': 0.75, 'njet':'6-7j','LT':'LT3','HT': 'HT3', 'tex':'\\textrm{LT3}, \\textrm{HT3}'}}},       
                     (8,-1): {(250, 350):{(500, 750):   {'deltaPhi': 1.0, 'njet':'#geq8j','LT':'LT1','HT': 'HT1',  'tex':'\\textrm{LT1}, \\textrm{HT1}'},               
                                          (750, -1):    {'deltaPhi': 1.0, 'njet':'#geq8j','LT':'LT1','HT': 'HT23', 'tex':'\\textrm{LT1}, \\textrm{HT23}'}},             
                              (350, 450):{(500, 750):   {'deltaPhi': 1.0, 'njet':'#geq8j','LT':'LT2','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'},
                                          (750, -1):    {'deltaPhi': 1.0, 'njet':'#geq8j','LT':'LT2','HT': 'HT23', 'tex':'\\textrm{LT2}, \\textrm{HT23}'}},
                              (450, -1): {(500, 1000):  {'deltaPhi': 0.75, 'njet':'#geq8j','LT':'LT3','HT': 'HT1', 'tex':'\\textrm{LT3}, \\textrm{HT1}'},
                                          (1000, -1):   {'deltaPhi': 0.75, 'njet':'#geq8j','LT':'LT3','HT': 'HT23', 'tex':'\\textrm{LT3}, \\textrm{HT23}'}}}}
aggregateRegions_Moriond2017 =  {(5,5): {(650, -1): {(750, -1):    {'deltaPhi': 0.5,  'njet':'5j'    ,'LT':'LT3i' ,'HT': 'HT1i', 'tex':'\\textrm{LT3i},  \\textrm{HT1i}'  }}},
                                 (6,7): {(450, 650): {(500, 1250):   {'deltaPhi': 0.75,  'njet':'6-7j'    ,'LT':'LT2'  ,'HT': 'HT02',  'tex':'\\textrm{LT2},   \\textrm{HT02}'},                                                  
                                                      (1250, -1):    {'deltaPhi': 0.75, 'njet':'6-7j'    ,'LT':'LT2'  ,'HT': 'HT3i', 'tex':'\\textrm{LT2},   \\textrm{HT3i}'  }},                              
                                         (650, -1): {(1250, -1):    {'deltaPhi': 0.5,  'njet':'6-7j'    ,'LT':'LT3i' ,'HT': 'HT3i', 'tex':'\\textrm{LT3i},  \\textrm{HT3i}'  }}},                                       
                                 (8,-1): {(250, 450):{(500, 1000):   {'deltaPhi': 1.0,  'njet':'#geq8j','LT':'LT01'  ,'HT': 'HT01', 'tex':'\\textrm{LT01},   \\textrm{HT01}'  },
                                                      (1000, -1):    {'deltaPhi': 1.0,  'njet':'#geq8j','LT':'LT01'  ,'HT': 'HT2i', 'tex':'\\textrm{LT01},   \\textrm{HT2i}'  }},                                       
                                          (450, -1): {(500, 1250):   {'deltaPhi': 0.75, 'njet':'#geq8j'    ,'LT':'LT2i'  ,'HT': 'HT02', 'tex':'\\textrm{LT2i},   \\textrm{HT02}'  },                                    
                                                      (1250, -1):    {'deltaPhi': 0.75, 'njet':'#geq8j'    ,'LT':'LT2i'  ,'HT': 'HT3i', 'tex':'\\textrm{LT2i},   \\textrm{HT3i}'  }}}}

parser = argparse.ArgumentParser()
parser.add_argument("--index_sr", dest="index_sr", default=0, action="store", help="index_sr")
parser.add_argument("--mglu", dest="mglu", default=1000, action="store", help="mglu")
parser.add_argument("--singlemglu", dest="singlemglu", default=True, action="store", help="true If you want one mgliuno point")
parser.add_argument('--nolimit', help='do not run limit', action='store_true')
parser.add_argument('--blind', help='use blind mode', action='store_true')
parser.add_argument('-f', '--force', dest='force', help='replace output files', action='store_true')
parser.add_argument('-d', '--dir', dest='dir', help='output directory', default=None)
#parser.add_argument('--SRonly', help='use only SRs', action='store_true')
parser.add_argument('--method', help='limit setting method', dest='method', \
                      choices=['CalcSingleLimit','CalcLimitSRonly','CalcAbcdLimit'],default=['CalcSingleLimit'])
parser.add_argument('--bins', help='list of bin indices to be used', 
                    dest='bins', default=None)
parser.add_argument('--signals', help='list of signal indices to be used', 
                    dest='signals', default=None)
parser.add_argument('--masses', help='gluino,lsp masses of a signal point', 
                    dest='masses', default=None)
args = parser.parse_args()

index_sr = int(args.index_sr)
#singlemglu = args.singlemglu
mglu_input = int(args.mglu)
print mglu_input
#regionToDPhi = signalRegions_Moriond2017_onebyone[index_sr]
#regionToDPhi = signalRegions_Moriond2017_merge1[index_sr]
#regionToDPhi = signalRegions2016_HT500_onebyone[index_sr]



useBinIndices = set()
if args.bins!=None:
  for f in args.bins.split(","):
    if f.find("-")>=0:
      gs = f.split("-")
      assert len(gs)==2
      for i in range(int(gs[0]),int(gs[1])+1):
        useBinIndices.add(i)
    else:
        useBinIndices.add(int(f))
assert not ( args.signals!=None and args.masses!=None )
useSignalIndices = set()
if args.signals!=None:
  for f in args.signals.split(","):
    if f.find("-")>=0:
      gs = f.split("-")
      assert len(gs)==2
      for i in range(int(gs[0]),int(gs[1])+1):
        useSignalIndices.add(i)
    else:
        useSignalIndices.add(int(f))
useSignalMasses = None
if args.masses!=None:
  ms = [ int(x) for x in args.masses.split(",") ]
  assert len(ms)==2
  useSignalMasses = ( ms[0], ms[1] )
  mglu_input = ms[0]

aggr_8bins = False 
ICHEP_36fb = False
aggr_test = False
Moriond2017_main = True
ICHEP2016 = False
ICHEP_40 = False

if Moriond2017_main :
  #regionToDPhi = signalRegions_Moriond2017
  regionToDPhi = signalRegions_Moriond2017_onebyone[index_sr]
  #full_sigres = pickle.load(file(os.path.expandvars("/afs/hephy.at/user/e/easilar/www/Moriond2017/pickles/signals/mglu"+str(mglu_input)+"Signal_pkl")))      ##Moriond2017 bins
  full_sigres = pickle.load(file(os.path.expandvars("/afs/hephy.at/user/e/easilar/www/Moriond2017/pickles/signals/mglu"+str(mglu_input)+"Signal_isoVetoCorrected_pkl")))      ##Moriond2017 bins
  #bkg_pickle_dir = '/afs/hephy.at/data/easilar01/Results2017/Prediction_Spring16_templates_SR_Moriond2017_newTT_lep_data_36p5/resultsFinal_withSystematics_Filesremoved_pkl'
  bkg_pickle_dir =  '/afs/hephy.at/data/easilar01/Results2017/Prediction_Spring16_templates_SR_Moriond2017_Summer16_lep_data_36p5/resultsFinal_withSystematics_Filesremoved_pkl'

if ICHEP_36fb :
  regionToDPhi =  regionToDPhi_ICHEP
  full_sigres = pickle.load(file(os.path.expandvars("/afs/hephy.at/user/e/easilar/www/Moriond2017/pickles/signals/mglu"+str(mglu_input)+"Signal_ICHEP2016_pkl")))    ##ICHEP2016 bins
  bkg_pickle_dir = '/afs/hephy.at/data/easilar01/Results2017/Prediction_Spring16_templates_SR_ICHEP2016_newTT_lep_MC_SF_36p5/resultsFinal_withSystematics_Filesremoved_pkl'  #ICHEP 2016 36.5 fb

if ICHEP2016:
  regionToDPhi =  regionToDPhi_ICHEP
  bkg_pickle_dir = "/afs/hephy.at/data/easilar01/Ra40b/pickleDir/resultsFinal_withSystematics_pkl"
  full_sigres = pickle.load(file(os.path.expandvars("/afs/hephy.at/data/easilar01/Ra40b/pickleDir/allSignals_12p88_ultimate_2016Syst_pkl")))

if ICHEP_40:
  regionToDPhi =  regionToDPhi_ICHEP
  full_sigres = pickle.load(file(os.path.expandvars("/afs/hephy.at/user/e/easilar/www/POST_ICHEP_studies/pickles/DeltaPhiCut_Optm/withSystMAx/mglu"+str(mglu_input)+"Signals_40fb_ICHEP_newprime_pkl")))
  bkg_pickle_dir = '/afs/hephy.at/data/easilar01/Results2016/Prediction_Spring16_templates_SR_ICHEP2016_v1_lep_MC_SF_40/resultsFinal_withSystematics_pkl'

if aggr_test :
  regionToDPhi = aggregateRegions_Moriond2017_Test2_onebyone[index_sr]
  full_sigres = pickle.load(file(os.path.expandvars("/afs/hephy.at/user/e/easilar/www/Moriond2017/pickles/signals/mglu"+str(mglu_input)+"Signal_aggr_inc_pkl")))    ##aggr test bins
  bkg_pickle_dir = '/afs/hephy.at/data/easilar01/Results2017/Prediction_Spring16_templates_aggr_Moriond2017_v3_lep_MC_SF_36p5/resultsFinal_withSystematics_Filesremoved_pkl'  #Aggr Test 36.5 fb

if aggr_8bins :
  regionToDPhi = aggregateRegions_Moriond2017
  full_sigres = pickle.load(file('/afs/hephy.at/user/e/easilar/www/Moriond2017/pickles/signals/mglu'+str(mglu_input)+'Signal_aggr_pkl')) ##8 aggr bins
  bkg_pickle_dir = '/afs/hephy.at/data/easilar01/Results2017/Prediction_Spring16_templates_aggr_Moriond2017_v1_lep_data_36p5//resultsFinal_withSystematics_Filesremoved_pkl' 

#if args.SRonly:
#  from CalcLimitSRonly import *
#else:
#  from CalcSingleLimit import *
if args.method=='CalcSingleLimit':
  from CalcSingleLimit import *
elif args.method=='CalcLimitSRonly':
  from CalcLimitSRonly import *
elif args.method=='CalcAbcdLimit':
  from CalcAbcdLimit import *
  
#ROOT.gROOT.LoadMacro("$CMSSW_BASE/src/Workspace/HEPHYPythonTools/scripts/root/tdrstyle.C")
#ROOT.setTDRStyle()

path = os.environ["HOME"]+"/www/combine_tests/"
if not os.path.exists(path):
  os.makedirs(path)

path_table = os.environ["HOME"]+"/www/combine_tests/"
if not os.path.exists(path_table):
  os.makedirs(path_table)

text_path = "text_files"
if not os.path.exists(text_path):
  os.makedirs(text_path)



##################################

#res = pickle.load(file(os.path.expandvars("singleLeptonic_Spring15__estimationResults_pkl_kappa_corrected-150116.pkl")))
#sigres = pickle.load(file(os.path.expandvars("resultsFinal_withSystematics_andSignals_NewStructure_150120.pkl")))
#sigres = pickle.load(file(os.path.expandvars("pickles150121/allSignals_2p3_pkl")))
#bkgres = pickle.load(file(os.path.expandvars("pickles150121/resultsFinal_withSystematics_pkl")))
#sigres = pickle.load(file(os.path.expandvars("pickles150125/allSignals_2p3_v2_pkl")))
#sigres = pickle.load(file(os.path.expandvars("pickles160130/allSignals_2p25_syst_pkl")))
#bkgres = pickle.load(file(os.path.expandvars("pickles150125/resultsFinal_withSystematics_pkl")))
#sigres = pickle.load(file(os.path.expandvars("pickles160218/allSignals_2p25_allSyst_approval_pkl")))
#bkgres = pickle.load(file(os.path.expandvars("pickles160218/resultsFinal_withSystematics_pkl")))
#sigres = pickle.load(file(os.path.expandvars("pickles160223/allSignals_2p25_allSyst_approval_pkl")))
#bkgres = pickle.load(file(os.path.expandvars("pickles160223/resultsFinal_withSystematics_pkl")))
#sigres = pickle.load(file(os.path.expandvars("pickles160303/allSignals_2p3_allSyst_pkl")))
#sigres = pickle.load(file(os.path.expandvars("/data/easilar/Spring15/25ns/allSignals_2p3_allSyst_VV_pkl")))
#sigres = pickle.load(file(os.path.expandvars("/afs/hephy.at/data/easilar01/Ra40b/pickleDir/allSignals_12p88_ultimate_2016Syst_pkl")))
#full_sigres = pickle.load(file(os.path.expandvars("/afs/hephy.at/user/e/easilar/www/POST_ICHEP_studies/pickles/DeltaPhiCut_Optm/withSystMAx/mglu"+str(mglu_input)+"Signals_40fb_test5_newprime_pkl")))      ##Moriond2017 bins
#full_sigres = pickle.load(file(os.path.expandvars("/afs/hephy.at/user/e/easilar/www/POST_ICHEP_studies/pickles/DeltaPhiCut_Optm/withSystMAx/mglu1500Signals_40fb_ICHEP_HT500_withSystematics_mergedbins_pkl")))      ##HT500 bins
##sigres = pickle.load(file(os.path.expandvars("/afs/hephy.at/user/e/easilar/www/POST_ICHEP_studies/pickles/DeltaPhiCut_Optm/withSystMAx/mglu"+str(mglu_input)+"Signals_40fb_ICHEP_newprime_pkl")))    ##ICHEP BINS 40 fb
#bkgres = pickle.load(file(os.path.expandvars("pickles160303/resultsFinal_withSystematics_pkl")))
#bkg_pickle_dir = '/afs/hephy.at/data/easilar01/Results2016/Prediction_Spring16_templates_SR_Moriond2017_v1_lep_MC_SF_40/resultsFinal_withSystematics_pkl'
#bkg_pickle_dir = '/afs/hephy.at/data/easilar01/Results2016/Prediction_Spring16_templates_SR_ICHEP2016_v1_lep_MC_SF_40/resultsFinal_withSystematics_HT500_pkl'
#bkg_pickle_dir = '/afs/hephy.at/data/easilar01/Results2017/Prediction_Spring16_templates_SR_Moriond2017_v8_lep_MC_SF_36p5/singleLeptonic_Spring16_iso_Veto_ISRforttJets_OLDttJetsSB_addDiBoson_MC_withSystematics_pkl'
#bkg_pickle_dir = '/afs/hephy.at/data/easilar01/Results2016/Prediction_Spring16_templates_SR_ICHEP2016_v1_lep_MC_SF_40/resultsFinal_withSystematics_pkl'
full_bkgres = pickle.load(file(os.path.expandvars(bkg_pickle_dir)))
testSR = {}
test_sig = {}
for njet in regionToDPhi:
  testSR[njet] = {}
  test_sig[njet] = {}
  for stb in regionToDPhi[njet]:
    testSR[njet][stb] = {} 
    test_sig[njet][stb] = {} 
    for htb in regionToDPhi[njet][stb]:
      testSR[njet][stb][htb] = full_bkgres[njet][stb][htb]
      test_sig[njet][stb][htb] = full_sigres[njet][stb][htb]

bkgres = testSR
sigres = test_sig

#pdg = 'pos'
#pdg = 'neg'
#pdg = 'both'

#
# consistency
#
njetBins = [ ]
ltBins = [ ]
htBins = [ ]
for nj in bkgres.keys():
  if type(nj)!=type(()):
    print "Rejecting key",nj
    continue
  njetBins.append(nj)
  for lt in bkgres[nj]:
    if not lt in ltBins:
      ltBins.append(lt)
    for ht in bkgres[nj][lt]:
      if not ht in htBins:
        htBins.append(ht)
njetBins.sort()
ltBins.sort()
htBins.sort()

#print njetBins
#print ltBins
#print htBins
#for njet in njetBins:
#  print njetBinToLabel(njet)
#for lt in ltBins:
#  print ltBinToLabel(lt)
#for ht in htBins:
#  print htBinToLabel(ht)

#signals = [
#          {'color': ROOT.kBlue ,'name': 's1500' , 'mglu' : 1500, 'mlsp' : 100, 'label': 'T5q^{4} 1.5/0.8/0.1'}, \
#          {'color': ROOT.kRed  ,'name': 's1200' , 'mglu' : 1200, 'mlsp' : 800, 'label': 'T5q^{4} 1.2/1.0/0.8'}, \
##          {'color': ROOT.kBlack ,'name': 's1000' , 'mglu' : 1000, 'mlsp' : 700, 'label': 'T5q^{4} 1.0/0.85/0.7'}, \
#          {'color': ROOT.kBlack ,'name': 's1000' , 'mglu' : 1000, 'mlsp' : 100, 'label': 'T5q^{4} 1.0/0.55/0.1'}, \
#         ]

#signal = signals[2]


#
# prepare bins
#

#nbins = 0
#for njet in njetBins[:]:
#  for lt in ltBins[:]:
#    if not lt in bkgres[njet]:
#      continue
#    for ht in htBins[:]:
#      if not ht in bkgres[njet][lt]:
#        continue
#      nbins += 1

if os.path.exists("results.log"):
  os.system("rm results.log; touch results.log")

sbBinNames = [ ]
sbBins = { }
mbBinNames = [ ]
mbBins = { }
for njet in njetBins[:]:
  for lt in ltBins[:]:
    if not lt in bkgres[njet]:
      continue
    for ht in htBins[:]:
      if not ht in bkgres[njet][lt]:
        continue
      dphiLimit = dphiLimitToLabel(regionToDPhi[njet][lt][ht]['deltaPhi'])
      print njetBinToLabel(njet) , ltBinToLabel(lt) , htBinToLabel(ht) , dphiLimit
      print njet , lt , ht , regionToDPhi[njet][lt][ht]['deltaPhi']
      bNameBase = njetBinToLabel(njet) + ltBinToLabel(lt) + htBinToLabel(ht) + dphiLimit
      bName = bNameBase
      #print "bname:" , bName
      #print "bNameBase" , bNameBase
      assert not bName in mbBinNames
      mbBinNames.append(bName)
      mbBins[bName] = ( njet, lt, ht )
      for sb in [ "W", "tt" ]:
        if sb=="W":
          sbName = "J3"  + ltBinToLabel(lt) + htBinToLabel(ht) + dphiLimit
          if not sbName in sbBinNames:
            sbBinNames.append(sbName)
            sbBins[sbName] = ( njet, lt, ht )
        elif sb=="tt":
          sbName = "J4"  + ltBinToLabel(lt) + htBinToLabel(ht) + dphiLimit
          if not sbName in sbBinNames:
            sbBinNames.append(sbName)
            sbBins[sbName] = ( njet, lt, ht )            

#print mbBinNames
#print sbBinNames                
sigmasses = set()
for nj in sigres:
  for lt in sigres[nj]:
    for ht in sigres[nj][lt]:
      for mglu in sigres[nj][lt][ht]["signals"]:           
        for mlsp in sigres[nj][lt][ht]["signals"][mglu]:
          masses = ( mglu, mlsp )
          if not masses in sigmasses:
            sigmasses.add(masses)
 

signals = [ ]
for masses in sorted(sigmasses):
  mglu, mlsp = masses
  fmgluTeV = float(mglu)/1000.
  fmlspTeV = float(mlsp)/1000.
  label = 'T5q^{4}VV '
  label += '{0:3.1f}/{1:3.1f}/{2:3.1f}'.format(fmgluTeV,(fmgluTeV+fmlspTeV)/2.,fmlspTeV)
  signals.append({ 'color': ROOT.kBlack, 'name': 'S_'+str(mglu)+"_"+str(mlsp), \
                     'mglu': mglu, 'mlsp': mlsp, 'label': label })

for isig,signal in enumerate(signals):
  if args.signals!=None and not (isig in useSignalIndices):
    continue
  if useSignalMasses!=None and ( signal["mglu"]!=useSignalMasses[0] or signal["mlsp"]!=useSignalMasses[1] ):
    continue
  #print signal
  calc = CalcSingleLimit(bkgres,sbBinNames,sbBins,mbBinNames,mbBins,sigres,signal)
  calc.name = "limit_"+str(signal["mglu"])+"_"+str(signal["mlsp"])
  calc.runLimit = not args.nolimit
  calc.runBlind = args.blind
  calc.force = args.force
  if args.dir==None:
    calc.dir = "."
  else:
    if not os.path.isdir(args.dir):
      os.mkdir(args.dir)
    calc.dir = args.dir
  if args.bins!=None:
    calc.useBins = sorted(useBinIndices)
  calc.limitSinglePoint()
