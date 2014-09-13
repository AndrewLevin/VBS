from ROOT import *
import optparse
import sys
from array import array

parser = optparse.OptionParser()

parser.add_option('-i', '--input_filename', help='input_filename', dest='infname', default='my_input_file.root')
parser.add_option('-o', '--output_filename', help='output_filename', dest='outfname', default='my_output_file.root')
parser.add_option('-x', '--xs', help='the cross section in pb', dest='xs', default='0.0')

(options,args) = parser.parse_args()

xs = float(options.xs)

fin=TFile(options.infname,"read")
fout=TFile(options.outfname,"recreate")
told=fin.Get("demo/events")
tnew=told.CloneTree()

w=array('f',[0])
br=tnew.Branch('xsWeight',w,'xsWeight/F')

n_events_run_over_hist=fin.Get("demo/n_events_run_over")

for entry in range(tnew.GetEntries()):
    tnew.GetEntry(entry)
    w[0] = 1000*xs/n_events_run_over_hist.GetEntries()
    br.Fill()

fout.cd()
tnew.Write()
