#if running on a dtmit machine, you need to move to root version 5.34.20 or higher
#source /afs/cern.ch/sw/lcg/external/gcc/4.7.2/x86_64-slc5-gcc47-opt/setup.sh
#source /afs/cern.ch/sw/lcg/app/releases/ROOT/5.34.20/x86_64-slc5-gcc47-opt/root/bin/thisroot.sh

import optparse

parser = optparse.OptionParser()

parser.add_option('-s', '--signal_filename', help='filename of the signal input ntuple', dest='sig_fname', default='my_signal_file.root')
parser.add_option('-b', '--background_filename', help='filename of the background input ntuple', dest='back_fname', default='my_background_file.root')
parser.add_option('-v', '--variable', help='which variable to plot', dest='variable', default='mjj')
parser.add_option('-c', '--channel', help='which channel to use', dest='channel', default='all')
parser.add_option('-d', '--datacard', help='the name of the file to write the datacard to', dest='datacard', default='datacard.txt')
parser.add_option('-l', '--lumi', help='the amount of integrated luminosity to weight the events with', dest='lumi', default='19.4')
parser.add_option('-o', '--output_dir', help='the directory to write the output plots', dest='output_dir', default='/afs/cern.ch/user/a/anlevin/www/tmp/')

(options,args) = parser.parse_args()

import sys

#otherwise, root will parse the command line options, see here http://root.cern.ch/phpBB3/viewtopic.php?f=14&t=18637
sys.argv = []

from ROOT import *

from array import array

gStyle.SetOptStat(0)

gROOT.ProcessLine('#include "/afs/cern.ch/work/a/anlevin/cmssw/CMSSW_7_2_0/src/ntuple_maker/ntuple_maker/interface/enum_definition.h"')

def fillHistograms(t,hist):
    print "t.GetEntries() = " + str(t.GetEntries())
    for entry in range(t.GetEntries()):
        t.GetEntry(entry)

        if entry % 100000 == 0:
            print "entry = " + str(entry)
            

        if (abs(t.lep1id) == 13 and abs(t.lep2id) == 11) or (abs(t.lep1id) == 11 and abs(t.lep1id) == 13) :
            channel="em"
        elif abs(t.lep1id) == 13 and abs(t.lep2id) == 13:
            channel = "mm"
        elif abs(t.lep1id) == 11 and abs(t.lep2id) == 11:
            channel = "ee"
        else:
            assert(0)

        if options.channel != channel and options.channel!="all":
            continue

        if t.lep1.pt() < 20:
            continue

        if t.lep2.pt() < 20:
            continue

        if t.lep1q != t.lep2q:
            continue

        if (t.jet1+t.jet2).M() < 500:
            continue
        if abs(t.jet1.Eta() - t.jet2.Eta()) < 2.5:
            continue

        lep1passfullid = bool(t.cuts & Lep1FullSelectionV1)
        lep2passfullid = bool(t.cuts & Lep2FullSelectionV1)

        if not lep1passfullid:
            continue

        if not lep2passfullid:
            continue

        w=t.xsWeight*float(options.lumi)

        if options.variable == "mjj":
            #put the overflow in the last bin
            if (t.jet1+t.jet2).M() > hist.GetBinLowEdge(hist.GetNbinsX()):
                hist.Fill(hist.GetBinCenter(hist.GetNbinsX()),w)
            else:              
                hist.Fill((t.jet1+t.jet2).M(),w)
        elif options.variable == "mll":    
            hist.Fill((t.lep1+t.lep2).M(),w)
        elif options.variable == "met":    
            hist.Fill(t.metpt,w)
        elif options.variable == "detajj":
            hist.Fill(abs(t.jet1.Eta() - t.jet2.Eta()),w)
        elif options.variable == "jet1btag":
            hist.Fill(t.jet1btag,w)    
        elif options.variable == "jet2btag":            
            hist.Fill(t.jet2btag,w)
        elif options.variable == "nvtx":            
            hist.Fill(t.nvtx,w)
        elif options.variable == "lep1pt":            
            hist.Fill(t.lep1.pt(),w)
        elif options.variable == "lep2pt":            
            hist.Fill(t.lep2.pt(),w)                
        else:
            assert(0)
        
signal_fname=options.sig_fname
background_fname=options.back_fname

c=TCanvas("c", "c",0,0,600,500)
c.Range(0,0,1,1)

f_signal=TFile(signal_fname)
f_background=TFile(background_fname)

tree_signal=f_signal.Get("events")
tree_background=f_background.Get("events")

if options.variable == "mjj":
    binning=array('f',[500,700,1100,1600,2000])
    hist = TH1F('mjj', 'mjj',4, binning )
    #hist = TH1F('mjj', 'mjj', 35, 0., 200 )
elif options.variable == "mll":    
    hist = TH1F('mll', 'mll', 35, 0., 500)
elif options.variable == "met":
    hist = TH1F('met', 'met', 35, 0., 200 )
elif options.variable == "detajj":
    hist = TH1F('detajj', 'detajj', 35, 0., 5 )
elif options.variable == "jet1btag":
    hist = TH1F('jet1btag', 'jet1btag', 35, -1., 1 )
elif options.variable == "jet2btag":
    hist = TH1F('jet2btag', 'jet2btag', 35, -1., 1 )
elif options.variable == "nvtx":
    hist = TH1F('nvtx', 'nvtx', 35, 0., 60 )
elif options.variable == "lep1pt":
    hist = TH1F('lep1pt', 'lep1pt', 35, 0., 100 )
elif options.variable == "lep2pt":
    hist = TH1F('lep2pt', 'lep2pt', 35, 0., 100 )        
else:
    assert(0)

#error = sqrt(sum weight^2)
hist.Sumw2()

hist.SetTitle("")
hist.SetMaximum(6)


hist.GetXaxis().CenterTitle()
hist.GetXaxis().SetTitleSize(0.045000000149)
hist.GetXaxis().SetTitle("m_{jj} (GeV)")

hist_signal=hist.Clone()
hist_background=hist.Clone()

#hist_signal.GetXaxis().SetTitleSize(0.00)
#hist_signal.GetYaxis().SetLabelSize(0.07)
#hist_signal.GetYaxis().SetTitleSize(0.08)
#hist_signal.GetYaxis().SetTitleOffset(0.76)
#hist_signal.GetXaxis().SetLabelSize(0.0)

#hist_background.GetXaxis().SetTitleSize(0.00)
#hist_background.GetYaxis().SetLabelSize(0.07)
#hist_background.GetYaxis().SetTitleSize(0.08)
#hist_background.GetYaxis().SetTitleOffset(0.76)
#hist_background.GetXaxis().SetLabelSize(0.0)

fillHistograms(tree_signal,hist_signal)
fillHistograms(tree_background,hist_background)

#hist_signal.Scale(1/hist_signal.Integral())
#hist_background.Scale(1/hist_background.Integral())

hist_signal.SetLineWidth(3)
hist_background.SetLineWidth(3)

hist_signal.SetLineColor(kRed)
hist_background.SetLineColor(kBlue)

hist_signal.SetMinimum(0)
hist_background.SetMinimum(0)



hist_signal.Draw()
print hist_background.GetEntries()
hist_background.Draw("SAME")

leg=TLegend(.60,.65,.85,.85)
leg.AddEntry(hist_signal,"signal","l")
leg.AddEntry(hist_background,"background","l")
leg.SetFillColor(0)
leg.Draw("SAME")

#c.GetYaxis().SetMaximum(6)

c.Update()

c.SaveAs(options.output_dir+options.variable+".png")

dcard = open(options.datacard,'w')

print >> dcard, "imax 1 number of channels"
print >> dcard, "jmax * number of background"
print >> dcard, "kmax * number of nuisance parameters"
print >> dcard, "Observation 0"
print >> dcard, "bin bin1 bin1"
print >> dcard, "process WWjj ttbar"
print >> dcard, "process 0 1"
print >> dcard, "rate "+str(hist_signal.Integral())+" 0.1"
print >> dcard, "lumi_8tev lnN 2.4 2.4"

raw_input()

