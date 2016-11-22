from ROOT import *

gROOT.ProcessLine('#include "/afs/cern.ch/work/a/anlevin/cmssw/CMSSW_7_4_15/src/ntuple_maker/ntuple_maker/interface/enum_definition.h"')

z_mass = 91.18

def passRelaxedSelectionExceptLeptonIDs(t,cfg):

    p=True

    if t.lep1.pt() < 20:
        p=False

    if t.lep2.pt() < 20:
        p=False

    if (t.lep1+t.lep2).mass() < 4:
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

    mask = 0

    if t.lep1.pt() < 20 or t.lep2.pt() < 20:
        p=False
    else:
        mask = mask | (1 << 1)

    if t.jet1.pt() < 30 or t.jet2.pt() < 30:
        p=False
    else:
        mask = mask | (1 << 2)

    if abs(t.jet1.eta()) > 4.7 or abs(t.jet2.eta()) > 4.7:
        p=False
    else:
        mask = mask | (1 << 3)

    if abs(t.lep1id) == 11 and abs(t.lep2id) == 11 and abs((t.lep1+t.lep2).mass() - z_mass) < 15:
        p=False
    else:
        mask = mask | (1 << 4)

    if (t.lep1+t.lep2).mass() < 50:
        p=False
    else:
        mask = mask | (1 << 5)

    if t.metpt < 40:
        p=False
    else:
        mask = mask | (1 << 6)

    if t.lep1q != t.lep2q:
        p=False
    else:
        mask = mask | (1 << 7)

    if t.maxbtagevent > 0.46:
    #if t.maxbtagevent > 0.56:
    #if t.maxbtagevent > 0.8:
    #if False:        
        p=False
    else:
        mask = mask | (1 << 8)

    if (t.flags & WLLJJVetoV1):
    #if False:        
        p=False
    else:
        mask = mask | (1 << 9)       

    if (t.flags & WLLJJVetoV2):
    #if False:        
        p=False
    else:
        mask = mask | (1 << 10)

    if (t.flags & WLLJJVetoV3):
    #if False:        
        p=False
    else:
        mask = mask | (1 << 11)

    if (t.flags & WLLJJVetoV5):
    #if False:        
        p=False
    else:
        mask = mask | (1 << 12)

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
        else:
            mask = mask | (1 << 13) 
        if abs(t.jet1.Eta() - t.jet2.Eta()) < 2.5:
            p=False
        else:
            mask = mask | (1 << 14)

    #passall = (1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (1 << 4) | (1 << 5) | (1 << 6) | (1 << 7) | (1 << 8) | (1 << 9) | (1 << 10) | (1 << 11) | (1 << 12) | (1 << 13) | (1 << 14) | (1 << 15)

    #assert(p == (mask == passall))
    
    return [p,mask]
