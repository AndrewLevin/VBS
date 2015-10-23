#if running on a dtmit machine, you need to move to root version 5.34.20 or higher
#source /afs/cern.ch/sw/lcg/external/gcc/4.7.2/x86_64-slc5-gcc47-opt/setup.sh
#source /afs/cern.ch/sw/lcg/app/releases/ROOT/5.34.20/x86_64-slc5-gcc47-opt/root/bin/thisroot.sh

import optparse

parser = optparse.OptionParser()

parser.add_option('-i', '--input_filename', help='filename of the input ntuple', dest='finname', default='my_file.root')
parser.add_option('--output_dir', help='directory to put the output plots in', dest='output_dir', default='/afs/cern.ch/user/a/anlevin/www/tmp/')
parser.add_option('--hist_name', help='name of the histogram', dest='hist_name', default='muon_frs')

(options,args) = parser.parse_args()

import sys

#otherwise, root will parse the command line options, see here http://root.cern.ch/phpBB3/viewtopic.php?f=14&t=18637
sys.argv = []

from ROOT import *

from array import array

gStyle.SetOptStat(0)

#gROOT.ProcessLine('#include "/afs/cern.ch/work/a/anlevin/crab/CMSSW_7_2_0/src/ntuple_maker/ntuple_maker/interface/enum_definition.h"')

finname=options.finname
fin=TFile(finname)

gROOT.cd()

th2f=fin.Get(options.hist_name)

#muon_ptbins=array('d', [10,15,20,25,30,35])

binning_y=[]

for ybin in range(1,th2f.GetYaxis().GetNbins()+1):
    binning_y.append(th2f.GetYaxis().GetBinLowEdge(ybin))

binning_y.append(th2f.GetYaxis().GetBinUpEdge(th2f.GetNbinsX()+1))    

print "binning_y:"
print binning_y    

binning_x=[]

for xbin in range(1,th2f.GetXaxis().GetNbins()+1):
    binning_x.append(th2f.GetXaxis().GetBinLowEdge(xbin))

binning_x.append(th2f.GetXaxis().GetBinUpEdge(th2f.GetNbinsX()+1))    


print "binning_x:"
print binning_x    

binning_x_array=array('d',binning_x)
binning_y_array=array('d',binning_y)

for xbin in range(1,th2f.GetNbinsX()+1):
    c=TCanvas("ptbin"+str(xbin))
    
    th1f=TH1F("","",len(binning_y_array)-1,binning_y_array)
    th1f.SetLineWidth(3)
    th1f.SetLineColor(kBlack)
    th1f.GetXaxis().SetTitle("p_{T} (GeV)")
    th1f.GetXaxis().CenterTitle()
    for ybin in range(0,th2f.GetNbinsY()+2):
        th1f.SetBinContent(ybin,th2f.GetBinContent(xbin,ybin))
        th1f.SetBinError(ybin,th2f.GetBinError(xbin,ybin))

    th1f.SetMinimum(0)    
    th1f.Draw()

    c.SaveAs(options.output_dir + options.hist_name + "_etabin"+str(xbin)+".png")

    #c.SaveAs("/afs/cern.ch/user/a/anlevin/www/tmp/delete_this_etabin"+str(xbin)+".png")

muon_etabins=array('d', [0,1,1.479,2.0,2.5])

for ybin in range(1,th2f.GetNbinsY()+1):
    c=TCanvas("etabin"+str(ybin))
    th1f=TH1F("","",len(binning_x_array)-1,binning_x_array)
    th1f.SetLineWidth(3)
    th1f.SetLineColor(kBlack)
    th1f.GetXaxis().CenterTitle()
    th1f.GetXaxis().SetTitle("\eta")
    for xbin in range(0,th2f.GetNbinsX()+2):
        th1f.SetBinContent(xbin,th2f.GetBinContent(xbin,ybin))
        th1f.SetBinError(xbin,th2f.GetBinError(xbin,ybin))

    th1f.SetMinimum(0)    
    th1f.Draw()

    c.SaveAs(options.output_dir + options.hist_name + "_ptbin"+str(ybin)+".png")
