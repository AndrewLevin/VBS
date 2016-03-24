from ROOT import *

gROOT.ProcessLine('#include "/afs/cern.ch/work/a/anlevin/cmssw/CMSSW_7_4_15/src/ntuple_maker/ntuple_maker/interface/enum_definition.h"')

def passSelection(t,mode):

    p=True

    if not passSelectionExceptLeptonIDs(t,mode):
        p = False

    lep1passfullid = bool(t.flags & Lep1TightSelectionV1)
    lep2passfullid = bool(t.flags & Lep2TightSelectionV1)

    if not lep1passfullid:
        p=False

    if not lep2passfullid:
        p=False


    #if (t.flags & WLLJJVetoV6):
    #    p=False                

    return p

z_mass = 91.18

def passSelectionExceptLeptonIDs(t,mode):

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

    #if abs(t.jet1.eta())> 2.5:
    #    p=False

    #if abs(t.jet2.eta())> 2.5:
    #    p=False        

    if t.lep1q != t.lep2q:
        p=False

    #if abs(t.jet1.Eta()) > 3 or abs(t.jet2.Eta()) > 3:
    #    p=False

    if mode == "sm_low_mjj_control_region":    
        if (t.jet1+t.jet2).M() > 500:
            p=False
    else:        
        if (t.jet1+t.jet2).M() < 500:
            p=False
        if abs(t.jet1.Eta() - t.jet2.Eta()) < 2.5:
            p=False


    if t.maxbtagevent > 0.605:

#   if t.maxbtagevent > 1:
#    if t.maxbtagevent > 0.89:
        p=False

    if (t.flags & WLLJJVetoV1):
        p=False

    if (t.flags & WLLJJVetoV2):
        p=False

    if abs(t.jet1.eta()) > 4.7 or abs(t.jet2.eta()) > 4.7:
        p=False

    if t.jet1.pt() < 30:
        p=False

    if t.jet2.pt() < 30:
        p=False                
        
    return p
