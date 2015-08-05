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

def make_new_tree(told):

    #prevents root from wring a lot of stuff into memory
    #tmpfile=TFile("weight_events_tmpfile.root","recreate")
    
    fout.cd()
    
    #gROOT.cd() #in order to prevent the original tree from being added to the output file
    tnew=told.CloneTree()

    w=array('f',[0])

    if sample not in samples.keys():
        print "sample name not found, exiting"
        sys.exit(0)

    sample_id=array('L',[samples[sample]]) #see page 302 of "Python in a nutshell"

    br=tnew.Branch('xsWeight',w,'xsWeight/F')

    #br2=tnew.Branch('sample',samples[sample],'sample/i')
    br2=tnew.Branch('sample',sample_id,'sample/i')

    n_events_run_over_hist=fin.Get("n_events_run_over")

    for entry in range(tnew.GetEntries()):
        tnew.GetEntry(entry)

        w[0] = 1000*xs/n_events_run_over_hist.GetEntries()

        br.Fill()
        br2.Fill()

    fout.cd()

    tnew.Write()

    #overwrite this file, which can be very large, with a new file, so that it becomes small
    #tmpfile=TFile("weight_events_tmpfile.root","recreate")    

#will weight every tree in the file
#if the file has directories, this will descend one level into the directory structure to look for the trees

#get the maximum cycle number

maxcycle=0

for key in fin.GetListOfKeys():
    if key.GetName() == "slha_header" or key.GetName() == "initrwgt_header":
        continue
    object=key.ReadObj()
    if object.GetName() == "events":
        if key.GetCycle() > maxcycle:
            maxcycle = key.GetCycle()

print "maxcycle = "+str(maxcycle)

for key in fin.GetListOfKeys():
    if key.GetName() == "slha_header" or key.GetName() == "initrwgt_header":
        continue
    object=key.ReadObj()
    if object.GetName() == "events":
        if key.GetCycle() != maxcycle:
            continue
        make_new_tree(object)

slha_header_vector = std.vector('string')()
initrwgt_header_vector = std.vector('string')()

fin.GetObject("slha_header",slha_header_vector)

fin.GetObject("initrwgt_header",initrwgt_header_vector)

fout.WriteObject(slha_header_vector,"slha_header")
fout.WriteObject(initrwgt_header_vector,"initrwgt_header")
