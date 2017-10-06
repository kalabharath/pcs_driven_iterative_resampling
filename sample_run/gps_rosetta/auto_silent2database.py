import itertools
import sys, os
import time

def extract_top_pdbs(desc, scores, iteration, protein):
    silent_file = "-in:file:silent top_relax_top_" + protein + "_r"+str(iteration)+".silent_file "
    infile = "pcs_"+protein+"_relax_top_rescore_r"+str(iteration)+".fsc"
    tdesc = ' '
    final_result = open("Final_results.txt", 'w')
    for i in  range(0, 10):
        tdesc = tdesc + desc[scores[i]][:-5]+" "
        tline = "top scoring decoy is: rank: "+str(i+1)+" ; and the pdb file is :"+desc[scores[i]][:-5]+".pdb\n"
        final_result.write(tline)
        print "top scoring files are: rank: ", i+1, " pdb file is :", desc[scores[i]][:-5], ".pdb"
    print tdesc
    tline = "Ranked based on PCS energies, extracted from file "+infile+"\n"
    final_result.write(tline)
    tline = "PDB files are extracted from the silent file "+"top_relax_top_" + protein + "_r"+str(iteration)+".silent_file \n"
    final_result.write(tline)
    final_result.close()
    tags = "-in:file:tags "+tdesc
    exe_path = (os.popen("sed -n '3p' config.txt").read()).rstrip()
    exe_path = exe_path.split("=")
    exe_path = exe_path[1]
    print exe_path
    exe_path = exe_path.split("/")
    print exe_path
    new_path = ''
    for i in range(1,len(exe_path)-1):
        new_path = new_path+'/'+exe_path[i]
    new_path = new_path+"/"+"extract_pdbs.mpi.linuxgccrelease "
    database_path = (os.popen("sed -n '5p' config.txt").read()).rstrip()
    database_path = database_path.split("=")
    database_path = '-database ' + database_path[1]

    mpirun= "mpirun -np 2 "
    run = mpirun+new_path+database_path+" "+silent_file+tags
    print run
    os.system(run)
    return True

def checkConvergence(protein, current_iter):

    lowest_score = []
    desc = []
    for i in range(0, current_iter+1):

        infile = "pcs_"+protein+"_relax_top_rescore_r"+str(i)+".fsc"
        print infile
        with open(infile) as fin:
            lines = fin.readlines()

        wts_file=protein+"_r"+str(i)+".wts"
        fin = open(wts_file,'r')
        wts = fin.readlines()
        current_wts = []
        tags = []
        for wt in wts:
            tag, wf = wt.split("=")
            current_wts.append(float(wf))
            tags.append(tag)
        tag_indices = []
        tline = lines[0].split()
        print tline
        for j in range(0, len(tline)):
            tentry = tline[j].strip()
            for tag in tags:
                tag = tag.strip()
                if tentry == tag:
                    tag_indices.append(j)
        t = []
        file_desc = {}
        for k in range(1,len(lines)):
            sline=lines[k].split()
            # use normalised pcs
            if sline[0]=='SCORE:':
                total_pcs_score = 0
                for j in range(0, len(tag_indices)):
                    total_pcs_score = total_pcs_score + float(sline[tag_indices[j]])/current_wts[j]
                total_pcs_score = round(total_pcs_score, 3)
                t.append(total_pcs_score)
                file_desc[total_pcs_score] = sline[-1]
        t.sort()
        lowest_score.append(t)
        desc.append(file_desc)
    for q in range(1, len(lowest_score)-1):
        if lowest_score[q+1][0] >= lowest_score[q][0]:
            print "converge achieved at iteration: ", q
            print "Lowest PCS Energy description is: ", desc[q][lowest_score[q][0]]
            extract_top_pdbs(desc[q], lowest_score[q], q, protein)
            sys.exit()
    return True

def updateIteration(iteration):
    with open("config.txt") as fin:
        lines = fin.readlines()
    fout = open("config.txt", 'w')
    for i in range(0, len(lines) - 1):
        fout.write(lines[i])
    tline = lines[-1].split("=")
    tmp = tline[0] + "=" + str(iteration)
    fout.write(tmp)
    fout.close()
    return True


def setup_variables():
    protein = (os.popen("sed -n '6p' config.txt").read()).rstrip()
    protein = protein.split("=")
    protein = protein[1]
    current_iter = (os.popen("sed -n '8p' config.txt").read()).rstrip()
    current_iter = current_iter.split("=")
    current_iter = int(current_iter[1])
    max_iter = (os.popen("sed -n '7p' config.txt").read()).rstrip()
    max_iter = max_iter.split("=")
    max_iter = int(max_iter[1])
    if (max_iter == current_iter):
        exit()
    return protein, current_iter


def silent2tensor(silentfile, tags):
    f1 = open(silentfile, 'r')
    line1 = f1.readline()
    line2 = f1.readline()
    line = f1.readline()
    description = []
    while (line):
        entries = line.split(' ')
        print entries[-1].rstrip()
        temp = open(entries[-1].rstrip() + str(".silent"), 'w')
        description.append(entries[-1].rstrip())
        temp.write(line1)
        temp.write(line2)
        temp.write(line)
        line = f1.readline()
        while (line[0:5] != 'SCORE'):
            temp.write(line)
            line = f1.readline()
            if ((line == '') or (line == '\n') or (line == ' ')):
                break
        temp.close()
    print description
    for entry in description:
        exe_path = (os.popen("sed -n '3p' config.txt").read()).rstrip()
        exe_path = exe_path.split("=")
        exe_path = exe_path[1]
        database_path = (os.popen("sed -n '5p' config.txt").read()).rstrip()
        database_path = database_path.split("=")
        print database_path
        database_path = '-database ' + database_path[1]
        silentin = "-in:file:silent " + entry + str(".silent")
        extras = "-in:file:fullatom -mute all"
        broker = "-broker::setup ../setup/broker.txt"
        mpi = "mpirun -np 2"
        tensor = ''
        for i in range(0, len(tags)):
            tensor = tensor + "-PCSTS" + str(i + 1) + ":write_extra " + entry + "_Ts" + str(i + 1) + ".tensor  "
        score_wts = "-score:weights pcsweight.patch -mute all"
        run_score = mpi + " " + exe_path + " " + database_path + " " + silentin + " " + tensor + " " + extras + " " + broker + " " + score_wts
        print run_score
        os.system(run_score)
        time.sleep(0.5)
    time.sleep(20)
    return True


def make_dict(array):
    tmp_dict = {}
    for entry in array:
        if (entry[0:1] != '#'):
            res_num, atom_name, PCS_exp, PCS_calc, PCS_dev, PCS_abs_dev = entry.split()
            tmp_dict.setdefault(int(res_num), []).append(float(PCS_abs_dev))
    return tmp_dict


def make_silent_dict(array):
    x = 0
    tmp_silent_dict = {}
    for entry in array:
        if (x == 0):
            const, seq = entry.split()
        x = x + 1
        if (x > 5):
            """   1 H   -64.542  -33.081  175.040    1.458    0.000    0.000    0.000    0.000    0.000    0.000 S_0001S_0001_0001
                  1 L     0.000  -97.653 -179.269    1.458    0.000    0.000 -176.179 -181.398   66.325    0.000 S_0261_0001
             """
            res_num, SStruct, phi, psi, omega, CA_x, CA_y, CA_z, donknow, donknow, donknow, donknow, descripiton = entry.split()
            tmp_silent_dict.setdefault(int(res_num), []).extend(
                [str(SStruct), float(CA_x), float(CA_y), float(CA_z), float(phi), float(psi), float(omega),
                 int(res_num)])
    return seq, tmp_silent_dict


def score(array, dictionary):
    sum_dev = 0
    num = 0
    for entry in array:
        try:
            for abs_dev in dictionary[entry]:
                num = num + 1
                sum_dev = sum_dev + abs_dev
        except:
            pass
    if ((sum_dev <= num * 0.05) and (num >= 4)):
        return True
    else:
        return False


def fourCtwo(score_list):
    combi_list = list(itertools.combinations(score_list, 2))
    for combi in combi_list:
        c1 = combi[0]
        c2 = combi[1]
        if c1 and c2:
            return True
    return False


############################################
######## Config variables  ##########
############################################

pcs_percent_frags = 12
old_percent_frags = 88

db9_dict, db3_dict = {}, {}
frag9_db, frag3_db = {}, {}

protein, current_iter = setup_variables()
if current_iter > 1:
    checkConvergence(protein, current_iter)

silentfile = "top_relax_top_" + protein + "_r" + str(current_iter) + ".silent_file"

wts_file = protein + "_r" + str(current_iter) + ".wts"
fin = open(wts_file, 'r')
wts = fin.readlines()
current_wts = []
tags = []
for wt in wts:
    tag, wf = wt.split("=")
    current_wts.append(float(wf))
    tags.append(tag.strip())
# generate individual silent and tensor files
silent2tensor(silentfile,tags)


# Extract and generate best PCS satisfied fragments.
score_dict = {}
with open("pcs_" + protein + "_relax_top_rescore_r" + str(current_iter) + ".fsc") as fin:
    scorelines = fin.readlines()
    tag_indices = []

tline = scorelines[0].split()
for i in range(0, len(tline)):
    tentry = tline[i].strip()
    for tag in tags:
        tag = tag.strip()
        if tentry == tag:
            tag_indices.append(i)

for i in range(1, len(scorelines)):
    sline = scorelines[i].split()
    # use normalised pcs
    if sline[0] == 'SCORE:':
        total_pcs_score = 0
        for j in range(0, len(tag_indices)):
            total_pcs_score = total_pcs_score + float(sline[tag_indices[j]]) / current_wts[j]
        score_dict[total_pcs_score] = sline[-1][:-5]

scores = score_dict.keys()
scores.sort()

top_100 = []
for j in range(0, 100):
    decoy = score_dict[scores[j]]
    top_100.append(decoy)

print top_100, len(top_100)

for file in top_100:
    file = file + ".silent"
    ktemp = []
    silentin = open(file, 'r')
    file = file[:-7]
    # read in all the tensor files
    tag_dicts = []
    for i in range(0, len(tags)):
        ten_file = file + "_Ts" + str(i + 1) + ".tensor"
        with open(ten_file) as fin:
            tdict = make_dict(fin.readlines())
            tag_dicts.append(tdict)

    seq, silent_dict = make_silent_dict(silentin.readlines())
    residue_list = silent_dict.keys()
    residue_list.sort()
    for i in range(0, len(residue_list)):
        window = residue_list[i:i + 9]
        tmp_seq = seq[i:i + 9]

        if (len(window) == 9):
            tscores = []

            for t in range(0, len(tags)):
                tscores.append(score(window, tag_dicts[t]))

            if len(tscores) == 4:
                if fourCtwo(tscores):
                    db9_dict.setdefault((i + 1), [])
                    for j in range(0, len(window)):
                        # pdb  AA SS  Pf#  Pb#   V# BFactor     CA_x     CA_y     CA_z      Phi      Psi    Omega
                        db9_dict.setdefault((i + 1), []).append(
                            [file[2:6], file[0], (i + j + 1), tmp_seq[j], silent_dict[window[j]][0],
                             silent_dict[window[j]][4], silent_dict[window[j]][5], silent_dict[window[j]][6]])
                    for k in range(0, (len(window) - 3)):
                        if ((i + k + 1) in ktemp):
                            break
                        else:
                            ktemp.append((i + k + 1))
                            db3_dict.setdefault((i + k + 1), [])
                        for l in range(k, k + 3):
                            db3_dict.setdefault((i + k + 1), []).append(
                                [file[2:6], file[0], (i + l + 1), tmp_seq[l], silent_dict[window[l]][0],
                                 silent_dict[window[l]][4], silent_dict[window[l]][5], silent_dict[window[l]][6]])

            elif len(tscores) == 3:
                if ((tscores[0] and tscores[1]) or (tscores[1] and tscores[2]) or (
                    tscores[0] and tscores[2])):  # combination of two pairs
                    db9_dict.setdefault((i + 1), [])
                    for j in range(0, len(window)):
                        # pdb  AA SS  Pf#  Pb#   V# BFactor     CA_x     CA_y     CA_z      Phi      Psi    Omega
                        db9_dict.setdefault((i + 1), []).append(
                            [file[2:6], file[0], (i + j + 1), tmp_seq[j], silent_dict[window[j]][0],
                             silent_dict[window[j]][4], silent_dict[window[j]][5], silent_dict[window[j]][6]])
                    for k in range(0, (len(window) - 3)):
                        if ((i + k + 1) in ktemp):
                            break
                        else:
                            ktemp.append((i + k + 1))
                            db3_dict.setdefault((i + k + 1), [])
                        for l in range(k, k + 3):
                            db3_dict.setdefault((i + k + 1), []).append(
                                [file[2:6], file[0], (i + l + 1), tmp_seq[l], silent_dict[window[l]][0],
                                 silent_dict[window[l]][4], silent_dict[window[l]][5], silent_dict[window[l]][6]])
            else:
                print " Data from atleast 3 tags are needed. will not run without them"
                exit()

    silentin.close()

print "Generating new Fragment files "

database = open("frag9_" + protein + "_r" + str(current_iter + 1) + ".tab", 'w')  # output frag9_ file suffix
database2 = open("frag3_" + protein + "_r" + str(current_iter + 1) + ".tab", 'w')  # output frag3_ file suffix
frag9 = open("frag9_" + protein + "_r0.tab", 'r')  # 9mer fragment database for the given protein
frag3 = open("frag3_" + protein + "_r0.tab", 'r')  # 3mer fragment database for the given protein

################################################################
######## Read in the server generated frag9 file ##########
###############################################################


# postion:            1 neighbors:          200

for p in range(0, (len(residue_list) - 8)):
    line_9 = frag9.readline()  # read positions
    try:
        posk, res_window, neigh, pdb_nos = line_9.split()
    except:
        continue
    frag9_db.setdefault(int(res_window), [])
    for q in range(0, int(pdb_nos)):  # iterate 200 times or number of neighbours as specified in the fragment library
        line_9 = frag9.readline()  # read the empty line
        for r in range(0, 9):
            line_9 = frag9.readline()  # read the fragment entry
            # 2o6k A    56 P L  -64.328  149.443 -179.819   24.380    6.894    13.912 9     0.000 P  1 F  1
            frag9_db.setdefault(int(res_window), []).append(
                [line_9[1:5], line_9[5:7], line_9[7:13], line_9[13:15], line_9[15:17], line_9[17:26], line_9[26:35],
                 line_9[35:44]])
    line_9 = frag9.readline()  # read the empty line
print "Read old frag9 file"
################################################################
######## Read in the server generated frag3 file ##########
###############################################################

for p in range(0, (len(residue_list) - 2)):
    line_3 = frag3.readline()  # read positions
    try:
        posk, res_window, neigh, pdb_nos = line_3.split()
    except:
        continue
    frag3_db.setdefault(int(res_window), [])
    for q in range(0, int(pdb_nos)):  # iterate 200 times or number of neighbours as specified in the fragment library
        line_3 = frag3.readline()  # read the empty line
        for r in range(0, 3):
            line_3 = frag3.readline()  # read the fragment entry
            # 2o6k A    56 P L  -64.328  149.443 -179.819   24.380    6.894    13.912 9     0.000 P  1 F  1
            frag3_db.setdefault(int(res_window), []).append(
                [line_3[1:5], line_3[5:7], line_3[7:13], line_3[13:15], line_3[15:17], line_3[17:26], line_3[26:35],
                 line_3[35:44]])
    line_3 = frag3.readline()  # read the empty line

print "Read old frag3 file"

##############################################
######## Write out the frag9 file ##########
#############################################
t_count = 0
for pos in range(1, (len(residue_list) - 7)):
    if db9_dict.has_key(pos) == frag9_db.has_key(pos):
        t_count += 1

        no_of_entries = (len(db9_dict.get(pos))) / 9
        print pos, t_count, no_of_entries
        # determine number of iterations for pcs_frags and number of entries from old_library

        old_entries = int((old_percent_frags * 200) / 100.0)
        pcs_entries = int((pcs_percent_frags * 200) / 100.0)

        # round off the iterations in biasing pcs_entries

        iters = int(pcs_entries / no_of_entries)

        if (iters == 0):
            iters = 1

        if (iters * no_of_entries < pcs_entries):
            old_entries = old_entries + (pcs_entries - (iters * no_of_entries))
            pcs_entries = pcs_entries - (pcs_entries - (iters * no_of_entries))

        if (iters * no_of_entries > pcs_entries):
            old_entries = old_entries - (iters * no_of_entries - pcs_entries)
            pcs_entries = pcs_entries + (iters * no_of_entries - pcs_entries)

        if (pos != 1):
            database.write("\n")
        header = " " + str("position:") + '%13s' % pos + " " + str("neighbors:") + '%13s' % (
        pcs_entries + old_entries) + "\n"
        database.write(header)
        contrl_old = True
        temp = 0
        for iterations in range(0, iters):
            for entry in db9_dict.get(pos):

                if (temp >= (9 * (pcs_entries + old_entries))):
                    contrl_old = False
                    break
                if (temp in range(-9, 20000, 9)):
                    database.write("\n")
                entry_line = " " + str(entry[0]) + '%2s' % str(entry[1]) + '%6d' % entry[2] + '%2s' % entry[3] + '%2s' % \
                                                                                                                 entry[
                                                                                                                     4] + '%9.3f' % \
                                                                                                                          entry[
                                                                                                                              5] + '%9.3f' % \
                                                                                                                                   entry[
                                                                                                                                       6] + '%9.3f' % \
                                                                                                                                            entry[
                                                                                                                                                7] + "\n"
                database.write(entry_line)
                temp = temp + 1
        if (contrl_old):
            for entry in frag9_db.get(pos):
                if (temp >= (9 * (pcs_entries + old_entries))):
                    break
                if (temp in range(0, 20000, 9)):
                    database.write("\n")
                entry_line = " " + str(entry[0]) + str(entry[1]) + entry[2] + entry[3] + entry[4] + entry[5] + entry[
                    6] + entry[7] + "\n"
                database.write(entry_line)
                temp = temp + 1

    else:
        no_of_entries = (len(frag9_db.get(pos))) / 9
        if (pos != 1):
            database.write("\n")
        header = " " + str("position:") + '%13s' % pos + " " + str("neighbors:") + '%13s' % no_of_entries + "\n"
        database.write(header)
        temp = 0
        for entry in frag9_db.get(pos):
            if (temp in range(-9, 20000, 9)):
                database.write("\n")
            entry_line = " " + str(entry[0]) + str(entry[1]) + entry[2] + entry[3] + entry[4] + entry[5] + entry[6] + \
                         entry[7] + "\n"
            database.write(entry_line)
            temp = temp + 1

print "Generated new frag9 file " + str(database)

##############################################
######## Write out the frag3 file ##########
#############################################

for pos2 in range(1, (len(residue_list) - 1)):
    if db3_dict.has_key(pos2) == frag3_db.has_key(pos2):
        no_of_entries2 = (len(db3_dict.get(pos2))) / 3

        # determine number of iterations for pcs_frags and number of entries from old_library

        old_entries2 = int((old_percent_frags * 200) / 100.0)
        pcs_entries2 = int((pcs_percent_frags * 200) / 100.0)

        # round off the iterations in biasing pcs_entries

        iters2 = int(pcs_entries2 / no_of_entries2)

        if (iters2 == 0):
            iters2 = 1

        if (iters2 * no_of_entries2 < pcs_entries2):
            old_entries2 = old_entries2 + (pcs_entries2 - (iters2 * no_of_entries2))
            pcs_entries2 = pcs_entries2 - (pcs_entries2 - (iters2 * no_of_entries2))

        if (iters2 * no_of_entries2 > pcs_entries2):
            old_entries2 = old_entries2 - (iters2 * no_of_entries2 - pcs_entries2)
            pcs_entries2 = pcs_entries2 + (iters2 * no_of_entries2 - pcs_entries2)

        if (pos2 != 1):
            database2.write("\n")

        header = " " + str("position:") + '%13s' % pos2 + " " + str("neighbors:") + '%13s' % (
        pcs_entries2 + old_entries2) + "\n"
        database2.write(header)
        contrl_old = True
        temp2 = 0
        for iteration in range(0, iters2):
            for entry2 in db3_dict.get(pos2):
                if (temp2 >= (3 * (pcs_entries2 + old_entries2))):
                    contrl_old = False
                    break
                if (temp2 in range(-3, 20000, 3)):
                    database2.write("\n")
                entry2_line = " " + str(entry2[0]) + '%2s' % str(entry2[1]) + '%6d' % entry2[2] + '%2s' % entry2[
                    3] + '%2s' % entry2[4] + '%9.3f' % entry2[5] + '%9.3f' % entry2[6] + '%9.3f' % entry2[7] + "\n"
                database2.write(entry2_line)
                temp2 = temp2 + 1
        if (contrl_old):
            for entry2 in frag3_db.get(pos2):
                if (temp2 >= (3 * (pcs_entries2 + old_entries2))):
                    break
                if (temp2 in range(0, 20000, 3)):
                    database2.write("\n")
                entry2_line = " " + str(entry2[0]) + str(entry2[1]) + entry2[2] + entry2[3] + entry2[4] + entry2[5] + \
                              entry2[6] + entry2[7] + "\n"
                database2.write(entry2_line)
                temp2 = temp2 + 1
    else:
        no_of_entries2 = (len(frag3_db.get(pos2))) / 3
        if (pos2 != 1):
            database2.write("\n")
        header = " " + str("position:") + '%13s' % pos2 + " " + str("neighbors:") + '%13s' % no_of_entries2 + "\n"
        database2.write(header)
        temp2 = 0
        for entry2 in frag3_db.get(pos2):
            if (temp2 in range(-3, 20000, 3)):
                database2.write("\n")
            entry2_line = " " + str(entry2[0]) + str(entry2[1]) + entry2[2] + entry2[3] + entry2[4] + entry2[5] + \
                          entry2[6] + entry2[7] + "\n"
            database2.write(entry2_line)
            temp2 = temp2 + 1
print "Generated new frag3 file " + str(database2)
print "all done"
database.close()
database2.close()
updateIteration(current_iter + 1)
rm_files = "rm S_* "
os.system(rm_files)
cp_wts = "cp " + protein + "_r0.wts " + protein + "_r" + str(current_iter + 1) + ".wts"
os.system(cp_wts)
os.system("qsub auto_iter.sh")
