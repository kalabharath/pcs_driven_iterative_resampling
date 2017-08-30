#!/bin/bash
#PBS -P xc4
#PBS -q normal
#PBS -l walltime=48:00:00  
#PBS -l mem=256GB
#PBS -l ncpus=240
#PBS -l wd   

module load openmpi

Executable="/short/xc4/kbp502/gps4rosetta/Rosetta/main/source/bin/minirosetta.mpi.linuxgccrelease"
database="-database /short/xc4/kbp502/gps4rosetta/Rosetta/main/database"
protein=$(sed -n '1p' config.txt)
arg1="-abinitio::increase_cycles 5"
arg2="-abinitio::rg_reweight 0.5 -abinitio::rsd_wt_helix 0.5 -abinitio::rsd_wt_loop 0.5 -abinitio::use_filters false"
arg3="-nstruct 2000"
arg4="-mute all"
#arg5="-frag9 ./hacked_renum_frag9_${protein}_r0.tab"
#arg6="-frag3 ./hacked_renum_frag3_${protein}_r0.tab"
arg5="-frag9 ./frag9_${protein}_r0.tab"
arg6="-frag3 ./frag3_${protein}_r0.tab"
#arg7="-native ../setup/idealized_$protein.pdb"
arg7="-in:file:native ../setup/idealized_$protein.pdb"
arg8="-out::file:silent ${protein}_r0.silent_file"
#arg9="-constraints:cst_file constraints.cst"
patch1="-abinitio::stage1_patch ${protein}_r0.wts"
patch2="-abinitio::stage2_patch ${protein}_r0.wts"
patch3="-abinitio::stage3a_patch ${protein}_r0.wts"
patch4="-abinitio::stage3b_patch ${protein}_r0.wts"
patch5="-abinitio::stage4_patch ${protein}_r0.wts"
#exclude="-in::file::native_exclude_res 1 2 3 4 33 34 35 36 37 38 52 53 66 67 68 69 70 71 83 84 85 86 93 94 95 96 98 99 100 101 113 121 122 123 124 125 126 127 142 143 144 145 146 161 162 163 164 165 166 167"
patch_flag="$patch1 $patch2 $patch3 $patch4 $patch5"
broker_flag="-broker::setup ../setup/broker-ts3.txt -run:protocol broker -overwrite"
mpirun="mpirun -np 240"
run="$mpirun $Executable $database $arg1 $arg2 $arg3 $arg4 $arg5 $arg6 $arg7 $arg8 $arg9 $arg10 $patch_flag $broker_flag $exclude"
echo $run
$run

qsub auto_extract_relax.sh
