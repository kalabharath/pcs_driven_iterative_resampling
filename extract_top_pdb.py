import sys,os


fin=open('config.txt','r')
protein=fin.readline().rstrip()
fin.close()

infile = "pcs_"+protein+"_relax_top_rescore_r10.fsc"
fin=open(infile,'r')
lines = fin.readlines()
fin.close()

pdb=''
rms=''
score=999.999

for i in range(1,len(lines)):
    sline=lines[i].split()
    pcsscore=float(sline[7])+float(sline[8])+float(sline[9])
    if float(pcsscore) < score:
        score=float(pcsscore)
        pdb = sline[-1]
        rms = sline[-5]
"""
for i in range(1,len(lines)):
    sline=lines[i].split()
    pcsscore=float(sline[1])
    if float(pcsscore) < score:
        score=float(pcsscore)
        pdb = sline[-1]
        rms = sline[-5]
"""
print score, pdb, rms

EXECUTABLE="/rsc/tungsten/data2/Rosetta_freeze/rosetta1505/main/source/bin/extract_pdbs.default.linuxgccrelease "
DATABASE="-database /rsc/tungsten/data2/Rosetta_freeze/rosetta1505/main/database "
PDBSCORE="-in:file:silent top_relax_top_"+protein+"_r10.silent_file "
OUT="-in:file:tags "+pdb[:-5]

run= EXECUTABLE+DATABASE+PDBSCORE+OUT
print run

os.system(run)

cp_file = "cp "+pdb[:-5]+"*.pdb "+pdb[:-5]+"_"+str(rms)+".pdb"

os.system(cp_file)
