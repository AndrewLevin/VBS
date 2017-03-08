from ROOT import *



f = TFile("histograms_2016.root","read")


lumi = 36.15*1000

n_expected_signal_no_cuts=0.05004*lumi
n_expected_wzjj_no_cuts=0.5049*lumi
n_expected_wgjets_no_cuts=5.661*lumi
#n_expected_ttbar_no_cuts=700*lumi

n_expected_signal_no_cuts_str="%.2f" % n_expected_signal_no_cuts
n_expected_wzjj_no_cuts_str="%.2f" % n_expected_wzjj_no_cuts
n_expected_wgjets_no_cuts_str="%.2f" % n_expected_wgjets_no_cuts
#n_expected_ttbar_no_cuts_str="%.2f" % n_expected_ttbar_no_cuts

print "\\begin{table}[htbp]"
print "\\begin{center}"
print "\\begin{tabular}{|c|c|c|c|c|}"

print "\hline"

#print "& $W^{\pm}W^{\pm}JJ$ & WZJJ & WGJJ & ttbar & fake \\\\"
print "& $W^{\pm}W^{\pm}JJ$ & WZJJ & WGJJ & fake \\\\"
print "\\hline"

print "\\hline"

print "no cuts & "+n_expected_signal_no_cuts_str + " & "+n_expected_wzjj_no_cuts_str + " & "+n_expected_wgjets_no_cuts_str + " & " + "\\\\"

cut_names = ["" , "" , ""  , "lepton selections" , "trigger" , "lepton $p_T$","$m_{ll} > 20$" , "MET" ,  "lepton charge",   "anti-b-tagging"  ,  "extra electron"  , "extra muon, $|m_{mm} - m_Z| < 15$", "extra electron, $|m_{ee} - m_{Z}| < 15$",  "$\\tau_h$"  ,  "$|m_{ee} - m_{Z}| < 15$" ,  "$m_{jj}$"  , "$|\\Delta \\eta_{jj}|$", "$\\left.\\text{max}\\left(\\left| \\eta^{l_1} - \\frac{\\eta^{j_2} + \\eta^{j_2}}{2}\\right| ,\\left|  \\eta^{l_2} - \\frac{\\eta^{j_2} + \\eta^{j_2}}{2} \\right|  \\right) \\right/\\left|\\Delta \\eta_{jj} \\right| $ "  ]

for i in range(0,18):

    if i == 0 or i == 1 or i == 2:
        continue
    
    h_signal=f.Get("signal_cut"+str(i))
    h_wzjj=f.Get("wzjjewk_cut"+str(i))
    h_wgjets=f.Get("wgjets_cut"+str(i))
    #h_ttbar=f.Get("ttbar_cut"+str(i))
    h_fake=f.Get("fake_cut"+str(i))
    print "\hline"
    signal="%.2f" % h_signal.Integral(0,5)
    wzjj="%.2f" % h_wzjj.Integral(0,5)
    wgjets="%.2f" % h_wgjets.Integral(0,5)
    #ttbar="%.2f" % h_ttbar.Integral(0,5)
    fake ="%.2f" % h_fake.Integral(0,5)
    print cut_names[i]+" & "+signal+" & "+wzjj +" & " + wgjets+ " & " + fake + " \\\\"

print "\hline"

print "\\end{tabular}"
print "\\end{center}"

print "\\caption{Expected number of events after each cut.}"

print "\\label{tab:cutflow}"

print "\\end{table}"

