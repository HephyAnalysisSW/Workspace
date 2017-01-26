#!/usr/bin/env python
import ROOT
import os, argparse, types, sys
from dataBase import *


ROOT.gROOT.SetStyle("Plain")
ROOT.gROOT.SetBatch() #canvas will not be drawn
ROOT.gStyle.SetOptStat(0000)
#ROOT.TGaxis.SetMaxDigits(4)
ROOT.gStyle.SetCanvasBorderMode(0)
ROOT.gStyle.SetPadLeftMargin(0.15)
ROOT.gStyle.SetPadRightMargin(0.05)
ROOT.gStyle.SetPadBottomMargin(0.2)
ROOT.gStyle.SetPadTopMargin(0.1)

#----------------------------#Configure plot from here#----------------------#
bar_color = ROOT.kGray
bar_width  =  0.9 
tex_width  =  1.035 #will determine pas names spacing 
histo_xaxis_max = 2000
line_color = ROOT.kBlue
line_depence = 1.03
path = "/afs/hephy.at/user/e/easilar/www/barplots/" #TODO
#path = os.getcwd()+'/'
filename='barplot_v2'
debug = True
#----------------------------#------------------------#----------------------#


#for analysis_group in all_analysis.keys():
#  print "there are " , len([x for x in all_analysis[analysis_group].keys() if "-" in x]) , " analysis for " , all_analysis[analysis_group]["name_tex"]

all_analysis_list  = [x for y in all_analysis.keys() for x in all_analysis[y].keys() if not "name" in x ] #with empties
xmax = len(all_analysis_list)
#print "in total there are " , xmax ,"analysis histogram xmas will be " , xmax+1 , ".This result is calculated with 4 empty histogram" 

#---------defining histograms-----------
c = ROOT.TCanvas()
bins = xmax
xmin = 0
#----------create TH1F with fixed bins-----------------
hmax05 = ROOT.TH1F('hmax05', '', bins, xmin, xmax+1)

#-----------fill histograms--------------

index = 0
for analysis_group in all_analysis:
  name_tex = all_analysis[str(analysis_group)]["name_tex"] 
  print 8*"*" , "in the analysis group : " , name_tex , 8*"*" # e.g. Stop&Sbottom
  Tot = len(all_analysis[str(analysis_group)].keys())  
  for num in reversed(range(1,Tot+1)):              # This loop respectes the ordering definined by 'pos' int he dictionary!
    for interp in all_analysis[str(analysis_group)] :
      if debug : print 'INTERP',interp
      if "-" in interp : 
         if debug : print 4*"-" , "interp is :" , interp
         interp_dict = all_analysis[analysis_group][interp] 
         if debug : 
          print interp_dict.keys()
          print "for this pas :" , interp_dict["max"]["050"][1] 
          print "for this lumi :" , interp_dict["max"]["050"][3] 
          print "the limit will be set to :" , interp_dict["max"]["050"][0] 
          print "with label :" , interp_dict["decay"]
          if interp_dict['pos']==num:
            if debug : print num , interp_dict['pos'] , interp
            hmax05.SetBinContent(index+1, interp_dict["max"]["050"][0])
            hmax05.GetXaxis().SetBinLabel(index+1, interp_dict["decay"])
            index +=1

#----------draw plot-----------

c.cd()
hmax05.SetFillColor(bar_color)
hmax05.SetStats(0)
hmax05.SetBarWidth(bar_width)
hmax05.SetBarOffset(0.05)
hmax05.SetTickLength(0)
hmax05.GetYaxis().SetTickLength(0.015)
hmax05.SetYTitle("Mass scale [GeV]")
hmax05.GetYaxis().SetTitleFont(42)
hmax05.SetTitleSize(0.025, "Y")
hmax05.GetYaxis().SetTitleOffset(1.1)
hmax05.SetLabelSize(0.015, "X")
hmax05.SetLabelSize(0.025, "Y")
hmax05.SetLabelFont(42, "X")
hmax05.SetLabelFont(42, "Y")
#hmax05.GetYaxis().CenterTitle() 
hmax05.SetMaximum(histo_xaxis_max)
hmax05.Draw('HBAR0')
#------For PAS numbers / Production Types ------
latex_pas = ROOT.TLatex()
latex_pas.SetTextSize(0.013)
latex_pas.SetLineWidth(2)
latex_ana = ROOT.TLatex()
latex_ana.SetTextColor(line_color)
latex_ana.SetTextFont(70)
latex_ana.SetTextSize(0.015)
latex_ana.SetTextAngle(90)
latex_ana.SetLineWidth(2)
latex_ana.Draw()
pas_place = 0.1
i = 0

for analysis_group in all_analysis:
  name_tex = all_analysis[str(analysis_group)]["name_tex"]
                  #  print "writing pas for :" , name_tex
                                      #  print 'NAME TEX', name_tex # e.g. Stop and Sbottom
  latex_ana.DrawLatex(-320,i*1.02 ,name_tex)

  Tot = len(all_analysis[str(analysis_group)].keys())  
  for num in reversed(range(1,Tot+1)):  
   for interp in all_analysis[str(analysis_group)] :
    if "-" in interp:
                                                                      # This loop respectes the ordering definined by 'pos' int he dictionary!
     interp_dict = all_analysis[analysis_group][interp]         #

     if(interp_dict['pos']==num ):              #

       latex_pas.DrawLatex(20,pas_place-all_analysis[analysis_group]["pp_difference"] ,interp_dict["max"]["050"][1]+' ' +interp_dict['search'] ) # Print CMS-SUS-XXX 0L '-like

       if analysis_group == 'Squark' and (not 'empty' in interp):
         latex_pas.DrawLatex(interp_dict["max"]["050"][0]+10,pas_place-all_analysis[analysis_group]["pp_difference"] ,squarks)          
       if debug :print interp_dict
       if 'x' in interp_dict.keys():
          if  (analysis_group == 'EWKGauginos'): latex_pas.DrawLatex(550,pas_place-0.15 ,'x='+str(interp_dict["x"]) )
          else: latex_pas.DrawLatex(550,pas_place ,'x='+str(interp_dict["x"]) )

       if "empty" in interp:
          if debug :     print "empty from " , name_tex
          exec('line_'+str(i)+' = ROOT.TLine(-320,(i*line_depence)+0.5,histo_xaxis_max,(i*line_depence)+0.5)')
          exec('line_'+str(i)+'.SetLineColor(line_color)')
          exec('line_'+str(i)+'.SetLineStyle(7)')
          exec('line_'+str(i)+'.Draw()')
       pas_place += tex_width
       i += 1

#------------CMS Headers ------------------------#
tex = ROOT.TLatex(0,43.0,"Selected CMS SUSY Results* - SMS Interpretation")
tex.SetTextSize(0.035)
tex.SetLineWidth(2)
tex.Draw()
tex2 = ROOT.TLatex(1480,43.0,"ICHEP 2016 data set")
tex2.SetTextSize(0.035)
tex2.SetLineWidth(2)
tex2.Draw()
tex1 = ROOT.TLatex(1400,10,"CMS Preliminary")
tex1.SetTextSize(0.04)
tex1.SetLineWidth(2)
tex1.Draw()
tex3 = ROOT.TLatex(1410,7.8,"#sqrt{s} = 13 TeV , L  = 12.9 fb^{-1}")
tex3.SetTextSize(0.025)
tex3.SetLineWidth(2)
tex3.Draw()
#-------------Foot note--------------------------#
tex4 = ROOT.TLatex(1400,2.7,"#splitline{For decays with intermediate mass,}{m_{intermediate} = x#upoint m_{Mother}+(1-x)#upoint m_{LSP}}");
tex4.SetTextFont(42);
tex4.SetTextSize(0.02);
tex4.SetLineWidth(2);
tex4.Draw();
tex5 = ROOT.TLatex(-0,-4.5,"#splitline{Observed limits at 95% C.L. - theory uncertainties not included}{Only a selection of available mass limits. Probe *up to* the quoted mass limit for  m _{LSP}~0 GeV }");
tex5.SetTextFont(42);
tex5.SetTextSize(0.021);
tex5.SetLineWidth(2);
tex5.Draw();
#tex6 = ROOT.TLatex(-0,-6.6,"Probe *up to* the quoted mass limit for m_{LSP}= 0 GeV");
#tex6.SetTextFont(42);
#tex6.SetTextSize(0.021);
#tex6.SetLineWidth(2);
#tex6.Draw();
tex6 = ROOT.TLatex(-0,-6.9,"** Probe up to m _{#tilde{t}} - m_{LSP}= 80 GeV; probe up to m_{#tilde{#chi}^{#pm}_{1},#tilde{#chi}^{0}_{2}} - m_{LSP}= 40 GeV");
tex6.SetTextFont(42);
tex6.SetTextSize(0.021);
tex6.SetLineWidth(2);
tex6.Draw();

#------------put save directories----------------#

#if not os.path.exists(path):
#    os.makedirs(path)

c.Print(path+filename+".pdf")
c.Print(path+filename+".C")
c.Print(path+filename+".png")
c.Print(path+filename+".root")


