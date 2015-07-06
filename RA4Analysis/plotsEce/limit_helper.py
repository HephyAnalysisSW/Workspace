from math import exp
import os,sys
import ROOT
import pickle
import array
import numpy as n


def plotsignif(signal_signif,path,option,lumi_origin) :
  can = ROOT.TCanvas("can","can",600,600)
  can.cd()
  latex = ROOT.TLatex()
  latex.SetNDC()
  latex.SetTextSize(0.035)
  latex.SetTextAlign(11)
  leg = ROOT.TLegend(0.55,0.2,0.95,0.3)
  leg.SetFillColor(0)

  gr = ROOT.TMultiGraph()
  for signal in signal_signif:
  #  print "x:" , signal['x'] , "y:" , signal['y']
    g_limit = ROOT.TGraph(len(signal['x']),signal['x'],signal['y'])
    g_limit.SetTitle("")
    g_limit.SetLineColor(signal['color'])
    g_limit.SetLineWidth(2)
    g_limit.SetMarkerStyle(22)
    g_limit.SetMarkerSize(1.5)
    g_limit.SetMarkerColor(signal['color'])
    g_limit.GetXaxis().SetTitle("Lumi fb^{-1}")
    g_limit.GetYaxis().SetTitle("#sigma")
    g_limit.GetYaxis().SetRangeUser(0,6)
    gr.Add(g_limit)
    #g_limit.Draw("AC")
    leg.AddEntry(g_limit,signal['label'] ,"l")


  gr.Draw("AC*")
  gr.GetXaxis().SetTitle("Integrated luminosity fb^{-1}")
  gr.GetYaxis().SetTitle("Expected significance in #sigma")

  leg.Draw()
  latex.DrawLatex(0.16,0.96,"CMS Simulation")
  latex.DrawLatex(0.71,0.96,"L="+str(lumi_origin)+" fb^{-1} (13 TeV)")
  #latex.DrawLatex(0.55,0.31,"bkg yield:"+str(round(tot_b_Y,2)))
  #latex.DrawLatex(0.55,0.35,"signal yield:"+str(round(tot_s_Y,2)))
  #latex.DrawLatex(0.55,0.39,"#sigma:"+str(round(sigma,2)))

  can.SaveAs(path+option+".root")
  can.SaveAs(path+option+".pdf")
  can.SaveAs(path+option+".png")
  print "plot saved :" , path


def plotLimit(signal,path,option,lumi_origin):
  can = ROOT.TCanvas("can","can",600,600)
  can.DrawFrame(0,0,11,7)
  can.cd()
  latex = ROOT.TLatex()
  latex.SetNDC()
  latex.SetTextSize(0.035)
  latex.SetTextAlign(11)
  leg = ROOT.TLegend(0.5,0.6,0.9,0.9)
  leg.SetFillColor(0)
  leg.SetBorderSize(0)
  g_limit = ROOT.TGraph(len(signal['x']),signal['x'],signal['y_m'])
  g_1min = ROOT.TGraph(len(signal['x']),signal['x'],signal['y1_min'])
  g_1max = ROOT.TGraph(len(signal['x']),signal['x'],signal['y1_max'])
  grshade1 = ROOT.TGraph(2*len(signal['x']))
  grshade2 = ROOT.TGraph(2*len(signal['x']))

  for i in range(int(len(signal['x']))):
     grshade1.SetPoint(i,signal['x'][i],signal['y1_max'][i])
     grshade1.SetPoint(len(signal['x'])+i,signal['x'][len(signal['x'])-i-1],signal['y1_min'][len(signal['x'])-i-1])
     grshade2.SetPoint(i,signal['x'][i],signal['y2_max'][i])
     grshade2.SetPoint(len(signal['x'])+i,signal['x'][len(signal['x'])-i-1],signal['y2_min'][len(signal['x'])-i-1])

  grshade2.SetFillColor(ROOT.kYellow)
  grshade2.Draw("f")
  grshade2.GetXaxis().SetTitle("Lumi fb^{-1}")
  grshade2.GetYaxis().SetTitle("r-value")
  grshade1.SetFillColor(ROOT.kGreen)
  grshade1.Draw("f")
  grshade1.GetXaxis().SetTitle("Lumi fb^{-1}")
  grshade1.GetYaxis().SetTitle("r-value")
  #grshade2.SetFillStyle(3013)
  leg.AddEntry(g_limit,"Expected limit" ,"l")
  leg.AddEntry(grshade1, "Expected #pm 1 #sigma" ,"f")
  leg.AddEntry(grshade2, "Expected #pm 2 #sigma" ,"f")


  func = ROOT.TF1('func',"[0]",1,10)
  func.SetParameter(0,1)
  func.SetLineColor(2)
  func.SetLineWidth(2)
  func.Draw("same")

  #g_1min.Draw("l")
  #g_1max.Draw("l")
  g_limit.SetLineWidth(2)
  g_limit.SetMarkerColor(1)
  g_limit.SetMarkerStyle(22)

  g_limit.Draw('same')
  g_limit.GetXaxis().SetTitle("Lumi fb^{-1}")
  g_limit.GetYaxis().SetTitle("r-value")
  #g_limit.GetYaxis().SetRangeUser(0,6)

  leg.AddEntry(func,"Theory "+signal['label'] ,"l")

  leg.Draw()
  #can.Draw()
  latex.DrawLatex(0.16,0.96,"CMS Simulation")
  latex.DrawLatex(0.71,0.96,"L="+str(lumi_origin)+" fb^{-1} (13 TeV)")


  can.SaveAs(path+option+signal['name']+".root")
  can.SaveAs(path+option+signal['name']+".pdf")
  can.SaveAs(path+option+signal['name']+".png")
  print "plot saved :" , path+option+signal['name']


def signal_bins_3fb():
  return [[\
    {'HT': (500  ,-1)   , 'ST': (250,350) , 'nJet': (5,5), 'dphi': 1},\
    ],\
    [\
    {'HT': (500  ,-1)   , 'ST': (350,450) , 'nJet': (5,5), 'dphi': 1},\
    ],\
    [\
    {'HT': (500  ,-1)   , 'ST': (450,-1) , 'nJet': (5,5), 'dphi': 1},\
    ],\
    [\
    {'HT': (500  ,750)   , 'ST': (250,350) , 'nJet': (6,7), 'dphi': 1},\
    {'HT': (750 , -1)  , 'ST': (250,350) , 'nJet': (6,7), 'dphi': 1},\
    ],\
    [\
    {'HT': (500  ,750)   , 'ST': (350,450) , 'nJet': (6,7), 'dphi': 1},\
    {'HT': (750 , -1)  , 'ST': (350,450) , 'nJet': (6,7), 'dphi': 1},\
    ],\
    [\
    {'HT': (500  ,750)   , 'ST': (450,-1) , 'nJet': (6,7), 'dphi': 0.75},\
    {'HT': (750 , 1250)  , 'ST': (450,-1) , 'nJet': (6,7), 'dphi': 0.75},\
    {'HT': (1250 , -1)  , 'ST': (450,-1) , 'nJet': (6,7), 'dphi': 0.75},\
    ],\
    [\
    {'HT': (500  ,750)   , 'ST': (250,350) , 'nJet': (8,-1), 'dphi': 1},\
    {'HT': (750 , -1)  , 'ST': (250,350) , 'nJet': (8,-1), 'dphi': 1},\
    ],\
    [\
    {'HT': (500  ,-1)   , 'ST': (350,450) , 'nJet': (8,-1), 'dphi': 0.75},\
    ],\
    [\
    {'HT': (500  ,-1)   , 'ST': (450,-1) , 'nJet': (8,-1), 'dphi': 0.75},\
    ],\
  ]

def signal_bins_3fb_table():
  return [\
    {'nJets': (5,5) , 'nnJets':3,'STbin': [\
    { 'nST': 1,'ST':(250,350) ,'dPhi':1.0,'HTbin':[(500 , -1)]},\
    { 'nST': 1,'ST':(350,450) ,'dPhi':1.0,'HTbin':[(500 , -1)]},\
    { 'nST': 1,'ST':(450,-1) , 'dPhi':1.0,'HTbin':[(500 , -1)]},\
    ]},\
    {'nJets': (6,7) , 'nnJets':6,'STbin': [\
    { 'nST': 2,'ST':(250,350) ,'dPhi':1.0, 'HTbin':[(500  ,750) ,(750 , -1)]},\
    { 'nST': 2,'ST':(350,450) ,'dPhi':1.0, 'HTbin':[(500  ,750) ,(750 , -1)]},\
    { 'nST': 2,'ST':(450,-1) , 'dPhi':0.75, 'HTbin':[(500  ,1000) ,(1000 , -1)]},\
    ]},\
    {'nJets': (8,-1) , 'nnJets':4,'STbin': [\
    { 'nST': 2,'ST':(250,350) ,'dPhi':1.0, 'HTbin':[(500  ,750) ,(750 , -1)]},\
    { 'nST': 1,'ST':(350,450) ,'dPhi':0.75, 'HTbin':[(500  ,-1)]},\
    { 'nST': 1,'ST':(450,-1) , 'dPhi':0.75,'HTbin':[(500,  -1)]},\
    ]}\
       ]                                                                           
