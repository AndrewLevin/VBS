import selection

import parse_reweight_info

from ROOT import *

from array import array

#gStyle.SetOptStat(0)
gROOT.ProcessLine('#include "/afs/cern.ch/work/a/anlevin/cmssw/CMSSW_8_0_20/src/ntuple_maker/ntuple_maker/interface/enum_definition.h"')

#fr_file=TFile("/home/anlevin/VBS/fake_leptons/frs_v12.root")

#which cuts must be passed for the event to pass the selection

pass_mask =  (1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (1 << 4) | (1 << 5) | (1 << 6) | (1 << 7) | (1 << 8) | (1 << 9) | (1 << 10) | (1 << 11) | (1 << 12) | (1 << 13) | (1 << 14) | (1 << 15) | (1 << 16) | (1 << 17)

pass_mask_w_o_lepton_ids =   (1 << 1) | (1 << 2) | (1 << 3) | (1 << 4) | (1 << 5) | (1 << 6) | (1 << 7) | (1 << 8) | (1 << 9) | (1 << 10) | (1 << 11) | (1 << 12) | (1 << 13) | (1 << 14) | (1 << 15) | (1 << 16) | (1 << 17)

lep2_tight_electron_mask = Lep2TightSelectionV5
lep1_tight_electron_mask = Lep1TightSelectionV5

#lep1_loose_muon_mask = Lep1LooseSelectionV4
#lep2_loose_muon_mask = Lep2LooseSelectionV4

#lep1_loose_muon_mask = Lep1LooseSelectionV4 | Lep2LooseSelectionV5
#lep2_loose_muon_mask = Lep2LooseSelectionV4 | Lep2LooseSelectionV5
lep1_loose_muon_mask = Lep2LooseSelectionV5
lep2_loose_muon_mask = Lep2LooseSelectionV5

lep1_tight_muon_mask = Lep1TightSelectionV1
lep2_tight_muon_mask = Lep2TightSelectionV1

lep1_loose_electron_mask = Lep1LooseSelectionV2
lep2_loose_electron_mask = Lep2LooseSelectionV2

#these will be initialized later
#muon_fr_hist=None
#electron_fr_hist=None
        
def muonfakerate(eta,pt,syst):

    myeta  = min(abs(eta),2.4999)
    mypt   = min(pt,69.999)

    etabin = muon_fr_hist.GetXaxis().FindFixBin(myeta)
    ptbin = muon_fr_hist.GetYaxis().FindFixBin(mypt)

    prob = muon_fr_hist.GetBinContent(etabin,ptbin)

    if syst == "up":
        prob+=muon_fr_hist.GetBinError(etabin,ptbin)
    elif syst == "down":
        prob-=muon_fr_hist.GetBinError(etabin,ptbin)
    else:
        if syst != "nominal":
            sys.exit(0)

    return prob/(1-prob)

def electronfakerate(eta,pt,syst):

    myeta  = min(abs(eta),2.4999)
    mypt   = min(pt,34.999)

    etabin = electron_fr_hist.GetXaxis().FindFixBin(myeta)
    ptbin = electron_fr_hist.GetYaxis().FindFixBin(mypt)

    prob = electron_fr_hist.GetBinContent(etabin,ptbin)

    if syst == "up":
        prob+=electron_fr_hist.GetBinError(etabin,ptbin)
    elif syst == "down":
        prob-=electron_fr_hist.GetBinError(etabin,ptbin)
    else:
        if syst != "nominal":
            sys.exit(0)

    return prob/(1-prob)


def getVariable(cfg,t):
    if cfg["variable"] == "mjj":
        return (t.jet1+t.jet2).M()
    elif cfg["variable"] == "mll":
        return (t.lep1+t.lep2).M()
    elif cfg["variable"] == "met":
        return t.metpt
    elif cfg["variable"] == "detajj":
        return abs(t.jet1.Eta() - t.jet2.Eta())
    elif cfg["variable"] == "maxbtagevent":
        return t.maxbtagevent
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

import json

f_json=open("/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON.txt")

#f_json = open("/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-258714_13TeV_PromptReco_Collisions15_25ns_JSON.txt")

#f_json=open("/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-259891_13TeV_PromptReco_Collisions15_25ns_JSON.txt")

good_run_lumis=json.loads(f_json.read())

def pass_json(run,lumi):

    if str(run) not in good_run_lumis.keys():
        return False

    for lumi_pair in good_run_lumis[str(run)]:
        if lumi <= lumi_pair[1] and lumi >= lumi_pair[0]:
            return True

    return False    

f_pu_weights = TFile("/afs/cern.ch/work/a/anlevin/VBS/13_tev/pileup_weights.root")

pu_weight_hist = f_pu_weights.Get("pileup_weights")

def fill_histograms_cut_mask(histograms,var, weight, mask):

    for i in range(0,len(histograms)):
        partial_pass_mask = 1
        for j in range(1,i+1):
            partial_pass_mask = partial_pass_mask | 1 << j

        if partial_pass_mask & mask == partial_pass_mask:
            
            histograms[i].Fill(var, weight)


def fillHistogram(cfg,t,hist,use_lhe_weight = False,is_data=False, syscalc=False, fill_cutflow_histograms = False,debug = False):

    print "t.GetEntries() = " + str(t.GetEntries())

    return_hist = hist.Clone()

    ncuts = 18
    cutflow_histograms = []
    for i in range(0,18):
        cutflow_histograms.append(hist.Clone())

    if syscalc:

        #return_hist_central = hist.Clone()
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

#        if t.event != 307072356:
#            continue

        #if is_data:
        #    if not pass_json(t.run,t.lumi):
        #        continue

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

        [p,mask] = selection.passSelectionExceptLeptonIDs(t,cfg)

        if cfg["which_selection"] == "relaxed" or cfg["which_selection"] == "relaxed_btagged":
            #in this case the mask has useless information
            p = True
            if not selection.passRelaxedSelectionExceptLeptonIDs(t,cfg):
                p = False
                continue

        pass_lepton_ids = True

        if abs(t.lep1id) == 13:
            if not bool(t.lepton_selection_flags & lep1_tight_muon_mask):
                pass_lepton_ids = False
        else:
            if not bool(t.lepton_selection_flags & lep1_tight_electron_mask):
                pass_lepton_ids = False
        if abs(t.lep2id) == 13:
            if not bool(t.lepton_selection_flags & lep2_tight_muon_mask):
                pass_lepton_ids = False
        else:
            if not bool(t.lepton_selection_flags & lep2_tight_electron_mask):
                pass_lepton_ids = False

        if pass_lepton_ids:
            mask = mask | (1 << 0)
        else:
            p = False

        #mask = mask | (1 << 0)

        if p and debug:
            print "eventNum lumiNum runNum " +str(t.event)+" "+str(t.lumi)+" "+str(t.run)

        if is_data:
            w = 1
        else:
            w=t.xsWeight*float(cfg["lumi"])

            if t.gen_weight < 0:
                w = -w
            #w = w*pu_weight_hist.GetBinContent(pu_weight_hist.FindFixBin(t.n_pu_interactions))

        var=getVariable(cfg,t)

        #if var > 500:
        #    print "["+str(t.event)+","+str(t.lumi)+","+str(t.run)+"],"

        if var > 500 and cfg["variable"] == "mjj" and cfg["blind_high_mjj"] == True:
            continue

        if cfg["mode"] == "non-sm" and use_lhe_weight == True:
            if var > return_hist.GetBinLowEdge(return_hist.GetNbinsX()):
                return_hist.Fill(return_hist.GetBinCenter(return_hist.GetNbinsX()),w*t.lhe_weights[int(options.which_lhe_weight)]/t.lhe_weight_orig)
            else:
                return_hist.Fill(var,w*t.lhe_weights[int(options.which_lhe_weight)]/t.lhe_weight_orig)
        else:

            if var > return_hist.GetBinLowEdge(return_hist.GetNbinsX()):
                fill_histograms_cut_mask(cutflow_histograms,return_hist.GetBinCenter(return_hist.GetNbinsX()),w,mask)                                
                if p:
                    return_hist.Fill(return_hist.GetBinCenter(return_hist.GetNbinsX()),w)
            else:
                fill_histograms_cut_mask(cutflow_histograms,var,w,mask)
                if p:
                    return_hist.Fill(var,w)

        if syscalc:

            for i in range(0,100):
                if var > histos[i].GetBinLowEdge(histos[i].GetNbinsX()):
                    if p:
                        histos[i].Fill(histos[i].GetBinCenter(histos[i].GetNbinsX()),w*t.pdf_weights[i]/t.qcd_pdf_weight_orig)
                else:
                    if p:
                        histos[i].Fill(var,w*t.pdf_weights[i]/t.qcd_pdf_weight_orig)

            if var > return_hist_qcd_up.GetBinLowEdge(return_hist_qcd_up.GetNbinsX()):
                if p:
                    return_hist_qcd_up.Fill(return_hist_qcd_up.GetBinCenter(return_hist_qcd_up.GetNbinsX()),w*t.qcd_weight_mur2muf2/t.qcd_pdf_weight_orig)
            else:
                if p:
                    return_hist_qcd_up.Fill(var,w*t.qcd_weight_mur2muf2/t.qcd_pdf_weight_orig)

            if var > return_hist_qcd_down.GetBinLowEdge(return_hist_qcd_down.GetNbinsX()):
                if p:
                    return_hist_qcd_down.Fill(return_hist_qcd_down.GetBinCenter(return_hist_qcd_down.GetNbinsX()),w*t.qcd_weight_mur0p5muf0p5/t.qcd_pdf_weight_orig)
            else:
                if p:
                    return_hist_qcd_down.Fill(var,w*t.qcd_weight_mur0p5muf0p5/t.qcd_pdf_weight_orig)
    

    if syscalc:
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

            return_hist_pdf_up.SetBinContent(i,return_hist.GetBinContent(i)+stdev)

    if syscalc:
        return {"hist_central" : return_hist , "hist_pdf_up" : return_hist_pdf_up  , "hist_qcd_up" : return_hist_qcd_up, "hist_qcd_down" : return_hist_qcd_down, "cutflow_histograms" : cutflow_histograms }
    else:
        return {"hist_central" : return_hist , "cutflow_histograms" : cutflow_histograms}

def fillHistogramFake(cfg,t,hist,fake_muons,fake_electrons,applying_to_ttbar_mc=False,debug=True):

    fr_file=TFile(cfg["fr_fname"])

    gROOT.cd()

    ncuts = 17
    cutflow_histograms = []
    for i in range(0,17):
        cutflow_histograms.append(hist.Clone())

    #these need to be accessed in the muonfakerate and electronfakerate functions
    global muon_fr_hist
    global electron_fr_hist

    muon_fr_hist=fr_file.Get("muon_frs")
    electron_fr_hist=fr_file.Get("electron_frs")

    if cfg["channel"] == "mm" or cfg["channel"] == "em" or cfg["channel"] == "all":
        muon_fr_max=muon_fr_hist.GetBinContent(muon_fr_hist.GetMaximumBin())

    if cfg["channel"] == "ee" or cfg["channel"] == "em" or cfg["channel"] == "all":
        electron_fr_max=electron_fr_hist.GetBinContent(electron_fr_hist.GetMaximumBin())

    if "electron_fr_max" in vars() and "muon_fr_max" in vars():
        fr_max = max(muon_fr_max,electron_fr_max)
    elif "electron_fr_max" in vars():
        fr_max = electron_fr_max
    elif "muon_fr_max" in vars():
        fr_max = muon_fr_max
    else:
        assert(0)
    
    print fr_max
    
    fake_rate_syst = "nominal"
    print "t.GetEntries() = " + str(t.GetEntries())

    return_hist = hist.Clone()
    
    for entry in range(t.GetEntries()):
        t.GetEntry(entry)

        if entry % 100000 == 0:
            print "entry = " + str(entry)

        #if not pass_json(t.run,t.lumi):
        #    continue

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

        [p,mask] = selection.passSelectionExceptLeptonIDs(t,cfg)

        if cfg["which_selection"] == "relaxed" or cfg["which_selection"] == "relaxed_btagged":
            #in this case the mask has useless information
            p = True
            if not selection.passRelaxedSelectionExceptLeptonIDs(t,cfg):
                p = False

        if abs(t.lep1id) == 13:
            lep1passlooseid = bool((t.lepton_selection_flags & lep1_loose_muon_mask) == lep1_loose_muon_mask)
            lep1passtightid = bool(t.lepton_selection_flags & lep1_tight_muon_mask)
        else:
            lep1passlooseid = bool(t.lepton_selection_flags & lep1_loose_electron_mask)
            lep1passtightid = bool(t.lepton_selection_flags & lep1_tight_electron_mask)
        if abs(t.lep2id) == 13:
            lep2passlooseid = bool((t.lepton_selection_flags & lep2_loose_muon_mask) == lep2_loose_muon_mask)
            lep2passtightid = bool(t.lepton_selection_flags & lep2_tight_muon_mask)
        else:
            lep2passlooseid = bool(t.lepton_selection_flags & lep2_loose_electron_mask)
            lep2passtightid = bool(t.lepton_selection_flags & lep2_tight_electron_mask)

        if applying_to_ttbar_mc:
            w=t.xsWeight*float(cfg["lumi"])
        else:
            w= 1

        var=getVariable(cfg,t)

        if var > 500 and cfg["variable"] == "mjj" and cfg["blind_high_mjj"] == True:
            continue

        if var > return_hist.GetBinLowEdge(return_hist.GetNbinsX()):
            var = return_hist.GetBinCenter(return_hist.GetNbinsX())
        
        loose_but_not_tight=True
        
        if (not lep1passtightid) and lep1passlooseid and lep2passtightid:

            if applying_to_ttbar_mc:
                if t.lep1_matching_real_gen_lepton_pdgid != 0:
                    continue
            
            if abs(t.lep1id) == 13:
                fake_lepton_abs_pdg_id = 13
                muon_corrected_pt = t.lep1.Pt() * (1 + max(0,t.lep1iso - 0.15))
                #muon_corrected_pt = t.lep1.Pt() 
                #print "fake muon event "+str((t.jet1 + t.jet2).mass())+ " "+ str(muon_corrected_pt)+" "+str(t.lep1.Eta())
                w = w * muonfakerate(t.lep1.Eta(), muon_corrected_pt,fake_rate_syst)
            elif abs(t.lep1id) == 11:
                fake_lepton_abs_pdg_id = 11
                #print "fake electron event "+str((t.jet1 + t.jet2).mass())+ " "+ str(t.lep1.Pt())+" "+str(t.lep1.Eta())
                w = w * electronfakerate(t.lep1.Eta(), t.lep1.Pt(),fake_rate_syst)
            else:
                print "unknown lepton flavor"
                sys.exit(0)
        elif lep1passtightid and (not lep2passtightid) and lep2passlooseid:

            if applying_to_ttbar_mc:
                if t.lep2_matching_real_gen_lepton_pdgid != 0:
                    continue

            if abs(t.lep2id) == 13:
                fake_lepton_abs_pdg_id = 13
                muon_corrected_pt = t.lep2.Pt() * (1 + max(0,t.lep2iso - 0.15))
                #muon_corrected_pt = t.lep2.Pt() 
                #print "fake muon event "+str((t.jet1 + t.jet2).mass())+ " "+ str(muon_corrected_pt)+" "+str(t.lep2.Eta())
                w = w * muonfakerate(t.lep2.Eta(), muon_corrected_pt,fake_rate_syst)
            elif abs(t.lep2id) == 11:
                fake_lepton_abs_pdg_id = 11

                #print "fake electron event " +str((t.jet1 + t.jet2).mass())+ " "+ str(t.lep2.Pt())+" "+str(t.lep2.Eta())
                w = w * electronfakerate(t.lep2.Eta(), t.lep2.Pt(),fake_rate_syst)
            else:
                print "unknown lepton flavor"
                sys.exit(0)
        else:
            loose_but_not_tight=False

        if loose_but_not_tight:
            mask = mask | (1 << 0)
        else:
            p=False

        if p and debug:
            print "eventNum lumiNum runNum " +str(t.event)+" "+str(t.lumi)+" "+str(t.run)

        assert(w > 0)

        #if (t.jet1 + t.jet2).mass() > 1100 and (t.jet1 + t.jet2).mass() < 1600:
        #    print t.maxbtagevent
        #    print w

        if cfg["mode"] == "non-sm" and use_lhe_weight == True:
            if var > return_hist.GetBinLowEdge(return_hist.GetNbinsX()):
                return_hist.Fill(return_hist.GetBinCenter(return_hist.GetNbinsX()),w*t.lhe_weights[int(options.which_lhe_weight)]/t.lhe_weight_orig)
            else:
                return_hist.Fill(var,w*t.lhe_weights[int(options.which_lhe_weight)]/t.lhe_weight_orig)
        else:

            if var > return_hist.GetBinLowEdge(return_hist.GetNbinsX()):
                fill_histograms_cut_mask(cutflow_histograms,return_hist.GetBinCenter(return_hist.GetNbinsX()),w,mask)
                if p:

                    assert("fake_lepton_abs_pdg_id" in vars() and fake_lepton_abs_pdg_id != -1)

                    if fake_lepton_abs_pdg_id == 11:
                        fake_electrons.Fill(var)
                    else:
                        fake_muons.Fill(var)                        

                    return_hist.Fill(return_hist.GetBinCenter(return_hist.GetNbinsX()),w)
            else:
                fill_histograms_cut_mask(cutflow_histograms,var,w,mask)
                if p:

                    assert("fake_lepton_abs_pdg_id" in vars() and fake_lepton_abs_pdg_id != -1)
                    
                    if fake_lepton_abs_pdg_id == 11:
                        fake_electrons.Fill(var)
                    else:
                        fake_muons.Fill(var)                        
                
                    return_hist.Fill(var,w)

    return {"hist_central" : return_hist , "cutflow_histograms" : cutflow_histograms}

def fillHistogramsWithReweight(cfg,t,histos,mgreweight_weight_index):
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

        w=t.xsWeight*float(cfg["lumi"])

        [p,mask] = selection.passSelectionExceptLeptonIDs(t,cfg)

        pass_lepton_ids = True

        if abs(t.lep1id) == 13:
            if not bool(t.lepton_selection_flags & lep1_tight_muon_mask):
                pass_lepton_ids = False
        else:
            if not bool(t.lepton_selection_flags & lep1_tight_electron_mask):
                pass_lepton_ids = False
        if abs(t.lep2id) == 13:
            if not bool(t.lepton_selection_flags & lep2_tight_muon_mask):
                pass_lepton_ids = False
        else:
            if not bool(t.lepton_selection_flags & lep2_tight_electron_mask):
                pass_lepton_ids = False

        if pass_lepton_ids:
            mask = mask | (1 << 0)
        else:
            p = False

        var=getVariable(cfg,t)

        for i in range(0,len(mgreweight_weight_index)):
            if var > histos[i].GetBinLowEdge(histos[i].GetNbinsX()):
                if p:
                    histos[i].Fill(histos[i].GetBinCenter(histos[i].GetNbinsX()),w*t.mgreweight_weights[mgreweight_weight_index[i]]/t.lhe_weight_orig)
            else:
                if p:
                    histos[i].Fill(var,w*t.mgreweight_weights[mgreweight_weight_index[i]]/t.lhe_weight_orig)


def fillHistogramWithQCDWeights(cfg,t,histo,qcd_up_histo,qcd_down_histo):
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

        if not selection.passSelection(t,cfg):
            continue

        w=t.xsWeight*float(options.lumi)

        var=getVariable(cfg,t)

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

