import sys,os

cp_shell=("cp ../../01_1s0p/gps/*.sh ./")

os.system(cp_shell)

cp_py=("cp ../../01_1s0p/gps/*.py ./")

os.system(cp_py)

cp_wts=("cp ../../01_1s0p/gps/pcsweight.patch ./")

os.system(cp_wts)

cp_t13=("cp ../../01_1s0p/gps/talaris2013.wts ./")

os.system(cp_t13)


#make config file

dirname, filename = os.path.split(os.path.abspath(__file__))

protein = dirname.split('/')[-2].split("_")[-1]

fout=open("config.txt",'w')

fout.write(protein)
fout.write("\n")
fout.write("10\n")
fout.write("0\n")
