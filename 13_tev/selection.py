from ROOT import *

#gROOT.ProcessLine('#include "/afs/cern.ch/work/a/anlevin/cmssw/CMSSW_8_0_20/src/ntuple_maker/ntuple_maker/interface/enum_definition.h")

gROOT.ProcessLine('#include "/afs/cern.ch/work/a/anlevin/cmssw/CMSSW_8_0_26_patch1/src/ntuple_maker/ntuple_maker/interface/enum_definition.h"')

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
        if t.maxbtagevent > 0.5426:
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

    #trigger
    if not (t.flags & PassTriggerV2):
    #if False:        
        p=False
    else:
        mask = mask | (1 << 1)        

    #jet pt cuts
    if t.jet1.pt() < 30 or t.jet2.pt() < 30:
        p=False
    else:
        mask = mask | (1 << 2)

    #jet eta cuts    
    if abs(t.jet1.eta()) > 4.7 or abs(t.jet2.eta()) > 4.7:
    #if False:
        p=False
    else:
        mask = mask | (1 << 3)

    #lepton pt cuts    
    if not(t.lep1.pt() > 25 and t.lep2.pt() > 20) and not (t.lep1.pt() > 20 and t.lep2.pt() > 25):
        p=False
    else:
        mask = mask | (1 << 4)

    #lepton charge requirement    
    if t.lep1q != t.lep2q:
        p=False
    else:
        mask = mask | (1 << 5)

    #additional loose muon veto    
#    if cfg["which_selection"] == "full_btagged" and (t.flags & VetoV5):
#        #if we are selecting b-tagged events, and there is a soft muon, then is is also likely a loose muon, so we don't want to apply this cut
#        #we should really redefine VetoV4 such that it does not include soft muons
#        pass
#    else:
    if (t.flags & VetoV4):
        #if False:        
        p=False
    else:
        mask = mask | (1 << 6)

    #reject events with an extra fakeable object electron or an extra loose electron
    if (t.flags & VetoV2):
    #if False:        
        p=False
    else:
        mask = mask | (1 << 7)

    #the hadronic tau veto
    if (t.flags & VetoV7):
    #if False:        
        p=False
    else:
        mask = mask | (1 << 8)

    #missing energy cut    
    if t.metpt < 40:
        p=False
    else:
        mask = mask | (1 << 9)

    #reject events where the two selected leptons are electrons consistent with a z boson    
    if abs(t.lep1id) == 11 and abs(t.lep2id) == 11 and abs((t.lep1+t.lep2).mass() - z_mass) < 15:
        p=False
    else:
        mask = mask | (1 << 10)

    #mll > 20 cut    
    if (t.lep1+t.lep2).mass() < 20:
        p=False
    else:
        mask = mask | (1 << 11)

    if  cfg["which_selection"] == "full_btagged":
#        if not (t.maxbtagevent > 0.8484 or (t.flags & VetoV5)):
        if not (t.maxbtagevent > 0.8484) or (t.flags & VetoV5):            
#        if not (t.maxbtagevent > 0.8484) or (t.maxbtagevent > 0.99) or (t.flags & VetoV5):            
            p=False
        else:
            mask = mask | (1 << 12)
    else:        
        if (t.maxbtagevent > 0.8484 or (t.flags & VetoV5)):
            p=False
        else:
            mask = mask | (1 << 12)            

    if cfg["mode"] == "fr_closure_test":
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
        if cfg["which_selection"] == "full_novbs":
            mask = mask | (1 << 13)
            mask = mask | (1 << 14)
            mask = mask | (1 << 15)
        elif cfg["which_selection"] == "full_lowmjj1":
            if (t.jet1+t.jet2).M() > 500:
                p=False
            if abs(t.jet1.Eta() - t.jet2.Eta()) < 2.5:
                p=False
            if max(abs(t.lep1.Eta() - (t.jet1.Eta() + t. jet2.Eta())/2)/abs(t.jet1.Eta() - t. jet2.Eta()),abs(t.lep2.Eta() - (t.jet1.Eta() + t. jet2.Eta())/2)/abs(t.jet1.Eta() - t. jet2.Eta())) > 0.75:
                p=False
        elif cfg["which_selection"] == "full_lowmjj2":
            if (t.jet1+t.jet2).M() > 500:
                p=False
        else:

            #mjj cut
            if (t.jet1+t.jet2).M() < 500:
                p=False
            else:
                mask = mask | (1 << 13)

            #delta eta jj cut    
            if abs(t.jet1.Eta() - t.jet2.Eta()) < 2.5:
                p=False
            else:
                mask = mask | (1 << 14)

            if abs(t.jet1.Eta() - t. jet2.Eta()) == 0:
                print "warning, abs(t.jet1.Eta() - t. jet2.Eta()) = 0 in event " + str(t.run)+ ":"+ str(t.lumi)+ ":" + str(t.event)

            #zeppenfeld-like variable cut    
            if (abs(t.jet1.Eta() - t. jet2.Eta()) == 0) or (max(abs(t.lep1.Eta() - (t.jet1.Eta() + t. jet2.Eta())/2)/abs(t.jet1.Eta() - t. jet2.Eta()),abs(t.lep2.Eta() - (t.jet1.Eta() + t. jet2.Eta())/2)/abs(t.jet1.Eta() - t. jet2.Eta())) > 0.75):
                p=False
            else:
                mask = mask | (1 << 15)

    return [p,mask]


def passWZSelectionExceptLeptonIDs(t,cfg):

    p=True

    mask = 0

    if t.jet1.pt() < 30 or t.jet2.pt() < 30:
        p=False
    else:
        mask = mask | (1 << 1)

    if abs(t.jet1.eta()) > 4.7 or abs(t.jet2.eta()) > 4.7:
    #if False:
        p=False
    else:
        mask = mask | (1 << 2)

    if (t.flags & VetoV12):
    #if False:        
        p=False
    else:
        mask = mask | (1 << 3)

    
    #

    #if not (t.flags & PassTriggerV6):
    #if not (t.flags & PassTriggerV3):
    if not (t.flags & PassTriggerV2):
    #if not (t.flags & PassTriggerV1):
    #if False:        
        p=False
    else:
        mask = mask | (1 << 4)        

    if not(t.lep1.pt() > 25 and t.lep2.pt() > 20 and t.lep3.pt() > 10) and not (t.lep1.pt() > 20 and t.lep2.pt() > 25 and t.lep3.pt() > 10) and not(t.lep1.pt() > 10 and t.lep2.pt() > 25 and t.lep3.pt() > 20) and not(t.lep1.pt() > 10 and t.lep2.pt() > 20 and t.lep3.pt() > 25) and not(t.lep1.pt() > 25 and t.lep2.pt() > 10 and t.lep3.pt() > 20) and not(t.lep1.pt() > 20 and t.lep2.pt() > 10 and t.lep3.pt() > 25):
        p=False
    else:
        mask = mask | (1 << 5)



#    if (t.lep1+t.lep2).mass() < 4:
    if False:
        p=False
    else:
        mask = mask | (1 << 6)



    if t.metpt < 40:
        p=False
    else:
        mask = mask | (1 << 7)

    #if t.lep1q != t.lep2q:
    if not (((t.lep1 + t.lep2).M() < 106.1876 and (t.lep1+t.lep2).M() > 76.1876 and t.lep1q != t.lep2q and abs(t.lep1id) == abs(t.lep2id)) or ((t.lep1 + t.lep3).M() < 106.1876 and (t.lep1+t.lep3).M() > 76.1876 and t.lep1q != t.lep3q and abs(t.lep1id) == abs(t.lep3id)) or ((t.lep2 + t.lep3).M() < 106.1876 and (t.lep2+t.lep3).M() > 76.1876 and t.lep2q != t.lep3q and abs(t.lep2id) == abs(t.lep3id))):
    #if False:
        p=False
    else:
        mask = mask | (1 << 8)




    if  cfg["which_selection"] == "full_btagged":
        if not (t.maxbtagevent > 0.9535 or (t.flags & VetoV13)):
            p=False
        else:
            mask = mask | (1 << 9)
    else:        
        if (t.maxbtagevent > 0.9535 or (t.flags & VetoV13)):
            p=False
        else:
            mask = mask | (1 << 9)            

    
        #extra electron veto
    #if (t.flags & WLLJJVetoV2):
    if False:        
        p=False
    else:
        mask = mask | (1 << 10)

#if t.maxbtagevent < 0.8484:        
    #if t.maxbtagevent > 0.5426:
    #if t.maxbtagevent > 0.56:
    #if t.maxbtagevent > 0.7:
    #if False:        

    #third muon z veto
#    if (t.flags & WLLJJVetoV10):
#    if (t.flags & WLLJJVetoV1):
    if False:        
        p=False
    else:
        mask = mask | (1 << 11)       


    #third electron z veto
    #if (t.flags & WLLJJVetoV9):
    if False:        
        p=False
    else:
        mask = mask | (1 << 12)



    #the hadronic tau veto
#    if (t.flags & WLLJJVetoV3):
    #if (t.flags & WLLJJVetoV7):
    if False:        
        p=False
    else:
        mask = mask | (1 << 13)

    #if abs(t.lep1id) == 11 and abs(t.lep2id) == 11 and abs((t.lep1+t.lep2).mass() - z_mass) < 15:
    if False:
        p=False
    else:
        mask = mask | (1 << 14)



    #if cfg["mode"] == "sm_low_mjj_control_region":
    #    if (t.jet1+t.jet2).M() > 500:
    #        p=False
    #    if abs(t.jet1.Eta() - t.jet2.Eta()) < 2.5:
    #        p=False
    #    if max(abs(t.lep1.Eta() - (t.jet1.Eta() + t. jet2.Eta())/2)/abs(t.jet1.Eta() - t. jet2.Eta()),abs(t.lep2.Eta() - (t.jet1.Eta() + t. jet2.Eta())/2)/abs(t.jet1.Eta() - t. jet2.Eta())) > 0.75:
    #        p=False
    if cfg["mode"] == "fr_closure_test":
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
        if cfg["which_selection"] == "full_novbs":
            mask = mask | (1 << 15)
            mask = mask | (1 << 16)
            mask = mask | (1 << 17)
        elif cfg["which_selection"] == "full_lowmjj1":
            if (t.jet1+t.jet2).M() > 500:
                p=False
            if abs(t.jet1.Eta() - t.jet2.Eta()) < 2.5:
                p=False
            if max(abs(t.lep1.Eta() - (t.jet1.Eta() + t. jet2.Eta())/2)/abs(t.jet1.Eta() - t. jet2.Eta()),abs(t.lep2.Eta() - (t.jet1.Eta() + t. jet2.Eta())/2)/abs(t.jet1.Eta() - t. jet2.Eta())) > 0.75:
                p=False
        elif cfg["which_selection"] == "full_lowmjj2":
            if (t.jet1+t.jet2).M() > 500:
                p=False
        else:
            if (t.jet1+t.jet2).M() < 500:
                p=False
            else:
                mask = mask | (1 << 15) 
            if abs(t.jet1.Eta() - t.jet2.Eta()) < 2.5:
                p=False
            else:
                mask = mask | (1 << 16)
            if False:    
            #if max(abs(t.lep1.Eta() - (t.jet1.Eta() + t. jet2.Eta())/2)/abs(t.jet1.Eta() - t. jet2.Eta()),abs(t.lep2.Eta() - (t.jet1.Eta() + t. jet2.Eta())/2)/abs(t.jet1.Eta() - t. jet2.Eta())) > 0.75:
                p=False
            else:
                mask = mask | (1 << 17)

    #print max(abs(t.lep1.Eta() - (t.jet1.Eta() + t. jet2.Eta())/2)/abs(t.jet1.Eta() - t. jet2.Eta()),abs(t.lep2.Eta() - (t.jet1.Eta() + t. jet2.Eta())/2)/abs(t.jet1.Eta() - t. jet2.Eta()))

    #passall = (1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (1 << 4) | (1 << 5) | (1 << 6) | (1 << 7) | (1 << 8) | (1 << 9) | (1 << 10) | (1 << 11) | (1 << 12) | (1 << 13) | (1 << 14) | (1 << 15)

    #assert(p == (mask == passall))

    return [p,mask]
