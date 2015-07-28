#filter.py - Filter over a range of generator cut values

print "\nExecuting filter.py script..."
   
import turnon

gMETcut_low = input("Enter lower generated MET cut boundary to scan: ")
gMETcut_up = input("Enter upper generated MET cut boundary to scan: ")
gMETcut_step = input("Enter generated MET cut steps: ")

gISRcut_low = input("Enter lower generated ISR Jet pT cut boundary to scan: ")
gISRcut_up = input("Enter upper generated ISR Jet pT cut boundary to scan: ")
gISRcut_step = input("Enter generated ISR Jet pT cut steps: ")
   
while gMETcut_low <= gMETcut_up:
   counter = gISRcut_low
   while counter <= gISRcut_up:
      turnon.main(gMETcut_low, counter)
      counter += gISRcut_step
   gMETcut_low += gMETcut_step
