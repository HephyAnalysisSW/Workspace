#!/bin/sh
python convert.py $1 stop200lsp170g100FastSim  &
python convert.py $1 stop300lsp240g150FastSim &
python convert.py $1 stop300lsp270g175FastSim &
python convert.py $1 stop300lsp270FastSim &
python convert.py $1 stop300lsp270g200FastSim &
python convert.py $1 stop200lsp170g100FullSim  &
python convert.py $1 stop300lsp240g150FullSim &
python convert.py $1 stop300lsp270g175FullSim &
python convert.py $1 stop300lsp270FullSim &
python convert.py $1 stop300lsp270g200FullSim &

