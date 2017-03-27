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

assert(cfg["which_selection"] == "relaxed" or cfg["which_selection"] == "full" or cfg["which_selection"] == "full_novbs" or cfg["which_selection"] == "relaxed_btagged" or cfg["which_selection"] == "full_btagged" or cfg["which_selection"] == "full_lowmjj1" or cfg["which_selection"] == "full_lowmjj2")

if cfg["significance_variable"] == "mllmjj":
    binningmjj=array('f',[500,800,1100,1500,2000])
    binningmll=array('f',[20,100,200,300])
    hist = TH2F('mllmjj', 'mllmjj',len(binningmjj)-1, binningmjj,len(binningmll)-1, binningmll )

else:
    assert(0)

plots_templates = {}
if cfg["plot_variable"] == "all":

    charge_flavor_permuations = ["mm_plus","mm_minus","em_plus","em_minus","ee_plus","ee_minus","mm_both","em_both","ee_both"]

    if cfg["which_selection"] == "full" or cfg["which_selection"] == "full_btagged":
        binningmjj=array('f',[500,800,1100,1500,2000])
        histmjj = TH1F('mjj', 'mjj',4, binningmjj )        
    elif cfg["which_selection"] == "full_lowmjj1" or cfg["which_selection"] == "full_lowmjj2":
        histmjj = TH1F('mjj', 'mjj', 4, 100., 500 )
    else:
        assert(0)

    binningmll = array('f',[50,100,200,300,500])
    histmll = TH1F('mll', 'mll',4, binningmll )    
    histmet = TH1F('met', 'met', 18 , 20., 200 )
    histmlljj = TH1F('mlljj', 'mlljj', 15 , 500., 2000 )    
    histdetajj = TH1F('detajj', 'detajj', 10, 2.5, 7.5 )
    histlep1pt = TH1F('lep1pt', 'lep1pt', 20, 0., 100 )
    histlep2pt = TH1F('lep2pt', 'lep2pt', 20, 0., 100 )
    histjet1pt = TH1F('jet1pt', 'jet1pt', 20, 0., 100 )
    histjet2pt = TH1F('jet2pt', 'jet2pt', 20, 0., 100 )
    histlep1eta = TH1F('lep1eta', 'lep1eta', 10, -2.5, 2.5 )
    histlep2eta = TH1F('lep2eta', 'lep2eta', 10, -2.5, 2.5 )
    histjet1eta = TH1F('jet1eta', 'jet1eta', 10, -5., 5 )
    histjet2eta = TH1F('jet2eta', 'jet1eta', 10, -5., 5 )

    histmll.Sumw2()
    histmet.Sumw2()
    histmlljj.Sumw2()
    histdetajj.Sumw2()
    histlep1pt.Sumw2()
    histlep2pt.Sumw2()
    histjet1pt.Sumw2()
    histjet2pt.Sumw2()
    histlep1eta.Sumw2()
    histlep2eta.Sumw2()
    histjet1eta.Sumw2()
    histjet2eta.Sumw2()

    plots_templates["mjj"] = histmjj
    plots_templates["mll"] = histmll
    plots_templates["mlljj"] = histmlljj    
    plots_templates["met"] = histmet
    plots_templates["detajj"] = histdetajj
    plots_templates["lep1pt"] = histlep1pt
    plots_templates["lep2pt"] = histlep2pt
    plots_templates["lep1eta"] = histlep1eta
    plots_templates["lep2eta"] = histlep2eta    
    plots_templates["jet1pt"] = histjet1pt
    plots_templates["jet2pt"] = histjet2pt
    plots_templates["jet1eta"] = histjet1eta
    plots_templates["jet2eta"] = histjet2eta

    for charge_flavor_permutation in charge_flavor_permuations:
        if cfg["which_selection"] == "full" or cfg["which_selection"] == "full_btagged":
            histmjjchargeflavorpermuation = TH1F('mjj_'+charge_flavor_permutation, 'mjj_'+charge_flavor_permutation,4, binningmjj )
        elif cfg["which_selection"] == "full_lowmjj1" or cfg["which_selection"] == "full_lowmjj2":
            histmjjchargeflavorpermutation = TH1F('mjj_'+charge_flavor_permutation, 'mjj_'+charge_flavor_permutation, 4, 100., 500 )
        else:
            assert(0)

        histmjjchargeflavorpermutation.Sumw2()
        plots_templates["mjj_"+charge_flavor_permutation] = histmjjchargeflavorpermutation
    
else:
    assert(0)
    
backgrounds = []

hist.Sumw2()



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

    plots = {}

    plots_data = {}

    for plots_template_key in plots_templates.keys():
        plots_data[plots_template_key] = plots_templates[plots_template_key].Clone()

    plots_fake = {}

    for plots_template_key in plots_templates.keys():
        plots_fake[plots_template_key] = plots_templates[plots_template_key].Clone()

    plots_signal = {}

    for plots_template_key in plots_templates.keys():
        plots_signal[plots_template_key] = plots_templates[plots_template_key].Clone()                

    hist_data=hist.Clone()

    hist_fake=hist.Clone()

    hist_signal=hist.Clone()

    c=TCanvas("c", "c",0,0,600,500)
    c.Range(0,0,1,1)

    f_signal=TFile(signal_info[0])

    tree_signal=f_signal.Get("events")

    if signal_info[2] == "syscalc":
        signal=histogram_fillers.fillHistogram(cfg,tree_signal,hist_signal,plots_signal,syscalc=True)
    else:
        assert(signal_info[2] == "none")
        signal=histogram_fillers.fillHistogram(cfg,tree_signal,hist_signal,plots_signal,fill_cutflow_histograms=True)

    mc_trees_for_fake_histogram_filler = []

    for background_info in backgrounds_info:

        f_background=TFile(background_info[0])

        gROOT.cd() #without this, hist_background gets written into a file that goes out of scope

        tree_background=f_background.Get("events").CloneTree()

        #tree_background.SetDirectory(0)

        mc_trees_for_fake_histogram_filler.append(tree_background)

        hist_background=hist.Clone()

        plots_background = {}

        for plots_template_key in plots_templates.keys():
            plots_background[plots_template_key] = plots_templates[plots_template_key].Clone()                

        if background_info[2] == "syscalc":
            return_hists = histogram_fillers.fillHistogram(cfg,tree_background,hist_background,plots_background,syscalc=True)
            backgrounds.append(return_hists)
        else:
            assert(background_info[2] == "none")
            return_hists = histogram_fillers.fillHistogram(cfg,tree_background,hist_background, plots_background)
            backgrounds.append(return_hists)

        plots[background_info[1]] = plots_background

    data_fname=cfg["data_file"]
    f_data = TFile(data_fname)
    tree_data = f_data.Get("events")

    fake_muons = hist.Clone()
    fake_electrons = hist.Clone()


#    for background_info in backgrounds_info:
#        print background_info[0]
#        f_background=TFile(background_info[0])
#        gROOT.cd()
#        tree_background=f_background.Get("events")
#        print type(tree_background)
#        mc_trees_for_fake_histogram_filler.append(tree_background)
#        break

#    f_signal=TFile(signal_info[0])
#    gROOT.cd()    
#    tree_signal=f_signal.Get("events")
#    print type(tree_signal)

    mc_trees_for_fake_histogram_filler.append(tree_signal)        

    plots["signal"] = plots_signal
    plots["fake"] = plots_fake
    plots["data"] = plots_data        

    fake=histogram_fillers.fillHistogramFake(cfg,tree_data,mc_trees_for_fake_histogram_filler,hist_fake,plots_fake,fake_muons,fake_electrons)

    data = None

    if not cfg["blind_high_mjj"]:
        data=histogram_fillers.fillHistogram(cfg,tree_data,hist_data,plots_data,is_data=True)


    
    write_results.write_sm_mc_fake(cfg,hist,hist_signal,hist_background,plots,backgrounds,backgrounds_info,signal,signal_info,fake_muons,fake_electrons,fake,data)

if cfg["mode"] == "sm_low_mjj_control_region":

    assert(cfg["channel"] == "all" or cfg["channel"] == "ee" or cfg["channel"] == "em" or cfg["channel"] == "mm")

    hist_data=hist.Clone()

    hist_fake=hist.Clone()

    #hist_signal=hist.Clone()
    
    #signal_fname=cfg["signal_file"]

    if "background_file" in cfg:
        backgrounds_info=cfg["background_file"]
    else:
        backgrounds_info = []

    c=TCanvas("c", "c",0,0,600,500)
    c.Range(0,0,1,1)

    #f_signal=TFile(signal_fname)

    #tree_signal=f_signal.Get("events")

    hist_background=hist.Clone()

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

    if "fakeratemc_sample_file" in cfg:
        fakeratemc_samples_info=cfg["fakeratemc_sample_file"]
    else:
        fakeratemc_samples_info = []        

    if "data_sample_file" in cfg:
        data_samples_info=cfg["data_sample_file"]    
    else:
        data_samples_info = []

    c=TCanvas("c", "c",0,0,600,500)
    c.Range(0,0,1,1)

    mc_samples = []

    data_samples = []    

    fake_samples = []

    fakeratemc_samples = []


    for fakeratemc_sample_info in fakeratemc_samples_info:
        f_fakeratemc_sample=TFile(fakeratemc_sample_info[0])
        gROOT.cd() #without this, hist_background gets written into a file that goes out of scope

        tree_fakeratemc_sample=f_fakeratemc_sample.Get("events")
        hist_fakeratemc_sample=hist.Clone()
        
        fake_muons = hist.Clone()
        fake_electrons = hist.Clone()

        return_hists=histogram_fillers.fillHistogramFake(cfg,tree_fakeratemc_sample,hist_fakeratemc_sample,fake_muons,fake_electrons,applying_to_ttbar_mc=True)

        fakeratemc_samples.append(return_hists)

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

        return_hists = histogram_fillers.fillHistogram(cfg,tree_mc_sample,hist_mc_sample,debug=True)

        mc_samples.append(return_hists)

    for data_sample_info in data_samples_info:
        f_data_sample=TFile(data_sample_info[0])
        gROOT.cd() #without this, hist_background gets written into a file that goes out of scope
        tree_data_sample=f_data_sample.Get("events")
        hist_data_sample=hist.Clone()

        return_hists = histogram_fillers.fillHistogram(cfg,tree_data_sample,hist_data_sample, is_data=True, debug=True)

        data_samples.append(return_hists)

    write_results.write_produce_histograms(cfg,hist,mc_samples,mc_samples_info,fake_samples, data_samples,fakeratemc_samples)


