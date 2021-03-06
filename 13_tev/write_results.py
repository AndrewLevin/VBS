from ROOT import *

def write_reweighted_mode_v1(cfg,hist,backgrounds, oneD_grid_points,aqgc_histos,fake_muons,fake_electrons,sm_lhe_weight,backgrounds_info,fake,data,plots):
    #signal["hist_central"].Write()

    #outfile=TFile(cfg["outfile"],"recreate")

    #outfile.cd()

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
            assert(aqgc_histos[sm_lhe_weight].GetBinContent(i) > 0)

            aqgc_scaling_hist.SetBinContent(aqgc_scaling_hist.GetXaxis().FindFixBin(oneD_grid_points[j]), aqgc_histos[j].GetBinContent(i)/aqgc_histos[sm_lhe_weight].GetBinContent(i))
        
        aqgc_outfile.cd()
        aqgc_scaling_hist.Write()    

    for i in range(1,aqgc_histos[sm_lhe_weight].GetNbinsX()+1):

        print ""
        for j in range(0,len(oneD_grid_points)):
            print 1+aqgc_histos[j].GetBinError(i)/aqgc_histos[j].GetBinContent(i)


        dcard = open(cfg["datacard_base"] + "_bin"+str(i)+".txt",'w')

        print >> dcard, "imax 1 number of channels"
        print >> dcard, "jmax * number of background"
        print >> dcard, "kmax * number of nuisance parameters"
        print >> dcard, "Observation "+str(data["hist_central"].GetBinContent(i))
        dcard.write("bin")
        dcard.write(" bin1")
        
        for background in backgrounds:
            dcard.write(" bin1")

        dcard.write(" bin1")    
        dcard.write('\n')    
        
        dcard.write("process")
        dcard.write(" WWjj")
        
        for background_info in backgrounds_info:
            dcard.write(" " + background_info[1])

        dcard.write(" fake")
        dcard.write('\n')    
        dcard.write("process")
        dcard.write(" 0")
        
        for j in range(1,len(backgrounds)+2):
            dcard.write(" " + str(j))
        dcard.write('\n')    
        dcard.write('rate')
        dcard.write(' '+str(aqgc_histos[sm_lhe_weight].GetBinContent(i)))
        for background in backgrounds:
            dcard.write(" "+ str(background["hist_central"].GetBinContent(i)))
        dcard.write(" "+str(fake["hist_central"].GetBinContent(i)))    
        dcard.write('\n')    

        
        #print >> dcard, "process WWjj background"
        #print >> dcard, "process 0 1"
        bkg_yield=max(hist_sum_background.GetBinContent(i),0.001)
        #print >> dcard, "rate "+str(reweighted["hist_central"].GetBinContent(i))+" "+str(bkg_yield)

        dcard.write("lumi_13tev lnN")

        dcard.write(" 1.027")

        for background in backgrounds:
            dcard.write(" 1.027")

        dcard.write(" 1.027")

        dcard.write('\n')    

        if aqgc_histos[sm_lhe_weight].GetBinContent(i) > 0:
            dcard.write("mcstat_dim8 lnN "+str(1+aqgc_histos[sm_lhe_weight].GetBinError(i)/aqgc_histos[sm_lhe_weight].GetBinContent(i)))
            for j in range(0,len(backgrounds)):
                dcard.write(" -")

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

                dcard.write(" -")        

                dcard.write('\n')        

        if fake["hist_central"].GetBinContent(i) > 0:

            dcard.write("fake lnN -")

            for j in range(0,len(backgrounds)):
                dcard.write(" -")

            dcard.write(" " + str(1+fake["hist_central"].GetBinError(i)/fake["hist_central"].GetBinContent(i)))            

            dcard.write('\n')
        #print >> dcard, "lumi_8tev lnN 1.027 1.027"    

    outfile=TFile(cfg["outfile"],"recreate")

    outfile.cd()

    #fake["hist_central"].Clone("fake").Write()

    #for i in range(0,len(backgrounds)):
    #    backgrounds[i]["hist_central"].Write(backgrounds_info[i][1])

    for process in plots.keys():
        for variable in plots[process].keys():
            plots[process][variable].Clone(str(process)+"_"+str(variable)).Write()


def write_reweighted_mode_v2(cfg,hist,backgrounds, oneD_grid_points,aqgc_histos,fake_muons,fake_electrons,sm_lhe_weight,backgrounds_info,fake):
    #signal["hist_central"].Write()

    atgcroostats_config=open(cfg["atgcroostats_config_fname"],"w")

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
        aqgc_scaling_hist=TH1D("bin_content_par1_"+str(i),"bin_content_par1_"+str(i),len(oneD_grid_points),histo_min,histo_max);

        for j in range(0,len(oneD_grid_points)):
            assert(aqgc_histos[sm_lhe_weight].GetBinContent(i) > 0)

            aqgc_scaling_hist.SetBinContent(aqgc_scaling_hist.GetXaxis().FindFixBin(oneD_grid_points[j]), aqgc_histos[j].GetBinContent(i)/aqgc_histos[sm_lhe_weight].GetBinContent(i))
        
        aqgc_outfile.cd()
        aqgc_scaling_hist.Write()    

    for i in range(1,aqgc_histos[sm_lhe_weight].GetNbinsX()+1):

        print ""
        for j in range(0,len(oneD_grid_points)):
            print 1+aqgc_histos[j].GetBinError(i)/aqgc_histos[j].GetBinContent(i)


        dcard = open(cfg["datacard_base"] + "_bin"+str(i)+".txt",'w')

        print >> dcard, "imax 1 number of channels"
        print >> dcard, "jmax * number of background"
        print >> dcard, "kmax * number of nuisance parameters"
        print >> dcard, "Observation 0"
        dcard.write("bin")
        dcard.write(" bin1")
        
        for background in backgrounds:
            dcard.write(" bin1")

        dcard.write(" bin1")    
        dcard.write('\n')    
        
        dcard.write("process")
        dcard.write(" WWjj")
        
        for background_info in backgrounds_info:
            dcard.write(" " + background_info[1])

        dcard.write(" fake")
        dcard.write('\n')    
        dcard.write("process")
        dcard.write(" 0")
        
        for j in range(1,len(backgrounds)+2):
            dcard.write(" " + str(j))
        dcard.write('\n')    
        dcard.write('rate')
        dcard.write(' '+str(aqgc_histos[sm_lhe_weight].GetBinContent(i)))
        for background in backgrounds:
            dcard.write(" "+ str(background["hist_central"].GetBinContent(i)))
        dcard.write(" "+str(fake["hist_central"].GetBinContent(i)))    
        dcard.write('\n')    

        
        #print >> dcard, "process WWjj background"
        #print >> dcard, "process 0 1"
        bkg_yield=max(hist_sum_background.GetBinContent(i),0.001)
        #print >> dcard, "rate "+str(reweighted["hist_central"].GetBinContent(i))+" "+str(bkg_yield)

        dcard.write("lumi_13tev lnN")

        dcard.write(" 1.027")

        for background in backgrounds:
            dcard.write(" 1.027")

        dcard.write(" 1.027")

        dcard.write('\n')    

        if aqgc_histos[sm_lhe_weight].GetBinContent(i) > 0:
            dcard.write("mcstat_dim8 lnN "+str(1+aqgc_histos[sm_lhe_weight].GetBinError(i)/aqgc_histos[sm_lhe_weight].GetBinContent(i)))
            for j in range(0,len(backgrounds)):
                dcard.write(" -")

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

                dcard.write(" -")        

                dcard.write('\n')        

        if fake["hist_central"].GetBinContent(i) > 0:

            dcard.write("fake lnN -")

            for j in range(0,len(backgrounds)):
                dcard.write(" -")

            dcard.write(" " + str(1+fake["hist_central"].GetBinError(i)/fake["hist_central"].GetBinContent(i)))            

            dcard.write('\n')
        #print >> dcard, "lumi_8tev lnN 1.027 1.027"    

    outfile=TFile(cfg["outfile"],"recreate")

    outfile.cd()

    for i in range(0,len(backgrounds)):
        down=backgrounds[i]["hist_central"].Clone("mcstat_"+backgrounds_info[i][1]+"Down")
        up=backgrounds[i]["hist_central"].Clone("mcstat_"+backgrounds_info[i][1]+"Up")
        
        for j in range(1,backgrounds[i]["hist_central"].GetNbinsX()+1):
            down.SetBinContent(j,max(down.GetBinContent(j) - down.GetBinError(j),0))
            up.SetBinContent(j,up.GetBinContent(j) + up.GetBinError(j))
            
        backgrounds[i]["hist_central"].Clone(backgrounds_info[i][1]).Write()
        down.Write()
        up.Write()


    down=fake["hist_central"].Clone("fakeDown")
    up=fake["hist_central"].Clone("fakeUp")
        
    for j in range(1,fake["hist_central"].GetNbinsX()+1):
        down.SetBinContent(j,max(down.GetBinContent(j) - down.GetBinError(j),0))
        up.SetBinContent(j,up.GetBinContent(j) + up.GetBinError(j))
            
    down.Write()
    up.Write()
    fake["hist_central"].Clone("fake").Write()

    down=aqgc_histos[sm_lhe_weight].Clone("mcstat_dibosonDown")
    up=aqgc_histos[sm_lhe_weight].Clone("mcstat_dibosonUp")

    for j in range(1,aqgc_histos[sm_lhe_weight].GetNbinsX()+1):
        down.SetBinContent(j,max(down.GetBinContent(j) - down.GetBinError(j),0))
        up.SetBinContent(j,up.GetBinContent(j) + up.GetBinError(j))

    down.Write()
    up.Write()
    aqgc_histos[sm_lhe_weight].Clone("diboson").Write()

    aqgc_histos[sm_lhe_weight].Clone("data_obs").Write()

    #for i in range(0,len(aqgc_histos)):
    #    aqgc_histos[i].Write()        

    atgcroostats_config.write("[Global]\n")
    atgcroostats_config.write("model=par1_TH1\n")
    atgcroostats_config.write("par1Name = par1\n")
    atgcroostats_config.write("par1Low = "+str(grid_min)+"\n")
    atgcroostats_config.write("par1High = "+str(grid_max)+"\n")
    atgcroostats_config.write("NlnN=1\n")
    atgcroostats_config.write("lnN1_name=lumi_13TeV\n")
    atgcroostats_config.write("lnN1_value=")
    atgcroostats_config.write("1.027,")
    for i in range(0,len(backgrounds_info)):
        atgcroostats_config.write("1.027,")
    atgcroostats_config.write("1.027")            
    atgcroostats_config.write("\n")
    atgcroostats_config.write("lnN1_for=channel1_signal,")
    for i in range(0,len(backgrounds_info)):
        atgcroostats_config.write("channel1_"+str(backgrounds_info[i][1]+","))
    atgcroostats_config.write("channel1_fake")            
    atgcroostats_config.write("\n")            
    #atgcroostats_config.write("lnN1_value=1.026,1.026,1.026,1.026\n")
    #atgcroostats_config.write("lnN1_for=channel1_signal,channel1_wzjj,channel1_wgjets,channel1_fake\n")
    #atgcroostats_config.write("lnN1_value=1.026,1.026,1.026\n")
    #atgcroostats_config.write("lnN1_for=channel1_signal,channel1_wzjj,channel1_wgjets\n")
    atgcroostats_config.write("\n")
    atgcroostats_config.write("[channel1]\n")
    #atgcroostats_config.write("Nbkg=2\n")
    atgcroostats_config.write("Nbkg="+str(len(backgrounds_info)+1)+"\n")
    for i in range(0,len(backgrounds_info)):
        atgcroostats_config.write("bkg"+str(i+1)+"_name="+str(backgrounds_info[i][1])+"\n")
        atgcroostats_config.write("bkg"+str(i+1)+"_shape_syst=mcstat_"+backgrounds_info[i][1]+"\n")
        
    atgcroostats_config.write("bkg"+str(len(backgrounds_info)+1)+"_name=fake\n")
    atgcroostats_config.write("bkg"+str(len(backgrounds_info)+1)+"_shape_syst=fake\n")

    atgcroostats_config.write("signal_shape_syst=mcstat_diboson\n")

    
    #atgcroostats_config.write("bkg1_name=wzjj\n")
    #atgcroostats_config.write("bkg2_name=wgjets\n")
    #atgcroostats_config.write("bkg3_name=fake\n")

def write_gm():

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

        dcard.write(" 1.025")

        for background in backgrounds:
            dcard.write(" 1.025")

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

            #for the fake background
            dcard.write(" -")

            dcard.write('\n')        

        #print >> dcard, "lumi_8tev lnN 1.024 1.024"    

def write_sm_mc_fake(cfg,hist,hist_signal,hist_background,plots,backgrounds,backgrounds_info,signal,signal_info,fake_muons,fake_electrons,fake,data):
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

    for i in range(0,len(signal["cutflow_histograms"])):
        signal["cutflow_histograms"][i].Clone("signal_cut"+str(i)).Write()

    for process in plots.keys():
        for variable in plots[process].keys():
            plots[process][variable].Clone(str(process)+"_"+str(variable)).Write()
        
    for i in range(0,len(backgrounds)):
        if "cutflow_histograms" in backgrounds[i]:
            for j in range(0,len(signal["cutflow_histograms"])):
                backgrounds[i]["cutflow_histograms"][j].Clone(backgrounds_info[i][1]+"_cut"+str(j)).Write()

    for i in range(0,len(fake["cutflow_histograms"])):
        fake["cutflow_histograms"][i].Clone("fake_cut"+str(i)).Write()

    #for i in range(0,len(backgrounds[1]["cutflow_histograms"])):
    #    backgrounds[1]["cutflow_histograms"][i].Clone().Write()


    hist_stack_background = THStack()
    hist_sum_background = hist.Clone("background_sum")

    for i in range(0,len(backgrounds)):
        backgrounds[i]["hist_central"].Clone(backgrounds_info[i][1]).Write()
        hist_stack_background.Add(backgrounds[i]["hist_central"])
        hist_sum_background.Add(backgrounds[i]["hist_central"])

    signal["hist_central"].Clone("wpwpjjewk").Write()

    if cfg["mode"] == "sm_mc_fake":
        fake["hist_central"].Clone("fake").Write()

    if cfg["blind_high_mjj"] == False:
        data["hist_central"].Clone("data").Write()

    hist_stack_background.Write()

    hist_sum_background.Write()

    fake_muons.Clone("fake_muons").Write()
    fake_electrons.Clone("fake_electrons").Write()

    if cfg["significance_variable"] == "mllmjj":
        for ix in range(1,signal["hist_central"].GetNbinsX()+1):
            for iy in range(1,signal["hist_central"].GetNbinsY()+1):            

                dcard = open(cfg["datacard_base"] + "_xbin"+str(ix)+"_ybin"+str(iy)+".txt",'w')

                print >> dcard, "imax 1 number of channels"
                print >> dcard, "jmax * number of background"
                print >> dcard, "kmax * number of nuisance parameters"

                if cfg["blind_high_mjj"] == False:
                    print >> dcard, "Observation "+str(data["hist_central"].GetBinContent(ix,iy))
                else:
                    print >> dcard, "Observation 0"
                dcard.write("bin")
                dcard.write(" bin1")
        
                for background in backgrounds:
                    dcard.write(" bin1")

                if cfg["mode"] == "sm_mc_fake":
                    dcard.write(" bin1")
            
                dcard.write('\n')    
        
                dcard.write("process")
                dcard.write(" WWjj")
        
                for background_info in backgrounds_info:
                    dcard.write(" " + background_info[1])

                if cfg["mode"] == "sm_mc_fake":
                    dcard.write(" fake")

            
                dcard.write('\n')    
                dcard.write("process")
                dcard.write(" 0")
        
                for j in range(1,len(backgrounds)+1):
                    dcard.write(" " + str(j))
            
                if cfg["mode"] == "sm_mc_fake":
                    dcard.write(" " + str(len(backgrounds)+1))
            
                dcard.write('\n')    
                dcard.write('rate')
                dcard.write(' '+str(signal["hist_central"].GetBinContent(ix,iy)))
                for background in backgrounds:
                    dcard.write(" "+ str(background["hist_central"].GetBinContent(ix,iy)))

                if cfg["mode"] == "sm_mc_fake":    
                    dcard.write(" " + str(fake["hist_central"].GetBinContent(ix,iy)))
            
                dcard.write('\n')    

        
        #print >> dcard, "process WWjj WWqcd ttbar"
        #print >> dcard, "process 0 1"
                bkg_yield=max(hist_sum_background.GetBinContent(ix,ix),0.001)
        #print >> dcard, "rate "+str(signal["hist_central"].GetBinContent(i))+" "+str(bkg_yield)

                dcard.write("lumi lnN")

                dcard.write(" 1.025")

                for background in backgrounds:
                    dcard.write(" 1.025")

                if cfg["mode"] == "sm_mc_fake":
                    dcard.write(" -")

                dcard.write('\n')    

                dcard.write("electron_efficiency_SF lnN")

                dcard.write(" 1.02")

                for background in backgrounds:
                    dcard.write(" 1.02")

                if cfg["mode"] == "sm_mc_fake":
                    dcard.write(" -")                    

                dcard.write('\n')

                dcard.write("muon_efficiency_SF lnN")

                dcard.write(" 1.02")

                for background in backgrounds:
                    dcard.write(" 1.02")

                if cfg["mode"] == "sm_mc_fake":
                    dcard.write(" -")                    

                dcard.write('\n')                    

                dcard.write("muon_energy_scale lnN")

                dcard.write(" 1.01")

                for background in backgrounds:
                    dcard.write(" 1.01")

                if cfg["mode"] == "sm_mc_fake":
                    dcard.write(" -")                    

                dcard.write('\n')                    

                dcard.write("electron_energy_scale lnN")

                dcard.write(" 1.01")

                for background in backgrounds:
                    dcard.write(" 1.01")

                if cfg["mode"] == "sm_mc_fake":
                    dcard.write(" -")                    

                dcard.write('\n')                    

                dcard.write("fake_sys lnN")

                dcard.write(" -")

                for background in backgrounds:
                    dcard.write(" -")

                if cfg["mode"] == "sm_mc_fake":
                    dcard.write(" 1.3")            

                dcard.write('\n')    

                if signal["hist_central"].GetBinContent(ix,iy) > 0:
                    dcard.write("mcstat_signal lnN "+str(1+signal["hist_central"].GetBinError(ix,iy)/signal["hist_central"].GetBinContent(ix,iy)))
                    for j in range(0,len(backgrounds)):
                        dcard.write(" -")
                
                    if cfg["mode"] == "sm_mc_fake":
                        dcard.write(" -")
                
                    dcard.write("\n")    
            
        
                for j in range(0,len(backgrounds)):
                    if backgrounds[j]["hist_central"].GetBinContent(ix,iy) > 0:
                        dcard.write("mcstat_"+backgrounds_info[j][1]+"_xbin_"+str(ix)+"_ybin"+str(iy)+" lnN -")
                        for k in range(0,len(backgrounds)):
                            if j != k:
                                dcard.write(" -")
                            else:    
                                dcard.write(" " + str(1+backgrounds[j]["hist_central"].GetBinError(ix,iy)/backgrounds[j]["hist_central"].GetBinContent(ix,iy)))

                        if cfg["mode"] == "sm_mc_fake":
                            dcard.write(" -")
                        
                        dcard.write('\n')        

                if cfg["mode"] == "sm_mc_fake" and fake["hist_central"].GetBinContent(ix,iy) < 0:
                    print "warning, fake lepton estimate less than 0 in xbin "+str(ix)+" ybin "+str(iy)+": "+ str(fake["hist_central"].GetBinContent(ix,iy))+ " +/- " + str(fake["hist_central"].GetBinError(ix,iy))
                    

                if cfg["mode"] == "sm_mc_fake" and fake["hist_central"].GetBinContent(ix,iy) != 0:

                    dcard.write("fake_stat_xbin"+str(ix)+"_ybin"+str(iy)+" lnN -")

                    for j in range(0,len(backgrounds)):
                        dcard.write(" -")

                    dcard.write(" " + str(1+fake["hist_central"].GetBinError(ix,iy)/fake["hist_central"].GetBinContent(ix,iy)))

                    dcard.write('\n')

                at_least_one_syscalc=False        
                for j in range(0,len(backgrounds)):
                    if backgrounds[j]["hist_central"].GetBinContent(ix,iy) > 0 and backgrounds_info[j][2] == "syscalc":
                        at_least_one_syscalc=True

                if signal_info[2] == "syscalc" and signal["hist_central"].GetBinContent(ix,iy) > 0:
                    at_least_one_syscalc = True


                if at_least_one_syscalc:
                    dcard.write("pdf lnN")


                    if signal_info[2] == "syscalc" and signal["hist_central"].GetBinContent(ix,iy) > 0:
                        dcard.write(" "+str(signal["hist_pdf_up"].GetBinContent(ix,iy)/signal["hist_central"].GetBinContent(ix,iy)))
                    else:
                        dcard.write(" -")
            
                    for j in range(0,len(backgrounds)):
                        if backgrounds[j]["hist_central"].GetBinContent(ix,iy) > 0 and backgrounds_info[j][2] == "syscalc":
                            dcard.write(" "+str(backgrounds[j]["hist_pdf_up"].GetBinContent(ix,iy)/backgrounds[j]["hist_central"].GetBinContent(ix,iy)))
                        else:
                            dcard.write(" -")

            #for the fake background
                    dcard.write(" -")

                    dcard.write('\n')        

                    dcard.write("qcd_scale lnN")

                    if signal_info[2] == "syscalc" and signal["hist_central"].GetBinContent(ix,iy) > 0:
                        dcard.write(" "+str(signal["hist_qcd_down"].GetBinContent(ix,iy)/signal["hist_central"].GetBinContent(ix,iy)) +"/"+str(signal["hist_qcd_up"].GetBinContent(ix,iy)/signal["hist_central"].GetBinContent(ix,iy)))
                    else:
                        dcard.write(" -")

                    for j in range(0,len(backgrounds)):
                        if backgrounds[j]["hist_central"].GetBinContent(ix,iy) > 0 and backgrounds_info[j][2] == "syscalc":
                            dcard.write(" "+str(backgrounds[j]["hist_qcd_down"].GetBinContent(ix,iy)/backgrounds[j]["hist_central"].GetBinContent(ix,iy)) +"/"+str(backgrounds[j]["hist_qcd_up"].GetBinContent(ix,iy)/backgrounds[j]["hist_central"].GetBinContent(ix,iy)))
                        else:
                            dcard.write(" -")
                    
            #for the fake background
                    dcard.write(" -")

                    dcard.write('\n')        

        return

    for i in range(1,signal["hist_central"].GetNbinsX()+1):

        dcard = open(cfg["datacard_base"] + "_bin"+str(i)+".txt",'w')

        print >> dcard, "imax 1 number of channels"
        print >> dcard, "jmax * number of background"
        print >> dcard, "kmax * number of nuisance parameters"

        if cfg["blind_high_mjj"] == False:
            print >> dcard, "Observation "+str(data["hist_central"].GetBinContent(i))
        else:
            print >> dcard, "Observation 0"
        dcard.write("bin")
        dcard.write(" bin1")
        
        for background in backgrounds:
            dcard.write(" bin1")

        if cfg["mode"] == "sm_mc_fake":
            dcard.write(" bin1")
            
        dcard.write('\n')    
        
        dcard.write("process")
        dcard.write(" WWjj")
        
        for background_info in backgrounds_info:
            dcard.write(" " + background_info[1])

        if cfg["mode"] == "sm_mc_fake":
            dcard.write(" fake")

            
        dcard.write('\n')    
        dcard.write("process")
        dcard.write(" 0")
        
        for j in range(1,len(backgrounds)+1):
            dcard.write(" " + str(j))
            
        if cfg["mode"] == "sm_mc_fake":
            dcard.write(" " + str(len(backgrounds)+1))
            
        dcard.write('\n')    
        dcard.write('rate')
        dcard.write(' '+str(signal["hist_central"].GetBinContent(i)))
        for background in backgrounds:
            dcard.write(" "+ str(background["hist_central"].GetBinContent(i)))

        if cfg["mode"] == "sm_mc_fake":    
            dcard.write(" " + str(fake["hist_central"].GetBinContent(i)))
            
        dcard.write('\n')    

        
        #print >> dcard, "process WWjj WWqcd ttbar"
        #print >> dcard, "process 0 1"
        bkg_yield=max(hist_sum_background.GetBinContent(i),0.001)
        #print >> dcard, "rate "+str(signal["hist_central"].GetBinContent(i))+" "+str(bkg_yield)

        dcard.write("lumi_13tev lnN")

        dcard.write(" 1.025")

        for background in backgrounds:
            dcard.write(" 1.025")

        if cfg["mode"] == "sm_mc_fake":
            dcard.write(" 1.025")

        dcard.write('\n')    

        dcard.write("fake_sys lnN")

        dcard.write(" -")

        for background in backgrounds:
            dcard.write(" -")

        if cfg["mode"] == "sm_mc_fake":
            dcard.write(" 1.3")            

        dcard.write('\n')    

        if signal["hist_central"].GetBinContent(i) > 0:
            dcard.write("mcstat_signal lnN "+str(1+signal["hist_central"].GetBinError(i)/signal["hist_central"].GetBinContent(i)))
            for j in range(0,len(backgrounds)):
                dcard.write(" -")
                
            if cfg["mode"] == "sm_mc_fake":
                dcard.write(" -")
                
            dcard.write("\n")    
            
        
        for j in range(0,len(backgrounds)):
            if backgrounds[j]["hist_central"].GetBinContent(i) > 0:
                dcard.write("mcstat_"+backgrounds_info[j][1]+"_bin_"+str(i)+" lnN -")
                for k in range(0,len(backgrounds)):
                    if j != k:
                        dcard.write(" -")
                    else:    
                        dcard.write(" " + str(1+backgrounds[j]["hist_central"].GetBinError(i)/backgrounds[j]["hist_central"].GetBinContent(i)))

                if cfg["mode"] == "sm_mc_fake":
                    dcard.write(" -")
                        
                dcard.write('\n')        

        if cfg["mode"] == "sm_mc_fake" and fake["hist_central"].GetBinContent(i) > 0:

            dcard.write("fake_stat_bin"+str(i)+" lnN -")

            for j in range(0,len(backgrounds)):
                dcard.write(" -")

            dcard.write(" " + str(1+fake["hist_central"].GetBinError(i)/fake["hist_central"].GetBinContent(i)))

            dcard.write('\n')

        at_least_one_syscalc=False        
        for j in range(0,len(backgrounds)):
            if backgrounds[j]["hist_central"].GetBinContent(i) > 0 and backgrounds_info[j][2] == "syscalc":
                at_least_one_syscalc=True

        if signal_info[2] == "syscalc":
            at_least_one_syscalc = True


        if at_least_one_syscalc:
            dcard.write("pdf lnN")


            if signal_info[2] == "syscalc":
                dcard.write(" "+str(signal["hist_pdf_up"].GetBinContent(i)/signal["hist_central"].GetBinContent(i)))
            else:
                dcard.write(" -")
            
            for j in range(0,len(backgrounds)):
                if backgrounds[j]["hist_central"].GetBinContent(i) > 0 and backgrounds_info[j][2] == "syscalc":
                    dcard.write(" "+str(backgrounds[j]["hist_pdf_up"].GetBinContent(i)/backgrounds[j]["hist_central"].GetBinContent(i)))
                else:
                    dcard.write(" -")

            #for the fake background
            dcard.write(" -")

            dcard.write('\n')        

            dcard.write("qcd_scale lnN")

            if signal_info[2] == "syscalc":
                dcard.write(" "+str(signal["hist_qcd_down"].GetBinContent(i)/signal["hist_central"].GetBinContent(i)) +"/"+str(signal["hist_qcd_up"].GetBinContent(i)/signal["hist_central"].GetBinContent(i)))
            else:
                dcard.write(" -")

            for j in range(0,len(backgrounds)):
                if backgrounds[j]["hist_central"].GetBinContent(i) > 0 and backgrounds_info[j][2] == "syscalc":
                    dcard.write(" "+str(backgrounds[j]["hist_qcd_down"].GetBinContent(i)/backgrounds[j]["hist_central"].GetBinContent(i)) +"/"+str(backgrounds[j]["hist_qcd_up"].GetBinContent(i)/backgrounds[j]["hist_central"].GetBinContent(i)))
                else:
                    dcard.write(" -")
                    
            #for the fake background
            dcard.write(" -")

            dcard.write('\n')        

        #print >> dcard, "lumi_8tev lnN 1.024 1.024"    

def write_sm_low_mjj_control_region(cfg,hist,hist_background,backgrounds,backgrounds_info,fake_muons,fake_electrons,fake,data):

    hist_background.SetLineWidth(3)

    hist_background.SetLineColor(kBlue)

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

    data["hist_central"].Clone("data").Write()

    fake["hist_central"].Clone("fake").Write()

    fake_electrons.Clone("fake_electrons").Write()

    fake_muons.Clone("fake_muons").Write()

    hist_stack_background.Write()

    hist_sum_background.Write()

def write_fr_closure_test(cfg,ttbar,ttbar_qcd_fr):

    outfile=TFile(cfg["outfile"],"recreate")

    outfile.cd()
    
    ttbar["hist_central"].Clone("ttbar").Write()

    print ttbar_qcd_fr
    
    ttbar_qcd_fr["hist_central"].Clone("ttbar_qcd_fr").Write()

def write_produce_histograms(cfg,hist,mc_samples,mc_samples_info,fake_samples, data_samples,fakeratemc_samples,plots):
    outfile=TFile(cfg["outfile"],"recreate")

    outfile.cd()

    for process in plots.keys():
        for variable in plots[process].keys():
            plots[process][variable].Clone(str(process)+"_"+str(variable)).Write()

    for i in range(0,len(fakeratemc_samples)):

        if "cutflow_histograms" in fakeratemc_samples[i]:
            for j in range(0,len(fakeratemc_samples[i]["cutflow_histograms"])):
                fakeratemc_samples[i]["cutflow_histograms"][j].Clone("fakeratemc_sample"+str(i)+"_cut"+str(j)).Write()

    for i in range(0,len(mc_samples)):
        if "cutflow_histograms" in mc_samples[i]:
            for j in range(0,len(mc_samples[i]["cutflow_histograms"])):
                mc_samples[i]["cutflow_histograms"][j].Clone(mc_samples_info[i][1]+"_cut"+str(j)).Write()

    for i in range(0,len(fake_samples)):
        if "cutflow_histograms" in fake_samples[i]:
            for j in range(0,len(fake_samples[i]["cutflow_histograms"])):
                fake_samples[i]["cutflow_histograms"][j].Clone("fake_sample" + str(i) + "_cut"+str(j)).Write()

    for i in range(0,len(data_samples)):
        if "cutflow_histograms" in data_samples[i]:
            for j in range(0,len(data_samples[i]["cutflow_histograms"])):
                data_samples[i]["cutflow_histograms"][j].Clone("data_sample" + str(i) + "_cut"+str(j)).Write()                
