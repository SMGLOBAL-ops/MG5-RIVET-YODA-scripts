#! /bin/bash

#Automate Yodascale in directory of parameter values for efficiency


par_name=cW

for i in -0.25 -0.2 -0.15 -0.1 -0.05 0.05 0.1 0.15 0.2 0.25


do

cd EWK_QCD_${par_name}_$i/Events/run_01

gunzip unweighted_events.lhe.gz

weight_val=$(awk '/^#  Average wgt           :/{print $NF'} unweighted_events.lhe)

val=$weightval

val2=$(printf "%.14f" $weight_val)

echo $val2


scalefactor=$(echo "1000 * 3000 * $val2" | bc)

echo 'Yoda file being scaled by:'

echo $scalefactor

echo 'Parameter Value:'

echo $i

yodascale -c ".* ${scalefactor}x" EWK_QCD_${par_name}_${i}_paramvalue.yoda

mv EWK_QCD_${par_name}_${i}_paramvalue-scaled.yoda /unix/bsmxsec/smustafa/mount/batchfarm/scaled_yoda_files_temp_folder

cd ../../../

done
