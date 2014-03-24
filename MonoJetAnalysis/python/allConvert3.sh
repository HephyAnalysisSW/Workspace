#!/bin/sh
python convert.py --samples=stop200lsp170g100FastSim  --chmode=$1 &
python convert.py --samples=stop300lsp240g150FastSim  --chmode=$1 &
python convert.py --samples=stop300lsp270g175FastSim  --chmode=$1 &
python convert.py --samples=stop300lsp270FastSim      --chmode=$1 &
python convert.py --samples=stop300lsp270g200FastSim  --chmode=$1 &
python convert.py --samples=stop200lsp170g100FullSim  --chmode=$1 &
python convert.py --samples=stop300lsp240g150FullSim  --chmode=$1 &
python convert.py --samples=stop300lsp270g175FullSim  --chmode=$1 &
python convert.py --samples=stop300lsp270FullSim      --chmode=$1 &
python convert.py --samples=stop300lsp270g200FullSim  --chmode=$1 &

