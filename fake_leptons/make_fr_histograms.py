#if running on a dtmit machine, you need to move to root version 5.34.20 or higher
#source /afs/cern.ch/sw/lcg/external/gcc/4.7.2/x86_64-slc5-gcc47-opt/setup.sh
#source /afs/cern.ch/sw/lcg/app/releases/ROOT/5.34.20/x86_64-slc5-gcc47-opt/root/bin/thisroot.sh

import json

import optparse

parser = optparse.OptionParser()

parser.add_option('--muon_input_filename', help='filename of the input muon ntuple', dest='finmuonname', default='my_file.root')
parser.add_option('--electron_input_filename', help='filename of the input electron ntuple', dest='finelectronname', default='my_file.root')
parser.add_option('-o', '--output_filename', help='filename of the output ntuple', dest='foutname', default='my_file.root')
parser.add_option('--n_events', help='number of events to run over', dest='n_events', default=100000)

(options,args) = parser.parse_args()

import sys

#otherwise, root will parse the command line options, see here http://root.cern.ch/phpBB3/viewtopic.php?f=14&t=18637
sys.argv = []

from ROOT import *

from array import array

gStyle.SetOptStat(0)

gROOT.ProcessLine('#include "/afs/cern.ch/work/a/anlevin/cmssw/CMSSW_7_4_15/src/ntuple_maker/ntuple_maker/interface/fr_enum_definition.h"')

finelectronname=options.finelectronname
finmuonname=options.finmuonname
foutname=options.foutname

finmuon=TFile(finmuonname)
finelectron=TFile(finelectronname)
fout=TFile(foutname,"recreate")

gROOT.cd()

muon_tree=finmuon.Get("loose_muons")

muon_ptbins=array('d', [10,15,20,25,30,35])
muon_etabins=array('d', [0,1,1.479,2.0,2.5])

loose_muon_th2d=TH2F("loose muons","loose muons",4,muon_etabins,5,muon_ptbins)
tight_muon_th2d=TH2F("tight muons","tight muons",4,muon_etabins,5,muon_ptbins)

loose_muon_th2d.Sumw2()
tight_muon_th2d.Sumw2()

def pass_json(run,lumi):

    f_json=open("/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-258750_13TeV_PromptReco_Collisions15_25ns_JSON.txt")
    good_run_lumis=json.loads(f_json.read())

    if str(run) not in good_run_lumis.keys():
        return False

    for lumi_pair in good_run_lumis[str(run)]:
        if lumi < lumi_pair[1] and lumi > lumi_pair[0]:
            return True

    return False    

for entry in range(muon_tree.GetEntries()):
    muon_tree.GetEntry(entry)

    if entry >= options.n_events:
        break

    if entry % 100000 == 0:
        print entry
        

    #if muon_tree.ptjetaway < 70:
    #   continue

    #if muon_tree.nearestparton_4mom.pt() > 20:
    #   continue

    #if muon_tree.nearestparton_pdgid != 5:
    #    continue    

    if not pass_json(muon_tree.run,muon_tree.lumi):
        continue

    if not (muon_tree.flags & LepLooseSelectionV1):
        continue

    if abs(muon_tree.muon_4mom.Eta()) > 2.4:
        continue

    weight = 1

    #use the xsWeight if it exists, otherwise all events have weight 1
    if type(muon_tree.GetListOfBranches().FindObject("xsWeight")) == TBranch:
        weight = muon_tree.xsWeight

    if muon_tree.muon_4mom.Pt() > loose_muon_th2d.GetYaxis().GetBinUpEdge(loose_muon_th2d.GetYaxis().GetNbins()):
        loose_muon_th2d.Fill(abs(muon_tree.muon_4mom.Eta()),loose_muon_th2d.GetYaxis().GetBinCenter(loose_muon_th2d.GetYaxis().GetNbins()),weight)
    else:    
        loose_muon_th2d.Fill(abs(muon_tree.muon_4mom.Eta()),muon_tree.muon_4mom.Pt(),weight)
    #loose_muon_th2d.Fill(abs(muon_tree.muon_4mom.Eta()),muon_tree.muon_4mom.Pt())

    if (muon_tree.flags & LepTightSelectionV2):
        if muon_tree.muon_4mom.Pt() > tight_muon_th2d.GetYaxis().GetBinUpEdge(tight_muon_th2d.GetYaxis().GetNbins()):
            tight_muon_th2d.Fill(abs(muon_tree.muon_4mom.Eta()),tight_muon_th2d.GetYaxis().GetBinCenter(tight_muon_th2d.GetYaxis().GetNbins()),weight)
        else:
            tight_muon_th2d.Fill(abs(muon_tree.muon_4mom.Eta()),muon_tree.muon_4mom.Pt(),weight)
    #if muon_tree.pass_full_muon_id:
    #    tight_muon_th2d.Fill(abs(muon_tree.muon_4mom.Eta()),muon_tree.muon_4mom.Pt())        

#tight_muon_th2d.Print("all")
#loose_muon_th2d.Print("all")
    
tight_muon_th2d.Divide(loose_muon_th2d)

electron_tree=finelectron.Get("loose_electrons")

electron_ptbins=array('d', [10,15,20,25,30,35])
electron_etabins=array('d', [0,1,1.479,2.0,2.5])

loose_electron_th2d=TH2F("loose electrons","loose electrons",4,electron_etabins,5,electron_ptbins)
tight_electron_th2d=TH2F("tight electrons","tight electrons",4,electron_etabins,5,electron_ptbins)

loose_electron_th2d.Sumw2()
tight_electron_th2d.Sumw2()

for entry in range(electron_tree.GetEntries()):
    electron_tree.GetEntry(entry)

    if entry >= options.n_events:
        break

    if not pass_json(electron_tree.run,electron_tree.lumi):
        continue

    #if electron_tree.ptjetaway < 70:
    #    continue

    #if electron_tree.nearestparton_4mom.pt() > 20:
    #   continue    

    #if electron_tree.nearestparton_pdgid != 5:
    #    continue    

    if not (electron_tree.flags & LepLooseSelectionV1):
        continue

    if abs(electron_tree.electron_4mom.Eta()) > 2.5:
        continue

    weight = 1

    #use the xsWeight if it exists, otherwise all events have weight 1
    if type(electron_tree.GetListOfBranches().FindObject("xsWeight")) == TBranch:
        weight = electron_tree.xsWeight

    if electron_tree.electron_4mom.Pt() > loose_electron_th2d.GetYaxis().GetBinUpEdge(loose_electron_th2d.GetYaxis().GetNbins()):
        loose_electron_th2d.Fill(abs(electron_tree.electron_4mom.Eta()),loose_electron_th2d.GetYaxis().GetBinCenter(loose_electron_th2d.GetYaxis().GetNbins()),weight)
    else:
        loose_electron_th2d.Fill(abs(electron_tree.electron_4mom.Eta()),electron_tree.electron_4mom.Pt(),weight)
#    loose_electron_th2d.Fill(electron_tree.electron_4mom.Eta(),electron_tree.electron_4mom.Pt())

    if (electron_tree.flags & LepTightSelectionV1):
        if electron_tree.electron_4mom.Pt() > tight_electron_th2d.GetYaxis().GetBinUpEdge(tight_electron_th2d.GetYaxis().GetNbins()):
            tight_electron_th2d.Fill(abs(electron_tree.electron_4mom.Eta()),tight_electron_th2d.GetYaxis().GetBinCenter(tight_electron_th2d.GetYaxis().GetNbins()),weight)
        else:    
            tight_electron_th2d.Fill(abs(electron_tree.electron_4mom.Eta()),electron_tree.electron_4mom.Pt(),weight)
#    if electron_tree.pass_full_electron_id:
#        tight_electron_th2d.Fill(electron_tree.electron_4mom.Eta(),electron_tree.electron_4mom.Pt())  
    
tight_electron_th2d.Divide(loose_electron_th2d)

tight_electron_th2d.Draw("lego")

fout.cd()
tight_muon_th2d.Clone("muon_frs").Write()
tight_electron_th2d.Clone("electron_frs").Write()

raw_input()

