function calc
{
    awk "BEGIN {print $*}";
}

lumis="\
900
160
"

filename="higgs_no_higgs_datacard.txt"

for lumi in $lumis
do
  > datacard.txt
  
  cat higgs_no_higgs_datacard.txt |
  while read -d' ' line
    do 
    if [ "$line" = "0.103" ]
	then
	echo -n `calc 0.103*$lumi` >> datacard.txt
    elif [ "$line" = "0.124" ]
	then
	echo -n `calc 0.124*$lumi` >> datacard.txt
    else    
	echo -n "$line " >> datacard.txt
    fi
    
  #echo $line
    
  done

  echo "" >> datacard.txt

  echo "lumi="$lumi

  combine datacard.txt -M ProfileLikelihood --expectSignal=1 --significance -t -1 -m 125 -n Expected234 | grep Significance
done
