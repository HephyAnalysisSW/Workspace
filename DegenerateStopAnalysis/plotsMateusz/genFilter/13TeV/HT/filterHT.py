#filter.py - Filter over a range of generator cut values. To be used with turnon.py.

print "\nExecuting filter.py script..."
   
import turnonHT #imports turnon.py script

genMETcut_low = 0 #input("Enter lower generated MET cut boundary to scan: ")
genMETcut_up = 110 #input("Enter upper generated MET cut boundary to scan: ")
genMETcut_step = 5 #input("Enter generated MET cut steps: ")

genHTcut_low = 140 #input("Enter lower generated HT Jet pT cut boundary to scan: ")
genHTcut_up = 200 #input("Enter upper generated HT Jet pT cut boundary to scan: ")
genHTcut_step = 5 #input("Enter generated HT Jet pT cut steps: ")
   
while genMETcut_low <= genMETcut_up:
   counter = genHTcut_low
   while counter <= genHTcut_up:
      turnonHT.main(genMETcut_low, counter)
      counter += genHTcut_step
   genMETcut_low += genMETcut_step
