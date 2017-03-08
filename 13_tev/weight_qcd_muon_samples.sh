version=v20

#https://cms-pdmv.cern.ch/mcm/requests?produce=%2FQCD_Pt-15to30_Tune4C_13TeV_pythia8%2FFall13-POSTLS162_V1_castor-v1%2FGEN-SIM&page=0&shown=262271

python2.6 weight_events.py --input_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_muon_15to30_v20_unweighted.root --output_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_muon_15to30_v20.root --x 1822000000  -s "qcd"

python2.6 weight_events.py --input_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_muon_30to50_v20_unweighted.root --output_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_muon_30to50_v20.root --x 138700000  -s "qcd"

python2.6 weight_events.py --input_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_muon_50to80_v20_unweighted.root --output_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_muon_50to80_v20.root --x 19120000  -s "qcd"

python2.6 weight_events.py --input_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_muon_80to120_v20_unweighted.root --output_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_muon_80to120_v20.root --x 2735000  -s "qcd"

python2.6 weight_events.py --input_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_muon_120to170_v20_unweighted.root --output_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_muon_120to170_v20.root --x 466300  -s "qcd"

python2.6 weight_events.py --input_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_muon_170to300_v20_unweighted.root --output_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_muon_170to300_v20.root --x 171200  -s "qcd"

python2.6 weight_events.py --input_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_muon_300to470_v20_unweighted.root --output_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_muon_300to470_v20.root --x 7755  -s "qcd"

hadd /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_muon_v20.root /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_muon_15to30_v20.root /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_muon_30to50_v20.root /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_muon_50to80_v20.root /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_muon_80to120_v20.root /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_muon_120to170_v20.root /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_muon_170to300_v20.root /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_muon_300to470_v20.root