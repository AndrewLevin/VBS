operators="\
FS0
FS1
FM0
FM1
FM6
FM7
FT0
FT1
FT2
"

for operator in $operators
do
python2.6 select_events.py --config config_reweighted_v1_${operator}.txt
done
