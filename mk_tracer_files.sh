for ((i=0; i<=10000; i+=20))
do for ((j=i; j<(($i+20)); j++))
do ./iSALEPlot -f $1 -m $2 -T $j < /dev/null > $3/remote_log.txt 2>&1 & done
wait
done

