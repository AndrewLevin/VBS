#if running on a dtmit machine, you need to move to root version 5.34.20 or higher
#source /afs/cern.ch/sw/lcg/external/gcc/4.7.2/x86_64-slc5-gcc47-opt/setup.sh
#source /afs/cern.ch/sw/lcg/app/releases/ROOT/5.34.20/x86_64-slc5-gcc47-opt/root/bin/thisroot.sh

import json

import optparse

parser = optparse.OptionParser()

parser.add_option('--muon_data_input_filename', help='filename of the input muon ntuple', dest='finmuondataname')
parser.add_option('--muon_mc_input_filename', help='filename of the input muon ntuple', dest='finmuonmcname')
parser.add_option('--electron_data_input_filename', help='filename of the input electron ntuple', dest='finelectrondataname')
parser.add_option('--electron_mc_input_filename', help='filename of the input mc electron ntuple', dest='finelectronmcname')
parser.add_option('-o', '--output_filename', help='filename of the output ntuple', dest='foutname', default='my_file.root')
parser.add_option('--mod', help='only use every mod events', dest='mod', default=1)

(options,args) = parser.parse_args()

#assert(options.finmuondataname != None)
#assert(options.finelectrondataname != None)

import sys

#otherwise, root will parse the command line options, see here http://root.cern.ch/phpBB3/viewtopic.php?f=14&t=18637
sys.argv = []

from ROOT import *

from array import array

gStyle.SetOptStat(0)

gROOT.ProcessLine('#include "/afs/cern.ch/work/a/anlevin/cmssw/CMSSW_8_0_26_patch1/src/ntuple_maker/ntuple_maker/interface/fr_enum_definition.h"')

foutname=options.foutname

fout=TFile(foutname,"recreate")

f_json=open("/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON.txt")
#f_json=open("delete_this_JSON.txt")

good_run_lumis=json.loads(f_json.read())

def pass_json(run,lumi):

    if str(run) not in good_run_lumis.keys():
        return False

    for lumi_pair in good_run_lumis[str(run)]:
        if lumi < lumi_pair[1] and lumi > lumi_pair[0]:
            return True

    return False    

if options.finmuondataname != None:

    finmuonname=options.finmuondataname

    finmuon=TFile(finmuonname)

    muon_tree=finmuon.Get("loose_muons")

    muon_data_mt_hist=TH1F("muon_data_met","muon_data_met",100,0,100)

    for entry in range(muon_tree.GetEntries()):
        muon_tree.GetEntry(entry)

        if entry % 100000 == 0:
            print entry

        if entry % int(options.mod) != 0:
            continue

        #if not pass_json(muon_tree.run,muon_tree.lumi):
        #    continue

        #if muon_tree.metpt < 30:
        #    continue

        if muon_tree.muon_4mom.pt() < 40:
            continue

        mt = sqrt(2*muon_tree.muon_4mom.pt()*muon_tree.metpt*(1 - cos(muon_tree.metphi - muon_tree.muon_4mom.phi())) )

        #if mt > 30:
        #    continue

        if not (muon_tree.flags & LepTightSelectionV1):
            continue

        if abs(muon_tree.muon_4mom.Eta()) > 2.5:
            continue

        muon_data_mt_hist.Fill(muon_tree.metpt)

if options.finmuonmcname != None:

    #mu17_lumi = 182.88/1000.0
    #mu17_lumi = 100.00/1000.0

    #mu17_lumi = 36*0.007
    mu17_lumi = 35.9
    
    finmuonmc = TFile(options.finmuonmcname)
    muon_mc_tree=finmuonmc.Get("loose_muons")

    muon_mc_mt_hist=TH1F("muon_mc_met","muon_mc_met",100,0,100)

    for entry in range(muon_mc_tree.GetEntries()):
        muon_mc_tree.GetEntry(entry)

        if entry % 100000 == 0:
            print entry

        if entry % int(options.mod) != 0:
            continue

        #if muon_mc_tree.metpt < 30:
        #    continue

        if muon_mc_tree.muon_4mom.pt() < 40:
            continue

        mt = sqrt(2*muon_mc_tree.muon_4mom.pt()*muon_mc_tree.metpt*(1 - cos(muon_mc_tree.metphi - muon_mc_tree.muon_4mom.phi())) )

        #if mt > 30:
        #    continue

        if not (muon_mc_tree.flags & LepTightSelectionV1):
            continue

        if abs(muon_mc_tree.muon_4mom.Eta()) > 2.5:
            continue

        weight = muon_mc_tree.xsWeight*mu17_lumi

        if muon_mc_tree.gen_weight < 0:
            weight = -weight

        muon_mc_mt_hist.Fill(muon_mc_tree.metpt,weight)

if options.finelectrondataname != None:

    finelectronname=options.finelectrondataname

    finelectron=TFile(finelectronname)

    electron_tree=finelectron.Get("loose_electrons")

    electron_data_mt_hist=TH1F("electron_data_met","electron_data_met",100,0,100)

    for entry in range(electron_tree.GetEntries()):
        electron_tree.GetEntry(entry)

    #if entry >= options.n_events:
    #    break

        if entry % 100000 == 0:
            print entry

        if entry % int(options.mod) != 0:
            continue

        if not (electron_tree.flags & PassTriggerV1):
            continue

        #if not pass_json(electron_tree.run,electron_tree.lumi):
        #    continue

        #if electron_tree.metpt < 30:
        #    continue

        if electron_tree.electron_4mom.pt() < 40:
            continue

        #mt = sqrt(2*electron_tree.electron_4mom.pt()*electron_tree.metpt*(1 - cos(electron_tree.metphi - electron_tree.electron_4mom.phi())) )

        #if mt > 30:
        #    continue

        if not (electron_tree.flags & LepTightSelectionV5):
           continue

        if abs(electron_tree.electron_4mom.Eta()) > 2.5:
            continue

        electron_data_mt_hist.Fill(electron_tree.metpt)

if options.finelectronmcname != None:

    ele12_lumi = 35.9
    #ele12_lumi = 35.9 * 0.0005
    #ele12_lumi = 5/1000.0
    #ele33_lumi = 4.98/1000.0
    
    finelectronmc = TFile(options.finelectronmcname)
    electron_mc_tree=finelectronmc.Get("loose_electrons")

    electron_mc_mt_hist=TH1F("electron_mc_met","electron_mc_met",100,0,100)

    for entry in range(electron_mc_tree.GetEntries()):
        electron_mc_tree.GetEntry(entry)

        if entry % 100000 == 0:
            print entry

        if entry % int(options.mod) != 0:
            continue

        #if electron_mc_tree.metpt < 30:
        #    continue

        if not (electron_mc_tree.flags & PassTriggerV1):
            continue

        if electron_mc_tree.electron_4mom.pt() < 40:
            continue

        #mt = sqrt(2*electron_tree.electron_4mom.pt()*electron_tree.metpt*(1 - cos(electron_tree.metphi - electron_tree.electron_4mom.phi())) )

        #if mt > 30:
        #    continue

        if not (electron_mc_tree.flags & LepTightSelectionV5):
            continue

        if abs(electron_mc_tree.electron_4mom.Eta()) > 2.5:
            continue

        #weight = electron_mc_tree.xsWeight*ele33_lumi
        weight = electron_mc_tree.xsWeight*ele12_lumi

        if electron_mc_tree.gen_weight < 0:
            weight = -weight

        electron_mc_mt_hist.Fill(electron_mc_tree.metpt,weight)

fout.cd()

if options.finelectronmcname != None:
    electron_mc_mt_hist.Write()

if options.finelectrondataname != None:
    electron_data_mt_hist.Write()    


if options.finmuonmcname != None:
    muon_mc_mt_hist.Write()

if options.finmuondataname != None:
    muon_data_mt_hist.Write()    
