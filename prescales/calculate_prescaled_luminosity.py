from ROOT import *
import optparse
import sys
import json
import os

parser = optparse.OptionParser()

parser.add_option('-i', '--input_filename', help='input_filename', dest='infname', default='my_input_file.root')

(options,args) = parser.parse_args()

fin=TFile(options.infname,"read")
fin.cd()

t = fin.Get("demo/prescales")

d = {}

for entry in range(t.GetEntries()):
    t.GetEntry(entry)

    assert(t.l1min == t.l1max)

    total_prescale = int(t.prescale)*int(t.l1max)

    if t.prescale not in d:
        d[total_prescale] = {}

    if t.run not in d[total_prescale]:
        d[total_prescale][t.run] = []

    d[total_prescale][t.run].append(t.lumi)

for k1 in d:
    for k2 in d[k1]:
        d[k1][k2].sort()

d_merged = {}

for k1 in d:
    d_merged[k1] = {}
    for k2 in d[k1]:
        d_merged[k1][k2] = []
        for i in range(0,len(d[k1][k2])):
            if i == 0:
                lower = d[k1][k2][i]


            if i == len(d[k1][k2]) - 1:
                d_merged[k1][k2].append([lower,d[k1][k2][i]])
            elif d[k1][k2][i+1] == d[k1][k2][i]+1:
                continue
            else:
                d_merged[k1][k2].append([lower,d[k1][k2][i]])
                lower = d[k1][k2][i+1]

sum=0

for k1 in d_merged:
    j = json.dumps(d_merged[k1])
    f = open("delete_this.txt",'w')
    print >> f, j
    f.flush()
    output=os.popen("rm -r ~/.local/lib/python2.7/site-packages/brilws-0.10.7-py2.7.egg-info/; export PATH=$HOME/.local/bin:/afs/cern.ch/cms/lumi/brilconda-1.0.3/bin:$PATH; pip install --install-option=\"--prefix=\$HOME/.local\" brilws; brilcalc lumi -u /pb -i delete_this.txt").read()
    sum=sum+float(output.split('|')[len(output.split('|'))-2])/float(k1)

print sum


#see this: http://cms-service-lumi.web.cern.ch/cms-service-lumi/brilwsdoc-010x.html

#os.system("pip install --install-option=\"--prefix=\$HOME/.local\" brilws")
#os.system("brilcalc lumi -u /pb -i delete_this_3.txt ")


#print j

#print d

