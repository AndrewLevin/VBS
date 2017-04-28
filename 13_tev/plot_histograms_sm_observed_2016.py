import style

import optparse

parser = optparse.OptionParser()

parser.add_option('--lumi',dest='lumi')
parser.add_option('--variable',dest='variable')
parser.add_option('--reweighted_index',dest='reweighted_index')
parser.add_option('--reweighted_label',dest='reweighted_label')
parser.add_option('--xaxislabel',dest='xaxislabel',default='m_{jj}')

parser.add_option('-i',dest='inputfile')
parser.add_option('-o',dest='outputfile',default="/afs/cern.ch/user/a/anlevin/www/tmp/plot.png")

(options,args) = parser.parse_args()

from ROOT import *

xoffsetstart = 0.0;
yoffsetstart = 0.0;
xoffset = 0.20;
yoffset = 0.05;

#region = "btagged"
#region = "signal"
region = "reweighted"
#region = "wz"

if region == "reweighted":
    xpositions = [0.40,0.40,0.40,0.40,0.40,0.40,0.40,0.40,0.40]
    ypositions = [0,1,2,3,4,5,6,7,8]

if region == "signal" or region == "wz" or region == "b-tagged":
    xpositions = [0.60,0.60,0.60,0.60,0.60,0.60,0.40,0.40,0.40,0.40,0.40,0.40,0.20,0.20,0.20,0.20,0.20,0.20]
    ypositions = [0,1,2,3,4,5,0,1,2,3,4,5,0,1,2,3,4,5]

style.GoodStyle().cd()

def get_max_bin_content_plus_bin_error(hist):
    max_bin_content_plus_bin_error = hist.GetBinContent(1)+hist.GetBinError(1)
    for i in range(2,hist.GetNbinsX()+1):
        if hist.GetBinContent(i)+hist.GetBinError(i) > max_bin_content_plus_bin_error:
            max_bin_content_plus_bin_error = hist.GetBinContent(i)+hist.GetBinError(i)
    return max_bin_content_plus_bin_error

def set_axis_fonts(thstack, coordinate, title):

    if coordinate == "x":
        axis = thstack.GetHistogram().GetXaxis();
    elif coordinate == "y":
        axis = thstack.GetHistogram().GetYaxis();
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



hist_file = TFile.Open(str(options.inputfile))

gROOT.cd()

c1 = TCanvas("c1", "c1",5,50,500,500);

#variable = "mjj"

data = hist_file.Get("data_"+options.variable).Clone()


if region == "btagged":
    ttbar = hist_file.Get("ttbar_"+options.variable).Clone()
    tzq = hist_file.Get("tZq_"+options.variable).Clone()
    ttw = hist_file.Get("ttW_"+options.variable).Clone()
    ttz = hist_file.Get("ttZ_"+options.variable).Clone()
    ttg = hist_file.Get("ttg_"+options.variable).Clone()
    fake = hist_file.Get("fake_"+options.variable).Clone()
    zjets = hist_file.Get("zjets_"+options.variable).Clone()
    wpwpjjewk = hist_file.Get("signal_"+options.variable).Clone()
    wpwpjjqcd = hist_file.Get("wpwpjjqcd_"+options.variable).Clone()
    wjwjdps = hist_file.Get("wjwjdps_"+options.variable).Clone()
    wzjjewk = hist_file.Get("wz_"+options.variable).Clone()
    wgjets = hist_file.Get("wgamma_"+options.variable).Clone()

if region == "wz":
    #wpwpjjewk = hist_file.Get("signal_"+options.variable).Clone()
    wzjjewk = hist_file.Get("wz_"+options.variable).Clone()    
    fake = hist_file.Get("fake_"+options.variable).Clone()    
    tzq = hist_file.Get("tzq_"+options.variable).Clone()
    ttw = hist_file.Get("ttw_"+options.variable).Clone()
    ttz = hist_file.Get("ttz_"+options.variable).Clone()
    www = hist_file.Get("www_"+options.variable).Clone()
    wwz = hist_file.Get("wwz_"+options.variable).Clone()    

if region == "signal":
    fake = hist_file.Get("fake_"+options.variable).Clone()
    zjets = hist_file.Get("zjets_"+options.variable).Clone()
    wpwpjjewk = hist_file.Get("signal_"+options.variable).Clone()
    wpwpjjqcd = hist_file.Get("wpwpjjqcd_"+options.variable).Clone()
    wjwjdps = hist_file.Get("wjwjdps_"+options.variable).Clone()
    wzjjewk = hist_file.Get("wz_"+options.variable).Clone()
    wgjets = hist_file.Get("wgamma_"+options.variable).Clone()

if region == "reweighted":
    fake = hist_file.Get("fake_"+options.variable).Clone()
    wg = hist_file.Get("wgjj_"+options.variable).Clone()
    wz = hist_file.Get("wz_"+options.variable).Clone()
    reweighted = hist_file.Get("reweighted_"+options.variable+"_mgreweightedindex"+str(options.reweighted_index)).Clone()


if region == "btagged":
    ttbar.SetLineColor(kBlue-2)
    tzq.SetLineColor(842)
    ttw.SetLineColor(832)
    ttz.SetLineColor(798)
    ttg.SetLineColor(kViolet-9)
    data.SetLineColor(kBlack)
    fake.SetLineColor(kMagenta)
    zjets.SetLineColor(kBlue+1)
    wpwpjjqcd.SetLineColor(kYellow)
    wpwpjjewk.SetLineColor(kOrange)
    wjwjdps.SetLineColor(kAzure-2)
    wzjjewk.SetLineColor(kRed)
    wgjets.SetLineColor(kGreen+2)

if region == "signal":
    data.SetLineColor(kBlack)
    fake.SetLineColor(kMagenta)
    zjets.SetLineColor(kBlue+1)
    wpwpjjqcd.SetLineColor(kYellow)
    wpwpjjewk.SetLineColor(kOrange)
    wjwjdps.SetLineColor(kAzure-2)
    wzjjewk.SetLineColor(kRed)
    wgjets.SetLineColor(kGreen+2)

if region == "wz":
    data.SetLineColor(kBlack)
    fake.SetLineColor(kMagenta)    
    tzq.SetLineColor(842)
    ttw.SetLineColor(832)
    ttz.SetLineColor(798)
    wzjjewk.SetLineColor(kRed)
    www.SetLineColor(kAzure-2)
    wwz.SetLineColor(kGreen+2)
    #wpwpjjewk.SetLineColor(kOrange)

if region == "reweighted":
    data.SetLineColor(kBlack)
    fake.SetLineColor(kMagenta)    
    wz.SetLineColor(kRed)
    wg.SetLineColor(kGreen+2)
    reweighted.SetLineColor(kOrange)

if region == "btagged":
    ttbar.SetFillStyle(1001)
    tzq.SetFillStyle(1001)
    ttw.SetFillStyle(1001)
    ttz.SetFillStyle(1001)
    ttg.SetFillStyle(1001)
    fake.SetFillStyle(1001)
    zjets.SetFillStyle(1001)
    wpwpjjqcd.SetFillStyle(1001)
    wpwpjjewk.SetFillStyle(1001)
    wjwjdps.SetFillStyle(1001)
    wgjets.SetFillStyle(1001)
    wzjjewk.SetFillStyle(1001)

if region == "signal":
    fake.SetFillStyle(1001)
    zjets.SetFillStyle(1001)
    wpwpjjqcd.SetFillStyle(1001)
    wpwpjjewk.SetFillStyle(1001)
    wjwjdps.SetFillStyle(1001)
    wgjets.SetFillStyle(1001)
    wzjjewk.SetFillStyle(1001)

if region == "wz":
    fake.SetFillStyle(1001)
    tzq.SetFillStyle(1001)
    ttw.SetFillStyle(1001)
    ttz.SetFillStyle(1001)
    wzjjewk.SetFillStyle(1001)    
    #wpwpjjewk.SetFillStyle(1001)
    www.SetFillStyle(1001)
    wwz.SetFillStyle(1001)    

if region == "reweighted":
    fake.SetFillStyle(1001)
    wz.SetFillStyle(1001)
    wg.SetFillStyle(1001)
    reweighted.SetFillStyle(1001)

if region == "signal":
    fake.SetFillColor(kMagenta)
    zjets.SetFillColor(kBlue+1)
    wpwpjjqcd.SetFillColor(kYellow)
    wpwpjjewk.SetFillColor(kOrange)
    wjwjdps.SetFillColor(kAzure-2)
    wzjjewk.SetFillColor(kRed)
    #wzjjqcd.SetFillColor(kRed)
    wgjets.SetFillColor(kGreen+2)
    
if region == "btagged":
    ttbar.SetFillColor(kBlue-2)
    tzq.SetFillColor(842)
    ttw.SetFillColor(832)
    ttz.SetFillColor(798)
    ttg.SetFillColor(kViolet-9)
    fake.SetFillColor(kMagenta)
    zjets.SetFillColor(kBlue+1)
    wpwpjjqcd.SetFillColor(kYellow)
    wpwpjjewk.SetFillColor(kOrange)
    wjwjdps.SetFillColor(kAzure-2)
    wzjjewk.SetFillColor(kRed)
    #wzjjqcd.SetFillColor(kRed)
    wgjets.SetFillColor(kGreen+2)

if region == "wz":
    tzq.SetFillColor(842)
    ttw.SetFillColor(832)
    ttz.SetFillColor(798)
    wzjjewk.SetFillColor(kRed)
    fake.SetFillColor(kMagenta)
    #wpwpjjewk.SetFillColor(kOrange)    
    www.SetFillColor(kAzure-2)
    wwz.SetFillColor(kGreen+2)

if region == "reweighted":
    data.SetFillColor(kBlack)
    fake.SetFillColor(kMagenta)    
    wz.SetFillColor(kRed)
    wg.SetFillColor(kGreen+2)
    reweighted.SetFillColor(kOrange)


data.SetMarkerStyle(kFullCircle);

#wpwpjjqcd.SetLineWidth(3)
#wpwpjjewk.SetLineWidth(3)

hstack = THStack()
hsum = fake.Clone()
hsum.Scale(0.0)

if region == "btagged":
    hstack.Add(fake)
    hstack.Add(zjets)
    hstack.Add(wpwpjjqcd)
    hstack.Add(wjwjdps)
    hstack.Add(wzjjewk)
    hstack.Add(wgjets)
    hstack.Add(wpwpjjewk)
    hstack.Add(ttbar)
    hstack.Add(tzq)
    hstack.Add(ttz)
    hstack.Add(ttw)
    hstack.Add(ttg)


if region == "signal":
    hstack.Add(fake)
    hstack.Add(zjets)
    hstack.Add(wpwpjjqcd)
    hstack.Add(wjwjdps)
    hstack.Add(wzjjewk)
    hstack.Add(wgjets)
    hstack.Add(wpwpjjewk)

if region == "wz":
    hstack.Add(wzjjewk)
    hstack.Add(fake)
    hstack.Add(tzq)
    hstack.Add(ttz)
    hstack.Add(ttw)
    hstack.Add(www)
    hstack.Add(wwz)
    #hstack.Add(wpwpjjewk)

if region == "reweighted":
    hstack.Add(fake)
    hstack.Add(wz)
    hstack.Add(wg)
    hstack.Add(reweighted)

if region == "btagged":
    hsum.Add(fake)
    hsum.Add(zjets)
    hsum.Add(wpwpjjqcd)
    hsum.Add(wjwjdps)
    hsum.Add(wzjjewk)
    hsum.Add(wgjets)
    hsum.Add(wpwpjjewk)
    hsum.Add(ttbar)
    hsum.Add(ttz)
    hsum.Add(ttw)
    hsum.Add(ttg)
    hsum.Add(tzq)

if region == "signal":
    hsum.Add(fake)
    hsum.Add(zjets)
    hsum.Add(wpwpjjqcd)
    hsum.Add(wjwjdps)
    hsum.Add(wzjjewk)
    hsum.Add(wgjets)
    hsum.Add(wpwpjjewk)

if region == "wz":
    hsum.Add(fake)
    hsum.Add(wzjjewk)
    hsum.Add(tzq)
    hsum.Add(ttz)
    hsum.Add(ttw)
    hsum.Add(www)
    hsum.Add(wwz)
    #hsum.Add(wpwpjjewk)

if region == "reweighted":
    hsum.Add(fake)
    hsum.Add(wz)
    hsum.Add(wg)
    hsum.Add(reweighted)
    
ymax = max(get_max_bin_content_plus_bin_error(hsum),get_max_bin_content_plus_bin_error(data))

hstack.SetMaximum(1.55 * ymax)

hstack.Draw()

s=str(options.lumi)+" fb^{-1} (13 TeV)"
lumilabel = TLatex (0.95, 0.93, s)
lumilabel.SetNDC ()
lumilabel.SetTextAlign (30)
lumilabel.SetTextFont (42)
lumilabel.SetTextSize (0.040)

hstack.Draw("hist")

#cmslabel = TLatex (0.18, 0.93, "#bf{CMS} (Unpublished)")
cmslabel = TLatex (0.18, 0.93, "")
cmslabel.SetNDC ()
cmslabel.SetTextAlign (10)
cmslabel.SetTextFont (42)
cmslabel.SetTextSize (0.040)
cmslabel.Draw ("same") 

lumilabel.Draw("same")

#wpwpjjewk.Draw("same")


if region == "btagged":
    j=0
    draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,fake,"fake","f")
    j=j+1
    draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,zjets,"Z+jets","f")
    j=j+1
    draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,wzjjewk,"WZ+jets","f")
    j=j+1
    draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,wpwpjjqcd,"WWJJ QCD","f")
    j=j+1
    draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,wgjets,"WGJJ","f")
    j=j+1
    draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,ttw,"TTW","f")
    j=j+1
    draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,ttz,"TTZ","f")
    j=j+1
    draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,ttg,"TTG","f")
    j=j+1
    draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,tzq,"TZQ","f")
    j=j+1
    draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,ttbar,"ttbar fl","f")
    j=j+1
    draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,wpwpjjewk,"WWJJ","f")


if region == "signal":
    j=0
    draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,fake,"fake","f")
    j=j+1
    draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,zjets,"Z+jets","f")
    j=j+1
    draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,wzjjewk,"WZ+jets","f")
    j=j+1
    draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,wpwpjjqcd,"WWJJ QCD","f")
    j=j+1
    draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,wgjets,"WGJJ","f")
    j=j+1
    draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,wpwpjjewk,"WWJJ","f")

if region == "wz":
    j=0
    draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,fake,"fake","f")
    j=j+1
    draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,wzjjewk,"WZ+jets","f")
    j=j+1
    draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,ttw,"TTW","f")
    j=j+1
    draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,ttz,"TTZ","f")
    j=j+1
    draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,tzq,"TZQ","f")
    j=j+1
    draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,wwz,"WWW","f")
    j=j+1
    draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,www,"WWZ","f")    

if region == "reweighted":
    j=0
    draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,fake,"fake","f")
    j=j+1
    draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,wz,"WZ+jets","f")
    j=j+1
    draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,wg,"WG+jets","f")
    j=j+1
    draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,reweighted,options.reweighted_label,"f")


j=j+1
draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,data,"data","lp")

data.Draw("Esame")

#set_axis_fonts(hstack,"x","m_{ll} (GeV)")
#set_axis_fonts(hstack,"x","|\Delta \eta_{jj}|")
set_axis_fonts(hstack,"x",options.xaxislabel)
#set_axis_fonts(hstack,"x","pt_{l}^{max} (GeV)")
set_axis_fonts(hstack,"y","Events / bin")

hstack.GetHistogram().LabelsOption("v");

gstat = TGraphAsymmErrors(hsum);
for i in range(0,gstat.GetN()):

    gstat.SetPointEYlow (i, hsum.GetBinError(i+1));
    gstat.SetPointEYhigh(i, hsum.GetBinError(i+1));

gstat.SetFillColor(12);
gstat.SetFillStyle(3345);
gstat.SetMarkerSize(0);
gstat.SetLineWidth(0);
gstat.SetLineColor(kWhite);
gstat.Draw("E2same");

c1.Update()
c1.ForceUpdate()

c1.SaveAs(options.outputfile)
