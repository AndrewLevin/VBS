import style

from ROOT import *

xoffsetstart = 0.0;
yoffsetstart = 0.0;
xoffset = 0.20;
yoffset = 0.05;

xpositions = [0.60,0.60,0.60,0.60,0.60,0.60,0.40,0.40,0.40]
ypositions = [0,1,2,3,4,5,0,1,2]

style.GoodStyle().cd()

def set_axis_fonts(thstack, coordinate, title):

    if coordinate == "x":
        axis = thstack.GetXaxis();
    elif coordinate == "y":
        axis = thstack.GetYaxis();
    else:
        assert(0)
    
    axis.SetLabelFont  (   42)
    axis.SetLabelOffset(0.015)
    axis.SetLabelSize  (0.050)
    axis.SetNdivisions (  505)
    axis.SetTitleFont  (   42)
    axis.SetTitleOffset(  1.5)
    axis.SetTitleSize  (0.050)
    if (coordinate == "y"):
        axis.SetTitleOffset(1.6)
    axis.SetTitle(title)    



def draw_legend(x1,y1,hist,label,options):

    legend = TLegend(x1+xoffsetstart,y1+yoffsetstart,x1+xoffsetstart + xoffset,y1+yoffsetstart + yoffset)

    legend.SetBorderSize(     0)
    legend.SetFillColor (     0)
    legend.SetTextAlign (    12)
    legend.SetTextFont  (    42)
    legend.SetTextSize  ( 0.040)

    legend.AddEntry(hist,label,options)

    legend.Draw("same")

    #otherwise the legend goes out of scope and is deleted once the function finishes
    hist.label = legend

hist_file = TFile.Open("histograms.root")

gROOT.cd()

c1 = TCanvas("c1", "c1",5,50,500,500);

ttbar = hist_file.Get("ttbar").Clone()
ttbar_qcd_fr = hist_file.Get("ttbar_qcd_fr").Clone()

ttbar.SetLineColor(kBlack)
ttbar_qcd_fr.SetLineColor(kMagenta)

ttbar.SetLineWidth(3)
ttbar_qcd_fr.SetLineWidth(3)

ymax = max(ttbar.GetMaximum(),ttbar_qcd_fr.GetMaximum())

ttbar.SetMinimum(0)
ttbar.SetMaximum(1.55 * ymax)

ttbar.SetTitle("")

ttbar.SetStats(kFALSE)

ttbar.Draw()

s="2.22 fb^{-1} (13 TeV)"
lumilabel = TLatex (0.95, 0.93, s)
lumilabel.SetNDC ()
lumilabel.SetTextAlign (30)
lumilabel.SetTextFont (42)
lumilabel.SetTextSize (0.040)

#hstack.Draw("hist")

cmslabel = TLatex (0.18, 0.93, "#bf{CMS} (Unpublished)")
cmslabel.SetNDC ()
cmslabel.SetTextAlign (10)
cmslabel.SetTextFont (42)
cmslabel.SetTextSize (0.040)
cmslabel.Draw ("same") 

lumilabel.Draw("same")

#wpwpjjewk.Draw("same")

j=0
draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,ttbar,"ttbar","l")
j=j+1
draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,ttbar_qcd_fr,"ttbar with qcd fr","l")


ttbar_qcd_fr.Draw("same")

set_axis_fonts(ttbar,"x","m_{jj} (GeV)")
set_axis_fonts(ttbar,"y","Events / bin")

ttbar.LabelsOption("v");

c1.Update()
c1.ForceUpdate()

c1.SaveAs("/afs/cern.ch/user/a/anlevin/www/tmp/mjj.png")
