#input_dir=eos/cms/store/user/anlevin/DoubleMuon/flattish_ntuples_v213
input_dir=eos/cms/store/user/anlevin/DoubleEG/flattish_ntuples_v216


filelist=""; 

for dir1 in `/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select ls ${input_dir}`; 

do 

echo $dir1

for dir2 in `/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select ls ${input_dir}/${dir1}`; 

do

for file in `/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select ls ${input_dir}/${dir1}/${dir2} | grep -v failed`; 

do 

#echo $file

filelist=$filelist" "root://eoscms//${input_dir}/${dir1}/${dir2}/$file; 

done; 

done;

done;

echo $filelist; 

hadd output_tree.root $filelist;
