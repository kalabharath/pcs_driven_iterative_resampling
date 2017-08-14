import sys, os


fin=open('config.txt','r')
protein=fin.readline().rstrip()
fin.close()

for i in range(0,10):
    filename="pcs_"+protein+"_relax_top_rescore_r"+str(i)+".fsc"
    filecheck=os.path.isfile(filename)
    if filecheck:
        if i == 0:
            print "plot '"+filename+"' using 41:2 with points",
        else:
            print ",'"+filename+"' using 41:2 with points",
