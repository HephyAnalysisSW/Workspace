#filter.py - Filter over a range of generator cut values. To be used with turnon.py.

print "\nExecuting filter.py script..."
   
import turnon #imports turnon.py script

genMETcut_low = 135 #input("Enter lower generated MET cut boundary to scan: ")
genMETcut_up = 135 #input("Enter upper generated MET cut boundary to scan: ")
genMETcut_step = 5 #input("Enter generated MET cut steps: ")

genISRcut_low = 80 #input("Enter lower generated ISR Jet pT cut boundary to scan: ")
genISRcut_up = 80 #input("Enter upper generated ISR Jet pT cut boundary to scan: ")
genISRcut_step = 5 #input("Enter generated ISR Jet pT cut steps: ")
   
while genMETcut_low <= genMETcut_up:
   counter = genISRcut_low
   while counter <= genISRcut_up:
      turnon.main(genMETcut_low, counter)
      counter += genISRcut_step
   genMETcut_low += genMETcut_step
