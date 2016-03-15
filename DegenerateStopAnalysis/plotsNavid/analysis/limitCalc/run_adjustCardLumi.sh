
#card_dir="../cutbased/cards/mass_scan_isr/isrrw*.txt"
card_dir="../cutbased/cards/13TeV/HT/IsrWeight_10000pbm1/*.txt"

for f in `ls $card_dir`
    do 

    python adjustCardLumi.py $f 2300 ../cutbased/cards/13TeV/HT/IsrWeight_2300pbm1/

    done

