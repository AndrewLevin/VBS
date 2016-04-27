output_dir_wmwm=/afs/cern.ch/user/a/anlevin/www/VBS/20Apr2016/wmwm/
output_dir_wpwp=/afs/cern.ch/user/a/anlevin/www/VBS/20Apr2016/wpwp/

python2.6 plot_lhe_distributions.py "output_distributions_madgraph_wmwm.root" "output_distributions_powheg_wmwm.root" 1 1 1 1 1 "diquark_mass" "diquark_mass" "m_{jj} (GeV)" "madgraph" "powheg" "${output_dir_wmwm}mg_powheg_mjj.png" 0
python2.6 plot_lhe_distributions.py "output_distributions_madgraph_wmwm.root" "output_distributions_powheg_wmwm.root" 1 1 1 1 1 "lepton_pt" "lepton_pt" "p_{T}^{l} (GeV)" "madgraph" "powheg" "${output_dir_wmwm}mg_powheg_ptl.png" 0
python2.6 plot_lhe_distributions.py "output_distributions_madgraph_wmwm.root" "output_distributions_powheg_wmwm.root" 1 1 1 1 1 "lepton_eta" "lepton_eta" "\eta^l" "madgraph" "powheg" "${output_dir_wmwm}mg_powheg_lepeta.png" 0
python2.6 plot_lhe_distributions.py "output_distributions_madgraph_wmwm.root" "output_distributions_powheg_wmwm.root" 1 1 1 1 1 "quark_pt" "quark_pt" "p_{T}^{q} (GeV)" "madgraph" "powheg" "${output_dir_wmwm}mg_powheg_ptq.png" 0
python2.6 plot_lhe_distributions.py "output_distributions_madgraph_wmwm.root" "output_distributions_powheg_wmwm.root" 1 1 1 1 1 "quark_eta" "quark_eta" "\eta^q" "madgraph" "powheg" "${output_dir_wmwm}mg_powheg_quarketa.png" 0
python2.6 plot_lhe_distributions.py "output_distributions_madgraph_wmwm.root" "output_distributions_powheg_wmwm.root" 1 1 1 1 1 "dilepton_mass" "dilepton_mass" "m_{ll}" "madgraph" "powheg" "${output_dir_wmwm}mg_powheg_mll.png" 0
python2.6 plot_lhe_distributions.py "output_distributions_madgraph_wmwm.root" "output_distributions_powheg_wmwm.root" 1 1 1 1 1 "costheta1" "costheta1" "" "madgraph" "powheg" "${output_dir_wmwm}mg_powheg_costheta1.png" 0
python2.6 plot_lhe_distributions.py "output_distributions_madgraph_wmwm.root" "output_distributions_powheg_wmwm.root" 1 1 1 1 1 "costheta2" "costheta2" "" "madgraph" "powheg" "${output_dir_wmwm}mg_powheg_costheta2.png" 0
python2.6 plot_lhe_distributions.py "output_distributions_madgraph_wmwm.root" "output_distributions_powheg_wmwm.root" 1 1 1 1 1 "deltaetajj" "deltaetajj" "|\Delta \eta_{jj}|" "madgraph" "powheg" "${output_dir_wmwm}mg_powheg_detajj.png" 0
python2.6 plot_lhe_distributions.py "output_distributions_madgraph_wmwm.root" "output_distributions_powheg_wmwm.root" 1 1 1 1 1 "deltaetall" "deltaetall" "|\Delta \eta_{ll}|" "madgraph" "powheg" "${output_dir_wmwm}mg_powheg_detall.png" 0
python2.6 plot_lhe_distributions.py "output_distributions_madgraph_wmwm.root" "output_distributions_powheg_wmwm.root" 1 1 1 1 1 "deltaphijj" "deltaphijj" "|\Delta \phi_{jj}|" "madgraph" "powheg" "${output_dir_wmwm}mg_powheg_dphijj.png" 0
python2.6 plot_lhe_distributions.py "output_distributions_madgraph_wmwm.root" "output_distributions_powheg_wmwm.root" 1 1 1 1 1 "deltaphill" "deltaphill" "|\Delta \phi_{ll}|" "madgraph" "powheg" "${output_dir_wmwm}mg_powheg_dphill.png" 0
python2.6 plot_lhe_distributions.py "output_distributions_madgraph_wmwm.root" "output_distributions_powheg_wmwm.root" 1 1 1 1 1 "neutrinos_pt" "neutrinos_pt" "p_{T}^{\nu\nu}" "madgraph" "powheg" "${output_dir_wmwm}mg_powheg_neutrinospt.png" 0

python2.6 plot_lhe_distributions.py "output_distributions_madgraph_wpwp.root" "output_distributions_powheg_wpwp.root" 1 1 1 1 1 "diquark_mass" "diquark_mass" "m_{jj} (GeV)" "madgraph" "powheg" "${output_dir_wpwp}mg_powheg_mjj.png" 0
python2.6 plot_lhe_distributions.py "output_distributions_madgraph_wpwp.root" "output_distributions_powheg_wpwp.root" 1 1 1 1 1 "lepton_pt" "lepton_pt" "p_{T}^{l} (GeV)" "madgraph" "powheg" "${output_dir_wpwp}mg_powheg_ptl.png" 0
python2.6 plot_lhe_distributions.py "output_distributions_madgraph_wpwp.root" "output_distributions_powheg_wpwp.root" 1 1 1 1 1 "lepton_eta" "lepton_eta" "\eta^l" "madgraph" "powheg" "${output_dir_wpwp}mg_powheg_lepeta.png" 0
python2.6 plot_lhe_distributions.py "output_distributions_madgraph_wpwp.root" "output_distributions_powheg_wpwp.root" 1 1 1 1 1 "quark_pt" "quark_pt" "p_{T}^{q} (GeV)" "madgraph" "powheg" "${output_dir_wpwp}mg_powheg_ptq.png" 0
python2.6 plot_lhe_distributions.py "output_distributions_madgraph_wpwp.root" "output_distributions_powheg_wpwp.root" 1 1 1 1 1 "quark_eta" "quark_eta" "\eta^q" "madgraph" "powheg" "${output_dir_wpwp}mg_powheg_quarketa.png" 0
python2.6 plot_lhe_distributions.py "output_distributions_madgraph_wpwp.root" "output_distributions_powheg_wpwp.root" 1 1 1 1 1 "dilepton_mass" "dilepton_mass" "m_{ll}" "madgraph" "powheg" "${output_dir_wpwp}mg_powheg_mll.png" 0
python2.6 plot_lhe_distributions.py "output_distributions_madgraph_wpwp.root" "output_distributions_powheg_wpwp.root" 1 1 1 1 1 "costheta1" "costheta1" "" "madgraph" "powheg" "${output_dir_wpwp}mg_powheg_costheta1.png" 0
python2.6 plot_lhe_distributions.py "output_distributions_madgraph_wpwp.root" "output_distributions_powheg_wpwp.root" 1 1 1 1 1 "costheta2" "costheta2" "" "madgraph" "powheg" "${output_dir_wpwp}mg_powheg_costheta2.png" 0
python2.6 plot_lhe_distributions.py "output_distributions_madgraph_wpwp.root" "output_distributions_powheg_wpwp.root" 1 1 1 1 1 "deltaetajj" "deltaetajj" "|\Delta \eta_{jj}|" "madgraph" "powheg" "${output_dir_wpwp}mg_powheg_detajj.png" 0
python2.6 plot_lhe_distributions.py "output_distributions_madgraph_wpwp.root" "output_distributions_powheg_wpwp.root" 1 1 1 1 1 "deltaetall" "deltaetall" "|\Delta \eta_{ll}|" "madgraph" "powheg" "${output_dir_wpwp}mg_powheg_detall.png" 0
python2.6 plot_lhe_distributions.py "output_distributions_madgraph_wpwp.root" "output_distributions_powheg_wpwp.root" 1 1 1 1 1 "deltaphijj" "deltaphijj" "|\Delta \phi_{jj}|" "madgraph" "powheg" "${output_dir_wpwp}mg_powheg_dphijj.png" 0
python2.6 plot_lhe_distributions.py "output_distributions_madgraph_wpwp.root" "output_distributions_powheg_wpwp.root" 1 1 1 1 1 "deltaphill" "deltaphill" "|\Delta \phi_{ll}|" "madgraph" "powheg" "${output_dir_wpwp}mg_powheg_dphill.png" 0
python2.6 plot_lhe_distributions.py "output_distributions_madgraph_wpwp.root" "output_distributions_powheg_wpwp.root" 1 1 1 1 1 "neutrinos_pt" "neutrinos_pt" "p_{T}^{\nu\nu}" "madgraph" "powheg" "${output_dir_wpwp}mg_powheg_neutrinospt.png" 0

