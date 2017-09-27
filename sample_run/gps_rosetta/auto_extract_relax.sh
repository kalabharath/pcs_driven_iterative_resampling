#!/bin/bash
#PBS -P xc4
#PBS -q normal
#PBS -l walltime=5:00:00
#PBS -l mem=64GB
#PBS -l ncpus=64
#PBS -l wd

#######################################
python auto_extract_ctop.py > /dev/null
#######################################

Executable_path=$(sed -n '4p' config.txt)
Executable="$(cut -d'=' -f2 <<<"$Executable_path")"
database_path=$(sed -n '5p' config.txt)
database="$(cut -d'=' -f2 <<<"$database_path")"
database="-database $database"
protein=$(sed -n '6p' config.txt)
protein="$(cut -d'=' -f2 <<<"$protein")"
iter=$(sed -n '8p' config.txt)
iter="$(cut -d'=' -f2 <<<"$iter")"
arg0="-in:file:silent  top_${protein}_r${iter}.silent_file"
arg1="-out:file:silent relax_top_${protein}_r${iter}.silent_file"
arg2="-in:file:native ../setup/idealized_$protein.pdb"
arg3="-mute all"
mpirun="mpirun -np 64"
run="$mpirun $Executable $database $arg0 $arg1 $arg2 $arg3"
echo $run
$run


#######################################
python auto_relax_rescore.py > /dev/null
python auto_extract_rtop.py > /dev/null
python auto_silent2database.py > s2db_r${iter}.log
#######################################
