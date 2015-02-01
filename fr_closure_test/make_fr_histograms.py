#if running on a dtmit machine, you need to move to root version 5.34.20 or higher
#source /afs/cern.ch/sw/lcg/external/gcc/4.7.2/x86_64-slc5-gcc47-opt/setup.sh
#source /afs/cern.ch/sw/lcg/app/releases/ROOT/5.34.20/x86_64-slc5-gcc47-opt/root/bin/thisroot.sh

import optparse

parser = optparse.OptionParser()

parser.add_option('-i', '--input_filename', help='filename of the input ntuple', dest='finname', default='my_file.root')
parser.add_option('-o', '--output_filename', help='filename of the output ntuple', dest='foutname', default='my_file.root')

(options,args) = parser.parse_args()

import sys

#otherwise, root will parse the command line options, see here http://root.cern.ch/phpBB3/viewtopic.php?f=14&t=18637
sys.argv = []

from ROOT import *

from array import array

gStyle.SetOptStat(0)

#gROOT.ProcessLine('#include "/afs/cern.ch/work/a/anlevin/crab/CMSSW_7_2_0/src/ntuple_maker/ntuple_maker/interface/enum_definition.h"')

finname=options.finname
foutname=options.foutname

fin=TFile(finname)
fout=TFile(foutname,"recreate")

gROOT.cd()

muon_tree=fin.Get("loose_muons")

muon_ptbins=array('d', [10,15,20,25,30,35])
muon_etabins=array('d', [0,1,1.479,2.0,2.5])

loose_muon_th2d=TH2F("loose muons","loose muons",4,muon_etabins,5,muon_ptbins)
tight_muon_th2d=TH2F("tight muons","tight muons",4,muon_etabins,5,muon_ptbins)

for entry in range(muon_tree.GetEntries()):
    muon_tree.GetEntry(entry)

    loose_muon_th2d.Fill(abs(muon_tree.muon_4mom.Eta()),muon_tree.muon_4mom.Pt(),muon_tree.xsWeight)

    if muon_tree.pass_full_muon_id:
        tight_muon_th2d.Fill(abs(muon_tree.muon_4mom.Eta()),muon_tree.muon_4mom.Pt(),muon_tree.xsWeight)
    
tight_muon_th2d.Divide(loose_muon_th2d)

electron_tree=fin.Get("loose_electrons")

electron_ptbins=array('d', [10,15,20,25,30,35])
electron_etabins=array('d', [0,1,1.479,2.0,2.5])

loose_electron_th2d=TH2F("loose electrons","loose electrons",4,electron_etabins,5,electron_ptbins)
tight_electron_th2d=TH2F("tight electrons","tight electrons",4,electron_etabins,5,electron_ptbins)

for entry in range(electron_tree.GetEntries()):
    electron_tree.GetEntry(entry)

    loose_electron_th2d.Fill(electron_tree.electron_4mom.Eta(),electron_tree.electron_4mom.Pt(),electron_tree.xsWeight)

    if electron_tree.pass_full_electron_id:
        tight_electron_th2d.Fill(electron_tree.electron_4mom.Eta(),electron_tree.electron_4mom.Pt(),electron_tree.xsWeight)
    
tight_electron_th2d.Divide(loose_electron_th2d)

tight_muon_th2d.Draw("lego")

fout.cd()
tight_muon_th2d.Clone("muon_frs").Write()
tight_electron_th2d.Clone("electron_frs").Write()

raw_input()

