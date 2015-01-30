#!/bin/sh 
python draw_pieCharts.py --lepton=muon --stb=250,350 --btb=0,0
python draw_pieCharts.py --lepton=muon --stb=350,450 --btb=0,0
python draw_pieCharts.py --lepton=muon --stb=450,-1 --btb=0,0
python draw_pieCharts.py --lepton=muon --stb=250,350 --btb=1,1
python draw_pieCharts.py --lepton=muon --stb=350,450 --btb=1,1
python draw_pieCharts.py --lepton=muon --stb=450,-1 --btb=1,1
python draw_pieCharts.py --lepton=muon --stb=250,350 --btb=2,2
python draw_pieCharts.py --lepton=muon --stb=350,450 --btb=2,2
python draw_pieCharts.py --lepton=muon --stb=450,-1 --btb=2,2
python draw_pieCharts.py --lepton=muon --stb=250,350 --btb=3,-1
python draw_pieCharts.py --lepton=muon --stb=350,450 --btb=3,-1
python draw_pieCharts.py --lepton=muon --stb=450,-1 --btb=3,-1
#stb = [(250, 350), (350, 450), (450,-1)]
#nbjetreg = [(0,0), (1,1), (2,2),(3,3),(4,-1), (3,-1), (2,-1), (1,-1)]
