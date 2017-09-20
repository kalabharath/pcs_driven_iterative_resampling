import sys, os,time

def setup_variables():
    protein=(os.popen("sed -n '6p' config.txt").read()).rstrip()
    protein = protein.split("=")
    protein = protein[1]
    current_iter=(os.popen("sed -n '8p' config.txt").read()).rstrip()
    current_iter = current_iter.split("=")
    current_iter = current_iter[1]
    silentfile = protein+str("_r")+str(current_iter)+str(".silent_file")
    return silentfile, protein, current_iter

silentfile, protein, current_iter = setup_variables()
filein=open(silentfile,'r')
lines=filein.readlines()
filein.close()

wts_file=protein+"_r"+str(current_iter)+".wts"
fin = open(wts_file,'r')
wts = fin.readlines()
current_wts = []
tags = []
for wt in wts:
    tag, wf = wt.split("=")
    current_wts.append(float(wf))
    tags.append(tag)

print "Reading entries in :", silentfile
score_dict={}
tag_indices = []
tline = lines[1].split()

for i in range(0, len(tline)):
    tentry = tline[i].strip()
    for tag in tags:
        tag = tag.strip()
        if tentry == tag:
            tag_indices.append(i)


for i in range(2,len(lines)):
    sline=lines[i].split()
    # use normalised pcs
    if sline[0]=='SCORE:':
        total_pcs_score = 0
        for j in range(0, len(tag_indices)):
            total_pcs_score = total_pcs_score + float(sline[tag_indices[j]])/current_wts[j]
        score_dict[total_pcs_score] = sline[-1]

fileout=open(str("top_")+silentfile,'w')
scores=score_dict.keys()
scores.sort()

top_200=[]

for j in range(0,200):
    decoy=score_dict[scores[j]]
    top_200.append(decoy)

print "top_200 entries are :\n ", top_200

for x in range (0,2):
    fileout.write(lines[x])

for i in range(2,len(lines)):
    line=lines[i].split()
    if (line[0]=='SCORE:') and (line[-1] in top_200):
        fileout.write(lines[i])
        i=i+1
        line=lines[i].split()
        while (line[0]!='SCORE:'):
            fileout.write(lines[i])
            i=i+1
            line=lines[i].split()

fileout.close()
# give a min to write to disk before you start your next job
time.sleep(60)
exit()
