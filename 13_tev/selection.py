from ROOT import *

gROOT.ProcessLine('#include "/afs/cern.ch/work/a/anlevin/cmssw/CMSSW_7_4_15/src/ntuple_maker/ntuple_maker/interface/enum_definition.h"')

z_mass = 91.18

def passRelaxedSelectionExceptLeptonIDs(t,cfg):

    p=True

    if t.lep1.pt() < 20:
        p=False

    if t.lep2.pt() < 20:
        p=False

    if t.lep1q != t.lep2q:
        p=False

    if cfg["mode"] == "sm_low_mjj_control_region":    
        if (t.jet1+t.jet2).M() > 500:
            p=False
    elif cfg["mode"] == "fr_closure_test":
        pass
    else:        
        if (t.jet1+t.jet2).M() < 500:
            p=False
        if abs(t.jet1.Eta() - t.jet2.Eta()) < 2.5:
            p=False

    if cfg["which_selection"] == "relaxed":
        if t.maxbtagevent > 0.46:
            p=False
        if (t.flags & WLLJJVetoV5):
            p=False                    
    elif cfg["which_selection"] == "relaxed_btagged":
        if t.maxbtagevent < 0.46:
            p=False        

    if abs(t.jet1.eta()) > 4.7 or abs(t.jet2.eta()) > 4.7:
        p=False

    if t.jet1.pt() < 30:
        p=False

    if t.jet2.pt() < 30:
        p=False                


       
    return p


def passSelectionExceptLeptonIDs(t,cfg):

    p=True

    if t.lep1.pt() < 20:
        p=False

    if t.lep2.pt() < 20:
        p=False

    if abs(t.lep1id) == 11 and abs(t.lep2id) == 11 and abs((t.lep1+t.lep2).mass() - z_mass) < 15:
        p=False

    if (t.lep1+t.lep2).mass() < 50:
        p=False

    if t.metpt < 40:
        p=False        

    if t.lep1q != t.lep2q:
        p=False

    if cfg["mode"] == "sm_low_mjj_control_region":    
        if (t.jet1+t.jet2).M() > 500:
            p=False
    elif cfg["mode"] == "fr_closure_test":
        if cfg["which_selection"] == "full":
            if (t.jet1+t.jet2).M() > 500:
                p=False        
            if abs(t.jet1.Eta() - t.jet2.Eta()) < 2.5:
                p=False
        elif cfg["which_selection"] == "full_novbs":
            pass
        else:
            assert(0)
    else:        
        if (t.jet1+t.jet2).M() < 500:
            p=False
        if abs(t.jet1.Eta() - t.jet2.Eta()) < 2.5:
            p=False


    if t.maxbtagevent > 0.46:
        p=False

    if (t.flags & WLLJJVetoV1):
        p=False

    if (t.flags & WLLJJVetoV2):
        p=False

    #if (t.flags & WLLJJVetoV3):
    #    p=False        

    if (t.flags & WLLJJVetoV5):
        p=False        

    if abs(t.jet1.eta()) > 4.7 or abs(t.jet2.eta()) > 4.7:
        p=False

    if t.jet1.pt() < 30:
        p=False

    if t.jet2.pt() < 30:
        p=False                
        
    return p
