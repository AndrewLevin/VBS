from ConfigurationParser import *

#if running on a dtmit machine, you need to move to root version 5.34.20 or higher
#source /afs/cern.ch/sw/lcg/external/gcc/4.7.2/x86_64-slc5-gcc47-opt/setup.sh
#source /afs/cern.ch/sw/lcg/app/releases/ROOT/5.34.20/x86_64-slc5-gcc47-opt/root/bin/thisroot.sh

import selection

import parse_reweight_info

import optparse

parser = optparse.OptionParser()

parser.add_option('--config',dest='config')

(options,args) = parser.parse_args()

cfg = ConfigurationParser(options.config)

assert("mode" in cfg and "channel" in cfg and "lumi" in cfg)

import sys

#otherwise, root will parse the command line options, see here http://root.cern.ch/phpBB3/viewtopic.php?f=14&t=18637
sys.argv = []

from ROOT import *

from array import array

#gStyle.SetOptStat(0)
gROOT.ProcessLine('#include "/afs/cern.ch/work/a/anlevin/cmssw/CMSSW_7_2_0/src/ntuple_maker/ntuple_maker/interface/enum_definition.h"')

#put the overflow in the last bin
#if (t.jet1+t.jet2).M() > hist.GetBinLowEdge(hist.GetNbinsX()):
#    hist.Fill(hist.GetBinCenter(hist.GetNbinsX()),w)
#else:
#    print (t.jet1+t.jet2).M()
#    hist.Fill((t.jet1+t.jet2).M(),w)

        


def getVariable(t):
    if cfg["variable"] == "mjj":
        return (t.jet1+t.jet2).M()
    elif cfg["variable"] == "mll":
        return (t.lep1+t.lep2).M()
    elif cfg["variable"] == "met":
        return t.metpt
    elif cfg["variable"] == "detajj":
        return abs(t.jet1.Eta() - t.jet2.Eta())
    elif cfg["variable"] == "jet1btag":
        return t.jet1btag
    elif cfg["variable"] == "jet2btag":
        return t.jet2btag
    elif cfg["variable"] == "nvtx":
        return t.nvtx
    elif cfg["variable"] == "lep1pt":
        return t.lep1.pt()
    elif cfg["variable"] == "lep2pt":
        return t.lep2.pt()
    elif cfg["variable"] == "zeppenfeld":
        return max(abs(t.lep1.Eta() - (t.jet1.Eta() + t.jet2.Eta())/2.0),abs(t.lep2.Eta() - (t.jet1.Eta() + t.jet2.Eta())/2.0))
    else:
        assert(0)    

def fillHistogram(t,hist,use_lhe_weight = False):
    print "t.GetEntries() = " + str(t.GetEntries())

    return_hist = hist.Clone()
    
    for entry in range(t.GetEntries()):
        t.GetEntry(entry)

        if entry % 100000 == 0:
            print "entry = " + str(entry)

        if cfg["charge"] == "+":
            if t.lep1id > 0:
                continue
        elif cfg["charge"] == "-":
            if t.lep1id < 0:
                continue
        else:
            assert(cfg["charge"] == "both")
            
        if (abs(t.lep1id) == 13 and abs(t.lep2id) == 11) or (abs(t.lep1id) == 11 and abs(t.lep2id) == 13) :
            channel="em"
        elif abs(t.lep1id) == 13 and abs(t.lep2id) == 13:
            channel = "mm"
        elif abs(t.lep1id) == 11 and abs(t.lep2id) == 11:
            channel = "ee"
        else:
            assert(0)
            
        if cfg["channel"] != channel and cfg["channel"] !="all":
            continue

        if not selection.passSelection(t):
            continue

        w=t.xsWeight*float(cfg["lumi"])

        var=getVariable(t)

        if cfg["mode"] == "non-sm" and use_lhe_weight == True:
            if var > return_hist.GetBinLowEdge(return_hist.GetNbinsX()):
                return_hist.Fill(return_hist.GetBinCenter(return_hist.GetNbinsX()),w*t.lhe_weights[int(options.which_lhe_weight)]/t.lhe_weight_orig)
            else:
                return_hist.Fill(var,w*t.lhe_weights[int(options.which_lhe_weight)]/t.lhe_weight_orig)
        else:
            if var > return_hist.GetBinLowEdge(return_hist.GetNbinsX()):
                return_hist.Fill(return_hist.GetBinCenter(return_hist.GetNbinsX()),w)
            else:
                return_hist.Fill(var,w)

    return {"hist_central" : return_hist }

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
            
        if cfg["channel"] != channel and cfg["channel"] !="all":
            continue

        if not selection.passSelection(t):
            continue

        w=t.xsWeight*float(cfg["lumi"])

        var=getVariable(t)

        for i in range(0,len(oneD_grid_points)):
            if var > histos[i].GetBinLowEdge(histos[i].GetNbinsX()):
                histos[i].Fill(histos[i].GetBinCenter(histos[i].GetNbinsX()),w*t.lhe_weights[lhe_weight_index[i]]/t.lhe_weight_orig)
            else:    
                histos[i].Fill(var,w*t.lhe_weights[lhe_weight_index[i]]/t.lhe_weight_orig)

def fillHistogramsSyscalc(t,hist):
    print "t.GetEntries() = " + str(t.GetEntries())

    return_hist_central = hist.Clone()
    return_hist_pdf_up = hist.Clone()
    return_hist_qcd_down = hist.Clone()
    return_hist_qcd_up = hist.Clone()

    histos = []

    for i in range(0,100):
        new_hist = hist.Clone()
        histos.append(new_hist)

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
            
        if cfg["channel"] != channel and cfg["channel"] !="all":
            continue

        if not selection.passSelection(t):
            continue

        w=t.xsWeight*float(cfg["lumi"])

        var=getVariable(t)

        if var > return_hist_central.GetBinLowEdge(return_hist_central.GetNbinsX()):
            return_hist_central.Fill(return_hist_central.GetBinCenter(return_hist_central.GetNbinsX()),w)
        else:
            return_hist_central.Fill(var,w)

        for i in range(0,100):
            if var > histos[i].GetBinLowEdge(histos[i].GetNbinsX()):
                histos[i].Fill(histos[i].GetBinCenter(histos[i].GetNbinsX()),w*t.pdf_weights[i]/t.qcd_pdf_weight_orig)
            else:    
                histos[i].Fill(var,w*t.pdf_weights[i]/t.qcd_pdf_weight_orig)

        if var > return_hist_qcd_up.GetBinLowEdge(return_hist_qcd_up.GetNbinsX()):
            return_hist_qcd_up.Fill(return_hist_qcd_up.GetBinCenter(return_hist_qcd_up.GetNbinsX()),w*t.qcd_weight_up/t.qcd_pdf_weight_orig)
        else:
            return_hist_qcd_up.Fill(var,w*t.qcd_weight_up/t.qcd_pdf_weight_orig)

        if var > return_hist_qcd_down.GetBinLowEdge(return_hist_qcd_down.GetNbinsX()):
            return_hist_qcd_down.Fill(return_hist_qcd_down.GetBinCenter(return_hist_qcd_down.GetNbinsX()),w*t.qcd_weight_down/t.qcd_pdf_weight_orig)
        else:
            return_hist_qcd_down.Fill(var,w*t.qcd_weight_down/t.qcd_pdf_weight_orig)

    #stdevs = []

    for i in range(1,hist.GetNbinsX()+1):
        yields = []
        
        for j in range(0,100):            
            yields.append(histos[j].GetBinContent(i))

        mean = 0.0    

        for j in range(0,len(yields)):
            mean = mean + yields[j]

        mean = mean/len(yields)

        stdev = 0.0

        for j in range(0,len(yields)):
            stdev = stdev+(yields[j] - mean)*(yields[j] - mean)

        stdev = sqrt(stdev/(len(yields) -1))

        return_hist_pdf_up.SetBinContent(i,return_hist_central.GetBinContent(i)+stdev)

        #stdevs.append(stdev)

    return {"hist_central" : return_hist_central , "hist_pdf_up" : return_hist_pdf_up  , "hist_qcd_up" : return_hist_qcd_up, "hist_qcd_down" : return_hist_qcd_down }

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

        if not selection.passSelection(t):
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

if  cfg["mode"] != "sm" and cfg["mode"] != "non-sm" and cfg["mode"] != "sm-pdf" and cfg["mode"] != "sm-qcd" and cfg["mode"] != "gm" and cfg["mode"] != "reweighted":
    print "unrecognized mode, exiting"
    sys.exit(1)

if cfg["mode"] == "non-sm":
    if "which_lhe_weight" not in cfg:
        print "non-sm mode requires that which_lhe_weight be set, exiting"
        sys.exit(1)
    if "datacard"  in cfg:
        print "datacard should not be used in non-sm mode, exiting"
        sys.exit(1)        
    if "param_name" in cfg:
        print "param_name should not be used in non-sm mode, exiting"
        sys.exit(1)
    if "reweighted_datacard_base" in cfg:
        print "reweighted_datacard_base should not be used in non-sm mode, exiting"
        sys.exit(1)
    if "reweighted_output_fname" in cfg:
        print "reweighted_output_fname should not be used in non-sm mode, exiting"
        sys.exit(1)
    if "reweighted_lhe_file" in cfg:
        print "reweighted_lhe_file should not be used in non-sm mode, exiting"
        sys.exit(1)
        
if cfg["mode"] == "sm":
    if "datacard_base" not in cfg:
        print "sm mode requires that datacard be used, exiting"
        sys.exit(1)        
    if "param_name" in cfg:
        print "param_name should only be used in reweighted mode, exiting"
        sys.exit(1)
    if "reweighted_datacard_base" in cfg:
        print "reweighted_datacard_base should only be used in reweighted mode, exiting"
        sys.exit(1)
    if "reweighted_output_fname" in cfg:
        print "reweighted_output_fname should only be used in reweighted mode, exiting"
        sys.exit(1)
        

if cfg["mode"] == "reweighted":
    if "datacard" in cfg:
        print "datacard should not be used in reweighted mode, exiting"
        sys.exit(1)
    if "reweighted_output_fname" not in cfg:
        print "reweighted mode requires that reweighted_output_fname be used, exiting"
        sys.exit(1)
    if "param_name" not in cfg:
        print "reweighted mode requires that param_name be used, exiting"
        sys.exit(1)
    if "datacard_base" not in cfg:
        print "reweighted mode requires that datacard_base be used, exiting"
        sys.exit(1)
    if "block_name" not in cfg:
        print "reweighted mode requires that block_name be used, exiting"
        sys.exit(1)
    if "units_conversion_exponent" not in cfg:
        print "reweighted mode requires that units_conversion_exponent be used, exiting"
        sys.exit(1)        
    if cfg["param_name"] == "cWW":
        param_number = 7
    elif cfg["param_name"] == "cHW":
        param_number = 9
    elif cfg["param_name"] == "FS0":
        param_number = 1
    elif cfg["param_name"] == "FS1":
        param_number = 2
    elif cfg["param_name"] == "FM0":
        param_number = 3
    elif cfg["param_name"] == "FM1":
        param_number = 4
    elif cfg["param_name"] == "FM6":
        param_number = 9
    elif cfg["param_name"] == "FM7":
        param_number = 10
    elif cfg["param_name"] == "FT0":
        param_number = 11
    elif cfg["param_name"] == "FT1":
        param_number = 12                       
    elif cfg["param_name"] == "FT2":
        param_number = 13
    else:
        print "unrecognized parameter name, exiting"
        sys.exit(1)        

if cfg["mode"] == "gm":
    if "datacard_base" not in cfg:
        print "gm mode requires that datacard_base be used, exiting"
        sys.exit(1)
    if "datacard" in cfg:
        print "datacard should not be used in gm mode, exiting"
        sys.exit(1)
    if "outfile" not in cfg:
        print "gm mode requires that outfile be used, exiting"
        sys.exit(1)

if cfg["mode"] == "reweighted":

    f_reweighted=TFile(cfg["reweighted_file"])

    slha_header_vector = std.vector('string')()
    initrwgt_header_vector = std.vector('string')()

    f_reweighted.GetObject("initrwgt_header",initrwgt_header_vector)

    f_reweighted.GetObject("slha_header",slha_header_vector)

    reweight_info=parse_reweight_info.parse_reweight_info(param_num=param_number, initrwgt_header=initrwgt_header_vector, slha_header=slha_header_vector,block_name=cfg["block_name"])

    oneD_grid_points=reweight_info["oneD_grid_points"]
    histo_grid=reweight_info["histo_grid"]
    lhe_weight_index=reweight_info["lhe_weight_index"]

    #print histo_grid
    #print oneD_grid_points

    #scale each of the parameter values so that they are in units of TeV^-4
    for i in range(0,len(oneD_grid_points)):
        oneD_grid_points[i] = oneD_grid_points[i]*pow(10,int(cfg["units_conversion_exponent"]))
        
    for i in range(0,len(oneD_grid_points)):
        if oneD_grid_points[i] == 0:
            sm_lhe_weight = i
            break

gROOT.cd()
if cfg["variable"] == "mjj":
    binning=array('f',[500,700,1100,1600,2000])
    hist = TH1F('mjj', 'mjj',4, binning )
    #hist = TH1F('mjj', 'mjj', 35, 0., 200 )
    #hist = TH1F('mjj', 'mjj', 35, 0., 3000 )
    hist.GetXaxis().SetTitle("m_{jj} (GeV)")
elif cfg["variable"] == "mll":
    binning = array('f',[50,100,200,300,500])
    hist = TH1F('mll', 'mll',4, binning )
    #hist = TH1F('mll', 'mll', 35, 0., 500)
    #hist = TH1F('mll', 'mll', 35, 0., 5000)
    hist.GetXaxis().SetTitle("m_{ll} (GeV)")
elif cfg["variable"] == "met":
    hist = TH1F('met', 'met', 35, 0., 200 )
elif cfg["variable"] == "detajj":
    hist = TH1F('detajj', 'detajj', 35, 0., 5 )
elif cfg["variable"] == "jet1btag":
    hist = TH1F('jet1btag', 'jet1btag', 35, -1., 1 )
elif cfg["variable"] == "jet2btag":
    hist = TH1F('jet2btag', 'jet2btag', 35, -1., 1 )
elif cfg["variable"] == "nvtx":
    hist = TH1F('nvtx', 'nvtx', 35, 0., 60 )
elif cfg["variable"] == "lep1pt":
    hist = TH1F('lep1pt', 'lep1pt', 35, 0., 100 )
elif cfg["variable"] == "lep2pt":
    hist = TH1F('lep2pt', 'lep2pt', 35, 0., 100 )
elif cfg["variable"] == "zeppenfeld":
    hist = TH1F('zeppenfeld','zeppenfeld',35,0,5)
else:
    assert(0)
    
gROOT.cd()
if cfg["mode"] == "reweighted":
    print hist
    aqgc_histos = [ hist.Clone("clone"+str(i)) for i in range(0,len(oneD_grid_points))]

#error = sqrt(sum weight^2)
hist.Sumw2()

hist.SetTitle("")
#hist.SetMaximum(6)

hist.GetXaxis().CenterTitle()
hist.GetXaxis().SetTitleSize(0.045000000149)

backgrounds = []

pdf_signal_hists=[]
hist_signal=hist.Clone()
hist_signal_qcd_up=hist.Clone()
hist_signal_qcd_down=hist.Clone()

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


if cfg["mode"] == "reweighted":
    f_reweighted=TFile(cfg["reweighted_file"])
    tree_reweighted=f_reweighted.Get("events")
    backgrounds_info=cfg["background_file"]
    for background_info in backgrounds_info:
        f_background=TFile(background_info[0])
        gROOT.cd() #without this, hist_background gets written into a file that goes out of scope
        tree_background=f_background.Get("events")
        hist_background=hist.Clone()

        if background_info[2] == "syscalc":
            return_hists = fillHistogramsSyscalc(tree_background,hist_background)
            backgrounds.append(return_hists)
        else:
            assert(background_info[2] == "none")
            return_hists = fillHistogram(tree_background,hist_background)
            backgrounds.append(return_hists)        

    fillHistogramsWithReweight(tree_reweighted,aqgc_histos)
elif cfg["mode"] == "sm":
    signal_fname=cfg["signal_file"]
    backgrounds_info=cfg["background_file"]

    c=TCanvas("c", "c",0,0,600,500)
    c.Range(0,0,1,1)

    f_signal=TFile(signal_fname)

    tree_signal=f_signal.Get("events")

    signal=fillHistogram(tree_signal,hist_signal)
    for background_info in backgrounds_info:
        f_background=TFile(background_info[0])
        gROOT.cd() #without this, hist_background gets written into a file that goes out of scope
        tree_background=f_background.Get("events")
        hist_background=hist.Clone()

        if background_info[2] == "syscalc":
            return_hists = fillHistogramsSyscalc(tree_background,hist_background)
            backgrounds.append(return_hists)
        else:
            assert(background_info[2] == "none")
            return_hists = fillHistogram(tree_background,hist_background)
            backgrounds.append(return_hists)        
elif cfg["mode"] == "non-sm":
    fillHistogram(tree_signal,hist_signal,True)
    fillHistogram(tree_background,hist_background)
elif cfg["mode"] == "gm":
    signal=fillHistogram(tree_signal,hist_signal)
    for background_info in backgrounds_info:
        f_background=TFile(background_info[0])
        gROOT.cd() #without this, hist_background gets written into a file that goes out of scope
        tree_background=f_background.Get("events")
        hist_background=hist.Clone()

        if background_info[2] == "syscalc":
            return_hists = fillHistogramsSyscalc(tree_background,hist_background)
            backgrounds.append(return_hists)
        else:
            assert(background_info[2] == "none")
            return_hists = fillHistogram(tree_background,hist_background)
            backgrounds.append(return_hists)        
elif cfg["mode"] == "sm-pdf":
    fillHistogramWithPDFWeights(tree_signal,pdf_signal_hists)
    fillHistogram(tree_background,hist_background)
elif cfg["mode"] == "sm-qcd":
    fillHistogramWithQCDWeights(tree_signal,hist_signal,hist_signal_qcd_up,hist_signal_qcd_down)
    fillHistogram(tree_background,hist_background)  
else:
    assert(0)



#hist_signal.Scale(1/hist_signal.Integral())
#hist_background.Scale(1/hist_background.Integral())

if cfg["mode"] == "sm-qcd":
    hist_signal.Draw()
    hist_signal_qcd_up.Draw("same")
    hist_signal_qcd_down.Draw("same")
    c.Update()
    c.SaveAs(options.output_dir+"qcd_scale_up_down.png")


if cfg["mode"] == "sm-pdf":

    pdf_bin_4 = TH1F('yield', 'yield',10,6.5,7.5)

    for i in range(0,len(pdf_signal_hists)):
        pdf_bin_4.Fill(pdf_signal_hists[i].GetBinContent(4))
        pdf_signal_hists[i].Draw()
        c.Update()
        c.SaveAs(options.output_dir+options.variable+str(i)+".png")
    pdf_bin_4.Draw()
    c.Update()
    c.SaveAs(options.output_dir+"pdf_bin_4.png")
        

if cfg["mode"] == "non-sm":
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

if cfg["mode"] == "sm-pdf" or cfg["mode"] == "sm-qcd":

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
    
if cfg["mode"] == "reweighted":

    hist_sum_background = hist.Clone()

    for background in backgrounds:
        #background["hist_central"].Write()
        hist_sum_background.Add(background["hist_central"])

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

    aqgc_outfile = TFile(cfg["reweighted_output_fname"],'recreate')

    for i in range(1,hist.GetNbinsX()+1):
        aqgc_scaling_hist=TH1D("aqgc_scaling_bin_"+str(i),"aqgc_scaling_bin_"+str(i),len(oneD_grid_points),histo_min,histo_max);

        for j in range(0,len(oneD_grid_points)):
            aqgc_scaling_hist.SetBinContent(aqgc_scaling_hist.GetXaxis().FindFixBin(oneD_grid_points[j]), aqgc_histos[j].GetBinContent(i)/aqgc_histos[sm_lhe_weight].GetBinContent(i))
        
        aqgc_outfile.cd()
        aqgc_scaling_hist.Write()    

    for i in range(1,aqgc_histos[sm_lhe_weight].GetNbinsX()+1):

        dcard = open(cfg["datacard_base"] + "_bin"+str(i)+".txt",'w')

        print >> dcard, "imax 1 number of channels"
        print >> dcard, "jmax * number of background"
        print >> dcard, "kmax * number of nuisance parameters"
        print >> dcard, "Observation 0"
        dcard.write("bin")
        dcard.write(" bin1")
        
        for background in backgrounds:
            dcard.write(" bin1")
        dcard.write('\n')    
        
        dcard.write("process")
        dcard.write(" WWjj")
        
        for background_info in backgrounds_info:
            dcard.write(" " + background_info[1])
        dcard.write('\n')    
        dcard.write("process")
        dcard.write(" 0")
        
        for j in range(1,len(backgrounds)+1):
            dcard.write(" " + str(j))
        dcard.write('\n')    
        dcard.write('rate')
        dcard.write(' '+str(aqgc_histos[sm_lhe_weight].GetBinContent(i)))
        for background in backgrounds:
            dcard.write(" "+ str(background["hist_central"].GetBinContent(i)))
        dcard.write('\n')    

        
        #print >> dcard, "process WWjj background"
        #print >> dcard, "process 0 1"
        bkg_yield=max(hist_sum_background.GetBinContent(i),0.001)
        #print >> dcard, "rate "+str(reweighted["hist_central"].GetBinContent(i))+" "+str(bkg_yield)

        dcard.write("lumi_13tev lnN")

        dcard.write(" 1.024")

        for background in backgrounds:
            dcard.write(" 1.024")

        dcard.write('\n')    

        if aqgc_histos[sm_lhe_weight].GetBinContent(i) > 0:
            dcard.write("mcstat_gm lnN "+str(1+aqgc_histos[sm_lhe_weight].GetBinError(i)/aqgc_histos[sm_lhe_weight].GetBinContent(i)))
            for j in range(0,len(backgrounds)):
                dcard.write(" -")
            dcard.write("\n")    
            
        
        for j in range(0,len(backgrounds)):
            if backgrounds[j]["hist_central"].GetBinContent(i) > 0:
                dcard.write("mcstat_"+backgrounds_info[j][1]+" lnN -")
                for k in range(0,len(backgrounds)):
                    if j != k:
                        dcard.write(" -")
                    else:    
                        dcard.write(" " + str(1+backgrounds[j]["hist_central"].GetBinError(i)/backgrounds[j]["hist_central"].GetBinContent(i)))
                dcard.write('\n')        

            dcard.write('\n')        

        #print >> dcard, "lumi_8tev lnN 1.024 1.024"    

#raw_input()

if cfg["mode"] == "gm":

    outfile=TFile(cfg["outfile"],"recreate")

    outfile.cd()

    hist_stack_background = THStack()
    hist_sum_background = hist.Clone()

    for background in backgrounds:
        background["hist_central"].Write()
        hist_stack_background.Add(background["hist_central"])
        hist_sum_background.Add(background["hist_central"])

    signal["hist_central"].Write()

    hist_stack_background.Write()

    hist_sum_background.Write()

    for i in range(1,signal["hist_central"].GetNbinsX()+1):

        dcard = open(cfg["datacard_base"] + "_bin"+str(i)+".txt",'w')

        print >> dcard, "imax 1 number of channels"
        print >> dcard, "jmax * number of background"
        print >> dcard, "kmax * number of nuisance parameters"
        print >> dcard, "Observation 0"
        dcard.write("bin")
        dcard.write(" bin1")
        
        for background in backgrounds:
            dcard.write(" bin1")
        dcard.write('\n')    
        
        dcard.write("process")
        dcard.write(" WWjj")
        
        for background_info in backgrounds_info:
            dcard.write(" " + background_info[1])
        dcard.write('\n')    
        dcard.write("process")
        dcard.write(" 0")
        
        for j in range(1,len(backgrounds)+1):
            dcard.write(" " + str(j))
        dcard.write('\n')    
        dcard.write('rate')
        dcard.write(' '+str(signal["hist_central"].GetBinContent(i)))
        for background in backgrounds:
            dcard.write(" "+ str(background["hist_central"].GetBinContent(i)))
        dcard.write('\n')    

        
        #print >> dcard, "process WWjj WWewk WWqcd ttbar"
        #print >> dcard, "process 0 1"
        bkg_yield=max(hist_sum_background.GetBinContent(i),0.001)
        #print >> dcard, "rate "+str(signal["hist_central"].GetBinContent(i))+" "+str(bkg_yield)

        dcard.write("lumi_13tev lnN")

        dcard.write(" 1.024")

        for background in backgrounds:
            dcard.write(" 1.024")

        dcard.write('\n')    

        if signal["hist_central"].GetBinContent(i) > 0:
            dcard.write("mcstat_gm lnN "+str(1+signal["hist_central"].GetBinError(i)/signal["hist_central"].GetBinContent(i)))
            for j in range(0,len(backgrounds)):
                dcard.write(" -")
            dcard.write("\n")    
            
        
        for j in range(0,len(backgrounds)):
            if backgrounds[j]["hist_central"].GetBinContent(i) > 0:
                dcard.write("mcstat_"+backgrounds_info[j][1]+" lnN -")
                for k in range(0,len(backgrounds)):
                    if j != k:
                        dcard.write(" -")
                    else:    
                        dcard.write(" " + str(1+backgrounds[j]["hist_central"].GetBinError(i)/backgrounds[j]["hist_central"].GetBinContent(i)))
                dcard.write('\n')        


        at_least_one_syscalc=False        
        for j in range(0,len(backgrounds)):
            if backgrounds[j]["hist_central"].GetBinContent(i) > 0 and backgrounds_info[j][2] == "syscalc":
                at_least_one_syscalc=True


        if at_least_one_syscalc:
            dcard.write("pdf lnN")

            dcard.write(" -")
            
            for j in range(0,len(backgrounds)):
                if backgrounds[j]["hist_central"].GetBinContent(i) > 0 and backgrounds_info[j][2] == "syscalc":
                    dcard.write(" "+str(backgrounds[j]["hist_pdf_up"].GetBinContent(i)/backgrounds[j]["hist_central"].GetBinContent(i)))
                else:
                    dcard.write(" -")

            dcard.write('\n')        

            dcard.write("qcd_scale lnN")

            dcard.write(" -")

            for j in range(0,len(backgrounds)):
                if backgrounds[j]["hist_central"].GetBinContent(i) > 0 and backgrounds_info[j][2] == "syscalc":
                    dcard.write(" "+str(backgrounds[j]["hist_qcd_down"].GetBinContent(i)/backgrounds[j]["hist_central"].GetBinContent(i)) +"/"+str(backgrounds[j]["hist_qcd_up"].GetBinContent(i)/backgrounds[j]["hist_central"].GetBinContent(i)))
                else:
                    dcard.write(" -")

            dcard.write('\n')        

        #print >> dcard, "lumi_8tev lnN 1.024 1.024"    


if cfg["mode"] == "sm":

    hist_signal.SetLineWidth(3)
    hist_background.SetLineWidth(3)

    hist_signal.SetLineColor(kRed)
    hist_background.SetLineColor(kBlue)

    hist_signal.SetMinimum(0)
    hist_background.SetMinimum(0)
    #hist_signal.SetMaximum(14)
    #hist_background.SetMaximum(14)

    outfile=TFile(cfg["outfile"],"recreate")

    outfile.cd()

    hist_stack_background = THStack()
    hist_sum_background = hist.Clone("background_sum")

    for i in range(0,len(backgrounds)):
        backgrounds[i]["hist_central"].Clone(backgrounds_info[i][1]).Write()
        hist_stack_background.Add(backgrounds[i]["hist_central"])
        hist_sum_background.Add(backgrounds[i]["hist_central"])

    signal["hist_central"].Clone("wpwpjjewk").Write()

    hist_stack_background.Write()

    hist_sum_background.Write()

    for i in range(1,signal["hist_central"].GetNbinsX()+1):

        dcard = open(cfg["datacard_base"] + "_bin"+str(i)+".txt",'w')

        print >> dcard, "imax 1 number of channels"
        print >> dcard, "jmax * number of background"
        print >> dcard, "kmax * number of nuisance parameters"
        print >> dcard, "Observation 0"
        dcard.write("bin")
        dcard.write(" bin1")
        
        for background in backgrounds:
            dcard.write(" bin1")
        dcard.write('\n')    
        
        dcard.write("process")
        dcard.write(" WWjj")
        
        for background_info in backgrounds_info:
            dcard.write(" " + background_info[1])
        dcard.write('\n')    
        dcard.write("process")
        dcard.write(" 0")
        
        for j in range(1,len(backgrounds)+1):
            dcard.write(" " + str(j))
        dcard.write('\n')    
        dcard.write('rate')
        dcard.write(' '+str(signal["hist_central"].GetBinContent(i)))
        for background in backgrounds:
            dcard.write(" "+ str(background["hist_central"].GetBinContent(i)))
        dcard.write('\n')    

        
        #print >> dcard, "process WWjj WWqcd ttbar"
        #print >> dcard, "process 0 1"
        bkg_yield=max(hist_sum_background.GetBinContent(i),0.001)
        #print >> dcard, "rate "+str(signal["hist_central"].GetBinContent(i))+" "+str(bkg_yield)

        dcard.write("lumi_13tev lnN")

        dcard.write(" 1.024")

        for background in backgrounds:
            dcard.write(" 1.024")

        dcard.write('\n')    

        if signal["hist_central"].GetBinContent(i) > 0:
            dcard.write("mcstat_gm lnN "+str(1+signal["hist_central"].GetBinError(i)/signal["hist_central"].GetBinContent(i)))
            for j in range(0,len(backgrounds)):
                dcard.write(" -")
            dcard.write("\n")    
            
        
        for j in range(0,len(backgrounds)):
            if backgrounds[j]["hist_central"].GetBinContent(i) > 0:
                dcard.write("mcstat_"+backgrounds_info[j][1]+" lnN -")
                for k in range(0,len(backgrounds)):
                    if j != k:
                        dcard.write(" -")
                    else:    
                        dcard.write(" " + str(1+backgrounds[j]["hist_central"].GetBinError(i)/backgrounds[j]["hist_central"].GetBinContent(i)))
                dcard.write('\n')        


        at_least_one_syscalc=False        
        for j in range(0,len(backgrounds)):
            if backgrounds[j]["hist_central"].GetBinContent(i) > 0 and backgrounds_info[j][2] == "syscalc":
                at_least_one_syscalc=True


        if at_least_one_syscalc:
            dcard.write("pdf lnN")

            dcard.write(" -")
            
            for j in range(0,len(backgrounds)):
                if backgrounds[j]["hist_central"].GetBinContent(i) > 0 and backgrounds_info[j][2] == "syscalc":
                    dcard.write(" "+str(backgrounds[j]["hist_pdf_up"].GetBinContent(i)/backgrounds[j]["hist_central"].GetBinContent(i)))
                else:
                    dcard.write(" -")

            dcard.write('\n')        

            dcard.write("qcd_scale lnN")

            dcard.write(" -")

            for j in range(0,len(backgrounds)):
                if backgrounds[j]["hist_central"].GetBinContent(i) > 0 and backgrounds_info[j][2] == "syscalc":
                    dcard.write(" "+str(backgrounds[j]["hist_qcd_down"].GetBinContent(i)/backgrounds[j]["hist_central"].GetBinContent(i)) +"/"+str(backgrounds[j]["hist_qcd_up"].GetBinContent(i)/backgrounds[j]["hist_central"].GetBinContent(i)))
                else:
                    dcard.write(" -")

            dcard.write('\n')        

        #print >> dcard, "lumi_8tev lnN 1.024 1.024"    
