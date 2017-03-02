from ROOT import *

f = TFile("histograms_2016.root","read")

n_expected_signal_no_cuts=0.05004*2.215*1000
n_expected_wzjj_no_cuts=0.5049*2.215*1000
n_expected_wgjets_no_cuts=5.661*2.215*1000
#n_expected_ttbar_no_cuts=700*2.215*1000

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

for i in range(0,15):
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
    print "cut "+str(i)+" & "+signal+" & "+wzjj +" & " + wgjets+ " & " + fake + " \\\\"

print "\hline"

print "\\end{tabular}"
print "\\end{center}"

print "\\caption{Expected number of events after each cut.}"

print "\\label{tab:cutflow}"

print "\\end{table}"

