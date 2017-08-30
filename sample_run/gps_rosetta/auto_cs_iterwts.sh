#!/bin/bash
#PBS -P xc4
#PBS -q normal
#PBS -l walltime=2:00:00  
#PBS -l mem=256GB
#PBS -l ncpus=256
#PBS -l wd   

Executable="/short/xc4/kbp502/gps4rosetta/Rosetta/main/source/bin/minirosetta.mpi.linuxgccrelease"
arg4="-database /short/xc4/kbp502/gps4rosetta/Rosetta/main/database"

protein=$(sed -n '1p' config.txt)
iter=$(sed -n '3p' config.txt)
arg1="-abinitio::increase_cycles 1.0"
arg3="-nstruct 1016"
arg9="-mute all"
arg5="-frag9 ./frag9_${protein}_r${iter}.tab"
arg6="-frag3 ./frag3_${protein}_r${iter}.tab"
#arg7="-native ../setup/idealized_$protein.pdb"
arg7="-in:file:native ../setup/idealized_$protein.pdb"

arg8="-out::file::silent $protein.silent"
#arg9="-constraints:cst_file constraints.cst"
arg2="-abinitio::rg_reweight 0.5 -abinitio::rsd_wt_helix 0.5 -abinitio::rsd_wt_loop 0.5 -abinitio::use_filters false"

mpirun="mpirun -np 256"

run="$mpirun $Executable $fasta $arg1 $arg2 $arg3 $arg4 $arg5 $arg6 $arg7 $arg8 $arg9 $arg10 $patch_flag $broker_flag $exclude $extras"

echo $run
$run

cat *.silent > ${protein}_wts_r${iter}.silent_file ; rm *.silent

python auto_iter_rescore.py > /dev/null
python auto_iter_pcswt.py > /dev/null


