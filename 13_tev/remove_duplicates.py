from ROOT import *
import optparse
import sys
from array import array
from samples import *

parser = optparse.OptionParser()

parser.add_option('-i', '--input_filename', help='input_filename', dest='infname', default='my_input_file.root')
parser.add_option('-o', '--output_filename', help='output_filename', dest='outfname', default='my_output_file.root')
parser.add_option('-x', '--xs', help='the cross section in pb', dest='xs', default='0.0')
parser.add_option('-s', '--sample', help='name of the sample', dest='sample')

(options,args) = parser.parse_args()

xs = float(options.xs)

fin=TFile(options.infname,"read")
fout=TFile(options.outfname,"recreate")
fin.cd()

sample=options.sample

#slha_header_vector = std.vector('string')()
#initrwgt_header_vector = std.vector('string')()

#fin.GetObject("slha_header",slha_header_vector)

#fin.GetObject("initrwgt_header",initrwgt_header_vector)

#fout.WriteObject(slha_header_vector,"slha_header")
#fout.WriteObject(initrwgt_header_vector,"initrwgt_header")

told = fin.Get("events")

fout.cd()

tnew = told.CloneTree(0)

#sys.stdout = open("/dev/null")
#sys.stderr = open("/dev/null")
    
run_lumi_evt_nums = {}

for entry in range(0,told.GetEntries()):

    if entry % 100000 == 0:
        print entry

    told.GetEntry(i)

    #sys.stdout("/dev/null")

    #search_string = "run=="+str(told.run)+"&&lumi=="+str(told.lumi)+"&&event=="+str(told.event)

    #scan_return=tnew.Draw("run:lumi:event",search_string,"goff")

    if (told.run,told.lumi,told.event) not in run_lumi_evt_nums:
        tnew.Fill()
        run_lumi_evt_nums[(told.run,told.lumi,told.event)] = True
