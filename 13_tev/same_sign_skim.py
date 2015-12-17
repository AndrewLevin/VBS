import optparse

parser.add_option('-i', '--input_filename', help='input_filename', dest='infname', default='my_input_file.root')
parser.add_option('-o', '--output_filename', help='output_filename', dest='outfname', default='my_output_file.root')

(options,args) = parser.parse_args()

from ROOT import *

infile=TFile(options.infname,"read")
outfile=TFile(options.outfname,"recreate")



intree=infile.Get("events")

outfile.cd()

outtree = intree.CloneTree(0)

for i in range(intree.GetEntries()):
    intree.GetEntry(i)

    if i % 100000 == 0:
        print i

    if intree.lep1q == intree.lep2q:
        outtree.Fill()


outtree.Write()    
