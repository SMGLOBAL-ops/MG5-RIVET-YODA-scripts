#! /bin/bash
#PBS -o /unix/bsmxsec/smustafa/mount/batchfarm
#PBS -e /unix/bsmxsec/smustafa/mount/batchfarm/err_files

#Specify name of parameter: 

par_name=cW

cd /unix/bsmxsec/smustafa/mount/batchfarm

n=0

mkdir "${par_name}"
cd ${par_name}


  #for i in -1.0 -0.75 -0.50 -0.25 1.00000e-99 0.25 0.50 0.75 1.0
   for i in -0.25 -0.2 -0.15 -0.1 -0.05 0.05 0.1 0.15 0.2 0.25
do


cp /home/smustafa/SFNP/MG5_aMC_v2_7_2/models/restrict_SMlimit_massless.dat /home/smustafa/SFNP/MG5_aMC_v2_7_2/models/SMEFTsim_A_U35_MwScheme_UFO_v2_1/restrict_${par_name}_${n}.dat
find /home/smustafa/SFNP/MG5_aMC_v2_7_2/models/SMEFTsim_A_U35_MwScheme_UFO_v2_1/restrict_${par_name}_${n}.dat -type f -exec sed -i "s/21 1.000000e-99 # cW /21 $i # cW /g" {} \;

################################################# Run MG5

~/SFNP/MG5_aMC_v2_7_2/bin/mg5_aMC  << EOF
import model SMEFTsim_A_U35_MwScheme_UFO_v2_1-${par_name}_${n}
generate p p > Z Z j j QCD==0
add process p p > Z Z j j QCD==2
output EWK_QCD_${par_name}_${i}
launch
shower = pythia8
0
set nevents 100000
set ebeam1 7000
set ebeam2 7000
0
exit
EOF
cd $PWD/EWK_QCD_${par_name}_${i}/Events/run_01/

gunzip unweighted_events.lhe
~/MadGraph5_v1_5_14/DECAY/decay << EOF
1
unweighted_events.lhe
decayed.lhe
z
4
EOF
mv unweighted_events.lhe old.lhe
mv decayed.lhe unweighted_events.lhe
gzip unweighted_events.lhe
mkfifo tag_1_pythia8_events.hepmc.fifo
sleep 1s
rm tag_1_pythia8.cmd
cp /home/smustafa/SFNP/MG5_aMC_v2_7_2/tag_1_pythia8.cmd .
sleep 1s
cp ~/Analysis/RivetVBSextra.so .
./run_shower.sh &
########################################## run Rivet
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase; source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh; asetup 21.6.6,AthGeneration;source setupRivet.sh; unset PYTHONHOME
sleep 2s
rivet -a ATLAS_2019_I00001 --pwd tag_1_pythia8_events.hepmc.fifo -o EWK_QCD_${par_name}_${i}_paramvalue.yoda
n=$((n+1))
cd ../../../
done  
