from ROOT import *
import sys
import time

g_higgs = TGraph()
g_no_higgs = TGraph()

g_higgs.SetPoint(0,0.2,1456)
g_higgs.SetPoint(1,0.3,1296)
g_higgs.SetPoint(2,0.4,1313)
g_higgs.SetPoint(3,0.5,1324)
g_higgs.SetPoint(4,0.6,1333)
g_higgs.SetPoint(5,0.7,1335)
g_higgs.SetPoint(6,0.8,1332)
g_higgs.SetPoint(7,0.9,1335)
g_higgs.SetPoint(8,1,1337)
g_higgs.SetPoint(9,2,1341)
g_higgs.SetPoint(10,3,1356)
g_higgs.SetPoint(11,4,1351)
g_higgs.SetPoint(12,5,1359)
g_higgs.SetPoint(13,6,1367)


g_no_higgs.SetPoint(0,0.2,1601)
g_no_higgs.SetPoint(1,0.3,1357)
g_no_higgs.SetPoint(2,0.4,1371)
g_no_higgs.SetPoint(3,0.5,1384)
g_no_higgs.SetPoint(4,0.6,1408)
g_no_higgs.SetPoint(5,0.7,1419)
g_no_higgs.SetPoint(6,0.8,1445)
g_no_higgs.SetPoint(7,0.9,1472)
g_no_higgs.SetPoint(8,1,1500)
g_no_higgs.SetPoint(9,2,1861)
g_no_higgs.SetPoint(10,3,2454)
g_no_higgs.SetPoint(11,4,3298)
g_no_higgs.SetPoint(12,5,4343)
g_no_higgs.SetPoint(13,6,5646)

g_higgs.SetMarkerColor(kGreen+1)
g_no_higgs.SetMarkerColor(kBlue)

g_higgs.SetLineColor(kGreen+1)
g_no_higgs.SetLineColor(kBlue)

g_higgs.SetLineWidth(3)
g_no_higgs.SetLineWidth(3)

g_no_higgs.GetYaxis().SetTitleOffset(1.2)
g_no_higgs.GetXaxis().SetTitle("$\sqrt{s}$ (GeV)")
g_no_higgs.GetYaxis().SetTitle("cross-section (pb)")

leg=TLegend(0.2,0.6,0.4,0.8)

leg.AddEntry(g_no_higgs,"without Higgs","l")
leg.AddEntry(g_higgs,"with Higgs","l")

g_no_higgs.SetMinimum(0)

g_no_higgs.Draw()
g_higgs.Draw("same")
leg.Draw("same")

gPad.SetLeftMargin(20)

gPad.Update()
gPad.ForceUpdate()

gPad.SaveAs("/afs/cern.ch/user/a/anlevin/www/tmp/ww_scattering_xs.png")
