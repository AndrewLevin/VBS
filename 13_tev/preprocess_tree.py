#removes redundant lhe header information
#puts the lhe header information into a vector
#puts everything in the top-level directory

from ROOT import *
import optparse
import sys
from array import array
from samples import *

parser = optparse.OptionParser()

parser.add_option('-i', '--input_filename', help='input_filename', dest='infname', default='my_input_file.root')
parser.add_option('-o', '--output_filename', help='output_filename', dest='outfname', default='my_output_file.root')

(options,args) = parser.parse_args()

fin=TFile(options.infname,"read")
fout=TFile(options.outfname,"recreate")
fin.cd()



#if the tree does not exist this is false
if type(fin.Get("demo/slha_header")) == TTree:
    slha_header_tree=fin.Get("demo/slha_header")

    fout.cd()

    slha_header = std.vector('string')()

    for entry in range(slha_header_tree.GetEntries()):
        slha_header_tree.GetEntry(entry)
        
        #the headers will be merged together, so only include the first one
        if slha_header_tree.slha_header_line == "END_SLHA_HEADER\n":
            break

        slha_header.push_back(slha_header_tree.slha_header_line)

    fout.WriteObject(slha_header,"slha_header")


#if the tree does not exist this is false
if type(fin.Get("demo/initrwgt_header")) == TTree:
    initrwgt_header_tree=fin.Get("demo/initrwgt_header")

    initrwgt_header = std.vector('string')()

    for entry in range(initrwgt_header_tree.GetEntries()):
        initrwgt_header_tree.GetEntry(entry)

        #the headers will be merged together, so only include the first one
        if initrwgt_header_tree.initrwgt_header_line == "END_INITRWGT_HEADER\n":
            break


        initrwgt_header.push_back(initrwgt_header_tree.initrwgt_header_line)

    fout.WriteObject(initrwgt_header,"initrwgt_header")

fout.cd()

maxcycle_events = 0
maxcycle_muon_tree = 0
maxcycle_electron_tree = 0

for key in fin.GetListOfKeys():
    object=key.ReadObj()
    if type(object) == TDirectoryFile:
        for key in object.GetListOfKeys():
            obj=key.ReadObj()
            if obj.GetName() == "events":
                if key.GetCycle() > maxcycle_events:
                    maxcycle_events = key.GetCycle()
            if obj.GetName() == "loose_muons":
                if key.GetCycle() > maxcycle_muon_tree:
                    maxcycle_muon_tree = key.GetCycle()
            if obj.GetName() == "loose_electrons":
                if key.GetCycle() > maxcycle_electron_tree:
                    maxcycle_electron_tree = key.GetCycle()                                        

for key in fin.GetListOfKeys():
    object=key.ReadObj()
    if type(object) == TDirectoryFile:
        for key in object.GetListOfKeys():
            obj=key.ReadObj()
            if obj.GetName() == "events":
                if type(obj)==TTree:
                    if key.GetCycle() != maxcycle_events:
                        continue
                    fout.WriteObject(obj.CloneTree(),obj.GetName())
            if obj.GetName() == "loose_muons":
                if type(obj)==TTree:
                    if key.GetCycle() != maxcycle_muon_tree:
                        continue
                    fout.WriteObject(obj.CloneTree(),obj.GetName())
            if obj.GetName() == "loose_electrons":
                if type(obj)==TTree:
                    if key.GetCycle() != maxcycle_electron_tree:
                        continue
                    fout.WriteObject(obj.CloneTree(),obj.GetName())                    
            if obj.GetName() == "n_events_run_over":
                fout.WriteObject(obj.Clone(),obj.GetName())
            if obj.GetName() == "n_weighted_events_run_over":
                fout.WriteObject(obj.Clone(),obj.GetName())                
            #print told.GetName()

