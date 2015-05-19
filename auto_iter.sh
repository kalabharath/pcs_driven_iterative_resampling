#!/usr/bin/env bash
#PBS -P xc4
#PBS -q normal
#PBS -l walltime=10:00:00
#PBS -l mem=2000GB
#PBS -l ncpus=1008
#PBS -l wd

module load openmpi

Executable="/short/xc4/kbp502/gps4rosetta/Rosetta/main/source/bin/minirosetta.mpi.linuxgccrelease"
database="-database /short/xc4/kbp502/gps4rosetta/Rosetta/main/database"
protein=$(sed -n '1p' config.txt)
iter=$(sed -n '3p' config.txt)
arg1="-abinitio::increase_cycles 4.0"
arg2="-abinitio::rg_reweight 0.5 -abinitio::rsd_wt_helix 0.5 -abinitio::rsd_wt_loop 0.5 -abinitio::use_filters false"
arg3="-nstruct 2012"
arg4="-mute all"
arg5="-frag9 ./frag9_${protein}_r${iter}.tab"
arg6="-frag3 ./frag3_${protein}_r${iter}.tab"
arg7="-out::file:silent ${protein}_r${iter}.silent_file"
arg8="-native ../setup/idealized_$protein.pdb"
#arg8="-in:file:native ../setup/idealized_$protein.pdb -native_exclude_res 1 2 3 4 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 37 38 39 40 41 42 43 44 45 46 47 48 54 55 56 57 66 67 68 84 85 86 87 88 89 97 98 99 100 101 102 109 110 111 112 113 114 115 126 127 128 129 130 137 138 139 140 141 142 143 144 145 151 152 153 154 155"
patch1="-abinitio::stage1_patch ${protein}_r${iter}.wts"
patch2="-abinitio::stage2_patch ${protein}_r${iter}.wts"
patch3="-abinitio::stage3a_patch ${protein}_r${iter}.wts"
patch4="-abinitio::stage3b_patch ${protein}_r${iter}.wts"
patch5="-abinitio::stage4_patch ${protein}_r${iter}.wts"

patch_flag="$patch1 $patch2 $patch3 $patch4 $patch5"
broker_flag="-broker::setup ../setup/broker-ts4.txt -run:protocol broker -overwrite"

mpirun="mpirun -np 1008"
run="$mpirun $Executable $database $arg1 $arg2 $arg3 $arg4 $arg5 $arg6 $arg7 $arg8 $arg9 $arg10 $patch_flag $broker_flag"
echo $run
$run

new_job="qsub auto_extract_relax.sh"
echo $new_job
$new_job
