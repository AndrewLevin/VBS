#if running on a dtmit machine, you need to move to root version 5.34.20 or higher
#source /afs/cern.ch/sw/lcg/external/gcc/4.7.2/x86_64-slc5-gcc47-opt/setup.sh
#source /afs/cern.ch/sw/lcg/app/releases/ROOT/5.34.20/x86_64-slc5-gcc47-opt/root/bin/thisroot.sh

import optparse

parser = optparse.OptionParser()

parser.add_option('--frfilename', help='name of the file with the fake rate histograms', dest='frfname', default='my_file.root')
parser.add_option('-f', '--filename', help='filename of the input ntuple', dest='fname', default='my_file.root')
parser.add_option('-v', '--variable', help='which variable to plot', dest='variable', default='mjj')
parser.add_option('-c', '--channel', help='which channel to use', dest='channel', default='all')
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

fr_file=TFile(options.frfname)
muon_fr_hist=fr_file.Get("muon_frs")
electron_fr_hist=fr_file.Get("electron_frs")

def muonfakerate(eta,pt,syst):
    myeta  = min(abs(eta),2.4999)
    mypt   = min(pt,34.999)

    etabin = muon_fr_hist.GetXaxis().FindBin(myeta)
    ptbin = muon_fr_hist.GetYaxis().FindBin(mypt)

    prob = muon_fr_hist.GetBinContent(ptbin,etabin)

    if syst == "up":
        prob+=muon_fr_hist.GetBinError(ptbin,etabin)
    elif syst == "down":
        prob-=muon_fr_hist.GetBinError(ptbin,etabin)
    else:
        if syst != "nominal":
            sys.exit(0)

    return prob/(1-prob)

def electronfakerate(eta,pt,syst):
    myeta  = min(abs(eta),2.4999)
    mypt   = min(pt,34.999)

    etabin = electron_fr_hist.GetXaxis().FindBin(myeta)
    ptbin = electron_fr_hist.GetYaxis().FindBin(mypt)

    prob = electron_fr_hist.GetBinContent(ptbin,etabin)

    if syst == "up":
        prob+=electron_fr_hist.GetBinError(ptbin,etabin)
    elif syst == "down":
        prob-=electron_fr_hist.GetBinError(ptbin,etabin)
    else:
        if syst != "nominal":
            sys.exit(0)

    return prob/(1-prob)

def fillHistograms(t,hist,use_fake_rate_method,fake_rate_syst):
    
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

        if use_fake_rate_method:
            if (not lep1passfullid) and lep2passfullid:
                w=t.xsWeight*float(options.lumi)
                if abs(t.lep1id) == 13:
                    w = w * muonfakerate(t.lep1.Eta(), t.lep1.Pt(),fake_rate_syst)
                elif abs(t.lep1id) == 11:
                    w = w * electronfakerate(t.lep1.Eta(), t.lep1.Pt(),fake_rate_syst)
                else:
                    print "unknown lepton flavor"
                    sys.exit(0)
            elif lep1passfullid and (not lep2passfullid):
                w=t.xsWeight*float(options.lumi)
                if abs(t.lep2id) == 13:
                    w = w * muonfakerate(t.lep2.Eta(), t.lep2.Pt(),fake_rate_syst)
                elif abs(t.lep2id) == 11:
                    w = w * electronfakerate(t.lep2.Eta(), t.lep2.Pt(),fake_rate_syst)
                else:
                    print "unknown lepton flavor"
                    sys.exit(0)
            else:
                continue
            
        else:            
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
        else:
            assert(0)
        
fname=options.fname

c=TCanvas("c", "c",0,0,600,500)
c.Range(0,0,1,1)

f=TFile(fname)

tree=f.Get("events")

if options.variable == "mjj":
    binning=array('f',[500,700,1100,1600,2000])
    hist = TH1F('mjj', 'mjj',4, binning )
    #hist = TH1F('mjj', 'mjj', 35, 0., 2000 )
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
else:
    assert(0)

#error = sqrt(sum weight^2)
hist.Sumw2()

hist.GetXaxis().CenterTitle()

hist.SetLineWidth(3)

hist.GetXaxis().SetTitleSize(0.045000000149)
#hist.GetXaxis().SetTitleOffset(1.70)

#hist.GetYaxis().SetLabelSize(0.07)
#hist.GetYaxis().SetTitleSize(0.08)
#hist.GetYaxis().SetTitleOffset(0.76)

hist.SetTitle("")
hist.GetXaxis().SetTitle("m_{jj} (GeV)")

hist_fr=hist.Clone()
hist_fr_up=hist.Clone()
hist_fr_down=hist.Clone()



#hist_fr.GetXaxis().SetTitleSize(0.00)
#hist_fr.GetYaxis().SetLabelSize(0.07)
#hist_fr.GetYaxis().SetTitleSize(0.08)
#hist_fr.GetYaxis().SetTitleOffset(0.76)

fillHistograms(tree,hist,false,"")
fillHistograms(tree,hist_fr,true,"nominal")
fillHistograms(tree,hist_fr_up,true,"up")
#fillHistograms(tree,hist_fr_down,true,"down")

for bin in range(0,hist_fr.GetNbinsX()+2):
    hist_fr.SetBinError(bin,sqrt(hist_fr.GetBinError(bin)*hist_fr.GetBinError(bin)+ abs(hist_fr_up.GetBinContent(bin) - hist_fr.GetBinContent(bin))*abs(hist_fr_up.GetBinContent(bin) - hist_fr.GetBinContent(bin))))

#change the bin errors for the nominal histogram

#hist_signal.Scale(1/hist_signal.Integral())
#hist_background.Scale(1/hist_background.Integral())


leg=TLegend(.60,.65,.85,.85)
leg.SetLineWidth(3)
leg.AddEntry(hist,"correct","l")
leg.AddEntry(hist_fr,"fake rate","l")
leg.SetFillColor(0)
leg.SetLineWidth(3)

#leg.SetBorderSize(1.1)


hist.SetLineColor(kRed)
hist_fr.SetLineColor(kBlue)

hist.SetMinimum(0)

hist_fr.Draw()
hist.Draw("SAME")

leg.Draw("SAME")

c.Update()

c.SaveAs(options.output_dir+options.variable+".png")

