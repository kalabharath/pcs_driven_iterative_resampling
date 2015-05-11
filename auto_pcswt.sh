#!/bin/bash
#PBS -P xc4
#PBS -q normal
#PBS -l walltime=00:30:00  
#PBS -l mem=4GB
#PBS -l ncpus=2   
#PBS -l wd   

python auto_rescore.py > /dev/null
python auto_pcswt.py > /dev/null
qsub auto_gps.sh



