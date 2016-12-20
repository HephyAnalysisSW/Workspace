#!/usr/bin/env python


import ROOT
import os, argparse, types, sys


ROOT.gROOT.SetStyle("Plain")
ROOT.gROOT.SetBatch() #canvas will not be drawn
ROOT.gStyle.SetOptStat(0000)
#ROOT.TGaxis.SetMaxDigits(4)
ROOT.gStyle.SetCanvasBorderMode(0)
ROOT.gStyle.SetPadLeftMargin(0.16)
ROOT.gStyle.SetPadRightMargin(0.02)
ROOT.gStyle.SetPadBottomMargin(0.11)
ROOT.gStyle.SetPadTopMargin(0.07)

#---------get data from dic's----------------
#sorthistos = ['TSlepSlep8','empty1','TChiChipmStauStau8','TChiChipmSlepStau8','TChiHW8','TChiWZ8','TChipChimSlepSnu8','TChiChipmSlepL8','empty2','T6bbZZ8','T6ttWW8','T2bb8','empty3','T2btHG8','T2bw7','T6bbWW8','T2tt7','T2tt8','empty4','T27','T28','empty5','T7btbtWW8','T5gg7','T5wg7','T5WW8','T5ZZ7','T5lnu7','T5tttt8','T3W7','T3tauh7','T3lh7','T1tttt8','T1bbbb8','T17','T18','empty'] 
# TODO sorthistos = ['TChiChipmStauStau8','TChiChipmSlepStau8','TChiHW8','TChiHZ8','TChiWZ8','TChiZZ8','TChipChimSlepSnu8','TChiChipmSlepL8',"empty"] 

sorthistos = ['16-028-T2tt','16-028-T6bbWW', 
              '16-029-T2tt', '16-029-T6bbWW',
              '16-024-TChiChipmSlepL','16-024-TChiChipmStauStau', '16-024-TChiWZ','16-024-TChiWH',
              '16-022-T1tttt', '16-022-T5VV',
              '16-016-T1bbbb', '16-016-T1tttt','16-016-T2bb','16-016-T2tt',
              '16-015-T1bbbb', '16-015-T1tttt', '16-015-T1', '16-015-T2bb', '16-015-T2tt', '16-015-T2', 
              '16-014-T2tt', '16-014-T2bb', '16-014-T1tttt','16-014-T1bbbb', '16-014-T1', '16-014-T2','16-014-T5VV',  
              '16-012-T6bbHH',
              '16-019-T5WW','16-019-T1tttt',
	      '16-030-T2tt', '16-030-T1tttt', '16-030-T5tctc',


"empty"]







Globals = {}
execfile('ICHEP_2016.py',Globals)
bars = Globals['bars']
bars.update({'legend':{'max':{'025':[2200.], '050':[2200.], '075':[2200.]}, 'delta':{'025':[475.], '050':[500.], '075':[525.]}, 'decay': ' '}})
#---------defining histograms-----------

c = ROOT.TCanvas('1800','1800')
#print len(bars)
bins = len(bars)
xmin = 0
xmax = len(bars) 

#----------create TH1F with fixed bins-----------------
hmax1 = ROOT.TH1F('hmax1', '', bins, xmin, xmax)
hmax2 = ROOT.TH1F('hmax2', '', bins, xmin, xmax)
hmax3 = ROOT.TH1F('hmax3', '', bins, xmin, xmax)
hmax05 = ROOT.TH1F('hmax05', '', bins, xmin, xmax)
hdelta1 = ROOT.TH1F('hdelta1', '', bins, xmin, xmax)
hdelta2 = ROOT.TH1F('hdelta2', '', bins, xmin, xmax)
hdelta3 = ROOT.TH1F('hdelta3', '', bins, xmin, xmax)
hdelta05 = ROOT.TH1F('hdelta05', '', bins, xmin, xmax)
hmax4 = ROOT.TH1F('hmax4', '', bins, xmin, xmax)
hmax5 = ROOT.TH1F('hmax5', '', bins, xmin, xmax)
hmax6 = ROOT.TH1F('hmax6', '', bins, xmin, xmax)
hmax058 = ROOT.TH1F('hmax058', '', bins, xmin, xmax)
hdelta4 = ROOT.TH1F('hdelta4', '', bins, xmin, xmax)
hdelta5 = ROOT.TH1F('hdelta5', '', bins, xmin, xmax)
hdelta6 = ROOT.TH1F('hdelta6', '', bins, xmin, xmax)
hdelta058 = ROOT.TH1F('hdelta058', '', bins, xmin, xmax)
hchange7 = ROOT.TH1F('hchange7', '', bins, xmin, xmax)
hchange8 = ROOT.TH1F('hchange8', '', bins, xmin, xmax)
hmin05 = ROOT.TH1F('hmin05', '', bins, xmin, xmax)
hmin1 = ROOT.TH1F('hmin1', '', bins, xmin, xmax)
hmin2 = ROOT.TH1F('hmin2', '', bins, xmin, xmax)
hmin3 = ROOT.TH1F('hmin3', '', bins, xmin, xmax)


#histos = ['hmax1' ,'hmax2', 'hmax3', 'hmax4', 'hmax5', 'hmax6', 'hdelta1', 'hdelta2', 'hdelta3', 'hdelta4', 'hdelta5', 'hdelta6', 'hmax05', 'hdelta05', 'hmax058', 'hdelta058']

#-----------fill histograms--------------

text = {}
i = 0
#t = [] just for testing
for topo in sorthistos:
	name = topo
	if ('empty' in topo):
		hmax1.Fill(name, 0.)
		hmax2.Fill(name, 0.)
		hmax3.Fill(name, 0.)
		hmax4.Fill(name, 0.)
		hmax5.Fill(name, 0.)
		hmax6.Fill(name, 0.)
		hdelta1.Fill(name, 0.)
		hdelta2.Fill(name, 0.)
		hdelta3.Fill(name, 0.)
		hdelta4.Fill(name, 0.)
		hdelta5.Fill(name, 0.)
		hdelta6.Fill(name, 0.)
		hmax05.Fill(name, 0.)
		hmax058.Fill(name, 0.)
		hdelta05.Fill(name, 0.)
		hdelta058.Fill(name, 0.)
#		hmin05.Fill(name, 0.)
#		hmin1.Fill(name, 0.)
#		hmin2.Fill(name, 0.)
#		hmin3.Fill(name, 0.)
		
		i += 1
		continue
	text.update({topo:{'PAS':[], 'ypos': i, 'lumi': []}})
	i += 1
	if (len(bars[topo]['max']) == 1) and (len(bars[topo]['delta']) == 1):
		if bars[topo]['max']['050'][2] == 7:
			hmax05.Fill(name, bars[topo]['max']['050'][0])
			hmax1.Fill(name, 0.)
			hmax2.Fill(name, 0.)
			hmax3.Fill(name, 0.)
			hmax058.Fill(name, 0.)
			hmax4.Fill(name, 0.)
			hmax5.Fill(name, 0.)
			hmax6.Fill(name, 0.)
			if not bars[topo]['max']['050'][1] in text[topo]['PAS']:
				text[topo]['PAS'].append(bars[topo]['max']['050'][1])
			if not bars[topo]['max']['050'][3] in text[topo]['lumi']:
				text[topo]['lumi'].append(bars[topo]['max']['050'][3])
   	    	elif bars[topo]['max']['050'][2] == 8:
#			print bars[topo]['max']['050'][0], topo
			hmax058.Fill(name, bars[topo]['max']['050'][0])
			hmax1.Fill(name, 0.)
			hmax2.Fill(name, 0.)
			hmax3.Fill(name, 0.)
			hmax05.Fill(name, 0.)
			hmax4.Fill(name, 0.)
			hmax5.Fill(name, 0.)
			hmax6.Fill(name, 0.)
			if not bars[topo]['max']['050'][1] in text[topo]['PAS']:
				text[topo]['PAS'].append(bars[topo]['max']['050'][1])
			if not bars[topo]['max']['050'][3] in text[topo]['lumi']:
				text[topo]['lumi'].append(bars[topo]['max']['050'][3])
		else:
			print 'Dont know if 7 or 8 TeV'
       		if bars[topo]['delta']['050'][2] == 7:
			hdelta05.Fill(name, bars[topo]['delta']['050'][0])
			hdelta1.Fill(name, 0.)
			hdelta2.Fill(name, 0.)
			hdelta3.Fill(name, 0.)
			hdelta058.Fill(name, 0.)
			hdelta4.Fill(name, 0.)
			hdelta5.Fill(name, 0.)
			hdelta6.Fill(name, 0.)
			if not bars[topo]['delta']['050'][1] in text[topo]['PAS']:
				text[topo]['PAS'].append(bars[topo]['delta']['050'][1])
			if not bars[topo]['delta']['050'][3] in text[topo]['lumi']:
				text[topo]['lumi'].append(bars[topo]['delta']['050'][3])
		elif bars[topo]['delta']['050'][2] == 8:
			hdelta058.Fill(name, bars[topo]['delta']['050'][0])
			hdelta1.Fill(name, 0.)
			hdelta2.Fill(name, 0.)
			hdelta3.Fill(name, 0.)
			hdelta05.Fill(name, 0.)
			hdelta4.Fill(name, 0.)
			hdelta5.Fill(name, 0.)
			hdelta6.Fill(name, 0.)
			if not bars[topo]['delta']['050'][1] in text[topo]['PAS']:
				text[topo]['PAS'].append(bars[topo]['delta']['050'][1])
			if not bars[topo]['delta']['050'][3] in text[topo]['lumi']:
				text[topo]['lumi'].append(bars[topo]['delta']['050'][3])
		else:
			print 'Dont know if 7 or 8 TeV'

	else:
		hmax05.Fill(name, 0.)
		hdelta05.Fill(name, 0.)
		hmax058.Fill(name, 0.)
		hdelta058.Fill(name, 0.)
		kmax = bars[topo]['max'].keys()
		kmax.sort()
		if topo == 'T2tt8':
			kmax = ['L', '050', 'R']
		if len(kmax) == 3:
			if bars[topo]['max'][kmax[2]][2] == 7:
				hmax1.Fill(name, bars[topo]['max'][kmax[2]][0])
				hmax4.Fill(name, 0.)
#				if not bars[topo]['max'][kmax[2]][1] in text[topo]['PAS']:			
#					text[topo]['PAS'].append(bars[topo]['max'][kmax[2]][1])
#					text[topo]['lumi'].append(bars[topo]['max']['050'][3])
			elif bars[topo]['max'][kmax[2]][2] == 8:
				hmax4.Fill(name, bars[topo]['max'][kmax[2]][0])
				hmax1.Fill(name, 0.)
#				if not bars[topo]['max'][kmax[2]][1] in text[topo]['PAS']:
#					text[topo]['PAS'].append(bars[topo]['max'][kmax[2]][1])
#					text[topo]['lumi'].append(bars[topo]['max']['050'][3])
			else:
				print 'Dont know if 7 or 8 TeV'
			if bars[topo]['max'][kmax[1]][2] == 7:
				hmax2.Fill(name, bars[topo]['max'][kmax[1]][0])
				hmax5.Fill(name, 0.)
#				if not bars[topo]['max'][kmax[1]][1] in text[topo]['PAS']:
#					text[topo]['PAS'].append(bars[topo]['max'][kmax[1]][1])
#					text[topo]['lumi'].append(bars[topo]['max']['050'][3])
			elif bars[topo]['max'][kmax[1]][2] == 8:
				hmax5.Fill(name, bars[topo]['max'][kmax[1]][0])
				hmax2.Fill(name, 0.)
#				if not bars[topo]['max'][kmax[1]][1] in text[topo]['PAS']:
#					text[topo]['PAS'].append(bars[topo]['max'][kmax[1]][1])
#					text[topo]['lumi'].append(bars[topo]['max']['050'][3])
			else:
				print 'Dont know if 7 or 8 TeV'
			if bars[topo]['max'][kmax[0]][2] == 7:
				hmax3.Fill(name, bars[topo]['max'][kmax[0]][0])
				hmax6.Fill(name, 0.)
#				if not bars[topo]['max'][kmax[0]][1] in text[topo]['PAS']:
#					text[topo]['PAS'].append(bars[topo]['max'][kmax[0]][1])
#					text[topo]['lumi'].append(bars[topo]['max']['050'][3])
			elif bars[topo]['max'][kmax[0]][2] == 8:
				hmax6.Fill(name, bars[topo]['max'][kmax[0]][0])
				hmax3.Fill(name, 0.)
#				if not bars[topo]['max'][kmax[0]][1] in text[topo]['PAS']:
#					text[topo]['PAS'].append(bars[topo]['max'][kmax[0]][1])
#					text[topo]['lumi'].append(bars[topo]['max']['050'][3])
			else:
				print 'Dont know if 7 or 8 TeV'
			for k in kmax:
				if not bars[topo]['max'][k][1] in text[topo]['PAS']:
					text[topo]['PAS'].append(bars[topo]['max'][k][1])
				if not bars[topo]['max'][k][3] in text[topo]['lumi']:
					text[topo]['lumi'].append(bars[topo]['max'][k][3])


		elif len(kmax) == 2:
			if kmax[0] == '050':
				if bars[topo]['max'][kmax[1]][2] == 7:
					hmax1.Fill(name, bars[topo]['max'][kmax[1]][0])
					hmax4.Fill(name, 0.)
#					if not bars[topo]['max'][kmax[1]][1] in text[topo]['PAS']:
#						text[topo]['PAS'].append(bars[topo]['max'][kmax[1]][1])
#						text[topo]['lumi'].append(bars[topo]['max']['050'][3])
				elif bars[topo]['max'][kmax[1]][2] == 8:
					hmax4.Fill(name, bars[topo]['max'][kmax[1]][0])
					hmax1.Fill(name, 0.)
#					if not bars[topo]['max'][kmax[1]][1] in text[topo]['PAS']:
#						text[topo]['PAS'].append(bars[topo]['max'][kmax[1]][1])
#						text[topo]['lumi'].append(bars[topo]['max']['050'][3])
				else:
					print 'Dont know if 7 or 8 TeV'
				if bars[topo]['max'][kmax[0]][2] == 7:
					hmax2.Fill(name, bars[topo]['max'][kmax[0]][0])
					hmax5.Fill(name, 0.)
#					if not bars[topo]['max'][kmax[0]][1] in text[topo]['PAS']:
#						text[topo]['PAS'].append(bars[topo]['max'][kmax[0]][1])
				elif bars[topo]['max'][kmax[0]][2] == 8:
					hmax5.Fill(name, bars[topo]['max'][kmax[0]][0])
					hmax2.Fill(name, 0.)
#					if not bars[topo]['max'][kmax[0]][1] in text[topo]['PAS']:
#						text[topo]['PAS'].append(bars[topo]['max'][kmax[0]][1])
				else:
					print 'Dont know if 7 or 8 TeV'
				hmax3.Fill(name, 0.)
				hmax6.Fill(name, 0.)
			elif kmax[1] == '050':
				hmax1.Fill(name, 0.)
				hmax4.Fill(name, 0.)
				if bars[topo]['max'][kmax[1]][2] == 7:
					hmax2.Fill(name, bars[topo]['max'][kmax[1]][0])
					hmax5.Fill(name, 0.)
#					if not bars[topo]['max'][kmax[1]][1] in text[topo]['PAS']:
#						text[topo]['PAS'].append(bars[topo]['max'][kmax[1]][1])
				elif bars[topo]['max'][kmax[1]][2] == 8:
					hmax5.Fill(name, bars[topo]['max'][kmax[1]][0])
					hmax2.Fill(name, 0.)
#					if not bars[topo]['max'][kmax[1]][1] in text[topo]['PAS']:
#						text[topo]['PAS'].append(bars[topo]['max'][kmax[1]][1])
				else:
					print 'Dont know if 7 or 8 TeV'
				if bars[topo]['max'][kmax[0]][2] == 7:
					hmax3.Fill(name, bars[topo]['max'][kmax[0]][0])
					hmax6.Fill(name, 0.)
#					if not bars[topo]['max'][kmax[0]][1] in text[topo]['PAS']:
#						text[topo]['PAS'].append(bars[topo]['max'][kmax[0]][1])
				elif bars[topo]['max'][kmax[0]][2] == 8:
					hmax6.Fill(name, bars[topo]['max'][kmax[0]][0])
					hmax3.Fill(name, 0.)
#					if not bars[topo]['max'][kmax[0]][1] in text[topo]['PAS']:
#						text[topo]['PAS'].append(bars[topo]['max'][kmax[0]][1])

				else:
					print 'Dont know if 7 or 8 TeV'
			else:
				print 'ERROR'
			for k in kmax:
				if not bars[topo]['max'][k][1] in text[topo]['PAS']:
					text[topo]['PAS'].append(bars[topo]['max'][k][1])
				if not bars[topo]['max'][k][3] in text[topo]['lumi']:
					text[topo]['lumi'].append(bars[topo]['max'][k][3])

		elif len(kmax) == 1:
			if kmax[0] == '050':
				hmax1.Fill(name, 0.)
				hmax4.Fill(name, 0.)
				if bars[topo]['max'][kmax[0]][2] == 7:
					hmax2.Fill(name, bars[topo]['max'][kmax[0]][0])
					hmax5.Fill(name, 0.)
				elif bars[topo]['max'][kmax[0]][2] == 8:
					hmax5.Fill(name, bars[topo]['max'][kmax[0]][0])
					hmax2.Fill(name, 0.)
				hmax3.Fill(name, 0.)
				hmax6.Fill(name, 0.)
#				if not bars[topo]['max'][kmax[0]][1] in text[topo]['PAS']:
#					text[topo]['PAS'].append(bars[topo]['max'][kmax[0]][1])
				for k in kmax:
					if not bars[topo]['max'][k][1] in text[topo]['PAS']:
						text[topo]['PAS'].append(bars[topo]['max'][k][1])
					if not bars[topo]['max'][k][3] in text[topo]['lumi']:
						text[topo]['lumi'].append(bars[topo]['max'][k][3])

		else:
			print 'ERROR'
		kdelta = bars[topo]['delta'].keys()
		kdelta.sort()
		if topo == 'T2tt8':
			kdelta = ['L', '050', 'R']
		if len(kdelta) == 3:
			if bars[topo]['delta'][kdelta[2]][2] == 7:
				hdelta1.Fill(name, bars[topo]['delta'][kdelta[2]][0])
				hdelta4.Fill(name, 0.)
			elif bars[topo]['delta'][kdelta[2]][2] == 8:
				hdelta4.Fill(name, bars[topo]['delta'][kdelta[2]][0])
				hdelta1.Fill(name, 0.)
			else:
				print 'Dont know if 7 or 8 TeV'
			if bars[topo]['delta'][kdelta[1]][2] == 7:
				hdelta2.Fill(name, bars[topo]['delta'][kdelta[1]][0])
				hdelta5.Fill(name, 0.)
			elif bars[topo]['delta'][kdelta[1]][2] == 8:
				hdelta5.Fill(name, bars[topo]['delta'][kdelta[1]][0])
				hdelta2.Fill(name, 0.)
			else:
				print 'Dont know if 7 or 8 TeV'
			if bars[topo]['delta'][kdelta[0]][2] == 7:
				hdelta3.Fill(name, bars[topo]['delta'][kdelta[0]][0])
				hdelta6.Fill(name, 0.)
			elif bars[topo]['delta'][kdelta[0]][2] == 8:
				hdelta6.Fill(name, bars[topo]['delta'][kdelta[0]][0])
				hdelta3.Fill(name, 0.)
			else:
				print 'Dont know if 7 or 8 TeV'
			for k in kdelta:
				if not bars[topo]['delta'][k][1] in text[topo]['PAS']:
					text[topo]['PAS'].append(bars[topo]['delta'][k][1])
				if not bars[topo]['delta'][k][3] in text[topo]['lumi']:
					text[topo]['lumi'].append(bars[topo]['delta'][k][3])
#			hdelta1.Fill(name, bars[topo]['delta'][kdelta[1]][0])
#			hdelta2.Fill(name, bars[topo]['delta'][kdelta[2]][0])
#			hdelta3.Fill(name, bars[topo]['delta'][kdelta[0]][0])
		elif len(kdelta) == 2:
			if kdelta[0] == '050':
				if bars[topo]['delta'][kdelta[1]][2] == 7:
					hdelta1.Fill(name, bars[topo]['delta'][kdelta[1]][0])
					hdelta4.Fill(name, 0.)
				elif bars[topo]['delta'][kdelta[1]][2] == 8:
					hdelta4.Fill(name, bars[topo]['delta'][kdelta[1]][0])
					hdelta1.Fill(name, 0.)
				else:
					print 'Dont know if 7 or 8 TeV'
				if bars[topo]['delta'][kdelta[0]][2] == 7:
					hdelta2.Fill(name, bars[topo]['delta'][kdelta[0]][0])
					hdelta5.Fill(name, 0.)
				elif bars[topo]['delta'][kdelta[0]][2] == 8:
					hdelta5.Fill(name, bars[topo]['delta'][kdelta[0]][0])
					hdelta2.Fill(name, 0.)
				else:
					print 'Dont know if 7 or 8 TeV'
#				hdelta1.Fill(name, bars[topo]['delta'][kdelta[1]][0])
#				hdelta2.Fill(name, bars[topo]['delta'][kdelta[0]][0])
				hdelta3.Fill(name, 0.)
				hdelta6.Fill(name, 0.)
				for k in kdelta:
					if not bars[topo]['delta'][k][1] in text[topo]['PAS']:
						text[topo]['PAS'].append(bars[topo]['delta'][k][1])
					if not bars[topo]['delta'][k][3] in text[topo]['lumi']:
						text[topo]['lumi'].append(bars[topo]['delta'][k][3])
			elif kdelta[1] == '050':
				hdelta1.Fill(name, 0.)
				hdelta4.Fill(name, 0.)
				if bars[topo]['delta'][kdelta[1]][2] == 7:
					hdelta2.Fill(name, bars[topo]['delta'][kdelta[1]][0])
					hdelta5.Fill(name, 0.)
				elif bars[topo]['delta'][kdelta[1]][2] == 8:
					hdelta5.Fill(name, bars[topo]['delta'][kdelta[1]][0])
					hdelta2.Fill(name, 0.)
				else:
					print 'Dont know if 7 or 8 TeV'
				if bars[topo]['delta'][kdelta[0]][2] == 7:
					hdelta3.Fill(name, bars[topo]['delta'][kdelta[0]][0])
					hdelta6.Fill(name, 0.)
				elif bars[topo]['delta'][kdelta[0]][2] == 8:
					hdelta6.Fill(name, bars[topo]['delta'][kdelta[0]][0])
					hdelta3.Fill(name, 0.)
				else:
					print 'Dont know if 7 or 8 TeV'
				for k in kdelta:
					if not bars[topo]['delta'][k][1] in text[topo]['PAS']:
						text[topo]['PAS'].append(bars[topo]['delta'][k][1])
					if not bars[topo]['delta'][k][3] in text[topo]['lumi']:
						text[topo]['lumi'].append(bars[topo]['delta'][k][3])
#				hdelta2.Fill(name, bars[topo]['delta'][kdelta[1]][0])
#				hdelta3.Fill(name, bars[topo]['delta'][kdelta[0]][0])
			else:
				print 'ERROR'
		elif len(kdelta) == 1:
			if kdelta[0] == '050':
				hdelta1.Fill(name, 0.)
				hdelta4.Fill(name, 0.)
				if bars[topo]['delta'][kdelta[0]][2] == 7:
					hdelta2.Fill(name, bars[topo]['delta'][kdelta[0]][0])
					hdelta5.Fill(name, 0.)
				elif bars[topo]['delta'][kdelta[0]][2] == 8:
					hdelta5.Fill(name, bars[topo]['delta'][kdelta[0]][0])
					hdelta2.Fill(name, 0.)
				else:
					print 'Dont know if 7 or 8 TeV'
				hdelta3.Fill(name, 0.)
				hdelta6.Fill(name, 0.)
				for k in kdelta:
					if not bars[topo]['delta'][k][1] in text[topo]['PAS']:
						text[topo]['PAS'].append(bars[topo]['delta'][k][1])
					if not bars[topo]['delta'][k][3] in text[topo]['lumi']:
						text[topo]['lumi'].append(bars[topo]['delta'][k][3])
		else:
			print 'ERROR'
print text

name = 'legend'
hmax1.Fill(name, bars['legend']['max']['075'][0])
hmax2.Fill(name, bars['legend']['max']['050'][0])
hmax3.Fill(name, bars['legend']['max']['025'][0])
hmax4.Fill(name, 0.)
hmax5.Fill(name, 0.)
hmax6.Fill(name, 0.)
hdelta1.Fill(name, bars['legend']['delta']['075'][0])
hdelta2.Fill(name, bars['legend']['delta']['050'][0])
hdelta3.Fill(name, bars['legend']['delta']['025'][0])
hdelta4.Fill(name, 0.)
hdelta5.Fill(name, 0.)
hdelta6.Fill(name, 0.)
hmax05.Fill(name, 0.)
hmax058.Fill(name, 0.)
hdelta05.Fill(name, 0.)
hdelta058.Fill(name, 0.)

hmax05.Copy(hchange7)
hmax058.Copy(hchange8)

for h in range(0, len(bars)-1):
	max7 = hchange7.GetBinContent(h)
	delta7 = hdelta05.GetBinContent(h)
#	print max7, delta7
	if max7 > delta7:
		hchange7.SetBinContent(h, 0.)
#		print 'SET', hchange7.GetBinContent(h), hmax05.GetBinContent(h)
	max8 = hchange8.GetBinContent(h)
	delta8 = hdelta058.GetBinContent(h)
	if max8 > delta8:
		hchange8.SetBinContent(h, 0.)

#--------add dashed lines and box----------------
#y0 = hmax05.GetXaxis().FindBin('empty6')
#y1 = hmax05.GetXaxis().FindBin('empty5')
#y2 = hmax05.GetXaxis().FindBin('empty4')
#y3 = hmax05.GetXaxis().FindBin('empty3')
#y4 = hmax05.GetXaxis().FindBin('empty2')
#y5 = hmax05.GetXaxis().FindBin('empty1')

#line0 = ROOT.TLine(-200.,y0-0.5, 1900., y0-0.5)
#line1 = ROOT.TLine(-200.,y1-0.5, 1900., y1-0.5)
#line2 = ROOT.TLine(-200.,y2-0.5, 1900., y2-0.5)
#line3 = ROOT.TLine(-200.,y3-0.5, 1900., y3-0.5)
#line4 = ROOT.TLine(-200.,y4-0.5, 1900., y4-0.5)
#line5 = ROOT.TLine(-200.,y5-0.5, 1900., y5-0.5)

#line0.SetLineStyle(7)
#line1.SetLineStyle(7)
#line2.SetLineStyle(7)
#line3.SetLineStyle(7)
#line4.SetLineStyle(7)
#line5.SetLineStyle(7)

#line0.SetLineColor(ROOT.kGray+1)
#line1.SetLineColor(ROOT.kGray+1)
#line2.SetLineColor(ROOT.kGray+1)
#line3.SetLineColor(ROOT.kGray+1)
#line4.SetLineColor(ROOT.kGray+1)
#line5.SetLineColor(ROOT.kGray+1)

box8 = ROOT.TBox(1150., 9, 1350., 10.3)
box8.SetFillColor(ROOT.kOrange+1)
box7 = ROOT.TBox(1150., 11, 1350., 12.3)
box7.SetFillColor(ROOT.kOrange+1)

#----------add Text----------
ytitle = hmax05.GetNbinsX() +0.5
ylegend = ytitle -1.25

txt = ROOT.TLatex(0, ytitle-0.2, "Summary of CMS SUSY Simplified Models Results*")
txt1 = ROOT.TLatex(1350., 26.25, "CMS Preliminary")
txt.SetTextSize(0.035)
txt1.SetTextSize(0.04)
txt2 = ROOT.TLatex(20., ylegend+0.2, "m(mother)-m(LSP)=200 GeV")
txt2.SetTextSize(0.025)
txt3 = ROOT.TLatex(850, ylegend+0.2, "m(LSP)=0 GeV")
txt3.SetTextSize(0.025)
txt5 = ROOT.TLatex(820, ytitle-0.2, "ICHEP 2016")
txt5.SetTextSize(0.035)
txt6 = ROOT.TLatex(1170, 11.2, "#sqrt{s} = 7 TeV")
txt6.SetTextSize(0.026)
txt7 = ROOT.TLatex(1170, 9.2, "#sqrt{s} = 8 TeV")
txt7.SetTextSize(0.026)
txt8 = ROOT.TLatex(1350, 23.75, "#splitline{For decays with intermediate mass,}{m_{intermediate} = x#upointm_{mother}-(1-x)#upointm_{lsp}}")
txt8.SetTextSize(0.02)
txt8.SetTextFont(42)
txt8.SetTextColor(ROOT.kGray+1)

txtfoot = ROOT.TLatex(-200., -3.5, "#splitline{*Observed limits, theory uncertainties not included}{Only a selection of available mass limits}" )
txtfoot2 = ROOT.TLatex(-200., -5.5, "Probe *up to* the quoted mass limit" )
txtfoot.SetTextSize(0.021)
txtfoot.SetTextColor(ROOT.kGray+1)
txtfoot.SetTextFont(42)
txtfoot2.SetTextSize(0.021)
txtfoot2.SetTextColor(ROOT.kGray+1)
txtfoot2.SetTextFont(42)

#txtv0 = ROOT.TLatex(-220., 7, "RPV")
#txtv1 = ROOT.TLatex(-220., y1+0.5, "gluino production")
#txtv2 = ROOT.TLatex(-220., y2-1, "squark")
#txtv3 = ROOT.TLatex(-220., y3+1.5, "stop")
#txtv4 = ROOT.TLatex(-220., y4-0., "sbottom")
#txtv5 = ROOT.TLatex(-220., y5+1., "EWK gauginos")
#txtv6 = ROOT.TLatex(-220., y0-1, "slepton")

txtv = []

#--------Set Labels------------

container = []

last = hmax05.GetNbinsX()
#bars['empty']['decay'] = 'Gluino mediated'
#bars['empty5']['decay'] = 'Squark Searched'
#bars['empty4']['decay'] = 'EWK Gauginos and Sleptons'
#bars['empty3']['decay'] = ''
#bars['empty4']['decay'] = ''
print last
print 'HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH'
for bi in range(1, last+1):
        print 'BI', bi
	topo = hmax05.GetXaxis().GetBinLabel(bi)
#	topo = sorthistos[bi-1]
	lab = bars[topo]['decay']
#	bi = hmax05.FindBin(topo)
	print bi, topo, lab
	hmax1.GetXaxis().SetBinLabel(bi, lab)
	hmax2.GetXaxis().SetBinLabel(bi, lab)
	hmax3.GetXaxis().SetBinLabel(bi, lab)
	hmax4.GetXaxis().SetBinLabel(bi, lab)
	hmax5.GetXaxis().SetBinLabel(bi, lab)
	hmax6.GetXaxis().SetBinLabel(bi, lab)
	hdelta1.GetXaxis().SetBinLabel(bi, lab)
	hdelta2.GetXaxis().SetBinLabel(bi, lab)
	hdelta3.GetXaxis().SetBinLabel(bi, lab)
	hdelta4.GetXaxis().SetBinLabel(bi, lab)
	hdelta5.GetXaxis().SetBinLabel(bi, lab)
	hdelta6.GetXaxis().SetBinLabel(bi, lab)
	hmax05.GetXaxis().SetBinLabel(bi, lab)
	hmax058.GetXaxis().SetBinLabel(bi, lab)
	hdelta05.GetXaxis().SetBinLabel(bi, lab)
	hdelta058.GetXaxis().SetBinLabel(bi, lab)
	hchange7.GetXaxis().SetBinLabel(bi, lab)
	hchange8.GetXaxis().SetBinLabel(bi, lab)
	container.append([hmax1,hmax2,hmax3,hmax4,hmax5,hmax6,hmax05,hmax058,hdelta1,hdelta2,hdelta3,hdelta4,hdelta5,hdelta6,hdelta05,hdelta058,hchange7,hchange8])

#----------draw plot-----------
#newColor1 = ROOT.kOrange+7
#newColor2 = ROOT.kOrange+1
newColor2 = ROOT.kAzure-3
newColor1= ROOT.kAzure+8

#ROOT.kAzure-3
#ROOT.kAzure+8
c.cd()
hmax05.SetFillColor(newColor1)
hmax05.SetBarWidth(0.9)
hmax05.SetBarOffset(0.05)
hmax05.SetTickLength(0)
hmax05.GetYaxis().SetTickLength(0.015)
hmax05.SetYTitle("Mass scales [GeV]")
hmax05.GetYaxis().SetTitleFont(42)
hmax05.SetTitleSize(0.025, "Y")
hmax05.GetYaxis().SetTitleOffset(1.1)
hmax05.SetLabelSize(0.03, "X")
hmax05.SetLabelSize(0.025, "Y")
hmax05.SetLabelFont(42, "X")
hmax05.SetLabelFont(42, "Y")
#hmax05.GetYaxis().CenterTitle() 
hmax05.SetMaximum(1000.)
hmax05.Draw('HBAR0')
hmax1.SetFillColor(newColor1)
hmax1.SetBarWidth(0.33)
hmax1.SetBarOffset(0.065)
hmax1.Draw('HBAR0SAME')
hmax2.SetFillColor(newColor1)
hmax2.SetBarWidth(0.33)
hmax2.SetBarOffset(0.35)
hmax2.Draw('HBAR0SAME')
hmax3.SetFillColor(newColor1)
hmax3.SetBarWidth(0.33)
hmax3.SetBarOffset(0.635)
hmax3.Draw('HBAR0SAME')

hdelta05.SetFillColor(ROOT.kOrange+1)
hdelta05.SetBarWidth(0.9)
hdelta05.SetBarOffset(0.05)
hdelta05.Draw('HBAR0SAME')
hdelta1.SetFillColor(ROOT.kOrange+1)
hdelta1.SetBarWidth(0.33)
hdelta1.SetBarOffset(0.065)
hdelta1.Draw('HBAR0SAME')
hdelta2.SetFillColor(ROOT.kOrange+1)
hdelta2.SetBarWidth(0.33)
hdelta2.SetBarOffset(0.35)
hdelta2.Draw('HBAR0SAME')
hdelta3.SetFillColor(ROOT.kOrange+1)
hdelta3.SetBarWidth(0.33)
hdelta3.SetBarOffset(0.635)
hdelta3.Draw('HBAR0SAME')

#same for 8 TeV, but different colors
#hmax058.SetFillColor(ROOT.kOrange+7)
hmax058.SetFillColor(ROOT.kOrange+7)
hmax058.SetBarWidth(0.9)
hmax058.SetBarOffset(0.05)
hmax058.Draw('HBAR0SAME')
hmax4.SetFillColor(ROOT.kOrange+7)
hmax4.SetBarWidth(0.33)
hmax4.SetBarOffset(0.065)
hmax4.Draw('HBAR0SAME')
hmax5.SetFillColor(ROOT.kOrange+7)
hmax5.SetBarWidth(0.33)
hmax5.SetBarOffset(0.35)
hmax5.Draw('HBAR0SAME')
hmax6.SetFillColor(ROOT.kOrange+7)
hmax6.SetBarWidth(0.33)
hmax6.SetBarOffset(0.635)
hmax6.Draw('HBAR0SAME')

hdelta058.SetFillColor(ROOT.kOrange+1)
hdelta058.SetBarWidth(0.9)
hdelta058.SetBarOffset(0.05)
hdelta058.Draw('HBAR0SAME')
hdelta4.SetFillColor(ROOT.kOrange+1)
hdelta4.SetBarWidth(0.33)
hdelta4.SetBarOffset(0.065)
hdelta4.Draw('HBAR0SAME')
hdelta5.SetFillColor(ROOT.kOrange+1)
hdelta5.SetBarWidth(0.33)
hdelta5.SetBarOffset(0.35)
hdelta5.Draw('HBAR0SAME')
hdelta6.SetFillColor(ROOT.kOrange+1)
hdelta6.SetBarWidth(0.33)
hdelta6.SetBarOffset(0.635)
hdelta6.Draw('HBAR0SAME')

hchange7.SetFillColor(newColor1)
hchange7.SetBarWidth(0.9)
hchange7.SetBarOffset(0.05)
#hchange7.Draw('HBAR0SAME')
hchange8.SetFillColor(ROOT.kWhite)
hchange8.SetBarWidth(0.9)
hchange8.SetBarOffset(0.05)
hchange8.Draw('HBAR0SAME')

#hmin05.SetFillColor(ROOT.kWhite)
#hmin05.SetBarWidth(0.9)
#hmin05.SetBarOffset(0.05)
#hmin05.Draw('HBAR0SAME')
#hmin1.SetFillColor(ROOT.kWhite)
#hmin1.SetBarWidth(0.33)
#hmin1.SetBarOffset(0.065)
#hmin1.Draw('HBAR0SAME')
#hmin2.SetFillColor(ROOT.kWhite)
#hmin2.SetBarWidth(0.33)
#hmin2.SetBarOffset(0.35)
#hmin2.Draw('HBAR0SAME')
#hmin3.SetFillColor(ROOT.kWhite)
#hmin3.SetBarWidth(0.33)
#hmin3.SetBarOffset(0.635)
#hmin3.Draw('HBAR0SAME')


#--------add text and legend----------------
#container = []
#xpos = [[500., 550., 600.], [500., 450., 400.],[500., 450., 400.], [500., 400., 500.], [500., 550., 500.], [350., 400., 350.]]
#z = 0
for j in text:
	sus = ''
	l = ''
	for m in text[j]['PAS']:
		sus += "%s " %m
	for n in text[j]['lumi']:
#		if float(n) < 12.:
		l += "%s " %n
#	print l
#	if l:
	sus = sus + "L=%s/fb" %l
#	print sus
#	print int(text[j]['ypos'])
	t = ROOT.TLatex(20., float(text[j]['ypos'])+0.4, sus)
	t.SetTextSize(0.0250)
	container.append(t)
	t.Draw('SAME')
	x = []
	for k in bars[j]['max']:
		x.append(k)
	x.sort()
	x1 = []
	for z in range(0,len(x)):
		x1.append(x[z].replace('0', '0.', 1))
#	print x1 
	if len(x) == 3:
		if j == 'T2tt8':
			x = ['left-handed top', 'unpolarized top', 'right-handed top']
			t2 = ROOT.TLatex(bars[j]['max']['L'][0]+10,float(text[j]['ypos'])+0.7, "%s" %x[0])
			t3 = ROOT.TLatex(bars[j]['max']['050'][0]+10,float(text[j]['ypos'])+0.37, "%s" %x[1])
			t4 = ROOT.TLatex(bars[j]['max']['R'][0]+10,float(text[j]['ypos'])-0.1, "%s" %x[2])
			t2.SetTextSize(0.008)
			t3.SetTextSize(0.008)
			t4.SetTextSize(0.008)
			container.append(t2)
			container.append(t3)
			container.append(t4)
			t2.Draw('SAME')
			t3.Draw('SAME')
			t4.Draw('SAME')
		elif j =='T6bbWW8':
			t2 = ROOT.TLatex(bars[j]['max'][x[0]][0]+10,float(text[j]['ypos'])+0.65, "x = %s" %x1[0])
			t3 = ROOT.TLatex(bars[j]['max'][x[1]][0]+10,float(text[j]['ypos'])+0.4, "x = %s" %x1[1])
			t4 = ROOT.TLatex(bars[j]['max'][x[2]][0]+10,float(text[j]['ypos']), "x = %s" %x1[2])
			t2.SetTextSize(0.008)
			t3.SetTextSize(0.008)
			t4.SetTextSize(0.008)
			container.append(t2)
			container.append(t3)
			container.append(t4)
			t2.Draw('SAME')
			t3.Draw('SAME')
			t4.Draw('SAME')
		    
		else:
			t2 = ROOT.TLatex(bars[j]['max'][x[0]][0]+10,float(text[j]['ypos'])+0.7, "x = %s" %x1[0])
			t3 = ROOT.TLatex(bars[j]['max'][x[1]][0]+10,float(text[j]['ypos'])+0.4, "x = %s" %x1[1])
			t4 = ROOT.TLatex(bars[j]['max'][x[2]][0]+10,float(text[j]['ypos'])+0.1, "x = %s" %x1[2])
			t2.SetTextSize(0.02)
			t3.SetTextSize(0.02)
			t4.SetTextSize(0.02)
			container.append(t2)
			container.append(t3)
			container.append(t4)
			t2.Draw('SAME')
			t3.Draw('SAME')
			t4.Draw('SAME')
	if len(x) == 2:
		t2 = ROOT.TLatex(bars[j]['max'][x[0]][0]+10,float(text[j]['ypos'])+0.65, "x = %s" %x1[0])
		t3 = ROOT.TLatex(bars[j]['max'][x[1]][0]+10,float(text[j]['ypos'])+0.35, "x = %s" %x1[1])
#		t4 = ROOT.TLatex(bars[j]['max'][x[1]][0]+10,float(text[j]['ypos'])+0.07, "x = %s" %x1[1])
		t2.SetTextSize(0.01)
		t3.SetTextSize(0.01)
#		t4.SetTextSize(0.01)
		container.append(t2)
		container.append(t3)
#		container.append(t4)
		t2.Draw('SAME')
		t3.Draw('SAME')
#		t4.Draw('SAME')

for tv in txtv:
	tv.SetTextSize(0.015)
	tv.SetTextFont(42)
	tv.SetTextAngle(90.)
	tv.SetTextColor(ROOT.kGray+1)
	container.append(tv)
	tv.Draw('SAME')

#box8.Draw('SAME')
#box7.Draw('SAME')
		
txt.Draw('SAME')
txt1.Draw('SAME')
txt2.Draw('SAME')
txt3.Draw('SAME')
#txt4.Draw('SAME')
txt5.Draw('SAME')
txt6.Draw('SAME')
txt7.Draw('SAME')
txt8.Draw('SAME')
txtfoot.Draw('SAME')
txtfoot2.Draw('SAME')

#line0.Draw('SAME')
#line1.Draw('SAME')
#line2.Draw('SAME')
#line3.Draw('SAME')
#line4.Draw('SAME')
#line5.Draw('SAME')

"""
legend = ROOT.TLegend(0.95, 0.26, 0.8, 0.16)
legend.SetFillStyle(0)
legend.SetBorderSize(0)
l1 = ROOT.TLine()
l1.SetLineColor(ROOT.kBlue)
l1.SetLineWidth(5)
#legend.AddEntry(l1, "#sqrt{s} = 7 TeV, L = %s - %s fb^{-1}" %(lu7s, lu7),"L")
legend.AddEntry(l1, "#sqrt{s} = 7 TeV","L")
l2 = ROOT.TLine()
l2.SetLineColor(ROOT.kMagenta+1)
l2.SetLineWidth(5)
#legend.AddEntry(l2, "#sqrt{s} = 8 TeV, L #leq %s fb^{-1}" %lu8,"L")
legend.AddEntry(l2, "#sqrt{s} = 8 TeV","L")

legend.Draw()
"""
filename='ICHEP_2016'
c.Print("ICHEP_2016.pdf")
import commands
#values for crop margins: " left x-value, top y-value, right x-value, bottom y-value " 
#commands.getoutput('pdfcrop %s.pdf --margins "300 100 -200 290"' % filename)
#commands.getoutput('convert %s-crop.pdf %s-crop.png' % (filename, filename))
#c.Print("barplot.png")
#os.system ( "convert barplot.pdf barplot.png" )
#os.system ( "convert barplot.png barplot.pdf" )
#raw_input()

#print bars
