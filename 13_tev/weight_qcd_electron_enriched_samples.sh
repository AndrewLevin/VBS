
python2.6 weight_events.py --input_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_em_enriched_2030_v20_unweighted.root --output_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_em_enriched_2030_v20.root --x 5534000  -s "qcd"
python2.6 weight_events.py --input_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_em_enriched_3050_v20_unweighted.root --output_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_em_enriched_3050_v20.root --x 6949000  -s "qcd" 
python2.6 weight_events.py --input_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_em_enriched_5080_v20_unweighted.root --output_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_em_enriched_5080_v20.root --x  2201000 -s "qcd"
python2.6 weight_events.py --input_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_em_enriched_80120_v20_unweighted.root --output_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_em_enriched_80120_v20.root --x 415500  -s "qcd"
python2.6 weight_events.py --input_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_em_enriched_120170_v20_unweighted.root --output_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_em_enriched_120170_v20.root --x 76140  -s "qcd"
python2.6 weight_events.py --input_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_em_enriched_170300_v20_unweighted.root --output_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_em_enriched_170300_v20.root --x 18710  -s "qcd"
python2.6 weight_events.py --input_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_em_enriched_300Inf_v20_unweighted.root --output_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_em_enriched_300Inf_v20.root --x 1220  -s "qcd"

hadd /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_em_enriched_v20.root /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_em_enriched_2030_v20.root /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_em_enriched_2030_v20.root /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_em_enriched_2030_v20.root /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_em_enriched_80120_v20.root /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_em_enriched_120170_v20.root /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_em_enriched_170300_v20.root /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_em_enriched_300Inf_v20.root

python2.6 weight_events.py --input_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_bctoe_2030_v20_unweighted.root --output_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_bctoe_2030_v20.root --x 363100  -s "qcd"
python2.6 weight_events.py --input_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_bctoe_3080_v20_unweighted.root --output_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_bctoe_3080_v20.root --x 417800  -s "qcd"
python2.6 weight_events.py --input_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_bctoe_80170_v20_unweighted.root --output_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_bctoe_80170_v20.root --x 39860  -s "qcd"
python2.6 weight_events.py --input_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_bctoe_170250_v20_unweighted.root --output_filename /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_bctoe_170250_v20.root --x 2608  -s "qcd"

hadd /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_bctoe_v20.root /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_bctoe_2030_v20.root /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_bctoe_3080_v20.root /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_bctoe_80170_v20.root /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_bctoe_170250_v20.root

hadd /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_electron_enriched_v20.root /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_bctoe_v20.root /afs/cern.ch/work/a/anlevin/data/fr_flattish_ntuples/qcd_em_enriched_v20.root