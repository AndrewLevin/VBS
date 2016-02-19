#removes redundant lhe header information
#puts the lhe header information into a vector
#puts everything in the top-level directory

from ROOT import *
import optparse
import sys
from array import array
from samples import *
import datetime


parser = optparse.OptionParser()

parser.add_option('-i', '--input_filename', help='input_filename', dest='infname', default='my_input_file.root')

(options,args) = parser.parse_args()

fin=TFile(options.infname,"read")

t=fin.Get("events")

run_lumi_evt_nums = {}

for entry in range(0,t.GetEntries()):
    t.GetEntry(entry)

    if entry % 100000 == 0:
        print entry
        #print datetime.datetime.now()

    if (t.run,t.lumi,t.event) in run_lumi_evt_nums:
        print "found duplicate event:"
        print (t.run,t.lumi,t.event)
        sys.exit(0)
        

    run_lumi_evt_nums[(t.run,t.lumi,t.event)] = True

#print run_lumi_event_list
