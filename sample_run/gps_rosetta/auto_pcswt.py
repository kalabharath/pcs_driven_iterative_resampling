import collections
import os
protein = (os.popen("sed -n '6p' config.txt").read()).rstrip()
protein = protein.split("=")
protein = protein[1]
os.system("mv score.fsc score_cs.fsc")


#output1 = open(protein + "_score12.wts", 'w', 1)

cs_score = []

with open("score_cs.fsc", 'r') as fin:
    lines = fin.readlines()
for i in range(1, len(lines)):
    tline = lines[i].split()
    try:
        score = float(tline[1])
        cs_score.append(score)
    except:
        pass

pcs_score = collections.defaultdict(list)

with open(protein + "_1_pcs.csc", 'r') as fin:
    lines = fin.readlines()

scores = lines[0].split()
total_tags = {}

for i in range(0, len(scores)):
    if 'pcsTs' in scores[i]:
        total_tags[i] = scores[i]


for i in range(1, len(lines)):
    tline = lines[i].split()
    try:
        indices = total_tags.keys()
        indices.sort()
        for index in indices:
            pcs_score[total_tags[index]].append(float(tline[index]))
    except:
        pass

no_of_tags = pcs_score.keys()
pcs_weights = []
cs_score.sort()
cs_low = sum(cs_score[0:100]) / 100.0
cs_high = sum(cs_score[-100:]) / 100.0

output = open(protein + "_r0.wts", 'w', 1)
relax_wts =  open(protein + "_relax.wts", 'w', 1)
relax_wts.write("METHOD_WEIGHTS ref  0.16 1.7 -0.67 -0.81 0.63 -0.17 0.56 0.24 -0.65 -0.1 -0.34 -0.89 0.02 -0.97 -0.98 -0.37 -0.27 0.29 0.91 0.51 \n")
for i in range(0, len(no_of_tags)):
    tag = 'pcsTs' + str(i + 1)
    tag_score = pcs_score[tag]
    tag_score.sort()
    tag_low = sum(tag_score[0:100]) / 100.0
    tag_high = sum(tag_score[-100:]) / 100.0
    pcs_weights = ((cs_high - cs_low) / (tag_high - tag_low))
    ttag = round(pcs_weights / float(len(no_of_tags)), 3)
    tmp_line = tag + "   =  " + str(ttag) + "\n"
    rtmp_line = tag + "    " + str(ttag) + "\n"
    output.write(tmp_line)
    relax_wts.write(rtmp_line)
output.close()
relax_wts.close()
