#Input options
import sys
import argparse

parser = argparse.ArgumentParser(description = "Input options")
parser.add_argument("--file", dest = "file",  help = "Input file", type = str, default = "")
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "Give .sh file as input"
   print makeLine()
   assert len(sys.argv) > 1

filename = args.file

outfile = open(filename.replace(".sh", "_nohup.sh"), "w")

with open(filename, "r") as infile:
   for line in infile:
      x = "nohup krenew -t -K 10 -- bash -c '%s' & disown\n"%line[:-1]
      outfile.write(x)

   infile.close()
