// c++ -o checkMomentum_00 `root-config --glibs --cflags` -lm checkMomentum_00.cpp
#include "LHEF.h"
#include <iomanip>
#include <vector>
#include <iostream>
#include <string>
#include <sstream>
#include "TH1.h"
#include "TFile.h"

#include "TLorentzVector.h"

// CINT does not understand some files included by LorentzVector
#include "Math/Vector3D.h"
#include "Math/Vector4D.h"

using namespace ROOT::Math;
using namespace std ;

double DeltaPhi(double phi1, double phi2)
{
  // Compute DeltaPhi between two given angles. Results is in [-pi/2,pi/2].
  double dphi = TMath::Abs(phi1-phi2);
  while (dphi>TMath::Pi())
    dphi = TMath::Abs(dphi - TMath::TwoPi());
  return(dphi);
}

TLorentzVector buildP (const LHEF::HEPEUP & event, int iPart)
{
  TLorentzVector dummy ;
  dummy.SetPxPyPzE (
      event.PUP.at (iPart).at (0), // px
      event.PUP.at (iPart).at (1), // py
      event.PUP.at (iPart).at (2), // pz
      event.PUP.at (iPart).at (3) // E
    ) ;
  return dummy ;  
}



int main(int argc, char ** argv) 
{
  if(argc < 5)
    {
      cout << "Usage:   " << argv[0] 
           << " input_ewk.lhe input_qcd.lhe input_ewk_plus_qcd.lhe outputfilename" << endl ;
      return -1;
    }

  std::ifstream ifs_ewk (argv[1]) ;
  LHEF::Reader reader_ewk (ifs_ewk) ;

  std::ifstream ifs_qcd (argv[2]) ;
  LHEF::Reader reader_qcd (ifs_qcd) ;

  std::ifstream ifs_ewk_plus_qcd (argv[3]) ;
  LHEF::Reader reader_ewk_plus_qcd (ifs_ewk_plus_qcd) ;

  std::string outputfilename = argv[4];

  TH1F mjj_ewk ("mjj_ewk", "mjj_ewk", 10, 500, 2000) ;
  TH1F mjj_qcd ("mjj_qcd", "mjj_qcd", 10, 500, 2000) ;
  TH1F mjj_ewk_plus_qcd ("mjj_ewk_plus_qcd", "mjj_ewk_plus_qcd", 10, 500, 2000) ;

  int n_events_ewk=0;
  int n_sel_events_ewk=0;

  //PG loop over input events
  while (reader_ewk.readEvent ()) 
    {

      n_events_ewk++;


      std::vector<TLorentzVector> quarks;
      std::vector<TLorentzVector> leptons;
      std::vector<TLorentzVector> neutrinos;

      if ( reader_ewk.outsideBlock.length() ) std::cout << reader_ewk.outsideBlock;

      // loop over particles in the event
      for (int iPart = 0 ; iPart < reader_ewk.hepeup.IDUP.size (); ++iPart) 
        {
           // outgoing particles          
           if (reader_ewk.hepeup.ISTUP.at (iPart) == 1)
             {
               if (abs (reader_ewk.hepeup.IDUP.at (iPart)) == 1 || abs (reader_ewk.hepeup.IDUP.at (iPart)) == 2 || abs (reader_ewk.hepeup.IDUP.at (iPart)) == 3 || abs (reader_ewk.hepeup.IDUP.at (iPart)) == 4 || abs (reader_ewk.hepeup.IDUP.at (iPart)) == 21 )
                 {
                   TLorentzVector vec = buildP (reader_ewk.hepeup, iPart) ;
                   quarks.push_back(vec);
                 }
               if (abs (reader_ewk.hepeup.IDUP.at (iPart)) == 12 || abs (reader_ewk.hepeup.IDUP.at (iPart)) == 14 || abs (reader_ewk.hepeup.IDUP.at (iPart)) == 16 )
                 {
                   TLorentzVector vec = buildP (reader_ewk.hepeup, iPart) ;
                   neutrinos.push_back(vec);
                 }
               if (abs (reader_ewk.hepeup.IDUP.at (iPart)) == 11 || abs (reader_ewk.hepeup.IDUP.at (iPart)) == 13 /*|| abs (reader_ewk.hepeup.IDUP.at (iPart)) == 15 */ )
                 {
                   TLorentzVector vec = buildP (reader_ewk.hepeup, iPart) ;
                   leptons.push_back(vec);
                 }
 
             } // outgoing particles
        } // loop over particles in the event

      int n_leptons_with_pt_gt_20 = 0;

      for (int i = 0; i < leptons.size(); i++){
	if (leptons[i].Pt() > 20) n_leptons_with_pt_gt_20++;
      }
      
      if (n_leptons_with_pt_gt_20 < 2)
	continue;


      TLorentzVector neutrinos_sum;

      for (int i=0; i < neutrinos.size(); i++){
	neutrinos_sum+=neutrinos[i];
      }

      if (neutrinos_sum.Pt() < 30)
	continue;

      assert(quarks.size() == 2);

      if(quarks.size() != 2){
	std::cout << "found event without exactly two quarks" << std::endl;
	continue;
      }

      if(abs(quarks[0].Eta() - quarks[1].Eta()) < 3.5)
	 continue;

      if(quarks[0].Pt() < 30)
	continue;

      if(quarks[1].Pt() < 30)
	continue;

      n_sel_events_ewk++;
      mjj_ewk.Fill( (quarks[0] + quarks[1]).M() );

    } //PG loop over input events


  std::cout << "n_events_ewk = " << n_events_ewk << std::endl;
  std::cout << "n_sel_events_ewk = " << n_sel_events_ewk << std::endl;

  int n_events_qcd=0;
  int n_sel_events_qcd=0;

  //PG loop over input events
  while (reader_qcd.readEvent ()) 
    {

      n_events_qcd++;

      std::vector<TLorentzVector> quarks;
      std::vector<TLorentzVector> neutrinos;
      std::vector<TLorentzVector> leptons;

      if ( reader_qcd.outsideBlock.length() ) std::cout << reader_qcd.outsideBlock;

      // loop over particles in the event
      for (int iPart = 0 ; iPart < reader_qcd.hepeup.IDUP.size (); ++iPart) 
        {

           // outgoing particles          
           if (reader_qcd.hepeup.ISTUP.at (iPart) == 1)
             {
               if (abs (reader_qcd.hepeup.IDUP.at (iPart)) == 1 || abs (reader_qcd.hepeup.IDUP.at (iPart)) == 2 || abs (reader_qcd.hepeup.IDUP.at (iPart)) == 3 || abs (reader_qcd.hepeup.IDUP.at (iPart)) == 4 || abs (reader_qcd.hepeup.IDUP.at (iPart)) == 21 )
                 {
                   TLorentzVector vec = buildP (reader_qcd.hepeup, iPart) ;
                   quarks.push_back(vec);
                 }
                if (abs (reader_qcd.hepeup.IDUP.at (iPart)) == 12 || abs (reader_qcd.hepeup.IDUP.at (iPart)) == 14 || abs (reader_qcd.hepeup.IDUP.at (iPart)) == 16 )
                 {
                   TLorentzVector vec = buildP (reader_qcd.hepeup, iPart) ;
                   neutrinos.push_back(vec);
                 }
                if (abs (reader_qcd.hepeup.IDUP.at (iPart)) == 11 || abs (reader_qcd.hepeup.IDUP.at (iPart)) == 13 /*|| abs (reader_qcd.hepeup.IDUP.at (iPart)) == 15 */)
                 {
                   TLorentzVector vec = buildP (reader_qcd.hepeup, iPart) ;
                   leptons.push_back(vec);
                 }
             } // outgoing particles
        } // loop over particles in the event

      int n_leptons_with_pt_gt_20 = 0;

      for (int i = 0; i < leptons.size(); i++){
	if (leptons[i].Pt() > 20) n_leptons_with_pt_gt_20++;
      }
      
      if (n_leptons_with_pt_gt_20 < 2)
	continue;


      TLorentzVector neutrinos_sum;

      for (int i=0; i < neutrinos.size(); i++){
	neutrinos_sum+=neutrinos[i];
      }

      if (neutrinos_sum.Pt() < 30)
	continue;

      assert(quarks.size() == 2);

      if(quarks.size() != 2){
	std::cout << "found event without exactly two quarks" << std::endl;
	continue;
      }

      if(abs(quarks[0].Eta() - quarks[1].Eta()) < 3.5)
	 continue;

      if(quarks[0].Pt() < 30)
	continue;

      if(quarks[1].Pt() < 30)
	continue;

      n_sel_events_qcd++;
      mjj_qcd.Fill( (quarks[0] + quarks[1]).M() );

    } //PG loop over input events


  std::cout << "n_events_qcd = " << n_events_qcd << std::endl;
  std::cout << "n_sel_events_qcd = " << n_sel_events_qcd << std::endl;

  int n_events_ewk_plus_qcd=0;
  int n_sel_events_ewk_plus_qcd=0;

  //PG loop over input events
  while (reader_ewk_plus_qcd.readEvent ()) 
    {

      n_events_ewk_plus_qcd++;

      std::vector<TLorentzVector> quarks;
      std::vector<TLorentzVector> neutrinos;
      std::vector<TLorentzVector> leptons;
      

      if ( reader_ewk_plus_qcd.outsideBlock.length() ) std::cout << reader_ewk_plus_qcd.outsideBlock;

      // loop over particles in the event
      for (int iPart = 0 ; iPart < reader_ewk_plus_qcd.hepeup.IDUP.size (); ++iPart) 
        {
           // outgoing particles          
           if (reader_ewk_plus_qcd.hepeup.ISTUP.at (iPart) == 1)
             {
               if (abs (reader_ewk_plus_qcd.hepeup.IDUP.at (iPart)) == 1 || abs (reader_ewk_plus_qcd.hepeup.IDUP.at (iPart)) == 2 || abs (reader_ewk_plus_qcd.hepeup.IDUP.at (iPart)) == 3 || abs (reader_ewk_plus_qcd.hepeup.IDUP.at (iPart)) == 4  || abs (reader_ewk_plus_qcd.hepeup.IDUP.at (iPart)) == 21)
                 {
                   TLorentzVector vec = buildP (reader_ewk_plus_qcd.hepeup, iPart) ;
                   quarks.push_back(vec);
                 }
                if (abs (reader_ewk_plus_qcd.hepeup.IDUP.at (iPart)) == 12 || abs (reader_ewk_plus_qcd.hepeup.IDUP.at (iPart)) == 14 || abs (reader_ewk_plus_qcd.hepeup.IDUP.at (iPart)) == 16 )
                 {
                   TLorentzVector vec = buildP (reader_ewk_plus_qcd.hepeup, iPart) ;
                   neutrinos.push_back(vec);
                 }
                if (abs (reader_ewk_plus_qcd.hepeup.IDUP.at (iPart)) == 11 || abs (reader_ewk_plus_qcd.hepeup.IDUP.at (iPart)) == 13 /*|| abs (reader_ewk_plus_qcd.hepeup.IDUP.at (iPart)) == 15 */ )
                 {
                   TLorentzVector vec = buildP (reader_ewk_plus_qcd.hepeup, iPart) ;
                   leptons.push_back(vec);
                 }
             } // outgoing particles
        } // loop over particles in the event

      int n_leptons_with_pt_gt_20 = 0;

      for (int i = 0; i < leptons.size(); i++){
	if (leptons[i].Pt() > 20) n_leptons_with_pt_gt_20++;
      }
      
      if (n_leptons_with_pt_gt_20 < 2)
	continue;

     TLorentzVector neutrinos_sum;

      for (int i=0; i < neutrinos.size(); i++){
	neutrinos_sum+=neutrinos[i];
      }

      if (neutrinos_sum.Pt() < 30)
	continue;

      assert(quarks.size() == 2);

      if(quarks.size() != 2){
	std::cout << "found event without exactly two quarks" << std::endl;
	continue;
      }

      if(abs(quarks[0].Eta() - quarks[1].Eta()) < 3.5)
	 continue;

      if(quarks[0].Pt() < 30)
	continue;

      if(quarks[1].Pt() < 30)
	continue;
 
      n_sel_events_ewk_plus_qcd++;
      mjj_ewk_plus_qcd.Fill( (quarks[0] + quarks[1]).M() );


    } //PG loop over input events


  std::cout << "n_events_ewk_plus_qcd = " << n_events_ewk_plus_qcd << std::endl;
  std::cout << "n_sel_events_ewk_plus_qcd = " << n_sel_events_ewk_plus_qcd << std::endl;

  TFile f (outputfilename.c_str(), "recreate") ;
  mjj_ewk.Write();
  mjj_qcd.Write();
  mjj_ewk_plus_qcd.Write();
  f.Close () ;

  return 0 ;
}
