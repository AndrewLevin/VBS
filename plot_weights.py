from ROOT import *
import sys
from array import array

f=TFile('test.root','recreate')

mytree=TTree("tree","tree")

w=array('f',[0])
mytree.Branch('weight',w,'weight/F')

f_input=open("delete_this.txt",'r')

binning=array('f')

print len(binning)

#for p in range(-2,6):
#    for k in range(1,10):
#        binning.extend([k*   pow(10,p)])

factor=1.02
min_bin=0.000001
min_width=0.000001

current_bin=min_bin
current_width=min_width
binning.extend([current_bin])
for i in range(1,1000):
    binning.extend([current_bin+current_width])
    current_bin=current_bin+current_width
    current_width=current_width*factor

print "last bin edge:"
print binning[len(binning)-1]

for i in binning:
    print i

for line in f_input:
    w[0]=float(line)/3.5925000e-04
    #print w[0]
    mytree.Fill()

print len(binning)

f.cd()
hist=TH1F("my_hist","reweight/SM weight",len(binning)-1,binning)

mytree.Draw("weight>>my_hist")

hist.Draw()

f.Write()
f.Close()
