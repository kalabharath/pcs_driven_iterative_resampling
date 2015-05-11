#!/bin/bash
#PBS -P xc4
#PBS -q normal
#PBS -l walltime=2:00:00  
#PBS -l mem=64GB
#PBS -l ncpus=64
#PBS -l wd   

#######################################
python auto_extract_ctop.py > /dev/null
#######################################

Executable="/short/xc4/kbp502/gps4rosetta/Rosetta/main/source/bin/relax.mpi.linuxgccrelease"
database="-database /short/xc4/kbp502/gps4rosetta/Rosetta/main/database"

protein=$(sed -n '1p' config.txt)
iter=$(sed -n '3p' config.txt)

arg0="-in:file:silent  top_${protein}_r${iter}.silent_file"
arg2="-out:file:silent relax_top_${protein}_r${iter}.silent_file"
arg3="-nstruct 5"
arg4="-wobblemoves"
arg5="-relax::stage1_ramp_cycles 3 -relax::min_tolerance 0.02 -relax::stage2_cycles 4 -relax:stage3_cycles 4"
arg6="-mute all -score:patch talaris2013.wts"
#arg9="-constraints::cst_fa_file constraints.cst -constraints::cst_file constraints.cst -cst_fa_weight 10 -cst_weight 10"
arg7="-in:file:native ../setup/idealized_$protein.pdb"
mpirun="mpirun -np 64"
run="$mpirun $Executable $database $arg0 $arg1 $arg2 $arg3 $argx $arg4 $arg5 $arg6 $arg7 $arg8 $arg9"
echo $run
$run


#######################################
python auto_relax_rescore.py > /dev/null
python auto_extract_rtop.py > /dev/null
python auto_silent2database.py > s2db_r${iter}.log
#######################################
