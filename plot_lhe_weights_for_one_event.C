#include "TH2D.h"
#include <vector>
#include <iostream>
#include <fstream>
#include <sstream>

std::vector<double> lhe_weights;

void fill_lhe_weights(){

  lhe_weights.push_back( +2.1687000e-04 );
  lhe_weights.push_back( +2.4842022e-04 );
  lhe_weights.push_back( +2.4516011e-04 );
  lhe_weights.push_back( +2.4195984e-04 );
  lhe_weights.push_back( +2.3881941e-04 );
  lhe_weights.push_back( +2.3573881e-04 );
  lhe_weights.push_back( +2.3271805e-04 );
  lhe_weights.push_back( +2.2975713e-04 );
  lhe_weights.push_back( +2.2685604e-04 );
  lhe_weights.push_back( +2.2401479e-04 );
  lhe_weights.push_back( +2.2123338e-04 );
  lhe_weights.push_back( +2.1851180e-04 );
  lhe_weights.push_back( +2.4503531e-04 );
  lhe_weights.push_back( +2.4180756e-04 );
  lhe_weights.push_back( +2.3863964e-04 );
  lhe_weights.push_back( +2.3553155e-04 );
  lhe_weights.push_back( +2.3248331e-04 );
  lhe_weights.push_back( +2.2949490e-04 );
  lhe_weights.push_back( +2.2656632e-04 );
  lhe_weights.push_back( +2.2369759e-04 );
  lhe_weights.push_back( +2.2088869e-04 );
  lhe_weights.push_back( +2.1813962e-04 );
  lhe_weights.push_back( +2.1545040e-04 );
  lhe_weights.push_back( +2.4167718e-04 );
  lhe_weights.push_back( +2.3848177e-04 );
  lhe_weights.push_back( +2.3534620e-04 );
  lhe_weights.push_back( +2.3227047e-04 );
  lhe_weights.push_back( +2.2925457e-04 );
  lhe_weights.push_back( +2.2629851e-04 );
  lhe_weights.push_back( +2.2340229e-04 );
  lhe_weights.push_back( +2.2056590e-04 );
  lhe_weights.push_back( +2.1778935e-04 );
  lhe_weights.push_back( +2.1507264e-04 );
  lhe_weights.push_back( +2.1241577e-04 );
  lhe_weights.push_back( +2.3834582e-04 );
  lhe_weights.push_back( +2.3518276e-04 );
  lhe_weights.push_back( +2.3207954e-04 );
  lhe_weights.push_back( +2.2903616e-04 );
  lhe_weights.push_back( +2.2605261e-04 );
  lhe_weights.push_back( +2.2312890e-04 );
  lhe_weights.push_back( +2.2026503e-04 );
  lhe_weights.push_back( +2.1746099e-04 );
  lhe_weights.push_back( +2.1471680e-04 );
  lhe_weights.push_back( +2.1203243e-04 );
  lhe_weights.push_back( +2.0940791e-04 );
  lhe_weights.push_back( +2.3504123e-04 );
  lhe_weights.push_back( +2.3191052e-04 );
  lhe_weights.push_back( +2.2883965e-04 );
  lhe_weights.push_back( +2.2582862e-04 );
  lhe_weights.push_back( +2.2287742e-04 );
  lhe_weights.push_back( +2.1998606e-04 );
  lhe_weights.push_back( +2.1715454e-04 );
  lhe_weights.push_back( +2.1438286e-04 );
  lhe_weights.push_back( +2.1167101e-04 );
  lhe_weights.push_back( +2.0901900e-04 );
  lhe_weights.push_back( +2.0642682e-04 );
  lhe_weights.push_back( +2.3176341e-04 );
  lhe_weights.push_back( +2.2866505e-04 );
  lhe_weights.push_back( +2.2562654e-04 );
  lhe_weights.push_back( +2.2264785e-04 );
  lhe_weights.push_back( +2.1972901e-04 );
  lhe_weights.push_back( +2.1407083e-04 );
  lhe_weights.push_back( +2.1133149e-04 );
  lhe_weights.push_back( +2.0865200e-04 );
  lhe_weights.push_back( +2.0603233e-04 );
  lhe_weights.push_back( +2.0347251e-04 );
  lhe_weights.push_back( +2.2851237e-04 );
  lhe_weights.push_back( +2.2544636e-04 );
  lhe_weights.push_back( +2.2244019e-04 );
  lhe_weights.push_back( +2.1949386e-04 );
  lhe_weights.push_back( +2.1660737e-04 );
  lhe_weights.push_back( +2.1378071e-04 );
  lhe_weights.push_back( +2.1101389e-04 );
  lhe_weights.push_back( +2.0830690e-04 );
  lhe_weights.push_back( +2.0565976e-04 );
  lhe_weights.push_back( +2.0307244e-04 );
  lhe_weights.push_back( +2.0054497e-04 );
  lhe_weights.push_back( +2.2528810e-04 );
  lhe_weights.push_back( +2.2225444e-04 );
  lhe_weights.push_back( +2.1928062e-04 );
  lhe_weights.push_back( +2.1636664e-04 );
  lhe_weights.push_back( +2.1351250e-04 );
  lhe_weights.push_back( +2.1071819e-04 );
  lhe_weights.push_back( +2.0798372e-04 );
  lhe_weights.push_back( +2.0530908e-04 );
  lhe_weights.push_back( +2.0269429e-04 );
  lhe_weights.push_back( +2.0013933e-04 );
  lhe_weights.push_back( +1.9764420e-04 );
  lhe_weights.push_back( +2.2209060e-04 );
  lhe_weights.push_back( +2.1908929e-04 );
  lhe_weights.push_back( +2.1614783e-04 );
  lhe_weights.push_back( +2.1326620e-04 );
  lhe_weights.push_back( +2.1044440e-04 );
  lhe_weights.push_back( +2.0768244e-04 );
  lhe_weights.push_back( +2.0498032e-04 );
  lhe_weights.push_back( +2.0233804e-04 );
  lhe_weights.push_back( +1.9975559e-04 );
  lhe_weights.push_back( +1.9723298e-04 );
  lhe_weights.push_back( +1.9477021e-04 );
  lhe_weights.push_back( +2.1891987e-04 );
  lhe_weights.push_back( +2.1595092e-04 );
  lhe_weights.push_back( +2.1304180e-04 );
  lhe_weights.push_back( +2.1019252e-04 );
  lhe_weights.push_back( +2.0740308e-04 );
  lhe_weights.push_back( +2.0467347e-04 );
  lhe_weights.push_back( +2.0200370e-04 );
  lhe_weights.push_back( +1.9939377e-04 );
  lhe_weights.push_back( +1.9684367e-04 );
  lhe_weights.push_back( +1.9435341e-04 );
  lhe_weights.push_back( +1.9192299e-04 );
  lhe_weights.push_back( +2.1577592e-04 );
  lhe_weights.push_back( +2.1283932e-04 );
  lhe_weights.push_back( +2.0996255e-04 );
  lhe_weights.push_back( +2.0714562e-04 );
  lhe_weights.push_back( +2.0438853e-04 );
  lhe_weights.push_back( +2.0169127e-04 );
  lhe_weights.push_back( +1.9905385e-04 );
  lhe_weights.push_back( +1.9647627e-04 );
  lhe_weights.push_back( +1.9395852e-04 );
  lhe_weights.push_back( +1.9150061e-04 );
  lhe_weights.push_back( +1.8910254e-04 );
}

std::string filename="/afs/cern.ch/work/a/anlevin/data/lhe/qed_4_qcd_99_ls0ls1_grid.lhe";

vector<pair<float,float> > grid_points;
vector<float> histo_grid;


void parse_grid()
{
  histo_grid= vector<float>(81);

  grid_points.push_back(pair<float,float>(0,0));

  ifstream infile(filename.c_str());
  assert(infile.is_open());

  while(!infile.eof()){
    std::string line;
    getline(infile,line);

    if(line=="<initrwgt>\0"){
      getline(infile,line);
      assert(line=="<weightgroup type='mg_reweighting'>");
      while(true){
	getline(infile,line);

	if(line=="</initrwgt>\0")
	  return;

	if (line == "</weight>\0" || line=="</weightgroup>\0")
	  continue;

	int param_number1 = 0;
	int param_number2 = 0;
	float param1 = 0;
	float param2 = 0;

	assert(line.find("set param_card anoinputs") != string::npos);
	std::string paraminfo1=line.substr(line.find("set param_card anoinputs ")+std::string("set param_card anoinputs ").size(),line.find("#")-line.find("set param_card anoinputs ")-std::string("set param_card anoinputs ").size());
	stringstream ss1;
	ss1 << paraminfo1;
	ss1 >> param_number1;
	if(param_number1 == 1)
	  ss1 >> param1;
	else if (param_number1==2)
	  ss1 >> param2;
	else
	  assert(0);

	getline(infile,line);

	if (line != "</weight>\0"){

	  assert(line.find("set param_card anoinputs") != string::npos);
	  std::string paraminfo2=line.substr(line.find("set param_card anoinputs ")+std::string("set param_card anoinputs ").size(),line.find("#")-line.find("set param_card anoinputs ")-std::string("set param_card anoinputs ").size());
	  stringstream ss2;
	  ss2 << paraminfo2;
	  ss2 >> param_number2;
	  if(param_number2 == 1)
	    ss2 >> param1;
	  else if (param_number2==2)
	    ss2 >> param2;
	  else
	    assert(0);

	  assert(param_number1 != param_number2);

	}
	
	grid_points.push_back(pair<float,float>(param1,param2));
	
      }
    }
  }

  std::cout << "reweight block not found, exiting" << std::endl;
  exit(1);

}


void plot_lhe_weights_for_one_event()
{

  fill_lhe_weights();
  parse_grid();

  std::cout << "grid_points.size() = " << grid_points.size() << std::endl;
  for(int i = 0; i < grid_points.size(); i++){
    std::cout << grid_points[i].first << ", " << grid_points[i].second << std::endl;
  }
  //change to more convenient units  
  for(int i = 0; i < grid_points.size(); i++){
    grid_points[i].first = grid_points[i].first*pow(10.,10);
    grid_points[i].second = grid_points[i].second*pow(10.,10);
  }
  for(int i = 0; i < grid_points.size(); i++){
    std::cout << grid_points[i].first << ", " << grid_points[i].second << std::endl;
  }

  TH2D * th2d = new TH2D("lhe_weights_hist","lhe weights for one event",11,-2.75,2.75,11,-2.75,2.75);

  assert(lhe_weights.size() == grid_points.size());

  std::cout << "grid_points.size() = " << grid_points.size() << std::endl;

  for (int a = 0; a < lhe_weights.size(); a++){
    std::cout << "a = " << a << std::endl;
    std::cout << "grid_points[a].first = " << grid_points[a].first << std::endl;
    th2d->SetBinContent(th2d->GetXaxis()->FindFixBin(grid_points[a].first), th2d->GetYaxis()->FindFixBin(grid_points[a].second), lhe_weights[a]/lhe_weights[0]);
  }
  
  std::cout << "finished" << std::endl;

}
