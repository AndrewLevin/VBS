version=v50

#https://cms-pdmv.cern.ch/mcm/requests?produce=%2FQCD_Pt-15to30_Tune4C_13TeV_pythia8%2FFall13-POSTLS162_V1_castor-v1%2FGEN-SIM&page=0&shown=262271

python2.6 weight_events.py --input_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_muon_15to30_${version}_unweighted.root --output_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_muon_15to30_${version}.root --x 1822000000  -s "qcd"

python2.6 weight_events.py --input_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_muon_30to50_${version}_unweighted.root --output_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_muon_30to50_${version}.root --x 138700000  -s "qcd"

python2.6 weight_events.py --input_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_muon_50to80_${version}_unweighted.root --output_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_muon_50to80_${version}.root --x 19120000  -s "qcd"

python2.6 weight_events.py --input_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_muon_80to120_${version}_unweighted.root --output_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_muon_80to120_${version}.root --x 2735000  -s "qcd"

python2.6 weight_events.py --input_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_muon_120to170_${version}_unweighted.root --output_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_muon_120to170_${version}.root --x 466300  -s "qcd"

python2.6 weight_events.py --input_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_muon_170to300_${version}_unweighted.root --output_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_muon_170to300_${version}.root --x 171200  -s "qcd"

python2.6 weight_events.py --input_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_muon_300to470_${version}_unweighted.root --output_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_muon_300to470_${version}.root --x 7755  -s "qcd"

hadd /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_muon_${version}.root /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_muon_15to30_${version}.root /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_muon_30to50_${version}.root /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_muon_50to80_${version}.root /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_muon_80to120_${version}.root /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_muon_120to170_${version}.root /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_muon_170to300_${version}.root /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_muon_300to470_${version}.root
