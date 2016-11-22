from ConfigurationParser import *

#if running on a dtmit machine, you need to move to root version 5.34.20 or higher
#source /afs/cern.ch/sw/lcg/external/gcc/4.7.2/x86_64-slc5-gcc47-opt/setup.sh
#source /afs/cern.ch/sw/lcg/app/releases/ROOT/5.34.20/x86_64-slc5-gcc47-opt/root/bin/thisroot.sh

import parse_reweight_info

import histogram_fillers

import write_results

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

if  cfg["mode"] != "sm" and cfg["mode"] != "non-sm" and cfg["mode"] != "sm-pdf" and cfg["mode"] != "sm-qcd" and cfg["mode"] != "gm" and cfg["mode"] != "reweighted_v1" and cfg["mode"] != "reweighted_v2" and cfg["mode"] != "sm_low_mjj_control_region" and cfg["mode"] != "sm_mc" and cfg["mode"] != "sm_mc_fake" and cfg["mode"] != "fr_closure_test" and cfg["mode"] != "produce_histograms":
    print "unrecognized mode, exiting"
    sys.exit(1)

gROOT.cd()
if cfg["variable"] == "mjj":
    if cfg["mode"] == "sm_low_mjj_control_region":
        hist = TH1F('mjj', 'mjj', 4, 100., 500 )
    elif cfg["mode"] == "fr_closure_test":
        if cfg["which_selection"] == "full":
            #hist = TH1F('mjj', 'mjj', 4, 100., 500 )
            binning=array('f',[500,700,1100,1600,2000])
            hist = TH1F('mjj', 'mjj',4, binning )
        elif cfg["which_selection"] == "full_novbs":
            binning=array('f',[0,100,200,300,400,500,700,1100,1600,2000])
            hist = TH1F('mjj', 'mjj',9, binning )
        elif cfg["which_selection"] == "relaxed_btag":
            binning=array('f',[0,100,200,300,400,500,700,1100,1600,2000])
            hist = TH1F('mjj', 'mjj',9, binning )                        
        else:
            binning=array('f',[0,100,200,300,400,500,700,1100,1600,2000])
            hist = TH1F('mjj', 'mjj',9, binning )
    elif cfg["mode"] == "produce_histograms":
        binning=array('f',[500,700,1100,1600,2000])
        hist = TH1F('mjj', 'mjj',4, binning )
        #binning=array('f',[0,100,200,300,400,500,700,1100,1600,2000])
        #hist = TH1F('mjj', 'mjj',9, binning )        
    else:
        #hist = TH1F('mjj', 'mjj', 4, 100., 500 )        
        binning=array('f',[500,700,1100,1600,2000])
        hist = TH1F('mjj', 'mjj',4, binning )
    #hist = TH1F('mjj', 'mjj', 35, 0., 200 )
    #hist = TH1F('mjj', 'mjj', 35, 0., 3000 )
    hist.GetXaxis().SetTitle("m_{jj} (GeV)")
elif cfg["variable"] == "mll":
    if cfg["mode"] == "sm_low_mjj_control_region":
        hist = TH1F('mll', 'mll', 15, 0., 150)
    else:
        #hist = TH1F('mll', 'mll', 15, 0., 150)
        #hist = TH1F('mll', 'mll', 5, 0., 50 )
        binning = array('f',[50,100,200,300,500])
        hist = TH1F('mll', 'mll',4, binning )
    #hist = TH1F('mll', 'mll', 35, 0., 500)
    #hist = TH1F('mll', 'mll', 35, 0., 5000)
    hist.GetXaxis().SetTitle("m_{ll} (GeV)")
elif cfg["variable"] == "met":
    hist = TH1F('met', 'met', 35, 0., 200 )
elif cfg["variable"] == "detajj":
    hist = TH1F('detajj', 'detajj', 35, 0., 5 )
elif cfg["variable"] == "maxbtagevent":
    hist = TH1F('maxbtagevent', 'maxbtagevent', 35, -1., 1 )
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

backgrounds = []

hist.Sumw2()

assert(cfg["which_selection"] == "relaxed" or cfg["which_selection"] == "full" or cfg["which_selection"] == "full_novbs" or cfg["which_selection"] == "relaxed_btagged")

if cfg["mode"] == "reweighted_v1" or cfg["mode"] == "reweighted_v2":
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

if cfg["mode"] == "reweighted_v2":
    if "atgcroostats_config_fname" not in cfg:
        print "reweighted_v2 mode requires that atgcroostats_config_fname be used, exiting"
        sys.exit(1)

if cfg["mode"] == "reweighted_v1":
    if "atgcroostats_config_fname" in cfg:
        print "atgcroostats_config_fname should not be used in reweighted_v1, exiting"
        sys.exit(1)        


if cfg["mode"] == "reweighted_v1" or cfg["mode"] == "reweighted_v2":

    hist_fake=hist.Clone()

    fake_muons = hist.Clone()
    fake_electrons = hist.Clone()

    f_reweighted=TFile(cfg["reweighted_file"])

    slha_header_vector = std.vector('string')()
    initrwgt_header_vector = std.vector('string')()

    f_reweighted.GetObject("initrwgt_header",initrwgt_header_vector)

    f_reweighted.GetObject("slha_header",slha_header_vector)

    reweight_info=parse_reweight_info.parse_reweight_info(param_num=param_number, initrwgt_header=initrwgt_header_vector, slha_header=slha_header_vector,block_name=cfg["block_name"])

    oneD_grid_points=reweight_info["oneD_grid_points"]
    histo_grid=reweight_info["histo_grid"]
    mgreweight_weight_index=reweight_info["lhe_weight_index"]

    assert(len(mgreweight_weight_index) == len(oneD_grid_points))

    #print histo_grid
    #print oneD_grid_points

    #scale each of the parameter values so that they are in units of TeV^-4
    for i in range(0,len(oneD_grid_points)):
        oneD_grid_points[i] = oneD_grid_points[i]*pow(10,int(cfg["units_conversion_exponent"]))
        
    for i in range(0,len(oneD_grid_points)):
        if oneD_grid_points[i] == 0:
            sm_lhe_weight = i
            break

    print hist

    gROOT.cd()

    aqgc_histos = [ hist.Clone("clone"+str(i)) for i in range(0,len(oneD_grid_points))]

    print aqgc_histos
    
    data_fname=cfg["data_file"]
    f_data = TFile(data_fname)
    tree_data = f_data.Get("events")
    
    f_reweighted=TFile(cfg["reweighted_file"])
    tree_reweighted=f_reweighted.Get("events")
    backgrounds_info=cfg["background_file"]
    for background_info in backgrounds_info:
        f_background=TFile(background_info[0])
        gROOT.cd() #without this, hist_background gets written into a file that goes out of scope
        tree_background=f_background.Get("events")
        hist_background=hist.Clone()

        if background_info[2] == "syscalc":
            return_hists = histogram_fillers.fillHistogram(cfg,tree_background,hist_background,syscalc=True)
            backgrounds.append(return_hists)
        else:
            assert(background_info[2] == "none")
            return_hists = histogram_fillers.fillHistogram(cfg,tree_background,hist_background)
            backgrounds.append(return_hists)

    print aqgc_histos

    histogram_fillers.fillHistogramsWithReweight(cfg,tree_reweighted,aqgc_histos,mgreweight_weight_index)

    fake=histogram_fillers.fillHistogramFake(cfg,tree_data,hist_fake,fake_muons,fake_electrons)

    if cfg["mode"] == "reweighted_v1":
        write_results.write_reweighted_mode_v1(cfg,hist,backgrounds, oneD_grid_points,aqgc_histos,fake_muons,fake_electrons,sm_lhe_weight,backgrounds_info,fake)
    elif cfg["mode"] == "reweighted_v2":
        write_results.write_reweighted_mode_v2(cfg,hist,backgrounds, oneD_grid_points,aqgc_histos,fake_muons,fake_electrons,sm_lhe_weight,backgrounds_info,fake)
    else:
        assert(0)

if cfg["mode"] == "sm_mc_fake":

    assert(cfg["channel"] == "all" or cfg["channel"] == "ee" or cfg["channel"] == "em" or cfg["channel"] == "mm")

    signal_info=cfg["signal_file"]
    backgrounds_info=cfg["background_file"]

    hist_fake=hist.Clone()

    hist_signal=hist.Clone()

    c=TCanvas("c", "c",0,0,600,500)
    c.Range(0,0,1,1)

    f_signal=TFile(signal_info[0])

    tree_signal=f_signal.Get("events")

    if signal_info[2] == "syscalc":
        signal=histogram_fillers.fillHistogram(cfg,tree_signal,hist_signal,syscalc=True)
    else:
        assert(signal_info[2] == "none")
        signal=histogram_fillers.fillHistogram(cfg,tree_signal,hist_signal,fill_cutflow_histograms=True)

    for background_info in backgrounds_info:
        f_background=TFile(background_info[0])
        gROOT.cd() #without this, hist_background gets written into a file that goes out of scope
        tree_background=f_background.Get("events")
        hist_background=hist.Clone()

        if background_info[2] == "syscalc":
            return_hists = histogram_fillers.fillHistogram(cfg,tree_background,hist_background,syscalc=True)
            backgrounds.append(return_hists)
        else:
            assert(background_info[2] == "none")
            return_hists = histogram_fillers.fillHistogram(cfg,tree_background,hist_background)
            backgrounds.append(return_hists)

    data_fname=cfg["data_file"]
    f_data = TFile(data_fname)
    tree_data = f_data.Get("events")

    fake_muons = hist.Clone()
    fake_electrons = hist.Clone()
    
    fake=histogram_fillers.fillHistogramFake(cfg,tree_data,hist_fake,fake_muons,fake_electrons)
    
    write_results.write_sm_mc_fake(cfg,hist,hist_signal,hist_background,backgrounds,backgrounds_info,signal,signal_info,fake_muons,fake_electrons,fake)

if cfg["mode"] == "sm_low_mjj_control_region":

    assert(cfg["channel"] == "all" or cfg["channel"] == "ee" or cfg["channel"] == "em" or cfg["channel"] == "mm")

    hist_data=hist.Clone()

    hist_fake=hist.Clone()

    #hist_signal=hist.Clone()
    
    #signal_fname=cfg["signal_file"]
    backgrounds_info=cfg["background_file"]

    c=TCanvas("c", "c",0,0,600,500)
    c.Range(0,0,1,1)

    #f_signal=TFile(signal_fname)

    #tree_signal=f_signal.Get("events")

    #signal=histogram_fillers.fillHistogram(cfg,tree_signal,hist_signal)
    for background_info in backgrounds_info:
        f_background=TFile(background_info[0])
        gROOT.cd() #without this, hist_background gets written into a file that goes out of scope
        tree_background=f_background.Get("events")
        hist_background=hist.Clone()

        if background_info[2] == "syscalc":
            return_hists = histogram_fillers.fillHistogram(cfg,tree_background,hist_background,syscalc=True)
            backgrounds.append(return_hists)
        else:
            assert(background_info[2] == "none")
            return_hists = histogram_fillers.fillHistogram(cfg,tree_background,hist_background)
            backgrounds.append(return_hists)

    data_fname=cfg["data_file"]
    f_data = TFile(data_fname)
    tree_data = f_data.Get("events")
    data=histogram_fillers.fillHistogram(cfg,tree_data,hist_data,is_data=True)

    fake_muons = hist.Clone()
    fake_electrons = hist.Clone()

    fake=histogram_fillers.fillHistogramFake(cfg,tree_data,hist_fake,fake_muons,fake_electrons)
    
    write_results.write_sm_low_mjj_control_region(cfg,hist,hist_background,backgrounds,backgrounds_info,fake_muons,fake_electrons,fake,data)


if cfg["mode"] == "fr_closure_test":

    hist_ttbar=hist.Clone()

    hist_ttbar_qcd_fr=hist.Clone()

    ttbar_fname=cfg["ttbar_fname"]

    c=TCanvas("c", "c",0,0,600,500)
    c.Range(0,0,1,1)

    f_ttbar=TFile(ttbar_fname)

    tree_ttbar=f_ttbar.Get("events")

    fake_muons = hist.Clone()
    fake_electrons = hist.Clone()

    ttbar=histogram_fillers.fillHistogram(cfg,tree_ttbar,hist_ttbar)
    ttbar_qcd_fr=histogram_fillers.fillHistogramFake(cfg,tree_ttbar,hist_ttbar_qcd_fr,fake_muons,fake_electrons,True)

    write_results.write_fr_closure_test(cfg,ttbar,ttbar_qcd_fr)

if cfg["mode"] == "produce_histograms":

    assert(cfg["channel"] == "all" or cfg["channel"] == "ee" or cfg["channel"] == "em" or cfg["channel"] == "mm")

    if "mc_sample_file" in cfg:
        mc_samples_info=cfg["mc_sample_file"]
    else:
        mc_samples_info = []

    if "fake_sample_file" in cfg:
        fake_samples_info=cfg["fake_sample_file"]
    else:
        fake_samples_info = []

    if "data_sample_file" in cfg:
        data_samples_info=cfg["data_sample_file"]    
    else:
        data_samples_info = []

    c=TCanvas("c", "c",0,0,600,500)
    c.Range(0,0,1,1)

    mc_samples = []

    data_samples = []    

    fake_samples = []

    for fake_sample_info in fake_samples_info:
        f_fake_sample=TFile(fake_sample_info[0])
        gROOT.cd() #without this, hist_background gets written into a file that goes out of scope

        tree_fake_sample=f_fake_sample.Get("events")
        hist_fake_sample=hist.Clone()
        
        fake_muons = hist.Clone()
        fake_electrons = hist.Clone()

        return_hists=histogram_fillers.fillHistogramFake(cfg,tree_fake_sample,hist_fake_sample,fake_muons,fake_electrons)

        fake_samples.append(return_hists)

    for mc_sample_info in mc_samples_info:
        f_mc_sample=TFile(mc_sample_info[0])
        gROOT.cd() #without this, hist_background gets written into a file that goes out of scope
        tree_mc_sample=f_mc_sample.Get("events")
        hist_mc_sample=hist.Clone()

        return_hists = histogram_fillers.fillHistogram(cfg,tree_mc_sample,hist_mc_sample)

        mc_samples.append(return_hists)

    for data_sample_info in data_samples_info:
        f_data_sample=TFile(data_sample_info[0])
        gROOT.cd() #without this, hist_background gets written into a file that goes out of scope
        tree_data_sample=f_data_sample.Get("events")
        hist_data_sample=hist.Clone()

        return_hists = histogram_fillers.fillHistogram(cfg,tree_data_sample,hist_data_sample, is_data=True)

        data_samples.append(return_hists)

    write_results.write_produce_histograms(cfg,hist,mc_samples,mc_samples_info,fake_samples, data_samples)


