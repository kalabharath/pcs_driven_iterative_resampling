#!/bin/bash
# Setup for PBS load balancing
#PBS -P xc4
#PBS -q normal
#PBS -l walltime=1:00:00
#PBS -l mem=128GB
#PBS -l ncpus=128
#PBS -l wd

# Load required module to run mpi compiled rosetta executables
module load openmpi

# Variable flags
################
# Change ./config.txt file
# Please change the executable and database paths according to your operating system.
# For arg1 and arg2, give input 9 and 3 residue fragment library files.
# For arg3, give the target protein starting model in pdb format.
# For arg4, give input broker file.
# For arg5, give number of structures to generate, typically 1,000 structures are needed. Atleast generate 100.
# For arg6, give the ouput silent file name.
# For arg7, give output score file name.
# Protein system dengue virus protease (dvp)

Executable="/short/xc4/kbp502/gps4rosetta/Rosetta/main/source/bin/minirosetta.mpi.linuxgccrelease"
database="-database /short/xc4/kbp502/gps4rosetta/Rosetta/main/database"
protein=$(sed -n '2p' config.txt)
echo $protein
arg1="-abinitio::increase_cycles 5"
arg3="-nstruct 1016"
arg9="-mute all"
arg5="-frag9 ./frag9_${protein}_r0.tab"
arg6="-frag3 ./frag3_${protein}_r0.tab"
arg7="-native ../setup/idealized_$protein.pdb"
arg8="-out::file::silent $protein.silent"
arg2="-abinitio::rg_reweight 0.5 -abinitio::rsd_wt_helix 0.5 -abinitio::rsd_wt_loop 0.5 -abinitio::use_filters false"

mpirun="mpirun -np 128"

run="$mpirun $Executable $database $fasta $arg1 $arg2 $arg3 $arg4 $arg5 $arg6 $arg7 $arg8 $arg9 $arg10 $patch_flag $broker_flag $exclude $extras"

echo $run
$run

cat *.silent > ${protein}.silent_file ; rm *.silent

# Compute the weights
python auto_rescore.py > /dev/null
python auto_pcswt.py > /dev/null
# Automatically submit the next PBS batch script to run GPS-Rosetta
qsub auto_gps.sh
