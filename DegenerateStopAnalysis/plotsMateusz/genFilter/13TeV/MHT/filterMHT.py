#filterMHT.py - Filter over a range of generator cut values. To be used with turnon.py.

print "\nExecuting filter.py script..."
   
import turnonMHT #imports turnon.py script

genHTcut_low = 170 #input("Enter lower generated HT cut boundary to scan: ")
genHTcut_up = 190 #input("Enter upper generated HT cut boundary to scan: ")
genHTcut_step = 5 #input("Enter generated HT cut steps: ")

genMHTcut_low = 0 #input("Enter lower generated HT Jet pT cut boundary to scan: ")
genMHTcut_up = 35 #input("Enter upper generated HT Jet pT cut boundary to scan: ")
genMHTcut_step = 5 #input("Enter generated HT Jet pT cut steps: ")
   
while genHTcut_low <= genHTcut_up:
   counter = genMHTcut_low
   while counter <= genMHTcut_up:
      turnonMHT.main(genHTcut_low, counter)
      counter += genMHTcut_step
   genHTcut_low += genHTcut_step
