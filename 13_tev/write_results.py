from ROOT import *

def write_reweighted_mode_v1(cfg,hist,backgrounds, oneD_grid_points,aqgc_histos,fake_muons,fake_electrons,sm_lhe_weight,backgrounds_info,fake):
    #signal["hist_central"].Write()

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

        dcard.write(" 1.024")

        for background in backgrounds:
            dcard.write(" 1.024")

        dcard.write(" 1.024")

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
        #print >> dcard, "lumi_8tev lnN 1.024 1.024"    

    outfile=TFile(cfg["outfile"],"recreate")

    outfile.cd()

    for background in backgrounds:
        background["hist_central"].Write()

    for i in range(0,len(aqgc_histos)):
        aqgc_histos[i].Write()


def write_reweighted_mode_v2(cfg,hist,backgrounds, oneD_grid_points,aqgc_histos,fake_muons,fake_electrons,sm_lhe_weight,backgrounds_info,fake):
    #signal["hist_central"].Write()

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

        dcard.write(" 1.024")

        for background in backgrounds:
            dcard.write(" 1.024")

        dcard.write(" 1.024")

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
        #print >> dcard, "lumi_8tev lnN 1.024 1.024"    

    outfile=TFile(cfg["outfile"],"recreate")

    outfile.cd()

    for i in range(0,len(backgrounds)):
        backgrounds[i]["hist_central"].Clone(backgrounds_info[i][1]).Write()

    aqgc_histos[sm_lhe_weight].Clone("diboson").Write()
    aqgc_histos[sm_lhe_weight].Clone("data_obs").Write()

    #for i in range(0,len(aqgc_histos)):
    #    aqgc_histos[i].Write()        

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

def write_sm_mc_fake(cfg,hist,hist_signal,hist_background,backgrounds,backgrounds_info,signal,fake_muons,fake_electrons,fake):
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

    signal["hist_central"].Clone("wpwpjjewkqcd").Write()


    if cfg["mode"] == "sm_mc_fake":
        fake["hist_central"].Clone("fake").Write()

    hist_stack_background.Write()

    hist_sum_background.Write()

    fake_muons.Clone("fake_muons").Write()
    fake_electrons.Clone("fake_electrons").Write()

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
            dcard.write(" " + str(len(backgrounds)))
            
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

        dcard.write(" 1.024")

        for background in backgrounds:
            dcard.write(" 1.024")

        if cfg["mode"] == "sm_mc_fake":
            dcard.write(" 1.024")

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
                dcard.write("mcstat_"+backgrounds_info[j][1]+" lnN -")
                for k in range(0,len(backgrounds)):
                    if j != k:
                        dcard.write(" -")
                    else:    
                        dcard.write(" " + str(1+backgrounds[j]["hist_central"].GetBinError(i)/backgrounds[j]["hist_central"].GetBinContent(i)))

                if cfg["mode"] == "sm_mc_fake":
                    dcard.write(" -")
                        
                dcard.write('\n')        

        if cfg["mode"] == "sm_mc_fake" and fake["hist_central"].GetBinContent(i) > 0:        

            dcard.write("stat_fake lnN -")

            for j in range(0,len(backgrounds)):
                dcard.write(" -")

            dcard.write(" " + str(1+fake["hist_central"].GetBinError(i)/fake["hist_central"].GetBinContent(i)))    

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

def write_sm_low_mjj_control_region(cfg,hist,hist_signal,hist_background,backgrounds,backgrounds_info,signal,fake_muons,fake_electrons,fake,data):

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

    signal["hist_central"].Clone("wpwpjjewkqcd").Write()

    data["hist_central"].Clone("data").Write()

    fake["hist_central"].Clone("fake").Write()

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

