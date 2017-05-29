gap_0 = 1 # 0-gap
gap_1 = 0 # 1-gap
gap_2 = 0 # 2-gap
gap_3 = 4 # 3-gap
gap_4 = 8  # 4-gap
gap_5 = 10 # 5-gap
gap_6 = 12 # 6-gap
gap_7 = 14 # 7-gap
gap_8 = 16 # 8-gap
gap_9 = 18 # 9-gap

pointer = 1

fout = open('potential_function_check_result.txt', 'w')

# From gap 0
fout.write("LB gap 0 start" + '\n')
fout.write(str(- gap_0 - gap_1 - gap_0 + gap_0 + gap_0 + gap_1 - pointer) + '\n')
fout.write(str(- gap_0 - gap_2 - gap_0 + gap_1 + gap_1 - pointer) + '\n')
fout.write(str(- gap_0 - gap_3 - gap_0 + gap_2 + gap_1 - pointer) + '\n')
fout.write(str(- gap_0 - gap_4 - gap_0 + gap_3 + gap_1 - pointer) + '\n')
fout.write(str(- gap_0 - gap_5 - gap_0 + gap_4 + gap_1 - pointer) + '\n')
fout.write(str(- gap_0 - gap_6 - gap_0 + gap_5 + gap_1 - pointer) + '\n')


# From gap 1
fout.write("LB gap 1 start" + '\n')
fout.write(str(- gap_1 - gap_1 - gap_0 + gap_2 + gap_0 - pointer) + '\n')
fout.write(str(- gap_1 - gap_2 - gap_0 + gap_2 + gap_1 - pointer) + '\n')
fout.write(str(- gap_1 - gap_3 - gap_0 + gap_2 + gap_2 - pointer) + '\n')
fout.write(str(- gap_1 - gap_4 - gap_0 + gap_2 + gap_3 - pointer) + '\n')
fout.write(str(- gap_1 - gap_5 - gap_0 + gap_2 + gap_4 - pointer) + '\n')
fout.write(str(- gap_1 - gap_6 - gap_0 + gap_2 + gap_5 - pointer) + '\n')


# Borrow 1 node due to lower bound conflict
fout.write("LB gap 2 start" + '\n')
fout.write(str(- gap_2 - gap_1 - gap_0 + gap_1 + gap_1 + gap_1) + '\n')
fout.write(str(- gap_2 - gap_2 - gap_0 + gap_1 + gap_2 + gap_1) + '\n')
fout.write(str(- gap_2 - gap_3 - gap_0 + gap_1 + gap_3 + gap_1) + '\n')
fout.write(str(- gap_2 - gap_4 - gap_0 + gap_1 + gap_4 + gap_1) + '\n')
fout.write(str(- gap_2 - gap_5 - gap_0 + gap_1 + gap_5 + gap_1) + '\n')
fout.write(str(- gap_2 - gap_6 - gap_0 + gap_1 + gap_6 + gap_1) + '\n')

# Borrow 2 nodes due to lower bound conflict
fout.write("LB gap 3 start" + '\n')
fout.write(str(- gap_3 - gap_1 - gap_0 + gap_1 + gap_1 + gap_2) + '\n')
fout.write(str(- gap_3 - gap_2 - gap_0 + gap_1 + gap_2 + gap_2) + '\n')
fout.write(str(- gap_3 - gap_3 - gap_0 + gap_1 + gap_3 + gap_2) + '\n')
fout.write(str(- gap_3 - gap_4 - gap_0 + gap_1 + gap_4 + gap_2) + '\n')
fout.write(str(- gap_3 - gap_5 - gap_0 + gap_1 + gap_5 + gap_2) + '\n')
fout.write(str(- gap_3 - gap_6 - gap_0 + gap_1 + gap_6 + gap_2) + '\n')

# From gap 4
fout.write("LB gap 4 start" + '\n')
fout.write(str(- gap_4 - gap_1 - gap_0 + gap_2 + gap_1 + gap_2) + '\n')
fout.write(str(- gap_4 - gap_2 - gap_0 + gap_2 + gap_2 + gap_2) + '\n')
fout.write(str(- gap_4 - gap_3 - gap_0 + gap_2 + gap_3 + gap_2) + '\n')
fout.write(str(- gap_4 - gap_4 - gap_0 + gap_2 + gap_4 + gap_2) + '\n')
fout.write(str(- gap_4 - gap_5 - gap_0 + gap_2 + gap_5 + gap_2) + '\n')
fout.write(str(- gap_4 - gap_6 - gap_0 + gap_2 + gap_6 + gap_2) + '\n')

# From gap 5
fout.write("LB gap 5 start" + '\n')
fout.write(str(- gap_5 - gap_1 - gap_0 + gap_3 + gap_1 + gap_2) + '\n')
fout.write(str(- gap_5 - gap_2 - gap_0 + gap_3 + gap_2 + gap_2) + '\n')
fout.write(str(- gap_5 - gap_3 - gap_0 + gap_3 + gap_3 + gap_2) + '\n')
fout.write(str(- gap_5 - gap_4 - gap_0 + gap_3 + gap_4 + gap_2) + '\n')
fout.write(str(- gap_5 - gap_5 - gap_0 + gap_3 + gap_5 + gap_2) + '\n')
fout.write(str(- gap_5 - gap_6 - gap_0 + gap_3 + gap_6 + gap_2) + '\n')

# From gap 6
fout.write("LB gap 6 start" + '\n')
fout.write(str(- gap_6 - gap_1 - gap_0 + gap_4 + gap_1 + gap_2) + '\n')
fout.write(str(- gap_6 - gap_2 - gap_0 + gap_4 + gap_2 + gap_2) + '\n')
fout.write(str(- gap_6 - gap_3 - gap_0 + gap_4 + gap_3 + gap_2) + '\n')
fout.write(str(- gap_6 - gap_4 - gap_0 + gap_4 + gap_4 + gap_2) + '\n')
fout.write(str(- gap_6 - gap_5 - gap_0 + gap_4 + gap_5 + gap_2) + '\n')
fout.write(str(- gap_6 - gap_6 - gap_0 + gap_4 + gap_6 + gap_2) + '\n')

# From gap 7
fout.write("LB gap 7 start" + '\n')
fout.write(str(- gap_7 - gap_1 - gap_0 + gap_5 + gap_1 + gap_2) + '\n')
fout.write(str(- gap_7 - gap_2 - gap_0 + gap_5 + gap_2 + gap_2) + '\n')
fout.write(str(- gap_7 - gap_3 - gap_0 + gap_5 + gap_3 + gap_2) + '\n')
fout.write(str(- gap_7 - gap_4 - gap_0 + gap_5 + gap_4 + gap_2) + '\n')
fout.write(str(- gap_7 - gap_5 - gap_0 + gap_5 + gap_5 + gap_2) + '\n')
fout.write(str(- gap_7 - gap_6 - gap_0 + gap_5 + gap_6 + gap_2) + '\n')

# From gap 8
fout.write("LB gap 8 start" + '\n')
fout.write(str(- gap_8 - gap_1 - gap_0 + gap_6 + gap_1 + gap_2) + '\n')
fout.write(str(- gap_8 - gap_2 - gap_0 + gap_6 + gap_2 + gap_2) + '\n')
fout.write(str(- gap_8 - gap_3 - gap_0 + gap_6 + gap_3 + gap_2) + '\n')
fout.write(str(- gap_8 - gap_4 - gap_0 + gap_6 + gap_4 + gap_2) + '\n')
fout.write(str(- gap_8 - gap_5 - gap_0 + gap_6 + gap_5 + gap_2) + '\n')
fout.write(str(- gap_8 - gap_6 - gap_0 + gap_6 + gap_6 + gap_2) + '\n')

# From gap 9
fout.write("LB gap 9 start" + '\n')
fout.write(str(- gap_9 - gap_1 - gap_0 + gap_7 + gap_1 + gap_2) + '\n')
fout.write(str(- gap_9 - gap_2 - gap_0 + gap_7 + gap_2 + gap_2) + '\n')
fout.write(str(- gap_9 - gap_3 - gap_0 + gap_7 + gap_3 + gap_2) + '\n')
fout.write(str(- gap_9 - gap_4 - gap_0 + gap_7 + gap_4 + gap_2) + '\n')
fout.write(str(- gap_9 - gap_5 - gap_0 + gap_7 + gap_5 + gap_2) + '\n')
fout.write(str(- gap_9 - gap_6 - gap_0 + gap_7 + gap_6 + gap_2) + '\n')

# Raising due x-2'th node upper bound conflict
# From gap 4
fout.write("UB gap 4 start" + '\n')
fout.write(str(- gap_4 - gap_0 + gap_1 + gap_1 + gap_2 + pointer) + '\n')
fout.write(str(- gap_4 - gap_1 + gap_1 + gap_2 + gap_2 + pointer) + '\n')
fout.write(str(- gap_4 - gap_2 + gap_1 + gap_3 + gap_2 + pointer) + '\n')
fout.write(str(- gap_4 - gap_3 + gap_1 + gap_4 + gap_2 + pointer) + '\n')
fout.write(str(- gap_4 - gap_4 + gap_1 + gap_5 + gap_2 + pointer) + '\n')
fout.write(str(- gap_4 - gap_5 + gap_1 + gap_6 + gap_2 + pointer) + '\n')

# From gap 5
fout.write("UB gap 5 start" + '\n')
fout.write(str(- gap_5 - gap_0 + gap_2 + gap_1 + gap_2 + pointer) + '\n')
fout.write(str(- gap_5 - gap_1 + gap_2 + gap_2 + gap_2 + pointer) + '\n')
fout.write(str(- gap_5 - gap_2 + gap_2 + gap_3 + gap_2 + pointer) + '\n')
fout.write(str(- gap_5 - gap_3 + gap_2 + gap_4 + gap_2 + pointer) + '\n')
fout.write(str(- gap_5 - gap_4 + gap_2 + gap_5 + gap_2 + pointer) + '\n')
fout.write(str(- gap_5 - gap_5 + gap_2 + gap_6 + gap_2 + pointer) + '\n')

# From gap 6
fout.write("UB gap 6 start" + '\n')
fout.write(str(- gap_6 - gap_0 + gap_3 + gap_1 + gap_2 + pointer) + '\n')
fout.write(str(- gap_6 - gap_1 + gap_3 + gap_2 + gap_2 + pointer) + '\n')
fout.write(str(- gap_6 - gap_2 + gap_3 + gap_3 + gap_2 + pointer) + '\n')
fout.write(str(- gap_6 - gap_3 + gap_3 + gap_4 + gap_2 + pointer) + '\n')
fout.write(str(- gap_6 - gap_4 + gap_3 + gap_5 + gap_2 + pointer) + '\n')
fout.write(str(- gap_6 - gap_5 + gap_3 + gap_6 + gap_2 + pointer) + '\n')

# From gap 7
fout.write("UB gap 7 start" + '\n')
fout.write(str(- gap_7 - gap_0 + gap_4 + gap_1 + gap_2 + pointer) + '\n')
fout.write(str(- gap_7 - gap_1 + gap_4 + gap_2 + gap_2 + pointer) + '\n')
fout.write(str(- gap_7 - gap_2 + gap_4 + gap_3 + gap_2 + pointer) + '\n')
fout.write(str(- gap_7 - gap_3 + gap_4 + gap_4 + gap_2 + pointer) + '\n')
fout.write(str(- gap_7 - gap_4 + gap_4 + gap_5 + gap_2 + pointer) + '\n')
fout.write(str(- gap_7 - gap_5 + gap_4 + gap_6 + gap_2 + pointer) + '\n')

# From gap 8
fout.write("UB gap 8 start" + '\n')
fout.write(str(- gap_8 - gap_0 + gap_5 + gap_1 + gap_2 + pointer) + '\n')
fout.write(str(- gap_8 - gap_1 + gap_5 + gap_2 + gap_2 + pointer) + '\n')
fout.write(str(- gap_8 - gap_2 + gap_5 + gap_3 + gap_2 + pointer) + '\n')
fout.write(str(- gap_8 - gap_3 + gap_5 + gap_4 + gap_2 + pointer) + '\n')
fout.write(str(- gap_8 - gap_4 + gap_5 + gap_5 + gap_2 + pointer) + '\n')
fout.write(str(- gap_8 - gap_5 + gap_5 + gap_6 + gap_2 + pointer) + '\n')

# From gap 9
fout.write("UB gap 9 start" + '\n')
fout.write(str(- gap_9 - gap_0 + gap_6 + gap_1 + gap_2 + pointer) + '\n')
fout.write(str(- gap_9 - gap_1 + gap_6 + gap_2 + gap_2 + pointer) + '\n')
fout.write(str(- gap_9 - gap_2 + gap_6 + gap_3 + gap_2 + pointer) + '\n')
fout.write(str(- gap_9 - gap_3 + gap_6 + gap_4 + gap_2 + pointer) + '\n')
fout.write(str(- gap_9 - gap_4 + gap_6 + gap_5 + gap_2 + pointer) + '\n')
fout.write(str(- gap_9 - gap_5 + gap_6 + gap_6 + gap_2 + pointer) + '\n')

fout.close()


fout_merge = open('merge_check_result.txt', 'w')

# Merge gap 0
fout_merge.write("Merge Gaps, left = 0" + '\n')
fout_merge.write(str(- gap_0 - gap_0 + gap_0) + '\n')
fout_merge.write(str(- gap_0 - gap_1 + gap_1) + '\n')
fout_merge.write(str(- gap_0 - gap_2 + gap_2) + '\n')
fout_merge.write(str(- gap_0 - gap_3 + gap_3) + '\n')
fout_merge.write(str(- gap_0 - gap_4 + gap_4) + '\n')
fout_merge.write(str(- gap_0 - gap_5 + gap_5) + '\n')

# Merge gap 1
fout_merge.write("Merge Gaps, left = 1" + '\n')
fout_merge.write(str(- gap_1 - gap_0 + gap_1) + '\n')
fout_merge.write(str(- gap_1 - gap_1 + gap_2) + '\n')
fout_merge.write(str(- gap_1 - gap_2 + gap_3) + '\n')
fout_merge.write(str(- gap_1 - gap_3 + gap_4) + '\n')
fout_merge.write(str(- gap_1 - gap_4 + gap_5) + '\n')
fout_merge.write(str(- gap_1 - gap_5 + gap_6) + '\n')

# Merge gap 2
fout_merge.write("Merge Gaps, left = 2" + '\n')
fout_merge.write(str(- gap_2 - gap_0 + gap_2) + '\n')
fout_merge.write(str(- gap_2 - gap_1 + gap_3) + '\n')
fout_merge.write(str(- gap_2 - gap_2 + gap_4) + '\n')
fout_merge.write(str(- gap_2 - gap_3 + gap_5) + '\n')
fout_merge.write(str(- gap_2 - gap_4 + gap_6) + '\n')
fout_merge.write(str(- gap_2 - gap_5 + gap_7) + '\n')

# Merge gap 3
fout_merge.write("Merge Gaps, left = 3" + '\n')
fout_merge.write(str(- gap_3 - gap_0 + gap_3) + '\n')
fout_merge.write(str(- gap_3 - gap_1 + gap_4) + '\n')
fout_merge.write(str(- gap_3 - gap_2 + gap_5) + '\n')
fout_merge.write(str(- gap_3 - gap_3 + gap_6) + '\n')
fout_merge.write(str(- gap_3 - gap_4 + gap_7) + '\n')
fout_merge.write(str(- gap_3 - gap_5 + gap_8) + '\n')

# Merge gap 4
fout_merge.write("Merge Gaps, left = 4" + '\n')
fout_merge.write(str(- gap_4 - gap_0 + gap_4) + '\n')
fout_merge.write(str(- gap_4 - gap_1 + gap_5) + '\n')
fout_merge.write(str(- gap_4 - gap_2 + gap_6) + '\n')
fout_merge.write(str(- gap_4 - gap_3 + gap_7) + '\n')
fout_merge.write(str(- gap_4 - gap_4 + gap_8) + '\n')
fout_merge.write(str(- gap_4 - gap_5 + gap_9) + '\n')

fout_merge.close()

print("")
fin = open('potential_function_check_result.txt')
for i, line in enumerate(fin):
    try:
        if float(line) >= 0:
            print('Transform: Error on line ' + str(i + 1))
    except ValueError:
        pass

fin.close()

fin2 = open('merge_check_result.txt')
for i, line in enumerate(fin2):
    try:
        if float(line) > 0:
            print('Merge: Error on line ' + str(i + 1))
    except ValueError:
        pass
fin2.close()