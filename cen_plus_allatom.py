"""
Simple demo of a scatter plot.


N = 50
x = np.random.rand(N)
y = np.random.rand(N)
colors = np.random.rand(N)
area = np.pi * (15 * np.random.rand(N))**2 # 0 to 15 point radiuses

plt.scatter(x, y, s=area, c=colors, alpha=0.5)
plt.show()

"""

def getIndex(line):
    index_array={}
    tarray=line.split()
    for stype in tarray:
        if stype.replace(" ","")=='score':
            tindex= tarray.index(stype)
            index_array[stype]=tindex
        if stype.replace(" ","")=='pcsTs1':
            tindex= tarray.index(stype)
            index_array[stype]=tindex
        if stype.replace(" ","")=='pcsTs2':
            tindex= tarray.index(stype)
            index_array[stype]=tindex
        if stype.replace(" ","")=='pcsTs3':
            tindex= tarray.index(stype)
            index_array[stype]=tindex
        if stype.replace(" ","")=='pcsTs4':
            tindex= tarray.index(stype)
            index_array[stype]=tindex
        if stype.replace(" ","")=='rms':
            tindex= tarray.index(stype)
            index_array[stype]=tindex
    return index_array

import numpy as np
import matplotlib.pyplot as plt
import os.path

color_map = ['#E80000', '#F63A00',  '#FF6F00', '#DA8500', '#FFC402', '#AEEE00', '#04E0AF', '#00AEDA','#0068E8', '#000BE4', '#3800DA', 'black']
color_map.reverse()


X_rmsd=[]
Y_pcs=[]
Y_total=[]

fin=open('config.txt','r')
protein=fin.readline().rstrip()
fin.close()


for i in range(0,11):
    ex="grep SCORE "+protein+"_r"+str(i)+".silent_file > temp"+str(i)+".csc"
    print ex
    os.system(ex)



plt.subplot(1,2,1)
plt.xlim((0,25))
# plt.ylabel('Rosetta + PCS energy')
plt.ylabel('PCS energy')
plt.xlabel('RMSD [$\AA \angstrom$]')
plt.title('Centroid Mode')
for i in range(0,11):
    t_rmsd=[]
    t_pcs=[]
    t_score=[]
    fin = 'temp'+str(i)+".csc"
    if os.path.isfile(fin):
        with open(fin, 'r') as infile:
            lines = infile.readlines()
    line = lines[0]
    indix_dict = getIndex(line)
    for i in range(1,len(lines)):
        tline = lines[i].split()
        t_rmsd.append(float(tline[indix_dict['rms']]))
        t_pcs1 = float(tline[indix_dict['pcsTs1']])
        t_pcs2 = float(tline[indix_dict['pcsTs2']])
        t_pcs3 = float(tline[indix_dict['pcsTs3']])
        t_pcs_total = t_pcs1+t_pcs2+t_pcs3
        t_pcs.append(t_pcs_total)
        t_score.append(float(tline[indix_dict['score']]))
    X_rmsd.append(t_rmsd)
    Y_pcs.append(t_pcs)
    Y_total.append(t_score)
for i in range(0,11):
    # plt.plot(X_rmsd[i], Y_total[i], color=color_map[i], linestyle='point', marker ='', markersize=12)
    # plt.scatter(X_rmsd[i], Y_total[i], color=color_map[i])
    plt.scatter(X_rmsd[i], Y_pcs[i], color=color_map[i])

plt.subplot(1,2,2)
X_rmsd=[]
Y_pcs=[]
Y_total=[]


for i in range(0,11):
    t_rmsd=[]
    t_pcs=[]
    t_score=[]
    #fin = 'temp'+str(i)+".csc"
    fin="pcs_"+protein+"_relax_top_rescore_r"+str(i)+".fsc"
    if os.path.isfile(fin):
        with open(fin, 'r') as infile:
            lines = infile.readlines()
    line = lines[0]
    indix_dict = getIndex(line)
    for i in range(1,len(lines)):
        tline = lines[i].split()
        t_rmsd.append(float(tline[indix_dict['rms']]))
        t_pcs1 = float(tline[indix_dict['pcsTs1']])
        t_pcs2 = float(tline[indix_dict['pcsTs2']])
        t_pcs3 = float(tline[indix_dict['pcsTs3']])
        t_pcs_total = t_pcs1+t_pcs2+t_pcs3
        t_pcs.append(t_pcs_total)
        t_score.append(float(tline[indix_dict['score']]))
    X_rmsd.append(t_rmsd)
    Y_pcs.append(t_pcs)
    Y_total.append(t_score)
for i in range(0,11):
    # plt.plot(X_rmsd[i], Y_total[i], color=color_map[i], linestyle='point', marker ='', markersize=12)
    # plt.scatter(X_rmsd[i], Y_total[i], color=color_map[i])
    plt.scatter(X_rmsd[i], Y_pcs[i], color=color_map[i])
plt.xlim((0,25))
plt.xlabel('RMSD [$\AA \angstrom$]')
plt.title('All atom mode')

save_file=protein+"_combined_PCS.png"
plt.savefig(save_file,dpi=500, format=None, orientation ='landscape', papertype= 'a4')

#cp_file = "cp *_combined.png ../../"

#os.system(cp_file)
