#!/bin/sh
#@ account_no = k104
#@ job_name= relax_top_clusters
#@ output=$(job_name).out
#@ error=$(job_name).err
#@ wall_clock_limit=72:00:00 
# neser-specific
#@ job_type=parallel
#@ node=1
#@ tasks_per_node=8
#@ queue

# Rosetta Alltom Classic Relax script

#relax.linuxgccrelease -database /home/kalabharath/mini_rosetta_database -out:pdb  -in:file:s dvp_model.pdb -nstruct 10 -wobblemoves -constant_seed  -relax::stage1_ramp_cycles 3 -relax::min_tolerance 0.02 -relax:stage2_cycles 4 -relax:stage3_cycles 4 -mute core.util.prof -mute core.io.database



Executable="/home/kalabharath/Github_rosetta/Rosetta/main/source/bin/relax.mpi.linuxgccrelease"
database="-database /home/kalabharath/Github_rosetta/Rosetta/main/database"
arg0="-in:file:silent $1"
arg2="-out:file:silent relax_top.silent"
arg3="-nstruct 10"
arg4="-wobblemoves "
arg5="-relax::stage1_ramp_cycles 3 -relax::min_tolerance 0.02 -relax::stage2_cycles 4 -relax:stage3_cycles 4"
arg6="-mute core.util.prof -mute all"
arg9="-constraints::cst_fa_file constraints.cst"
arg7="-in:file:native ../setup/idealized_2lf2.pdb"
mpirun="mpirun --hostfile mpi_hostfile -np 30"
run="$mpirun $Executable $database $arg0 $arg1 $arg2 $arg3 $argx $arg4 $arg5 $arg6 $arg7 $arg8 $arg9"
echo $run
$run
