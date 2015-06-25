#if running on a dtmit machine, you need to move to root version 5.34.20 or higher
#source /afs/cern.ch/sw/lcg/external/gcc/4.7.2/x86_64-slc5-gcc47-opt/setup.sh
#source /afs/cern.ch/sw/lcg/app/releases/ROOT/5.34.20/x86_64-slc5-gcc47-opt/root/bin/thisroot.sh

import parse_reweight_info

import optparse

parser = optparse.OptionParser()

parser.add_option('-s', '--signal_filename', help='filename of the signal input ntuple', dest='sig_fname', default='my_signal_file.root')
parser.add_option('-b', '--background_filename', help='filename of the background input ntuple', dest='back_fname', default='my_background_file.root')
parser.add_option('-v', '--variable', help='which variable to plot', dest='variable', default='mjj')
parser.add_option('-c', '--channel', help='which channel to use', dest='channel', default='all')
parser.add_option('-d', '--datacard', help='the name of the file to write the datacard to', dest='datacard')
parser.add_option('-l', '--lumi', help='the amount of integrated luminosity to weight the events with', dest='lumi', default='19.4')
parser.add_option('-o', '--output_dir', help='the directory to write the output plots', dest='output_dir', default='/afs/cern.ch/user/a/anlevin/www/tmp/')
parser.add_option('--dim8_output_fname', help='file where the dim8c scaling histograms will be written', dest='dim8_output_fname')
parser.add_option('--dim8_param', help='dimension 8 parameter e.g. FS0', dest='dim8_param')
parser.add_option('--dim8_lhe_file', help='dimension 8 LHE file which contains the reweighting information', dest='dim8_lhe_file')
parser.add_option('--mode', help='which mode to run this script in', dest='mode')
parser.add_option('--dim8_datacard_base', help='the base of the filename to write the dim8 datacards to', dest='dim8_datacard_base')
parser.add_option('--which_lhe_weight', help='use one of the lhe weights to weight the events', dest='which_lhe_weight')
parser.add_option('--gm_datacard_base', help='the base of the filename to write the gm datacards to', dest='gm_datacard_base')

(options,args) = parser.parse_args()

import sys

#otherwise, root will parse the command line options, see here http://root.cern.ch/phpBB3/viewtopic.php?f=14&t=18637
sys.argv = []

from ROOT import *

from array import array

#gStyle.SetOptStat(0)

gROOT.ProcessLine('#include "/afs/cern.ch/work/a/anlevin/cmssw/CMSSW_7_2_0/src/ntuple_maker/ntuple_maker/interface/enum_definition.h"')

def passSelection(t):

    p=True

    if t.lep1.pt() < 20:
        p=False
        
    if t.lep2.pt() < 20:
        p=False

    if t.lep1q != t.lep2q:
        p=False

    if (t.jet1+t.jet2).M() < 500:
        p=False
    if abs(t.jet1.Eta() - t.jet2.Eta()) < 2.5:
        p=False

    lep1passfullid = bool(t.flags & Lep1TightSelectionV1)
    lep2passfullid = bool(t.flags & Lep2TightSelectionV1)

    if not lep1passfullid:
        p=False

    if not lep2passfullid:
        p=False

    return p

#put the overflow in the last bin
#if (t.jet1+t.jet2).M() > hist.GetBinLowEdge(hist.GetNbinsX()):
#    hist.Fill(hist.GetBinCenter(hist.GetNbinsX()),w)
#else:
#    print (t.jet1+t.jet2).M()
#    hist.Fill((t.jet1+t.jet2).M(),w)

        


def getVariable(t):
    if options.variable == "mjj":
        return (t.jet1+t.jet2).M()
    elif options.variable == "mll":
        return (t.lep1+t.lep2).M()
    elif options.variable == "met":
        return t.metpt
    elif options.variable == "detajj":
        return abs(t.jet1.Eta() - t.jet2.Eta())
    elif options.variable == "jet1btag":
        return t.jet1btag
    elif options.variable == "jet2btag":
        return t.jet2btag
    elif options.variable == "nvtx":
        return t.nvtx
    elif options.variable == "lep1pt":
        return t.lep1.pt()
    elif options.variable == "lep2pt":
        return t.lep2.pt()
    else:
        assert(0)    

def fillHistogram(t,hist,use_lhe_weight = False):
    print "t.GetEntries() = " + str(t.GetEntries())
    for entry in range(t.GetEntries()):
        t.GetEntry(entry)

        if entry % 100000 == 0:
            print "entry = " + str(entry)

        if (abs(t.lep1id) == 13 and abs(t.lep2id) == 11) or (abs(t.lep1id) == 11 and abs(t.lep2id) == 13) :
            channel="em"
        elif abs(t.lep1id) == 13 and abs(t.lep2id) == 13:
            channel = "mm"
        elif abs(t.lep1id) == 11 and abs(t.lep2id) == 11:
            channel = "ee"
        else:
            assert(0)
            
        if options.channel != channel and options.channel!="all":
            continue

        if not passSelection(t):
            continue

        w=t.xsWeight*float(options.lumi)

        var=getVariable(t)

        if options.mode == "non-sm" and use_lhe_weight == True:
            if var > hist.GetBinLowEdge(hist.GetNbinsX()):
                hist.Fill(hist.GetBinCenter(hist.GetNbinsX()),w*t.lhe_weights[int(options.which_lhe_weight)]/t.lhe_weight_orig)
            else:
                hist.Fill(var,w*t.lhe_weights[int(options.which_lhe_weight)]/t.lhe_weight_orig)
        else:
            if var > hist.GetBinLowEdge(hist.GetNbinsX()):
                hist.Fill(hist.GetBinCenter(hist.GetNbinsX()),w)
            else:
                hist.Fill(var,w)

def fillHistogramsWithReweight(t,histos):
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

        if not passSelection(t):
            continue

        w=t.xsWeight*float(options.lumi)

        var=getVariable(t)

        for i in range(0,len(oneD_grid_points)):
            if var > histos[i].GetBinLowEdge(histos[i].GetNbinsX()):
                histos[i].Fill(histos[i].GetBinCenter(histos[i].GetNbinsX()),w*t.lhe_weights[lhe_weight_index[i]]/t.lhe_weight_orig)
            else:    
                histos[i].Fill(var,w*t.lhe_weights[lhe_weight_index[i]]/t.lhe_weight_orig)

def fillHistogramWithPDFWeights(t,histos):
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

        if not passSelection(t):
            continue

        w=t.xsWeight*float(options.lumi)

        var=getVariable(t)

        for i in range(0,100):
            if var > histos[i].GetBinLowEdge(histos[i].GetNbinsX()):
                histos[i].Fill(histos[i].GetBinCenter(histos[i].GetNbinsX()),w*t.pdf_weights[i]/t.qcd_pdf_weight_orig)
            else:    
                histos[i].Fill(var,w*t.pdf_weights[i]/t.qcd_pdf_weight_orig)

def fillHistogramWithQCDWeights(t,histo,qcd_up_histo,qcd_down_histo):
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

        if not passSelection(t):
            continue

        w=t.xsWeight*float(options.lumi)

        var=getVariable(t)

        if var > qcd_up_histo.GetBinLowEdge(qcd_up_histo.GetNbinsX()):
            qcd_up_histo.Fill(qcd_up_histo.GetBinCenter(qcd_up_histo.GetNbinsX()),w*t.qcd_weight_up/t.qcd_pdf_weight_orig)
        else:    
            qcd_up_histo.Fill(var,w*t.qcd_weight_up/t.qcd_pdf_weight_orig)

        if var > qcd_down_histo.GetBinLowEdge(qcd_down_histo.GetNbinsX()):
            qcd_down_histo.Fill(qcd_down_histo.GetBinCenter(qcd_down_histo.GetNbinsX()),w*t.qcd_weight_down/t.qcd_pdf_weight_orig)
        else:    
            qcd_down_histo.Fill(var,w*t.qcd_weight_down/t.qcd_pdf_weight_orig)

        if var > histo.GetBinLowEdge(histo.GetNbinsX()):
            histo.Fill(histo.GetBinCenter(histo.GetNbinsX()),w)
        else:    
            histo.Fill(var,w)                                                        

if options.mode != "dim8" and options.mode != "sm" and options.mode != "non-sm" and options.mode != "sm-pdf" and options.mode != "sm-qcd" and options.mode != "gm":
    print "unrecognized mode, exiting"
    sys.exit(1)

if options.mode == "non-sm":
    if options.which_lhe_weight == None:
        print "non-sim mode requires that --which_lhe_weight be used, exiting"
        sys.exit(1)
    if options.datacard != None:
        print "--datacard should not be used in non-sm mode, exiting"
        sys.exit(1)        
    if options.dim8_param != None:
        print "--dim8_param option should only be used in non-sm mode, exiting"
        sys.exit(1)
    if options.dim8_datacard_base != None:
        print "--dim8_datacard_base option should only be used in non-sm mode, exiting"
        sys.exit(1)
    if options.dim8_output_fname != None:
        print "--dim8_output_fname option should only be used in non-sm mode, exiting"
        sys.exit(1)
    if options.dim8_lhe_file != None:
        print "--dim8_lhe_file option should only be used in non-sm mode, exiting"
        sys.exit(1)
        
if options.mode == "sm" or options.mode == "sm-pdf" or options.mode == "sm-qcd":
    if options.datacard == None:
        print "sm mode requires that --datacard be used, exiting"
        sys.exit(1)        
    if options.dim8_param != None:
        print "--dim8_param option should only be used in dim8 mode, exiting"
        sys.exit(1)
    if options.dim8_datacard_base != None:
        print "--dim8_datacard_base option should only be used in dim8 mode, exiting"
        sys.exit(1)
    if options.dim8_output_fname != None:
        print "--dim8_output_fname option should only be used in dim8 mode, exiting"
        sys.exit(1)
    if options.dim8_lhe_file != None:
        print "--dim8_lhe_file option should only be used in dim8 mode, exiting"
        sys.exit(1)
        

if options.mode == "dim8":
    if options.datacard != None:
        print "--datacard should not be used in dim8 mode, exiting"
        sys.exit(1)
    if options.dim8_output_fname == None:
        print "dim8 mode requires that --dim8_output_fname be used, exiting"
        sys.exit(1)
    if options.dim8_param == None:
        print "dim8 mode requires that --dim8_param be used, exiting"
        sys.exit(1)
    if options.dim8_lhe_file == None:
        print "dim8 mode requires that --dim8_lhe_file be used, exiting"
        sys.exit(1)        
    if options.dim8_datacard_base == None:
        print "dim8 mode requires that --dim8_datacard_base be used, exiting"
        sys.exit(1)
    elif options.dim8_param == "FS0":
        dim8_param_number = 1
    elif options.dim8_param == "FS1":
        dim8_param_number = 2
    elif options.dim8_param == "FM0":
        dim8_param_number = 3
    elif options.dim8_param == "FM1":
        dim8_param_number = 4
    elif options.dim8_param == "FM6":
        dim8_param_number = 9
    elif options.dim8_param == "FM7":
        dim8_param_number = 10
    elif options.dim8_param == "FT0":
        dim8_param_number = 11
    elif options.dim8_param == "FT1":
        dim8_param_number = 12                       
    elif options.dim8_param == "FT2":
        dim8_param_number = 13
    else:
        print "unrecognized dimension 8 parameter, exiting"
        sys.exit(1)

if options.mode == "gm":
    if options.gm_datacard_base == None:
        print "gm mode requires that --gm_datacard_base be used, exiting"
        sys.exit(1)
    if options.datacard != None:
        print "--datacard should not be used in gm mode, exiting"
        sys.exit(1)



if options.mode == "dim8":
    reweight_info=parse_reweight_info.parse_reweight_info(dim8_param_number=dim8_param_number,fname=options.dim8_lhe_file)

    oneD_grid_points=reweight_info["oneD_grid_points"]
    histo_grid=reweight_info["histo_grid"]
    lhe_weight_index=reweight_info["lhe_weight_index"]

    #scale each of the parameter values so that they are in units of TeV^-4
    for i in range(0,len(oneD_grid_points)):
        oneD_grid_points[i] = oneD_grid_points[i]*pow(10,12)

    for i in range(0,len(oneD_grid_points)):
        if oneD_grid_points[i] == 0:
            sm_lhe_weight = i
            break


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
    #hist = TH1F('mjj', 'mjj', 35, 0., 3000 )
    hist.GetXaxis().SetTitle("m_{jj} (GeV)")
elif options.variable == "mll":
    binning = array('f',[50,100,200,300,500])
    hist = TH1F('mll', 'mll',4, binning )
    #hist = TH1F('mll', 'mll', 35, 0., 500)
    #hist = TH1F('mll', 'mll', 35, 0., 5000)
    hist.GetXaxis().SetTitle("m_{ll} (GeV)")
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

if options.mode == "dim8":
    aqgc_histos = [ hist.Clone("clone"+str(i)) for i in range(0,len(oneD_grid_points))]

#error = sqrt(sum weight^2)
hist.Sumw2()

hist.SetTitle("")
#hist.SetMaximum(6)

hist.GetXaxis().CenterTitle()
hist.GetXaxis().SetTitleSize(0.045000000149)


pdf_signal_hists=[]
hist_signal=hist.Clone()
hist_signal_qcd_up=hist.Clone()
hist_signal_qcd_down=hist.Clone()
hist_background=hist.Clone()

for i in range(0,100):
    pdf_signal_hists.append(hist.Clone())

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


if options.mode == "dim8":
    fillHistogramsWithReweight(tree_signal,aqgc_histos)
    fillHistogram(tree_background,hist_background)
elif options.mode == "sm":
    fillHistogram(tree_signal,hist_signal)
    fillHistogram(tree_background,hist_background)
elif options.mode == "non-sm":
    fillHistogram(tree_signal,hist_signal,True)
    fillHistogram(tree_background,hist_background)
elif options.mode == "gm":
    fillHistogram(tree_signal,hist_signal)
    fillHistogram(tree_background,hist_background)    
elif options.mode == "sm-pdf":
    fillHistogramWithPDFWeights(tree_signal,pdf_signal_hists)
    fillHistogram(tree_background,hist_background)
elif options.mode == "sm-qcd":
    fillHistogramWithQCDWeights(tree_signal,hist_signal,hist_signal_qcd_up,hist_signal_qcd_down)
    fillHistogram(tree_background,hist_background)  
else:
    assert(0)



#hist_signal.Scale(1/hist_signal.Integral())
#hist_background.Scale(1/hist_background.Integral())

hist_signal.SetLineWidth(3)
hist_background.SetLineWidth(3)

hist_signal.SetLineColor(kRed)
hist_background.SetLineColor(kBlue)

hist_signal.SetMinimum(0)
hist_background.SetMinimum(0)
#hist_signal.SetMaximum(14)
#hist_background.SetMaximum(14)

if options.mode == "sm-qcd":
    hist_signal.Draw()
    hist_signal_qcd_up.Draw("same")
    hist_signal_qcd_down.Draw("same")
    c.Update()
    c.SaveAs(options.output_dir+"qcd_scale_up_down.png")


if options.mode == "sm-pdf":

    pdf_bin_4 = TH1F('yield', 'yield',10,6.5,7.5)

    for i in range(0,len(pdf_signal_hists)):
        pdf_bin_4.Fill(pdf_signal_hists[i].GetBinContent(4))
        pdf_signal_hists[i].Draw()
        c.Update()
        c.SaveAs(options.output_dir+options.variable+str(i)+".png")
    pdf_bin_4.Draw()
    c.Update()
    c.SaveAs(options.output_dir+"pdf_bin_4.png")
        

if options.mode == "sm" or options.mode == "non-sm" or options.mode == "gm":
    hist_signal.Draw()
    print hist_background.GetEntries()
    hist_background.Draw("SAME")

    leg=TLegend(.60,.65,.85,.85)
    leg.AddEntry(hist_signal,"signal","l")
    leg.AddEntry(hist_background,"background","l")
    leg.SetFillColor(0)
    leg.Draw("SAME")

    #c.GetYaxis().SetMaximum(14)
    #c.SetMaximum(14)

    #c.SetLogy()

    c.Update()

    c.SaveAs(options.output_dir+options.variable+".png")

if options.mode == "sm" or options.mode == "sm-pdf" or options.mode == "sm-qcd":

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
    
if options.mode == "dim8":

    for i in range(0,len(oneD_grid_points)):
        if i == 0:
            grid_min = oneD_grid_points[i]
            grid_max = oneD_grid_points[i]
        
        if oneD_grid_points[i] > grid_max:
            grid_max = oneD_grid_points[i]
        
        if oneD_grid_points[i] < grid_min:
            grid_min = oneD_grid_points[i]

    histo_max = grid_max + (grid_max - grid_min)/(len(oneD_grid_points)-1)/2
    histo_min = grid_min - (grid_max - grid_min)/(len(oneD_grid_points)-1)/2

    aqgc_outfile = TFile(options.dim8_output_fname,'recreate')

    for i in range(1,hist.GetNbinsX()+1):
        aqgc_scaling_hist=TH1D("aqgc_scaling_bin_"+str(i),"aqgc_scaling_bin_"+str(i),len(oneD_grid_points),histo_min,histo_max);

        for j in range(0,len(oneD_grid_points)):
            aqgc_scaling_hist.SetBinContent(aqgc_scaling_hist.GetXaxis().FindFixBin(oneD_grid_points[j]), aqgc_histos[j].GetBinContent(i)/aqgc_histos[sm_lhe_weight].GetBinContent(i))
        
        aqgc_outfile.cd()
        aqgc_scaling_hist.Write()    

    for i in range(1,hist_signal.GetNbinsX()+1):

        dcard = open(options.dim8_datacard_base + "_" + options.dim8_param  + "_bin"+str(i)+".txt",'w')

        print >> dcard, "imax 1 number of channels"
        print >> dcard, "jmax * number of background"
        print >> dcard, "kmax * number of nuisance parameters"
        print >> dcard, "Observation 0"
        print >> dcard, "bin bin1 bin1"
        print >> dcard, "process WWjj background"
        print >> dcard, "process 0 1"
        bkg_yield=max(hist_background.GetBinContent(i),0.001)
        print >> dcard, "rate "+str(aqgc_histos[sm_lhe_weight].GetBinContent(i))+" "+str(bkg_yield)
        print >> dcard, "lumi_8tev lnN 2.4 2.4"

#raw_input()

if options.mode == "gm":

    for i in range(1,hist_signal.GetNbinsX()+1):

        dcard = open(options.gm_datacard_base + "_bin"+str(i)+".txt",'w')

        print >> dcard, "imax 1 number of channels"
        print >> dcard, "jmax * number of background"
        print >> dcard, "kmax * number of nuisance parameters"
        print >> dcard, "Observation 0"
        print >> dcard, "bin bin1 bin1"
        print >> dcard, "process WWjj background"
        print >> dcard, "process 0 1"
        bkg_yield=max(hist_background.GetBinContent(i),0.001)
        print >> dcard, "rate "+str(hist_signal.GetBinContent(i))+" "+str(bkg_yield)
        print >> dcard, "lumi_8tev lnN 2.4 2.4"    
