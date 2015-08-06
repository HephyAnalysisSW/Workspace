#filter.py - Filter over a range of generator cut values

print "\nExecuting filter.py script..."
   
import turnon

gMETcut_low = 120 #input("Enter lower generated MET cut boundary to scan: ")
gMETcut_up = 160 #input("Enter upper generated MET cut boundary to scan: ")
gMETcut_step = 5 #input("Enter generated MET cut steps: ")

gISRcut_low = 90 #input("Enter lower generated ISR Jet pT cut boundary to scan: ")
gISRcut_up = 100 #input("Enter upper generated ISR Jet pT cut boundary to scan: ")
gISRcut_step = 5 #input("Enter generated ISR Jet pT cut steps: ")
   
while gMETcut_low <= gMETcut_up:
   counter = gISRcut_low
   while counter <= gISRcut_up:
      turnon.main(gMETcut_low, counter)
      counter += gISRcut_step
   gMETcut_low += gMETcut_step
