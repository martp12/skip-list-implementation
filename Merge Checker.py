factor = 2

gap = 8 * factor

gap_0 = 1 # 0-gap
gap_1 = 0 # 1-gap
gap_2 = 0 # 2-gap
gap_3 = 4 # 3-gap
gap_4 = 8 # 4-gap
gap_5 = 10 # 5-gap
gap_6 = 12 # 6-gap
gap_7 = 14 # 7-gap
gap_8 = 16 # 8-gap
gap_9 = 18 # 9-gap

pointer = 1

fout = open('merge_check_result.txt', 'w')


# Merge gap 0
fout.write("Merge Gaps, left = 0" + '\n')
fout.write(str(- gap_0 - gap_0 + gap_0) + '\n')
fout.write(str(- gap_0 - gap_1 + gap_1) + '\n')
fout.write(str(- gap_0 - gap_2 + gap_2) + '\n')
fout.write(str(- gap_0 - gap_3 + gap_3) + '\n')
fout.write(str(- gap_0 - gap_4 + gap_4) + '\n')
fout.write(str(- gap_0 - gap_5 + gap_5) + '\n')

# Merge gap 1
fout.write("Merge Gaps, left = 0" + '\n')
fout.write(str(- gap_1 - gap_0 + gap_1) + '\n')
fout.write(str(- gap_1 - gap_1 + gap_2) + '\n')
fout.write(str(- gap_1 - gap_2 + gap_3) + '\n')
fout.write(str(- gap_1 - gap_3 + gap_4) + '\n')
fout.write(str(- gap_1 - gap_4 + gap_5) + '\n')
fout.write(str(- gap_1 - gap_5 + gap_6) + '\n')

# Merge gap 2
fout.write("Merge Gaps, left = 0" + '\n')
fout.write(str(- gap_2 - gap_0 + gap_2) + '\n')
fout.write(str(- gap_2 - gap_1 + gap_3) + '\n')
fout.write(str(- gap_2 - gap_2 + gap_4) + '\n')
fout.write(str(- gap_2 - gap_3 + gap_5) + '\n')
fout.write(str(- gap_2 - gap_4 + gap_6) + '\n')
fout.write(str(- gap_2 - gap_5 + gap_7) + '\n')

# Merge gap 3
fout.write("Merge Gaps, left = 0" + '\n')
fout.write(str(- gap_3 - gap_0 + gap_3) + '\n')
fout.write(str(- gap_3 - gap_1 + gap_4) + '\n')
fout.write(str(- gap_3 - gap_2 + gap_5) + '\n')
fout.write(str(- gap_3 - gap_3 + gap_6) + '\n')
fout.write(str(- gap_3 - gap_4 + gap_7) + '\n')
fout.write(str(- gap_3 - gap_5 + gap_8) + '\n')

# Merge gap 4
fout.write("Merge Gaps, left = 0" + '\n')
fout.write(str(- gap_4 - gap_0 + gap_4) + '\n')
fout.write(str(- gap_4 - gap_1 + gap_5) + '\n')
fout.write(str(- gap_4 - gap_2 + gap_6) + '\n')
fout.write(str(- gap_4 - gap_3 + gap_7) + '\n')
fout.write(str(- gap_4 - gap_4 + gap_8) + '\n')
fout.write(str(- gap_4 - gap_5 + gap_9) + '\n')

fout.close()

print("")
fin = open('merge_check_result.txt')
for i, line in enumerate(fin):
    try:
        if float(line) > 0:
            print('Error on line ' + str(i + 1))
    except:
        pass
