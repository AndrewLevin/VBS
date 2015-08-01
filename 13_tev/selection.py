from ROOT import *

gROOT.ProcessLine('#include "/afs/cern.ch/work/a/anlevin/cmssw/CMSSW_7_2_0/src/ntuple_maker/ntuple_maker/interface/enum_definition.h"')

def passSelection(t):

    p=True

    if t.lep1.pt() < 20:
        p=False

    if t.lep2.pt() < 20:
        p=False

    if t.lep1q != t.lep2q:
        p=False

    if (t.jet1+t.jet2).M() < 500:
        p=False

    if abs(t.jet1.Eta() - t.jet2.Eta()) < 2.5:
        p=False

    if t.maxbtagevent > 0.89:
        p=False

    lep1passfullid = bool(t.flags & Lep1TightSelectionV1)
    lep2passfullid = bool(t.flags & Lep2TightSelectionV1)

    if not lep1passfullid:
        p=False

    if not lep2passfullid:
        p=False

    return p
